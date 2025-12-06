# Data Mesh Guide

Decentralized data architecture for large organizations. Addresses centralized bottlenecks through domain ownership.


## Table of Contents

- [Four Core Principles](#four-core-principles)
  - [1. Domain-Oriented Decentralization](#1-domain-oriented-decentralization)
  - [2. Data as a Product](#2-data-as-a-product)
  - [3. Self-Serve Data Infrastructure](#3-self-serve-data-infrastructure)
  - [4. Federated Computational Governance](#4-federated-computational-governance)
- [When to Use Data Mesh](#when-to-use-data-mesh)
- [Lakehouse Implementation](#lakehouse-implementation)
- [Readiness Assessment](#readiness-assessment)

## Four Core Principles

### 1. Domain-Oriented Decentralization

Each business domain owns its data:
- Sales domain owns sales data
- Marketing domain owns marketing data
- Product domain owns product usage data

**Traditional vs Mesh:**
```
Traditional: All Domains → Central Data Team → Warehouse
Data Mesh:   Sales Domain → Sales Data Product → Consumers
             Marketing Domain → Marketing Data Product → Consumers
```

### 2. Data as a Product

Treat data like products with quality commitments:
- **SLAs:** Freshness, availability, quality guarantees
- **Documentation:** Schema, use cases, examples
- **Support:** Help channels, onboarding
- **Consumers as customers:** Internal users treated like external customers

**Data Product Contract Example:**
```yaml
data_product:
  name: sales-orders-product
  domain: sales
  owner: sales-data-team@company.com
  sla:
    freshness: 15 minutes
    availability: 99.9%
    quality_score: >95%
  schema:
    format: Avro
    version: 2.1.0
  access:
    read: SELECT on sales.orders
    authentication: OAuth2
```

### 3. Self-Serve Data Infrastructure

Platform team provides tooling for domain autonomy:
- Infrastructure as code (Terraform, Pulumi)
- CI/CD pipelines for data products
- Observability (monitoring, alerting, lineage)
- Data catalog (discovery)
- Governance tooling

**Domain teams can do (without platform team):**
- Deploy new data pipeline
- Update schema
- Monitor data quality
- Set up alerts
- Publish data product to catalog

### 4. Federated Computational Governance

Global policies with local implementation:
- **Global Policy:** "All PII must be encrypted at rest"
- **Domain Implementation:** Sales team encrypts customer email
- **Automated Check:** Platform scans for unencrypted PII
- **Audit:** Central governance reviews quarterly

## When to Use Data Mesh

**Strong Candidates:**
- Large organizations (>500 people)
- Clear business domains with distinct ownership
- Central data team is bottleneck
- Domain teams have data engineering skills

**Not Ready:**
- Small organizations (<100 people)
- Unclear domain boundaries
- No platform engineering team
- Domain teams lack data skills

## Lakehouse Implementation

Each domain owns bronze-silver-gold for their data products:

```
Sales Domain:
  bronze.sales_raw → silver.sales_cleaned → gold.sales_analytics (data product)

Marketing Domain:
  bronze.marketing_raw → silver.marketing_cleaned → gold.marketing_analytics

Cross-Domain:
  gold.customer_360 (combines sales + marketing silver tables)
```

## Readiness Assessment

Score 1-5 for each factor:
1. Domain clarity
2. Team maturity
3. Platform capability
4. Governance maturity
5. Scale need
6. Organizational buy-in

**24-30:** Strong mesh candidate
**18-23:** Hybrid approach
**12-17:** Build foundation first
**6-11:** Centralized approach

See [decision-frameworks.md](decision-frameworks.md#data-mesh-readiness) for full assessment.
