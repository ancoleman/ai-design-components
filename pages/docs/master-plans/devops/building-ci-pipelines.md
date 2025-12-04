---
sidebar_position: 1
---

# Building CI/CD Pipelines

Master plan for designing, implementing, and optimizing continuous integration and continuous delivery pipelines. This skill covers pipeline architecture patterns, build optimization, deployment strategies, and integration with modern development workflows.

**Status**: 🟢 Master Plan Available

## Key Topics

- **Pipeline Architecture**: Multi-stage pipelines, parallel execution, job dependencies, artifact management
- **Build Optimization**: Caching strategies, incremental builds, distributed builds, build matrix patterns
- **Testing Integration**: Unit tests, integration tests, E2E tests, security scanning, test parallelization
- **Deployment Strategies**: Blue-green deployments, canary releases, rolling updates, feature flags
- **Pipeline Triggers**: Git hooks, scheduled builds, manual approvals, external events
- **Environment Management**: Environment variables, secrets management, environment promotion
- **Monitoring & Observability**: Build metrics, failure analysis, pipeline health dashboards
- **Multi-Platform Builds**: Cross-platform compilation, Docker builds, native builds

## Primary Tools & Technologies

- **CI/CD Platforms**: GitHub Actions, GitLab CI, Jenkins, CircleCI, Azure DevOps, Buildkite
- **Build Tools**: Make, Gradle, Maven, Bazel, Yarn, npm, Go modules
- **Container Tools**: Docker, Buildah, Kaniko, BuildKit
- **Testing Frameworks**: Jest, pytest, JUnit, Cypress, Playwright
- **Security Scanning**: Snyk, Trivy, SonarQube, GitHub Advanced Security
- **Artifact Storage**: Artifactory, Nexus, GitHub Packages, Azure Artifacts

## Integration Points

- **GitOps Workflows**: Pipeline outputs trigger GitOps deployments
- **Writing Dockerfiles**: Container builds within CI pipelines
- **Testing Strategies**: Test execution and reporting in pipelines
- **Platform Engineering**: Pipelines as part of internal developer platforms
- **Incident Management**: Automated rollbacks and incident response
- **Infrastructure as Code**: Infrastructure validation and deployment
- **Security Operations**: Security scanning and compliance checks

## Use Cases

- Setting up CI/CD for microservices architectures
- Implementing monorepo build strategies
- Optimizing slow build and test pipelines
- Designing deployment pipelines with multiple environments
- Creating reusable pipeline templates
- Implementing security scanning in CI/CD
- Building cross-platform release pipelines

## Decision Framework

**Choose pipeline strategy based on:**
- Repository structure (monorepo vs multi-repo)
- Team size and workflow (trunk-based vs feature branches)
- Deployment frequency (continuous vs scheduled)
- Security requirements (compliance, scanning, approvals)
- Infrastructure target (Kubernetes, VMs, serverless, hybrid)

**Optimize for:**
- Fast feedback (failing fast on errors)
- Developer experience (clear logs, easy troubleshooting)
- Resource efficiency (parallelization, caching)
- Reliability (retries, idempotency, rollback capabilities)
