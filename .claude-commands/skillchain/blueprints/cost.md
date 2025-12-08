# Cost Optimization (FinOps) Blueprint

**Version:** 1.0.0
**Last Updated:** 2025-12-06
**Category:** FinOps

---

## Overview

Pre-configured skill chain optimized for implementing cloud cost optimization, FinOps practices, cost allocation, budget management, and resource optimization. This blueprint provides production-ready defaults for the most common cloud cost management patterns, minimizing configuration while maximizing cost visibility and savings.

---

## Trigger Keywords

**Primary (high confidence):**
- finops
- cost optimization
- cloud costs
- cost management
- budget
- spend optimization

**Secondary (medium confidence):**
- tagging
- spend
- savings
- reserved instances
- spot instances
- cost allocation
- budget alerts
- rightsizing
- cost visibility

**Example goals that match:**
- "finops dashboard with cost tracking"
- "cloud cost optimization and tagging strategy"
- "budget management system with alerts"
- "cost allocation by team and project"
- "reserved instance recommendations"
- "multi-cloud cost visibility dashboard"

---

## Skill Chain (Pre-configured)

This blueprint invokes 5 skills in the following order:

```
1. theming-components          (foundation - always required)
2. tagging-resources            (cost allocation foundation)
3. implementing-observability   (cost monitoring & metrics)
4. creating-dashboards          (cost visualization)
5. assembling-components        (final assembly - always required)
```

**Total estimated time:** 20-30 minutes
**Total estimated questions:** 10-15 questions (or 3 with blueprint defaults)

---

## Pre-configured Defaults

### 1. theming-components
```yaml
color_scheme: "finops-green"
  # Professional green-blue palette optimized for cost data
  # Primary: #059669 (green-600) - savings
  # Success: #10B981 (green-500) - under budget
  # Warning: #F59E0B (amber-500) - approaching limit
  # Danger: #EF4444 (red-500) - over budget
  # Info: #3B82F6 (blue-500) - neutral metrics

theme_modes: ["light", "dark"]
  # Both light and dark modes for accessibility
  # Dark mode optimized for extended monitoring sessions

spacing_base: "8px"
  # 8px grid system for consistent component spacing
  # Scale: 4, 8, 12, 16, 24, 32, 48, 64px
```

### 2. tagging-resources
```yaml
tagging_strategy: "hierarchical"
  # Multi-level tagging for granular cost allocation
  # Supports: Organization → Department → Team → Project → Environment

required_tags:
  # Enforce these tags on all resources
  - environment      # dev, staging, prod, test
  - team            # engineering, product, marketing, etc.
  - project         # Project identifier
  - cost_center     # Finance cost center code
  - owner           # Team/person responsible
  - application     # Application name

optional_tags:
  # Recommended but not enforced
  - expiry_date     # For temporary resources
  - backup          # Backup policy
  - compliance      # Compliance requirements
  - data_classification  # Data sensitivity level

tag_validation: true
  # Validate tag format and values
  # Prevent resources without required tags
  # Auto-suggest valid tag values

tag_propagation: true
  # Automatically propagate tags to child resources
  # RDS instance → snapshots, replicas
  # EC2 instance → volumes, snapshots
  # ECS service → tasks

governance_policy: "enforce"
  # Block resource creation without required tags
  # Options: "enforce" (block), "warn" (allow with warning), "audit" (log only)
```

### 3. implementing-observability
```yaml
metrics_collection: "comprehensive"
  # Collect all cost-related metrics
  # Hourly granularity for recent data (14 days)
  # Daily granularity for historical data (12 months)

cost_metrics:
  # Primary cost metrics to track
  - total_spend          # Total cloud spend
  - daily_spend          # Daily spend trend
  - service_spend        # Per-service breakdown
  - tag_spend           # Spend by tag dimension
  - account_spend       # Per-account (multi-account orgs)
  - region_spend        # Per-region breakdown
  - reserved_coverage   # Reserved instance coverage %
  - savings_plans_coverage  # Savings plans coverage %
  - spot_usage          # Spot instance usage %

budget_thresholds:
  # Alert thresholds as percentage of budget
  - 50%   # Early warning
  - 80%   # Approaching limit
  - 100%  # Budget exceeded
  - 120%  # Critical overspend

anomaly_detection: true
  # ML-based cost anomaly detection
  # Alert on unexpected spend increases
  # Configurable sensitivity: low, medium, high
  # Default: medium (alert on >25% deviation)

alert_channels:
  # Where to send cost alerts
  - email           # Email notifications
  - slack           # Slack channel integration
  - pagerduty       # PagerDuty for critical alerts
  - webhook         # Custom webhook endpoint

monitoring_frequency: "hourly"
  # How often to check for anomalies
  # Options: realtime, hourly, daily
  # Realtime requires streaming metrics

retention_policy:
  # How long to retain cost data
  - detailed: 90_days      # Hourly granularity
  - aggregated: 13_months  # Daily granularity
  - summary: 36_months     # Monthly granularity
```

