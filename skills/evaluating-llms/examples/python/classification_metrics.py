"""
Classification Metrics for LLM Evaluation

Demonstrates using standard classification metrics (accuracy, precision, recall, F1)
to evaluate LLM classification tasks like sentiment analysis, intent detection, etc.

Installation:
    pip install scikit-learn numpy matplotlib seaborn

Usage:
    python classification_metrics.py
"""

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    precision_recall_fscore_support,
    confusion_matrix,
    classification_report,
)
from typing import List, Dict, Tuple
import warnings

warnings.filterwarnings("ignore")


# ============================================================================
# SAMPLE DATA
# ============================================================================


def create_sample_predictions() -> Tuple[List[str], List[str]]:
    """
    Create sample true labels and predictions for sentiment classification.

    Returns:
        Tuple of (y_true, y_pred)
    """
    y_true = [
        "positive",
        "negative",
        "neutral",
        "positive",
        "negative",
        "positive",
        "neutral",
        "negative",
        "positive",
        "neutral",
        "positive",
        "negative",
        "neutral",
        "positive",
        "negative",
    ]

    y_pred = [
        "positive",  # Correct
        "negative",  # Correct
        "neutral",  # Correct
        "neutral",  # Wrong (should be positive)
        "negative",  # Correct
        "positive",  # Correct
        "negative",  # Wrong (should be neutral)
        "negative",  # Correct
        "positive",  # Correct
        "neutral",  # Correct
        "positive",  # Correct
        "neutral",  # Wrong (should be negative)
        "neutral",  # Correct
        "positive",  # Correct
        "negative",  # Correct
    ]

    return y_true, y_pred


# ============================================================================
# BASIC METRICS
# ============================================================================


def calculate_basic_metrics(y_true: List[str], y_pred: List[str]) -> Dict[str, float]:
    """
    Calculate basic classification metrics.

    Args:
        y_true: True labels
        y_pred: Predicted labels

    Returns:
        Dictionary of metrics
    """
    accuracy = accuracy_score(y_true, y_pred)

    # Weighted averages (accounts for class imbalance)
    precision = precision_score(y_true, y_pred, average="weighted", zero_division=0)
    recall = recall_score(y_true, y_pred, average="weighted", zero_division=0)
    f1 = f1_score(y_true, y_pred, average="weighted", zero_division=0)

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
    }


def print_basic_metrics(metrics: Dict[str, float]):
    """Print basic metrics in formatted table."""
    print("\n" + "=" * 60)
    print("BASIC CLASSIFICATION METRICS")
    print("=" * 60)

    print(f"{'Metric':<20} {'Score':<15} {'Interpretation'}")
    print("-" * 60)

    interpretations = {
        "accuracy": "Overall correctness",
        "precision": "Positive prediction reliability",
        "recall": "True positive detection rate",
        "f1_score": "Harmonic mean of P&R",
    }

    for metric, score in metrics.items():
        interp = interpretations.get(metric, "")
        print(f"{metric.capitalize():<20} {score:>6.1%}         {interp}")


# ============================================================================
# PER-CLASS METRICS
# ============================================================================


def calculate_per_class_metrics(
    y_true: List[str], y_pred: List[str]
) -> Dict[str, Dict[str, float]]:
    """
    Calculate metrics for each class separately.

    Args:
        y_true: True labels
        y_pred: Predicted labels

    Returns:
        Dictionary mapping class to metrics
    """
    # Get unique classes
    classes = sorted(set(y_true))

    # Calculate per-class metrics
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=classes, zero_division=0
    )

    results = {}
    for i, cls in enumerate(classes):
        results[cls] = {
            "precision": precision[i],
            "recall": recall[i],
            "f1_score": f1[i],
            "support": int(support[i]),
        }

    return results


def print_per_class_metrics(metrics: Dict[str, Dict[str, float]]):
    """Print per-class metrics in formatted table."""
    print("\n" + "=" * 60)
    print("PER-CLASS METRICS")
    print("=" * 60)

    print(f"{'Class':<15} {'Precision':<12} {'Recall':<12} {'F1':<12} {'Support'}")
    print("-" * 60)

    for cls, scores in metrics.items():
        print(
            f"{cls:<15} "
            f"{scores['precision']:>6.1%}      "
            f"{scores['recall']:>6.1%}      "
            f"{scores['f1_score']:>6.1%}      "
            f"{scores['support']:>4}"
        )


