# Server-Sent Events (SSE) Reference Guide

SSE provides one-way server-to-client event streaming over HTTP.

## Protocol Overview

SSE is a simple text-based protocol for pushing events from server to client.

**HTTP Request:**
```
GET /stream HTTP/1.1
Host: example.com
Accept: text/event-stream
Cache-Control: no-cache
```

**HTTP Response:**
```
HTTP/1.1 200 OK
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive

data: Hello world

data: Multi-line
data: message

event: custom
data: Custom event

id: 123
data: Event with ID
```

## SSE Message Format

### Basic Message
```
data: This is a message

```
Note: Two newlines (`\n\n`) terminate each message.

### Multi-Line Message
```
data: Line 1
data: Line 2
data: Line 3

```

### Event Type
```
event: notification
data: You have a new message

```

### Event ID (for resumption)
```
id: 42
data: This event can be resumed

```

### Combined
```
id: 100
event: update
data: {"user": "alice", "action": "joined"}
retry: 10000

```

## Automatic Reconnection

Browser's EventSource automatically reconnects with exponential backoff.

**Default Behavior:**
- Initial reconnect: ~1 second
- Subsequent: exponential backoff (2s, 4s, 8s, 16s, 32s)
- Max delay: ~64 seconds
- Browser sends `Last-Event-ID` header on reconnect

**Server-Side Resumption:**
```python
from sse_starlette.sse import EventSourceResponse
from fastapi import Request

@app.get("/stream")
async def stream(request: Request):
    # Get last event ID from header
    last_event_id = request.headers.get("Last-Event-ID")

    async def generate():
        # Resume from last received event
        start_from = int(last_event_id) if last_event_id else 0

        for i in range(start_from, 1000):
            yield {
                "id": str(i),          # Include ID for resumption
                "event": "message",
                "data": f"Event {i}"
            }

    return EventSourceResponse(generate())
```

## Custom Retry Interval

Override browser's reconnection delay:

```python
async def generate():
    # First event sets retry interval
    yield {
        "retry": 5000,  # 5 seconds
        "data": "Connected"
    }

    for i in range(100):
        yield {
            "data": f"Message {i}"
        }
```

**Protocol:**
```
retry: 5000

data: Connected

data: Message 0

data: Message 1

```

## LLM Streaming Pattern

Stream LLM tokens progressively to frontend.

### OpenAI/Anthropic Relay

**Python (FastAPI → OpenAI):**
```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI
import os

app = FastAPI()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/chat/stream")
async def stream_chat(prompt: str):
    async def generate():
        stream = await client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content

                # SSE format
                yield f"event: token\n"
                yield f"data: {content}\n\n"

        # Done signal
        yield f"event: done\n"
        yield f"data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable Nginx buffering
        }
    )
```

**Python (FastAPI → Anthropic):**
```python
from anthropic import AsyncAnthropic

client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@app.post("/chat/stream")
async def stream_chat(prompt: str):
    async def generate():
        async with client.messages.stream(
            model="claude-3-5-sonnet-20241022",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024
        ) as stream:
            async for text in stream.text_stream:
                yield f"event: token\n"
                yield f"data: {text}\n\n"

        yield f"event: done\n"
        yield f"data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
```

### Frontend Integration

**EventSource API (Browser):**
```typescript
function streamLLMResponse(prompt: string) {
  const eventSource = new EventSource(
    `/chat/stream?prompt=${encodeURIComponent(prompt)}`
  )

  eventSource.addEventListener('token', (event) => {
    const token = event.data
    appendToMessage(token)  // Progressive rendering
  })

  eventSource.addEventListener('done', () => {
    eventSource.close()
    markComplete()
  })

  eventSource.onerror = (error) => {
    console.error('SSE error:', error)
    eventSource.close()
    handleError()
  }
}
```

