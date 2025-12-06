# Test Type Selection Decision Tree

## Table of Contents

1. [Primary Decision Framework](#primary-decision-framework)
2. [Feature-Based Decision Making](#feature-based-decision-making)
3. [Architecture-Driven Decisions](#architecture-driven-decisions)
4. [Edge Case Scenarios](#edge-case-scenarios)
5. [Multi-Level Testing](#multi-level-testing)

## Primary Decision Framework

### The Core Decision Tree

```
START: Need to test [feature/function/component]

Q1: What am I testing?
  ├─ Pure function/business logic → Go to Q2
  ├─ API endpoint → Go to Q3
  ├─ Database operation → Go to Q4
  ├─ UI component → Go to Q5
  ├─ User workflow → Go to Q6
  └─ Service integration → Go to Q7

Q2: Pure Function/Business Logic
  ├─ Has simple inputs/outputs?
  │   └─ YES → Unit Test (vitest, pytest, testing)
  ├─ Has many edge cases?
  │   └─ YES → Unit Test + Property-Based Test (fast-check, hypothesis, proptest)
  └─ Complex algorithm?
      └─ YES → Unit Test + Snapshot Test

Q3: API Endpoint
  ├─ Simple CRUD operation?
  │   └─ YES → Integration Test (database + endpoint)
  ├─ Complex business logic?
  │   └─ YES → Unit Test (logic) + Integration Test (endpoint)
  ├─ External API calls?
  │   └─ YES → Integration Test with Mocked External API (MSW, pytest-httpserver)
  └─ Critical to user workflow?
      └─ YES → Integration Test + E2E Test

Q4: Database Operation
  ├─ Repository method (CRUD)?
  │   └─ YES → Integration Test (real test database)
  ├─ Complex query?
  │   └─ YES → Integration Test (validate query correctness)
  └─ Transaction handling?
      └─ YES → Integration Test (test rollback, commit)

Q5: UI Component
  ├─ Stateless presentation?
  │   └─ YES → Unit Test (rendering) or Snapshot Test
  ├─ Interactive with state?
  │   └─ YES → Integration Test (component + state management)
  ├─ Data fetching?
  │   └─ YES → Integration Test (component + API mocking)
  └─ Complex user interaction?
      └─ YES → E2E Test (user workflow)

Q6: User Workflow
  ├─ Critical path (login, checkout, payment)?
  │   └─ YES → E2E Test (full stack)
  ├─ Multi-step process?
  │   └─ YES → E2E Test for happy path + Integration Tests for edge cases
  └─ Cross-browser required?
      └─ YES → E2E Test with Playwright (multiple browsers)

Q7: Service Integration (Microservices)
  ├─ Service-to-service communication?
  │   └─ YES → Contract Test (Pact - consumer + provider)
  ├─ Message queue/event bus?
  │   └─ YES → Integration Test (publish + consume)
  └─ API gateway?
      └─ YES → Integration Test (routing + transformation)
```

## Feature-Based Decision Making

### Authentication Features

| Feature | Test Type | Tools | Rationale |
|---------|-----------|-------|-----------|
| Password hashing | Unit | Vitest, pytest | Pure function, deterministic |
| Token generation | Unit + Property-Based | fast-check, hypothesis | Many edge cases |
| Login endpoint | Integration | Supertest, FastAPI TestClient | Validates DB + auth logic |
| Login flow (UI) | E2E | Playwright | Critical user journey |
| OAuth callback | Integration | Mock OAuth provider | External dependency |
| Session validation | Unit | Standard test framework | Logic-only validation |

### E-Commerce Features

| Feature | Test Type | Tools | Rationale |
|---------|-----------|-------|-----------|
| Product price calculation | Unit | Vitest, pytest | Pure business logic |
| Add to cart | Integration | Component + state test | State management + UI |
| Checkout flow | E2E | Playwright | Critical revenue path |
| Payment processing | Integration + E2E | Mock payment API, full flow | Critical + external API |
| Order confirmation | Integration | Email mock, DB validation | Multiple system interaction |
| Inventory update | Integration | Real DB, transaction test | Data integrity critical |

### Data Processing Features

| Feature | Test Type | Tools | Rationale |
|---------|-----------|-------|-----------|
| Data transformation | Unit + Property-Based | fast-check, hypothesis | Complex logic, edge cases |
| File parsing | Unit + Snapshot | Standard test framework | Consistent output |
| Data validation | Unit + Property-Based | Validation-specific | Many input variations |
| Batch processing | Integration | Real DB, test data | DB interaction, performance |
| API data fetch | Integration | MSW, pytest-httpserver | External dependency |
| Report generation | Integration + Snapshot | DB + output capture | Complex query + formatting |

## Architecture-Driven Decisions

### Monolithic Application

**Testing Strategy**:
- **70% Unit Tests**: Business logic, utilities, helpers
- **20% Integration Tests**: API endpoints, database operations
- **10% E2E Tests**: Critical user journeys

**Decision Factors**:
- Single deployment unit → More integration tests acceptable
- Shared database → Integration tests validate data consistency
- Tightly coupled components → E2E tests for critical paths

**Example**:
```
Rails/Django Monolith:
- Unit: Model methods, service objects, helpers
- Integration: Controller/view actions, database queries
- E2E: User signup, checkout, admin workflows
```

### Microservices Architecture

**Testing Strategy**:
- **60% Unit Tests**: Service-specific logic
- **30% Integration/Contract Tests**: Service boundaries, API contracts
- **10% E2E Tests**: User-facing workflows only

**Decision Factors**:
- Distributed services → Contract tests essential
- Service boundaries → Integration tests for each service
- Avoid E2E test explosion → Focus on critical user journeys

**Example**:
```
Microservices E-Commerce:
- Unit: Product service logic, pricing calculations
- Contract: Product service → Cart service interface
- Integration: Each service's API endpoints
- E2E: Checkout flow (crosses all services)
```

### Serverless/Cloud Functions

**Testing Strategy**:
- **70% Unit Tests**: Function logic (handler + business logic)
- **25% Integration Tests**: Cloud service integration (S3, DynamoDB)
- **5% E2E Tests**: Complete workflows (rare, expensive)

**Decision Factors**:
- Stateless functions → Unit test handler logic
- Cloud service dependencies → Integration tests with emulators
- Event-driven → Integration tests for event handling

**Example**:
```
AWS Lambda Functions:
- Unit: Handler logic, data transformation
- Integration: DynamoDB operations (use LocalStack/DynamoDB Local)
- E2E: Complete user action (API Gateway → Lambda → DynamoDB)
```

### Frontend Single-Page Application (SPA)

**Testing Strategy**:
- **50% Unit Tests**: Utility functions, hooks, pure logic
- **40% Integration Tests**: Component + state + data fetching
- **10% E2E Tests**: Critical user flows

**Decision Factors**:
- Component-based → Integration tests more valuable than unit
- State management → Integration tests validate state transitions
- User interactions → E2E for complete workflows

**Example**:
```
React/Vue SPA:
- Unit: Hooks, utilities, formatters
- Integration: Component with Redux/Vuex, API mocking (MSW)
- E2E: Login → Dashboard → User action
```

## Edge Case Scenarios

### Complex Business Rules

**Scenario**: Tax calculation with multiple jurisdictions, exemptions, special rates

**Recommended Approach**:
1. **Unit Tests**: Core calculation logic with fixtures
2. **Property-Based Tests**: Generate random scenarios to find edge cases
3. **Integration Tests**: Full tax calculation API endpoint with database

**Example**:
```typescript
// Unit test: Known scenarios
test('calculates California sales tax', () => {
  expect(calculateTax(100, 'CA')).toBe(107.25)
})

// Property-based: Edge cases
fc.assert(
  fc.property(fc.float(), fc.string(), (amount, state) => {
    const tax = calculateTax(amount, state)
    return tax >= amount // Tax never reduces price
  })
)

// Integration: Full endpoint
test('POST /calculate-tax returns correct tax', async () => {
  const response = await request(app)
    .post('/calculate-tax')
    .send({ amount: 100, state: 'CA', items: [...] })
  expect(response.body.totalTax).toBe(7.25)
})
```

### External API Integration

**Scenario**: Payment processing via Stripe, shipping via FedEx API

**Recommended Approach**:
1. **Unit Tests**: API client logic (request formatting, response parsing)
2. **Integration Tests**: Mock external API (MSW, VCR.py)
3. **E2E Tests**: Sandbox environment (Stripe test mode)

**Example**:
```python
# Unit test: Request formatting
def test_stripe_charge_request_format():
    request = build_stripe_charge_request(amount=1000, currency='usd')
    assert request['amount'] == 1000
    assert request['currency'] == 'usd'

# Integration test: Mock Stripe API
@pytest.fixture
def mock_stripe(httpserver):
    httpserver.expect_request('/v1/charges').respond_with_json({
        'id': 'ch_test123',
        'status': 'succeeded'
    })
    return httpserver

def test_charge_customer(mock_stripe):
    charge = stripe_service.charge_customer(1000, 'usd', 'tok_visa')
    assert charge['status'] == 'succeeded'

# E2E test: Stripe test mode
def test_checkout_flow_with_payment(page):
    page.goto('/checkout')
    page.fill('[data-testid="card-number"]', '4242424242424242')
    page.click('[data-testid="submit-payment"]')
    expect(page.locator('[data-testid="order-confirmation"]')).to_be_visible()
```

### Real-Time Features

**Scenario**: WebSocket chat, live dashboards, collaborative editing

**Recommended Approach**:
1. **Unit Tests**: Message parsing, state updates
2. **Integration Tests**: WebSocket connection, message handling
3. **E2E Tests**: Multi-client interaction (if critical)

**Example**:
```typescript
// Unit test: Message parsing
test('parses chat message', () => {
  const parsed = parseMessage('{"type": "chat", "text": "Hello"}')
  expect(parsed.type).toBe('chat')
  expect(parsed.text).toBe('Hello')
})

// Integration test: WebSocket handling
test('handles incoming message', async () => {
  const ws = new WebSocket('ws://localhost:3000')
  ws.send(JSON.stringify({ type: 'chat', text: 'Hi' }))
  const response = await waitForMessage(ws)
  expect(response.type).toBe('chat')
})

// E2E test: Multi-client chat
test('messages appear across clients', async ({ browser }) => {
  const page1 = await browser.newPage()
  const page2 = await browser.newPage()

  await page1.goto('/chat')
  await page2.goto('/chat')

  await page1.fill('[data-testid="message-input"]', 'Hello from user 1')
  await page1.click('[data-testid="send-button"]')

  await expect(page2.locator('text=Hello from user 1')).toBeVisible()
})
```

### Background Jobs/Workers

**Scenario**: Email sending, report generation, data synchronization

**Recommended Approach**:
1. **Unit Tests**: Job logic (data preparation, validation)
2. **Integration Tests**: Job execution with real queue (Redis, RabbitMQ)
3. **E2E Tests**: Trigger job, verify outcome (if user-visible)

**Example**:
```python
# Unit test: Job logic
def test_prepare_email_data():
    data = prepare_email_data(user_id=123)
    assert data['to'] == 'user@example.com'
    assert 'subject' in data

# Integration test: Job execution
def test_send_email_job(redis_queue):
    job = send_email_job.delay(user_id=123)
    job.wait(timeout=5)
    assert job.status == 'SUCCESS'
    assert job.result['sent'] is True

# E2E test: User trigger + outcome
def test_user_receives_confirmation_email(page, email_client):
    page.goto('/signup')
    page.fill('[name="email"]', 'test@example.com')
    page.click('[type="submit"]')

    # Wait for background job
    email = email_client.wait_for_email('test@example.com', timeout=10)
    assert 'Welcome' in email.subject
```

## Multi-Level Testing

### When to Test at Multiple Levels

Some features benefit from testing at multiple levels for comprehensive coverage.

**Example: Password Validation**

```typescript
// Level 1: Unit Test (validation logic)
describe('validatePassword', () => {
  test('rejects passwords shorter than 8 characters', () => {
    expect(validatePassword('short')).toBe(false)
  })

  test('requires at least one number', () => {
    expect(validatePassword('noNumbers')).toBe(false)
    expect(validatePassword('hasNumber1')).toBe(true)
  })
})

// Level 2: Integration Test (API endpoint)
describe('POST /signup', () => {
  test('returns 400 for weak password', async () => {
    const response = await request(app)
      .post('/signup')
      .send({ email: 'test@example.com', password: 'weak' })
    expect(response.status).toBe(400)
    expect(response.body.error).toContain('password')
  })
})

// Level 3: E2E Test (user workflow)
test('signup form shows password requirements', async ({ page }) => {
  await page.goto('/signup')
  await page.fill('[name="password"]', 'weak')
  await page.click('[type="submit"]')

  await expect(page.locator('.error')).toContainText('at least 8 characters')
})
```

**Rationale**:
- **Unit test**: Validates core logic quickly (many edge cases)
- **Integration test**: Validates API contract and error responses
- **E2E test**: Validates user experience and error messaging

**Trade-off**: More comprehensive coverage vs. test suite complexity. Use multi-level testing for:
- Critical features (authentication, payment)
- Complex business rules (tax calculation, pricing)
- User-facing validation (forms, input requirements)

## Summary

**Key Decision Factors**:

1. **Scope of test**: Single function → Unit, Multiple components → Integration, Full workflow → E2E
2. **Dependencies**: None → Unit, Database/API → Integration, Full stack → E2E
3. **Criticality**: High → Multi-level testing, Medium → Integration + Unit, Low → Unit only
4. **Architecture**: Monolith → More integration, Microservices → More contract, SPA → More component integration

**Quick Reference Table**:

| What | Dependencies | Critical? | Test Type |
|------|--------------|-----------|-----------|
| Pure function | None | Any | Unit |
| API endpoint | Database | Yes | Integration + E2E |
| API endpoint | Database | No | Integration |
| UI component | State management | No | Integration |
| User workflow | Full stack | Yes | E2E |
| Service interface | Other services | Yes | Contract + Integration |

**Next Steps**:
- Use this decision tree when planning tests for new features
- Review existing tests and identify misplaced test types
- Refactor tests to appropriate levels for better speed/confidence balance
