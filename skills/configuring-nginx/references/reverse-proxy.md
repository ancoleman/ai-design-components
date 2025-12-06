# nginx Reverse Proxy Configuration

Complete guide to configuring nginx as a reverse proxy for backend applications.

## Table of Contents

1. [Basic Reverse Proxy](#basic-reverse-proxy)
2. [Proxy Headers](#proxy-headers)
3. [WebSocket Proxying](#websocket-proxying)
4. [API Gateway Patterns](#api-gateway-patterns)
5. [Proxy Buffering](#proxy-buffering)
6. [Timeouts](#timeouts)
7. [Error Handling](#error-handling)

## Basic Reverse Proxy

### Single Backend

Proxy all requests to a single backend server:

```nginx
upstream app_backend {
    server 127.0.0.1:3000;
    keepalive 32;
}

server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://app_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }
}
```

### Multiple Backends (Load Balancing)

```nginx
upstream app_backend {
    server 127.0.0.1:3000;
    server 127.0.0.1:3001;
    server 127.0.0.1:3002;
    keepalive 32;
}
```

## Proxy Headers

### Essential Headers

Create `/etc/nginx/snippets/proxy-params.conf`:

```nginx
# Preserve client information
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;

# HTTP/1.1 for keepalive
proxy_http_version 1.1;
proxy_set_header Connection "";

# Timeouts
proxy_connect_timeout 60s;
proxy_send_timeout 60s;
proxy_read_timeout 60s;
```

Usage:
```nginx
location / {
    proxy_pass http://backend;
    include snippets/proxy-params.conf;
}
```

### Header Explanations

**Host:** Backend needs original hostname for virtual host routing
```nginx
proxy_set_header Host $host;
```

**X-Real-IP:** Backend sees client IP, not proxy IP
```nginx
proxy_set_header X-Real-IP $remote_addr;
```

**X-Forwarded-For:** Full chain of proxies (append to existing)
```nginx
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
```

**X-Forwarded-Proto:** Backend knows if original request was HTTPS
```nginx
proxy_set_header X-Forwarded-Proto $scheme;
```

**Connection:** Enable persistent connections to backend
```nginx
proxy_http_version 1.1;
proxy_set_header Connection "";
```

## WebSocket Proxying

WebSocket requires HTTP/1.1 and connection upgrade:

```nginx
upstream websocket_backend {
    server 127.0.0.1:3000;
}

server {
    listen 80;
    server_name ws.example.com;

    location / {
        proxy_pass http://websocket_backend;

        # WebSocket upgrade headers
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Standard proxy headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # Long timeouts for persistent connections
        proxy_connect_timeout 7d;
        proxy_send_timeout 7d;
        proxy_read_timeout 7d;
    }
}
```

### Socket.io Configuration

```nginx
location /socket.io/ {
    proxy_pass http://socketio_backend;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_cache_bypass $http_upgrade;
}
```

## API Gateway Patterns

### Path-Based Routing

Route different paths to different services:

```nginx
upstream auth_service {
    server 127.0.0.1:4000;
}

upstream user_service {
    server 127.0.0.1:4001;
}

upstream order_service {
    server 127.0.0.1:4002;
}

server {
    listen 80;
    server_name api.example.com;

    # Authentication service
    location /api/auth/ {
        proxy_pass http://auth_service/;
        include snippets/proxy-params.conf;
    }

    # User service
    location /api/users/ {
        proxy_pass http://user_service/;
        include snippets/proxy-params.conf;
    }

    # Order service
    location /api/orders/ {
        proxy_pass http://order_service/;
        include snippets/proxy-params.conf;
    }

    # Health check (nginx responds directly)
    location /health {
        access_log off;
        return 200 "OK\n";
        add_header Content-Type text/plain;
    }
}
```

### Header-Based Routing

Route based on request headers:

```nginx
http {
    map $http_x_api_version $backend {
        "v1"    backend_v1;
        "v2"    backend_v2;
        default backend_v2;
    }

    upstream backend_v1 {
        server 127.0.0.1:4001;
    }

    upstream backend_v2 {
        server 127.0.0.1:4002;
    }

    server {
        listen 80;
        server_name api.example.com;

        location / {
            proxy_pass http://$backend;
            include snippets/proxy-params.conf;
        }
    }
}
```

### Subdomain-Based Routing

Route based on subdomain:

```nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://api_backend;
        include snippets/proxy-params.conf;
    }
}

server {
    listen 80;
    server_name admin.example.com;

    location / {
        proxy_pass http://admin_backend;
        include snippets/proxy-params.conf;
    }
}

server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://app_backend;
        include snippets/proxy-params.conf;
    }
}
```

## Proxy Buffering

### Enable Buffering (Default)

Reduces load on backend by buffering responses:

```nginx
location / {
    proxy_pass http://backend;

    # Enable buffering
    proxy_buffering on;
    proxy_buffer_size 4k;
    proxy_buffers 8 4k;
    proxy_busy_buffers_size 8k;
    proxy_max_temp_file_size 1024m;
}
```

### Disable Buffering (Streaming)

For server-sent events (SSE) or real-time streaming:

```nginx
location /stream {
    proxy_pass http://backend;
    proxy_buffering off;
    proxy_cache off;
    proxy_http_version 1.1;
    proxy_set_header Connection "";

    # Long timeout for streaming
    proxy_read_timeout 24h;
}
```

### Request Body Buffering

```nginx
# Buffer small uploads to disk
client_body_buffer_size 128k;

# Maximum upload size
client_max_body_size 100m;

# Temp file location
client_body_temp_path /var/nginx/client_body_temp;
```

## Timeouts

### Proxy Timeouts

```nginx
location / {
    proxy_pass http://backend;

    # Time to establish connection to backend
    proxy_connect_timeout 60s;

    # Time to transmit request to backend
    proxy_send_timeout 60s;

    # Time to receive response from backend
    proxy_read_timeout 60s;
}
```

### Application-Specific Timeouts

**Fast APIs:**
```nginx
proxy_connect_timeout 5s;
proxy_send_timeout 10s;
proxy_read_timeout 10s;
```

**Slow processing (reports, analytics):**
```nginx
proxy_connect_timeout 10s;
proxy_send_timeout 120s;
proxy_read_timeout 300s;  # 5 minutes
```

**Long-polling:**
```nginx
proxy_connect_timeout 10s;
proxy_read_timeout 3600s;  # 1 hour
```

## Error Handling

### Custom Error Pages

```nginx
server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://backend;
        include snippets/proxy-params.conf;

        # Intercept errors
        proxy_intercept_errors on;

        # Custom error pages
        error_page 502 503 504 /50x.html;
        error_page 404 /404.html;
    }

    location = /50x.html {
        root /var/www/errors;
        internal;
    }

    location = /404.html {
        root /var/www/errors;
        internal;
    }
}
```

### Fallback to Backup Backend

```nginx
upstream backend {
    server backend1.example.com:8080 max_fails=3 fail_timeout=30s;
    server backend2.example.com:8080 max_fails=3 fail_timeout=30s;
    server backup.example.com:8080 backup;
}

server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://backend;
        proxy_next_upstream error timeout http_502 http_503 http_504;
        proxy_next_upstream_tries 3;
        proxy_next_upstream_timeout 10s;
        include snippets/proxy-params.conf;
    }
}
```

### Named Location Fallback

```nginx
location / {
    proxy_pass http://primary_backend;
    proxy_intercept_errors on;
    error_page 502 503 504 = @fallback;
}

location @fallback {
    proxy_pass http://backup_backend;
    include snippets/proxy-params.conf;
}
```

## Advanced Patterns

### Serving Static Files Directly

Bypass backend for static assets:

```nginx
server {
    listen 80;
    server_name app.example.com;

    # Serve static files directly from nginx
    location /static/ {
        alias /var/www/app/static/;
        expires 1y;
        access_log off;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/app/media/;
        expires 30d;
    }

    # Proxy dynamic content to backend
    location / {
        proxy_pass http://app_backend;
        include snippets/proxy-params.conf;
    }
}
```

### URL Rewriting

Modify URL before proxying:

```nginx
# Remove /api prefix before proxying
location /api/ {
    rewrite ^/api/(.*)$ /$1 break;
    proxy_pass http://backend;
    include snippets/proxy-params.conf;
}

# Add prefix
location / {
    proxy_pass http://backend/app/;
    include snippets/proxy-params.conf;
}
```

### Conditional Proxying

```nginx
# Route mobile users to different backend
set $backend app_backend;

if ($http_user_agent ~* (mobile|android|iphone)) {
    set $backend mobile_backend;
}

location / {
    proxy_pass http://$backend;
    include snippets/proxy-params.conf;
}
```

### Adding/Removing Headers

```nginx
location / {
    proxy_pass http://backend;

    # Add custom headers
    proxy_set_header X-Custom-Header "value";
    proxy_set_header X-Request-ID $request_id;

    # Remove headers from response
    proxy_hide_header X-Powered-By;
    proxy_hide_header Server;

    include snippets/proxy-params.conf;
}
```

## Testing and Debugging

### Test Proxy Configuration

```bash
# Test nginx configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx

# Test locally
curl -H "Host: app.example.com" http://localhost/

# Check backend is reachable
curl http://127.0.0.1:3000/

# Test with headers
curl -H "X-Forwarded-For: 1.2.3.4" http://app.example.com/
```

### View Proxy Headers

Backend application should log received headers to verify proxy configuration:

```javascript
// Node.js/Express
app.use((req, res, next) => {
    console.log('Headers:', req.headers);
    console.log('Host:', req.headers.host);
    console.log('X-Real-IP:', req.headers['x-real-ip']);
    console.log('X-Forwarded-For:', req.headers['x-forwarded-for']);
    console.log('X-Forwarded-Proto:', req.headers['x-forwarded-proto']);
    next();
});
```

### Debug Proxy Issues

Enable debug logging:

```nginx
error_log /var/log/nginx/error.log debug;

location / {
    proxy_pass http://backend;
    access_log /var/log/nginx/proxy-debug.log;
}
```

View logs:
```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/proxy-debug.log
```

## Common Issues

**502 Bad Gateway:**
- Backend not running: `curl http://127.0.0.1:3000`
- Wrong backend address in proxy_pass
- SELinux blocking connections: `sudo setsebool -P httpd_can_network_connect 1`

**504 Gateway Timeout:**
- Backend too slow
- Increase proxy_read_timeout
- Check backend performance

**Connection reset:**
- Ensure proxy_http_version 1.1
- Check keepalive settings
- Verify upstream keepalive directive

**Headers not reaching backend:**
- Check proxy_set_header directives
- Verify backend logging
- Test with curl -H
