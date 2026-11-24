# AI Career & Internship Agent

A LangGraph multi-agent pipeline that compares a resume with a job description,
identifies the missing skills, and produces a personalized plan to close the gap
and prepare for the interview. Built with students and internship applicants in
mind: it treats projects, coursework, and activities as first-class evidence, not
just work history.

**Framework**: LangGraph  
**LLM**: Gemini 3.6 Flash (Google)

## What it does

1. **Resume Analyzer**: extracts a structured profile (skills, projects, education, activities)
2. **JD Analyzer**: splits the job description into must-have and nice-to-have requirements
3. **Matching Agent**: judges every requirement as met / partial / missing, with evidence from the resume
4. **Gap Analysis Agent**: ranks unmet requirements as blocking / important / nice-to-have, citing the JD
5. **Recommendation Agent**: a week-by-week learning plan, small project ideas that close key gaps,
   specific resume improvements, and interview questions targeted at weak spots

It can also **search a catalog of job postings** for the ones that best fit your skills
(see [Find jobs that match your skills](#find-jobs-that-match-your-skills)).

### How the score works

The LLM only judges evidence; the score is computed in code, so it can be traced
back to the per-requirement assessments:

| | met | partial | missing |
|---|---|---|---|
| must-have (weight 2) | 2 | 1 | 0 |
| nice-to-have (weight 1) | 1 | 0.5 | 0 |

`score = 100 × earned / maximum`. The code also guarantees that every JD requirement
is assessed exactly once, and that a missing must-have is always ranked **blocking**.

## Architecture

```
Resume ──> [Resume Analyzer] ─┐
                              ├─> [Matching Agent] ─> [Gap Analysis Agent] ─> [Recommendation Agent] ─> Plan
JD ─────> [JD Analyzer] ──────┘
```

The resume and JD analyzers run in parallel; every stage returns a typed Pydantic object
via Gemini structured output.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your API key
```

Get a free API key: Google AI Studio, https://aistudio.google.com/apikey

To use a different Gemini model, set `GEMINI_MODEL` in `.env` (default: `gemini-3.6-flash`).

## Run

```bash
# Built-in sample (Year 3 Computer Engineering student, backend internship)
python agent.py

# Your own resume and job posting
python agent.py --resume path/to/resume.pdf --job-desc path/to/job_posting.txt

# 4-week plan, raw JSON output
python agent.py --weeks 4 --json
```

`--resume` and `--job-desc` accept a `.pdf` or text file, or raw text.
Runtime: five LLM calls, typically under a minute.

## Find jobs that match your skills

`--find-jobs` ranks a whole catalog of postings against your skills, best fit first.

```bash
# Type your skills: no LLM call, no API key needed
python agent.py --find-jobs --skills "Python, PostgreSQL, Docker, FastAPI, Git"

# Skills extracted from your resume (1 LLM call), searched against your own postings
python agent.py --find-jobs --resume resume.pdf --jobs jobs.json --top 10

# Re-check the top 3 with the LLM Matching Agent (3 more LLM calls, run in parallel)
python agent.py --find-jobs --resume resume.pdf --rerank 3
```

Without `--jobs`, it searches a built-in catalog of 14 fictional internships in Thailand
(backend, frontend, data, ML, mobile, DevOps, QA, embedded, design, security, games).
`--jobs` takes a JSON list. Each posting has a `title` and `must_have_skills` /
`nice_to_have_skills`, or just a `description`, which the JD Analyzer turns into skills
(one LLM call per posting):

```json
[
  {"id": "acme-be", "title": "Backend Intern", "company": "Acme",
   "must_have_skills": ["Python", "SQL"], "nice_to_have_skills": ["Docker", "AWS or GCP"]},
  {"title": "Data Intern", "description": "We're looking for a student who knows SQL and Python..."}
]
```

**How it works.** Running the Matching Agent on every posting would take one LLM call per job,
so search uses a deterministic matcher on the same met / partial / missing scale and weights as
the main score. It knows three kinds of relationship between skills:

| | Example | Result |
|---|---|---|
| Aliases | `Postgres` for *PostgreSQL*, `ReactJS` for *React* | met |
| Implications | `PostgreSQL` for *SQL*, `Next.js` for *JavaScript*, `scikit-learn` for *Machine Learning* | met |
| Families | `MySQL` for *PostgreSQL*, `Flask` for *FastAPI or Django* | partial |

Requirements with alternatives (`FastAPI or Django`, `Cloud (AWS/GCP)`) are met by any one of them.
Ties are broken by the number of missing must-haves. A skill that isn't in the matcher's tables
(for example `Spring Boot`) only matches its exact name. That is what `--rerank` is for: the
LLM judges the top results from your full resume, including how deep each skill goes.

```
 1. Software Engineer Intern (Backend) — FinTech startup · Bangkok
    📊 91/100
    ✅ Python  ✅ SQL  ✅ REST API design  ✅ Git  ✅ FastAPI or Django  ✅ Docker  ❌ Cloud (AWS/GCP)
```

## Accuracy, performance and tests

None of these call the LLM, so they run without an API key.

```bash
python agent.py --eval        # accuracy against hand-labeled cases
python agent.py --bench       # search speed on synthetic catalogs of 1k / 10k / 50k jobs
python agent.py --self-test   # unit, accuracy and performance tests (also: python -m unittest agent)
```

**Accuracy** (`--eval`) is measured at two levels and compared with an exact-name baseline
that uses the same weights but no aliases, implications or families:

| Level | Metric | Matcher | Exact-name baseline |
|---|---|---|---|
| Requirement (39 cases) | status accuracy (met/partial/missing) | 92.3% | 15.4% |
| Ranking (9 candidates × 14 jobs) | Top-1 (best result is a strong fit) | 0.89 | 0.78 |
| | MRR (first strong fit) | 0.91 | 0.87 |
| | NDCG@5 | 0.95 | 0.91 |
| | Recall@5 (any fit) | 0.90 | 0.84 |

The three requirement misses are out-of-vocabulary on purpose (`Spring Boot` → Java,
`MongoDB` → NoSQL, `React` → React Native). The ranking miss is the sample-resume candidate:
it lists React, so the matcher ranks the frontend internship first, while a human reading the
resume sees "basic React" and ranks the backend role first. Skill names alone can't show depth.

The labels were written by hand for this project, alongside the matcher, so treat these numbers
as a regression check on a small set, not as a benchmark of real-world accuracy. To measure
accuracy on your own data, add candidates and labels to `EVAL_CANDIDATES` and `REQUIREMENT_CASES`
in `agent.py`.

**Performance** (`--bench`, one laptop, Python 3.10):

| Jobs | Index build | Search p50 | Search p95 |
|---|---|---|---|
| 1,000 | 26 ms | 3.2 ms | 3.5 ms |
| 10,000 | 267 ms | 22.8 ms | 30.0 ms |
| 50,000 | 1.2 s | 98 ms | 109 ms |

Search time grows linearly with the catalog, at about 400k jobs/second. Requirements are
parsed once when the index is built, each skill verdict is cached per search, and the detailed
per-requirement output is built only for the jobs returned. `--self-test` fails if a
10k-job search takes over 250 ms at p95 or the index build takes over 2 s.

## Sample Output

_To be added from a real run._

## Ethical considerations

- **Not a hiring tool.** The match score is guidance for the applicant, not a
  judgment of their worth. Do not use it to screen or rank candidates.
- **Bias.** LLMs can undervalue non-traditional backgrounds, non-English resumes,
  or unconventional career paths. Treat the gap list as a starting point, not a verdict.
- **Hallucinated resources.** Learning resources are named, not linked, to avoid
  invented URLs; check that a course or book exists before relying on it.
- **Personal data.** Resumes contain PII (names, contact details, education history).
  The text is sent to Google's Gemini API; check its data-use terms (the free tier
  may use inputs to improve Google's products) before using real resumes, and
  do not commit resumes to the repository.
