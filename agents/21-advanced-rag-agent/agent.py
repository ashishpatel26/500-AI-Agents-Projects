"""
Advanced RAG Agent using LangGraph.

Combines:
1. Adaptive RAG (Query Routing)
2. Corrective RAG (Document grading & Web search fallback)
3. Self-RAG (Hallucination & Answer relevance grading loop)

Usage:
    python agent.py
    python agent.py --query "What is the file size limit for CloudSync Pro?"
"""

import argparse
import os
from typing import Annotated, Literal, TypedDict
from pydantic import BaseModel, Field

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import END, StateGraph

load_dotenv()

# =====================================================================
# 1. Knowledge Base and Embeddings
# =====================================================================

SAMPLE_KB = [
    "Product: CloudSync Pro. Features: real-time sync across 5 devices, 1TB storage, offline mode, version history 30 days.",
    "Pricing: Basic $9/mo (100GB, 2 devices), Pro $19/mo (1TB, 5 devices), Business $49/mo (5TB, unlimited devices).",
    "Cancellation: Cancel anytime from Account > Subscription > Cancel. Refunds available within 14 days of charge.",
    "Password reset: Go to login page, click 'Forgot Password', enter email. Reset link expires in 1 hour.",
    "Sync issues: Check internet connection, ensure app is updated, try Sign Out and Sign In. If persists, contact support.",
    "Supported platforms: Windows 10+, macOS 12+, iOS 15+, Android 10+, Linux (Beta).",
    "Data security: AES-256 encryption at rest and in transit. SOC 2 Type II certified. Zero-knowledge architecture.",
    "File size limit: Individual files up to 10GB (Pro/Business), 2GB (Basic). No limit on total number of files.",
]


def is_openai_configured() -> bool:
    api_key = os.environ.get("OPENAI_API_KEY")
    return bool(api_key and not api_key.startswith("your_"))


# =====================================================================
# 2. State & Pydantic Schemas for Structured Output
# =====================================================================

class GraphState(TypedDict):
    question: str
    generation: str
    web_search: str  # "Yes" or "No"
    documents: list[str]
    steps: list[str]


class RouteQuery(BaseModel):
    datasource: Literal["vectorstore", "web_search", "direct_answer"] = Field(
        description="Choose where to route the user query."
    )


class GradeDocuments(BaseModel):
    binary_score: Literal["yes", "no"] = Field(
        description="Is the document relevant to the user question? 'yes' or 'no'"
    )


class GradeHallucinations(BaseModel):
    binary_score: Literal["yes", "no"] = Field(
        description="Is the generated answer grounded in the provided facts? 'yes' or 'no'"
    )


class GradeAnswer(BaseModel):
    binary_score: Literal["yes", "no"] = Field(
        description="Does the generated answer directly address and answer the question? 'yes' or 'no'"
    )


# =====================================================================
# 3. Nodes Implementation
# =====================================================================

