"""
RAG Evaluation with RAGAS Framework

Demonstrates comprehensive RAG system evaluation using the RAGAS library,
measuring faithfulness, answer relevance, context relevance, precision, and recall.

Installation:
    pip install ragas datasets openai langchain

Usage:
    python ragas_example.py
"""

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_relevancy,
    context_precision,
    context_recall,
)
from datasets import Dataset
import openai
import os
from typing import List, Dict


def create_sample_rag_dataset() -> Dataset:
    """
    Create sample RAG evaluation dataset.

    Returns:
        Dataset with question, answer, contexts, and ground_truth
    """
    data = {
        "question": [
            "What is the capital of France?",
            "Who wrote Romeo and Juliet?",
            "What is the speed of light?",
        ],
        "answer": [
            "The capital of France is Paris, a beautiful city known for the Eiffel Tower.",
            "Romeo and Juliet was written by William Shakespeare in the 1590s.",
            "The speed of light in a vacuum is approximately 299,792,458 meters per second.",
        ],
        "contexts": [
            [
                "Paris is the capital and most populous city of France.",
                "The Eiffel Tower is a landmark in Paris, France.",
            ],
            [
                "William Shakespeare was an English playwright and poet.",
                "Romeo and Juliet is a tragedy written by Shakespeare around 1594-1596.",
            ],
            [
                "The speed of light in vacuum is 299,792,458 m/s.",
                "Light travels slower in other mediums like water or glass.",
            ],
        ],
        "ground_truth": [
            "Paris",
            "William Shakespeare",
            "299,792,458 meters per second",
        ],
    }

    return Dataset.from_dict(data)


def evaluate_rag_system(dataset: Dataset) -> Dict[str, float]:
    """
    Evaluate RAG system using RAGAS metrics.

    Args:
        dataset: Dataset with required fields (question, answer, contexts, ground_truth)

    Returns:
        Dictionary of metric scores
    """
    # Ensure OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable must be set")

    # Run evaluation
    print("Running RAGAS evaluation...")
    results = evaluate(
        dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_relevancy,
            context_precision,
            context_recall,
        ],
    )

    return results


def interpret_ragas_scores(results: Dict[str, float]) -> None:
    """
    Interpret RAGAS scores and provide recommendations.

    Args:
        results: Dictionary of metric scores from RAGAS evaluation
    """
    print("\n" + "=" * 60)
    print("RAGAS EVALUATION RESULTS")
    print("=" * 60)

    metrics_info = {
        "faithfulness": {
            "description": "Answer grounded in context (prevents hallucinations)",
            "target": 0.8,
            "critical": True,
        },
        "answer_relevancy": {
            "description": "Answer addresses the query",
            "target": 0.7,
            "critical": True,
        },
        "context_relevancy": {
            "description": "Retrieved chunks are relevant",
            "target": 0.7,
            "critical": False,
        },
        "context_precision": {
            "description": "Relevant chunks ranked higher",
            "target": 0.5,
            "critical": False,
        },
        "context_recall": {
            "description": "All relevant chunks retrieved",
            "target": 0.8,
            "critical": False,
        },
    }

    for metric_name, score in results.items():
        if metric_name not in metrics_info:
            continue

        info = metrics_info[metric_name]
        status = "✅" if score >= info["target"] else "⚠️"
        priority = "CRITICAL" if info["critical"] else "Important"

        print(f"\n{status} {metric_name.upper()}: {score:.3f} (Target: {info['target']})")
        print(f"   {info['description']}")
        print(f"   Priority: {priority}")

        # Provide recommendations if below target
        if score < info["target"]:
            print(f"   📋 RECOMMENDATION:")
            if metric_name == "faithfulness":
                print(f"      - Adjust prompt: 'Only use information from context'")
                print(f"      - Require citations to context chunks")
                print(f"      - Add post-processing to filter unsupported claims")
            elif metric_name == "answer_relevancy":
                print(f"      - Improve prompt instructions")
                print(f"      - Add few-shot examples of good answers")
                print(f"      - Ensure context contains relevant information")
            elif metric_name == "context_relevancy":
                print(f"      - Improve retrieval (better embeddings, hybrid search)")
                print(f"      - Tune retrieval parameters (top-k, similarity threshold)")
                print(f"      - Add query rewriting or expansion")
            elif metric_name == "context_precision":
                print(f"      - Add re-ranking step (cross-encoder)")
                print(f"      - Improve retrieval scoring function")
                print(f"      - Use hybrid search (keyword + semantic)")
            elif metric_name == "context_recall":
                print(f"      - Increase retrieval count (top-k)")
                print(f"      - Improve chunking strategy (smaller chunks)")
                print(f"      - Use query expansion")


