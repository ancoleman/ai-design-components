# BentoML - ML Model Deployment Made Easy


## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Basic Workflow](#basic-workflow)
  - [1. Train and Save Model](#1-train-and-save-model)
  - [2. Create Service](#2-create-service)
  - [3. Serve Locally](#3-serve-locally)
  - [4. Build and Deploy](#4-build-and-deploy)
- [Adaptive Batching](#adaptive-batching)
  - [How It Works](#how-it-works)
  - [Configuration](#configuration)
- [Multi-Framework Support](#multi-framework-support)
  - [PyTorch](#pytorch)
  - [XGBoost](#xgboost)
  - [TensorFlow](#tensorflow)
- [Configuration](#configuration)
  - [Service Configuration](#service-configuration)
  - [bentofile.yaml](#bentofileyaml)
- [Deployment Patterns](#deployment-patterns)
  - [Docker](#docker)
  - [Kubernetes](#kubernetes)
  - [AWS Lambda](#aws-lambda)
- [Observability](#observability)
  - [Built-in Metrics](#built-in-metrics)
  - [Logging](#logging)
  - [Distributed Tracing](#distributed-tracing)
- [Testing](#testing)
- [Best Practices](#best-practices)
- [Resources](#resources)

## Overview

BentoML is a Python-native framework for building production-ready ML model serving APIs with adaptive batching, multi-framework support, and easy deployment to Kubernetes, AWS, GCP, and Azure.

**Key Features:**
- Python-first design (feels native for data scientists)
- Adaptive batching for throughput optimization
- Multi-framework: scikit-learn, PyTorch, TensorFlow, XGBoost, LightGBM
- Deploy anywhere: Docker, Kubernetes, AWS Lambda, GCP Cloud Run
- Built-in observability: metrics, logging, tracing

## Installation

```bash
# Core BentoML
pip install bentoml

# Framework-specific
pip install bentoml[sklearn]
pip install bentoml[pytorch]
pip install bentoml[tensorflow]
pip install bentoml[xgboost]
```

## Basic Workflow

### 1. Train and Save Model

```python
import bentoml
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris

# Train model
X, y = load_iris(return_X_y=True)
model = RandomForestClassifier()
model.fit(X, y)

# Save to BentoML model store
bentoml.sklearn.save_model(
    "iris_classifier",
    model,
    signatures={"predict": {"batchable": True}},
    metadata={
        "framework": "scikit-learn",
        "accuracy": 0.96,
        "created_at": "2025-12-02"
    }
)
```

### 2. Create Service

```python
# service.py
import bentoml
import numpy as np
from pydantic import BaseModel

class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@bentoml.service(
    resources={"cpu": "2", "memory": "4Gi"},
    traffic={"timeout": 10}
)
class IrisClassifier:
    model_ref = bentoml.models.get("iris_classifier:latest")

    def __init__(self):
        self.model = bentoml.sklearn.load_model(self.model_ref)
        self.class_names = ['setosa', 'versicolor', 'virginica']

    @bentoml.api(batchable=True, max_batch_size=32, max_latency_ms=1000)
    def classify(self, features: list[IrisFeatures]) -> list[str]:
        # Convert to numpy array
        X = np.array([[
            f.sepal_length,
            f.sepal_width,
            f.petal_length,
            f.petal_width
        ] for f in features])

        # Predict
        predictions = self.model.predict(X)

        # Map to class names
        return [self.class_names[p] for p in predictions]

    @bentoml.api
    def predict_proba(self, features: IrisFeatures) -> dict[str, float]:
        X = np.array([[
            features.sepal_length,
            features.sepal_width,
            features.petal_length,
            features.petal_width
        ]])

        probas = self.model.predict_proba(X)[0]

        return {
            self.class_names[i]: float(probas[i])
            for i in range(len(self.class_names))
        }
```

### 3. Serve Locally

```bash
# Development server
bentoml serve service:IrisClassifier

# Production server (with workers)
bentoml serve service:IrisClassifier --production
```

### 4. Build and Deploy

```bash
# Build Bento (packaged service)
bentoml build

# Containerize
bentoml containerize iris_classifier:latest

# Deploy to Kubernetes
kubectl apply -f deployment.yaml

# Or deploy to BentoCloud (managed)
bentoml deploy iris_classifier:latest
```

## Adaptive Batching

BentoML's killer feature: automatic request batching for throughput.

### How It Works

```
Without Batching:
Request 1 → Model (10ms)
Request 2 → Model (10ms)  ← Wait for Request 1
Request 3 → Model (10ms)  ← Wait for Request 2
Total: 30ms for 3 requests

With Adaptive Batching:
Request 1 ─┐
Request 2 ─┼→ Batch → Model (12ms)
Request 3 ─┘
Total: 12ms for 3 requests (2.5x faster)
```

### Configuration

```python
@bentoml.api(
    batchable=True,
    max_batch_size=32,      # Maximum batch size
    max_latency_ms=1000     # Maximum wait time to fill batch
)
def predict(self, inputs: list[np.ndarray]) -> list[float]:
    # BentoML automatically batches requests
    batch = np.array(inputs)
    return self.model.predict(batch).tolist()
```

**Tuning Parameters:**
- `max_batch_size`: Larger = higher throughput, but higher latency
- `max_latency_ms`: Shorter = lower latency, but smaller batches

**Rule of thumb:**
- High throughput service: `max_batch_size=64, max_latency_ms=2000`
- Low latency service: `max_batch_size=8, max_latency_ms=100`

## Multi-Framework Support

### PyTorch

```python
import bentoml
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Save PyTorch model
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")
bentoml.pytorch.save_model("bert_classifier", model)

# Service
@bentoml.service
class BertClassifier:
    model_ref = bentoml.models.get("bert_classifier:latest")

    def __init__(self):
        self.model = bentoml.pytorch.load_model(self.model_ref)
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

    @bentoml.api
    def classify(self, text: str) -> dict:
        inputs = self.tokenizer(text, return_tensors="pt", padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return {"logits": outputs.logits.tolist()}
```

### XGBoost

```python
import bentoml
import xgboost as xgb

# Save XGBoost model
model = xgb.XGBClassifier()
model.fit(X_train, y_train)
bentoml.xgboost.save_model("fraud_detector", model)

# Service
@bentoml.service
class FraudDetector:
    model_ref = bentoml.models.get("fraud_detector:latest")

    def __init__(self):
        self.model = bentoml.xgboost.load_model(self.model_ref)

    @bentoml.api(batchable=True, max_batch_size=128)
    def predict(self, transactions: list[dict]) -> list[bool]:
        import pandas as pd
        df = pd.DataFrame(transactions)
        predictions = self.model.predict(df)
        return predictions.tolist()
```

### TensorFlow

```python
import bentoml
import tensorflow as tf

# Save TensorFlow model
model = tf.keras.models.Sequential([...])
bentoml.tensorflow.save_model("image_classifier", model)

# Service
@bentoml.service
class ImageClassifier:
    model_ref = bentoml.models.get("image_classifier:latest")

    def __init__(self):
        self.model = bentoml.tensorflow.load_model(self.model_ref)

    @bentoml.api
    def classify(self, image: np.ndarray) -> dict:
        predictions = self.model.predict(np.expand_dims(image, 0))
        return {"class": int(np.argmax(predictions))}
```

## Configuration

### Service Configuration

```python
@bentoml.service(
    # Resource allocation
    resources={
        "cpu": "2",           # 2 CPU cores
        "memory": "4Gi",      # 4GB RAM
        "gpu": 1,             # 1 GPU (optional)
        "gpu_type": "nvidia-tesla-t4"
    },

    # Traffic settings
    traffic={
        "timeout": 30,        # Request timeout (seconds)
        "concurrency": 32     # Max concurrent requests
    },

    # Workers (production mode)
    workers=4,               # Number of worker processes

    # Logging
    logging={
        "access": {
            "enabled": True,
            "request_content_length": True,
            "response_content_length": True
        }
    }
)
class MyService:
    ...
```

### bentofile.yaml

For build-time configuration:

```yaml
service: "service:IrisClassifier"
include:
  - "service.py"
  - "preprocessing.py"
python:
  packages:
    - scikit-learn==1.3.0
    - pandas==2.0.0
    - numpy==1.24.0
docker:
  distro: debian
  python_version: "3.11"
  system_packages:
    - git
  env:
    MODEL_NAME: "iris_classifier"
```

## Deployment Patterns

### Docker

```bash
# Build container
bentoml containerize iris_classifier:latest -t iris:v1

# Run locally
docker run -p 3000:3000 iris:v1

# Push to registry
docker tag iris:v1 myregistry.io/iris:v1
docker push myregistry.io/iris:v1
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: iris-classifier
spec:
  replicas: 3
  selector:
    matchLabels:
      app: iris-classifier
  template:
    metadata:
      labels:
        app: iris-classifier
    spec:
      containers:
      - name: iris
        image: myregistry.io/iris:v1
        ports:
        - containerPort: 3000
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        livenessProbe:
          httpGet:
            path: /livez
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /readyz
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: iris-classifier
spec:
  selector:
    app: iris-classifier
  ports:
  - port: 80
    targetPort: 3000
  type: LoadBalancer
```

### AWS Lambda

```bash
# Build for Lambda
bentoml build --containerize

# Deploy to AWS
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker tag iris:latest <account>.dkr.ecr.us-east-1.amazonaws.com/iris:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/iris:latest

# Create Lambda function
aws lambda create-function \
  --function-name iris-classifier \
  --package-type Image \
  --code ImageUri=<account>.dkr.ecr.us-east-1.amazonaws.com/iris:latest \
  --role arn:aws:iam::<account>:role/lambda-execution-role
```

## Observability

### Built-in Metrics

BentoML exposes Prometheus metrics at `/metrics`:

**Key Metrics:**
- `bentoml_request_duration_seconds` - Request latency histogram
- `bentoml_request_total` - Total requests counter
- `bentoml_request_in_progress` - Current active requests
- `bentoml_runner_adaptive_batch_size` - Current batch size

### Logging

```python
import logging

logger = logging.getLogger(__name__)

@bentoml.service
class MyService:
    @bentoml.api
    def predict(self, data: dict):
        logger.info(f"Received request: {data}")
        result = self.model.predict(data)
        logger.info(f"Prediction: {result}")
        return result
```

### Distributed Tracing

```python
from opentelemetry import trace

@bentoml.service
class MyService:
    @bentoml.api
    def predict(self, data: dict):
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("preprocessing"):
            processed = preprocess(data)
        with tracer.start_as_current_span("inference"):
            result = self.model.predict(processed)
        return result
```

## Testing

```python
import bentoml
from bentoml.testing.server import serve

def test_classifier():
    with serve("service:IrisClassifier") as client:
        # Test classify endpoint
        response = client.classify(
            features=[{
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }]
        )
        assert response == ["setosa"]

        # Test probability endpoint
        response = client.predict_proba(
            features={
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }
        )
        assert "setosa" in response
        assert response["setosa"] > 0.9
```

## Best Practices

1. **Use Pydantic for Input Validation:**
   ```python
   from pydantic import BaseModel, validator

   class Features(BaseModel):
       value: float

       @validator('value')
       def check_range(cls, v):
           if not 0 <= v <= 100:
               raise ValueError('value must be between 0 and 100')
           return v
   ```

2. **Enable Adaptive Batching for High Throughput:**
   ```python
   @bentoml.api(batchable=True, max_batch_size=64)
   def predict(self, inputs: list[np.ndarray]) -> list[float]:
       ...
   ```

3. **Set Resource Limits:**
   ```python
   @bentoml.service(resources={"cpu": "2", "memory": "4Gi"})
   ```

4. **Add Health Checks:**
   BentoML provides `/healthz`, `/livez`, `/readyz` automatically

5. **Version Models:**
   ```python
   bentoml.sklearn.save_model("classifier", model, version="v1.2.0")
   ```

6. **Monitor Metrics:**
   Configure Prometheus scraping of `/metrics` endpoint

## Resources

- BentoML Documentation: https://docs.bentoml.com/
- GitHub: https://github.com/bentoml/BentoML
- Examples: https://github.com/bentoml/BentoML/tree/main/examples
- BentoCloud: https://bentoml.com/ (managed deployment)
