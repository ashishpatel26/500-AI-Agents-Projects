"""
Competitive Analysis Agent using LangGraph.

Multi-step agent that analyzes competitors:
1. Identifies key competitors
2. Analyzes each competitor's strengths/weaknesses
3. Generates competitive positioning recommendations

Usage:
    python agent.py --company "Notion" --industry "productivity software"
"""

import argparse
import os
from typing import Annotated, TypedDict, Dict, Tuple
import concurrent.futures

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
# Reuse cached LLM instances from agents._common to avoid recreating clients per call
from agents._common import get_llm
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

load_dotenv()


class AnalysisState(TypedDict):
    messages: Annotated[list, add_messages]
    company: str
    industry: str
    competitors: list[str]
    competitor_analyses: dict[str, str]
    final_report: str


def identify_competitors(state: AnalysisState) -> AnalysisState:
    llm = get_llm(model="gpt-4o-mini", temperature=0)
    response = llm.invoke([
        SystemMessage(content="You are a market research analyst. List exactly 5 main competitors as a comma-separated list. Nothing else."),
        HumanMessage(content=f"Company: {state['company']}\nIndustry: {state['industry']}\n\nList 5 main competitors:"),
    ])
    competitors = [c.strip() for c in response.content.split(",")][:5]
    return {"competitors": competitors, "messages": [response]}


def _analyze_one(competitor: str, company: str, industry: str) -> Tuple[str, str]:
    """Worker helper to analyze a single competitor. Returns (competitor, analysis_text)."""
    llm = get_llm(model="gpt-4o-mini", temperature=0)
    try:
        response = llm.invoke([
            SystemMessage(content="Provide a concise competitive analysis in 100 words covering: main products, strengths (2), weaknesses (2), pricing model, target market."),
            HumanMessage(content=f"Analyze {competitor} vs {company} in {industry}:"),
        ])
        return competitor, response.content
    except Exception as e:
        # On error, return an explanatory placeholder so the pipeline can continue
        return competitor, f"<ERROR during analysis: {e}>"


def analyze_competitor(state: AnalysisState) -> AnalysisState:
    analyses: Dict[str, str] = {}
    competitors = state.get("competitors", [])

    if not competitors:
        return {"competitor_analyses": analyses}

    # Use a ThreadPoolExecutor to analyze competitors in parallel and reduce wall-clock latency.
    max_workers = min(5, len(competitors))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as exc:
        # Submit all tasks
        futures = [exc.submit(_analyze_one, c, state["company"], state["industry"]) for c in competitors]
        # Collect results as they complete
        for fut in concurrent.futures.as_completed(futures):
            comp, text = fut.result()
            analyses[comp] = text

    return {"competitor_analyses": analyses}


def generate_report(state: AnalysisState) -> AnalysisState:
    llm = get_llm(model="gpt-4o", temperature=0)

    analyses_text = "\n\n".join(
        f"**{name}:**\n{analysis}"
        for name, analysis in state["competitor_analyses"].items()
    )

    response = llm.invoke([
        SystemMessage(content="""You are a strategic consultant. Create a competitive analysis report with:
1. Executive Summary (3 sentences)
2. Competitive Landscape Table (company, strength, weakness, price)
3. Market Gaps & Opportunities (3 bullet points)
4. Strategic Recommendations for {company} (5 action items)
5. Threat Assessment (High/Medium/Low for each competitor)""".replace("{company}", state["company"])),
        HumanMessage(content=f"Company: {state['company']}\nIndustry: {state['industry']}\n\nCompetitor analyses:\n{analyses_text}"),
    ])

    return {"final_report": response.content, "messages": [response]}


def build_graph():
    graph = StateGraph(AnalysisState)
    graph.add_node("identify", identify_competitors)
    graph.add_node("analyze", analyze_competitor)
    graph.add_node("report", generate_report)
    graph.set_entry_point("identify")
    graph.add_edge("identify", "analyze")
    graph.add_edge("analyze", "report")
    graph.add_edge("report", END)
    return graph.compile()


def main():
    parser = argparse.ArgumentParser(description="Competitive Analysis Agent")
    parser.add_argument("--company", default="Notion", help="Company to analyze")
    parser.add_argument("--industry", default="productivity and collaboration software", help="Industry")
    args = parser.parse_args()

    print(f"\n🔍 Analyzing competitive landscape for {args.company}...\n")

    agent = build_graph()
    result = agent.invoke({
        "company": args.company,
        "industry": args.industry,
        "messages": [],
        "competitors": [],
        "competitor_analyses": {},
        "final_report": "",
    })

    print(f"🏢 Competitors identified: {', '.join(result['competitors'])}\n")
    print("=" * 60)
    print("📊 COMPETITIVE ANALYSIS REPORT")
    print("=" * 60)
    print(result["final_report"])


if __name__ == "__main__":
    main()
