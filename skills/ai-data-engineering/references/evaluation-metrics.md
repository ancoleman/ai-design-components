# RAGAS: RAG Evaluation Metrics

Complete guide to evaluating RAG pipeline quality with RAGAS framework.

## Table of Contents

- [Overview](#overview)
- [Why Traditional Metrics Fail](#why-traditional-metrics-fail)
- [RAGAS Metrics](#ragas-metrics)
- [Implementation](#implementation)
- [Continuous Evaluation](#continuous-evaluation)
- [Best Practices](#best-practices)

## Overview

RAGAS (Retrieval-Augmented Generation Assessment) is an LLM-as-judge framework for evaluating RAG pipeline quality.

**Traditional Metrics (Don't Work for RAG):**
- BLEU, ROUGE - Measure word overlap, not semantic correctness
- Perplexity - Measures language model quality, not retrieval
- Exact Match - Too strict for generative responses

**RAGAS Metrics (Designed for RAG):**
- **Faithfulness** - Is the answer grounded in retrieved context?
- **Answer Relevancy** - Does the answer address the question?
- **Context Precision** - Are retrieved chunks relevant?
- **Context Recall** - Were all necessary chunks retrieved?

## Why Traditional Metrics Fail

### Example

**Question:** "What is the capital of France?"

**Retrieved Context:** "France is a country in Western Europe. Paris is the capital and largest city."

**Generated Answer:** "The capital of France is Paris, which is also its largest city."

**Ground Truth:** "Paris"

**Traditional Metrics:**
- BLEU: 0.2 (low because answer has extra words)
- ROUGE: 0.3 (low because answer is longer)
- Exact Match: 0.0 (not exact match)

**Problem:** All metrics are low despite perfect answer!

**RAGAS Metrics:**
- Faithfulness: 1.0 (all claims supported by context)
- Answer Relevancy: 1.0 (directly answers question)
- Context Precision: 1.0 (both retrieved sentences relevant)
- Context Recall: 1.0 (all necessary info retrieved)

**Result:** RAGAS correctly identifies this as excellent RAG output.

## RAGAS Metrics

### 1. Faithfulness

**Definition:** Percentage of claims in the answer that can be verified from the retrieved context.

**Formula:**
```
Faithfulness = Number of verified claims / Total number of claims
```

**Good Score:** > 0.8

**Example:**

**Context:** "Paris is the capital of France. France is in Western Europe."

**Answer:** "Paris is the capital of France, which is located in Western Europe."

**Claims:**
1. "Paris is the capital of France" ✓ (verified in context)
2. "France is located in Western Europe" ✓ (verified in context)

**Faithfulness:** 2/2 = 1.0 (perfect)

**Bad Example:**

**Context:** "Paris is the capital of France."

**Answer:** "Paris is the capital of France and has a population of 12 million."

**Claims:**
1. "Paris is the capital of France" ✓ (verified)
2. "Paris has a population of 12 million" ✗ (not in context - hallucination!)

**Faithfulness:** 1/2 = 0.5 (poor - hallucination detected)

### 2. Answer Relevancy

**Definition:** How well does the answer address the user's question?

**Formula:**
```
Answer Relevancy = Cosine similarity between:
  - Question embedding
  - Generated answer embedding
```

**Good Score:** > 0.7

**Example:**

**Question:** "What is the capital of France?"

**Good Answer:** "The capital of France is Paris." (Relevancy: 0.95)
**Bad Answer:** "France is a beautiful country with great food." (Relevancy: 0.3)

**Implementation:**
```python
from ragas.metrics import answer_relevancy

# RAGAS computes this automatically
score = answer_relevancy.score(
    question="What is the capital of France?",
    answer="The capital of France is Paris."
)
```

### 3. Context Precision

**Definition:** Percentage of retrieved chunks that are actually relevant to answering the question.

**Formula:**
```
Context Precision = Relevant chunks / Total retrieved chunks
```

**Good Score:** > 0.6

**Example:**

**Question:** "What is machine learning?"

**Retrieved Chunks:**
1. "Machine learning is a subset of AI..." ✓ (relevant)
2. "Deep learning uses neural networks..." ✓ (relevant)
3. "Python is a programming language..." ✗ (not relevant)
4. "Data preprocessing is important..." ✓ (relevant)
5. "Cloud computing offers scalability..." ✗ (not relevant)

**Context Precision:** 3/5 = 0.6 (acceptable)

**Why This Matters:**
- Low precision = wasted context tokens
- Irrelevant chunks confuse the LLM
- Higher precision = better answers

### 4. Context Recall

**Definition:** Percentage of information needed to answer the question that was actually retrieved.

**Formula:**
```
Context Recall = Statements in ground truth that can be attributed to retrieved context / Total statements in ground truth
```

**Good Score:** > 0.7

**Example:**

**Question:** "What are the benefits of machine learning?"

**Ground Truth:** "Machine learning can automate tasks, improve accuracy, and scale efficiently."

**Retrieved Context:** "Machine learning automates repetitive tasks. It improves prediction accuracy."

**Analysis:**
- "automate tasks" ✓ (in context)
- "improve accuracy" ✓ (in context)
- "scale efficiently" ✗ (missing from context)

**Context Recall:** 2/3 = 0.67 (borderline - missing important info)

**Why This Matters:**
- Low recall = incomplete answers
- User questions not fully addressed
- May need to retrieve more chunks (increase k)

## Implementation

### Installation

```bash
pip install ragas datasets
```

### Basic Evaluation

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)
from datasets import Dataset

# Prepare evaluation dataset
eval_data = {
    "question": [
        "What is the capital of France?",
        "Who wrote Pride and Prejudice?"
    ],
    "answer": [
        "Paris is the capital of France.",
        "Jane Austen wrote Pride and Prejudice."
    ],
    "contexts": [
        ["France's capital city is Paris, located in the north-central part."],
        ["Pride and Prejudice is a novel by Jane Austen, published in 1813."]
    ],
    "ground_truth": [
        "Paris",
        "Jane Austen"
    ]
}

dataset = Dataset.from_dict(eval_data)

# Evaluate
result = evaluate(
    dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall
    ]
)

# Print results
print(f"Faithfulness: {result['faithfulness']:.2f}")
print(f"Answer Relevancy: {result['answer_relevancy']:.2f}")
print(f"Context Precision: {result['context_precision']:.2f}")
print(f"Context Recall: {result['context_recall']:.2f}")
```

### Evaluating Your RAG Pipeline

```python
from langchain_qdrant import QdrantVectorStore
from langchain_openai import ChatOpenAI
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from datasets import Dataset

# Your RAG pipeline
def rag_pipeline(question: str):
    """Your existing RAG implementation."""
    # Retrieve context
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    docs = retriever.get_relevant_documents(question)
    contexts = [doc.page_content for doc in docs]

    # Generate answer
    chain = create_rag_chain()  # Your chain
    answer = chain.invoke(question)

    return {
        "question": question,
        "answer": answer,
        "contexts": contexts
    }

# Test questions with ground truth
test_questions = [
    {
        "question": "What is machine learning?",
        "ground_truth": "Machine learning is a subset of artificial intelligence that enables computers to learn from data without explicit programming."
    },
    {
        "question": "What is deep learning?",
        "ground_truth": "Deep learning is a subset of machine learning that uses neural networks with multiple layers."
    }
]

# Run RAG pipeline on test questions
results = []
for test in test_questions:
    result = rag_pipeline(test["question"])
    result["ground_truth"] = test["ground_truth"]
    results.append(result)

# Prepare for RAGAS
eval_data = {
    "question": [r["question"] for r in results],
    "answer": [r["answer"] for r in results],
    "contexts": [r["contexts"] for r in results],
    "ground_truth": [r["ground_truth"] for r in results]
}

dataset = Dataset.from_dict(eval_data)

# Evaluate
scores = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall]
)

print("RAG Pipeline Evaluation:")
print(f"Faithfulness: {scores['faithfulness']:.2f}")
print(f"Answer Relevancy: {scores['answer_relevancy']:.2f}")
print(f"Context Precision: {scores['context_precision']:.2f}")
print(f"Context Recall: {scores['context_recall']:.2f}")
```

### Custom LLM for Evaluation

RAGAS uses GPT-4 by default for evaluation. You can customize:

```python
from ragas.llms import LangchainLLMWrapper
from langchain_anthropic import ChatAnthropic

# Use Claude for evaluation
claude = ChatAnthropic(model="claude-sonnet-4")
ragas_llm = LangchainLLMWrapper(claude)

# Evaluate with custom LLM
result = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy],
    llm=ragas_llm
)
```

## Continuous Evaluation

### Pattern 1: Automated Testing

Run RAGAS evaluation on every pipeline change:

```python
# tests/test_rag_quality.py
import pytest
from ragas import evaluate
from datasets import Dataset

def test_rag_quality():
    """Test RAG pipeline quality with RAGAS."""

    # Load test dataset
    with open("test_data/qa_pairs.json") as f:
        test_data = json.load(f)

    # Run RAG pipeline
    results = []
    for item in test_data:
        result = rag_pipeline(item["question"])
        result["ground_truth"] = item["ground_truth"]
        results.append(result)

    # Prepare dataset
    eval_data = {
        "question": [r["question"] for r in results],
        "answer": [r["answer"] for r in results],
        "contexts": [r["contexts"] for r in results],
        "ground_truth": [r["ground_truth"] for r in results]
    }

    dataset = Dataset.from_dict(eval_data)

    # Evaluate
    scores = evaluate(dataset, metrics=[faithfulness, answer_relevancy])

    # Assert minimum quality thresholds
    assert scores['faithfulness'] > 0.8, f"Faithfulness too low: {scores['faithfulness']}"
    assert scores['answer_relevancy'] > 0.7, f"Relevancy too low: {scores['answer_relevancy']}"

# Run with pytest
# pytest tests/test_rag_quality.py
```

### Pattern 2: Metrics Tracking

Track metrics over time:

```python
import json
from datetime import datetime
from ragas import evaluate

def track_rag_metrics(pipeline_version: str, test_data: dict):
    """Track RAG metrics over time."""

    # Run evaluation
    dataset = Dataset.from_dict(test_data)
    scores = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall]
    )

    # Save metrics
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "pipeline_version": pipeline_version,
        "scores": {
            "faithfulness": float(scores['faithfulness']),
            "answer_relevancy": float(scores['answer_relevancy']),
            "context_precision": float(scores['context_precision']),
            "context_recall": float(scores['context_recall'])
        }
    }

    # Append to metrics history
    with open("metrics_history.jsonl", "a") as f:
        f.write(json.dumps(metrics) + "\n")

    return metrics

