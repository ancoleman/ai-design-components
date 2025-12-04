---
sidebar_position: 7
---

# Writing GitHub Actions

Master plan for authoring GitHub Actions workflows for CI/CD, automation, and DevOps tasks. This skill covers workflow syntax, action development, secrets management, matrix strategies, and best practices for building robust and efficient automation pipelines.

## Status

<span class="badge badge--primary">Master Plan Available</span>

## Key Topics

- **Workflow Fundamentals**
  - YAML syntax and structure
  - Triggers (push, pull_request, schedule, workflow_dispatch)
  - Jobs and steps organization
  - Runner selection (ubuntu, windows, macos)
  - Workflow dependencies and sequencing

- **Action Development**
  - JavaScript actions vs Docker actions vs Composite actions
  - Action metadata (action.yml)
  - Inputs, outputs, and environment variables
  - Action versioning and releases
  - Publishing to GitHub Marketplace

- **CI/CD Patterns**
  - Build and test workflows
  - Multi-language matrix testing
  - Caching dependencies (npm, pip, cargo)
  - Artifact uploading and downloading
  - Deployment strategies

- **Advanced Techniques**
  - Reusable workflows
  - Composite actions for DRY
  - Dynamic matrix generation
  - Conditional execution (if statements)
  - Workflow orchestration

- **Security & Secrets**
  - Secrets management
  - GITHUB_TOKEN permissions
  - Environment protection rules
  - Dependency scanning
  - Security hardening

- **Optimization**
  - Workflow performance tuning
  - Parallelization strategies
  - Caching optimization
  - Self-hosted runners
  - Cost optimization

## Primary Tools & Technologies

- **GitHub Actions**: Workflows, Actions, Runners
- **Marketplace Actions**: actions/checkout, actions/setup-node, actions/cache
- **Action Development**: @actions/core, @actions/github, Docker
- **Testing**: act (local testing), nektos/act
- **Monitoring**: GitHub Actions dashboard, workflow run logs

## Integration Points

- **Git Workflows**: Automate Git operations
- **Documentation Generation**: Auto-deploy documentation
- **Building CLIs**: Test and release CLIs
- **SDK Design**: Test and publish SDKs
- **API Design Principles**: API testing and deployment

## Related Skills

- CI/CD pipelines
- DevOps automation
- Container development
- Testing automation
- Release management

## Implementation Approach

The skill will provide:
- Workflow templates for common scenarios
- Action development boilerplates
- Matrix strategy examples
- Security best practices checklist
- Performance optimization guide
- Troubleshooting patterns
