# PII Sanitization Agent

Redacts Personally Identifiable Information (PII) **locally and offline** before text reaches an LLM or external third-party API.

When integrated with external services like the TrustBoost API (`https://api.trustboost.dev`), this agent enforces a strict **local pre-sanitization gate**: all sensitive entities are detected and redacted in-process *before* constructing the HTTP request. Raw PII is never transmitted over the network.

---

## Security & Architecture Model

```
                    ┌──────────────────────────────────────────────┐
                    │               User Raw Input                 │
                    └──────────────────────┬───────────────────────┘
                                           │
                                           ▼
                    ┌──────────────────────────────────────────────┐
                    │      1. Local Detection & Sanitization       │
                    │   - RegEx patterns with strict boundaries    │
                    │   - Luhn checksum for payment cards          │
                    │   - MOD-97 checksum for formatted IBANs      │
                    │   - ipaddress library for IPv4 / IPv6        │
                    │   - Standard library only / zero network     │
                    └──────────────────────┬───────────────────────┘
                                           │
                                           ▼
                             [ Locally Sanitized Content ]
                                           │
               ┌───────────────────────────┴───────────────────────────┐
               ▼                                                       ▼
      [ Local Mode (Default) ]                             [ Remote API Mode (--api) ]
      Returns structured result                            Dispatches PRE-SANITIZED text to
      immediately; zero network                            https://api.trustboost.dev
      I/O and fail-safe.                                   (Raw PII is NEVER transmitted!)
```

### Key Security Guarantees

1. **Local-First Pre-Sanitization**: Sensitive values are replaced with stable placeholders (`[EMAIL]`, `[PHONE]`, etc.) locally inside the host process before any network socket is opened.
2. **Metadata Sanitization & Leakage Prevention**: Outbound metadata fields (`context`, `tx_hash`, `wallet_address`) are validated against strict contracts and screened so sensitive information is never leaked via metadata.
3. **Data Minimization**: The third-party API request body carries only the pre-sanitized text. Outgoing network payloads never contain raw sensitive data.
4. **Safe Error Handling & Fallback**: If the third-party service is unreachable, times out, or returns HTTP 402/500/malformed JSON, the agent fails closed / falls back safely to the locally sanitized result. Raw user inputs are never exposed in error messages, stack traces, or logs.
5. **Idempotency & Retry Safety**: The TrustBoost API does not document or support server-side idempotency keys. To prevent duplicate charges or billing operations against the wallet, automatic blind retries are avoided.
6. **No Raw Input Echoing**: The command-line interface prints only the sanitized output, preventing sensitive data from leaking into terminal scrollback or CI logs.

---

## Supported PII Categories

| Category | Description | Placeholder |
| :--- | :--- | :--- |
| **Email Addresses** | RFC 5322 standard email formats | `[EMAIL]` |
| **Phone Numbers** | International (`+1`, `+44`, `+91`), dashed, parenthesized, or unseparated (10–15 digits) | `[PHONE]` |
| **Payment Cards** | Visa, MasterCard, Amex (13–19 digits) verified with Luhn checksum | `[CREDIT_CARD]` |
| **US SSN** | US Social Security Numbers (`###-##-####`) | `[SSN]` |
| **Government / Tax IDs** | Case-insensitive national identification numbers (e.g., Mexican CURP 18-char, RFC 12–13 char) | `[GOV_ID]` |
| **IP Addresses** | Valid IPv4 and IPv6 addresses validated via `ipaddress` | `[IP_ADDRESS]` |
| **Bank Accounts** | Labeled account numbers (`Account: ...`, `Acc No: ...`, `Cuenta: ...`) with spaces/hyphens | `[BANK_ACCOUNT]` |
| **Formatted IBANs** | Formatted IBANs with spaces or hyphens, case-insensitive, verified via MOD-97 checksum | `[BANK_ACCOUNT]` |
| **API Keys & Secrets** | OpenAI (`sk-proj-...`, `sk-svcacct-...`, `sk-...`), GitHub (`github_pat_...`, `ghp_...`), AWS (`AKIA...`) | `[API_KEY]` |

