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
import heapq
import json
import math
import os
import random
import re
import statistics
import sys
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from pathlib import Path
from typing import Literal, Optional, TypedDict
from unittest import mock

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


def dedupe_requirements(must_have: list[str], nice_to_have: list[str]) -> list[tuple[str, str]]:
    """One (skill, importance) per requirement, so no skill is scored twice; must-have wins."""
    requirements, seen = [], set()
    for skill, importance in [(s, "must-have") for s in must_have] + [(s, "nice-to-have") for s in nice_to_have]:
        if norm(skill) and norm(skill) not in seen:
            seen.add(norm(skill))
            requirements.append((skill, importance))
    return requirements


def match_skills(state: CareerState) -> CareerState:
    """Matching Agent: the LLM judges evidence per requirement; the score is computed here."""
    jd = state["job_requirements"]
    requirements = dedupe_requirements(jd.must_have_skills, jd.nice_to_have_skills)
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
# Job search: rank a whole catalog of postings against one set of skills
# ---------------------------------------------------------------------------
#
# Running the Matching Agent on every posting would cost one LLM call per job, so
# job search ranks the catalog with a deterministic matcher on the same
# met / partial / missing scale and weights, then can re-check the top few with
# the Matching Agent (--rerank). The matcher knows three kinds of relationship:
#   ALIASES  different spellings of one skill       Postgres == PostgreSQL
#   IMPLIES  having A demonstrates B                PostgreSQL -> SQL (met)
#   FAMILIES interchangeable-ish tools              MySQL ~ PostgreSQL (partial)

# Keys and values are norm()-ed names.
ALIASES = {
    "postgres": "postgresql", "psql": "postgresql", "mssql": "sqlserver", "mongo": "mongodb",
    "js": "javascript", "es6": "javascript", "ts": "typescript", "reactjs": "react", "vuejs": "vue",
    "angularjs": "angular", "node": "nodejs", "expressjs": "express", "html": "htmlcss", "css": "htmlcss",
    "html5": "htmlcss", "css3": "htmlcss", "golang": "go", "csharp": "c#", "cpp": "c++",
    "sklearn": "scikitlearn", "ml": "machinelearning", "dl": "deeplearning", "naturallanguageprocessing": "nlp",
    "github": "git", "gitlab": "git", "bitbucket": "git",
    "rest": "restapi", "restapis": "restapi", "restapidesign": "restapi", "restful": "restapi",
    "restfulapi": "restapi", "restfulapis": "restapi",
    "amazonwebservices": "aws", "googlecloud": "gcp", "googlecloudplatform": "gcp", "microsoftazure": "azure",
    "k8s": "kubernetes", "ci": "cicd", "continuousintegration": "cicd", "shell": "bash", "shellscripting": "bash",
    "unix": "linux", "msexcel": "excel", "microsoftexcel": "excel", "stats": "statistics",
    "testing": "softwaretesting", "unittesting": "softwaretesting", "testautomation": "softwaretesting",
    "automatedtesting": "softwaretesting", "qa": "softwaretesting",
    "android": "androidsdk", "ios": "iossdk", "xcode": "iossdk", "compose": "jetpackcompose",
    "arduino": "microcontrollers", "stm32": "microcontrollers", "esp32": "microcontrollers",
    "microcontroller": "microcontrollers", "freertos": "rtos", "pcb": "pcbdesign",
    "uiux": "uidesign", "uiuxdesign": "uidesign", "uxuidesign": "uidesign", "uxresearch": "userresearch",
    "networks": "networking", "computernetworking": "networking", "tcpip": "networking",
    "pentest": "penetrationtesting", "pentesting": "penetrationtesting",
    "apachespark": "spark", "pyspark": "spark", "apacheairflow": "airflow", "unity3d": "unity",
}

IMPLIES = {
    **{db: ["sql"] for db in ("postgresql", "mysql", "sqlite", "sqlserver", "oracle", "mariadb")},
    "django": ["python"], "flask": ["python"], "fastapi": ["python", "restapi"],
    "pandas": ["python"], "numpy": ["python"], "scikitlearn": ["python", "machinelearning"],
    **{dl: ["python", "deeplearning"] for dl in ("pytorch", "tensorflow", "keras")},
    "deeplearning": ["machinelearning"], "nlp": ["machinelearning"],
    "react": ["javascript"], "vue": ["javascript"], "svelte": ["javascript"], "angular": ["typescript"],
    "nextjs": ["react"], "typescript": ["javascript"], "nodejs": ["javascript"], "express": ["nodejs"],
    "aws": ["cloud"], "gcp": ["cloud"], "azure": ["cloud"],
    "jetpackcompose": ["androidsdk"], "swiftui": ["swift", "iossdk"],
    "selenium": ["softwaretesting"], "playwright": ["softwaretesting"], "pytest": ["softwaretesting", "python"],
    "junit": ["softwaretesting", "java"], "cypress": ["softwaretesting", "javascript"],
    "githubactions": ["cicd"], "jenkins": ["cicd"], "gitlabci": ["cicd"],
    "airflow": ["etl"], "spark": ["etl"], "dbt": ["etl", "sql"], "rtos": ["microcontrollers"],
}