### 4. creating-dashboards
```yaml
layout: "finops-comprehensive"
  # Specialized FinOps dashboard layout
  # Sections: Budget overview, trends, allocation, recommendations, anomalies

kpi_cards: 6
  # Six primary KPI cards in top rows
  # 1. Current month spend
  # 2. Budget remaining
  # 3. Month-over-month change
  # 4. Projected end-of-month spend
  # 5. Total savings (reserved/spot)
  # 6. Cost per unit metric (e.g., cost per user)

responsive: true
  # Automatic reflowing of dashboard components
  # Touch-friendly on mobile devices
  # Optimized spacing for different screen sizes

auto_refresh: true
  # Enable real-time data updates
  # Polling interval: 5 minutes for cost data
  # Instant updates for budget alerts

export_enabled: true
  # Enable CSV/PDF/Excel export
  # Export formats:
  #   - CSV: Raw data for analysis
  #   - PDF: Executive reports
  #   - Excel: Detailed cost breakdowns with pivot tables

time_ranges:
  # Predefined time range filters
  - today
  - yesterday
  - this_week
  - last_week
  - this_month
  - last_month
  - this_quarter
  - last_quarter
  - this_year
  - last_year
  - custom      # Custom date range picker

cost_allocation_views:
  # Different cost allocation perspectives
  - by_service      # AWS service breakdown (EC2, S3, RDS, etc.)
  - by_team         # Team/department breakdown
  - by_project      # Project breakdown
  - by_environment  # Dev/staging/prod breakdown
  - by_region       # Geographic region breakdown
  - by_account      # Multi-account breakdown
  - by_tag          # Custom tag dimension

visualization_types:
  # Charts included in dashboard
  - spend_trend_line       # Line chart: Spend over time
  - service_breakdown_pie  # Pie chart: Spend by service
  - budget_progress_bar    # Progress bars: Budget consumption
  - cost_heatmap          # Heatmap: Spend by day/hour
  - allocation_treemap    # Treemap: Hierarchical cost allocation
  - forecast_area         # Area chart: Projected spend
```

### 5. assembling-components
```yaml
validate_tokens: true
  # Enforce token usage (no hardcoded values)
  # Validate all components reference tokens.css
  # Auto-fix common violations

production_ready: true
  # Include error boundaries
  # Add loading states for all async operations
  # Accessibility compliance (WCAG 2.1 AA)
  # TypeScript types included
  # PropTypes for component validation

file_structure: "feature-based"
  # /finops/components/ (KPI cards, charts, alerts)
  # /finops/policies/ (Tagging policies, governance rules)
  # /finops/monitoring/ (Metrics, dashboards, alerts)
  # /finops/recommendations/ (Optimization suggestions)
  # /finops/reports/ (Cost reports, exports)

integrations:
  # Cloud provider integrations
  - aws_cost_explorer    # AWS Cost Explorer API
  - aws_organizations    # Multi-account management
  - gcp_billing          # GCP Billing API
  - azure_cost_mgmt      # Azure Cost Management API
  - kubernetes_metrics   # K8s cost allocation
```

---

## Quick Questions (Only 3)

When blueprint is detected, ask only these essential questions:

### Question 1: Cloud Provider(s)
```
Which cloud provider(s) are you using?

Options:
1. AWS only
2. GCP only
3. Azure only
4. Multi-cloud (AWS + GCP)
5. Multi-cloud (AWS + Azure)
6. Multi-cloud (all three)

Your answer: _______________
```

**Why this matters:**
- Determines API integrations and data sources
- Affects tagging strategy (providers have different limits)
- Influences cost allocation methods
- Determines which optimization recommendations apply

**Default if skipped:** "AWS only"

---

### Question 2: Primary Cost Concern
```
What is your primary cost optimization goal?

Options:
1. Overall cost reduction (identify waste, rightsizing)
2. Cost allocation visibility (chargeback/showback by team)
3. Budget control (prevent overruns, enforce limits)
4. Reserved capacity optimization (RI/savings plans recommendations)
5. Multi-cloud cost comparison (optimize provider mix)

Your answer: _______________
```

**Why this matters:**
- Determines dashboard focus and primary KPIs
- Affects which recommendations to prioritize
- Influences alert configuration
- Determines report templates

**Default if skipped:** "Overall cost reduction"

---

### Question 3: Organization Size
```
What is your organization size and structure?

Options:
1. Startup (1-10 engineers, single team, <$10k/month spend)
2. Small business (10-50 engineers, 2-5 teams, $10k-$100k/month)
3. Growth company (50-200 engineers, 5-20 teams, $100k-$1M/month)
4. Enterprise (200+ engineers, 20+ teams, $1M+/month spend)
5. Enterprise with FinOps team (dedicated cost optimization team)

Your answer: _______________
```

**Why this matters:**
- Determines governance complexity (simple vs. advanced)
- Affects tagging granularity requirements
- Influences budget allocation strategy
- Determines automation sophistication

**Default if skipped:** "Growth company"

---

## Blueprint Detection Logic

Trigger this blueprint when the user's goal matches:

