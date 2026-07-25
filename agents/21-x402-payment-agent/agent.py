# x402 Payment Agent — Pay-per-call AI agent with market data & DeFi intelligence
#
# This agent demonstrates the x402 micropayment pattern: agents pay per API call
# using USDC on Base or Solana — no API keys, no subscriptions, no sign-up.
#
# Flow:
#   1. Agent receives a natural language request (e.g. "What's the price of ETH?")
#   2. Agent discovers the right x402-protected API endpoint
#   3. Agent calls the endpoint — receives HTTP 402 Payment Required
#   4. Agent settles the payment via x402 (USDC transfer in the HTTP response)
#   5. Agent retries the request with the payment proof → gets the data
#   6. Agent returns the result to the user
#
# Requires: pip install requests

import os
import json
import hashlib
import base64
from urllib.parse import urljoin
from typing import Optional, Dict

import requests


# ─── x402 Client Library (simplified — real impl in gentech-kit) ───

X402_ACCEPTS = {
    "USDC on Base": {
        "chain_id": 8453,
        "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",  # USDC on Base
        "decimals": 6,
    }
}


def discover_x402_endpoint(base_url: str) -> Optional[dict]:
    """Discover available x402 services by probing well-known paths."""
    well_known = ["/openapi.json", "/v1/", "/.well-known/x402"]
    for path in well_known:
        try:
            r = requests.get(urljoin(base_url, path), timeout=5)
            if r.status_code == 200:
                try:
                    spec = r.json()
                    paths = spec.get("paths", spec)
                    endpoints = {}
                    for p, methods in paths.items():
                        for method, details in (methods or {}).items():
                            if isinstance(details, dict) and details.get("x-payment-info"):
                                endpoints[p] = {
                                    "method": method.upper(),
                                    "payment": details["x-payment-info"],
                                }
                    return endpoints
                except (json.JSONDecodeError, AttributeError):
                    continue
        except requests.RequestException:
            continue
    return None


def parse_402(payment_required_header: str) -> Optional[Dict]:
    """Parse the x402 v2 Payment Required header into a settlement object."""
    try:
        decoded = base64.b64decode(payment_required_header).decode()
        return json.loads(decoded)
    except (json.JSONDecodeError, UnicodeDecodeError, Exception):
        return None


def settle_x402(payment_info: dict, sender_key: str) -> Optional[str]:
    """
    Settle an x402 payment challenge.
    In production this signs an EIP-3009 transfer via the agent's wallet.
    Returns a payment proof string.
    """
    # Simplified for demonstration — real implementation uses EIP-3009 / EIP-7702
    amount = int(payment_info.get("amount", "0"))
    pay_to = payment_info.get("pay_to", "")
    nonce = payment_info.get("nonce", "")

    # Create a deterministic payment proof (in production: on-chain tx hash)
    proof_input = f"{sender_key}:{pay_to}:{amount}:{nonce}".encode()
    proof = hashlib.sha256(proof_input).hexdigest()[:64]

    return proof


def call_x402_api(
    endpoint: str, method: str = "GET", params: dict = None, sender_key: str = "agent-wallet-0x..."
) -> Optional[dict]:
    """Call an x402-protected API — handles 402 → settle → retry automatically."""
    headers = {"Accept": "application/json"}

    # First call — expect 402 Payment Required
    if method == "GET":
        r = requests.get(endpoint, headers=headers, params=params, timeout=10)
    else:
        r = requests.post(endpoint, headers=headers, json=params, timeout=10)

    if r.status_code == 200:
        return r.json()

    if r.status_code == 402:
        # Extract payment challenge from response headers
        ph = r.headers.get("payment-required") or r.headers.get("x-payment-required")
        if not ph:
            print("  ⚠️  402 but no payment-required header")
            return None

        payment_info = parse_402(ph)
        if not payment_info:
            print("  ⚠️  Could not parse payment-required header")
            return None

        price = payment_info.get("price", {})
        print(f"  💰 Settling ${price.get('amount', '?')} USDC on Base...")

        # Settle the payment
        proof = settle_x402(payment_info, sender_key)
        if not proof:
            print("  ⚠️  Settlement failed")
            return None

        # Retry with payment proof
        auth_header = base64.b64encode(json.dumps({
            "payment_proof": proof,
            "nonce": payment_info.get("nonce"),
        }).encode()).decode()

        headers["X-402-Proof"] = auth_header
        if method == "GET":
            r2 = requests.get(endpoint, headers=headers, params=params, timeout=10)
        else:
            r2 = requests.post(endpoint, headers=headers, json=params, timeout=10)

        if r2.status_code == 200:
            return r2.json()
        else:
            print(f"  ⚠️  Payment retry failed: HTTP {r2.status_code}")
            return None

    print(f"  ⚠️  API error: HTTP {r.status_code}")
    return None


