# Encryption Implementations


## Table of Contents

- [Overview](#overview)
- [Encryption at Rest](#encryption-at-rest)
  - [AWS Implementation](#aws-implementation)
  - [Azure Implementation](#azure-implementation)
  - [GCP Implementation](#gcp-implementation)
- [Encryption in Transit](#encryption-in-transit)
  - [TLS Configuration](#tls-configuration)
  - [Database Connection Encryption](#database-connection-encryption)
- [Key Management](#key-management)
  - [Key Rotation](#key-rotation)
  - [Key Access Policies](#key-access-policies)
- [Encryption Validation](#encryption-validation)
  - [OPA Policy](#opa-policy)

## Overview

Encryption requirements across compliance frameworks:
- **Algorithm:** AES-256 for data at rest, TLS 1.3 for data in transit
- **Key Management:** Centralized KMS with automatic rotation
- **Scope:** All sensitive data (PHI, PII, cardholder data, confidential information)
- **Framework Requirements:** SOC 2 (CC6.1), HIPAA (§164.312), PCI-DSS (Req 3-4), GDPR (Art 32)

## Encryption at Rest

### AWS Implementation

#### S3 Buckets

```hcl
# terraform/s3_encryption.tf
resource "aws_kms_key" "data" {
  description             = "Data encryption key for compliance"
  deletion_window_in_days = 30
  enable_key_rotation     = true  # PCI-DSS Req 3.6

  tags = {
    Compliance = "ENC-001,ENC-003"
    Frameworks = "SOC2-CC6.1,HIPAA-164.312(a)(2)(iv),PCI-DSS-Req3.4,GDPR-Art32"
    Purpose    = "data-encryption"
  }
}

resource "aws_kms_alias" "data" {
  name          = "alias/${var.environment}-data-key"
  target_key_id = aws_kms_key.data.id
}

resource "aws_s3_bucket" "data" {
  bucket = "company-data-${var.environment}"

  tags = {
    Compliance = "ENC-001,DATA-001"
    Environment = var.environment
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.data.arn
    }
    bucket_key_enabled = true  # Reduces KMS API calls
  }
}

# Block public access
resource "aws_s3_bucket_public_access_block" "data" {
  bucket = aws_s3_bucket.data.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Versioning for data integrity
resource "aws_s3_bucket_versioning" "data" {
  bucket = aws_s3_bucket.data.id
  versioning_configuration {
    status = "Enabled"
  }
}
```

#### RDS Databases

```hcl
# terraform/rds_encryption.tf
resource "aws_db_instance" "main" {
  identifier     = "${var.environment}-database"
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.t3.medium"

  # Encryption (HIPAA, PCI-DSS, GDPR)
  storage_encrypted = true
  kms_key_id       = aws_kms_key.data.arn

  # Backup encryption
  backup_retention_period = 30  # 30 days
  backup_window          = "03:00-04:00"

  # Enable IAM authentication
  iam_database_authentication_enabled = true

  # Network isolation
  db_subnet_group_name   = aws_db_subnet_group.private.name
  vpc_security_group_ids = [aws_security_group.database.id]
  publicly_accessible    = false

  # Logging for audit trail
  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]

  tags = {
    Compliance = "ENC-001,LOG-001"
    Frameworks = "HIPAA-164.312(a)(2)(iv),PCI-DSS-Req3.4"
  }
}

# Aurora encryption
resource "aws_rds_cluster" "aurora" {
  cluster_identifier = "${var.environment}-aurora"
  engine            = "aurora-postgresql"
  engine_version    = "15.4"

  storage_encrypted = true
  kms_key_id       = aws_kms_key.data.arn

  # Enable audit logging
  enabled_cloudwatch_logs_exports = ["postgresql"]

  tags = {
    Compliance = "ENC-001"
  }
}
```

#### EBS Volumes

```hcl
# terraform/ebs_encryption.tf
# Enable EBS encryption by default
resource "aws_ebs_encryption_by_default" "enabled" {
  enabled = true
}

# Set default KMS key for EBS
resource "aws_ebs_default_kms_key" "default" {
  key_arn = aws_kms_key.data.arn
}

# Explicit volume encryption
resource "aws_ebs_volume" "data" {
  availability_zone = var.availability_zone
  size             = 100
  type             = "gp3"

  encrypted  = true
  kms_key_id = aws_kms_key.data.arn

  tags = {
    Compliance = "ENC-001"
  }
}
```

#### DynamoDB Tables

```hcl
# terraform/dynamodb_encryption.tf
resource "aws_dynamodb_table" "sessions" {
  name           = "${var.environment}-sessions"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "session_id"

  # Server-side encryption
  server_side_encryption {
    enabled     = true
    kms_key_arn = aws_kms_key.data.arn
  }

  # Point-in-time recovery
  point_in_time_recovery {
    enabled = true
  }

  attribute {
    name = "session_id"
    type = "S"
  }

  ttl {
    enabled        = true
    attribute_name = "expiration_time"
  }

  tags = {
    Compliance = "ENC-001,DATA-002"
  }
}
```

### Azure Implementation

```hcl
# terraform/azure_encryption.tf
# Storage Account with encryption
resource "azurerm_storage_account" "data" {
  name                     = "companydata${var.environment}"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "GRS"

  # Encryption at rest
  enable_https_traffic_only = true
  min_tls_version          = "TLS1_3"

  # Customer-managed key
  identity {
    type = "SystemAssigned"
  }

  customer_managed_key {
    key_vault_key_id          = azurerm_key_vault_key.storage.id
    user_assigned_identity_id = azurerm_user_assigned_identity.storage.id
  }

  tags = {
    Compliance = "ENC-001,ENC-002"
  }
}

# Key Vault for key management
resource "azurerm_key_vault" "main" {
  name                = "company-kv-${var.environment}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tenant_id           = data.azurerm_client_config.current.tenant_id

  sku_name = "premium"  # HSM-backed keys

  enabled_for_disk_encryption = true
  soft_delete_retention_days  = 90
  purge_protection_enabled    = true

  tags = {
    Compliance = "ENC-003"
  }
}

# Azure SQL encryption
resource "azurerm_mssql_server" "main" {
  name                         = "company-sql-${var.environment}"
  resource_group_name          = azurerm_resource_group.main.name
  location                     = azurerm_resource_group.main.location
  version                      = "12.0"
  administrator_login          = var.sql_admin_username
  administrator_login_password = var.sql_admin_password
  minimum_tls_version          = "1.3"

  azuread_administrator {
    login_username = var.azuread_admin_username
    object_id      = var.azuread_admin_object_id
  }

  tags = {
    Compliance = "ENC-001,ENC-002"
  }
}

resource "azurerm_mssql_database" "main" {
  name      = "company-db"
  server_id = azurerm_mssql_server.main.id
  sku_name  = "S1"

  # Transparent Data Encryption (TDE)
  transparent_data_encryption_enabled = true
}
```

### GCP Implementation

```hcl
# terraform/gcp_encryption.tf
# KMS Key Ring
resource "google_kms_key_ring" "main" {
  name     = "company-keyring-${var.environment}"
  location = var.region
}

# KMS Crypto Key
resource "google_kms_crypto_key" "data" {
  name            = "data-encryption-key"
  key_ring        = google_kms_key_ring.main.id
  rotation_period = "2592000s"  # 30 days

  lifecycle {
    prevent_destroy = true
  }

  labels = {
    compliance = "enc-001"
  }
}

# Cloud Storage with CMEK
resource "google_storage_bucket" "data" {
  name     = "company-data-${var.environment}"
  location = var.region

  encryption {
    default_kms_key_name = google_kms_crypto_key.data.id
  }

  versioning {
    enabled = true
  }

  labels = {
    compliance = "enc-001"
  }
}

# Cloud SQL with encryption
resource "google_sql_database_instance" "main" {
  name             = "company-db-${var.environment}"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier = "db-f1-micro"

    database_flags {
      name  = "cloudsql.enable_pgaudit"
      value = "on"
    }

    backup_configuration {
      enabled    = true
      start_time = "03:00"
    }

    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.main.id
      require_ssl     = true
    }
  }

  encryption_key_name = google_kms_crypto_key.data.id
}
```

## Encryption in Transit

### TLS Configuration

#### Application Level (Python/Flask)

```python
# api/config/tls_config.py
import ssl
from typing import Dict

class TLSConfig:
    """TLS configuration for HIPAA, PCI-DSS compliance"""

    # TLS 1.3 for maximum security
    TLS_MIN_VERSION = ssl.TLSVersion.TLSv1_3

    # Strong cipher suites only
    TLS_CIPHERS = [
        "TLS_AES_256_GCM_SHA384",
        "TLS_CHACHA20_POLY1305_SHA256",
        "TLS_AES_128_GCM_SHA256",
    ]

    # HSTS settings
    HSTS_MAX_AGE = 31536000  # 1 year
    HSTS_INCLUDE_SUBDOMAINS = True
    HSTS_PRELOAD = True

    @staticmethod
    def get_ssl_context() -> ssl.SSLContext:
        """Create secure SSL context"""
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.minimum_version = TLSConfig.TLS_MIN_VERSION
        context.set_ciphers(":".join(TLSConfig.TLS_CIPHERS))
        return context

    @staticmethod
    def get_security_headers() -> Dict[str, str]:
        """Security headers for all responses"""
        return {
            "Strict-Transport-Security":
                f"max-age={TLSConfig.HSTS_MAX_AGE}; includeSubDomains; preload",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Content-Security-Policy": "default-src 'self'",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }

# app.py
from flask import Flask, Response
from config.tls_config import TLSConfig

app = Flask(__name__)

@app.after_request
def add_security_headers(response: Response) -> Response:
    """Add security headers to all responses"""
    for header, value in TLSConfig.get_security_headers().items():
        response.headers[header] = value
    return response

if __name__ == "__main__":
    ssl_context = TLSConfig.get_ssl_context()
    app.run(ssl_context=ssl_context, host="0.0.0.0", port=443)
```

#### Load Balancer Configuration

**AWS Application Load Balancer:**

```hcl
# terraform/alb_tls.tf
resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.main.arn
  port              = 443
  protocol          = "HTTPS"

  # TLS 1.3 policy (PCI-DSS 4.0 compliant)
  ssl_policy      = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn = aws_acm_certificate.main.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}

# Redirect HTTP to HTTPS (mandatory)
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "redirect"
    redirect {
      protocol    = "HTTPS"
      port        = "443"
      status_code = "HTTP_301"
    }
  }
}

# ACM certificate with auto-renewal
resource "aws_acm_certificate" "main" {
  domain_name       = var.domain_name
  validation_method = "DNS"

  subject_alternative_names = [
    "*.${var.domain_name}"
  ]

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Compliance = "ENC-002"
  }
}

# Automated DNS validation
resource "aws_acm_certificate_validation" "main" {
  certificate_arn         = aws_acm_certificate.main.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
}
```

#### NGINX Configuration

```nginx
# /etc/nginx/conf.d/tls.conf
# TLS 1.3 configuration for compliance

server {
    listen 443 ssl http2;
    server_name api.example.com;

    # TLS certificates
    ssl_certificate     /etc/nginx/certs/server.crt;
    ssl_certificate_key /etc/nginx/certs/server.key;

    # TLS 1.3 only (PCI-DSS 4.0)
    ssl_protocols TLSv1.3;

    # Strong cipher suites
    ssl_ciphers 'TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256';
    ssl_prefer_server_ciphers on;

    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/nginx/certs/chain.crt;

    # Session cache
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_session_tickets off;

    # HSTS header (SOC 2, HIPAA)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'" always;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name api.example.com;
    return 301 https://$host$request_uri;
}
```

### Database Connection Encryption

**PostgreSQL (HIPAA-compliant):**

```python
# api/database/connection.py
import psycopg2
from typing import Dict

class DatabaseConnection:
    """HIPAA-compliant PostgreSQL connection"""

    @staticmethod
    def get_connection_params() -> Dict:
        """Connection parameters with TLS enforcement"""
        return {
            "host": "db.example.com",
            "port": 5432,
            "database": "app_db",
            "user": "app_user",
            "password": "secure_password",
            # Enforce TLS 1.2+
            "sslmode": "verify-full",
            "sslrootcert": "/etc/ssl/certs/ca-bundle.crt",
            # Application name for audit logging
            "application_name": "api-server",
            # Connection timeout
            "connect_timeout": 10,
        }

    @staticmethod
    def create_connection():
        """Create encrypted database connection"""
        params = DatabaseConnection.get_connection_params()
        conn = psycopg2.connect(**params)

        # Verify connection is encrypted
        cursor = conn.cursor()
        cursor.execute("SELECT ssl_is_used();")
        ssl_enabled = cursor.fetchone()[0]

        if not ssl_enabled:
            raise SecurityError("Database connection is not encrypted")

        return conn
```

**MySQL/MariaDB:**

```python
# api/database/mysql_connection.py
import mysql.connector
from mysql.connector import Error

class MySQLConnection:
    """PCI-DSS compliant MySQL connection"""

    @staticmethod
    def create_connection():
        """Create encrypted MySQL connection"""
        try:
            conn = mysql.connector.connect(
                host="db.example.com",
                user="app_user",
                password="secure_password",
                database="app_db",
                # Enforce TLS
                ssl_ca="/etc/ssl/certs/ca-bundle.crt",
                ssl_verify_cert=True,
                ssl_verify_identity=True,
                # Connection settings
                connection_timeout=10,
                autocommit=False,
            )

            # Verify encryption
            cursor = conn.cursor()
            cursor.execute("SHOW STATUS LIKE 'Ssl_cipher';")
            result = cursor.fetchone()

            if not result or not result[1]:
                raise Error("MySQL connection is not encrypted")

            return conn

        except Error as e:
            raise ConnectionError(f"MySQL connection failed: {e}")
```

## Key Management

### Key Rotation

**Automated KMS Rotation (AWS):**

```python
# scripts/validate_key_rotation.py
import boto3
from datetime import datetime, timedelta

kms = boto3.client('kms')

def check_key_rotation():
    """Validate KMS key rotation is enabled (PCI-DSS Req 3.6)"""
    keys = kms.list_keys()
    violations = []

    for key in keys['Keys']:
        key_id = key['KeyId']
        metadata = kms.describe_key(KeyId=key_id)

        # Check if customer-managed key
        if metadata['KeyMetadata']['KeyManager'] == 'CUSTOMER':
            # Check rotation status
            try:
                rotation = kms.get_key_rotation_status(KeyId=key_id)
                if not rotation['KeyRotationEnabled']:
                    violations.append({
                        'KeyId': key_id,
                        'Alias': get_key_alias(key_id),
                        'Issue': 'Key rotation not enabled'
                    })
            except Exception as e:
                violations.append({
                    'KeyId': key_id,
                    'Issue': f'Cannot check rotation: {e}'
                })

    return violations

def get_key_alias(key_id):
    """Get key alias for reporting"""
    try:
        aliases = kms.list_aliases(KeyId=key_id)
        if aliases['Aliases']:
            return aliases['Aliases'][0]['AliasName']
    except:
        pass
    return "No alias"

if __name__ == "__main__":
    violations = check_key_rotation()
    if violations:
        print("❌ Key rotation violations found:")
        for v in violations:
            print(f"  - {v}")
        exit(1)
    else:
        print("✅ All keys have rotation enabled")
```

### Key Access Policies

```hcl
# terraform/kms_policy.tf
data "aws_iam_policy_document" "kms_key_policy" {
  # Allow account root full access
  statement {
    sid    = "Enable IAM User Permissions"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"]
    }
    actions   = ["kms:*"]
    resources = ["*"]
  }

  # Allow services to use key
  statement {
    sid    = "Allow services to use the key"
    effect = "Allow"
    principals {
      type = "Service"
      identifiers = [
        "s3.amazonaws.com",
        "rds.amazonaws.com",
        "dynamodb.amazonaws.com",
        "logs.amazonaws.com"
      ]
    }
    actions = [
      "kms:Decrypt",
      "kms:GenerateDataKey"
    ]
    resources = ["*"]
  }

  # Audit key usage
  statement {
    sid    = "Allow CloudTrail to describe key"
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }
    actions   = ["kms:DescribeKey"]
    resources = ["*"]
  }
}

resource "aws_kms_key" "data" {
  description             = "Data encryption key"
  deletion_window_in_days = 30
  enable_key_rotation     = true
  policy                  = data.aws_iam_policy_document.kms_key_policy.json

  tags = {
    Compliance = "ENC-003"
    Purpose    = "data-encryption"
  }
}
```

## Encryption Validation

### OPA Policy

```rego
# policies/compliance/encryption.rego
package compliance.encryption

# Deny unencrypted S3 buckets
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_s3_bucket"
  not has_bucket_encryption(resource.address)

  msg := sprintf(
    "CRITICAL: S3 bucket '%s' must have encryption enabled (SOC2:CC6.1, HIPAA:164.312(a)(2)(iv), PCI-DSS:Req3.4)",
    [resource.address]
  )
}

has_bucket_encryption(bucket_address) {
  encryption_resource := input.resource_changes[_]
  encryption_resource.type == "aws_s3_bucket_server_side_encryption_configuration"
  startswith(encryption_resource.address, bucket_address)
}

# Deny unencrypted RDS
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_db_instance"
  resource.change.after.storage_encrypted != true

  msg := sprintf(
    "CRITICAL: RDS instance '%s' must enable storage_encrypted",
    [resource.address]
  )
}

# Require KMS (not default encryption)
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_s3_bucket_server_side_encryption_configuration"
  rule := resource.change.after.rule[_]
  encryption := rule.apply_server_side_encryption_by_default
  encryption.sse_algorithm != "aws:kms"

  msg := sprintf(
    "HIGH: Bucket '%s' must use KMS encryption (not default AES256)",
    [resource.address]
  )
}

# Require key rotation
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_kms_key"
  resource.change.after.enable_key_rotation != true

  msg := sprintf(
    "MEDIUM: KMS key '%s' must have rotation enabled (PCI-DSS:Req3.6)",
    [resource.address]
  )
}
```

This comprehensive encryption implementation satisfies all major compliance framework requirements while following security best practices.
