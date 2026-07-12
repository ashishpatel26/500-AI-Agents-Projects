# NiDaan — RAG-based Clinical Triage Assistant (Demo)

A minimal, self-contained demo of **NiDaan**, a retrieval-augmented clinical
triage assistant originally built for ASHA (rural health) workers in West
Bengal, India. This demo distills the core RAG pipeline into a single
runnable script so it can be evaluated without the full production stack.

- **Full project:** https://github.com/PriyanshuPaul79/AshaPulse
- **Live app:** https://nidaan7.vercel.app (20–30 active daily field users)

## What this demo does

1. Loads a handful of sample clinical protocol snippets (fever, respiratory
   distress, dehydration, burns, malnutrition).
2. Builds a local vector index using ChromaDB with a custom TF-IDF embedding
   function — fully offline, no model downloads required.
3. Retrieves the most relevant protocol snippets for a given set of patient
   symptoms.
4. Generates a plain-language triage recommendation (urgency level + next
   step), using whichever LLM backend is available:
   - **Groq API** if `GROQ_API_KEY` is set
   - **Local Ollama** if running at `localhost:11434`
   - **Rule-based fallback** if neither is available (always works, zero
     setup)

This mirrors the production system's swappable multi-provider LLM routing
(Groq / NVIDIA NIM / Ollama), just simplified for a quick, dependency-light
demo.

## Quick start

```bash
pip install -r requirements.txt
python run_demo.py
```

No API key or internet access is required to see a full end-to-end run —
the rule-based fallback kicks in automatically. To see LLM-generated
recommendations instead, set `GROQ_API_KEY` first:

```bash
export GROQ_API_KEY=your_key_here
python run_demo.py
```

**Runtime:** under 30 seconds on a modest CPU-only machine (laptop, no GPU
needed).

## Expected output

```
Loading sample clinical protocol snippets...
Loaded 5 protocol snippets: [...list of files found in sample_data/...]

Building local vector index (TF-IDF embeddings + ChromaDB)...
======================================================================
Patient symptoms: 3 year old child, fast breathing, chest indrawing, fever since 2 days
Retrieved protocols: [the 2 most relevant .txt files in sample_data/]

Urgency level (deterministic safety floor): RED (refer immediately)
Guidance source: rule-based fallback
Matched protocol notes: ...
Recommendation: Follow the matched protocol notes above. Refer to the
nearest PHC if this falls in the RED category.
```

Note: `run_demo.py` loads every `.txt` file found in `sample_data/` dynamically
(via `glob`), so the exact filenames and their count aren't hardcoded anywhere
in the code — only illustrative in this README.

The **urgency level is always computed deterministically first** (negation-aware
keyword matching over the symptom text), before any LLM backend runs. Whichever
backend generates the free-text "Recommendation" line, it cannot override or
lower that safety-floor urgency level.

## Running the smoke test

```bash
python tests/test_smoke.py
```

This runs the full pipeline end-to-end using the rule-based fallback only,
so it passes with no API keys or internet access.

## A note on the pinned `chromadb` version

`requirements.txt` pins `chromadb==0.5.23`, a version from before `1.0.0`.
This is deliberate: ChromaDB versions `1.0.0` through at least `1.5.9` have a
critical, still-unpatched pre-authentication RCE (CVE-2026-45829,
"ChromaToast") in the Python FastAPI **server**, triggered via a malicious
Hugging Face model reference with `trust_remote_code`. This demo never runs
that server or that embedding function — it only uses the local in-memory
`chromadb.Client()` with a custom TF-IDF embedding function — so it isn't
exploitable via this CVE as written. Even so, pinning a version that
predates the vulnerability entirely is the safer choice for a public
contribution. If you upgrade this dependency later, check whether a patched
release exists first.

## Ethical considerations / safety notes

This is a **demo for educational and portfolio purposes**, not a
production-ready medical device:

- Sample protocol snippets here are simplified, original summaries written
  for demonstration only — they are **not** verbatim reproductions of any
  clinical guideline document, and should not be used for real patient care.
- The production NiDaan system is designed as a **decision-support tool**
  for trained ASHA workers, always with a human-in-the-loop, and is not a
  substitute for clinical judgment or referral to a qualified health
  facility.
- Any real deployment of a clinical triage tool should be validated against
  official protocols (e.g. IMCI/WHO/NTEP) by qualified medical
  professionals before use, and should always default to the safer
  (more urgent) classification when uncertain.

## Architecture notes (for reviewers)

- **Retrieval:** ChromaDB with a custom TF-IDF `EmbeddingFunction` (kept
  lightweight/offline for this demo; production uses sentence-transformer
  embeddings via LangChain).
- **Generation:** tiered LLM fallback (Groq → Ollama → rule-based), mirroring
  the production system's multi-provider routing design.
- **Urgency classification:** a deterministic, negation-aware keyword classifier
  computes a *safety floor* directly from the symptom text, independently of
  any LLM backend. This floor is always reported as-is and cannot be lowered
  by an LLM's free-text output — the LLM only supplies supplementary guidance
  text. This demo's classifier is intentionally simple (illustrative keyword
  matching with negation detection); production system uses LLM-driven
  classification grounded in retrieved IMCI/WHO/NTEP protocol content, with
  adversarial test cases validated against clinical review.