"""
AI Career & Internship Agent using LangGraph + Gemini.

A five-stage multi-agent pipeline that turns a resume and a job description
into a personalized, actionable preparation plan:

    Resume Analyzer ─┐
                     ├─> Matching Agent -> Gap Analysis Agent -> Recommendation Agent
    JD Analyzer ─────┘

The LLM judges evidence (is this requirement met, partially met, or missing?);
the match score and the "missing must-have = blocking" rule are computed in code,
so the score is reproducible from the assessments rather than invented.

Usage:
    python agent.py                                   # built-in sample resume + JD
    python agent.py --resume resume.pdf --job-desc job_posting.txt
    python agent.py --weeks 4 --json                  # 4-week plan, raw JSON output
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Literal, Optional, TypedDict

from dotenv import load_dotenv
from langchain_core.exceptions import (
    ModelAuthenticationError,
    ModelInvalidRequestError,
    ModelNotFoundError,
    ModelRateLimitError,
)
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

load_dotenv()

DEFAULT_MODEL = "gemini-3.6-flash"

# Weights used to turn per-requirement assessments into a 0-100 score.
IMPORTANCE_WEIGHT = {"must-have": 2.0, "nice-to-have": 1.0}
STATUS_CREDIT = {"met": 1.0, "partial": 0.5, "missing": 0.0}


def get_llm() -> ChatGoogleGenerativeAI:
    # No temperature: Gemini 3.x models use fixed sampling defaults and ignore it.
    return ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL", DEFAULT_MODEL))


def ask(schema: type[BaseModel], system: str, user: str) -> BaseModel:
    """Call Gemini and parse the reply straight into a Pydantic model."""
    llm = get_llm().with_structured_output(schema)
    return llm.invoke([SystemMessage(content=system), HumanMessage(content=user)])


def norm(skill: str) -> str:
    """Normalize a skill name for comparison: 'REST APIs' -> 'restapis', 'C#' -> 'c#'."""
    return re.sub(r"[^a-z0-9+#]", "", skill.lower())


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
    skills: list[str] = Field(default_factory=list, description="Short canonical skill names")
    projects: list[Project] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    activities: list[str] = Field(default_factory=list, description="Clubs, hackathons, competitions")


class JobRequirements(BaseModel):
    """Output of the JD Analyzer."""

    title: str
    company: Optional[str] = None
    eligibility: list[str] = Field(default_factory=list, description="Non-skill criteria, e.g. enrollment, dates")
    must_have_skills: list[str] = Field(default_factory=list)
    nice_to_have_skills: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)


class RequirementAssessment(BaseModel):
    skill: str = Field(description="Exactly as given in the requirement list")
    importance: Literal["must-have", "nice-to-have"]
    status: Literal["met", "partial", "missing"]
    evidence: str = Field(description="Quote or paraphrase from the resume, or what is absent")


class MatchAssessment(BaseModel):
    """What the Matching Agent asks the LLM for."""

    assessments: list[RequirementAssessment]
    summary: str = Field(description="2-3 sentences on overall fit, without a numeric score")


class MatchResult(BaseModel):
    """Output of the Matching Agent (score computed in code)."""

    score: int
    assessments: list[RequirementAssessment]
    summary: str


class SkillGap(BaseModel):
    skill: str
    severity: Literal["blocking", "important", "nice-to-have"]
    evidence: str = Field(description="Where in the JD this requirement comes from")
    why_it_matters: str


class GapAnalysis(BaseModel):
    """Output of the Gap Analysis Agent."""

    gaps: list[SkillGap] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list, description="Strengths to lean on in the application")


class WeekPlan(BaseModel):
    week: int
    focus: str
    tasks: list[str]
    resources: list[str] = Field(default_factory=list, description="Named resources, no URLs")


class ProjectIdea(BaseModel):
    title: str
    description: str
    skills_covered: list[str]


class InterviewQuestion(BaseModel):
    question: str
    why_asked: str
    how_to_prepare: str


class Recommendation(BaseModel):
    """Output of the Recommendation Agent."""

    learning_plan: list[WeekPlan]
    project_ideas: list[ProjectIdea]
    resume_improvements: list[str]
    interview_questions: list[InterviewQuestion]


class CareerState(TypedDict, total=False):
    resume_text: str
    job_description: str
    weeks: int
    resume_profile: ResumeProfile
    job_requirements: JobRequirements
    match: MatchResult
    gap_analysis: GapAnalysis
    recommendation: Recommendation


# ---------------------------------------------------------------------------
# Agents (graph nodes)
# ---------------------------------------------------------------------------

RESUME_PROMPT = """You are a career advisor analyzing the resume of a student or early-career applicant.
Extract a structured profile.
- List skills as short canonical names (e.g. "Python", "PostgreSQL", "REST APIs", "Docker").
- Include skills demonstrated in projects, coursework, or activities, not only the skills section.
- Never add anything the resume does not support."""

JD_PROMPT = """You are a technical recruiter analyzing a job description.
Extract its requirements.
- must_have_skills: explicitly required. nice_to_have_skills: preferred, bonus, or "plus".
- Use short canonical skill names (e.g. "Python", "SQL", "REST API design", "Docker").
- Keep alternatives as ONE requirement: "FastAPI or Django", "Cloud (AWS or GCP)". Never split them.
- Put non-skill criteria (degree enrollment, availability, location) in eligibility, not in skills."""

MATCH_PROMPT = """You compare a candidate profile with a list of job requirements.
Assess EVERY requirement in the list, keeping its skill name and importance exactly as given.
- A requirement with alternatives ("X or Y") is met if the candidate has any one of them.
- met: clear evidence in the profile (skills, projects, experience).
- partial: related or shallow evidence (coursework only, an adjacent tool, a basic level).
- missing: no evidence.
Be strict: do not assume skills without evidence. Do not output a numeric score."""

GAP_PROMPT = """You are a career coach. Given the requirements a candidate has not fully met, classify each gap:
- blocking: a must-have that is missing; likely to fail screening.
- important: a must-have that is only partial, or a nice-to-have that matters for this role's core work.
- nice-to-have: everything else.
Explain why each gap matters for THIS role, citing the job description.
Also list 3-5 genuine strengths the candidate should lean on."""

RECOMMEND_PROMPT = """You are a mentor helping a student prepare for a specific internship or job.
Create a personalized, realistic plan to close the gaps before applying and interviewing.
Honesty is non-negotiable: the candidate must never claim a skill, tool, or result they do not have.
- learning_plan: exactly {weeks} weeks, blocking gaps first, roughly 8-10 hours per week.
  Name concrete resources (official docs, well-known free courses), no URLs.
