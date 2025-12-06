# AWS Multi-Account Security Architecture

## Overview

Multi-account AWS architecture provides security isolation, billing separation, and blast radius containment. Organize accounts using AWS Organizations with security controls enforced through Service Control Policies (SCPs).

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        AWS ORGANIZATION ROOT                             │
│                      (Management Account)                                │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Organization Policies:                                           │   │
│  │ - Require MFA for all users                                      │   │
│  │ - Enforce encryption at rest                                     │   │
│  │ - Deny root user access                                          │   │
│  │ - Restrict regions (compliance)                                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
           │
           ├───────────────────┬──────────────────┬──────────────────┐
           │                   │                  │                  │
           ▼                   ▼                  ▼                  ▼
    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │ Security OU │    │  Workload OU│    │Infrastructure│    │ Suspended OU│
    │             │    │             │    │     OU      │    │             │
    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
           │                   │                  │                  │
           │                   │                  │                  │
    ┌──────┴──────┐     ┌──────┴──────┐    ┌─────┴─────┐           │
    ▼             ▼     ▼             ▼    ▼           ▼           ▼
┌────────┐  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│Security│  │Logging │ │  Prod  │ │  Dev   │ │Shared  │ │Network │ │Quarantine│
│Tooling │  │Account │ │Account │ │Account │ │Services│ │Account │ │Account │
│        │  │        │ │        │ │        │ │        │ │        │ │        │
│GuardDuty│ │CloudTr.│ │        │ │        │ │CI/CD   │ │Transit │ │        │
│SecHub  │  │Config  │ │        │ │        │ │Artifact│ │Gateway │ │        │
│Macie   │  │S3      │ │        │ │        │ │        │ │VPC     │ │        │
└────────┘  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘
     │           │          │          │          │          │
     │           │          │          │          │          │
     └───────────┴──────────┴──────────┴──────────┴──────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │ Centralized      │
                  │ Security Logging │
                  │                  │
                  │ - CloudTrail     │
                  │ - VPC Flow Logs  │
                  │ - GuardDuty      │
                  │ - Security Hub   │
                  │ - Config         │
                  └──────────────────┘
```

## Organizational Unit (OU) Design

### Security OU

Contains accounts dedicated to security tooling and centralized logging.

**Security Tooling Account:**
- AWS Security Hub (aggregator)
- Amazon GuardDuty (threat detection)
- Amazon Macie (data discovery)
- AWS IAM Access Analyzer
- AWS Firewall Manager
- Amazon Detective (investigation)

**Logging Account:**
- Centralized CloudTrail logs (organization trail)
- AWS Config aggregator
- VPC Flow Logs aggregation
- S3 bucket policies preventing deletion
- Lifecycle policies for cost optimization
- Cross-region replication for DR

**SCPs Applied:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenySecurityLogDeletion",
      "Effect": "Deny",
      "Action": [
        "s3:DeleteBucket",
        "s3:DeleteObject",
        "s3:DeleteObjectVersion",
        "logs:DeleteLogGroup",
        "logs:DeleteLogStream"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:RequestedRegion": [
            "us-east-1",
            "us-west-2"
          ]
        }
      }
    }
  ]
}
```

### Workload OU

Contains production and non-production application accounts.

**Production Account:**
- Production workloads only
- Strict change control
- Enhanced monitoring
- Automated backups
- Encryption enforced

**Development/Staging Accounts:**
- Lower environment workloads
- Testing and experimentation
- Cost controls via budgets
- Automatic resource cleanup

**SCPs Applied:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "RequireEncryption",
      "Effect": "Deny",
      "Action": [
        "s3:PutObject",
        "ec2:RunInstances",
        "rds:CreateDBInstance"
      ],
      "Resource": "*",
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    },
    {
      "Sid": "DenyProdChangesOutsideWindow",
      "Effect": "Deny",
      "Action": [
        "ec2:*",
        "rds:*",
        "lambda:*"
      ],
      "Resource": "*",
      "Condition": {
        "DateGreaterThan": {"aws:CurrentTime": "2024-01-01T17:00:00Z"},
        "DateLessThan": {"aws:CurrentTime": "2024-01-01T09:00:00Z"},
        "StringEquals": {"aws:RequestedRegion": "us-east-1"}
      }
    }
  ]
}
```

### Infrastructure OU

Contains shared infrastructure and networking accounts.

**Shared Services Account:**
- Centralized CI/CD pipelines
- Artifact repositories (ECR, CodeArtifact)
- Shared AMI builder
- Secrets management
- Certificate management (ACM)

**Network Account:**
- AWS Transit Gateway
- VPC peering connections
- AWS Direct Connect
- Route53 private hosted zones
- Network Firewall
- AWS Network Firewall policies

**SCPs Applied:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyNetworkChanges",
      "Effect": "Deny",
      "Action": [
        "ec2:DeleteTransitGateway*",
        "ec2:DeleteVpc",
        "ec2:DeleteInternetGateway"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:PrincipalArn": "arn:aws:iam::*:role/NetworkAdminRole"
        }
      }
    }
  ]
}
```

