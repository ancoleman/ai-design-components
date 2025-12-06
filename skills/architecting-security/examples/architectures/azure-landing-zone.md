# Azure Landing Zone Security Architecture

## Overview

Azure Landing Zone provides a secure, scalable foundation for enterprise Azure deployments. Organize resources using management groups with governance enforced through Azure Policy and role-based access control (RBAC).

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    TENANT ROOT GROUP                                     │
│                 (Contoso Organization)                                   │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Tenant-Level Policies:                                           │   │
│  │ - Require tags (Environment, Owner, CostCenter)                  │   │
│  │ - Allowed locations (East US 2, West US 2, West Europe)         │   │
│  │ - Require encryption in transit and at rest                      │   │
│  │ - Diagnostic settings for all resources                          │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
           │
           ├────────────────┬──────────────────┬──────────────────┐
           │                │                  │                  │
           ▼                ▼                  ▼                  ▼
    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
    │  Platform   │  │  Landing    │  │ Decommission│  │   Sandbox   │
    │             │  │   Zones     │  │             │  │             │
    └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘
           │                │                │                │
           │                │                │                │
    ┌──────┴───┬───────┐   │         ┌──────┴──────┐        │
    ▼          ▼       ▼   │         ▼             ▼        ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐   ┌────────┐ ┌────────┐
│Identity│ │Manage. │ │Connect.│ │ Corp   │   │Quarant.│ │Sandbox │
│        │ │        │ │        │ │        │   │        │ │Sub     │
│Entra ID│ │Log     │ │Hub VNet│ │ Prod   │   │        │ │        │
│Priv. ID│ │Analytics│ │Firewall│ │ Dev    │   │        │ │Full    │
│        │ │Sentinel│ │VPN/ER  │ │ Test   │   │        │ │Access  │
└────────┘ └────────┘ └────────┘ └────────┘   └────────┘ └────────┘
                           │           │
                           └───────────┴──────────┐
                                                  ▼
                                        ┌──────────────────┐
                                        │  Hub-Spoke VNet  │
                                        │                  │
                                        │ - Azure Firewall │
                                        │ - VPN Gateway    │
                                        │ - Bastion        │
                                        │ - DDoS Protection│
                                        └──────────────────┘
