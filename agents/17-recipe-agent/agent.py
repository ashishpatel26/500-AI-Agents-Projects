import re
import json
from typing import Any, Optional


def _strip_code_fence(s: str) -> str:
    """Remove surrounding triple-backtick fence if present (``` or ```json)."""
    s = s.strip()
    if s.startswith("```") and s.endswith("```"):
        # Allow optional language label after opening fence
        s = re.sub(r"(?s)^```(?:\w+)?\s*", "", s)
        s = re.sub(r"(?s)\s*```\s*$", "", s)
    return s


def _extract_json_at(s: str, start_idx: int, max_chars: int = 1_000_000) -> Optional[str]:
    """
    Extract a JSON substring starting at start_idx. Handles strings and escapes.
    Returns the substring or None if not found / incomplete.
    """
    if start_idx >= len(s):
        return None
    opener = s[start_idx]
    if opener not in "{[":
        return None
    closer = "}" if opener == "{" else "]"
    depth = 0
    in_string = False
    escape = False
    out_chars = []
    end = min(len(s), start_idx + max_chars)
    for i in range(start_idx, end):
        ch = s[i]
        out_chars.append(ch)
        if escape:
            escape = False
            continue
        if ch == "\\" and in_string:
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == opener:
            depth += 1
        elif ch == closer:
            depth -= 1
            if depth == 0:
                return "".join(out_chars)
    return None  # incomplete or exceeded max_chars


def parse_json_response(text: str, max_scan_chars: int = 1_000_000) -> Any:
    """
    Parse the first JSON value (object or array) found in the given text.
    Strips surrounding triple-backticks and returns the decoded JSON (could be dict, list, ...).
    Raises ValueError on failure with a helpful message.
    """
    cleaned = _strip_code_fence(text)
    m = re.search(r"[\{\[]", cleaned)
    if not m:
        raise ValueError("No JSON object or array opener ('{' or '[') found in text.")
    start = m.start()
    json_text = _extract_json_at(cleaned, start_idx=start, max_chars=max_scan_chars)
    if not json_text:
        raise ValueError("Could not extract a complete JSON substring (maybe truncated or too large).")
    try:
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        snippet = json_text[:1000]
        raise ValueError(f"json.loads failed: {e.msg} (at pos {e.pos}). Extracted snippet: {snippet!r}") from e
