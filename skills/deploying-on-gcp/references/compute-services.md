# GCP Compute Services Reference

Detailed patterns and configurations for Google Cloud Platform compute services.

## Table of Contents

1. [Cloud Run (Serverless Containers)](#cloud-run-serverless-containers)
2. [Google Kubernetes Engine (GKE)](#google-kubernetes-engine-gke)
3. [Cloud Functions](#cloud-functions)
4. [Compute Engine (VMs)](#compute-engine-vms)
5. [App Engine](#app-engine)
6. [Service Comparison Matrix](#service-comparison-matrix)

---

## Cloud Run (Serverless Containers)

### When to Use Cloud Run

**Ideal For:**
- Stateless HTTP services and APIs
- Microservices architecture
- Variable or unpredictable traffic
- Services that should scale to zero when idle
- Quick deployment without infrastructure management

**Not Ideal For:**
- Long-running jobs (use Cloud Run Jobs)
- Stateful applications (use GKE or Compute Engine)
- Applications requiring persistent connections (use GKE)

### Cloud Run Configuration

**Terraform Example:**

```hcl
resource "google_cloud_run_service" "api" {
  name     = "api-service"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "gcr.io/project-id/api:latest"

        # Resource limits
        resources {
          limits = {
            cpu    = "2"      # Up to 8 CPUs
            memory = "2Gi"    # Up to 32GB
          }
        }

        # Environment variables
        env {
          name  = "DATABASE_URL"
          value = "postgresql://..."
        }

        # Secret from Secret Manager
        env {
          name = "API_KEY"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.api_key.secret_id
              key  = "latest"
            }
          }
        }

        # Port configuration
        ports {
          container_port = 8080
        }

        # Startup probe
        startup_probe {
          http_get {
            path = "/health"
          }
          initial_delay_seconds = 0
          timeout_seconds       = 1
          period_seconds        = 3
          failure_threshold     = 3
        }
      }

      # Concurrency control
      container_concurrency = 80  # Max concurrent requests per instance

      # Timeout
      timeout_seconds = 300  # Max 60 minutes

      # Service account for Workload Identity
      service_account_name = google_service_account.api.email
    }

    metadata {
      annotations = {
        # Auto-scaling
        "autoscaling.knative.dev/minScale" = "1"
        "autoscaling.dev/maxScale" = "100"

        # CPU allocation (always or request-based)
        "run.googleapis.com/cpu-throttling" = "true"  # CPU allocated only during requests

        # Cloud SQL connection
        "run.googleapis.com/cloudsql-instances" = google_sql_database_instance.main.connection_name

        # VPC connector (for private resources)
        "run.googleapis.com/vpc-access-connector" = google_vpc_access_connector.connector.id
        "run.googleapis.com/vpc-access-egress"    = "private-ranges-only"
      }

      labels = {
        environment = "production"
        team        = "api"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  # Prevent accidental deletion
  lifecycle {
    prevent_destroy = true
  }
}

# Public access
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

# Private access (requires authentication)
resource "google_cloud_run_service_iam_member" "auth" {
  location = google_cloud_run_service.api.location
  service  = google_cloud_run_service.api.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:caller@project.iam.gserviceaccount.com"
}
```

### Cloud Run Jobs

For batch processing and scheduled tasks:

```hcl
resource "google_cloud_run_v2_job" "batch_processor" {
  name     = "batch-processor"
  location = "us-central1"

  template {
    template {
      containers {
        image = "gcr.io/project-id/batch:latest"

        resources {
          limits = {
            cpu    = "4"
            memory = "8Gi"
          }
        }
      }

      # Max execution time
      timeout = "3600s"  # 1 hour

      # Task configuration
      max_retries = 3
    }

    # Parallelism
    task_count = 10
    parallelism = 5
  }
}

# Schedule with Cloud Scheduler
resource "google_cloud_scheduler_job" "trigger" {
  name        = "trigger-batch"
  description = "Trigger batch processing job"
  schedule    = "0 2 * * *"  # Daily at 2am
  time_zone   = "America/New_York"

  http_target {
    http_method = "POST"
    uri         = "https://${google_cloud_run_v2_job.batch_processor.location}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${var.project_id}/jobs/${google_cloud_run_v2_job.batch_processor.name}:run"

    oauth_token {
      service_account_email = google_service_account.scheduler.email
    }
  }
}
```

---

## Google Kubernetes Engine (GKE)

### When to Use GKE

**Ideal For:**
- Complex multi-service orchestration
- Stateful applications (databases, caches)
- Applications requiring persistent connections
- Existing Kubernetes deployments
- Advanced networking requirements
- Multi-tenant platforms

**Not Ideal For:**
- Simple stateless services (use Cloud Run)
- No Kubernetes expertise (use Cloud Run or App Engine)

### GKE Autopilot vs Standard

| Feature | Autopilot | Standard |
|---------|-----------|----------|
| **Node Management** | Fully managed | Self-managed |
| **Cost Model** | Pay per pod resources | Pay for nodes |
| **Configuration** | Opinionated, secure defaults | Full customization |
| **Scaling** | Automatic | Manual or cluster autoscaler |
| **Best For** | Most workloads | Advanced customization needs |

### GKE Autopilot Configuration

```hcl
resource "google_container_cluster" "autopilot" {
  name     = "gke-autopilot-cluster"
  location = "us-central1"

  # Enable Autopilot
  enable_autopilot = true

  # Release channel (RAPID, REGULAR, STABLE)
  release_channel {
    channel = "REGULAR"
  }

  # IP allocation policy
  ip_allocation_policy {
    cluster_secondary_range_name  = "pods"
    services_secondary_range_name = "services"
  }

  # Workload Identity (required for Autopilot)
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
      display_name = "internal-network"
    }
  }

  # Maintenance window
  maintenance_policy {
    daily_maintenance_window {
      start_time = "03:00"
    }
  }

  # Binary authorization
  binary_authorization {
    evaluation_mode = "PROJECT_SINGLETON_POLICY_ENFORCE"
  }

  # Network policy
  network_policy {
    enabled  = true
    provider = "PROVIDER_UNSPECIFIED"
  }

  # Monitoring and logging
  monitoring_config {
    enable_components = ["SYSTEM_COMPONENTS", "WORKLOADS"]
    managed_prometheus {
      enabled = true
    }
  }

  logging_config {
    enable_components = ["SYSTEM_COMPONENTS", "WORKLOADS"]
  }
}
```

### GKE Standard Configuration

```hcl
resource "google_container_cluster" "standard" {
  name     = "gke-standard-cluster"
  location = "us-central1"

  # Remove default node pool (create custom pool separately)
  remove_default_node_pool = true
  initial_node_count       = 1

  release_channel {
    channel = "REGULAR"
  }

  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = false
    master_ipv4_cidr_block  = "172.16.0.0/28"
  }

  ip_allocation_policy {
    cluster_secondary_range_name  = "pods"
    services_secondary_range_name = "services"
  }

  network_policy {
    enabled  = true
    provider = "PROVIDER_UNSPECIFIED"
  }

  addons_config {
    http_load_balancing {
      disabled = false
    }
    horizontal_pod_autoscaling {
      disabled = false
    }
    network_policy_config {
      disabled = false
    }
    gcp_filestore_csi_driver_config {
      enabled = true
    }
    gce_persistent_disk_csi_driver_config {
      enabled = true
    }
  }
}

# Custom node pool
resource "google_container_node_pool" "primary" {
  name       = "primary-pool"
  location   = "us-central1"
  cluster    = google_container_cluster.standard.name
  node_count = 1

  autoscaling {
    min_node_count = 1
    max_node_count = 10
  }

  management {
    auto_repair  = true
    auto_upgrade = true
  }

  node_config {
    preemptible  = false
    machine_type = "e2-standard-4"
    disk_size_gb = 100
    disk_type    = "pd-standard"

    # Service account with minimal permissions
    service_account = google_service_account.gke_nodes.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    # Workload Identity
    workload_metadata_config {
      mode = "GKE_METADATA"
    }

    # Shielded instance
    shielded_instance_config {
      enable_secure_boot          = true
      enable_integrity_monitoring = true
    }

    labels = {
      environment = "production"
    }

    tags = ["gke-node"]
  }
}

# Spot VM node pool (for fault-tolerant workloads)
resource "google_container_node_pool" "spot" {
  name       = "spot-pool"
  location   = "us-central1"
  cluster    = google_container_cluster.standard.name
  node_count = 0

  autoscaling {
    min_node_count = 0
    max_node_count = 20
  }

  node_config {
    spot         = true  # 60-91% cheaper
    machine_type = "e2-standard-4"

    service_account = google_service_account.gke_nodes.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    workload_metadata_config {
      mode = "GKE_METADATA"
    }

    labels = {
      workload-type = "batch"
    }

    taint {
      key    = "workload-type"
      value  = "batch"
      effect = "NO_SCHEDULE"
    }
  }
}
```

### Workload Identity Setup

```bash
# Enable Workload Identity on cluster
gcloud container clusters update CLUSTER_NAME \
    --workload-pool=PROJECT_ID.svc.id.goog

# Create Kubernetes service account
kubectl create serviceaccount KSA_NAME \
    --namespace NAMESPACE

# Create GCP service account
gcloud iam service-accounts create GSA_NAME

# Bind Kubernetes SA to GCP SA
gcloud iam service-accounts add-iam-policy-binding \
    GSA_NAME@PROJECT_ID.iam.gserviceaccount.com \
    --role roles/iam.workloadIdentityUser \
    --member "serviceAccount:PROJECT_ID.svc.id.goog[NAMESPACE/KSA_NAME]"

# Annotate Kubernetes SA
kubectl annotate serviceaccount KSA_NAME \
    --namespace NAMESPACE \
    iam.gke.io/gcp-service-account=GSA_NAME@PROJECT_ID.iam.gserviceaccount.com
```

---

## Cloud Functions

### When to Use Cloud Functions

**Ideal For:**
- Event-driven processing (Cloud Storage, Pub/Sub, Firestore triggers)
- Lightweight HTTP endpoints
- Single-purpose functions
- Integration glue between GCP services

**Not Ideal For:**
- Long-running tasks (10-minute max for gen2)
- Complex application logic (use Cloud Run)
- Stateful operations

### Cloud Functions Gen2 (Recommended)

```hcl
# Storage bucket for function source
resource "google_storage_bucket" "functions" {
  name     = "${var.project_id}-functions"
  location = "US"
}

# Upload function source
resource "google_storage_bucket_object" "function_zip" {
  name   = "function-source.zip"
  bucket = google_storage_bucket.functions.name
  source = "path/to/function.zip"
}

# Cloud Function with HTTP trigger
resource "google_cloudfunctions2_function" "http_function" {
  name     = "http-function"
  location = "us-central1"

  build_config {
    runtime     = "python39"
    entry_point = "hello_http"
    source {
      storage_source {
        bucket = google_storage_bucket.functions.name
        object = google_storage_bucket_object.function_zip.name
      }
    }
  }

  service_config {
    max_instance_count = 100
    min_instance_count = 0
    available_memory   = "256Mi"
    timeout_seconds    = 60

    environment_variables = {
      API_KEY = "value"
    }

    # Secret from Secret Manager
    secret_environment_variables {
      key        = "DB_PASSWORD"
      project_id = var.project_id
      secret     = google_secret_manager_secret.db_password.secret_id
      version    = "latest"
    }

    service_account_email = google_service_account.function.email
  }
}

# Cloud Function with Pub/Sub trigger
resource "google_cloudfunctions2_function" "pubsub_function" {
  name     = "pubsub-function"
  location = "us-central1"

  build_config {
    runtime     = "python39"
    entry_point = "process_message"
    source {
      storage_source {
        bucket = google_storage_bucket.functions.name
        object = google_storage_bucket_object.function_zip.name
      }
    }
  }

  service_config {
    max_instance_count = 100
    available_memory   = "512Mi"
    timeout_seconds    = 300
  }

  event_trigger {
    trigger_region = "us-central1"
    event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic   = google_pubsub_topic.events.id
    retry_policy   = "RETRY_POLICY_RETRY"
  }
}

# Cloud Function with Storage trigger
resource "google_cloudfunctions2_function" "storage_function" {
  name     = "storage-function"
  location = "us-central1"

  build_config {
    runtime     = "python39"
    entry_point = "process_file"
    source {
      storage_source {
        bucket = google_storage_bucket.functions.name
        object = google_storage_bucket_object.function_zip.name
      }
    }
  }

  service_config {
    max_instance_count = 50
    available_memory   = "1Gi"
    timeout_seconds    = 540
  }

  event_trigger {
    trigger_region = "us-central1"
    event_type     = "google.cloud.storage.object.v1.finalized"
    event_filters {
      attribute = "bucket"
      value     = google_storage_bucket.uploads.name
    }
  }
}
```

---

## Compute Engine (VMs)

### When to Use Compute Engine

**Ideal For:**
- Full OS control required
- GPU/TPU workloads
- Windows applications
- Legacy application lift-and-shift
- Custom kernel or networking

**Not Ideal For:**
- Simple web services (use Cloud Run)
- Don't want to manage infrastructure (use Cloud Run or App Engine)

### Compute Engine Configuration

```hcl
# Instance template for managed instance group
resource "google_compute_instance_template" "web" {
  name_prefix  = "web-template-"
  machine_type = "e2-medium"
  region       = "us-central1"

  disk {
    source_image = "debian-cloud/debian-11"
    auto_delete  = true
    boot         = true
    disk_size_gb = 20
    disk_type    = "pd-balanced"
  }

  network_interface {
    network    = google_compute_network.main.id
    subnetwork = google_compute_subnetwork.private.id

    # No external IP (use Cloud NAT)
    access_config {
      network_tier = "PREMIUM"
    }
  }

  metadata_startup_script = file("startup.sh")

  service_account {
    email  = google_service_account.instance.email
    scopes = ["cloud-platform"]
  }

  shielded_instance_config {
    enable_secure_boot          = true
    enable_integrity_monitoring = true
    enable_vtpm                 = true
  }

  tags = ["web-server"]

  lifecycle {
    create_before_destroy = true
  }
}

# Managed instance group with autoscaling
resource "google_compute_region_instance_group_manager" "web" {
  name   = "web-igm"
  region = "us-central1"

  base_instance_name = "web"

  version {
    instance_template = google_compute_instance_template.web.id
  }

  target_size = 3

  named_port {
    name = "http"
    port = 80
  }

  auto_healing_policies {
    health_check      = google_compute_health_check.web.id
    initial_delay_sec = 300
  }
}

# Autoscaler
resource "google_compute_region_autoscaler" "web" {
  name   = "web-autoscaler"
  region = "us-central1"
  target = google_compute_region_instance_group_manager.web.id

  autoscaling_policy {
    min_replicas    = 2
    max_replicas    = 10
    cooldown_period = 60

    cpu_utilization {
      target = 0.6
    }
  }
}
```

---

## App Engine

### When to Use App Engine

**Ideal For:**
- Simple web applications
- Quick prototyping
- Legacy App Engine applications
- No infrastructure management desired

**Not Ideal For:**
- New projects (Cloud Run is preferred)
- Need containerization (use Cloud Run)
- Complex orchestration (use GKE)

### App Engine Configuration

```yaml
# app.yaml
runtime: python39
entrypoint: gunicorn -b :$PORT main:app

instance_class: F2

automatic_scaling:
  target_cpu_utilization: 0.65
  min_instances: 1
  max_instances: 10
  min_pending_latency: 30ms
  max_pending_latency: automatic
  max_concurrent_requests: 50

env_variables:
  API_KEY: "value"

handlers:
- url: /static
  static_dir: static

- url: /.*
  script: auto
```

---

## Service Comparison Matrix

| Feature | Cloud Run | GKE Autopilot | GKE Standard | Cloud Functions | Compute Engine | App Engine |
|---------|-----------|---------------|--------------|-----------------|----------------|------------|
| **Management** | Fully managed | Fully managed | Self-managed nodes | Fully managed | Self-managed | Fully managed |
| **Scale to Zero** | Yes | No | No | Yes | No | No |
| **Max Execution Time** | 60 min | Unlimited | Unlimited | 60 min | Unlimited | 60 min |
| **Min Instances** | 0 | 0 | 0 | 0 | 0 | 1 |
| **Max Instances** | 1000 | Unlimited | Unlimited | 1000 | Unlimited | Unlimited |
| **Cold Start** | ~1s | N/A | N/A | 1-5s | Minutes | Seconds |
| **Pricing Model** | Per request | Per pod | Per node | Per invocation | Per VM hour | Per instance hour |
| **Best For** | HTTP APIs | Complex apps | Advanced K8s | Events | Full control | Simple web apps |
| **Container Support** | Yes | Yes | Yes | Limited | Yes | Limited |
| **Persistent Connections** | Limited | Yes | Yes | No | Yes | Limited |
| **GPU Support** | No | Yes | Yes | No | Yes | No |

## Selection Decision Tree

```
Need to run application in GCP?
├─ Need Kubernetes? → YES
│  ├─ Need node customization? → YES → GKE Standard
│  └─ NO (want managed) → GKE Autopilot
│
├─ HTTP service? → YES
│  ├─ Stateless? → YES
│  │  ├─ Container-based? → YES → Cloud Run
│  │  └─ NO (simple web app) → App Engine
│  └─ NO (stateful) → Compute Engine or GKE
│
├─ Event-driven? → YES
│  ├─ Simple function? → YES → Cloud Functions
│  └─ Complex processing → Cloud Run Jobs
│
└─ Need full OS control? → YES → Compute Engine
```

**Recommendation:** Start with Cloud Run for most HTTP services. Move to GKE only if you need Kubernetes-specific features or complex orchestration.