### Suspended OU

Contains accounts for quarantine and decommissioning.

**Quarantine Account:**
- Compromised resource isolation
- Forensics analysis
- Incident response workspace
- No internet access
- All services disabled except forensics tools

**SCP Applied:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyAllExceptForensics",
      "Effect": "Deny",
      "NotAction": [
        "ec2:Describe*",
        "s3:GetObject",
        "s3:ListBucket",
        "cloudtrail:LookupEvents",
        "logs:FilterLogEvents"
      ],
      "Resource": "*"
    }
  ]
}
```

## Service Control Policies (SCPs)

### Global Security Baseline

Apply to all accounts in the organization:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyRootUser",
      "Effect": "Deny",
      "Action": "*",
      "Resource": "*",
      "Condition": {
        "StringLike": {
          "aws:PrincipalArn": "arn:aws:iam::*:root"
        }
      }
    },
    {
      "Sid": "RequireIMDSv2",
      "Effect": "Deny",
      "Action": "ec2:RunInstances",
      "Resource": "arn:aws:ec2:*:*:instance/*",
      "Condition": {
        "StringNotEquals": {
          "ec2:MetadataHttpTokens": "required"
        }
      }
    },
    {
      "Sid": "DenyRegionRestriction",
      "Effect": "Deny",
      "NotAction": [
        "iam:*",
        "organizations:*",
        "route53:*",
        "cloudfront:*",
        "support:*"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:RequestedRegion": [
            "us-east-1",
            "us-west-2",
            "eu-west-1"
          ]
        }
      }
    },
    {
      "Sid": "RequireEncryptionAtRest",
      "Effect": "Deny",
      "Action": [
        "s3:PutObject",
        "ec2:CreateVolume",
        "rds:CreateDBInstance"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "s3:x-amz-server-side-encryption": "AES256",
          "ec2:Encrypted": "true",
          "rds:StorageEncrypted": "true"
        }
      }
    },
    {
      "Sid": "DenySecurityServiceDisable",
      "Effect": "Deny",
      "Action": [
        "guardduty:DeleteDetector",
        "securityhub:DisableSecurityHub",
        "config:DeleteConfigurationRecorder",
        "cloudtrail:StopLogging",
        "macie2:DisableMacie"
      ],
      "Resource": "*"
    }
  ]
}
```

### Cost Control SCP (Development Accounts)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyExpensiveInstances",
      "Effect": "Deny",
      "Action": "ec2:RunInstances",
      "Resource": "arn:aws:ec2:*:*:instance/*",
      "Condition": {
        "ForAnyValue:StringNotLike": {
          "ec2:InstanceType": [
            "t3.*",
            "t3a.*",
            "t4g.*"
          ]
        }
      }
    }
  ]
}
```

## Cross-Account Access Patterns

### Centralized IAM Identity Center (AWS SSO)

**Permission Sets:**

```yaml
# ReadOnlyAccess
PermissionSet:
  Name: ReadOnlyAccess
  ManagedPolicies:
    - arn:aws:iam::aws:policy/ReadOnlyAccess
  SessionDuration: PT4H

# DeveloperAccess
PermissionSet:
  Name: DeveloperAccess
  ManagedPolicies:
    - arn:aws:iam::aws:policy/PowerUserAccess
  InlinePolicy:
    Statement:
      - Effect: Deny
        Action:
          - iam:*
          - organizations:*
        Resource: "*"
  SessionDuration: PT8H

# AdminAccess
PermissionSet:
  Name: AdminAccess
  ManagedPolicies:
    - arn:aws:iam::aws:policy/AdministratorAccess
  SessionDuration: PT1H
  RequireMFA: true
```

### Cross-Account IAM Roles

**Assumption Pattern:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::111111111111:role/TrustedRole"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "unique-external-id-12345"
        },
        "IpAddress": {
          "aws:SourceIp": [
            "10.0.0.0/8",
            "172.16.0.0/12"
          ]
        },
        "Bool": {
          "aws:MultiFactorAuthPresent": "true"
        }
      }
    }
  ]
}
```

