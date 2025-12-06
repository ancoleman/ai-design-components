/**
 * Basic Load Test Example (k6)
 *
 * Demonstrates: Baseline load testing to validate SLO compliance
 *
 * Usage:
 *   k6 run load-test.js
 *
 * Scenario:
 *   - Ramp up to 20 virtual users over 30 seconds
 *   - Sustain 20 users for 1 minute
 *   - Ramp down to 0 over 30 seconds
 *
 * SLO Targets:
 *   - p95 latency < 500ms
 *   - Error rate < 1%
 */

import http from 'k6/http';
import { check, sleep } from 'k6';

// Test configuration
export const options = {
  stages: [
    { duration: '30s', target: 20 },  // Ramp up to 20 users
    { duration: '1m', target: 20 },   // Stay at 20 users
    { duration: '30s', target: 0 },   // Ramp down to 0
  ],

  // Performance thresholds (SLOs)
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% of requests < 500ms
    http_req_failed: ['rate<0.01'],    // Error rate < 1%
    http_reqs: ['rate>10'],            // Throughput > 10 RPS
  },
};

// Virtual user scenario
export default function () {
  // GET request to API
  const res = http.get('https://api.example.com/products');

  // Validate response
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
    'response has products': (r) => JSON.parse(r.body).products !== undefined,
  });

  // Think time (simulate user reading response)
  sleep(1);
}
