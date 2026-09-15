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

Get a free API key at https://platform.openai.com/api-keys. DuckDuckGo search
needs no key.

## Run

```bash
# Default topic
python agent.py

# Custom topic
python agent.py --topic "how retrieval-augmented generation works"
```

Runtime: under a minute and a few cents on `gpt-4o-mini`.

## Sample Output

```
Topic: Model Context Protocol

Summary: The Model Context Protocol (MCP) is an open-source framework
introduced by Anthropic on November 25, 2024, aimed at standardizing how AI
systems, particularly large language models (LLMs), integrate and interact
with external data sources and tools.

Findings:
  - MCP serves as a universal connector, facilitating communication between AI
    models and external systems without custom integrations.
    source: https://grokipedia.com/page/model-context-protocol
  - It allows AI applications to share context and metadata, which can reduce
    errors such as misinterpretations or hallucinations.
    source: https://cloud.google.com/discover/what-is-model-context-protocol
  - MCP has been adopted by various AI providers and is supported by
    organizations including AWS and Microsoft.
    source: https://en.wikipedia.org/wiki/Model_Context_Protocol

Confidence: high - The information is supported by multiple reliable sources,
including primary documentation and recent articles from reputable platforms.
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
