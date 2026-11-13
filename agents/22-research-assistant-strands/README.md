# Research Assistant (Strands Agents)

A [Strands Agents](https://github.com/strands-agents/harness-sdk) agent that
researches a topic on the live web and returns a structured, source-grounded
brief.

**Framework**: Strands Agents
**LLM**: GPT-4o-mini (OpenAI)
**Search**: DuckDuckGo (no API key)

## What it does

1. Takes a topic
2. Searches the web and reads the pages it finds
3. Returns a typed brief: summary, findings with a source URL each, and a
   stated confidence level

The model runs the agent loop. It decides which tool to call, in what order,
and when it has read enough to answer. You do not write that control flow. The
two tools describe themselves in their docstrings, so the system prompt only
sets the agent's role and standards, not a tool-by-tool script. The final
answer is validated against a Pydantic schema, so you get a typed object
rather than a string to parse.

Strands is provider-agnostic. This runs on OpenAI `gpt-4o-mini` by default;
pointing the same agent at Anthropic, Gemini, Ollama, or any OpenAI-compatible
endpoint is a change to one model object in `build_agent()`, not to the agent.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # add your OpenAI API key
```

Get an API key at https://platform.openai.com/api-keys. DuckDuckGo search
needs no key.

## Run

```bash
# Default topic
python agent.py

# Custom topic
python agent.py --topic "how retrieval-augmented generation works"
```

Runtime: about 25 seconds and a few cents on `gpt-4o-mini`.

## Sample Output

Real output of `python agent.py` (default topic):

```
Topic: AI agents use of the Model Context Protocol (MCP)

Summary: The Model Context Protocol (MCP) is an open-source standard designed
to facilitate communication between AI agents and external systems, such as
databases, tools, and workflows. It allows AI applications to access and
utilize various resources effectively, enhancing their functionality and
enabling more complex interactions.

Findings:
  - The MCP system consists of three main components: the MCP host (where the
    agent runs), the MCP client (the interface for the agent), and the MCP
    server (which provides access to external tools and data).
    source: https://www.aihandbook.io/agentic-ai-handbook/mcp/
  - MCP defines a clear protocol for how tools expose their capabilities, how
    agents request actions or data, and how context is shared, allowing agents
    to interact with tools without needing to understand their internal
    workings.
    source: https://www.aihandbook.io/agentic-ai-handbook/mcp/
  - MCP is supported by various AI applications, including Claude and ChatGPT,
    and acts like a USB-C port for AI applications, providing a universal
    connection standard.
    source: https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro

Confidence: high - The information is derived from multiple reputable sources,
including the official MCP documentation and a detailed analysis of its
architecture and applications.
```

The run made several tool calls: the model searched, read the pages it found,
then produced the typed brief. URLs and figures come from the pages the agent
actually read. `read_page` only fetches public http(s) URLs; local, private,
and non-web addresses are refused, so a malicious search result cannot make the
agent read local files or cloud metadata.

## Architecture

```
Topic -> [agent loop] -> search_web (DuckDuckGo)
                      -> read_page (fetch + extract) x N
                      -> ResearchBrief (validated Pydantic output)
```

The two tools are `search_web` and `read_page`. Both hit the live web with no
API key. Swap their bodies for a hosted search API or an internal knowledge
base to point the same agent at other sources.

## Configuration

`agent.py` reads `OPENAI_API_KEY` from the environment (via a `.env` file). To
run on another provider, replace the model object in `build_agent()`; the
agent, tools, and system prompt stay the same.

## Links

- Strands Agents SDK: https://github.com/strands-agents/harness-sdk
- Documentation: https://strandsagents.com
