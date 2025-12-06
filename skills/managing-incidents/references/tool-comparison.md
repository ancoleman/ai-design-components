# Incident Management Tool Comparison


## Table of Contents

- [Overview](#overview)
- [Platform Comparison Matrix](#platform-comparison-matrix)
- [Detailed Platform Reviews](#detailed-platform-reviews)
  - [PagerDuty](#pagerduty)
  - [Opsgenie](#opsgenie)
  - [incident.io](#incidentio)
  - [Splunk On-Call (formerly VictorOps)](#splunk-on-call-formerly-victorops)
- [Decision Framework](#decision-framework)
  - [By Team Size](#by-team-size)
  - [By Budget](#by-budget)
  - [By Existing Stack](#by-existing-stack)
  - [By Use Case](#by-use-case)
- [Status Page Solutions](#status-page-solutions)
  - [Statuspage.io (Atlassian)](#statuspageio-atlassian)
  - [Instatus](#instatus)
  - [Custom Status Page (Self-Hosted)](#custom-status-page-self-hosted)
- [Integration Patterns](#integration-patterns)
  - [Monitoring → Incident Management](#monitoring-incident-management)
  - [Incident Management → Communication](#incident-management-communication)
  - [Incident Management → Status Page](#incident-management-status-page)
- [Migration Considerations](#migration-considerations)
  - [Migrating Between Platforms](#migrating-between-platforms)
- [Open Source Alternatives](#open-source-alternatives)
  - [Alertmanager (Prometheus)](#alertmanager-prometheus)
  - [Grafana OnCall](#grafana-oncall)
- [Recommended Starter Stacks](#recommended-starter-stacks)
  - [Budget-Conscious Stack ($500/month)](#budget-conscious-stack-500month)
  - [Enterprise Stack ($2,000+/month)](#enterprise-stack-2000month)
  - [Atlassian-Centric Stack](#atlassian-centric-stack)
- [Further Reading](#further-reading)

## Overview

Selecting the right incident management platform depends on team size, budget, existing tooling, and organizational needs. This guide compares leading platforms and provides decision frameworks.

---

## Platform Comparison Matrix

| Feature | PagerDuty | Opsgenie | incident.io | Splunk On-Call |
|---------|-----------|----------|-------------|----------------|
| **Best For** | Enterprise | Atlassian Users | Modern Teams | Splunk Users |
| **Team Size** | 10-1000+ | 5-500 | 5-200 | 20-500 |
| **Price Range** | $19-41/user/mo | $9-29/user/mo | Contact Sales | Splunk Bundle |
| **Integrations** | 700+ | 200+ | 100+ | 300+ (Splunk focus) |
| **AIOps** | Advanced | Basic | AI-Powered | Moderate |
| **Slack Integration** | Good | Good | Excellent | Good |
| **API Quality** | Excellent | Good | Good | Moderate |
| **Mobile App** | Excellent | Excellent | Good | Good |
| **Status Page** | Add-on | Separate (Statuspage.io) | Integrated | Separate |
| **Post-Mortem** | Add-on | Manual | Integrated | Manual |
| **Runbook Automation** | Yes | Yes | Limited | Yes |
| **Learning Curve** | Steep | Moderate | Easy | Moderate |
| **Terraform Support** | Excellent (976 snippets) | Good | Limited | Moderate |

---

## Detailed Platform Reviews

### PagerDuty

**Overview:** Market leader, most mature platform, extensive integrations.

**Strengths:**
- **700+ Integrations:** Datadog, Prometheus, AWS CloudWatch, New Relic, Splunk, and more
- **AIOps:** Intelligent event grouping, noise reduction, anomaly detection
- **Mature Platform:** Battle-tested by Fortune 500 companies
- **Terraform Provider:** Infrastructure-as-code support (Context7: 976 code snippets)
- **Comprehensive API:** Full automation capabilities (Context7: 208 code snippets, Benchmark 35.2)
- **Advanced Escalation:** Complex multi-team escalation policies
- **Analytics:** Detailed incident metrics and reporting
- **Incident Response:** Runbook automation, status updates, stakeholder management

**Weaknesses:**
- **Cost:** Most expensive option ($19-41/user/month)
- **Complexity:** Feature-rich but steep learning curve (can overwhelm small teams)
- **Vendor Lock-In:** Deep integrations make migration difficult

**Pricing Tiers:**
- **Starter:** $19/user/month (basic on-call, simple escalation)
- **Professional:** $41/user/month (AIOps, advanced escalation, Slack integration)
- **Business:** Custom pricing (enterprise features, SSO, audit logs)

**When to Choose PagerDuty:**
- Team size: 10+ engineers
- Budget: $500+/month
- Need: Complex multi-team escalations, extensive third-party integrations
- Infrastructure: Multi-cloud, microservices, complex dependencies
- Existing stack: Already using Datadog, AWS, New Relic

**Resources:**
- Context7: `/pagerduty/terraform-provider-pagerduty` (High reputation, 976 snippets)
- Context7: `/websites/developer_pagerduty_api-reference` (High reputation, Benchmark 35.2)
- Documentation: https://developer.pagerduty.com/

---

### Opsgenie

**Overview:** Atlassian product, flexible routing, more affordable than PagerDuty.

**Strengths:**
- **Atlassian Integration:** Seamless with Jira, Confluence, Bitbucket, Trello
- **Flexible Routing:** Advanced on-call scheduling, custom routing rules
- **Cost:** More affordable than PagerDuty ($9-29/user/month)
- **Mobile App:** Excellent iOS/Android experience with push notifications
- **Automation:** Strong workflow automation (create Jira tickets, run scripts)
- **Heartbeat Monitoring:** Built-in uptime monitoring
- **Stakeholder Notifications:** Custom alert policies for non-technical stakeholders

**Weaknesses:**
- **Fewer Integrations:** Less extensive than PagerDuty (200+ vs 700+)
- **AIOps:** Less mature than PagerDuty's AI features
- **Terraform Support:** Good but less mature than PagerDuty

**Pricing Tiers:**
- **Free:** Up to 5 users (basic alerting, on-call schedules)
- **Standard:** $9/user/month (integrations, escalations, mobile app)
- **Enterprise:** $29/user/month (advanced automation, SSO, audit logs)

**When to Choose Opsgenie:**
- Already using Atlassian products (Jira, Confluence)
- Budget: $200-500/month
- Need: Custom routing rules, flexible schedules, Jira integration
- Team size: 5-50 engineers
- Workflow: Heavy Jira usage for incident tracking

**Resources:**
- Documentation: https://docs.opsgenie.com/
- Terraform Provider: https://registry.terraform.io/providers/opsgenie/opsgenie

---

### incident.io

**Overview:** Modern platform, AI-powered response, Slack-native workflow.

**Strengths:**
- **AI-Powered:** Autonomous investigation, pattern detection, faster resolution
- **Slack-Native:** Deep Slack integration, incident channels, slash commands
- **Modern UX:** Clean, intuitive interface (easy onboarding)
- **Full-Stack:** On-call, incident management, post-mortems in one platform
- **Fast Setup:** 10-minute setup, minimal configuration
- **Post-Mortem Integration:** Automated post-mortem generation from incident data
- **Status Page:** Built-in status page functionality

**Weaknesses:**
- **Newer Platform:** Less proven than PagerDuty/Opsgenie (founded ~2020)
- **Integration:** Fewer third-party integrations (100+ vs 700+)
- **Limited Documentation:** Not yet in Context7 (newer product)
- **Pricing Transparency:** Must contact sales for pricing

**Pricing:**
- Contact sales for pricing (typically competitive with Opsgenie)

**When to Choose incident.io:**
- Team size: 5-50 engineers
- Workflow: Slack-centric culture
- Need: Modern tooling, AI assistance, fast setup
- Value: Simplicity over feature breadth
- Culture: Early adopter, willing to try newer platforms

**Resources:**
- Documentation: https://incident.io/docs
- Blog: https://incident.io/blog (excellent incident management content)

---

### Splunk On-Call (formerly VictorOps)

**Overview:** Splunk product, best for existing Splunk observability users.

**Strengths:**
- **Splunk Ecosystem:** Native integration with Splunk Observability Cloud
- **Timeline View:** Excellent incident timeline visualization
- **ChatOps:** Strong Slack/Teams integration
- **Transmogrifier:** Flexible alert transformation and routing
- **Incident Metrics:** Deep analytics on MTTA, MTTR, on-call load

**Weaknesses:**
- **Splunk Lock-In:** Less valuable without Splunk stack
- **Cost:** Tied to Splunk licensing (can be expensive)
- **UI:** Less modern than incident.io or Opsgenie

**Pricing:**
- Bundled with Splunk Observability Cloud
- Standalone: $25-40/user/month

**When to Choose Splunk On-Call:**
- Already using Splunk for monitoring/logging
- Need: Unified Splunk platform
- Budget: Enterprise (Splunk licensing already acquired)
- Infrastructure: Heavy investment in Splunk ecosystem

**Resources:**
- Documentation: https://help.victorops.com/

---

## Decision Framework

### By Team Size

**Small Teams (5-10 Engineers):**
- **Recommended:** Opsgenie Free or incident.io
- **Why:** Affordable, easy setup, sufficient features for small scale
- **Alternative:** PagerDuty Starter if extensive integrations needed

**Medium Teams (10-50 Engineers):**
- **Recommended:** Opsgenie Standard or incident.io
- **Why:** Balance of features, cost, and scalability
- **Alternative:** PagerDuty Professional if complex escalations needed

**Large Teams (50-500 Engineers):**
- **Recommended:** PagerDuty Professional or Opsgenie Enterprise
- **Why:** Advanced features, multi-team coordination, AIOps
- **Alternative:** Splunk On-Call if already using Splunk

**Enterprise (500+ Engineers):**
- **Recommended:** PagerDuty Business
- **Why:** Enterprise features (SSO, audit logs, advanced analytics)
- **Alternative:** Opsgenie Enterprise for Atlassian-centric orgs

---

### By Budget

**Budget: $0-200/month:**
- **Opsgenie Free:** Up to 5 users, basic features
- **DIY:** Custom solution with Slack + Twilio + scripts

**Budget: $200-500/month:**
- **Opsgenie Standard:** 10-20 users with full features
- **incident.io:** Modern platform with AI features

**Budget: $500-2000/month:**
- **PagerDuty Professional:** 15-50 users with AIOps
- **Opsgenie Enterprise:** 30-70 users with advanced automation

**Budget: $2000+/month:**
- **PagerDuty Business:** Enterprise features, unlimited users
- **Splunk On-Call:** If part of Splunk bundle

---

### By Existing Stack

**Atlassian Ecosystem (Jira, Confluence, Bitbucket):**
- **Best Choice:** Opsgenie
- **Why:** Native integrations, unified experience

**Splunk Monitoring/Logging:**
- **Best Choice:** Splunk On-Call
- **Why:** Seamless Splunk integration

**Slack-Centric Culture:**
- **Best Choice:** incident.io
- **Why:** Deepest Slack integration, Slack-native workflow

**AWS-Heavy Infrastructure:**
- **Best Choice:** PagerDuty
- **Why:** Extensive AWS integrations (CloudWatch, SNS, Lambda)

**Datadog Monitoring:**
- **Best Choice:** PagerDuty or Opsgenie
- **Why:** Both have excellent Datadog integrations

---

### By Use Case

**Complex Multi-Team Escalations:**
- **PagerDuty:** Most advanced escalation policies
- **Example:** Tier 1 → Tier 2 → Team Lead → Director → VP chains

**AI-Powered Incident Response:**
- **incident.io:** Most advanced AI features
- **Example:** Autonomous investigation, pattern detection

**Budget-Conscious Startups:**
- **Opsgenie Free or Standard:** Best value for money
- **Example:** 10-person startup with limited budget

**Rapid Setup (< 1 hour):**
- **incident.io:** Fastest setup and onboarding
- **Example:** New team needs incident management today

**Regulatory Compliance (Audit Logs, SSO):**
- **PagerDuty Business or Opsgenie Enterprise:** Full audit trails
- **Example:** Healthcare, finance with compliance requirements

---

## Status Page Solutions

### Statuspage.io (Atlassian)

**Best For:** Most teams, trusted brand, easy setup

**Strengths:**
- Widely recognized by customers (builds trust)
- 10-minute setup, minimal configuration
- Integrations: Auto-updates from PagerDuty, Datadog, etc.
- Subscriber management: Email/SMS notifications
- Custom domain: status.yourcompany.com
- Multi-language support

**Cost:** $29-399/month (based on subscribers)

**When to Choose:**
- Need: Trusted, recognizable status page
- Budget: $29+/month acceptable
- Integrations: Want auto-updates from monitoring tools

---

### Instatus

**Best For:** Budget-conscious teams, modern design

**Strengths:**
- Affordable: $19-99/month
- Modern UI: Clean, customizable design
- Fast: Lightweight, instant page loads
- Unlimited Subscribers: No subscriber limits
- Easy Setup: 5-minute deployment
- API: Automation for status updates

**Cost:** $19-99/month (unlimited subscribers)

**When to Choose:**
- Budget: Under $100/month
- Need: Modern, fast status page
- Subscribers: High subscriber count (unlimited)

**Resources:**
- Website: https://instatus.com/

---

### Custom Status Page (Self-Hosted)

**Best For:** High customization needs, compliance requirements

**Example Implementations:**
- GitHub Status (custom-built)
- AWS Status Dashboard
- Cloudflare Status

**Pros:**
- Full control over design and functionality
- No vendor lock-in
- Data sovereignty (compliance)

**Cons:**
- Maintenance burden (updates, hosting, monitoring)
- Build time (2-4 weeks initial setup)
- Ongoing operational overhead

**When to Choose:**
- Need: Full customization, regulatory data residency
- Resources: Engineering capacity for maintenance
- Budget: Prefer one-time build over recurring SaaS cost

---

## Integration Patterns

### Monitoring → Incident Management

**Prometheus → PagerDuty:**
```yaml
# Alertmanager config
receivers:
  - name: pagerduty
    pagerduty_configs:
      - service_key: <integration-key>
        severity: '{{ .GroupLabels.severity }}'
        description: '{{ .CommonAnnotations.summary }}'
```

**Datadog → Opsgenie:**
```
Datadog Integration → Opsgenie API
- Datadog Monitor triggers
- Sends to Opsgenie endpoint
- Creates alert with Datadog context
```

---

### Incident Management → Communication

**PagerDuty → Slack:**
```python
# Webhook handler
@app.post("/pagerduty-webhook")
def pagerduty_webhook(data: dict):
    incident_id = data['incident']['id']
    severity = data['incident']['urgency']

    # Create incident channel
    channel_name = f"incident-{date.today()}-{incident_id}"
    slack.channels_create(name=channel_name)

    # Post initial message
    slack.chat_postMessage(
        channel=channel_name,
        text=f"Incident {incident_id} declared: {severity}"
    )
```

See `examples/integrations/pagerduty-slack.py` for complete implementation.

---

### Incident Management → Status Page

**Opsgenie → Statuspage.io:**
```python
# Auto-update status page from Opsgenie alert
def on_alert_created(alert):
    statuspage.create_incident(
        name=alert['message'],
        status='investigating',
        body=alert['description']
    )
```

See `examples/integrations/statuspage-auto-update.py` for complete implementation.

---

## Migration Considerations

### Migrating Between Platforms

**From PagerDuty to Opsgenie:**
- Export: PagerDuty schedules, escalation policies (API or manual)
- Import: Create in Opsgenie via Terraform or API
- Integrations: Reconfigure monitoring tools to new endpoints
- Testing: Run parallel for 1-2 weeks before cutover

**From Legacy System to Modern Platform:**
- Phase 1: Set up new platform in parallel (shadow mode)
- Phase 2: Migrate one team at a time (A/B testing)
- Phase 3: Full cutover after 1 month validation
- Rollback: Keep legacy system available for 1 month

---

## Open Source Alternatives

### Alertmanager (Prometheus)

**Best For:** Self-hosted, Prometheus-centric environments

**Features:**
- Alert routing and grouping
- Silence management
- Integration with chat (Slack, PagerDuty)

**Limitations:**
- No on-call scheduling (add PagerDuty or Opsgenie)
- No incident management (only alerting)
- Requires operational overhead

---

### Grafana OnCall

**Best For:** Grafana users, open source preference

**Features:**
- On-call scheduling
- Escalation chains
- Grafana integration
- Slack, Telegram integration

**Limitations:**
- Newer platform (less mature)
- Limited integrations vs. commercial options

---

## Recommended Starter Stacks

### Budget-Conscious Stack ($500/month)

```
Incident Management: Opsgenie Standard ($200-400/month)
Status Page: Instatus ($19-99/month)
Communication: Slack (free or $7/user/month)
Post-Mortems: Google Docs (free)
Runbooks: Git + Markdown (free)
Monitoring: Prometheus + Grafana (free/self-hosted)
```

**Total:** ~$300-600/month for 20-30 person team

---

### Enterprise Stack ($2,000+/month)

```
Incident Management: PagerDuty Professional ($1,000-3,000/month)
Status Page: Statuspage.io ($399/month)
Communication: Slack ($7/user/month)
Post-Mortems: Confluence + Jeli ($500+/month)
Runbooks: PagerDuty Runbook Automation (included)
Monitoring: Datadog, New Relic, or Splunk
```

**Total:** $2,500-5,000/month for 50-100 person team

---

### Atlassian-Centric Stack

```
Incident Management: Opsgenie Enterprise ($500-1,500/month)
Status Page: Statuspage.io ($399/month)
Communication: Slack or Microsoft Teams
Post-Mortems: Confluence (included in Atlassian bundle)
Runbooks: Confluence + Jira (included)
Issue Tracking: Jira (included)
```

**Total:** Bundled in Atlassian subscription (~$1,000-2,000/month)

---

## Further Reading

- **PagerDuty:** https://www.pagerduty.com/platform/
- **Opsgenie:** https://www.atlassian.com/software/opsgenie
- **incident.io:** https://incident.io/
- **Splunk On-Call:** https://www.splunk.com/en_us/products/on-call.html
- **Statuspage.io:** https://www.atlassian.com/software/statuspage
- **Instatus:** https://instatus.com/

**Comparison Sites:**
- G2: User reviews and ratings
- Gartner: IT management tool analysis
- TrustRadius: Detailed platform comparisons
