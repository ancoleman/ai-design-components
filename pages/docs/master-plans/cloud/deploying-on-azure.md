---
sidebar_position: 3
title: Azure Patterns
description: Microsoft Azure architectural patterns with Container Apps, Azure OpenAI, and enterprise integration
tags: [master-plan, cloud, azure, microsoft]
---

# Azure Patterns

:::info Status
**Master Plan** - Comprehensive init.md complete, ready for SKILL.md implementation
:::

Microsoft Azure architectural patterns with emphasis on enterprise integration, hybrid cloud, and AI services leadership.

## Scope

This skill provides Azure-specific service selection and patterns:

- **Compute**: Container Apps vs. AKS vs. Functions vs. App Service
- **AI Services**: Azure OpenAI Service (GPT-4, embeddings), Cognitive Services
- **Storage**: Blob Storage tiers, Azure Files, Managed Disks, Data Lake Gen2
- **Databases**: Azure SQL vs. Cosmos DB vs. PostgreSQL Flexible Server
- **Integration**: Service Bus, Event Grid, Event Hubs, Logic Apps
- **Networking**: Private Endpoints, hub-spoke topology, Application Gateway, Front Door

## Key Components

- **Container Apps First** - Serverless container platform (no node management like AKS)
- **Azure OpenAI Service** - Enterprise-grade GPT-4 access with data privacy
- **Private Endpoints Everywhere** - Security best practice for all PaaS services
- **Managed Identities Always** - No hardcoded credentials when Managed Identity available
- **Well-Architected Framework** - Five pillars (cost, operations, performance, reliability, security)
- **Azure Verified Modules** - Microsoft-blessed Bicep and Terraform modules

## Decision Framework

**Compute Service Selection:**
```
Containers + no K8s → Container Apps
Need Kubernetes → AKS
Event-driven functions → Azure Functions
Traditional web app → App Service
```

**Database Selection:**
```
SQL Server compatible → Azure SQL Database
Global distribution → Cosmos DB
PostgreSQL/MySQL → Flexible Server
```

## Tool Recommendations

- **Bicep** (Azure-native DSL) - Recommended by Microsoft for Azure IaC
- **Terraform** (azurerm provider) - Multi-cloud IaC
- **Azure CLI** (az command) - Cross-platform management
- **azure-*** (Python SDK) - Official Azure libraries

## Integration Points

- `writing-infrastructure-code` - Azure patterns implemented via Bicep/Terraform
- `operating-kubernetes` - AKS-specific patterns and configuration
- `deploying-applications` - Container Apps, App Service deployment
- `building-ci-pipelines` - Azure DevOps, GitHub Actions integration
- `securing-authentication` - Entra ID (Azure AD), Managed Identity, Key Vault
- `implementing-observability` - Azure Monitor, Application Insights
- `ai-chat` - Azure OpenAI Service integration (RAG patterns)

## Learn More

- [Full Master Plan](https://github.com/ancoleman/ai-design-components/blob/main/skills/deploying-on-azure/init.md)
- [Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/)
- [Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/)
- [Azure Verified Modules](https://aka.ms/avm)
