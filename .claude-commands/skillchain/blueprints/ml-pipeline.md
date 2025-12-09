# ML Pipeline Blueprint

**Version:** 1.0.0
**Last Updated:** 2024-12-06
**Category:** AI-ML

---

## Overview

Pre-configured skill chain optimized for building end-to-end machine learning pipelines, MLOps workflows, experiment tracking, model training, and deployment infrastructure. This blueprint provides production-ready defaults for the most common ML pipeline patterns, minimizing configuration while maximizing reproducibility and operational excellence.

---

## Trigger Keywords

**Primary (high confidence):**
- ml pipeline
- machine learning pipeline
- model training
- mlops
- ml workflow
- training pipeline

**Secondary (medium confidence):**
- experiment tracking
- model serving
- model deployment
- feature store
- model registry
- mlflow
- kubeflow
- sagemaker
- vertex ai
- model monitoring
- ml infrastructure

**Example goals that match:**
- "ml pipeline for image classification"
- "machine learning pipeline with experiment tracking"
- "end-to-end mlops workflow"
- "training pipeline with feature store"
- "model serving infrastructure"
- "ml pipeline with mlflow and model registry"
- "production ml pipeline for recommendation system"
- "automated training and deployment pipeline"

---

## Skill Chain (Pre-configured)

This blueprint invokes 7 skills in the following order:

```
1. implementing-mlops            (core - ML pipeline orchestration)
2. engineering-ai-data           (feature engineering and data preparation)
3. managing-experiments          (experiment tracking and versioning)
4. serving-models                (model deployment and inference)
5. designing-databases-vector    (optional - for embeddings/similarity)
6. implementing-observability    (monitoring, logging, alerting)
7. assembling-components         (final integration and validation)
```

**Total estimated time:** 35-50 minutes
**Total estimated questions:** 15-20 questions (or 3 with blueprint defaults)

---

## Pre-configured Defaults

### 1. implementing-mlops
```yaml
orchestration: "prefect"
  # Modern workflow orchestration with Python-native API
  # Alternatives: Airflow (complex), Kubeflow (K8s-native), Metaflow (AWS)
  # Prefect chosen for: Pythonic, dynamic workflows, built-in retries

pipeline_stages:
  - data_ingestion       # Load raw data from sources
  - data_validation      # Schema validation, quality checks
  - feature_engineering  # Transform raw data into features
  - data_splitting       # Train/validation/test splits
  - model_training       # Train model with hyperparameters
  - model_evaluation     # Compute metrics, validate performance
  - model_registration   # Register to model registry
  - model_deployment     # Deploy to serving infrastructure
  - monitoring_setup     # Configure drift detection

versioning: "dvc"
  # Data Version Control for datasets and models
  # Integrates with Git for reproducibility
  # Supports S3, GCS, Azure Blob storage

containerization: "docker"
  # Reproducible training environments
  # Consistent deployment across dev/staging/prod
  # Multi-stage builds for optimization

infrastructure: "kubernetes"
  # Scalable training with auto-scaling
  # GPU/TPU support for deep learning
  # Resource isolation and management
  # Alternative: Cloud-specific (SageMaker, Vertex AI)
```

### 2. engineering-ai-data
```yaml
feature_store: "feast"
  # Open-source feature store for feature management
  # Online + offline feature serving
  # Point-in-time correct feature retrieval
  # Alternative: Tecton (managed), AWS Feature Store

data_validation: "great-expectations"
  # Data quality assertions
  # Automatic profiling and documentation
  # Integration with pipelines for early failure

preprocessing_framework: "scikit-learn"
  # StandardScaler, OneHotEncoder, Pipeline
  # Consistent transformations across train/serve
  # Serializable for deployment

feature_engineering_tools:
  - pandas: "Data manipulation and aggregation"
  - numpy: "Numerical operations"
  - category_encoders: "Advanced categorical encoding"
  - feature_engine: "Feature engineering transformations"

storage_format: "parquet"
  # Columnar format for efficient storage and queries
  # Compression enabled (snappy)
  # Schema enforcement
```

### 3. managing-experiments
```yaml
tracking_system: "mlflow"
  # De facto standard for ML experiment tracking
  # Logs: params, metrics, artifacts, models
  # UI for experiment comparison
  # Model registry integration

logging_frequency: "per-epoch"
  # Log training metrics after each epoch
  # Balance between granularity and overhead
  # Adjustable for long-running training

metrics_tracked:
  - loss: "Training loss per epoch"
  - val_loss: "Validation loss per epoch"
  - accuracy: "Validation accuracy"
  - custom_metrics: "Task-specific metrics (F1, AUC, etc.)"
  - system_metrics: "GPU utilization, memory, training time"

artifact_storage:
  - model_checkpoints: "Best model weights"
  - feature_importance: "Feature contribution plots"
  - confusion_matrix: "Classification performance"
  - training_curves: "Loss and metric plots"
  - hyperparameters: "Full config files"

comparison_enabled: true
  # Side-by-side experiment comparison in UI
  # Automatic best model selection by metric
  # Export comparison reports
```

### 4. serving-models
```yaml
serving_framework: "fastapi"
  # REST API for model inference
  # Async support for high throughput
  # Automatic OpenAPI documentation
  # Easy integration with load balancers

model_format: "mlflow-models"
  # Platform-agnostic model serialization
  # Includes preprocessing, model, postprocessing
  # Version controlled and reproducible

prediction_types:
  - batch: "Offline batch predictions (high volume)"
  - real-time: "Online predictions (low latency)"
  - streaming: "Event-driven predictions (Kafka/Kinesis)"

optimization:
  - model_quantization: false  # Enable for edge deployment
  - onnx_conversion: false     # Cross-framework optimization
  - batching: true             # Dynamic batching for throughput
  - caching: true              # Cache frequent predictions

load_balancing: "kubernetes-service"
  # Automatic load balancing across pods
  # Horizontal pod autoscaling based on CPU/requests
  # Rolling updates for zero-downtime deployments

monitoring:
  - latency_tracking: true     # P50, P95, P99 latencies
  - throughput_metrics: true   # Requests per second
  - error_rates: true          # 4xx, 5xx errors
  - model_version: true        # Track which model version served
```

