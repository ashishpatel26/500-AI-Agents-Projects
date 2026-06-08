"""
Documentation Writer Agent.

Generates comprehensive documentation for Python modules:
README, API reference, docstrings, and usage examples.

Usage:
    python agent.py --file path/to/module.py
    python agent.py --file src/utils.py --format readme
"""

import argparse
import ast
import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

load_dotenv()


def extract_structure(code: str) -> str:
    """Extract functions, classes, and their signatures from Python code."""
    try:
        tree = ast.parse(code)
        structure = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                args = [a.arg for a in node.args.args]
                structure.append(f"def {node.name}({', '.join(args)})")
            elif isinstance(node, ast.ClassDef):
                structure.append(f"class {node.name}:")
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        args = [a.arg for a in item.args.args]
                        structure.append(f"  def {item.name}({', '.join(args)})")

        return "\n".join(structure)
    except Exception:
        return "Could not parse structure"


README_PROMPT = """You are a technical documentation expert. Generate a complete, professional README.md for this Python module.

Include:
1. Module title and one-line description
2. Features list (bullet points)
3. Installation section
4. Quick Start with working code example
5. API Reference (each public function/class with parameters, return type, example)
6. Configuration (environment variables if any)
7. Error Handling section

Write in clear, developer-friendly markdown. Be specific and concrete."""

DOCSTRING_PROMPT = """Add comprehensive Google-style docstrings to every function and class that lacks them.

Format:
```
def function(param: type) -> return_type:
    \"\"\"One-line summary.

    Args:
        param: Description of parameter.

    Returns:
        Description of return value.

    Raises:
        ErrorType: When this error is raised.

    Example:
        >>> function(value)
        expected_output
    \"\"\"
```

Return the complete updated Python file with docstrings added."""


def generate_readme(code: str, filename: str) -> str:
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    structure = extract_structure(code)
    messages = [
        SystemMessage(content=README_PROMPT),
        HumanMessage(content=f"File: {filename}\n\nCode structure:\n{structure}\n\nFull code:\n```python\n{code[:3000]}\n```"),
    ]
    return llm.invoke(messages).content


def add_docstrings(code: str, filename: str) -> str:
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    messages = [
        SystemMessage(content=DOCSTRING_PROMPT),
        HumanMessage(content=f"Add docstrings to this Python file ({filename}):\n\n```python\n{code}\n```"),
    ]
    result = llm.invoke(messages).content
    # Clean markdown fences
    if "```python" in result:
        result = result.split("```python")[1].split("```")[0].strip()
    return result


SAMPLE_CODE = r'''
import hashlib
import re
from datetime import datetime


def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def hash_password(password: str, salt: str = "") -> str:
    combined = f"{password}{salt}"
    return hashlib.sha256(combined.encode()).hexdigest()


def parse_date(date_string: str) -> datetime:
    formats = ["%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y", "%Y%m%d"]
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unable to parse date: {date_string}")


class UserValidator:
    MIN_PASSWORD_LENGTH = 8

    def validate_username(self, username: str) -> tuple[bool, str]:
        if len(username) < 3:
            return False, "Username too short"
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Only letters, numbers, underscores allowed"
        return True, ""

    def validate_password(self, password: str) -> tuple[bool, str]:
        if len(password) < self.MIN_PASSWORD_LENGTH:
            return False, f"Password must be at least {self.MIN_PASSWORD_LENGTH} characters"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r'\d', password):
            return False, "Password must contain at least one digit"
        return True, ""
'''


def main():
    parser = argparse.ArgumentParser(description="Documentation Writer Agent")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--file", help="Python file to document")
    group.add_argument("--code", help="Inline code to document")
    parser.add_argument("--format", choices=["readme", "docstrings", "both"], default="both", help="Documentation format to generate")
    args = parser.parse_args()

    if args.file:
        with open(args.file) as f:
            code = f.read()
        filename = os.path.basename(args.file)
    elif args.code:
        code = args.code
        filename = "module.py"
    else:
        code = SAMPLE_CODE
        filename = "validators.py"
        print("\n📝 Using sample validators module")

    print(f"\n✍️  Generating documentation for: {filename}\n")

    if args.format in ("readme", "both"):
        print("📄 Generating README...")
        readme = generate_readme(code, filename)
        readme_file = f"README_{filename.replace('.py', '')}.md"
        with open(readme_file, "w") as f:
            f.write(readme)
        print(f"✅ README saved to: {readme_file}")

    if args.format in ("docstrings", "both"):
        print("📝 Adding docstrings...")
        documented_code = add_docstrings(code, filename)
        output_file = f"documented_{filename}"
        with open(output_file, "w") as f:
            f.write(documented_code)
        print(f"✅ Documented code saved to: {output_file}")


if __name__ == "__main__":
    main()
