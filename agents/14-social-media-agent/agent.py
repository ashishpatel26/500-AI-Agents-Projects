"""
Social Media Content Agent using CrewAI.

Generates platform-optimized content (Twitter/X, LinkedIn, Instagram)
from a topic or article URL.

Usage:
    python agent.py --topic "The rise of AI agents in 2025"
    python agent.py --topic "New product launch: CloudSync Pro v3" --brand "CloudSync"
"""

import argparse
import os

from crewai import Agent, Crew, Process, Task
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def generate_social_content(topic: str, brand: str, platforms: list[str]) -> str:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    strategist = Agent(
        role="Social Media Strategist",
        goal="Analyze the topic and define the key message, target audience, and tone for each platform",
        backstory="Award-winning social media strategist who has grown 50+ brand accounts to 100k+ followers.",
        llm=llm,
        verbose=False,
    )

    writer = Agent(
        role="Social Media Copywriter",
        goal="Write engaging, platform-optimized content that drives engagement",
        backstory="Viral content creator with expertise in platform-specific formats, hashtags, and hooks.",
        llm=llm,
        verbose=False,
    )

    strategy_task = Task(
        description=f"""Analyze this topic for social media: "{topic}"
Brand: {brand or 'Not specified'}
Platforms: {', '.join(platforms)}
Define: core message, target audience, emotional hook, 5 relevant hashtags.""",
        agent=strategist,
        expected_output="Content strategy: message, audience, hook, and hashtags",
    )

    writing_task = Task(
        description=f"""Write social media posts for: {', '.join(platforms)}
Topic: {topic}. Brand: {brand or 'General'}.

For each platform:
- Twitter/X: 2 tweet variations (under 280 chars each) + thread opener
- LinkedIn: Professional post (150-200 words) with storytelling hook
- Instagram: Caption (100-150 words) + 15 hashtags

Make them platform-native — Twitter punchy, LinkedIn thoughtful, Instagram visual.""",
        agent=writer,
        expected_output="Platform-optimized posts for all requested platforms",
        context=[strategy_task],
    )

    crew = Crew(
        agents=[strategist, writer],
        tasks=[strategy_task, writing_task],
        process=Process.sequential,
        verbose=False,
    )

    return str(crew.kickoff())


def main():
    parser = argparse.ArgumentParser(description="Social Media Content Agent")
    parser.add_argument("--topic", default="How AI is transforming software development in 2025", help="Content topic")
    parser.add_argument("--brand", default="", help="Brand name (optional)")
    parser.add_argument("--platforms", default="twitter,linkedin,instagram", help="Comma-separated platforms")
    args = parser.parse_args()

    platforms = [p.strip() for p in args.platforms.split(",")]
    print(f"\n📱 Generating content for: {', '.join(platforms)}")
    print(f"📌 Topic: {args.topic}\n")

    content = generate_social_content(args.topic, args.brand, platforms)

    print("=" * 60)
    print("✍️  SOCIAL MEDIA CONTENT")
    print("=" * 60)
    print(content)


if __name__ == "__main__":
    main()
