# Multi-Cluster Service Mesh

## Table of Contents

- [Istio Multi-Cluster](#istio-multi-cluster)
- [Linkerd Multi-Cluster](#linkerd-multi-cluster)
- [Cilium Cluster Mesh](#cilium-cluster-mesh)
- [Traffic Patterns](#traffic-patterns)
- [Failover and HA](#failover-and-ha)

## Istio Multi-Cluster

Connect multiple Kubernetes clusters in a single mesh.

### Architecture Models

**Primary-Remote (Single Control Plane):**
- One cluster hosts Istiod
- Remote clusters use primary's control plane
- Best for: Small deployments, cost optimization

**Multi-Primary (Multiple Control Planes):**
- Each cluster has its own Istiod
- Meshes communicate peer-to-peer
- Best for: High availability, isolation

### Single Network Multi-Primary

Clusters share same network (pod IPs routable).

**Install on Cluster 1:**

```bash
# Set context
export CTX_CLUSTER1=cluster1
export CTX_CLUSTER2=cluster2

# Configure mesh ID and network
cat <<EOF > cluster1.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  values:
    global:
      meshID: mesh1
      multiCluster:
        clusterName: cluster1
      network: network1
EOF

# Install
istioctl install --context="${CTX_CLUSTER1}" -f cluster1.yaml
```

**Install on Cluster 2:**

```bash
cat <<EOF > cluster2.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  values:
    global:
      meshID: mesh1
      multiCluster:
        clusterName: cluster2
      network: network1
EOF

istioctl install --context="${CTX_CLUSTER2}" -f cluster2.yaml
```

**Enable Cross-Cluster Service Discovery:**

```bash
# Create remote secret for cluster2 on cluster1
istioctl x create-remote-secret \
  --context="${CTX_CLUSTER2}" \
  --name=cluster2 | \
  kubectl apply -f - --context="${CTX_CLUSTER1}"

# Create remote secret for cluster1 on cluster2
istioctl x create-remote-secret \
  --context="${CTX_CLUSTER1}" \
  --name=cluster1 | \
  kubectl apply -f - --context="${CTX_CLUSTER2}"
```

### Multi-Network Multi-Primary

Clusters on different networks (requires gateways).

**Install with East-West Gateway:**

```bash
# Cluster 1
cat <<EOF > cluster1-multinetwork.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  values:
    global:
      meshID: mesh1
      multiCluster:
        clusterName: cluster1
      network: network1
EOF

istioctl install --context="${CTX_CLUSTER1}" -f cluster1-multinetwork.yaml

# Install east-west gateway
samples/multicluster/gen-eastwest-gateway.sh \
  --mesh mesh1 --cluster cluster1 --network network1 | \
  istioctl --context="${CTX_CLUSTER1}" install -y -f -

# Expose services via east-west gateway
kubectl --context="${CTX_CLUSTER1}" apply -n istio-system -f \
  samples/multicluster/expose-services.yaml
```

**Cluster 2 (Same Process):**

```bash
# Install Istio
cat <<EOF > cluster2-multinetwork.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  values:
    global:
      meshID: mesh1
      multiCluster:
        clusterName: cluster2
      network: network2
EOF

istioctl install --context="${CTX_CLUSTER2}" -f cluster2-multinetwork.yaml

# Install east-west gateway
samples/multicluster/gen-eastwest-gateway.sh \
  --mesh mesh1 --cluster cluster2 --network network2 | \
  istioctl --context="${CTX_CLUSTER2}" install -y -f -

# Expose services
kubectl --context="${CTX_CLUSTER2}" apply -n istio-system -f \
  samples/multicluster/expose-services.yaml
```

**Exchange Secrets:**

```bash
# Cluster2 secret on cluster1
istioctl x create-remote-secret \
  --context="${CTX_CLUSTER2}" \
  --name=cluster2 | \
  kubectl apply -f - --context="${CTX_CLUSTER1}"

# Cluster1 secret on cluster2
istioctl x create-remote-secret \
  --context="${CTX_CLUSTER1}" \
  --name=cluster1 | \
  kubectl apply -f - --context="${CTX_CLUSTER2}"
```

### Primary-Remote Setup

Remote cluster uses primary's control plane.

**Primary Cluster:**

```bash
cat <<EOF > cluster1-primary.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  values:
    global:
      meshID: mesh1
      multiCluster:
        clusterName: cluster1
      network: network1
EOF

istioctl install --context="${CTX_CLUSTER1}" -f cluster1-primary.yaml
```

**Remote Cluster:**

```bash
# Generate remote configuration
istioctl x create-remote-secret \
  --context="${CTX_CLUSTER2}" \
  --name=cluster2 | \
  kubectl apply -f - --context="${CTX_CLUSTER1}"

# Install remote components
cat <<EOF > cluster2-remote.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  profile: remote
  values:
    global:
      meshID: mesh1
      multiCluster:
        clusterName: cluster2
      network: network2
      remotePilotAddress: <CLUSTER1_INGRESS_GATEWAY_IP>
EOF

istioctl install --context="${CTX_CLUSTER2}" -f cluster2-remote.yaml
```

### Verify Multi-Cluster

```bash
# Check remote secrets
kubectl get secrets -n istio-system | grep istio-remote-secret

# Verify endpoints
istioctl proxy-config endpoints <POD_NAME> -n production | grep cluster

# Test cross-cluster connectivity
kubectl exec -n production <POD> -- curl http://service.namespace.svc.cluster.local
```

## Linkerd Multi-Cluster

Link multiple Linkerd clusters.

### Setup Linkerd Multi-Cluster

**Cluster 1:**

```bash
# Install Linkerd
linkerd install --cluster-domain cluster1.local | \
  kubectl --context=cluster1 apply -f -

# Install multicluster components
linkerd multicluster install --cluster-domain cluster1.local | \
  kubectl --context=cluster1 apply -f -

# Check installation
linkerd --context=cluster1 check
linkerd --context=cluster1 multicluster check
```

**Cluster 2:**

```bash
# Install Linkerd
linkerd install --cluster-domain cluster2.local | \
  kubectl --context=cluster2 apply -f -

# Install multicluster components
linkerd multicluster install --cluster-domain cluster2.local | \
  kubectl --context=cluster2 apply -f -

# Check
linkerd --context=cluster2 check
linkerd --context=cluster2 multicluster check
```

### Link Clusters

**From Cluster 1 to Cluster 2:**

```bash
# Generate link
linkerd --context=cluster2 multicluster link --cluster-name cluster2 | \
  kubectl --context=cluster1 apply -f -

# Verify link
linkerd --context=cluster1 multicluster check

# View linked clusters
linkerd --context=cluster1 multicluster gateways
```

**From Cluster 2 to Cluster 1:**

```bash
linkerd --context=cluster1 multicluster link --cluster-name cluster1 | \
  kubectl --context=cluster2 apply -f -
```

### Export Services

**Export Service from Cluster 2:**

```bash
# Label service for export
kubectl --context=cluster2 label svc/backend \
  -n production \
  mirror.linkerd.io/exported=true

# Service automatically appears in cluster1 as:
# backend-cluster2.production.svc.cluster1.local
```

**Verify Mirrored Service:**

```bash
# Check mirrored service in cluster1
kubectl --context=cluster1 get svc -n production | grep cluster2

# Test connectivity
kubectl --context=cluster1 exec -n production <POD> -- \
  curl http://backend-cluster2.production:8080
```

### Unlink Clusters

```bash
# Remove link
linkerd --context=cluster1 multicluster unlink --cluster-name cluster2 | \
  kubectl delete -f -
```

## Cilium Cluster Mesh

Connect Cilium clusters at network layer.

### Enable Cluster Mesh

**Cluster 1:**

```bash
# Install Cilium with unique cluster ID
helm install cilium cilium/cilium \
  --namespace kube-system \
  --set cluster.name=cluster1 \
  --set cluster.id=1 \
  --set ipam.mode=kubernetes

# Enable cluster mesh
cilium clustermesh enable --context cluster1
```

**Cluster 2:**

```bash
helm install cilium cilium/cilium \
  --namespace kube-system \
  --set cluster.name=cluster2 \
  --set cluster.id=2 \
  --set ipam.mode=kubernetes

cilium clustermesh enable --context cluster2
```

### Connect Clusters

```bash
# Connect cluster1 to cluster2
cilium clustermesh connect \
  --context cluster1 \
  --destination-context cluster2

# Verify connection
cilium clustermesh status --context cluster1
```

### Global Services

**Create Global Service:**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend
  namespace: production
  annotations:
    io.cilium/global-service: "true"
spec:
  type: ClusterIP
  ports:
  - port: 8080
  selector:
    app: backend
```

**Verify Global Service:**

```bash
# Check service endpoints across clusters
cilium service list | grep backend
```

### Cross-Cluster Policy

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: cross-cluster-policy
  namespace: production
spec:
  endpointSelector:
    matchLabels:
      app: backend
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: frontend
        io.cilium.k8s.policy.cluster: cluster1
    - matchLabels:
        app: frontend
        io.cilium.k8s.policy.cluster: cluster2
```

## Traffic Patterns

### Locality-Based Routing (Istio)

Prefer local cluster, failover to remote.

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: backend-locality
spec:
  host: backend.production.svc.cluster.local
  trafficPolicy:
    loadBalancer:
      localityLbSetting:
        enabled: true
        distribute:
        - from: us-east/us-east-1/*
          to:
            "us-east/us-east-1/*": 80
            "us-west/us-west-1/*": 20
    outlierDetection:
      consecutiveErrors: 5
      interval: 30s
      baseEjectionTime: 30s
```

### Cross-Cluster Load Balancing (Linkerd)

**80/20 split between clusters:**

```yaml
apiVersion: policy.linkerd.io/v1beta2
kind: HTTPRoute
metadata:
  name: backend-multi-cluster
  namespace: production
spec:
  parentRefs:
  - name: backend
  rules:
  - backendRefs:
    - name: backend          # Local cluster
      port: 8080
      weight: 80
    - name: backend-cluster2 # Remote cluster
      port: 8080
      weight: 20
```

### Active-Active Deployment

Deploy to both clusters, equal traffic.

```yaml
# Istio
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: backend-active-active
spec:
  hosts:
  - backend
  http:
  - route:
    - destination:
        host: backend.production.svc.cluster.local
      weight: 50
    - destination:
        host: backend.production.svc.cluster2.global
      weight: 50
```

## Failover and HA

### Automatic Failover (Istio)

Outlier detection for automatic failover.

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: backend-failover
spec:
  host: backend
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 10
    outlierDetection:
      consecutiveErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
      minHealthPercent: 20
    loadBalancer:
      localityLbSetting:
        enabled: true
        failover:
        - from: us-east
          to: us-west
```

### Health-Based Routing

Route based on endpoint health.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend
  annotations:
    service.alpha.kubernetes.io/tolerate-unready-endpoints: "false"
spec:
  selector:
    app: backend
  ports:
  - port: 8080
---
apiVersion: v1
kind: Pod
metadata:
  name: backend
spec:
  containers:
  - name: backend
    livenessProbe:
      httpGet:
        path: /healthz
        port: 8080
      initialDelaySeconds: 3
      periodSeconds: 3
    readinessProbe:
      httpGet:
        path: /ready
        port: 8080
      initialDelaySeconds: 3
      periodSeconds: 3
```

### Circuit Breaking for Remote Clusters

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: remote-circuit-breaker
spec:
  host: backend.production.svc.cluster2.global
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 50
      http:
        http1MaxPendingRequests: 5
        http2MaxRequests: 50
    outlierDetection:
      consecutiveErrors: 3
      interval: 10s
      baseEjectionTime: 30s
      maxEjectionPercent: 100
```

### Disaster Recovery

**Cross-Region Failover:**

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: dr-failover
spec:
  host: backend
  trafficPolicy:
    loadBalancer:
      localityLbSetting:
        enabled: true
        failover:
        - from: us-east
          to: eu-west
        - from: eu-west
          to: us-east
    outlierDetection:
      consecutiveErrors: 5
      interval: 30s
```

## Best Practices

**Architecture:**
- Use multi-primary for production (HA)
- Use primary-remote for cost optimization
- Ensure network connectivity between clusters
- Use unique cluster IDs and names

**Service Discovery:**
- Test cross-cluster DNS resolution
- Monitor remote secret sync
- Use explicit service FQDNs when needed
- Document service naming conventions

**Security:**
- Enable mTLS across clusters
- Use same root CA for trust
- Rotate remote secrets regularly
- Monitor cross-cluster auth failures

**Performance:**
- Prefer local endpoints (locality-based routing)
- Set connection limits for remote calls
- Use circuit breakers for failover
- Monitor cross-cluster latency

**Resilience:**
- Configure outlier detection
- Set appropriate failover priorities
- Test failover scenarios regularly
- Monitor endpoint health

**Operations:**
- Automate cluster linking
- Monitor multi-cluster metrics
- Set up cross-cluster alerts
- Document runbooks for failures
