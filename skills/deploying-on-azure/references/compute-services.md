# Azure Compute Services Reference

Comprehensive guide to Azure compute service selection, configuration, and implementation patterns.

## Table of Contents

1. [Azure Container Apps](#azure-container-apps)
2. [Azure Kubernetes Service (AKS)](#azure-kubernetes-service-aks)
3. [Azure Functions](#azure-functions)
4. [Azure App Service](#azure-app-service)
5. [Virtual Machines](#virtual-machines)
6. [Cost Comparison](#cost-comparison)

---

## Azure Container Apps

**Best For:** Microservices, APIs, background workers, event-driven applications

**Key Features:**
- Fully managed container platform (no node management)
- Built-in KEDA for event-driven autoscaling
- Dapr integration for microservices patterns
- Automatic HTTPS with custom domains
- Traffic splitting for blue-green deployments

### When to Use Container Apps

Choose Container Apps when:
- Building microservices architecture
- Need Kubernetes benefits without operational overhead
- Event-driven scaling (HTTP, queue depth, custom metrics)
- Want lower cost than AKS
- Dapr integration for distributed patterns

Avoid Container Apps when:
- Need full Kubernetes control plane access
- Require custom CRDs or operators
- Complex service mesh (Istio, Linkerd)
- Existing Helm chart dependencies

### Bicep Implementation

```bicep
// Container App Environment (shared by multiple apps)
resource containerAppEnvironment 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: 'production-env'
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
    zoneRedundant: true
    vnetConfiguration: {
      infrastructureSubnetId: subnet.id
      internal: true  // Private environment
    }
  }
}

// Container App with autoscaling
resource containerApp 'Microsoft.App/containerApps@2024-03-01' = {
  name: 'api-service'
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    managedEnvironmentId: containerAppEnvironment.id
    configuration: {
      activeRevisionsMode: 'Single'
      ingress: {
        external: true
        targetPort: 8080
        transport: 'http2'
        allowInsecure: false
        traffic: [
          {
            latestRevision: true
            weight: 100
          }
        ]
        customDomains: [
          {
            name: 'api.example.com'
            bindingType: 'SniEnabled'
            certificateId: certificate.id
          }
        ]
      }
      secrets: [
        {
          name: 'db-connection-string'
          keyVaultUrl: 'https://keyvault.vault.azure.net/secrets/db-conn'
          identity: 'system'
        }
        {
          name: 'api-key'
          value: apiKey
        }
      ]
      registries: [
        {
          server: 'myregistry.azurecr.io'
          identity: 'system'
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'api'
          image: 'myregistry.azurecr.io/api:latest'
          resources: {
            cpu: json('1.0')
            memory: '2Gi'
          }
          env: [
            {
              name: 'DATABASE_URL'
              secretRef: 'db-connection-string'
            }
            {
              name: 'API_KEY'
              secretRef: 'api-key'
            }
            {
              name: 'ENVIRONMENT'
              value: 'production'
            }
          ]
          probes: [
            {
              type: 'Liveness'
              httpGet: {
                path: '/health'
                port: 8080
              }
              initialDelaySeconds: 10
              periodSeconds: 10
            }
            {
              type: 'Readiness'
              httpGet: {
                path: '/ready'
                port: 8080
              }
              initialDelaySeconds: 5
              periodSeconds: 5
            }
          ]
        }
      ]
      scale: {
        minReplicas: 2
        maxReplicas: 50
        rules: [
          // HTTP concurrency scaling
          {
            name: 'http-scaling-rule'
            http: {
              metadata: {
                concurrentRequests: '100'
              }
            }
          }
          // Azure Service Bus queue scaling
          {
            name: 'queue-scaling-rule'
            custom: {
              type: 'azure-servicebus'
              metadata: {
                queueName: 'orders'
                messageCount: '10'
                namespace: 'myservicebus'
              }
              auth: [
                {
                  secretRef: 'servicebus-connection'
                  triggerParameter: 'connection'
                }
              ]
            }
          }
          // Time-based scaling (business hours)
          {
            name: 'business-hours-rule'
            custom: {
              type: 'cron'
              metadata: {
                timezone: 'America/New_York'
                start: '0 8 * * MON-FRI'
                end: '0 18 * * MON-FRI'
                desiredReplicas: '20'
              }
            }
          }
        ]
      }
    }
  }
}
```

### Terraform Implementation

```hcl
resource "azurerm_container_app_environment" "main" {
  name                       = "production-env"
  location                   = var.location
  resource_group_name        = azurerm_resource_group.main.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id
  zone_redundancy_enabled    = true

  infrastructure_subnet_id = azurerm_subnet.container_apps.id
  internal_load_balancer_enabled = true
}

resource "azurerm_container_app" "api" {
  name                         = "api-service"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"

  identity {
    type = "SystemAssigned"
  }

  registry {
    server   = "myregistry.azurecr.io"
    identity = "system"
  }

  secret {
    name                = "db-connection-string"
    key_vault_secret_id = azurerm_key_vault_secret.db_conn.id
    identity            = "system"
  }

  template {
    container {
      name   = "api"
      image  = "myregistry.azurecr.io/api:latest"
      cpu    = 1.0
      memory = "2Gi"

      env {
        name        = "DATABASE_URL"
        secret_name = "db-connection-string"
      }

      liveness_probe {
        transport = "HTTP"
        port      = 8080
        path      = "/health"
      }

      readiness_probe {
        transport = "HTTP"
        port      = 8080
        path      = "/ready"
      }
    }

    min_replicas = 2
    max_replicas = 50

    http_scale_rule {
      name                = "http-scaling"
      concurrent_requests = 100
    }

    custom_scale_rule {
      name             = "queue-scaling"
      custom_rule_type = "azure-servicebus"
      metadata = {
        queueName    = "orders"
        messageCount = "10"
        namespace    = "myservicebus"
      }
      authentication {
        secret_name       = "servicebus-connection"
        trigger_parameter = "connection"
      }
    }
  }

  ingress {
    external_enabled = true
    target_port      = 8080
    transport        = "http2"

    custom_domain {
      name           = "api.example.com"
      certificate_id = azurerm_container_app_certificate.main.id
    }

    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }
}
```

---

## Azure Kubernetes Service (AKS)

**Best For:** Complex Kubernetes workloads, service mesh, multi-tenant clusters, custom operators

**Key Features:**
- Fully managed Kubernetes control plane
- Multiple node pools with different VM sizes
- Azure CNI or Kubenet networking
- Workload Identity for pod-level authentication
- Integrated monitoring with Azure Monitor

### When to Use AKS

Choose AKS when:
- Need full Kubernetes control plane access
- Using Helm charts with complex dependencies
- Implementing service mesh (Istio, Linkerd)
- Require custom CRDs and operators
- Multi-tenant cluster with advanced RBAC
- Existing Kubernetes expertise

Avoid AKS when:
- Simple container hosting needs
- Limited Kubernetes knowledge
- Want to minimize operational overhead
- Cost-sensitive (Container Apps cheaper for most workloads)

### Bicep Implementation

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
    aadProfile: {
      managed: true
      enableAzureRBAC: true
      adminGroupObjectIDs: [
        adminGroupId
      ]
    }

    networkProfile: {
      networkPlugin: 'azure'  // Azure CNI
      networkPolicy: 'calico'
      loadBalancerSku: 'standard'
      serviceCidr: '10.0.0.0/16'
      dnsServiceIP: '10.0.0.10'
      outboundType: 'loadBalancer'
    }

    agentPoolProfiles: [
      // System node pool (for kube-system pods)
      {
        name: 'systempool'
        count: 3
        vmSize: 'Standard_D4s_v5'
        mode: 'System'
        osType: 'Linux'
        osSKU: 'AzureLinux'
        availabilityZones: ['1', '2', '3']
        enableAutoScaling: true
        minCount: 3
        maxCount: 6
        nodeTaints: [
          'CriticalAddonsOnly=true:NoSchedule'
        ]
      }
      // User node pool (for application workloads)
      {
        name: 'userpool'
        count: 3
        vmSize: 'Standard_D8s_v5'
        mode: 'User'
        osType: 'Linux'
        osSKU: 'AzureLinux'
        availabilityZones: ['1', '2', '3']
        enableAutoScaling: true
        minCount: 3
        maxCount: 20
        maxPods: 110
      }
      // GPU node pool (for ML workloads)
      {
        name: 'gpupool'
        count: 0
        vmSize: 'Standard_NC6s_v3'
        mode: 'User'
        osType: 'Linux'
        enableAutoScaling: true
        minCount: 0
        maxCount: 5
        nodeTaints: [
          'nvidia.com/gpu=true:NoSchedule'
        ]
      }
    ]

    addonProfiles: {
      azureKeyvaultSecretsProvider: {
        enabled: true
        config: {
          enableSecretRotation: 'true'
          rotationPollInterval: '2m'
        }
      }
      azurepolicy: {
        enabled: true
      }
      omsagent: {
        enabled: true
        config: {
          logAnalyticsWorkspaceResourceID: logAnalytics.id
        }
      }
    }

    oidcIssuerProfile: {
      enabled: true
    }

    securityProfile: {
      workloadIdentity: {
        enabled: true
      }
      defender: {
        logAnalyticsWorkspaceResourceId: logAnalytics.id
        securityMonitoring: {
          enabled: true
        }
      }
    }

    autoUpgradeProfile: {
      upgradeChannel: 'stable'
    }
  }
}

// Grant AKS access to pull images from ACR
resource acrPullRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(aks.id, acr.id, 'AcrPull')
  scope: acr
  properties: {
    principalId: aks.properties.identityProfile.kubeletidentity.objectId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')
  }
}
```

---

## Azure Functions

**Best For:** Event-driven workloads, short-duration tasks, serverless APIs

**Key Features:**
- Multiple trigger types (HTTP, Timer, Queue, Blob, Event Hub)
- Consumption pricing (pay per execution)
- Premium plan for VNet integration and longer timeouts
- Durable Functions for stateful orchestrations
- Python, Node.js, .NET, Java, PowerShell support

### Hosting Plans

| Plan | Max Duration | Pricing | VNet Integration | Use Case |
|------|--------------|---------|------------------|----------|
| **Consumption** | 5 minutes (default) | Per execution | No | Unpredictable traffic, cost-sensitive |
| **Premium** | 60 minutes (default) | Per hour running | Yes | Predictable traffic, VNet required |
| **Dedicated (App Service)** | Unlimited | App Service Plan | Yes | Existing App Service capacity |

### Python Function Example

```python
# function_app.py
import azure.functions as func
import logging
import json
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp()

# HTTP trigger with Managed Identity
@app.function_name(name="ProcessOrder")
@app.route(route="orders", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
def process_order(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing order request')

    try:
        # Get order from request body
        order = req.get_json()

        # Use Managed Identity to access Key Vault
        credential = DefaultAzureCredential()
        keyvault_client = SecretClient(
            vault_url="https://mykeyvault.vault.azure.net",
            credential=credential
        )
        api_key = keyvault_client.get_secret("external-api-key").value

        # Process order...
        logging.info(f"Order {order['id']} processed successfully")

        return func.HttpResponse(
            json.dumps({"status": "success", "order_id": order['id']}),
            mimetype="application/json",
            status_code=200
        )

    except ValueError as e:
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON"}),
            mimetype="application/json",
            status_code=400
        )
    except Exception as e:
        logging.error(f"Error processing order: {e}")
        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            mimetype="application/json",
            status_code=500
        )

# Queue trigger (Azure Storage Queue)
@app.function_name(name="ProcessQueueMessage")
@app.queue_trigger(arg_name="msg", queue_name="orders", connection="AzureWebJobsStorage")
def process_queue_message(msg: func.QueueMessage) -> None:
    logging.info(f'Processing queue message: {msg.id}')

    order = json.loads(msg.get_body().decode('utf-8'))
    logging.info(f"Order ID: {order['id']}, Total: {order['total']}")

    # Process order asynchronously...

# Timer trigger (runs every 5 minutes)
@app.function_name(name="CleanupOldData")
@app.schedule(schedule="0 */5 * * * *", arg_name="timer", run_on_startup=False)
def cleanup_old_data(timer: func.TimerRequest) -> None:
    if timer.past_due:
        logging.info('Timer is past due!')

    logging.info('Running cleanup job...')

    # Cleanup old data, send reports, etc.

# Blob trigger (fires when blob created)
@app.function_name(name="ProcessUploadedImage")
@app.blob_trigger(arg_name="blob", path="uploads/{name}", connection="AzureWebJobsStorage")
@app.blob_output(arg_name="outputblob", path="processed/{name}", connection="AzureWebJobsStorage")
def process_uploaded_image(blob: func.InputStream, outputblob: func.Out[bytes]) -> None:
    logging.info(f'Processing blob: {blob.name}, Size: {blob.length} bytes')

    # Read blob content
    content = blob.read()

    # Process image (resize, compress, etc.)
    processed_content = content  # Placeholder

    # Write to output blob
    outputblob.set(processed_content)
```

### Bicep Deployment

```bicep
resource functionApp 'Microsoft.Web/sites@2023-01-01' = {
  name: 'my-function-app'
  location: location
  kind: 'functionapp,linux'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'Python|3.11'
      appSettings: [
        {
          name: 'AzureWebJobsStorage__accountName'
          value: storageAccount.name
        }
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~4'
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
        {
          name: 'KEY_VAULT_URL'
          value: 'https://mykeyvault.vault.azure.net'
        }
      ]
      ftpsState: 'Disabled'
      minTlsVersion: '1.2'
    }
  }
}
```

---

## Azure App Service

**Best For:** Web applications, REST APIs, mobile backends

**Key Features:**
- Built-in CI/CD with GitHub Actions
- Deployment slots for staging/production
- Auto-scaling based on metrics
- Custom domains and SSL certificates
- Multiple language support (.NET, Node.js, Python, PHP, Java)

### When to Use App Service

Choose App Service when:
- Building traditional web applications
- Need easy deployment slots (blue-green)
- Want integrated CI/CD
- Simple autoscaling requirements
- Multi-language support needed

### Service Plan Tiers

| Tier | vCPUs | RAM | Auto-scale | VNet | Price/Month |
|------|-------|-----|------------|------|-------------|
| **F1 (Free)** | Shared | 1 GB | No | No | $0 |
| **B1 (Basic)** | 1 | 1.75 GB | No | No | ~$13 |
| **S1 (Standard)** | 1 | 1.75 GB | Yes | No | ~$70 |
| **P1v3 (Premium)** | 2 | 8 GB | Yes | Yes | ~$145 |
| **I1v2 (Isolated)** | 2 | 8 GB | Yes | Yes (dedicated) | ~$400 |

### Bicep Implementation

```bicep
resource appServicePlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: 'production-plan'
  location: location
  sku: {
    name: 'P1v3'
    tier: 'PremiumV3'
    capacity: 3
  }
  kind: 'linux'
  properties: {
    reserved: true  // Required for Linux
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
    clientAffinityEnabled: false  // Disable sticky sessions for stateless apps

    siteConfig: {
      linuxFxVersion: 'NODE|18-lts'
      minTlsVersion: '1.2'
      ftpsState: 'Disabled'
      http20Enabled: true
      alwaysOn: true

      appSettings: [
        {
          name: 'DATABASE_URL'
          value: '@Microsoft.KeyVault(VaultName=mykeyvault;SecretName=db-connection-string)'
        }
        {
          name: 'WEBSITE_RUN_FROM_PACKAGE'
          value: '1'
        }
      ]

      healthCheckPath: '/health'
    }
  }
}

