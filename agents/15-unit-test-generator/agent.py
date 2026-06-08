"""
Unit Test Generator Agent.

Analyzes Python code and generates comprehensive pytest test suites
covering happy paths, edge cases, and error conditions.

Usage:
    python agent.py --file path/to/module.py
    python agent.py --code "def calculate_bmi(weight, height): return weight / height**2"
"""

import argparse
import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

load_dotenv()

TEST_PROMPT = """You are an expert Python test engineer. Generate a comprehensive pytest test suite for the provided code.

Requirements:
1. Use pytest fixtures where appropriate
2. Test happy paths (normal expected inputs)
3. Test edge cases (boundary values, empty inputs)
4. Test error conditions (invalid inputs, exceptions)
5. Use descriptive test names: `test_function_name_scenario`
6. Add brief docstrings to each test
7. Use `pytest.mark.parametrize` for repetitive tests
8. Mock external dependencies (API calls, file I/O, DB)
9. Aim for 90%+ code coverage

Output ONLY the complete test file content, ready to run with `pytest`."""

SAMPLE_CODE = '''
def calculate_discount(price: float, discount_percent: float) -> float:
    """Calculate discounted price."""
    if price < 0:
        raise ValueError("Price cannot be negative")
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")
    return price * (1 - discount_percent / 100)


def find_longest_word(text: str) -> str:
    """Find the longest word in a text string."""
    if not text or not text.strip():
        return ""
    words = text.split()
    return max(words, key=len)


class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, name: str, price: float, quantity: int = 1):
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1")
        if name in self.items:
            self.items[name]["quantity"] += quantity
        else:
            self.items[name] = {"price": price, "quantity": quantity}

    def remove_item(self, name: str):
        if name not in self.items:
            raise KeyError(f"Item '{name}' not in cart")
        del self.items[name]

    def total(self) -> float:
        return sum(item["price"] * item["quantity"] for item in self.items.values())
'''


def generate_tests(code: str, filename: str = "module") -> str:
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    messages = [
        SystemMessage(content=TEST_PROMPT),
        HumanMessage(content=f"Generate tests for this Python code (from `{filename}`):\n\n```python\n{code}\n```"),
    ]
    response = llm.invoke(messages)
    return response.content


def main():
    parser = argparse.ArgumentParser(description="Unit Test Generator")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--file", help="Python file to generate tests for")
    group.add_argument("--code", help="Inline code to generate tests for")
    parser.add_argument("--output", help="Output file path (default: test_<name>.py)")
    args = parser.parse_args()

    if args.file:
        with open(args.file) as f:
            code = f.read()
        module_name = os.path.splitext(os.path.basename(args.file))[0]
        print(f"\n🧪 Generating tests for: {args.file}")
    elif args.code:
        code = args.code
        module_name = "module"
        print(f"\n🧪 Generating tests for inline code")
    else:
        code = SAMPLE_CODE
        module_name = "shopping"
        print(f"\n🧪 Generating tests for sample code")

    tests = generate_tests(code, module_name)

    # Clean up markdown fences if present
    if tests.startswith("```"):
        lines = tests.split("\n")
        tests = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])

    output_file = args.output or f"test_{module_name}.py"
    with open(output_file, "w") as f:
        f.write(tests)

    print(f"\n✅ Tests saved to: {output_file}")
    print(f"\nRun with: pytest {output_file} -v")
    print("\n" + "=" * 60)
    print(tests[:500] + "..." if len(tests) > 500 else tests)


if __name__ == "__main__":
    main()
