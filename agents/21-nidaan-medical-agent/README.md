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
Loaded 5 protocol snippets: ['burn_injury.txt', 'diarrhea_dehydration.txt', ...]

Building local vector index (TF-IDF embeddings + ChromaDB)...
======================================================================
Patient symptoms: 3 year old child, fast breathing, chest indrawing, fever since 2 days
Retrieved protocols: ['pneumonia_signs.txt', 'fever_child.txt']

Triage recommendation:
[Rule-based fallback — no LLM backend configured]
Urgency level: RED (refer immediately)
...
```

## Running the smoke test

```bash
python tests/test_smoke.py
```

This runs the full pipeline end-to-end using the rule-based fallback only,
so it passes with no API keys or internet access.

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
- **Urgency classification:** simple keyword-based heuristic in this demo;
  production system uses LLM-driven classification grounded in retrieved
  IMCI/WHO/NTEP protocol content, with adversarial test cases validated
  against clinical review.