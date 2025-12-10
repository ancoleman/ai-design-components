# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

**Delegated Execution Mode (Solves Context Rot):**
- `delegated.md` - New orchestrator that spawns fresh-context sub-agents per skill
  - Solves context rot problem where long chains (4+ skills) cause 50% activation
  - Each skill executes in isolated Task sub-agent with fresh context
  - Coordinator maintains minimal state, delegates all skill work
  - Supports parallel execution for independent skills
  - Guarantees ~100% skill activation regardless of chain length
- Step 3.7 added to `start.md` for execution mode selection
  - Auto-recommends delegated for 4+ skill chains
  - User can choose standard (single conversation) or delegated (sub-agents)
- `delegated-execution.md` - Documentation explaining the pattern and when to use it

**Dynamic Skill Chain Improvements:**
- `dynamic.md` - Dynamic orchestrator for building custom skill chains without blueprints
- `skill-graph.yaml` - Skill tiers, dependencies, and domain rules for chain building
- `execution-protocol.md` - Mandatory behaviors to guarantee >80% skill activation
- Step 3.6 added to `start.md` for dynamic skill selection option

### Fixed

- Skill invocation mismatches across blueprints and orchestrators (56 corrections)
- CI workflow now uses manual file copy instead of interactive install.sh
- Evaluation threshold adjusted to 80% pass rate

## [0.6.0] - 2025-12-09

### 🎯 MAJOR MILESTONE: Complete Skillchain Validation & Context Architecture

**Strategic Achievement:** Implemented the complete Skillchain Improvement Plan, solving the "58% completeness problem" where generated projects had missing deliverables. This release introduces a comprehensive validation and context-passing architecture that ensures skills produce complete outputs matching blueprint promises.

### Added

**Skill Deliverables Declaration (76 outputs.yaml files):**
Every skill now declares its expected outputs, enabling validation:
- All 76 skills have `outputs.yaml` files specifying:
  - `base_outputs` - Files always generated
  - `conditional_outputs` - Maturity-dependent outputs (starter/intermediate/advanced)
  - `path`, `must_contain`, `content_markers` for validation
- Schema validates against `config/rules.yaml` outputs_yaml section

**Chain Context Architecture:**
- `chain-context-schema.yaml` - Comprehensive state tracking specification
  - Router metadata (blueprint, goal, domains, matched_skills)
  - Orchestrator config (maturity, project_path, skills_sequence)
  - Execution tracking (skill_outputs with files_created, deliverables_contributed)
  - Deliverables validation (status: pending/fulfilled/missing/skipped)
- Context flows: start.md → orchestrator → validation.md → skills

**Skillchain Validation Framework:**
- `validation.md` - Shared validation logic with pseudo-code functions:
  - `validate_chain()` - Full chain validation against blueprint
  - `validate_deliverable()` - Single deliverable check
  - `check_files_exist()` - Glob pattern file checking
  - `run_content_checks()` - Regex content validation
  - `run_basic_completeness_check()` - Fallback when no blueprint
- Step 5.5 added to all 12 category orchestrators (devops, frontend, backend, etc.)
- Step 8 added to start.md for post-generation validation

**Blueprint Deliverables Specification:**
All 12 blueprints updated with concrete validation requirements:
- `## Deliverables Specification` section with YAML definitions
- Each deliverable specifies: `primary_skill`, `required_files`, `content_checks`, `maturity_required`
- `### Maturity Profiles` section with starter/intermediate/advanced configurations
- `skip_deliverables`, `require_additionally`, `empty_dirs_allowed` per maturity level

**Validation Package Extensions (`scripts/validation/`):**
- **New** `blueprints.py` - Blueprint validation engine:
  - `BlueprintValidator` class with YAML extraction from markdown
  - `BlueprintResult` and `BlueprintReport` dataclasses
  - Validates deliverables and maturity profile structure
- **New** CLI command: `python -m scripts.validation blueprints`
  - Single blueprint: `validation blueprints api-first.md`
  - All blueprints: `validation blueprints --verbose`
- **New** outputs.yaml validation integrated into skill validation:
  - `_validate_outputs_yaml()` method in validator.py
  - Checks required fields, output sections, maturity levels
- **New** rule sections in `config/rules.yaml`:
  - `outputs_yaml:` - Schema for skill deliverables files
  - `blueprints:` - Schema for blueprint markdown validation

**Post-Generation Evaluation Tools:**
- `scripts/runtime/completeness_checker.py` - Project validation:
  - Blueprint-based validation with maturity filtering
  - Basic mode for projects without blueprints
  - File existence and content pattern checking
  - 80% completeness threshold with remediation suggestions
- `evaluation/post_gen_evaluate.py` - Comprehensive project scoring:
  - Directory completeness (0-1 score)
  - Runnability checks (poetry, pytest, imports)
  - Blueprint promise fulfillment
  - Sample data availability
  - Documentation coverage
- Updated `evaluation/scenarios.yaml` with post_generation criteria:
  - `expected_directories`, `expected_files`, `blueprint_promises`
  - `runnability_checks` with commands and expected exit codes

