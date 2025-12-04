---
sidebar_position: 2
---

# GitOps Workflows

Master plan for implementing GitOps patterns using declarative infrastructure and automated synchronization. This skill covers GitOps principles, tooling selection, repository structures, and operational patterns for managing applications and infrastructure through Git.

**Status**: 🟢 Master Plan Available

## Key Topics

- **GitOps Principles**: Declarative configuration, Git as source of truth, automated reconciliation, observability
- **Repository Patterns**: Monorepo vs multi-repo, application repos vs infrastructure repos, environment branching
- **Synchronization Strategies**: Automated sync, manual approval gates, progressive delivery, drift detection
- **Application Deployment**: Kubernetes manifests, Helm charts, Kustomize overlays, templating strategies
- **Configuration Management**: Environment-specific configs, secrets management, config drift prevention
- **Promotion Workflows**: Dev → staging → production, automated promotions, rollback procedures
- **Access Control**: RBAC patterns, separation of duties, audit trails, compliance requirements
- **Multi-Cluster Management**: Fleet management, cluster bootstrapping, policy enforcement

## Primary Tools & Technologies

- **GitOps Operators**: Flux CD, ArgoCD, Rancher Fleet, Jenkins X
- **Kubernetes Tools**: kubectl, Helm, Kustomize, Kubebuilder
- **Git Platforms**: GitHub, GitLab, Bitbucket, Azure Repos
- **Policy Enforcement**: OPA/Gatekeeper, Kyverno, Polaris
- **Secrets Management**: Sealed Secrets, External Secrets Operator, Vault, SOPS
- **Visualization**: ArgoCD UI, Flux UI, Weave GitOps, Octant

## Integration Points

- **Building CI/CD Pipelines**: CI builds artifacts, GitOps deploys them
- **Infrastructure as Code**: Terraform/Pulumi managed via GitOps
- **Kubernetes Operations**: Cluster configuration and app deployment
- **Security Operations**: Policy enforcement and compliance scanning
- **Platform Engineering**: GitOps as platform delivery mechanism
- **Incident Management**: GitOps for incident response and rollbacks
- **Observability**: Deployment tracking and sync status monitoring

## Use Cases

- Implementing GitOps for microservices on Kubernetes
- Managing multi-environment deployments (dev/staging/prod)
- Automating infrastructure provisioning via GitOps
- Setting up progressive delivery with canary deployments
- Managing configuration drift across clusters
- Implementing policy-driven deployments
- Creating self-service deployment workflows

## Decision Framework

**Choose GitOps tool based on:**
- **Flux CD**: Native Kubernetes, lightweight, multi-tenancy focus
- **ArgoCD**: Rich UI, ApplicationSets, strong RBAC, plugin ecosystem
- **Rancher Fleet**: Multi-cluster at scale, edge deployments
- **Jenkins X**: Opinionated GitOps + CI/CD integrated

**Repository structure based on:**
- **Monorepo**: Single team, tightly coupled apps, simplified dependencies
- **Multi-repo**: Multiple teams, independent release cycles, clear boundaries
- **Hybrid**: Application repos separate, shared infrastructure repo

**Sync strategy based on:**
- **Automated**: Low-risk changes, dev environments, high confidence
- **Manual**: Production deployments, high-risk changes, compliance requirements
- **Progressive**: Gradual rollout, canary analysis, automated rollback
