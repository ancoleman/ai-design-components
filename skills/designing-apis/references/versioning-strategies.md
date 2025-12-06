# API Versioning Strategies

Comprehensive guide to API versioning approaches, breaking change management, and deprecation policies.

## Table of Contents

1. [Why Version APIs](#why-version-apis)
2. [Versioning Strategies](#versioning-strategies)
3. [Breaking vs Non-Breaking Changes](#breaking-vs-non-breaking-changes)
4. [Deprecation Process](#deprecation-process)
5. [Migration Patterns](#migration-patterns)
6. [Version Strategy Selection](#version-strategy-selection)

## Why Version APIs

### Business Drivers

**Backward Compatibility:**
- Old clients continue working while new features are added
- Gradual migration reduces risk
- Multiple client versions coexist

**Evolving Requirements:**
- Business needs change over time
- New features require API changes
- Technical debt must be addressed

**Multiple Clients:**
- Web, mobile, desktop apps on different release cycles
- Third-party integrations with varying upgrade capabilities
- Internal services with independent deployments

### Consequences of Poor Versioning

- Broken production integrations
- Client downtime during upgrades
- Support burden for unlimited old versions
- Technical debt accumulation
- Lost customer trust

## Versioning Strategies

### 1. URL Path Versioning (Recommended)

**Format:**
```
https://api.example.com/v1/users
https://api.example.com/v2/users
```

**Pros:**
- ✅ Highly visible and explicit
- ✅ Easy to implement and test
- ✅ Works with all HTTP clients
- ✅ Simplifies caching (different URLs)
- ✅ Clear in logs and documentation
- ✅ Easy to route to different codebases

**Cons:**
- ❌ Not strictly RESTful (resource identity changes)
- ❌ Maintenance overhead (multiple codebases)
- ❌ URLs become longer

**Implementation Example:**

Structure:
```
/api/v1/users  → v1_routes
/api/v2/users  → v2_routes
```

Express.js:
```javascript
const v1Router = require('./routes/v1');
const v2Router = require('./routes/v2');

app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);
```

FastAPI:
```python
from fastapi import APIRouter

v1_router = APIRouter(prefix="/api/v1")
v2_router = APIRouter(prefix="/api/v2")

app.include_router(v1_router)
app.include_router(v2_router)
```

**When to Use:**
- Public APIs with diverse clients
- APIs with long support windows
- When visibility is important
- When testing ease is critical

### 2. Header-Based Versioning

**Format:**
```http
GET /api/users
Accept-Version: v1
```

or

```http
GET /api/users
X-API-Version: 2
```

**Pros:**
- ✅ Clean URLs (resource identity preserved)
- ✅ RESTful principles maintained
- ✅ Supports content negotiation
- ✅ Easy to add new versions without URL changes

**Cons:**
- ❌ Less visible (hidden in headers)
- ❌ Harder to test in browser
- ❌ Requires middleware/header parsing
- ❌ Not cacheable by default (Vary header needed)

**Implementation Example:**

Express.js:
```javascript
app.use((req, res, next) => {
  const version = req.headers['accept-version'] || 'v1';
  req.apiVersion = version;
  next();
});

router.get('/users', (req, res) => {
  if (req.apiVersion === 'v2') {
    return v2.getUsers(req, res);
  }
  return v1.getUsers(req, res);
});
```

**Caching Considerations:**
```http
Vary: Accept-Version
```

**When to Use:**
- Internal APIs
- APIs where clean URLs are prioritized
- When strong RESTful principles required

### 3. Media Type Versioning

**Format:**
```http
GET /api/users
Accept: application/vnd.example.v1+json
```

**Custom Media Types:**
- `application/vnd.example.v1+json` (version 1)
- `application/vnd.example.v2+json` (version 2)

**Pros:**
- ✅ True content negotiation
- ✅ RESTful and semantic
- ✅ Allows multiple representations per version

**Cons:**
- ❌ Complex implementation
- ❌ Requires proper Accept header handling
- ❌ Less discoverable
- ❌ Not widely adopted

**Implementation Example:**

```javascript
app.use((req, res, next) => {
  const accept = req.headers['accept'] || 'application/json';

  if (accept.includes('vnd.example.v2+json')) {
    req.apiVersion = 'v2';
  } else {
    req.apiVersion = 'v1';
  }

  next();
});
```

**Response:**
```http
200 OK
Content-Type: application/vnd.example.v2+json
```

**When to Use:**
- APIs with strong REST requirements
- Multiple representation formats per version
- When content negotiation is already used

### 4. Query Parameter Versioning

**Format:**
```
https://api.example.com/users?version=1
https://api.example.com/users?v=2
```

**Pros:**
- ✅ Easy to test
- ✅ Visible in URL

**Cons:**
- ❌ Clutters query string
- ❌ Not RESTful
- ❌ Complicates caching
- ❌ Mixes with other parameters

**Implementation Example:**

```javascript
router.get('/users', (req, res) => {
  const version = req.query.version || req.query.v || '1';

  if (version === '2') {
    return v2.getUsers(req, res);
  }
  return v1.getUsers(req, res);
});
```

**When to Use:**
- Prototyping only
- Internal APIs with short lifespan
- **NOT recommended for production**

### 5. Semantic Versioning

**Format:** `MAJOR.MINOR.PATCH`

Example: `2.1.3`

**Version Increments:**
- **MAJOR**: Breaking changes (2.0.0 → 3.0.0)
- **MINOR**: New features, backward compatible (2.0.0 → 2.1.0)
- **PATCH**: Bug fixes, backward compatible (2.0.0 → 2.0.1)

**Usage:**
```http
GET /api/users
Accept-Version: 2.1.3

or

GET /api/v2.1/users
```

**When to Use:**
- Libraries and SDKs
- Internal service APIs with frequent updates
- When fine-grained versioning needed

## Breaking vs Non-Breaking Changes

### Breaking Changes (Require New Version)

**Field Changes:**
- ❌ Remove field from response
- ❌ Rename field
- ❌ Change field type (string → number)
- ❌ Make optional field required
- ❌ Change field validation rules (stricter)

**Endpoint Changes:**
- ❌ Remove endpoint
- ❌ Change URL structure
- ❌ Change HTTP method
- ❌ Change request/response format

**Behavior Changes:**
- ❌ Change status code semantics
- ❌ Change error response format
- ❌ Change pagination behavior
- ❌ Change sorting defaults

**Authentication Changes:**
- ❌ Change authentication mechanism
- ❌ Change token format
- ❌ Remove authentication method

### Non-Breaking Changes (No New Version)

**Additions:**
- ✅ Add new endpoint
- ✅ Add new optional field to request
- ✅ Add new field to response
- ✅ Add new optional query parameter
- ✅ Add new HTTP method to existing resource

**Relaxations:**
- ✅ Make required field optional
- ✅ Relax validation rules
- ✅ Accept additional input formats

**Bug Fixes:**
- ✅ Fix incorrect behavior
- ✅ Fix error messages
- ✅ Performance improvements

### Example Breaking Change

**v1:**
```json
{
  "name": "Alice Smith",
  "email": "alice@example.com"
}
```

**v2 (Breaking - field split):**
```json
{
  "firstName": "Alice",
  "lastName": "Smith",
  "email": "alice@example.com"
}
```

### Example Non-Breaking Change

**v1:**
```json
{
  "id": "123",
  "username": "alice"
}
```

**v1.1 (Non-breaking - field added):**
```json
{
  "id": "123",
  "username": "alice",
  "avatar": "https://cdn.example.com/avatar.jpg"
}
```

## Deprecation Process

### Timeline

**Standard Deprecation Timeline:**
```
Month 0: Announce deprecation
  ├─ Update documentation
  ├─ Send notifications to API consumers
  └─ Add deprecation warnings to responses

Months 1-3: Migration period
  ├─ Provide migration guide
  ├─ Offer migration support
  └─ Monitor old version usage

Months 4-6: Deprecation warnings
  ├─ Return deprecation headers
  ├─ Log usage for proactive outreach
  └─ Escalate communications

Month 6: Sunset (remove old version)
  └─ Return 410 Gone for old endpoints
```

### Deprecation Headers

**Standard headers:**
```http
GET /api/v1/users

200 OK
Deprecation: true
Sunset: Sat, 31 Dec 2025 23:59:59 GMT
Link: </api/v2/users>; rel="successor-version"
```

**Implementation:**
```javascript
// v1 routes middleware
app.use('/api/v1', (req, res, next) => {
  res.setHeader('Deprecation', 'true');
  res.setHeader('Sunset', 'Sat, 31 Dec 2025 23:59:59 GMT');
  res.setHeader('Link', '</api/v2' + req.path + '>; rel="successor-version"');
  next();
});
```

### After Sunset

**410 Gone Response:**
```http
GET /api/v1/users

410 Gone
Content-Type: application/problem+json

{
  "type": "https://api.example.com/errors/version-sunset",
  "title": "API Version Sunset",
  "status": 410,
  "detail": "API v1 was sunset on December 31, 2025",
  "successorVersion": "/api/v2/users"
}
```

### Communication Plan

**Announcement Channels:**
- API documentation (prominent banner)
- Email to registered API consumers
- Blog post / changelog
- Deprecation warnings in API responses
- Dashboard notifications (if applicable)

**Announcement Content:**
```markdown
# API v1 Deprecation Notice

API v1 will be deprecated on December 31, 2025.

## Timeline
- November 1, 2025: Deprecation announcement
- December 1-31, 2025: Migration period
- January 1, 2026: v1 sunset (no longer available)

## Migration Guide
See: https://docs.example.com/migration/v1-to-v2

## Support
Contact: api-support@example.com

## What's changing in v2
- [List breaking changes]
```

## Migration Patterns

### Gradual Migration

**Phase 1: Add v2 alongside v1**
```
/api/v1/users  (existing, will be deprecated)
/api/v2/users  (new, recommended)
```

**Phase 2: Encourage migration**
- Documentation emphasizes v2
- Deprecation warnings in v1 responses
- Migration guide available

**Phase 3: Monitor usage**
```javascript
// Track v1 usage
logger.info('v1_usage', {
  endpoint: req.path,
  userId: req.user.id,
  timestamp: new Date()
});
```

**Phase 4: Sunset v1**
- After migration period ends
- Return 410 Gone for v1 requests

### Adapter Pattern

Support both versions with shared business logic:

```javascript
// Shared business logic
async function getUserData(userId) {
  return await db.users.findById(userId);
}

// v1 adapter
function formatUserV1(user) {
  return {
    name: `${user.firstName} ${user.lastName}`,
    email: user.email
  };
}

// v2 adapter
function formatUserV2(user) {
  return {
    firstName: user.firstName,
    lastName: user.lastName,
    email: user.email
  };
}

// v1 route
router.get('/api/v1/users/:id', async (req, res) => {
  const user = await getUserData(req.params.id);
  res.json(formatUserV1(user));
});

// v2 route
router.get('/api/v2/users/:id', async (req, res) => {
  const user = await getUserData(req.params.id);
  res.json(formatUserV2(user));
});
```

### Migration Tools

**Provide tooling to assist migration:**

```javascript
// SDK with automatic version handling
const client = new APIClient({
  version: 'v2',
  fallback: 'v1'  // Fallback to v1 if v2 fails
});
```

**Migration helper:**
```javascript
// Convert v1 response to v2 format
function convertV1toV2(v1Response) {
  const [firstName, ...lastNameParts] = v1Response.name.split(' ');
  return {
    firstName,
    lastName: lastNameParts.join(' '),
    email: v1Response.email
  };
}
```

## Version Strategy Selection

### Decision Matrix

| Factor | URL Path | Header | Media Type | Query Param |
|--------|----------|--------|------------|-------------|
| **Visibility** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **Simplicity** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **RESTful** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Caching** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Testing** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **Best For** | Public APIs | Internal APIs | Content negotiation | Prototyping |

### Recommendations by Use Case

**Public Third-Party API:**
- Use: URL Path Versioning
- Why: Maximum visibility, ease of testing, clear documentation

**Internal Microservices:**
- Use: Header-Based or Semantic Versioning
- Why: Clean URLs, frequent minor updates

**Mobile App Backend:**
- Use: URL Path Versioning
- Why: Mobile apps update slowly, need clear version targeting

**Legacy System Migration:**
- Use: URL Path Versioning
- Why: Clear separation, gradual migration, both versions coexist

**GraphQL API:**
- Use: No versioning (schema evolution)
- Why: GraphQL supports field deprecation natively

## Best Practices Checklist

### Versioning Strategy
- [ ] Choose consistent versioning strategy (URL path recommended)
- [ ] Document versioning policy
- [ ] Communicate breaking changes clearly
- [ ] Maintain migration guides

### Breaking Changes
- [ ] Identify breaking vs non-breaking changes
- [ ] Increment major version for breaking changes
- [ ] Provide migration period (minimum 3-6 months)
- [ ] Support previous version during migration

### Deprecation
- [ ] Announce deprecation with clear timeline
- [ ] Add deprecation headers to responses
- [ ] Monitor old version usage
- [ ] Provide migration support
- [ ] Return 410 Gone after sunset

### Documentation
- [ ] Document current version
- [ ] Document deprecated versions
- [ ] Provide migration guides
- [ ] Show examples for each version
- [ ] Highlight breaking changes

### Testing
- [ ] Test all supported versions
- [ ] Test migration paths
- [ ] Monitor error rates per version
- [ ] Track adoption of new versions
