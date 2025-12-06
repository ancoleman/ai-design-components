# nginx Security Hardening

Security best practices for nginx deployments.


## Table of Contents

- [Rate Limiting](#rate-limiting)
  - [Basic Rate Limiting](#basic-rate-limiting)
  - [Custom Error Response](#custom-error-response)
- [Security Headers](#security-headers)
- [Access Control](#access-control)
  - [IP-Based Restrictions](#ip-based-restrictions)
  - [Geo-Based Blocking](#geo-based-blocking)
- [Hide Server Information](#hide-server-information)
- [Disable Unwanted HTTP Methods](#disable-unwanted-http-methods)
- [Prevent Hotlinking](#prevent-hotlinking)
- [File Upload Security](#file-upload-security)
- [Protect Sensitive Files](#protect-sensitive-files)
- [Block User Agents](#block-user-agents)
- [DDoS Protection](#ddos-protection)
  - [Connection Limits](#connection-limits)
  - [Slowloris Protection](#slowloris-protection)
- [SSL/TLS Security](#ssltls-security)
- [ModSecurity WAF (Optional)](#modsecurity-waf-optional)
- [Security Checklist](#security-checklist)

## Rate Limiting

Protect against DDoS and brute force attacks:

### Basic Rate Limiting

```nginx
http {
    # Define rate limit zones
    limit_req_zone $binary_remote_addr zone=general_limit:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=5r/s;
    limit_req_zone $binary_remote_addr zone=login_limit:10m rate=2r/m;

    # Connection limit
    limit_conn_zone $binary_remote_addr zone=conn_limit:10m;
}

server {
    listen 80;

    # Global rate limit
    limit_req zone=general_limit burst=20 nodelay;
    limit_conn conn_limit 10;

    location / {
        proxy_pass http://backend;
    }

    # API with stricter limits
    location /api/ {
        limit_req zone=api_limit burst=10 nodelay;
        proxy_pass http://backend;
    }

    # Login endpoint
    location /login {
        limit_req zone=login_limit burst=5 nodelay;
        proxy_pass http://backend;
    }
}
```

### Custom Error Response

```nginx
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=5r/s;
limit_req_status 429;

server {
    location /api/ {
        limit_req zone=api_limit burst=10 nodelay;

        error_page 429 = @rate_limited;
        proxy_pass http://backend;
    }

    location @rate_limited {
        return 429 '{"error": "Rate limit exceeded", "retry_after": 60}\n';
        add_header Content-Type application/json;
    }
}
```

## Security Headers

OWASP recommended security headers:

Create `/etc/nginx/snippets/security-headers.conf`:

```nginx
# HSTS (HTTP Strict Transport Security)
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;

# Prevent clickjacking
add_header X-Frame-Options "SAMEORIGIN" always;

# Prevent MIME sniffing
add_header X-Content-Type-Options "nosniff" always;

# XSS Protection
add_header X-XSS-Protection "1; mode=block" always;

# Referrer policy
add_header Referrer-Policy "strict-origin-when-cross-origin" always;

# Content Security Policy (customize for your app)
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self'; frame-ancestors 'self';" always;

# Permissions Policy
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
```

Usage:
```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    include snippets/security-headers.conf;

    location / {
        # ...
    }
}
```

## Access Control

### IP-Based Restrictions

```nginx
server {
    listen 80;
    server_name admin.example.com;

    # Allow specific IPs
    allow 10.0.0.0/8;
    allow 203.0.113.0/24;

    # Deny all others
    deny all;

    location / {
        proxy_pass http://admin_backend;
    }
}
```

### Geo-Based Blocking

```nginx
http {
    # Requires geoip module
    geoip_country /usr/share/GeoIP/GeoIP.dat;

    map $geoip_country_code $allowed_country {
        default no;
        US yes;
        CA yes;
        GB yes;
    }

    server {
        listen 80;

        if ($allowed_country = no) {
            return 403;
        }

        location / {
            proxy_pass http://backend;
        }
    }
}
```

## Hide Server Information

```nginx
http {
    # Hide nginx version
    server_tokens off;

    # Remove Server header entirely (requires headers-more module)
    more_clear_headers 'Server';
}
```

## Disable Unwanted HTTP Methods

```nginx
server {
    listen 80;

    # Only allow GET, POST, HEAD
    if ($request_method !~ ^(GET|POST|HEAD)$) {
        return 405;
    }

    location / {
        proxy_pass http://backend;
    }
}
```

## Prevent Hotlinking

```nginx
location ~* \.(jpg|jpeg|png|gif)$ {
    valid_referers none blocked server_names
                   *.example.com example.com;

    if ($invalid_referer) {
        return 403;
    }
}
```

## File Upload Security

```nginx
server {
    # Limit upload size
    client_max_body_size 10m;

    # Limit upload speed
    limit_rate 500k;

    # File upload location
    location /upload {
        # Only allow POST
        if ($request_method != POST) {
            return 405;
        }

        proxy_pass http://upload_backend;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Protect Sensitive Files

```nginx
# Deny access to hidden files
location ~ /\. {
    deny all;
    access_log off;
    log_not_found off;
}

# Deny access to backup files
location ~* \.(bak|config|sql|fla|psd|ini|log|sh|inc|swp|dist)$ {
    deny all;
}

# Protect specific directories
location ~* /(uploads|files)/.*\.(php|php5|php7|phtml)$ {
    deny all;
}
```

## Block User Agents

```nginx
# Block bad bots
if ($http_user_agent ~* (scrapy|curl|wget|python-requests)) {
    return 403;
}

# Or use map
map $http_user_agent $bad_bot {
    default 0;
    ~*scrapy 1;
    ~*curl 1;
    ~*wget 1;
}

server {
    if ($bad_bot) {
        return 403;
    }
}
```

## DDoS Protection

### Connection Limits

```nginx
http {
    limit_conn_zone $binary_remote_addr zone=addr:10m;
    limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;

    server {
        location / {
            limit_conn addr 10;
            limit_req zone=one burst=5;
            proxy_pass http://backend;
        }
    }
}
```

### Slowloris Protection

```nginx
http {
    client_body_timeout 10s;
    client_header_timeout 10s;
    keepalive_timeout 5s 5s;
    send_timeout 10s;
}
```

## SSL/TLS Security

See `ssl-tls-config.md` for complete TLS configuration.

## ModSecurity WAF (Optional)

Web Application Firewall integration:

```bash
# Install ModSecurity
sudo apt install libmodsecurity3 libnginx-mod-http-modsecurity

# Enable in nginx
load_module modules/ngx_http_modsecurity_module.so;

http {
    modsecurity on;
    modsecurity_rules_file /etc/nginx/modsec/main.conf;
}
```

## Security Checklist

- [ ] Enable SSL/TLS with modern configuration
- [ ] Add security headers
- [ ] Implement rate limiting
- [ ] Hide server version and information
- [ ] Restrict access by IP for admin panels
- [ ] Disable unwanted HTTP methods
- [ ] Protect sensitive files
- [ ] Limit file upload sizes
- [ ] Configure timeouts to prevent slowloris
- [ ] Regular security updates: `sudo apt update && sudo apt upgrade nginx`
- [ ] Monitor logs for suspicious activity
- [ ] Use fail2ban for automated blocking
