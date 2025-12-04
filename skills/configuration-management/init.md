# Configuration Management Skill - Master Plan

**Skill Name:** `configuration-management`
**Level:** Mid Level (5,000-8,000 tokens, 500-800 lines)
**Status:** Planning Phase
**Date:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [Configuration Management Taxonomy](#configuration-management-taxonomy)
5. [Decision Framework](#decision-framework)
6. [Ansible Patterns](#ansible-patterns)
7. [Testing Patterns](#testing-patterns)
8. [Tool Recommendations](#tool-recommendations)
9. [Skill Structure Design](#skill-structure-design)
10. [Integration Points](#integration-points)
11. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Market Context (2025)

**Configuration Management Landscape:**

- **Ansible dominates** for cloud-native and agentless automation (70%+ market share for new deployments)
- **Chef/Puppet declining** - legacy enterprise holdouts, minimal new adoption
- **GitOps emerging** - Configuration as code in Git repositories (ArgoCD, Flux)
- **Kubernetes ConfigMaps** - Container-native configuration (not covered here, see `kubernetes-operations`)
- **Infrastructure-as-Code overlap** - Terraform for provisioning, Ansible for configuration

**Key Trends:**

1. **Agentless > Agent-based** - SSH/WinRM preferred over installed agents
2. **Declarative > Imperative** - Define desired state, not procedural steps
3. **Idempotency critical** - Run playbooks repeatedly without side effects
4. **Cloud-native first** - Dynamic inventories from AWS/Azure/GCP
5. **Security focus** - Secrets management (Vault, ansible-vault) mandatory
6. **Testing required** - Molecule for role testing before production

### Skill Positioning

**This skill covers:**
- ✅ Ansible (primary focus - 80% of content)
- ✅ Configuration management patterns (idempotency, handlers, templates)
- ✅ Inventory management (static, dynamic, hybrid)
- ✅ Secret management (ansible-vault, HashiCorp Vault integration)
- ✅ Testing configurations (Molecule, ansible-lint)
- ✅ Chef/Puppet basics (10% - for teams migrating)
- ✅ GitOps configuration workflows

**Explicitly NOT covered:**
- ❌ Infrastructure provisioning (see `infrastructure-as-code`)
- ❌ Kubernetes configuration (see `kubernetes-operations`)
- ❌ CI/CD pipelines (see `building-ci-pipelines`)
- ❌ Monitoring/observability (different skill domain)

### Target Audience

**Primary:**
- DevOps engineers managing server configurations
- Platform teams standardizing infrastructure
- SREs automating operational tasks
- Cloud engineers managing hybrid environments

**Secondary:**
- Security teams implementing compliance (CIS benchmarks)
- Application teams deploying applications
- Teams migrating from Chef/Puppet to Ansible

---

## Skill Purpose and Scope

### What This Skill Does

This skill guides users through creating, managing, and testing configuration management automation using Ansible and related tools. It provides:

1. **Decision framework** - When to use Ansible vs Chef vs Puppet
2. **Ansible patterns** - Playbooks, roles, collections, inventory
3. **Idempotency guidance** - Ensuring repeatable, safe executions
4. **Secret management** - ansible-vault and HashiCorp Vault integration
5. **Testing strategies** - Molecule for role testing, ansible-lint for quality
6. **GitOps workflows** - Configuration as code with version control

### When to Use This Skill

**Trigger scenarios:**
- "Create an Ansible playbook to configure web servers"
- "Set up dynamic inventory for AWS EC2 instances"
- "Test this Ansible role with Molecule"
- "Migrate Chef cookbooks to Ansible"
- "Implement idempotent database configuration"
- "Manage secrets in Ansible with Vault"
- "Create reusable Ansible roles for NGINX"

### What Success Looks Like

**Users can:**
- ✅ Write idempotent Ansible playbooks
- ✅ Structure roles with proper directory layout
- ✅ Manage inventories (static and dynamic)
- ✅ Secure secrets using ansible-vault
- ✅ Test roles with Molecule before production
- ✅ Debug playbook failures efficiently
- ✅ Apply configuration management best practices

---

## Research Findings

### Research Methodology

**Research Date:** December 3, 2025
**Tools Used:** Google Search Grounding, Context7
**Libraries Evaluated:** Ansible, Ansible Lint, Molecule, Terraform, Chef, Puppet

### Google Search Grounding Results

#### Query 1: Ansible Best Practices 2025

**Key Findings:**

**Playbooks:**
- Keep simple and modular - organize tasks into roles
- Use tags for selective execution (`--tags install,restart`)
- Ensure idempotency with desired state (`present`, `started`, `latest`)
- Include `pre_tasks` and `post_tasks` for validation/cleanup
- Leverage AI-assisted generation tools (GitHub Copilot, ChatGPT)

**Roles:**
- Generated with `ansible-galaxy init` for consistent structure
- Single responsibility principle - one role, one purpose
- Standard directories: `defaults/`, `vars/`, `tasks/`, `handlers/`, `templates/`, `files/`
- Package in Ansible collections for distribution
- Consistent naming: `role_name.module_functionality`

**Collections:**
- Organize roles, modules, plugins by category
- Use semantic versioning (immutable tags prevent unexpected changes)
- Manage dependencies between collections
- Engage community for support and contributions

**General Best Practices:**
- Clean project structure: `inventory/`, `group_vars/`, `host_vars/`, `roles/`, `library/`
- Variable hygiene: `group_vars/all` for common values, selective overrides
- Secrets: ansible-vault or HashiCorp Vault
- Testing: Vendor collections against virtual devices
- Readability: Comments, consistent whitespace, clear names
- Use `--check` for dry runs, `--limit` for scoping, `--tags` for selective execution

**Sources:** gocodeo.com, moldstud.com, github.io, cloudmylab.com

#### Query 2: Configuration Management Tools Comparison

**Key Findings:**

**Ansible:**
- **Architecture:** Agentless (SSH/WinRM), push-based
- **Language:** YAML (easiest to learn)
- **Best for:** Simplicity, speed, small-to-medium environments
- **Scalability:** Lightweight, highly scalable
- **Security:** SSH + Vault
- **Downsides:** Debugging complex playbooks, large-scale SSH challenges

**Chef:**
- **Architecture:** Agent-based, pull-based (Chef Server)
- **Language:** Ruby DSL (steeper learning curve)
- **Best for:** Highly customizable, hybrid cloud
- **Security:** InSpec for auditing/compliance
- **Downsides:** Complex setup, resource-intensive

**Puppet:**
- **Architecture:** Agent-based (can be agentless), pull-based
- **Language:** Puppet DSL (declarative)
- **Best for:** Compliance-heavy, large enterprises
- **Security:** Strong compliance tools (Puppet Remediate)
- **Downsides:** Steep learning curve, resource-intensive

**Platform Support:** All support Linux/Unix, Puppet best for Windows

**Market Trend:** Ansible winning for new deployments (simplicity, agentless)

**Sources:** devopsroles.com, automq.com, attuneops.io, dev.to, betterstack.com

#### Query 3: Ansible Idempotency & Inventory

**Key Findings:**

**Idempotency:**
- **Definition:** Running task multiple times = same result as once
- **Why essential:** Predictability, reliability, efficiency, production safety
- **How to achieve:**
  - Use idempotent modules (most Ansible modules are)
  - Conditional execution with `when` clauses
  - Handlers for change-triggered actions
  - `ansible-lint` for checking best practices
  - Granular tasks with individual handlers
  - Thorough testing in controlled environments

**Static Inventory:**
- **Format:** INI or YAML files
- **Best for:** Small environments, stable infrastructure
- **Structure:** Groups in `[]`, hosts listed below
- **Best practices:** Organize by roles, descriptive names, consistent layout

**Dynamic Inventory:**
- **Best for:** Large/complex, cloud-based, multi-cloud
- **How it works:** Scripts/plugins query APIs, return JSON
- **Supported sources:** AWS, Azure, GCP, containers, virtualization, databases
- **Best practices:** Use inventory plugins (preferred), leverage cloud provider plugins, NetBox as source of truth

**Hybrid Approach:** Combine static + dynamic inventories

**Inventory Best Practices:**
- Define variables for parameterization
- Use ansible-vault for secrets
- Version control with Git
- Labeling to prevent wrong-host execution
- `group_vars` to avoid repetition

**Sources:** ansible.com, medium.com, devops.dev, centlinux.com, spacelift.io

### Context7 Library Research

#### Ansible (Primary)

**Library ID:** `/websites/ansible_ansible`
**Trust Score:** High
**Code Snippets:** 65,664+
**Benchmark Score:** 81.6

**Key Documentation Topics:**
- Playbooks, roles, inventory, modules
- Idempotency, handlers, variables, vault
- Dynamic inventory sources
- Collections and Galaxy

**Research Notes:**
- Massive documentation coverage (65K+ snippets)
- High trust score indicates production-ready
- Comprehensive module ecosystem
- Strong community support

#### Ansible Lint

**Library ID:** `/ansible/ansible-lint`
**Trust Score:** High
**Code Snippets:** 445+
**Benchmark Score:** N/A

**Purpose:** Check playbooks against best practices

#### Ansible Molecule

**Library ID:** `/websites/ansible_readthedocs_io-projects-molecule`
**Trust Score:** High
**Code Snippets:** 202+
**Benchmark Score:** N/A

**Purpose:** Role development and testing framework

**Key Features:**
- Multiple test sequences (converge, verify, idempotence)
- Integration with Testinfra for verification
- Support for Docker, Podman, VMs
- Parallel test execution with Tox

### Key Insights from Research

**2025 Configuration Management Reality:**

1. **Ansible is the standard** - Agentless, YAML, massive ecosystem
2. **Idempotency is non-negotiable** - Production safety requires it
3. **Dynamic inventory mandatory for cloud** - Static won't scale
4. **Secrets management critical** - ansible-vault minimum, Vault preferred
5. **Testing before production** - Molecule + ansible-lint required
6. **Collections replacing roles** - Distribution and versioning
7. **GitOps integration** - Configuration in Git, automated deployment

---

## Configuration Management Taxonomy

### Configuration Management Hierarchy

```
Configuration Management
│
├── Provisioning (NOT this skill - see infrastructure-as-code)
│   ├── Terraform - Infrastructure creation
│   ├── CloudFormation - AWS resources
│   └── Pulumi - Multi-cloud provisioning
│
├── Configuration (THIS SKILL)
│   ├── Ansible - Agentless, YAML, push/pull
│   ├── Chef - Agent-based, Ruby, pull
│   └── Puppet - Agent-based, DSL, pull
│
├── Orchestration (Partial overlap)
│   ├── Ansible - Application deployment
│   ├── Kubernetes - Container orchestration (see kubernetes-operations)
│   └── Docker Compose - Local development
│
└── GitOps (Integration pattern)
    ├── ArgoCD - Kubernetes GitOps
    ├── Flux - Kubernetes GitOps
    └── Ansible + Git - Server configuration GitOps
```

### Ansible Component Taxonomy

```
Ansible
│
├── Inventory
│   ├── Static (INI/YAML files)
│   ├── Dynamic (Scripts/Plugins)
│   │   ├── AWS EC2
│   │   ├── Azure
│   │   ├── GCP
│   │   ├── VMware
│   │   └── Custom scripts
│   └── Hybrid (Static + Dynamic)
│
├── Playbooks
│   ├── Tasks (ordered actions)
│   ├── Handlers (triggered on change)
│   ├── Variables (parameterization)
│   ├── Templates (Jinja2)
│   ├── Tags (selective execution)
│   └── Pre/Post Tasks (validation)
│
├── Roles
│   ├── Directory Structure
│   │   ├── defaults/ (default variables)
│   │   ├── vars/ (override variables)
│   │   ├── tasks/ (main task list)
│   │   ├── handlers/ (change handlers)
│   │   ├── templates/ (Jinja2 templates)
│   │   ├── files/ (static files)
│   │   ├── meta/ (role metadata)
│   │   └── tests/ (role tests)
│   └── Best Practices
│       ├── Single responsibility
│       ├── Reusability
│       ├── Parameterization
│       └── Documentation
│
├── Collections
│   ├── Roles (bundled roles)
│   ├── Modules (custom modules)
│   ├── Plugins (custom plugins)
│   └── Documentation
│
├── Modules
│   ├── Core Modules (ansible.builtin)
│   │   ├── file, copy, template
│   │   ├── service, systemd
│   │   ├── user, group
│   │   ├── package, apt, yum
│   │   └── command, shell, script
│   ├── Cloud Modules
│   │   ├── aws_* (EC2, S3, RDS)
│   │   ├── azure_* (VMs, Storage)
│   │   └── gcp_* (Compute, Storage)
│   └── Custom Modules (Python)
│
├── Secrets Management
│   ├── ansible-vault (built-in)
│   │   ├── Encrypt files
│   │   ├── Encrypt strings
│   │   └── Vault IDs
│   └── HashiCorp Vault (integration)
│       ├── KV secrets
│       ├── Dynamic credentials
│       └── Token authentication
│
└── Testing
    ├── ansible-lint (linting)
    ├── Molecule (role testing)
    │   ├── Docker driver
    │   ├── Podman driver
    │   └── VM drivers
    ├── Testinfra (verification)
    └── Check mode (dry-run)
```

### Configuration Patterns Taxonomy

**By Idempotency:**
- **Declarative:** Define desired state (preferred)
- **Imperative:** Define procedural steps (avoid)

**By Execution Model:**
- **Push:** Control node pushes to managed nodes (Ansible default)
- **Pull:** Managed nodes pull from control node (Ansible-pull, Chef, Puppet)

**By Architecture:**
- **Agentless:** SSH/WinRM (Ansible)
- **Agent-based:** Installed agent (Chef, Puppet)

**By Scope:**
- **Host configuration:** OS settings, packages, users
- **Application deployment:** Code, dependencies, configs
- **Service orchestration:** Multi-host coordination

---

## Decision Framework

### When to Use Configuration Management

**Use configuration management when:**
- ✅ Managing server/VM configurations
- ✅ Ensuring compliance (CIS benchmarks, PCI-DSS)
- ✅ Deploying applications to servers/VMs
- ✅ Standardizing environments (dev, staging, prod)
- ✅ Automating operational tasks (backups, updates)
- ✅ Managing cloud resources post-provisioning

**Don't use configuration management for:**
- ❌ Creating cloud infrastructure (use IaC tools)
- ❌ Container orchestration (use Kubernetes)
- ❌ CI/CD pipelines (use Jenkins/GitHub Actions)
- ❌ Immutable infrastructure (use image baking)

### Tool Selection: Ansible vs Chef vs Puppet

```
Decision Tree:
│
├── New project / greenfield?
│   └── YES → Ansible (easiest, modern, agentless)
│
├── Existing Chef/Puppet?
│   ├── Working well? → Keep it (don't migrate for no reason)
│   └── Pain points? → Migrate to Ansible (assess effort)
│
├── Windows-heavy environment?
│   ├── Mostly Windows → Puppet (best Windows support) OR Ansible (WinRM)
│   └── Mixed → Ansible (handles both)
│
├── Compliance-critical enterprise?
│   ├── Need compliance tools → Puppet (Remediate) OR Ansible (custom)
│   └── Standard compliance → Ansible (sufficient)
│
├── Large team, complex organization?
│   ├── Need enterprise support → Red Hat Ansible Automation Platform
│   └── Open source sufficient → Ansible (community)
│
└── Cloud-native / containers?
    └── YES → Ansible (best cloud integration, agentless)
```

### Ansible vs Infrastructure-as-Code

**Use Ansible when:**
- Configuring resources AFTER provisioning
- Deploying applications
- Managing OS-level settings
- Orchestrating multi-step workflows

**Use Terraform/IaC when:**
- Creating cloud infrastructure
- Managing resource lifecycle
- Defining infrastructure state
- Multi-cloud resource orchestration

**Best Practice:** Terraform provisions, Ansible configures

**Example workflow:**
1. Terraform creates AWS EC2 instances, security groups, load balancers
2. Terraform outputs instance IPs to Ansible inventory
3. Ansible configures OS, installs packages, deploys application
4. Ansible sets up monitoring, backups, cron jobs

### Static vs Dynamic Inventory

```
Decision Matrix:

Static Inventory:
├── Small environment (<50 hosts)
├── Stable infrastructure (rarely changes)
├── On-premises servers
└── Simple host grouping

Dynamic Inventory:
├── Large environment (>50 hosts)
├── Cloud-based (AWS, Azure, GCP)
├── Frequent scaling (auto-scaling groups)
├── Multi-cloud or hybrid
└── Source of truth in external system (NetBox, CMDB)

Hybrid Inventory:
├── Some static hosts (on-prem)
├── Some dynamic hosts (cloud)
└── Unified management
```

---

## Ansible Patterns

### Playbook Structure Pattern

```yaml
---
# site.yml - Main playbook
- name: Configure web servers
  hosts: webservers
  become: yes

  vars:
    nginx_version: "1.24"
    app_port: 8080

  pre_tasks:
    - name: Update package cache
      apt:
        update_cache: yes
        cache_valid_time: 3600
      when: ansible_os_family == "Debian"

  roles:
    - common
    - nginx
    - application

  tasks:
    - name: Ensure application is running
      service:
        name: myapp
        state: started
        enabled: yes

  handlers:
    - name: Restart nginx
      service:
        name: nginx
        state: restarted

  post_tasks:
    - name: Verify application responds
      uri:
        url: "http://localhost:{{ app_port }}/health"
        status_code: 200
      retries: 3
      delay: 5
```

**Best Practices:**
- One playbook per application/service tier
- Use `pre_tasks` for system prep (package updates)
- Use `roles` for reusable configuration
- Use `tasks` for playbook-specific actions
- Use `post_tasks` for verification
- Always include verification tasks

### Role Structure Pattern

```
roles/nginx/
├── defaults/
│   └── main.yml          # Default variables (lowest precedence)
├── vars/
│   └── main.yml          # Override variables (high precedence)
├── tasks/
│   ├── main.yml          # Main task entry point
│   ├── install.yml       # Installation tasks
│   ├── configure.yml     # Configuration tasks
│   └── security.yml      # Security hardening
├── handlers/
│   └── main.yml          # Change handlers (restart, reload)
├── templates/
│   ├── nginx.conf.j2     # Main config template
│   └── site.conf.j2      # Site config template
├── files/
│   └── ssl/              # Static SSL certificates
├── meta/
│   └── main.yml          # Role metadata (dependencies)
└── tests/
    ├── test.yml          # Test playbook
    └── inventory         # Test inventory
```

**defaults/main.yml:**
```yaml
---
# Default variables (can be overridden)
nginx_version: "1.24"
nginx_user: www-data
nginx_worker_processes: auto
nginx_worker_connections: 1024
nginx_enable_ssl: false
nginx_ssl_protocols: "TLSv1.2 TLSv1.3"
```

**tasks/main.yml:**
```yaml
---
# Main task file - orchestrates subtasks
- name: Include installation tasks
  include_tasks: install.yml

- name: Include configuration tasks
  include_tasks: configure.yml

- name: Include security hardening
  include_tasks: security.yml
  when: nginx_security_hardening | default(true)
```

**tasks/install.yml:**
```yaml
---
# Installation tasks (idempotent)
- name: Ensure NGINX is installed
  package:
    name: nginx
    state: present
  notify: Restart nginx

- name: Ensure NGINX service is enabled
  service:
    name: nginx
    enabled: yes
```

**handlers/main.yml:**
```yaml
---
# Handlers (triggered on change)
- name: Restart nginx
  service:
    name: nginx
    state: restarted

- name: Reload nginx
  service:
    name: nginx
    state: reloaded

- name: Validate nginx config
  command: nginx -t
  changed_when: false
```

### Idempotency Patterns

**Pattern 1: Use Idempotent Modules**

```yaml
# BAD - Not idempotent (runs every time)
- name: Install package
  command: apt-get install -y nginx

# GOOD - Idempotent (only installs if missing)
- name: Ensure nginx is installed
  apt:
    name: nginx
    state: present
```

**Pattern 2: Check Before Action**

```yaml
# Check if action needed
- name: Check if config exists
  stat:
    path: /etc/myapp/config.yml
  register: config_file

- name: Create config only if missing
  template:
    src: config.yml.j2
    dest: /etc/myapp/config.yml
  when: not config_file.stat.exists
```

**Pattern 3: Handlers for Side Effects**

```yaml
# Only restart if config changed
tasks:
  - name: Update nginx config
    template:
      src: nginx.conf.j2
      dest: /etc/nginx/nginx.conf
    notify: Restart nginx

handlers:
  - name: Restart nginx
    service:
      name: nginx
      state: restarted
```

**Pattern 4: Conditional Execution**

```yaml
# Only run on specific OS
- name: Install package on Debian
  apt:
    name: nginx
    state: present
  when: ansible_os_family == "Debian"

# Only run if variable defined
- name: Configure SSL
  template:
    src: ssl.conf.j2
    dest: /etc/nginx/ssl.conf
  when: nginx_enable_ssl | default(false)
```

### Inventory Patterns

**Static Inventory (INI format):**

```ini
# inventory/production

[webservers]
web1.example.com ansible_host=10.0.1.10
web2.example.com ansible_host=10.0.1.11
web3.example.com ansible_host=10.0.1.12

[databases]
db1.example.com ansible_host=10.0.2.10
db2.example.com ansible_host=10.0.2.11

[loadbalancers]
lb1.example.com ansible_host=10.0.3.10

# Group variables
[webservers:vars]
nginx_worker_processes=4
app_env=production

[databases:vars]
postgres_version=15
postgres_max_connections=200

# Parent groups
[production:children]
webservers
databases
loadbalancers

[production:vars]
ansible_user=deploy
ansible_become=yes
```

**Static Inventory (YAML format):**

```yaml
# inventory/production.yml
all:
  children:
    production:
      children:
        webservers:
          hosts:
            web1.example.com:
              ansible_host: 10.0.1.10
            web2.example.com:
              ansible_host: 10.0.1.11
            web3.example.com:
              ansible_host: 10.0.1.12
          vars:
            nginx_worker_processes: 4
            app_env: production

        databases:
          hosts:
            db1.example.com:
              ansible_host: 10.0.2.10
            db2.example.com:
              ansible_host: 10.0.2.11
          vars:
            postgres_version: 15
            postgres_max_connections: 200

        loadbalancers:
          hosts:
            lb1.example.com:
              ansible_host: 10.0.3.10

      vars:
        ansible_user: deploy
        ansible_become: yes
```

**Dynamic Inventory (AWS EC2):**

```yaml
# inventory/aws_ec2.yml
plugin: aws_ec2
regions:
  - us-east-1
  - us-west-2

filters:
  tag:Environment: production
  instance-state-name: running

keyed_groups:
  # Group by tag
  - key: tags.Role
    prefix: role
  # Group by instance type
  - key: instance_type
    prefix: type
  # Group by availability zone
  - key: placement.availability_zone
    prefix: az

hostnames:
  - tag:Name
  - private-ip-address

compose:
  ansible_host: private_ip_address
```

**Usage:**
```bash
# List dynamic inventory
ansible-inventory -i inventory/aws_ec2.yml --list

# Run playbook with dynamic inventory
ansible-playbook -i inventory/aws_ec2.yml site.yml
```

### Variable Precedence Pattern

**Ansible variable precedence (lowest to highest):**

1. Role defaults (`roles/nginx/defaults/main.yml`)
2. Inventory file vars (`inventory/production`)
3. Inventory `group_vars/all`
4. Inventory `group_vars/webservers`
5. Inventory `host_vars/web1.example.com`
6. Playbook `vars`
7. Playbook `vars_files`
8. Role `vars` (`roles/nginx/vars/main.yml`)
9. Command-line `-e` extra vars

**Best Practice Structure:**

```
project/
├── inventory/
│   ├── production
│   └── staging
├── group_vars/
│   ├── all/
│   │   ├── common.yml       # Variables for ALL hosts
│   │   └── vault.yml        # Encrypted secrets for ALL
│   ├── webservers/
│   │   ├── nginx.yml        # Webserver-specific vars
│   │   └── vault.yml        # Webserver secrets
│   └── databases/
│       ├── postgres.yml     # Database-specific vars
│       └── vault.yml        # Database secrets
└── host_vars/
    └── web1.example.com/
        └── custom.yml       # Host-specific overrides
```

### Secret Management Patterns

**Pattern 1: ansible-vault (Built-in)**

```bash
# Create encrypted file
ansible-vault create group_vars/all/vault.yml

# Edit encrypted file
ansible-vault edit group_vars/all/vault.yml

# Encrypt existing file
ansible-vault encrypt sensitive.yml

# Decrypt file
ansible-vault decrypt sensitive.yml

# View encrypted file
ansible-vault view group_vars/all/vault.yml
```

**vault.yml content:**
```yaml
---
# Encrypted variables
vault_database_password: "SuperSecretPassword123"
vault_api_key: "sk-abcdef123456"
vault_ssl_private_key: |
  -----BEGIN PRIVATE KEY-----
  MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...
  -----END PRIVATE KEY-----
```

**Reference in playbook:**
```yaml
# group_vars/all/vars.yml (unencrypted)
database_user: appuser
database_host: db.example.com
database_password: "{{ vault_database_password }}"

# Playbook
- name: Configure database connection
  template:
    src: database.conf.j2
    dest: /etc/myapp/database.conf
  vars:
    db_password: "{{ database_password }}"
```

**Run with vault:**
```bash
# Prompt for password
ansible-playbook site.yml --ask-vault-pass

# Use password file
ansible-playbook site.yml --vault-password-file ~/.vault_pass

# Multiple vault IDs
ansible-playbook site.yml --vault-id prod@~/.vault_pass_prod
```

**Pattern 2: HashiCorp Vault Integration**

```yaml
# Lookup from Vault
- name: Fetch secret from HashiCorp Vault
  set_fact:
    db_password: "{{ lookup('community.hashi_vault.vault_kv2_get', 'secret/data/myapp/database').secret.password }}"

# Use in task
- name: Configure app with Vault secret
  template:
    src: config.yml.j2
    dest: /etc/myapp/config.yml
  vars:
    database_password: "{{ db_password }}"
```

### Template Pattern (Jinja2)

```jinja2
{# templates/nginx.conf.j2 #}
user {{ nginx_user }};
worker_processes {{ nginx_worker_processes }};
pid /run/nginx.pid;

events {
    worker_connections {{ nginx_worker_connections }};
}

http {
    # Basic settings
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # Logging
    access_log {{ nginx_access_log | default('/var/log/nginx/access.log') }};
    error_log {{ nginx_error_log | default('/var/log/nginx/error.log') }};

    # SSL Settings
    {% if nginx_enable_ssl %}
    ssl_protocols {{ nginx_ssl_protocols }};
    ssl_prefer_server_ciphers on;
    {% endif %}

    # Virtual Hosts
    {% for site in nginx_sites %}
    server {
        listen {{ site.port | default(80) }};
        server_name {{ site.server_name }};
        root {{ site.root }};

        {% if site.ssl | default(false) %}
        ssl_certificate {{ site.ssl_cert }};
        ssl_certificate_key {{ site.ssl_key }};
        {% endif %}

        location / {
            try_files $uri $uri/ =404;
        }
    }
    {% endfor %}
}
```

**Usage in task:**
```yaml
- name: Configure nginx
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    owner: root
    group: root
    mode: '0644'
  notify: Reload nginx
```

---

## Testing Patterns

### Ansible-Lint Pattern

**Installation:**
```bash
pip install ansible-lint
```

**Configuration (`.ansible-lint`):**
```yaml
---
# Exclude paths
exclude_paths:
  - .cache/
  - .git/
  - molecule/
  - venv/

# Enable specific rules
enable_list:
  - yaml
  - fqcn-builtins
  - no-handler

# Skip specific rules
skip_list:
  - name[casing]  # Allow flexible task naming

# Warn on specific rules
warn_list:
  - experimental
```

**Usage:**
```bash
# Lint all playbooks
ansible-lint

# Lint specific playbook
ansible-lint playbooks/webservers.yml

# Lint role
ansible-lint roles/nginx/

# Auto-fix issues
ansible-lint --fix
```

### Molecule Testing Pattern

**Installation:**
```bash
pip install molecule molecule-docker ansible-core
```

**Initialize role with Molecule:**
```bash
# Create new role with molecule
molecule init role my_role --driver-name docker

# Add molecule to existing role
cd roles/nginx
molecule init scenario default --driver-name docker
```

**Molecule structure:**
```
roles/nginx/
└── molecule/
    └── default/
        ├── molecule.yml       # Molecule config
        ├── converge.yml       # Test playbook
        ├── verify.yml         # Verification tasks
        └── prepare.yml        # Preparation tasks (optional)
```

**molecule.yml:**
```yaml
---
dependency:
  name: galaxy
  options:
    requirements-file: requirements.yml

driver:
  name: docker

platforms:
  - name: nginx-ubuntu
    image: ubuntu:22.04
    pre_build_image: true
    privileged: true
    command: /lib/systemd/systemd
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:ro

  - name: nginx-centos
    image: centos:stream9
    pre_build_image: true
    privileged: true
    command: /usr/sbin/init
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:ro

provisioner:
  name: ansible
  config_options:
    defaults:
      callbacks_enabled: ansible.posix.profile_tasks
  inventory:
    group_vars:
      all:
        nginx_worker_processes: 2

verifier:
  name: ansible

scenario:
  test_sequence:
    - dependency
    - cleanup
    - destroy
    - syntax
    - create
    - prepare
    - converge
    - idempotence
    - side_effect
    - verify
    - cleanup
    - destroy
```

**converge.yml (test playbook):**
```yaml
---
- name: Converge
  hosts: all
  become: true

  tasks:
    - name: Include nginx role
      include_role:
        name: nginx
      vars:
        nginx_worker_processes: 4
        nginx_enable_ssl: false
```

**verify.yml (verification):**
```yaml
---
- name: Verify
  hosts: all
  gather_facts: false

  tasks:
    - name: Check nginx is installed
      package:
        name: nginx
        state: present
      check_mode: yes
      register: nginx_installed
      failed_when: nginx_installed is changed

    - name: Check nginx service is running
      service:
        name: nginx
        state: started
      check_mode: yes
      register: nginx_running
      failed_when: nginx_running is changed

    - name: Verify nginx responds
      uri:
        url: http://localhost:80
        status_code: 200
      retries: 3
      delay: 2
```

**Molecule workflow:**
```bash
# Full test sequence
molecule test

# Create instances
molecule create

# Apply role
molecule converge

# Verify configuration
molecule verify

# Test idempotence (run twice, should have no changes)
molecule idempotence

# Destroy instances
molecule destroy

# Test specific platform
molecule test --platform-name nginx-ubuntu
```

### Check Mode (Dry Run) Pattern

```bash
# Dry run (show what would change)
ansible-playbook site.yml --check

# Dry run with diff output
ansible-playbook site.yml --check --diff

# Limit to specific hosts
ansible-playbook site.yml --check --limit webservers
```

**In playbook:**
```yaml
# Task always runs in check mode
- name: Validate config syntax
  command: nginx -t
  check_mode: yes
  changed_when: false

# Task never runs in check mode
- name: Restart service
  service:
    name: nginx
    state: restarted
  check_mode: no
```

---

## Tool Recommendations

### Recommended Tools & Libraries (2025)

#### **Primary: Ansible** (Configuration Management)

**Library:** `/websites/ansible_ansible`
**Trust Score:** High
**Code Snippets:** 65,664+
**Benchmark Score:** 81.6

**Why Ansible?**
- Agentless architecture (SSH/WinRM)
- YAML syntax (easiest learning curve)
- Massive module ecosystem (5,000+ modules)
- Strong cloud integration (AWS, Azure, GCP)
- Active community and Red Hat support

**When to Use:**
- Any server/VM configuration task
- Application deployment
- Cloud resource configuration
- Hybrid/multi-cloud environments
- Teams new to configuration management

**Installation:**
```bash
# pip (recommended)
pip install ansible

# Homebrew (macOS)
brew install ansible

# apt (Ubuntu/Debian)
sudo apt update
sudo apt install ansible

# dnf (RHEL/CentOS)
sudo dnf install ansible
```

**Example - Simple Playbook:**
```yaml
---
- name: Configure web servers
  hosts: webservers
  become: yes

  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present

    - name: Start nginx
      service:
        name: nginx
        state: started
        enabled: yes
```

---

#### **Testing: Ansible Lint** (Quality Checking)

**Library:** `/ansible/ansible-lint`
**Trust Score:** High
**Code Snippets:** 445+

**Why Ansible Lint?**
- Catches common mistakes before production
- Enforces best practices
- Customizable rules
- CI/CD integration

**When to Use:**
- Before committing playbooks
- In CI/CD pipelines
- During code review

**Installation:**
```bash
pip install ansible-lint
```

**Example:**
```bash
# Lint all playbooks
ansible-lint

# Auto-fix issues
ansible-lint --fix
```

---

#### **Testing: Molecule** (Role Testing)

**Library:** `/websites/ansible_readthedocs_io-projects-molecule`
**Trust Score:** High
**Code Snippets:** 202+

**Why Molecule?**
- Test roles in isolated environments
- Multiple OS/platform testing
- Idempotence verification
- Docker/Podman integration

**When to Use:**
- Developing reusable roles
- Testing against multiple OS distributions
- Validating idempotence
- Pre-production verification

**Installation:**
```bash
pip install molecule molecule-docker
```

**Example:**
```bash
# Full test cycle
molecule test

# Test idempotence
molecule idempotence
```

---

#### **Alternative: Chef** (Legacy Enterprise)

**Architecture:** Agent-based, Ruby DSL
**Best For:** Existing Chef deployments, complex hybrid cloud

**When to Consider:**
- Already using Chef (migration cost high)
- Need Chef-specific tools (InSpec)
- Ruby expertise on team

**When to Avoid:**
- New projects (Ansible simpler)
- Small teams (learning curve steep)
- Cloud-native (Ansible better integration)

---

#### **Alternative: Puppet** (Enterprise Compliance)

**Architecture:** Agent-based, Puppet DSL
**Best For:** Compliance-heavy enterprises, large Windows environments

**When to Consider:**
- Strong compliance requirements
- Existing Puppet infrastructure
- Large Windows deployments

**When to Avoid:**
- New projects (Ansible simpler)
- Cloud-native (agentless better)
- Small-to-medium environments

---

### Tool Comparison Matrix

| Tool | Architecture | Language | Learning Curve | Cloud Integration | Best For |
|------|-------------|----------|----------------|-------------------|----------|
| **Ansible** | Agentless (SSH) | YAML | ⭐⭐⭐⭐⭐ Easy | ⭐⭐⭐⭐⭐ Excellent | Most use cases |
| **Chef** | Agent-based | Ruby DSL | ⭐⭐ Steep | ⭐⭐⭐ Good | Hybrid cloud, Ruby teams |
| **Puppet** | Agent-based | Puppet DSL | ⭐⭐⭐ Moderate | ⭐⭐⭐ Good | Compliance, Windows |
| **Terraform** | Agentless | HCL | ⭐⭐⭐⭐ Easy | ⭐⭐⭐⭐⭐ Excellent | Provisioning (not config) |

---

### Recommendations by Use Case

**Small-to-Medium Environments (< 100 hosts):**
- **Primary:** Ansible
- **Testing:** ansible-lint (CI/CD)
- **Secrets:** ansible-vault

**Large Environments (> 100 hosts):**
- **Primary:** Ansible with dynamic inventory
- **Testing:** Molecule + ansible-lint
- **Secrets:** HashiCorp Vault
- **Platform:** Red Hat Ansible Automation Platform (enterprise support)

**Cloud-Native / Multi-Cloud:**
- **Primary:** Ansible
- **Inventory:** Dynamic (aws_ec2, azure_rm, gcp_compute)
- **Integration:** Terraform (provision) → Ansible (configure)

**Compliance-Heavy:**
- **Primary:** Ansible or Puppet
- **Testing:** Molecule + compliance test suites
- **Auditing:** InSpec (Chef) or custom Ansible checks

**Windows Environments:**
- **Primary:** Ansible (WinRM) or Puppet
- **Modules:** ansible.windows collection
- **Authentication:** Kerberos or NTLM

---

## Skill Structure Design

### SKILL.md Structure (500 lines max)

```markdown
---
name: configuration-management
description: Guides users through creating, managing, and testing server configuration automation using Ansible, including playbooks, roles, inventory, secrets, and testing with Molecule. Covers idempotency patterns, dynamic inventory for cloud, and GitOps workflows.
---

# Configuration Management Skill

## Purpose
[2-3 sentences on what this skill does]

## When to Use
[Trigger scenarios]

## Quick Start
[Minimal example to get started]

## Core Concepts
1. Idempotency
2. Inventory Management
3. Playbooks vs Roles
4. Secret Management

## Common Workflows

### Workflow 1: Create Ansible Playbook
[Step-by-step guide with references to detailed docs]

### Workflow 2: Test Role with Molecule
[Step-by-step guide with references]

### Workflow 3: Manage Secrets
[Step-by-step guide with references]

## Tool Selection
[Quick decision tree - see reference/decision-framework.md]

## Troubleshooting
[Common issues - see reference/troubleshooting.md]

## References
- reference/playbook-patterns.md
- reference/role-structure.md
- reference/inventory-management.md
- reference/secrets-management.md
- reference/testing-guide.md
- reference/decision-framework.md
- scripts/validate-playbook.py
- scripts/generate-inventory.py
```

### Bundled Resources Structure

```
configuration-management/
├── SKILL.md                           # Main skill file (500 lines)
│
├── reference/                         # Detailed documentation
│   ├── playbook-patterns.md          # Playbook best practices
│   ├── role-structure.md             # Role directory layout
│   ├── inventory-management.md       # Static/dynamic inventory
│   ├── secrets-management.md         # ansible-vault, HashiCorp Vault
│   ├── testing-guide.md              # Molecule, ansible-lint
│   ├── idempotency-guide.md          # Ensuring idempotent playbooks
│   ├── decision-framework.md         # When to use what tool
│   ├── chef-puppet-migration.md      # Migrating to Ansible
│   └── troubleshooting.md            # Common issues
│
├── examples/                          # Code examples
│   ├── playbooks/
│   │   ├── simple-webserver.yml      # Basic playbook
│   │   ├── multi-tier-app.yml        # Complex playbook
│   │   └── with-vault.yml            # Using secrets
│   ├── roles/
│   │   ├── nginx/                    # Complete role example
│   │   └── postgres/                 # Database role example
│   ├── inventory/
│   │   ├── static-ini/               # INI format inventory
│   │   ├── static-yaml/              # YAML format inventory
│   │   └── dynamic-aws/              # AWS EC2 dynamic inventory
│   └── molecule/
│       └── nginx-test/               # Molecule test scenario
│
├── scripts/                           # Utility scripts
│   ├── validate-playbook.py          # Validate playbook syntax
│   ├── generate-inventory.py         # Generate inventory from cloud
│   ├── ansible-vault-helper.sh       # Vault management helper
│   └── molecule-runner.sh            # Run Molecule tests
│
└── assets/                            # Templates and schemas
    ├── role-template/                # ansible-galaxy init template
    ├── molecule-template/            # Molecule scenario template
    └── playbook-schema.json          # JSON schema for validation
```

### Progressive Disclosure Strategy

**Level 1: SKILL.md (Always Loaded)**
- Quick start examples
- Common workflows
- References to detailed docs

**Level 2: Reference Files (Loaded on Demand)**
- `reference/playbook-patterns.md` - When user asks about playbooks
- `reference/role-structure.md` - When user creates roles
- `reference/inventory-management.md` - When user manages inventory
- `reference/secrets-management.md` - When user handles secrets
- `reference/testing-guide.md` - When user wants to test

**Level 3: Examples (Loaded When Needed)**
- `examples/playbooks/` - Copy-paste examples
- `examples/roles/` - Complete role templates
- `examples/molecule/` - Testing scaffolds

**Level 4: Scripts (Executed, Not Loaded)**
- `scripts/validate-playbook.py` - Run validation
- `scripts/generate-inventory.py` - Generate inventory
- Zero token cost (output only consumed)

### Writing Style

**Imperative/Infinitive Form (NOT second person):**

✅ **Good:**
- "To create a playbook, use YAML syntax..."
- "Reference role-structure.md for directory layout..."
- "Run Molecule tests before production deployment..."
- "Ensure idempotency by using state parameters..."

❌ **Bad:**
- "You should create a playbook using YAML..."
- "If you want to test your role, you can use Molecule..."
- "When you're ready, you should run tests..."

---

## Integration Points

### With Other Skills

**infrastructure-as-code:**
- Terraform provisions infrastructure
- Ansible configures resources post-provisioning
- Terraform outputs feed Ansible inventory

**kubernetes-operations:**
- Ansible deploys K8s clusters (kubespray)
- Kubernetes handles container config
- Ansible manages node configuration

**building-ci-pipelines:**
- CI/CD runs ansible-lint
- Molecule tests in pipeline
- Deployment stage runs playbooks

**secret-management:**
- ansible-vault for simple secrets
- HashiCorp Vault for advanced secrets
- Both integrated via lookups

**security-hardening:**
- Ansible applies CIS benchmarks
- Security roles enforce compliance
- Molecule verifies hardening

**testing-strategies:**
- Molecule for role testing
- Testinfra for verification
- Integration test suites

### External Tool Integration

**Version Control (Git):**
```bash
# Standard repository structure
project/
├── .git/
├── .gitignore
├── ansible.cfg
├── playbooks/
├── roles/
├── inventory/
└── group_vars/
```

**CI/CD (GitHub Actions example):**
```yaml
# .github/workflows/ansible-lint.yml
name: Ansible Lint
on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run ansible-lint
        uses: ansible/ansible-lint-action@v6
        with:
          path: "playbooks/"
```

**Cloud Providers:**
- AWS: `aws_ec2` inventory plugin
- Azure: `azure_rm` inventory plugin
- GCP: `gcp_compute` inventory plugin

**Terraform Integration:**
```hcl
# Terraform outputs for Ansible
output "web_servers" {
  value = {
    for instance in aws_instance.web :
    instance.tags.Name => instance.private_ip
  }
}

# Generate Ansible inventory
resource "local_file" "ansible_inventory" {
  content = templatefile("inventory.tpl", {
    web_servers = aws_instance.web
  })
  filename = "../ansible/inventory/terraform.yml"
}
```

---

## Implementation Roadmap

### Phase 1: Core Skill (Week 1)

**Deliverables:**
- [ ] SKILL.md (main file, 500 lines)
- [ ] reference/playbook-patterns.md
- [ ] reference/role-structure.md
- [ ] reference/inventory-management.md
- [ ] examples/playbooks/simple-webserver.yml
- [ ] examples/roles/nginx/

**Focus:** Get users productive quickly with Ansible

### Phase 2: Testing & Quality (Week 2)

**Deliverables:**
- [ ] reference/testing-guide.md (Molecule + ansible-lint)
- [ ] reference/idempotency-guide.md
- [ ] examples/molecule/nginx-test/
- [ ] scripts/validate-playbook.py
- [ ] scripts/molecule-runner.sh

**Focus:** Ensure production-ready configurations

### Phase 3: Secrets & Security (Week 3)

**Deliverables:**
- [ ] reference/secrets-management.md
- [ ] examples/playbooks/with-vault.yml
- [ ] scripts/ansible-vault-helper.sh
- [ ] Integration with HashiCorp Vault examples

**Focus:** Secure credential management

### Phase 4: Advanced Patterns (Week 4)

**Deliverables:**
- [ ] reference/decision-framework.md
- [ ] reference/chef-puppet-migration.md
- [ ] reference/troubleshooting.md
- [ ] examples/inventory/dynamic-aws/
- [ ] scripts/generate-inventory.py

**Focus:** Advanced use cases and migration paths

### Phase 5: Polish & Testing (Week 5)

**Deliverables:**
- [ ] Validation script testing
- [ ] Example playbook verification
- [ ] Documentation review
- [ ] Integration testing with other skills
- [ ] README and contributor guide

**Focus:** Production readiness

---

## Success Metrics

**Skill effectiveness measured by:**

1. **User can create playbook in < 5 minutes**
   - Quick start example works immediately
   - Clear path from example to custom playbook

2. **Idempotency achieved without explicit teaching**
   - Examples use idempotent patterns
   - Users naturally adopt best practices

3. **Testing integrated early**
   - Molecule introduced in core workflows
   - ansible-lint runs before deployment

4. **Secrets managed securely**
   - No plaintext credentials in examples
   - ansible-vault or HashiCorp Vault used

5. **Dynamic inventory adopted for cloud**
   - AWS/Azure examples work out-of-box
   - Clear migration from static to dynamic

---

## Appendix: Research Sources

### Google Search Grounding Sources

**Ansible Best Practices:**
- gocodeo.com - Ansible playbook best practices 2025
- moldstud.com - Role and collection organization
- github.io - Community best practices
- cloudmylab.com - Enterprise patterns

**Tool Comparison:**
- devopsroles.com - Ansible vs Chef vs Puppet comparison
- automq.com - Configuration management tools 2025
- attuneops.io - Tool selection guide
- dev.to - Practical tool experiences
- betterstack.com - DevOps tool reviews

**Idempotency & Inventory:**
- ansible.com - Official idempotency docs
- medium.com - Dynamic inventory patterns
- devops.dev - Best practices compilation
- centlinux.com - Practical guides
- spacelift.io - Infrastructure automation

### Context7 Libraries

**Ansible Core:**
- Library: `/websites/ansible_ansible`
- Trust: High, Snippets: 65,664+, Score: 81.6
- Coverage: Comprehensive documentation

**Ansible Lint:**
- Library: `/ansible/ansible-lint`
- Trust: High, Snippets: 445+
- Purpose: Quality checking

**Molecule:**
- Library: `/websites/ansible_readthedocs_io-projects-molecule`
- Trust: High, Snippets: 202+
- Purpose: Role testing framework

---

## Version History

**v1.0 (December 3, 2025):**
- Initial master plan
- Research completed (Google Search Grounding + Context7)
- Comprehensive Ansible focus with Chef/Puppet alternatives
- Testing patterns (Molecule, ansible-lint)
- Secret management (ansible-vault, HashiCorp Vault)
- Cloud-native inventory patterns

---

**End of init.md**

**Next Steps:**
1. Review and validate master plan
2. Begin SKILL.md implementation (Phase 1)
3. Create reference documentation
4. Develop example playbooks and roles
5. Build validation scripts
6. Test with real use cases
