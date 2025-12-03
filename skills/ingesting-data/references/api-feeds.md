# API Feed Ingestion

## REST API Polling

### Python with httpx (async)
```python
import httpx
import asyncio
from datetime import datetime, timedelta

async def poll_api(
    url: str,
    interval_seconds: int = 60,
    cursor_field: str = "updated_at"
):
    """Poll API with incremental loading."""
    async with httpx.AsyncClient() as client:
        cursor = load_cursor()  # Load from DB/file

        while True:
            params = {cursor_field + "_gt": cursor} if cursor else {}

            response = await client.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            if data["items"]:
                await process_items(data["items"])
                cursor = max(item[cursor_field] for item in data["items"])
                save_cursor(cursor)

            await asyncio.sleep(interval_seconds)

# With pagination
async def fetch_all_pages(url: str, page_size: int = 100):
    """Fetch all pages from paginated API."""
    async with httpx.AsyncClient() as client:
        page = 1
        while True:
            response = await client.get(url, params={
                "page": page,
                "per_page": page_size
            })
            data = response.json()

            yield data["items"]

            if len(data["items"]) < page_size:
                break
            page += 1
```

### TypeScript with fetch
```typescript
async function* fetchWithPagination(baseUrl: string, pageSize = 100) {
  let cursor: string | undefined;

  while (true) {
    const url = new URL(baseUrl);
    url.searchParams.set("limit", String(pageSize));
    if (cursor) url.searchParams.set("cursor", cursor);

    const response = await fetch(url);
    const data = await response.json();

    yield data.items;

    cursor = data.next_cursor;
    if (!cursor) break;
  }
}

// Usage
for await (const batch of fetchWithPagination("https://api.example.com/items")) {
  await processBatch(batch);
}
```

## Webhook Receivers

### Python (FastAPI)
```python
from fastapi import FastAPI, Request, HTTPException
import hmac
import hashlib

app = FastAPI()

@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    # Verify signature
    if not verify_stripe_signature(payload, sig_header):
        raise HTTPException(status_code=400, detail="Invalid signature")

    event = await request.json()

    # Idempotency check
    if await is_processed(event["id"]):
        return {"status": "already_processed"}

    # Process and store
    await store_event(event)
    await mark_processed(event["id"])

    return {"status": "ok"}

def verify_stripe_signature(payload: bytes, sig_header: str) -> bool:
    secret = os.environ["STRIPE_WEBHOOK_SECRET"]
    timestamp, signature = parse_stripe_header(sig_header)

    signed_payload = f"{timestamp}.{payload.decode()}"
    expected = hmac.new(
        secret.encode(),
        signed_payload.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected)
```

### TypeScript (Hono)
```typescript
import { Hono } from "hono";
import { createHmac, timingSafeEqual } from "crypto";

const app = new Hono();

app.post("/webhooks/github", async (c) => {
  const payload = await c.req.text();
  const signature = c.req.header("x-hub-signature-256");

  // Verify
  const expected = `sha256=${createHmac("sha256", process.env.GITHUB_SECRET!)
    .update(payload)
    .digest("hex")}`;

  if (!timingSafeEqual(Buffer.from(signature!), Buffer.from(expected))) {
    return c.json({ error: "Invalid signature" }, 401);
  }

  const event = JSON.parse(payload);
  await db.insert(githubEvents).values({
    eventId: c.req.header("x-github-delivery"),
    eventType: c.req.header("x-github-event"),
    payload: event,
    receivedAt: new Date()
  });

  return c.json({ received: true });
});
```

## GraphQL Subscriptions

### Python (gql)
```python
from gql import Client, gql
from gql.transport.websockets import WebsocketsTransport

transport = WebsocketsTransport(
    url="wss://api.example.com/graphql",
    headers={"Authorization": f"Bearer {token}"}
)

async with Client(transport=transport) as session:
    subscription = gql("""
        subscription {
            orderCreated {
                id
                customer { name }
                items { product quantity }
                total
            }
        }
    """)

    async for result in session.subscribe(subscription):
        await process_order(result["orderCreated"])
```

## Rate Limiting & Backoff

```python
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=60)
)
async def fetch_with_retry(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            await asyncio.sleep(retry_after)
            raise Exception("Rate limited")
        response.raise_for_status()
        return response.json()
```

## Best Practices

1. **Always use idempotency keys** - Prevent duplicate processing
2. **Verify webhook signatures** - Security is critical
3. **Implement cursor-based pagination** - More reliable than offset
4. **Store raw payloads** - Debug and replay capability
5. **Use exponential backoff** - Be a good API citizen