**React Hook:**
```typescript
import { useEffect, useState } from 'react'

function useSSEStream(url: string) {
  const [data, setData] = useState('')
  const [isDone, setIsDone] = useState(false)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    const eventSource = new EventSource(url)

    eventSource.addEventListener('token', (event) => {
      setData(prev => prev + event.data)
    })

    eventSource.addEventListener('done', () => {
      setIsDone(true)
      eventSource.close()
    })

    eventSource.onerror = (err) => {
      setError(new Error('Stream error'))
      eventSource.close()
    }

    return () => {
      eventSource.close()
    }
  }, [url])

  return { data, isDone, error }
}

// Usage
function ChatMessage({ prompt }: { prompt: string }) {
  const { data, isDone, error } = useSSEStream(`/chat/stream?prompt=${prompt}`)

  if (error) return <div>Error: {error.message}</div>

  return (
    <div className="chat-message">
      {data}
      {!isDone && <span className="cursor">▊</span>}
    </div>
  )
}
```

## Edge Runtime Support

### Hono (Cloudflare Workers, Deno)

```typescript
import { Hono } from 'hono'
import { streamSSE } from 'hono/streaming'

const app = new Hono()

app.get('/stream', (c) => {
  return streamSSE(c, async (stream) => {
    const tokens = ['Hello', ' ', 'from', ' ', 'the', ' ', 'edge!']

    for (const token of tokens) {
      await stream.writeSSE({
        event: 'token',
        data: token,
      })
      await stream.sleep(100)
    }

    await stream.writeSSE({
      event: 'done',
      data: '[DONE]',
    })
  })
})

export default app
```

### Next.js Edge Runtime

```typescript
// app/api/stream/route.ts
export const runtime = 'edge'

export async function GET(request: Request) {
  const encoder = new TextEncoder()

  const stream = new ReadableStream({
    async start(controller) {
      const tokens = ['Hello', ' ', 'Next.js', ' ', 'Edge!']

      for (const token of tokens) {
        controller.enqueue(
          encoder.encode(`event: token\ndata: ${token}\n\n`)
        )
        await new Promise(resolve => setTimeout(resolve, 100))
      }

      controller.enqueue(
        encoder.encode(`event: done\ndata: [DONE]\n\n`)
      )
      controller.close()
    }
  })

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    }
  })
}
```

## Live Metrics Dashboard

Push real-time metrics to dashboard.

**Backend (Python):**
```python
import asyncio
from datetime import datetime

@app.get("/metrics")
async def stream_metrics():
    async def generate():
        while True:
            # Fetch current metrics
            metrics = {
                "active_users": get_active_users(),
                "revenue": get_current_revenue(),
                "timestamp": datetime.now().isoformat()
            }

            yield {
                "event": "metrics",
                "data": json.dumps(metrics)
            }

            await asyncio.sleep(5)  # Update every 5 seconds

    return EventSourceResponse(generate())
```

**Frontend (React):**
```typescript
import { useEffect, useState } from 'react'

function LiveDashboard() {
  const [metrics, setMetrics] = useState({
    active_users: 0,
    revenue: 0
  })

  useEffect(() => {
    const eventSource = new EventSource('/metrics')

    eventSource.addEventListener('metrics', (event) => {
      const data = JSON.parse(event.data)
      setMetrics(data)
    })

    return () => eventSource.close()
  }, [])

  return (
    <div>
      <KPICard label="Active Users" value={metrics.active_users} />
      <KPICard label="Revenue" value={`$${metrics.revenue}`} />
    </div>
  )
}
```

## Notification Feed

Push notifications to users.

