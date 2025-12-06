# Model Serving

Deploy ML models for inference at scale with optimized infrastructure and serving patterns.

## Table of Contents

- [Overview](#overview)
- [Serving Platforms](#serving-platforms)
- [Serving Patterns](#serving-patterns)
- [Model Optimization](#model-optimization)
- [Auto-Scaling](#auto-scaling)
- [Implementation Examples](#implementation-examples)

## Overview

Model serving transforms trained models into production endpoints capable of handling inference requests at scale with low latency and high availability.

### Serving Requirements

| Requirement | Description | Target |
|------------|-------------|--------|
| Latency | Time to return prediction | <100ms (REST), <10ms (gRPC) |
| Throughput | Predictions per second | 100-10,000+ RPS |
| Availability | Uptime percentage | 99.9% (3 nines) |
| Scalability | Handle traffic spikes | Auto-scale 10x |
| Cost | Infrastructure cost per 1M predictions | <$10 |

## Serving Platforms

### TensorFlow Serving

**Production-grade serving for TensorFlow models.**

```bash
# Install TensorFlow Serving
docker pull tensorflow/serving

# Serve model
docker run -p 8501:8501 \
  --mount type=bind,source=/path/to/model,target=/models/my_model \
  -e MODEL_NAME=my_model \
  -t tensorflow/serving
```

**REST API:**
```python
import requests
import json

# Predict
data = json.dumps({
    "signature_name": "serving_default",
    "instances": [[1.0, 2.0, 3.0, 4.0]]
})

response = requests.post(
    'http://localhost:8501/v1/models/my_model:predict',
    data=data
)

predictions = response.json()['predictions']
```

**gRPC (lower latency):**
```python
import grpc
from tensorflow_serving.apis import prediction_service_pb2_grpc
from tensorflow_serving.apis import predict_pb2

channel = grpc.insecure_channel('localhost:8500')
stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

request = predict_pb2.PredictRequest()
request.model_spec.name = 'my_model'
request.model_spec.signature_name = 'serving_default'

# Add input tensors
request.inputs['input'].CopyFrom(tf.make_tensor_proto([1.0, 2.0, 3.0, 4.0]))

result = stub.Predict(request)
```

### TorchServe

**PyTorch official serving solution.**

```bash
# Install TorchServe
pip install torchserve torch-model-archiver

# Archive model
torch-model-archiver \
  --model-name fraud_detection \
  --version 1.0 \
  --serialized-file model.pt \
  --handler image_classifier

# Start server
torchserve --start --model-store model_store --models fraud_detection.mar
```

**Inference:**
```python
import requests

response = requests.post(
    'http://localhost:8080/predictions/fraud_detection',
    files={'data': open('input.json', 'rb')}
)

prediction = response.json()
```

### BentoML

**Python-first model serving with simplicity focus.**

```python
# bentoml_service.py
import bentoml
from bentoml.io import JSON, NumpyNdarray

# Save model to BentoML
bentoml.sklearn.save_model("fraud_detection", model)

# Create service
fraud_detection_runner = bentoml.sklearn.get("fraud_detection:latest").to_runner()

svc = bentoml.Service("fraud_detection_service", runners=[fraud_detection_runner])

@svc.api(input=NumpyNdarray(), output=JSON())
def predict(input_data):
    result = fraud_detection_runner.predict.run(input_data)
    return {"prediction": result.tolist()}
```

**Serve:**
```bash
# Local development
bentoml serve service.py:svc --reload

# Build container
bentoml containerize fraud_detection_service:latest

# Deploy to Kubernetes
bentoml deploy fraud_detection_service:latest
```

### Seldon Core

**Kubernetes-native ML serving with advanced deployment patterns.**

```yaml
# seldon-deployment.yaml
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: fraud-detection
spec:
  predictors:
  - name: default
    replicas: 3
    graph:
      name: classifier
      type: MODEL
      endpoint:
        type: REST
      children: []
    componentSpecs:
    - spec:
        containers:
        - name: classifier
          image: fraud-detection:v1
          resources:
            requests:
              memory: "1Gi"
              cpu: "1"
            limits:
              memory: "2Gi"
              cpu: "2"
```

**Canary deployment:**
```yaml
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: fraud-detection
spec:
  predictors:
  - name: main
    replicas: 3
    traffic: 90
    graph:
      name: classifier
      type: MODEL
      endpoint:
        type: REST
    componentSpecs:
    - spec:
        containers:
        - name: classifier
          image: fraud-detection:v1

  - name: canary
    replicas: 1
    traffic: 10
    graph:
      name: classifier
      type: MODEL
      endpoint:
        type: REST
    componentSpecs:
    - spec:
        containers:
        - name: classifier
          image: fraud-detection:v2
```

### KServe

**CNCF standard for ML serving on Kubernetes.**

```yaml
# kserve-inference-service.yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: fraud-detection
spec:
  predictor:
    sklearn:
      storageUri: "s3://models/fraud-detection"
      resources:
        requests:
          cpu: "1"
          memory: "2Gi"
        limits:
          cpu: "2"
          memory: "4Gi"
```

**Auto-scaling (Knative):**
```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: fraud-detection
  annotations:
    autoscaling.knative.dev/target: "10"
    autoscaling.knative.dev/minScale: "1"
    autoscaling.knative.dev/maxScale: "10"
spec:
  predictor:
    sklearn:
      storageUri: "s3://models/fraud-detection"
```

## Serving Patterns

### REST API Serving

Synchronous HTTP endpoint for predictions.

```python
# fastapi_serving.py
from fastapi import FastAPI
import mlflow.pyfunc
import numpy as np

app = FastAPI()

# Load model at startup
model = mlflow.pyfunc.load_model("models:/fraud_detection/Production")

@app.post("/predict")
def predict(features: list[float]):
    """Predict fraud probability."""

    # Convert to numpy array
    input_data = np.array([features])

    # Predict
    prediction = model.predict(input_data)

    return {
        "prediction": int(prediction[0]),
        "probability": float(prediction[0])
    }

# Run: uvicorn fastapi_serving:app --host 0.0.0.0 --port 8000
```

### Batch Inference

Process large datasets offline.

```python
# batch_inference.py
import pandas as pd
import mlflow.pyfunc
from pyspark.sql import SparkSession

def batch_predict_spark(input_path, output_path, model_uri):
    """Batch inference with Spark for large datasets."""

    spark = SparkSession.builder.appName("BatchInference").getOrCreate()

    # Load data
    df = spark.read.parquet(input_path)

    # Load model as UDF
    predict_udf = mlflow.pyfunc.spark_udf(
        spark,
        model_uri=model_uri,
        result_type='double'
    )

    # Apply predictions
    predictions_df = df.withColumn(
        'prediction',
        predict_udf(*df.columns)
    )

    # Save results
    predictions_df.write.parquet(output_path)

    print(f"Batch predictions saved to {output_path}")

# Usage
batch_predict_spark(
    input_path="s3://data/to_predict.parquet",
    output_path="s3://data/predictions.parquet",
    model_uri="models:/fraud_detection/Production"
)
```

### Streaming Inference

Real-time predictions on streaming data.

```python
# streaming_inference.py
from kafka import KafkaConsumer, KafkaProducer
import json
import mlflow.pyfunc

# Load model
model = mlflow.pyfunc.load_model("models:/fraud_detection/Production")

# Kafka consumer
consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

# Stream processing
for message in consumer:
    transaction = message.value

    # Extract features
    features = [
        transaction['amount'],
        transaction['merchant_category'],
        transaction['time_of_day']
    ]

    # Predict
    prediction = model.predict([features])[0]

    # Produce prediction
    result = {
        'transaction_id': transaction['id'],
        'prediction': int(prediction),
        'timestamp': transaction['timestamp']
    }

    producer.send('fraud_predictions', result)
```

### gRPC Serving

Low-latency serving with gRPC protocol.

```python
# grpc_serving.py
import grpc
from concurrent import futures
import model_pb2
import model_pb2_grpc
import mlflow.pyfunc

class ModelServicer(model_pb2_grpc.ModelServiceServicer):
    def __init__(self):
        self.model = mlflow.pyfunc.load_model("models:/fraud_detection/Production")

    def Predict(self, request, context):
        # Extract features
        features = [request.features]

        # Predict
        prediction = self.model.predict(features)[0]

        # Return response
        return model_pb2.PredictResponse(
            prediction=int(prediction),
            probability=float(prediction)
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    model_pb2_grpc.add_ModelServiceServicer_to_server(ModelServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
```

## Model Optimization

Reduce model size and inference latency.

### Quantization

Convert model weights from float32 to int8.

```python
# quantization.py
import torch
from torch.quantization import quantize_dynamic

# Load PyTorch model
model = torch.load('model.pt')

# Dynamic quantization
quantized_model = quantize_dynamic(
    model,
    {torch.nn.Linear},  # Layers to quantize
    dtype=torch.qint8
)

# Save quantized model
torch.save(quantized_model, 'model_quantized.pt')

# Size reduction: ~4x smaller
# Latency reduction: ~2-3x faster
# Accuracy impact: <1% degradation typically
```

### ONNX Conversion

Convert to ONNX for cross-framework compatibility and optimization.

```python
# onnx_conversion.py
import torch
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

# Convert sklearn model
initial_type = [('float_input', FloatTensorType([None, 10]))]
onnx_model = convert_sklearn(sklearn_model, initial_types=initial_type)

# Save
with open("model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())

# Inference with ONNX Runtime
import onnxruntime as rt

sess = rt.InferenceSession("model.onnx")
input_name = sess.get_inputs()[0].name
output_name = sess.get_outputs()[0].name

prediction = sess.run([output_name], {input_name: input_data})

# Speed improvement: 1.5-3x faster than native framework
```

### Model Pruning

Remove less important weights.

```python
# pruning.py
import torch
import torch.nn.utils.prune as prune

# Load model
model = torch.load('model.pt')

# Prune 30% of weights in linear layers
for name, module in model.named_modules():
    if isinstance(module, torch.nn.Linear):
        prune.l1_unstructured(module, name='weight', amount=0.3)

# Make pruning permanent
for name, module in model.named_modules():
    if isinstance(module, torch.nn.Linear):
        prune.remove(module, 'weight')

# Save pruned model
torch.save(model, 'model_pruned.pt')

# Size reduction: 30% smaller
# Speed improvement: 1.5-2x faster
```

## Auto-Scaling

Scale serving infrastructure based on traffic.

### Kubernetes Horizontal Pod Autoscaler

```yaml
# hpa.yaml
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
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: inference_requests_per_second
      target:
        type: AverageValue
        averageValue: "100"
```

### Custom Metrics Auto-Scaling

```python
# custom_metrics.py
from prometheus_client import Gauge
import time

# Prometheus metric
queue_length = Gauge('inference_queue_length', 'Number of pending requests')

def monitor_queue():
    """Monitor queue and expose metric for HPA."""
    while True:
        pending_requests = get_queue_length()
        queue_length.set(pending_requests)
        time.sleep(5)

# HPA scales based on queue length
# If queue > 50, scale up
# If queue < 10, scale down
```

## Implementation Examples

### Example 1: FastAPI with Load Testing

```python
# fastapi_production.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.pyfunc
from prometheus_client import Counter, Histogram, make_asgi_app
import time

app = FastAPI()

# Prometheus metrics
predictions_counter = Counter('predictions_total', 'Total predictions')
latency_histogram = Histogram('prediction_latency_seconds', 'Prediction latency')
errors_counter = Counter('prediction_errors_total', 'Prediction errors')

# Load model
model = mlflow.pyfunc.load_model("models:/fraud_detection/Production")

class PredictionRequest(BaseModel):
    features: list[float]

class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    latency_ms: float

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    """Predict with monitoring."""

    start_time = time.time()

    try:
        # Validate input
        if len(request.features) != 10:
            raise HTTPException(status_code=400, detail="Expected 10 features")

        # Predict
        prediction = model.predict([request.features])[0]

        # Metrics
        latency = time.time() - start_time
        predictions_counter.inc()
        latency_histogram.observe(latency)

        return PredictionResponse(
            prediction=int(prediction),
            probability=float(prediction),
            latency_ms=latency * 1000
        )

    except Exception as e:
        errors_counter.inc()
        raise HTTPException(status_code=500, detail=str(e))

# Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy"}
```

**Load testing:**
```bash
# Install locust
pip install locust

# locustfile.py
from locust import HttpUser, task, between

class ModelUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def predict(self):
        self.client.post("/predict", json={
            "features": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        })

# Run load test
locust -f locustfile.py --host=http://localhost:8000 --users 100 --spawn-rate 10
```

### Example 2: Serverless Deployment (AWS Lambda)

```python
# lambda_handler.py
import json
import mlflow.pyfunc
import boto3

# Load model from S3
s3 = boto3.client('s3')
s3.download_file('ml-models', 'fraud_detection/model.pkl', '/tmp/model.pkl')

model = mlflow.pyfunc.load_model('/tmp/model.pkl')

def lambda_handler(event, context):
    """Lambda function handler."""

    # Extract features
    body = json.loads(event['body'])
    features = body['features']

    # Predict
    prediction = model.predict([features])[0]

    # Return response
    return {
        'statusCode': 200,
        'body': json.dumps({
            'prediction': int(prediction),
            'probability': float(prediction)
        })
    }
```

**Deploy:**
```bash
# Package dependencies
pip install -t package/ mlflow scikit-learn boto3

# Create deployment package
cd package
zip -r ../lambda_function.zip .
cd ..
zip -g lambda_function.zip lambda_handler.py

# Deploy to Lambda
aws lambda create-function \
  --function-name fraud-detection \
  --runtime python3.9 \
  --role arn:aws:iam::123456789:role/lambda-role \
  --handler lambda_handler.lambda_handler \
  --zip-file fileb://lambda_function.zip \
  --memory-size 1024 \
  --timeout 30
```

### Example 3: Multi-Model Serving

```python
# multi_model_serving.py
from fastapi import FastAPI
import mlflow.pyfunc

app = FastAPI()

# Load multiple models
models = {
    'fraud': mlflow.pyfunc.load_model("models:/fraud_detection/Production"),
    'churn': mlflow.pyfunc.load_model("models:/churn_prediction/Production"),
    'recommendation': mlflow.pyfunc.load_model("models:/product_recommendation/Production")
}

@app.post("/predict/{model_name}")
def predict(model_name: str, features: list[float]):
    """Multi-model prediction endpoint."""

    if model_name not in models:
        return {"error": f"Model '{model_name}' not found"}

    model = models[model_name]
    prediction = model.predict([features])[0]

    return {
        'model': model_name,
        'prediction': int(prediction)
    }

# Usage:
# POST /predict/fraud {"features": [1, 2, 3, ...]}
# POST /predict/churn {"features": [4, 5, 6, ...]}
```
