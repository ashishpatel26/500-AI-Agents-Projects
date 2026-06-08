"""
Travel Planner Agent using CrewAI.

Multi-agent crew that creates personalized travel itineraries:
- Destination Researcher: gathers destination info
- Activity Planner: creates day-by-day activities
- Budget Analyst: estimates costs

Usage:
    python agent.py --destination "Tokyo, Japan" --days 5 --budget 2000
"""

import argparse
import os

from crewai import Agent, Crew, Process, Task
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def build_travel_crew(destination: str, days: int, budget: float, interests: str) -> str:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4)

    researcher = Agent(
        role="Destination Researcher",
        goal=f"Research {destination} and provide key travel insights",
        backstory="Expert travel journalist who has visited 100+ countries. Knows the best hidden gems and practical tips.",
        llm=llm,
        verbose=False,
    )

    planner = Agent(
        role="Travel Itinerary Planner",
        goal=f"Create a detailed {days}-day itinerary for {destination}",
        backstory="Luxury travel consultant with 15 years of experience crafting personalized itineraries.",
        llm=llm,
        verbose=False,
    )

    budget_analyst = Agent(
        role="Travel Budget Analyst",
        goal=f"Estimate realistic costs for the trip within ${budget} budget",
        backstory="Financial travel advisor who helps travelers maximize experiences within budget.",
        llm=llm,
        verbose=False,
    )

    research_task = Task(
        description=f"""Research {destination} for a {days}-day trip.
Cover: best time to visit, neighborhoods to stay in, must-see attractions,
local food scene, transportation tips, and cultural customs to know.
Traveler interests: {interests}""",
        agent=researcher,
        expected_output="Destination brief with key areas, attractions, food, and practical tips",
    )

    planning_task = Task(
        description=f"""Create a {days}-day itinerary for {destination}.
Budget: ${budget} total. Interests: {interests}.
Include morning/afternoon/evening activities, specific restaurant recommendations,
and travel time between locations. Make it achievable and enjoyable.""",
        agent=planner,
        expected_output=f"Day-by-day {days}-day itinerary with activities, meals, and timing",
        context=[research_task],
    )

    budget_task = Task(
        description=f"""Provide a budget breakdown for the {days}-day {destination} trip.
Total budget: ${budget}. Include: flights (estimate), accommodation, food, activities,
transportation. Flag if budget is tight and suggest adjustments.""",
        agent=budget_analyst,
        expected_output="Itemized budget breakdown with daily averages and money-saving tips",
        context=[research_task, planning_task],
    )

    crew = Crew(
        agents=[researcher, planner, budget_analyst],
        tasks=[research_task, planning_task, budget_task],
        process=Process.sequential,
        verbose=False,
    )

    return str(crew.kickoff())


def main():
    parser = argparse.ArgumentParser(description="Travel Planner Agent")
    parser.add_argument("--destination", default="Tokyo, Japan", help="Travel destination")
    parser.add_argument("--days", type=int, default=7, help="Number of days")
    parser.add_argument("--budget", type=float, default=3000, help="Total budget in USD")
    parser.add_argument("--interests", default="food, culture, history", help="Traveler interests")
    args = parser.parse_args()

    print(f"\n✈️  Planning {args.days}-day trip to {args.destination} (Budget: ${args.budget})\n")
    itinerary = build_travel_crew(args.destination, args.days, args.budget, args.interests)

    print("=" * 60)
    print("🗺️  TRAVEL ITINERARY")
    print("=" * 60)
    print(itinerary)


if __name__ == "__main__":
    main()
