# AI Career & Internship Agent

> **Work in progress:** the pipeline structure and schemas are in place; the agents are not implemented yet.

A LangGraph multi-agent pipeline that compares a resume with a job description,
identifies the missing skills, and produces a personalized plan to close the gap
and prepare for the interview. Built with students and internship applicants in
mind: it treats projects, coursework, and activities as first-class evidence, not
just work history.

**Framework**: LangGraph  
**LLM**: TBD

## What it does

1. **Resume Analyzer**: extracts a structured profile (skills, projects, education, activities)
2. **JD Analyzer**: splits the job description into must-have and nice-to-have requirements
3. **Matching Agent**: computes weighted skill coverage and explains the score
4. **Gap Analysis Agent**: ranks missing skills as blocking / important / nice-to-have, with evidence from the JD
5. **Recommendation Agent**: a 2–4 week learning plan, one small project idea per key gap,
   resume improvements, and interview questions targeted at weak spots

## Architecture

```
Resume ──> [Resume Analyzer] ─┐
                              ├─> [Matching Agent] ─> [Gap Analysis Agent] ─> [Recommendation Agent] ─> Plan
JD ─────> [JD Analyzer] ──────┘
```

The resume and JD analyzers run in parallel; every stage returns a typed Pydantic object.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your API key
```

## Run

```bash
# Built-in sample (Year 3 Computer Engineering student, backend internship)
python agent.py

# Your own resume and job posting
python agent.py --resume path/to/resume.pdf --job-desc path/to/job_posting.txt
```

## Sample Output

_To be added from a real run once the agents are implemented._

## Ethical considerations

- **Not a hiring tool.** The match score is guidance for the applicant, not a
  judgment of their worth. Do not use it to screen or rank candidates.
- **Bias.** LLMs can undervalue non-traditional backgrounds, non-English resumes,
  or unconventional career paths. Treat the gap list as a starting point, not a verdict.
- **Personal data.** Resumes contain PII (names, contact details, education history).
  The text is sent to the configured LLM provider; check its data-retention policy
  before using real resumes, and do not commit resumes to the repository.
