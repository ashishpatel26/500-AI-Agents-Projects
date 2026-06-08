# Customer Support Agent

LangGraph-powered support agent with RAG knowledge base and automatic escalation routing.

**Framework**: LangGraph + FAISS  
**LLM**: GPT-4o-mini  

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
```

## Run

```bash
python agent.py

# Use your own .txt/.md knowledge base files
python agent.py --kb-dir docs/
```

## Features

- RAG over product knowledge base
- Automatic escalation detection for sensitive issues (billing disputes, data loss, etc.)
- Conversation history maintained
- Easily swap in your own knowledge base docs
