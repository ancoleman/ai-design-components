# Troubleshooting Guide

## Table of Contents

1. [Connection Issues](#connection-issues)
2. [Playbook Execution Issues](#playbook-execution-issues)
3. [Module-Specific Issues](#module-specific-issues)
4. [Performance Issues](#performance-issues)
5. [Debugging Techniques](#debugging-techniques)
6. [Vault Issues](#vault-issues)
7. [Inventory Issues](#inventory-issues)
8. [Common Error Messages](#common-error-messages)
9. [Getting Help](#getting-help)

---

## Connection Issues

### Cannot Connect via SSH

**Symptoms:**
```
fatal: [web1.example.com]: UNREACHABLE! => {"changed": false, "msg": "Failed to connect"}
```

**Solutions:**

1. **Test SSH connectivity manually:**
```bash
ssh user@web1.example.com
```

2. **Verify SSH keys:**
```bash
ssh-add -l  # List loaded keys
ssh -vvv user@web1.example.com  # Verbose debugging
```

3. **Check inventory configuration:**
```ini
[webservers]
web1.example.com ansible_host=10.0.1.10 ansible_user=deploy
```

4. **Use password authentication temporarily:**
```bash
ansible-playbook site.yml --ask-pass
```

5. **Check SSH agent forwarding:**
```bash
ssh-add ~/.ssh/id_rsa
ansible-playbook site.yml
```

### Permission Denied (publickey)

**Solutions:**

1. **Verify SSH key is on target:**
```bash
ssh-copy-id user@web1.example.com
```

2. **Check file permissions:**
```bash
# On control node
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub

# On managed node
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

3. **Use different key:**
```ini
[webservers]
web1.example.com ansible_ssh_private_key_file=~/.ssh/custom_key
```

### Privilege Escalation Failed

**Symptoms:**
```
fatal: [web1.example.com]: FAILED! => {"msg": "Missing sudo password"}
```

**Solutions:**

1. **Provide sudo password:**
```bash
ansible-playbook site.yml --ask-become-pass
```

2. **Configure passwordless sudo:**
```bash
# On managed node
echo "deploy ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/deploy
```

3. **Use different become method:**
```yaml
- hosts: all
  become: yes
  become_method: su  # Instead of sudo
  become_user: root
```

---

## Playbook Execution Issues

### Handler Not Firing

**Problem:** Handler defined but never executes.

**Causes:**

1. **Handler name mismatch:**
```yaml
# BAD: Names don't match
- name: Update config
  notify: Restart nginx

handlers:
  - name: Restart Nginx  # Capital N - won't match
```

2. **Task never changes:**
```yaml
- name: Update config
  copy:
    src: nginx.conf
    dest: /etc/nginx/nginx.conf
  notify: Restart nginx
# Handler only fires if copy reports "changed"
```

**Solutions:**

1. **Verify exact name match:**
```yaml
- name: Update config
  notify: Restart nginx  # Exact match required

handlers:
  - name: Restart nginx
```

2. **Force handler execution:**
```yaml
- name: Update config
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  notify: Restart nginx

- name: Flush handlers now
  meta: flush_handlers
```

3. **Check task changed status:**
```yaml
- name: Update config
  copy:
    src: nginx.conf
    dest: /etc/nginx/nginx.conf
  register: config_update

- debug:
    msg: "Config changed: {{ config_update.changed }}"
```

### Variable Not Defined

**Symptoms:**
```
fatal: [web1]: FAILED! => {"msg": "The task includes an option with an undefined variable. The error was: 'db_password' is undefined"}
```

**Solutions:**

1. **Check variable exists:**
```yaml
- debug:
    var: db_password
```

2. **Use default value:**
```yaml
db_password: "{{ db_password | default('changeme') }}"
```

3. **Verify variable precedence:**
```bash
# Show all variables for host
ansible-inventory -i inventory --host web1.example.com
```

4. **Check variable file loaded:**
```yaml
- name: Load variables
  include_vars: database.yml

- debug:
    msg: "Password: {{ db_password }}"
```

### Idempotency Violations

**Problem:** Playbook reports changes on every run.

**Diagnosis:**
```bash
# Run twice and compare
ansible-playbook site.yml -v > run1.log
ansible-playbook site.yml -v > run2.log
diff run1.log run2.log
```

**Common Causes:**

1. **Using command instead of module:**
```yaml
# BAD
- command: apt-get install nginx

# GOOD
- apt:
    name: nginx
    state: present
```

2. **Missing changed_when:**
```yaml
# BAD
- command: echo "test"

# GOOD
- command: echo "test"
  changed_when: false
```

3. **File operations without proper checks:**
```yaml
# BAD
- command: mkdir /opt/app

# GOOD
- file:
    path: /opt/app
    state: directory
```

---

## Module-Specific Issues

### apt Module Failures

**Problem:** Package installation fails.

**Solutions:**

1. **Update cache first:**
```yaml
- name: Update apt cache
  apt:
    update_cache: yes
    cache_valid_time: 3600

- name: Install package
  apt:
    name: nginx
    state: present
```

2. **Check package name:**
```bash
# On managed node
apt-cache search nginx
```

3. **Handle missing packages gracefully:**
```yaml
- name: Install optional package
  apt:
    name: some-package
    state: present
  ignore_errors: yes
```

### template Module Failures

**Problem:** Template rendering fails.

**Solutions:**

1. **Check template syntax:**
```bash
# Validate Jinja2 template locally
python3 << EOF
from jinja2 import Template
with open('template.j2') as f:
    template = Template(f.read())
    print(template.render(var1='value1'))
EOF
```

2. **Debug variable values:**
```yaml
- debug:
    var: ansible_facts

- template:
    src: config.j2
    dest: /etc/app/config
```

3. **Verify file paths:**
```yaml
- stat:
    path: templates/config.j2
  register: template_file
  delegate_to: localhost

- debug:
    var: template_file
```

### service Module Issues

**Problem:** Service management fails.

**Solutions:**

1. **Check service exists:**
```bash
# On managed node
systemctl list-units --type=service | grep nginx
```

2. **Use correct service name:**
```yaml
# Check actual service name
- name: Find service name
  shell: systemctl list-units --type=service | grep -i nginx
  register: service_list

- debug:
    var: service_list.stdout
```

3. **Handle init systems:**
```yaml
- name: Start service (systemd)
  systemd:
    name: nginx
    state: started
  when: ansible_service_mgr == "systemd"

- name: Start service (sysvinit)
  service:
    name: nginx
    state: started
  when: ansible_service_mgr == "sysvinit"
```

---

## Performance Issues

### Playbook Runs Slowly

**Solutions:**

1. **Enable SSH pipelining:**
```ini
# ansible.cfg
[ssh_connection]
pipelining = True
```

2. **Increase forks:**
```ini
# ansible.cfg
[defaults]
forks = 20  # Default is 5
```

3. **Disable fact gathering if not needed:**
```yaml
- hosts: all
  gather_facts: no
```

4. **Use mitogen strategy:**
```bash
pip install mitogen
```

```ini
# ansible.cfg
[defaults]
strategy_plugins = /path/to/mitogen/ansible_mitogen/plugins/strategy
strategy = mitogen_linear
```

5. **Profile tasks:**
```ini
# ansible.cfg
[defaults]
callbacks_enabled = profile_tasks
```

### Fact Gathering Slow

**Solutions:**

1. **Gather only needed facts:**
```yaml
- hosts: all
  gather_facts: yes
  gather_subset:
    - '!all'
    - '!min'
    - network
```

2. **Cache facts:**
```ini
# ansible.cfg
[defaults]
gathering = smart
fact_caching = jsonfile
fact_caching_connection = /tmp/ansible_facts
fact_caching_timeout = 86400
```

---

## Debugging Techniques

### Enable Verbose Output

```bash
# Levels of verbosity
ansible-playbook site.yml -v     # Show task results
ansible-playbook site.yml -vv    # Show task & configuration
ansible-playbook site.yml -vvv   # Show connection info
ansible-playbook site.yml -vvvv  # Show SSH commands
```

### Use Debug Module

```yaml
- name: Debug variable
  debug:
    var: my_variable

- name: Debug message
  debug:
    msg: "Value is {{ my_variable }}"

- name: Debug all variables
  debug:
    var: vars

- name: Debug facts
  debug:
    var: ansible_facts
```

### Register and Inspect

```yaml
- name: Run command
  command: ls /opt
  register: command_output

- name: Show output
  debug:
    var: command_output

- name: Show stdout
  debug:
    msg: "{{ command_output.stdout_lines }}"
```

### Use assert for Validation

```yaml
- name: Validate prerequisites
  assert:
    that:
      - ansible_version.full is version('2.12', '>=')
      - db_password is defined
      - db_password | length > 8
    fail_msg: "Prerequisites not met"
    success_msg: "Prerequisites validated"
```

### Check Syntax

```bash
# Syntax check only
ansible-playbook site.yml --syntax-check

# List tasks
ansible-playbook site.yml --list-tasks

# List hosts
ansible-playbook site.yml --list-hosts
```

### Step Through Playbook

```bash
# Interactive step-by-step
ansible-playbook site.yml --step

# Start at specific task
ansible-playbook site.yml --start-at-task="Install nginx"
```

---

## Vault Issues

### Wrong Vault Password

**Symptoms:**
```
ERROR! Decryption failed
```

**Solutions:**

1. **Verify password:**
```bash
ansible-vault view group_vars/all/vault.yml --ask-vault-pass
```

2. **Check password file:**
```bash
cat ~/.vault_pass  # Verify contents
ansible-playbook site.yml --vault-password-file ~/.vault_pass
```

3. **Use correct vault ID:**
```bash
ansible-playbook site.yml --vault-id prod@~/.vault_pass_prod
```

### Cannot Edit Vault File

**Solutions:**

1. **Set EDITOR variable:**
```bash
export EDITOR=vim
ansible-vault edit vault.yml
```

2. **Decrypt, edit, re-encrypt:**
```bash
ansible-vault decrypt vault.yml
vim vault.yml
ansible-vault encrypt vault.yml
```

---

## Inventory Issues

### Host Not Found

**Solutions:**

1. **List inventory:**
```bash
ansible-inventory -i inventory --list
ansible-inventory -i inventory --graph
```

2. **Test host pattern:**
```bash
ansible all -i inventory --list-hosts
ansible webservers -i inventory --list-hosts
```

3. **Verify inventory file syntax:**
```bash
# INI format check
ansible-inventory -i inventory/hosts --list

# YAML format check
yamllint inventory/production.yml
```

### Dynamic Inventory Not Working

**Solutions:**

1. **Test plugin directly:**
```bash
ansible-inventory -i inventory/aws_ec2.yml --list
```

2. **Check AWS credentials:**
```bash
aws ec2 describe-instances  # Test AWS access
```

3. **Verify plugin installation:**
```bash
ansible-doc -t inventory -l | grep aws_ec2
```

---

## Common Error Messages

### "ERROR! Syntax Error while loading YAML"

**Cause:** YAML formatting error.

**Solution:**
```bash
# Validate YAML
yamllint playbook.yml

# Or use Python
python3 -c "import yaml; yaml.safe_load(open('playbook.yml'))"
```

### "ERROR! conflicting action statements"

**Cause:** Multiple module calls in one task.

**Bad:**
```yaml
- name: Install packages
  apt: name=nginx
  yum: name=nginx
```

**Good:**
```yaml
- name: Install nginx (Debian)
  apt:
    name: nginx
  when: ansible_os_family == "Debian"

- name: Install nginx (RedHat)
  yum:
    name: nginx
  when: ansible_os_family == "RedHat"
```

### "ERROR! 'item' is undefined"

**Cause:** Using loop variable outside of loop.

**Solution:**
```yaml
- name: Install packages
  apt:
    name: "{{ item }}"
  loop:
    - nginx
    - postgresql
  register: install_result

# Access loop results
- debug:
    var: install_result.results
```

---

## Getting Help

### Documentation

```bash
# Module documentation
ansible-doc apt
ansible-doc -l  # List all modules

# Plugin documentation
ansible-doc -t inventory aws_ec2
ansible-doc -t callback profile_tasks
```

### Community Resources

- **Official Docs:** https://docs.ansible.com
- **Forums:** https://forum.ansible.com
- **GitHub:** https://github.com/ansible/ansible
- **IRC:** #ansible on libera.chat
- **Reddit:** r/ansible
- **Stack Overflow:** Tag: ansible

### Professional Support

- **Red Hat Ansible Automation Platform:** Enterprise support
- **Ansible Consulting:** Professional services
- **Training:** Red Hat certified courses
