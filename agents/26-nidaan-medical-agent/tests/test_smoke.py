"""
Smoke test for the NiDaan demo.

Confirms the full pipeline (load docs -> build index -> retrieve ->
generate recommendation) runs end-to-end, using only the rule-based
fallback path (no API keys or local LLM required). Also directly
exercises the deterministic urgency classifier against negation and
conflicting-symptom cases, since that classifier is the safety floor
for the whole system.

The Ollama call path is explicitly patched to fail in the end-to-end
test, so it deterministically exercises the rule-based fallback
regardless of whether the machine running it happens to have Ollama
installed and running locally.

Run with: python tests/test_smoke.py
"""

import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Make sure no LLM backends are picked up during the smoke test, so it
# always exercises the deterministic rule-based fallback path.
os.environ.pop("GROQ_API_KEY", None)

import agent
from agent import (
    load_sample_docs,
    build_index,
    retrieve,
    generate_recommendation,
    classify_urgency_floor,
)


def test_pipeline_runs_end_to_end():
    docs, ids, metadatas = load_sample_docs()
    assert len(docs) >= 3, "Expected at least 3 sample protocol snippets"

    collection = build_index(docs, ids, metadatas)

    query = "3 year old child, fast breathing, chest indrawing, fever since 2 days"
    hits = retrieve(collection, query, k=2)
    assert len(hits) == 2, "Expected 2 retrieved documents"

    context = "\n---\n".join(doc for doc, _, _ in hits)

    # Force the Ollama path to fail so this test always exercises the
    # deterministic rule-based fallback, independent of the local machine.
    with patch.object(
        agent, "call_ollama", side_effect=RuntimeError("Ollama disabled in smoke test")
    ):
        recommendation = generate_recommendation(context, query)

    assert isinstance(recommendation, str) and len(recommendation) > 0
    assert "Urgency level (deterministic safety floor): RED" in recommendation, (
        "Expected the safety floor to classify this case as RED, got:\n" + recommendation
    )
    assert "refer to the nearest phc" in recommendation.lower(), (
        "Expected a referral recommendation for a RED case, got:\n" + recommendation
    )
    print("End-to-end test passed. Sample recommendation:\n", recommendation)


def test_urgency_floor_affirmed_danger_sign():
    """A clearly affirmed danger sign should classify as RED."""
    level = classify_urgency_floor(
        "3 year old child, fast breathing, chest indrawing, fever since 2 days"
    )
    assert level == "RED", f"Expected RED, got {level}"


def test_urgency_floor_negated_danger_sign():
    """The same danger-sign phrase, negated, should NOT trigger RED.
    This is the exact failure mode the reviewer flagged: naive substring
    matching would incorrectly classify this as RED."""
    level = classify_urgency_floor(
        "child with fever but no chest indrawing, alert and drinking well"
    )
    assert level == "YELLOW", f"Expected YELLOW (fever alone), got {level}"


def test_urgency_floor_negated_symptom_word():
    """'denies vomiting' should not count as an active vomiting symptom."""
    level = classify_urgency_floor(
        "child denies vomiting, no fever, playing normally"
    )
    assert level == "GREEN", f"Expected GREEN, got {level}"


def test_urgency_floor_conflicting_symptoms():
    """When a mild symptom (fever) and a genuine danger sign (unable to
    drink) both appear, the danger sign must win -- urgency should never
    be silently averaged or downgraded."""
    level = classify_urgency_floor(
        "child has mild fever but is unable to drink and appears lethargic"
    )
    assert level == "RED", f"Expected RED (danger sign present), got {level}"


def test_urgency_floor_multiple_negations():
    """Multiple negated danger signs alongside an affirmed mild symptom
    should resolve to the mild level, not RED."""
    level = classify_urgency_floor(
        "no convulsions, not unconscious, no severe dehydration, but has a cough"
    )
    assert level == "YELLOW", f"Expected YELLOW (cough only), got {level}"


if __name__ == "__main__":
    test_pipeline_runs_end_to_end()
    test_urgency_floor_affirmed_danger_sign()
    test_urgency_floor_negated_danger_sign()
    test_urgency_floor_negated_symptom_word()
    test_urgency_floor_conflicting_symptoms()
    test_urgency_floor_multiple_negations()
    print("\n✅ All smoke tests passed.")