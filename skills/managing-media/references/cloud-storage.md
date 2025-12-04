# Cloud Storage Integration

S3, R2, and GCS integration for media upload and delivery.

## S3 Direct Upload (Pre-signed URLs)

### Backend (Generate Pre-signed URL)

```python
import boto3
from datetime import timedelta

s3 = boto3.client('s3')

def generate_presigned_upload(filename: str) -> dict:
    key = f"uploads/{uuid.uuid4()}/{filename}"

    presigned_data = s3.generate_presigned_post(
        Bucket='my-bucket',
        Key=key,
        ExpiresIn=3600,  # 1 hour
        Conditions=[
            ['content-length-range', 0, 10485760],  # Max 10MB
            ['starts-with', '$Content-Type', 'image/'],
        ]
    )

    return {
        'url': presigned_data['url'],
        'fields': presigned_data['fields'],
        'key': key,
    }
```

### Frontend (Upload Directly to S3)

```tsx
async function uploadToS3(file: File) {
  // 1. Get pre-signed URL from backend
  const { url, fields, key } = await fetch('/api/upload/presign', {
    method: 'POST',
    body: JSON.stringify({ filename: file.name }),
  }).then(r => r.json());

  // 2. Upload directly to S3
  const formData = new FormData();
  Object.entries(fields).forEach(([k, v]) => formData.append(k, v as string));
  formData.append('file', file);

  await fetch(url, {
    method: 'POST',
    body: formData,
  });

  return key;
}
```

## Cloudflare R2

```tsx
// Backend
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';

const r2 = new S3Client({
  region: 'auto',
  endpoint: `https://${ACCOUNT_ID}.r2.cloudflarestorage.com`,
  credentials: {
    accessKeyId: R2_ACCESS_KEY_ID,
    secretAccessKey: R2_SECRET_ACCESS_KEY,
  },
});

await r2.send(new PutObjectCommand({
  Bucket: 'my-bucket',
  Key: key,
  Body: buffer,
  ContentType: 'image/jpeg',
}));
```

## Best Practices

1. **Pre-signed URLs** - Direct upload to S3/R2
2. **CDN in front** - CloudFront, Cloudflare
3. **Lifecycle policies** - Auto-delete temp files
4. **Access control** - Signed URLs for private content
5. **Compression** - Client-side before upload

## Resources

- AWS S3: https://aws.amazon.com/s3/
- Cloudflare R2: https://developers.cloudflare.com/r2/