```python
def should_use_finops_blueprint(goal: str) -> bool:
    goal_lower = goal.lower()

    # Primary keywords (high confidence)
    primary_match = any(keyword in goal_lower for keyword in [
        "finops",
        "cost optimization",
        "cloud cost",
        "cost management",
        "budget",
        "spend optimization"
    ])

    # Secondary keywords + cost-related terms
    secondary_match = (
        any(keyword in goal_lower for keyword in [
            "tagging", "spend", "savings", "reserved", "spot"
        ]) and
        any(keyword in goal_lower for keyword in [
            "cost", "budget", "optimization", "allocation", "monitoring"
        ])
    )

    # Dashboard + cost context
    dashboard_cost_match = (
        "dashboard" in goal_lower and
        any(keyword in goal_lower for keyword in ["cost", "budget", "spend", "finops"])
    )

    return primary_match or secondary_match or dashboard_cost_match
```

**Confidence levels:**
- **High (90%+):** Contains "finops" or "cost optimization"
- **Medium (70-89%):** Contains "budget" or "cost" + "dashboard"/"management"
- **Low (50-69%):** Contains cost-related secondary keywords

**Present blueprint when confidence >= 70%**

---

## Blueprint Offer Message

When blueprint is detected, present this message to the user:

```
┌────────────────────────────────────────────────────────────┐
│ 💰 FINOPS BLUEPRINT DETECTED                               │
├────────────────────────────────────────────────────────────┤
│ Your goal matches our optimized FinOps Blueprint!         │
│                                                            │
│ Pre-configured features:                                   │
│  ✓ Hierarchical tagging strategy (6 required tags)        │
│  ✓ Budget alerts (50%, 80%, 100% thresholds)              │
│  ✓ Cost allocation dashboard (6 KPI metrics)              │
│  ✓ Anomaly detection (ML-based spend alerts)              │
│  ✓ Multi-cloud support (AWS, GCP, Azure)                  │
│  ✓ Reserved instance recommendations                       │
│  ✓ Chargeback reports by team/project                     │
│  ✓ Export to CSV/PDF/Excel                                │
│                                                            │
│ Using blueprint reduces questions from 15 to 3!           │
│                                                            │
│ Options:                                                   │
│  1. Use blueprint (3 quick questions, ~10 min)            │
│  2. Custom configuration (15 questions, ~35 min)          │
│  3. Skip all questions (use all defaults, ~5 min)         │
│                                                            │
│ Your choice (1/2/3): _____                                │
└────────────────────────────────────────────────────────────┘
```

**Handle responses:**
- **1 or "blueprint"** → Ask only 3 blueprint questions
- **2 or "custom"** → Ask all skill questions (normal flow)
- **3 or "skip"** → Use all defaults, skip all questions

---

## Generated Output Structure

When blueprint is executed, generate this file structure:

