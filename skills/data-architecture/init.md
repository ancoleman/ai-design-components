# Data Architecture Skill - Master Plan

**Skill Name:** `data-architecture`
**Skill Level:** High Level (Strategic/Architectural, 8,000-12,000 tokens)
**Status:** Planning Phase (init.md complete, SKILL.md to be created)
**Last Updated:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [Component Taxonomy](#component-taxonomy)
5. [Decision Frameworks](#decision-frameworks)
6. [Data Modeling Approaches](#data-modeling-approaches)
7. [Storage Paradigms](#storage-paradigms)
8. [Data Mesh Principles](#data-mesh-principles)
9. [Modern Data Stack Architecture](#modern-data-stack-architecture)
10. [Medallion Architecture Pattern](#medallion-architecture-pattern)
11. [Data Governance and Cataloging](#data-governance-and-cataloging)
12. [Tool Recommendations](#tool-recommendations)
13. [Skill Structure Design](#skill-structure-design)
14. [Integration Points](#integration-points)
15. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why Data Architecture Matters in 2025

Data architecture has evolved from traditional data warehousing to cloud-native, decentralized, and AI-optimized patterns. In 2025, organizations face unprecedented data volumes, diverse sources, and AI/ML requirements that demand modern architectural approaches.

**Market Drivers:**
- **AI/ML Data Requirements:** LLMs and ML models need massive, high-quality datasets
- **Real-Time Analytics:** Business decisions require millisecond-latency data access
- **Data Democratization:** Self-service analytics for all business users
- **Multi-Cloud Reality:** Data distributed across AWS, GCP, Azure, on-premises
- **Regulatory Compliance:** GDPR, CCPA, SOC2 require governance-first design
- **Cost Optimization:** Cloud storage costs drive lakehouse adoption

**Strategic Value:**
1. **AI Enablement:** Proper data architecture unlocks AI/ML capabilities
2. **Business Agility:** Self-service analytics accelerates decision-making
3. **Cost Efficiency:** Lakehouse patterns reduce storage/compute costs 60-80%
4. **Scalability:** Modern patterns handle petabyte-scale data
5. **Governance:** Centralized policies with decentralized execution

### Competitive Landscape 2025

**Traditional vs Modern:**
- **Old:** Centralized data warehouses (Teradata, Oracle)
- **New:** Cloud-native lakehouses (Snowflake, Databricks)
- **Emerging:** Data mesh with domain ownership

**Key Differentiators:**
- **Separation of Storage/Compute:** Scale independently
- **Schema-on-Read:** Flexibility for evolving requirements
- **Open Table Formats:** Apache Iceberg, Delta Lake prevent vendor lock-in
- **Streaming-First:** Real-time ingestion as default

### How This Differs from Existing Solutions

**Existing Resources:**
- **Vendor Documentation:** Snowflake/Databricks docs are tool-specific
- **Academic Papers:** Data mesh/lakehouse theory without practical implementation
- **Legacy Patterns:** Kimball/Inmon dimensional modeling without cloud context

**Our Approach:**
- **Decision-Driven:** When to use data lake vs warehouse vs lakehouse
- **Multi-Paradigm:** Covers dimensional, normalized, data vault, data mesh
- **Tool-Agnostic:** Patterns work across Snowflake, Databricks, BigQuery
- **AI-First:** Optimized for ML feature stores and LLM training data
- **Governance-Integrated:** Security, lineage, quality from day one

---

## Skill Purpose and Scope

### What This Skill Teaches

**Core Competencies:**

1. **Data Modeling Approaches**
   - Dimensional modeling (Kimball star/snowflake schemas)
   - Normalized modeling (3NF, BCNF for transactional systems)
   - Data Vault 2.0 (hubs, links, satellites for flexibility)
   - Wide tables (denormalized for analytical performance)
   - When to use each approach

2. **Storage Paradigms**
   - Data Lake (raw, unstructured, cost-optimized)
   - Data Warehouse (structured, optimized for BI)
   - Data Lakehouse (hybrid: lake flexibility + warehouse reliability)
   - Trade-offs: cost, performance, governance

3. **Data Mesh Principles**
   - Domain-oriented decentralization
   - Data as a product
   - Self-serve data infrastructure
   - Federated computational governance
   - When data mesh fits vs overkill

4. **Modern Data Stack Components**
   - Ingestion (Fivetran, Airbyte, Kafka)
   - Transformation (dbt, Dataform)
   - Orchestration (Airflow, Dagster, Prefect)
   - Storage (Snowflake, Databricks, BigQuery)
   - Visualization (Tableau, Looker, Power BI)

5. **Medallion Architecture**
   - Bronze layer (raw ingestion)
   - Silver layer (cleaned, conformed)
   - Gold layer (business-level aggregates)
   - Data quality patterns at each layer

6. **Open Table Formats**
   - Apache Iceberg (metadata layers, time travel)
   - Delta Lake (ACID transactions, versioning)
   - Apache Hudi (upserts, incremental processing)
   - When to use each format

7. **Data Governance and Cataloging**
   - Data discovery (Alation, Collibra, DataHub)
   - Lineage tracking (OpenLineage, Marquez)
   - Data quality (Great Expectations, Soda)
   - Access control (RBAC, ABAC, column-level security)

8. **Schema Evolution Strategies**
   - Schema-on-read vs schema-on-write
   - Backward/forward compatibility
   - Schema versioning and migration
   - Handling breaking changes

9. **Data Product Design**
   - Interface contracts (APIs, schemas)
   - SLAs and SLOs for data products
   - Quality metrics and monitoring
   - Consumer feedback loops

10. **Performance Optimization**
    - Partitioning strategies (time, geography, hash)
    - Clustering and indexing
    - Materialized views
    - Query optimization patterns

### What This Skill Does NOT Cover

- **Specific Tool Implementation:** See `databases-*` skills for database-specific details
- **Data Ingestion Mechanics:** See `ingesting-data` for ETL/ELT patterns
- **Streaming Data:** See `streaming-data` for Kafka, Flink, Spark Streaming
- **Data Transformation:** See `data-transformation` for dbt, Dataform specifics
- **ML Engineering:** See `ai-data-engineering` for feature stores, training pipelines
- **Data Science:** Statistical modeling, ML algorithms
- **Database Administration:** Backup/recovery, performance tuning
- **Cloud Provider Specifics:** AWS Redshift vs GCP BigQuery operational details

**Scope Boundaries:**
- **Focus:** Strategic architectural decisions and patterns
- **Level:** High-level design, not implementation code
- **Audience:** Data architects, platform engineers, technical leads

---

## Research Findings

### Google Search Grounding (December 2025)

**Research Methodology:**
- Conducted 4 targeted searches on data architecture patterns, data mesh vs lakehouse, modern data stack, and dimensional modeling
- Successfully gathered insights from 2 queries (2 experienced technical errors)
- Cross-referenced with Context7 library research for tool validation

**Key 2025 Trends:**

**1. Data Architecture Patterns:**
- **Scalability is Critical:** Organizations generating more data than ever; architecture must rapidly integrate new sources
- **Cloud-Native Architectures:** Modular, cloud-native frameworks are standard; elasticity, modularity, and speed are core requirements
- **Business-Driven Approach:** Architecture aligns to business outcomes (reporting, self-service, ML, real-time processing)
- **Hybrid Architectures:** Support multiple data types (structured, semi-structured, unstructured), sources, and delivery modes
- **Data Lakehouse Emergence:** Combines flexibility of data lakes with reliability of data warehouses
- **Layered Ecosystem:** Ingestion → Storage → Processing → Orchestration/Transformation → Delivery

**Architectural Layers (2025 Standard):**
1. **Ingestion:** Stream and batch (Apache Kafka, Apache NiFi, AWS Kinesis)
2. **Storage:** Hybrid lakes/warehouses (Apache Iceberg, Delta Lake for schema evolution and time-travel)
3. **Processing:** Elastic compute (Databricks, Snowflake, BigQuery) supporting SQL and programmatic workflows
4. **Orchestration/Transformation:** dbt, Apache Airflow, Dagster for pipeline automation
5. **Delivery:** Governed interfaces for consumption

**Data Processing Paradigms:**
- Traditional ETL pipelines
- In-database ELT transformations
- Low-code data wrangling
- Streaming data integration
- Virtualized access via SQL or APIs

**Best Practices:**
- Start small, scale intelligently (avoid over-engineering)
- Invest in automation (infrastructure-as-code, CI/CD)
- Prioritize observability (pipeline health, data quality, system performance)
- Enable collaboration (shared environments, version control)
- Align architecture to business outcomes, not just technologies
- Treat data modeling as strategic, ongoing activity

**2. Data Mesh vs Data Lakehouse:**

**Data Lakehouse:**
- **What:** Architecture combining cost-efficiency/flexibility of data lakes with data management/ACID capabilities of warehouses
- **How:** Stores data in low-cost cloud object storage; metadata layer provides structure, governance, warehouse-like features
- **Benefits:** BI and ML on all data; single system; complete, up-to-date data; unified analytics without data movement
- **Focus:** Optimizing current data centralization workflows

**Data Mesh:**
- **What:** Decentralized architecture organizing data by business domain (marketing, sales, etc.)
- **How:** Domain teams treat data as a product; central framework governs data sharing
- **Benefits:** Addresses centralized bottlenecks; self-service access; reduces silos; improves agility and decision-making speed
- **Focus:** Decentralized data management

**Key Differences:**
| Aspect | Data Lakehouse | Data Mesh |
|--------|----------------|-----------|
| Architecture | Unified, centralized | Decentralized, domain-oriented |
| Data Ownership | Centralized teams | Distributed to domain teams |
| Governance | Centralized policies | Federated governance |
| Scope | Technology-focused | Organizational + cultural shifts |
| Self-Service | Optimized accessibility | Self-serve infrastructure as core principle |
| Data as Product | Not emphasized | Core principle |
| Complexity | Lower administrative burden | Higher (multiple domain owners) |

**When to Use Which:**
- **Data Lakehouse:** Smaller businesses, centralized approach preferred, simpler administrative needs
- **Data Mesh:** Large datasets, frequently updated analyses, domain-driven platforms, bottlenecked central teams

**Relationship:** Not mutually exclusive; data mesh is organizational approach, lakehouse is technology that can support mesh implementation

**3. Modern Data Stack (2025):**

**Core Components:**
- **Fivetran:** Data integration tool automating extraction from various sources and loading into warehouse; pre-built connectors simplify ingestion
- **dbt (data build tool):** Transformation tool enabling SQL-based data transformation in warehouse; promotes software engineering approach (version control, testing, documentation)
- **Snowflake:** Cloud-based data warehouse providing scalable storage/compute for analytics

**Typical Architecture Flow:**
1. Fivetran extracts from sources (databases, applications, cloud platforms) → loads into Snowflake
2. dbt transforms raw data within Snowflake into analytics-ready models
3. BI tools connect to Snowflake for visualization/analysis

**Benefits:** Streamlined pipeline building, automated ingestion/transformation, scalable warehouse

**4. Dimensional Modeling Best Practices:**
- **Choose appropriate granularity:** Level of detail in fact table impacts analysis and query performance; align with business needs, query patterns, storage constraints
- **Build star schema:** Dimensions and fact tables designed to minimize query time
- **Keep dimension tables denormalized:** Improves performance
- **Limit foreign keys:** Reduce number in fact table
- **Use unique key values:** Each dimension table needs key to avoid many-to-many relationships
- **Ensure appropriate indexing:** Index fact and dimension tables
- **Optimize schema:** Regularly review based on usage patterns
- **Incremental refresh:** For large fact tables, reduce rows transferred
- **Self-describing column names:** Use in dimension tables
- **Consistent grain:** Fact tables always load data at consistent grain

### Context7 Library Research (December 2025)

**Research Methodology:**
- Searched for dbt, Apache Iceberg, Delta Lake using Context7 resolve-library-id
- Successfully retrieved dbt and Apache Iceberg metadata
- Delta Lake queries experienced connection errors (Context7 service intermittent)
- Analyzed trust scores, code snippet counts, source reputations

**1. dbt (data build tool) - Context7: /websites/getdbt**
- **Code Snippets:** 3,532 (highest count, indicating extensive documentation)
- **Source Reputation:** High
- **Benchmark Score:** 87.0 (excellent quality indicator)
- **Description:** Industry standard for data transformation; enables analytics engineers to transform data and deploy analytics code using software engineering best practices
- **Notable Packages:**
  - dbt-core (/dbt-labs/dbt-core): 90 snippets, High reputation, Benchmark 64.5
  - dbt-utils (/dbt-labs/dbt-utils): 74 snippets, High reputation, Benchmark 80.3
  - dbt-databricks (/databricks/dbt-databricks): 116 snippets, High reputation, Benchmark 72.4
  - dbt-project-evaluator (/dbt-labs/dbt-project-evaluator): 64 snippets, High reputation, Benchmark 78.5
  - dbt-expectations (/metaplane/dbt-expectations): 70 snippets, High reputation (Great Expectations integration)

**Key Insight:** dbt ecosystem is mature with extensive documentation, high trust scores, and comprehensive package ecosystem for testing, governance, and cross-platform support.

**2. Apache Iceberg - Context7: /apache/iceberg**
- **Code Snippets:** 832 (primary project)
- **Source Reputation:** High
- **Benchmark Score:** 79.7 (strong quality)
- **Description:** High-performance open table format for huge analytic datasets; brings reliability and simplicity to big data
- **Alternative:** /netflix/iceberg (original Netflix project): 1,469 snippets, High reputation
- **Related Implementations:**
  - Apache Iceberg Rust (/apache/iceberg-rust): 71 snippets, High reputation, Benchmark 64.5
  - Iceberg Golang (/apache/iceberg-go): 46 snippets, High reputation, Benchmark 40.4

**Ecosystem Tools:**
- **Apache Polaris** (/apache/polaris): 1,224 snippets, High reputation - Open-source catalog for Iceberg implementing REST API; enables multi-engine interoperability
- **Project Nessie** (/websites/projectnessie_nessie-latest): 356 snippets, High reputation, Benchmark 41 - Cloud-native service providing cross-table transactions and Git-like data history for Iceberg data lakes
- **Lakekeeper** (/lakekeeper/lakekeeper): 301 snippets, Medium reputation, Benchmark 49 - Apache-licensed, secure, fast Iceberg REST Catalog in Rust

**Key Insight:** Apache Iceberg has strong ecosystem support across multiple languages (Java, Rust, Go) and comprehensive catalog/governance tooling. High trust scores indicate production readiness.

**3. Delta Lake - Research Incomplete**
- Context7 queries experienced connection errors during research
- Delta Lake is Databricks' open-source project, competing with Iceberg
- Known features: ACID transactions, time travel, schema evolution, upserts
- **Recommendation:** Validate with Databricks documentation when implementing

**Trust Score Summary:**
| Tool | Primary Library ID | Code Snippets | Reputation | Benchmark | Status |
|------|-------------------|---------------|------------|-----------|--------|
| dbt | /websites/getdbt | 3,532 | High | 87.0 | ✅ Production-ready |
| Apache Iceberg | /apache/iceberg | 832 | High | 79.7 | ✅ Production-ready |
| Delta Lake | N/A (research error) | N/A | N/A | N/A | ⚠️ Validate separately |

**Recommendation:** Both dbt and Apache Iceberg have excellent trust scores and extensive documentation. Safe to recommend as production-ready tools. Delta Lake should be validated through Databricks official docs.

---

## Component Taxonomy

### 1. Data Modeling Approaches

#### 1.1 Dimensional Modeling (Kimball Methodology)
**Purpose:** Optimized for analytical queries and business intelligence
**Structure:**
- **Fact Tables:** Measures/metrics (sales, transactions, events)
- **Dimension Tables:** Context (time, product, customer, location)

**Patterns:**
- **Star Schema:** Fact table surrounded by denormalized dimension tables (simple, fast queries)
- **Snowflake Schema:** Normalized dimension tables (reduced redundancy, more joins)

**When to Use:**
- Business intelligence and reporting
- Known query patterns (dashboards, KPIs)
- Historical trend analysis
- User-friendly for SQL analysts

**Trade-offs:**
- ✅ Fast analytical queries
- ✅ Intuitive for business users
- ✅ Optimized for BI tools
- ❌ Inflexible to schema changes
- ❌ Denormalization creates redundancy
- ❌ Requires upfront modeling effort

**Example Use Cases:**
- Sales analytics dashboard
- Customer behavior analysis
- Financial reporting
- Marketing attribution

#### 1.2 Normalized Modeling (Inmon Methodology)
**Purpose:** Eliminate redundancy, ensure data integrity for transactional systems
**Structure:**
- 3rd Normal Form (3NF): Every non-key attribute depends only on primary key
- Boyce-Codd Normal Form (BCNF): Stricter version of 3NF

**When to Use:**
- Transactional systems (OLTP)
- Data with frequent updates
- Strong consistency requirements
- Source systems feeding data warehouse

**Trade-offs:**
- ✅ No redundancy
- ✅ Data integrity enforced
- ✅ Flexible to changes
- ❌ Complex joins slow analytical queries
- ❌ Not intuitive for business users
- ❌ Poor performance for BI

**Example Use Cases:**
- E-commerce order management
- CRM systems
- ERP systems
- Inventory management

#### 1.3 Data Vault 2.0
**Purpose:** Flexible, auditable, scalable model for enterprise data warehouses
**Structure:**
- **Hubs:** Unique business keys (Customer, Product)
- **Links:** Relationships between hubs (Order connects Customer + Product)
- **Satellites:** Descriptive attributes, temporal history

**When to Use:**
- Compliance-heavy industries (finance, healthcare)
- Audit requirements (track all changes)
- Uncertain requirements (agile data warehousing)
- Multiple source systems with overlapping data

**Trade-offs:**
- ✅ Highly flexible (easy to add sources)
- ✅ Complete audit trail
- ✅ Parallel loading (hubs, links, satellites independent)
- ❌ Complex queries (many joins)
- ❌ Requires data mart layer for BI
- ❌ Storage overhead

**Example Use Cases:**
- Banking (regulatory compliance)
- Healthcare (HIPAA audit trails)
- Multi-source master data management
- Long-term historical archives

#### 1.4 Wide Tables (Denormalized, One Big Table)
**Purpose:** Maximize query performance for analytical workloads
**Structure:**
- Single table with hundreds of columns
- Pre-joined dimensions and facts
- Optimized for columnar storage (Parquet, ORC)

**When to Use:**
- Cloud data warehouses (Snowflake, BigQuery)
- Known query patterns
- Columnar storage engines
- Data science/ML feature tables

**Trade-offs:**
- ✅ Fastest analytical queries (no joins)
- ✅ Simple for users (one table)
- ✅ Efficient in columnar storage (only read needed columns)
- ❌ Significant redundancy
- ❌ Large storage footprint
- ❌ Update complexity

**Example Use Cases:**
- ML feature stores
- Data science notebooks
- High-performance dashboards
- Aggregated reporting tables

### 2. Storage Paradigms

#### 2.1 Data Lake
**Definition:** Centralized repository storing raw data in native format at scale

**Characteristics:**
- **Schema-on-read:** Structure applied when querying, not when storing
- **Format-agnostic:** CSV, JSON, Parquet, Avro, images, logs
- **Cost-optimized:** Object storage (S3, GCS, ADLS)
- **Scalability:** Petabyte+ capacity

**Architecture:**
```
Data Lake Layers:
┌─────────────────────────────────────────┐
│ Raw Zone (Bronze)                       │
│ - Exact copy of source data             │
│ - No transformations                    │
│ - Immutable historical record           │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Cleaned Zone (Silver)                   │
│ - Validated, deduplicated               │
│ - Type conversions                      │
│ - Normalized formats                    │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Curated Zone (Gold)                     │
│ - Business-level aggregates             │
│ - Ready for consumption                 │
│ - Optimized for queries                 │
└─────────────────────────────────────────┘
```

**When to Use:**
- Diverse data sources (structured + unstructured)
- Exploratory analytics (unknown use cases)
- ML/AI training data (need raw, full-history data)
- Cost-sensitive workloads
- Long-term archival

**Trade-offs:**
- ✅ Lowest storage cost
- ✅ Schema flexibility
- ✅ Future-proof (keep raw data)
- ❌ No ACID guarantees
- ❌ Data quality issues
- ❌ Governance challenges (data swamp risk)

**Technologies:**
- Storage: AWS S3, Google GCS, Azure ADLS
- Formats: Parquet, ORC, Avro
- Query: Presto, Athena, Spark

#### 2.2 Data Warehouse
**Definition:** Centralized, structured repository optimized for analytical queries

**Characteristics:**
- **Schema-on-write:** Structure enforced on ingestion
- **Optimized for BI:** Indexing, partitioning, materialized views
- **ACID transactions:** Data consistency guaranteed
- **High performance:** Columnar storage, query optimization

**Architecture:**
```
Data Warehouse Architecture:
┌─────────────────────────────────────────┐
│ Staging Layer                           │
│ - Raw data ingestion                    │
│ - Temporary storage                     │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Integration Layer                       │
│ - Cleaned, conformed data               │
│ - Normalized or data vault              │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Presentation Layer (Data Marts)         │
│ - Star/snowflake schemas                │
│ - Department-specific views             │
└─────────────────────────────────────────┘
```

**When to Use:**
- Structured, relational data
- Known BI/reporting use cases
- Strong governance requirements
- Performance-critical dashboards
- Financial reporting, compliance

**Trade-offs:**
- ✅ Best query performance
- ✅ Strong governance
- ✅ Data quality enforced
- ❌ Higher storage cost
- ❌ Schema inflexibility
- ❌ Not ideal for unstructured data

**Technologies:**
- Cloud: Snowflake, BigQuery, Redshift, Synapse
- On-premises: Teradata, Oracle Exadata, Netezza

#### 2.3 Data Lakehouse
**Definition:** Hybrid architecture combining data lake flexibility with warehouse reliability

**Characteristics:**
- **Open table formats:** Apache Iceberg, Delta Lake, Apache Hudi
- **ACID transactions:** On top of object storage
- **Schema enforcement:** Optional validation on write
- **Time travel:** Query historical versions
- **Unified platform:** BI and ML on same data

**Architecture:**
```
Data Lakehouse Architecture:
┌─────────────────────────────────────────┐
│ Cloud Object Storage (S3, GCS, ADLS)   │
│ - Low-cost, scalable                    │
│ - Parquet/ORC files                     │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Metadata Layer (Iceberg/Delta)          │
│ - Table schema, statistics              │
│ - Partition information                 │
│ - Transaction log                       │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Compute Engines                         │
│ - Spark, Presto, Trino, Flink           │
│ - Multiple engines access same data     │
└─────────────────────────────────────────┘
```

**When to Use:**
- Both BI and ML workloads
- Cost optimization (60-80% cheaper than warehouse)
- Multi-engine access (Spark, Presto, Flink)
- Schema evolution requirements
- Streaming + batch processing

**Trade-offs:**
- ✅ Cost-effective (lake pricing, warehouse features)
- ✅ Flexible (structured + semi-structured)
- ✅ Multi-engine support
- ✅ Open formats (no vendor lock-in)
- ❌ Newer technology (less mature than warehouse)
- ❌ Performance not quite warehouse-level
- ❌ Requires careful optimization

**Technologies:**
- Table Formats: Apache Iceberg, Delta Lake, Apache Hudi
- Platforms: Databricks, Snowflake (Iceberg support), AWS Lake Formation
- Engines: Spark, Presto, Trino, Flink, Dremio

### 3. Data Mesh vs Centralized

#### 3.1 Centralized Data Platform (Traditional)
**Structure:**
- Single central data team owns all data assets
- Central data warehouse/lake
- Central ETL/ELT pipelines

**When to Use:**
- Small to medium organizations
- Limited data domains
- Clear data ownership
- Strong central team

**Trade-offs:**
- ✅ Simpler governance
- ✅ Consistent standards
- ✅ Lower overhead
- ❌ Central team bottleneck
- ❌ Doesn't scale to large orgs
- ❌ Slow to respond to domain needs

#### 3.2 Data Mesh (Decentralized)
**Principles:**
1. **Domain-oriented decentralization:** Each business domain owns its data
2. **Data as a product:** Domain teams treat data like product (quality, SLA, consumers)
3. **Self-serve data infrastructure:** Platform team provides tooling
4. **Federated computational governance:** Global policies, local implementation

**Architecture:**
```
Data Mesh Architecture:
┌─────────────────────────────────────────┐
│ Domain A (Sales)                        │
│ - Sales data product                    │
│ - Owns transformation + quality         │
│ - Exposes API/table interface           │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│ Domain B (Marketing)                    │
│ - Marketing data product                │
│ - Consumes Sales data product           │
│ - Owns marketing analytics              │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│ Domain C (Product)                      │
│ - Product usage data product            │
│ - Consumes Sales + Marketing            │
│ - Owns product metrics                  │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Self-Serve Data Platform                │
│ - Infrastructure as code                │
│ - CI/CD pipelines                       │
│ - Observability, cataloging             │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Federated Governance                    │
│ - Global policies (security, privacy)   │
│ - Standards (schema, quality)           │
│ - Compliance (GDPR, CCPA)               │
└─────────────────────────────────────────┘
```

**When to Use:**
- Large organizations (>500 people)
- Multiple business domains with clear ownership
- Central data team is bottleneck
- Domain teams have data expertise
- Need for rapid, independent iteration

**Trade-offs:**
- ✅ Scales to large organizations
- ✅ Domain expertise embedded in data
- ✅ Faster iteration (no central bottleneck)
- ✅ Clear ownership and accountability
- ❌ Higher complexity
- ❌ Requires strong platform team
- ❌ Governance more difficult
- ❌ Potential inconsistencies across domains

**Data Mesh + Lakehouse:**
- Data mesh is organizational/cultural
- Lakehouse is technical implementation
- Use lakehouse as underlying platform for mesh
- Each domain publishes data products to lakehouse

---

## Decision Frameworks

### Framework 1: Choosing Storage Paradigm

**Decision Tree:**
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

**Detailed Criteria:**

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

**Recommendation by Organization Size:**
- **Startup (<50 people):** Data Warehouse (Snowflake, BigQuery) - simplicity over flexibility
- **Growth (50-500 people):** Data Lakehouse (Databricks, Iceberg) - balance cost and features
- **Enterprise (>500 people):** Hybrid (Warehouse for BI, Lake for ML, or unified Lakehouse)

### Framework 2: Choosing Data Modeling Approach

**Decision Matrix:**
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

**Criteria by Model:**

| Factor | Dimensional | Normalized | Data Vault | Wide Tables |
|--------|-------------|------------|------------|-------------|
| **BI Performance** | Excellent | Poor | Poor (needs mart) | Excellent |
| **Flexibility** | Low | Medium | High | Low |
| **Update Complexity** | Medium | Low | Low | High |
| **Historical Tracking** | Slowly Changing Dims | Difficult | Excellent | Medium |
| **Auditability** | Medium | Medium | Excellent | Low |
| **Query Complexity** | Simple | Complex | Complex | Simplest |
| **Storage Efficiency** | Good | Best | Medium | Worst |
| **Learning Curve** | Medium | Low | High | Low |

### Framework 3: Data Mesh Readiness Assessment

**Score your organization (1-5 scale):**

1. **Domain Clarity:** Do we have clear business domains with distinct data ownership?
2. **Team Maturity:** Do domain teams have data engineering skills?
3. **Platform Capability:** Can we provide self-serve infrastructure?
4. **Governance Maturity:** Do we have federated governance processes?
5. **Scale Need:** Is our central data team a bottleneck?
6. **Organizational Buy-in:** Do leadership and teams support decentralization?

**Scoring:**
- **24-30 points:** Strong data mesh candidate
- **18-23 points:** Consider hybrid (critical domains mesh, others centralized)
- **12-17 points:** Improve platform and governance before mesh
- **6-11 points:** Stick with centralized; invest in team scaling

**Red Flags (Do NOT pursue data mesh):**
- Domains lack clear ownership
- No platform engineering team
- Weak data governance
- Small organization (<100 people)
- Domain teams lack data skills

### Framework 4: Open Table Format Selection

**Apache Iceberg vs Delta Lake vs Apache Hudi:**

| Feature | Apache Iceberg | Delta Lake | Apache Hudi |
|---------|---------------|------------|-------------|
| **Primary Use Case** | Multi-engine analytics | Databricks ecosystem | Streaming upserts |
| **ACID Transactions** | Yes | Yes | Yes |
| **Time Travel** | Yes | Yes | Yes |
| **Schema Evolution** | Excellent | Good | Good |
| **Partition Evolution** | Yes (no rewrite) | No | Limited |
| **Hidden Partitioning** | Yes | No | No |
| **Multi-Engine Support** | Excellent (Spark, Trino, Flink, Presto) | Spark-primary | Spark, Flink |
| **Metadata Management** | Excellent | Good | Good |
| **Streaming** | Good | Excellent | Excellent |
| **Upserts/Deletes** | Good | Excellent | Excellent (best) |
| **Maturity** | High | High | Medium |
| **Governance** | Apache Foundation | Databricks (Linux Foundation) | Apache Foundation |
| **Vendor Neutrality** | Highest | Medium (Databricks-led) | High |

**Decision Tree:**
```
Start: What is your priority?
│
├─ Multi-engine flexibility (avoid lock-in)
│  └─ Apache Iceberg
│
├─ Databricks ecosystem
│  └─ Delta Lake
│
├─ Frequent upserts/CDC (Change Data Capture)
│  └─ Apache Hudi
│
├─ Partition evolution without rewrites
│  └─ Apache Iceberg
│
└─ Maximum community support
   └─ Apache Iceberg (broadest adoption)
```

**Recommendation:** Apache Iceberg for new projects (vendor-neutral, best feature set). Delta Lake if committed to Databricks. Apache Hudi for CDC-heavy workloads.

---

## Data Modeling Approaches

### 1. Dimensional Modeling Deep Dive

**Star Schema Design Process:**

**Step 1: Identify Business Process**
- Example: "Analyze product sales performance"

**Step 2: Declare Grain**
- "One row per order line item"
- Grain must be specific and consistent

**Step 3: Identify Dimensions**
- Who: Customer
- What: Product
- When: Date/Time
- Where: Store/Location
- How: Payment Method
- Why: Promotion/Campaign

**Step 4: Identify Facts (Measures)**
- Quantity Sold
- Unit Price
- Discount Amount
- Net Revenue
- Cost
- Profit

**Example Star Schema:**
```
DimDate                DimProduct              DimCustomer
- DateKey (PK)         - ProductKey (PK)       - CustomerKey (PK)
- Date                 - ProductID             - CustomerID
- DayOfWeek            - ProductName           - CustomerName
- Month                - Category              - Segment
- Quarter              - Brand                 - Country
- Year                 - UnitCost              - JoinDate
           \                 |                 /
            \                |                /
             \               |               /
              \              |              /
               \             |             /
                \            |            /
                 FactSales (Fact Table)
                 - DateKey (FK)
                 - ProductKey (FK)
                 - CustomerKey (FK)
                 - StoreKey (FK)
                 - Quantity
                 - UnitPrice
                 - DiscountAmount
                 - NetRevenue
```

**Slowly Changing Dimensions (SCD):**

**Type 1 (Overwrite):**
- Update in place, no history
- Use when history doesn't matter (e.g., fixing typos)

**Type 2 (Add Row):**
- New row for each change
- Columns: `EffectiveDate`, `EndDate`, `IsCurrent`
- Use when history is critical (e.g., customer address changes)

**Type 3 (Add Column):**
- Store previous value in new column
- Use when need to compare current vs previous (limited history)

**Type 6 (Hybrid):**
- Combines Type 1, 2, and 3
- Tracks full history + current value in all rows

### 2. Data Vault 2.0 Deep Dive

**Core Concepts:**

**Hubs:**
- Unique business keys
- No descriptive attributes
- Immutable (never deleted)

```
HubCustomer
- CustomerHashKey (PK, hash of CustomerID)
- CustomerID (Business Key)
- LoadDate
- RecordSource
```

**Links:**
- Relationships between hubs
- Represent transactions or associations

```
LinkOrder
- OrderHashKey (PK)
- CustomerHashKey (FK to HubCustomer)
- ProductHashKey (FK to HubProduct)
- OrderID (Business Key)
- LoadDate
- RecordSource
```

**Satellites:**
- Descriptive attributes
- Temporal (tracks changes over time)
- Multiple satellites per hub (source-specific)

```
SatCustomer
- CustomerHashKey (FK to HubCustomer)
- LoadDate (part of PK)
- EndDate
- CustomerName
- Email
- Phone
- Address
- RecordSource
```

**When to Use Data Vault:**
- ✅ Compliance requirements (full audit trail)
- ✅ Multiple source systems with overlapping data
- ✅ Agile warehousing (requirements change frequently)
- ✅ Long-term historical archive
- ❌ Simple BI requirements (overkill)
- ❌ Small team (high complexity)

### 3. Wide Tables for Analytics

**Pattern: Denormalized Feature Table**

```
CustomerFeatureTable (for ML)
- customer_id
- tenure_days
- total_purchases_last_30d
- total_purchases_last_90d
- total_purchases_lifetime
- avg_order_value_last_30d
- product_category_1_purchases
- product_category_2_purchases
- ... (100+ features)
- last_purchase_date
- churn_risk_score
- customer_lifetime_value
```

**Optimization Techniques:**
- **Columnar Storage:** Parquet, ORC (only read needed columns)
- **Partitioning:** By date, customer_segment, geography
- **Clustering:** By customer_id, last_purchase_date
- **Materialized Views:** Pre-aggregate common calculations

**When to Use Wide Tables:**
- ✅ ML feature stores
- ✅ Data science notebooks (exploratory analysis)
- ✅ High-performance dashboards
- ✅ Columnar databases (Snowflake, BigQuery, Redshift)
- ❌ Frequent updates (high overhead)
- ❌ Normalized OLTP systems

---

## Storage Paradigms

### Data Lake Architecture Patterns

**Lambda Architecture (Batch + Speed Layers):**
```
Data Sources
     ↓
┌────────────────────┬────────────────────┐
│ Batch Layer        │ Speed Layer        │
│ (Hourly/Daily)     │ (Real-time)        │
│ - Historical data  │ - Recent data      │
│ - Reprocessable    │ - Low latency      │
│ - Spark batch      │ - Kafka + Flink    │
└──────────┬─────────┴──────────┬─────────┘
           │                     │
           ↓                     ↓
      Batch View            Real-time View
           │                     │
           └──────────┬──────────┘
                      ↓
                 Serving Layer
                  (Queries)
```

**Kappa Architecture (Streaming-Only):**
```
Data Sources
     ↓
 Stream Processing
 (Kafka + Flink)
     ↓
┌────────────────────┬────────────────────┐
│ Serving Layer      │ Archive Layer      │
│ (Last 30 days)     │ (All history)      │
│ - Fast queries     │ - S3/GCS           │
│ - Hot data         │ - Reprocessable    │
└────────────────────┴────────────────────┘
```

**Medallion Architecture (Databricks/Lakehouse Standard):**
```
Bronze Layer (Raw)
- Exact copy of source
- Append-only
- All history retained
     ↓
Silver Layer (Cleaned)
- Validated, deduplicated
- Type conversions
- Slowly Changing Dimensions applied
     ↓
Gold Layer (Business-level)
- Aggregates
- Star schemas
- Feature tables
- Ready for BI/ML
```

### Data Warehouse Optimization Patterns

**1. Partitioning Strategies:**
- **Time-based:** Most common (daily, monthly)
- **Geography:** Region, country for global systems
- **Hash:** Distribute evenly across nodes
- **List:** Explicit value lists (e.g., product categories)

**2. Clustering:**
- Co-locate related data on disk
- Snowflake: Automatic micro-partitions + clustering keys
- BigQuery: Clustering columns (max 4)
- Redshift: Distribution + sort keys

**3. Materialized Views:**
- Pre-compute expensive aggregations
- Auto-refresh on base table changes
- Trade-off: Storage cost vs query performance

**4. Incremental Loading:**
- Only load new/changed data
- Pattern: Watermark column (last_updated_timestamp)
- Reduces load time 90%+

### Data Lakehouse Implementation

**Apache Iceberg Architecture:**
```
┌─────────────────────────────────────────┐
│ Query Engines (Spark, Trino, Flink)    │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│ Iceberg Metadata Layer                  │
│ - Manifest files (file lists)           │
│ - Manifest lists (snapshots)            │
│ - Metadata.json (table schema)          │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│ Data Files (Parquet/ORC)                │
│ - S3/GCS/ADLS object storage            │
│ - Immutable, partitioned                │
└─────────────────────────────────────────┘
```

**Key Features:**
- **Hidden Partitioning:** Partition evolution without rewriting data
- **Time Travel:** `SELECT * FROM table TIMESTAMP AS OF '2025-01-01'`
- **Schema Evolution:** Add/drop/rename columns without breaking queries
- **ACID:** Serializable isolation for concurrent writes

**Delta Lake Architecture:**
```
┌─────────────────────────────────────────┐
│ Spark/Databricks                        │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│ Delta Transaction Log (_delta_log/)     │
│ - JSON files (ordered, immutable)       │
│ - ACID guarantees                       │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│ Parquet Data Files                      │
│ - S3/ADLS/GCS                           │
│ - Partitioned, versioned                │
└─────────────────────────────────────────┘
```

**Key Features:**
- **ACID Transactions:** Transaction log ensures consistency
- **Time Travel:** `SELECT * FROM table VERSION AS OF 10`
- **MERGE/UPSERT:** Efficient updates and deletes
- **Z-Ordering:** Co-locate related data for performance

---

## Data Mesh Principles

### 1. Domain-Oriented Decentralization

**Traditional (Centralized):**
```
All Domains → Central Data Team → Data Warehouse → Consumers
              (Bottleneck)
```

**Data Mesh (Decentralized):**
```
Sales Domain → Sales Data Product → Consumers
Marketing Domain → Marketing Data Product → Consumers
Product Domain → Product Data Product → Consumers
     ↑
Self-Serve Platform (enables autonomy)
```

**Domain Identification:**
- Bounded contexts (Domain-Driven Design)
- Examples: Sales, Marketing, Product, Support, Finance
- Each domain owns source data and derived analytics

**Domain Data Product Team Structure:**
- Product Owner (business priorities)
- Data Engineers (pipelines, quality)
- Domain Experts (business logic)
- Platform Engineers (infrastructure)

### 2. Data as a Product

**Product Thinking:**
- **Consumers are customers:** Internal data consumers treated like external customers
- **SLA/SLO commitments:** Uptime, freshness, quality guarantees
- **Documentation:** Schema, lineage, use cases
- **Support:** Help channels, onboarding

**Data Product Interface Contract:**
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
    registry: Confluent Schema Registry

  access:
    read: SELECT on sales.orders table
    authentication: OAuth2
    authorization: RBAC (role-based)

  documentation:
    url: https://wiki.company.com/sales-orders
    examples: https://github.com/company/data-products/sales-orders

  lineage:
    source_systems: [Salesforce, Stripe]
    transformations: https://github.com/company/dbt-sales
```

### 3. Self-Serve Data Infrastructure

**Platform Team Responsibilities:**
- Infrastructure as code (Terraform, Pulumi)
- CI/CD pipelines for data products
- Observability (monitoring, alerting, lineage)
- Data catalog (discovery, search)
- Governance tooling (access control, quality checks)

**Self-Serve Capabilities:**
```
Domain Team Can Do (Without Platform Team):
✅ Deploy new data pipeline
✅ Update schema
✅ Monitor data quality
✅ Set up alerts
✅ Publish data product to catalog
✅ Grant access to consumers

Domain Team Cannot Do (Platform Managed):
❌ Modify global security policies
❌ Change infrastructure architecture
❌ Access other domains' raw data (without permission)
```

### 4. Federated Computational Governance

**Global Policies (Centralized):**
- Data classification (PII, confidential, public)
- Retention policies (GDPR right to erasure)
- Security standards (encryption, access controls)
- Compliance (SOC2, HIPAA, GDPR)

**Local Implementation (Decentralized):**
- Domain teams implement policies in their context
- Automated checks enforce compliance
- Central team audits, doesn't execute

**Example: PII Handling Policy**
- **Global Policy:** "All PII must be encrypted at rest and in transit"
- **Domain Implementation:** Sales team encrypts customer email in sales data product
- **Automated Check:** Platform scans for unencrypted PII columns, alerts if found
- **Audit:** Central governance team reviews quarterly

---

## Modern Data Stack Architecture

### Typical Modern Data Stack (2025)

```
┌─────────────────────────────────────────────────────────┐
│ Data Sources                                            │
│ - Databases (PostgreSQL, MySQL, MongoDB)                │
│ - SaaS (Salesforce, Stripe, HubSpot)                   │
│ - Events (Segment, Rudderstack)                         │
│ - Files (S3, GCS, SFTP)                                 │
└─────────────────────┬───────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────┐
│ Ingestion Layer                                         │
│ - Fivetran (ELT, pre-built connectors)                  │
│ - Airbyte (open-source, custom connectors)             │
│ - Kafka (streaming, event-driven)                       │
│ - Apache NiFi (on-premises, complex routing)            │
└─────────────────────┬───────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────┐
│ Storage Layer                                           │
│ - Snowflake (cloud data warehouse)                      │
│ - Databricks (lakehouse, Spark-based)                   │
│ - BigQuery (Google Cloud, serverless)                   │
│ - Redshift (AWS, legacy migration)                      │
└─────────────────────┬───────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────┐
│ Transformation Layer                                    │
│ - dbt (SQL-based, version controlled)                   │
│ - Dataform (Google, SQL + Dataform syntax)             │
│ - Apache Spark (PySpark, large-scale)                   │
└─────────────────────┬───────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────┐
│ Orchestration Layer                                     │
│ - Apache Airflow (most popular, Python DAGs)            │
│ - Dagster (asset-based, modern)                         │
│ - Prefect (Python, dynamic workflows)                   │
│ - dbt Cloud (dbt-specific)                              │
└─────────────────────┬───────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────┐
│ Visualization/BI Layer                                  │
│ - Tableau (enterprise, rich visualizations)             │
│ - Looker (Google, LookML modeling)                      │
│ - Power BI (Microsoft ecosystem)                        │
│ - Metabase (open-source, simple)                        │
└─────────────────────┬───────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────┐
│ Data Governance Layer (Cross-Cutting)                   │
│ - Alation (data catalog, enterprise)                    │
│ - DataHub (LinkedIn, open-source)                       │
│ - Monte Carlo (data observability)                      │
│ - Great Expectations (data quality)                     │
│ - OpenLineage (lineage tracking)                        │
└─────────────────────────────────────────────────────────┘
```

### Tool Selection Criteria

**Ingestion (Fivetran vs Airbyte vs Kafka):**
- **Fivetran:** Pre-built connectors, SaaS, expensive, low maintenance
- **Airbyte:** Open-source, custom connectors, self-hosted or cloud
- **Kafka:** Streaming, event-driven, high throughput, complex setup
- **Use Fivetran when:** Standard sources, budget available, want simplicity
- **Use Airbyte when:** Custom sources, cost-sensitive, engineering resources
- **Use Kafka when:** Real-time streaming, event-driven architecture

**Storage (Snowflake vs Databricks vs BigQuery):**
- **Snowflake:** Best for BI/analytics, strong governance, multi-cloud
- **Databricks:** Best for ML/data science, Spark-native, lakehouse
- **BigQuery:** Best for Google Cloud users, serverless, integrated
- **Use Snowflake when:** BI-primary, need zero-maintenance, multi-cloud
- **Use Databricks when:** ML-primary, Spark expertise, lakehouse pattern
- **Use BigQuery when:** GCP-committed, simple pay-per-query, serverless

**Transformation (dbt vs Spark):**
- **dbt:** SQL-based, version controlled, testing framework, BI-focused
- **Spark:** PySpark/Scala, large-scale processing, ML integration
- **Use dbt when:** Analysts writing transformations, SQL-based, < 100TB
- **Use Spark when:** Data engineers, complex logic, > 100TB, ML workflows

**Orchestration (Airflow vs Dagster vs Prefect):**
- **Airflow:** Most mature, large community, Python DAGs, operational overhead
- **Dagster:** Asset-based (not task-based), modern, strong testing
- **Prefect:** Dynamic workflows, Python-native, easier than Airflow
- **Use Airflow when:** Need mature ecosystem, complex dependencies
- **Use Dagster when:** Asset-oriented thinking, strong software engineering
- **Use Prefect when:** Want simpler than Airflow, dynamic workflows

---

## Medallion Architecture Pattern

### Overview

Medallion architecture is the standard pattern for organizing data in lakehouses (popularized by Databricks). It creates layers of increasing data quality and refinement.

### Three Layers

#### Bronze Layer (Raw Data)
**Purpose:** Exact copy of source systems; historical archive

**Characteristics:**
- **Immutable:** Never modify or delete (append-only)
- **Full fidelity:** All columns, all rows
- **Format:** Source format (JSON, CSV) or Parquet
- **Schema:** Minimal (often just string types)
- **Retention:** Forever (or years)

**Example Table:**
```
bronze.salesforce_accounts (raw)
- _ingested_at: timestamp
- _source_file: string
- _raw_data: string (entire JSON/XML blob)
```

**Use Cases:**
- Reprocess silver/gold without re-ingesting
- Audit original data
- Handle late-arriving data
- Debug data issues

#### Silver Layer (Cleaned & Conformed)
**Purpose:** Validated, deduplicated, typed data

**Characteristics:**
- **Data Quality:** Validated against schema
- **Deduplication:** Remove duplicates
- **Type Conversion:** String → int, date, etc.
- **Normalized:** Consistent naming, formatting
- **Retention:** 1-2 years typical

**Example Transformations:**
```sql
-- Bronze → Silver
CREATE OR REPLACE TABLE silver.accounts AS
SELECT
  -- Parse JSON
  json_extract_scalar(_raw_data, '$.id') AS account_id,
  json_extract_scalar(_raw_data, '$.name') AS account_name,
  -- Type conversion
  CAST(json_extract_scalar(_raw_data, '$.annual_revenue') AS BIGINT) AS annual_revenue,
  -- Date parsing
  DATE(json_extract_scalar(_raw_data, '$.created_date')) AS created_date,
  -- Metadata
  _ingested_at,
  CURRENT_TIMESTAMP() AS _processed_at
FROM bronze.salesforce_accounts
WHERE _ingested_at > (SELECT MAX(_processed_at) FROM silver.accounts) -- Incremental
QUALIFY ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY _ingested_at DESC) = 1; -- Deduplicate
```

**Data Quality Checks (Silver Layer):**
- Primary key uniqueness
- Null checks on required fields
- Referential integrity
- Value range validation
- Format validation (email, phone)

**Use Cases:**
- Source for gold layer
- Data science exploratory analysis
- Joins across multiple sources

#### Gold Layer (Business-Level Aggregates)
**Purpose:** Optimized for consumption (BI, ML, APIs)

**Characteristics:**
- **Business Logic:** Calculated metrics, KPIs
- **Aggregations:** Pre-computed rollups
- **Dimensional Models:** Star schemas
- **Denormalized:** Optimized for query performance
- **Retention:** Based on business need

**Example Transformations:**
```sql
-- Silver → Gold (Star Schema: Fact Table)
CREATE OR REPLACE TABLE gold.fact_sales AS
SELECT
  s.order_id,
  d.date_key,
  c.customer_key,
  p.product_key,
  st.store_key,
  -- Metrics
  s.quantity,
  s.unit_price,
  s.discount_amount,
  s.quantity * s.unit_price AS gross_revenue,
  s.quantity * s.unit_price - s.discount_amount AS net_revenue,
  s.quantity * p.unit_cost AS cost,
  (s.quantity * s.unit_price - s.discount_amount) - (s.quantity * p.unit_cost) AS profit
FROM silver.sales s
JOIN gold.dim_date d ON s.order_date = d.date
JOIN gold.dim_customer c ON s.customer_id = c.customer_id
JOIN gold.dim_product p ON s.product_id = p.product_id
JOIN gold.dim_store st ON s.store_id = st.store_id;
```

**Gold Layer Patterns:**
- **Dimensional (Star/Snowflake):** BI dashboards
- **Wide Tables:** ML feature tables
- **Aggregates:** Summary tables (daily_sales_by_region)
- **OBT (One Big Table):** Fully denormalized for specific use case

**Use Cases:**
- Power BI/Tableau dashboards
- Automated reporting
- ML model training
- External API consumption

### Medallion + Data Mesh

**Pattern:** Each domain owns bronze-silver-gold for their data products

```
Sales Domain:
  bronze.sales_raw
  silver.sales_cleaned
  gold.sales_analytics (data product)

Marketing Domain:
  bronze.marketing_raw
  silver.marketing_cleaned
  gold.marketing_analytics (data product)

Cross-Domain:
  gold.customer_360 (combines sales + marketing silver tables)
```

---

## Data Governance and Cataloging

### Data Catalog

**Purpose:** Searchable inventory of all data assets

**Core Features:**
- **Metadata Management:** Schema, owner, lineage
- **Search & Discovery:** Find tables by name, description, column
- **Tagging:** PII, confidential, deprecated
- **Documentation:** Business glossary, data dictionary
- **Lineage:** Visual graph of data flow

**Tools:**
- **Alation:** Enterprise, AI-powered search, data stewardship
- **Collibra:** Governance-focused, workflows, compliance
- **DataHub (LinkedIn):** Open-source, REST API, extensible
- **AWS Glue Data Catalog:** Native AWS, integrates with Athena
- **Azure Purview:** Native Azure, Microsoft ecosystem

**Example: DataHub Metadata**
```yaml
dataset:
  name: gold.fact_sales
  platform: snowflake

  schema:
    columns:
      - name: customer_key
        type: bigint
        tags: [PII, joins_to_dim_customer]
      - name: net_revenue
        type: decimal(18,2)
        description: Revenue after discounts

  ownership:
    owners: [sales-data-team@company.com]
    domain: sales

  tags: [gold-layer, star-schema, sales-domain]

  documentation:
    url: https://wiki.company.com/gold-fact-sales
    last_updated: 2025-12-01
```

### Data Lineage

**Purpose:** Track data flow from source to consumption

**Benefits:**
- Impact analysis (if I change this table, what breaks?)
- Root cause analysis (where did bad data come from?)
- Compliance (where is PII stored and used?)

**Lineage Tracking Approaches:**

**1. OpenLineage (Standard):**
```
Source (PostgreSQL)
  → Fivetran
  → Bronze Table
  → dbt Model (Silver)
  → dbt Model (Gold)
  → Tableau Dashboard
```

**2. Column-Level Lineage:**
```
customers.email
  → bronze.raw_customers._raw_data['email']
  → silver.customers.email
  → gold.customer_360.email_address
  → Sent to Marketing Tool (GDPR: track PII)
```

**Tools:**
- **OpenLineage:** Open standard, integrations with Airflow, Spark, dbt
- **Marquez:** Reference implementation of OpenLineage
- **DataHub:** Lineage visualization, REST API
- **Atlan:** Modern, collaboration-focused

### Data Quality

**Data Quality Dimensions:**
1. **Accuracy:** Does data reflect reality?
2. **Completeness:** Are required fields populated?
3. **Consistency:** Do related data agree?
4. **Timeliness:** Is data fresh enough?
5. **Validity:** Does data conform to schema/rules?
6. **Uniqueness:** Are there unwanted duplicates?

**Tools:**

**Great Expectations:**
```python
import great_expectations as gx

# Define expectations
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name="silver_customers_suite"
)

# Expectations
validator.expect_column_values_to_not_be_null("customer_id")
validator.expect_column_values_to_be_unique("customer_id")
validator.expect_column_values_to_match_regex("email", r'^[\w\.-]+@[\w\.-]+\.\w+$')
validator.expect_column_values_to_be_between("annual_revenue", min_value=0, max_value=1e12)

# Run validation
results = validator.validate()
```

**Soda Core:**
```yaml
# checks.yml
checks for silver.customers:
  - row_count > 1000
  - missing_count(customer_id) = 0
  - duplicate_count(customer_id) = 0
  - invalid_percent(email) < 1%:
      valid format: email
  - freshness(created_at) < 1h
```

**dbt Tests:**
```yaml
# models/silver/customers.yml
version: 2
models:
  - name: customers
    columns:
      - name: customer_id
        tests:
          - unique
          - not_null
      - name: email
        tests:
          - not_null
      - name: created_at
        tests:
          - dbt_utils.at_least_one
```

**Data Quality in Medallion:**
- **Bronze → Silver:** Schema validation, type checks
- **Silver → Gold:** Business rule validation, referential integrity
- **Gold:** Anomaly detection, statistical checks

### Access Control

**Patterns:**

**1. Role-Based Access Control (RBAC):**
```sql
-- Snowflake example
CREATE ROLE sales_analyst;
GRANT SELECT ON gold.fact_sales TO ROLE sales_analyst;
GRANT SELECT ON gold.dim_customer TO ROLE sales_analyst;
GRANT ROLE sales_analyst TO USER alice@company.com;
```

**2. Attribute-Based Access Control (ABAC):**
```sql
-- Row-level security (Snowflake)
CREATE OR REPLACE ROW ACCESS POLICY customers_region_policy
AS (region string) RETURNS BOOLEAN ->
  CASE
    WHEN IS_ROLE_IN_SESSION('GLOBAL_ADMIN') THEN TRUE
    WHEN IS_ROLE_IN_SESSION('US_ANALYST') AND region = 'US' THEN TRUE
    WHEN IS_ROLE_IN_SESSION('EU_ANALYST') AND region = 'EU' THEN TRUE
    ELSE FALSE
  END;

ALTER TABLE gold.customers
  ADD ROW ACCESS POLICY customers_region_policy ON (region);
```

**3. Column-Level Security:**
```sql
-- Dynamic Data Masking (Snowflake)
CREATE OR REPLACE MASKING POLICY mask_email AS (val string) RETURNS string ->
  CASE
    WHEN IS_ROLE_IN_SESSION('PII_VIEWER') THEN val
    ELSE '***MASKED***'
  END;

ALTER TABLE gold.customers
  MODIFY COLUMN email SET MASKING POLICY mask_email;
```

---

## Tool Recommendations

### Research-Validated Tools

Based on Context7 research (December 2025), the following tools have high trust scores and extensive documentation:

#### 1. dbt (Data Build Tool)
**Context7 Score:** 87.0 (Excellent)
**Code Snippets:** 3,532
**Reputation:** High

**Use Cases:**
- SQL-based transformations in warehouse
- Version control for data pipelines
- Testing and documentation
- Lineage tracking

**Why Recommended:**
- Industry standard (majority of modern data teams use dbt)
- Strong software engineering practices (Git, CI/CD, testing)
- Extensive package ecosystem (dbt-utils, dbt-expectations, etc.)
- Multi-warehouse support (Snowflake, BigQuery, Redshift, Databricks)

**Getting Started:**
```bash
pip install dbt-snowflake
dbt init my_project
cd my_project

# models/staging/stg_customers.sql
SELECT
  customer_id,
  UPPER(customer_name) AS customer_name,
  email
FROM {{ source('raw', 'customers') }}

dbt run
dbt test
```

#### 2. Apache Iceberg
**Context7 Score:** 79.7 (Strong)
**Code Snippets:** 832
**Reputation:** High

**Use Cases:**
- Open table format for data lakehouses
- Multi-engine analytics (Spark, Trino, Flink, Presto)
- ACID transactions on object storage
- Schema evolution without rewrites

**Why Recommended:**
- Vendor-neutral (Apache Foundation)
- Best multi-engine support (not tied to Databricks/Snowflake)
- Hidden partitioning (partition evolution without rewriting data)
- Production-ready (Netflix, Apple, Adobe in production)

**Ecosystem:**
- **Apache Polaris:** Open-source Iceberg catalog (1,224 snippets, High reputation)
- **Project Nessie:** Git-like versioning for Iceberg (356 snippets, High reputation)

#### 3. Snowflake
**Status:** No Context7 data (proprietary), but industry-leading data warehouse

**Use Cases:**
- Cloud data warehouse (BI/analytics primary)
- Multi-cloud (AWS, GCP, Azure)
- Zero-maintenance (fully managed)
- Strong governance (RBAC, masking, row-level security)

**Why Recommended:**
- Market leader in cloud data warehousing
- Best for BI/reporting workloads
- Separation of storage and compute
- Extensive connector ecosystem (Fivetran, dbt, Tableau)

#### 4. Databricks
**Status:** No Context7 data, but leading lakehouse platform

**Use Cases:**
- Lakehouse platform (BI + ML)
- Spark-based processing
- Delta Lake (ACID on data lake)
- ML and data science workflows

**Why Recommended:**
- Best for ML/data science teams
- Unified analytics platform
- Excellent notebook experience
- Photon engine (fast SQL queries)

#### 5. Fivetran
**Status:** No Context7 data, but leading ELT platform

**Use Cases:**
- Automated data ingestion
- 300+ pre-built connectors
- SaaS tools (Salesforce, HubSpot, Stripe)
- Cloud databases (PostgreSQL, MySQL, MongoDB)

**Why Recommended:**
- Simplest ingestion solution
- Minimal engineering effort
- Auto-schema change detection
- Strong reliability (retries, monitoring)

**Alternative (Open-Source):** Airbyte (cost-sensitive, custom connectors)

#### 6. Apache Airflow
**Status:** Industry-standard orchestration

**Use Cases:**
- Workflow orchestration
- Complex dependencies (DAGs)
- Scheduling and monitoring
- Python-based workflows

**Why Recommended:**
- Most mature orchestration platform
- Large community and ecosystem
- Integrations with every data tool
- Battle-tested at scale

**Alternatives:**
- **Dagster:** Asset-based, modern (better for data products)
- **Prefect:** Simpler than Airflow, dynamic workflows

#### 7. Great Expectations
**Status:** De-facto standard for data quality

**Use Cases:**
- Data validation and testing
- Data profiling
- Automated documentation
- CI/CD integration

**Why Recommended:**
- Comprehensive expectation library
- Integrates with dbt, Airflow, Spark
- Human-readable reports
- Open-source, active community

**Alternative:** Soda Core (simpler YAML-based checks)

#### 8. DataHub (LinkedIn)
**Status:** Leading open-source data catalog

**Use Cases:**
- Data discovery and cataloging
- Metadata management
- Lineage visualization
- Data governance

**Why Recommended:**
- Open-source (avoid vendor lock-in)
- REST API and GraphQL
- Integrates with dbt, Airflow, Spark, Kafka
- Active community

**Alternatives:**
- **Alation:** Enterprise, AI-powered search
- **Collibra:** Governance-focused, compliance workflows

### Tool Stack Recommendations by Use Case

**Startup (Cost-Optimized, Simple):**
- **Storage:** BigQuery or Snowflake (pay-per-use)
- **Ingestion:** Airbyte (open-source)
- **Transformation:** dbt
- **Orchestration:** dbt Cloud or Prefect
- **Visualization:** Metabase (open-source) or Looker Studio (free)

**Growth Company (Balanced):**
- **Storage:** Snowflake (BI-focused) or Databricks (ML-focused)
- **Ingestion:** Fivetran (convenience) + Kafka (real-time)
- **Transformation:** dbt
- **Orchestration:** Airflow (Astronomer or MWAA)
- **Visualization:** Tableau or Looker
- **Catalog:** DataHub

**Enterprise (Full Stack):**
- **Storage:** Snowflake (BI) + Databricks (ML) hybrid
- **Ingestion:** Fivetran + Custom Airflow DAGs + Kafka
- **Transformation:** dbt + Spark (for heavy processing)
- **Orchestration:** Airflow
- **Visualization:** Tableau (enterprise license)
- **Catalog:** Alation or Collibra
- **Observability:** Monte Carlo
- **Quality:** Great Expectations + Soda

---

## Skill Structure Design

### Proposed SKILL.md Structure

**Target Length:** 800-1,200 lines (High Level skill)

**Structure:**

```markdown
---
name: data-architecture
description: Strategic guidance for designing modern data platforms, covering storage paradigms (data lake, warehouse, lakehouse), modeling approaches (dimensional, normalized, data vault, wide tables), data mesh principles, and medallion architecture patterns. Use when architecting data platforms, choosing between centralized vs decentralized patterns, selecting table formats (Iceberg, Delta Lake), or designing data governance frameworks.
---

## Purpose

Guide architects and platform engineers through strategic data architecture decisions for modern cloud-native data platforms.

## When to Use This Skill

- Designing a new data platform or modernizing legacy systems
- Choosing between data lake, data warehouse, or data lakehouse
- Deciding on dimensional, normalized, data vault, or wide table modeling
- Evaluating centralized vs data mesh architecture
- Selecting open table formats (Iceberg, Delta Lake, Hudi)
- Designing medallion architecture (bronze, silver, gold layers)
- Implementing data governance and cataloging

## Core Concepts

### 1. Storage Paradigms
- Data Lake, Data Warehouse, Data Lakehouse comparison
- Decision framework: When to use which
- Reference: [storage-paradigms.md](reference/storage-paradigms.md)

### 2. Data Modeling Approaches
- Dimensional (star/snowflake)
- Normalized (3NF)
- Data Vault 2.0
- Wide tables (denormalized)
- Reference: [modeling-approaches.md](reference/modeling-approaches.md)

### 3. Data Mesh
- Four principles: Domain-oriented, Data as Product, Self-serve, Federated Governance
- Readiness assessment
- Reference: [data-mesh-guide.md](reference/data-mesh-guide.md)

### 4. Modern Data Stack
- Tool categories: Ingestion, Storage, Transformation, Orchestration, Visualization
- Reference: [modern-data-stack.md](reference/modern-data-stack.md)

### 5. Medallion Architecture
- Bronze (raw), Silver (cleaned), Gold (business-level)
- Reference: [medallion-pattern.md](reference/medallion-pattern.md)

### 6. Data Governance
- Catalog, lineage, quality, access control
- Reference: [governance-patterns.md](reference/governance-patterns.md)

## Decision Frameworks

### Framework 1: Storage Paradigm Selection
Reference: [decision-frameworks.md](reference/decision-frameworks.md#storage-paradigm)

Quick Guide:
- BI/Reporting only + Known queries → Data Warehouse
- ML/AI primary + Raw data needed → Data Lake or Lakehouse
- Mixed BI + ML + Cost optimization → Data Lakehouse
- Exploratory/Unknown use cases → Data Lake

### Framework 2: Data Modeling Approach
Reference: [decision-frameworks.md](reference/decision-frameworks.md#modeling-approach)

Quick Guide:
- Analytical (BI) + Known queries → Dimensional (Star Schema)
- Transactional (OLTP) → Normalized (3NF)
- Compliance/Audit required → Data Vault 2.0
- Data Science/ML → Wide Tables

### Framework 3: Data Mesh Readiness
Reference: [decision-frameworks.md](reference/decision-frameworks.md#data-mesh-readiness)

Quick Assessment:
- Large org (>500 people) + Clear domains + Central bottleneck → Data Mesh
- Small org or unclear ownership → Centralized

### Framework 4: Table Format Selection
Reference: [decision-frameworks.md](reference/decision-frameworks.md#table-format)

Quick Guide:
- Multi-engine flexibility → Apache Iceberg
- Databricks ecosystem → Delta Lake
- Frequent upserts/CDC → Apache Hudi

## Implementation Patterns

### Pattern 1: Medallion Architecture
Reference: [medallion-pattern.md](reference/medallion-pattern.md)

```
Bronze (Raw) → Silver (Cleaned) → Gold (Business)
```

### Pattern 2: Data Mesh with Lakehouse
Reference: [data-mesh-guide.md](reference/data-mesh-guide.md#lakehouse-implementation)

Each domain owns bronze-silver-gold for their data products.

### Pattern 3: Data Quality in Pipelines
Reference: [governance-patterns.md](reference/governance-patterns.md#data-quality)

Tools: Great Expectations, Soda, dbt tests

## Tool Recommendations

Reference: [tool-recommendations.md](reference/tool-recommendations.md)

**Production-Ready (High Trust Scores):**
- dbt (Context7: 87.0, 3,532 snippets) - Transformation
- Apache Iceberg (Context7: 79.7, 832 snippets) - Table format
- Snowflake - Data warehouse (BI-focused)
- Databricks - Lakehouse (ML-focused)

## Common Scenarios

### Scenario 1: Startup Data Platform
Reference: [scenarios.md](reference/scenarios.md#startup)

Recommendation: BigQuery + Airbyte + dbt + dbt Cloud

### Scenario 2: Enterprise Modernization
Reference: [scenarios.md](reference/scenarios.md#enterprise)

Recommendation: Hybrid (Snowflake for BI, Databricks for ML) + Medallion

### Scenario 3: Data Mesh Implementation
Reference: [scenarios.md](reference/scenarios.md#data-mesh)

Recommendation: Domain-owned data products on shared lakehouse platform

## Integration with Other Skills

- **ingesting-data**: ETL/ELT mechanics, Fivetran, Airbyte
- **data-transformation**: dbt, Dataform implementation details
- **streaming-data**: Kafka, Flink for real-time ingestion
- **databases-relational**: PostgreSQL, MySQL as sources
- **databases-document**: MongoDB, DynamoDB as sources
- **ai-data-engineering**: Feature stores, ML pipelines
- **designing-distributed-systems**: CAP theorem, consistency models
- **observability**: Monitoring data pipelines

## Best Practices

1. **Start simple:** Don't over-engineer; begin with data warehouse or basic lakehouse
2. **Invest in governance early:** Catalog, lineage, quality from day one
3. **Medallion architecture:** Use bronze-silver-gold pattern for clear data quality layers
4. **Open table formats:** Prefer Iceberg or Delta Lake to avoid vendor lock-in
5. **Data mesh maturity:** Don't rush; assess readiness before decentralizing
6. **Automate quality:** Integrate data tests into CI/CD pipelines
7. **Monitor and alert:** Observability is critical for data pipelines
8. **Document as code:** Use dbt docs, DataHub, YAML for documentation

## Anti-Patterns

❌ **Data swamp:** Data lake without governance or cataloging
❌ **Premature data mesh:** Implementing data mesh before org readiness
❌ **Tool sprawl:** Too many tools; prefer fewer, well-integrated tools
❌ **Ignoring data quality:** No tests or validation; "garbage in, garbage out"
❌ **Centralized bottleneck:** Single team owning all data in large org
❌ **Vendor lock-in:** Proprietary formats without migration path
❌ **No lineage:** Can't answer "where did this data come from?"

## Further Reading

- Reference files (8 total): [reference/](reference/)
- Tool recommendations: [tool-recommendations.md](reference/tool-recommendations.md)
- Decision frameworks: [decision-frameworks.md](reference/decision-frameworks.md)
- Common scenarios: [scenarios.md](reference/scenarios.md)
```

### Proposed Bundled Resources

**reference/ directory (8 files):**
1. **storage-paradigms.md** - Deep dive on lake vs warehouse vs lakehouse
2. **modeling-approaches.md** - Dimensional, normalized, data vault, wide tables
3. **data-mesh-guide.md** - Data mesh principles and implementation
4. **modern-data-stack.md** - Tool categories and selection
5. **medallion-pattern.md** - Bronze, silver, gold layer patterns
6. **governance-patterns.md** - Catalog, lineage, quality, access control
7. **decision-frameworks.md** - All 4 decision frameworks in detail
8. **tool-recommendations.md** - dbt, Iceberg, Snowflake, Databricks details
9. **scenarios.md** - Startup, growth, enterprise, data mesh scenarios

**scripts/ directory (optional):**
- None required for this strategic skill (no code generation)

**examples/ directory (optional):**
1. **dbt-project-structure/** - Example dbt project with bronze/silver/gold models
2. **iceberg-table-creation.sql** - SQL examples for Iceberg tables
3. **great-expectations-suite.py** - Data quality expectations examples
4. **data-mesh-contract.yaml** - Example data product contract

**assets/ directory (optional):**
1. **architecture-diagrams/** - ASCII diagrams of lake/warehouse/lakehouse/mesh
2. **decision-tree-flowcharts/** - Visual flowcharts for decision frameworks

---

## Integration Points

### Related Skills

**Direct Dependencies:**
- **ingesting-data**: Covers ETL/ELT mechanics, Fivetran, Airbyte implementation
- **data-transformation**: dbt and Dataform detailed implementation
- **streaming-data**: Kafka, Flink for real-time data pipelines

**Complementary Skills:**
- **databases-relational**: PostgreSQL, MySQL as source systems
- **databases-document**: MongoDB, DynamoDB as sources
- **databases-timeseries**: InfluxDB, TimescaleDB for metrics
- **databases-vector**: Pinecone, Weaviate for AI/ML embeddings
- **ai-data-engineering**: Feature stores, ML training pipelines
- **designing-distributed-systems**: CAP theorem, consistency models applied to data systems
- **observability**: Monitoring data pipeline health, data quality metrics

**Downstream Skills:**
- **visualizing-data**: BI and dashboard patterns consuming data warehouse
- **creating-dashboards**: Dashboard design patterns
- **sql-optimization**: Query performance tuning in data warehouse

### Cross-Skill Patterns

**Pattern 1: Data Platform for AI/ML**
```
data-architecture (lakehouse design)
  → ingesting-data (Kafka streaming)
  → data-transformation (dbt feature engineering)
  → ai-data-engineering (feature store)
  → model-serving (ML models)
```

**Pattern 2: End-to-End Analytics**
```
data-architecture (warehouse design)
  → ingesting-data (Fivetran connectors)
  → data-transformation (dbt models)
  → visualizing-data (Tableau dashboards)
```

**Pattern 3: Real-Time Data Pipeline**
```
streaming-data (Kafka topics)
  → data-architecture (lakehouse ingestion)
  → data-transformation (Flink streaming)
  → databases-timeseries (metrics storage)
  → observability (monitoring dashboards)
```

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
**Goal:** Establish core architectural concepts

**Tasks:**
1. ✅ Complete research (Google Search, Context7)
2. ✅ Write init.md (this document)
3. Create SKILL.md (800-1,200 lines)
4. Write core reference files:
   - storage-paradigms.md
   - modeling-approaches.md
   - decision-frameworks.md

**Success Criteria:**
- SKILL.md under 1,200 lines
- 3 core reference files complete
- Decision frameworks actionable

### Phase 2: Depth (Weeks 3-4)
**Goal:** Add comprehensive guidance

**Tasks:**
1. Write remaining reference files:
   - data-mesh-guide.md
   - modern-data-stack.md
   - medallion-pattern.md
   - governance-patterns.md
   - tool-recommendations.md
   - scenarios.md
2. Create examples:
   - dbt project structure
   - Iceberg table creation SQL
   - Great Expectations suite

**Success Criteria:**
- All 9 reference files complete
- 3+ working code examples
- Real-world scenarios covered

### Phase 3: Validation (Week 5)
**Goal:** Test and refine

**Tasks:**
1. Create evaluation scenarios:
   - "Design a data platform for a startup"
   - "Should we use data mesh for our 200-person company?"
   - "Choose between Iceberg and Delta Lake for our lakehouse"
   - "Design medallion architecture for sales analytics"
2. Test with Claude (no skill) → baseline
3. Test with Claude (with skill) → measure improvement
4. Refine based on results

**Success Criteria:**
- 5+ evaluation scenarios
- Skill demonstrates clear value over baseline
- Decision frameworks lead to correct recommendations

### Phase 4: Integration (Week 6)
**Goal:** Connect to related skills

**Tasks:**
1. Cross-reference with:
   - ingesting-data
   - data-transformation
   - streaming-data
   - ai-data-engineering
2. Update SKILL.md with integration guidance
3. Create cross-skill examples

**Success Criteria:**
- Clear boundaries between this skill and related skills
- Integration patterns documented
- Users know when to switch skills

### Phase 5: Polish (Week 7)
**Goal:** Production-ready

**Tasks:**
1. Review for conciseness (remove Claude's existing knowledge)
2. Ensure consistent terminology
3. Validate all tool recommendations
4. Add ASCII diagrams for clarity
5. Final testing across Haiku, Sonnet, Opus

**Success Criteria:**
- SKILL.md < 1,200 lines (ideally ~1,000)
- All examples tested and working
- Consistent voice (imperative/infinitive, not second-person)
- Validated with multiple models

---

## Evaluation Criteria

### Test Scenarios (for Phase 3)

**Scenario 1: Startup Data Platform Design**
- **User Query:** "We're a 50-person startup with PostgreSQL, MongoDB, and Stripe data. We need analytics for the CEO dashboard and want to start ML experiments. Design our data platform."
- **Expected Outcome:** Recommend BigQuery/Snowflake (simplicity), Airbyte (cost-effective ingestion), dbt (transformation), dbt Cloud (orchestration), Looker/Metabase (viz). Explain medallion architecture. Mention data lakehouse if ML becomes priority.

**Scenario 2: Data Mesh Readiness**
- **User Query:** "We're a 200-person company with centralized data team (5 people). Should we adopt data mesh? We have sales, marketing, and product domains."
- **Expected Outcome:** Use readiness assessment framework. Likely answer: NO, not yet. Central team is small (not a bottleneck yet). Recommend improving platform and governance first. Consider data mesh at 500+ people or when central team is clearly a bottleneck.

**Scenario 3: Table Format Selection**
- **User Query:** "We're building a lakehouse on S3. We need Spark for ML and Trino for BI queries. Should we use Iceberg or Delta Lake?"
- **Expected Outcome:** Recommend Apache Iceberg (multi-engine support, vendor-neutral). Delta Lake is Databricks-centric, less optimal for Trino. Mention Iceberg's hidden partitioning and partition evolution as advantages.

**Scenario 4: Medallion Architecture**
- **User Query:** "Explain how to structure our data lake for sales analytics. We have raw Salesforce and Stripe data."
- **Expected Outcome:** Propose medallion architecture. Bronze: raw JSON from Salesforce/Stripe. Silver: parsed, typed, deduplicated. Gold: star schema with fact_sales and dimensions (dim_date, dim_customer, dim_product). Include data quality checks at each layer.

**Scenario 5: Enterprise Modernization**
- **User Query:** "We have a legacy Oracle data warehouse. We want to modernize to cloud, support both BI and ML, and reduce costs. What architecture?"
- **Expected Outcome:** Recommend data lakehouse (Databricks or Snowflake with Iceberg). Migrate incrementally: Keep Oracle for critical BI short-term, build lakehouse for new workloads and ML. Use CDC tools (Debezium, Fivetran) for migration. Implement medallion architecture. Estimate 60-80% cost reduction with lake storage.

### Success Metrics

**Quantitative:**
- Skill reduces decision time by >50% (measured via evaluation response length)
- Recommendations align with industry best practices (validated against research)
- Users reach correct decision in <5 minutes of interaction

**Qualitative:**
- Users understand trade-offs (not just tool names)
- Recommendations are context-aware (startup vs enterprise)
- Users avoid common anti-patterns (data swamp, premature mesh)

---

## Open Questions and Future Work

### Open Questions

1. **Streaming Integration:** How deep should we cover Kafka, Flink in this skill vs defer to `streaming-data`?
   - **Decision:** Cover high-level (streaming as ingestion layer), defer implementation to `streaming-data`

2. **ML Feature Stores:** Include detailed feature store patterns or defer to `ai-data-engineering`?
   - **Decision:** Cover wide tables for ML, defer feature store specifics

3. **Cloud Provider Specifics:** How much AWS/GCP/Azure specifics to include?
   - **Decision:** Tool-agnostic patterns, mention cloud services but don't detail operations

4. **Data Vault Depth:** Data Vault 2.0 is complex; how much detail?
   - **Decision:** Cover core concepts (hubs, links, satellites), link to external resources for full implementation

### Future Enhancements

**Version 2.0 (Potential):**
- **Real-Time OLAP:** Apache Pinot, ClickHouse, Druid patterns
- **Multi-Cloud Architectures:** Data replication across AWS/GCP/Azure
- **Data Marketplace:** Internal data product marketplaces
- **Reverse ETL:** Pushing warehouse data back to operational systems
- **Data Contracts:** Schema enforcement across teams
- **Column-Level Lineage:** Advanced lineage tracking
- **Privacy Engineering:** Differential privacy, k-anonymity in data platforms

**Monitoring and Updates:**
- **Quarterly Tool Review:** Validate tool recommendations (new tools, deprecated tools)
- **Research Refresh:** Update Context7 scores, benchmark data
- **Community Feedback:** Gather feedback from users, refine frameworks

---

## Appendix: Research Sources

### Google Search Grounding (December 2025)

**Query 1: "data architecture patterns 2025"**
- Sources: datadecoded.com, datacrossroads.nl, dataversity.net, medium.com, daffodilsw.com
- Key Insights: Cloud-native, layered ecosystem, data lakehouse, modular design

**Query 2: "data mesh vs data lakehouse comparison"**
- Sources: atlan.com, ibm.com, hpe.com, google.com, databricks.com, amazon.com, getdbt.com, wikipedia.org
- Key Insights: Complementary (not exclusive), organizational vs technical, use cases

**Query 3: "modern data stack components dbt Fivetran Snowflake"**
- Sources: medium.com, nexla.com, phdata.io, hevodata.com
- Key Insights: Standard stack (Fivetran → Snowflake → dbt → BI tools)

**Query 4: "dimensional modeling star schema best practices"**
- Sources: owox.com, ghcollaborate.com, microsoft.com, swiftorial.com
- Key Insights: Grain, denormalization, indexing, incremental refresh

### Context7 Library Research (December 2025)

**dbt (/websites/getdbt):**
- Benchmark: 87.0, Snippets: 3,532, Reputation: High
- Packages: dbt-core, dbt-utils, dbt-databricks, dbt-expectations

**Apache Iceberg (/apache/iceberg):**
- Benchmark: 79.7, Snippets: 832, Reputation: High
- Ecosystem: Apache Polaris, Project Nessie, Lakekeeper

**Delta Lake:**
- Research incomplete (connection errors)
- Recommendation: Validate via Databricks documentation

---

## Document History

- **December 3, 2025:** Initial creation (research and planning phase)
- **Version:** 0.1.0 (init.md complete, SKILL.md pending)
- **Word Count:** ~12,500 words (~1,042 lines at 12 words/line average)
- **Status:** Ready for Phase 1 implementation (SKILL.md creation)

---

**Next Steps:**
1. Review and approve init.md structure
2. Begin SKILL.md creation (Phase 1)
3. Create core reference files (storage-paradigms.md, modeling-approaches.md, decision-frameworks.md)
4. Develop evaluation scenarios

**Note:** This init.md follows the established pattern from `designing-distributed-systems` and other High Level skills, targeting 800-1,200 lines with comprehensive research, decision frameworks, and clear implementation roadmap.
