# Alert Tuning Strategies

## Alert Lifecycle

1. **Detection Rule Created** - Conservative thresholds, deploy to production
2. **Baseline Period (2-4 weeks)** - Collect alert data, tag true/false positives
3. **Tuning Phase** - Add whitelisting, adjust thresholds, refine correlation
4. **Continuous Improvement** - Weekly metrics review, monthly effectiveness review

## Noise Reduction Techniques

### Whitelisting

```yaml
# Example: Allow scanner IPs
- rule_id: brute_force_detection
  whitelist:
    - source_ip: "10.0.0.100"  # Security scanner
    - user_agent: "Nagios"      # Monitoring system
```

### Threshold Tuning

```yaml
# Before: Too sensitive (500 alerts/day, 5% true positive rate)
- rule: failed_login_attempts
  threshold: 3 attempts in 5 minutes

# After: Tuned (50 alerts/day, 40% true positive rate)
- rule: failed_login_attempts
  threshold: 10 attempts in 10 minutes
```

### Multi-Event Correlation

```yaml
# Instead of: Single event alert
- alert_on: "Failed authentication"

# Use: Correlated pattern
- alert_on:
    - "Failed authentication (5+ times)"
    - AND "From new IP address"
    - AND "Successful authentication follows"
    - WITHIN: 30 minutes
```

## Target Alert Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Total Alerts/Day | <100 | 87 | ✅ |
| True Positive Rate | >30% | 42% | ✅ |
| Mean Time to Investigate | <15 min | 12 min | ✅ |
| False Positive Rate | <50% | 58% | ⚠️ Needs tuning |
| Critical Alerts/Day | <10 | 6 | ✅ |

## Summary

- **Baseline first** - Collect 2-4 weeks of data before tuning
- **Whitelist known-safe patterns** - Reduce noise from legitimate activity
- **Adjust thresholds** - Balance sensitivity vs. alert fatigue
- **Use correlation** - Multi-event patterns reduce false positives
- **Track metrics** - Monitor true positive rate, alert volume, investigation time