### 5. designing-databases-vector (optional)
```yaml
vector_db: "qdrant"
  # High-performance vector similarity search
  # Native filtering and hybrid search
  # Docker-ready, cloud-managed option available
  # Alternatives: Pinecone (managed), Weaviate, Milvus

use_cases:
  - embeddings_storage: "Store model embeddings for similarity search"
  - knn_retrieval: "K-nearest neighbors for recommendations"
  - semantic_search: "Natural language query matching"
  - rag_systems: "Retrieval-augmented generation pipelines"

enabled_when:
  - model_type == "embedding"
  - model_type == "llm" and rag_enabled
  - use_case == "recommendation"
  - use_case == "similarity_search"

skip_when:
  - model_type == "tabular"
  - model_type == "time_series"
  - no_embeddings_required
```

### 6. implementing-observability
```yaml
monitoring_stack: "prometheus-grafana"
  # Prometheus: Metrics collection and alerting
  # Grafana: Visualization dashboards
  # Industry standard for ML monitoring

metrics_monitored:
  training_metrics:
    - training_duration: "Time per training run"
    - dataset_size: "Number of samples processed"
    - gpu_utilization: "GPU memory and compute usage"
    - training_loss_convergence: "Final training loss"

  serving_metrics:
    - prediction_latency: "P50, P95, P99 latencies"
    - throughput: "Predictions per second"
    - error_rate: "Failed prediction percentage"
    - model_version_distribution: "Which versions are serving"

  data_quality_metrics:
    - feature_drift: "Distribution shift in input features"
    - prediction_drift: "Distribution shift in predictions"
    - missing_values: "Percentage of null features"
    - outliers_detected: "Out-of-distribution inputs"

alerting_rules:
  - high_latency: "P95 latency > 500ms for 5 minutes"
  - low_accuracy: "Validation accuracy drops > 5% from baseline"
  - feature_drift: "Feature distribution shift > 0.3 (KL divergence)"
  - service_down: "Model API unavailable for 2 minutes"
  - gpu_memory: "GPU memory > 90% for 10 minutes"

logging: "structured-json"
  # JSON-formatted logs for easy parsing
  # Centralized logging with ELK/Loki
  # Request ID tracking for distributed tracing

dashboards:
  - training_overview: "Training runs, loss curves, experiment comparison"
  - serving_overview: "Latency, throughput, error rates, version distribution"
  - data_quality: "Feature drift, data validation failures"
  - infrastructure: "CPU, memory, GPU utilization, costs"
```

### 7. assembling-components
```yaml
project_structure: "ml-cookiecutter"
  # Standard ML project template
  # Separation: data, models, notebooks, src, tests
  # CI/CD integration ready

testing_framework: "pytest"
  # Unit tests for data processing functions
  # Integration tests for pipeline stages
  # Model performance tests (accuracy thresholds)

ci_cd_pipeline: "github-actions"
  # Automated testing on PR
  # Model training on merge to main
  # Deployment to staging/production
  # Alternatives: GitLab CI, Jenkins, CircleCI

environment_management: "conda"
  # Reproducible Python environments
  # Environment.yml for dependency tracking
  # Alternative: Poetry, pipenv

documentation:
  - model_cards: "Model metadata, performance, limitations"
  - api_docs: "OpenAPI specs for serving endpoints"
  - pipeline_docs: "Data flow, stage descriptions, runbooks"
  - setup_guide: "Local development, deployment instructions"

production_checks:
  - unit_test_coverage: ">= 80%"
  - integration_tests: "All pipeline stages pass"
  - model_accuracy_threshold: "Defined per use case"
  - latency_sla: "P95 < 500ms (configurable)"
  - data_validation: "Schema checks pass"
```

---

## Quick Questions (Only 3)

When blueprint is detected, ask only these essential questions:

### Question 1: ML Type and Use Case
```
What type of ML problem are you solving?

Options:
1. Traditional ML (classification, regression, clustering)
   - Examples: Fraud detection, price prediction, customer segmentation

2. Deep Learning (computer vision, NLP, generative)
   - Examples: Image classification, text generation, object detection

3. LLM/RAG (large language models, retrieval-augmented generation)
   - Examples: Chatbots, document Q&A, semantic search

4. Time Series (forecasting, anomaly detection)
   - Examples: Sales forecasting, predictive maintenance

Your answer (1/2/3/4): _______________
```

**Why this matters:**
- Determines framework selection (scikit-learn vs PyTorch vs transformers)
- Influences infrastructure requirements (GPU/TPU needs)
- Affects vector database inclusion (LLM/RAG requires it)
- Shapes monitoring metrics (accuracy vs perplexity vs MSE)

**Default if skipped:** "1 - Traditional ML"

**Blueprint adjustments:**
- **Option 1:** sklearn + CPU training + standard metrics
- **Option 2:** PyTorch/TensorFlow + GPU training + tensorboard integration
- **Option 3:** transformers + vector DB + embedding monitoring + LLM observability
- **Option 4:** statsmodels/prophet + time-series specific validation

---

