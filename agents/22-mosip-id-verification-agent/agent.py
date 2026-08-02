import os
import re
import json
import operator
from typing import Dict, Any, List, TypedDict, Optional, Annotated
from dotenv import load_dotenv

load_dotenv()

# LangGraph and LangChain optional imports with safe fallbacks
try:
    from langgraph.graph import StateGraph, START, END
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False

try:
    from langchain_core.messages import SystemMessage, HumanMessage
    from langchain_openai import ChatOpenAI
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

# ============================================================================
# 1. MOSIP MOCK DATA REPOSITORY & SCHEMA UTILITIES
# ============================================================================

MOSIP_MOCK_DATABASE = {
    "UIN-9876543210": {
        "uin": "UIN-9876543210",
        "full_name": "Mohammed Abdul Rahman",
        "dob": "1988-05-14",
        "gender": "MALE",
        "address": "Flat 402, Al Noor Towers, Sector 5, City Center, 560001",
        "postal_code": "560001",
        "phone": "+91-9876543210",
        "status": "ACTIVE",
        "created_date": "2020-01-15"
    },
    "UIN-1122334455": {
        "uin": "UIN-1122334455",
        "full_name": "Priya Sharma",
        "dob": "1995-11-20",
        "gender": "FEMALE",
        "address": "12/A Green Park Layout, Outer Ring Road, 560100",
        "postal_code": "560100",
        "phone": "+91-9123456789",
        "status": "ACTIVE",
        "created_date": "2021-06-10"
    }
}

def validate_uin_format(uin: str) -> bool:
    """Validates MOSIP UIN format (UIN-XXXXXXXXXX with 10 digits)."""
    pattern = r"^UIN-\d{10}$"
    return bool(re.match(pattern, uin))


# ============================================================================
# 2. STATE DEFINITIONS FOR MULTI-AGENT GRAPH
# ============================================================================

class MultiAgentState(TypedDict):
    claim_id: str
    submitted_claim: Dict[str, Any]
    reference_record: Optional[Dict[str, Any]]
    demographic_result: Optional[Dict[str, Any]]
    address_result: Optional[Dict[str, Any]]
    security_result: Optional[Dict[str, Any]]
    final_assessment: Optional[Dict[str, Any]]
    status_logs: Annotated[List[str], operator.add]


def get_llm():
    if not LANGCHAIN_AVAILABLE:
        return None
    api_key = os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    if api_key and api_key != "your_openai_api_key_here":
        return ChatOpenAI(model=model_name, temperature=0.0)
    return None


# ============================================================================
# 3. ORCHESTRATOR & PARALLEL WORKER AGENT NODES
# ============================================================================

def master_orchestrator_node(state: MultiAgentState) -> Dict[str, Any]:
    """Orchestrator Node: Validates claim structure and fetches MOSIP record."""
    claim = state["submitted_claim"]
    uin = claim.get("uin", "")
    logs = [f"[Orchestrator] Received verification claim ID: {state['claim_id']}"]
    
    reference = MOSIP_MOCK_DATABASE.get(uin)
    if reference:
        logs.append(f"[Orchestrator] Found active MOSIP record for UIN: {uin}")
    else:
        logs.append(f"[Orchestrator] WARNING: No reference record found for UIN: {uin}")
        
    return {
        "reference_record": reference,
        "status_logs": logs
    }


