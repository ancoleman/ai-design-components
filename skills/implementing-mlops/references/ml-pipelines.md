# ML Pipeline Orchestration

Automate training, evaluation, and deployment workflows for machine learning systems.

## Table of Contents

- [Overview](#overview)
- [Pipeline Stages](#pipeline-stages)
- [Platform Comparison](#platform-comparison)
- [Continuous Training](#continuous-training)
- [DAG Design Best Practices](#dag-design-best-practices)
- [Implementation Examples](#implementation-examples)

## Overview

ML pipelines orchestrate the complete model lifecycle from data ingestion to deployment, ensuring reproducibility and automation.

### Training Pipeline Architecture

```
Data Sources
    |
Data Validation (Great Expectations)
    |
Feature Engineering (transform raw data)
    |
Data Splitting (train/validation/test)
    |
Model Training (hyperparameter tuning)
    |
Model Evaluation (accuracy, fairness, explainability)
    |
Model Registration (push to registry if metrics pass)
    |
Deployment (promote to staging/production)
```

## Pipeline Stages

### Stage 1: Data Validation

Validate data quality before training.

```python
# data_validation.py
import great_expectations as ge

def validate_training_data(data_path: str):
    """Validate training data schema and quality."""

    # Load data as GE DataFrame
    df = ge.read_csv(data_path)

    # Schema validation
    df.expect_table_columns_to_match_ordered_list([
        'user_id', 'timestamp', 'feature_1', 'feature_2', 'label'
    ])

    # Data quality checks
    df.expect_column_values_to_not_be_null('user_id')
    df.expect_column_values_to_be_between('feature_1', min_value=0, max_value=100)
    df.expect_column_values_to_be_in_set('label', [0, 1])

    # Get validation results
    results = df.validate()

    if not results['success']:
        raise ValueError(f"Data validation failed: {results['results']}")

    print("✓ Data validation passed")
    return True
```

### Stage 2: Feature Engineering

Transform raw data into features.

```python
# feature_engineering.py
from sklearn.preprocessing import StandardScaler
import pandas as pd

def engineer_features(df: pd.DataFrame):
    """Feature engineering pipeline."""

    # Derived features
    df['days_since_signup'] = (pd.to_datetime('today') - pd.to_datetime(df['signup_date'])).dt.days
    df['purchase_frequency'] = df['total_purchases'] / df['days_since_signup']

    # Categorical encoding
    df = pd.get_dummies(df, columns=['category'], prefix='cat')

    # Scaling
    scaler = StandardScaler()
    numeric_cols = ['feature_1', 'feature_2', 'purchase_frequency']
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    return df, scaler
```

### Stage 3: Model Training

Train model with hyperparameter tuning.

```python
# training.py
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

def train_model(X_train, y_train):
    """Train model with hyperparameter tuning."""

    # Hyperparameter grid
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 20, 30],
        'min_samples_split': [2, 5, 10]
    }

    # Grid search
    model = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(
        model,
        param_grid,
        cv=5,
        scoring='f1',
        n_jobs=-1
    )

    grid_search.fit(X_train, y_train)

    print(f"Best parameters: {grid_search.best_params_}")
    print(f"Best F1 score: {grid_search.best_score_:.3f}")

    return grid_search.best_estimator_
```

### Stage 4: Model Evaluation

Evaluate model performance and fairness.

```python
# evaluation.py
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def evaluate_model(model, X_test, y_test, thresholds: dict):
    """Evaluate model against thresholds."""

    # Predictions
    y_pred = model.predict(X_test)

    # Metrics
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1': f1_score(y_test, y_pred)
    }

    # Check thresholds
    passed = True
    for metric, value in metrics.items():
        threshold = thresholds.get(metric, 0)
        if value < threshold:
            print(f"✗ {metric}: {value:.3f} < {threshold} (FAILED)")
            passed = False
        else:
            print(f"✓ {metric}: {value:.3f} >= {threshold}")

    return metrics, passed
```

### Stage 5: Model Registration

Register model if evaluation passes.

```python
# registration.py
import mlflow

def register_model(model, metrics, passed: bool):
    """Register model to MLflow registry."""

    if not passed:
        print("Model evaluation failed, skipping registration")
        return None

    # Log model
    with mlflow.start_run():
        mlflow.log_metrics(metrics)
        mlflow.sklearn.log_model(
            model,
            "model",
            registered_model_name="fraud_detection"
        )

        run_id = mlflow.active_run().info.run_id
        print(f"Model registered: run_id={run_id}")

    return run_id
```

## Platform Comparison

### Kubeflow Pipelines

**ML-native orchestration for Kubernetes.**

```python
# kubeflow_pipeline.py
import kfp
from kfp import dsl

@dsl.component
def validate_data(data_path: str) -> bool:
    """Data validation component."""
    # Validation logic
    return True

@dsl.component
def train_model(data_path: str, model_path: dsl.Output[dsl.Model]):
    """Training component."""
    # Training logic
    pass

@dsl.component
def evaluate_model(model_path: dsl.Input[dsl.Model]) -> dict:
    """Evaluation component."""
    # Evaluation logic
    return {'accuracy': 0.95}

@dsl.pipeline(name='fraud-detection-training')
def training_pipeline(data_path: str):
    """Complete training pipeline."""

    # Data validation
    validate_task = validate_data(data_path=data_path)

    # Train model (depends on validation)
    train_task = train_model(data_path=data_path).after(validate_task)

    # Evaluate model
    evaluate_task = evaluate_model(model_path=train_task.outputs['model_path'])

# Compile and run
kfp.compiler.Compiler().compile(training_pipeline, 'pipeline.yaml')

client = kfp.Client()
client.create_run_from_pipeline_func(
    training_pipeline,
    arguments={'data_path': 's3://ml-data/train.parquet'}
)
```

**Advantages:**
- ML-specific (GPU scheduling, distributed training)
- Component reusability
- Kubernetes-native scaling
- Integrated with Katib (hyperparameter tuning)

**Disadvantages:**
- Steep learning curve
- Requires Kubernetes
- Complex setup

### Apache Airflow

**Mature general-purpose orchestration.**

```python
# airflow_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'ml-team',
    'depends_on_past': False,
    'email_on_failure': True,
    'email': ['ml-team@company.com'],
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'fraud_detection_training',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False
)

# Tasks
validate_task = PythonOperator(
    task_id='validate_data',
    python_callable=validate_training_data,
    op_kwargs={'data_path': 's3://ml-data/train.parquet'},
    dag=dag
)

train_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model_task,
    dag=dag
)

evaluate_task = PythonOperator(
    task_id='evaluate_model',
    python_callable=evaluate_model_task,
    dag=dag
)

register_task = PythonOperator(
    task_id='register_model',
    python_callable=register_model_task,
    dag=dag
)

# Dependencies
validate_task >> train_task >> evaluate_task >> register_task
```

**Advantages:**
- Mature, battle-tested
- Huge ecosystem (300+ integrations)
- Strong community support
- Rich UI

**Disadvantages:**
- Not ML-specific
- Can be complex for simple workflows
- Requires infrastructure management

### Metaflow (Netflix)

**Data science-friendly orchestration.**

```python
# metaflow_pipeline.py
from metaflow import FlowSpec, step, Parameter

class FraudDetectionFlow(FlowSpec):
    """Fraud detection training pipeline."""

    data_path = Parameter('data_path', default='s3://ml-data/train.parquet')

    @step
    def start(self):
        """Load data."""
        import pandas as pd
        self.df = pd.read_parquet(self.data_path)
        self.next(self.validate)

    @step
    def validate(self):
        """Validate data."""
        validate_training_data(self.df)
        self.next(self.train)

    @step
    def train(self):
        """Train model."""
        from sklearn.model_selection import train_test_split

        X = self.df.drop('label', axis=1)
        y = self.df['label']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        self.model = train_model(X_train, y_train)
        self.X_test = X_test
        self.y_test = y_test

        self.next(self.evaluate)

    @step
    def evaluate(self):
        """Evaluate model."""
        self.metrics, self.passed = evaluate_model(
            self.model,
            self.X_test,
            self.y_test,
            thresholds={'accuracy': 0.85, 'f1': 0.80}
        )
        self.next(self.end)

    @step
    def end(self):
        """Register model."""
        if self.passed:
            register_model(self.model, self.metrics, self.passed)
            print("✓ Pipeline complete")

if __name__ == '__main__':
    FraudDetectionFlow()
```

**Run:**
```bash
# Local
python fraud_detection_flow.py run

# AWS Batch
python fraud_detection_flow.py run --with batch
```

**Advantages:**
- Easiest for data scientists
- Excellent local development
- Automatic versioning
- Integrated with AWS Batch/Kubernetes

**Disadvantages:**
- Smaller community than Airflow
- Less mature

### Prefect

**Modern Python-native orchestration.**

```python
# prefect_flow.py
from prefect import flow, task

@task
def validate_data(data_path: str):
    """Validate data."""
    validate_training_data(data_path)
    return data_path

@task
def train_model_task(data_path: str):
    """Train model."""
    # Load data, train model
    return model

@task
def evaluate_model_task(model):
    """Evaluate model."""
    metrics, passed = evaluate_model(model, X_test, y_test, thresholds)
    return metrics, passed

@task
def register_model_task(model, metrics, passed):
    """Register model."""
    if passed:
        register_model(model, metrics, passed)

@flow(name="fraud-detection-training")
def training_flow(data_path: str):
    """Training pipeline."""
    validated_path = validate_data(data_path)
    model = train_model_task(validated_path)
    metrics, passed = evaluate_model_task(model)
    register_model_task(model, metrics, passed)

# Run
training_flow(data_path='s3://ml-data/train.parquet')
```

**Advantages:**
- Modern Python-native API
- Better error handling than Airflow
- Dynamic workflows (not static DAGs)
- Good UI

**Disadvantages:**
- Smaller community
- Less mature than Airflow

## Continuous Training

Automate model retraining based on drift detection.

### Continuous Training Pipeline

```python
# continuous_training.py
from datetime import datetime, timedelta

class ContinuousTrainingPipeline:
    """Automated retraining based on drift."""

    def __init__(self, model_name: str):
        self.model_name = model_name

    def should_retrain(self) -> bool:
        """Check if retraining needed."""

        # Get production model
        production_model = mlflow.pyfunc.load_model(f"models:/{self.model_name}/Production")

        # Get recent production data
        recent_data = fetch_recent_data(days=7)

        # Detect data drift
        drift_detected = self.detect_drift(production_model, recent_data)

        # Check performance degradation
        performance_degraded = self.check_performance(production_model, recent_data)

        # Check data volume
        sufficient_data = len(recent_data) > 10000

        return (drift_detected or performance_degraded) and sufficient_data

    def detect_drift(self, model, recent_data) -> bool:
        """Detect data drift."""
        from scipy import stats

        # Get training data distribution
        training_data = fetch_training_data(model)

        # KS test for each feature
        for col in recent_data.columns:
            if col == 'label':
                continue

            statistic, p_value = stats.ks_2samp(
                training_data[col],
                recent_data[col]
            )

            if p_value < 0.05:
                print(f"Drift detected in {col}: p-value={p_value:.4f}")
                return True

        return False

    def check_performance(self, model, recent_data) -> bool:
        """Check model performance degradation."""

        # Get predictions
        X = recent_data.drop('label', axis=1)
        y_true = recent_data['label']
        y_pred = model.predict(X)

        # Current accuracy
        from sklearn.metrics import accuracy_score
        current_accuracy = accuracy_score(y_true, y_pred)

        # Baseline accuracy (from model metadata)
        baseline_accuracy = get_model_baseline_accuracy(model)

        # Check degradation (>5% drop)
        degradation = baseline_accuracy - current_accuracy

        if degradation > 0.05:
            print(f"Performance degraded: {baseline_accuracy:.3f} → {current_accuracy:.3f}")
            return True

        return False

    def retrain(self):
        """Trigger retraining pipeline."""
        print("Triggering retraining pipeline...")

        # Trigger Airflow DAG or Kubeflow pipeline
        trigger_training_pipeline(model_name=self.model_name)

# Scheduled job (runs daily)
pipeline = ContinuousTrainingPipeline(model_name='fraud_detection')

if pipeline.should_retrain():
    pipeline.retrain()
else:
    print("No retraining needed")
```

## DAG Design Best Practices

### 1. Idempotency

Tasks should produce same result when re-run.

```python
# BAD: Not idempotent
@task
def train_model():
    # Appends to existing file (running twice duplicates data)
    with open('model.pkl', 'ab') as f:
        pickle.dump(model, f)

# GOOD: Idempotent
@task
def train_model():
    # Overwrites file (running twice produces same result)
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
```

### 2. Atomicity

Tasks should be atomic (all or nothing).

```python
# BAD: Non-atomic
@task
def register_model():
    save_model_to_s3()  # Success
    update_database()   # Fails
    # Result: Inconsistent state (S3 has model, DB doesn't)

# GOOD: Atomic with rollback
@task
def register_model():
    try:
        model_path = save_model_to_s3()
        update_database(model_path)
    except Exception as e:
        # Rollback
        delete_model_from_s3(model_path)
        raise
```

### 3. Separation of Concerns

Split complex tasks into smaller, focused tasks.

```python
# BAD: Monolithic task
@task
def train_and_deploy():
    # Validates, trains, evaluates, deploys (too much)
    validate_data()
    train_model()
    evaluate_model()
    deploy_model()

# GOOD: Separate tasks
@task
def validate_data(): ...

@task
def train_model(): ...

@task
def evaluate_model(): ...

@task
def deploy_model(): ...
```

### 4. Parameterization

Make pipelines reusable with parameters.

```python
@dsl.pipeline(name='training-pipeline')
def training_pipeline(
    data_path: str,
    model_name: str,
    hyperparameters: dict
):
    """Parameterized pipeline."""
    # Use parameters
    pass

# Run with different parameters
client.create_run_from_pipeline_func(
    training_pipeline,
    arguments={
        'data_path': 's3://ml-data/train.parquet',
        'model_name': 'fraud_detection',
        'hyperparameters': {'n_estimators': 100, 'max_depth': 10}
    }
)
```

## Implementation Examples

### Example: End-to-End Kubeflow Pipeline

```python
# kubeflow_complete_pipeline.py
import kfp
from kfp import dsl

@dsl.component(base_image='python:3.9', packages_to_install=['pandas', 'great-expectations'])
def validate_data(data_path: str) -> bool:
    """Data validation component."""
    import great_expectations as ge

    df = ge.read_csv(data_path)
    df.expect_table_columns_to_match_ordered_list(['user_id', 'feature_1', 'label'])
    results = df.validate()

    if not results['success']:
        raise ValueError("Data validation failed")

    return True

@dsl.component(base_image='python:3.9', packages_to_install=['pandas', 'scikit-learn'])
def train_model(
    data_path: str,
    n_estimators: int,
    max_depth: int,
    model_path: dsl.Output[dsl.Model]
):
    """Training component."""
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    import pickle

    # Load data
    df = pd.read_parquet(data_path)
    X = df.drop('label', axis=1)
    y = df['label']

    # Train
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
    model.fit(X, y)

    # Save
    with open(model_path.path, 'wb') as f:
        pickle.dump(model, f)

@dsl.component(base_image='python:3.9', packages_to_install=['scikit-learn'])
def evaluate_model(
    model_path: dsl.Input[dsl.Model],
    test_data_path: str
) -> dict:
    """Evaluation component."""
    import pickle
    import pandas as pd
    from sklearn.metrics import accuracy_score, f1_score

    # Load model
    with open(model_path.path, 'rb') as f:
        model = pickle.load(f)

    # Load test data
    df = pd.read_parquet(test_data_path)
    X_test = df.drop('label', axis=1)
    y_test = df['label']

    # Evaluate
    y_pred = model.predict(X_test)
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'f1': f1_score(y_test, y_pred)
    }

    return metrics

@dsl.pipeline(
    name='Fraud Detection Training Pipeline',
    description='Complete ML training pipeline'
)
def training_pipeline(
    data_path: str = 's3://ml-data/train.parquet',
    test_data_path: str = 's3://ml-data/test.parquet',
    n_estimators: int = 100,
    max_depth: int = 10
):
    """Complete training pipeline."""

    # Validate data
    validate_task = validate_data(data_path=data_path)

    # Train model (after validation)
    train_task = train_model(
        data_path=data_path,
        n_estimators=n_estimators,
        max_depth=max_depth
    ).after(validate_task)

    # Evaluate model
    evaluate_task = evaluate_model(
        model_path=train_task.outputs['model_path'],
        test_data_path=test_data_path
    )

    # Conditional deployment (if accuracy > 0.85)
    with dsl.Condition(evaluate_task.outputs['accuracy'] > 0.85):
        deploy_task = deploy_model(model_path=train_task.outputs['model_path'])

# Compile
kfp.compiler.Compiler().compile(training_pipeline, 'pipeline.yaml')

# Submit
client = kfp.Client(host='http://kubeflow.example.com')
run = client.create_run_from_pipeline_func(
    training_pipeline,
    arguments={
        'data_path': 's3://ml-data/train.parquet',
        'n_estimators': 200,
        'max_depth': 15
    }
)
```

### Example: Airflow with MLflow Integration

```python
# airflow_mlflow_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import mlflow

def train_with_mlflow(**context):
    """Train model with MLflow tracking."""

    with mlflow.start_run(run_name=f"training_{context['ds']}"):

        # Log parameters
        mlflow.log_params({
            'n_estimators': 100,
            'max_depth': 10
        })

        # Train
        model = train_model()

        # Evaluate
        metrics, passed = evaluate_model(model)

        # Log metrics
        mlflow.log_metrics(metrics)

        # Register if passed
        if passed:
            mlflow.sklearn.log_model(
                model,
                "model",
                registered_model_name="fraud_detection"
            )

            # Pass run_id to next task
            context['ti'].xcom_push(key='run_id', value=mlflow.active_run().info.run_id)

def promote_to_staging(**context):
    """Promote model to staging."""
    run_id = context['ti'].xcom_pull(key='run_id')

    client = mlflow.tracking.MlflowClient()

    # Get model version
    model_versions = client.search_model_versions(f"run_id='{run_id}'")
    version = model_versions[0].version

    # Promote to staging
    client.transition_model_version_stage(
        name="fraud_detection",
        version=version,
        stage="Staging"
    )

dag = DAG(
    'fraud_detection_training_mlflow',
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1)
)

train_task = PythonOperator(
    task_id='train_model',
    python_callable=train_with_mlflow,
    dag=dag
)

promote_task = PythonOperator(
    task_id='promote_to_staging',
    python_callable=promote_to_staging,
    dag=dag
)

train_task >> promote_task
```
