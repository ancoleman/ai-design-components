# RTO/RPO Planning Guide

## Table of Contents

1. [Defining Recovery Objectives](#defining-recovery-objectives)
2. [Business Impact Analysis](#business-impact-analysis)
3. [Criticality Tier Classification](#criticality-tier-classification)
4. [Cost-Benefit Analysis](#cost-benefit-analysis)
5. [RTO/RPO Calculation Examples](#rtorpo-calculation-examples)

## Defining Recovery Objectives

### Recovery Time Objective (RTO)

**Definition:** Maximum tolerable duration that a system can be down after a failure or disaster occurs.

**Measurement:** Time from disaster declaration to full service restoration.

**Factors to Consider:**
- Business impact of downtime (revenue loss, customer impact)
- Regulatory requirements
- Customer SLA commitments
- Seasonal/time-of-day variations
- Cascading dependencies

**Example RTO Definitions:**
- E-commerce checkout: 15 minutes (high revenue impact)
- Customer-facing website: 1 hour (brand reputation)
- Internal CRM: 4 hours (operational impact)
- Analytics database: 24 hours (low immediate impact)

### Recovery Point Objective (RPO)

**Definition:** Maximum tolerable amount of data loss measured in time.

**Measurement:** Time between last recoverable backup and disaster occurrence.

**Factors to Consider:**
- Transaction volume and frequency
- Data criticality and compliance requirements
- Cost of recreating lost data
- Data interdependencies
- Regulatory data retention requirements

**Example RPO Definitions:**
- Financial transactions: 0 seconds (zero data loss tolerance)
- User profiles: 5 minutes (recent changes acceptable loss)
- Application logs: 1 hour (can be reconstructed)
- Static content: 24 hours (infrequent changes)

## Business Impact Analysis

### Impact Assessment Framework

**Step 1: Identify Critical Business Functions**

List all business processes and rank by impact of failure:
- Revenue generation (sales, transactions)
- Customer service (support, communication)
- Operations (order fulfillment, delivery)
- Internal functions (HR, finance)

**Step 2: Quantify Downtime Impact**

Calculate cost of downtime per hour for each function:
```
Downtime Cost = (Revenue Loss + Productivity Loss + Recovery Cost + Reputation Impact)
```

**Example Calculation:**
- Revenue: $10,000/hour in lost sales
- Productivity: 50 employees × $50/hour = $2,500/hour
- Recovery: Overtime labor, emergency vendor costs
- Reputation: Customer churn, brand damage (harder to quantify)

**Total:** $15,000+/hour minimum quantifiable impact

**Step 3: Define Acceptable Risk**

Balance cost of downtime against cost of DR solution:
- RTO too aggressive: Over-investment in DR infrastructure
- RTO too lenient: Business impact exceeds DR cost

**Break-Even Analysis:**
```
Annual DR Cost ≤ (Probability of Disaster × Downtime Cost × Hours Saved)
```

## Criticality Tier Classification

### Tier 0: Mission-Critical

**Characteristics:**
- Business cannot operate without this system
- High revenue impact (> $10,000/hour)
- Customer-facing transactional systems
- Regulatory/compliance requirements

**Requirements:**
- RTO: < 1 hour
- RPO: < 5 minutes
- Availability: 99.99%+ (< 52 min downtime/year)

**DR Strategy:**
- Active-Active multi-region deployment
- Continuous replication (synchronous or near-synchronous)
- Automated failover
- Continuous backup with PITR

**Examples:**
- Payment processing systems
- Trading platforms
- Emergency service dispatch
- Healthcare patient systems

### Tier 1: Production

**Characteristics:**
- Important to business operations
- Moderate revenue impact ($1,000-$10,000/hour)
- Core application functionality
- Customer-impacting but not transactional

**Requirements:**
- RTO: 1-4 hours
- RPO: 15-60 minutes
- Availability: 99.9% (< 8.7 hours downtime/year)

**DR Strategy:**
- Active-Passive with warm standby
- Asynchronous replication
- Semi-automated failover
- Incremental backups with WAL archiving

**Examples:**
- CRM systems
- Inventory management
- Customer support portals
- Product catalogs

### Tier 2: Important

**Characteristics:**
- Supports business operations
- Low revenue impact (< $1,000/hour)
- Internal tools and systems
- Short-term workarounds available

**Requirements:**
- RTO: 4-24 hours
- RPO: 1-6 hours
- Availability: 99.5% (< 44 hours downtime/year)

**DR Strategy:**
- Pilot Light or cold standby
- Daily incremental backups
- Manual or semi-automated failover
- Cross-region backup storage

**Examples:**
- Internal wikis and documentation
- Project management tools
- Employee directories
- Non-critical reporting

### Tier 3: Standard

**Characteristics:**
- Nice to have, minimal business impact
- No direct revenue impact
- Long-term workarounds available
- Low usage frequency

**Requirements:**
- RTO: > 24 hours
- RPO: > 6 hours
- Availability: 99% (< 87 hours downtime/year)

**DR Strategy:**
- Backup and restore only
- Weekly full + daily incremental
- Manual recovery procedures
- Single region backup

**Examples:**
- Development environments
- Test systems
- Archived data
- Internal tools with low adoption

## Cost-Benefit Analysis

### DR Strategy Cost Comparison

| Strategy | Setup Cost | Monthly Cost | RTO | RPO | Best For |
|----------|-----------|-------------|-----|-----|----------|
| **Active-Active** | $$$$$ | $$$$$ | < 1 min | < 1 min | Tier 0 |
| **Warm Standby** | $$$$ | $$$$ | 10-60 min | 5-15 min | Tier 1 |
| **Pilot Light** | $$$ | $$$ | 15-60 min | 15-60 min | Tier 1-2 |
| **Backup/Restore** | $$ | $$ | 4-24 hours | 1-6 hours | Tier 2-3 |
| **Minimal** | $ | $ | > 24 hours | > 24 hours | Tier 3 |

### ROI Calculation

**Formula:**
```
Annual DR Cost Justification = Expected Annual Loss Without DR - DR Infrastructure Cost

Where:
Expected Annual Loss = (Probability of Disaster) × (Downtime Cost per Hour) × (Hours of Downtime)
```

**Example Scenario:**

System: Production API (Tier 1)
- Downtime cost: $5,000/hour
- Historical disaster probability: 2% per year (based on incident logs)
- Expected downtime without DR: 48 hours
- Expected downtime with DR: 2 hours

**Without DR:**
Expected Annual Loss = 0.02 × $5,000/hour × 48 hours = $4,800

**With DR (Warm Standby):**
- DR Infrastructure Cost: $2,000/month = $24,000/year
- Expected Annual Loss: 0.02 × $5,000/hour × 2 hours = $200
- Net Cost: $24,000 + $200 = $24,200

**ROI Decision:**
In this case, DR cost ($24,200) exceeds expected loss without DR ($4,800). Options:
1. Accept risk and implement cheaper backup strategy (RPO relaxed to 6 hours, cost $6,000/year)
2. Revisit disaster probability assumptions (2% may be low)
3. Quantify additional intangible costs (reputation, customer churn)

## RTO/RPO Calculation Examples

### Example 1: E-commerce Platform

**Business Context:**
- Peak revenue: $50,000/hour
- Off-peak revenue: $10,000/hour
- Customer base: 100,000 active users
- Average transaction value: $85

**Impact Analysis:**
- 1 hour downtime during peak: $50,000 + reputation damage
- Probability of disaster: 3% per year (historical)
- Expected annual loss: 0.03 × $50,000 × 24 hours = $36,000

**RTO/RPO Requirements:**
- RTO: 15 minutes (minimize revenue loss)
- RPO: 1 minute (zero transaction loss tolerance)

**Selected Strategy:**
- Active-Active across two regions
- Aurora Global Database (cross-region replication)
- Application deployed in both regions
- Global load balancer with health checks
- Annual cost: $60,000

**Justification:**
Expected loss without DR: $36,000 (direct) + $100,000+ (reputation, churn)
DR cost: $60,000
Net benefit: Positive, plus improved customer confidence

### Example 2: Internal HR System

**Business Context:**
- 500 employees
- Used for payroll, time tracking, benefits
- Payroll runs twice monthly
- Average employee cost: $75/hour

**Impact Analysis:**
- Downtime impact: 500 employees × $75/hour × (productivity loss)
- Critical during payroll: 2 days/month
- Non-critical otherwise

**RTO/RPO Requirements:**
- RTO: 4 hours (acceptable manual workarounds)
- RPO: 24 hours (daily changes acceptable)

**Selected Strategy:**
- Daily full backups to S3
- Cross-region backup replication
- Manual restore procedure
- Annual cost: $3,600

**Justification:**
Expected loss: Low (manual workarounds available)
DR cost: $3,600 (minimal)
Net benefit: Insurance against data loss

### Example 3: Real-Time Analytics Pipeline

**Business Context:**
- Processes 10M events/hour
- Drives real-time product recommendations
- Revenue impact: 5% conversion rate improvement = $5,000/hour

**Impact Analysis:**
- Downtime: Degrades to batch recommendations (2% conversion)
- Revenue impact: 3% × average order value
- Data loss: Can be replayed from event log

**RTO/RPO Requirements:**
- RTO: 1 hour (acceptable temporary degradation)
- RPO: 15 minutes (event replay from Kafka)

**Selected Strategy:**
- Kubernetes with Velero daily backups
- Kafka topic retention: 7 days
- Multi-AZ deployment (not multi-region)
- Annual cost: $18,000

**Justification:**
Expected loss: $5,000/hour × 2 hours × 0.03 probability = $300/year
DR cost: $18,000
Trade-off: Over-investment for pure DR, but enables other benefits (easy cluster migration, testing)

## Testing RTO/RPO Compliance

### Validation Procedures

**RTO Testing:**
1. Declare simulated disaster (in non-production)
2. Start timer
3. Execute failover procedures
4. Verify application health
5. Stop timer when service fully restored
6. Compare actual vs target RTO

**RPO Testing:**
1. Note timestamp of last transaction before disaster
2. Restore from backup
3. Query most recent data in restored system
4. Calculate time gap between disaster and last recovered data
5. Compare actual vs target RPO

**Frequency:**
- Tier 0: Monthly DR drills
- Tier 1: Quarterly DR drills
- Tier 2: Semi-annual DR drills
- Tier 3: Annual validation

### Metrics to Track

**Key Performance Indicators:**
- Actual RTO vs Target RTO
- Actual RPO vs Target RPO
- Failover success rate
- Data integrity post-restore
- Manual vs automated steps
- Mean time to detect (MTTD)
- Mean time to respond (MTTR)

**Continuous Improvement:**
- Identify bottlenecks in recovery procedures
- Automate manual steps
- Update runbooks based on drill findings
- Adjust RTO/RPO based on business changes
