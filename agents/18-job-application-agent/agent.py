"""
Job Application Agent using CrewAI.

Analyzes a job description and a candidate profile, then generates:
- Tailored cover letter
- Resume bullet points to highlight
- Interview preparation questions

Usage:
    python agent.py --job-desc "Senior Python Engineer at Stripe..." --candidate "7 years Python, FastAPI..."
"""

import argparse
import os

from crewai import Agent, Crew, Process, Task
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

SAMPLE_JOB = """Senior Python Engineer at Stripe
We're looking for a Senior Python Engineer to join our API Platform team.

Requirements:
- 5+ years Python development
- Experience with distributed systems
- Strong understanding of REST APIs and microservices
- Experience with PostgreSQL, Redis
- Kubernetes experience preferred
- Strong communication skills

Responsibilities:
- Design and build high-performance APIs handling millions of requests/day
- Lead technical design reviews
- Mentor junior engineers
- Collaborate with product managers on technical feasibility
"""

SAMPLE_CANDIDATE = """
Jane Doe — 7 years Python experience
Current role: Senior Software Engineer at DataCorp
Skills: Python, FastAPI, Django, PostgreSQL, Redis, Docker, Kubernetes, AWS
Achievements:
- Built API platform handling 5M requests/day
- Led team of 4 engineers
- Reduced API latency by 40%
- Mentored 3 junior engineers
Education: BS Computer Science, UC Berkeley
"""


def run_job_application_crew(job_desc: str, candidate_profile: str) -> str:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4)

    analyst = Agent(
        role="Job Requirements Analyst",
        goal="Analyze the job description and identify key requirements, values, and culture signals",
        backstory="Ex-hiring manager at FAANG with 10 years recruiting experience. Expert at decoding job descriptions.",
        llm=llm,
        verbose=False,
    )

    writer = Agent(
        role="Career Coach and Application Writer",
        goal="Create tailored application materials that maximize interview chances",
        backstory="Career coach who has helped 500+ candidates land roles at top tech companies.",
        llm=llm,
        verbose=False,
    )

    analyst_task = Task(
        description=f"""Analyze this job description:
{job_desc}

Extract: top 5 required skills, culture signals, what this company values most, potential red flags, and key phrases to mirror in the application.""",
        agent=analyst,
        expected_output="Job analysis: key requirements, culture signals, important keywords",
    )

    application_task = Task(
        description=f"""Using the job analysis, create application materials for this candidate:
{candidate_profile}

Produce:
1. COVER LETTER (250-300 words, 3 paragraphs: hook, evidence, close)
2. TOP 5 RESUME BULLETS TO HIGHLIGHT (tailored to this specific role)
3. 10 LIKELY INTERVIEW QUESTIONS (5 behavioral, 5 technical) with suggested answer frameworks
4. NEGOTIATION RANGE ESTIMATE based on role seniority and company""",
        agent=writer,
        expected_output="Cover letter, resume bullets, interview questions, salary range",
        context=[analyst_task],
    )

    crew = Crew(
        agents=[analyst, writer],
        tasks=[analyst_task, application_task],
        process=Process.sequential,
        verbose=False,
    )

    return str(crew.kickoff())


def main():
    parser = argparse.ArgumentParser(description="Job Application Agent")
    parser.add_argument("--job-desc", default=SAMPLE_JOB, help="Job description text")
    parser.add_argument("--candidate", default=SAMPLE_CANDIDATE, help="Candidate profile summary")
    args = parser.parse_args()

    print("\n💼 Preparing job application materials...\n")
    result = run_job_application_crew(args.job_desc, args.candidate)

    print("=" * 60)
    print("📋 JOB APPLICATION PACKAGE")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    main()
