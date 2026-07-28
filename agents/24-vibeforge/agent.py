"""
VibeForge — mood-based playlist agent with a self-correcting Critic loop.

A LangGraph state machine: a Mood Analyst extracts emotional context from a
natural-language mood/activity description, a Music Curator builds a 10-track
playlist from that analysis, and a Critic scores it 1-10 on genre diversity,
artist diversity, and mood fit. If the score is below the bar, the Critic's
feedback is fed back into the Curator (up to two refinement passes) before the
playlist is finalised.

Usage:
    python agent.py --mood "late night lo-fi study session"
    python agent.py --mood "sunny road trip, windows down" --context "summer, weekend"
"""

import argparse
import json
import re
import sys
from typing import Literal, Optional, TypedDict
from urllib.parse import quote_plus

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import END, StateGraph
from pydantic import BaseModel, Field, ValidationError

load_dotenv()

if sys.stdout.encoding.lower() != "utf-8":  # emoji-safe output on legacy Windows consoles
    sys.stdout.reconfigure(encoding="utf-8")

DEFAULT_MODEL = "llama-3.3-70b-versatile"
ACCEPT_SCORE = 7
MAX_REFINEMENTS = 2


# --- Schemas ------------------------------------------------------------------

class Track(BaseModel):
    title: str
    artist: str
    genre: str
    bpm: Optional[int] = None


class Playlist(BaseModel):
    name: str = Field(description="Creative playlist name reflecting the mood")
    mood_summary: str = Field(description="2-3 sentence description of the mood and why these songs fit")
    energy_level: Literal["low", "medium", "high"]
    tracks: list[Track] = Field(description="Exactly 10 tracks", min_length=10, max_length=10)
    genres: list[str] = Field(description="Primary genres featured in this playlist")


class MoodAnalysis(BaseModel):
    primary_emotion: str
    energy_level: Literal["low", "medium", "high"]
    bpm_range: str
    recommended_genres: list[str]
    avoid_genres: list[str]


class Critique(BaseModel):
    score: int = Field(ge=1, le=10, description="Overall quality score 1-10")
    issues: list[str] = Field(description="Specific problems found in the playlist")
    feedback: str = Field(description="Actionable instructions for the curator to fix the issues")


class AgentState(TypedDict):
    mood_input: str
    context: str
    model: str
    mood_analysis: Optional[MoodAnalysis]
    playlist: Optional[Playlist]
    critique: Optional[Critique]
    refinement_attempts: int


# --- Prompts --------------------------------------------------------------------

ANALYST_PROMPT = """You are a music psychologist and emotion expert.
Analyse the user's mood/activity input and return ONLY valid JSON — no markdown, no extra text:
{
  "primary_emotion": "string",
  "energy_level": "low|medium|high",
  "bpm_range": "60-80",
  "recommended_genres": ["string"],
  "avoid_genres": ["string"]
}"""

CURATOR_PROMPT = """You are a world-class DJ and music curator with encyclopaedic knowledge of songs \
across all genres, eras, and languages. Given a mood analysis (and optional critic feedback), curate a \
10-track playlist. Return ONLY valid JSON — no markdown, no extra text:
{
  "name": "string",
  "mood_summary": "string",
  "energy_level": "low|medium|high",
  "genres": ["string"],
  "tracks": [{"title": "string", "artist": "string", "genre": "string", "bpm": 120}]
}
Rules:
- Exactly 10 tracks that genuinely fit the mood.
- Quality mix: 2-3 well-known hits, 3 cult classics or deep cuts, 3-4 fresh discoveries the \
listener likely hasn't heard.
- Genre diversity: no single genre exceeds 40% of the playlist (max 4 of 10 tracks).
- Artist diversity: no artist appears more than twice.
- BPM values must fall within the bpm_range from the mood analysis."""

CRITIC_PROMPT = """You are a music playlist quality critic. Evaluate the playlist against these criteria:
1. Genre diversity — no single genre > 40% of tracks
2. Artist diversity — no artist appears more than twice
3. Mood coherence — tracks genuinely fit the stated mood and energy level
4. Track authenticity — all tracks are real, well-known recordings

Return ONLY valid JSON — no markdown, no extra text:
{"score": 8, "issues": ["issue 1"], "feedback": "actionable instructions for the curator"}

Score 8-10: excellent, accept as-is. Score 5-7: decent but fixable. Score 1-4: significant problems."""


# --- LLM helpers ------------------------------------------------------------------

def strip_fences(raw: str) -> str:
    """Extract JSON from LLM output — handles fenced blocks and bare unfenced JSON."""
    raw = raw.strip()
    match = re.search(r"```[^\n]*\n(.*?)```", raw, re.DOTALL)
    if match:
        return match.group(1).strip()
    start, end = raw.find("{"), raw.rfind("}")
    return raw[start:end + 1] if start != -1 and end > start else raw


def invoke_json(llm: ChatGroq, messages: list, schema: type, label: str, max_attempts: int = 3):
    """Invoke the LLM, parse + validate the JSON response, retrying on failure."""
    for attempt in range(max_attempts):
        raw = str(llm.invoke(messages).content)
        try:
            return schema(**json.loads(strip_fences(raw)))
        except (json.JSONDecodeError, ValidationError) as exc:
            if attempt == max_attempts - 1:
                raise RuntimeError(f"{label} returned invalid JSON after {max_attempts} attempts") from exc
            messages = [*messages, HumanMessage(content=f"Your response had errors: {exc}. Return valid JSON only.")]


