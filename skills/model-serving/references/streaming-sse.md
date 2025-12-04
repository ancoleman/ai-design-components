# Server-Sent Events (SSE) for LLM Streaming

Complete guide for streaming LLM responses using Server-Sent Events (SSE) across multiple backends.

## Why SSE for LLM Streaming

**Advantages over WebSockets:**
- Simpler protocol (HTTP, not bidirectional)
- Automatic reconnection (browser handles it)
- Built-in event IDs for resumption
- Standard HTTP infrastructure (proxies, load balancers work)

**Use case:** Streaming LLM tokens progressively to frontend (ai-chat skill integration).

## Protocol Overview

**SSE format:**
```
data: First chunk of text\n\n
data: Second chunk\n\n
data: {"token": "word", "done": false}\n\n
data: [DONE]\n\n
```

**Key points:**
- Each message starts with `data: `
- Messages end with double newline (`\n\n`)
- Can send JSON or plain text
- Client auto-reconnects on disconnect

---

## Python + FastAPI

### Basic Implementation

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
import asyncio

app = FastAPI()

async def generate_tokens():
    """Simulate LLM streaming"""
    tokens = ["Hello", " there!", " How", " can", " I", " help", " you", " today", "?"]

    for token in tokens:
        yield {
            "event": "message",
            "data": token
        }
        await asyncio.sleep(0.1)  # Simulate model latency

    yield {
        "event": "done",
        "data": "[DONE]"
    }

@app.post("/chat/stream")
async def stream_chat():
    return EventSourceResponse(generate_tokens())
```

### OpenAI-Compatible vLLM Streaming

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from openai import OpenAI
import json

app = FastAPI()
client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")

@app.post("/chat/stream")
async def stream_chat(prompt: str):
    async def generate():
        stream = client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            max_tokens=512,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                token = chunk.choices[0].delta.content
                # SSE format
                yield f"data: {json.dumps({'token': token})}\n\n"

        yield f"data: {json.dumps({'done': True})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        },
    )
```

---

## TypeScript + Hono (Edge)

### Cloudflare Workers

```typescript
import { Hono } from 'hono';
import { streamSSE } from 'hono/streaming';

const app = new Hono();

app.post('/chat/stream', async (c) => {
  const { prompt } = await c.req.json();

  return streamSSE(c, async (stream) => {
    const tokens = prompt.split(' ');

    for (const token of tokens) {
      await stream.writeSSE({
        data: JSON.stringify({ token: token + ' ' }),
        event: 'message',
      });
      await stream.sleep(100);
    }

    await stream.writeSSE({
      data: JSON.stringify({ done: true }),
      event: 'done',
    });
  });
});

export default app;
```

---

## Rust + Axum

```rust
use axum::{
    response::sse::{Event, Sse},
    routing::post,
    Json, Router,
};
use futures::stream::{self, Stream};
use serde::{Deserialize, Serialize};
use std::convert::Infallible;
use std::time::Duration;
use tokio::time::sleep;

#[derive(Deserialize)]
struct ChatRequest {
    prompt: String,
}

#[derive(Serialize)]
struct TokenResponse {
    token: String,
    done: bool,
}

async fn stream_chat(
    Json(payload): Json<ChatRequest>,
) -> Sse<impl Stream<Item = Result<Event, Infallible>>> {
    let tokens: Vec<String> = payload.prompt.split_whitespace()
        .map(|s| s.to_string())
        .collect();

    let stream = stream::iter(tokens)
        .then(|token| async move {
            sleep(Duration::from_millis(100)).await;

            let response = TokenResponse {
                token: format!("{} ", token),
                done: false,
            };

            Ok::<_, Infallible>(
                Event::default()
                    .event("message")
                    .json_data(response)
                    .unwrap()
            )
        });

    Sse::new(stream)
        .keep_alive(axum::response::sse::KeepAlive::default())
}

#[tokio::main]
async fn main() {
    let app = Router::new().route("/chat/stream", post(stream_chat));

    axum::Server::bind(&"0.0.0.0:3000".parse().unwrap())
        .serve(app.into_make_service())
        .await
        .unwrap();
}
```

---

## Frontend Integration

### React + EventSource (Native)

