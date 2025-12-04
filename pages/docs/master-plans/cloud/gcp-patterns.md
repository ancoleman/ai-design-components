---
sidebar_position: 2
title: GCP Patterns
description: Google Cloud Platform architectural patterns with BigQuery analytics, Cloud Run serverless, and GKE Kubernetes
tags: [master-plan, cloud, gcp, google-cloud]
---

# GCP Patterns

:::info Status
**Master Plan** - Comprehensive init.md complete, ready for SKILL.md implementation
:::

Google Cloud Platform architectural patterns covering data analytics, machine learning, Kubernetes, and serverless computing.

## Scope

This skill provides GCP-specific service selection and patterns:

- **Compute**: Cloud Run vs. GKE vs. Cloud Functions vs. Compute Engine
- **Data & Analytics**: BigQuery, Pub/Sub, Dataflow, Dataproc
- **AI/ML**: Vertex AI, AutoML, pre-trained APIs, TPUs
- **Storage**: Cloud Storage tiers, Persistent Disk, Filestore
- **Databases**: Cloud SQL, Cloud Spanner, Firestore, Bigtable
- **Networking**: VPC design, Cloud Load Balancing, Cloud CDN, Cloud Armor

## Key Components

- **Cloud Run First** - Default choice for stateless HTTP services (serverless, auto-scale to zero)
- **BigQuery for Analytics** - Best-in-class petabyte-scale data warehouse
- **GKE for Kubernetes** - Most mature managed Kubernetes (invented by Kubernetes creators)
- **Vertex AI Platform** - Unified ML lifecycle (training, deployment, monitoring)
- **Multi-Region Architecture** - 99.95% SLA with multi-region deployment
- **Workload Identity** - Modern authentication for GKE (no service account keys)

## Decision Framework

**Compute Service Selection:**
```
HTTP service + stateless → Cloud Run
Need Kubernetes control → GKE
Simple event-driven → Cloud Functions
Full VM control → Compute Engine
```

**Database Selection:**
```
Global distribution → Cloud Spanner
Relational (regional) → Cloud SQL
Document + real-time → Firestore
Key-value + scale → Bigtable
```

## Tool Recommendations

- **Terraform** (hashicorp/google provider) - Multi-cloud IaC
- **gcloud CLI** - Official Google Cloud command-line tool
- **google-cloud-*** (Python SDK) - Comprehensive API coverage
- **Cloud Code** (VS Code/IntelliJ) - IDE integration for GCP

## Integration Points

- `infrastructure-as-code` - GCP resources via Terraform
- `kubernetes-operations` - GKE management and Workload Identity
- `data-architecture` - BigQuery as data warehouse
- `building-ci-pipelines` - Cloud Build for CI/CD
- `secret-management` - Secret Manager integration
- `observability` - Cloud Monitoring/Logging (formerly Stackdriver)
- `ai-data-engineering` - Vertex AI + BigQuery ML pipelines

## Learn More

- [Full Master Plan](https://github.com/ancoleman/ai-design-components/blob/main/skills/gcp-patterns/init.md)
- [GCP Architecture Center](https://cloud.google.com/architecture)
- [GCP Best Practices](https://cloud.google.com/docs/enterprise/best-practices-for-enterprise-organizations)
