# WebSocket Reference Guide

WebSocket protocol for bidirectional real-time communication.


## Table of Contents

- [Protocol Overview](#protocol-overview)
- [Authentication Patterns](#authentication-patterns)
  - [Pattern 1: Cookie-Based (Recommended for Same-Origin)](#pattern-1-cookie-based-recommended-for-same-origin)
  - [Pattern 2: Token in Sec-WebSocket-Protocol](#pattern-2-token-in-sec-websocket-protocol)
  - [Pattern 3: First Message Authentication](#pattern-3-first-message-authentication)
- [Heartbeat (Ping/Pong)](#heartbeat-pingpong)
  - [Server-Side Heartbeat (Python)](#server-side-heartbeat-python)
  - [Client-Side Heartbeat (TypeScript)](#client-side-heartbeat-typescript)
- [Message Framing](#message-framing)
  - [Text Frames (JSON)](#text-frames-json)
  - [Binary Frames (Protocol Buffers, MessagePack)](#binary-frames-protocol-buffers-messagepack)
- [Horizontal Scaling](#horizontal-scaling)
  - [Challenge](#challenge)
  - [Solution 1: Redis Pub/Sub](#solution-1-redis-pubsub)
  - [Solution 2: Sticky Sessions (Load Balancer)](#solution-2-sticky-sessions-load-balancer)
- [Connection Limits](#connection-limits)
  - [Browser Limits](#browser-limits)
  - [Server Limits](#server-limits)
- [Error Codes](#error-codes)
- [CORS Configuration](#cors-configuration)
- [Best Practices](#best-practices)

## Protocol Overview

WebSocket provides full-duplex communication over a single TCP connection, upgrading from HTTP.

**Handshake (HTTP → WebSocket):**
```
Client Request:
GET /ws HTTP/1.1
Host: example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13

Server Response:
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

## Authentication Patterns

### Pattern 1: Cookie-Based (Recommended for Same-Origin)

**Flow:**
1. User logs in via HTTP POST
2. Server sets HTTP-only cookie
3. WebSocket connection automatically sends cookie
4. Server validates cookie on connection

**Implementation:**
```python
from fastapi import WebSocket, Cookie, HTTPException

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    session_token: str = Cookie(None)
):
    if not verify_session(session_token):
        await websocket.close(code=1008)  # Policy violation
        return

    await websocket.accept()
    # Connection authenticated
```

**Frontend:**
```typescript
// Cookie set via HTTP login
await fetch('/api/login', {
  method: 'POST',
  credentials: 'include',
  body: JSON.stringify({ username, password })
})

// WebSocket automatically sends cookie
const ws = new WebSocket('ws://example.com/ws')
```

### Pattern 2: Token in Sec-WebSocket-Protocol

**Flow:**
1. Client obtains JWT token
2. Passes token in `Sec-WebSocket-Protocol` header
3. Server validates token during handshake
4. Server responds with same subprotocol

**Implementation:**
```python
from fastapi import WebSocket, HTTPException

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Get token from subprotocol
    protocols = websocket.headers.get("sec-websocket-protocol", "").split(", ")

    token = None
    for proto in protocols:
        if proto.startswith("access_token_"):
            token = proto.replace("access_token_", "")

    if not token or not verify_jwt(token):
        await websocket.close(code=1008)
        return

    await websocket.accept(subprotocol="access_token")
```

**Frontend:**
```typescript
const token = await getAuthToken()
const ws = new WebSocket('ws://example.com/ws', [`access_token_${token}`])
```

### Pattern 3: First Message Authentication

**Flow:**
1. Accept WebSocket connection
2. Wait for authentication message
3. Validate credentials
4. Send confirmation or close

**Implementation:**
```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Wait for auth message (5 second timeout)
    try:
        auth_msg = await asyncio.wait_for(
            websocket.receive_json(),
            timeout=5.0
        )
    except asyncio.TimeoutError:
        await websocket.close(code=1008)
        return

    if auth_msg.get("type") != "auth" or not verify_token(auth_msg.get("token")):
        await websocket.close(code=1008)
        return

    await websocket.send_json({"type": "auth_ok"})
    # Authenticated
```

**Frontend:**
```typescript
const ws = new WebSocket('ws://example.com/ws')

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'auth',
    token: getAuthToken()
  }))
}

ws.onmessage = (event) => {
  const msg = JSON.parse(event.data)
  if (msg.type === 'auth_ok') {
    // Now authenticated
  }
}
```

## Heartbeat (Ping/Pong)

Detect dead connections and prevent timeout.

### Server-Side Heartbeat (Python)

```python
import asyncio
from fastapi import WebSocket

HEARTBEAT_INTERVAL = 30  # seconds

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    async def heartbeat():
        while True:
            try:
                await asyncio.sleep(HEARTBEAT_INTERVAL)
                await websocket.send_json({"type": "ping"})

                # Wait for pong response
                response = await asyncio.wait_for(
                    websocket.receive_json(),
                    timeout=10.0
                )

                if response.get("type") != "pong":
                    raise ValueError("Expected pong")
            except:
                await websocket.close()
                break

    # Start heartbeat task
    heartbeat_task = asyncio.create_task(heartbeat())

    try:
        while True:
            data = await websocket.receive_text()
            # Process messages
    finally:
        heartbeat_task.cancel()
```

### Client-Side Heartbeat (TypeScript)

```typescript
class HeartbeatWebSocket {
  private ws: WebSocket
  private heartbeatInterval: NodeJS.Timeout | null = null

  connect(url: string) {
    this.ws = new WebSocket(url)

    this.ws.onopen = () => {
      this.startHeartbeat()
    }

    this.ws.onmessage = (event) => {
      const msg = JSON.parse(event.data)

      if (msg.type === 'ping') {
        this.ws.send(JSON.stringify({ type: 'pong' }))
      } else {
        this.handleMessage(msg)
      }
    }

    this.ws.onclose = () => {
      this.stopHeartbeat()
    }
  }

  private startHeartbeat() {
    this.heartbeatInterval = setInterval(() => {
      if (this.ws.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify({ type: 'ping' }))
      }
    }, 30000)
  }

  private stopHeartbeat() {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval)
      this.heartbeatInterval = null
    }
  }
}
```

## Message Framing

WebSocket supports text and binary frames.

### Text Frames (JSON)

```python
# Send
await websocket.send_json({
    "type": "message",
    "content": "Hello",
    "timestamp": datetime.now().isoformat()
})

# Receive
data = await websocket.receive_json()
```

### Binary Frames (Protocol Buffers, MessagePack)

```python
import msgpack

# Send
binary_data = msgpack.packb({"user": "alice", "msg": "hello"})
await websocket.send_bytes(binary_data)

# Receive
binary_data = await websocket.receive_bytes()
data = msgpack.unpackb(binary_data)
```

## Horizontal Scaling

### Challenge

WebSocket connections are stateful - user connections on Server A cannot directly reach users on Server B.

```
User A → Server 1
User B → Server 2

User A sends message → Server 1 → ??? → Server 2 → User B
```

### Solution 1: Redis Pub/Sub

Broadcast messages across all servers using Redis.

**Architecture:**
```
Server 1 → Redis Pub/Sub ← Server 2
  ↓                          ↓
User A                     User B
```

**Implementation:**
```python
import redis.asyncio as redis

redis_client = redis.from_url("redis://localhost:6379")

class ConnectionManager:
    def __init__(self):
        self.active_connections: set[WebSocket] = set()
        self.pubsub = None

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

        # Start listening to Redis
        if not self.pubsub:
            self.pubsub = redis_client.pubsub()
            await self.pubsub.subscribe("broadcast")
            asyncio.create_task(self._listen_redis())

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        # Publish to Redis (reaches ALL servers)
        await redis_client.publish("broadcast", message)

    async def _listen_redis(self):
        """Listen to Redis and broadcast to local connections"""
        async for message in self.pubsub.listen():
            if message['type'] == 'message':
                await self._send_to_local(message['data'])

    async def _send_to_local(self, message: str):
        """Send to local connections only"""
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                await self.disconnect(connection)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast via Redis to ALL servers
            await manager.broadcast(data)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
```

### Solution 2: Sticky Sessions (Load Balancer)

Route same user to same server using load balancer.

**Nginx Configuration:**
```nginx
upstream websocket_backend {
    # Sticky sessions based on client IP
    ip_hash;

    server backend1:8080;
    server backend2:8080;
    server backend3:8080;
}

server {
    listen 80;

    location /ws {
        proxy_pass http://websocket_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 86400;  # 24 hours
    }
}
```

**HAProxy Configuration:**
```
backend websocket_backend
    balance source  # Hash based on source IP
    hash-type consistent

    server backend1 10.0.1.1:8080 check
    server backend2 10.0.1.2:8080 check
    server backend3 10.0.1.3:8080 check
```

**Pros:**
- Simple - no Redis dependency
- No broadcast needed (users on same server)

**Cons:**
- Users can't communicate across servers
- Uneven load distribution
- Reconnection may hit different server

## Connection Limits

### Browser Limits

Browsers limit concurrent connections per domain:
- HTTP/1.1: 6-8 connections
- WebSocket: Typically 200-255 per domain

**Workaround: Use subdomains**
```typescript
const ws1 = new WebSocket('ws://ws1.example.com/ws')
const ws2 = new WebSocket('ws://ws2.example.com/ws')
const ws3 = new WebSocket('ws://ws3.example.com/ws')
```

### Server Limits

**File Descriptor Limits:**
```bash
# Check current limit
ulimit -n

# Set higher limit
ulimit -n 65536

# Or in /etc/security/limits.conf:
* soft nofile 65536
* hard nofile 65536
```

**Per-Process Connection Limits:**
- Python (asyncio): ~10,000+ connections per process
- Rust (tokio): ~100,000+ connections per process
- Go: ~1,000,000+ connections (goroutines)

## Error Codes

Common WebSocket close codes:

| Code | Meaning | When to Use |
|------|---------|-------------|
| 1000 | Normal closure | Clean shutdown |
| 1001 | Going away | Server restart, browser navigation |
| 1002 | Protocol error | Invalid message format |
| 1003 | Unsupported data | Wrong data type |
| 1008 | Policy violation | Authentication failed |
| 1011 | Unexpected condition | Server error |

**Implementation:**
```python
# Normal close
await websocket.close(code=1000, reason="Goodbye")

# Authentication failed
await websocket.close(code=1008, reason="Unauthorized")

# Server error
await websocket.close(code=1011, reason="Internal error")
```

## CORS Configuration

WebSocket upgrade requests include Origin header.

**Python (FastAPI):**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Check origin manually if needed
    origin = websocket.headers.get("origin")
    if origin not in ["https://example.com", "https://app.example.com"]:
        await websocket.close(code=1008)
        return

    await websocket.accept()
```

**Go (gorilla/websocket):**
```go
var upgrader = websocket.Upgrader{
    CheckOrigin: func(r *http.Request) bool {
        origin := r.Header.Get("Origin")
        return origin == "https://example.com" ||
               origin == "https://app.example.com"
    },
}
```

## Best Practices

1. **Always validate authentication** during handshake
2. **Implement heartbeat** to detect dead connections
3. **Use exponential backoff** for reconnection (client-side)
4. **Rate limit** messages per connection
5. **Close connections gracefully** with appropriate codes
6. **Monitor connection count** and set alerts
7. **Use Redis pub/sub** for horizontal scaling
8. **Configure CORS** explicitly for security
9. **Set timeouts** for read/write operations
10. **Log errors** with connection metadata for debugging
