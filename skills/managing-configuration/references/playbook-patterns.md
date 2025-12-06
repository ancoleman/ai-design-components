# Ansible Playbook Patterns

## Table of Contents

1. [Playbook Structure](#playbook-structure)
2. [Task Organization](#task-organization)
3. [Handlers](#handlers)
4. [Variables](#variables)
5. [Templates](#templates)
6. [Tags](#tags)
7. [Conditional Execution](#conditional-execution)
8. [Loops](#loops)
9. [Error Handling](#error-handling)
10. [Best Practices](#best-practices)

---

## Playbook Structure

### Complete Playbook Anatomy

```yaml
---
# site.yml - Main playbook
- name: Configure web servers
  hosts: webservers
  become: yes
  gather_facts: yes

  vars:
    nginx_version: "1.24"
    app_port: 8080

  vars_files:
    - vars/common.yml
    - vars/webservers.yml

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
      tags: [service, application]

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

### Execution Order

1. **gather_facts** - Collect system information
2. **pre_tasks** - Preparation tasks (package cache updates, prerequisite checks)
3. **roles** - Execute role tasks in order
4. **tasks** - Playbook-specific tasks
5. **post_tasks** - Verification and cleanup
6. **handlers** - Triggered handlers (if notified)

---

## Task Organization

### Simple Task

```yaml
- name: Install nginx
  apt:
    name: nginx
    state: present
```

### Task with Multiple Parameters

```yaml
- name: Configure nginx
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    owner: root
    group: root
    mode: '0644'
    backup: yes
  notify: Reload nginx
```

### Include External Task Files

```yaml
# tasks/main.yml
- name: Include installation tasks
  include_tasks: install.yml

- name: Include configuration tasks
  include_tasks: configure.yml
  when: configure_app | default(true)
```

### Import Task Files (Static)

```yaml
# Evaluated at playbook parse time
- name: Import common tasks
  import_tasks: common.yml
```

### Block Tasks for Grouping

```yaml
- name: Configure application
  block:
    - name: Install dependencies
      apt:
        name: "{{ item }}"
        state: present
      loop: "{{ app_dependencies }}"

    - name: Deploy application
      copy:
        src: app.tar.gz
        dest: /opt/app/

  rescue:
    - name: Rollback deployment
      file:
        path: /opt/app
        state: absent

  always:
    - name: Log deployment attempt
      lineinfile:
        path: /var/log/deployments.log
        line: "Deployment attempted at {{ ansible_date_time.iso8601 }}"
```

---

## Handlers

### Basic Handler

```yaml
# tasks
- name: Update nginx config
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  notify: Restart nginx

# handlers
handlers:
  - name: Restart nginx
    service:
      name: nginx
      state: restarted
```

### Multiple Handlers

```yaml
- name: Update application config
  template:
    src: app.conf.j2
    dest: /etc/app/app.conf
  notify:
    - Validate config
    - Restart application
    - Clear cache

handlers:
  - name: Validate config
    command: app validate-config /etc/app/app.conf
    changed_when: false

  - name: Restart application
    service:
      name: myapp
      state: restarted

  - name: Clear cache
    command: app clear-cache
```

### Listen Handlers (Multiple Triggers)

```yaml
# tasks
- name: Update web config
  template:
    src: web.conf.j2
    dest: /etc/web/web.conf
  notify: Reload web services

- name: Update API config
  template:
    src: api.conf.j2
    dest: /etc/api/api.conf
  notify: Reload web services

# handlers
handlers:
  - name: Reload nginx
    service:
      name: nginx
      state: reloaded
    listen: Reload web services

  - name: Reload haproxy
    service:
      name: haproxy
      state: reloaded
    listen: Reload web services
```

### Force Handler Execution

```yaml
- name: Update critical config
  template:
    src: critical.conf.j2
    dest: /etc/app/critical.conf
  notify: Restart app

- name: Flush handlers now
  meta: flush_handlers

- name: Verify app started
  uri:
    url: http://localhost:8080/health
    status_code: 200
```

---

## Variables

### Variable Definition Locations

**Playbook vars:**
```yaml
- name: Configure app
  hosts: all
  vars:
    app_version: "2.1.0"
    app_port: 8080
```

**Vars files:**
```yaml
- name: Configure app
  hosts: all
  vars_files:
    - vars/common.yml
    - vars/{{ env }}.yml
```

**Inventory variables:**
```ini
# inventory/production
[webservers]
web1.example.com app_port=8080
web2.example.com app_port=8081

[webservers:vars]
app_version=2.1.0
```

**Group/Host vars:**
```
group_vars/
├── all/
│   └── common.yml
├── webservers/
│   └── nginx.yml
host_vars/
└── web1.example.com/
    └── custom.yml
```

### Variable Precedence (Lowest to Highest)

1. Role defaults
2. Inventory file vars
3. Inventory group_vars/all
4. Inventory group_vars/*
5. Inventory host_vars/*
6. Playbook vars
7. Playbook vars_files
8. Role vars
9. Block vars
10. Task vars
11. Command-line extra vars (`-e`)

### Register Variables

```yaml
- name: Check if config exists
  stat:
    path: /etc/app/app.conf
  register: config_file

- name: Create config if missing
  template:
    src: app.conf.j2
    dest: /etc/app/app.conf
  when: not config_file.stat.exists
```

### Set Facts

```yaml
- name: Set deployment timestamp
  set_fact:
    deployment_time: "{{ ansible_date_time.iso8601 }}"

- name: Use fact in later task
  lineinfile:
    path: /etc/app/version.txt
    line: "Deployed: {{ deployment_time }}"
```

---

## Templates

### Basic Jinja2 Template

```jinja2
{# templates/app.conf.j2 #}
# Application Configuration
app_version: {{ app_version }}
app_port: {{ app_port }}
log_level: {{ log_level | default('info') }}

{% if enable_debug %}
debug: true
{% endif %}
```

### Using Template

```yaml
- name: Deploy application config
  template:
    src: app.conf.j2
    dest: /etc/app/app.conf
    owner: app
    group: app
    mode: '0640'
  notify: Restart app
```

### Advanced Template (Loops)

```jinja2
{# templates/nginx.conf.j2 #}
http {
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

### Template with Filters

```jinja2
{# Common Jinja2 filters #}
{{ app_name | upper }}
{{ app_version | lower }}
{{ app_port | int }}
{{ config_value | default('fallback') }}
{{ sensitive_data | b64encode }}
{{ json_data | from_json }}
{{ list_data | join(',') }}
```

---

## Tags

### Define Tags

```yaml
- name: Install packages
  apt:
    name: nginx
    state: present
  tags: [install, packages]

- name: Configure services
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  tags: [config, nginx]

- name: Start services
  service:
    name: nginx
    state: started
  tags: [service, nginx]
```

### Run Specific Tags

```bash
# Run only install tasks
ansible-playbook site.yml --tags install

# Run multiple tags
ansible-playbook site.yml --tags "install,config"

# Skip tags
ansible-playbook site.yml --skip-tags service
```

### Special Tags

```yaml
# Always runs (unless explicitly skipped)
- name: Log execution
  debug:
    msg: "Playbook started"
  tags: [always]

# Never runs (unless explicitly included)
- name: Debug task
  debug:
    var: ansible_facts
  tags: [never, debug]
```

---

## Conditional Execution

### When Condition

```yaml
# OS family check
- name: Install package on Debian
  apt:
    name: nginx
    state: present
  when: ansible_os_family == "Debian"

# Multiple conditions (AND)
- name: Install on Ubuntu 22.04
  apt:
    name: nginx
    state: present
  when:
    - ansible_distribution == "Ubuntu"
    - ansible_distribution_version == "22.04"

# OR conditions
- name: Install on RedHat or CentOS
  yum:
    name: nginx
    state: present
  when: ansible_distribution in ["RedHat", "CentOS"]

# Variable defined check
- name: Configure SSL
  template:
    src: ssl.conf.j2
    dest: /etc/nginx/ssl.conf
  when: ssl_enabled is defined and ssl_enabled
```

### Register and Condition

```yaml
- name: Check service status
  command: systemctl is-active nginx
  register: nginx_status
  failed_when: false
  changed_when: false

- name: Start nginx if not running
  service:
    name: nginx
    state: started
  when: nginx_status.rc != 0
```

### Failed When

```yaml
- name: Run application tests
  command: npm test
  register: test_result
  failed_when:
    - test_result.rc != 0
    - "'error' in test_result.stderr"
```

### Changed When

```yaml
- name: Check config syntax
  command: nginx -t
  register: config_check
  changed_when: false  # Never report as changed

- name: Deploy script
  copy:
    src: deploy.sh
    dest: /usr/local/bin/deploy.sh
  register: script_deployed
  changed_when: script_deployed.checksum != previous_checksum
```

---

## Loops

### Simple Loop

```yaml
- name: Install multiple packages
  apt:
    name: "{{ item }}"
    state: present
  loop:
    - nginx
    - postgresql
    - redis
```

### Loop with Dictionary

```yaml
- name: Create users
  user:
    name: "{{ item.name }}"
    uid: "{{ item.uid }}"
    groups: "{{ item.groups }}"
  loop:
    - { name: 'alice', uid: 1001, groups: 'admin,developers' }
    - { name: 'bob', uid: 1002, groups: 'developers' }
    - { name: 'charlie', uid: 1003, groups: 'operators' }
```

### Loop from Variable

```yaml
vars:
  packages:
    - name: nginx
      state: present
    - name: postgresql
      state: present

tasks:
  - name: Manage packages
    apt:
      name: "{{ item.name }}"
      state: "{{ item.state }}"
    loop: "{{ packages }}"
```

### Loop with Index

```yaml
- name: Create numbered directories
  file:
    path: "/data/shard{{ item.0 }}"
    state: directory
  loop: "{{ range(1, 6) | list }}"
```

### Nested Loops

```yaml
- name: Configure firewall rules
  ufw:
    rule: allow
    port: "{{ item.1 }}"
    from_ip: "{{ item.0 }}"
  loop: "{{ trusted_ips | product(allowed_ports) | list }}"
  vars:
    trusted_ips: ['10.0.1.0/24', '10.0.2.0/24']
    allowed_ports: [80, 443]
```

### Loop Until

```yaml
- name: Wait for service to be ready
  uri:
    url: http://localhost:8080/health
    status_code: 200
  register: health_check
  until: health_check.status == 200
  retries: 10
  delay: 5
```

---

## Error Handling

### Ignore Errors

```yaml
- name: Attempt to stop service
  service:
    name: oldapp
    state: stopped
  ignore_errors: yes
```

### Block Rescue Always

```yaml
- name: Deploy application
  block:
    - name: Stop application
      service:
        name: myapp
        state: stopped

    - name: Deploy new version
      copy:
        src: app-v2.0.tar.gz
        dest: /opt/app/

    - name: Start application
      service:
        name: myapp
        state: started

  rescue:
    - name: Rollback to previous version
      copy:
        src: app-v1.9-backup.tar.gz
        dest: /opt/app/

    - name: Start previous version
      service:
        name: myapp
        state: started

    - name: Send alert
      mail:
        to: ops@example.com
        subject: "Deployment failed"

  always:
    - name: Clear deployment lock
      file:
        path: /var/lock/deployment.lock
        state: absent
```

### Any Errors Fatal

```yaml
- name: Critical deployment
  hosts: all
  any_errors_fatal: yes

  tasks:
    - name: Update database schema
      command: /opt/app/migrate.sh
```

---

## Best Practices

### 1. Use Pre-Tasks for Preparation

```yaml
pre_tasks:
  - name: Update package cache
    apt:
      update_cache: yes
      cache_valid_time: 3600

  - name: Ensure prerequisites installed
    apt:
      name:
        - python3
        - python3-pip
      state: present
```

### 2. Use Post-Tasks for Verification

```yaml
post_tasks:
  - name: Verify web service responds
    uri:
      url: http://localhost:80
      status_code: 200
    retries: 5
    delay: 3

  - name: Check log for errors
    command: grep -i error /var/log/app/app.log
    register: log_check
    failed_when:
      - log_check.rc == 0
      - "'CRITICAL' in log_check.stdout"
```

### 3. Separate Concerns with Roles

```yaml
# Don't put everything in one playbook
# Instead, organize by responsibility:
roles:
  - common          # OS configuration
  - security        # Firewall, users
  - monitoring      # Metrics, logging
  - application     # App-specific config
```

### 4. Use Check Mode for Safety

```yaml
# Always test with --check first
ansible-playbook site.yml --check --diff

# Some tasks need check mode disabled
- name: Validate config
  command: nginx -t
  check_mode: no
```

### 5. Document with Clear Names

```yaml
# Good: Clear, descriptive names
- name: Install nginx web server
- name: Configure nginx virtual hosts
- name: Ensure nginx service is running

# Bad: Vague names
- name: Install package
- name: Configure stuff
- name: Run command
```

### 6. Keep Playbooks Focused

```yaml
# Good: Single responsibility
# webservers.yml - Configure web tier
# databases.yml - Configure database tier
# monitoring.yml - Configure monitoring

# Bad: One massive playbook
# everything.yml - Does everything
```

### 7. Use Variable Validation

```yaml
- name: Validate required variables
  assert:
    that:
      - app_version is defined
      - app_port is defined
      - app_port | int > 1024
    fail_msg: "Required variables not properly defined"
```

### 8. Leverage Ansible Facts

```yaml
- name: Configure based on system facts
  template:
    src: app.conf.j2
    dest: /etc/app/app.conf
  vars:
    memory_limit: "{{ (ansible_memtotal_mb * 0.8) | int }}"
    cpu_workers: "{{ ansible_processor_vcpus }}"
```

### 9. Use Handlers for Restarts

```yaml
# Don't restart services directly in tasks
# Use handlers triggered by changes

tasks:
  - name: Update config
    template:
      src: app.conf.j2
      dest: /etc/app/app.conf
    notify: Restart app

handlers:
  - name: Restart app
    service:
      name: myapp
      state: restarted
```

### 10. Test Idempotency

```bash
# Run playbook twice
ansible-playbook site.yml
ansible-playbook site.yml

# Second run should have zero changes
# If tasks show "changed" on second run, fix idempotency
```