FAMILIES = [
    {"postgresql", "mysql", "sqlite", "sqlserver", "oracle", "mariadb"},
    {"mongodb", "firebase", "dynamodb"},
    {"django", "fastapi", "flask"},
    {"react", "vue", "angular", "svelte"},
    {"aws", "gcp", "azure"},
    {"pytorch", "tensorflow", "keras", "jax"},
    {"java", "kotlin", "scala"},
    {"c", "c++"},
    {"docker", "kubernetes"},
    {"tableau", "powerbi", "looker"},
    {"selenium", "cypress", "playwright"},
    {"unity", "unreal", "godot"},
]
SIBLINGS: dict[str, set[str]] = {}
for _family in FAMILIES:
    for _skill in _family:
        SIBLINGS.setdefault(_skill, set()).update(_family - {_skill})

KNOWN_SKILLS = (set(ALIASES.values()) | set(IMPLIES) | set(SIBLINGS)
                | {s for implied in IMPLIES.values() for s in implied})

# Filler words recruiters wrap around skill names: "Strong Python skills" -> "python".
FILLER = {"strong", "solid", "basic", "good", "experience", "experienced", "with", "in", "of", "familiarity",
          "familiar", "knowledge", "proficiency", "proficient", "understanding", "skills", "skill",
          "development", "programming", "language", "databases", "database", "framework"}

STATUS_RANK = {"met": 2, "partial": 1, "missing": 0}


@lru_cache(maxsize=None)
def canon(skill: str) -> str:
    """Canonical skill key: 'Strong Python skills' -> 'python', 'Postgres' -> 'postgresql'."""
    words = [w for w in skill.lower().split() if w not in FILLER]
    key = norm(" ".join(words)) or norm(skill)
    return ALIASES.get(key, key)


@lru_cache(maxsize=None)
def alternatives(requirement: str) -> tuple[str, ...]:
    """Canonical skills that each satisfy a requirement.

    'FastAPI or Django' -> (fastapi, django); 'Cloud (AWS/GCP)' -> (cloud, aws, gcp);
    'CI/CD' and 'HTML/CSS' stay one skill because they are known names.
    """
    whole = canon(requirement)
    if whole in KNOWN_SKILLS:
        return (whole,)
    parts = []
    m = re.fullmatch(r"(.*?)\((.+)\)\s*", requirement)
    if m:
        outer = canon(m.group(1))
        if outer in KNOWN_SKILLS:
            parts.append(outer)
        body = m.group(2)
    else:
        body = requirement
    parts += [canon(p) for p in re.split(r"\s+or\s+|/|,|\|", body, flags=re.IGNORECASE)]
    return tuple(dict.fromkeys(p for p in parts if p)) or (whole,)


class SkillMatcher:
    """Judges requirements against one candidate's skills, caching each verdict."""

    def __init__(self, skills: list[str]):
        # Map every skill the candidate demonstrates to the listed skill that shows it.
        # Listed skills go in first, so an inferred skill never hides a listed one.
        self.has: dict[str, str] = {}
        for s in skills:
            if canon(s):
                self.has.setdefault(canon(s), s.strip())
        self.listed = set(self.has)
        stack = list(self.has.items())
        while stack:
            skill, source = stack.pop()
            for implied in IMPLIES.get(skill, ()):
                if implied not in self.has:
                    self.has[implied] = source
                    stack.append((implied, source))
        self._cache: dict[tuple[str, ...], tuple[str, str]] = {}

    def _judge_one(self, skill: str) -> tuple[str, str]:
        if skill in self.has:
            implied = "" if skill in self.listed else ", which implies it"
            return "met", f"Lists {self.has[skill]}{implied}"
        for sibling in sorted(SIBLINGS.get(skill, ())):
            if sibling in self.has:
                return "partial", f"Related skill: {self.has[sibling]}"
        return "missing", "No matching or related skill listed"

    def judge(self, alts: tuple[str, ...]) -> tuple[str, str]:
        """(status, evidence) for a requirement; any one alternative is enough."""
        if alts not in self._cache:
            self._cache[alts] = max((self._judge_one(a) for a in alts), key=lambda v: STATUS_RANK[v[0]])
        return self._cache[alts]


class JobPosting(BaseModel):
    id: str
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    must_have_skills: list[str] = Field(default_factory=list)
    nice_to_have_skills: list[str] = Field(default_factory=list)


class JobMatch(BaseModel):
    job: JobPosting
    score: int = Field(description="Quick skill-match score from the deterministic matcher")
    missing_must_haves: list[str]
    assessments: list[RequirementAssessment]
    llm_score: Optional[int] = Field(default=None, description="Matching Agent score, when re-ranked")
    llm_summary: Optional[str] = None


