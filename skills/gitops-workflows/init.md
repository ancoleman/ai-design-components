# GitOps Workflows Skill - Master Plan

**Skill Name:** `gitops-workflows`
**Skill Level:** Mid Level (5,000-8,000 tokens, 500-800 lines init.md)
**Status:** Planning Phase (init.md complete, SKILL.md to be created)
**Last Updated:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [GitOps Tool Taxonomy](#gitops-tool-taxonomy)
5. [Decision Frameworks](#decision-frameworks)
6. [Implementation Patterns](#implementation-patterns)
7. [Library Recommendations](#library-recommendations)
8. [Skill Structure Design](#skill-structure-design)
9. [Integration Points](#integration-points)
10. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why GitOps Matters in 2025

GitOps has evolved from an emerging pattern to the **de facto standard** for Kubernetes continuous delivery. In 2025, over 90% of Kubernetes deployments are predicted to use GitOps practices, making this a foundational skill for modern cloud-native development.

**Market Drivers:**
- **Declarative Infrastructure:** Git as single source of truth for entire system state
- **Automated Reconciliation:** Continuous drift detection and auto-healing
- **Audit Trail:** Every change tracked via Git commits for compliance
- **Multi-Cluster Management:** Single control plane for hundreds of clusters
- **Developer Experience:** Pull-based deployment reduces CI/CD complexity

**Strategic Value:**
1. **Security:** Pull-based model eliminates CI credentials to production
2. **Reliability:** Automated reconciliation ensures desired state maintained
3. **Velocity:** Faster deployments through automation and self-healing
4. **Compliance:** Complete audit trail and policy enforcement
5. **Scale:** Manage edge, air-gapped, and unreliable network environments

### How This Differs from Traditional CD

**Traditional CI/CD (Push Model):**
- CI pipeline pushes changes to clusters
- Credentials stored in CI system (security risk)
- Manual drift detection
- Limited multi-cluster support

**GitOps (Pull Model):**
- Operators pull changes from Git
- No cluster credentials in CI
- Continuous drift detection
- Native multi-cluster support

---

## Skill Purpose and Scope

### What This Skill Teaches

**Core Competencies:**

1. **GitOps Fundamentals**
   - Git as single source of truth
   - Declarative configuration
   - Automated delivery and reconciliation
   - Pull-based vs push-based models

2. **ArgoCD Mastery**
   - Installation and configuration
   - Application and ApplicationSet patterns
   - Sync strategies and hooks
   - Progressive delivery with Argo Rollouts
   - Multi-cluster management
   - UI and CLI operations

3. **Flux CD Mastery**
   - Installation and bootstrap
   - GitRepository and OCIRepository sources
   - Kustomization and HelmRelease controllers
   - Multi-tenancy patterns
   - Notifications and webhooks

4. **Operational Patterns**
   - Environment promotion (dev → staging → prod)
   - Secret management integration (SOPS, ESO)
   - Drift detection and remediation
   - Rollback strategies
   - Disaster recovery

### What This Skill Does NOT Cover

- **Kubernetes basics** (use `kubernetes-operations` skill)
- **Infrastructure provisioning** (use `infrastructure-as-code` skill)
- **CI pipeline construction** (use `building-ci-pipelines` skill)
- **Container registry management** (use `deploying-applications` skill)
- **Observability setup** (covered in other skills)

---

## Research Findings

### Google Search Grounding Results (December 2025)

**Query 1: "GitOps best practices 2025 ArgoCD Flux comparison"**

**Key Findings:**
- **Git as Single Source of Truth:** All configuration in Git, no manual changes
- **Declarative Everything:** YAML/HCL for desired state, not imperative scripts
- **Automated Delivery:** Git commits trigger automatic deployments
- **Continuous Reconciliation:** Tools watch Git and reconcile live state
- **Security Best Practices:** Signed commits, RBAC, policy enforcement
- **Trunk-Based Development:** Simplified branching for GitOps repos

**ArgoCD vs Flux - Key Differences:**

| Aspect | ArgoCD | Flux |
|--------|--------|------|
| **Architecture** | Monolithic, stateful | Modular, stateless |
| **UI** | Built-in web UI | CLI-first (integrate dashboards) |
| **State Management** | Internal state store | Kubernetes CRDs only |
| **Multi-Tenancy** | Built-in RBAC & projects | Kubernetes RBAC + namespaces |
| **Learning Curve** | Easier (visual management) | Steeper (controller concepts) |
| **Best For** | Teams wanting UI, easier onboarding | API-driven, platform engineering |

**When to Choose:**
- **ArgoCD:** Transitioning to GitOps, need UI, centralized management
- **Flux:** Building platforms, resource-constrained, advanced workflows
- **Both:** Some teams use Flux for infra + ArgoCD for apps

---

**Query 2: "GitOps Kubernetes continuous delivery patterns 2025"**

**Key Findings:**
- **90%+ Adoption:** GitOps predicted for vast majority of K8s deployments
- **Kubernetes as Control Plane:** Managing VMs, serverless, AI pipelines, edge
- **AI/ML Integration:** Intelligent deployment optimization and anomaly detection
- **DevSecOps Integration:** Security scanning and policy enforcement in Git
- **Edge/IoT Growth:** GitOps for distributed, unreliable network environments
- **Hybrid/Multi-Cloud:** Unified management across cloud providers

**Emerging Patterns:**
- **Progressive Delivery:** Canary, blue-green with automated rollback
- **Policy as Code:** OPA, Kyverno for compliance enforcement
- **Modular Components:** Helm charts, Kustomize overlays for reusability
- **Immutable Deployments:** Never modify running resources, always replace

---

**Query 3: "ArgoCD vs Flux 2025 features comparison"**

**ArgoCD 2025 Updates:**
- **ArgoCD v3:** Refined security, optimized performance
- **OCI Support:** Native support for OCI registries as artifact sources
- **CLI Plugins:** Custom commands integrated with ArgoCD CLI
- **UI Enhancements:** Direct scaling of Deployments/StatefulSets in UI
- **ApplicationSets:** Sophisticated multi-cluster app generation

**Flux 2025 Updates:**
- **GA APIs:** Image automation, OCI artifacts, events to general availability
- **UX Improvements:** Custom health checks, CEL support, OAuth integration
- **GitOps Toolkit:** Extensible, composable controllers
- **Flagger Integration:** Progressive delivery (canary, blue-green)

---

### Context7 Library Research

**ArgoCD (Official):**
- **Library ID:** `/argoproj/argo-cd`
- **Trust Score:** 9.18/10 (High)
- **Code Snippets:** 1,237+
- **Benchmark Score:** 91.8

**Flux CD (Official):**
- **Library ID:** `/websites/fluxcd_io_flux`
- **Trust Score:** High
- **Code Snippets:** 1,605+
- **Benchmark Score:** 80.8

**Kustomize (Kubernetes SIG):**
- **Library ID:** `/kubernetes-sigs/kustomize`
- **Trust Score:** High
- **Code Snippets:** 1,038+
- **Benchmark Score:** 90.7

All three tools have **excellent documentation coverage** and are **production-ready** for enterprise use.

---

## GitOps Tool Taxonomy

### Tier 1: ArgoCD (UI-First, Stateful)

**Use When:**
- Team prefers visual management
- Transitioning to GitOps (easier onboarding)
- Multi-cluster deployments with centralized UI
- Built-in RBAC and multi-tenancy needed
- Self-healing and health checks critical

**Architecture:**
- Monolithic controller with internal state
- API server, web UI, repo server, application controller
- Maintains application state independently

**ArgoCD Installation:**
```yaml
# Install ArgoCD in argocd namespace
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Access UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Get admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

**Basic Application:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/myapp.git
    targetRevision: HEAD
    path: k8s/base
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

**ApplicationSet (Multi-Environment):**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: myapp-envs
  namespace: argocd
spec:
  goTemplate: true
  generators:
  - list:
      elements:
      - env: dev
        cluster: https://kubernetes.default.svc
        replicas: 1
      - env: staging
        cluster: https://kubernetes.default.svc
        replicas: 2
      - env: prod
        cluster: https://prod-cluster.example.com
        replicas: 5
  template:
    metadata:
      name: 'myapp-{{.env}}'
      labels:
        environment: '{{.env}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/myorg/myapp.git
        targetRevision: HEAD
        path: 'k8s/overlays/{{.env}}'
      destination:
        server: '{{.cluster}}'
        namespace: 'myapp-{{.env}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

**Progressive Rollout with RollingSync:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: progressive-rollout
  namespace: argocd
spec:
  generators:
  - list:
      elements:
      - cluster: dev
        url: https://dev-cluster.example.com
        env: development
      - cluster: staging
        url: https://staging-cluster.example.com
        env: staging
      - cluster: prod
        url: https://prod-cluster.example.com
        env: production
  strategy:
    type: RollingSync
    rollingSync:
      steps:
      - matchExpressions:
        - key: envLabel
          operator: In
          values:
          - development
        # maxUpdate: 100% (default, all at once)
      - matchExpressions:
        - key: envLabel
          operator: In
          values:
          - staging
        maxUpdate: 1  # One application at a time
      - matchExpressions:
        - key: envLabel
          operator: In
          values:
          - production
        maxUpdate: 10%  # 10% at a time
  template:
    metadata:
      name: '{{.cluster}}-myapp'
      labels:
        envLabel: '{{.env}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/myorg/myapp.git
        targetRevision: HEAD
        path: 'k8s/{{.cluster}}'
      destination:
        server: '{{.url}}'
        namespace: myapp
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

**Sync Hooks for Pre/Post Operations:**
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    spec:
      containers:
      - name: migrate
        image: myapp:latest
        command: ["/migrate.sh"]
      restartPolicy: Never
```

---

### Tier 2: Flux CD (CLI-First, Stateless)

**Use When:**
- Building internal platforms
- Resource-constrained environments
- API-driven operations preferred
- Advanced multi-source syncs needed
- Modular, flexible workflows required

**Architecture:**
- Modular controllers (source, kustomize, helm, notification, image)
- Stateless (all state in Kubernetes CRDs)
- GitOps Toolkit for extensibility

**Flux Installation (Bootstrap):**
```bash
# Install Flux CLI
curl -s https://fluxcd.io/install.sh | sudo bash

# Bootstrap Flux to cluster
flux bootstrap github \
  --owner=myorg \
  --repository=fleet-infra \
  --branch=main \
  --path=clusters/production \
  --personal

# This commits Flux manifests to your repo and installs Flux
```

**GitRepository Source:**
```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/myorg/myapp
  ref:
    branch: main
  secretRef:
    name: git-credentials
```

**Kustomization Controller:**
```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 10m
  retryInterval: 2m
  path: "./k8s/base"
  prune: true
  wait: true
  timeout: 5m
  sourceRef:
    kind: GitRepository
    name: myapp
  healthChecks:
  - apiVersion: apps/v1
    kind: Deployment
    name: myapp
    namespace: myapp
```

**HelmRelease Controller:**
```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: HelmRepository
metadata:
  name: podinfo
  namespace: flux-system
spec:
  interval: 1h
  url: https://stefanprodan.github.io/podinfo
---
apiVersion: helm.toolkit.fluxcd.io/v2
kind: HelmRelease
metadata:
  name: podinfo
  namespace: flux-system
spec:
  interval: 10m
  chart:
    spec:
      chart: podinfo
      version: ">=6.0.0 <7.0.0"
      sourceRef:
        kind: HelmRepository
        name: podinfo
  values:
    replicaCount: 2
    resources:
      limits:
        memory: 256Mi
      requests:
        cpu: 100m
        memory: 64Mi
```

**Multi-Environment with Kustomize Overlays:**
```yaml
# Base kustomization
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: myapp-base
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: myapp
  path: "./k8s/base"
  prune: false  # Don't prune base
---
# Dev overlay
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: myapp-dev
  namespace: flux-system
spec:
  interval: 5m
  dependsOn:
  - name: myapp-base
  sourceRef:
    kind: GitRepository
    name: myapp
  path: "./k8s/overlays/dev"
  prune: true
  targetNamespace: myapp-dev
  patches:
  - patch: |-
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: myapp
      spec:
        replicas: 1
    target:
      kind: Deployment
      name: myapp
---
# Prod overlay
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: myapp-prod
  namespace: flux-system
spec:
  interval: 10m
  dependsOn:
  - name: myapp-base
  sourceRef:
    kind: GitRepository
    name: myapp
  path: "./k8s/overlays/prod"
  prune: true
  targetNamespace: myapp-prod
  patches:
  - patch: |-
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: myapp
      spec:
        replicas: 5
    target:
      kind: Deployment
      name: myapp
```

**OCI Repository (Container Registry):**
```yaml
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: OCIRepository
metadata:
  name: myapp-config
  namespace: flux-system
spec:
  interval: 5m
  url: oci://ghcr.io/myorg/myapp-config
  ref:
    tag: latest
---
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: myapp-from-oci
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: OCIRepository
    name: myapp-config
  path: ./
  prune: true
```

---

### Tier 3: Kustomize (Configuration Management)

**Use When:**
- Template-free Kubernetes configuration
- Base + overlay pattern for environments
- No Helm required (pure YAML)
- Works with both ArgoCD and Flux

**Basic Kustomization:**
```yaml
# k8s/base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml
- service.yaml
- configmap.yaml

commonLabels:
  app: myapp
  managed-by: kustomize

namePrefix: myapp-
namespace: default
```

**Development Overlay:**
```yaml
# k8s/overlays/dev/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- ../../base

namePrefix: dev-
namespace: myapp-dev

replicas:
- name: myapp-deployment
  count: 1

images:
- name: myapp
  newTag: dev-latest

patches:
- patch: |-
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: myapp-config
    data:
      LOG_LEVEL: debug
      ENVIRONMENT: development
```

**Production Overlay:**
```yaml
# k8s/overlays/prod/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- ../../base

namePrefix: prod-
namespace: myapp-prod

replicas:
- name: myapp-deployment
  count: 5

images:
- name: myapp
  newTag: v1.2.3

patches:
- patch: |-
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: myapp-config
    data:
      LOG_LEVEL: info
      ENVIRONMENT: production
- patch: |-
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: myapp-deployment
    spec:
      template:
        spec:
          containers:
          - name: myapp
            resources:
              limits:
                memory: "512Mi"
                cpu: "1000m"
              requests:
                memory: "256Mi"
                cpu: "500m"
```

**Kustomize Components (Reusable Fragments):**
```yaml
# components/monitoring/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1alpha1
kind: Component

resources:
- servicemonitor.yaml

labels:
- pairs:
    monitoring: enabled

patches:
- patch: |-
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: not-important
    spec:
      template:
        metadata:
          annotations:
            prometheus.io/scrape: "true"
            prometheus.io/port: "8080"
  target:
    kind: Deployment

---
# Using component in overlay
# k8s/overlays/prod/kustomization.yaml
resources:
- ../../base

components:
- ../../components/monitoring
- ../../components/security

replicas:
- name: myapp-deployment
  count: 5
```

---

## Decision Frameworks

### Framework 1: ArgoCD vs Flux

```
START: Choosing GitOps Tool
  │
  ├─► Team Preference?
  │     ├─ Visual Management Preferred ──► ARGOCD
  │     └─ CLI/API Preferred ──► FLUX
  │
  ├─► Environment Constraints?
  │     ├─ Resource-Constrained (Edge/IoT) ──► FLUX
  │     └─ Standard Kubernetes ──► Either
  │
  ├─► Multi-Tenancy Needs?
  │     ├─ Built-in RBAC & Projects ──► ARGOCD
  │     └─ Kubernetes-Native RBAC ──► FLUX
  │
  ├─► Ecosystem Integration?
  │     ├─ Argo Workflows/Events ──► ARGOCD
  │     └─ Flagger, Kyverno, etc ──► FLUX
  │
  └─► Use Both?
        ├─ Flux for Infrastructure ──► Multi-Tool
        └─ ArgoCD for Applications ──► Strategy
```

### Framework 2: Deployment Strategy Selection

| Strategy | Use Case | Complexity | Risk |
|----------|----------|------------|------|
| **Direct Sync** | Dev/Staging, low-traffic | Low | Medium |
| **Blue-Green** | Zero-downtime, instant rollback | Medium | Low |
| **Canary** | Gradual rollout, metric-based | High | Low |
| **Rolling Update** | Standard, progressive | Medium | Medium |

**ArgoCD Strategies:**
- Built-in: AllAtOnce, RollingSync
- Argo Rollouts: Canary, Blue-Green with analysis

**Flux Strategies:**
- Flagger integration: Canary, Blue-Green, A/B testing
- Progressive delivery with automated rollback

### Framework 3: Repository Structure

**Monorepo (Single Git Repo):**
```
fleet-infra/
├── clusters/
│   ├── dev/
│   ├── staging/
│   └── prod/
├── apps/
│   ├── base/
│   └── overlays/
└── infrastructure/
    ├── ingress/
    ├── monitoring/
    └── storage/
```

**Pros:** Simplified management, atomic changes
**Cons:** Complex RBAC, potential blast radius

---

**Multi-Repo (App-Per-Repo):**
```
app1-config/
├── k8s/
│   ├── base/
│   └── overlays/

app2-config/
├── k8s/
│   ├── base/
│   └── overlays/

cluster-config/
├── clusters/
└── infrastructure/
```

**Pros:** Isolated changes, granular RBAC
**Cons:** Coordination overhead, dependency management

---

**Recommendation:**
- **Small Teams:** Monorepo (easier coordination)
- **Large Teams:** Multi-repo (isolation, ownership)
- **Hybrid:** Infrastructure in monorepo, apps in separate repos

### Framework 4: Secret Management Integration

| Method | Tool | Security | Complexity |
|--------|------|----------|------------|
| **Sealed Secrets** | Bitnami | Medium | Low |
| **SOPS** | Mozilla | High | Medium |
| **External Secrets** | ESO | High | Medium |
| **Vault** | HashiCorp | Very High | High |

**GitOps Integration:**
```yaml
# Sealed Secret (encrypted in Git)
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: mysecret
spec:
  encryptedData:
    password: AgBy3i4OJSWK+PiTySY...

---
# External Secret (reference to vault)
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: mysecret
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: mysecret
  data:
  - secretKey: password
    remoteRef:
      key: secret/data/myapp
      property: password
```

---

## Implementation Patterns

### Pattern 1: Environment Promotion Pipeline

**Git Branch Strategy:**
```
main (prod)
├── staging (auto-sync from main)
└── dev (auto-sync from staging)
```

**ArgoCD Implementation:**
```yaml
# Dev auto-syncs from dev branch
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-dev
spec:
  source:
    repoURL: https://github.com/myorg/myapp
    targetRevision: dev
    path: k8s/overlays/dev
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
---
# Staging syncs from staging branch (manual promotion)
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-staging
spec:
  source:
    repoURL: https://github.com/myorg/myapp
    targetRevision: staging
    path: k8s/overlays/staging
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
---
# Prod syncs from main (manual promotion + approval)
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-prod
spec:
  source:
    repoURL: https://github.com/myorg/myapp
    targetRevision: main
    path: k8s/overlays/prod
  syncPolicy:
    syncOptions:
    - CreateNamespace=true
  # No automated sync for production
```

**Promotion Process:**
1. Deploy to dev (automatic)
2. Test in dev environment
3. Merge dev → staging (triggers staging deployment)
4. Test in staging
5. Create PR: staging → main
6. Review + approve
7. Merge → triggers prod deployment

---

### Pattern 2: Multi-Cluster Management

**ArgoCD Cluster Registration:**
```bash
# Add external cluster
argocd cluster add prod-cluster \
  --kubeconfig=~/.kube/prod-config \
  --name=prod-cluster

# List clusters
argocd cluster list
```

**ApplicationSet for Multi-Cluster:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: multi-cluster-app
spec:
  generators:
  - clusters:
      selector:
        matchLabels:
          environment: production
  template:
    metadata:
      name: 'myapp-{{name}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/myorg/myapp
        targetRevision: HEAD
        path: k8s/base
      destination:
        server: '{{server}}'
        namespace: myapp
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

**Flux Multi-Cluster:**
```yaml
# Cluster 1: Dev cluster (in-cluster)
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: myapp-dev
  namespace: flux-system
spec:
  interval: 5m
  sourceRef:
    kind: GitRepository
    name: myapp
  path: ./k8s/overlays/dev
  targetNamespace: myapp
---
# Cluster 2: Prod cluster (remote via kubeconfig)
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: myapp-prod
  namespace: flux-system
spec:
  interval: 10m
  kubeConfig:
    secretRef:
      name: prod-kubeconfig
  sourceRef:
    kind: GitRepository
    name: myapp
  path: ./k8s/overlays/prod
  targetNamespace: myapp
```

---

### Pattern 3: Progressive Delivery with Argo Rollouts

**Canary Deployment:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: myapp
spec:
  replicas: 5
  strategy:
    canary:
      steps:
      - setWeight: 20
      - pause: {duration: 1m}
      - setWeight: 40
      - pause: {duration: 1m}
      - setWeight: 60
      - pause: {duration: 1m}
      - setWeight: 80
      - pause: {duration: 1m}
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:v2
        ports:
        - containerPort: 8080
```

**Canary with Analysis:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: myapp
spec:
  replicas: 5
  strategy:
    canary:
      steps:
      - setWeight: 20
      - pause: {duration: 30s}
      - analysis:
          templates:
          - templateName: success-rate
          args:
          - name: service-name
            value: myapp-canary
      - setWeight: 50
      - pause: {duration: 30s}
      - analysis:
          templates:
          - templateName: success-rate
          - templateName: latency
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:v2
---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  args:
  - name: service-name
  metrics:
  - name: success-rate
    interval: 5m
    successCondition: result[0] >= 0.95
    provider:
      prometheus:
        address: http://prometheus.monitoring:9090
        query: |
          sum(rate(
            http_requests_total{service="{{args.service-name}}",status=~"2.."}[5m]
          )) /
          sum(rate(
            http_requests_total{service="{{args.service-name}}"}[5m]
          ))
```

---

### Pattern 4: Drift Detection and Remediation

**ArgoCD Drift Detection:**
```bash
# Check sync status
argocd app get myapp

# See diff between Git and cluster
argocd app diff myapp

# Sync manually (override self-heal)
argocd app sync myapp

# Hard refresh (compare against latest Git)
argocd app get myapp --hard-refresh
```

**Flux Drift Detection:**
```bash
# Check kustomization status
flux get kustomizations

# Reconcile immediately
flux reconcile kustomization myapp --with-source

# Suspend automatic reconciliation
flux suspend kustomization myapp

# Resume
flux resume kustomization myapp
```

**Automated Remediation:**
```yaml
# ArgoCD: selfHeal enabled
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
spec:
  syncPolicy:
    automated:
      prune: true
      selfHeal: true  # Auto-revert manual changes
---
# Flux: automatic reconciliation (default)
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: myapp
spec:
  interval: 10m  # Check every 10 minutes
  prune: true    # Remove resources not in Git
  force: true    # Force apply on conflicts
```

---

### Pattern 5: Disaster Recovery

**Backup Strategy:**
1. **Git is Source of Truth:** All config in Git (versioned, recoverable)
2. **Cluster State:** ArgoCD/Flux manifests backed up
3. **Secrets:** Encrypted in Git (SOPS) or external vault

**Recovery Process:**

**ArgoCD Recovery:**
```bash
# 1. Reinstall ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# 2. Re-register clusters
argocd cluster add prod-cluster --kubeconfig=/path/to/kubeconfig

# 3. Restore applications from Git
kubectl apply -f git-repo/argocd/applications/

# 4. Sync all applications
argocd app sync --all
```

**Flux Recovery:**
```bash
# 1. Bootstrap Flux (idempotent)
flux bootstrap github \
  --owner=myorg \
  --repository=fleet-infra \
  --branch=main \
  --path=clusters/production

# Flux automatically reconciles all resources from Git
# No manual sync needed - pull model handles recovery
```

---

## Library Recommendations

### Primary Tools (2025)

**1. ArgoCD** (UI-First GitOps)
- **Library ID:** `/argoproj/argo-cd`
- **Version:** v2.9+ (v3 in development)
- **Trust Score:** 9.18/10
- **Code Snippets:** 1,237+
- **Best For:** Teams wanting visual management, easier onboarding

**Installation:**
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

**When to Use:**
- Transitioning to GitOps (UI reduces learning curve)
- Multi-cluster management with centralized control
- Built-in RBAC and multi-tenancy needed
- Team prefers visual application management

---

**2. Flux CD** (CLI-First GitOps)
- **Library ID:** `/websites/fluxcd_io_flux` and `/fluxcd/flux2`
- **Version:** v2.2+
- **Trust Score:** High
- **Code Snippets:** 1,605+
- **Best For:** Platform engineering, API-driven operations

**Installation:**
```bash
curl -s https://fluxcd.io/install.sh | sudo bash
flux bootstrap github \
  --owner=myorg \
  --repository=fleet-infra \
  --branch=main \
  --path=clusters/production
```

**When to Use:**
- Building internal developer platforms
- Resource-constrained environments (edge, IoT)
- Advanced multi-source synchronization
- Prefer modular, composable architecture

---

**3. Kustomize** (Configuration Management)
- **Library ID:** `/kubernetes-sigs/kustomize`
- **Version:** v5.0+
- **Trust Score:** High
- **Code Snippets:** 1,038+
- **Best For:** Template-free Kubernetes configuration

**Installation:**
```bash
# Built into kubectl
kubectl kustomize k8s/overlays/dev

# Standalone
curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash
```

**When to Use:**
- Template-free configuration (no Helm complexity)
- Base + overlay pattern for environments
- Works with both ArgoCD and Flux
- Team prefers pure YAML

---

### Supporting Tools

**4. Argo Rollouts** (Progressive Delivery)
- **Version:** v1.6+
- **Use:** Canary, blue-green deployments
- **Integration:** Works with ArgoCD and Flux

```bash
kubectl create namespace argo-rollouts
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml
```

**5. Flagger** (Progressive Delivery for Flux)
- **Version:** v1.34+
- **Use:** Automated canary releases with metrics
- **Integration:** Native Flux integration

```bash
flux install
kubectl apply -k github.com/fluxcd/flagger//kustomize/linkerd
```

**6. Sealed Secrets** (Secret Encryption)
- **Version:** v0.24+
- **Use:** Encrypt secrets for Git storage
- **Integration:** Works with both ArgoCD and Flux

```bash
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/controller.yaml
```

**7. External Secrets Operator** (Secret Management)
- **Version:** v0.9+
- **Use:** Sync secrets from external vaults
- **Integration:** Vault, AWS Secrets Manager, GCP Secret Manager

```bash
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets external-secrets/external-secrets -n external-secrets-system
```

---

### Tool Comparison Matrix

| Feature | ArgoCD | Flux | Kustomize |
|---------|--------|------|-----------|
| **UI** | ✅ Built-in | ❌ CLI only | ❌ CLI only |
| **Multi-Cluster** | ✅ Excellent | ✅ Good | N/A |
| **Learning Curve** | ⭐⭐⭐ Easy | ⭐⭐⭐⭐ Medium | ⭐⭐ Easy |
| **State Management** | Stateful | Stateless | N/A |
| **RBAC** | Built-in | K8s RBAC | N/A |
| **Helm Support** | ✅ Native | ✅ Native | ❌ External |
| **OCI Support** | ✅ v2.9+ | ✅ Native | ❌ No |
| **Webhooks** | ✅ Yes | ✅ Yes | N/A |
| **Progressive Delivery** | Argo Rollouts | Flagger | N/A |

---

## Skill Structure Design

```
gitops-workflows/
├── SKILL.md                          # Main skill (500-600 lines)
├── references/
│   ├── argocd-patterns.md            # ArgoCD implementation patterns
│   ├── flux-patterns.md              # Flux implementation patterns
│   ├── kustomize-overlays.md         # Kustomize configuration management
│   ├── progressive-delivery.md       # Canary, blue-green strategies
│   ├── multi-cluster.md              # Multi-cluster management
│   ├── secret-management.md          # SOPS, ESO integration
│   └── drift-remediation.md          # Drift detection and recovery
├── examples/
│   ├── argocd/
│   │   ├── application.yaml          # Basic Application
│   │   ├── applicationset.yaml       # Multi-environment ApplicationSet
│   │   ├── progressive-rollout.yaml  # RollingSync strategy
│   │   └── sync-hooks.yaml           # Pre/Post sync hooks
│   ├── flux/
│   │   ├── gitrepository.yaml        # Git source
│   │   ├── kustomization.yaml        # Kustomization controller
│   │   ├── helmrelease.yaml          # Helm release
│   │   └── ocirepository.yaml        # OCI artifact source
│   ├── kustomize/
│   │   ├── base/
│   │   │   └── kustomization.yaml
│   │   └── overlays/
│   │       ├── dev/
│   │       ├── staging/
│   │       └── prod/
│   └── rollouts/
│       ├── canary.yaml               # Canary deployment
│       └── blue-green.yaml           # Blue-green deployment
└── scripts/
    ├── install-argocd.sh             # ArgoCD installation
    ├── install-flux.sh               # Flux bootstrap
    ├── check-drift.sh                # Drift detection script
    └── promote-env.sh                # Environment promotion helper
```

---

## Integration Points

### With Existing Skills

| Skill | Integration |
|-------|-------------|
| `infrastructure-as-code` | IaC provisions clusters, GitOps deploys apps |
| `kubernetes-operations` | K8s fundamentals, GitOps automates deployments |
| `building-ci-pipelines` | CI builds images, GitOps deploys to clusters |
| `secret-management` | Vault/ESO + GitOps for secure secret delivery |
| `deploying-applications` | GitOps is the deployment mechanism |

### Skill Chaining Example

```
infrastructure-as-code → gitops-workflows → deploying-applications
        │                        │                       │
        ▼                        ▼                       ▼
  Provision cluster     Bootstrap ArgoCD/Flux    Deploy workloads
  with Terraform        Configure GitRepo         Monitor health
```

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- [ ] Core GitOps principles and decision frameworks
- [ ] ArgoCD installation and basic Application patterns
- [ ] Flux installation and basic Kustomization patterns
- [ ] Kustomize base + overlay examples

### Phase 2: Advanced Patterns (Week 3-4)
- [ ] ApplicationSets for multi-environment deployment
- [ ] Progressive rollout strategies (RollingSync)
- [ ] Flux HelmRelease and multi-source patterns
- [ ] Secret management integration (SOPS, ESO)

### Phase 3: Operational Excellence (Week 5-6)
- [ ] Multi-cluster management patterns
- [ ] Progressive delivery (Argo Rollouts, Flagger)
- [ ] Drift detection and remediation strategies
- [ ] Disaster recovery procedures

### Phase 4: Integration (Week 7)
- [ ] CI/CD pipeline integration
- [ ] Monitoring and observability
- [ ] Testing and validation
- [ ] Documentation polish

---

## Key Takeaways

1. **GitOps is Standard:** Over 90% of K8s deployments use GitOps in 2025
2. **Choose Your Tool:** ArgoCD for UI, Flux for CLI/API, or both
3. **Git is Truth:** All configuration in Git, no manual changes
4. **Automate Everything:** Self-healing, drift detection, progressive delivery
5. **Multi-Cluster Ready:** Manage hundreds of clusters from single control plane
6. **Security First:** Pull-based model, encrypted secrets, policy enforcement
7. **Composability:** Kustomize overlays + Helm charts for flexibility
8. **Progressive Delivery:** Canary and blue-green with automated rollback

---

**Progressive disclosure:** This init.md provides the master plan. Detailed implementation guidance in `references/`, working examples in `examples/`, and automation scripts in `scripts/`.