**GitHub Actions Updates:**
- Enhanced `validate-skillchain.yml`:
  - Added blueprint YAML validation step
  - Path triggers for `scripts/validation/**` and `scripts/runtime/**`
  - Installs skillchain commands before validation
  - Runs `python -m scripts.validation blueprints --verbose`

**Documentation:**
- `evaluation/README.md` - Complete evaluation tools documentation
- Updated `scripts/validation/README.md` with blueprint validation docs

### Changed

**Skillchain Flow:**
- start.md now creates and passes `chain_context` to orchestrators
- All 12 orchestrators track skill outputs and validate deliverables
- Validation reports show fulfilled/missing/skipped status with completeness %
- Remediation flow offers to generate missing components

**Validation Package:**
- `rules.py` - Added `OutputsYamlRules` and `BlueprintRules` dataclasses
- `validator.py` - Integrated outputs.yaml validation into skill validation
- `__init__.py` - Exports `BlueprintValidator`, `BlueprintResult`, `BlueprintReport`, `BlueprintRules`
- `__main__.py` - Added `blueprints` subcommand

**Evaluation Framework:**
- `scenarios.yaml` - Added Phase 2 post_generation_criteria with 5 metrics
- S11 (ML Pipeline) now has complete post_generation validation spec

### Statistics

- **outputs.yaml files created:** 76 (100% skill coverage)
- **Blueprints updated:** 12 (all with deliverables specs)
- **Orchestrators updated:** 12 (all with Step 5.5)
- **New validation methods:** 5 (in validator.py and blueprints.py)
- **New CLI commands:** 1 (`validation blueprints`)
- **Files in this release:** 116 uncommitted changes

### Architecture Impact

**Before v0.6.0:**
- Skills executed without output tracking
- Blueprints promised features but didn't validate
- 58% average completeness on generated projects
- No remediation path for missing deliverables

**After v0.6.0:**
- Complete chain context tracking from router to validation
- Skills declare expected outputs in outputs.yaml
- Blueprints define concrete deliverables with validation rules
- Maturity-aware validation (skip non-required deliverables)
- Automated completeness checking with 80% threshold
- Remediation flow for missing components

---

## [0.5.2] - 2025-12-08

### Added

**Enhanced Interactive Installer:**
- Reorganized menu with 12 options grouped by action type (Install, Update, Uninstall, Info)
- Option 1: Full Install - Marketplace + all plugins + /skillchain command
- Option 2: Install Skillchain only
- Option 6: Update Skillchain - Refresh to latest version
- Option 7: Update Marketplace - Refresh marketplace plugins
- Option 8: Uninstall Skillchain - Remove commands and data
- Option 10: Uninstall Everything - Complete removal

**Skillchain Management Commands:**
- `./install.sh commands` - Install skillchain globally
- `./install.sh commands update` - Update skillchain to latest version
- `./install.sh commands uninstall` - Remove skillchain commands and data
- `./install.sh uninstall-all` - Remove everything (skillchain + plugins + marketplace)
- Smart install/update detection with appropriate messaging

**New Blog Post:**
- `pages/blog/2025-12-08-skillchain-v3.0.md` - Comprehensive v3.0 announcement covering 76 skills, 10 domains, 12 blueprints

### Changed

**Documentation Updates:**
- Completely rewrote `pages/docs/installation.md` for v3.0 with full installer documentation
- Updated `pages/docs/skillchain/` docs to reflect v3.0 architecture
- Updated all references from `install-skillchain.sh` to `./install.sh`
- Updated all references from `/skillchain` to `/skillchain:start`
- Fixed GitHub issue templates with current installation commands

### Removed

- `.claude-commands/install-skillchain.sh` - Replaced by `./install.sh commands`

## [0.5.1] - 2025-12-08

### Fixed

**Skillchain Command Duplication:**
- Moved `commands/` to `.claude-commands/` to prevent skillchain from appearing under every plugin
- Previously, all 19 plugins had `"source": "./"` which caused each plugin to expose its own `/plugin:skillchain:skillchain` command
- Skillchain now only appears as a user-level command when installed via `./install.sh commands`

### Added

**Skillchain Enhancements (9 New Blueprints):**
- `api-first` - API-first development with OpenAPI-driven workflows
- `ci-cd` - Complete CI/CD pipeline setup with testing and deployment
- `cloud` - Multi-cloud deployment patterns for AWS/GCP/Azure
- `cost` - FinOps-focused cost optimization workflows
- `data-pipeline` - End-to-end data pipeline construction
- `k8s` - Kubernetes deployment with Helm and operators
- `ml-pipeline` - Machine learning pipeline with MLOps practices
- `observability` - Full-stack observability with metrics, logs, traces
- `security` - Security-hardened deployment patterns

**Skillchain Categories (8 New Domain Categories):**
- `cloud` - AWS, GCP, Azure provider skills
- `data` - Data engineering and architecture skills
- `developer` - Developer productivity skills
- `devops` - CI/CD, GitOps, platform engineering
- `finops` - Cost optimization and tagging
- `infrastructure` - IaC, Kubernetes, networking
- `multi-domain` - Cross-cutting composite workflows
- `security` - Security architecture and compliance

