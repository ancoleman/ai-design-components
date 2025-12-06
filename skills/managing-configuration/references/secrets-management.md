# Secrets Management

## Table of Contents

1. [ansible-vault (Built-in)](#ansible-vault-built-in)
2. [HashiCorp Vault Integration](#hashicorp-vault-integration)
3. [Best Practices](#best-practices)
4. [Comparison](#comparison)

---

## ansible-vault (Built-in)

### Basic Operations

**Create encrypted file:**
```bash
ansible-vault create group_vars/all/vault.yml
# Enter password when prompted
```

**Edit encrypted file:**
```bash
ansible-vault edit group_vars/all/vault.yml
```

**View encrypted file:**
```bash
ansible-vault view group_vars/all/vault.yml
```

**Encrypt existing file:**
```bash
ansible-vault encrypt secrets.yml
```

**Decrypt file:**
```bash
ansible-vault decrypt secrets.yml
```

**Change password:**
```bash
ansible-vault rekey group_vars/all/vault.yml
```

### Vault File Content

**group_vars/all/vault.yml (encrypted):**
```yaml
---
vault_db_password: "SuperSecretPassword123"
vault_api_key: "sk-abcdef123456"
vault_smtp_password: "email_password"
vault_ssl_private_key: |
  -----BEGIN PRIVATE KEY-----
  MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...
  -----END PRIVATE KEY-----
```

**Reference in unencrypted file:**

**group_vars/all/vars.yml (unencrypted):**
```yaml
---
db_host: "db.example.com"
db_user: "appuser"
db_password: "{{ vault_db_password }}"

api_endpoint: "https://api.example.com"
api_key: "{{ vault_api_key }}"
```

### Run Playbooks with Vault

**Method 1: Interactive password:**
```bash
ansible-playbook site.yml --ask-vault-pass
```

**Method 2: Password file:**
```bash
# Create password file
echo "MyVaultPassword" > ~/.vault_pass
chmod 600 ~/.vault_pass

# Run playbook
ansible-playbook site.yml --vault-password-file ~/.vault_pass
```

**Method 3: Executable script:**
```bash
# Create password script
cat > ~/.vault_pass.sh << 'EOF'
#!/bin/bash
# Fetch password from secret manager
aws secretsmanager get-secret-value \
  --secret-id ansible-vault-password \
  --query SecretString \
  --output text
EOF

chmod +x ~/.vault_pass.sh

# Run playbook
ansible-playbook site.yml --vault-password-file ~/.vault_pass.sh
```

### Multiple Vault IDs

Use different passwords for different environments.

**Create vaults with IDs:**
```bash
# Production vault
ansible-vault create group_vars/production/vault.yml --vault-id prod@prompt

# Staging vault
ansible-vault create group_vars/staging/vault.yml --vault-id staging@prompt
```

**Password files:**
```bash
# Store passwords
echo "ProductionPassword" > ~/.vault_pass_prod
echo "StagingPassword" > ~/.vault_pass_staging
chmod 600 ~/.vault_pass_*
```

**Run with specific vault ID:**
```bash
ansible-playbook site.yml \
  --vault-id prod@~/.vault_pass_prod \
  --vault-id staging@~/.vault_pass_staging
```

### Encrypt Strings

Encrypt individual strings instead of entire files.

```bash
# Encrypt string
ansible-vault encrypt_string 'SuperSecret123' --name 'db_password'
```

**Output:**
```yaml
db_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          66386439653033653834303138656337353833656362393137313633633732306362333...
```

**Use in playbook:**
```yaml
---
- name: Configure database
  hosts: databases
  vars:
    db_user: appuser
    db_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          66386439653033653834303138656337353833656362393137313633633732306362333...

  tasks:
    - name: Create database user
      postgresql_user:
        name: "{{ db_user }}"
        password: "{{ db_password }}"
```

### ansible.cfg Configuration

```ini
[defaults]
vault_password_file = ~/.vault_pass

# Or multiple vault IDs
vault_identity_list = prod@~/.vault_pass_prod, staging@~/.vault_pass_staging
```

---

## HashiCorp Vault Integration

### Prerequisites

**Install collection:**
```bash
ansible-galaxy collection install community.hashi_vault
```

**Vault server setup:**
```bash
# Start Vault (dev mode for testing)
vault server -dev

# Set environment
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='dev-token'

# Create secrets
vault kv put secret/myapp/database \
  host=db.example.com \
  username=appuser \
  password=SuperSecret123

vault kv put secret/myapp/api \
  endpoint=https://api.example.com \
  key=sk-abcdef123456
```

### Lookup Secrets in Playbooks

**Method 1: KV v2 secrets (default):**
```yaml
---
- name: Configure application
  hosts: appservers
  vars:
    vault_addr: "http://127.0.0.1:8200"
    vault_token: "{{ lookup('env', 'VAULT_TOKEN') }}"

  tasks:
    - name: Fetch database password from Vault
      set_fact:
        db_config: "{{ lookup('community.hashi_vault.vault_kv2_get', 'secret/data/myapp/database', url=vault_addr, token=vault_token) }}"

    - name: Configure database connection
      template:
        src: database.conf.j2
        dest: /etc/myapp/database.conf
      vars:
        db_host: "{{ db_config.secret.host }}"
        db_user: "{{ db_config.secret.username }}"
        db_password: "{{ db_config.secret.password }}"
```

**Method 2: Direct lookup:**
```yaml
- name: Read secret value
  debug:
    msg: "{{ lookup('community.hashi_vault.vault_read', 'secret/data/myapp/database').data.data.password }}"
```

**Method 3: Using hashi_vault lookup (legacy):**
```yaml
- name: Fetch API key
  set_fact:
    api_key: "{{ lookup('community.hashi_vault.hashi_vault', 'secret/myapp/api:key') }}"
```

### Authentication Methods

**Token auth (simple):**
```yaml
vars:
  vault_token: "{{ lookup('env', 'VAULT_TOKEN') }}"

lookup('community.hashi_vault.vault_kv2_get',
       'secret/data/myapp/database',
       token=vault_token)
```

**AppRole auth (production):**
```yaml
vars:
  vault_role_id: "{{ lookup('env', 'VAULT_ROLE_ID') }}"
  vault_secret_id: "{{ lookup('env', 'VAULT_SECRET_ID') }}"

lookup('community.hashi_vault.vault_kv2_get',
       'secret/data/myapp/database',
       role_id=vault_role_id,
       secret_id=vault_secret_id)
```

**AWS IAM auth:**
```yaml
lookup('community.hashi_vault.vault_kv2_get',
       'secret/data/myapp/database',
       auth_method='aws_iam',
       mount_point='aws')
```

### Dynamic Secrets

Generate credentials on-demand.

**Database credentials:**
```yaml
- name: Generate dynamic database credentials
  set_fact:
    db_creds: "{{ lookup('community.hashi_vault.vault_read', 'database/creds/myapp-role') }}"

- name: Use dynamic credentials
  debug:
    msg: |
      Username: {{ db_creds.data.username }}
      Password: {{ db_creds.data.password }}
      Lease: {{ db_creds.lease_duration }} seconds
```

**AWS credentials:**
```yaml
- name: Generate AWS credentials
  set_fact:
    aws_creds: "{{ lookup('community.hashi_vault.vault_read', 'aws/creds/deploy-role') }}"

- name: Use AWS credentials
  aws_s3:
    aws_access_key: "{{ aws_creds.data.access_key }}"
    aws_secret_key: "{{ aws_creds.data.secret_key }}"
    bucket: mybucket
    object: myfile
    mode: put
```

### Template Example

**templates/database.conf.j2:**
```jinja2
# Database Configuration
{% set db = lookup('community.hashi_vault.vault_kv2_get', 'secret/data/myapp/database') %}

[database]
host = {{ db.secret.host }}
port = {{ db.secret.port | default(5432) }}
name = {{ db.secret.database }}
user = {{ db.secret.username }}
password = {{ db.secret.password }}

[connection]
pool_size = {{ db_pool_size | default(10) }}
```

---

## Best Practices

### 1. Separate Secrets from Configuration

**Good structure:**
```
group_vars/
├── all/
│   ├── vars.yml        # Unencrypted config
│   └── vault.yml       # Encrypted secrets
└── production/
    ├── vars.yml
    └── vault.yml
```

**vars.yml (unencrypted):**
```yaml
db_host: "db.example.com"
db_user: "appuser"
db_password: "{{ vault_db_password }}"
```

**vault.yml (encrypted):**
```yaml
vault_db_password: "SuperSecret123"
```

### 2. Prefix Vault Variables

```yaml
# Good: Clear which vars are from vault
vault_db_password: "secret"
vault_api_key: "secret"
vault_ssl_cert: "secret"

# Bad: Unclear source
db_password: "secret"
api_key: "secret"
ssl_cert: "secret"
```

### 3. Never Commit Unencrypted Secrets

**.gitignore:**
```
# Vault password files
.vault_pass*
vault_password*

# Decrypted files (if working locally)
*_decrypted.yml
secrets_plain.yml

# SSH keys
*.pem
id_rsa
```

### 4. Rotate Secrets Regularly

```bash
# Update secret in vault
ansible-vault edit group_vars/all/vault.yml

# Rotate vault password
ansible-vault rekey group_vars/all/vault.yml
```

### 5. Use Different Passwords per Environment

```
.vault_pass_production   # Production password
.vault_pass_staging      # Staging password
.vault_pass_development  # Development password
```

### 6. Audit Secret Access

With HashiCorp Vault:
```bash
# Enable audit logging
vault audit enable file file_path=/var/log/vault_audit.log

# View audit log
tail -f /var/log/vault_audit.log
```

### 7. Limit Secret Scope

Don't put all secrets in one file.

**Good:**
```
group_vars/
├── webservers/
│   └── vault.yml      # Only web secrets
└── databases/
    └── vault.yml      # Only DB secrets
```

**Bad:**
```
group_vars/
└── all/
    └── vault.yml      # All secrets (unnecessary exposure)
```

### 8. Test Vault Access

```bash
# Test vault decryption
ansible-vault view group_vars/all/vault.yml --vault-password-file ~/.vault_pass

# Test playbook with vault
ansible-playbook site.yml --check --vault-password-file ~/.vault_pass
```

### 9. Use Vault for CI/CD

**GitHub Actions example:**
```yaml
- name: Run Ansible playbook
  env:
    VAULT_PASSWORD: ${{ secrets.VAULT_PASSWORD }}
  run: |
    echo "$VAULT_PASSWORD" > .vault_pass
    ansible-playbook site.yml --vault-password-file .vault_pass
    rm .vault_pass
```

### 10. Document Secret Requirements

**README.md:**
```markdown
## Required Secrets

### ansible-vault
- `vault_db_password` - PostgreSQL password
- `vault_api_key` - External API key
- `vault_ssl_private_key` - SSL private key

### HashiCorp Vault Paths
- `secret/myapp/database` - Database credentials
- `secret/myapp/api` - API configuration
- `secret/myapp/ssl` - SSL certificates
```

---

## Comparison

| Feature | ansible-vault | HashiCorp Vault |
|---------|---------------|-----------------|
| **Complexity** | Simple | Complex setup |
| **Dynamic secrets** | No | Yes |
| **Audit logging** | No | Yes |
| **Secret rotation** | Manual | Automated |
| **Access control** | Password-based | Policies, roles |
| **Integration** | Built-in | Requires plugin |
| **Best for** | Small teams, simple needs | Enterprise, compliance |
| **Cost** | Free | Free (OSS) / Paid (Enterprise) |

### When to Use ansible-vault

- Small teams (< 10 people)
- Simple secret management needs
- No compliance requirements
- Secrets change infrequently
- No need for audit trails

### When to Use HashiCorp Vault

- Large teams or enterprises
- Dynamic secret generation needed
- Compliance requirements (SOC2, PCI-DSS)
- Frequent secret rotation
- Detailed audit logging required
- Integration with multiple tools (not just Ansible)
- Cloud-native architectures

### Hybrid Approach

Use both for different purposes:

```yaml
# Low-sensitivity config: ansible-vault
vault_app_config: "non-critical-config"

# High-sensitivity credentials: HashiCorp Vault
db_password: "{{ lookup('community.hashi_vault.vault_kv2_get', 'secret/data/myapp/database').secret.password }}"
```
