# nginx Troubleshooting Guide

Common issues and solutions.


## Table of Contents

- [Configuration Errors](#configuration-errors)
  - [Test Configuration](#test-configuration)
  - [Common Syntax Errors](#common-syntax-errors)
- [Common HTTP Errors](#common-http-errors)
  - [502 Bad Gateway](#502-bad-gateway)
  - [503 Service Unavailable](#503-service-unavailable)
  - [504 Gateway Timeout](#504-gateway-timeout)
  - [413 Request Entity Too Large](#413-request-entity-too-large)
  - [404 Not Found](#404-not-found)
- [Port and Binding Issues](#port-and-binding-issues)
  - ["Address already in use"](#address-already-in-use)
  - [Permission Denied](#permission-denied)
- [SSL/TLS Issues](#ssltls-issues)
  - [Certificate Not Found](#certificate-not-found)
  - [SSL Handshake Failure](#ssl-handshake-failure)
- [Performance Issues](#performance-issues)
  - [High Memory Usage](#high-memory-usage)
  - [High CPU Usage](#high-cpu-usage)
- [Connection Issues](#connection-issues)
  - [Connection Refused](#connection-refused)
  - [Connection Reset](#connection-reset)
- [Logging and Debugging](#logging-and-debugging)
  - [Enable Debug Logging](#enable-debug-logging)
  - [View Logs](#view-logs)
  - [Custom Log Format](#custom-log-format)
- [Service Management Issues](#service-management-issues)
  - [nginx Not Starting](#nginx-not-starting)
  - [Can't Reload Configuration](#cant-reload-configuration)
- [Quick Diagnostics](#quick-diagnostics)

## Configuration Errors

### Test Configuration

Always test before reloading:

```bash
# Test configuration
sudo nginx -t

# View complete configuration
sudo nginx -T

# Reload if test passes
sudo nginx -t && sudo systemctl reload nginx
```

### Common Syntax Errors

**Missing semicolon:**
```nginx
# Wrong
server {
    listen 80
}

# Correct
server {
    listen 80;
}
```

**Invalid directive:**
```nginx
# Check spelling and context
proxy_pass http://backend;  # Correct
proxy-pass http://backend;  # Wrong (dash instead of underscore)
```

## Common HTTP Errors

### 502 Bad Gateway

Backend server not reachable or not running.

**Check backend:**
```bash
# Is backend running?
curl http://127.0.0.1:3000

# Check process
ps aux | grep node  # or python, ruby, etc.

# Check logs
sudo journalctl -u myapp -f
```

**Fix SELinux (RHEL/CentOS):**
```bash
# Allow nginx to connect to network
sudo setsebool -P httpd_can_network_connect 1
```

### 503 Service Unavailable

All backend servers are down or unreachable.

**Check upstream configuration:**
```nginx
upstream backend {
    server 127.0.0.1:8080 max_fails=3 fail_timeout=30s;
}
```

**Reset failure count:**
```bash
sudo systemctl reload nginx
```

### 504 Gateway Timeout

Backend taking too long to respond.

**Increase timeouts:**
```nginx
location / {
    proxy_pass http://backend;
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 300s;  # 5 minutes
}
```

### 413 Request Entity Too Large

File upload exceeds limit.

**Increase upload size:**
```nginx
server {
    client_max_body_size 100m;
}
```

### 404 Not Found

File or location not found.

**Check root path:**
```nginx
server {
    root /var/www/example.com;  # Verify path exists

    location / {
        try_files $uri $uri/ =404;
    }
}
```

**Verify file permissions:**
```bash
ls -la /var/www/example.com
# Should be readable by www-data user
```

## Port and Binding Issues

### "Address already in use"

```
nginx: [emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)
```

**Find what's using the port:**
```bash
sudo lsof -i :80
sudo netstat -tlnp | grep :80
sudo ss -tlnp | grep :80
```

**Stop conflicting service:**
```bash
sudo systemctl stop apache2
```

### Permission Denied

```
nginx: [emerg] bind() to 0.0.0.0:80 failed (13: Permission denied)
```

Port 80/443 require root privileges:

```bash
# Start nginx as root
sudo systemctl start nginx

# Or use non-privileged ports (>1024)
listen 8080;
```

## SSL/TLS Issues

### Certificate Not Found

```
nginx: [emerg] cannot load certificate "/etc/ssl/certs/example.com.crt"
```

**Verify certificate exists:**
```bash
sudo ls -la /etc/ssl/certs/example.com.crt
sudo ls -la /etc/ssl/private/example.com.key
```

**Check permissions:**
```bash
sudo chmod 644 /etc/ssl/certs/example.com.crt
sudo chmod 600 /etc/ssl/private/example.com.key
```

### SSL Handshake Failure

**Test SSL:**
```bash
openssl s_client -connect example.com:443 -servername example.com
```

**Check certificate chain:**
```bash
openssl s_client -connect example.com:443 -showcerts
```

## Performance Issues

### High Memory Usage

**Check worker configuration:**
```nginx
worker_processes auto;  # Don't set too high
worker_connections 4096;  # Adjust based on traffic
```

**Monitor processes:**
```bash
top
htop
ps aux | grep nginx
```

### High CPU Usage

**Check gzip compression level:**
```nginx
gzip_comp_level 6;  # Don't use 9, too CPU intensive
```

**Monitor with top:**
```bash
top -p $(pgrep -d, nginx)
```

## Connection Issues

### Connection Refused

Backend not accepting connections.

**Check backend is listening:**
```bash
netstat -tlnp | grep 3000
curl http://127.0.0.1:3000
```

### Connection Reset

**Enable keepalive:**
```nginx
upstream backend {
    server 127.0.0.1:3000;
    keepalive 32;
}

location / {
    proxy_http_version 1.1;
    proxy_set_header Connection "";
}
```

## Logging and Debugging

### Enable Debug Logging

```nginx
error_log /var/log/nginx/error.log debug;
```

**Warning:** Very verbose, use temporarily.

### View Logs

```bash
# Error log
sudo tail -f /var/log/nginx/error.log

# Access log
sudo tail -f /var/log/nginx/access.log

# Systemd logs
sudo journalctl -u nginx -f
```

### Custom Log Format

```nginx
log_format debug '$remote_addr - $remote_user [$time_local] "$request" '
                 '$status $body_bytes_sent "$http_referer" "$http_user_agent" '
                 'rt=$request_time uct="$upstream_connect_time" '
                 'uht="$upstream_header_time" urt="$upstream_response_time"';

access_log /var/log/nginx/debug.log debug;
```

## Service Management Issues

### nginx Not Starting

**Check configuration:**
```bash
sudo nginx -t
```

**Check service status:**
```bash
sudo systemctl status nginx
```

**View detailed errors:**
```bash
sudo journalctl -xeu nginx
```

### Can't Reload Configuration

**Force reload:**
```bash
sudo systemctl reload nginx

# If that fails, restart
sudo systemctl restart nginx
```

## Quick Diagnostics

```bash
# 1. Test configuration
sudo nginx -t

# 2. Check nginx is running
sudo systemctl status nginx

# 3. Check ports
sudo netstat -tlnp | grep nginx

# 4. Test locally
curl http://localhost

# 5. Check logs
sudo tail -20 /var/log/nginx/error.log

# 6. Check backend
curl http://127.0.0.1:3000

# 7. Verify DNS
dig example.com

# 8. Test SSL
openssl s_client -connect example.com:443
```
