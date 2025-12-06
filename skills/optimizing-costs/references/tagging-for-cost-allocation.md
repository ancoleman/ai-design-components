# Tagging for Cost Allocation

Effective tagging is the foundation of cost visibility and accountability. Without proper tags, costs cannot be allocated to teams, projects, or environments.

## Table of Contents

1. [Required Tags](#required-tags)
2. [Cloud-Specific Tag Activation](#cloud-specific-tag-activation)
3. [Tagging Enforcement](#tagging-enforcement)
4. [Tagging Automation](#tagging-automation)
5. [Tagging Audit and Backfill](#tagging-audit-and-backfill)
6. [Cost Allocation Reports](#cost-allocation-reports)
7. [Showback and Chargeback](#showback-and-chargeback)
8. [Tag Naming Conventions](#tag-naming-conventions)
9. [Tagging Compliance Checklist](#tagging-compliance-checklist)

---

## Required Tags

### Minimum Tagging Strategy

Every cloud resource must have these four tags:

| Tag Key | Purpose | Example Values |
|---------|---------|----------------|
| `Owner` or `Team` | Responsible team/department | backend-team, data-engineering, platform |
| `Project` or `Application` | Business unit or application | customer-api, analytics-pipeline, website |
| `Environment` | Deployment environment | prod, staging, dev, test |
| `CostCenter` | Finance cost center code | CC-1001, engineering, marketing |

### Recommended Additional Tags

| Tag Key | Purpose | Example Values |
|---------|---------|----------------|
| `Service` | Microservice name | user-service, payment-service, auth-service |
| `ManagedBy` | Provisioning tool | terraform, cloudformation, manual |
| `Owner-Email` | Contact for questions | team-backend@company.com |
| `Lifecycle` | Resource lifecycle | permanent, temporary, experiment |
| `Compliance` | Regulatory requirements | pci-dss, hipaa, gdpr, none |

---

## Cloud-Specific Tag Activation

### AWS: Cost Allocation Tags

**Activate tags in billing console:**
```bash
# Enable cost allocation tag
aws ce update-cost-allocation-tags-status \
  --cost-allocation-tags-status TagKey=Environment,Status=Active \
  --cost-allocation-tags-status TagKey=Project,Status=Active
```

**Tags take 24 hours to appear in Cost Explorer after activation.**

**User-Defined vs. AWS-Generated Tags:**
- User-Defined: Custom tags added to resources
- AWS-Generated: Automatic tags (aws:createdBy, aws:cloudformation:stack-name)

### Azure: Tags and Resource Policies

**Apply tags via Azure Policy:**
```json
{
  "policyRule": {
    "if": {
      "allOf": [
        {"field": "type", "equals": "Microsoft.Compute/virtualMachines"},
        {"field": "tags['Environment']", "exists": "false"}
      ]
    },
    "then": {
      "effect": "deny"
    }
  }
}
```

**View costs by tag:**
```bash
az consumption usage list \
  --start-date 2025-12-01 \
  --end-date 2025-12-31 \
  --query "[?tags.Environment=='prod']"
```

### GCP: Labels (Not Tags)

**GCP uses "labels" instead of "tags":**
```bash
# Add labels to instance
gcloud compute instances add-labels my-instance \
  --labels=environment=prod,team=backend,project=api
```

**Export billing data to BigQuery with labels:**
```sql
SELECT
  labels.key,
  labels.value,
  SUM(cost) as total_cost
FROM `project.dataset.gcp_billing_export_v1_BILLING_ACCOUNT_ID`
WHERE labels.key = 'environment'
GROUP BY labels.key, labels.value
ORDER BY total_cost DESC;
```

---

## Tagging Enforcement

### AWS Config Rule

**Require tags on EC2 instances:**
```json
{
  "ConfigRuleName": "required-tags",
  "Source": {
    "Owner": "AWS",
    "SourceIdentifier": "REQUIRED_TAGS"
  },
  "Scope": {
    "ComplianceResourceTypes": [
      "AWS::EC2::Instance",
      "AWS::RDS::DBInstance",
      "AWS::S3::Bucket"
    ]
  },
  "InputParameters": "{\"tag1Key\":\"Environment\",\"tag2Key\":\"Owner\",\"tag3Key\":\"Project\"}"
}
```

### Azure Policy

**Deny resources without required tags:**
```json
{
  "properties": {
    "displayName": "Require tags on resources",
    "mode": "All",
    "policyRule": {
      "if": {
        "anyOf": [
          {"field": "tags['Environment']", "exists": "false"},
          {"field": "tags['Owner']", "exists": "false"},
          {"field": "tags['Project']", "exists": "false"}
        ]
      },
      "then": {"effect": "deny"}
    }
  }
}
```

### GCP Organization Policies

**Require labels on Compute Engine instances:**
```yaml
constraint: constraints/compute.requireLabels
listPolicy:
  allowedValues:
    - "environment"
    - "team"
    - "project"
```

---

## Tagging Automation

### Terraform: Enforce tags via default_tags

**AWS Provider:**
```hcl
provider "aws" {
  region = "us-east-1"

  default_tags {
    tags = {
      ManagedBy   = "Terraform"
      Environment = var.environment
      Project     = var.project_name
      Owner       = var.team_name
    }
  }
}

# All resources automatically inherit default tags
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  # Additional tags (merged with default_tags)
  tags = {
    Name = "web-server-1"
  }
}
```

### AWS Lambda: Auto-Tag Resources

```python
import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    """
    Auto-tag EC2 instances on creation.
    Triggered by CloudWatch Events (EC2 instance state change).
    """
    instance_id = event['detail']['instance-id']

    # Extract tags from instance metadata or environment
    tags = [
        {'Key': 'AutoTagged', 'Value': 'true'},
        {'Key': 'CreatedBy', 'Value': event['detail']['userIdentity']['principalId']},
        {'Key': 'CreatedAt', 'Value': event['time']}
    ]

    ec2.create_tags(Resources=[instance_id], Tags=tags)

    return {'statusCode': 200, 'body': f'Tagged {instance_id}'}
```

---

## Tagging Audit and Backfill

### Find Untagged Resources (AWS)

```bash
# EC2 instances without required tags
aws ec2 describe-instances \
  --query 'Reservations[].Instances[?!not_null(Tags[?Key==`Environment`])].[InstanceId]' \
  --output text

# RDS instances without tags
aws rds describe-db-instances \
  --query 'DBInstances[?length(TagList)==`0`].[DBInstanceIdentifier]' \
  --output text
```

### Backfill Tags on Existing Resources

```bash
# Tag all untagged EC2 instances
for instance in $(aws ec2 describe-instances --query 'Reservations[].Instances[?!not_null(Tags[?Key==`Environment`])].[InstanceId]' --output text); do
  aws ec2 create-tags \
    --resources $instance \
    --tags Key=Environment,Value=unknown Key=Owner,Value=platform-team
done
```

---

## Cost Allocation Reports

### AWS Cost and Usage Report (CUR)

**Enable CUR with tag columns:**
```bash
aws cur put-report-definition \
  --report-definition '{
    "ReportName": "cost-usage-report",
    "TimeUnit": "DAILY",
    "Format": "Parquet",
    "Compression": "Parquet",
    "S3Bucket": "my-cur-bucket",
    "S3Prefix": "reports/",
    "S3Region": "us-east-1",
    "AdditionalSchemaElements": ["RESOURCES"],
    "ReportVersioning": "OVERWRITE_REPORT",
    "AdditionalArtifacts": ["ATHENA"]
  }'
```

**Query CUR in Athena:**
```sql
SELECT
  line_item_resource_id,
  resource_tags_user_environment,
  resource_tags_user_team,
  SUM(line_item_unblended_cost) AS cost
FROM cost_usage_report
WHERE year = '2025' AND month = '12'
GROUP BY 1, 2, 3
ORDER BY cost DESC
LIMIT 100;
```

### Azure Cost Management

**Export costs by tag:**
```bash
az consumption usage list \
  --start-date 2025-12-01 \
  --end-date 2025-12-31 \
  --query "[].{Resource:instanceName, Environment:tags.Environment, Cost:pretaxCost}" \
  --output table
```

### GCP Billing Export

**Query BigQuery for cost by label:**
```sql
SELECT
  ARRAY(
    SELECT value
    FROM UNNEST(labels)
    WHERE key = 'environment'
  )[OFFSET(0)] AS environment,
  ARRAY(
    SELECT value
    FROM UNNEST(labels)
    WHERE key = 'team'
  )[OFFSET(0)] AS team,
  SUM(cost) AS total_cost
FROM `project.dataset.gcp_billing_export_v1_BILLING_ACCOUNT_ID`
WHERE _PARTITIONTIME >= '2025-12-01'
  AND _PARTITIONTIME < '2025-12-31'
GROUP BY environment, team
ORDER BY total_cost DESC;
```

---

## Showback and Chargeback

### Showback (Informational)

**Monthly cost report by team:**
```
Team: Backend
Environment: Production
Month: December 2025

Service          Cost
--------------   --------
EC2 Instances    $15,234
RDS Databases    $8,456
S3 Storage       $2,123
Data Transfer    $1,890
--------------   --------
Total            $27,703
```

**Automation:**
- Weekly Slack messages with team costs
- Monthly email reports to team leads
- Grafana dashboards with cost metrics

### Chargeback (Financial Accountability)

**Invoice teams for their usage:**
```
Invoice: Backend Team - December 2025
Budget: $25,000
Actual: $27,703
Variance: +$2,703 (10.8% over budget)

Action Required:
- Reduce EC2 instance count by 15%
- Right-size RDS instances (currently <40% utilization)
- Implement S3 lifecycle policies
```

**Implementation:**
1. Start with Showback (3-6 months) to establish baseline
2. Set team budgets based on historical usage
3. Transition to Chargeback (actual billing to teams)
4. Monthly budget reviews and variance analysis

---

## Tag Naming Conventions

### Best Practices

**Use PascalCase or kebab-case consistently:**
- ✅ Good: `Environment`, `CostCenter`, `OwnerEmail`
- ✅ Good: `environment`, `cost-center`, `owner-email`
- ❌ Bad: `ENVIRONMENT`, `cost_center`, `Owner-email` (inconsistent)

**Avoid special characters:**
- ✅ Good: `team-backend`, `project-api`
- ❌ Bad: `team@backend`, `project/api` (special chars cause issues)

**Keep values lowercase:**
- ✅ Good: `environment=prod`, `owner=backend-team`
- ❌ Bad: `environment=PROD`, `owner=Backend_Team` (case mismatch)

**Use controlled vocabulary:**
```yaml
# Tag value whitelist
Environment:
  - prod
  - staging
  - dev
  - test

Owner:
  - backend-team
  - frontend-team
  - data-team
  - platform-team
```

---

## Tagging Compliance Checklist

- [ ] Define required tags (Owner, Project, Environment, CostCenter)
- [ ] Activate cost allocation tags in cloud billing console
- [ ] Enforce tagging via policy (AWS Config, Azure Policy, GCP Org Policy)
- [ ] Automate tagging (Terraform default_tags, Lambda auto-tag)
- [ ] Audit untagged resources weekly
- [ ] Backfill tags on existing resources
- [ ] Generate showback reports monthly
- [ ] Transition to chargeback (optional, after 3-6 months)
- [ ] Monitor tag compliance (target >90% coverage)
