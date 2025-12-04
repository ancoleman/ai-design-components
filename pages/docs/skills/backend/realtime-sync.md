---
sidebar_position: 8
title: Real-Time Sync
description: Real-time communication patterns for live updates, collaboration, and presence
tags: [backend, realtime, websocket, sse, crdt, collaboration]
---

# Real-Time Sync

Implement real-time communication for live updates, collaboration, and presence awareness across applications.

## When to Use

Use when building:
- **LLM streaming interfaces** - Stream tokens progressively (ai-chat integration)
- **Live dashboards** - Push metrics and updates to clients
- **Collaborative editing** - Multi-user document/spreadsheet editing with CRDTs
- **Chat applications** - Real-time messaging with presence
- **Multiplayer features** - Cursor tracking, live updates, presence awareness
- **Offline-first apps** - Mobile/PWA with sync-on-reconnect

## Multi-Language Support

This skill provides patterns for:
- **Python**: FastAPI WebSocket, sse-starlette, Flask-SocketIO
- **Rust**: axum WebSocket, tokio-tungstenite, axum SSE
- **Go**: gorilla/websocket, nhooyr/websocket, native SSE
- **TypeScript**: ws, Socket.io, Hono WebSocket, EventSource (native)

## Protocol Selection Framework

### Decision Tree

```
ONE-WAY (Server → Client only)
├─ LLM streaming, notifications, live feeds
└─ Use SSE (Server-Sent Events)
   ├─ Automatic reconnection (browser-native)
   ├─ Event IDs for resumption
   └─ Simple HTTP implementation

BIDIRECTIONAL (Client ↔ Server)
├─ Chat, games, collaborative editing
└─ Use WebSocket
   ├─ Manual reconnection required
   ├─ Binary + text support
   └─ Lower latency for two-way

COLLABORATIVE EDITING
├─ Multi-user documents/spreadsheets
└─ Use WebSocket + CRDT (Yjs or Automerge)
   ├─ CRDT handles conflict resolution
   ├─ WebSocket for transport
   └─ Offline-first with sync

PEER-TO-PEER MEDIA
├─ Video, screen sharing, voice calls
└─ Use WebRTC
   ├─ WebSocket for signaling
   ├─ Direct P2P connection
   └─ STUN/TURN for NAT traversal
```

### Protocol Comparison

| Protocol | Direction | Reconnection | Complexity | Best For |
|----------|-----------|--------------|------------|----------|
| SSE | Server → Client | Automatic | Low | Live feeds, LLM streaming |
| WebSocket | Bidirectional | Manual | Medium | Chat, games, collaboration |
| WebRTC | P2P | Complex | High | Video, screen share, voice |

## Implementation Patterns

### Pattern 1: LLM Streaming with SSE

Stream LLM tokens progressively to frontend (ai-chat integration).

**Python (FastAPI):**
```python
from sse_starlette.sse import EventSourceResponse

@app.post("/chat/stream")
async def stream_chat(prompt: str):
    async def generate():
        async for chunk in llm_stream:
            yield {"event": "token", "data": chunk.content}
        yield {"event": "done", "data": "[DONE]"}
    return EventSourceResponse(generate())
```

**Frontend:**
```typescript
const es = new EventSource('/chat/stream')
es.addEventListener('token', (e) => appendToken(e.data))
```

### Pattern 2: WebSocket Chat

Bidirectional communication for chat applications.

**Python (FastAPI):**
```python
connections: set[WebSocket] = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for conn in connections:
                await conn.send_text(data)
    except WebSocketDisconnect:
        connections.remove(websocket)
```

### Pattern 3: Collaborative Editing with CRDTs

Conflict-free multi-user editing using Yjs.

**TypeScript (Yjs):**
```typescript
import * as Y from 'yjs'
import { WebsocketProvider } from 'y-websocket'

const doc = new Y.Doc()
const provider = new WebsocketProvider('ws://localhost:1234', 'doc-id', doc)
const ytext = doc.getText('content')

ytext.observe(event => console.log('Changes:', event.changes))
ytext.insert(0, 'Hello collaborative world!')
```

