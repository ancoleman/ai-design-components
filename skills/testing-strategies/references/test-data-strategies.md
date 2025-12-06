# Test Data Management Strategies

## Table of Contents

1. [Overview](#overview)
2. [Fixtures (Static Data)](#fixtures-static-data)
3. [Factories (Generated Data)](#factories-generated-data)
4. [Property-Based Testing](#property-based-testing)
5. [Database Seeding](#database-seeding)
6. [Snapshot Testing](#snapshot-testing)
7. [Strategy Selection Guide](#strategy-selection-guide)

## Overview

Test data management is critical for reliable, maintainable tests. Choose the right strategy based on your testing needs.

### The Four Primary Strategies

| Strategy | Deterministic | Variety | Speed | Best For |
|----------|---------------|---------|-------|----------|
| **Fixtures** | ✅ High | ❌ Low | ⚡ Fast | Known scenarios, regression tests |
| **Factories** | ⚠️ Medium | ✅ High | ⚡ Fast | Flexible data, integration tests |
| **Property-Based** | ❌ Low | ✅ Very High | 🐌 Slow | Edge cases, complex algorithms |
| **Snapshots** | ✅ High | ❌ Low | ⚡ Fast | Output validation, UI components |

## Fixtures (Static Data)

### What Are Fixtures?

Predefined, static test data loaded before tests run.

**Characteristics**:
- Same data every test run
- Easy to understand and debug
- Version-controlled alongside tests
- Can become stale or outdated

### When to Use Fixtures

✅ **Use fixtures when**:
- Testing known scenarios (happy path, specific edge cases)
- Regression testing (ensure bug stays fixed)
- Need deterministic, reproducible tests
- Debugging failing tests (same data every run)

❌ **Avoid fixtures when**:
- Need variety (testing many scenarios)
- Data structure changes frequently
- Testing edge cases you haven't thought of

### TypeScript/JavaScript Example (Vitest)

**Inline fixtures**:
```typescript
import { describe, test, expect } from 'vitest'
import { calculateTotal } from './cart'

describe('calculateTotal', () => {
  test('calculates total for known items', () => {
    const items = [
      { id: 1, name: 'Widget', price: 10, quantity: 2 },
      { id: 2, name: 'Gadget', price: 5, quantity: 1 }
    ]

    expect(calculateTotal(items)).toBe(25)
  })
})
```

**External fixture files**:
```typescript
// fixtures/products.ts
export const sampleProducts = [
  { id: 1, name: 'Widget', price: 10, stock: 100 },
  { id: 2, name: 'Gadget', price: 5, stock: 50 }
]

// products.test.ts
import { sampleProducts } from './fixtures/products'

test('filters products by price', () => {
  const filtered = filterByPrice(sampleProducts, { max: 7 })
  expect(filtered).toHaveLength(1)
  expect(filtered[0].name).toBe('Gadget')
})
```

**JSON fixtures**:
```typescript
// fixtures/api-response.json
{
  "users": [
    { "id": 1, "name": "Alice", "email": "alice@example.com" },
    { "id": 2, "name": "Bob", "email": "bob@example.com" }
  ]
}

// api.test.ts
import apiResponse from './fixtures/api-response.json'

test('parses API response', () => {
  const users = parseUsers(apiResponse)
  expect(users).toHaveLength(2)
})
```

### Python Example (pytest)

**pytest fixtures** (function-scoped):
```python
import pytest

@pytest.fixture
def sample_user():
    """Provide a sample user for testing"""
    return {
        'id': 1,
        'name': 'Alice',
        'email': 'alice@example.com',
        'age': 30
    }

def test_user_validation(sample_user):
    assert validate_user(sample_user) is True

def test_user_serialization(sample_user):
    serialized = serialize_user(sample_user)
    assert serialized['name'] == 'Alice'
```

**Fixture scopes**:
```python
@pytest.fixture(scope='session')  # Once per test session
def database_connection():
    conn = create_connection()
    yield conn
    conn.close()

@pytest.fixture(scope='module')  # Once per test module
def sample_data():
    return load_sample_data()

@pytest.fixture(scope='function')  # Default: once per test function
def temp_file():
    file = create_temp_file()
    yield file
    file.delete()
```

**External fixture files**:
```python
# conftest.py (shared across tests)
import pytest
import json

@pytest.fixture
def api_response():
    with open('fixtures/api-response.json') as f:
        return json.load(f)

# test_api.py
def test_parse_response(api_response):
    users = parse_users(api_response)
    assert len(users) == 2
```

### Go Example

```go
package products_test

import (
    "testing"
    "github.com/stretchr/testify/assert"
)

// Fixture: Sample products
var sampleProducts = []Product{
    {ID: 1, Name: "Widget", Price: 10.0, Stock: 100},
    {ID: 2, Name: "Gadget", Price: 5.0, Stock: 50},
}

func TestFilterByPrice(t *testing.T) {
    filtered := FilterByPrice(sampleProducts, PriceFilter{Max: 7.0})
    assert.Len(t, filtered, 1)
    assert.Equal(t, "Gadget", filtered[0].Name)
}
```

### Rust Example

```rust
#[cfg(test)]
mod tests {
    use super::*;

    // Fixture: Sample products
    fn sample_products() -> Vec<Product> {
        vec![
            Product { id: 1, name: "Widget".to_string(), price: 10.0, stock: 100 },
            Product { id: 2, name: "Gadget".to_string(), price: 5.0, stock: 50 },
        ]
    }

    #[test]
    fn test_filter_by_price() {
        let products = sample_products();
        let filtered = filter_by_price(&products, PriceFilter { max: Some(7.0) });
        assert_eq!(filtered.len(), 1);
        assert_eq!(filtered[0].name, "Gadget");
    }
}
```

## Factories (Generated Data)

### What Are Factories?

Functions that generate test data with sensible defaults, allowing customization.

**Characteristics**:
- Generate fresh data for each test
- Customizable (override defaults)
- More flexible than fixtures
- Slightly less deterministic

### When to Use Factories

✅ **Use factories when**:
- Need variety in test data
- Testing multiple scenarios with similar structure
- Want to avoid data coupling between tests
- Need realistic but flexible data

❌ **Avoid factories when**:
- Need exact, reproducible data
- Debugging specific scenarios
- Simple tests with few data variations

### TypeScript/JavaScript Example

**Simple factory**:
```typescript
// factories/user.ts
export function createUser(overrides = {}) {
  return {
    id: Math.random().toString(),
    name: 'Test User',
    email: 'test@example.com',
    createdAt: new Date(),
    ...overrides
  }
}

// user.test.ts
test('creates user with valid email', () => {
  const user = createUser({ email: 'alice@example.com' })
  expect(validateUser(user)).toBe(true)
})

test('rejects user with invalid email', () => {
  const user = createUser({ email: 'invalid' })
  expect(validateUser(user)).toBe(false)
})
```

**Factory with builder pattern**:
```typescript
class UserFactory {
  private data = {
    id: '',
    name: 'Test User',
    email: 'test@example.com',
    role: 'user' as const
  }

  withId(id: string) {
    this.data.id = id
    return this
  }

  withEmail(email: string) {
    this.data.email = email
    return this
  }

  asAdmin() {
    this.data.role = 'admin'
    return this
  }

  build() {
    return { ...this.data, id: this.data.id || Math.random().toString() }
  }
}

// Usage
test('admin user has elevated permissions', () => {
  const admin = new UserFactory().asAdmin().build()
  expect(hasPermission(admin, 'delete-users')).toBe(true)
})
```

### Python Example

**Factory function**:
```python
# factories.py
def create_user(**kwargs):
    """Factory for creating test users"""
    defaults = {
        'id': uuid.uuid4(),
        'name': 'Test User',
        'email': 'test@example.com',
        'created_at': datetime.now()
    }
    return {**defaults, **kwargs}

# test_users.py
def test_user_validation():
    user = create_user(email='alice@example.com')
    assert validate_user(user) is True

def test_invalid_email():
    user = create_user(email='invalid')
    assert validate_user(user) is False
```

**Factory Boy (advanced library)**:
```python
import factory
from models import User

class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    name = factory.Faker('name')
    email = factory.Faker('email')
    created_at = factory.Faker('date_time_this_year')

# Usage
def test_user_creation():
    user = UserFactory.create()
    assert user.email is not None

def test_admin_user():
    admin = UserFactory.create(role='admin')
    assert admin.role == 'admin'

def test_multiple_users():
    users = UserFactory.create_batch(10)
    assert len(users) == 10
```

### Go Example

```go
// Factory function
func NewTestUser(opts ...func(*User)) *User {
    user := &User{
        ID:    uuid.New().String(),
        Name:  "Test User",
        Email: "test@example.com",
        Role:  "user",
    }

    for _, opt := range opts {
        opt(user)
    }

    return user
}

// Option functions
func WithEmail(email string) func(*User) {
    return func(u *User) {
        u.Email = email
    }
}

func AsAdmin() func(*User) {
    return func(u *User) {
        u.Role = "admin"
    }
}

// Usage
func TestAdminPermissions(t *testing.T) {
    admin := NewTestUser(AsAdmin(), WithEmail("admin@example.com"))
    assert.Equal(t, "admin", admin.Role)
}
```

## Property-Based Testing

### What Is Property-Based Testing?

Generate hundreds/thousands of random inputs to find edge cases you didn't think of.

**Characteristics**:
- Discovers unexpected edge cases
- Tests invariants (properties that should always hold)
- Slower than fixture/factory tests
- Failures can be hard to debug (but shrinking helps)

### When to Use Property-Based Testing

✅ **Use property-based testing when**:
- Testing complex algorithms (sorting, parsing, compression)
- Testing mathematical properties (commutativity, associativity)
- Validating parsers/serializers (round-trip properties)
- Finding edge cases in validation logic

❌ **Avoid property-based testing when**:
- Simple, straightforward functions
- Performance-critical test suites (property tests are slow)
- Need deterministic test data

### TypeScript/JavaScript Example (fast-check)

**Basic property test**:
```typescript
import fc from 'fast-check'

test('reversing twice returns original', () => {
  fc.assert(
    fc.property(fc.array(fc.integer()), (arr) => {
      expect(reverse(reverse(arr))).toEqual(arr)
    })
  )
})

test('sorting is idempotent', () => {
  fc.assert(
    fc.property(fc.array(fc.integer()), (arr) => {
      const sorted = sort(arr)
      expect(sort(sorted)).toEqual(sorted)
    })
  )
})
```

**Round-trip testing**:
```typescript
test('JSON serialization round-trip', () => {
  fc.assert(
    fc.property(
      fc.record({
        id: fc.integer(),
        name: fc.string(),
        active: fc.boolean()
      }),
      (obj) => {
        const serialized = JSON.stringify(obj)
        const deserialized = JSON.parse(serialized)
        expect(deserialized).toEqual(obj)
      }
    )
  )
})
```

### Python Example (hypothesis)

**Basic property test**:
```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_reverse_reverse_is_identity(lst):
    assert reverse(reverse(lst)) == lst

@given(st.lists(st.integers()))
def test_sorting_is_idempotent(lst):
    sorted_list = sorted(lst)
    assert sorted(sorted_list) == sorted_list
```

**Complex strategies**:
```python
from hypothesis import given, strategies as st

# Generate users with constraints
user_strategy = st.builds(
    dict,
    id=st.integers(min_value=1),
    name=st.text(min_size=1, max_size=100),
    email=st.emails(),
    age=st.integers(min_value=18, max_value=120)
)

@given(user_strategy)
def test_user_validation(user):
    assert validate_user(user) is True
    assert user['age'] >= 18
```

**Shrinking example**:
```python
# hypothesis automatically shrinks failing cases to minimal example
@given(st.lists(st.integers()))
def test_no_duplicates_after_dedup(lst):
    deduped = remove_duplicates(lst)
    assert len(deduped) == len(set(deduped))

# If this fails on [1, 2, 2, 3], hypothesis will shrink to [0, 0]
```

### Rust Example (proptest)

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn test_reverse_twice(ref v in prop::collection::vec(any::<i32>(), 0..100)) {
        let reversed_twice: Vec<_> = v.iter().rev().rev().copied().collect();
        assert_eq!(v, &reversed_twice);
    }

    #[test]
    fn test_add_is_commutative(a in any::<i32>(), b in any::<i32>()) {
        prop_assume!(a.checked_add(b).is_some());
        assert_eq!(a + b, b + a);
    }
}
```

## Database Seeding

### When to Use Database Seeding

For integration tests that require specific database state.

**Characteristics**:
- Sets up known database state before tests
- Cleans up after tests (transaction rollback or truncate)
- Realistic data for integration testing
- Slower than in-memory tests

### TypeScript/JavaScript Example (Vitest + Postgres)

```typescript
import { beforeEach, afterEach, test, expect } from 'vitest'
import { db } from './database'

beforeEach(async () => {
  // Seed database
  await db.query('TRUNCATE users, products RESTART IDENTITY CASCADE')
  await db.query(`
    INSERT INTO users (name, email) VALUES
    ('Alice', 'alice@example.com'),
    ('Bob', 'bob@example.com')
  `)
})

afterEach(async () => {
  // Cleanup
  await db.query('TRUNCATE users, products RESTART IDENTITY CASCADE')
})

test('fetches all users', async () => {
  const users = await fetchUsers()
  expect(users).toHaveLength(2)
})
```

### Python Example (pytest + SQLAlchemy)

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User

@pytest.fixture(scope='function')
def db_session():
    """Provide a clean database session for each test"""
    engine = create_engine('postgresql://localhost/test_db')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Seed data
    session.add(User(name='Alice', email='alice@example.com'))
    session.add(User(name='Bob', email='bob@example.com'))
    session.commit()

    yield session

    session.close()
    Base.metadata.drop_all(engine)

def test_fetch_users(db_session):
    users = db_session.query(User).all()
    assert len(users) == 2
```

## Snapshot Testing

### What Is Snapshot Testing?

Capture output and compare against saved snapshots to detect unintended changes.

**When to Use**:
- UI component rendering
- API response structures
- Generated code output
- Configuration files

**Caution**: Easy to over-use. Update snapshots mindfully.

### TypeScript/JavaScript Example (Vitest)

```typescript
import { test, expect } from 'vitest'
import { render } from '@testing-library/react'
import { UserCard } from './UserCard'

test('renders user card correctly', () => {
  const user = { name: 'Alice', email: 'alice@example.com' }
  const { container } = render(<UserCard user={user} />)
  expect(container.firstChild).toMatchSnapshot()
})

test('generates correct config', () => {
  const config = generateConfig({ apiUrl: 'https://api.example.com' })
  expect(config).toMatchSnapshot()
})
```

### Python Example (pytest-snapshot)

```python
def test_api_response_structure(snapshot):
    response = fetch_user_data(user_id=1)
    snapshot.assert_match(response, 'user_response.json')

def test_generated_html(snapshot):
    html = generate_email_template(user='Alice', subject='Welcome')
    snapshot.assert_match(html, 'welcome_email.html')
```

## Strategy Selection Guide

### Decision Matrix

| Scenario | Recommended Strategy | Rationale |
|----------|---------------------|-----------|
| Known happy path | Fixtures | Deterministic, easy to debug |
| Multiple similar scenarios | Factories | Flexible, avoid duplication |
| Complex algorithm edge cases | Property-Based | Discovers unexpected cases |
| Integration test setup | Database Seeding + Factories | Realistic data, flexible |
| UI component rendering | Snapshot | Detect unintended changes |
| Round-trip validation | Property-Based | Tests invariants |
| Regression test | Fixtures | Ensure specific bug stays fixed |
| Performance testing | Factories | Generate large datasets |

### Combining Strategies

**Example: User authentication testing**

```typescript
// Unit test: Use fixtures for known scenarios
test('validates correct password', () => {
  const user = { username: 'alice', passwordHash: 'hash123' }
  expect(validatePassword(user, 'password')).toBe(true)
})

// Unit test: Use property-based for edge cases
fc.assert(
  fc.property(fc.string(), fc.string(), (username, password) => {
    const user = createUser({ username, password })
    // Property: Never validate empty password
    if (password === '') {
      expect(validatePassword(user, password)).toBe(false)
    }
  })
)

// Integration test: Use factories + database seeding
test('login endpoint returns token', async () => {
  const user = await UserFactory.create({ password: 'password123' })
  const response = await request(app)
    .post('/login')
    .send({ username: user.username, password: 'password123' })
  expect(response.body.token).toBeDefined()
})

// E2E test: Use fixtures for reproducible scenarios
test('user can login and access dashboard', async ({ page }) => {
  // Seed known user
  await seedUser({ username: 'alice', password: 'password123' })

  await page.goto('/login')
  await page.fill('[name="username"]', 'alice')
  await page.fill('[name="password"]', 'password123')
  await page.click('[type="submit"]')

  await expect(page.locator('h1')).toContainText('Dashboard')
})
```

## Summary

**Key Takeaways**:

1. **Fixtures**: Best for known scenarios, regression tests, debugging
2. **Factories**: Best for flexible data, integration tests, avoiding duplication
3. **Property-Based**: Best for complex algorithms, finding edge cases, validating invariants
4. **Database Seeding**: Best for integration tests requiring realistic data
5. **Snapshots**: Best for UI components, configuration files, detecting unintended changes

**Recommendations**:
- Start with fixtures for simple tests
- Use factories as tests grow and need flexibility
- Add property-based tests for critical logic
- Combine strategies for comprehensive coverage
- Update snapshots mindfully (not automatically)
