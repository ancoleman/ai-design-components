# Open Table Formats Comparison

Quick comparison of Apache Iceberg, Delta Lake, and Apache Hudi for lakehouse architectures.

## Feature Matrix

| Feature | Apache Iceberg | Delta Lake | Apache Hudi |
|---------|---------------|------------|-------------|
| **ACID Transactions** | Yes (serializable) | Yes | Yes |
| **Time Travel** | Yes (snapshot ID) | Yes (version number) | Yes (commit time) |
| **Schema Evolution** | Excellent | Good | Good |
| **Partition Evolution** | Yes (no rewrite) | No | Limited |
| **Hidden Partitioning** | Yes | No | No |
| **Multi-Engine Support** | Spark, Trino, Flink, Presto, Dremio | Spark (primary), Trino (limited) | Spark, Flink |
| **Governance** | Apache Foundation | Databricks/Linux Foundation | Apache Foundation |
| **CDC Support** | Good | Excellent | Excellent |
| **Streaming** | Good | Excellent | Excellent |

## Decision Matrix

**Use Apache Iceberg when:**
- Need multi-engine flexibility (Spark, Trino, Flink)
- Want vendor neutrality (Apache Foundation)
- Partition evolution required
- Future-proof architecture (broadest adoption)

**Use Delta Lake when:**
- Committed to Databricks ecosystem
- Primarily Spark-based workflows
- Excellent streaming + CDC support needed
- Unity Catalog integration desired

**Use Apache Hudi when:**
- CDC and upserts are primary workload
- Streaming ingestion dominant
- Need record-level updates (Merge-on-Read)
- Cost-optimized incremental processing

## Recommendation

**Default:** Apache Iceberg (vendor-neutral, multi-engine, best long-term)
