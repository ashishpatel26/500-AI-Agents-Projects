"""
NiDaan Demo — Minimal RAG-based Clinical Triage Pipeline
=========================================================

A stripped-down, self-contained version of NiDaan's retrieval-augmented
triage engine, originally built for ASHA (rural health) workers in
West Bengal, India.

Full production system: https://github.com/PriyanshuPaul79/AshaPulse
Live app:               https://nidaan7.vercel.app

This demo shows the core pipeline:
  1. Load a handful of sample clinical protocol snippets.
  2. Build a lightweight, fully offline local vector index
     (TF-IDF embeddings stored in ChromaDB).
  3. Retrieve the most relevant protocol snippets for a patient's symptoms.
  4. Compute a deterministic urgency *safety floor* directly from the
     symptom text (negation-aware keyword matching).
  5. Generate a plain-language recommendation from an LLM backend, but
     always report the safety floor as the final urgency — the LLM's
     free text is supplementary guidance only, and can never lower the
     urgency level below what the deterministic classifier computed.

LLM backend is auto-selected in this order, so the demo runs anywhere
with zero setup:
  1. Groq API      (used if GROQ_API_KEY is set in the environment)
  2. Local Ollama  (used if reachable at localhost:11434)
  3. Rule-based fallback (deterministic, always works, no keys needed)

Note: production NiDaan uses sentence-transformer embeddings and a much
larger IMCI/WHO/NTEP-aligned protocol corpus. This demo swaps in a
TF-IDF embedding function and 5 sample protocol snippets so it can run
in under a minute with no internet access or model downloads.
"""

import os
import re
import sys
import glob

try:
    import chromadb
    from chromadb.api.types import EmbeddingFunction
except ImportError:
    print("Missing dependency. Run: pip install -r requirements.txt")
    sys.exit(1)

from sklearn.feature_extraction.text import TfidfVectorizer

SAMPLE_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_data")


class TfidfEmbeddingFunction(EmbeddingFunction):
    """A lightweight, fully offline embedding function so the demo needs
    no internet access or model downloads (unlike production NiDaan,
    which uses sentence-transformer embeddings via LangChain)."""

    def __init__(self, corpus):
        self.vectorizer = TfidfVectorizer(max_features=512)
        self.vectorizer.fit(corpus)

    def __call__(self, input):
        vecs = self.vectorizer.transform(input).toarray()
        return vecs.tolist()


def load_sample_docs():
    docs, ids, metadatas = [], [], []
    for path in sorted(glob.glob(os.path.join(SAMPLE_DATA_DIR, "*.txt"))):
        with open(path, "r") as f:
            text = f.read().strip()
        docs.append(text)
        ids.append(os.path.basename(path))
        metadatas.append({"source": os.path.basename(path)})
    return docs, ids, metadatas


def build_index(docs, ids, metadatas):
    embed_fn = TfidfEmbeddingFunction(docs)
    client = chromadb.Client()  # in-memory, no persistence needed for the demo
    collection = client.get_or_create_collection(
        name="nidaan_demo", embedding_function=embed_fn
    )
    collection.add(documents=docs, ids=ids, metadatas=metadatas)
    return collection


def retrieve(collection, query, k=2):
    results = collection.query(query_texts=[query], n_results=k)
    return list(
        zip(results["documents"][0], results["metadatas"][0], results["distances"][0])
    )


# ---------------------------------------------------------------------------
# Deterministic, negation-aware urgency classification.
#
# This is a SAFETY FLOOR, not a full clinical decision engine: it is a
# demo-scale illustration of the principle that a triage system's final
# urgency should never be silently lowered by an LLM's free-text output.
# Production NiDaan validates urgency classification against IMCI/WHO/NTEP
# protocols with clinical review; this demo uses a small illustrative
# keyword set instead.
# ---------------------------------------------------------------------------

URGENCY_RANK = {"GREEN": 0, "YELLOW": 1, "RED": 2}

RED_KEYWORDS = [
    "convulsion", "unconscious", "unable to drink", "chest indrawing",
    "severe dehydration", "deep burn", "blue lips", "lethargic",
    "not breathing well",
]

YELLOW_KEYWORDS = [
    "fast breathing", "some dehydration", "fever", "diarrhea", "cough",
    "moderate burn", "vomiting",
]

NEGATION_MARKERS = {
    "no", "not", "without", "denies", "denied", "absent", "negative",
    "ruled", "none", "never",
}


