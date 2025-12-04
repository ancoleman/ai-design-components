---
sidebar_position: 12
title: Configuring NGINX
description: Master plan for NGINX configuration including reverse proxy, load balancing, SSL/TLS, caching, and performance tuning
tags: [master-plan, infrastructure, nginx, web-server, reverse-proxy]
---

# Configuring NGINX

:::info Status
**Master Plan** - Comprehensive init.md complete, ready for SKILL.md implementation
:::

NGINX powers 33.6% of all websites and is the de facto standard for reverse proxy and load balancing. This skill covers static file serving, reverse proxying, load balancing, SSL/TLS termination, caching, performance tuning, and security hardening.

## Scope

This skill teaches:

- **Basic Configuration** - Server blocks, location blocks, routing
- **Reverse Proxy** - Proxying to Node.js/Python/Ruby backends
- **Load Balancing** - Round-robin, least_conn, ip_hash algorithms
- **SSL/TLS** - HTTPS configuration, TLS 1.3, modern cipher suites
- **Caching** - Proxy caching, FastCGI caching, microcaching
- **Performance Tuning** - Worker processes, connections, buffers
- **Security** - Rate limiting, security headers, DDoS protection
- **WebSocket Support** - Proxying WebSocket connections

## Key Components

### Server Block (Virtual Host)

```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    root /var/www/example.com;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### Reverse Proxy Configuration

```nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Load Balancing

```nginx
upstream backend {
    least_conn;  # or round_robin (default), ip_hash
    server backend1.example.com:3000;
    server backend2.example.com:3000;
    server backend3.example.com:3000;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
    }
}
```

### SSL/TLS Configuration (2025 Best Practices)

```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # TLS 1.3 only (or TLS 1.2+)
    ssl_protocols TLSv1.3 TLSv1.2;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers off;

    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    location / {
        proxy_pass http://backend;
    }
}
```

### Caching

```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=10g inactive=60m use_temp_path=off;

server {
    location / {
        proxy_cache my_cache;
        proxy_cache_valid 200 60m;
        proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
        add_header X-Cache-Status $upstream_cache_status;
        proxy_pass http://backend;
    }
}
```

## Decision Framework

**Which NGINX Use Case?**

```
Static website?
  YES → Simple server block + try_files

Backend application?
  YES → Reverse proxy configuration

Multiple backend servers?
  YES → Load balancing + upstream block

Need HTTPS?
  YES → SSL/TLS configuration + cert-manager/Let's Encrypt

Performance issues?
  YES → Caching + performance tuning
```

**Load Balancing Algorithm Selection:**

```
All backends equal capacity?
  YES → Round-robin (default)

Backends different capacity?
  YES → Weighted round-robin

Long-lived connections (WebSocket)?
  YES → least_conn (least connections)

Need session persistence?
  YES → ip_hash (client IP based)
```

## Tool Recommendations

### Configuration Management

**NGINX Itself:**
- NGINX Open Source (free)
- NGINX Plus (commercial, advanced features)

**Configuration Tools:**
- `nginx -t` - Test configuration
- `nginx -s reload` - Reload without downtime
- Ansible/Puppet/Chef roles for automation

**SSL/TLS:**
- **Let's Encrypt** - Free SSL certificates
- **Certbot** - Automatic certificate management
- **acme.sh** - Alternative ACME client

### Monitoring and Debugging

**Logs:**
- Access log: `/var/log/nginx/access.log`
- Error log: `/var/log/nginx/error.log`
- Custom log formats for debugging

**Status Module:**
```nginx
location /nginx_status {
    stub_status on;
    allow 127.0.0.1;
    deny all;
}
```

**Metrics:**
- NGINX Amplify (official monitoring)
- Prometheus nginx-exporter
- Datadog/New Relic integrations

### Performance Tuning

**Key Directives:**
- `worker_processes auto;` - Match CPU cores
- `worker_connections 1024;` - Connections per worker
- `keepalive_timeout 65;` - Connection keep-alive
- `client_max_body_size 10M;` - Upload size limit
- `gzip on;` - Compression

**Caching:**
- Proxy caching (reverse proxy)
- FastCGI caching (PHP)
- Microcaching (1-second cache for dynamic content)

## Integration Points

**With Other Skills:**
- `load-balancing-patterns` - Advanced load balancing strategies
- `infrastructure-as-code` - Automate NGINX deployment (Ansible, Terraform)
- `kubernetes-operations` - NGINX Ingress Controller
- `security-hardening` - Security headers, rate limiting, WAF integration
- `dns-management` - DNS setup for NGINX domains
- `observability` - NGINX metrics, access log analysis

**Workflow Example:**
```
Git Config → Ansible → NGINX Reload → Monitoring
     │          │           │             │
     ▼          ▼           ▼             ▼
nginx.conf  Deploy     nginx -s     Prometheus
changes     to server  reload       metrics
```

## Learn More

- [Full Master Plan (init.md)](https://github.com/ancoleman/ai-design-components/blob/main/skills/configuring-nginx/init.md)
- Related: `load-balancing-patterns`, `infrastructure-as-code`, `security-hardening`
