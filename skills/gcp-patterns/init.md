# GCP Patterns Skill - Master Plan

**Skill Name:** `gcp-patterns`
**Skill Level:** Mid Level (Implementation Patterns, 500-800 tokens)
**Status:** Planning Phase (init.md complete, SKILL.md to be created)
**Last Updated:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [GCP Service Taxonomy](#gcp-service-taxonomy)
5. [Decision Frameworks](#decision-frameworks)
6. [Implementation Patterns](#implementation-patterns)
7. [Multi-Language Support](#multi-language-support)
8. [Best Practices](#best-practices)
9. [Library Recommendations](#library-recommendations)
10. [Skill Structure Design](#skill-structure-design)
11. [Integration Points](#integration-points)
12. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why GCP Patterns Matter

Google Cloud Platform (GCP) has distinct advantages in data analytics, machine learning, Kubernetes, and serverless computing. As organizations increasingly adopt multi-cloud strategies and AI/ML workloads, GCP expertise becomes critical.

**Market Drivers:**
- **Data & Analytics Leadership:** BigQuery is the gold standard for cloud data warehousing
- **AI/ML Innovation:** Vertex AI, TPUs, and AutoML lead the industry
- **Kubernetes Native:** GKE invented by Kubernetes creators
- **Serverless Maturity:** Cloud Run offers best-in-class container serverless
- **Multi-Cloud Reality:** 76% of enterprises use GCP alongside AWS/Azure

**Strategic Value:**
1. **Data-First Architecture:** Best choice for analytics-heavy workloads
2. **ML/AI Workloads:** Industry-leading AI services and infrastructure
3. **Container Orchestration:** GKE offers most mature Kubernetes experience
4. **Cost Optimization:** Per-second billing, sustained use discounts
5. **Global Infrastructure:** Premium network tier for low-latency global apps

### GCP's Unique Strengths

**Compared to AWS:**
- Superior data analytics (BigQuery vs Redshift)
- Better Kubernetes integration (GKE vs EKS)
- Simpler pricing model
- Stronger ML/AI capabilities (Vertex AI vs SageMaker)

**Compared to Azure:**
- More open-source friendly
- Better for containerized workloads
- Superior data engineering tools
- Stronger AI research backing (Google Research, DeepMind)

### When to Choose GCP

**Primary Use Cases:**
1. **Data Analytics & BI:** BigQuery for petabyte-scale analytics
2. **Machine Learning:** Vertex AI for end-to-end ML pipelines
3. **Containerized Apps:** GKE for production Kubernetes
4. **Serverless Containers:** Cloud Run for stateless services
5. **Real-time Streaming:** Pub/Sub + Dataflow for event processing

---

## Skill Purpose and Scope

### What This Skill Teaches

**Core Competencies:**

1. **Compute Service Selection**
   - Cloud Run (serverless containers)
   - GKE (managed Kubernetes)
   - Cloud Functions (event-driven functions)
   - Compute Engine (VMs)
   - App Engine (PaaS)

2. **Storage & Database Strategy**
   - Cloud Storage (object storage)
   - Cloud SQL (managed PostgreSQL/MySQL)
   - Cloud Spanner (global distributed SQL)
   - Firestore (NoSQL document DB)
   - Bigtable (wide-column NoSQL)
   - AlloyDB (PostgreSQL-compatible)

3. **Data & Analytics Platform**
   - BigQuery (data warehouse)
   - Pub/Sub (messaging)
   - Dataflow (stream/batch processing)
   - Dataproc (managed Spark/Hadoop)
   - Composer (managed Airflow)

4. **AI/ML Services**
   - Vertex AI (unified ML platform)
   - AutoML (no-code ML)
   - AI Platform Notebooks (Jupyter)
   - TPUs (ML accelerators)

5. **Networking & Security**
   - VPC design patterns
   - Cloud Load Balancing
   - Cloud CDN
   - Cloud Armor (WAF)
   - Identity-Aware Proxy (IAP)

### What This Skill Does NOT Cover

- Infrastructure as Code syntax (use `infrastructure-as-code` skill)
- Kubernetes operations (use `kubernetes-operations` skill)
- CI/CD pipelines (use `building-ci-pipelines` skill)
- Security hardening details (use `security-hardening` skill)
- AWS or Azure specifics (use `aws-patterns`, `azure-patterns` skills)

---

## Research Findings

### GCP Architecture Best Practices (2025)

**Key Trends:**
1. **Cloud Run Dominance:** Fastest-growing compute service for stateless apps
2. **BigQuery Lakehouse:** Blending data warehouse and data lake patterns
3. **Vertex AI Adoption:** Consolidating ML workloads onto unified platform
4. **Workload Identity:** Modern authentication for GKE workloads
5. **Multi-Region Redundancy:** Critical for production workloads

### Service Maturity Matrix

| Service | Maturity | Adoption | Best For |
|---------|----------|----------|----------|
| **Cloud Run** | High | Growing Fast | Stateless containers |
| **GKE** | Very High | Established | Complex orchestration |
| **BigQuery** | Very High | Dominant | Data warehousing |
| **Vertex AI** | High | Growing | ML pipelines |
| **Cloud Spanner** | High | Niche | Global transactions |
| **Firestore** | High | Growing | Mobile/web apps |
| **Pub/Sub** | Very High | Established | Event streaming |
| **Cloud Storage** | Very High | Universal | Object storage |

### GCP vs AWS vs Azure: Service Mapping

| Category | GCP | AWS | Azure |
|----------|-----|-----|-------|
| **VMs** | Compute Engine | EC2 | Virtual Machines |
| **Serverless Containers** | Cloud Run | Fargate | Container Instances |
| **Kubernetes** | GKE | EKS | AKS |
| **Functions** | Cloud Functions | Lambda | Functions |
| **Object Storage** | Cloud Storage | S3 | Blob Storage |
| **SQL Database** | Cloud SQL | RDS | SQL Database |
| **NoSQL Document** | Firestore | DynamoDB | Cosmos DB |
| **Data Warehouse** | BigQuery | Redshift | Synapse |
| **Messaging** | Pub/Sub | SNS/SQS | Service Bus |
| **ML Platform** | Vertex AI | SageMaker | Machine Learning |

---

## GCP Service Taxonomy

### Compute Services (5 Options)

#### 1. Cloud Run (Serverless Containers)
**When to Use:**
- Stateless HTTP services
- Microservices architecture
- Variable traffic patterns
- No infrastructure management desired

**Characteristics:**
- Auto-scaling to zero
- Pay per request
- Built-in HTTPS
- Concurrency control

**Example Use Cases:**
- REST APIs
- Web backends
- Webhooks
- Scheduled jobs (Cloud Run Jobs)

#### 2. Google Kubernetes Engine (GKE)
**When to Use:**
- Complex orchestration needs
- Stateful applications
- Multi-service deployments
- Kubernetes expertise available

**Characteristics:**
- Full Kubernetes API
- Node auto-provisioning
- Workload Identity
- Multi-cluster management

**Example Use Cases:**
- Microservices platforms
- ML model serving
- Database clusters
- Stateful applications

#### 3. Cloud Functions (FaaS)
**When to Use:**
- Event-driven processing
- Simple single-purpose functions
- Tight GCP service integration
- No containerization needed

**Characteristics:**
- Multiple language runtimes
- Automatic scaling
- Event triggers
- Short execution time (up to 60 min)

**Example Use Cases:**
- Cloud Storage triggers
- Pub/Sub event handlers
- HTTP webhooks
- Scheduled tasks

#### 4. Compute Engine (IaaS)
**When to Use:**
- Full OS control required
- Legacy application migration
- GPU/TPU access needed
- Custom networking requirements

**Characteristics:**
- Customizable VMs
- Persistent disks
- Load balancing
- Auto-scaling groups

**Example Use Cases:**
- Lift-and-shift migrations
- Windows workloads
- High-performance computing
- Gaming servers

#### 5. App Engine (PaaS)
**When to Use:**
- Simple web applications
- Automatic scaling desired
- Legacy App Engine apps
- Standard runtime requirements met

**Characteristics:**
- Automatic scaling
- Traffic splitting
- Integrated services
- Standard and Flexible environments

**Example Use Cases:**
- Web applications
- Mobile backends
- Simple APIs
- Internal tools

### Storage Services (6 Options)

#### 1. Cloud Storage (Object Storage)
**When to Use:**
- Unstructured data (files, media, backups)
- Static website hosting
- Data lake foundation
- Archival storage

**Storage Classes:**
- **Standard:** Hot data, frequent access
- **Nearline:** Once per month access
- **Coldline:** Once per quarter access
- **Archive:** Once per year access

**Example Use Cases:**
- Media storage (images, videos)
- Backup and disaster recovery
- Data lake storage
- Static website hosting

#### 2. Persistent Disk
**When to Use:**
- Block storage for VMs
- Database storage
- High IOPS requirements
- Snapshotting needed

**Types:**
- **Standard (HDD):** Cost-effective
- **SSD:** High performance
- **Extreme:** Highest IOPS

#### 3. Filestore (NFS)
**When to Use:**
- Shared file systems
- Legacy app migration
- Media rendering
- Development environments

### Database Services (6 Options)

#### 1. Cloud SQL (Managed Relational)
**When to Use:**
- Traditional RDBMS needs
- PostgreSQL/MySQL/SQL Server apps
- Regional deployment
- Up to 96 TB storage

**Characteristics:**
- Automatic backups
- High availability
- Read replicas
- Point-in-time recovery

**Example Use Cases:**
- OLTP applications
- CMS backends
- E-commerce platforms
- Internal tools

#### 2. Cloud Spanner (Global SQL)
**When to Use:**
- Global transactions required
- Strong consistency needed
- Multi-region active-active
- Unlimited scale

**Characteristics:**
- 99.999% availability SLA
- Global transactions
- Horizontal scaling
- SQL interface

**Example Use Cases:**
- Financial systems
- Global inventory management
- Gaming leaderboards
- Supply chain tracking

#### 3. Firestore (NoSQL Document)
**When to Use:**
- Mobile/web applications
- Real-time synchronization
- Offline support needed
- Flexible schema

**Characteristics:**
- Real-time listeners
- Offline persistence
- Automatic indexing
- Client SDKs (Web, iOS, Android)

**Example Use Cases:**
- Mobile apps
- Real-time dashboards
- Collaborative tools
- Gaming state management

#### 4. Bigtable (Wide-Column NoSQL)
**When to Use:**
- Time-series data
- IoT sensor data
- Financial tick data
- High throughput (>1M ops/sec)

**Characteristics:**
- Petabyte scale
- Single-digit ms latency
- HBase API compatible
- Automatic replication

**Example Use Cases:**
- Time-series analytics
- IoT data ingestion
- AdTech real-time bidding
- Financial trading systems

#### 5. AlloyDB (PostgreSQL-Compatible)
**When to Use:**
- PostgreSQL migration from on-prem
- Demanding transactional workloads
- Analytical queries on transactional data
- Need for better performance than Cloud SQL

**Characteristics:**
- 4x faster than PostgreSQL
- Columnar engine for analytics
- Machine learning integration
- PostgreSQL compatibility

#### 6. Memorystore (In-Memory Cache)
**When to Use:**
- Application caching
- Session storage
- Real-time analytics
- Leaderboards

**Options:**
- **Redis:** Advanced data structures
- **Memcached:** Simple key-value

### Data & Analytics Services (5 Options)

#### 1. BigQuery (Data Warehouse)
**When to Use:**
- Petabyte-scale analytics
- SQL-based data analysis
- Business intelligence
- Data science workloads

**Characteristics:**
- Serverless (no infrastructure)
- Columnar storage
- Federated queries
- ML integration (BigQuery ML)

**Example Use Cases:**
- Data warehousing
- Log analytics
- Ad-hoc analysis
- Predictive analytics

#### 2. Pub/Sub (Messaging)
**When to Use:**
- Event-driven architectures
- Microservices communication
- Real-time event processing
- Decoupling services

**Characteristics:**
- At-least-once delivery
- Global message ordering
- Dead letter queues
- Push and pull subscriptions

**Example Use Cases:**
- Event streaming
- IoT data ingestion
- Log aggregation
- Workflow orchestration

#### 3. Dataflow (Stream/Batch Processing)
**When to Use:**
- ETL/ELT pipelines
- Stream processing
- Batch processing
- Data transformations

**Characteristics:**
- Apache Beam SDK
- Unified batch and streaming
- Auto-scaling
- Exactly-once processing

**Example Use Cases:**
- Real-time analytics
- Data transformations
- Fraud detection
- Recommendation systems

#### 4. Dataproc (Managed Spark/Hadoop)
**When to Use:**
- Existing Spark/Hadoop workloads
- Big data batch processing
- Data science with Spark
- Migration from on-prem Hadoop

**Characteristics:**
- Fast cluster provisioning (90 seconds)
- Autoscaling
- Integration with GCS
- Pre-installed ecosystem tools

#### 5. Cloud Composer (Managed Airflow)
**When to Use:**
- Workflow orchestration
- Data pipeline management
- Scheduled data processing
- Complex dependencies

**Characteristics:**
- Fully managed Airflow
- Python-based DAGs
- Integration with GCP services
- Monitoring and logging

### AI/ML Services (4 Tiers)

#### 1. Vertex AI (Unified ML Platform)
**When to Use:**
- End-to-end ML workflows
- Custom model training
- Model deployment and monitoring
- MLOps required

**Capabilities:**
- Workbench (Jupyter notebooks)
- Training (custom and AutoML)
- Prediction serving
- Pipelines (Kubeflow)
- Feature Store
- Model Monitoring

#### 2. AutoML (No-Code ML)
**When to Use:**
- Limited ML expertise
- Standard ML tasks
- Quick prototyping
- Domain-specific models

**Services:**
- AutoML Vision (image classification)
- AutoML Natural Language (text)
- AutoML Tables (structured data)
- AutoML Video (video analysis)

#### 3. Pre-Trained APIs (Zero-Code ML)
**When to Use:**
- Common ML tasks
- No training needed
- Quick integration
- Pay-per-use

**APIs:**
- Vision API (image analysis)
- Natural Language API (text analysis)
- Speech-to-Text / Text-to-Speech
- Translation API
- Video Intelligence API

#### 4. TPUs (ML Accelerators)
**When to Use:**
- Large-scale model training
- Transformer models (BERT, GPT)
- Research workloads
- Cost optimization for training

### Networking Services (5 Core Areas)

#### 1. VPC (Virtual Private Cloud)
**Patterns:**
- **Shared VPC:** Centralized networking
- **VPC Peering:** Connect VPCs
- **Private Google Access:** Access GCP services without internet
- **Cloud NAT:** Outbound internet for private instances

#### 2. Cloud Load Balancing
**Types:**
- **Global HTTP(S):** Multi-region web apps
- **Global SSL Proxy:** Non-HTTP traffic
- **Regional Network:** TCP/UDP within region
- **Internal:** Private load balancing

#### 3. Cloud CDN
**When to Use:**
- Static content distribution
- Global audience
- Reduce origin load
- Improve latency

#### 4. Cloud Armor (WAF)
**When to Use:**
- DDoS protection
- WAF rules
- Adaptive protection
- Rate limiting

#### 5. Identity-Aware Proxy (IAP)
**When to Use:**
- Zero-trust access
- No VPN required
- Context-aware access
- BeyondCorp model

---

## Decision Frameworks

### Framework 1: Compute Service Selection

```
START: Need to run code in GCP
  │
  ├─► HTTP service?
  │     YES ──► Stateless?
  │               YES ──► Traffic predictable?
  │                         YES ──► App Engine
  │                         NO  ──► Cloud Run (auto-scale to zero)
  │               NO  ──► Need Kubernetes?
  │                         YES ──► GKE
  │                         NO  ──► Compute Engine
  │
  └─► NO (Event-driven)
        │
        ├─► Simple function?
        │     YES ──► Cloud Functions
        │
        └─► Complex orchestration?
              YES ──► GKE
              NO  ──► Cloud Run Jobs
```

**Rule of Thumb:**
- **First choice:** Cloud Run (unless you need state/Kubernetes)
- **Need Kubernetes:** GKE
- **Simple events:** Cloud Functions
- **Full control:** Compute Engine

### Framework 2: Database Selection

```
START: Need database
  │
  ├─► Data model?
  │     ├─► Relational ──► Multi-region?
  │     │                   YES ──► Cloud Spanner
  │     │                   NO  ──► Need >4TB?
  │     │                           YES ──► AlloyDB (if PostgreSQL) or Spanner
  │     │                           NO  ──► Cloud SQL
  │     │
  │     ├─► Document ──► Mobile/web with offline?
  │     │                 YES ──► Firestore
  │     │                 NO  ──► MongoDB Atlas (marketplace)
  │     │
  │     ├─► Key-Value ──► Time-series/IoT?
  │     │                 YES ──► Bigtable
  │     │                 NO  ──► Memorystore (Redis)
  │     │
  │     └─► Graph ──► Neo4j (marketplace) or BigQuery (analysis)
```

### Framework 3: Storage Selection

```
START: Need storage
  │
  ├─► Data type?
  │     ├─► Objects/Files ──► Access pattern?
  │     │                      ├─► Frequent ──► Cloud Storage (Standard)
  │     │                      ├─► Monthly ──► Cloud Storage (Nearline)
  │     │                      ├─► Quarterly ──► Cloud Storage (Coldline)
  │     │                      └─► Yearly ──► Cloud Storage (Archive)
  │     │
  │     ├─► Block storage ──► Persistent Disk (SSD or Standard)
  │     │
  │     └─► Shared filesystem ──► Filestore (NFS)
```

### Framework 4: Data Processing Selection

```
START: Need to process data
  │
  ├─► Data size?
  │     ├─► Petabyte-scale analytics ──► BigQuery
  │     │
  │     ├─► Real-time streaming ──► Pub/Sub + Dataflow
  │     │
  │     ├─► Batch processing ──► Existing Spark?
  │     │                         YES ──► Dataproc
  │     │                         NO  ──► Dataflow
  │     │
  │     └─► Workflow orchestration ──► Cloud Composer
```

### Framework 5: ML/AI Service Selection

```
START: Need ML capability
  │
  ├─► Have labeled data?
  │     NO ──► Pre-trained API (Vision, NLP, etc.)
  │     │
  │     YES ──► ML expertise?
  │              LOW ──► AutoML
  │              MED ──► Vertex AI (AutoML + custom)
  │              HIGH ──► Vertex AI (custom training)
  │                       │
  │                       └─► Large models? ──► TPUs
```

---

## Implementation Patterns

### Pattern 1: Serverless Web Application (Cloud Run)

**Architecture:**
```
Internet → Cloud Load Balancer → Cloud Run → Cloud SQL
                                            → Cloud Storage
                                            → Memorystore (Redis)
```

**Terraform Example:**
```hcl
# Cloud Run service
resource "google_cloud_run_service" "api" {
  name     = "api-service"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "gcr.io/project/api:latest"

        resources {
          limits = {
            cpu    = "2"
            memory = "1Gi"
          }
        }

        env {
          name  = "DATABASE_URL"
          value = google_sql_database_instance.main.connection_name
        }
      }

      # Concurrency control
      container_concurrency = 80

      # Service account for Workload Identity
      service_account_name = google_service_account.api.email
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale" = "1"
        "autoscaling.knative.dev/maxScale" = "100"
        "run.googleapis.com/cloudsql-instances" = google_sql_database_instance.main.connection_name
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Cloud SQL instance
resource "google_sql_database_instance" "main" {
  name             = "main-db"
  database_version = "POSTGRES_15"
  region           = "us-central1"

  settings {
    tier = "db-custom-2-8192"

    backup_configuration {
      enabled    = true
      start_time = "03:00"
    }

    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.main.id
    }
  }
}

# Allow public access to Cloud Run
data "google_iam_policy" "noauth" {
  binding {
    role    = "roles/run.invoker"
    members = ["allUsers"]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location = google_cloud_run_service.api.location
  service  = google_cloud_run_service.api.name
  policy_data = data.google_iam_policy.noauth.policy_data
}
```

**Python Client Example (google-cloud-run):**
```python
from google.cloud import run_v2

client = run_v2.ServicesClient()

# Deploy Cloud Run service
service = run_v2.Service()
service.name = "projects/PROJECT_ID/locations/us-central1/services/api"

container = run_v2.Container()
container.image = "gcr.io/project/api:latest"
container.resources.limits = {"cpu": "2", "memory": "1Gi"}

service.template.containers = [container]
service.template.scaling.min_instance_count = 1
service.template.scaling.max_instance_count = 100

request = run_v2.CreateServiceRequest(
    parent="projects/PROJECT_ID/locations/us-central1",
    service=service,
    service_id="api"
)

operation = client.create_service(request=request)
response = operation.result()
```

### Pattern 2: GKE Microservices Platform

**Architecture:**
```
Internet → Cloud Load Balancer → GKE Cluster
                                    ├─► Frontend (Cloud Run on GKE)
                                    ├─► API Gateway
                                    ├─► Service A (GKE workload)
                                    ├─► Service B (GKE workload)
                                    └─► Service C (GKE workload)
```

**Terraform Example:**
```hcl
# GKE cluster with Autopilot
resource "google_container_cluster" "primary" {
  name     = "gke-cluster"
  location = "us-central1"

  # Enable Autopilot
  enable_autopilot = true

  # Release channel
  release_channel {
    channel = "REGULAR"
  }

  # Workload Identity
  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  # Private cluster
  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = false
    master_ipv4_cidr_block  = "172.16.0.0/28"
  }

  # Master authorized networks
  master_authorized_networks_config {
    cidr_blocks {
      cidr_block   = "10.0.0.0/8"
      display_name = "internal"
    }
  }
}

# For standard GKE (non-Autopilot)
resource "google_container_node_pool" "primary_nodes" {
  name       = "primary-node-pool"
  location   = "us-central1"
  cluster    = google_container_cluster.primary.name
  node_count = 1

  autoscaling {
    min_node_count = 1
    max_node_count = 10
  }

  node_config {
    preemptible  = false
    machine_type = "e2-medium"

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    workload_metadata_config {
      mode = "GKE_METADATA"
    }
  }
}
```

**gcloud CLI Commands:**
```bash
# Create GKE Autopilot cluster
gcloud container clusters create-auto gke-cluster \
  --region=us-central1 \
  --release-channel=regular

# Get credentials
gcloud container clusters get-credentials gke-cluster \
  --region=us-central1

# Deploy application
kubectl apply -f k8s/

# Enable Config Connector (manage GCP resources via K8s)
gcloud container clusters update gke-cluster \
  --update-addons ConfigConnector=ENABLED \
  --region=us-central1
```

### Pattern 3: Data Analytics Platform (BigQuery + Dataflow)

**Architecture:**
```
Data Sources → Pub/Sub → Dataflow → BigQuery → Looker/Tableau
                           ↓
                      Cloud Storage (staging)
```

**Terraform Example:**
```hcl
# BigQuery dataset
resource "google_bigquery_dataset" "analytics" {
  dataset_id    = "analytics"
  friendly_name = "Analytics Dataset"
  location      = "US"

  default_table_expiration_ms = 3600000  # 1 hour

  labels = {
    env = "production"
  }
}

# BigQuery table with schema
resource "google_bigquery_table" "events" {
  dataset_id = google_bigquery_dataset.analytics.dataset_id
  table_id   = "events"

  time_partitioning {
    type  = "DAY"
    field = "event_timestamp"
  }

  clustering = ["user_id", "event_type"]

  schema = jsonencode([
    {
      name = "event_id"
      type = "STRING"
      mode = "REQUIRED"
    },
    {
      name = "event_timestamp"
      type = "TIMESTAMP"
      mode = "REQUIRED"
    },
    {
      name = "user_id"
      type = "STRING"
      mode = "REQUIRED"
    },
    {
      name = "event_type"
      type = "STRING"
      mode = "REQUIRED"
    },
    {
      name = "properties"
      type = "JSON"
      mode = "NULLABLE"
    }
  ])
}

# Pub/Sub topic
resource "google_pubsub_topic" "events" {
  name = "events-topic"

  schema_settings {
    schema   = google_pubsub_schema.events.id
    encoding = "JSON"
  }
}

# Pub/Sub subscription
resource "google_pubsub_subscription" "events_pull" {
  name  = "events-pull"
  topic = google_pubsub_topic.events.name

  ack_deadline_seconds = 20

  message_retention_duration = "604800s"  # 7 days

  retry_policy {
    minimum_backoff = "10s"
    maximum_backoff = "600s"
  }
}

# Dataflow job (requires template)
resource "google_dataflow_job" "stream_events" {
  name              = "stream-events"
  template_gcs_path = "gs://dataflow-templates/latest/PubSub_to_BigQuery"
  temp_gcs_location = "gs://${google_storage_bucket.dataflow_temp.name}/temp"

  parameters = {
    inputTopic      = google_pubsub_topic.events.id
    outputTableSpec = "${var.project_id}:${google_bigquery_dataset.analytics.dataset_id}.${google_bigquery_table.events.table_id}"
  }
}
```

**Python BigQuery Client Example:**
```python
from google.cloud import bigquery
from datetime import datetime, timedelta

# Initialize client
client = bigquery.Client()

# Query with parameters
query = """
    SELECT
        event_type,
        COUNT(*) as event_count,
        COUNT(DISTINCT user_id) as unique_users
    FROM `project.analytics.events`
    WHERE event_timestamp >= @start_time
        AND event_timestamp < @end_time
    GROUP BY event_type
    ORDER BY event_count DESC
"""

job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter(
            "start_time",
            "TIMESTAMP",
            datetime.now() - timedelta(days=7)
        ),
        bigquery.ScalarQueryParameter(
            "end_time",
            "TIMESTAMP",
            datetime.now()
        ),
    ]
)

# Run query
query_job = client.query(query, job_config=job_config)
results = query_job.result()

for row in results:
    print(f"{row.event_type}: {row.event_count} events, {row.unique_users} users")

# Streaming insert
rows_to_insert = [
    {
        "event_id": "evt_123",
        "event_timestamp": datetime.now().isoformat(),
        "user_id": "user_456",
        "event_type": "page_view",
        "properties": {"page": "/home"}
    }
]

errors = client.insert_rows_json(
    "project.analytics.events",
    rows_to_insert
)

if errors:
    print(f"Errors: {errors}")
```

### Pattern 4: ML Pipeline (Vertex AI)

**Architecture:**
```
Training Data (GCS) → Vertex AI Training → Model Registry → Vertex AI Endpoints
                                                               ↓
                                                          Predictions
```

**Python Vertex AI Example:**
```python
from google.cloud import aiplatform
from google.cloud.aiplatform import gapic

# Initialize Vertex AI
aiplatform.init(
    project="my-project",
    location="us-central1",
    staging_bucket="gs://my-bucket"
)

# Create custom training job
job = aiplatform.CustomTrainingJob(
    display_name="my-training-job",
    script_path="train.py",
    container_uri="gcr.io/cloud-aiplatform/training/pytorch-gpu.1-13:latest",
    requirements=["pandas", "scikit-learn"],
    model_serving_container_image_uri="gcr.io/cloud-aiplatform/prediction/pytorch-gpu.1-13:latest",
)

# Run training
model = job.run(
    dataset=dataset,
    replica_count=1,
    machine_type="n1-standard-4",
    accelerator_type="NVIDIA_TESLA_T4",
    accelerator_count=1,
    model_display_name="my-model",
)

# Deploy model to endpoint
endpoint = model.deploy(
    deployed_model_display_name="my-endpoint",
    machine_type="n1-standard-2",
    min_replica_count=1,
    max_replica_count=10,
    accelerator_type="NVIDIA_TESLA_T4",
    accelerator_count=1,
)

# Make prediction
prediction = endpoint.predict(instances=[...])
print(prediction)

# Batch prediction
batch_prediction_job = model.batch_predict(
    job_display_name="batch-prediction",
    gcs_source="gs://my-bucket/input.jsonl",
    gcs_destination_prefix="gs://my-bucket/output",
    machine_type="n1-standard-4",
)

batch_prediction_job.wait()
```

### Pattern 5: Event-Driven Architecture (Cloud Functions + Pub/Sub)

**Architecture:**
```
Cloud Storage Upload → Cloud Function (trigger) → Pub/Sub → Cloud Function (process)
                                                             ↓
                                                        BigQuery Insert
```

**Terraform Example:**
```hcl
# Storage bucket
resource "google_storage_bucket" "uploads" {
  name     = "uploads-bucket"
  location = "US"
}

# Cloud Function (storage trigger)
resource "google_cloudfunctions_function" "process_upload" {
  name        = "process-upload"
  description = "Process file uploads"
  runtime     = "python39"

  available_memory_mb   = 256
  source_archive_bucket = google_storage_bucket.functions_source.name
  source_archive_object = google_storage_bucket_object.function_zip.name

  event_trigger {
    event_type = "google.storage.object.finalize"
    resource   = google_storage_bucket.uploads.name
  }

  entry_point = "process_upload"

  environment_variables = {
    PUBSUB_TOPIC = google_pubsub_topic.processing.id
  }
}

# Cloud Function (Pub/Sub trigger)
resource "google_cloudfunctions_function" "save_to_bq" {
  name    = "save-to-bigquery"
  runtime = "python39"

  available_memory_mb   = 256
  source_archive_bucket = google_storage_bucket.functions_source.name
  source_archive_object = google_storage_bucket_object.function_zip.name

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = google_pubsub_topic.processing.id
  }

  entry_point = "save_to_bigquery"
}
```

**Python Cloud Function Example:**
```python
# main.py (storage trigger)
import json
from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('project-id', 'processing-topic')

def process_upload(event, context):
    """Triggered by a change to a Cloud Storage bucket."""
    file_name = event['name']
    bucket = event['bucket']

    print(f'Processing file: {file_name} from bucket: {bucket}')

    # Publish message to Pub/Sub
    message_data = json.dumps({
        'file': file_name,
        'bucket': bucket,
        'timestamp': context.timestamp
    }).encode('utf-8')

    future = publisher.publish(topic_path, message_data)
    print(f'Published message ID: {future.result()}')

# main.py (Pub/Sub trigger)
import base64
import json
from google.cloud import bigquery

client = bigquery.Client()
table_id = "project.dataset.table"

def save_to_bigquery(event, context):
    """Triggered from a message on a Pub/Sub topic."""
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    message_data = json.loads(pubsub_message)

    print(f'Saving to BigQuery: {message_data}')

    rows_to_insert = [message_data]
    errors = client.insert_rows_json(table_id, rows_to_insert)

    if errors:
        print(f'Errors: {errors}')
    else:
        print('Data inserted successfully')
```

---

## Multi-Language Support

### Python (Primary for Data/ML)

**Installation:**
```bash
# Core SDK
pip install google-cloud-core

# Service-specific libraries
pip install google-cloud-storage        # Cloud Storage
pip install google-cloud-bigquery       # BigQuery
pip install google-cloud-pubsub         # Pub/Sub
pip install google-cloud-firestore      # Firestore
pip install google-cloud-aiplatform     # Vertex AI
pip install google-cloud-run            # Cloud Run
```

**Authentication:**
```python
from google.cloud import storage
from google.oauth2 import service_account

# Using Application Default Credentials (ADC)
client = storage.Client()

# Using service account key file
credentials = service_account.Credentials.from_service_account_file(
    'path/to/key.json'
)
client = storage.Client(credentials=credentials)
```

### Node.js (For Web Applications)

**Installation:**
```bash
npm install @google-cloud/storage
npm install @google-cloud/bigquery
npm install @google-cloud/pubsub
npm install @google-cloud/firestore
```

**Example:**
```javascript
const {Storage} = require('@google-cloud/storage');
const storage = new Storage();

async function uploadFile(bucketName, filename) {
  await storage.bucket(bucketName).upload(filename, {
    gzip: true,
    metadata: {
      cacheControl: 'public, max-age=31536000',
    },
  });
  console.log(`${filename} uploaded to ${bucketName}`);
}
```

### Go (For High-Performance Services)

**Installation:**
```bash
go get cloud.google.com/go/storage
go get cloud.google.com/go/bigquery
go get cloud.google.com/go/pubsub
```

**Example:**
```go
import (
    "context"
    "cloud.google.com/go/storage"
)

func uploadFile(bucket, object string) error {
    ctx := context.Background()
    client, err := storage.NewClient(ctx)
    if err != nil {
        return err
    }
    defer client.Close()

    wc := client.Bucket(bucket).Object(object).NewWriter(ctx)
    if _, err := wc.Write([]byte("Hello, World!")); err != nil {
        return err
    }
    return wc.Close()
}
```

### Terraform (Infrastructure as Code)

**Provider Configuration:**
```hcl
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
```

---

## Best Practices

### 1. Cost Optimization

**Compute:**
- Use **Committed Use Discounts** for predictable workloads (57% off)
- Use **Spot VMs** for fault-tolerant workloads (60-91% off)
- **Cloud Run**: Scales to zero when idle
- **GKE Autopilot**: Pay only for pod resources, not nodes

**Storage:**
- Use appropriate **Cloud Storage classes** (Standard/Nearline/Coldline/Archive)
- Enable **Object Lifecycle Management** to transition cold data
- Use **Coldline/Archive** for backups (99% cheaper than Standard)

**Data:**
- **BigQuery**: Use partitioned and clustered tables
- **BigQuery**: Use BI Engine for caching (up to 10TB free)
- Avoid `SELECT *` - query only needed columns
- Use **flat-rate pricing** for heavy BigQuery usage

**Monitoring:**
```bash
# Enable cost breakdown
gcloud billing accounts list
gcloud billing projects describe PROJECT_ID

# Use Cloud Billing export to BigQuery for analysis
```

### 2. Security Best Practices

**Identity and Access Management (IAM):**
```hcl
# Principle of least privilege
resource "google_project_iam_member" "app_storage_reader" {
  project = var.project_id
  role    = "roles/storage.objectViewer"  # Not "roles/storage.admin"
  member  = "serviceAccount:app@project.iam.gserviceaccount.com"
}

# Use service accounts, not user accounts
resource "google_service_account" "app" {
  account_id   = "app-service-account"
  display_name = "Application Service Account"
}
```

**Workload Identity (GKE):**
```bash
# Enable Workload Identity
gcloud container clusters update CLUSTER_NAME \
    --workload-pool=PROJECT_ID.svc.id.goog

# Bind K8s service account to GCP service account
gcloud iam service-accounts add-iam-policy-binding \
    GSA_NAME@PROJECT_ID.iam.gserviceaccount.com \
    --role roles/iam.workloadIdentityUser \
    --member "serviceAccount:PROJECT_ID.svc.id.goog[NAMESPACE/KSA_NAME]"
```

**Secret Management:**
```hcl
# Use Secret Manager, not environment variables
resource "google_secret_manager_secret" "db_password" {
  secret_id = "db-password"

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "db_password" {
  secret      = google_secret_manager_secret.db_password.id
  secret_data = random_password.db.result
}

# Access from Cloud Run
resource "google_secret_manager_secret_iam_member" "access" {
  secret_id = google_secret_manager_secret.db_password.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.app.email}"
}
```

**VPC Security:**
```hcl
# Private Google Access (no public IPs needed)
resource "google_compute_subnetwork" "private" {
  name          = "private-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = "us-central1"
  network       = google_compute_network.main.id

  private_ip_google_access = true
}

# Cloud NAT for outbound internet
resource "google_compute_router_nat" "nat" {
  name   = "nat"
  router = google_compute_router.router.name
  region = google_compute_router.router.region

  nat_ip_allocate_option = "AUTO_ONLY"

  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
}
```

### 3. High Availability

**Multi-Regional Deployment:**
```hcl
# Cloud Storage with multi-region
resource "google_storage_bucket" "multi_region" {
  name          = "my-multi-region-bucket"
  location      = "US"  # Multi-region
  storage_class = "STANDARD"

  versioning {
    enabled = true
  }
}

# Cloud SQL with HA
resource "google_sql_database_instance" "ha" {
  name             = "ha-instance"
  database_version = "POSTGRES_15"
  region           = "us-central1"

  settings {
    tier = "db-custom-2-8192"

    availability_type = "REGIONAL"  # HA with automatic failover

    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = true
      transaction_log_retention_days = 7
    }
  }
}

# Cloud Spanner with multi-region
resource "google_spanner_instance" "multi_region" {
  name         = "multi-region-instance"
  config       = "nam3"  # North America multi-region
  display_name = "Multi-region instance"
  num_nodes    = 2

  labels = {
    env = "production"
  }
}
```

**Load Balancing:**
```hcl
# Global HTTP(S) Load Balancer
resource "google_compute_global_address" "default" {
  name = "global-lb-ip"
}

resource "google_compute_global_forwarding_rule" "default" {
  name       = "global-lb-forwarding-rule"
  target     = google_compute_target_https_proxy.default.id
  port_range = "443"
  ip_address = google_compute_global_address.default.address
}

resource "google_compute_backend_service" "default" {
  name                  = "backend-service"
  protocol              = "HTTP"
  timeout_sec           = 30
  health_checks         = [google_compute_health_check.default.id]
  load_balancing_scheme = "EXTERNAL_MANAGED"

  backend {
    group           = google_compute_region_network_endpoint_group.us_central1.id
    balancing_mode  = "UTILIZATION"
    capacity_scaler = 1.0
  }

  backend {
    group           = google_compute_region_network_endpoint_group.us_east1.id
    balancing_mode  = "UTILIZATION"
    capacity_scaler = 1.0
  }

  cdn_policy {
    cache_mode = "CACHE_ALL_STATIC"
    default_ttl = 3600
  }
}
```

### 4. Monitoring and Logging

**Cloud Monitoring:**
```python
from google.cloud import monitoring_v3
import time

client = monitoring_v3.MetricServiceClient()
project_name = f"projects/{project_id}"

# Create custom metric
series = monitoring_v3.TimeSeries()
series.metric.type = "custom.googleapis.com/api/request_count"
series.resource.type = "global"

point = monitoring_v3.Point()
point.value.int64_value = 123
point.interval.end_time.seconds = int(time.time())

series.points = [point]
client.create_time_series(name=project_name, time_series=[series])

# Query metrics
interval = monitoring_v3.TimeInterval()
now = time.time()
interval.end_time.seconds = int(now)
interval.start_time.seconds = int(now - 3600)

results = client.list_time_series(
    request={
        "name": project_name,
        "filter": 'metric.type="compute.googleapis.com/instance/cpu/utilization"',
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }
)

for result in results:
    print(result)
```

**Cloud Logging:**
```python
from google.cloud import logging

client = logging.Client()
logger = client.logger("my-app")

# Write structured log
logger.log_struct(
    {
        "message": "User login",
        "user_id": "user_123",
        "ip_address": "1.2.3.4",
        "severity": "INFO"
    }
)

# Read logs
entries = client.list_entries(filter_='resource.type="cloud_run_revision"')
for entry in entries:
    print(entry.payload)
```

### 5. Network Architecture

**VPC Design Pattern:**
```
VPC: 10.0.0.0/16
├─► Region: us-central1
│   ├─► Subnet: public (10.0.1.0/24)
│   └─► Subnet: private (10.0.2.0/24)
├─► Region: us-east1
│   ├─► Subnet: public (10.0.3.0/24)
│   └─► Subnet: private (10.0.4.0/24)
```

**Terraform VPC:**
```hcl
resource "google_compute_network" "main" {
  name                    = "main-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "us_central1_private" {
  name          = "us-central1-private"
  ip_cidr_range = "10.0.2.0/24"
  region        = "us-central1"
  network       = google_compute_network.main.id

  private_ip_google_access = true

  secondary_ip_range {
    range_name    = "pods"
    ip_cidr_range = "10.1.0.0/16"
  }

  secondary_ip_range {
    range_name    = "services"
    ip_cidr_range = "10.2.0.0/20"
  }
}

# Firewall rules
resource "google_compute_firewall" "allow_internal" {
  name    = "allow-internal"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
    ports    = ["0-65535"]
  }

  allow {
    protocol = "udp"
    ports    = ["0-65535"]
  }

  allow {
    protocol = "icmp"
  }

  source_ranges = ["10.0.0.0/16"]
}

resource "google_compute_firewall" "allow_health_check" {
  name    = "allow-health-check"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
  }

  source_ranges = ["35.191.0.0/16", "130.211.0.0/22"]
}
```

---

## Library Recommendations

### Official Google Cloud SDKs

| Language | Package | Latest Version | Installation |
|----------|---------|----------------|--------------|
| **Python** | google-cloud-* | 2.x | `pip install google-cloud-{service}` |
| **Node.js** | @google-cloud/* | 7.x | `npm install @google-cloud/{service}` |
| **Go** | cloud.google.com/go | 0.110+ | `go get cloud.google.com/go/{service}` |
| **Java** | com.google.cloud | 2.x | Maven/Gradle |
| **C#** | Google.Cloud.* | 3.x | NuGet |

### Terraform Provider

```hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 5.0"
    }
  }
}
```

### CLI Tools

| Tool | Purpose | Installation |
|------|---------|--------------|
| **gcloud** | GCP CLI | `curl https://sdk.cloud.google.com | bash` |
| **terraform** | IaC | https://terraform.io/downloads |
| **kubectl** | Kubernetes | `gcloud components install kubectl` |
| **bq** | BigQuery CLI | Included with gcloud |
| **gsutil** | Cloud Storage CLI | Included with gcloud |

---

## Skill Structure Design

```
gcp-patterns/
├── SKILL.md                          # Main skill (500-700 lines)
├── references/
│   ├── compute-services.md           # Cloud Run, GKE, Functions, Compute Engine
│   ├── storage-databases.md          # Storage classes, SQL/NoSQL decision tree
│   ├── data-analytics.md             # BigQuery, Pub/Sub, Dataflow, Dataproc
│   ├── ml-ai-services.md             # Vertex AI, AutoML, pre-trained APIs
│   ├── networking.md                 # VPC, Load Balancing, CDN, Armor
│   ├── security-iam.md               # IAM patterns, Workload Identity, Secret Manager
│   └── cost-optimization.md          # Cost patterns, committed use, spot VMs
├── examples/
│   ├── terraform/
│   │   ├── cloud-run-service/        # Serverless web app
│   │   ├── gke-cluster/              # Kubernetes cluster
│   │   ├── bigquery-pipeline/        # Data analytics
│   │   └── vertex-ai-pipeline/       # ML workflow
│   ├── python/
│   │   ├── storage-operations.py
│   │   ├── bigquery-queries.py
│   │   ├── pubsub-messaging.py
│   │   └── vertex-ai-training.py
│   └── gcloud/
│       └── common-commands.sh
└── scripts/
    ├── setup-project.sh              # Initialize GCP project
    ├── cost-report.sh                # Cost analysis
    └── security-audit.sh             # Security best practices check
```

---

## Integration Points

### With Existing Skills

| Skill | Integration | Example |
|-------|-------------|---------|
| `infrastructure-as-code` | GCP resources via Terraform/Pulumi | Provision GKE clusters |
| `kubernetes-operations` | GKE management | Deploy apps to GKE |
| `data-architecture` | BigQuery as data warehouse | Design analytics pipelines |
| `building-ci-pipelines` | Cloud Build for CI/CD | Deploy to Cloud Run |
| `secret-management` | Secret Manager integration | Store database credentials |
| `observability` | Cloud Monitoring/Logging | Monitor GCP services |
| `databases-*` | GCP database services | Choose Cloud SQL vs Spanner |
| `ai-data-engineering` | Vertex AI + BigQuery | ML on data warehouse |

### Skill Chaining Example

```
gcp-patterns → infrastructure-as-code → kubernetes-operations
      │                   │                       │
      ▼                   ▼                       ▼
Choose Cloud Run    Write Terraform      Configure GKE
or GKE              for GKE              workloads
```

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1)
- [ ] Core decision frameworks (compute, storage, database)
- [ ] Cloud Run patterns and examples
- [ ] Cloud Storage and Cloud SQL basics

### Phase 2: Container & Orchestration (Week 2)
- [ ] GKE patterns and examples
- [ ] Workload Identity setup
- [ ] Container best practices

### Phase 3: Data & Analytics (Week 3)
- [ ] BigQuery patterns
- [ ] Pub/Sub + Dataflow pipelines
- [ ] Data warehouse design

### Phase 4: ML/AI (Week 4)
- [ ] Vertex AI examples
- [ ] AutoML patterns
- [ ] Pre-trained API usage

### Phase 5: Advanced Topics (Week 5)
- [ ] Multi-region deployment
- [ ] Cost optimization strategies
- [ ] Security hardening

### Phase 6: Polish & Review (Week 6)
- [ ] Complete all examples
- [ ] Test Terraform configurations
- [ ] Documentation review

---

## Key Takeaways

1. **Cloud Run First:** Default choice for stateless HTTP services (serverless, auto-scale)
2. **BigQuery for Analytics:** Best-in-class data warehouse (petabyte scale, serverless)
3. **GKE for Kubernetes:** Most mature managed Kubernetes (invented by Kubernetes creators)
4. **Vertex AI for ML:** Unified platform for entire ML lifecycle (training, deployment, monitoring)
5. **Cost Optimization:** Per-second billing, sustained use discounts, committed use (57% off)
6. **Multi-Region Matters:** Use multi-region for production (99.95% SLA vs 99.5%)
7. **Workload Identity:** Modern authentication for GKE (no service account keys)
8. **Private Google Access:** Access GCP services without public IPs (security best practice)

---

**Progressive Disclosure:** This init.md provides the master plan. Detailed documentation will be in `references/` directory, working examples in `examples/`, and utility scripts in `scripts/`.
