---
slug: skillchain-v3.0
title: "Skillchain v3.0: 76 Skills, 10 Domains, Separated Architecture"
authors: [ancoleman]
tags: [release, skillchain, features, automation, v3.0]
---

# Skillchain v3.0: 76 Skills Across 10 Domains

Skillchain v3.0 represents a major milestone with complete coverage across all development domains. This release brings 76 production-ready skills, 12 category orchestrators, and a cleaner separated architecture.

<!-- truncate -->

## What's New in v3.0

### 76 Production-Ready Skills

We've grown from 29 skills in v2.1 to **76 complete skills** covering every aspect of modern software development:

| Domain | Skills | Examples |
|--------|--------|----------|
| Frontend | 15 | theming-components, visualizing-data, building-ai-chat |
| Backend | 14 | api-patterns, databases-relational, auth-security |
| DevOps | 6 | testing-strategies, building-ci-pipelines, implementing-gitops |
| Infrastructure | 12 | operating-kubernetes, writing-infrastructure-code, configuring-nginx |
| Security | 7 | architecting-security, implementing-compliance, implementing-tls |
| Developer Productivity | 7 | designing-apis, building-clis, debugging-techniques |
| Data Engineering | 6 | architecting-data, streaming-data, optimizing-sql |
| AI/ML | 4 | implementing-mlops, prompt-engineering, evaluating-llms |
| Cloud | 3 | deploying-on-aws, deploying-on-gcp, deploying-on-azure |
| FinOps | 2 | optimizing-costs, resource-tagging |

### 12 Category Orchestrators

Each domain has its own specialized orchestrator, plus cross-domain handlers:

**Single-Domain Orchestrators (10):**
- frontend.md - React, Vue, Svelte, component libraries
- backend.md - APIs, databases, authentication
- devops.md - CI/CD, testing, GitOps
- infrastructure.md - Kubernetes, IaC, networking
- security.md - Security architecture, compliance, hardening
- developer.md - API design, CLIs, SDKs
- data.md - Data pipelines, warehouses, streaming
- ai-ml.md - MLOps, prompt engineering, evaluation
- cloud.md - AWS, GCP, Azure patterns
- finops.md - Cost optimization, tagging strategies

**Cross-Domain Orchestrators (2):**
- fullstack.md - Coordinates frontend + backend skills
- multi-domain.md - Handles complex cross-cutting requests

### 12 Blueprints for Common Patterns

Pre-configured skill chains for rapid development:

```bash
# Infrastructure & Security
/skillchain:start k8s-deployment
/skillchain:start ci-cd-pipeline
/skillchain:start security-hardened-api

# Data & Analytics
/skillchain:start data-pipeline
/skillchain:start ml-pipeline
/skillchain:start dashboard

# Cloud & Operations
/skillchain:start cloud-native-app
/skillchain:start observability-stack
/skillchain:start cost-optimized-infra
```

### Separated Directory Architecture

v3.0 introduces a cleaner separation between commands and data:

```
~/.claude/
├── commands/
│   └── skillchain/           # Exposed as /skillchain:* commands
│       ├── start.md          # /skillchain:start
│       ├── help.md           # /skillchain:help
│       ├── blueprints/       # /skillchain:blueprints:*
│       └── categories/       # /skillchain:categories:*
│
└── skillchain-data/          # NOT exposed as commands
    ├── registries/           # 10 domain-specific YAML registries
    └── shared/               # Common resources
```

**Benefits:**
- Cleaner command namespace (no `/_registry` clutter)
- Faster command discovery
- Better organization of data files
- Easier to maintain and extend

### New Command Pattern

The main command is now `/skillchain:start` instead of `/skillchain`:

```bash
# New pattern (v3.0)
/skillchain:start dashboard with charts
/skillchain:start REST API with postgres
/skillchain:start kubernetes deployment

# Help and documentation
/skillchain:help

# Direct blueprint access
/skillchain:blueprints:dashboard
/skillchain:blueprints:ci-cd

# Direct category access
/skillchain:categories:frontend
/skillchain:categories:backend
```

## Domain Highlights

### Infrastructure Skills (12)

Complete infrastructure automation coverage:

