"""
Smoke tests for the LinkedIn Outreach Agent.
Mocks the Claude API so no real API key is needed in CI.
Run: pytest tests/
"""

import json
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent))

import linkedin_outreach_agent as agent

SAMPLE_PROFILE = {
    "name": "Test User",
    "title": "Software Engineer",
    "company": "TestCorp",
    "reason": "AI agents",
    "goal": "networking",
}

MOCK_CONNECTION = "Hi Test, your work on AI agents at TestCorp caught my eye. I'd love to connect!"

MOCK_FOLLOWUP = json.dumps({
    "step1": "Great to connect! Your AI agent work looks fascinating.",
    "step2": "I thought you might find this article on multi-agent systems useful.",
    "step3": "Would you be open to a 20-minute chat about agent frameworks?",
})


def _mock_call_claude(system, user, max_tokens=512):
    if "connection request" in system.lower():
        return MOCK_CONNECTION
    return MOCK_FOLLOWUP


def test_connection_request_under_limit():
    with patch.object(agent, "_call_claude", side_effect=_mock_call_claude):
        msg = agent.generate_connection_request(SAMPLE_PROFILE)
    assert isinstance(msg, str)
    assert len(msg) <= agent.CONNECTION_LIMIT


def test_followup_sequence_has_three_steps():
    with patch.object(agent, "_call_claude", side_effect=_mock_call_claude):
        seq = agent.generate_followup_sequence(SAMPLE_PROFILE, MOCK_CONNECTION)
    assert set(seq.keys()) == {"step1", "step2", "step3"}
    for val in seq.values():
        assert isinstance(val, str) and len(val) > 0


def test_run_outreach_creates_log(tmp_path, monkeypatch):
    monkeypatch.setattr(agent, "LOG_FILE", tmp_path / "test_log.json")
    with patch.object(agent, "_call_claude", side_effect=_mock_call_claude):
        entry = agent.run_outreach(SAMPLE_PROFILE)
    assert entry["profile"]["name"] == "Test User"
    assert (tmp_path / "test_log.json").exists()
    log = json.loads((tmp_path / "test_log.json").read_text())
    assert len(log) == 1
    assert log[0]["status"] == "pending"


def test_update_status(tmp_path, monkeypatch):
    monkeypatch.setattr(agent, "LOG_FILE", tmp_path / "test_log.json")
    with patch.object(agent, "_call_claude", side_effect=_mock_call_claude):
        agent.run_outreach(SAMPLE_PROFILE)
    result = agent.update_status("Test User", "TestCorp", "accepted")
    assert result is True
    log = json.loads((tmp_path / "test_log.json").read_text())
    assert log[0]["status"] == "accepted"


def test_update_status_not_found(tmp_path, monkeypatch):
    monkeypatch.setattr(agent, "LOG_FILE", tmp_path / "empty_log.json")
    result = agent.update_status("Ghost", "NoCorp", "accepted")
    assert result is False
