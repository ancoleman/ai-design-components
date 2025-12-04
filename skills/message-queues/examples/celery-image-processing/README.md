# Celery Image Processing Pipeline

Distributed image processing using Celery with FastAPI, including optimization, thumbnail generation, and CDN upload.

## Use Case

Handle image uploads asynchronously:
1. User uploads image → immediate response
2. Background: Optimize, generate thumbnails, upload to S3
3. Notify user when complete

## Files

```
celery-image-processing/
├── app/
│   ├── main.py              # FastAPI app
│   ├── celery_app.py        # Celery configuration
│   ├── tasks/
│   │   └── image_tasks.py   # Image processing tasks
│   └── routes/
│       └── upload.py        # Upload endpoint
├── requirements.txt
└── .env.example
```

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Start Redis
docker run -p 6379:6379 redis

# Start Celery worker
celery -A app.celery_app worker --loglevel=info

# Start FastAPI
uvicorn app.main:app --reload
```

## Implementation

### Celery Tasks

```python
# app/tasks/image_tasks.py
from celery import chain
from PIL import Image
import boto3

@celery_app.task
def optimize_image(image_path):
    """Optimize image (reduce file size)"""
    img = Image.open(image_path)

    # Optimize
    img.save(
        image_path,
        optimize=True,
        quality=85,
    )

    return image_path

@celery_app.task
def generate_thumbnail(image_path):
    """Generate 200x200 thumbnail"""
    img = Image.open(image_path)
    img.thumbnail((200, 200))

    thumb_path = image_path.replace('.jpg', '_thumb.jpg')
    img.save(thumb_path)

    return thumb_path

@celery_app.task
def upload_to_s3(file_paths):
    """Upload files to S3"""
    s3 = boto3.client('s3')
    urls = []

    for path in file_paths:
        key = f"images/{Path(path).name}"
        s3.upload_file(path, 'my-bucket', key)
        urls.append(f"https://my-bucket.s3.amazonaws.com/{key}")

    return urls

@celery_app.task
def notify_user(user_id, image_urls):
    """Send notification to user"""
    # Send email/push notification
    return {'notified': user_id, 'urls': image_urls}
```

### FastAPI Endpoint

```python
# app/routes/upload.py
from fastapi import APIRouter, UploadFile, File
from celery import chain

router = APIRouter()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...), user_id: int):
    # Save temp file
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Create task chain
    workflow = chain(
        optimize_image.s(temp_path),
        generate_thumbnail.s(),
        upload_to_s3.s(),
        notify_user.s(user_id),
    )

    task = workflow.apply_async()

    return {
        "message": "Processing started",
        "task_id": task.id,
        "status_url": f"/status/{task.id}"
    }

@router.get("/status/{task_id}")
async def get_status(task_id: str):
    from celery.result import AsyncResult

    task = AsyncResult(task_id)

    return {
        "task_id": task_id,
        "status": task.status,
        "result": task.result if task.ready() else None,
    }
```

## Error Handling

```python
@celery_app.task(bind=True, max_retries=3)
def upload_to_s3(self, file_path):
    try:
        s3.upload_file(file_path, 'bucket', 'key')
    except ClientError as exc:
        if exc.response['Error']['Code'] == 'SlowDown':
            # Retry with backoff
            raise self.retry(exc=exc, countdown=60)
        else:
            # Don't retry (permanent failure)
            raise
```

## Monitoring

```bash
# Start Flower dashboard
celery -A app.celery_app flower --port=5555
```

Features:
- Task progress tracking
- Failed task inspection
- Worker health monitoring
- Task rate graphs