```

## Management Group Hierarchy

### Platform Management Group

Contains shared platform services and centralized operations.

**Identity Subscription:**
- Microsoft Entra ID (Azure AD)
- Entra ID Privileged Identity Management (PIM)
- Entra ID Identity Protection
- Conditional Access policies
- Domain controllers (if hybrid)
- Azure AD Connect (if hybrid)

**Management Subscription:**
- Azure Monitor Log Analytics workspace
- Microsoft Sentinel (SIEM)
- Azure Automation accounts
- Azure Policy compliance dashboard
- Cost Management + Billing
- Azure Backup vaults

**Connectivity Subscription:**
- Hub virtual network
- Azure Firewall / NVA
- VPN Gateway / ExpressRoute
- Azure Bastion
- Network Watcher
- DDoS Protection Plan
- Private DNS zones

**Policies Applied:**

```json
{
  "properties": {
    "displayName": "Platform Security Baseline",
    "policyType": "Custom",
    "mode": "All",
    "parameters": {},
    "policyRule": {
      "if": {
        "allOf": [
          {
            "field": "type",
            "equals": "Microsoft.Network/networkSecurityGroups"
          },
          {
            "count": {
              "field": "Microsoft.Network/networkSecurityGroups/securityRules[*]",
              "where": {
                "allOf": [
                  {
                    "field": "Microsoft.Network/networkSecurityGroups/securityRules[*].access",
                    "equals": "Allow"
                  },
                  {
                    "field": "Microsoft.Network/networkSecurityGroups/securityRules[*].direction",
                    "equals": "Inbound"
                  },
                  {
                    "field": "Microsoft.Network/networkSecurityGroups/securityRules[*].sourceAddressPrefix",
                    "in": ["*", "Internet", "0.0.0.0/0"]
                  }
                ]
              }
            },
            "greater": 0
          }
        ]
      },
      "then": {
        "effect": "deny"
      }
    }
  }
}
```

### Landing Zones Management Group

Contains application workloads organized by environment and compliance requirements.

**Corporate Landing Zone:**
- Production workloads
- On-premises connectivity required
- Spoke VNet peered to hub
- Managed identities enforced
- Private endpoints mandatory

**Online Landing Zone:**
- Internet-facing applications
- Public endpoints allowed
- Web Application Firewall required
- DDoS protection enabled
- Enhanced monitoring

**Policies Applied:**

```json
{
  "properties": {
    "displayName": "Require Private Endpoints for Storage",
    "policyType": "Custom",
    "mode": "Indexed",
    "parameters": {},
    "policyRule": {
      "if": {
        "allOf": [
          {
            "field": "type",
            "equals": "Microsoft.Storage/storageAccounts"
          },
          {
            "field": "Microsoft.Storage/storageAccounts/networkAcls.defaultAction",
            "notEquals": "Deny"
          }
        ]
      },
      "then": {
        "effect": "deny"
      }
    }
  }
}
```

### Decommissioned Management Group

Contains subscriptions being sunset or quarantined.

**Quarantine Subscription:**
- Compromised resource isolation
- All network access blocked
- Forensics tooling only
- Read-only access for security team

**Policies Applied:**

```json
{
  "properties": {
    "displayName": "Deny All Resource Creation",
    "policyType": "Custom",
    "mode": "All",
    "parameters": {},
    "policyRule": {
      "if": {
        "field": "type",
        "notIn": [
          "Microsoft.Security/assessments",
          "Microsoft.Security/complianceResults"
        ]
      },
      "then": {
        "effect": "deny"
      }
    }
  }
}
```

### Sandbox Management Group

Provides innovation space with relaxed policies.

**Sandbox Subscriptions:**
- Full service access
- Cost limits enforced via budgets
- Automatic resource cleanup (30 days)
- No production data allowed
- No connectivity to corporate network

**Policies Applied:**

```json
{
  "properties": {
    "displayName": "Enforce Budget Limits",
    "policyType": "Custom",
    "mode": "All",
    "parameters": {
      "budgetAmount": {
        "type": "Integer",
        "metadata": {
          "displayName": "Monthly Budget",
          "description": "Maximum monthly spend in USD"
        },
        "defaultValue": 1000
      }
    },
    "policyRule": {
      "if": {
        "field": "type",
        "equals": "Microsoft.Resources/subscriptions"
      },
      "then": {
        "effect": "deployIfNotExists",
        "details": {
          "type": "Microsoft.Consumption/budgets",
          "roleDefinitionIds": [
            "/providers/Microsoft.Authorization/roleDefinitions/b24988ac-6180-42a0-ab88-20f7382dd24c"
          ],
          "deployment": {
            "properties": {
              "mode": "incremental",
              "template": {
                "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
                "contentVersion": "1.0.0.0",
                "resources": [
                  {
                    "type": "Microsoft.Consumption/budgets",
                    "apiVersion": "2021-10-01",
                    "name": "SandboxBudget",
                    "properties": {
                      "category": "Cost",
                      "amount": "[parameters('budgetAmount')]",
                      "timeGrain": "Monthly",
                      "timePeriod": {
                        "startDate": "[concat(utcNow('yyyy-MM'), '-01')]"
                      },
                      "notifications": {
                        "Actual_80_Percent": {
                          "enabled": true,
                          "operator": "GreaterThan",
                          "threshold": 80,
                          "contactEmails": ["sandbox-admins@contoso.com"]
                        }
                      }
                    }
                  }
                ]
              }
            }
          }
        }
      }
    }
  }
}
```

## Azure Policy Initiatives

### Security Baseline Initiative

Comprehensive security controls applied at tenant root:

```json
{
  "properties": {
    "displayName": "Contoso Security Baseline",
    "policyType": "Custom",
    "description": "Enforce organization-wide security controls",
    "metadata": {
      "category": "Security"
    },
    "parameters": {},
    "policyDefinitions": [
      {
        "policyDefinitionId": "/providers/Microsoft.Authorization/policyDefinitions/404c3081-a854-4457-ae30-26a93ef643f9",
        "parameters": {}
      },
      {
        "policyDefinitionId": "/providers/Microsoft.Authorization/policyDefinitions/a1181c5f-672a-477a-979a-7d58aa086233",
        "parameters": {}
      },
      {
        "policyDefinitionId": "/providers/Microsoft.Authorization/policyDefinitions/013e242c-8828-4970-87b3-ab247555486d",
        "parameters": {}
      },
      {
        "policyDefinitionId": "/providers/Microsoft.Authorization/policyDefinitions/7d7be79c-23ba-4033-84dd-45e2a5ccdd67",
        "parameters": {}
      },
      {
        "policyDefinitionId": "/providers/Microsoft.Authorization/policyDefinitions/0961003e-5a0a-4549-abde-af6a37f2724d",
        "parameters": {}
      }
    ]
  }
}
```

**Key Policies Included:**

1. **Secure transfer to storage accounts should be enabled** (404c3081)
2. **Audit VMs without managed disks** (a1181c5f)
3. **Deploy Diagnostic Settings for Network Security Groups** (013e242c)
4. **Function apps should only be accessible over HTTPS** (7d7be79c)
5. **Require a tag and its value on resources** (0961003e)

### Compliance Initiative (CIS Benchmark)

```json
{
  "properties": {
    "displayName": "CIS Microsoft Azure Foundations Benchmark v1.4.0",
    "policyType": "BuiltIn",
    "policyDefinitionId": "/providers/Microsoft.Authorization/policySetDefinitions/c3f5c4d9-9a1d-4a99-85c0-7f93e384d5c5",
    "parameters": {
      "effect": {
        "value": "Audit"
      }
    }
  }
}
```

### Custom Network Security Initiative

```json
{
  "properties": {
    "displayName": "Network Security Controls",
    "policyType": "Custom",
    "policyDefinitions": [
      {
        "policyDefinitionId": "/subscriptions/xxx/providers/Microsoft.Authorization/policyDefinitions/deny-public-ip",
        "parameters": {
          "effect": {
            "value": "Deny"
          }
        }
      },
      {
        "policyDefinitionId": "/subscriptions/xxx/providers/Microsoft.Authorization/policyDefinitions/require-nsg-on-subnet",
        "parameters": {
          "effect": {
            "value": "Audit"
          }
        }
      },
      {
        "policyDefinitionId": "/subscriptions/xxx/providers/Microsoft.Authorization/policyDefinitions/allowed-nsg-rules-only",
        "parameters": {
          "allowedPorts": {
            "value": [443, 22]
          }
        }
      }
    ]
  }
}
```

## Hub-Spoke Network Security

### Hub VNet Design

```
┌─────────────────────────────────────────────────────────────┐
│              Hub VNet (10.0.0.0/16)                         │
│                                                              │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │ GatewaySubnet    │  │ AzureFirewall    │                │
│  │ 10.0.0.0/24      │  │ Subnet           │                │
│  │                  │  │ 10.0.1.0/26      │                │
│  │ - VPN Gateway    │  │                  │                │
│  │ - ExpressRoute   │  │ - Firewall       │                │
│  └──────────────────┘  │ - Public IP      │                │
│                        └──────────────────┘                │
│                                                              │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │ AzureBastion     │  │ Management       │                │
│  │ Subnet           │  │ Subnet           │                │
│  │ 10.0.2.0/27      │  │ 10.0.3.0/24      │                │
│  │                  │  │                  │                │
│  │ - Bastion Host   │  │ - Jump Boxes     │                │
│  └──────────────────┘  │ - Monitoring VMs │                │
│                        └──────────────────┘                │
└─────────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
        ▼                                   ▼
