# CrewAI with FastMCP Server Integration Course

This course teaches beginners how to use CrewAI with FastMCP server access through step-by-step programming examples.

## Course Overview

This course is designed for beginner developers with basic Python knowledge who want to learn how to integrate CrewAI agents with FastMCP servers. The course covers fundamental concepts, practical implementation, and advanced patterns for building intelligent agent workflows.

## Lessons

### Lesson 1: Setting up CrewAI with MCP Server Access
- Install required packages
- Set up environment variables
- Create a basic CrewAI agent
- Execute simple tasks

```mermaid
graph TD
    A[Install Packages] --> B[Set Environment Variables]
    B --> C[Create CrewAI Agent]
    C --> D[Execute Task]
```

### Lesson 2: Integrating MCP Server with CrewAI
- Create custom tools for MCP server access
- Configure authentication and connection settings
- Use MCP server data in agent tasks
- Handle errors and exceptions

```mermaid
graph TD
    A[Create FastMCP Tool] --> B[Configure Authentication]
    B --> C[Create Agent with Tool]
    C --> D[Execute Task with MCP Data]
    D --> E[Handle Response]
```

### Lesson 3: Advanced CrewAI Patterns with MCP Server
- Implement multi-agent workflows
- Use hierarchical processes
- Share data between agents through the MCP server
- Store and retrieve research findings
- Implement quality assurance processes

```mermaid
graph TD
    A[Researcher Agent] -->|Query| B(FastMCP Server)
    B -->|Return Data| A
    A -->|Share Findings| C[Writer Agent]
    C -->|Create Report| D[Reviewer Agent]
    D -->|Provide Feedback| C
    C -->|Final Report| E[Output]
```

## Getting Started

### Using pip (traditional method)

1. Install the required packages for the lesson you want to run:
```bash
pip install -r lesson_01/requirements.txt
pip install -r lesson_02/requirements.txt
pip install -r lesson_03/requirements.txt
```

2. Set up your environment variables:
```bash
export OPENAI_API_KEY=your-openai-api-key
export MCP_SERVER_URL=http://localhost:8000
```

3. Run the examples:
```bash
python lesson_01/agent.py
python lesson_02/agent.py --topic "AI agents in healthcare"

# Lesson 03 includes a matching FastMCP server and CrewAI wrappers.
python lesson_03/agent.py
# Optional: inspect/run the FastMCP server separately:
python lesson_03/mcp_server.py
```

### Using uv (recommended modern method)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver. To use uv:

1. Install uv:
```bash
pip install uv
```

2. Create and activate a virtual environment:
```bash
uv venv
source .venv/Scripts/activate
```

3. Install dependencies:
```bash
uv pip install -r lesson_01/requirements.txt
uv pip install -r lesson_02/requirements.txt
uv pip install -r lesson_03/requirements.txt
```

4. Set up your environment variables:
```bash
export OPENAI_API_KEY=your-openai-api-key
export MCP_SERVER_URL=http://localhost:8000
```

5. Run the examples:
```bash
python lesson_01/agent.py
python lesson_02/agent.py --topic "AI agents in healthcare"

python lesson_03/agent.py
# Optional: inspect/run the FastMCP server separately:
python lesson_03/mcp_server.py
```

## Requirements

- Python 3.8+
- CrewAI library
- FastMCP library
- OpenAI API key
- FastMCP server example for Lesson 03

## Course Structure

Each lesson includes:
- A lesson folder with `agent.py`, `requirements.txt`, and `.env.example`
- Clear objectives and expected outcomes
- Step-by-step implementation
- Best practices for error handling and security

## Next Steps

After completing this course, you should be able to:
- Create and configure CrewAI agents
- Integrate MCP servers with agent workflows
- Build complex multi-agent systems
- Implement data sharing between agents
- Design robust error handling for production systems
