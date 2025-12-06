# GCP Firewall Rules Guide

Google Cloud Platform firewall rules operate at the VPC level and are stateful, similar to AWS Security Groups.


## Table of Contents

- [Key Concepts](#key-concepts)
- [Firewall Rule Components](#firewall-rule-components)
- [gcloud CLI Examples](#gcloud-cli-examples)
  - [List Firewall Rules](#list-firewall-rules)
  - [Create Firewall Rules](#create-firewall-rules)
  - [Delete/Update Rules](#deleteupdate-rules)
- [Terraform Examples](#terraform-examples)
  - [Basic Web Server](#basic-web-server)
  - [Database (Internal Only)](#database-internal-only)
  - [Using Service Accounts (Identity-Based)](#using-service-accounts-identity-based)
  - [Egress Rules (Restrict Outbound)](#egress-rules-restrict-outbound)
- [Priority System](#priority-system)
- [Network Tags](#network-tags)
- [Implied Rules](#implied-rules)
- [Best Practices](#best-practices)
- [VPC Firewall Logs](#vpc-firewall-logs)
- [Three-Tier Application Example](#three-tier-application-example)
- [Comparison with AWS](#comparison-with-aws)
- [Resources](#resources)

## Key Concepts

**VPC Firewall Characteristics:**
- **Stateful:** Return traffic automatically allowed
- **VPC-level:** Applied to VPC, not individual instances
- **Priority-based:** Lower priority number = higher priority (0-65535)
- **Default deny ingress, allow egress**
- **Implied rules:** Allow internal VPC traffic, deny external ingress

## Firewall Rule Components

```
Direction: Ingress or Egress
Priority: 0-65535 (lower = higher priority)
Action: Allow or Deny
Target: All instances, tags, or service accounts
Source/Destination: IP ranges, tags, service accounts
Protocol/Port: TCP, UDP, ICMP with port ranges
```

## gcloud CLI Examples

### List Firewall Rules

```bash
# List all rules
gcloud compute firewall-rules list

# Describe specific rule
gcloud compute firewall-rules describe allow-ssh
```

### Create Firewall Rules

```bash
# Allow SSH from anywhere
gcloud compute firewall-rules create allow-ssh \
    --network=default \
    --action=allow \
    --direction=ingress \
    --rules=tcp:22 \
    --source-ranges=0.0.0.0/0

# Allow HTTP/HTTPS
gcloud compute firewall-rules create allow-http-https \
    --network=default \
    --action=allow \
    --direction=ingress \
    --rules=tcp:80,tcp:443 \
    --source-ranges=0.0.0.0/0

# Allow from specific IP
gcloud compute firewall-rules create allow-office-ssh \
    --network=default \
    --action=allow \
    --direction=ingress \
    --rules=tcp:22 \
    --source-ranges=203.0.113.0/24

# Allow using network tags (target specific instances)
gcloud compute firewall-rules create allow-web-traffic \
    --network=default \
    --action=allow \
    --direction=ingress \
    --rules=tcp:80,tcp:443 \
    --target-tags=web-server \
    --source-ranges=0.0.0.0/0
```

### Delete/Update Rules

```bash
# Delete rule
gcloud compute firewall-rules delete allow-ssh

# Update rule (change priority)
gcloud compute firewall-rules update allow-ssh --priority=1000
```

## Terraform Examples

### Basic Web Server

```hcl
resource "google_compute_firewall" "allow_http_https" {
  name    = "allow-http-https"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
    ports    = ["80", "443"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["web-server"]
}

resource "google_compute_firewall" "allow_ssh" {
  name    = "allow-ssh"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["203.0.113.0/24"]  # Office IP
  target_tags   = ["ssh-accessible"]
}
```

### Database (Internal Only)

```hcl
resource "google_compute_firewall" "allow_postgresql_internal" {
  name    = "allow-postgresql-internal"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
    ports    = ["5432"]
  }

  source_tags = ["app-server"]  # Only from app servers
  target_tags = ["database"]
}

# Deny external access to database
resource "google_compute_firewall" "deny_database_external" {
  name     = "deny-database-external"
  network  = google_compute_network.main.name
  priority = 900  # Higher priority than default allow

  deny {
    protocol = "all"
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["database"]
}
```

### Using Service Accounts (Identity-Based)

```hcl
resource "google_compute_firewall" "allow_app_to_database" {
  name    = "allow-app-to-database"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
    ports    = ["5432"]
  }

  source_service_accounts = [google_service_account.app.email]
  target_service_accounts = [google_service_account.database.email]
}
```

### Egress Rules (Restrict Outbound)

```hcl
# Deny all egress (must come after default allow)
resource "google_compute_firewall" "deny_all_egress" {
  name      = "deny-all-egress"
  network   = google_compute_network.main.name
  direction = "EGRESS"
  priority  = 65534  # Low priority

  deny {
    protocol = "all"
  }

  destination_ranges = ["0.0.0.0/0"]
  target_tags        = ["restricted-egress"]
}

# Allow specific egress
resource "google_compute_firewall" "allow_egress_https" {
  name      = "allow-egress-https"
  network   = google_compute_network.main.name
  direction = "EGRESS"
  priority  = 1000  # Higher than deny-all

  allow {
    protocol = "tcp"
    ports    = ["443"]
  }

  destination_ranges = ["0.0.0.0/0"]
  target_tags        = ["restricted-egress"]
}
```

## Priority System

Rules are evaluated by priority (0-65535):
- **0-999:** High priority (deny rules, specific allows)
- **1000:** Default priority
- **65535:** Lowest priority (catch-all rules)

**Evaluation:**
- Lower priority number processed first
- First match wins (allow or deny)
- If no match, default deny (ingress) or allow (egress)

## Network Tags

Tags target specific instances:

```bash
# Assign tag to instance
gcloud compute instances add-tags web-server-1 \
    --tags=web-server,ssh-accessible

# Create firewall rule using tags
gcloud compute firewall-rules create allow-web-traffic \
    --target-tags=web-server \
    --allow=tcp:80,tcp:443
```

## Implied Rules

GCP creates two implied rules (cannot be deleted):

1. **Deny all ingress** (priority 65535)
2. **Allow all egress** (priority 65535)

Plus default rules in default network:
- Allow internal traffic (10.128.0.0/9)
- Allow SSH (tcp:22) from anywhere
- Allow RDP (tcp:3389) from anywhere
- Allow ICMP from anywhere

## Best Practices

1. **Use Network Tags:** Target specific instance groups
2. **Least Privilege:** Only open necessary ports
3. **Source Restrictions:** Use specific source ranges, not 0.0.0.0/0
4. **Service Accounts:** Use identity-based rules when possible
5. **Priority Management:** Reserve 0-999 for security rules
6. **Documentation:** Use descriptive names and descriptions
7. **Infrastructure as Code:** Manage with Terraform
8. **Regular Audits:** Review rules quarterly
9. **VPC Firewall Logs:** Enable for monitoring
10. **Delete Default Rules:** In production, remove permissive defaults

## VPC Firewall Logs

```hcl
resource "google_compute_firewall" "logged_rule" {
  name    = "allow-ssh-logged"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]

  log_config {
    metadata = "INCLUDE_ALL_METADATA"
  }
}
```

View logs:
```bash
# Cloud Logging
gcloud logging read "resource.type=gce_subnetwork AND logName:compute.googleapis.com/firewall"
```

## Three-Tier Application Example

```hcl
# VPC
resource "google_compute_network" "main" {
  name                    = "main-vpc"
  auto_create_subnetworks = false
}

# Subnets
resource "google_compute_subnetwork" "web" {
  name          = "web-subnet"
  network       = google_compute_network.main.id
  ip_cidr_range = "10.0.1.0/24"
  region        = "us-central1"
}

resource "google_compute_subnetwork" "app" {
  name          = "app-subnet"
  network       = google_compute_network.main.id
  ip_cidr_range = "10.0.2.0/24"
  region        = "us-central1"
}

resource "google_compute_subnetwork" "data" {
  name          = "data-subnet"
  network       = google_compute_network.main.id
  ip_cidr_range = "10.0.3.0/24"
  region        = "us-central1"
}

# Firewall: Internet → Web
resource "google_compute_firewall" "internet_to_web" {
  name    = "internet-to-web"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
    ports    = ["80", "443"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["web-tier"]
}

# Firewall: Web → App
resource "google_compute_firewall" "web_to_app" {
  name    = "web-to-app"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
    ports    = ["8080"]
  }

  source_tags = ["web-tier"]
  target_tags = ["app-tier"]
}

# Firewall: App → Database
resource "google_compute_firewall" "app_to_database" {
  name    = "app-to-database"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
    ports    = ["5432"]
  }

  source_tags = ["app-tier"]
  target_tags = ["database-tier"]
}

# Firewall: Bastion SSH
resource "google_compute_firewall" "bastion_ssh" {
  name    = "bastion-ssh"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["203.0.113.0/24"]  # Office IP
  target_tags   = ["bastion"]
}

# Firewall: Internal SSH from Bastion
resource "google_compute_firewall" "internal_ssh" {
  name    = "internal-ssh"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_tags = ["bastion"]
  target_tags = ["web-tier", "app-tier", "database-tier"]
}
```

## Comparison with AWS

| Feature | GCP Firewall Rules | AWS Security Groups |
|---------|-------------------|---------------------|
| **Level** | VPC | Instance (ENI) |
| **State** | Stateful | Stateful |
| **Priority** | Yes (0-65535) | No (all evaluated) |
| **Deny Rules** | Yes | No (allow only) |
| **Direction** | Ingress + Egress | Inbound + Outbound |
| **Targeting** | Tags, Service Accounts | Security Group ID |
| **Default** | Deny ingress, allow egress | Deny ingress, allow egress |

## Resources

- GCP Firewall Documentation: https://cloud.google.com/vpc/docs/firewalls
- Terraform google_compute_firewall: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_firewall