**Service-to-Service Pattern:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "aws:SourceAccount": "222222222222"
        },
        "ArnLike": {
          "aws:SourceArn": "arn:aws:lambda:us-east-1:222222222222:function/allowed-function"
        }
      }
    }
  ]
}
```

## Centralized Logging Architecture

### CloudTrail Organization Trail

**Configuration:**

```json
{
  "Name": "OrganizationTrail",
  "IsOrganizationTrail": true,
  "IsMultiRegionTrail": true,
  "IncludeGlobalServiceEvents": true,
  "EnableLogFileValidation": true,
  "EventSelectors": [
    {
      "ReadWriteType": "All",
      "IncludeManagementEvents": true,
      "DataResources": [
        {
          "Type": "AWS::S3::Object",
          "Values": ["arn:aws:s3:::*/sensitive-data/*"]
        },
        {
          "Type": "AWS::Lambda::Function",
          "Values": ["arn:aws:lambda:*:*:function/*"]
        }
      ]
    }
  ],
  "InsightSelectors": [
    {
      "InsightType": "ApiCallRateInsight"
    },
    {
      "InsightType": "ApiErrorRateInsight"
    }
  ]
}
```

**S3 Bucket Policy (Logging Account):**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AWSCloudTrailAclCheck",
      "Effect": "Allow",
      "Principal": {
        "Service": "cloudtrail.amazonaws.com"
      },
      "Action": "s3:GetBucketAcl",
      "Resource": "arn:aws:s3:::org-cloudtrail-logs"
    },
    {
      "Sid": "AWSCloudTrailWrite",
      "Effect": "Allow",
      "Principal": {
        "Service": "cloudtrail.amazonaws.com"
      },
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::org-cloudtrail-logs/*",
      "Condition": {
        "StringEquals": {
          "s3:x-amz-acl": "bucket-owner-full-control"
        }
      }
    },
    {
      "Sid": "DenyUnencryptedObjectUploads",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::org-cloudtrail-logs/*",
      "Condition": {
        "StringNotEquals": {
          "s3:x-amz-server-side-encryption": "AES256"
        }
      }
    },
    {
      "Sid": "DenyInsecureTransport",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::org-cloudtrail-logs",
        "arn:aws:s3:::org-cloudtrail-logs/*"
      ],
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    }
  ]
}
```

### VPC Flow Logs

**Centralized Collection:**

```bash
# Enable VPC Flow Logs for all VPCs across accounts
aws ec2 create-flow-logs \
  --resource-type VPC \
  --resource-ids vpc-xxxxx \
  --traffic-type ALL \
  --log-destination-type s3 \
  --log-destination arn:aws:s3:::org-vpc-flow-logs \
  --log-format '${srcaddr} ${dstaddr} ${srcport} ${dstport} ${protocol} ${packets} ${bytes} ${start} ${end} ${action} ${log-status} ${vpc-id} ${subnet-id} ${instance-id} ${tcp-flags} ${type} ${pkt-srcaddr} ${pkt-dstaddr} ${region} ${az-id} ${sublocation-type} ${sublocation-id}'
```

**Athena Query Setup:**

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS vpc_flow_logs (
  srcaddr string,
  dstaddr string,
  srcport int,
  dstport int,
  protocol int,
  packets bigint,
  bytes bigint,
  start_time bigint,
  end_time bigint,
  action string,
  log_status string,
  vpc_id string,
  subnet_id string,
  instance_id string,
  tcp_flags int,
  type string,
  pkt_srcaddr string,
  pkt_dstaddr string,
  region string,
  az_id string,
  sublocation_type string,
  sublocation_id string
)
PARTITIONED BY (year string, month string, day string)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ' '
LOCATION 's3://org-vpc-flow-logs/AWSLogs/'
TBLPROPERTIES ("skip.header.line.count"="1");
```

### AWS Security Hub

**Aggregator Configuration:**

```python
import boto3

securityhub = boto3.client('securityhub', region_name='us-east-1')

# Enable Security Hub in aggregator account
securityhub.enable_security_hub(
    EnableDefaultStandards=True
)

# Enable standards
securityhub.batch_enable_standards(
    StandardsSubscriptionRequests=[
        {'StandardsArn': 'arn:aws:securityhub:us-east-1::standards/aws-foundational-security-best-practices/v/1.0.0'},
        {'StandardsArn': 'arn:aws:securityhub:us-east-1::standards/cis-aws-foundations-benchmark/v/1.4.0'},
        {'StandardsArn': 'arn:aws:securityhub:us-east-1::standards/pci-dss/v/3.2.1'}
    ]
)

