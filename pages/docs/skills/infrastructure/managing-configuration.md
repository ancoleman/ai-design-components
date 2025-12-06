---
sidebar_position: 11
title: Managing Configuration
description: Ansible configuration management with playbooks, roles, and testing
tags: [infrastructure, ansible, configuration-management, automation]
---

# Managing Configuration

Automate server and application configuration using Ansible. Covers playbook creation, role structure, inventory management, secret management, testing patterns, and idempotency best practices.

## When to Use

Use when:
- Creating Ansible playbooks to configure servers or deploy applications
- Structuring reusable Ansible roles with proper directory layout
- Managing inventories (static files or dynamic cloud-based)
- Securing secrets with ansible-vault or HashiCorp Vault integration
- Testing roles with Molecule before production deployment
- Ensuring idempotent playbooks that safely run multiple times
- Implementing GitOps workflows for configuration as code

## Quick Start

### Basic Playbook Example

```yaml
---
# site.yml
- name: Configure web servers
  hosts: webservers
  become: yes

  tasks:
    - name: Ensure nginx is installed
      apt:
        name: nginx
        state: present
      notify: Restart nginx

    - name: Start nginx service
      service:
        name: nginx
        state: started
        enabled: yes

  handlers:
    - name: Restart nginx
      service:
        name: nginx
        state: restarted
```

Run with:
```bash
ansible-playbook -i inventory/production site.yml
```

## Core Concepts

### 1. Idempotency

Run playbooks multiple times without unintended side effects. Use state-based modules (`present`, `started`, `latest`) instead of imperative commands.

**Idempotent (good):**
```yaml
- name: Ensure package installed
  apt:
    name: nginx
    state: present
```

**Not idempotent (avoid):**
```yaml
- name: Install package
  command: apt-get install -y nginx
```

### 2. Inventory Management

**Static Inventory:** INI or YAML files for stable environments.
**Dynamic Inventory:** Scripts or plugins for cloud environments (AWS, Azure, GCP).

Example static inventory (INI):
```ini
[webservers]
web1.example.com ansible_host=10.0.1.10
web2.example.com ansible_host=10.0.1.11

[webservers:vars]
nginx_worker_processes=4
```

### 3. Roles vs Playbooks

**Playbooks:** Orchestrate multiple tasks and roles for specific deployments.
**Roles:** Reusable, self-contained configuration units with standardized directory structure.

Standard role structure:
```
roles/nginx/
├── defaults/     # Default variables
├── tasks/        # Task files
├── handlers/     # Change handlers
├── templates/    # Jinja2 templates
├── files/        # Static files
└── meta/         # Dependencies
```

### 4. Secret Management

**ansible-vault:** Built-in encryption for sensitive data.
**HashiCorp Vault:** Enterprise-grade secrets management with dynamic credentials.

Encrypt secrets:
```bash
ansible-vault create group_vars/all/vault.yml
ansible-playbook site.yml --ask-vault-pass
```

## Common Workflows

### Workflow 1: Create New Playbook

**Step 1:** Define inventory
```ini
# inventory/production
[webservers]
web1.example.com
web2.example.com
```

**Step 2:** Create playbook structure
```yaml
---
- name: Configure application
  hosts: webservers
  become: yes

  pre_tasks:
    - name: Update package cache
      apt:
        update_cache: yes

  roles:
    - common
    - application

  post_tasks:
    - name: Verify service
      uri:
        url: http://localhost:8080/health
        status_code: 200
```

**Step 3:** Test with check mode
```bash
ansible-playbook -i inventory/production site.yml --check --diff
```

**Step 4:** Execute playbook
```bash
ansible-playbook -i inventory/production site.yml
```

### Workflow 2: Create and Test Role

**Step 1:** Initialize role structure
```bash
ansible-galaxy init roles/myapp
```

**Step 2:** Define tasks
```yaml
# roles/myapp/tasks/main.yml
---
- name: Install application dependencies
  apt:
    name: "{{ item }}"
    state: present
  loop: "{{ myapp_dependencies }}"

- name: Deploy application
  template:
    src: app.conf.j2
    dest: /etc/myapp/app.conf
  notify: Restart myapp
```

