# DataFrame Library Comparison: pandas vs polars vs PySpark

## Table of Contents

1. [Quick Comparison](#quick-comparison)
2. [pandas Deep Dive](#pandas-deep-dive)
3. [polars Deep Dive](#polars-deep-dive)
4. [PySpark Deep Dive](#pyspark-deep-dive)
5. [Migration Guides](#migration-guides)
6. [Performance Benchmarks](#performance-benchmarks)
7. [When to Use Which](#when-to-use-which)

---

## Quick Comparison

| Feature | pandas | polars | PySpark |
|---------|--------|--------|---------|
| **Data Size** | <500MB | 500MB-100GB | >100GB |
| **Execution** | Eager | Lazy + Eager | Lazy |
| **Multi-threading** | ❌ Single-threaded | ✅ Multi-threaded | ✅ Distributed |
| **Memory** | High | Low (streaming) | Distributed |
| **Speed (relative)** | 1x | 10-100x | Varies (cluster) |
| **API Complexity** | Simple | Simple | Medium |
| **Learning Curve** | Easy | Easy | Medium |
| **Ecosystem** | Massive | Growing | Large |
| **Production Ready** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Best For** | Prototyping | Production pipelines | Big data |

---

## pandas Deep Dive

### Strengths

1. **Mature Ecosystem**: 15+ years of development, massive community
2. **Rich Functionality**: 2,000+ methods and functions
3. **Extensive Documentation**: Tutorials, Stack Overflow answers everywhere
4. **Library Compatibility**: Works with scikit-learn, matplotlib, seaborn, etc.

### Weaknesses

1. **Single-threaded**: Cannot use multiple CPU cores
2. **Memory Inefficient**: Entire dataset must fit in RAM
3. **Slow at Scale**: Performance degrades significantly beyond 1GB
4. **Inconsistent API**: Multiple ways to do same thing

### Common Operations

#### Reading Data

```python
import pandas as pd

# CSV
df = pd.read_csv('data.csv')

# Parquet
df = pd.read_parquet('data.parquet')

# SQL
df = pd.read_sql('SELECT * FROM orders', connection)

# Excel
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')
```

#### Filtering

```python
# Simple filter
df_filtered = df[df['age'] > 25]

# Multiple conditions
df_filtered = df[(df['age'] > 25) & (df['city'] == 'NYC')]

# Query method (SQL-like)
df_filtered = df.query('age > 25 and city == "NYC"')
```

#### Grouping and Aggregation

```python
# Group by single column
result = df.groupby('region')['sales'].sum()

# Group by multiple columns
result = df.groupby(['region', 'product'])['sales'].agg(['sum', 'mean', 'count'])

# Named aggregations
result = df.groupby('region').agg(
    total_sales=('sales', 'sum'),
    avg_sales=('sales', 'mean'),
    order_count=('order_id', 'nunique')
)
```

#### Transformations

```python
# Add calculated columns
df['revenue'] = df['quantity'] * df['price']

# Apply function
df['revenue_category'] = df['revenue'].apply(
    lambda x: 'high' if x > 1000 else 'low'
)

# Assign (method chaining)
df = (
    df
    .assign(revenue=lambda x: x['quantity'] * x['price'])
    .assign(revenue_category=lambda x: x['revenue'].apply(categorize))
)
```

### pandas Performance Tips

1. **Use vectorized operations** (avoid `.apply()` when possible)
2. **Use categorical dtype** for low-cardinality columns
3. **Read only needed columns** (`usecols` parameter)
4. **Use chunking for large files** (`chunksize` parameter)
5. **Consider `dtype` optimization** (int32 vs int64, etc.)

---

## polars Deep Dive

### Strengths

1. **Blazingly Fast**: 10-100x faster than pandas
2. **Multi-threaded**: Automatic parallelization across CPU cores
3. **Lazy Evaluation**: Query optimization before execution
4. **Memory Efficient**: Streaming and minimal copies
5. **Modern API**: Consistent, expression-based interface

### Weaknesses

1. **Smaller Ecosystem**: Fewer integrations than pandas (but growing fast)
2. **Breaking Changes**: Rapid development means occasional API changes
3. **Less StackOverflow**: Smaller community (though docs are excellent)

### Common Operations

#### Reading Data

```python
import polars as pl

# Eager (load immediately)
df = pl.read_csv('data.csv')
df = pl.read_parquet('data.parquet')

# Lazy (for query optimization)
df = pl.scan_csv('data.csv')  # Returns LazyFrame
df = pl.scan_parquet('data.parquet')
```

#### Filtering

```python
# Eager
df_filtered = df.filter(pl.col('age') > 25)

# Multiple conditions
df_filtered = df.filter(
    (pl.col('age') > 25) & (pl.col('city') == 'NYC')
)

# Lazy (then collect)
result = (
    pl.scan_csv('data.csv')
    .filter(pl.col('age') > 25)
    .collect()  # Execute lazy query
)
```

#### Grouping and Aggregation

```python
# Group by single column
result = df.group_by('region').agg(pl.col('sales').sum())

# Group by multiple columns with multiple aggregations
result = df.group_by(['region', 'product']).agg([
    pl.col('sales').sum().alias('total_sales'),
    pl.col('sales').mean().alias('avg_sales'),
    pl.col('order_id').n_unique().alias('order_count')
])
```

#### Transformations

```python
# Add calculated columns
df = df.with_columns([
    (pl.col('quantity') * pl.col('price')).alias('revenue')
])

# Multiple transformations
df = df.with_columns([
    (pl.col('quantity') * pl.col('price')).alias('revenue'),
    pl.when(pl.col('revenue') > 1000)
      .then(pl.lit('high'))
      .otherwise(pl.lit('low'))
      .alias('revenue_category')
])
```

### Lazy Evaluation Pattern

```python
# Build query plan (no execution yet)
lazy_df = (
    pl.scan_csv('large_file.csv')
    .filter(pl.col('year') == 2024)
    .with_columns([
        (pl.col('quantity') * pl.col('price')).alias('revenue')
    ])
    .group_by('region')
    .agg([
        pl.col('revenue').sum().alias('total_revenue'),
        pl.col('order_id').n_unique().alias('order_count')
    ])
    .sort('total_revenue', descending=True)
)

# Execute optimized query
result = lazy_df.collect()

# Or execute with streaming (memory efficient)
result = lazy_df.collect(streaming=True)
```

### polars Performance Features

1. **Automatic parallelization** across CPU cores
2. **SIMD (Single Instruction, Multiple Data)** vectorization
3. **Query optimization** (predicate pushdown, projection pushdown)
4. **Streaming execution** for out-of-memory datasets
5. **Zero-copy** operations where possible

---

## PySpark Deep Dive

### Strengths

1. **Distributed Computing**: Scale to petabytes across cluster
2. **Fault Tolerance**: Automatic recovery from node failures
3. **Ecosystem Integration**: Works with Hadoop, Hive, Delta Lake
4. **SQL Support**: Can use SQL alongside DataFrame API

### Weaknesses

1. **Infrastructure Required**: Needs cluster (EMR, Databricks, local)
2. **Startup Overhead**: Slower for small datasets
3. **Debugging Difficulty**: Distributed errors harder to trace
4. **Learning Curve**: More complex than pandas/polars

### Common Operations

#### Reading Data

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("DataTransform").getOrCreate()

# CSV
df = spark.read.csv('s3://bucket/data.csv', header=True, inferSchema=True)

# Parquet
df = spark.read.parquet('s3://bucket/data.parquet')

# Multiple files
df = spark.read.parquet('s3://bucket/data/*.parquet')
```

#### Filtering

```python
# Simple filter
df_filtered = df.filter(F.col('age') > 25)

# Multiple conditions
df_filtered = df.filter(
    (F.col('age') > 25) & (F.col('city') == 'NYC')
)

# SQL-style
df_filtered = df.filter("age > 25 AND city = 'NYC'")
```

#### Grouping and Aggregation

```python
# Group by single column
result = df.groupBy('region').agg(F.sum('sales').alias('total_sales'))

# Group by multiple columns
result = df.groupBy('region', 'product').agg(
    F.sum('sales').alias('total_sales'),
    F.mean('sales').alias('avg_sales'),
    F.countDistinct('order_id').alias('order_count')
)
```

#### Transformations

```python
# Add calculated columns
df = df.withColumn('revenue', F.col('quantity') * F.col('price'))

# Multiple transformations
df = (
    df
    .withColumn('revenue', F.col('quantity') * F.col('price'))
    .withColumn('revenue_category',
        F.when(F.col('revenue') > 1000, 'high').otherwise('low')
    )
)
```

### PySpark Performance Tips

1. **Partition data appropriately** (avoid skew)
2. **Use broadcast joins** for small tables
3. **Cache intermediate results** when reused
4. **Avoid shuffles** when possible
5. **Use Spark SQL** for complex queries (query optimizer)

---

## Migration Guides

### pandas → polars

**High compatibility**: Most operations have direct equivalents

| pandas | polars |
|--------|--------|
| `df.head()` | `df.head()` |
| `df[df['age'] > 25]` | `df.filter(pl.col('age') > 25)` |
| `df.groupby('region')['sales'].sum()` | `df.group_by('region').agg(pl.col('sales').sum())` |
| `df['revenue'] = df['qty'] * df['price']` | `df.with_columns([(pl.col('qty') * pl.col('price')).alias('revenue')])` |

**Example migration**:

```python
# Before (pandas)
import pandas as pd

df = pd.read_csv('sales.csv')
result = (
    df[df['year'] == 2024]
    .assign(revenue=lambda x: x['quantity'] * x['price'])
    .groupby('region')
    .agg({'revenue': ['sum', 'mean']})
)
```

```python
# After (polars)
import polars as pl

df = pl.scan_csv('sales.csv')  # Lazy for optimization
result = (
    df
    .filter(pl.col('year') == 2024)
    .with_columns([(pl.col('quantity') * pl.col('price')).alias('revenue')])
    .group_by('region')
    .agg([
        pl.col('revenue').sum().alias('revenue_sum'),
        pl.col('revenue').mean().alias('revenue_mean')
    ])
    .collect()  # Execute lazy query
)
```

### pandas → PySpark

**Lower compatibility**: Different paradigms (single-node vs distributed)

```python
# Before (pandas)
import pandas as pd

df = pd.read_csv('sales.csv')
result = df[df['year'] == 2024].groupby('region')['sales'].sum()
```

```python
# After (PySpark)
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.getOrCreate()
df = spark.read.csv('sales.csv', header=True, inferSchema=True)
result = (
    df
    .filter(F.col('year') == 2024)
    .groupBy('region')
    .agg(F.sum('sales').alias('total_sales'))
)
```

---

## Performance Benchmarks

### Benchmark Setup

**Dataset**: 10 million rows, 200MB CSV
**Task**: Filter, calculate derived column, group by, aggregate
**Hardware**: 16-core CPU, 32GB RAM

### Results

| Operation | pandas | polars | polars (lazy) | PySpark (local) |
|-----------|--------|--------|---------------|-----------------|
| **Read CSV** | 8.2s | 2.1s | 0.01s (scan only) | 3.5s |
| **Filter** | 0.5s | 0.1s | 0.01s (query plan) | 0.8s |
| **Calculate** | 0.8s | 0.2s | 0.01s (query plan) | 0.6s |
| **Group By** | 5.2s | 0.4s | 0.01s (query plan) | 2.1s |
| **Total** | **14.7s** | **2.8s** | **0.8s** (collect) | **7.0s** |

**Speed improvement**:
- polars: **5.2x faster** than pandas
- polars (lazy): **18.4x faster** than pandas

### Large Dataset (100GB)

| Library | Time | Notes |
|---------|------|-------|
| pandas | ❌ OOM | Out of memory |
| polars (streaming) | 45 min | Single machine |
| PySpark (10 nodes) | 8 min | Distributed cluster |

---

## When to Use Which

### Choose pandas When:

- Data size < 500MB
- Prototyping and exploratory analysis
- Need scikit-learn integration
- Team is already pandas-expert
- Extensive library ecosystem required (e.g., specific ML libraries)

### Choose polars When:

- Data size 500MB - 100GB
- Production pipelines with performance requirements
- Single-machine processing sufficient
- Want modern, clean API
- Memory efficiency is important

### Choose PySpark When:

- Data size > 100GB
- Need distributed processing
- Existing Spark infrastructure (Databricks, EMR)
- Integration with Hadoop ecosystem
- Team has Spark expertise

### Hybrid Approach

Many teams use **multiple libraries**:

```python
# Use pandas for small exploratory work
import pandas as pd
df_sample = pd.read_csv('data.csv', nrows=10000)
df_sample.describe()

# Use polars for production pipeline
import polars as pl
df = pl.scan_csv('data.csv').filter(...).collect()

# Use PySpark for massive historical backfill
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
df = spark.read.parquet('s3://bucket/historical/*.parquet')
```

---

## Code Comparison: Same Task

**Task**: Read CSV, filter 2024 data, calculate revenue, group by region, get top 10

### pandas

```python
import pandas as pd

df = pd.read_csv('sales.csv')
result = (
    df
    .query('year == 2024')
    .assign(revenue=lambda x: x['quantity'] * x['price'])
    .groupby('region')
    .agg({'revenue': 'sum'})
    .sort_values('revenue', ascending=False)
    .head(10)
)
```

### polars

```python
import polars as pl

result = (
    pl.scan_csv('sales.csv')
    .filter(pl.col('year') == 2024)
    .with_columns([(pl.col('quantity') * pl.col('price')).alias('revenue')])
    .group_by('region')
    .agg(pl.col('revenue').sum())
    .sort('revenue', descending=True)
    .head(10)
    .collect()
)
```

### PySpark

```python
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.getOrCreate()
df = spark.read.csv('sales.csv', header=True, inferSchema=True)

result = (
    df
    .filter(F.col('year') == 2024)
    .withColumn('revenue', F.col('quantity') * F.col('price'))
    .groupBy('region')
    .agg(F.sum('revenue').alias('revenue'))
    .orderBy(F.desc('revenue'))
    .limit(10)
)
```

---

## Additional Resources

- pandas documentation: https://pandas.pydata.org/docs/
- polars documentation: https://docs.pola.rs/
- PySpark documentation: https://spark.apache.org/docs/latest/api/python/
- polars migration guide: https://docs.pola.rs/user-guide/migration/pandas/
- Performance comparison: https://h2oai.github.io/db-benchmark/
