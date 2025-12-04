# Testing Strategies Skill - Master Plan

**Skill Name:** `testing-strategies`
**Skill Level:** Mid Level (5,000-8,000 tokens)
**Status:** Planning Phase (init.md complete, SKILL.md to be created)
**Last Updated:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [Testing Pyramid and Strategy Framework](#testing-pyramid-and-strategy-framework)
5. [Component Taxonomy](#component-taxonomy)
6. [Decision Frameworks](#decision-frameworks)
7. [Multi-Language Implementations](#multi-language-implementations)
8. [Library Recommendations](#library-recommendations)
9. [Skill Structure Design](#skill-structure-design)
10. [Integration Points](#integration-points)
11. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why This Skill Matters

Testing is the foundation of reliable software development. In 2025, with the rise of AI-assisted development, microservices architectures, and continuous delivery practices, comprehensive testing strategies are more critical than ever.

**Market Drivers:**
- **Shift-Left Testing:** Organizations moving testing earlier in the development cycle
- **AI-Powered Test Optimization:** Using AI to improve testing efficiency (2025 trend)
- **Continuous Testing:** Integration testing into CI/CD pipelines is standard practice
- **Microservices Complexity:** Contract testing and integration testing crucial for service architectures
- **Speed vs. Quality:** Balance between fast feedback (unit tests) and comprehensive coverage (E2E tests)

**Strategic Value:**
1. **Universal Need:** Every application needs testing at multiple levels
2. **Cross-Cutting Concern:** Integrates with all other skills (forms, APIs, dashboards, etc.)
3. **Quality Enabler:** Foundation for reliable, maintainable software
4. **CI/CD Critical:** Essential for automated deployment pipelines

### How This Differs from Existing Solutions

**Existing Testing Documentation:**
- **Framework-Specific:** Most docs focus on single tools (Jest docs, Pytest docs, Playwright docs)
- **Single-Language:** Typically JavaScript OR Python OR Rust, not unified
- **Tactical Focus:** "How to write a test" vs. "When to use what test type"

**Our Approach:**
- **Strategic Decision Framework:** When to use unit vs. integration vs. E2E vs. contract testing
- **Multi-Language Unified:** Consistent patterns across TypeScript, Python, Go, Rust
- **Testing Pyramid Guidance:** Practical advice on balancing test types
- **Integration-Focused:** How testing fits into full-stack development workflow
- **Modern Best Practices:** 2025 patterns including AI-driven optimization, shift-left testing

### Target Audience

**Primary Users:**
- Full-stack developers building production applications
- Backend developers creating APIs and microservices
- Frontend developers testing UI components and user flows
- DevOps engineers setting up CI/CD pipelines

**Skill Level Assumptions:**
- Understands basic programming concepts
- Familiar with at least one testing framework
- Knows difference between unit/integration/E2E testing (but needs guidance on when to use each)

---

## Skill Purpose and Scope

### What This Skill Teaches

**Core Competencies:**

1. **Testing Strategy Selection**
   - When to use unit, integration, E2E, contract testing
   - How to balance test pyramid for optimal coverage and speed
   - Trade-offs between different testing approaches

2. **Multi-Level Testing Patterns**
   - Unit testing: Pure functions, components, utilities
   - Integration testing: API endpoints, database interactions, service communication
   - E2E testing: User workflows, critical paths, cross-browser scenarios
   - Contract testing: Microservice interfaces, API contracts

3. **Test Data Management**
   - Fixtures and factories for consistent test data
   - Mocking strategies for external dependencies
   - Database seeding and cleanup patterns

4. **Coverage and Quality Metrics**
   - Meaningful coverage targets (not just 100%)
   - Mutation testing for test quality validation
   - Performance benchmarking in tests

5. **Property-Based Testing**
   - Generative testing for edge cases
   - Hypothesis/Proptest patterns for robust validation

### What This Skill Does NOT Cover

**Out of Scope:**
- **Performance/Load Testing:** Covered by `observability` skill
- **Security Testing:** Covered by `auth-security` skill
- **Deployment Testing:** Covered by `deploying-applications` and `building-ci-pipelines` skills
- **Visual Regression Testing:** May be added later as advanced topic
- **Chaos Engineering:** Advanced reliability topic, separate skill

### Success Criteria

**A user successfully uses this skill when they can:**
1. Select appropriate test types for a given feature
2. Write effective unit tests with proper isolation
3. Create integration tests that validate component interactions
4. Implement E2E tests for critical user journeys
5. Set up contract tests for microservice interfaces
6. Achieve meaningful test coverage without over-testing
7. Integrate tests into CI/CD pipelines

---

## Research Findings

### Research Date: December 3, 2025

**Research Tools Used:**
- Google Search Grounding (Vertex AI)
- Context7 for library documentation
- Official documentation for Jest, Vitest, Playwright, pytest

### Key Trends for 2025

**1. AI-Powered Test Optimization**
- AI tools generating test cases from specifications
- Intelligent test selection (run only affected tests)
- Automated test data generation

**2. Shift-Left Testing**
- Testing earlier in development cycle
- Developer-owned testing (not separate QA team)
- Faster feedback loops

**3. Continuous Testing**
- Integration with CI/CD as standard practice
- Automated testing on every commit
- Fast test execution critical (parallel, incremental)

**4. Risk-Based Testing Prioritization**
- Focus on high-impact areas
- Critical path testing over edge cases
- Business-value-driven test selection

**5. Contract Testing Adoption**
- Consumer-Driven Contract (CDC) testing standard for microservices
- Reduces need for heavy end-to-end testing
- Faster, more reliable service integration validation

### Testing Pyramid Evolution (2025)

**Traditional Pyramid Still Valid:**
```
         /\
        /  \  E2E (Targeted, High-Value)
       /----\
      /      \  Integration/Service (API, Contract)
     /--------\
    /          \  Unit (Broad Base, Fast Feedback)
   /------------\
```

**Modern Adaptations:**
- **Microservices:** Contract testing layer between unit and E2E
- **Cloud-Native:** Integration tests use containers, ephemeral databases
- **AI-Driven:** Automated test generation supplements manual test writing

**Key Principle:** Unit tests provide fast feedback, integration tests validate interactions, E2E tests verify critical user journeys. Balance for speed AND confidence.

---

## Component Taxonomy

### Testing Levels (Test Pyramid)

#### Tier 1: Unit Testing (Foundation)

**Purpose:** Validate small, isolated units of code (functions, methods, components)

**Characteristics:**
- **Fast:** Milliseconds per test
- **Isolated:** No external dependencies (database, network, filesystem)
- **Deterministic:** Same input = same output
- **Broad Coverage:** Many tests, small scope each

**When to Use:**
- Pure functions (input → output, no side effects)
- Business logic and algorithms
- Utility functions and helpers
- Component rendering (without integration)
- Validation logic

**Tools by Language:**
- **TypeScript/JavaScript:** Vitest (primary), Jest (legacy)
- **Python:** pytest (primary)
- **Go:** testing package (stdlib), testify (assertions)
- **Rust:** cargo test (stdlib), proptest (property-based)

---

#### Tier 2: Integration Testing (Middle Layer)

**Purpose:** Validate interactions between components, modules, or services

**Characteristics:**
- **Moderate Speed:** Seconds per test
- **Partial Integration:** Real database, mocked external APIs
- **Focused Scope:** Test component boundaries
- **API Testing:** Validate endpoint contracts

**When to Use:**
- API endpoints (request → response)
- Database operations (CRUD, queries)
- Service-to-service communication
- Event handlers and message processing
- File I/O operations

**Subcategories:**

**A. Component Integration**
- UI components with state management
- Form submission with validation
- Data fetching with caching

**B. API Integration**
- REST endpoint testing
- GraphQL query/mutation testing
- Request/response validation

**C. Database Integration**
- Repository layer testing
- Query correctness validation
- Transaction handling

**D. Contract Testing** (Microservices-Specific)
- Consumer-driven contracts (Pact)
- Provider verification
- Schema validation

**Tools by Language:**
- **TypeScript/JavaScript:** Vitest + MSW (API mocking), Supertest (HTTP testing)
- **Python:** pytest + pytest-httpserver, pytest-postgresql
- **Go:** testing package + httptest, testcontainers
- **Rust:** cargo test + mockito, testcontainers

---

#### Tier 3: End-to-End Testing (Top Layer)

**Purpose:** Validate complete user workflows across the entire application stack

**Characteristics:**
- **Slow:** Minutes per test suite
- **Full Integration:** Real browser, real services, real database
- **Wide Scope:** User journeys from start to finish
- **Brittle:** More prone to flakiness

**When to Use:**
- Critical user journeys (login, checkout, payment)
- Cross-browser compatibility
- Real-world scenarios (not covered by integration tests)
- Regression prevention for core features

**Best Practices:**
- **Limit E2E Tests:** Only high-value scenarios (not every edge case)
- **Stable Selectors:** Use data-testid, not CSS classes
- **Retry Logic:** Handle network flakiness
- **Parallel Execution:** Speed up test runs

**Tools by Language:**
- **TypeScript/JavaScript:** Playwright (primary), Cypress (alternative)
- **Python:** Playwright (Python bindings)
- **Go:** Playwright (Go bindings)
- **Rust:** Limited, use Node.js Playwright or browser automation crates

---

### Special Testing Patterns

#### Property-Based Testing

**Purpose:** Generate random inputs to find edge cases

**When to Use:**
- Complex algorithms with many edge cases
- Data transformation logic
- Validation functions
- Parsers and serializers

**Tools:**
- **TypeScript/JavaScript:** fast-check
- **Python:** hypothesis
- **Go:** gopter
- **Rust:** proptest (primary), quickcheck

**Example Pattern:**
```typescript
// Instead of manually testing edge cases:
test('reverse twice returns original', () => {
  expect(reverse(reverse('hello'))).toBe('hello')
  expect(reverse(reverse('a'))).toBe('a')
  expect(reverse(reverse(''))).toBe('')
})

// Property-based test generates hundreds of cases:
fc.assert(
  fc.property(fc.string(), (str) => {
    expect(reverse(reverse(str))).toBe(str)
  })
)
```

---

#### Snapshot Testing

**Purpose:** Capture output and detect unintended changes

**When to Use:**
- Component rendering (UI snapshots)
- API response validation
- Generated code output
- Configuration files

**Caution:** Easy to over-use. Update snapshots mindfully.

**Tools:**
- **TypeScript/JavaScript:** Vitest snapshots, Jest snapshots
- **Python:** pytest snapshot plugins (pytest-snapshot, snapshottest)
- **Go:** go-snaps
- **Rust:** insta

---

#### Mutation Testing

**Purpose:** Validate test quality by introducing bugs and checking if tests catch them

**When to Use:**
- High-criticality code (payment processing, authentication)
- Validating test suite effectiveness
- Finding weak test coverage

**Tools:**
- **TypeScript/JavaScript:** Stryker Mutator
- **Python:** mutmut, cosmic-ray
- **Go:** go-mutesting
- **Rust:** cargo-mutants

---

## Decision Frameworks

### Framework 1: Which Test Type Should I Use?

**Decision Tree:**

```
START: I need to test [feature]

Q1: Does this feature involve multiple systems/services?
  ├─ YES → Q2
  └─ NO  → Q3

Q2: Is this a critical user-facing workflow?
  ├─ YES → E2E Test (Playwright)
  └─ NO  → Integration Test or Contract Test

Q3: Does this feature interact with external dependencies (DB, API, filesystem)?
  ├─ YES → Integration Test (with real DB/mocked API)
  └─ NO  → Q4

Q4: Is this pure business logic or a pure function?
  ├─ YES → Unit Test (fast, isolated)
  └─ NO  → Consider if component test (UI) or integration test
```

**Examples:**

| Feature | Test Type | Rationale |
|---------|-----------|-----------|
| `calculateTotal(items)` | Unit | Pure function, no dependencies |
| `POST /api/users` endpoint | Integration | Tests API + database interaction |
| User registration flow (form → API → redirect) | E2E | Critical user journey, full stack |
| Microservice A → B communication | Contract | Service interface validation |
| `formatCurrency(amount, locale)` | Unit + Property | Pure logic, many edge cases |
| Form validation logic | Unit | Isolated business rules |
| File upload to S3 | Integration | External service interaction |

---

### Framework 2: How Much of Each Test Type?

**The 70/20/10 Rule (Guideline, Not Law):**

- **70% Unit Tests:** Fast feedback, broad coverage
- **20% Integration Tests:** Validate component interactions
- **10% E2E Tests:** Critical user journeys only

**Microservices Adjustment (60/30/10):**

- **60% Unit Tests:** Still foundation
- **30% Integration/Contract Tests:** Service interactions critical
- **10% E2E Tests:** User-facing workflows

**Anti-Patterns to Avoid:**

❌ **Ice Cream Cone (Inverted Pyramid):**
```
   /------------\  E2E (Too Many, Slow)
  /--------\       Integration (Some)
 /----\            Unit (Too Few)
/  \
```
**Problem:** Slow test suites, flaky tests, long feedback loops

✅ **Balanced Pyramid:**
```
     /\            E2E (Few, High-Value)
    /--\
   /----\          Integration (Moderate)
  /------\
 /--------\
/----------\       Unit (Many, Fast)
```
**Benefit:** Fast feedback, reliable tests, good coverage

---

### Framework 3: When to Mock vs. Use Real Dependencies?

**Mocking Decision Matrix:**

| Dependency | Unit Test | Integration Test | E2E Test |
|------------|-----------|------------------|----------|
| **Database** | Mock (in-memory, stub) | Real (test DB, Docker) | Real (staging DB) |
| **External API** | Mock (MSW, nock) | Mock (MSW, VCR) | Real (or staging) |
| **Filesystem** | Mock (in-memory FS) | Real (temp directory) | Real |
| **Time/Date** | Mock (freezeTime) | Mock (if deterministic) | Real (usually) |
| **Environment Variables** | Mock (setEnv) | Mock (test config) | Real (test env) |
| **Internal Services** | Mock (stub) | Real (or container) | Real |

**Guiding Principles:**

1. **Unit Tests:** Mock everything external (database, API, filesystem)
2. **Integration Tests:** Use real database (ephemeral), mock external APIs
3. **E2E Tests:** Use real everything (or staging equivalents)
4. **Contract Tests:** Mock nothing (test real interface contracts)

---

### Framework 4: Test Data Management Strategy

**Options:**

**A. Fixtures (Static Data)**
- **Pros:** Deterministic, easy to debug
- **Cons:** Can become stale, doesn't test variety
- **Use When:** Testing known scenarios, regression tests

**B. Factories (Generated Data)**
- **Pros:** Flexible, generates variety
- **Cons:** Less deterministic, harder to debug
- **Use When:** Need diverse test data, testing edge cases

**C. Property-Based (Random Data)**
- **Pros:** Finds edge cases you didn't think of
- **Cons:** Can be slow, failures harder to reproduce
- **Use When:** Complex algorithms, parsers, validators

**D. Snapshot (Captured Output)**
- **Pros:** Easy to create, detects changes
- **Cons:** Can be over-used, doesn't validate correctness
- **Use When:** UI components, API responses (stable interfaces)

**Recommended Combination:**
- **Unit Tests:** Fixtures (known inputs) + Property-Based (edge cases)
- **Integration Tests:** Factories (flexible data) + Database seeding
- **E2E Tests:** Fixtures (reproducible scenarios)

---

## Multi-Language Implementations

### TypeScript/JavaScript (PRIMARY)

**Ecosystem Overview:**

**Unit Testing:**
- **Vitest** (Primary, 2025 recommendation)
  - Vite-native, 10x faster than Jest
  - ESM support out-of-the-box
  - Jest-compatible API (easy migration)
  - Better TypeScript support

- **Jest** (Legacy, still widely used)
  - Mature ecosystem, many plugins
  - Slower than Vitest
  - CJS-focused (ESM is bolted on)

**Integration Testing:**
- **MSW (Mock Service Worker)** for API mocking
- **Supertest** for HTTP endpoint testing
- **Testing Library** for component integration

**E2E Testing:**
- **Playwright** (Primary)
  - Cross-browser (Chromium, Firefox, WebKit)
  - Fast, reliable, modern API
  - Built-in parallelization

- **Cypress** (Alternative)
  - Developer-friendly UI
  - Real-time reloading
  - Chrome/Edge/Firefox only (no Safari)

**Property-Based:**
- **fast-check** (excellent TypeScript support)

---

### Python (PRIMARY)

**Ecosystem Overview:**

**Unit Testing:**
- **pytest** (Primary, industry standard)
  - Simple, powerful, extensible
  - Rich fixture system
  - Excellent parametrization
  - Huge plugin ecosystem

**Integration Testing:**
- **pytest** + **pytest-postgresql** (database)
- **pytest** + **pytest-httpserver** (API mocking)
- **pytest** + **pytest-docker** (container integration)

**E2E Testing:**
- **Playwright (Python bindings)**
- **Selenium** (older, still used)

**Property-Based:**
- **hypothesis** (best-in-class, highly recommended)

**Contract Testing:**
- **Pact (Python client)**

---

### Go

**Ecosystem Overview:**

**Unit Testing:**
- **testing** package (stdlib)
- **testify** (assertions, suites, mocks)

**Integration Testing:**
- **httptest** (stdlib, HTTP testing)
- **testcontainers-go** (Docker containers for tests)

**E2E Testing:**
- **Playwright (Go bindings)**
- **chromedp** (headless Chrome automation)

**Property-Based:**
- **gopter** (property-based testing)

---

### Rust

**Ecosystem Overview:**

**Unit Testing:**
- **cargo test** (stdlib, integrated with Cargo)
- **assert macros** (assert_eq!, assert_ne!)

**Integration Testing:**
- **cargo test** (separate tests/ directory)
- **mockito** (HTTP mocking)
- **testcontainers-rs** (Docker containers)

**E2E Testing:**
- Limited native support
- **fantoccini** (WebDriver client)
- Use Playwright (via Node.js bridge) for full browser testing

**Property-Based:**
- **proptest** (primary, Hypothesis-inspired)
- **quickcheck** (older, Haskell-inspired)

---

## Library Recommendations

### Research Summary

**Research Date:** December 3, 2025
**Libraries Evaluated:** 15+
**Research Tools:** Google Search Grounding (Vertex AI), Context7

---

### TypeScript/JavaScript Testing Libraries (2025)

#### **Primary: Vitest** (Unit + Integration)

**Library:** `/vitest-dev/vitest`
**Trust Score:** 93.5/100
**Code Snippets:** 1,234+
**Bundle Size:** ~450KB (dev dependency)

**Why Vitest?**
- **10x Faster than Jest:** Vite-native, instant HMR, smart watch mode
- **Jest-Compatible API:** Easy migration from Jest
- **ESM-First:** Native ES Modules support (no config needed)
- **Better TypeScript:** First-class TypeScript support
- **Modern Features:** Built-in coverage (c8/istanbul), workspace support
- **Active Development:** Rapidly evolving, community-driven

**When to Use:**
- Any project using Vite (React, Vue, Svelte)
- New projects (2025 recommendation)
- Projects needing fast test feedback
- TypeScript projects

**Installation:**
```bash
npm install -D vitest @vitest/ui
```

**Example (Unit Test):**
```typescript
import { describe, test, expect } from 'vitest'
import { calculateTotal } from './cart'

describe('calculateTotal', () => {
  test('calculates total with tax', () => {
    const items = [
      { price: 10, quantity: 2 },
      { price: 5, quantity: 1 }
    ]
    expect(calculateTotal(items, 0.1)).toBe(27.5) // (20 + 5) * 1.1
  })
})
```

**Example (Integration Test with MSW):**
```typescript
import { beforeAll, afterAll, afterEach, test, expect } from 'vitest'
import { setupServer } from 'msw/node'
import { http, HttpResponse } from 'msw'
import { fetchUser } from './api'

const server = setupServer(
  http.get('/api/user/:id', ({ params }) => {
    return HttpResponse.json({ id: params.id, name: 'Test User' })
  })
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

test('fetchUser returns user data', async () => {
  const user = await fetchUser('123')
  expect(user).toEqual({ id: '123', name: 'Test User' })
})
```

---

#### **Alternative: Jest** (Unit + Integration)

**Library:** `/jestjs/jest`
**Trust Score:** 94.8/100
**Code Snippets:** 1,717+
**Bundle Size:** ~2MB (dev dependency)

**Why Jest?**
- **Mature Ecosystem:** Huge plugin library, extensive community
- **Batteries-Included:** Mocking, snapshots, coverage built-in
- **Facebook-Backed:** Used in React, React Native, Next.js
- **Stable:** Production-ready, well-tested

**When to Use:**
- Legacy projects already using Jest
- Projects requiring specific Jest plugins
- React Native projects (Jest is default)
- Teams familiar with Jest

**Migration Note:** Vitest API is Jest-compatible. Most tests work with minimal changes.

---

#### **Primary: Playwright** (E2E)

**Library:** `/microsoft/playwright`
**Trust Score:** 89.4/100
**Code Snippets:** 2,623+
**Multi-Language:** TypeScript, Python, Java, .NET, Go

**Why Playwright?**
- **Cross-Browser:** Chromium, Firefox, WebKit (Safari)
- **Fast and Reliable:** Auto-wait, retry-ability, parallel execution
- **Modern API:** Async/await, Promise-based
- **Microsoft-Backed:** Active development, enterprise support
- **Built-In Tooling:** Codegen, trace viewer, inspector

**When to Use:**
- E2E testing for web applications
- Cross-browser testing requirements
- Automated user workflow testing
- Visual regression testing (with screenshots)

**Installation:**
```bash
npm install -D @playwright/test
npx playwright install
```

**Example (E2E Test):**
```typescript
import { test, expect } from '@playwright/test'

test('user can complete checkout', async ({ page }) => {
  // Navigate
  await page.goto('https://example.com')

  // Add to cart
  await page.getByRole('button', { name: 'Add to Cart' }).click()
  await expect(page.getByText('1 item in cart')).toBeVisible()

  // Checkout
  await page.getByRole('link', { name: 'Checkout' }).click()
  await page.getByLabel('Email').fill('test@example.com')
  await page.getByLabel('Card Number').fill('4242424242424242')
  await page.getByRole('button', { name: 'Complete Purchase' }).click()

  // Verify success
  await expect(page.getByText('Order confirmed')).toBeVisible()
})
```

**Fixtures Example:**
```typescript
import { test as base } from '@playwright/test'

type Fixtures = {
  authenticatedPage: Page
}

const test = base.extend<Fixtures>({
  authenticatedPage: async ({ page }, use) => {
    // Login before each test
    await page.goto('/login')
    await page.getByLabel('Email').fill('user@example.com')
    await page.getByLabel('Password').fill('password123')
    await page.getByRole('button', { name: 'Login' }).click()
    await page.waitForURL('/dashboard')

    await use(page)
  }
})

test('dashboard shows user data', async ({ authenticatedPage }) => {
  await expect(authenticatedPage.getByText('Welcome back')).toBeVisible()
})
```

---

#### **Alternative: Cypress** (E2E)

**Library:** Cypress (not in Context7 top results, but widely used)
**Popularity:** Very high (used in Angular, Vue)
**Browser Support:** Chrome, Edge, Firefox (no Safari/WebKit)

**Why Cypress?**
- **Developer-Friendly:** Interactive test runner, time-travel debugging
- **Real-Time Reloading:** See tests update as you write them
- **Network Stubbing:** Built-in request/response mocking
- **Screenshots/Videos:** Automatic failure capture

**When to Use:**
- Teams preferring Cypress DX
- Chrome/Firefox-only testing acceptable
- Need for interactive debugging

**Limitation:** No Safari/WebKit support (Playwright has this)

---

#### **Primary: MSW (Mock Service Worker)** (API Mocking)

**Library:** MSW (Mock Service Worker)
**Use Case:** Mock HTTP requests in tests and development

**Why MSW?**
- **Service Worker Based:** Intercepts requests at network level
- **Framework Agnostic:** Works with any testing library
- **Realistic Mocking:** Same handlers for tests and development
- **TypeScript Support:** Full type safety

**When to Use:**
- Integration tests requiring API mocking
- Component tests with data fetching
- Development without backend (storybook, local dev)

**Installation:**
```bash
npm install -D msw
```

**Example:**
```typescript
import { http, HttpResponse } from 'msw'
import { setupServer } from 'msw/node'

const server = setupServer(
  http.get('/api/products', () => {
    return HttpResponse.json([
      { id: 1, name: 'Product 1', price: 19.99 },
      { id: 2, name: 'Product 2', price: 29.99 }
    ])
  })
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

---

### Python Testing Libraries (2025)

#### **Primary: pytest** (Unit + Integration)

**Library:** `/websites/pytest_en_stable`
**Trust Score:** 86.7/100
**Code Snippets:** 1,974+
**Ecosystem:** Massive plugin ecosystem (500+ plugins)

**Why pytest?**
- **Industry Standard:** De facto Python testing framework
- **Simple Syntax:** No boilerplate (no classes required)
- **Powerful Fixtures:** Dependency injection, parametrization
- **Rich Plugins:** pytest-cov, pytest-xdist, pytest-asyncio, pytest-django
- **Excellent Error Messages:** Clear failure output

**When to Use:**
- All Python projects (Django, FastAPI, Flask, CLI tools)
- Unit testing, integration testing, API testing
- Any testing need in Python

**Installation:**
```bash
pip install pytest pytest-cov pytest-asyncio
```

**Example (Unit Test):**
```python
import pytest
from cart import calculate_total

def test_calculate_total_with_tax():
    items = [
        {"price": 10, "quantity": 2},
        {"price": 5, "quantity": 1}
    ]
    assert calculate_total(items, tax_rate=0.1) == 27.5

@pytest.mark.parametrize("tax_rate,expected", [
    (0.0, 25.0),
    (0.1, 27.5),
    (0.2, 30.0)
])
def test_calculate_total_various_tax_rates(tax_rate, expected):
    items = [{"price": 10, "quantity": 2}, {"price": 5, "quantity": 1}]
    assert calculate_total(items, tax_rate) == expected
```

**Example (Fixtures):**
```python
import pytest
from database import Database

@pytest.fixture
def db():
    """Provide a clean database for each test"""
    database = Database(':memory:')
    database.create_tables()
    yield database
    database.close()

@pytest.fixture
def sample_user(db):
    """Provide a sample user in the database"""
    user = db.create_user(email='test@example.com', name='Test User')
    return user

def test_user_creation(db):
    user = db.create_user(email='new@example.com', name='New User')
    assert user.email == 'new@example.com'

def test_user_retrieval(sample_user, db):
    found = db.get_user(sample_user.id)
    assert found.email == sample_user.email
```

**Example (Integration Test with Database):**
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base, engine

@pytest.fixture
def client():
    """Test client with clean database"""
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)

def test_create_user(client):
    response = client.post('/api/users', json={
        'email': 'test@example.com',
        'name': 'Test User'
    })
    assert response.status_code == 201
    data = response.json()
    assert data['email'] == 'test@example.com'
    assert 'id' in data
```

---

#### **Primary: Playwright (Python)** (E2E)

**Library:** `/microsoft/playwright-python`
**Trust Score:** 95.2/100
**Code Snippets:** 56+

**Why Playwright for Python?**
- **Same API as TypeScript:** Consistent across languages
- **Full Browser Support:** Chromium, Firefox, WebKit
- **Python-Native:** Async/await, pytest integration

**Installation:**
```bash
pip install pytest-playwright
playwright install
```

**Example:**
```python
import pytest
from playwright.sync_api import Page, expect

def test_checkout_flow(page: Page):
    # Navigate
    page.goto('https://example.com')

    # Add to cart
    page.get_by_role('button', name='Add to Cart').click()
    expect(page.get_by_text('1 item in cart')).to_be_visible()

    # Checkout
    page.get_by_role('link', name='Checkout').click()
    page.get_by_label('Email').fill('test@example.com')
    page.get_by_label('Card Number').fill('4242424242424242')
    page.get_by_role('button', name='Complete Purchase').click()

    # Verify
    expect(page.get_by_text('Order confirmed')).to_be_visible()
```

---

#### **Primary: hypothesis** (Property-Based)

**Library:** Hypothesis
**Use Case:** Property-based testing (generative testing)

**Why hypothesis?**
- **Best-in-Class:** Industry standard for Python property testing
- **Smart Shrinking:** Minimizes failing examples
- **Extensive Strategies:** Generates all Python types
- **Deterministic:** Reproducible failures with seeds

**Installation:**
```bash
pip install hypothesis
```

**Example:**
```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_reverse_reverse_is_identity(lst):
    """Reversing a list twice returns original"""
    assert list(reversed(list(reversed(lst)))) == lst

@given(st.text(), st.text())
def test_string_concatenation_length(s1, s2):
    """Concatenated string length equals sum of parts"""
    result = s1 + s2
    assert len(result) == len(s1) + len(s2)
```

---

### Go Testing Libraries

#### **Primary: testing (stdlib) + testify**

**Library:** `testing` (stdlib) + `github.com/stretchr/testify`
**Why testify?** Adds assertions, mocks, suites to stdlib testing

**Example (Unit Test):**
```go
package cart_test

import (
    "testing"
    "github.com/stretchr/testify/assert"
    "yourapp/cart"
)

func TestCalculateTotal(t *testing.T) {
    items := []cart.Item{
        {Price: 10.0, Quantity: 2},
        {Price: 5.0, Quantity: 1},
    }

    total := cart.CalculateTotal(items, 0.1)
    assert.Equal(t, 27.5, total)
}

func TestCalculateTotalNoTax(t *testing.T) {
    items := []cart.Item{
        {Price: 10.0, Quantity: 2},
    }

    total := cart.CalculateTotal(items, 0.0)
    assert.Equal(t, 20.0, total)
}
```

**Example (Integration Test with httptest):**
```go
package api_test

import (
    "net/http"
    "net/http/httptest"
    "testing"
    "github.com/stretchr/testify/assert"
    "yourapp/api"
)

func TestCreateUser(t *testing.T) {
    handler := api.NewHandler()

    req := httptest.NewRequest("POST", "/api/users", strings.NewReader(`{
        "email": "test@example.com",
        "name": "Test User"
    }`))
    req.Header.Set("Content-Type", "application/json")

    rr := httptest.NewRecorder()
    handler.ServeHTTP(rr, req)

    assert.Equal(t, http.StatusCreated, rr.Code)
    assert.Contains(t, rr.Body.String(), "test@example.com")
}
```

---

### Rust Testing Libraries

#### **Primary: cargo test (stdlib)**

**Library:** Built-in Rust testing (cargo test)
**Why Built-In?** Integrated with Cargo, no external dependencies needed

**Example (Unit Test):**
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_calculate_total() {
        let items = vec![
            Item { price: 10.0, quantity: 2 },
            Item { price: 5.0, quantity: 1 },
        ];

        assert_eq!(calculate_total(&items, 0.1), 27.5);
    }

    #[test]
    #[should_panic(expected = "tax rate must be between 0 and 1")]
    fn test_invalid_tax_rate() {
        let items = vec![Item { price: 10.0, quantity: 1 }];
        calculate_total(&items, 1.5); // Should panic
    }
}
```

**Example (Property-Based with proptest):**
```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn test_reverse_reverse_is_identity(ref v in prop::collection::vec(any::<i32>(), 0..100)) {
        let reversed_twice: Vec<_> = v.iter().rev().rev().copied().collect();
        assert_eq!(v, &reversed_twice);
    }
}
```

---

### Contract Testing (Multi-Language)

#### **Primary: Pact** (Consumer-Driven Contracts)

**Library:** Pact (pact.io)
**Language Support:** JavaScript, Python, Go, Rust, Java, .NET, Ruby

**Why Pact?**
- **Consumer-Driven:** Consumers define expected contracts
- **Bi-Directional:** Tests both consumer and provider
- **Microservices Standard:** Industry-standard for service contracts
- **Pact Broker:** Central repository for contracts

**When to Use:**
- Microservices architecture
- Service-to-service communication
- API contract validation
- Reduce E2E testing needs

**Example (JavaScript Consumer):**
```typescript
import { PactV3 } from '@pact-foundation/pact'
import { fetchUser } from './api'

const provider = new PactV3({
  consumer: 'UserServiceClient',
  provider: 'UserService'
})

describe('User API', () => {
  test('fetch user by ID', async () => {
    await provider
      .given('user 123 exists')
      .uponReceiving('a request for user 123')
      .withRequest({
        method: 'GET',
        path: '/users/123'
      })
      .willRespondWith({
        status: 200,
        headers: { 'Content-Type': 'application/json' },
        body: {
          id: '123',
          name: 'Test User',
          email: 'test@example.com'
        }
      })

    await provider.executeTest(async (mockServer) => {
      const user = await fetchUser('123', mockServer.url)
      expect(user.name).toBe('Test User')
    })
  })
})
```

**Example (Python Provider Verification):**
```python
from pact import Verifier

verifier = Verifier(provider='UserService', provider_base_url='http://localhost:8000')

success = verifier.verify_pacts(
    './pacts/UserServiceClient-UserService.json',
    provider_states_setup_url='http://localhost:8000/_pact/provider_states'
)

assert success == 0
```

---

### Coverage Tools

#### **TypeScript/JavaScript**

**Vitest Coverage (Built-In):**
```bash
npm install -D @vitest/coverage-v8
```

**Configuration:**
```typescript
// vitest.config.ts
export default {
  test: {
    coverage: {
      provider: 'v8', // or 'istanbul'
      reporter: ['text', 'html', 'json'],
      include: ['src/**/*.ts'],
      exclude: ['**/*.test.ts', '**/*.spec.ts']
    }
  }
}
```

**Run:**
```bash
vitest --coverage
```

---

#### **Python**

**pytest-cov (pytest plugin):**
```bash
pip install pytest-cov
pytest --cov=src --cov-report=html --cov-report=term
```

---

#### **Go**

**Built-in coverage:**
```bash
go test -cover ./...
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

---

#### **Rust**

**cargo-tarpaulin (coverage tool):**
```bash
cargo install cargo-tarpaulin
cargo tarpaulin --out Html
```

---

## Skill Structure Design

### Skill File Organization

**Proposed Structure:**

```
testing-strategies/
├── SKILL.md                          # Main skill file (<500 lines)
├── references/
│   ├── testing-pyramid.md            # Test pyramid framework
│   ├── decision-tree.md              # Which test type to use
│   ├── test-data-strategies.md       # Fixtures, factories, property-based
│   ├── mocking-strategies.md         # When to mock, how to mock
│   ├── coverage-strategies.md        # Meaningful coverage targets
│   └── contract-testing.md           # Microservices contract testing
├── examples/
│   ├── typescript/
│   │   ├── vitest-unit.test.ts       # Unit test examples
│   │   ├── vitest-integration.test.ts # Integration with MSW
│   │   ├── playwright-e2e.spec.ts    # E2E test examples
│   │   └── property-based.test.ts    # fast-check examples
│   ├── python/
│   │   ├── pytest_unit_test.py       # Unit test examples
│   │   ├── pytest_fixtures_test.py   # Fixture patterns
│   │   ├── pytest_integration_test.py # Integration examples
│   │   ├── playwright_e2e_test.py    # E2E examples
│   │   └── hypothesis_property_test.py # Property-based examples
│   ├── go/
│   │   ├── unit_test.go              # stdlib testing examples
│   │   ├── integration_test.go       # httptest examples
│   │   └── testify_example_test.go   # testify assertions
│   └── rust/
│       ├── unit_tests.rs             # cargo test examples
│       ├── integration_tests.rs      # integration test patterns
│       └── proptest_example.rs       # Property-based examples
└── scripts/
    └── coverage-report.sh            # Generate coverage across languages
```

---

### SKILL.md Structure (Main File)

**Sections (Target: ~400-450 lines):**

1. **Frontmatter** (YAML)
   - name, description

2. **Purpose** (2-3 paragraphs)
   - What this skill teaches
   - When to use this skill

3. **Universal Testing Concepts** (~100 lines)
   - Testing pyramid overview
   - When to use unit/integration/E2E/contract
   - Quick decision tree
   - Coverage targets

4. **Language-Specific Quick Starts** (~150 lines)
   - TypeScript/JavaScript (Vitest + Playwright)
   - Python (pytest + Playwright)
   - Go (testing + testify)
   - Rust (cargo test)

5. **Common Patterns** (~100 lines)
   - Mocking strategies
   - Test data management (fixtures, factories)
   - Snapshot testing
   - Property-based testing

6. **Integration with CI/CD** (~50 lines)
   - Running tests in pipelines
   - Parallel execution
   - Coverage reporting

7. **Reference Links** (~20 lines)
   - Links to detailed references/ files
   - Links to examples/ files

---

### Progressive Disclosure Strategy

**Main SKILL.md Contains:**
- High-level decision frameworks
- Quick-start examples (minimal code)
- When to use each test type
- Links to detailed references

**References/ Contains:**
- Detailed decision trees (references/decision-tree.md)
- Comprehensive mocking patterns (references/mocking-strategies.md)
- In-depth coverage strategies (references/coverage-strategies.md)
- Contract testing guide (references/contract-testing.md)

**Examples/ Contains:**
- Working code examples (copy-paste ready)
- Organized by language
- Real-world scenarios

**Scripts/ Contains:**
- Coverage report generation (cross-language)
- Test result aggregation (optional)

---

## Integration Points

### Integration with Existing Skills

#### 1. **building-forms** Skill
- **Unit Tests:** Validate form validation logic
- **Integration Tests:** Test form submission with API
- **E2E Tests:** Complete form workflow (fill, submit, redirect)

**Example Integration:**
```typescript
// Unit test: Validation logic
import { validateEmail } from './validation'

test('validateEmail accepts valid emails', () => {
  expect(validateEmail('test@example.com')).toBe(true)
})

// Integration test: Form submission
import { submitForm } from './api'
import { http, HttpResponse } from 'msw'

test('submitForm posts to API', async () => {
  server.use(
    http.post('/api/forms', () => HttpResponse.json({ success: true }))
  )
  const result = await submitForm({ email: 'test@example.com' })
  expect(result.success).toBe(true)
})

// E2E test: Full workflow
test('user can submit contact form', async ({ page }) => {
  await page.goto('/contact')
  await page.getByLabel('Email').fill('test@example.com')
  await page.getByLabel('Message').fill('Hello')
  await page.getByRole('button', { name: 'Submit' }).click()
  await expect(page.getByText('Thank you')).toBeVisible()
})
```

---

#### 2. **api-patterns** Skill
- **Integration Tests:** Validate API endpoints (request → response)
- **Contract Tests:** Service-to-service contracts
- **E2E Tests:** API workflows (authentication → request → response)

**Example Integration:**
```typescript
// Integration test: API endpoint
test('POST /api/users creates user', async () => {
  const response = await request(app)
    .post('/api/users')
    .send({ email: 'test@example.com', name: 'Test' })
  expect(response.status).toBe(201)
  expect(response.body).toHaveProperty('id')
})

// Contract test: Consumer side
await provider
  .given('user service is available')
  .uponReceiving('a request to create user')
  .withRequest({
    method: 'POST',
    path: '/api/users',
    body: { email: 'test@example.com' }
  })
  .willRespondWith({
    status: 201,
    body: { id: string, email: 'test@example.com' }
  })
```

---

#### 3. **building-ci-pipelines** Skill
- **CI Integration:** Running tests in GitHub Actions, GitLab CI
- **Parallel Execution:** Splitting tests across workers
- **Coverage Reporting:** Uploading coverage to Codecov/Coveralls

**Example Integration (.github/workflows/test.yml):**
```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install dependencies
        run: npm ci

      - name: Run unit tests
        run: npm run test:unit

      - name: Run integration tests
        run: npm run test:integration

      - name: Run E2E tests
        run: npx playwright test

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
```

---

#### 4. **visualizing-data** Skill
- **Snapshot Tests:** Capture chart rendering output
- **Integration Tests:** Test data transformation → chart
- **Visual Regression:** Screenshot-based testing (Playwright)

**Example Integration:**
```typescript
// Snapshot test: Chart configuration
test('generates correct chart config', () => {
  const config = generateChartConfig(mockData)
  expect(config).toMatchSnapshot()
})

// Visual regression test
test('bar chart renders correctly', async ({ page }) => {
  await page.goto('/charts/bar')
  await expect(page.locator('#chart')).toHaveScreenshot('bar-chart.png')
})
```

---

#### 5. **theming-components** Skill
- **Unit Tests:** Validate token calculations
- **Integration Tests:** Test theme switching
- **Visual Regression:** Ensure themes render correctly

**Example Integration:**
```typescript
// Unit test: Token resolution
test('resolves color token correctly', () => {
  const color = resolveToken('color.primary')
  expect(color).toBe('#0066cc')
})

// Visual regression: Theme variants
test('dark theme renders correctly', async ({ page }) => {
  await page.goto('/')
  await page.evaluate(() => {
    document.documentElement.setAttribute('data-theme', 'dark')
  })
  await expect(page).toHaveScreenshot('dark-theme.png')
})
```

---

### Integration with CI/CD Workflows

**Key Patterns:**

1. **Fast Feedback Loop:**
   - Run unit tests on every commit (< 1 minute)
   - Run integration tests on PR (< 5 minutes)
   - Run E2E tests before merge (< 10 minutes)

2. **Parallel Execution:**
   - Vitest: `vitest --reporter=verbose --threads`
   - Playwright: `playwright test --workers=4`
   - pytest: `pytest -n auto` (pytest-xdist)

3. **Coverage Thresholds:**
   - Fail build if coverage drops below threshold
   - Track coverage trends over time
   - Focus on meaningful coverage (not 100%)

4. **Test Artifacts:**
   - Upload test results (JUnit XML)
   - Upload screenshots/videos on failure
   - Upload coverage reports

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1)

**Deliverables:**
- [x] Complete init.md (this document)
- [ ] Create SKILL.md main file
- [ ] Write references/testing-pyramid.md
- [ ] Write references/decision-tree.md

**Content Focus:**
- Universal testing concepts
- Testing pyramid framework
- Decision tree: Which test type to use

---

### Phase 2: TypeScript/JavaScript (Week 2)

**Deliverables:**
- [ ] Complete Vitest examples (unit + integration)
- [ ] Complete Playwright examples (E2E)
- [ ] MSW integration examples
- [ ] Property-based testing (fast-check)

**Files:**
- examples/typescript/vitest-unit.test.ts
- examples/typescript/vitest-integration.test.ts
- examples/typescript/playwright-e2e.spec.ts
- examples/typescript/property-based.test.ts

---

### Phase 3: Python (Week 3)

**Deliverables:**
- [ ] Complete pytest examples (unit + integration)
- [ ] pytest fixtures patterns
- [ ] Playwright (Python) examples
- [ ] hypothesis (property-based) examples

**Files:**
- examples/python/pytest_unit_test.py
- examples/python/pytest_fixtures_test.py
- examples/python/pytest_integration_test.py
- examples/python/playwright_e2e_test.py
- examples/python/hypothesis_property_test.py

---

### Phase 4: Go & Rust (Week 4)

**Deliverables:**
- [ ] Go testing examples (stdlib + testify)
- [ ] Go httptest integration examples
- [ ] Rust cargo test examples
- [ ] Rust proptest examples

**Files:**
- examples/go/unit_test.go
- examples/go/integration_test.go
- examples/rust/unit_tests.rs
- examples/rust/proptest_example.rs

---

### Phase 5: Advanced Topics (Week 5)

**Deliverables:**
- [ ] Write references/mocking-strategies.md
- [ ] Write references/test-data-strategies.md
- [ ] Write references/contract-testing.md
- [ ] Contract testing examples (Pact)

---

### Phase 6: Integration & Polish (Week 6)

**Deliverables:**
- [ ] Write references/coverage-strategies.md
- [ ] CI/CD integration examples
- [ ] Create scripts/coverage-report.sh
- [ ] Cross-link with related skills (forms, APIs, CI/CD)

---

## Validation Checklist

### Before Creating SKILL.md

- [x] Research complete (Google Search + Context7)
- [x] Library recommendations validated (trust scores, snippets)
- [x] Decision frameworks designed
- [x] Multi-language patterns identified
- [x] Integration points with other skills mapped

### Before Finalizing Skill

- [ ] SKILL.md under 500 lines
- [ ] All references/ files created
- [ ] All examples/ files working and tested
- [ ] Progressive disclosure effective (main → references → examples)
- [ ] Tested with real projects
- [ ] Cross-language consistency validated
- [ ] Integration with related skills verified

---

## Success Metrics

**This skill is successful if developers can:**

1. **Make Strategic Decisions:**
   - Choose correct test type for a feature (unit vs. integration vs. E2E)
   - Balance test pyramid effectively (not too many E2E tests)
   - Know when to mock vs. use real dependencies

2. **Write Effective Tests:**
   - Unit tests with proper isolation
   - Integration tests with real DB, mocked APIs
   - E2E tests for critical user journeys
   - Contract tests for microservice interfaces

3. **Achieve Quality Metrics:**
   - Meaningful coverage (70%+ for critical paths)
   - Fast feedback (<1 min for unit tests)
   - Reliable tests (minimal flakiness)

4. **Integrate with Workflow:**
   - Tests run in CI/CD pipelines
   - Coverage tracked over time
   - Test failures block deployments

---

## Future Enhancements

**Potential Additions (Not in Initial Release):**

1. **Visual Regression Testing**
   - Playwright screenshots
   - Percy/Chromatic integration
   - Storybook snapshot testing

2. **Performance Testing**
   - Benchmark testing (criterion for Rust, benchmark.js for JS)
   - Load testing (k6, Locust)
   - Memory profiling

3. **Mutation Testing**
   - Stryker Mutator (JavaScript)
   - mutmut (Python)
   - cargo-mutants (Rust)

4. **Advanced E2E Patterns**
   - Multi-tab testing
   - File upload/download testing
   - Accessibility testing (axe-core)

5. **AI-Powered Testing**
   - AI test generation
   - Intelligent test selection
   - Automated test maintenance

---

## Appendix: Library Comparison Matrix

### TypeScript/JavaScript Unit Testing

| Library | Trust | Snippets | Speed | ESM Support | Bundle Size | Best For |
|---------|-------|----------|-------|-------------|-------------|----------|
| **Vitest** | 93.5 | 1,234+ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 450KB | Vite projects, modern apps |
| **Jest** | 94.8 | 1,717+ | ⭐⭐⭐ | ⭐⭐ | 2MB | Legacy projects, React Native |

---

### E2E Testing

| Library | Trust | Snippets | Browsers | Speed | DX | Best For |
|---------|-------|----------|----------|-------|-----|----------|
| **Playwright** | 89.4 | 2,623+ | Chrome, Firefox, Safari | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Cross-browser, CI/CD |
| **Cypress** | N/A | High | Chrome, Firefox | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Interactive debugging |

---

### Python Testing

| Library | Trust | Snippets | Features | Ecosystem | Best For |
|---------|-------|----------|----------|-----------|----------|
| **pytest** | 86.7 | 1,974+ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ (500+ plugins) | All Python projects |
| **hypothesis** | High | Medium | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Property-based testing |

---

## References

**Research Sources:**
- Google Search Grounding (Vertex AI): Testing strategies 2025 best practices
- Context7 Documentation: Vitest, Playwright, pytest, Jest
- Official Documentation: pytest.org, playwright.dev, vitest.dev
- Industry Best Practices: Test pyramid, shift-left testing, continuous testing

**Related Skills:**
- `building-forms` - Form validation testing
- `api-patterns` - API endpoint testing
- `building-ci-pipelines` - CI/CD integration
- `visualizing-data` - Chart snapshot testing
- `theming-components` - Visual regression testing

---

**Document Status:** ✅ Complete
**Next Step:** Create SKILL.md from this master plan
**Owner:** AI Design Components Project
**Last Updated:** December 3, 2025
