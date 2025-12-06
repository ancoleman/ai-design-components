# HAProxy Load Balancing Patterns

Complete guide to HAProxy configuration for high-performance load balancing.


## Table of Contents

- [Basic HTTP Load Balancing](#basic-http-load-balancing)
- [Load Balancing Algorithms](#load-balancing-algorithms)
- [Health Checks](#health-checks)
  - [HTTP Health Check](#http-health-check)
  - [TCP Health Check](#tcp-health-check)
  - [Advanced Health Checks](#advanced-health-checks)
- [Sticky Sessions](#sticky-sessions)
  - [Cookie-Based](#cookie-based)
  - [Source IP](#source-ip)
  - [Application Cookie](#application-cookie)
- [SSL/TLS Termination](#ssltls-termination)
- [ACL-Based Routing](#acl-based-routing)
- [TCP Mode (Layer 4)](#tcp-mode-layer-4)
- [Advanced Features](#advanced-features)
  - [Rate Limiting](#rate-limiting)
  - [Connection Draining](#connection-draining)
  - [Statistics Dashboard](#statistics-dashboard)

## Basic HTTP Load Balancing

```haproxy
global
    log /dev/log local0
    maxconn 4096
    user haproxy
    group haproxy
    daemon

defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    option  http-server-close
    option  forwardfor except 127.0.0.0/8
    retries 3
    timeout connect 5000
    timeout client  50000
    timeout server  50000

frontend http_front
    bind *:80
    default_backend web_servers

backend web_servers
    balance roundrobin
    option httpchk GET /health
    server web1 192.168.1.101:8080 check
    server web2 192.168.1.102:8080 check
```

## Load Balancing Algorithms

HAProxy supports 10+ algorithms:

**Round Robin:**
```haproxy
backend web_servers
    balance roundrobin
    server web1 192.168.1.101:8080
    server web2 192.168.1.102:8080
```

**Least Connections:**
```haproxy
backend web_servers
    balance leastconn
    server web1 192.168.1.101:8080
    server web2 192.168.1.102:8080
```

**Source IP Hash:**
```haproxy
backend web_servers
    balance source
    hash-type consistent
    server web1 192.168.1.101:8080
    server web2 192.168.1.102:8080
```

**URI Hash:**
```haproxy
backend web_servers
    balance uri
    hash-type consistent
    server web1 192.168.1.101:8080
    server web2 192.168.1.102:8080
```

## Health Checks

### HTTP Health Check

```haproxy
backend web_servers
    option httpchk GET /health HTTP/1.1\r\nHost:\ example.com
    http-check expect status 200
    http-check expect rstring "healthy"

    server web1 192.168.1.101:8080 check inter 5s fall 3 rise 2
```

**Parameters:**
- `check`: Enable health checks
- `inter 5s`: Check every 5 seconds
- `fall 3`: Mark down after 3 failures
- `rise 2`: Mark up after 2 successes

### TCP Health Check

```haproxy
backend mysql_servers
    mode tcp
    option tcp-check
    tcp-check connect port 3306

    server mysql1 192.168.1.101:3306 check inter 5s
```

### Advanced Health Checks

**Redis:**
```haproxy
backend redis_servers
    mode tcp
    option tcp-check
    tcp-check send PING\r\n
    tcp-check expect string +PONG

    server redis1 192.168.1.101:6379 check
```

**MySQL:**
```haproxy
backend mysql_servers
    mode tcp
    option mysql-check user haproxy

    server mysql1 192.168.1.101:3306 check
```

## Sticky Sessions

### Cookie-Based

```haproxy
backend web_servers
    balance roundrobin
    cookie SERVERID insert indirect nocache
    server web1 192.168.1.101:8080 check cookie web1
    server web2 192.168.1.102:8080 check cookie web2
```

### Source IP

```haproxy
backend web_servers
    balance source
    hash-type consistent
    server web1 192.168.1.101:8080 check
    server web2 192.168.1.102:8080 check
```

### Application Cookie

```haproxy
backend web_servers
    stick-table type string len 32 size 100k expire 30m
    stick on cookie(JSESSIONID)

    server web1 192.168.1.101:8080 check
    server web2 192.168.1.102:8080 check
```

## SSL/TLS Termination

```haproxy
frontend https_front
    bind *:443 ssl crt /etc/haproxy/certs/example.com.pem
    redirect scheme https code 301 if !{ ssl_fc }
    default_backend web_servers

backend web_servers
    balance roundrobin
    server web1 192.168.1.101:8080 check
```

## ACL-Based Routing

```haproxy
frontend http_front
    bind *:80

    acl is_api path_beg /api
    acl is_static path_beg /static
    acl is_admin hdr(host) -i admin.example.com

    use_backend api_servers if is_api
    use_backend static_servers if is_static
    use_backend admin_servers if is_admin
    default_backend web_servers
```

## TCP Mode (Layer 4)

```haproxy
frontend mysql_front
    mode tcp
    bind *:3306
    default_backend mysql_servers

backend mysql_servers
    mode tcp
    balance leastconn
    option tcp-check

    server mysql1 192.168.1.101:3306 check
    server mysql2 192.168.1.102:3306 check
```

## Advanced Features

### Rate Limiting

```haproxy
frontend http_front
    stick-table type ip size 100k expire 30s store http_req_rate(10s)
    http-request track-sc0 src
    http-request deny if { sc_http_req_rate(0) gt 100 }
```

### Connection Draining

```haproxy
backend web_servers
    server web1 192.168.1.101:8080 check weight 100
    server web2 192.168.1.102:8080 check weight 100
    # To drain web1: set weight to 0, wait for connections to finish
```

### Statistics Dashboard

```haproxy
frontend stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 30s
    stats auth admin:password
```

Complete configuration examples available in `examples/haproxy/` directory.