# ============================================================================
# CONFUSION MATRIX
# ============================================================================


def calculate_confusion_matrix(y_true: List[str], y_pred: List[str]) -> np.ndarray:
    """
    Calculate confusion matrix.

    Args:
        y_true: True labels
        y_pred: Predicted labels

    Returns:
        Confusion matrix as numpy array
    """
    classes = sorted(set(y_true))
    cm = confusion_matrix(y_true, y_pred, labels=classes)
    return cm, classes


def print_confusion_matrix(cm: np.ndarray, classes: List[str]):
    """Print confusion matrix in formatted table."""
    print("\n" + "=" * 60)
    print("CONFUSION MATRIX")
    print("=" * 60)
    print("Rows: True labels, Columns: Predicted labels\n")

    # Header
    header = "True \\ Pred".ljust(15)
    for cls in classes:
        header += f"{cls:<12}"
    print(header)
    print("-" * 60)

    # Matrix rows
    for i, true_cls in enumerate(classes):
        row = f"{true_cls:<15}"
        for j, pred_cls in enumerate(classes):
            row += f"{cm[i][j]:<12}"
        print(row)

    # Interpretation
    print("\nInterpretation:")
    print("- Diagonal: Correct predictions")
    print("- Off-diagonal: Misclassifications")


# ============================================================================
# CLASSIFICATION REPORT
# ============================================================================


def print_classification_report(y_true: List[str], y_pred: List[str]):
    """Print comprehensive classification report."""
    print("\n" + "=" * 60)
    print("CLASSIFICATION REPORT (scikit-learn)")
    print("=" * 60)
    print(classification_report(y_true, y_pred, zero_division=0))


# ============================================================================
# ERROR ANALYSIS
# ============================================================================


def analyze_errors(
    y_true: List[str], y_pred: List[str], samples: List[str] = None
) -> Dict[str, List[Dict]]:
    """
    Analyze misclassifications.

    Args:
        y_true: True labels
        y_pred: Predicted labels
        samples: Optional list of sample texts

    Returns:
        Dictionary of misclassification patterns
    """
    errors = []

    for i, (true, pred) in enumerate(zip(y_true, y_pred)):
        if true != pred:
            error = {
                "index": i,
                "true_label": true,
                "predicted_label": pred,
            }
            if samples:
                error["sample"] = samples[i]
            errors.append(error)

    # Group by error type
    error_patterns = {}
    for error in errors:
        key = f"{error['true_label']} → {error['predicted_label']}"
        if key not in error_patterns:
            error_patterns[key] = []
        error_patterns[key].append(error)

    return error_patterns


def print_error_analysis(error_patterns: Dict[str, List[Dict]]):
    """Print error analysis report."""
    print("\n" + "=" * 60)
    print("ERROR ANALYSIS")
    print("=" * 60)

    if not error_patterns:
        print("No errors found!")
        return

    total_errors = sum(len(errors) for errors in error_patterns.values())
    print(f"Total Errors: {total_errors}\n")

    # Sort by frequency
    sorted_patterns = sorted(
        error_patterns.items(), key=lambda x: len(x[1]), reverse=True
    )

    print("Most Common Error Patterns:")
    for pattern, errors in sorted_patterns:
        count = len(errors)
        percentage = count / total_errors * 100
        print(f"  {pattern}: {count} errors ({percentage:.1f}%)")

        # Show examples
        if errors[0].get("sample"):
            print(f"    Example: {errors[0]['sample'][:60]}...")


# ============================================================================
# BINARY CLASSIFICATION METRICS
# ============================================================================


