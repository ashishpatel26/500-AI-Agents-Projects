# VibeForge

A LangGraph agent that turns a natural-language mood or activity description into a
10-track playlist, with a self-correcting Critic loop for genre diversity, artist
diversity, and mood fit.

**Framework**: LangGraph
**LLM**: Llama 3.3 70B (Groq, free tier)

## What it does

1. **Mood Analyst** — extracts primary emotion, energy level, BPM range, and genre
   preferences from your input
2. **Music Curator** — builds a 10-track playlist matching that analysis
3. **Critic** — scores the playlist 1-10 on genre diversity, artist diversity, and
   mood coherence
4. If the score is below 7, the Critic's feedback is fed back into the Curator (up
   to 2 refinement passes) before the playlist is finalised

```
Mood Analyst → Music Curator → Critic (score < 7?) → Music Curator (refine) → Critic → Finalise
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your Groq API key
```

Get a free API key: https://console.groq.com (no credit card needed)

## Run

```bash
python agent.py --mood "late night lo-fi study session"
python agent.py --mood "sunny road trip, windows down" --context "summer, weekend"
```

## Sample Output

```
Generating a playlist for: late night lo-fi study session

🎭 Mood Analyst — calm focus, low energy, BPM 70-90
🎧 Music Curator — Building 'Late Night Focus'
🧐 Critic — 8/10 (accepted)

============================================================
🎵 Late Night Focus
============================================================
A relaxed, concentrated atmosphere for a late night study session — mellow
beats and warm textures that stay in the background without breaking focus.

 1. Rainy Night — Jinsang [lo-fi, 90 BPM]
    https://open.spotify.com/search/Jinsang%20Rainy%20Night
 2. Aruarian Dance — Nujabes [lo-fi, 95 BPM]
    https://open.spotify.com/search/Nujabes%20Aruarian%20Dance
 ...

Genres: lo-fi hip hop, electronic, instrumental  |  Energy: LOW
```

## Architecture

```
User Input → [Mood Analyst] → mood analysis (emotion, energy, BPM, genres)
                                      │
                                      ▼
                            [Music Curator] → 10-track playlist
                                      │
                                      ▼
                                 [Critic] → score 1-10
                              score < 7 │  score >= 7
                        (max 2 retries) │
                                      ▼  ▼
                        back to Curator   Finalise
```

## Tests

```bash
pip install pytest
pytest test_agent.py -v
```

## Full project

This is a trimmed CLI demo. The full project — a Streamlit web UI, session
memory that learns your preferences over time, live weather/time context, real
Spotify link enrichment, and two additional generation modes — lives at
[github.com/niravpatidar37/mood-playlist-agent](https://github.com/niravpatidar37/mood-playlist-agent).
