# Incident Communication Templates

## Overview

Communication templates for internal coordination and external customer updates during incidents. Customize for your organization while maintaining clarity and consistency.

---

## Internal Status Update Template (Slack)

**Use:** Post in incident Slack channel every 15-30 minutes during active incidents

```markdown
**[TIMESTAMP] Update #[N] - [Status]**

**Current Status:** [Investigating | Identified | Implementing Fix | Monitoring | Resolved]

**Issue:** [One-sentence description of what's broken]

**Impact:** [Who/what is affected, e.g., "~5,000 customers unable to complete checkout"]

**Progress:** [What we've learned/done since last update]

**Next Steps:** [What we're doing next]

**ETA:** [Expected resolution time or "Unknown - investigating"]

**Next Update:** [TIMESTAMP + 15/30 min]
```

**Example:**

```
14:45 PST Update #3 - Implementing Fix

Current Status: Implementing Fix

Issue: API experiencing elevated error rates (15% of requests failing)

Impact: ~5,000 customers unable to complete checkout

Progress: Root cause identified - database connection pool exhausted. Mitigation deployed: increased pool size from 100 to 200 connections. Error rate dropped from 15% to 5%.

Next Steps: Monitoring error rate trend. Investigating secondary issue with retry logic causing thundering herd.

ETA: Expect full resolution within 30 minutes

Next Update: 15:00 PST
```

---

## External Status Page Update Template

**Use:** Post to public status page (Statuspage.io, Instatus, etc.)

### Status: Investigating

```markdown
**[Timestamp] Investigating - [Component Name]**

We are investigating reports of [brief issue description]. Customers may experience [specific impact, e.g., "slow page loads" or "checkout errors"]. We are working to identify the root cause and will provide updates as we learn more.
```

**Example:**

```
Dec 3, 14:20 PST Investigating - API

We are investigating reports of elevated API error rates. Customers may experience errors when attempting to complete checkout. We are working to identify the root cause and will provide updates every 15 minutes.
```

---

### Status: Identified

```markdown
**[Timestamp] Identified - [Component Name]**

We have identified the issue: [brief technical description in plain language]. We are implementing a fix and expect resolution within [timeframe]. Customers are still experiencing [impact].
```

**Example:**

```
Dec 3, 14:30 PST Identified - API

We have identified the issue: our database connection pool reached capacity during higher-than-expected traffic. We are increasing the pool size and expect resolution within 30 minutes. Customers are still experiencing occasional checkout errors (~5% failure rate, down from 15%).
```

---

### Status: Monitoring

```markdown
**[Timestamp] Monitoring - [Component Name]**

The fix has been applied and [metric] has returned to normal levels. We are monitoring the situation to ensure stability before marking this incident as resolved.
```

**Example:**

```
Dec 3, 15:00 PST Monitoring - API

The fix has been applied and API error rates have returned to normal levels (<0.1%). We are monitoring the situation for the next 30 minutes to ensure stability before marking this incident as resolved.
```

---

### Status: Resolved

```markdown
**[Timestamp] Resolved - [Component Name]**

This incident has been resolved. [Component] is operating normally. Customers should no longer experience [impact]. We will be conducting a post-mortem to prevent recurrence and will share findings soon.
```

**Example:**

```
Dec 3, 15:45 PST Resolved - API

This incident has been resolved. The API is operating normally. Customers should no longer experience checkout errors. We will be conducting a post-mortem to prevent recurrence and will share a summary with affected customers within 24 hours.
```

---

## Customer Email Template (Post-Incident)

**Use:** Send to affected customers after SEV0/SEV1 incidents

**Timing:** Within 24 hours of resolution

**Subject Line:** `[Resolved] [Service Name] Incident on [Date]`

