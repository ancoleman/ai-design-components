# Index Types by Database

Quick reference guide to index types across PostgreSQL, MySQL, and SQL Server.

## PostgreSQL Index Types

| Index Type | Use Case | Operators Supported | Creation |
|-----------|----------|-------------------|----------|
| **B-tree** | General-purpose (default) | <, ≤, =, ≥, >, BETWEEN, IN, IS NULL | `CREATE INDEX ON table (column)` |
| **Hash** | Equality only | = | `CREATE INDEX ON table USING HASH (column)` |
| **GIN** | Full-text, JSONB, arrays | @>, ?, ?&, ?|, @@ | `CREATE INDEX ON table USING GIN (column)` |
| **GiST** | Spatial, ranges, full-text | &&, <->, @>, <<, &< | `CREATE INDEX ON table USING GIST (column)` |
| **SP-GiST** | Non-balanced trees, partitioned | Same as GiST | `CREATE INDEX ON table USING SPGIST (column)` |
| **BRIN** | Large sequential tables | <, ≤, =, ≥, > | `CREATE INDEX ON table USING BRIN (column)` |
| **Bloom** | Multi-column equality | = (multiple columns) | `CREATE INDEX ON table USING BLOOM (col1, col2, ...)` |

**Recommendations:**
- **Default:** B-tree (99% of use cases)
- **Full-text:** GIN on `tsvector`
- **JSONB:** GIN
- **Spatial:** GiST
- **Time-series >100GB:** BRIN

## MySQL Index Types

| Index Type | Use Case | Storage Engines | Creation |
|-----------|----------|----------------|----------|
| **B-tree** | General-purpose (default) | InnoDB, MyISAM | `CREATE INDEX ON table (column)` |
| **Hash** | Equality only | MEMORY engine only | `CREATE INDEX USING HASH ON table (column)` |
| **Full-text** | Text search | InnoDB (5.6+), MyISAM | `CREATE FULLTEXT INDEX ON table (column)` |
| **Spatial** | Geometric data | InnoDB (5.7+), MyISAM | `CREATE SPATIAL INDEX ON table (column)` |

**Recommendations:**
- **Default:** B-tree
- **Text search:** Full-text index
- **Spatial:** Spatial index

## SQL Server Index Types

| Index Type | Use Case | Clustered | Creation |
|-----------|----------|-----------|----------|
| **Clustered** | Primary table organization | Yes (1 per table) | `CREATE CLUSTERED INDEX ON table (column)` |
| **Non-Clustered** | Secondary lookups | No (multiple per table) | `CREATE NONCLUSTERED INDEX ON table (column)` |
| **Covering (INCLUDE)** | Index-only scans | No | `CREATE INDEX ON table (col) INCLUDE (col2, ...)` |
| **Filtered** | Partial index | No | `CREATE INDEX ON table (col) WHERE condition` |
| **Columnstore** | Analytics/DW | Yes or No | `CREATE COLUMNSTORE INDEX ON table` |
| **Full-text** | Text search | No | `CREATE FULLTEXT INDEX ON table (column)` |
| **Spatial** | Geometric data | No | `CREATE SPATIAL INDEX ON table (column)` |
| **XML** | XML data | No | `CREATE XML INDEX ON table (column)` |

**Recommendations:**
- **Primary key:** Clustered index (default)
- **Foreign keys:** Non-clustered index
- **Frequent queries:** Covering index
- **Analytics:** Columnstore index

## Cross-Database Index Comparison

### General-Purpose Indexes

| Database | Name | Notes |
|----------|------|-------|
| PostgreSQL | B-tree | Default, most common |
| MySQL | B-tree | InnoDB uses clustered primary key |
| SQL Server | Non-Clustered | Separate from table data |

### Full-Text Search

| Database | Implementation | Query Syntax |
|----------|---------------|--------------|
| PostgreSQL | GIN + tsvector | `to_tsvector() @@ to_tsquery()` |
| MySQL | Full-text index | `MATCH() AGAINST()` |
| SQL Server | Full-text index | `CONTAINS()`, `FREETEXT()` |

### Partial/Filtered Indexes

| Database | Support | Syntax |
|----------|---------|--------|
| PostgreSQL | Yes (Partial Index) | `CREATE INDEX ... WHERE condition` |
| MySQL | No | Use generated columns as workaround |
| SQL Server | Yes (Filtered Index) | `CREATE INDEX ... WHERE condition` |

### Expression/Computed Indexes

| Database | Support | Syntax |
|----------|---------|--------|
| PostgreSQL | Yes (Expression Index) | `CREATE INDEX ON table (LOWER(column))` |
| MySQL | Via Generated Columns | `ADD COLUMN ... GENERATED ... + INDEX` |
| SQL Server | Via Computed Columns | `ADD COLUMN ... AS expression + INDEX` |

### Covering Indexes

| Database | Implementation | Syntax |
|----------|---------------|--------|
| PostgreSQL | INCLUDE clause | `CREATE INDEX ON t (col) INCLUDE (col2, col3)` |
| MySQL | Add columns to index | `CREATE INDEX ON t (col, col2, col3)` |
| SQL Server | INCLUDE clause | `CREATE INDEX ON t (col) INCLUDE (col2, col3)` |

## Index Selection Decision Tree

```
What type of query?
├─ Equality (column = value)
│  ├─ PostgreSQL → B-tree or Hash
│  ├─ MySQL → B-tree
│  └─ SQL Server → Non-clustered
│
├─ Range (column > value, BETWEEN)
│  ├─ PostgreSQL → B-tree
│  ├─ MySQL → B-tree
│  └─ SQL Server → Non-clustered
│
├─ Full-text search
│  ├─ PostgreSQL → GIN (tsvector)
│  ├─ MySQL → Full-text
│  └─ SQL Server → Full-text
│
├─ JSON queries
│  ├─ PostgreSQL → GIN (JSONB)
│  ├─ MySQL → Generated column + B-tree
│  └─ SQL Server → JSON index (2016+)
│
├─ Spatial queries
│  ├─ PostgreSQL → GiST (PostGIS)
│  ├─ MySQL → Spatial
│  └─ SQL Server → Spatial
│
└─ Large time-series table
   ├─ PostgreSQL → BRIN
   ├─ MySQL → Partitioning + B-tree
   └─ SQL Server → Partitioning + Columnstore
```
