"""
PDF Q&A Agent using LlamaIndex.

Loads a PDF, indexes it, and answers questions about its content.
Maintains conversation history for follow-up questions.

Usage:
    python agent.py --pdf path/to/document.pdf
    python agent.py --pdf report.pdf --question "What is the main finding?"
"""

import argparse
import os

from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.llms.openai import OpenAI

load_dotenv()


def build_index(pdf_path: str) -> VectorStoreIndex:
    print(f"📄 Loading and indexing {pdf_path}...")
    reader = SimpleDirectoryReader(input_files=[pdf_path])
    docs = reader.load_data()
    index = VectorStoreIndex.from_documents(docs)
    print(f"✅ Indexed {len(docs)} document chunk(s)")
    return index


def interactive_qa(index: VectorStoreIndex):
    llm = OpenAI(model="gpt-4o-mini", temperature=0)
    memory = ChatMemoryBuffer.from_defaults(token_limit=4096)
    chat_engine = index.as_chat_engine(
        chat_mode="context",
        llm=llm,
        memory=memory,
        verbose=False,
    )

    print("\n💬 PDF Q&A Agent ready. Type 'quit' to exit.\n")
    while True:
        question = input("You: ").strip()
        if question.lower() in ("quit", "exit", "q"):
            break
        if not question:
            continue
        response = chat_engine.chat(question)
        print(f"\nAgent: {response.response}\n")


def single_question(index: VectorStoreIndex, question: str):
    query_engine = index.as_query_engine(similarity_top_k=5)
    response = query_engine.query(question)
    print("\n" + "=" * 60)
    print("📋 ANSWER")
    print("=" * 60)
    print(response.response)
    if hasattr(response, "source_nodes"):
        print(f"\n📚 Sources: {len(response.source_nodes)} chunk(s) referenced")


def main():
    parser = argparse.ArgumentParser(description="PDF Q&A Agent")
    parser.add_argument("--pdf", required=True, help="Path to PDF file")
    parser.add_argument("--question", help="Single question (omit for interactive mode)")
    args = parser.parse_args()

    index = build_index(args.pdf)

    if args.question:
        single_question(index, args.question)
    else:
        interactive_qa(index)


if __name__ == "__main__":
    main()
