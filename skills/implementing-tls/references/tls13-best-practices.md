# TLS 1.3 Best Practices and Configuration

Guide to configuring TLS 1.3 for optimal security and performance.

## Table of Contents

1. [Why TLS 1.3](#why-tls-13)
2. [Protocol Configuration](#protocol-configuration)
3. [Cipher Suite Selection](#cipher-suite-selection)
4. [Security Features](#security-features)
5. [Performance Optimization](#performance-optimization)

## Why TLS 1.3

### Key Improvements Over TLS 1.2

**Performance:**
- **Faster handshake**: 1-RTT instead of 2-RTT (50% faster)
- **0-RTT resumption**: Zero round-trip time for repeat connections
- **Reduced latency**: 100-200ms saved per connection

**Security:**
- **Forward secrecy mandatory**: All cipher suites use ephemeral keys
- **Encrypted handshake**: More of the handshake is encrypted
- **Simplified cipher suites**: Removed weak algorithms
- **Downgrade protection**: Prevents protocol downgrade attacks

**Removed Vulnerabilities:**
- No RSA key transport (forward secrecy required)
- No static DH/ECDH
- No CBC mode ciphers (BEAST, Lucky13 attacks)
- No MD5, SHA-1, RC4, 3DES
- No compression (CRIME attack)
- No renegotiation

### TLS 1.3 vs TLS 1.2 Handshake

**TLS 1.2 (2-RTT):**
```
Client                          Server
  |--- ClientHello ------------->|
  |<-- ServerHello, Certificate -|
  |<-- ServerHelloDone ----------|
  |--- ClientKeyExchange ------->|
  |--- Finished ---------------->|
  |<-- Finished -----------------|
  |=== Application Data ========>|

Total: 2 round trips before data
```

**TLS 1.3 (1-RTT):**
```
Client                          Server
  |--- ClientHello + KeyShare -->|
  |<-- ServerHello, Certificate -|
  |<-- Finished -----------------|
  |=== Application Data ========>|
  |--- Finished ---------------->|

Total: 1 round trip before data
```

**TLS 1.3 with 0-RTT Resumption:**
```
Client                          Server
  |--- ClientHello + Early Data >|
  |=== Application Data ========>|  (sent immediately!)
  |<-- ServerHello ---------------|
  |<-- Finished -----------------|

Total: 0 round trips (but replay risk)
```

## Protocol Configuration

### Nginx Configuration

**Recommended TLS 1.3 configuration:**

```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    # Certificate files
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;

    # Protocol versions (TLS 1.3 + TLS 1.2 fallback)
    ssl_protocols TLSv1.3 TLSv1.2;

    # Let client choose cipher (modern best practice)
    ssl_prefer_server_ciphers off;

    # TLS 1.3 cipher suites (optional - defaults are good)
    ssl_ciphersuites TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256;

    # TLS 1.2 cipher suites (fallback)
    ssl_ciphers 'ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-CHACHA20-POLY1305';

    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/ssl/certs/chain.pem;
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;

    # Session resumption
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_session_tickets off;  # Disable for perfect forward secrecy

    # HSTS (force HTTPS)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    location / {
        proxy_pass http://backend;
    }
}

# HTTP to HTTPS redirect
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

### Apache Configuration

```apache
<VirtualHost *:443>
    ServerName example.com

    # Certificate files
    SSLCertificateFile /etc/ssl/certs/example.com.crt
    SSLCertificateKeyFile /etc/ssl/private/example.com.key
    SSLCertificateChainFile /etc/ssl/certs/chain.pem

    # Protocol versions
    SSLProtocol -all +TLSv1.3 +TLSv1.2

    # Cipher suites
    SSLCipherSuite TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256
    SSLCipherSuite ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-CHACHA20-POLY1305

    # Prefer client cipher order (modern)
    SSLHonorCipherOrder off

    # OCSP stapling
    SSLUseStapling on
    SSLStaplingCache "shmcb:logs/ssl_stapling(32768)"

    # Session resumption
    SSLSessionCache "shmcb:logs/ssl_scache(512000)"
    SSLSessionCacheTimeout 300

    # HSTS
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
</VirtualHost>
```

### HAProxy Configuration

```haproxy
frontend https_front
    bind *:443 ssl crt /etc/ssl/certs/example.com.pem ssl-min-ver TLSv1.2 alpn h2,http/1.1

    # TLS 1.3 cipher suites
    ssl-default-bind-ciphersuites TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256

    # TLS 1.2 ciphers
    ssl-default-bind-ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-CHACHA20-POLY1305

    # Security options
    ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets

    # HSTS
    http-response set-header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"

    default_backend web_servers
```

## Cipher Suite Selection

### TLS 1.3 Cipher Suites

Only 5 cipher suites in TLS 1.3 (all AEAD):

```
TLS_AES_256_GCM_SHA384           - AES-256 with GCM mode
TLS_CHACHA20_POLY1305_SHA256     - ChaCha20-Poly1305 (mobile-optimized)
TLS_AES_128_GCM_SHA256           - AES-128 with GCM mode (performance)
TLS_AES_128_CCM_SHA256           - AES-128 with CCM (constrained devices)
TLS_AES_128_CCM_8_SHA256         - AES-128 with CCM-8 (IoT)
```

**Recommended order:**

```nginx
# Let client choose (modern approach)
ssl_prefer_server_ciphers off;
ssl_ciphersuites TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256;
```

**Cipher characteristics:**

| Cipher | Security | Performance | Mobile | Notes |
|--------|----------|-------------|--------|-------|
| TLS_AES_256_GCM_SHA384 | Highest | Good (AES-NI) | Good | Strongest encryption |
| TLS_CHACHA20_POLY1305_SHA256 | High | Excellent | Best | Fast on ARM/mobile |
| TLS_AES_128_GCM_SHA256 | High | Best (AES-NI) | Good | Balanced choice |
| TLS_AES_128_CCM_* | High | Moderate | Good | IoT/constrained devices |

### TLS 1.2 Cipher Suites (Fallback)

**Recommended for compatibility:**

```
ECDHE-RSA-AES256-GCM-SHA384
ECDHE-RSA-AES128-GCM-SHA256
ECDHE-RSA-CHACHA20-POLY1305
```

**What to disable:**

```
# Disable weak ciphers
ssl_ciphers '!RC4:!DES:!3DES:!MD5:!SHA1:!aNULL:!eNULL:!EXPORT';

# Specific ciphers to avoid:
- RC4 (broken)
- DES, 3DES (too weak)
- MD5, SHA-1 (collision attacks)
- CBC mode (BEAST, Lucky13)
- RSA key transport (no forward secrecy)
- Export ciphers (intentionally weak)
- Anonymous ciphers (no authentication)
```

### Verify Cipher Configuration

```bash
# Test with OpenSSL
openssl s_client -connect example.com:443 -tls1_3

# Check negotiated cipher
# Look for "Cipher    : TLS_AES_256_GCM_SHA384"

# Test specific cipher
openssl s_client -connect example.com:443 \
  -tls1_3 -ciphersuites 'TLS_AES_256_GCM_SHA384'

# Test with nmap
nmap --script ssl-enum-ciphers -p 443 example.com

# Test with testssl.sh
./testssl.sh example.com
```

## Security Features

### OCSP Stapling

**What it does:**
- Server fetches OCSP response from CA
- Staples (includes) response in TLS handshake
- Client doesn't need to contact CA (privacy + performance)

**Nginx configuration:**

```nginx
ssl_stapling on;
ssl_stapling_verify on;
ssl_trusted_certificate /etc/ssl/certs/chain.pem;
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;
```

**Verify OCSP stapling:**

```bash
openssl s_client -connect example.com:443 -status

# Look for:
# OCSP Response Status: successful (0x0)
# Cert Status: good
```

### HSTS (HTTP Strict Transport Security)

**Force HTTPS for all connections:**

```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
```

**Parameters:**
- `max-age=31536000`: Cache for 1 year (seconds)
- `includeSubDomains`: Apply to all subdomains
- `preload`: Submit to HSTS preload list (browsers)

**Preload list submission:**
Visit: https://hstspreload.org/

### Session Resumption

**Session cache (server-side):**

```nginx
# Shared cache across workers
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;

# Disable session tickets (better forward secrecy)
ssl_session_tickets off;
```

**Why disable session tickets:**
- Session tickets stored client-side
- Encrypted with server's ticket key
- If ticket key compromised, past sessions compromised
- Disabling improves forward secrecy

### Perfect Forward Secrecy (PFS)

**Ensured in TLS 1.3** (all cipher suites use ephemeral keys).

**TLS 1.2 requires ECDHE or DHE:**

```nginx
# PFS-enabled ciphers only
ssl_ciphers 'ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256';
```

**Verify PFS:**

```bash
openssl s_client -connect example.com:443 | grep "Server Temp Key"

# Should show: Server Temp Key: ECDH, X25519, 253 bits
# Not: No server temp key (no PFS)
```

### Certificate Transparency

**Required for public certificates (2018+):**

All certificates issued by public CAs are logged to public CT logs.

**Check CT logs:**
- https://crt.sh/
- https://transparencyreport.google.com/https/certificates

**Nginx expects CT via OCSP stapling:**
```nginx
ssl_stapling on;
ssl_stapling_verify on;
```

### 0-RTT Resumption (Use with Caution)

**Benefits:**
- Zero round-trip time for repeat connections
- Fastest possible resumption

**Risks:**
- Vulnerable to replay attacks
- Early data can be replayed by attacker
- Only use for idempotent requests (GET, not POST)

**Nginx configuration:**

```nginx
ssl_early_data on;

# Pass header to backend
location / {
    proxy_pass http://backend;
    proxy_set_header Early-Data $ssl_early_data;
}
```

**Application must check:**

```python
# Python/Flask example
@app.before_request
def check_early_data():
    if request.headers.get('Early-Data') == '1':
        # Only allow safe methods
        if request.method not in ['GET', 'HEAD', 'OPTIONS']:
            abort(425, "Too Early")
```

**When to disable 0-RTT:**
- APIs with state-changing operations
- Authentication endpoints
- Payment processing
- High-security applications

## Performance Optimization

### HTTP/2 and HTTP/3

**HTTP/2 over TLS 1.3:**

```nginx
listen 443 ssl http2;
ssl_protocols TLSv1.3 TLSv1.2;
```

**HTTP/3 (QUIC) support:**

```nginx
# Nginx 1.25.0+
listen 443 quic reuseport;
listen 443 ssl http2;

# Advertise HTTP/3 availability
add_header Alt-Svc 'h3=":443"; ma=86400';
```

### Session Cache Tuning

```nginx
# Shared cache for multiple workers
ssl_session_cache shared:SSL:10m;  # 10MB = ~40,000 sessions
ssl_session_timeout 10m;

# Monitor cache usage
# Check Nginx error log for "session cache size" messages
```

### Hardware Acceleration

**Enable AES-NI (Intel/AMD CPUs):**

```bash
# Check if AES-NI available
grep -o aes /proc/cpuinfo | wc -l
# > 0 means available

# Nginx automatically uses AES-NI if available
# OpenSSL 1.0.1+ required
openssl version
```

**Benchmark:**

```bash
# Test AES-128-GCM performance
openssl speed -evp aes-128-gcm

# Test ChaCha20-Poly1305 performance
openssl speed chacha20-poly1305
```

### Connection Reuse

```nginx
# Keep connections alive
keepalive_timeout 65;
keepalive_requests 100;

# Upstream keepalive (to backend)
upstream backend {
    server 10.0.0.1:8080;
    keepalive 32;  # Keep 32 connections per worker
}
```

## Testing and Validation

### SSL Labs Test

```
Visit: https://www.ssllabs.com/ssltest/analyze.html?d=example.com

Target rating: A+ (with HSTS preload)
```

### testssl.sh (Command-Line)

```bash
git clone https://github.com/drwetter/testssl.sh.git
cd testssl.sh

# Full test
./testssl.sh example.com

# Quick test
./testssl.sh --fast example.com

# Check specific features
./testssl.sh --protocols example.com
./testssl.sh --cipher example.com
./testssl.sh --pfs example.com
```

### Verify Configuration

```bash
# Check TLS 1.3 support
openssl s_client -connect example.com:443 -tls1_3

# Verify cipher
echo | openssl s_client -connect example.com:443 2>/dev/null | \
  grep "Cipher"

# Check certificate chain
openssl s_client -connect example.com:443 -showcerts

# Verify OCSP stapling
openssl s_client -connect example.com:443 -status | \
  grep "OCSP Response Status"

# Check HSTS header
curl -I https://example.com | grep -i strict-transport
```

## Best Practices Summary

1. **Enable TLS 1.3 and 1.2 only** (disable 1.1, 1.0, SSLv3)
2. **Let client choose cipher** (ssl_prefer_server_ciphers off)
3. **Use strong cipher suites** (AES-GCM, ChaCha20-Poly1305)
4. **Enable OCSP stapling** (privacy + performance)
5. **Implement HSTS** (force HTTPS)
6. **Disable session tickets** (better forward secrecy)
7. **Use HTTP/2** (multiplexing, header compression)
8. **Short certificate lifetimes** (90 days or less)
9. **Monitor certificate expiry** (alert 7-30 days before)
10. **Regular security testing** (SSL Labs, testssl.sh)
11. **Keep OpenSSL updated** (security patches)
12. **Use 0-RTT cautiously** (replay attack risk)

## Common Mistakes to Avoid

1. **Enabling TLS 1.0/1.1** (insecure, deprecated)
2. **Weak cipher suites** (RC4, 3DES, CBC mode)
3. **Missing intermediate certificates** (chain incomplete)
4. **Long certificate lifetimes** (>1 year is suspicious)
5. **No HSTS** (allows downgrade attacks)
6. **Self-signed certs in production** (browser warnings)
7. **Ignoring OCSP/CRL** (revoked certs still work)
8. **Static session keys** (no forward secrecy)
9. **Compression enabled** (CRIME attack)
10. **Renegotiation allowed** (DoS risk)

## Migration Checklist

Migrating from TLS 1.2 to TLS 1.3:

- [ ] Update OpenSSL to 1.1.1+ (TLS 1.3 support)
- [ ] Update web server (Nginx 1.13+, Apache 2.4.37+)
- [ ] Configure ssl_protocols (add TLSv1.3)
- [ ] Test with modern clients (Chrome, Firefox, curl)
- [ ] Monitor for connection failures (old clients)
- [ ] Verify performance improvement (1-RTT handshake)
- [ ] Consider 0-RTT for read-only endpoints
- [ ] Update monitoring (track TLS version usage)

For certificate generation and renewal, see `certificate-generation.md` and `automation-patterns.md`.
