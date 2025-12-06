# Session Persistence Strategies

Comprehensive guide to managing sessions in load-balanced environments.


## Table of Contents

- [Sticky Sessions (Avoid When Possible)](#sticky-sessions-avoid-when-possible)
  - [Cookie-Based Stickiness](#cookie-based-stickiness)
  - [IP Hash Stickiness](#ip-hash-stickiness)
  - [Drawbacks](#drawbacks)
- [Shared Session Store (Recommended)](#shared-session-store-recommended)
  - [Redis Session Store](#redis-session-store)
  - [Benefits](#benefits)
- [Client-Side Tokens (Best for APIs)](#client-side-tokens-best-for-apis)
  - [JWT (JSON Web Tokens)](#jwt-json-web-tokens)
  - [Benefits](#benefits)
- [Session Replication](#session-replication)
- [Migration Strategy](#migration-strategy)
- [Summary](#summary)

## Sticky Sessions (Avoid When Possible)

### Cookie-Based Stickiness

Load balancer sets cookie to track server affinity.

**NGINX Plus:**
```nginx
upstream backend {
    sticky cookie srv_id expires=1h domain=.example.com path=/;
    server backend1:8080;
    server backend2:8080;
}
```

**HAProxy:**
```haproxy
backend web_servers
    cookie SERVERID insert indirect nocache
    server web1 192.168.1.101:8080 check cookie web1
    server web2 192.168.1.102:8080 check cookie web2
```

**AWS ALB:**
```hcl
resource "aws_lb_target_group" "app" {
  stickiness {
    type            = "lb_cookie"
    cookie_duration = 86400
    enabled         = true
  }
}
```

### IP Hash Stickiness

Hash client IP to select backend server.

**NGINX:**
```nginx
upstream backend {
    ip_hash;
    server backend1:8080;
    server backend2:8080;
}
```

**HAProxy:**
```haproxy
backend web_servers
    balance source
    hash-type consistent
    server web1 192.168.1.101:8080
    server web2 192.168.1.102:8080
```

### Drawbacks

- Uneven load distribution
- Session lost on server failure
- Complicates horizontal scaling
- Reduces load balancing effectiveness

## Shared Session Store (Recommended)

Stateless application servers with centralized session storage.

### Redis Session Store

**Node.js/Express:**
```javascript
const session = require('express-session');
const RedisStore = require('connect-redis').default;
const { createClient } = require('redis');

const redisClient = createClient({
  host: 'redis.example.com',
  port: 6379
});

app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: 'session-secret',
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: true,
    httpOnly: true,
    maxAge: 3600000
  }
}));
```

**Python/Flask:**
```python
from flask import Flask, session
from redis import Redis

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = Redis(host='redis.example.com', port=6379)
```

### Benefits

- No sticky sessions needed
- True load balancing
- Server failures don't lose sessions
- Horizontal scaling trivial
- Consistent user experience

## Client-Side Tokens (Best for APIs)

### JWT (JSON Web Tokens)

**Server generates token:**
```javascript
const jwt = require('jsonwebtoken');

function login(user) {
  const token = jwt.sign(
    { userId: user.id, role: user.role },
    process.env.JWT_SECRET,
    { expiresIn: '1h' }
  );
  return { token };
}
```

**Client sends token with requests:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**Server validates (stateless):**
```javascript
function authenticate(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (err) {
    res.status(401).json({ error: 'Invalid token' });
  }
}
```

### Benefits

- Fully stateless servers
- Perfect load balancing
- No session storage needed
- Horizontal scaling effortless

## Session Replication

For applications that must use server-side sessions, replicate across instances.

**Memcached replication:**
- Use consistent hashing
- Replicate to multiple nodes
- Accept eventual consistency

**Database-backed sessions:**
- Store sessions in shared database
- Less performant than Redis
- Simpler for small deployments

## Migration Strategy

Moving from sticky sessions to stateless:

1. **Add shared session store** (Redis)
2. **Configure dual-write** (local + Redis)
3. **Test failover** behavior
4. **Switch to Redis-only** sessions
5. **Remove sticky session** configuration
6. **Monitor** session loss rates

## Summary

Prefer stateless architecture with client-side tokens (JWT) for APIs. Use shared session store (Redis) for web applications. Avoid sticky sessions unless absolutely necessary. When using sticky sessions, implement session replication for high availability.
