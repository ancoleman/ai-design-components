# Proposed Skills Expansion

> **Analysis Date**: December 2025
> **Current Skills**: 29
> **Proposed New Skills**: 47
> **Total After Implementation**: 76

This document proposes new skills to expand the AI Design Components library to better serve **Developers**, **Systems Engineers**, **Network Engineers**, **DevOps Engineers**, **Platform Engineers**, and **Security Engineers**.

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Gap Analysis](#gap-analysis)
3. [Skill Level Definitions](#skill-level-definitions)
4. [Proposed Skills by Category](#proposed-skills-by-category)
   - [Infrastructure & Systems](#infrastructure--systems)
   - [Networking](#networking)
   - [Security](#security)
   - [DevOps & Platform](#devops--platform)
   - [Developer Productivity](#developer-productivity)
   - [Data & Analytics](#data--analytics)
   - [AI/ML Operations](#aiml-operations)
5. [Persona Coverage Matrix](#persona-coverage-matrix)
6. [Implementation Priority](#implementation-priority)
7. [Skill Dependencies](#skill-dependencies)

---

## Executive Summary

### Current Library Strengths

The existing 29 skills provide excellent coverage for:
- **Frontend Development**: Comprehensive UI/UX patterns (15 skills)
- **Backend APIs**: Strong API and data layer support (14 skills)
- **Database Diversity**: Relational, vector, document, graph, and time-series
- **Modern AI/ML**: RAG pipelines, embeddings, model serving

### Critical Gaps Identified

| Gap Area | Impact | Priority |
|----------|--------|----------|
| **Infrastructure as Code** | No Terraform/Pulumi patterns beyond basic deployment | Critical |
| **Container Orchestration** | Missing deep Kubernetes operational patterns | Critical |
| **Network Engineering** | No networking, DNS, load balancing skills | High |
| **Security Engineering** | Only auth-security exists; missing threat modeling, SIEM, compliance | Critical |
| **Systems Administration** | No Linux administration, configuration management | High |
| **CI/CD Pipelines** | Deployment skill lacks pipeline construction patterns | High |
| **Testing Strategies** | No testing skills (unit, integration, e2e, performance) | Critical |
| **Cost Optimization** | No FinOps, resource optimization patterns | Medium |
| **Disaster Recovery** | No backup, recovery, business continuity patterns | High |
| **Developer Tooling** | No CLI building, SDK design, documentation generation | Medium |

---

## Gap Analysis

### What Exists vs. What's Missing

```
CURRENT COVERAGE                    MISSING COVERAGE
─────────────────────────────────   ─────────────────────────────────
✅ Frontend UI (15 skills)          ❌ Infrastructure as Code (deep)
✅ API Patterns                     ❌ Container Orchestration (deep)
✅ Database Types (5 skills)        ❌ Network Engineering
✅ Real-time Communication          ❌ Security Operations (SIEM, etc.)
✅ Observability (basic)            ❌ Testing Strategies
✅ Auth & Security (basic)          ❌ CI/CD Pipeline Construction
✅ Deployment (basic)               ❌ Configuration Management
✅ AI Data Engineering              ❌ Disaster Recovery
✅ Model Serving                    ❌ Performance Engineering
                                    ❌ Developer Tooling
                                    ❌ FinOps / Cost Optimization
```

---

## Skill Level Definitions

### High Level Skills (Strategic/Architectural)
- **Scope**: Cross-cutting concerns, architectural patterns, decision frameworks
- **Token Budget**: 8,000-12,000 tokens
- **Purpose**: Guide major technical decisions and system design
- **Example**: `designing-distributed-systems`, `security-architecture`

### Mid Level Skills (Implementation Patterns)
- **Scope**: Specific technology implementations, integration patterns
- **Token Budget**: 5,000-8,000 tokens
- **Purpose**: Implement complete subsystems or features
- **Example**: `kubernetes-operations`, `building-ci-pipelines`

### Low Level Skills (Tactical/Quick Reference)
- **Scope**: Single-purpose utilities, quick patterns, specific tools
- **Token Budget**: 2,000-5,000 tokens
- **Purpose**: Fast execution of common tasks
- **Example**: `writing-dockerfiles`, `configuring-nginx`

---

## Proposed Skills by Category

---

## Infrastructure & Systems

### High Level

#### 1. `designing-distributed-systems`
**Purpose**: Architectural patterns for distributed systems including CAP theorem applications, consistency models, and failure handling.

**Covers**:
- Consistency patterns (eventual, strong, causal)
- Partitioning strategies (hash, range, geo)
- Replication patterns (leader-follower, multi-leader, leaderless)
- Consensus algorithms (Raft, Paxos concepts)
- Circuit breakers, bulkheads, timeouts
- Saga patterns for distributed transactions

**Persona**: Systems Engineer, Platform Engineer, Senior Developer

**Chains With**: `api-patterns`, `message-queues`, `databases-*`

---

#### 2. `infrastructure-as-code`
**Purpose**: Comprehensive IaC patterns beyond basic deployment, covering state management, module design, and multi-environment strategies.

**Covers**:
- Terraform/OpenTofu patterns (modules, workspaces, state management)
- Pulumi with TypeScript/Python/Go
- CloudFormation/CDK patterns
- State locking, remote backends
- Drift detection and remediation
- Module composition and versioning
- Secret management in IaC

**Persona**: DevOps Engineer, Platform Engineer, Systems Engineer

**Chains With**: `deploying-applications`, `kubernetes-operations`

---

### Mid Level

#### 3. `kubernetes-operations`
**Purpose**: Deep Kubernetes operational patterns beyond basic deployment.

**Covers**:
- Resource management (requests, limits, QoS classes)
- Scheduling (affinity, taints, tolerations, topology spread)
- Networking (NetworkPolicies, Ingress, Service mesh basics)
- Storage (PV/PVC, StorageClasses, CSI drivers)
- Security (RBAC, PodSecurityStandards, OPA/Kyverno)
- Autoscaling (HPA, VPA, KEDA, Cluster Autoscaler)
- Troubleshooting (debugging pods, node issues, networking)

**Persona**: DevOps Engineer, Platform Engineer, Systems Engineer

**Chains With**: `deploying-applications`, `observability`, `infrastructure-as-code`

---

#### 4. `configuration-management`
**Purpose**: Configuration management with Ansible, Chef, Puppet, and modern alternatives.

**Covers**:
- Ansible playbooks, roles, and collections
- Inventory management (static, dynamic)
- Idempotency patterns
- Secret management in configuration
- Testing configurations (Molecule, kitchen-ci)
- GitOps for configuration

**Persona**: Systems Engineer, DevOps Engineer

**Chains With**: `infrastructure-as-code`, `deploying-applications`

---

#### 5. `linux-administration`
**Purpose**: Linux system administration patterns for production environments.

**Covers**:
- Systemd service management
- Process management and monitoring
- Filesystem management (LVM, ZFS, XFS)
- User/group management and sudo
- Package management (apt, yum, dnf)
- Performance tuning (sysctl, ulimits)
- Log management (journald, rsyslog)
- Cron and systemd timers

**Persona**: Systems Engineer, DevOps Engineer

**Chains With**: `configuration-management`, `observability`

---

### Low Level

#### 6. `writing-dockerfiles`
**Purpose**: Dockerfile best practices for efficient, secure container images.

**Covers**:
- Multi-stage builds
- Layer optimization
- Security hardening (non-root, distroless)
- Build arguments and secrets
- Health checks
- Language-specific patterns (Python, Node, Go, Rust)

**Persona**: Developer, DevOps Engineer

**Chains With**: `deploying-applications`, `kubernetes-operations`

---

#### 7. `shell-scripting`
**Purpose**: Bash/shell scripting patterns for automation.

**Covers**:
- Error handling (set -euo pipefail)
- Argument parsing (getopts, manual)
- Functions and modularity
- Process substitution
- Common utilities (awk, sed, jq, yq)
- Cross-platform considerations

**Persona**: Systems Engineer, DevOps Engineer, Developer

**Chains With**: `linux-administration`, `building-ci-pipelines`

---

## Networking

### High Level

#### 8. `network-architecture`
**Purpose**: Network design patterns for cloud and hybrid environments.

**Covers**:
- VPC design patterns (hub-spoke, mesh)
- Subnet strategy (public, private, isolated)
- Network segmentation and microsegmentation
- Hybrid connectivity (VPN, Direct Connect, ExpressRoute)
- Multi-region networking
- Zero trust network architecture
- DNS architecture

**Persona**: Network Engineer, Platform Engineer, Security Engineer

**Chains With**: `infrastructure-as-code`, `kubernetes-operations`

---

### Mid Level

#### 9. `load-balancing-patterns`
**Purpose**: Load balancing strategies across L4 and L7.

**Covers**:
- L4 vs L7 load balancing trade-offs
- Cloud load balancers (ALB, NLB, Cloud Load Balancing)
- Self-managed (HAProxy, NGINX, Envoy)
- Health check patterns
- Session persistence strategies
- SSL/TLS termination
- Global load balancing and GeoDNS

**Persona**: Network Engineer, Platform Engineer, DevOps Engineer

**Chains With**: `kubernetes-operations`, `api-patterns`

---

#### 10. `dns-management`
**Purpose**: DNS configuration, optimization, and troubleshooting.

**Covers**:
- Record types and use cases (A, AAAA, CNAME, MX, TXT, SRV)
- TTL strategies
- DNS-based load balancing
- Split-horizon DNS
- DNSSEC
- DNS as code (external-dns, OctoDNS)
- Troubleshooting (dig, nslookup, DNS propagation)

**Persona**: Network Engineer, Systems Engineer, DevOps Engineer

**Chains With**: `load-balancing-patterns`, `infrastructure-as-code`

---

#### 11. `service-mesh`
**Purpose**: Service mesh implementation with Istio, Linkerd, or Cilium.

**Covers**:
- Sidecar vs sidecar-less architecture
- Traffic management (routing, retries, timeouts)
- Observability (distributed tracing, metrics)
- Security (mTLS, authorization policies)
- Istio vs Linkerd vs Cilium trade-offs
- Progressive rollouts with mesh

**Persona**: Platform Engineer, Network Engineer, DevOps Engineer

**Chains With**: `kubernetes-operations`, `observability`, `auth-security`

---

### Low Level

#### 12. `configuring-nginx`
**Purpose**: NGINX configuration patterns for web serving and proxying.

**Covers**:
- Reverse proxy configuration
- SSL/TLS setup
- Rate limiting
- Caching strategies
- WebSocket proxying
- Security headers
- Performance tuning

**Persona**: DevOps Engineer, Systems Engineer, Developer

**Chains With**: `load-balancing-patterns`, `api-patterns`

---

#### 13. `configuring-firewalls`
**Purpose**: Firewall rules and network security configuration.

**Covers**:
- iptables/nftables basics
- Cloud security groups (AWS, GCP, Azure)
- UFW for simple setups
- Stateful vs stateless rules
- Common security patterns (bastion, DMZ)
- Logging and auditing

**Persona**: Network Engineer, Security Engineer, Systems Engineer

**Chains With**: `network-architecture`, `security-hardening`

---

## Security

### High Level

#### 14. `security-architecture`
**Purpose**: Security architecture patterns and frameworks for secure system design.

**Covers**:
- Defense in depth strategies
- Zero trust architecture implementation
- Security reference architectures
- Threat modeling (STRIDE, PASTA)
- Security controls mapping (NIST, CIS)
- Secure SDLC integration
- Supply chain security

**Persona**: Security Engineer, Platform Engineer, Systems Engineer

**Chains With**: `auth-security`, `network-architecture`, `kubernetes-operations`

---

#### 15. `compliance-frameworks`
**Purpose**: Implementing compliance requirements (SOC2, HIPAA, PCI-DSS, GDPR).

**Covers**:
- Control mapping by framework
- Evidence collection automation
- Audit logging requirements
- Data classification
- Retention policies
- Privacy by design patterns
- Compliance as code

**Persona**: Security Engineer, Platform Engineer, DevOps Engineer

**Chains With**: `observability`, `security-architecture`, `auth-security`

---

### Mid Level

#### 16. `security-hardening`
**Purpose**: System and application hardening patterns.

**Covers**:
- CIS benchmarks implementation
- OS hardening (Linux, Windows)
- Container hardening
- Cloud configuration hardening
- Database security hardening
- Network hardening
- Automated hardening verification

**Persona**: Security Engineer, Systems Engineer, DevOps Engineer

**Chains With**: `linux-administration`, `kubernetes-operations`, `databases-*`

---

#### 17. `secret-management`
**Purpose**: Secrets management with HashiCorp Vault, AWS Secrets Manager, and alternatives.

**Covers**:
- Vault architecture and operations
- Dynamic secrets
- Secret rotation patterns
- Kubernetes secrets integration (ESO, CSI driver)
- Application integration patterns
- Secret scanning and remediation
- Zero-knowledge patterns

**Persona**: Security Engineer, DevOps Engineer, Platform Engineer

**Chains With**: `infrastructure-as-code`, `kubernetes-operations`, `auth-security`

---

#### 18. `vulnerability-management`
**Purpose**: Vulnerability scanning, prioritization, and remediation workflows.

**Covers**:
- Container image scanning (Trivy, Grype, Snyk)
- SAST/DAST integration
- SCA for dependency scanning
- SBOM generation and management
- Vulnerability prioritization (CVSS, EPSS)
- Remediation workflows
- CI/CD security gates

**Persona**: Security Engineer, DevOps Engineer, Developer

**Chains With**: `building-ci-pipelines`, `writing-dockerfiles`

---

#### 19. `siem-logging`
**Purpose**: Security information and event management patterns.

**Covers**:
- Log aggregation architecture
- Security event correlation
- Alert tuning and fatigue reduction
- Threat detection rules
- SIEM tools (Splunk, Elastic SIEM, Sentinel)
- Log retention and compliance
- Incident response integration

**Persona**: Security Engineer, Systems Engineer

**Chains With**: `observability`, `compliance-frameworks`

---

### Low Level

#### 20. `implementing-tls`
**Purpose**: TLS configuration and certificate management.

**Covers**:
- Certificate generation (openssl, cfssl)
- ACME/Let's Encrypt automation
- Certificate manager (cert-manager, Caddy)
- mTLS patterns
- Cipher suite selection
- Certificate rotation
- Debugging TLS issues

**Persona**: Security Engineer, DevOps Engineer, Systems Engineer

**Chains With**: `configuring-nginx`, `kubernetes-operations`, `service-mesh`

---

## DevOps & Platform

### High Level

#### 21. `platform-engineering`
**Purpose**: Building internal developer platforms (IDP) and golden paths.

**Covers**:
- Platform architecture patterns
- Service catalogs (Backstage, Port)
- Self-service infrastructure
- Golden paths and templates
- Developer experience metrics
- Platform team operating model
- API-first platform design

**Persona**: Platform Engineer, DevOps Engineer

**Chains With**: `infrastructure-as-code`, `kubernetes-operations`, `building-ci-pipelines`

---

#### 22. `disaster-recovery`
**Purpose**: Backup, recovery, and business continuity patterns.

**Covers**:
- RTO/RPO planning
- Backup strategies (full, incremental, differential)
- Database backup patterns
- Cross-region replication
- Chaos engineering basics
- Runbook automation
- DR testing procedures

**Persona**: Systems Engineer, Platform Engineer, DevOps Engineer

**Chains With**: `databases-*`, `kubernetes-operations`, `infrastructure-as-code`

---

### Mid Level

#### 23. `building-ci-pipelines`
**Purpose**: CI/CD pipeline construction patterns.

**Covers**:
- GitHub Actions patterns
- GitLab CI patterns
- Jenkins pipelines
- Tekton/Argo Workflows
- Pipeline security (secrets, SLSA)
- Caching strategies
- Parallelization patterns
- Monorepo CI patterns

**Persona**: DevOps Engineer, Developer, Platform Engineer

**Chains With**: `deploying-applications`, `vulnerability-management`

---

#### 24. `gitops-workflows`
**Purpose**: GitOps implementation with ArgoCD, Flux, and alternatives.

**Covers**:
- GitOps principles and patterns
- ArgoCD setup and patterns
- Flux setup and patterns
- Application sets and generators
- Secret management in GitOps
- Multi-cluster GitOps
- Promotion strategies

**Persona**: DevOps Engineer, Platform Engineer

**Chains With**: `kubernetes-operations`, `infrastructure-as-code`, `building-ci-pipelines`

---

#### 25. `performance-engineering`
**Purpose**: Performance testing, profiling, and optimization patterns.

**Covers**:
- Load testing (k6, Locust, Gatling)
- Performance profiling (pprof, py-spy, perf)
- APM integration
- Bottleneck identification
- Database query optimization
- Caching strategies
- CDN optimization

**Persona**: Developer, DevOps Engineer, Systems Engineer

**Chains With**: `observability`, `api-patterns`, `databases-*`

---

#### 26. `incident-management`
**Purpose**: Incident response and on-call patterns.

**Covers**:
- Incident classification and severity
- On-call rotations (PagerDuty, Opsgenie)
- Runbook design
- Incident command structure
- Post-incident reviews (blameless)
- SLO/SLA management
- Automated remediation

**Persona**: DevOps Engineer, Systems Engineer, Platform Engineer

**Chains With**: `observability`, `siem-logging`

---

### Low Level

#### 27. `writing-github-actions`
**Purpose**: GitHub Actions workflow patterns and best practices.

**Covers**:
- Workflow syntax deep dive
- Reusable workflows
- Composite actions
- Matrix builds
- Caching patterns
- Secrets handling
- Self-hosted runners

**Persona**: Developer, DevOps Engineer

**Chains With**: `building-ci-pipelines`

---

## Developer Productivity

### High Level

#### 28. `api-design-principles`
**Purpose**: API design standards, versioning strategies, and documentation.

**Covers**:
- RESTful design principles
- API versioning strategies
- Error response standards
- Pagination patterns
- Rate limiting design
- API documentation (OpenAPI, AsyncAPI)
- Breaking change management

**Persona**: Developer, Platform Engineer

**Chains With**: `api-patterns`, `building-forms` (client consumption)

---

### Mid Level

#### 29. `testing-strategies`
**Purpose**: Comprehensive testing patterns across the testing pyramid.

**Covers**:
- Unit testing patterns (pytest, Jest, Go testing)
- Integration testing strategies
- E2E testing (Playwright, Cypress)
- Contract testing (Pact)
- Test data management
- Mocking and stubbing patterns
- Test coverage analysis
- Property-based testing

**Persona**: Developer, DevOps Engineer

**Chains With**: `building-ci-pipelines`, `api-patterns`

---

#### 30. `building-clis`
**Purpose**: CLI application development patterns.

**Covers**:
- CLI frameworks (Click/Typer, Cobra, clap)
- Argument parsing patterns
- Interactive prompts
- Configuration management
- Output formatting (tables, JSON, colors)
- Progress indicators
- Shell completion
- Distribution patterns

**Persona**: Developer, DevOps Engineer

**Chains With**: `shell-scripting`

---

#### 31. `sdk-design`
**Purpose**: SDK/client library design patterns.

**Covers**:
- SDK architecture patterns
- Authentication handling
- Retry and backoff strategies
- Error handling patterns
- Pagination abstraction
- Async/sync API design
- Multi-language considerations
- Versioning and deprecation

**Persona**: Developer, Platform Engineer

**Chains With**: `api-patterns`, `testing-strategies`

---

#### 32. `documentation-generation`
**Purpose**: Automated documentation from code and specifications.

**Covers**:
- API documentation (Swagger UI, Redoc)
- Code documentation (Sphinx, TypeDoc, rustdoc)
- Documentation as code (Docusaurus, MkDocs)
- Changelog automation
- ADR (Architecture Decision Records)
- Diagram generation (Mermaid, PlantUML)

**Persona**: Developer, Platform Engineer

**Chains With**: `api-patterns`, `api-design-principles`

---

### Low Level

#### 33. `debugging-techniques`
**Purpose**: Debugging patterns across languages and environments.

**Covers**:
- Language-specific debuggers (pdb, delve, lldb)
- Remote debugging
- Container debugging
- Production debugging (safely)
- Log-based debugging
- Memory profiling
- Core dump analysis

**Persona**: Developer, Systems Engineer

**Chains With**: `observability`, `linux-administration`

---

#### 34. `git-workflows`
**Purpose**: Git branching strategies and collaboration patterns.

**Covers**:
- Branching strategies (trunk-based, GitFlow, GitHub Flow)
- Merge vs rebase patterns
- Conventional commits
- Code review workflows
- Monorepo patterns
- Git hooks
- Large file handling (LFS)

**Persona**: Developer, DevOps Engineer

**Chains With**: `building-ci-pipelines`, `gitops-workflows`

---

## Data & Analytics

### High Level

#### 35. `data-architecture`
**Purpose**: Data architecture patterns for modern data platforms.

**Covers**:
- Data mesh principles
- Data lakehouse architecture
- Data warehouse patterns
- Data governance frameworks
- Data quality patterns
- Metadata management
- Data lineage

**Persona**: Developer, Platform Engineer, Systems Engineer

**Chains With**: `databases-*`, `ingesting-data`, `ai-data-engineering`

---

### Mid Level

#### 36. `streaming-data`
**Purpose**: Stream processing patterns beyond basic message queues.

**Covers**:
- Apache Kafka Streams
- Apache Flink patterns
- Spark Streaming
- Windowing strategies
- Exactly-once semantics
- Stream-table duality
- Real-time analytics

**Persona**: Developer, Systems Engineer

**Chains With**: `message-queues`, `ingesting-data`, `databases-timeseries`

---

#### 37. `data-transformation`
**Purpose**: Data transformation and ETL/ELT patterns.

**Covers**:
- dbt patterns
- Spark transformations
- Pandas/Polars patterns
- SQL transformation patterns
- Data validation (Great Expectations, Soda)
- Orchestration integration

**Persona**: Developer, Systems Engineer

**Chains With**: `ingesting-data`, `databases-*`, `ai-data-engineering`

---

### Low Level

#### 38. `sql-optimization`
**Purpose**: SQL query optimization and performance patterns.

**Covers**:
- Query plan analysis (EXPLAIN)
- Index design patterns
- Query rewriting techniques
- Join optimization
- Common table expressions (CTEs)
- Window functions
- Partitioning strategies

**Persona**: Developer, Systems Engineer

**Chains With**: `databases-relational`, `performance-engineering`

---

## AI/ML Operations

### High Level

#### 39. `mlops-patterns`
**Purpose**: MLOps patterns for production ML systems.

**Covers**:
- ML pipeline design
- Feature store patterns
- Model registry
- A/B testing for ML
- Model monitoring and drift detection
- Retraining strategies
- ML governance

**Persona**: Developer, Platform Engineer

**Chains With**: `ai-data-engineering`, `model-serving`, `observability`

---

### Mid Level

#### 40. `prompt-engineering`
**Purpose**: Prompt engineering patterns for LLM applications.

**Covers**:
- Prompt design patterns
- Chain-of-thought prompting
- Few-shot learning patterns
- Prompt templates and management
- Output parsing and validation
- Cost optimization
- Guardrails and safety

**Persona**: Developer

**Chains With**: `model-serving`, `building-ai-chat`

---

#### 41. `llm-evaluation`
**Purpose**: LLM application evaluation and testing patterns.

**Covers**:
- Evaluation frameworks (RAGAS, DeepEval)
- Human evaluation patterns
- Automated test generation
- Regression testing for LLMs
- Benchmark creation
- Bias detection
- Quality metrics

**Persona**: Developer

**Chains With**: `ai-data-engineering`, `prompt-engineering`, `testing-strategies`

---

### Low Level

#### 42. `embedding-optimization`
**Purpose**: Embedding generation and optimization patterns.

**Covers**:
- Embedding model selection
- Chunking strategies (advanced)
- Hybrid search tuning
- Embedding caching
- Dimensionality reduction
- Batch processing optimization
- Fine-tuning embeddings

**Persona**: Developer

**Chains With**: `databases-vector`, `ai-data-engineering`

---

## Cloud-Specific Skills

### Mid Level

#### 43. `aws-patterns`
**Purpose**: AWS-specific architecture and service patterns.

**Covers**:
- Well-Architected Framework application
- Cost optimization patterns
- Service selection decision trees
- Multi-account strategies (Organizations, Control Tower)
- Common service patterns (Lambda, ECS, EKS, RDS)
- IAM patterns and best practices

**Persona**: DevOps Engineer, Platform Engineer, Systems Engineer

**Chains With**: `infrastructure-as-code`, `kubernetes-operations`

---

#### 44. `gcp-patterns`
**Purpose**: GCP-specific architecture and service patterns.

**Covers**:
- GCP architecture patterns
- Project and folder structure
- Service selection (Cloud Run, GKE, Cloud SQL)
- IAM and organization policies
- BigQuery patterns
- Cloud Functions patterns

**Persona**: DevOps Engineer, Platform Engineer, Systems Engineer

**Chains With**: `infrastructure-as-code`, `kubernetes-operations`

---

#### 45. `azure-patterns`
**Purpose**: Azure-specific architecture and service patterns.

**Covers**:
- Azure architecture patterns
- Subscription and management group design
- Service selection (AKS, Azure Functions, CosmosDB)
- Azure AD integration
- Azure DevOps patterns
- Landing zone patterns

**Persona**: DevOps Engineer, Platform Engineer, Systems Engineer

**Chains With**: `infrastructure-as-code`, `kubernetes-operations`

---

## FinOps

### Mid Level

#### 46. `cost-optimization`
**Purpose**: Cloud cost optimization and FinOps patterns.

**Covers**:
- Cost visibility and allocation
- Right-sizing strategies
- Reserved/committed use discounts
- Spot/preemptible instance patterns
- Storage optimization
- Network cost optimization
- Showback/chargeback models

**Persona**: DevOps Engineer, Platform Engineer, Systems Engineer

**Chains With**: `kubernetes-operations`, `infrastructure-as-code`, `observability`

---

### Low Level

#### 47. `resource-tagging`
**Purpose**: Resource tagging strategies for governance and cost allocation.

**Covers**:
- Tagging strategy design
- Mandatory vs optional tags
- Tag enforcement (policies)
- Tag-based automation
- Cost allocation tags
- Compliance tagging

**Persona**: DevOps Engineer, Platform Engineer

**Chains With**: `infrastructure-as-code`, `cost-optimization`

---

## Persona Coverage Matrix

| Skill | Developer | Systems Eng | Network Eng | DevOps Eng | Platform Eng | Security Eng |
|-------|:---------:|:-----------:|:-----------:|:----------:|:------------:|:------------:|
| **Infrastructure & Systems** |
| designing-distributed-systems | ◐ | ● | ○ | ◐ | ● | ○ |
| infrastructure-as-code | ◐ | ● | ◐ | ● | ● | ◐ |
| kubernetes-operations | ◐ | ● | ◐ | ● | ● | ◐ |
| configuration-management | ○ | ● | ○ | ● | ◐ | ○ |
| linux-administration | ◐ | ● | ◐ | ● | ◐ | ◐ |
| writing-dockerfiles | ● | ◐ | ○ | ● | ◐ | ○ |
| shell-scripting | ● | ● | ◐ | ● | ◐ | ◐ |
| **Networking** |
| network-architecture | ○ | ◐ | ● | ◐ | ● | ● |
| load-balancing-patterns | ◐ | ◐ | ● | ● | ● | ○ |
| dns-management | ◐ | ◐ | ● | ● | ◐ | ○ |
| service-mesh | ◐ | ○ | ● | ● | ● | ◐ |
| configuring-nginx | ◐ | ◐ | ◐ | ● | ◐ | ○ |
| configuring-firewalls | ○ | ◐ | ● | ◐ | ◐ | ● |
| **Security** |
| security-architecture | ◐ | ● | ◐ | ◐ | ● | ● |
| compliance-frameworks | ○ | ◐ | ○ | ◐ | ● | ● |
| security-hardening | ◐ | ● | ◐ | ● | ◐ | ● |
| secret-management | ◐ | ◐ | ○ | ● | ● | ● |
| vulnerability-management | ● | ◐ | ○ | ● | ◐ | ● |
| siem-logging | ○ | ● | ○ | ◐ | ◐ | ● |
| implementing-tls | ◐ | ◐ | ◐ | ● | ◐ | ● |
| **DevOps & Platform** |
| platform-engineering | ◐ | ○ | ○ | ● | ● | ○ |
| disaster-recovery | ○ | ● | ◐ | ● | ● | ◐ |
| building-ci-pipelines | ● | ◐ | ○ | ● | ● | ◐ |
| gitops-workflows | ◐ | ○ | ○ | ● | ● | ○ |
| performance-engineering | ● | ● | ○ | ● | ◐ | ○ |
| incident-management | ○ | ● | ◐ | ● | ● | ◐ |
| writing-github-actions | ● | ○ | ○ | ● | ◐ | ○ |
| **Developer Productivity** |
| api-design-principles | ● | ○ | ○ | ◐ | ● | ○ |
| testing-strategies | ● | ◐ | ○ | ● | ◐ | ◐ |
| building-clis | ● | ◐ | ○ | ● | ◐ | ○ |
| sdk-design | ● | ○ | ○ | ◐ | ● | ○ |
| documentation-generation | ● | ○ | ○ | ◐ | ● | ○ |
| debugging-techniques | ● | ● | ○ | ◐ | ○ | ○ |
| git-workflows | ● | ◐ | ○ | ● | ◐ | ○ |
| **Data & Analytics** |
| data-architecture | ● | ● | ○ | ◐ | ● | ◐ |
| streaming-data | ● | ● | ○ | ◐ | ◐ | ○ |
| data-transformation | ● | ◐ | ○ | ◐ | ◐ | ○ |
| sql-optimization | ● | ◐ | ○ | ◐ | ◐ | ○ |
| **AI/ML Operations** |
| mlops-patterns | ● | ○ | ○ | ◐ | ● | ○ |
| prompt-engineering | ● | ○ | ○ | ○ | ◐ | ○ |
| llm-evaluation | ● | ○ | ○ | ○ | ◐ | ○ |
| embedding-optimization | ● | ○ | ○ | ○ | ◐ | ○ |
| **Cloud & FinOps** |
| aws-patterns | ◐ | ● | ◐ | ● | ● | ◐ |
| gcp-patterns | ◐ | ● | ◐ | ● | ● | ◐ |
| azure-patterns | ◐ | ● | ◐ | ● | ● | ◐ |
| cost-optimization | ○ | ◐ | ○ | ● | ● | ○ |
| resource-tagging | ○ | ◐ | ○ | ● | ● | ◐ |

**Legend**: ● Primary User | ◐ Regular User | ○ Occasional User

---

## Implementation Priority

### Phase 1: Critical (Implement First)
High-impact skills addressing the largest gaps:

| Priority | Skill | Rationale |
|----------|-------|-----------|
| 1 | `testing-strategies` | Every project needs testing; currently zero coverage |
| 2 | `building-ci-pipelines` | Deployment exists but pipeline construction missing |
| 3 | `kubernetes-operations` | Deep K8s knowledge essential for modern deployments |
| 4 | `infrastructure-as-code` | Critical for reproducible infrastructure |
| 5 | `security-hardening` | Security beyond auth is critical gap |
| 6 | `secret-management` | Secrets handling is fundamental security need |

### Phase 2: High Priority
Fills significant gaps for core personas:

| Priority | Skill | Rationale |
|----------|-------|-----------|
| 7 | `gitops-workflows` | Natural extension of deployment skill |
| 8 | `linux-administration` | Foundation for systems engineering |
| 9 | `network-architecture` | Major gap for network engineers |
| 10 | `load-balancing-patterns` | Critical for production systems |
| 11 | `disaster-recovery` | Business continuity is essential |
| 12 | `performance-engineering` | Performance optimization is common need |

### Phase 3: Medium Priority
Expands capability for specialized use cases:

| Priority | Skill | Rationale |
|----------|-------|-----------|
| 13-18 | Remaining Security skills | Complete security coverage |
| 19-24 | Developer Productivity skills | Enhance developer workflows |
| 25-30 | Data & Analytics skills | Deep data engineering |
| 31-35 | Cloud-specific patterns | Platform specialization |

### Phase 4: Enhancement
Nice-to-have for complete coverage:

| Priority | Skill | Rationale |
|----------|-------|-----------|
| 36-42 | Low-level tactical skills | Quick reference utilities |
| 43-47 | FinOps and specialized skills | Optimization focus |

---

## Skill Dependencies

```
                                    ┌─────────────────────────┐
                                    │   security-architecture  │
                                    └────────────┬────────────┘
                                                 │
                    ┌────────────────────────────┼────────────────────────────┐
                    ▼                            ▼                            ▼
         ┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐
         │ compliance-      │         │ security-        │         │ network-         │
         │ frameworks       │         │ hardening        │         │ architecture     │
         └────────┬─────────┘         └────────┬─────────┘         └────────┬─────────┘
                  │                            │                            │
                  ▼                            ▼                            ▼
         ┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐
         │ siem-logging     │         │ secret-          │         │ load-balancing   │
         │                  │         │ management       │         │ patterns         │
         └──────────────────┘         └────────┬─────────┘         └────────┬─────────┘
                                               │                            │
                                               ▼                            ▼
                                      ┌──────────────────┐         ┌──────────────────┐
                                      │ implementing-tls │         │ service-mesh     │
                                      └──────────────────┘         └──────────────────┘


         ┌──────────────────────────────────────────────────────────────────┐
         │                    infrastructure-as-code                        │
         └──────────────────────────────┬───────────────────────────────────┘
                                        │
              ┌─────────────────────────┼─────────────────────────┐
              ▼                         ▼                         ▼
    ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
    │ kubernetes-      │     │ configuration-   │     │ cloud-patterns   │
    │ operations       │     │ management       │     │ (aws/gcp/azure)  │
    └────────┬─────────┘     └────────┬─────────┘     └──────────────────┘
             │                        │
             ▼                        ▼
    ┌──────────────────┐     ┌──────────────────┐
    │ gitops-workflows │     │ linux-           │
    │                  │     │ administration   │
    └────────┬─────────┘     └──────────────────┘
             │
             ▼
    ┌──────────────────┐
    │ platform-        │
    │ engineering      │
    └──────────────────┘


         ┌──────────────────────────────────────────────────────────────────┐
         │                    testing-strategies                             │
         └──────────────────────────────┬───────────────────────────────────┘
                                        │
              ┌─────────────────────────┼─────────────────────────┐
              ▼                         ▼                         ▼
    ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
    │ building-ci-     │     │ performance-     │     │ llm-evaluation   │
    │ pipelines        │     │ engineering      │     │                  │
    └────────┬─────────┘     └──────────────────┘     └──────────────────┘
             │
             ▼
    ┌──────────────────┐
    │ writing-github-  │
    │ actions          │
    └──────────────────┘
```

---

## Summary

### Skill Count by Category

| Category | Current | Proposed | Total |
|----------|---------|----------|-------|
| Frontend UI/UX | 15 | 0 | 15 |
| Backend APIs & Data | 14 | 0 | 14 |
| Infrastructure & Systems | 0 | 7 | 7 |
| Networking | 0 | 6 | 6 |
| Security | 1 | 7 | 8 |
| DevOps & Platform | 1 | 7 | 8 |
| Developer Productivity | 0 | 7 | 7 |
| Data & Analytics | 2 | 4 | 6 |
| AI/ML Operations | 2 | 4 | 6 |
| Cloud-Specific | 0 | 3 | 3 |
| FinOps | 0 | 2 | 2 |
| **Total** | **29** | **47** | **76** |

### Skills by Level

| Level | Count | Purpose |
|-------|-------|---------|
| High Level | 12 | Strategic/Architectural decisions |
| Mid Level | 25 | Implementation patterns |
| Low Level | 10 | Tactical quick reference |

### Persona Coverage Improvement

| Persona | Current Skills | New Skills | Total |
|---------|---------------|------------|-------|
| Developer | 25 | 35 | 60 |
| Systems Engineer | 10 | 38 | 48 |
| Network Engineer | 3 | 25 | 28 |
| DevOps Engineer | 12 | 42 | 54 |
| Platform Engineer | 15 | 40 | 55 |
| Security Engineer | 5 | 30 | 35 |

---

## Next Steps

1. **Validate priorities** with team feedback
2. **Begin Phase 1** skill development (testing-strategies, building-ci-pipelines)
3. **Establish templates** for each skill level
4. **Define token budgets** for each level
5. **Create skill dependency graph** in skillchain command
6. **Iterate** based on usage patterns
