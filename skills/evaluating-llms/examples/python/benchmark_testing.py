"""
Benchmark Testing for LLM Systems

Demonstrates running standardized benchmarks (MMLU, HumanEval-style) and
creating custom benchmarks for domain-specific evaluation.

Installation:
    pip install openai datasets

Usage:
    python benchmark_testing.py
"""

import os
import json
from typing import List, Dict, Any
from dataclasses import dataclass
from openai import OpenAI
from datasets import load_dataset


@dataclass
class BenchmarkResult:
    """Result from benchmark evaluation."""

    total_questions: int
    correct: int
    accuracy: float
    details: List[Dict[str, Any]]


# ============================================================================
# MMLU-STYLE MULTIPLE CHOICE BENCHMARK
# ============================================================================


def run_mmlu_style_benchmark(
    questions: List[Dict[str, Any]],
    model: str = "gpt-3.5-turbo",
) -> BenchmarkResult:
    """
    Run MMLU-style multiple choice benchmark.

    Args:
        questions: List of questions with format:
            {
                "question": "What is...",
                "choices": ["A) ...", "B) ...", "C) ...", "D) ..."],
                "correct_answer": "A"
            }
        model: Model to evaluate

    Returns:
        BenchmarkResult with accuracy and details
    """
    client = OpenAI()
    correct = 0
    details = []

    for i, q in enumerate(questions):
        # Format prompt
        choices_text = "\n".join(q["choices"])
        prompt = f"{q['question']}\n\n{choices_text}\n\nAnswer with only the letter (A, B, C, or D):"

        # Get model response
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=1,
        )

        predicted = response.choices[0].message.content.strip().upper()

        # Check correctness
        is_correct = predicted == q["correct_answer"]
        if is_correct:
            correct += 1

        details.append(
            {
                "question_id": i,
                "question": q["question"],
                "predicted": predicted,
                "correct_answer": q["correct_answer"],
                "is_correct": is_correct,
            }
        )

    accuracy = correct / len(questions) if questions else 0.0

    return BenchmarkResult(
        total_questions=len(questions),
        correct=correct,
        accuracy=accuracy,
        details=details,
    )


def create_sample_mmlu_benchmark() -> List[Dict[str, Any]]:
    """Create sample MMLU-style questions."""
    return [
        {
            "question": "What is the capital of France?",
            "choices": ["A) London", "B) Berlin", "C) Paris", "D) Rome"],
            "correct_answer": "C",
        },
        {
            "question": "What is the chemical symbol for gold?",
            "choices": ["A) Go", "B) Au", "C) Gd", "D) Ag"],
            "correct_answer": "B",
        },
        {
            "question": "Who wrote 'Romeo and Juliet'?",
            "choices": [
                "A) Charles Dickens",
                "B) William Shakespeare",
                "C) Jane Austen",
                "D) Mark Twain",
            ],
            "correct_answer": "B",
        },
        {
            "question": "What is the speed of light in vacuum?",
            "choices": [
                "A) 300,000 km/s",
                "B) 150,000 km/s",
                "C) 450,000 km/s",
                "D) 600,000 km/s",
            ],
            "correct_answer": "A",
        },
        {
            "question": "Which planet is known as the Red Planet?",
            "choices": ["A) Venus", "B) Mars", "C) Jupiter", "D) Saturn"],
            "correct_answer": "B",
        },
    ]


# ============================================================================
# HUMANEVAL-STYLE CODE GENERATION BENCHMARK
# ============================================================================


