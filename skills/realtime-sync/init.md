# Real-Time Sync - Master Plan

> **Skill Purpose**: Real-time communication patterns for live updates, collaboration, and presence across Python, Rust, Go, and TypeScript backend implementations.
>
> **Date**: December 2025
> **Status**: Planning Phase
> **Research Sources**: FULL_STACK_SKILLS_UNIFIED.md (Skill 8), WebSocket/SSE protocol specifications, CRDT research (Yjs, Automerge), LLM streaming patterns

---

## Strategic Positioning

### The Gap This Skill Fills

Real-time synchronization is **critical infrastructure** for modern applications, yet implementation varies wildly across ecosystems. This skill provides:

1. **Protocol selection guidance** - SSE vs WebSocket vs WebRTC decision frameworks
2. **Library recommendations** - Production-ready choices for Python, Rust, Go, TypeScript
3. **Pattern implementations** - LLM streaming, collaborative editing, presence
4. **Offline sync strategies** - Mobile-first resilience patterns

### Integration with Frontend Skills

| Frontend Skill | Real-Time Pattern | Backend Implementation |
|----------------|-------------------|------------------------|
| **ai-chat** | LLM streaming responses | SSE with token streaming |
| **dashboards** | Live metrics updates | SSE or WebSocket push |
| **tables** | Collaborative editing | WebSocket + CRDT (Yjs) |
| **drag-drop** | Multi-user presence | WebSocket presence channel |
| **feedback** | Live notifications | SSE notification stream |

### Critical Use Cases

**1. LLM Streaming (AI-Chat Integration)**
```
User Query → Backend → OpenAI/Anthropic → Stream tokens → SSE → Frontend
                                                ↓
                                         Progressive rendering
```

**2. Collaborative Editing (Tables Integration)**
```
User Edit → CRDT Update → WebSocket → Broadcast → Other Users
                    ↓
              Conflict-free merge
```

**3. Live Dashboard Metrics (Dashboards Integration)**
```
Database Change → Trigger → WebSocket/SSE → Frontend Chart Update
```

---

## Transport Protocol Comparison

### Decision Matrix

| Protocol | Direction | Reconnection | Complexity | Best For |
|----------|-----------|--------------|------------|----------|
| **SSE (Server-Sent Events)** | Server → Client only | Automatic (browser-native) | Low | Live feeds, LLM streaming, notifications |
| **WebSocket** | Bidirectional | Manual implementation | Medium | Chat, games, collaborative editing |
| **WebRTC** | Peer-to-peer | Complex (STUN/TURN) | High | Video, screen share, voice |
| **Long Polling** | Client ← Server | Manual | Low | Legacy browser support |

### SSE (Server-Sent Events)

**Strengths:**
- Native browser EventSource API (automatic reconnection)
- HTTP/2 multiplexing (no connection limit)
- Simple server implementation (just HTTP)
- Built-in event IDs for resume-after-disconnect

**Limitations:**
- One-way only (server → client)
- Text-based only (must encode binary as base64)
- No request headers after initial connection

**Ideal Use Cases:**
- ✅ LLM token streaming (ai-chat skill)
- ✅ Live metrics dashboard updates
- ✅ Notification feeds
- ✅ Stock ticker updates
- ❌ Bidirectional chat (use WebSocket)

### WebSocket

**Strengths:**
- Full bidirectional communication
- Binary and text frames
- Lower latency than SSE for two-way
- Protocol upgrade from HTTP

**Limitations:**
- Manual reconnection logic required
- HTTP/1.1 connection limit (6-8 per domain)
- More complex server implementation
- No built-in message replay

**Ideal Use Cases:**
- ✅ Chat applications
- ✅ Multiplayer games
- ✅ Collaborative editing (with CRDT)
- ✅ Real-time cursors/presence
- ❌ One-way feeds (use SSE)

### WebRTC

**Strengths:**
- Peer-to-peer (no server relay)
- Ultra-low latency
- Built-in encryption (DTLS-SRTP)
- Media-optimized

**Limitations:**
- Complex signaling setup
- NAT traversal (STUN/TURN servers)
- Browser-only (no native backend)
- Overkill for text data

