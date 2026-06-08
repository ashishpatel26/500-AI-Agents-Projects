"""
Lesson 03: CrewAI + FastMCP Integration

Demonstrates:
- Building a FastMCP server that exposes tools
- Mirroring MCP server tools as CrewAI BaseTool wrappers
- Production pattern: keep tool contracts stable between MCP server and CrewAI wrappers

Architecture:
    MCP Server tool contracts → CrewAI tool wrappers → Output

Run the agent: python agent.py
Optional: run python mcp_server.py to inspect the matching FastMCP server tools.
"""

import asyncio
import json
import os
from datetime import datetime

from crewai import Agent, Crew, Process, Task
from crewai.tools import BaseTool
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import Field

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)


# CrewAI tool wrappers that mirror the FastMCP server's tool contracts.
# In production, replace these wrappers with a real MCP client adapter.
class DateTimeTool(BaseTool):
    name: str = "get_datetime"
    description: str = "Get the current date and time"

    def _run(self, query: str = "") -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")


class JsonFormatterTool(BaseTool):
    name: str = "format_as_json"
    description: str = "Format data as structured JSON. Input: a description of the data to format."

    def _run(self, data_description: str) -> str:
        return json.dumps({
            "formatted": True,
            "timestamp": datetime.now().isoformat(),
            "data": data_description,
        }, indent=2)


class TaskPrioritizerTool(BaseTool):
    name: str = "prioritize_tasks"
    description: str = "Prioritize a list of tasks by importance. Input: comma-separated task list."

    def _run(self, tasks_csv: str) -> str:
        tasks = [t.strip() for t in tasks_csv.split(",")]
        prioritized = [{"rank": i + 1, "task": task, "priority": ["HIGH", "MEDIUM", "LOW"][i % 3]}
                      for i, task in enumerate(tasks)]
        return json.dumps(prioritized, indent=2)


# MCP-connected agent
mcp_agent = Agent(
    role="MCP-Powered Workflow Orchestrator",
    goal="Use MCP tools to orchestrate complex workflows and produce structured outputs",
    backstory="""You are an advanced AI agent with access to MCP (Model Context Protocol) tools.
    You excel at using these tools to gather data, format outputs, and prioritize work.
    You always produce structured, actionable results.""",
    llm=llm,
    tools=[DateTimeTool(), JsonFormatterTool(), TaskPrioritizerTool()],
    verbose=True,
)

# Coordinator agent
coordinator = Agent(
    role="Project Coordinator",
    goal="Coordinate tasks and produce a final project status report",
    backstory="Experienced project manager who synthesizes information into clear status reports.",
    llm=llm,
    verbose=True,
)


def run_mcp_workflow(project_name: str, tasks: list[str]) -> str:
    tasks_str = ", ".join(tasks)

    gather_task = Task(
        description=f"""For project "{project_name}", use your MCP tools to:
        1. Get the current datetime using get_datetime tool
        2. Prioritize these tasks using prioritize_tasks tool: {tasks_str}
        3. Format the results as JSON using format_as_json tool

        Return all gathered information.""",
        expected_output="Current time, prioritized task list, and formatted data",
        agent=mcp_agent,
    )

    report_task = Task(
        description=f"""Create a project status report for "{project_name}" using the gathered data.

        Report format:
        - Project: {project_name}
        - Generated: [timestamp from data]
        - Status: Active
        - Task Priority Matrix: [use the prioritized tasks]
        - Next Action: [highest priority incomplete task]
        - Executive Summary: 2-3 sentences

        Make it professional and actionable.""",
        expected_output="Professional project status report",
        agent=coordinator,
        context=[gather_task],
    )

    crew = Crew(
        agents=[mcp_agent, coordinator],
        tasks=[gather_task, report_task],
        process=Process.sequential,
        verbose=True,
    )

    return str(crew.kickoff())


if __name__ == "__main__":
    project = "AI Agent Platform v2.0"
    tasks = [
        "Implement RAG pipeline",
        "Write unit tests",
        "Deploy to staging",
        "Update documentation",
        "Security audit",
        "Performance benchmarking",
    ]

    print(f"\n🔗 Running MCP-powered CrewAI workflow for: {project}\n")
    result = run_mcp_workflow(project, tasks)

    print("\n" + "=" * 60)
    print("PROJECT STATUS REPORT:")
    print("=" * 60)
    print(result)
