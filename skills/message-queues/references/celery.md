# Celery Reference Guide

Distributed task queue for Python with support for scheduling, retries, and result backends.

## When to Use Celery

- Python ecosystem (FastAPI, Django, Flask)
- Complex task workflows (chains, groups, chords)
- Scheduled tasks (cron-like)
- Long-running background jobs
- Need multiple queue backends (Redis, RabbitMQ, SQS)

## Installation

```bash
# With Redis backend
pip install celery[redis]

# With RabbitMQ backend
pip install celery[amqp]

# With SQS backend
pip install celery[sqs]
```

## Basic Setup

### celery_app.py

```python
from celery import Celery

app = Celery(
    'myapp',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1',
)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@app.task
def add(x, y):
    return x + y

@app.task(bind=True, max_retries=3)
def send_email(self, to, subject, body):
    try:
        # Send email logic
        return {'sent': True, 'to': to}
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)  # Retry after 1 minute
```

## Running Workers

```bash
# Start worker (single process)
celery -A celery_app worker --loglevel=info

# Multiple workers with concurrency
celery -A celery_app worker --concurrency=4 --loglevel=info

# Specific queue
celery -A celery_app worker -Q high-priority,default --loglevel=info
```

## Task Invocation

```python
# Fire and forget
result = add.delay(4, 5)

# Wait for result
result = add.delay(4, 5)
print(result.get(timeout=10))  # Blocks until complete

# Async with callback
add.apply_async((4, 5), link=notify_completion.s())

# ETA (execute at specific time)
from datetime import datetime, timedelta
add.apply_async((4, 5), eta=datetime.now() + timedelta(hours=1))

# Countdown (delay in seconds)
add.apply_async((4, 5), countdown=300)  # Run in 5 minutes
```

## Task Routing and Prioritization

```python
# Route tasks to specific queues
app.conf.task_routes = {
    'myapp.tasks.send_email': {'queue': 'high-priority'},
    'myapp.tasks.generate_report': {'queue': 'low-priority'},
}

# Priority (0-9, higher = more important)
send_email.apply_async((to, subject, body), priority=9)
```

## Periodic Tasks (Beat)

```python
from celery.schedules import crontab

app.conf.beat_schedule = {
    'send-daily-report': {
        'task': 'myapp.tasks.generate_daily_report',
        'schedule': crontab(hour=9, minute=0),  # 9 AM daily
    },
    'cleanup-old-files': {
        'task': 'myapp.tasks.cleanup_files',
        'schedule': crontab(hour=2, minute=0, day_of_week='sunday'),
    },
    'check-every-5-minutes': {
        'task': 'myapp.tasks.health_check',
        'schedule': 300.0,  # Every 5 minutes (seconds)
    },
}
```

Start beat scheduler:
```bash
celery -A celery_app beat --loglevel=info
```

## Task Workflows

### Chain (Sequential)

```python
from celery import chain

# download → process → upload (sequential)
workflow = chain(
    download_image.s(url),
    process_image.s(),
    upload_to_s3.s(),
)

result = workflow.apply_async()
```

### Group (Parallel)

```python
from celery import group

# Process multiple images in parallel
job = group(
    process_image.s(image1),
    process_image.s(image2),
    process_image.s(image3),
)

result = job.apply_async()
results = result.get()  # Wait for all to complete
```

### Chord (Parallel + Callback)

```python
from celery import chord

# Process in parallel, then aggregate
job = chord(
    [process_image.s(img) for img in images],
    aggregate_results.s(),  # Called with all results
)

result = job.apply_async()
```

## Retry Configuration

```python
@app.task(
    bind=True,
    autoretry_for=(ConnectionError, TimeoutError),
    retry_kwargs={'max_retries': 5},
    retry_backoff=True,     # Exponential backoff
    retry_backoff_max=600,  # Max 10 minutes
    retry_jitter=True,      # Add randomness
)
def flaky_api_call(self, url):
    response = requests.get(url, timeout=10)
    return response.json()
```

## Task Progress Tracking

```python
@app.task(bind=True)
def long_running_task(self, items):
    total = len(items)

    for i, item in enumerate(items):
        process_item(item)

        # Update progress
        self.update_state(
            state='PROGRESS',
            meta={'current': i + 1, 'total': total, 'percent': (i + 1) / total * 100}
        )

    return {'status': 'Complete', 'processed': total}

# Check progress
result = long_running_task.delay(items)
while not result.ready():
    info = result.info
    if isinstance(info, dict):
        print(f"Progress: {info.get('percent')}%")
    time.sleep(1)
```

## FastAPI Integration

```python
from fastapi import FastAPI, BackgroundTasks
from celery.result import AsyncResult

app = FastAPI()

@app.post("/process")
async def process_endpoint(data: dict):
    # Queue task
    task = process_data.delay(data)

    return {"task_id": task.id, "status": "queued"}

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    task = AsyncResult(task_id, app=celery_app)

    return {
        "task_id": task_id,
        "status": task.status,
        "result": task.result if task.ready() else None,
    }
```

## Monitoring with Flower

```bash
# Install
pip install flower

# Run dashboard
celery -A celery_app flower --port=5555
```

Access: http://localhost:5555

Features:
- Real-time task monitoring
- Worker management
- Task history and stats
- Retry/revoke tasks
- Task rate graphs

## Result Backends

```python
# Redis (default)
app = Celery(broker='redis://localhost', backend='redis://localhost')

# PostgreSQL (persistent)
app = Celery(
    broker='redis://localhost',
    backend='db+postgresql://user:pass@localhost/celery_results'
)

# Disable backend (fire-and-forget)
app = Celery(broker='redis://localhost', backend=None)
```

## Best Practices

1. **Keep tasks small** - Break large jobs into smaller tasks
2. **Use task routing** - Separate queues for different priorities
3. **Set timeouts** - Prevent hanging tasks
4. **Monitor task states** - Failed tasks need attention
5. **Clean old results** - `result_expires` setting
6. **Use idempotent tasks** - Safe to retry
7. **Avoid task coupling** - Tasks shouldn't depend on each other's state
8. **Use serializers wisely** - JSON (safe), pickle (faster but unsafe)

## Common Patterns

### Image Processing

```python
@app.task
def process_uploaded_image(image_path):
    # Optimize
    optimized = optimize_image(image_path)

    # Generate variants
    thumbnail = generate_thumbnail(optimized)
    webp = convert_to_webp(optimized)

    # Upload to CDN
    urls = upload_to_cdn([optimized, thumbnail, webp])

    return {'urls': urls}

# Usage in upload endpoint
@app.post("/upload")
async def upload_image(file: UploadFile):
    path = await save_temp_file(file)
    task = process_uploaded_image.delay(path)
    return {"task_id": task.id}
```

### Email Campaigns

```python
@app.task
def send_campaign_emails(campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    users = campaign.get_target_users()

    # Create group of tasks
    job = group(send_email.s(user.email, campaign.template) for user in users)
    return job.apply_async()

@app.task(rate_limit='100/m')  # Max 100 emails/minute
def send_email(to, template):
    # Actual email sending
    pass
```

## Resources

- Celery Docs: https://docs.celeryq.dev/
- Flower: https://flower.readthedocs.io/
- GitHub: https://github.com/celery/celery