**Ideal Use Cases:**
- ✅ Video conferencing
- ✅ Screen sharing
- ✅ Voice calls
- ❌ Text chat (use WebSocket)
- ❌ Metrics streaming (use SSE)

---

## Decision Framework

```
┌─────────────────────────────────────────────────────────────┐
│            Real-Time Transport Selection                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  COMMUNICATION PATTERN?                                      │
│  ├── ONE-WAY: SERVER → CLIENT                                │
│  │   └─ SSE (Server-Sent Events)                             │
│  │       ├─ Use Case: LLM streaming, notifications          │
│  │       ├─ Reconnection: Automatic (browser-native)        │
│  │       └─ Implementation: Simple HTTP endpoint            │
│  │                                                          │
│  ├── BIDIRECTIONAL: CLIENT ↔ SERVER                          │
│  │   └─ WebSocket                                            │
│  │       ├─ Use Case: Chat, games, collaboration            │
│  │       ├─ Reconnection: Manual (implement exponential)    │
│  │       └─ Implementation: Upgrade from HTTP               │
│  │                                                          │
│  ├── COLLABORATIVE EDITING                                   │
│  │   └─ WebSocket + CRDT (Yjs or Automerge)                 │
│  │       ├─ CRDT handles conflict resolution               │
│  │       ├─ WebSocket for transport                         │
│  │       └─ Offline-first with sync                         │
│  │                                                          │
│  ├── VIDEO / SCREEN SHARING                                  │
│  │   └─ WebRTC (peer-to-peer)                                │
│  │       ├─ Signaling: WebSocket for handshake             │
│  │       ├─ Media: Direct P2P connection                    │
│  │       └─ NAT: STUN/TURN servers                          │
│  │                                                          │
│  └── MOBILE / UNRELIABLE CONNECTIONS                         │
│      └─ WebSocket with Offline Queue + Sync                  │
│          ├─ Queue mutations locally                         │
│          ├─ Replay on reconnection                          │
│          └─ Use CRDT for conflict-free merge                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Libraries by Language

### Python

#### WebSocket
| Library | Best For | Key Features |
|---------|----------|--------------|
| **websockets 13.x** | AsyncIO-based servers | Async/await, HTTP/2, production-ready |
| **FastAPI WebSocket** | FastAPI integration | Built-in, dependency injection |
| **Flask-SocketIO** | Flask integration | Socket.IO protocol (fallbacks) |
| **Channels** | Django integration | Redis backend, scaling |

#### SSE
| Library | Best For | Key Features |
|---------|----------|--------------|
| **sse-starlette** | FastAPI/Starlette | Async, generator-based |
| **Flask-SSE** | Flask | Redis backend for pub/sub |
| **aiohttp-sse** | aiohttp | AsyncIO native |

**Python Example (FastAPI SSE for LLM Streaming):**
```python
from fastapi import FastAPI
from sse_starlette.sse import EventSourceResponse
import asyncio

app = FastAPI()

@app.get("/stream")
async def stream_llm_response():
    async def event_generator():
        # Simulating LLM token streaming
        tokens = ["Hello", " ", "world", "!", " ", "How", " ", "can", " ", "I", " ", "help", "?"]
        for token in tokens:
            yield {
                "event": "token",
                "data": token
            }
            await asyncio.sleep(0.05)  # Simulate streaming delay

        yield {
            "event": "done",
            "data": "[DONE]"
        }

    return EventSourceResponse(event_generator())
```

---

### Rust

#### WebSocket
| Library | Best For | Key Features |
|---------|----------|--------------|
| **tokio-tungstenite 0.23** | Async WebSocket | Tokio integration, production-ready |
| **axum WebSocket** | Axum framework | Built-in extractors, tower middleware |
| **actix-web-actors** | Actix Web | Actor model, scaling |
| **warp WebSocket** | Warp framework | Filters-based routing |

#### SSE
| Library | Best For | Key Features |
|---------|----------|--------------|
| **axum SSE** | Axum framework | Native support, async streams |
| **warp SSE** | Warp framework | Filter-based |
| **actix-web SSE** | Actix Web | Chunked encoding |

**Rust Example (Axum WebSocket):**
```rust
use axum::{
    extract::ws::{WebSocket, WebSocketUpgrade},
    response::Response,
    routing::get,
    Router,
};
use futures_util::{SinkExt, StreamExt};

