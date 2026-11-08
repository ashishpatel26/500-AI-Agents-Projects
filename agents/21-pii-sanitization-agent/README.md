# PII Sanitization Agent

Redacts common PII from text **locally and offline** before it reaches an LLM
or another external service. It uses only Python's standard library and makes
no network requests.

## Redacted data

- Email addresses → `[EMAIL]`
- Phone numbers, including international, dashed, and parenthesized formats → `[PHONE]`
- Credit and debit card numbers with 13–19 digits and optional spaces/hyphens → `[CREDIT_CARD]`
- US Social Security numbers → `[SSN]`
- Valid IPv4 and IPv6 addresses → `[IP_ADDRESS]`

## Quick start

No dependencies or API credentials are required.

```bash
python agent.py --text "Call me at +1 (555) 123-4567 or email a@b.com"
python agent.py --file input.txt
python agent.py
```

The final command runs the built-in offline example covering every supported
PII category. The CLI prints only the sanitized result, not the raw input.

## Python usage

```python
from agent import sanitize, sanitize_text

sanitize_text("Email a@b.com; SSN 123-45-6789")
# "Email [EMAIL]; SSN [SSN]"

result = sanitize("Card 4111-1111-1111-1111")
# result["data"]["sanitized_content"] == "Card [CREDIT_CARD]"
```

`sanitize(text, context="general", tx_hash="TRIAL")` retains its existing
signature for compatibility. The optional `context` and `tx_hash` arguments
are accepted but unused; sanitization is entirely local.

## Notes

Regex-based redaction is a useful guardrail, but it cannot identify every kind
of personal or sensitive data. Add application-specific patterns and human
review where high-risk data is involved.

## License

MIT (repository root).
