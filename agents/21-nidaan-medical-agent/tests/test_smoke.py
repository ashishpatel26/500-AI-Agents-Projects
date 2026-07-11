"""
Smoke test for the NiDaan demo.

Confirms the full pipeline (load docs -> build index -> retrieve ->
generate recommendation) runs end-to-end without error, using only the
rule-based fallback (no API keys or local LLM required). This is what
CI / reviewers should run to verify the contribution works.

Run with: python tests/test_smoke.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Make sure no LLM backends are picked up during the smoke test, so it
# always exercises the deterministic rule-based fallback path.
os.environ.pop("GROQ_API_KEY", None)

from run_demo import load_sample_docs, build_index, retrieve, generate_recommendation


def test_pipeline_runs_end_to_end():
    docs, ids, metadatas = load_sample_docs()
    assert len(docs) >= 3, "Expected at least 3 sample protocol snippets"

    collection = build_index(docs, ids, metadatas)

    query = "3 year old child, fast breathing, chest indrawing, fever since 2 days"
    hits = retrieve(collection, query, k=2)
    assert len(hits) == 2, "Expected 2 retrieved documents"

    context = "\n---\n".join(doc for doc, _, _ in hits)
    recommendation = generate_recommendation(context, query)

    assert isinstance(recommendation, str) and len(recommendation) > 0
    print("Smoke test passed. Sample recommendation:\n", recommendation)


if __name__ == "__main__":
    test_pipeline_runs_end_to_end()
    print("\n✅ All smoke tests passed.")