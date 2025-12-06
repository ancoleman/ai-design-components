# RAG (Retrieval-Augmented Generation) Evaluation

Comprehensive guide to evaluating RAG systems using the RAGAS framework.

## Table of Contents

1. [RAG System Overview](#rag-system-overview)
2. [RAGAS Framework](#ragas-framework)
3. [Retrieval Quality Metrics](#retrieval-quality-metrics)
4. [Generation Quality Metrics](#generation-quality-metrics)
5. [End-to-End Evaluation](#end-to-end-evaluation)
6. [Troubleshooting Guide](#troubleshooting-guide)

---

## RAG System Overview

### Components

A typical RAG system has three stages:

1. **Retrieval:** Fetch relevant documents/chunks from knowledge base
2. **Context Assembly:** Combine retrieved chunks into context
3. **Generation:** LLM generates answer using context

### Why RAG Needs Specialized Evaluation

**Dual Failure Modes:**
- **Retrieval Failures:** Retrieving irrelevant or missing relevant documents
- **Generation Failures:** Hallucinating despite good context, ignoring context

**Standard metrics (BLEU, accuracy) don't capture:**
- Whether answer is grounded in retrieved context (faithfulness)
- Whether retrieved context is actually relevant to the question
- Trade-offs between retrieval and generation quality

---

## RAGAS Framework

### Overview

**RAGAS** (Retrieval Augmented Generation Assessment) is the industry-standard framework for RAG evaluation.

**Key Innovation:** LLM-powered metrics that don't require manual annotation.

**Installation:**
```bash
pip install ragas
```

**Core Philosophy:**
Separate evaluation of retrieval quality from generation quality.

### Required Data Format

RAGAS expects datasets with these fields:

```python
{
    "question": str,           # User query
    "answer": str,             # LLM-generated answer
    "contexts": List[str],     # Retrieved document chunks
    "ground_truth": str        # (Optional) Reference answer
}
```

**Example:**
```python
from datasets import Dataset

data = {
    "question": ["What is the capital of France?"],
    "answer": ["The capital of France is Paris, located in the north-central part of the country."],
    "contexts": [["Paris is the capital and most populous city of France, situated on the Seine River."]],
    "ground_truth": ["Paris"]
}

dataset = Dataset.from_dict(data)
```

---

## Retrieval Quality Metrics

Evaluate the quality of document retrieval before generation.

### Context Relevance

**Definition:** How relevant are the retrieved chunks to the user's question?

**Calculation:**
1. LLM identifies which sentences in retrieved context are relevant to the question
2. Score = Relevant sentences / Total sentences

**Score Range:** 0-1 (higher is better)

**Target:** > 0.7

**Why It Matters:**
- Irrelevant context wastes tokens and confuses the LLM
- Low context relevance indicates poor retrieval

**Example:**
```python
from ragas.metrics import context_relevancy

# Evaluate
results = evaluate(dataset, metrics=[context_relevancy])
print(f"Context Relevance: {results['context_relevancy']:.2f}")
```

**Improving Low Scores:**
- Improve embedding model quality
- Use hybrid search (keyword + semantic)
- Add query expansion or rewriting
- Adjust chunk size and overlap
- Add re-ranking step after retrieval

---

### Context Precision

**Definition:** Are relevant chunks ranked higher than irrelevant chunks?

**Calculation:**
1. For each retrieved chunk, determine if it's relevant to the question
2. Calculate precision at K (precision considering rank)
3. Penalize relevant chunks appearing late in the list

**Score Range:** 0-1 (higher is better)

**Target:** > 0.5

**Why It Matters:**
- LLMs pay more attention to earlier chunks in context
- Relevant information should appear first

**Improving Low Scores:**
- Add cross-encoder re-ranker after initial retrieval
- Tune retrieval weights (if using hybrid search)
- Experiment with different embedding models
- Consider reciprocal rank fusion for combining search results

---

### Context Recall

**Definition:** Are all relevant chunks from the knowledge base retrieved?

**Calculation:**
1. Identify all ground-truth relevant chunks
2. Calculate: Retrieved relevant chunks / Total relevant chunks

**Score Range:** 0-1 (higher is better)

**Target:** > 0.8

**Note:** Requires ground truth annotations of relevant documents.

**Why It Matters:**
- Missing relevant information leads to incomplete answers
- High recall ensures comprehensive coverage

**Improving Low Scores:**
- Increase number of retrieved chunks (K value)
- Improve chunking strategy (smaller chunks may help)
- Use query expansion to match more variations
- Consider multiple embedding models and merge results

---

## Generation Quality Metrics

Evaluate the quality of LLM-generated answers given retrieved context.

### Faithfulness (Most Critical Metric)

**Definition:** Is the answer grounded in the retrieved context? Does it hallucinate?

**Calculation:**
1. LLM extracts all factual claims from the generated answer
2. For each claim, LLM checks if it's supported by the retrieved context
3. Score = Supported claims / Total claims

**Score Range:** 0-1 (higher is better)

**Target:** > 0.8 (strict requirement for production RAG systems)

**Why It Matters:**
- Hallucinations are the #1 RAG failure mode
- Users trust RAG systems to be factually grounded
- Unfaithful answers can cause serious harm (medical, legal, financial domains)

**Example:**
```python
from ragas.metrics import faithfulness

results = evaluate(dataset, metrics=[faithfulness])
print(f"Faithfulness: {results['faithfulness']:.2f}")

# If faithfulness < 0.8, you have a hallucination problem
```

**Example Evaluation:**

```
Question: "What is the population of Tokyo?"
Context: "Tokyo has approximately 14 million residents within the city proper."
Answer: "Tokyo has 14 million people in the city, and 37 million in the metro area."

Claims:
1. "Tokyo has 14 million people in the city" - SUPPORTED
2. "37 million in the metro area" - NOT SUPPORTED (not in context)

Faithfulness Score: 1/2 = 0.5 (FAILING - hallucination detected)
```

**Improving Low Scores:**
- Add explicit grounding instruction to prompt: "Only use information from the provided context"
- Require citations: "Answer with inline citations [1] to source chunks"
- Use lower temperature (more deterministic)
- Add post-generation fact-checking step
- Consider using models with better instruction following (Claude, GPT-4)

---

### Answer Relevance

**Definition:** How well does the generated answer address the user's question?

**Calculation:**
1. LLM generates multiple questions that the answer would address
2. Calculate semantic similarity between generated questions and original question
3. Higher similarity = more relevant answer

**Score Range:** 0-1 (higher is better)

**Target:** > 0.7

**Why It Matters:**
- Answer can be faithful but still off-topic
- Ensures answer is useful to the user

**Example:**
```python
from ragas.metrics import answer_relevancy

results = evaluate(dataset, metrics=[answer_relevancy])
print(f"Answer Relevance: {results['answer_relevancy']:.2f}")
```

**Example Evaluation:**

```
Question: "How do I reset my password?"
Answer: "Our company was founded in 2010 and has grown significantly since then."

Generated reverse questions from answer:
- "When was your company founded?"
- "How has your company grown?"

Similarity to original question: LOW (0.2)
Answer Relevance Score: 0.2 (FAILING - irrelevant answer)
```

**Improving Low Scores:**
- Add question restatement to prompt: "First, restate the user's question"
- Add relevance check in prompt: "Ensure your answer directly addresses the question"
- Use few-shot examples of good answers
- Add post-generation relevance filter

---

## End-to-End Evaluation

### Running Complete RAGAS Evaluation

**Full Pipeline Example:**

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_relevancy,
    context_precision,
    context_recall
)
from datasets import Dataset

# Prepare evaluation dataset
eval_data = {
    "question": [
        "What is the capital of France?",
        "Who wrote Romeo and Juliet?",
        "What is the speed of light?"
    ],
    "answer": [
        "The capital of France is Paris, located in the north-central region.",
        "William Shakespeare wrote Romeo and Juliet in the 1590s.",
        "The speed of light is approximately 299,792 kilometers per second."
    ],
    "contexts": [
        ["Paris is the capital and largest city of France, located on the Seine River."],
        ["Romeo and Juliet is a tragedy written by William Shakespeare early in his career, around 1594-1596."],
        ["The speed of light in vacuum is exactly 299,792,458 meters per second."]
    ],
    "ground_truth": [
        "Paris",
        "William Shakespeare",
        "299,792 km/s"
    ]
}

dataset = Dataset.from_dict(eval_data)

# Run evaluation with all metrics
results = evaluate(
    dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_relevancy,
        context_precision,
        context_recall
    ]
)

# Print results
print("RAGAS Evaluation Results:")
print(f"  Faithfulness:       {results['faithfulness']:.2f}")
print(f"  Answer Relevance:   {results['answer_relevancy']:.2f}")
print(f"  Context Relevance:  {results['context_relevancy']:.2f}")
print(f"  Context Precision:  {results['context_precision']:.2f}")
print(f"  Context Recall:     {results['context_recall']:.2f}")
```

### Score Interpretation

**Excellent RAG System:**
- Faithfulness: > 0.9
- Answer Relevance: > 0.8
- Context Relevance: > 0.8
- Context Precision: > 0.7
- Context Recall: > 0.9

**Good RAG System:**
- Faithfulness: > 0.8
- Answer Relevance: > 0.7
- Context Relevance: > 0.7
- Context Precision: > 0.5
- Context Recall: > 0.8

**Needs Improvement:**
- Any metric below the "Good" thresholds

---

## Troubleshooting Guide

### Problem: Low Faithfulness (< 0.8)

**Symptoms:**
- LLM adds information not in context
- Answers contain plausible but unsupported claims
- Inconsistent answers for same question

**Root Causes:**
1. **Weak grounding instruction:** Prompt doesn't emphasize using only provided context
2. **Model hallucination tendency:** Some models hallucinate more than others
3. **Temperature too high:** Non-deterministic generation adds creativity

**Solutions:**
```python
# Solution 1: Strengthen grounding instruction
prompt = """
Answer the question using ONLY the information in the provided context.
If the context doesn't contain enough information to answer, say "I don't have enough information to answer this question."

Context: {context}
Question: {question}
Answer:
"""

# Solution 2: Require citations
prompt = """
Answer the question using the provided context.
Include inline citations [1], [2] to indicate which source each claim comes from.
"""

# Solution 3: Lower temperature
response = llm.generate(prompt, temperature=0.1)  # More deterministic

# Solution 4: Add post-generation fact-checking
def fact_check(answer, context):
    check_prompt = f"""
    Check if all claims in this answer are supported by the context.
    Answer: {answer}
    Context: {context}
    Are all claims supported? Yes/No
    """
    return llm.generate(check_prompt)
```

---

### Problem: Low Answer Relevance (< 0.7)

**Symptoms:**
- Answers are accurate but don't address the question
- Answers are too generic or too specific
- Answers include tangential information

**Root Causes:**
1. **Poor question understanding:** LLM misinterprets query intent
2. **Context overwhelms question:** Too much irrelevant context distracts LLM
3. **Missing relevance instruction:** Prompt doesn't emphasize addressing the question

**Solutions:**
```python
# Solution 1: Question restatement
prompt = """
First, restate the user's question to confirm understanding.
Then, answer the question using the provided context.

Question: {question}
Context: {context}

Restatement: [restate question here]
Answer: [answer here]
"""

# Solution 2: Improve retrieval to reduce irrelevant context
# Add re-ranking after retrieval
from sentence_transformers import CrossEncoder

reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
scores = reranker.predict([(question, chunk) for chunk in retrieved_chunks])
top_chunks = [chunk for _, chunk in sorted(zip(scores, retrieved_chunks), reverse=True)[:5]]

# Solution 3: Add relevance instruction
prompt = """
Answer the question directly and concisely.
Focus only on information that helps answer the specific question asked.
Avoid adding background information unless directly relevant.
"""
```

---

### Problem: Low Context Relevance (< 0.7)

**Symptoms:**
- Retrieved documents are off-topic
- Retrieved chunks contain mostly irrelevant information
- Manual review shows better documents exist but weren't retrieved

**Root Causes:**
1. **Poor embedding model:** Embeddings don't capture semantic similarity well
2. **Query-document mismatch:** User queries phrased differently than documents
3. **Chunk size issues:** Chunks too large (diluted relevance) or too small (missing context)

**Solutions:**
```python
# Solution 1: Improve embedding model
# Try domain-specific or better general embeddings
from sentence_transformers import SentenceTransformer

# Upgrade from all-MiniLM-L6-v2 to better model
model = SentenceTransformer('all-mpnet-base-v2')  # Better quality

# Solution 2: Query expansion
def expand_query(query):
    expansion_prompt = f"""
    Generate 3 variations of this query with different phrasings:
    Original: {query}
    Variations:
    """
    variations = llm.generate(expansion_prompt)
    return [query] + variations

# Retrieve using all query variations, merge results

# Solution 3: Hybrid search (keyword + semantic)
from rank_bm25 import BM25Okapi

# Combine BM25 (keyword) and embedding (semantic) search
bm25_scores = bm25.get_scores(query_tokens)
semantic_scores = cosine_similarity(query_embedding, chunk_embeddings)
combined_scores = 0.5 * bm25_scores + 0.5 * semantic_scores

# Solution 4: Optimize chunk size
# Experiment with different chunk sizes (256, 512, 1024 tokens)
# Smaller chunks = more precise, larger chunks = more context
```

---

### Problem: Low Context Precision (< 0.5)

**Symptoms:**
- Relevant documents appear late in results
- First few retrieved chunks are irrelevant
- Manual review shows better ranking is possible

**Root Causes:**
1. **No re-ranking:** Relying solely on first-pass retrieval
2. **Poor ranking from retrieval:** Embedding model doesn't rank well
3. **Query ambiguity:** Multiple possible interpretations ranked differently

**Solutions:**
```python
# Solution 1: Add cross-encoder re-ranker
from sentence_transformers import CrossEncoder

reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-12-v2')

# Initial retrieval (fast)
initial_chunks = vector_db.similarity_search(query, k=20)

# Re-rank top results (slower but more accurate)
pairs = [(query, chunk.page_content) for chunk in initial_chunks]
scores = reranker.predict(pairs)
reranked_chunks = [chunk for _, chunk in sorted(zip(scores, initial_chunks), reverse=True)[:5]]

# Solution 2: Reciprocal Rank Fusion (combine multiple retrievers)
def reciprocal_rank_fusion(rankings_list, k=60):
    scores = {}
    for rankings in rankings_list:
        for rank, doc_id in enumerate(rankings):
            if doc_id not in scores:
                scores[doc_id] = 0
            scores[doc_id] += 1 / (rank + k)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

# Combine semantic search, BM25, and query expansion results
```

---

### Problem: Low Context Recall (< 0.8)

**Symptoms:**
- Missing relevant documents in retrieval
- Answers are incomplete or partial
- Multiple queries needed to get full information

**Root Causes:**
1. **K (retrieval count) too low:** Not retrieving enough chunks
2. **Chunk size too large:** Relevant information split across chunks
3. **Overly specific retrieval:** Missing paraphrased or related content

**Solutions:**
```python
# Solution 1: Increase K (number of retrieved chunks)
chunks = vector_db.similarity_search(query, k=10)  # Increase from 5 to 10

# Solution 2: Smaller chunks with overlap
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,      # Smaller chunks
    chunk_overlap=128    # Overlap to avoid splitting related info
)

# Solution 3: Multi-query retrieval
def multi_query_retrieval(original_query):
    # Generate related queries
    related_queries = generate_related_queries(original_query)

    # Retrieve for all queries
    all_chunks = []
    for query in [original_query] + related_queries:
        chunks = vector_db.similarity_search(query, k=5)
        all_chunks.extend(chunks)

    # Deduplicate and return
    return list(set(all_chunks))
```

---

## Advanced Patterns

### Continuous RAG Monitoring

Set up ongoing evaluation in production:

```python
# Sample 10% of production queries for evaluation
import random

def evaluate_production_rag(sample_rate=0.1):
    if random.random() > sample_rate:
        return  # Skip this query

    # Run RAGAS evaluation on this query
    results = evaluate_single(question, answer, contexts)

    # Log results
    log_metrics({
        "timestamp": datetime.now(),
        "faithfulness": results["faithfulness"],
        "answer_relevance": results["answer_relevance"],
        "context_relevance": results["context_relevance"]
    })

    # Alert if below threshold
    if results["faithfulness"] < 0.8:
        alert_team(f"Low faithfulness detected: {results['faithfulness']}")
```

### A/B Testing RAG Configurations

Compare two RAG setups:

```python
# Configuration A: Simple retrieval
config_a = {
    "retrieval": "semantic_only",
    "k": 5,
    "rerank": False
}

# Configuration B: Hybrid + rerank
config_b = {
    "retrieval": "hybrid_search",
    "k": 10,
    "rerank": True
}

# Run evaluation on same dataset with both configs
results_a = evaluate_rag_config(config_a, eval_dataset)
results_b = evaluate_rag_config(config_b, eval_dataset)

# Compare
print(f"Config A Faithfulness: {results_a['faithfulness']:.2f}")
print(f"Config B Faithfulness: {results_b['faithfulness']:.2f}")
```

---

## Summary

**Priority Order for RAG Evaluation:**
1. **Faithfulness** (> 0.8) - Prevent hallucinations
2. **Context Relevance** (> 0.7) - Ensure good retrieval
3. **Answer Relevance** (> 0.7) - Ensure useful answers
4. **Context Precision** (> 0.5) - Optimize ranking
5. **Context Recall** (> 0.8) - Complete information retrieval

**Remember:** Fix retrieval problems first (context metrics), then generation problems (faithfulness, answer relevance).
