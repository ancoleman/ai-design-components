# Claude Code Commands

This directory contains slash commands for Claude Code that provide guided workflows for AI Design Components.

## The Skillchain Command (v3.0)

The `/skillchain:start` command is the **recommended entry point** for using AI Design Components. Instead of relying on prompt formulation to trigger individual skills, skillchain provides a guided, step-by-step workflow.

### Why Use Skillchain?

| Traditional Approach | Skillchain Approach |
|---------------------|---------------------|
| User must know skill names | Describe what you want to build |
| User triggers skills individually | Skills chain automatically |
| Easy to miss required skills | Correct skill order enforced |
| No theming consistency | Theming always applied first |
| Manual component assembly | Assembly skill runs at end |

**Example:**

Traditional (requires knowledge):
```
"Use the theming-components skill, then designing-layouts,
then creating-dashboards, then visualizing-data..."
```

Skillchain (just describe your goal):
```
/skillchain:start sales dashboard with revenue charts
```

## Installation

### Option 1: Global Installation (Recommended)

Install once, use in all your projects:

```bash
./install.sh
```

This installs to `~/.claude/commands/skillchain/` and `~/.claude/skillchain-data/`, making the commands available in **every project** you work on.

### Option 2: Project-Specific Installation

Install for a single project (can be committed and shared with team):

```bash
# Install to current directory
./install.sh --project

# Or install to a specific project
./install.sh --project ~/path/to/your/project
```

This installs to `<project>/.claude/commands/skillchain/`, making it available only in that project.

## Installation Locations

Claude Code looks for commands in two locations:

| Location | Scope | Use Case |
|----------|-------|----------|
| `~/.claude/commands/` | Global (your user) | Personal commands available everywhere |
| `.claude/commands/` | Project-specific | Team commands committed to repo |

**Resolution order:** Project commands override global commands if both exist.

## Usage

After installation, start Claude Code in any project:

```bash
claude
```

Then use the skillchain command:

```
/skillchain:start help                           # Show all 76 available skills
/skillchain:start dashboard with charts          # Build a dashboard
/skillchain:start CI/CD pipeline                 # Build CI/CD workflow
/skillchain:start Kubernetes deployment          # Build K8s infrastructure
/skillchain:start SOC2 compliance                # Implement security compliance
/skillchain:start RAG pipeline with embeddings   # Build AI data pipeline
/skillchain:start deploy to AWS                  # Cloud deployment
```

### How It Works

1. **Parse Goal** - Skillchain analyzes keywords in your description
2. **Detect Domain(s)** - Routes to one of 10 domain orchestrators (or fullstack/multi-domain)
3. **Match Blueprint** - Checks for pre-configured patterns (12 available)
4. **Order Skills** - Ensures correct execution order with dependency resolution
5. **Load Preferences** - Applies saved preferences from previous sessions
6. **Guide Configuration** - Asks questions for each skill (or uses defaults)
7. **Parallel Loading** - Invokes independent skills concurrently
8. **Generate Code** - Produces themed, accessible components
9. **Save Preferences** - Optionally saves choices for next time

---

## v3.0 Features

### 10 Domains, 76 Skills

v3.0 expands from 2 domains (frontend/backend) to **10 comprehensive domains**:

| Domain | Skills | Focus |
|--------|--------|-------|
| Frontend | 15 | UI components, forms, charts, dashboards |
| Backend | 14 | APIs, databases, messaging, deployment |
| DevOps | 6 | CI/CD, Docker, GitOps, incidents |
| Infrastructure | 12 | Kubernetes, Terraform, networking |
| Security | 7 | Compliance, TLS, firewalls, SIEM |
| Developer | 7 | APIs, CLIs, SDKs, documentation |
| Data | 6 | ETL, streaming, SQL optimization |
| AI/ML | 4 | MLOps, prompts, LLM evaluation |
| Cloud | 3 | AWS, GCP, Azure deployments |
| FinOps | 2 | Cost optimization, tagging |