# Usage
track_rag_metrics("v1.2.0-voyage3", test_data)
```

### Pattern 3: A/B Testing

Compare two RAG pipeline versions:

```python
def compare_rag_pipelines(pipeline_a, pipeline_b, test_questions):
    """A/B test two RAG pipelines."""

    results_a = []
    results_b = []

    for question in test_questions:
        # Pipeline A
        result_a = pipeline_a(question["question"])
        result_a["ground_truth"] = question["ground_truth"]
        results_a.append(result_a)

        # Pipeline B
        result_b = pipeline_b(question["question"])
        result_b["ground_truth"] = question["ground_truth"]
        results_b.append(result_b)

    # Prepare datasets
    dataset_a = Dataset.from_dict({
        "question": [r["question"] for r in results_a],
        "answer": [r["answer"] for r in results_a],
        "contexts": [r["contexts"] for r in results_a],
        "ground_truth": [r["ground_truth"] for r in results_a]
    })

    dataset_b = Dataset.from_dict({
        "question": [r["question"] for r in results_b],
        "answer": [r["answer"] for r in results_b],
        "contexts": [r["contexts"] for r in results_b],
        "ground_truth": [r["ground_truth"] for r in results_b]
    })

    # Evaluate both
    scores_a = evaluate(dataset_a, metrics=[faithfulness, answer_relevancy])
    scores_b = evaluate(dataset_b, metrics=[faithfulness, answer_relevancy])

    # Compare
    comparison = {
        "pipeline_a": {
            "faithfulness": scores_a['faithfulness'],
            "answer_relevancy": scores_a['answer_relevancy']
        },
        "pipeline_b": {
            "faithfulness": scores_b['faithfulness'],
            "answer_relevancy": scores_b['answer_relevancy']
        },
        "improvement": {
            "faithfulness": scores_b['faithfulness'] - scores_a['faithfulness'],
            "answer_relevancy": scores_b['answer_relevancy'] - scores_a['answer_relevancy']
        }
    }

    return comparison