```markdown
Subject: [Resolved] API Outage on December 3, 2025

Dear [Customer Name / Customers],

We experienced a service disruption on [Date] from [Start Time] to [End Time] [Timezone]. During this time, [describe customer-facing impact in plain language].

**What Happened:**
[2-3 sentences explaining what broke in non-technical terms]

**Impact:**
- Duration: [X hours/minutes]
- Affected Users: [Approximately X customers or "All users"]
- Affected Functionality: [Specific features that were unavailable]
- Data: [Confirm no data loss or describe scope if any]

**How We Resolved It:**
[1-2 sentences describing the fix applied]

**What We're Doing to Prevent This:**
We take incidents seriously and are implementing the following improvements:
1. [Prevention measure 1]
2. [Prevention measure 2]
3. [Prevention measure 3]

**We Sincerely Apologize:**
We understand how disruptive service interruptions are and apologize for the inconvenience. If you have any questions or concerns, please contact our support team at [support email/phone].

Thank you for your patience and continued trust.

Sincerely,
[Name]
[Title]
[Company]
```

**Example:**

```
Subject: [Resolved] API Outage on December 3, 2025

Dear Customers,

We experienced an API outage on December 3, 2025, from 2:15 PM to 3:45 PM PST. During this time, approximately 5,000 customers were unable to complete checkout transactions.

What Happened:
Our database connection pool reached capacity during higher-than-expected holiday traffic. This caused our API to reject requests and display error messages during checkout.

Impact:
- Duration: 90 minutes (2:15 PM - 3:45 PM PST)
- Affected Users: Approximately 5,000 customers
- Affected Functionality: Checkout and payment processing
- Data: No customer data was lost or compromised

How We Resolved It:
We increased our database connection pool capacity and implemented circuit breaker logic to prevent similar cascading failures.

What We're Doing to Prevent This:
1. Adding proactive monitoring alerts for connection pool saturation (before errors occur)
2. Implementing load testing for 2x traffic scenarios before all releases
3. Auto-scaling our database connection pool to handle traffic spikes

We Sincerely Apologize:
We understand how frustrating this disruption was, especially during the holiday shopping season. We apologize for the inconvenience and appreciate your patience. If you have any questions, please contact support@example.com or call 1-800-XXX-XXXX.

Thank you for your continued trust.

Sincerely,
Jane Smith
VP Engineering
Example Company
```

---

## Executive Brief Template (Internal)

**Use:** Brief C-level stakeholders during/after SEV0 incidents

**Format:** Email or Slack DM

**Subject:** `Executive Brief: [Incident Title]`

```markdown
**Incident:** [One-line description]
**Status:** [Ongoing | Resolved]
**Severity:** [SEV0 | SEV1]
**Duration:** [X hours/minutes]

**Business Impact:**
- Customers Affected: [Number or percentage]
- Revenue Impact: [$ estimate or "Investigating"]
- SLA Breach: [Yes/No]
- PR/Media Risk: [High/Medium/Low]

**Current Status:**
[2-3 sentences on where we are in incident response]

**Root Cause:**
[If identified: brief explanation | If not: "Still investigating"]

**Resolution:**
[If ongoing: "Expected resolution: [timeframe]" | If resolved: "Resolved at [time]"]

**Customer Communication:**
[Status page updated? Customer email sent? Planned?]

**Next Steps:**
1. [Action 1]
2. [Action 2]
3. [Post-mortem scheduled for [date]]

**Contact:** [IC or Incident Manager name and Slack handle]
```

**Example:**

```
Executive Brief: API Outage - Dec 3, 2025

Incident: API error rates reached 15%, preventing checkout
Status: Resolved
Severity: SEV1
Duration: 90 minutes (2:15 PM - 3:45 PM PST)

Business Impact:
- Customers Affected: ~5,000 (15% of active users during incident)
- Revenue Impact: Estimated $12,000 in lost transactions
- SLA Breach: Yes - 99.9% monthly SLA now at 99.85%
- PR/Media Risk: Low - proactive customer communication sent

Root Cause:
Database connection pool exhausted during 2x traffic spike (holiday shopping). Contributing factors: no proactive monitoring, aggressive retry logic amplified impact.

Resolution:
Resolved at 3:45 PM PST. Connection pool size increased, circuit breaker implemented.

Customer Communication:
- Status page updated throughout (6 updates)
- Post-incident email sent to all affected customers
- Support team briefed on expected follow-up questions

Next Steps:
1. Add proactive connection pool monitoring (by Dec 10)
2. Load test all releases for 2x traffic (checklist updated)
3. Post-mortem scheduled for Dec 5 at 10am

Contact: @bob (IC) in #incident-2025-12-03-api-outage
```

