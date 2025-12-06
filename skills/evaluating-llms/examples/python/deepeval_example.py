"""
DeepEval Framework for LLM Evaluation

Demonstrates using DeepEval for comprehensive LLM testing with pytest integration,
G-Eval metrics, custom metrics, and test case management.

Installation:
    pip install deepeval openai

Usage:
    python deepeval_example.py
    # Or with pytest:
    pytest deepeval_example.py -v
"""

import pytest
from deepeval import assert_test
from deepeval.metrics import (
    GEval,
    FaithfulnessMetric,
    AnswerRelevancyMetric,
    ContextualRelevancyMetric,
)
from deepeval.test_case import LLMTestCase
from typing import List, Optional


# ============================================================================
# BASIC EVALUATION EXAMPLES
# ============================================================================


def test_basic_answer_relevancy():
    """
    Test answer relevancy using DeepEval's built-in metric.
    """
    test_case = LLMTestCase(
        input="What is the capital of France?",
        actual_output="The capital of France is Paris, a beautiful city known for the Eiffel Tower.",
        retrieval_context=[
            "Paris is the capital and most populous city of France.",
            "The Eiffel Tower is a landmark in Paris, France.",
        ],
    )

    metric = AnswerRelevancyMetric(threshold=0.7)
    assert_test(test_case, [metric])


def test_faithfulness():
    """
    Test that answer is grounded in provided context (no hallucinations).
    """
    test_case = LLMTestCase(
        input="What are the benefits of exercise?",
        actual_output=(
            "Exercise improves cardiovascular health, strengthens muscles, "
            "and enhances mental well-being."
        ),
        retrieval_context=[
            "Regular exercise improves heart health and circulation.",
            "Physical activity strengthens muscles and bones.",
            "Exercise reduces stress and improves mood.",
        ],
    )

    metric = FaithfulnessMetric(threshold=0.8)
    assert_test(test_case, [metric])


def test_hallucination_detection():
    """
    Test case that should fail due to hallucination.
    """
    test_case = LLMTestCase(
        input="What is the population of Tokyo?",
        actual_output="Tokyo has a population of 50 million people and is the largest city in Europe.",
        retrieval_context=[
            "Tokyo is the capital of Japan with a population of approximately 14 million.",
            "The Greater Tokyo Area has about 37 million residents.",
        ],
    )

    metric = FaithfulnessMetric(threshold=0.8)

    try:
        assert_test(test_case, [metric])
        print("❌ Test should have failed (hallucination not detected)")
    except AssertionError:
        print("✅ Hallucination correctly detected!")


# ============================================================================
# G-EVAL CUSTOM METRICS
# ============================================================================


def test_geval_coherence():
    """
    Use G-Eval to measure text coherence.
    """
    coherence_metric = GEval(
        name="Coherence",
        criteria="Coherence - the logical flow and consistency of the text",
        evaluation_steps=[
            "Assess whether sentences connect logically",
            "Check for smooth transitions between ideas",
            "Verify consistent narrative or argument",
            "Identify any contradictions or gaps",
        ],
        evaluation_params=[LLMTestCase.actual_output],
        threshold=0.7,
    )

    test_case = LLMTestCase(
        input="Explain how photosynthesis works",
        actual_output=(
            "Photosynthesis is the process by which plants convert light energy into chemical energy. "
            "First, chlorophyll in plant cells absorbs sunlight. This energy is then used to convert "
            "carbon dioxide and water into glucose and oxygen. The glucose provides energy for the plant, "
            "while oxygen is released as a byproduct."
        ),
    )

    assert_test(test_case, [coherence_metric])


def test_geval_conciseness():
    """
    Use G-Eval to measure response conciseness.
    """
    conciseness_metric = GEval(
        name="Conciseness",
        criteria="Conciseness - the response is brief and to-the-point without unnecessary details",
        evaluation_steps=[
            "Check if the response directly answers the question",
            "Identify any redundant or repetitive information",
            "Assess if all information is relevant to the query",
            "Verify the response is appropriately brief",
        ],
        evaluation_params=[LLMTestCase.input, LLMTestCase.actual_output],
        threshold=0.7,
    )

    test_case = LLMTestCase(
        input="What is 2+2?",
        actual_output="4",
    )

    assert_test(test_case, [conciseness_metric])


