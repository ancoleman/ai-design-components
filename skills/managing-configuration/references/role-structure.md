# Ansible Role Structure

## Table of Contents

1. [Role Directory Layout](#role-directory-layout)
2. [Creating Roles](#creating-roles)
3. [Role Components](#role-components)
4. [Best Practices](#best-practices)
5. [Role Dependencies](#role-dependencies)
6. [Collections](#collections)
7. [Testing Roles](#testing-roles)

---

## Role Directory Layout

### Standard Role Structure

```
roles/myapp/
├── defaults/
│   └── main.yml          # Default variables (lowest precedence)
├── vars/
│   └── main.yml          # Override variables (higher precedence)
├── tasks/
│   ├── main.yml          # Main task entry point
│   ├── install.yml       # Installation tasks
│   ├── configure.yml     # Configuration tasks
│   └── security.yml      # Security hardening
├── handlers/
│   └── main.yml          # Change handlers
├── templates/
│   ├── app.conf.j2       # Jinja2 templates
│   └── systemd.service.j2
├── files/
│   ├── app.tar.gz        # Static files
│   └── ssl/
│       └── ca.crt
├── meta/
│   └── main.yml          # Role metadata and dependencies
├── library/
│   └── custom_module.py  # Custom modules (optional)
├── module_utils/
│   └── helpers.py        # Shared module utilities (optional)
├── tests/
│   ├── test.yml          # Test playbook
│   └── inventory         # Test inventory
└── README.md             # Role documentation
```

### File Loading Order

1. `meta/main.yml` - Dependencies loaded first
2. `defaults/main.yml` - Default variables
3. `vars/main.yml` - Role variables
4. `tasks/main.yml` - Task execution begins
5. `handlers/main.yml` - Handlers registered
6. Templates and files loaded on demand

---

## Creating Roles

### Initialize Role with ansible-galaxy

```bash
# Create new role
ansible-galaxy init roles/myapp

# Create role with specific author
ansible-galaxy init roles/myapp --init-path roles/

# View role structure
tree roles/myapp
```

### Minimal Role Example

```
roles/nginx/
├── defaults/
│   └── main.yml
├── tasks/
│   └── main.yml
├── handlers/
│   └── main.yml
└── templates/
    └── nginx.conf.j2
```

**defaults/main.yml:**
```yaml
---
# Default variables
nginx_version: "1.24"
nginx_user: www-data
nginx_worker_processes: auto
nginx_worker_connections: 1024
nginx_enable_ssl: false
```

**tasks/main.yml:**
```yaml
---
- name: Install nginx
  apt:
    name: nginx
    state: present
  notify: Restart nginx

- name: Configure nginx
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  notify: Reload nginx

- name: Ensure nginx is running
  service:
    name: nginx
    state: started
    enabled: yes
```

**handlers/main.yml:**
```yaml
---
- name: Restart nginx
  service:
    name: nginx
    state: restarted

- name: Reload nginx
  service:
    name: nginx
    state: reloaded
```

### Using Roles in Playbooks

**Method 1: Roles section (recommended)**
```yaml
---
- name: Configure web servers
  hosts: webservers
  become: yes

  roles:
    - common
    - nginx
    - application
```

**Method 2: Include role task**
```yaml
---
- name: Configure web servers
  hosts: webservers
  become: yes

  tasks:
    - name: Apply nginx role
      include_role:
        name: nginx
```

**Method 3: Import role (static)**
```yaml
---
- name: Configure web servers
  hosts: webservers
  become: yes

  tasks:
    - name: Import nginx role
      import_role:
        name: nginx
```

**With variables:**
```yaml
---
- name: Configure web servers
  hosts: webservers
  become: yes

  roles:
    - role: nginx
      vars:
        nginx_worker_processes: 4
        nginx_enable_ssl: true
```

---

## Role Components

### defaults/main.yml

Define default variable values (can be overridden).

```yaml
---
# Application settings
app_name: myapp
app_version: "1.0.0"
app_port: 8080
app_user: appuser
app_group: appuser

# Installation settings
app_install_dir: /opt/{{ app_name }}
app_config_dir: /etc/{{ app_name }}
app_log_dir: /var/log/{{ app_name }}

# Feature flags
enable_monitoring: true
enable_backup: false

# Dependencies
app_dependencies:
  - python3
  - python3-pip
  - libpq-dev
```

### vars/main.yml

Define role variables (higher precedence than defaults).

```yaml
---
# OS-specific package names
_app_packages:
  Debian:
    - nginx
    - postgresql-client
  RedHat:
    - nginx
    - postgresql

app_packages: "{{ _app_packages[ansible_os_family] }}"

# Computed values
app_memory_limit: "{{ (ansible_memtotal_mb * 0.7) | int }}m"
app_workers: "{{ ansible_processor_vcpus }}"
```

### tasks/main.yml

Main task file - orchestrate task execution.

**Pattern 1: Single file (simple roles)**
```yaml
---
- name: Install application
  apt:
    name: myapp
    state: present

- name: Configure application
  template:
    src: app.conf.j2
    dest: /etc/myapp/app.conf
  notify: Restart myapp

- name: Start application
  service:
    name: myapp
    state: started
    enabled: yes
```

**Pattern 2: Include subtasks (complex roles)**
```yaml
---
- name: Include OS-specific variables
  include_vars: "{{ ansible_os_family }}.yml"

- name: Include pre-flight checks
  include_tasks: preflight.yml

- name: Include installation tasks
  include_tasks: install.yml

- name: Include configuration tasks
  include_tasks: configure.yml

- name: Include security hardening
  include_tasks: security.yml
  when: enable_security_hardening | default(true)
```

**tasks/install.yml:**
```yaml
---
- name: Create application user
  user:
    name: "{{ app_user }}"
    system: yes
    shell: /bin/false

- name: Install application packages
  apt:
    name: "{{ app_packages }}"
    state: present

- name: Create application directories
  file:
    path: "{{ item }}"
    state: directory
    owner: "{{ app_user }}"
    group: "{{ app_group }}"
    mode: '0755'
  loop:
    - "{{ app_install_dir }}"
    - "{{ app_config_dir }}"
    - "{{ app_log_dir }}"
```

### handlers/main.yml

Define handlers triggered by task changes.

```yaml
---
- name: Restart myapp
  service:
    name: myapp
    state: restarted

- name: Reload myapp
  service:
    name: myapp
    state: reloaded

- name: Validate config
  command: myapp validate-config /etc/myapp/app.conf
  changed_when: false

- name: Clear cache
  command: myapp clear-cache

# Listen pattern (multiple triggers)
- name: Update systemd
  systemd:
    daemon_reload: yes
  listen: Reload systemd
```

### templates/

Jinja2 templates for dynamic configuration files.

**templates/app.conf.j2:**
```jinja2
# {{ ansible_managed }}
# Application Configuration

[server]
port = {{ app_port }}
workers = {{ app_workers | default(4) }}
timeout = {{ app_timeout | default(30) }}

[logging]
level = {{ log_level | default('info') }}
path = {{ app_log_dir }}/app.log

{% if enable_monitoring %}
[monitoring]
enabled = true
metrics_port = {{ monitoring_port | default(9090) }}
{% endif %}

[database]
host = {{ db_host }}
port = {{ db_port }}
name = {{ db_name }}
user = {{ db_user }}
# Password stored in vault
```

**templates/systemd.service.j2:**
```jinja2
[Unit]
Description={{ app_name }} application
After=network.target

[Service]
Type=simple
User={{ app_user }}
Group={{ app_group }}
WorkingDirectory={{ app_install_dir }}
ExecStart={{ app_install_dir }}/bin/{{ app_name }} --config {{ app_config_dir }}/app.conf
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### files/

Static files copied without modification.

```
files/
├── ssl/
│   ├── ca.crt
│   └── dhparam.pem
├── scripts/
│   ├── backup.sh
│   └── healthcheck.sh
└── config/
    └── static.conf
```

**Usage:**
```yaml
- name: Copy SSL certificate
  copy:
    src: ssl/ca.crt
    dest: /etc/ssl/certs/ca.crt
    owner: root
    group: root
    mode: '0644'

- name: Deploy backup script
  copy:
    src: scripts/backup.sh
    dest: /usr/local/bin/backup.sh
    owner: root
    group: root
    mode: '0755'
```

### meta/main.yml

Role metadata and dependencies.

```yaml
---
galaxy_info:
  role_name: myapp
  author: Your Name
  description: Deploy and configure myapp application
  company: Example Corp

  license: MIT

  min_ansible_version: "2.12"

  platforms:
    - name: Ubuntu
      versions:
        - focal
        - jammy
    - name: Debian
      versions:
        - bullseye

  galaxy_tags:
    - application
    - web
    - deployment

dependencies:
  - role: common
  - role: postgresql
    vars:
      postgresql_version: "15"
  - role: nginx
    when: install_nginx | default(true)
```

---

## Best Practices

### 1. Single Responsibility

Each role should have one clear purpose.

**Good:**
```
roles/
├── nginx/         # Web server configuration
├── postgresql/    # Database configuration
├── redis/         # Cache configuration
└── myapp/         # Application deployment
```

**Bad:**
```
roles/
└── everything/    # Configures web, database, cache, app
```

### 2. Parameterize with Defaults

Provide sensible defaults, allow overrides.

```yaml
# defaults/main.yml
nginx_worker_processes: auto  # Sensible default
nginx_worker_connections: 1024
nginx_enable_ssl: false       # Safe default

# Allow override in playbook
- role: nginx
  vars:
    nginx_worker_processes: 8
    nginx_enable_ssl: true
```

### 3. Use Descriptive Variable Names

```yaml
# Good: Clear, scoped naming
nginx_worker_processes: 4
nginx_client_max_body_size: "10m"
nginx_ssl_protocols: "TLSv1.2 TLSv1.3"

# Bad: Vague, generic names
workers: 4
max_size: "10m"
protocols: "TLSv1.2 TLSv1.3"
```

### 4. Prefix Role Variables

Prevent variable collisions between roles.

```yaml
# Good: Role prefix
myapp_version: "1.0.0"
myapp_port: 8080
myapp_enable_ssl: true

# Bad: No prefix (conflicts possible)
version: "1.0.0"
port: 8080
enable_ssl: true
```

### 5. Organize Complex Tasks

Split large task files into logical units.

```yaml
# tasks/main.yml
- include_tasks: preflight.yml
- include_tasks: install.yml
- include_tasks: configure.yml
- include_tasks: security.yml
```

### 6. Document Role Usage

Create comprehensive README.md.

```markdown
# myapp Role

Deploy and configure myapp application.

## Requirements

- Ansible >= 2.12
- Ubuntu 20.04 or 22.04

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `app_version` | `1.0.0` | Application version |
| `app_port` | `8080` | Application port |
| `enable_ssl` | `false` | Enable SSL |

## Dependencies

- `common`
- `postgresql`

## Example Playbook

```yaml
- hosts: appservers
  roles:
    - role: myapp
      vars:
        app_version: "2.0.0"
        app_port: 9000
```

## License

MIT
```

### 7. Version Control

```
.gitignore:
*.retry
.vault_pass
.molecule/
```

### 8. Test Roles with Molecule

Use Molecule for automated role testing.

```bash
cd roles/myapp
molecule test
```

---

## Role Dependencies

### Define Dependencies in meta/main.yml

```yaml
---
dependencies:
  - role: common
  - role: postgresql
    vars:
      postgresql_version: "15"
      postgresql_databases:
        - name: myapp
          owner: myapp
  - role: nginx
    when: use_nginx_proxy | default(true)
```

### Dependency Resolution

Dependencies execute before the role itself.

**Execution order:**
1. `common` role (dependency)
2. `postgresql` role (dependency)
3. `nginx` role (dependency, if condition met)
4. `myapp` role (main role)

### Circular Dependencies

Avoid circular dependencies:

```yaml
# BAD: Circular dependency
# Role A depends on B
# Role B depends on A

# GOOD: Extract shared logic to separate role
roles/
├── base/        # Shared dependencies
├── roleA/       # Depends on base
└── roleB/       # Depends on base
```

---

## Collections

### Collection Structure

Collections bundle roles, modules, and plugins.

```
ansible_collections/
└── mycompany/
    └── myapp/
        ├── roles/
        │   ├── webserver/
        │   ├── database/
        │   └── monitoring/
        ├── plugins/
        │   ├── modules/
        │   └── inventory/
        ├── playbooks/
        └── galaxy.yml
```

### Create Collection

```bash
# Initialize collection
ansible-galaxy collection init mycompany.myapp

# Build collection
ansible-galaxy collection build

# Install collection
ansible-galaxy collection install mycompany-myapp-1.0.0.tar.gz
```

### galaxy.yml

```yaml
---
namespace: mycompany
name: myapp
version: 1.0.0
readme: README.md
authors:
  - Your Name <you@example.com>
description: MyApp deployment collection
license:
  - MIT
tags:
  - application
  - web
dependencies:
  community.general: ">=5.0.0"
  ansible.posix: ">=1.4.0"
```

### Use Collection in Playbook

```yaml
---
- name: Deploy application
  hosts: appservers
  collections:
    - mycompany.myapp

  roles:
    - webserver
    - database
    - monitoring
```

---

## Testing Roles

### Directory Structure

```
roles/myapp/
├── molecule/
│   └── default/
│       ├── molecule.yml
│       ├── converge.yml
│       └── verify.yml
└── tests/
    ├── test.yml
    └── inventory
```

### Simple Test Playbook

**tests/test.yml:**
```yaml
---
- name: Test myapp role
  hosts: localhost
  become: yes

  roles:
    - myapp

  post_tasks:
    - name: Verify service is running
      service:
        name: myapp
        state: started
      check_mode: yes
      register: service_check
      failed_when: service_check is changed
```

### Run Test

```bash
# Run test playbook
ansible-playbook tests/test.yml -i tests/inventory

# With Molecule
molecule test
```

Run automated tests to verify role functionality before production deployment.
