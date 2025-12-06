#!/usr/bin/env python3
"""
RAGAS-Based RAG Evaluation Script

Evaluates RAG pipeline quality using RAGAS metrics:
- Faithfulness: Is the answer grounded in retrieved context?
- Answer Relevancy: Does the answer address the question?
- Context Precision: Are retrieved chunks relevant?
- Context Recall: Were all necessary chunks retrieved?

Usage:
    python scripts/evaluate_rag.py --dataset eval_data.json --output results.json
    python scripts/evaluate_rag.py --dataset eval_data.json --metrics faithfulness answer_relevancy
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

# Check dependencies
try:
    from ragas import evaluate
    from ragas.metrics import (
        faithfulness,
        answer_relevancy,
        context_recall,
        context_precision,
    )
    from datasets import Dataset
except ImportError as e:
    print(f"Error: Missing required package: {e.name}")
    print("\nInstall dependencies:")
    print("  pip install ragas datasets")
    sys.exit(1)


def load_evaluation_dataset(file_path: str) -> Dataset:
    """
    Load evaluation dataset from JSON file.

    Expected format:
    {
        "questions": ["Question 1", "Question 2"],
        "answers": ["Answer 1", "Answer 2"],
        "contexts": [["Context chunk 1", "Context chunk 2"], ["Context chunk 3"]],
        "ground_truths": ["Ground truth 1", "Ground truth 2"]
    }
    """
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Validate required keys
    required_keys = ["questions", "answers", "contexts"]
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing required key '{key}' in dataset")

    # Convert to RAGAS format
    ragas_data = {
        "question": data["questions"],
        "answer": data["answers"],
        "contexts": data["contexts"],
    }

    # Ground truth is optional but recommended
    if "ground_truths" in data:
        ragas_data["ground_truth"] = data["ground_truths"]

    return Dataset.from_dict(ragas_data)


def run_evaluation(
    dataset: Dataset,
    metrics: List[str] = None,
) -> Dict[str, Any]:
    """Run RAGAS evaluation on dataset"""

    # Available metrics
    metric_map = {
        "faithfulness": faithfulness,
        "answer_relevancy": answer_relevancy,
        "context_recall": context_recall,
        "context_precision": context_precision,
    }

    # Use all metrics if none specified
    if metrics is None:
        metrics = list(metric_map.keys())

    # Validate metrics
    invalid_metrics = set(metrics) - set(metric_map.keys())
    if invalid_metrics:
        raise ValueError(f"Invalid metrics: {invalid_metrics}. Valid: {list(metric_map.keys())}")

    # Select metrics
    selected_metrics = [metric_map[m] for m in metrics]

    print(f"Evaluating {len(dataset)} samples with metrics: {', '.join(metrics)}")
    print("-" * 60)

    # Run evaluation
    result = evaluate(dataset, metrics=selected_metrics)

    return result


def save_results(results: Dict[str, Any], output_path: str):
    """Save evaluation results to JSON file"""
    output = {
        "metrics": {k: float(v) for k, v in results.items()},
        "summary": generate_summary(results),
    }

    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to: {output_path}")


def generate_summary(results: Dict[str, Any]) -> Dict[str, str]:
    """Generate human-readable summary of results"""
    summary = {}

    thresholds = {
        "faithfulness": 0.90,
        "answer_relevancy": 0.85,
        "context_recall": 0.80,
        "context_precision": 0.75,
    }

    for metric, score in results.items():
        threshold = thresholds.get(metric, 0.70)

        if score >= threshold:
            status = "✓ PASS"
        else:
            status = "✗ FAIL"

        summary[metric] = f"{status} - {score:.3f} (target: {threshold:.2f})"

    return summary


def print_results(results: Dict[str, Any]):
    """Print results to console"""
    print("\n" + "=" * 60)
    print("RAGAS Evaluation Results")
    print("=" * 60)

    for metric, score in results.items():
        print(f"{metric:20s}: {score:.4f}")

    print("\nProduction Quality Targets:")
    print("  Faithfulness:       > 0.90  (minimal hallucination)")
    print("  Answer Relevancy:   > 0.85  (addresses user query)")
    print("  Context Recall:     > 0.80  (sufficient context retrieved)")
    print("  Context Precision:  > 0.75  (minimal noise)")


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate RAG pipeline using RAGAS metrics"
    )
    parser.add_argument(
        "--dataset",
        required=True,
        help="Path to evaluation dataset JSON file"
    )
    parser.add_argument(
        "--output",
        help="Path to save results JSON file (default: results.json)",
        default="results.json"
    )
    parser.add_argument(
        "--metrics",
        nargs="+",
        choices=["faithfulness", "answer_relevancy", "context_recall", "context_precision"],
        help="Metrics to evaluate (default: all)",
        default=None
    )

    args = parser.parse_args()

    # Validate dataset file exists
    if not Path(args.dataset).exists():
        print(f"Error: Dataset file not found: {args.dataset}")
        sys.exit(1)

    try:
        # Load dataset
        print(f"Loading dataset from: {args.dataset}")
        dataset = load_evaluation_dataset(args.dataset)

        # Run evaluation
        results = run_evaluation(dataset, args.metrics)

        # Print results
        print_results(results)

        # Save results
        save_results(results, args.output)

        # Exit with non-zero if any metric fails
        thresholds = {
            "faithfulness": 0.90,
            "answer_relevancy": 0.85,
            "context_recall": 0.80,
            "context_precision": 0.75,
        }

        failed = [
            metric for metric, score in results.items()
            if score < thresholds.get(metric, 0.70)
        ]

        if failed:
            print(f"\n⚠ Warning: {len(failed)} metric(s) below threshold: {', '.join(failed)}")
            sys.exit(1)
        else:
            print("\n✓ All metrics meet production quality targets")
            sys.exit(0)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