- project_ideas: 2-3 small projects, each finishable in a weekend or two, that close key gaps;
  extend the candidate's existing projects where possible.
- resume_improvements: specific edits that reframe what the candidate ALREADY did to be more relevant
  (quantify results, surface skills they used but undersell, reorder for this role). Anything that depends
  on finishing a project idea must start with "After completing <project title>:".
- interview_questions: 6-8 questions this employer is likely to ask, mixing technical questions on
  gap areas, deep-dives on the candidate's own projects, and behavioral questions. Questions about the
  candidate's projects must describe them as they are on the resume, not as they could be extended."""


def analyze_resume(state: CareerState) -> CareerState:
    """Resume Analyzer: extract a structured, skill-normalized profile."""
    profile = ask(ResumeProfile, RESUME_PROMPT, state["resume_text"])
    return {"resume_profile": profile}


def analyze_job(state: CareerState) -> CareerState:
    """JD Analyzer: split requirements into must-have vs nice-to-have."""
    requirements = ask(JobRequirements, JD_PROMPT, state["job_description"])
    return {"job_requirements": requirements}


def score_assessments(assessments: list[RequirementAssessment]) -> int:
    total = sum(IMPORTANCE_WEIGHT[a.importance] for a in assessments)
    if total == 0:
        return 0
    earned = sum(IMPORTANCE_WEIGHT[a.importance] * STATUS_CREDIT[a.status] for a in assessments)
    return round(100 * earned / total)