class JobIndex:
    """A job catalog with requirements parsed once, so each search is a cheap scan."""

    def __init__(self, jobs: list[JobPosting]):
        self.jobs = jobs
        self._requirements = [
            [(skill, importance, alternatives(skill))
             for skill, importance in dedupe_requirements(job.must_have_skills, job.nice_to_have_skills)]
            for job in jobs
        ]
        # Scoring view of the same data: (total weight, [(alternatives, weight, is_must_have)]).
        self._scoring = [
            (sum(IMPORTANCE_WEIGHT[imp] for _, imp, _ in reqs),
             [(alts, IMPORTANCE_WEIGHT[imp], imp == "must-have") for _, imp, alts in reqs])
            for reqs in self._requirements
        ]

    def rank(self, skills: list[str], top: Optional[int] = 5) -> list[JobMatch]:
        """Best-fitting jobs first; ties go to fewer missing must-haves, then catalog order."""
        matcher = SkillMatcher(skills)
        keys = []
        for i, (total, requirements) in enumerate(self._scoring):
            earned = 0.0
            missing_must = 0
            for alts, weight, is_must in requirements:
                status = matcher.judge(alts)[0]
                earned += weight * STATUS_CREDIT[status]
                missing_must += is_must and status == "missing"
            keys.append((-(round(100 * earned / total) if total else 0), missing_must, i))
        best = heapq.nsmallest(top, keys) if top is not None else sorted(keys)
        # Pydantic objects are built only for the jobs returned: on large catalogs, building
        # them for every requirement of every job would dominate the search time.
        return [self._explain(i, matcher) for _, _, i in best]

    def _explain(self, i: int, matcher: SkillMatcher) -> JobMatch:
        assessments = []
        for skill, importance, alts in self._requirements[i]:
            status, evidence = matcher.judge(alts)
            assessments.append(RequirementAssessment(skill=skill, importance=importance, status=status,
                                                     evidence=evidence))
        return JobMatch(
            job=self.jobs[i],
            score=score_assessments(assessments),
            missing_must_haves=[a.skill for a in assessments if a.importance == "must-have" and a.status == "missing"],
            assessments=assessments,
        )


def rerank_with_llm(matches: list[JobMatch], profile: ResumeProfile, workers: int = 4) -> list[JobMatch]:
    """Re-check matches with the Matching Agent (one LLM call each, run in parallel)."""

    def check(m: JobMatch) -> JobMatch:
        jd = JobRequirements(title=m.job.title, company=m.job.company,
                             must_have_skills=m.job.must_have_skills, nice_to_have_skills=m.job.nice_to_have_skills)
        llm = match_skills({"resume_profile": profile, "job_requirements": jd})["match"]
        missing = [a.skill for a in llm.assessments if a.importance == "must-have" and a.status == "missing"]
        return m.model_copy(update={"llm_score": llm.score, "llm_summary": llm.summary,
                                    "assessments": llm.assessments, "missing_must_haves": missing})

    with ThreadPoolExecutor(max_workers=max(1, min(workers, len(matches)))) as pool:
        checked = list(pool.map(check, matches))
    return sorted(checked, key=lambda m: (-m.llm_score, -m.score))


def find_jobs(skills: list[str], jobs: list[JobPosting], top: int = 5, rerank: int = 0,
              profile: Optional[ResumeProfile] = None, timings: Optional[dict] = None) -> list[JobMatch]:
    """Rank jobs by skill fit; with rerank > 0, the top `rerank` are re-checked by the LLM.

    Pass a dict as `timings` to get the time spent in each stage (ms).
    """
    timings = {} if timings is None else timings
    start = time.perf_counter()
    matches = JobIndex(jobs).rank(skills, top=max(top, rerank))
    timings["rank_ms"] = (time.perf_counter() - start) * 1000
    if rerank and matches:
        start = time.perf_counter()
        profile = profile or ResumeProfile(name="Candidate", skills=skills)
        matches = rerank_with_llm(matches[:rerank], profile) + matches[rerank:]
        timings["rerank_ms"] = (time.perf_counter() - start) * 1000
        timings["reranked"] = min(rerank, len(matches))
    return matches[:top]


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

# Skills listed on SAMPLE_RESUME, used by --find-jobs when no --skills or --resume is given.
SAMPLE_SKILLS = ["Python", "Java", "SQL", "Git", "HTML/CSS", "React", "pandas", "scikit-learn", "Firebase"]


def _job(id, title, company, location, must, nice):
    return JobPosting(id=id, title=title, company=company, location=location,
                      must_have_skills=must, nice_to_have_skills=nice)