### 12 Blueprints

Pre-configured skill chains for common patterns:

| Blueprint | Category | Description |
|-----------|----------|-------------|
| dashboard | Frontend | Analytics dashboard with charts & KPIs |
| crud-api | Backend | REST API with database & auth |
| api-first | Developer | API-first design with OpenAPI |
| rag-pipeline | AI/ML | RAG with vector search & embeddings |
| ml-pipeline | AI/ML | MLOps pipeline with training & serving |
| ci-cd | DevOps | CI/CD with testing & deployment |
| k8s | Infrastructure | Kubernetes deployment with Helm |
| cloud | Cloud | Multi-cloud deployment patterns |
| observability | DevOps | Monitoring, logging, tracing stack |
| security | Security | Security architecture & compliance |
| cost | FinOps | Cost optimization strategy |
| data-pipeline | Data | ETL/ELT data processing pipeline |

### User Preferences System

Skillchain remembers your choices between sessions:

```yaml
# Saved to ~/.claude/skillchain-prefs.yaml
global:
  theme:
    color_scheme: "blue-gray"
    theme_modes: ["light", "dark"]
  frameworks:
    frontend: "react"
    backend: "fastapi"
```

**How it works:**
- First run: Answer questions, offered to save preferences
- Future runs: Your saved preferences become smart defaults
- Override anytime: Just provide a different answer

### Skill Versioning

All 76 skills are versioned for compatibility tracking:

```yaml
# In registries/*.yaml
visualizing-data:
  version: "1.0.0"
  # ...
```

### Parallel Skill Loading

Independent skills are loaded concurrently for faster workflows:

```
# Instead of sequential:
Step 1: theming-components
Step 2: designing-layouts
Step 3: visualizing-data   # waits for layouts
Step 4: building-tables    # waits for viz

# Parallel loading:
Step 1: theming-components
Step 2: designing-layouts
Step 3 (PARALLEL): visualizing-data + building-tables
```

---

## Architecture (v3.0)

Skillchain uses a **separated structure** to prevent internal files from appearing as commands:

```
~/.claude/
├── commands/
│   └── skillchain/                    # Commands (exposed as /skillchain:*)
│       ├── start.md                   # /skillchain:start (main entry)
│       ├── help.md                    # /skillchain:help
│       ├── blueprints/                # /skillchain:blueprints:*
│       │   ├── dashboard.md
│       │   ├── crud-api.md
│       │   ├── rag-pipeline.md
│       │   └── ... (12 total)
│       └── categories/                # /skillchain:categories:*
│           ├── frontend.md
│           ├── backend.md
│           ├── devops.md
│           ├── infrastructure.md
│           ├── security.md
│           ├── developer.md
│           ├── data.md
│           ├── ai-ml.md
│           ├── cloud.md
│           ├── finops.md
│           ├── fullstack.md
│           └── multi-domain.md
│
└── skillchain-data/                   # Data (NOT exposed as commands)
    ├── registries/
    │   ├── _index.yaml
    │   ├── frontend.yaml
    │   ├── backend.yaml
    │   └── ... (10 domain registries)
    └── shared/
        ├── preferences.md
        ├── theming-rules.md
        └── execution-flow.md
```

### Command Pattern

Skillchain exposes a hierarchical command structure:

| Command | Description |
|---------|-------------|
| `/skillchain:start [goal]` | Main guided workflow |
| `/skillchain:help` | Show help and 76 skills |
| `/skillchain:blueprints:dashboard` | Direct dashboard blueprint |
| `/skillchain:blueprints:rag-pipeline` | Direct RAG pipeline blueprint |
| `/skillchain:categories:frontend` | Frontend orchestrator |
| `/skillchain:categories:devops` | DevOps orchestrator |

### Dynamic Path Discovery

Skillchain works from any project by dynamically finding its installation location:

