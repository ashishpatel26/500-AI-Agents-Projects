"""
News Summarizer Agent using AutoGen.

Fetches news articles and produces structured summaries with key insights.

Usage:
    python agent.py --topic "artificial intelligence"
    python agent.py --topic "climate change" --count 5
"""

import argparse
import os

import requests
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def fetch_news(topic: str, count: int = 5) -> list[dict]:
    if not NEWS_API_KEY:
        # Return mock data if no API key
        return [
            {"title": f"Major development in {topic}", "description": f"Researchers announce breakthrough in {topic} field.", "url": "https://example.com/1", "source": {"name": "Tech News"}},
            {"title": f"{topic.title()} industry sees rapid growth", "description": f"New report shows {topic} adoption up 40% year-over-year.", "url": "https://example.com/2", "source": {"name": "Business Daily"}},
            {"title": f"Experts weigh in on {topic} challenges", "description": f"Leading experts discuss obstacles facing the {topic} space.", "url": "https://example.com/3", "source": {"name": "Science Weekly"}},
        ]

    url = f"https://newsapi.org/v2/everything?q={topic}&language=en&pageSize={count}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    response = requests.get(url, timeout=10)
    data = response.json()
    return data.get("articles", [])


def summarize_news(topic: str, articles: list[dict]) -> str:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    articles_text = "\n\n".join(
        f"Title: {a['title']}\nSource: {a.get('source', {}).get('name', 'Unknown')}\nSummary: {a.get('description', 'N/A')}"
        for a in articles[:5]
    )

    messages = [
        SystemMessage(content="You are a news analyst. Create a structured news briefing with: 1) Top Story, 2) Key Themes (3 bullet points), 3) What to Watch, 4) Quick Headlines list."),
        HumanMessage(content=f"Topic: {topic}\n\nArticles:\n{articles_text}"),
    ]

    response = llm.invoke(messages)
    return response.content


def main():
    parser = argparse.ArgumentParser(description="News Summarizer Agent")
    parser.add_argument("--topic", default="artificial intelligence", help="News topic to search")
    parser.add_argument("--count", type=int, default=5, help="Number of articles to fetch")
    args = parser.parse_args()

    print(f"\n📰 Fetching news about: {args.topic}\n")
    articles = fetch_news(args.topic, args.count)
    print(f"✅ Found {len(articles)} articles")

    summary = summarize_news(args.topic, articles)

    print("\n" + "=" * 60)
    print(f"📋 NEWS BRIEFING: {args.topic.upper()}")
    print("=" * 60)
    print(summary)


if __name__ == "__main__":
    main()