### Question 2: Training Infrastructure
```
Where will model training run?

Options:
1. Local development (laptop/workstation)
   - Best for: Small datasets, experimentation, prototyping
   - Resource limits: CPU-only or single GPU

2. Cloud VMs (AWS EC2, GCP Compute, Azure VMs)
   - Best for: Medium datasets, on-demand GPU access
   - Requires: Cloud provider setup, cost monitoring

3. Kubernetes cluster (self-managed or managed)
   - Best for: Large-scale training, distributed jobs
   - Requires: K8s knowledge, cluster setup

4. Managed ML platform (SageMaker, Vertex AI, Azure ML)
   - Best for: Fully managed, auto-scaling, minimal ops
   - Trade-off: Higher cost, vendor lock-in

Your answer (1/2/3/4): _______________
```

**Why this matters:**
- Determines orchestration complexity (local scripts vs K8s jobs)
- Affects Docker configuration (multi-stage builds, base images)
- Influences monitoring setup (local logs vs centralized metrics)
- Shapes deployment strategy (single instance vs autoscaling)

**Default if skipped:** "2 - Cloud VMs"

**Blueprint adjustments:**
- **Option 1:** Docker Compose, local MLflow, simple scripts
- **Option 2:** Single-node training, cloud storage (S3/GCS), remote MLflow
- **Option 3:** Kubernetes jobs, distributed training, Helm charts, cluster monitoring
- **Option 4:** Platform-specific SDKs (boto3, google-cloud-aiplatform), managed endpoints

---

### Question 3: MLOps Maturity Level
```
What's your MLOps maturity and requirements?

Options:
1. Starter (manual workflows, exploration focused)
   - Features: Jupyter notebooks, basic experiment tracking
   - Deployment: Manual model deployment, simple API
   - Monitoring: Basic logging, no drift detection

2. Production (automated pipelines, business critical)
   - Features: Automated training, CI/CD, model registry
   - Deployment: Automated deployment, canary/blue-green
   - Monitoring: Full observability, drift detection, alerts

3. Advanced (high-scale, multi-model, complex workflows)
   - Features: A/B testing, multi-model ensembles, auto-retraining
   - Deployment: Multi-region, edge deployment, model caching
   - Monitoring: Real-time monitoring, automated rollbacks, cost tracking

Your answer (1/2/3): _______________
```

**Why this matters:**
- Determines automation level (manual vs fully automated)
- Affects tooling complexity (simple scripts vs Kubeflow pipelines)
- Influences testing requirements (basic tests vs comprehensive suite)
- Shapes monitoring depth (logs only vs full observability)

**Default if skipped:** "2 - Production"

**Blueprint adjustments:**
- **Option 1:** Minimal automation, notebook-driven, simple FastAPI, basic MLflow
- **Option 2:** Full pipeline automation, comprehensive testing, drift monitoring, alerting (DEFAULT)
- **Option 3:** Advanced orchestration, multi-model serving, feature stores, cost optimization, A/B testing

---

## Blueprint Detection Logic

Trigger this blueprint when the user's goal matches:

```python
def should_use_ml_pipeline_blueprint(goal: str) -> bool:
    goal_lower = goal.lower()

    # Primary keywords (high confidence)
    primary_match = any(keyword in goal_lower for keyword in [
        "ml pipeline",
        "machine learning pipeline",
        "mlops",
        "training pipeline",
        "ml workflow",
        "model pipeline"
    ])

    # Secondary keywords + ML context
    secondary_match = (
        any(keyword in goal_lower for keyword in [
            "experiment tracking", "model training", "model serving",
            "feature store", "model registry", "mlflow", "kubeflow"
        ]) and
        any(keyword in goal_lower for keyword in [
            "pipeline", "workflow", "automation", "deployment", "infrastructure"
        ])
    )

    # ML problem + infrastructure keywords
    tertiary_match = (
        any(keyword in goal_lower for keyword in [
            "classification", "regression", "deep learning",
            "neural network", "llm", "time series forecasting"
        ]) and
        any(keyword in goal_lower for keyword in [
            "end-to-end", "production", "deployment", "serving", "monitoring"
        ])
    )

    return primary_match or secondary_match or tertiary_match
```

**Confidence levels:**
- **High (90%+):** Contains "ml pipeline" or "mlops" + infrastructure term
- **Medium (70-89%):** Contains ML tool (mlflow, kubeflow) + "pipeline" or "workflow"
- **Low (50-69%):** Contains ML problem + production/deployment terms

**Present blueprint when confidence >= 70%**

---

## Blueprint Offer Message

When blueprint is detected, present this message to the user:

```
┌────────────────────────────────────────────────────────────┐
│ 🤖 ML PIPELINE BLUEPRINT DETECTED                          │
├────────────────────────────────────────────────────────────┤
│ Your goal matches our optimized ML Pipeline Blueprint!    │
│                                                            │
│ Pre-configured features:                                   │
│  ✓ End-to-end ML pipeline (data → training → serving)    │
│  ✓ MLflow experiment tracking & model registry           │
│  ✓ Feature store (Feast) for feature management          │
│  ✓ Model serving API (FastAPI) with monitoring           │
│  ✓ Data validation & drift detection                     │
│  ✓ Kubernetes-ready containerized deployment             │
│  ✓ Prometheus + Grafana observability stack              │
│  ✓ Automated CI/CD with testing                          │
│                                                            │
│ Using blueprint reduces questions from 20 to 3!           │
│                                                            │
│ Options:                                                   │
│  1. Use blueprint (3 quick questions, ~15 min)            │
│  2. Custom configuration (20 questions, ~45 min)          │
│  3. Skip all questions (use all defaults, ~8 min)         │
│                                                            │
│ Your choice (1/2/3): _____                                │
└────────────────────────────────────────────────────────────┘
```

**Handle responses:**
- **1 or "blueprint"** → Ask only 3 blueprint questions
- **2 or "custom"** → Ask all skill questions (normal flow)
- **3 or "skip"** → Use all defaults, skip all questions

---

## Generated Output Structure

