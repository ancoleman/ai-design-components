# Kubernetes Ingress Controllers

Complete guide to Kubernetes ingress for HTTP load balancing.


## Table of Contents

- [NGINX Ingress Controller](#nginx-ingress-controller)
  - [Installation](#installation)
  - [Basic Ingress](#basic-ingress)
  - [Advanced Features](#advanced-features)
- [Traefik Ingress](#traefik-ingress)
  - [Installation](#installation)
  - [IngressRoute (CRD)](#ingressroute-crd)
- [HAProxy Ingress](#haproxy-ingress)
- [Gateway API (Next Generation)](#gateway-api-next-generation)
- [Health Checks](#health-checks)

## NGINX Ingress Controller

### Installation

```bash
helm repo add nginx-stable https://helm.nginx.com/stable
helm install nginx-ingress nginx-stable/nginx-ingress \
  --namespace ingress-nginx \
  --create-namespace
```

### Basic Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

### Advanced Features

**Sticky Sessions:**
```yaml
annotations:
  nginx.ingress.kubernetes.io/affinity: "cookie"
  nginx.ingress.kubernetes.io/session-cookie-name: "app_session"
```

**Rate Limiting:**
```yaml
annotations:
  nginx.ingress.kubernetes.io/limit-rps: "100"
```

## Traefik Ingress

### Installation

```bash
helm install traefik traefik/traefik \
  --namespace traefik \
  --create-namespace
```

### IngressRoute (CRD)

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
  tls:
    certResolver: letsencrypt
```

## HAProxy Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    haproxy.org/load-balance: "leastconn"
    haproxy.org/cookie-persistence: "app-cookie"
spec:
  ingressClassName: haproxy
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80
```

## Gateway API (Next Generation)

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: app-gateway
spec:
  gatewayClassName: envoy
  listeners:
  - name: https
    protocol: HTTPS
    port: 443
    tls:
      certificateRefs:
      - name: app-tls

---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: app-route
spec:
  parentRefs:
  - name: app-gateway
  hostnames:
  - "app.example.com"
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /api
    backendRefs:
    - name: api-service
      port: 80
```

## Health Checks

All ingress controllers rely on Kubernetes Service and Pod health:

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    livenessProbe:
      httpGet:
        path: /health/live
        port: 8080
      initialDelaySeconds: 30
      periodSeconds: 10

    readinessProbe:
      httpGet:
        path: /health/ready
        port: 8080
      initialDelaySeconds: 5
      periodSeconds: 5
```

Complete examples in `examples/kubernetes/` directory.