```
finops-project/
├── infrastructure/
│   ├── tagging/
│   │   ├── tag-policies.yaml          # Tag validation rules
│   │   ├── required-tags.yaml         # Required tag definitions
│   │   ├── tag-values.yaml            # Valid tag value enumerations
│   │   ├── tag-governance.tf          # Terraform tag enforcement
│   │   ├── tag-compliance-check.py    # Tag compliance scanner script
│   │   └── auto-tagger.py             # Automatic tag propagation script
│   │
│   ├── budgets/
│   │   ├── budget-definitions.yaml    # Budget limits by team/project
│   │   ├── alert-rules.yaml           # Budget alert configurations
│   │   ├── budget-terraform.tf        # Terraform budget resources
│   │   └── budget-enforcer.py         # Budget enforcement script
│   │
│   ├── policies/
│   │   ├── cost-policies.yaml         # Cost optimization policies
│   │   ├── resource-limits.yaml       # Resource size/type restrictions
│   │   ├── reserved-instance.yaml     # RI purchase policies
│   │   ├── spot-instance.yaml         # Spot usage policies
│   │   └── lifecycle-policies.yaml    # Resource lifecycle rules
│   │
│   └── monitoring/
│       ├── cost-metrics.yaml          # Cost metric definitions
│       ├── anomaly-detection.yaml     # Anomaly detection config
│       ├── alert-channels.yaml        # Alert routing configuration
│       └── dashboards.yaml            # Dashboard configurations
│
├── src/
│   ├── tokens.css                     # Design tokens (ALWAYS FIRST)
│   │   # CSS custom properties for colors, spacing, typography
│   │   # FinOps-specific color scheme (green = savings, red = overspend)
│   │
│   ├── components/
│   │   ├── finops/
│   │   │   ├── FinOpsDashboard.tsx    # Main FinOps dashboard container
│   │   │   ├── BudgetOverview.tsx     # Budget status and alerts
│   │   │   ├── CostTrendChart.tsx     # Spend trend visualization
│   │   │   ├── CostAllocation.tsx     # Cost allocation by dimension
│   │   │   ├── Recommendations.tsx    # Optimization recommendations
│   │   │   ├── AnomalyAlerts.tsx      # Cost anomaly notifications
│   │   │   ├── TagCompliance.tsx      # Tagging compliance dashboard
│   │   │   └── ReservedInstanceRecs.tsx # RI/Savings Plans recommendations
│   │   │
│   │   ├── kpis/
│   │   │   ├── CurrentSpendCard.tsx   # Current month spend
│   │   │   ├── BudgetRemainingCard.tsx # Budget remaining
│   │   │   ├── MoMChangeCard.tsx      # Month-over-month change
│   │   │   ├── ForecastCard.tsx       # Projected spend
│   │   │   ├── SavingsCard.tsx        # Total savings
│   │   │   └── CostPerUnitCard.tsx    # Cost per unit metric
│   │   │
│   │   ├── charts/
│   │   │   ├── SpendTrendLine.tsx     # Line chart: Spend over time
│   │   │   ├── ServiceBreakdownPie.tsx # Pie chart: Spend by service
│   │   │   ├── BudgetProgressBar.tsx  # Progress bar: Budget consumption
│   │   │   ├── CostHeatmap.tsx        # Heatmap: Spend by day/hour
│   │   │   ├── AllocationTreemap.tsx  # Treemap: Hierarchical allocation
│   │   │   ├── ForecastArea.tsx       # Area chart: Projected spend
│   │   │   └── SavingsOpportunities.tsx # Bar chart: Savings opportunities
│   │   │
│   │   ├── filters/
│   │   │   ├── TimeRangeFilter.tsx    # Date range selector
│   │   │   ├── ServiceFilter.tsx      # Cloud service filter
│   │   │   ├── TeamFilter.tsx         # Team/department filter
│   │   │   ├── ProjectFilter.tsx      # Project filter
│   │   │   ├── EnvironmentFilter.tsx  # Environment filter
│   │   │   └── TagFilter.tsx          # Custom tag filter
│   │   │
│   │   ├── reports/
│   │   │   ├── ChargebackReport.tsx   # Team chargeback report
│   │   │   ├── ShowbackReport.tsx     # Cost allocation showback
│   │   │   ├── ExecutiveSummary.tsx   # Executive summary report
│   │   │   ├── DetailedCostReport.tsx # Detailed line-item report
│   │   │   └── ExportButton.tsx       # CSV/PDF/Excel export
│   │   │
│   │   └── alerts/
│   │       ├── BudgetAlert.tsx        # Budget threshold alert
│   │       ├── AnomalyAlert.tsx       # Cost anomaly alert
│   │       ├── TagComplianceAlert.tsx # Tag compliance alert
│   │       └── AlertManager.tsx       # Alert orchestration
│   │
│   ├── hooks/
│   │   ├── useCostData.ts             # Cost data fetching hook
│   │   ├── useBudgetStatus.ts         # Budget status hook
│   │   ├── useTagCompliance.ts        # Tag compliance hook
│   │   ├── useRecommendations.ts      # Optimization recommendations hook
│   │   ├── useAnomalyDetection.ts     # Anomaly detection hook
│   │   ├── useCostAllocation.ts       # Cost allocation hook
│   │   └── useExportReport.ts         # Report export hook
│   │
│   ├── services/
│   │   ├── aws/
│   │   │   ├── costExplorer.ts        # AWS Cost Explorer API client
│   │   │   ├── budgets.ts             # AWS Budgets API client
│   │   │   ├── organizations.ts       # AWS Organizations API client
│   │   │   └── recommendationsEngine.ts # AWS RI recommendations
│   │   │
│   │   ├── gcp/
│   │   │   ├── billing.ts             # GCP Billing API client
│   │   │   ├── budgets.ts             # GCP Budget API client
│   │   │   └── recommender.ts         # GCP Recommender API client
│   │   │
│   │   ├── azure/
│   │   │   ├── costManagement.ts      # Azure Cost Management API
│   │   │   ├── budgets.ts             # Azure Budget API
│   │   │   └── advisor.ts             # Azure Advisor API client
│   │   │
│   │   └── aggregator/
│   │       ├── multiCloudCosts.ts     # Multi-cloud cost aggregation
│   │       └── normalizer.ts          # Cross-cloud data normalization
│   │
│   ├── utils/
│   │   ├── costCalculations.ts        # Cost calculation utilities
│   │   ├── budgetMath.ts              # Budget math functions
│   │   ├── tagValidation.ts           # Tag validation logic
│   │   ├── anomalyDetection.ts        # Anomaly detection algorithms
│   │   ├── forecasting.ts             # Cost forecasting algorithms
│   │   ├── formatters.ts              # Currency/number formatting
│   │   └── exportHelpers.ts           # Report export utilities
│   │
│   ├── types/
│   │   ├── cost.ts                    # Cost data types
│   │   ├── budget.ts                  # Budget types
│   │   ├── tag.ts                     # Tag types
│   │   ├── recommendation.ts          # Recommendation types
│   │   ├── alert.ts                   # Alert types
│   │   └── report.ts                  # Report types
│   │
│   ├── data/
│   │   ├── mockCostData.ts            # Sample cost data
│   │   ├── mockBudgets.ts             # Sample budget data
│   │   ├── mockRecommendations.ts     # Sample recommendations
│   │   └── tagSchemas.ts              # Tag schema definitions
│   │
│   ├── App.tsx                        # Root application component
│   ├── main.tsx                       # Application entry point
│   └── index.css                      # Global styles (imports tokens.css)
│
├── scripts/
│   ├── tag-compliance-scanner.py      # Scan resources for tag compliance
│   ├── cost-anomaly-detector.py       # Detect cost anomalies
│   ├── ri-optimizer.py                # Reserved instance optimizer
│   ├── spot-analyzer.py               # Spot instance opportunity analyzer
│   ├── budget-projector.py            # Budget projection calculator
│   ├── chargeback-generator.py        # Generate chargeback reports
│   └── multi-cloud-consolidator.py    # Consolidate multi-cloud costs
│
├── docs/
│   ├── TAGGING_STRATEGY.md            # Tagging strategy documentation
│   ├── BUDGET_POLICIES.md             # Budget policy documentation
│   ├── COST_ALLOCATION_GUIDE.md       # Cost allocation guide
│   ├── OPTIMIZATION_PLAYBOOK.md       # Cost optimization playbook
│   └── ALERT_RUNBOOK.md               # Alert response runbook
│
├── package.json                       # Dependencies and scripts
├── tsconfig.json                      # TypeScript configuration
├── vite.config.ts                     # Vite build configuration
└── README.md                          # Setup and usage instructions
```

