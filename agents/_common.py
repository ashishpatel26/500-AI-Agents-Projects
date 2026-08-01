"""
Common utilities for agents: shared LLM client and HTTP session to improve performance
by reusing connections and avoiding repeated client construction.

Usage:
    from agents._common import get_llm, get_http_session
    llm = get_llm(model="gpt-4o-mini")
    session = get_http_session()
"""

import os
import threading
from typing import Optional

import requests
from langchain_openai import ChatOpenAI


_lock = threading.Lock()
_llm_instances: dict[str, ChatOpenAI] = {}
_http_session: Optional[requests.Session] = None


def get_llm(model: str = "gpt-4o-mini", temperature: float = 0.0) -> ChatOpenAI:
    """Return a cached ChatOpenAI instance for the (model, temperature) key.

    This avoids re-creating the client for every call which can add latency
    and prevent connection/session reuse inside the underlying transport.
    """
    key = f"{model}::${temperature}"
    global _llm_instances
    if key in _llm_instances:
        return _llm_instances[key]

    with _lock:
        # Double-checked locking
        if key in _llm_instances:
            return _llm_instances[key]
        # Construct the ChatOpenAI client once and cache it
        llm = ChatOpenAI(model=model, temperature=temperature)
        _llm_instances[key] = llm
        return llm


def get_http_session() -> requests.Session:
    """Return a singleton requests.Session with optional authorization header from env.

    Reusing a Session allows connection pooling and lower latency for many HTTP calls.
    """
    global _http_session
    if _http_session is not None:
        return _http_session

    with _lock:
        if _http_session is not None:
            return _http_session
        s = requests.Session()
        # Example: propagate GITHUB_TOKEN if available for API calls
        token = os.getenv("GITHUB_TOKEN")
        if token:
            s.headers.update({"Authorization": f"token {token}"})
        s.headers.update({"Accept": "application/json"})
        _http_session = s
        return _http_session
