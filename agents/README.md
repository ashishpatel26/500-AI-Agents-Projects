# Agents — Working Implementations

Each folder is a self-contained, runnable AI agent. No monorepo setup needed.

## Quick Start

```bash
cd agents/<agent-name>
pip install -r requirements.txt
cp .env.example .env   # fill in your API keys
python agent.py
```

## Agent Index

| # | Agent | Framework | LLM | Industry | Difficulty |
|---|---|---|---|---|---|
| 01 | [Web Research Agent](01-web-research-agent/) | LangGraph | GPT-4o / Claude | General | ⭐⭐ |
| 02 | [Code Review Agent](02-code-review-agent/) | LangChain | GPT-4o / Claude | Software Dev | ⭐⭐ |
| 03 | [PDF Q&A Agent](03-pdf-qa-agent/) | LlamaIndex | GPT-4o | Research | ⭐⭐ |
| 04 | [SQL Query Agent](04-sql-query-agent/) | LangChain | GPT-4o | Data | ⭐⭐ |
| 05 | [Email Drafting Agent](05-email-drafting-agent/) | CrewAI | GPT-4o | Communication | ⭐ |
| 06 | [News Summarizer Agent](06-news-summarizer-agent/) | LangChain | GPT-4o | Media | ⭐ |
| 07 | [GitHub Issue Triager](07-github-issue-triager/) | LangGraph | GPT-4o / Claude | DevOps | ⭐⭐ |
| 08 | [Data Analysis Agent](08-data-analysis-agent/) | LangChain | GPT-4o | Analytics | ⭐⭐ |
| 09 | [Resume Parser Agent](09-resume-parser-agent/) | LangChain | GPT-4o | HR | ⭐ |
| 10 | [Meeting Notes Agent](10-meeting-notes-agent/) | LangChain | GPT-4o | Productivity | ⭐⭐ |
| 11 | [Stock Research Agent](11-stock-research-agent/) | LangChain | GPT-4o | Finance | ⭐⭐ |
| 12 | [Travel Planner Agent](12-travel-planner-agent/) | CrewAI | GPT-4o | Travel | ⭐⭐ |
| 13 | [Customer Support Agent](13-customer-support-agent/) | LangGraph | GPT-4o | Customer Service | ⭐⭐⭐ |
| 14 | [Social Media Content Agent](14-social-media-agent/) | CrewAI | GPT-4o | Marketing | ⭐ |
| 15 | [Unit Test Generator Agent](15-unit-test-generator/) | LangChain | GPT-4o / Claude | Software Dev | ⭐⭐ |
| 16 | [Documentation Writer Agent](16-documentation-writer/) | LangChain | GPT-4o / Claude | Software Dev | ⭐⭐ |
| 17 | [Recipe Recommendation Agent](17-recipe-agent/) | LangChain | GPT-4o | Food | ⭐ |
| 18 | [Job Application Agent](18-job-application-agent/) | CrewAI | GPT-4o | HR | ⭐⭐ |
| 19 | [Competitive Analysis Agent](19-competitive-analysis-agent/) | LangGraph | GPT-4o | Business | ⭐⭐⭐ |
| 20 | [Multi-Agent Debate System](20-multi-agent-debate/) | LangChain | GPT-4o | Research | ⭐⭐⭐ |

## Adding Your Agent

1. Create a folder: `agents/NN-your-agent-name/`
2. Include: `agent.py`, `requirements.txt`, `.env.example`, `README.md`, `metadata.yaml`
3. Open a PR following the [PR template](../.github/PULL_REQUEST_TEMPLATE.md)