---

## Component Architecture

### Cost Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                   FinOpsDashboard                           │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Multi-Cloud Cost Aggregator                           │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐            │ │
│  │  │   AWS    │  │   GCP    │  │  Azure   │            │ │
│  │  │ Cost API │  │ Cost API │  │ Cost API │            │ │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘            │ │
│  │       └────────────┬┴────────────┘                    │ │
│  │                    ▼                                   │ │
│  │          Cost Data Normalizer                         │ │
│  │          (Unified cost format)                        │ │
│  └────────────────────┬──────────────────────────────────┘ │
│                       │                                     │
│  ┌────────────────────▼──────────────────┐                 │
│  │ Cost Processing Pipeline              │                │
│  │  - Tag-based allocation               │                │
│  │  - Budget tracking                    │                │
│  │  - Anomaly detection                  │                │
│  │  - Forecasting                        │                │
│  │  - Recommendations                    │                │
│  └────────────────────┬──────────────────┘                 │
│                       │                                     │
│       ┌───────────────┴───────────────┐                    │
│       │                               │                    │
│  ┌────▼────────┐              ┌───────▼──────┐            │
│  │ Dashboard   │              │ Alert System │            │
│  │ Components  │              │              │            │
│  │             │              │ - Budget     │            │
│  │ ┌─────────┐ │              │ - Anomaly    │            │
│  │ │ KPI Grid│ │              │ - Tag        │            │
│  │ │ (6 KPIs)│ │              │              │            │
│  │ └─────────┘ │              └──────────────┘            │
│  │             │                                           │
│  │ ┌─────────┐ │                                           │
│  │ │ Spend   │ │                                           │
│  │ │ Trend   │ │                                           │
│  │ └─────────┘ │                                           │
│  │             │                                           │
│  │ ┌─────────┐ │                                           │
│  │ │ Cost    │ │                                           │
│  │ │Allocation│ │                                           │
│  │ └─────────┘ │                                           │
│  │             │                                           │
│  │ ┌─────────┐ │                                           │
│  │ │ Recomm- │ │                                           │
│  │ │endations│ │                                           │
│  │ └─────────┘ │                                           │
│  └─────────────┘                                           │
└─────────────────────────────────────────────────────────────┘
```

### Tagging Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 Resource Tagging Flow                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  New Resource Created                                   │
│         │                                               │
│         ▼                                               │
│  ┌──────────────────┐                                   │
│  │ Tag Validation   │                                   │
│  │ - Required tags? │                                   │
│  │ - Valid values?  │                                   │
│  └────────┬─────────┘                                   │
│           │                                             │
│    ┌──────┴──────┐                                      │
│    │             │                                      │
│  PASS          FAIL                                     │
│    │             │                                      │
│    ▼             ▼                                      │
│  Allow     ┌─────────────┐                             │
│            │ Governance  │                             │
│            │   Action    │                             │
│            ├─────────────┤                             │
│            │ Enforce:    │                             │
│            │  - Block    │                             │
│            │            │                             │
│            │ Warn:       │                             │
│            │  - Allow    │                             │
│            │  + Alert    │                             │
│            │            │                             │
│            │ Audit:      │                             │
│            │  - Allow    │                             │
│            │  + Log      │                             │
│            └─────────────┘                             │
│                                                         │
│  ┌──────────────────────────────────────┐              │
│  │ Tag Propagation (if enabled)         │              │
│  │  - EC2 → EBS volumes, snapshots      │              │
│  │  - RDS → Snapshots, replicas         │              │
│  │  - Auto Scaling → Instances          │              │
│  └──────────────────────────────────────┘              │
│                                                         │
│  ┌──────────────────────────────────────┐              │
│  │ Cost Allocation Tags                 │              │
│  │  - Activate in billing console       │              │
│  │  - Enable in Cost Explorer           │              │
│  │  - Propagate to reports              │              │
│  └──────────────────────────────────────┘              │
└─────────────────────────────────────────────────────────┘
```

---

## Default Budgets and Alerts

### Budget Configuration