┌──────────────────┐              ┌──────────────────┐
│ Spoke VNet 1     │              │ Spoke VNet 2     │
│ (Production)     │              │ (Development)    │
│ 10.1.0.0/16      │              │ 10.2.0.0/16      │
│                  │              │                  │
│ - App Subnet     │              │ - App Subnet     │
│ - Data Subnet    │              │ - Data Subnet    │
│ - Private Endpts │              │ - Private Endpts │
└──────────────────┘              └──────────────────┘
```

### Azure Firewall Configuration

**Network Rules:**

```json
{
  "properties": {
    "ruleCollections": [
      {
        "name": "AllowOutboundHTTPS",
        "priority": 100,
        "action": {
          "type": "Allow"
        },
        "rules": [
          {
            "name": "AllowHTTPS",
            "protocols": ["TCP"],
            "sourceAddresses": ["10.1.0.0/16", "10.2.0.0/16"],
            "destinationAddresses": ["*"],
            "destinationPorts": ["443"]
          }
        ]
      },
      {
        "name": "AllowDNS",
        "priority": 110,
        "action": {
          "type": "Allow"
        },
        "rules": [
          {
            "name": "AllowDNSQueries",
            "protocols": ["UDP"],
            "sourceAddresses": ["10.1.0.0/16", "10.2.0.0/16"],
            "destinationAddresses": ["168.63.129.16"],
            "destinationPorts": ["53"]
          }
        ]
      }
    ]
  }
}
```

**Application Rules:**

```json
{
  "properties": {
    "ruleCollections": [
      {
        "name": "AllowAzureServices",
        "priority": 200,
        "action": {
          "type": "Allow"
        },
        "rules": [
          {
            "name": "AllowAzureMonitor",
            "protocols": [
              {
                "protocolType": "Https",
                "port": 443
              }
            ],
            "targetFqdns": [
              "*.ods.opinsights.azure.com",
              "*.oms.opinsights.azure.com",
              "*.monitoring.azure.com"
            ],
            "sourceAddresses": ["10.1.0.0/16", "10.2.0.0/16"]
          },
          {
            "name": "AllowWindowsUpdate",
            "protocols": [
              {
                "protocolType": "Http",
                "port": 80
              },
              {
                "protocolType": "Https",
                "port": 443
              }
            ],
            "targetFqdns": [
              "*.windowsupdate.microsoft.com",
              "*.update.microsoft.com"
            ],
            "sourceAddresses": ["10.1.0.0/16"]
          }
        ]
      }
    ]
  }
}
```

**Threat Intelligence:**

```json
{
  "properties": {
    "threatIntelMode": "Alert",
    "threatIntelWhitelist": {
      "fqdns": ["trusted-partner.com"],
      "ipAddresses": ["20.30.40.50"]
    }
  }
}
```

### VNet Peering Security

```json
{
  "properties": {
    "allowVirtualNetworkAccess": true,
    "allowForwardedTraffic": true,
    "allowGatewayTransit": true,
    "useRemoteGateways": false,
    "remoteVirtualNetwork": {
      "id": "/subscriptions/xxx/resourceGroups/hub-network-rg/providers/Microsoft.Network/virtualNetworks/hub-vnet"
    }
  }
}
```

## Microsoft Defender for Cloud Integration

### Enable All Defender Plans

```powershell
# Enable Defender for Cloud Standard tier
Set-AzSecurityPricing -Name "VirtualMachines" -PricingTier "Standard"
Set-AzSecurityPricing -Name "SqlServers" -PricingTier "Standard"
Set-AzSecurityPricing -Name "AppServices" -PricingTier "Standard"
Set-AzSecurityPricing -Name "StorageAccounts" -PricingTier "Standard"
Set-AzSecurityPricing -Name "SqlServerVirtualMachines" -PricingTier "Standard"
Set-AzSecurityPricing -Name "KubernetesService" -PricingTier "Standard"
Set-AzSecurityPricing -Name "ContainerRegistry" -PricingTier "Standard"
Set-AzSecurityPricing -Name "KeyVaults" -PricingTier "Standard"
Set-AzSecurityPricing -Name "Dns" -PricingTier "Standard"
Set-AzSecurityPricing -Name "Arm" -PricingTier "Standard"
Set-AzSecurityPricing -Name "OpenSourceRelationalDatabases" -PricingTier "Standard"
Set-AzSecurityPricing -Name "Containers" -PricingTier "Standard"