# ─── GenTech API endpoints (x402-protected) ───

GENTECH_API = "https://api.gentechlabs.net"


def get_market_data(token: str) -> Optional[dict]:
    """Get real-time market data for a token via x402."""
    print(f"\n  🔍 Fetching market data for {token}...")
    return call_x402_api(
        f"{GENTECH_API}/v1/games/search",
        params={"q": token},
    )


def get_wallet_insights(address: str) -> Optional[dict]:
    """Analyze a wallet's holdings and risk via x402."""
    print(f"\n  🔍 Analyzing wallet {address[:8]}...{address[-6:]}...")
    return call_x402_api(
        f"{GENTECH_API}/v1/wallet/analyze",
        method="POST",
        params={"address": address},
    )


def get_token_intel(symbol: str) -> Optional[dict]:
    """Get token security intel and market data via x402."""
    print(f"\n  🔍 Scanning token intel for {symbol}...")
    return call_x402_api(
        f"{GENTECH_API}/v1/intel/search",
        params={"symbol": symbol},
    )


def check_airdrops(address: str) -> Optional[dict]:
    """Check unclaimed airdrops for a wallet via x402."""
    print(f"\n  🔍 Checking airdrops for {address[:8]}...{address[-6:]}...")
    return call_x402_api(
        f"{GENTECH_API}/v1/airdrops/check",
        method="POST",
        params={"address": address},
    )


# ─── Agent Logic ───

SERVICES = {
    "price": {"func": get_market_data, "desc": "Get token price and market data"},
    "wallet": {"func": get_wallet_insights, "desc": "Analyze wallet holdings and risk"},
    "token": {"func": get_token_intel, "desc": "Token security intel and market data"},
    "airdrop": {"func": check_airdrops, "desc": "Check unclaimed airdrops"},
}


def route_request(query: str) -> tuple:
    """Route a natural language request to the right x402 service."""
    q = query.lower()
    if "price" in q or "market data" in q or "price of" in q or "value of" in q:
        return "price", ["ETH", "BTC", "SOL", "DOGE", query.split()[-1]]
    elif "wallet" in q or "analyze" in q or "portfolio" in q:
        return "wallet", [extract_address(query) or "0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18"]
    elif "token" in q or "intel" in q or "safe" in q or "scam" in q:
        return "token", [query.split()[-1].upper()]
    elif "airdrop" in q or "claim" in q:
        return "airdrop", [extract_address(query) or "0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18"]
    else:
        return "price", ["ETH"]


def extract_address(text: str) -> Optional[str]:
    """Extract an Ethereum-style address from text."""
    import re
    match = re.search(r"0x[a-fA-F0-9]{40}", text)
    return match.group(0) if match else None


def main():
    print("═" * 56)
    print("  🤖 GenTech x402 Payment Agent")
    print("  Pay-per-call AI agent with USDC micropayments")
    print("═" * 56)

    # Example queries to demonstrate the agent
    queries = [
        "What's the price of ETH?",
        "Analyze wallet 0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18",
        "Is SOL safe to trade?",
        "Check airdrops for my wallet",
    ]

    for query in queries:
        print(f"\n{'─' * 56}")
        print(f"  📝 User: \"{query}\"")
        print(f"{'─' * 56}")

        service, args = route_request(query)
        handler = SERVICES[service]["func"]

        result = handler(*args)

        if result:
            print(f"\n  ✅ Result received via x402 payment")
            preview = json.dumps(result, indent=2)[:400]
            print(f"  {preview}")
        else:
            print(f"\n  ❌ Could not fetch result (requires funded x402 wallet)")

    print(f"\n{'═' * 56}")
    print("  💡 No API keys needed — every call settled in USDC on Base")
    print("  Install the full agent kit: pip install git+https://github.com/ProtoJay4789/genTech-agent-kit.git")
    print("═" * 56)


if __name__ == "__main__":
    main()
