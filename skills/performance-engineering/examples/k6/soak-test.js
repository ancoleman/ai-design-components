/**
 * Soak Test Example (k6)
 *
 * Demonstrates: Long-duration stability testing to detect memory leaks
 *
 * Usage:
 *   k6 run soak-test.js
 *
 * Scenario:
 *   - Ramp up to 50 users over 5 minutes
 *   - Sustain 50 users for 24 hours
 *   - Ramp down to 0 over 5 minutes
 *
 * Monitoring:
 *   - Watch memory usage trends (should be stable)
 *   - Check connection pool usage (should not grow)
 *   - Monitor response time degradation
 *
 * NOTE: Run during off-hours to avoid impacting production
 */

import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '5m', target: 50 },    // Ramp up to 50 users
    { duration: '24h', target: 50 },   // Sustain for 24 hours
    { duration: '5m', target: 0 },     // Ramp down
  ],

  // Thresholds (should remain stable throughout)
  thresholds: {
    http_req_duration: ['p(95)<300'],  // p95 should stay < 300ms
    http_req_failed: ['rate<0.001'],   // Very low error rate (< 0.1%)
  },
};

export default function () {
  // Simulate realistic user session
  const endpoints = [
    '/api/products',
    '/api/products/123',
    '/api/cart',
    '/api/user/profile',
  ];

  // Random endpoint selection (varied load)
  const endpoint = endpoints[Math.floor(Math.random() * endpoints.length)];
  const res = http.get(`https://api.example.com${endpoint}`);

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time stable': (r) => r.timings.duration < 300,
  });

  // Realistic think time
  sleep(Math.random() * 3 + 2);  // 2-5 seconds
}
