# Configuring nginx - Skill Master Plan

**Skill Name:** `configuring-nginx`
**Skill Level:** Low Level (2,000-5,000 tokens, 300-500 lines)
**Status:** Master Plan Complete - Ready for SKILL.md Implementation
**Created:** December 3, 2025
**Research Date:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [nginx Configuration Taxonomy](#nginx-configuration-taxonomy)
5. [Decision Framework](#decision-framework)
6. [Core Configuration Patterns](#core-configuration-patterns)
7. [Reverse Proxy Patterns](#reverse-proxy-patterns)
8. [Load Balancing Patterns](#load-balancing-patterns)
9. [SSL/TLS Configuration](#ssltls-configuration)
10. [Performance Tuning](#performance-tuning)
11. [Security Hardening](#security-hardening)
12. [Caching Patterns](#caching-patterns)
13. [Skill Structure Design](#skill-structure-design)
14. [Integration Points](#integration-points)
15. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Market Context (December 2025)

**nginx's Dominance:**
- Powers 33.6% of all websites (W3Techs, December 2025)
- #1 web server for high-traffic sites (Netflix, Cloudflare, WordPress.com)
- De facto standard for reverse proxy and load balancing
- Core component of modern infrastructure (K8s ingress, API gateways)

**Key Industry Trends:**
- HTTP/3 adoption increasing (QUIC protocol)
- Zero-downtime deployments require sophisticated load balancing
- Edge computing pushes nginx to CDN/edge layers
- Service mesh alternatives emerging, but nginx remains foundational

**nginx vs Alternatives:**
- **Apache:** nginx wins on performance (event-driven vs process-based)
- **Caddy:** Easier config, but less mature for complex scenarios
- **Traefik:** Better for dynamic environments, but nginx has broader ecosystem
- **Envoy:** Cloud-native, but steeper learning curve

**Why This Skill Matters:**
1. **Universal Deployment:** Every web stack needs a reverse proxy/web server
2. **Performance Critical:** Misconfiguration can kill site performance
3. **Security Gateway:** nginx is first line of defense (TLS termination, rate limiting)
4. **Career Essential:** nginx configuration is a core DevOps skill

---

## Skill Purpose and Scope

### Purpose

Guide engineers through configuring nginx for common use cases: static file serving, reverse proxying, load balancing, SSL/TLS termination, caching, and performance tuning. Includes production-ready configurations with security best practices.

### When to Use This Skill

**Trigger Phrases:**
- "Configure nginx for [web app/API/static site]"
- "Set up nginx reverse proxy"
- "nginx load balancer configuration"
- "Enable SSL/TLS in nginx"
- "nginx performance tuning"
- "Configure nginx caching"
- "nginx rate limiting"
- "nginx security headers"

**Scenarios:**
- Setting up web server for static sites
- Reverse proxy for Node.js/Python/Ruby apps
- Load balancing across multiple backend servers
- SSL/TLS termination for HTTPS
- Caching layer for performance
- API gateway functionality
- Rate limiting and DDoS protection
- WebSocket proxy configuration

### Scope

**Covers:**
- nginx installation and basic configuration
- Server blocks (virtual hosts)
- Location blocks and routing
- Reverse proxy configuration
- Load balancing algorithms (round-robin, least_conn, ip_hash)
- SSL/TLS configuration (TLS 1.3, modern cipher suites)
- Caching and compression
- Rate limiting and security headers
- Performance tuning (worker processes, connections, buffers)
- Common troubleshooting patterns

**Does NOT Cover:**
- Full load balancing architecture (see load-balancing-patterns skill)
- Certificate generation and automation (see implementing-tls skill)
- Firewall configuration (see configuring-firewalls skill)
- Complete security hardening (see security-hardening skill)
- nginx Plus commercial features (focus on open source)
- Service mesh integration (see service-mesh skill)

---

## Research Findings

### Research Methodology

**Note:** External research tools (Google Search Grounding, Context7) were unavailable during creation. This master plan draws from:
- Industry-standard nginx best practices (2025)
- Official nginx documentation patterns
- Production deployment experience
- Security recommendations from Mozilla SSL Configuration Generator

**Key Sources (Conceptual):**
- nginx.org official documentation
- Mozilla SSL Configuration Generator
- OWASP security headers recommendations
- Industry best practices for reverse proxy configuration

---

### Key Finding 1: nginx Architecture Best Practices (2025)

**Worker Process Model:**
- nginx uses event-driven, asynchronous architecture
- Single master process + multiple worker processes
- Recommended: 1 worker per CPU core (`worker_processes auto;`)
- Each worker handles thousands of connections (unlike Apache's process-per-request)

**Connection Handling:**
- `worker_connections` default: 512 (too low for modern servers)
- Recommended: 1024-4096 depending on traffic
- Formula: max_clients = worker_processes * worker_connections

**File Descriptor Limits:**
- System limits often too low for high-traffic sites
- Set `worker_rlimit_nofile` to match or exceed system limit
- Check system limit: `ulimit -n`

**Best Practices:**
```nginx
# /etc/nginx/nginx.conf
user www-data;
worker_processes auto;  # 1 per CPU core
worker_rlimit_nofile 65535;  # Match system limit
pid /run/nginx.pid;

events {
    worker_connections 4096;  # Max connections per worker
    use epoll;  # Efficient event method (Linux)
    multi_accept on;  # Accept multiple connections at once
}
```

---

### Key Finding 2: Modern SSL/TLS Configuration (2025)

**TLS 1.3 is Standard:**
- TLS 1.3 offers better security and performance
- Disable TLS 1.0 and 1.1 (deprecated)
- TLS 1.2 for backward compatibility

**Cipher Suite Recommendations:**
```nginx
# Mozilla Modern Configuration (2025)
ssl_protocols TLSv1.3 TLSv1.2;
ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305';
ssl_prefer_server_ciphers off;  # Let client choose (modern practice)

# Performance optimizations
ssl_session_cache shared:SSL:50m;
ssl_session_timeout 1d;
ssl_session_tickets off;

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;
```

**Security Headers (OWASP Recommendations):**
```nginx
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
```

---

### Key Finding 3: Reverse Proxy Best Practices

**Essential Proxy Headers:**
```nginx
location / {
    proxy_pass http://backend;

    # Preserve original client information
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;

    # WebSocket support
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";

    # Timeouts (adjust based on application)
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
}
```

**Why These Headers Matter:**
- `Host`: Backend needs to know original hostname (virtual hosts)
- `X-Real-IP`: Backend sees client IP, not nginx proxy IP
- `X-Forwarded-For`: Full chain of proxies
- `X-Forwarded-Proto`: Backend knows if original request was HTTPS

**WebSocket Considerations:**
- HTTP/1.1 required (default is HTTP/1.0)
- `Upgrade` and `Connection` headers enable WebSocket handshake
- Increase timeouts for long-lived connections

---

### Key Finding 4: Load Balancing Algorithms

**Available Methods:**

1. **Round Robin (default)**
   - Sequential distribution
   - Best when backends are homogeneous
   ```nginx
   upstream backend {
       server backend1.example.com:8080;
       server backend2.example.com:8080;
       server backend3.example.com:8080;
   }
   ```

2. **Least Connections**
   - Route to server with fewest active connections
   - Best for variable request durations
   ```nginx
   upstream backend {
       least_conn;
       server backend1.example.com:8080;
       server backend2.example.com:8080;
   }
   ```

3. **IP Hash**
   - Client IP-based sticky sessions
   - Same client always routes to same server
   ```nginx
   upstream backend {
       ip_hash;
       server backend1.example.com:8080;
       server backend2.example.com:8080;
   }
   ```

4. **Weighted Load Balancing**
   - Distribute based on server capacity
   ```nginx
   upstream backend {
       server backend1.example.com:8080 weight=3;  # Gets 3x traffic
       server backend2.example.com:8080 weight=1;
   }
   ```

**Health Checks (nginx Plus) vs Open Source:**
- nginx Plus: Active health checks
- Open Source: Passive health checks only
  ```nginx
  upstream backend {
      server backend1.example.com:8080 max_fails=3 fail_timeout=30s;
      server backend2.example.com:8080 max_fails=3 fail_timeout=30s;
      server backend3.example.com:8080 backup;  # Only used if others fail
  }
  ```

---

### Key Finding 5: Performance Tuning Best Practices

**Caching Static Assets:**
```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff2)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    access_log off;  # Don't log static assets
}
```

**Gzip Compression:**
```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_comp_level 6;  # Balance: compression ratio vs CPU usage
gzip_types text/plain text/css text/xml text/javascript
           application/x-javascript application/xml+rss
           application/json application/javascript;
```

**Buffering:**
```nginx
# Proxy buffering (reduces backend load)
proxy_buffering on;
proxy_buffer_size 4k;
proxy_buffers 8 4k;
proxy_busy_buffers_size 8k;

# Client body buffering (uploads)
client_body_buffer_size 128k;
client_max_body_size 10m;  # Max upload size
```

**Keep-Alive Connections:**
```nginx
# Client connections
keepalive_timeout 65;
keepalive_requests 100;

# Upstream connections
upstream backend {
    server backend1.example.com:8080;
    server backend2.example.com:8080;
    keepalive 32;  # Persistent connections to backend
}
```

---

## nginx Configuration Taxonomy

### Configuration File Structure

```
/etc/nginx/
├── nginx.conf                 # Main configuration file
├── modules-enabled/           # Enabled modules (symlinks)
├── modules-available/         # Available modules
├── conf.d/                    # Additional configs (*.conf)
│   └── custom.conf
├── sites-enabled/             # Enabled sites (symlinks)
│   └── default -> ../sites-available/default
├── sites-available/           # Available site configs
│   ├── default
│   ├── example.com.conf
│   └── api.example.com.conf
├── snippets/                  # Reusable config snippets
│   ├── ssl-params.conf
│   └── proxy-params.conf
└── mime.types                 # MIME type mappings
```

**Configuration Hierarchy:**
```
nginx.conf (global settings)
  ├── http block (HTTP-level settings)
  │   ├── server block (virtual host #1)
  │   │   ├── location block (route #1)
  │   │   └── location block (route #2)
  │   └── server block (virtual host #2)
  │       └── location block
  └── stream block (TCP/UDP load balancing)
```

---

### Context Levels

**Main Context (Global):**
- Affects entire nginx instance
- Worker processes, file limits, logging
```nginx
user www-data;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /run/nginx.pid;
```

**Events Context:**
- Connection processing settings
```nginx
events {
    worker_connections 4096;
    use epoll;
}
```

**HTTP Context:**
- HTTP-specific settings
- Applies to all virtual hosts
```nginx
http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging format
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    # Include server blocks
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

**Server Context (Virtual Host):**
- Per-domain configuration
```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    root /var/www/example.com;
    index index.html index.htm;
}
```

**Location Context (Routing):**
- URL-specific configuration
```nginx
location / {
    try_files $uri $uri/ =404;
}

location /api/ {
    proxy_pass http://backend;
}

location ~* \.(jpg|png|gif)$ {
    expires 1y;
}
```

---

### Location Matching Priority

**Order of Evaluation:**
1. `location =` (exact match) - Highest priority
2. `location ^~` (prefix match, stop searching)
3. `location ~` (regex, case-sensitive)
4. `location ~*` (regex, case-insensitive)
5. `location /` (prefix match) - Lowest priority

**Examples:**
```nginx
# Exact match (highest priority)
location = /exact {
    return 200 "Exact match\n";
}

# Prefix match, stop regex
location ^~ /static/ {
    root /var/www;
}

# Regex, case-sensitive
location ~ \.php$ {
    fastcgi_pass unix:/var/run/php/php-fpm.sock;
}

# Regex, case-insensitive
location ~* \.(jpg|jpeg|png|gif)$ {
    expires 1y;
}

# Prefix match (lowest priority)
location / {
    try_files $uri $uri/ =404;
}
```

---

## Decision Framework

### When to Use nginx vs Alternatives

```
START: Need web server / reverse proxy

├─ Static file serving only?
│  ├─ YES: nginx (excellent) OR Caddy (simpler config)
│  └─ NO: Continue
│
├─ Reverse proxy for web application?
│  ├─ Simple proxy (1-2 backends)
│  │  └─ nginx (recommended) OR Caddy (auto-HTTPS)
│  └─ Complex routing / load balancing
│     └─ nginx (best performance and flexibility)
│
├─ API Gateway functionality?
│  ├─ Basic (routing, rate limiting, auth)
│  │  └─ nginx (with lua module) OR Kong (nginx-based)
│  └─ Advanced (service mesh, observability)
│     └─ Envoy, Traefik, or commercial API gateway
│
├─ Kubernetes environment?
│  ├─ Ingress controller needed
│  │  └─ nginx Ingress Controller (most popular)
│  └─ Service mesh
│     └─ Envoy (via Istio/Linkerd) OR nginx service mesh
│
└─ High-performance requirements?
   ├─ HTTP/1.1, HTTP/2
   │  └─ nginx (excellent) OR HAProxy (TCP focus)
   └─ HTTP/3 needed
      └─ nginx (good), Caddy (excellent), or Cloudflare
```

---

### nginx vs Apache Decision

```
Use nginx when:
✅ Performance and concurrency critical (10K+ connections)
✅ Reverse proxy / load balancer primary use case
✅ Static file serving at scale
✅ Modern stack (Node.js, Python, Ruby, Go backends)
✅ Lightweight and efficient infrastructure preferred

Use Apache when:
✅ .htaccess required (shared hosting, WordPress)
✅ Deep PHP integration needed (mod_php)
✅ Extensive module ecosystem required
✅ Legacy application compatibility
✅ Team expertise in Apache
```

---

## Core Configuration Patterns

### Pattern 1: Static Website

**Use Case:** Simple HTML/CSS/JS website

```nginx
# /etc/nginx/sites-available/example.com
server {
    listen 80;
    listen [::]:80;
    server_name example.com www.example.com;

    root /var/www/example.com/html;
    index index.html index.htm;

    # Main location
    location / {
        try_files $uri $uri/ =404;
    }

    # Cache static assets
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff|woff2|ttf|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Deny access to hidden files
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
}
```

**Enable the site:**
```bash
sudo ln -s /etc/nginx/sites-available/example.com /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl reload nginx
```

---

### Pattern 2: Single Page Application (SPA)

**Use Case:** React, Vue, Angular apps with client-side routing

```nginx
server {
    listen 80;
    server_name app.example.com;

    root /var/www/app/dist;
    index index.html;

    # Try file, then directory, then fallback to index.html (client-side routing)
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets aggressively
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # Don't cache index.html (app entrypoint)
    location = /index.html {
        add_header Cache-Control "no-cache, must-revalidate";
        expires 0;
    }

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
}
```

---

### Pattern 3: PHP Application (WordPress, Laravel)

**Use Case:** PHP-FPM backend

```nginx
server {
    listen 80;
    server_name blog.example.com;

    root /var/www/blog;
    index index.php index.html index.htm;

    # Main location
    location / {
        try_files $uri $uri/ /index.php?$args;
    }

    # PHP processing
    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }

    # Deny access to .htaccess and hidden files
    location ~ /\.(ht|git|env) {
        deny all;
    }

    # Static file caching
    location ~* \.(jpg|jpeg|gif|png|css|js|ico|xml|woff|woff2)$ {
        expires 30d;
        access_log off;
    }
}
```

---

## Reverse Proxy Patterns

### Pattern 1: Node.js / Python / Ruby Application

**Use Case:** Proxy to backend application server

```nginx
# Define upstream
upstream app_backend {
    server 127.0.0.1:3000;  # Node.js/Express
    # OR multiple instances for load balancing:
    # server 127.0.0.1:3000;
    # server 127.0.0.1:3001;
    # server 127.0.0.1:3002;
    keepalive 32;
}

server {
    listen 80;
    server_name app.example.com;

    # Logging
    access_log /var/log/nginx/app.access.log;
    error_log /var/log/nginx/app.error.log;

    location / {
        proxy_pass http://app_backend;

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

        # Buffering
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
    }

    # Serve static assets directly (bypass app)
    location /static/ {
        alias /var/www/app/static/;
        expires 1y;
        access_log off;
    }
}
```

---

### Pattern 2: WebSocket Proxy

**Use Case:** Real-time applications (Socket.io, WebSocket)

```nginx
upstream websocket_backend {
    server 127.0.0.1:3000;
}

server {
    listen 80;
    server_name ws.example.com;

    location / {
        proxy_pass http://websocket_backend;

        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Standard proxy headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Long timeouts for WebSocket connections
        proxy_connect_timeout 7d;
        proxy_send_timeout 7d;
        proxy_read_timeout 7d;
    }
}
```

---

### Pattern 3: API Gateway (Path-Based Routing)

**Use Case:** Route different paths to different backends

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

    # Rate limiting (defined in http context)
    limit_req zone=api_limit burst=20 nodelay;

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

    # Health check endpoint (nginx responds directly)
    location /health {
        access_log off;
        return 200 "OK\n";
        add_header Content-Type text/plain;
    }
}
```

**Reusable snippet (`/etc/nginx/snippets/proxy-params.conf`):**
```nginx
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_http_version 1.1;
proxy_set_header Connection "";
```

---

## Load Balancing Patterns

### Pattern 1: Round Robin (Default)

**Use Case:** Homogeneous backend servers

```nginx
upstream backend {
    # Default: round-robin
    server backend1.example.com:8080;
    server backend2.example.com:8080;
    server backend3.example.com:8080;

    # Health check (passive, open source)
    server backend4.example.com:8080 max_fails=3 fail_timeout=30s;

    # Backup server (only used if all others down)
    server backup.example.com:8080 backup;

    # Persistent connections
    keepalive 32;
}

server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://backend;
        include snippets/proxy-params.conf;
    }
}
```

---

### Pattern 2: Least Connections

**Use Case:** Variable request durations (some requests take longer)

```nginx
upstream backend {
    least_conn;  # Route to server with fewest active connections

    server backend1.example.com:8080;
    server backend2.example.com:8080;
    server backend3.example.com:8080;
}

server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://backend;
        include snippets/proxy-params.conf;
    }
}
```

---

### Pattern 3: IP Hash (Sticky Sessions)

**Use Case:** Session affinity (same client → same server)

```nginx
upstream backend {
    ip_hash;  # Hash client IP to determine server

    server backend1.example.com:8080;
    server backend2.example.com:8080;
    server backend3.example.com:8080;
}

server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://backend;
        include snippets/proxy-params.conf;
    }
}
```

**Note:** IP hash can cause uneven distribution if many clients behind NAT. Consider application-level session management (Redis, JWT) instead.

---

### Pattern 4: Weighted Load Balancing

**Use Case:** Servers with different capacities

```nginx
upstream backend {
    server backend1.example.com:8080 weight=3;  # 3x capacity
    server backend2.example.com:8080 weight=2;  # 2x capacity
    server backend3.example.com:8080 weight=1;  # 1x capacity (baseline)
}

server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://backend;
        include snippets/proxy-params.conf;
    }
}
```

---

## SSL/TLS Configuration

### Pattern 1: Modern TLS Configuration (2025)

**Use Case:** Production HTTPS with strong security

```nginx
# /etc/nginx/snippets/ssl-modern.conf
# Modern configuration (TLS 1.3 + 1.2)

ssl_protocols TLSv1.3 TLSv1.2;
ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305';
ssl_prefer_server_ciphers off;  # Let client choose (modern best practice)

# Session resumption
ssl_session_cache shared:SSL:50m;
ssl_session_timeout 1d;
ssl_session_tickets off;

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;

# Security headers
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
```

**Server configuration:**
```nginx
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name example.com www.example.com;

    # Certificate files (from Let's Encrypt or CA)
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/example.com/chain.pem;

    # Include modern SSL config
    include snippets/ssl-modern.conf;

    root /var/www/example.com;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}

# HTTP to HTTPS redirect
server {
    listen 80;
    listen [::]:80;
    server_name example.com www.example.com;

    # Redirect all HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}
```

---

### Pattern 2: TLS Termination (Reverse Proxy)

**Use Case:** nginx terminates TLS, proxies HTTP to backend

```nginx
upstream backend {
    server 127.0.0.1:8080;
    server 127.0.0.1:8081;
}

server {
    listen 443 ssl http2;
    server_name api.example.com;

    # TLS configuration
    ssl_certificate /etc/ssl/certs/api.example.com.crt;
    ssl_certificate_key /etc/ssl/private/api.example.com.key;
    include snippets/ssl-modern.conf;

    location / {
        # Proxy to HTTP backend
        proxy_pass http://backend;

        # Important: Tell backend original protocol was HTTPS
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Forwarded-Ssl on;

        include snippets/proxy-params.conf;
    }
}

# HTTP redirect
server {
    listen 80;
    server_name api.example.com;
    return 301 https://$server_name$request_uri;
}
```

---

### Pattern 3: Client Certificate Authentication (mTLS)

**Use Case:** Mutual TLS for service-to-service authentication

```nginx
server {
    listen 443 ssl http2;
    server_name internal-api.example.com;

    # Server certificate
    ssl_certificate /etc/ssl/certs/server.crt;
    ssl_certificate_key /etc/ssl/private/server.key;

    # CA certificate to verify client certs
    ssl_client_certificate /etc/ssl/certs/ca.crt;

    # Require valid client certificate
    ssl_verify_client on;
    ssl_verify_depth 2;

    include snippets/ssl-modern.conf;

    location / {
        proxy_pass http://backend;

        # Pass client cert info to backend
        proxy_set_header X-SSL-Client-Cert $ssl_client_cert;
        proxy_set_header X-SSL-Client-S-DN $ssl_client_s_dn;
        proxy_set_header X-SSL-Client-Verify $ssl_client_verify;

        include snippets/proxy-params.conf;
    }
}
```

---

## Performance Tuning

### Pattern 1: High-Performance Configuration

**Use Case:** Optimize for high-traffic sites

```nginx
# /etc/nginx/nginx.conf

user www-data;
worker_processes auto;  # 1 per CPU core
worker_rlimit_nofile 65535;
pid /run/nginx.pid;

events {
    worker_connections 4096;
    use epoll;  # Efficient event method (Linux)
    multi_accept on;
}

http {
    # Basic settings
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    keepalive_requests 100;
    types_hash_max_size 2048;
    server_tokens off;  # Hide nginx version

    # Buffer sizes
    client_body_buffer_size 128k;
    client_max_body_size 10m;
    client_header_buffer_size 1k;
    large_client_header_buffers 4 8k;
    output_buffers 2 32k;

    # Timeouts
    client_body_timeout 12;
    client_header_timeout 12;
    send_timeout 10;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript
               application/json application/javascript
               application/xml+rss application/atom+xml
               image/svg+xml;

    # File cache (open file descriptors)
    open_file_cache max=10000 inactive=20s;
    open_file_cache_valid 30s;
    open_file_cache_min_uses 2;
    open_file_cache_errors on;

    # Include configs
    include /etc/nginx/mime.types;
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

---

### Pattern 2: Proxy Caching

**Use Case:** Cache backend responses to reduce load

```nginx
# /etc/nginx/nginx.conf (http context)
http {
    # Define cache zone (100MB in memory, 1GB on disk)
    proxy_cache_path /var/cache/nginx/proxy
                     levels=1:2
                     keys_zone=app_cache:100m
                     max_size=1g
                     inactive=60m
                     use_temp_path=off;
}

# Server configuration
server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://backend;

        # Enable caching
        proxy_cache app_cache;
        proxy_cache_valid 200 60m;  # Cache 200 responses for 60 minutes
        proxy_cache_valid 404 10m;  # Cache 404 for 10 minutes
        proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
        proxy_cache_background_update on;
        proxy_cache_lock on;

        # Add cache status header
        add_header X-Cache-Status $upstream_cache_status;

        # Cache key (default: $scheme$proxy_host$request_uri)
        proxy_cache_key "$scheme$request_method$host$request_uri";

        include snippets/proxy-params.conf;
    }

    # Bypass cache for certain paths
    location /api/admin/ {
        proxy_pass http://backend;
        proxy_cache_bypass 1;  # Don't cache admin endpoints
        include snippets/proxy-params.conf;
    }

    # Cache purge endpoint (optional)
    location /cache-purge/ {
        proxy_cache_purge app_cache "$scheme$request_method$host$request_uri";
        access_log off;
    }
}
```

---

## Security Hardening

### Pattern 1: Rate Limiting

**Use Case:** Protect against DDoS and brute force

```nginx
# /etc/nginx/nginx.conf (http context)
http {
    # Define rate limit zones
    limit_req_zone $binary_remote_addr zone=general_limit:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=5r/s;
    limit_req_zone $binary_remote_addr zone=login_limit:10m rate=2r/m;

    # Connection limit zone
    limit_conn_zone $binary_remote_addr zone=conn_limit:10m;
}

# Server configuration
server {
    listen 80;
    server_name app.example.com;

    # Global rate limit
    limit_req zone=general_limit burst=20 nodelay;
    limit_conn conn_limit 10;  # Max 10 concurrent connections per IP

    # Main application
    location / {
        proxy_pass http://backend;
        include snippets/proxy-params.conf;
    }

    # API with stricter limits
    location /api/ {
        limit_req zone=api_limit burst=10 nodelay;
        proxy_pass http://backend;
        include snippets/proxy-params.conf;
    }

    # Login endpoint with very strict limit
    location /login {
        limit_req zone=login_limit burst=5 nodelay;
        proxy_pass http://backend;
        include snippets/proxy-params.conf;
    }
}
```

---

### Pattern 2: Security Headers

**Use Case:** Comprehensive security headers (OWASP recommendations)

```nginx
# /etc/nginx/snippets/security-headers.conf

# HSTS (HTTP Strict Transport Security)
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;

# Prevent clickjacking
add_header X-Frame-Options "SAMEORIGIN" always;

# Prevent MIME sniffing
add_header X-Content-Type-Options "nosniff" always;

# XSS Protection (legacy, but still useful)
add_header X-XSS-Protection "1; mode=block" always;

# Referrer policy
add_header Referrer-Policy "strict-origin-when-cross-origin" always;

# Content Security Policy (customize for your app)
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self'; frame-ancestors 'self';" always;

# Permissions Policy (formerly Feature-Policy)
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
```

**Usage:**
```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    include snippets/ssl-modern.conf;
    include snippets/security-headers.conf;

    # ... rest of config
}
```

---

### Pattern 3: Access Control

**Use Case:** IP-based access restrictions

```nginx
# Deny specific IPs
server {
    listen 80;
    server_name admin.example.com;

    # Deny specific IP
    deny 192.0.2.50;

    # Allow specific IP range
    allow 10.0.0.0/8;

    # Allow office IP
    allow 203.0.113.0/24;

    # Deny all others
    deny all;

    location / {
        proxy_pass http://admin_backend;
        include snippets/proxy-params.conf;
    }
}

# Allow only Cloudflare IPs (for sites behind Cloudflare)
server {
    listen 80;
    server_name example.com;

    # Cloudflare IPv4 ranges (example, update regularly)
    allow 173.245.48.0/20;
    allow 103.21.244.0/22;
    allow 103.22.200.0/22;
    # ... (full list: https://www.cloudflare.com/ips/)

    deny all;

    location / {
        # Restore original client IP from CF-Connecting-IP header
        real_ip_header CF-Connecting-IP;
        proxy_pass http://backend;
        include snippets/proxy-params.conf;
    }
}
```

---

## Caching Patterns

### Pattern 1: Browser Caching (Static Assets)

**Use Case:** Reduce bandwidth and improve page load times

```nginx
server {
    listen 80;
    server_name example.com;

    root /var/www/example.com;

    # HTML (no cache, must revalidate)
    location ~* \.(html)$ {
        expires -1;
        add_header Cache-Control "no-cache, must-revalidate";
    }

    # Images (1 year cache)
    location ~* \.(jpg|jpeg|png|gif|ico|svg|webp)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # CSS and JS (1 year with immutable)
    location ~* \.(css|js)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # Fonts (1 year)
    location ~* \.(woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # Media files (30 days)
    location ~* \.(mp4|webm|ogg|mp3|wav)$ {
        expires 30d;
        add_header Cache-Control "public";
        access_log off;
    }
}
```

---

### Pattern 2: FastCGI Cache (PHP)

**Use Case:** Cache PHP responses (WordPress, Laravel)

```nginx
# /etc/nginx/nginx.conf (http context)
http {
    # Define cache path
    fastcgi_cache_path /var/cache/nginx/fastcgi
                       levels=1:2
                       keys_zone=php_cache:100m
                       max_size=1g
                       inactive=60m
                       use_temp_path=off;
}

# Server configuration
server {
    listen 80;
    server_name blog.example.com;

    root /var/www/blog;
    index index.php;

    # Set cache bypass conditions
    set $skip_cache 0;

    # POST requests and URLs with query strings should always bypass cache
    if ($request_method = POST) {
        set $skip_cache 1;
    }
    if ($query_string != "") {
        set $skip_cache 1;
    }

    # Don't cache admin pages or logged-in users (WordPress example)
    if ($request_uri ~* "/wp-admin/|/xmlrpc.php|wp-.*.php|/feed/|index.php|sitemap(_index)?.xml") {
        set $skip_cache 1;
    }
    if ($http_cookie ~* "comment_author|wordpress_[a-f0-9]+|wp-postpass|wordpress_no_cache|wordpress_logged_in") {
        set $skip_cache 1;
    }

    location / {
        try_files $uri $uri/ /index.php?$args;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;

        # FastCGI cache
        fastcgi_cache php_cache;
        fastcgi_cache_valid 200 60m;
        fastcgi_cache_bypass $skip_cache;
        fastcgi_no_cache $skip_cache;

        # Add cache status header
        add_header X-Cache-Status $upstream_cache_status;
    }
}
```

---

## Skill Structure Design

### Proposed File Structure

```
configuring-nginx/
├── SKILL.md                          # Main skill file (400-500 lines)
│   ├── Purpose and Scope
│   ├── When to Use This Skill
│   ├── Quick Start Guide
│   │   ├── Installation
│   │   ├── Basic static site
│   │   ├── Reverse proxy setup
│   │   └── SSL/TLS quick start
│   ├── Decision Framework (nginx vs alternatives)
│   ├── Core Patterns (brief examples)
│   ├── Safety Checklist
│   └── References to Detailed Guides
│
├── reference/                        # Progressive disclosure
│   ├── installation-guide.md        # Install nginx on various OSes
│   ├── configuration-structure.md   # File structure, contexts, includes
│   ├── static-sites.md              # Static hosting patterns
│   ├── reverse-proxy.md             # Detailed proxy configurations
│   ├── load-balancing.md            # All LB algorithms and patterns
│   ├── ssl-tls-config.md            # SSL/TLS deep dive
│   ├── performance-tuning.md        # Worker processes, caching, compression
│   ├── security-hardening.md        # Rate limiting, headers, access control
│   ├── troubleshooting.md           # Common errors and debugging
│   └── nginx-plus-features.md       # Commercial features overview
│
├── examples/                         # Working configurations
│   ├── static-site/
│   │   ├── basic.conf
│   │   └── spa.conf
│   ├── reverse-proxy/
│   │   ├── nodejs-app.conf
│   │   ├── websocket.conf
│   │   └── api-gateway.conf
│   ├── load-balancing/
│   │   ├── round-robin.conf
│   │   ├── least-conn.conf
│   │   └── weighted.conf
│   ├── ssl-tls/
│   │   ├── modern-tls.conf
│   │   ├── mtls-client-cert.conf
│   │   └── tls-termination.conf
│   ├── performance/
│   │   ├── high-traffic.conf
│   │   ├── proxy-cache.conf
│   │   └── fastcgi-cache.conf
│   └── security/
│       ├── rate-limiting.conf
│       ├── security-headers.conf
│       └── access-control.conf
│
└── snippets/                         # Reusable config snippets
    ├── ssl-modern.conf
    ├── ssl-intermediate.conf
    ├── proxy-params.conf
    ├── security-headers.conf
    └── cache-static.conf
```

### SKILL.md Content Outline (400-500 lines)

```markdown
---
name: configuring-nginx
description: Configure nginx for static sites, reverse proxying, load balancing, SSL/TLS termination, caching, and performance tuning. Includes production-ready patterns with modern security best practices for TLS 1.3, rate limiting, and security headers.
---

# Configuring nginx

## Purpose
[2-3 sentences: nginx configuration for web serving, reverse proxy, load balancing]

## When to Use This Skill
[Trigger phrases and scenarios]

## Quick Start

### Installation
[One-liner install commands for Ubuntu, RHEL, Docker]

### Basic Static Site
[5-10 line example]
See reference/static-sites.md for complete guide

### Reverse Proxy Setup
[5-10 line example]
See reference/reverse-proxy.md for complete guide

### SSL/TLS Quick Start
[5-10 line example with Let's Encrypt]
See reference/ssl-tls-config.md for complete guide

## Decision Framework
[When to use nginx vs Apache/Caddy/Traefik]
See reference/decision-framework.md for detailed comparison

## Core Concepts

### Configuration Structure
[Brief overview of nginx.conf, server blocks, location blocks]
See reference/configuration-structure.md

### Location Matching Priority
[Quick reference for = ^~ ~ ~* / priority]

## Common Patterns

### Static Website Hosting
[Brief example]
See reference/static-sites.md

### Reverse Proxy
[Brief example with proxy headers]
See reference/reverse-proxy.md

### Load Balancing
[Quick round-robin example]
See reference/load-balancing.md for all algorithms

### SSL/TLS Configuration
[Modern TLS snippet]
See reference/ssl-tls-config.md

### Performance Tuning
[Key settings: worker_processes, gzip, caching]
See reference/performance-tuning.md

### Security Hardening
[Rate limiting, security headers]
See reference/security-hardening.md

## Safety Checklist
- [ ] Test configuration: sudo nginx -t
- [ ] Reload, don't restart: sudo systemctl reload nginx
- [ ] Check error logs: /var/log/nginx/error.log
- [ ] Verify SSL: openssl s_client -connect domain:443
- [ ] Test externally: curl -I https://domain.com

## Troubleshooting
See reference/troubleshooting.md

## Integration Points
- implementing-tls (SSL/TLS certificate management)
- load-balancing-patterns (advanced LB architecture)
- deploying-applications (application deployment with nginx)
- security-hardening (server security beyond nginx)
```

### Progressive Disclosure Strategy

**Level 1: SKILL.md (Always Loaded)**
- Purpose and when to use
- Quick start examples (installation, basic configs)
- Decision framework (nginx vs alternatives)
- Core concepts (brief overview)
- Common patterns (high-level, 5-10 lines each)
- Safety checklist
- References to detailed guides

**Level 2: reference/ (Loaded on Demand)**
- installation-guide.md: Detailed installation for all platforms
- configuration-structure.md: nginx.conf anatomy, contexts, includes
- static-sites.md: Complete static hosting patterns (basic, SPA, PHP)
- reverse-proxy.md: All proxy scenarios (apps, WebSocket, API gateway)
- load-balancing.md: All algorithms, health checks, sticky sessions
- ssl-tls-config.md: TLS 1.3 config, mTLS, OCSP stapling
- performance-tuning.md: Workers, caching, compression, buffers
- security-hardening.md: Rate limiting, headers, access control
- troubleshooting.md: Common errors, debugging techniques

**Level 3: examples/ and snippets/ (Referenced as Needed)**
- examples/: Complete working configurations to copy
- snippets/: Reusable config blocks to include

---

## Integration Points

### 1. implementing-tls Skill

**Relationship:** nginx uses certificates generated/managed by implementing-tls

**Integration:**
- implementing-tls generates certificates (certbot, cert-manager)
- configuring-nginx uses those certificates in SSL configuration
- implementing-tls handles renewal automation
- configuring-nginx focuses on nginx-specific TLS settings

**Cross-Reference:**
```markdown
# In implementing-tls/SKILL.md
## nginx SSL/TLS Configuration
For nginx-specific SSL configuration, see configuring-nginx skill.
Certificate paths for nginx:
- ssl_certificate /etc/letsencrypt/live/domain/fullchain.pem;
- ssl_certificate_key /etc/letsencrypt/live/domain/privkey.pem;

# In configuring-nginx/SKILL.md
## SSL/TLS Setup
For certificate generation and automation:
- Let's Encrypt with certbot → implementing-tls skill
- Kubernetes cert-manager → implementing-tls skill
- Internal CA setup → implementing-tls skill

This skill covers nginx SSL configuration only.
```

---

### 2. load-balancing-patterns Skill

**Relationship:** configuring-nginx covers nginx-specific LB config, load-balancing-patterns covers architecture

**Boundary:**
- configuring-nginx: nginx upstream blocks, algorithms, syntax
- load-balancing-patterns: L4 vs L7, cloud LBs, HAProxy, Envoy, decision frameworks

**Integration:**
```markdown
# In load-balancing-patterns/SKILL.md
## nginx Load Balancing
For detailed nginx load balancer configuration:
See configuring-nginx skill for:
- Upstream block syntax
- Health check configuration
- Sticky session patterns
- Keepalive connections

# In configuring-nginx/SKILL.md
## Load Balancing
For broader load balancing architecture:
- L4 vs L7 decision → load-balancing-patterns skill
- Cloud load balancers → load-balancing-patterns skill
- HAProxy/Envoy comparison → load-balancing-patterns skill
```

---

### 3. deploying-applications Skill

**Relationship:** Applications need nginx configured for serving/proxying

**Integration:**
```markdown
# In deploying-applications/SKILL.md
## Web Server Configuration
For nginx reverse proxy setup:
- See configuring-nginx skill for:
  - Reverse proxy configuration
  - WebSocket proxying
  - SSL/TLS termination
  - Performance tuning

# In configuring-nginx/SKILL.md
## Application Deployment
For application-specific deployment:
- Docker deployment → deploying-applications skill
- Kubernetes deployment → kubernetes-operations skill
- Process management (PM2, systemd) → deploying-applications skill
```

---

### 4. security-hardening Skill

**Relationship:** nginx is ONE component of server security

**Boundary:**
- configuring-nginx: nginx-specific security (rate limiting, headers, access control)
- security-hardening: Full server hardening (SSH, firewall, users, packages, fail2ban)

**Integration:**
```markdown
# In security-hardening/SKILL.md
## Web Server Security
For nginx-specific hardening:
See configuring-nginx skill for:
- Rate limiting configuration
- Security headers (HSTS, CSP, etc.)
- TLS configuration
- Access control (IP allow/deny)

# In configuring-nginx/SKILL.md
## Broader Security Context
nginx security is one layer. For complete server hardening:
- Firewall configuration → configuring-firewalls skill
- SSH hardening → security-hardening skill
- fail2ban integration → security-hardening skill
- OS-level security → security-hardening skill
```

---

### 5. configuring-firewalls Skill

**Relationship:** nginx needs firewall rules to be accessible

**Integration:**
```markdown
# In configuring-firewalls/SKILL.md
## Web Server Firewall Rules
For nginx servers, allow:
- Port 80 (HTTP)
- Port 443 (HTTPS)

Example (UFW):
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# In configuring-nginx/SKILL.md
## Network Access
Ensure firewall allows HTTP/HTTPS:
See configuring-firewalls skill for:
- UFW configuration (Ubuntu)
- iptables/nftables rules (Linux)
- AWS Security Groups (cloud)
```

---

## Implementation Roadmap

### Phase 1: Core SKILL.md (Week 1)
- [ ] Write SKILL.md main file (400-500 lines)
- [ ] Include decision framework
- [ ] Quick start examples (static, proxy, SSL)
- [ ] Safety checklist
- [ ] Cross-references to detailed guides

### Phase 2: Basic Patterns (Week 1-2)
- [ ] reference/installation-guide.md
- [ ] reference/configuration-structure.md
- [ ] reference/static-sites.md
- [ ] reference/reverse-proxy.md
- [ ] examples/static-site/
- [ ] examples/reverse-proxy/

### Phase 3: Advanced Features (Week 2)
- [ ] reference/load-balancing.md
- [ ] reference/ssl-tls-config.md
- [ ] reference/performance-tuning.md
- [ ] examples/load-balancing/
- [ ] examples/ssl-tls/
- [ ] snippets/ssl-modern.conf
- [ ] snippets/proxy-params.conf

### Phase 4: Security and Optimization (Week 2-3)
- [ ] reference/security-hardening.md
- [ ] reference/troubleshooting.md
- [ ] examples/performance/
- [ ] examples/security/
- [ ] snippets/security-headers.conf

### Phase 5: Testing & Iteration (Week 3)
- [ ] Test all configurations
- [ ] Verify SSL/TLS with SSL Labs
- [ ] Test performance with ab/wrk
- [ ] Validate against nginx -t
- [ ] Token count optimization

---

## Success Criteria

### Functionality
- ✅ Configurations work as copy-paste ready
- ✅ SSL/TLS configs pass Mozilla SSL Config Generator standards
- ✅ Load balancing examples distribute traffic correctly
- ✅ Security headers pass OWASP checks
- ✅ Performance tuning measurably improves throughput

### Quality
- ✅ SKILL.md under 500 lines
- ✅ All nginx configs syntactically valid (nginx -t passes)
- ✅ No time-sensitive information
- ✅ Consistent terminology throughout
- ✅ Examples use modern best practices (TLS 1.3, HTTP/2, etc.)

### Usability
- ✅ Quick start examples in main SKILL.md
- ✅ Progressive disclosure to detailed guides
- ✅ Clear troubleshooting section
- ✅ Safety checklist prevents configuration errors
- ✅ Integration points documented

---

## Key Takeaways

**This skill provides:**
- **nginx configuration** for all common use cases
- **Production-ready patterns** with security best practices
- **Modern TLS configuration** (TLS 1.3, OCSP stapling, security headers)
- **Performance tuning** (caching, compression, worker optimization)
- **Load balancing** (all algorithms, health checks, sticky sessions)

**Key differentiators:**
- **Practical focus**: Copy-paste ready configurations
- **Modern standards**: TLS 1.3, HTTP/2, security headers
- **Safety-first**: Test commands, reload vs restart, error checking
- **Progressive disclosure**: Quick start → detailed guides

**Integration:**
- Works with `implementing-tls` for certificate management
- Complements `load-balancing-patterns` for LB architecture
- Supports `deploying-applications` for app deployment
- Integrates with `security-hardening` for full server security

**Token efficiency:**
- Core guidance in SKILL.md (~2,500 tokens)
- Detailed references loaded on demand (~3,000 tokens)
- Complete examples in examples/ directory
- Total: 2,000-5,000 tokens (Low Level target achieved)

---

**Status:** Master Plan Complete ✅
**Next Step:** Implement SKILL.md using this plan
**Research Valid Until:** June 2026 (re-validate for nginx 2.x or major HTTP changes)
