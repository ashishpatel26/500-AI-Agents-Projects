"""
Data Analysis Agent using LangChain + pandas.

Loads a CSV/Excel file and answers analytical questions about it using
natural language. The agent generates Python/pandas code to answer questions.

Usage:
    python agent.py --file data.csv
    python agent.py --file sales.xlsx --question "What is the monthly revenue trend?"
"""

import argparse
import os

import pandas as pd
from dotenv import load_dotenv
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI

load_dotenv()


def create_sample_data(path: str):
    """Creates a sample sales dataset for demo."""
    import random
    from datetime import date, timedelta

    random.seed(42)
    rows = []
    products = ["Laptop", "Phone", "Tablet", "Monitor", "Keyboard"]
    regions = ["North", "South", "East", "West"]
    start = date(2024, 1, 1)

    for i in range(200):
        d = start + timedelta(days=random.randint(0, 364))
        rows.append({
            "date": d.isoformat(),
            "product": random.choice(products),
            "region": random.choice(regions),
            "quantity": random.randint(1, 20),
            "unit_price": round(random.uniform(50, 2000), 2),
            "revenue": 0,
        })

    df = pd.DataFrame(rows)
    df["revenue"] = df["quantity"] * df["unit_price"]
    df.to_csv(path, index=False)
    return df


def main():
    parser = argparse.ArgumentParser(description="Data Analysis Agent")
    parser.add_argument("--file", default="sample_data.csv", help="CSV or Excel file to analyze")
    parser.add_argument("--question", help="Single question (omit for interactive mode)")
    parser.add_argument(
        "--allow-dangerous-code",
        action="store_true",
        help="Required to let the pandas agent execute generated Python code locally",
    )
    args = parser.parse_args()

    if args.file == "sample_data.csv" and not os.path.exists("sample_data.csv"):
        print("🏗️  Creating sample sales dataset...")
        df = create_sample_data("sample_data.csv")
    else:
        ext = os.path.splitext(args.file)[1].lower()
        df = pd.read_excel(args.file) if ext in (".xlsx", ".xls") else pd.read_csv(args.file)

    print(f"\n📊 Loaded: {args.file} ({len(df)} rows × {len(df.columns)} columns)")
    print(f"📋 Columns: {', '.join(df.columns)}\n")

    if not args.allow_dangerous_code:
        print("⚠️  This agent uses LangChain's pandas agent, which executes model-generated Python code.")
        print("Run again with --allow-dangerous-code only with trusted prompts and non-sensitive data.")
        return

    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=False,
        allow_dangerous_code=args.allow_dangerous_code,
    )

    if args.question:
        print(f"❓ Question: {args.question}")
        result = agent.invoke({"input": args.question})
        print(f"\n✅ Answer: {result['output']}")
    else:
        print("💬 Data Analysis Agent ready. Ask questions about your data. Type 'quit' to exit.\n")
        print("Example questions:")
        print("  - What is the total revenue by product?")
        print("  - Which region has the highest average order value?")
        print("  - Show me the top 5 sales days\n")
        while True:
            question = input("You: ").strip()
            if question.lower() in ("quit", "exit", "q"):
                break
            if not question:
                continue
            result = agent.invoke({"input": question})
            print(f"\nAgent: {result['output']}\n")


if __name__ == "__main__":
    main()
