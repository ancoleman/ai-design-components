# Azure Network Security Groups (NSGs) Guide

Azure Network Security Groups provide firewall controls for VMs, subnets, and network interfaces.


## Table of Contents

- [Key Concepts](#key-concepts)
- [NSG Components](#nsg-components)
- [Azure CLI Examples](#azure-cli-examples)
  - [Create NSG](#create-nsg)
  - [List and View NSGs](#list-and-view-nsgs)
- [Terraform Examples](#terraform-examples)
  - [Basic Web Server NSG](#basic-web-server-nsg)
  - [Database NSG (Private)](#database-nsg-private)
  - [Associate NSG with Subnet](#associate-nsg-with-subnet)
  - [Associate NSG with Network Interface](#associate-nsg-with-network-interface)
- [Service Tags](#service-tags)
- [Application Security Groups (ASGs)](#application-security-groups-asgs)
- [Default Security Rules](#default-security-rules)
- [NSG Flow Logs](#nsg-flow-logs)
- [Three-Tier Application Example](#three-tier-application-example)
- [Best Practices](#best-practices)
- [Comparison with AWS/GCP](#comparison-with-awsgcp)
- [Resources](#resources)

## Key Concepts

**NSG Characteristics:**
- **Stateful:** Return traffic automatically allowed
- **Priority-based:** 100-4096 (lower = higher priority)
- **Subnet or NIC level:** Can attach to subnet or network interface
- **Default rules:** Cannot be deleted, lowest priority

## NSG Components

```
Priority: 100-4096 (lower = higher priority)
Name: Descriptive rule name
Port: Port or port range
Protocol: TCP, UDP, ICMP, or Any
Source: IP, Service Tag, or Application Security Group
Destination: IP, Service Tag, or Application Security Group
Action: Allow or Deny
Direction: Inbound or Outbound
```

## Azure CLI Examples

### Create NSG

```bash
# Create NSG
az network nsg create \
    --resource-group myResourceGroup \
    --name web-nsg \
    --location eastus

# Create rule
az network nsg rule create \
    --resource-group myResourceGroup \
    --nsg-name web-nsg \
    --name allow-http \
    --priority 100 \
    --source-address-prefixes '*' \
    --source-port-ranges '*' \
    --destination-address-prefixes '*' \
    --destination-port-ranges 80 \
    --access Allow \
    --protocol Tcp \
    --direction Inbound
```

### List and View NSGs

```bash
# List NSGs
az network nsg list --output table

# Show NSG details
az network nsg show --resource-group myResourceGroup --name web-nsg

# List rules
az network nsg rule list --resource-group myResourceGroup --nsg-name web-nsg --output table
```

## Terraform Examples

### Basic Web Server NSG

```hcl
resource "azurerm_network_security_group" "web" {
  name                = "web-nsg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  # Inbound: Allow HTTP
  security_rule {
    name                       = "allow-http"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # Inbound: Allow HTTPS
  security_rule {
    name                       = "allow-https"
    priority                   = 110
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # Inbound: Allow SSH from office
  security_rule {
    name                       = "allow-ssh-office"
    priority                   = 120
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "203.0.113.0/24"  # Office IP
    destination_address_prefix = "*"
  }

  tags = {
    Environment = "Production"
    Tier        = "Web"
  }
}
```

### Database NSG (Private)

```hcl
resource "azurerm_network_security_group" "database" {
  name                = "database-nsg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  # Inbound: Allow PostgreSQL from app subnet
  security_rule {
    name                       = "allow-postgresql-from-app"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "5432"
    source_address_prefix      = "10.0.2.0/24"  # App subnet
    destination_address_prefix = "*"
  }

  # Deny all other inbound
  security_rule {
    name                       = "deny-all-inbound"
    priority                   = 4000
    direction                  = "Inbound"
    access                     = "Deny"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  tags = {
    Environment = "Production"
    Tier        = "Database"
  }
}
```

### Associate NSG with Subnet

```hcl
resource "azurerm_subnet_network_security_group_association" "web" {
  subnet_id                 = azurerm_subnet.web.id
  network_security_group_id = azurerm_network_security_group.web.id
}
```

### Associate NSG with Network Interface

```hcl
resource "azurerm_network_interface_security_group_association" "web_vm" {
  network_interface_id      = azurerm_network_interface.web_vm.id
  network_security_group_id = azurerm_network_security_group.web.id
}
```

## Service Tags

Azure service tags represent groups of IP addresses:

```hcl
resource "azurerm_network_security_group" "app" {
  name                = "app-nsg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  # Allow to Azure Storage
  security_rule {
    name                       = "allow-storage"
    priority                   = 100
    direction                  = "Outbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "*"
    destination_address_prefix = "Storage"  # Service tag
  }

  # Allow to Azure SQL
  security_rule {
    name                       = "allow-sql"
    priority                   = 110
    direction                  = "Outbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "1433"
    source_address_prefix      = "*"
    destination_address_prefix = "Sql"  # Service tag
  }
}
```

**Common Service Tags:**
- `Internet` - All Internet addresses
- `VirtualNetwork` - All VNet addresses
- `AzureLoadBalancer` - Azure load balancer
- `Storage` - Azure Storage
- `Sql` - Azure SQL Database
- `AzureMonitor` - Azure Monitor

## Application Security Groups (ASGs)

Group VMs logically without IP addresses:

```hcl
# Define ASGs
resource "azurerm_application_security_group" "web" {
  name                = "web-asg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_application_security_group" "app" {
  name                = "app-asg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

# Use ASGs in NSG rules
resource "azurerm_network_security_group" "main" {
  name                = "main-nsg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  security_rule {
    name                                       = "web-to-app"
    priority                                   = 100
    direction                                  = "Inbound"
    access                                     = "Allow"
    protocol                                   = "Tcp"
    source_port_range                          = "*"
    destination_port_range                     = "8080"
    source_application_security_group_ids      = [azurerm_application_security_group.web.id]
    destination_application_security_group_ids = [azurerm_application_security_group.app.id]
  }
}

# Associate VM NIC with ASG
resource "azurerm_network_interface_application_security_group_association" "web_vm" {
  network_interface_id          = azurerm_network_interface.web_vm.id
  application_security_group_id = azurerm_application_security_group.web.id
}
```

## Default Security Rules

Azure creates default rules (cannot be deleted):

**Inbound:**
- Priority 65000: Allow VNet → VNet
- Priority 65001: Allow AzureLoadBalancer → Any
- Priority 65500: Deny All

**Outbound:**
- Priority 65000: Allow VNet → VNet
- Priority 65001: Allow Any → Internet
- Priority 65500: Deny All

Override with custom rules (priority 100-4096).

## NSG Flow Logs

Enable for monitoring:

```hcl
resource "azurerm_network_watcher_flow_log" "nsg" {
  network_watcher_name = azurerm_network_watcher.main.name
  resource_group_name  = azurerm_resource_group.main.name
  name                 = "nsg-flow-log"

  network_security_group_id = azurerm_network_security_group.web.id
  storage_account_id        = azurerm_storage_account.logs.id
  enabled                   = true

  retention_policy {
    enabled = true
    days    = 30
  }

  traffic_analytics {
    enabled               = true
    workspace_id          = azurerm_log_analytics_workspace.main.workspace_id
    workspace_region      = azurerm_log_analytics_workspace.main.location
    workspace_resource_id = azurerm_log_analytics_workspace.main.id
    interval_in_minutes   = 10
  }
}
```

## Three-Tier Application Example

```hcl
# Web Tier NSG
resource "azurerm_network_security_group" "web" {
  name                = "web-tier-nsg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  security_rule {
    name                       = "allow-https"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "Internet"
    destination_address_prefix = "*"
  }

  security_rule {
    name                                       = "allow-to-app"
    priority                                   = 100
    direction                                  = "Outbound"
    access                                     = "Allow"
    protocol                                   = "Tcp"
    source_port_range                          = "*"
    destination_port_range                     = "8080"
    source_application_security_group_ids      = [azurerm_application_security_group.web.id]
    destination_application_security_group_ids = [azurerm_application_security_group.app.id]
  }
}

# App Tier NSG
resource "azurerm_network_security_group" "app" {
  name                = "app-tier-nsg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  security_rule {
    name                                       = "allow-from-web"
    priority                                   = 100
    direction                                  = "Inbound"
    access                                     = "Allow"
    protocol                                   = "Tcp"
    source_port_range                          = "*"
    destination_port_range                     = "8080"
    source_application_security_group_ids      = [azurerm_application_security_group.web.id]
    destination_application_security_group_ids = [azurerm_application_security_group.app.id]
  }

  security_rule {
    name                       = "allow-to-database"
    priority                   = 100
    direction                  = "Outbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "5432"
    source_address_prefix      = "*"
    destination_address_prefix = "10.0.3.0/24"  # Database subnet
  }
}

# Database Tier NSG
resource "azurerm_network_security_group" "database" {
  name                = "database-tier-nsg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  security_rule {
    name                       = "allow-from-app"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "5432"
    source_address_prefix      = "10.0.2.0/24"  # App subnet
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "deny-outbound-internet"
    priority                   = 4000
    direction                  = "Outbound"
    access                     = "Deny"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefix = "Internet"
  }
}
```

## Best Practices

1. **Use Application Security Groups:** Logical grouping, not IP-based
2. **Descriptive Names:** Clear rule names and descriptions
3. **Priority Spacing:** Use 100, 110, 120 for easy insertion
4. **Service Tags:** Use tags instead of hardcoded IPs
5. **Least Privilege:** Only open necessary ports
6. **Flow Logs:** Enable for monitoring and troubleshooting
7. **Infrastructure as Code:** Manage with Terraform
8. **Regular Audits:** Review rules quarterly
9. **Document Rules:** Add descriptions to every rule
10. **Defense-in-Depth:** NSGs on subnet AND NIC

## Comparison with AWS/GCP

| Feature | Azure NSG | AWS Security Groups | GCP Firewall Rules |
|---------|-----------|---------------------|-------------------|
| **Level** | Subnet or NIC | Instance (ENI) | VPC |
| **Priority** | Yes (100-4096) | No | Yes (0-65535) |
| **Deny Rules** | Yes | No | Yes |
| **Stateful** | Yes | Yes | Yes |
| **Service Tags** | Yes | No (Prefix Lists) | Yes |
| **ASGs** | Yes | No | No (Tags) |

## Resources

- Azure NSG Documentation: https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview
- Terraform azurerm_network_security_group: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/network_security_group