# Built-in catalog of fictional internship postings (Thailand), already in structured form.
SAMPLE_JOBS = [
    _job("backend-fintech", "Software Engineer Intern (Backend)", "FinTech startup", "Bangkok",
         ["Python", "SQL", "REST API design", "Git"], ["FastAPI or Django", "Docker", "Cloud (AWS/GCP)"]),
    _job("frontend-ecommerce", "Frontend Developer Intern", "E-commerce platform", "Bangkok",
         ["JavaScript", "React", "HTML/CSS", "Git"], ["TypeScript", "Next.js", "Figma"]),
    _job("data-analyst", "Data Analyst Intern", "Retail group", "Bangkok",
         ["SQL", "Excel", "Python"], ["Tableau or Power BI", "pandas", "Statistics"]),
    _job("ml-engineer", "Machine Learning Engineer Intern", "AI research lab", "Bangkok",
         ["Python", "Machine Learning", "PyTorch or TensorFlow"], ["NLP", "Docker", "Linux"]),
    _job("android", "Android Developer Intern", "Food delivery app", "Bangkok",
         ["Kotlin or Java", "Android SDK", "Git"], ["Jetpack Compose", "Firebase", "REST APIs"]),
    _job("ios", "iOS Developer Intern", "Travel booking app", "Chiang Mai",
         ["Swift", "iOS SDK", "Git"], ["SwiftUI", "Firebase"]),
    _job("devops", "DevOps / Cloud Intern", "Telecom company", "Bangkok",
         ["Linux", "Docker", "Bash", "Git"], ["Kubernetes", "AWS", "Terraform", "CI/CD"]),
    _job("qa-automation", "QA Automation Intern", "Banking software vendor", "Bangkok",
         ["Python or Java", "Software testing", "Git"], ["Selenium", "CI/CD", "SQL"]),
    _job("embedded", "Embedded Systems Intern", "Electronics manufacturer", "Chonburi",
         ["C", "C++", "Microcontrollers"], ["RTOS", "Python", "PCB design"]),
    _job("ux-ui", "UX/UI Design Intern", "Digital agency", "Remote",
         ["Figma", "UI design", "User research"], ["HTML/CSS", "Prototyping"]),
    _job("fullstack", "Full-stack Developer Intern", "SaaS startup", "Remote",
         ["JavaScript", "Node.js", "React", "SQL"], ["TypeScript", "Docker", "MongoDB"]),
    _job("data-engineer", "Data Engineering Intern", "Logistics company", "Bangkok",
         ["Python", "SQL", "ETL"], ["Apache Spark", "Airflow", "Cloud (AWS/GCP)"]),
    _job("security", "Cybersecurity Intern", "Managed security provider", "Bangkok",
         ["Networking", "Linux", "Python"], ["Penetration testing", "Wireshark"]),
    _job("game-dev", "Game Developer Intern", "Indie game studio", "Bangkok",
         ["C#", "Unity"], ["Blender", "C++"]),
]

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


def load_jobs(path: str) -> list[JobPosting]:
    """Read postings from a JSON list. Each one needs a title and skill lists, or a raw
    "description" that the JD Analyzer turns into skills (one LLM call per such posting)."""
    jobs = []
    for i, item in enumerate(json.loads(Path(path).read_text(encoding="utf-8")), 1):
        item = {**item, "id": str(item.get("id", f"job-{i}"))}
        if not (item.get("must_have_skills") or item.get("nice_to_have_skills")) and item.get("description"):
            jd = analyze_job({"job_description": item["description"]})["job_requirements"]
            item.update(title=item.get("title") or jd.title, company=item.get("company") or jd.company,
                        must_have_skills=jd.must_have_skills, nice_to_have_skills=jd.nice_to_have_skills)
        jobs.append(JobPosting.model_validate({k: v for k, v in item.items() if k in JobPosting.model_fields}))
    return jobs


def print_job_matches(matches: list[JobMatch], n_jobs: int, skills: list[str], timings: dict) -> None:
    line = "=" * 60
    print(f"\n{line}\n🔎 Top {len(matches)} of {n_jobs} jobs for: {', '.join(skills)}\n{line}")
    for rank, m in enumerate(matches, 1):
        where = " · ".join(x for x in (m.job.company, m.job.location) if x)
        score = f"{m.score}/100" if m.llm_score is None else f"{m.llm_score}/100 (LLM re-check; quick score {m.score})"
        print(f"\n {rank}. {m.job.title}" + (f" — {where}" if where else "") + f"\n    📊 {score}")
        print("    " + "  ".join(f"{STATUS_ICON[a.status]} {a.skill}" for a in m.assessments))
        if m.missing_must_haves:
            print(f"    ⚠️  Missing must-haves: {', '.join(m.missing_must_haves)}")
        if m.llm_summary:
            print(f"    💬 {m.llm_summary}")
    timing = f"Ranked {n_jobs} jobs in {timings['rank_ms']:.1f} ms"
    if "rerank_ms" in timings:
        timing += f"; LLM re-check of the top {timings['reranked']} took {timings['rerank_ms'] / 1000:.1f} s"
    print(f"\n⏱️  {timing}.\n")


# ---------------------------------------------------------------------------
# Accuracy evaluation (--eval), benchmark (--bench) and self-tests (--self-test)
# None of these call the LLM, so they run without an API key.
# ---------------------------------------------------------------------------

