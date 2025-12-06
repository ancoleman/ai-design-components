# Traefik Load Balancing Patterns

Cloud-native edge router with automatic service discovery.


## Table of Contents

- [Docker Provider](#docker-provider)
- [File Provider](#file-provider)
- [Kubernetes Ingress](#kubernetes-ingress)
- [Load Balancing Methods](#load-balancing-methods)
- [Middleware](#middleware)
  - [Rate Limiting](#rate-limiting)
  - [Circuit Breaker](#circuit-breaker)

## Docker Provider

```yaml
# docker-compose.yml
version: '3.8'

services:
  traefik:
    image: traefik:v3.0
    command:
      - --api.insecure=true
      - --providers.docker=true
      - --entrypoints.web.address=:80
      - --entrypoints.websecure.address=:443
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro

  app:
    image: myapp:latest
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.app.rule=Host(`app.example.com`)"
      - "traefik.http.services.app.loadbalancer.server.port=8080"
      - "traefik.http.services.app.loadbalancer.healthcheck.path=/health"
      - "traefik.http.services.app.loadbalancer.healthcheck.interval=10s"
    deploy:
      replicas: 3
```

## File Provider

```yaml
# traefik.yml
entryPoints:
  web:
    address: ":80"
  websecure:
    address: ":443"

providers:
  file:
    filename: /etc/traefik/dynamic.yml

# dynamic.yml
http:
  routers:
    app-router:
      rule: "Host(`app.example.com`)"
      service: app-service
      entryPoints:
        - websecure
      tls:
        certResolver: letsencrypt

  services:
    app-service:
      loadBalancer:
        servers:
          - url: "http://backend1:8080"
          - url: "http://backend2:8080"
        healthCheck:
          path: /health
          interval: 10s
          timeout: 3s
```

## Kubernetes Ingress

```yaml
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: app-route
spec:
  entryPoints:
    - websecure
  routes:
  - match: Host(`app.example.com`)
    kind: Rule
    services:
    - name: app-service
      port: 80
      sticky:
        cookie:
          name: app_session
          httpOnly: true
  tls:
    certResolver: letsencrypt
```

## Load Balancing Methods

**Weighted Round Robin:**
```yaml
services:
  app-service:
    loadBalancer:
      servers:
        - url: "http://backend1:8080"
        - url: "http://backend2:8080"
          weight: 2
```

**Sticky Sessions:**
```yaml
services:
  app-service:
    loadBalancer:
      sticky:
        cookie:
          name: app_session
          httpOnly: true
          secure: true
```

## Middleware

### Rate Limiting

```yaml
http:
  middlewares:
    api-ratelimit:
      rateLimit:
        average: 100
        burst: 50
        period: 1s

  routers:
    api-router:
      rule: "Host(`api.example.com`)"
      middlewares:
        - api-ratelimit
      service: api-service
```

### Circuit Breaker

```yaml
http:
  middlewares:
    api-circuit-breaker:
      circuitBreaker:
        expression: "NetworkErrorRatio() > 0.30"
```

Complete examples in `examples/traefik/` directory.
