# Contract Testing for Microservices

## Table of Contents

1. [Overview](#overview)
2. [Consumer-Driven Contracts](#consumer-driven-contracts)
3. [Pact Framework](#pact-framework)
4. [Implementation Examples](#implementation-examples)

## Overview

Contract testing validates service interfaces without requiring full end-to-end integration. This is critical for microservices architectures where services evolve independently.

### Why Contract Testing?

**Traditional Integration Testing Problems**:
- Requires all services running
- Slow feedback loops
- Brittle tests (multiple failure points)
- Hard to isolate issues

**Contract Testing Benefits**:
- Fast feedback (no full integration required)
- Independent service testing
- Clear interface contracts
- Prevents breaking changes

## Consumer-Driven Contracts

**Concept**: Consumers define expected contracts, providers verify they meet them.

**Workflow**:
1. Consumer writes contract test (expected request/response)
2. Contract published to Pact Broker
3. Provider verifies it can fulfill contract
4. Both services deploy independently

## Pact Framework

Pact is the industry-standard tool for consumer-driven contract testing.

**Supported Languages**: TypeScript, Python, Go, Rust, Java, .NET, Ruby

### TypeScript Consumer Example

```typescript
import { PactV3 } from '@pact-foundation/pact'

const provider = new PactV3({
  consumer: 'UserServiceClient',
  provider: 'UserService'
})

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
      body: {
        id: '123',
        name: string,
        email: string
      }
    })

  await provider.executeTest(async (mockServer) => {
    const user = await fetchUser('123', mockServer.url)
    expect(user.name).toBeDefined()
  })
})
```

### Python Provider Verification

```python
from pact import Verifier

verifier = Verifier(
    provider='UserService',
    provider_base_url='http://localhost:8000'
)

success = verifier.verify_pacts(
    './pacts/UserServiceClient-UserService.json',
    provider_states_setup_url='http://localhost:8000/_pact/provider_states'
)

assert success == 0
```

## Implementation Examples

For complete working examples, refer to:
- Pact official documentation: https://docs.pact.io
- Language-specific guides in the Pact repository

## Summary

Contract testing is essential for microservices:
- Faster than E2E tests
- Independent service development
- Clear interface contracts
- Prevents breaking changes

Use Pact for consumer-driven contract testing across all major languages.
