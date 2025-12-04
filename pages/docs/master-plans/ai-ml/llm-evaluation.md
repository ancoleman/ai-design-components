---
sidebar_position: 3
---

# LLM Evaluation

A comprehensive skill for testing, benchmarking, and validating large language model outputs. This skill provides frameworks for measuring LLM performance across quality, safety, and reliability dimensions.

**Status:** 🔵 Master Plan Available

## Key Topics

- **Evaluation Frameworks**
  - Automated metrics (BLEU, ROUGE, perplexity)
  - Model-based evaluation (LLM-as-judge)
  - Human evaluation protocols
  - Benchmark datasets and leaderboards

- **Quality Dimensions**
  - Accuracy and factual correctness
  - Relevance and coherence
  - Fluency and readability
  - Instruction following
  - Reasoning capabilities

- **Safety & Alignment**
  - Harmful content detection
  - Bias and fairness testing
  - Jailbreak resistance
  - Privacy and PII handling
  - Hallucination detection

- **Production Monitoring**
  - Regression testing
  - A/B test design
  - Confidence scoring
  - Error analysis workflows
  - User feedback integration

## Primary Tools & Technologies

- **Evaluation Frameworks:** OpenAI Evals, EleutherAI LM Evaluation Harness, HELM
- **LLM-as-Judge:** GPT-4, Claude, custom evaluation models
- **Benchmarks:** MMLU, HumanEval, TruthfulQA, BBH, GSM8K
- **Testing Tools:** PromptFoo, DeepEval, Ragas (RAG evaluation)
- **Observability:** LangSmith, Helicone, Arize AI, Traceloop
- **Human Annotation:** Label Studio, Prodigy, Scale AI

## Integration Points

- **Prompt Engineering:** Iterative refinement based on evaluation
- **MLOps:** CI/CD integration, regression testing
- **Monitoring:** Production performance tracking
- **Content Moderation:** Safety evaluation pipelines
- **User Research:** Human feedback collection

## Evaluation Methodologies

### Automated Metrics
```
Quantitative measurements:
- BLEU, ROUGE: Text similarity
- Perplexity: Model confidence
- BERTScore: Semantic similarity
- Exact Match: Precision tasks
- F1 Score: Information extraction
```

### LLM-as-Judge
```
Model-based evaluation:
- Pairwise comparison (Model A vs B)
- Single-answer grading (0-10 scale)
- Rubric-based assessment
- Multi-dimensional scoring
- Chain-of-thought explanations
```

### Human Evaluation
```
Expert and crowd-sourced review:
- Side-by-side comparison
- Likert scale ratings
- Task completion success
- Qualitative feedback
- Edge case identification
```

### RAG-Specific Evaluation
```
Retrieval-augmented systems:
- Context relevance
- Answer faithfulness
- Groundedness (citation accuracy)
- Context utilization
- Retrieval precision/recall
```

## Evaluation Dimensions

### Quality Metrics
- **Accuracy:** Factual correctness of information
- **Relevance:** Alignment with user intent
- **Completeness:** Coverage of required information
- **Coherence:** Logical flow and consistency
- **Conciseness:** Appropriate length and clarity

### Safety Metrics
- **Toxicity:** Offensive or harmful content
- **Bias:** Unfair treatment of groups
- **Privacy:** PII leakage or exposure
- **Jailbreaks:** Circumvention attempts
- **Refusals:** Appropriate boundary-setting

### Performance Metrics
- **Latency:** Time to first token, total generation time
- **Throughput:** Requests per second
- **Cost:** Tokens consumed per request
- **Reliability:** Success rate, error frequency
- **Consistency:** Output stability across similar inputs

## Testing Workflows

### Pre-Deployment Testing
```
1. Unit Tests → Individual prompt variations
2. Integration Tests → End-to-end workflows
3. Benchmark Tests → Standard dataset evaluation
4. Safety Tests → Red teaming, adversarial inputs
5. Human Review → Expert validation
6. A/B Test Design → Production experiment setup
```

### Production Monitoring
```
1. Sample Traffic → Representative request subset
2. Automated Scoring → Real-time quality metrics
3. Anomaly Detection → Drift and degradation
4. User Feedback → Thumbs up/down, reports
5. Periodic Audits → Comprehensive reviews
6. Regression Tests → Version comparison
```

## Best Practices

- **Multiple Evaluation Methods:** Combine automated, model-based, and human evaluation
- **Representative Test Sets:** Cover diverse use cases and edge cases
- **Calibration:** Validate automated metrics against human judgment
- **Continuous Monitoring:** Track performance over time
- **Version Control:** Maintain evaluation datasets and results
- **Clear Rubrics:** Define explicit evaluation criteria
- **Blind Testing:** Prevent bias in comparative evaluations
- **Statistical Significance:** Use adequate sample sizes

## Common Pitfalls

- Over-relying on single metrics (e.g., only accuracy)
- Insufficient test set diversity
- Evaluation-training data leakage
- Ignoring latency and cost in evaluation
- Not testing failure modes and edge cases
- Lack of baseline comparisons
- Poor inter-annotator agreement in human eval
- Evaluating on outdated or biased benchmarks

## Success Metrics

- **Test Coverage:** Percentage of use cases with evaluations
- **Evaluation Velocity:** Time from development to validated results
- **Quality Score:** Aggregate performance across dimensions
- **Pass Rate:** Percentage meeting quality thresholds
- **Regression Detection:** Catching performance degradation
- **Cost Efficiency:** Evaluation cost per model improvement
