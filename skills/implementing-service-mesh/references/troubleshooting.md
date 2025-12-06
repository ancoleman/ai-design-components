# Service Mesh Troubleshooting Guide

## Table of Contents

- [Common Issues and Solutions](#common-issues-and-solutions)
- [Debug Commands](#debug-commands)
- [Performance Tuning](#performance-tuning)
- [Monitoring and Alerts](#monitoring-and-alerts)
- [Recovery Procedures](#recovery-procedures)
- [Best Practices](#best-practices)

## Common Issues and Solutions

### mTLS Not Working

**Symptoms:**
- Services cannot communicate
- Connection refused errors
- "503 Service Unavailable" responses

**Diagnosis (Istio):**

```bash
# Check mTLS status
istioctl authn tls-check frontend.production.svc.cluster.local

# Check peer authentication policies
kubectl get peerauthentication -A

# Verify certificates
istioctl proxy-config secret deployment/frontend -n production

# Check proxy logs
kubectl logs -n production deployment/frontend -c istio-proxy
```

**Diagnosis (Linkerd):**

```bash
# Check mTLS edges
linkerd edges deployment/frontend -n production

# Verify identity
linkerd identity list -n production

# Check certificate expiry
linkerd identity show deployment/frontend -n production
```

**Solutions:**

```yaml
# Set PERMISSIVE mode temporarily
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: temp-permissive
  namespace: production
spec:
  mtls:
    mode: PERMISSIVE
```

```bash
# Restart pods to refresh certificates
kubectl rollout restart deployment/frontend -n production
```

### Traffic Not Routing Correctly

**Symptoms:**
- Traffic always goes to one version
- VirtualService rules not applied
- 404 errors on valid paths

**Diagnosis (Istio):**

```bash
# Analyze configuration
istioctl analyze -n production

# Check VirtualService
kubectl get virtualservice -n production
kubectl describe virtualservice backend-routing -n production

# Verify DestinationRule subsets
kubectl get destinationrule -n production
kubectl describe destinationrule backend -n production

# Check endpoints
istioctl proxy-config endpoints deployment/frontend -n production | grep backend
```

**Common Mistakes:**

```yaml
# WRONG: Missing subset definition
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: backend
spec:
  hosts:
  - backend
  http:
  - route:
    - destination:
        host: backend
        subset: v2  # Subset not defined in DestinationRule
```

**Solution:**

```yaml
# CORRECT: Define subset in DestinationRule
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
  name: backend
spec:
  hosts:
  - backend
  http:
  - route:
    - destination:
        host: backend
        subset: v2
```

### Authorization Policies Blocking Traffic

**Symptoms:**
- "RBAC: access denied" errors
- 403 Forbidden responses
- Previously working services now fail

**Diagnosis:**

```bash
# Check authorization policies
kubectl get authorizationpolicy -n production

# Describe specific policy
kubectl describe authorizationpolicy allow-frontend -n production

# Check proxy logs for denials
kubectl logs -n production deployment/backend -c istio-proxy | grep RBAC

# Test with policy temporarily disabled
kubectl delete authorizationpolicy deny-all -n production
```

**Debug with Audit Mode:**

```yaml
# Set to AUDIT instead of ENFORCE
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: test-policy
  namespace: production
spec:
  action: AUDIT  # Logs denials but allows traffic
  rules:
  - from:
    - source:
        principals:
        - cluster.local/ns/production/sa/frontend
```

**Common Issues:**

```yaml
# WRONG: Typo in principal
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
spec:
  rules:
  - from:
    - source:
        principals:
        - cluster.local/ns/production/sa/fronted  # Typo: "fronted" not "frontend"
```

### Gateway Not Accessible

**Symptoms:**
- Cannot access ingress gateway from outside
- LoadBalancer IP not assigned
- TLS certificate errors

**Diagnosis:**

```bash
# Check gateway configuration
kubectl get gateway -n production
kubectl describe gateway https-gateway -n production

# Check ingress gateway service
kubectl get svc -n istio-system istio-ingressgateway

# Check gateway pods
kubectl get pods -n istio-system -l app=istio-ingressgateway

# View logs
kubectl logs -n istio-system -l app=istio-ingressgateway
```

**Check TLS Configuration:**

```bash
# Verify secret exists
kubectl get secret -n istio-system api-cert

# Check certificate details
kubectl get secret -n istio-system api-cert -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -text -noout
```

**Common Issues:**

```yaml
# WRONG: Gateway and VirtualService in different namespaces without proper reference
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: https-gateway
  namespace: istio-system
---
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: api-routing
  namespace: production
spec:
  gateways:
  - https-gateway  # WRONG: Should be "istio-system/https-gateway"
```

**Solution:**

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: api-routing
  namespace: production
spec:
  gateways:
  - istio-system/https-gateway  # CORRECT: namespace/gateway
```

### High Latency or Timeouts

**Symptoms:**
- Requests timing out
- High P95/P99 latencies
- Intermittent failures

**Diagnosis:**

```bash
# Check proxy stats
istioctl proxy-config clusters deployment/frontend -n production

# View connection pool stats
istioctl proxy-config endpoints deployment/frontend -n production

# Check for circuit breaker tripping
kubectl logs -n production deployment/frontend -c istio-proxy | grep "overflow"
```

**Adjust Timeouts:**

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: backend
spec:
  hosts:
  - backend
  http:
  - route:
    - destination:
        host: backend
    timeout: 30s  # Increase from default 15s
```

**Adjust Circuit Breaker:**

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: backend
spec:
  host: backend
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 200  # Increase from 100
      http:
        http1MaxPendingRequests: 50  # Increase from 10
```

### Certificate Expiration Issues

**Symptoms:**
- "certificate has expired" errors
- mTLS failures after some time
- Unable to establish secure connections

**Diagnosis:**

```bash
# Check certificate expiry (Istio)
istioctl proxy-config secret deployment/frontend -n production -o json | \
  jq '.dynamicActiveSecrets[] | select(.name=="default") | .secret.tlsCertificate.certificateChain.inlineBytes' | \
  base64 -d | openssl x509 -text -noout | grep "Not After"

# Check Linkerd certificate expiry
linkerd identity check

# View certificate details
kubectl get secret istio-ca-secret -n istio-system -o yaml
```

**Solutions:**

```bash
# Restart pods to get new certificates
kubectl rollout restart deployment/frontend -n production

# Force certificate rotation (Istio)
kubectl delete secret istio-ca-secret -n istio-system
kubectl rollout restart deployment -n istio-system istiod
```

### Sidecar Injection Not Working

**Symptoms:**
- Pods don't have istio-proxy container
- Mesh features not working
- Service not showing in mesh

**Diagnosis:**

```bash
# Check namespace label
kubectl get namespace production --show-labels

# Check injection webhook
kubectl get mutatingwebhookconfigurations | grep istio

# Check pod for sidecar
kubectl get pod -n production <POD_NAME> -o jsonpath='{.spec.containers[*].name}'

# View injection status
kubectl get pod -n production <POD_NAME> -o jsonpath='{.metadata.annotations.sidecar\.istio\.io/status}'
```

**Solutions:**

```bash
# Label namespace for injection
kubectl label namespace production istio-injection=enabled

# Restart deployments
kubectl rollout restart deployment -n production

# For individual pod, add annotation
kubectl patch deployment frontend -n production -p '{"spec":{"template":{"metadata":{"annotations":{"sidecar.istio.io/inject":"true"}}}}}'
```

## Debug Commands

### Istio

**Configuration Analysis:**

```bash
# Analyze all namespaces
istioctl analyze -A

# Analyze specific namespace
istioctl analyze -n production

# Check installation
istioctl verify-install

# View mesh configuration
kubectl get configmap istio -n istio-system -o yaml
```

**Proxy Configuration:**

```bash
# View all proxy config
istioctl proxy-config all deployment/frontend -n production

# View listeners
istioctl proxy-config listeners deployment/frontend -n production

# View routes
istioctl proxy-config routes deployment/frontend -n production

# View clusters
istioctl proxy-config clusters deployment/frontend -n production

# View endpoints
istioctl proxy-config endpoints deployment/frontend -n production

# View secrets (certificates)
istioctl proxy-config secrets deployment/frontend -n production
```

**Logs:**

```bash
# View proxy logs
kubectl logs -n production deployment/frontend -c istio-proxy

# Follow logs
kubectl logs -n production deployment/frontend -c istio-proxy -f

# View control plane logs
kubectl logs -n istio-system deployment/istiod
```

**Traffic Debugging:**

```bash
# Enable debug logging
istioctl proxy-config log deployment/frontend -n production --level debug

# Disable debug logging
istioctl proxy-config log deployment/frontend -n production --level info
```

### Linkerd

**Health Checks:**

```bash
# Check overall health
linkerd check

# Check data plane
linkerd check --proxy

# Check multi-cluster
linkerd multicluster check
```

**Traffic Inspection:**

```bash
# Tap live traffic
linkerd tap deployment/frontend -n production

# Tap specific route
linkerd tap deployment/frontend -n production --path /api/users

# Tap with filtering
linkerd tap deployment/frontend -n production \
  --method GET \
  --authority backend.production.svc.cluster.local
```

**Statistics:**

```bash
# Service stats
linkerd stat deployment/frontend -n production

# Route stats
linkerd routes deployment/frontend -n production

# Edge stats (mTLS)
linkerd edges deployment/frontend -n production
```

**Dashboard:**

```bash
# Launch dashboard
linkerd dashboard

# Access specific namespace
linkerd viz dashboard -n production
```

### Cilium

**Status Checks:**

```bash
# Overall status
cilium status

# Connectivity test
cilium connectivity test

# Check specific endpoint
cilium endpoint list
cilium endpoint get <ENDPOINT_ID>
```

**Policy Debugging:**

```bash
# View policies
cilium policy get

# Validate policy
cilium policy validate <POLICY_FILE>

# Trace policy decision
cilium monitor --type policy-verdict
```

**Hubble Observability:**

```bash
# Observe all traffic
hubble observe

# Observe specific namespace
hubble observe --namespace production

# Observe dropped packets
hubble observe --verdict DROPPED

# Observe HTTP traffic
hubble observe --protocol http

# Observe specific pod
hubble observe --pod backend-7d8f9c5b4-xyz12
```

**Network Troubleshooting:**

```bash
# View BPF maps
cilium bpf endpoint list
cilium bpf ct list global
cilium bpf nat list

# Check service endpoints
cilium service list

# Monitor events
cilium monitor
```

## Performance Tuning

### Reduce Latency Overhead

**Use Ambient Mode (Istio):**

```bash
# Install ambient profile
istioctl install --set profile=ambient -y

# Add namespace to ambient
kubectl label namespace production istio.io/dataplane-mode=ambient
```

**Optimize Envoy:**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: istio
  namespace: istio-system
data:
  mesh: |
    defaultConfig:
      concurrency: 2
      drainDuration: 5s
      parentShutdownDuration: 10s
```

**Adjust Resource Limits:**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: istio-sidecar-injector
  namespace: istio-system
data:
  values: |
    sidecarInjectorWebhook:
      neverInjectSelector:
      - matchLabels:
          app: high-perf-service
```

### Reduce Resource Usage

**Limit Proxy CPU/Memory:**

```yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  values:
    global:
      proxy:
        resources:
          requests:
            cpu: 10m
            memory: 40Mi
          limits:
            cpu: 100m
            memory: 128Mi
```

**Use Sidecar Resource:**

```yaml
apiVersion: networking.istio.io/v1
kind: Sidecar
metadata:
  name: frontend-sidecar
  namespace: production
spec:
  workloadSelector:
    labels:
      app: frontend
  egress:
  - hosts:
    - "production/*"
    - "istio-system/*"
```

## Monitoring and Alerts

### Key Metrics to Monitor

**Control Plane:**
```promql
# Istiod memory usage
container_memory_working_set_bytes{pod=~"istiod.*"}

# Istiod CPU usage
rate(container_cpu_usage_seconds_total{pod=~"istiod.*"}[5m])

# Configuration push time
pilot_proxy_convergence_time_bucket
```

**Data Plane:**
```promql
# Envoy memory
envoy_server_memory_allocated

# Connection pool overflow
envoy_cluster_upstream_rq_pending_overflow

# Circuit breaker tripped
envoy_cluster_circuit_breakers_default_cx_open
```

**mTLS:**
```promql
# mTLS success rate
sum(rate(istio_requests_total{connection_security_policy="mutual_tls"}[5m]))
/ sum(rate(istio_requests_total[5m]))
```

### Alert Examples

```yaml
groups:
- name: implementing-service-mesh
  rules:
  - alert: IstiodDown
    expr: up{job="istiod"} == 0
    for: 1m
    annotations:
      summary: "Istio control plane down"

  - alert: HighProxyMemory
    expr: container_memory_working_set_bytes{container="istio-proxy"} > 500000000
    for: 5m
    annotations:
      summary: "Proxy using >500MB memory"

  - alert: mTLSDisabled
    expr: |
      sum(rate(istio_requests_total{connection_security_policy!="mutual_tls"}[5m]))
      / sum(rate(istio_requests_total[5m])) > 0.01
    for: 5m
    annotations:
      summary: "More than 1% traffic without mTLS"
```

## Recovery Procedures

### Rollback Istio Upgrade

```bash
# Revert to previous version
istioctl install --set revision=1-19-0

# Update workloads to use old revision
kubectl label namespace production istio.io/rev=1-19-0 --overwrite

# Restart workloads
kubectl rollout restart deployment -n production
```

### Emergency Mesh Disable

```bash
# Remove sidecar injection
kubectl label namespace production istio-injection-

# Restart pods
kubectl rollout restart deployment -n production
```

### Certificate Recovery

```bash
# Regenerate CA certificates
istioctl x ca create \
  --ca-name istio-ca \
  --ca-namespace istio-system \
  --overwrite

# Restart control plane
kubectl rollout restart deployment -n istio-system istiod

# Restart data plane
kubectl rollout restart deployment -n production
```

## Best Practices

**Debugging:**
- Enable debug logs temporarily only
- Use analyze before applying configs
- Check control plane health first
- Verify certificates regularly
- Monitor proxy resource usage

**Performance:**
- Use ambient mode for lower overhead
- Tune connection pools appropriately
- Set reasonable timeouts
- Monitor latency metrics
- Load test before production

**Operations:**
- Automate health checks
- Set up proper monitoring
- Document runbooks
- Test recovery procedures
- Keep mesh components updated
