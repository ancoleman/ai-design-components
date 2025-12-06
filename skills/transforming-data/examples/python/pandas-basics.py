"""
pandas Basic Transformations Example

Demonstrates common pandas operations for data transformation.

Dependencies:
    pip install pandas

Usage:
    python pandas-basics.py
"""

import pandas as pd
from datetime import datetime

def example_read_and_filter():
    """Read CSV and filter data"""
    # Read CSV
    df = pd.read_csv('sales.csv')

    # Filter rows
    df_2024 = df[df['year'] == 2024]

    # Multiple conditions
    df_filtered = df[(df['year'] == 2024) & (df['region'] == 'US')]

    return df_filtered


def example_calculated_columns():
    """Add calculated columns"""
    df = pd.read_csv('sales.csv')

    # Simple calculation
    df['revenue'] = df['quantity'] * df['price']

    # Method chaining with assign
    df = (
        df
        .assign(revenue=lambda x: x['quantity'] * x['price'])
        .assign(discount_amount=lambda x: x['revenue'] * x['discount_pct'] / 100)
        .assign(net_revenue=lambda x: x['revenue'] - x['discount_amount'])
    )

    return df


def example_groupby_aggregation():
    """Group by and aggregate"""
    df = pd.read_csv('sales.csv')

    # Simple aggregation
    revenue_by_region = df.groupby('region')['revenue'].sum()

    # Multiple aggregations
    summary = df.groupby(['region', 'product_category']).agg({
        'revenue': ['sum', 'mean', 'count'],
        'quantity': 'sum',
        'order_id': 'nunique'  # Count distinct
    })

    # Named aggregations (pandas 0.25+)
    summary_named = df.groupby('region').agg(
        total_revenue=('revenue', 'sum'),
        avg_revenue=('revenue', 'mean'),
        order_count=('order_id', 'nunique'),
        total_quantity=('quantity', 'sum')
    ).reset_index()

    return summary_named


def example_window_functions():
    """Window function equivalents"""
    df = pd.read_csv('sales.csv')

    # Cumulative sum
    df['cumulative_revenue'] = df.groupby('customer_id')['revenue'].cumsum()

    # Rank
    df['revenue_rank'] = df.groupby('region')['revenue'].rank(ascending=False, method='dense')

    # Lag (previous value)
    df = df.sort_values(['customer_id', 'order_date'])
    df['prev_order_amount'] = df.groupby('customer_id')['revenue'].shift(1)

    # Rolling average (7-day)
    df = df.sort_values('order_date')
    df['revenue_7d_ma'] = df['revenue'].rolling(window=7, min_periods=1).mean()

    return df


def example_join_operations():
    """Join multiple DataFrames"""
    orders = pd.read_csv('orders.csv')
    customers = pd.read_csv('customers.csv')
    products = pd.read_csv('products.csv')

    # Left join
    orders_with_customers = orders.merge(
        customers,
        on='customer_id',
        how='left'
    )

    # Multiple joins
    full_data = (
        orders
        .merge(customers, on='customer_id', how='left')
        .merge(products, on='product_id', how='left')
    )

    return full_data


def example_complete_pipeline():
    """Complete transformation pipeline"""
    df = pd.read_csv('raw_sales.csv')

    result = (
        df
        # Filter to 2024
        .query('year == 2024 and order_status != "cancelled"')

        # Add calculated columns
        .assign(
            revenue=lambda x: x['quantity'] * x['price'],
            discount_amount=lambda x: x['revenue'] * x['discount_pct'] / 100,
            net_revenue=lambda x: x['revenue'] - x['discount_amount']
        )

        # Group and aggregate
        .groupby(['region', 'product_category'])
        .agg({
            'net_revenue': ['sum', 'mean'],
            'quantity': 'sum',
            'order_id': 'nunique'
        })

        # Flatten multi-index columns
        .reset_index()

        # Sort by revenue
        .sort_values(('net_revenue', 'sum'), ascending=False)
    )

    # Flatten column names
    result.columns = ['_'.join(col).strip('_') if col[1] else col[0]
                      for col in result.columns.values]

    return result


def example_data_quality_checks():
    """Validate data quality"""
    df = pd.read_csv('sales.csv')

    # Check for nulls
    assert df['order_id'].notna().all(), "order_id has nulls"
    assert df['customer_id'].notna().all(), "customer_id has nulls"

    # Check for duplicates
    assert df['order_id'].is_unique, "Duplicate order_ids found"

    # Check value ranges
    assert (df['quantity'] > 0).all(), "Negative quantities found"
    assert (df['price'] >= 0).all(), "Negative prices found"

    # Check data types
    assert df['order_date'].dtype == 'datetime64[ns]', "order_date not datetime"

    print("All quality checks passed!")
    return df


if __name__ == '__main__':
    # Example usage
    print("Running pandas transformation examples...")

    # Run examples (would need actual CSV files)
    # result = example_complete_pipeline()
    # result.to_csv('transformed_sales.csv', index=False)

    print("Examples completed successfully!")
