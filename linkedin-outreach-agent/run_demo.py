"""
Demo: run the LinkedIn Outreach Agent against three sample profiles.
Usage:
    pip install -r requirements.txt
    cp .env.example .env   # add your ANTHROPIC_API_KEY
    python run_demo.py
"""

from linkedin_outreach_agent import run_outreach, update_status

SAMPLE_PROFILES = [
    {
        "name": "Priya Sharma",
        "title": "Head of AI Products",
        "company": "Accenture",
        "reason": "Both working on LLM-based enterprise agents",
        "goal": "discuss potential collaboration on AI agent frameworks",
    },
    {
        "name": "James O'Brien",
        "title": "Founder & CEO",
        "company": "FinSight AI",
        "reason": "Building AI agents for financial analysis — aligns with our research",
        "goal": "explore partnership or knowledge sharing",
    },
    {
        "name": "Mei Lin",
        "title": "ML Engineer",
        "company": "OpenAI",
        "reason": "Published research on multi-agent coordination that we referenced",
        "goal": "ask about open-source tools mentioned in their paper",
    },
]


def main():
    print("=" * 60)
    print("  LinkedIn Outreach Agent — Demo Run")
    print("=" * 60)

    for profile in SAMPLE_PROFILES:
        run_outreach(profile)
        print("\n" + "-" * 60)

    # Simulate updating a status after a reply
    update_status("Priya Sharma", "Accenture", "accepted")

    print("\n[Demo complete] Check outreach_log.json for full output.")


if __name__ == "__main__":
    main()
