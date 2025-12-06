# Coverage and Quality Metrics

## Table of Contents

1. [Meaningful Coverage Targets](#meaningful-coverage-targets)
2. [Coverage Tools](#coverage-tools)
3. [Mutation Testing](#mutation-testing)
4. [Beyond Line Coverage](#beyond-line-coverage)

## Meaningful Coverage Targets

### Anti-Pattern: 100% Coverage Goal

**Problem**: Chasing 100% coverage leads to:
- Testing trivial code (getters/setters)
- Testing framework code
- False sense of security
- Wasted effort

**Better Approach**: Risk-based coverage targets

### Recommended Targets

| Code Type | Target | Rationale |
|-----------|--------|-----------|
| **Critical Business Logic** | 90%+ | Payment, auth, data integrity |
| **API Endpoints** | 80%+ | Public interfaces |
| **Utility Functions** | 70%+ | Commonly reused code |
| **UI Components** | 60%+ | Focus on logic, not markup |
| **Overall Project** | 70-80% | Balanced coverage |

### What NOT to Test

- Simple getters/setters
- Framework-generated code
- Third-party libraries
- Configuration files
- Trivial pass-through functions

## Coverage Tools

### TypeScript/JavaScript

**Vitest Coverage** (recommended):
```bash
npm install -D @vitest/coverage-v8
vitest --coverage
```

**Configuration**:
```typescript
// vitest.config.ts
export default {
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'json'],
      include: ['src/**/*.ts'],
      exclude: ['**/*.test.ts', '**/*.spec.ts'],
      lines: 70,
      functions: 70,
      branches: 70,
      statements: 70
    }
  }
}
```

### Python

**pytest-cov**:
```bash
pip install pytest-cov
pytest --cov=src --cov-report=html --cov-report=term
```

**Configuration (.coveragerc)**:
```ini
[run]
omit = */tests/*, */migrations/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

### Go

**Built-in coverage**:
```bash
go test -cover ./...
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

### Rust

**cargo-tarpaulin**:
```bash
cargo install cargo-tarpaulin
cargo tarpaulin --out Html
```

## Mutation Testing

### What Is Mutation Testing?

Mutation testing validates test quality by introducing bugs (mutations) and checking if tests catch them.

**Example**:
```typescript
// Original code
function add(a, b) {
  return a + b
}

// Mutation 1: Change + to -
function add(a, b) {
  return a - b  // If tests still pass, they're weak!
}

// Mutation 2: Change return value
function add(a, b) {
  return 0  // If tests still pass, they're weak!
}
```

### Mutation Testing Tools

**TypeScript/JavaScript: Stryker Mutator**:
```bash
npm install -D @stryker-mutator/core @stryker-mutator/vitest-runner
npx stryker run
```

**Python: mutmut**:
```bash
pip install mutmut
mutmut run
```

**Rust: cargo-mutants**:
```bash
cargo install cargo-mutants
cargo mutants
```

### When to Use Mutation Testing

✅ **Use mutation testing for**:
- High-criticality code (payment, auth)
- Core business logic
- Validating test suite quality

❌ **Skip mutation testing for**:
- Simple CRUD operations
- UI components (slow, low value)
- Integration tests (too slow)

## Beyond Line Coverage

### Branch Coverage

Ensure all conditional branches are tested:

```typescript
function getUserStatus(age: number) {
  if (age < 18) {
    return 'minor'
  } else {
    return 'adult'
  }
}

// Need tests for BOTH branches:
test('returns minor for age < 18', () => {
  expect(getUserStatus(15)).toBe('minor')
})

test('returns adult for age >= 18', () => {
  expect(getUserStatus(25)).toBe('adult')
})
```

### Function Coverage

Ensure all functions are called at least once.

### Statement Coverage

Ensure all statements are executed.

## CI/CD Integration

### Enforce Coverage Thresholds

**GitHub Actions**:
```yaml
- name: Run tests with coverage
  run: npm run test:coverage

- name: Check coverage threshold
  run: |
    COVERAGE=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
    if (( $(echo "$COVERAGE < 70" | bc -l) )); then
      echo "Coverage $COVERAGE% is below 70%"
      exit 1
    fi
```

### Track Coverage Trends

Use tools like Codecov or Coveralls to track coverage over time:
- Prevent coverage regressions
- Visualize coverage trends
- Comment coverage changes on PRs

## Summary

**Key Takeaways**:

1. **Don't chase 100% coverage**: Focus on meaningful coverage
2. **Risk-based targets**: Higher coverage for critical code
3. **Use mutation testing**: Validate test quality, not just coverage
4. **Enforce in CI/CD**: Prevent coverage regressions
5. **Track trends**: Monitor coverage over time

**Next Steps**:
- Set realistic coverage targets for your project
- Configure coverage tools in your test framework
- Consider mutation testing for critical paths
- Integrate coverage reporting into CI/CD
