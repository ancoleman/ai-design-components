# Cost Allocation with Resource Tags

Complete guide to enabling cost allocation, showback/chargeback, and budget management using cloud resource tags.

## Table of Contents

1. [Cost Allocation Overview](#cost-allocation-overview)
2. [AWS Cost Allocation](#aws-cost-allocation)
3. [Azure Cost Management](#azure-cost-management)
4. [GCP Cloud Billing](#gcp-cloud-billing)
5. [Kubernetes Cost Allocation](#kubernetes-cost-allocation)
6. [Multi-Cloud Cost Visibility](#multi-cloud-cost-visibility)
7. [Showback and Chargeback](#showback-and-chargeback)

---

## Cost Allocation Overview

Resource tagging enables precise cost allocation, reducing unallocated cloud spend from 35% to <5%.

```
┌────────────────────────────────────────────────────────┐
│        Cloud Cost Allocation Hierarchy                 │
├────────────────────────────────────────────────────────┤
│                                                         │
│  WITHOUT TAGS:                                         │
│  └── Total Cloud Spend: $500,000/month                 │
│      ├── Allocated: $325,000 (65%)                     │
│      └── Unallocated: $175,000 (35%) ← Lost visibility│
│                                                         │
│  WITH COMPREHENSIVE TAGGING:                           │
│  └── Total Cloud Spend: $500,000/month                 │
│      ├── By Project:                                   │
│      │   ├── ecommerce: $200,000 (40%)                 │
│      │   ├── mobile-app: $150,000 (30%)                │
│      │   └── analytics: $125,000 (25%)                 │
│      ├── By Environment:                               │
│      │   ├── prod: $350,000 (70%)                      │
│      │   ├── staging: $75,000 (15%)                    │
│      │   └── dev: $50,000 (10%)                        │
│      ├── By Team:                                      │
│      │   ├── platform-team: $250,000 (50%)             │
│      │   ├── data-team: $150,000 (30%)                 │
│      │   └── mobile-team: $75,000 (15%)                │
│      └── Unallocated: $25,000 (5%) ← Minimal waste    │
│                                                         │
└────────────────────────────────────────────────────────┘
```

**Key cost allocation tags**:

| Tag | Purpose | Example |
|-----|---------|---------|
| **Project** | Track costs by business initiative | `ecommerce-platform` |
| **Environment** | Separate prod vs. dev/test costs | `prod`, `staging`, `dev` |
| **Owner** | Assign costs to responsible team | `platform-team@company.com` |
| **CostCenter** | Allocate to finance cost center | `CC-1234` |
| **Application** | Multi-app cost breakdown | `payment-api`, `user-service` |
| **Component** | Tier-level costs (web, db, cache) | `database`, `web`, `api` |

---

## AWS Cost Allocation

AWS Cost Explorer and Cost Allocation Tags provide detailed cost breakdowns.

### Step 1: Enable Cost Allocation Tags

**Cost allocation tags must be activated** (takes up to 24 hours for activation).

#### Via AWS Console

1. Navigate to AWS Billing → Cost Allocation Tags
2. Select tags to activate (Environment, Owner, CostCenter, Project)
3. Click "Activate"
4. Wait 24 hours for data to appear in Cost Explorer

#### Via Terraform

```hcl
# Enable cost allocation tags
resource "aws_ce_cost_allocation_tag" "environment" {
  tag_key = "Environment"
  status  = "Active"
}

resource "aws_ce_cost_allocation_tag" "owner" {
  tag_key = "Owner"
  status  = "Active"
}

resource "aws_ce_cost_allocation_tag" "costcenter" {
  tag_key = "CostCenter"
  status  = "Active"
}

resource "aws_ce_cost_allocation_tag" "project" {
  tag_key = "Project"
  status  = "Active"
}

resource "aws_ce_cost_allocation_tag" "application" {
  tag_key = "Application"
  status  = "Active"
}

resource "aws_ce_cost_allocation_tag" "component" {
  tag_key = "Component"
  status  = "Active"
}
```

**Cost**: No additional charge for cost allocation tags

---

### Step 2: Create Cost Allocation Reports

Query costs by tags in AWS Cost Explorer.

#### AWS CLI: Cost by Project Tag

```bash
# Get costs grouped by Project tag (last 30 days)
aws ce get-cost-and-usage \
  --time-period Start=2025-11-01,End=2025-12-01 \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --group-by Type=TAG,Key=Project \
  --output json | jq '.ResultsByTime[].Groups[] | {Project: .Keys[0], Cost: .Metrics.UnblendedCost.Amount}'
```

#### Terraform: Automated Cost Report

```hcl
# S3 bucket for cost reports
resource "aws_s3_bucket" "cost_reports" {
  bucket = "company-cost-allocation-reports"
}

resource "aws_s3_bucket_versioning" "cost_reports" {
  bucket = aws_s3_bucket.cost_reports.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Cost and Usage Report with tag breakdowns
resource "aws_cur_report_definition" "cost_allocation" {
  report_name                = "cost-allocation-report"
  time_unit                  = "DAILY"
  format                     = "Parquet"
  compression                = "Parquet"
  additional_schema_elements = ["RESOURCES"]
  s3_bucket                  = aws_s3_bucket.cost_reports.id
  s3_region                  = "us-east-1"
  s3_prefix                  = "cost-reports"

  additional_artifacts = ["ATHENA"]

  # Include tag columns in report
  report_versioning = "OVERWRITE_REPORT"
}
```

**Athena Query Example** (query Parquet cost reports):

```sql
-- Cost by Project tag (last 30 days)
SELECT
  line_item_usage_account_id,
  resource_tags_user_project AS project,
  resource_tags_user_environment AS environment,
  SUM(line_item_unblended_cost) AS total_cost
FROM
  cost_and_usage_report
WHERE
  year = '2025'
  AND month = '12'
  AND resource_tags_user_project IS NOT NULL
GROUP BY
  line_item_usage_account_id,
  resource_tags_user_project,
  resource_tags_user_environment
ORDER BY
  total_cost DESC
```

---

### Step 3: Cost Anomaly Detection by Tag

Detect unusual spending patterns for specific tags.

```hcl
# Cost anomaly monitor for Project tag
resource "aws_ce_anomaly_monitor" "project_monitor" {
  name              = "project-cost-monitor"
  monitor_type      = "DIMENSIONAL"
  monitor_dimension = "TAG"

  monitor_specification = jsonencode({
    Tags = {
      Key    = "Project"
      Values = ["ecommerce", "mobile-app", "analytics"]
    }
  })
}

# Alert when anomaly detected (cost spike >$100)
resource "aws_ce_anomaly_subscription" "project_alerts" {
  name      = "project-cost-alerts"
  frequency = "DAILY"

  monitor_arn_list = [
    aws_ce_anomaly_monitor.project_monitor.arn
  ]

  subscriber {
    type    = "EMAIL"
    address = "finops-team@company.com"
  }

  threshold_expression {
    dimension {
      key           = "ANOMALY_TOTAL_IMPACT_ABSOLUTE"
      values        = ["100"]
      match_options = ["GREATER_THAN_OR_EQUAL"]
    }
  }
}

# Monitor by Environment tag
resource "aws_ce_anomaly_monitor" "environment_monitor" {
  name              = "environment-cost-monitor"
  monitor_type      = "DIMENSIONAL"
  monitor_dimension = "TAG"

  monitor_specification = jsonencode({
    Tags = {
      Key    = "Environment"
      Values = ["prod", "staging", "dev"]
    }
  })
}
```

**Cost**: $0.01 per anomaly detection monitored per day

---

### Step 4: Budget Alerts by Tag

Create budgets for specific tag values (e.g., per-project budgets).

```hcl
# Budget for ecommerce project
resource "aws_budgets_budget" "ecommerce_budget" {
  name              = "ecommerce-monthly-budget"
  budget_type       = "COST"
  limit_amount      = "50000"
  limit_unit        = "USD"
  time_period_start = "2025-01-01_00:00"
  time_unit         = "MONTHLY"

  cost_filters = {
    TagKeyValue = "Project$ecommerce"
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = ["platform-team@company.com"]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = ["finance@company.com", "platform-team@company.com"]
  }
}

# Budget per environment
resource "aws_budgets_budget" "dev_budget" {
  name              = "dev-environment-budget"
  budget_type       = "COST"
  limit_amount      = "5000"
  limit_unit        = "USD"
  time_period_start = "2025-01-01_00:00"
  time_unit         = "MONTHLY"

  cost_filters = {
    TagKeyValue = "Environment$dev"
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 90
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = ["devops-team@company.com"]
  }
}
```

---

## Azure Cost Management

Azure Cost Management provides cost analysis and budget management by tags.

### Step 1: Cost Analysis by Tags

#### Azure Portal

1. Navigate to Cost Management + Billing → Cost Analysis
2. Click "Group by" → Select "Tag: Environment" (or other tag)
3. View cost breakdown by tag value

#### Azure CLI

```bash
# Export costs grouped by tags
az consumption usage list \
  --start-date 2025-11-01 \
  --end-date 2025-12-01 \
  --query "[].{Date:usageStart, Cost:pretaxCost, Project:tags.Project, Environment:tags.Environment, Owner:tags.Owner}" \
  --output table

# Cost summary by Project tag
az consumption usage list \
  --start-date 2025-11-01 \
  --end-date 2025-12-01 \
  --query "group_by([], tags.Project, sum(pretaxCost))" \
  --output json
```

---

### Step 2: Cost Management Query (REST API)

```bash
# Cost breakdown by tags via REST API
POST https://management.azure.com/subscriptions/{subscription-id}/providers/Microsoft.CostManagement/query?api-version=2021-10-01

{
  "type": "ActualCost",
  "timeframe": "MonthToDate",
  "dataset": {
    "granularity": "Daily",
    "aggregation": {
      "totalCost": {
        "name": "Cost",
        "function": "Sum"
      }
    },
    "grouping": [
      {
        "type": "TagKey",
        "name": "Project"
      },
      {
        "type": "TagKey",
        "name": "Environment"
      }
    ]
  }
}
```

#### Terraform: Cost Management Export

```hcl
# Storage account for cost exports
resource "azurerm_storage_account" "cost_exports" {
  name                     = "companycostexports"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = "eastus"
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "cost_data" {
  name                  = "cost-data"
  storage_account_name  = azurerm_storage_account.cost_exports.name
  container_access_type = "private"
}

# Cost export with tag columns
resource "azurerm_cost_management_export_resource_group" "monthly_export" {
  name                    = "monthly-cost-export"
  resource_group_id       = azurerm_resource_group.main.id
  recurrence_type         = "Monthly"
  recurrence_period_start = "2025-01-01T00:00:00Z"
  recurrence_period_end   = "2026-12-31T23:59:59Z"

  delivery_info {
    storage_account_id = azurerm_storage_account.cost_exports.id
    container_name     = azurerm_storage_container.cost_data.name
    root_folder_path   = "cost-exports"
  }

  query {
    type       = "ActualCost"
    time_frame = "MonthToDate"

    dataset {
      granularity = "Daily"

      grouping {
        type = "TagKey"
        name = "Project"
      }

      grouping {
        type = "TagKey"
        name = "Environment"
      }
    }
  }
}
```

---

### Step 3: Budget Alerts by Tags

```hcl
# Budget for specific project tag
resource "azurerm_consumption_budget_resource_group" "ecommerce_budget" {
  name              = "ecommerce-project-budget"
  resource_group_id = azurerm_resource_group.main.id

  amount     = 50000
  time_grain = "Monthly"

  time_period {
    start_date = "2025-01-01T00:00:00Z"
    end_date   = "2026-12-31T23:59:59Z"
  }

  filter {
    tag {
      name   = "Project"
      values = ["ecommerce"]
    }
  }

  notification {
    enabled   = true
    threshold = 80.0
    operator  = "GreaterThan"

    contact_emails = [
      "platform-team@company.com",
    ]
  }

  notification {
    enabled   = true
    threshold = 100.0
    operator  = "GreaterThan"

    contact_emails = [
      "finance@company.com",
      "platform-team@company.com",
    ]
  }
}
```

---

## GCP Cloud Billing

GCP exports billing data to BigQuery with label breakdowns.

### Step 1: Enable Billing Export to BigQuery

#### GCP Console

1. Navigate to Billing → Billing export
2. Enable "BigQuery export"
3. Select dataset for export (creates daily billing tables)

#### Terraform

```hcl
# BigQuery dataset for billing export
resource "google_bigquery_dataset" "billing_export" {
  dataset_id  = "billing_export"
  location    = "US"
  description = "GCP billing data export"

  labels = {
    environment = "prod"
    managedby   = "terraform"
  }
}

# Billing export (configured via gcloud, not Terraform)
# gcloud beta billing accounts export billing-data \
#   --billing-account=BILLING_ACCOUNT_ID \
#   --dataset-id=PROJECT_ID:billing_export
```

---

### Step 2: Query Costs by Labels

```sql
-- Cost breakdown by label (last 30 days)
SELECT
  labels.key AS label_key,
  labels.value AS label_value,
  SUM(cost) AS total_cost,
  SUM(usage.amount) AS total_usage,
  usage.unit
FROM
  `project.billing_export.gcp_billing_export_v1_XXXXX`
CROSS JOIN
  UNNEST(labels) AS labels
WHERE
  _PARTITIONTIME >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  AND labels.key IN ('environment', 'project', 'costcenter', 'owner')
GROUP BY
  label_key, label_value, usage.unit
ORDER BY
  total_cost DESC
```

```sql
-- Cost by project label (monthly trend)
SELECT
  EXTRACT(MONTH FROM usage_start_time) AS month,
  labels.value AS project,
  SUM(cost) AS monthly_cost
FROM
  `project.billing_export.gcp_billing_export_v1_XXXXX`
CROSS JOIN
  UNNEST(labels) AS labels
WHERE
  labels.key = 'project'
  AND usage_start_time >= TIMESTAMP('2025-01-01')
GROUP BY
  month, project
ORDER BY
  month, monthly_cost DESC
```

```sql
-- Untagged resources (missing required labels)
SELECT
  service.description AS service,
  sku.description AS resource_type,
  SUM(cost) AS unallocated_cost
FROM
  `project.billing_export.gcp_billing_export_v1_XXXXX`
WHERE
  _PARTITIONTIME >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  AND (
    ARRAY_LENGTH(labels) = 0  -- No labels at all
    OR NOT EXISTS (
      SELECT 1 FROM UNNEST(labels) WHERE key IN ('environment', 'project', 'owner')
    )
  )
GROUP BY
  service, resource_type
ORDER BY
  unallocated_cost DESC
LIMIT 20
```

---

### Step 3: Budget Alerts by Labels

```hcl
# Budget for specific project label
resource "google_billing_budget" "ecommerce_budget" {
  billing_account = var.billing_account_id
  display_name    = "Ecommerce Project Budget"

  budget_filter {
    projects = ["projects/${var.project_id}"]

    labels = {
      project = "ecommerce"
    }
  }

  amount {
    specified_amount {
      currency_code = "USD"
      units         = "50000"
    }
  }

  threshold_rules {
    threshold_percent = 0.8
  }

  threshold_rules {
    threshold_percent = 1.0
  }

  threshold_rules {
    threshold_percent = 1.2
    spend_basis       = "FORECASTED_SPEND"
  }

  all_updates_rule {
    monitoring_notification_channels = [
      google_monitoring_notification_channel.email.name
    ]
  }
}

resource "google_monitoring_notification_channel" "email" {
  display_name = "FinOps Team Email"
  type         = "email"

  labels = {
    email_address = "finops-team@company.com"
  }
}
```

---

## Kubernetes Cost Allocation

Track Kubernetes costs by namespace labels using Kubecost or OpenCost.

### Kubecost Label-Based Allocation

**Install Kubecost**:

```bash
helm repo add kubecost https://kubecost.github.io/cost-analyzer/
helm install kubecost kubecost/cost-analyzer \
  --namespace kubecost --create-namespace \
  --set kubecostToken="your-token"
```

**Query costs by label via API**:

```bash
# Cost by environment label (last 7 days)
curl "http://kubecost.company.com/model/allocation \
  ?window=7d \
  &aggregate=label:environment \
  &accumulate=true"

# Cost by project label
curl "http://kubecost.company.com/model/allocation \
  ?window=month \
  &aggregate=label:project"
```

**Kubecost allocation configuration**:

```yaml
# values.yaml for Kubecost Helm chart
kubecostModel:
  allocationLabels:
    - environment
    - project
    - owner
    - costcenter
    - app
```

---

### OpenCost (Open Source Alternative)

```bash
# Install OpenCost
kubectl apply -f https://raw.githubusercontent.com/opencost/opencost/develop/kubernetes/opencost.yaml

# Port-forward to access UI
kubectl port-forward -n opencost service/opencost 9003:9003

# Query costs by label
curl "http://localhost:9003/allocation \
  ?window=7d \
  &aggregate=label:environment"
```

---

## Multi-Cloud Cost Visibility

Aggregate costs across AWS, Azure, GCP using multi-cloud cost management tools.

### CloudHealth by VMware

**Features**:
- Multi-cloud cost aggregation (AWS, Azure, GCP)
- Tag-based showback/chargeback
- Cost anomaly detection
- Budget management

**Integration**: Connect AWS, Azure, GCP billing accounts via IAM roles/service principals

---

### Apptio Cloudability

**Features**:
- Unified cost dashboard (AWS, Azure, GCP, Kubernetes)
- Tag normalization (standardize tags across clouds)
- Showback reports by tag
- Commitment optimization (RIs, Savings Plans)

---

### Custom Multi-Cloud Cost Dashboard

Aggregate billing exports from all clouds into single data warehouse.

```sql
-- Unified cost view (AWS + Azure + GCP)
CREATE VIEW unified_cloud_costs AS
SELECT
  'AWS' AS cloud_provider,
  line_item_usage_account_id AS account_id,
  resource_tags_user_project AS project,
  resource_tags_user_environment AS environment,
  line_item_unblended_cost AS cost,
  line_item_usage_start_date AS usage_date
FROM aws_cost_and_usage_report
WHERE resource_tags_user_project IS NOT NULL

UNION ALL

SELECT
  'Azure' AS cloud_provider,
  subscription_id AS account_id,
  tags['Project'] AS project,
  tags['Environment'] AS environment,
  cost AS cost,
  date AS usage_date
FROM azure_cost_export
WHERE tags['Project'] IS NOT NULL

UNION ALL

SELECT
  'GCP' AS cloud_provider,
  project.id AS account_id,
  labels.value AS project,
  env_labels.value AS environment,
  cost AS cost,
  usage_start_time AS usage_date
FROM gcp_billing_export
CROSS JOIN UNNEST(labels) AS labels
CROSS JOIN UNNEST(labels) AS env_labels
WHERE labels.key = 'project'
  AND env_labels.key = 'environment'
```

---

## Showback and Chargeback

### Showback (Informational Cost Reporting)

**Purpose**: Show teams their cloud costs without billing them
**Use case**: Dev/test environments, internal transparency

**Monthly showback report example**:

| Team | Project | Environment | Monthly Cost | YoY Change |
|------|---------|-------------|--------------|------------|
| Platform Team | ecommerce | prod | $25,000 | +15% |
| Platform Team | ecommerce | staging | $3,000 | +5% |
| Data Team | analytics | prod | $18,000 | +30% |
| Mobile Team | mobile-app | prod | $12,000 | -10% |

**Implementation**: Automated email report generated from cost allocation queries

---

### Chargeback (Actual Cost Billing)

**Purpose**: Bill internal teams for their actual cloud usage
**Use case**: Multi-tenant SaaS, shared services billing

**Chargeback implementation**:

```python
# chargeback_report.py
import boto3
from datetime import datetime, timedelta

def generate_chargeback_report(start_date, end_date):
    ce_client = boto3.client('ce')

    response = ce_client.get_cost_and_usage(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        Granularity='MONTHLY',
        Metrics=['UnblendedCost'],
        GroupBy=[
            {'Type': 'TAG', 'Key': 'CostCenter'},
            {'Type': 'TAG', 'Key': 'Project'}
        ]
    )

    chargeback = {}
    for result in response['ResultsByTime']:
        for group in result['Groups']:
            cost_center = group['Keys'][0].split('$')[1]
            project = group['Keys'][1].split('$')[1]
            cost = float(group['Metrics']['UnblendedCost']['Amount'])

            if cost_center not in chargeback:
                chargeback[cost_center] = {}
            chargeback[cost_center][project] = cost

    return chargeback

# Export to finance system (CSV)
def export_chargeback_csv(chargeback_data, output_file):
    with open(output_file, 'w') as f:
        f.write('CostCenter,Project,Amount\n')
        for cost_center, projects in chargeback_data.items():
            for project, amount in projects.items():
                f.write(f'{cost_center},{project},{amount:.2f}\n')

if __name__ == '__main__':
    last_month_start = (datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1).strftime('%Y-%m-%d')
    last_month_end = datetime.now().replace(day=1).strftime('%Y-%m-%d')

    chargeback = generate_chargeback_report(last_month_start, last_month_end)
    export_chargeback_csv(chargeback, f'chargeback_{last_month_start}.csv')
```

---

## Best Practices Summary

1. **Activate cost allocation tags** in billing console (AWS, Azure, GCP)
2. **Wait 24 hours** for cost allocation data to populate (AWS)
3. **Create budgets by tag** to prevent cost overruns per project/team
4. **Set up anomaly detection** for unusual spending patterns
5. **Export billing data** to data warehouse for custom analysis
6. **Automate showback reports** (monthly email to teams with their costs)
7. **Track unallocated spend** (resources without required tags = wasted visibility)
8. **Use Kubecost/OpenCost** for Kubernetes cost allocation by namespace/label
9. **Normalize tags** across clouds for unified multi-cloud cost reporting
10. **Integrate with finance systems** for automated chargeback billing
