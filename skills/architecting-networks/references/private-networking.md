# Private Networking

Private connectivity to cloud services without traversing the public internet.

## VPC Endpoints (AWS)

### Gateway Endpoints (Free)

**Supported Services:**
- S3
- DynamoDB

**Use When:**
- Accessing S3 or DynamoDB from private subnets
- Avoiding NAT Gateway data processing charges

### Interface Endpoints (AWS PrivateLink)

**Cost:** $0.01/hour/endpoint + $0.01/GB

**Supported Services:**
- Most AWS services (EC2, ECS, SNS, SQS, etc.)
- Third-party SaaS applications

**Use When:**
- Accessing AWS services from private subnets
- Security requirement: No public internet access
- Cost optimization: High-volume S3/DynamoDB access

## Private Service Connect (GCP)

**Purpose:** Private access to Google APIs and services

**Use When:**
- Accessing Google services without external IP
- Compliance requires private connectivity

## Private Link (Azure)

**Purpose:** Private access to Azure services over private IP

**Supported Services:**
- Azure Storage
- Azure SQL
- Azure Cosmos DB
- Custom private endpoints

## Implementation Pattern

**Before (via NAT Gateway):**
```
Private Instance → NAT Gateway → Internet → S3
Cost: NAT Gateway charges ($0.045/GB)
```

**After (via VPC Endpoint):**
```
Private Instance → VPC Endpoint → S3
Cost: Gateway endpoint (free), Interface endpoint ($0.01/GB)
```

## Cost Savings Example

**Scenario:** 100 TB/month S3 access from private subnets

**Via NAT Gateway:**
- NAT processing: 100 TB × $0.045/GB = $4,608

**Via Gateway Endpoint:**
- Endpoint: $0
- **Savings: $4,608/month**
