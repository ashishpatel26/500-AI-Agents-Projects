"""Research assistant built with the Strands Agents SDK.

Give it a topic. The agent searches the web, reads the results it finds, and
returns a structured brief where every claim carries the source it came from.
The model runs the agent loop: it decides which tools to call, in what order,
and when it has enough to answer. The tools describe themselves through their
docstrings, so the system prompt only sets the agent's role and standards,
never a tool-by-tool script.

Default model: OpenAI gpt-4o-mini. Strands is provider-agnostic, so the same
agent code runs on Anthropic, Gemini, Ollama, or any OpenAI-compatible
endpoint by swapping the model object in build_agent(). See the README.
"""

import argparse
import ipaddress
import os
import re
import socket
import urllib.error
import urllib.parse
import urllib.request
from typing import Literal

from ddgs import DDGS
from dotenv import load_dotenv
from pydantic import BaseModel, Field, HttpUrl
from strands import Agent, tool
from strands.models.openai import OpenAIModel

load_dotenv()


def _is_safe_public_url(url: str) -> bool:
    """Return True only for http(s) URLs that resolve to a public address.

    Blocks non-web schemes (file, gopher, ftp, data) and any host that
    resolves to a loopback, link-local, private, or otherwise reserved
    address. This keeps a model-supplied or prompt-injected URL from reaching
    local files or cloud metadata endpoints.
    """
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        return False
    try:
        infos = socket.getaddrinfo(parsed.hostname, parsed.port or 80, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return False
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_reserved
            or ip.is_multicast
            or ip.is_unspecified
        ):
            return False
    return True


# --- Tools -----------------------------------------------------------------
# Each tool's docstring is the contract the model reads. It states what the
# tool returns and when it is the right one to call, so the system prompt does
# not have to. Both tools hit the live web through DuckDuckGo, which needs no
# API key.


@tool
def search_web(query: str) -> str:
    """Search the web and return the top results for a query.

    Use this to discover what exists on a topic. Returns numbered results,
    each with a title, URL, and short snippet, most relevant first.
    """
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=6))
    if not results:
        return f"No results for '{query}'."
    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"{i}. {r.get('title', 'Untitled')}\n   {r.get('href', '')}\n   {r.get('body', '')}")
    return "\n".join(lines)


@tool
def read_page(url: str) -> str:
    """Fetch a page by URL and return a plain-text excerpt of its content.

    Use this after search_web to read a specific result in more depth before
    relying on it. Returns the start of the page's readable text. Only public
    http(s) URLs are fetched; local, private, and non-web addresses are refused.
    """
    if not _is_safe_public_url(url):
        return f"Refused to fetch {url}: only public http(s) URLs are allowed."

    # Resolve redirects manually so each hop is re-checked against the SSRF
    # policy, and cap the number of hops.
    class _NoAutoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *args, **kwargs):  # noqa: D401, ANN002, ANN003
            return None

    opener = urllib.request.build_opener(_NoAutoRedirect)
    current = url
    try:
        for _ in range(4):
            req = urllib.request.Request(current, headers={"User-Agent": "Mozilla/5.0"})
            try:
                resp = opener.open(req, timeout=15)
            except urllib.error.HTTPError as http_err:
                if http_err.code in (301, 302, 303, 307, 308):
                    location = http_err.headers.get("Location")
                    if not location:
                        return f"Could not fetch {url}: redirect without location."
                    current = urllib.parse.urljoin(current, location)
                    if not _is_safe_public_url(current):
                        return f"Refused to follow redirect to {current}: not a public http(s) URL."
                    continue
                raise
            raw = resp.read(200_000).decode("utf-8", errors="ignore")
            break
        else:
            return f"Could not fetch {url}: too many redirects."
    except Exception as exc:  # noqa: BLE001 - surface fetch failure to the model
        return f"Could not fetch {url}: {exc}"

    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:2000] if text else f"No readable text at {url}."


# --- Structured output ------------------------------------------------------
# Strands validates the model's final answer against this schema, so the
# result is a typed object, not a string you have to parse.


class Finding(BaseModel):
    claim: str = Field(min_length=1, description="A single factual statement supported by a source.")
    source_url: HttpUrl = Field(description="The URL that supports the claim.")


class ResearchBrief(BaseModel):
    topic: str = Field(min_length=1)
    summary: str = Field(min_length=1, description="Two or three sentences answering the request.")
    findings: list[Finding] = Field(min_length=1, description="Individual claims, each with a source.")
    confidence: Literal["high", "medium", "low"] = Field(
        description="Overall confidence in the brief."
    )
    confidence_reason: str = Field(
        min_length=1, description="One line explaining the confidence level."
    )


SYSTEM_PROMPT = (
    "You are a research assistant. Given a topic, produce a brief that a "
    "careful reader can trust: gather material before you conclude, ground "
    "every claim in a source you actually read, prefer recent and primary "
    "sources over secondary ones, and state your confidence honestly. If the "
    "material does not support a claim, leave it out rather than guessing. "
    "Keep the summary tight and specific."
)


def build_agent() -> Agent:
    """Construct the research agent with the OpenAI provider.

    To run on a different provider, replace this model object. The agent,
    tools, and system prompt do not change. For example, Anthropic:
        from strands.models.anthropic import AnthropicModel
        model = AnthropicModel(model_id="claude-...", ...)
    or a local Ollama model, or any OpenAI-compatible endpoint via base_url.
    """
    model = OpenAIModel(
        client_args={"api_key": os.environ["OPENAI_API_KEY"]},
        model_id="gpt-4o-mini",
        params={"temperature": 0.3},
    )
    return Agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=[search_web, read_page],
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Research assistant built with Strands Agents")
    parser.add_argument(
        "--topic",
        default="How AI agents use the Model Context Protocol (MCP)",
        help="The topic to research",
    )
    args = parser.parse_args()

    agent = build_agent()
    result = agent(args.topic, structured_output_model=ResearchBrief)
    brief = result.structured_output

    print(f"\nTopic: {brief.topic}\n")
    print(f"Summary: {brief.summary}\n")
    print("Findings:")
    for f in brief.findings:
        print(f"  - {f.claim}\n    source: {f.source_url}")
    print(f"\nConfidence: {brief.confidence} - {brief.confidence_reason}")


if __name__ == "__main__":
    main()
