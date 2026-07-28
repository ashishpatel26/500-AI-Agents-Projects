# PII Sanitization Agent

Removes sensitive data from text **before** it reaches an LLM or external API.
Built for autonomous agent pipelines where human review is not possible.

The agent calls the [TrustBoost](https://api.trustboost.dev) API, which detects
and redacts PII (emails, phones, national IDs, bank accounts, API keys) and
returns a structured, auditable result. This is a thin client: the detection
models, multilingual support, and on-chain proof of sanitization live behind the
API, so no PII-handling code or weights live in this repo.

## Why it matters

PII leaking through autonomous pipelines is a real gap — an agent that forwards
user text to an LLM can accidentally expose emails, phones, tax IDs, or secrets.
This agent is the guardrail: sanitize first, then send.

- Semantic PII detection (well above regex-only accuracy)
- Multilingual: EN, ES-LATAM, PT-BR, DE, JA
- LATAM identifiers: RFC, CPF, CUIT, RUT
- Fail-closed: on any API/transport error it returns `[REDACTED]`, never raw PII
- Audit trail: no raw PII is stored by the agent; optional on-chain proof available

## Quick start

```bash
pip install -r requirements.txt
python agent.py --text "Call me at 555-123-4567, email a@b.com, RFC PEMJ880126MNEZSN01"
```

With no API key it uses the **free trial** (50 sanitizations, `tx_hash=TRIAL`).
For higher volume, pay once via x402 and pass the Solana tx hash:

```bash
export TRUSTBOOST_WALLET="<your-agent-wallet>"
python agent.py --text "..." --tx-hash "<solana_tx_hash>"
```

Sanitize a file:

```bash
python agent.py --file input.txt --context legal
```

Context modes: `general | financial | legal | medical | code`.

## Sample output

```json
{
  "status": "success",
  "data": {
    "sanitized_content": "Hi, I'm [REDACTED]. My email is [REDACTED] and my phone is [REDACTED]. RFC: [REDACTED]. Account [REDACTED]. API key [REDACTED].",
    "safety_score": 0.6,
    "risk_category": "PRIVATE",
    "entities": [
      {"type": "email", "category": "PRIVATE"},
      {"type": "phone", "category": "PRIVATE"},
      {"type": "national_id", "category": "PRIVATE"}
    ]
  }
}
```

(Runtime: ~2–5 s per call depending on network. End-to-end demo under 10 min.)

## Ethical considerations

- Raw input is never stored by this agent. Sanitized output may be retained by the
  API provider for 90 days for audit; see the TrustBoost privacy docs.
- Fails closed on API error — it will not emit raw PII if the service is unreachable.
- Human oversight is recommended for high-risk deployments (healthcare, finance, legal).
- The included `sk-abc123fakekeynotreal0000000000` in sample text is a **fake** fixture,
  exactly what the redactor should catch.

## Compliance context

EU AI Act, GDPR, HIPAA, LGPD. Use this agent wherever agent-to-agent or
agent-to-LLM text carries user data.

## License

MIT (repository root). The TrustBoost API is a separate service; see its terms.