**Skillchain Registries (10 Domain Registries):**
- Organized skill references by domain for faster loading
- Registries: ai-ml, backend, cloud, data, developer, devops, finops, frontend, infrastructure, security

**Evaluation Framework:**
- `evaluation/evaluate.py` - Python script for skill evaluation
- `evaluation/scenarios.yaml` - Test scenarios for skill validation
- `evaluation/evaluation_report.json` - Generated evaluation reports

**GitHub Actions:**
- `.github/workflows/validate-skills.yml` - CI workflow for skill validation

**MLOps Examples:**
- `skills/implementing-mlops/examples/` - 5 production examples:
  - BentoML model serving
  - Feast feature store
  - Kubeflow pipelines
  - MLflow experiment tracking
  - Model monitoring

**Documentation:**
- `pages/docs/guides/plugin-commands.md` - Complete CLI reference for marketplace and plugin management

### Changed

**Installer Updates (v3.0):**
- Updated `install.sh` to reference new `.claude-commands/` path
- Proper handling of Claude Code plugin CLI commands
- Better error messages for marketplace operations

**SQL Optimization Skill:**
- Renamed `reference/` to `references/` for consistency with other skills

## [0.5.0] - 2025-12-05

### 🎉 MAJOR MILESTONE: All 76 Skills Production-Ready

**Historic Achievement:** Converted all 47 master plans into complete SKILL.md implementations. The project now has **76 production-ready skills** with full documentation, code examples, and decision frameworks.

### Added

**47 New SKILL.md Implementations:**

All skills follow Anthropic's best practices with progressive disclosure, multi-language support, and decision frameworks.

**DevOps Skills (6):**
- `testing-strategies` - Unit, integration, E2E testing patterns
- `building-ci-pipelines` - GitHub Actions, GitLab CI, Jenkins pipelines
- `implementing-gitops` - ArgoCD, Flux, GitOps workflows
- `platform-engineering` - Internal Developer Platforms (IDPs), Backstage
- `managing-incidents` - Incident response, postmortems, on-call
- `writing-dockerfiles` - Multi-stage builds, security hardening, distroless

**Infrastructure Skills (12):**
- `operating-kubernetes` - K8s deployments, operators, Helm management
- `writing-infrastructure-code` - Terraform, Pulumi, CloudFormation patterns
- `administering-linux` - System management, systemd, troubleshooting
- `architecting-networks` - VPC design, subnets, routing, firewalls
- `load-balancing-patterns` - L4/L7 LBs, health checks, algorithms
- `planning-disaster-recovery` - RTO/RPO, backup strategies, failover testing
- `configuring-nginx` - Reverse proxy, SSL termination, performance tuning
- `shell-scripting` - Bash best practices, error handling, portability
- `managing-dns` - Route53, zones, record types, DNSSEC
- `implementing-service-mesh` - Istio, Linkerd, mTLS, traffic management
- `managing-configuration` - Configuration management, environment variables
- `designing-distributed-systems` - CAP theorem, consistency patterns, scaling

**Security Skills (7):**
- `architecting-security` - Zero trust, defense in depth, least privilege
- `implementing-compliance` - SOC 2, GDPR, HIPAA, ISO 27001 controls
- `managing-vulnerabilities` - CVE management, scanning, remediation
- `implementing-tls` - Certificate management, mTLS, ACME automation
- `configuring-firewalls` - iptables, cloud firewalls, segmentation
- `siem-logging` - SIEM platforms, threat detection, log aggregation
- `security-hardening` - CIS benchmarks, OS hardening, secure configuration

**Developer Productivity Skills (7):**
- `designing-apis` - REST, GraphQL, OpenAPI design principles
- `building-clis` - Python (Click, Typer), Go (Cobra), Rust (Clap)
- `designing-sdks` - Client library patterns, versioning, documentation
- `generating-documentation` - Docusaurus, OpenAPI, auto-generated docs
- `debugging-techniques` - Profiling, logging, troubleshooting strategies
- `managing-git-workflows` - Branching strategies, hooks, conflict resolution
- `writing-github-actions` - Workflows, reusable actions, matrix builds

**Data Engineering Skills (6):**
- `architecting-data` - Data lake, warehouse, lakehouse, medallion architecture
- `streaming-data` - Kafka, Flink, event-driven architectures
- `transforming-data` - dbt, ETL/ELT patterns, data quality
- `optimizing-sql` - Query optimization, indexing, execution plans
- `secret-management` - Vault, secret rotation, Kubernetes secrets
- `performance-engineering` - Profiling, benchmarking, optimization

**AI/ML Skills (4):**
- `implementing-mlops` - MLflow, experiment tracking, model registries
- `prompt-engineering` - LLM prompting techniques, chain-of-thought
- `evaluating-llms` - RAGAS, benchmarks, safety testing
- `embedding-optimization` - Chunking strategies, model selection, caching

**Cloud Skills (3):**
- `deploying-on-aws` - Well-Architected Framework, service selection
- `deploying-on-gcp` - BigQuery, Cloud Run, Vertex AI patterns
- `deploying-on-azure` - Container Apps, Azure OpenAI, Cosmos DB

