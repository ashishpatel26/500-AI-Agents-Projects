"""Shared utilities used across agents."""

from __future__ import annotations

import json
import logging
import re
from functools import lru_cache
from typing import TYPE_CHECKING, Any, TypeVar

logger = logging.getLogger(__name__)

from pydantic import BaseModel, ValidationError

if TYPE_CHECKING:
    from langchain_groq import ChatGroq
    from .models import Playlist

_M = TypeVar("_M", bound=BaseModel)

DEFAULT_MODEL = "llama-3.3-70b-versatile"
AVAILABLE_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "gemma2-9b-it",
]

PLAYLIST_CURATOR_RULES = """\
- Exactly 10 tracks that genuinely fit the mood.
- Quality mix (like Spotify/YouTube algorithm): 2 well-known hits the user probably loves, 3 cult classics or critically acclaimed deep cuts, 3 fresh discoveries the user likely hasn't heard, 2 wildcard picks from other languages or genres that still fit the vibe.
- Prioritise the user's "loved tracks" — match their energy, genre, and era first. Include 1-2 of them if they fit the mood.
- Include 1-2 "session favorites" if they fit the mood and aren't recently heard.
- Skip every track listed under "recently heard" and "never play again" — no exceptions.
- Genre diversity: no single genre should exceed 40% of the playlist (max 4 out of 10 tracks). Actively mix genres.
- Artist diversity: no artist appears more than twice.
- Support all languages and genres (Bollywood, K-pop, Latin, Afrobeats, jazz, classical, etc.)."""

_PLAYLIST_SCHEMA_DICT = {
    "name": "string",
    "mood_summary": "string",
    "vibe_tags": ["string"],
    "energy_level": "low|medium|high",
    "genres": ["string"],
    "tracks": [{
        "title": "string",
        "artist": "string",
        "genre": "string",
        "bpm": 120,
        "spotify_search_url": "",
        "youtube_search_url": "",
    }],
}
PLAYLIST_JSON_SCHEMA = json.dumps(_PLAYLIST_SCHEMA_DICT, indent=2)


@lru_cache(maxsize=16)
def get_cached_llm(model: str, temperature: float = 0.8) -> ChatGroq:
    """Return a cached ChatGroq client; shared across both pipeline modes."""
    from langchain_groq import ChatGroq
    return ChatGroq(model=model, temperature=temperature)


def _format_json_error(exc: json.JSONDecodeError) -> str:
    return f"Response was not valid JSON at position {exc.pos}: {exc.msg}"


def _format_validation_error(exc: ValidationError) -> str:
    parts: list[str] = []
    for err in exc.errors()[:3]:
        loc = ".".join(str(p) for p in err.get("loc", []))
        msg = err.get("msg", "invalid value")
        parts.append(f"{loc}: {msg}" if loc else msg)
    remaining = len(exc.errors()) - len(parts)
    if remaining > 0:
        parts.append(f"... and {remaining} more error(s)")
    return "; ".join(parts)


def invoke_with_retry(llm: ChatGroq, messages: list[Any], model_class: type[_M], label: str, max_attempts: int = 3) -> _M:
    """Invoke LLM, extract JSON from the response, validate with Pydantic — retry on failure."""
    from langchain_core.messages import HumanMessage

    for attempt in range(max_attempts):
        resp = llm.invoke(messages)
        raw = strip_fences(str(resp.content))
        try:
            return model_class(**json.loads(raw))
        except (json.JSONDecodeError, ValidationError) as exc:
            summary = _format_json_error(exc) if isinstance(exc, json.JSONDecodeError) else _format_validation_error(exc)
            if attempt == max_attempts - 1:
                raise RuntimeError(f"{label} returned invalid JSON after {max_attempts} attempts: {summary}") from exc
            messages = [*messages, HumanMessage(content=f"Your response had errors: {summary}. Return valid JSON only.")]
    raise AssertionError("unreachable")


def clamp_bpm(playlist: Playlist, bpm_range: str) -> None:
    """Clamp track BPMs into the analyst's recommended range, logging violations."""
    match = re.fullmatch(r"(\d+)\s*-\s*(\d+)", bpm_range.strip())
    if not match:
        return
    lo, hi = int(match.group(1)), int(match.group(2))
    for track in playlist.tracks:
        if track.bpm is not None and not (lo <= track.bpm <= hi):
            logger.warning("Track '%s' BPM %d outside %s — clamping", track.title, track.bpm, bpm_range)
            track.bpm = max(lo, min(hi, track.bpm))


def strip_fences(raw: str) -> str:
    """Extract JSON from LLM output — handles fenced blocks and bare unfenced JSON."""
    raw = raw.strip()
    match = re.search(r"```[^\n]*\n(.*?)```", raw, re.DOTALL)
    if match:
        return match.group(1).strip()
    # Fallback: extract the outermost {...} block when the model skips fences
    start, end = raw.find("{"), raw.rfind("}")
    if start != -1 and end > start:
        return raw[start:end + 1]
    return raw
