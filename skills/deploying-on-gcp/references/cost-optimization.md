# GCP Cost Optimization Reference

Strategies for reducing Google Cloud Platform costs.


## Table of Contents

- [Compute Cost Optimization](#compute-cost-optimization)
  - [Committed Use Discounts (57% off)](#committed-use-discounts-57-off)
  - [Spot VMs (60-91% off)](#spot-vms-60-91-off)
  - [Right-Sizing VMs](#right-sizing-vms)
  - [Cloud Run Cost Optimization](#cloud-run-cost-optimization)
- [Storage Cost Optimization](#storage-cost-optimization)
  - [Object Lifecycle Management](#object-lifecycle-management)
  - [Compression and Deduplication](#compression-and-deduplication)
- [BigQuery Cost Optimization](#bigquery-cost-optimization)
  - [Partitioned and Clustered Tables](#partitioned-and-clustered-tables)
  - [Query Best Practices](#query-best-practices)
  - [Flat-Rate Pricing](#flat-rate-pricing)
- [Database Cost Optimization](#database-cost-optimization)
  - [Cloud SQL Instance Scheduling](#cloud-sql-instance-scheduling)
  - [Use Read Replicas Instead of Scaling Up](#use-read-replicas-instead-of-scaling-up)
- [Network Cost Optimization](#network-cost-optimization)
  - [Use Regional Resources](#use-regional-resources)
  - [Cloud CDN for Egress](#cloud-cdn-for-egress)
  - [Premium vs Standard Network Tier](#premium-vs-standard-network-tier)
- [Monitoring and Alerts](#monitoring-and-alerts)
  - [Cost Budget Alerts](#cost-budget-alerts)
  - [Cost Anomaly Detection](#cost-anomaly-detection)
- [Cost Optimization Summary](#cost-optimization-summary)
- [Cost Monitoring Tools](#cost-monitoring-tools)
- [Best Practices Checklist](#best-practices-checklist)

## Compute Cost Optimization

### Committed Use Discounts (57% off)

```hcl
# Reserve compute resources for 1 or 3 years
resource "google_compute_commitment" "commitment" {
  name   = "compute-commitment"
  region = "us-central1"
  plan   = "THIRTY_SIX_MONTH"  # 1-year or 3-year

  resources {
    type   = "VCPU"
    amount = "100"
  }

  resources {
    type   = "MEMORY"
    amount = "400"  # GB
  }
}
```

### Spot VMs (60-91% off)

```hcl
resource "google_compute_instance_template" "spot" {
  name_prefix  = "spot-template-"
  machine_type = "n2-standard-4"

  scheduling {
    preemptible                 = true
    automatic_restart           = false
    on_host_maintenance         = "TERMINATE"
    provisioning_model          = "SPOT"
    instance_termination_action = "STOP"
  }

  disk {
    source_image = "debian-cloud/debian-11"
  }

  network_interface {
    network = "default"
  }
}
```

### Right-Sizing VMs

```bash
# Get recommendations
gcloud recommender recommendations list \
    --project=PROJECT_ID \
    --location=us-central1 \
    --recommender=google.compute.instance.MachineTypeRecommender

# Apply recommendation
gcloud compute instances set-machine-type INSTANCE_NAME \
    --machine-type=n2-standard-2 \
    --zone=us-central1-a
```

### Cloud Run Cost Optimization

```hcl
resource "google_cloud_run_service" "optimized" {
  name     = "optimized-service"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "gcr.io/project/app:latest"

        resources {
          limits = {
            cpu    = "1"      # Right-size CPU
            memory = "512Mi"  # Right-size memory
          }
        }
      }

      # Scale to zero when idle
      container_concurrency = 80
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale" = "0"  # Scale to zero
        "autoscaling.knative.dev/maxScale" = "10"

        # CPU allocated only during requests
        "run.googleapis.com/cpu-throttling" = "true"
      }
    }
  }
}
```

## Storage Cost Optimization

### Object Lifecycle Management

```hcl
resource "google_storage_bucket" "optimized" {
  name     = "optimized-bucket"
  location = "US"

  # Transition to cheaper storage classes
  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"  # $0.01/GB/month vs $0.02/GB for Standard
    }
  }

  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type          = "SetStorageClass"
      storage_class = "COLDLINE"  # $0.004/GB/month
    }
  }

  lifecycle_rule {
    condition {
      age = 365
    }
    action {
      type          = "SetStorageClass"
      storage_class = "ARCHIVE"  # $0.0012/GB/month
    }
  }

  # Delete old data
  lifecycle_rule {
    condition {
      age = 730  # 2 years
    }
    action {
      type = "Delete"
    }
  }

  # Delete old versions
  lifecycle_rule {
    condition {
      num_newer_versions = 3
    }
    action {
      type = "Delete"
    }
  }
}
```

### Compression and Deduplication

```python
from google.cloud import storage
import gzip

client = storage.Client()
bucket = client.bucket('my-bucket')

# Upload compressed objects
blob = bucket.blob('data.json.gz')
blob.content_encoding = 'gzip'

with gzip.open('data.json', 'rb') as f:
    blob.upload_from_file(f, content_type='application/json')
```

## BigQuery Cost Optimization

### Partitioned and Clustered Tables

```hcl
resource "google_bigquery_table" "optimized" {
  dataset_id = google_bigquery_dataset.analytics.dataset_id
  table_id   = "events_optimized"

  # Partitioning reduces query costs
  time_partitioning {
    type          = "DAY"
    field         = "event_timestamp"
    expiration_ms = 7776000000  # Auto-delete after 90 days
  }

  # Clustering further reduces costs
  clustering = ["user_id", "event_type", "country"]

  # Range partitioning (alternative)
  range_partitioning {
    field = "user_id"
    range {
      start    = 0
      end      = 1000000
      interval = 10000
    }
  }

  schema = jsonencode([
    { name = "event_timestamp", type = "TIMESTAMP", mode = "REQUIRED" },
    { name = "user_id", type = "INTEGER", mode = "REQUIRED" },
    { name = "event_type", type = "STRING", mode = "REQUIRED" },
    { name = "country", type = "STRING", mode = "NULLABLE" }
  ])
}
```

### Query Best Practices

```sql
-- BAD: Full table scan ($$$)
SELECT * FROM `project.dataset.table`;

-- GOOD: Query specific columns and partitions ($)
SELECT user_id, event_type
FROM `project.dataset.table`
WHERE event_timestamp >= '2025-01-01'
  AND event_timestamp < '2025-01-02'
  AND country = 'US';

-- Use LIMIT for exploration
SELECT *
FROM `project.dataset.table`
WHERE event_timestamp >= '2025-01-01'
LIMIT 1000;

-- Preview without cost
SELECT *
FROM `project.dataset.table`
TABLESAMPLE SYSTEM (1 PERCENT);
```

### Flat-Rate Pricing

For heavy BigQuery usage:

```hcl
resource "google_bigquery_reservation" "reservation" {
  name     = "production-reservation"
  location = "US"

  # 100 slots = ~$2,000/month (vs on-demand at $5/TB)
  # Break-even: ~400 TB queried per month
  slot_capacity = 100
}

resource "google_bigquery_reservation_assignment" "assignment" {
  assignee      = "projects/${var.project_id}"
  job_type      = "QUERY"
  reservation   = google_bigquery_reservation.reservation.id
}
```

## Database Cost Optimization

### Cloud SQL Instance Scheduling

```bash
# Stop instance during off-hours
gcloud sql instances patch INSTANCE_NAME \
    --activation-policy=NEVER

# Start instance
gcloud sql instances patch INSTANCE_NAME \
    --activation-policy=ALWAYS

# Automate with Cloud Scheduler
gcloud scheduler jobs create http stop-db \
    --schedule="0 18 * * *" \
    --uri="https://sqladmin.googleapis.com/v1/projects/PROJECT_ID/instances/INSTANCE_NAME/stop" \
    --http-method=POST \
    --oauth-service-account-email=SERVICE_ACCOUNT
```

### Use Read Replicas Instead of Scaling Up

```hcl
# Read replica in same region (cheaper than larger primary)
resource "google_sql_database_instance" "replica" {
  name                 = "read-replica"
  master_instance_name = google_sql_database_instance.main.name
  region               = "us-central1"

  replica_configuration {
    failover_target = false
  }

  settings {
    tier = "db-custom-2-8192"  # Smaller than primary
  }
}
```

## Network Cost Optimization

### Use Regional Resources

```hcl
# Multi-region costs more for data processing
# Use regional unless global distribution required

resource "google_compute_backend_service" "regional" {
  name                  = "regional-backend"
  load_balancing_scheme = "INTERNAL_MANAGED"  # Regional, cheaper
  protocol              = "HTTP"
}
```

### Cloud CDN for Egress

```hcl
resource "google_compute_backend_service" "cdn_enabled" {
  name = "cdn-backend"

  # Enable CDN to reduce egress costs
  cdn_policy {
    cache_mode  = "CACHE_ALL_STATIC"
    default_ttl = 3600
  }
}
```

### Premium vs Standard Network Tier

```hcl
# Standard tier: 25-40% cheaper, acceptable for most workloads
resource "google_compute_address" "standard_tier" {
  name         = "standard-ip"
  region       = "us-central1"
  network_tier = "STANDARD"  # Cheaper than PREMIUM
}
```

## Monitoring and Alerts

### Cost Budget Alerts

```hcl
resource "google_billing_budget" "budget" {
  billing_account = var.billing_account
  display_name    = "Monthly Budget"

  budget_filter {
    projects = ["projects/${var.project_id}"]
  }

  amount {
    specified_amount {
      currency_code = "USD"
      units         = "1000"
    }
  }

  threshold_rules {
    threshold_percent = 0.5
  }

  threshold_rules {
    threshold_percent = 0.9
  }

  threshold_rules {
    threshold_percent = 1.0
  }

  all_updates_rule {
    pubsub_topic = google_pubsub_topic.budget_alerts.id
  }
}
```

### Cost Anomaly Detection

```bash
# Enable cost anomaly detection
gcloud billing accounts describe BILLING_ACCOUNT \
    --format="value(anomalyConfig.state)"

# List anomalies
gcloud billing accounts anomalies list \
    --billing-account=BILLING_ACCOUNT
```

## Cost Optimization Summary

| Service | Strategy | Savings |
|---------|----------|---------|
| **Compute** | Committed use discounts | 57% |
| **Compute** | Spot VMs | 60-91% |
| **Compute** | Right-sizing | 20-40% |
| **Cloud Run** | Scale to zero | 100% when idle |
| **Storage** | Lifecycle management | 80-98% |
| **BigQuery** | Partitioning/clustering | 50-90% |
| **BigQuery** | Flat-rate (heavy use) | 40-60% |
| **Cloud SQL** | Instance scheduling | 50% (off hours) |
| **Networking** | CDN for egress | 30-50% |
| **Networking** | Standard tier | 25-40% |

## Cost Monitoring Tools

```bash
# Export billing to BigQuery
gcloud alpha billing accounts update BILLING_ACCOUNT \
    --export-enabled \
    --export-dataset=PROJECT_ID:billing_export

# Query costs
SELECT
  service.description AS service,
  SUM(cost) AS total_cost
FROM `project.billing_export.gcp_billing_export_v1_*`
WHERE _TABLE_SUFFIX = FORMAT_DATE('%Y%m%d', CURRENT_DATE())
GROUP BY service
ORDER BY total_cost DESC;
```

## Best Practices Checklist

- [ ] Use committed use discounts for predictable workloads
- [ ] Use Spot VMs for batch/fault-tolerant workloads
- [ ] Right-size all resources (use Recommender)
- [ ] Enable Cloud Run CPU throttling and scale-to-zero
- [ ] Implement Storage lifecycle policies
- [ ] Use partitioned and clustered tables in BigQuery
- [ ] Stop non-production databases during off-hours
- [ ] Enable Cloud CDN for static content
- [ ] Use Standard network tier where acceptable
- [ ] Set up budget alerts and anomaly detection
- [ ] Export billing data to BigQuery for analysis
- [ ] Review cost recommendations monthly