def demographic_worker_agent(state: MultiAgentState) -> Dict[str, Any]:
    """Worker Agent 1: Analyzes Name, DOB, Gender, and Transliteration variations."""
    logs = ["[Demographic Worker] Analyzing demographic match..."]
    
    claim = state["submitted_claim"]
    ref = state.get("reference_record")
    
    if not ref:
        return {
            "demographic_result": {
                "match_score": 0,
                "reasoning": "Reference record missing. Cannot perform demographic match.",
                "passed": False
            },
            "status_logs": logs
        }
        
    llm = get_llm()
    if llm:
        prompt = f"""You are a specialized MOSIP Demographic Verification Agent.
Compare the claimed demographic data with the official MOSIP reference record.

Claimed Data: Name: {claim.get('full_name')}, DOB: {claim.get('dob')}, Gender: {claim.get('gender')}
Official Reference: Name: {ref.get('full_name')}, DOB: {ref.get('dob')}, Gender: {ref.get('gender')}

Return JSON ONLY with keys: "match_score" (0-100), "reasoning" (string), "passed" (boolean).
"""
        try:
            response = llm.invoke([SystemMessage(content="You return strict JSON."), HumanMessage(content=prompt)])
            res = json.loads(response.content)
            if isinstance(res, dict) and "match_score" in res and "passed" in res:
                return {"demographic_result": res, "status_logs": logs}
        except (json.JSONDecodeError, KeyError, TypeError):
            pass

    # Deterministic fallback evaluation
    name_claim = claim.get("full_name", "").lower().strip()
    name_ref = ref.get("full_name", "").lower().strip()
    dob_match = claim.get("dob") == ref.get("dob")
    gender_match = claim.get("gender", "").upper() == ref.get("gender", "").upper()
    
    claim_first = name_claim.split()[0] if name_claim else ""
    ref_first = name_ref.split()[0] if name_ref else ""
    
    name_similarity = 0.9 if (claim_first in ref_first or ref_first in claim_first) else 0.2
    if name_claim == name_ref:
        name_similarity = 1.0

    score = int(name_similarity * 60) + (25 if dob_match else 0) + (15 if gender_match else 0)
    passed = score >= 75
    
    return {
        "demographic_result": {
            "match_score": score,
            "reasoning": f"Demographic match: Name similarity {int(name_similarity*100)}%, DOB match: {dob_match}, Gender match: {gender_match}",
            "passed": passed
        },
        "status_logs": logs
    }


def address_worker_agent(state: MultiAgentState) -> Dict[str, Any]:
    """Worker Agent 2: Analyzes Address variations, postal codes, and regional structures."""
    logs = ["[Address Worker] Analyzing address & location structural match..."]
    
    claim = state["submitted_claim"]
    ref = state.get("reference_record")
    
    if not ref:
        return {
            "address_result": {
                "match_score": 0,
                "reasoning": "Reference record missing. Cannot perform address match.",
                "passed": False
            },
            "status_logs": logs
        }

    llm = get_llm()
    if llm:
        prompt = f"""You are a MOSIP Address & Spatial Verification Agent.
Compare the claimed address with the official MOSIP address.

Claimed: {claim.get('address')} (Postal: {claim.get('postal_code')})
Official MOSIP: {ref.get('address')} (Postal: {ref.get('postal_code')})

Return JSON ONLY with keys: "match_score" (0-100), "reasoning" (string), "passed" (boolean).
"""
        try:
            response = llm.invoke([SystemMessage(content="You return strict JSON."), HumanMessage(content=prompt)])
            res = json.loads(response.content)
            if isinstance(res, dict) and "match_score" in res and "passed" in res:
                return {"address_result": res, "status_logs": logs}
        except (json.JSONDecodeError, KeyError, TypeError):
            pass

    c_addr = claim.get("address", "").lower()
    r_addr = ref.get("address", "").lower()
    p_match = claim.get("postal_code") == ref.get("postal_code")
    
    c_words = set(re.findall(r'\w+', c_addr))
    r_words = set(re.findall(r'\w+', r_addr))
    word_overlap = len(c_words.intersection(r_words)) / max(len(r_words), 1)
    
    score = int(word_overlap * 60) + (40 if p_match else 0)
    return {
        "address_result": {
            "match_score": score,
            "reasoning": f"Postal code match: {p_match}. Address word structure overlap: {int(word_overlap*100)}%.",
            "passed": score >= 70
        },
        "status_logs": logs
    }