```yaml
# Budget definitions (per organization size)
budgets:
  startup:
    monthly_limit: 10000  # $10k
    thresholds: [50, 80, 100]
    auto_actions: []  # No automated shutdown

  small_business:
    monthly_limit: 50000  # $50k
    thresholds: [50, 80, 100, 120]
    auto_actions:
      - type: "notify_owner"
        threshold: 100
      - type: "require_approval"
        threshold: 120

  growth_company:
    monthly_limit: 500000  # $500k
    thresholds: [50, 80, 100]
    auto_actions:
      - type: "notify_owner"
        threshold: 80
      - type: "notify_executives"
        threshold: 100
      - type: "throttle_non_prod"
        threshold: 120

  enterprise:
    monthly_limit: 5000000  # $5M
    thresholds: [50, 80, 90, 100, 110]
    auto_actions:
      - type: "notify_finops_team"
        threshold: 80
      - type: "executive_alert"
        threshold: 100
      - type: "freeze_new_resources"
        threshold: 110
```

### Alert Rules

```yaml
# Cost anomaly alerts
anomalies:
  sensitivity: "medium"  # low, medium, high
  thresholds:
    low: 50%      # Alert on >50% deviation
    medium: 25%   # Alert on >25% deviation (default)
    high: 10%     # Alert on >10% deviation

  evaluation_period: "7_days"  # Compare to past 7 days
  minimum_spend: 100  # Only alert if daily spend > $100

# Tag compliance alerts
tag_compliance:
  scan_frequency: "daily"
  alert_on:
    - missing_required_tags
    - invalid_tag_values
    - untagged_resources_cost_threshold: 1000  # Alert if >$1k untagged

# Budget alerts
budget_alerts:
  channels:
    50%:
      - email: "team-lead@company.com"
      - slack: "#finops-alerts"
    80%:
      - email: "team-lead@company.com"
      - email: "finance@company.com"
      - slack: "#finops-alerts"
      - pagerduty: "finops-team"
    100%:
      - email: "team-lead@company.com"
      - email: "finance@company.com"
      - email: "cfo@company.com"
      - slack: "#finops-critical"
      - pagerduty: "finops-team"
      - webhook: "https://company.com/budget-exceeded"
```

---

## Cost Optimization Recommendations

### Recommendation Engine

The blueprint includes an optimization recommendation engine that analyzes:

```yaml
recommendation_categories:
  1. rightsizing:
      # Underutilized resources
      - ec2_cpu_utilization < 20%
      - rds_connections < 10% capacity
      - ebs_iops_utilization < 30%
      recommendation: "Downsize or terminate"
      potential_savings: "30-70%"

  2. reserved_capacity:
      # On-demand instances eligible for RI/Savings Plans
      - running_time > 70% per month
      - predictable workloads
      recommendation: "Purchase reserved capacity"
      potential_savings: "30-50%"

  3. spot_instances:
      # Fault-tolerant workloads
      - batch_processing
      - ci_cd_pipelines
      - development_environments
      recommendation: "Use spot instances"
      potential_savings: "60-90%"

  4. storage_optimization:
      # Inefficient storage usage
      - old_snapshots > 90_days
      - unattached_volumes
      - s3_infrequent_access
      recommendation: "Lifecycle policies, cleanup, tiering"
      potential_savings: "20-80%"

  5. network_optimization:
      # Expensive data transfer
      - cross_region_traffic
      - cross_az_traffic
      - public_internet_egress
      recommendation: "VPC endpoints, CloudFront, region consolidation"
      potential_savings: "40-60%"

  6. idle_resources:
      # Unused resources
      - stopped_instances_with_volumes
      - unused_load_balancers
      - idle_nat_gateways
      recommendation: "Delete unused resources"
      potential_savings: "100%"
```

---

## Default KPI Metrics

### Primary KPIs (6 cards)

```typescript
interface CostKPI {
  id: string;
  label: string;
  value: number;
  format: 'currency' | 'percentage' | 'number';
  change: number;
  changeType: 'increase' | 'decrease';
  status: 'good' | 'warning' | 'critical';
  icon: string;
}

const defaultCostKPIs: CostKPI[] = [
  {
    id: 'current_spend',
    label: 'Current Month Spend',
    value: 42350,
    format: 'currency',
    change: 8.5,
    changeType: 'increase',
    status: 'warning',  // Over historical average
    icon: 'dollar-sign'
  },
  {
    id: 'budget_remaining',
    label: 'Budget Remaining',
    value: 7650,
    format: 'currency',
    change: -15,  // Decreasing (expected)
    changeType: 'decrease',
    status: 'warning',  // 85% consumed
    icon: 'trending-down'
  },
  {
    id: 'mom_change',
    label: 'Month-over-Month Change',
    value: 12.3,
    format: 'percentage',
    change: 4.2,
    changeType: 'increase',
    status: 'critical',  // Growing faster than revenue
    icon: 'arrow-up'
  },
  {
    id: 'projected_spend',
    label: 'Projected Month-End Spend',
    value: 52100,
    format: 'currency',
    change: 4.2,
    changeType: 'increase',
    status: 'critical',  // Will exceed budget ($50k)
    icon: 'trending-up'
  },
  {
    id: 'total_savings',
    label: 'Total Savings (RI + Spot)',
    value: 8420,
    format: 'currency',
    change: 15.7,
    changeType: 'increase',
    status: 'good',  // Savings growing
    icon: 'piggy-bank'
  },
  {
    id: 'cost_per_user',
    label: 'Cost per Active User',
    value: 4.23,
    format: 'currency',
    change: -2.1,
    changeType: 'decrease',
    status: 'good',  // Efficiency improving
    icon: 'users'
  }
];
```

---

