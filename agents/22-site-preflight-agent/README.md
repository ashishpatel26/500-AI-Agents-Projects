# Site Preflight Agent

A web agent that asks before it acts. Before it reads or cites a site it gets a **signed decision** from [CrawlCheck](https://crawlcheck.io/for-agents) (allow / warn / require_confirmation / block), **verifies the Ed25519 signature locally**, and keeps every decision receipt in `receipts/` so the run can be audited afterwards. Redirects are never followed blindly: every hop must be HTTPS and public, and gets its own read decision first. No API key, no quota: the decisions are a public service.

**Framework**: none (plain Python, `crawlcheck` SDK)  
**LLM**: GPT-4o-mini (optional; without a key the answer is extractive)  
**Runtime**: about 5 seconds

## What it does

1. **Resolve** the domain: one signed answer about what the site declares (robots.txt policy, machine files, capabilities) and what crawlers were actually served, with a decision per action
2. **Preflight `read`**: a signed decision receipt; the agent fetches the page only on `allow` or `warn`, asks a human on `require_confirmation`, and stops on anything else (fail closed). A redirect to another host gets its own read decision before it is followed; `http://`, non-public and more-than-three-hop redirects are refused
3. **Preflight `cite`**: decides whether the answer may name its source
4. **Answer** the task from the page text (gpt-4o-mini if `OPENAI_API_KEY` is set, otherwise an extractive summary)

Each receipt is verified offline (document hash, key id, signature, published key) before the agent acts on it. The signed receipt is written to `receipts/<host>-<action>-<time>.json` with the verification result beside it as `.verification.json`. Any receipt can be re-checked later: `python -m crawlcheck verify receipts/<file>.json`.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # optional: add OPENAI_API_KEY for an LLM-written answer
```

## Run

```bash
# Default: example.com
python agent.py

# Any URL and task
python agent.py --url https://crawlcheck.io/for-agents --task "what should an agent know before it acts on a site"

# Non-interactive (answers yes to any confirmation prompt)
python agent.py --url https://example.com --yes
```

## Sample Output

```
Task: what does this site say it is for
Site: https://example.com

1. Resolve - what is known about example.com
  status measured - observed 2026-10-14T20:44:03.934Z
  read: warn, cite: warn, connect: warn, transact: block, administer: block

2. Preflight before reading
  [read] warn - no robots.txt policy was read, so permission is unknown
           signature verified - example.com-read-20261014T152340-818753342.json
  fetched 171 characters from https://example.com

3. Preflight before citing
  [cite] warn - no robots.txt policy was read, so permission is unknown; the publisher's identity was not observed, so attribution is unconfirmed
           signature verified - example.com-cite-20261014T152341-189945432.json

4. Answer
  (extractive)
  Example Domain This domain is for use in documentation examples without needing permission.

  Source: https://example.com

Receipts: receipts/ - verify any of them later with: python -m crawlcheck verify <file>
```

## Why

An agent that fetches first and asks never is the failure mode the agentic web keeps producing: scraping past a robots.txt it did not read, citing a page whose publisher it cannot name, following a redirect to a host nobody checked. This agent makes the check a step with evidence: a decision it did not make itself, signed by a third party, verifiable on its own machine, kept.

Decisions: `allow`, `warn`, `require_confirmation`, `block`, `unsupported`. A policy of your own (`max_age_hours`, `on_warn`, `require_entity`, `human_approval`) can only make a decision stricter — see the [SDK](https://pypi.org/project/crawlcheck/) and the [Resolve protocol](https://crawlcheck.io/spec/resolve).
