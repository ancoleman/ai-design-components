"""
Unit Testing for LLM Outputs

Demonstrates unit testing patterns for LLM systems using pytest, including
exact match, fuzzy matching, semantic similarity, and deterministic assertions.

Installation:
    pip install pytest openai sentence-transformers scikit-learn

Usage:
    pytest unit_evaluation.py -v
    # Or run directly:
    python unit_evaluation.py
"""

import pytest
import re
import json
from typing import List, Dict, Any
from openai import OpenAI
import os


# ============================================================================
# EXACT MATCH TESTING
# ============================================================================


def classify_sentiment(text: str, model: str = "gpt-3.5-turbo") -> str:
    """Classify sentiment of text (positive/negative/neutral)."""
    client = OpenAI()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Classify sentiment as positive, negative, or neutral. Return only the label.",
            },
            {"role": "user", "content": text},
        ],
        temperature=0,
    )

    return response.choices[0].message.content.strip().lower()


def test_positive_sentiment():
    """Test exact match for positive sentiment."""
    result = classify_sentiment("I love this product!")
    assert result == "positive", f"Expected 'positive', got '{result}'"


def test_negative_sentiment():
    """Test exact match for negative sentiment."""
    result = classify_sentiment("This is terrible and disappointing.")
    assert result == "negative", f"Expected 'negative', got '{result}'"


def test_neutral_sentiment():
    """Test exact match for neutral sentiment."""
    result = classify_sentiment("The product arrived on time.")
    assert result == "neutral", f"Expected 'neutral', got '{result}'"


# ============================================================================
# REGEX PATTERN MATCHING
# ============================================================================


def extract_email(text: str, model: str = "gpt-3.5-turbo") -> str:
    """Extract email address from text."""
    client = OpenAI()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Extract the email address from the text. Return only the email.",
            },
            {"role": "user", "content": text},
        ],
        temperature=0,
    )

    return response.choices[0].message.content.strip()


def test_email_extraction_format():
    """Test email extraction returns valid email format."""
    text = "Please contact me at john.doe@example.com for more information."
    result = extract_email(text)

    # Regex pattern for email validation
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    assert re.match(email_pattern, result), f"Invalid email format: {result}"


def test_email_extraction_correct():
    """Test email extraction returns correct email."""
    text = "Contact support@company.com for help."
    result = extract_email(text)
    assert result == "support@company.com", f"Expected 'support@company.com', got '{result}'"


# ============================================================================
# JSON SCHEMA VALIDATION
# ============================================================================


def extract_structured_data(text: str, model: str = "gpt-3.5-turbo") -> str:
    """Extract structured data as JSON."""
    client = OpenAI()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Extract name, age, and city as JSON: {\"name\": \"...\", \"age\": ..., \"city\": \"...\"}",
            },
            {"role": "user", "content": text},
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )

    return response.choices[0].message.content


def test_json_valid_format():
    """Test JSON output is valid."""
    text = "John Smith is 35 years old and lives in San Francisco."
    result = extract_structured_data(text)

    # Should parse without error
    data = json.loads(result)
    assert isinstance(data, dict), "Output is not a valid JSON object"


def test_json_required_fields():
    """Test JSON contains required fields."""
    text = "Jane Doe is 28 years old and lives in New York."
    result = extract_structured_data(text)

    data = json.loads(result)
    required_fields = ["name", "age", "city"]

    for field in required_fields:
        assert field in data, f"Missing required field: {field}"


def test_json_field_types():
    """Test JSON field types are correct."""
    text = "Bob Johnson is 42 years old and lives in Chicago."
    result = extract_structured_data(text)

    data = json.loads(result)

    assert isinstance(data["name"], str), "name should be string"
    assert isinstance(data["age"], int), "age should be integer"
    assert isinstance(data["city"], str), "city should be string"


# ============================================================================
# KEYWORD PRESENCE TESTING
# ============================================================================


def generate_summary(text: str, model: str = "gpt-3.5-turbo") -> str:
    """Generate summary of text."""
    client = OpenAI()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Summarize the following text in 2-3 sentences."},
            {"role": "user", "content": text},
        ],
        temperature=0,
    )

    return response.choices[0].message.content


def test_summary_contains_keywords():
    """Test summary contains important keywords."""
    text = (
        "Climate change is causing rising global temperatures. "
        "Scientists warn that immediate action is needed to reduce greenhouse gas emissions. "
        "Renewable energy sources are crucial for addressing this challenge."
    )

    result = generate_summary(text)

    # Check for important keywords
    keywords = ["climate", "temperature", "emission", "energy"]

    # At least 2 keywords should appear
    found_keywords = [kw for kw in keywords if kw.lower() in result.lower()]
    assert (
        len(found_keywords) >= 2
    ), f"Summary missing key concepts. Found only: {found_keywords}"


def test_summary_length():
    """Test summary is appropriately concise."""
    text = "Lorem ipsum dolor sit amet. " * 50  # Long text

    result = generate_summary(text)
    word_count = len(result.split())

    assert 10 <= word_count <= 100, f"Summary length inappropriate: {word_count} words"


# ============================================================================
# FUZZY MATCHING
# ============================================================================