---

## Quick Start

### Installation

```bash
cd agents/21-pii-sanitization-agent
pip install -r requirements.txt
```

### Command-Line Usage

```bash
# 1. Sanitize text passed directly via CLI (local offline mode)
python agent.py --text "Contact me at +1 (555) 123-4567 or email juan.perez@example.com"

# 2. Sanitize explicitly empty string (safely returns empty output)
python agent.py --text ""

# 3. Sanitize an input file
python agent.py --file input.txt

# 4. Run built-in demo covering all supported PII categories
python agent.py

# 5. Run with TrustBoost API remote verification (pre-sanitizes locally before sending)
python agent.py --text "My email is alice@example.com" --api

# 6. Force local-only mode (overrides TRUSTBOOST_CALL_API=true in environment)
python agent.py --text "My email is alice@example.com" --local

# 7. Run built-in regression self-checks (zero network I/O)
python agent.py --self-test
```

Sample CLI output:
```json
{
  "status": "success",
  "data": {
    "sanitized_content": "Contact me at [PHONE] or email [EMAIL]",
    "risk_category": "PRIVATE",
    "entities": [
      {
        "type": "email",
        "category": "PRIVATE",
        "count": "1"
      },
      {
        "type": "phone",
        "category": "PRIVATE",
        "count": "1"
      }
    ]
  },
  "sanitized_content": "Contact me at [PHONE] or email [EMAIL]",
  "risk_category": "PRIVATE"
}
```

---

## Python Usage

```python
from agent import sanitize, sanitize_text, sanitize_locally

# 1. Direct text sanitization
clean = sanitize_text("My email is akif@example.com and phone is 9876543210.")
print(clean)
# "My email is [EMAIL] and phone is [PHONE]."

# 2. Structured local sanitization (no network I/O)
result = sanitize("Card 4111-1111-1111-1111; SSN 123-45-6789")
print(result["data"]["sanitized_content"])
# "Card [CREDIT_CARD]; SSN [SSN]"
print(result["data"]["entities"])
# [{'type': 'credit_card', 'category': 'PRIVATE', 'count': '1'}, {'type': 'ssn', 'category': 'PRIVATE', 'count': '1'}]

# 3. Third-party API verification (with local pre-sanitization)
api_result = sanitize("Email user@example.com", call_api=True)
```

`sanitize(text, context="general", tx_hash="TRIAL", call_api=None, timeout=30)` maintains full backward compatibility with previous call signatures.

---

## Environment Variables

Copy `.env.example` to `.env` to configure optional remote integration:

```bash
# Target TrustBoost API endpoint
TRUSTBOOST_API_BASE=https://api.trustboost.dev

# Wallet identifier for on-chain proof / audit logging
TRUSTBOOST_WALLET=demo-agent

# Set to true to automatically call TrustBoost API after local sanitization
TRUSTBOOST_CALL_API=false
```

---

## Testing

Run the automated test suite covering all 11 Sourcery findings, edge cases, error handling, and third-party API request security:

```bash
python test_agent.py -v
```

---

## Known Limitations

- **Pattern & Checksum Limits**: While regex and checksum validation accurately identify structured PII (emails, cards, IPs, SSNs, phone numbers, API keys, IBANs), unstructured or context-dependent identifiers (e.g., individual person names, physical street addresses, company names) require specialized Named Entity Recognition (NER) models.
- **Remote Idempotency**: The TrustBoost API does not document or support server-side idempotency keys. Network timeouts are caught safely, but automated blind retries are not performed to protect against duplicate billing.
- **International Identifier Formats**: Regional tax and national identity formats vary by jurisdiction. Organizations with specialized identification formats should register additional custom regex patterns.
- **High-Risk Environments**: Critical compliance pipelines (HIPAA, GDPR, PCI-DSS) should combine automated pre-sanitization with human-in-the-loop review.

---

## License

MIT (repository root).
