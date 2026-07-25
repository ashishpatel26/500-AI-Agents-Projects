"""
PII Sanitization Agent — client for the TrustBoost API.

Removes sensitive data (emails, phones, national IDs, bank accounts,
API keys) from text before it reaches an LLM or external API. Built for
autonomous agent pipelines where human review is not possible.

This is a thin client: the sanitization logic, models, and on-chain
proof live behind the TrustBoost API. The agent demonstrates the
privacy/security pattern — call it on any user text before an LLM call.

Usage:
    python agent.py --text "Call me at 555-123-4567, email a@b.com"
    python agent.py --file input.txt
    python agent.py   # runs the built-in demo

Uses the free trial (50 sanitizations) when no API key / tx_hash is set.
"""

import argparse
import os
import sys
import json

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

import requests

API_BASE = os.environ.get("TRUSTBOOST_API_BASE", "https://api.trustboost.dev")
ENDPOINT = f"{API_BASE}/sanitize"


def sanitize(text: str, context: str = "general", tx_hash: str = "TRIAL") -> dict:
    """Send text to TrustBoost and return the sanitized result.

    Args:
        text: raw text that may contain PII
        context: general | financial | legal | medical | code
        tx_hash: "TRIAL" for the free tier, or a Solana tx hash after payment
    """
    payload = {
        "text": text,
        "tx_hash": tx_hash,
        "wallet_address": os.environ.get("TRUSTBOOST_WALLET", "demo-agent"),
        "context": context,
    }
    try:
        resp = requests.post(ENDPOINT, json=payload, timeout=30)
    except requests.RequestException as e:
        # Fail closed: do NOT return raw PII on transport error.
        return {
            "status": "error",
            "risk_category": "CRITICAL",
            "sanitized_content": "[REDACTED — sanitization service unreachable]",
            "error": str(e),
        }

    if resp.status_code == 200:
        return resp.json()

    if resp.status_code == 402:
        # Payment required — the service is live but needs a paid tx_hash.
        return {
            "status": "payment_required",
            "risk_category": "CRITICAL",
            "sanitized_content": "[REDACTED — payment required to sanitize]",
            "detail": resp.json().get("error", "Payment required"),
        }

    # Any other failure: fail closed.
    return {
        "status": "error",
        "risk_category": "CRITICAL",
        "sanitized_content": "[REDACTED — unexpected response]",
        "http_status": resp.status_code,
    }


DEMO_TEXT = (
    "Hi, I'm Juan Pérez. My email is juan.perez@example.com and my phone is "
    "+1-555-123-4567. RFC: PEMJ880126MNEZSN01. Account 0123456789. "
    "API key sk-abc123fakekeynotreal0000000000."
)


def main():
    ap = argparse.ArgumentParser(description="PII Sanitization Agent (TrustBoost client)")
    ap.add_argument("--text", help="text to sanitize")
    ap.add_argument("--file", help="path to a text file to sanitize")
    ap.add_argument("--context", default="general", help="general|financial|legal|medical|code")
    ap.add_argument("--tx-hash", default="TRIAL", help="TRIAL for free tier, or Solana tx hash")
    args = ap.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        text = DEMO_TEXT
        print("No --text/--file provided. Running built-in demo.\n")

    print("INPUT :", text[:120] + ("..." if len(text) > 120 else ""))
    result = sanitize(text, context=args.context, tx_hash=args.tx_hash)
    print("\nRESULT :")
    print(json.dumps(result, indent=2, ensure_ascii=False)[:800])


if __name__ == "__main__":
    main()
