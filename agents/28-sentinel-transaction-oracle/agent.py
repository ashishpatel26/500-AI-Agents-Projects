"""
SENTINEL — Pre-Execution Transaction Safety Oracle client.

Call SENTINEL before an autonomous agent signs any on-chain transaction.
Returns a SAFE / UNSAFE / UNKNOWN verdict plus a signed receipt (ed25519).

This is a thin client: the oracle logic (contract security scan, call
simulation, signature verification) lives behind the SENTINEL API. The agent
demonstrates the safety-before-signing pattern for autonomous agents.

Usage:
    python agent.py --tx "<json transaction payload>"
    python agent.py --file tx.json
    python agent.py   # runs the built-in demo

Paid per call via x402 (USDC on Base). Uses the free trial when no tx_hash set.
"""

import argparse
import json
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

import requests

API_BASE = os.environ.get("SENTINEL_API_BASE", "https://sentinel-agent.dev")
ENDPOINT = f"{API_BASE}/v1/guard"


def guard(tx_payload: dict, tx_hash: str = "TRIAL") -> dict:
    """Send a transaction to SENTINEL and get a signed safety verdict.

    Args:
        tx_payload: the transaction object to evaluate (chain, to, data, value...)
        tx_hash: "TRIAL" for free tier, or a Base tx hash after x402 payment
    """
    headers = {"Content-Type": "application/json"}
    if tx_hash and tx_hash != "TRIAL":
        headers["X-Payment"] = tx_hash

    body = {"tx": tx_payload, "tx_hash": tx_hash}

    try:
        resp = requests.post(ENDPOINT, json=body, headers=headers, timeout=30)
    except requests.RequestException as e:
        # Fail closed: never sign an uninspected transaction.
        return {
            "verdict": "UNKNOWN",
            "safe_to_sign": False,
            "error": f"oracle unreachable: {e}",
        }

    if resp.status_code == 200:
        return resp.json()

    if resp.status_code == 402:
        return {
            "verdict": "UNKNOWN",
            "safe_to_sign": False,
            "error": "payment required (x402)",
        }

    return {
        "verdict": "UNKNOWN",
        "safe_to_sign": False,
        "http_status": resp.status_code,
    }


DEMO_TX = {
    "chain": "base",
    "to": "0x0000000000000000000000000000000000000000",
    "data": "0x",
    "value": "0",
}


def main():
    ap = argparse.ArgumentParser(description="SENTINEL Transaction Safety Oracle client")
    ap.add_argument("--tx", help="JSON transaction payload")
    ap.add_argument("--file", help="path to a JSON file with the transaction")
    ap.add_argument("--tx-hash", default="TRIAL", help="TRIAL for free tier, or Base tx hash")
    args = ap.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            tx = json.load(f)
    elif args.tx:
        tx = json.loads(args.tx)
    else:
        tx = DEMO_TX
        print("No --tx/--file provided. Running built-in demo.\n")

    print("TX    :", json.dumps(tx)[:120])
    result = guard(tx, tx_hash=args.tx_hash)
    print("\nVERDICT:", result.get("verdict"), "| safe_to_sign:", result.get("safe_to_sign"))
    print(json.dumps(result, indent=2, ensure_ascii=False)[:600])


if __name__ == "__main__":
    main()