**FinOps Skills (2):**
- `optimizing-costs` - FinOps practices, rightsizing, commitment discounts
- `resource-tagging` - Tag governance, cost allocation, enforcement

**GitHub Pages Documentation (8 New Categories):**

Complete documentation site with 47 new skill pages:
- `/docs/skills/devops/` - 6 DevOps skill docs
- `/docs/skills/infrastructure/` - 12 Infrastructure skill docs
- `/docs/skills/security/` - 7 Security skill docs
- `/docs/skills/developer-productivity/` - 7 Developer Productivity docs
- `/docs/skills/data-engineering/` - 6 Data Engineering docs
- `/docs/skills/ai-ml/` - 4 AI/ML docs
- `/docs/skills/cloud/` - 3 Cloud docs
- `/docs/skills/finops/` - 2 FinOps docs

**Plugin Marketplace Updates:**
- Added 8 new plugin groups in marketplace.json:
  - `devops-skills` - CI/CD, GitOps, testing, Docker
  - `infrastructure-skills` - K8s, IaC, networking, distributed systems
  - `security-skills` - Architecture, compliance, TLS, SIEM
  - `developer-productivity-skills` - APIs, CLIs, SDKs, docs
  - `data-engineering-skills` - Architecture, streaming, SQL, secrets
  - `ai-ml-skills` - MLOps, prompts, evaluation, embeddings
  - `cloud-provider-skills` - AWS, GCP, Azure
  - `finops-skills` - Cost optimization, tagging

### Changed

- **Skill Count:** 29 production → **76 production** (162% increase)
- **Master Plans:** 47 → 0 (all converted to production SKILL.md)
- **Documentation:** Added 8 new category pages with 47 skill docs
- **Sidebar:** Updated with all 10 skill categories
- **README:** Simplified to reflect all skills now production-ready

### Fixed

- MDX compilation errors in 12 documentation files (angle bracket escaping)
- JSX variable reference errors in GitOps documentation
- Broken link in security-hardening.md

### Statistics

- **New SKILL.md files:** 47
- **New documentation pages:** 47
- **New category configs:** 8
- **Plugin groups:** 11 → 19
- **Total production skills:** 76

---

## [0.4.2] - 2025-12-04

### Added

**Validation Package (`scripts/validation/`):**
- New modular validation package with CI and TUI modes
- **CI Mode**: Machine-readable output for pipelines
  - Output formats: JSON, JUnit XML, TAP, Console, Markdown
  - Exit codes: 0 (pass), 1 (failures), 2 (errors)
  - Flags: `--completed`, `--phase`, `--rules-only`, `--fail-fast`, `--quiet`, `--verbose`
- **TUI Mode**: Interactive terminal interface using Textual
  - Real-time validation with progress indicators
  - Filterable skill list (all/passed/failed/warnings)
  - Detail panel with errors, warnings, project rules, and suggestions
  - Keyboard navigation (j/k, arrows, vim-style)
- **Three-tier rule system**:
  - `rules.yaml` - Core validation rules (errors/warnings)
  - `community.yaml` - Community practices (suggestions)
  - `project.yaml` - Project-specific rules (ai-design-components conventions)
- **Project Rules**: First rule requires skills mentioning libraries to reference `RESEARCH_GUIDE.md`
- **Programmatic API**: `from validation import Validator, ValidationReport`

**TUI Features:**
- Column display: #, Skill Name, Status, Err, Warn, Proj, Sug
- Color-coded severity: red (errors), yellow (warnings), magenta (project rules), blue (suggestions)
- Separate "Project Rules" section in detail panel
- Summary bar with pass/fail/pending counts

### Changed
- Validation now separates core warnings from project-specific rule warnings
- TUI detail panel groups issues by source (core vs project rules)

### Fixed
- UTF-8 encoding errors when reading files with special characters (e.g., section symbols)

---

## [0.4.1] - 2025-12-03

### 🚀 MILESTONE: 47 New Skill Master Plans (DevOps, Security, Cloud, AI/ML)

**Major Achievement:** Created comprehensive init.md master plans for 47 new skills covering DevOps, Infrastructure, Security, Cloud, and AI/ML domains. Total of 90,839 lines of strategic planning documentation.

### Added

**47 New Skill Master Plans (init.md files):**

**Infrastructure & Networking (12 skills):**
- `infrastructure-as-code` - Terraform, Pulumi, CDK patterns (769 lines)
- `kubernetes-operations` - K8s management, Helm, operators (2,083 lines)
- `designing-distributed-systems` - Architecture patterns, CAP theorem (2,905 lines)
- `configuration-management` - Ansible, Chef, Puppet (1,844 lines)
- `network-architecture` - VPC design, subnets, routing (2,302 lines)
- `load-balancing-patterns` - ALB, NLB, service mesh LB (2,224 lines)
- `dns-management` - Route53, CloudDNS, record types (2,534 lines)
- `service-mesh` - Istio, Linkerd, Cilium (2,051 lines)
- `disaster-recovery` - RPO/RTO, backup strategies (2,843 lines)
- `linux-administration` - System management, troubleshooting (2,559 lines)
- `shell-scripting` - Bash/Zsh patterns (1,194 lines)
- `configuring-nginx` - Reverse proxy, SSL, performance (1,917 lines)

