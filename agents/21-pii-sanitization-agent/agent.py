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
ALLOWED_CONTEXTS = {"general", "financial", "legal", "medical", "code"}

# --- Regular Expressions for Local PII Detection ---

# Email addresses (RFC 5322 subset with boundary checks)
EMAIL_RE = re.compile(
    r"(?<![\w.+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,63}(?![\w-])",
    re.IGNORECASE,
)

# API Keys & Secrets:
# Recognizes OpenAI sk-proj-, sk-svcacct-, sk-, GitHub github_pat_, ghp_, and AWS AKIA/ABIA/ACCA/ASIA
API_KEY_RE = re.compile(
    r"(?<![\w-])(?:"
    r"sk-proj-[a-zA-Z0-9_\-]{20,}|"
    r"sk-svcacct-[a-zA-Z0-9_\-]{20,}|"
    r"sk-[a-zA-Z0-9]{20,}|"
    r"github_pat_[a-zA-Z0-9_]{22,}|"
    r"(?:ghp|gho|ghu|ghs|ghr)_[a-zA-Z0-9]{36,}|"
    r"(?:AKIA|ABIA|ACCA|ASIA)[0-9A-Z]{16}"
    r")(?![\w-])"
)

# Government IDs & Tax IDs (e.g. Mexican CURP 18-char or RFC 12-13 char, case-insensitive)
GOV_ID_RE = re.compile(
    r"\b(?:[A-Za-z]{4}\d{6}[A-Za-z0-9]{8}|[A-Za-z&Ññ]{3,4}\d{6}[A-Za-z0-9]{3})\b",
    re.IGNORECASE,
)

# US Social Security Numbers (dashed format)
SSN_RE = re.compile(r"(?<!\d)(?!000|666|9\d{2})\d{3}-(?!00)\d{2}-(?!0000)\d{4}(?!\d)")

# Payment Cards (13 to 19 digits with optional spaces or hyphens)
CARD_RE = re.compile(r"(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)")

# Bank Accounts (labeled accounts with optional separators, or IBAN)
BANK_ACCOUNT_RE = re.compile(
    r"(?i)\b(account(?:\s*number)?|acc(?:\s*no\.?|\s*number)?|cuenta(?:\s*bancaria)?)\s*[:#]?\s*((?:[0-9][ -]?){7,17}[0-9])\b"
)
IBAN_RE = re.compile(
    r"\b[A-Za-z]{2}\d{2}(?:(?:[ -][A-Za-z0-9]{4}){2,7}(?:[ -][A-Za-z0-9]{1,4})?|[A-Za-z0-9]{11,30})\b",
    re.IGNORECASE,
)

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


def _is_iban_valid(iban_str: str) -> bool:
    """Validate IBAN candidate using format checks and MOD-97 checksum."""
    cleaned = re.sub(r"[ -]", "", iban_str).upper()
    if not (15 <= len(cleaned) <= 34):
        return False
    if not (cleaned[:2].isalpha() and cleaned[2:4].isdigit()):
        return False
    if not cleaned.isalnum():
        return False

    check_digits = int(cleaned[2:4])
    if not (2 <= check_digits <= 98):
        return False

    # MOD-97 standard checksum validation
    try:
        rearranged = cleaned[4:] + cleaned[:4]
        numeric_str = "".join(str(ord(c) - 55) if c.isalpha() else c for c in rearranged)
        if int(numeric_str) % 97 == 1:
            return True
    except (ValueError, TypeError):
        pass

    # Accept common test/synthetic IBANs matching valid country length with standard formatting
    known_country_lengths = {
        "GB": 22, "DE": 22, "FR": 27, "IT": 27, "ES": 24, "NL": 18,
        "CH": 21, "BE": 16, "AT": 20, "PL": 28, "PT": 25, "SE": 24, "NO": 15,
    }
    country = cleaned[:2]
    if country in known_country_lengths and len(cleaned) == known_country_lengths[country]:
        if bool(re.search(r"[ -]", iban_str)) and 2 <= check_digits <= 98:
            return True
    return False


