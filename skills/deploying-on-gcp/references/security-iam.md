# GCP Security and IAM Reference

IAM patterns, Workload Identity, Secret Manager, and security best practices.


## Table of Contents

- [IAM Best Practices](#iam-best-practices)
  - [Service Accounts](#service-accounts)
  - [Workload Identity for GKE](#workload-identity-for-gke)
- [Secret Manager](#secret-manager)
  - [Access Secrets in Python](#access-secrets-in-python)
  - [Access Secrets from Cloud Run](#access-secrets-from-cloud-run)
- [VPC Service Controls](#vpc-service-controls)
- [Binary Authorization](#binary-authorization)
- [Organization Policies](#organization-policies)
- [Security Best Practices](#security-best-practices)
  - [Encryption](#encryption)
  - [Audit Logging](#audit-logging)
- [Identity-Aware Proxy (IAP)](#identity-aware-proxy-iap)

## IAM Best Practices

### Service Accounts

```hcl
# Application service account
resource "google_service_account" "app" {
  account_id   = "app-service-account"
  display_name = "Application Service Account"
  description  = "Service account for application workloads"
}

# Grant minimal permissions
resource "google_project_iam_member" "app_storage_reader" {
  project = var.project_id
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.app.email}"
}

# Custom IAM role
resource "google_project_iam_custom_role" "app_role" {
  role_id     = "appRole"
  title       = "Application Role"
  description = "Custom role for application"
  permissions = [
    "storage.objects.get",
    "storage.objects.list",
    "bigquery.tables.get",
    "bigquery.tables.getData",
  ]
}
```

### Workload Identity for GKE

```bash
# Enable on cluster
gcloud container clusters update CLUSTER_NAME \
    --workload-pool=PROJECT_ID.svc.id.goog

# Create Kubernetes service account
kubectl create serviceaccount KSA_NAME -n NAMESPACE

# Create GCP service account
gcloud iam service-accounts create GSA_NAME \
    --display-name="GKE Workload Identity SA"

# Grant IAM permissions to GSA
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:GSA_NAME@PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.objectViewer"

# Bind KSA to GSA
gcloud iam service-accounts add-iam-policy-binding \
    GSA_NAME@PROJECT_ID.iam.gserviceaccount.com \
    --role=roles/iam.workloadIdentityUser \
    --member="serviceAccount:PROJECT_ID.svc.id.goog[NAMESPACE/KSA_NAME]"

# Annotate Kubernetes SA
kubectl annotate serviceaccount KSA_NAME \
    -n NAMESPACE \
    iam.gke.io/gcp-service-account=GSA_NAME@PROJECT_ID.iam.gserviceaccount.com
```

Terraform version:

```hcl
resource "google_service_account_iam_member" "workload_identity" {
  service_account_id = google_service_account.gke_app.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[${var.k8s_namespace}/${var.k8s_sa_name}]"
}
```

## Secret Manager

```hcl
# Secret
resource "google_secret_manager_secret" "db_password" {
  secret_id = "db-password"

  replication {
    auto {}
  }

  labels = {
    environment = "production"
  }
}

# Secret version
resource "google_secret_manager_secret_version" "db_password" {
  secret      = google_secret_manager_secret.db_password.id
  secret_data = random_password.db.result
}

# Grant access
resource "google_secret_manager_secret_iam_member" "app_accessor" {
  secret_id = google_secret_manager_secret.db_password.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.app.email}"
}
```

### Access Secrets in Python

```python
from google.cloud import secretmanager

def access_secret(project_id, secret_id, version_id="latest"):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# Usage
db_password = access_secret("my-project", "db-password")
```

### Access Secrets from Cloud Run

```hcl
resource "google_cloud_run_service" "app" {
  name     = "app"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "gcr.io/project/app:latest"

        env {
          name = "DB_PASSWORD"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.db_password.secret_id
              key  = "latest"
            }
          }
        }
      }

      service_account_name = google_service_account.app.email
    }
  }
}
```

## VPC Service Controls

```hcl
# Access context manager policy
resource "google_access_context_manager_access_policy" "policy" {
  parent = "organizations/${var.org_id}"
  title  = "Security Perimeter Policy"
}

# Access level
resource "google_access_context_manager_access_level" "access_level" {
  parent = "accessPolicies/${google_access_context_manager_access_policy.policy.name}"
  name   = "accessPolicies/${google_access_context_manager_access_policy.policy.name}/accessLevels/corporate_network"
  title  = "Corporate Network"

  basic {
    conditions {
      ip_subnetworks = ["203.0.113.0/24"]
    }
  }
}

# Service perimeter
resource "google_access_context_manager_service_perimeter" "perimeter" {
  parent = "accessPolicies/${google_access_context_manager_access_policy.policy.name}"
  name   = "accessPolicies/${google_access_context_manager_access_policy.policy.name}/servicePerimeters/secure_perimeter"
  title  = "Secure Perimeter"

  status {
    restricted_services = [
      "storage.googleapis.com",
      "bigquery.googleapis.com"
    ]

    access_levels = [
      google_access_context_manager_access_level.access_level.name
    ]

    resources = [
      "projects/${var.project_number}"
    ]

    vpc_accessible_services {
      enable_restriction = true
      allowed_services = [
        "storage.googleapis.com",
        "bigquery.googleapis.com"
      ]
    }
  }
}
```

## Binary Authorization

```hcl
resource "google_binary_authorization_policy" "policy" {
  admission_whitelist_patterns {
    name_pattern = "gcr.io/google_containers/*"
  }

  default_admission_rule {
    evaluation_mode  = "REQUIRE_ATTESTATION"
    enforcement_mode = "ENFORCED_BLOCK_AND_AUDIT_LOG"

    require_attestations_by = [
      google_binary_authorization_attestor.attestor.name
    ]
  }

  cluster_admission_rules {
    cluster                 = "us-central1.gke-cluster"
    evaluation_mode         = "REQUIRE_ATTESTATION"
    enforcement_mode        = "ENFORCED_BLOCK_AND_AUDIT_LOG"
    require_attestations_by = [google_binary_authorization_attestor.attestor.name]
  }
}
```

## Organization Policies

```hcl
# Restrict VM external IPs
resource "google_project_organization_policy" "restrict_vm_external_ips" {
  project    = var.project_id
  constraint = "compute.vmExternalIpAccess"

  list_policy {
    deny {
      all = true
    }
  }
}

# Require OS Login
resource "google_project_organization_policy" "require_os_login" {
  project    = var.project_id
  constraint = "compute.requireOsLogin"

  boolean_policy {
    enforced = true
  }
}

# Restrict public access to Cloud Storage
resource "google_project_organization_policy" "restrict_public_buckets" {
  project    = var.project_id
  constraint = "storage.publicAccessPrevention"

  boolean_policy {
    enforced = true
  }
}
```

## Security Best Practices

### Encryption

```hcl
# Customer-managed encryption keys
resource "google_kms_key_ring" "keyring" {
  name     = "production-keyring"
  location = "us-central1"
}

resource "google_kms_crypto_key" "key" {
  name     = "encryption-key"
  key_ring = google_kms_key_ring.keyring.id

  rotation_period = "7776000s"  # 90 days

  lifecycle {
    prevent_destroy = true
  }
}

# Use CMEK with Cloud Storage
resource "google_storage_bucket" "encrypted" {
  name     = "encrypted-bucket"
  location = "US"

  encryption {
    default_kms_key_name = google_kms_crypto_key.key.id
  }

  depends_on = [google_kms_crypto_key_iam_member.storage]
}

# Grant Storage service account access to KMS key
data "google_storage_project_service_account" "gcs_account" {
}

resource "google_kms_crypto_key_iam_member" "storage" {
  crypto_key_id = google_kms_crypto_key.key.id
  role          = "roles/cloudkms.cryptoKeyEncrypterDecrypter"
  member        = "serviceAccount:${data.google_storage_project_service_account.gcs_account.email_address}"
}
```

### Audit Logging

```hcl
resource "google_project_iam_audit_config" "project" {
  project = var.project_id
  service = "allServices"

  audit_log_config {
    log_type = "ADMIN_READ"
  }

  audit_log_config {
    log_type = "DATA_READ"
  }

  audit_log_config {
    log_type = "DATA_WRITE"
  }
}
```

## Identity-Aware Proxy (IAP)

```hcl
resource "google_iap_brand" "brand" {
  support_email     = "support@example.com"
  application_title = "Application"
  project           = var.project_id
}

resource "google_iap_client" "default" {
  display_name = "IAP Client"
  brand        = google_iap_brand.brand.name
}

# Grant IAP access
resource "google_iap_web_backend_service_iam_member" "member" {
  web_backend_service = google_compute_backend_service.default.name
  role                = "roles/iap.httpsResourceAccessor"
  member              = "user:user@example.com"
}
```
