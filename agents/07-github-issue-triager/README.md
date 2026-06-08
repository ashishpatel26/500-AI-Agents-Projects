# GitHub Issue Triager

Automatically triages GitHub issues: assigns severity, category, labels, and routing recommendations.

**Framework**: LangChain  
**LLM**: GPT-4o-mini  

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
```

## Run

```bash
# From a GitHub URL
python agent.py --issue-url https://github.com/owner/repo/issues/123

# From title + body text
python agent.py --title "App crashes on login" --body "Steps: 1. Open app 2. Click login 3. App crashes"
```

## Output

```
🔴 Severity: CRITICAL (Priority: 9/10)
📁 Category: bug
👤 Assignee: backend team
🏷️  Labels: bug, critical, authentication
📝 Summary: Authentication crash affecting all users on login
```
