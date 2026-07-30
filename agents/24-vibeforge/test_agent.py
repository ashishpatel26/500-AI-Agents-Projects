"""Unit tests for VibeForge's schemas and helpers — no API key needed."""

import pytest
from pydantic import ValidationError

from agent import Playlist, Track, search_links, strip_fences


def make_track(**kwargs):
    defaults = {"title": "Blinding Lights", "artist": "The Weeknd", "genre": "Synth-pop"}
    return Track(**{**defaults, **kwargs})


def make_playlist(n_tracks: int = 10) -> Playlist:
    tracks = [make_track(title=f"Song {i}", artist=f"Artist {i}") for i in range(n_tracks)]
    return Playlist(
        name="Test Vibes", mood_summary="A test playlist", energy_level="medium", genres=["Pop"], tracks=tracks
    )


class TestPlaylist:
    def test_valid_playlist(self):
        assert len(make_playlist().tracks) == 10

    def test_too_few_tracks_raises(self):
        with pytest.raises(ValidationError):
            make_playlist(n_tracks=3)

    def test_too_many_tracks_raises(self):
        with pytest.raises(ValidationError):
            make_playlist(n_tracks=13)

    def test_invalid_energy_level_raises(self):
        with pytest.raises(ValidationError):
            Playlist(
                name="Bad", mood_summary="bad", energy_level="extreme", genres=[],
                tracks=[make_track(title=f"Song {i}", artist=f"A {i}") for i in range(10)],
            )


class TestSearchLinks:
    def test_returns_spotify_and_youtube_urls(self):
        spotify_url, youtube_url = search_links("Blinding Lights", "The Weeknd")
        assert spotify_url.startswith("https://open.spotify.com/search/")
        assert youtube_url.startswith("https://www.youtube.com/results?search_query=")
        assert "Weeknd" in spotify_url


class TestStripFences:
    def test_extracts_fenced_json(self):
        raw = '```json\n{"a": 1}\n```'
        assert strip_fences(raw) == '{"a": 1}'

    def test_extracts_bare_json(self):
        assert strip_fences('here you go: {"a": 1} thanks') == '{"a": 1}'
