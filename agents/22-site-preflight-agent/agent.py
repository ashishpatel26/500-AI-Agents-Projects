"""Site preflight agent.

A web agent that asks before it acts. Before it reads or cites a host it gets a
signed decision from CrawlCheck (https://crawlcheck.io), checks the Ed25519
signature locally, and only then fetches, summarises or cites. Every decision
receipt is kept in receipts/ so the run can be audited afterwards. Redirects are
never followed blindly: each hop is HTTPS-only, never a private address, and gets
its own read decision before it is fetched.

No API key is needed for the decisions. OPENAI_API_KEY is optional: with it the
summary is written by gpt-4o-mini; without it the agent prints an extractive one.

    python agent.py --url https://example.com --task "what does this site say it is for"
"""
import argparse
import html
import ipaddress
import json
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from crawlcheck import CrawlCheck

AGENT_NAME = "site-preflight-agent"
RECEIPTS = Path(__file__).parent / "receipts"
MAX_HOPS = 3
PROCEED = {"allow", "warn"}  # every other decision fails closed


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Redirects are returned to the caller, never followed by urllib."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


OPENER = urllib.request.build_opener(_NoRedirect)


def load_env():
    p = Path(__file__).parent / ".env"
    if p.exists():
        for line in p.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def host_of(url):
    """The exact hostname of an https URL, or None when the URL is not one we fetch."""
    u = urllib.parse.urlparse(url)
    if u.scheme != "https" or not u.hostname:
        return None
    return u.hostname.lower()


def is_private_host(host):
    """True for loopback, link-local, private or otherwise non-public addresses."""
    try:
        infos = socket.getaddrinfo(host, 443, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return True
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if not ip.is_global:
            return True
    return False


def preflight(cc, domain, action, confirm):
    """One signed decision, verified locally, written to receipts/."""
    receipt = cc.preflight(domain, action=action, agent=AGENT_NAME)
    check = cc.verify(receipt)
    RECEIPTS.mkdir(exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%S") + f"-{time.time_ns() % 1_000_000_000:09d}"
    out = RECEIPTS / f"{domain}-{action}-{stamp}.json"
    out.write_text(json.dumps(receipt, indent=2))  # the signed document itself: `python -m crawlcheck verify <file>` reads it
    out.with_suffix(".verification.json").write_text(json.dumps(check, indent=2))
    decision = str(receipt.get("decision", ""))
    why = "; ".join(s["why"] for s in receipt.get("steps", [])) or "no reason given"
    print(f"  [{action}] {decision or 'missing'} - {why}")
    print(f"           signature {'verified' if check['accepted'] else 'NOT accepted'} - {out.name}")
    if not check["accepted"]:
        return False
    if decision == "require_confirmation":
        return confirm(f"{domain}: {action} needs a human yes ({why}). Continue?")
    return decision in PROCEED


def fetch_text(url, cc, confirm):
    """Fetch over HTTPS, one checked hop at a time. Returns (text, final_url) or (None, reason)."""
    headers = {"user-agent": f"{AGENT_NAME}/1.0 (+https://crawlcheck.io/for-agents)"}
    seen = {host_of(url)}
    for _ in range(MAX_HOPS + 1):
        host = host_of(url)
        if not host:
            return None, f"refused: {url} is not an https URL"
        if is_private_host(host):
            return None, f"refused: {host} is not a public address"
        try:
            with OPENER.open(urllib.request.Request(url, headers=headers), timeout=20) as r:
                raw = r.read(400_000).decode("utf-8", "ignore")
        except urllib.error.HTTPError as e:
            if e.code not in (301, 302, 303, 307, 308):
                return None, f"refused: {host} answered {e.code}"
            nxt = urllib.parse.urljoin(url, e.headers.get("location", ""))
            nhost = host_of(nxt)
            if not nhost:
                return None, f"refused: redirect to a non-https URL"
            if nhost not in seen:
                print(f"  redirect to {nhost} - asking before following")
                if not preflight(cc, nhost, "read", confirm):
                    return None, f"refused: reading {nhost} was not allowed"
                seen.add(nhost)
            url = nxt
            continue
        raw = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
        text = re.sub(r"<[^>]+>", " ", raw)
        return re.sub(r"\s+", " ", html.unescape(text)).strip(), url
    return None, f"refused: more than {MAX_HOPS} redirects"


def summarise(task, text, url):
    key = os.environ.get("OPENAI_API_KEY")
    if key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=key)
            model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
            r = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Answer the task from the page text only. Three sentences. Say if the page does not answer it."},
                    {"role": "user", "content": f"Task: {task}\nPage: {url}\n\n{text[:12000]}"},
                ],
                temperature=0,
            )
            return r.choices[0].message.content.strip(), model
        except Exception as e:  # fall through to the extractive summary
            print(f"  (LLM unavailable: {e.__class__.__name__}; using an extractive summary)")
    words = set(re.findall(r"[a-z]{4,}", task.lower()))
    sentences = re.split(r"(?<=[.!?])\s+", text)
    scored = sorted(sentences, key=lambda s: -len(words & set(re.findall(r"[a-z]{4,}", s.lower()))))
    return " ".join(scored[:3])[:800] or text[:600], "extractive"


def main():
    load_env()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--url", default="https://example.com")
    ap.add_argument("--task", default="what does this site say it is for")
    ap.add_argument("--yes", action="store_true", help="answer yes to any confirmation prompt (CI)")
    a = ap.parse_args()
    domain = host_of(a.url)
    if not domain:
        sys.exit("an https URL is needed, e.g. https://example.com")
    if is_private_host(domain):
        sys.exit(f"{domain} is not a public address; nothing was asked or fetched")
    confirm = (lambda q: True) if a.yes else (lambda q: input(q + " [y/N] ").strip().lower() == "y")
    cc = CrawlCheck()

    print(f"\nTask: {a.task}\nSite: {a.url}\n\n1. Resolve - what is known about {domain}")
    answer = cc.resolve(domain)
    acts = answer.get("actions", {})
    print(f"  status {answer.get('status')} - observed {answer.get('freshness', {}).get('observed_at')}")
    print("  " + ", ".join(f"{k}: {v.get('decision')}" for k, v in acts.items() if isinstance(v, dict)))

    print("\n2. Preflight before reading")
    if not preflight(cc, domain, "read", confirm):
        print("\nStopped: reading this site was not allowed. Nothing was fetched.")
        return
    text, final_url = fetch_text(a.url, cc, confirm)
    if text is None:
        print(f"\nStopped: {final_url}. Nothing was summarised.")
        return
    print(f"  fetched {len(text):,} characters from {final_url}")
    domain = host_of(final_url)

    print("\n3. Preflight before citing")
    may_cite = preflight(cc, domain, "cite", confirm)

    print("\n4. Answer")
    summary, by = summarise(a.task, text, final_url)
    print(f"  ({by})\n  {summary}")
    print(f"\n  Source: {final_url}" if may_cite else "\n  (not cited: the cite decision did not allow it)")
    print(f"\nReceipts: {RECEIPTS}/ - verify any of them later with: python -m crawlcheck verify <file>")


if __name__ == "__main__":
    main()