# Example: Test chunk size change
pipeline_512 = create_rag_pipeline(chunk_size=512)
pipeline_256 = create_rag_pipeline(chunk_size=256)

results = compare_rag_pipelines(pipeline_512, pipeline_256, test_questions)
print(f"Chunk size 256 improves faithfulness by: {results['improvement']['faithfulness']:.2f}")
```

## Best Practices

### 1. Build a Quality Test Dataset

Create a comprehensive test dataset:

```python
# test_data/qa_pairs.json
[
  {
    "question": "What is machine learning?",
    "ground_truth": "Machine learning is a subset of AI that enables computers to learn from data.",
    "category": "definition",
    "difficulty": "easy"
  },
  {
    "question": "How does gradient descent work in neural networks?",
    "ground_truth": "Gradient descent optimizes neural networks by iteratively adjusting weights in the direction that reduces the loss function.",
    "category": "technical",
    "difficulty": "hard"
  }
]
```

**Test Dataset Guidelines:**
- 50+ question-answer pairs minimum
- Cover all document categories
- Include easy, medium, hard questions
- Mix factual, conceptual, and procedural questions
- Update when documentation changes

### 2. Set Quality Thresholds

Define minimum acceptable scores:

```python
QUALITY_THRESHOLDS = {
    "faithfulness": 0.8,       # No hallucinations
    "answer_relevancy": 0.7,   # Addresses question
    "context_precision": 0.6,  # Minimal irrelevant chunks
    "context_recall": 0.7      # Complete information
}

