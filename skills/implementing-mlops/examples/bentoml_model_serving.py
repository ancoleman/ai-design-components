"""
BentoML Model Serving Example

Demonstrates model serving patterns including:
- Model packaging and versioning
- REST API endpoint creation
- Batching for inference optimization
- Docker containerization
"""

import bentoml
from bentoml.io import JSON, NumpyNdarray
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from pydantic import BaseModel
from typing import List
import asyncio


# =============================================================================
# Model Training and Saving
# =============================================================================

def train_and_save_model():
    """Train a model and save it to BentoML model store."""
    # Generate sample data
    X, y = make_classification(
        n_samples=1000,
        n_features=20,
        n_informative=15,
        random_state=42
    )

    # Train model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42
    )
    model.fit(X, y)

    # Save to BentoML model store
    saved_model = bentoml.sklearn.save_model(
        "fraud_classifier",
        model,
        signatures={
            "predict": {"batchable": True, "batch_dim": 0},
            "predict_proba": {"batchable": True, "batch_dim": 0},
        },
        labels={
            "framework": "sklearn",
            "model_type": "RandomForestClassifier",
            "version": "1.0.0",
        },
        metadata={
            "accuracy": 0.95,
            "training_date": "2025-01-15",
            "features": 20,
        },
        custom_objects={
            "feature_names": [f"feature_{i}" for i in range(20)],
        },
    )

    print(f"Model saved: {saved_model}")
    return saved_model


# =============================================================================
# Service Definition (service.py)
# =============================================================================

# Load the model
fraud_classifier = bentoml.sklearn.get("fraud_classifier:latest")

# Create a runner with batching enabled
fraud_runner = fraud_classifier.to_runner()

# Create the BentoML service
svc = bentoml.Service("fraud_detection_service", runners=[fraud_runner])


# Request/Response schemas
class PredictionRequest(BaseModel):
    features: List[float]


class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    model_version: str


class BatchPredictionRequest(BaseModel):
    instances: List[List[float]]


class BatchPredictionResponse(BaseModel):
    predictions: List[int]
    probabilities: List[float]


# Single prediction endpoint
@svc.api(input=JSON(pydantic_model=PredictionRequest), output=JSON(pydantic_model=PredictionResponse))
async def predict(request: PredictionRequest) -> PredictionResponse:
    """
    Single prediction endpoint.

    BentoML automatically batches concurrent requests for efficiency.
    """
    input_array = np.array([request.features])
    prediction = await fraud_runner.predict.async_run(input_array)
    probability = await fraud_runner.predict_proba.async_run(input_array)

    return PredictionResponse(
        prediction=int(prediction[0]),
        probability=float(probability[0][1]),
        model_version=fraud_classifier.tag.version,
    )


# Batch prediction endpoint
@svc.api(
    input=JSON(pydantic_model=BatchPredictionRequest),
    output=JSON(pydantic_model=BatchPredictionResponse)
)
async def predict_batch(request: BatchPredictionRequest) -> BatchPredictionResponse:
    """
    Batch prediction endpoint for bulk inference.

    More efficient for processing multiple instances at once.
    """
    input_array = np.array(request.instances)
    predictions = await fraud_runner.predict.async_run(input_array)
    probabilities = await fraud_runner.predict_proba.async_run(input_array)

    return BatchPredictionResponse(
        predictions=[int(p) for p in predictions],
        probabilities=[float(p[1]) for p in probabilities],
    )


# Health check endpoint
@svc.api(input=JSON(), output=JSON())
async def health() -> dict:
    """Health check for load balancer probes."""
    return {
        "status": "healthy",
        "model": "fraud_classifier",
        "version": fraud_classifier.tag.version,
    }


# =============================================================================
# Bento Configuration (bentofile.yaml)
# =============================================================================

BENTOFILE_CONFIG = """
service: "service:svc"
labels:
  owner: ml-team
  project: fraud-detection
include:
  - "*.py"
python:
  packages:
    - scikit-learn>=1.0
    - numpy>=1.20
    - pydantic>=2.0
docker:
  distro: debian
  python_version: "3.11"
  cuda_version: null  # Set for GPU models
  env:
    BENTOML_CONFIG: /home/bentoml/configuration.yaml
  setup_script: |
    apt-get update && apt-get install -y curl
"""


# =============================================================================
# Deployment Configurations
# =============================================================================

# Kubernetes Deployment
K8S_DEPLOYMENT = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fraud-detection
  labels:
    app: fraud-detection
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fraud-detection
  template:
    metadata:
      labels:
        app: fraud-detection
    spec:
      containers:
      - name: fraud-detection
        image: fraud-detection:latest
        ports:
        - containerPort: 3000
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
        env:
        - name: BENTOML_PORT
          value: "3000"
---
apiVersion: v1
kind: Service
metadata:
  name: fraud-detection
spec:
  selector:
    app: fraud-detection
  ports:
  - port: 80
    targetPort: 3000
  type: LoadBalancer
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: fraud-detection-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: fraud-detection
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
"""


# =============================================================================
# CLI Commands
# =============================================================================

CLI_COMMANDS = """
# Build the Bento
bentoml build

# List saved models
bentoml models list

# List built Bentos
bentoml list

# Serve locally for development
bentoml serve service:svc --reload

# Containerize
bentoml containerize fraud_detection_service:latest

# Push to registry
bentoml push fraud_detection_service:latest

# Deploy to BentoCloud
bentoml deploy fraud_detection_service:latest

# Export Bento to directory
bentoml export fraud_detection_service:latest ./export/
"""


if __name__ == "__main__":
    # Train and save model
    saved_model = train_and_save_model()

    print("\n=== BentoML Model Serving ===")
    print(f"Model saved: {saved_model.tag}")
    print("\nTo serve locally:")
    print("  bentoml serve service:svc --reload")
    print("\nTo build and containerize:")
    print("  bentoml build")
    print("  bentoml containerize fraud_detection_service:latest")
