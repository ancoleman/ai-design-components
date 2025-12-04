---
sidebar_position: 3
---

# Testing Strategies

Master plan for designing comprehensive testing strategies across the software development lifecycle. This skill covers test pyramid architecture, framework selection, test automation patterns, and quality assurance practices for modern applications.

**Status**: 🟢 Master Plan Available

## Key Topics

- **Test Pyramid**: Unit tests, integration tests, E2E tests, contract tests, balance and priorities
- **Test Automation**: CI/CD integration, test parallelization, flaky test management, test reporting
- **Framework Selection**: Language-specific frameworks, testing library ecosystems, migration strategies
- **API Testing**: REST API testing, GraphQL testing, contract testing, load testing
- **UI Testing**: Browser automation, visual regression, accessibility testing, mobile testing
- **Database Testing**: Test data management, fixtures, migrations testing, performance testing
- **Performance Testing**: Load testing, stress testing, spike testing, soak testing
- **Security Testing**: SAST, DAST, dependency scanning, penetration testing

## Primary Tools & Technologies

- **Unit Testing**: Jest, pytest, JUnit, Go testing, RSpec, Mocha
- **Integration Testing**: Testcontainers, Mockito, WireMock, Pact
- **E2E Testing**: Cypress, Playwright, Selenium, Puppeteer
- **API Testing**: Postman, Rest Assured, Supertest, Karate
- **Load Testing**: k6, Gatling, JMeter, Locust, Artillery
- **Visual Testing**: Percy, Chromatic, BackstopJS
- **Security Testing**: OWASP ZAP, Burp Suite, Snyk, Trivy
- **Test Management**: TestRail, Zephyr, Allure, ReportPortal

## Integration Points

- **Building CI/CD Pipelines**: Test execution in automated pipelines
- **Platform Engineering**: Standardized testing infrastructure
- **Incident Management**: Post-incident test creation
- **Kubernetes Operations**: Testing Kubernetes deployments
- **Observability**: Test result metrics and trends
- **Security Operations**: Security testing integration
- **Infrastructure as Code**: Infrastructure testing and validation

## Use Cases

- Designing test strategy for microservices architecture
- Implementing contract testing between services
- Setting up visual regression testing
- Creating load testing for API endpoints
- Building E2E test suites for web applications
- Implementing database migration testing
- Setting up automated security testing
- Managing test data and fixtures

## Decision Framework

**Test level selection:**
- **Unit tests (70%)**: Fast, isolated, developer-written, high coverage
- **Integration tests (20%)**: Service interactions, database queries, external APIs
- **E2E tests (10%)**: Critical user journeys, high-value workflows, smoke tests

**Framework selection based on:**
- Language ecosystem (native vs cross-language)
- Team expertise (learning curve vs familiarity)
- CI/CD integration (ease of automation)
- Test execution speed (parallelization support)
- Community support (documentation, plugins, maintenance)

**Automation priorities:**
- Critical business flows (highest priority)
- Regression-prone areas (high bug frequency)
- Time-consuming manual tests (biggest ROI)
- Stable features (low maintenance cost)

**Test data strategy:**
- **Static fixtures**: Predictable, version-controlled, fast setup
- **Generated data**: Randomized, edge cases, large datasets
- **Production-like**: Anonymized prod data, realistic scenarios
- **Synthetic**: AI-generated, diverse test cases

## Testing Anti-Patterns to Avoid

- Over-reliance on E2E tests (slow, fragile, expensive)
- Testing implementation details (brittle tests)
- No test isolation (shared state, dependencies)
- Ignoring flaky tests (erodes trust)
- Testing through UI only (missing unit/integration coverage)
- No performance testing until production (scalability issues)
