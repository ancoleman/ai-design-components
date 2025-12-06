# Golden Path Templates

## Table of Contents

1. [Template Design Principles](#template-design-principles)
2. [Full-Stack Web Application Template](#full-stack-web-application-template)
3. [Data Pipeline Template](#data-pipeline-template)
4. [Machine Learning Service Template](#machine-learning-service-template)
5. [Event-Driven Microservice Template](#event-driven-microservice-template)
6. [Scheduled Job Template](#scheduled-job-template)

## Template Design Principles

### The 80/20 Rule

Golden paths should cover 80% of use cases while providing clear escape hatches for the remaining 20%.

**Key Principles:**
- **Opinionated but flexible**: Make strong recommendations, allow overrides
- **Security by default**: Bake in security best practices (RBAC, network policies, scanning)
- **Observable from day one**: Include metrics, logging, tracing instrumentation
- **Production-ready**: Include all necessary configs (health checks, resource limits, monitoring)
- **Self-documenting**: Clear README, inline comments, architecture diagrams
- **Version-controlled**: Templates evolve, provide migration paths

### Template Anatomy

Every golden path template should include:

1. **Application Code**: Framework setup, boilerplate, example endpoints
2. **Infrastructure as Code**: Kubernetes manifests, Terraform modules
3. **CI/CD Pipeline**: Build, test, deploy automation
4. **Observability**: Metrics exporters, structured logging, tracing setup
5. **Security**: RBAC, network policies, secret references, scanning config
6. **Documentation**: README, runbooks, architecture diagrams

### Constraint Mechanisms

**Required (Hard Constraints):**
- Health check endpoints (liveness, readiness)
- Resource limits (CPU, memory)
- Security scanning (SAST, container scanning)
- Logging to stdout/stderr (structured JSON)

**Recommended (Soft Constraints):**
- Approved frameworks (Node.js, Python, Go preferred)
- Standard observability stack (Prometheus, Grafana)
- Naming conventions (kebab-case for services)

**Optional (Escape Hatches):**
- Custom middleware/libraries
- Alternative databases (must be from approved list)
- Advanced Kubernetes features (with platform team consultation)

## Full-Stack Web Application Template

### Use Case

Web application with backend API, database, and frontend (SPA or SSR).

### Technology Stack

**Backend:**
- Node.js + Express (or FastAPI for Python, Gin for Go)
- PostgreSQL database

**Frontend:**
- React (or Vue, Angular)
- Vite build tool

**Infrastructure:**
- Kubernetes deployment
- Ingress for routing
- Horizontal Pod Autoscaler

### Directory Structure

```
my-web-app/
├── catalog-info.yaml          # Backstage catalog metadata
├── README.md
├── backend/
│   ├── src/
│   │   ├── index.ts           # Entry point
│   │   ├── app.ts             # Express app
│   │   ├── routes/            # API routes
│   │   ├── models/            # Database models
│   │   └── middleware/        # Custom middleware
│   ├── package.json
│   ├── tsconfig.json
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   └── pages/
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
├── k8s/
│   ├── namespace.yaml
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── postgres.yaml          # Dev environment only
│   ├── ingress.yaml
│   └── hpa.yaml
├── .github/
│   └── workflows/
│       ├── backend-ci.yaml
│       └── frontend-ci.yaml
└── docs/
    ├── index.md               # TechDocs
    └── architecture.md
```

### Backend Example (Node.js + Express)

**src/index.ts:**
```typescript
import app from './app';
import { logger } from './utils/logger';

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  logger.info(`Server started on port ${PORT}`);
});
```

**src/app.ts:**
```typescript
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import promBundle from 'express-prom-bundle';
import { healthRouter } from './routes/health';
import { apiRouter } from './routes/api';
import { errorHandler } from './middleware/error';
import { requestLogger } from './middleware/logging';

const app = express();

// Security
app.use(helmet());
app.use(cors());

// Metrics (Prometheus)
const metricsMiddleware = promBundle({
  includeMethod: true,
  includePath: true,
  includeStatusCode: true,
  includeUp: true,
  customLabels: { service: 'my-web-app' },
  promClient: { collectDefaultMetrics: {} }
});
app.use(metricsMiddleware);

// Logging
app.use(requestLogger);

// Body parsing
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes
app.use('/health', healthRouter);
app.use('/api', apiRouter);

// Error handling
app.use(errorHandler);

export default app;
```

**Kubernetes Deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-web-app-backend
  labels:
    app: my-web-app
    component: backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: my-web-app
      component: backend
  template:
    metadata:
      labels:
        app: my-web-app
        component: backend
    spec:
      containers:
      - name: backend
        image: my-registry/my-web-app-backend:latest
        ports:
        - containerPort: 3000
          name: http
        - containerPort: 9090
          name: metrics
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: database-credentials
              key: url
        livenessProbe:
          httpGet:
            path: /health/liveness
            port: http
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/readiness
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

## Data Pipeline Template

### Use Case

ETL/ELT data processing pipeline with workflow orchestration.

### Technology Stack

- Workflow orchestrator: Apache Airflow (or Prefect, Dagster)
- Data connectors: S3, BigQuery, Snowflake, databases
- Data quality: Great Expectations or dbt tests
- Scheduling: Cron or orchestrator built-in

### Directory Structure

```
my-data-pipeline/
├── catalog-info.yaml
├── README.md
├── dags/
│   └── my_pipeline.py         # Airflow DAG
├── tasks/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── tests/
│   └── test_pipeline.py
├── k8s/
│   └── cronjob.yaml           # Alternative to Airflow
├── requirements.txt
└── Dockerfile
```

### Airflow DAG Example

**dags/my_pipeline.py:**
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime, timedelta
import logging

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'my_data_pipeline',
    default_args=default_args,
    description='Extract, transform, load data pipeline',
    schedule_interval='0 2 * * *',  # Daily at 2 AM
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['etl', 'production'],
)

def extract_data(**context):
    """Extract data from source"""
    logging.info("Extracting data from S3")
    s3_hook = S3Hook(aws_conn_id='aws_default')
    data = s3_hook.read_key('source-data/input.csv', bucket_name='my-bucket')
    # Process and return
    context['ti'].xcom_push(key='raw_data', value=data)

def transform_data(**context):
    """Transform data"""
    logging.info("Transforming data")
    raw_data = context['ti'].xcom_pull(key='raw_data')
    # Transformation logic
    transformed_data = raw_data  # Placeholder
    context['ti'].xcom_push(key='transformed_data', value=transformed_data)

def load_data(**context):
    """Load data to destination"""
    logging.info("Loading data to BigQuery")
    transformed_data = context['ti'].xcom_pull(key='transformed_data')
    # Load to BigQuery
    # ...

extract_task = PythonOperator(
    task_id='extract',
    python_callable=extract_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform',
    python_callable=transform_data,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load',
    python_callable=load_data,
    dag=dag,
)

extract_task >> transform_task >> load_task
```

## Machine Learning Service Template

### Use Case

ML model serving for inference (REST API).

### Technology Stack

- Model serving: FastAPI or TorchServe
- Model registry: MLflow or Weights & Biases
- Inference: GPU support (optional)
- Monitoring: Drift detection, performance metrics

### Directory Structure

```
my-ml-service/
├── catalog-info.yaml
├── README.md
├── src/
│   ├── main.py                # FastAPI app
│   ├── model_loader.py
│   ├── inference.py
│   └── monitoring.py
├── models/
│   └── model.pkl              # Serialized model
├── k8s/
│   ├── deployment.yaml        # With GPU resources
│   ├── service.yaml
│   └── hpa.yaml
├── requirements.txt
└── Dockerfile
```

### FastAPI Inference Example

**src/main.py:**
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, make_asgi_app
import numpy as np
import logging

from .model_loader import load_model
from .inference import predict
from .monitoring import track_prediction

app = FastAPI(title="ML Inference Service")

# Metrics
prediction_counter = Counter('predictions_total', 'Total predictions')
prediction_latency = Histogram('prediction_latency_seconds', 'Prediction latency')

# Load model at startup
model = load_model('models/model.pkl')

class PredictionRequest(BaseModel):
    features: list[float]

class PredictionResponse(BaseModel):
    prediction: float
    confidence: float

@app.get("/health/liveness")
async def liveness():
    return {"status": "alive"}

@app.get("/health/readiness")
async def readiness():
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "ready"}

@app.post("/predict", response_model=PredictionResponse)
async def predict_endpoint(request: PredictionRequest):
    with prediction_latency.time():
        try:
            result = predict(model, np.array(request.features))
            prediction_counter.inc()
            track_prediction(request.features, result)
            return PredictionResponse(
                prediction=result['value'],
                confidence=result['confidence']
            )
        except Exception as e:
            logging.error(f"Prediction error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

# Metrics endpoint for Prometheus
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
```

## Event-Driven Microservice Template

### Use Case

Service consuming/producing events via message broker (async architecture).

### Technology Stack

- Message broker: Kafka (or RabbitMQ, AWS SQS/SNS)
- Schema registry: Avro or Protobuf
- Consumer pattern: At-least-once or exactly-once delivery

### Kafka Consumer Example

**src/consumer.py:**
```python
from confluent_kafka import Consumer, KafkaException
from prometheus_client import Counter, Histogram
import json
import logging

# Metrics
messages_consumed = Counter('messages_consumed_total', 'Total messages consumed', ['topic'])
processing_latency = Histogram('message_processing_seconds', 'Message processing time')

consumer = Consumer({
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'my-consumer-group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False,
})

consumer.subscribe(['my-topic'])

def process_message(message):
    """Process individual message"""
    with processing_latency.time():
        try:
            data = json.loads(message.value().decode('utf-8'))
            # Business logic here
            logging.info(f"Processed message: {data}")
            messages_consumed.labels(topic=message.topic()).inc()
            return True
        except Exception as e:
            logging.error(f"Error processing message: {e}")
            return False

def run_consumer():
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())

            success = process_message(msg)
            if success:
                consumer.commit(asynchronous=False)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == '__main__':
    run_consumer()
```

## Scheduled Job Template

### Use Case

Cron jobs, batch processing, periodic tasks.

### Technology Stack

- Kubernetes CronJob (or external scheduler like Airflow)
- Execution timeout enforcement
- Success/failure notifications

### Kubernetes CronJob Example

**k8s/cronjob.yaml:**
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: my-scheduled-job
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  concurrencyPolicy: Forbid  # Don't run if previous job still running
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 3
  jobTemplate:
    spec:
      backoffLimit: 2  # Retry twice
      activeDeadlineSeconds: 3600  # Kill after 1 hour
      template:
        spec:
          containers:
          - name: job
            image: my-registry/my-job:latest
            env:
            - name: JOB_TYPE
              value: "daily-cleanup"
            resources:
              requests:
                memory: "512Mi"
                cpu: "250m"
              limits:
                memory: "1Gi"
                cpu: "500m"
          restartPolicy: OnFailure
```

**Job Script Example:**
```python
#!/usr/bin/env python3
import logging
import sys
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        logging.info("Starting scheduled job")

        # Job logic here
        logging.info("Processing data...")

        # Success
        logging.info("Job completed successfully")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Job failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
```

## Template Versioning and Migration

### Version Strategy

**Template Versions:**
- v1.0: Initial release
- v1.1: Minor improvements (backward compatible)
- v2.0: Breaking changes (require migration)

**Deprecation Policy:**
- Announce deprecation 6 months before removal
- Provide migration guide
- Support old versions during transition

### Migration Guide Example

**Migrating from v1.x to v2.0:**

**Breaking Changes:**
1. Health check paths changed: `/health` → `/health/liveness` and `/health/readiness`
2. Metrics endpoint moved: `/metrics` no longer included by default, add manually
3. Environment variable naming: `DB_HOST` → `DATABASE_HOST`

**Migration Steps:**
1. Update health check paths in Kubernetes manifests
2. Add metrics endpoint if needed
3. Update environment variable names
4. Test in development environment
5. Deploy to staging
6. Deploy to production with rollback plan
