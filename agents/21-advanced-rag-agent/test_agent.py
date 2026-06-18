"""
Unit tests for the Advanced RAG LangGraph Agent.

Tests the state, routing, grading heuristics, and compiled graph transitions.
Run with:
    python -m unittest test_agent.py
"""

import unittest
from agent import (
    build_graph,
    route_question,
    grade_documents,
    decide_to_generate,
    grade_generation_v_documents_and_question,
    SAMPLE_KB,
)


class TestAdvancedRAGAgent(unittest.TestCase):

    def setUp(self):
        self.graph = build_graph()

    def test_routing_logic(self):
        """Test that questions are routed to the correct nodes."""
        # 1. RAG Query
        state_rag = {"question": "What is the pricing of CloudSync Pro?"}
        self.assertEqual(route_question(state_rag), "retrieve")

        # 2. Web Search Query
        state_search = {"question": "What is the latest release date of Python 3.12?"}
        self.assertEqual(route_question(state_search), "web_search")

        # 3. Direct Answer Query
        state_direct = {"question": "Explain how recursion works in Python."}
        self.assertEqual(route_question(state_direct), "direct_answer")

    def test_grade_documents_heuristic(self):
        """Test document grading heuristic for relevance."""
        # Query with relevant terms
        state = {
            "question": "storage limit",
            "documents": [SAMPLE_KB[7]],  # Document containing 'File size limit'
            "steps": [],
        }
        res = grade_documents(state)
        self.assertEqual(res["web_search"], "No")

        # Query with irrelevant terms triggers search fallback
        state_irr = {
            "question": "weather in Seattle",
            "documents": [SAMPLE_KB[0]],
            "steps": [],
        }
        res_irr = grade_documents(state_irr)
        self.assertEqual(res_irr["web_search"], "Yes")

    def test_decide_to_generate(self):
        """Test transition path selection based on web search flag."""
        state_search = {"web_search": "Yes"}
        self.assertEqual(decide_to_generate(state_search), "web_search")

        state_generate = {"web_search": "No"}
        self.assertEqual(decide_to_generate(state_generate), "generate")

    def test_grade_generation_grounding(self):
        """Test hallucination/answer grading outputs in mock mode."""
        state = {
            "question": "recursion",
            "documents": [],
            "generation": "Recursion is when a function calls itself.",
        }
        # In mock mode, defaults to "useful"
        res = grade_generation_v_documents_and_question(state)
        self.assertEqual(res, "useful")

    def test_graph_execution_mock_direct(self):
        """Test execution flow of the compiled graph for a direct answer query in mock mode."""
        initial_state = {
            "question": "Explain recursion.",
            "generation": "",
            "web_search": "No",
            "documents": [],
            "steps": [],
        }
        output = self.graph.invoke(initial_state)
        self.assertIn("generate", output["steps"])
        self.assertTrue(len(output["generation"]) > 0)

    def test_graph_execution_mock_rag(self):
        """Test execution flow for a RAG-based query in mock mode."""
        initial_state = {
            "question": "What is the storage limit of CloudSync Pro?",
            "generation": "",
            "web_search": "No",
            "documents": [],
            "steps": [],
        }
        output = self.graph.invoke(initial_state)
        self.assertIn("retrieve", output["steps"])
        self.assertIn("grade_documents", output["steps"])
        # Since it contains relevant keywords, it shouldn't route to web search in mock
        self.assertIn("generate", output["steps"])
        self.assertTrue(len(output["generation"]) > 0)


if __name__ == "__main__":
    unittest.main()
