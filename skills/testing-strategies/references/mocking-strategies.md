# Mocking Strategies

## Table of Contents

1. [Overview](#overview)
2. [When to Mock vs. Use Real Dependencies](#when-to-mock-vs-use-real-dependencies)
3. [Mocking External APIs](#mocking-external-apis)
4. [Mocking Databases](#mocking-databases)
5. [Mocking Time and Randomness](#mocking-time-and-randomness)
6. [Test Doubles Taxonomy](#test-doubles-taxonomy)
7. [Anti-Patterns](#anti-patterns)

## Overview

Mocking is the practice of replacing real dependencies with controlled substitutes during testing. Effective mocking enables fast, isolated tests while maintaining confidence in system behavior.

### The Mocking Decision Matrix

| Dependency | Unit Test | Integration Test | E2E Test |
|------------|-----------|------------------|----------|
| **Database** | Mock (in-memory) | Real (test DB, Docker) | Real (staging DB) |
| **External API** | Mock (MSW, nock) | Mock (MSW, VCR) | Real (or staging) |
| **Filesystem** | Mock (in-memory FS) | Real (temp directory) | Real |
| **Time/Date** | Mock (freezeTime) | Mock (if deterministic) | Real (usually) |
| **Environment Variables** | Mock (setEnv) | Mock (test config) | Real (test env) |
| **Internal Services** | Mock (stub) | Real (or container) | Real |
| **Random Number Generator** | Mock (seeded) | Mock (deterministic) | Real |
| **External Queue** | Mock (in-memory) | Real (test queue) | Real |

## When to Mock vs. Use Real Dependencies

### Use Mock When

✅ **External API calls**:
- Third-party services (payment, shipping, email)
- Avoid rate limits and costs
- Ensure deterministic responses
- Test error scenarios (API down, timeout)

✅ **Slow operations**:
- File I/O (unless testing file handling specifically)
- Network requests
- Heavy computations (not core to test)

✅ **Non-deterministic behavior**:
- Current time (Date.now(), datetime.now())
- Random number generation
- UUIDs and unique IDs

✅ **External dependencies outside your control**:
- Third-party libraries with side effects
- System-level operations (process.exit, os.shutdown)

### Use Real Dependency When

✅ **Database operations** (integration tests):
- Use ephemeral database (Docker, in-memory SQLite)
- Test actual SQL queries
- Validate transaction behavior
- Ensure data integrity

✅ **Internal services** (integration tests):
- Test component interactions
- Validate interface contracts
- Ensure data flow correctness

✅ **File operations** (integration tests):
- Use temporary directories
- Test file parsing, generation
- Validate file handling edge cases

✅ **Core business logic**:
- Never mock the system under test
- Never mock what you're trying to validate

## Mocking External APIs

### TypeScript/JavaScript: Mock Service Worker (MSW)

**Why MSW?**
- Intercepts requests at network level (realistic)
- Same handlers for tests and development
- Framework-agnostic (works with any test library)
- TypeScript support

**Basic Setup**:
```typescript
// mocks/handlers.ts
import { http, HttpResponse } from 'msw'

export const handlers = [
  http.get('/api/users/:id', ({ params }) => {
    return HttpResponse.json({
      id: params.id,
      name: 'Test User',
      email: 'test@example.com'
    })
  }),

  http.post('/api/users', async ({ request }) => {
    const body = await request.json()
    return HttpResponse.json(
      { id: '123', ...body },
      { status: 201 }
    )
  })
]

// mocks/server.ts
import { setupServer } from 'msw/node'
import { handlers } from './handlers'

export const server = setupServer(...handlers)

// vitest.setup.ts
import { beforeAll, afterEach, afterAll } from 'vitest'
import { server } from './mocks/server'

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

**Usage in Tests**:
```typescript
import { test, expect } from 'vitest'
import { server } from './mocks/server'
import { http, HttpResponse } from 'msw'
import { fetchUser, createUser } from './api'

test('fetches user data', async () => {
  const user = await fetchUser('123')
  expect(user.name).toBe('Test User')
})

test('handles API errors', async () => {
  server.use(
    http.get('/api/users/:id', () => {
      return HttpResponse.json(
        { error: 'User not found' },
        { status: 404 }
      )
    })
  )

  await expect(fetchUser('999')).rejects.toThrow('User not found')
})

test('creates user', async () => {
  const newUser = await createUser({ name: 'Alice', email: 'alice@example.com' })
  expect(newUser.id).toBe('123')
  expect(newUser.name).toBe('Alice')
})
```

**Advanced: Request Matching and Validation**:
```typescript
test('sends correct request body', async () => {
  let capturedRequest: any

  server.use(
    http.post('/api/users', async ({ request }) => {
      capturedRequest = await request.json()
      return HttpResponse.json({ id: '123', ...capturedRequest })
    })
  )

  await createUser({ name: 'Bob', email: 'bob@example.com' })

  expect(capturedRequest).toEqual({
    name: 'Bob',
    email: 'bob@example.com'
  })
})
```

### Python: pytest-httpserver

**Setup**:
```python
import pytest
from pytest_httpserver import HTTPServer

@pytest.fixture
def mock_api(httpserver: HTTPServer):
    httpserver.expect_request('/api/users/123').respond_with_json({
        'id': '123',
        'name': 'Test User',
        'email': 'test@example.com'
    })
    return httpserver

def test_fetch_user(mock_api):
    response = fetch_user('123', base_url=mock_api.url_for(''))
    assert response['name'] == 'Test User'
```

**Error Simulation**:
```python
def test_api_error_handling(httpserver):
    httpserver.expect_request('/api/users/999').respond_with_json(
        {'error': 'User not found'},
        status=404
    )

    with pytest.raises(UserNotFoundError):
        fetch_user('999', base_url=httpserver.url_for(''))
```

### Python: VCR.py (Record/Replay)

**Record real API responses, replay in tests**:
```python
import vcr

@vcr.use_cassette('fixtures/vcr_cassettes/user_123.yaml')
def test_fetch_user():
    # First run: Makes real API call, records response
    # Subsequent runs: Replays recorded response
    user = fetch_user('123')
    assert user['name'] == 'Test User'
```

**Benefits**:
- Real API responses (realistic data)
- No mocking code needed
- Offline testing (no network required)

**Drawbacks**:
- Cassettes can become stale
- Doesn't test error scenarios easily
- Large responses bloat repository

### Go: httptest

**Standard library mocking**:
```go
func TestFetchUser(t *testing.T) {
    server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
        w.Write([]byte(`{"id": "123", "name": "Test User"}`))
    }))
    defer server.Close()

    user, err := fetchUser("123", server.URL)
    assert.NoError(t, err)
    assert.Equal(t, "Test User", user.Name)
}
```

### Rust: mockito

```rust
use mockito::{mock, server_url};

#[test]
fn test_fetch_user() {
    let _m = mock("GET", "/api/users/123")
        .with_status(200)
        .with_header("content-type", "application/json")
        .with_body(r#"{"id": "123", "name": "Test User"}"#)
        .create();

    let user = fetch_user("123", &server_url()).unwrap();
    assert_eq!(user.name, "Test User");
}
```

## Mocking Databases

### In-Memory SQLite (Fast Unit Tests)

**TypeScript/JavaScript (better-sqlite3)**:
```typescript
import Database from 'better-sqlite3'
import { beforeEach, test, expect } from 'vitest'

let db: Database.Database

beforeEach(() => {
  db = new Database(':memory:')
  db.exec(`
    CREATE TABLE users (
      id INTEGER PRIMARY KEY,
      name TEXT,
      email TEXT
    )
  `)
})

test('inserts user', () => {
  const stmt = db.prepare('INSERT INTO users (name, email) VALUES (?, ?)')
  const result = stmt.run('Alice', 'alice@example.com')
  expect(result.changes).toBe(1)
})
```

**Python (SQLite)**:
```python
import sqlite3
import pytest

@pytest.fixture
def db():
    conn = sqlite3.connect(':memory:')
    conn.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT
        )
    ''')
    yield conn
    conn.close()

def test_insert_user(db):
    cursor = db.execute('INSERT INTO users (name, email) VALUES (?, ?)',
                        ('Alice', 'alice@example.com'))
    assert cursor.rowcount == 1
```

### Docker Test Containers (Real Database Integration)

**TypeScript/JavaScript (testcontainers)**:
```typescript
import { PostgreSqlContainer } from '@testcontainers/postgresql'
import { beforeAll, afterAll, test } from 'vitest'
import pg from 'pg'

let container: StartedPostgreSqlContainer
let client: pg.Client

beforeAll(async () => {
  container = await new PostgreSqlContainer().start()
  client = new pg.Client({ connectionString: container.getConnectionUri() })
  await client.connect()
  await client.query(`
    CREATE TABLE users (
      id SERIAL PRIMARY KEY,
      name VARCHAR(255),
      email VARCHAR(255)
    )
  `)
}, 30000)

afterAll(async () => {
  await client.end()
  await container.stop()
})

test('creates user in real postgres', async () => {
  const result = await client.query(
    'INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id',
    ['Alice', 'alice@example.com']
  )
  expect(result.rows[0].id).toBeDefined()
})
```

**Python (testcontainers-python)**:
```python
from testcontainers.postgres import PostgresContainer
import psycopg2
import pytest

@pytest.fixture(scope='module')
def postgres():
    with PostgresContainer("postgres:16") as container:
        conn = psycopg2.connect(container.get_connection_url())
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                email VARCHAR(255)
            )
        ''')
        conn.commit()
        yield conn
        conn.close()

def test_create_user(postgres):
    cursor = postgres.cursor()
    cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id',
                   ('Alice', 'alice@example.com'))
    user_id = cursor.fetchone()[0]
    assert user_id is not None
```

### Database Mocking Libraries

**TypeScript: mock-knex**:
```typescript
import knex from 'knex'
import mockKnex from 'mock-knex'

const db = knex({ client: 'pg' })
mockKnex.mock(db)

test('mocks database query', async () => {
  const tracker = mockKnex.getTracker()
  tracker.install()

  tracker.on('query', (query) => {
    query.response([{ id: 1, name: 'Alice' }])
  })

  const users = await db('users').select()
  expect(users[0].name).toBe('Alice')

  tracker.uninstall()
})
```

## Mocking Time and Randomness

### Mocking Time (Deterministic Tests)

**TypeScript/JavaScript: Vitest useFakeTimers**:
```typescript
import { test, expect, vi, beforeEach, afterEach } from 'vitest'

beforeEach(() => {
  vi.useFakeTimers()
})

afterEach(() => {
  vi.useRealTimers()
})

test('schedules task for future', () => {
  const callback = vi.fn()

  setTimeout(callback, 1000)

  // Time hasn't passed yet
  expect(callback).not.toHaveBeenCalled()

  // Fast-forward 1 second
  vi.advanceTimersByTime(1000)

  expect(callback).toHaveBeenCalledOnce()
})

test('freezes time at specific date', () => {
  const mockDate = new Date('2025-01-01T00:00:00Z')
  vi.setSystemTime(mockDate)

  expect(new Date()).toEqual(mockDate)

  // Time doesn't advance
  setTimeout(() => {}, 5000)
  vi.advanceTimersByTime(5000)

  expect(new Date()).toEqual(mockDate)
})
```

**Python: freezegun**:
```python
from freezegun import freeze_time
from datetime import datetime

@freeze_time("2025-01-01 00:00:00")
def test_time_frozen():
    assert datetime.now().year == 2025
    assert datetime.now().month == 1

@freeze_time("2025-01-01")
def test_date_calculation():
    # Time is frozen, calculations are deterministic
    expiry = calculate_expiry_date(days=30)
    assert expiry.day == 31
```

**Python: unittest.mock (patch time)**:
```python
from unittest.mock import patch
from datetime import datetime

@patch('mymodule.datetime')
def test_current_time(mock_datetime):
    mock_datetime.now.return_value = datetime(2025, 1, 1, 12, 0, 0)

    result = get_current_timestamp()
    assert result == '2025-01-01 12:00:00'
```

### Mocking Random Number Generation

**TypeScript/JavaScript**:
```typescript
import { test, expect, vi } from 'vitest'

test('generates predictable random numbers', () => {
  const mockRandom = vi.spyOn(Math, 'random')
  mockRandom.mockReturnValueOnce(0.5)

  const result = generateId() // Uses Math.random()
  expect(result).toBe('expected-id-for-0.5')

  mockRandom.mockRestore()
})
```

**Python**:
```python
from unittest.mock import patch

@patch('random.randint')
def test_random_generation(mock_randint):
    mock_randint.return_value = 42

    result = generate_random_id()
    assert result == 'id-42'
```

## Test Doubles Taxonomy

### Types of Test Doubles

**Dummy**: Passed but never used
```typescript
test('creates user without password validation', () => {
  const dummyValidator = null // Never called
  const user = createUser({ name: 'Alice' }, dummyValidator)
  expect(user.name).toBe('Alice')
})
```

**Stub**: Returns predetermined values
```typescript
const stubDatabase = {
  findUser: () => ({ id: '123', name: 'Alice' })
}

test('fetches user from stubbed database', () => {
  const user = userService.getUser('123', stubDatabase)
  expect(user.name).toBe('Alice')
})
```

**Spy**: Records calls and arguments
```typescript
test('calls email service with correct arguments', () => {
  const emailSpy = vi.fn()

  sendWelcomeEmail('alice@example.com', emailSpy)

  expect(emailSpy).toHaveBeenCalledWith({
    to: 'alice@example.com',
    subject: 'Welcome',
    body: expect.any(String)
  })
})
```

**Mock**: Stub + Spy (preset responses, verify calls)
```typescript
test('authenticates user and logs event', () => {
  const authMock = vi.fn().mockResolvedValue({ authenticated: true })
  const logMock = vi.fn()

  await loginUser('alice', 'password', authMock, logMock)

  expect(authMock).toHaveBeenCalledWith('alice', 'password')
  expect(logMock).toHaveBeenCalledWith('login', { user: 'alice' })
})
```

**Fake**: Working implementation (simplified)
```typescript
class FakeDatabase {
  private data = new Map()

  async save(id: string, value: any) {
    this.data.set(id, value)
  }

  async find(id: string) {
    return this.data.get(id)
  }
}

test('saves and retrieves from fake database', async () => {
  const db = new FakeDatabase()
  await db.save('123', { name: 'Alice' })
  const user = await db.find('123')
  expect(user.name).toBe('Alice')
})
```

## Anti-Patterns

### Over-Mocking (Testing Implementation, Not Behavior)

**❌ Bad: Mocking everything**:
```typescript
test('bad: over-mocked', () => {
  const mockAdd = vi.fn((a, b) => a + b)
  const mockMultiply = vi.fn((a, b) => a * b)

  const result = calculate(5, 3, mockAdd, mockMultiply)

  expect(mockAdd).toHaveBeenCalledWith(5, 3)
  expect(mockMultiply).toHaveBeenCalled()
  // Not testing actual behavior, just mocks!
})
```

**✅ Good: Test behavior, mock external dependencies only**:
```typescript
test('good: test behavior', () => {
  const result = calculate(5, 3)
  expect(result).toBe(23) // Test actual result
})
```

### Mocking What You're Testing

**❌ Bad: Mocking the system under test**:
```typescript
test('bad: mocks the function being tested', () => {
  const mockCalculate = vi.fn(() => 42)
  expect(mockCalculate()).toBe(42) // Meaningless!
})
```

**✅ Good: Mock dependencies, test real implementation**:
```typescript
test('good: test real function with mocked dependencies', () => {
  const mockFetch = vi.fn().mockResolvedValue({ data: [1, 2, 3] })
  const result = await processData(mockFetch)
  expect(result.length).toBe(3)
})
```

### Brittle Mocks (Coupled to Implementation)

**❌ Bad: Mocks too specific to implementation**:
```typescript
test('bad: brittle mock', () => {
  const mock = vi.fn()
  processUser(mock)
  expect(mock).toHaveBeenCalledWith('step1')
  expect(mock).toHaveBeenCalledWith('step2')
  expect(mock).toHaveBeenCalledWith('step3')
  // Breaks if internal steps change
})
```

**✅ Good: Test outcomes, not internal steps**:
```typescript
test('good: test outcomes', () => {
  const result = processUser()
  expect(result.status).toBe('completed')
  expect(result.errors).toHaveLength(0)
})
```

### Mock Leakage (Not Resetting Mocks)

**❌ Bad: Mocks persist across tests**:
```typescript
const mockFetch = vi.fn()

test('test 1', () => {
  mockFetch.mockResolvedValue({ data: 'test1' })
  // ...
})

test('test 2', () => {
  // mockFetch still has behavior from test 1! 🐛
})
```

**✅ Good: Reset mocks between tests**:
```typescript
import { beforeEach, afterEach } from 'vitest'

const mockFetch = vi.fn()

beforeEach(() => {
  mockFetch.mockReset()
})

// Or use Vitest's global resetMocks
```

## Summary

**Key Takeaways**:

1. **Mock external dependencies**: APIs, time, randomness
2. **Use real dependencies for integration tests**: Databases (ephemeral), internal services
3. **Never mock the system under test**: Test real behavior, not mocks
4. **Choose the right test double**: Dummy, stub, spy, mock, fake
5. **Avoid over-mocking**: Only mock what's necessary
6. **Reset mocks between tests**: Prevent test pollution

**Tools by Language**:
- **TypeScript/JavaScript**: MSW (APIs), Vitest mocks/spies, useFakeTimers
- **Python**: pytest-httpserver, VCR.py, freezegun, unittest.mock
- **Go**: httptest (stdlib), testify/mock
- **Rust**: mockito, mockall

**Next Steps**:
- Identify slow/flaky tests caused by external dependencies
- Replace with appropriate mocks (MSW for APIs, Docker for databases)
- Verify mocks are reset between tests
- Refactor over-mocked tests to test behavior, not implementation
