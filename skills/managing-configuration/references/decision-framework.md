# Decision Framework

## Table of Contents

1. [When to Use Configuration Management](#when-to-use-configuration-management)
2. [Tool Selection: Ansible vs Chef vs Puppet](#tool-selection-ansible-vs-chef-vs-puppet)
3. [Ansible vs Infrastructure-as-Code](#ansible-vs-infrastructure-as-code)
4. [Static vs Dynamic Inventory](#static-vs-dynamic-inventory)
5. [Playbooks vs Roles](#playbooks-vs-roles)
6. [Secret Management Selection](#secret-management-selection)
7. [Testing Strategy Selection](#testing-strategy-selection)
8. [Environment Strategy](#environment-strategy)
9. [Push vs Pull Model](#push-vs-pull-model)
10. [When to Consider Alternatives](#when-to-consider-alternatives)

---

## When to Use Configuration Management

### Use Configuration Management When:

✅ Managing server/VM configurations (OS settings, packages, users)
✅ Ensuring compliance (CIS benchmarks, PCI-DSS, SOC2)
✅ Deploying applications to servers/VMs
✅ Standardizing environments (dev, staging, production)
✅ Automating operational tasks (backups, updates, monitoring)
✅ Managing cloud resources post-provisioning

### Don't Use Configuration Management For:

❌ Creating cloud infrastructure (use Terraform, CloudFormation)
❌ Container orchestration (use Kubernetes, Docker Swarm)
❌ CI/CD pipelines (use Jenkins, GitHub Actions, GitLab CI)
❌ Immutable infrastructure (use Packer for image baking)

---

## Tool Selection: Ansible vs Chef vs Puppet

### Decision Tree

```
Start
│
├─ New project / greenfield?
│  └─ YES → Ansible (easiest, modern, agentless)
│
├─ Existing Chef/Puppet?
│  ├─ Working well? → Keep it (don't migrate unnecessarily)
│  └─ Pain points? → Migrate to Ansible (assess effort)
│
├─ Windows-heavy environment?
│  ├─ Mostly Windows → Puppet (best Windows support) OR Ansible (WinRM)
│  └─ Mixed → Ansible (handles both)
│
├─ Compliance-critical enterprise?
│  ├─ Need compliance tools → Puppet (Remediate) OR Ansible (custom)
│  └─ Standard compliance → Ansible (sufficient)
│
├─ Large team, complex organization?
│  ├─ Need enterprise support → Red Hat Ansible Automation Platform
│  └─ Open source sufficient → Ansible (community)
│
└─ Cloud-native / containers?
   └─ YES → Ansible (best cloud integration, agentless)
```

### Quick Comparison

| Factor | Ansible | Chef | Puppet |
|--------|---------|------|--------|
| **Learning Curve** | Easy (YAML) | Steep (Ruby) | Moderate (DSL) |
| **Architecture** | Agentless (SSH) | Agent-based | Agent-based |
| **Best For** | Most use cases | Hybrid cloud | Windows, compliance |
| **Setup Time** | Minutes | Hours | Hours |
| **Cloud Integration** | Excellent | Good | Good |
| **Community** | Large, active | Moderate | Moderate |
| **Enterprise Support** | Red Hat | Chef Software | Puppet Inc. |

---

## Ansible vs Infrastructure-as-Code

### Use Ansible When:

- Configuring resources AFTER provisioning
- Deploying applications to existing infrastructure
- Managing OS-level settings (users, packages, services)
- Orchestrating multi-step workflows across hosts
- Operational tasks (backups, updates, maintenance)

### Use Terraform/IaC When:

- Creating cloud infrastructure (VPCs, instances, databases)
- Managing resource lifecycle (create, update, destroy)
- Defining infrastructure state declaratively
- Multi-cloud resource orchestration
- Infrastructure dependencies and ordering

### Best Practice: Use Both Together

**Workflow:**
1. **Terraform** creates AWS EC2 instances, security groups, load balancers
2. **Terraform** outputs instance IPs to Ansible inventory
3. **Ansible** configures OS, installs packages, deploys application
4. **Ansible** sets up monitoring, backups, cron jobs

**Example Terraform output:**
```hcl
output "web_servers" {
  value = {
    for instance in aws_instance.web :
    instance.tags.Name => instance.private_ip
  }
}

resource "local_file" "ansible_inventory" {
  content = templatefile("inventory.tpl", {
    web_servers = aws_instance.web
  })
  filename = "../ansible/inventory/terraform.yml"
}
```

---

## Static vs Dynamic Inventory

### Decision Matrix

| Factor | Static Inventory | Dynamic Inventory |
|--------|------------------|-------------------|
| **Environment Size** | < 50 hosts | > 50 hosts |
| **Infrastructure Change Frequency** | Rarely | Frequently (auto-scaling) |
| **Deployment Type** | On-premises | Cloud (AWS, Azure, GCP) |
| **Host Discovery** | Manual | Automatic |
| **Use Cases** | Small shops, stable infra | Cloud-native, enterprise |

### Use Static Inventory When:

- Small environment (< 50 hosts)
- Stable infrastructure (rarely changes)
- On-premises servers with fixed IPs
- Simple host grouping requirements
- No cloud integration needed

**Example:**
```ini
[webservers]
web1.example.com
web2.example.com

[databases]
db1.example.com
```

### Use Dynamic Inventory When:

- Large environment (> 50 hosts)
- Cloud-based infrastructure (AWS, Azure, GCP)
- Frequent scaling (auto-scaling groups)
- Multi-cloud or hybrid environments
- Source of truth in external system (NetBox, CMDB)

**Example:**
```yaml
# inventory/aws_ec2.yml
plugin: aws_ec2
regions:
  - us-east-1
filters:
  tag:Environment: production
  instance-state-name: running
```

### Use Hybrid Inventory When:

- Some static hosts (on-premises)
- Some dynamic hosts (cloud)
- Unified management across environments

```
inventory/
├── static/
│   └── onprem-hosts
└── aws_ec2.yml
```

---

## Playbooks vs Roles

### Use Playbooks When:

- One-time deployment tasks
- Environment-specific orchestration
- Combining multiple roles
- Custom workflow for specific application

**Example:**
```yaml
# deploy-production.yml
- hosts: webservers
  roles:
    - common
    - nginx
    - myapp
```

### Use Roles When:

- Reusable configuration units
- Shareable across projects
- Testing in isolation
- Publishing to Ansible Galaxy

**Example:**
```
roles/nginx/
├── tasks/
├── handlers/
├── templates/
└── defaults/
```

---

## Secret Management Selection

### Use ansible-vault When:

- Small teams (< 10 people)
- Simple secret management needs
- No compliance requirements
- Secrets change infrequently
- No need for audit trails
- Budget constraints

**Pros:**
- Built-in, no additional setup
- Simple to use
- Free
- Integrates seamlessly with Ansible

**Cons:**
- No dynamic secrets
- No audit logging
- Manual secret rotation
- Password-based access control

### Use HashiCorp Vault When:

- Large teams or enterprises
- Dynamic secret generation needed (database credentials)
- Compliance requirements (SOC2, PCI-DSS, HIPAA)
- Frequent secret rotation required
- Detailed audit logging needed
- Integration with multiple tools (not just Ansible)
- Cloud-native architectures

**Pros:**
- Dynamic secrets (time-limited credentials)
- Comprehensive audit logging
- Fine-grained access control (policies, roles)
- Automated secret rotation
- Multi-tool integration

**Cons:**
- Additional infrastructure to manage
- More complex setup
- Requires operational expertise
- Cost (enterprise features)

### Hybrid Approach

Use both for different security tiers:

```yaml
# Low-sensitivity: ansible-vault
app_config_param: "{{ vault_app_config }}"

# High-sensitivity: HashiCorp Vault
db_password: "{{ lookup('hashi_vault', 'secret/data/myapp:password') }}"
```

---

## Testing Strategy Selection

### Use ansible-lint When:

- Pre-commit checks
- CI/CD quality gates
- Catching common mistakes
- Enforcing best practices

**Run:** Before every commit

### Use Check Mode When:

- Manual verification before deployment
- Dry-run testing in production
- Validating changes without applying

**Run:** Before production deployments

### Use Molecule When:

- Developing reusable roles
- Testing against multiple OS distributions
- Validating idempotence
- Pre-production verification
- Publishing roles to Ansible Galaxy

**Run:** During role development

### Use Testinfra When:

- Infrastructure state verification
- Compliance testing
- Post-deployment validation
- Integration testing

**Run:** After deployments

---

## Environment Strategy

### Single Environment Inventory

**When:**
- Small deployments
- Single environment (prod only)
- Simple infrastructure

```
inventory/
└── hosts
```

### Multi-Environment Inventory

**When:**
- Development, staging, production environments
- Different configurations per environment
- Separate teams/access controls

```
inventory/
├── production/
│   ├── hosts
│   └── group_vars/
├── staging/
│   ├── hosts
│   └── group_vars/
└── development/
    ├── hosts
    └── group_vars/
```

---

## Push vs Pull Model

### Push (Default Ansible)

**When:**
- Small-to-medium environments
- Centralized control preferred
- On-demand deployments
- Cloud-based (SSH always available)

**Command:**
```bash
ansible-playbook site.yml
```

### Pull (ansible-pull)

**When:**
- Large-scale deployments (1000+ nodes)
- Autonomous node configuration
- Periodic updates (cron-based)
- Nodes behind firewalls

**Setup:**
```bash
# On managed node
ansible-pull -U https://github.com/org/ansible-repo.git site.yml
```

---

## When to Consider Alternatives

### Switch to Kubernetes when:

- Running containerized applications
- Need container orchestration
- Require service mesh features
- Horizontal scaling requirements

### Use Packer instead when:

- Building immutable images
- Image-based deployments
- Golden image creation
- No post-boot configuration needed

### Consider SaltStack when:

- Real-time remote execution needed
- Event-driven automation
- Already using Salt infrastructure

### Stick with manual when:

- One-time setup (< 5 servers)
- Exploratory/learning phase
- No repeatability requirements
- Cost of automation > cost of manual work