def match_skills(state: CareerState) -> CareerState:
    """Matching Agent: the LLM judges evidence per requirement; the score is computed here."""
    jd = state["job_requirements"]
    # De-duplicate so one skill is never scored twice; must-have wins over nice-to-have.
    requirements, seen = [], set()
    for skill, importance in [(s, "must-have") for s in jd.must_have_skills] + [
        (s, "nice-to-have") for s in jd.nice_to_have_skills
    ]:
        if norm(skill) not in seen:
            seen.add(norm(skill))
            requirements.append((skill, importance))
    requirement_list = "\n".join(f"- {skill} ({importance})" for skill, importance in requirements)

    result = ask(
        MatchAssessment,
        MATCH_PROMPT,
        f"Candidate profile:\n{state['resume_profile'].model_dump_json(indent=2)}\n\n"
        f"Requirements:\n{requirement_list}",
    )

    # Keep exactly one assessment per JD requirement: drop extras the LLM invented,
    # and count any requirement it skipped as missing.
    by_skill = {norm(a.skill): a for a in result.assessments}
    assessments = []
    for skill, importance in requirements:
        found = by_skill.get(norm(skill))
        if found:
            assessments.append(found.model_copy(update={"skill": skill, "importance": importance}))
        else:
            assessments.append(RequirementAssessment(
                skill=skill, importance=importance, status="missing", evidence="Not assessed; treated as missing."
            ))

    match = MatchResult(score=score_assessments(assessments), assessments=assessments, summary=result.summary)
    return {"match": match}


def analyze_gaps(state: CareerState) -> CareerState:
    """Gap Analysis Agent: rank missing/partial skills by severity with JD evidence."""
    open_items = [a for a in state["match"].assessments if a.status != "met"]
    if not open_items:
        return {"gap_analysis": GapAnalysis(strengths=["Meets every listed requirement."])}

    jd = state["job_requirements"]
    analysis = ask(
        GapAnalysis,
        GAP_PROMPT,
        f"Role: {jd.title}\nResponsibilities:\n" + "\n".join(f"- {r}" for r in jd.responsibilities)
        + "\n\nUnmet requirements:\n"
        + json.dumps([a.model_dump() for a in open_items], indent=2, ensure_ascii=False)
        + f"\n\nCandidate profile:\n{state['resume_profile'].model_dump_json(indent=2)}",
    )

    # Enforce the one rule that should never depend on the model's judgment.
    status = {norm(a.skill): a for a in open_items}
    gaps = []
    for gap in analysis.gaps:
        item = status.get(norm(gap.skill))
        if item and item.importance == "must-have" and item.status == "missing":
            gap = gap.model_copy(update={"severity": "blocking"})
        gaps.append(gap)
    order = {"blocking": 0, "important": 1, "nice-to-have": 2}
    gaps.sort(key=lambda g: order[g.severity])

    return {"gap_analysis": analysis.model_copy(update={"gaps": gaps})}


def recommend(state: CareerState) -> CareerState:
    """Recommendation Agent: learning plan, project ideas, resume edits, interview prep."""
    weeks = state.get("weeks", 3)
    jd = state["job_requirements"]
    recommendation = ask(
        Recommendation,
        RECOMMEND_PROMPT.format(weeks=weeks),
        f"Target role:\n{jd.model_dump_json(indent=2)}\n\n"
        f"Candidate profile:\n{state['resume_profile'].model_dump_json(indent=2)}\n\n"
        f"Match score: {state['match'].score}/100\n{state['match'].summary}\n\n"
        f"Gap analysis:\n{state['gap_analysis'].model_dump_json(indent=2)}",
    )
    return {"recommendation": recommendation}


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
# Inputs and report
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

STATUS_ICON = {"met": "✅", "partial": "🟡", "missing": "❌"}
SEVERITY_ICON = {"blocking": "🔴", "important": "🟠", "nice-to-have": "🟢"}


def read_text(source: str) -> str:
    """Read a .pdf or text file, or treat the argument itself as raw text."""
    path = Path(source)
    if not path.is_file():
        return source
    if path.suffix.lower() == ".pdf":
        from pypdf import PdfReader

        return "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)
    return path.read_text(encoding="utf-8")


