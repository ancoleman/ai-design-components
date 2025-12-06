# Authorization Patterns: RBAC, ABAC, and ReBAC

Authorization determines what authenticated users can access and modify.


## Table of Contents

- [Authorization Model Comparison](#authorization-model-comparison)
- [RBAC (Role-Based Access Control)](#rbac-role-based-access-control)
  - [Structure](#structure)
  - [Example Schema](#example-schema)
  - [Implementation with Casbin](#implementation-with-casbin)
  - [When to Use RBAC](#when-to-use-rbac)
  - [RBAC Limitations](#rbac-limitations)
- [ABAC (Attribute-Based Access Control)](#abac-attribute-based-access-control)
  - [Structure](#structure)
  - [Example Policies (OPA Rego)](#example-policies-opa-rego)
  - [Implementation with OPA (Open Policy Agent)](#implementation-with-opa-open-policy-agent)
  - [When to Use ABAC](#when-to-use-abac)
  - [ABAC Limitations](#abac-limitations)
- [ReBAC (Relationship-Based Access Control)](#rebac-relationship-based-access-control)
  - [Structure](#structure)
  - [Example Schema (SpiceDB)](#example-schema-spicedb)
  - [Relationships](#relationships)
  - [Permission Checks](#permission-checks)
  - [Implementation with SpiceDB](#implementation-with-spicedb)
  - [When to Use ReBAC](#when-to-use-rebac)
  - [ReBAC Limitations](#rebac-limitations)
- [Authorization Engine Selection](#authorization-engine-selection)
  - [Casbin (RBAC/ABAC)](#casbin-rbacabac)
  - [OPA (Open Policy Agent)](#opa-open-policy-agent)
  - [Cerbos](#cerbos)
  - [SpiceDB (ReBAC)](#spicedb-rebac)
- [Implementation Patterns](#implementation-patterns)
  - [Middleware Pattern (Express)](#middleware-pattern-express)
  - [Decorator Pattern (FastAPI)](#decorator-pattern-fastapi)
  - [Row-Level Security (Database)](#row-level-security-database)
- [Audit Logging](#audit-logging)
  - [OPA Decision Logs](#opa-decision-logs)
  - [Custom Audit Logging](#custom-audit-logging)
- [Testing Authorization](#testing-authorization)
  - [Unit Tests](#unit-tests)
  - [Integration Tests](#integration-tests)
- [Performance Optimization](#performance-optimization)
  - [Caching](#caching)
  - [Batch Checks](#batch-checks)
- [Common Pitfalls](#common-pitfalls)
  - [Pitfall 1: Authorization in Frontend Only](#pitfall-1-authorization-in-frontend-only)
  - [Pitfall 2: Hardcoded Permissions](#pitfall-2-hardcoded-permissions)
  - [Pitfall 3: No Audit Trail](#pitfall-3-no-audit-trail)

## Authorization Model Comparison

| Model | Complexity | Use Case | Example |
|-------|------------|----------|---------|
| **ACL** | Low | Simple file systems | User A can read file.txt |
| **RBAC** | Medium | Enterprise applications | Admins can delete users |
| **ABAC** | High | Complex policies | Allow if clearance >= classification |
| **ReBAC** | Very High | Multi-tenant, collaborative | Can edit if member of workspace |

## RBAC (Role-Based Access Control)

Assign permissions to roles, then assign roles to users.

### Structure

```
Users → Roles → Permissions → Resources
```

### Example Schema

```
Roles:
  - Admin: [users:create, users:delete, posts:delete]
  - Editor: [posts:create, posts:update, posts:delete]
  - Viewer: [posts:read]

Users:
  - alice: [Admin]
  - bob: [Editor]
  - charlie: [Viewer]
```

### Implementation with Casbin

**Policy File (policy.csv):**
```csv
p, admin, users, create
p, admin, users, delete
p, admin, posts, delete
p, editor, posts, create
p, editor, posts, update
p, editor, posts, delete
p, viewer, posts, read

g, alice, admin
g, bob, editor
g, charlie, viewer
```

**Model File (model.conf):**
```ini
[request_definition]
r = sub, obj, act

[policy_definition]
p = sub, obj, act

[role_definition]
g = _, _

[policy_effect]
e = some(where (p.eft == allow))

[matchers]
m = g(r.sub, p.sub) && r.obj == p.obj && r.act == p.act
```

**TypeScript:**
```typescript
import { newEnforcer } from 'casbin'

const enforcer = await newEnforcer('model.conf', 'policy.csv')

// Check permission
const allowed = await enforcer.enforce('alice', 'users', 'delete')
console.log(allowed) // true (alice is admin)

const denied = await enforcer.enforce('bob', 'users', 'delete')
console.log(denied) // false (bob is editor)
```

**Python:**
```python
import casbin

enforcer = casbin.Enforcer('model.conf', 'policy.csv')

# Check permission
allowed = enforcer.enforce('alice', 'users', 'delete')
print(allowed)  # True

# Add role
enforcer.add_role_for_user('dave', 'editor')

# Add permission
enforcer.add_permission_for_user('editor', 'comments', 'moderate')
```

### When to Use RBAC

- **Simple role hierarchies** (< 20 roles)
- **Clear permission boundaries** (admin vs user)
- **Infrequent role changes**
- **Static permissions** (not context-dependent)

### RBAC Limitations

- **Role explosion:** Complex organizations need many roles
- **No context:** Can't express "owner can delete their own posts"
- **Hard to audit:** "Who can access resource X?" requires traversing graph

## ABAC (Attribute-Based Access Control)

Policies based on attributes of user, resource, and environment.

### Structure

```
Policy: Allow if
  user.department == resource.department AND
  user.clearance >= resource.classification AND
  time.hour >= 9 AND time.hour < 17
```

### Example Policies (OPA Rego)

```rego
package authz

# Allow if user is admin
allow {
  input.user.role == "admin"
}

# Allow if user owns the resource
allow {
  input.user.id == input.resource.owner_id
}

# Allow if user's clearance >= resource's classification
allow {
  input.user.clearance >= input.resource.classification
  input.user.department == input.resource.department
}

# Allow if within business hours
allow {
  hour := time.clock(input.time)[0]
  hour >= 9
  hour < 17
}
```

**Query OPA:**
```bash
curl -X POST http://localhost:8181/v1/data/authz/allow \
  -d '{
    "input": {
      "user": {"id": "alice", "role": "editor", "clearance": 3, "department": "eng"},
      "resource": {"id": "doc-123", "owner_id": "bob", "classification": 2, "department": "eng"},
      "action": "read",
      "time": "2025-12-02T14:00:00Z"
    }
  }'
```

**Response:**
```json
{
  "result": true
}
```

### Implementation with OPA (Open Policy Agent)

**TypeScript:**
```typescript
import axios from 'axios'

async function checkPermission(
  user: { id: string; role: string; clearance: number },
  resource: { id: string; classification: number },
  action: string
): Promise<boolean> {
  const response = await axios.post('http://localhost:8181/v1/data/authz/allow', {
    input: { user, resource, action },
  })

  return response.data.result === true
}

// Usage
const allowed = await checkPermission(
  { id: 'alice', role: 'editor', clearance: 3 },
  { id: 'doc-123', classification: 2 },
  'read'
)
```

**Python:**
```python
import requests

def check_permission(user, resource, action):
    response = requests.post(
        'http://localhost:8181/v1/data/authz/allow',
        json={'input': {'user': user, 'resource': resource, 'action': action}}
    )
    return response.json().get('result') == True

# Usage
allowed = check_permission(
    {'id': 'alice', 'role': 'editor', 'clearance': 3},
    {'id': 'doc-123', 'classification': 2},
    'read'
)
```

### When to Use ABAC

- **Complex conditional rules**
- **Context-dependent permissions** (time, location, device)
- **Fine-grained access control**
- **Compliance requirements** (HIPAA, SOC 2)

### ABAC Limitations

- **Policy complexity:** Hard to write and maintain complex policies
- **Performance:** Evaluating many attributes can be slow
- **Debugging:** Hard to understand why access was denied

## ReBAC (Relationship-Based Access Control)

Permissions based on relationships between entities (Google Zanzibar model).

### Structure

```
User → Relationship → Group → Relationship → Resource
```

### Example Schema (SpiceDB)

```zed
// Define user type
definition user {}

// Define workspace with members and admins
definition workspace {
    relation member: user
    relation admin: user

    permission view = member + admin
    permission edit = admin
}

// Define document within workspace
definition document {
    relation workspace: workspace
    relation writer: user

    permission view = workspace->view + writer
    permission edit = workspace->edit + writer
}
```

### Relationships

```
// alice is admin of workspace:acme
workspace:acme#admin@user:alice

// bob is member of workspace:acme
workspace:acme#member@user:bob

// doc:123 is in workspace:acme
document:doc-123#workspace@workspace:acme

// charlie is writer of doc:123
document:doc-123#writer@user:charlie
```

### Permission Checks

```bash
# Can alice edit doc:123?
spicedb check user:alice edit document:doc-123
# → true (alice is admin of workspace, doc is in workspace)

# Can bob edit doc:123?
spicedb check user:bob edit document:doc-123
# → false (bob is member, not admin)

# Can charlie edit doc:123?
spicedb check user:charlie edit document:doc-123
# → true (charlie is writer of doc)
```

### Implementation with SpiceDB

**TypeScript:**
```typescript
import { v1 } from '@authzed/authzed-node'

const client = v1.NewClient(
  'grpcs://localhost:50051',
  v1.ClientSecurity.TLS_INSECURE
)

// Check permission
async function checkPermission(
  userId: string,
  permission: string,
  resourceType: string,
  resourceId: string
): Promise<boolean> {
  const response = await client.checkPermission({
    resource: { objectType: resourceType, objectId: resourceId },
    permission,
    subject: { object: { objectType: 'user', objectId: userId } },
  })

  return response.permissionship === v1.CheckPermissionResponse_Permissionship.HAS_PERMISSION
}

// Usage
const canEdit = await checkPermission('alice', 'edit', 'document', 'doc-123')
```

**Python:**
```python
from authzed.api.v1 import Client, CheckPermissionRequest, SubjectReference, ObjectReference

client = Client('grpcs://localhost:50051', 'token')

def check_permission(user_id, permission, resource_type, resource_id):
    request = CheckPermissionRequest(
        resource=ObjectReference(object_type=resource_type, object_id=resource_id),
        permission=permission,
        subject=SubjectReference(object=ObjectReference(object_type='user', object_id=user_id)),
    )
    response = client.permissions_service.check_permission(request)
    return response.permissionship == 2  # HAS_PERMISSION

# Usage
can_edit = check_permission('alice', 'edit', 'document', 'doc-123')
```

### When to Use ReBAC

- **Multi-tenant applications** (Notion, Google Docs, GitHub)
- **Collaborative tools** (shared workspaces)
- **Hierarchical organizations** (teams, departments)
- **Complex permission inheritance**

### ReBAC Limitations

- **Complexity:** Requires understanding graph traversal
- **Setup overhead:** Need dedicated service (SpiceDB)
- **Performance:** Deep graph traversal can be slow
- **Debugging:** Hard to visualize permission paths

## Authorization Engine Selection

### Casbin (RBAC/ABAC)

**Languages:** Go, Python, Rust, JavaScript, Java, PHP

**Best For:**
- Embedded application logic
- Simple to medium complexity
- Multi-language projects

**Pros:**
- Easy to integrate (library, not service)
- Supports multiple models (RBAC, ABAC, ACL)
- Fast (in-process)

**Cons:**
- Limited to single-process (no distributed)
- No relationship graphs

**Example:**
```typescript
import { newEnforcer } from 'casbin'

const enforcer = await newEnforcer('model.conf', 'policy.csv')
const allowed = await enforcer.enforce('alice', 'data', 'read')
```

### OPA (Open Policy Agent)

**Language:** Rego (policy language)

**Best For:**
- Kubernetes admission control
- Infrastructure policies
- Complex attribute-based rules

**Pros:**
- Powerful policy language (Rego)
- Decoupled from application
- Decision logging (audit trail)
- CNCF graduated project

**Cons:**
- Learning curve (Rego syntax)
- Requires separate service
- Not relationship-aware

**Example:**
```rego
allow {
  input.user.role == "admin"
}
```

### Cerbos

**Language:** Go

**Best For:**
- API-first authorization
- Policy-as-code (Git-backed)
- gRPC/REST APIs

**Pros:**
- Developer-friendly (YAML policies)
- Git workflow (version control, PR reviews)
- Audit logs built-in

**Cons:**
- Requires service deployment
- Not relationship-aware

**Example (YAML):**
```yaml
apiVersion: api.cerbos.dev/v1
resourcePolicy:
  version: "default"
  resource: "document"
  rules:
    - actions: ["read"]
      effect: EFFECT_ALLOW
      roles: ["viewer", "editor", "admin"]
```

### SpiceDB (ReBAC)

**Language:** Go

**Best For:**
- Multi-tenant applications
- Collaborative tools
- Google Zanzibar-style permissions

**Pros:**
- Relationship graphs (powerful)
- Sub-second performance
- Distributed consistency

**Cons:**
- Complex setup (requires dedicated service)
- Steep learning curve
- Overkill for simple RBAC

**Example:**
```bash
spicedb check user:alice edit document:doc-123
```

## Implementation Patterns

### Middleware Pattern (Express)

```typescript
import { enforcer } from './casbin'

export function authorize(resource: string, action: string) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const userId = req.user?.id

    if (!userId) {
      return res.status(401).json({ error: 'Unauthorized' })
    }

    const allowed = await enforcer.enforce(userId, resource, action)

    if (!allowed) {
      return res.status(403).json({ error: 'Forbidden' })
    }

    next()
  }
}

// Usage
app.delete('/api/users/:id', authorize('users', 'delete'), deleteUser)
```

### Decorator Pattern (FastAPI)

```python
from functools import wraps
from fastapi import HTTPException

def authorize(resource: str, action: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_id = kwargs.get('user_id')
            if not user_id:
                raise HTTPException(401, "Unauthorized")

            allowed = enforcer.enforce(user_id, resource, action)
            if not allowed:
                raise HTTPException(403, "Forbidden")

            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Usage
@app.delete("/api/users/{user_id}")
@authorize("users", "delete")
async def delete_user(user_id: str):
    pass
```

### Row-Level Security (Database)

Postgres Row-Level Security (RLS) with policies:

```sql
-- Enable RLS on table
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Policy: Users can read documents in their workspace
CREATE POLICY documents_read_policy ON documents
  FOR SELECT
  USING (
    workspace_id IN (
      SELECT workspace_id FROM workspace_members
      WHERE user_id = current_setting('app.user_id')::uuid
    )
  );

-- Policy: Admins can update any document
CREATE POLICY documents_update_policy ON documents
  FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM users
      WHERE id = current_setting('app.user_id')::uuid
      AND role = 'admin'
    )
  );
```

**Set user context:**
```typescript
await db.query('SET app.user_id = $1', [userId])
const docs = await db.query('SELECT * FROM documents')
// Only returns documents user can read
```

## Audit Logging

Track authorization decisions for compliance.

### OPA Decision Logs

```bash
# Enable decision logging
opa run --server --set decision_logs.console=true
```

**Decision log entry:**
```json
{
  "input": {
    "user": {"id": "alice", "role": "editor"},
    "resource": {"id": "doc-123"},
    "action": "delete"
  },
  "result": false,
  "timestamp": "2025-12-02T14:30:00Z"
}
```

### Custom Audit Logging

```typescript
async function checkPermissionWithAudit(
  userId: string,
  resource: string,
  action: string
): Promise<boolean> {
  const allowed = await enforcer.enforce(userId, resource, action)

  // Log decision
  await db.auditLogs.create({
    userId,
    resource,
    action,
    allowed,
    timestamp: new Date(),
    ip: req.ip,
    userAgent: req.headers['user-agent'],
  })

  return allowed
}
```

## Testing Authorization

### Unit Tests

```typescript
import { expect, test } from 'vitest'
import { enforcer } from './casbin'

test('admin can delete users', async () => {
  const allowed = await enforcer.enforce('admin', 'users', 'delete')
  expect(allowed).toBe(true)
})

test('editor cannot delete users', async () => {
  const allowed = await enforcer.enforce('editor', 'users', 'delete')
  expect(allowed).toBe(false)
})
```

### Integration Tests

```typescript
test('DELETE /api/users/:id requires admin role', async () => {
  // Alice is editor
  const response = await request(app)
    .delete('/api/users/123')
    .set('Authorization', `Bearer ${aliceToken}`)

  expect(response.status).toBe(403)
  expect(response.body.error).toBe('Forbidden')
})
```

## Performance Optimization

### Caching

```typescript
const permissionCache = new Map<string, boolean>()

async function checkPermissionCached(
  userId: string,
  resource: string,
  action: string
): Promise<boolean> {
  const cacheKey = `${userId}:${resource}:${action}`

  if (permissionCache.has(cacheKey)) {
    return permissionCache.get(cacheKey)!
  }

  const allowed = await enforcer.enforce(userId, resource, action)
  permissionCache.set(cacheKey, allowed)

  // Expire after 5 minutes
  setTimeout(() => permissionCache.delete(cacheKey), 5 * 60 * 1000)

  return allowed
}
```

### Batch Checks

```typescript
async function checkPermissionsBatch(
  userId: string,
  permissions: Array<{ resource: string; action: string }>
): Promise<Map<string, boolean>> {
  const results = new Map<string, boolean>()

  await Promise.all(
    permissions.map(async ({ resource, action }) => {
      const allowed = await enforcer.enforce(userId, resource, action)
      results.set(`${resource}:${action}`, allowed)
    })
  )

  return results
}
```

## Common Pitfalls

### Pitfall 1: Authorization in Frontend Only

**Bad:**
```typescript
// Only in frontend
if (user.role === 'admin') {
  return <DeleteButton />
}
```

**Good:**
```typescript
// Frontend
if (user.role === 'admin') {
  return <DeleteButton />
}

// Backend (always validate)
app.delete('/api/users/:id', authorize('users', 'delete'), deleteUser)
```

### Pitfall 2: Hardcoded Permissions

**Bad:**
```typescript
if (user.role === 'admin') {
  // Allow
}
```

**Good:**
```typescript
const allowed = await enforcer.enforce(user.id, resource, action)
if (allowed) {
  // Allow
}
```

### Pitfall 3: No Audit Trail

**Bad:**
```typescript
return await enforcer.enforce(user.id, resource, action)
```

**Good:**
```typescript
const allowed = await enforcer.enforce(user.id, resource, action)
await logAuthorizationDecision(user.id, resource, action, allowed)
return allowed
```