def test_geval_politeness():
    """
    Use G-Eval to measure response politeness and professionalism.
    """
    politeness_metric = GEval(
        name="Politeness",
        criteria="Politeness - the response is courteous, respectful, and professional",
        evaluation_steps=[
            "Check for courteous language and tone",
            "Assess whether response acknowledges the user appropriately",
            "Verify absence of rude, dismissive, or condescending language",
            "Confirm professional and respectful demeanor",
        ],
        evaluation_params=[LLMTestCase.actual_output],
        threshold=0.8,
    )

    test_case = LLMTestCase(
        input="I need help with my account",
        actual_output=(
            "I'd be happy to help you with your account. Could you please provide "
            "more details about the issue you're experiencing? I'm here to assist you."
        ),
    )

    assert_test(test_case, [politeness_metric])


# ============================================================================
# CUSTOM METRIC IMPLEMENTATION
# ============================================================================


from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase


class JSONFormatMetric(BaseMetric):
    """
    Custom metric to verify output is valid JSON with required fields.
    """

    def __init__(
        self,
        required_fields: Optional[List[str]] = None,
        threshold: float = 1.0,
    ):
        self.required_fields = required_fields or []
        self.threshold = threshold

    def measure(self, test_case: LLMTestCase):
        import json

        try:
            # Parse JSON
            output = json.loads(test_case.actual_output)

            # Check required fields
            missing_fields = [
                field for field in self.required_fields if field not in output
            ]

            if missing_fields:
                self.score = 0.0
                self.reason = f"Missing required fields: {missing_fields}"
            else:
                self.score = 1.0
                self.reason = "Valid JSON with all required fields"

        except json.JSONDecodeError as e:
            self.score = 0.0
            self.reason = f"Invalid JSON: {str(e)}"

        self.success = self.score >= self.threshold
        return self.score

    def is_successful(self):
        return self.success

    @property
    def __name__(self):
        return "JSON Format"


def test_json_output_format():
    """
    Test that LLM output is valid JSON with required fields.
    """
    test_case = LLMTestCase(
        input="Extract the name and age from: John is 30 years old",
        actual_output='{"name": "John", "age": 30}',
    )

    metric = JSONFormatMetric(required_fields=["name", "age"])
    assert_test(test_case, [metric])


class ResponseLengthMetric(BaseMetric):
    """
    Custom metric to verify response length is within acceptable range.
    """

    def __init__(
        self,
        min_length: int = 10,
        max_length: int = 500,
        threshold: float = 1.0,
    ):
        self.min_length = min_length
        self.max_length = max_length
        self.threshold = threshold

    def measure(self, test_case: LLMTestCase):
        length = len(test_case.actual_output)

        if length < self.min_length:
            self.score = 0.0
            self.reason = f"Response too short: {length} chars (min: {self.min_length})"
        elif length > self.max_length:
            self.score = 0.0
            self.reason = f"Response too long: {length} chars (max: {self.max_length})"
        else:
            self.score = 1.0
            self.reason = f"Response length appropriate: {length} chars"

        self.success = self.score >= self.threshold
        return self.score

    def is_successful(self):
        return self.success

    @property
    def __name__(self):
        return "Response Length"


def test_response_length():
    """
    Test that response length is within acceptable range.
    """
    test_case = LLMTestCase(
        input="Summarize the main idea in one sentence",
        actual_output="The main idea is that climate change requires immediate action.",
    )

    metric = ResponseLengthMetric(min_length=20, max_length=100)
    assert_test(test_case, [metric])


# ============================================================================
# MULTI-METRIC EVALUATION
# ============================================================================