When blueprint is executed, generate this file structure:

```
ml-pipeline-project/
├── data/
│   ├── raw/                          # Raw, immutable data
│   ├── processed/                    # Cleaned, transformed data
│   ├── features/                     # Feature store outputs
│   └── external/                     # External data sources
│
├── models/
│   ├── trained/                      # Serialized trained models
│   ├── checkpoints/                  # Training checkpoints
│   └── registered/                   # Model registry artifacts
│
├── notebooks/
│   ├── 01_exploration.ipynb          # Data exploration
│   ├── 02_feature_engineering.ipynb  # Feature development
│   ├── 03_model_training.ipynb       # Model experimentation
│   └── 04_evaluation.ipynb           # Model evaluation
│
├── src/
│   ├── data/
│   │   ├── __init__.py
│   │   ├── ingestion.py              # Data loading from sources
│   │   ├── validation.py             # Great Expectations checks
│   │   ├── preprocessing.py          # Data cleaning, normalization
│   │   └── splitting.py              # Train/val/test splits
│   │
│   ├── features/
│   │   ├── __init__.py
│   │   ├── feature_engineering.py    # Feature transformations
│   │   ├── feature_store.py          # Feast integration
│   │   └── feature_definitions.py    # Feature metadata
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── train.py                  # Training logic
│   │   ├── evaluate.py               # Evaluation metrics
│   │   ├── predict.py                # Inference logic
│   │   └── hyperparameters.py        # Hyperparameter configs
│   │
│   ├── serving/
│   │   ├── __init__.py
│   │   ├── api.py                    # FastAPI application
│   │   ├── schemas.py                # Pydantic request/response models
│   │   ├── model_loader.py           # Load models from registry
│   │   └── preprocessing.py          # Inference-time preprocessing
│   │
│   ├── monitoring/
│   │   ├── __init__.py
│   │   ├── drift_detection.py        # Feature/prediction drift
│   │   ├── metrics_logger.py         # Prometheus metrics
│   │   └── alerting.py               # Alert rule definitions
│   │
│   └── utils/
│       ├── __init__.py
│       ├── config.py                 # Configuration management
│       ├── logging.py                # Structured logging setup
│       └── storage.py                # Cloud storage helpers (S3/GCS)
│
├── pipelines/
│   ├── __init__.py
│   ├── training_pipeline.py          # Prefect training workflow
│   ├── inference_pipeline.py         # Batch inference workflow
│   └── monitoring_pipeline.py        # Drift detection workflow
│
├── tests/
│   ├── unit/
│   │   ├── test_data_validation.py
│   │   ├── test_preprocessing.py
│   │   ├── test_feature_engineering.py
│   │   ├── test_model_training.py
│   │   └── test_api.py
│   │
│   ├── integration/
│   │   ├── test_training_pipeline.py
│   │   ├── test_serving_pipeline.py
│   │   └── test_end_to_end.py
│   │
│   └── fixtures/
│       ├── sample_data.csv
│       └── test_config.yaml
│
├── config/
│   ├── model_config.yaml             # Model hyperparameters
│   ├── pipeline_config.yaml          # Pipeline settings
│   ├── serving_config.yaml           # API configuration
│   └── monitoring_config.yaml        # Alert thresholds
│
├── infrastructure/
│   ├── docker/
│   │   ├── Dockerfile.training       # Training environment
│   │   ├── Dockerfile.serving        # Serving environment
│   │   └── docker-compose.yml        # Local development stack
│   │
│   ├── kubernetes/
│   │   ├── training-job.yaml         # K8s training job
│   │   ├── serving-deployment.yaml   # Model serving deployment
│   │   ├── monitoring-stack.yaml     # Prometheus/Grafana
│   │   └── secrets.yaml              # Secrets (template)
│   │
│   └── terraform/                    # Infrastructure as code (optional)
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
│
├── monitoring/
│   ├── grafana/
│   │   └── dashboards/
│   │       ├── training_metrics.json
│   │       ├── serving_metrics.json
│   │       └── data_quality.json
│   │
│   └── prometheus/
│       ├── prometheus.yml            # Prometheus config
│       └── alert_rules.yml           # Alerting rules
│
├── .github/
│   └── workflows/
│       ├── ci.yml                    # Run tests on PR
│       ├── train.yml                 # Trigger training on merge
│       └── deploy.yml                # Deploy to staging/prod
│
├── mlruns/                           # MLflow tracking (local)
├── .dvc/                             # DVC metadata
├── .gitignore
├── .dvcignore
├── dvc.yaml                          # DVC pipeline definition
├── pyproject.toml                    # Poetry/pip dependencies
├── environment.yml                   # Conda environment
├── README.md                         # Setup and usage guide
├── Makefile                          # Common commands (train, serve, test)
└── model_card.md                     # Model documentation template
```

---

## Pipeline Architecture