def run_code_benchmark(
    problems: List[Dict[str, Any]],
    model: str = "gpt-3.5-turbo",
) -> BenchmarkResult:
    """
    Run HumanEval-style code generation benchmark.

    Args:
        problems: List of coding problems with format:
            {
                "prompt": "def function_name(...):\n    '''...",
                "test_cases": [
                    {"input": [...], "expected_output": ...},
                    ...
                ]
            }
        model: Model to evaluate

    Returns:
        BenchmarkResult with pass rate
    """
    client = OpenAI()
    passed = 0
    details = []

    for i, problem in enumerate(problems):
        # Get code generation
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Complete the Python function. Return only the code.",
                },
                {"role": "user", "content": problem["prompt"]},
            ],
            temperature=0,
        )

        generated_code = response.choices[0].message.content

        # Test generated code
        test_results = []
        all_passed = True

        for test_case in problem["test_cases"]:
            try:
                # Execute code with test input
                local_scope = {}
                exec(generated_code, local_scope)

                # Get function name from prompt
                func_name = problem["prompt"].split("(")[0].replace("def ", "").strip()
                result = local_scope[func_name](*test_case["input"])

                passed_test = result == test_case["expected_output"]
                test_results.append(
                    {
                        "input": test_case["input"],
                        "expected": test_case["expected_output"],
                        "actual": result,
                        "passed": passed_test,
                    }
                )

                if not passed_test:
                    all_passed = False

            except Exception as e:
                test_results.append(
                    {
                        "input": test_case["input"],
                        "expected": test_case["expected_output"],
                        "error": str(e),
                        "passed": False,
                    }
                )
                all_passed = False

        if all_passed:
            passed += 1

        details.append(
            {
                "problem_id": i,
                "prompt": problem["prompt"][:100] + "...",
                "generated_code": generated_code,
                "test_results": test_results,
                "all_tests_passed": all_passed,
            }
        )

    pass_rate = passed / len(problems) if problems else 0.0

    return BenchmarkResult(
        total_questions=len(problems),
        correct=passed,
        accuracy=pass_rate,
        details=details,
    )


def create_sample_code_benchmark() -> List[Dict[str, Any]]:
    """Create sample coding problems."""
    return [
        {
            "prompt": """def add(a, b):
    '''Return the sum of a and b.'''""",
            "test_cases": [
                {"input": [2, 3], "expected_output": 5},
                {"input": [0, 0], "expected_output": 0},
                {"input": [-1, 1], "expected_output": 0},
            ],
        },
        {
            "prompt": """def is_even(n):
    '''Return True if n is even, False otherwise.'''""",
            "test_cases": [
                {"input": [4], "expected_output": True},
                {"input": [3], "expected_output": False},
                {"input": [0], "expected_output": True},
            ],
        },
        {
            "prompt": """def reverse_string(s):
    '''Return the reversed string.'''""",
            "test_cases": [
                {"input": ["hello"], "expected_output": "olleh"},
                {"input": [""], "expected_output": ""},
                {"input": ["a"], "expected_output": "a"},
            ],
        },
    ]


# ============================================================================
# CUSTOM DOMAIN BENCHMARK
# ============================================================================


def run_qa_benchmark(
    questions: List[Dict[str, str]],
    model: str = "gpt-3.5-turbo",
) -> BenchmarkResult:
    """
    Run question-answering benchmark with exact match scoring.

    Args:
        questions: List of questions with format:
            {"question": "...", "answer": "..."}
        model: Model to evaluate

    Returns:
        BenchmarkResult with exact match score
    """
    client = OpenAI()
    correct = 0
    details = []

    for i, q in enumerate(questions):
        # Get model response
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Answer concisely."},
                {"role": "user", "content": q["question"]},
            ],
            temperature=0,
        )

        predicted = response.choices[0].message.content.strip().lower()
        expected = q["answer"].lower()

        # Check exact match
        is_correct = predicted == expected

        # Also check if expected is substring of predicted (partial credit)
        partial_match = expected in predicted

        if is_correct:
            correct += 1

        details.append(
            {
                "question_id": i,
                "question": q["question"],
                "predicted": predicted,
                "expected": expected,
                "exact_match": is_correct,
                "partial_match": partial_match,
            }
        )

    accuracy = correct / len(questions) if questions else 0.0

    return BenchmarkResult(
        total_questions=len(questions),
        correct=correct,
        accuracy=accuracy,
        details=details,
    )


def create_custom_domain_benchmark() -> List[Dict[str, str]]:
    """Create custom domain-specific benchmark (e.g., customer support)."""
    return [
        {
            "question": "How do I reset my password?",
            "answer": "Click 'Forgot Password' on the login page.",
        },
        {
            "question": "What is your refund policy?",
            "answer": "30-day money-back guarantee.",
        },
        {
            "question": "How long does shipping take?",
            "answer": "3-5 business days.",
        },
    ]


# ============================================================================
# BENCHMARK COMPARISON
# ============================================================================


def compare_models(
    benchmark_fn,
    benchmark_data: List[Dict[str, Any]],
    models: List[str],
) -> Dict[str, BenchmarkResult]:
    """
    Compare multiple models on same benchmark.

    Args:
        benchmark_fn: Benchmark function to run
        benchmark_data: Benchmark questions/problems
        models: List of model names to compare

    Returns:
        Dictionary mapping model name to BenchmarkResult
    """
    results = {}

    for model in models:
        print(f"\nEvaluating {model}...")
        result = benchmark_fn(benchmark_data, model=model)
        results[model] = result

    return results


