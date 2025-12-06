# nginx Load Balancing

Guide to load balancing configuration in nginx.


## Table of Contents

- [Load Balancing Methods](#load-balancing-methods)
  - [Round Robin (Default)](#round-robin-default)
  - [Least Connections](#least-connections)
  - [IP Hash (Sticky Sessions)](#ip-hash-sticky-sessions)
  - [Weighted Load Balancing](#weighted-load-balancing)
- [Health Checks](#health-checks)
  - [Passive Health Checks (Open Source)](#passive-health-checks-open-source)
- [Persistent Connections](#persistent-connections)
  - [Keepalive to Backend](#keepalive-to-backend)
- [Complete Examples](#complete-examples)
  - [High Availability Setup](#high-availability-setup)

## Load Balancing Methods

### Round Robin (Default)

Sequential distribution to each server:

```nginx
upstream backend {
    server backend1.example.com:8080;
    server backend2.example.com:8080;
    server backend3.example.com:8080;
}
```

### Least Connections

Route to server with fewest active connections:

```nginx
upstream backend {
    least_conn;
    server backend1.example.com:8080;
    server backend2.example.com:8080;
}
```

### IP Hash (Sticky Sessions)

Same client always routes to same server based on IP:

```nginx
upstream backend {
    ip_hash;
    server backend1.example.com:8080;
    server backend2.example.com:8080;
}
```

**Note:** Can cause uneven distribution if many clients behind NAT.

### Weighted Load Balancing

Distribute based on server capacity:

```nginx
upstream backend {
    server backend1.example.com:8080 weight=3;  # Gets 3x traffic
    server backend2.example.com:8080 weight=2;  # Gets 2x traffic
    server backend3.example.com:8080 weight=1;  # Gets 1x traffic
}
```

## Health Checks

### Passive Health Checks (Open Source)

nginx marks server down after failures:

```nginx
upstream backend {
    server backend1.example.com:8080 max_fails=3 fail_timeout=30s;
    server backend2.example.com:8080 max_fails=3 fail_timeout=30s;
    server backup.example.com:8080 backup;
}
```

- `max_fails`: Number of failed attempts before marking down
- `fail_timeout`: How long to wait before retry
- `backup`: Only used if all primary servers down

## Persistent Connections

### Keepalive to Backend

```nginx
upstream backend {
    server backend1.example.com:8080;
    server backend2.example.com:8080;

    keepalive 32;  # Keep 32 idle connections open
    keepalive_timeout 60s;
    keepalive_requests 100;
}

server {
    location / {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }
}
```

## Complete Examples

### High Availability Setup

```nginx
upstream backend {
    least_conn;

    # Primary servers
    server backend1.example.com:8080 weight=3 max_fails=3 fail_timeout=30s;
    server backend2.example.com:8080 weight=2 max_fails=3 fail_timeout=30s;

    # Backup server
    server backup.example.com:8080 backup;

    # Persistent connections
    keepalive 32;
}

server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://backend;
        proxy_next_upstream error timeout http_502 http_503 http_504;
        proxy_next_upstream_tries 3;
        include snippets/proxy-params.conf;
    }
}
```
