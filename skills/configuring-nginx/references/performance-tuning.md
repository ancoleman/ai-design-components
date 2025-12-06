# nginx Performance Tuning

Optimization strategies for high-traffic nginx deployments.


## Table of Contents

- [Worker Process Configuration](#worker-process-configuration)
  - [CPU and Connection Optimization](#cpu-and-connection-optimization)
  - [Check System Limits](#check-system-limits)
- [HTTP Performance Settings](#http-performance-settings)
- [Gzip Compression](#gzip-compression)
- [File Caching](#file-caching)
  - [Open File Cache](#open-file-cache)
  - [Static Asset Caching](#static-asset-caching)
- [Proxy Caching](#proxy-caching)
- [Buffering](#buffering)
  - [Proxy Buffering](#proxy-buffering)
- [Connection Keep-Alive](#connection-keep-alive)
  - [Client Connections](#client-connections)
  - [Upstream Connections](#upstream-connections)
- [Monitoring Performance](#monitoring-performance)
  - [Status Module](#status-module)
- [Benchmarking](#benchmarking)
  - [Using ab (ApacheBench)](#using-ab-apachebench)
  - [Using wrk](#using-wrk)
- [Best Practices](#best-practices)

## Worker Process Configuration

### CPU and Connection Optimization

```nginx
# /etc/nginx/nginx.conf

user www-data;
worker_processes auto;  # 1 per CPU core
worker_rlimit_nofile 65535;  # Match system ulimit
pid /run/nginx.pid;

events {
    worker_connections 4096;  # Max connections per worker
    use epoll;  # Linux: epoll, BSD: kqueue, macOS: kqueue
    multi_accept on;  # Accept multiple connections at once
}
```

**Calculations:**
- Max clients = worker_processes × worker_connections
- With 4 cores and 4096 connections: 16,384 concurrent connections

### Check System Limits

```bash
# Check current limit
ulimit -n

# Set limit temporarily
ulimit -n 65535

# Set permanently in /etc/security/limits.conf
www-data soft nofile 65535
www-data hard nofile 65535
```

## HTTP Performance Settings

```nginx
http {
    # File operations
    sendfile on;  # Kernel-level file sending
    tcp_nopush on;  # Send headers in one packet
    tcp_nodelay on;  # Don't buffer data

    # Timeouts
    keepalive_timeout 65;
    keepalive_requests 100;
    client_body_timeout 12;
    client_header_timeout 12;
    send_timeout 10;

    # Hide version
    server_tokens off;

    # Hash table sizes
    types_hash_max_size 2048;
    server_names_hash_bucket_size 64;

    # Buffer sizes
    client_body_buffer_size 128k;
    client_max_body_size 10m;
    client_header_buffer_size 1k;
    large_client_header_buffers 4 8k;
    output_buffers 2 32k;
}
```

## Gzip Compression

Reduce bandwidth and improve page load times:

```nginx
http {
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;  # 1-9, balance compression vs CPU
    gzip_min_length 1024;  # Don't compress < 1KB
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;

    # Don't compress already-compressed formats
    gzip_disable "msie6";
}
```

## File Caching

### Open File Cache

Cache file descriptors:

```nginx
http {
    open_file_cache max=10000 inactive=20s;
    open_file_cache_valid 30s;
    open_file_cache_min_uses 2;
    open_file_cache_errors on;
}
```

### Static Asset Caching

Browser caching for static files:

```nginx
location ~* \.(jpg|jpeg|png|gif|ico|svg|webp)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    access_log off;
}

location ~* \.(css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    access_log off;
}

location ~* \.(woff|woff2|ttf|eot)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    access_log off;
}
```

## Proxy Caching

Cache backend responses:

```nginx
http {
    # Define cache zone
    proxy_cache_path /var/cache/nginx/proxy
                     levels=1:2
                     keys_zone=app_cache:100m
                     max_size=1g
                     inactive=60m
                     use_temp_path=off;

    server {
        location / {
            proxy_pass http://backend;

            # Enable caching
            proxy_cache app_cache;
            proxy_cache_valid 200 60m;
            proxy_cache_valid 404 10m;
            proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
            proxy_cache_background_update on;
            proxy_cache_lock on;

            # Cache status header
            add_header X-Cache-Status $upstream_cache_status;
        }
    }
}
```

## Buffering

### Proxy Buffering

```nginx
location / {
    proxy_pass http://backend;

    proxy_buffering on;
    proxy_buffer_size 4k;
    proxy_buffers 8 4k;
    proxy_busy_buffers_size 8k;
}
```

## Connection Keep-Alive

### Client Connections

```nginx
keepalive_timeout 65;
keepalive_requests 100;
```

### Upstream Connections

```nginx
upstream backend {
    server backend1.example.com:8080;
    server backend2.example.com:8080;

    keepalive 32;  # Keep 32 idle connections
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

## Monitoring Performance

### Status Module

Enable stub_status module:

```nginx
server {
    listen 8080;
    server_name localhost;

    location /nginx_status {
        stub_status on;
        access_log off;
        allow 127.0.0.1;
        deny all;
    }
}
```

Check status:
```bash
curl http://localhost:8080/nginx_status
```

Output:
```
Active connections: 291
server accepts handled requests
 16630948 16630948 31070465
Reading: 6 Writing: 179 Waiting: 106
```

## Benchmarking

### Using ab (ApacheBench)

```bash
# 1000 requests, 10 concurrent
ab -n 1000 -c 10 http://example.com/

# With keepalive
ab -n 1000 -c 10 -k http://example.com/
```

### Using wrk

```bash
# 12 threads, 400 connections, 30 seconds
wrk -t12 -c400 -d30s http://example.com/
```

## Best Practices

1. **Use worker_processes auto** - Automatically matches CPU cores
2. **Enable gzip compression** - Reduces bandwidth
3. **Cache static assets** - Long expires headers
4. **Use proxy caching** - Reduces backend load
5. **Enable keepalive to upstreams** - Reduces connection overhead
6. **Monitor worker connections** - Increase if hitting limits
7. **Tune buffer sizes** - Based on typical request/response sizes
8. **Log analysis** - Identify slow endpoints
