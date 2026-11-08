"""Local, zero-network PII sanitization agent.

Redacts common PII before text is passed to an LLM or another external service.
All matching happens in this process using only Python's standard library; the
raw text is never transmitted by this module.

Usage:
    python agent.py --text "Call me at 555-123-4567, email a@b.com"
    python agent.py --file input.txt
    python agent.py  # runs the built-in offline examples
"""

import argparse
import ipaddress
import json
import re
from collections import Counter


EMAIL_RE = re.compile(
    r"(?<![\w.+-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,63}(?![\w-])",
    re.IGNORECASE,
)
SSN_RE = re.compile(r"(?<!\d)\d{3}-?\d{2}-?\d{4}(?!\d)")
CARD_RE = re.compile(r"(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)")

# Candidates are validated by ``ipaddress`` before redaction so ordinary
# colon-separated text and invalid IPv4 values are not mistakenly removed.
IPV6_CANDIDATE_RE = re.compile(
    r"(?<![\w:])(?=[0-9A-Fa-f:.]*:)[0-9A-Fa-f:.]+(?<!\.)(?![\w:])"
)
IPV4_CANDIDATE_RE = re.compile(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?!\w)")

# Accept common national/international formats. The replacement callback
# requires 10–15 digits, avoiding short numeric strings.
PHONE_CANDIDATE_RE = re.compile(
    r"(?<![\w+])(?:\+?\d{1,3}[ .-]?)?(?:\(?\d{2,4}\)?[ .-]?){1,3}\d{3,4}(?![\w-])"
)


def _sanitize_with_counts(text: str) -> tuple[str, Counter[str]]:
    """Return *text* with common PII replaced by stable placeholder labels.

    Cards are processed before phones so a card number cannot be partially
    replaced as a phone number. IPv6 is processed before IPv4 for the same
    reason when an IPv4 address appears inside an IPv6 representation.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    counts: Counter[str] = Counter()
    sanitized, counts["EMAIL"] = EMAIL_RE.subn("[EMAIL]", text)
    sanitized, counts["SSN"] = SSN_RE.subn("[SSN]", sanitized)
    sanitized, counts["CREDIT_CARD"] = CARD_RE.subn("[CREDIT_CARD]", sanitized)

    def replace_if_valid_ip(match: re.Match) -> str:
        """Redact only valid address candidates and record actual replacements."""
        try:
            ipaddress.ip_address(match.group(0))
        except ValueError:
            return match.group(0)
        counts["IP_ADDRESS"] += 1
        return "[IP_ADDRESS]"

    def replace_phone(match: re.Match) -> str:
        """Redact only phone candidates with a plausible digit count."""
        value = match.group(0)
        digit_count = sum(char.isdigit() for char in value)
        if not 10 <= digit_count <= 15:
            return value
        counts["PHONE"] += 1
        return "[PHONE]"

    sanitized = IPV6_CANDIDATE_RE.sub(replace_if_valid_ip, sanitized)
    sanitized = IPV4_CANDIDATE_RE.sub(replace_if_valid_ip, sanitized)
    sanitized = PHONE_CANDIDATE_RE.sub(replace_phone, sanitized)
    return sanitized, counts


def sanitize_text(text: str) -> str:
    """Return *text* with common PII replaced by stable placeholder labels."""
    sanitized, _ = _sanitize_with_counts(text)
    return sanitized


def _entities_in(counts: Counter[str]) -> list[dict[str, str]]:
    """Build metadata from actual redactions, never literal input placeholders."""
    return [
        {"type": label.lower(), "category": "PRIVATE", "count": str(count)}
        for label, count in sorted(counts.items())
        if count
    ]


def sanitize(text: str, context: str = "general", tx_hash: str = "TRIAL") -> dict:
    """Sanitize text locally and return the legacy structured result shape.

    ``context`` and ``tx_hash`` remain accepted for compatibility with existing
    callers. They are intentionally unused: this function performs no I/O.
    """
    del context, tx_hash
    sanitized_content, counts = _sanitize_with_counts(text)
    entities = _entities_in(counts)
    return {
        "status": "success",
        "data": {
            "sanitized_content": sanitized_content,
            "safety_score": 1.0,
            "risk_category": "PRIVATE" if entities else "NONE",
            "entities": entities,
        },
    }


DEMO_TEXT = (
    "Email: juan.perez@example.com; phone: +1 (555) 123-4567; "
    "card: 4111-1111-1111-1111; SSN: 123-45-6789; "
    "IPv4: 192.0.2.42; IPv6: 2001:db8::1."
)


def main() -> None:
    """Run the command-line interface without printing raw input."""
    parser = argparse.ArgumentParser(description="Local, offline PII Sanitization Agent")
    parser.add_argument("--text", help="text to sanitize")
    parser.add_argument("--file", help="path to a text file to sanitize")
    parser.add_argument("--context", default="general", help="accepted for compatibility; unused")
    parser.add_argument("--tx-hash", default="TRIAL", help="accepted for compatibility; unused")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as source:
            text = source.read()
    elif args.text:
        text = args.text
    else:
        text = DEMO_TEXT
        print("No --text/--file provided. Running local offline redaction demo.\n")

    result = sanitize(text, context=args.context, tx_hash=args.tx_hash)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def _run_self_checks() -> None:
    """Check regression cases without making network requests."""
    email_result = sanitize("a@b.com.")
    assert email_result["data"]["sanitized_content"] == "[EMAIL]."
    assert email_result["data"]["entities"] == [
        {"type": "email", "category": "PRIVATE", "count": "1"}
    ]

    ipv6_result = sanitize("2001:db8::1.")
    assert ipv6_result["data"]["sanitized_content"] == "[IP_ADDRESS]."

    literal_placeholder_result = sanitize("The literal [EMAIL] is not PII.")
    assert literal_placeholder_result["data"]["sanitized_content"] == "The literal [EMAIL] is not PII."
    assert literal_placeholder_result["data"]["entities"] == []
    assert literal_placeholder_result["data"]["risk_category"] == "NONE"


if __name__ == "__main__":
    _run_self_checks()
    main()
