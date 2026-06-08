# SQL Query Agent

Connects to any SQLite database and answers natural language questions by generating and executing SQL.

**Framework**: LangChain  
**LLM**: GPT-4o-mini  

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
```

## Run

```bash
# Demo mode — creates a sample e-commerce database automatically
python agent.py

# Your own database
python agent.py --db path/to/your/database.sqlite

# Single question
python agent.py --question "What is the total revenue by country?"
```

Databases open in read-only mode by default. Use `--allow-write` only with a disposable database
if you intentionally want the generated SQL agent to be able to mutate data.

## Example Questions

- "How many customers do we have in each country?"
- "What are the top 3 best-selling products?"
- "What was the total revenue last month?"
- "Which customer has spent the most?"

## Architecture

```
Natural Language → LLM (generates SQL) → SQLite → LLM (formats answer) → Response
```