def _is_negated(text, match_start, window=4):
    """Look at the few words immediately before a keyword match to see if
    it was negated (e.g. 'no chest indrawing', 'denies fever',
    'without severe dehydration'). This is a simple heuristic, not full
    NLP negation scoping -- good enough for a demo, not for production
    clinical use."""
    preceding = text[:match_start]
    words = re.findall(r"[a-z']+", preceding.lower())[-window:]
    return any(w in NEGATION_MARKERS for w in words)


def classify_urgency_floor(symptom_text):
    """Return the highest-ranked, non-negated urgency level found in the
    symptom text. This is the safety floor: whatever an LLM backend says
    afterward, the reported urgency is never lower than this."""
    text = symptom_text.lower()
    best_level = "GREEN"

    for level, keywords in (("RED", RED_KEYWORDS), ("YELLOW", YELLOW_KEYWORDS)):
        for kw in keywords:
            for match in re.finditer(re.escape(kw), text):
                if not _is_negated(text, match.start()):
                    if URGENCY_RANK[level] > URGENCY_RANK[best_level]:
                        best_level = level
                    break  # one non-negated hit is enough for this keyword

    return best_level


URGENCY_LABELS = {
    "RED": "RED (refer immediately)",
    "YELLOW": "YELLOW (treat and monitor closely)",
    "GREEN": "GREEN (home care with follow-up advice)",
}


def call_groq(context, query, floor):
    from groq import Groq

    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    prompt = (
        "You are a clinical triage assistant helping a rural health worker.\n"
        f"Relevant protocol notes:\n{context}\n\n"
        f"Patient symptoms: {query}\n\n"
        f"A deterministic safety check has already classified this case as "
        f"urgency level {floor}. Do not suggest anything less urgent than this "
        f"level. In 2-3 sentences, give plain-language next-step guidance "
        f"consistent with that urgency level."
    )
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
    )
    return resp.choices[0].message.content.strip()


def call_ollama(context, query, floor):
    import requests

    prompt = (
        f"Relevant protocol notes:\n{context}\n\n"
        f"Patient symptoms: {query}\n\n"
        f"A deterministic safety check has already classified this case as "
        f"urgency level {floor}. Do not suggest anything less urgent than this "
        f"level. In 2-3 sentences, give plain-language next-step guidance "
        f"consistent with that urgency level."
    )
    resp = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt, "stream": False},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()["response"].strip()


def generate_recommendation(context, query):
    """Compute the deterministic safety floor first, then get supplementary
    free-text guidance from whichever backend is available. The floor is
    always reported as-is; backend text is appended as additional guidance
    and never replaces or downgrades it."""
    floor = classify_urgency_floor(query)
    floor_label = URGENCY_LABELS[floor]

    guidance = None
    source = "rule-based fallback"

    if os.environ.get("GROQ_API_KEY"):
        try:
            guidance = call_groq(context, query, floor)
            source = "Groq"
        except Exception as e:
            print(f"[warn] Groq call failed ({e}), trying Ollama...")

    if guidance is None:
        try:
            guidance = call_ollama(context, query, floor)
            source = "Ollama"
        except Exception:
            guidance = (
                f"Follow the matched protocol notes above. "
                f"Refer to the nearest PHC if this falls in the RED category."
            )
            source = "rule-based fallback"

    return (
        f"Urgency level (deterministic safety floor): {floor_label}\n"
        f"Guidance source: {source}\n"
        f"Matched protocol notes:\n{context}\n"
        f"Recommendation: {guidance}"
    )


def main():
    print("Loading sample clinical protocol snippets...")
    docs, ids, metadatas = load_sample_docs()
    print(f"Loaded {len(docs)} protocol snippets: {ids}\n")

    print("Building local vector index (TF-IDF embeddings + ChromaDB)...")
    collection = build_index(docs, ids, metadatas)

    sample_queries = [
        "3 year old child, fast breathing, chest indrawing, fever since 2 days",
        "child with mild diarrhea, drinking normally, no blood in stool",
        "child with fever but no chest indrawing, alert and drinking well",
    ]

    for query in sample_queries:
        print("=" * 70)
        print(f"Patient symptoms: {query}")
        hits = retrieve(collection, query, k=2)
        context = "\n---\n".join(doc for doc, _, _ in hits)
        print(f"Retrieved protocols: {[meta['source'] for _, meta, _ in hits]}")
        recommendation = generate_recommendation(context, query)
        print(f"\n{recommendation}\n")


if __name__ == "__main__":
    main()