def test_comprehensive_rag_evaluation():
    """
    Evaluate RAG output with multiple metrics simultaneously.
    """
    test_case = LLMTestCase(
        input="What are the main causes of climate change?",
        actual_output=(
            "The main causes of climate change include greenhouse gas emissions from "
            "burning fossil fuels, deforestation, and industrial processes. These activities "
            "release carbon dioxide and other gases that trap heat in the atmosphere."
        ),
        expected_output=(
            "Climate change is primarily caused by human activities that increase "
            "greenhouse gas concentrations, including fossil fuel combustion and deforestation."
        ),
        retrieval_context=[
            "Burning fossil fuels for energy releases CO2 into the atmosphere.",
            "Deforestation reduces the planet's capacity to absorb CO2.",
            "Industrial processes and agriculture contribute significant greenhouse gases.",
        ],
    )

    # Multiple metrics
    metrics = [
        FaithfulnessMetric(threshold=0.8),
        AnswerRelevancyMetric(threshold=0.7),
        ContextualRelevancyMetric(threshold=0.7),
        ResponseLengthMetric(min_length=50, max_length=300),
    ]

    assert_test(test_case, metrics)


# ============================================================================
# PARAMETRIZED TESTS
# ============================================================================


@pytest.mark.parametrize(
    "query,expected_sentiment",
    [
        ("I love this product!", "positive"),
        ("This is the worst experience ever.", "negative"),
        ("The product is okay, nothing special.", "neutral"),
    ],
)
def test_sentiment_classification(query, expected_sentiment):
    """
    Parametrized test for sentiment classification.
    """
    # Simulate LLM classification
    def classify_sentiment(text: str) -> str:
        # In real scenario, this would call your LLM
        if "love" in text.lower() or "great" in text.lower():
            return "positive"
        elif "worst" in text.lower() or "terrible" in text.lower():
            return "negative"
        else:
            return "neutral"

    result = classify_sentiment(query)
    assert (
        result == expected_sentiment
    ), f"Expected {expected_sentiment}, got {result}"


# ============================================================================
# BATCH EVALUATION
# ============================================================================


def batch_evaluate_test_cases():
    """
    Evaluate multiple test cases in batch.
    """
    test_cases = [
        LLMTestCase(
            input="What is Python?",
            actual_output="Python is a high-level programming language known for its simplicity and readability.",
            retrieval_context=["Python is a popular programming language created by Guido van Rossum."],
        ),
        LLMTestCase(
            input="What is JavaScript?",
            actual_output="JavaScript is a programming language primarily used for web development.",
            retrieval_context=["JavaScript is a scripting language for creating interactive web pages."],
        ),
    ]

    metric = AnswerRelevancyMetric(threshold=0.7)

    results = []
    for i, test_case in enumerate(test_cases):
        try:
            assert_test(test_case, [metric])
            results.append((i, "PASS", metric.score))
            print(f"✅ Test case {i}: PASS (score: {metric.score:.2f})")
        except AssertionError:
            results.append((i, "FAIL", metric.score))
            print(f"❌ Test case {i}: FAIL (score: {metric.score:.2f})")

    # Summary
    passed = sum(1 for _, status, _ in results if status == "PASS")
    total = len(results)
    print(f"\nResults: {passed}/{total} passed ({passed/total*100:.1f}%)")


# ============================================================================
# MAIN EXECUTION
# ============================================================================


if __name__ == "__main__":
    print("=" * 60)
    print("DEEPEVAL FRAMEWORK EXAMPLES")
    print("=" * 60)

    print("\n1. Testing basic metrics...")
    try:
        test_basic_answer_relevancy()
        print("✅ Answer relevancy test passed")
    except Exception as e:
        print(f"❌ Answer relevancy test failed: {e}")

    print("\n2. Testing faithfulness...")
    try:
        test_faithfulness()
        print("✅ Faithfulness test passed")
    except Exception as e:
        print(f"❌ Faithfulness test failed: {e}")

    print("\n3. Testing hallucination detection...")
    test_hallucination_detection()

    print("\n4. Testing G-Eval metrics...")
    try:
        test_geval_coherence()
        print("✅ Coherence test passed")
    except Exception as e:
        print(f"❌ Coherence test failed: {e}")

    print("\n5. Testing custom metrics...")
    try:
        test_json_output_format()
        print("✅ JSON format test passed")
    except Exception as e:
        print(f"❌ JSON format test failed: {e}")

    print("\n6. Running batch evaluation...")
    batch_evaluate_test_cases()

    print("\n" + "=" * 60)
    print("To run with pytest:")
    print("  pytest deepeval_example.py -v")
    print("\nTo run specific tests:")
    print("  pytest deepeval_example.py::test_faithfulness -v")
    print("=" * 60)