def calculate_binary_metrics(
    y_true: List[str], y_pred: List[str], positive_class: str
) -> Dict[str, float]:
    """
    Calculate binary classification metrics for a specific positive class.

    Args:
        y_true: True labels
        y_pred: Predicted labels
        positive_class: Label to treat as positive

    Returns:
        Dictionary of binary metrics
    """
    # Convert to binary (positive class vs rest)
    y_true_binary = [1 if label == positive_class else 0 for label in y_true]
    y_pred_binary = [1 if label == positive_class else 0 for label in y_pred]

    # Calculate metrics
    tn, fp, fn, tp = confusion_matrix(y_true_binary, y_pred_binary).ravel()

    return {
        "true_positives": int(tp),
        "false_positives": int(fp),
        "true_negatives": int(tn),
        "false_negatives": int(fn),
        "precision": tp / (tp + fp) if (tp + fp) > 0 else 0,
        "recall": tp / (tp + fn) if (tp + fn) > 0 else 0,
        "specificity": tn / (tn + fp) if (tn + fp) > 0 else 0,
        "f1_score": f1_score(y_true_binary, y_pred_binary, zero_division=0),
    }


def print_binary_metrics(metrics: Dict[str, float], positive_class: str):
    """Print binary classification metrics."""
    print("\n" + "=" * 60)
    print(f"BINARY METRICS (Positive Class: {positive_class})")
    print("=" * 60)

    print("\nConfusion Matrix Components:")
    print(f"  True Positives:  {metrics['true_positives']}")
    print(f"  False Positives: {metrics['false_positives']}")
    print(f"  True Negatives:  {metrics['true_negatives']}")
    print(f"  False Negatives: {metrics['false_negatives']}")

    print("\nMetrics:")
    print(f"  Precision:   {metrics['precision']:.1%}")
    print(f"  Recall:      {metrics['recall']:.1%}")
    print(f"  Specificity: {metrics['specificity']:.1%}")
    print(f"  F1 Score:    {metrics['f1_score']:.1%}")


# ============================================================================
# EXAMPLES
# ============================================================================


def example_basic_evaluation():
    """Example: Basic classification evaluation."""
    y_true, y_pred = create_sample_predictions()

    metrics = calculate_basic_metrics(y_true, y_pred)
    print_basic_metrics(metrics)


def example_per_class_evaluation():
    """Example: Per-class metrics."""
    y_true, y_pred = create_sample_predictions()

    metrics = calculate_per_class_metrics(y_true, y_pred)
    print_per_class_metrics(metrics)


def example_confusion_matrix():
    """Example: Confusion matrix."""
    y_true, y_pred = create_sample_predictions()

    cm, classes = calculate_confusion_matrix(y_true, y_pred)
    print_confusion_matrix(cm, classes)


def example_error_analysis():
    """Example: Error analysis."""
    y_true, y_pred = create_sample_predictions()

    # Sample texts (for demonstration)
    samples = [
        "I love this product!",
        "Terrible experience.",
        "It's okay.",
        "Good but expensive.",
        "Worst purchase ever.",
        "Amazing quality!",
        "Not impressed.",
        "Disappointing.",
        "Highly recommend!",
        "Average product.",
        "Fantastic!",
        "Could be better.",
        "Neutral opinion.",
        "Best ever!",
        "Very bad.",
    ]

    error_patterns = analyze_errors(y_true, y_pred, samples)
    print_error_analysis(error_patterns)


def example_binary_classification():
    """Example: Binary classification metrics."""
    y_true, y_pred = create_sample_predictions()

    metrics = calculate_binary_metrics(y_true, y_pred, positive_class="positive")
    print_binary_metrics(metrics, "positive")


# ============================================================================
# MAIN
# ============================================================================


if __name__ == "__main__":
    print("=" * 60)
    print("CLASSIFICATION METRICS FOR LLM EVALUATION")
    print("=" * 60)

    # Run all examples
    example_basic_evaluation()
    example_per_class_evaluation()
    example_confusion_matrix()
    print_classification_report(*create_sample_predictions())
    example_error_analysis()
    example_binary_classification()

    print("\n" + "=" * 60)
    print("EVALUATION COMPLETE")
    print("=" * 60)

    print("\nKey Takeaways:")
    print("1. Use accuracy for balanced datasets")
    print("2. Use F1-score for imbalanced datasets")
    print("3. Analyze confusion matrix to identify specific error patterns")
    print("4. Per-class metrics reveal which categories need improvement")
    print("5. Error analysis guides prompt engineering and data collection")

    print("\nNext Steps:")
    print("1. Replace sample data with your actual LLM predictions")
    print("2. Set target thresholds (e.g., F1 > 0.8)")
    print("3. Track metrics over time to detect regressions")
    print("4. Use error analysis to improve prompts and examples")
