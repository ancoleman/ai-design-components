# Metrics Reference

Comprehensive guide to evaluation metrics for LLM systems, covering traditional NLP metrics, LLM-specific metrics, and task-specific metrics.

## Table of Contents

- [Traditional NLP Metrics](#traditional-nlp-metrics)
  - [BLEU](#bleu)
  - [ROUGE](#rouge)
  - [METEOR](#meteor)
  - [BERTScore](#bertscore)
- [LLM-Specific Metrics](#llm-specific-metrics)
  - [Coherence](#coherence)
  - [Relevance](#relevance)
  - [Factuality](#factuality)
  - [Fluency](#fluency)
- [RAG Metrics](#rag-metrics)
  - [Context Relevance](#context-relevance)
  - [Answer Faithfulness](#answer-faithfulness)
  - [Context Precision](#context-precision)
  - [Context Recall](#context-recall)
  - [Answer Relevance](#answer-relevance)
- [Task-Specific Metrics](#task-specific-metrics)
  - [Summarization](#summarization)
  - [Question Answering](#question-answering)
  - [Code Generation](#code-generation)
  - [Classification](#classification)
- [When to Use Which Metric](#when-to-use-which-metric)

## Traditional NLP Metrics

### BLEU

**Bilingual Evaluation Understudy** - Measures n-gram overlap between generated text and reference.

**Formula:**
```
BLEU = BP × exp(∑(w_n × log(p_n)))

Where:
- BP = Brevity penalty (penalizes short outputs)
- p_n = Precision of n-grams (1-gram to 4-gram)
- w_n = Weight for each n-gram (typically 0.25 each)
```

**Score Range:** 0-1 (or 0-100 when scaled)

**Interpretation:**
- **0.00-0.10:** Almost no overlap, very poor
- **0.10-0.30:** Some overlap, poor to fair
- **0.30-0.50:** Moderate overlap, acceptable
- **0.50-0.70:** Good overlap, high quality
- **0.70-1.00:** Excellent overlap, near-perfect

**Use Cases:**
- Machine translation (original use case)
- Text generation with reference outputs
- Controlled generation tasks

**Limitations:**
- Doesn't capture semantic similarity (synonyms score poorly)
- Requires exact n-gram matches
- Correlates weakly with human judgment for creative tasks
- Biased toward shorter outputs

**Python Implementation:**
```python
from nltk.translate.bleu_score import sentence_bleu

reference = [["the", "cat", "sat", "on", "the", "mat"]]
candidate = ["the", "cat", "is", "on", "the", "mat"]

score = sentence_bleu(reference, candidate)
# Score: ~0.60 (good overlap despite "sat" vs "is")
```

### ROUGE

**Recall-Oriented Understudy for Gisting Evaluation** - Measures overlap focusing on recall.

**Variants:**
- **ROUGE-N:** N-gram recall (ROUGE-1, ROUGE-2)
- **ROUGE-L:** Longest common subsequence
- **ROUGE-S:** Skip-bigram overlap

**Formula (ROUGE-N):**
```
ROUGE-N = ∑(Count_match(n-gram)) / ∑(Count(n-gram in reference))

Where:
- Count_match = n-grams appearing in both candidate and reference
- Count = total n-grams in reference
```

**Score Range:** 0-1

**Interpretation:**
- **ROUGE-1 > 0.4:** Good unigram overlap (word coverage)
- **ROUGE-2 > 0.2:** Good bigram overlap (phrase preservation)
- **ROUGE-L > 0.3:** Good sentence structure preservation

**Use Cases:**
- Summarization (primary use case)
- Abstractive generation evaluation
- Measuring content coverage

**Limitations:**
- Recall-focused (doesn't penalize verbosity)
- Doesn't measure factual accuracy
- Weak correlation with human judgment for creative tasks

**Python Implementation:**
```python
from rouge import Rouge

rouge = Rouge()

reference = "The cat sat on the mat"
candidate = "The cat is on the mat"

scores = rouge.get_scores(candidate, reference)
# {'rouge-1': {'r': 0.83, 'p': 0.83, 'f': 0.83},
#  'rouge-2': {'r': 0.60, 'p': 0.60, 'f': 0.60},
#  'rouge-l': {'r': 0.83, 'p': 0.83, 'f': 0.83}}
```

### METEOR

**Metric for Evaluation of Translation with Explicit ORdering** - Extends BLEU with stemming, synonyms, and paraphrases.

**Features:**
- Matches stems (running → run)
- Recognizes synonyms (big → large)
- Considers word order
- Recall-oriented (like ROUGE)

**Formula:**
```
METEOR = (1 - Penalty) × F_mean

Where:
- F_mean = Harmonic mean of precision and recall
- Penalty = Fragmentation penalty for word order
```

**Score Range:** 0-1

**Interpretation:**
- **0.00-0.20:** Poor alignment
- **0.20-0.40:** Fair alignment
- **0.40-0.60:** Good alignment
- **0.60-1.00:** Excellent alignment

**Use Cases:**
- Translation evaluation
- Paraphrase detection
- When semantic similarity matters

**Limitations:**
- Computationally expensive
- Requires external resources (WordNet)
- Language-dependent

**Python Implementation:**
```python
from nltk.translate.meteor_score import meteor_score

reference = ["the cat sat on the mat"]
candidate = "the feline rested on the rug"

score = meteor_score(reference, candidate)
# Score: ~0.55 (captures synonyms: cat→feline, sat→rested, mat→rug)
```

### BERTScore

**Contextual Embedding Similarity** - Measures semantic similarity using BERT embeddings.

**How It Works:**
1. Encode reference and candidate with BERT
2. Compute cosine similarity for each token pair
3. Match tokens with maximum similarity
4. Aggregate to precision, recall, F1

**Score Range:** 0-1 (typically 0.7-1.0 for reasonable outputs)

**Interpretation:**
- **0.70-0.80:** Weak semantic similarity
- **0.80-0.90:** Moderate semantic similarity
- **0.90-0.95:** Strong semantic similarity
- **0.95-1.00:** Near-identical semantics

**Use Cases:**
- Paraphrase evaluation
- Semantic similarity measurement
- When exact n-gram matches are not required

**Advantages:**
- Captures semantic equivalence (synonyms, paraphrases)
- Higher correlation with human judgment than BLEU/ROUGE
- Language-agnostic (with multilingual models)

**Limitations:**
- Computationally expensive
- Requires GPU for speed
- Doesn't measure factuality

**Python Implementation:**
```python
from bert_score import score

references = ["The cat sat on the mat"]
candidates = ["A feline rested on the rug"]

P, R, F1 = score(candidates, references, lang="en")
# F1: ~0.92 (high semantic similarity despite different words)
```

## LLM-Specific Metrics

### Coherence

**Definition:** Logical flow and consistency of generated text.

**Measurement Methods:**
1. **LLM-as-judge:** Rate 1-5 for logical progression
2. **Automated:** Sentence embedding similarity between adjacent sentences
3. **Entity tracking:** Consistency of entity references

**Evaluation Prompt (LLM-as-judge):**
```
Rate the coherence of this text on a 1-5 scale:

TEXT: {generated_text}

Coherence Criteria:
5 - Perfectly logical flow, ideas connect smoothly
4 - Mostly coherent, minor transitions could improve
3 - Somewhat coherent, noticeable gaps in logic
2 - Disjointed, ideas don't connect well
1 - Incoherent, random or contradictory

Score: [1-5]
```

### Relevance

**Definition:** How well the output addresses the input query.

**Measurement Methods:**
1. **LLM-as-judge:** Rate query-response alignment
2. **Semantic similarity:** Cosine similarity of query/response embeddings
3. **Keyword overlap:** Presence of query terms in response

**Target Scores:**
- **Semantic similarity > 0.6:** Response is on-topic
- **LLM-as-judge > 3/5:** Acceptable relevance

### Factuality

**Definition:** Accuracy of factual claims in generated text.

**Measurement Methods:**
1. **Fact-checking APIs:** Google Fact Check, ClaimBuster
2. **Knowledge base verification:** Check claims against WikiData, DBpedia
3. **LLM-as-judge with grounding:** Verify claims against provided context
4. **Self-consistency:** Generate multiple responses, check agreement

**Evaluation Approach:**
```python
# Claim extraction + verification
claims = extract_claims(response)  # Parse into atomic claims
for claim in claims:
    verified = check_against_knowledge_base(claim)
    factuality_score = verified_claims / total_claims
```

### Fluency

**Definition:** Grammatical correctness and natural language flow.

**Measurement Methods:**
1. **Perplexity:** Language model probability (lower = more fluent)
2. **Grammar checkers:** LanguageTool, Grammarly API
3. **LLM-as-judge:** Rate naturalness 1-5

**Interpretation:**
- **Perplexity < 20:** Highly fluent
- **Perplexity 20-50:** Acceptable fluency
- **Perplexity > 50:** Disfluent or unnatural

## RAG Metrics

### Context Relevance

**Definition:** Are retrieved chunks relevant to the query?

**Formula (RAGAS):**
```
Context Relevance = Relevant chunks / Total retrieved chunks
```

**Target:** > 0.7

**Measurement:**
- LLM evaluates each chunk: "Is this relevant to the query? Yes/No"
- Aggregate to percentage

**If Failing (<0.7):**
- Improve retrieval (better embeddings, hybrid search)
- Tune retrieval parameters (top-k, similarity threshold)
- Add query rewriting or expansion

### Answer Faithfulness

**Definition:** Is the answer grounded in retrieved context?

**Formula (RAGAS):**
```
Faithfulness = Supported claims / Total claims in answer
```

**Target:** > 0.8 (**MOST CRITICAL RAG METRIC**)

**Measurement:**
1. Extract claims from answer
2. For each claim, check if supported by context
3. Calculate percentage of supported claims

**If Failing (<0.8):**
- Adjust prompt: "Only use information from the context"
- Require citations: "Reference specific context chunks"
- Add post-processing: Filter unsupported claims

### Context Precision

**Definition:** Are relevant chunks ranked higher than irrelevant ones?

**Formula (RAGAS):**
```
Context Precision = ∑(Relevance@k × Precision@k) / Total relevant chunks

Where:
- Relevance@k = 1 if chunk at rank k is relevant, else 0
- Precision@k = Relevant chunks in top-k / k
```

**Target:** > 0.5

**Measurement:**
- Evaluates ranking quality of retrieval system
- Higher precision = better ranking

**If Failing (<0.5):**
- Add re-ranking step (cross-encoder)
- Improve retrieval scoring function
- Use hybrid search (keyword + semantic)

### Context Recall

**Definition:** Are all relevant chunks retrieved?

**Formula (RAGAS):**
```
Context Recall = Retrieved relevant chunks / All relevant chunks in corpus
```

**Target:** > 0.8

**Measurement:**
- Requires ground truth of all relevant chunks
- Typically measured on benchmark datasets

**If Failing (<0.8):**
- Increase retrieval count (top-k)
- Improve chunking strategy (smaller chunks)
- Use query expansion

### Answer Relevance

**Definition:** How well does the answer address the query?

**Formula (RAGAS):**
```
Answer Relevance = Cosine similarity of:
  - Original query
  - Generated queries from answer (reverse engineering)
```

**Target:** > 0.7

**Measurement:**
1. LLM generates queries that the answer would satisfy
2. Compare generated queries to original query
3. High similarity = answer is relevant

**If Failing (<0.7):**
- Improve prompt instructions
- Add few-shot examples of good answers
- Ensure context contains relevant information

## Task-Specific Metrics

### Summarization

**Primary Metrics:**
1. **ROUGE-1, ROUGE-2, ROUGE-L** (content coverage)
2. **Faithfulness** (no hallucinated facts)
3. **Compression Ratio** (original length / summary length)

**Target Scores:**
- ROUGE-1 > 0.4
- ROUGE-2 > 0.2
- Faithfulness > 0.9 (critical for news/legal)

**Evaluation Approach:**
```python
from rouge import Rouge

rouge = Rouge()
scores = rouge.get_scores(summary, reference)

# Also check faithfulness
faithfulness = check_faithfulness(summary, original_document)
```

### Question Answering

**Primary Metrics:**
1. **Exact Match (EM):** Answer exactly matches reference
2. **F1 Score:** Token-level overlap
3. **Semantic Similarity:** Embedding cosine similarity

**Target Scores:**
- EM > 60% (for extractive QA)
- F1 > 70% (more lenient)
- Semantic Similarity > 0.8 (for abstractive QA)

**Evaluation Approach:**
```python
# Exact Match
em = int(normalize(pred_answer) == normalize(gold_answer))

# F1 (token overlap)
pred_tokens = set(pred_answer.split())
gold_tokens = set(gold_answer.split())
precision = len(pred_tokens & gold_tokens) / len(pred_tokens)
recall = len(pred_tokens & gold_tokens) / len(gold_tokens)
f1 = 2 * precision * recall / (precision + recall)
```

### Code Generation

**Primary Metrics:**
1. **Pass@K:** Percentage passing unit tests in top-k attempts
2. **Test Pass Rate:** Percentage of test cases passed
3. **Functional Correctness:** Exact output match for test inputs

**Target Scores:**
- Pass@1 > 40% (HumanEval benchmark)
- Pass@10 > 70%
- Test Pass Rate > 80% (for production)

**Evaluation Approach:**
```python
def evaluate_code(generated_code, test_cases):
    passed = 0
    for test in test_cases:
        try:
            result = execute_code(generated_code, test['input'])
            if result == test['expected_output']:
                passed += 1
        except Exception:
            pass

    return passed / len(test_cases)
```

### Classification

**Primary Metrics:**
1. **Accuracy:** Correct predictions / Total predictions
2. **Precision:** True positives / (True positives + False positives)
3. **Recall:** True positives / (True positives + False negatives)
4. **F1 Score:** Harmonic mean of precision and recall

**Target Scores:**
- Accuracy > 85% (general classification)
- F1 > 0.8 (balanced precision/recall)
- Recall > 0.9 (for safety-critical detection)

**Evaluation Approach:**
```python
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

y_true = ["positive", "negative", "neutral"]
y_pred = ["positive", "negative", "positive"]

accuracy = accuracy_score(y_true, y_pred)
precision, recall, f1, _ = precision_recall_fscore_support(
    y_true, y_pred, average='weighted'
)
```

## When to Use Which Metric

### Decision Matrix

| Task Type | Primary Metrics | Secondary Metrics | Tools |
|-----------|----------------|-------------------|-------|
| **RAG Systems** | Faithfulness (>0.8), Answer Relevance (>0.7) | Context Relevance, Precision | RAGAS |
| **Summarization** | ROUGE-1 (>0.4), ROUGE-2 (>0.2) | Faithfulness, Compression ratio | rouge-score |
| **Question Answering** | F1 (>0.7), Exact Match (>0.6) | Semantic similarity | Custom evaluators |
| **Code Generation** | Pass@1 (>0.4), Test Pass Rate (>0.8) | Execution time, Code quality | pytest, HumanEval |
| **Classification** | Accuracy (>0.85), F1 (>0.8) | Precision, Recall | scikit-learn |
| **Generation Quality** | LLM-as-judge (>3/5) | Coherence, Relevance | GPT-4/Claude |
| **Translation** | BLEU (>0.3), METEOR (>0.4) | BERTScore | nltk, sacrebleu |
| **Paraphrase** | BERTScore (>0.9) | Semantic similarity | bert-score |

### By Evaluation Stage

**Development (Fast Feedback):**
- Automated metrics (BLEU, ROUGE, Exact Match)
- Regex/JSON validation
- Unit test assertions

**Pre-Production (Quality Validation):**
- LLM-as-judge on sample (10-20%)
- RAG metrics (if applicable)
- Benchmark testing

**Production (Continuous Monitoring):**
- User feedback (thumbs up/down)
- Business metrics (task completion)
- Sampled LLM-as-judge (1-5%)
- Automated safety checks (toxicity, hallucination)

### By Budget

**Free ($0):**
- Regex matching
- JSON schema validation
- BLEU, ROUGE, Exact Match
- Classification metrics (sklearn)

**Low Cost ($0.01-0.10 per eval):**
- LLM-as-judge with GPT-3.5/Claude Haiku
- BERTScore (one-time GPU cost)
- Simple RAG metrics

**Medium Cost ($0.10-1.00 per eval):**
- LLM-as-judge with GPT-4/Claude Opus
- Full RAGAS evaluation
- Multi-dimensional rubrics

**High Cost ($1+ per eval):**
- Human evaluation
- Expert review
- Multi-rater agreement studies
