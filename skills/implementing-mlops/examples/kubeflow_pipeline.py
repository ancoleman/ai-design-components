"""
Kubeflow Pipeline Example

Demonstrates ML pipeline orchestration patterns including:
- Component definition and containerization
- Pipeline DAG construction
- Artifact passing between components
- Conditional execution and loops
"""

from kfp import dsl
from kfp import compiler
from kfp.dsl import Input, Output, Dataset, Model, Metrics, Artifact
from typing import NamedTuple


# =============================================================================
# Pipeline Components
# =============================================================================

@dsl.component(
    base_image="python:3.11-slim",
    packages_to_install=["pandas", "scikit-learn", "pyarrow"]
)
def load_data(
    dataset_path: str,
    output_dataset: Output[Dataset],
) -> NamedTuple("Outputs", [("num_samples", int), ("num_features", int)]):
    """Load and validate training data."""
    import pandas as pd
    from collections import namedtuple

    # Load data (in production, this would read from GCS/S3)
    from sklearn.datasets import make_classification
    X, y = make_classification(
        n_samples=10000,
        n_features=20,
        n_informative=15,
        random_state=42
    )

    df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(20)])
    df["target"] = y

    # Save to output artifact
    df.to_parquet(output_dataset.path)

    outputs = namedtuple("Outputs", ["num_samples", "num_features"])
    return outputs(len(df), len(df.columns) - 1)


@dsl.component(
    base_image="python:3.11-slim",
    packages_to_install=["pandas", "scikit-learn", "pyarrow"]
)
def preprocess_data(
    input_dataset: Input[Dataset],
    train_dataset: Output[Dataset],
    test_dataset: Output[Dataset],
    test_size: float = 0.2,
):
    """Split data into train/test sets and apply preprocessing."""
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler

    # Load data
    df = pd.read_parquet(input_dataset.path)
    X = df.drop("target", axis=1)
    y = df["target"]

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(
        scaler.fit_transform(X_train),
        columns=X_train.columns
    )
    X_test_scaled = pd.DataFrame(
        scaler.transform(X_test),
        columns=X_test.columns
    )

    # Save outputs
    train_df = X_train_scaled.copy()
    train_df["target"] = y_train.values
    train_df.to_parquet(train_dataset.path)

    test_df = X_test_scaled.copy()
    test_df["target"] = y_test.values
    test_df.to_parquet(test_dataset.path)


@dsl.component(
    base_image="python:3.11-slim",
    packages_to_install=["pandas", "scikit-learn", "pyarrow", "joblib"]
)
def train_model(
    train_dataset: Input[Dataset],
    model_artifact: Output[Model],
    n_estimators: int = 100,
    max_depth: int = 10,
):
    """Train a RandomForest classifier."""
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    import joblib

    # Load training data
    df = pd.read_parquet(train_dataset.path)
    X = df.drop("target", axis=1)
    y = df["target"]

    # Train model
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X, y)

    # Save model artifact
    model_artifact.metadata["framework"] = "sklearn"
    model_artifact.metadata["model_type"] = "RandomForestClassifier"
    model_artifact.metadata["n_estimators"] = n_estimators
    model_artifact.metadata["max_depth"] = max_depth

    joblib.dump(model, model_artifact.path)


@dsl.component(
    base_image="python:3.11-slim",
    packages_to_install=["pandas", "scikit-learn", "pyarrow", "joblib"]
)
def evaluate_model(
    model_artifact: Input[Model],
    test_dataset: Input[Dataset],
    metrics: Output[Metrics],
    evaluation_report: Output[Artifact],
) -> NamedTuple("Outputs", [("accuracy", float), ("f1_score", float)]):
    """Evaluate model performance on test set."""
    import pandas as pd
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score, f1_score,
        classification_report, confusion_matrix
    )
    import joblib
    import json
    from collections import namedtuple

    # Load model and test data
    model = joblib.load(model_artifact.path)
    df = pd.read_parquet(test_dataset.path)
    X_test = df.drop("target", axis=1)
    y_test = df["target"]

    # Predict
    y_pred = model.predict(X_test)

    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    # Log metrics for Kubeflow UI
    metrics.log_metric("accuracy", accuracy)
    metrics.log_metric("precision", precision)
    metrics.log_metric("recall", recall)
    metrics.log_metric("f1_score", f1)

    # Save detailed report
    report = {
        "classification_report": classification_report(y_test, y_pred, output_dict=True),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
    }

    with open(evaluation_report.path, "w") as f:
        json.dump(report, f, indent=2)

    outputs = namedtuple("Outputs", ["accuracy", "f1_score"])
    return outputs(accuracy, f1)


