"""Integration-style example runs (require GROQ_API_KEY — skipped if absent)."""

import os
import pytest

pytestmark = pytest.mark.skipif(
    not os.getenv("GROQ_API_KEY"),
    reason="GROQ_API_KEY not set — skipping live API tests",
)


@pytest.fixture(autouse=True)
def isolated_memory(tmp_path, monkeypatch):
    """Redirect session memory to a temp dir so tests never touch ~/.vibeforge."""
    monkeypatch.setenv("VIBEFORGE_DATA_DIR", str(tmp_path))


def test_generate_playlist_chill():
    from mood_playlist_agent.playlist_agent import generate_playlist
    playlist = generate_playlist("feeling chill after a long day", spotify_enrich=False)
    assert playlist.name
    assert len(playlist.tracks) == 10
    assert playlist.energy_level in {"low", "medium", "high"}


def test_generate_playlist_workout():
    from mood_playlist_agent.playlist_agent import generate_playlist
    playlist = generate_playlist("pumped up for gym, need high energy", spotify_enrich=False)
    assert playlist.energy_level in {"medium", "high"}
    assert len(playlist.tracks) == 10


def test_generate_playlist_multilingual():
    from mood_playlist_agent.playlist_agent import generate_playlist
    playlist = generate_playlist("nostalgic Bollywood evening", spotify_enrich=False)
    assert playlist.name
    genres_lower = [g.lower() for g in playlist.genres]
    assert any("bollywood" in g or "hindi" in g or "indian" in g for g in genres_lower)


def test_generate_playlist_with_crew():
    from mood_playlist_agent.crew_agent import generate_playlist_with_crew
    playlist = generate_playlist_with_crew("Sunday morning coffee and jazz", spotify_enrich=False)
    assert playlist.name
    assert len(playlist.tracks) == 10


def test_generate_playlist_with_graph():
    from mood_playlist_agent.graph_agent import generate_playlist_with_graph
    playlist = generate_playlist_with_graph("birthday celebration, high energy party", spotify_enrich=False)
    assert playlist.name
    assert len(playlist.tracks) == 10
    assert playlist.energy_level in {"low", "medium", "high"}


def test_generate_playlist_with_graph_streams():
    from mood_playlist_agent.graph_agent import stream_playlist_with_graph
    nodes_seen = []
    state = {}
    for node_name, current in stream_playlist_with_graph(
        "rainy evening, jazz and coffee", spotify_enrich=False
    ):
        nodes_seen.append(node_name)
        state = current
    assert "analyse_mood" in nodes_seen
    assert "curate_playlist" in nodes_seen
    assert "finalise" in nodes_seen
    assert state.get("playlist") is not None
    assert len(state["playlist"].tracks) == 10