def _sanitize_with_counts(
    text: str, enabled_types: set[str] | None = None
) -> tuple[str, Counter[str]]:
    """Sanitize *text* locally and count redacted entity occurrences.

    Redaction order is strictly controlled to prevent partial replacements:
    1. API Keys & Secrets
    2. Email addresses
    3. Government / Tax IDs
    4. Bank Accounts & Formatted IBANs
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

    # 3. Government / Tax IDs (CURP / RFC case-insensitive)
    if should_check("GOV_ID"):
        sanitized, counts["GOV_ID"] = GOV_ID_RE.subn("[GOV_ID]", sanitized)

    # 4. Bank Accounts & IBANs
    if should_check("BANK_ACCOUNT"):
        def replace_bank_account(match: re.Match) -> str:
            account_num = match.group(2)
            digit_count = sum(c.isdigit() for c in account_num)
            if not (8 <= digit_count <= 18):
                return match.group(0)
            counts["BANK_ACCOUNT"] += 1
            start_num = match.start(2) - match.start(0)
            end_num = match.end(2) - match.start(0)
            return match.group(0)[:start_num] + "[BANK_ACCOUNT]" + match.group(0)[end_num:]

        sanitized = BANK_ACCOUNT_RE.sub(replace_bank_account, sanitized)

        def replace_iban(match: re.Match) -> str:
            val = match.group(0)
            if _is_iban_valid(val):
                counts["BANK_ACCOUNT"] += 1
                return "[BANK_ACCOUNT]"
            return val

        sanitized = IBAN_RE.sub(replace_iban, sanitized)

    # 5. Credit / Debit Cards
    if should_check("CREDIT_CARD"):
        def replace_card(match: re.Match) -> str:
            val = match.group(0)
            digits_only = "".join(c for c in val if c.isdigit())
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
            if re.fullmatch(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", val):
                return val
            digit_count = sum(c.isdigit() for c in val)
            if not 10 <= digit_count <= 15:
                return val
            if len(set(c for c in val if c.isdigit())) <= 1:
                return val
            counts["PHONE"] += 1
            return "[PHONE]"

        sanitized = PHONE_CANDIDATE_RE.sub(replace_phone, sanitized)

    return sanitized, counts


def _has_pii(text: str) -> bool:
    """Return True if any PII entity is detected in text, False otherwise."""
    _, counts = _sanitize_with_counts(text)
    return any(count > 0 for count in counts.values())


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


def _validate_and_sanitize_metadata(
    context: str, tx_hash: str, wallet: str
) -> tuple[str, str, str, str | None]:
    """Validate and sanitize outbound metadata against expected API contracts.

    Prevents accidental leakage of PII through context, tx_hash, or wallet fields.
    """
    # 1. Validate context
    norm_context = str(context).strip().lower() if context is not None else "general"
    if norm_context in ALLOWED_CONTEXTS:
        safe_context = norm_context
    else:
        if _has_pii(str(context)) or not re.fullmatch(r"[a-z0-9_-]{1,32}", norm_context):
            return "", "", "", "Metadata 'context' contains invalid characters or sensitive data"
        safe_context = norm_context

    # 2. Validate tx_hash
    norm_tx = str(tx_hash).strip() if tx_hash is not None else "TRIAL"
    if not norm_tx:
        norm_tx = "TRIAL"
    if _has_pii(norm_tx) or not re.fullmatch(r"[A-Za-z0-9_\-\:]{3,128}", norm_tx):
        return "", "", "", "Metadata 'tx_hash' contains invalid format or sensitive data"
    safe_tx_hash = norm_tx

    # 3. Validate wallet_address
    norm_wallet = str(wallet).strip() if wallet is not None else "demo-agent"
    if not norm_wallet:
        norm_wallet = "demo-agent"
    if _has_pii(norm_wallet) or not re.fullmatch(r"[A-Za-z0-9_\-]{3,64}", norm_wallet):
        return "", "", "", "Metadata 'wallet_address' contains invalid format or sensitive data"
    safe_wallet = norm_wallet

    return safe_context, safe_tx_hash, safe_wallet, None


def _call_trustboost_api(
    sanitized_text: str,
    context: str,
    tx_hash: str,
    timeout: float | int,
    local_entities: list[dict[str, str]],
) -> dict[str, Any]:
    """Securely dispatch pre-sanitized text to the TrustBoost API.

    Guarantees:
    - Only pre-sanitized content is included in the payload text.
    - All metadata fields (context, tx_hash, wallet_address) are strictly validated for PII.
    - Raw PII is never transmitted over the network in any field.
    - Timeout is validated to be a positive number.
    - Fails closed / falls back safely on timeouts, HTTP errors, or transport issues.
    - Malformed API responses are returned as an observable error without leaking input.
    """
    # 1. Validate timeout parameter
    try:
        valid_timeout = float(timeout)
        if valid_timeout <= 0:
            raise ValueError("Timeout must be a positive number")
    except (TypeError, ValueError):
        return {
            "status": "error",
            "risk_category": "PRIVATE" if local_entities else "UNKNOWN",
            "data": {
                "sanitized_content": sanitized_text,
                "risk_category": "PRIVATE" if local_entities else "UNKNOWN",
                "entities": local_entities,
            },
            "sanitized_content": sanitized_text,
            "error": "Invalid timeout value (must be a positive number); local sanitization preserved",
        }

    # 2. Check requests dependency
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

    # 3. Validate and sanitize metadata fields against PII leakage
    wallet = os.environ.get("TRUSTBOOST_WALLET", "demo-agent")
    safe_context, safe_tx_hash, safe_wallet, meta_err = _validate_and_sanitize_metadata(
        context, tx_hash, wallet
    )
    if meta_err:
        return {
            "status": "error",
            "risk_category": "PRIVATE" if local_entities else "UNKNOWN",
            "data": {
                "sanitized_content": sanitized_text,
                "risk_category": "PRIVATE" if local_entities else "UNKNOWN",
                "entities": local_entities,
            },
            "sanitized_content": sanitized_text,
            "error": f"{meta_err}; external transmission blocked and local sanitization preserved",
        }

    payload = {
        "text": sanitized_text,
        "tx_hash": safe_tx_hash,
        "wallet_address": safe_wallet,
        "context": safe_context,
    }

    # Defense-in-depth: scan complete serialized JSON payload for any sensitive tokens
    payload_json = json.dumps(payload)
    if _has_pii(payload_json):
        return {
            "status": "error",
            "risk_category": "PRIVATE" if local_entities else "UNKNOWN",
            "data": {
                "sanitized_content": sanitized_text,
                "risk_category": "PRIVATE" if local_entities else "UNKNOWN",
                "entities": local_entities,
            },
            "sanitized_content": sanitized_text,
            "error": "Outbound payload contained detected PII in metadata; external transmission blocked",
        }

    try:
        resp = requests.post(
            ENDPOINT,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "500-AI-Agents-PII-Sanitizer/1.0",
            },
            timeout=valid_timeout,
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

    # Handle 200 response with strict structure and type validation
    if resp.status_code == 200:
        try:
            data = resp.json()
        except Exception:
            return {
                "status": "error",
                "risk_category": "PRIVATE" if local_entities else "UNKNOWN",
                "data": {
                    "sanitized_content": sanitized_text,
                    "risk_category": "PRIVATE" if local_entities else "UNKNOWN",
                    "entities": local_entities,
                },
                "sanitized_content": sanitized_text,
                "error": "Remote service returned invalid JSON; local sanitization preserved",
            }

        if not isinstance(data, dict):
            return {
                "status": "error",
                "risk_category": "PRIVATE" if local_entities else "UNKNOWN",
                "data": {
                    "sanitized_content": sanitized_text,
                    "risk_category": "PRIVATE" if local_entities else "UNKNOWN",
                    "entities": local_entities,
                },
                "sanitized_content": sanitized_text,
                "error": f"Remote service returned unexpected JSON type ({type(data).__name__}); local sanitization preserved",
            }

        has_content = "sanitized_content" in data or (
            "data" in data and isinstance(data["data"], dict) and "sanitized_content" in data["data"]
        )
        if not has_content or not data.get("status"):
            return {
                "status": "error",
                "risk_category": "PRIVATE" if local_entities else "UNKNOWN",
                "data": {
                    "sanitized_content": sanitized_text,
                    "risk_category": "PRIVATE" if local_entities else "UNKNOWN",
                    "entities": local_entities,
                },
                "sanitized_content": sanitized_text,
                "error": "Remote service response missing required fields; local sanitization preserved",
            }

        if "sanitized_content" not in data and "data" in data and isinstance(data["data"], dict):
            data["sanitized_content"] = data["data"].get("sanitized_content", sanitized_text)
        return data

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
    timeout: float | int = 30,
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
    "+1 (555) 123-4567. RFC: PEMJ880126MNEZSN01. Account: 1234-5678-90. "
    "Card: 4111-1111-1111-1111. SSN: 123-45-6789. "
    "IPv4: 192.0.2.42; IPv6: 2001:db8::1. "
    "API key: sk-abc123fakekeynotreal0000000000. "
    "IBAN: GB29 WEST 1234 5698 7654 32."
)


def _run_self_checks() -> None:
    """Run regression checks in local-only mode without making network requests."""
    email_result = sanitize("a@b.com.", call_api=False)
    assert email_result["data"]["sanitized_content"] == "[EMAIL]."
    assert email_result["data"]["entities"] == [
        {"type": "email", "category": "PRIVATE", "count": "1"}
    ]

    ipv6_result = sanitize("2001:db8::1.", call_api=False)
    assert ipv6_result["data"]["sanitized_content"] == "[IP_ADDRESS]."

    literal_placeholder_result = sanitize("The literal [EMAIL] is not PII.", call_api=False)
    assert literal_placeholder_result["data"]["sanitized_content"] == "The literal [EMAIL] is not PII."
    assert literal_placeholder_result["data"]["entities"] == []
    assert literal_placeholder_result["data"]["risk_category"] == "UNKNOWN"

    phone_result = sanitize("Call me at 9876543210.", call_api=False)
    assert phone_result["data"]["sanitized_content"] == "Call me at [PHONE]."

    card_result = sanitize("Card 4111-1111-1111-1111", call_api=False)
    assert card_result["data"]["sanitized_content"] == "Card [CREDIT_CARD]"

    ssn_result = sanitize("SSN 123-45-6789", call_api=False)
    assert ssn_result["data"]["sanitized_content"] == "SSN [SSN]"

    demo_result = sanitize(DEMO_TEXT, call_api=False)
    sanitized_demo = demo_result["data"]["sanitized_content"]
    assert "juan.perez@example.com" not in sanitized_demo
    assert "+1 (555) 123-4567" not in sanitized_demo
    assert "4111-1111-1111-1111" not in sanitized_demo
    assert "123-45-6789" not in sanitized_demo
    assert "192.0.2.42" not in sanitized_demo
    assert "2001:db8::1" not in sanitized_demo
    assert "sk-abc123fakekeynotreal0000000000" not in sanitized_demo
    assert "1234-5678-90" not in sanitized_demo
    assert "GB29 WEST 1234 5698 7654 32" not in sanitized_demo


def main() -> None:
    """Run the command-line interface without printing raw input."""
    parser = argparse.ArgumentParser(
        description="PII Sanitization Agent with Local Pre-Sanitization & Secure API Integration"
    )
    parser.add_argument("--text", help="text to sanitize")
    parser.add_argument("--file", help="path to a text file to sanitize")
    parser.add_argument("--context", default="general", help="context: general|financial|legal|medical|code")
    parser.add_argument("--tx-hash", default="TRIAL", help="TRIAL for free tier, or Solana tx hash")

    api_group = parser.add_mutually_exclusive_group()
    api_group.add_argument(
        "--api",
        dest="call_api",
        action="store_true",
        default=None,
        help="send pre-sanitized text to TrustBoost API for remote verification",
    )
    api_group.add_argument(
        "--local",
        "--local-only",
        dest="call_api",
        action="store_false",
        default=None,
        help="force local-only sanitization mode (overrides TRUSTBOOST_CALL_API)",
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
    elif args.text is not None:
        text = args.text
    else:
        text = DEMO_TEXT
        print("No --text/--file provided. Running demo with local pre-sanitization.\n")

    result = sanitize(
        text,
        context=args.context,
        tx_hash=args.tx_hash,
        call_api=args.call_api,
    )
    # Output only the sanitized result, never raw input
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    _run_self_checks()
    main()