def evaluate_single_interaction(
    question: str,
    answer: str,
    contexts: List[str],
    ground_truth: str = None,
) -> Dict[str, float]:
    """
    Evaluate a single RAG interaction.

    Args:
        question: User query
        answer: LLM-generated answer
        contexts: Retrieved context chunks
        ground_truth: Reference answer (optional)

    Returns:
        Dictionary of metric scores
    """
    data = {
        "question": [question],
        "answer": [answer],
        "contexts": [contexts],
    }

    if ground_truth:
        data["ground_truth"] = [ground_truth]

    dataset = Dataset.from_dict(data)

    # Use subset of metrics if no ground truth
    metrics_to_use = (
        [faithfulness, answer_relevancy, context_relevancy]
        if not ground_truth
        else [faithfulness, answer_relevancy, context_relevancy, context_recall]
    )

    results = evaluate(dataset, metrics=metrics_to_use)
    return results


def batch_evaluation_example():
    """
    Example of batch evaluation on custom RAG dataset.
    """
    print("=" * 60)
    print("BATCH RAG EVALUATION EXAMPLE")
    print("=" * 60)

    # Create sample dataset
    dataset = create_sample_rag_dataset()

    print(f"\nEvaluating {len(dataset)} RAG interactions...")
    print(f"Metrics: Faithfulness, Answer Relevance, Context Relevance, Precision, Recall")

    # Run evaluation
    try:
        results = evaluate_rag_system(dataset)
        interpret_ragas_scores(results)

        # Overall assessment
        print("\n" + "=" * 60)
        print("OVERALL ASSESSMENT")
        print("=" * 60)

        faithfulness_score = results.get("faithfulness", 0)
        answer_relevancy_score = results.get("answer_relevancy", 0)

        if faithfulness_score >= 0.8 and answer_relevancy_score >= 0.7:
            print("✅ RAG system is performing well!")
            print("   All critical metrics meet targets.")
        elif faithfulness_score < 0.8:
            print("⚠️  CRITICAL: Faithfulness below target!")
            print("   Risk of hallucinations. Address immediately.")
        elif answer_relevancy_score < 0.7:
            print("⚠️  Answer relevance needs improvement")
            print("   Responses may not fully address queries.")
        else:
            print("⚠️  Some metrics need improvement")
            print("   Review recommendations above.")

    except Exception as e:
        print(f"\n❌ Error during evaluation: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure OPENAI_API_KEY is set: export OPENAI_API_KEY=your_key")
        print("2. Install dependencies: pip install ragas datasets openai")
        print("3. Check internet connection (RAGAS requires API access)")


def single_interaction_example():
    """
    Example of evaluating a single RAG interaction.
    """
    print("\n" + "=" * 60)
    print("SINGLE INTERACTION EVALUATION EXAMPLE")
    print("=" * 60)

    # Example interaction
    question = "What are the health benefits of exercise?"
    answer = (
        "Exercise has numerous health benefits including improved cardiovascular health, "
        "stronger muscles and bones, and better mental health. It can reduce the risk of "
        "chronic diseases like diabetes and heart disease."
    )
    contexts = [
        "Regular physical activity improves cardiovascular health and reduces heart disease risk.",
        "Exercise strengthens muscles and bones, reducing osteoporosis risk.",
        "Physical activity has mental health benefits, reducing anxiety and depression.",
        "Studies show exercise helps prevent type 2 diabetes.",
    ]
    ground_truth = (
        "Exercise improves cardiovascular health, strengthens muscles and bones, "
        "enhances mental health, and reduces chronic disease risk."
    )

    print(f"\nQuestion: {question}")
    print(f"Answer: {answer[:100]}...")
    print(f"Contexts: {len(contexts)} chunks")

    try:
        results = evaluate_single_interaction(question, answer, contexts, ground_truth)

        print("\nResults:")
        for metric, score in results.items():
            status = "✅" if score >= 0.7 else "⚠️"
            print(f"{status} {metric}: {score:.3f}")

    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set")
        print("Set it with: export OPENAI_API_KEY=your_key")
        print("\nRunning examples anyway (will fail at evaluation step)...\n")

    # Run examples
    batch_evaluation_example()
    single_interaction_example()

    print("\n" + "=" * 60)
    print("RAGAS EVALUATION COMPLETE")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Replace sample data with your actual RAG system outputs")
    print("2. Set target thresholds based on your use case")
    print("3. Integrate into CI/CD for regression testing")
    print("4. Monitor metrics in production (sample 5-10% of outputs)")
