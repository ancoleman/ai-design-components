# Production Evaluation

Evaluation patterns for production LLM systems, covering online evaluation, offline pipelines, continuous monitoring, and human-in-the-loop workflows.

## Table of Contents

- [Overview](#overview)
- [Online Evaluation](#online-evaluation)
  - [A/B Testing](#ab-testing)
  - [Interleaving](#interleaving)
  - [Multi-Armed Bandits](#multi-armed-bandits)
- [Offline Evaluation Pipelines](#offline-evaluation-pipelines)
  - [Dataset Management](#dataset-management)
  - [Regression Testing](#regression-testing)
  - [Benchmark Tracking](#benchmark-tracking)
- [Continuous Evaluation Systems](#continuous-evaluation-systems)
  - [Real-Time Monitoring](#real-time-monitoring)
  - [Alerting and Anomaly Detection](#alerting-and-anomaly-detection)
  - [Drift Detection](#drift-detection)
- [Human-in-the-Loop Evaluation](#human-in-the-loop-evaluation)
  - [Sampling Strategies](#sampling-strategies)
  - [Labeling Workflows](#labeling-workflows)
  - [Feedback Integration](#feedback-integration)
- [Cost-Effective Sampling](#cost-effective-sampling)
- [Production Metrics Dashboard](#production-metrics-dashboard)

## Overview

Production evaluation differs from development evaluation:

**Development Evaluation:**
- One-time measurement on fixed dataset
- Focus on absolute quality
- All data evaluated thoroughly

**Production Evaluation:**
- Continuous monitoring of live traffic
- Focus on relative quality and trends
- Sampled evaluation (cost constraints)
- Real user feedback integration

**Key Principles:**
1. **Sample, don't evaluate everything** - Cost prohibitive at scale
2. **Layer evaluation methods** - Automated → LLM → Human
3. **Monitor trends, not absolutes** - Detect degradation early
4. **Close the feedback loop** - Use learnings to improve system

## Online Evaluation

Evaluation using live production traffic.

### A/B Testing

Compare two variants (A vs B) with real users.

**Setup:**
- **Control (A):** Current production model/prompt
- **Treatment (B):** New model/prompt to test
- **Traffic split:** 50/50 or 90/10 (safer for risky changes)
- **Duration:** 1-2 weeks for statistical significance

**Metrics to Track:**

| Metric Type | Examples | Target |
|-------------|----------|--------|
| **User Satisfaction** | Thumbs up/down, ratings | +5% improvement |
| **Task Completion** | Successful interactions, conversions | +10% improvement |
| **Engagement** | Messages per session, session length | +15% improvement |
| **Quality** | LLM-as-judge score on sample | +0.2 point improvement |
| **Cost** | Tokens used, inference time | -20% reduction |

**Implementation (Python):**
```python
import random
from dataclasses import dataclass

@dataclass
class ABTestConfig:
    variant_a_weight: float = 0.5  # 50% traffic to A
    variant_b_weight: float = 0.5  # 50% traffic to B

def assign_variant(user_id: str, config: ABTestConfig) -> str:
    """Consistent assignment based on user_id hash"""
    hash_val = hash(user_id) % 100 / 100.0
    if hash_val < config.variant_a_weight:
        return "A"
    else:
        return "B"

# Usage
variant = assign_variant(user_id="user123", config=ABTestConfig())
if variant == "A":
    response = model_a.generate(prompt)
else:
    response = model_b.generate(prompt)

# Log for analysis
log_event({
    "user_id": user_id,
    "variant": variant,
    "prompt": prompt,
    "response": response,
    "timestamp": now()
})
```

**Statistical Significance:**
```python
from scipy import stats

# Example: Compare thumbs-up rates
variant_a_thumbs_up = 450  # out of 1000 users
variant_b_thumbs_up = 520  # out of 1000 users

# Chi-square test
observed = [[450, 550], [520, 480]]
chi2, p_value, dof, expected = stats.chi2_contingency(observed)

if p_value < 0.05:
    print(f"Variant B is significantly better (p={p_value:.4f})")
else:
    print(f"No significant difference (p={p_value:.4f})")
```

**When to Use:**
- Testing new models (GPT-4 vs Claude)
- Evaluating prompt changes
- Validating cost optimizations
- Large traffic volumes (>1000 users/week)

### Interleaving

Show both variants to same user and track preferences.

**How It Works:**
1. User submits query
2. Generate responses from both A and B
3. Randomize presentation order
4. User implicitly selects (clicks, copies, rates)
5. Track which variant performed better

**Advantages:**
- Higher statistical power (within-subject design)
- Faster to significance (fewer users needed)
- Controls for user variability

**Implementation:**
```python
def interleaved_evaluation(query: str, user_id: str):
    # Generate both responses
    response_a = model_a.generate(query)
    response_b = model_b.generate(query)

    # Randomize order
    if random.random() < 0.5:
        shown_order = [("A", response_a), ("B", response_b)]
    else:
        shown_order = [("B", response_b), ("A", response_a)]

    # Present to user
    for i, (variant, response) in enumerate(shown_order):
        display_response(response, position=i)

    # Track interaction
    selected_position = get_user_selection()
    winner = shown_order[selected_position][0]

    log_event({
        "user_id": user_id,
        "query": query,
        "winner": winner,
        "loser": "A" if winner == "B" else "B"
    })
```

**When to Use:**
- Search/recommendation systems
- Pairwise model comparison
- When implicit feedback is available (clicks, dwell time)

### Multi-Armed Bandits

Dynamically allocate traffic to best-performing variant.

**How It Works:**
- Start with equal traffic split
- Continuously measure performance
- Shift traffic toward better variant
- Balance exploration (testing) vs exploitation (using best)

**Advantages:**
- Minimize regret (time spent on worse variant)
- Automatic winner selection
- No need to wait for statistical significance

**Implementation (Epsilon-Greedy):**
```python
from collections import defaultdict
import random

class EpsilonGreedyBandit:
    def __init__(self, epsilon=0.1):
        self.epsilon = epsilon
        self.rewards = defaultdict(list)

    def select_variant(self, variants):
        # Exploration: random variant
        if random.random() < self.epsilon:
            return random.choice(variants)

        # Exploitation: best variant
        avg_rewards = {
            v: sum(self.rewards[v]) / len(self.rewards[v])
            if self.rewards[v] else 0.0
            for v in variants
        }
        return max(avg_rewards, key=avg_rewards.get)

    def update(self, variant: str, reward: float):
        self.rewards[variant].append(reward)

# Usage
bandit = EpsilonGreedyBandit(epsilon=0.1)
variants = ["gpt-4", "claude-opus", "llama-3-70b"]

for _ in range(1000):  # 1000 requests
    variant = bandit.select_variant(variants)
    response = generate_response(variant, query)
    reward = get_user_feedback(response)  # 0-1 score
    bandit.update(variant, reward)
```

**When to Use:**
- Continuous optimization (no fixed experiment duration)
- Multiple variants (>2)
- When opportunity cost of worse variant is high

## Offline Evaluation Pipelines

Evaluation on static datasets before production deployment.

### Dataset Management

**Evaluation Dataset Structure:**
```json
{
  "dataset_id": "customer_support_qa_v1",
  "created_at": "2025-01-15",
  "samples": [
    {
      "id": "sample_001",
      "query": "How do I reset my password?",
      "context": ["Password reset instructions: Click 'Forgot Password'..."],
      "expected_answer": "Click 'Forgot Password' on the login page.",
      "tags": ["account_management", "authentication"]
    }
  ]
}
```

**Best Practices:**
- **Version control:** Track dataset changes over time
- **Stratified sampling:** Ensure diverse query types
- **Regular updates:** Add new edge cases monthly
- **Size:** 100-500 samples (balance coverage vs cost)

### Regression Testing

Prevent quality degradation when making changes.

**Workflow:**
1. **Baseline:** Evaluate current system on dataset
2. **Change:** Modify prompt/model/parameters
3. **Re-evaluate:** Run same dataset on new system
4. **Compare:** Alert if metrics drop >5%

**Implementation:**
```python
import json
from typing import Dict

def run_regression_test(
    dataset_path: str,
    baseline_results_path: str,
    current_system,
    threshold: float = 0.05
):
    # Load dataset and baseline
    with open(dataset_path) as f:
        dataset = json.load(f)
    with open(baseline_results_path) as f:
        baseline = json.load(f)

    # Evaluate current system
    current_results = evaluate_system(current_system, dataset)

    # Compare metrics
    for metric_name, baseline_score in baseline['metrics'].items():
        current_score = current_results['metrics'][metric_name]
        change = (current_score - baseline_score) / baseline_score

        if change < -threshold:
            print(f"⚠️  REGRESSION DETECTED in {metric_name}")
            print(f"   Baseline: {baseline_score:.3f}")
            print(f"   Current:  {current_score:.3f}")
            print(f"   Change:   {change:.1%}")
            return False

    print("✅ No regressions detected")
    return True
```

**CI/CD Integration:**
```yaml
# .github/workflows/llm-evaluation.yml
name: LLM Regression Tests

on: [pull_request]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run evaluation
        run: python scripts/run_regression_test.py
      - name: Check for regressions
        run: |
          if [ $? -ne 0 ]; then
            echo "Regression detected! Blocking merge."
            exit 1
          fi
```

### Benchmark Tracking

Track performance on standardized benchmarks over time.

**Benchmarks to Track:**
- **General:** MMLU, HellaSwag, GPQA
- **Domain-specific:** MedQA (medical), LegalBench (legal)
- **Task-specific:** HumanEval (code), MATH (reasoning)

**Tracking Dashboard:**
```
Date       | Model         | MMLU | HumanEval | Latency | Cost
-----------|---------------|------|-----------|---------|------
2025-01-01 | gpt-4-turbo   | 0.86 | 0.67      | 1.2s    | $0.03
2025-02-01 | claude-opus   | 0.88 | 0.70      | 0.9s    | $0.05
2025-03-01 | llama-3-70b   | 0.82 | 0.58      | 0.5s    | $0.01
```

## Continuous Evaluation Systems

### Real-Time Monitoring

Monitor LLM quality metrics in production.

**Metrics to Track:**

| Metric Category | Specific Metrics | Frequency |
|----------------|------------------|-----------|
| **Quality** | LLM-as-judge score (sampled 5%) | Every hour |
| **User Feedback** | Thumbs up/down ratio | Real-time |
| **Safety** | Toxicity detection (all outputs) | Real-time |
| **Performance** | Latency (p50, p95, p99) | Real-time |
| **Cost** | Tokens per request, daily spend | Every 15 min |

**Implementation (LangSmith):**
```python
from langsmith import Client

client = Client()

# Log every LLM interaction
run = client.create_run(
    name="customer_support_query",
    inputs={"query": user_query},
    run_type="llm",
    extra={"user_id": user_id}
)

# Generate response
response = llm.generate(user_query)

# Log output
client.update_run(
    run.id,
    outputs={"response": response},
    end_time=datetime.now()
)

# Add user feedback (when available)
if user_feedback:
    client.create_feedback(
        run.id,
        key="user_rating",
        score=user_feedback.rating  # 1-5
    )
```

### Alerting and Anomaly Detection

Detect quality issues early.

**Alert Conditions:**
```python
# Example alert rules
ALERT_RULES = {
    "low_quality": {
        "metric": "llm_as_judge_score",
        "condition": "< 3.0",
        "window": "1 hour",
        "threshold": "10% of samples"
    },
    "high_latency": {
        "metric": "response_time_p95",
        "condition": "> 3.0s",
        "window": "5 minutes"
    },
    "safety_violation": {
        "metric": "toxicity_detected",
        "condition": "> 0",
        "threshold": "1 occurrence"
    }
}
```

**Anomaly Detection:**
```python
from scipy import stats
import numpy as np

def detect_anomaly(current_metric: float, historical_data: list) -> bool:
    """Z-score based anomaly detection"""
    mean = np.mean(historical_data)
    std = np.std(historical_data)
    z_score = abs((current_metric - mean) / std)

    # Alert if >3 standard deviations
    return z_score > 3.0

# Example usage
historical_scores = [4.2, 4.3, 4.1, 4.4, 4.2, 4.3]
current_score = 2.5

if detect_anomaly(current_score, historical_scores):
    send_alert("Quality score anomaly detected!")
```

### Drift Detection

Detect when input or output distributions change.

**Types of Drift:**
1. **Input Drift:** User queries changing (new topics, languages)
2. **Output Drift:** Response characteristics changing (length, style)
3. **Concept Drift:** Relationship between input/output changing

**Detection Methods:**
```python
from scipy.spatial.distance import jensenshannon
import numpy as np

def detect_distribution_drift(
    baseline_samples: list,
    current_samples: list,
    threshold: float = 0.1
) -> bool:
    """Detect drift using Jensen-Shannon divergence"""

    # Compute distributions (e.g., response length)
    baseline_dist = np.histogram(
        [len(s) for s in baseline_samples],
        bins=20,
        density=True
    )[0]
    current_dist = np.histogram(
        [len(s) for s in current_samples],
        bins=20,
        density=True
    )[0]

    # Compute divergence
    divergence = jensenshannon(baseline_dist, current_dist)

    return divergence > threshold
```

## Human-in-the-Loop Evaluation

### Sampling Strategies

**1. Random Sampling**
- Evaluate random 1-10% of outputs
- Unbiased quality estimate
- Good for ongoing monitoring

**2. Confidence-Based Sampling**
- Flag low-confidence outputs for review
- Focus human effort on uncertain cases
- Requires confidence scores from model

**3. Error-Triggered Sampling**
- Review when automated checks fail
- Flag suspicious patterns (very short/long responses)
- Catch edge cases

**4. Stratified Sampling**
- Sample across different user segments
- Ensure coverage of all query types
- Prevent bias toward high-volume queries

**Implementation:**
```python
import random

def sample_for_human_review(
    interactions: list,
    strategy: str = "random",
    sample_rate: float = 0.1
) -> list:
    """Select interactions for human review"""

    if strategy == "random":
        return random.sample(
            interactions,
            k=int(len(interactions) * sample_rate)
        )

    elif strategy == "confidence":
        # Sort by confidence, take lowest
        sorted_interactions = sorted(
            interactions,
            key=lambda x: x.get('confidence', 1.0)
        )
        return sorted_interactions[:int(len(interactions) * sample_rate)]

    elif strategy == "error_triggered":
        # Only review flagged interactions
        return [i for i in interactions if i.get('flagged', False)]

    elif strategy == "stratified":
        # Sample equally from each category
        by_category = defaultdict(list)
        for i in interactions:
            by_category[i['category']].append(i)

        samples = []
        for category, items in by_category.items():
            n = int(len(items) * sample_rate)
            samples.extend(random.sample(items, min(n, len(items))))
        return samples
```

### Labeling Workflows

**Labeling Interface (Gradio Example):**
```python
import gradio as gr

def create_labeling_interface():
    def label_interaction(query, response):
        # Save label
        save_label({
            "query": query,
            "response": response,
            "quality": quality_score,
            "issues": issues
        })
        return "Labeled successfully!"

    interface = gr.Interface(
        fn=label_interaction,
        inputs=[
            gr.Textbox(label="User Query"),
            gr.Textbox(label="LLM Response"),
            gr.Slider(1, 5, label="Quality Score"),
            gr.CheckboxGroup(
                ["Hallucination", "Irrelevant", "Unsafe", "Poor Formatting"],
                label="Issues"
            )
        ],
        outputs=gr.Textbox(label="Status")
    )
    return interface
```

### Feedback Integration

**Closing the Loop:**
1. **Collect human labels** on sampled data
2. **Identify patterns** in failures
3. **Update system** (prompt, retrieval, model)
4. **Re-evaluate** on labeled data
5. **Deploy improvements**

**Example Workflow:**
```python
def analyze_human_feedback(labels: list) -> dict:
    """Find patterns in human-labeled failures"""

    failures = [l for l in labels if l['quality'] < 3]

    # Group by issue type
    issue_counts = defaultdict(int)
    for failure in failures:
        for issue in failure.get('issues', []):
            issue_counts[issue] += 1

    # Identify top issues
    top_issues = sorted(
        issue_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return {
        "total_failures": len(failures),
        "failure_rate": len(failures) / len(labels),
        "top_issues": top_issues[:3]
    }
```

## Cost-Effective Sampling

Balance evaluation quality vs. cost.

**Layered Evaluation (Recommended):**
```
Layer 1: Automated checks (100% of outputs) - FREE
  ↓ Pass automated checks

Layer 2: LLM-as-judge (10% sample) - $0.01-0.10 each
  ↓ Pass LLM evaluation

Layer 3: Human review (1% sample) - $1-10 each
  ↓ Final validation
```

**Cost Calculation:**
```python
def calculate_evaluation_cost(
    daily_outputs: int,
    llm_sample_rate: float = 0.1,
    human_sample_rate: float = 0.01,
    llm_cost_per_eval: float = 0.05,
    human_cost_per_eval: float = 5.0
) -> dict:
    """Estimate monthly evaluation costs"""

    monthly_outputs = daily_outputs * 30

    llm_evals = monthly_outputs * llm_sample_rate
    human_evals = monthly_outputs * human_sample_rate

    llm_cost = llm_evals * llm_cost_per_eval
    human_cost = human_evals * human_cost_per_eval

    return {
        "monthly_outputs": monthly_outputs,
        "llm_evaluations": int(llm_evals),
        "human_evaluations": int(human_evals),
        "llm_cost": f"${llm_cost:.2f}",
        "human_cost": f"${human_cost:.2f}",
        "total_cost": f"${llm_cost + human_cost:.2f}"
    }

# Example: 10,000 outputs/day
costs = calculate_evaluation_cost(daily_outputs=10000)
# Result: ~$1,500/month LLM + $1,500/month human = $3,000 total
```

## Production Metrics Dashboard

**Recommended Dashboard Sections:**

**1. Quality Metrics**
- Average LLM-as-judge score (trend over time)
- User satisfaction rate (thumbs up %)
- Safety violations per 1000 outputs

**2. Performance Metrics**
- Latency (p50, p95, p99)
- Throughput (requests per second)
- Error rate

**3. Cost Metrics**
- Daily inference cost
- Cost per successful interaction
- Token usage trends

**4. Usage Metrics**
- Daily active users
- Queries per user
- Peak traffic times

**Example Monitoring Setup (Prometheus + Grafana):**
```python
from prometheus_client import Counter, Histogram, Gauge

# Define metrics
llm_quality_score = Gauge(
    'llm_quality_score',
    'LLM-as-judge quality score'
)

user_feedback = Counter(
    'user_feedback_total',
    'User feedback counts',
    ['feedback_type']  # thumbs_up, thumbs_down
)

response_latency = Histogram(
    'llm_response_latency_seconds',
    'Response generation time'
)

# Update metrics
llm_quality_score.set(4.2)
user_feedback.labels(feedback_type='thumbs_up').inc()
response_latency.observe(1.5)  # 1.5 seconds
```
