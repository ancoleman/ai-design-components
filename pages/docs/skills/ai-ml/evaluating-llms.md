---
sidebar_position: 3
title: Evaluating LLMs
description: Evaluate LLM systems using automated metrics, LLM-as-judge, and benchmarks
tags: [ai-ml, llm-evaluation, ragas, testing, quality-assurance, hallucination-detection]
---

# Evaluating LLMs

Evaluate Large Language Model (LLM) systems using automated metrics, LLM-as-judge patterns, and standardized benchmarks to ensure production quality and safety.

## When to Use

Use this skill when:

- Testing individual prompts for correctness and formatting
- Validating RAG (Retrieval-Augmented Generation) pipeline quality
- Measuring hallucinations, bias, or toxicity in LLM outputs
- Comparing different models or prompt configurations (A/B testing)
- Running benchmark tests (MMLU, HumanEval) to assess model capabilities
- Setting up production monitoring for LLM applications
- Integrating LLM quality checks into CI/CD pipelines

## Key Features

### 1. Evaluation Strategy Selection

**By Task Type:**

| Task Type | Primary Approach | Metrics | Tools |
|-----------|------------------|---------|-------|
| Classification (sentiment, intent) | Automated metrics | Accuracy, Precision, Recall, F1 | scikit-learn |
| Generation (summaries, creative text) | LLM-as-judge + automated | BLEU, ROUGE, BERTScore, Quality rubric | GPT-4/Claude for judging |
| Question Answering | Exact match + semantic similarity | EM, F1, Cosine similarity | Custom evaluators |
| RAG Systems | RAGAS framework | Faithfulness, Answer/Context relevance | RAGAS library |
| Code Generation | Unit tests + execution | Pass@K, Test pass rate | HumanEval, pytest |
| Multi-step Agents | Task completion + tool accuracy | Success rate, Efficiency | Custom evaluators |

**Layered Approach (Production):**
1. **Layer 1**: Automated metrics for all outputs (fast, cheap)
2. **Layer 2**: LLM-as-judge for 10% sample (nuanced quality)
3. **Layer 3**: Human review for 1% edge cases (validation)

### 2. RAG Evaluation with RAGAS

**Critical Metrics (Priority Order):**

1. **Faithfulness** (Target: > 0.8) - MOST CRITICAL
   - Measures: Is the answer grounded in retrieved context?
   - Prevents hallucinations
   - If failing: Adjust prompt to emphasize grounding, require citations

2. **Answer Relevance** (Target: > 0.7)
   - Measures: How well does the answer address the query?
   - If failing: Improve prompt instructions, add few-shot examples

3. **Context Relevance** (Target: > 0.7)
   - Measures: Are retrieved chunks relevant to the query?
   - If failing: Improve retrieval (better embeddings, hybrid search)

4. **Context Precision** (Target: > 0.5)
   - Measures: Are relevant chunks ranked higher than irrelevant?
   - If failing: Add re-ranking step to retrieval pipeline

5. **Context Recall** (Target: > 0.8)
   - Measures: Are all relevant chunks retrieved?
   - If failing: Increase retrieval count, improve chunking strategy

### 3. LLM-as-Judge Evaluation

**When to Use:**
- Generation quality assessment (summaries, creative writing)
- Nuanced evaluation criteria (tone, clarity, helpfulness)
- Custom rubrics for domain-specific tasks
- Medium-volume evaluation (100-1,000 samples)

**Correlation with Human Judgment:** 0.75-0.85 for well-designed rubrics

**Best Practices:**
- Use clear, specific rubrics (1-5 scale with detailed criteria)
- Include few-shot examples in evaluation prompt
- Average multiple evaluations to reduce variance
- Be aware of biases (position bias, verbosity bias, self-preference)

### 4. Safety and Alignment Evaluation

#### Hallucination Detection

**Methods:**

1. **Faithfulness to Context (RAG):**
   - Use RAGAS faithfulness metric
   - LLM checks if claims are supported by context
   - Score: Supported claims / Total claims

2. **Factual Accuracy (Closed-Book):**
   - LLM-as-judge with access to reliable sources
   - Fact-checking APIs (Google Fact Check)
   - Entity-level verification (dates, names, statistics)

3. **Self-Consistency:**
   - Generate multiple responses to same question
   - Measure agreement between responses
   - Low consistency suggests hallucination

#### Bias Evaluation

**Types of Bias:**
- Gender bias (stereotypical associations)
- Racial/ethnic bias (discriminatory outputs)
- Cultural bias (Western-centric assumptions)
- Age/disability bias (ableist or ageist language)

**Evaluation Methods:**
- **BBQ (Bias Benchmark for QA)**: 58,000 question-answer pairs
- **BOLD (Bias in Open-Ended Language Generation)**: Measure stereotype amplification
- **Counterfactual Evaluation**: Generate responses with demographic swaps

#### Toxicity Detection

**Tools:**
- **Perspective API (Google)**: Toxicity, threat, insult scores
- **Detoxify (HuggingFace)**: Open-source toxicity classifier
- **OpenAI Moderation API**: Hate, harassment, violence detection

### 5. Benchmark Testing

**Standard Benchmarks:**

| Benchmark | Coverage | Format | Difficulty | Use Case |
|-----------|----------|--------|------------|----------|
| **MMLU** | 57 subjects (STEM, humanities) | Multiple choice | High school - professional | General intelligence |
| **HellaSwag** | Sentence completion | Multiple choice | Common sense | Reasoning validation |
| **GPQA** | PhD-level science | Multiple choice | Very high (expert-level) | Frontier model testing |
| **HumanEval** | 164 Python problems | Code generation | Medium | Code capability |
| **MATH** | 12,500 competition problems | Math solving | High school competitions | Math reasoning |

