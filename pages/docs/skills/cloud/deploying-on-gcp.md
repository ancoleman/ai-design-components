---
sidebar_position: 2
title: Deploying on GCP
description: Implement applications using Google Cloud Platform services
tags: [cloud, gcp, cloud-run, gke, bigquery, pub-sub, vertex-ai, google-cloud]
---

# Deploying on GCP

Build applications and infrastructure using Google Cloud Platform services with appropriate service selection, architecture patterns, and best practices.

## When to Use

Use this skill when:

- Selecting GCP compute services (Cloud Run, GKE, Cloud Functions, Compute Engine, App Engine)
- Choosing storage or database services (Cloud Storage, Cloud SQL, Spanner, Firestore, Bigtable, BigQuery)
- Designing data analytics pipelines (BigQuery, Pub/Sub, Dataflow, Dataproc, Composer)
- Implementing ML workflows (Vertex AI, AutoML, pre-trained APIs)
- Architecting network infrastructure (VPC, Load Balancing, CDN, Cloud Armor)
- Setting up IAM, security, and cost optimization
- Migrating from AWS or Azure to GCP
- Building multi-cloud or GCP-first architectures

## Key Features

### 1. Compute Service Selection

**Decision Framework:**

```
Need to run code in GCP?
├─ HTTP service?
│  ├─ YES → Stateless?
│  │  ├─ YES → Cloud Run (auto-scale to zero)
│  │  └─ NO → Need Kubernetes? → GKE | Compute Engine
│  └─ NO (Event-driven)
│     ├─ Simple function? → Cloud Functions
│     └─ Complex orchestration? → GKE | Cloud Run Jobs
```

**Selection Guide:**
- **First choice**: Cloud Run (unless state or Kubernetes required)
- **Need Kubernetes**: GKE Autopilot (managed) or Standard (full control)
- **Simple events**: Cloud Functions (60-min max execution)
- **Full control**: Compute Engine (VMs with custom configuration)

### 2. Database Service Selection

**Decision Matrix:**

```
Relational (SQL)
  ├─ Multi-region required? → Cloud Spanner
  ├─ PostgreSQL + high performance? → AlloyDB
  └─ Standard RDBMS → Cloud SQL (PostgreSQL/MySQL/SQL Server)

Document (NoSQL)
  ├─ Mobile/web with offline sync? → Firestore
  └─ Flexible schema, no offline? → MongoDB Atlas (Marketplace)

Key-Value
  ├─ Time-series or IoT data? → Bigtable
  └─ Caching layer? → Memorystore (Redis/Memcached)

Analytics
  └─ Petabyte-scale SQL analytics → BigQuery
```

### 3. GCP vs AWS vs Azure Service Mapping

| Category | GCP | AWS | Azure |
|----------|-----|-----|-------|
| **Serverless Containers** | Cloud Run | Fargate | Container Instances |
| **Kubernetes** | GKE | EKS | AKS |
| **Functions** | Cloud Functions | Lambda | Functions |
| **VMs** | Compute Engine | EC2 | Virtual Machines |
| **Object Storage** | Cloud Storage | S3 | Blob Storage |
| **SQL Database** | Cloud SQL | RDS | SQL Database |
| **NoSQL Document** | Firestore | DynamoDB | Cosmos DB |
| **Data Warehouse** | BigQuery | Redshift | Synapse |
| **Messaging** | Pub/Sub | SNS/SQS | Service Bus |
| **ML Platform** | Vertex AI | SageMaker | Machine Learning |

## Architecture Patterns

### Pattern 1: Serverless Web Application

**Use Case:** Stateless HTTP API with database and caching

**Architecture:**
```
Internet → Cloud Load Balancer → Cloud Run → Cloud SQL (PostgreSQL)
                                            → Memorystore (Redis)
                                            → Cloud Storage
```

**Key Services:**
- Cloud Run for API service (auto-scaling containers)
- Cloud SQL for transactional data
- Memorystore for caching
- Cloud Storage for file uploads

### Pattern 2: Data Analytics Platform

**Use Case:** Real-time event processing and analytics

**Architecture:**
```
Data Sources → Pub/Sub → Dataflow → BigQuery → Looker/Tableau
                          ↓
                     Cloud Storage (staging)
```

