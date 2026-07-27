"""
VeraData — Verified Latin American Data client.

Fetches verified LATAM data via the VeraData API: sanctions screening (OFAC
SDN + SARLAFT + CNBV + COAF + UAF), entity enrichment (RUES/CNPJ/RFC), and
real-time central bank rates (CO/MX/BR/CL/PE, including Argentina dólar blue).

This is a thin client: the data sources, fuzzy matching, and EU AI Act audit
trail live behind the VeraData API. The agent demonstrates the pattern of
pulling verified LATAM data inside an autonomous pipeline.

Usage:
    python agent.py --endpoint rates --params '{"country":"CO"}'
    python agent.py --endpoint sanctions --params '{"name":"Example Corp"}'
    python agent.py   # runs the built-in demo

Paid per call via x402 (USDC on Base/Solana). Free trial when no tx_hash set.
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

API_BASE = os.environ.get("VERADATA_API_BASE", "https://api.veradata.dev")


def call(endpoint: str, params: dict, tx_hash: str = "TRIAL") -> dict:
    """Call a VeraData endpoint and return structured data.

    Args:
        endpoint: rates | sanctions | entity | context
        params: query parameters for the endpoint
        tx_hash: "TRIAL" for free tier, or a tx hash after x402 payment
    """
    url = f"{API_BASE}/{endpoint.lstrip('/')}"
    headers = {"Content-Type": "application/json"}
    if tx_hash and tx_hash != "TRIAL":
        headers["X-Payment"] = tx_hash

    try:
        resp = requests.post(url, json=params, headers=headers, timeout=30)
    except requests.RequestException as e:
        return {"status": "error", "error": f"service unreachable: {e}"}

    if resp.status_code == 200:
        return resp.json()

    if resp.status_code == 402:
        return {"status": "payment_required", "detail": "x402 payment required"}

    return {"status": "error", "http_status": resp.status_code}


DEMO = {"endpoint": "rates", "params": {"country": "CO"}}


def main():
    ap = argparse.ArgumentParser(description="VeraData LATAM data client")
    ap.add_argument("--endpoint", default="rates", help="rates|sanctions|entity|context")
    ap.add_argument("--params", default="{}", help="JSON params for the endpoint")
    ap.add_argument("--tx-hash", default="TRIAL", help="TRIAL for free tier, or tx hash")
    args = ap.parse_args()

    params = json.loads(args.params)
    if args.endpoint == "rates" and not params:
        params = {"country": "CO"}

    print(f"CALL  : POST /{args.endpoint} {params}")
    result = call(args.endpoint, params, tx_hash=args.tx_hash)
    print("\nRESULT:")
    print(json.dumps(result, indent=2, ensure_ascii=False)[:600])


if __name__ == "__main__":
    main()
