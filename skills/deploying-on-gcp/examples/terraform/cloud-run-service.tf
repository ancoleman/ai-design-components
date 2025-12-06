# Cloud Run Service with Best Practices
# This configuration demonstrates a production-ready Cloud Run deployment
# with IAM, networking, and security configurations

terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

# Provider configuration
provider "google" {
  project = var.project_id
  region  = var.region
}

# Variables
variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region for Cloud Run service"
  type        = string
  default     = "us-central1"
}

variable "service_name" {
  description = "Name of the Cloud Run service"
  type        = string
  default     = "api-service"
}

variable "container_image" {
  description = "Container image URL (e.g., gcr.io/project/image:tag)"
  type        = string
}

variable "max_instances" {
  description = "Maximum number of container instances"
  type        = number
  default     = 10
}

variable "min_instances" {
  description = "Minimum number of container instances (0 for scale to zero)"
  type        = number
  default     = 0
}

variable "cpu" {
  description = "Number of CPUs per container (1, 2, 4, 8)"
  type        = string
  default     = "1"
}

variable "memory" {
  description = "Memory allocation per container (e.g., 512Mi, 1Gi, 2Gi)"
  type        = string
  default     = "512Mi"
}

variable "allow_public_access" {
  description = "Allow unauthenticated public access to the service"
  type        = bool
  default     = false
}

variable "environment_variables" {
  description = "Environment variables for the container"
  type        = map(string)
  default     = {}
}

# Service Account for Cloud Run
# Following principle of least privilege - create dedicated service account
resource "google_service_account" "cloud_run_sa" {
  account_id   = "${var.service_name}-sa"
  display_name = "Service Account for ${var.service_name} Cloud Run"
  description  = "Dedicated service account for Cloud Run service with minimal permissions"
}

# IAM binding to allow Cloud Run to use the service account
resource "google_service_account_iam_member" "cloud_run_sa_user" {
  service_account_id = google_service_account.cloud_run_sa.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[default/cloud-run]"
}

# Example IAM role for accessing Cloud SQL (if needed)
# Uncomment and adjust based on your requirements
# resource "google_project_iam_member" "cloud_sql_client" {
#   project = var.project_id
#   role    = "roles/cloudsql.client"
#   member  = "serviceAccount:${google_service_account.cloud_run_sa.email}"
# }

# Example IAM role for accessing Cloud Storage (if needed)
# resource "google_project_iam_member" "storage_object_viewer" {
#   project = var.project_id
#   role    = "roles/storage.objectViewer"
#   member  = "serviceAccount:${google_service_account.cloud_run_sa.email}"
# }

# Cloud Run Service
resource "google_cloud_run_v2_service" "main" {
  name     = var.service_name
  location = var.region

  # Use the dedicated service account
  ingress = "INGRESS_TRAFFIC_ALL"

  template {
    # Scaling configuration
    scaling {
      min_instance_count = var.min_instances
      max_instance_count = var.max_instances
    }

    # Service account for the running containers
    service_account = google_service_account.cloud_run_sa.email

    # VPC connector (optional - uncomment if using VPC resources)
    # vpc_access {
    #   connector = google_vpc_access_connector.connector.id
    #   egress    = "PRIVATE_RANGES_ONLY"
    # }

    # Container configuration
    containers {
      image = var.container_image

      # Resource limits - important for cost control
      resources {
        limits = {
          cpu    = var.cpu
          memory = var.memory
        }
        # CPU is always allocated (use true for always-on services)
        cpu_idle = true
        # Startup CPU boost for faster cold starts
        startup_cpu_boost = true
      }

      # Environment variables (non-sensitive configuration)
      dynamic "env" {
        for_each = var.environment_variables
        content {
          name  = env.key
          value = env.value
        }
      }

      # Example: Load secrets from Secret Manager (recommended for sensitive data)
      # env {
      #   name = "DATABASE_PASSWORD"
      #   value_source {
      #     secret_key_ref {
      #       secret  = google_secret_manager_secret.db_password.secret_id
      #       version = "latest"
      #     }
      #   }
      # }

      # Health check and startup probe
      startup_probe {
        http_get {
          path = "/health"
          port = 8080
        }
        initial_delay_seconds = 0
        timeout_seconds       = 1
        period_seconds        = 3
        failure_threshold     = 3
      }

      # Liveness probe - restart unhealthy containers
      liveness_probe {
        http_get {
          path = "/health"
          port = 8080
        }
        initial_delay_seconds = 10
        timeout_seconds       = 1
        period_seconds        = 10
        failure_threshold     = 3
      }

      # Container port
      ports {
        name           = "http1"
        container_port = 8080
      }
    }

    # Timeout for request processing (max 3600 seconds)
    timeout = "300s"

    # Execution environment (Second generation recommended for better performance)
    execution_environment = "EXECUTION_ENVIRONMENT_GEN2"

    # Session affinity (optional - for stateful applications)
    # session_affinity = true
  }

  # Traffic routing - 100% to latest revision
  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  # Lifecycle policy to prevent accidental deletion
  lifecycle {
    prevent_destroy = false # Set to true in production
  }

  # Labels for organization and cost tracking
  labels = {
    environment = "production"
    managed_by  = "terraform"
    service     = var.service_name
  }
}