**Security (6 skills):**
- `security-architecture` - Zero trust, defense in depth (1,570 lines)
- `compliance-frameworks` - SOC2, ISO27001, HIPAA (2,333 lines)
- `vulnerability-management` - Scanning, remediation (2,023 lines)
- `siem-logging` - Security monitoring, alerting (2,666 lines)
- `implementing-tls` - Certificate management, mTLS (2,093 lines)
- `configuring-firewalls` - Network security rules (1,704 lines)

**Developer Productivity (7 skills):**
- `api-design-principles` - REST, GraphQL design patterns (2,781 lines)
- `building-clis` - Python, Go, Rust CLI frameworks (2,368 lines) [MULTI-LANGUAGE]
- `sdk-design` - Client library patterns (2,461 lines) [MULTI-LANGUAGE]
- `documentation-generation` - API docs, code docs (3,140 lines)
- `debugging-techniques` - Profiling, troubleshooting (1,711 lines) [MULTI-LANGUAGE]
- `git-workflows` - Branching strategies, hooks (1,549 lines)
- `writing-github-actions` - CI/CD workflows (1,996 lines)

**DevOps & Platform (6 skills):**
- `building-ci-pipelines` - GitHub Actions, GitLab CI, Jenkins (1,793 lines)
- `gitops-workflows` - ArgoCD, Flux patterns (1,454 lines)
- `testing-strategies` - Unit, integration, E2E testing (1,791 lines) [MULTI-LANGUAGE]
- `platform-engineering` - IDP, Backstage, developer experience (2,876 lines)
- `incident-management` - On-call, post-mortems, SRE (1,615 lines)
- `writing-dockerfiles` - Multi-stage, security hardening (1,212 lines)

**Data & Analytics (6 skills):**
- `data-architecture` - Data mesh, lakehouse, medallion (2,359 lines)
- `streaming-data` - Kafka, Flink, event streaming (1,624 lines) [MULTI-LANGUAGE]
- `data-transformation` - dbt, ETL/ELT patterns (1,780 lines) [MULTI-LANGUAGE]
- `sql-optimization` - Query tuning, indexing (1,106 lines)
- `secret-management` - Vault, secrets rotation (1,427 lines)
- `performance-engineering` - Profiling, optimization (1,714 lines)

**AI/ML Operations (4 skills):**
- `mlops-patterns` - MLflow, experiment tracking, feature stores (2,295 lines)
- `prompt-engineering` - LLM prompting, chain-of-thought (1,577 lines)
- `llm-evaluation` - RAGAS, benchmarks, safety testing (1,557 lines)
- `embedding-optimization` - Chunking, model selection (1,416 lines)

**Cloud Patterns (3 skills):**
- `aws-patterns` - Well-Architected, service selection (2,475 lines)
- `gcp-patterns` - BigQuery, Vertex AI, GKE (1,840 lines)
- `azure-patterns` - Container Apps, Azure OpenAI (1,695 lines)

**FinOps (3 skills):**
- `cost-optimization` - FinOps practices, rightsizing (1,370 lines)
- `resource-tagging` - Tag governance, enforcement (1,175 lines)
- `security-hardening` - CIS benchmarks, hardening (1,068 lines)

**Project Documentation:**
- `docs/SKILL_ORCHESTRATION_PLAN.md` - Wave-based execution strategy for skill creation

### Multi-Language Skills

9 skills include implementations across TypeScript, Python, Go, and Rust:
- `testing-strategies`, `building-clis`, `sdk-design`, `debugging-techniques`
- `streaming-data`, `data-transformation`, `shell-scripting`, `sql-optimization`
- All cloud pattern skills include Terraform, CDK, and native SDK examples

### Research Methodology

All init.md files include research from:
- **Google Search Grounding**: 100+ queries for 2025 best practices
- **Context7**: Library trust scores and documentation (e.g., Argo CD 91.8/100, MLflow 95/100)
- Decision frameworks with actionable guidance
- Production-ready tool recommendations

### Statistics

- **Total init.md files:** 47
- **Total lines written:** 90,839
- **Average lines per skill:** 1,933
- **Skills with SKILL.md (production):** 29
- **Total skill coverage:** 76 skills

---

## [0.4.0] - 2025-12-03

### 🎉 MILESTONE: 100% Progressive Disclosure Coverage

**Major Achievement:** All 29 skills now have complete progressive disclosure with zero broken references.

### Added

**110 new files created across 17 skills to complete progressive disclosure:**

**Phase 0 - Low Priority (7 skills, 20 files):**
- `using-timeseries-databases/references/questdb.md` - QuestDB high-throughput guide
- `visualizing-data/examples/javascript/accessible-chart.tsx` - WCAG 2.1 AA compliant chart
- `securing-authentication/references/` - 3 files (api-security, managed-auth-comparison, self-hosted-auth)
- `using-relational-databases/references/` - 3 files (mysql-guide, sqlite-guide, serverless-databases)
- `implementing-navigation/examples/` - 3 files (mobile-navigation, django_urls, fastapi_routes)
- `model-serving/` - 3 files (streaming-sse.md, k8s-vllm-deployment/, langchain-rag-qdrant/)
- `using-vector-databases/` - 4 files (hybrid-search.md, rust-axum-vector/, typescript-rag/, evaluate_rag.py)