def print_report(result: CareerState) -> None:
    profile, jd = result["resume_profile"], result["job_requirements"]
    match, gaps, rec = result["match"], result["gap_analysis"], result["recommendation"]
    line = "=" * 60

    print(f"\n{line}\n🎯 {profile.name}  →  {jd.title}" + (f" @ {jd.company}" if jd.company else ""))
    print(f"{line}\n\n📊 MATCH SCORE: {match.score}/100\n{match.summary}\n")
    for a in match.assessments:
        print(f"  {STATUS_ICON[a.status]} {a.skill} ({a.importance}): {a.evidence}")

    print(f"\n{line}\n🔍 GAP ANALYSIS\n{line}")
    for g in gaps.gaps:
        print(f"  {SEVERITY_ICON[g.severity]} [{g.severity}] {g.skill}: {g.why_it_matters}")
    if gaps.strengths:
        print("\n  💪 Strengths to lean on:")
        for s in gaps.strengths:
            print(f"   - {s}")

    print(f"\n{line}\n🗺️  LEARNING PLAN\n{line}")
    for w in rec.learning_plan:
        print(f"\n  Week {w.week}: {w.focus}")
        for t in w.tasks:
            print(f"   - {t}")
        if w.resources:
            print(f"   📚 {', '.join(w.resources)}")

    print(f"\n{line}\n🛠️  PROJECT IDEAS\n{line}")
    for p in rec.project_ideas:
        print(f"\n  {p.title} [{', '.join(p.skills_covered)}]\n   {p.description}")

    print(f"\n{line}\n📝 RESUME IMPROVEMENTS\n{line}")
    for r in rec.resume_improvements:
        print(f"  - {r}")

    print(f"\n{line}\n🎤 INTERVIEW PREP\n{line}")
    for i, q in enumerate(rec.interview_questions, 1):
        print(f"\n  {i}. {q.question}\n     Why: {q.why_asked}\n     Prep: {q.how_to_prepare}")
    print()


def main():
    parser = argparse.ArgumentParser(description="AI Career & Internship Agent")
    parser.add_argument("--resume", help="Path to resume (.pdf/.txt) or raw text")
    parser.add_argument("--job-desc", help="Path to job description file or raw text")
    parser.add_argument("--weeks", type=int, default=3, help="Length of the learning plan (default: 3)")
    parser.add_argument("--json", action="store_true", help="Print raw JSON instead of the report")
    args = parser.parse_args()

    # Emoji and Thai text in the report crash non-UTF-8 consoles (e.g. default Windows code pages).
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    state: CareerState = {
        "resume_text": read_text(args.resume) if args.resume else SAMPLE_RESUME,
        "job_description": read_text(args.job_desc) if args.job_desc else SAMPLE_JOB_DESCRIPTION,
        "weeks": args.weeks,
    }

    model = os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
    print(f"🚀 Analyzing with {model}...")
    try:
        result = build_graph().invoke(state)
    except ModelRateLimitError:
        sys.exit(f"❌ Gemini quota exceeded for {model}. The free tier allows about 20 requests/day per model "
                 "(one run uses 5). Wait for the reset or set GEMINI_MODEL to another model in .env.")
    except (ModelAuthenticationError, ModelInvalidRequestError) as e:
        # Google reports a bad key as 400 INVALID_ARGUMENT with reason API_KEY_INVALID.
        if isinstance(e, ModelInvalidRequestError) and "API_KEY_INVALID" not in str(e):
            raise
        sys.exit("❌ Gemini rejected the API key. Check GOOGLE_API_KEY in .env.")
    except ModelNotFoundError:
        sys.exit(f"❌ Model '{model}' not found. Set GEMINI_MODEL in .env to a current Gemini model.")

    if args.json:
        keys = ("resume_profile", "job_requirements", "match", "gap_analysis", "recommendation")
        print(json.dumps({k: result[k].model_dump() for k in keys}, indent=2, ensure_ascii=False))
    else:
        print_report(result)


if __name__ == "__main__":
    main()
