# Tag Enforcement Patterns

Complete guide to enforcing cloud resource tagging across AWS, Azure, GCP, and Kubernetes using native policy engines.

## Table of Contents

1. [Enforcement Strategy Overview](#enforcement-strategy-overview)
2. [AWS Tag Enforcement](#aws-tag-enforcement)
3. [Azure Tag Enforcement](#azure-tag-enforcement)
4. [GCP Label Enforcement](#gcp-label-enforcement)
5. [Kubernetes Label Enforcement](#kubernetes-label-enforcement)
6. [Multi-Cloud Enforcement](#multi-cloud-enforcement)
7. [Pre-Deployment Validation](#pre-deployment-validation)

---

## Enforcement Strategy Overview

Three enforcement levels determine how strictly tagging policies are applied:

```
┌────────────────────────────────────────────────────────┐
│           Tag Enforcement Hierarchy                    │
├────────────────────────────────────────────────────────┤
│                                                         │
│  1. HARD ENFORCEMENT (Deny Creation)                   │
│     ├── Cost allocation tags (Owner, CostCenter)       │
│     ├── Lifecycle tags (Environment, ManagedBy)        │
│     └── Identification (Name)                          │
│     → Block resource creation if tags missing          │
│                                                         │
│  2. SOFT ENFORCEMENT (Alert Only)                      │
│     ├── Operational tags (Backup, Monitoring)          │
│     ├── Security tags (Compliance, DataClassification) │
│     └── Support tags (SLA, ChangeManagement)           │
│     → Allow creation, send notification to owner       │
│                                                         │
│  3. NO ENFORCEMENT (Best Effort)                       │
│     ├── Custom tags (Application, Component)           │
│     └── Experimental tags                              │
│     → No validation or alerts                          │
│                                                         │
└────────────────────────────────────────────────────────┘
```

**Recommendation**: Start with soft enforcement (alerts only), transition to hard enforcement after 30-90 days of compliance tracking.

---

## AWS Tag Enforcement

AWS provides three enforcement mechanisms: AWS Config Rules, Tag Policies, and Service Control Policies (SCPs).

### Pattern 1: AWS Config Rules (Reactive Enforcement)

Check tag compliance after resource creation and trigger remediation.

**Use case**: Alert when required tags are missing, optionally auto-remediate

#### Terraform Implementation

```hcl
# Enable AWS Config (prerequisite)
resource "aws_config_configuration_recorder" "main" {
  name     = "tag-compliance-recorder"
  role_arn = aws_iam_role.config_role.arn

  recording_group {
    all_supported                 = true
    include_global_resource_types = true
  }
}

resource "aws_config_delivery_channel" "main" {
  name           = "tag-compliance-channel"
  s3_bucket_name = aws_s3_bucket.config_logs.id
  depends_on     = [aws_config_configuration_recorder.main]
}

resource "aws_config_configuration_recorder_status" "main" {
  name       = aws_config_configuration_recorder.main.name
  is_enabled = true
  depends_on = [aws_config_delivery_channel.main]
}

# Required tags Config rule
resource "aws_config_config_rule" "required_tags" {
  name = "required-tags-check"

  source {
    owner             = "AWS"
    source_identifier = "REQUIRED_TAGS"
  }

  input_parameters = jsonencode({
    tag1Key = "Environment"
    tag2Key = "Owner"
    tag3Key = "CostCenter"
    tag4Key = "Project"
    tag5Key = "ManagedBy"
    tag6Key = "Name"
  })

  scope {
    compliance_resource_types = [
      "AWS::EC2::Instance",
      "AWS::RDS::DBInstance",
      "AWS::S3::Bucket",
      "AWS::Lambda::Function",
      "AWS::DynamoDB::Table",
      "AWS::ECS::Service",
    ]
  }

  depends_on = [aws_config_configuration_recorder.main]
}

# SNS topic for compliance alerts
resource "aws_sns_topic" "compliance_alerts" {
  name = "tag-compliance-alerts"
}

resource "aws_sns_topic_subscription" "compliance_email" {
  topic_arn = aws_sns_topic.compliance_alerts.arn
  protocol  = "email"
  endpoint  = "finops-team@company.com"
}

# EventBridge rule to notify on non-compliance
resource "aws_cloudwatch_event_rule" "config_non_compliant" {
  name        = "tag-compliance-violations"
  description = "Trigger when resources are non-compliant with tag policies"

  event_pattern = jsonencode({
    source      = ["aws.config"]
    detail-type = ["Config Rules Compliance Change"]
    detail = {
      configRuleName = [aws_config_config_rule.required_tags.name]
      newEvaluationResult = {
        complianceType = ["NON_COMPLIANT"]
      }
    }
  })
}

resource "aws_cloudwatch_event_target" "sns" {
  rule      = aws_cloudwatch_event_rule.config_non_compliant.name
  target_id = "SendToSNS"
  arn       = aws_sns_topic.compliance_alerts.arn
}

# Auto-remediation (optional): Add missing tags via Systems Manager
resource "aws_config_remediation_configuration" "add_default_tags" {
  config_rule_name = aws_config_config_rule.required_tags.name
  resource_type    = "AWS::EC2::Instance"

  target_type      = "SSM_DOCUMENT"
  target_identifier = aws_ssm_document.add_tags.name
  target_version   = "1"

  parameter {
    name         = "InstanceId"
    resource_value = "RESOURCE_ID"
  }

  parameter {
    name         = "Tags"
    static_value = jsonencode({
      ManagedBy = "terraform"
      Owner     = "unknown@company.com"
    })
  }

  automatic                  = true
  maximum_automatic_attempts = 5
  retry_attempt_seconds      = 60
}

resource "aws_ssm_document" "add_tags" {
  name          = "AddRequiredTags"
  document_type = "Automation"
  content = jsonencode({
    schemaVersion = "0.3"
    description   = "Add required tags to EC2 instances"
    parameters = {
      InstanceId = {
        type = "String"
      }
      Tags = {
        type = "String"
      }
    }
    mainSteps = [{
      name   = "addTags"
      action = "aws:createTags"
      inputs = {
        ResourceType = "EC2"
        ResourceIds  = ["{{ InstanceId }}"]
        Tags         = "{{ Tags }}"
      }
    }]
  })
}
```

**Cost**: AWS Config charges $0.003 per configuration item recorded + $0.001 per rule evaluation

---

### Pattern 2: AWS Tag Policies (Preventive Enforcement)

Enforce tags at AWS Organizations level (preventive, not reactive).

**Use case**: Define allowed tag keys and values across entire AWS Organization

#### Tag Policy JSON

```json
{
  "tags": {
    "Environment": {
      "tag_key": {
        "@@assign": "Environment",
        "@@operators_allowed_for_child_policies": ["@@none"]
      },
      "tag_value": {
        "@@assign": ["prod", "staging", "dev", "test"]
      },
      "enforced_for": {
        "@@assign": [
          "ec2:instance",
          "rds:db",
          "s3:bucket",
          "lambda:function"
        ]
      }
    },
    "Owner": {
      "tag_key": {
        "@@assign": "Owner"
      },
      "tag_value": {
        "@@assign": ["*@company.com"]
      },
      "enforced_for": {
        "@@assign": ["*"]
      }
    },
    "CostCenter": {
      "tag_key": {
        "@@assign": "CostCenter"
      },
      "tag_value": {
        "@@assign": ["CC-*"]
      },
      "enforced_for": {
        "@@assign": ["*"]
      }
    }
  }
}
```

#### Terraform Deployment

```hcl
resource "aws_organizations_policy" "tag_policy" {
  name        = "enforce-required-tags"
  description = "Enforce required tags on all resources"
  type        = "TAG_POLICY"

  content = file("${path.module}/policies/tag-policy.json")
}

resource "aws_organizations_policy_attachment" "tag_policy_root" {
  policy_id = aws_organizations_policy.tag_policy.id
  target_id = data.aws_organizations_organization.current.roots[0].id
}
```

**Limitations**: Tag policies provide case-sensitivity enforcement and value constraints, but do NOT block resource creation if tags are missing (use SCPs for that).

---

### Pattern 3: Service Control Policies (Hard Deny)

Block resource creation if required tags are missing.

**Use case**: Prevent untagged resources at creation time (hard enforcement)

#### SCP JSON

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyEC2WithoutRequiredTags",
      "Effect": "Deny",
      "Action": [
        "ec2:RunInstances"
      ],
      "Resource": [
        "arn:aws:ec2:*:*:instance/*"
      ],
      "Condition": {
        "StringNotLike": {
          "aws:RequestTag/Environment": ["prod", "staging", "dev", "test"],
          "aws:RequestTag/Owner": "*@company.com",
          "aws:RequestTag/CostCenter": "CC-*",
          "aws:RequestTag/Project": "*",
          "aws:RequestTag/ManagedBy": "*"
        }
      }
    },
    {
      "Sid": "DenyS3WithoutRequiredTags",
      "Effect": "Deny",
      "Action": [
        "s3:CreateBucket"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotLike": {
          "aws:RequestTag/Environment": ["prod", "staging", "dev"],
          "aws:RequestTag/Owner": "*@company.com"
        }
      }
    }
  ]
}
```

#### Terraform Deployment

```hcl
resource "aws_organizations_policy" "deny_untagged" {
  name        = "deny-untagged-resources"
  description = "Deny resource creation without required tags"
  type        = "SERVICE_CONTROL_POLICY"

  content = file("${path.module}/policies/scp-deny-untagged.json")
}

resource "aws_organizations_policy_attachment" "scp_attach" {
  policy_id = aws_organizations_policy.deny_untagged.id
  target_id = data.aws_organizations_organization.current.roots[0].id
}
```

**Warning**: SCPs are powerful (can lock out root user). Test in sandbox account first.

---

### Pattern 4: CloudFormation StackSets with Tag Propagation

Apply tags to all resources in a CloudFormation stack automatically.

**Use case**: Consistent tagging across multi-account deployments

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Example stack with tag propagation'

Parameters:
  Environment:
    Type: String
    AllowedValues: [prod, staging, dev]
    Default: dev
  Owner:
    Type: String
    Default: platform-team@company.com
  CostCenter:
    Type: String
    AllowedPattern: 'CC-[0-9]{4}'
  Project:
    Type: String

# Apply these tags to ALL resources in this stack
Tags:
  - Key: Environment
    Value: !Ref Environment
  - Key: Owner
    Value: !Ref Owner
  - Key: CostCenter
    Value: !Ref CostCenter
  - Key: Project
    Value: !Ref Project
  - Key: ManagedBy
    Value: cloudformation
  - Key: StackId
    Value: !Ref AWS::StackId
  - Key: StackName
    Value: !Ref AWS::StackName

Resources:
  AppInstance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: !Ref LatestAmiId
      InstanceType: t3.medium
      # Tags inherited from stack-level tags automatically
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-${Project}-app'
        - Key: Component
          Value: web
```

---

## Azure Tag Enforcement

Azure Policy provides tag enforcement, inheritance, and auto-remediation.

### Pattern 1: Require Tags (Hard Enforcement)

Deny resource creation if required tags are missing.

#### Azure Policy Definition (JSON)

```json
{
  "mode": "Indexed",
  "policyRule": {
    "if": {
      "anyOf": [
        {
          "field": "tags['Environment']",
          "exists": "false"
        },
        {
          "field": "tags['Owner']",
          "exists": "false"
        },
        {
          "field": "tags['CostCenter']",
          "exists": "false"
        }
      ]
    },
    "then": {
      "effect": "deny"
    }
  },
  "parameters": {}
}
```

#### Terraform Deployment

```hcl
resource "azurerm_policy_definition" "require_tags" {
  name         = "require-standard-tags"
  policy_type  = "Custom"
  mode         = "Indexed"
  display_name = "Require standard tags on all resources"

  policy_rule = file("${path.module}/policies/require-tags.json")
}

resource "azurerm_policy_assignment" "require_tags_subscription" {
  name                 = "require-tags"
  policy_definition_id = azurerm_policy_definition.require_tags.id
  scope                = "/subscriptions/${var.subscription_id}"
}
```

---

### Pattern 2: Tag Inheritance from Resource Group

Automatically inherit tags from parent resource group.

#### Azure Policy Definition (JSON)

```json
{
  "mode": "Indexed",
  "policyRule": {
    "if": {
      "allOf": [
        {
          "field": "[concat('tags[', parameters('tagName'), ']')]",
          "exists": "false"
        },
        {
          "value": "[resourceGroup().tags[parameters('tagName')]]",
          "notEquals": ""
        }
      ]
    },
    "then": {
      "effect": "modify",
      "details": {
        "roleDefinitionIds": [
          "/providers/microsoft.authorization/roleDefinitions/b24988ac-6180-42a0-ab88-20f7382dd24c"
        ],
        "operations": [
          {
            "operation": "add",
            "field": "[concat('tags[', parameters('tagName'), ']')]",
            "value": "[resourceGroup().tags[parameters('tagName')]]"
          }
        ]
      }
    }
  },
  "parameters": {
    "tagName": {
      "type": "String",
      "metadata": {
        "displayName": "Tag Name",
        "description": "Name of the tag to inherit from resource group"
      }
    }
  }
}
```

#### Terraform Deployment

```hcl
resource "azurerm_policy_definition" "inherit_tags" {
  name         = "inherit-tags-from-rg"
  policy_type  = "Custom"
  mode         = "Indexed"
  display_name = "Inherit tags from resource group"

  policy_rule = file("${path.module}/policies/inherit-tags.json")

  parameters = jsonencode({
    tagName = {
      type = "String"
      metadata = {
        displayName = "Tag Name"
        description = "Name of the tag to inherit"
      }
    }
  })
}

# Assign policy for each tag to inherit
resource "azurerm_policy_assignment" "inherit_environment" {
  name                 = "inherit-environment-tag"
  policy_definition_id = azurerm_policy_definition.inherit_tags.id
  scope                = "/subscriptions/${var.subscription_id}"

  parameters = jsonencode({
    tagName = { value = "Environment" }
  })
}

resource "azurerm_policy_assignment" "inherit_owner" {
  name                 = "inherit-owner-tag"
  policy_definition_id = azurerm_policy_definition.inherit_tags.id
  scope                = "/subscriptions/${var.subscription_id}"

  parameters = jsonencode({
    tagName = { value = "Owner" }
  })
}
```

---

### Pattern 3: Tag Value Enforcement (Enum)

Restrict tag values to allowed list.

#### Azure Policy Definition (JSON)

```json
{
  "mode": "Indexed",
  "policyRule": {
    "if": {
      "not": {
        "field": "tags['Environment']",
        "in": "[parameters('allowedValues')]"
      }
    },
    "then": {
      "effect": "deny"
    }
  },
  "parameters": {
    "allowedValues": {
      "type": "Array",
      "metadata": {
        "displayName": "Allowed Environment values",
        "description": "List of allowed values for Environment tag"
      },
      "defaultValue": ["prod", "staging", "dev", "test"]
    }
  }
}
```

#### Terraform Deployment

```hcl
resource "azurerm_policy_definition" "enforce_environment_values" {
  name         = "enforce-environment-tag-values"
  policy_type  = "Custom"
  mode         = "Indexed"
  display_name = "Enforce Environment tag values"

  policy_rule = file("${path.module}/policies/enforce-environment-values.json")

  parameters = jsonencode({
    allowedValues = {
      type = "Array"
      metadata = {
        displayName = "Allowed Environment values"
      }
      defaultValue = ["prod", "staging", "dev", "test"]
    }
  })
}

resource "azurerm_policy_assignment" "enforce_environment" {
  name                 = "enforce-environment-values"
  policy_definition_id = azurerm_policy_definition.enforce_environment_values.id
  scope                = "/subscriptions/${var.subscription_id}"
}
```

---

## GCP Label Enforcement

GCP uses Organization Policies to enforce label requirements.

### Pattern 1: Require Labels (Hard Enforcement)

Deny resource creation if required labels are missing.

**Note**: GCP Organization Policies enforce at folder/organization level, not per-resource. Use custom constraints for per-resource enforcement.

#### Organization Policy (YAML)

```yaml
constraint: constraints/gcp.resourceLabels
listPolicy:
  allowedValues:
  - environment:prod
  - environment:staging
  - environment:dev
  - owner:*@company.com
  - costcenter:cc-*
  - project:*
  deniedValues: []
  inheritFromParent: true
```

#### Terraform Deployment

```hcl
resource "google_organization_policy" "require_labels" {
  org_id     = var.organization_id
  constraint = "constraints/gcp.resourceLabels"

  list_policy {
    allow {
      values = [
        "environment:prod",
        "environment:staging",
        "environment:dev",
      ]
    }

    suggested_value     = "environment:dev"
    inherit_from_parent = true
  }
}
```

---

### Pattern 2: Custom Constraint (Regex Validation)

Enforce label value patterns using custom constraints.

#### Custom Constraint (YAML)

```yaml
name: organizations/{org_id}/customConstraints/custom.requireOwnerEmail
resource_types:
- "*"
method_types:
- CREATE
- UPDATE
condition: "resource.labels.owner.matches('^[a-z0-9._%+-]+@company\\\\.com$')"
action_type: DENY
display_name: "Require owner label with company domain email"
description: "All resources must have an owner label with @company.com email"
```

#### Terraform Deployment

```hcl
resource "google_org_policy_custom_constraint" "owner_email" {
  parent = "organizations/${var.organization_id}"
  name   = "custom.requireOwnerEmail"

  action_type    = "DENY"
  condition      = "resource.labels.owner.matches('^[a-z0-9._%+-]+@company\\\\.com$')"
  method_types   = ["CREATE", "UPDATE"]
  resource_types = ["*"]

  display_name = "Require owner label with company domain email"
  description  = "All resources must have an owner label with @company.com email"
}

resource "google_org_policy_policy" "owner_email_policy" {
  name   = "${google_org_policy_custom_constraint.owner_email.parent}/policies/${google_org_policy_custom_constraint.owner_email.name}"
  parent = google_org_policy_custom_constraint.owner_email.parent

  spec {
    rules {
      enforce = "TRUE"
    }
  }
}
```

---

### Pattern 3: Label Inheritance from Project

Apply project-level labels to all resources automatically.

```hcl
resource "google_project" "app_project" {
  name       = "ecommerce-prod"
  project_id = "ecommerce-prod-12345"
  org_id     = var.organization_id

  labels = {
    environment = "prod"
    owner       = "platform-team"
    costcenter  = "cc-1234"
    project     = "ecommerce"
    managedby   = "terraform"
  }
}

# All resources in this project inherit these labels
resource "google_compute_instance" "app_server" {
  name         = "prod-app-server"
  machine_type = "n1-standard-1"
  zone         = "us-central1-a"
  project      = google_project.app_project.project_id

  # Additional resource-specific labels
  labels = {
    component = "web"
    backup    = "daily"
  }
}
```

---

## Kubernetes Label Enforcement

Kubernetes uses admission controllers (OPA Gatekeeper, Kyverno) to enforce label requirements.

### Pattern 1: OPA Gatekeeper (Require Labels)

Block pod creation if required labels are missing.

#### Constraint Template

```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        openAPIV3Schema:
          type: object
          properties:
            labels:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels

        violation[{"msg": msg, "details": {"missing_labels": missing}}] {
          provided := {label | input.review.object.metadata.labels[label]}
          required := {label | label := input.parameters.labels[_]}
          missing := required - provided
          count(missing) > 0
          msg := sprintf("Resource is missing required labels: %v", [missing])
        }
```

#### Constraint

```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: require-standard-labels
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod", "Service"]
      - apiGroups: ["apps"]
        kinds: ["Deployment", "StatefulSet", "DaemonSet"]
  parameters:
    labels:
      - "environment"
      - "owner"
      - "project"
      - "app"
```

---

### Pattern 2: Kyverno Auto-Labeling

Automatically add labels to resources based on namespace or other metadata.

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-default-labels
spec:
  background: false
  rules:
  - name: add-environment-from-namespace
    match:
      any:
      - resources:
          kinds:
          - Pod
          - Deployment
          - StatefulSet
    mutate:
      patchStrategicMerge:
        metadata:
          labels:
            +(environment): "{{request.namespace}}"
            +(managed-by): "kyverno"
            +(created-by): "{{request.userInfo.username}}"

  - name: add-owner-from-namespace
    match:
      any:
      - resources:
          kinds:
          - Pod
    mutate:
      patchStrategicMerge:
        metadata:
          labels:
            +(owner): "{{request.object.metadata.namespace}}-team@company.com"

  - name: require-cost-center-label
    match:
      any:
      - resources:
          kinds:
          - PersistentVolumeClaim
          - Service
    validate:
      message: "CostCenter label is required for billing resources"
      pattern:
        metadata:
          labels:
            costcenter: "?*"
```

---

### Pattern 3: Kyverno Label Value Validation

Enforce label value patterns (enum or regex).

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: validate-label-values
spec:
  validationFailureAction: enforce
  background: true
  rules:
  - name: validate-environment-label
    match:
      any:
      - resources:
          kinds:
          - Pod
          - Deployment
    validate:
      message: "Environment label must be one of: prod, staging, dev, test"
      pattern:
        metadata:
          labels:
            environment: "prod|staging|dev|test"

  - name: validate-owner-email-format
    match:
      any:
      - resources:
          kinds:
          - Deployment
    validate:
      message: "Owner label must be a valid email address"
      deny:
        conditions:
          any:
          - key: "{{request.object.metadata.labels.owner}}"
            operator: NotEquals
            value: "*@company.com"
```

---

## Multi-Cloud Enforcement

Enforce consistent tagging across AWS, Azure, and GCP using infrastructure as code.

### Terraform Multi-Cloud Tags Module

```hcl
# modules/standard-tags/variables.tf
variable "environment" {
  type        = string
  description = "Environment (prod, staging, dev)"
  validation {
    condition     = contains(["prod", "staging", "dev", "test"], var.environment)
    error_message = "Environment must be prod, staging, dev, or test"
  }
}

variable "owner" {
  type        = string
  description = "Team email address"
  validation {
    condition     = can(regex("^[a-z0-9._%+-]+@company\\.com$", var.owner))
    error_message = "Owner must be a valid @company.com email"
  }
}

variable "cost_center" {
  type        = string
  description = "Finance cost center code"
  validation {
    condition     = can(regex("^CC-[0-9]{4}$", var.cost_center))
    error_message = "CostCenter must match format CC-####"
  }
}

variable "project" {
  type        = string
  description = "Project name"
}

# modules/standard-tags/outputs.tf
output "aws_tags" {
  value = {
    Environment = var.environment
    Owner       = var.owner
    CostCenter  = var.cost_center
    Project     = var.project
    ManagedBy   = "terraform"
  }
}

output "azure_tags" {
  value = {
    Environment = var.environment
    Owner       = var.owner
    CostCenter  = var.cost_center
    Project     = var.project
    ManagedBy   = "terraform"
  }
}

output "gcp_labels" {
  # GCP requires lowercase
  value = {
    environment = lower(var.environment)
    owner       = lower(replace(var.owner, "@", "-at-"))
    costcenter  = lower(var.cost_center)
    project     = lower(var.project)
    managedby   = "terraform"
  }
}

output "kubernetes_labels" {
  value = {
    environment = var.environment
    owner       = var.owner
    costcenter  = var.cost_center
    project     = var.project
    managedby   = "terraform"
  }
}
```

#### Usage

```hcl
module "tags" {
  source = "./modules/standard-tags"

  environment  = "prod"
  owner        = "platform-team@company.com"
  cost_center  = "CC-1234"
  project      = "ecommerce"
}

# AWS resources
resource "aws_instance" "app" {
  ami           = var.ami_id
  instance_type = "t3.medium"

  tags = merge(
    module.tags.aws_tags,
    {
      Name      = "prod-app-server"
      Component = "web"
    }
  )
}

# Azure resources
resource "azurerm_virtual_machine" "app" {
  name                = "prod-app-server"
  location            = "eastus"
  resource_group_name = azurerm_resource_group.main.name

  tags = merge(
    module.tags.azure_tags,
    {
      Component = "web"
    }
  )
}

# GCP resources
resource "google_compute_instance" "app" {
  name         = "prod-app-server"
  machine_type = "n1-standard-1"
  zone         = "us-central1-a"

  labels = merge(
    module.tags.gcp_labels,
    {
      component = "web"
    }
  )
}
```

---

## Pre-Deployment Validation

Validate tags BEFORE deployment using IaC linting tools.

### Checkov (Python)

```bash
# Install Checkov
pip install checkov

# Run tag validation on Terraform
checkov -d . --framework terraform --check CKV_AWS_111

# Custom Checkov policy for required tags
cat > .checkov.yaml <<EOF
---
framework: terraform
checks:
  - id: CKV_CUSTOM_1
    name: "Ensure all resources have required tags"
    guideline: "All resources must have Environment, Owner, CostCenter, Project tags"
    resource_types:
      - aws_instance
      - aws_db_instance
      - aws_s3_bucket
    tags_required:
      - Environment
      - Owner
      - CostCenter
      - Project
EOF
```

### tflint (Go)

```bash
# Install tflint
brew install tflint

# Configure tflint for tag enforcement
cat > .tflint.hcl <<EOF
rule "aws_resource_missing_tags" {
  enabled = true
  tags = ["Environment", "Owner", "CostCenter", "Project", "ManagedBy"]
}
EOF

# Run tflint
tflint
```

### terraform-compliance (Python BDD)

```bash
# Install terraform-compliance
pip install terraform-compliance

# Define tag compliance tests
mkdir -p compliance
cat > compliance/tags.feature <<EOF
Feature: Resource Tagging
  Scenario: Ensure all EC2 instances have required tags
    Given I have aws_instance defined
    Then it must contain tags
    And it must contain Environment
    And it must contain Owner
    And it must contain CostCenter
    And it must contain Project
EOF

# Run compliance tests
terraform-compliance -f compliance -p terraform.plan.json
```

---

## Best Practices Summary

1. **Start with soft enforcement** (alerts only), transition to hard enforcement after 30-90 days
2. **Use IaC for tags** (Terraform provider default_tags) to reduce manual errors by 95%
3. **Inherit from parents** (resource groups, folders, namespaces) to reduce tagging effort
4. **Validate pre-deployment** (Checkov, tflint) to catch violations before creation
5. **Automate remediation** (AWS Config, Azure Policy modify effect) for missing tags
6. **Audit weekly** (AWS Config, Azure Resource Graph, GCP Asset Inventory) to identify drift
7. **Test enforcement in sandbox** (SCPs/policies can lock out root user - test first)
8. **Document exceptions** (create waiver process for valid exceptions to tag policies)
