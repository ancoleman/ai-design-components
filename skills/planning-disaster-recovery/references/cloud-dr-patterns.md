# Cloud-Specific DR Patterns

## Table of Contents

1. [AWS](#aws)
2. [GCP](#gcp)
3. [Azure](#azure)

## AWS

### RDS Multi-AZ and Read Replicas

**Multi-AZ (Synchronous Replication):**
- Automatic failover within same region
- RPO: Near-zero (synchronous)
- RTO: 1-2 minutes (automatic)

**Cross-Region Read Replica (Asynchronous):**
- Manual promotion required
- RPO: Seconds to minutes (asynchronous lag)
- RTO: 5-15 minutes (manual promotion + DNS update)

### Aurora Global Database

**Configuration Example:**
```hcl
resource "aws_rds_global_cluster" "main" {
  global_cluster_identifier = "prod-global"
  engine                    = "aurora-postgresql"
  engine_version            = "14.7"
}

resource "aws_rds_cluster" "primary" {
  cluster_identifier        = "prod-primary"
  global_cluster_identifier = aws_rds_global_cluster.main.id
  backup_retention_period   = 30
}

resource "aws_rds_cluster" "secondary" {
  provider                  = aws.eu-west-1
  cluster_identifier        = "prod-secondary"
  global_cluster_identifier = aws_rds_global_cluster.main.id
}
```

**Failover Process:**
```bash
aws rds remove-from-global-cluster \
  --region eu-west-1 \
  --global-cluster-identifier prod-global \
  --db-cluster-identifier prod-secondary
```

### S3 Cross-Region Replication

**With Replication Time Control (15-min SLA):**
```hcl
resource "aws_s3_bucket_replication_configuration" "crr" {
  rule {
    status = "Enabled"
    destination {
      bucket = aws_s3_bucket.replica.arn
      replication_time {
        status = "Enabled"
        time { minutes = 15 }
      }
      metrics {
        status = "Enabled"
        event_threshold { minutes = 15 }
      }
    }
  }
}
```

## GCP

### Cloud SQL High Availability

**Regional HA (Synchronous):**
```hcl
resource "google_sql_database_instance" "main" {
  settings {
    availability_type = "REGIONAL"
    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = true
      transaction_log_retention_days = 7
    }
  }
}
```

**Cross-Region Read Replica:**
```hcl
resource "google_sql_database_instance" "replica" {
  master_instance_name = google_sql_database_instance.main.name
  region               = "us-west1"
  
  replica_configuration {
    failover_target = false
  }
}
```

### GCS Multi-Regional Storage

```hcl
resource "google_storage_bucket" "backups" {
  location      = "US"  # Multi-region
  storage_class = "STANDARD"
  
  versioning { enabled = true }
  
  lifecycle_rule {
    condition { age = 30 }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }
}
```

## Azure

### Azure SQL Geo-Replication

```hcl
resource "azurerm_mssql_database" "primary" {
  name      = "prod-db"
  server_id = azurerm_mssql_server.primary.id
  sku_name  = "S3"
  
  short_term_retention_policy {
    retention_days = 35
  }
  
  long_term_retention_policy {
    weekly_retention  = "P12W"
    monthly_retention = "P12M"
    yearly_retention  = "P5Y"
  }
}

resource "azurerm_mssql_database_extended_auditing_policy" "primary" {
  database_id = azurerm_mssql_database.primary.id
  retention_in_days = 90
}
```

### Azure Site Recovery

```hcl
resource "azurerm_site_recovery_replicated_vm" "vm" {
  name                                      = "replicated-vm"
  resource_group_name                       = azurerm_resource_group.secondary.name
  recovery_vault_name                       = azurerm_recovery_services_vault.vault.name
  source_recovery_fabric_name               = azurerm_site_recovery_fabric.primary.name
  source_vm_id                              = azurerm_virtual_machine.vm.id
  target_recovery_fabric_id                 = azurerm_site_recovery_fabric.secondary.id
  target_resource_group_id                  = azurerm_resource_group.secondary.id
  target_recovery_protection_container_id   = azurerm_site_recovery_protection_container.secondary.id
  target_availability_set_id                = azurerm_availability_set.secondary.id
  
  managed_disk {
    disk_id                    = azurerm_managed_disk.vm.id
    staging_storage_account_id = azurerm_storage_account.cache.id
    target_resource_group_id   = azurerm_resource_group.secondary.id
    target_disk_type           = "Premium_LRS"
    target_replica_disk_type   = "Premium_LRS"
  }
}
```
