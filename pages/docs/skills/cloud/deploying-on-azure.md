---
sidebar_position: 3
title: Deploying on Azure
description: Design and implement Azure cloud architectures using best practices
tags: [cloud, azure, container-apps, aks, app-service, azure-openai, cosmos-db]
---

# Deploying on Azure

Design and implement Azure cloud architectures following Microsoft's Well-Architected Framework and best practices for service selection, cost optimization, and security.

## When to Use

Use this skill when:

- Designing new applications for Azure cloud
- Selecting Azure compute services (Container Apps, AKS, Functions, App Service)
- Architecting storage solutions (Blob Storage, Files, Cosmos DB)
- Integrating Azure OpenAI or Cognitive Services
- Implementing messaging patterns (Service Bus, Event Grid, Event Hubs)
- Designing secure networks with Private Endpoints
- Applying Azure governance and compliance policies
- Optimizing Azure costs and performance

## Key Features

### 1. Compute Service Selection

**Decision Framework:**

```
Container-based workload?
  YES → Need Kubernetes control plane?
          YES → Azure Kubernetes Service (AKS)
          NO → Azure Container Apps (recommended)
  NO → Event-driven function?
         YES → Azure Functions
         NO → Web application?
                YES → Azure App Service
                NO → Legacy/specialized → Virtual Machines
```

**Service Comparison:**

| Service | Best For | Pricing Model | Operational Overhead |
|---------|----------|---------------|---------------------|
| **Container Apps** | Microservices, APIs, background jobs | Consumption or dedicated | Low |
| **AKS** | Complex K8s workloads, service mesh | Node-based | High |
| **Functions** | Event-driven, short tasks (&lt;10 min) | Consumption or premium | Low |
| **App Service** | Web apps, simple APIs | Dedicated plans | Low |
| **Virtual Machines** | Legacy apps, specialized software | VM-based | High |

**Recommendation:** Start with Azure Container Apps for 80% of containerized workloads (simpler and cheaper than AKS).

### 2. Database Service Selection

**Decision Matrix:**

```
Relational data?
  YES → SQL Server compatible?
          YES → Need VM-level access?
                  YES → SQL Managed Instance
                  NO → Azure SQL Database
          NO → Open source?
                 PostgreSQL → PostgreSQL Flexible Server
                 MySQL → MySQL Flexible Server
  NO → Data model?
         Document/JSON → Cosmos DB (NoSQL API)
         Graph → Cosmos DB (Gremlin API)
         Wide-column → Cosmos DB (Cassandra API)
         Key-value cache → Azure Cache for Redis
         Time-series → Azure Data Explorer
```

### 3. Storage Architecture

**Blob Storage Tier Selection:**

| Tier | Access Pattern | Cost/GB/Month | Minimum Storage Duration |
|------|---------------|---------------|--------------------------|
| **Hot** | Daily access | $0.018 | None |
| **Cool** | &lt;1/month access | $0.010 | 30 days |
| **Cold** | &lt;90 days access | $0.0045 | 90 days |
| **Archive** | Rare access | $0.00099 | 180 days |

**Pattern:** Use lifecycle management policies to automatically move data to lower-cost tiers.

**Storage Service Decision:**

```
File system interface required?
  YES → Protocol?
          SMB → Azure Files (or NetApp Files for high performance)
          NFS → Azure Files (NFS 4.1)
  NO → Object storage → Blob Storage
       Block storage → Managed Disks (Standard/Premium SSD/Ultra)
       Analytics → Data Lake Storage Gen2
```

### 4. Azure OpenAI Service

**Use Cases:**
- Chatbots and conversational AI (GPT-4)
- Content generation and summarization
- Semantic search with embeddings (RAG pattern)
- Code generation and completion
- Function calling for structured outputs

**Key Advantages:**
- Enterprise data privacy (no model training on customer data)
- Regional deployment for data residency
- Microsoft enterprise SLAs
- Built-in content filtering

