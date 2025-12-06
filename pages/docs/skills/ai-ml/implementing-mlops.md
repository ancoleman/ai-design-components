---
sidebar_position: 1
title: Implementing MLOps
description: Strategic guidance for operationalizing machine learning models from experimentation to production
tags: [ai-ml, mlops, machine-learning, model-serving, model-monitoring, ml-pipelines]
---

# Implementing MLOps

Operationalize machine learning models from experimentation to production deployment and monitoring.

## When to Use

Use this skill when:

- Designing MLOps infrastructure for production ML systems
- Selecting experiment tracking platforms (MLflow, Weights & Biases, Neptune)
- Implementing feature stores for online/offline feature serving
- Choosing model serving solutions (Seldon Core, KServe, BentoML, TorchServe)
- Building ML pipelines for training, evaluation, and deployment
- Setting up model monitoring and drift detection
- Establishing model governance and compliance frameworks
- Optimizing ML inference costs and performance
- Migrating from notebooks to production ML systems
- Implementing continuous training and automated retraining

## Key Features

### 1. Experiment Tracking and Model Registry

**Platform Options:**
- **MLflow**: Open-source standard, framework-agnostic, self-hosted or cloud-agnostic
- **Weights & Biases**: Advanced visualization, team collaboration, integrated hyperparameter optimization
- **Neptune.ai**: Enterprise features (RBAC, audit logs, compliance)

**Model Registry Components:**
- Model artifacts with version control and stage management
- Training metrics, hyperparameters, and dataset versions
- Model cards for documentation and limitations
- Feature schema (input/output signatures)

**Selection Criteria:**
- Open-source requirement → MLflow
- Team collaboration critical → Weights & Biases
- Enterprise compliance (RBAC, audits) → Neptune.ai

### 2. Feature Stores

**Problem Addressed:** Training/serving skew from inconsistent feature engineering

**Feature Store Solution:**
- **Online Store**: Low-latency retrieval for real-time inference (Redis, DynamoDB)
- **Offline Store**: Historical data for training and backtesting (Parquet, BigQuery)
- **Point-in-Time Correctness**: No future data leakage during training

**Platform Comparison:**
- **Feast**: Open-source, cloud-agnostic, most popular
- **Tecton**: Managed service, production-grade, Feast-compatible API
- **SageMaker Feature Store**: AWS ecosystem integration
- **Databricks Feature Store**: Unity Catalog integration

### 3. Model Serving Patterns

**Serving Options:**
- **REST API**: HTTP endpoint for synchronous predictions (&lt;100ms latency)
- **gRPC**: High-performance RPC for low-latency inference (&lt;10ms)
- **Batch Inference**: Process large datasets offline (minutes to hours)
- **Streaming Inference**: Real-time predictions on streaming data (milliseconds)

**Platform Selection:**
- **Seldon Core**: Kubernetes-native, advanced deployment strategies (canary, A/B testing)
- **KServe**: CNCF standard, serverless scaling with Knative
- **BentoML**: Python-first, simplest to get started
- **TorchServe**: PyTorch-specific, production-grade
- **TensorFlow Serving**: TensorFlow-specific, optimized

### 4. Deployment Strategies

**Blue-Green Deployment:** Two environments, instant traffic switch, instant rollback

**Canary Deployment:** Gradual rollout (5% → 10% → 25% → 50% → 100%)

**Shadow Deployment:** New model receives traffic but predictions not used (zero production risk)

**A/B Testing:** Split traffic between versions, measure business metrics

**Multi-Armed Bandit:** Epsilon-greedy exploration for continuous optimization

### 5. ML Pipeline Orchestration

**Pipeline Stages:**
1. Data Validation (Great Expectations)
2. Feature Engineering
3. Data Splitting (train/validation/test)
4. Model Training with hyperparameter tuning
5. Model Evaluation (accuracy, fairness, explainability)
6. Model Registration
7. Deployment

**Platform Comparison:**
- **Kubeflow Pipelines**: ML-native, Kubernetes-based
- **Apache Airflow**: Mature, general-purpose, large ecosystem
- **Metaflow**: Netflix, data science-friendly, easy for scientists
- **Prefect**: Modern, dynamic workflows, better error handling than Airflow
- **Dagster**: Asset-based thinking, strong testing features

### 6. Model Monitoring and Drift Detection

**Data Drift Detection:**
- Kolmogorov-Smirnov (KS) Test: Compare distributions
- Population Stability Index (PSI): Measure distribution shift
- Chi-Square Test: For categorical features

**Model Drift Detection:**
- Ground truth accuracy (delayed labels)
- Prediction distribution changes
- Calibration drift (predicted probabilities vs actual outcomes)

**Performance Monitoring:**
- Latency: P50, P95, P99 inference time
- Throughput: Predictions per second
- Error Rate: Failed predictions / total
- Resource Utilization: CPU, memory, GPU usage

**Tools:**
- Evidently AI: Data drift, model drift reports
- Prometheus + Grafana: Performance metrics
- Arize AI: ML observability platform
- Fiddler: Model monitoring and explainability

### 7. Model Optimization Techniques