## Sample Cost Data

### Monthly Spend Trend

```typescript
const monthlySpendData = [
  { month: 'Jan', spend: 38500, budget: 50000, forecast: 38500 },
  { month: 'Feb', spend: 41200, budget: 50000, forecast: 41200 },
  { month: 'Mar', spend: 39800, budget: 50000, forecast: 39800 },
  { month: 'Apr', spend: 42100, budget: 50000, forecast: 42100 },
  { month: 'May', spend: 44300, budget: 50000, forecast: 44300 },
  { month: 'Jun', spend: 42350, budget: 50000, forecast: 52100 }  // Projected
];
```

### Service Breakdown

```typescript
const serviceBreakdownData = [
  { service: 'EC2', spend: 18500, percentage: 43.7 },
  { service: 'RDS', spend: 8200, percentage: 19.4 },
  { service: 'S3', spend: 6100, percentage: 14.4 },
  { service: 'CloudFront', spend: 4200, percentage: 9.9 },
  { service: 'Lambda', spend: 2800, percentage: 6.6 },
  { service: 'Other', spend: 2550, percentage: 6.0 }
];
```

### Cost by Team

```typescript
const teamAllocationData = [
  { team: 'Engineering', spend: 22500, budget: 28000, percentage: 80.4 },
  { team: 'Product', spend: 8900, budget: 10000, percentage: 89.0 },
  { team: 'Data Science', spend: 6200, budget: 7000, percentage: 88.6 },
  { team: 'Marketing', spend: 3100, budget: 4000, percentage: 77.5 },
  { team: 'Shared', spend: 1650, budget: 1000, percentage: 165.0 }  // Over budget
];
```

---

## Dependencies

The blueprint includes these npm packages:

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "recharts": "^2.10.0",              // Charts
    "date-fns": "^2.30.0",              // Date formatting
    "clsx": "^2.0.0",                   // Conditional classnames
    "papaparse": "^5.4.1",              // CSV export
    "jspdf": "^2.5.1",                  // PDF export
    "jspdf-autotable": "^3.7.0",        // PDF table generation
    "xlsx": "^0.18.5"                   // Excel export
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@types/papaparse": "^5.3.0",
    "typescript": "^5.2.0",
    "vite": "^5.0.0",
    "@vitejs/plugin-react": "^4.2.0",
    "aws-sdk": "^2.1500.0",             // AWS SDK (cost APIs)
    "@google-cloud/billing": "^4.2.0",  // GCP Billing API
    "@azure/arm-costmanagement": "^1.2.0", // Azure Cost API
    "terraform": "^1.6.0"               // Infrastructure as Code
  }
}
```

**Cloud provider SDKs** (installed based on Q1 answer):
- AWS: `aws-sdk` (~40MB) - Cost Explorer, Budgets, Organizations APIs
- GCP: `@google-cloud/billing` (~8MB) - Cloud Billing API
- Azure: `@azure/arm-costmanagement` (~5MB) - Cost Management API

---

## Tagging Strategy Details

### Required Tags (6)

```yaml
environment:
  description: "Deployment environment"
  values: ["dev", "staging", "prod", "test", "sandbox"]
  required: true
  case_sensitive: false

team:
  description: "Owning team or department"
  values: ["engineering", "product", "data", "marketing", "infrastructure", "security"]
  required: true
  case_sensitive: false

project:
  description: "Project identifier"
  pattern: "^[a-z0-9-]+$"  # Lowercase alphanumeric with hyphens
  required: true
  max_length: 50

cost_center:
  description: "Finance cost center code"
  pattern: "^CC-[0-9]{4}$"  # Format: CC-1234
  required: true
  examples: ["CC-1001", "CC-1002"]

owner:
  description: "Team or person responsible for resource"
  pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"  # Email format
  required: true
  examples: ["team-platform@company.com", "john.doe@company.com"]

application:
  description: "Application or service name"
  pattern: "^[a-z0-9-]+$"
  required: true
  max_length: 50
  examples: ["user-service", "payment-api", "web-app"]
```

### Optional Tags (4)

```yaml
expiry_date:
  description: "Date when resource should be deleted (for temporary resources)"
  pattern: "^\\d{4}-\\d{2}-\\d{2}$"  # Format: YYYY-MM-DD
  required: false
  auto_actions: true  # Auto-delete after expiry

backup:
  description: "Backup retention policy"
  values: ["daily", "weekly", "monthly", "none"]
  required: false
  default: "none"

compliance:
  description: "Compliance requirements"
  values: ["pci", "hipaa", "sox", "gdpr", "none"]
  required: false
  multi_value: true  # Can have multiple compliance requirements

data_classification:
  description: "Data sensitivity level"
  values: ["public", "internal", "confidential", "restricted"]
  required: false
  default: "internal"
```

---

## Governance Policies

### Tag Enforcement Levels

```yaml
governance:
  mode: "enforce"  # Options: enforce, warn, audit

  enforcement:
    description: "Block resource creation without required tags"
    applies_to:
      - ec2_instances
      - rds_instances
      - s3_buckets
      - lambda_functions
      - dynamodb_tables
      - ebs_volumes
      - elastic_ips
    exception_principals: []  # No exceptions by default

  warnings:
    description: "Allow creation but send alerts"
    alert_channels:
      - email: "finops-team@company.com"
      - slack: "#tag-compliance"

  audit:
    description: "Log all tag violations"
    retention_days: 90
    compliance_reports: "weekly"
