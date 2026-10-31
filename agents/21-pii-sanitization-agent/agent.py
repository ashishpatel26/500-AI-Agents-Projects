"""PII Sanitization Agent.

Detects and redacts sensitive PII (emails, phone numbers, payment card numbers,
SSNs, government IDs, IP addresses, bank accounts, and API keys) locally before
any transmission to external LLMs or third-party services.

When integrated with the TrustBoost API (https://api.trustboost.dev), all text
is pre-sanitized locally *before* constructing the HTTP request, guaranteeing
that raw sensitive data is never transmitted across the network.
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import logging
import os
import re
import sys
from collections import Counter
from typing import Any

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

try:
    import requests
except ImportError:
    requests = None  # type: ignore

logger = logging.getLogger("pii_sanitization_agent")

API_BASE = os.environ.get("TRUSTBOOST_API_BASE", "https://api.trustboost.dev")
ENDPOINT = f"{API_BASE}/sanitize"

# --- Regular Expressions for Local PII Detection ---

# Email addresses (RFC 5322 subset with boundary checks)
EMAIL_RE = re.compile(
    r"(?<![\w.+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,63}(?![\w-])",
    re.IGNORECASE,
)

# API Keys & Secrets (e.g. OpenAI sk-..., GitHub ghp_..., AWS AKIA...)
API_KEY_RE = re.compile(
    r"(?<![\w-])(?:sk-[a-zA-Z0-9]{20,}|(?:ghp|gho|ghu|ghs|ghr)_[a-zA-Z0-9]{36,}|(?:AKIA|ABIA|ACCA|ASIA)[0-9A-Z]{16})(?![\w-])"
)

# Government IDs & Tax IDs (e.g. Mexican CURP 18-char or RFC 12-13 char)
GOV_ID_RE = re.compile(
    r"\b(?:[A-Z]{4}\d{6}[A-Z0-9]{8}|[A-Z&Ñ]{3,4}\d{6}[A-Z0-9]{3})\b"
)

# US Social Security Numbers (dashed format)
SSN_RE = re.compile(r"(?<!\d)(?!000|666|9\d{2})\d{3}-(?!00)\d{2}-(?!0000)\d{4}(?!\d)")

# Payment Cards (13 to 19 digits with optional spaces or hyphens)
CARD_RE = re.compile(r"(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)")

# Bank Accounts (labeled accounts or IBAN)
BANK_ACCOUNT_RE = re.compile(
    r"(?i)\b(?:account(?:\s*number)?|acc(?:\s*no)?|cuenta)\s*[:#]?\s*([0-9]{8,18})\b"
)
IBAN_RE = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{4,30}\b")

# IP addresses (validated via ipaddress module)
IPV6_CANDIDATE_RE = re.compile(
    r"(?<![\w:])(?=[0-9A-Fa-f:.]*:)[0-9A-Fa-f:.]+(?<!\.)(?![\w:])"
)
IPV4_CANDIDATE_RE = re.compile(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?!\w)")

# Phone numbers (international, domestic, parenthesized, dashed, or 10-15 digits)
PHONE_CANDIDATE_RE = re.compile(
    r"(?<![\w+])(?:\+?\d{1,3}[ .-]?)?(?:\(?\d{2,4}\)?[ .-]?){1,3}\d{3,4}(?![\w-])"
)


def _is_luhn_valid(num_str: str) -> bool:
    """Validate numeric string using the Luhn checksum algorithm."""
    digits = [int(c) for c in num_str if c.isdigit()]
    if not (13 <= len(digits) <= 19):
        return False
    checksum = 0
    reverse_digits = digits[::-1]
    for i, d in enumerate(reverse_digits):
        if i % 2 == 1:
            doubled = d * 2
            checksum += doubled - 9 if doubled > 9 else doubled
        else:
            checksum += d
    return checksum % 10 == 0


def _sanitize_with_counts(
    text: str, enabled_types: set[str] | None = None
) -> tuple[str, Counter[str]]:
    """Sanitize *text* locally and count redacted entity occurrences.

    Redaction order is strictly controlled to prevent partial replacements:
    1. API Keys & Secrets
    2. Email addresses
    3. Government / Tax IDs
    4. Bank Accounts & IBANs
    5. Credit / Debit Cards (with Luhn validation)
    6. US SSNs
    7. IPv6 and IPv4 addresses
    8. Phone numbers
    """
    if not isinstance(text, str):
        raise TypeError(f"Input text must be a string, got {type(text).__name__}")

    if not text:
        return "", Counter()

    counts: Counter[str] = Counter()

    def should_check(entity_type: str) -> bool:
        return enabled_types is None or entity_type in enabled_types

    sanitized = text

    # 1. API Keys
    if should_check("API_KEY"):
        sanitized, counts["API_KEY"] = API_KEY_RE.subn("[API_KEY]", sanitized)

    # 2. Emails
    if should_check("EMAIL"):
        sanitized, counts["EMAIL"] = EMAIL_RE.subn("[EMAIL]", sanitized)

    # 3. Government / Tax IDs
    if should_check("GOV_ID"):
        sanitized, counts["GOV_ID"] = GOV_ID_RE.subn("[GOV_ID]", sanitized)

    # 4. Bank Accounts
    if should_check("BANK_ACCOUNT"):
        def replace_bank_account(match: re.Match) -> str:
            full_match = match.group(0)
            account_num = match.group(1)
            counts["BANK_ACCOUNT"] += 1
            return full_match.replace(account_num, "[BANK_ACCOUNT]")

        sanitized = BANK_ACCOUNT_RE.sub(replace_bank_account, sanitized)

        def replace_iban(match: re.Match) -> str:
            val = match.group(0)
            # Basic IBAN format: 2 country letters, 2 check digits, alphanumeric
            if len(val) >= 15 and val[:2].isalpha() and val[2:4].isdigit():
                counts["BANK_ACCOUNT"] += 1
                return "[BANK_ACCOUNT]"
            return val

        sanitized = IBAN_RE.sub(replace_iban, sanitized)

    # 5. Credit / Debit Cards
    if should_check("CREDIT_CARD"):
        def replace_card(match: re.Match) -> str:
            val = match.group(0)
            digits_only = "".join(c for c in val if c.isdigit())
            # Accept if standard 4x4 format or passes Luhn checksum
            is_grouped = bool(re.fullmatch(r"\d{4}[ -]\d{4}[ -]\d{4}[ -]\d{4}", val))
            if is_grouped or _is_luhn_valid(digits_only):
                counts["CREDIT_CARD"] += 1
                return "[CREDIT_CARD]"
            return val

        sanitized = CARD_RE.sub(replace_card, sanitized)

    # 6. SSN
    if should_check("SSN"):
        sanitized, counts["SSN"] = SSN_RE.subn("[SSN]", sanitized)

    # 7. IP Addresses
    if should_check("IP_ADDRESS"):
        def replace_if_valid_ip(match: re.Match) -> str:
            try:
                ipaddress.ip_address(match.group(0))
            except ValueError:
                return match.group(0)
            counts["IP_ADDRESS"] += 1
            return "[IP_ADDRESS]"

        sanitized = IPV6_CANDIDATE_RE.sub(replace_if_valid_ip, sanitized)
        sanitized = IPV4_CANDIDATE_RE.sub(replace_if_valid_ip, sanitized)

    # 8. Phone Numbers
    if should_check("PHONE"):
        def replace_phone(match: re.Match) -> str:
            val = match.group(0)
            # If formatted as 4 dot-separated octets, it is an IP format, not a phone
            if re.fullmatch(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", val):
                return val
            digit_count = sum(c.isdigit() for c in val)
            if not 10 <= digit_count <= 15:
                return val
            # Exclude strings with only a single repeated digit (e.g. 0000000000, 9999999999)
            if len(set(c for c in val if c.isdigit())) <= 1:
                return val
            counts["PHONE"] += 1
            return "[PHONE]"

        sanitized = PHONE_CANDIDATE_RE.sub(replace_phone, sanitized)

    return sanitized, counts


def _entities_in(counts: Counter[str]) -> list[dict[str, str]]:
    """Build structured entity metadata from recorded redaction counts."""
    return [
        {"type": label.lower(), "category": "PRIVATE", "count": str(count)}
        for label, count in sorted(counts.items())
        if count
    ]


def sanitize_text(text: str) -> str:
    """Return *text* with all detected PII replaced by local placeholders."""
    sanitized, _ = _sanitize_with_counts(text)
    return sanitized


def sanitize_locally(text: str) -> dict[str, Any]:
    """Perform purely local, offline PII sanitization returning structured results."""
    sanitized_content, counts = _sanitize_with_counts(text)
    entities = _entities_in(counts)
    risk_category = "PRIVATE" if entities else "UNKNOWN"
    return {
        "status": "success",
        "data": {
            "sanitized_content": sanitized_content,
            "risk_category": risk_category,
            "entities": entities,
        },
        "sanitized_content": sanitized_content,
        "risk_category": risk_category,
    }


def _call_trustboost_api(
    sanitized_text: str,
    context: str,
    tx_hash: str,
    timeout: int,
    local_entities: list[dict[str, str]],
) -> dict[str, Any]:
    """Securely dispatch pre-sanitized text to the TrustBoost API.

    Guarantees:
    - Only pre-sanitized content is included in the payload.
    - Raw PII is never transmitted over the network.
    - Fails closed / falls back safely on timeouts, HTTP errors, or transport issues.
    - Never logs or exposes raw user data.
    """
    if requests is None:
        return {
            "status": "error",
            "risk_category": "PRIVATE" if local_entities else "UNKNOWN",
            "data": {
                "sanitized_content": sanitized_text,
                "risk_category": "PRIVATE" if local_entities else "UNKNOWN",
                "entities": local_entities,
            },
            "sanitized_content": sanitized_text,
            "error": "The 'requests' package is not installed; using local sanitization",
        }

    payload = {
        "text": sanitized_text,  # ALWAYS sanitized, NEVER raw text
        "tx_hash": tx_hash,
        "wallet_address": os.environ.get("TRUSTBOOST_WALLET", "demo-agent"),
        "context": context,
    }

    try:
        resp = requests.post(
            ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json", "User-Agent": "500-AI-Agents-PII-Sanitizer/1.0"},
            timeout=timeout,
        )
    except requests.Timeout:
        return {
            "status": "error",
            "risk_category": "PRIVATE" if local_entities else "UNKNOWN",
            "data": {
                "sanitized_content": sanitized_text,
                "risk_category": "PRIVATE" if local_entities else "UNKNOWN",
                "entities": local_entities,
            },
            "sanitized_content": sanitized_text,
            "error": "Third-party sanitization service timed out; local sanitization preserved",
        }
    except requests.RequestException:
        return {
            "status": "error",
            "risk_category": "PRIVATE" if local_entities else "UNKNOWN",
            "data": {
                "sanitized_content": sanitized_text,
                "risk_category": "PRIVATE" if local_entities else "UNKNOWN",
                "entities": local_entities,
            },
            "sanitized_content": sanitized_text,
            "error": "Third-party sanitization service unreachable; local sanitization preserved",
        }

    if resp.status_code == 200:
        try:
            data = resp.json()
            # Ensure sanitized_content remains safely available
            if isinstance(data, dict):
                if "sanitized_content" not in data and "data" in data and isinstance(data["data"], dict):
                    data["sanitized_content"] = data["data"].get("sanitized_content", sanitized_text)
                return data
        except Exception:
            pass
        return {
            "status": "success",
            "data": {
                "sanitized_content": sanitized_text,
                "risk_category": "PRIVATE" if local_entities else "UNKNOWN",
                "entities": local_entities,
            },
            "sanitized_content": sanitized_text,
        }

    if resp.status_code == 402:
        return {
            "status": "payment_required",
            "risk_category": "PRIVATE" if local_entities else "UNKNOWN",
            "data": {
                "sanitized_content": sanitized_text,
                "risk_category": "PRIVATE" if local_entities else "UNKNOWN",
                "entities": local_entities,
            },
            "sanitized_content": sanitized_text,
            "detail": "Payment required for TrustBoost API; local sanitization preserved",
        }

    return {
        "status": "error",
        "http_status": resp.status_code,
        "risk_category": "PRIVATE" if local_entities else "UNKNOWN",
        "data": {
            "sanitized_content": sanitized_text,
            "risk_category": "PRIVATE" if local_entities else "UNKNOWN",
            "entities": local_entities,
        },
        "sanitized_content": sanitized_text,
        "error": f"Remote service returned HTTP {resp.status_code}; local sanitization preserved",
    }


def sanitize(
    text: str,
    context: str = "general",
    tx_hash: str = "TRIAL",
    call_api: bool | None = None,
    timeout: int = 30,
) -> dict[str, Any]:
    """Sanitize text by performing local redaction first, then optionally calling the remote API.

    Guarantees:
    - Local PII detection and sanitization ALWAYS runs first.
    - If ``call_api`` is True (or TRUSTBOOST_CALL_API=true in environment), the pre-sanitized
      content is securely transmitted to the TrustBoost API.
    - If the remote API fails, times out, or requires payment, local sanitization is preserved.
    - Backward-compatible with both legacy and new structured return shapes.

    Args:
        text: Raw text to sanitize.
        context: Context classification (general|financial|legal|medical|code).
        tx_hash: "TRIAL" or payment transaction hash.
        call_api: Whether to call the external TrustBoost API. Defaults to checking
                  the TRUSTBOOST_CALL_API environment variable, or False if unset.
        timeout: Network timeout in seconds.
    """
    if not isinstance(text, str):
        raise TypeError(f"Input text must be a string, got {type(text).__name__}")

    # Step 1: ALWAYS perform local sanitization first
    sanitized_content, counts = _sanitize_with_counts(text)
    local_entities = _entities_in(counts)
    risk_category = "PRIVATE" if local_entities else "UNKNOWN"

    # Step 2: Determine if third-party API should be called
    if call_api is None:
        env_val = os.environ.get("TRUSTBOOST_CALL_API", "").strip().lower()
        call_api = env_val in ("1", "true", "yes", "on")

    # Step 3: If API is not requested, return the local sanitization result directly
    if not call_api:
        return {
            "status": "success",
            "data": {
                "sanitized_content": sanitized_content,
                "risk_category": risk_category,
                "entities": local_entities,
            },
            "sanitized_content": sanitized_content,
            "risk_category": risk_category,
        }

    # Step 4: Securely call external API with pre-sanitized text only
    return _call_trustboost_api(
        sanitized_text=sanitized_content,
        context=context,
        tx_hash=tx_hash,
        timeout=timeout,
        local_entities=local_entities,
    )


DEMO_TEXT = (
    "Hi, I'm Juan Pérez. My email is juan.perez@example.com and my phone is "
    "+1 (555) 123-4567. RFC: PEMJ880126MNEZSN01. Account 0123456789. "
    "Card: 4111-1111-1111-1111. SSN: 123-45-6789. "
    "IPv4: 192.0.2.42; IPv6: 2001:db8::1. "
    "API key: sk-abc123fakekeynotreal0000000000."
)


def _run_self_checks() -> None:
    """Run regression checks without making network requests."""
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
    assert literal_placeholder_result["data"]["risk_category"] == "UNKNOWN"

    phone_result = sanitize("Call me at 9876543210.")
    assert phone_result["data"]["sanitized_content"] == "Call me at [PHONE]."

    card_result = sanitize("Card 4111-1111-1111-1111")
    assert card_result["data"]["sanitized_content"] == "Card [CREDIT_CARD]"

    ssn_result = sanitize("SSN 123-45-6789")
    assert ssn_result["data"]["sanitized_content"] == "SSN [SSN]"

    demo_result = sanitize(DEMO_TEXT)
    sanitized_demo = demo_result["data"]["sanitized_content"]
    assert "juan.perez@example.com" not in sanitized_demo
    assert "+1 (555) 123-4567" not in sanitized_demo
    assert "4111-1111-1111-1111" not in sanitized_demo
    assert "123-45-6789" not in sanitized_demo
    assert "192.0.2.42" not in sanitized_demo
    assert "2001:db8::1" not in sanitized_demo
    assert "sk-abc123fakekeynotreal0000000000" not in sanitized_demo


def main() -> None:
    """Run the command-line interface without printing raw input."""
    parser = argparse.ArgumentParser(
        description="PII Sanitization Agent with Local Pre-Sanitization & Secure API Integration"
    )
    parser.add_argument("--text", help="text to sanitize")
    parser.add_argument("--file", help="path to a text file to sanitize")
    parser.add_argument("--context", default="general", help="context: general|financial|legal|medical|code")
    parser.add_argument("--tx-hash", default="TRIAL", help="TRIAL for free tier, or Solana tx hash")
    parser.add_argument(
        "--api",
        action="store_true",
        default=False,
        help="send pre-sanitized text to TrustBoost API for remote verification",
    )
    parser.add_argument("--self-test", action="store_true", help="run built-in regression checks and exit")
    args = parser.parse_args()

    if args.self_test:
        _run_self_checks()
        print("Self-checks passed successfully.")
        return

    if args.file:
        with open(args.file, "r", encoding="utf-8") as source:
            text = source.read()
    elif args.text:
        text = args.text
    else:
        text = DEMO_TEXT
        print("No --text/--file provided. Running demo with local pre-sanitization.\n")

    result = sanitize(
        text,
        context=args.context,
        tx_hash=args.tx_hash,
        call_api=args.api,
    )
    # Output only the sanitized result, never raw input
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    _run_self_checks()
    main()
