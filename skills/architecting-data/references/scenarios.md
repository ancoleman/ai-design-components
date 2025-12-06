# Common Scenarios and Recommendations


## Table of Contents

- [Scenario 1: Startup Data Platform](#scenario-1-startup-data-platform)
- [Scenario 2: Enterprise Modernization](#scenario-2-enterprise-modernization)
- [Scenario 3: Data Mesh Assessment](#scenario-3-data-mesh-assessment)
- [Scenario 4: Lakehouse Table Format Selection](#scenario-4-lakehouse-table-format-selection)
- [Scenario 5: Streaming + Batch Architecture](#scenario-5-streaming-batch-architecture)
- [Scenario 6: Cost Optimization](#scenario-6-cost-optimization)
- [Decision Framework Summary](#decision-framework-summary)

## Scenario 1: Startup Data Platform

**Context:**
- 50-person startup
- Data sources: PostgreSQL, MongoDB, Stripe
- Need: Analytics for CEO dashboard + ML experiments
- Team: 1-2 analysts, no data engineers
- Budget: <$5K/month

**Recommendation:**

**Storage:** BigQuery or Snowflake (pay-per-use)
- BigQuery if GCP-committed
- Snowflake if multi-cloud flexibility desired

**Ingestion:** Airbyte (open-source) or Fivetran (if budget)
- Airbyte: Free, requires some ops
- Fivetran: $1K-2K/month, zero maintenance

**Transformation:** dbt Core (SQL-based)
- Free, open-source
- Version control with Git
- Testing framework included

**Orchestration:** dbt Cloud or Prefect Cloud
- dbt Cloud: Simple, dbt-specific
- Prefect Cloud: More flexible

**Visualization:** Metabase (open-source) or Looker Studio (free)

**Architecture:** Simple data warehouse
- Start with dimensional models (star schemas)
- Add lakehouse if ML becomes priority

**Why:** Minimize complexity, leverage managed services, focus on business value.

---

## Scenario 2: Enterprise Modernization

**Context:**
- Legacy Oracle data warehouse
- Want cloud migration
- Support BI + ML workloads
- Reduce costs
- Team: 10+ data engineers

**Recommendation:**

**Storage:** Data Lakehouse (Databricks or Snowflake with Iceberg)
- Databricks if ML-heavy
- Snowflake if BI-primary

**Migration Strategy:**
1. Identify critical BI reports (keep on Oracle short-term)
2. Build lakehouse for new analytics and ML
3. Use CDC tools (Debezium, Fivetran) for continuous replication
4. Gradually migrate Oracle tables to lakehouse
5. Sunset Oracle after full migration

**Architecture:** Medallion (bronze, silver, gold)
- Bronze: Raw replication from Oracle
- Silver: Cleaned, typed data
- Gold: Star schemas + ML features

**Cost Savings:** 60-80% with lake storage vs Oracle licensing

**Timeline:** 12-18 months for full migration

---

## Scenario 3: Data Mesh Assessment

**Context:**
- 200-person company
- Centralized data team: 5 people
- Domains: Sales, Marketing, Product
- Question: Should we adopt data mesh?

**Assessment:**

**6-Factor Scores (1-5):**
1. Domain clarity: 4 (clear domains)
2. Team maturity: 2 (analysts, but no data engineers in domains)
3. Platform capability: 2 (some automation, but not self-serve)
4. Governance maturity: 3 (centralized, but difficult to enforce)
5. Scale need: 2 (5-person team not yet bottleneck)
6. Organizational buy-in: 3 (interested, but skeptical)

**Total Score:** 16/30

**Recommendation:** NOT YET. Build foundation first.

**Why:**
- 200 people is too small for full data mesh (recommend >500)
- Central team of 5 is not yet a bottleneck
- Domain teams lack data engineering skills
- Self-serve platform doesn't exist yet

**Alternative Approach:**
1. Invest in self-serve platform (infrastructure as code, CI/CD)
2. Improve governance (catalog, lineage, quality)
3. Train domain teams on data engineering
4. Start with "data product thinking" (SLAs, documentation) without full decentralization
5. Reconsider data mesh at 500+ people or when central team is clear bottleneck

**Hybrid Option:**
- Sales domain (most mature) could start owning data products
- Marketing and Product remain centralized
- Platform team provides shared infrastructure

---

## Scenario 4: Lakehouse Table Format Selection

**Context:**
- Building lakehouse on S3
- Need Spark for ML
- Need Trino for BI queries
- Want to avoid vendor lock-in

**Recommendation:** Apache Iceberg

**Why:**
- **Multi-engine support:** Both Spark and Trino have excellent Iceberg support
- **Vendor-neutral:** Apache Foundation governance (not Databricks-led)
- **Hidden partitioning:** Query without partition predicates
- **Partition evolution:** Change partitioning without rewriting data
- **Mature ecosystem:** Apache Polaris (catalog), Project Nessie (versioning)

**Alternative:** Delta Lake if committed to Databricks, but less optimal for Trino

**Implementation:**
```sql
CREATE TABLE catalog.db.sales (
  order_id BIGINT,
  customer_id BIGINT,
  order_date DATE,
  amount DECIMAL(10,2)
)
USING iceberg
PARTITIONED BY (days(order_date));
```

---

## Scenario 5: Streaming + Batch Architecture

**Context:**
- Need both real-time dashboards and historical analytics
- Data sources: Kafka (streaming), PostgreSQL (batch)
- Team: Experienced data engineers

**Recommendation:** Kappa Architecture with Medallion

**Architecture:**
```
Kafka (Streaming)
  → Flink (Stream Processing)
  → Bronze Layer (Iceberg tables)
  → Silver Layer (cleaned, 5-minute windows)
  → Gold Layer (BI dashboards + ML features)

PostgreSQL (Batch)
  → Fivetran (CDC)
  → Bronze Layer
  → Silver Layer (daily batch)
  → Gold Layer
```

**Unified Gold Layer:** Merge streaming and batch data

**Why:**
- Single pipeline for both streaming and batch (Kappa)
- Medallion architecture for quality layers
- Iceberg supports both streaming writes (Flink) and batch reads (Trino)

**Trade-Offs:**
- Complexity: High (streaming infrastructure)
- Latency: Real-time (milliseconds for streaming path)
- Cost: Medium (compute for streaming)

---

## Scenario 6: Cost Optimization

**Context:**
- Currently on Snowflake
- $50K/month bill
- Mostly BI workloads
- Want to reduce costs

**Recommendation:** Migrate to Lakehouse

**Strategy:**
1. **Assess workloads:**
   - 80% of queries access last 30 days
   - 20% access historical data (>1 year)

2. **Hot-Cold Architecture:**
   - Hot data (last 30 days): Snowflake
   - Cold data (>30 days): Iceberg on S3
   - Unified view: Snowflake External Tables + Iceberg

3. **Incremental Migration:**
   - Week 1-2: Export historical data to S3 as Iceberg tables
   - Week 3-4: Update queries to use external tables for historical data
   - Week 5+: Keep only hot data in Snowflake

**Cost Savings:**
- Snowflake: $50K/month → $15K/month (70% reduction)
- S3 + Trino: $5K/month
- Total: $20K/month (60% savings)

**Trade-Offs:**
- Query performance: Slightly slower for historical queries
- Complexity: Moderate (manage hybrid architecture)
- Maintenance: Some ops work for Iceberg tables

---

## Decision Framework Summary

| Scenario | Organization Size | Primary Workload | Recommendation |
|----------|------------------|------------------|----------------|
| Startup | <50 | BI + Early ML | Data Warehouse (BigQuery, Snowflake) |
| Growth | 50-500 | BI + ML | Data Lakehouse (Databricks, Iceberg) |
| Enterprise | >500 | Mixed | Hybrid (Snowflake BI + Databricks ML) |
| Data Mesh | >500 + Bottleneck | Decentralized | Domain-owned data products |
| Cost-Sensitive | Any | Any | Lakehouse (60-80% cheaper) |
| Streaming + Batch | Any | Real-time + Historical | Kappa + Medallion |
