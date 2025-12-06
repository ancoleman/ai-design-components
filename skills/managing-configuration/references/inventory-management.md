# Inventory Management

## Table of Contents

1. [Static Inventory](#static-inventory)
2. [Dynamic Inventory](#dynamic-inventory)
3. [Hybrid Inventory](#hybrid-inventory)
4. [Inventory Variables](#inventory-variables)
5. [Best Practices](#best-practices)

---

## Static Inventory

### INI Format

**Basic inventory:**
```ini
# inventory/production

[webservers]
web1.example.com
web2.example.com
web3.example.com

[databases]
db1.example.com
db2.example.com

[loadbalancers]
lb1.example.com
```

**With host variables:**
```ini
[webservers]
web1.example.com ansible_host=10.0.1.10 nginx_worker_processes=4
web2.example.com ansible_host=10.0.1.11 nginx_worker_processes=8
web3.example.com ansible_host=10.0.1.12 nginx_worker_processes=4
```

**With group variables:**
```ini
[webservers]
web1.example.com
web2.example.com
web3.example.com

[webservers:vars]
nginx_worker_processes=4
app_env=production
ansible_user=deploy
```

**Parent groups:**
```ini
[webservers]
web1.example.com
web2.example.com

[databases]
db1.example.com
db2.example.com

[production:children]
webservers
databases

[production:vars]
ansible_user=deploy
ansible_become=yes
```

### YAML Format

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
              nginx_worker_processes: 4
            web2.example.com:
              ansible_host: 10.0.1.11
              nginx_worker_processes: 8
          vars:
            app_env: production

        databases:
          hosts:
            db1.example.com:
              ansible_host: 10.0.2.10
            db2.example.com:
              ansible_host: 10.0.2.11
          vars:
            postgres_version: 15

      vars:
        ansible_user: deploy
        ansible_become: yes
```

### Multiple Inventory Files

```
inventory/
├── production/
│   ├── hosts            # Main inventory
│   ├── webservers       # Web tier hosts
│   └── databases        # Database tier hosts
└── staging/
    ├── hosts
    ├── webservers
    └── databases
```

Run with directory:
```bash
ansible-playbook -i inventory/production site.yml
```

---

## Dynamic Inventory

### AWS EC2 Plugin

**Installation:**
```bash
ansible-galaxy collection install amazon.aws
```

**inventory/aws_ec2.yml:**
```yaml
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
    separator: "_"
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
  ansible_user: "'ubuntu'"
```

**Test inventory:**
```bash
# List all hosts
ansible-inventory -i inventory/aws_ec2.yml --list

# Graph view
ansible-inventory -i inventory/aws_ec2.yml --graph

# Run playbook
ansible-playbook -i inventory/aws_ec2.yml site.yml
```

### Azure Resource Manager Plugin

**Installation:**
```bash
ansible-galaxy collection install azure.azcollection
```

**inventory/azure_rm.yml:**
```yaml
plugin: azure_rm

auth_source: auto

include_vm_resource_groups:
  - production-rg

keyed_groups:
  - prefix: tag
    key: tags
  - prefix: location
    key: location

hostnames:
  - name
  - default

compose:
  ansible_host: public_ipv4_addresses[0]
  ansible_user: "'azureuser'"
```

### GCP Compute Plugin

**Installation:**
```bash
ansible-galaxy collection install google.cloud
```

**inventory/gcp_compute.yml:**
```yaml
plugin: gcp_compute

projects:
  - my-project-id

zones:
  - us-central1-a
  - us-central1-b

filters:
  - labels.environment = production
  - status = RUNNING

keyed_groups:
  - key: labels.role
    prefix: role
  - key: zone
    prefix: zone

hostnames:
  - name

compose:
  ansible_host: networkInterfaces[0].accessConfigs[0].natIP
  ansible_user: "'ubuntu'"
```

### Custom Dynamic Inventory Script

**inventory/custom.py:**
```python
#!/usr/bin/env python3
import json
import sys

def get_inventory():
    """Return inventory data structure."""
    inventory = {
        "webservers": {
            "hosts": ["web1.example.com", "web2.example.com"],
            "vars": {
                "nginx_worker_processes": 4,
                "app_env": "production"
            }
        },
        "databases": {
            "hosts": ["db1.example.com", "db2.example.com"],
            "vars": {
                "postgres_version": 15
            }
        },
        "_meta": {
            "hostvars": {
                "web1.example.com": {
                    "ansible_host": "10.0.1.10"
                },
                "web2.example.com": {
                    "ansible_host": "10.0.1.11"
                }
            }
        }
    }
    return inventory

def main():
    if len(sys.argv) == 2 and sys.argv[1] == '--list':
        print(json.dumps(get_inventory(), indent=2))
    elif len(sys.argv) == 3 and sys.argv[1] == '--host':
        # Return empty dict for host-specific vars (use _meta above)
        print(json.dumps({}))
    else:
        print("Usage: {} --list | --host <hostname>".format(sys.argv[0]))
        sys.exit(1)

if __name__ == '__main__':
    main()
```

Make executable:
```bash
chmod +x inventory/custom.py
```

Use script:
```bash
ansible-playbook -i inventory/custom.py site.yml
```

---

## Hybrid Inventory

Combine static and dynamic inventories.

```
inventory/
├── static/
│   └── hosts              # Static on-prem servers
├── aws_ec2.yml            # Dynamic AWS instances
└── azure_rm.yml           # Dynamic Azure instances
```

Run with multiple inventories:
```bash
ansible-playbook -i inventory/ site.yml
```

All inventory sources merged automatically.

---

## Inventory Variables

### Group Variables

```
group_vars/
├── all/
│   ├── common.yml         # Variables for ALL hosts
│   └── vault.yml          # Encrypted secrets for ALL
├── webservers/
│   ├── nginx.yml          # Webserver-specific vars
│   └── vault.yml          # Webserver secrets
└── databases/
    ├── postgres.yml       # Database-specific vars
    └── vault.yml          # Database secrets
```

**group_vars/all/common.yml:**
```yaml
---
# Common variables for all hosts
ntp_servers:
  - 0.pool.ntp.org
  - 1.pool.ntp.org

dns_servers:
  - 8.8.8.8
  - 8.8.4.4

ansible_user: deploy
ansible_become: yes
```

**group_vars/webservers/nginx.yml:**
```yaml
---
# Webserver-specific variables
nginx_worker_processes: "{{ ansible_processor_vcpus }}"
nginx_worker_connections: 1024
nginx_client_max_body_size: "10m"
```

### Host Variables

```
host_vars/
├── web1.example.com/
│   └── custom.yml         # Host-specific overrides
└── db1.example.com/
    └── custom.yml
```

**host_vars/web1.example.com/custom.yml:**
```yaml
---
# Host-specific overrides
nginx_worker_processes: 8
custom_config_option: "special_value"
```

### Variable Precedence

From lowest to highest:
1. Role defaults
2. Inventory file vars
3. Inventory `group_vars/all`
4. Inventory `group_vars/*`
5. Inventory `host_vars/*`
6. Playbook vars
7. Command-line extra vars (`-e`)

---

## Best Practices

### 1. Organize by Environment

```
inventory/
├── production/
│   ├── hosts
│   ├── group_vars/
│   └── host_vars/
└── staging/
    ├── hosts
    ├── group_vars/
    └── host_vars/
```

### 2. Use Consistent Naming

```ini
# Good: Clear patterns
[webservers]
web-prod-01.example.com
web-prod-02.example.com

[databases]
db-prod-01.example.com
db-prod-02.example.com

# Bad: Inconsistent
[webservers]
server1
production-web-2
```

### 3. Group by Function

```ini
[webservers]
web1.example.com
web2.example.com

[appservers]
app1.example.com
app2.example.com

[databases]
db1.example.com
db2.example.com

# Parent groups
[frontend:children]
webservers
appservers

[backend:children]
databases
```

### 4. Version Control Inventory

```
.gitignore:
*vault.yml           # Encrypted secrets
*.pem                # SSH keys
inventory/production # Production inventory (separate repo)
```

### 5. Document Inventory Structure

```markdown
# Inventory Structure

## Environments
- production/ - Production servers
- staging/ - Staging servers
- development/ - Development servers

## Groups
- webservers - NGINX web tier
- appservers - Application tier
- databases - PostgreSQL databases
- loadbalancers - HAProxy load balancers

## Variables
- group_vars/all/ - Global variables
- group_vars/{group}/ - Group-specific variables
- host_vars/{host}/ - Host-specific overrides
```

### 6. Limit Playbook Scope

```bash
# Run on specific group
ansible-playbook -i inventory site.yml --limit webservers

# Run on specific host
ansible-playbook -i inventory site.yml --limit web1.example.com

# Run on multiple hosts
ansible-playbook -i inventory site.yml --limit "web1,web2,db1"

# Exclude hosts
ansible-playbook -i inventory site.yml --limit "all:!databases"
```

### 7. Test Inventory

```bash
# List all hosts
ansible-inventory -i inventory --list

# Show graph
ansible-inventory -i inventory --graph

# Show host variables
ansible-inventory -i inventory --host web1.example.com

# Ping all hosts
ansible all -i inventory -m ping
```

### 8. Use Dynamic Inventory for Cloud

Static inventory becomes stale quickly in cloud environments. Use dynamic inventory plugins.

**Bad (manual updates):**
```ini
[webservers]
web1.example.com ansible_host=10.0.1.10  # IP changes frequently
web2.example.com ansible_host=10.0.1.11
```

**Good (auto-discovery):**
```yaml
# inventory/aws_ec2.yml
plugin: aws_ec2
filters:
  tag:Role: webserver
  instance-state-name: running
```

### 9. Separate Secrets

Don't put secrets in inventory files.

**Bad:**
```ini
[databases:vars]
db_password=SuperSecret123
```

**Good:**
```yaml
# group_vars/databases/vault.yml (encrypted)
vault_db_password: SuperSecret123

# group_vars/databases/vars.yml (unencrypted)
db_password: "{{ vault_db_password }}"
```

### 10. Use Inventory Plugins

Prefer inventory plugins over custom scripts.

**Supported plugins:**
- `aws_ec2` - AWS EC2
- `azure_rm` - Azure Resource Manager
- `gcp_compute` - Google Cloud Platform
- `openstack` - OpenStack
- `vmware_vm_inventory` - VMware
- `docker_containers` - Docker
- `kubernetes` - Kubernetes pods

List available plugins:
```bash
ansible-doc -t inventory -l
```
