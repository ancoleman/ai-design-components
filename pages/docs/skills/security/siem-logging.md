---
sidebar_position: 6
title: SIEM Logging
description: Configure SIEM systems for threat detection, log aggregation, and compliance
tags: [security, siem, logging, threat-detection, elastic, sentinel, wazuh, splunk]
---

# SIEM Logging

Configure comprehensive security logging infrastructure using SIEM platforms (Elastic SIEM, Microsoft Sentinel, Wazuh, Splunk) to detect threats, investigate incidents, and maintain compliance audit trails.

## When to Use

Use this skill when:
- Implementing centralized security event monitoring across infrastructure
- Writing threat detection rules for authentication failures, privilege escalation, data exfiltration
- Designing log aggregation for multi-cloud environments (AWS, Azure, GCP, Kubernetes)
- Meeting compliance requirements for log retention and audit trails
- Tuning security alerts to reduce false positives and alert fatigue
- Calculating costs for high-volume security logging (TB/day scale)
- Integrating security logging with incident response workflows

## Key Features

**SIEM Platform Selection:**
- **Elastic SIEM**: Multi-cloud, customization needs, DevOps teams ($$$ cloud/self-hosted)
- **Microsoft Sentinel**: Azure-heavy orgs, built-in SOAR, cloud-first ($$$ cloud)
- **Wazuh**: Cost-conscious, SMBs, compliance requirements (Free, self-hosted)
- **Splunk ES**: Large enterprises, massive scale, unlimited budget ($$$$$ cloud/on-prem)

**Detection Rules:**
- **SIGMA**: Universal format compiling to any SIEM (Elastic EQL, Splunk SPL, Microsoft KQL)
- **Elastic EQL**: Event Query Language for sequence-based detection
- **Microsoft KQL**: Kusto Query Language for Azure Sentinel
- **Splunk SPL**: Search Processing Language for Splunk queries

**Log Retention & Compliance:**
- **Hot Tier (7-30 days)**: Real-time indexing, fast queries ($0.10/GB/month)
- **Warm Tier (30-90 days)**: Read-only indices, occasional searches ($0.05/GB/month)
- **Cold Tier (90 days+)**: Searchable snapshots, rare queries ($0.01/GB/month)
- **Compliance**: GDPR (30-90d), HIPAA (6 years), PCI-DSS (1 year), SOC 2 (1 year)

**Alert Tuning:**
- Target metrics: &lt;100 alerts/day, &gt;30% true positive rate, &lt;15 min MTTI
- Noise reduction: Whitelisting, threshold tuning, multi-event correlation
- Lifecycle: Create → Baseline (2-4 weeks) → Tune → Continuous improvement

## Quick Start

```yaml
# SIGMA Rule: Brute Force Detection
title: Multiple Failed Login Attempts from Single Source
id: 8a9e3c7f-4b2d-4e8a-9f1c-2d5e6f7a8b9c
status: stable
description: Detects potential brute force attacks (10+ failed logins in 10 minutes)
author: Security Team
date: 2025/12/03
references:
  - https://attack.mitre.org/techniques/T1110/
tags:
  - attack.credential_access
  - attack.t1110
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

**Compile SIGMA to Platform-Specific:**

```bash
# Install SIGMA compiler
pip install sigma-cli

# Compile to Elastic EQL
sigmac -t es-eql sigma_rule.yml

# Compile to Splunk SPL
sigmac -t splunk sigma_rule.yml

# Compile to Microsoft KQL
sigmac -t kusto sigma_rule.yml
```

**Elastic EQL Sequence Detection:**

```eql
sequence by user.name with maxspan=5m
  [process where process.name == "powershell.exe" and
   process.args : ("Invoke-WebRequest", "iwr", "wget")]
  [process where process.parent.name == "powershell.exe"]
```

**Microsoft Sentinel KQL:**

```kql
SigninLogs
| where TimeGenerated > ago(1h)
| where ResultType != 0  // Failed login
| summarize FailedAttempts=count() by UserPrincipalName, IPAddress
| where FailedAttempts >= 10
```

**Deploy Wazuh (Free SIEM):**

```bash
git clone https://github.com/wazuh/wazuh-docker.git
cd wazuh-docker/single-node
docker-compose up -d
# Access: https://localhost:443 (admin/admin)
```

## What to Log (Security Events)

**Critical Events (MUST LOG):**
- **Authentication**: Login attempts, MFA, password changes, privilege escalation
- **Authorization**: Permission changes, role modifications, access denials
- **Data Access**: Sensitive database/file access, API calls, exports
- **Network**: Connections, firewall denials, VPN, DNS queries
- **System**: Service changes, configuration modifications, software installations

**Severity Levels:**
- Failed auth (3+): HIGH alert
- Privilege escalation: CRITICAL alert
- Data export: HIGH alert
- Config change: MEDIUM (no alert)

## Cost Optimization Example

```
500 GB/day log volume, 1-year retention

Hot (30 days):   15 TB @ $0.10/GB = $1,500/month
Warm (60 days):  30 TB @ $0.05/GB = $1,500/month
Cold (275 days): 137.5 TB @ $0.01/GB = $1,375/month

Total: $4,375/month = $52,500/year

vs. Hot-only: $18,250/month = $219,000/year
Savings: 76% ($166,500/year)
```

## Related Skills

- [Security Architecture](./architecting-security.md) - Implement security monitoring architecture
- [Implementing Compliance](./implementing-compliance.md) - Log retention for compliance requirements
- [Configuring Firewalls](./configuring-firewalls.md) - Monitor firewall events and denials
- [Managing Vulnerabilities](./managing-vulnerabilities.md) - Monitor vulnerability remediation activities

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/siem-logging)
- [Master Plan](../../master-plans/security/siem-logging.md)