**Domain-Specific Benchmarks:**
- **Medical**: MedQA (USMLE), PubMedQA
- **Legal**: LegalBench
- **Finance**: FinQA, ConvFinQA

## Quick Start

### Unit Evaluation (Python)
```python
import pytest
from openai import OpenAI

client = OpenAI()

def classify_sentiment(text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Classify sentiment as positive, negative, or neutral. Return only the label."},
            {"role": "user", "content": text}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip().lower()

def test_positive_sentiment():
    result = classify_sentiment("I love this product!")
    assert result == "positive"
```

### RAG Evaluation (RAGAS)
```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_relevancy
from datasets import Dataset

data = {
    "question": ["What is the capital of France?"],
    "answer": ["The capital of France is Paris."],
    "contexts": [["Paris is the capital of France."]],
    "ground_truth": ["Paris"]
}

dataset = Dataset.from_dict(data)
results = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_relevancy])
print(f"Faithfulness: {results['faithfulness']:.2f}")
```

### LLM-as-Judge (Python)
```python
from openai import OpenAI

client = OpenAI()

def evaluate_quality(prompt: str, response: str) -> tuple[int, str]:
    """Returns (score 1-5, reasoning)"""
    eval_prompt = f"""
Rate the following LLM response on relevance and helpfulness.

USER PROMPT: {prompt}
LLM RESPONSE: {response}

Provide:
Score: [1-5, where 5 is best]
Reasoning: [1-2 sentences]
"""
    result = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": eval_prompt}],
        temperature=0.3
    )
    content = result.choices[0].message.content
    lines = content.strip().split('\n')
    score = int(lines[0].split(':')[1].strip())
    reasoning = lines[1].split(':', 1)[1].strip()
    return score, reasoning
```

## Python Library Recommendations

| Library | Use Case | Installation |
|---------|----------|--------------|
| **RAGAS** | RAG evaluation | `pip install ragas` |
| **DeepEval** | General LLM evaluation, pytest integration | `pip install deepeval` |
| **LangSmith** | Production monitoring, A/B testing | `pip install langsmith` |
| **lm-eval** | Benchmark testing (MMLU, HumanEval) | `pip install lm-eval` |
| **scikit-learn** | Classification metrics | `pip install scikit-learn` |

## Safety Evaluation Priority Matrix

| Application | Hallucination Risk | Bias Risk | Toxicity Risk | Evaluation Priority |
|-------------|-------------------|-----------|---------------|---------------------|
| Customer Support | High | Medium | High | 1. Faithfulness, 2. Toxicity, 3. Bias |
| Medical Diagnosis | Critical | High | Low | 1. Factual Accuracy, 2. Hallucination, 3. Bias |
| Creative Writing | Low | Medium | Medium | 1. Quality/Fluency, 2. Content Policy |
| Code Generation | Medium | Low | Low | 1. Functional Correctness, 2. Security |
| Content Moderation | Low | Critical | Critical | 1. Bias, 2. False Positives/Negatives |

## Production Evaluation Patterns

### A/B Testing
Compare two LLM configurations:
- **Variant A**: GPT-4 (expensive, high quality)
- **Variant B**: Claude Sonnet (cheaper, fast)

**Metrics:**
- User satisfaction scores (thumbs up/down)
- Task completion rates
- Response time and latency
- Cost per successful interaction

### Online Evaluation
Real-time quality monitoring:
- **Response Quality**: LLM-as-judge scoring every Nth response
- **User Feedback**: Explicit ratings, thumbs up/down
- **Business Metrics**: Conversion rates, support ticket resolution
- **Cost Tracking**: Tokens used, inference costs

### Human-in-the-Loop
Sample-based human evaluation:
- **Random Sampling**: Evaluate 10% of responses
- **Confidence-Based**: Evaluate low-confidence outputs
- **Error-Triggered**: Flag suspicious responses for review

## Related Skills

- **building-ai-chat**: Evaluate AI chat applications (this skill tests what that skill builds)
- **prompt-engineering**: Test prompt quality and effectiveness
- **testing-strategies**: Apply testing pyramid to LLM evaluation
- **implementing-observability**: Production monitoring and alerting for LLM quality
- **building-ci-pipelines**: Integrate LLM evaluation into CI/CD

## Common Pitfalls

1. **Over-reliance on Automated Metrics for Generation**: BLEU/ROUGE correlate weakly with human judgment for creative text
2. **Ignoring Faithfulness in RAG Systems**: Hallucinations are the #1 RAG failure mode
3. **No Production Monitoring**: Models can degrade over time, prompts can break with updates
4. **Biased LLM-as-Judge Evaluation**: Evaluator LLMs have biases (position bias, verbosity bias)
5. **Insufficient Benchmark Coverage**: Single benchmark doesn't capture full model capability
6. **Missing Safety Evaluation**: Production LLMs can generate harmful content

## References

- Full skill documentation: `/skills/evaluating-llms/SKILL.md`
- Evaluation types: `/skills/evaluating-llms/references/evaluation-types.md`
- RAG evaluation: `/skills/evaluating-llms/references/rag-evaluation.md`
- Safety evaluation: `/skills/evaluating-llms/references/safety-evaluation.md`
- Benchmarks: `/skills/evaluating-llms/references/benchmarks.md`
- LLM-as-judge: `/skills/evaluating-llms/references/llm-as-judge.md`
- Production evaluation: `/skills/evaluating-llms/references/production-evaluation.md`
- Metrics reference: `/skills/evaluating-llms/references/metrics-reference.md`
