# SSL/TLS Configuration for nginx

Modern SSL/TLS configuration patterns.


## Table of Contents

- [Modern TLS Configuration (2025)](#modern-tls-configuration-2025)
- [Reusable SSL Snippet](#reusable-ssl-snippet)
- [Let's Encrypt Integration](#lets-encrypt-integration)
  - [Certbot Installation](#certbot-installation)
  - [Obtain Certificate](#obtain-certificate)
  - [Auto-Renewal](#auto-renewal)
- [Client Certificate Authentication (mTLS)](#client-certificate-authentication-mtls)
- [Testing SSL/TLS](#testing-ssltls)

## Modern TLS Configuration (2025)

Recommended for compatibility and security:

```nginx
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name example.com;

    # Certificate files
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/example.com/chain.pem;

    # Protocols (TLS 1.2 and 1.3)
    ssl_protocols TLSv1.3 TLSv1.2;

    # Cipher suites
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305';
    ssl_prefer_server_ciphers off;

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

    location / {
        root /var/www/example.com;
        index index.html;
    }
}

# HTTP to HTTPS redirect
server {
    listen 80;
    listen [::]:80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

## Reusable SSL Snippet

Create `/etc/nginx/snippets/ssl-modern.conf`:

```nginx
# Protocols
ssl_protocols TLSv1.3 TLSv1.2;

# Ciphers
ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305';
ssl_prefer_server_ciphers off;

# Session resumption
ssl_session_cache shared:SSL:50m;
ssl_session_timeout 1d;
ssl_session_tickets off;

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;

# HSTS
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
```

Usage:
```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    include snippets/ssl-modern.conf;

    location / {
        # ...
    }
}
```

## Let's Encrypt Integration

### Certbot Installation

```bash
# Ubuntu/Debian
sudo apt install certbot python3-certbot-nginx

# RHEL/CentOS
sudo dnf install certbot python3-certbot-nginx
```

### Obtain Certificate

```bash
# Automatic configuration
sudo certbot --nginx -d example.com -d www.example.com

# Manual certificate only
sudo certbot certonly --nginx -d example.com -d www.example.com
```

### Auto-Renewal

```bash
# Test renewal
sudo certbot renew --dry-run

# Automatic renewal (systemd timer)
sudo systemctl enable certbot-renew.timer
sudo systemctl start certbot-renew.timer
```

## Client Certificate Authentication (mTLS)

Mutual TLS for service-to-service authentication:

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

## Testing SSL/TLS

```bash
# Test SSL connection
openssl s_client -connect example.com:443 -servername example.com

# Check certificate
openssl s_client -connect example.com:443 -servername example.com < /dev/null | openssl x509 -text

# Test with curl
curl -vI https://example.com

# SSL Labs test
# Visit: https://www.ssllabs.com/ssltest/analyze.html?d=example.com
```