async fn ws_handler(ws: WebSocketUpgrade) -> Response {
    ws.on_upgrade(handle_socket)
}

async fn handle_socket(mut socket: WebSocket) {
    while let Some(Ok(msg)) = socket.recv().await {
        if let axum::extract::ws::Message::Text(text) = msg {
            // Echo back
            if socket.send(axum::extract::ws::Message::Text(text)).await.is_err() {
                break;
            }
        }
    }
}

#[tokio::main]
async fn main() {
    let app = Router::new().route("/ws", get(ws_handler));

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000")
        .await
        .unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

---

### Go

#### WebSocket
| Library | Best For | Key Features |
|---------|----------|--------------|
| **gorilla/websocket** | Production standard | Battle-tested, compression |
| **nhooyr/websocket** | Modern API | Context support, simpler API |
| **gobwas/ws** | High performance | Zero-copy, low-level |

#### SSE
| Library | Best For | Key Features |
|---------|----------|--------------|
| **net/http (native)** | Built-in | Flusher interface, no deps |
| **r3labs/sse** | Pub/sub SSE | Channel-based broadcasting |

**Go Example (gorilla/websocket):**
```go
package main

import (
    "log"
    "net/http"

    "github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
    CheckOrigin: func(r *http.Request) bool {
        return true // Configure CORS properly in production
    },
}

func wsHandler(w http.ResponseWriter, r *http.Request) {
    conn, err := upgrader.Upgrade(w, r, nil)
    if err != nil {
        log.Println(err)
        return
    }
    defer conn.Close()

    for {
        messageType, message, err := conn.ReadMessage()
        if err != nil {
            log.Println("read:", err)
            break
        }

        // Echo back
        err = conn.WriteMessage(messageType, message)
        if err != nil {
            log.Println("write:", err)
            break
        }
    }
}

func main() {
    http.HandleFunc("/ws", wsHandler)
    log.Fatal(http.ListenAndServe(":8080", nil))
}
```

---

### TypeScript

#### WebSocket
| Library | Best For | Key Features |
|---------|----------|--------------|
| **ws** | Native WebSocket server | Lightweight, standard |
| **Socket.io 4.x** | Real-time apps | Auto-reconnect, fallbacks, rooms |
| **Hono WebSocket** | Edge runtime | Works on Cloudflare Workers, Deno |

#### SSE
| Library | Best For | Key Features |
|---------|----------|--------------|
| **EventSource (native)** | Client-side | Browser-native, automatic retry |
| **Node.js http (native)** | Server-side | Built-in, no dependencies |
| **express-sse** | Express | Middleware-based |

**TypeScript Example (Hono SSE for Edge):**
```typescript
import { Hono } from 'hono'
import { streamSSE } from 'hono/streaming'

const app = new Hono()

app.get('/stream', (c) => {
  return streamSSE(c, async (stream) => {
    const tokens = ['Hello', ' ', 'from', ' ', 'edge!']

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

---

## CRDT (Conflict-Free Replicated Data Types)

### Why CRDTs?

Traditional collaborative editing problems:
```
User A: Insert "hello" at position 5
User B: Insert "world" at position 5 (simultaneously)
Result: CONFLICT! 💥
```

With CRDTs:
```
User A: Insert "hello" with unique ID A1
User B: Insert "world" with unique ID B1
Result: Deterministic merge (e.g., "helloworld" or "worldhello" based on ID ordering)
No conflict! ✅
```

### CRDT Libraries

| Library | Language | Best For | Integration |
|---------|----------|----------|-------------|
| **Yjs** | TypeScript/Rust | Text editing, rich text | ProseMirror, Monaco, CodeMirror |
| **Automerge** | Rust/JS | General data structures | Any JSON-like data |
| **Diamond Types** | Rust | High performance text | Custom editors |
| **Loro** | Rust/WASM | Rich text + tree | New, promising |

### Yjs (Primary Recommendation)

**Why Yjs?**
- Mature (2015+), production-tested
- Excellent TypeScript/JavaScript ecosystem
- WASM bindings for Rust backend
- Rich text editing out-of-the-box
- Network-agnostic (works with WebSocket, WebRTC, HTTP)

**Yjs Architecture:**
```
┌─────────────────────────────────────────────────────────────┐
│                    Yjs CRDT Architecture                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Frontend (Browser 1)                                        │
│  ┌────────────────┐                                         │
│  │  Y.Doc         │ ← Shared state                          │
│  │  Y.Text        │ ← Text CRDT                             │
│  │  Y.Array       │ ← Array CRDT                            │
│  │  Y.Map         │ ← Map CRDT                              │
│  └────────┬───────┘                                         │
│           │                                                 │
│           ├─ y-websocket provider                           │
│           │  (syncs over WebSocket)                         │
│           │                                                 │
│  Backend (Rust/Python)                                       │
│  ┌────────┴───────┐                                         │
│  │  y-websocket   │                                         │
│  │  server        │                                         │
│  │  (y-sweet)     │                                         │
│  └────────┬───────┘                                         │
│           │                                                 │
│  Frontend (Browser 2)                                        │
│  ┌────────┴───────┐                                         │
│  │  Y.Doc         │ ← Automatically synced!                │
│  │  Y.Text        │                                         │
│  └────────────────┘                                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Yjs Example (TypeScript):**
```typescript
import * as Y from 'yjs'
import { WebsocketProvider } from 'y-websocket'

// Create shared document
const doc = new Y.Doc()

// WebSocket provider for sync
const provider = new WebsocketProvider(
  'ws://localhost:1234',
  'my-document',
  doc
)

// Shared text type
const ytext = doc.getText('content')

// Listen for changes
ytext.observe(event => {
  console.log('Text changed:', event.changes)
})

// Make changes (will sync to all peers)
ytext.insert(0, 'Hello collaborative world!')
```

**Yjs Backend (y-sweet server - Rust):**
```bash
# Run y-sweet server (Rust-based Yjs WebSocket server)
npx y-sweet serve
# or
docker run -p 1234:1234 ysweet/y-sweet
```

### Automerge (Alternative)

**When to use Automerge over Yjs:**
- Need full Rust implementation (Yjs is TypeScript-first)
- JSON-like data structures (not just text)
- Time-travel / history playback
- Local-first architecture

**Automerge Example (Rust):**
```rust
use automerge::{AutoCommit, transaction::Transactable};

fn main() {
    let mut doc = AutoCommit::new();

    let mut tx = doc.transaction();

    // Create a map
    let map = tx.put_object(automerge::ROOT, "notes", automerge::ObjType::Map).unwrap();

    // Insert text
    tx.put(&map, "title", "Meeting Notes").unwrap();

    tx.commit();

    // Generate binary update
    let changes = doc.get_changes(&[]).unwrap();

    // Send changes over network (WebSocket, HTTP, etc.)
    // Other peers can apply these changes conflict-free
}
```

---

## SSE for LLM Streaming (Critical Pattern)

### Why SSE for LLM?

**OpenAI/Anthropic streaming APIs return SSE format:**
```
data: {"choices": [{"delta": {"content": "Hello"}}]}

data: {"choices": [{"delta": {"content": " world"}}]}

data: [DONE]
```

**Backend must relay this to frontend:**

### Python Implementation (FastAPI → OpenAI)

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
                yield f"data: {content}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
```

### Frontend Integration (EventSource)

```typescript
// Frontend (React + ai-chat skill integration)
const streamResponse = async (prompt: string) => {
  const eventSource = new EventSource(
    `/chat/stream?prompt=${encodeURIComponent(prompt)}`
  )

  eventSource.onmessage = (event) => {
    if (event.data === '[DONE]') {
      eventSource.close()
      return
    }

    // Append token to UI (ai-chat skill pattern)
    appendToken(event.data)
  }

  eventSource.onerror = (error) => {
    console.error('SSE error:', error)
    eventSource.close()
  }
}
```

---

## Offline Sync Pattern (Mobile/PWA)

### Challenge

Mobile apps have unreliable connections. Need to:
1. Queue mutations locally
2. Apply optimistically to UI
3. Sync when connection restored
4. Resolve conflicts

### Solution: Offline Queue + CRDT

**Architecture:**
```
┌─────────────────────────────────────────────────────────────┐
│                Offline-First Sync Pattern                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Mobile Client                                               │
│  ┌──────────────────────────────────┐                       │
│  │  User Action                     │                       │
│  │  (edit text, move card)          │                       │
│  └──────────┬───────────────────────┘                       │
│             ↓                                                │
│  ┌──────────────────────────────────┐                       │
│  │  Local CRDT Update               │                       │
│  │  (Yjs Y.Doc)                     │                       │
│  └──────────┬───────────────────────┘                       │
│             ├─── Apply to UI immediately (optimistic)        │
│             ↓                                                │
│  ┌──────────────────────────────────┐                       │
│  │  Offline Queue                   │                       │
│  │  (IndexedDB)                     │                       │
│  └──────────┬───────────────────────┘                       │
│             │                                                │
│             │ Connection restored?                          │
│             ↓                                                │
│  ┌──────────────────────────────────┐                       │
│  │  Sync Queue → WebSocket          │                       │
│  └──────────┬───────────────────────┘                       │
│             ↓                                                │
│  Backend (CRDT merge)                                        │
│  ┌──────────────────────────────────┐                       │
│  │  Receive updates                 │                       │
│  │  Merge CRDTs (conflict-free)     │                       │
│  │  Broadcast to other clients      │                       │
│  └──────────────────────────────────┘                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Implementation (TypeScript + Yjs + IndexedDB)

```typescript
import * as Y from 'yjs'
import { IndexeddbPersistence } from 'y-indexeddb'
import { WebsocketProvider } from 'y-websocket'

// Create Yjs document
const doc = new Y.Doc()

// Local persistence (IndexedDB)
const indexeddbProvider = new IndexeddbPersistence('my-doc', doc)

// WebSocket provider (auto-reconnects)
const wsProvider = new WebsocketProvider(
  'wss://api.example.com/sync',
  'my-doc',
  doc,
  { connect: true }
)

// Monitor connection status
wsProvider.on('status', (event) => {
  if (event.status === 'connected') {
    console.log('✅ Online - syncing...')
  } else {
    console.log('📴 Offline - queuing locally...')
  }
})

// All changes are automatically:
// 1. Applied to local IndexedDB
// 2. Queued for sync when online
// 3. Conflict-free when merged
```

---

## Presence Patterns

### What is Presence?

Real-time awareness of other users:
- Who's online?
- Cursor positions
- Active selection/focus
- Typing indicators

### Yjs Awareness API

```typescript
import { WebsocketProvider } from 'y-websocket'

const provider = new WebsocketProvider('ws://localhost:1234', 'doc', doc)
const awareness = provider.awareness

// Set local user state
awareness.setLocalState({
  user: {
    name: 'Alice',
    color: '#FF5733'
  },
  cursor: {
    x: 100,
    y: 200
  }
})

// Listen for other users
awareness.on('change', (changes) => {
  // changes.added = array of client IDs that joined
  // changes.updated = array of client IDs that changed state
  // changes.removed = array of client IDs that left

  awareness.getStates().forEach((state, clientId) => {
    if (clientId !== awareness.clientID) {
      // Render other user's cursor
      renderCursor(state.cursor, state.user.name, state.user.color)
    }
  })
})
```

---

## Reconnection Strategies

### SSE Reconnection (Automatic)

Browser's `EventSource` handles reconnection automatically:
- Exponential backoff (1s, 2s, 4s, 8s, max 64s)
- Sends `Last-Event-ID` header to resume from last event
- No code required!

**Server-side resumption support:**
```python
from sse_starlette.sse import EventSourceResponse
from fastapi import Request

@app.get("/stream")
async def stream(request: Request):
    # Get last event ID from header
    last_event_id = request.headers.get("Last-Event-ID")

    async def generate():
        # Resume from last_event_id if provided
        start_from = int(last_event_id) if last_event_id else 0

        for i in range(start_from, 100):
            yield {
                "id": str(i),  # Event ID for resumption
                "event": "message",
                "data": f"Event {i}"
            }

    return EventSourceResponse(generate())
```

### WebSocket Reconnection (Manual)

**Exponential backoff with jitter:**
```typescript
class ReconnectingWebSocket {
  private ws: WebSocket | null = null
  private reconnectAttempts = 0
  private maxReconnectDelay = 30000 // 30 seconds

  connect(url: string) {
    this.ws = new WebSocket(url)

    this.ws.onopen = () => {
      console.log('Connected')
      this.reconnectAttempts = 0
    }

    this.ws.onclose = () => {
      this.reconnect(url)
    }

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }
  }

  private reconnect(url: string) {
    const delay = Math.min(
      1000 * Math.pow(2, this.reconnectAttempts),
      this.maxReconnectDelay
    )

    // Add jitter (0-1000ms) to prevent thundering herd
    const jitter = Math.random() * 1000

    setTimeout(() => {
      console.log(`Reconnecting... (attempt ${this.reconnectAttempts + 1})`)
      this.reconnectAttempts++
      this.connect(url)
    }, delay + jitter)
  }

  send(data: string) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(data)
    } else {
      console.warn('WebSocket not open, queuing message...')
      // Queue message for retry
    }
  }
}
```

---

## Scaling Patterns

### Horizontal Scaling Challenge

With multiple backend servers, WebSocket connections are stateful:

```
User A → Server 1
User B → Server 2

User A sends message → Server 1 → How to reach User B on Server 2?
```

### Solution 1: Redis Pub/Sub

```python
import redis.asyncio as redis
from fastapi import WebSocket

# Redis client
redis_client = redis.from_url("redis://localhost")

# Store active connections per server
connections: set[WebSocket] = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.add(websocket)

    # Subscribe to Redis channel
    pubsub = redis_client.pubsub()
    await pubsub.subscribe("chat")

    async def listen_redis():
        async for message in pubsub.listen():
            if message['type'] == 'message':
                # Broadcast to local connections
                for conn in connections:
                    await conn.send_text(message['data'])

    # Listen in background
    task = asyncio.create_task(listen_redis())

    try:
        while True:
            data = await websocket.receive_text()
            # Publish to Redis (reaches all servers)
            await redis_client.publish("chat", data)
    finally:
        connections.remove(websocket)
        task.cancel()
```

### Solution 2: Sticky Sessions (Load Balancer)

Configure load balancer to route same user to same server:
- Based on session cookie
- Based on IP address (less reliable)
- Based on WebSocket subprotocol

**Nginx example:**
```nginx
upstream websocket_backend {
    ip_hash;  # Sticky sessions based on IP
    server backend1:8080;
    server backend2:8080;
}

server {
    location /ws {
        proxy_pass http://websocket_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

---

## Security Considerations

### Authentication

**WebSocket authentication challenge:**
- No `Authorization` header after upgrade
- Must authenticate during initial HTTP request

**Pattern 1: Token in URL (NOT RECOMMENDED - logs tokens)**
```typescript
const ws = new WebSocket('ws://example.com/ws?token=secret123')
```

**Pattern 2: Token in Sec-WebSocket-Protocol (Better)**
```typescript
// Client
const ws = new WebSocket('ws://example.com/ws', ['access_token', token])

// Server (Python)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Get token from subprotocol
    token = websocket.headers.get("sec-websocket-protocol")
    if not verify_token(token):
        await websocket.close(code=1008)
        return
    await websocket.accept(subprotocol="access_token")
```

**Pattern 3: Cookie-based (Best for same-origin)**
```typescript
// Set HTTP-only cookie first
await fetch('/login', { credentials: 'include' })

// WebSocket will send cookie automatically
const ws = new WebSocket('ws://example.com/ws')
```

### Rate Limiting

Prevent abuse:
```python
from collections import defaultdict
from datetime import datetime, timedelta

# Track messages per user
message_counts = defaultdict(list)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()

    while True:
        data = await websocket.receive_text()

        # Rate limit: 10 messages per minute
        now = datetime.now()
        message_counts[user_id] = [
            ts for ts in message_counts[user_id]
            if now - ts < timedelta(minutes=1)
        ]

        if len(message_counts[user_id]) >= 10:
            await websocket.send_text("Rate limit exceeded")
            continue

        message_counts[user_id].append(now)
        # Process message...
```

---

## Frontend Integration Patterns

### Integration with ai-chat Skill

**SSE streaming for LLM responses:**
```typescript
// ai-chat component
import { useEffect, useState } from 'react'

function ChatMessage({ prompt }: { prompt: string }) {
  const [content, setContent] = useState('')
  const [isDone, setIsDone] = useState(false)

  useEffect(() => {
    const eventSource = new EventSource(`/api/chat/stream?prompt=${prompt}`)

    eventSource.addEventListener('token', (event) => {
      setContent(prev => prev + event.data)
    })

    eventSource.addEventListener('done', () => {
      setIsDone(true)
      eventSource.close()
    })

    return () => eventSource.close()
  }, [prompt])

  return (
    <div className="chat-message">
      {content}
      {!isDone && <span className="cursor">▊</span>}
    </div>
  )
}
```

### Integration with dashboards Skill

**WebSocket for live metric updates:**
```typescript
// Dashboard component
import { useEffect, useState } from 'react'

function LiveMetrics() {
  const [metrics, setMetrics] = useState({ users: 0, revenue: 0 })

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/metrics')

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      setMetrics(data)
    }

    return () => ws.close()
  }, [])

  return (
    <div className="metrics-grid">
      <KPICard label="Active Users" value={metrics.users} />
      <KPICard label="Revenue" value={`$${metrics.revenue}`} />
    </div>
  )
}
```

### Integration with tables Skill

**Yjs collaborative editing:**
```typescript
// Collaborative table component
import * as Y from 'yjs'
import { WebsocketProvider } from 'y-websocket'
import { useEffect, useState } from 'react'