---

## On-Call Handoff Template

**Use:** Weekly on-call rotation handoff (e.g., every Monday)

**Format:** Slack post in #on-call channel or shared Google Doc

```markdown
# On-Call Handoff - Week of [Date]

**Outgoing On-Call:** @[name]
**Incoming On-Call:** @[name]
**Handoff Date:** [Date and Time]

---

## Active Issues

### [Issue 1 Title]
- **Status:** [Monitoring | Investigating | Resolved]
- **Severity:** [SEV2/SEV3 typically for active issues]
- **Description:** [1-2 sentences]
- **Next Steps:** [What incoming on-call should do]
- **Resources:** [Link to ticket, dashboard, runbook]

### [Issue 2 Title]
[Same format as above]

**No Active Issues:** All systems normal ✅

---

## Upcoming Changes

### [Deploy/Maintenance 1]
- **Date/Time:** [When it's happening]
- **Impact:** [Expected customer impact or "No downtime expected"]
- **Risk Level:** [High/Medium/Low]
- **IC Assigned:** [Yes/No - who?]
- **Runbook:** [Link if applicable]

### [Deploy/Maintenance 2]
[Same format as above]

---

## New Runbooks / Updates

- **Added:** [Runbook name and link]
- **Updated:** [Runbook name and what changed]

**No Changes:** All runbooks current ✅

---

## System Health Notes

**Overall:** [Green/Yellow/Red - brief assessment]

- **[System 1]:** [Status and any notes]
- **[System 2]:** [Status and any notes]
- **[System 3]:** [Status and any notes]

**Monitoring Issues:**
- [Any dashboards down, alert issues, blind spots]

---

## Questions / Clarifications

**Q:** [Any questions from incoming on-call]
**A:** [Answers from outgoing on-call]

---

## Access Verification

- [ ] VPN connected
- [ ] PagerDuty app configured
- [ ] AWS/GCP console access verified
- [ ] Database access verified
- [ ] Monitoring dashboards accessible
- [ ] Slack notifications enabled

---

## Contact Info

**Outgoing On-Call:** @[handle] | [phone if needed]
**Incoming On-Call:** @[handle] | [phone if needed]
**Escalation:** @[team-lead-handle] | @[senior-oncall-handle]

**Handoff Complete:** ✅ [Timestamp when both parties confirm]
```

**Example:**

```markdown
# On-Call Handoff - Week of Dec 3-10, 2025

Outgoing On-Call: @alice
Incoming On-Call: @bob
Handoff Date: Monday, Dec 3, 10:00 AM PST

---

## Active Issues

### Database Replica Lag Spike
- Status: Monitoring
- Severity: SEV3
- Description: Replica lag spiking to 30 seconds every few hours, cause unknown. Primary unaffected.
- Next Steps: Monitor replica lag dashboard, escalate to @db-team if lag > 60 seconds
- Resources: https://monitoring.example.com/dashboard/db-replication

No other active issues. All systems normal ✅

---

## Upcoming Changes

### API Deploy v2.3.0
- Date/Time: Wednesday, Dec 5, 2:00 PM PST
- Impact: No downtime expected (rolling deploy)
- Risk Level: Medium (includes database migration)
- IC Assigned: Yes - @alice on standby
- Runbook: https://wiki.example.com/deploys/api-v2.3.0

### Database Maintenance Window
- Date/Time: Saturday, Dec 7, 2:00 AM PST
- Impact: Read-only mode for 30 minutes
- Risk Level: Low (routine maintenance)
- IC Assigned: No (automated)
- Runbook: RB-DB-003 (maintenance procedures)

---

## New Runbooks / Updates

- Updated: RB-DB-001 (Database Failover) - New DNS process added
- Added: RB-CACHE-001 (Redis Cache Invalidation) - New runbook for cache issues

---

## System Health Notes

Overall: Green (replica lag being monitored)

- API: Green - 99.99% uptime this week
- Database: Yellow - Replica lag spikes (under investigation)
- Cache: Green - All metrics normal
- CDN: Green - No issues

Monitoring Issues:
- None - all dashboards and alerts operational

---

## Questions / Clarifications

Q: What should I do if replica lag hits 60 seconds?
A: Page @db-team immediately. If they don't respond in 5 min, consider failing over to replica (use RB-DB-001).

Q: Is the v2.3.0 deploy high risk?
A: Medium risk due to DB migration. I'll be on Slack Wednesday afternoon as backup IC if needed.

---

## Access Verification

- [X] VPN connected
- [X] PagerDuty app configured
- [X] AWS console access verified
- [X] Database access verified
- [X] Monitoring dashboards accessible
- [X] Slack notifications enabled

---

## Contact Info

Outgoing On-Call: @alice | 555-0123 (cell)
Incoming On-Call: @bob | 555-0456 (cell)
Escalation: @team-lead | @senior-oncall

Handoff Complete: ✅ Dec 3, 10:15 AM PST
```