# Configure auto-provisioning
Set-AzSecurityAutoProvisioningSetting -Name "default" -EnableAutoProvision
```

### Defender for Servers Configuration

```json
{
  "properties": {
    "pricingTier": "Standard",
    "subPlan": "P2",
    "extensions": [
      {
        "name": "MDE",
        "isEnabled": "True"
      },
      {
        "name": "AgentlessVmScanning",
        "isEnabled": "True"
      },
      {
        "name": "FileSensitivity",
        "isEnabled": "True"
      }
    ]
  }
}
```

### Security Alerts Automation

```json
{
  "type": "Microsoft.Security/automations",
  "apiVersion": "2019-01-01-preview",
  "name": "HighSeverityAlertAutomation",
  "location": "eastus2",
  "properties": {
    "description": "Trigger incident response for high severity alerts",
    "isEnabled": true,
    "scopes": [
      {
        "description": "All subscriptions",
        "scopePath": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
      }
    ],
    "sources": [
      {
        "eventSource": "Alerts",
        "ruleSets": [
          {
            "rules": [
              {
                "propertyJPath": "properties.metadata.severity",
                "propertyType": "String",
                "expectedValue": "High",
                "operator": "Equals"
              }
            ]
          }
        ]
      }
    ],
    "actions": [
      {
        "actionType": "LogicApp",
        "logicAppResourceId": "/subscriptions/xxx/resourceGroups/security-automation/providers/Microsoft.Logic/workflows/IncidentResponseWorkflow",
        "uri": "https://prod-xx.eastus2.logic.azure.com:443/workflows/xxx/triggers/manual/paths/invoke"
      }
    ]
  }
}
```

## Microsoft Entra ID Configuration

### Conditional Access Policies

**Require MFA for All Users:**

```json
{
  "displayName": "Require MFA for all users",
  "state": "enabled",
  "conditions": {
    "users": {
      "includeUsers": ["All"],
      "excludeGroups": ["BreakGlassAccounts"]
    },
    "applications": {
      "includeApplications": ["All"]
    },
    "locations": {
      "includeLocations": ["All"]
    }
  },
  "grantControls": {
    "operator": "OR",
    "builtInControls": ["mfa"]
  }
}
```

**Block Legacy Authentication:**

```json
{
  "displayName": "Block legacy authentication",
  "state": "enabled",
  "conditions": {
    "users": {
      "includeUsers": ["All"],
      "excludeGroups": ["LegacyAppExceptions"]
    },
    "applications": {
      "includeApplications": ["All"]
    },
    "clientAppTypes": [
      "exchangeActiveSync",
      "other"
    ]
  },
  "grantControls": {
    "operator": "OR",
    "builtInControls": ["block"]
  }
}
```

**Require Compliant Device for Admins:**

```json
{
  "displayName": "Require compliant device for admins",
  "state": "enabled",
  "conditions": {
    "users": {
      "includeRoles": [
        "62e90394-69f5-4237-9190-012177145e10",
        "194ae4cb-b126-40b2-bd5b-6091b380977d"
      ]
    },
    "applications": {
      "includeApplications": ["All"]
    }
  },
  "grantControls": {
    "operator": "OR",
    "builtInControls": ["compliantDevice", "domainJoinedDevice"]
  }
}
```

### Privileged Identity Management (PIM)

**Role Assignment:**

```json
{
  "properties": {
    "roleDefinitionId": "/subscriptions/xxx/providers/Microsoft.Authorization/roleDefinitions/8e3af657-a8ff-443c-a75c-2fe8c4bcb635",
    "principalId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "requestType": "AdminAssign",
    "scheduleInfo": {
      "startDateTime": "2024-01-01T00:00:00Z",
      "expiration": {
        "type": "AfterDuration",
        "duration": "PT8H"
      }
    },
    "condition": "@Resource[Microsoft.Storage/storageAccounts/blobServices/containers:name] StringEquals 'production-data'",
    "conditionVersion": "2.0"
  }
}
```

**PIM Settings:**

```json
{
  "properties": {
    "userMemberSettings": {
      "permanentEligibleSettings": {
        "approvalRequired": false
      },
      "expiringEligibleSettings": {
        "maximumGrantPeriod": "P365D"
      },
      "permanentActiveSettings": {
        "approvalRequired": true,
        "approvers": [
          {
            "id": "/subscriptions/xxx/resourceGroups/xxx/providers/Microsoft.ManagedIdentity/userAssignedIdentities/pim-approver"
          }
        ]
      },
      "activationSettings": {
        "maximumGrantPeriod": "PT8H",
        "approvalRequired": true,
        "requireMFA": true,
        "requireJustification": true,
        "requireTicketInfo": true
      }
    }
  }
}
```

## Centralized Logging with Microsoft Sentinel

### Log Analytics Workspace Design

```powershell
# Create Log Analytics workspace
New-AzOperationalInsightsWorkspace `
  -ResourceGroupName "security-logging-rg" `
  -Name "contoso-sentinel-workspace" `
  -Location "eastus2" `
  -Sku "PerGB2018" `
  -RetentionInDays 90

# Enable Sentinel
Set-AzSentinelOnboardingState `
  -ResourceGroupName "security-logging-rg" `
  -WorkspaceName "contoso-sentinel-workspace" `
  -CustomerManagedKey $false