def security_compliance_worker_agent(state: MultiAgentState) -> Dict[str, Any]:
    """Worker Agent 3: Checks UIN format, status, and fraud risk indicators."""
    logs = ["[Security Worker] Auditing MOSIP UIN format and security risk..."]
    
    claim = state["submitted_claim"]
    uin = claim.get("uin", "")
    ref = state.get("reference_record")
    
    format_valid = validate_uin_format(uin)
    status_active = ref.get("status") == "ACTIVE" if ref else False
    
    if not format_valid:
        score = 0
        reasoning = f"SECURITY ALERT: Invalid MOSIP UIN format structure ({uin})."
        passed = False
    elif not ref:
        score = 20
        reasoning = f"SECURITY ALERT: UIN {uin} not found in MOSIP registry."
        passed = False
    elif not status_active:
        score = 30
        reasoning = f"SECURITY ALERT: UIN {uin} status: {ref.get('status')}."
        passed = False
    else:
        score = 100
        reasoning = "UIN format valid. Record is ACTIVE in MOSIP registry."
        passed = True
        
    return {
        "security_result": {
            "match_score": score,
            "reasoning": reasoning,
            "passed": passed
        },
        "status_logs": logs
    }


def synthesis_aggregator_node(state: MultiAgentState) -> Dict[str, Any]:
    """Aggregator Node: Synthesizes reports from all 3 workers and routes final decision."""
    logs = ["[Aggregator] Synthesizing multi-agent outputs into final MOSIP decision..."]
    
    demo = state.get("demographic_result", {"match_score": 0, "reasoning": ""})
    addr = state.get("address_result", {"match_score": 0, "reasoning": ""})
    sec = state.get("security_result", {"match_score": 0, "passed": False, "reasoning": ""})
    
    weighted_score = (demo["match_score"] * 0.40) + (addr["match_score"] * 0.35) + (sec["match_score"] * 0.25)
    weighted_score = round(weighted_score, 2)
    
    if not sec.get("passed", False):
        decision = "REJECTED"
        recommendation = "Security check failed. Invalid UIN format or inactive record."
    elif weighted_score >= 85:
        decision = "APPROVED"
        recommendation = "High confidence identity match. Verification complete."
    elif weighted_score >= 65:
        decision = "FLAGGED_FOR_MANUAL_REVIEW"
        recommendation = "Moderate identity match. Human operator review required for address/name variations."
    else:
        decision = "REJECTED"
        recommendation = "Low identity match score across demographic and spatial fields."
        
    final_assessment = {
        "claim_id": state["claim_id"],
        "uin": state["submitted_claim"].get("uin"),
        "overall_confidence_score": weighted_score,
        "final_decision": decision,
        "recommendation": recommendation,
        "breakdown": {
            "demographic_score": demo["match_score"],
            "address_score": addr["match_score"],
            "security_score": sec["match_score"]
        },
        "worker_summaries": {
            "demographic": demo.get("reasoning"),
            "address": addr.get("reasoning"),
            "security": sec.get("reasoning")
        }
    }
    
    return {
        "final_assessment": final_assessment,
        "status_logs": logs
    }


# ============================================================================
# 4. MULTI-AGENT GRAPH & ORCHESTRATION PIPELINE
# ============================================================================