def retrieve(state: GraphState) -> GraphState:
    print("---RETRIEVING FROM VECTOR STORE---")
    question = state["question"]
    steps = state.get("steps", [])
    steps.append("retrieve")

    if is_openai_configured():
        embeddings = OpenAIEmbeddings()
        splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=30)
        docs_split = splitter.create_documents(SAMPLE_KB)
        vectorstore = FAISS.from_documents(docs_split, embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
        retrieved_docs = retriever.invoke(question)
        documents = [d.page_content for d in retrieved_docs]
    else:
        # Fallback Mock retrieval logic matching keywords
        print("[MOCK] Simulating vector store retrieval...")
        query_words = question.lower().split()
        documents = []
        for doc in SAMPLE_KB:
            if any(word in doc.lower() for word in query_words if len(word) > 3):
                documents.append(doc)
        if not documents:
            documents = SAMPLE_KB[:2]  # Default fallback

    return {"documents": documents, "steps": steps}


def generate(state: GraphState) -> GraphState:
    print("---GENERATING RESPONSE---")
    question = state["question"]
    documents = state["documents"]
    steps = state.get("steps", [])
    steps.append("generate")

    context = "\n\n".join(documents)

    if is_openai_configured():
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        messages = [
            SystemMessage(content=f"You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, say that you don't know.\n\nContext:\n{context}"),
            HumanMessage(content=question),
        ]
        response = llm.invoke(messages)
        generation = response.content
    else:
        # Fallback Mock generation logic
        print("[MOCK] Simulating response generation...")
        if "recursion" in question.lower():
            generation = "Recursion in programming is a technique where a function calls itself directly or indirectly to solve a problem by breaking it down into smaller sub-problems."
        elif "storage" in question.lower() or "limit" in question.lower() or "pricing" in question.lower():
            generation = "According to CloudSync Pro specifications: The Pro subscription costs $19/mo and features 1TB storage, offline mode, and real-time sync across 5 devices. The individual file size limit is 10GB for Pro/Business, and 2GB for Basic."
        elif "python" in question.lower() or "release" in question.lower():
            generation = "Based on web search results: Python 3.12 was released on October 2, 2023. It features new syntax options, improved performance, and cleaner syntax."
        else:
            generation = f"This is a mock response answering: '{question}' using context:\n{context[:150]}..."

    return {"generation": generation, "steps": steps}


def grade_documents(state: GraphState) -> GraphState:
    print("---GRADING DOCUMENTS FOR RELEVANCE---")
    question = state["question"]
    documents = state["documents"]
    steps = state.get("steps", [])
    steps.append("grade_documents")

    web_search = "No"
    filtered_docs = []

    if is_openai_configured():
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        structured_grader = llm.with_structured_output(GradeDocuments)

        for doc in documents:
            grade_prompt = f"Assess if this document is relevant to the question.\nDocument: {doc}\nQuestion: {question}"
            grade = structured_grader.invoke([HumanMessage(content=grade_prompt)])
            if grade.binary_score == "yes":
                filtered_docs.append(doc)
            else:
                web_search = "Yes"  # Trigger web search if any doc is irrelevant
    else:
        # Fallback Mock grading logic
        print("[MOCK] Simulating document relevance grading...")
        for doc in documents:
            query_words = question.lower().split()
            # Simple keyword matching heuristic
            if any(word in doc.lower() for word in query_words if len(word) > 3):
                filtered_docs.append(doc)
            else:
                web_search = "Yes"

        # If no docs match, we definitely search the web
        if not filtered_docs:
            web_search = "Yes"
            filtered_docs = documents

    print(f"Relevance grade: web_search flag = {web_search}")
    return {"documents": filtered_docs, "web_search": web_search, "steps": steps}


def web_search(state: GraphState) -> GraphState:
    print("---WEB SEARCH FALLBACK---")
    question = state["question"]
    documents = state.get("documents", [])
    steps = state.get("steps", [])
    steps.append("web_search")

    tavily_key = os.environ.get("TAVILY_API_KEY")
    if is_openai_configured() and tavily_key and not tavily_key.startswith("your_"):
        from langchain_tavily import TavilySearch
        search_tool = TavilySearch(max_results=3)
        results = search_tool.invoke(question)
        if isinstance(results, list):
            search_content = "\n".join(r.get("content", "") for r in results)
        else:
            search_content = str(results)
    else:
        # Fallback Mock search logic
        print("[MOCK] Simulating web search execution...")
        if "python 3.12" in question.lower():
            search_content = "Python 3.12.0 was officially released on October 2, 2023. Key updates include isolation of subinterpreters, f-string improvements, and PEP 695 type parameter syntax."
        elif "weather" in question.lower():
            search_content = "The weather today in Seattle is 65°F and partly cloudy with a 10% chance of rain."
        else:
            search_content = f"Web search results matching query '{question}': Found articles discussing the details, specifications, and related updates."

    documents.append(f"[Web Search Source] {search_content}")
    return {"documents": documents, "steps": steps}


# =====================================================================
# 4. Conditional Edges / Routing Logic
# =====================================================================

def route_question(state: GraphState) -> Literal["web_search", "retrieve", "direct_answer"]:
    print("---ROUTING QUESTION---")
    question = state["question"]

    if is_openai_configured():
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        structured_router = llm.with_structured_output(RouteQuery)
        
        router_prompt = (
            "You are a router. Route the user question to either 'web_search', 'vectorstore', or 'direct_answer'.\n"
            "Use 'vectorstore' for questions about CloudSync Pro (features, limits, sync, pricing, reset, platforms, security).\n"
            "Use 'web_search' for current affairs, external facts, or search engine topics (e.g. weather, release dates).\n"
            "Use 'direct_answer' for general greetings, educational explanations not requiring specific documents, or writing code.\n"
            f"Question: {question}"
        )
        decision = structured_router.invoke([HumanMessage(content=router_prompt)])
        datasource = decision.datasource
    else:
        # Fallback Mock routing logic
        print("[MOCK] Simulating query routing...")
        q_lower = question.lower()
        if "cloudsync" in q_lower or "storage" in q_lower or "limit" in q_lower or "price" in q_lower or "account" in q_lower:
            datasource = "vectorstore"
        elif "python" in q_lower or "latest" in q_lower or "weather" in q_lower or "date" in q_lower:
            datasource = "web_search"
        else:
            datasource = "direct_answer"

    print(f"Routing query '{question}' to: {datasource}")
    if datasource == "vectorstore":
        return "retrieve"
    elif datasource == "web_search":
        return "web_search"
    else:
        return "direct_answer"


def decide_to_generate(state: GraphState) -> Literal["web_search", "generate"]:
    print("---DECIDING TO GENERATE OR SEARCH---")
    if state["web_search"] == "Yes":
        print("Decision: Some docs irrelevant. Routing to Web Search.")
        return "web_search"
    else:
        print("Decision: All docs relevant. Routing to Response Generator.")
        return "generate"


def grade_generation_v_documents_and_question(state: GraphState) -> Literal["not grounded", "not useful", "useful"]:
    print("---EVALUATING GENERATION---")
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]

    if is_openai_configured():
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        
        # 1. Hallucination check
        structured_hallucination_grader = llm.with_structured_output(GradeHallucinations)
        hallucination_prompt = (
            "Assess if the generation is grounded in / supported by the facts.\n"
            f"Facts:\n{chr(10).join(documents)}\n"
            f"Generation:\n{generation}"
        )
        hallucination_grade = structured_hallucination_grader.invoke([HumanMessage(content=hallucination_prompt)])
        
        if hallucination_grade.binary_score == "yes":
            print("---GENERATION IS GROUNDED (NO HALLUCINATIONS)---")
            # 2. Answer relevance check
            structured_answer_grader = llm.with_structured_output(GradeAnswer)
            answer_prompt = (
                "Assess if the generation addresses the question.\n"
                f"Question:\n{question}\n"
                f"Generation:\n{generation}"
            )
            answer_grade = structured_answer_grader.invoke([HumanMessage(content=answer_prompt)])
            
            if answer_grade.binary_score == "yes":
                print("---GENERATION IS USEFUL AND ANSWERS THE QUESTION---")
                return "useful"
            else:
                print("---GENERATION DOES NOT ANSWER THE QUESTION---")
                return "not useful"
        else:
            print("---GENERATION IS NOT GROUNDED (HALLUCINATED)---")
            return "not grounded"
    else:
        # Fallback Mock evaluation
        print("[MOCK] Simulating evaluation metrics...")
        print("---GENERATION IS GROUNDED & USEFUL---")
        return "useful"


