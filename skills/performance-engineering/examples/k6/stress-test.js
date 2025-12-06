/**
 * Stress Test Example (k6)
 *
 * Demonstrates: Finding breaking points and maximum capacity
 *
 * Usage:
 *   k6 run stress-test.js
 *
 * Scenario:
 *   - Ramp up to 100 users over 2 minutes
 *   - Sustain 100 users for 5 minutes
 *   - Ramp to 200 users over 2 minutes (stress)
 *   - Sustain 200 users for 5 minutes
 *   - Ramp to 300 users over 2 minutes (breaking point)
 *   - Sustain 300 users for 5 minutes
 *   - Ramp down to 0 over 2 minutes
 *
 * Goal: Identify at what load level error rate spikes (> 5%)
 */

import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 },   // Ramp to 100 users
    { duration: '5m', target: 100 },   // Stay at 100
    { duration: '2m', target: 200 },   // Ramp to 200
    { duration: '5m', target: 200 },   // Stay at 200
    { duration: '2m', target: 300 },   // Ramp to 300 (stress)
    { duration: '5m', target: 300 },   // Stay at 300
    { duration: '2m', target: 0 },     // Ramp down
  ],

  // Thresholds (allow some errors under stress)
  thresholds: {
    http_req_duration: ['p(99)<1000'],  // p99 < 1s
    http_req_failed: ['rate<0.05'],     // Error rate < 5% (lenient under stress)
  },
};

export default function () {
  // POST request (more resource-intensive than GET)
  const payload = JSON.stringify({
    product_id: Math.floor(Math.random() * 1000),
    quantity: Math.floor(Math.random() * 5) + 1,
  });

  const res = http.post('https://api.example.com/orders', payload, {
    headers: { 'Content-Type': 'application/json' },
  });

  check(res, {
    'order created': (r) => r.status === 201,
    'has order ID': (r) => JSON.parse(r.body).order_id !== undefined,
  });

  sleep(0.5);  // Shorter think time for higher stress
}
