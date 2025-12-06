# nginx Configuration Structure

Complete guide to nginx configuration file organization and syntax.

## Table of Contents

1. [Configuration File Hierarchy](#configuration-file-hierarchy)
2. [Context Levels](#context-levels)
3. [Configuration Directives](#configuration-directives)
4. [Include System](#include-system)
5. [Variables](#variables)
6. [Best Practices](#best-practices)

## Configuration File Hierarchy

### Standard Directory Structure

```
/etc/nginx/
├── nginx.conf                 # Main configuration file
├── mime.types                 # MIME type mappings
├── fastcgi.conf              # FastCGI parameters
├── fastcgi_params            # FastCGI parameters (legacy)
├── scgi_params               # SCGI parameters
├── uwsgi_params              # uWSGI parameters
├── modules-enabled/           # Enabled modules (symlinks)
│   └── 50-mod-http-geoip2.conf
├── modules-available/         # Available modules
│   └── mod-http-geoip2.conf
├── conf.d/                    # Additional configs (*.conf)
│   └── custom.conf
├── sites-enabled/             # Enabled sites (Debian/Ubuntu)
│   └── default -> ../sites-available/default
├── sites-available/           # Available site configs
│   ├── default
│   ├── example.com.conf
│   └── api.example.com.conf
└── snippets/                  # Reusable config snippets
    ├── ssl-params.conf
    ├── proxy-params.conf
    └── security-headers.conf
```

### Naming Conventions

**Site configuration files:**
- Use domain name: `example.com.conf`
- Include purpose: `api.example.com.conf`
- Avoid spaces: Use hyphens `my-site.conf`

**Snippets:**
- Descriptive names: `ssl-modern.conf`, `proxy-params.conf`
- Purpose-based: `security-headers.conf`, `cache-static.conf`

## Context Levels

nginx configuration uses nested contexts (blocks). Directives in outer contexts are inherited by inner contexts.

### Main Context (Global)

Top-level directives outside any block. Affect entire nginx instance.

```nginx
# User and group
user www-data;

# Worker processes (auto = 1 per CPU core)
worker_processes auto;

# Maximum open files per worker
worker_rlimit_nofile 65535;

# Error log
error_log /var/log/nginx/error.log warn;

# Process ID file
pid /run/nginx.pid;

# Include dynamic modules
include /etc/nginx/modules-enabled/*.conf;
```

### Events Context

Connection processing configuration. Single events block in main context.

```nginx
events {
    # Maximum connections per worker
    worker_connections 4096;

    # Connection processing method (Linux: epoll, BSD: kqueue)
    use epoll;

    # Accept multiple connections at once
    multi_accept on;

    # Accept mutex for connection distribution
    accept_mutex off;
}
```

### HTTP Context

HTTP-specific settings. Single http block in main context.

```nginx
http {
    # MIME types
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging format
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    # Performance settings
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    server_tokens off;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_types text/plain text/css application/json;

    # Rate limiting zones
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

    # Upstream definitions
    upstream backend {
        server 127.0.0.1:8080;
    }

    # Include server blocks
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

### Server Context (Virtual Host)

Defines a virtual host. Multiple server blocks allowed in http context.

```nginx
server {
    # Listen directives
    listen 80;
    listen [::]:80;

    # Server name (virtual host matching)
    server_name example.com www.example.com;

    # Document root
    root /var/www/example.com;

    # Default index files
    index index.html index.htm;

    # Access log (optional, overrides http-level)
    access_log /var/log/nginx/example.com.access.log;
    error_log /var/log/nginx/example.com.error.log;

    # Server-specific settings
    client_max_body_size 10m;

    # Location blocks
    location / {
        try_files $uri $uri/ =404;
    }
}
```

### Location Context (URL Routing)

URL-specific configuration. Multiple location blocks in server context.

```nginx
# Exact match
location = /api/status {
    return 200 "OK\n";
    add_header Content-Type text/plain;
}

# Prefix match with regex stop
location ^~ /static/ {
    root /var/www;
    expires 1y;
}

# Regex match (case-sensitive)
location ~ \.php$ {
    fastcgi_pass unix:/var/run/php/php-fpm.sock;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    include fastcgi_params;
}

# Regex match (case-insensitive)
location ~* \.(jpg|jpeg|png|gif|ico)$ {
    expires 30d;
    access_log off;
}

# Prefix match (lowest priority)
location / {
    proxy_pass http://backend;
    proxy_set_header Host $host;
}

# Named location (internal redirect only)
location @fallback {
    proxy_pass http://backup_backend;
}
```

### Upstream Context

Backend server definitions. Multiple upstream blocks in http context.

```nginx
upstream backend {
    # Load balancing method
    least_conn;

    # Backend servers
    server backend1.example.com:8080 weight=3;
    server backend2.example.com:8080 weight=2;
    server backend3.example.com:8080 backup;

    # Health checks
    server backend4.example.com:8080 max_fails=3 fail_timeout=30s;

    # Persistent connections
    keepalive 32;
    keepalive_timeout 60s;
    keepalive_requests 100;
}
```

### If Context

Conditional configuration. Use sparingly (can be inefficient).

```nginx
# Set variable based on condition
set $mobile_redirect 0;

if ($http_user_agent ~* (mobile|android|iphone)) {
    set $mobile_redirect 1;
}

if ($mobile_redirect = 1) {
    return 302 https://m.example.com$request_uri;
}
```

**Warning:** `if` in location context has limitations. Prefer `map` or `try_files` when possible.

## Configuration Directives

### Inheritance Rules

Directives in outer contexts are inherited by inner contexts unless overridden:

```nginx
http {
    # Applies to all servers
    client_max_body_size 10m;

    server {
        # Inherits 10m from http

        location /uploads {
            # Override for this location
            client_max_body_size 100m;
        }
    }
}
```

### Directive Types

**Simple directives:**
```nginx
worker_processes 4;
server_tokens off;
```

**Block directives:**
```nginx
server {
    # ...
}

location / {
    # ...
}
```

**Array directives:**
```nginx
listen 80;
listen [::]:80;
listen 443 ssl http2;
```

## Include System

Modularize configuration using includes:

### Including Files

```nginx
# Include single file
include /etc/nginx/mime.types;

# Include all files matching pattern
include /etc/nginx/conf.d/*.conf;
include /etc/nginx/sites-enabled/*;

# Include relative to nginx prefix
include conf.d/*.conf;
```

### Creating Reusable Snippets

**Example: `/etc/nginx/snippets/proxy-params.conf`**
```nginx
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_http_version 1.1;
proxy_set_header Connection "";
```

**Usage:**
```nginx
location / {
    proxy_pass http://backend;
    include snippets/proxy-params.conf;
}
```

### Site Management (Debian/Ubuntu)

Enable/disable sites without editing main config:

```bash
# Create site configuration
sudo nano /etc/nginx/sites-available/example.com

# Enable site (create symlink)
sudo ln -s /etc/nginx/sites-available/example.com /etc/nginx/sites-enabled/

# Disable site (remove symlink)
sudo rm /etc/nginx/sites-enabled/example.com

# Test and reload
sudo nginx -t && sudo systemctl reload nginx
```

## Variables

### Built-in Variables

**Request variables:**
```nginx
$request_uri          # Full original request URI
$uri                  # Normalized URI
$request_method       # GET, POST, etc.
$args                 # Query string
$arg_name             # Specific query parameter
$is_args              # "?" if query string exists
$request_body         # Request body
$content_type         # Content-Type header
$content_length       # Content-Length header
```

**Connection variables:**
```nginx
$remote_addr          # Client IP address
$remote_port          # Client port
$remote_user          # HTTP auth username
$server_addr          # Server IP address
$server_port          # Server port
$server_protocol      # HTTP/1.0, HTTP/1.1, HTTP/2.0
```

**Response variables:**
```nginx
$status               # Response status code
$body_bytes_sent      # Bytes sent to client
$bytes_sent           # Total bytes sent (headers + body)
$connection           # Connection serial number
$connection_requests  # Request count in connection
$msec                 # Current Unix time
$request_time         # Request processing time
$upstream_response_time  # Time to receive upstream response
```

**Headers:**
```nginx
$http_user_agent      # User-Agent header
$http_referer         # Referer header
$http_host            # Host header
$http_cookie          # Cookie header
$http_x_forwarded_for # X-Forwarded-For header
```

**SSL/TLS:**
```nginx
$ssl_protocol         # TLS protocol version
$ssl_cipher           # Cipher suite
$ssl_client_cert      # Client certificate
$ssl_client_s_dn      # Client DN
$ssl_session_id       # SSL session ID
```

### Custom Variables

Define custom variables using `set`:

```nginx
server {
    # Set variable
    set $backend_server backend1.example.com;

    # Use variable
    proxy_pass http://$backend_server;
}
```

### Map Directive

Create variables based on other variables:

```nginx
http {
    # Map user agent to backend
    map $http_user_agent $backend {
        default         backend_web;
        ~*mobile        backend_mobile;
        ~*bot           backend_bot;
    }

    server {
        location / {
            proxy_pass http://$backend;
        }
    }
}
```

## Best Practices

### Organization

1. **Keep main nginx.conf minimal** - Include only global settings
2. **Use sites-available/sites-enabled pattern** - Easy site management
3. **Create reusable snippets** - DRY principle
4. **One site per file** - Better organization
5. **Use descriptive filenames** - `api.example.com.conf`, not `site1.conf`

### Comments

```nginx
# Single-line comment
server {
    listen 80;  # Inline comment

    # Multi-line explanation
    # This location handles API requests
    # and proxies to the backend
    location /api/ {
        proxy_pass http://backend;
    }
}
```

### Testing

Always test before reloading:

```bash
# Test configuration syntax
sudo nginx -t

# View complete configuration (includes resolved)
sudo nginx -T

# Reload if test passes
sudo nginx -t && sudo systemctl reload nginx
```

### Version Control

Track configuration in git:

```bash
cd /etc/nginx
git init
git add .
git commit -m "Initial nginx configuration"

# After changes
git diff
git add sites-available/new-site.conf
git commit -m "Add new-site configuration"
```

### Security

1. **Hide nginx version:** `server_tokens off;`
2. **Set appropriate permissions:**
   ```bash
   sudo chown -R root:root /etc/nginx
   sudo chmod -R 644 /etc/nginx
   sudo chmod 755 /etc/nginx /etc/nginx/sites-available /etc/nginx/sites-enabled
   ```
3. **Protect sensitive files:**
   ```bash
   sudo chmod 600 /etc/nginx/ssl/*.key
   ```

### Performance

1. **Use worker_processes auto** - Automatic CPU core detection
2. **Tune worker_connections** - Based on expected traffic
3. **Enable gzip compression** - Reduce bandwidth
4. **Use proxy caching** - Reduce backend load
5. **Minimize includes** - Reduces config parsing time

## Example: Complete Configuration Structure

```nginx
# /etc/nginx/nginx.conf (main)
user www-data;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /run/nginx.pid;

events {
    worker_connections 4096;
    use epoll;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    keepalive_timeout 65;
    gzip on;

    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

```nginx
# /etc/nginx/sites-available/example.com
server {
    listen 80;
    server_name example.com www.example.com;

    root /var/www/example.com;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    include snippets/security-headers.conf;
}
```

Enable and test:
```bash
sudo ln -s /etc/nginx/sites-available/example.com /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```
