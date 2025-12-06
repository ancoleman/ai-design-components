# Log Retention Policies

## Table of Contents

- [Compliance Framework Requirements](#compliance-framework-requirements)
- [Storage Tiering Strategy](#storage-tiering-strategy)
- [Retention Policy Examples](#retention-policy-examples)
- [Index Lifecycle Management (ILM)](#index-lifecycle-management-ilm)
- [Data Minimization Strategies](#data-minimization-strategies)
- [GDPR-Specific Requirements](#gdpr-specific-requirements)
- [Summary](#summary)

## Compliance Framework Requirements

| Framework | Minimum Retention | Key Requirements | Penalties for Non-Compliance |
|-----------|------------------|------------------|------------------------------|
| **GDPR** | 30-90 days (varies) | Right to be forgotten, data minimization, encryption | Up to €20M or 4% of revenue |
| **HIPAA** | 6 years | Encryption at rest and in transit, access controls, audit trails | Up to $1.5M/year |
| **PCI DSS** | 1 year | Log integrity, tamper-proof storage, quarterly reviews | Up to $100k/month fines |
| **SOC 2** | 1 year | Access controls, encryption, audit trail | Loss of certification |
| **NIST 800-53** | Varies by control | Comprehensive logging, 90-day retention minimum | Federal contract loss |

## Storage Tiering Strategy

### Hot Tier (Real-Time Analysis)

**Duration:** Last 7-30 days
**Storage:** SSD, high-IOPS
**Cost:** $0.10-0.15/GB/month
**Use Cases:**
- Real-time threat detection
- Active incident investigation
- Dashboard queries
- Frequent searches

### Warm Tier (Recent History)

**Duration:** 30-90 days
**Storage:** HDD, lower IOPS
**Cost:** $0.03-0.05/GB/month
**Use Cases:**
- Occasional threat hunting
- Weekly/monthly reports
- Historical trend analysis
- Non-urgent investigations

### Cold Tier (Compliance Archive)

**Duration:** 90 days to retention limit
**Storage:** S3 Glacier, Azure Cool Blob
**Cost:** $0.004-0.01/GB/month
**Use Cases:**
- Compliance audit requirements
- Legal discovery
- Rare searches (acceptable latency)
- Long-term retention

## Retention Policy Examples

### Startup (Moderate Budget)

```yaml
Data Volume: 50 GB/day
Retention: 90 days (SOC 2 Type II)

Hot Tier (7 days): 350 GB @ $0.10 = $35/month
Warm Tier (30 days): 1.5 TB @ $0.05 = $75/month
Cold Tier (53 days): 2.65 TB @ $0.01 = $26.50/month

Total Cost: $136.50/month ($1,638/year)
```

### Mid-Market (Healthcare, HIPAA)

```yaml
Data Volume: 200 GB/day
Retention: 6 years (HIPAA)

Hot Tier (30 days): 6 TB @ $0.10 = $600/month
Warm Tier (90 days): 18 TB @ $0.05 = $900/month
Cold Tier (6 years): 425 TB @ $0.01 = $4,250/month

Total Cost: $5,750/month ($69,000/year)
```

### Enterprise (Financial Services, PCI DSS)

```yaml
Data Volume: 1 TB/day
Retention: 1 year (PCI DSS)

Hot Tier (30 days): 30 TB @ $0.10 = $3,000/month
Warm Tier (90 days): 90 TB @ $0.05 = $4,500/month
Cold Tier (245 days): 245 TB @ $0.01 = $2,450/month

Total Cost: $9,950/month ($119,400/year)
```

## Index Lifecycle Management (ILM)

### Elastic ILM Policy

```json
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_size": "50GB",
            "max_age": "7d"
          },
          "set_priority": {
            "priority": 100
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
          },
          "set_priority": {
            "priority": 50
          }
        }
      },
      "cold": {
        "min_age": "90d",
        "actions": {
          "searchable_snapshot": {
            "snapshot_repository": "security-snapshots"
          },
          "set_priority": {
            "priority": 0
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

### Microsoft Sentinel Retention

```bash
# Azure CLI: Configure 90-day interactive retention, 1-year total
az monitor log-analytics workspace update \
  --resource-group security-rg \
  --workspace-name security-sentinel \
  --retention-time 365 \
  --total-retention-time 365
```

## Data Minimization Strategies

### Log Sampling

**When to Use:** High-volume non-critical logs (info/debug level)

```yaml
# Fluentd sampling (keep 10%)
<filter application.info>
  @type sampling
  @id sample_info_logs
  interval 10
  sample_rate 1
</filter>
```

### Selective Field Retention

**Example:** Strip PII from logs before storage

```ruby
# Logstash: Remove sensitive fields
filter {
  mutate {
    remove_field => ["credit_card", "ssn", "password"]
  }

  # Mask email addresses
  mutate {
    gsub => [
      "message", "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL_REDACTED]"
    ]
  }
}
```

### Aggregation Before Storage

**Example:** Store aggregated metrics, not raw logs

```yaml
# Store: "200 failed logins from 10.0.0.1 in last hour"
# Instead of: 200 individual log entries
```

## GDPR-Specific Requirements

### Right to Be Forgotten

```bash
# Elasticsearch: Delete user data
POST /security-logs/_delete_by_query
{
  "query": {
    "term": {
      "user.email": "user@example.com"
    }
  }
}
```

### Data Anonymization

```python
# Python: Anonymize IP addresses
import hashlib

def anonymize_ip(ip_address, salt="secret"):
    return hashlib.sha256(f"{ip_address}{salt}".encode()).hexdigest()[:16]

# 192.168.1.100 → 7a8f9d3c2b1e4f6a
```

### Consent Management

- Log user consent for data collection
- Track data processing purposes
- Enable audit trails for data access
- Implement data export capabilities

## Summary

**Critical Retention Requirements:**
- GDPR: 30-90 days (minimize data, enable deletion)
- HIPAA: 6 years (healthcare, encryption required)
- PCI DSS: 1 year (payment data, quarterly reviews)
- SOC 2: 1 year (varies by security control)

**Cost Optimization:**
- Use hot/warm/cold tiering (saves 70-80%)
- Sample non-critical logs (reduces volume 50-90%)
- Strip PII before storage (compliance + cost savings)
- Aggregate before storing (reduces volume 80-95%)

**Implementation:**
- Use Index Lifecycle Management (Elastic, Splunk)
- Configure Azure Sentinel retention policies
- Implement S3 lifecycle rules for AWS Security Lake
- Automate data deletion after retention period
