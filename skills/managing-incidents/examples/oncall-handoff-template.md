# On-Call Handoff Template

## Overview

Structure weekly on-call handoffs to ensure smooth transition of responsibilities, context transfer, and continuity of operational awareness. Conduct handoff ceremony at consistent time (e.g., Monday 10am) with 30-minute dedicated meeting.

---

## Pre-Handoff Checklist

**Outgoing On-Call:**
- [ ] Review all incidents from past week
- [ ] Identify ongoing issues requiring attention
- [ ] Check monitoring for degraded services
- [ ] Review upcoming maintenance windows
- [ ] Prepare notes on known issues
- [ ] Update runbooks if needed

**Incoming On-Call:**
- [ ] Verify PagerDuty/Opsgenie account active
- [ ] Test alert delivery (phone, SMS, push)
- [ ] Review on-call procedures and escalation paths
- [ ] Have laptop and VPN ready
- [ ] Review recent incident post-mortems

---

## Handoff Meeting Template

### Meeting Details

**Date:** [YYYY-MM-DD]
**Outgoing On-Call:** [@outgoing-person]
**Incoming On-Call:** [@incoming-person]
**Duration:** 30 minutes
**Video Call:** [Zoom/Meet link]

---

## Section 1: Week in Review

### Incident Summary

**Total Incidents:** [N]

| Date | Severity | Duration | Issue | Status |
|------|----------|----------|-------|--------|
| Dec 1 | SEV1 | 45 min | API error spike | Resolved |
| Dec 2 | SEV2 | 2 hours | Cache degradation | Resolved |
| Dec 3 | SEV3 | 30 min | UI layout bug | Resolved |

**Key Incidents to Discuss:**

#### Incident 1: [Brief Title]
- **When:** [Date/Time]
- **Severity:** [SEV0/SEV1/SEV2/SEV3]
- **Impact:** [Customer/service impact]
- **Root Cause:** [Technical cause]
- **Resolution:** [How resolved]
- **Follow-Up Actions:** [Open action items]
- **Post-Mortem:** [Link to doc if applicable]

#### Incident 2: [Brief Title]
- **When:** [Date/Time]
- **Severity:** [SEV0/SEV1/SEV2/SEV3]
- **Impact:** [Customer/service impact]
- **Root Cause:** [Technical cause]
- **Resolution:** [How resolved]
- **Follow-Up Actions:** [Open action items]

---

## Section 2: Ongoing Issues

### Active Monitoring Items

**Issue 1: [Brief Description]**
- **Status:** [Monitoring | Under Investigation | Escalated]
- **Since:** [Date issue started]
- **Impact:** [Current impact, if any]
- **Context:** [Background information]
- **Next Steps:** [What to watch for or do]
- **Escalation:** [Who to contact if worsens]

**Example:**

```
Issue: Database Replication Lag Elevated

Status: Monitoring
Since: Nov 30, 2025
Impact: No customer impact, but lag 2-3 seconds vs normal 0.5s
Context: Traffic increased 20% due to holiday shopping. Replication keeping up but slower than usual. DBA team aware.
Next Steps: Monitor lag metric. Escalate if > 5 seconds or query errors appear.
Escalation: @db-sre-oncall
Alert: database-replication-lag-warning
Dashboard: https://monitoring.example.com/dashboard/database-health
```

---

### Known Issues (Non-Urgent)

**Issue 1: [Brief Description]**
- **Impact:** [Minor/cosmetic/low priority]
- **Ticket:** [JIRA-123]
- **Notes:** [Any context]

**Example:**

```
Issue: Slow Dashboard Load Times (EU Region)

Impact: Dashboards load in 3-5 seconds vs normal 1-2 seconds. Non-critical feature.
Ticket: PERF-456
Notes: Performance team investigating. No customer complaints. CDN optimization planned for Sprint 42.
```

---

## Section 3: Scheduled Maintenance

### Upcoming Maintenance Windows

**Maintenance 1: [Brief Description]**
- **When:** [Date/Time with timezone]
- **Duration:** [Expected duration]
- **Impact:** [Customer impact, if any]
- **Team Responsible:** [@team]
- **Your Role:** [What on-call needs to do]
- **Runbook:** [Link to maintenance procedure]

**Example:**

