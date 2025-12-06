# SIEM Platform Comparison

## Table of Contents

- [Overview](#overview)
- [Elastic SIEM](#elastic-siem)
- [Microsoft Sentinel](#microsoft-sentinel)
- [Wazuh](#wazuh)
- [Splunk Enterprise Security](#splunk-enterprise-security)
- [AWS Security Lake](#aws-security-lake)
- [Feature Comparison Matrix](#feature-comparison-matrix)
- [Selection Decision Tree](#selection-decision-tree)
- [Cost Comparison](#cost-comparison)

## Overview

This guide provides comprehensive comparison of leading SIEM platforms in 2025, covering features, pricing, deployment models, and use cases to help select the right platform for your organization.

## Elastic SIEM

### Overview

- **Vendor:** Elastic
- **Deployment:** Cloud (Elastic Cloud) or Self-Hosted
- **Foundation:** Open-source Elasticsearch
- **License:** Elastic License (commercial) or Apache 2.0 (open-source core)

### Strengths

**Open-Source Foundation:**
- Built on Elasticsearch (open-source core)
- Start with ELK stack (free), add commercial features later
- Full control and customization
- Extensive plugin ecosystem

**Unified XDR Platform:**
- Extends beyond SIEM to endpoint detection (EDR)
- Cloud security posture management (CSPM)
- Unified detection across SIEM, endpoint, and cloud

**AI-Powered Detection:**
- Elastic AI SOC Engine (EASE) for automated alert correlation
- Machine learning for anomaly detection
- Behavioral analytics

**Detection-as-Code:**
- Extensive community-contributed detection rules
- SIGMA rule support
- Event Query Language (EQL) for sequence-based detection
- MITRE ATT&CK mapping built-in

**Multi-Cloud Support:**
- Works across AWS, Azure, GCP, on-premise
- No vendor lock-in
- Flexible deployment options

### Weaknesses

- Steeper learning curve than Sentinel
- Requires Elasticsearch expertise for advanced configurations
- Self-hosted option requires infrastructure management
- Less mature SOAR capabilities compared to Sentinel

### When to Use

- DevOps/engineering teams comfortable with Elasticsearch
- Multi-cloud or hybrid environments
- Need for customization and extensibility
- Want option to start open-source, add commercial features later
- Medium to large data volumes (100 GB - 10 TB/day)

### Pricing

**Elastic Cloud (Managed):**
- Standard: ~$95/month (16 GB RAM, 128 GB storage)
- Hot tier: ~$0.11/GB/month
- Warm tier: ~$0.03/GB/month
- Cold tier: ~$0.01/GB/month

**Self-Hosted (Open-Source):**
- Free for ELK stack (Elasticsearch, Logstash, Kibana)
- Commercial features (SIEM, ML, alerting): License required
- Infrastructure costs only

### Example Deployment

```bash
# Elastic Cloud (Managed)
# Sign up at cloud.elastic.co
# Create deployment (Security tier)

# Self-Hosted (Docker Compose)
version: '3.8'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=true
    ports:
      - "9200:9200"
    volumes:
      - esdata:/usr/share/elasticsearch/data

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5601:5601"

volumes:
  esdata:
```

---

## Microsoft Sentinel

### Overview

- **Vendor:** Microsoft
- **Deployment:** Cloud-only (Azure)
- **Foundation:** Azure Monitor, Log Analytics
- **License:** Pay-as-you-go (per GB ingested)

### Strengths

**Cloud-Native:**
- Built on Azure, infinite scale
- No infrastructure management
- Auto-scaling to any volume

**Azure Ecosystem Integration:**
- Seamless integration with Microsoft 365, Azure AD, Defender, Intune
- Native Azure resource monitoring
- Azure Security Center integration

**Built-in SOAR:**
- Azure Logic Apps for automation (included)
- No separate SOAR product needed
- Pre-built playbooks for common responses

**AI-Driven Threat Intelligence:**
- Microsoft Threat Intelligence integration
- Behavioral analytics
- ML-based anomaly detection
- Sentinel Graph for attack path visualization

**Ease of Use:**
- User-friendly interface
- Pre-built dashboards and workbooks
- Guided onboarding

**Cost-Effective for SMBs:**
- 50 GB commitment tier introduced (2024)
- Pay-as-you-go pricing
- No upfront costs

### Weaknesses

- Azure-locked (limited multi-cloud support)
- Less customization than Elastic/Splunk
- Requires Azure expertise
- Data egress costs for multi-cloud scenarios

### When to Use

- Heavy Azure/Microsoft 365 investment
- Want cloud-native, managed SIEM (no infrastructure)
- Need built-in SOAR capabilities
- Small to large organizations (scalable pricing)
- Existing Microsoft ecosystem (AD, Office 365, Defender)

### Pricing

**Pay-As-You-Go:**
- $2.80/GB for first 5 TB/day
- Volume discounts at higher tiers
- 50 GB commitment tier: ~$140/month minimum

**Commitment Tiers:**
- 50 GB/day: ~$140/day (~$4,200/month)
- 100 GB/day: ~$260/day (~$7,800/month)
- 200 GB/day: ~$500/day (~$15,000/month)

### Example Deployment

```bash
# Azure CLI
az monitor log-analytics workspace create \
  --resource-group security-rg \
  --workspace-name security-sentinel \
  --location eastus

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

---

## Wazuh

### Overview

- **Vendor:** Wazuh (Open-Source)
- **Deployment:** Self-Hosted (on-premise or cloud VMs)
- **Foundation:** OpenSearch (fork of Elasticsearch)
- **License:** GPL v2 (free and open-source)

### Strengths

**Free and Open-Source:**
- Zero licensing costs
- Active community (10,000+ GitHub stars)
- Regular updates and security patches

**XDR Capabilities:**
- Unified threat prevention, detection, and response
- Endpoint security (file integrity monitoring, rootkit detection)
- Vulnerability detection
- Security configuration assessment

**Multi-Platform Support:**
- Linux, Windows, macOS, Docker, Kubernetes, cloud VMs
- Unified agent across platforms
- Centralized management

**Built-in Compliance Features:**
- PCI DSS compliance modules
- HIPAA, GDPR, SOC 2 compliance templates
- CIS benchmarks
- Automated compliance reporting

**Easy to Deploy:**
- Docker Compose for quick start
- Kubernetes Helm charts
- Ansible playbooks for automation

**Active Development:**
- Regular releases (quarterly)
- Responsive to security landscape
- Community-contributed rules

### Weaknesses

- Fewer enterprise features than commercial SIEMs
- Requires self-hosting and maintenance
- Smaller ecosystem than Elastic/Splunk
- Less mature AI/ML capabilities
- Limited advanced correlation features

### When to Use

- Tight budget (startups, SMBs, non-profits)
- Want full control and customization
- Need compliance features (PCI DSS, HIPAA, GDPR, SOC 2)
- Comfortable managing infrastructure
- Small to medium data volumes (<500 GB/day)

### Pricing

**Software Cost:** Free (GPL v2 license)

**Infrastructure Costs:**
- Cloud VMs: ~$200-$1,000/month (depending on scale)
- On-premise: Hardware costs only
- Storage: S3/Azure Blob/GCS for log archive

### Example Deployment

```bash
# Docker Compose
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

## Splunk Enterprise Security

### Overview

- **Vendor:** Splunk
- **Deployment:** On-Premise or Splunk Cloud
- **Foundation:** Proprietary Splunk platform
- **License:** Commercial (per GB ingested/day)

### Strengths

**Market Leader:**
- Used by Fortune 100 companies
- Proven at enterprise scale
- Decades of development

**Massive Scalability:**
- Proven at petabyte scale
- Handles TB/day ingestion rates
- Distributed search and indexing

**Customization:**
- Extensive customization options
- SPL (Search Processing Language) - powerful query language
- Splunkbase (1,000+ apps and integrations)

**Ecosystem:**
- Thousands of pre-built integrations
- Vendor partnerships
- Extensive training and certification programs

**Enterprise Support:**
- 24/7 support
- Professional services
- Dedicated account teams
- SLAs and uptime guarantees

**Advanced Analytics:**
- Machine learning toolkit
- ITSI (IT Service Intelligence) integration
- User behavior analytics (UBA)

### Weaknesses

- **Very expensive:** Licensing costs can be prohibitive ($150k-$1M+/year)
- Complex to deploy and manage
- Requires dedicated Splunk team
- Separate SOAR product (Splunk SOAR) adds significant cost
- Steep learning curve

### When to Use

- Large enterprises with unlimited budget
- Need for massive scale (TB/day+)
- Require enterprise support and SLAs
- Existing Splunk investment
- Complex use cases requiring deep customization

### Pricing

**On-Premise:**
- ~$1,800/GB/day ingestion license
- Example: 100 GB/day = ~$180,000/year

**Splunk Cloud:**
- ~$2,300/GB/day (includes infrastructure)
- Example: 100 GB/day = ~$230,000/year

**Enterprise Security Add-On:**
- Additional ~20-30% on top of core license

---

## AWS Security Lake

### Overview

- **Vendor:** Amazon Web Services
- **Deployment:** Cloud-only (AWS)
- **Foundation:** S3, OpenSearch, Athena
- **License:** Pay-as-you-go (AWS services)

### Strengths

**AWS-Native:**
- Seamless integration with AWS services
- CloudTrail, VPC Flow Logs, GuardDuty, Security Hub
- Native IAM integration

**Centralized Data Lake:**
- OCSF (Open Cybersecurity Schema Framework) format
- Single repository for security data from multiple sources
- S3-based storage (cheap, scalable)

**Flexible Analysis:**
- OpenSearch for SIEM-like analysis
- Athena for SQL queries
- SageMaker for ML analysis
- Third-party SIEM integration

**Cost-Effective:**
- Pay only for S3 storage and query compute
- No per-GB ingestion fees
- Data tiering (S3 Standard → Glacier)

### Weaknesses

- AWS-locked (limited multi-cloud support)
- Newer platform (less mature than competitors)
- Requires AWS expertise
- SIEM features less advanced than dedicated platforms
- Manual setup and configuration

### When to Use

- AWS-heavy organizations (90%+ AWS infrastructure)
- Want centralized security data lake
- Need flexible analysis options (OpenSearch, Athena, custom)
- Budget-conscious (avoid per-GB ingestion fees)

### Pricing

**Security Lake:**
- Free service (pay for underlying resources)

**Storage (S3):**
- S3 Standard: ~$0.023/GB/month
- S3 Glacier: ~$0.004/GB/month

**OpenSearch:**
- ~$0.15/hour per node (t3.medium.search)
- ~$3,600/month for 3-node cluster

**Athena Queries:**
- $5/TB scanned

---

## Feature Comparison Matrix

| Feature | Elastic SIEM | Microsoft Sentinel | Wazuh | Splunk ES | AWS Security Lake |
|---------|-------------|-------------------|-------|-----------|-------------------|
| **Cost (GB/day)** | $$$ | $$$ | Free | $$$$$ | $$ |
| **Deployment** | Cloud/Self-Hosted | Cloud | Self-Hosted | Cloud/On-Prem | Cloud |
| **Scalability** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Ease of Use** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Customization** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **AI/ML** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Built-in SOAR** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **Multi-Cloud** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Community** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Learning Curve** | Medium-High | Medium | Low-Medium | High | Medium-High |
| **Open-Source** | Partial | No | Yes | No | Partial |
| **Detection Rules** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Compliance** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## Selection Decision Tree

```
START: Which SIEM platform should I use?

Q1: What is your budget?
  ├─ Unlimited ($500k+/year) → Q2
  ├─ Moderate ($50k-$500k/year) → Q3
  └─ Tight (<$50k/year) → Wazuh (Free, Open-Source)

Q2: Do you have existing vendor ecosystem?
  ├─ Heavy Azure investment → Microsoft Sentinel
  ├─ Heavy AWS investment → AWS Security Lake + OpenSearch
  └─ Multi-cloud or on-premise → Splunk Enterprise Security

Q3: What is your data volume?
  ├─ >1 TB/day → Elastic Cloud or Splunk Cloud
  ├─ 100 GB - 1 TB/day → Microsoft Sentinel or Elastic SIEM
  └─ <100 GB/day → Wazuh or Sentinel (50 GB tier)

Q4: What is your team's expertise?
  ├─ Elasticsearch experts → Elastic SIEM
  ├─ Microsoft/Azure experts → Microsoft Sentinel
  ├─ Splunk experience → Splunk
  └─ Generalists → Wazuh (easiest learning curve)

Q5: What deployment model do you prefer?
  ├─ Cloud-native (no infrastructure) → Microsoft Sentinel or Elastic Cloud
  ├─ Self-hosted (full control) → Wazuh or Elastic (self-hosted)
  └─ Hybrid (flexible) → Elastic SIEM
```

---

## Cost Comparison

### Scenario: 200 GB/day ingestion, 1-year retention

| Platform | Monthly Cost | Annual Cost | Notes |
|----------|-------------|-------------|-------|
| **Elastic Cloud** | ~$6,600 | ~$79,200 | Hot: 30d, Warm: 90d, Cold: 245d |
| **Microsoft Sentinel** | ~$16,800 | ~$201,600 | 200 GB commitment tier |
| **Wazuh** | ~$500 | ~$6,000 | Infrastructure only (VMs, storage) |
| **Splunk ES** | ~$30,000 | ~$360,000 | On-premise license |
| **AWS Security Lake** | ~$5,000 | ~$60,000 | S3 + OpenSearch + Athena |

### Scenario: 1 TB/day ingestion, 1-year retention

| Platform | Monthly Cost | Annual Cost | Notes |
|----------|-------------|-------------|-------|
| **Elastic Cloud** | ~$33,000 | ~$396,000 | Hot: 30d, Warm: 90d, Cold: 245d |
| **Microsoft Sentinel** | ~$75,000 | ~$900,000 | 1 TB commitment tier |
| **Wazuh** | ~$2,500 | ~$30,000 | Infrastructure (larger VMs, storage) |
| **Splunk ES** | ~$150,000 | ~$1,800,000 | On-premise license |
| **AWS Security Lake** | ~$25,000 | ~$300,000 | S3 + OpenSearch (larger) + Athena |

### Cost Optimization Tips

**Elastic SIEM:**
- Use hot/warm/cold tiering aggressively
- Sample non-critical logs (reduce volume)
- Self-host for larger deployments (cost-effective >500 GB/day)

**Microsoft Sentinel:**
- Use 50 GB commitment tier for SMBs
- Enable data retention archiving (cheaper long-term storage)
- Filter noisy logs before ingestion

**Wazuh:**
- Use cloud VMs with reserved instances (60% savings)
- Archive to S3/Azure Blob/GCS (cheap long-term storage)
- Scale horizontally (add nodes as needed)

**Splunk:**
- Negotiate volume discounts (40%+ discounts possible)
- Use Splunk Cloud for smaller deployments (<500 GB/day)
- Implement data tiering (reduce hot storage)

**AWS Security Lake:**
- Use S3 Intelligent-Tiering (automatic cost optimization)
- Partition data by date (reduce Athena scan costs)
- Use OpenSearch reserved instances (30% savings)

---

## Summary

**Choose Elastic SIEM when:**
- Multi-cloud or hybrid environment
- DevOps/engineering team with Elasticsearch skills
- Need customization and extensibility
- Want open-source foundation with commercial options

**Choose Microsoft Sentinel when:**
- Heavy Azure/Microsoft 365 investment
- Want cloud-native, fully managed SIEM
- Need built-in SOAR capabilities
- Small to large organizations with scalable pricing

**Choose Wazuh when:**
- Tight budget (startups, SMBs, non-profits)
- Want full control and open-source solution
- Need compliance features (PCI DSS, HIPAA, GDPR)
- Comfortable managing infrastructure

**Choose Splunk when:**
- Large enterprise with unlimited budget
- Need proven scalability at massive scale
- Require enterprise support and SLAs
- Complex use cases requiring deep customization

**Choose AWS Security Lake when:**
- AWS-heavy organization (90%+ AWS infrastructure)
- Want centralized security data lake
- Need flexible analysis options
- Budget-conscious (avoid per-GB ingestion fees)