function CollaborativeTable({ documentId }: { documentId: string }) {
  const [rows, setRows] = useState([])
  const [doc] = useState(() => new Y.Doc())

  useEffect(() => {
    const provider = new WebsocketProvider(
      'ws://localhost:1234',
      documentId,
      doc
    )

    const yarray = doc.getArray('rows')

    // Sync Yjs state to React state
    const updateRows = () => {
      setRows(yarray.toArray())
    }

    yarray.observe(updateRows)
    updateRows()

    return () => {
      provider.destroy()
      doc.destroy()
    }
  }, [documentId])

  const addRow = (data: any) => {
    const yarray = doc.getArray('rows')
    yarray.push([data])  // CRDT operation - conflict-free!
  }

  return (
    <table>
      {rows.map((row, i) => (
        <tr key={i}>
          <td>{row.name}</td>
        </tr>
      ))}
    </table>
  )
}
```

---

## Skill Structure

```
skills/realtime-sync/
├── init.md                           # This file - master plan
├── SKILL.md                          # Main skill file (< 500 lines)
├── references/
│   ├── sse-protocol.md               # SSE specification details
│   ├── websocket-protocol.md         # WebSocket specification details
│   ├── yjs-guide.md                  # Complete Yjs integration guide
│   ├── automerge-guide.md            # Automerge patterns
│   ├── scaling-patterns.md           # Redis pub/sub, sticky sessions
│   ├── security-best-practices.md    # Auth, rate limiting, CORS
│   └── reconnection-strategies.md    # Exponential backoff patterns
├── examples/
│   ├── python-fastapi-sse/           # LLM streaming example
│   ├── python-fastapi-websocket/     # Chat example
│   ├── rust-axum-websocket/          # Rust WebSocket server
│   ├── go-gorilla-websocket/         # Go WebSocket server
│   ├── typescript-hono-sse/          # Edge SSE example
│   ├── yjs-collaborative-editor/     # Full Yjs setup
│   └── offline-sync-pwa/             # PWA with IndexedDB queue
├── scripts/
│   ├── benchmark_protocols.py        # SSE vs WebSocket benchmarks
│   ├── test_reconnection.py          # Reconnection logic testing
│   └── validate_crdt_sync.py         # CRDT consistency tests
└── assets/
    ├── protocol-comparison.svg       # Visual protocol comparison
    └── crdt-architecture.svg         # CRDT merge visualization