**Quantization:** Convert float32 to int8 (4x smaller, 2-3x faster)

**Model Distillation:** Train small student model to mimic large teacher (2-10x smaller)

**ONNX Conversion:** Cross-framework compatibility, optimized inference (1.5-3x faster)

**Model Pruning:** Remove less important weights (2-10x smaller)

### 8. LLMOps Patterns

**LLM Fine-Tuning:** LoRA and QLoRA for parameter-efficient fine-tuning

**Prompt Versioning:** Version control for prompts, A/B testing

**RAG System Monitoring:** Retrieval quality, generation quality, hallucination detection

**LLM Inference Optimization:**
- vLLM: High-throughput LLM serving
- TensorRT-LLM: NVIDIA-optimized
- Text Generation Inference (TGI): Hugging Face serving

### 9. Model Governance and Compliance

**Model Cards:** Documentation of model purpose, limitations, biases, ethical considerations

**Bias and Fairness Detection:**
- Tools: Fairlearn, AI Fairness 360 (IBM)
- Metrics: Demographic parity, equalized odds, calibration

**Regulatory Compliance:**
- EU AI Act: High-risk AI systems documentation
- Model Risk Management (SR 11-7): Banking requirements
- GDPR: Right to explanation
- HIPAA: Healthcare data privacy

## Quick Start

### Setup MLflow Server
```bash
# Install MLflow
pip install mlflow

# Start local tracking server
mlflow server --host 0.0.0.0 --port 5000
```

### Track Experiments
```python
import mlflow
from sklearn.ensemble import RandomForestClassifier

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("my-experiment")

with mlflow.start_run():
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_param("n_estimators", 100)
    mlflow.sklearn.log_model(model, "model")
```

### Deploy with BentoML
```python
import bentoml
from sklearn.ensemble import RandomForestClassifier

# Train and save model
model = RandomForestClassifier()
model.fit(X_train, y_train)
bentoml.sklearn.save_model("my_model", model)

# Create service
import bentoml
from bentoml.io import JSON

@bentoml.service
class MyService:
    model = bentoml.sklearn.get("my_model:latest")

    @bentoml.api
    def predict(self, input_data: JSON) -> JSON:
        return self.model.predict([input_data])
```

## Tool Recommendations

### Production-Ready Stack (Startup)
- **Experiment Tracking**: MLflow (free, self-hosted)
- **Feature Store**: Skip initially → Feast when needed
- **Model Serving**: BentoML (easy) or cloud functions
- **Orchestration**: Prefect or cron jobs
- **Monitoring**: Basic logging + Prometheus

### Production-Ready Stack (Growth Company)
- **Experiment Tracking**: Weights & Biases or MLflow
- **Feature Store**: Feast (open-source, production-ready)
- **Model Serving**: BentoML or KServe (Kubernetes-based)
- **Orchestration**: Kubeflow Pipelines or Airflow
- **Monitoring**: Evidently + Prometheus + Grafana

### Production-Ready Stack (Enterprise)
- **Experiment Tracking**: MLflow (self-hosted) or Neptune.ai (compliance)
- **Feature Store**: Tecton (managed) or Feast (self-hosted)
- **Model Serving**: Seldon Core (advanced) or KServe
- **Orchestration**: Kubeflow Pipelines or Airflow
- **Monitoring**: Evidently + Prometheus + Grafana + PagerDuty

## Related Skills

- **ai-data-engineering**: Feature engineering, ML algorithms, data preparation
- **kubernetes-operations**: K8s cluster management, GPU scheduling for ML workloads
- **implementing-observability**: Monitoring, alerting, distributed tracing for ML systems
- **designing-distributed-systems**: Scalability patterns for ML workloads
- **building-ai-chat**: LLM-powered applications consuming ML models

## Best Practices

1. **Version Everything**: Code (Git), data (DVC), models (semantic versioning), features
2. **Automate Testing**: Unit tests, integration tests, model validation
3. **Monitor Continuously**: Data drift, model drift, performance
4. **Start Simple**: Begin with MLflow + basic serving, add complexity as needed
5. **Point-in-Time Correctness**: Use feature stores to avoid training/serving skew
6. **Deployment Strategies**: Use canary for medium-risk, shadow for high-risk models
7. **Governance**: Model cards, audit trails, compliance tracking
8. **Cost Optimization**: Quantization, spot instances, autoscaling

## References

- Full skill documentation: `/skills/implementing-mlops/SKILL.md`
- Experiment tracking guide: `/skills/implementing-mlops/references/experiment-tracking.md`
- Model registry patterns: `/skills/implementing-mlops/references/model-registry.md`
- Feature stores: `/skills/implementing-mlops/references/feature-stores.md`
- Model serving: `/skills/implementing-mlops/references/model-serving.md`
- Deployment strategies: `/skills/implementing-mlops/references/deployment-strategies.md`
- ML pipelines: `/skills/implementing-mlops/references/ml-pipelines.md`
- Model monitoring: `/skills/implementing-mlops/references/model-monitoring.md`
- LLMOps patterns: `/skills/implementing-mlops/references/llmops-patterns.md`
