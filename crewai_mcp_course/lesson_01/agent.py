"""
Lesson 01: Your First CrewAI Agent

Demonstrates the fundamentals of CrewAI:
- Creating agents with roles, goals, and backstories
- Defining tasks
- Running a simple crew

Run: python agent.py
"""

from crewai import Agent, Crew, Process, Task
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# 1. Define the agent
researcher = Agent(
    role="AI Researcher",
    goal="Research and summarize the latest developments in AI agents",
    backstory="""You are a seasoned AI researcher who stays up-to-date with
    the latest papers, frameworks, and applications in the AI agent space.
    You write clear, accurate summaries for technical audiences.""",
    llm=llm,
    verbose=True,
)

# 2. Define the task
research_task = Task(
    description="""Research and write a concise briefing on:
    "The current state of AI agents in 2025"

    Cover:
    - What are AI agents and why they matter
    - Top 3 frameworks (CrewAI, LangGraph, AutoGen)
    - 2 real-world use cases making impact
    - What's coming next

    Keep it under 300 words, technical audience.""",
    expected_output="A concise technical briefing on AI agents in 2025",
    agent=researcher,
)

# 3. Create and run the crew
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\n" + "=" * 60)
    print("FINAL RESULT:")
    print("=" * 60)
    print(result)