# Requirement level: (candidate skills, requirement, status a careful human reviewer would give).
# The last three are out-of-vocabulary for the matcher and are kept on purpose, so the score
# shows the limit of a table-driven matcher (that is what --rerank is for).
REQUIREMENT_CASES = [
    (["Python"], "Strong Python skills", "met"),
    (["Postgres"], "PostgreSQL", "met"),
    (["PostgreSQL"], "Experience with SQL databases", "met"),
    (["MySQL"], "PostgreSQL", "partial"),
    (["Django"], "FastAPI or Django", "met"),
    (["Flask"], "FastAPI or Django", "partial"),
    (["AWS"], "Cloud (AWS/GCP)", "met"),
    (["Azure"], "Cloud (AWS/GCP)", "met"),
    (["Azure"], "AWS or GCP", "partial"),
    (["ReactJS"], "React", "met"),
    (["Next.js"], "JavaScript", "met"),
    (["TypeScript"], "JavaScript", "met"),
    (["Java"], "Kotlin or Java", "met"),
    (["Kotlin"], "Java", "partial"),
    (["Python"], "Java", "missing"),
    (["Java"], "JavaScript", "missing"),
    (["scikit-learn"], "Machine Learning", "met"),
    (["PyTorch"], "PyTorch or TensorFlow", "met"),
    (["Keras"], "TensorFlow", "partial"),
    (["C++"], "C", "partial"),
    (["C"], "C#", "missing"),
    (["C++"], "C/C++", "met"),
    (["Docker"], "Kubernetes", "partial"),
    (["GitHub"], "Git", "met"),
    (["Selenium"], "Software testing", "met"),
    (["pytest"], "Unit testing", "met"),
    (["Excel"], "Power BI", "missing"),
    (["Tableau"], "Tableau or Power BI", "met"),
    (["HTML", "CSS"], "HTML/CSS", "met"),
    (["Node"], "Node.js", "met"),
    (["REST APIs"], "REST API design", "met"),
    (["Jetpack Compose"], "Android SDK", "met"),
    (["GitHub Actions"], "CI/CD", "met"),
    (["Arduino"], "Microcontrollers", "met"),
    (["SQL"], "NoSQL", "missing"),
    (["Go"], "Google Cloud", "missing"),
    (["React"], "React Native", "partial"),
    (["Spring Boot"], "Java", "met"),
    (["MongoDB"], "NoSQL databases", "met"),
]

# Ranking level: candidate skills and how well each SAMPLE_JOBS posting fits them, judged by hand:
# 2 = strong fit (apply now), 1 = stretch (worth applying after some prep), unlisted = 0 (poor fit).
EVAL_CANDIDATES = {
    "backend": (["Python", "Django", "PostgreSQL", "Git", "REST APIs", "Docker", "Linux"],
                {"backend-fintech": 2, "data-engineer": 1, "devops": 1, "qa-automation": 1,
                 "data-analyst": 1, "security": 1, "fullstack": 1}),
    "frontend": (["JavaScript", "TypeScript", "React", "Next.js", "HTML/CSS", "Figma", "Git"],
                 {"frontend-ecommerce": 2, "fullstack": 1, "ux-ui": 1}),
    "data-ml": (["Python", "pandas", "NumPy", "scikit-learn", "PyTorch", "SQL", "Statistics", "Jupyter"],
                {"ml-engineer": 2, "data-analyst": 2, "data-engineer": 1, "backend-fintech": 1}),
    "mobile": (["Kotlin", "Java", "Android SDK", "Jetpack Compose", "Firebase", "Git"],
               {"android": 2, "ios": 1, "qa-automation": 1}),
    "devops": (["Linux", "Bash", "Docker", "Kubernetes", "AWS", "Terraform", "Git", "Python", "GitHub Actions"],
               {"devops": 2, "backend-fintech": 1, "data-engineer": 1, "security": 1, "qa-automation": 1}),
    "embedded": (["C", "C++", "Arduino", "FreeRTOS", "Python", "PCB design"], {"embedded": 2}),
    "designer": (["Figma", "UI/UX design", "User research", "Prototyping", "HTML", "CSS"],
                 {"ux-ui": 2, "frontend-ecommerce": 1}),
    "game": (["C#", "Unity", "Blender", "C++", "Git"], {"game-dev": 2}),
    "sample-resume": (SAMPLE_SKILLS,
                      {"backend-fintech": 2, "data-analyst": 1, "qa-automation": 1, "frontend-ecommerce": 1,
                       "fullstack": 1, "ml-engineer": 1, "android": 1, "data-engineer": 1}),
}


def baseline_rank(jobs: list[JobPosting], skills: list[str]) -> list[str]:
    """Exact-name overlap with the same weights: the matcher minus aliases, implications, families."""
    have = {s.strip().lower() for s in skills}

    def score(job: JobPosting) -> float:
        reqs = dedupe_requirements(job.must_have_skills, job.nice_to_have_skills)
        total = sum(IMPORTANCE_WEIGHT[imp] for _, imp in reqs)
        return sum(IMPORTANCE_WEIGHT[imp] for s, imp in reqs if s.strip().lower() in have) / total if total else 0.0

    return [job.id for job in sorted(jobs, key=score, reverse=True)]