```

---

## Budget Management Features

### Budget Hierarchy

```yaml
# Multi-level budget structure
budgets:
  organizational:
    total: 5000000  # $5M total org budget
    alert_thresholds: [80, 90, 100]

  departmental:
    - name: "Engineering"
      budget: 3000000  # $3M (60% of org budget)
      teams:
        - name: "Platform"
          budget: 1200000
        - name: "Product"
          budget: 1000000
        - name: "Data"
          budget: 800000

    - name: "Operations"
      budget: 1500000
      teams:
        - name: "Infrastructure"
          budget: 1000000
        - name: "Security"
          budget: 500000

    - name: "R&D"
      budget: 500000

  project_based:
    - name: "Project Alpha"
      budget: 250000
      duration: "3 months"
      auto_alerts: true

    - name: "Project Beta"
      budget: 150000
      duration: "2 months"
      auto_alerts: true
```

---

## Accessibility Features

All FinOps dashboard components include:

- **Keyboard navigation:** Tab order, focus indicators, keyboard shortcuts
- **Screen reader support:** ARIA labels, roles, live regions for cost alerts
- **Color contrast:** WCAG 2.1 AA compliance (4.5:1 for text)
- **Semantic HTML:** Proper heading hierarchy, landmark regions
- **Focus management:** Trapped focus in modals, skip links
- **Reduced motion:** Respects `prefers-reduced-motion` media query
- **High contrast mode:** Enhanced visibility for budget/cost data

---

## Performance Optimizations

- **Cost data caching:** Cache cost data for 5 minutes (reduce API calls)
- **Lazy loading:** Defer loading detailed reports until requested
- **Data pagination:** Load cost line items in batches (100 per page)
- **Memoization:** React.memo for expensive chart components
- **Debounced filters:** Date range/tag filters with 500ms debounce
- **Optimized queries:** Query only necessary date ranges and dimensions
- **Background refresh:** Refresh cost data in background without blocking UI

---

## Testing Recommendations

Include these test files:

```
tests/
├── components/
│   ├── BudgetOverview.test.tsx      # Budget status display tests
│   ├── CostTrendChart.test.tsx      # Chart rendering tests
│   ├── TagCompliance.test.tsx       # Tag validation tests
│   └── Recommendations.test.tsx     # Optimization recommendation tests
│
├── hooks/
│   ├── useCostData.test.ts          # Cost data fetching tests
│   ├── useBudgetStatus.test.ts      # Budget calculation tests
│   └── useAnomalyDetection.test.ts  # Anomaly detection tests
│
├── utils/
│   ├── costCalculations.test.ts     # Cost math tests
│   ├── tagValidation.test.ts        # Tag validation logic tests
│   └── forecasting.test.ts          # Cost forecasting tests
│
└── integration/
    ├── FinOpsFlow.test.tsx          # End-to-end FinOps workflow tests
    └── MultiCloudIntegration.test.tsx # Multi-cloud cost aggregation tests
```

**Test coverage targets:**
- Components: 80%+
- Hooks: 90%+
- Utils: 95%+
- Critical paths (budgets, alerts): 100%

---

## Customization Points

After blueprint generation, users can easily customize:

1. **Tag strategy:** Edit `tag-policies.yaml` to add/modify required tags
2. **Budget thresholds:** Modify `budget-definitions.yaml` alert levels
3. **Alert channels:** Update `alert-channels.yaml` with Slack/email/PagerDuty webhooks
4. **Cost allocation views:** Add custom tag dimensions in dashboard config
5. **Color scheme:** Edit `tokens.css` to match brand (keep semantic meaning)
6. **Recommendations:** Tune recommendation engine sensitivity in config
7. **Data sources:** Replace mock data with real cloud provider APIs

---

## Migration Path

If user starts with blueprint but needs advanced features later:

1. **Add chargeback automation:** Integrate with invoicing/accounting systems
2. **Add commitment planning:** Build RI/Savings Plans purchase workflow
3. **Add forecasting ML:** Integrate ML-based cost forecasting models
4. **Add resource scheduling:** Auto-start/stop dev resources on schedule
5. **Add showback analytics:** Advanced analytics for internal cost visibility
6. **Add carbon tracking:** Integrate carbon emissions tracking

All additions will integrate with existing tagging and cost allocation infrastructure.

---

## Version History

**1.0.0** (2025-12-06)
- Initial FinOps blueprint
- 5-skill chain with optimized defaults
- 3-question quick configuration
- Multi-cloud support (AWS, GCP, Azure)
- Hierarchical tagging strategy (6 required tags)
- Budget management with 3-tier alerts
- ML-based anomaly detection
- Chargeback/showback reporting
- Reserved instance recommendations
- Full accessibility support

---

## Related Blueprints

- **Dashboard Blueprint:** For general analytics dashboards
- **Monitoring Blueprint:** For system/application monitoring
- **Compliance Blueprint:** For compliance and audit reporting
- **Data Pipeline Blueprint:** For cost data ETL and warehousing

---

**Blueprint Complete**
