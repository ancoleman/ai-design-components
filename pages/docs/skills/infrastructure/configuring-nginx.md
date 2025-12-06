---
sidebar_position: 7
title: Configuring NGINX
description: NGINX configuration for static sites, reverse proxy, SSL/TLS, and load balancing
tags: [infrastructure, nginx, web-server, reverse-proxy]
---

# Configuring NGINX

Configure nginx for static sites, reverse proxying, load balancing, SSL/TLS termination, caching, and performance tuning with modern security best practices.

## When to Use

Use when:
- Setting up web server for static sites or single-page applications
- Configuring reverse proxy for Node.js, Python, Ruby, or Go applications
- Implementing load balancing across multiple backend servers
- Terminating SSL/TLS for HTTPS traffic
- Adding caching layer for performance improvement
- Building API gateway functionality
- Protecting against DDoS with rate limiting
- Proxying WebSocket connections

## Quick Start Examples

### Static Website

```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    root /var/www/example.com/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### Reverse Proxy

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

### SSL/TLS Configuration

```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    ssl_protocols TLSv1.3 TLSv1.2;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:50m;
    ssl_session_timeout 1d;

    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;

    location / {
        try_files $uri $uri/ =404;
    }
}

server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

## Core Concepts

### Configuration Structure

```
nginx.conf (global settings)
├── events { } (connection processing)
└── http { } (HTTP-level settings)
    └── server { } (virtual host)
        └── location { } (URL routing)
```

**File locations:**
- `/etc/nginx/nginx.conf` - Main configuration
- `/etc/nginx/sites-available/` - Available site configs
- `/etc/nginx/sites-enabled/` - Enabled sites (symlinks)
- `/etc/nginx/conf.d/*.conf` - Additional configs
- `/etc/nginx/snippets/` - Reusable config snippets

### Location Matching Priority

1. `location = /exact` - Exact match (highest priority)
2. `location ^~ /prefix` - Prefix match, stop searching
3. `location ~ \.php$` - Regex, case-sensitive
4. `location ~* \.(jpg|png)$` - Regex, case-insensitive
5. `location /` - Prefix match (lowest priority)

## Common Patterns

### Load Balancing

**Round Robin (default):**
```nginx
upstream backend {
    server backend1.example.com:8080;
    server backend2.example.com:8080;
    server backend3.example.com:8080;
    keepalive 32;
}
```

**Least Connections:**
```nginx
upstream backend {
    least_conn;
    server backend1.example.com:8080;
    server backend2.example.com:8080;
}
```

**IP Hash (sticky sessions):**
```nginx
upstream backend {
    ip_hash;
    server backend1.example.com:8080;
    server backend2.example.com:8080;
}
```

**Health Checks:**
```nginx
upstream backend {
    server backend1.example.com:8080 max_fails=3 fail_timeout=30s;
    server backend2.example.com:8080 max_fails=3 fail_timeout=30s;
    server backup.example.com:8080 backup;
}
```

### WebSocket Proxying

```nginx
upstream websocket_backend {
    server 127.0.0.1:3000;
}

server {
    listen 80;
    server_name ws.example.com;

    location / {
        proxy_pass http://websocket_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;

        # Long timeouts for persistent connections
        proxy_connect_timeout 7d;
        proxy_send_timeout 7d;
        proxy_read_timeout 7d;
    }
}
```

### Rate Limiting

```nginx
# In http context
http {
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=5r/s;
    limit_conn_zone $binary_remote_addr zone=conn_limit:10m;
}

# In server context
server {
    listen 80;

    limit_req zone=api_limit burst=10 nodelay;
    limit_conn conn_limit 10;

    location /api/ {
        proxy_pass http://backend;
    }
}
```

### Performance Optimization

**Worker Configuration:**
```nginx
# In main context
user www-data;
worker_processes auto;  # 1 per CPU core
worker_rlimit_nofile 65535;

events {
    worker_connections 4096;
    use epoll;
    multi_accept on;
}
```

**Gzip Compression:**
```nginx
# In http context
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_comp_level 6;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
```

**Proxy Caching:**
```nginx
# Define cache zone
proxy_cache_path /var/cache/nginx/proxy
                 levels=1:2
                 keys_zone=app_cache:100m
                 max_size=1g
                 inactive=60m;

# Use in location
location / {
    proxy_cache app_cache;
    proxy_cache_valid 200 60m;
    proxy_cache_use_stale error timeout updating;
    add_header X-Cache-Status $upstream_cache_status;
    proxy_pass http://backend;
}
```

### Security Headers

```nginx
# Create /etc/nginx/snippets/security-headers.conf
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
```

Include in server blocks:
```nginx
server {
    include snippets/security-headers.conf;
    # ... rest of config
}
```

## Safety Checklist

Before deploying:

- [ ] Test configuration syntax: `sudo nginx -t`
- [ ] Use reload, not restart: `sudo systemctl reload nginx`
- [ ] Check error logs: `sudo tail -f /var/log/nginx/error.log`
- [ ] Verify SSL/TLS: `openssl s_client -connect domain:443`
- [ ] Test externally: `curl -I https://domain.com`
- [ ] Monitor worker processes: `ps aux | grep nginx`

## Troubleshooting

**Quick fixes:**
- Test config: `sudo nginx -t`
- Check logs: `/var/log/nginx/error.log`
- Verify backend: `curl http://127.0.0.1:3000`

**Common errors:**
- 502: Backend down
- 504: Timeout (increase `proxy_read_timeout`)
- 413: Upload size (set `client_max_body_size`)

## Decision Framework

**Choose nginx for:**
- Performance-critical workloads (10K+ connections)
- Reverse proxy and load balancing
- Static file serving
- Modern application stacks

**Choose alternatives for:**
- Apache (`.htaccess`, mod_php, legacy apps)
- Caddy (auto-HTTPS, simpler config)
- Traefik (dynamic containers)
- Envoy (service mesh)

## Related Skills

- [Load Balancing Patterns](./load-balancing-patterns) - Advanced load balancing architecture
- [Administering Linux](./administering-linux) - Linux server management for nginx
- [Operating Kubernetes](./operating-kubernetes) - nginx Ingress Controller for Kubernetes
- [Shell Scripting](./shell-scripting) - Automate nginx deployment and configuration

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/configuring-nginx)
- Configuration Structure: `references/configuration-structure.md`
- Static Sites: `references/static-sites.md`
- Reverse Proxy: `references/reverse-proxy.md`
- Load Balancing: `references/load-balancing.md`
- SSL/TLS Config: `references/ssl-tls-config.md`
- Performance Tuning: `references/performance-tuning.md`
- Security Hardening: `references/security-hardening.md`