```bash
# Commands directory
if [ -d ".claude/commands/skillchain" ]; then
  SKILLCHAIN_CMD="$(pwd)/.claude/commands/skillchain"
elif [ -d "$HOME/.claude/commands/skillchain" ]; then
  SKILLCHAIN_CMD="$HOME/.claude/commands/skillchain"
fi

# Data directory (separate from commands)
if [ -d ".claude/skillchain-data" ]; then
  SKILLCHAIN_DATA="$(pwd)/.claude/skillchain-data"
elif [ -d "$HOME/.claude/skillchain-data" ]; then
  SKILLCHAIN_DATA="$HOME/.claude/skillchain-data"
fi
```

All file references use `{SKILLCHAIN_CMD}/...` and `{SKILLCHAIN_DATA}/...` patterns for portability.

---

## Skill Categories

### Frontend Skills (15)

| Skill | Group | Description |
|-------|-------|-------------|
| theming-components | foundation | Design tokens, colors, dark mode |
| designing-layouts | structure | Grid systems, responsive design |
| implementing-navigation | structure | Menus, tabs, routing |
| visualizing-data | data-display | Charts, graphs, plots |
| building-tables | data-display | Data grids, pagination |
| creating-dashboards | data-display | KPI cards, widgets |
| building-forms | user-input | Inputs, validation |
| implementing-search-filter | user-input | Search, faceted filters |
| building-ai-chat | interaction | Chat UI, streaming |
| implementing-drag-drop | interaction | Sortable, kanban |
| providing-feedback | interaction | Toasts, alerts, loading |
| displaying-timelines | structure | Activity feeds, history |
| managing-media | content | File upload, galleries |
| guiding-users | content | Onboarding, tooltips |
| assembling-components | assembly | Final integration |

### Backend Skills (14)

| Skill | Group | Description |
|-------|-------|-------------|
| ingesting-data | data-ingestion | ETL, CSV, S3 imports |
| using-relational-databases | databases | Postgres, MySQL, SQLite |
| using-vector-databases | databases | Qdrant, pgvector, Pinecone |
| using-timeseries-databases | databases | ClickHouse, InfluxDB |
| using-document-databases | databases | MongoDB, DynamoDB |
| using-graph-databases | databases | Neo4j, knowledge graphs |
| implementing-api-patterns | apis | REST, GraphQL, gRPC |
| using-message-queues | messaging | Kafka, RabbitMQ, Celery |
| implementing-realtime-sync | messaging | WebSocket, SSE, CRDTs |
| securing-authentication | platform | JWT, OAuth, RBAC |
| implementing-observability | platform | OpenTelemetry, logging |
| deploying-applications | platform | Kubernetes, serverless |
| ai-data-engineering | ai-ml | RAG pipelines, chunking |
| model-serving | ai-ml | vLLM, Ollama, inference |

### DevOps Skills (6)

| Skill | Group | Description |
|-------|-------|-------------|
| writing-dockerfiles | containers | Multi-stage builds, optimization |
| testing-strategies | quality | Unit, integration, e2e tests |
| building-ci-pipelines | automation | GitHub Actions, Jenkins |
| implementing-gitops | deployment | ArgoCD, Flux workflows |
| managing-incidents | reliability | On-call, postmortems, runbooks |
| platform-engineering | platform | IDP, Backstage, developer portals |

### Infrastructure Skills (12)

| Skill | Group | Description |
|-------|-------|-------------|
| operating-kubernetes | orchestration | kubectl, Helm, deployments |
| writing-infrastructure-code | iac | Terraform, Pulumi, Ansible |
| managing-configuration | config | Ansible, Chef, Puppet |
| architecting-networks | networking | VPC, subnets, routing |
| load-balancing-patterns | networking | ALB, NLB, HAProxy |
| managing-dns | networking | Route53, BIND, DNS records |
| implementing-service-mesh | networking | Istio, Linkerd, Consul |
| administering-linux | systems | Ubuntu, RHEL, systemd |
| configuring-nginx | systems | Reverse proxy, SSL |
| shell-scripting | systems | Bash, automation |
| planning-disaster-recovery | reliability | DR, backup, failover |
| designing-distributed-systems | reliability | Microservices, consensus |