**Step 3:** Add handler
```yaml
# roles/myapp/handlers/main.yml
---
- name: Restart myapp
  service:
    name: myapp
    state: restarted
```

**Step 4:** Initialize Molecule testing
```bash
cd roles/myapp
molecule init scenario default --driver-name docker
```

**Step 5:** Run tests
```bash
molecule test
```

### Workflow 3: Set Up Dynamic Inventory (AWS)

**Step 1:** Install AWS collection
```bash
ansible-galaxy collection install amazon.aws
```

**Step 2:** Configure dynamic inventory
```yaml
# inventory/aws_ec2.yml
plugin: aws_ec2
regions:
  - us-east-1
filters:
  tag:Environment: production
  instance-state-name: running
keyed_groups:
  - key: tags.Role
    prefix: role
hostnames:
  - tag:Name
compose:
  ansible_host: private_ip_address
```

**Step 3:** Verify inventory
```bash
ansible-inventory -i inventory/aws_ec2.yml --list
```

**Step 4:** Run playbook
```bash
ansible-playbook -i inventory/aws_ec2.yml site.yml
```

## Testing and Quality

### Pre-Deployment Validation

**Step 1:** Lint playbooks
```bash
ansible-lint playbooks/
```

**Step 2:** Check mode (dry run)
```bash
ansible-playbook site.yml --check --diff
```

**Step 3:** Test roles with Molecule
```bash
cd roles/myapp
molecule test
```

**Step 4:** Verify idempotence
```bash
molecule idempotence
```

## Tool Selection

### When to Use Ansible

- Configuring servers/VMs after provisioning
- Deploying applications to existing infrastructure
- Managing OS-level settings (users, packages, services)
- Orchestrating multi-step workflows across hosts
- Cloud-native environments (agentless SSH/WinRM)
- Teams new to configuration management

### When to Use Alternatives

**Infrastructure-as-Code (Terraform):** Creating cloud infrastructure resources.
**Kubernetes:** Container orchestration and configuration.
**Chef/Puppet:** Existing deployments with high migration costs.

### Ansible vs IaC Integration

Best practice: Terraform provisions, Ansible configures.

**Workflow:**
1. Terraform creates AWS EC2 instances, security groups, load balancers
2. Terraform outputs instance IPs to Ansible inventory
3. Ansible configures OS, installs packages, deploys applications
4. Ansible sets up monitoring, backups, operational tasks

## Troubleshooting

### Common Issues

**Connection failures:**
- Verify SSH access: `ansible all -i inventory -m ping`
- Check SSH keys: `ssh -vvv user@host`
- Test with password: `ansible-playbook site.yml --ask-pass`

**Handler not firing:**
- Handlers only run on change (check task `changed` status)
- Handlers run at end of playbook (use `meta: flush_handlers` to force earlier)
- Handler names must match exactly

**Variable not defined:**
- Check variable precedence (command-line > playbook > inventory > defaults)
- Use debug module: `- debug: var=myvar`
- Verify variable files are loaded: `ansible-playbook site.yml -v`

**Idempotency violations:**
- Run playbook twice, compare output
- Check for `changed` on every run
- Use state-based modules instead of `command`/`shell`

## Integration with Other Skills

- [Writing Infrastructure Code](./writing-infrastructure-code) - Terraform provisions, Ansible configures
- [Operating Kubernetes](./operating-kubernetes) - Ansible deploys K8s clusters (kubespray)
- [Administering Linux](./administering-linux) - Linux commands and system administration
- [Shell Scripting](./shell-scripting) - Ansible playbook automation

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/managing-configuration)
- Playbook Patterns: `references/playbook-patterns.md`
- Role Structure: `references/role-structure.md`
- Inventory Management: `references/inventory-management.md`
- Secrets Management: `references/secrets-management.md`
- Testing Guide: `references/testing-guide.md`
- Idempotency Guide: `references/idempotency-guide.md`
- Decision Framework: `references/decision-framework.md`
- Troubleshooting: `references/troubleshooting.md`
