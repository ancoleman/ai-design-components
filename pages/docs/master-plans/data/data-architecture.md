---
sidebar_position: 1
---

# Data Architecture

Master plan for designing scalable, maintainable data models and architecture patterns. Covers schema design, normalization strategies, data modeling techniques, and architectural patterns for databases and data warehouses.

## Key Topics

- **Database Schema Design**: Normalization (1NF-5NF), denormalization strategies, and trade-offs
- **Data Modeling Patterns**: Star schema, snowflake schema, data vault, and dimensional modeling
- **Entity-Relationship Design**: ER diagrams, cardinality, referential integrity, and constraints
- **Data Warehouse Architecture**: Kimball vs. Inmon methodologies, staging layers, and data marts
- **NoSQL Data Models**: Document, key-value, column-family, and graph database patterns
- **Data Partitioning**: Horizontal/vertical partitioning, sharding strategies, and distribution keys
- **Temporal Data Handling**: Slowly changing dimensions (SCD Types 1-6), temporal tables, and audit trails
- **Data Governance**: Metadata management, data lineage, and data catalog integration
- **Schema Evolution**: Migration strategies, backward compatibility, and versioning
- **Multi-Tenancy Patterns**: Shared schema, separate schema, and separate database approaches

## Primary Tools & Technologies

**Relational Databases:**
- PostgreSQL, MySQL, SQL Server, Oracle
- Schema design tools (dbdiagram.io, Lucidchart, ERD Plus)

**Data Warehouses:**
- Snowflake, BigQuery, Redshift, Databricks SQL
- dbt (data build tool) for modeling and transformations

**NoSQL Databases:**
- MongoDB (document), Redis (key-value), Cassandra (column-family), Neo4j (graph)

**Modeling Tools:**
- ERwin, PowerDesigner, ER/Studio
- Apache Atlas (metadata and governance)

**Documentation:**
- dbt docs, Dataedo, Collibra, Alation

## Integration Points

**Upstream Dependencies:**
- **Application Architecture**: Domain-driven design informing data model boundaries
- **API Design**: Data models aligned with API contracts and versioning

**Downstream Consumers:**
- **Data Transformation**: ETL/ELT pipelines consuming modeled data structures
- **SQL Optimization**: Query patterns influenced by schema design choices
- **Streaming Data**: Event schema design for real-time data flows
- **Performance Engineering**: Indexing and partitioning strategies

**Cross-Functional:**
- **Security**: Data classification, encryption at rest, and access control
- **Secret Management**: Connection string and credential handling
- **Documentation**: Auto-generated data dictionaries and lineage diagrams

## Status

**Master Plan Available** - Comprehensive guidance for data architecture and modeling patterns, covering relational, NoSQL, and data warehouse design strategies.

---

*Part of the Data Engineering skill collection focused on building robust, scalable data foundations.*