# IAM Policy for public access (if enabled)
# This allows unauthenticated invocations - use carefully!
resource "google_cloud_run_service_iam_member" "public_access" {
  count = var.allow_public_access ? 1 : 0

  service  = google_cloud_run_v2_service.main.name
  location = google_cloud_run_v2_service.main.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Example: Grant specific user or service account access
# resource "google_cloud_run_service_iam_member" "authorized_invoker" {
#   service  = google_cloud_run_v2_service.main.name
#   location = google_cloud_run_v2_service.main.location
#   role     = "roles/run.invoker"
#   member   = "user:example@example.com"
# }

# Optional: VPC Connector for private networking
# Uncomment if Cloud Run needs to access resources in a VPC
# resource "google_vpc_access_connector" "connector" {
#   name          = "${var.service_name}-vpc-connector"
#   region        = var.region
#   ip_cidr_range = "10.8.0.0/28"
#   network       = "default"
#
#   # Throughput configuration
#   min_throughput = 200
#   max_throughput = 300
# }

# Optional: Cloud SQL Connection (if using Cloud SQL)
# Uncomment and configure based on your Cloud SQL instance
# resource "google_cloud_run_v2_service" "main_with_cloudsql" {
#   # ... (same configuration as above)
#
#   template {
#     containers {
#       # ... (container config)
#     }
#
#     # Cloud SQL instance connection
#     cloud_sql_instances = [
#       google_sql_database_instance.main.connection_name
#     ]
#   }
# }

# Outputs
output "service_url" {
  description = "URL of the deployed Cloud Run service"
  value       = google_cloud_run_v2_service.main.uri
}

output "service_name" {
  description = "Name of the Cloud Run service"
  value       = google_cloud_run_v2_service.main.name
}

output "service_account_email" {
  description = "Email of the service account used by Cloud Run"
  value       = google_service_account.cloud_run_sa.email
}

output "latest_revision" {
  description = "Latest deployed revision name"
  value       = google_cloud_run_v2_service.main.latest_ready_revision
}

# Example usage:
#
# 1. Initialize Terraform:
#    terraform init
#
# 2. Plan the deployment:
#    terraform plan -var="project_id=my-project" -var="container_image=gcr.io/my-project/api:v1"
#
# 3. Apply the configuration:
#    terraform apply -var="project_id=my-project" -var="container_image=gcr.io/my-project/api:v1"
#
# 4. For public access:
#    terraform apply -var="project_id=my-project" -var="container_image=gcr.io/my-project/api:v1" -var="allow_public_access=true"
#
# 5. Destroy resources:
#    terraform destroy -var="project_id=my-project" -var="container_image=gcr.io/my-project/api:v1"
