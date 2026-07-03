"""Multimodal media generation agent using Atlas Cloud.

The agent turns a marketing brief into a concrete image or video prompt, selects
a live display-console Atlas Cloud model, validates the current input schema,
and prepares a generation request. It is dry-run by default; pass --submit only
after reviewing the selected model, request body, and cost metadata.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import dataclass
from typing import Any

import requests
from dotenv import load_dotenv


MEDIA_BASE_URL = "https://api.atlascloud.ai/api/v1"
MODELS_URL = f"{MEDIA_BASE_URL}/models"
DEFAULT_HEADERS = {
    "Accept": "application/json",
    "User-Agent": "500-ai-agents-atlascloud-media-agent/1.0",
}
TERMINAL_STATUSES = {"completed", "succeeded", "failed"}


class AgentError(RuntimeError):
    """Raised when a recoverable agent step fails."""


@dataclass(frozen=True)
class ModelChoice:
    model: str
    display_name: str
    model_type: str
    schema_url: str
    price: Any


def get_json(url: str, *, headers: dict[str, str] | None = None, timeout: int = 30) -> dict[str, Any]:
    response = requests.get(url, headers={**DEFAULT_HEADERS, **(headers or {})}, timeout=timeout)
    try:
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise AgentError(f"GET {url} failed: {exc}") from exc
    except ValueError as exc:
        raise AgentError(f"GET {url} returned non-JSON data") from exc


def post_json(url: str, payload: dict[str, Any], api_key: str, timeout: int = 60) -> dict[str, Any]:
    response = requests.post(
        url,
        json=payload,
        headers={
            **DEFAULT_HEADERS,
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        timeout=timeout,
    )
    try:
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise AgentError(f"POST {url} failed: {exc}") from exc
    except ValueError as exc:
        raise AgentError(f"POST {url} returned non-JSON data") from exc


def load_console_models(model_type: str) -> list[dict[str, Any]]:
    catalog = get_json(MODELS_URL)
    return [
        model
        for model in catalog.get("data", [])
        if model.get("display_console") is True and model.get("type") == model_type
    ]


def choose_model(model_type: str, keyword: str) -> ModelChoice:
    keyword_norm = keyword.lower()
    matches: list[dict[str, Any]] = []
    for model in load_console_models(model_type):
        searchable = " ".join(
            str(model.get(field, ""))
            for field in ("model", "displayName", "familyDisplayName", "profile", "tags")
        ).lower()
        if keyword_norm in searchable:
            matches.append(model)

    if not matches:
        raise AgentError(f"No display-console {model_type} model matched keyword: {keyword}")

    selected = matches[0]
    schema_url = selected.get("schema")
    if not schema_url:
        raise AgentError(f"Selected model {selected.get('model')} does not expose a schema URL")

    return ModelChoice(
        model=selected["model"],
        display_name=selected.get("displayName") or selected["model"],
        model_type=selected["type"],
        schema_url=schema_url,
        price=selected.get("price"),
    )


def load_input_schema(choice: ModelChoice) -> tuple[dict[str, Any], list[str]]:
    schema = get_json(choice.schema_url)
    input_schema = schema.get("components", {}).get("schemas", {}).get("Input", {})
    properties = input_schema.get("properties", {})
    required = input_schema.get("required", [])
    if not properties:
        raise AgentError(f"Schema for {choice.model} does not include Input.properties")
    return properties, required


def build_media_prompt(brief: str, audience: str, style: str) -> str:
    return (
        f"Create a polished campaign asset for this brief: {brief}. "
        f"Audience: {audience}. "
        f"Style: {style}. "
        "Use a clear composition, strong focal point, and production-ready visual direction."
    )


def parse_extra_json(raw: str | None) -> dict[str, Any]:
    if not raw:
        return {}
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise AgentError(f"--extra-json must be valid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise AgentError("--extra-json must decode to a JSON object")
    return value


def build_request_body(
    choice: ModelChoice,
    properties: dict[str, Any],
    required: list[str],
    prompt: str,
    extra: dict[str, Any],
) -> dict[str, Any]:
    request_body: dict[str, Any] = {"model": choice.model}

    if "prompt" in properties:
        request_body["prompt"] = prompt
    elif "text" in properties:
        request_body["text"] = prompt
    else:
        raise AgentError("Selected model schema has neither 'prompt' nor 'text'")

    allowed_fields = set(properties)
    ignored_fields = sorted(set(extra) - allowed_fields)
    for key, value in extra.items():
        if key in allowed_fields:
            request_body[key] = value

    missing_required = [
        field
        for field in required
        if field not in request_body and field != "model"
    ]
    if missing_required:
        raise AgentError(
            "Missing required schema fields: "
            + ", ".join(missing_required)
            + ". Provide them with --extra-json."
        )

    if ignored_fields:
        print(f"Ignored fields not present in the live schema: {', '.join(ignored_fields)}")

    return request_body


def submit_generation(choice: ModelChoice, request_body: dict[str, Any], api_key: str) -> str:
    endpoint = "generateImage" if choice.model_type == "Image" else "generateVideo"
    result = post_json(f"{MEDIA_BASE_URL}/model/{endpoint}", request_body, api_key)
    prediction_id = result.get("data", {}).get("id")
    if not prediction_id:
        raise AgentError(f"Generation response did not include data.id: {result}")
    return str(prediction_id)


def poll_prediction(prediction_id: str, api_key: str, interval_seconds: int = 5) -> dict[str, Any]:
    headers = {"Authorization": f"Bearer {api_key}"}
    while True:
        result = get_json(
            f"{MEDIA_BASE_URL}/model/prediction/{prediction_id}",
            headers=headers,
            timeout=30,
        )
        status = str(result.get("data", {}).get("status", ""))
        print(f"prediction={prediction_id} status={status}")
        if status in TERMINAL_STATUSES:
            return result
        time.sleep(interval_seconds)


def main() -> int:
    load_dotenv()

    parser = argparse.ArgumentParser(description="Atlas Cloud multimodal media generation agent")
    parser.add_argument("--type", choices=["Image", "Video"], default="Image")
    parser.add_argument("--keyword", default="text-to-image", help="Keyword used to select a live model")
    parser.add_argument("--brief", required=True, help="Campaign or content brief")
    parser.add_argument("--audience", default="general audience", help="Target audience")
    parser.add_argument("--style", default="clean editorial visual style", help="Visual style guidance")
    parser.add_argument("--extra-json", help="Optional JSON object with schema-validated fields")
    parser.add_argument("--submit", action="store_true", help="Submit the generation job after preview")
    parser.add_argument("--poll", action="store_true", help="Poll the submitted job until it finishes")
    args = parser.parse_args()

    choice = choose_model(args.type, args.keyword)
    properties, required = load_input_schema(choice)
    prompt = build_media_prompt(args.brief, args.audience, args.style)
    request_body = build_request_body(
        choice=choice,
        properties=properties,
        required=required,
        prompt=prompt,
        extra=parse_extra_json(args.extra_json),
    )

    preview = {
        "selected_model": choice.__dict__,
        "schema_fields": sorted(properties),
        "required_fields": required,
        "request_body": request_body,
        "submit": args.submit,
    }
    print(json.dumps(preview, indent=2, ensure_ascii=False))

    if not args.submit:
        print("Dry run only. Re-run with --submit after reviewing the request and cost.")
        return 0

    api_key = os.getenv("ATLASCLOUD_API_KEY")
    if not api_key:
        raise AgentError("Set ATLASCLOUD_API_KEY before using --submit.")

    prediction_id = submit_generation(choice, request_body, api_key)
    print(f"Submitted prediction: {prediction_id}")

    if args.poll:
        result = poll_prediction(prediction_id, api_key)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
