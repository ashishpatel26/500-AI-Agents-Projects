# VeraData — Verified Latin American Data Agent

Fetches **verified Latin American data** via the [VeraData](https://api.veradata.dev)
API, designed for autonomous AI agents that need trustworthy LATAM data without
human lookup.

This agent is a thin client. The data sources (central banks, sanctions lists,
company registries), fuzzy matching, and EU AI Act audit trail live behind the
VeraData API — no data pipeline code ships in this repo.

## What it covers

- **Sanctions screening** — OFAC SDN + SARLAFT (CO) + CNBV (MX) + COAF (BR) + UAF (CL)
- **Entity enrichment** — RUES (CO), CNPJ (BR), RFC (MX), CMF (CL), SUNAT (PE)
- **Central bank rates** — CO/MX/BR/CL/PE, including Argentina *dólar blue*
- **EU AI Act Art. 12/13** compliant hash-chain audit trail

## Why it matters

Autonomous agents operating in LATAM need verified data (is this counterparty
sanctioned? what's the real FX rate?) without a human in the loop. VeraData
returns structured, auditable data via x402 micropayments.

## Quick start

```bash
pip install -r requirements.txt
python agent.py --endpoint rates --params '{"country":"CO"}'
python agent.py --endpoint sanctions --params '{"name":"Example Corp"}'
```

Uses the free trial (`tx_hash=TRIAL`) with no payment. For volume, pay via x402
(USDC on Base/Solana) and pass the tx hash.

## Sample output

```json
{
  "status": "success",
  "data": {
    "country": "CO",
    "signal": "TRM",
    "value": 4123.45,
    "fetched_at": "2026-07-25T..."
  }
}
```

(Runtime: ~2–5 s per call. End-to-end demo under 10 min.)

## Ethical considerations

- Data is sourced from public/regulatory sources; see VeraData terms for
  provenance and licensing.
- The audit trail (hash-chain) is for compliance — retain it for EU AI Act / GDPR.
- Fail-closed: if the service is unreachable the agent gets an error, never
  silently fabricated data.

## Compliance context

EU AI Act, GDPR, LGPD. Use wherever an agent needs verified LATAM data.

## License

MIT (repository root). The VeraData API is a separate service; see its terms.