```
Maintenance: Database Upgrade (PostgreSQL 14 → 15)

When: Dec 7, 2025 02:00-04:00 PST (Sunday night)
Duration: 2 hours (max)
Impact: 5-minute read-only mode during cutover. No downtime expected.
Team Responsible: @db-sre-team
Your Role: Monitor alerts during window. Be available for escalation if issues occur.
Runbook: https://wiki.example.com/database-upgrade-procedure
Slack Channel: #maintenance-dec7-db-upgrade
Rollback Plan: Available in runbook (revert to snapshot if critical issues)
```

---

## Section 4: System Health Overview

### Service Status Dashboard

**Core Services:**
- **API:** ✅ Healthy (error rate < 0.1%, latency p99 < 200ms)
- **Database:** ⚠️ Monitoring (replication lag 2-3s, see "Ongoing Issues")
- **Cache (Redis):** ✅ Healthy (hit rate 94%)
- **Job Queue:** ✅ Healthy (processing rate normal)
- **CDN:** ✅ Healthy (cache hit rate 97%)

**Dashboard:** https://monitoring.example.com/dashboard/overview

---

### Recent Configuration Changes

**Change 1: [Description]**
- **When:** [Date/Time]
- **Who:** [@person]
- **What Changed:** [Brief description]
- **Monitoring:** [What to watch]

**Example:**

```
Change: Increased API Rate Limits for Enterprise Tier

When: Dec 2, 2025 14:00 PST
Who: @backend-team
What Changed: Increased rate limit from 1000 → 5000 req/min for enterprise customers
Monitoring: Watch API error rate and database connection pool utilization
Risk: Potential for database overload if multiple enterprise customers spike simultaneously
Rollback: Feature flag "enterprise_rate_limit_v2" can be disabled instantly
```

---

## Section 5: Key Contacts and Resources

### Escalation Paths

**By Service Area:**

| Service | Primary Contact | Secondary Contact | Escalation |
|---------|----------------|-------------------|------------|
| API | @backend-oncall | @backend-lead | @vp-engineering |
| Database | @db-sre-oncall | @senior-dba | @infrastructure-director |
| Frontend | @frontend-oncall | @frontend-lead | @vp-engineering |
| Infrastructure | @platform-oncall | @platform-lead | @infrastructure-director |

**Executive Escalation (SEV0 Only):**
- VP Engineering: @vp-eng (Slack + Phone: +1-555-0100)
- CTO: @cto (Phone: +1-555-0101)
- CEO: @ceo (Phone: +1-555-0102) - Only for business-critical SEV0

---

### Key Resources

**Runbooks:**
- Master Index: https://wiki.example.com/runbooks
- Database Failover: `runbooks/database-failover.md`
- Cache Invalidation: `runbooks/cache-invalidation.md`
- DDoS Mitigation: `runbooks/ddos-mitigation.md`

**Dashboards:**
- Overall Health: https://monitoring.example.com/dashboard/overview
- API Metrics: https://monitoring.example.com/dashboard/api
- Database Health: https://monitoring.example.com/dashboard/database
- Infrastructure: https://monitoring.example.com/dashboard/infra

**Documentation:**
- Incident Response Guide: https://wiki.example.com/incident-response
- Severity Classification: https://wiki.example.com/severity-levels
- On-Call Procedures: https://wiki.example.com/oncall-guide

**Slack Channels:**
- #incidents (automated incident creation)
- #oncall-general (on-call team coordination)
- #oncall-handoff (handoff notes archive)
- #database-operations (database team)
- #platform-engineering (infrastructure team)

---

## Section 6: Tips and Lessons Learned

### What Went Well This Week

**Example:**

```
- Quick response to API incident (MTTA 3 minutes, MTTR 45 minutes)
- Database team proactive about replication lag, no surprises
- Runbook for cache invalidation worked perfectly, no escalation needed
```

### Challenges and Learnings

**Example:**

```
- Alert fatigue: Received 12 non-actionable "warning" alerts for disk space that were false positives
  → Action: Opened ticket to adjust thresholds (INFRA-789)

- Cache invalidation runbook missing step for verifying propagation to all regions
  → Action: Updated runbook with verification step

- Unclear when to escalate for replication lag - waited longer than needed
  → Learning: Escalate to @db-sre-oncall if lag > 5 seconds, don't wait
```

### Advice for Incoming On-Call

**Example:**

```
- Keep an eye on database replication lag metric - it's been elevated all week
- EU region performance slower than usual, but no customer complaints yet
- Database maintenance Sunday night - be available 2am-4am PST
- New runbook for DDoS mitigation just added - review before your shift
- Coffee machine on floor 3 is broken, use floor 5 :)
```

---

