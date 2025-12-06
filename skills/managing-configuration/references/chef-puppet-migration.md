# Chef and Puppet Migration Guide

## Table of Contents

1. [Chef to Ansible Migration](#chef-to-ansible-migration)
2. [Puppet to Ansible Migration](#puppet-to-ansible-migration)
3. [Migration Strategy](#migration-strategy)
4. [Migration Tools](#migration-tools)
5. [Common Pitfalls](#common-pitfalls)
6. [Best Practices](#best-practices)
7. [Resources](#resources)

---

## Chef to Ansible Migration

### Conceptual Mapping

| Chef Concept | Ansible Equivalent |
|--------------|-------------------|
| Recipe | Task list in role |
| Cookbook | Role |
| Attribute | Variable |
| Resource | Module |
| Template | Jinja2 template |
| Data bag | Variable file (encrypted with vault) |
| Node | Managed host in inventory |
| Chef Server | Ansible control node |
| knife | ansible, ansible-playbook CLI |

### Recipe to Playbook Translation

**Chef Recipe (install_nginx.rb):**
```ruby
package 'nginx' do
  action :install
end

template '/etc/nginx/nginx.conf' do
  source 'nginx.conf.erb'
  owner 'root'
  group 'root'
  mode '0644'
  notifies :reload, 'service[nginx]'
end

service 'nginx' do
  action [:enable, :start]
end
```

**Ansible Playbook:**
```yaml
---
- name: Install nginx
  ansible.builtin.apt:
    name: nginx
    state: present

- name: Configure nginx
  ansible.builtin.template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    owner: root
    group: root
    mode: '0644'
  notify: Reload nginx

- name: Start nginx
  ansible.builtin.service:
    name: nginx
    state: started
    enabled: yes

handlers:
  - name: Reload nginx
    ansible.builtin.service:
      name: nginx
      state: reloaded
```

### Common Chef Patterns in Ansible

**1. Package Installation:**

Chef:
```ruby
package ['nginx', 'postgresql', 'redis'] do
  action :install
end
```

Ansible:
```yaml
- name: Install packages
  ansible.builtin.apt:
    name:
      - nginx
      - postgresql
      - redis
    state: present
```

**2. File Management:**

Chef:
```ruby
file '/etc/app/config.yml' do
  content 'key: value'
  owner 'app'
  group 'app'
  mode '0600'
end
```

Ansible:
```yaml
- name: Create config file
  ansible.builtin.copy:
    content: 'key: value'
    dest: /etc/app/config.yml
    owner: app
    group: app
    mode: '0600'
```

**3. Conditionals:**

Chef:
```ruby
package 'nginx' do
  action :install
  only_if { node['platform_family'] == 'debian' }
end
```

Ansible:
```yaml
- name: Install nginx
  ansible.builtin.apt:
    name: nginx
    state: present
  when: ansible_os_family == "Debian"
```

---

## Puppet to Ansible Migration

### Conceptual Mapping

| Puppet Concept | Ansible Equivalent |
|----------------|-------------------|
| Manifest | Playbook |
| Module | Role |
| Resource | Module |
| Class | Role |
| Template | Jinja2 template |
| Hiera | group_vars, host_vars |
| Facter | Ansible facts |
| Puppet Master | Ansible control node |
| Node | Managed host in inventory |
| puppet agent | ansible-pull (optional) |

### Manifest to Playbook Translation

**Puppet Manifest (nginx.pp):**
```puppet
package { 'nginx':
  ensure => installed,
}

file { '/etc/nginx/nginx.conf':
  ensure  => file,
  owner   => 'root',
  group   => 'root',
  mode    => '0644',
  source  => 'puppet:///modules/nginx/nginx.conf',
  notify  => Service['nginx'],
}

service { 'nginx':
  ensure => running,
  enable => true,
}
```

**Ansible Playbook:**
```yaml
---
- name: Install nginx
  ansible.builtin.apt:
    name: nginx
    state: present

- name: Configure nginx
  ansible.builtin.copy:
    src: nginx.conf
    dest: /etc/nginx/nginx.conf
    owner: root
    group: root
    mode: '0644'
  notify: Restart nginx

- name: Start nginx
  ansible.builtin.service:
    name: nginx
    state: started
    enabled: yes

handlers:
  - name: Restart nginx
    ansible.builtin.service:
      name: nginx
      state: restarted
```

### Common Puppet Patterns in Ansible

**1. Resource Ensure:**

Puppet:
```puppet
package { 'nginx':
  ensure => installed,
}

service { 'nginx':
  ensure => running,
}
```

Ansible:
```yaml
- name: Ensure nginx installed
  ansible.builtin.apt:
    name: nginx
    state: present

- name: Ensure nginx running
  ansible.builtin.service:
    name: nginx
    state: started
```

**2. File Resources:**

Puppet:
```puppet
file { '/opt/app':
  ensure => directory,
  owner  => 'app',
  mode   => '0755',
}
```

Ansible:
```yaml
- name: Ensure directory exists
  ansible.builtin.file:
    path: /opt/app
    state: directory
    owner: app
    mode: '0755'
```

**3. User Management:**

Puppet:
```puppet
user { 'appuser':
  ensure => present,
  uid    => 1001,
  gid    => 'appgroup',
  home   => '/home/appuser',
  shell  => '/bin/bash',
}
```

Ansible:
```yaml
- name: Create user
  ansible.builtin.user:
    name: appuser
    uid: 1001
    group: appgroup
    home: /home/appuser
    shell: /bin/bash
    state: present
```

---

## Migration Strategy

### Phase 1: Assessment (Week 1)

**Tasks:**
1. Inventory existing Chef/Puppet code
2. Identify critical cookbooks/modules
3. Document dependencies
4. Assess complexity
5. Choose pilot project

**Deliverables:**
- Migration scope document
- Priority list
- Resource requirements

### Phase 2: Parallel Implementation (Weeks 2-4)

**Tasks:**
1. Install Ansible on control node
2. Convert pilot cookbook/module
3. Test in non-production
4. Run Chef/Puppet and Ansible in parallel
5. Validate equivalence

**Approach:**
- Start with simplest cookbook/module
- Convert 1-2 cookbooks/modules per week
- Maintain existing system during migration

### Phase 3: Validation (Week 5)

**Tasks:**
1. Compare Chef/Puppet output vs Ansible output
2. Run compliance checks
3. Performance testing
4. Security audit
5. Documentation review

### Phase 4: Cutover (Week 6)

**Tasks:**
1. Disable Chef/Puppet
2. Full Ansible deployment
3. Monitor for issues
4. Address any gaps
5. Document new workflows

### Phase 5: Cleanup (Week 7)

**Tasks:**
1. Remove Chef/Puppet infrastructure
2. Archive old code
3. Train team on Ansible
4. Update runbooks
5. Celebrate!

---

## Migration Tools

### chefspec to Molecule

Convert Chef cookbook tests to Molecule tests.

### puppet-lint to ansible-lint

Run ansible-lint for quality checks.

### Custom Conversion Scripts

Simple script to help translate:

```python
#!/usr/bin/env python3
"""Simple Chef recipe to Ansible playbook converter."""

import re
import sys

def convert_package(line):
    match = re.search(r"package ['\"]([^'\"]+)['\"]", line)
    if match:
        return f"""
- name: Install {match.group(1)}
  ansible.builtin.apt:
    name: {match.group(1)}
    state: present
"""
    return None

def convert_service(line):
    match = re.search(r"service ['\"]([^'\"]+)['\"]", line)
    if match:
        return f"""
- name: Start {match.group(1)}
  ansible.builtin.service:
    name: {match.group(1)}
    state: started
    enabled: yes
"""
    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: convert.py recipe.rb")
        sys.exit(1)

    print("---")
    with open(sys.argv[1]) as f:
        for line in f:
            result = convert_package(line) or convert_service(line)
            if result:
                print(result)

if __name__ == '__main__':
    main()
```

---

## Common Pitfalls

### 1. Agent Dependency

**Chef/Puppet:** Requires agent on managed nodes.
**Ansible:** Agentless (SSH only).

**Solution:** Ensure SSH access configured before migration.

### 2. Pull vs Push Model

**Chef/Puppet:** Nodes pull configuration.
**Ansible:** Control node pushes configuration.

**Solution:** Use `ansible-pull` if pull model required.

### 3. State Files

**Chef/Puppet:** Maintain state on nodes.
**Ansible:** Stateless by default.

**Solution:** Use dynamic inventory for state tracking if needed.

### 4. Custom Resources

**Chef/Puppet:** Custom resources in Ruby/Puppet DSL.
**Ansible:** Custom modules in Python.

**Solution:** Rewrite custom resources as Ansible modules or use `command`/`shell` temporarily.

---

## Best Practices

### 1. Incremental Migration

Don't try to migrate everything at once. Start with simple, low-risk cookbooks/modules.

### 2. Maintain Parity

Run both systems in parallel during migration to ensure equivalence.

### 3. Test Thoroughly

Use Molecule to test converted roles before deploying.

### 4. Document Changes

Keep detailed notes on translation decisions for future reference.

### 5. Train Team

Ensure team is comfortable with Ansible before full cutover.

### 6. Leverage Ansible Galaxy

Check if equivalent roles already exist on Ansible Galaxy before rewriting.

---

## Resources

**Ansible Documentation:**
- https://docs.ansible.com/ansible/latest/porting_guides/

**Community Examples:**
- https://github.com/geerlingguy/ansible-for-devops
- https://github.com/ansible/ansible-examples

**Consulting:**
- Red Hat Consulting Services
- Ansible Professional Services
