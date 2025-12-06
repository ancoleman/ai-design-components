# Azure Well-Architected Framework Implementation

Implementation guide for the five pillars of Azure Well-Architected Framework.

## Table of Contents

1. [Cost Optimization](#cost-optimization)
2. [Operational Excellence](#operational-excellence)
3. [Performance Efficiency](#performance-efficiency)
4. [Reliability](#reliability)
5. [Security](#security)

---

## Cost Optimization

**Maximize value delivered within budget constraints**

### Reserved Instances Strategy

```
Workload Analysis
  ↓
Steady-state (24/7, 1-3 years)? → Reserved Instances (40-60% savings)
  ↓
Variable traffic? → Consumption pricing (Functions, Container Apps)
  ↓
Fault-tolerant batch? → Spot VMs (up to 90% savings)
```

### Implementation Patterns

**1. Storage Lifecycle Management**

```bicep
resource lifecyclePolicy 'Microsoft.Storage/storageAccounts/managementPolicies@2023-01-01' = {
  parent: storageAccount
  name: 'default'
  properties: {
    policy: {
      rules: [
        {
          name: 'move-to-lower-tiers'
          enabled: true
          type: 'Lifecycle'
          definition: {
            filters: {
              blobTypes: ['blockBlob']
              prefixMatch: ['logs/']
            }
            actions: {
              baseBlob: {
                tierToCool: {
                  daysAfterModificationGreaterThan: 30
                }
                tierToCold: {
                  daysAfterModificationGreaterThan: 90
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

**Savings:** Hot ($0.018/GB) → Cool ($0.010/GB) → Archive ($0.00099/GB) = 94% reduction

**2. Auto-Shutdown for Dev/Test Resources**

```bicep
resource vmAutoshutdown 'Microsoft.DevTestLab/schedules@2018-09-15' = {
  name: 'shutdown-computevm-${vm.name}'
  location: location
  properties: {
    status: 'Enabled'
    taskType: 'ComputeVmShutdownTask'
    dailyRecurrence: {
      time: '1900'  // 7 PM
    }
    timeZoneId: 'Eastern Standard Time'
    notificationSettings: {
      status: 'Enabled'
      timeInMinutes: 30
      emailRecipient: 'devteam@example.com'
    }
    targetResourceId: vm.id
  }
}
```

**Savings:** ~65% for dev/test resources (off 18 hours/day + weekends)

**3. Cost Budgets and Alerts**

```bicep
resource budget 'Microsoft.Consumption/budgets@2023-11-01' = {
  name: 'monthly-budget'
  properties: {
    category: 'Cost'
    amount: 10000  // $10,000 per month
    timeGrain: 'Monthly'
    timePeriod: {
      startDate: '2025-01-01'
    }
    notifications: {
      warning80: {
        enabled: true
        operator: 'GreaterThan'
        threshold: 80
        contactEmails: [
          'finance@example.com'
          'engineering@example.com'
        ]
      }
      critical100: {
        enabled: true
        operator: 'GreaterThan'
        threshold: 100
        contactEmails: [
          'finance@example.com'
        ]
      }
    }
  }
}
```

### Cost Optimization Checklist

- [ ] Tag all resources (Environment, Owner, CostCenter)
- [ ] Purchase Reserved Instances for predictable workloads
- [ ] Enable auto-scaling (scale down during off-hours)
- [ ] Use Spot VMs for fault-tolerant batch jobs
- [ ] Implement storage lifecycle policies
- [ ] Right-size VMs (review Azure Advisor recommendations)
- [ ] Delete unused resources (unattached disks, orphaned IPs)
- [ ] Set budgets and cost alerts
- [ ] Review monthly cost reports

---

## Operational Excellence

**Run reliable, manageable systems at scale**

### Azure Policy for Governance

**Common Policy Patterns:**

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

// Enforce allowed Azure regions
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
          in: ['eastus', 'eastus2', 'westus2', 'centralus']
        }
      }
      then: {
        effect: 'deny'
      }
    }
  }
}

// Enforce TLS 1.2 minimum
resource enforceTlsPolicy 'Microsoft.Authorization/policyDefinitions@2021-06-01' = {
  name: 'enforce-tls-policy'
  properties: {
    policyType: 'Custom'
    mode: 'All'
    displayName: 'Enforce TLS 1.2 minimum for storage accounts'
    policyRule: {
      if: {
        allOf: [
          { field: 'type', equals: 'Microsoft.Storage/storageAccounts' }
          {
            field: 'Microsoft.Storage/storageAccounts/minimumTlsVersion'
            notEquals: 'TLS1_2'
          }
        ]
      }
      then: {
        effect: 'deny'
      }
    }
  }
}
```

### Azure Blueprints for Repeatable Environments

**Blueprint Components:**
- Resource Groups
- Policy Assignments
- Role Assignments
- ARM Templates (Bicep)

**Use Case:** Deploy compliant production environments in minutes

### Infrastructure as Code Best Practices

**Bicep Organization:**
```
infrastructure/
├── main.bicep                 # Entry point
├── parameters/
│   ├── dev.json
│   ├── staging.json
│   └── production.json
├── modules/
│   ├── networking.bicep       # VNets, NSGs, Private Endpoints
│   ├── compute.bicep          # Container Apps, AKS, VMs
│   ├── data.bicep             # Databases, storage
│   └── monitoring.bicep       # Log Analytics, App Insights
└── policies/
    └── governance.bicep       # Azure Policy definitions
```

**Deployment:**
```bash
az deployment sub create \
  --location eastus \
  --template-file main.bicep \
  --parameters parameters/production.json
```

---

## Performance Efficiency

**Scale to meet demand efficiently**

### Autoscaling Patterns

**Container Apps Multi-Rule Scaling:**

```bicep
scale: {
  minReplicas: 2
  maxReplicas: 50
  rules: [
    // HTTP concurrency
    {
      name: 'http-rule'
      http: {
        metadata: {
          concurrentRequests: '100'
        }
      }
    }
    // Queue depth
    {
      name: 'queue-rule'
      custom: {
        type: 'azure-servicebus'
        metadata: {
          queueName: 'orders'
          messageCount: '10'
        }
      }
    }
    // Business hours boost
    {
      name: 'business-hours'
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
```

### Caching Strategy

**Azure Cache for Redis:**

```bicep
resource redis 'Microsoft.Cache/redis@2023-08-01' = {
  name: 'mycache'
  location: location
  properties: {
    sku: {
      name: 'Premium'  // Basic, Standard, Premium
      family: 'P'
      capacity: 1
    }
    enableNonSslPort: false
    minimumTlsVersion: '1.2'
    redisConfiguration: {
      'maxmemory-policy': 'allkeys-lru'
    }
    publicNetworkAccess: 'Disabled'  // Use Private Endpoint
  }
}
```

**Cache Patterns:**
- **Cache-Aside:** Application manages cache (most common)
- **Read-Through:** Cache fetches from database automatically
- **Write-Behind:** Cache writes to database asynchronously

### CDN for Static Content

```bicep
resource cdn 'Microsoft.Cdn/profiles@2023-05-01' = {
  name: 'mycdn'
  location: 'global'
  sku: {
    name: 'Standard_Microsoft'  // or Premium_Verizon, Premium_Akamai
  }
}

resource endpoint 'Microsoft.Cdn/profiles/endpoints@2023-05-01' = {
  parent: cdn
  name: 'static-assets'
  location: 'global'
  properties: {
    originHostHeader: 'mystorageaccount.blob.core.windows.net'
    isHttpAllowed: false
    isHttpsAllowed: true
    origins: [
      {
        name: 'storage-origin'
        properties: {
          hostName: 'mystorageaccount.blob.core.windows.net'
        }
      }
    ]
  }
}
```

---

## Reliability

**Recover from failures and meet availability commitments**

### Availability Zones

**Zone-Redundant Deployment:**

```bicep
// VM Scale Set across 3 zones
resource vmss 'Microsoft.Compute/virtualMachineScaleSets@2023-09-01' = {
  name: 'app-vmss'
  location: location
  zones: ['1', '2', '3']
  sku: {
    name: 'Standard_D4s_v5'
    capacity: 6  // 2 per zone
  }
  properties: {
    zoneBalance: true
    platformFaultDomainCount: 1
    singlePlacementGroup: false
  }
}

// Zone-redundant storage
resource storage 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'mystorageaccount'
  location: location
  sku: {
    name: 'Standard_ZRS'  // Zone-Redundant Storage
  }
  kind: 'StorageV2'
}
```

**Availability SLAs:**
- Single VM (Premium SSD): 99.9%
- Availability Set: 99.95%
- Availability Zones: 99.99%

### Multi-Region Architecture

**Traffic Manager for Global Routing:**

```bicep
resource trafficManager 'Microsoft.Network/trafficmanagerprofiles@2022-04-01' = {
  name: 'myapp-traffic-manager'
  location: 'global'
  properties: {
    profileStatus: 'Enabled'
    trafficRoutingMethod: 'Performance'  // or Priority, Weighted, Geographic
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
          priority: 2
        }
      }
    ]
  }
}
```

### Backup and Disaster Recovery

**Azure Backup for VMs:**

```bicep
resource recoveryVault 'Microsoft.RecoveryServices/vaults@2023-01-01' = {
  name: 'backup-vault'
  location: location
  sku: {
    name: 'RS0'
    tier: 'Standard'
  }
  properties: {}
}

resource backupPolicy 'Microsoft.RecoveryServices/vaults/backupPolicies@2023-01-01' = {
  parent: recoveryVault
  name: 'daily-backup'
  properties: {
    backupManagementType: 'AzureIaasVM'
    schedulePolicy: {
      schedulePolicyType: 'SimpleSchedulePolicy'
      scheduleRunFrequency: 'Daily'
      scheduleRunTimes: ['2025-01-01T02:00:00Z']
    }
    retentionPolicy: {
      retentionPolicyType: 'LongTermRetentionPolicy'
      dailySchedule: {
        retentionTimes: ['2025-01-01T02:00:00Z']
        retentionDuration: {
          count: 30
          durationType: 'Days'
        }
      }
    }
  }
}
```

**RPO/RTO Targets:**
- **RPO (Recovery Point Objective):** How much data loss acceptable (e.g., 1 hour)
- **RTO (Recovery Time Objective):** How long to restore (e.g., 4 hours)

---

## Security

**Protect data, systems, and assets**

### Managed Identity Pattern

**System-Assigned Identity:**

```bicep
resource containerApp 'Microsoft.App/containerApps@2024-03-01' = {
  name: 'api-service'
  identity: {
    type: 'SystemAssigned'
  }
  // ...
}

// Grant access to Key Vault
resource keyVaultAccessPolicy 'Microsoft.KeyVault/vaults/accessPolicies@2023-02-01' = {
  parent: keyVault
  name: 'add'
  properties: {
    accessPolicies: [
      {
        tenantId: subscription().tenantId
        objectId: containerApp.identity.principalId
        permissions: {
          secrets: ['get', 'list']
        }
      }
    ]
  }
}
```

### Private Endpoints

**Isolate PaaS Services in VNet:**

```bicep
// Storage Account with Private Endpoint
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'mystorageaccount'
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  properties: {
    publicNetworkAccess: 'Disabled'
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
  }
}

resource privateEndpoint 'Microsoft.Network/privateEndpoints@2023-05-01' = {
  name: 'storage-pe'
  location: location
  properties: {
    subnet: {
      id: subnet.id
    }
    privateLinkServiceConnections: [
      {
        name: 'storage-connection'
        properties: {
          privateLinkServiceId: storageAccount.id
          groupIds: ['blob']
        }
      }
    ]
  }
}

// Private DNS Zone
resource privateDnsZone 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: 'privatelink.blob.core.windows.net'
  location: 'global'
}

resource dnsZoneLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = {
  parent: privateDnsZone
  name: 'vnet-link'
  location: 'global'
  properties: {
    virtualNetwork: {
      id: vnet.id
    }
    registrationEnabled: false
  }
}
```

### Microsoft Defender for Cloud

**Enable for All Resource Types:**

```bicep
resource defenderPlan 'Microsoft.Security/pricings@2023-01-01' = {
  name: 'VirtualMachines'
  properties: {
    pricingTier: 'Standard'
  }
}

resource defenderContainers 'Microsoft.Security/pricings@2023-01-01' = {
  name: 'Containers'
  properties: {
    pricingTier: 'Standard'
  }
}

resource defenderDatabases 'Microsoft.Security/pricings@2023-01-01' = {
  name: 'SqlServers'
  properties: {
    pricingTier: 'Standard'
  }
}
```

**Features:**
- Vulnerability scanning
- Just-In-Time VM access
- Adaptive application controls
- Security alerts and recommendations

### Network Security Groups

**Micro-Segmentation:**

```bicep
resource nsg 'Microsoft.Network/networkSecurityGroups@2023-05-01' = {
  name: 'app-subnet-nsg'
  location: location
  properties: {
    securityRules: [
      {
        name: 'allow-https'
        properties: {
          priority: 100
          direction: 'Inbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourceAddressPrefix: '*'
          sourcePortRange: '*'
          destinationAddressPrefix: '*'
          destinationPortRange: '443'
        }
      }
      {
        name: 'deny-all-inbound'
        properties: {
          priority: 4096
          direction: 'Inbound'
          access: 'Deny'
          protocol: '*'
          sourceAddressPrefix: '*'
          sourcePortRange: '*'
          destinationAddressPrefix: '*'
          destinationPortRange: '*'
        }
      }
    ]
  }
}
```

---

## Pillar Implementation Checklist

### Cost Optimization
- [ ] Tag all resources
- [ ] Purchase Reserved Instances
- [ ] Implement lifecycle policies
- [ ] Set budgets and alerts
- [ ] Right-size resources

### Operational Excellence
- [ ] Deploy Azure Policy
- [ ] Use Infrastructure as Code
- [ ] Implement CI/CD
- [ ] Enable diagnostics logging
- [ ] Document runbooks

### Performance Efficiency
- [ ] Configure autoscaling
- [ ] Implement caching
- [ ] Use CDN for static content
- [ ] Monitor performance metrics
- [ ] Conduct load testing

### Reliability
- [ ] Deploy across Availability Zones
- [ ] Implement health checks
- [ ] Configure backup policies
- [ ] Test disaster recovery
- [ ] Define SLAs

### Security
- [ ] Enable Managed Identity
- [ ] Use Private Endpoints
- [ ] Enable Microsoft Defender
- [ ] Implement RBAC
- [ ] Encrypt data at rest and in transit

---

**Use Azure Advisor for personalized recommendations across all five pillars.**
