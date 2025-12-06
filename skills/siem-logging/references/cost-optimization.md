# Cost Optimization

## Storage Tiering

### Cost Comparison (1 TB storage, 1 year)

| Storage Tier | AWS Cost | Azure Cost | Use Case |
|--------------|----------|------------|----------|
| **Hot (Elasticsearch)** | ~$1,200/year | ~$1,100/year | Real-time analysis |
| **Warm (S3 Standard)** | ~$276/year | ~$230/year | Occasional queries |
| **Cold (S3 Glacier)** | ~$48/year | ~$24/year | Compliance archive |

### Tiering Strategy

```
Real-time logs (7 days) → Hot (Elasticsearch)
Recent logs (30 days) → Warm (S3 Standard)
Archive (1 year) → Cold (Glacier Deep Archive)
Delete after 1 year (GDPR compliance)
```

## Data Volume Reduction

### Log Sampling

```yaml
# Fluentd: Keep 10% of info-level logs
<filter application.info>
  @type sampling
  interval 10
  sample_rate 1
</filter>
```

### Selective Field Retention

```ruby
# Logstash: Remove sensitive/unnecessary fields
filter {
  mutate {
    remove_field => ["headers", "cookies", "query_params"]
  }
}
```

## Example Cost Optimization

```
500 GB/day log volume, 1-year retention

Hot (30 days):   15 TB @ $0.10/GB = $1,500/month
Warm (60 days):  30 TB @ $0.05/GB = $1,500/month
Cold (275 days): 137.5 TB @ $0.01/GB = $1,375/month

Total: $4,375/month = $52,500/year

vs. Hot-only: $18,250/month = $219,000/year
Savings: 76% ($166,500/year)
```

## Summary

- **Use tiering** - Save 70-80% with hot/warm/cold strategy
- **Sample non-critical logs** - Reduce volume 50-90%
- **Strip unnecessary fields** - Reduce storage 20-30%
- **Implement ILM** - Automate lifecycle management
