# Resource Tagging Taxonomy

Complete taxonomy of cloud resource tags organized by category, purpose, and use case.

## Table of Contents

1. [Tag Categories Overview](#tag-categories-overview)
2. [Technical Tags](#technical-tags)
3. [Business Tags](#business-tags)
4. [Security Tags](#security-tags)
5. [Automation Tags](#automation-tags)
6. [Operational Tags](#operational-tags)
7. [Custom Tags](#custom-tags)
8. [Tag Naming Patterns](#tag-naming-patterns)
9. [Tag Value Standards](#tag-value-standards)

---

## Tag Categories Overview

Six core tag categories provide complete cloud governance coverage:

```
┌─────────────────────────────────────────────────────────┐
│                  Six Core Tag Categories                 │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. TECHNICAL TAGS → Operations & Lifecycle             │
│  2. BUSINESS TAGS → Cost Allocation & Ownership         │
│  3. SECURITY TAGS → Compliance & Access Control         │
│  4. AUTOMATION TAGS → Infrastructure Management         │
│  5. OPERATIONAL TAGS → Support & Change Management      │
│  6. CUSTOM TAGS → Organization-Specific Metadata        │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Priority recommendation**: Start with Technical + Business tags (categories 1-2), add Security + Automation (3-4) for regulated industries, use Operational + Custom (5-6) for advanced governance.

---

## Technical Tags

Operations-focused metadata for resource identification and lifecycle management.

### Name

**Purpose**: Human-readable resource identifier
**Required**: Yes (all resources)
**Format**: `{env}-{app}-{component}-{number}`
**Example**: `prod-api-server-01`

**Naming patterns**:
- Short, descriptive, unique within environment
- Include environment prefix for clarity across accounts
- Sequential numbering for multiple identical resources
- Kebab-case recommended for readability

**AWS**: Name tag displayed in console as primary identifier
**Azure**: Name property separate from tags
**GCP**: Name property separate from labels
**Kubernetes**: metadata.name (separate from labels)

### Environment

**Purpose**: Deployment lifecycle stage
**Required**: Yes (all resources)
**Values**: `prod` | `staging` | `dev` | `test` | `qa` | `demo`
**Example**: `prod`

**Use cases**:
- Cost allocation by environment
- Automated shutdown policies (dev/test resources overnight)
- Security policies (prod requires stricter access controls)
- Backup policies (prod: daily, dev: weekly or none)

**Recommended values**:
```yaml
prod:     Production workloads (customer-facing)
staging:  Pre-production validation environment
dev:      Development/experimental environment
test:     Automated testing environment
qa:       Quality assurance testing
demo:     Sales/demo environment
```

### Version

**Purpose**: Application or infrastructure version
**Required**: No (optional)
**Format**: Semantic versioning `vX.Y.Z` or git commit SHA
**Example**: `v1.2.3` or `abc123de`

**Use cases**:
- Track deployed application version
- Correlate resource configuration with code version
- Rollback identification
- Change tracking

### ManagedBy

**Purpose**: Resource creation and management method
**Required**: Yes (prevents accidental manual changes to IaC resources)
**Values**: `terraform` | `pulumi` | `cloudformation` | `ansible` | `manual`
**Example**: `terraform`

**Use cases**:
- Prevent manual changes to IaC-managed resources
- Identify drift from IaC state
- Audit which resources are managed vs. ad-hoc
- Cleanup automation (identify orphaned manual resources)

**AWS Config rule**: Alert when IaC-managed resource is modified outside IaC
**Azure Policy**: Audit resources created manually vs. via ARM/Bicep
**GCP Organization Policy**: Tag resources with creation method

---

## Business Tags

Cost allocation and ownership metadata for financial operations (FinOps).

### Owner

**Purpose**: Responsible team or individual contact
**Required**: Yes (all resources)
**Format**: Team email address
**Example**: `platform-team@company.com`

**Use cases**:
- Security incident contact (who to notify for this resource)
- Cost allocation responsibility
- Change approval routing
- Resource lifecycle decisions (can this be deleted?)

**Best practices**:
- Use team/group email (not individual email - avoids orphaned resources when employees leave)
- Format: `{team-name}@company.com`
- Integrate with identity provider for validation
- Distribution list preferred over individual accounts

### CostCenter

**Purpose**: Finance department code for billing allocation
**Required**: Yes (cost allocation)
**Format**: Organization-specific finance code
**Example**: `CC-1234` or `ENG-001`

**Use cases**:
- Showback/chargeback to business units
- Budget tracking by department
- Cost anomaly detection by cost center
- Financial reporting and forecasting

**Integration**:
- AWS Cost Explorer: Group costs by CostCenter tag
- Azure Cost Management: Allocate costs to billing accounts
- GCP Cloud Billing: Export with cost center labels
- ERP systems: Match cloud costs to finance codes

**Validation**: Regex pattern `^[A-Z]{2,4}-[0-9]{3,6}$` (adjust to org standard)

### Project

**Purpose**: Business initiative or product name
**Required**: Yes (cost allocation + organization)
**Format**: Kebab-case project name
**Example**: `ecommerce-platform` or `mobile-app`

**Use cases**:
- Cost tracking by project/product
- Resource discovery (find all resources for project X)
- Access control (grant project team access to project resources)
- Lifecycle management (sunset all resources when project ends)

**Best practices**:
- Single project name across all resources for that initiative
- Lowercase, hyphens only (avoid spaces, special chars)
- Match project name in project management tools (Jira, Azure DevOps)
- Archive project tag when project sunset

### Department

**Purpose**: Organizational department
**Required**: No (optional)
**Values**: `engineering` | `sales` | `marketing` | `finance` | `operations`
**Example**: `engineering`

**Use cases**:
- High-level cost allocation (department-level budgets)
- Organizational reporting
- Compliance scope (which departments handle PCI data?)

**When to use**: Large organizations (500+ employees) with department-level budgeting

---

## Security Tags

Compliance and access control metadata for security policies.

### Confidentiality

**Purpose**: Data sensitivity classification
**Required**: Recommended (security-sensitive orgs)
**Values**: `public` | `internal` | `confidential` | `restricted`
**Example**: `confidential`

**Use cases**:
- Access control policies (restrict access to confidential resources)
- Encryption requirements (confidential = encrypt at rest + in transit)
- Audit logging (confidential resources require detailed logs)
- Data residency (restricted data cannot leave specific regions)

**Mapping**:
```yaml
public:        Publicly accessible data (website content, marketing)
internal:      Internal company data (not publicly shared)
confidential:  Sensitive business data (financial, strategic)
restricted:    Highly sensitive data (PII, PHI, payment data)
```

### Compliance

**Purpose**: Regulatory compliance requirements
**Required**: Yes (for regulated industries)
**Values**: `PCI` | `HIPAA` | `SOC2` | `GDPR` | `FedRAMP` | `none`
**Example**: `PCI` or `HIPAA,SOC2` (comma-separated if multiple)

**Use cases**:
- Compliance scope definition (which resources are in-scope for audit)
- Automated policy enforcement (PCI resources require specific security controls)
- Audit trail generation (compliance resources require enhanced logging)
- Cost tracking (compliance adds overhead cost to resources)

**Integration**:
- AWS Security Hub: Filter compliance findings by tag
- Azure Policy: Enforce controls on compliance-tagged resources
- GCP Security Command Center: Scope assessments by compliance label

### DataClassification

**Purpose**: Data tier classification for retention/backup
**Required**: No (optional)
**Values**: `tier1` | `tier2` | `tier3` | `tier4`
**Example**: `tier1`

**Tier definitions**:
```yaml
tier1: Critical data (cannot be recreated, RPO < 1 hour)
tier2: Important data (difficult to recreate, RPO < 24 hours)
tier3: Standard data (can be recreated, RPO < 7 days)
tier4: Ephemeral data (easily recreated, no backup required)
```

**Use cases**:
- Backup frequency (tier1: continuous, tier2: hourly, tier3: daily, tier4: none)
- Retention policies (tier1: 7 years, tier2: 3 years, tier3: 1 year, tier4: 30 days)
- Disaster recovery priority (tier1 restored first)

### SecurityZone

**Purpose**: Network security zone classification
**Required**: No (optional)
**Values**: `dmz` | `internal` | `restricted` | `management`
**Example**: `internal`

**Use cases**:
- Network segmentation (dmz resources in public subnet, restricted in private)
- Firewall rules (security zone determines allowed traffic)
- Access control (management zone requires VPN/bastion)

---

## Automation Tags

Lifecycle and infrastructure management metadata for automation policies.

### Backup

**Purpose**: Backup policy assignment
**Required**: Recommended (data resources)
**Values**: `continuous` | `hourly` | `daily` | `weekly` | `monthly` | `none`
**Example**: `daily`

**Use cases**:
- AWS Backup: Select resources by Backup tag
- Azure Backup: Assign backup policies by tag
- GCP Cloud Backup: Schedule backups by label
- Snapshot automation: Trigger automated snapshots

**Cost impact**: Daily backups cost more than weekly (storage + API calls)

**Integration**:
```hcl
# AWS Backup plan targeting Backup:daily tag
resource "aws_backup_selection" "daily_backups" {
  plan_id = aws_backup_plan.daily.id

  resources = ["*"]

  condition {
    string_equals = {
      key   = "Backup"
      value = "daily"
    }
  }
}
```

### Monitoring

**Purpose**: Monitoring/observability enablement
**Required**: No (optional)
**Values**: `enabled` | `disabled` | `custom`
**Example**: `enabled`

**Use cases**:
- CloudWatch/Application Insights agent installation
- Metric collection enablement
- Alerting policy assignment
- Cost optimization (disable monitoring for non-critical resources)

### Schedule

**Purpose**: Resource uptime schedule
**Required**: No (cost optimization use case)
**Values**: `always-on` | `business-hours` | `weekdays` | `on-demand`
**Example**: `business-hours`

**Use cases**:
- Automated shutdown of dev/test resources (save 50-70% on compute)
- EC2/VM scheduler (stop overnight, start morning)
- Database instance scaling (reduce size during off-hours)

**Schedule definitions**:
```yaml
always-on:       24/7 uptime (production resources)
business-hours:  8am-6pm weekdays (dev/test environments)
weekdays:        Monday-Friday (weekend shutdown)
on-demand:       Manual start/stop only (cost-sensitive workloads)
```

**Cost savings**: `business-hours` = ~65% reduction vs. `always-on`

### AutoShutdown

**Purpose**: Automated shutdown enablement
**Required**: No (cost optimization)
**Values**: `enabled` | `disabled`
**Example**: `enabled`

**Use cases**:
- Dev/test environment cost reduction
- Lambda/CloudFunction automatic stopping
- Idle resource detection and termination

---

## Operational Tags

Support and change management metadata for operational processes.

### SLA

**Purpose**: Service level agreement tier
**Required**: No (operational maturity)
**Values**: `critical` | `high` | `medium` | `low`
**Example**: `critical`

**Use cases**:
- Incident response prioritization (critical = page on-call)
- Monitoring threshold configuration (critical = tighter thresholds)
- Backup/DR requirements (critical = highest RPO/RTO)
- Support escalation routing

**SLA definitions**:
```yaml
critical: Customer-facing production (RPO < 1h, RTO < 15min)
high:     Internal production services (RPO < 4h, RTO < 1h)
medium:   Non-critical production (RPO < 24h, RTO < 4h)
low:      Development/testing (no SLA guarantee)
```

### ChangeManagement

**Purpose**: Change ticket reference
**Required**: No (change control orgs)
**Format**: `{TICKET_SYSTEM}-{NUMBER}`
**Example**: `CHG-12345` or `JIRA-567`

**Use cases**:
- Audit trail (which change authorized this resource?)
- Rollback reference (revert to pre-change state)
- Compliance requirement (ITIL change management)

### CreatedBy

**Purpose**: User who created resource
**Required**: No (audit trail)
**Format**: Email address or username
**Example**: `john.doe@company.com`

**Use cases**:
- Audit trail (who created this resource?)
- Ownership transfer (contact creator when owner email bounces)
- Security investigation (trace unauthorized resource creation)

**Auto-population**:
- Terraform: `data.aws_caller_identity.current.user_id`
- Azure: `user().principalName`
- Kubernetes: `{{request.userInfo.username}}` (Kyverno auto-inject)

### CreatedDate

**Purpose**: Resource creation timestamp
**Required**: No (lifecycle tracking)
**Format**: ISO 8601 timestamp
**Example**: `2025-12-04T10:30:00Z`

**Use cases**:
- Resource age calculation (identify old resources)
- Lifecycle policies (delete resources older than X days)
- Audit trail (when was this resource created?)

**Auto-population**:
- Terraform: `timestamp()` function
- CloudFormation: `!Ref AWS::StackCreationTime`
- Pulumi: `new Date().toISOString()`

---

## Custom Tags

Organization-specific metadata for unique business requirements.

### Customer

**Purpose**: Multi-tenant customer identifier
**Required**: If multi-tenant SaaS
**Format**: Customer ID or slug
**Example**: `customer-acme-corp`

**Use cases**:
- Cost allocation by customer (SaaS showback)
- Resource isolation (tenant-per-VPC architecture)
- Data residency (customer X requires EU-only resources)
- Access control (customer admins access only their resources)

### Application

**Purpose**: Application name (for multi-app projects)
**Required**: No (if single app per project)
**Format**: Kebab-case app name
**Example**: `payment-api` or `user-service`

**Use cases**:
- Service discovery (find all resources for app X)
- Cost allocation by application
- Dependency mapping (app A depends on app B)
- Rollback isolation (rollback app X without affecting app Y)

### Component

**Purpose**: Resource role within application
**Required**: No (architectural clarity)
**Values**: `web` | `api` | `database` | `cache` | `queue` | `worker`
**Example**: `api`

**Use cases**:
- Architecture diagrams (auto-generate from tags)
- Cost allocation by tier (web tier costs vs. database tier)
- Scaling policies (web tier scales differently than worker tier)
- Monitoring dashboards (group by component)

### Stack

**Purpose**: Full-stack identifier
**Required**: No (microservices architecture)
**Format**: `{app}-{env}-{region}`
**Example**: `ecommerce-prod-us-east-1`

**Use cases**:
- Multi-region deployments (identify region-specific resources)
- Stack-level cost tracking
- Disaster recovery (restore entire stack)

---

## Tag Naming Patterns

### PascalCase (AWS Standard)

**Format**: CapitalizeEachWord
**Example**: `CostCenter`, `ProjectName`, `DataClassification`

**Best for**: AWS-first organizations
**Pros**: AWS console default, most AWS documentation uses PascalCase
**Cons**: Case-sensitive (typos create duplicate tags: `Environment` ≠ `environment`)

### lowercase (GCP Required)

**Format**: alllowercase
**Example**: `costcenter`, `projectname`, `dataclassification`

**Best for**: GCP-first organizations
**Pros**: GCP labels require lowercase (no choice)
**Cons**: Less readable for multi-word tags

### kebab-case (Azure Standard)

**Format**: lowercase-with-hyphens
**Example**: `cost-center`, `project-name`, `data-classification`

**Best for**: Azure-first organizations or multi-cloud consistency
**Pros**: Case-insensitive, highly readable
**Cons**: Hyphens can conflict with some automation tools

### Namespaced (Enterprise Standard)

**Format**: `namespace:key`
**Example**: `company:environment`, `team:owner`, `finance:costcenter`

**Best for**: Large enterprises with multiple organizations/teams
**Pros**: Prevents tag collision between teams, clear ownership
**Cons**: Longer tag keys (counts toward character limits)

**AWS Tag Policies**: Enforce namespaced tags for organizational consistency

---

## Tag Value Standards

### Allowed Characters

| Provider | Key Allowed | Value Allowed | Case Sensitive |
|----------|-------------|---------------|----------------|
| **AWS** | `a-z`, `A-Z`, `0-9`, `+`, `-`, `=`, `.`, `_`, `:`, `/`, `@` | Same | Yes |
| **Azure** | `a-z`, `A-Z`, `0-9`, `-`, `_`, `.` | Same | No |
| **GCP** | `a-z`, `0-9`, `-`, `_` | Same | No |
| **Kubernetes** | `a-z`, `A-Z`, `0-9`, `-`, `_`, `.` | Same | Yes |

**Recommendation**: Use only `a-z`, `0-9`, `-` for maximum portability across providers

### Enumerated Values (Restrict to Allowed List)

Enforce allowed values via policies to prevent typos and sprawl:

**AWS Tag Policy**:
```json
{
  "tags": {
    "Environment": {
      "tag_value": {
        "@@assign": ["prod", "staging", "dev", "test"]
      }
    }
  }
}
```

**Azure Policy** (custom constraint):
```json
{
  "policyRule": {
    "if": {
      "not": {
        "field": "tags['Environment']",
        "in": ["prod", "staging", "dev", "test"]
      }
    },
    "then": {
      "effect": "deny"
    }
  }
}
```

**GCP Organization Policy**:
```yaml
constraint: constraints/gcp.resourceLabels
listPolicy:
  allowedValues:
  - environment:prod
  - environment:staging
  - environment:dev
  - environment:test
```

### Tag Value Patterns (Regex Validation)

Validate tag value formats via policies:

**Example: Owner must be email**:
```yaml
# Azure Policy regex
"pattern": "^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,}$"

# GCP custom constraint
condition: "resource.labels.owner.matches('^[a-z0-9._%+-]+@company\\\\.com$')"
```

**Example: CostCenter must be CC-#### format**:
```yaml
# AWS Config rule parameter
"pattern": "^CC-[0-9]{4}$"
```

---

## Best Practices Summary

1. **Start minimal**: "Big Six" required tags (Name, Environment, Owner, CostCenter, Project, ManagedBy)
2. **Choose ONE naming convention**: PascalCase, lowercase, or kebab-case - enforce organization-wide
3. **Restrict tag values**: Use enums/regex to prevent typos (prod vs. production vs. PROD)
4. **Auto-populate metadata**: Use IaC to auto-set CreatedBy, CreatedDate, ManagedBy
5. **Tag inheritance**: Let parent resources (resource groups, folders) propagate common tags
6. **Validate at creation**: Use policies to block untagged or incorrectly tagged resources
7. **Audit regularly**: Weekly tag compliance checks identify drift and sprawl
8. **Document standards**: Maintain tag dictionary with purpose, values, and examples
