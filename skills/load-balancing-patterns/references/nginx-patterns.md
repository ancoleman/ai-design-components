# NGINX Load Balancing Patterns

Complete guide to NGINX and NGINX Plus load balancing configurations.


## Table of Contents

- [Basic HTTP Load Balancing](#basic-http-load-balancing)
  - [Upstream Configuration](#upstream-configuration)
  - [Load Balancing Algorithms](#load-balancing-algorithms)
- [Server Parameters](#server-parameters)
- [Health Checks](#health-checks)
  - [Passive Health Checks (Open Source)](#passive-health-checks-open-source)
  - [Active Health Checks (NGINX Plus)](#active-health-checks-nginx-plus)
- [Sticky Sessions (NGINX Plus)](#sticky-sessions-nginx-plus)
  - [Cookie-Based](#cookie-based)
  - [Learn from Application Cookie](#learn-from-application-cookie)
- [TCP/UDP Stream Load Balancing](#tcpudp-stream-load-balancing)
- [SSL/TLS Termination](#ssltls-termination)
- [Advanced Patterns](#advanced-patterns)
  - [Slow Start (NGINX Plus)](#slow-start-nginx-plus)
  - [Connection Limits](#connection-limits)
  - [Error Handling](#error-handling)
- [Complete Configuration Example](#complete-configuration-example)

## Basic HTTP Load Balancing

### Upstream Configuration

```nginx
upstream backend {
    # Algorithm: round-robin (default)
    # Alternatives: least_conn, ip_hash, hash, random

    server backend1.example.com:8080;
    server backend2.example.com:8080;
    server backend3.example.com:8080;

    # Keepalive connections
    keepalive 32;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
    }
}
```

### Load Balancing Algorithms

**Round Robin (default):**
```nginx
upstream backend {
    server backend1:8080;
    server backend2:8080;
}
```

**Least Connections:**
```nginx
upstream backend {
    least_conn;
    server backend1:8080;
    server backend2:8080;
}
```

**IP Hash (sticky sessions):**
```nginx
upstream backend {
    ip_hash;
    server backend1:8080;
    server backend2:8080;
}
```

**Hash (custom key):**
```nginx
upstream backend {
    hash $request_uri consistent;
    server backend1:8080;
    server backend2:8080;
}
```

**Random:**
```nginx
upstream backend {
    random two least_conn;
    server backend1:8080;
    server backend2:8080;
}
```

## Server Parameters

```nginx
upstream backend {
    server backend1:8080 weight=3 max_fails=3 fail_timeout=30s;
    server backend2:8080 weight=2 max_fails=3 fail_timeout=30s;
    server backend3:8080 backup;
    server backend4:8080 down;
}
```

**Parameters:**
- `weight=n`: Server weight (default: 1)
- `max_fails=n`: Failed attempts before marking server down
- `fail_timeout=time`: Time server marked down after max_fails
- `backup`: Backup server (used when primaries unavailable)
- `down`: Permanently mark server as unavailable

## Health Checks

### Passive Health Checks (Open Source)

```nginx
upstream backend {
    server backend1:8080 max_fails=3 fail_timeout=30s;
    server backend2:8080 max_fails=3 fail_timeout=30s;
}
```

### Active Health Checks (NGINX Plus)

```nginx
upstream backend {
    zone backend 64k;
    server backend1:8080;
    server backend2:8080;
}

match server_ok {
    status 200-399;
    header Content-Type = "application/json";
    body ~ "\"status\":\"healthy\"";
}

server {
    location / {
        proxy_pass http://backend;
        health_check interval=5s fails=3 passes=2 uri=/health match=server_ok;
    }
}
```

## Sticky Sessions (NGINX Plus)

### Cookie-Based

```nginx
upstream backend {
    zone backend 64k;
    server backend1:8080;
    server backend2:8080;

    sticky cookie srv_id expires=1h domain=.example.com path=/;
}
```

### Learn from Application Cookie

```nginx
upstream backend {
    zone backend 64k;
    server backend1:8080;
    server backend2:8080;

    sticky learn
        create=$upstream_cookie_JSESSIONID
        lookup=$cookie_JSESSIONID
        zone=client_sessions:1m;
}
```

## TCP/UDP Stream Load Balancing

```nginx
stream {
    upstream mysql_backend {
        least_conn;
        server mysql1:3306 max_fails=3 fail_timeout=30s;
        server mysql2:3306 max_fails=3 fail_timeout=30s;
    }

    server {
        listen 3306;
        proxy_pass mysql_backend;
        proxy_timeout 5s;
        proxy_connect_timeout 1s;
    }
}
```

## SSL/TLS Termination

```nginx
upstream backend {
    server backend1:8080;
    server backend2:8080;
    keepalive 32;
}

server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/nginx/ssl/example.com.crt;
    ssl_certificate_key /etc/nginx/ssl/example.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }
}
```

## Advanced Patterns

### Slow Start (NGINX Plus)

Gradually increase traffic to newly added or recovered servers:

```nginx
upstream backend {
    zone backend 64k;
    server backend1:8080 slow_start=30s;
    server backend2:8080 slow_start=30s;
}
```

### Connection Limits

```nginx
upstream backend {
    server backend1:8080 max_conns=100;
    server backend2:8080 max_conns=100;
    queue 50 timeout=30s;
}
```

### Error Handling

```nginx
location / {
    proxy_pass http://backend;
    proxy_next_upstream error timeout http_500 http_502 http_503;
    proxy_next_upstream_tries 2;
    proxy_next_upstream_timeout 10s;
}
```

## Complete Configuration Example

See `examples/nginx/http-load-balancing.conf` for a production-ready configuration with:
- Multiple upstream pools
- SSL termination
- Health checks
- Caching
- Rate limiting
- Security headers