### Pattern 4: Presence Awareness

Track online users, cursor positions, and typing indicators.

**Yjs Awareness API:**
```typescript
const awareness = provider.awareness
awareness.setLocalState({ user: { name: 'Alice' }, cursor: { x: 100, y: 200 } })
awareness.on('change', () => {
  awareness.getStates().forEach((state, clientId) => {
    renderCursor(state.cursor, state.user)
  })
})
```

### Pattern 5: Offline Sync (Mobile/PWA)

Queue mutations locally and sync when connection restored.

**TypeScript (Yjs + IndexedDB):**
```typescript
import { IndexeddbPersistence } from 'y-indexeddb'
import { WebsocketProvider } from 'y-websocket'

const doc = new Y.Doc()
const indexeddbProvider = new IndexeddbPersistence('my-doc', doc)
const wsProvider = new WebsocketProvider('wss://api.example.com/sync', 'my-doc', doc)

wsProvider.on('status', (e) => {
  console.log(e.status === 'connected' ? 'Online' : 'Offline')
})
```

## Library Recommendations

### Python
- **WebSocket**: websockets 13.x, FastAPI WebSocket, Flask-SocketIO
- **SSE**: sse-starlette, Flask-SSE

### Rust
- **WebSocket**: tokio-tungstenite 0.23, axum WebSocket
- **SSE**: axum SSE

### Go
- **WebSocket**: gorilla/websocket, nhooyr/websocket
- **SSE**: net/http (native, Flusher interface)

### TypeScript
- **WebSocket**: ws, Socket.io 4.x, Hono WebSocket
- **SSE**: EventSource (native browser), Node.js http
- **CRDT**: Yjs (mature, Rust-backed), Automerge (Rust/JS, time-travel)

## Reconnection Strategies

**SSE:** Browser's EventSource handles reconnection automatically with exponential backoff.

**WebSocket:** Implement manual exponential backoff with jitter to prevent thundering herd.

## Security Patterns

**Authentication:** Use cookie-based (same-origin) or token in Sec-WebSocket-Protocol header.

**Rate Limiting:** Implement per-user message throttling with sliding window.

## Scaling with Redis Pub/Sub

For horizontal scaling, use Redis pub/sub to broadcast messages across multiple backend servers.

**Example:**
```python
import redis
redis_client = redis.Redis()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    pubsub = redis_client.pubsub()
    pubsub.subscribe('chat')

    # Broadcast to Redis
    redis_client.publish('chat', message)

    # Receive from Redis and forward to WebSocket
    for message in pubsub.listen():
        await websocket.send_text(message['data'])
```

## Frontend Integration

### React Hooks Pattern

**SSE for LLM Streaming (ai-chat):**
```typescript
useEffect(() => {
  const es = new EventSource(`/api/chat/stream?prompt=${prompt}`)
  es.addEventListener('token', (e) => setContent(prev => prev + e.data))
  return () => es.close()
}, [prompt])
```

**WebSocket for Live Metrics (dashboards):**
```typescript
useEffect(() => {
  const ws = new WebSocket('ws://localhost:8000/metrics')
  ws.onmessage = (e) => setMetrics(JSON.parse(e.data))
  return () => ws.close()
}, [])
```

**Yjs for Collaborative Tables:**
```typescript
useEffect(() => {
  const doc = new Y.Doc()
  const provider = new WebsocketProvider('ws://localhost:1234', docId, doc)
  const yarray = doc.getArray('rows')
  yarray.observe(() => setRows(yarray.toArray()))
  return () => provider.destroy()
}, [docId])
```

## Related Skills

- [AI Chat](../frontend/ai-chat) - LLM streaming interfaces
- [Dashboards](../frontend/dashboards) - Live metrics visualization
- [Message Queues](./message-queues) - Async job status updates via SSE
- [API Patterns](./api-patterns) - WebSocket authentication

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/realtime-sync)
- Yjs: https://docs.yjs.dev/
- Socket.io: https://socket.io/
- WebSocket MDN: https://developer.mozilla.org/en-US/docs/Web/API/WebSocket
- SSE MDN: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