```

### Data Connectors

```json
{
  "kind": "AzureActiveDirectory",
  "properties": {
    "tenantId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "dataTypes": {
      "alerts": {
        "state": "enabled"
      }
    }
  }
}
```

```json
{
  "kind": "AzureSecurityCenter",
  "properties": {
    "subscriptionId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "dataTypes": {
      "alerts": {
        "state": "enabled"
      }
    }
  }
}
```

### Analytics Rules

**Suspicious Sign-In Activity:**

```kql
SigninLogs
| where TimeGenerated > ago(1h)
| where ResultType != "0"
| summarize
    FailureCount = count(),
    DistinctIPCount = dcount(IPAddress),
    FirstFailure = min(TimeGenerated),
    LastFailure = max(TimeGenerated)
    by UserPrincipalName, AppDisplayName
| where FailureCount > 10 or DistinctIPCount > 5
| extend
    Severity = iff(FailureCount > 50, "High", "Medium"),
    Description = strcat("User ", UserPrincipalName, " had ", FailureCount, " failed sign-ins")
```

**Anomalous Resource Creation:**

```kql
AzureActivity
| where TimeGenerated > ago(1h)
| where OperationNameValue endswith "write"
| where ActivityStatusValue == "Success"
| summarize
    ResourceCount = count(),
    ResourceTypes = make_set(ResourceType)
    by Caller, CallerIpAddress
