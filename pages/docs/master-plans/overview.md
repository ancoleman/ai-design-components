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

| Category | Skills | Focus Areas |
|----------|--------|-------------|
| [Infrastructure](/docs/master-plans/infrastructure) | 12 | IaC, Kubernetes, networking, distributed systems |
| [Security](/docs/master-plans/security) | 6 | Architecture, compliance, vulnerability management |
| [DevOps](/docs/master-plans/devops) | 6 | CI/CD, GitOps, testing, platform engineering |
| [Developer Productivity](/docs/master-plans/developer-productivity) | 7 | APIs, CLIs, SDKs, debugging, documentation |
| [Data](/docs/master-plans/data) | 6 | Architecture, streaming, transformation, governance |
| [AI/ML](/docs/master-plans/ai-ml) | 4 | MLOps, prompts, evaluation, data engineering |
| [Cloud](/docs/master-plans/cloud) | 3 | AWS, GCP, Azure patterns |
| [FinOps](/docs/master-plans/finops) | 3 | Cost optimization, tagging, security hardening |

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