# Create aggregator
securityhub.create_finding_aggregator(
    RegionLinkingMode='ALL_REGIONS'
)
```

### Amazon GuardDuty

**Organization Configuration:**

```python
import boto3

guardduty = boto3.client('guardduty', region_name='us-east-1')

# Create detector in delegated admin account
detector_response = guardduty.create_detector(
    Enable=True,
    FindingPublishingFrequency='FIFTEEN_MINUTES',
    DataSources={
        'S3Logs': {'Enable': True},
        'Kubernetes': {
            'AuditLogs': {'Enable': True}
        },
        'MalwareProtection': {
            'ScanEc2InstanceWithFindings': {
                'EbsVolumes': {'Enable': True}
            }
        }
    }
)

detector_id = detector_response['DetectorId']

# Enable for organization
guardduty.enable_organization_admin_account(
    AdminAccountId='333333333333'  # Security Tooling account
)

# Auto-enable for new accounts
guardduty.update_organization_configuration(
    DetectorId=detector_id,
    AutoEnable=True,
    DataSources={
        'S3Logs': {'AutoEnable': True},
        'Kubernetes': {
            'AuditLogs': {'AutoEnable': True}
        },
        'MalwareProtection': {
            'ScanEc2InstanceWithFindings': {
                'EbsVolumes': {'AutoEnable': True}
            }
        }
    }
)
```

## Network Security Architecture

### Transit Gateway Design

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Prod VPC    │     │  Dev VPC     │     │ Shared VPC   │
│ 10.0.0.0/16  │     │ 10.1.0.0/16  │     │ 10.2.0.0/16  │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
       │    ┌───────────────┴────────────────┐   │
       └────┤   AWS Transit Gateway          ├───┘
            │   Route Tables:                │
            │   - Prod (isolated)            │
            │   - Non-Prod (shared)          │
            │   - Egress (internet-bound)    │
            └───────────────┬────────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │ Network Firewall │
                  │ - IDS/IPS         │
                  │ - DPI             │
                  │ - Domain filtering│
                  └──────────────────┘
```

### Security Groups Strategy

**Tiered Application Pattern:**

```json
{
  "SecurityGroups": {
    "ALB": {
      "Ingress": [
        {"Protocol": "tcp", "Port": 443, "Source": "0.0.0.0/0"}
      ],
      "Egress": [
        {"Protocol": "tcp", "Port": 8080, "Destination": "sg-app-tier"}
      ]
    },
    "AppTier": {
      "Ingress": [
        {"Protocol": "tcp", "Port": 8080, "Source": "sg-alb"}
      ],
      "Egress": [
        {"Protocol": "tcp", "Port": 5432, "Destination": "sg-db-tier"}
      ]
    },
    "DBTier": {
      "Ingress": [
        {"Protocol": "tcp", "Port": 5432, "Source": "sg-app-tier"}
      ],
      "Egress": []
    }
  }
}
```

## Compliance and Governance

### AWS Config Rules

**Organization Conformance Packs:**

```yaml
ConformancePackName: OrganizationSecurityBaseline
ConformancePackInputParameters:
  - ParameterName: RequiredTags
    ParameterValue: "Environment,Owner,CostCenter"

Resources:
  - ConfigRule:
      ConfigRuleName: encrypted-volumes
      Source:
        Owner: AWS
        SourceIdentifier: ENCRYPTED_VOLUMES
      Scope:
        ComplianceResourceTypes:
          - AWS::EC2::Volume

  - ConfigRule:
      ConfigRuleName: s3-bucket-public-read-prohibited
      Source:
        Owner: AWS
        SourceIdentifier: S3_BUCKET_PUBLIC_READ_PROHIBITED

  - ConfigRule:
      ConfigRuleName: iam-password-policy
      Source:
        Owner: AWS
        SourceIdentifier: IAM_PASSWORD_POLICY
      InputParameters:
        RequireUppercaseCharacters: true
        RequireLowercaseCharacters: true
        RequireSymbols: true
        RequireNumbers: true
        MinimumPasswordLength: 14
        PasswordReusePrevention: 24
        MaxPasswordAge: 90
```

### Backup Strategy

**AWS Backup Organization Policy:**

