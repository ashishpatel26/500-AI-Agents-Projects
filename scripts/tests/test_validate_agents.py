from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.validate_agents import ALLOWED_DIFFICULTIES, ALLOWED_FRAMEWORKS, validate_repository

VALID_METADATA = """\
title: example-agent
description: A small validation fixture
author: contributor
language: python
framework: langgraph
tags: [testing, example]
industry: general
difficulty: beginner
llm: none
entrypoint: agent.py
requirements: requirements.txt
"""


class ValidateAgentsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        (self.root / "agents").mkdir()

    def create_agent(self, name: str = "01-example-agent", metadata: str = VALID_METADATA) -> Path:
        agent = self.root / "agents" / name
        agent.mkdir()
        (agent / "README.md").write_text("# Example Agent\n", encoding="utf-8")
        (agent / ".env.example").write_text("API_KEY=your-key-here\n", encoding="utf-8")
        (agent / "metadata.yaml").write_text(metadata, encoding="utf-8")
        (agent / "agent.py").write_text("print('hello')\n", encoding="utf-8")
        (agent / "requirements.txt").write_text("PyYAML==6.0.2\n", encoding="utf-8")
        return agent

    def test_valid_agent_passes(self) -> None:
        self.create_agent()

        self.assertEqual(validate_repository(self.root), [])

    def test_missing_metadata_field_is_reported_once(self) -> None:
        self.create_agent(metadata=VALID_METADATA.replace("author: contributor\n", ""))

        errors = validate_repository(self.root)

        self.assertEqual(sum("author" in error for error in errors), 1)

    def test_empty_enum_field_is_reported_once(self) -> None:
        fields = (("framework", "langgraph"), ("difficulty", "beginner"))
        for index, (field, valid_value) in enumerate(fields, start=1):
            with self.subTest(field=field):
                metadata = VALID_METADATA.replace(f"{field}: {valid_value}", f"{field}: '   '")
                self.create_agent(name=f"{index:02d}-{field}-agent", metadata=metadata)

                errors = validate_repository(self.root)

                self.assertEqual(sum(f"metadata.{field}" in error for error in errors), 1)

    def test_invalid_framework_and_difficulty_are_rejected(self) -> None:
        metadata = VALID_METADATA.replace("framework: langgraph", "framework: unsupported").replace(
            "difficulty: beginner", "difficulty: expert"
        )
        self.create_agent(metadata=metadata)

        errors = validate_repository(self.root)

        self.assertTrue(any("metadata.framework must be one of" in error for error in errors))
        self.assertTrue(any("metadata.difficulty must be one of" in error for error in errors))

    def test_documented_enum_values_match_validator(self) -> None:
        contribution = (Path(__file__).resolve().parents[2] / "CONTRIBUTION.md").read_text(
            encoding="utf-8"
        )
        lines = contribution.splitlines()

        framework_line = next(line for line in lines if line.startswith("framework: langgraph"))
        documented_frameworks = {
            item.strip() for item in framework_line.split("#", 1)[1].split("|")
        }
        difficulty_line = next(
            line for line in lines if line.startswith("difficulty: intermediate")
        )
        documented_difficulties = {
            item.strip() for item in difficulty_line.split("#", 1)[1].split("|")
        }

        self.assertEqual(documented_frameworks, ALLOWED_FRAMEWORKS)
        self.assertEqual(documented_difficulties, ALLOWED_DIFFICULTIES)

    def test_declared_file_cannot_escape_agent_directory(self) -> None:
        metadata = VALID_METADATA.replace("entrypoint: agent.py", "entrypoint: ../outside.py")
        self.create_agent(metadata=metadata)
        (self.root / "agents" / "outside.py").write_text("", encoding="utf-8")

        errors = validate_repository(self.root)

        self.assertTrue(any("must stay inside" in error for error in errors))

    def test_invalid_python_entrypoint_is_rejected(self) -> None:
        agent = self.create_agent()
        (agent / "agent.py").write_text("if\n", encoding="utf-8")

        errors = validate_repository(self.root)

        self.assertTrue(any("entrypoint is not valid Python" in error for error in errors))

    def test_requirements_cannot_escape_agent_directory(self) -> None:
        metadata = VALID_METADATA.replace(
            "requirements: requirements.txt", "requirements: ../requirements.txt"
        )
        self.create_agent(metadata=metadata)

        errors = validate_repository(self.root)

        self.assertTrue(any("metadata.requirements must stay inside" in error for error in errors))

    def test_missing_requirements_file_is_rejected(self) -> None:
        metadata = VALID_METADATA.replace(
            "requirements: requirements.txt", "requirements: missing-requirements.txt"
        )
        self.create_agent(metadata=metadata)

        errors = validate_repository(self.root)

        self.assertTrue(
            any("metadata.requirements points to missing file" in error for error in errors)
        )

    def test_numeric_prefixes_must_be_unique(self) -> None:
        self.create_agent("01-first-agent")
        self.create_agent("001-second-agent")

        errors = validate_repository(self.root)

        self.assertTrue(any("numeric prefix 1 is already used" in error for error in errors))

    def test_missing_agents_directory_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            errors = validate_repository(Path(directory))

        self.assertEqual(errors, ["agents directory does not exist"])

    def test_empty_agents_directory_is_rejected(self) -> None:
        self.assertEqual(
            validate_repository(self.root), ["agents directory contains no agent projects"]
        )


if __name__ == "__main__":
    unittest.main()
