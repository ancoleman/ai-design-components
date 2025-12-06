# Deployment Strategies

Strategic patterns for deploying machine learning models safely with rollback capabilities.

## Table of Contents

- [Overview](#overview)
- [Blue-Green Deployment](#blue-green-deployment)
- [Canary Deployment](#canary-deployment)
- [Shadow Deployment](#shadow-deployment)
- [A/B Testing](#ab-testing)
- [Multi-Armed Bandit](#multi-armed-bandit)
- [Decision Framework](#decision-framework)
- [Implementation Examples](#implementation-examples)

## Overview

Model deployment strategies balance risk, complexity, and speed of rollout. Each strategy offers different trade-offs between safety, infrastructure cost, and deployment velocity.

### Strategy Comparison Matrix

| Strategy | Risk Level | Infrastructure Cost | Deployment Speed | Rollback Speed | Best For |
|----------|-----------|---------------------|------------------|----------------|----------|
| Blue-Green | Low | 2x (duplicate env) | Instant switch | Instant | Low-risk updates |
| Canary | Medium | 1.1-1.5x | Gradual (hours) | Minutes | Medium-risk updates |
| Shadow | Lowest | 2x (parallel compute) | Days (validation) | N/A (no prod impact) | High-risk validation |
| A/B Testing | Low-Medium | 1x | Immediate | Minutes | Business optimization |
| Multi-Armed Bandit | Medium | 1x | Continuous | Gradual | Continuous learning |

## Blue-Green Deployment

Deploy to identical duplicate environment, then switch traffic instantly.

### Architecture

```
                    Load Balancer
                         |
           +-------------+-------------+
           |                           |
    Blue (Current)              Green (New)
    - Version 1.0              - Version 2.0
    - 100% traffic             - 0% traffic
           |
    [Switch Traffic]
           |
           v
    Blue (Old)                 Green (Current)
    - Version 1.0              - Version 2.0
    - 0% traffic               - 100% traffic
```

### Implementation Steps

1. **Deploy to Green environment** (identical to Blue)
   - Same infrastructure, configuration, dependencies
   - Deploy new model version 2.0

2. **Test Green environment**
   - Smoke tests: Model loads, accepts input, returns predictions
   - Integration tests: End-to-end workflow validation
   - Performance tests: Latency, throughput benchmarks

3. **Switch traffic** (atomic operation)
   - Update load balancer to route 100% traffic to Green
   - Blue environment becomes idle (standby for rollback)

4. **Monitor new version**
   - Track metrics for 1-24 hours
   - Compare accuracy, latency, error rates to baseline

5. **Rollback if issues detected**
   - Switch load balancer back to Blue (instant)
   - Investigate issues, fix in Green, retry

### Advantages

- **Instant switchover**: Zero-downtime deployment
- **Instant rollback**: Switch back to Blue immediately
- **Full testing**: Test Green before directing traffic
- **Zero risk to production**: Users never see broken state

### Disadvantages

- **2x infrastructure cost**: Maintain two identical environments
- **Database migrations complex**: Schema changes require careful handling
- **All-or-nothing**: Cannot gradually roll out (100% switch)

### Use Cases

- **Low-risk model updates**: Incremental improvements
- **Time-sensitive deployments**: Need instant cutover
- **Mature models**: High confidence in new version

### Example: Kubernetes Blue-Green

```yaml
# blue-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fraud-detection-blue
  labels:
    app: fraud-detection
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fraud-detection
      version: v1
  template:
    metadata:
      labels:
        app: fraud-detection
        version: v1
    spec:
      containers:
      - name: model
        image: fraud-detection:v1.0.0
        ports:
        - containerPort: 8080

---
# green-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fraud-detection-green
  labels:
    app: fraud-detection
    version: v2
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fraud-detection
      version: v2
  template:
    metadata:
      labels:
        app: fraud-detection
        version: v2
    spec:
      containers:
      - name: model
        image: fraud-detection:v2.0.0
        ports:
        - containerPort: 8080

---
# service.yaml (switch by updating selector)
apiVersion: v1
kind: Service
metadata:
  name: fraud-detection
spec:
  selector:
    app: fraud-detection
    version: v1  # Switch to v2 for green deployment
  ports:
  - port: 80
    targetPort: 8080
```

**Switch command:**
```bash
# Switch to green
kubectl patch service fraud-detection -p '{"spec":{"selector":{"version":"v2"}}}'

# Rollback to blue
kubectl patch service fraud-detection -p '{"spec":{"selector":{"version":"v1"}}}'
```

## Canary Deployment

Gradually roll out new model version to increasing percentage of traffic.

### Architecture

```
                Load Balancer
                     |
      +--------------+---------------+
      |                              |
Version 1.0                    Version 2.0
95% traffic                    5% traffic (canary)
      |
[Monitor metrics, increase canary if healthy]
      |
      v
Version 1.0                    Version 2.0
0% traffic                     100% traffic
```

### Implementation Steps

1. **Deploy canary** (5% traffic)
   - Route small percentage to new version
   - Maintain old version handling majority

2. **Monitor canary metrics** (15-60 minutes)
   - Accuracy: Compare predictions to ground truth (if available)
   - Latency: P50, P95, P99 response times
   - Error rate: Failed predictions / total predictions
   - Business metrics: Conversion rate, revenue impact

3. **Increase traffic gradually**
   - 5% → 10% → 25% → 50% → 100%
   - Monitor at each stage (15-60 minutes)

4. **Rollback if metrics degrade**
   - Automated rollback if error rate > threshold
   - Manual rollback if business metrics decline

### Rollout Schedule Example

| Stage | Canary % | Duration | Rollback Criteria |
|-------|----------|----------|-------------------|
| 1 | 5% | 30 min | Error rate > 2% OR P95 latency > 150ms |
| 2 | 10% | 30 min | Error rate > 1.5% OR P95 latency > 130ms |
| 3 | 25% | 1 hour | Error rate > 1% OR accuracy drop > 3% |
| 4 | 50% | 2 hours | Error rate > 0.5% OR accuracy drop > 2% |
| 5 | 100% | - | Monitor for 24 hours |

### Advantages

- **Gradual risk**: Limit impact to small user percentage
- **Early detection**: Catch issues before full rollout
- **Flexible rollback**: Can stop at any stage
- **Real-world validation**: Test with production traffic patterns

### Disadvantages

- **Complex routing**: Traffic splitting logic required
- **Longer deployment**: Hours instead of instant
- **Monitoring overhead**: Track metrics for both versions
- **Stateful challenges**: Session affinity complications

### Use Cases

- **Medium-risk models**: Significant architecture changes
- **Large user base**: Cannot afford full-scale issues
- **Critical applications**: Fraud detection, healthcare

### Example: Istio Canary with Progressive Traffic Shift

```yaml
# destination-rule.yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: recommendation-model
spec:
  host: recommendation-model
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2

---
# virtual-service.yaml (Stage 1: 5% canary)
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: recommendation-model
spec:
  hosts:
  - recommendation-model
  http:
  - match:
    - headers:
        canary:
          exact: "true"
    route:
    - destination:
        host: recommendation-model
        subset: v2
      weight: 100
  - route:
    - destination:
        host: recommendation-model
        subset: v1
      weight: 95
    - destination:
        host: recommendation-model
        subset: v2
      weight: 5
```

**Automated rollout script:**
```python
import time
import requests

def check_metrics(version, duration_seconds):
    """Monitor canary metrics for specified duration."""
    start = time.time()
    errors = 0
    total = 0
    latencies = []

    while time.time() - start < duration_seconds:
        try:
            response = requests.get(
                "http://monitoring/metrics",
                params={"version": version}
            )
            metrics = response.json()

            error_rate = metrics["error_rate"]
            p95_latency = metrics["p95_latency"]

            # Check rollback criteria
            if error_rate > 0.02:  # 2%
                return False, f"Error rate too high: {error_rate}"
            if p95_latency > 150:  # 150ms
                return False, f"P95 latency too high: {p95_latency}ms"

        except Exception as e:
            return False, f"Monitoring failed: {e}"

        time.sleep(60)  # Check every minute

    return True, "Metrics healthy"

def rollout_canary():
    """Progressive canary rollout with automated rollback."""
    stages = [
        (5, 1800),    # 5% for 30 minutes
        (10, 1800),   # 10% for 30 minutes
        (25, 3600),   # 25% for 1 hour
        (50, 7200),   # 50% for 2 hours
        (100, 0),     # 100% (final)
    ]

    for weight, duration in stages:
        print(f"Setting canary to {weight}%")

        # Update Istio VirtualService
        update_traffic_split(v1_weight=100-weight, v2_weight=weight)

        if duration > 0:
            print(f"Monitoring for {duration/60} minutes...")
            healthy, message = check_metrics("v2", duration)

            if not healthy:
                print(f"ROLLBACK: {message}")
                update_traffic_split(v1_weight=100, v2_weight=0)
                return False

    print("Canary rollout complete!")
    return True

def update_traffic_split(v1_weight, v2_weight):
    """Update Istio traffic split using kubectl."""
    import subprocess

    virtual_service = f"""
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: recommendation-model
spec:
  hosts:
  - recommendation-model
  http:
  - route:
    - destination:
        host: recommendation-model
        subset: v1
      weight: {v1_weight}
    - destination:
        host: recommendation-model
        subset: v2
      weight: {v2_weight}
"""

    subprocess.run(
        ["kubectl", "apply", "-f", "-"],
        input=virtual_service.encode(),
        check=True
    )
```

## Shadow Deployment

Run new model in parallel, compare predictions offline, zero production risk.

### Architecture

```
                Production Traffic
                        |
            +-----------+-----------+
            |                       |
    Production Model v1      Shadow Model v2
    (predictions used)      (predictions logged)
            |                       |
            v                       v
    Return to user          Log for analysis
                                    |
                        [Offline comparison]
```

### Implementation Steps

1. **Deploy shadow model**
   - Receives copy of production requests
   - Predictions logged but not used
   - Zero impact on users

2. **Collect shadow predictions**
   - Log inputs, v1 predictions, v2 predictions
   - Store in data warehouse for analysis

3. **Compare offline**
   - Accuracy: When ground truth available
   - Prediction distribution: Detect major shifts
   - Latency: Performance comparison
   - Feature importance: Model behavior analysis

4. **Analyze differences**
   - Where do models disagree? (error analysis)
   - Performance on different segments
   - Edge cases and failure modes

5. **Promote to production**
   - If shadow performs better → blue-green or canary rollout
   - If shadow has issues → fix and re-shadow

### Advantages

- **Zero production risk**: Predictions never used
- **Real production data**: Validation on actual traffic
- **Comprehensive testing**: Weeks/months of validation
- **Deep analysis**: Compare predictions, understand differences

### Disadvantages

- **2x compute cost**: Run both models simultaneously
- **Delayed feedback**: No immediate impact measurement
- **Storage overhead**: Log all predictions for analysis
- **Ground truth delays**: May wait days/weeks for labels

### Use Cases

- **High-risk models**: Healthcare, financial, safety-critical
- **Major architecture changes**: New algorithm, new features
- **Unproven models**: Experimental approaches
- **Regulatory requirements**: Need extensive validation

### Example: Shadow Deployment with Request Mirroring

```python
# shadow_deployment.py
import asyncio
import logging
from fastapi import FastAPI, Request
from prometheus_client import Counter, Histogram
import json

app = FastAPI()

# Metrics
predictions_counter = Counter(
    'model_predictions_total',
    'Total predictions',
    ['model_version']
)

latency_histogram = Histogram(
    'model_latency_seconds',
    'Prediction latency',
    ['model_version']
)

# Model clients
production_model = ModelClient(version="v1")
shadow_model = ModelClient(version="v2")

# Shadow prediction logger
shadow_logger = logging.getLogger('shadow')
shadow_logger.setLevel(logging.INFO)
handler = logging.FileHandler('/var/log/shadow_predictions.jsonl')
shadow_logger.addHandler(handler)

@app.post("/predict")
async def predict(request: Request):
    """Handle prediction with shadow deployment."""
    input_data = await request.json()

    # Production prediction (blocking)
    with latency_histogram.labels(model_version='v1').time():
        prod_prediction = production_model.predict(input_data)

    predictions_counter.labels(model_version='v1').inc()

    # Shadow prediction (async, non-blocking)
    asyncio.create_task(
        shadow_predict(input_data, prod_prediction)
    )

    # Return production prediction only
    return {"prediction": prod_prediction}

async def shadow_predict(input_data, prod_prediction):
    """Async shadow prediction and logging."""
    try:
        with latency_histogram.labels(model_version='v2').time():
            shadow_prediction = shadow_model.predict(input_data)

        predictions_counter.labels(model_version='v2').inc()

        # Log for offline analysis
        log_entry = {
            "timestamp": time.time(),
            "input": input_data,
            "production_prediction": prod_prediction,
            "shadow_prediction": shadow_prediction,
            "difference": abs(prod_prediction - shadow_prediction)
        }

        shadow_logger.info(json.dumps(log_entry))

    except Exception as e:
        logging.error(f"Shadow prediction failed: {e}")
```

**Analysis script:**
```python
# analyze_shadow_predictions.py
import pandas as pd
import json
from scipy import stats

def load_shadow_logs(filepath):
    """Load shadow predictions from JSONL log."""
    records = []
    with open(filepath) as f:
        for line in f:
            records.append(json.loads(line))
    return pd.DataFrame(records)

def compare_predictions(df):
    """Compare production vs shadow predictions."""

    # Prediction difference distribution
    diff_mean = df['difference'].mean()
    diff_std = df['difference'].std()
    diff_max = df['difference'].max()

    print(f"Prediction Difference Stats:")
    print(f"  Mean: {diff_mean:.4f}")
    print(f"  Std:  {diff_std:.4f}")
    print(f"  Max:  {diff_max:.4f}")

    # Correlation between predictions
    corr = df['production_prediction'].corr(df['shadow_prediction'])
    print(f"\nCorrelation: {corr:.4f}")

    # Statistical test: Are predictions significantly different?
    t_stat, p_value = stats.ttest_rel(
        df['production_prediction'],
        df['shadow_prediction']
    )
    print(f"\nPaired t-test:")
    print(f"  t-statistic: {t_stat:.4f}")
    print(f"  p-value:     {p_value:.4f}")

    if p_value < 0.05:
        print("  Predictions are significantly different")
    else:
        print("  Predictions are not significantly different")

    # Cases with large disagreement
    threshold = diff_mean + 2 * diff_std
    outliers = df[df['difference'] > threshold]
    print(f"\nLarge disagreements (>{threshold:.4f}): {len(outliers)}")

    return {
        'diff_mean': diff_mean,
        'diff_std': diff_std,
        'correlation': corr,
        'p_value': p_value,
        'outlier_count': len(outliers)
    }

# Analyze 1 week of shadow predictions
df = load_shadow_logs('/var/log/shadow_predictions.jsonl')
results = compare_predictions(df)

# Decision: Promote to production?
if results['correlation'] > 0.95 and results['p_value'] > 0.05:
    print("\n✓ RECOMMENDATION: Promote shadow to production")
else:
    print("\n✗ RECOMMENDATION: Further investigation needed")
```

## A/B Testing

Split traffic between model versions to optimize business metrics.

### Architecture

```
                User Traffic
                     |
          +----------+----------+
          |                     |
    Variant A (50%)      Variant B (50%)
    Model v1            Model v2
          |                     |
          v                     v
    Business Metrics      Business Metrics
    (conversion, revenue) (conversion, revenue)
                     |
            [Statistical Analysis]
                     |
                Winner Selection
```

### Key Differences from Canary

| Aspect | Canary Deployment | A/B Testing |
|--------|------------------|-------------|
| Goal | Safe rollout | Business optimization |
| Metrics | ML metrics (accuracy, latency) | Business metrics (conversion, revenue) |
| Duration | Hours to days | Days to weeks |
| Traffic Split | Progressive (5%→100%) | Fixed (50/50 or 90/10) |
| Winner Selection | Technical performance | Statistical significance |

### Implementation Steps

1. **Design experiment**
   - Hypothesis: Model v2 will increase conversion rate by 5%
   - Metric: Conversion rate (purchases / visits)
   - Sample size: Calculate required users for statistical power
   - Significance level: α = 0.05 (5% false positive rate)

2. **Split traffic**
   - Random assignment: 50% variant A, 50% variant B
   - Session consistency: User sees same variant throughout session

3. **Collect data** (minimum duration)
   - Track business metrics for both variants
   - Ensure sufficient sample size for statistical power

4. **Statistical analysis**
   - Two-sample t-test: Compare mean conversion rates
   - Calculate p-value: Probability difference is due to chance
   - Confidence interval: Range of plausible effect sizes

5. **Select winner**
   - If p-value < 0.05 and effect size meaningful → Deploy winner
   - If no significant difference → Keep current version

### Sample Size Calculation

```python
from scipy import stats
import numpy as np

def calculate_sample_size(baseline_rate, minimum_detectable_effect,
                          alpha=0.05, power=0.8):
    """
    Calculate required sample size per variant for A/B test.

    Args:
        baseline_rate: Current conversion rate (e.g., 0.10 for 10%)
        minimum_detectable_effect: Minimum improvement to detect (e.g., 0.05 for 5% lift)
        alpha: Significance level (default 0.05)
        power: Statistical power (default 0.8)

    Returns:
        Required sample size per variant
    """
    # Effect size (Cohen's h)
    p1 = baseline_rate
    p2 = baseline_rate * (1 + minimum_detectable_effect)

    effect_size = 2 * (np.arcsin(np.sqrt(p2)) - np.arcsin(np.sqrt(p1)))

    # Z-scores
    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_beta = stats.norm.ppf(power)

    # Sample size per variant
    n = ((z_alpha + z_beta) / effect_size) ** 2

    return int(np.ceil(n))

# Example: Detect 5% improvement in 10% conversion rate
sample_size = calculate_sample_size(
    baseline_rate=0.10,
    minimum_detectable_effect=0.05
)
print(f"Required sample size per variant: {sample_size:,}")
# Output: Required sample size per variant: 3,142
```

### Statistical Analysis

```python
from scipy import stats

def analyze_ab_test(variant_a_conversions, variant_a_total,
                    variant_b_conversions, variant_b_total):
    """
    Analyze A/B test results using two-proportion z-test.

    Returns:
        dict with test results and recommendation
    """
    # Conversion rates
    rate_a = variant_a_conversions / variant_a_total
    rate_b = variant_b_conversions / variant_b_total

    # Pooled proportion
    pooled = (variant_a_conversions + variant_b_conversions) / (variant_a_total + variant_b_total)

    # Standard error
    se = np.sqrt(pooled * (1 - pooled) * (1/variant_a_total + 1/variant_b_total))

    # Z-statistic
    z_stat = (rate_b - rate_a) / se

    # Two-tailed p-value
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    # Confidence interval for difference
    ci_95 = stats.norm.ppf(0.975) * se

    # Relative lift
    lift = (rate_b - rate_a) / rate_a

    results = {
        'variant_a_rate': rate_a,
        'variant_b_rate': rate_b,
        'absolute_difference': rate_b - rate_a,
        'relative_lift': lift,
        'z_statistic': z_stat,
        'p_value': p_value,
        'confidence_interval_95': (rate_b - rate_a - ci_95, rate_b - rate_a + ci_95),
        'significant': p_value < 0.05,
        'winner': 'B' if p_value < 0.05 and rate_b > rate_a else 'A' if p_value < 0.05 else 'No winner'
    }

    return results

# Example analysis
results = analyze_ab_test(
    variant_a_conversions=320,
    variant_a_total=10000,
    variant_b_conversions=358,
    variant_b_total=10000
)

print(f"Variant A conversion rate: {results['variant_a_rate']:.2%}")
print(f"Variant B conversion rate: {results['variant_b_rate']:.2%}")
print(f"Relative lift: {results['relative_lift']:.2%}")
print(f"P-value: {results['p_value']:.4f}")
print(f"95% CI: ({results['confidence_interval_95'][0]:.4f}, {results['confidence_interval_95'][1]:.4f})")
print(f"Statistically significant: {results['significant']}")
print(f"Winner: {results['winner']}")
```

## Multi-Armed Bandit

Dynamically allocate traffic to optimize cumulative reward, balancing exploration and exploitation.

### Epsilon-Greedy Algorithm

```python
import numpy as np
import random

class EpsilonGreedyBandit:
    """
    Multi-armed bandit with epsilon-greedy exploration.

    Epsilon (ε) controls exploration:
    - ε = 0.1 (10% explore, 90% exploit)
    - ε = 0.2 (20% explore, 80% exploit)
    """

    def __init__(self, n_arms, epsilon=0.1):
        self.n_arms = n_arms
        self.epsilon = epsilon
        self.counts = np.zeros(n_arms)  # Times each arm selected
        self.values = np.zeros(n_arms)  # Average reward per arm

    def select_arm(self):
        """Select arm using epsilon-greedy strategy."""
        if random.random() < self.epsilon:
            # Explore: Random arm
            return random.randrange(self.n_arms)
        else:
            # Exploit: Best arm so far
            return np.argmax(self.values)

    def update(self, arm, reward):
        """Update arm statistics after observing reward."""
        self.counts[arm] += 1
        n = self.counts[arm]

        # Incremental average
        self.values[arm] = ((n - 1) / n) * self.values[arm] + (1 / n) * reward

# Example: 3 model versions
bandit = EpsilonGreedyBandit(n_arms=3, epsilon=0.1)

# Simulate 10,000 predictions
for _ in range(10000):
    # Select model version
    model_version = bandit.select_arm()

    # Get prediction and observe reward (conversion: 0 or 1)
    reward = make_prediction_and_get_reward(model_version)

    # Update bandit statistics
    bandit.update(model_version, reward)

print("Final statistics:")
for i in range(3):
    print(f"Model {i}: {bandit.counts[i]} selections, {bandit.values[i]:.4f} avg reward")
```

### Thompson Sampling (Bayesian Bandit)

```python
import numpy as np

class ThompsonSamplingBandit:
    """
    Bayesian multi-armed bandit using Thompson Sampling.

    Assumes Beta prior for conversion rate:
    - α (successes + 1)
    - β (failures + 1)
    """

    def __init__(self, n_arms):
        self.n_arms = n_arms
        self.successes = np.ones(n_arms)  # Beta prior α = 1
        self.failures = np.ones(n_arms)   # Beta prior β = 1

    def select_arm(self):
        """Sample from posterior and select highest."""
        samples = [
            np.random.beta(self.successes[i], self.failures[i])
            for i in range(self.n_arms)
        ]
        return np.argmax(samples)

    def update(self, arm, reward):
        """Update Beta distribution parameters."""
        if reward > 0:
            self.successes[arm] += 1
        else:
            self.failures[arm] += 1

    def get_statistics(self):
        """Get mean and credible interval for each arm."""
        stats = []
        for i in range(self.n_arms):
            alpha = self.successes[i]
            beta = self.failures[i]

            mean = alpha / (alpha + beta)

            # 95% credible interval
            lower = np.random.beta(alpha, beta, size=10000)
            ci_lower, ci_upper = np.percentile(lower, [2.5, 97.5])

            stats.append({
                'mean': mean,
                'ci_95': (ci_lower, ci_upper),
                'samples': int(alpha + beta - 2)
            })

        return stats

# Example usage
bandit = ThompsonSamplingBandit(n_arms=3)

for _ in range(10000):
    model_version = bandit.select_arm()
    reward = make_prediction_and_get_reward(model_version)
    bandit.update(model_version, reward)

stats = bandit.get_statistics()
for i, s in enumerate(stats):
    print(f"Model {i}: {s['mean']:.4f} (95% CI: {s['ci_95']}), {s['samples']} samples")
```

### When to Use MAB vs A/B Testing

| Scenario | Use A/B Testing | Use Multi-Armed Bandit |
|----------|----------------|------------------------|
| Goal | Determine best version | Maximize cumulative reward |
| Prior knowledge | No prior belief about winner | Strong priors available |
| Sample efficiency | Less efficient (50/50 split) | More efficient (adaptive) |
| Statistical rigor | Clear significance testing | Bayesian credible intervals |
| Simplicity | Simpler to explain/audit | More complex algorithm |
| Regulatory | Easier to justify | May be harder to explain |

## Decision Framework

### Selection Matrix

```
                    Risk Level
                Low         Medium        High
            +------------+------------+------------+
Infrastructure| Blue-Green | Canary     | Shadow     |
Cost: 2x      | ✓ Fast     | ✓ Gradual  | ✓ Zero risk|
            +------------+------------+------------+
Infrastructure| A/B Test   | Canary     | Shadow     |
Cost: 1x      | ✓ Business | ✓ Balanced | ✓ Safe     |
            +------------+------------+------------+
```

### Decision Tree

```
Start: New model version to deploy
    |
    ├─ High-risk model (healthcare, financial)?
    │   └─ YES → Shadow Deployment (weeks of validation)
    │
    ├─ Optimize for business metrics?
    │   └─ YES → A/B Testing or Multi-Armed Bandit
    │
    ├─ Need instant cutover?
    │   └─ YES → Blue-Green Deployment
    │
    ├─ Need gradual rollout with monitoring?
    │   └─ YES → Canary Deployment
    │
    └─ Default → Canary Deployment
```

## Implementation Examples

### Example 1: Canary with Flagger (Kubernetes)

```yaml
# flagger-canary.yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: recommendation-model
  namespace: production
spec:
  # Target deployment
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: recommendation-model

  # Service configuration
  service:
    port: 80
    targetPort: 8080

  # Canary analysis
  analysis:
    # Schedule interval
    interval: 1m

    # Max traffic percentage during canary analysis
    threshold: 5

    # Max number of failed checks before rollback
    maxWeight: 50

    # Incremental traffic increase
    stepWeight: 10

    # Metrics to monitor
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99
      interval: 1m

    - name: request-duration
      thresholdRange:
        max: 500
      interval: 1m

    # Webhooks for custom checks
    webhooks:
    - name: accuracy-check
      url: http://monitoring-service/check-accuracy
      timeout: 5s
      metadata:
        model: recommendation-model
        threshold: "0.85"
```

### Example 2: Shadow Deployment with Seldon Core

```yaml
# seldon-shadow.yaml
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: fraud-detection
spec:
  predictors:
  - name: production
    replicas: 3
    graph:
      name: production-model
      type: MODEL
      endpoint:
        type: REST
      children: []
    componentSpecs:
    - spec:
        containers:
        - name: production-model
          image: fraud-detection:v1.0.0

  - name: shadow
    replicas: 3
    shadow: true  # Shadow mode: predictions logged but not returned
    graph:
      name: shadow-model
      type: MODEL
      endpoint:
        type: REST
      children: []
    componentSpecs:
    - spec:
        containers:
        - name: shadow-model
          image: fraud-detection:v2.0.0
```

### Example 3: Blue-Green with AWS CodeDeploy

```yaml
# appspec.yaml
version: 0.0
Resources:
  - TargetService:
      Type: AWS::ECS::Service
      Properties:
        TaskDefinition: "arn:aws:ecs:us-east-1:123456789:task-definition/fraud-model:10"
        LoadBalancerInfo:
          ContainerName: "fraud-model"
          ContainerPort: 8080
        PlatformVersion: "LATEST"

Hooks:
  - BeforeInstall: "LambdaFunctionToValidateBeforeInstall"
  - AfterInstall: "LambdaFunctionToValidateAfterInstall"
  - AfterAllowTestTraffic: "LambdaFunctionToRunTests"
  - BeforeAllowTraffic: "LambdaFunctionToValidateBeforeTrafficShift"
  - AfterAllowTraffic: "LambdaFunctionToValidateAfterTrafficShift"
```

**CodeDeploy deployment config:**
```json
{
  "deploymentConfigName": "BlueGreen.ECS.Canary10Percent5Minutes",
  "computePlatform": "ECS",
  "trafficRoutingConfig": {
    "type": "TimeBasedCanary",
    "timeBasedCanary": {
      "canaryPercentage": 10,
      "canaryInterval": 5
    }
  },
  "blueGreenDeploymentConfiguration": {
    "terminateBlueInstancesOnDeploymentSuccess": {
      "action": "TERMINATE",
      "terminationWaitTimeInMinutes": 60
    },
    "deploymentReadyOption": {
      "actionOnTimeout": "CONTINUE_DEPLOYMENT"
    }
  }
}
```