def ranking_metrics(ranked: list[str], labels: dict[str, int], k: int = 5) -> dict[str, float]:
    """Top-1 (best result is a strong fit), MRR of the first strong fit, NDCG@k, Recall@k of any fit."""
    first_strong = next((r for r, job in enumerate(ranked, 1) if labels.get(job) == 2), None)
    dcg = sum((2 ** labels.get(job, 0) - 1) / math.log2(r + 2) for r, job in enumerate(ranked[:k]))
    ideal = sum((2 ** g - 1) / math.log2(r + 2) for r, g in enumerate(sorted(labels.values(), reverse=True)[:k]))
    relevant = {job for job, g in labels.items() if g >= 1}
    return {
        "Top-1": float(labels.get(ranked[0]) == 2),
        "MRR": 1 / first_strong if first_strong else 0.0,
        f"NDCG@{k}": dcg / ideal if ideal else 0.0,
        f"Recall@{k}": len(relevant & set(ranked[:k])) / len(relevant) if relevant else 1.0,
    }


def evaluate(jobs: list[JobPosting] = SAMPLE_JOBS) -> dict:
    """Score the matcher (and an exact-name baseline) against the hand labels."""
    misses, baseline_correct = [], 0
    for skills, requirement, expected in REQUIREMENT_CASES:
        got = SkillMatcher(skills).judge(alternatives(requirement))[0]
        if got != expected:
            misses.append((skills, requirement, expected, got))
        exact = "met" if requirement.strip().lower() in {s.strip().lower() for s in skills} else "missing"
        baseline_correct += exact == expected

    index = JobIndex(jobs)
    per_candidate, matcher_rows, baseline_rows = {}, [], []
    for name, (skills, labels) in EVAL_CANDIDATES.items():
        ranked = [m.job.id for m in index.rank(skills, top=None)]
        matcher_rows.append(ranking_metrics(ranked, labels))
        baseline_rows.append(ranking_metrics(baseline_rank(jobs, skills), labels))
        per_candidate[name] = {"top3": ranked[:3], **matcher_rows[-1]}

    def mean(rows):
        return {metric: statistics.mean(row[metric] for row in rows) for metric in rows[0]}

    n = len(REQUIREMENT_CASES)
    return {
        "requirement_accuracy": (n - len(misses)) / n,
        "baseline_requirement_accuracy": baseline_correct / n,
        "requirement_cases": n,
        "misses": misses,
        "ranking": {"matcher": mean(matcher_rows), "baseline": mean(baseline_rows)},
        "per_candidate": per_candidate,
    }


def print_eval(report: dict) -> None:
    line = "=" * 60
    print(f"\n{line}\n📏 REQUIREMENT ACCURACY ({report['requirement_cases']} hand-labeled cases)\n{line}")
    print(f"  matcher {report['requirement_accuracy']:6.1%}    "
          f"baseline (exact name) {report['baseline_requirement_accuracy']:6.1%}")
    for skills, requirement, expected, got in report["misses"]:
        print(f"  ✗ {', '.join(skills)} vs '{requirement}': expected {expected}, got {got}")

    print(f"\n{line}\n📏 RANKING QUALITY ({len(report['per_candidate'])} candidates × {len(SAMPLE_JOBS)} jobs)\n{line}")
    matcher, baseline = report["ranking"]["matcher"], report["ranking"]["baseline"]
    print(f"  {'metric':<10}{'matcher':>9}{'baseline':>10}")
    for metric in matcher:
        print(f"  {metric:<10}{matcher[metric]:>9.2f}{baseline[metric]:>10.2f}")
    print()
    for name, row in report["per_candidate"].items():
        print(f"  {name:<14} NDCG@5 {row['NDCG@5']:.2f}  top 3: {', '.join(row['top3'])}")
    print()


def synthetic_catalog(n: int, seed: int = 7) -> list[JobPosting]:
    """n random postings drawn from the skills used in SAMPLE_JOBS, ~15% with 'X or Y' requirements."""
    rng = random.Random(seed)
    vocab = sorted({s for job in SAMPLE_JOBS for s in job.must_have_skills + job.nice_to_have_skills})

    def requirement() -> str:
        return f"{rng.choice(vocab)} or {rng.choice(vocab)}" if rng.random() < 0.15 else rng.choice(vocab)

    return [JobPosting(id=f"job-{i}", title=f"Synthetic job {i}",
                       must_have_skills=[requirement() for _ in range(rng.randint(2, 5))],
                       nice_to_have_skills=[requirement() for _ in range(rng.randint(1, 4))])
            for i in range(n)]


def benchmark(sizes=(1_000, 10_000, 50_000), queries: int = 30, top: int = 10, seed: int = 7) -> list[dict]:
    """Index build time and per-search latency on synthetic catalogs; each search uses new skills."""
    rng = random.Random(seed)
    vocab = sorted({s for job in SAMPLE_JOBS for s in job.must_have_skills + job.nice_to_have_skills})
    results = []
    for n in sizes:
        catalog = synthetic_catalog(n, seed)
        canon.cache_clear()
        alternatives.cache_clear()
        start = time.perf_counter()
        index = JobIndex(catalog)
        build_ms = (time.perf_counter() - start) * 1000
        latencies = []
        for _ in range(queries):
            skills = rng.sample(vocab, rng.randint(4, 10))
            start = time.perf_counter()
            index.rank(skills, top=top)
            latencies.append((time.perf_counter() - start) * 1000)
        results.append({
            "jobs": n, "build_ms": build_ms,
            "p50_ms": statistics.median(latencies),
            "p95_ms": statistics.quantiles(latencies, n=20)[18],
            "jobs_per_sec": n / (statistics.mean(latencies) / 1000),
        })
    return results


