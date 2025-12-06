"""
polars Migration Example - pandas to polars

Demonstrates migrating from pandas to polars for 10-100x performance improvement.

Dependencies:
    pip install polars pandas

Usage:
    python polars-migration.py
"""

import polars as pl
import pandas as pd
import time

# COMPARISON: pandas vs polars for same task

def pandas_transformation(file_path):
    """pandas version (eager evaluation, single-threaded)"""
    start = time.time()

    df = pd.read_csv(file_path)
    result = (
        df
        [df['year'] == 2024]
        .assign(revenue=lambda x: x['quantity'] * x['price'])
        .groupby(['region', 'product_id'])
        .agg({'revenue': ['sum', 'mean'], 'quantity': 'sum'})
        .reset_index()
    )

    elapsed = time.time() - start
    print(f"pandas: {elapsed:.2f} seconds")
    return result


def polars_transformation(file_path):
    """polars version (lazy evaluation, multi-threaded)"""
    start = time.time()

    result = (
        pl.scan_csv(file_path)  # Lazy read
        .filter(pl.col('year') == 2024)
        .with_columns([
            (pl.col('quantity') * pl.col('price')).alias('revenue')
        ])
        .group_by(['region', 'product_id'])
        .agg([
            pl.col('revenue').sum().alias('revenue_sum'),
            pl.col('revenue').mean().alias('revenue_mean'),
            pl.col('quantity').sum().alias('quantity_sum')
        ])
        .collect()  # Execute lazy query
    )

    elapsed = time.time() - start
    print(f"polars: {elapsed:.2f} seconds")
    return result


# MIGRATION PATTERNS

def pattern_read_data():
    """Reading data: pandas vs polars"""

    # pandas (eager)
    df_pandas = pd.read_csv('data.csv')
    df_pandas = pd.read_parquet('data.parquet')

    # polars (eager)
    df_polars = pl.read_csv('data.csv')
    df_polars = pl.read_parquet('data.parquet')

    # polars (lazy - recommended for large files)
    df_lazy = pl.scan_csv('data.csv')  # Returns LazyFrame
    df_lazy = pl.scan_parquet('data.parquet')
    df = df_lazy.collect()  # Execute when needed


def pattern_filtering():
    """Filtering: pandas vs polars"""

    # pandas
    df_pandas = df[df['age'] > 25]
    df_pandas = df[(df['age'] > 25) & (df['city'] == 'NYC')]

    # polars
    df_polars = df.filter(pl.col('age') > 25)
    df_polars = df.filter((pl.col('age') > 25) & (pl.col('city') == 'NYC'))


def pattern_add_columns():
    """Adding columns: pandas vs polars"""

    # pandas
    df['revenue'] = df['quantity'] * df['price']
    df = df.assign(revenue=lambda x: x['quantity'] * x['price'])

    # polars
    df = df.with_columns([
        (pl.col('quantity') * pl.col('price')).alias('revenue')
    ])


def pattern_groupby():
    """Grouping and aggregation: pandas vs polars"""

    # pandas
    result = df.groupby('region').agg({
        'revenue': ['sum', 'mean'],
        'quantity': 'sum'
    })

    # polars
    result = df.group_by('region').agg([
        pl.col('revenue').sum().alias('revenue_sum'),
        pl.col('revenue').mean().alias('revenue_mean'),
        pl.col('quantity').sum().alias('quantity_sum')
    ])


def pattern_window_functions():
    """Window functions: pandas vs polars"""

    # pandas (cumulative sum)
    df = df.sort_values('date')
    df['cumsum'] = df['revenue'].cumsum()

    # polars (cumulative sum)
    df = df.sort('date')
    df = df.with_columns([
        pl.col('revenue').cum_sum().alias('cumsum')
    ])

    # pandas (moving average)
    df['ma_7d'] = df['revenue'].rolling(window=7).mean()

    # polars (moving average)
    df = df.with_columns([
        pl.col('revenue').rolling_mean(window_size=7).alias('ma_7d')
    ])


def pattern_complete_pipeline():
    """Complete pipeline comparison"""

    # pandas version
    df_pandas = (
        pd.read_csv('sales.csv')
        .query('year == 2024')
        .assign(revenue=lambda x: x['quantity'] * x['price'])
        .groupby('region')
        .agg({'revenue': 'sum'})
        .sort_values('revenue', ascending=False)
    )

    # polars version (lazy - optimized)
    df_polars = (
        pl.scan_csv('sales.csv')
        .filter(pl.col('year') == 2024)
        .with_columns([(pl.col('quantity') * pl.col('price')).alias('revenue')])
        .group_by('region')
        .agg(pl.col('revenue').sum())
        .sort('revenue', descending=True)
        .collect()  # Execute optimized query plan
    )


# LAZY EVALUATION BENEFITS

def lazy_evaluation_example():
    """Demonstrate query optimization with lazy evaluation"""

    # Build lazy query (no execution yet)
    lazy_query = (
        pl.scan_csv('large_file.csv')
        .filter(pl.col('year') == 2024)  # Predicate pushdown
        .select(['customer_id', 'revenue'])  # Projection pushdown
        .filter(pl.col('revenue') > 100)  # Combined with first filter
        .group_by('customer_id')
        .agg(pl.col('revenue').sum())
        .sort('revenue', descending=True)
        .head(100)  # Limit pushdown
    )

    # polars optimizes query plan before execution:
    # - Pushes filters early (read less data)
    # - Only reads needed columns
    # - Combines filters
    # - Applies limit early

    # Execute optimized query
    result = lazy_query.collect()

    # Or stream for very large datasets
    result = lazy_query.collect(streaming=True)


# STREAMING FOR OUT-OF-MEMORY DATASETS

def streaming_example():
    """Process datasets larger than RAM"""

    # Process 100GB file with 16GB RAM
    result = (
        pl.scan_csv('very_large_file.csv')
        .filter(pl.col('year') == 2024)
        .group_by('region')
        .agg(pl.col('revenue').sum())
        .collect(streaming=True)  # Process in chunks
    )


if __name__ == '__main__':
    print("polars migration examples...")
    print("polars is 10-100x faster than pandas for most operations")
    print("Use lazy evaluation (.scan_*) for automatic query optimization")
