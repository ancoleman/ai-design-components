---
sidebar_position: 2
title: Kubernetes Operations
description: Master plan for operating production Kubernetes clusters with resource management, scheduling, networking, security, and autoscaling
tags: [master-plan, infrastructure, kubernetes, k8s, operations]
---

# Kubernetes Operations

:::info Status
**Master Plan** - Comprehensive init.md complete, ready for SKILL.md implementation
:::

Kubernetes has become the de facto standard for container orchestration. This skill covers operational patterns for managing production clusters, including resource optimization, advanced scheduling, networking, security hardening, and troubleshooting.

## Scope

This skill teaches:

- **Resource Management** - CPU/memory requests/limits, QoS classes, VPA for rightsizing
- **Advanced Scheduling** - Node affinity, taints/tolerations, topology spread constraints
- **Networking** - NetworkPolicies, Ingress controllers, Gateway API, service mesh patterns
- **Storage Operations** - StorageClasses, PV/PVC lifecycle, CSI drivers, volume snapshots
- **Security Hardening** - RBAC, Pod Security Standards, policy enforcement (Kyverno/OPA)
- **Autoscaling** - HPA, VPA, Cluster Autoscaler, KEDA (event-driven)
- **Troubleshooting** - Systematic debugging for common failure modes

## Key Components

### Resource Management
- **QoS Classes**: Guaranteed (requests = limits), Burstable (requests < limits), BestEffort (no limits)
- **Resource Quotas**: Namespace-level limits for multi-tenancy
- **LimitRanges**: Default container constraints
- **VPA**: Automated CPU/memory rightsizing (30-50% cost reduction)

### Scheduling Patterns
- **Node Affinity**: Required vs preferred node selection
- **Taints/Tolerations**: Reserve nodes for specific workloads
- **Topology Spread**: Even distribution across zones/nodes for HA
- **Pod Priority**: Critical workload prioritization

### Networking
- **NetworkPolicies**: Micro-segmentation (default-deny security)
- **Ingress**: Legacy L7 routing (Nginx, Traefik)
- **Gateway API**: Modern routing (GA in 1.29+)
- **Service Mesh**: mTLS, traffic management (Istio, Linkerd)

## Decision Framework

**Which Resource QoS Class?**

```
Critical production service?
  YES → Can tolerate ANY variability?
          YES → Burstable
          NO → Guaranteed
  NO → Batch/background job?
          YES → Burstable (low requests, high limits)
          NO → Dev/testing?
                  YES → BestEffort
                  NO → Burstable (default)
```

**HPA vs VPA vs Cluster Autoscaler?**

| Scenario | HPA | VPA | Cluster Autoscaler |
|----------|-----|-----|--------------------|
| Stateless web app with traffic spikes | ✅ | ❌ | Maybe (if nodes full) |
| Stateful database (single instance) | ❌ | ✅ | Maybe (if undersized) |
| Queue processor (event-driven) | ✅ KEDA | ❌ | Maybe |
| Pods pending (no resources) | ❌ | ❌ | ✅ |
| Requests too high/low | ❌ | ✅ | ❌ |

## Tool Recommendations

### Core: Kubernetes
- **Library**: `/websites/kubernetes_io`
- **Trust Score**: 93.7/100
- **Code Snippets**: 6,932+
- **Installation**: `kubectl` CLI (brew/apt/yum)

### Autoscaling: KEDA
- **Status**: CNCF Graduated Project
- **Event Sources**: 50+ (Kafka, RabbitMQ, AWS SQS, Prometheus, Cron)
- **Scale to Zero**: Cost savings for idle workloads

### Policy: Kyverno
- **Status**: CNCF Incubating
- **Advantages**: Native Kubernetes (YAML, not Rego), easier than OPA
- **Actions**: Validate, mutate, generate policies

### Monitoring: Metrics Server
- **Purpose**: HPA requirement, CPU/memory usage per pod
- **Trust Score**: 61.8/100

## Integration Points

**With Other Skills:**
- `building-ci-pipelines` - Deploy to Kubernetes from CI/CD
- `observability` - Monitor clusters (Prometheus, Grafana, tracing)
- `secret-management` - External Secrets Operator, Sealed Secrets
- `testing-strategies` - Kubeval, Conftest, Kind for testing
- `infrastructure-as-code` - Terraform provisions clusters

**Metrics to Monitor:**
- Node CPU/memory utilization
- Pod restart count
- HPA scaling events
- PVC storage usage
- NetworkPolicy denied connections

## Learn More

- [Full Master Plan (init.md)](https://github.com/ancoleman/ai-design-components/blob/main/skills/kubernetes-operations/init.md)
- Related: `infrastructure-as-code`, `observability`, `secret-management`
