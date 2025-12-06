# Model Monitoring and Observability

Monitor production ML models for drift, performance degradation, and quality issues.

## Table of Contents

- [Overview](#overview)
- [Data Drift Detection](#data-drift-detection)
- [Model Drift Detection](#model-drift-detection)
- [Performance Monitoring](#performance-monitoring)
- [Feature Importance Tracking](#feature-importance-tracking)
- [Tools and Platforms](#tools-and-platforms)
- [Implementation Examples](#implementation-examples)

## Overview

Production models degrade over time due to changing data distributions, concept drift, and data quality issues. Monitoring detects issues early and triggers interventions.

### Monitoring Categories

| Category | What to Monitor | Detection Method | Action |
|----------|----------------|------------------|--------|
| Data Drift | Input feature distributions | Statistical tests (KS, PSI) | Retrain model |
| Model Drift | Prediction quality | Ground truth comparison | Retrain model |
| Performance | Latency, throughput | APM tools | Scale infrastructure |
| Data Quality | Missing values, outliers | Schema validation | Fix data pipeline |

## Data Drift Detection

Detect when input feature distributions change over time.

### Kolmogorov-Smirnov (KS) Test

Compare distributions using KS statistic.

```python
# ks_test.py
from scipy import stats
import numpy as np

def detect_drift_ks(reference_data, current_data, threshold=0.05):
    """
    Detect drift using KS test.

    Args:
        reference_data: Training data distribution
        current_data: Current production data
        threshold: P-value threshold (default 0.05)

    Returns:
        dict with drift results per feature
    """
    drift_results = {}

    for column in reference_data.columns:
        # KS test
        statistic, p_value = stats.ks_2samp(
            reference_data[column],
            current_data[column]
        )

        drift_detected = p_value < threshold

        drift_results[column] = {
            'statistic': statistic,
            'p_value': p_value,
            'drift_detected': drift_detected
        }

        if drift_detected:
            print(f"⚠️  Drift detected in {column}: p-value={p_value:.4f}")

    return drift_results

# Example
reference = pd.DataFrame({'feature_1': np.random.normal(50, 10, 1000)})
current = pd.DataFrame({'feature_1': np.random.normal(55, 12, 1000)})  # Distribution shifted

results = detect_drift_ks(reference, current)
```

### Population Stability Index (PSI)

Measure distribution shift magnitude.

```python
# psi.py
import numpy as np

def calculate_psi(reference, current, bins=10):
    """
    Calculate Population Stability Index.

    PSI Interpretation:
    - PSI < 0.1: No significant change
    - 0.1 <= PSI < 0.2: Moderate change (investigate)
    - PSI >= 0.2: Significant change (retrain model)

    Returns:
        PSI value
    """

    # Create bins based on reference distribution
    breakpoints = np.percentile(reference, np.linspace(0, 100, bins + 1))

    # Calculate percentage in each bin
    reference_percents = np.histogram(reference, bins=breakpoints)[0] / len(reference)
    current_percents = np.histogram(current, bins=breakpoints)[0] / len(current)

    # Avoid division by zero
    reference_percents = np.where(reference_percents == 0, 0.0001, reference_percents)
    current_percents = np.where(current_percents == 0, 0.0001, current_percents)

    # Calculate PSI
    psi = np.sum((current_percents - reference_percents) * np.log(current_percents / reference_percents))

    return psi

# Example
reference = np.random.normal(50, 10, 10000)
current = np.random.normal(55, 12, 10000)  # Shifted

psi = calculate_psi(reference, current)
print(f"PSI: {psi:.4f}")

if psi >= 0.2:
    print("⚠️  Significant drift detected")
elif psi >= 0.1:
    print("⚠️  Moderate drift detected")
else:
    print("✓ No significant drift")
```

### Chi-Square Test (Categorical Features)

Test for changes in categorical distributions.

```python
# chi_square_test.py
from scipy.stats import chi2_contingency
import pandas as pd

def detect_drift_categorical(reference, current, threshold=0.05):
    """Detect drift in categorical features using chi-square test."""

    # Value counts
    reference_counts = reference.value_counts()
    current_counts = current.value_counts()

    # Align categories
    all_categories = set(reference_counts.index).union(set(current_counts.index))

    reference_aligned = [reference_counts.get(cat, 0) for cat in all_categories]
    current_aligned = [current_counts.get(cat, 0) for cat in all_categories]

    # Chi-square test
    contingency_table = [reference_aligned, current_aligned]
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)

    drift_detected = p_value < threshold

    if drift_detected:
        print(f"⚠️  Drift detected: p-value={p_value:.4f}")

    return {
        'chi2_statistic': chi2,
        'p_value': p_value,
        'drift_detected': drift_detected
    }

# Example
reference = pd.Series(['A'] * 400 + ['B'] * 300 + ['C'] * 300)
current = pd.Series(['A'] * 200 + ['B'] * 400 + ['C'] * 400)  # Distribution shifted

result = detect_drift_categorical(reference, current)
```

## Model Drift Detection

Monitor prediction quality degradation.

### Ground Truth Accuracy Monitoring

Compare predictions to delayed ground truth labels.

```python
# accuracy_monitoring.py
from sklearn.metrics import accuracy_score, f1_score
import pandas as pd

class AccuracyMonitor:
    """Monitor model accuracy with delayed ground truth."""

    def __init__(self, baseline_accuracy: float, threshold: float = 0.05):
        """
        Args:
            baseline_accuracy: Training/validation accuracy
            threshold: Alert if accuracy drops more than this
        """
        self.baseline_accuracy = baseline_accuracy
        self.threshold = threshold
        self.history = []

    def check_accuracy(self, y_true, y_pred, timestamp):
        """Check current accuracy against baseline."""

        current_accuracy = accuracy_score(y_true, y_pred)
        degradation = self.baseline_accuracy - current_accuracy

        self.history.append({
            'timestamp': timestamp,
            'accuracy': current_accuracy,
            'degradation': degradation
        })

        if degradation > self.threshold:
            print(f"⚠️  Accuracy degraded: {self.baseline_accuracy:.3f} → {current_accuracy:.3f} (drop: {degradation:.3f})")
            return {'alert': True, 'degradation': degradation}

        return {'alert': False, 'degradation': degradation}

    def get_trend(self):
        """Get accuracy trend over time."""
        return pd.DataFrame(self.history)

# Example
monitor = AccuracyMonitor(baseline_accuracy=0.92, threshold=0.05)

# Week 1
result = monitor.check_accuracy(y_true_week1, y_pred_week1, timestamp='2023-06-01')

# Week 2
result = monitor.check_accuracy(y_true_week2, y_pred_week2, timestamp='2023-06-08')

# View trend
trend = monitor.get_trend()
print(trend)
```

### Prediction Distribution Monitoring

Monitor changes in prediction distributions (useful when ground truth delayed).

```python
# prediction_distribution_monitoring.py
import numpy as np

class PredictionDistributionMonitor:
    """Monitor prediction distribution for anomalies."""

    def __init__(self, reference_predictions):
        """
        Args:
            reference_predictions: Predictions from validation set
        """
        self.reference_mean = np.mean(reference_predictions)
        self.reference_std = np.std(reference_predictions)

    def check_distribution(self, current_predictions):
        """Check if current predictions deviate from reference."""

        current_mean = np.mean(current_predictions)
        current_std = np.std(current_predictions)

        # Z-score for mean shift
        mean_zscore = abs(current_mean - self.reference_mean) / self.reference_std

        # Check if significant shift (z-score > 3 is ~99.7% confidence)
        if mean_zscore > 3:
            print(f"⚠️  Prediction mean shifted: {self.reference_mean:.3f} → {current_mean:.3f}")
            return {'alert': True, 'mean_shift': mean_zscore}

        # Check if variance changed significantly
        variance_ratio = current_std / self.reference_std

        if variance_ratio > 2 or variance_ratio < 0.5:
            print(f"⚠️  Prediction variance changed: {self.reference_std:.3f} → {current_std:.3f}")
            return {'alert': True, 'variance_ratio': variance_ratio}

        return {'alert': False}

# Example
reference_preds = np.random.beta(2, 5, 10000)  # Reference distribution
current_preds = np.random.beta(3, 5, 1000)    # Shifted distribution

monitor = PredictionDistributionMonitor(reference_preds)
result = monitor.check_distribution(current_preds)
```

## Performance Monitoring

Track latency, throughput, and resource utilization.

### Prometheus Metrics

```python
# prometheus_metrics.py
from prometheus_client import Counter, Histogram, Gauge
import time

# Metrics
model_predictions_total = Counter(
    'model_predictions_total',
    'Total predictions',
    ['model_name', 'version']
)

model_prediction_latency = Histogram(
    'model_prediction_latency_seconds',
    'Prediction latency',
    ['model_name', 'version']
)

model_errors_total = Counter(
    'model_errors_total',
    'Total prediction errors',
    ['model_name', 'version', 'error_type']
)

model_accuracy_gauge = Gauge(
    'model_accuracy',
    'Current model accuracy',
    ['model_name', 'version']
)

class MonitoredModel:
    """Model wrapper with Prometheus monitoring."""

    def __init__(self, model, model_name, version):
        self.model = model
        self.model_name = model_name
        self.version = version

    def predict(self, X):
        """Predict with monitoring."""

        start_time = time.time()

        try:
            # Prediction
            predictions = self.model.predict(X)

            # Track metrics
            latency = time.time() - start_time
            model_prediction_latency.labels(
                model_name=self.model_name,
                version=self.version
            ).observe(latency)

            model_predictions_total.labels(
                model_name=self.model_name,
                version=self.version
            ).inc(len(predictions))

            return predictions

        except Exception as e:
            # Track errors
            model_errors_total.labels(
                model_name=self.model_name,
                version=self.version,
                error_type=type(e).__name__
            ).inc()

            raise

# Usage
monitored_model = MonitoredModel(model, model_name='fraud_detection', version='v2.1')
predictions = monitored_model.predict(X_test)

# Metrics exposed at /metrics endpoint for Prometheus
```

### Grafana Dashboard Configuration

```yaml
# grafana_dashboard.json (simplified)
{
  "dashboard": {
    "title": "ML Model Monitoring",
    "panels": [
      {
        "title": "Predictions per Second",
        "targets": [
          {
            "expr": "rate(model_predictions_total[5m])"
          }
        ]
      },
      {
        "title": "P95 Latency",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, model_prediction_latency_seconds_bucket)"
          }
        ]
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(model_errors_total[5m]) / rate(model_predictions_total[5m])"
          }
        ]
      }
    ]
  }
}
```

## Feature Importance Tracking

Monitor changes in feature importance over time.

```python
# feature_importance_monitoring.py
import numpy as np
from sklearn.inspection import permutation_importance

class FeatureImportanceMonitor:
    """Track feature importance shifts."""

    def __init__(self, model, X_reference, y_reference):
        """Initialize with reference feature importance."""

        # Calculate reference importance
        result = permutation_importance(
            model, X_reference, y_reference,
            n_repeats=10,
            random_state=42
        )

        self.reference_importance = {
            feature: result.importances_mean[i]
            for i, feature in enumerate(X_reference.columns)
        }

    def check_importance_shift(self, model, X_current, y_current):
        """Check for feature importance shifts."""

        # Calculate current importance
        result = permutation_importance(
            model, X_current, y_current,
            n_repeats=10,
            random_state=42
        )

        current_importance = {
            feature: result.importances_mean[i]
            for i, feature in enumerate(X_current.columns)
        }

        # Compare
        shifts = {}
        for feature in self.reference_importance:
            ref_imp = self.reference_importance[feature]
            curr_imp = current_importance.get(feature, 0)

            if ref_imp > 0:
                relative_change = (curr_imp - ref_imp) / ref_imp
                shifts[feature] = {
                    'reference': ref_imp,
                    'current': curr_imp,
                    'relative_change': relative_change
                }

                if abs(relative_change) > 0.5:  # 50% change
                    print(f"⚠️  {feature} importance changed by {relative_change:.1%}")

        return shifts

# Example
monitor = FeatureImportanceMonitor(model, X_train, y_train)

# Check after 1 month
shifts = monitor.check_importance_shift(model, X_current, y_current)
```

## Tools and Platforms

### Evidently AI

Open-source ML monitoring library.

```python
# evidently_monitoring.py
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset
from evidently.metrics import DatasetDriftMetric, DatasetMissingValuesMetric

# Create drift report
report = Report(metrics=[
    DataDriftPreset(),
    DataQualityPreset()
])

# Run report
report.run(reference_data=reference_df, current_data=current_df)

# Save HTML report
report.save_html("drift_report.html")

# Get programmatic results
report_dict = report.as_dict()

# Check if drift detected
dataset_drift = report_dict['metrics'][0]['result']['dataset_drift']

if dataset_drift:
    print("⚠️  Dataset drift detected")

    # Get drifted features
    drifted_features = [
        feature['column_name']
        for feature in report_dict['metrics'][0]['result']['drift_by_columns'].values()
        if feature['drift_detected']
    ]

    print(f"Drifted features: {drifted_features}")
```

### WhyLabs

Cloud-based ML monitoring platform.

```python
# whylabs_monitoring.py
import whylogs as why

# Profile data
results = why.log(pandas=current_df)

# Upload to WhyLabs
results.writer("whylabs").write()

# WhyLabs automatically:
# - Detects data drift
# - Monitors data quality
# - Tracks model performance
# - Sends alerts
```

### Arize AI

End-to-end ML observability platform.

```python
# arize_monitoring.py
from arize.pandas.logger import Client
from arize.utils.types import ModelTypes, Environments

arize_client = Client(api_key="YOUR_API_KEY")

# Log predictions
response = arize_client.log(
    model_id="fraud_detection",
    model_version="v2.1",
    model_type=ModelTypes.BINARY_CLASSIFICATION,
    environment=Environments.PRODUCTION,
    dataframe=predictions_df,
    prediction_label_column_name="prediction",
    actual_label_column_name="actual",
    feature_column_names=feature_columns
)

# Arize monitors:
# - Data drift
# - Model performance
# - Feature importance
# - Prediction distribution
```

## Implementation Examples

### Example: Complete Monitoring Pipeline

```python
# complete_monitoring.py
from datetime import datetime, timedelta
import pandas as pd

class MLMonitoringPipeline:
    """Complete monitoring pipeline."""

    def __init__(self, model_name, baseline_accuracy, reference_data):
        self.model_name = model_name
        self.accuracy_monitor = AccuracyMonitor(baseline_accuracy, threshold=0.05)
        self.reference_data = reference_data

    def monitor(self, current_data, predictions, ground_truth=None):
        """Run all monitoring checks."""

        alerts = []

        # 1. Data drift
        drift_results = detect_drift_ks(self.reference_data, current_data)

        for feature, result in drift_results.items():
            if result['drift_detected']:
                alerts.append({
                    'type': 'DATA_DRIFT',
                    'feature': feature,
                    'p_value': result['p_value']
                })

        # 2. Prediction distribution
        pred_monitor = PredictionDistributionMonitor(self.reference_predictions)
        pred_result = pred_monitor.check_distribution(predictions)

        if pred_result['alert']:
            alerts.append({
                'type': 'PREDICTION_DRIFT',
                'details': pred_result
            })

        # 3. Accuracy (if ground truth available)
        if ground_truth is not None:
            acc_result = self.accuracy_monitor.check_accuracy(
                ground_truth,
                predictions,
                timestamp=datetime.now()
            )

            if acc_result['alert']:
                alerts.append({
                    'type': 'ACCURACY_DEGRADATION',
                    'degradation': acc_result['degradation']
                })

        # 4. Data quality
        missing_percentage = current_data.isnull().sum() / len(current_data)

        for col, pct in missing_percentage.items():
            if pct > 0.1:  # 10% missing
                alerts.append({
                    'type': 'DATA_QUALITY',
                    'feature': col,
                    'missing_percentage': pct
                })

        # Send alerts
        if alerts:
            self.send_alerts(alerts)

        return alerts

    def send_alerts(self, alerts):
        """Send alerts via email/Slack/PagerDuty."""

        print(f"⚠️  {len(alerts)} alerts detected")

        for alert in alerts:
            print(f"  - {alert['type']}: {alert}")

            # Send to alerting system
            # send_slack_alert(alert)
            # send_email_alert(alert)

# Usage
pipeline = MLMonitoringPipeline(
    model_name='fraud_detection',
    baseline_accuracy=0.92,
    reference_data=training_data
)

# Run monitoring (daily)
alerts = pipeline.monitor(
    current_data=today_production_data,
    predictions=today_predictions,
    ground_truth=today_labels  # If available
)

# Trigger retraining if critical alerts
if any(alert['type'] in ['DATA_DRIFT', 'ACCURACY_DEGRADATION'] for alert in alerts):
    trigger_retraining_pipeline()
```

### Example: Scheduled Monitoring Job

```python
# scheduled_monitoring.py
import schedule
import time

def monitoring_job():
    """Daily monitoring job."""

    print(f"Running monitoring at {datetime.now()}")

    # Fetch recent data
    current_data = fetch_last_24h_data()
    predictions = fetch_last_24h_predictions()
    ground_truth = fetch_last_24h_labels()

    # Run monitoring
    pipeline = MLMonitoringPipeline(...)
    alerts = pipeline.monitor(current_data, predictions, ground_truth)

    # Generate report
    generate_daily_report(alerts)

# Schedule daily at 2 AM
schedule.every().day.at("02:00").do(monitoring_job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Example: Real-Time Monitoring with Kafka

```python
# realtime_monitoring.py
from kafka import KafkaConsumer, KafkaProducer
import json

consumer = KafkaConsumer(
    'model-predictions',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

# Real-time monitoring
for message in consumer:
    prediction_data = message.value

    # Check for anomalies
    if is_anomalous(prediction_data):
        # Send alert
        alert = {
            'type': 'ANOMALOUS_PREDICTION',
            'timestamp': datetime.now().isoformat(),
            'data': prediction_data
        }

        producer.send('monitoring-alerts', alert)

        print(f"⚠️  Anomalous prediction: {prediction_data}")
```
