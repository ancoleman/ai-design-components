---
sidebar_position: 1
title: Master Plans Overview
description: 47 comprehensive skill master plans ready for implementation across DevOps, Infrastructure, Security, Cloud, and AI/ML domains
---

# Master Plans

47 comprehensive `init.md` master plans covering DevOps, Infrastructure, Security, Cloud, and AI/ML domains. Each master plan is a detailed planning document ready for SKILL.md implementation.

## What are Master Plans?

Master plans are detailed planning documents that contain:
- **Strategic positioning and market context** - Why this skill matters
- **Component taxonomy** - Comprehensive breakdown of all patterns
- **Decision frameworks** - When to use each approach
- **Tool recommendations with research backing** - Verified tools and libraries
- **Integration points with other skills** - How skills work together
- **Implementation roadmap** - Phased approach to building the skill

## Categories

| Category | Skills | Key Skills |
|----------|--------|------------|
| **Infrastructure** | 12 | [Kubernetes](./infrastructure/operating-kubernetes), [IaC](./infrastructure/writing-infrastructure-code), [Networks](./infrastructure/architecting-networks), [Service Mesh](./infrastructure/implementing-service-mesh) |
| **Security** | 6 | [Architecture](./security/architecting-security), [Compliance](./security/implementing-compliance), [TLS](./security/implementing-tls), [SIEM](./security/siem-logging) |
| **DevOps** | 6 | [CI/CD](./devops/building-ci-pipelines), [GitOps](./devops/implementing-gitops), [Testing](./devops/testing-strategies), [Platform](./devops/platform-engineering) |
| **Developer Productivity** | 7 | [APIs](./developer-productivity/designing-apis), [CLIs](./developer-productivity/building-clis), [SDKs](./developer-productivity/designing-sdks), [Docs](./developer-productivity/generating-documentation) |
| **Data** | 6 | [Architecture](./data/architecting-data), [Streaming](./data/streaming-data), [Transform](./data/transforming-data), [SQL](./data/optimizing-sql) |
| **AI/ML** | 4 | [MLOps](./ai-ml/implementing-mlops), [Prompts](./ai-ml/prompt-engineering), [Eval](./ai-ml/evaluating-llms), [Embeddings](./ai-ml/embedding-optimization) |
| **Cloud** | 3 | [AWS](./cloud/deploying-on-aws), [GCP](./cloud/deploying-on-gcp), [Azure](./cloud/deploying-on-azure) |
| **FinOps** | 3 | [Costs](./finops/optimizing-costs), [Tags](./finops/resource-tagging), [Hardening](./finops/security-hardening) |

## Multi-Language Skills

9 master plans include implementations in multiple programming languages:
- **TypeScript** - Node.js backends, web applications
- **Python** - Data engineering, ML, automation
- **Go** - High-performance services, CLI tools
- **Rust** - Systems programming, performance-critical code

## Skill Levels

Master plans are categorized by complexity:

- **Low (Quick Reference)** - 300-500 lines, tactical patterns (e.g., resource-tagging)
- **Mid (Implementation Patterns)** - 500-800 lines, decision frameworks (e.g., cost-optimization)
- **High (Comprehensive Guide)** - 800-1200 lines, end-to-end workflows (e.g., aws-patterns)

## Next Steps

These master plans are ready for SKILL.md implementation following [Anthropic's best practices](/docs/guides/best-practices).

### How to Implement a Skill

1. **Read the init.md master plan** - Understand strategic positioning and scope
2. **Review decision frameworks** - Core patterns to include in SKILL.md
3. **Follow the 6-step process** from Anthropic's skill-creator:
   - Concrete examples first
   - Plan reusable resources (scripts/, references/, examples/)
   - Create SKILL.md (main file)
   - Add bundled resources
   - Validate and package
   - Iterate based on real usage

4. **Progressive disclosure** - Main SKILL.md references detailed files
5. **Testing** - Use real tasks, measure effectiveness

## Contributing

All master plans are in the [ai-design-components repository](https://github.com/ancoleman/ai-design-components/tree/main/skills). Each skill directory contains:
- `init.md` - Master plan (complete)
- `SKILL.md` - Main skill file (to be created)
- `references/` - Detailed documentation
- `examples/` - Working code examples
- `scripts/` - Utility scripts
- `assets/` - Templates and resources (optional)
