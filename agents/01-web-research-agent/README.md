# Web Research Agent

A LangGraph agent that searches the web for any topic and synthesizes a structured research report.

**Framework**: LangGraph  
**LLM**: GPT-4o-mini (OpenAI)  
**Search**: Tavily

## What it does

1. Takes a research query
2. Searches the web using Tavily (5 results)
3. Synthesizes findings into a structured report (Summary, Key Findings, Sources)

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your API keys
```

Get free API keys:
- OpenAI: https://platform.openai.com/api-keys
- Tavily: https://app.tavily.com (free tier available)

## Run

```bash
# Default query
python agent.py

# Custom query
python agent.py --query "latest advances in quantum computing"
```

## Sample Output

```
🔍 Researching: latest advances in AI agents 2024

============================================================
📄 RESEARCH REPORT
============================================================
## Summary
AI agents have seen significant advances in 2024, with major improvements
in reasoning, tool use, and multi-agent collaboration...

## Key Findings
- LangGraph and CrewAI have emerged as leading frameworks for production agents
- OpenAI's GPT-4o enables real-time multimodal agent interactions
- ...

## Sources
- https://...
```

## Architecture

```
User Query → [Search Node] → Tavily Web Search → [Synthesize Node] → GPT-4o → Report
```
