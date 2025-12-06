# Data Architecture Decision Frameworks

## Table of Contents

1. [Storage Paradigm Selection](#storage-paradigm-selection)
2. [Data Modeling Approach](#data-modeling-approach)
3. [Data Mesh Readiness Assessment](#data-mesh-readiness-assessment)
4. [Open Table Format Selection](#open-table-format-selection)

---

## Storage Paradigm Selection

### Decision Tree

```
Start: What is your primary use case?
│
├─ BI/Reporting only
│  └─ Known queries, structured data?
│     ├─ Yes → Data Warehouse
│     └─ No → Data Lakehouse
│
├─ ML/AI primary
│  └─ Need raw data + feature engineering?
│     ├─ Yes → Data Lake or Lakehouse
│     └─ No → Data Lakehouse
│
├─ Mixed BI + ML
│  └─ Budget constraints?
│     ├─ High budget → Data Warehouse + Data Lake
│     └─ Optimizing cost → Data Lakehouse
│
└─ Exploratory/Unknown
   └─ Data Lake (preserve raw, decide later)
```

### Detailed Criteria Matrix

| Criteria | Data Lake | Data Warehouse | Data Lakehouse |
|----------|-----------|----------------|----------------|
| **Cost** | Lowest ($) | Highest ($$$) | Medium ($$) |
| **Query Performance** | Slowest | Fastest | Fast |
| **Schema Flexibility** | Highest | Lowest | High |
| **Data Quality** | User-managed | Enforced | Optional enforcement |
| **ACID Transactions** | No | Yes | Yes (with table formats) |
| **BI Workloads** | Poor | Excellent | Good |
| **ML Workloads** | Excellent | Limited | Excellent |
| **Governance** | Difficult | Strong | Improving |
| **Time to Value** | Slow | Fast (if schema known) | Medium |
| **Skill Level** | High (data engineers) | Medium (analysts) | High |
| **Schema Evolution** | Trivial (schema-on-read) | Difficult (migrations) | Easy (table formats) |
| **Multi-Engine Support** | Excellent | Limited | Excellent |

### Recommendation by Organization Size

**Startup (<50 people):**
- **Primary:** Data Warehouse (Snowflake, BigQuery)
- **Why:** Simplicity over flexibility; focus on BI
- **Cost:** Pay-per-use pricing manageable at small scale
- **Skills:** Analysts can write SQL; no data engineers needed

**Growth (50-500 people):**
- **Primary:** Data Lakehouse (Databricks with Delta Lake, or Iceberg on S3)
- **Why:** Balance cost and features; support BI and emerging ML
- **Cost:** 60-80% cheaper than warehouse at scale
- **Skills:** Hire 1-2 data engineers for lakehouse management

**Enterprise (>500 people):**
- **Primary:** Hybrid or unified Lakehouse
- **Option 1 (Hybrid):** Snowflake for BI + Databricks for ML
- **Option 2 (Unified):** Databricks lakehouse for all workloads
- **Why:** Scale and specialization requirements
- **Cost:** Negotiate enterprise contracts; leverage reserved capacity

### Cost-Benefit Analysis

**Data Lake:**
- **Storage Cost:** $0.02-0.03/GB/month (S3, GCS)
- **Compute Cost:** Pay per query (Athena, Presto)
- **Total Cost (1TB):** ~$30-50/month storage + query costs
- **Best for:** Archive, exploration, raw data retention

**Data Warehouse:**
- **Storage Cost:** $20-40/TB/month (Snowflake, BigQuery)
- **Compute Cost:** $2-5/credit-hour (varies by size)
- **Total Cost (1TB):** ~$500-2,000/month (including compute)
- **Best for:** Known BI workloads, fast queries

**Data Lakehouse:**
- **Storage Cost:** $0.02-0.03/GB/month (lake storage)
- **Compute Cost:** $2-5/DBU-hour (Databricks) or similar
- **Total Cost (1TB):** ~$100-500/month (depending on compute)
- **Best for:** Mixed workloads, cost optimization

---

## Data Modeling Approach

### Decision Matrix

```
Primary Workload?
│
├─ Analytical (BI, Dashboards)
│  └─ Query patterns known?
│     ├─ Yes → Dimensional (Star Schema)
│     └─ No → Wide Tables or Data Vault
│
├─ Transactional (OLTP)
│  └─ Normalized (3NF)
│
├─ Compliance/Audit Required?
│  └─ Yes → Data Vault 2.0
│  └─ No → Dimensional or Wide
│
├─ Data Science/ML
│  └─ Wide Tables (Feature Tables)
│
└─ Multi-source Integration
   └─ Data Vault 2.0
```

### Criteria by Model

| Factor | Dimensional | Normalized | Data Vault | Wide Tables |
|--------|-------------|------------|------------|-------------|
| **BI Performance** | Excellent | Poor | Poor (needs mart) | Excellent |
| **Flexibility** | Low | Medium | High | Low |
| **Update Complexity** | Medium | Low | Low | High |
| **Historical Tracking** | SCD Types | Difficult | Excellent | Medium |
| **Auditability** | Medium | Medium | Excellent | Low |
| **Query Complexity** | Simple | Complex | Complex | Simplest |
| **Storage Efficiency** | Good | Best | Medium | Worst |
| **Learning Curve** | Medium | Low | High | Low |
| **Schema Changes** | Moderate impact | Minimal impact | Minimal impact | High impact |
| **Join Performance** | Fast (denormalized) | Slow (many joins) | Slow (many joins) | Fastest (no joins) |

### Use Case Mapping

**Dimensional Modeling (Star/Snowflake):**
- Sales analytics dashboard
- Customer behavior analysis
- Financial reporting
- Marketing attribution
- Operational KPIs

**Normalized Modeling (3NF):**
- E-commerce order management
- CRM systems
- ERP systems
- Inventory management
- Transactional databases

**Data Vault 2.0:**
- Banking (regulatory compliance)
- Healthcare (HIPAA audit trails)
- Multi-source master data management
- Long-term historical archives
- Insurance claims processing

**Wide Tables (Denormalized):**
- ML feature stores
- Data science notebooks
- High-performance dashboards
- Aggregated reporting tables
- Real-time analytics

### Slowly Changing Dimensions (SCD) Selection

**Type 1 (Overwrite):**
- **Use when:** History doesn't matter
- **Example:** Fixing typos in customer names
- **Storage:** No additional columns
- **Query Complexity:** Simple

**Type 2 (Add Row):**
- **Use when:** Full history is critical
- **Example:** Customer address changes
- **Storage:** Add `effective_date`, `end_date`, `is_current`
- **Query Complexity:** Filter on `is_current` or date ranges

**Type 3 (Add Column):**
- **Use when:** Need to compare current vs previous
- **Example:** Customer's previous and current segment
- **Storage:** Add `previous_value` column
- **Query Complexity:** Simple, limited to one previous value

**Type 6 (Hybrid 1+2+3):**
- **Use when:** Need full history + current value in all rows
- **Example:** Product pricing with full history and current price
- **Storage:** Combine Type 2 + add `current_value` to all rows
- **Query Complexity:** Medium

---

## Data Mesh Readiness Assessment

### 6-Factor Assessment (Score 1-5 each)

**1. Domain Clarity:**
- 1: No clear domains, everything is interconnected
- 3: Some domains exist but boundaries are fuzzy
- 5: Clear bounded contexts (Domain-Driven Design), distinct ownership

**2. Team Maturity:**
- 1: Domain teams have no data skills
- 3: Some teams have analysts, but no data engineers
- 5: Domain teams have data engineers, can own pipelines

**3. Platform Capability:**
- 1: No self-serve infrastructure, manual provisioning
- 3: Some automation (Terraform), but requires platform team involvement
- 5: Fully self-serve platform (domains can deploy independently)

**4. Governance Maturity:**
- 1: No data governance, ad-hoc policies
- 3: Centralized governance, but difficult to enforce
- 5: Federated governance with automated enforcement

**5. Scale Need:**
- 1: Central team is adequate, no bottleneck
- 3: Central team is sometimes slow, but manageable
- 5: Central team is clear bottleneck, blocks domain progress

**6. Organizational Buy-In:**
- 1: No leadership support, resistance to change
- 3: Leadership is interested, but skeptical
- 5: Strong leadership support, cultural readiness

### Scoring Interpretation

**24-30 points: Strong Data Mesh Candidate**
- Proceed with data mesh implementation
- Start with pilot domain (sales or marketing)
- Build self-serve platform capabilities
- Establish federated governance framework

**18-23 points: Hybrid Approach**
- Implement data mesh for critical domains only
- Keep less critical domains centralized
- Gradually expand mesh as maturity increases
- Example: Sales domain owns data products, others remain central

**12-17 points: Build Foundation First**
- Invest in self-serve platform (infrastructure as code)
- Improve governance (catalog, lineage, quality)
- Train domain teams on data engineering
- Reassess in 6-12 months

**6-11 points: Centralized Approach**
- Data mesh is premature
- Focus on scaling central team
- Improve centralized platform efficiency
- Consider data mesh at >500 people or when bottleneck emerges

### Red Flags (Do NOT Pursue Data Mesh)

**Organizational:**
- Small organization (<100 people)
- Unclear domain boundaries
- No platform engineering team
- Leadership resistance

**Technical:**
- Weak data governance
- No catalog or lineage tooling
- Poor observability
- Immature data engineering practices

**Cultural:**
- Domain teams lack data ownership mindset
- Centralized team is not a bottleneck
- No appetite for decentralization
- Resistance to data-as-product thinking

### Readiness Checklist

**Before starting data mesh:**
- [ ] Organization has >500 people (or >200 with clear need)
- [ ] 3+ clear business domains with distinct ownership
- [ ] Domain teams have data engineering skills or budget to hire
- [ ] Self-serve platform exists (infrastructure as code, CI/CD)
- [ ] Data catalog and lineage tooling in place
- [ ] Federated governance processes defined
- [ ] Central data team is clear bottleneck (proven, not assumed)
- [ ] Leadership buy-in and commitment to cultural shift
- [ ] Budget for domain-level data teams
- [ ] Pilot domain identified with executive sponsor

---

## Open Table Format Selection

### Feature Comparison Matrix

| Feature | Apache Iceberg | Delta Lake | Apache Hudi |
|---------|---------------|------------|-------------|
| **Primary Use Case** | Multi-engine analytics | Databricks ecosystem | Streaming upserts |
| **ACID Transactions** | Yes (serializable) | Yes | Yes |
| **Time Travel** | Yes (snapshot-based) | Yes (version-based) | Yes (commit-based) |
| **Schema Evolution** | Excellent | Good | Good |
| **Add/Drop/Rename Columns** | Yes (all operations) | Yes | Yes |
| **Partition Evolution** | Yes (no rewrite) | No (requires rewrite) | Limited |
| **Hidden Partitioning** | Yes | No | No |
| **Multi-Engine Support** | Excellent (Spark, Trino, Flink, Presto, Dremio) | Spark-primary (limited Trino) | Spark, Flink |
| **Metadata Management** | Excellent (manifest files, metadata layers) | Good (transaction log) | Good (timeline, metadata) |
| **Streaming** | Good | Excellent | Excellent (best) |
| **Upserts/Deletes** | Good | Excellent | Excellent (optimized) |
| **CDC Support** | Good | Excellent | Excellent (best) |
| **Incremental Processing** | Good | Good | Excellent (incremental view) |
| **Maturity** | High (production since 2018) | High (production since 2019) | Medium (maturing) |
| **Governance** | Apache Foundation | Databricks (Linux Foundation) | Apache Foundation |
| **Vendor Neutrality** | Highest | Medium (Databricks-led) | High |
| **Community Support** | Broadest (AWS, Google, Snowflake, Databricks) | Databricks-focused | Growing |
| **Documentation** | Excellent | Excellent | Good |
| **Ecosystem Tools** | Polaris, Nessie, Lakekeeper | Databricks Unity Catalog | Hudi DeltaStreamer |

### Decision Tree

```
Start: What is your priority?
│
├─ Multi-engine flexibility (avoid lock-in)
│  └─ Apache Iceberg
│
├─ Databricks ecosystem (committed)
│  └─ Delta Lake
│
├─ Frequent upserts/CDC (Change Data Capture)
│  └─ Apache Hudi
│
├─ Partition evolution without rewrites
│  └─ Apache Iceberg
│
├─ Maximum community support
│  └─ Apache Iceberg (broadest adoption)
│
├─ Streaming-first architecture
│  └─ Apache Hudi or Delta Lake
│
└─ Cost optimization (query performance)
   └─ Apache Iceberg or Delta Lake
```

### Vendor Lock-In Analysis

**Apache Iceberg:**
- **Governance:** Apache Foundation (vendor-neutral)
- **Support:** AWS (Athena, EMR), Google (BigQuery), Snowflake, Databricks, Cloudera
- **Migration:** Easy to switch query engines (multi-engine design)
- **Lock-In Risk:** Lowest

**Delta Lake:**
- **Governance:** Linux Foundation (Databricks-led)
- **Support:** Databricks (primary), AWS EMR, Azure Synapse, limited Trino
- **Migration:** Possible but optimized for Databricks
- **Lock-In Risk:** Medium (Databricks ecosystem)

**Apache Hudi:**
- **Governance:** Apache Foundation (vendor-neutral)
- **Support:** AWS (EMR, Glue), Uber, Alibaba, ByteDance
- **Migration:** Possible, but fewer query engine options
- **Lock-In Risk:** Low-Medium

### Workload-Based Recommendations

**Batch Analytics (BI, Reporting):**
- **Best:** Apache Iceberg
- **Why:** Multi-engine support, best query performance optimizations
- **Alternative:** Delta Lake if using Databricks

**Streaming Analytics (Real-Time):**
- **Best:** Apache Hudi or Delta Lake
- **Why:** Optimized for streaming upserts and CDC
- **Alternative:** Iceberg with Flink for streaming

**Mixed Batch + Streaming:**
- **Best:** Apache Iceberg
- **Why:** Balanced support for both patterns
- **Alternative:** Delta Lake (streaming excellent, batch good)

**ML/Data Science:**
- **Best:** Apache Iceberg or Delta Lake
- **Why:** Time travel, schema evolution, snapshot isolation
- **Alternative:** Both are excellent; choose based on ecosystem

**CDC-Heavy Workloads:**
- **Best:** Apache Hudi
- **Why:** Optimized for record-level updates (Merge-on-Read)
- **Alternative:** Delta Lake (also excellent for CDC)

### Migration Considerations

**Migrating from Hive Tables:**
- **Iceberg:** In-place migration (no data rewrite)
- **Delta Lake:** Requires data rewrite
- **Hudi:** Requires data rewrite

**Migrating from Parquet:**
- **All:** Require metadata creation; data files can often be reused

**Cross-Format Migration:**
- **Iceberg ↔ Delta Lake:** Possible with tools (e.g., Delta Lake Universal Format)
- **Hudi ↔ Others:** More complex, may require full rewrite

### Recommendation Summary

**For New Projects:**
- **Default:** Apache Iceberg (vendor-neutral, broadest support)
- **If Databricks-committed:** Delta Lake
- **If CDC-heavy:** Apache Hudi

**For Existing Systems:**
- **Hive migration:** Apache Iceberg (in-place migration)
- **Databricks platform:** Delta Lake
- **Streaming-first:** Apache Hudi or Delta Lake

**Red Flags for Each Format:**
- **Iceberg:** Avoid if only using Databricks (Delta Lake is better integrated)
- **Delta Lake:** Avoid if need multi-cloud, multi-engine flexibility
- **Hudi:** Avoid if batch analytics is primary workload (Iceberg/Delta better)
