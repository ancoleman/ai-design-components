# GCP Storage and Database Services Reference

Detailed patterns for Google Cloud Platform storage and database services.

## Table of Contents

1. [Cloud Storage](#cloud-storage)
2. [Cloud SQL](#cloud-sql)
3. [Cloud Spanner](#cloud-spanner)
4. [Firestore](#firestore)
5. [Bigtable](#bigtable)
6. [AlloyDB](#alloydb)
7. [Memorystore](#memorystore)
8. [Service Selection Guide](#service-selection-guide)

---

## Cloud Storage

### Storage Classes

| Class | Access Pattern | Min Storage Duration | Retrieval Cost | Use Case |
|-------|----------------|---------------------|----------------|----------|
| **Standard** | Frequent | None | None | Hot data, static websites |
| **Nearline** | Once/month | 30 days | $0.01/GB | Backups, infrequent access |
| **Coldline** | Once/quarter | 90 days | $0.02/GB | Disaster recovery |
| **Archive** | Once/year | 365 days | $0.05/GB | Long-term archival |

### Terraform Configuration

```hcl
# Standard bucket with lifecycle rules
resource "google_storage_bucket" "main" {
  name          = "my-bucket"
  location      = "US"  # Multi-region
  storage_class = "STANDARD"

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }

  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type          = "SetStorageClass"
      storage_class = "COLDLINE"
    }
  }

  lifecycle_rule {
    condition {
      age = 365
    }
    action {
      type          = "SetStorageClass"
      storage_class = "ARCHIVE"
    }
  }

  uniform_bucket_level_access = true

  cors {
    origin          = ["https://example.com"]
    method          = ["GET", "HEAD", "PUT", "POST", "DELETE"]
    response_header = ["*"]
    max_age_seconds = 3600
  }
}

# IAM binding
resource "google_storage_bucket_iam_member" "viewer" {
  bucket = google_storage_bucket.main.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:app@project.iam.gserviceaccount.com"
}
```

---

## Cloud SQL

### When to Use Cloud SQL

- Standard relational database needs (PostgreSQL, MySQL, SQL Server)
- Up to 96TB storage
- Regional deployment
- Read replicas and HA required

### High Availability Configuration

```hcl
resource "google_sql_database_instance" "main" {
  name             = "main-db"
  database_version = "POSTGRES_15"
  region           = "us-central1"

  settings {
    tier              = "db-custom-4-16384"  # 4 vCPU, 16GB RAM
    availability_type = "REGIONAL"           # HA with automatic failover
    disk_size         = 100
    disk_type         = "PD_SSD"
    disk_autoresize   = true

    backup_configuration {
      enabled                        = true
      start_time                     = "03:00"
      point_in_time_recovery_enabled = true
      transaction_log_retention_days = 7
      backup_retention_settings {
        retained_backups = 7
      }
    }

    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.main.id
      require_ssl     = true
    }

    database_flags {
      name  = "max_connections"
      value = "200"
    }

    insights_config {
      query_insights_enabled  = true
      query_string_length     = 1024
      record_application_tags = true
    }
  }

  deletion_protection = true
}

# Read replica
resource "google_sql_database_instance" "replica" {
  name                 = "read-replica"
  master_instance_name = google_sql_database_instance.main.name
  region               = "us-east1"
  database_version     = "POSTGRES_15"

  replica_configuration {
    failover_target = false
  }

  settings {
    tier              = "db-custom-4-16384"
    availability_type = "ZONAL"
    disk_autoresize   = true
  }
}
```

---

## Cloud Spanner

### When to Use Cloud Spanner

- Global transactions with strong consistency
- Multi-region active-active deployment
- Unlimited horizontal scaling
- 99.999% availability SLA required

### Configuration

```hcl
resource "google_spanner_instance" "main" {
  config       = "nam3"  # North America multi-region
  display_name = "Production Spanner"
  num_nodes    = 2

  autoscaling_config {
    autoscaling_limits {
      min_nodes = 2
      max_nodes = 10
    }
    autoscaling_targets {
      high_priority_cpu_utilization_percent = 65
      storage_utilization_percent           = 85
    }
  }

  labels = {
    environment = "production"
  }
}

resource "google_spanner_database" "database" {
  instance = google_spanner_instance.main.name
  name     = "app-database"
  ddl = [
    "CREATE TABLE Users (UserId INT64 NOT NULL, Email STRING(MAX), Name STRING(MAX)) PRIMARY KEY (UserId)",
    "CREATE INDEX UsersByEmail ON Users(Email)",
  ]

  deletion_protection = true
}
```

---

## Firestore

### When to Use Firestore

- Mobile and web applications
- Real-time synchronization required
- Offline support needed
- Document-based data model
- Flexible schema

### Configuration

```hcl
resource "google_firestore_database" "database" {
  project     = var.project_id
  name        = "(default)"
  location_id = "nam5"  # Multi-region
  type        = "FIRESTORE_NATIVE"

  concurrency_mode = "OPTIMISTIC"
  app_engine_integration_mode = "DISABLED"
}

# Index for complex queries
resource "google_firestore_index" "users_by_created" {
  project    = var.project_id
  collection = "users"

  fields {
    field_path = "status"
    order      = "ASCENDING"
  }

  fields {
    field_path = "created_at"
    order      = "DESCENDING"
  }
}
```

### Python Client Example

```python
from google.cloud import firestore

db = firestore.Client()

# Write document
doc_ref = db.collection('users').document('user_123')
doc_ref.set({
    'name': 'John Doe',
    'email': 'john@example.com',
    'created_at': firestore.SERVER_TIMESTAMP
})

# Query with real-time listener
def on_snapshot(docs, changes, read_time):
    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')

query = db.collection('users').where('status', '==', 'active')
query.on_snapshot(on_snapshot)

# Batch write
batch = db.batch()
for i in range(100):
    doc_ref = db.collection('items').document(f'item_{i}')
    batch.set(doc_ref, {'value': i})
batch.commit()
```

---

## Bigtable

### When to Use Bigtable

- Time-series data (IoT sensors, financial ticks)
- High throughput (>1M ops/sec)
- Single-digit millisecond latency
- Petabyte-scale data
- HBase API compatibility

### Configuration

```hcl
resource "google_bigtable_instance" "main" {
  name = "production-instance"

  cluster {
    cluster_id   = "us-central1-cluster"
    zone         = "us-central1-a"
    num_nodes    = 3
    storage_type = "SSD"

    autoscaling_config {
      min_nodes      = 3
      max_nodes      = 10
      cpu_target     = 60
      storage_target = 2560  # GB
    }
  }

  cluster {
    cluster_id   = "us-east1-cluster"
    zone         = "us-east1-b"
    num_nodes    = 3
    storage_type = "SSD"
  }

  deletion_protection = true
}

resource "google_bigtable_table" "time_series" {
  name          = "time_series"
  instance_name = google_bigtable_instance.main.name

  column_family {
    family = "metrics"
  }

  column_family {
    family = "metadata"
  }
}
```

---

## AlloyDB

### When to Use AlloyDB

- PostgreSQL migration from on-premises
- Need 4x faster performance than standard PostgreSQL
- Analytical queries on transactional data
- Machine learning integration required

### Configuration

```hcl
resource "google_alloydb_cluster" "main" {
  cluster_id = "alloydb-cluster"
  location   = "us-central1"
  network    = google_compute_network.main.id

  initial_user {
    user     = "admin"
    password = random_password.alloydb.result
  }

  automated_backup_policy {
    backup_window = "03:00-05:00"
    enabled       = true
    location      = "us-central1"

    quantity_based_retention {
      count = 7
    }
  }
}

resource "google_alloydb_instance" "primary" {
  cluster       = google_alloydb_cluster.main.name
  instance_id   = "primary-instance"
  instance_type = "PRIMARY"

  machine_config {
    cpu_count = 8
  }

  availability_type = "REGIONAL"
}
```

---

## Memorystore

### When to Use Memorystore

- Application caching
- Session storage
- Real-time analytics
- Leaderboards and counters

### Redis Configuration

```hcl
resource "google_redis_instance" "cache" {
  name           = "app-cache"
  tier           = "STANDARD_HA"
  memory_size_gb = 5
  region         = "us-central1"

  redis_version     = "REDIS_7_0"
  display_name      = "Application Cache"
  reserved_ip_range = "10.137.125.0/29"

  authorized_network = google_compute_network.main.id

  redis_configs = {
    maxmemory-policy = "allkeys-lru"
  }

  maintenance_policy {
    weekly_maintenance_window {
      day = "SUNDAY"
      start_time {
        hours   = 3
        minutes = 0
      }
    }
  }
}
```

---

## Service Selection Guide

### Decision Matrix

| Requirement | Service | Configuration |
|-------------|---------|---------------|
| **Objects/files** | Cloud Storage | Standard/Nearline/Coldline/Archive |
| **RDBMS <96TB** | Cloud SQL | PostgreSQL/MySQL/SQL Server |
| **RDBMS >96TB** | AlloyDB or Spanner | AlloyDB for single-region, Spanner for multi-region |
| **Global SQL** | Cloud Spanner | Multi-region config |
| **Document NoSQL** | Firestore | Mobile/web apps with offline |
| **Time-series** | Bigtable | IoT, financial, high throughput |
| **Caching** | Memorystore | Redis or Memcached |
| **Analytics** | BigQuery | Petabyte-scale warehouse |

### Cost Comparison (Monthly Estimate)

| Service | Typical Config | Approx Cost |
|---------|----------------|-------------|
| Cloud Storage (Standard, 1TB) | 1TB storage | $20 |
| Cloud SQL (db-custom-2-8192) | 2 vCPU, 8GB, 100GB SSD | $200 |
| Cloud Spanner (2 nodes) | 2 nodes, nam3 | $1,300 |
| Firestore | 1GB, 50K reads, 20K writes/day | $1 |
| Bigtable (3 nodes, SSD) | 3 nodes, 1TB storage | $1,500 |
| Memorystore Redis (5GB, HA) | 5GB memory, HA | $200 |

### Performance Characteristics

| Service | Latency | Throughput | Max Size |
|---------|---------|------------|----------|
| Cloud Storage | 10-100ms | GB/s | Unlimited |
| Cloud SQL | 1-10ms | 10K QPS | 96TB |
| Cloud Spanner | 5-10ms | 100K+ QPS | Unlimited |
| Firestore | 10-50ms | 10K writes/s | Unlimited |
| Bigtable | <10ms | >1M ops/s | Petabytes |
| Memorystore | <1ms | 1M+ ops/s | 300GB |
| AlloyDB | <5ms | 100K+ QPS | 64TB |