### End-to-End Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     ML PIPELINE ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 1. DATA INGESTION                                        │  │
│  │  - Load from sources (databases, APIs, files)            │  │
│  │  - Schema validation (Great Expectations)               │  │
│  │  - Data quality checks                                   │  │
│  │  - Store in data/raw/                                    │  │
│  └────────────────────┬─────────────────────────────────────┘  │
│                       │                                         │
│  ┌────────────────────▼─────────────────────────────────────┐  │
│  │ 2. DATA PREPROCESSING                                    │  │
│  │  - Cleaning (missing values, outliers)                   │  │
│  │  - Normalization/standardization                         │  │
│  │  - Train/val/test split (stratified)                     │  │
│  │  - Store in data/processed/                              │  │
│  └────────────────────┬─────────────────────────────────────┘  │
│                       │                                         │
│  ┌────────────────────▼─────────────────────────────────────┐  │
│  │ 3. FEATURE ENGINEERING                                   │  │
│  │  - Feature transformations                               │  │
│  │  - Categorical encoding                                  │  │
│  │  - Feature selection                                     │  │
│  │  - Register features to Feast                           │  │
│  │  - Store in data/features/                               │  │
│  └────────────────────┬─────────────────────────────────────┘  │
│                       │                                         │
│  ┌────────────────────▼─────────────────────────────────────┐  │
│  │ 4. MODEL TRAINING                                        │  │
│  │  - Load features from feature store                      │  │
│  │  - Initialize model (sklearn/PyTorch/TensorFlow)         │  │
│  │  - Train with hyperparameters                            │  │
│  │  - Log metrics to MLflow (loss, accuracy, etc.)          │  │
│  │  - Save checkpoints to models/checkpoints/               │  │
│  └────────────────────┬─────────────────────────────────────┘  │
│                       │                                         │
│  ┌────────────────────▼─────────────────────────────────────┐  │
│  │ 5. MODEL EVALUATION                                      │  │
│  │  - Compute metrics on validation set                     │  │
│  │  - Generate confusion matrix, ROC curves                 │  │
│  │  - Compare with previous best model                      │  │
│  │  - Log artifacts to MLflow                               │  │
│  │  - Decision: Register if better than baseline            │  │
│  └────────────────────┬─────────────────────────────────────┘  │
│                       │                                         │
│              ┌────────▼───────┐                                │
│              │ Meets criteria? │                               │
│              └────┬───────┬────┘                               │
│                   Yes    No                                    │
│                   │      │                                     │
│  ┌────────────────▼──┐   └──────> End (log failure)           │
│  │ 6. MODEL REGISTRY │                                        │
│  │  - Register to MLflow Model Registry                      │  │
│  │  - Tag version (staging/production)                       │  │
│  │  - Store model card metadata                              │  │
│  │  - Archive trained model                                  │  │
│  └────────────────┬──┘                                        │
│                   │                                            │
│  ┌────────────────▼─────────────────────────────────────────┐ │
│  │ 7. MODEL DEPLOYMENT                                      │ │
│  │  - Load model from registry                              │ │
│  │  - Build serving container (FastAPI + model)             │ │
│  │  - Deploy to K8s (or cloud platform)                     │ │
│  │  - Health check and smoke tests                          │ │
│  │  - Gradual rollout (canary/blue-green)                   │ │
│  └────────────────┬─────────────────────────────────────────┘ │
│                   │                                            │
│  ┌────────────────▼─────────────────────────────────────────┐ │
│  │ 8. MONITORING & FEEDBACK                                 │ │
│  │  - Log predictions and latencies                         │ │
│  │  - Detect feature/prediction drift                       │ │
│  │  - Monitor model performance degradation                 │ │
│  │  - Alert on anomalies                                    │ │
│  │  - Trigger retraining if drift detected                  │ │
│  └──────────────────────────────────────────────────────────┘ │
│                   │                                            │
│                   └───────────> Feedback loop (retrain)        │
│                                                                │
└─────────────────────────────────────────────────────────────────┘
```

### Orchestration with Prefect

```python
from prefect import flow, task
from prefect.deployments import Deployment

@task
def ingest_data():
    """Load and validate data from sources."""
    pass

@task
def preprocess_data(raw_data):
    """Clean and split data."""
    pass

@task
def engineer_features(processed_data):
    """Generate features and register to Feast."""
    pass

@task
def train_model(features, labels):
    """Train model and log to MLflow."""
    pass

@task
def evaluate_model(model, val_features, val_labels):
    """Compute metrics and decide registration."""
    pass

@task
def register_model(model, metrics):
    """Register to MLflow Model Registry."""
    pass

@task
def deploy_model(model_uri):
    """Deploy to serving infrastructure."""
    pass

@flow(name="ml-training-pipeline")
def training_pipeline():
    """End-to-end training pipeline."""
    raw_data = ingest_data()
    processed_data = preprocess_data(raw_data)
    features, labels = engineer_features(processed_data)
    model = train_model(features, labels)
    metrics = evaluate_model(model, val_features, val_labels)

    if metrics['accuracy'] > 0.85:  # Threshold
        model_uri = register_model(model, metrics)
        deploy_model(model_uri)
```

---

## Default Model Configurations

### Traditional ML (scikit-learn)
```python
# config/model_config.yaml
model_type: "random_forest"
hyperparameters:
  n_estimators: 100
  max_depth: 10
  min_samples_split: 5
  random_state: 42

training:
  cross_validation: 5
  scoring: "accuracy"

evaluation:
  metrics: ["accuracy", "precision", "recall", "f1", "roc_auc"]
  threshold: 0.85  # Minimum accuracy for registration
```

### Deep Learning (PyTorch)
```python
# config/model_config.yaml
model_type: "neural_network"
architecture:
  input_size: 784
  hidden_layers: [256, 128, 64]
  output_size: 10
  activation: "relu"
  dropout: 0.3

training:
  optimizer: "adam"
  learning_rate: 0.001
  batch_size: 32
  epochs: 50
  early_stopping:
    patience: 5
    min_delta: 0.001
    monitor: "val_loss"

evaluation:
  metrics: ["accuracy", "loss", "confusion_matrix"]
  threshold: 0.90
```

### LLM/RAG Pipeline
```python
# config/model_config.yaml
model_type: "llm_rag"
llm:
  provider: "openai"  # or "anthropic", "huggingface"
  model: "gpt-4-turbo"
  temperature: 0.7
  max_tokens: 500

embeddings:
  model: "text-embedding-3-small"
  dimension: 1536

vector_store:
  provider: "qdrant"
  collection: "documents"
  similarity_metric: "cosine"

retrieval:
  top_k: 5
  score_threshold: 0.7

