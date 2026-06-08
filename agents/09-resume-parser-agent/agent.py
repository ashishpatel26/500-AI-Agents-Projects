"""
Resume Parser Agent using LangChain.

Extracts structured information from resume text or PDF:
contact info, skills, experience, education, and provides
a candidate summary and fit score for a job description.

Usage:
    python agent.py --resume resume.txt
    python agent.py --resume resume.pdf --job-desc "Senior Python Developer with 5+ years..."
"""

import argparse
import json
import os
import re

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

load_dotenv()

PARSE_PROMPT = """Extract structured information from this resume and return JSON:
{
  "name": "full name",
  "email": "email or null",
  "phone": "phone or null",
  "location": "city, country or null",
  "linkedin": "URL or null",
  "github": "URL or null",
  "summary": "2-3 sentence professional summary",
  "years_experience": number,
  "current_title": "current/most recent job title",
  "skills": {
    "languages": ["Python", "JavaScript", ...],
    "frameworks": ["Django", "React", ...],
    "tools": ["Docker", "Git", ...],
    "soft_skills": ["leadership", ...]
  },
  "experience": [{"title": "...", "company": "...", "duration": "...", "highlights": ["..."]}],
  "education": [{"degree": "...", "institution": "...", "year": "..."}],
  "certifications": ["..."],
  "languages_spoken": ["English", ...]
}
Return only valid JSON."""

FIT_PROMPT = """Given this candidate profile and job description, return JSON:
{
  "fit_score": 0-100,
  "fit_label": "Excellent|Good|Fair|Poor",
  "strengths": ["matching point 1", "matching point 2", ...],
  "gaps": ["missing skill 1", ...],
  "recommendation": "Hire|Consider|Pass",
  "recommendation_reason": "2-3 sentence explanation"
}
Return only valid JSON."""


def parse_json_response(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        cleaned = match.group(0)
    return json.loads(cleaned)


def read_resume_text(path: str) -> str:
    if path.endswith(".pdf"):
        try:
            import pypdf
            with open(path, "rb") as f:
                reader = pypdf.PdfReader(f)
                return "\n".join(page.extract_text() for page in reader.pages)
        except ImportError:
            print("⚠️  pypdf not installed. Install with: pip install pypdf")
            raise
    with open(path) as f:
        return f.read()


def parse_resume(text: str) -> dict:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    messages = [SystemMessage(content=PARSE_PROMPT), HumanMessage(content=text)]
    response = llm.invoke(messages)
    return parse_json_response(response.content)


def score_fit(profile: dict, job_desc: str) -> dict:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    messages = [
        SystemMessage(content=FIT_PROMPT),
        HumanMessage(content=f"Candidate profile:\n{json.dumps(profile, indent=2)}\n\nJob description:\n{job_desc}"),
    ]
    response = llm.invoke(messages)
    return parse_json_response(response.content)


SAMPLE_RESUME = """
Jane Doe
jane.doe@email.com | +1 (555) 123-4567 | San Francisco, CA
linkedin.com/in/janedoe | github.com/janedoe

SUMMARY
Senior Python developer with 7 years of experience building scalable web applications
and data pipelines. Led teams of 5-8 engineers at Series B startups.

EXPERIENCE
Senior Software Engineer | TechCorp Inc. | 2021-present
- Architected microservices platform handling 10M requests/day using FastAPI + Kubernetes
- Reduced API latency by 40% through Redis caching and async optimization
- Led migration from monolith to microservices (12-month project, 5 engineers)

Software Engineer | DataFlow Systems | 2018-2021
- Built ML data pipelines processing 500GB/day using Apache Spark and Airflow
- Developed REST APIs with Django REST Framework serving 50k daily users

SKILLS
Languages: Python, JavaScript, SQL, Bash
Frameworks: FastAPI, Django, React, Spark
Tools: Docker, Kubernetes, Redis, PostgreSQL, Git, Airflow
Cloud: AWS (EC2, S3, RDS, Lambda)

EDUCATION
B.S. Computer Science | UC Berkeley | 2017

CERTIFICATIONS
AWS Solutions Architect Associate
"""


def main():
    parser = argparse.ArgumentParser(description="Resume Parser Agent")
    parser.add_argument("--resume", help="Path to resume file (.txt or .pdf)")
    parser.add_argument("--job-desc", help="Job description to match against")
    args = parser.parse_args()

    if args.resume:
        print(f"\n📄 Parsing resume: {args.resume}")
        text = read_resume_text(args.resume)
    else:
        print("\n📄 Using sample resume (pass --resume to use your own)")
        text = SAMPLE_RESUME

    profile = parse_resume(text)

    print("\n" + "=" * 60)
    print("👤 PARSED RESUME")
    print("=" * 60)
    print(f"Name: {profile.get('name')}")
    print(f"Title: {profile.get('current_title')}")
    print(f"Experience: {profile.get('years_experience')} years")
    print(f"Skills: {', '.join(profile.get('skills', {}).get('languages', []))}")
    print(f"\nSummary: {profile.get('summary')}")

    if args.job_desc:
        print("\n" + "=" * 60)
        print("📊 JOB FIT ANALYSIS")
        print("=" * 60)
        fit = score_fit(profile, args.job_desc)
        fit_label = fit.get("fit_label", "N/A")
        label_emoji = {"Excellent": "🟢", "Good": "🟡", "Fair": "🟠", "Poor": "🔴"}.get(fit_label, "⚪")
        print(f"{label_emoji} Fit Score: {fit.get('fit_score', 'N/A')}/100 ({fit_label})")
        print(f"✅ Strengths: {', '.join(fit.get('strengths', [])[:3])}")
        print(f"⚠️  Gaps: {', '.join(fit.get('gaps', ['None identified'])[:3])}")
        print(f"🎯 Recommendation: {fit.get('recommendation', 'N/A')}")
        print(f"💭 {fit.get('recommendation_reason', 'N/A')}")


if __name__ == "__main__":
    main()
