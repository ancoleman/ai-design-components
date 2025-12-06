# Cloud Storage Ingestion Patterns


## Table of Contents

- [S3 (AWS)](#s3-aws)
  - [Python with boto3](#python-with-boto3)
  - [TypeScript with AWS SDK v3](#typescript-with-aws-sdk-v3)
- [GCS (Google Cloud)](#gcs-google-cloud)
  - [Python with gcsfs](#python-with-gcsfs)
- [Azure Blob Storage](#azure-blob-storage)
  - [Python with adlfs](#python-with-adlfs)
- [Best Practices](#best-practices)

## S3 (AWS)

### Python with boto3
```python
import boto3
import polars as pl
from io import BytesIO

s3 = boto3.client('s3')

def list_and_ingest(bucket: str, prefix: str):
    """List objects and ingest all matching files."""
    paginator = s3.get_paginator('list_objects_v2')

    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get('Contents', []):
            key = obj['Key']
            if key.endswith('.parquet'):
                ingest_parquet(bucket, key)

def ingest_parquet(bucket: str, key: str) -> pl.DataFrame:
    """Ingest Parquet file from S3."""
    response = s3.get_object(Bucket=bucket, Key=key)
    return pl.read_parquet(BytesIO(response['Body'].read()))

# Stream large files
def stream_csv(bucket: str, key: str, chunk_size: int = 10000):
    """Stream CSV in chunks for memory efficiency."""
    response = s3.get_object(Bucket=bucket, Key=key)

    reader = pl.read_csv_batched(response['Body'], batch_size=chunk_size)
    while True:
        batch = reader.next_batches(1)
        if not batch:
            break
        yield batch[0]
```

### TypeScript with AWS SDK v3
```typescript
import { S3Client, GetObjectCommand, ListObjectsV2Command } from "@aws-sdk/client-s3";
import { Readable } from "stream";

const s3 = new S3Client({ region: process.env.AWS_REGION });

async function* listObjects(bucket: string, prefix: string) {
  let continuationToken: string | undefined;

  do {
    const response = await s3.send(new ListObjectsV2Command({
      Bucket: bucket,
      Prefix: prefix,
      ContinuationToken: continuationToken
    }));

    for (const obj of response.Contents ?? []) {
      yield obj;
    }

    continuationToken = response.NextContinuationToken;
  } while (continuationToken);
}

async function downloadAsStream(bucket: string, key: string): Promise<Readable> {
  const response = await s3.send(new GetObjectCommand({ Bucket: bucket, Key: key }));
  return response.Body as Readable;
}
```

## GCS (Google Cloud)

### Python with gcsfs
```python
import gcsfs
import polars as pl

fs = gcsfs.GCSFileSystem(project='my-project')

# Direct read with Polars
df = pl.read_parquet('gs://bucket/path/data.parquet')

# List and process
files = fs.glob('gs://bucket/data/*.csv')
for file in files:
    with fs.open(file) as f:
        df = pl.read_csv(f)
        process(df)
```

## Azure Blob Storage

### Python with adlfs
```python
import adlfs
import polars as pl

fs = adlfs.AzureBlobFileSystem(
    account_name='storageaccount',
    account_key='...'  # or use managed identity
)

# Read directly
df = pl.read_parquet('abfs://container/path/data.parquet')
```

## Best Practices

1. **Use appropriate file formats:**
   - Parquet for analytics (columnar, compressed)
   - JSON Lines for streaming/logs
   - CSV only for interchange with external systems

2. **Implement resumable downloads:**
   ```python
   def download_with_resume(bucket, key, local_path):
       existing_size = os.path.getsize(local_path) if os.path.exists(local_path) else 0
       response = s3.get_object(
           Bucket=bucket,
           Key=key,
           Range=f'bytes={existing_size}-'
       )
       with open(local_path, 'ab') as f:
           f.write(response['Body'].read())
   ```

3. **Track processed files:**
   ```python
   def mark_processed(key: str):
       db.execute(
           "INSERT INTO processed_files (key, processed_at) VALUES (?, ?)",
           (key, datetime.utcnow())
       )
   ```

4. **Handle rate limits:**
   - Use exponential backoff
   - Implement request throttling
   - Consider S3 Inventory for large bucket listings