# =====================================================================
# 5. Graph Definition & Compilation
# =====================================================================

def build_graph() -> StateGraph:
    workflow = StateGraph(GraphState)

    # Register nodes
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("grade_documents", grade_documents)
    workflow.add_node("generate", generate)
    workflow.add_node("web_search", web_search)

    # Dynamic starting routing
    workflow.set_conditional_entry_point(
        route_question,
        {
            "retrieve": "retrieve",
            "web_search": "web_search",
            "direct_answer": "generate",
        }
    )

    # Main graph transitions
    workflow.add_edge("retrieve", "grade_documents")
    
    workflow.add_conditional_edges(
        "grade_documents",
        decide_to_generate,
        {
            "web_search": "web_search",
            "generate": "generate",
        }
    )
    
    workflow.add_edge("web_search", "generate")
    
    workflow.add_conditional_edges(
        "generate",
        grade_generation_v_documents_and_question,
        {
            "not grounded": "generate",
            "not useful": "web_search",
            "useful": END,
        }
    )

    return workflow.compile()


# =====================================================================
# 6. Main Runner
# =====================================================================

def main():
    parser = argparse.ArgumentParser(description="Advanced RAG Agent with LangGraph")
    parser.add_argument(
        "--query", 
        default="What is the storage limit for CloudSync Pro Pro subscription?", 
        help="Query to ask the agent"
    )
    args = parser.parse_args()

    if not is_openai_configured():
        print("=" * 80)
        print("⚠️  Warning: OPENAI_API_KEY environment variable is not set or holds default value.")
        print("   Running agent in SIMULATION / MOCK mode to demonstrate state graph routing.")
        print("=" * 80)

    print(f"\n🚀 Question: {args.query}")
    print("----------------------------------------------------------------------")
    
    graph = build_graph()
    initial_state = {
        "question": args.query,
        "generation": "",
        "web_search": "No",
        "documents": [],
        "steps": []
    }
    
    final_state = graph.invoke(initial_state)
    
    print("\n" + "=" * 80)
    print("📊 EXECUTION PATH STEPS TAKEN:")
    print(" -> ".join(final_state["steps"]) + " -> END")
    print("=" * 80)
    print("🤖 FINAL RESPONSE:")
    print(final_state["generation"])
    print("=" * 80)


if __name__ == "__main__":
    main()
