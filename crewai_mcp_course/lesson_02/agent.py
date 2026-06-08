"""
Lesson 02: Multi-Agent Crew with Tool Use

Demonstrates:
- Multiple specialized agents with different roles
- Custom tools (web search, calculator)
- Sequential and hierarchical processes
- Agent collaboration patterns

Run: python agent.py --topic "quantum computing applications"
"""

import argparse
import os

from crewai import Agent, Crew, Process, Task
from crewai.tools import BaseTool
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import Field

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)


# Custom Tool: Word Counter
class WordCountTool(BaseTool):
    name: str = "word_counter"
    description: str = "Count words in a text string. Input: text string."

    def _run(self, text: str) -> str:
        count = len(text.split())
        return f"Word count: {count}"


# Custom Tool: Text Formatter
class TextFormatterTool(BaseTool):
    name: str = "text_formatter"
    description: str = "Format text as a numbered list. Input: comma-separated items."

    def _run(self, items: str) -> str:
        item_list = [i.strip() for i in items.split(",")]
        return "\n".join(f"{i+1}. {item}" for i, item in enumerate(item_list))


word_counter = WordCountTool()
formatter = TextFormatterTool()

# Agent 1: Researcher
researcher = Agent(
    role="Senior Researcher",
    goal="Research topics thoroughly and provide factual, well-structured information",
    backstory="PhD researcher with expertise in synthesizing complex information from multiple sources.",
    llm=llm,
    tools=[word_counter],
    verbose=True,
)

# Agent 2: Writer
writer = Agent(
    role="Technical Writer",
    goal="Transform research into clear, engaging content for technical audiences",
    backstory="Award-winning technical writer with 10 years experience in AI/ML documentation.",
    llm=llm,
    tools=[formatter],
    verbose=True,
)

# Agent 3: Editor
editor = Agent(
    role="Content Editor",
    goal="Review and polish content for clarity, accuracy, and conciseness",
    backstory="Senior editor who ensures all content meets the highest quality standards.",
    llm=llm,
    verbose=True,
)


def run_crew(topic: str) -> str:
    research_task = Task(
        description=f"""Research the topic: "{topic}"

        Find:
        1. Core definition and key concepts (3 bullet points)
        2. Current applications (3 real examples)
        3. Future potential (2 predictions)
        4. Key challenges or limitations

        Use the word_counter tool to verify your output is under 250 words.""",
        expected_output="Research brief with definitions, applications, and future outlook",
        agent=researcher,
    )

    writing_task = Task(
        description=f"""Transform the research into an engaging technical article about "{topic}".

        Structure:
        - Hook opening (1-2 sentences)
        - What it is (clear definition)
        - Why it matters (use formatter tool for 3 key benefits as numbered list)
        - Real-world impact (2 examples)
        - Call to action closing

        Target: 200-250 words, technical but accessible.""",
        expected_output="Polished technical article ready for publication",
        agent=writer,
        context=[research_task],
    )

    editing_task = Task(
        description="""Review the article for:
        1. Accuracy (check facts align with research)
        2. Clarity (remove jargon, improve flow)
        3. Conciseness (trim wordiness)
        4. Add a compelling title and subtitle

        Return the final polished version.""",
        expected_output="Final edited article with title, subtitle, and polished content",
        agent=editor,
        context=[research_task, writing_task],
    )

    crew = Crew(
        agents=[researcher, writer, editor],
        tasks=[research_task, writing_task, editing_task],
        process=Process.sequential,
        verbose=True,
    )

    return str(crew.kickoff())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Agent Research & Writing Crew")
    parser.add_argument("--topic", default="AI agents in healthcare", help="Research topic")
    args = parser.parse_args()

    print(f"\n🚀 Starting crew for topic: {args.topic}\n")
    result = run_crew(args.topic)

    print("\n" + "=" * 60)
    print("FINAL ARTICLE:")
    print("=" * 60)
    print(result)
