# x402 Payment Agent

An AI agent that uses **x402 micropayments** to access pay-per-call API services for market data, DeFi intelligence, wallet analytics, and token security — no API keys, no subscriptions, no sign-up.

**Framework**: LangChain-style
**LLM**: GPT-4o (or any LLM — the agent pattern is framework-agnostic)
**Payment Rail**: x402 v2 — HTTP 402 Payment Required → USDC settlement on Base

## What it does

1. Receives a natural language request (e.g. "What's the price of ETH?")
2. Routes to the appropriate x402-protected API endpoint
3. Calls the endpoint — receives **HTTP 402 Payment Required**
4. Settles the payment via x402 (USDC transfer — typically ~$0.01–0.05 per call)
5. Retries with payment proof → gets the data
6. Returns the result to the user

## Services

| Service | Endpoint | Cost |
|---------|----------|------|
| Market Data | `/v1/games/search` | ~$0.01 |
| Wallet Analytics | `/v1/wallet/analyze` | ~$0.02 |
| Token Intel | `/v1/intel/search` | ~$0.01 |
| Airdrop Check | `/v1/airdrops/check` | ~$0.02 |

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your x402 wallet private key (optional — demo mode works without it)
```

## Run

```bash
python agent.py
```

The agent will demonstrate 4 example queries with the x402 settlement flow.

## Sample Output

```
════════════════════════════════════════════════════════
  🤖 GenTech x402 Payment Agent
  Pay-per-call AI agent with USDC micropayments
════════════════════════════════════════════════════════

────────────────────────────────────────────────────────
  📝 User: "What's the price of ETH?"
────────────────────────────────────────────────────────

  🔍 Fetching market data for ETH...

  💰 Settling $0.01 USDC on Base...

  ✅ Result received via x402 payment
  {
    "token": "ETH",
    "price_usd": 2847.32,
    "24h_change": 2.13,
    ...
  }
```

## Architecture

```
User Request
    │
    ▼
Route Query → Determine service + params
    │
    ▼
Call x402 API → HTTP 402 (Payment Required)
    │
    ▼
Parse payment-required header
    │
    ▼
Settle via x402 → EIP-3009 USDC transfer on Base
    │
    ▼
Retry with proof → HTTP 200 + Data
    │
    ▼
Return to User
```

## How x402 Works

x402 is an HTTP payment protocol:

1. **Agent** sends a normal HTTP request to a paid API
2. **Gateway** responds with `402 Payment Required` + a base64-encoded payment challenge
3. **Agent** settles by sending USDC on Base (or Solana) — no gas fees, no API key
4. **Gateway** returns the data

This is **agent-to-agent commerce** — the agent pays, the API responds, no human in the loop.

## Full Agent Kit

```bash
pip install git+https://github.com/ProtoJay4789/genTech-agent-kit.git
gentech-kit --help
```

## Resources

- [GenTech Agent Kit](https://github.com/ProtoJay4789/genTech-agent-kit)
- [x402scan — x402 Ecosystem Explorer](https://x402scan.com)
- [GenTech API Docs](https://docs.gentechlabs.net)