```

---

## SKILL.md Frontmatter Template

```yaml
---
name: realtime-sync
description: Real-time communication patterns for live updates, collaboration, and presence. Use when building chat applications, collaborative tools, live dashboards, or streaming interfaces (LLM responses, metrics). Covers SSE (server-sent events for one-way streams), WebSocket (bidirectional communication), WebRTC (peer-to-peer video/audio), CRDTs (Yjs, Automerge for conflict-free collaboration), presence patterns (cursors, typing indicators), offline sync (mobile/PWA), and scaling strategies (Redis pub/sub). Supports Python (FastAPI, websockets), Rust (Axum, tokio-tungstenite), Go (gorilla/websocket), and TypeScript (ws, Socket.io, Hono).
---
```

---

## Quality Checklist

Before finalizing SKILL.md:

**Core Requirements:**
- [ ] Description includes WHAT (real-time sync) and WHEN (live updates, collaboration)
- [ ] Decision framework for protocol selection (SSE vs WebSocket vs WebRTC)
- [ ] Multi-language support (Python, Rust, Go, TypeScript)
- [ ] Integration patterns with frontend skills (ai-chat, dashboards, tables)
- [ ] Security best practices (authentication, rate limiting)

**Protocol Coverage:**
- [ ] SSE for one-way streaming (LLM responses, notifications)
- [ ] WebSocket for bidirectional (chat, games)
- [ ] WebRTC for peer-to-peer (video, screen share)
- [ ] CRDT for collaborative editing (Yjs, Automerge)

**Implementation Patterns:**
- [ ] LLM streaming pattern (OpenAI → FastAPI → SSE → Frontend)
- [ ] Collaborative editing pattern (Yjs + WebSocket)
- [ ] Presence pattern (Yjs Awareness API)
- [ ] Offline sync pattern (IndexedDB + CRDT)

**Scaling & Production:**
- [ ] Reconnection strategies (exponential backoff with jitter)
- [ ] Horizontal scaling (Redis pub/sub or sticky sessions)
- [ ] Rate limiting patterns
- [ ] Monitoring & observability integration

**Progressive Disclosure:**
- [ ] SKILL.md under 500 lines
- [ ] References to detailed guides (yjs-guide.md, scaling-patterns.md)
- [ ] Working code examples in examples/
- [ ] Token-free benchmark scripts in scripts/

---

## Research Sources

### Protocol Specifications
- **SSE**: W3C Server-Sent Events specification
- **WebSocket**: RFC 6455 (The WebSocket Protocol)
- **WebRTC**: W3C WebRTC 1.0 specification

### CRDT Research
- **Yjs**: https://docs.yjs.dev/ (production-ready CRDT library)
- **Automerge**: https://automerge.org/ (Rust/WASM CRDT)
- **CRDT Papers**: "Conflict-free Replicated Data Types" (Shapiro et al., 2011)
- **Diamond Types**: https://github.com/josephg/diamond-types (high-performance text CRDT)

### Library Documentation
- **Python websockets**: https://websockets.readthedocs.io/
- **sse-starlette**: https://github.com/sysid/sse-starlette
- **tokio-tungstenite**: https://docs.rs/tokio-tungstenite/
- **gorilla/websocket**: https://pkg.go.dev/github.com/gorilla/websocket
- **Socket.io**: https://socket.io/docs/v4/

### LLM Streaming Patterns
- **OpenAI Streaming**: https://platform.openai.com/docs/api-reference/streaming
- **Anthropic Streaming**: https://docs.anthropic.com/claude/reference/messages-streaming

### Scaling Patterns
- **Redis Pub/Sub**: https://redis.io/docs/manual/pubsub/
- **Nginx WebSocket**: https://nginx.org/en/docs/http/websocket.html

---

## Success Metrics

This skill is successful when:

1. **Protocol Selection Accuracy**: Users choose correct transport (SSE vs WebSocket) 95%+ of time
2. **LLM Streaming Works**: ai-chat skill integrations stream tokens without blocking
3. **Collaborative Editing**: Yjs integration enables conflict-free multi-user editing
4. **Offline Resilience**: Mobile apps queue and sync changes correctly
5. **Production Readiness**: Implementations include auth, rate limiting, reconnection logic

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2025-12-02 | Initial master plan created |

---

*Document generated: December 2025*
*Sources: FULL_STACK_SKILLS_UNIFIED.md (Skill 8), WebSocket/SSE specs, CRDT research*
*Status: Planning Phase - Ready for SKILL.md implementation*