**Phase 1 - Medium Priority (4 skills, 22 files):**
- `assembling-components/` - 7 files (Python/React/Rust templates + 4 dashboard examples)
- `implementing-api-patterns/examples/` - 5 files (go-gin, graphql-strawberry, grpc-tonic, rust-axum, typescript-trpc)
- `using-message-queues/` - 5 files (BullMQ/Celery guides + 3 complete workflow examples)
- `implementing-observability/` - 4 files (axum-tracing, lgtm-docker-compose, 2 automation scripts)

**Phase 2 - High Priority (4 skills, 30 files):**
- `creating-dashboards/` - 10 files (grid layouts, KPI formats, themes, 5 dashboard examples, 2 scripts)
- `building-ai-chat/` - 8 files (4 reference guides + 4 complete chat examples)
- `ai-data-engineering/` - 4 files (chunking strategies, data versioning, orchestration, Qdrant setup)
- `using-document-databases/` - 8 files (aggregation, indexing, patterns, anti-patterns, 2 examples)

**Phase 3 - Critical Priority (2 skills, 38 files):**
- `building-tables/` - 14 files (6 reference guides + 6 examples + 2 scripts)
  - References: basic-tables, interactive, advanced-grids, editing, responsive, selection
  - Examples: TanStack basic, sortable/filtered, virtual scrolling, AG Grid, responsive patterns, editable cells, state persistence, server-side sorting
  - Scripts: export_table_data, (existing scripts)
- `managing-media/` - 24 files (13 reference guides + 11 examples)
  - References: image upload/optimization, video optimization, PDF viewer, audio player, cloud storage, carousel, responsive, accessibility (images/video/audio), advanced upload, office viewer
  - Examples: image crop, carousel, gallery, chunked upload, S3 direct, audio player/waveform, video player, PDF viewers

**Project Documentation:**
- `SKILL_COMPLETION_PLAN.md` - Comprehensive completion tracking document (v2.0 - FINAL)

### Changed

- **Completion Status:** 41% → 100% (all 29 skills complete)
- **Missing Files:** 116 → 0 (100% reduction)
- **Progressive Disclosure:** Fully intact across all skills
- Updated `SKILL_COMPLETION_PLAN.md` through versions 1.0 → 2.0 (FINAL)

### Impact

**Coverage Now Complete For:**
- All database types (relational, document, vector, timeseries, graph)
- All API patterns (REST, GraphQL, gRPC, tRPC) across 5 languages
- Full AI/ML pipeline (RAG, embeddings, chunking, orchestration)
- Complete chat interfaces (streaming, multi-modal, tool-calling, accessibility)
- Dashboard components (executive, monitoring, customizable, real-time)
- Data tables (basic, interactive, advanced grids, virtual scrolling, editing)
- Media handling (image, video, audio, PDF, Office docs)
- Message queues (BullMQ, Celery, Temporal)
- Observability (LGTM stack, OpenTelemetry)
- Full-stack templates (Python, TypeScript, Rust, Go)
- Authentication and security
- Navigation patterns
- All 29 skills production-ready

### Files Created

- **Reference Documentation:** 54 comprehensive guides
- **Code Examples:** 42 working implementations
- **Scripts:** 12 automation utilities (token-free execution)
- **Assets:** 2 configuration files

### Statistics

- Total files created: 110
- Time elapsed: ~7 hours
- Skills completed: 17 (from 12 to 29)
- Languages supported: Python, TypeScript, Rust, Go
- Zero broken references remaining

## [0.3.4] - 2025-12-03

### Added
- **Community Health Files**:
  - `CODE_OF_CONDUCT.md` - Contributor Covenant v2.1
  - `CONTRIBUTING.md` - Comprehensive contribution guidelines
    - Skill development guidelines from skill_best_practice.md
    - Branch naming, commit messages, PR process
    - Quality checklist for skills
    - Multi-language support expectations

- **GitHub Issue Templates** (`.github/ISSUE_TEMPLATE/`):
  - `bug_report.yml` - Bug reporting with component, skill, environment fields
  - `feature_request.yml` - Feature proposals with priority and acceptance criteria
  - `skill_contribution.yml` - Dedicated skill contribution workflow
    - Quality checklist (500 line limit, gerund naming, progressive disclosure)
    - Decision framework requirements
    - Multi-language support
  - `documentation.yml` - Documentation improvement requests
  - `question.yml` - General questions and discussions
  - `config.yml` - Template configuration with contact links

- **Project Roadmap System**:
  - `.github/ROADMAP.md` - Comprehensive project roadmap reflecting all 29 skills complete
  - `.github/ISSUE_TEMPLATE/roadmap_item.yml` - Issue template for proposing roadmap items

### Changed
- **Documentation Updates**:
  - `docs/STYLING_TEMPLATE.md` - Completely rewritten as integration guide
    - Updated to reflect all 29 skills complete
    - Added component-specific token references for all 12 UI skills
    - Added theme switching, RTL support, and accessibility sections
    - Uses correct gerund skill naming convention
  - Added `source_data/` to `.gitignore`

