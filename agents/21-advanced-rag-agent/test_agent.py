"""
Unit tests for the Advanced RAG LangGraph Agent.

Tests the state, routing, grading heuristics, and compiled graph transitions.
Run with:
    python -m unittest test_agent.py
"""

import unittest
from unittest.mock import patch, MagicMock
from agent import (
    build_graph,
    route_question,
    grade_documents,
    decide_to_generate,
    grade_generation_v_documents_and_question,
    SAMPLE_KB,
)


class MockGrade:
    def __init__(self, score: str):
        self.binary_score = score


class TestAdvancedRAGAgent(unittest.TestCase):

    def setUp(self):
        # Force is_openai_configured to False when building the graph for base testing
        with patch('agent.is_openai_configured', return_value=False):
            self.graph = build_graph()

    @patch('agent.is_openai_configured', return_value=False)
    def test_routing_logic_mock(self, mock_is_configured):
        """Test that questions are routed correctly in mock mode."""
        # 1. RAG Query
        state_rag = {"question": "What is the pricing of CloudSync Pro?"}
        self.assertEqual(route_question(state_rag), "retrieve")

        # 2. Web Search Query
        state_search = {"question": "What is the latest release date of Python 3.12?"}
        self.assertEqual(route_question(state_search), "web_search")

        # 3. Direct Answer Query
        state_direct = {"question": "Explain how recursion works in Python."}
        self.assertEqual(route_question(state_direct), "direct_answer")

    @patch('agent.is_openai_configured', return_value=False)
    def test_grade_documents_heuristic(self, mock_is_configured):
        """Test document grading heuristic for relevance in mock mode."""
        # Query with relevant terms
        state = {
            "question": "storage limit",
            "documents": [SAMPLE_KB[7]],  # Document containing 'File size limit'
            "steps": [],
        }
        res = grade_documents(state)
        self.assertFalse(res["should_web_search"])
        self.assertEqual(len(res["documents"]), 1)

        # Query with irrelevant terms triggers search fallback
        state_irr = {
            "question": "weather in Seattle",
            "documents": [SAMPLE_KB[0]],
            "steps": [],
        }
        res_irr = grade_documents(state_irr)
        self.assertTrue(res_irr["should_web_search"])

    def test_decide_to_generate(self):
        """Test transition path selection based on web search flag."""
        state_search = {"should_web_search": True}
        self.assertEqual(decide_to_generate(state_search), "web_search")

        state_generate = {"should_web_search": False}
        self.assertEqual(decide_to_generate(state_generate), "generate")

    @patch('agent.is_openai_configured', return_value=False)
    def test_grade_generation_grounding_mock(self, mock_is_configured):
        """Test hallucination/answer grading outputs in mock mode."""
        state = {
            "question": "recursion",
            "documents": [],
            "generation": "Recursion is when a function calls itself.",
        }
        # In mock mode, defaults to "useful"
        res = grade_generation_v_documents_and_question(state)
        self.assertEqual(res, "useful")

    @patch('agent.is_openai_configured', return_value=True)
    @patch('agent.ChatOpenAI')
    def test_grade_generation_not_grounded(self, mock_chat_openai, mock_is_configured):
        """Test the hallucination check branch when generation is not grounded."""
        mock_llm = MagicMock()
        mock_chat_openai.return_value = mock_llm

        # Force first grader (hallucination) to return binary_score="no"
        mock_grader = MagicMock()
        mock_grader.invoke.return_value = MockGrade("no")
        mock_llm.with_structured_output.return_value = mock_grader

        state = {
            "question": "What is recursion?",
            "documents": ["Recursion is about sorting algorithms."],
            "generation": "Recursion is a kind of sorting algorithm.",
            "steps": []
        }

        res = grade_generation_v_documents_and_question(state)
        self.assertEqual(res, "not grounded")

    @patch('agent.is_openai_configured', return_value=True)
    @patch('agent.ChatOpenAI')
    def test_grade_generation_not_useful(self, mock_chat_openai, mock_is_configured):
        """Test the answer relevance check branch when generation is grounded but not useful."""
        mock_llm = MagicMock()
        mock_chat_openai.return_value = mock_llm

        # Force hallucination grader to "yes" and answer relevance grader to "no"
        mock_grader_hallucination = MagicMock()
        mock_grader_hallucination.invoke.return_value = MockGrade("yes")

        mock_grader_answer = MagicMock()
        mock_grader_answer.invoke.return_value = MockGrade("no")

        mock_llm.with_structured_output.side_effect = [
            mock_grader_hallucination,
            mock_grader_answer
        ]

        state = {
            "question": "What is recursion?",
            "documents": ["Recursion is a function calling itself."],
            "generation": "Python was released in 1991.",
            "steps": []
        }

        res = grade_generation_v_documents_and_question(state)
        self.assertEqual(res, "not useful")

    @patch('agent.is_openai_configured', return_value=False)
    def test_graph_execution_mock_direct(self, mock_is_configured):
        """Test execution flow of the compiled graph for a direct answer query in mock mode."""
        initial_state = {
            "question": "Explain recursion.",
            "generation": "",
            "should_web_search": False,
            "documents": [],
            "steps": [],
        }
        output = self.graph.invoke(initial_state)
        self.assertIn("direct_generate", output["steps"])
        self.assertNotIn("retrieve", output["steps"])
        self.assertNotIn("web_search", output["steps"])
        self.assertNotIn("generate", output["steps"])
        self.assertTrue(len(output["generation"]) > 0)

    @patch('agent.is_openai_configured', return_value=False)
    def test_graph_execution_mock_rag(self, mock_is_configured):
        """Test execution flow for a RAG-based query in mock mode."""
        initial_state = {
            "question": "What is the storage limit of CloudSync Pro?",
            "generation": "",
            "should_web_search": False,
            "documents": [],
            "steps": [],
        }
        output = self.graph.invoke(initial_state)
        self.assertIn("retrieve", output["steps"])
        self.assertIn("grade_documents", output["steps"])
        self.assertNotIn("web_search", output["steps"])
        self.assertIn("generate", output["steps"])
        self.assertTrue(len(output["generation"]) > 0)


if __name__ == "__main__":
    unittest.main()