- **operating-kubernetes** - Deployments, services, ingress, HPA, operators
- **writing-infrastructure-code** - Terraform, Pulumi, CloudFormation patterns
- **administering-linux** - System administration, systemd, package management
- **architecting-networks** - VPC design, subnets, routing, firewalls
- **load-balancing-patterns** - Layer 4/7, health checks, algorithms
- **planning-disaster-recovery** - Backup strategies, RTO/RPO, failover
- **configuring-nginx** - Reverse proxy, SSL, caching, optimization
- **shell-scripting** - Bash best practices, error handling, portability
- **managing-dns** - Route53, zones, records, DNSSEC
- **implementing-service-mesh** - Istio, Linkerd, mTLS, traffic management
- **managing-configuration** - Config management, environment variables
- **designing-distributed-systems** - CAP theorem, consistency patterns

### Security Skills (7)

Enterprise-grade security patterns:

- **architecting-security** - Zero trust, defense in depth
- **implementing-compliance** - SOC 2, GDPR, HIPAA frameworks
- **managing-vulnerabilities** - CVE management, patching strategies
- **implementing-tls** - Certificate management, mTLS
- **configuring-firewalls** - Network security, segmentation
- **siem-logging** - Log aggregation, alerting, correlation
- **security-hardening** - CIS benchmarks, OS hardening

### AI/ML Skills (4)

Complete AI development lifecycle:

- **implementing-mlops** - Training pipelines, model versioning
- **prompt-engineering** - Chain-of-thought, few-shot, evaluation
- **evaluating-llms** - Benchmarks, quality metrics, A/B testing
- **embedding-optimization** - Chunking strategies, retrieval tuning

## Installation

The interactive installer now prominently features skillchain installation:

```bash
# Clone and run installer
git clone https://github.com/ancoleman/ai-design-components.git
cd ai-design-components
./install.sh
```

**Interactive Menu (v3.0):**
```
What would you like to do?

  1) Full Install - Marketplace + all plugins + /skillchain command
  2) Install Skillchain - Install /skillchain:start command globally
  3) Marketplace + Plugins - Add marketplace + install all plugins
  4) Marketplace Only - Just add the marketplace
  5) Select Plugins - Choose which plugins to install
  6) Uninstall - Remove marketplace and plugins
  7) List Plugins - Show available plugins
  8) Help - Show all commands
```

**Direct Installation:**
```bash
# Install everything
./install.sh
# Select option 1

# Install skillchain only
./install.sh commands
```

## Example Workflows

### Full-Stack Dashboard

```bash
/skillchain:start analytics dashboard with postgres backend
```

Skillchain automatically:
1. Routes to fullstack orchestrator
2. Loads creating-dashboards, visualizing-data, databases-relational
3. Applies theming-components for consistent styling
4. Configures auth-security if needed

### Kubernetes Deployment

```bash
/skillchain:start deploy my app to kubernetes
```

Skillchain automatically:
1. Routes to infrastructure orchestrator
2. Loads operating-kubernetes, writing-infrastructure-code
3. Adds observability and security-hardening
4. Generates complete k8s manifests

### Security-First API

```bash
/skillchain:start secure REST API with OAuth
```

Skillchain automatically:
1. Routes across backend + security domains
2. Loads api-patterns, auth-security, implementing-tls
3. Adds rate limiting, input validation
4. Configures proper CORS and headers

## Upgrade Notes

### From v2.1

If upgrading from v2.1:

1. **Re-run installer**: `./install.sh commands`
2. **Update commands**: Use `/skillchain:start` instead of `/skillchain`
3. **Directory changes**: Data now in `~/.claude/skillchain-data/`
4. **Preferences preserved**: Your saved choices still work

### Breaking Changes

- Command changed from `/skillchain` to `/skillchain:start`
- Directory structure reorganized (commands vs data separated)
- Registry format updated (domain-specific YAML files)

## Performance

- **Skill loading**: ~2-3 seconds (parallel loading)
- **Registry lookup**: under 50ms (domain-specific files)
- **Path discovery**: under 50ms
- **Total startup**: ~3-4 seconds

## What's Next

Future enhancements planned:

- **Skill recommendations** - AI-suggested skill chains based on project context
- **Template library** - Community-contributed blueprints
- **Skill marketplace** - Browse and install community skills
- **Project scaffolding** - Generate complete starter projects
- **Cross-domain intelligence** - Smarter skill combinations

## Resources

- [Skillchain Documentation](/docs/skillchain/overview)
- [Skills Overview](/docs/skills/overview) - All 76 skills
- [Creating Skills](/docs/guides/creating-skills) - Contribute new skills
- [Full Changelog](https://github.com/ancoleman/ai-design-components/blob/main/CHANGELOG.md)
- [GitHub Repository](https://github.com/ancoleman/ai-design-components)

---

**76 skills. 10 domains. One command.**

```bash
/skillchain:start [describe what you're building]
```
