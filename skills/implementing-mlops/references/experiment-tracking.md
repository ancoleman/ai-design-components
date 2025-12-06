# Experiment Tracking

Comprehensive guide to tracking machine learning experiments for reproducibility and collaboration.

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [MLflow](#mlflow)
3. [Weights & Biases](#weights--biases)
4. [Neptune.ai](#neptuneai)
5. [TensorBoard](#tensorboard)
6. [Best Practices](#best-practices)
7. [Common Patterns](#common-patterns)

---

## Core Concepts

### What to Track

**Parameters (Hyperparameters):**
- Model architecture config (layers, units, activation functions)
- Learning rate, batch size, epochs
- Regularization (dropout, L1/L2)
- Optimizer settings (momentum, beta values)
- Data preprocessing parameters

**Metrics:**
- Training metrics (loss, accuracy per epoch)
- Validation metrics (val_loss, val_accuracy)
- Test metrics (final accuracy, F1, precision, recall, AUC)
- Custom business metrics (conversion rate impact)

**Artifacts:**
- Model weights (checkpoints, final model)
- Training/validation plots (loss curves, confusion matrices)
- Datasets (training data version, test data samples)
- Configuration files (YAML, JSON)
- Code snapshots (Git commit SHA)

**Metadata:**
- Experiment name and description
- Tags (model_type: "cnn", dataset: "imagenet")
- Git commit SHA and branch
- Environment info (Python version, library versions)
- Hardware used (GPU type, memory)
- Runtime (training duration)

### Reproducibility Requirements

**Deterministic Training:**
- Set random seeds (Python, NumPy, PyTorch, TensorFlow)
- Disable non-deterministic operations (CuDNN benchmarking)
- Log all random state initialization

**Environment Capture:**
- Log library versions (requirements.txt, conda environment)
- Log system info (OS, CPU, GPU)
- Container images (Docker SHA)

**Data Versioning:**
- Track dataset version (DVC hash, Git-LFS commit)
- Log data preprocessing steps
- Store data validation results

---

## MLflow

### Architecture

**Components:**
- **Tracking Server:** REST API for logging experiments
- **Backend Store:** Database (PostgreSQL, MySQL, SQLite) for metadata
- **Artifact Store:** Object storage (S3, GCS, Azure Blob) for large files
- **Model Registry:** Centralized model repository

**Setup:**
```bash
# Install MLflow
pip install mlflow

# Start local tracking server
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./mlruns \
  --host 0.0.0.0 \
  --port 5000

# Production setup (PostgreSQL + S3)
mlflow server \
  --backend-store-uri postgresql://user:password@localhost/mlflow \
  --default-artifact-root s3://my-mlflow-bucket/artifacts \
  --host 0.0.0.0 \
  --port 5000
```

### Logging Experiments

**Basic Logging:**
```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier

# Set tracking URI
mlflow.set_tracking_uri("http://localhost:5000")

# Set experiment
mlflow.set_experiment("customer-churn-prediction")

# Start run
with mlflow.start_run(run_name="rf-baseline"):
    # Log parameters
    n_estimators = 100
    max_depth = 10
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)
    mlflow.log_param("data_version", "v1.2.3")

    # Train model
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )
    model.fit(X_train, y_train)

    # Log metrics
    train_acc = model.score(X_train, y_train)
    test_acc = model.score(X_test, y_test)
    mlflow.log_metric("train_accuracy", train_acc)
    mlflow.log_metric("test_accuracy", test_acc)

    # Log model with signature
    from mlflow.models.signature import infer_signature
    signature = infer_signature(X_train, model.predict(X_train))
    mlflow.sklearn.log_model(
        model,
        "model",
        signature=signature,
        input_example=X_train.iloc[:5]
    )

    # Log artifacts
    import matplotlib.pyplot as plt
    from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

    cm = confusion_matrix(y_test, model.predict(X_test))
    disp = ConfusionMatrixDisplay(cm)
    disp.plot()
    plt.savefig("confusion_matrix.png")
    mlflow.log_artifact("confusion_matrix.png")
```

**Autologging (Automatic Tracking):**
```python
import mlflow
import mlflow.sklearn

# Enable autologging
mlflow.sklearn.autolog()

# Training automatically logged
with mlflow.start_run():
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    # Parameters, metrics, model automatically logged
```

**Nested Runs (Hyperparameter Tuning):**
```python
from sklearn.model_selection import GridSearchCV

# Parent run for hyperparameter search
with mlflow.start_run(run_name="rf-grid-search"):
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [5, 10, 20]
    }

    grid_search = GridSearchCV(
        RandomForestClassifier(),
        param_grid,
        cv=5,
        scoring='accuracy'
    )

    grid_search.fit(X_train, y_train)

    # Log each combination as nested run
    for params, mean_score in zip(grid_search.cv_results_['params'],
                                    grid_search.cv_results_['mean_test_score']):
        with mlflow.start_run(nested=True):
            mlflow.log_params(params)
            mlflow.log_metric("cv_accuracy", mean_score)

    # Log best model
    mlflow.sklearn.log_model(grid_search.best_estimator_, "best_model")
    mlflow.log_params(grid_search.best_params_)
    mlflow.log_metric("best_cv_accuracy", grid_search.best_score_)
```

### Model Registry

**Register Model:**
```python
# Option 1: During run
with mlflow.start_run():
    mlflow.sklearn.log_model(
        model,
        "model",
        registered_model_name="customer-churn"
    )

# Option 2: Register existing run
model_uri = f"runs:/{run_id}/model"
result = mlflow.register_model(model_uri, "customer-churn")
print(f"Model version: {result.version}")
```

**Manage Model Versions:**
```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Transition to staging
client.transition_model_version_stage(
    name="customer-churn",
    version=3,
    stage="Staging"
)

# Transition to production
client.transition_model_version_stage(
    name="customer-churn",
    version=3,
    stage="Production"
)

# Archive old version
client.transition_model_version_stage(
    name="customer-churn",
    version=2,
    stage="Archived"
)

# Add description and tags
client.update_model_version(
    name="customer-churn",
    version=3,
    description="RandomForest model, 87% accuracy, v1.2.3 data"
)
client.set_model_version_tag(
    name="customer-churn",
    version=3,
    key="task",
    value="binary_classification"
)
```

**Load Model from Registry:**
```python
import mlflow.pyfunc

# Load production model
model = mlflow.pyfunc.load_model("models:/customer-churn/production")
predictions = model.predict(X_new)

# Load specific version
model_v3 = mlflow.pyfunc.load_model("models:/customer-churn/3")
```

---

## Weights & Biases

### Setup

```bash
# Install wandb
pip install wandb

# Login (API key from wandb.ai)
wandb login
```

### Logging Experiments

**Basic Logging:**
```python
import wandb
from sklearn.ensemble import RandomForestClassifier

# Initialize run
wandb.init(
    project="customer-churn",
    name="rf-baseline",
    config={
        "n_estimators": 100,
        "max_depth": 10,
        "dataset": "v1.2.3"
    }
)

# Train model
model = RandomForestClassifier(
    n_estimators=wandb.config.n_estimators,
    max_depth=wandb.config.max_depth
)
model.fit(X_train, y_train)

# Log metrics
wandb.log({
    "train_accuracy": model.score(X_train, y_train),
    "test_accuracy": model.score(X_test, y_test)
})

# Log confusion matrix
from wandb.sklearn import plot_confusion_matrix
plot_confusion_matrix(y_test, model.predict(X_test), labels=["0", "1"])

# Save model
wandb.save("model.pkl")

# Finish run
wandb.finish()
```

**Deep Learning (PyTorch):**
```python
import torch
import wandb

# Initialize run
wandb.init(project="image-classification", name="resnet50")

# Log model architecture
wandb.watch(model, log="all", log_freq=100)

# Training loop
for epoch in range(num_epochs):
    for batch_idx, (data, target) in enumerate(train_loader):
        # Forward pass
        output = model(data)
        loss = criterion(output, target)

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Log metrics
        wandb.log({
            "epoch": epoch,
            "batch": batch_idx,
            "loss": loss.item(),
            "learning_rate": optimizer.param_groups[0]['lr']
        })

    # Validation
    val_acc = evaluate(model, val_loader)
    wandb.log({"epoch": epoch, "val_accuracy": val_acc})
```

### Hyperparameter Sweeps

**Define Sweep:**
```python
# sweep_config.yaml
sweep_config = {
    'method': 'bayes',  # or 'grid', 'random'
    'metric': {
        'name': 'val_accuracy',
        'goal': 'maximize'
    },
    'parameters': {
        'learning_rate': {
            'distribution': 'log_uniform_values',
            'min': 1e-5,
            'max': 1e-1
        },
        'batch_size': {
            'values': [16, 32, 64, 128]
        },
        'optimizer': {
            'values': ['adam', 'sgd', 'adamw']
        }
    }
}

# Initialize sweep
sweep_id = wandb.sweep(sweep_config, project="image-classification")

# Run sweep
def train():
    wandb.init()
    config = wandb.config

    model = build_model(config)
    train_model(model, config)

    wandb.log({"val_accuracy": val_acc})

wandb.agent(sweep_id, function=train, count=50)  # 50 trials
```

### Artifacts

**Log Artifacts:**
```python
import wandb

wandb.init(project="customer-churn")

# Log dataset
artifact = wandb.Artifact("customer-data", type="dataset")
artifact.add_file("train.csv")
artifact.add_file("test.csv")
wandb.log_artifact(artifact)

# Log model
model_artifact = wandb.Artifact("churn-model", type="model")
model_artifact.add_file("model.pkl")
wandb.log_artifact(model_artifact)
```

**Use Artifacts:**
```python
# Download dataset
artifact = wandb.use_artifact("customer-data:latest")
artifact_dir = artifact.download()

# Download model
model_artifact = wandb.use_artifact("churn-model:v3")
model_path = model_artifact.download()
```

---

## Neptune.ai

### Setup

```bash
# Install neptune
pip install neptune-client

# Get API token from app.neptune.ai
```

### Logging Experiments

**Basic Logging:**
```python
import neptune.new as neptune
from sklearn.ensemble import RandomForestClassifier

# Initialize run
run = neptune.init_run(
    project="workspace/customer-churn",
    api_token="YOUR_API_TOKEN",
    name="rf-baseline",
    tags=["baseline", "random-forest"]
)

# Log parameters
run["parameters"] = {
    "n_estimators": 100,
    "max_depth": 10,
    "dataset_version": "v1.2.3"
}

# Train model
model = RandomForestClassifier(n_estimators=100, max_depth=10)
model.fit(X_train, y_train)

# Log metrics
run["metrics/train_accuracy"] = model.score(X_train, y_train)
run["metrics/test_accuracy"] = model.score(X_test, y_test)

# Log artifacts
run["artifacts/confusion_matrix"].upload("confusion_matrix.png")
run["artifacts/model"].upload("model.pkl")

# Stop run
run.stop()
```

**Model Registry:**
```python
import neptune.new as neptune

# Initialize model
model = neptune.init_model(
    project="workspace/customer-churn",
    name="churn-predictor",
    key="CHURN"
)

# Create model version
model_version = neptune.init_model_version(
    model="CHURN",
    name="rf-v1"
)

# Log model metadata
model_version["model/parameters"] = {"n_estimators": 100}
model_version["model/accuracy"] = 0.87
model_version["model/artifact"].upload("model.pkl")

# Change stage
model_version.change_stage("staging")
```

---

## TensorBoard

### Setup

```bash
# Install TensorBoard
pip install tensorboard

# Start TensorBoard
tensorboard --logdir=./logs
```

### Logging with TensorFlow

```python
import tensorflow as tf

# Create TensorBoard callback
tensorboard_callback = tf.keras.callbacks.TensorBoard(
    log_dir="./logs",
    histogram_freq=1,  # Log weight histograms every epoch
    write_graph=True,
    update_freq='epoch'
)

# Train model
model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=10,
    callbacks=[tensorboard_callback]
)
```

### Logging with PyTorch

```python
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter('runs/experiment_1')

# Log scalars
for epoch in range(num_epochs):
    loss = train_one_epoch(model, train_loader)
    writer.add_scalar('Loss/train', loss, epoch)

    val_loss = validate(model, val_loader)
    writer.add_scalar('Loss/val', val_loss, epoch)

# Log model graph
writer.add_graph(model, sample_input)

# Log images
writer.add_images('predictions', images, epoch)

writer.close()
```

---

## Best Practices

### Experiment Organization

**Naming Conventions:**
- Experiment: `{project}-{model_type}` (e.g., "customer-churn-randomforest")
- Run: `{model}-{version}-{date}` (e.g., "rf-v1-20250104")
- Tags: `["baseline", "production", "experiment"]`

**Parameter Naming:**
- Use consistent names across experiments
- Prefix related params: `"model/n_estimators"`, `"data/train_size"`
- Avoid abbreviations: `"learning_rate"` not `"lr"`

**Metric Naming:**
- Prefix by stage: `"train/accuracy"`, `"val/accuracy"`, `"test/accuracy"`
- Use standard names: `"f1_score"` not `"f1"`
- Log per-class metrics: `"accuracy/class_0"`, `"accuracy/class_1"`

### Reproducibility Checklist

- [ ] Set random seeds (Python, NumPy, framework)
- [ ] Log Git commit SHA
- [ ] Log library versions (requirements.txt)
- [ ] Log dataset version (DVC hash)
- [ ] Log hardware used (GPU type)
- [ ] Log environment variables
- [ ] Save model architecture (config.json)
- [ ] Save preprocessing steps
- [ ] Log data validation results

### Performance Optimization

**Reduce Logging Overhead:**
- Log metrics every N steps, not every step
- Batch metric logging (log_metrics vs log_metric)
- Disable autologging if too slow
- Use asynchronous logging when available

**Storage Optimization:**
- Compress large artifacts before logging
- Delete old artifacts after archiving
- Use artifact versioning (don't duplicate)
- Set artifact retention policies

---

## Common Patterns

### Pattern 1: Multi-Stage Training

Track different training stages (pretraining, fine-tuning).

```python
import mlflow

# Pretraining
with mlflow.start_run(run_name="pretraining") as parent_run:
    mlflow.log_param("stage", "pretrain")
    pretrain_model = pretrain(base_model, pretrain_data)
    mlflow.log_metric("pretrain_loss", pretrain_loss)

    # Fine-tuning (nested)
    with mlflow.start_run(run_name="fine-tuning", nested=True):
        mlflow.log_param("stage", "finetune")
        final_model = finetune(pretrain_model, finetune_data)
        mlflow.log_metric("finetune_accuracy", accuracy)
        mlflow.sklearn.log_model(final_model, "model")
```

### Pattern 2: Experiment Comparison

Compare multiple experiments systematically.

```python
import mlflow

experiments = [
    {"name": "rf-50-trees", "n_estimators": 50},
    {"name": "rf-100-trees", "n_estimators": 100},
    {"name": "rf-200-trees", "n_estimators": 200}
]

for exp in experiments:
    with mlflow.start_run(run_name=exp["name"]):
        mlflow.log_param("n_estimators", exp["n_estimators"])
        model = RandomForestClassifier(n_estimators=exp["n_estimators"])
        model.fit(X_train, y_train)
        mlflow.log_metric("accuracy", model.score(X_test, y_test))
```

### Pattern 3: Cross-Validation Tracking

Track each fold in cross-validation.

```python
from sklearn.model_selection import cross_val_score

with mlflow.start_run(run_name="rf-cv"):
    scores = []
    for fold in range(5):
        with mlflow.start_run(nested=True, run_name=f"fold-{fold}"):
            # Train on fold
            score = train_on_fold(fold)
            mlflow.log_metric("accuracy", score)
            scores.append(score)

    # Log aggregate metrics
    mlflow.log_metric("mean_accuracy", np.mean(scores))
    mlflow.log_metric("std_accuracy", np.std(scores))
```

### Pattern 4: Failed Experiment Handling

Track failures for debugging.

```python
import mlflow

with mlflow.start_run(run_name="experiment-1"):
    try:
        # Training logic
        model.fit(X_train, y_train)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.set_tag("status", "success")
    except Exception as e:
        mlflow.set_tag("status", "failed")
        mlflow.set_tag("error", str(e))
        mlflow.log_param("traceback", traceback.format_exc())
        raise
```
