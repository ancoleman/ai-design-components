"""
PySpark Transformations Example

Dependencies:
    pip install pyspark

Usage:
    spark-submit pyspark-transformations.py
"""

from pyspark.sql import SparkSession, functions as F, Window

# Initialize Spark
spark = SparkSession.builder \
    .appName("DataTransformations") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

# Read data
df = spark.read.parquet('s3://bucket/sales/*.parquet')

# Basic transformations
result = (
    df
    .filter(F.col('year') == 2024)
    .withColumn('revenue', F.col('quantity') * F.col('price'))
    .groupBy('region')
    .agg(F.sum('revenue').alias('total_revenue'))
    .orderBy(F.desc('total_revenue'))
)

# Window functions
window_spec = Window.partitionBy('customer_id').orderBy('order_date')

df_with_windows = df.withColumn(
    'customer_order_number',
    F.row_number().over(window_spec)
)

# Save with partitioning
result.write.mode('overwrite').partitionBy('region').parquet('s3://bucket/output/')