@dsl.component(
    base_image="python:3.11-slim",
    packages_to_install=["joblib", "google-cloud-storage"]
)
def deploy_model(
    model_artifact: Input[Model],
    model_name: str,
    deployment_env: str,
) -> str:
    """Deploy model to serving infrastructure."""
    import joblib
    import json

    model = joblib.load(model_artifact.path)

    # In production, this would:
    # 1. Push model to model registry
    # 2. Update serving deployment
    # 3. Run canary deployment

    deployment_info = {
        "model_name": model_name,
        "environment": deployment_env,
        "model_metadata": model_artifact.metadata,
        "status": "deployed",
    }

    print(f"Deployed model: {json.dumps(deployment_info, indent=2)}")

    return f"gs://models/{model_name}/{deployment_env}/model.joblib"


# =============================================================================
# Pipeline Definition
# =============================================================================

@dsl.pipeline(
    name="ml-training-pipeline",
    description="End-to-end ML training pipeline with evaluation and deployment"
)
def ml_training_pipeline(
    dataset_path: str = "gs://bucket/data/training_data.parquet",
    n_estimators: int = 100,
    max_depth: int = 10,
    test_size: float = 0.2,
    min_accuracy: float = 0.85,
    model_name: str = "fraud_classifier",
    deployment_env: str = "staging",
):
    """
    ML Training Pipeline

    1. Load and validate data
    2. Preprocess and split data
    3. Train model with hyperparameters
    4. Evaluate model performance
    5. Deploy if accuracy threshold met
    """
    # Load data
    load_task = load_data(dataset_path=dataset_path)

    # Preprocess
    preprocess_task = preprocess_data(
        input_dataset=load_task.outputs["output_dataset"],
        test_size=test_size,
    )

    # Train model
    train_task = train_model(
        train_dataset=preprocess_task.outputs["train_dataset"],
        n_estimators=n_estimators,
        max_depth=max_depth,
    )

    # Evaluate
    eval_task = evaluate_model(
        model_artifact=train_task.outputs["model_artifact"],
        test_dataset=preprocess_task.outputs["test_dataset"],
    )

    # Conditional deployment based on accuracy threshold
    with dsl.If(eval_task.outputs["accuracy"] >= min_accuracy):
        deploy_model(
            model_artifact=train_task.outputs["model_artifact"],
            model_name=model_name,
            deployment_env=deployment_env,
        )


# =============================================================================
# Pipeline with Hyperparameter Tuning
# =============================================================================

@dsl.pipeline(
    name="ml-hyperparameter-tuning",
    description="Pipeline with parallel hyperparameter experiments"
)
def hyperparameter_tuning_pipeline(
    dataset_path: str = "gs://bucket/data/training_data.parquet",
):
    """Run multiple training experiments with different hyperparameters."""

    # Load data once
    load_task = load_data(dataset_path=dataset_path)
    preprocess_task = preprocess_data(
        input_dataset=load_task.outputs["output_dataset"],
    )

    # Hyperparameter configurations
    configs = [
        {"n_estimators": 50, "max_depth": 5},
        {"n_estimators": 100, "max_depth": 10},
        {"n_estimators": 200, "max_depth": 15},
        {"n_estimators": 100, "max_depth": 20},
    ]

    # Run experiments in parallel using ParallelFor
    with dsl.ParallelFor(configs) as config:
        train_task = train_model(
            train_dataset=preprocess_task.outputs["train_dataset"],
            n_estimators=config.n_estimators,
            max_depth=config.max_depth,
        )

        evaluate_model(
            model_artifact=train_task.outputs["model_artifact"],
            test_dataset=preprocess_task.outputs["test_dataset"],
        )


# =============================================================================
# Compile and Run
# =============================================================================

if __name__ == "__main__":
    # Compile pipeline to YAML
    compiler.Compiler().compile(
        pipeline_func=ml_training_pipeline,
        package_path="ml_training_pipeline.yaml"
    )
    print("Pipeline compiled to ml_training_pipeline.yaml")

    compiler.Compiler().compile(
        pipeline_func=hyperparameter_tuning_pipeline,
        package_path="hyperparameter_tuning_pipeline.yaml"
    )
    print("Pipeline compiled to hyperparameter_tuning_pipeline.yaml")

    # To run on Kubeflow:
    # from kfp.client import Client
    # client = Client(host="https://kubeflow.example.com")
    # client.create_run_from_pipeline_package(
    #     "ml_training_pipeline.yaml",
    #     arguments={
    #         "n_estimators": 150,
    #         "max_depth": 12,
    #         "min_accuracy": 0.9,
    #     }
    # )