**Key Services:**
- Pub/Sub for event ingestion (at-least-once delivery)
- Dataflow for stream processing (Apache Beam)
- BigQuery for analytics (partitioned tables, clustering)
- Cloud Storage for staging and backups

### Pattern 3: ML Pipeline

**Use Case:** End-to-end machine learning workflow

**Architecture:**
```
Training Data (GCS) → Vertex AI Training → Model Registry → Vertex AI Endpoints
                                                              ↓
                                                         Predictions
```

**Key Services:**
- Vertex AI Workbench for notebook development
- Vertex AI Training for custom models (GPU/TPU support)
- Vertex AI Endpoints for model serving (auto-scaling)
- Vertex AI Pipelines for orchestration (Kubeflow)

### Pattern 4: GKE Microservices Platform

**Use Case:** Complex orchestration with multiple services

**Architecture:**
```
Internet → Cloud Load Balancer → GKE Cluster
                                   ├─ Ingress Controller
                                   ├─ Service Mesh (optional)
                                   ├─ Microservice A
                                   ├─ Microservice B
                                   └─ Microservice C
```

**Key Features:**
- GKE Autopilot (fully managed nodes) or Standard (custom configuration)
- Workload Identity for secure GCP service access
- Private cluster with Private Google Access
- Config Connector for managing GCP resources via Kubernetes

## Best Practices

### Cost Optimization

**Compute:**
- Use Committed Use Discounts for predictable workloads (57% off)
- Use Spot VMs for fault-tolerant workloads (60-91% off)
- Cloud Run scales to zero when idle (no charges)
- GKE Autopilot charges only for pod resources, not nodes

**Storage:**
- Use appropriate Cloud Storage classes (Standard/Nearline/Coldline/Archive)
- Enable Object Lifecycle Management to transition cold data
- Archive backups with Coldline or Archive (99% cheaper than Standard)

**Data:**
- BigQuery: Use partitioned and clustered tables
- Query only needed columns (avoid `SELECT *`)
- Use BI Engine for caching (up to 10TB free)
- Consider flat-rate pricing for heavy BigQuery usage

### Security Fundamentals

**IAM Best Practices:**
- Follow principle of least privilege
- Use service accounts, not user accounts for applications
- Enable Workload Identity for GKE workloads (no service account keys)
- Use Secret Manager for secrets, not environment variables

**Network Security:**
- Use Private Google Access (access GCP services without public IPs)
- Enable Cloud NAT for outbound internet from private instances
- Implement VPC Service Controls for data exfiltration protection
- Use Identity-Aware Proxy (IAP) for zero-trust access

**Data Security:**
- Enable encryption at rest (default) and in transit
- Use Customer-Managed Encryption Keys (CMEK) for sensitive data
- Implement VPC Service Controls perimeter for data protection
- Enable audit logging for all projects

### High Availability

**Multi-Region Strategy:**
- Cloud Storage: Use multi-region locations (US, EU, ASIA)
- Cloud SQL: Enable Regional HA (automatic failover)
- Cloud Spanner: Use multi-region configurations (99.999% SLA)
- Global Load Balancing: Route traffic to nearest healthy backend

**Backup and Disaster Recovery:**
- Cloud SQL: Enable automated backups and point-in-time recovery
- Persistent Disk: Schedule snapshot backups
- Cloud Storage: Enable versioning for critical data
- BigQuery: Use table snapshots for time travel

## Quick Start

### Deploy Cloud Run Service
```bash
# Deploy from source
gcloud run deploy SERVICE_NAME \
  --image IMAGE_URL \
  --region REGION \
  --allow-unauthenticated
```

### Create GKE Autopilot Cluster
```bash
# Create cluster
gcloud container clusters create-auto CLUSTER_NAME \
  --region REGION

# Get credentials
gcloud container clusters get-credentials CLUSTER_NAME \
  --region REGION
```

### Python SDK Examples

**Cloud Storage:**
```python
from google.cloud import storage
client = storage.Client()
bucket = client.bucket('my-bucket')
blob = bucket.blob('file.txt')
blob.upload_from_filename('local-file.txt')
```

