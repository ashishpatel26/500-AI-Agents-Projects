"""
Code Review Agent using LangChain.

Reviews Python code for bugs, security issues, style violations, and
suggests improvements. Accepts a file path or inline code snippet.

Usage:
    python agent.py --file path/to/code.py
    python agent.py --code "def add(a,b): return a+b"
"""

import argparse
import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

load_dotenv()

SYSTEM_PROMPT = """You are an expert code reviewer. Analyze the provided code and return a structured review covering:

1. **Bugs & Correctness** — logic errors, edge cases, exception handling
2. **Security Issues** — injection risks, secrets exposure, unsafe operations
3. **Performance** — inefficiencies, unnecessary computation, memory issues
4. **Code Style** — PEP 8 violations, naming conventions, readability
5. **Improvements** — refactoring suggestions, better patterns

Format: Use markdown. Rate overall quality as: 🟢 Good / 🟡 Needs Work / 🔴 Critical Issues."""


def review_code(code: str, language: str = "python") -> str:
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Review this {language} code:\n\n```{language}\n{code}\n```"),
    ]
    response = llm.invoke(messages)
    return response.content


def main():
    parser = argparse.ArgumentParser(description="Code Review Agent")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", help="Path to file to review")
    group.add_argument("--code", help="Inline code snippet to review")
    parser.add_argument("--language", default="python", help="Programming language (default: python)")
    args = parser.parse_args()

    if args.file:
        with open(args.file) as f:
            code = f.read()
        print(f"\n🔍 Reviewing: {args.file}\n")
    else:
        code = args.code
        print(f"\n🔍 Reviewing inline code snippet\n")

    review = review_code(code, args.language)

    print("=" * 60)
    print("📋 CODE REVIEW")
    print("=" * 60)
    print(review)


if __name__ == "__main__":
    main()
