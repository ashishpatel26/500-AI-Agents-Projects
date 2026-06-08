# Meeting Notes Agent

Converts meeting transcripts into structured notes with summary, action items, decisions, and follow-ups.

**Framework**: LangChain  
**LLM**: GPT-4o-mini  

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
```

## Run

```bash
# Use built-in sample transcript
python agent.py

# Your own transcript file
python agent.py --transcript meeting_transcript.txt

# Inline text
python agent.py --text "Alice: Let's ship by Friday. Bob: I need 2 more days for testing..."

# Custom output path
python agent.py --transcript meeting_transcript.txt --output sprint_notes.md
```

## Output

Saves structured markdown to `meeting_notes.md` by default. If that file already exists,
the agent writes a timestamped file instead. The output includes:
- Executive summary
- Key decisions
- Action items with owners and due dates
- Blockers
- Next meeting time
