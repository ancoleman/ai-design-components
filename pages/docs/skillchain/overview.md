---
sidebar_position: 1
title: Skillchain Overview
description: Guided workflow for building full-stack applications with 76 production-ready skills across 10 domains
---

# Skillchain

Skillchain is a guided, step-by-step workflow system that chains Claude Skills together to build full-stack applications. Instead of manually triggering individual skills, skillchain automatically routes to the right orchestrator, loads dependencies, and ensures correct execution order.

## What is Skillchain?

The `/skillchain:start` command is the **recommended entry point** for using AI Design Components. It provides a conversational workflow that:

- **Analyzes your goal** from natural language descriptions
- **Detects the domain(s)** (frontend, backend, devops, infrastructure, security, developer, data, ai-ml, cloud, finops)
- **Matches relevant skills** using keyword detection and scoring
- **Orders skills correctly** with automatic dependency resolution
- **Applies user preferences** as smart defaults from previous sessions
- **Loads skills in parallel** when dependencies allow
- **Guides configuration** through targeted questions
- **Generates production code** with theming, accessibility, and best practices

## Why Use Skillchain?

| Traditional Approach | Skillchain Approach |
|---------------------|---------------------|
| User must know skill names | Describe what you want to build |
| User triggers skills individually | Skills chain automatically |
| Easy to miss required skills | Correct skill order enforced |
| No theming consistency | Theming always applied first |
| Manual component assembly | Assembly skill runs at end |
| Repeat configuration every time | Preferences saved between sessions |

### Example Comparison

**Traditional (requires knowledge):**
```
"Use the theming-components skill, then designing-layouts,
then creating-dashboards, then visualizing-data..."
```

**Skillchain (just describe your goal):**
```
/skillchain:start sales dashboard with revenue charts
```

## Version 3.0 Features

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

When detected, blueprints offer a faster path with optimized defaults (3-4 questions instead of 12+).

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
- **First run:** Answer questions, offered to save preferences
- **Future runs:** Your saved preferences become smart defaults
- **Override anytime:** Just provide a different answer

**Preference Priority:**
1. User's explicit choice (current workflow) - Highest
2. Saved preferences (from `~/.claude/skillchain-prefs.yaml`) - Medium
3. Default values (from skill definitions) - Lowest

### Skill Versioning

All 76 skills are versioned for compatibility tracking:

```yaml
# In registries/*.yaml
visualizing-data:
  version: "1.0.0"
  # ...
```

This enables:
- **Compatibility matrix** tracking which skills work together
- **Changelog tracking** for each skill's evolution
- **Version pinning** for reproducible builds

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

Skills are grouped by `parallel_group` in the registry. Dependencies are automatically resolved to ensure safe parallelization.

## Quick Start Examples

```bash
# Start Claude Code in your project
claude

# Frontend examples
/skillchain:start sales dashboard with revenue charts
/skillchain:start login form with validation

# Backend examples
/skillchain:start REST API with PostgreSQL
/skillchain:start RAG pipeline with vector search

# DevOps examples
/skillchain:start CI/CD pipeline with GitHub Actions
/skillchain:start GitOps deployment with ArgoCD

# Infrastructure examples
/skillchain:start Kubernetes cluster with Helm
/skillchain:start Terraform infrastructure for AWS

# Security examples
/skillchain:start SOC2 compliance implementation
/skillchain:start security hardening checklist

# AI/ML examples
/skillchain:start MLOps pipeline with MLflow
/skillchain:start LLM evaluation framework
```

## How It Works

1. **Parse Goal** - Skillchain analyzes keywords in your description
2. **Detect Domain(s)** - Routes to one of 10 domain orchestrators (or fullstack/multi-domain)
3. **Match Blueprint** - Checks for pre-configured patterns (12 available)
4. **Order Skills** - Ensures correct execution order with dependency resolution
5. **Load Preferences** - Applies saved preferences from previous sessions
6. **Guide Configuration** - Asks questions for each skill (or uses defaults)
7. **Parallel Loading** - Invokes independent skills concurrently
8. **Generate Code** - Produces themed, accessible components
9. **Save Preferences** - Optionally saves choices for next time

## Available Skills (76 Total)

### Frontend Skills (15)

| Group | Skills |
|-------|--------|
| Foundation | theming-components |
| Data Display | visualizing-data, building-tables, creating-dashboards |
| User Input | building-forms, implementing-search-filter |
| Interaction | building-ai-chat, implementing-drag-drop, providing-feedback |
| Structure | implementing-navigation, designing-layouts, displaying-timelines |
| Content | managing-media, guiding-users |
| Assembly | assembling-components |

### Backend Skills (14)

| Group | Skills |
|-------|--------|
| Data Ingestion | ingesting-data |
| Databases | using-relational-databases, using-vector-databases, using-timeseries-databases, using-document-databases, using-graph-databases |
| APIs & Messaging | implementing-api-patterns, using-message-queues, implementing-realtime-sync |
| Platform | securing-authentication, implementing-observability, deploying-applications |
| AI/ML | ai-data-engineering, model-serving |

### DevOps Skills (6)

writing-dockerfiles, testing-strategies, building-ci-pipelines, implementing-gitops, managing-incidents, platform-engineering

### Infrastructure Skills (12)

operating-kubernetes, writing-infrastructure-code, managing-configuration, architecting-networks, load-balancing-patterns, managing-dns, implementing-service-mesh, administering-linux, configuring-nginx, shell-scripting, planning-disaster-recovery, designing-distributed-systems

### Security Skills (7)

architecting-security, implementing-compliance, managing-vulnerabilities, implementing-tls, configuring-firewalls, siem-logging, security-hardening

### Developer Productivity Skills (7)

designing-apis, building-clis, designing-sdks, generating-documentation, debugging-techniques, managing-git-workflows, writing-github-actions

### Data Engineering Skills (6)

architecting-data, streaming-data, transforming-data, optimizing-sql, secret-management, performance-engineering

### AI/ML Skills (4)

implementing-mlops, prompt-engineering, evaluating-llms, embedding-optimization

### Cloud Provider Skills (3)

deploying-on-aws, deploying-on-gcp, deploying-on-azure

### FinOps Skills (2)

optimizing-costs, resource-tagging

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

## Next Steps

- [Install Skillchain](./installation.md) globally or per-project
- [Learn usage patterns](./usage.md) with examples
- [Explore blueprints](./blueprints.md) for fast-track presets
- [Understand architecture](./architecture.md) and how it works internally