evaluation:
  metrics: ["relevance_score", "answer_accuracy", "latency"]
```

---

## Dependencies

The blueprint includes these Python packages:

```toml
# pyproject.toml
[tool.poetry.dependencies]
python = "^3.9"

# Core ML
scikit-learn = "^1.3.0"           # Traditional ML
pandas = "^2.0.0"                 # Data manipulation
numpy = "^1.24.0"                 # Numerical computing

# Optional: Deep Learning (if selected)
torch = { version = "^2.0.0", optional = true }
tensorflow = { version = "^2.13.0", optional = true }

# Experiment Tracking
mlflow = "^2.8.0"                 # Experiment tracking, model registry

# Feature Store
feast = "^0.35.0"                 # Feature store

# Data Validation
great-expectations = "^0.18.0"    # Data quality

# Orchestration
prefect = "^2.14.0"               # Workflow orchestration

# Model Serving
fastapi = "^0.104.0"              # API framework
uvicorn = "^0.24.0"               # ASGI server
pydantic = "^2.5.0"               # Data validation

# Monitoring
prometheus-client = "^0.18.0"     # Metrics export
evidently = "^0.4.0"              # Drift detection

# Storage
dvc = "^3.30.0"                   # Data version control
boto3 = "^1.28.0"                 # AWS SDK (optional)
google-cloud-storage = "^2.10.0"  # GCS SDK (optional)

# Optional: Vector DB (if LLM/RAG selected)
qdrant-client = { version = "^1.6.0", optional = true }
sentence-transformers = { version = "^2.2.0", optional = true }

# Optional: LLM (if selected)
openai = { version = "^1.3.0", optional = true }
transformers = { version = "^4.35.0", optional = true }

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-cov = "^4.1.0"
black = "^23.10.0"
ruff = "^0.1.5"
mypy = "^1.6.0"

[tool.poetry.extras]
deep-learning-torch = ["torch", "torchvision"]
deep-learning-tf = ["tensorflow"]
llm = ["openai", "transformers", "qdrant-client", "sentence-transformers"]
cloud-aws = ["boto3", "sagemaker"]
cloud-gcp = ["google-cloud-storage", "google-cloud-aiplatform"]
```

---

## Monitoring Dashboards

### 1. Training Metrics Dashboard (Grafana)
```json
{
  "dashboard": "ML Training Overview",
  "panels": [
    {
      "title": "Training Loss Over Time",
      "type": "graph",
      "targets": ["training_loss", "validation_loss"]
    },
    {
      "title": "Model Accuracy",
      "type": "stat",
      "targets": ["validation_accuracy"]
    },
    {
      "title": "Training Duration",
      "type": "graph",
      "targets": ["training_duration_seconds"]
    },
    {
      "title": "GPU Utilization",
      "type": "gauge",
      "targets": ["gpu_memory_used_percent", "gpu_compute_percent"]
    },
    {
      "title": "Dataset Statistics",
      "type": "table",
      "targets": ["dataset_size", "num_features", "class_distribution"]
    }
  ]
}
```

### 2. Serving Metrics Dashboard (Grafana)
```json
{
  "dashboard": "Model Serving Overview",
  "panels": [
    {
      "title": "Prediction Latency (P95)",
      "type": "graph",
      "targets": ["prediction_latency_p95_ms"]
    },
    {
      "title": "Throughput (req/s)",
      "type": "graph",
      "targets": ["requests_per_second"]
    },
    {
      "title": "Error Rate",
      "type": "gauge",
      "targets": ["error_rate_percent"]
    },
    {
      "title": "Model Version Distribution",
      "type": "pie",
      "targets": ["model_version_served"]
    },
    {
      "title": "Feature Drift Detection",
      "type": "heatmap",
      "targets": ["feature_drift_score"]
    }
  ]
}
```

---

## CI/CD Pipeline (GitHub Actions)

### Automated Training on Merge
```yaml
# .github/workflows/train.yml
name: Train Model

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  train:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install poetry
          poetry install

      - name: Pull data with DVC
        run: dvc pull
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

      - name: Run training pipeline
        run: poetry run python pipelines/training_pipeline.py
        env:
          MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}

      - name: Evaluate model
        run: poetry run python src/models/evaluate.py

      - name: Register model (if meets criteria)
        run: |
          poetry run python scripts/register_model.py \
            --run-id ${{ env.MLFLOW_RUN_ID }} \
            --min-accuracy 0.85
```

---

## Testing Strategy

### Unit Tests
```python
# tests/unit/test_preprocessing.py
import pytest
from src.data.preprocessing import clean_data, normalize_features

def test_clean_data_removes_nulls():
    """Test that clean_data removes rows with null values."""
    dirty_data = pd.DataFrame({
        'feature1': [1, 2, None, 4],
        'feature2': [5, None, 7, 8]
    })
    cleaned = clean_data(dirty_data)
    assert cleaned.isnull().sum().sum() == 0
    assert len(cleaned) == 2  # Only 2 complete rows

def test_normalize_features_scales_to_zero_mean():
    """Test that normalization produces zero mean."""
    data = pd.DataFrame({'feature': [1, 2, 3, 4, 5]})
    normalized = normalize_features(data)
    assert abs(normalized['feature'].mean()) < 1e-10
    assert abs(normalized['feature'].std() - 1.0) < 1e-10
```

### Integration Tests
```python
# tests/integration/test_training_pipeline.py
import pytest
from pipelines.training_pipeline import training_pipeline

def test_full_training_pipeline():
    """Test end-to-end training pipeline."""
    result = training_pipeline()

    # Check pipeline completed
    assert result.state.is_completed()

    # Check model was registered
    assert result.artifacts['model_uri'] is not None

    # Check metrics meet threshold
    assert result.artifacts['accuracy'] >= 0.85