**Integration Pattern:**
```python
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = AzureOpenAI(
    azure_endpoint="https://myopenai.openai.azure.com",
    azure_ad_token_provider=token_provider,
    api_version="2024-02-15-preview"
)

response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### 5. Messaging and Integration

**Service Selection Matrix:**

| Service | Pattern | Message Size | Ordering | Transactions | Best For |
|---------|---------|--------------|----------|--------------|----------|
| **Service Bus** | Queue/Topic | 256 KB - 100 MB | Yes (sessions) | Yes | Enterprise messaging |
| **Event Grid** | Pub/Sub | 1 MB | No | No | Event-driven architectures |
| **Event Hubs** | Streaming | 1 MB | Yes (partitions) | No | Big data ingestion, telemetry |
| **Storage Queues** | Simple queue | 64 KB | No | No | Async work, &lt;500k msgs/sec |

**When to Use What:**
- **Service Bus**: Reliable messaging with transactions (e.g., order processing)
- **Event Grid**: React to Azure resource events (e.g., blob created, VM stopped)
- **Event Hubs**: High-throughput streaming (e.g., IoT telemetry, application logs)

## Architecture Patterns

### Pattern 1: Serverless Web Application

**Architecture:**
```
CloudFront (CDN)
  → S3 (React frontend)
  → API Gateway (REST API)
    → Lambda (business logic)
      → DynamoDB (data)
      → S3 (file storage)
```

### Pattern 2: Containerized Microservices

**Architecture:**
```
Route 53 (DNS)
  → CloudFront (CDN)
    → ALB (load balancer)
      → ECS Fargate (services)
        → RDS Aurora (database)
        → ElastiCache Redis (cache)
```

### Pattern 3: Event-Driven Data Pipeline

**Architecture:**
```
S3 Upload
  → EventBridge Rule
    → Lambda (transform)
      → Kinesis Firehose
        → S3 Data Lake
          → Athena (query)
```

## Best Practices

### Azure Well-Architected Framework (Five Pillars)

| Pillar | Focus | Key Practices |
|--------|-------|---------------|
| **Cost Optimization** | Maximize value within budget | Reserved Instances, auto-scaling, lifecycle management |
| **Operational Excellence** | Run reliable systems | Azure Policy, automation, monitoring |
| **Performance Efficiency** | Scale to meet demand | Autoscaling, caching, CDN |
| **Reliability** | Recover from failures | Availability Zones, multi-region, backup |
| **Security** | Protect data and assets | Managed Identity, Private Endpoints, Key Vault |

### Networking Architecture

**Private Endpoints vs. Service Endpoints:**

| Aspect | Private Endpoint | Service Endpoint |
|--------|------------------|------------------|
| **Security Model** | Private IP in VNet | Optimized route to public endpoint |
| **Data Exfiltration Protection** | Yes (network-isolated) | Limited (service firewall only) |
| **Cost** | ~$7.30/month per endpoint | Free |
| **Recommendation** | Production workloads | Dev/test environments |

**Hub-and-Spoke Topology:**
- **Hub VNet**: Shared services (Azure Firewall, VPN Gateway, Private Endpoints)
- **Spoke VNets**: Application workloads (isolated per environment or team)
- **VNet Peering**: Low-latency connectivity between hub and spokes

### Identity and Access Management

**Managed Identity Pattern:**

**Always use Managed Identity instead of:**
- Connection strings in code
- Storage account keys
- Service principal credentials
- API keys

**System-Assigned vs. User-Assigned:**

| Type | Lifecycle | Use Case |
|------|-----------|----------|
| **System-Assigned** | Tied to resource | Single resource needs access |
| **User-Assigned** | Independent | Multiple resources share identity |

**Example:**
```python
from azure.identity import DefaultAzureCredential