```json
{
  "plans": {
    "ProductionBackupPlan": {
      "regions": ["us-east-1", "us-west-2"],
      "rules": {
        "DailyBackup": {
          "schedule_expression": "cron(0 5 ? * * *)",
          "start_window_minutes": 60,
          "target_backup_vault_name": "ProductionVault",
          "lifecycle": {
            "move_to_cold_storage_after_days": 30,
            "delete_after_days": 365
          },
          "copy_actions": [
            {
              "destination_backup_vault_arn": "arn:aws:backup:us-west-2:444444444444:backup-vault:ProductionVaultDR",
              "lifecycle": {
                "delete_after_days": 365
              }
            }
          ]
        }
      },
      "selections": {
        "ProductionResources": {
          "iam_role_arn": "arn:aws:iam::444444444444:role/AWSBackupRole",
          "resources": [
            "arn:aws:ec2:*:*:volume/*",
            "arn:aws:rds:*:*:db:*",
            "arn:aws:dynamodb:*:*:table/*"
          ],
          "conditions": {
            "tags": {
              "Environment": "Production"
            }
          }
        }
      }
    }
  }
}
```

## Incident Response Preparation

### Automated Quarantine

**Lambda Function (EventBridge Rule Trigger):**

```python
import boto3
import json

ec2 = boto3.client('ec2')
sns = boto3.client('sns')

def lambda_handler(event, context):
    """
    Quarantine compromised EC2 instance based on GuardDuty finding.
    """
    # Extract instance ID from GuardDuty finding
    finding = event['detail']
    instance_id = finding['resource']['instanceDetails']['instanceId']

    # Create forensics snapshot
    volumes = ec2.describe_instance_attribute(
        InstanceId=instance_id,
        Attribute='blockDeviceMapping'
    )

    for volume in volumes['BlockDeviceMappings']:
        volume_id = volume['Ebs']['VolumeId']
        ec2.create_snapshot(
            VolumeId=volume_id,
            Description=f'Forensics snapshot - GuardDuty finding',
            TagSpecifications=[
                {
                    'ResourceType': 'snapshot',
                    'Tags': [
                        {'Key': 'Forensics', 'Value': 'true'},
                        {'Key': 'SourceInstance', 'Value': instance_id}
                    ]
                }
            ]
        )

    # Apply quarantine security group
    ec2.modify_instance_attribute(
        InstanceId=instance_id,
        Groups=['sg-quarantine']
    )

    # Notify security team
    sns.publish(
        TopicArn='arn:aws:sns:us-east-1:333333333333:SecurityAlerts',
        Subject=f'Instance Quarantined: {instance_id}',
        Message=json.dumps(finding, indent=2)
    )

    return {
        'statusCode': 200,
        'body': json.dumps(f'Instance {instance_id} quarantined successfully')
    }
```

## Key Security Metrics

Monitor these metrics across the organization:

1. **Access Metrics:**
   - Failed login attempts per account
   - Root user usage (should be zero)
   - MFA coverage percentage
   - Unused IAM credentials (>90 days)

2. **Compliance Metrics:**
   - Config rule compliance rate
   - Security Hub security score
   - Unencrypted resources count
   - Public-facing resources

3. **Threat Detection:**
   - GuardDuty findings by severity
   - Mean time to remediation (MTTR)
   - Repeat findings count
   - Security Hub critical findings

4. **Network Security:**
   - Unprotected security groups
   - VPC Flow Logs enabled percentage
   - Network Firewall blocks per hour
   - Unusual traffic patterns

## Implementation Checklist

- [ ] Create AWS Organization structure
- [ ] Define OU hierarchy and account placement
- [ ] Configure Service Control Policies (SCPs)
- [ ] Enable AWS IAM Identity Center (SSO)
- [ ] Create permission sets for least privilege
- [ ] Deploy organization CloudTrail
- [ ] Enable GuardDuty organization-wide
- [ ] Configure Security Hub aggregator
- [ ] Deploy AWS Config conformance packs
- [ ] Implement centralized logging (S3 buckets)
- [ ] Configure VPC Flow Logs for all VPCs
- [ ] Deploy Transit Gateway (if applicable)
- [ ] Configure AWS Backup organization policy
- [ ] Create incident response runbooks
- [ ] Deploy automated quarantine mechanisms
- [ ] Establish security metrics dashboard
- [ ] Configure alerting and notifications
- [ ] Document cross-account access patterns
- [ ] Train teams on multi-account operations
- [ ] Conduct tabletop incident response exercise

## References

- [AWS Organizations Best Practices](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_best-practices.html)
- [AWS Security Reference Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html)
- [CIS AWS Foundations Benchmark](https://www.cisecurity.org/benchmark/amazon_web_services)
- [AWS Multi-Account Strategy](https://aws.amazon.com/organizations/getting-started/best-practices/)
