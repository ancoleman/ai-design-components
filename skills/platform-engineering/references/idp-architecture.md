# Internal Developer Platform (IDP) Architecture

## Table of Contents

1. [Three-Layer Architecture](#three-layer-architecture)
2. [Developer Portal Layer](#developer-portal-layer)
3. [Platform Orchestration Layer](#platform-orchestration-layer)
4. [Integration Layer](#integration-layer)
5. [Reference Architecture Diagrams](#reference-architecture-diagrams)

## Three-Layer Architecture

An Internal Developer Platform consists of three architectural layers that work together to provide a comprehensive developer experience:

```
┌─────────────────────────────────────────────────────────┐
│         Developer Portal (Frontend Layer)              │
│  - Service Catalog    - Software Templates             │
│  - Documentation Hub  - Workflow Automation             │
└─────────────────────────────────────────────────────────┘
                          ↓ ↑
┌─────────────────────────────────────────────────────────┐
│         Integration Layer (Glue)                        │
│  - API Gateway      - CI/CD Integration                 │
│  - Observability    - Security Integration              │
│  - FinOps           - Secrets Management                │
└─────────────────────────────────────────────────────────┘
                          ↓ ↑
┌─────────────────────────────────────────────────────────┐
│         Platform Orchestration (Backend Layer)          │
│  - Infrastructure Provisioning                          │
│  - Environment Management                               │
│  - Deployment Automation (GitOps)                       │
└─────────────────────────────────────────────────────────┘
```

## Developer Portal Layer

### Purpose

Provide a unified interface for developers to discover, create, and manage services without needing to understand underlying infrastructure complexity.

### Core Components

#### 1. Service Catalog

**Function:** Centralized inventory of all software assets with ownership, dependencies, and health status.

**Key Features:**
- Software inventory (services, APIs, libraries, data pipelines, ML models)
- Ownership tracking (teams, individuals, on-call rotation)
- Dependency mapping (upstream/downstream relationships, service mesh topology)
- Health and SLO status (real-time metrics, historical trends)
- Documentation links (architecture diagrams, runbooks, API specifications)
- Metadata (tech stack, cloud provider, cost attribution)

**Implementation Examples:**

**Backstage Software Catalog:**
- YAML metadata files in service repositories
- API for programmatic access
- Plugins for enrichment (pull deployment status, cost data)
- Discovery: Automatic scanning of repositories

**Port Service Catalog:**
- Entity modeling (define custom entities beyond services)
- Blueprints for entity types
- Scorecard system (track service quality, compliance)

**Cortex Service Catalog:**
- Compliance scoring (based on best practices)
- Integration with incident management (PagerDuty, Opsgenie)
- Service health scoring

#### 2. Software Templates / Scaffolders

**Function:** Project initialization with best practices, infrastructure, and CI/CD configurations baked in.

**Template Components:**
- Repository structure (monorepo vs. polyrepo, directory layout)
- Application boilerplate code (framework setup, starter files)
- Infrastructure as code (Kubernetes manifests, Terraform modules)
- CI/CD pipeline configurations (GitHub Actions workflows, GitLab CI YAML)
- Observability instrumentation (Prometheus metrics, structured logging, OpenTelemetry tracing)
- Security configurations (RBAC, network policies, secrets references)
- Documentation templates (README, runbooks, architecture diagrams, API docs)

**Implementation Examples:**

**Backstage Scaffolder:**
- Cookiecutter/Yeoman-style templates
- Template inputs (service name, tech stack, deployment environment)
- Actions: Create repository, scaffold code, configure CI/CD, register in catalog
- Template composition (base template + mixins)

**Humanitec Resource Packs:**
- Infrastructure abstractions (database, cache, message queue)
- Cloud-agnostic resource definitions
- Automatic provisioning on deployment

**Template Versioning:**
- Version templates (v1.0, v2.0)
- Migration guides when templates evolve
- Deprecation notices for old templates

#### 3. Documentation Hub

**Function:** Centralized, searchable, version-controlled documentation.

**Features:**
- Centralized docs (architecture, tutorials, runbooks, API specs)
- Version-controlled (docs-as-code, Git-backed, PR workflow)
- Search and discovery (full-text search, tagging, categorization)
- Auto-generated docs (API specs from OpenAPI, dependency graphs)
- Metrics (doc views, staleness detection)

**Implementation Examples:**

**Backstage TechDocs:**
- Markdown + MkDocs
- Docs live alongside code in repositories
- Automatic build and publish on commit
- Search across all docs

**GitBook / Confluence Integrations:**
- Embed external docs in portal
- Single pane of glass for all documentation

**Swagger/OpenAPI Integrations:**
- Auto-generate API docs from specs
- Interactive API exploration

#### 4. Workflow Automation

**Function:** Self-service actions for common platform operations.

**Capabilities:**
- Self-service actions (create environment, deploy service, request database access)
- Approval workflows (production access requires manager approval)
- Integration with ticketing (Jira, ServiceNow for non-self-service requests)
- ChatOps integrations (Slack, Microsoft Teams for bot-driven workflows)

**Implementation Examples:**

**Port Self-Service Actions:**
- Define actions in UI
- Trigger via API, portal, or Slack
- Approval steps configurable

**Backstage Custom Plugins:**
- React components for custom actions
- API calls to platform services (Kubernetes API, Terraform Cloud)
- Feedback to user (action status, logs)

**Humanitec Deployment Pipelines:**
- Deploy to environment with one click
- Environment diff before deploy
- Automated rollback on failure

## Platform Orchestration Layer

### Purpose

Manage infrastructure provisioning, environment lifecycle, and deployment automation without exposing raw cloud APIs to developers.

### Core Components

#### 1. Infrastructure Orchestration

**Function:** Multi-cloud resource provisioning with platform-agnostic APIs.

**Capabilities:**
- Multi-cloud resource provisioning (AWS, Azure, GCP, on-prem)
- Kubernetes cluster management (namespaces, RBAC, network policies, resource quotas)
- Resource abstraction (developer requests "database", platform provisions RDS/Cloud SQL/etc.)
- Configuration management (separation of app config vs. infrastructure config)

**Implementation Examples:**

**Crossplane:**
- Universal control plane for Kubernetes
- Providers for clouds (AWS, Azure, GCP), services (GitHub, Datadog)
- Compositions: Reusable infrastructure abstractions
- Kubernetes-native (CRDs, controllers)

**Humanitec Platform Orchestrator:**
- Resource management (databases, caches, message queues)
- Resource matching (dev uses in-cluster Postgres, prod uses managed RDS)
- Live Resource Graph: Single source of truth for all resources

**Terraform Cloud:**
- Workspace orchestration (separate state per environment/service)
- Remote execution (consistent environment, audit trail)
- Policy as code (Sentinel policies for compliance)

**Pulumi Automation API:**
- Programmatic infrastructure management
- Multi-language support (TypeScript, Python, Go)
- State management and diffs

#### 2. Environment Management

**Function:** Standardized environments with automated provisioning and promotion pipelines.

**Environment Types:**
- Development: Developer-owned, permissive policies, frequent deployments, auto-cleanup
- Staging: Pre-production testing, production-like configuration, automated integration tests
- Production: Strict policies, approval workflows, automated rollback, immutable infrastructure

**Capabilities:**
- Ephemeral environments (per-PR preview deployments, on-demand test environments)
- Environment promotion pipelines (dev → staging → prod, automated or manual)
- Configuration drift detection (compare actual vs. desired state)
- Configuration drift remediation (auto-fix or alert)

**Implementation Examples:**

**Humanitec Environment Manager:**
- Environment types with inheritance (base config + overrides)
- Automatic environment creation
- Environment diff (see what changes between dev and prod)

**Kubernetes Namespaces + GitOps:**
- Namespace per environment
- Argo CD ApplicationSets (template environments)
- Kustomize overlays (base + environment-specific overrides)

**Cloud Provider Environments:**
- AWS Environments (isolated accounts)
- Azure Management Groups (hierarchy of subscriptions)
- GCP Folders (project organization)

#### 3. Deployment Automation

**Function:** GitOps-based continuous delivery with progressive deployment strategies.

**Principles:**
- GitOps-based continuous delivery (Git as source of truth)
- Progressive delivery (canary, blue-green, rolling updates)
- Deployment policies (require approval, automated testing, gradual rollout)
- Rollback capabilities (automated on failure, manual trigger, retain last N versions)

**Implementation Examples:**

**Argo CD:**
- GitOps for Kubernetes (declarative desired state in Git)
- Multi-cluster application management
- ApplicationSets for templated deployments
- Sync waves for ordered rollouts
- Health assessment (check app is actually working, not just deployed)

**Flux:**
- Toolkit approach (composable controllers)
- Image automation (auto-update image tags in Git)
- Notification system (alerts to Slack, GitHub, etc.)

**Humanitec Deployment Pipelines:**
- Environment-aware deployments
- Approval gates (manual approval before prod)
- Automated testing integration (deploy → run tests → promote)

**Spinnaker:**
- Advanced deployment strategies (canary analysis, blue-green, rolling)
- Multi-cloud support
- Pipeline as code (JSON/YAML)

## Integration Layer

### Purpose

Connect developer portal with underlying infrastructure, CI/CD, observability, security, and FinOps tools.

### Core Components

#### 1. API Gateway / Abstraction Layer

**Function:** Unified API for platform capabilities with authentication and rate limiting.

**Features:**
- Unified API for platform capabilities (abstract underlying tool complexity)
- Authentication and authorization (SSO integration, RBAC, API keys)
- Rate limiting and quotas (prevent abuse, fair usage)
- API versioning and deprecation (backward compatibility, migration paths)

**Implementation Examples:**

**Kubernetes API Server:**
- Platform-native for Kubernetes resources
- RBAC for fine-grained permissions
- Admission controllers for policy enforcement

**Backstage Backend API:**
- REST API for catalog, scaffolder, auth
- Plugin backend APIs

**Custom API Gateways:**
- Kong, Tyk, AWS API Gateway
- Aggregate multiple backends
- Transform requests/responses

#### 2. CI/CD Integration

**Function:** Pipeline visibility and control from developer portal.

**Features:**
- Pipeline status visibility (in-progress, failed, succeeded)
- Trigger builds/deployments from portal
- Artifact management (container registry, package repositories)
- Test results and quality gates (unit tests, integration tests, security scans)

**Implementation Examples:**

**Backstage CI/CD Plugins:**
- GitHub Actions plugin (show workflow runs)
- GitLab CI plugin (pipeline status)
- Jenkins plugin (job history)
- CircleCI plugin

**Argo Workflows:**
- Kubernetes-native CI
- DAG-based workflows
- Artifact passing between steps

**Tekton:**
- Cloud-native CI/CD (Kubernetes CRDs)
- Reusable tasks and pipelines

#### 3. Observability Integration

**Function:** Metrics, logs, and traces surfaced in developer portal.

**Features:**
- Metrics dashboards in portal (per-service, per-team, per-environment)
- Log aggregation and search (centralized logging, grep/filter)
- Distributed tracing (request path visualization, latency breakdown)
- Alerting and on-call management (PagerDuty, Opsgenie integration)

**Implementation Examples:**

**Backstage Prometheus/Grafana Plugins:**
- Embed Grafana dashboards
- Show Prometheus metrics per service

**Commercial Observability:**
- Datadog plugin (APM, logs, metrics in one place)
- New Relic plugin
- Splunk integration

**OpenTelemetry:**
- Standard instrumentation across languages
- Vendor-agnostic telemetry collection
- Automatic instrumentation in golden paths

#### 4. Security Integration

**Function:** Vulnerability scanning, policy enforcement, secrets management.

**Features:**
- Vulnerability scanning (container images, dependencies, IaC)
- Policy enforcement (OPA, Kyverno for Kubernetes)
- Secrets management (Vault integration, encrypted configs, rotation)
- Compliance reporting (SOC2, GDPR, HIPAA dashboards)

**Implementation Examples:**

**Backstage Security Insights Plugins:**
- Show vulnerability scan results
- Dependency security scores
- Compliance status per service

**Scanning Tools:**
- Snyk (container and dependency scanning)
- Trivy (comprehensive vulnerability scanner)
- Aqua, Twistlock (runtime security)

**Policy Engines:**
- OPA Gatekeeper (Kubernetes admission control)
- Kyverno (policy as Kubernetes resources)
- Cloud Custodian (cloud resource policies)

**Secrets Management:**
- HashiCorp Vault (dynamic secrets, encryption as a service)
- AWS Secrets Manager, Azure Key Vault, GCP Secret Manager
- External Secrets Operator (sync cloud secrets to Kubernetes)

#### 5. FinOps Integration

**Function:** Cost visibility, budgets, and optimization recommendations.

**Features:**
- Cost visibility (per-service, per-team, per-environment, per-deployment)
- Budget alerts (spending thresholds, trend analysis)
- Right-sizing recommendations (over-provisioned resources, unused resources)
- Resource lifecycle management (auto-delete unused resources, hibernation)

**Implementation Examples:**

**Backstage Cost Insights Plugin:**
- Show cost per service
- Compare cost across teams
- Trend analysis

**Cloud Provider Cost Tools:**
- AWS Cost Explorer (detailed cost breakdown)
- Azure Cost Management (budgets, recommendations)
- GCP Cost Management (cost attribution, forecasting)

**Kubernetes Cost Tools:**
- Kubecost (cost allocation per namespace, pod, label)
- OpenCost (open-source Kubernetes cost monitoring)

**Infrastructure Cost Estimation:**
- Infracost (IaC cost estimation before deployment)
- Terraform cost estimation modules

## Reference Architecture Diagrams

### Full-Stack IDP Architecture (Backstage + Crossplane + Argo CD)

```
┌─────────────────────────────────────────────────────────────────┐
│                        Developer Portal (Backstage)             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Service    │  │   Software   │  │  TechDocs    │          │
│  │   Catalog    │  │   Templates  │  │  (Markdown)  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   CI/CD      │  │ Observability│  │  Cost        │          │
│  │   Status     │  │  Dashboards  │  │  Insights    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                            ↓ API Calls
┌─────────────────────────────────────────────────────────────────┐
│                     Kubernetes Clusters                          │
│  ┌─────────────────────────────────────────────────────┐        │
│  │  Crossplane (Infrastructure Orchestration)          │        │
│  │  - Providers: AWS, Azure, GCP                       │        │
│  │  - Compositions: Reusable resource abstractions     │        │
│  └─────────────────────────────────────────────────────┘        │
│  ┌─────────────────────────────────────────────────────┐        │
│  │  Argo CD (GitOps Continuous Delivery)              │        │
│  │  - Sync Git → Cluster                               │        │
│  │  - ApplicationSets for multi-env                    │        │
│  └─────────────────────────────────────────────────────┘        │
│  ┌─────────────────────────────────────────────────────┐        │
│  │  Application Workloads                              │        │
│  │  - Deployments, Services, Ingresses                 │        │
│  └─────────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                     Cloud Providers                              │
│  AWS (RDS, S3, EKS)  │  Azure (CosmosDB, AKS)  │  GCP (GKE)     │
└─────────────────────────────────────────────────────────────────┘
```

### Hybrid Architecture (Backstage + Humanitec)

```
┌─────────────────────────────────────────────────────────────────┐
│             Developer Portal (Backstage or Port)                │
│  - Service Catalog    - Documentation    - Self-Service UI     │
└─────────────────────────────────────────────────────────────────┘
                            ↓ API
┌─────────────────────────────────────────────────────────────────┐
│             Platform Orchestrator (Humanitec)                   │
│  ┌─────────────────────────────────────────────────────┐        │
│  │  Live Resource Graph (Single Source of Truth)      │        │
│  │  - Applications, Resources, Dependencies            │        │
│  └─────────────────────────────────────────────────────┘        │
│  ┌─────────────────────────────────────────────────────┐        │
│  │  Resource Management                                │        │
│  │  - Resource Definitions (databases, caches, etc.)   │        │
│  │  - Resource Matching (dev vs. prod resources)       │        │
│  └─────────────────────────────────────────────────────┘        │
│  ┌─────────────────────────────────────────────────────┐        │
│  │  Deployment Pipelines                               │        │
│  │  - Environment orchestration                        │        │
│  │  - Approval workflows                               │        │
│  └─────────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│     Infrastructure Provisioning (Terraform, Crossplane)         │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow: Developer Creates New Service

```
1. Developer opens Backstage portal
   ↓
2. Selects "Create Component" → chooses template (e.g., "Node.js API")
   ↓
3. Fills in template parameters (service name, team, database type)
   ↓
4. Backstage Scaffolder executes template actions:
   a. Create Git repository (GitHub/GitLab API)
   b. Scaffold code (Cookiecutter template)
   c. Add CI/CD pipeline (GitHub Actions workflow file)
   d. Register in service catalog (catalog-info.yaml)
   ↓
5. Developer pushes first commit
   ↓
6. CI/CD pipeline triggers:
   a. Build container image
   b. Security scan (Trivy)
   c. Push to container registry
   ↓
7. Developer creates deployment via portal:
   a. Selects environment (dev, staging, prod)
   b. Crossplane provisions infrastructure (database, cache)
   c. Argo CD syncs application manifests to cluster
   ↓
8. Service is deployed and visible in:
   - Service catalog (ownership, dependencies)
   - Observability dashboards (metrics, logs)
   - Cost insights (resource costs)
```

## Best Practices

### Portal Design

**Navigation:**
- Clear information architecture (catalog, docs, create, admin)
- Search as primary navigation (developers know what they want)
- Personalization (show my services, my team's services)

**Performance:**
- Fast load times (<3s for catalog page)
- Pagination for large catalogs (100 services per page)
- Caching for frequently accessed data

**Accessibility:**
- Keyboard navigation
- Screen reader support
- High contrast mode

### Orchestration Layer

**Resource Abstraction:**
- Platform-agnostic APIs (request "database", not "RDS instance")
- Environment-aware resource matching (dev: in-cluster Postgres, prod: managed RDS)
- Cost-aware defaults (right-size by default, allow overrides)

**Idempotency:**
- Infrastructure operations should be idempotent
- Retry-safe (multiple applies don't create duplicates)
- Rollback-safe (can undo without side effects)

### Integration Layer

**API Design:**
- Versioned APIs (v1, v2 with deprecation notices)
- Pagination for list endpoints
- Filtering and sorting
- Clear error messages

**Monitoring:**
- Instrument all integrations (metrics for API calls, latency, errors)
- Circuit breakers (fail fast if backend is down)
- Timeouts (don't wait forever for slow backends)
