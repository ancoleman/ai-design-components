#!/usr/bin/env python3
"""
RAGAS Evaluation Script (TOKEN-FREE)

Evaluates RAG pipeline quality using RAGAS metrics without loading into context.

Usage:
    python evaluate_rag.py --dataset eval_data.json --output results.json

Dependencies:
    pip install ragas datasets
"""

import argparse
import json
import sys
from pathlib import Path


def validate_dataset(data: dict) -> bool:
    """Validate dataset format."""
    required_fields = ["question", "answer", "contexts", "ground_truth"]

    for field in required_fields:
        if field not in data:
            print(f"Error: Missing required field '{field}'", file=sys.stderr)
            return False

        if not isinstance(data[field], list):
            print(f"Error: Field '{field}' must be a list", file=sys.stderr)
            return False

    # Check all lists same length
    lengths = [len(data[field]) for field in required_fields]
    if len(set(lengths)) > 1:
        print(f"Error: All fields must have same length. Found: {lengths}", file=sys.stderr)
        return False

    return True


def run_evaluation(dataset_path: str, output_path: str = None):
    """Run RAGAS evaluation."""
    try:
        from ragas import evaluate
        from ragas.metrics import (
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall
        )
        from datasets import Dataset
    except ImportError as e:
        print(f"Error: Missing dependencies. Run: pip install ragas datasets", file=sys.stderr)
        print(f"Details: {e}", file=sys.stderr)
        return 1

    # Load dataset
    try:
        with open(dataset_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Dataset not found: {dataset_path}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in dataset: {e}", file=sys.stderr)
        return 1

    # Validate
    if not validate_dataset(data):
        return 1

    # Convert to Dataset
    dataset = Dataset.from_dict(data)

    print(f"Evaluating {len(dataset)} examples...")
    print("This may take a few minutes (using LLM-as-judge)...")

    # Run evaluation
    try:
        result = evaluate(
            dataset,
            metrics=[
                faithfulness,
                answer_relevancy,
                context_precision,
                context_recall
            ]
        )
    except Exception as e:
        print(f"Error during evaluation: {e}", file=sys.stderr)
        return 1

    # Format results
    results = {
        "dataset": dataset_path,
        "num_examples": len(dataset),
        "metrics": {
            "faithfulness": float(result['faithfulness']),
            "answer_relevancy": float(result['answer_relevancy']),
            "context_precision": float(result['context_precision']),
            "context_recall": float(result['context_recall'])
        },
        "quality_check": {
            "faithfulness": "PASS" if result['faithfulness'] > 0.8 else "FAIL",
            "answer_relevancy": "PASS" if result['answer_relevancy'] > 0.7 else "FAIL",
            "context_precision": "PASS" if result['context_precision'] > 0.6 else "FAIL",
            "context_recall": "PASS" if result['context_recall'] > 0.7 else "FAIL"
        }
    }

    # Print results
    print("\n=== RAGAS Evaluation Results ===\n")
    print(f"Dataset: {dataset_path}")
    print(f"Examples: {results['num_examples']}\n")

    print("Metrics:")
    for metric, score in results['metrics'].items():
        status = results['quality_check'][metric]
        print(f"  {metric:20s}: {score:.3f} [{status}]")

    # Check overall quality
    all_pass = all(v == "PASS" for v in results['quality_check'].values())
    print(f"\nOverall Quality: {'PASS' if all_pass else 'FAIL'}")

    # Save to file
    if output_path:
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {output_path}")

    return 0 if all_pass else 1


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate RAG pipeline using RAGAS metrics"
    )
    parser.add_argument(
        "--dataset",
        required=True,
        help="Path to evaluation dataset (JSON file)"
    )
    parser.add_argument(
        "--output",
        help="Path to save results (JSON file)"
    )

    args = parser.parse_args()

    return run_evaluation(args.dataset, args.output)


if __name__ == "__main__":
    sys.exit(main())
