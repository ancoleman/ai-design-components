/**
 * Azure Container Apps - Complete Production Example
 *
 * This template deploys a production-ready Container Apps environment with:
 * - VNet integration and Private Endpoints
 * - Managed Identity authentication
 * - Key Vault integration
 * - Azure Container Registry
 * - Log Analytics monitoring
 * - Autoscaling rules (HTTP, queue, schedule)
 *
 * Usage:
 *   az deployment group create \
 *     --resource-group my-rg \
 *     --template-file main.bicep \
 *     --parameters environment=production location=eastus
 */

@description('Environment name (dev, staging, production)')
@allowed(['dev', 'staging', 'production'])
param environment string = 'production'

@description('Azure region')
param location string = resourceGroup().location

@description('Container image tag')
param imageTag string = 'latest'

@description('Database connection string (stored in Key Vault)')
@secure()
param dbConnectionString string

// Variables
var baseName = 'myapp-${environment}'
var tags = {
  Environment: environment
  ManagedBy: 'Bicep'
  Application: 'MyApp'
}

// Virtual Network
resource vnet 'Microsoft.Network/virtualNetworks@2023-05-01' = {
  name: '${baseName}-vnet'
  location: location
  tags: tags
  properties: {
    addressSpace: {
      addressPrefixes: ['10.0.0.0/16']
    }
    subnets: [
      {
        name: 'container-apps-subnet'
        properties: {
          addressPrefix: '10.0.0.0/23'
          delegations: [
            {
              name: 'Microsoft.App/environments'
              properties: {
                serviceName: 'Microsoft.App/environments'
              }
            }
          ]
        }
      }
      {
        name: 'private-endpoints-subnet'
        properties: {
          addressPrefix: '10.0.2.0/24'
          privateEndpointNetworkPolicies: 'Disabled'
        }
      }
    ]
  }
}

// Log Analytics Workspace
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: '${baseName}-logs'
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

// Azure Container Registry
resource acr 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: replace('${baseName}acr', '-', '')
  location: location
  tags: tags
  sku: {
    name: 'Premium'  // Required for Private Endpoints
  }
  properties: {
    adminUserEnabled: false
    publicNetworkAccess: 'Disabled'
  }
}

// ACR Private Endpoint
resource acrPrivateEndpoint 'Microsoft.Network/privateEndpoints@2023-05-01' = {
  name: '${baseName}-acr-pe'
  location: location
  tags: tags
  properties: {
    subnet: {
      id: '${vnet.id}/subnets/private-endpoints-subnet'
    }
    privateLinkServiceConnections: [
      {
        name: 'acr-connection'
        properties: {
          privateLinkServiceId: acr.id
          groupIds: ['registry']
        }
      }
    ]
  }
}

// Key Vault
resource keyVault 'Microsoft.KeyVault/vaults@2023-02-01' = {
  name: '${baseName}-kv'
  location: location
  tags: tags
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
    publicNetworkAccess: 'Disabled'
  }
}

// Store database connection string
resource dbConnectionSecret 'Microsoft.KeyVault/vaults/secrets@2023-02-01' = {
  parent: keyVault
  name: 'db-connection-string'
  properties: {
    value: dbConnectionString
  }
}

// Key Vault Private Endpoint
resource kvPrivateEndpoint 'Microsoft.Network/privateEndpoints@2023-05-01' = {
  name: '${baseName}-kv-pe'
  location: location
  tags: tags
  properties: {
    subnet: {
      id: '${vnet.id}/subnets/private-endpoints-subnet'
    }
    privateLinkServiceConnections: [
      {
        name: 'kv-connection'
        properties: {
          privateLinkServiceId: keyVault.id
          groupIds: ['vault']
        }
      }
    ]
  }
}

// Container App Environment
resource containerAppEnvironment 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: '${baseName}-env'
  location: location
  tags: tags
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
    zoneRedundant: environment == 'production'
    vnetConfiguration: {
      infrastructureSubnetId: '${vnet.id}/subnets/container-apps-subnet'
      internal: true
    }
  }
}

// User-Assigned Managed Identity
resource userIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: '${baseName}-identity'
  location: location
  tags: tags
}

// Grant identity AcrPull role on ACR
resource acrPullRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(acr.id, userIdentity.id, 'AcrPull')
  scope: acr
  properties: {
    principalId: userIdentity.properties.principalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')
    principalType: 'ServicePrincipal'
  }
}

// Grant identity Key Vault Secrets User role
resource kvSecretsUserRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyVault.id, userIdentity.id, 'KeyVaultSecretsUser')
  scope: keyVault
  properties: {
    principalId: userIdentity.properties.principalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '4633458b-17de-408a-b874-0445c86b69e6')
    principalType: 'ServicePrincipal'
  }
}

// Container App (API Service)
resource apiContainerApp 'Microsoft.App/containerApps@2024-03-01' = {
  name: '${baseName}-api'
  location: location
  tags: tags
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${userIdentity.id}': {}
    }
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
      }
      secrets: [
        {
          name: 'db-connection-string'
          keyVaultUrl: dbConnectionSecret.properties.secretUri
          identity: userIdentity.id
        }
      ]
      registries: [
        {
          server: acr.properties.loginServer
          identity: userIdentity.id
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'api'
          image: '${acr.properties.loginServer}/api:${imageTag}'
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
              name: 'ENVIRONMENT'
              value: environment
            }
            {
              name: 'LOG_LEVEL'
              value: environment == 'production' ? 'info' : 'debug'
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
              failureThreshold: 3
            }
            {
              type: 'Readiness'
              httpGet: {
                path: '/ready'
                port: 8080
              }
              initialDelaySeconds: 5
              periodSeconds: 5
              failureThreshold: 3
            }
          ]
        }
      ]
      scale: {
        minReplicas: environment == 'production' ? 3 : 1
        maxReplicas: environment == 'production' ? 50 : 10
        rules: [
          {
            name: 'http-scaling-rule'
            http: {
              metadata: {
                concurrentRequests: '100'
              }
            }
          }
          {
            name: 'business-hours-rule'
            custom: {
              type: 'cron'
              metadata: {
                timezone: 'America/New_York'
                start: '0 8 * * MON-FRI'
                end: '0 18 * * MON-FRI'
                desiredReplicas: environment == 'production' ? '20' : '5'
              }
            }
          }
        ]
      }
    }
  }
  dependsOn: [
    acrPullRole
    kvSecretsUserRole
  ]
}

// Outputs
output containerAppUrl string = 'https://${apiContainerApp.properties.configuration.ingress.fqdn}'
output containerRegistryLoginServer string = acr.properties.loginServer
output keyVaultName string = keyVault.name
output logAnalyticsWorkspaceId string = logAnalytics.id
