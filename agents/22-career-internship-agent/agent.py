"""
AI Career & Internship Agent using LangGraph.

A five-stage multi-agent pipeline that turns a resume and a job description
into a personalized, actionable preparation plan:

    Resume Analyzer ─┐
                     ├─> Matching Agent -> Gap Analysis Agent -> Recommendation Agent
    JD Analyzer ─────┘

Usage:
    python agent.py                                   # built-in sample resume + JD
    python agent.py --resume resume.pdf --job-desc job_posting.txt
"""

import argparse
import json
from pathlib import Path
from typing import Literal, Optional, TypedDict

from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

load_dotenv()


# ---------------------------------------------------------------------------
# Structured outputs, one per stage
# ---------------------------------------------------------------------------


class Project(BaseModel):
    name: str
    description: str
    skills_used: list[str] = Field(default_factory=list)


class ResumeProfile(BaseModel):
    """Output of the Resume Analyzer."""

    name: str
    education: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list, description="Normalized skill names")
    projects: list[Project] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    activities: list[str] = Field(default_factory=list, description="Clubs, hackathons, competitions")


class JobRequirements(BaseModel):
    """Output of the JD Analyzer."""

    title: str
    company: Optional[str] = None
    must_have_skills: list[str] = Field(default_factory=list)
    nice_to_have_skills: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)


class MatchResult(BaseModel):
    """Output of the Matching Agent."""

    matched_must_have: list[str] = Field(default_factory=list)
    matched_nice_to_have: list[str] = Field(default_factory=list)
    missing_must_have: list[str] = Field(default_factory=list)
    missing_nice_to_have: list[str] = Field(default_factory=list)
    score: int = Field(ge=0, le=100, description="Weighted skill coverage")
    explanation: str = ""


class SkillGap(BaseModel):
    skill: str
    severity: Literal["blocking", "important", "nice-to-have"]
    evidence: str = Field(description="Where in the JD this requirement comes from")
    why_it_matters: str


class GapAnalysis(BaseModel):
    """Output of the Gap Analysis Agent."""

    gaps: list[SkillGap] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)


class Recommendation(BaseModel):
    """Output of the Recommendation Agent."""

    learning_plan: list[str] = Field(default_factory=list, description="Week-by-week, 2-4 weeks")
    project_ideas: list[str] = Field(default_factory=list, description="One small project per key gap")
    resume_improvements: list[str] = Field(default_factory=list)
    interview_questions: list[str] = Field(default_factory=list, description="Targeted at weak spots")


class CareerState(TypedDict, total=False):
    resume_text: str
    job_description: str
    resume_profile: ResumeProfile
    job_requirements: JobRequirements
    match: MatchResult
    gap_analysis: GapAnalysis
    recommendation: Recommendation


# ---------------------------------------------------------------------------
# Agents (graph nodes)
# ---------------------------------------------------------------------------


def analyze_resume(state: CareerState) -> CareerState:
    """Resume Analyzer: extract a structured, skill-normalized profile."""
    raise NotImplementedError("Resume Analyzer not implemented yet")


def analyze_job(state: CareerState) -> CareerState:
    """JD Analyzer: split requirements into must-have vs nice-to-have."""
    raise NotImplementedError("JD Analyzer not implemented yet")


def match_skills(state: CareerState) -> CareerState:
    """Matching Agent: compute skill coverage; the LLM explains, not invents, the score."""
    raise NotImplementedError("Matching Agent not implemented yet")


def analyze_gaps(state: CareerState) -> CareerState:
    """Gap Analysis Agent: rank missing skills by severity with JD evidence."""
    raise NotImplementedError("Gap Analysis Agent not implemented yet")


def recommend(state: CareerState) -> CareerState:
    """Recommendation Agent: learning plan, project ideas, interview prep."""
    raise NotImplementedError("Recommendation Agent not implemented yet")


def build_graph():
    graph = StateGraph(CareerState)
    graph.add_node("resume_analyzer", analyze_resume)
    graph.add_node("jd_analyzer", analyze_job)
    graph.add_node("matcher", match_skills)
    graph.add_node("gap_analyzer", analyze_gaps)
    graph.add_node("recommender", recommend)

    # Resume and JD are analyzed in parallel, then joined at the matcher.
    graph.add_edge(START, "resume_analyzer")
    graph.add_edge(START, "jd_analyzer")
    graph.add_edge(["resume_analyzer", "jd_analyzer"], "matcher")
    graph.add_edge("matcher", "gap_analyzer")
    graph.add_edge("gap_analyzer", "recommender")
    graph.add_edge("recommender", END)
    return graph.compile()


# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------

SAMPLE_RESUME = """
Ploy Srisuk
B.Eng. Computer Engineering (Year 3), Chulalongkorn University — GPA 3.42

Skills: Python, Java, SQL, Git, HTML/CSS, basic React, pandas

Projects
- Campus Food Finder: React + Firebase web app to browse canteen menus (team of 3)
- Thai News Classifier: scikit-learn model classifying news headlines into 6 topics, 84% accuracy
- Data Structures coursework: implemented AVL tree and graph algorithms in Java

Activities
- Staff, CU Hackathon 2026
- Member, Google Developer Student Club
"""

SAMPLE_JOB_DESCRIPTION = """
Software Engineer Intern (Backend) — FinTech startup, Bangkok
Duration: 3 months, summer 2027

Responsibilities
- Build and maintain REST APIs for our payments platform
- Write unit and integration tests
- Work with the team on code reviews and deployments

Requirements
- Currently pursuing a degree in Computer Science/Engineering
- Strong Python skills
- Experience with SQL databases
- Familiarity with REST API design
- Git and collaborative development

Nice to have
- FastAPI or Django
- Docker
- Cloud experience (AWS/GCP)
- Interest in finance or payments
"""


def read_text(source: str) -> str:
    """Read a .pdf or text file, or treat the argument itself as raw text."""
    path = Path(source)
    if not path.is_file():
        return source
    if path.suffix.lower() == ".pdf":
        from pypdf import PdfReader

        return "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)
    return path.read_text(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="AI Career & Internship Agent")
    parser.add_argument("--resume", help="Path to resume (.pdf/.txt) or raw text")
    parser.add_argument("--job-desc", help="Path to job description file or raw text")
    args = parser.parse_args()

    state: CareerState = {
        "resume_text": read_text(args.resume) if args.resume else SAMPLE_RESUME,
        "job_description": read_text(args.job_desc) if args.job_desc else SAMPLE_JOB_DESCRIPTION,
    }

    result = build_graph().invoke(state)

    for key in ("match", "gap_analysis", "recommendation"):
        print(f"\n{'=' * 60}\n{key.replace('_', ' ').upper()}\n{'=' * 60}")
        print(json.dumps(result[key].model_dump(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
