# Azure Identity and Access Management Reference

Comprehensive guide to Azure Entra ID, Managed Identity, and RBAC patterns.

## Table of Contents

1. [Managed Identity](#managed-identity)
2. [Azure RBAC](#azure-rbac)
3. [Entra ID (Azure AD)](#entra-id-azure-ad)
4. [Conditional Access](#conditional-access)

---

## Managed Identity

Azure-managed identity for applications to authenticate to Azure services without storing credentials.

### System-Assigned vs. User-Assigned

| Aspect | System-Assigned | User-Assigned |
|--------|----------------|---------------|
| **Lifecycle** | Tied to resource | Independent |
| **Sharing** | One resource only | Multiple resources |
| **Use Case** | Single resource needs access | Shared identity across resources |
| **Deletion** | Auto-deleted with resource | Manual deletion |

### Common Access Patterns

```python
from azure.identity import DefaultAzureCredential

# Works with both system and user-assigned identities
credential = DefaultAzureCredential()

# Use with any Azure SDK
from azure.keyvault.secrets import SecretClient
client = SecretClient(vault_url="https://mykv.vault.azure.net", credential=credential)
```

---

## Azure RBAC

Role-Based Access Control for fine-grained permissions.

### Built-In Roles

| Role | Permissions | Use Case |
|------|-------------|----------|
| **Owner** | Full access + manage access | Subscription/RG admins |
| **Contributor** | Full access (no access mgmt) | Developers, operators |
| **Reader** | Read-only | Auditors, viewers |
| **Key Vault Secrets User** | Read secrets | Apps accessing secrets |
| **Storage Blob Data Contributor** | Read/write blobs | Apps using Blob Storage |

### Best Practices

- Assign roles at Resource Group level (not subscription)
- Use built-in roles when possible
- Create custom roles only when necessary
- Assign to Azure AD groups (not individual users)
- Audit role assignments quarterly

---

## Entra ID (Azure AD)

Cloud-based identity and access management service.

### Authentication Patterns

- OAuth 2.0 / OpenID Connect
- SAML 2.0 (for legacy apps)
- Managed Identity (for Azure resources)

### Multi-Tenant Applications

Register app in Entra ID for multi-org SaaS applications.

---

## Conditional Access

Risk-based access policies.

### Common Policies

- Require MFA for admins
- Block legacy authentication
- Require compliant devices
- Restrict access by location
- Require approved client apps
