---
sidebar_position: 1
title: Operating Kubernetes
description: Production Kubernetes operations with resource management, security, and autoscaling
tags: [infrastructure, kubernetes, containers, orchestration]
---

# Operating Kubernetes

Production-grade Kubernetes cluster operations covering resource management, advanced scheduling, networking, storage, security hardening, and autoscaling patterns.

## When to Use

Use when:
- Deploying workloads to Kubernetes clusters
- Configuring resource requests/limits and QoS classes
- Implementing NetworkPolicies for zero-trust security
- Setting up autoscaling (HPA, VPA, KEDA)
- Managing persistent storage with StorageClasses
- Troubleshooting pod issues (CrashLoopBackOff, Pending)
- Configuring RBAC with least privilege
- Spreading pods across availability zones

## Key Features

### Resource Management
- Quality of Service (QoS) classes: Guaranteed, Burstable, BestEffort
- Resource quotas and LimitRanges for multi-tenancy
- Vertical Pod Autoscaler for automated rightsizing
- Container resource requests and limits (CPU/memory)

### Advanced Scheduling
- Node affinity for targeted pod placement
- Taints and tolerations for workload isolation
- Topology spread constraints for high availability
- Pod priority and preemption

### Networking
- NetworkPolicies with default-deny security
- Ingress vs. Gateway API for traffic management
- Service mesh integration patterns
- DNS-based service discovery

### Storage Operations
- StorageClasses for performance tiers (SSD, HDD)
- PersistentVolumeClaims and access modes (RWO, ROX, RWX)
- CSI drivers for cloud-native storage
- Volume snapshots and backups

### Security
- RBAC (Role-Based Access Control)
- Pod Security Standards (Restricted, Baseline, Privileged)
- Policy enforcement with Kyverno/OPA Gatekeeper
- Secrets management integration

### Autoscaling
- Horizontal Pod Autoscaler (HPA) for replica scaling
- Vertical Pod Autoscaler (VPA) for resource optimization
- KEDA for event-driven autoscaling (queues, cron, metrics)
- Cluster autoscaler for node provisioning

## Quick Start

```yaml
# High-availability deployment with resource management
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
spec:
  replicas: 3
  template:
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchLabels:
                app: api-server
            topologyKey: topology.kubernetes.io/zone
      containers:
      - name: api
        image: api-server:v1.2.0
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8080
          initialDelaySeconds: 30
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8080
          initialDelaySeconds: 10
---
# Horizontal Pod Autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-server-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-server
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Troubleshooting Common Issues

**Pod Stuck in Pending:**
```bash
kubectl describe pod <pod-name>
# Check: Insufficient resources, node selector mismatch, PVC not bound, taint intolerance
```

**CrashLoopBackOff:**
```bash
kubectl logs <pod-name>
kubectl logs <pod-name> --previous
# Check: Application crash, missing env vars, liveness probe failing, OOMKilled
```

**Service Not Accessible:**
```bash
kubectl get endpoints <service-name>
# If empty: Service selector doesn't match pod labels, pods not ready, NetworkPolicies blocking
```

## Related Skills

- [Writing Infrastructure Code](./writing-infrastructure-code) - Provision EKS, GKE, AKS clusters via IaC
- [Implementing Service Mesh](./implementing-service-mesh) - Advanced traffic management with Istio/Linkerd
- [Disaster Recovery](./planning-disaster-recovery) - Kubernetes backup with Velero
- [Managing Configuration](./managing-configuration) - Ansible for K8s node configuration

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/operating-kubernetes)
- [Kubernetes Official Docs](https://kubernetes.io/docs/)
- Resource Management: `references/resource-management.md`
- Scheduling Patterns: `references/scheduling-patterns.md`
- Networking: `references/networking.md`
- Security: `references/security.md`
- Troubleshooting: `references/troubleshooting.md`