def search_links(title: str, artist: str) -> tuple[str, str]:
    q = quote_plus(f"{artist} {title}")
    return f"https://open.spotify.com/search/{q}", f"https://www.youtube.com/results?search_query={q}"


# --- Graph nodes ---------------------------------------------------------------

def analyse_mood(state: AgentState) -> AgentState:
    llm = ChatGroq(model=state["model"], temperature=0.7)
    user_msg = f"Mood / activity: {state['mood_input']}"
    if state["context"]:
        user_msg += f"\nContext: {state['context']}"
    analysis = invoke_json(
        llm, [SystemMessage(content=ANALYST_PROMPT), HumanMessage(content=user_msg)], MoodAnalysis, "Mood Analyst"
    )
    print(f"🎭 Mood Analyst — {analysis.primary_emotion}, {analysis.energy_level} energy, BPM {analysis.bpm_range}")
    return {**state, "mood_analysis": analysis}


def curate_playlist(state: AgentState) -> AgentState:
    llm = ChatGroq(model=state["model"], temperature=0.8)
    analysis = state["mood_analysis"]
    assert analysis is not None
    content = f"Mood analysis:\n{analysis.model_dump_json(indent=2)}"
    critique = state.get("critique")
    if critique and state["refinement_attempts"] > 0:
        content += (
            f"\n\nCritic review (score {critique.score}/10 — needs improvement):\n"
            f"Issues: {'; '.join(critique.issues)}\nFeedback: {critique.feedback}\n"
            "Please address ALL issues above in your revised playlist."
        )
    playlist = invoke_json(
        llm, [SystemMessage(content=CURATOR_PROMPT), HumanMessage(content=content)], Playlist, "Music Curator"
    )
    verb = "Refining" if state["refinement_attempts"] > 0 else "Building"
    print(f"🎧 Music Curator — {verb} '{playlist.name}'")
    return {**state, "playlist": playlist}


def critique_playlist(state: AgentState) -> AgentState:
    llm = ChatGroq(model=state["model"], temperature=0.3)
    playlist = state["playlist"]
    assert playlist is not None
    content = f"Mood: {state['mood_input']}\n\nPlaylist:\n{playlist.model_dump_json(indent=2)}"
    critique = invoke_json(
        llm, [SystemMessage(content=CRITIC_PROMPT), HumanMessage(content=content)], Critique, "Critic"
    )
    verdict = "accepted" if critique.score >= ACCEPT_SCORE else "needs refinement"
    print(f"🧐 Critic — {critique.score}/10 ({verdict})")
    return {**state, "critique": critique}


def route_after_critique(state: AgentState) -> str:
    critique = state.get("critique")
    if critique and critique.score < ACCEPT_SCORE and state["refinement_attempts"] < MAX_REFINEMENTS:
        return "refine"
    return "finalise"


def increment_attempts(state: AgentState) -> AgentState:
    return {**state, "refinement_attempts": state["refinement_attempts"] + 1}


def finalise(state: AgentState) -> AgentState:
    return state


def build_graph():
    g = StateGraph(AgentState)
    g.add_node("analyse_mood", analyse_mood)
    g.add_node("curate_playlist", curate_playlist)
    g.add_node("critique_playlist", critique_playlist)
    g.add_node("increment_attempts", increment_attempts)
    g.add_node("finalise", finalise)

    g.set_entry_point("analyse_mood")
    g.add_edge("analyse_mood", "curate_playlist")
    g.add_edge("curate_playlist", "critique_playlist")
    g.add_conditional_edges(
        "critique_playlist", route_after_critique, {"refine": "increment_attempts", "finalise": "finalise"}
    )
    g.add_edge("increment_attempts", "curate_playlist")
    g.add_edge("finalise", END)
    return g.compile()


# --- CLI --------------------------------------------------------------------------

def print_playlist(playlist: Playlist) -> None:
    print(f"\n{'=' * 60}")
    print(f"🎵 {playlist.name}")
    print(f"{'=' * 60}")
    print(f"{playlist.mood_summary}\n")
    for i, track in enumerate(playlist.tracks, 1):
        spotify_url, youtube_url = search_links(track.title, track.artist)
        bpm = f"{track.bpm} BPM" if track.bpm else ""
        print(f"{i:>2}. {track.title} — {track.artist} [{track.genre}{', ' + bpm if bpm else ''}]")
        print(f"    {spotify_url}")
    print(f"\nGenres: {', '.join(playlist.genres)}  |  Energy: {playlist.energy_level.upper()}")


def run(mood: str, context: str, model: str) -> Playlist:
    graph = build_graph()
    initial: AgentState = {
        "mood_input": mood,
        "context": context,
        "model": model,
        "mood_analysis": None,
        "playlist": None,
        "critique": None,
        "refinement_attempts": 0,
    }
    final = graph.invoke(initial)
    playlist = final["playlist"]
    if playlist is None:
        raise RuntimeError("Pipeline failed to produce a playlist.")
    return playlist


def main():
    parser = argparse.ArgumentParser(description="VibeForge — AI mood-based playlist generator")
    parser.add_argument("--mood", help="Mood or activity description, e.g. 'rainy day, studying'")
    parser.add_argument("--context", default="", help="Extra context, e.g. 'weekend, summer'")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Groq model to use")
    args = parser.parse_args()

    mood = args.mood or input("How are you feeling? ")
    print(f"\nGenerating a playlist for: {mood}\n")
    playlist = run(mood, args.context, args.model)
    print_playlist(playlist)


if __name__ == "__main__":
    main()