def print_benchmark(results: list[dict]) -> None:
    line = "=" * 60
    print(f"\n{line}\n⚡ JOB SEARCH BENCHMARK (synthetic catalogs, top 10)\n{line}")
    print(f"  {'jobs':>8}{'index build':>14}{'search p50':>13}{'search p95':>13}{'jobs/sec':>12}")
    for r in results:
        print(f"  {r['jobs']:>8,}{r['build_ms']:>11.0f} ms{r['p50_ms']:>10.1f} ms{r['p95_ms']:>10.1f} ms"
              f"{r['jobs_per_sec']:>12,.0f}")
    print(f"\n  For comparison: the LLM Matching Agent on every job would take "
          f"{results[-1]['jobs']:,} API calls for one search.\n")


class TestSkillMatcher(unittest.TestCase):
    def test_alternatives(self):
        self.assertEqual(alternatives("Cloud (AWS/GCP)"), ("cloud", "aws", "gcp"))
        self.assertEqual(alternatives("Tableau or Power BI"), ("tableau", "powerbi"))
        self.assertEqual(alternatives("C/C++"), ("c", "c++"))
        self.assertEqual(alternatives("CI/CD"), ("cicd",))
        self.assertEqual(alternatives("HTML/CSS"), ("htmlcss",))
        self.assertEqual(alternatives("Strong Python skills"), ("python",))

    def test_listed_skill_is_cited_before_an_implied_one(self):
        status, evidence = SkillMatcher(["Next.js", "React"]).judge(("react",))
        self.assertEqual((status, evidence), ("met", "Lists React"))
        self.assertEqual(SkillMatcher(["Next.js"]).judge(("javascript",)), ("met", "Lists Next.js, which implies it"))

    def test_requirement_accuracy(self):
        report = evaluate()
        self.assertGreaterEqual(report["requirement_accuracy"], 0.90, report["misses"])


class TestJobSearch(unittest.TestCase):
    def test_full_ranking_covers_every_job_sorted_by_score(self):
        index = JobIndex(SAMPLE_JOBS)
        for skills, _ in EVAL_CANDIDATES.values():
            matches = index.rank(skills, top=None)
            self.assertEqual(len(matches), len(SAMPLE_JOBS))
            scores = [m.score for m in matches]
            self.assertEqual(scores, sorted(scores, reverse=True))

    def test_fewer_missing_must_haves_win_ties(self):
        # Both score 60 for Python + SQL, but only "a" is missing a must-have (Rust).
        jobs = [_job("a", "A", None, None, ["Python", "Rust"], ["SQL"]),
                _job("b", "B", None, None, ["Python"], ["SQL", "Rust", "Go"])]
        matches = JobIndex(jobs).rank(["Python", "SQL"], top=None)
        self.assertEqual([(m.job.id, m.score) for m in matches], [("b", 60), ("a", 60)])

    def test_search_without_rerank_never_calls_the_llm(self):
        with mock.patch.object(sys.modules[__name__], "get_llm", side_effect=AssertionError("LLM called")):
            matches = find_jobs(SAMPLE_SKILLS, SAMPLE_JOBS, top=3)
        self.assertEqual(len(matches), 3)
        self.assertTrue(all(m.llm_score is None for m in matches))

    def test_rerank_orders_by_llm_score_and_keeps_the_rest(self):
        quick = find_jobs(SAMPLE_SKILLS, SAMPLE_JOBS, top=5)
        # The LLM disagrees with the quick matcher about its favourite job.
        demoted = quick[0].job.title

        def fake_match(state):
            score = 40 if state["job_requirements"].title == demoted else 90
            return {"match": MatchResult(score=score, assessments=[], summary="fake")}

        with mock.patch.object(sys.modules[__name__], "match_skills", side_effect=fake_match) as fake:
            reranked = find_jobs(SAMPLE_SKILLS, SAMPLE_JOBS, top=5, rerank=3)
        self.assertEqual(fake.call_count, 3)
        self.assertEqual([m.llm_score for m in reranked[:3]], [90, 90, 40])
        self.assertEqual(reranked[2].job.title, demoted)
        self.assertEqual({m.job.id for m in reranked[:3]}, {m.job.id for m in quick[:3]})
        self.assertEqual([m.job.id for m in reranked[3:]], [m.job.id for m in quick[3:]])
        self.assertTrue(all(m.llm_score is None for m in reranked[3:]))


class TestAccuracy(unittest.TestCase):
    def test_ranking_quality_and_beats_exact_name_baseline(self):
        ranking = evaluate()["ranking"]
        matcher, baseline = ranking["matcher"], ranking["baseline"]
        self.assertGreaterEqual(matcher["Top-1"], 0.85)
        self.assertGreaterEqual(matcher["NDCG@5"], 0.85)
        self.assertGreaterEqual(matcher["Recall@5"], 0.85)
        self.assertGreater(matcher["NDCG@5"], baseline["NDCG@5"])


