---
sidebar_position: 1
title: Testing Strategies
description: Strategic guidance for choosing and implementing testing approaches across the test pyramid
tags: [devops, testing, unit-tests, integration-tests, e2e, contract-testing]
---

# Testing Strategies

Build comprehensive, effective test suites by strategically selecting and implementing the right testing approaches across unit, integration, E2E, and contract testing levels.

## When to Use

Use this skill when:
- Building a new feature that requires test coverage
- Designing a testing strategy for a new project
- Refactoring existing tests to improve speed or reliability
- Setting up CI/CD pipelines with testing stages
- Choosing between unit, integration, or E2E testing approaches
- Implementing contract testing for microservices
- Managing test data with fixtures, factories, or property-based testing

## Key Features

- **Test Pyramid Framework**: Optimize test distribution (60-70% unit, 20-30% integration, 10% E2E) for fast feedback and reliable coverage
- **Multi-Language Support**: Consistent testing patterns across TypeScript, Python, Go, and Rust
- **Decision Tree**: Universal framework for choosing which test type to use
- **Modern Tools**: Vitest (10x faster than Jest), Playwright, pytest, property-based testing
- **Test Data Strategies**: Fixtures, factories, and property-based testing guidance
- **CI/CD Integration**: Fast feedback loop patterns with parallel execution
- **Coverage Metrics**: Meaningful coverage targets and mutation testing

## Testing Pyramid Framework

```
         /\
        /  \  E2E Tests (10%)
       /----\  - Slow but comprehensive
      /      \  - Full stack validation
     /--------\
    /          \  Integration Tests (20-30%)
   /            \  - Moderate speed
  /--------------\  - Component interactions
 /                \
/------------------\  Unit Tests (60-70%)
                      - Fast feedback
                      - Isolated units
```

**Key Principle**: More unit tests (fast, isolated), fewer E2E tests (slow, comprehensive). Integration tests bridge the gap.

## Quick Decision Tree

```
START: Need to test [feature]

Q1: Does this involve multiple systems/services?
  ├─ YES → Q2
  └─ NO  → Q3

Q2: Is this a critical user-facing workflow?
  ├─ YES → E2E Test (complete user journey)
  └─ NO  → Integration or Contract Test

Q3: Does this interact with external dependencies (DB, API, filesystem)?
  ├─ YES → Integration Test (real DB, mocked API)
  └─ NO  → Q4

Q4: Is this pure business logic or a pure function?
  ├─ YES → Unit Test (fast, isolated)
  └─ NO  → Component or Integration Test
```

## Tool Recommendations

### TypeScript/JavaScript
- **Unit Testing**: Vitest (primary - 10x faster than Jest)
- **Integration**: Vitest + MSW (API mocking), Supertest (HTTP)
- **E2E**: Playwright (cross-browser, fast)
- **Property-Based**: fast-check

### Python
- **Unit/Integration**: pytest (industry standard)
- **Property-Based**: hypothesis (best-in-class)
- **E2E**: Playwright

### Go
- **Unit**: testing package (stdlib) + testify
- **Integration**: httptest, testcontainers
- **Property-Based**: gopter

### Rust
- **Unit**: cargo test (stdlib)
- **Integration**: testcontainers
- **Property-Based**: proptest

## Quick Start: TypeScript with Vitest

```typescript
// Unit test
import { describe, test, expect } from 'vitest'

test('calculates total with tax', () => {
  const items = [{ price: 10, quantity: 2 }]
  expect(calculateTotal(items, 0.1)).toBe(22)
})

// Integration test with MSW
import { setupServer } from 'msw/node'
import { http, HttpResponse } from 'msw'

const server = setupServer(
  http.get('/api/user/:id', ({ params }) => {
    return HttpResponse.json({ id: params.id, name: 'Test User' })
  })
)

// E2E test with Playwright
import { test, expect } from '@playwright/test'

test('user can checkout', async ({ page }) => {
  await page.goto('https://example.com')
  await page.getByRole('button', { name: 'Add to Cart' }).click()
  await expect(page.getByText('1 item in cart')).toBeVisible()
})
```

## Test Type Selection Examples

| Feature | Test Type | Rationale |
|---------|-----------|-----------|
| `calculateTotal(items)` | Unit | Pure function, no dependencies |
| `POST /api/users` endpoint | Integration | Tests API + database interaction |
| User registration flow | E2E | Critical user journey, full stack |
| Microservice A → B communication | Contract | Service interface validation |
| `formatCurrency(amount, locale)` | Unit + Property | Pure logic, many edge cases |

## Coverage and Metrics

### Recommended Coverage Targets
- **Critical Business Logic**: 90%+ coverage
- **API Endpoints**: 80%+ coverage
- **Utility Functions**: 70%+ coverage
- **UI Components**: 60%+ coverage (focus on logic, not markup)
- **Overall Project**: 70-80% coverage

**Anti-Pattern**: Aiming for 100% coverage leads to testing trivial code and false confidence.

### Mutation Testing
Validate test quality by introducing bugs and verifying tests catch them.

**Tools**:
- **TypeScript/JavaScript**: Stryker Mutator
- **Python**: mutmut
- **Go**: go-mutesting
- **Rust**: cargo-mutants

## CI/CD Integration Patterns

**Stage 1: Pre-Commit (< 30 seconds)**
- Lint and format checks
- Unit tests (critical paths only)

**Stage 2: On Commit (< 2 minutes)**
- All unit tests
- Static analysis

**Stage 3: Pull Request (< 5 minutes)**
- Integration tests
- Coverage reporting

**Stage 4: Pre-Merge (< 10 minutes)**
- E2E tests (critical paths)
- Cross-browser testing

### Parallel Execution for Speed
- **Vitest**: `vitest --threads`
- **Playwright**: `playwright test --workers=4`
- **pytest**: `pytest -n auto` (requires pytest-xdist)
- **Go**: `go test -parallel 4`

## Common Anti-Patterns to Avoid

1. **The Ice Cream Cone (Inverted Pyramid)**: Too many E2E tests, too few unit tests → Slow test suites, flaky tests
2. **Testing Implementation Details**: Tests coupled to internal structure, not behavior
3. **Over-Mocking in Integration Tests**: Mocking everything defeats purpose
4. **Flaky E2E Tests**: Use auto-wait features, avoid hardcoded waits, use stable selectors

## Related Skills

- [Building CI Pipelines](./building-ci-pipelines) - Test automation, parallel execution, and coverage reporting
- [Platform Engineering](./platform-engineering) - Golden paths with testing best practices
- [Writing Dockerfiles](./writing-dockerfiles) - Containerized testing environments

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/testing-strategies)
- [Testing Pyramid Guide](https://github.com/ancoleman/ai-design-components/tree/main/skills/testing-strategies/references/testing-pyramid.md)
- [Language-Specific Examples](https://github.com/ancoleman/ai-design-components/tree/main/skills/testing-strategies/examples)
