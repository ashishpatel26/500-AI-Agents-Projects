"""
Email Drafting Agent using CrewAI.

A two-agent crew that drafts professional emails:
- Analyst agent: understands context and tone requirements
- Writer agent: drafts the final email

Usage:
    python agent.py
    python agent.py --context "Follow up on the Q3 proposal sent last week" --tone "professional"
"""

import argparse
import os

from crewai import Agent, Crew, Process, Task
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def build_email_crew(context: str, tone: str, recipient: str) -> str:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

    analyst = Agent(
        role="Email Context Analyst",
        goal="Understand the email context, extract key points, and define the structure",
        backstory="You are an expert business communication analyst who distills complex situations into clear email requirements.",
        llm=llm,
        verbose=False,
    )

    writer = Agent(
        role="Professional Email Writer",
        goal="Draft clear, concise, and effective professional emails",
        backstory="You are a professional copywriter specializing in business emails that get responses.",
        llm=llm,
        verbose=False,
    )

    analyze_task = Task(
        description=f"""Analyze this email requirement:
Context: {context}
Recipient: {recipient}
Desired tone: {tone}

Extract: purpose, key points to cover, call to action, subject line suggestion.""",
        agent=analyst,
        expected_output="Structured email brief: purpose, key points, CTA, and suggested subject line",
    )

    write_task = Task(
        description=f"""Using the analysis, draft a complete professional email.
Tone: {tone}. Recipient: {recipient}.
Include: Subject line, greeting, body paragraphs, closing, signature placeholder.
Keep it concise — under 200 words for the body.""",
        agent=writer,
        expected_output="Complete formatted email ready to send",
        context=[analyze_task],
    )

    crew = Crew(
        agents=[analyst, writer],
        tasks=[analyze_task, write_task],
        process=Process.sequential,
        verbose=False,
    )

    result = crew.kickoff()
    return str(result)


def main():
    parser = argparse.ArgumentParser(description="Email Drafting Agent")
    parser.add_argument("--context", default="Follow up on our product demo from last Tuesday. They seemed interested but haven't responded.", help="Email context/purpose")
    parser.add_argument("--tone", default="professional and friendly", help="Email tone")
    parser.add_argument("--recipient", default="a potential client", help="Who the email is for")
    args = parser.parse_args()

    print(f"\n✉️  Drafting email...\n")
    email = build_email_crew(args.context, args.tone, args.recipient)

    print("=" * 60)
    print("📧 DRAFTED EMAIL")
    print("=" * 60)
    print(email)


if __name__ == "__main__":
    main()
