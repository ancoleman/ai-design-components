# Kubernetes NetworkPolicies Guide

NetworkPolicies provide firewall-like controls for pod-to-pod communication in Kubernetes clusters.


## Table of Contents

- [Prerequisites](#prerequisites)
- [Key Concepts](#key-concepts)
  - [Pod Selectors](#pod-selectors)
  - [Namespace Selectors](#namespace-selectors)
  - [Policy Types](#policy-types)
  - [Default Behavior](#default-behavior)
- [Default Deny Pattern](#default-deny-pattern)
  - [Deny All Ingress](#deny-all-ingress)
  - [Deny All Egress](#deny-all-egress)
  - [Deny All (Ingress + Egress)](#deny-all-ingress-egress)
- [Common Patterns](#common-patterns)
  - [Allow DNS Queries](#allow-dns-queries)
  - [Frontend → Backend Communication](#frontend-backend-communication)
  - [Allow from Ingress Controller](#allow-from-ingress-controller)
  - [Allow External HTTPS (Egress)](#allow-external-https-egress)
  - [Cross-Namespace Communication](#cross-namespace-communication)
  - [Allow Monitoring (Prometheus)](#allow-monitoring-prometheus)
- [IP Block Rules](#ip-block-rules)
  - [Allow Specific External IPs](#allow-specific-external-ips)
  - [Block Internal IPs (Egress)](#block-internal-ips-egress)
- [Multi-Tier Application Example](#multi-tier-application-example)
- [Testing NetworkPolicies](#testing-networkpolicies)
  - [Check Applied Policies](#check-applied-policies)
  - [Test Connectivity](#test-connectivity)
  - [Debug Denied Traffic](#debug-denied-traffic)
- [Calico-Specific Features](#calico-specific-features)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Monitoring Tools](#monitoring-tools)
- [Migration Strategy](#migration-strategy)
- [Resources](#resources)

## Prerequisites

**CNI Plugin Support Required:**
- ✅ Calico
- ✅ Cilium
- ✅ Weave Net
- ❌ Flannel (no NetworkPolicy support)
- ❌ Default Kubernetes networking

Check CNI plugin:
```bash
kubectl get pods -n kube-system | grep -E 'calico|cilium|weave|flannel'
```

## Key Concepts

### Pod Selectors

```yaml
# Select pods by label
podSelector:
  matchLabels:
    app: backend

# Select all pods
podSelector: {}

# Advanced selection
podSelector:
  matchExpressions:
    - key: app
      operator: In
      values: [backend, frontend]
```

### Namespace Selectors

```yaml
# Select namespace by label
namespaceSelector:
  matchLabels:
    name: production

# All namespaces
namespaceSelector: {}
```

### Policy Types

- `Ingress` - Controls incoming traffic to pods
- `Egress` - Controls outgoing traffic from pods

### Default Behavior

**Without NetworkPolicies:**
- All pods can communicate with all pods
- All pods can reach external networks

**With NetworkPolicies:**
- If ANY NetworkPolicy selects a pod, that pod is "isolated"
- Only explicitly allowed traffic is permitted
- Default deny for non-matched traffic

## Default Deny Pattern

### Deny All Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: production
spec:
  podSelector: {}  # All pods in namespace
  policyTypes:
    - Ingress
```

### Deny All Egress

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-egress
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Egress
```

### Deny All (Ingress + Egress)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
```

## Common Patterns

### Allow DNS Queries

**Essential after default-deny-egress:**

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Egress
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
        - protocol: TCP
          port: 53
```

### Frontend → Backend Communication

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend  # Target pods
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend  # Source pods
      ports:
        - protocol: TCP
          port: 8080
```

### Allow from Ingress Controller

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-ingress-controller
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: frontend
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
      ports:
        - protocol: TCP
          port: 80
```

### Allow External HTTPS (Egress)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-external-https
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Egress
  egress:
    - to:
        - namespaceSelector: {}  # Any namespace
      ports:
        - protocol: TCP
          port: 443
    # For stricter control, use ipBlock:
    # - to:
    #     - ipBlock:
    #         cidr: 0.0.0.0/0
    #         except:
    #           - 10.0.0.0/8  # Block internal IPs
```

### Cross-Namespace Communication

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-from-another-namespace
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: staging
          podSelector:
            matchLabels:
              app: client
      ports:
        - protocol: TCP
          port: 8080
```

### Allow Monitoring (Prometheus)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-prometheus-scraping
  namespace: production
spec:
  podSelector: {}  # All pods
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: monitoring
          podSelector:
            matchLabels:
              app: prometheus
      ports:
        - protocol: TCP
          port: 9090  # Metrics port
```

## IP Block Rules

### Allow Specific External IPs

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-external-api
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Egress
  egress:
    - to:
        - ipBlock:
            cidr: 52.1.2.0/24  # AWS API endpoint
        - ipBlock:
            cidr: 140.82.112.0/20  # GitHub API
      ports:
        - protocol: TCP
          port: 443
```

### Block Internal IPs (Egress)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: block-internal-egress
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: untrusted
  policyTypes:
    - Egress
  egress:
    - to:
        - ipBlock:
            cidr: 0.0.0.0/0
            except:
              - 10.0.0.0/8      # Private IP ranges
              - 172.16.0.0/12
              - 192.168.0.0/16
      ports:
        - protocol: TCP
          port: 443
```

## Multi-Tier Application Example

```yaml
---
# Default deny all
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: app
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress

---
# Allow DNS
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns
  namespace: app
spec:
  podSelector: {}
  policyTypes:
    - Egress
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
      ports:
        - protocol: UDP
          port: 53

---
# Ingress → Frontend
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ingress-to-frontend
  namespace: app
spec:
  podSelector:
    matchLabels:
      tier: frontend
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
      ports:
        - protocol: TCP
          port: 80

---
# Frontend → Backend
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: frontend-to-backend
  namespace: app
spec:
  podSelector:
    matchLabels:
      tier: backend
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              tier: frontend
      ports:
        - protocol: TCP
          port: 8080

---
# Backend → Database
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-to-database
  namespace: app
spec:
  podSelector:
    matchLabels:
      tier: database
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              tier: backend
      ports:
        - protocol: TCP
          port: 5432

---
# Backend → External APIs
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-external-https
  namespace: app
spec:
  podSelector:
    matchLabels:
      tier: backend
  policyTypes:
    - Egress
  egress:
    - to:
        - namespaceSelector: {}
      ports:
        - protocol: TCP
          port: 443
```

## Testing NetworkPolicies

### Check Applied Policies

```bash
# List all NetworkPolicies in namespace
kubectl get networkpolicies -n production

# Describe specific policy
kubectl describe networkpolicy allow-frontend-to-backend -n production

# View YAML
kubectl get networkpolicy allow-frontend-to-backend -n production -o yaml
```

### Test Connectivity

```bash
# Create test pod
kubectl run test-pod --image=nicolaka/netshoot -n production -- sleep 3600

# Test connection from test pod
kubectl exec -it test-pod -n production -- curl http://backend-service:8080

# Test DNS resolution
kubectl exec -it test-pod -n production -- nslookup backend-service

# Clean up
kubectl delete pod test-pod -n production
```

### Debug Denied Traffic

```bash
# Check pod logs for connection errors
kubectl logs <pod-name> -n production

# Describe pod (check Events section)
kubectl describe pod <pod-name> -n production

# Temporarily remove NetworkPolicies to test
kubectl delete networkpolicy <policy-name> -n production
# Test connectivity
# Re-apply policy
kubectl apply -f <policy-file>.yaml
```

## Calico-Specific Features

Calico extends NetworkPolicies with GlobalNetworkPolicy:

```yaml
apiVersion: projectcalico.org/v3
kind: GlobalNetworkPolicy
metadata:
  name: deny-all-external-egress
spec:
  selector: all()
  types:
    - Egress
  egress:
    - action: Deny
      destination:
        notNets:
          - 10.0.0.0/8      # Allow internal
          - 172.16.0.0/12
          - 192.168.0.0/16
```

## Best Practices

1. **Start with Default Deny** - Namespace-wide default deny, then allow explicitly
2. **Allow DNS First** - Essential for name resolution
3. **Label Consistently** - Use consistent labels (app, tier, component)
4. **Test Before Production** - Apply to staging namespace first
5. **Document Policies** - Use descriptive names and comments
6. **Least Privilege** - Only allow necessary ports and sources
7. **Monitor Denied Traffic** - Use Calico/Cilium monitoring tools
8. **Version Control** - Store policies in Git
9. **Namespace Isolation** - Label namespaces for cross-namespace policies
10. **Regular Audits** - Review policies quarterly

## Troubleshooting

**Pods can't communicate after applying policy:**
- Check if policy selects correct pods: `kubectl describe networkpolicy`
- Verify CNI plugin supports NetworkPolicies
- Ensure DNS is allowed (egress to kube-system)
- Test with policy temporarily deleted

**DNS resolution fails:**
- Apply allow-dns policy (egress to kube-dns/CoreDNS)
- Check kube-dns/CoreDNS pod labels match selector

**NetworkPolicies not working at all:**
- CNI plugin may not support NetworkPolicies (check if using Flannel)
- Install Calico, Cilium, or Weave Net

**Too restrictive, can't debug:**
- Create temporary allow-all policy for debugging
- Remove after identifying issue

## Monitoring Tools

**Calico:**
```bash
# View denied traffic
calicoctl get globalnetworkpolicy -o yaml

# Flow logs
kubectl logs -n kube-system <calico-node-pod>
```

**Cilium:**
```bash
# Hubble (Cilium observability)
hubble observe --namespace production

# Network policy editor
cilium-hubble ui
```

## Migration Strategy

1. **Audit Current Traffic** - Use monitoring to understand actual traffic patterns
2. **Label Pods** - Ensure all pods have consistent labels
3. **Test in Staging** - Apply policies to non-production namespace
4. **Apply Default Deny** - Start with deny-all
5. **Allow Incrementally** - Add allow rules based on audit data
6. **Monitor Errors** - Watch for connection failures
7. **Iterate** - Adjust policies based on application needs

## Resources

- Kubernetes Docs: https://kubernetes.io/docs/concepts/services-networking/network-policies/
- Calico Docs: https://docs.projectcalico.org/security/kubernetes-network-policy
- Cilium Docs: https://docs.cilium.io/en/stable/policy/
- Network Policy Recipes: https://github.com/ahmetb/kubernetes-network-policy-recipes