## [0.3.3] - 2025-12-02

### Added
- **Skillchain v2.1 - Modular Architecture (Phase 3 Complete)**:
  - **User Preferences System**: Saves choices to `~/.claude/skillchain-prefs.yaml` for smart defaults
  - **Skill Versioning**: All 29 skills versioned (v1.0.0) with changelog and compatibility tracking
  - **Parallel Skill Loading**: Independent skills load concurrently via `parallel_group` field
  - **Blueprint System**: Pre-configured skill chains for common patterns:
    - `dashboard` - Analytics dashboard with charts & KPIs
    - `crud-api` - REST API with database & auth
    - `rag-pipeline` - RAG with vector search & embeddings
  - **Category Orchestrators**: Specialized handlers for frontend, backend, fullstack, ai-ml
  - **Dynamic Path Discovery**: Works globally from any project via Bash path detection

- New skillchain directory structure (19 files):
  - `skillchain.md` - Router with Step 0 (path discovery), Step 0.5 (preferences), Step 7 (save prefs)
  - `_registry.yaml` - 29 skills with keywords, dependencies, versions, parallel_group
  - `_help.md` - Updated help with v2.1 features
  - `_shared/` - 9 shared resource files (theming-rules, execution-flow, preferences, parallel-loading, changelog, compatibility)
  - `categories/` - 4 orchestrators (frontend.md, backend.md, fullstack.md, ai-ml.md)
  - `blueprints/` - 3 templates (dashboard.md, crud-api.md, rag-pipeline.md)

- Updated `commands/README.md` with comprehensive v2.1 documentation
- Updated `_help.md` with v2.1 features section and revised workflow steps

### Changed
- Installer updated to v2.1 with Phase 3 feature display
- Registry version bumped to 2.1.0
- All file references now use `{SKILLCHAIN_DIR}/...` pattern for portability
- `_help.md` "How It Works" section updated to reflect 8-step workflow

### Removed
- Old monolithic `skillchain.md` files (replaced by modular structure)

## [0.3.2] - 2025-12-02

### Added
- Complete backend support in `/skillchain` command:
  - Backend plugin groups: `backend-data-skills`, `backend-api-skills`, `backend-platform-skills`, `backend-ai-skills`
  - Backend skill mappings for all 14 backend skills
  - 14 new backend configuration question blocks (databases, APIs, auth, observability, deployment, AI/ML)
  - Backend keyword detection (database, api, vector, kafka, deploy, auth, etc.)
  - Full-stack compound detection combining frontend and backend skills
- Backend examples in skillchain help guide
- Global installation option for skillchain command (`--global` flag)
- Architecture documentation directory (`docs/architecture/`)

### Changed
- Updated skillchain.md to show all 29 skills (was showing only 15)
- Help guide now displays both frontend (15) and backend (14) skill categories
- Skillchain description updated to "full-stack applications" (from "UI components")
- Moved TOKEN_EFFICIENCY.md to `docs/architecture/` for better organization
- Updated README.md with architecture docs link

### Removed
- Deleted `skillchains/` directory (17 files) - outdated documentation superseded by `/skillchain` command
  - README.md, GUIDE.md, ROADMAP.md (outdated, claimed "3/14 skills")
  - patterns/ directory (now embedded in skillchain.md)
  - chains/ directory (superseded by keyword mapping)
  - examples/ directory

### Fixed
- YAML frontmatter error in skillchain.md (unquoted values containing colons)

## [0.3.1] - 2025-12-02

### Added
- New `ingesting-data` skill for data onboarding and ETL pipelines
  - Cloud storage ingestion (S3, GCS, Azure Blob)
  - File format handling (CSV, JSON, Parquet, Excel)
  - API feed consumption (REST polling, webhooks, GraphQL subscriptions)
  - Streaming sources (Kafka, Kinesis, Pub/Sub)
  - Database migration and CDC patterns
  - ETL tools reference (dlt, Meltano, Airbyte, Dagster)
- Scripts for ingesting-data:
  - `validate_csv_schema.py` - CSV schema validation
  - `test_s3_connection.py` - S3 connectivity testing
  - `generate_dlt_pipeline.py` - dlt pipeline scaffold generator

### Changed
- Updated skillchain.md with ingestion keyword mapping
- backend-data-skills plugin now includes ingesting-data as first skill
- Version bump to 0.3.1

## [0.3.0] - 2025-12-02

### Added
- **13 Backend Skills** - Complete backend development capability:

  **Database Skills (5):**
  - `databases-relational` - PostgreSQL, MySQL, SQLite with Prisma/Drizzle/SQLAlchemy
  - `databases-vector` - Qdrant, Pinecone, pgvector for RAG and semantic search
  - `databases-timeseries` - ClickHouse, TimescaleDB, InfluxDB for metrics
  - `databases-document` - MongoDB, Firestore, DynamoDB for flexible schemas
  - `databases-graph` - Neo4j, memgraph with Cypher query patterns

  **API & Communication Skills (3):**
  - `api-patterns` - REST, GraphQL, gRPC, tRPC across Python/TypeScript/Rust/Go
  - `message-queues` - Kafka, RabbitMQ, NATS, Temporal for async processing
  - `realtime-sync` - WebSockets, SSE, Y.js, Liveblocks for live collaboration

  **Platform Skills (3):**
  - `observability` - OpenTelemetry, LGTM stack (Loki, Grafana, Tempo, Mimir)
  - `auth-security` - OAuth 2.1, passkeys/WebAuthn, RBAC, secrets management
  - `deploying-applications` - Kubernetes, serverless, edge deployment patterns

  **AI/ML Skills (2):**
  - `ai-data-engineering` - RAG pipelines, embedding strategies, chunking
  - `model-serving` - vLLM, BentoML, Ollama for LLM deployment