```typescript
import { useState, useEffect } from 'react';

export function useStreamingChat() {
  const [response, setResponse] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);

  const sendMessage = async (prompt: string) => {
    setResponse('');
    setIsStreaming(true);

    const es = new EventSource(`/chat/stream?prompt=${encodeURIComponent(prompt)}`);

    es.addEventListener('message', (e) => {
      const data = JSON.parse(e.data);
      if (data.token) {
        setResponse((prev) => prev + data.token);
      }
    });

    es.addEventListener('done', () => {
      setIsStreaming(false);
      es.close();
    });

    es.onerror = () => {
      setIsStreaming(false);
      es.close();
    };
  };

  return { response, isStreaming, sendMessage };
}

// Usage
function ChatComponent() {
  const { response, isStreaming, sendMessage } = useStreamingChat();

  return (
    <div>
      <button onClick={() => sendMessage('Hello AI!')}>
        Send
      </button>
      <div>{response}</div>
      {isStreaming && <span>...</span>}
    </div>
  );
}
```

### Fetch API (POST with SSE)

```typescript
async function streamChat(prompt: string) {
  const response = await fetch('/chat/stream', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt }),
  });

  const reader = response.body!.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    const lines = chunk.split('\n\n');

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = JSON.parse(line.slice(6));

        if (data.token) {
          appendToken(data.token);
        }

        if (data.done) {
          return;
        }
      }
    }
  }
}
```

---

## Advanced Patterns

### Reconnection with Event ID

```python
from fastapi import Request
from sse_starlette.sse import EventSourceResponse

@app.post("/chat/stream")
async def stream_chat(request: Request):
    last_event_id = request.headers.get("Last-Event-ID", "0")
    start_index = int(last_event_id)

    async def generate():
        tokens = get_all_tokens()  # Get full token list

        for i, token in enumerate(tokens[start_index:], start=start_index):
            yield {
                "id": str(i + 1),  # Event ID for resumption
                "event": "message",
                "data": token
            }

    return EventSourceResponse(generate())
```

**Frontend auto-reconnection:**
```typescript
const es = new EventSource('/chat/stream');

// Browser automatically sends Last-Event-ID header on reconnect
es.addEventListener('message', (e) => {
  console.log('Last ID:', e.lastEventId);  // Automatically tracked
});
```

### Error Handling

```python
@app.post("/chat/stream")
async def stream_chat():
    async def generate():
        try:
            # LLM streaming logic
            for token in llm_stream:
                yield {"data": token}
        except Exception as e:
            yield {
                "event": "error",
                "data": json.dumps({"error": str(e)})
            }

    return EventSourceResponse(generate())
```

---

## Production Considerations

### Nginx Configuration

```nginx
# Disable buffering for SSE
location /chat/stream {
    proxy_pass http://backend;
    proxy_buffering off;
    proxy_cache off;
    proxy_set_header Connection '';
    proxy_http_version 1.1;
    chunked_transfer_encoding off;
}
```

### Load Balancing

**Sticky sessions required:**
```yaml
# Kubernetes ingress annotation
nginx.ingress.kubernetes.io/affinity: "cookie"
nginx.ingress.kubernetes.io/session-cookie-name: "route"
```

### Timeouts

```python
# Set appropriate timeouts
EventSourceResponse(
    generate(),
    ping_interval=15,  # Send keep-alive every 15s
)
```

---

## Comparison with Alternatives

| Protocol | Direction | Reconnection | Complexity | Best For |
|----------|-----------|--------------|------------|----------|
| **SSE** | Server→Client | Automatic | Low | LLM streaming, live updates |
| **WebSocket** | Bidirectional | Manual | Medium | Chat, games, real-time collab |
| **HTTP Streaming** | Server→Client | Manual | Medium | Video/audio streaming |

---

## Common Pitfalls

**Buffer issues:**
```python
# ❌ Don't do this (buffered)
return Response(generate(), media_type="text/event-stream")

# ✅ Do this (streaming)
return EventSourceResponse(generate())
```

**Missing headers:**
```python
# Required headers for SSE
headers = {
    "Cache-Control": "no-cache",
    "X-Accel-Buffering": "no",  # Disable nginx buffering
    "Connection": "keep-alive",
}
```

---

## Resources

- MDN SSE Docs: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
- sse-starlette: https://github.com/sysid/sse-starlette
- Hono Streaming: https://hono.dev/helpers/streaming