| where ResourceCount > 20
| extend
    Severity = "Medium",
    Description = strcat(Caller, " created ", ResourceCount, " resources from ", CallerIpAddress)
```

### Playbooks (Logic Apps)

**Isolation Playbook:**

```json
{
  "definition": {
    "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
    "actions": {
      "Parse_Alert": {
        "type": "ParseJson",
        "inputs": {
          "content": "@triggerBody()?['Entities']",
          "schema": {
            "type": "object",
            "properties": {
              "ResourceId": {"type": "string"}
            }
          }
        }
      },
      "Get_VM_Details": {
        "type": "ApiConnection",
        "inputs": {
          "host": {
            "connection": {
              "name": "@parameters('$connections')['azurevm']['connectionId']"
            }
          },
          "method": "get",
          "path": "/subscriptions/@{encodeURIComponent(variables('subscriptionId'))}/resourceGroups/@{encodeURIComponent(variables('resourceGroup'))}/providers/Microsoft.Compute/virtualMachines/@{encodeURIComponent(variables('vmName'))}"
        },
        "runAfter": {
          "Parse_Alert": ["Succeeded"]
        }
      },
      "Apply_Quarantine_NSG": {
        "type": "ApiConnection",
        "inputs": {
          "host": {
            "connection": {
              "name": "@parameters('$connections')['azurenetworksecuritygroups']['connectionId']"
            }
          },
          "method": "put",
          "path": "/subscriptions/@{encodeURIComponent(variables('subscriptionId'))}/resourceGroups/@{encodeURIComponent(variables('resourceGroup'))}/providers/Microsoft.Network/networkInterfaces/@{encodeURIComponent(variables('nicName'))}",
          "body": {
            "properties": {
              "networkSecurityGroup": {
                "id": "/subscriptions/xxx/resourceGroups/security-rg/providers/Microsoft.Network/networkSecurityGroups/quarantine-nsg"
              }
            }
          }
        },
        "runAfter": {
          "Get_VM_Details": ["Succeeded"]
        }
      },
      "Create_Incident": {
        "type": "ApiConnection",
        "inputs": {
          "host": {
            "connection": {
              "name": "@parameters('$connections')['azuresentinel']['connectionId']"
            }
          },
          "method": "put",
          "path": "/Incidents",
          "body": {
            "properties": {
              "title": "VM Isolated - @{variables('vmName')}",
              "severity": "High",
              "status": "New"
            }
          }
        },
        "runAfter": {
          "Apply_Quarantine_NSG": ["Succeeded"]
        }
      }
    }
  }
}
```

## Diagnostic Settings

### Subscription-Level Diagnostics

```json
{
  "properties": {
    "workspaceId": "/subscriptions/xxx/resourceGroups/security-logging-rg/providers/Microsoft.OperationalInsights/workspaces/contoso-sentinel-workspace",
    "logs": [
      {
        "category": "Administrative",
        "enabled": true
      },
      {
        "category": "Security",
        "enabled": true
      },
      {
        "category": "Alert",
        "enabled": true
      },
      {
        "category": "Policy",
        "enabled": true
      }
    ]
  }
}
```

### Resource-Level Diagnostics (Azure Policy)

```json
{
  "properties": {
    "displayName": "Deploy Diagnostic Settings for Storage Accounts",
    "policyType": "Custom",
    "mode": "Indexed",
    "parameters": {
      "workspaceId": {
        "type": "String",
        "metadata": {
          "displayName": "Log Analytics workspace"
        }
      }
    },
    "policyRule": {
      "if": {
        "field": "type",
        "equals": "Microsoft.Storage/storageAccounts"
      },
      "then": {
        "effect": "deployIfNotExists",
        "details": {
          "type": "Microsoft.Insights/diagnosticSettings",
          "existenceCondition": {
            "allOf": [
              {
                "field": "Microsoft.Insights/diagnosticSettings/logs[*].enabled",
                "equals": "true"
              }
            ]
          },
          "roleDefinitionIds": [
            "/providers/Microsoft.Authorization/roleDefinitions/b24988ac-6180-42a0-ab88-20f7382dd24c"
          ],
          "deployment": {
            "properties": {
              "mode": "incremental",
              "template": {
                "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
                "contentVersion": "1.0.0.0",
                "parameters": {
                  "resourceName": {
                    "type": "string"
                  },
                  "workspaceId": {
                    "type": "string"
                  }
                },
                "resources": [
                  {
                    "type": "Microsoft.Storage/storageAccounts/providers/diagnosticSettings",
                    "apiVersion": "2021-05-01-preview",
                    "name": "[concat(parameters('resourceName'), '/Microsoft.Insights/default')]",
                    "properties": {
                      "workspaceId": "[parameters('workspaceId')]",
                      "metrics": [
                        {
                          "category": "Transaction",
                          "enabled": true
                        }
                      ]
                    }
                  }
                ]
              },
              "parameters": {
                "resourceName": {
                  "value": "[field('name')]"
                },
                "workspaceId": {
                  "value": "[parameters('workspaceId')]"
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## Key Security Metrics

Monitor these metrics across the Azure environment:

1. **Identity Metrics:**
   - Failed sign-in attempts per user
   - MFA coverage percentage
   - Privileged role activations
   - Conditional Access policy effectiveness

2. **Compliance Metrics:**
   - Azure Policy compliance rate
   - Defender for Cloud secure score
   - Non-compliant resources count
   - Security recommendations by severity

3. **Network Metrics:**
   - Azure Firewall threat intel hits
   - DDoS attack attempts
   - NSG rule violations
   - Private endpoint coverage

4. **Detection Metrics:**
   - Sentinel alert volume by severity
   - Mean time to detect (MTTD)
   - Mean time to respond (MTTR)
   - False positive rate

## Implementation Checklist

- [ ] Design management group hierarchy
- [ ] Create platform subscriptions (Identity, Management, Connectivity)
- [ ] Deploy hub virtual network
- [ ] Configure Azure Firewall
- [ ] Create Azure Policy initiatives
- [ ] Assign policies at appropriate scopes
- [ ] Configure Microsoft Entra ID (Azure AD)
- [ ] Deploy Conditional Access policies
- [ ] Enable Privileged Identity Management
- [ ] Deploy Log Analytics workspace
- [ ] Enable Microsoft Sentinel
- [ ] Configure diagnostic settings (subscription and resource)
- [ ] Enable Defender for Cloud on all subscriptions
- [ ] Create landing zone subscriptions
- [ ] Deploy spoke virtual networks
- [ ] Configure VNet peering
- [ ] Create security automation playbooks
- [ ] Establish security monitoring dashboard
- [ ] Configure alert notifications
- [ ] Document deployment procedures
- [ ] Train operations teams

## References

- [Azure Landing Zone Architecture](https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/)
- [Azure Security Benchmark](https://learn.microsoft.com/security/benchmark/azure/)
- [Microsoft Entra ID Best Practices](https://learn.microsoft.com/entra/identity/fundamentals/security-operations-introduction)
- [Microsoft Sentinel Best Practices](https://learn.microsoft.com/azure/sentinel/best-practices)
- [CIS Microsoft Azure Foundations Benchmark](https://www.cisecurity.org/benchmark/azure)