### Security Skills (7)

| Skill | Group | Description |
|-------|-------|-------------|
| architecting-security | architecture | Zero trust, threat modeling |
| implementing-compliance | compliance | SOC2, HIPAA, GDPR, PCI |
| managing-vulnerabilities | operations | CVE scanning, patching |
| implementing-tls | encryption | Certificates, mTLS |
| configuring-firewalls | network | iptables, security groups |
| siem-logging | monitoring | Security logging, Splunk |
| security-hardening | hardening | CIS benchmarks, least privilege |

### Developer Productivity Skills (7)

| Skill | Group | Description |
|-------|-------|-------------|
| designing-apis | api | REST, GraphQL, OpenAPI |
| building-clis | tools | Click, Typer, Cobra |
| designing-sdks | tools | Client libraries, wrappers |
| generating-documentation | docs | Sphinx, MkDocs, JSDoc |
| debugging-techniques | debugging | pdb, gdb, DevTools |
| managing-git-workflows | vcs | Branching, rebasing, PRs |
| writing-github-actions | automation | Workflows, actions |

### Data Engineering Skills (6)

| Skill | Group | Description |
|-------|-------|-------------|
| architecting-data | architecture | Data warehouse, lake, schema |
| streaming-data | streaming | Kafka, Kinesis, real-time |
| transforming-data | etl | dbt, Airflow, pipelines |
| optimizing-sql | performance | Query optimization, indexes |
| secret-management | security | Vault, AWS Secrets Manager |
| performance-engineering | optimization | Profiling, benchmarking |

### AI/ML Skills (4)

| Skill | Group | Description |
|-------|-------|-------------|
| implementing-mlops | mlops | MLflow, Kubeflow, monitoring |
| prompt-engineering | prompts | Few-shot, chain of thought |
| evaluating-llms | evaluation | Benchmarks, evals |
| embedding-optimization | vectors | Vector search, similarity |

### Cloud Provider Skills (3)

| Skill | Group | Description |
|-------|-------|-------------|
| deploying-on-aws | aws | Lambda, S3, EC2, ECS |
| deploying-on-gcp | gcp | Cloud Run, Cloud Functions |
| deploying-on-azure | azure | Azure Functions, AKS |

### FinOps Skills (2)

| Skill | Group | Description |
|-------|-------|-------------|
| optimizing-costs | cost | Right-sizing, reserved instances |
| resource-tagging | governance | Tag strategy, cost allocation |

---

## Workflow Commands

During a skillchain session, you can use:

| Command | Action |
|---------|--------|
| `back` | Return to previous skill |
| `skip` | Use defaults for current question |
| `status` | Show current progress |
| `done` | Finish early with current selections |
| `restart` | Start over from beginning |
| `help` | Show workflow commands |

---

## Files

```
.claude-commands/
├── skillchain/                  # Commands (26 files)
│   ├── start.md                 # Main router
│   ├── help.md                  # Help content
│   ├── blueprints/              # 12 blueprint templates
│   └── categories/              # 12 category orchestrators
├── skillchain-data/             # Data (not exposed as commands)
│   ├── registries/              # 11 registry files
│   └── shared/                  # Shared resources
└── README.md                    # This documentation
```

## Updating

To update an existing installation, run the installer again:

```bash
# Update global installation
./install.sh

# Update project installation
./install.sh --project ~/your-project
```

The installer will detect and update existing installations.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v3.0.0 | 2025-12-08 | 10 domains, 76 skills, 12 blueprints, separated data directory |
| v2.1.0 | 2025-12-02 | User preferences, skill versioning, parallel loading |
| v2.0.0 | 2025-12-02 | Modular architecture, blueprints, dynamic paths |
| v1.0.0 | 2025-12-01 | Initial monolithic release |

See `skillchain-data/shared/changelog.md` for detailed version history.