// Deployment slot (staging)
resource stagingSlot 'Microsoft.Web/sites/slots@2023-01-01' = {
  parent: webApp
  name: 'staging'
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'NODE|18-lts'
      appSettings: [
        {
          name: 'ENVIRONMENT'
          value: 'staging'
        }
      ]
    }
  }
}

// Autoscale rule
resource autoscale 'Microsoft.Insights/autoscalesettings@2022-10-01' = {
  name: 'app-autoscale'
  location: location
  properties: {
    targetResourceUri: appServicePlan.id
    enabled: true
    profiles: [
      {
        name: 'Auto scale condition'
        capacity: {
          minimum: '3'
          maximum: '20'
          default: '3'
        }
        rules: [
          {
            metricTrigger: {
              metricName: 'CpuPercentage'
              metricResourceUri: appServicePlan.id
              timeGrain: 'PT1M'
              statistic: 'Average'
              timeWindow: 'PT5M'
              timeAggregation: 'Average'
              operator: 'GreaterThan'
              threshold: 70
            }
            scaleAction: {
              direction: 'Increase'
              type: 'ChangeCount'
              value: '2'
              cooldown: 'PT5M'
            }
          }
          {
            metricTrigger: {
              metricName: 'CpuPercentage'
              metricResourceUri: appServicePlan.id
              timeGrain: 'PT1M'
              statistic: 'Average'
              timeWindow: 'PT5M'
              timeAggregation: 'Average'
              operator: 'LessThan'
              threshold: 30
            }
            scaleAction: {
              direction: 'Decrease'
              type: 'ChangeCount'
              value: '1'
              cooldown: 'PT10M'
            }
          }
        ]
      }
    ]
  }
}
```

---

## Virtual Machines

**Best For:** Legacy applications, specialized software, lift-and-shift migrations

**When to Use VMs:**
- Legacy applications requiring specific OS configurations
- Third-party software with licensing requirements
- Lift-and-shift migrations
- Applications requiring VM-level access

**When to Avoid VMs:**
- PaaS options available (Container Apps, App Service)
- Modern cloud-native applications
- Cost-sensitive workloads (VMs more expensive to operate)

### VM Size Selection

| Series | CPU:RAM Ratio | Use Case | Example Sizes |
|--------|---------------|----------|---------------|
| **B-series** | Burstable | Dev/test, low CPU | B2s, B4ms |
| **D-series** | Balanced (1:4) | General purpose web apps | D4s_v5, D8s_v5 |
| **E-series** | Memory (1:8) | Databases, caching | E4s_v5, E8s_v5 |
| **F-series** | Compute (1:2) | Batch processing, analytics | F4s_v2, F8s_v2 |
| **N-series** | GPU | ML training, rendering | NC6s_v3, ND96asr_v4 |

---

## Cost Comparison

### Approximate Monthly Costs (US East, 24/7 operation, 2025)

| Service | Configuration | Cost/Month | Notes |
|---------|---------------|------------|-------|
| **Container Apps** | 1 vCPU, 2GB RAM | ~$60 | Consumption model, actual usage |
| **Container Apps** | 4 vCPU, 8GB RAM | ~$240 | High-traffic API |
| **AKS** | 3-node D4s_v5 | ~$400 | Plus node costs |
| **Functions** | Premium EP1 (1 vCPU, 3.5GB) | ~$140 | 24/7 premium plan |
| **Functions** | Consumption | ~$20 | 1M executions, 400ms avg |
| **App Service** | P1v3 (2 vCPU, 8GB) | ~$145 | Includes 3 deployment slots |
| **VM** | D4s_v5 (4 vCPU, 16GB) | ~$140 | Plus OS, storage, egress |

### Cost Optimization Strategies

1. **Use Reserved Instances:** 40-60% savings for predictable workloads (VMs, App Service)
2. **Leverage Consumption Pricing:** Functions, Container Apps for variable traffic
3. **Auto-scaling:** Scale down during off-hours
4. **Spot VMs:** Up to 90% savings for fault-tolerant batch workloads
5. **Right-sizing:** Monitor and resize VMs based on actual usage

---

## Summary Decision Matrix

| If You Need... | Choose | Why |
|----------------|--------|-----|
| Kubernetes features | AKS | Full control, CRDs, operators |
| Microservices without K8s | Container Apps | Simpler, cheaper, KEDA built-in |
| Event-driven functions | Functions | Pay per execution, multiple triggers |
| Web app with CI/CD | App Service | Deployment slots, easy GitHub integration |
| Legacy migration | VMs | VM-level access, specialized software |
| Batch processing | Azure Batch or Spot VMs | Cost-effective for fault-tolerant jobs |