class TestPerformance(unittest.TestCase):
    def test_search_10k_jobs_under_budget(self):
        # Budgets are ~8x what a laptop measures (p95 ~30 ms, build ~270 ms), to stay stable on slow machines.
        result = benchmark(sizes=(10_000,), queries=20)[0]
        self.assertLess(result["p95_ms"], 250, result)
        self.assertLess(result["build_ms"], 2_000, result)


def run_self_tests() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    return 0 if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful() else 1


def run_with_llm_errors(model: str, fn, *args):
    """Run fn, turning common Gemini errors into one-line exits."""
    try:
        return fn(*args)
    except ModelRateLimitError:
        sys.exit(f"❌ Gemini quota exceeded for {model}. The free tier allows about 20 requests/day per model "
                 "(a full run uses 5). Wait for the reset or set GEMINI_MODEL to another model in .env.")
    except (ModelAuthenticationError, ModelInvalidRequestError) as e:
        # Google reports a bad key as 400 INVALID_ARGUMENT with reason API_KEY_INVALID.
        if isinstance(e, ModelInvalidRequestError) and "API_KEY_INVALID" not in str(e):
            raise
        sys.exit("❌ Gemini rejected the API key. Check GOOGLE_API_KEY in .env.")
    except ModelNotFoundError:
        sys.exit(f"❌ Model '{model}' not found. Set GEMINI_MODEL in .env to a current Gemini model.")


def run_find_jobs(args) -> None:
    jobs = load_jobs(args.jobs) if args.jobs else SAMPLE_JOBS
    profile = None
    if args.skills:
        skills = [s.strip() for s in args.skills.split(",") if s.strip()]
    elif args.resume:
        print("📄 Extracting skills from the resume...", file=sys.stderr)
        profile = analyze_resume({"resume_text": read_text(args.resume)})["resume_profile"]
        skills = profile.skills
    else:
        print("ℹ️  No --skills or --resume given; using the sample resume's skills.", file=sys.stderr)
        skills = SAMPLE_SKILLS

    timings: dict = {}
    matches = find_jobs(skills, jobs, top=args.top, rerank=args.rerank, profile=profile, timings=timings)
    if args.json:
        print(json.dumps([m.model_dump() for m in matches], indent=2, ensure_ascii=False))
    else:
        print_job_matches(matches, len(jobs), skills, timings)


def main():
    parser = argparse.ArgumentParser(description="AI Career & Internship Agent")
    parser.add_argument("--resume", help="Path to resume (.pdf/.txt) or raw text")
    parser.add_argument("--job-desc", help="Path to job description file or raw text")
    parser.add_argument("--weeks", type=int, default=3, help="Length of the learning plan (default: 3)")
    parser.add_argument("--json", action="store_true", help="Print raw JSON instead of the report")

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--find-jobs", action="store_true", help="Rank job postings by how well they fit your skills")
    mode.add_argument("--eval", action="store_true", help="Measure job-matching accuracy on hand-labeled cases")
    mode.add_argument("--bench", action="store_true", help="Benchmark job-search speed on synthetic catalogs")
    mode.add_argument("--self-test", action="store_true", help="Run the unit, accuracy and performance tests")

    search = parser.add_argument_group("job search (--find-jobs)")
    search.add_argument("--skills", help='Comma-separated skills, e.g. "Python, SQL, React" (no LLM call needed)')
    search.add_argument("--jobs", help="JSON file of job postings (default: built-in internship catalog)")
    search.add_argument("--top", type=int, default=5, help="Number of jobs to show (default: 5)")
    search.add_argument("--rerank", type=int, default=0, metavar="N",
                        help="Re-check the top N jobs with the LLM Matching Agent (N LLM calls)")
    args = parser.parse_args()

    # Emoji and Thai text in the report crash non-UTF-8 consoles (e.g. default Windows code pages).
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    if args.self_test:
        sys.exit(run_self_tests())
    if args.eval:
        print_eval(evaluate())
        return
    if args.bench:
        print_benchmark(benchmark())
        return

    model = os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
    if args.find_jobs:
        run_with_llm_errors(model, run_find_jobs, args)
        return

    state: CareerState = {
        "resume_text": read_text(args.resume) if args.resume else SAMPLE_RESUME,
        "job_description": read_text(args.job_desc) if args.job_desc else SAMPLE_JOB_DESCRIPTION,
        "weeks": args.weeks,
    }
    print(f"🚀 Analyzing with {model}...")
    result = run_with_llm_errors(model, build_graph().invoke, state)

    if args.json:
        keys = ("resume_profile", "job_requirements", "match", "gap_analysis", "recommendation")
        print(json.dumps({k: result[k].model_dump() for k in keys}, indent=2, ensure_ascii=False))
    else:
        print_report(result)


if __name__ == "__main__":
    main()