def validate_rag_quality(scores: dict):
    """Validate RAG quality against thresholds."""
    failures = []

    for metric, threshold in QUALITY_THRESHOLDS.items():
        if scores[metric] < threshold:
            failures.append(
                f"{metric}: {scores[metric]:.2f} < {threshold} (threshold)"
            )

    if failures:
        raise ValueError(f"RAG quality below thresholds:\n" + "\n".join(failures))

    return True
```

### 3. Diagnose Poor Scores

**Low Faithfulness (<0.8):**
- LLM is hallucinating
- Retrieved context is incomplete
- Try: Lower temperature (0.0), improve retrieval, add "only use context" to prompt

**Low Answer Relevancy (<0.7):**
- Answers don't address questions
- Context is irrelevant
- Try: Improve retrieval strategy, use hybrid search, add re-ranking

**Low Context Precision (<0.6):**
- Too many irrelevant chunks
- Retrieval strategy too broad
- Try: Reduce k (retrieve fewer chunks), use MMR, add metadata filtering

**Low Context Recall (<0.7):**
- Missing necessary information
- Not retrieving enough chunks
- Try: Increase k, use multi-query, reduce chunk size (better granularity)

### 4. Run Evaluations Regularly

```python
# Schedule daily evaluation
from dagster import asset, AssetExecutionContext

@asset
def daily_rag_evaluation(context: AssetExecutionContext):
    """Run daily RAG quality evaluation."""

    # Load test dataset
    with open("test_data/qa_pairs.json") as f:
        test_data = json.load(f)

    # Run pipeline
    results = []
    for item in test_data:
        result = rag_pipeline(item["question"])
        result["ground_truth"] = item["ground_truth"]
        results.append(result)

    # Evaluate
    dataset = Dataset.from_dict({
        "question": [r["question"] for r in results],
        "answer": [r["answer"] for r in results],
        "contexts": [r["contexts"] for r in results],
        "ground_truth": [r["ground_truth"] for r in results]
    })

    scores = evaluate(dataset, metrics=[faithfulness, answer_relevancy])

    # Save to monitoring system
    track_rag_metrics("production", {
        "faithfulness": scores['faithfulness'],
        "answer_relevancy": scores['answer_relevancy']
    })

    # Alert if below threshold
    if scores['faithfulness'] < 0.8:
        alert("RAG faithfulness degraded!", scores)

    return scores
```

### 5. Visualize Metrics Over Time

```python
import pandas as pd
import matplotlib.pyplot as plt

def visualize_metrics_history():
    """Plot RAGAS metrics over time."""

    # Load metrics history
    metrics = []
    with open("metrics_history.jsonl") as f:
        for line in f:
            metrics.append(json.loads(line))

    df = pd.DataFrame(metrics)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    df.plot(x='timestamp', y='faithfulness', ax=axes[0, 0], title='Faithfulness')
    df.plot(x='timestamp', y='answer_relevancy', ax=axes[0, 1], title='Answer Relevancy')
    df.plot(x='timestamp', y='context_precision', ax=axes[1, 0], title='Context Precision')
    df.plot(x='timestamp', y='context_recall', ax=axes[1, 1], title='Context Recall')

    plt.tight_layout()
    plt.savefig('ragas_metrics_history.png')
```

## Summary

**RAGAS provides 4 critical metrics:**

1. **Faithfulness** - No hallucinations (> 0.8)
2. **Answer Relevancy** - Addresses question (> 0.7)
3. **Context Precision** - Relevant chunks (> 0.6)
4. **Context Recall** - Complete info (> 0.7)

**Best Practices:**
- Build quality test dataset (50+ QA pairs)
- Run evaluations on every pipeline change
- Track metrics over time
- Set quality thresholds
- Alert on degradation
- A/B test improvements

**Common Fixes:**
- Low faithfulness → Lower temperature, improve prompts
- Low relevancy → Better retrieval, hybrid search
- Low precision → Reduce k, use MMR
- Low recall → Increase k, multi-query