```

---

## Customization Points

After blueprint generation, users can easily customize:

1. **Model architecture:** Edit `src/models/train.py` and `config/model_config.yaml`
2. **Features:** Add feature engineering in `src/features/feature_engineering.py`
3. **Data sources:** Update `src/data/ingestion.py` with new connectors
4. **Hyperparameters:** Tune in `config/model_config.yaml`
5. **Deployment strategy:** Modify `infrastructure/kubernetes/serving-deployment.yaml`
6. **Monitoring alerts:** Configure thresholds in `monitoring/prometheus/alert_rules.yml`

---

## Migration Path

If user starts with blueprint but needs custom features later:

1. **Add hyperparameter tuning:** Integrate Optuna/Ray Tune
2. **Add distributed training:** Use Horovod/PyTorch DDP
3. **Add A/B testing:** Implement multi-armed bandit or Bayesian optimization
4. **Add model explainability:** Integrate SHAP/LIME
5. **Add federated learning:** Use Flower framework
6. **Add edge deployment:** Convert to ONNX/TensorRT

All additions will integrate with existing MLflow tracking and monitoring.

---

## Version History

**1.0.0** (2024-12-06)
- Initial ML pipeline blueprint
- 7-skill chain with production-ready defaults
- 3-question quick configuration
- MLflow + Feast + Prefect stack
- Kubernetes-ready deployment
- Full observability with Prometheus/Grafana
- Support for traditional ML, deep learning, LLM/RAG, time series

---

## Related Blueprints

- **API Blueprint:** For exposing models as REST/GraphQL APIs
- **Dashboard Blueprint:** For visualizing model performance metrics
- **Data Pipeline Blueprint:** For pure data engineering workflows
- **LLM Application Blueprint:** For LLM-powered applications with RAG

---

## Deliverables Specification

This section defines concrete validation checks for blueprint promises, ensuring skills produce what users expect.

### Deliverables

```yaml
deliverables:
  "MLflow experiment tracking":
    primary_skill: implementing-mlops
    required_files:
      - src/models/train.py
    content_checks:
      - pattern: "import mlflow"
        in: src/models/train.py
      - pattern: "mlflow\\.log|mlflow\\.start_run"
        in: src/models/train.py
    maturity_required: [starter, intermediate, advanced]

  "Training pipeline orchestration":
    primary_skill: implementing-mlops
    required_files:
      - pipelines/training_pipeline.py
    content_checks:
      - pattern: "@flow|@task|def.*pipeline"
        in: pipelines/training_pipeline.py
      - pattern: "import prefect|from prefect"
        in: pipelines/training_pipeline.py
    maturity_required: [intermediate, advanced]

  "Feature engineering code":
    primary_skill: engineering-ai-data
    required_files:
      - src/features/feature_engineering.py
    content_checks:
      - pattern: "class.*Feature|def.*feature|transform"
        in: src/features/feature_engineering.py
    maturity_required: [starter, intermediate, advanced]

  "Feature store (Feast)":
    primary_skill: engineering-ai-data
    required_files:
      - src/features/feature_store.py
      - src/features/feature_definitions.py
    content_checks:
      - pattern: "feast|FeatureStore|FeatureView"
        in: src/features/
    maturity_required: [intermediate, advanced]

  "Data validation (Great Expectations)":
    primary_skill: engineering-ai-data
    required_files:
      - src/data/validation.py
    content_checks:
      - pattern: "great_expectations|ExpectationSuite"
        in: src/data/validation.py
    maturity_required: [intermediate, advanced]

  "Model serving API":
    primary_skill: serving-models
    required_files:
      - src/serving/api.py
      - src/serving/schemas.py
    content_checks:
      - pattern: "FastAPI|@app\\.(get|post)"
        in: src/serving/api.py
      - pattern: "BaseModel|Schema"
        in: src/serving/schemas.py
    maturity_required: [starter, intermediate, advanced]

  "Model deployment infrastructure":
    primary_skill: serving-models
    required_files:
      - infrastructure/docker/Dockerfile.serving
    content_checks:
      - pattern: "FROM|CMD|ENTRYPOINT"
        in: infrastructure/docker/Dockerfile.serving
    maturity_required: [starter, intermediate, advanced]

  "Kubernetes deployment manifests":
    primary_skill: designing-databases-vector
    required_files:
      - infrastructure/kubernetes/deployment.yaml
      - infrastructure/kubernetes/service.yaml
    content_checks:
      - pattern: "kind: Deployment"
        in: infrastructure/kubernetes/deployment.yaml
      - pattern: "kind: Service"
        in: infrastructure/kubernetes/service.yaml
    maturity_required: [intermediate, advanced]

  "Prometheus monitoring configuration":
    primary_skill: implementing-observability
    required_files:
      - monitoring/prometheus/prometheus.yml
      - monitoring/prometheus/alert_rules.yml
    content_checks:
      - pattern: "scrape_configs|job_name"
        in: monitoring/prometheus/prometheus.yml
      - pattern: "alert:|expr:"
        in: monitoring/prometheus/alert_rules.yml
    maturity_required: [intermediate, advanced]

  "Grafana dashboards":
    primary_skill: implementing-observability
    required_files:
      - monitoring/grafana/dashboards/training_metrics.json
      - monitoring/grafana/dashboards/serving_metrics.json
    content_checks:
      - pattern: '"type":\\s*"graph"|"type":\\s*"gauge"'
        in: monitoring/grafana/dashboards/
      - pattern: '"title".*Training|"title".*Serving'
        in: monitoring/grafana/dashboards/
    maturity_required: [intermediate, advanced]

  "Sample data generation script":
    primary_skill: engineering-ai-data
    required_files:
      - scripts/generate_sample_data.py
    content_checks:
      - pattern: "def generate|def create"
        in: scripts/generate_sample_data.py
      - pattern: "to_csv|to_parquet|save"
        in: scripts/generate_sample_data.py
    maturity_required: [starter]

  "Quick start notebook":
    primary_skill: implementing-mlops
    required_files:
      - notebooks/01_quickstart.ipynb
    content_checks:
      - pattern: '"cell_type":\\s*"code"'
        in: notebooks/01_quickstart.ipynb
      - pattern: "train|mlflow|predict"
        in: notebooks/01_quickstart.ipynb
    maturity_required: [starter]

  "CI/CD pipeline configuration":
    primary_skill: assembling-components
    required_files:
      - .github/workflows/ci.yml
      - .github/workflows/train.yml
    content_checks:
      - pattern: "on:\\s*(push|pull_request)"
        in: .github/workflows/
      - pattern: "pytest|test"
        in: .github/workflows/ci.yml
    maturity_required: [intermediate, advanced]

  "Unit tests":
    primary_skill: assembling-components
    required_files:
      - tests/unit/test_preprocessing.py
      - tests/unit/test_model_training.py
    content_checks:
      - pattern: "def test_|@pytest"
        in: tests/unit/
      - pattern: "assert"
        in: tests/unit/
    maturity_required: [intermediate, advanced]

  "Integration tests":
    primary_skill: assembling-components
    required_files:
      - tests/integration/test_training_pipeline.py
    content_checks:
      - pattern: "def test_|@pytest"
        in: tests/integration/
      - pattern: "pipeline|end.to.end"
        in: tests/integration/
    maturity_required: [advanced]
