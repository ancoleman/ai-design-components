# Azure Tag Enforcement Example
#
# Demonstrates Azure Policy for tag enforcement and inheritance
#
# Dependencies:
#   terraform >= 1.0
#   azurerm provider >= 3.0
#
# Usage:
#   terraform init
#   terraform plan
#   terraform apply

terraform {
  required_version = ">= 1.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

variable "subscription_id" {
  type        = string
  description = "Azure subscription ID"
}

variable "environment" {
  type = string
}

variable "owner" {
  type = string
}

variable "cost_center" {
  type = string
}

variable "project" {
  type = string
}

# Resource group with standard tags
resource "azurerm_resource_group" "main" {
  name     = "${var.project}-${var.environment}-rg"
  location = "East US"

  tags = {
    Environment = var.environment
    Owner       = var.owner
    CostCenter  = var.cost_center
    Project     = var.project
    ManagedBy   = "terraform"
  }
}

# Azure Policy: Require tags on resources
resource "azurerm_policy_definition" "require_tags" {
  name         = "require-standard-tags"
  policy_type  = "Custom"
  mode         = "Indexed"
  display_name = "Require standard tags on all resources"
  description  = "Deny resource creation without required tags"

  policy_rule = jsonencode({
    if = {
      anyOf = [
        {
          field  = "tags['Environment']"
          exists = "false"
        },
        {
          field  = "tags['Owner']"
          exists = "false"
        },
        {
          field  = "tags['CostCenter']"
          exists = "false"
        },
        {
          field  = "tags['Project']"
          exists = "false"
        }
      ]
    }
    then = {
      effect = "deny"
    }
  })
}

resource "azurerm_policy_assignment" "require_tags" {
  name                 = "require-standard-tags"
  policy_definition_id = azurerm_policy_definition.require_tags.id
  scope                = "/subscriptions/${var.subscription_id}"
}

# Azure Policy: Inherit tags from resource group
resource "azurerm_policy_definition" "inherit_tags" {
  name         = "inherit-tags-from-rg"
  policy_type  = "Custom"
  mode         = "Indexed"
  display_name = "Inherit tags from resource group"

  policy_rule = jsonencode({
    if = {
      allOf = [
        {
          field  = "[concat('tags[', parameters('tagName'), ']')]"
          exists = "false"
        },
        {
          value    = "[resourceGroup().tags[parameters('tagName')]]"
          notEquals = ""
        }
      ]
    }
    then = {
      effect = "modify"
      details = {
        roleDefinitionIds = [
          "/providers/microsoft.authorization/roleDefinitions/b24988ac-6180-42a0-ab88-20f7382dd24c"
        ]
        operations = [
          {
            operation = "add"
            field     = "[concat('tags[', parameters('tagName'), ']')]"
            value     = "[resourceGroup().tags[parameters('tagName')]]"
          }
        ]
      }
    }
  })

  parameters = jsonencode({
    tagName = {
      type = "String"
      metadata = {
        displayName = "Tag Name"
        description = "Name of the tag to inherit from resource group"
      }
    }
  })
}

# Assign policy to inherit Environment tag
resource "azurerm_policy_assignment" "inherit_environment" {
  name                 = "inherit-environment-tag"
  policy_definition_id = azurerm_policy_definition.inherit_tags.id
  scope                = "/subscriptions/${var.subscription_id}"

  identity {
    type = "SystemAssigned"
  }

  parameters = jsonencode({
    tagName = { value = "Environment" }
  })
}

# Assign policy to inherit Owner tag
resource "azurerm_policy_assignment" "inherit_owner" {
  name                 = "inherit-owner-tag"
  policy_definition_id = azurerm_policy_definition.inherit_tags.id
  scope                = "/subscriptions/${var.subscription_id}"

  identity {
    type = "SystemAssigned"
  }

  parameters = jsonencode({
    tagName = { value = "Owner" }
  })
}

# Example: Virtual machine with tags
resource "azurerm_virtual_machine" "app_server" {
  name                = "${var.environment}-app-server"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  vm_size             = "Standard_B2s"

  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  storage_os_disk {
    name              = "${var.environment}-app-os-disk"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }

  os_profile {
    computer_name  = "appserver"
    admin_username = "adminuser"
    admin_password = "P@ssw0rd1234!"
  }

  os_profile_linux_config {
    disable_password_authentication = false
  }

  # Resource-specific tags (merged with inherited tags from resource group)
  tags = {
    Name      = "${var.environment}-app-server"
    Component = "web"
    Backup    = "daily"
  }
}

# Outputs
output "resource_group_tags" {
  description = "Resource group tags that will be inherited"
  value       = azurerm_resource_group.main.tags
}

output "policy_assignment_ids" {
  description = "Policy assignment IDs"
  value = {
    require_tags        = azurerm_policy_assignment.require_tags.id
    inherit_environment = azurerm_policy_assignment.inherit_environment.id
    inherit_owner       = azurerm_policy_assignment.inherit_owner.id
  }
}
