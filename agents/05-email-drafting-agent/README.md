# Email Drafting Agent

A CrewAI two-agent system that drafts professional emails. An analyst agent extracts requirements, then a writer agent produces the final email.

**Framework**: CrewAI  
**LLM**: GPT-4o-mini  

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
```

## Run

```bash
# Default example
python agent.py

# Custom email
python agent.py \
  --context "Apologize for the delayed delivery of the software project" \
  --tone "apologetic but confident" \
  --recipient "the client project manager"
```

## Architecture

```
Context → [Analyst Agent] → Email Brief → [Writer Agent] → Final Email
```