**Backend (Python with Redis Pub/Sub):**
```python
import redis.asyncio as redis

redis_client = redis.from_url("redis://localhost")

@app.get("/notifications/{user_id}")
async def stream_notifications(user_id: str):
    async def generate():
        pubsub = redis_client.pubsub()
        await pubsub.subscribe(f"notifications:{user_id}")

        async for message in pubsub.listen():
            if message['type'] == 'message':
                yield {
                    "event": "notification",
                    "data": message['data']
                }

    return EventSourceResponse(generate())

# Publish notification
@app.post("/notify/{user_id}")
async def notify_user(user_id: str, message: str):
    await redis_client.publish(
        f"notifications:{user_id}",
        json.dumps({"message": message, "timestamp": datetime.now().isoformat()})
    )
    return {"status": "sent"}
```

**Frontend:**
```typescript
function NotificationCenter({ userId }: { userId: string }) {
  const [notifications, setNotifications] = useState([])

  useEffect(() => {
    const eventSource = new EventSource(`/notifications/${userId}`)

    eventSource.addEventListener('notification', (event) => {
      const notification = JSON.parse(event.data)
      setNotifications(prev => [notification, ...prev])
    })

    return () => eventSource.close()
  }, [userId])

  return (
    <div>
      {notifications.map((notif, i) => (
        <Notification key={i} {...notif} />
      ))}
    </div>
  )
}
```

## Authentication

SSE uses standard HTTP, so authentication follows HTTP patterns.

### Cookie-Based

```python
from fastapi import Request, HTTPException

@app.get("/stream")
async def stream(request: Request):
    # Validate session cookie
    session_token = request.cookies.get("session_token")
    if not verify_session(session_token):
        raise HTTPException(status_code=401, detail="Unauthorized")

    async def generate():
        yield {"data": "Authenticated stream"}

    return EventSourceResponse(generate())
```

### Bearer Token

```typescript
// Frontend - pass token in URL (NOT recommended - use POST)
const eventSource = new EventSource(`/stream?token=${token}`)

// Better: Use POST with Authorization header (requires EventSource polyfill)
import { EventSourcePolyfill } from 'event-source-polyfill'

const eventSource = new EventSourcePolyfill('/stream', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
})
```

**Backend:**
```python
from fastapi import Header, HTTPException

@app.get("/stream")
async def stream(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401)

    token = authorization.replace("Bearer ", "")
    if not verify_jwt(token):
        raise HTTPException(status_code=401)

    async def generate():
        yield {"data": "Authenticated stream"}

    return EventSourceResponse(generate())
```

## Compression

Enable gzip compression for SSE responses.

**Nginx:**
```nginx
http {
    gzip on;
    gzip_types text/event-stream;

    server {
        location /stream {
            proxy_pass http://backend;
            proxy_set_header Connection '';
            proxy_http_version 1.1;
            chunked_transfer_encoding off;
            proxy_buffering off;
            proxy_cache off;
        }
    }
}
```

**Python (FastAPI with gzip):**
```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

## Browser Compatibility

**Supported:**
- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- Opera: ✅ Full support

**Not Supported:**
- Internet Explorer: ❌ No support (use polyfill or WebSocket fallback)

**Polyfill:**
```typescript
import { EventSourcePolyfill } from 'event-source-polyfill'

// Use polyfill with custom headers
const eventSource = new EventSourcePolyfill('/stream', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
})
```

## Limitations

1. **One-way only** - Server → Client (no client → server messages)
2. **Text-based** - Binary data must be base64 encoded
3. **No request headers** - Can't add headers after initial connection (without polyfill)
4. **HTTP/1.1 connection limit** - 6-8 connections per domain (use HTTP/2)
5. **Browser limit** - ~255 EventSource connections per domain

## Best Practices

1. **Include event IDs** for automatic resumption
2. **Set retry interval** explicitly for predictable behavior
3. **Use HTTP/2** to avoid connection limits
4. **Disable buffering** in reverse proxies (Nginx, Apache)
5. **Send heartbeat** every 30-60 seconds to keep connection alive
6. **Close streams** when no longer needed to free resources
7. **Handle errors** gracefully with automatic reconnection
8. **Use compression** for large payloads
9. **Monitor connection count** and set limits
10. **Test with slow networks** to ensure proper buffering