**BigQuery:**
```python
from google.cloud import bigquery
client = bigquery.Client()
query = "SELECT * FROM `project.dataset.table` LIMIT 10"
results = client.query(query).result()
```

**Pub/Sub:**
```python
from google.cloud import pubsub_v1
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('project', 'topic-name')
future = publisher.publish(topic_path, b'message data')
```

### Terraform Quick Start

```hcl
# Provider configuration
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = "my-project-id"
  region  = "us-central1"
}

# Cloud Run service
resource "google_cloud_run_service" "api" {
  name     = "api-service"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "gcr.io/project/api:latest"
      }
    }
  }
}
```

## Service Selection Cheatsheet

| Requirement | Recommended Service | Alternative |
|-------------|---------------------|-------------|
| Stateless HTTP API | Cloud Run | App Engine |
| Complex orchestration | GKE Autopilot | GKE Standard |
| Event processing | Cloud Functions | Cloud Run Jobs |
| Object storage | Cloud Storage | N/A |
| Relational database | Cloud SQL | AlloyDB, Spanner |
| NoSQL document | Firestore | MongoDB Atlas |
| Time-series data | Bigtable | N/A |
| Data warehouse | BigQuery | N/A |
| Message queue | Pub/Sub | N/A |
| Stream processing | Dataflow | Dataproc |
| Batch processing | Dataflow | Dataproc |
| ML training | Vertex AI | Custom on GKE |
| Caching | Memorystore Redis | N/A |

## Cost Optimization Tactics

### GCP-Specific Optimizations

1. **Export Billing to BigQuery**: Custom cost analysis with SQL
2. **Sustained Use Discounts**: Automatic 20-30% discount (no commitment)
3. **Committed Use Discounts**: 52-70% savings for 3-year commitments
4. **Preemptible VMs**: Up to 91% discount for batch workloads
5. **GCP Recommender**: Idle VM detection and rightsizing advice

### Multi-Region Recommendations

- Production workloads: Use multi-region for 99.95%+ SLA
- Cloud Storage: Multi-region for global access
- Cloud Spanner: Multi-region for global transactions
- Global Load Balancing: Route to nearest healthy backend

## GCP's Unique Advantages

**When choosing GCP:**
- Data analytics workloads (BigQuery is best-in-class)
- ML/AI applications (Vertex AI, TPUs, Google Research backing)
- Kubernetes-native applications (GKE invented by Kubernetes creators)
- Serverless containers (Cloud Run is mature and cost-effective)
- Real-time streaming (Pub/Sub + Dataflow)

**Differentiators:**
- BigQuery: Serverless, petabyte-scale, fastest data warehouse
- Cloud Run: Most mature serverless container platform
- GKE: Most advanced managed Kubernetes (Autopilot mode)
- Vertex AI: Unified ML platform (training, deployment, monitoring)
- Per-second billing and sustained use discounts (automatic cost savings)

## Related Skills

- **writing-infrastructure-code**: Use Terraform to provision GCP resources
- **operating-kubernetes**: Deploy and manage applications on GKE
- **building-ci-pipelines**: Use Cloud Build for CI/CD to Cloud Run or GKE
- **managing-secrets**: Use Secret Manager for sensitive configuration
- **implementing-observability**: Use Cloud Monitoring and Cloud Logging
- **architecting-data**: Design data lakes and warehouses using BigQuery
- **implementing-mlops**: Implement ML pipelines using Vertex AI
- **deploying-on-aws**: Compare AWS and GCP service equivalents
- **deploying-on-azure**: Compare Azure and GCP service equivalents

## References

- Full skill documentation: `/skills/deploying-on-gcp/SKILL.md`
- Compute services: `/skills/deploying-on-gcp/references/compute-services.md`
- Storage & databases: `/skills/deploying-on-gcp/references/storage-databases.md`
- Data analytics: `/skills/deploying-on-gcp/references/data-analytics.md`
- ML/AI services: `/skills/deploying-on-gcp/references/ml-ai-services.md`
- Networking: `/skills/deploying-on-gcp/references/networking.md`
- Security & IAM: `/skills/deploying-on-gcp/references/security-iam.md`
- Cost optimization: `/skills/deploying-on-gcp/references/cost-optimization.md`
