# File Format Handling

## CSV Processing

### Python (Polars - Recommended)
```python
import polars as pl

# Basic read with type inference
df = pl.read_csv("data.csv")

# With explicit schema
df = pl.read_csv(
    "data.csv",
    schema={
        "id": pl.Int64,
        "name": pl.Utf8,
        "amount": pl.Float64,
        "created_at": pl.Datetime
    },
    null_values=["", "NULL", "N/A"],
    skip_rows=1  # Skip header if needed
)

# Chunked reading for large files
reader = pl.read_csv_batched("large.csv", batch_size=100_000)
while True:
    batch = reader.next_batches(1)
    if not batch:
        break
    process_batch(batch[0])
```

### TypeScript (papaparse)
```typescript
import Papa from "papaparse";
import fs from "fs";

// Streaming parse
const file = fs.createReadStream("data.csv");

Papa.parse(file, {
  header: true,
  dynamicTyping: true,
  step: (row) => {
    // Process each row
    processRow(row.data);
  },
  complete: () => {
    console.log("Parsing complete");
  }
});
```

## JSON Processing

### JSON Lines (Recommended for streaming)
```python
import polars as pl
import json

# Polars native NDJSON
df = pl.read_ndjson("events.jsonl")

# Streaming JSON Lines
def stream_jsonl(path: str):
    with open(path) as f:
        for line in f:
            yield json.loads(line)

# Write JSON Lines
df.write_ndjson("output.jsonl")
```

### Nested JSON
```python
# Flatten nested structures
df = pl.read_json("nested.json")
df = df.unnest("metadata").unnest("user")
```

## Parquet (Analytics Recommended)

### Python
```python
import polars as pl

# Read with column selection (efficient!)
df = pl.read_parquet(
    "data.parquet",
    columns=["id", "amount", "created_at"]
)

# Read from S3 directly
df = pl.read_parquet("s3://bucket/data.parquet")

# Write with compression
df.write_parquet("output.parquet", compression="zstd")

# Partitioned writes
df.write_parquet(
    "output/",
    partition_by=["year", "month"]
)
```

### Rust (arrow-rs)
```rust
use arrow::parquet::arrow::arrow_reader::ParquetRecordBatchReaderBuilder;
use std::fs::File;

fn read_parquet(path: &str) -> Result<Vec<RecordBatch>> {
    let file = File::open(path)?;
    let builder = ParquetRecordBatchReaderBuilder::try_new(file)?;
    let reader = builder.build()?;

    reader.collect()
}
```

## Excel Processing

### Python (openpyxl + polars)
```python
import polars as pl

# Read specific sheet
df = pl.read_excel(
    "data.xlsx",
    sheet_name="Sheet1",
    read_options={"header_row": 0}
)

# Read all sheets
sheets = pl.read_excel("data.xlsx", sheet_name=None)
for name, df in sheets.items():
    print(f"Sheet: {name}, Rows: {len(df)}")
```

## Schema Validation

### Python with Pandera
```python
import pandera as pa
import polars as pl

schema = pa.DataFrameSchema({
    "id": pa.Column(int, nullable=False, unique=True),
    "email": pa.Column(str, pa.Check.str_matches(r'^[\w\.-]+@[\w\.-]+\.\w+$')),
    "amount": pa.Column(float, pa.Check.ge(0)),
    "status": pa.Column(str, pa.Check.isin(["pending", "completed", "failed"]))
})

# Validate
df = pl.read_csv("data.csv")
validated = schema.validate(df.to_pandas())
```

## Format Selection Guide

| Use Case | Format | Why |
|----------|--------|-----|
| Analytics/BI | Parquet | Columnar, compressed, fast |
| Streaming/Logs | JSON Lines | Appendable, streamable |
| Data Exchange | CSV | Universal compatibility |
| Human Editing | Excel/CSV | Familiar tools |
| Configuration | JSON/YAML | Structured, readable |
