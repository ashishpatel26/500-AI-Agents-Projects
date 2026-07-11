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
  4. Generate a plain-language triage recommendation (urgency + next step).

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


URGENCY_KEYWORDS = {
    "RED (refer immediately)": [
        "convulsion", "unconscious", "unable to drink", "chest indrawing",
        "severe dehydration", "deep burn", "blue lips", "lethargic",
    ],
    "YELLOW (treat and monitor closely)": [
        "fast breathing", "some dehydration", "fever", "diarrhea", "cough",
        "moderate burn", "vomiting",
    ],
}


def classify_urgency(symptom_text):
    text = symptom_text.lower()
    for level, keywords in URGENCY_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return level
    return "GREEN (home care with follow-up advice)"


def call_groq(context, query):
    from groq import Groq

    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    prompt = (
        "You are a clinical triage assistant helping a rural health worker.\n"
        f"Relevant protocol notes:\n{context}\n\n"
        f"Patient symptoms: {query}\n\n"
        "In 3-4 sentences, give a plain-language triage recommendation and next step."
    )
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
    )
    return resp.choices[0].message.content.strip()


def call_ollama(context, query):
    import requests

    prompt = (
        f"Relevant protocol notes:\n{context}\n\n"
        f"Patient symptoms: {query}\n\n"
        "In 3-4 sentences, give a plain-language triage recommendation and next step."
    )
    resp = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt, "stream": False},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()["response"].strip()


def rule_based_fallback(context, query):
    urgency = classify_urgency(query)
    return (
        f"[Rule-based fallback — no LLM backend configured]\n"
        f"Urgency level: {urgency}\n"
        f"Matched protocol notes:\n{context}\n"
        f"Recommended action: follow the matched protocol above; refer to the "
        f"nearest PHC if symptoms fall in the RED category."
    )


def generate_recommendation(context, query):
    if os.environ.get("GROQ_API_KEY"):
        try:
            return call_groq(context, query)
        except Exception as e:
            print(f"[warn] Groq call failed ({e}), trying Ollama...")
    try:
        return call_ollama(context, query)
    except Exception:
        return rule_based_fallback(context, query)


def main():
    print("Loading sample clinical protocol snippets...")
    docs, ids, metadatas = load_sample_docs()
    print(f"Loaded {len(docs)} protocol snippets: {ids}\n")

    print("Building local vector index (TF-IDF embeddings + ChromaDB)...")
    collection = build_index(docs, ids, metadatas)

    sample_queries = [
        "3 year old child, fast breathing, chest indrawing, fever since 2 days",
        "child with mild diarrhea, drinking normally, no blood in stool",
    ]

    for query in sample_queries:
        print("=" * 70)
        print(f"Patient symptoms: {query}")
        hits = retrieve(collection, query, k=2)
        context = "\n---\n".join(doc for doc, _, _ in hits)
        print(f"Retrieved protocols: {[meta['source'] for _, meta, _ in hits]}")
        recommendation = generate_recommendation(context, query)
        print(f"\nTriage recommendation:\n{recommendation}\n")


if __name__ == "__main__":
    main()