# ============================================================================
# REPORTING
# ============================================================================


def print_benchmark_report(result: BenchmarkResult, benchmark_name: str):
    """Print formatted benchmark results."""
    print("\n" + "=" * 60)
    print(f"{benchmark_name} RESULTS")
    print("=" * 60)
    print(f"Total Questions: {result.total_questions}")
    print(f"Correct: {result.correct}")
    print(f"Accuracy: {result.accuracy:.1%}")

    # Show failures
    failures = [d for d in result.details if not d.get("is_correct", d.get("all_tests_passed", False))]

    if failures:
        print(f"\nFailures ({len(failures)}):")
        for fail in failures[:5]:  # Show first 5
            if "question" in fail:
                print(f"  - Q: {fail['question'][:60]}...")
                print(f"    Predicted: {fail['predicted']}, Correct: {fail['correct_answer']}")
            elif "prompt" in fail:
                print(f"  - Problem: {fail['prompt'][:60]}...")
                print(f"    Tests passed: {sum(t.get('passed', False) for t in fail['test_results'])}/{len(fail['test_results'])}")


def print_model_comparison(results: Dict[str, BenchmarkResult]):
    """Print model comparison table."""
    print("\n" + "=" * 60)
    print("MODEL COMPARISON")
    print("=" * 60)
    print(f"{'Model':<20} {'Accuracy':<15} {'Correct/Total'}")
    print("-" * 60)

    for model, result in results.items():
        print(
            f"{model:<20} {result.accuracy:>6.1%}         {result.correct}/{result.total_questions}"
        )


# ============================================================================
# EXAMPLES
# ============================================================================


def example_mmlu_benchmark():
    """Example: Run MMLU-style benchmark."""
    print("\n" + "=" * 60)
    print("MMLU-STYLE BENCHMARK EXAMPLE")
    print("=" * 60)

    questions = create_sample_mmlu_benchmark()
    result = run_mmlu_style_benchmark(questions, model="gpt-3.5-turbo")
    print_benchmark_report(result, "MMLU-Style Multiple Choice")


def example_code_benchmark():
    """Example: Run code generation benchmark."""
    print("\n" + "=" * 60)
    print("CODE GENERATION BENCHMARK EXAMPLE")
    print("=" * 60)

    problems = create_sample_code_benchmark()
    result = run_code_benchmark(problems, model="gpt-3.5-turbo")
    print_benchmark_report(result, "HumanEval-Style Code Generation")


def example_custom_benchmark():
    """Example: Run custom domain benchmark."""
    print("\n" + "=" * 60)
    print("CUSTOM DOMAIN BENCHMARK EXAMPLE")
    print("=" * 60)

    questions = create_custom_domain_benchmark()
    result = run_qa_benchmark(questions, model="gpt-3.5-turbo")
    print_benchmark_report(result, "Customer Support Q&A")


def example_model_comparison():
    """Example: Compare multiple models."""
    print("\n" + "=" * 60)
    print("MODEL COMPARISON EXAMPLE")
    print("=" * 60)

    questions = create_sample_mmlu_benchmark()
    models = ["gpt-3.5-turbo", "gpt-4"]

    results = compare_models(run_mmlu_style_benchmark, questions, models)
    print_model_comparison(results)


# ============================================================================
# MAIN
# ============================================================================


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Error: OPENAI_API_KEY not set")
        print("Set it with: export OPENAI_API_KEY=your_key")
        exit(1)

    print("=" * 60)
    print("BENCHMARK TESTING FOR LLM SYSTEMS")
    print("=" * 60)

    try:
        example_mmlu_benchmark()
        example_code_benchmark()
        example_custom_benchmark()
        # example_model_comparison()  # Uncomment to compare models (costs more)

        print("\n" + "=" * 60)
        print("BENCHMARK TESTING COMPLETE")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Create domain-specific benchmarks for your use case")
        print("2. Run benchmarks in CI/CD for regression testing")
        print("3. Track benchmark scores over time")
        print("4. Compare different models to select best for your needs")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Verify OPENAI_API_KEY is set correctly")
        print("2. Check internet connection")
        print("3. Ensure sufficient API credits")