# Works automatically with Managed Identity
credential = DefaultAzureCredential()
keyvault_client = SecretClient(vault_url="...", credential=credential)
```

### Governance and Compliance

**Azure Policy for Guardrails:**
- Require tags on all resources (Environment, Owner, CostCenter)
- Restrict allowed Azure regions
- Enforce TLS 1.2 minimum
- Require Private Endpoints for storage accounts
- Deny public IP addresses on VMs

**Policy Effects:**
- **Deny**: Block non-compliant resource creation
- **Audit**: Log non-compliance but allow creation
- **DeployIfNotExists**: Auto-remediate missing configurations
- **Modify**: Change resource properties during deployment

## Infrastructure as Code

### Tool Selection

| Tool | Best For | Azure Integration | Multi-Cloud |
|------|----------|-------------------|-------------|
| **Bicep** | Azure-native projects | Excellent (official) | No |
| **Terraform** | Multi-cloud environments | Good (azurerm provider) | Yes |
| **Pulumi** | Developer-first approach | Good (native SDK) | Yes |
| **Azure CLI** | Scripts and automation | Excellent | No |

**Recommendation:**
- Use **Bicep** for Azure-only infrastructure (best Azure integration, native type safety)
- Use **Terraform** for multi-cloud or existing Terraform shops
- Use **Azure CLI** for quick scripts and CI/CD automation

### Bicep Example

```bicep
resource containerApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: 'my-app'
  location: location
  properties: {
    configuration: {
      ingress: {
        external: true
        targetPort: 80
      }
    }
    template: {
      containers: [
        {
          name: 'api'
          image: 'myregistry.azurecr.io/api:latest'
        }
      ]
    }
  }
}
```

## Cost Optimization

**Optimization Strategies:**

| Pattern | Savings | Use Case |
|---------|---------|----------|
| **Reserved Instances (1-year)** | 40-50% | Steady-state workloads (databases, VMs) |
| **Reserved Instances (3-year)** | 60-70% | Long-term commitments |
| **Spot VMs** | Up to 90% | Fault-tolerant batch processing |
| **Auto-shutdown** | Variable | Dev/test resources (off-hours) |
| **Storage lifecycle policies** | 50-90% | Move to Cool/Archive tiers |

**Monitoring:**
- Set budgets and alerts in Azure Cost Management
- Review Azure Advisor cost recommendations weekly
- Tag resources for cost allocation
- Use FinOps Toolkit for Power BI dashboards

## Security Best Practices

**Essential Security Controls:**

| Control | Implementation | Priority |
|---------|---------------|----------|
| **Managed Identity** | Enable on all compute resources | Critical |
| **Private Endpoints** | All PaaS services in production | Critical |
| **Key Vault** | Store secrets, keys, certificates | Critical |
| **Network Segmentation** | NSGs, application security groups | High |
| **Microsoft Defender** | Enable for all resource types | High |
| **Azure Policy** | Preventive controls | High |
| **Just-In-Time Access** | VMs and privileged access | Medium |

**Defense-in-Depth Layers:**
1. **Network**: Private Endpoints, NSGs, Azure Firewall
2. **Identity**: Entra ID, Managed Identity, Conditional Access
3. **Application**: Web Application Firewall, API Management
4. **Data**: Encryption at rest, encryption in transit (TLS 1.2+)
5. **Monitoring**: Microsoft Defender, Azure Monitor, Sentinel

## Quick Reference

### Cosmos DB Consistency Levels

| Level | Use Case | Latency | Throughput |
|-------|----------|---------|------------|
| **Strong** | Financial transactions, inventory | Highest | Lowest |
| **Bounded Staleness** | Real-time leaderboards with acceptable lag | High | Low |
| **Session** | Shopping carts, user sessions (default) | Medium | Medium |
| **Consistent Prefix** | Social feeds, IoT telemetry | Low | High |
| **Eventual** | Analytics, ML training data | Lowest | Highest |

### Cost Estimation

**Compute:**
- Container Apps: ~$60/month (1 vCPU, 2GB RAM, 24/7)
- AKS: ~$400/month (3-node D4s_v5 cluster)
- App Service P1v3: ~$145/month (2 vCPU, 8GB RAM)
- Functions Consumption: ~$0.20 per 1M executions

**Storage:**
- Blob Hot: $0.018/GB/month
- Blob Cool: $0.010/GB/month
- Blob Archive: $0.00099/GB/month
- Managed Disks Premium SSD: $0.15/GB/month

**Database:**
- Azure SQL Database (2 vCores): ~$280/month
- Cosmos DB Serverless: Pay per RU consumed
- PostgreSQL Flexible (2 vCores): ~$125/month

## Related Skills

- **writing-infrastructure-code**: Implement Azure patterns using Bicep or Terraform
- **operating-kubernetes**: AKS-specific configuration and operations
- **deploying-applications**: Container Apps and App Service deployment
- **building-ci-pipelines**: Azure DevOps and GitHub Actions integration
- **architecting-security**: Entra ID authentication and authorization patterns
- **implementing-observability**: Azure Monitor and Application Insights
- **building-ai-chat**: Azure OpenAI Service for chat applications
- **using-nosql-databases**: Cosmos DB implementation details
- **managing-secrets**: Azure Key Vault integration patterns

## References

- Full skill documentation: `/skills/deploying-on-azure/SKILL.md`
- Compute services: `/skills/deploying-on-azure/references/compute-services.md`
- Storage patterns: `/skills/deploying-on-azure/references/storage-patterns.md`
- Database selection: `/skills/deploying-on-azure/references/database-selection.md`
- AI integration: `/skills/deploying-on-azure/references/ai-integration.md`
- Messaging patterns: `/skills/deploying-on-azure/references/messaging-patterns.md`
- Networking architecture: `/skills/deploying-on-azure/references/networking-architecture.md`
- Identity & access: `/skills/deploying-on-azure/references/identity-access.md`
- Governance & compliance: `/skills/deploying-on-azure/references/governance-compliance.md`
- Well-Architected: `/skills/deploying-on-azure/references/well-architected.md`
