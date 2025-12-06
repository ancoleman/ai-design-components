# Compliance and Retention Requirements

## Table of Contents

1. [Common Regulatory Frameworks](#common-regulatory-frameworks)
2. [Retention Policy Implementation](#retention-policy-implementation)
3. [Immutable Backups for Ransomware Protection](#immutable-backups-for-ransomware-protection)
4. [Compliance Reporting](#compliance-reporting)

## Common Regulatory Frameworks

| Regulation | Retention Period | Data Types | Requirements |
|------------|------------------|------------|--------------|
| **GDPR** | Varies (1-7 years typical) | Personal data | EU data residency, right to erasure |
| **SOC 2** | 1 year minimum | Audit logs, backups | Secure deletion, access controls |
| **HIPAA** | 6 years | PHI, audit logs | Encryption at rest/transit |
| **PCI DSS** | 3 months (logs), 1 year (audit) | Cardholder data | Secure deletion, quarterly reviews |
| **FINRA** | 6 years | Financial records | WORM storage for some data |

## Retention Policy Implementation

### S3 Lifecycle Example

```bash
aws s3api put-bucket-lifecycle-configuration \
  --bucket compliance-backups \
  --lifecycle-configuration '{
    "Rules": [
      {
        "Id": "compliance-retention",
        "Status": "Enabled",
        "Transitions": [
          {"Days": 30, "StorageClass": "STANDARD_IA"},
          {"Days": 90, "StorageClass": "GLACIER"},
          {"Days": 365, "StorageClass": "DEEP_ARCHIVE"}
        ],
        "Expiration": {"Days": 2555}
      }
    ]
  }'
```

### GCS Retention Lock

```bash
gsutil retention set 7y gs://compliance-backups
gsutil retention lock gs://compliance-backups
```

## Immutable Backups for Ransomware Protection

### S3 Object Lock

```hcl
resource "aws_s3_bucket_object_lock_configuration" "backups" {
  bucket = aws_s3_bucket.backups.id

  rule {
    default_retention {
      mode = "GOVERNANCE"  # or "COMPLIANCE"
      days = 30
    }
  }
}
```

### Azure Immutable Blob Storage

```hcl
resource "azurerm_storage_container" "backups" {
  name                  = "backups"
  storage_account_name  = azurerm_storage_account.main.name
  
  immutability_policy {
    period_since_creation_in_days = 30
    state                         = "Locked"
  }
}
```

## Compliance Reporting

### Backup Compliance Report Script

```bash
#!/bin/bash
# scripts/generate-dr-report.sh

echo "DR Compliance Report - $(date)"
echo "================================"

# Check backup age
LAST_BACKUP=$(aws s3 ls s3://backups/ | tail -1 | awk '{print $1" "$2}')
BACKUP_AGE=$(( ($(date +%s) - $(date -d "$LAST_BACKUP" +%s)) / 3600 ))

if [ $BACKUP_AGE -lt 24 ]; then
  echo "✓ Backup freshness: PASS (${BACKUP_AGE}h old)"
else
  echo "✗ Backup freshness: FAIL (${BACKUP_AGE}h old)"
fi

# Check retention
BACKUP_COUNT=$(aws s3 ls s3://backups/ | wc -l)
if [ $BACKUP_COUNT -ge 30 ]; then
  echo "✓ Retention compliance: PASS ($BACKUP_COUNT backups)"
else
  echo "✗ Retention compliance: FAIL ($BACKUP_COUNT backups)"
fi

# Check encryption
ENCRYPTED=$(aws s3api get-bucket-encryption --bucket backups 2>/dev/null)
if [ $? -eq 0 ]; then
  echo "✓ Encryption: PASS"
else
  echo "✗ Encryption: FAIL"
fi
```