```

### Maturity Profiles

```yaml
maturity_profiles:
  starter:
    description: "Learning-focused with working examples, extensive documentation, minimal infrastructure"

    require_additionally:
      - "Sample data generation script"
      - "Quick start notebook"
      - "Model serving API"
      - "MLflow experiment tracking"
      - "Feature engineering code"

    skip_deliverables:
      - "Feature store (Feast)"
      - "Data validation (Great Expectations)"
      - "Kubernetes deployment manifests"
      - "Prometheus monitoring configuration"
      - "Grafana dashboards"
      - "CI/CD pipeline configuration"
      - "Unit tests"
      - "Integration tests"

    empty_dirs_allowed:
      - infrastructure/kubernetes/
      - monitoring/grafana/dashboards/
      - monitoring/prometheus/
      - tests/integration/
      - data/raw/
      - data/processed/
      - models/trained/

    generation_adjustments:
      - Add extensive inline comments
      - Include README with step-by-step setup
      - Provide sample data out of the box
      - Use Docker Compose instead of Kubernetes
      - Include notebooks for exploration

  intermediate:
    description: "Production-ready patterns with automation, monitoring, and testing"

    require_additionally:
      - "CI/CD pipeline configuration"
      - "Unit tests"
      - "Prometheus monitoring configuration"
      - "Grafana dashboards"
      - "Feature store (Feast)"
      - "Data validation (Great Expectations)"
      - "Training pipeline orchestration"

    skip_deliverables:
      - "Integration tests"
      - "Sample data generation script"
      - "Quick start notebook"

    empty_dirs_allowed:
      - data/raw/
      - data/processed/
      - models/trained/
      - tests/fixtures/

    generation_adjustments:
      - Include production-grade error handling
      - Add monitoring and alerting
      - Set up CI/CD pipeline
      - Configure feature store
      - Enable data validation

  advanced:
    description: "Enterprise-scale with full automation, advanced monitoring, comprehensive testing"

    require_additionally:
      - "Kubernetes deployment manifests"
      - "Integration tests"
      - "Feature store (Feast)"
      - "Data validation (Great Expectations)"
      - "Prometheus monitoring configuration"
      - "Grafana dashboards"
      - "CI/CD pipeline configuration"
      - "Training pipeline orchestration"

    skip_deliverables: []

    empty_dirs_allowed:
      - data/raw/
      - data/processed/
      - models/trained/

    generation_adjustments:
      - Enable all features and integrations
      - Add comprehensive testing suite
      - Include performance optimization
      - Set up distributed training support
      - Configure multi-environment deployment
      - Enable advanced monitoring and observability
```

### Validation Process

After all skills complete, the skillchain orchestrator validates deliverables:

1. **Load maturity profile** - Determine which deliverables are required based on user's selected maturity level

2. **Check required files exist** - Verify each deliverable's required files are present in the generated project

3. **Run content checks** - Use grep/pattern matching to verify files contain expected code (not just scaffolding)

4. **Calculate completeness score**:
   ```
   completeness = (fulfilled_deliverables / required_deliverables) * 100
   ```

5. **Report results**:
   - If completeness >= 90%: Success, ready to use
   - If completeness 70-89%: Warning, some optional features missing
   - If completeness < 70%: Failure, critical features missing

6. **Offer remediation** if completeness < 90%:
   ```
   Missing deliverables detected:
   - Grafana dashboards: monitoring/grafana/dashboards/ is empty
   - Feature store: src/features/feature_store.py missing

   Would you like me to:
   a) Generate missing components now
   b) Continue with current implementation
   c) See detailed gap report
   ```

### Integration with Skills

Skills receive expectations context to know what to generate:

```python
expectations_context = {
    "blueprint": "ml-pipeline",
    "maturity": "starter",
    "required_deliverables": [
        "MLflow experiment tracking",
        "Model serving API",
        "Sample data generation script",
        "Quick start notebook",
        "Feature engineering code"
    ],
    "skipped_deliverables": [
        "Feature store (Feast)",
        "Kubernetes deployment manifests",
        "Grafana dashboards"
    ]
}
```

This ensures skills know exactly what's expected and can validate their own outputs before completing.

---

**Blueprint Complete**
