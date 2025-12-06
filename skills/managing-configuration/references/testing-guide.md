# Testing Guide

## Table of Contents

1. [ansible-lint](#ansible-lint)
2. [Molecule](#molecule)
3. [Check Mode](#check-mode)
4. [Testinfra Verification](#testinfra-verification)
5. [CI/CD Integration](#cicd-integration)
6. [Best Practices](#best-practices)

---

## ansible-lint

### Installation

```bash
pip install ansible-lint
```

### Basic Usage

```bash
# Lint all playbooks in current directory
ansible-lint

# Lint specific playbook
ansible-lint playbooks/webservers.yml

# Lint role
ansible-lint roles/nginx/

# Auto-fix issues
ansible-lint --fix

# Output as JSON
ansible-lint --format json
```

### Configuration

**.ansible-lint:**
```yaml
---
# Exclude paths
exclude_paths:
  - .cache/
  - .git/
  - molecule/
  - venv/
  - __pycache__/

# Enable specific rules
enable_list:
  - yaml
  - fqcn-builtins  # Require FQCN for builtin modules

# Skip specific rules
skip_list:
  - name[casing]   # Allow flexible task naming
  - risky-file-permissions  # Allow without explicit mode

# Warn on experimental rules
warn_list:
  - experimental

# Use tags
tags:
  - idiom
  - security

# Set offline mode
offline: false
```

### Common Rules

| Rule ID | Description | Example |
|---------|-------------|---------|
| `yaml` | YAML syntax errors | Invalid indentation |
| `name[casing]` | Task names should be title case | Use "Install nginx" not "install nginx" |
| `fqcn-builtins` | Use FQCN for builtin modules | `ansible.builtin.copy` not `copy` |
| `risky-file-permissions` | File tasks should set mode | Add `mode: '0644'` |
| `no-changed-when` | Command tasks need changed_when | Avoid false positives |
| `command-instead-of-module` | Use module instead of command | Use `apt` not `command: apt-get` |

### Fix Common Issues

**Issue 1: Missing FQCN**
```yaml
# Bad
- name: Copy file
  copy:
    src: file.txt
    dest: /tmp/file.txt

# Good
- name: Copy file
  ansible.builtin.copy:
    src: file.txt
    dest: /tmp/file.txt
```

**Issue 2: Missing file mode**
```yaml
# Bad
- name: Create file
  copy:
    src: file.txt
    dest: /tmp/file.txt

# Good
- name: Create file
  copy:
    src: file.txt
    dest: /tmp/file.txt
    mode: '0644'
```

**Issue 3: Command without changed_when**
```yaml
# Bad
- name: Check status
  command: systemctl is-active nginx

# Good
- name: Check status
  command: systemctl is-active nginx
  changed_when: false
  failed_when: false
```

---

## Molecule

### Installation

```bash
# Install Molecule with Docker driver
pip install molecule molecule-docker ansible-core

# Or with Podman
pip install molecule molecule-podman
```

### Initialize Role with Molecule

**New role:**
```bash
molecule init role my_role --driver-name docker
```

**Add to existing role:**
```bash
cd roles/nginx
molecule init scenario default --driver-name docker
```

### Directory Structure

```
roles/nginx/
└── molecule/
    └── default/
        ├── molecule.yml      # Molecule configuration
        ├── converge.yml      # Test playbook
        ├── verify.yml        # Verification tasks
        ├── prepare.yml       # Preparation tasks (optional)
        └── requirements.yml  # Role dependencies (optional)
```

### molecule.yml Configuration

```yaml
---
dependency:
  name: galaxy
  options:
    requirements-file: requirements.yml

driver:
  name: docker

platforms:
  - name: nginx-ubuntu-22
    image: ubuntu:22.04
    pre_build_image: true
    privileged: true
    command: /lib/systemd/systemd
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:ro
    tmpfs:
      - /run
      - /tmp

  - name: nginx-centos-9
    image: quay.io/centos/centos:stream9
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
      stdout_callback: yaml
  inventory:
    group_vars:
      all:
        nginx_worker_processes: 2
        nginx_enable_ssl: false

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

### converge.yml (Test Playbook)

```yaml
---
- name: Converge
  hosts: all
  become: true

  tasks:
    - name: Include nginx role
      ansible.builtin.include_role:
        name: nginx
      vars:
        nginx_worker_processes: 4
        nginx_enable_ssl: false
```

### verify.yml (Verification)

```yaml
---
- name: Verify
  hosts: all
  gather_facts: false

  tasks:
    - name: Check nginx package is installed
      ansible.builtin.package:
        name: nginx
        state: present
      check_mode: yes
      register: pkg
      failed_when: pkg is changed

    - name: Check nginx service is running
      ansible.builtin.service:
        name: nginx
        state: started
      check_mode: yes
      register: svc
      failed_when: svc is changed

    - name: Verify nginx responds on port 80
      ansible.builtin.uri:
        url: http://localhost:80
        status_code: 200
      retries: 3
      delay: 2

    - name: Check nginx config syntax
      ansible.builtin.command: nginx -t
      changed_when: false

    - name: Verify nginx user exists
      ansible.builtin.user:
        name: www-data
        state: present
      check_mode: yes
      register: user
      failed_when: user is changed
```

### Molecule Workflow

**Full test sequence:**
```bash
molecule test
```

**Individual steps:**
```bash
# Create test instances
molecule create

# Apply role (converge)
molecule converge

# Run verification
molecule verify

# Test idempotence (run twice, should have no changes)
molecule idempotence

# Destroy instances
molecule destroy
```

**Development workflow:**
```bash
# Create instances
molecule create

# Test changes repeatedly
molecule converge

# When satisfied, run full test
molecule test
```

**Test specific platform:**
```bash
molecule test --platform-name nginx-ubuntu-22
```

**Debug mode:**
```bash
molecule --debug test
```

### Testinfra Integration

Install Testinfra:
```bash
pip install molecule-plugins[testinfra]
```

**Update molecule.yml:**
```yaml
verifier:
  name: testinfra
```

**Create molecule/default/test_default.py:**
```python
import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_nginx_installed(host):
    """Test nginx package is installed."""
    nginx = host.package("nginx")
    assert nginx.is_installed

def test_nginx_running(host):
    """Test nginx service is running."""
    nginx = host.service("nginx")
    assert nginx.is_running
    assert nginx.is_enabled

def test_nginx_listening(host):
    """Test nginx is listening on port 80."""
    assert host.socket("tcp://0.0.0.0:80").is_listening

def test_nginx_config_valid(host):
    """Test nginx configuration is valid."""
    cmd = host.run("nginx -t")
    assert cmd.rc == 0

def test_nginx_responds(host):
    """Test nginx responds to HTTP requests."""
    cmd = host.run("curl -f http://localhost")
    assert cmd.rc == 0
```

---

## Check Mode

### Basic Check Mode

```bash
# Dry run (show what would change)
ansible-playbook site.yml --check

# Dry run with diff output
ansible-playbook site.yml --check --diff

# Limit to specific hosts
ansible-playbook site.yml --check --limit webservers
```

### In Playbooks

**Always run in check mode:**
```yaml
- name: Validate nginx config
  ansible.builtin.command: nginx -t
  check_mode: yes
  changed_when: false
```

**Never run in check mode:**
```yaml
- name: Restart nginx
  ansible.builtin.service:
    name: nginx
    state: restarted
  check_mode: no
```

**Conditional check mode:**
```yaml
- name: Deploy configuration
  ansible.builtin.template:
    src: app.conf.j2
    dest: /etc/app/app.conf
  register: config_deployed

- name: Validate config
  ansible.builtin.command: app validate-config /etc/app/app.conf
  when: config_deployed is changed and not ansible_check_mode
```

---

## Testinfra Verification

### Installation

```bash
pip install testinfra
```

### Write Tests

**test_webserver.py:**
```python
def test_nginx_installed(host):
    """Nginx package is installed."""
    assert host.package("nginx").is_installed

def test_nginx_running(host):
    """Nginx service is running and enabled."""
    nginx = host.service("nginx")
    assert nginx.is_running
    assert nginx.is_enabled

def test_nginx_port(host):
    """Nginx is listening on port 80."""
    assert host.socket("tcp://0.0.0.0:80").is_listening

def test_nginx_config(host):
    """Nginx configuration file exists."""
    config = host.file("/etc/nginx/nginx.conf")
    assert config.exists
    assert config.is_file
    assert config.user == "root"
    assert config.mode == 0o644

def test_nginx_process(host):
    """Nginx process is running."""
    assert len(host.process.filter(comm="nginx")) >= 1

def test_nginx_response(host):
    """Nginx responds to HTTP requests."""
    cmd = host.run("curl -f http://localhost")
    assert cmd.rc == 0
    assert "nginx" in cmd.stdout.lower()
```

### Run Tests

```bash
# Test against localhost
testinfra test_webserver.py --connection=local

# Test against SSH host
testinfra test_webserver.py --hosts=web1.example.com

# Test with Ansible inventory
testinfra test_webserver.py --ansible-inventory=inventory/production

# Test specific group
testinfra test_webserver.py --hosts='ansible://webservers'
```

---

## CI/CD Integration

### GitHub Actions

**.github/workflows/ansible-test.yml:**
```yaml
name: Ansible Tests

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install ansible ansible-lint

      - name: Run ansible-lint
        run: |
          ansible-lint playbooks/

  molecule:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install molecule molecule-docker ansible-core

      - name: Run Molecule tests
        run: |
          cd roles/nginx
          molecule test

  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Ansible
        run: pip install ansible

      - name: Run playbook check
        run: |
          ansible-playbook site.yml --check --syntax-check
```

### GitLab CI

**.gitlab-ci.yml:**
```yaml
stages:
  - lint
  - test

ansible-lint:
  stage: lint
  image: python:3.11
  before_script:
    - pip install ansible ansible-lint
  script:
    - ansible-lint playbooks/

molecule-test:
  stage: test
  image: python:3.11
  services:
    - docker:dind
  before_script:
    - pip install molecule molecule-docker ansible-core
  script:
    - cd roles/nginx
    - molecule test
```

---

## Best Practices

### 1. Test Early and Often

```bash
# During development
molecule converge  # Apply changes
molecule verify    # Check results

# Before committing
ansible-lint
molecule test
```

### 2. Test Multiple OS Platforms

```yaml
# molecule.yml
platforms:
  - name: ubuntu-20
    image: ubuntu:20.04
  - name: ubuntu-22
    image: ubuntu:22.04
  - name: centos-9
    image: centos:stream9
  - name: debian-11
    image: debian:11
```

### 3. Verify Idempotence

```bash
# Molecule automatically tests idempotence
molecule idempotence

# Or manually
ansible-playbook site.yml
ansible-playbook site.yml  # Should report 0 changes
```

### 4. Separate Unit and Integration Tests

```
roles/nginx/
└── molecule/
    ├── default/          # Unit tests (single role)
    └── integration/      # Integration tests (full stack)
```

### 5. Use Check Mode Before Production

```bash
# Always check before deploying
ansible-playbook site.yml --check --diff --limit production
```

### 6. Test Error Conditions

```yaml
# verify.yml
- name: Test with invalid config
  block:
    - name: Deploy invalid config
      ansible.builtin.copy:
        content: "invalid syntax"
        dest: /etc/nginx/invalid.conf

    - name: Verify nginx rejects invalid config
      ansible.builtin.command: nginx -t -c /etc/nginx/invalid.conf
      register: result
      failed_when: result.rc == 0  # Should fail
```

### 7. Document Test Requirements

**README.md:**
```markdown
## Testing

### Prerequisites
- Docker or Podman
- Python 3.11+
- pip packages: molecule, molecule-docker, ansible-lint

### Run Tests
```bash
# Lint
ansible-lint

# Full test suite
molecule test

# Quick test
molecule converge && molecule verify
```

### 8. Clean Up After Tests

```bash
# Molecule cleanup
molecule destroy

# Remove containers
docker ps -a | grep molecule | awk '{print $1}' | xargs docker rm -f
```

### 9. Use Assertions in Verification

```yaml
- name: Verify critical settings
  ansible.builtin.assert:
    that:
      - nginx_worker_processes is defined
      - nginx_worker_processes | int > 0
      - nginx_user == "www-data"
    fail_msg: "Critical configuration missing or invalid"
```

### 10. Profile Performance

```yaml
# molecule.yml
provisioner:
  config_options:
    defaults:
      callbacks_enabled: ansible.posix.profile_tasks
```