def run_multi_agent_pipeline(initial_state: MultiAgentState) -> MultiAgentState:
    """Runs graph if LangGraph is available, or uses direct orchestrator pipeline."""
    if LANGGRAPH_AVAILABLE:
        builder = StateGraph(MultiAgentState)
        builder.add_node("orchestrator", master_orchestrator_node)
        builder.add_node("demographic_worker", demographic_worker_agent)
        builder.add_node("address_worker", address_worker_agent)
        builder.add_node("security_worker", security_compliance_worker_agent)
        builder.add_node("aggregator", synthesis_aggregator_node)
        
        builder.add_edge(START, "orchestrator")
        builder.add_edge("orchestrator", "demographic_worker")
        builder.add_edge("orchestrator", "address_worker")
        builder.add_edge("orchestrator", "security_worker")
        builder.add_edge("demographic_worker", "aggregator")
        builder.add_edge("address_worker", "aggregator")
        builder.add_edge("security_worker", "aggregator")
        builder.add_edge("aggregator", END)
        
        graph = builder.compile()
        return graph.invoke(initial_state)
    else:
        # Sequential multi-agent pipeline fallback aggregating status_logs properly
        o_res = master_orchestrator_node(initial_state)
        s1 = {**initial_state, **o_res}
        
        d_res = demographic_worker_agent(s1)
        a_res = address_worker_agent(s1)
        sec_res = security_compliance_worker_agent(s1)
        
        combined_logs = s1.get("status_logs", []) + d_res.get("status_logs", []) + a_res.get("status_logs", []) + sec_res.get("status_logs", [])
        
        s_combined = {
            **s1,
            "demographic_result": d_res.get("demographic_result"),
            "address_result": a_res.get("address_result"),
            "security_result": sec_res.get("security_result"),
            "status_logs": combined_logs
        }
        
        agg_res = synthesis_aggregator_node(s_combined)
        final_logs = s_combined["status_logs"] + agg_res.get("status_logs", [])
        
        return {
            **s_combined,
            "final_assessment": agg_res.get("final_assessment"),
            "status_logs": final_logs
        }


# ============================================================================
# 5. DEMO EXECUTION ROUTINE
# ============================================================================

def run_demo():
    print("=" * 80)
    print("MOSIP MULTI-AGENT DIGITAL IDENTITY VERIFICATION SYSTEM")
    print(f"Framework: LangGraph ({'Enabled' if LANGGRAPH_AVAILABLE else 'Sequential Fallback Mode'})")
    print("Architecture: Parallel Multi-Worker Orchestration Layer")
    print("=" * 80 + "\n")
    
    test_claims = [
        {
            "claim_id": "CLM-101",
            "description": "Valid claim with minor name spelling variation & address format difference",
            "data": {
                "uin": "UIN-9876543210",
                "full_name": "Mohamed A Rahman",
                "dob": "1988-05-14",
                "gender": "MALE",
                "address": "Flat 402 Al Noor Towers, Sector 5",
                "postal_code": "560001"
            }
        },
        {
            "claim_id": "CLM-102",
            "description": "Invalid UIN format (Security Failure Test)",
            "data": {
                "uin": "UIN-INVALID-99",
                "full_name": "Priya Sharma",
                "dob": "1995-11-20",
                "gender": "FEMALE",
                "address": "12 Green Park",
                "postal_code": "560100"
            }
        },
        {
            "claim_id": "CLM-103",
            "description": "Mismatching Demographic Data Claim",
            "data": {
                "uin": "UIN-1122334455",
                "full_name": "Vikram Singh",
                "dob": "1980-01-01",
                "gender": "MALE",
                "address": "99 Unknown Road",
                "postal_code": "999999"
            }
        }
    ]
    
    for test in test_claims:
        print(f"▶ RUNNING TEST: {test['claim_id']} ({test['description']})")
        initial_state: MultiAgentState = {
            "claim_id": test["claim_id"],
            "submitted_claim": test["data"],
            "reference_record": None,
            "demographic_result": None,
            "address_result": None,
            "security_result": None,
            "final_assessment": None,
            "status_logs": []
        }
        
        final_state = run_multi_agent_pipeline(initial_state)
        assessment = final_state["final_assessment"]
        
        print("\n--- Execution Logs ---")
        seen_logs = set()
        for log in final_state["status_logs"]:
            if log not in seen_logs:
                print(f"  {log}")
                seen_logs.add(log)
            
        print("\n--- Verification Summary ---")
        print(f"  Overall Score : {assessment['overall_confidence_score']}%")
        print(f"  Final Decision: {assessment['final_decision']}")
        print(f"  Recommendation: {assessment['recommendation']}")
        print(f"  Score Breakdown: Demographic ({assessment['breakdown']['demographic_score']}%), Address ({assessment['breakdown']['address_score']}%), Security ({assessment['breakdown']['security_score']}%)")
        print("-" * 80 + "\n")


if __name__ == "__main__":
    run_demo()
