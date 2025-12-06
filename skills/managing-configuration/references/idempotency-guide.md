# Idempotency Guide

## Table of Contents

1. [What is Idempotency?](#what-is-idempotency)
2. [Patterns for Idempotency](#patterns-for-idempotency)
3. [Common Idempotency Issues](#common-idempotency-issues)
4. [Testing Idempotency](#testing-idempotency)
5. [Module Reference](#module-reference)
6. [Best Practices](#best-practices)
7. [Debugging Idempotency Issues](#debugging-idempotency-issues)

---

## What is Idempotency?

Idempotency means running a playbook multiple times produces the same result as running it once. Tasks should converge to a desired state without side effects on repeated execution.

**Benefits:**
- **Safe to re-run** - No unintended changes
- **Predictable** - Same input = same output
- **Efficient** - Only applies necessary changes
- **Production-ready** - Can safely run on live systems

---

## Patterns for Idempotency

### 1. Use State-Based Modules

**Good (idempotent):**
```yaml
- name: Ensure nginx is installed
  ansible.builtin.apt:
    name: nginx
    state: present
```

**Bad (not idempotent):**
```yaml
- name: Install nginx
  ansible.builtin.command: apt-get install -y nginx
```

### 2. Check Before Action

```yaml
- name: Check if config exists
  ansible.builtin.stat:
    path: /etc/app/app.conf
  register: config_file

- name: Create config only if missing
  ansible.builtin.template:
    src: app.conf.j2
    dest: /etc/app/app.conf
  when: not config_file.stat.exists
```

### 3. Use Handlers for Side Effects

```yaml
tasks:
  - name: Update nginx config
    ansible.builtin.template:
      src: nginx.conf.j2
      dest: /etc/nginx/nginx.conf
    notify: Reload nginx

handlers:
  - name: Reload nginx
    ansible.builtin.service:
      name: nginx
      state: reloaded
```

### 4. Set changed_when Appropriately

```yaml
# Command that doesn't change system
- name: Check nginx config syntax
  ansible.builtin.command: nginx -t
  changed_when: false

# Command with conditional change detection
- name: Update cache
  ansible.builtin.command: apt-get update
  register: apt_update
  changed_when: "'Reading package lists' in apt_update.stdout"
```

### 5. Use Desired State Parameters

```yaml
# Service management
- name: Ensure nginx is running
  ansible.builtin.service:
    name: nginx
    state: started      # started, stopped, restarted, reloaded
    enabled: yes        # Boot persistence

# Package management
- name: Ensure package version
  ansible.builtin.apt:
    name: nginx=1.24.0-1
    state: present      # present, absent, latest

# File management
- name: Ensure file exists
  ansible.builtin.copy:
    src: file.txt
    dest: /tmp/file.txt
    force: no           # Don't overwrite if exists
```

---

## Common Idempotency Issues

### Issue 1: Command/Shell Modules

**Problem:**
```yaml
# Always reports "changed"
- name: Create directory
  ansible.builtin.command: mkdir /opt/app
```

**Solution 1: Use appropriate module**
```yaml
- name: Ensure directory exists
  ansible.builtin.file:
    path: /opt/app
    state: directory
```

**Solution 2: Add changed_when**
```yaml
- name: Create directory
  ansible.builtin.command: mkdir /opt/app
  args:
    creates: /opt/app  # Only run if /opt/app doesn't exist
```

### Issue 2: Database Operations

**Problem:**
```yaml
# Fails on second run
- name: Create database
  ansible.builtin.command: createdb myapp
```

**Solution:**
```yaml
- name: Ensure database exists
  community.postgresql.postgresql_db:
    name: myapp
    state: present
```

### Issue 3: User/Group Creation

**Problem:**
```yaml
# Not idempotent
- name: Add user
  ansible.builtin.command: useradd appuser
```

**Solution:**
```yaml
- name: Ensure user exists
  ansible.builtin.user:
    name: appuser
    system: yes
    state: present
```

### Issue 4: Package Downloads

**Problem:**
```yaml
# Downloads every time
- name: Download application
  ansible.builtin.get_url:
    url: https://example.com/app.tar.gz
    dest: /tmp/app.tar.gz
```

**Solution:**
```yaml
- name: Download application (cached)
  ansible.builtin.get_url:
    url: https://example.com/app.tar.gz
    dest: /tmp/app.tar.gz
    checksum: sha256:abc123...  # Only downloads if checksum differs
```

### Issue 5: Configuration Appends

**Problem:**
```yaml
# Appends every run
- name: Add config line
  ansible.builtin.lineinfile:
    path: /etc/hosts
    line: "10.0.0.1 server1"
    state: present
    # Missing unique identifier
```

**Solution:**
```yaml
- name: Ensure host entry exists
  ansible.builtin.lineinfile:
    path: /etc/hosts
    regexp: '^.* server1$'  # Unique match pattern
    line: "10.0.0.1 server1"
    state: present
```

---

## Testing Idempotency

### Manual Test

```bash
# Run playbook twice
ansible-playbook site.yml
ansible-playbook site.yml

# Second run should report:
# ok=N changed=0 unreachable=0 failed=0
```

### Molecule Idempotence Test

```bash
# Automatic idempotence check
molecule idempotence
```

**Passes if:** Second run has zero changes.
**Fails if:** Second run reports any changed tasks.

### Idempotence Verification Task

```yaml
- name: Verify idempotence
  block:
    - name: Run role first time
      ansible.builtin.include_role:
        name: myapp

    - name: Run role second time
      ansible.builtin.include_role:
        name: myapp
      register: second_run

    - name: Assert no changes on second run
      ansible.builtin.assert:
        that:
          - not second_run.changed
        fail_msg: "Role is not idempotent"
```

---

## Module Reference

### Idempotent Modules (Safe to Use)

| Module | Purpose | Idempotent |
|--------|---------|------------|
| `apt`, `yum`, `dnf` | Package management | ✅ Yes |
| `service`, `systemd` | Service management | ✅ Yes |
| `user`, `group` | User management | ✅ Yes |
| `file` | File/directory operations | ✅ Yes |
| `copy`, `template` | File deployment | ✅ Yes |
| `lineinfile`, `blockinfile` | Config file editing | ✅ Yes (with regexp) |
| `git` | Git operations | ✅ Yes |
| `postgresql_db`, `mysql_db` | Database management | ✅ Yes |

### Non-Idempotent Modules (Use Carefully)

| Module | Purpose | Requires |
|--------|---------|----------|
| `command` | Run commands | `creates`, `removes`, or `changed_when` |
| `shell` | Run shell commands | `creates`, `removes`, or `changed_when` |
| `raw` | Run raw commands | `changed_when` |
| `script` | Run local scripts | `creates`, `removes`, or `changed_when` |

---

## Best Practices

### 1. Always Use State Parameters

```yaml
# Good
- name: Ensure service is running
  ansible.builtin.service:
    name: nginx
    state: started
    enabled: yes

# Bad
- name: Start service
  ansible.builtin.command: systemctl start nginx
```

### 2. Add changed_when to Commands

```yaml
# Read-only commands
- name: Check version
  ansible.builtin.command: app --version
  changed_when: false
  register: version

# Conditional changes
- name: Run migration
  ansible.builtin.command: /opt/app/migrate.sh
  register: migration
  changed_when: "'Applied' in migration.stdout"
```

### 3. Use creates/removes Arguments

```yaml
# Only run if file doesn't exist
- name: Extract archive
  ansible.builtin.command: tar -xzf /tmp/app.tar.gz
  args:
    chdir: /opt/app
    creates: /opt/app/bin/app

# Only run if file exists
- name: Clean up
  ansible.builtin.command: rm -rf /tmp/build
  args:
    removes: /tmp/build
```

### 4. Check State Before Changing

```yaml
- name: Check if service exists
  ansible.builtin.stat:
    path: /etc/systemd/system/myapp.service
  register: service_file

- name: Install service
  ansible.builtin.template:
    src: myapp.service.j2
    dest: /etc/systemd/system/myapp.service
  when: not service_file.stat.exists or force_reinstall | default(false)
  notify: Reload systemd
```

### 5. Use Handlers for Restarts

```yaml
# Don't restart directly
tasks:
  - name: Update config
    ansible.builtin.template:
      src: app.conf.j2
      dest: /etc/app/app.conf
    notify: Restart app

# Use handler (only restarts if config changed)
handlers:
  - name: Restart app
    ansible.builtin.service:
      name: myapp
      state: restarted
```

### 6. Avoid Destructive Operations

```yaml
# Bad: Destroys data every run
- name: Reset database
  ansible.builtin.command: dropdb myapp && createdb myapp

# Good: Only create if missing
- name: Ensure database exists
  community.postgresql.postgresql_db:
    name: myapp
    state: present
```

### 7. Use force Parameter Carefully

```yaml
# Bad: Always overwrites
- name: Deploy config
  ansible.builtin.copy:
    src: app.conf
    dest: /etc/app/app.conf
    force: yes  # Always copies

# Good: Only copies if different
- name: Deploy config
  ansible.builtin.copy:
    src: app.conf
    dest: /etc/app/app.conf
    force: no   # Preserves existing if present
    # Or omit force (default behavior checks content)
```

### 8. Document Non-Idempotent Tasks

```yaml
- name: Run database migration (NOT IDEMPOTENT)
  ansible.builtin.command: /opt/app/migrate.sh
  # NOTE: This will apply all pending migrations each run
  # Future enhancement: track applied migrations
```

### 9. Test Repeatedly

```bash
# Run playbook 3 times
for i in 1 2 3; do
  echo "Run $i"
  ansible-playbook site.yml
done

# All runs after first should show: changed=0
```

### 10. Use Molecule for Automated Testing

```yaml
# molecule.yml includes idempotence test
scenario:
  test_sequence:
    - converge      # First run
    - idempotence   # Second run (verifies no changes)
    - verify        # Verification
```

---

## Debugging Idempotency Issues

### Find Non-Idempotent Tasks

```bash
# Run twice, compare output
ansible-playbook site.yml -v > run1.log
ansible-playbook site.yml -v > run2.log
diff run1.log run2.log
```

### Check Task Results

```yaml
- name: Run task
  ansible.builtin.command: some-command
  register: result

- name: Show result
  ansible.builtin.debug:
    var: result
  # Check: result.changed, result.rc, result.stdout
```

### Use Check Mode

```bash
# Dry run shows what would change
ansible-playbook site.yml --check --diff
```

### Enable Verbose Output

```bash
# Show detailed task execution
ansible-playbook site.yml -vvv
```
