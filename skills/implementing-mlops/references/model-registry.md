# Model Registry

Centralized repository for managing model artifacts, versions, and metadata throughout the ML lifecycle.

## Table of Contents

- [Overview](#overview)
- [Model Registry Components](#model-registry-components)
- [Stage Management](#stage-management)
- [Versioning Strategies](#versioning-strategies)
- [Model Lineage](#model-lineage)
- [Platform Comparison](#platform-comparison)
- [Implementation Examples](#implementation-examples)

## Overview

Model registries provide centralized storage and versioning for ML models, enabling teams to track experiments, manage deployments, and maintain model lineage.

### Key Benefits

- **Version Control**: Track all model versions with metadata
- **Stage Management**: Transition models through development stages (None → Staging → Production)
- **Metadata Storage**: Store training metrics, hyperparameters, feature schemas
- **Lineage Tracking**: Understand model dependencies (data, code, parent models)
- **Collaboration**: Share models across teams
- **Governance**: Audit trail for compliance

## Model Registry Components

### 1. Model Artifacts

Binary files storing trained model weights.

```python
# Save model artifacts
import mlflow
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier()
model.fit(X_train, y_train)

# Log model
mlflow.sklearn.log_model(
    model,
    artifact_path="model",
    registered_model_name="fraud_detection"
)
```

### 2. Model Metadata

Descriptive information about the model.

```python
# Log metadata
mlflow.log_params({
    'n_estimators': 100,
    'max_depth': 10,
    'min_samples_split': 5
})

mlflow.log_metrics({
    'accuracy': 0.92,
    'precision': 0.89,
    'recall': 0.85,
    'f1_score': 0.87
})

mlflow.set_tags({
    'model_type': 'RandomForest',
    'use_case': 'fraud_detection',
    'team': 'risk_analytics',
    'data_version': 'v2023-06'
})
```

### 3. Training Artifacts

Additional files from training process.

```python
# Log artifacts
mlflow.log_artifact('feature_importance.png')
mlflow.log_artifact('confusion_matrix.png')
mlflow.log_artifact('training_config.yaml')
mlflow.log_artifact('feature_schema.json')
```

### 4. Model Signature

Input/output schema for model.

```python
# Define signature
from mlflow.models.signature import infer_signature

signature = infer_signature(X_train, model.predict(X_train))

# Log with signature
mlflow.sklearn.log_model(
    model,
    "model",
    signature=signature
)

# Signature example:
# inputs: [{"name": "feature_1", "type": "double"}, {"name": "feature_2", "type": "long"}]
# outputs: [{"type": "long"}]
```

## Stage Management

Models transition through stages: None → Staging → Production → Archived.

### Stage Definitions

**None**:
- Newly registered model
- Not yet tested
- Not deployed

**Staging**:
- Deployed to staging environment
- Under testing and validation
- Not serving production traffic

**Production**:
- Serving live production traffic
- Actively monitored
- Primary model version

**Archived**:
- Deprecated, no longer used
- Retained for compliance/audit
- Can be restored if needed

### Stage Transitions

```python
# mlflow_stage_management.py
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Promote to Staging
client.transition_model_version_stage(
    name="fraud_detection",
    version=5,
    stage="Staging"
)

# Promote to Production (archives current production version)
client.transition_model_version_stage(
    name="fraud_detection",
    version=5,
    stage="Production",
    archive_existing_versions=True
)

# Archive old version
client.transition_model_version_stage(
    name="fraud_detection",
    version=3,
    stage="Archived"
)
```

### Loading Models by Stage

```python
# Load latest production model
import mlflow.pyfunc

model = mlflow.pyfunc.load_model("models:/fraud_detection/Production")

# Load specific version
model = mlflow.pyfunc.load_model("models:/fraud_detection/5")

# Load staging model
model = mlflow.pyfunc.load_model("models:/fraud_detection/Staging")
```

## Versioning Strategies

### Semantic Versioning for Models

Adapt semantic versioning (MAJOR.MINOR.PATCH) for ML models.

```
MAJOR: Breaking change in input/output schema
MINOR: New feature, backward-compatible (e.g., new feature added)
PATCH: Bug fix, model retrained on new data (same architecture)
```

**Examples:**
- `v1.0.0` → `v2.0.0`: Change feature schema (breaking)
- `v1.0.0` → `v1.1.0`: Add new feature (compatible)
- `v1.0.0` → `v1.0.1`: Retrain on fresh data (same schema)

```python
# semantic_versioning.py
def register_model_with_semver(model, current_version, change_type):
    """
    Register model with semantic versioning.

    Args:
        model: Trained model
        current_version: Current version (e.g., "1.0.0")
        change_type: "major", "minor", or "patch"
    """
    major, minor, patch = map(int, current_version.split('.'))

    if change_type == 'major':
        new_version = f"{major + 1}.0.0"
    elif change_type == 'minor':
        new_version = f"{major}.{minor + 1}.0"
    elif change_type == 'patch':
        new_version = f"{major}.{minor}.{patch + 1}"

    mlflow.sklearn.log_model(
        model,
        "model",
        registered_model_name="fraud_detection"
    )

    # Tag with semantic version
    client = MlflowClient()
    versions = client.search_model_versions(f"name='fraud_detection'")
    latest_version = versions[0].version

    client.set_model_version_tag(
        name="fraud_detection",
        version=latest_version,
        key="semver",
        value=new_version
    )

    print(f"Model registered as v{new_version}")

# Usage
register_model_with_semver(model, current_version="1.0.0", change_type="minor")
# Output: Model registered as v1.1.0
```

### Git-Based Versioning

Link model to Git commit for reproducibility.

```python
# git_versioning.py
import git
import mlflow

def log_model_with_git_info(model):
    """Log model with Git commit info."""

    repo = git.Repo(search_parent_directories=True)

    # Git info
    git_commit = repo.head.object.hexsha
    git_branch = repo.active_branch.name
    is_dirty = repo.is_dirty()

    if is_dirty:
        print("⚠️  Warning: Git repository has uncommitted changes")

    # Log model with Git metadata
    with mlflow.start_run():
        mlflow.sklearn.log_model(model, "model")

        mlflow.set_tags({
            'git_commit': git_commit,
            'git_branch': git_branch,
            'git_dirty': str(is_dirty)
        })

        # Log code snapshot
        mlflow.log_artifact('.', artifact_path='code_snapshot')

    print(f"Model logged with commit {git_commit[:7]}")
```

## Model Lineage

Track relationships between models, data, and code.

### Lineage Components

```
Training Data (v2023-06)
    |
Feature Engineering Code (commit abc123)
    |
Training Script (commit def456)
    |
Parent Model (v1.0.0)
    |
Fine-Tuned Model (v1.1.0)
    |
Deployed to Production
```

### Tracking Lineage in MLflow

```python
# lineage_tracking.py
import mlflow

def train_with_lineage(parent_model_uri, training_data_version):
    """Train model with full lineage tracking."""

    with mlflow.start_run(run_name="fraud_detection_v1.1"):

        # Log parent model
        mlflow.set_tag("parent_model", parent_model_uri)

        # Log data lineage
        mlflow.set_tag("training_data_version", training_data_version)
        mlflow.set_tag("training_data_path", "s3://ml-data/train_v2023-06.parquet")

        # Log code lineage
        mlflow.set_tag("git_commit", get_git_commit())

        # Log feature store version
        mlflow.set_tag("feature_store_commit", "feature-store-v1.2")

        # Train model
        model = train_model()

        # Log model
        mlflow.sklearn.log_model(
            model,
            "model",
            registered_model_name="fraud_detection"
        )

# Usage
train_with_lineage(
    parent_model_uri="models:/fraud_detection/3",
    training_data_version="v2023-06"
)
```

### Querying Lineage

```python
# query_lineage.py
from mlflow.tracking import MlflowClient

def get_model_lineage(model_name, version):
    """Get complete lineage for model version."""

    client = MlflowClient()

    # Get model version
    model_version = client.get_model_version(model_name, version)

    # Get run info
    run = client.get_run(model_version.run_id)

    # Extract lineage
    lineage = {
        'model': f"{model_name} v{version}",
        'training_date': run.info.start_time,
        'git_commit': run.data.tags.get('git_commit'),
        'training_data': run.data.tags.get('training_data_path'),
        'data_version': run.data.tags.get('training_data_version'),
        'parent_model': run.data.tags.get('parent_model'),
        'feature_store_version': run.data.tags.get('feature_store_commit'),
        'metrics': run.data.metrics
    }

    return lineage

# Usage
lineage = get_model_lineage("fraud_detection", version=5)
print(lineage)
```

## Platform Comparison

### MLflow Model Registry

**Open-source, self-hosted.**

```python
# MLflow setup
import mlflow

mlflow.set_tracking_uri("http://mlflow.example.com")

# Register model
mlflow.sklearn.log_model(
    model,
    "model",
    registered_model_name="fraud_detection"
)

# Manage stages
client = MlflowClient()
client.transition_model_version_stage(
    name="fraud_detection",
    version=5,
    stage="Production"
)
```

**Advantages:**
- Open-source, free
- Framework-agnostic
- Self-hosted or cloud-agnostic
- Strong community

**Disadvantages:**
- Basic UI
- No built-in approval workflows
- Manual infrastructure management

### Vertex AI Model Registry (GCP)

**Google Cloud managed registry.**

```python
# Vertex AI setup
from google.cloud import aiplatform

aiplatform.init(project="my-project", location="us-central1")

# Upload model
model = aiplatform.Model.upload(
    display_name="fraud_detection",
    artifact_uri="gs://my-bucket/model",
    serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.1-0:latest"
)

# Deploy
endpoint = model.deploy(
    deployed_model_display_name="fraud_detection_v1",
    machine_type="n1-standard-4"
)
```

**Advantages:**
- Fully managed
- Integrated with GCP
- Auto-scaling
- Built-in monitoring

**Disadvantages:**
- GCP lock-in
- Higher cost than self-hosted

### SageMaker Model Registry (AWS)

**AWS managed registry.**

```python
# SageMaker Model Registry
import sagemaker
from sagemaker.model import Model

model = Model(
    image_uri="sagemaker-sklearn",
    model_data="s3://my-bucket/model.tar.gz",
    role=sagemaker_role
)

# Register
model_package = model.register(
    content_types=["application/json"],
    response_types=["application/json"],
    inference_instances=["ml.m5.large"],
    model_package_group_name="fraud-detection-models"
)

# Approve for production
sm_client.update_model_package(
    ModelPackageArn=model_package.model_package_arn,
    ModelApprovalStatus="Approved"
)
```

**Advantages:**
- Integrated with AWS SageMaker
- Built-in approval workflows
- Model lineage tracking

**Disadvantages:**
- AWS lock-in

### Azure ML Model Registry

**Azure managed registry.**

```python
# Azure ML Model Registry
from azureml.core import Workspace, Model

ws = Workspace.from_config()

# Register model
model = Model.register(
    workspace=ws,
    model_name="fraud_detection",
    model_path="outputs/model.pkl",
    tags={"accuracy": "0.92", "framework": "sklearn"}
)

# Download model
model.download(target_dir="./downloaded_model")
```

**Advantages:**
- Integrated with Azure ML
- Enterprise features

**Disadvantages:**
- Azure lock-in

## Implementation Examples

### Example 1: Complete Model Registration Pipeline

```python
# complete_registration.py
import mlflow
from mlflow.tracking import MlflowClient
import git

def register_model_complete(
    model,
    model_name,
    X_train,
    y_train,
    X_test,
    y_test,
    hyperparameters
):
    """Complete model registration with metadata, lineage, and validation."""

    client = MlflowClient()

    with mlflow.start_run(run_name=f"{model_name}_training"):

        # 1. Log hyperparameters
        mlflow.log_params(hyperparameters)

        # 2. Evaluate and log metrics
        from sklearn.metrics import accuracy_score, precision_score, recall_score

        y_pred = model.predict(X_test)
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred)
        }
        mlflow.log_metrics(metrics)

        # 3. Log Git info
        repo = git.Repo(search_parent_directories=True)
        mlflow.set_tag('git_commit', repo.head.object.hexsha)

        # 4. Log data lineage
        mlflow.set_tag('training_data_path', 's3://ml-data/train.parquet')
        mlflow.set_tag('training_samples', len(X_train))

        # 5. Log model signature
        from mlflow.models.signature import infer_signature
        signature = infer_signature(X_train, model.predict(X_train))

        # 6. Log model
        model_info = mlflow.sklearn.log_model(
            model,
            "model",
            signature=signature,
            registered_model_name=model_name
        )

        # 7. Add model description
        versions = client.search_model_versions(f"name='{model_name}'")
        latest_version = versions[0].version

        client.update_model_version(
            name=model_name,
            version=latest_version,
            description=f"Trained on {len(X_train)} samples. Accuracy: {metrics['accuracy']:.3f}"
        )

        # 8. Tag version
        client.set_model_version_tag(
            name=model_name,
            version=latest_version,
            key="validated",
            value="true"
        )

        print(f"Model registered: {model_name} v{latest_version}")
        print(f"Metrics: {metrics}")

        return latest_version

# Usage
version = register_model_complete(
    model=trained_model,
    model_name="fraud_detection",
    X_train=X_train,
    y_train=y_train,
    X_test=X_test,
    y_test=y_test,
    hyperparameters={'n_estimators': 100, 'max_depth': 10}
)
```

### Example 2: Model Comparison

```python
# model_comparison.py
from mlflow.tracking import MlflowClient
import pandas as pd

def compare_model_versions(model_name):
    """Compare all versions of a model."""

    client = MlflowClient()

    # Get all versions
    versions = client.search_model_versions(f"name='{model_name}'")

    comparison = []
    for version in versions:
        run = client.get_run(version.run_id)

        comparison.append({
            'version': version.version,
            'stage': version.current_stage,
            'accuracy': run.data.metrics.get('accuracy'),
            'precision': run.data.metrics.get('precision'),
            'recall': run.data.metrics.get('recall'),
            'created_at': version.creation_timestamp,
            'description': version.description
        })

    # Convert to DataFrame
    df = pd.DataFrame(comparison)
    df = df.sort_values('version', ascending=False)

    return df

# Usage
comparison = compare_model_versions("fraud_detection")
print(comparison)

#    version      stage  accuracy  precision  recall      created_at
# 0        5 Production     0.920      0.890   0.850  1686182400000
# 1        4    Staging     0.915      0.880   0.840  1686096000000
# 2        3   Archived     0.905      0.870   0.830  1686009600000
```

### Example 3: A/B Testing with Model Registry

```python
# ab_testing_registry.py
import random
import mlflow

class ModelABTest:
    """A/B test between two model versions."""

    def __init__(self, model_name, variant_a_version, variant_b_version, split=0.5):
        """
        Args:
            model_name: Name of model in registry
            variant_a_version: Version for variant A (e.g., "4")
            variant_b_version: Version for variant B (e.g., "5")
            split: Traffic split (0.5 = 50/50)
        """
        self.model_name = model_name
        self.variant_a = mlflow.pyfunc.load_model(f"models:/{model_name}/{variant_a_version}")
        self.variant_b = mlflow.pyfunc.load_model(f"models:/{model_name}/{variant_b_version}")
        self.split = split

        self.metrics_a = {'predictions': 0, 'correct': 0}
        self.metrics_b = {'predictions': 0, 'correct': 0}

    def predict(self, X, user_id):
        """Predict with A/B test."""

        # Assign variant based on user_id (consistent)
        if hash(user_id) % 100 < self.split * 100:
            variant = 'A'
            prediction = self.variant_a.predict(X)
            self.metrics_a['predictions'] += 1
        else:
            variant = 'B'
            prediction = self.variant_b.predict(X)
            self.metrics_b['predictions'] += 1

        return prediction, variant

    def record_outcome(self, variant, correct):
        """Record prediction outcome."""
        if variant == 'A':
            self.metrics_a['correct'] += int(correct)
        else:
            self.metrics_b['correct'] += int(correct)

    def get_results(self):
        """Get A/B test results."""
        accuracy_a = self.metrics_a['correct'] / self.metrics_a['predictions'] if self.metrics_a['predictions'] > 0 else 0
        accuracy_b = self.metrics_b['correct'] / self.metrics_b['predictions'] if self.metrics_b['predictions'] > 0 else 0

        return {
            'variant_a': {
                'predictions': self.metrics_a['predictions'],
                'accuracy': accuracy_a
            },
            'variant_b': {
                'predictions': self.metrics_b['predictions'],
                'accuracy': accuracy_b
            },
            'winner': 'A' if accuracy_a > accuracy_b else 'B'
        }

# Usage
ab_test = ModelABTest(
    model_name="fraud_detection",
    variant_a_version="4",
    variant_b_version="5",
    split=0.5
)

# Predict
prediction, variant = ab_test.predict(X_test[0:1], user_id="user_12345")

# Record outcome (after ground truth available)
ab_test.record_outcome(variant, correct=True)

# Get results after sufficient data
results = ab_test.get_results()
print(results)
```
