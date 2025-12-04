# Skill Master Plans

> 47 comprehensive init.md master plans ready for SKILL.md implementation

## Overview

Master plans are comprehensive `init.md` files that contain research, decision frameworks, and implementation roadmaps for each skill. These serve as the foundation for creating production-ready `SKILL.md` files.

Each master plan includes:
- Strategic positioning and market context
- Component taxonomy and categorization
- Decision frameworks with actionable guidance
- Tool/library recommendations with research backing
- Multi-language code examples (where applicable)
- Integration points with other skills
- Implementation roadmap

## Skills by Category

### Infrastructure & Networking (12 skills)

| Skill | Description | Multi-Lang |
|-------|-------------|------------|
| `infrastructure-as-code` | Terraform, Pulumi, CDK patterns | |
| `kubernetes-operations` | K8s management, Helm, operators | |
| `designing-distributed-systems` | CAP theorem, architecture patterns | |
| `configuration-management` | Ansible, Chef, Puppet | |
| `network-architecture` | VPC design, subnets, routing | |
| `load-balancing-patterns` | ALB, NLB, service mesh LB | |
| `dns-management` | Route53, CloudDNS, record types | |
| `service-mesh` | Istio, Linkerd, Cilium | |
| `disaster-recovery` | RPO/RTO, backup strategies | |
| `linux-administration` | System management, troubleshooting | |
| `shell-scripting` | Bash/Zsh patterns | |
| `configuring-nginx` | Reverse proxy, SSL, performance | |

### Security (6 skills)

| Skill | Description | Multi-Lang |
|-------|-------------|------------|
| `security-architecture` | Zero trust, defense in depth | |
| `compliance-frameworks` | SOC2, ISO27001, HIPAA, PCI-DSS | |
| `vulnerability-management` | Scanning, remediation workflows | |
| `siem-logging` | Security monitoring, alerting | |
| `implementing-tls` | Certificate management, mTLS | |
| `configuring-firewalls` | Network security rules | |

### Developer Productivity (7 skills)

| Skill | Description | Multi-Lang |
|-------|-------------|------------|
| `api-design-principles` | REST, GraphQL design patterns | |
| `building-clis` | Python, Go, Rust CLI frameworks | TS/Py/Go/Rust |
| `sdk-design` | Client library patterns | TS/Py/Go |
| `documentation-generation` | API docs, code documentation | |
| `debugging-techniques` | Profiling, troubleshooting | Py/Go/Rust |
| `git-workflows` | Branching strategies, hooks | |
| `writing-github-actions` | CI/CD workflow authoring | |

### DevOps & Platform (6 skills)

| Skill | Description | Multi-Lang |
|-------|-------------|------------|
| `building-ci-pipelines` | GitHub Actions, GitLab CI, Jenkins | |
| `gitops-workflows` | ArgoCD, Flux patterns | |
| `testing-strategies` | Unit, integration, E2E testing | TS/Py/Go/Rust |
| `platform-engineering` | IDP, Backstage, developer experience | |
| `incident-management` | On-call, post-mortems, SRE | |
| `writing-dockerfiles` | Multi-stage, security hardening | |

### Data & Analytics (6 skills)

| Skill | Description | Multi-Lang |
|-------|-------------|------------|
| `data-architecture` | Data mesh, lakehouse, medallion | |
| `streaming-data` | Kafka, Flink, event streaming | TS/Py/Go/Java |
| `data-transformation` | dbt, ETL/ELT patterns | Py/SQL/Spark |
| `sql-optimization` | Query tuning, indexing | PG/MySQL/MSSQL |
| `secret-management` | Vault, secrets rotation | |
| `performance-engineering` | Profiling, optimization | |

### AI/ML Operations (4 skills)

| Skill | Description | Multi-Lang |
|-------|-------------|------------|
| `mlops-patterns` | MLflow, experiment tracking, feature stores | |
| `prompt-engineering` | LLM prompting, chain-of-thought | Py/TS |
| `llm-evaluation` | RAGAS, benchmarks, safety testing | Py/TS |
| `embedding-optimization` | Chunking strategies, model selection | |

### Cloud Patterns (3 skills)

| Skill | Description | Multi-Lang |
|-------|-------------|------------|
| `aws-patterns` | Well-Architected, service selection | |
| `gcp-patterns` | BigQuery, Vertex AI, GKE | |
| `azure-patterns` | Container Apps, Azure OpenAI | |

### FinOps (3 skills)

| Skill | Description | Multi-Lang |
|-------|-------------|------------|
| `cost-optimization` | FinOps practices, rightsizing | |
| `resource-tagging` | Tag governance, enforcement | |
| `security-hardening` | CIS benchmarks, hardening | |

## Research Methodology

All master plans include research from:
- **Google Search Grounding** - 2025 best practices and trends
- **Context7** - Library trust scores and documentation
- Decision frameworks with actionable guidance
- Production-ready tool recommendations

## Next Steps

These master plans are ready for SKILL.md implementation following Anthropic's 6-step process:

1. Create SKILL.md files (progressive disclosure, <500 lines)
2. Build reference documentation in `references/`
3. Create working code examples in `examples/`
4. Develop utility scripts in `scripts/` (token-free execution)
5. Test across models (Haiku, Sonnet, Opus)

See [SKILL_ORCHESTRATION_PLAN.md](./SKILL_ORCHESTRATION_PLAN.md) for the execution strategy.