---

## Regulatory Notification Template

**Use:** Required for data breaches, security incidents (GDPR, HIPAA, PCI)

**Consult Legal Team Before Sending**

### GDPR Data Breach Notification (72-hour requirement)

```markdown
Subject: Data Breach Notification - [Company Name]

[Regulatory Authority Name]
[Address]

Date: [Date]

Re: Personal Data Breach Notification

Dear [Authority Name],

[Company Name] is writing to notify you of a personal data breach pursuant to Article 33 of the General Data Protection Regulation (GDPR).

1. Description of the Breach:
[Date and time breach discovered]
[Nature of the breach - unauthorized access, data loss, etc.]

2. Categories and Approximate Number of Data Subjects Concerned:
[E.g., "Approximately 5,000 EU residents"]

3. Categories and Approximate Number of Personal Data Records Concerned:
[E.g., "Names, email addresses, hashed passwords"]

4. Likely Consequences of the Breach:
[Describe potential impact on individuals]

5. Measures Taken to Address the Breach:
[Actions taken to stop breach and mitigate impact]

6. Measures Taken to Mitigate Adverse Effects:
[E.g., "Password reset required for all affected accounts"]

7. Contact Point:
[Name, title, email, phone of Data Protection Officer]

We will provide further information as our investigation progresses.

Sincerely,
[Name]
[Title]
[Company]
[Contact Information]
```

---

## Incident Closure Announcement

**Use:** Post in incident Slack channel when IC declares incident resolved

```markdown
**🎉 INCIDENT RESOLVED 🎉**

**Incident:** [Title]
**Duration:** [X hours/minutes]
**Resolved At:** [Timestamp]

**Summary:**
[1-2 sentences on what happened and how it was fixed]

**Final Metrics:**
- MTTA: [X minutes]
- MTTR: [X minutes]
- Customer Impact: [Brief summary]

**Next Steps:**
1. Post-mortem scheduled: [Date/Time]
2. Action items will be tracked in [Jira/GitHub/etc.]
3. Customer communication: [Sent/Scheduled]

**Thank You:**
Thank you to everyone who responded! Special thanks to:
- IC: @[name]
- SMEs: @[name1], @[name2]
- Communications: @[name]

**Post-Mortem Doc:** [Link to post-mortem draft]

---

This incident channel will remain open for 24 hours, then will be archived.
```

---

## Tips for Effective Communication

### Dos
✅ **Be Clear:** Use simple language, avoid jargon
✅ **Be Honest:** Don't over-promise on ETAs
✅ **Be Timely:** Update on schedule even if "no new information"
✅ **Be Empathetic:** Acknowledge customer frustration
✅ **Be Specific:** "15% error rate" vs. "some errors"

### Don'ts
❌ **Don't Speculate:** Stick to confirmed facts
❌ **Don't Blame:** External communication should never blame individuals or teams
❌ **Don't Over-Commit:** Avoid "This will never happen again"
❌ **Don't Ghost:** Even "no update" is an update
❌ **Don't Use Acronyms:** Customers don't know "SEV1" or "MTTR"

---

## Further Reading

- **Atlassian:** "How to Communicate During an Incident"
- **PagerDuty:** "Incident Communication Best Practices"
- **Statuspage.io:** "Writing Great Incident Updates"