- 4 new plugin groups in marketplace.json:
  - `backend-data-skills` - All database skills
  - `backend-api-skills` - API, messaging, realtime
  - `backend-platform-skills` - Observability, auth, deployment
  - `backend-ai-skills` - AI data engineering, model serving

- Backend keyword mappings in skillchain.md for automatic skill chaining
- Multi-language support across all backend skills (Python, TypeScript, Rust, Go)
- Scripts for auth-security:
  - `generate_jwt_keys.py` - EdDSA/ES256 key pair generation
  - `validate_oauth_config.py` - OAuth 2.1 compliance validation
- Script for realtime-sync:
  - `test_websocket_connection.py` - WebSocket connectivity testing

### Changed
- Total skill count: 15 frontend + 13 backend = 28 skills
- All backend SKILL.md files under 500 lines (progressive disclosure applied)
- Updated CLAUDE.md with backend skill references

## [0.2.0] - 2025-12-01

### Added
- Complete SKILL.md implementations for all 14 component skills
- New skills completed:
  - `managing-media` - Media & file management components
  - `guiding-users` - Onboarding & help systems
  - `displaying-timelines` - Timeline & activity components
  - `building-ai-chat` - AI chat interfaces (strategic priority)
  - `creating-dashboards` - Dashboard & analytics components
  - `building-tables` - Tables & data grids
  - `implementing-search-filter` - Search & filter interfaces
  - `implementing-drag-drop` - Drag-and-drop functionality
  - `providing-feedback` - Feedback & notification systems
  - `implementing-navigation` - Navigation patterns
  - `designing-layouts` - Layout systems & responsive design
- Reference files for theming-components:
  - `color-system.md` - Complete color token reference
  - `typography-system.md` - Typography token reference
  - `spacing-system.md` - Spacing token reference
- Comprehensive chart catalog for visualizing-data (24+ chart types)

### Changed
- Renamed all skill directories to use gerund naming convention (Anthropic best practice):
  - `data-viz` → `visualizing-data`
  - `forms` → `building-forms`
  - `design-tokens` → `theming-components`
  - `ai-chat` → `building-ai-chat`
  - `dashboards` → `creating-dashboards`
  - `tables` → `building-tables`
  - `search-filter` → `implementing-search-filter`
  - `drag-drop` → `implementing-drag-drop`
  - `feedback` → `providing-feedback`
  - `navigation` → `implementing-navigation`
  - `layout` → `designing-layouts`
  - `timeline` → `displaying-timelines`
  - `media` → `managing-media`
  - `onboarding` → `guiding-users`
- Reduced `theming-components/SKILL.md` from 878 to 384 lines (progressive disclosure)
- Reduced `visualizing-data/SKILL.md` from 639 to 329 lines (progressive disclosure)
- Updated marketplace.json with all 14 correct skill paths
- Moved all init.md files to `docs/init_files/` for reference

### Fixed
- Skill naming convention violations (now all use gerund form)
- SKILL.md line count violations (all now under 500 lines)
- Directory names now match SKILL.md frontmatter names

## [0.1.0] - 2025-01-13

### Added
- Initial project structure with 14 component skill categories
- Completed `data-viz` skill with 24+ visualization types and decision frameworks
- Completed `forms` skill with 50+ input types and validation patterns
- Comprehensive master plans (init.md) for all 14 skill categories
- Research methodology guide for library recommendations
- Skills organized into 6 plugin groups in marketplace.json:
  - ui-foundation-skills (design-tokens)
  - ui-data-skills (data-viz, tables, dashboards)
  - ui-input-skills (forms, search-filter)
  - ui-interaction-skills (ai-chat, drag-drop, feedback)
  - ui-structure-skills (navigation, layout, timeline)
  - ui-content-skills (media, onboarding)
- Project documentation (README.md, CLAUDE.md, skill_best_practice.md)
- MIT License
- Comprehensive .gitignore for development

### In Progress
- 12 additional component skills awaiting SKILL.md implementation
- Design tokens foundational system
- AI chat interfaces (strategic priority)

[0.6.0]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.6.0
[0.5.2]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.5.2
[0.5.1]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.5.1
[0.5.0]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.5.0
[0.4.2]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.4.2
[0.4.1]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.4.1
[0.4.0]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.4.0
[0.3.4]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.3.4
[0.3.3]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.3.3
[0.3.2]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.3.2
[0.3.1]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.3.1
[0.3.0]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.3.0
[0.2.0]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.2.0
[0.1.0]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.1.0
