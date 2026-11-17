#!/usr/bin/env python3
"""Validate the structure and metadata of runnable agent projects."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml

REQUIRED_METADATA = {
    "title",
    "description",
    "author",
    "language",
    "framework",
    "tags",
    "industry",
    "difficulty",
    "llm",
    "entrypoint",
    "requirements",
}
REQUIRED_STATIC_FILES = {"README.md", ".env.example", "metadata.yaml"}
ALLOWED_FRAMEWORKS = {
    "agno",
    "autogen",
    "crewai",
    "langchain",
    "langgraph",
    "llamaindex",
    "other",
}
ALLOWED_DIFFICULTIES = {"beginner", "intermediate", "advanced"}
AGENT_DIRECTORY = re.compile(r"^(?P<number>\d{2,})-[a-z0-9]+(?:-[a-z0-9]+)*$")


def load_metadata(path: Path) -> dict[str, Any]:
    """Load one metadata file and require a mapping at its root."""
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise ValueError(f"cannot read valid YAML: {error}") from error

    if not isinstance(data, dict):
        raise ValueError("metadata must be a YAML mapping")
    return data


def resolve_declared_file(
    agent_dir: Path, value: Any, field: str
) -> tuple[Path | None, str | None]:
    """Resolve a metadata path while preventing absolute or parent traversal."""
    if not isinstance(value, str) or not value.strip():
        return None, f"metadata.{field} must be a non-empty relative path"

    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        return None, f"metadata.{field} must stay inside the agent directory"

    declared = (agent_dir / relative).resolve()
    if not declared.is_relative_to(agent_dir.resolve()):
        return None, f"metadata.{field} must stay inside the agent directory"
    if not declared.is_file():
        return None, f"metadata.{field} points to missing file: {value}"
    return declared, None


def validate_agent(agent_dir: Path) -> list[str]:
    """Return validation errors for one agent directory."""
    errors: list[str] = []

    if not AGENT_DIRECTORY.fullmatch(agent_dir.name):
        errors.append("directory name must match NN-lowercase-hyphenated-name")

    for name in sorted(REQUIRED_STATIC_FILES):
        if not (agent_dir / name).is_file():
            errors.append(f"missing required file: {name}")

    metadata_path = agent_dir / "metadata.yaml"
    if not metadata_path.is_file():
        return errors

    try:
        metadata = load_metadata(metadata_path)
    except ValueError as error:
        errors.append(str(error))
        return errors

    missing = sorted(REQUIRED_METADATA - metadata.keys())
    if missing:
        errors.append(f"missing metadata fields: {', '.join(missing)}")

    for field in sorted(REQUIRED_METADATA - {"tags", "entrypoint", "requirements"}):
        if field not in metadata:
            continue
        value = metadata.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"metadata.{field} must be a non-empty string")

    if "tags" in metadata:
        tags = metadata["tags"]
        if (
            not isinstance(tags, list)
            or not tags
            or not all(isinstance(tag, str) and tag.strip() for tag in tags)
        ):
            errors.append("metadata.tags must be a non-empty list of strings")

    framework = metadata.get("framework")
    if isinstance(framework, str) and framework.strip() and framework not in ALLOWED_FRAMEWORKS:
        errors.append("metadata.framework must be one of: " + ", ".join(sorted(ALLOWED_FRAMEWORKS)))

    difficulty = metadata.get("difficulty")
    if (
        isinstance(difficulty, str)
        and difficulty.strip()
        and difficulty not in ALLOWED_DIFFICULTIES
    ):
        errors.append(
            "metadata.difficulty must be one of: " + ", ".join(sorted(ALLOWED_DIFFICULTIES))
        )

    entrypoint, entrypoint_error = resolve_declared_file(
        agent_dir, metadata.get("entrypoint"), "entrypoint"
    )
    if entrypoint_error:
        errors.append(entrypoint_error)
    elif entrypoint and entrypoint.suffix == ".py":
        try:
            source = entrypoint.read_text(encoding="utf-8")
            compile(source, str(entrypoint), "exec")
        except (OSError, UnicodeError, SyntaxError) as error:
            errors.append(f"entrypoint is not valid Python: {error}")

    _, requirements_error = resolve_declared_file(
        agent_dir, metadata.get("requirements"), "requirements"
    )
    if requirements_error:
        errors.append(requirements_error)

    return errors


def _validate_repository_with_count(root: Path) -> tuple[list[str], int]:
    """Validate a repository and return its errors and discovered agent count."""
    agents_dir = root / "agents"
    if not agents_dir.is_dir():
        return ["agents directory does not exist"], 0

    agent_dirs = sorted(path for path in agents_dir.iterdir() if path.is_dir())
    if not agent_dirs:
        return ["agents directory contains no agent projects"], 0

    errors: list[str] = []
    numbers: dict[int, str] = {}
    for agent_dir in agent_dirs:
        match = AGENT_DIRECTORY.fullmatch(agent_dir.name)
        if match:
            number = int(match.group("number"))
            if number in numbers:
                errors.append(
                    f"{agent_dir.name}: numeric prefix {number} is already used by {numbers[number]}"
                )
            else:
                numbers[number] = agent_dir.name
        errors.extend(f"{agent_dir.name}: {error}" for error in validate_agent(agent_dir))
    return errors, len(agent_dirs)


def validate_repository(root: Path) -> list[str]:
    """Return validation errors for all agents in a repository."""
    errors, _ = _validate_repository_with_count(root)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (defaults to the script's parent repository)",
    )
    args = parser.parse_args()

    errors, count = _validate_repository_with_count(args.root.resolve())
    if errors:
        print("Agent catalog validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {count} agent projects.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
