"""
MLflow Experiment Tracking Example

Demonstrates experiment tracking patterns for ML projects including:
- Logging parameters, metrics, and artifacts
- Model versioning and registration
- Experiment comparison and reproducibility
"""

import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np
from datetime import datetime


def setup_mlflow(experiment_name: str, tracking_uri: str = "sqlite:///mlflow.db"):
    """Initialize MLflow tracking with local SQLite backend."""
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)
    return mlflow.get_experiment_by_name(experiment_name)


def train_with_tracking(
    n_estimators: int = 100,
    max_depth: int = 10,
    min_samples_split: int = 2,
    experiment_name: str = "rf_classifier_experiment"
):
    """
    Train RandomForest classifier with full MLflow tracking.

    Logs:
    - Hyperparameters (n_estimators, max_depth, min_samples_split)
    - Metrics (accuracy, precision, recall, f1)
    - Model artifacts (sklearn model, feature importances)
    - Metadata (git commit, timestamp, dataset info)
    """
    setup_mlflow(experiment_name)

    # Generate synthetic classification data
    X, y = make_classification(
        n_samples=1000,
        n_features=20,
        n_informative=15,
        n_redundant=5,
        random_state=42
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    with mlflow.start_run(run_name=f"rf_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
        # Log parameters
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("min_samples_split", min_samples_split)
        mlflow.log_param("dataset_size", len(X))
        mlflow.log_param("n_features", X.shape[1])

        # Log tags for organization
        mlflow.set_tag("model_type", "RandomForestClassifier")
        mlflow.set_tag("framework", "sklearn")
        mlflow.set_tag("stage", "development")

        # Train model
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train, y_train)

        # Evaluate and log metrics
        y_pred = model.predict(X_test)

        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred),
            "recall": recall_score(y_test, y_pred),
            "f1": f1_score(y_test, y_pred)
        }

        for metric_name, metric_value in metrics.items():
            mlflow.log_metric(metric_name, metric_value)

        # Log feature importances as artifact
        importances = model.feature_importances_
        np.save("feature_importances.npy", importances)
        mlflow.log_artifact("feature_importances.npy")

        # Log model with signature
        signature = mlflow.models.infer_signature(X_train, model.predict(X_train))
        mlflow.sklearn.log_model(
            model,
            "model",
            signature=signature,
            registered_model_name="rf_classifier"
        )

        print(f"Run completed: {mlflow.active_run().info.run_id}")
        print(f"Metrics: {metrics}")

        return model, metrics


def compare_experiments(experiment_name: str, metric: str = "f1"):
    """Compare runs within an experiment by a specific metric."""
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if not experiment:
        raise ValueError(f"Experiment '{experiment_name}' not found")

    runs = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=[f"metrics.{metric} DESC"]
    )

    print(f"\nTop runs by {metric}:")
    print(runs[["run_id", f"metrics.{metric}", "params.n_estimators", "params.max_depth"]].head(5))

    return runs


def promote_model_to_production(model_name: str, version: int):
    """
    Transition a model version to production stage.

    Stage transitions:
    - None -> Staging: Initial testing
    - Staging -> Production: Approved for serving
    - Production -> Archived: Deprecated
    """
    client = mlflow.tracking.MlflowClient()

    # Transition to staging first
    client.transition_model_version_stage(
        name=model_name,
        version=version,
        stage="Staging"
    )
    print(f"Model {model_name} v{version} promoted to Staging")

    # After validation, promote to production
    client.transition_model_version_stage(
        name=model_name,
        version=version,
        stage="Production"
    )
    print(f"Model {model_name} v{version} promoted to Production")


if __name__ == "__main__":
    # Run hyperparameter experiments
    experiments = [
        {"n_estimators": 50, "max_depth": 5},
        {"n_estimators": 100, "max_depth": 10},
        {"n_estimators": 200, "max_depth": 15},
        {"n_estimators": 100, "max_depth": None},  # Unlimited depth
    ]

    for params in experiments:
        print(f"\nTraining with params: {params}")
        train_with_tracking(**params)

    # Compare experiment results
    compare_experiments("rf_classifier_experiment", metric="f1")
