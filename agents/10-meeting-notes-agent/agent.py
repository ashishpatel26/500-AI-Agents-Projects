"""
Meeting Notes Agent.

Converts meeting transcript text into structured meeting notes:
summary, action items, decisions, and follow-ups.

Usage:
    python agent.py --transcript meeting.txt
    python agent.py --text "John: Let's ship v2 next Friday..."
"""

import argparse
import json
import os
import re
from datetime import date, datetime

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

load_dotenv()

NOTES_PROMPT = """You are a professional meeting note-taker. Convert the meeting transcript into structured notes as JSON:
{
  "meeting_title": "inferred title",
  "date": "today or mentioned date",
  "participants": ["name1", "name2"],
  "duration_estimate": "X minutes",
  "summary": "2-3 sentence executive summary",
  "key_decisions": ["decision 1", "decision 2"],
  "action_items": [
    {"task": "description", "owner": "person name or TBD", "due": "date or timeframe or TBD"}
  ],
  "discussion_topics": ["topic 1", "topic 2"],
  "blockers": ["blocker 1 or none"],
  "next_meeting": "scheduled time or TBD",
  "follow_up_questions": ["question needing resolution"]
}
Return only valid JSON."""

SAMPLE_TRANSCRIPT = """
Sarah: Alright everyone, let's get started. It's Monday the 3rd and we have John, Mike, and Lisa here.

John: Thanks Sarah. So the main thing I wanted to cover is the Q4 product roadmap.
We need to decide on the feature freeze date.

Sarah: I think we should freeze by November 15th. That gives QA three weeks before the holiday release.

Mike: That works for me. But we still need to finalize the payment integration. Lisa, where are you on that?

Lisa: I'm about 60% done. I need the API docs from the payment provider. I've emailed them twice but haven't heard back.

John: I'll escalate that today. I'll reach out to our account manager at PaymentCo. That's blocking us.

Sarah: Okay, so John will handle the PaymentCo escalation by end of today. Lisa continues on payment integration, targeting completion by November 10th.

Mike: I can help with testing once Lisa has a draft ready. Let's say I start testing November 11th.

Sarah: Great. Also, we decided to cut the social login feature from this release. Too risky to add now.

John: Agreed. We'll put it in Q1 backlog.

Sarah: Any other blockers? No? Okay. Same time next week, November 10th.
"""


def parse_json_response(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        cleaned = match.group(0)
    return json.loads(cleaned)


def generate_meeting_notes(transcript: str) -> dict:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    messages = [
        SystemMessage(content=NOTES_PROMPT),
        HumanMessage(content=f"Meeting transcript:\n\n{transcript}"),
    ]
    response = llm.invoke(messages)
    return parse_json_response(response.content)


def format_notes(notes: dict) -> str:
    lines = [
        f"# {notes.get('meeting_title', 'Meeting Notes')}",
        f"**Date:** {notes.get('date', date.today().isoformat())}  |  **Duration:** {notes.get('duration_estimate', 'N/A')}",
        f"**Participants:** {', '.join(notes.get('participants', []))}",
        "",
        "## Summary",
        notes.get("summary", ""),
        "",
        "## Key Decisions",
        *[f"- {d}" for d in notes.get("key_decisions", [])],
        "",
        "## Action Items",
    ]
    for item in notes.get("action_items", []):
        lines.append(f"- [ ] **{item.get('task', 'Task')}** — Owner: {item.get('owner', 'TBD')} | Due: {item.get('due', 'TBD')}")

    if notes.get("blockers"):
        lines += ["", "## Blockers", *[f"- {b}" for b in notes["blockers"]]]

    if notes.get("next_meeting") and notes["next_meeting"] != "TBD":
        lines += ["", f"**Next Meeting:** {notes['next_meeting']}"]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Meeting Notes Agent")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--transcript", help="Path to transcript text file")
    group.add_argument("--text", help="Transcript text directly")
    parser.add_argument("--output", default="meeting_notes.md", help="Markdown output path")
    args = parser.parse_args()

    if args.transcript:
        with open(args.transcript) as f:
            transcript = f.read()
        print(f"\n📝 Processing: {args.transcript}\n")
    elif args.text:
        transcript = args.text
        print("\n📝 Processing transcript...\n")
    else:
        print("\n📝 Using sample meeting transcript\n")
        transcript = SAMPLE_TRANSCRIPT

    notes = generate_meeting_notes(transcript)
    formatted = format_notes(notes)

    print("=" * 60)
    print(formatted)
    print("=" * 60)

    # Save to file
    output_file = args.output
    if os.path.exists(output_file) and args.output == "meeting_notes.md":
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"meeting_notes_{stamp}.md"
    with open(output_file, "w") as f:
        f.write(formatted)
    print(f"\n✅ Saved to: {output_file}")


if __name__ == "__main__":
    main()
