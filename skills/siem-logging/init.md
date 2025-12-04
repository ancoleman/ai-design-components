# SIEM Logging Skill - Master Plan

**Skill Name:** `siem-logging`
**Skill Level:** Mid Level (5,000-8,000 tokens)
**Status:** Planning Phase (init.md complete, SKILL.md to be created)
**Last Updated:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [SIEM Architecture Taxonomy](#siem-architecture-taxonomy)
5. [Decision Frameworks](#decision-frameworks)
6. [Detection Rule Patterns](#detection-rule-patterns)
7. [Log Aggregation Architectures](#log-aggregation-architectures)
8. [Tool Recommendations](#tool-recommendations)
9. [Skill Structure Design](#skill-structure-design)
10. [Integration Points](#integration-points)
11. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why This Skill Matters

Security Information and Event Management (SIEM) is the foundation of modern security operations. In 2025, with the rise of sophisticated cyber threats, cloud-native architectures, and regulatory compliance requirements, comprehensive security logging and threat detection are critical capabilities for any organization.

**Market Drivers:**

- **AI-Driven Threat Detection:** SIEM platforms are evolving with AI-powered threat detection, agentic AI for cyber defense, and automated response capabilities
- **Cloud-Native Security:** Organizations need to monitor multi-cloud environments (AWS, Azure, GCP) with unified visibility
- **Compliance Requirements:** GDPR, HIPAA, PCI DSS, SOC 2 mandate comprehensive logging and audit trails
- **Zero Trust Architecture:** Security logging is essential for verifying every request and detecting anomalous behavior
- **Ransomware & Supply Chain Attacks:** Real-time threat detection is critical for preventing devastating attacks
- **Cost Management:** High-volume logging requires strategic approaches to manage costs while maintaining security coverage

**Strategic Value:**

1. **Universal Need:** Every production system needs security logging and threat detection
2. **Proactive Defense:** Shift from reactive incident response to proactive threat hunting
3. **Compliance Enabler:** Foundation for meeting regulatory and audit requirements
4. **Cross-Platform:** Spans cloud providers, on-premise infrastructure, containers, and serverless
5. **Integration Critical:** SIEM integrates with incident response, vulnerability management, and security automation

### How This Differs from Existing Solutions

**Existing SIEM Documentation:**

- **Vendor-Specific:** Splunk docs, Elastic SIEM docs, Microsoft Sentinel docs exist in isolation
- **Implementation-Focused:** "How to configure" vs. "When to use what architecture"
- **Tool-Centric:** Assumes you've already chosen a SIEM platform
- **Enterprise-Biased:** Optimized for large organizations with dedicated security teams

**Our Approach:**

- **Strategic Decision Framework:** When to use centralized vs. distributed logging, how to choose between SIEM platforms
- **Multi-Platform Patterns:** Consistent patterns across Elastic SIEM, Splunk, Microsoft Sentinel, Wazuh, and cloud-native solutions
- **Cost-Conscious:** Practical guidance on managing high-volume logging costs (sampling, retention, tiering)
- **Detection-First:** Emphasis on effective threat detection rules (SIGMA format, Elastic detection rules, custom queries)
- **Cloud-Native Focus:** Modern architectures with containers, Kubernetes, serverless, and multi-cloud environments
- **Right-Sizing:** Solutions for startups (open-source, cloud-native) to enterprises (commercial platforms)

### Target Audience

**Primary Users:**

- Security engineers implementing SIEM solutions
- DevOps/Platform engineers responsible for security logging infrastructure
- Security analysts writing detection rules and hunting threats
- Compliance officers ensuring audit trail requirements are met
- Backend developers integrating application logging with SIEM

**Skill Level Assumptions:**

- Understands basic security concepts (authentication, authorization, encryption)
- Familiar with logging frameworks (structured logging, log levels)
- Knows difference between logs, metrics, and traces (but needs guidance on security-specific logging)
- Has deployed applications to production (understands operational concerns)

---

## Skill Purpose and Scope

### What This Skill Teaches

**Core Competencies:**

1. **SIEM Platform Selection**
   - When to use Elastic SIEM vs. Splunk vs. Microsoft Sentinel vs. Wazuh
   - Open-source vs. commercial trade-offs
   - Cloud-native vs. self-hosted considerations
   - Cost modeling for high-volume logging

2. **Log Aggregation Architecture**
   - Centralized vs. distributed logging patterns
   - Multi-region, multi-cloud log aggregation
   - Log shipping strategies (agents, syslog, cloud-native integrations)
   - Buffering, batching, and reliability patterns

3. **Threat Detection Rules**
   - SIGMA rule format (universal detection language)
   - Elastic detection rules and EQL (Event Query Language)
   - Splunk SPL (Search Processing Language) queries
   - Microsoft Sentinel KQL (Kusto Query Language)
   - Custom rule development workflow

4. **Security Event Correlation**
   - Multi-event correlation patterns (user activity, network traffic, system events)
   - Attack chain detection (MITRE ATT&CK framework)
   - Behavioral analytics and anomaly detection
   - False positive reduction techniques

5. **Log Retention and Compliance**
   - Retention policies by compliance framework (GDPR, HIPAA, PCI DSS, SOC 2)
   - Hot/warm/cold storage tiering
   - Data anonymization and PII handling
   - Tamper-proof log storage

6. **Cloud-Native Logging**
   - AWS CloudWatch, CloudTrail, VPC Flow Logs
   - Azure Monitor, Azure Activity Logs
   - GCP Cloud Logging, Audit Logs
   - Kubernetes audit logs and container logging
   - Serverless function logging (Lambda, Cloud Functions, Azure Functions)

7. **Alert Tuning and Fatigue Reduction**
   - Alert prioritization (severity levels, business impact)
   - Noise reduction strategies (whitelisting, threshold tuning)
   - Alert routing and escalation workflows
   - SOAR (Security Orchestration, Automation, Response) integration

8. **Metrics and KPIs for Security Operations**
   - Mean Time to Detect (MTTD)
   - Mean Time to Respond (MTTR)
   - Alert volume and false positive rates
   - Coverage metrics (monitored assets, detection rules)
   - Cost per GB of log data

### What This Skill Does NOT Cover

**Out of Scope:**

- **General Observability:** Application performance monitoring, distributed tracing (see `observability` skill)
- **Infrastructure Monitoring:** Server metrics, uptime monitoring (see `observability` skill)
- **Incident Response Procedures:** Playbooks, runbooks, post-mortem analysis (see `incident-management` skill)
- **Vulnerability Scanning:** CVE detection, patch management (see `security-hardening` skill)
- **Penetration Testing:** Offensive security, red teaming (separate skill)
- **Access Control Implementation:** IAM, RBAC configuration (see `auth-security` skill)
- **Network Security:** Firewalls, IDS/IPS, DDoS protection (see `security-hardening` skill)

### Success Criteria

**A user successfully uses this skill when they can:**

1. Select the right SIEM platform for their organization's size, budget, and requirements
2. Design a scalable log aggregation architecture for multi-cloud environments
3. Write effective threat detection rules in SIGMA, EQL, SPL, or KQL
4. Implement log retention policies that meet compliance requirements
5. Configure cloud-native logging integrations (AWS, Azure, GCP, Kubernetes)
6. Tune alerts to reduce false positives and alert fatigue
7. Calculate and optimize costs for high-volume logging (TB/day scale)
8. Integrate SIEM with incident response workflows

---

## Research Findings

### Research Date: December 3, 2025

**Research Tools Used:**
- Google Search Grounding (Vertex AI): SIEM tools comparison, security logging best practices
- Context7 for library documentation: Elasticsearch, Wazuh
- Official documentation: Elastic SIEM, Microsoft Sentinel, Splunk, Wazuh

### Key Trends for 2025

**1. AI-Powered SIEM Evolution**

- **Agentic AI for Cyber Defense:** SIEM platforms are integrating AI agents for autonomous threat hunting, investigation, and response
- **Elastic AI SOC Engine (EASE):** AI-driven alert correlation, triage, and automated response
- **Microsoft Sentinel:** Evolving into broader security platform with AI-driven threat intelligence
- **Splunk Agentic SOC:** AI-powered security operations center capabilities

**2. Cloud-Native and Multi-Cloud Dominance**

- **Microsoft Sentinel:** Cloud-native SIEM built on Azure, elastic scaling, pay-as-you-go pricing
- **AWS Security Lake:** Centralized security data lake for multi-source log aggregation
- **Elastic Cloud:** Cloud-hosted Elastic SIEM with auto-scaling
- **Hybrid Deployments:** Organizations running SIEM in cloud while monitoring on-premise and multi-cloud resources

**3. Open-Source SIEM Adoption**

- **Wazuh:** Free, open-source XDR and SIEM platform gaining traction for cost-conscious organizations
- **Elastic Stack (ELK):** Open-source foundation with commercial Elastic SIEM add-ons
- **OpenSearch:** AWS fork of Elasticsearch used in AWS Security Lake

**4. Detection-as-Code Movement**

- **SIGMA Rules:** Universal detection format supported across SIEM platforms (Elastic, Splunk, Sentinel, Wazuh)
- **Elastic Detection Rules:** Community-contributed detection rules mapped to MITRE ATT&CK
- **Version Control for Rules:** Detection rules treated as infrastructure-as-code (Git, CI/CD)
- **Automated Rule Testing:** Unit testing and validation for detection logic

**5. Cost Optimization Strategies**

- **Data Tiering:** Hot (real-time), warm (recent), cold (archive) storage for cost savings
- **Sampling and Filtering:** Smart log sampling to reduce ingestion volumes
- **Commitment Tiers:** Microsoft Sentinel 50 GB tier for small/mid-sized organizations
- **Open-Source Alternatives:** Wazuh + Elasticsearch as zero-license-cost alternative

**6. Compliance and Privacy Requirements**

- **GDPR, CCPA:** Data anonymization, PII masking in logs
- **HIPAA:** Tamper-proof audit logs, encryption at rest and in transit
- **PCI DSS:** Log retention requirements, real-time monitoring
- **SOC 2:** Comprehensive audit trails, access control

### SIEM Platform Comparison (2025)

**Market Leaders:**

| Platform | Deployment | Strengths | Weaknesses | Best For |
|----------|-----------|-----------|------------|----------|
| **Splunk Enterprise Security** | On-prem, Cloud | Scalability, customization, Fortune 100 usage, powerful analytics | Complexity, high cost, requires SOAR add-on | Large enterprises, high data volumes |
| **Microsoft Sentinel** | Cloud (Azure) | Cloud-native, Azure ecosystem integration, built-in SOAR, AI-driven threat intelligence | Azure-locked, best for Microsoft shops | Cloud-first orgs on Azure |
| **Elastic SIEM** | On-prem, Cloud | Open-source foundation, unified XDR, AI-powered (EASE), extensible | Requires unified vision, steep learning curve | DevOps teams, open-source advocates |
| **Wazuh** | On-prem, Cloud | Free/open-source, XDR capabilities, active community | Less enterprise features than commercial options | Cost-conscious organizations, SMBs |
| **AWS Security Lake** | Cloud (AWS) | AWS-native, multi-source aggregation, OpenSearch-based | AWS-locked, newer platform | AWS-heavy organizations |

**Key Selection Criteria:**

1. **Existing Infrastructure:** Azure → Sentinel, AWS → Security Lake, Multi-cloud → Elastic/Splunk/Wazuh
2. **Budget:** Unlimited → Splunk, Moderate → Sentinel/Elastic, Constrained → Wazuh
3. **Team Skills:** Microsoft experts → Sentinel, Elasticsearch experts → Elastic, Generalists → Wazuh
4. **Data Volume:** TB/day scale → Splunk/Elastic Cloud, GB/day → Sentinel/Wazuh
5. **Compliance:** Heavy compliance → Splunk/Sentinel (mature), Modern compliance → Elastic/Wazuh

### Security Logging Best Practices (2025)

**From Research:**

**Core Logging Practices:**

- **Comprehensive Logging:** API endpoints, authentication events, request/response details, source IPs
- **Centralized Aggregation:** Single pane of glass for security events across all systems
- **Log All Regions:** Multi-region trails for complete cloud environment coverage
- **Structured Logging:** JSON format with consistent schema for parsing and correlation

**Data Security:**

- **Encryption:** TLS 1.3 in transit, AES-256 at rest, KMS/HSM for key management
- **Access Control:** RBAC for log data access, separate from production environment
- **Tamper-Proof Storage:** Write-once-read-many (WORM) for compliance, log validation features
- **Data Masking:** Anonymize PII, credit cards, credentials before storage

**Monitoring and Alerting:**

- **Real-Time Monitoring:** Critical events trigger immediate alerts (authentication failures, privilege escalation)
- **Threat Detection:** AI-powered anomaly detection, behavioral analytics
- **Alert Routing:** Severity-based escalation, integration with incident response platforms

**Access Management:**

- **Multi-Factor Authentication (MFA):** All SIEM access, especially administrative functions
- **Least Privilege:** Role-based access for security analysts, engineers, auditors
- **Zero Trust:** Verify every SIEM access request, context-aware authentication

**Compliance and Governance:**

- **Retention Policies:** GDPR (varies), HIPAA (6 years), PCI DSS (1 year), SOC 2 (varies)
- **Regular Audits:** Verify SIEM configuration, rule effectiveness, coverage gaps
- **Incident Response Plan:** Documented playbooks for common security events

---

## SIEM Architecture Taxonomy

### Architecture Patterns

#### 1. Centralized SIEM Architecture

**Pattern:**

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  Web Servers│   │  App Servers│   │  Databases  │
│   (Logs)    │   │   (Logs)    │   │   (Logs)    │
└──────┬──────┘   └──────┬──────┘   └──────┬──────┘
       │                 │                 │
       │    ┌────────────┴────────────┐    │
       │    │                         │    │
       ├────►  Log Aggregation Layer  ◄────┤
       │    │  (Fluentd, Logstash,   │    │
       │    │   Filebeat, CloudWatch) │    │
       │    └────────────┬────────────┘    │
       │                 │                 │
       │                 ▼                 │
       │    ┌─────────────────────────┐   │
       └───►│   SIEM Platform         │◄──┘
            │  (Elastic, Splunk,      │
            │   Sentinel, Wazuh)      │
            └─────────────────────────┘
                        │
                        ▼
            ┌─────────────────────────┐
            │  Security Analysts       │
            │  (Dashboard, Alerts)     │
            └─────────────────────────┘
```

**Characteristics:**

- **Single SIEM Instance:** All logs flow to one central platform
- **Centralized Analysis:** Correlation across all data sources in one place
- **Simplified Management:** Single configuration, single UI, single team

**When to Use:**

- Single-region deployments
- Small to medium data volumes (<1 TB/day)
- Single cloud provider or on-premise
- Limited security team (1-10 analysts)

**Advantages:**

- Simplest architecture to implement and maintain
- Full correlation across all data sources
- Lower operational complexity
- Easier compliance reporting (single source of truth)

**Limitations:**

- Single point of failure (requires high availability)
- Network latency for global deployments
- Scaling limits at very high volumes
- Regulatory challenges (data residency)

---

#### 2. Distributed SIEM Architecture (Multi-Region)

**Pattern:**

```
┌───────────────────────────────────────────────────────┐
│               Global SIEM Platform                     │
│         (Correlation, Threat Intelligence)             │
└───────────────────┬───────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│  Region   │ │  Region   │ │  Region   │
│  SIEM     │ │  SIEM     │ │  SIEM     │
│  (US-East)│ │  (EU-West)│ │  (APAC)   │
└─────┬────┘ └─────┬────┘ └─────┬────┘
      │            │            │
   [Local        [Local       [Local
    Logs]         Logs]        Logs]
```

**Characteristics:**

- **Regional SIEM Instances:** Local analysis and alerting
- **Global Aggregation:** High-priority events forwarded to central SIEM
- **Data Residency:** Logs stay in region for compliance

**When to Use:**

- Multi-region global deployments
- Data residency requirements (GDPR, data sovereignty)
- High data volumes (>1 TB/day per region)
- Low-latency requirements for regional analysis

**Advantages:**

- Meets data residency requirements
- Lower network costs (logs don't cross regions)
- Improved performance (local analysis)
- Fault isolation (regional failures don't affect others)

**Limitations:**

- Complex management (multiple SIEM instances)
- Partial correlation (global threats may be missed)
- Higher operational costs
- Consistency challenges (rule synchronization)

---

#### 3. Cloud-Native SIEM Architecture

**Pattern (AWS Example):**

```
┌─────────────────────────────────────────────────┐
│           AWS Security Lake                      │
│     (Centralized Security Data Lake)             │
└───────────┬─────────────────────────────────────┘
            │
    ┌───────┼───────┬─────────┬─────────┐
    │       │       │         │         │
    ▼       ▼       ▼         ▼         ▼
CloudTrail VPC     GuardDuty Security  3rd-Party
(API Logs) Flow    (Threat   Hub      (Custom
           Logs    Detection)(Findings) Logs)

            │
            ▼
┌─────────────────────────────┐
│  OpenSearch (SIEM Engine)    │
│  - Detection Rules           │
│  - Dashboards                │
│  - Alerting                  │
└─────────────────────────────┘
            │
            ▼
┌─────────────────────────────┐
│  EventBridge / Lambda        │
│  (Automated Response)        │
└─────────────────────────────┘
```

**Characteristics:**

- **Cloud-Native Services:** Leverages managed services (CloudWatch, Security Lake, Sentinel)
- **Auto-Scaling:** Elastic capacity based on log volume
- **Tight Integration:** Native cloud service integrations (IAM, network, compute logs)

**When to Use:**

- Cloud-first organizations (AWS, Azure, GCP)
- Want to avoid managing SIEM infrastructure
- Elastic workloads with variable log volumes
- Budget for cloud service costs

**Advantages:**

- No infrastructure management
- Auto-scaling to any volume
- Native cloud integrations
- Pay-as-you-go pricing

**Limitations:**

- Vendor lock-in (AWS Security Lake, Azure Sentinel, GCP Chronicle)
- Potentially higher costs at scale
- Less customization than self-hosted
- Data egress costs (multi-cloud)

---

#### 4. Hybrid SIEM Architecture

**Pattern:**

```
┌──────────────────────────────────────────┐
│         Cloud SIEM (Microsoft Sentinel)   │
│         - Cloud workload logs             │
│         - Central correlation              │
└───────────────────┬──────────────────────┘
                    │
                    │ (Encrypted VPN/ExpressRoute)
                    │
┌───────────────────▼──────────────────────┐
│   On-Premise SIEM (Splunk/Elastic)        │
│   - Legacy systems logs                   │
│   - Network device logs                   │
│   - Critical infrastructure               │
└───────────────────────────────────────────┘
```

**Characteristics:**

- **Multi-Platform:** Cloud SIEM for cloud resources, on-premise SIEM for legacy systems
- **Selective Forwarding:** Critical events forwarded between platforms
- **Gradual Migration:** Transition from on-premise to cloud over time

**When to Use:**

- Hybrid cloud deployments (cloud + on-premise)
- Migration in progress (legacy to cloud)
- Regulatory requirements for on-premise logs
- Cost optimization (keep historical data on-premise)

**Advantages:**

- Flexibility for hybrid environments
- Gradual cloud migration path
- Cost optimization (cheap on-premise storage for archives)
- Meets compliance for on-premise data

**Limitations:**

- Most complex architecture
- Requires managing multiple platforms
- Correlation challenges across platforms
- Higher skill requirements

---

### Log Aggregation Layers

#### Tier 1: Log Shippers (Agent-Based)

**Purpose:** Collect logs from endpoints and forward to aggregation layer

**Tools:**

- **Elastic Filebeat:** Lightweight log shipper, native Elasticsearch integration
- **Fluentd/Fluent Bit:** CNCF project, Kubernetes-native, plugin ecosystem
- **Splunk Universal Forwarder:** Splunk-native agent, efficient forwarding
- **Wazuh Agent:** Security-focused agent with built-in threat detection
- **AWS CloudWatch Agent:** AWS-native log collection
- **Azure Monitor Agent:** Azure-native log collection

**Patterns:**

```yaml
# Filebeat Example (YAML)
filebeat.inputs:
  - type: log
    paths:
      - /var/log/nginx/access.log
      - /var/log/nginx/error.log
    fields:
      service: nginx
      environment: production

output.elasticsearch:
  hosts: ["https://elasticsearch:9200"]
  username: "elastic"
  password: "${ELASTIC_PASSWORD}"
```

---

#### Tier 2: Log Aggregation (Centralized Processing)

**Purpose:** Buffer, parse, enrich, and route logs to SIEM

**Tools:**

- **Logstash:** Elastic Stack component, rich plugin ecosystem
- **Fluentd:** CNCF log aggregator, cloud-native
- **Kafka:** High-throughput buffering and streaming
- **AWS Kinesis Firehose:** AWS-managed streaming

**Patterns:**

```ruby
# Logstash Example (Grok Parsing)
filter {
  grok {
    match => {
      "message" => "%{IPORHOST:client_ip} - - \[%{HTTPDATE:timestamp}\] \"%{WORD:http_method} %{URIPATHPARAM:request_path} HTTP/%{NUMBER:http_version}\" %{NUMBER:response_code} %{NUMBER:bytes_sent}"
    }
  }

  geoip {
    source => "client_ip"
    target => "geoip"
  }

  date {
    match => [ "timestamp", "dd/MMM/yyyy:HH:mm:ss Z" ]
    target => "@timestamp"
  }
}

output {
  elasticsearch {
    hosts => ["https://elasticsearch:9200"]
    index => "nginx-logs-%{+YYYY.MM.dd}"
  }
}
```

---

#### Tier 3: SIEM Storage and Analysis

**Purpose:** Store, index, search, correlate, and alert on security events

**Storage Patterns:**

**A. Hot-Warm-Cold Architecture (Elastic)**

```
┌──────────────┐
│  Hot Tier    │  Last 7 days, SSD, frequent searches
│  (Recent)    │  Real-time indexing, fast queries
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Warm Tier   │  8-90 days, slower storage, less frequent searches
│  (Recent-ish)│  Read-only indices, reduced replicas
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Cold Tier   │  >90 days, cheapest storage, rare searches
│  (Archive)   │  Searchable snapshots, S3/Azure Blob
└──────────────┘
```

**B. Index Lifecycle Management (ILM)**

```json
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_size": "50GB",
            "max_age": "7d"
          }
        }
      },
      "warm": {
        "min_age": "7d",
        "actions": {
          "shrink": {
            "number_of_shards": 1
          },
          "forcemerge": {
            "max_num_segments": 1
          }
        }
      },
      "cold": {
        "min_age": "90d",
        "actions": {
          "searchable_snapshot": {
            "snapshot_repository": "security-snapshots"
          }
        }
      },
      "delete": {
        "min_age": "365d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

---

## Decision Frameworks

### Framework 1: SIEM Platform Selection

**Decision Tree:**

```
START: Which SIEM platform should I use?

Q1: What is your budget?
  ├─ Unlimited budget → Q2
  ├─ Moderate budget ($50k-$500k/year) → Q3
  └─ Tight budget (<$50k/year) → Open-Source (Wazuh + Elastic Stack)

Q2: Do you have existing vendor ecosystem?
  ├─ Heavy Azure investment → Microsoft Sentinel
  ├─ Heavy AWS investment → AWS Security Lake + OpenSearch
  └─ Multi-cloud or on-premise → Splunk Enterprise Security

Q3: What is your data volume?
  ├─ >1 TB/day → Elastic Cloud or Splunk Cloud
  ├─ 100 GB - 1 TB/day → Microsoft Sentinel or Elastic
  └─ <100 GB/day → Wazuh or Sentinel (50 GB tier)

Q4: What is your team's expertise?
  ├─ Elasticsearch experts → Elastic SIEM
  ├─ Microsoft/Azure experts → Microsoft Sentinel
  ├─ Splunk experience → Splunk
  └─ Generalists → Wazuh (easiest learning curve)
```

**Comparison Matrix:**

| Criteria | Splunk ES | Microsoft Sentinel | Elastic SIEM | Wazuh | AWS Security Lake |
|----------|-----------|-------------------|--------------|-------|-------------------|
| **Cost (GB/day)** | $$$$$ | $$$ | $$$ | $ (free) | $$$ |
| **Scalability** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Ease of Use** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Cloud-Native** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Customization** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Built-in SOAR** | ⭐⭐ (add-on) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Community** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **AI/ML Features** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

---

### Framework 2: Log Retention Policy Design

**Decision Matrix:**

| Compliance Framework | Hot Storage | Warm Storage | Cold Storage | Total Retention |
|---------------------|-------------|--------------|--------------|-----------------|
| **GDPR** | 7 days | 30 days | 60 days (optional) | 30-90 days |
| **HIPAA** | 30 days | 180 days | 6 years | 6 years |
| **PCI DSS** | 90 days | 180 days | 1 year | 1 year |
| **SOC 2** | 30 days | 90 days | 1 year | 1 year |
| **NIST** | 30 days | 90 days | Varies | Varies |
| **General Best Practice** | 14 days | 60 days | 1 year | 1 year |

**Retention Strategy:**

```
1. Identify applicable compliance frameworks
2. Take the MAXIMUM retention requirement across all frameworks
3. Design tiering strategy:
   - Hot: Last 7-30 days (real-time analysis, SSD)
   - Warm: 30-90 days (occasional searches, HDD)
   - Cold: 90 days - retention limit (archive, S3/Blob)
   - Delete: Beyond retention limit (GDPR right to be forgotten)
```

**Cost Optimization:**

```
Example: 500 GB/day log volume, 1-year retention

Hot (30 days): 15 TB @ $0.10/GB/month = $1,500/month
Warm (60 days): 30 TB @ $0.05/GB/month = $1,500/month
Cold (275 days): 137.5 TB @ $0.01/GB/month = $1,375/month

Total: $4,375/month = $52,500/year

vs. Hot-only (365 days): 182.5 TB @ $0.10/GB/month = $18,250/month = $219,000/year

Savings: $166,500/year (76% reduction)
```

---

### Framework 3: What to Log (Security Events)

**Critical Security Events (MUST LOG):**

1. **Authentication Events**
   - Login attempts (successful and failed)
   - MFA challenges
   - Password changes
   - Session creation/termination
   - Privilege escalation

2. **Authorization Events**
   - Permission grants/revocations
   - Role changes
   - Policy modifications
   - Access denials

3. **Data Access Events**
   - Database queries (sensitive tables)
   - File access (PII, financial data)
   - API calls (sensitive endpoints)
   - Export operations

4. **Network Events**
   - Inbound/outbound connections
   - Firewall denials
   - VPN connections
   - DNS queries (C2 detection)

5. **System Events**
   - Service starts/stops
   - Configuration changes
   - Software installations
   - Kernel module loads

6. **Application Events**
   - Error messages
   - Validation failures
   - Business logic violations
   - Sensitive operations

**Log Level Mapping:**

| Event Type | Severity | SIEM Index | Real-Time Alert |
|------------|----------|------------|-----------------|
| Failed authentication (3+ attempts) | HIGH | security-auth | Yes |
| Successful authentication | INFO | security-auth | No |
| Privilege escalation | CRITICAL | security-auth | Yes |
| Data export (large volume) | HIGH | security-data | Yes |
| Configuration change | MEDIUM | security-system | No |
| API error (5xx) | MEDIUM | application | No |
| Firewall denial | LOW | security-network | No |

---

### Framework 4: Alert Tuning Strategy

**Alert Lifecycle:**

```
1. Detection Rule Created
   ├─ Initial threshold (conservative, low false positives)
   ├─ Deploy to production
   └─ Monitor alert volume

2. Baseline Period (2-4 weeks)
   ├─ Collect alert data
   ├─ Investigate all alerts
   ├─ Tag true positives vs. false positives
   └─ Identify patterns

3. Tuning Phase
   ├─ Add whitelisting (known-safe patterns)
   ├─ Adjust thresholds (reduce noise)
   ├─ Refine correlation logic
   └─ Update severity levels

4. Continuous Improvement
   ├─ Weekly review of alert metrics
   ├─ Monthly rule effectiveness review
   └─ Quarterly threat landscape updates
```

**Noise Reduction Techniques:**

**A. Whitelisting (Known-Safe Patterns)**

```yaml
# Example: Allow scanner IPs to trigger rate-limit alerts
- rule_id: brute_force_detection
  whitelist:
    - source_ip: "10.0.0.100"  # Security scanner
    - user_agent: "Nagios"      # Monitoring system
```

**B. Threshold Tuning**

```yaml
# Before: Too sensitive
- rule: failed_login_attempts
  threshold: 3 attempts in 5 minutes
  alerts_per_day: 500
  true_positive_rate: 5%

# After: Tuned
- rule: failed_login_attempts
  threshold: 10 attempts in 10 minutes
  alerts_per_day: 50
  true_positive_rate: 40%
```

**C. Correlation (Multi-Event)**

```yaml
# Instead of: Single event alert
- alert_on: "Failed authentication"

# Use: Correlated pattern
- alert_on:
    - "Failed authentication (5+ times)"
    - AND "From new IP address"
    - AND "Successful authentication follows"
    - WITHIN: 30 minutes
```

**Alert Metrics Dashboard:**

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Total Alerts/Day | <100 | 87 | ✅ |
| True Positive Rate | >30% | 42% | ✅ |
| Mean Time to Investigate | <15 min | 12 min | ✅ |
| False Positive Rate | <50% | 58% | ⚠️ Needs tuning |
| Critical Alerts/Day | <10 | 6 | ✅ |

---

## Detection Rule Patterns

### SIGMA Rule Format (Universal Detection Language)

**What is SIGMA?**

SIGMA is an open-source, generic signature format for SIEM systems. Write once, compile to any SIEM query language (Elastic EQL, Splunk SPL, Microsoft KQL, etc.).

**SIGMA Rule Structure:**

```yaml
title: Suspicious PowerShell Download Execution
id: 1f21ec3f-810d-4b0e-8045-322202e22b4b
status: stable
description: Detects PowerShell commands downloading files from the internet
author: Security Team
date: 2025/12/03
references:
  - https://attack.mitre.org/techniques/T1059/001/
tags:
  - attack.execution
  - attack.t1059.001
logsource:
  category: process_creation
  product: windows
detection:
  selection:
    Image|endswith: '\powershell.exe'
    CommandLine|contains:
      - 'Invoke-WebRequest'
      - 'iwr'
      - 'wget'
      - 'curl'
      - 'DownloadFile'
      - 'DownloadString'
  condition: selection
falsepositives:
  - Legitimate software updates
  - Admin scripts
level: medium
```

**Compiling SIGMA to SIEM Queries:**

```bash
# Install sigmac (SIGMA compiler)
pip install sigma-cli

# Compile to Elastic EQL
sigmac -t es-eql sigma_rule.yml

# Compile to Splunk SPL
sigmac -t splunk sigma_rule.yml

# Compile to Microsoft KQL
sigmac -t kusto sigma_rule.yml
```

**Example Output (Elastic EQL):**

```eql
process where event.type == "start" and
  process.name == "powershell.exe" and
  process.command_line : ("*Invoke-WebRequest*", "*iwr*", "*wget*", "*curl*", "*DownloadFile*", "*DownloadString*")
```

---

### SIGMA Rule Examples (Common Patterns)

#### 1. Brute Force Detection

```yaml
title: Multiple Failed Login Attempts from Single Source
id: 8a9e3c7f-4b2d-4e8a-9f1c-2d5e6f7a8b9c
description: Detects potential brute force attacks (10+ failed logins in 10 minutes)
logsource:
  category: authentication
  product: linux
detection:
  selection:
    event.type: authentication
    event.outcome: failure
  timeframe: 10m
  condition: selection | count() by source.ip > 10
level: high
```

#### 2. Privilege Escalation (Linux sudo)

```yaml
title: Suspicious Sudo Execution
id: 7b8c9d0e-1f2a-3b4c-5d6e-7f8a9b0c1d2e
description: Detects sudo execution by non-privileged users
logsource:
  category: process_creation
  product: linux
detection:
  selection:
    process.name: sudo
    user.name:
      - 'www-data'
      - 'nobody'
      - 'nginx'
      - 'apache'
  condition: selection
level: high
```

#### 3. Data Exfiltration (Large Upload)

```yaml
title: Large Data Upload to External Domain
id: 9c0d1e2f-3a4b-5c6d-7e8f-9a0b1c2d3e4f
description: Detects uploads >100MB to non-whitelisted domains
logsource:
  category: network_traffic
  product: proxy
detection:
  selection:
    http.request.method: POST
    http.request.bytes: '>100000000'
  filter_whitelist:
    destination.domain:
      - 'backup.company.com'
      - 's3.amazonaws.com'
  condition: selection and not filter_whitelist
level: critical
```

#### 4. Credential Access (Mimikatz Detection)

```yaml
title: Mimikatz Execution Detected
id: 0d1e2f3a-4b5c-6d7e-8f9a-0b1c2d3e4f5a
description: Detects Mimikatz credential dumping tool
logsource:
  category: process_creation
  product: windows
detection:
  selection:
    CommandLine|contains:
      - 'sekurlsa::logonpasswords'
      - 'sekurlsa::tickets'
      - 'lsadump::sam'
      - 'kerberos::golden'
  condition: selection
level: critical
```

#### 5. Lateral Movement (RDP from Unusual Source)

```yaml
title: RDP Connection from Non-Admin Workstation
id: 1e2f3a4b-5c6d-7e8f-9a0b-1c2d3e4f5a6b
description: Detects RDP connections from workstations (not jump servers)
logsource:
  category: network_traffic
  product: firewall
detection:
  selection:
    destination.port: 3389
    network.protocol: tcp
  filter_jumpservers:
    source.ip:
      - '10.0.1.100'  # Jump Server 1
      - '10.0.1.101'  # Jump Server 2
  condition: selection and not filter_jumpservers
level: medium
```

---

### Elastic Detection Rules (EQL Examples)

**Event Query Language (EQL) Advantages:**

- Native to Elastic SIEM
- Sequence-based detection (multi-event correlation)
- MITRE ATT&CK mapping
- Time-based analysis

#### Example 1: Process Injection Detection (Sequence)

```eql
sequence by user.name with maxspan=5m
  [process where event.type == "start" and process.name == "powershell.exe"]
  [library where dll.name == "kernel32.dll" and
    dll.code_signature.subject_name != "Microsoft Corporation"]
  [network where process.name == "powershell.exe"]
```

**Explanation:**

1. PowerShell starts
2. Loads non-Microsoft signed DLL (suspicious)
3. Makes network connection (potential C2)
4. All within 5 minutes, by same user

#### Example 2: Credential Dumping (Registry Access)

```eql
registry where registry.path : (
  "HKLM\\SAM\\SAM\\Domains\\Account\\Users\\*",
  "HKLM\\SECURITY\\Policy\\Secrets\\*"
) and not process.executable : (
  "C:\\Windows\\System32\\lsass.exe",
  "C:\\Windows\\System32\\svchost.exe"
)
```

**Explanation:**

Detects non-system processes accessing registry paths where credentials are stored.

#### Example 3: Ransomware Behavior Detection

```eql
sequence by host.id with maxspan=1h
  [file where event.action == "modification" and file.extension : ("docx", "xlsx", "pdf")]
  [file where event.action == "modification" and file.extension : ("encrypted", "locked", "crypted")]
  [file where event.action == "creation" and file.name : ("*README*", "*DECRYPT*", "*RANSOM*")]
```

**Explanation:**

1. Normal files modified (documents, spreadsheets)
2. Files renamed with encryption extensions
3. Ransom note created
4. All on same host within 1 hour

---

### Microsoft Sentinel KQL Examples

**Kusto Query Language (KQL):**

```kql
// Example 1: Failed Logins from Multiple Countries
let threshold = 3;
SigninLogs
| where TimeGenerated > ago(1h)
| where ResultType != 0  // Failed login
| summarize FailedCountries=dcount(LocationDetails.countryOrRegion),
            FailedAttempts=count() by UserPrincipalName
| where FailedCountries >= threshold
| project UserPrincipalName, FailedCountries, FailedAttempts
```

```kql
// Example 2: Suspicious Azure Resource Deletion
AzureActivity
| where TimeGenerated > ago(24h)
| where OperationNameValue endswith "DELETE"
| where ActivityStatusValue == "Success"
| where ResourceProvider in ("Microsoft.Compute", "Microsoft.Storage", "Microsoft.Sql")
| summarize DeletedResources=count() by Caller, ResourceProvider
| where DeletedResources > 5
```

```kql
// Example 3: Office 365 Email Forwarding Rule Created
OfficeActivity
| where TimeGenerated > ago(7d)
| where Operation == "New-InboxRule"
| where Parameters has "ForwardTo" or Parameters has "RedirectTo"
| extend ForwardingAddress = extract("(ForwardTo|RedirectTo):([^;]+)", 2, Parameters)
| project TimeGenerated, UserId, ClientIP, ForwardingAddress
```

---

### Splunk SPL Examples

**Search Processing Language (SPL):**

```spl
# Example 1: Detect SQL Injection Attempts
index=web_logs sourcetype=access_combined
| rex field=uri "(?<sql_keywords>union|select|insert|update|delete|drop|exec|script)"
| where isnotnull(sql_keywords)
| stats count by src_ip, uri, sql_keywords
| where count > 5
```

```spl
# Example 2: Unusual Process Parent-Child Relationship
index=windows_logs sourcetype=WinEventLog:Security EventCode=4688
| eval parent_child=parent_process_name + "->" + new_process_name
| search parent_child IN (
    "winword.exe->cmd.exe",
    "excel.exe->powershell.exe",
    "outlook.exe->wscript.exe"
)
| stats count by ComputerName, user, parent_child
```

```spl
# Example 3: AWS CloudTrail Anomalous API Activity
index=aws_cloudtrail
| stats count by userName, eventName
| eventstats avg(count) as avg_count, stdev(count) as stdev_count by eventName
| eval threshold = avg_count + (2 * stdev_count)
| where count > threshold
| table userName, eventName, count, avg_count, threshold
```

---

## Log Aggregation Architectures

### Pattern 1: ELK Stack (Elastic, Logstash, Kibana)

**Architecture:**

```
┌─────────────┐
│ Application │
│   Servers   │
└──────┬──────┘
       │
       │ (Filebeat)
       ▼
┌─────────────┐
│  Logstash   │  ← Parsing, Enrichment, Filtering
└──────┬──────┘
       │
       ▼
┌─────────────┐
│Elasticsearch│  ← Storage, Indexing, Searching
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Kibana    │  ← Visualization, Dashboards
└─────────────┘
```

**Deployment (Docker Compose):**

```yaml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=true
      - ELASTIC_PASSWORD=changeme
    volumes:
      - esdata:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"

  logstash:
    image: docker.elastic.co/logstash/logstash:8.11.0
    volumes:
      - ./logstash/pipeline:/usr/share/logstash/pipeline
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
      - ELASTICSEARCH_USERNAME=elastic
      - ELASTICSEARCH_PASSWORD=changeme
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch

volumes:
  esdata:
```

**Logstash Pipeline (Security Logs):**

```ruby
# /logstash/pipeline/security.conf
input {
  beats {
    port => 5044
  }
}

filter {
  # Parse syslog messages
  if [type] == "syslog" {
    grok {
      match => {
        "message" => "%{SYSLOGBASE} %{GREEDYDATA:syslog_message}"
      }
    }
    date {
      match => [ "timestamp", "MMM  d HH:mm:ss", "MMM dd HH:mm:ss" ]
    }
  }

  # Parse authentication logs
  if [type] == "auth" {
    grok {
      match => {
        "message" => [
          "Failed password for %{USER:failed_user} from %{IP:source_ip}",
          "Accepted publickey for %{USER:success_user} from %{IP:source_ip}"
        ]
      }
    }

    if [failed_user] {
      mutate {
        add_field => { "event_type" => "failed_auth" }
        add_tag => [ "security", "authentication_failure" ]
      }
    }

    if [success_user] {
      mutate {
        add_field => { "event_type" => "successful_auth" }
        add_tag => [ "security", "authentication_success" ]
      }
    }
  }

  # GeoIP enrichment
  if [source_ip] {
    geoip {
      source => "source_ip"
      target => "geoip"
    }
  }

  # Threat intelligence lookup (example)
  if [source_ip] {
    translate {
      source => "source_ip"
      target => "threat_intel"
      dictionary_path => "/etc/logstash/threat_intel.yml"
      fallback => "unknown"
    }
  }
}

output {
  elasticsearch {
    hosts => ["http://elasticsearch:9200"]
    user => "elastic"
    password => "changeme"
    index => "security-logs-%{+YYYY.MM.dd}"
  }
}
```

---

### Pattern 2: Fluentd + Elasticsearch (Cloud-Native)

**Architecture (Kubernetes):**

```
┌─────────────────────────────────────────┐
│         Kubernetes Cluster               │
│                                          │
│  ┌──────┐  ┌──────┐  ┌──────┐          │
│  │ Pod  │  │ Pod  │  │ Pod  │          │
│  │      │  │      │  │      │          │
│  └───┬──┘  └───┬──┘  └───┬──┘          │
│      │         │         │              │
│      └─────────┴─────────┘              │
│                │                         │
│         ┌──────▼──────┐                 │
│         │ Fluentd     │ (DaemonSet)     │
│         │ (Collector) │                 │
│         └──────┬──────┘                 │
└────────────────┼────────────────────────┘
                 │
                 ▼
        ┌────────────────┐
        │ Elasticsearch  │
        │   (SIEM)       │
        └────────────────┘
```

**Fluentd Configuration (Kubernetes DaemonSet):**

```yaml
# fluentd-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
  namespace: kube-logging
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/containers/*.log
      pos_file /var/log/fluentd-containers.log.pos
      tag kubernetes.*
      read_from_head true
      <parse>
        @type json
        time_format %Y-%m-%dT%H:%M:%S.%NZ
      </parse>
    </source>

    <filter kubernetes.**>
      @type kubernetes_metadata
      @id filter_kube_metadata
      kubernetes_url "https://kubernetes.default.svc:443"
      verify_ssl true
    </filter>

    <filter kubernetes.**>
      @type parser
      key_name log
      reserve_data true
      remove_key_name_field true
      <parse>
        @type json
      </parse>
    </filter>

    # Security event enrichment
    <filter kubernetes.var.log.containers.nginx**>
      @type record_transformer
      <record>
        security_category "web_access"
        severity "info"
      </record>
    </filter>

    <match kubernetes.var.log.containers.auth**>
      @type elasticsearch
      host elasticsearch.kube-logging.svc.cluster.local
      port 9200
      user elastic
      password "#{ENV['ELASTICSEARCH_PASSWORD']}"
      index_name security-auth-logs
      type_name _doc
      <buffer>
        @type file
        path /var/log/fluentd-buffers/kubernetes.auth.buffer
        flush_mode interval
        flush_interval 5s
        retry_type exponential_backoff
        retry_wait 10s
        retry_max_interval 300s
        retry_forever false
        retry_max_times 5
      </buffer>
    </match>

    <match kubernetes.**>
      @type elasticsearch
      host elasticsearch.kube-logging.svc.cluster.local
      port 9200
      user elastic
      password "#{ENV['ELASTICSEARCH_PASSWORD']}"
      index_name k8s-logs
      type_name _doc
      <buffer>
        @type file
        path /var/log/fluentd-buffers/kubernetes.system.buffer
        flush_mode interval
        flush_interval 10s
      </buffer>
    </match>
```

---

### Pattern 3: AWS Security Lake Architecture

**Components:**

```
┌─────────────────────────────────────────────────┐
│            AWS Account (Production)              │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │CloudTrail│  │VPC Flow  │  │GuardDuty │     │
│  │(API Logs)│  │  Logs    │  │(Threats) │     │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘     │
└────────┼─────────────┼─────────────┼───────────┘
         │             │             │
         └─────────────┴─────────────┘
                       │
                       ▼
         ┌─────────────────────────┐
         │   AWS Security Lake     │
         │  (Centralized Data Lake)│
         │     - S3 Storage         │
         │     - Parquet Format     │
         │     - OCSF Schema        │
         └───────────┬─────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│   OpenSearch    │    │   Amazon Athena │
│  (SIEM Analysis)│    │  (SQL Queries)  │
└─────────────────┘    └─────────────────┘
```

**Terraform Configuration:**

```hcl
# security_lake.tf
resource "aws_securitylake_data_lake" "main" {
  region = "us-east-1"

  lifecycle_configuration {
    expiration {
      days = 365
    }

    transition {
      days          = 30
      storage_class = "GLACIER"
    }
  }

  replication_configuration {
    regions = ["us-west-2"]
    role_arn = aws_iam_role.security_lake_replication.arn
  }
}

resource "aws_securitylake_aws_log_source" "cloudtrail" {
  source_name    = "CLOUD_TRAIL_MGMT"
  source_version = "2.0"

  depends_on = [aws_securitylake_data_lake.main]
}

resource "aws_securitylake_aws_log_source" "vpc_flow" {
  source_name    = "VPC_FLOW"
  source_version = "2.0"

  depends_on = [aws_securitylake_data_lake.main]
}

resource "aws_securitylake_aws_log_source" "guardduty" {
  source_name    = "SH_FINDINGS"
  source_version = "2.0"

  depends_on = [aws_securitylake_data_lake.main]
}

# OpenSearch for SIEM analysis
resource "aws_opensearch_domain" "security_siem" {
  domain_name    = "security-siem"
  engine_version = "OpenSearch_2.11"

  cluster_config {
    instance_type  = "r6g.2xlarge.search"
    instance_count = 3

    zone_awareness_enabled = true
    zone_awareness_config {
      availability_zone_count = 3
    }
  }

  ebs_options {
    ebs_enabled = true
    volume_size = 1000
    volume_type = "gp3"
  }

  encrypt_at_rest {
    enabled = true
  }

  node_to_node_encryption {
    enabled = true
  }

  domain_endpoint_options {
    enforce_https       = true
    tls_security_policy = "Policy-Min-TLS-1-2-2019-07"
  }
}

# Lambda to forward Security Lake data to OpenSearch
resource "aws_lambda_function" "security_lake_to_opensearch" {
  filename      = "security_lake_forwarder.zip"
  function_name = "SecurityLakeToOpenSearch"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "index.handler"
  runtime       = "python3.11"
  timeout       = 300

  environment {
    variables = {
      OPENSEARCH_ENDPOINT = aws_opensearch_domain.security_siem.endpoint
      SECURITY_LAKE_BUCKET = aws_securitylake_data_lake.main.s3_bucket_arn
    }
  }
}

# S3 event notification to trigger Lambda
resource "aws_s3_bucket_notification" "security_lake_events" {
  bucket = aws_securitylake_data_lake.main.s3_bucket_arn

  lambda_function {
    lambda_function_arn = aws_lambda_function.security_lake_to_opensearch.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "aws-cloudtrail-logs/"
  }
}
```

---

### Pattern 4: Wazuh Open-Source SIEM

**Architecture:**

```
┌─────────────────────────────────────────────┐
│         Monitored Infrastructure             │
│                                              │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐   │
│  │Linux │  │Windows│ │Docker│  │Cloud │   │
│  │Server│  │Server │ │Host  │  │VMs   │   │
│  └───┬──┘  └───┬───┘ └───┬──┘  └───┬──┘   │
│      │  Wazuh  │  Wazuh  │  Wazuh  │      │
│      │  Agent  │  Agent  │  Agent  │      │
└──────┼─────────┼─────────┼─────────┼───────┘
       │         │         │         │
       └─────────┴─────────┴─────────┘
                     │
                     ▼
        ┌─────────────────────────┐
        │   Wazuh Manager         │
        │  - Event Analysis        │
        │  - Rule Engine           │
        │  - Alert Generation      │
        └───────────┬─────────────┘
                    │
                    ▼
        ┌─────────────────────────┐
        │  Wazuh Indexer          │
        │  (OpenSearch-based)     │
        └───────────┬─────────────┘
                    │
                    ▼
        ┌─────────────────────────┐
        │  Wazuh Dashboard        │
        │  (Kibana-based UI)      │
        └─────────────────────────┘
```

**Docker Compose Deployment:**

```yaml
# docker-compose.yml
version: '3.8'

services:
  wazuh-manager:
    image: wazuh/wazuh-manager:4.7.0
    hostname: wazuh-manager
    restart: always
    ports:
      - "1514:1514"     # Agent connection
      - "1515:1515"     # Agent registration
      - "514:514/udp"   # Syslog
      - "55000:55000"   # API
    environment:
      - INDEXER_URL=https://wazuh-indexer:9200
      - INDEXER_USERNAME=admin
      - INDEXER_PASSWORD=SecurePassword123
      - FILEBEAT_SSL_VERIFICATION_MODE=none
    volumes:
      - wazuh_api_configuration:/var/ossec/api/configuration
      - wazuh_etc:/var/ossec/etc
      - wazuh_logs:/var/ossec/logs
      - wazuh_queue:/var/ossec/queue
      - wazuh_ruleset:/var/ossec/ruleset

  wazuh-indexer:
    image: wazuh/wazuh-indexer:4.7.0
    hostname: wazuh-indexer
    restart: always
    ports:
      - "9200:9200"
    environment:
      - "OPENSEARCH_JAVA_OPTS=-Xms1g -Xmx1g"
      - "bootstrap.memory_lock=true"
      - "discovery.type=single-node"
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    volumes:
      - wazuh-indexer-data:/var/lib/wazuh-indexer

  wazuh-dashboard:
    image: wazuh/wazuh-dashboard:4.7.0
    hostname: wazuh-dashboard
    restart: always
    ports:
      - "443:5601"
    environment:
      - INDEXER_USERNAME=admin
      - INDEXER_PASSWORD=SecurePassword123
      - WAZUH_API_URL=https://wazuh-manager
      - API_USERNAME=wazuh-wui
      - API_PASSWORD=SecurePassword123
    depends_on:
      - wazuh-indexer
      - wazuh-manager
    links:
      - wazuh-indexer:wazuh-indexer
      - wazuh-manager:wazuh-manager

volumes:
  wazuh_api_configuration:
  wazuh_etc:
  wazuh_logs:
  wazuh_queue:
  wazuh_ruleset:
  wazuh-indexer-data:
```

**Wazuh Custom Rule (XML):**

```xml
<!-- /var/ossec/ruleset/rules/custom_ssh_rules.xml -->
<group name="ssh,authentication,">

  <!-- Rule: Multiple failed SSH login attempts -->
  <rule id="100001" level="10">
    <if_matched_sid>5710</if_matched_sid>
    <same_source_ip />
    <description>Multiple failed SSH login attempts from same source</description>
    <frequency>5</frequency>
    <timeframe>300</timeframe>
    <options>no_email_alert</options>
    <group>authentication_failed,brute_force_attack,</group>
  </rule>

  <!-- Rule: SSH login from unusual country -->
  <rule id="100002" level="8">
    <if_sid>5715</if_sid>
    <match>^Accepted publickey for</match>
    <srcgeoip>CN|RU|KP</srcgeoip>
    <description>SSH login from high-risk country</description>
    <group>authentication_success,geographic_anomaly,</group>
  </rule>

  <!-- Rule: Root login via SSH -->
  <rule id="100003" level="12">
    <if_sid>5715</if_sid>
    <match>^Accepted publickey for root</match>
    <description>Root login via SSH detected</description>
    <group>authentication_success,policy_violation,</group>
  </rule>

</group>
```

---

## Tool Recommendations

### Research Summary

**Research Date:** December 3, 2025
**Research Tools:** Google Search Grounding (Vertex AI), Context7
**Platforms Evaluated:** 8+ (Splunk, Elastic, Sentinel, Wazuh, AWS, GCP, IBM QRadar, CrowdStrike)

---

### SIEM Platforms (2025)

#### **Primary: Elastic SIEM** (Open-Source Foundation, Cloud or Self-Hosted)

**Library:** `/websites/elastic_co_reference`
**Trust Score:** High (Source Reputation)
**Code Snippets:** 26,603+
**Deployment:** Cloud (Elastic Cloud) or Self-Hosted

**Why Elastic SIEM?**

- **Open-Source Foundation:** Built on Elasticsearch (open-source), extensible and customizable
- **Unified XDR:** Extends detection across SIEM, endpoint (EDR), and cloud security
- **AI-Powered:** Elastic AI SOC Engine (EASE) for alert correlation, triage, and automated response
- **Detection-as-Code:** Extensive community-contributed detection rules (SIGMA, EQL)
- **Multi-Cloud:** Works across AWS, Azure, GCP, and on-premise
- **Cost-Effective:** Open-source option (ELK stack) or commercial with flexible pricing
- **Strong Community:** Large user base, active development, extensive documentation

**When to Use:**

- DevOps/engineering teams comfortable with Elasticsearch
- Multi-cloud or hybrid environments
- Need for customization and extensibility
- Want option to start open-source, add commercial features later
- Medium to large data volumes (100 GB - 10 TB/day)

**Limitations:**

- Steeper learning curve than Microsoft Sentinel
- Requires Elasticsearch expertise for advanced configurations
- Self-hosted option requires infrastructure management

**Installation (Elastic Cloud):**

```bash
# Sign up at cloud.elastic.co
# Create deployment (Security tier)
# Get deployment credentials

# Install Elastic Agent on endpoints
curl -L -O https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-8.11.0-linux-x86_64.tar.gz
tar xzvf elastic-agent-8.11.0-linux-x86_64.tar.gz
cd elastic-agent-8.11.0-linux-x86_64
sudo ./elastic-agent install \
  --url=https://your-deployment.elastic.cloud:443 \
  --enrollment-token=your-enrollment-token
```

**Example Detection Rule (EQL):**

```json
{
  "rule": {
    "name": "Suspicious PowerShell Download and Execute",
    "description": "Detects PowerShell downloading file and executing it",
    "type": "eql",
    "query": "sequence by user.name with maxspan=5m\n  [process where process.name == \"powershell.exe\" and \n   process.args : (\"Invoke-WebRequest\", \"iwr\", \"wget\")]\n  [process where process.parent.name == \"powershell.exe\"]",
    "severity": "high",
    "risk_score": 73,
    "mitre_attack": ["T1059.001", "T1105"]
  }
}
```

---

#### **Alternative: Microsoft Sentinel** (Cloud-Native SIEM for Azure)

**Platform:** Azure-native cloud SIEM
**Deployment:** Cloud-only (Azure)
**Pricing:** Pay-as-you-go, 50 GB commitment tier available

**Why Microsoft Sentinel?**

- **Cloud-Native:** Built on Azure, infinite scale, no infrastructure management
- **Azure Integration:** Seamless integration with Microsoft 365, Azure AD, Defender, Intune
- **Built-in SOAR:** Azure Logic Apps for automation (no separate product needed)
- **AI-Driven:** Microsoft threat intelligence, behavioral analytics, ML-based detection
- **Sentinel Graph:** Visual relationship mapping for attack path analysis
- **Cost-Effective for SMBs:** 50 GB commitment tier introduced for small organizations

**When to Use:**

- Heavy Azure/Microsoft 365 investment
- Want cloud-native, managed SIEM (no infrastructure)
- Need built-in SOAR capabilities
- Small to large organizations (scalable pricing)

**Limitations:**

- Azure-locked (limited multi-cloud support)
- Less customization than Elastic/Splunk
- Requires Azure expertise

**Setup (Azure CLI):**

```bash
# Create Log Analytics Workspace
az monitor log-analytics workspace create \
  --resource-group security-rg \
  --workspace-name security-sentinel \
  --location eastus

# Enable Microsoft Sentinel
az sentinel workspace create \
  --resource-group security-rg \
  --workspace-name security-sentinel

# Connect data sources
az sentinel data-connector create \
  --resource-group security-rg \
  --workspace-name security-sentinel \
  --name AzureActiveDirectory \
  --kind AzureActiveDirectory
```

**Example Detection Rule (KQL):**

```kql
// Detect multiple failed logins followed by success
let threshold = 5;
let timeframe = 10m;
SigninLogs
| where TimeGenerated > ago(1h)
| summarize
    FailedAttempts = countif(ResultType != 0),
    SuccessAttempts = countif(ResultType == 0)
    by UserPrincipalName, IPAddress, bin(TimeGenerated, timeframe)
| where FailedAttempts >= threshold and SuccessAttempts > 0
| project TimeGenerated, UserPrincipalName, IPAddress, FailedAttempts
```

---

#### **Alternative: Wazuh** (Free, Open-Source XDR/SIEM)

**Library:** `/wazuh/wazuh`
**Trust Score:** High (Source Reputation)
**Code Snippets:** 2,384+
**Deployment:** Self-hosted (on-premise or cloud VMs)

**Why Wazuh?**

- **Free and Open-Source:** Zero licensing costs, active community
- **XDR Capabilities:** Unified threat prevention, detection, and response
- **Multi-Platform:** Linux, Windows, macOS, Docker, Kubernetes, cloud VMs
- **Built-in Features:** File integrity monitoring, vulnerability detection, compliance (PCI DSS, HIPAA, GDPR)
- **Easy to Deploy:** Docker Compose, Ansible, Kubernetes Helm charts
- **Active Development:** Regular updates, responsive to security landscape

**When to Use:**

- Tight budget (startups, SMBs, non-profits)
- Want full control and customization
- Need compliance features (PCI DSS, HIPAA, GDPR, SOC 2)
- Comfortable managing infrastructure

**Limitations:**

- Fewer enterprise features than commercial SIEMs
- Requires self-hosting and maintenance
- Smaller ecosystem than Elastic/Splunk
- Less mature AI/ML capabilities

**Quick Start (Docker):**

```bash
# Clone Wazuh Docker repository
git clone https://github.com/wazuh/wazuh-docker.git
cd wazuh-docker/single-node

# Generate certificates
docker-compose -f generate-indexer-certs.yml run --rm generator

# Start Wazuh stack
docker-compose up -d

# Access dashboard: https://localhost
# Default credentials: admin / SecretPassword (change immediately)
```

---

#### **Enterprise: Splunk Enterprise Security**

**Platform:** Commercial SIEM (market leader)
**Deployment:** On-premise or Splunk Cloud

**Why Splunk?**

- **Market Leader:** Used by Fortune 100 companies
- **Scalability:** Proven at massive scale (petabytes)
- **Customization:** Extensive customization options, SPL query language
- **Ecosystem:** Thousands of integrations, apps, add-ons
- **Enterprise Support:** 24/7 support, professional services

**When to Use:**

- Large enterprises with unlimited budget
- Need for massive scale (TB/day+)
- Require enterprise support and SLAs
- Existing Splunk investment

**Limitations:**

- **Very expensive:** Licensing costs can be prohibitive
- Complex to deploy and manage
- Requires dedicated Splunk team
- Separate SOAR product (Splunk SOAR) adds cost

---

### Comparison Matrix: SIEM Platforms

| Criteria | Elastic SIEM | Microsoft Sentinel | Wazuh | Splunk ES |
|----------|-------------|-------------------|-------|-----------|
| **Cost** | $$$ (Cloud) / $$ (Open-Source) | $$$ (Pay-as-you-go) | $ (Free) | $$$$$ |
| **Deployment** | Cloud or Self-Hosted | Cloud-only | Self-Hosted | Cloud or On-Prem |
| **Scalability** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Ease of Use** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Customization** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **AI/ML** | ⭐⭐⭐⭐ (EASE) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Built-in SOAR** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ (Logic Apps) | ⭐⭐⭐ | ⭐⭐ (Separate) |
| **Community** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Multi-Cloud** | ⭐⭐⭐⭐⭐ | ⭐⭐ (Azure-focused) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Learning Curve** | Medium-High | Medium | Low-Medium | High |

---

### Log Aggregation Tools

#### **Primary: Fluentd** (Cloud-Native Log Aggregation)

**CNCF Project:** Graduated project, Kubernetes-native
**Use Case:** Cloud-native environments, Kubernetes, microservices

**Why Fluentd?**

- **Cloud-Native:** Designed for containerized environments
- **Unified Logging Layer:** Single interface for all log sources
- **Plugin Ecosystem:** 500+ plugins for inputs, outputs, filters
- **High Performance:** Fluent Bit (lightweight) for edge, Fluentd for aggregation
- **Kubernetes Integration:** Native DaemonSet deployment

**When to Use:**

- Kubernetes clusters
- Multi-cloud logging (AWS, Azure, GCP)
- Containerized applications (Docker, ECS, GKE, AKS)
- Need flexible log routing

```yaml
# Fluentd config example
<source>
  @type forward
  port 24224
</source>

<filter **>
  @type parser
  key_name message
  <parse>
    @type json
  </parse>
</filter>

<match security.**>
  @type elasticsearch
  host elasticsearch.svc.cluster.local
  port 9200
  index_name security-logs
  <buffer>
    @type file
    path /var/log/fluentd-buffers/security.buffer
    flush_interval 10s
  </buffer>
</match>
```

---

#### **Alternative: Logstash** (Elastic Stack Component)

**Part of:** ELK Stack (Elasticsearch, Logstash, Kibana)
**Use Case:** Elastic-based SIEM deployments

**Why Logstash?**

- **Native Elastic Integration:** Built for Elasticsearch
- **Rich Plugin Ecosystem:** 200+ input/filter/output plugins
- **Powerful Parsing:** Grok patterns for complex log formats
- **Data Enrichment:** GeoIP, DNS lookup, external API calls

**When to Use:**

- Already using Elasticsearch/Elastic SIEM
- Need advanced log parsing (grok patterns)
- Data enrichment requirements (GeoIP, threat intel lookup)

---

### Cost Optimization Tools

#### **S3 Glacier / Azure Archive** (Cold Storage)

**Use Case:** Long-term log retention for compliance

**Cost Comparison (1 TB storage, 1 year):**

| Storage Tier | AWS Cost | Azure Cost | Use Case |
|--------------|----------|------------|----------|
| **Hot (Elasticsearch)** | ~$1,200/year | ~$1,100/year | Real-time analysis |
| **Warm (S3 Standard)** | ~$276/year | ~$230/year | Occasional queries |
| **Cold (S3 Glacier)** | ~$48/year | ~$24/year | Compliance archive |

**Strategy:**

```
Real-time logs (7 days) → Hot (Elasticsearch)
Recent logs (30 days) → Warm (S3 Standard)
Archive (1 year) → Cold (Glacier Deep Archive)
Delete after 1 year (GDPR compliance)
```

---

## Skill Structure Design

### Skill File Organization

**Proposed Structure:**

```
siem-logging/
├── SKILL.md                          # Main skill file (<500 lines)
├── references/
│   ├── platform-comparison.md        # Splunk vs Elastic vs Sentinel vs Wazuh
│   ├── detection-rules-guide.md      # SIGMA, EQL, SPL, KQL examples
│   ├── log-retention-policies.md     # Compliance requirements, tiering
│   ├── cloud-native-logging.md       # AWS, Azure, GCP integrations
│   ├── alert-tuning-strategies.md    # False positive reduction
│   └── cost-optimization.md          # Hot/warm/cold storage, sampling
├── examples/
│   ├── sigma-rules/
│   │   ├── brute-force-detection.yml
│   │   ├── privilege-escalation.yml
│   │   ├── data-exfiltration.yml
│   │   └── lateral-movement.yml
│   ├── elastic-eql/
│   │   ├── process-injection.eql
│   │   ├── credential-dumping.eql
│   │   └── ransomware-behavior.eql
│   ├── microsoft-kql/
│   │   ├── failed-logins-multi-country.kql
│   │   ├── azure-resource-deletion.kql
│   │   └── email-forwarding-rule.kql
│   ├── splunk-spl/
│   │   ├── sql-injection-detection.spl
│   │   ├── suspicious-parent-child.spl
│   │   └── cloudtrail-anomaly.spl
│   ├── architectures/
│   │   ├── elk-stack-docker-compose.yml
│   │   ├── fluentd-kubernetes-daemonset.yaml
│   │   ├── aws-security-lake-terraform/
│   │   └── wazuh-docker-compose.yml
│   └── logstash-pipelines/
│       ├── security-logs.conf
│       ├── authentication.conf
│       └── network-traffic.conf
└── scripts/
    ├── sigma-to-elastic.sh           # Convert SIGMA to Elastic EQL
    └── cost-calculator.py             # Estimate SIEM costs
```

---

### SKILL.md Structure (Main File)

**Sections (Target: ~450 lines):**

1. **Frontmatter** (YAML)
   - name: siem-logging
   - description

2. **Purpose** (2-3 paragraphs)
   - What this skill teaches
   - When to use this skill

3. **SIEM Platform Selection** (~80 lines)
   - Quick decision tree
   - Platform comparison matrix
   - When to use Elastic vs Sentinel vs Wazuh vs Splunk
   - Link to references/platform-comparison.md

4. **Detection Rules Overview** (~100 lines)
   - SIGMA format (universal)
   - Platform-specific formats (EQL, KQL, SPL)
   - Example rule with explanation
   - Link to references/detection-rules-guide.md
   - Link to examples/sigma-rules/

5. **Log Aggregation Patterns** (~80 lines)
   - Centralized vs distributed architecture
   - Cloud-native logging (AWS, Azure, GCP)
   - Log shipping tools (Fluentd, Logstash, Filebeat)
   - Link to references/cloud-native-logging.md
   - Link to examples/architectures/

6. **Retention and Compliance** (~60 lines)
   - Compliance framework requirements
   - Hot/warm/cold storage tiering
   - Cost optimization strategies
   - Link to references/log-retention-policies.md
   - Link to references/cost-optimization.md

7. **Alert Tuning** (~60 lines)
   - Noise reduction techniques
   - False positive management
   - Alert metrics and KPIs
   - Link to references/alert-tuning-strategies.md

8. **Quick Start Examples** (~50 lines)
   - Deploy Wazuh with Docker Compose
   - Set up Elastic Cloud trial
   - Create first SIGMA detection rule
   - Link to examples/

9. **Reference Links** (~20 lines)
   - Links to detailed references/ files
   - Links to examples/ files
   - Official documentation (Elastic, Sentinel, Wazuh, Splunk)

---

### Progressive Disclosure Strategy

**Main SKILL.md Contains:**

- High-level platform selection guidance (decision tree)
- Quick-start detection rule examples (1-2 SIGMA rules)
- Architecture pattern overview (centralized vs distributed)
- Links to detailed references and examples

**References/ Contains:**

- Detailed platform comparison (features, pricing, use cases)
- Comprehensive detection rule guide (SIGMA, EQL, KQL, SPL)
- In-depth log retention policies by compliance framework
- Cloud-native logging setup guides (AWS, Azure, GCP, Kubernetes)
- Alert tuning strategies and metrics
- Cost optimization techniques

**Examples/ Contains:**

- Working SIGMA rules (copy-paste ready)
- Platform-specific detection queries
- Complete architecture deployments (Docker Compose, Kubernetes, Terraform)
- Logstash pipeline configurations

**Scripts/ Contains:**

- SIGMA rule converter (SIGMA → EQL/KQL/SPL)
- Cost calculator for estimating SIEM expenses

---

## Integration Points

### Integration with Existing Skills

#### 1. **observability** Skill

**Overlap:** Both deal with logging, but different purposes

**SIEM Logging (This Skill):**
- Security events (authentication, authorization, network threats)
- Threat detection and incident response
- Compliance and audit trails

**Observability Skill:**
- Application performance (metrics, traces, logs)
- System health and uptime
- Performance optimization

**Integration:**

```yaml
# Shared logging infrastructure (Fluentd)
# Route security logs to SIEM, performance logs to observability platform

<match security.**>
  @type elasticsearch
  host siem-elasticsearch.company.com
  index_name security-logs
</match>

<match application.**>
  @type elasticsearch
  host observability-elasticsearch.company.com
  index_name application-logs
</match>
```

---

#### 2. **incident-management** Skill

**Integration:** SIEM alerts trigger incident response workflows

**Workflow:**

```
1. SIEM detects threat (e.g., brute force attack)
2. Alert sent to incident management platform (PagerDuty, Opsgenie)
3. Incident created automatically
4. Security analyst investigates using SIEM
5. Incident resolved, documented
6. SIEM rule tuned based on findings
```

**Example (Elastic → PagerDuty):**

```json
{
  "actions": [
    {
      "group": "default",
      "id": "pagerduty-incident",
      "params": {
        "summary": "{{context.rule.name}}",
        "severity": "{{context.rule.severity}}",
        "eventAction": "trigger",
        "dedupKey": "{{alert.id}}",
        "class": "security",
        "component": "elastic-siem"
      }
    }
  ]
}
```

---

#### 3. **security-hardening** Skill

**Integration:** SIEM monitors security configurations and detects misconfigurations

**Use Case:**

- Security hardening skill: Implements CIS benchmarks, disables unnecessary services
- SIEM logging skill: Monitors for compliance violations, detects configuration drift

**Example Detection Rule:**

```yaml
# SIGMA rule: Detect SSH running on non-standard port
title: SSH Service on Non-Standard Port
logsource:
  category: process_creation
  product: linux
detection:
  selection:
    process.name: sshd
    process.args: '-p'
  filter_standard:
    process.args: '22'
  condition: selection and not filter_standard
level: medium
```

---

#### 4. **building-ci-pipelines** Skill

**Integration:** CI/CD pipelines generate security-relevant events

**Events to Log:**

- Code commits (who, when, what repository)
- Build executions (success/failure, dependencies installed)
- Deployment events (what, where, by whom)
- Secrets access (vault reads, credential usage)
- Container image builds and pushes

**Example (GitHub Actions → SIEM):**

```yaml
# .github/workflows/security-logging.yml
name: Log Security Events to SIEM

on:
  push:
  pull_request:
  deployment:

jobs:
  log-to-siem:
    runs-on: ubuntu-latest
    steps:
      - name: Send event to SIEM
        run: |
          curl -X POST https://logstash.company.com:5044 \
            -H "Content-Type: application/json" \
            -d '{
              "event_type": "${{ github.event_name }}",
              "repository": "${{ github.repository }}",
              "actor": "${{ github.actor }}",
              "ref": "${{ github.ref }}",
              "sha": "${{ github.sha }}",
              "timestamp": "${{ github.event.head_commit.timestamp }}"
            }'
```

---

#### 5. **secret-management** Skill

**Integration:** Log all secrets access for audit trails

**Events to Log:**

- Secrets read/write operations
- Secrets rotation events
- Access denials
- Secrets expiration warnings

**Example (HashiCorp Vault Audit Logs → SIEM):**

```hcl
# Vault audit log configuration
audit {
  type = "file"
  options = {
    file_path = "/var/log/vault/audit.log"
    format = "json"
  }
}
```

```ruby
# Logstash pipeline for Vault logs
input {
  file {
    path => "/var/log/vault/audit.log"
    type => "vault_audit"
    codec => "json"
  }
}

filter {
  if [type] == "vault_audit" {
    mutate {
      add_field => {
        "security_category" => "secrets_access"
        "severity" => "high"
      }
    }
  }
}

output {
  elasticsearch {
    hosts => ["https://siem-elasticsearch:9200"]
    index => "vault-audit-logs-%{+YYYY.MM.dd}"
  }
}
```

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1)

**Deliverables:**

- [x] Complete init.md (this document)
- [ ] Create SKILL.md main file
- [ ] Write references/platform-comparison.md
- [ ] Write references/detection-rules-guide.md

**Content Focus:**

- SIEM platform selection guidance
- Detection rule formats (SIGMA, EQL, KQL, SPL)
- Quick-start examples

---

### Phase 2: Detection Rules (Week 2)

**Deliverables:**

- [ ] Create 10+ SIGMA rule examples
- [ ] Create Elastic EQL examples
- [ ] Create Microsoft KQL examples
- [ ] Create Splunk SPL examples
- [ ] Write references/alert-tuning-strategies.md

**Files:**

- examples/sigma-rules/ (10+ rules)
- examples/elastic-eql/ (5+ queries)
- examples/microsoft-kql/ (5+ queries)
- examples/splunk-spl/ (5+ queries)

---

### Phase 3: Architecture Patterns (Week 3)

**Deliverables:**

- [ ] ELK Stack Docker Compose example
- [ ] Fluentd Kubernetes DaemonSet example
- [ ] AWS Security Lake Terraform example
- [ ] Wazuh Docker Compose example
- [ ] Write references/cloud-native-logging.md

**Files:**

- examples/architectures/elk-stack-docker-compose.yml
- examples/architectures/fluentd-kubernetes-daemonset.yaml
- examples/architectures/aws-security-lake-terraform/
- examples/architectures/wazuh-docker-compose.yml

---

### Phase 4: Compliance & Retention (Week 4)

**Deliverables:**

- [ ] Write references/log-retention-policies.md
- [ ] Write references/cost-optimization.md
- [ ] Create cost calculator script
- [ ] Document compliance requirements (GDPR, HIPAA, PCI DSS, SOC 2)

**Files:**

- scripts/cost-calculator.py
- references/log-retention-policies.md (compliance matrix)

---

### Phase 5: Integration & Polish (Week 5)

**Deliverables:**

- [ ] Create SIGMA converter script (SIGMA → EQL/KQL/SPL)
- [ ] Cross-link with related skills (observability, incident-management, security-hardening)
- [ ] Logstash pipeline examples
- [ ] Final review and testing

**Files:**

- scripts/sigma-to-elastic.sh
- examples/logstash-pipelines/ (3+ configs)

---

## Validation Checklist

### Before Creating SKILL.md

- [x] Research complete (Google Search Grounding, Context7)
- [x] SIEM platform comparison validated
- [x] Detection rule formats researched (SIGMA, EQL, KQL, SPL)
- [x] Architecture patterns designed
- [x] Integration points with other skills mapped

### Before Finalizing Skill

- [ ] SKILL.md under 500 lines
- [ ] All references/ files created
- [ ] All examples/ files working and tested
- [ ] Progressive disclosure effective (main → references → examples)
- [ ] Detection rules validated across platforms
- [ ] Architecture examples deployable
- [ ] Cost calculator functional
- [ ] Integration with related skills verified

---

## Success Metrics

**This skill is successful if security engineers can:**

1. **Select Right SIEM Platform:**
   - Choose between Elastic, Sentinel, Wazuh, Splunk based on budget, scale, and requirements
   - Understand cost implications and architectural trade-offs

2. **Write Effective Detection Rules:**
   - Create SIGMA rules (universal format)
   - Convert SIGMA to platform-specific formats (EQL, KQL, SPL)
   - Map rules to MITRE ATT&CK framework

3. **Design Scalable Architecture:**
   - Implement centralized or distributed logging based on requirements
   - Set up cloud-native logging (AWS, Azure, GCP, Kubernetes)
   - Configure log aggregation tools (Fluentd, Logstash)

4. **Meet Compliance Requirements:**
   - Implement retention policies for GDPR, HIPAA, PCI DSS, SOC 2
   - Set up hot/warm/cold storage tiering
   - Calculate and optimize SIEM costs

5. **Tune Alerts Effectively:**
   - Reduce false positives through whitelisting and threshold tuning
   - Achieve >30% true positive rate
   - Integrate with incident response workflows

6. **Deploy Working SIEM:**
   - Deploy Wazuh, ELK stack, or cloud SIEM (Sentinel, Elastic Cloud)
   - Configure data sources and detection rules
   - Set up dashboards and alerting

---

## Future Enhancements

**Potential Additions (Not in Initial Release):**

1. **SOAR Integration**
   - Automated response playbooks
   - Integration with Splunk SOAR, Azure Logic Apps, Tines
   - Incident orchestration workflows

2. **Threat Intelligence Integration**
   - TIP (Threat Intelligence Platform) integration
   - STIX/TAXII feeds
   - Automated IOC enrichment

3. **User and Entity Behavior Analytics (UEBA)**
   - Baseline normal behavior
   - Detect anomalies (impossible travel, unusual access patterns)
   - Insider threat detection

4. **Security Data Lake Architecture**
   - AWS Security Lake deep dive
   - OCSF (Open Cybersecurity Schema Framework)
   - Multi-SIEM federation

5. **Advanced Detection Techniques**
   - Machine learning for anomaly detection
   - Behavior-based detection
   - Threat hunting methodologies

---

## Appendix: MITRE ATT&CK Mapping

**Top 10 Techniques to Detect:**

| MITRE Technique | Technique Name | SIGMA Rule | SIEM Platform |
|-----------------|---------------|------------|---------------|
| **T1078** | Valid Accounts | Detect unusual login patterns | All |
| **T1059.001** | PowerShell | Malicious PowerShell commands | All |
| **T1003** | Credential Dumping | Mimikatz, registry access | All |
| **T1021.001** | Remote Desktop | RDP from unusual sources | All |
| **T1071** | Application Layer Protocol | C2 communication via HTTP/DNS | All |
| **T1105** | Ingress Tool Transfer | File downloads from internet | All |
| **T1486** | Data Encrypted for Impact | Ransomware file encryption | All |
| **T1087** | Account Discovery | Enumeration commands | All |
| **T1098** | Account Manipulation | Privilege escalation | All |
| **T1562.001** | Disable Security Tools | Stopping AV, SIEM agents | All |

---

## References

**Research Sources:**

- **Google Search Grounding (Vertex AI):** SIEM tools comparison 2025, security logging best practices
- **Context7 Documentation:** Elasticsearch (/websites/elastic_co_reference), Wazuh (/wazuh/wazuh)
- **Official Documentation:**
  - Elastic SIEM: https://www.elastic.co/security
  - Microsoft Sentinel: https://azure.microsoft.com/en-us/products/microsoft-sentinel
  - Wazuh: https://wazuh.com/
  - Splunk Enterprise Security: https://www.splunk.com/en_us/products/enterprise-security.html
- **SIGMA Rules:** https://github.com/SigmaHQ/sigma
- **MITRE ATT&CK:** https://attack.mitre.org/

**Related Skills:**

- `observability` - Application performance monitoring, metrics, traces
- `incident-management` - Incident response workflows, playbooks
- `security-hardening` - Security configurations, CIS benchmarks
- `building-ci-pipelines` - CI/CD security logging
- `secret-management` - Secrets access audit trails

---

**Document Status:** ✅ Complete
**Next Step:** Create SKILL.md from this master plan
**Owner:** AI Design Components Project
**Last Updated:** December 3, 2025