def normalize_text(text: str) -> str:
    """Normalize text for fuzzy comparison."""
    # Lowercase, remove punctuation, strip whitespace
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = " ".join(text.split())
    return text


def fuzzy_match(text1: str, text2: str, threshold: float = 0.8) -> bool:
    """Check if two texts are similar enough (fuzzy match)."""
    from difflib import SequenceMatcher

    norm1 = normalize_text(text1)
    norm2 = normalize_text(text2)

    similarity = SequenceMatcher(None, norm1, norm2).ratio()
    return similarity >= threshold


def answer_question(question: str, model: str = "gpt-3.5-turbo") -> str:
    """Answer a question."""
    client = OpenAI()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Answer the question concisely."},
            {"role": "user", "content": question},
        ],
        temperature=0,
    )

    return response.choices[0].message.content


def test_fuzzy_answer_match():
    """Test answer is close enough to expected (fuzzy match)."""
    question = "What is the capital of Japan?"
    expected = "Tokyo"

    result = answer_question(question)

    assert fuzzy_match(
        result, expected, threshold=0.5
    ), f"Answer '{result}' doesn't match expected '{expected}'"


# ============================================================================
# SEMANTIC SIMILARITY
# ============================================================================


def semantic_similarity(text1: str, text2: str) -> float:
    """
    Compute semantic similarity using sentence embeddings.

    Returns:
        Similarity score between 0 and 1
    """
    from sentence_transformers import SentenceTransformer, util

    model = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings = model.encode([text1, text2])
    similarity = util.cos_sim(embeddings[0], embeddings[1]).item()

    return similarity


def test_semantic_similarity_high():
    """Test answer is semantically similar to expected."""
    question = "What are the benefits of exercise?"
    expected = "Exercise improves health, fitness, and mental wellbeing."

    result = answer_question(question)
    similarity = semantic_similarity(result, expected)

    assert (
        similarity >= 0.6
    ), f"Semantic similarity too low: {similarity:.2f} (expected >= 0.6)"


# ============================================================================
# PARAMETRIZED TESTS
# ============================================================================


@pytest.mark.parametrize(
    "input_text,expected_label",
    [
        ("I absolutely love this!", "positive"),
        ("This is awful and terrible.", "negative"),
        ("The package arrived.", "neutral"),
        ("Amazing product, highly recommend!", "positive"),
    ],
)
def test_sentiment_parametrized(input_text, expected_label):
    """Parametrized test for multiple sentiment examples."""
    result = classify_sentiment(input_text)
    assert result == expected_label, f"Expected {expected_label}, got {result}"


# ============================================================================
# BINARY PASS/FAIL TESTS
# ============================================================================


def is_response_helpful(response: str) -> bool:
    """
    Check if response is helpful (basic heuristics).

    Returns:
        True if response appears helpful
    """
    # Basic checks
    if len(response) < 10:
        return False

    unhelpful_phrases = [
        "i don't know",
        "i cannot help",
        "i can't answer",
        "no information",
    ]

    response_lower = response.lower()
    if any(phrase in response_lower for phrase in unhelpful_phrases):
        return False

    return True


def test_response_is_helpful():
    """Test response passes basic helpfulness checks."""
    question = "How do I reset my password?"
    result = answer_question(question)

    assert is_response_helpful(
        result
    ), f"Response not helpful: {result}"


# ============================================================================
# DETERMINISTIC BEHAVIOR TESTS
# ============================================================================


def test_deterministic_output():
    """Test that same input produces consistent output (temperature=0)."""
    question = "What is 2+2?"

    result1 = answer_question(question)
    result2 = answer_question(question)

    # With temperature=0, should be identical or very similar
    assert fuzzy_match(
        result1, result2, threshold=0.9
    ), f"Output not deterministic: '{result1}' vs '{result2}'"


# ============================================================================
# MAIN EXECUTION
# ============================================================================


def run_all_tests():
    """Run all tests programmatically."""
    print("=" * 60)
    print("RUNNING UNIT TESTS FOR LLM OUTPUTS")
    print("=" * 60)

    test_functions = [
        ("Positive Sentiment", test_positive_sentiment),
        ("Negative Sentiment", test_negative_sentiment),
        ("Neutral Sentiment", test_neutral_sentiment),
        ("Email Format", test_email_extraction_format),
        ("JSON Format", test_json_valid_format),
        ("JSON Fields", test_json_required_fields),
        ("Summary Keywords", test_summary_contains_keywords),
        ("Fuzzy Match", test_fuzzy_answer_match),
        ("Helpful Response", test_response_is_helpful),
        ("Deterministic Output", test_deterministic_output),
    ]

    passed = 0
    failed = 0

    for name, test_fn in test_functions:
        try:
            test_fn()
            print(f"✅ {name}: PASS")
            passed += 1
        except AssertionError as e:
            print(f"❌ {name}: FAIL - {e}")
            failed += 1
        except Exception as e:
            print(f"⚠️  {name}: ERROR - {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set")
        print("Set it with: export OPENAI_API_KEY=your_key")
        print("\nSome tests will fail without API key.\n")

    print("Run with pytest for better output:")
    print("  pytest unit_evaluation.py -v\n")
    print("Running tests programmatically...\n")

    run_all_tests()
