---
sidebar_position: 4
title: SIEM & Logging
description: Master plan for SIEM and centralized logging including detection rules, log aggregation, and security monitoring
tags: [master-plan, security, siem, logging, detection, monitoring]
---

# SIEM & Logging

:::info Status
**Master Plan** - Comprehensive init.md complete, ready for SKILL.md implementation
:::

Security Information and Event Management (SIEM) provides centralized logging, threat detection, and incident response. This skill covers SIEM architecture, detection rule patterns, log aggregation strategies, and security monitoring best practices.

## Scope

This skill teaches:

- **SIEM Architecture** - Centralized logging, correlation engines, detection rules
- **Log Aggregation** - Collection from distributed systems (ELK, Splunk, Sentinel)
- **Detection Rules** - SIGMA rules, custom detection logic, threat hunting
- **Log Sources** - Application logs, infrastructure logs, security logs
- **Retention and Compliance** - Log retention policies, immutable logs
- **Incident Response** - Alert triage, investigation playbooks, SOAR integration

## Key Components

### SIEM Platforms

**Elastic Security (ELK Stack)**
- Elasticsearch (storage), Logstash (ingestion), Kibana (visualization)
- Open source with commercial features
- Pre-built detection rules
- Best for: Self-hosted, customizable, cost-sensitive

**Splunk**
- Commercial SIEM platform
- Powerful search (SPL)
- Extensive integrations
- Best for: Enterprise, mature security teams

**Azure Sentinel**
- Cloud-native SIEM (Microsoft)
- KQL query language
- Tight Azure integration
- Best for: Azure-heavy environments

**Chronicle Security**
- Google Cloud SIEM
- Petabyte-scale log retention
- BigQuery backend
- Best for: GCP-heavy, massive scale

### Log Sources

**Infrastructure Logs:**
- VPC flow logs (network traffic)
- Load balancer access logs
- Firewall logs
- DNS query logs

**Application Logs:**
- Application errors and exceptions
- Authentication/authorization events
- API access logs
- Database audit logs

**Security Logs:**
- IDS/IPS alerts
- Antivirus/EDR detections
- WAF alerts
- Vulnerability scan results

**Cloud Provider Logs:**
- AWS CloudTrail (API calls)
- GCP Cloud Audit Logs
- Azure Activity Logs

### Detection Rule Patterns

**SIGMA Rules** (Universal Detection Format)
```yaml
title: Suspicious PowerShell Execution
description: Detects PowerShell with suspicious parameters
logsource:
  product: windows
  service: powershell
detection:
  selection:
    EventID: 4104
    ScriptBlockText|contains:
      - '-encodedcommand'
      - 'Invoke-Expression'
      - 'DownloadString'
  condition: selection
level: high
```

**Common Detection Patterns:**
- **Brute Force:** Multiple failed logins followed by success
- **Data Exfiltration:** Large outbound data transfers to unusual destinations
- **Privilege Escalation:** sudo/admin commands from unexpected users
- **Lateral Movement:** Unusual internal network connections
- **Command and Control:** Beaconing patterns, DNS tunneling

### Log Aggregation Architecture

**Centralized Pattern:**
```
Application → Log Shipper → SIEM → Alerts
     │            │           │        │
     ▼            ▼           ▼        ▼
Container    Fluentd/    Elasticsearch  PagerDuty
logs         Filebeat    + Kibana      /Slack
```

**Distributed Pattern (High Scale):**
```
Apps → Kafka → Stream Processors → SIEM
  │      │          │                 │
  ▼      ▼          ▼                 ▼
1000s  Buffer   Enrichment,       Long-term
logs/sec        filtering         storage
```

## Decision Framework

**Which SIEM Platform?**

```
Budget / cost?
  Limited → Elastic Security (open source)
  Enterprise → Splunk OR Azure Sentinel

Cloud provider?
  AWS → Elastic on EC2 OR Splunk Cloud
  Azure → Azure Sentinel (native)
  GCP → Chronicle Security (native)

Scale / log volume?
  < 1 TB/day → Elastic OR Splunk
  > 1 TB/day → Chronicle OR Splunk Enterprise

Team expertise?
  Open source preference → Elastic
  Prefer commercial support → Splunk/Sentinel
```

**Log Retention Policy:**

```
Compliance requirements?
  PCI-DSS → 1 year minimum
  HIPAA → 6 years minimum
  SOC 2 → 1 year minimum
  GDPR → Varies (document retention policy)

Storage cost optimization?
  Hot storage (0-30 days): Fast queries, expensive
  Warm storage (30-90 days): Slower queries, medium cost
  Cold storage (90+ days): Archive, cheapest
```

**Alert Severity Levels:**

| Level | Response Time | Example |
|-------|---------------|---------|
| **Critical** | Immediate (24/7) | Active breach, ransomware |
| **High** | < 1 hour | Brute force successful, privilege escalation |
| **Medium** | < 4 hours | Multiple failed logins, suspicious scanning |
| **Low** | Next business day | Policy violations, unusual behavior |

## Tool Recommendations

### Log Shippers

**Fluentd/Fluent Bit:**
- Cloud-native log forwarding
- 500+ plugins
- Kubernetes native

**Filebeat (Elastic):**
- Lightweight log shipper
- Elastic Stack integration
- Modules for common log formats

**Vector (Datadog):**
- High-performance log router
- Transform and filter logs
- Multiple output destinations

### SIEM Platforms

**Open Source:**
- Elastic Security + ELK Stack
- Wazuh (host-based intrusion detection)
- OSSEC (file integrity monitoring)

**Commercial:**
- Splunk Enterprise/Cloud
- Azure Sentinel
- Chronicle Security (Google)
- IBM QRadar
- LogRhythm

### Detection Rule Libraries

**SIGMA Rules:**
- https://github.com/SigmaHQ/sigma
- Universal detection rule format
- Convert to SIEM-specific queries

**Elastic Detection Rules:**
- Pre-built rules for common attacks
- MITRE ATT&CK mapping

**Falco Rules:**
- Runtime security for Kubernetes
- Detect anomalous container behavior

## Integration Points

**With Other Skills:**
- `implementing-observability` - Application metrics and traces (complementary to logs)
- `architecting-security` - Implement detective security controls
- `implementing-compliance` - Log retention for compliance
- `incident-response` - Alert triage and investigation
- `operating-kubernetes` - Container and K8s logs

**Workflow Example:**
```
Logs Generated → Aggregation → Detection → Alert → Incident Response
       │              │           │         │            │
       ▼              ▼           ▼         ▼            ▼
   App logs      Fluentd →   SIGMA    PagerDuty    Security
   VPC flows     Kafka       rules    notification  team
                                                    investigation
```

## Learn More

- [Full Master Plan (init.md)](https://github.com/ancoleman/ai-design-components/blob/main/skills/siem-logging/init.md)
- Related: `implementing-observability`, `architecting-security`, `implementing-compliance`
