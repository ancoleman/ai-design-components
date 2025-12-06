# Progressive Delivery Patterns

## Table of Contents

- [Canary Deployments](#canary-deployments)
- [Blue/Green Deployments](#bluegreen-deployments)
- [A/B Testing](#ab-testing)
- [Automated Rollback](#automated-rollback)
- [Flagger Integration](#flagger-integration)

## Canary Deployments

Gradually shift traffic to new version while monitoring metrics.

### Manual Canary (Istio)

**Stage 1: Deploy v2 with 0% Traffic**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-v2
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
      version: v2
  template:
    metadata:
      labels:
        app: backend
        version: v2
    spec:
      containers:
      - name: backend
        image: backend:v2
---
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: backend
spec:
  host: backend
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
---
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: backend-canary
spec:
  hosts:
  - backend
  http:
  - route:
    - destination:
        host: backend
        subset: v1
      weight: 100
    - destination:
        host: backend
        subset: v2
      weight: 0
```

**Stage 2: Route 10% to v2**

```bash
kubectl apply -f - <<EOF
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: backend-canary
  namespace: production
spec:
  hosts:
  - backend
  http:
  - route:
    - destination:
        host: backend
        subset: v1
      weight: 90
    - destination:
        host: backend
        subset: v2
      weight: 10
EOF
```

**Stage 3: Progressive Increase**

```bash
# Monitor metrics, then increase
# 10% → 25% → 50% → 75% → 100%

# 25%
kubectl patch vs backend-canary -n production --type merge -p '
{
  "spec": {
    "http": [{
      "route": [
        {"destination": {"host": "backend", "subset": "v1"}, "weight": 75},
        {"destination": {"host": "backend", "subset": "v2"}, "weight": 25}
      ]
    }]
  }
}'

# 50%
kubectl patch vs backend-canary -n production --type merge -p '
{
  "spec": {
    "http": [{
      "route": [
        {"destination": {"host": "backend", "subset": "v1"}, "weight": 50},
        {"destination": {"host": "backend", "subset": "v2"}, "weight": 50}
      ]
    }]
  }
}'

# 100%
kubectl patch vs backend-canary -n production --type merge -p '
{
  "spec": {
    "http": [{
      "route": [
        {"destination": {"host": "backend", "subset": "v2"}, "weight": 100}
      ]
    }]
  }
}'
```

**Stage 4: Cleanup**

```bash
# Delete v1 deployment
kubectl delete deployment backend-v1 -n production

# Update VirtualService to simple routing
kubectl apply -f - <<EOF
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: backend
  namespace: production
spec:
  hosts:
  - backend
  http:
  - route:
    - destination:
        host: backend
EOF
```

### Manual Canary (Linkerd)

**Traffic Split Configuration:**

```yaml
apiVersion: policy.linkerd.io/v1beta2
kind: HTTPRoute
metadata:
  name: backend-canary
  namespace: production
spec:
  parentRefs:
  - name: backend
    kind: Service
  rules:
  - backendRefs:
    - name: backend-v1
      port: 8080
      weight: 90
    - name: backend-v2
      port: 8080
      weight: 10
```

**Update Weights:**

```bash
# Increase to 25%
kubectl patch httproute backend-canary -n production --type merge -p '
{
  "spec": {
    "rules": [{
      "backendRefs": [
        {"name": "backend-v1", "port": 8080, "weight": 75},
        {"name": "backend-v2", "port": 8080, "weight": 25}
      ]
    }]
  }
}'
```

### Canary with Header-Based Routing

Test canary with internal users first.

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: backend-canary-staged
spec:
  hosts:
  - backend
  http:
  # Internal testers always see canary
  - match:
    - headers:
        x-canary-user:
          exact: "true"
    route:
    - destination:
        host: backend
        subset: v2
  # Production: gradual rollout
  - route:
    - destination:
        host: backend
        subset: v1
      weight: 90
    - destination:
        host: backend
        subset: v2
      weight: 10
```

### Monitoring During Canary

**Key Metrics to Watch:**

```promql
# Error rate comparison
sum(rate(http_requests_total{code=~"5..", version="v2"}[5m]))
/ sum(rate(http_requests_total{version="v2"}[5m]))

# Latency P95 comparison
histogram_quantile(0.95,
  sum(rate(http_request_duration_seconds_bucket{version="v2"}[5m])) by (le)
)

# Request rate
sum(rate(http_requests_total{version="v2"}[5m]))
```

**Alert on Issues:**

```yaml
# Prometheus alert
- alert: CanaryHighErrorRate
  expr: |
    sum(rate(http_requests_total{code=~"5..", version="v2"}[5m]))
    / sum(rate(http_requests_total{version="v2"}[5m])) > 0.01
  for: 5m
  annotations:
    summary: "Canary v2 error rate above 1%"
```

## Blue/Green Deployments

Instant traffic cutover between versions.

### Blue/Green (Linkerd)

**Stage 1: Deploy Green Alongside Blue**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
      version: blue
  template:
    metadata:
      labels:
        app: backend
        version: blue
    spec:
      containers:
      - name: backend
        image: backend:blue
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
      version: green
  template:
    metadata:
      labels:
        app: backend
        version: green
    spec:
      containers:
      - name: backend
        image: backend:green
---
apiVersion: v1
kind: Service
metadata:
  name: backend-blue
spec:
  selector:
    app: backend
    version: blue
  ports:
  - port: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: backend-green
spec:
  selector:
    app: backend
    version: green
  ports:
  - port: 8080
```

**Stage 2: Test Green with Subset**

```yaml
apiVersion: policy.linkerd.io/v1beta2
kind: HTTPRoute
metadata:
  name: backend-bluegreen-test
spec:
  parentRefs:
  - name: backend
  rules:
  # Test traffic: route to green
  - matches:
    - headers:
      - name: x-version
        value: green
    backendRefs:
    - name: backend-green
      port: 8080
  # Production traffic: route to blue
  - backendRefs:
    - name: backend-blue
      port: 8080
```

**Stage 3: Instant Cutover to Green**

```yaml
apiVersion: policy.linkerd.io/v1beta2
kind: HTTPRoute
metadata:
  name: backend-cutover
spec:
  parentRefs:
  - name: backend
  rules:
  - backendRefs:
    - name: backend-green
      port: 8080
```

**Stage 4: Rollback if Needed**

```bash
# Instant rollback to blue
kubectl apply -f - <<EOF
apiVersion: policy.linkerd.io/v1beta2
kind: HTTPRoute
metadata:
  name: backend-rollback
  namespace: production
spec:
  parentRefs:
  - name: backend
  rules:
  - backendRefs:
    - name: backend-blue
      port: 8080
EOF
```

### Blue/Green (Istio)

**Cutover Configuration:**

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: backend-bluegreen
spec:
  hosts:
  - backend
  http:
  - route:
    - destination:
        host: backend-green.production.svc.cluster.local
```

**Rollback:**

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: backend-rollback
spec:
  hosts:
  - backend
  http:
  - route:
    - destination:
        host: backend-blue.production.svc.cluster.local
```

## A/B Testing

Route traffic based on user segments.

### Cookie-Based A/B Test (Istio)

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: frontend-ab-test
spec:
  hosts:
  - frontend
  http:
  # Variant A: existing experience
  - match:
    - headers:
        cookie:
          regex: "^(.*?;)?(ab-test=a)(;.*)?$"
    route:
    - destination:
        host: frontend
        subset: variant-a
  # Variant B: new experience
  - match:
    - headers:
        cookie:
          regex: "^(.*?;)?(ab-test=b)(;.*)?$"
    route:
    - destination:
        host: frontend
        subset: variant-b
  # No cookie: 50/50 split
  - route:
    - destination:
        host: frontend
        subset: variant-a
      weight: 50
      headers:
        response:
          set:
            Set-Cookie: "ab-test=a; Max-Age=86400"
    - destination:
        host: frontend
        subset: variant-b
      weight: 50
      headers:
        response:
          set:
            Set-Cookie: "ab-test=b; Max-Age=86400"
```

### User-Agent Based Routing

Route mobile users differently.

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: mobile-routing
spec:
  hosts:
  - api
  http:
  - match:
    - headers:
        user-agent:
          regex: ".*(Mobile|Android|iPhone).*"
    route:
    - destination:
        host: api
        subset: mobile-optimized
  - route:
    - destination:
        host: api
        subset: desktop
```

### Geographic Routing

Route based on user location (requires geo headers).

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: geo-routing
spec:
  hosts:
  - api
  http:
  - match:
    - headers:
        x-user-region:
          exact: "us-east"
    route:
    - destination:
        host: api-us-east.production.svc.cluster.local
  - match:
    - headers:
        x-user-region:
          exact: "eu-west"
    route:
    - destination:
        host: api-eu-west.production.svc.cluster.local
```

## Automated Rollback

Automatically revert on metric failures.

### Prometheus-Based Alerts

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: canary-alerts
data:
  alerts.yaml: |
    groups:
    - name: canary
      interval: 30s
      rules:
      # High error rate
      - alert: CanaryHighErrors
        expr: |
          sum(rate(http_requests_total{code=~"5..", version="v2"}[5m]))
          / sum(rate(http_requests_total{version="v2"}[5m])) > 0.01
        for: 2m
        annotations:
          summary: "Canary error rate > 1%"

      # High latency
      - alert: CanaryHighLatency
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket{version="v2"}[5m])) by (le)
          ) > 0.5
        for: 2m
        annotations:
          summary: "Canary P95 latency > 500ms"
```

### Rollback Script

```bash
#!/bin/bash
# rollback-canary.sh

NAMESPACE="production"
SERVICE="backend"

echo "Rolling back canary deployment..."

kubectl apply -f - <<EOF
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: ${SERVICE}-canary
  namespace: ${NAMESPACE}
spec:
  hosts:
  - ${SERVICE}
  http:
  - route:
    - destination:
        host: ${SERVICE}
        subset: v1
      weight: 100
EOF

echo "Rollback complete. All traffic to v1."
```

## Flagger Integration

Automated progressive delivery with Flagger.

### Install Flagger

```bash
# Add Flagger Helm repository
helm repo add flagger https://flagger.app

# Install Flagger for Istio
helm install flagger flagger/flagger \
  --namespace istio-system \
  --set meshProvider=istio \
  --set metricsServer=http://prometheus:9090

# Install Flagger for Linkerd
helm install flagger flagger/flagger \
  --namespace linkerd \
  --set meshProvider=linkerd \
  --set metricsServer=http://prometheus:9090
```

### Canary with Flagger (Istio)

```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: backend
  namespace: production
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  service:
    port: 8080
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
    # Success rate must be > 99%
    - name: request-success-rate
      thresholdRange:
        min: 99
      interval: 1m
    # P95 latency must be < 500ms
    - name: request-duration
      thresholdRange:
        max: 500
      interval: 1m
  webhooks:
  # Pre-rollout checks
  - name: pre-rollout
    type: pre-rollout
    url: http://flagger-loadtester/
    timeout: 15s
    metadata:
      type: bash
      cmd: "curl -sd 'test' http://backend-canary:8080/healthz"
  # Load testing during rollout
  - name: load-test
    url: http://flagger-loadtester/
    timeout: 5s
    metadata:
      cmd: "hey -z 1m -q 10 -c 2 http://backend-canary.production:8080/"
```

### Canary with Flagger (Linkerd)

```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: backend
  namespace: production
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  service:
    port: 8080
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99
      interval: 1m
    - name: request-duration
      thresholdRange:
        max: 500
      interval: 1m
```

### A/B Testing with Flagger

```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: frontend-ab
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: frontend
  service:
    port: 80
  analysis:
    interval: 1m
    iterations: 10
    match:
    - headers:
        x-user-type:
          exact: "beta"
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99
```

### Blue/Green with Flagger

```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: backend-bluegreen
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  service:
    port: 8080
  analysis:
    interval: 1m
    threshold: 10
    iterations: 2
    maxWeight: 100
    stepWeight: 100
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99
```

### Monitor Flagger

```bash
# Watch canary progress
kubectl -n production get canaries --watch

# Describe canary status
kubectl -n production describe canary backend

# View Flagger events
kubectl -n production get events --sort-by='.lastTimestamp'
```

## Best Practices

**Canary Deployments:**
- Start with small traffic percentages (5-10%)
- Monitor key metrics: error rate, latency, throughput
- Increase traffic gradually (10% → 25% → 50% → 100%)
- Wait for stabilization between stages
- Set clear rollback criteria

**Blue/Green:**
- Test green environment thoroughly before cutover
- Use header-based routing for pre-production validation
- Keep blue environment running for quick rollback
- Monitor metrics after cutover
- Automate cutover and rollback procedures

**A/B Testing:**
- Use consistent user assignment (cookies, headers)
- Define success metrics before test
- Ensure statistical significance
- Isolate test variables
- Document test results

**Automated Rollback:**
- Define clear success criteria
- Use multiple metrics (error rate, latency, throughput)
- Set appropriate thresholds
- Implement alerts for failures
- Test rollback procedures regularly

**Flagger:**
- Use load testing webhooks for realistic traffic
- Set appropriate thresholds based on SLOs
- Monitor Flagger events for debugging
- Integrate with alerting systems
- Test analysis configuration in staging first
