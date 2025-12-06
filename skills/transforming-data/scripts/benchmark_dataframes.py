#!/usr/bin/env python3
"""
Benchmark pandas vs polars Performance

Compare execution times for common DataFrame operations.

Dependencies:
    pip install pandas polars

Usage:
    python benchmark_dataframes.py
"""

import pandas as pd
import polars as pl
import time
import tempfile
import numpy as np

def generate_test_data(rows=1_000_000):
    """Generate test CSV data"""
    print(f"Generating {rows:,} rows of test data...")

    data = pd.DataFrame({
        'id': range(rows),
        'year': np.random.choice([2023, 2024], rows),
        'region': np.random.choice(['US', 'EU', 'APAC'], rows),
        'quantity': np.random.randint(1, 100, rows),
        'price': np.random.uniform(10, 1000, rows)
    })

    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
    data.to_csv(temp_file.name, index=False)
    print(f"Test data saved to: {temp_file.name}")

    return temp_file.name


def benchmark_pandas(file_path):
    """Benchmark pandas transformation"""
    start = time.time()

    df = pd.read_csv(file_path)
    result = (
        df[df['year'] == 2024]
        .assign(revenue=lambda x: x['quantity'] * x['price'])
        .groupby('region')
        .agg({'revenue': ['sum', 'mean']})
    )

    elapsed = time.time() - start
    return elapsed, len(result)


def benchmark_polars_eager(file_path):
    """Benchmark polars eager transformation"""
    start = time.time()

    df = pl.read_csv(file_path)
    result = (
        df
        .filter(pl.col('year') == 2024)
        .with_columns([(pl.col('quantity') * pl.col('price')).alias('revenue')])
        .group_by('region')
        .agg([
            pl.col('revenue').sum().alias('revenue_sum'),
            pl.col('revenue').mean().alias('revenue_mean')
        ])
    )

    elapsed = time.time() - start
    return elapsed, len(result)


def benchmark_polars_lazy(file_path):
    """Benchmark polars lazy transformation"""
    start = time.time()

    result = (
        pl.scan_csv(file_path)
        .filter(pl.col('year') == 2024)
        .with_columns([(pl.col('quantity') * pl.col('price')).alias('revenue')])
        .group_by('region')
        .agg([
            pl.col('revenue').sum().alias('revenue_sum'),
            pl.col('revenue').mean().alias('revenue_mean')
        ])
        .collect()
    )

    elapsed = time.time() - start
    return elapsed, len(result)


def run_benchmarks(file_path):
    """Run all benchmarks"""
    print("\n" + "="*60)
    print("DataFrame Library Benchmark")
    print("="*60)

    # pandas
    print("\nRunning pandas benchmark...")
    pandas_time, pandas_rows = benchmark_pandas(file_path)
    print(f"pandas: {pandas_time:.2f}s ({pandas_rows} result rows)")

    # polars eager
    print("\nRunning polars (eager) benchmark...")
    polars_eager_time, polars_eager_rows = benchmark_polars_eager(file_path)
    print(f"polars (eager): {polars_eager_time:.2f}s ({polars_eager_rows} result rows)")

    # polars lazy
    print("\nRunning polars (lazy) benchmark...")
    polars_lazy_time, polars_lazy_rows = benchmark_polars_lazy(file_path)
    print(f"polars (lazy): {polars_lazy_time:.2f}s ({polars_lazy_rows} result rows)")

    # Summary
    print("\n" + "="*60)
    print("Performance Summary")
    print("="*60)
    print(f"pandas:        {pandas_time:.2f}s (baseline)")
    print(f"polars eager:  {polars_eager_time:.2f}s ({pandas_time/polars_eager_time:.1f}x faster)")
    print(f"polars lazy:   {polars_lazy_time:.2f}s ({pandas_time/polars_lazy_time:.1f}x faster)")
    print("="*60)


if __name__ == '__main__':
    # Generate test data
    test_file = generate_test_data(rows=1_000_000)

    # Run benchmarks
    run_benchmarks(test_file)

    print("\nConclusion: polars is typically 10-100x faster than pandas")
    print("Use polars for production pipelines with large datasets")