## Section 7: Action Items

### Follow-Up from Last Week

- [ ] **[ITEM-1]** - [Description] - Owner: [@person] - Due: [Date]
- [ ] **[ITEM-2]** - [Description] - Owner: [@person] - Due: [Date]

**Example:**

```
- [x] Update cache-invalidation runbook with verification step - Owner: @alice - Due: Dec 4
- [ ] Adjust disk space alert thresholds to reduce false positives - Owner: @bob - Due: Dec 10
- [ ] Schedule disaster recovery drill for Q1 2026 - Owner: @oncall-lead - Due: Dec 15
```

---

### New Action Items from Handoff

- [ ] **[NEW-ITEM-1]** - [Description] - Owner: [@person] - Due: [Date]
- [ ] **[NEW-ITEM-2]** - [Description] - Owner: [@person] - Due: [Date]

---

## Section 8: Questions and Clarifications

**Incoming On-Call Questions:**

Q: [Question from incoming on-call]
A: [Answer from outgoing on-call]

**Example:**

```
Q: What's the typical response time for database team during off-hours?
A: Usually 5-10 minutes. They're very responsive. Use @db-sre-oncall in Slack first, escalate to phone if no response in 10 min.

Q: Is there a runbook for the replication lag issue?
A: Yes - RB-DB-003 (Database Replication Repair). But consult @db-sre-oncall before executing since they're already monitoring it.

Q: What's the threshold for escalating to VP Engineering?
A: SEV0 incidents lasting > 30 minutes, or any data breach/security incident, or if customer-facing impact is severe and we need executive communication.
```

---

## Post-Handoff Actions

**Outgoing On-Call:**
- [ ] Post handoff notes in #oncall-handoff Slack channel
- [ ] Update on-call schedule if any coverage gaps
- [ ] Archive handoff document in wiki: https://wiki.example.com/oncall-handoffs/YYYY-MM-DD
- [ ] Complete on-call feedback survey (if applicable)

**Incoming On-Call:**
- [ ] Acknowledge receipt of handoff
- [ ] Review all linked dashboards and runbooks
- [ ] Test alert delivery immediately after handoff
- [ ] Introduce yourself in #oncall-general Slack channel
- [ ] Review action items and clarify ownership

---

## Handoff Confirmation

**Outgoing On-Call Confirmation:**
```
I confirm that I have:
- Reviewed all incidents from the past week
- Briefed @[incoming] on ongoing issues
- Provided context on upcoming maintenance
- Shared key contacts and escalation paths
- Answered all questions to the best of my ability

Signed: [@outgoing-person], [Date]
```

**Incoming On-Call Confirmation:**
```
I confirm that I have:
- Reviewed all handoff materials
- Asked clarifying questions
- Tested alert delivery (PagerDuty/phone/SMS)
- Reviewed key dashboards and runbooks
- Understand escalation procedures

Ready to assume on-call responsibility.

Signed: [@incoming-person], [Date]
```

---

## Template Usage Notes

### Customization

**Adapt sections based on organization size:**
- **Small teams (< 10 engineers):** Focus on Sections 1-3, 5-6
- **Medium teams (10-50 engineers):** Use all sections
- **Large teams (50+ engineers):** Add service-specific handoffs

**Frequency:**
- **Weekly rotation:** Full handoff every week
- **Daily rotation:** Abbreviated handoff (Sections 1-2, 6 only)
- **Follow-the-sun:** Twice daily brief handoff (15 minutes)

---

### Handoff Best Practices

**Timing:**
- Schedule at consistent time (e.g., Monday 10am)
- Allow 30 minutes minimum
- No multitasking - give full attention

**Documentation:**
- Archive handoff notes for future reference
- Update runbooks based on learnings
- Track common issues for process improvement

**Communication:**
- Use video call, not just Slack
- Screen share dashboards and runbooks
- Encourage questions - no question is too basic

**Cultural:**
- Recognize outgoing on-call's efforts
- Share positive incidents (fast resolution, good teamwork)
- Acknowledge challenges without blame

---

## Related Templates

- **Incident Response:** `communication-templates.md`
- **Post-Mortem:** `postmortem-template.md`
- **Runbooks:** `runbooks/` directory

---

## Changelog

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-12-05 | 1.0 | Initial template | @incident-management-team |

---

## Contact

**Owner:** SRE Team
**Slack:** #oncall-general
**Documentation:** https://wiki.example.com/oncall-guide

**For template improvements:** Open PR or post in #sre-team
