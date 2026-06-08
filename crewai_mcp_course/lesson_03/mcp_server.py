"""
FastMCP Server for Lesson 03.

Exposes tools that CrewAI agents can call via the MCP protocol.
This is the server side — agents connect to this to use the tools.

Run: python mcp_server.py
(Keep this running while agent.py is running)
"""

import json
from datetime import datetime

try:
    from fastmcp import FastMCP
    HAS_FASTMCP = True
except ImportError:
    HAS_FASTMCP = False
    print("FastMCP not installed. Run: pip install fastmcp")
    print("Showing example server code only.\n")


def create_mcp_server():
    if not HAS_FASTMCP:
        return None

    mcp = FastMCP("CrewAI Course Tools")

    @mcp.tool()
    def get_datetime() -> str:
        """Get the current date and time in UTC."""
        return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    @mcp.tool()
    def prioritize_tasks(tasks: list[str]) -> str:
        """
        Prioritize a list of tasks by estimated importance.

        Args:
            tasks: List of task descriptions to prioritize

        Returns:
            JSON string with prioritized tasks
        """
        prioritized = []
        for i, task in enumerate(tasks):
            priority = "HIGH" if i < len(tasks) // 3 else "MEDIUM" if i < 2 * len(tasks) // 3 else "LOW"
            prioritized.append({"rank": i + 1, "task": task, "priority": priority})
        return json.dumps(prioritized, indent=2)

    @mcp.tool()
    def format_as_json(data: dict) -> str:
        """
        Format data as pretty-printed JSON.

        Args:
            data: Dictionary to format

        Returns:
            Pretty-printed JSON string
        """
        return json.dumps(data, indent=2, default=str)

    @mcp.tool()
    def calculate_project_metrics(tasks_completed: int, tasks_total: int) -> dict:
        """
        Calculate project completion metrics.

        Args:
            tasks_completed: Number of completed tasks
            tasks_total: Total number of tasks

        Returns:
            Dictionary with completion percentage and status
        """
        percentage = (tasks_completed / tasks_total * 100) if tasks_total > 0 else 0
        status = "On Track" if percentage >= 50 else "At Risk" if percentage >= 25 else "Behind"
        return {
            "completed": tasks_completed,
            "total": tasks_total,
            "percentage": round(percentage, 1),
            "status": status,
        }

    return mcp


if __name__ == "__main__":
    mcp = create_mcp_server()
    if mcp:
        print("🚀 MCP Server starting on localhost:8000")
        print("Tools available: get_datetime, prioritize_tasks, format_as_json, calculate_project_metrics")
        mcp.run(transport="streamable-http", host="localhost", port=8000)
    else:
        print("Install fastmcp to run the server: pip install fastmcp")
