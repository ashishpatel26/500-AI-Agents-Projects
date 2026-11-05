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
