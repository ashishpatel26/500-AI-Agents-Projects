"""
LinkedIn Outreach Agent — generates personalized connection requests and follow-up
sequences using Claude. Logs all outreach to outreach_log.json.
"""

import json
import os
from datetime import datetime
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()

LOG_FILE = Path("outreach_log.json")
CONNECTION_LIMIT = 300  # LinkedIn connection message character limit


def _load_log() -> list[dict]:
    if LOG_FILE.exists():
        return json.loads(LOG_FILE.read_text(encoding="utf-8"))
    return []


def _save_log(entries: list[dict]) -> None:
    LOG_FILE.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")


def _call_claude(system: str, user: str, max_tokens: int = 512) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return message.content[0].text.strip()


def generate_connection_request(profile: dict) -> str:
    """Generate a LinkedIn connection request under 300 characters."""
    system = (
        "You are an expert LinkedIn outreach specialist. Write genuine, concise, "
        "non-spammy connection request notes. Always stay under 300 characters. "
        "Do not use hollow phrases like 'I came across your profile'. Be specific."
    )
    user = (
        f"Write a LinkedIn connection request note for:\n"
        f"Name: {profile['name']}\n"
        f"Title: {profile['title']}\n"
        f"Company: {profile['company']}\n"
        f"Mutual interests / reason to connect: {profile.get('reason', 'AI and technology')}\n\n"
        f"Hard limit: {CONNECTION_LIMIT} characters. Return only the message text."
    )
    message = _call_claude(system, user, max_tokens=150)
    # Enforce character limit as a safety net
    return message[:CONNECTION_LIMIT]


def generate_followup_sequence(profile: dict, connection_message: str) -> dict:
    """Generate a 3-step follow-up sequence after connection is accepted."""
    system = (
        "You are a B2B outreach strategist. Write a three-message LinkedIn follow-up "
        "sequence: (1) warm opener after acceptance, (2) value-add message, "
        "(3) soft ask / CTA. Keep each message under 500 characters. "
        "Be conversational, not salesy. Return valid JSON only."
    )
    user = (
        f"Profile:\nName: {profile['name']}\nTitle: {profile['title']}\n"
        f"Company: {profile['company']}\nGoal: {profile.get('goal', 'explore collaboration')}\n\n"
        f"Original connection note sent:\n{connection_message}\n\n"
        "Return JSON with keys: step1, step2, step3. Each value is the message string."
    )
    raw = _call_claude(system, user, max_tokens=600)
    # Strip markdown fences if present
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(raw)


def run_outreach(profile: dict) -> dict:
    """Full outreach pipeline: connection request + follow-up sequence + log entry."""
    print(f"\n[Agent] Building outreach for {profile['name']} @ {profile['company']}...")

    connection_msg = generate_connection_request(profile)
    print(f"\n--- Connection Request ({len(connection_msg)} chars) ---\n{connection_msg}")

    followups = generate_followup_sequence(profile, connection_msg)
    print("\n--- Follow-up Sequence ---")
    for step, msg in followups.items():
        print(f"\n[{step.upper()}]\n{msg}")

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "profile": profile,
        "connection_message": connection_msg,
        "followup_sequence": followups,
        "status": "pending",
    }

    log = _load_log()
    log.append(entry)
    _save_log(log)
    print(f"\n[Agent] Saved to {LOG_FILE}. Total logged: {len(log)}")
    return entry


def update_status(name: str, company: str, status: str) -> bool:
    """Update outreach status (pending / accepted / replied / closed)."""
    log = _load_log()
    for entry in log:
        if entry["profile"]["name"] == name and entry["profile"]["company"] == company:
            entry["status"] = status
            _save_log(log)
            print(f"[Agent] Updated {name} @ {company} → {status}")
            return True
    print(f"[Agent] No entry found for {name} @ {company}")
    return False
