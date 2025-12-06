---
sidebar_position: 4
title: Configuration Management
description: Master plan for server configuration automation with Ansible, including playbooks, roles, inventory, secrets, and testing with Molecule
tags: [master-plan, infrastructure, configuration, ansible, automation]
---

# Configuration Management

:::info Status
**Master Plan** - Comprehensive init.md complete, ready for SKILL.md implementation
:::

Configuration management automates server and application configuration across environments. This skill focuses on Ansible (80% of content) with Chef/Puppet alternatives, covering idempotent playbooks, role architecture, dynamic inventory, secrets management, and testing strategies.

## Scope

This skill teaches:

- **Ansible Fundamentals** - Playbooks, roles, collections, inventory management
- **Idempotency Patterns** - Ensuring repeatable, safe executions
- **Inventory Management** - Static (INI/YAML), dynamic (AWS/Azure/GCP), hybrid
- **Secret Management** - ansible-vault and HashiCorp Vault integration
- **Testing Strategies** - Molecule for role testing, ansible-lint for quality
- **GitOps Workflows** - Configuration as code with version control
- **Chef/Puppet Basics** - For teams migrating to Ansible

## Key Components

### Ansible Architecture
- **Agentless** - SSH/WinRM (no agent installation)
- **YAML-based** - Easiest learning curve
- **Modules** - 5,000+ built-in modules (cloud, network, system)
- **Collections** - Organized roles, modules, plugins

### Core Patterns

**Playbook Structure:**
```yaml
pre_tasks:   # System prep (package updates)
roles:       # Reusable configuration
tasks:       # Playbook-specific actions
handlers:    # Change-triggered actions
post_tasks:  # Verification
```

**Role Structure:**
```
roles/nginx/
├── defaults/    # Default variables
├── vars/        # Override variables
├── tasks/       # Main task list
├── handlers/    # Change handlers
├── templates/   # Jinja2 templates
├── files/       # Static files
├── meta/        # Role metadata
└── tests/       # Role tests
```

**Idempotency:**
- Use idempotent modules (most Ansible modules are)
- Conditional execution with `when` clauses
- Handlers for change-triggered actions
- `ansible-lint` for checking best practices

### Inventory Management

**Static Inventory** (INI or YAML)
- Best for: Small environments (&lt;50 hosts), stable infrastructure
- Organize by roles, use group variables

**Dynamic Inventory** (Scripts/Plugins)
- Best for: Cloud-based, auto-scaling, multi-cloud
- Plugins: aws_ec2, azure_rm, gcp_compute
- Query APIs, return JSON

**Hybrid** - Combine static + dynamic for unified management

## Decision Framework

**Which Configuration Tool?**

```
New project / greenfield?
  YES → Ansible (easiest, modern, agentless)

Existing Chef/Puppet?
  Working well? → Keep it
  Pain points? → Migrate to Ansible

Windows-heavy environment?
  Mostly Windows → Puppet OR Ansible (WinRM)
  Mixed → Ansible (handles both)

Compliance-critical?
  Need compliance tools → Puppet (Remediate) OR Ansible
  Standard compliance → Ansible (sufficient)

Cloud-native / containers?
  YES → Ansible (best cloud integration, agentless)
```

**Ansible vs IaC:**
- **Use Ansible**: Configure resources AFTER provisioning, deploy applications, manage OS settings
- **Use Terraform/IaC**: Create cloud infrastructure, manage resource lifecycle
- **Best Practice**: Terraform provisions → Ansible configures

## Tool Recommendations

### Primary: Ansible
- **Library**: `/websites/ansible_ansible`
- **Trust Score**: High
- **Code Snippets**: 65,664+
- **Benchmark Score**: 81.6
- **Installation**: `pip install ansible`

### Testing: Ansible Lint
- **Library**: `/ansible/ansible-lint`
- **Code Snippets**: 445+
- **Purpose**: Check playbooks against best practices
- **Usage**: `ansible-lint --fix`

### Testing: Molecule
- **Library**: `/websites/ansible_readthedocs_io-projects-molecule`
- **Code Snippets**: 202+
- **Purpose**: Role development and testing framework
- **Features**: Multiple OS testing, idempotence verification, Docker/Podman integration

### Alternatives

**Chef** - Agent-based, Ruby DSL
- Best for: Existing Chef deployments, hybrid cloud
- Downsides: Complex setup, steep learning curve

**Puppet** - Agent-based, Puppet DSL
- Best for: Compliance-heavy, large Windows environments
- Downsides: Steep learning curve, resource-intensive

## Integration Points

**With Other Skills:**
- `writing-infrastructure-code` - Terraform provisions, Ansible configures
- `operating-kubernetes` - Ansible deploys K8s clusters (kubespray)
- `building-ci-pipelines` - CI/CD runs ansible-lint, Molecule tests
- `secret-management` - ansible-vault for simple, Vault for advanced
- `security-hardening` - Ansible applies CIS benchmarks
- `testing-strategies` - Molecule for role testing, Testinfra for verification

**GitOps Workflow:**
```
Configuration in Git → CI/CD Pipeline → Ansible Deploy
     │                      │                  │
     ▼                      ▼                  ▼
Version control      ansible-lint        Apply to
Audit trail          Molecule tests      servers
```

## Learn More

- [Full Master Plan (init.md)](https://github.com/ancoleman/ai-design-components/blob/main/skills/managing-configuration/init.md)
- Related: `writing-infrastructure-code`, `operating-kubernetes`, `secret-management`
