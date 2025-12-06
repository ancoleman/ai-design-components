# Cloud Hardening Reference

Comprehensive guide to hardening AWS, GCP, and Azure cloud configurations using least privilege, encryption, and CSPM tools.

## Table of Contents

1. [AWS Hardening](#aws-hardening)
2. [GCP Hardening](#gcp-hardening)
3. [Azure Hardening](#azure-hardening)
4. [Multi-Cloud Patterns](#multi-cloud-patterns)
5. [Cloud Security Posture Management](#cloud-security-posture-management)

---

## AWS Hardening

### IAM Hardening

**Principle: Least Privilege with MFA**

```hcl
# terraform/aws/iam-hardening.tf

# Deny all actions without MFA
resource "aws_iam_policy" "mfa_required" {
  name        = "mfa-required-sensitive"
  description = "Require MFA for sensitive operations"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "DenyWithoutMFA"
        Effect = "Deny"
        Action = [
          "iam:*",
          "organizations:*",
          "account:*",
          "ec2:TerminateInstances",
          "rds:DeleteDBInstance",
          "s3:DeleteBucket"
        ]
        Resource = "*"
        Condition = {
          BoolIfExists = {
            "aws:MultiFactorAuthPresent" = "false"
          }
        }
      }
    ]
  })
}

# Least privilege application role
resource "aws_iam_role" "app_role" {
  name = "app-least-privilege"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_policy" "app_policy" {
  name = "app-specific-permissions"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "S3ReadOnly"
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.app_data.arn,
          "${aws_s3_bucket.app_data.arn}/*"
        ]
      },
      {
        Sid    = "SecretsManagerRead"
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = aws_secretsmanager_secret.app_secrets.arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "app_attach" {
  role       = aws_iam_role.app_role.name
  policy_arn = aws_iam_policy.app_policy.arn
}
```

**IAM Best Practices:**
- Enable MFA for all human users
- Use roles instead of access keys
- Rotate access keys regularly (90 days)
- Use SCPs (Service Control Policies) for organization-wide controls
- Enable CloudTrail for IAM action logging

### S3 Bucket Hardening

```hcl
# terraform/aws/s3-hardening.tf

resource "aws_s3_bucket" "secure" {
  bucket = "company-secure-bucket"
}

# Block all public access
resource "aws_s3_bucket_public_access_block" "secure" {
  bucket = aws_s3_bucket.secure.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Enable versioning (protects against accidental deletion)
resource "aws_s3_bucket_versioning" "secure" {
  bucket = aws_s3_bucket.secure.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Enable encryption at rest
resource "aws_s3_bucket_server_side_encryption_configuration" "secure" {
  bucket = aws_s3_bucket.secure.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.s3.arn
    }
    bucket_key_enabled = true
  }
}

# Enable access logging
resource "aws_s3_bucket_logging" "secure" {
  bucket = aws_s3_bucket.secure.id

  target_bucket = aws_s3_bucket.logs.id
  target_prefix = "s3-access-logs/"
}

# Enforce TLS for data in transit
resource "aws_s3_bucket_policy" "enforce_tls" {
  bucket = aws_s3_bucket.secure.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid    = "DenyInsecureTransport"
      Effect = "Deny"
      Principal = "*"
      Action = "s3:*"
      Resource = [
        aws_s3_bucket.secure.arn,
        "${aws_s3_bucket.secure.arn}/*"
      ]
      Condition = {
        Bool = {
          "aws:SecureTransport" = "false"
        }
      }
    }]
  })
}

# Lifecycle policy (optional: delete old versions)
resource "aws_s3_bucket_lifecycle_configuration" "secure" {
  bucket = aws_s3_bucket.secure.id

  rule {
    id     = "expire-old-versions"
    status = "Enabled"

    noncurrent_version_expiration {
      noncurrent_days = 90
    }
  }
}
```

### VPC and Network Hardening

```hcl
# terraform/aws/vpc-hardening.tf

# VPC with private subnets
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "secure-vpc"
  }
}

# Enable VPC Flow Logs
resource "aws_flow_log" "main" {
  vpc_id          = aws_vpc.main.id
  traffic_type    = "ALL"
  iam_role_arn    = aws_iam_role.flow_logs.arn
  log_destination = aws_cloudwatch_log_group.flow_logs.arn
}

# Security group: default deny
resource "aws_security_group" "app" {
  name        = "app-hardened"
  description = "Hardened application security group"
  vpc_id      = aws_vpc.main.id

  # No ingress rules (add explicitly as needed)

  # Egress: only HTTPS
  egress {
    description = "HTTPS outbound"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Egress: Database access
  egress {
    description     = "Database access"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.db.id]
  }

  tags = {
    Name = "app-hardened"
  }
}

# Enable GuardDuty
resource "aws_guardduty_detector" "main" {
  enable = true

  datasources {
    s3_logs {
      enable = true
    }
    kubernetes {
      audit_logs {
        enable = true
      }
    }
  }
}
```

### RDS Database Hardening

```hcl
# terraform/aws/rds-hardening.tf

resource "aws_db_instance" "hardened" {
  identifier = "hardened-postgres"

  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.t3.medium"

  # Storage
  allocated_storage     = 100
  storage_encrypted     = true
  kms_key_id            = aws_kms_key.rds.arn
  storage_type          = "gp3"

  # Network isolation
  publicly_accessible    = false
  db_subnet_group_name   = aws_db_subnet_group.private.name
  vpc_security_group_ids = [aws_security_group.db.id]

  # Authentication
  username                            = "dbadmin"
  manage_master_user_password         = true  # AWS Secrets Manager
  iam_database_authentication_enabled = true

  # Backup and recovery
  backup_retention_period = 30
  backup_window          = "03:00-04:00"
  copy_tags_to_snapshot  = true
  skip_final_snapshot    = false
  final_snapshot_identifier = "hardened-postgres-final"

  # Maintenance
  auto_minor_version_upgrade = true
  maintenance_window         = "Mon:04:00-Mon:05:00"

  # Logging
  enabled_cloudwatch_logs_exports = [
    "postgresql",
    "upgrade"
  ]

  # Deletion protection
  deletion_protection = true

  # Performance Insights
  performance_insights_enabled    = true
  performance_insights_kms_key_id = aws_kms_key.rds.arn

  tags = {
    Name = "hardened-postgres"
  }
}

# Database parameter group hardening
resource "aws_db_parameter_group" "hardened" {
  name   = "postgres-hardened"
  family = "postgres15"

  parameter {
    name  = "log_statement"
    value = "all"  # Log all SQL statements
  }

  parameter {
    name  = "log_connections"
    value = "1"  # Log connection attempts
  }

  parameter {
    name  = "log_disconnections"
    value = "1"  # Log disconnections
  }

  parameter {
    name  = "rds.force_ssl"
    value = "1"  # Require SSL connections
  }
}
```

### AWS Config Rules

```hcl
# terraform/aws/config-hardening.tf

resource "aws_config_configuration_recorder" "main" {
  name     = "config-recorder"
  role_arn = aws_iam_role.config.arn

  recording_group {
    all_supported                 = true
    include_global_resource_types = true
  }
}

# Check S3 bucket public access
resource "aws_config_config_rule" "s3_bucket_public_read_prohibited" {
  name = "s3-bucket-public-read-prohibited"

  source {
    owner             = "AWS"
    source_identifier = "S3_BUCKET_PUBLIC_READ_PROHIBITED"
  }

  depends_on = [aws_config_configuration_recorder.main]
}

# Check S3 bucket encryption
resource "aws_config_config_rule" "s3_bucket_server_side_encryption_enabled" {
  name = "s3-bucket-server-side-encryption-enabled"

  source {
    owner             = "AWS"
    source_identifier = "S3_BUCKET_SERVER_SIDE_ENCRYPTION_ENABLED"
  }

  depends_on = [aws_config_configuration_recorder.main]
}

# Check RDS encryption
resource "aws_config_config_rule" "rds_storage_encrypted" {
  name = "rds-storage-encrypted"

  source {
    owner             = "AWS"
    source_identifier = "RDS_STORAGE_ENCRYPTED"
  }

  depends_on = [aws_config_configuration_recorder.main]
}

# Check MFA for root account
resource "aws_config_config_rule" "root_account_mfa_enabled" {
  name = "root-account-mfa-enabled"

  source {
    owner             = "AWS"
    source_identifier = "ROOT_ACCOUNT_MFA_ENABLED"
  }

  depends_on = [aws_config_configuration_recorder.main]
}
```

---

## GCP Hardening

### IAM and Service Accounts

```hcl
# terraform/gcp/iam-hardening.tf

# Service account with minimal permissions
resource "google_service_account" "app" {
  account_id   = "app-service-account"
  display_name = "Application Service Account"
  project      = var.project_id
}

# Grant minimal permissions
resource "google_project_iam_member" "app_storage_reader" {
  project = var.project_id
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.app.email}"

  condition {
    title       = "access_specific_bucket"
    description = "Access only to app-data bucket"
    expression  = "resource.name.startsWith('projects/_/buckets/app-data')"
  }
}

# Workload Identity for GKE
resource "google_service_account_iam_member" "workload_identity" {
  service_account_id = google_service_account.app.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[${var.namespace}/${var.ksa_name}]"
}
```

### Cloud Storage Hardening

```hcl
# terraform/gcp/storage-hardening.tf

resource "google_storage_bucket" "secure" {
  name     = "company-secure-bucket"
  location = "US"
  project  = var.project_id

  # Prevent public access
  public_access_prevention = "enforced"

  # Enable uniform bucket-level access
  uniform_bucket_level_access {
    enabled = true
  }

  # Enable versioning
  versioning {
    enabled = true
  }

  # Encryption
  encryption {
    default_kms_key_name = google_kms_crypto_key.bucket.id
  }

  # Lifecycle rules
  lifecycle_rule {
    condition {
      num_newer_versions = 3
    }
    action {
      type = "Delete"
    }
  }

  # Logging
  logging {
    log_bucket        = google_storage_bucket.logs.name
    log_object_prefix = "storage-logs/"
  }

  # Labels
  labels = {
    environment = "production"
    compliance  = "required"
  }
}

# Bucket IAM: deny public access
resource "google_storage_bucket_iam_member" "no_public_access" {
  bucket = google_storage_bucket.secure.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.app.email}"
}
```

### VPC and Firewall Hardening

```hcl
# terraform/gcp/vpc-hardening.tf

# VPC with private IP ranges
resource "google_compute_network" "secure" {
  name                    = "secure-vpc"
  auto_create_subnetworks = false
  project                 = var.project_id
}

resource "google_compute_subnetwork" "private" {
  name          = "private-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = "us-central1"
  network       = google_compute_network.secure.id
  project       = var.project_id

  # Enable VPC Flow Logs
  log_config {
    aggregation_interval = "INTERVAL_10_MIN"
    flow_sampling        = 0.5
    metadata             = "INCLUDE_ALL_METADATA"
  }

  # Private Google Access
  private_ip_google_access = true
}

# Firewall: default deny
resource "google_compute_firewall" "deny_all" {
  name    = "deny-all"
  network = google_compute_network.secure.name
  project = var.project_id

  deny {
    protocol = "all"
  }

  source_ranges = ["0.0.0.0/0"]
  priority      = 65534
}

# Firewall: allow specific traffic
resource "google_compute_firewall" "allow_app" {
  name    = "allow-app"
  network = google_compute_network.secure.name
  project = var.project_id

  allow {
    protocol = "tcp"
    ports    = ["8080"]
  }

  source_tags = ["frontend"]
  target_tags = ["app"]
  priority    = 1000
}
```

### Cloud SQL Hardening

```hcl
# terraform/gcp/cloudsql-hardening.tf

resource "google_sql_database_instance" "hardened" {
  name             = "hardened-postgres"
  database_version = "POSTGRES_15"
  region           = "us-central1"
  project          = var.project_id

  settings {
    tier              = "db-custom-2-7680"
    availability_type = "REGIONAL"  # High availability

    # Backup configuration
    backup_configuration {
      enabled                        = true
      start_time                     = "03:00"
      point_in_time_recovery_enabled = true
      backup_retention_settings {
        retained_backups = 30
      }
    }

    # IP configuration
    ip_configuration {
      ipv4_enabled    = false  # No public IP
      private_network = google_compute_network.secure.id
      require_ssl     = true
    }

    # Database flags
    database_flags {
      name  = "log_connections"
      value = "on"
    }

    database_flags {
      name  = "log_disconnections"
      value = "on"
    }

    database_flags {
      name  = "log_statement"
      value = "all"
    }

    # Maintenance window
    maintenance_window {
      day          = 1  # Monday
      hour         = 4
      update_track = "stable"
    }

    # Insights
    insights_config {
      query_insights_enabled  = true
      query_plans_per_minute  = 5
      query_string_length     = 1024
      record_application_tags = true
    }
  }

  deletion_protection = true
}
```

---

## Azure Hardening

### Azure AD and RBAC

```hcl
# terraform/azure/rbac-hardening.tf

# Custom role with minimal permissions
resource "azurerm_role_definition" "app_reader" {
  name        = "App Reader"
  scope       = data.azurerm_subscription.primary.id
  description = "Can read app-specific resources only"

  permissions {
    actions = [
      "Microsoft.Storage/storageAccounts/blobServices/containers/read",
      "Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read"
    ]
    not_actions = []
  }

  assignable_scopes = [
    data.azurerm_subscription.primary.id
  ]
}

# Assign role to managed identity
resource "azurerm_role_assignment" "app_reader" {
  scope                = azurerm_storage_account.app.id
  role_definition_name = azurerm_role_definition.app_reader.name
  principal_id         = azurerm_user_assigned_identity.app.principal_id
}

# Managed identity for applications
resource "azurerm_user_assigned_identity" "app" {
  name                = "app-identity"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
}
```

### Storage Account Hardening

```hcl
# terraform/azure/storage-hardening.tf

resource "azurerm_storage_account" "secure" {
  name                     = "companysecurestorage"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "GRS"

  # Disable public access
  allow_nested_items_to_be_public = false
  public_network_access_enabled   = false

  # Require HTTPS
  enable_https_traffic_only = true
  min_tls_version          = "TLS1_2"

  # Network rules
  network_rules {
    default_action             = "Deny"
    virtual_network_subnet_ids = [azurerm_subnet.app.id]
    bypass                     = ["AzureServices"]
  }

  # Blob properties
  blob_properties {
    versioning_enabled = true

    delete_retention_policy {
      days = 30
    }

    container_delete_retention_policy {
      days = 30
    }
  }

  # Encryption
  infrastructure_encryption_enabled = true

  identity {
    type = "SystemAssigned"
  }

  tags = {
    environment = "production"
  }
}

# Enable encryption with customer-managed key
resource "azurerm_storage_account_customer_managed_key" "secure" {
  storage_account_id = azurerm_storage_account.secure.id
  key_vault_id       = azurerm_key_vault.main.id
  key_name           = azurerm_key_vault_key.storage.name
}
```

### Network Security Groups

```hcl
# terraform/azure/nsg-hardening.tf

resource "azurerm_network_security_group" "app" {
  name                = "app-nsg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

# Deny all inbound (default)
resource "azurerm_network_security_rule" "deny_all_inbound" {
  name                        = "DenyAllInbound"
  priority                    = 4096
  direction                   = "Inbound"
  access                      = "Deny"
  protocol                    = "*"
  source_port_range           = "*"
  destination_port_range      = "*"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.main.name
  network_security_group_name = azurerm_network_security_group.app.name
}

# Allow specific traffic
resource "azurerm_network_security_rule" "allow_app" {
  name                        = "AllowApp"
  priority                    = 1000
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "8080"
  source_address_prefixes     = azurerm_subnet.frontend.address_prefixes
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.main.name
  network_security_group_name = azurerm_network_security_group.app.name
}
```

---

## Multi-Cloud Patterns

### Common Hardening Patterns

**1. Zero Trust Network Access:**
- Authenticate every request
- Verify device posture
- Enforce least privilege
- Log all access

**2. Encryption Everywhere:**
- At rest: KMS/CMEK for all storage
- In transit: TLS 1.2+ for all connections
- Key rotation: Automated, regular

**3. Centralized Logging:**
- CloudTrail (AWS), Cloud Logging (GCP), Azure Monitor
- Ship to SIEM (Splunk, ELK, Datadog)
- Retention: 90+ days

**4. Automated Compliance:**
- AWS Config, GCP Security Command Center, Azure Policy
- Continuous compliance monitoring
- Automated remediation where possible

---

## Cloud Security Posture Management

### Prowler (AWS)

```bash
# Install Prowler
pip install prowler

# Run comprehensive AWS scan
prowler aws --services s3 iam ec2 rds vpc

# Run CIS benchmark
prowler aws --compliance cis_2.0_aws

# Output to JSON
prowler aws --output-modes json --output-directory ./reports/
```

### ScoutSuite (Multi-Cloud)

```bash
# Install ScoutSuite
pip install scoutsuite

# Scan AWS
scout aws --report-dir ./reports/aws/

# Scan GCP
scout gcp --project-id my-project --report-dir ./reports/gcp/

# Scan Azure
scout azure --report-dir ./reports/azure/
```

### Checkov (IaC Scanning)

```bash
# Install Checkov
pip install checkov

# Scan Terraform
checkov -d terraform/ --framework terraform

# Scan CloudFormation
checkov -f cloudformation-template.yaml --framework cloudformation

# CI/CD integration
checkov -d terraform/ --output json --quiet --compact
```

---

## Additional Resources

- AWS Security Best Practices: https://aws.amazon.com/security/best-practices/
- GCP Security Best Practices: https://cloud.google.com/security/best-practices
- Azure Security Best Practices: https://learn.microsoft.com/en-us/azure/security/fundamentals/best-practices-and-patterns
- CIS AWS Benchmark: https://www.cisecurity.org/benchmark/amazon_web_services
- Prowler: https://github.com/prowler-cloud/prowler
- ScoutSuite: https://github.com/nccgroup/ScoutSuite
