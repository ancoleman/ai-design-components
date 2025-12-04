# Azure Patterns Skill - Master Plan

**Skill Name:** `azure-patterns`
**Skill Level:** Mid Level (5,000-8,000 tokens)
**Status:** Planning Phase (init.md complete, SKILL.md to be created)
**Last Updated:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [Azure Service Taxonomy](#azure-service-taxonomy)
5. [Decision Frameworks](#decision-frameworks)
6. [Implementation Patterns](#implementation-patterns)
7. [Well-Architected Framework](#well-architected-framework)
8. [Library Recommendations](#library-recommendations)
9. [Skill Structure Design](#skill-structure-design)
10. [Integration Points](#integration-points)
11. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why This Skill Matters

Azure is the second-largest cloud provider (23% market share in 2025) and the dominant choice for enterprises with existing Microsoft investments. Azure's unique strengths in hybrid cloud, enterprise integration, and AI services make it strategically important for modern cloud architectures.

**Market Drivers (2025):**
- **Enterprise Dominance:** 95% of Fortune 500 companies use Azure
- **Microsoft 365 Integration:** Seamless identity (Azure AD/Entra ID) and productivity tools
- **Hybrid Cloud Leader:** Azure Arc extends Azure services to on-premises and multi-cloud
- **AI/ML Innovation:** Azure OpenAI Service provides GPT-4, Claude, and other frontier models
- **Compliance Strength:** 100+ compliance certifications (more than any cloud provider)

**Strategic Value:**
1. **Enterprise Integration:** Native Microsoft ecosystem (Active Directory, SharePoint, Teams)
2. **Hybrid Cloud Excellence:** Azure Stack, Azure Arc for consistent operations across environments
3. **AI Services Leadership:** Azure OpenAI, Cognitive Services, Azure ML comprehensive platform
4. **Developer Productivity:** Visual Studio integration, GitHub Actions native support
5. **Global Reach:** 60+ regions (more than any cloud provider)

### How This Differs from Existing Solutions

**Existing Azure Documentation:**
- **Official Microsoft Learn:** Comprehensive but overwhelming (100,000+ documents)
- **Azure Architecture Center:** Excellent patterns but lacks service selection guidance
- **Blog Posts/Tutorials:** Tactical "how-to" without strategic decision frameworks
- **Third-Party Courses:** Often outdated in fast-moving Azure ecosystem

**Our Approach:**
- **Decision-First Framework:** When to use each service, not just how
- **Service Comparison Trees:** Container Apps vs. AKS vs. App Service vs. Functions
- **Cost-Aware Patterns:** TCO analysis built into every decision
- **Multi-Tool Implementation:** Bicep, Terraform, Azure CLI, and SDK examples
- **Enterprise Integration:** Entra ID, RBAC, Policy, and governance patterns
- **2025 Best Practices:** Azure Verified Modules, Landing Zones, FinOps integration

### Target Audience

**Primary Users:**
- Cloud architects designing Azure solutions
- DevOps engineers deploying to Azure
- Backend developers building Azure-native applications
- Enterprise IT teams migrating to Azure

**Skill Level Assumptions:**
- Understands cloud computing fundamentals (IaaS, PaaS, SaaS)
- Familiar with basic Azure concepts (Resource Groups, Subscriptions, Regions)
- Has used Azure Portal or Azure CLI
- Needs guidance on service selection and architecture patterns

---

## Skill Purpose and Scope

### What This Skill Teaches

**Core Competencies:**

1. **Compute Service Selection**
   - Azure Functions vs. Container Apps vs. AKS vs. App Service
   - VM selection (sizing, spot instances, reserved instances)
   - Batch computing for HPC and data processing
   - Azure CycleCloud for scientific computing

2. **Storage Architecture**
   - Blob Storage tiers (Hot, Cool, Cold, Archive)
   - Azure Files vs. NetApp Files vs. Elastic SAN
   - Managed Disks performance tiers (Standard, Premium SSD, Ultra Disk)
   - Data Lake Storage Gen2 for analytics

3. **Database Service Selection**
   - Azure SQL Database vs. SQL Managed Instance
   - Cosmos DB consistency models and API selection
   - PostgreSQL/MySQL Flexible Server vs. Single Server
   - Azure Database for MariaDB alternatives

4. **AI and Machine Learning Services**
   - Azure OpenAI Service (GPT-4, GPT-4 Turbo, embeddings)
   - Cognitive Services (Vision, Speech, Language, Decision)
   - Azure Machine Learning (training, deployment, MLOps)
   - Azure AI Search (formerly Cognitive Search)

5. **Integration and Messaging**
   - Service Bus vs. Event Grid vs. Event Hubs
   - Logic Apps for workflow automation
   - API Management for API governance
   - Azure Functions for event-driven integration

6. **Networking Architecture**
   - Virtual Network design and subnetting
   - Private Endpoints vs. Service Endpoints
   - Application Gateway vs. Front Door vs. Load Balancer
   - Azure Firewall and Network Security Groups

7. **Identity and Access Management**
   - Entra ID (Azure AD) authentication patterns
   - Managed Identities for Azure resources
   - Azure RBAC (built-in roles vs. custom roles)
   - Azure AD B2C for customer identity

8. **Governance and Compliance**
   - Azure Policy for guardrails
   - Azure Blueprints for repeatable environments
   - Cost Management and Budgets
   - Azure Advisor recommendations

### What This Skill Does NOT Cover

**Out of Scope:**
- **Azure DevOps Pipelines:** Covered by `building-ci-pipelines` skill
- **Kubernetes Deep Dive:** Covered by `kubernetes-operations` skill
- **Infrastructure as Code Basics:** Covered by `infrastructure-as-code` skill
- **Security Hardening Details:** Covered by `security-hardening` skill
- **Monitoring/Observability:** Covered by `observability` skill

### Success Criteria

**A user successfully uses this skill when they can:**
1. Select the appropriate Azure compute service for their workload
2. Design storage solutions balancing cost, performance, and durability
3. Choose the right database service for their data model and scale requirements
4. Integrate Azure OpenAI Service into applications
5. Implement messaging patterns for decoupled architectures
6. Design secure network architectures with Private Endpoints
7. Apply Azure Well-Architected Framework principles
8. Estimate and optimize Azure costs

---

## Research Findings

### Research Date: December 3, 2025

**Research Approach:**
Due to MCP service unavailability, this research is based on:
- Azure Well-Architected Framework documentation (as of January 2025)
- Azure Architecture Center patterns (updated through Q4 2024)
- Azure Friday and Azure updates blog posts
- Author's knowledge of Azure ecosystem (current through January 2025)

### Key Trends for 2025

**1. Azure Container Apps Momentum**
- **Trend:** Serverless container platform gaining rapid adoption
- **Advantages:**
  - Fully managed (no node management like AKS)
  - Built-in KEDA for event-driven scaling
  - Dapr integration for microservices
  - Lower cost than AKS for most workloads
- **When to Use:** Microservices, APIs, background workers, event processors
- **When to Avoid:** Need Kubernetes control plane access, complex networking

**2. Azure OpenAI Service Dominance**
- **Trend:** Enterprise-preferred way to access GPT-4 and other LLMs
- **Features:**
  - Data privacy (no model training on customer data)
  - Enterprise SLAs and support
  - Regional deployment options
  - Content filtering and abuse monitoring
- **Patterns:**
  - Retrieval-Augmented Generation (RAG) with Azure AI Search
  - Function calling for structured outputs
  - Prompt engineering and few-shot learning
  - Fine-tuning for domain-specific tasks

**3. Azure Verified Modules (AVM)**
- **Trend:** Microsoft-blessed Bicep and Terraform modules
- **Purpose:** Standardized, tested, secure infrastructure templates
- **Impact:** Replacing custom module development
- **Adoption:** Enterprise Landing Zones built on AVM

**4. FinOps Integration**
- **Trend:** Cost optimization is now architectural concern
- **Tools:**
  - Azure Cost Management (native)
  - FinOps Toolkit (Power BI dashboards)
  - Azure Advisor cost recommendations
- **Patterns:**
  - Reserved Instances for predictable workloads (40-60% savings)
  - Spot VMs for fault-tolerant batch jobs (up to 90% savings)
  - Auto-shutdown for dev/test resources
  - Storage tier optimization (Hot → Cool → Archive)

**5. Azure Arc Hybrid Cloud**
- **Trend:** Consistent Azure experience everywhere
- **Capabilities:**
  - Azure services on-premises (App Service, Functions, Data Services)
  - Multi-cloud Kubernetes management
  - Policy and governance across environments
  - Azure Monitor for hybrid infrastructure

**6. Private Endpoints Everywhere**
- **Trend:** Public endpoints considered security anti-pattern
- **Services:** Now supported by 100+ Azure services
- **Architecture:** All PaaS services accessed via private IPs in VNet
- **Impact:** Network complexity increases but security improves

**7. Azure Landing Zones**
- **Trend:** Enterprise-scale reference architectures
- **Components:**
  - Management groups hierarchy
  - Policy-driven governance
  - Hub-and-spoke networking
  - Identity and access management
- **Adoption:** Standard for large enterprises

### Best Practices Summary (2025)

**Compute:**
- ✅ Use Azure Container Apps for most containerized workloads
- ✅ Use AKS only when Kubernetes control plane access needed
- ✅ Use Azure Functions for event-driven, short-duration tasks
- ✅ Use App Service for simple web apps with auto-scaling
- ❌ Don't use VMs unless PaaS options don't fit

**Storage:**
- ✅ Use lifecycle management to move data to Cool/Archive tiers
- ✅ Use Azure Files for SMB shares, Blob Storage for object storage
- ✅ Enable soft delete and versioning for data protection
- ✅ Use Premium SSD only when IOPS requirements justify cost
- ❌ Don't use Hot tier for infrequently accessed data

**Database:**
- ✅ Use Cosmos DB for globally distributed, multi-model data
- ✅ Use Azure SQL Database for relational workloads with elastic scaling
- ✅ Use PostgreSQL Flexible Server for open-source workloads
- ✅ Use Azure Cache for Redis for session state and caching
- ❌ Don't use SQL Managed Instance unless VM-level access required

**AI/ML:**
- ✅ Use Azure OpenAI Service for GPT-4 access with enterprise features
- ✅ Use Cognitive Services for pre-built AI capabilities
- ✅ Use Azure Machine Learning for custom model training and MLOps
- ✅ Use Azure AI Search for RAG patterns
- ❌ Don't build custom models when pre-trained services available

**Networking:**
- ✅ Use Private Endpoints for all PaaS services
- ✅ Use Azure Front Door for global routing with WAF
- ✅ Use Application Gateway for regional load balancing
- ✅ Use Network Security Groups for micro-segmentation
- ❌ Don't expose services to public internet without justification

**Security:**
- ✅ Use Managed Identities (no credentials in code)
- ✅ Use Azure Key Vault for secrets, keys, and certificates
- ✅ Enable Microsoft Defender for Cloud (security posture)
- ✅ Use Azure Policy for preventive controls
- ❌ Don't use shared access keys when Managed Identity available

---

## Azure Service Taxonomy

### Compute Services

#### Tier 1: Serverless Container Platform (Azure Container Apps)

**Use When:**
- Microservices architecture (REST APIs, gRPC services)
- Event-driven applications (queue processors, webhooks)
- Background jobs and scheduled tasks
- Want Kubernetes benefits without operational overhead

**Bicep Example:**
```bicep
resource containerApp 'Microsoft.App/containerApps@2024-03-01' = {
  name: 'api-service'
  location: location
  properties: {
    managedEnvironmentId: containerAppEnvironment.id
    configuration: {
      ingress: {
        external: true
        targetPort: 8080
        transport: 'http'
        allowInsecure: false
      }
      secrets: [
        {
          name: 'db-connection-string'
          keyVaultUrl: 'https://keyvault.vault.azure.net/secrets/db-conn'
          identity: userAssignedIdentity.id
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'api'
          image: 'myregistry.azurecr.io/api:latest'
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
          env: [
            {
              name: 'DATABASE_URL'
              secretRef: 'db-connection-string'
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 10
        rules: [
          {
            name: 'http-scaling'
            http: {
              metadata: {
                concurrentRequests: '50'
              }
            }
          }
        ]
      }
    }
  }
}
```

**Terraform Example:**
```hcl
resource "azurerm_container_app" "api" {
  name                         = "api-service"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"

  template {
    container {
      name   = "api"
      image  = "myregistry.azurecr.io/api:latest"
      cpu    = 0.5
      memory = "1Gi"

      env {
        name        = "DATABASE_URL"
        secret_name = "db-connection-string"
      }
    }

    min_replicas = 1
    max_replicas = 10

    http_scale_rule {
      name                = "http-scaling"
      concurrent_requests = 50
    }
  }

  secret {
    name                = "db-connection-string"
    key_vault_secret_id = azurerm_key_vault_secret.db_conn.id
    identity            = azurerm_user_assigned_identity.main.id
  }

  ingress {
    external_enabled = true
    target_port      = 8080
    transport        = "http"
  }

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.main.id]
  }
}
```

#### Tier 2: Managed Kubernetes (Azure Kubernetes Service)

**Use When:**
- Need full Kubernetes control plane access
- Complex service mesh requirements (Istio, Linkerd)
- Custom CRDs and operators
- Multi-tenant cluster with advanced RBAC

**When to Avoid Container Apps:**
- Need specific Kubernetes features (NetworkPolicies, PodSecurityPolicies)
- Running existing Helm charts with complex dependencies
- Require fine-grained node pool management

**Bicep Example:**
```bicep
resource aks 'Microsoft.ContainerService/managedClusters@2024-01-01' = {
  name: 'production-aks'
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    dnsPrefix: 'production-aks'
    kubernetesVersion: '1.28'
    enableRBAC: true

    networkProfile: {
      networkPlugin: 'azure'
      networkPolicy: 'calico'
      loadBalancerSku: 'standard'
      serviceCidr: '10.0.0.0/16'
      dnsServiceIP: '10.0.0.10'
    }

    agentPoolProfiles: [
      {
        name: 'systempool'
        count: 3
        vmSize: 'Standard_D4s_v5'
        mode: 'System'
        osType: 'Linux'
        availabilityZones: ['1', '2', '3']
      }
      {
        name: 'userpool'
        count: 3
        vmSize: 'Standard_D8s_v5'
        mode: 'User'
        osType: 'Linux'
        availabilityZones: ['1', '2', '3']
        enableAutoScaling: true
        minCount: 3
        maxCount: 10
      }
    ]

    addonProfiles: {
      azureKeyvaultSecretsProvider: {
        enabled: true
      }
      azurepolicy: {
        enabled: true
      }
    }

    oidcIssuerProfile: {
      enabled: true
    }

    securityProfile: {
      workloadIdentity: {
        enabled: true
      }
    }
  }
}
```

#### Tier 3: Serverless Functions (Azure Functions)

**Use When:**
- Event-driven workloads (HTTP triggers, queue messages, timers)
- Short-duration tasks (< 10 minutes)
- Unpredictable or spiky traffic patterns
- Rapid development with minimal infrastructure

**Python Example:**
```python
# function_app.py
import azure.functions as func
import logging
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app = func.FunctionApp()

@app.function_name(name="HttpTrigger")
@app.route(route="hello", auth_level=func.AuthLevel.ANONYMOUS)
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
            name = req_body.get('name')
        except ValueError:
            pass

    if name:
        return func.HttpResponse(f"Hello, {name}!")
    else:
        return func.HttpResponse(
            "Please pass a name on the query string or in the request body",
            status_code=400
        )

@app.function_name(name="QueueTrigger")
@app.queue_trigger(arg_name="msg", queue_name="orders", connection="AzureWebJobsStorage")
def queue_trigger(msg: func.QueueMessage) -> None:
    logging.info('Python queue trigger function processed a queue item: %s', msg.get_body().decode('utf-8'))

    # Process order
    order = msg.get_json()
    logging.info(f"Processing order {order['id']}")

@app.function_name(name="TimerTrigger")
@app.schedule(schedule="0 */5 * * * *", arg_name="timer", run_on_startup=False)
def timer_trigger(timer: func.TimerRequest) -> None:
    logging.info('Python timer trigger function executed.')

    # Run cleanup or batch job
    if timer.past_due:
        logging.info('The timer is past due!')
```

#### Tier 4: Web Apps (Azure App Service)

**Use When:**
- Traditional web applications (ASP.NET, Node.js, Python, PHP)
- Need built-in CI/CD with GitHub Actions
- Want easy custom domain and SSL certificate management
- Require deployment slots for blue-green deployments

**Bicep Example:**
```bicep
resource appServicePlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: 'production-plan'
  location: location
  sku: {
    name: 'P1v3'
    tier: 'PremiumV3'
    capacity: 3
  }
  properties: {
    zoneRedundant: true
  }
}

resource webApp 'Microsoft.Web/sites@2023-01-01' = {
  name: 'myapp'
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true

    siteConfig: {
      linuxFxVersion: 'NODE|18-lts'
      minTlsVersion: '1.2'
      ftpsState: 'Disabled'
      http20Enabled: true

      appSettings: [
        {
          name: 'DATABASE_URL'
          value: '@Microsoft.KeyVault(VaultName=mykeyvault;SecretName=db-connection-string)'
        }
      ]
    }
  }
}
```

### Storage Services

#### Blob Storage Tier Selection

**Decision Framework:**

| Tier | Access Frequency | Cost/GB/Month | Use Case |
|------|------------------|---------------|----------|
| **Hot** | Daily access | $0.018 | Active data, frequently accessed files |
| **Cool** | <1/month access | $0.010 | Backups, logs, short-term archives (30+ days) |
| **Cold** | <90 days access | $0.0045 | Long-term backups, compliance data (90+ days) |
| **Archive** | Rare access | $0.00099 | Regulatory archives, multi-year retention |

**Lifecycle Management Example:**
```bicep
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'mystorageaccount'
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
    allowBlobPublicAccess: false
  }
}

resource lifecyclePolicy 'Microsoft.Storage/storageAccounts/managementPolicies@2023-01-01' = {
  parent: storageAccount
  name: 'default'
  properties: {
    policy: {
      rules: [
        {
          name: 'move-to-cool-after-30-days'
          enabled: true
          type: 'Lifecycle'
          definition: {
            filters: {
              blobTypes: ['blockBlob']
            }
            actions: {
              baseBlob: {
                tierToCool: {
                  daysAfterModificationGreaterThan: 30
                }
                tierToArchive: {
                  daysAfterModificationGreaterThan: 365
                }
                delete: {
                  daysAfterModificationGreaterThan: 2555  // 7 years
                }
              }
            }
          }
        }
      ]
    }
  }
}
```

### Database Services

#### Decision Framework: Which Azure Database?

```
START
  │
  ├─► Relational data?
  │     YES ──► SQL Server compatible?
  │               YES ──► Need VM-level access?
  │                         YES ──► SQL Managed Instance
  │                         NO  ──► Azure SQL Database
  │               NO ──► Open source?
  │                        PostgreSQL ──► Azure Database for PostgreSQL Flexible Server
  │                        MySQL ──► Azure Database for MySQL Flexible Server
  │     NO ──► Data model?
  │              Document/JSON ──► Cosmos DB (NoSQL API)
  │              Graph ──► Cosmos DB (Gremlin API)
  │              Wide-column ──► Cosmos DB (Cassandra API)
  │              Key-value ──► Cosmos DB (Table API) or Azure Cache for Redis
  │              Time-series ──► Azure Data Explorer
```

#### Azure Cosmos DB Consistency Levels

**Decision Matrix:**

| Level | Latency | Throughput | Use Case |
|-------|---------|------------|----------|
| **Strong** | Highest | Lowest | Financial transactions, inventory |
| **Bounded Staleness** | High | Low | Real-time leaderboards with slight lag acceptable |
| **Session** | Medium | Medium | Shopping carts, user sessions (default) |
| **Consistent Prefix** | Low | High | Social media feeds, IoT telemetry |
| **Eventual** | Lowest | Highest | Analytics, machine learning training data |

**Cosmos DB Example:**
```bicep
resource cosmosAccount 'Microsoft.DocumentDB/databaseAccounts@2024-05-15' = {
  name: 'mycosmosdb'
  location: location
  kind: 'GlobalDocumentDB'
  properties: {
    databaseAccountOfferType: 'Standard'
    consistencyPolicy: {
      defaultConsistencyLevel: 'Session'
    }
    locations: [
      {
        locationName: location
        failoverPriority: 0
        isZoneRedundant: true
      }
      {
        locationName: 'westus2'
        failoverPriority: 1
        isZoneRedundant: true
      }
    ]
    enableAutomaticFailover: true
    enableMultipleWriteLocations: true
    capabilities: [
      {
        name: 'EnableServerless'
      }
    ]
  }
}

resource cosmosDatabase 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2024-05-15' = {
  parent: cosmosAccount
  name: 'app-database'
  properties: {
    resource: {
      id: 'app-database'
    }
  }
}

resource cosmosContainer 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-05-15' = {
  parent: cosmosDatabase
  name: 'users'
  properties: {
    resource: {
      id: 'users'
      partitionKey: {
        paths: ['/userId']
        kind: 'Hash'
      }
      indexingPolicy: {
        indexingMode: 'consistent'
        automatic: true
        includedPaths: [
          { path: '/*' }
        ]
      }
    }
  }
}
```

### AI and Machine Learning Services

#### Azure OpenAI Service Integration

**Use Cases:**
- **Chatbots and Virtual Assistants:** GPT-4 for conversational AI
- **Content Generation:** Marketing copy, documentation, code
- **Semantic Search:** Embeddings with Azure AI Search (RAG pattern)
- **Code Generation:** GitHub Copilot-like functionality
- **Function Calling:** Structured outputs for tool use

**Python SDK Example:**
```python
# app.py
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

# Azure OpenAI setup with Managed Identity
credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(
    credential,
    "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
    azure_endpoint="https://myopenai.openai.azure.com",
    azure_ad_token_provider=token_provider,
    api_version="2024-02-15-preview"
)

# Retrieval-Augmented Generation (RAG) Pattern
search_client = SearchClient(
    endpoint="https://myaisearch.search.windows.net",
    index_name="product-docs",
    credential=AzureKeyCredential(os.environ["SEARCH_KEY"])
)

def rag_query(user_question: str) -> str:
    """Answer questions using RAG pattern with Azure AI Search."""

    # 1. Retrieve relevant documents
    search_results = search_client.search(
        search_text=user_question,
        top=3,
        select=["content", "title"]
    )

    context = "\n\n".join([
        f"Document: {doc['title']}\n{doc['content']}"
        for doc in search_results
    ])

    # 2. Generate answer with context
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that answers questions based on the provided context. If the answer is not in the context, say so."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {user_question}"
            }
        ],
        temperature=0.2,
        max_tokens=500
    )

    return response.choices[0].message.content

# Function calling example
def get_weather(location: str, unit: str = "celsius") -> str:
    """Get current weather for a location."""
    # Simulate API call
    return f"The weather in {location} is 22°{unit[0].upper()}"

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[{"role": "user", "content": "What's the weather like in Seattle?"}],
    tools=tools,
    tool_choice="auto"
)

# Handle function call
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    function_args = json.loads(tool_call.function.arguments)
    result = get_weather(**function_args)
    print(result)
```

### Integration and Messaging Services

#### Service Selection Framework

| Service | Pattern | Use Case | Message Size | Ordering | Transactions |
|---------|---------|----------|--------------|----------|--------------|
| **Service Bus** | Queue/Topic-Subscription | Enterprise messaging | 256 KB - 100 MB | Yes (sessions) | Yes |
| **Event Grid** | Pub/Sub | Event-driven architectures | 1 MB | No | No |
| **Event Hubs** | Streaming | Big data ingestion, telemetry | 1 MB | Yes (partitions) | No |
| **Storage Queues** | Simple queue | Async work, < 500k msgs/sec | 64 KB | No | No |

**Service Bus Example (Python):**
```python
# producer.py
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.identity import DefaultAzureCredential

# Use Managed Identity
credential = DefaultAzureCredential()
servicebus_client = ServiceBusClient(
    fully_qualified_namespace="myservicebus.servicebus.windows.net",
    credential=credential
)

with servicebus_client:
    sender = servicebus_client.get_queue_sender(queue_name="orders")
    with sender:
        message = ServiceBusMessage(
            body=json.dumps({"order_id": "12345", "total": 99.99}),
            content_type="application/json",
            message_id="order-12345",
            session_id="customer-abc"  # For ordered processing
        )
        sender.send_messages(message)

# consumer.py
from azure.servicebus import ServiceBusClient

with servicebus_client:
    receiver = servicebus_client.get_queue_receiver(queue_name="orders")
    with receiver:
        for msg in receiver:
            order = json.loads(str(msg))
            print(f"Processing order {order['order_id']}")

            # Process order...

            # Complete message (remove from queue)
            receiver.complete_message(msg)
```

**Event Grid Example (Bicep):**
```bicep
resource eventGridTopic 'Microsoft.EventGrid/topics@2023-12-15-preview' = {
  name: 'app-events'
  location: location
}

resource eventSubscription 'Microsoft.EventGrid/eventSubscriptions@2023-12-15-preview' = {
  name: 'order-processor-subscription'
  scope: eventGridTopic
  properties: {
    destination: {
      endpointType: 'WebHook'
      properties: {
        endpointUrl: 'https://myapp.azurewebsites.net/api/webhooks/orders'
      }
    }
    filter: {
      includedEventTypes: [
        'OrderPlaced'
        'OrderCancelled'
      ]
      advancedFilters: [
        {
          operatorType: 'NumberGreaterThan'
          key: 'data.total'
          value: 100
        }
      ]
    }
    retryPolicy: {
      maxDeliveryAttempts: 30
      eventTimeToLiveInMinutes: 1440
    }
  }
}
```

---

## Decision Frameworks

### Framework 1: Compute Service Selection

```
START
  │
  ├─► Container-based?
  │     YES ──► Need Kubernetes control?
  │               YES ──► Azure Kubernetes Service (AKS)
  │               NO ──► Event-driven?
  │                        YES ──► Azure Container Apps
  │                        NO ──► Long-running services?
  │                                  YES ──► Azure Container Apps
  │                                  NO ──► Azure Functions (containers)
  │     NO ──► Language/Framework?
  │              Event-driven function ──► Azure Functions
  │              Web app (Node, .NET, Python) ──► Azure App Service
  │              Batch/HPC ──► Azure Batch or VM Scale Sets
  │              Legacy app ──► Azure Virtual Machines
```

**Cost Comparison (Approximate, US East, 2025):**

| Service | Scenario | Monthly Cost |
|---------|----------|--------------|
| **Container Apps** | 1 vCPU, 2GB RAM, 24/7 | ~$60 |
| **AKS** | 3-node cluster (D4s_v5), 24/7 | ~$400 |
| **App Service** | P1v3 (2 vCPU, 8GB RAM), 24/7 | ~$145 |
| **Functions** | Premium EP1 (1 vCPU, 3.5GB RAM), 24/7 | ~$140 |
| **Functions** | Consumption (1M executions, 400ms avg) | ~$20 |

### Framework 2: Database Service Selection

**Relational Workload Decision Tree:**

```
Relational Database Needed
  │
  ├─► SQL Server features required? (T-SQL, SQL Agent, CLR)
  │     YES ──► VM-level access needed? (maintenance plans, linked servers)
  │               YES ──► Azure SQL Managed Instance
  │               NO ──► Azure SQL Database (Hyperscale for > 4TB)
  │     NO ──► Open source preferred?
  │              PostgreSQL ──► Azure Database for PostgreSQL Flexible Server
  │              MySQL ──► Azure Database for MySQL Flexible Server
  │              MariaDB ──► Migrate to PostgreSQL/MySQL (MariaDB deprecated)
```

**NoSQL Workload Decision Tree:**

```
NoSQL Database Needed
  │
  ├─► Global distribution required?
  │     YES ──► Cosmos DB (choose API: NoSQL, MongoDB, Cassandra, Gremlin)
  │     NO ──► Data model?
  │              Document/JSON ──► Cosmos DB (NoSQL API) or MongoDB on VM
  │              Key-value cache ──► Azure Cache for Redis
  │              Graph relationships ──► Cosmos DB (Gremlin API)
  │              Wide-column ──► Cosmos DB (Cassandra API)
  │              Time-series ──► Azure Data Explorer (ADX)
```

### Framework 3: Storage Service Selection

```
Storage Needed
  │
  ├─► File system interface required?
  │     YES ──► Protocol needed?
  │               SMB ──► Azure Files or Azure NetApp Files (high performance)
  │               NFS ──► Azure Files (NFS 4.1) or Azure NetApp Files
  │     NO ──► Object storage?
  │              YES ──► Blob Storage (with lifecycle management)
  │              NO ──► Block storage for VMs?
  │                       Standard workloads ──► Standard SSD Managed Disks
  │                       High IOPS (> 20,000) ──► Premium SSD or Ultra Disk
  │                       Analytics/Big Data ──► Azure Data Lake Storage Gen2
```

### Framework 4: Networking Architecture

**Private Endpoint vs. Service Endpoint:**

| Aspect | Private Endpoint | Service Endpoint |
|--------|------------------|------------------|
| **IP Address** | Private IP in VNet | Service keeps public IP |
| **Routing** | Traffic stays in VNet | Optimized route to service |
| **Access Control** | Network-level (NSG, firewall) | Service-level (firewall rules) |
| **Cost** | ~$7.30/month per endpoint | Free |
| **Use Case** | Production, strict isolation | Dev/test, cost-sensitive |

**Example Architecture (Hub-and-Spoke with Private Endpoints):**

```bicep
// Hub VNet with shared services
resource hubVnet 'Microsoft.Network/virtualNetworks@2023-05-01' = {
  name: 'hub-vnet'
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: ['10.0.0.0/16']
    }
    subnets: [
      {
        name: 'AzureFirewallSubnet'
        properties: {
          addressPrefix: '10.0.1.0/26'
        }
      }
      {
        name: 'GatewaySubnet'
        properties: {
          addressPrefix: '10.0.2.0/27'
        }
      }
      {
        name: 'private-endpoints'
        properties: {
          addressPrefix: '10.0.3.0/24'
          privateEndpointNetworkPolicies: 'Disabled'
        }
      }
    ]
  }
}

// Spoke VNet for application workloads
resource spokeVnet 'Microsoft.Network/virtualNetworks@2023-05-01' = {
  name: 'spoke-prod-vnet'
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: ['10.1.0.0/16']
    }
    subnets: [
      {
        name: 'app-subnet'
        properties: {
          addressPrefix: '10.1.1.0/24'
          delegations: [
            {
              name: 'container-apps-delegation'
              properties: {
                serviceName: 'Microsoft.App/environments'
              }
            }
          ]
        }
      }
    ]
  }
}

// VNet peering (hub-to-spoke)
resource peeringHubToSpoke 'Microsoft.Network/virtualNetworks/virtualNetworkPeerings@2023-05-01' = {
  parent: hubVnet
  name: 'hub-to-spoke-prod'
  properties: {
    remoteVirtualNetwork: {
      id: spokeVnet.id
    }
    allowVirtualNetworkAccess: true
    allowForwardedTraffic: true
    allowGatewayTransit: true
  }
}

// Private endpoint for Azure SQL Database in hub
resource sqlPrivateEndpoint 'Microsoft.Network/privateEndpoints@2023-05-01' = {
  name: 'sql-private-endpoint'
  location: location
  properties: {
    subnet: {
      id: '${hubVnet.id}/subnets/private-endpoints'
    }
    privateLinkServiceConnections: [
      {
        name: 'sql-connection'
        properties: {
          privateLinkServiceId: sqlServer.id
          groupIds: ['sqlServer']
        }
      }
    ]
  }
}

// Private DNS zone for SQL Database
resource privateDnsZone 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: 'privatelink.database.windows.net'
  location: 'global'
}

resource dnsZoneLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = {
  parent: privateDnsZone
  name: 'hub-link'
  location: 'global'
  properties: {
    virtualNetwork: {
      id: hubVnet.id
    }
    registrationEnabled: false
  }
}
```

---

## Well-Architected Framework

### Five Pillars Overview

1. **Cost Optimization** - Maximize value within budget
2. **Operational Excellence** - Run reliable, manageable systems
3. **Performance Efficiency** - Scale to meet demand efficiently
4. **Reliability** - Recover from failures, meet availability commitments
5. **Security** - Protect data, systems, and assets

### Pillar 1: Cost Optimization Patterns

**Reserved Instances Strategy:**
```
Workload Analysis
  │
  ├─► Steady-state workload (24/7 for 1-3 years)?
  │     YES ──► Purchase Reserved Instances (40-60% savings)
  │               1-year commitment ──► Standard-tier databases, VMs
  │               3-year commitment ──► Maximum savings for stable workloads
  │     NO ──► Workload pattern?
  │              Predictable hours (business hours only) ──► Auto-shutdown/scaling
  │              Unpredictable spikes ──► Consumption/serverless pricing
  │              Fault-tolerant batch ──► Spot VMs (up to 90% savings)
```

**Azure Advisor Cost Recommendations:**
- Right-size underutilized VMs
- Delete unattached disks and NICs
- Enable auto-pause for Azure SQL Database serverless
- Move cold data to lower storage tiers
- Purchase reserved capacity for predictable workloads

### Pillar 2: Operational Excellence Patterns

**Azure Policy for Guardrails:**
```bicep
// Require tags on all resources
resource requireTagsPolicy 'Microsoft.Authorization/policyDefinitions@2021-06-01' = {
  name: 'require-tags-policy'
  properties: {
    policyType: 'Custom'
    mode: 'Indexed'
    displayName: 'Require tags: Environment, Owner, CostCenter'
    policyRule: {
      if: {
        anyOf: [
          { field: 'tags.Environment', exists: false }
          { field: 'tags.Owner', exists: false }
          { field: 'tags.CostCenter', exists: false }
        ]
      }
      then: {
        effect: 'deny'
      }
    }
  }
}

// Allowed regions policy
resource allowedLocationsPolicy 'Microsoft.Authorization/policyDefinitions@2021-06-01' = {
  name: 'allowed-locations-policy'
  properties: {
    policyType: 'Custom'
    mode: 'Indexed'
    displayName: 'Allowed Azure regions'
    policyRule: {
      if: {
        not: {
          field: 'location'
          in: [
            'eastus'
            'eastus2'
            'westus2'
            'centralus'
          ]
        }
      }
      then: {
        effect: 'deny'
      }
    }
  }
}

// Assign policies to subscription
resource policyAssignment 'Microsoft.Authorization/policyAssignments@2022-06-01' = {
  name: 'governance-policies'
  properties: {
    policyDefinitionId: requireTagsPolicy.id
    displayName: 'Enforce governance policies'
  }
}
```

### Pillar 3: Performance Efficiency Patterns

**Autoscaling Configuration:**
```bicep
// Container Apps autoscaling with multiple rules
resource containerApp 'Microsoft.App/containerApps@2024-03-01' = {
  name: 'api-service'
  properties: {
    template: {
      scale: {
        minReplicas: 2  // Always 2 for HA
        maxReplicas: 50
        rules: [
          // Scale based on HTTP concurrency
          {
            name: 'http-rule'
            http: {
              metadata: {
                concurrentRequests: '100'
              }
            }
          }
          // Scale based on Azure Service Bus queue depth
          {
            name: 'queue-rule'
            azureQueue: {
              queueName: 'orders'
              queueLength: '10'
              auth: [
                {
                  secretRef: 'servicebus-connection'
                  triggerParameter: 'connection'
                }
              ]
            }
          }
          // Scale based on time (business hours)
          {
            name: 'business-hours-rule'
            custom: {
              type: 'cron'
              metadata: {
                timezone: 'America/New_York'
                start: '0 8 * * MON-FRI'  // 8 AM weekdays
                end: '0 18 * * MON-FRI'   // 6 PM weekdays
                desiredReplicas: '10'
              }
            }
          }
        ]
      }
    }
  }
}
```

### Pillar 4: Reliability Patterns

**Multi-Region Deployment with Traffic Manager:**
```bicep
resource trafficManagerProfile 'Microsoft.Network/trafficmanagerprofiles@2022-04-01' = {
  name: 'myapp-traffic-manager'
  location: 'global'
  properties: {
    profileStatus: 'Enabled'
    trafficRoutingMethod: 'Performance'  // Route to fastest region
    dnsConfig: {
      relativeName: 'myapp'
      ttl: 60
    }
    monitorConfig: {
      protocol: 'HTTPS'
      port: 443
      path: '/health'
      intervalInSeconds: 30
      toleratedNumberOfFailures: 3
      timeoutInSeconds: 10
    }
    endpoints: [
      {
        name: 'eastus-endpoint'
        type: 'Microsoft.Network/trafficManagerProfiles/azureEndpoints'
        properties: {
          targetResourceId: webAppEastUs.id
          endpointStatus: 'Enabled'
          weight: 100
          priority: 1
        }
      }
      {
        name: 'westeurope-endpoint'
        type: 'Microsoft.Network/trafficManagerProfiles/azureEndpoints'
        properties: {
          targetResourceId: webAppWestEurope.id
          endpointStatus: 'Enabled'
          weight: 100
          priority: 2  // Failover priority
        }
      }
    ]
  }
}
```

**Availability Zones for High Availability:**
```bicep
// VM Scale Set with zone redundancy
resource vmss 'Microsoft.Compute/virtualMachineScaleSets@2023-09-01' = {
  name: 'app-vmss'
  location: location
  zones: ['1', '2', '3']  // Distribute across AZs
  sku: {
    name: 'Standard_D4s_v5'
    capacity: 6  // 2 instances per zone
  }
  properties: {
    zoneBalance: true  // Even distribution
    platformFaultDomainCount: 1
    singlePlacementGroup: false

    virtualMachineProfile: {
      storageProfile: {
        imageReference: {
          publisher: 'Canonical'
          offer: 'UbuntuServer'
          sku: '22.04-LTS'
          version: 'latest'
        }
        osDisk: {
          createOption: 'FromImage'
          managedDisk: {
            storageAccountType: 'Premium_ZRS'  // Zone-redundant storage
          }
        }
      }
    }
  }
}
```

### Pillar 5: Security Patterns

**Managed Identity for Service-to-Service Authentication:**
```bicep
// Container App with Managed Identity
resource containerApp 'Microsoft.App/containerApps@2024-03-01' = {
  name: 'api-service'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    configuration: {
      secrets: [
        {
          name: 'db-connection'
          keyVaultUrl: 'https://mykeyvault.vault.azure.net/secrets/db-connection-string'
          identity: 'system'
        }
      ]
    }
  }
}

// Grant Container App access to Key Vault
resource keyVaultAccessPolicy 'Microsoft.KeyVault/vaults/accessPolicies@2023-02-01' = {
  parent: keyVault
  name: 'add'
  properties: {
    accessPolicies: [
      {
        tenantId: subscription().tenantId
        objectId: containerApp.identity.principalId
        permissions: {
          secrets: ['get']
        }
      }
    ]
  }
}

// Grant Container App access to Azure SQL Database
resource sqlRoleAssignment 'Microsoft.Sql/servers/databases/sqlRoleAssignments@2023-05-01-preview' = {
  parent: sqlDatabase
  name: guid(containerApp.id, sqlDatabase.id, 'db_datareader')
  properties: {
    principalId: containerApp.identity.principalId
    roleDefinitionId: '/subscriptions/${subscription().subscriptionId}/providers/Microsoft.Sql/servers/${sqlServer.name}/databases/${sqlDatabase.name}/roleDefinitions/db_datareader'
  }
}
```

**Python SDK with Managed Identity:**
```python
# app.py
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobServiceClient
import pyodbc

# Managed Identity authentication (no secrets in code!)
credential = DefaultAzureCredential()

# Access Key Vault
keyvault_client = SecretClient(
    vault_url="https://mykeyvault.vault.azure.net",
    credential=credential
)
db_connection_string = keyvault_client.get_secret("db-connection-string").value

# Access Blob Storage
blob_service_client = BlobServiceClient(
    account_url="https://mystorageaccount.blob.core.windows.net",
    credential=credential
)

# Access Azure SQL Database with Managed Identity
conn = pyodbc.connect(
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=tcp:myserver.database.windows.net,1433;"
    "Database=mydb;"
    "Authentication=ActiveDirectoryMsi;"  # Managed Identity auth
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
)
```

---

## Library Recommendations

### Infrastructure as Code

| Tool | Version | Use Case | Language |
|------|---------|----------|----------|
| **Bicep** | Latest | Azure-native, recommended by Microsoft | Bicep DSL |
| **Terraform** | 1.6+ | Multi-cloud, mature ecosystem | HCL |
| **Pulumi** | 3.x | Developer-centric, programming languages | TS/Python/Go/C# |
| **Azure CLI** | 2.x | Scripting, automation | Bash/PowerShell |

**Recommendation:** Use Bicep for Azure-only infrastructure (best Azure integration), Terraform for multi-cloud environments.

### Azure SDKs

| Language | SDK Version | Package Manager | Notes |
|----------|-------------|-----------------|-------|
| **Python** | azure-* 12.x+ | pip | Most comprehensive, newest features first |
| **TypeScript/JavaScript** | @azure/* | npm | Excellent for Node.js backends, Functions |
| **.NET/C#** | Azure.* 12.x+ | NuGet | Best performance, native Azure support |
| **Go** | github.com/Azure/azure-sdk-for-go | go get | Growing ecosystem, good for CLI tools |
| **Java** | com.azure:azure-* | Maven/Gradle | Enterprise Java applications |

**Python SDK Example:**
```python
# requirements.txt
azure-identity==1.15.0
azure-keyvault-secrets==4.7.0
azure-storage-blob==12.19.0
azure-cosmos==4.5.1
azure-servicebus==7.11.4
openai==1.10.0  # Azure OpenAI

# app.py
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient
from azure.servicebus import ServiceBusClient

credential = DefaultAzureCredential()

# Blob Storage client
blob_service = BlobServiceClient(
    account_url="https://mystorageaccount.blob.core.windows.net",
    credential=credential
)

# Cosmos DB client
cosmos_client = CosmosClient(
    url="https://mycosmosdb.documents.azure.com:443/",
    credential=credential
)

# Service Bus client
servicebus_client = ServiceBusClient(
    fully_qualified_namespace="myservicebus.servicebus.windows.net",
    credential=credential
)
```

### Monitoring and Observability

| Tool | Purpose | Azure Integration |
|------|---------|-------------------|
| **Azure Monitor** | Native monitoring, metrics, logs | Built-in |
| **Application Insights** | APM, distributed tracing | Built-in |
| **Azure Log Analytics** | Log aggregation and querying (KQL) | Built-in |
| **Prometheus** | Metrics (AKS) | Managed Prometheus in Azure Monitor |
| **Grafana** | Dashboards | Managed Grafana in Azure Monitor |

### Development Tools

| Tool | Purpose |
|------|---------|
| **Azure CLI** | Command-line management |
| **Azure PowerShell** | PowerShell cmdlets for Azure |
| **Azure Developer CLI (azd)** | Opinionated app deployment |
| **Azure Bicep Extension (VS Code)** | Bicep language support |
| **Azure Functions Core Tools** | Local Functions development |
| **Azurite** | Local storage emulator |

---

## Skill Structure Design

```
azure-patterns/
├── SKILL.md                         # Main skill (600-800 lines)
├── references/
│   ├── compute-services.md          # Container Apps, AKS, Functions, App Service
│   ├── storage-patterns.md          # Blob, Files, Disks, Data Lake
│   ├── database-selection.md        # SQL, Cosmos DB, PostgreSQL, MySQL
│   ├── ai-integration.md            # Azure OpenAI, Cognitive Services, Azure ML
│   ├── messaging-patterns.md        # Service Bus, Event Grid, Event Hubs
│   ├── networking-architecture.md   # VNets, Private Endpoints, Front Door
│   ├── identity-access.md           # Entra ID, Managed Identity, RBAC
│   ├── governance-compliance.md     # Azure Policy, Blueprints, Cost Management
│   └── well-architected.md          # Five pillars implementation
├── examples/
│   ├── bicep/
│   │   ├── container-apps/
│   │   ├── aks-cluster/
│   │   ├── hub-spoke-networking/
│   │   └── cosmos-db/
│   ├── terraform/
│   │   ├── container-apps/
│   │   ├── aks-cluster/
│   │   └── hub-spoke-networking/
│   └── sdk/
│       ├── python/
│       │   ├── azure-openai-rag.py
│       │   ├── managed-identity-auth.py
│       │   └── service-bus-messaging.py
│       └── typescript/
│           ├── azure-openai-rag.ts
│           └── managed-identity-auth.ts
└── scripts/
    ├── cost-estimate.sh             # Azure pricing calculator wrapper
    ├── validate-bicep.sh            # Bicep linting and validation
    └── security-scan.sh             # Checkov/tfsec for IaC security
```

---

## Integration Points

### With Existing Skills

| Skill | Integration |
|-------|-------------|
| `infrastructure-as-code` | Azure patterns implemented via Bicep/Terraform |
| `kubernetes-operations` | AKS-specific patterns and configuration |
| `deploying-applications` | Container Apps, App Service deployment |
| `building-ci-pipelines` | Azure DevOps, GitHub Actions integration |
| `auth-security` | Entra ID, Managed Identity, Key Vault |
| `observability` | Azure Monitor, Application Insights |
| `ai-chat` | Azure OpenAI Service integration |
| `databases-*` | Azure SQL, Cosmos DB, PostgreSQL patterns |

### Skill Chaining Example

```
azure-patterns → infrastructure-as-code → deploying-applications
      │                     │                      │
      ▼                     ▼                      ▼
Select services      Provision with Bicep    Deploy containers
(Container Apps,     (ARM templates,         (CI/CD, GitHub
 Cosmos DB,          state management)        Actions)
 OpenAI)
```

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- [ ] Core decision frameworks (compute, storage, database)
- [ ] Bicep examples for common services
- [ ] Azure CLI patterns and scripts
- [ ] Cost optimization patterns

### Phase 2: Advanced Services (Week 3-4)
- [ ] Azure OpenAI integration patterns
- [ ] Messaging and event-driven architectures
- [ ] Networking architecture (hub-spoke, Private Endpoints)
- [ ] Identity and access management (Managed Identity, RBAC)

### Phase 3: SDK and Automation (Week 5-6)
- [ ] Python SDK examples (most comprehensive)
- [ ] TypeScript SDK examples
- [ ] Terraform examples (for multi-cloud shops)
- [ ] Azure Policy and governance patterns

### Phase 4: Well-Architected Framework (Week 7-8)
- [ ] Five pillars implementation guide
- [ ] Cost optimization deep-dive
- [ ] Security hardening patterns
- [ ] Reliability and HA architectures
- [ ] Polish and review

---

## Key Takeaways

1. **Container Apps First** - Use Azure Container Apps for most containerized workloads (simpler and cheaper than AKS)
2. **Private Endpoints Everywhere** - Treat public endpoints as security anti-pattern
3. **Managed Identity Always** - Never hardcode credentials when Managed Identity available
4. **Cost Optimization Built-In** - Reserved Instances for steady-state, consumption pricing for variable workloads
5. **Azure OpenAI for AI** - Enterprise-grade LLM access with data privacy
6. **Bicep for Azure-Native** - Microsoft's recommended IaC tool for Azure
7. **Well-Architected Framework** - Apply five pillars to every architecture decision
8. **Hub-Spoke Networking** - Standard enterprise pattern for secure, scalable networks

---

## Additional Resources

- **Azure Architecture Center:** https://learn.microsoft.com/en-us/azure/architecture/
- **Azure Well-Architected Framework:** https://learn.microsoft.com/en-us/azure/well-architected/
- **Azure Verified Modules:** https://aka.ms/avm
- **Azure Charts (Service Comparison):** https://azurecharts.com/
- **Azure Speed Test:** https://azurespeedtest.azurewebsites.net/
- **Azure Updates:** https://azure.microsoft.com/updates/

---

**Progressive disclosure:** This init.md provides the master plan. Detailed documentation in `references/` directory with Bicep, Terraform, and SDK examples in `examples/`.
