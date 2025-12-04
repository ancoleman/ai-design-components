# Incident Management Skill - Master Plan

**Skill Name:** `incident-management`
**Skill Level:** Mid Level (500-800 lines, 4,000-6,000 tokens)
**Status:** Planning Phase (init.md complete, SKILL.md to be created)
**Last Updated:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [Component Taxonomy](#component-taxonomy)
5. [Decision Frameworks](#decision-frameworks)
6. [Implementation Patterns](#implementation-patterns)
7. [Tool Recommendations](#tool-recommendations)
8. [Skill Structure Design](#skill-structure-design)
9. [Integration Points](#integration-points)
10. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why Incident Management Matters in 2025

Incident management has evolved from reactive firefighting to proactive, culturally-embedded operational excellence. Modern organizations recognize that incidents are inevitable—the differentiator is how quickly and effectively teams respond, communicate, and learn.

**Market Drivers:**

- **Zero Tolerance for Downtime:** Customer expectations demand rapid detection and resolution
- **SRE Culture Adoption:** Google's SRE principles have become industry standard
- **Distributed Systems Complexity:** Microservices, multi-cloud, and serverless architectures increase incident surface area
- **Blameless Post-Mortem Movement:** Focus shifted from "who" to "why" and "how to prevent"
- **Automation & AI:** Incident response platforms now offer automated escalation, intelligent routing, and AI-assisted diagnosis

**Strategic Value:**

1. **Reliability Foundation:** Incident management is the operational backbone of high-availability systems
2. **Customer Trust:** Fast, transparent incident response builds confidence
3. **Learning Culture:** Blameless post-mortems turn failures into organizational knowledge
4. [**MTTR Reduction:** Structured processes reduce Mean Time To Recovery from hours to minutes
5. **Team Well-Being:** Proper on-call rotation prevents burnout and improves retention

### How This Differs from Existing Solutions

**Existing Incident Management Documentation:**
- **Tool-Specific:** PagerDuty docs OR Opsgenie docs, not unified principles
- **Reactive Focus:** "How to page someone" vs "How to design on-call culture"
- **Limited Post-Mortem Guidance:** Assumes teams know how to conduct blameless reviews
- **Fragmented Communication:** Status pages, runbooks, escalation treated separately

**Our Approach:**
- **Culture + Process + Tools:** SRE principles first, tools second
- **Decision Framework:** Severity classification, escalation matrices, communication templates
- **Blameless Culture:** Post-mortem templates and facilitation guidance
- **End-to-End Coverage:** Detection → Response → Communication → Learning
- **Multi-Tool Support:** Principles work across PagerDuty, Opsgenie, incident.io, FireHydrant

---

## Skill Purpose and Scope

### What This Skill Teaches

**Core Competencies:**

1. **Incident Detection and Alerting**
   - Alert design principles (actionable, not noisy)
   - Alert routing and aggregation
   - Integration with monitoring systems
   - Alert fatigue prevention

2. **On-Call Management**
   - On-call rotation design (follow-the-sun, tiered)
   - Escalation policies and backup contacts
   - On-call handoff procedures
   - Compensation and burnout prevention

3. **Incident Command Structure**
   - Incident Commander (IC) role and responsibilities
   - Communications Lead role
   - Subject Matter Expert (SME) coordination
   - ICS (Incident Command System) adaptation for tech

4. **Severity Classification**
   - SEV0/P0 (Critical): Complete service outage
   - SEV1/P1 (High): Major functionality degraded
   - SEV2/P2 (Medium): Minor functionality impaired
   - SEV3/P3 (Low): Cosmetic or non-critical issues
   - Impact vs. urgency matrices

5. **Communication Protocols**
   - Internal: War rooms, Slack channels, status updates
   - External: Customer status pages, email notifications
   - Stakeholder management (executives, product, support)
   - Regulatory notifications (data breaches, compliance)

6. **Incident Response Workflows**
   - Incident declaration (early and often)
   - Initial triage and severity assignment
   - Mitigation first, root cause later
   - Escalation triggers and thresholds
   - Incident closure criteria

7. **Runbooks and Playbooks**
   - Runbook structure and templates
   - Common failure scenarios (database failover, DDoS, API degradation)
   - Automated runbook execution
   - Runbook maintenance and versioning

8. **Post-Incident Review (Blameless Post-Mortems)**
   - Blameless culture principles
   - Timeline reconstruction
   - Root cause analysis (5 Whys, Fishbone diagrams)
   - Action items with owners and due dates
   - Knowledge base integration

9. **Metrics and Continuous Improvement**
   - MTTA (Mean Time To Acknowledge)
   - MTTR (Mean Time To Recovery)
   - MTBF (Mean Time Between Failures)
   - Incident frequency trends
   - Action item completion rates

### What This Skill Does NOT Cover

- **Monitoring and observability setup** → Use `observability`, `prometheus-grafana` skills
- **Infrastructure automation** → Use `infrastructure-as-code` skill
- **Disaster recovery planning** → Use `disaster-recovery` skill
- **Security incident response** → Use `security-incident-response` skill
- **Change management processes** → Use `deployment-strategies` skill

**Integration:** This skill focuses on operational incident response. It integrates with monitoring, infrastructure, and security skills for complete coverage.

---

## Research Findings

### Google Search Grounding Results (December 2025)

#### Query 1: Incident Management Best Practices 2025

**Key Findings:**

**Core Best Practices:**

1. **Incident Response Plan:** Develop and maintain a comprehensive, regularly updated plan
2. **Early Detection:** Prioritize continuous monitoring with AI-driven analytics and behavior-based threat detection
3. **Clear Roles:** Establish specific responsibilities for incident management team
4. **Strategic Communication:**
   - Dedicated coordination channels (Slack, MS Teams)
   - Stakeholder updates every 15-30 minutes during active incidents
   - Post-incident communication to affected users
5. **Automation:** Use ITSM tools to automate repetitive processes
6. **Real-Time Documentation:** Record all actions, decisions, and learnings during incidents
7. **Continuous Training:** Workshops, tabletop exercises, real-world simulations
8. **Blameless Post-Mortems:** Foster environment that reduces anxiety, encourages collaboration
9. **Incident Declaration:** Declare incidents early and often—don't wait for certainty
10. **Mitigation First:** Focus on stopping the bleeding before diagnosing root cause

**Modern Incident Management Focus:**

- **Incident Management Platforms:** Automate declaration, role assignment, communication, documentation, postmortem processes
- **Integration:** Connect monitoring, ITSM, ChatOps tools for seamless workflow
- **Knowledge Base:** Maintain comprehensive runbook library
- **Alert Aggregation:** Define meaningful thresholds to reduce noise
- **Escalation Paths:** Clear backup contacts for each role

**Sources:**
- cyble.com
- purplesec.us
- medium.com
- rootly.com
- alertops.com

#### Query 2: SRE Incident Response Tools Comparison

**Key Tool Categories:**

1. **On-Call and Incident Management:**
   - **PagerDuty:** Leading platform, automates on-call schedules and escalation, AIOps features for event correlation and noise reduction
   - **Incident.io:** Full-stack incident management, AI-powered autonomous investigation
   - **Opsgenie:** Atlassian product, customizable workflows, advanced on-call scheduling
   - **Zenduty:** Real-time detection, automated alerting and escalation
   - **Splunk On-Call (VictorOps):** Centralized on-call scheduling and collaboration

2. **Monitoring/Observability Integration:**
   - Prometheus, Datadog, Grafana integration critical
   - Centralized alert routing

3. **Communication Platforms:**
   - Slack, Microsoft Teams for real-time collaboration
   - ChatOps integration for incident response

**Key Tool Selection Criteria:**

- **Integration:** Works with existing monitoring and communication tools
- **Automation:** Reduces manual escalation and routing
- **Real-time Insights:** Visibility into incident status
- **Scalability:** Handles complex multi-team organizations
- **AI Features:** Intelligent event correlation, noise reduction, automated remediation
- **Cost:** Balance open-source and commercial solutions

**Sources:**
- signoz.io
- port.io
- instatus.com
- squareops.com
- zenduty.com

### Web Search Results: Blameless Post-Mortem Templates

**Key Template Findings:**

**Blameless Culture Principles:**
- **No Finger-Pointing:** Everyone did their best with available information
- **Focus on Facts:** Reconstruct timeline and data before concluding
- **Ask "Why" Five Times:** Dig to systemic or process-level causes
- **System Focus:** How did the process fail, not who failed

**Template Structure:**

1. **Incident Summary:** Plain-language description of what happened
2. **Timeline:** Chronological record from detection to full recovery
3. **Root Cause Analysis:**
   - Primary root cause (main trigger/failure point)
   - Contributing factors (conditions that worsened impact)
4. **Impact Assessment:**
   - Customer impact (users affected, downtime duration)
   - Revenue impact
   - SLA violations
5. **What Went Well:** Positive actions during incident response
6. **What Went Wrong:** Areas for improvement (process, not people)
7. **Action Items:**
   - Clear, actionable takeaways
   - Assigned owners with due dates
   - Follow-up tracking

**Available Template Resources:**
- **Miro:** Blameless Post-Mortem Canvas template
- **GitHub (dastergon/postmortem-templates):** Collection from SRE book, Cloud System Administration
- **Smartsheet:** Free template for recording post-mortem results
- **ilert:** Google Docs template
- **Google SRE Book:** Authoritative guide to postmortem culture

**Best Practices:**
- Involve right stakeholders (engineers, ops, business teams)
- Use data and logs for objective timeline reconstruction
- Assign clear action items with owners and deadlines
- Foster psychological safety for honest discussion

**Sources:**
- [FREE Blameless Postmortem Canvas Template | Miro 2025](https://miro.com/templates/blameless-postmortem-canvas/)
- [Ultimate Post-Mortem Template: Free Downloads](https://uptimerobot.com/knowledge-hub/monitoring/ultimate-post-mortem-templates/)
- [GitHub - postmortem-templates](https://github.com/dastergon/postmortem-templates)
- [Google SRE - Blameless Postmortem](https://sre.google/sre-book/postmortem-culture/)
- [Atlassian - How to run a blameless postmortem](https://www.atlassian.com/incident-management/postmortem/blameless)

### Context7 Research: PagerDuty

**Available Resources:**

1. **Terraform Provider for PagerDuty** (`/pagerduty/terraform-provider-pagerduty`)
   - Code Snippets: 976
   - Source Reputation: High
   - Use Case: Infrastructure-as-code for PagerDuty configuration

2. **PagerDuty API Reference** (`/websites/developer_pagerduty_api-reference`)
   - Code Snippets: 208
   - Source Reputation: High
   - Benchmark Score: 35.2
   - Comprehensive endpoints for incident management automation

**PagerDuty Capabilities:**
- On-call schedule management
- Escalation policy automation
- Incident creation and management
- Integration with 700+ monitoring tools
- Real-time notifications
- AIOps for intelligent alert grouping

### Context7 Research: Incident.io

**Finding:** No direct incident.io library in Context7, but **IncidentHub** found:

**IncidentHub** (`/llmstxt/incidenthub_cloud-llms.txt`)
- Code Snippets: 348
- Source Reputation: High
- Description: Aggregates public status pages of Cloud/SaaS services, provides real-time alerts for incidents and maintenance

**Note:** Incident.io is newer (launched ~2020s) and may not have extensive API documentation yet in Context7.

---

## Component Taxonomy

### 1. Incident Detection and Alerting

**Alert Design Principles:**
- **Actionable:** Every alert requires immediate human action
- **Context-Rich:** Include runbook links, graphs, recent changes
- **Deduplicated:** Group related alerts to prevent noise
- **Routed:** Send to appropriate team/person based on service ownership

**Alert Types:**
- **Threshold Alerts:** CPU > 90%, error rate > 1%
- **Anomaly Detection:** ML-based deviation from baseline
- **Synthetic Monitoring:** Proactive health checks
- **Customer-Reported:** Support tickets, social media

**Anti-Patterns:**
- Alert fatigue from noisy, non-actionable alerts
- No clear ownership of alert
- Missing context for responders
- Alerts without runbooks

### 2. On-Call Management

**Rotation Patterns:**

1. **Follow-the-Sun (24/7 coverage):**
   - Team A: US hours (9am-5pm PT)
   - Team B: Europe hours (9am-5pm CET)
   - Team C: Asia hours (9am-5pm IST/SGT)
   - Benefit: No night shifts, improved work-life balance

2. **Tiered Escalation:**
   - Tier 1: Junior on-call (common issues, runbook-driven)
   - Tier 2: Senior on-call (complex troubleshooting)
   - Tier 3: Team lead / architect (critical decisions)
   - Escalation after: 15 minutes no ack, 30 minutes no resolution

3. **Primary + Secondary:**
   - Primary on-call: First responder
   - Secondary on-call: Backup if primary doesn't ack in 5 min
   - Reduces single point of failure

**Best Practices:**
- **Rotation Length:** 1 week (not too short, not too long)
- **Handoff Ceremony:** 30-min call to discuss active issues, upcoming changes
- **Compensation:** On-call stipend + time off after incidents
- **Tooling:** PagerDuty, Opsgenie for schedule management
- **Limits:** Max 2-3 pages per night, escalate if exceeded

### 3. Incident Command Structure

**Roles (Adapted from ICS - Incident Command System):**

1. **Incident Commander (IC):**
   - **Responsibilities:**
     - Owns overall incident response
     - Delegates tasks to responders
     - Makes strategic decisions (rollback vs. debug)
     - Calls incident resolved
   - **Skills:** Leadership, decision-making under pressure, communication
   - **NOT:** Hands-on keyboard debugging (delegates to SMEs)

2. **Communications Lead:**
   - **Responsibilities:**
     - Posts status updates (internal Slack, external status page)
     - Coordinates with stakeholders (execs, product, support)
     - Drafts post-incident customer communication
   - **Skills:** Clear writing, empathy, stakeholder management
   - **Cadence:** Update every 15-30 minutes during SEV0/SEV1

3. **Subject Matter Experts (SMEs):**
   - **Responsibilities:**
     - Hands-on debugging and mitigation
     - Execute runbooks
     - Provide technical context to IC
   - **Skills:** Deep technical knowledge of affected systems

4. **Scribe:**
   - **Responsibilities:**
     - Documents timeline, actions taken, decisions made
     - Real-time incident notes for post-mortem
   - **Tools:** Shared Google Doc, incident management platform

**When to Assign Roles:**
- **SEV2/SEV3:** Single responder (no formal structure)
- **SEV1:** IC + SME(s)
- **SEV0:** IC + Communications Lead + SME(s) + Scribe

### 4. Severity Classification

**Standard Severity Levels:**

| Severity | Impact | Examples | Response Time | Escalation |
|----------|--------|----------|---------------|------------|
| **SEV0 (P0)** | Complete outage, critical data loss | API down, database unavailable, payment processing broken | Page immediately, 24/7 | All hands on deck, executive notification |
| **SEV1 (P1)** | Major functionality degraded | Slow response times, partial feature unavailable | Page during business hours, escalate off-hours | Team lead, IC assigned |
| **SEV2 (P2)** | Minor functionality impaired | Edge case bug, non-critical feature broken | Email/Slack alert, next business day | Standard on-call response |
| **SEV3 (P3)** | Cosmetic or low-impact issues | UI glitch, typo, minor performance degradation | Ticket queue, planned sprint | No immediate response |

**Impact vs. Urgency Matrix:**

```
         High Impact │ Low Impact
        ─────────────┼─────────────
High     SEV0/SEV1   │   SEV2
Urgency  (page now)  │ (alert, respond business hours)
        ─────────────┼─────────────
Low      SEV1/SEV2   │   SEV3
Urgency  (plan fix)  │ (backlog)
```

**Decision Criteria:**
- **SEV0:** Production completely down, revenue-generating functions broken, critical security breach
- **SEV1:** Significant customer impact, workaround exists, performance severely degraded
- **SEV2:** Small subset of customers affected, minor degradation
- **SEV3:** Internal-only impact, cosmetic issues

### 5. Communication Protocols

**Internal Communication:**

1. **Incident Slack Channel:**
   - Format: `#incident-2025-12-03-api-outage`
   - Purpose: Central coordination, real-time updates
   - Participants: IC, SMEs, Communications Lead, stakeholders

2. **War Room (Video Call):**
   - When: SEV0/SEV1 incidents
   - Platform: Zoom, Google Meet, Slack Huddle
   - Purpose: Real-time voice coordination

3. **Status Update Cadence:**
   - SEV0: Every 15 minutes
   - SEV1: Every 30 minutes
   - SEV2: Every 1-2 hours or at major milestones

**External Communication:**

1. **Status Page:**
   - Tools: Statuspage.io, Instatus, custom page
   - Updates: Investigating → Identified → Monitoring → Resolved
   - Transparency: Acknowledge issue publicly, provide ETAs

2. **Customer Email:**
   - When: SEV0/SEV1 affecting customers
   - Timing: Within 1 hour of incident start (acknowledge), post-resolution (full details)
   - Tone: Apologetic, transparent, action-oriented

3. **Regulatory Notifications:**
   - Data Breach: GDPR requires notification within 72 hours
   - Financial Services: Immediate notification to regulators
   - Healthcare: HIPAA breach notification rules

**Communication Templates:**

**Status Update Template:**
```
[TIMESTAMP] Update #3 - Investigating

Issue: API experiencing elevated error rates (15% of requests failing)
Impact: ~5,000 customers unable to complete checkout
Current Status: Team identified database connection pool exhaustion, applying fix
ETA: Expect resolution within 30 minutes
Next Update: [TIMESTAMP + 15 min]
```

**Post-Incident Email Template:**
```
Subject: [Resolved] API Outage on Dec 3, 2025

Dear Customers,

We experienced an API outage on December 3, 2025, from 2:15 PM to 3:45 PM PST.
During this time, approximately 5,000 customers were unable to complete checkout.

What Happened:
Our database connection pool reached capacity due to a misconfigured retry policy...

Impact:
- Duration: 90 minutes
- Affected Users: ~5,000
- Data Loss: None

Resolution:
We increased connection pool size and fixed the retry configuration...

Prevention:
We're implementing the following changes:
1. Enhanced monitoring for connection pool metrics
2. Load testing for retry scenarios
3. Automated circuit breakers

We sincerely apologize for the disruption. If you have questions, contact support@...

[Team Name]
```

### 6. Incident Response Workflow

**Standard Incident Lifecycle:**

```
1. Detection
   ↓
2. Triage & Severity Assignment
   ↓
3. Incident Declaration (create channel, assign IC)
   ↓
4. Investigation & Diagnosis
   ↓
5. Mitigation (stop the bleeding)
   ↓
6. Resolution (fix root cause)
   ↓
7. Monitoring (ensure stability)
   ↓
8. Closure (IC confirms resolved)
   ↓
9. Post-Mortem (within 48 hours)
```

**Key Decision Points:**

- **Declare Early:** When in doubt, declare incident (can always downgrade severity)
- **Mitigation vs. Diagnosis:** Stop customer impact first (rollback, disable feature), debug later
- **Escalation Triggers:**
  - No progress after 30 minutes
  - Severity increases (SEV2 → SEV1)
  - Expertise needed (specialized system knowledge)
- **Closure Criteria:**
  - Issue resolved and stable for 30+ minutes
  - Monitoring shows normal metrics
  - IC confirms no further customer impact

### 7. Runbooks and Playbooks

**Runbook Structure:**

```markdown
# Runbook: Database Failover

## Trigger
- Primary database unreachable
- Alert: "PostgreSQL Primary Down"

## Severity
SEV1 (Major functionality degraded until failover complete)

## Prerequisites
- Replication lag < 5 seconds
- Secondary database healthy

## Steps
1. Verify primary is truly down (not network blip)
   - Check: `pg_isready -h primary-db.example.com`
2. Check replication status
   - Run: `SELECT * FROM pg_stat_replication;` on secondary
3. Promote secondary to primary
   - Command: `pg_ctl promote -D /var/lib/postgresql/data`
4. Update DNS/load balancer to point to new primary
   - Terraform: `terraform apply -target=aws_route53_record.db_primary`
5. Verify application connectivity
   - Check error rates in Datadog
6. Update runbook if steps changed

## Rollback
- If promotion fails, revert DNS change
- Investigate replication lag before retry

## Owner
Database SRE team (@db-sre-team)

## Last Updated
2025-12-01
```

**Common Runbook Categories:**
- Database failover (PostgreSQL, MySQL, MongoDB)
- Cache invalidation (Redis, Memcached)
- Service restart (graceful vs. force)
- Traffic shifting (canary rollback, feature flag disable)
- DDoS mitigation (rate limiting, WAF rules)
- Certificate renewal (TLS/SSL)
- Disk space cleanup

**Runbook Best Practices:**
- **Executable:** Commands copy-pasteable, not just descriptions
- **Tested:** Run during DR drills to verify accuracy
- **Versioned:** Track changes in Git
- **Linked:** Reference from alert definitions
- **Automated:** Convert manual steps to scripts over time

### 8. Post-Incident Review (Blameless Post-Mortems)

**Blameless Culture Tenets:**

1. **Assume Good Intentions:** Everyone made the best decision with available information
2. **Focus on Systems:** How did processes fail, not who failed
3. **Psychological Safety:** Honesty without fear of punishment
4. **Learning Opportunity:** Incidents are gifts of organizational knowledge

**Post-Mortem Process:**

1. **Schedule Review (Within 48 Hours):**
   - While memory is fresh
   - Attendees: IC, SMEs, stakeholders, optional: leadership

2. **Pre-Work:**
   - Timeline reconstruction from incident notes
   - Gather logs, metrics, screenshots
   - Draft initial post-mortem document

3. **Meeting Facilitation:**
   - **Facilitator (not IC):** Keeps discussion blameless, on-track
   - **Timeline Walkthrough:** Chronological review of events
   - **5 Whys Analysis:** Dig to root causes
   - **What Went Well:** Celebrate effective responses
   - **What Went Wrong:** Identify improvement areas
   - **Action Items:** Specific, assigned, with due dates

4. **Post-Mortem Document:**
   - **Template Sections:**
     - Incident Summary
     - Timeline
     - Root Cause(s)
     - Impact Assessment (customers, revenue, SLA)
     - What Went Well
     - What Went Wrong
     - Action Items (owner, due date, status)
   - **Distribution:** Share with engineering, product, support, leadership
   - **Knowledge Base:** Store in searchable wiki/docs

5. **Follow-Up:**
   - Track action item completion
   - Review in sprint planning
   - Celebrate completion

**Post-Mortem Template:**

```markdown
# Post-Mortem: API Outage - December 3, 2025

**Incident ID:** INC-2025-1203-001
**Severity:** SEV1
**Duration:** 90 minutes (2:15 PM - 3:45 PM PST)
**Author:** [Name]
**Attendees:** [List]

## Summary
On December 3, 2025, our API experienced elevated error rates (15% failure rate)
due to database connection pool exhaustion. Approximately 5,000 customers were
unable to complete checkout during the incident.

## Timeline (All times PST)

| Time | Event |
|------|-------|
| 14:15 | First alert: "API Error Rate High" |
| 14:17 | On-call engineer acknowledged, began investigation |
| 14:20 | Incident declared as SEV1, IC assigned |
| 14:25 | Root cause identified: DB connection pool saturated |
| 14:30 | Mitigation: Increased connection pool size from 100 → 200 |
| 14:35 | Error rate dropped to 5% |
| 14:45 | Identified secondary issue: retry logic causing thundering herd |
| 14:50 | Disabled aggressive retry, enabled circuit breaker |
| 15:00 | Error rate returned to baseline (<0.1%) |
| 15:00-15:45 | Monitoring for stability |
| 15:45 | IC declared incident resolved |

## Root Cause Analysis

**Primary Cause:**
Database connection pool size (100 connections) was insufficient for peak traffic load
(doubled due to holiday shopping).

**Contributing Factors:**
1. Aggressive retry logic caused "thundering herd" when DB slowed
2. No alerting on connection pool saturation (only on errors)
3. Recent code deploy increased DB query frequency by 20%

**Why (5 Whys):**
1. Why did API fail? → DB connection pool exhausted
2. Why was pool exhausted? → Traffic doubled, pool size unchanged
3. Why didn't we anticipate? → No load testing for 2x traffic
4. Why no load testing? → Not in release checklist
5. Why not in checklist? → Process gap

## Impact Assessment

- **Customers Affected:** ~5,000 (15% of active users during incident)
- **Revenue Impact:** Estimated $12,000 in lost transactions
- **SLA Violation:** 99.9% monthly SLA breached (now at 99.85%)
- **Support Tickets:** 47 tickets filed during incident

## What Went Well

- Fast detection (2 minutes from issue start to alert)
- Clear IC assignment and role delegation
- Effective communication (status updates every 15 min)
- Quick mitigation (connection pool increase)
- No data loss or corruption

## What Went Wrong

- No proactive monitoring of connection pool metrics
- Retry logic not tested under DB degradation
- Recent deploy not load tested for 2x traffic
- Post-incident communication delayed by 30 minutes

## Action Items

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| Add connection pool saturation alerts | @alice | 2025-12-10 | In Progress |
| Implement circuit breaker library | @bob | 2025-12-15 | Not Started |
| Add "load test for 2x traffic" to release checklist | @charlie | 2025-12-05 | Complete |
| Create runbook for DB connection pool tuning | @alice | 2025-12-12 | Not Started |
| Post-incident email to affected customers | @comms | 2025-12-04 | Complete |

## Lessons Learned

1. Connection pool metrics are critical leading indicators
2. Retry logic needs circuit breakers to prevent cascading failures
3. Load testing should include traffic spike scenarios
4. Proactive monitoring > reactive alerting
```

### 9. Metrics and Continuous Improvement

**Key Incident Metrics:**

1. **MTTA (Mean Time To Acknowledge):**
   - Definition: Time from alert to human acknowledgment
   - Target: < 5 minutes for SEV1, < 15 minutes for SEV2
   - Improvement: Better on-call coverage, clearer escalation

2. **MTTR (Mean Time To Recovery):**
   - Definition: Time from detection to full resolution
   - Target: < 1 hour for SEV1, < 4 hours for SEV2
   - Improvement: Runbooks, automation, expertise distribution

3. **MTBF (Mean Time Between Failures):**
   - Definition: Average time between incidents for a service
   - Target: > 30 days for critical services
   - Improvement: Root cause fixes, preventive measures

4. **Incident Frequency:**
   - Track: SEV0, SEV1, SEV2 counts per week/month
   - Target: Downward trend over time
   - Improvement: Action item completion, systemic fixes

5. **Action Item Completion Rate:**
   - Definition: % of post-mortem action items completed on time
   - Target: > 90%
   - Improvement: Sprint integration, ownership clarity

**Continuous Improvement Loop:**

```
Incident → Post-Mortem → Action Items → Prevention
   ↑                                          ↓
   └──────────── Fewer Incidents ─────────────┘
```

**Quarterly Reviews:**
- Trend analysis: Are incidents decreasing?
- Common patterns: Which services have most incidents?
- Action item effectiveness: Did fixes prevent recurrence?
- Training needs: Knowledge gaps identified?

---

## Decision Frameworks

### Framework 1: Severity Classification Decision Tree

```
Is production completely down or critical data at risk?
├─ YES → SEV0 (Page all hands immediately)
└─ NO  → Is major functionality degraded?
          ├─ YES → Is there a workaround?
          │        ├─ YES → SEV1 (Page on-call, assign IC)
          │        └─ NO  → SEV0 (No workaround = critical)
          └─ NO  → Are customers impacted?
                   ├─ YES → SEV2 (Alert on-call, standard response)
                   └─ NO  → SEV3 (Create ticket, backlog)
```

### Framework 2: Escalation Decision Matrix

```
Time Since Incident Start | No Progress | Severity Increase | Expertise Needed
─────────────────────────────────────────────────────────────────────────────
< 15 minutes              | Primary      | -                 | -
15-30 minutes             | Secondary    | SEV2 → SEV1       | Specialist
30+ minutes               | Team Lead    | SEV1 → SEV0       | Architect
60+ minutes               | Director     | -                 | VP Engineering
```

### Framework 3: Mitigation vs. Root Cause Decision

**When to Prioritize Mitigation (Stop the Bleeding):**
- Active customer impact ongoing
- Revenue loss accumulating
- Incident duration < 30 minutes (quick fix available)
- Rollback or disable feature is low-risk

**When to Prioritize Root Cause Investigation:**
- Customer impact already mitigated (workaround in place)
- Fix requires careful analysis (database corruption, security)
- Incident duration > 1 hour (already deep in debugging)
- Risk of making it worse with blind fixes

**Default: Mitigation First (99% of cases)**

### Framework 4: On-Call Rotation Selection

```
Team Size | Follow-the-Sun | Tiered | Primary+Secondary
────────────────────────────────────────────────────────
< 5       | ❌             | ❌     | ✅ (1-week rotation)
5-15      | ❌             | ✅     | ✅ (1-week rotation)
15-50     | ✅             | ✅     | ✅ (1-week rotation)
50+       | ✅             | ✅     | ✅ (3-4 day rotation)

Global Team: Follow-the-Sun preferred
Single Timezone: Primary+Secondary sufficient
Complex Systems: Tiered escalation (L1 → L2 → L3)
```

---

## Implementation Patterns

### Pattern 1: Incident Declaration Automation

**Goal:** Reduce friction to declare incidents (declare early and often).

**Implementation:**

```yaml
# Slack Slash Command: /incident-declare
Trigger: /incident-declare SEV1 API down
Actions:
  1. Create incident Slack channel: #incident-2025-12-03-api-down
  2. Post template message:
     - Severity: SEV1
     - Commander: [auto-assign based on on-call]
     - Status: Investigating
  3. Create PagerDuty incident
  4. Post status page update: "Investigating API issues"
  5. Start incident timer
  6. Invite on-call team to channel
```

**Tools:**
- Slack Workflow Builder
- PagerDuty API
- Statuspage.io API
- Custom bot (incident.io, Rootly, FireHydrant)

### Pattern 2: Automated Status Updates

**Goal:** Communications Lead posts regular updates without manual effort.

**Implementation:**

```python
# Slack Bot: Status Update Reminder
Every 15 minutes during SEV0/SEV1:
  - Post to incident channel:
    "⏰ Status Update Due
     Last update: 15 minutes ago
     Template: [Link to status update template]
     @comms-lead please post update"

# Status Page Auto-Post
When update posted in Slack:
  - Bot detects message from @comms-lead
  - Parses update format
  - Auto-posts to status page
  - Tweets from @StatusAccount
```

**Tools:**
- Slack Bot (Bolt framework)
- Statuspage.io API
- Twitter API (for status tweets)

### Pattern 3: Runbook Execution Tracking

**Goal:** Track which runbook steps completed during incident.

**Implementation:**

```markdown
# Interactive Runbook in Slack
/runbook database-failover

Bot Posts Checklist:
[ ] 1. Verify primary DB is down
[ ] 2. Check replication lag
[ ] 3. Promote secondary to primary
[ ] 4. Update DNS to new primary
[ ] 5. Verify application connectivity

Responder clicks checkboxes as completed
Bot timestamps each step
At incident close, full log available for post-mortem
```

**Tools:**
- Slack Block Kit (interactive messages)
- PagerDuty Runbook Automation
- Custom bot with runbook storage

### Pattern 4: Blameless Post-Mortem Template

**Goal:** Consistent, high-quality post-mortems with minimal effort.

**Implementation:**

```yaml
# Auto-Generate Post-Mortem Doc
Trigger: Incident marked "Resolved" in PagerDuty
Actions:
  1. Create Google Doc from template
  2. Pre-fill:
     - Incident ID, severity, duration (from PagerDuty)
     - Timeline (from Slack channel messages)
     - Participants (from Slack channel members)
  3. Share with IC and SMEs
  4. Schedule post-mortem meeting (48 hours out)
  5. Post reminder in Slack to complete pre-work
```

**Tools:**
- Google Docs API
- PagerDuty webhook
- Slack channel history API
- Google Calendar API

### Pattern 5: On-Call Handoff Ceremony

**Goal:** Smooth transition between on-call rotations.

**Implementation:**

```
Weekly On-Call Handoff (Every Monday 10am)
├─ 1. Outgoing on-call presents:
│     - Incidents from past week
│     - Ongoing issues
│     - Upcoming changes/deploys
├─ 2. Incoming on-call asks questions
├─ 3. Review on-call runbooks
├─ 4. Verify access (VPN, PagerDuty, dashboards)
└─ 5. Update shared handoff doc
```

**Documentation:**

```markdown
# On-Call Handoff Doc (Updated Weekly)

## Week of Dec 3-10, 2025
**Outgoing:** Alice
**Incoming:** Bob

### Active Issues
- Database replica lag spiking (SEV3, monitoring)
- Occasional 500s on /api/search (investigating)

### Upcoming Changes
- Dec 5: Deploy v2.3.0 (high risk, IC on standby)
- Dec 7: Database maintenance window (2-4am)

### New Runbooks
- Added: "Redis Cache Invalidation"
- Updated: "Database Failover" (new DNS process)

### Notes
- Cache hit rate dropped 10%, investigating
- Support team escalated login issue, no repro yet
```

---

## Tool Recommendations

### Tier 1: Incident Management Platforms (Choose One)

#### 1. PagerDuty
**Best For:** Established enterprises, complex escalation policies, extensive integrations

**Strengths:**
- **700+ Integrations:** Datadog, Prometheus, AWS CloudWatch, etc.
- **AIOps:** Intelligent event grouping, noise reduction
- **Mature Platform:** Battle-tested by thousands of companies
- **Terraform Provider:** Infrastructure-as-code support (976 code snippets)
- **API:** Comprehensive automation capabilities (208 code snippets)

**Weaknesses:**
- **Cost:** Expensive for small teams ($19-41/user/month)
- **Complexity:** Feature-rich but steep learning curve

**When to Choose:**
- Team size: 10+ engineers
- Budget: $500+/month
- Need: Complex multi-team escalations, extensive integrations

**Resources:**
- Context7: `/pagerduty/terraform-provider-pagerduty` (High reputation, 976 snippets)
- Context7: `/websites/developer_pagerduty_api-reference` (High reputation, Benchmark 35.2)

#### 2. Opsgenie
**Best For:** Atlassian ecosystem users, flexible routing, mid-sized teams

**Strengths:**
- **Atlassian Integration:** Seamless with Jira, Confluence, Bitbucket
- **Flexible Routing:** Advanced on-call scheduling, customizable workflows
- **Cost:** More affordable than PagerDuty (~$9-29/user/month)
- **Mobile App:** Excellent iOS/Android experience

**Weaknesses:**
- **Fewer Integrations:** Less extensive than PagerDuty
- **AIOps:** Less mature than PagerDuty's AI features

**When to Choose:**
- Already using Atlassian products
- Budget: $200-500/month
- Need: Custom routing rules, flexible schedules

#### 3. incident.io
**Best For:** Modern teams, AI-powered response, Slack-native workflow

**Strengths:**
- **AI-Powered:** Autonomous investigation, faster resolution
- **Slack-Native:** Deep Slack integration for workflow
- **Modern UX:** Clean, intuitive interface
- **Full-Stack:** On-call, incident management, post-mortems in one platform

**Weaknesses:**
- **Newer Platform:** Less proven than PagerDuty/Opsgenie
- **Integration:** Fewer third-party integrations
- **Limited Documentation:** Not yet in Context7 (newer product)

**When to Choose:**
- Team size: 5-50 engineers
- Workflow: Slack-centric culture
- Need: Modern tooling, AI assistance

#### 4. Splunk On-Call (VictorOps)
**Best For:** Splunk users, existing Splunk observability stack

**Strengths:**
- **Splunk Ecosystem:** Native integration with Splunk Observability Cloud
- **Timeline View:** Excellent incident timeline visualization
- **ChatOps:** Strong Slack/Teams integration

**Weaknesses:**
- **Splunk Lock-In:** Less valuable without Splunk stack
- **Cost:** Tied to Splunk licensing

**When to Choose:**
- Already using Splunk for monitoring/logging
- Need: Unified Splunk platform

### Tier 2: Status Page Solutions

#### 1. Statuspage.io (Atlassian)
**Best For:** Most teams, trusted brand, easy setup

**Strengths:**
- **Trusted:** Widely recognized by customers
- **Easy Setup:** 10-minute deployment
- **Integrations:** Auto-updates from PagerDuty, Datadog, etc.
- **Subscriber Management:** Email/SMS notifications

**Cost:** $29-399/month

#### 2. Instatus
**Best For:** Budget-conscious teams, modern design

**Strengths:**
- **Affordable:** $19-99/month
- **Modern UI:** Clean, customizable design
- **Fast:** Lightweight, fast page loads
- **Unlimited Subscribers:** No subscriber limits

**Weaknesses:**
- **Fewer Features:** Less mature than Statuspage.io

#### 3. Custom Status Page (Self-Hosted)
**Best For:** High customization needs, compliance requirements

**Example:** GitHub Status (custom-built)
**Pros:** Full control, no vendor lock-in
**Cons:** Maintenance burden, build time

### Tier 3: Communication Tools

#### 1. Slack (Recommended)
**Best For:** Real-time incident coordination

**Use Cases:**
- Incident channels (`#incident-YYYY-MM-DD-topic`)
- War room huddles (voice/video)
- Bot integrations (status updates, runbook execution)
- Post-mortem scheduling

#### 2. Microsoft Teams
**Best For:** Microsoft-centric organizations

**Similar Capabilities:** Channels, video calls, bot integrations

### Tier 4: Post-Mortem Tools

#### 1. Google Docs (Recommended for Most)
**Best For:** Collaboration, commenting, version history

**Template:** [Link to blameless post-mortem template]

#### 2. Confluence
**Best For:** Teams already using Atlassian

**Strengths:** Wiki integration, searchable knowledge base

#### 3. Jeli
**Best For:** Advanced incident analysis, learning-focused teams

**Strengths:**
- Timeline reconstruction from Slack, logs, metrics
- Pattern detection across incidents
- Learning-focused (not just blameless, but educational)

**Cost:** Enterprise pricing (contact sales)

### Tier 5: Runbook Automation

#### 1. Rundeck
**Best For:** Self-hosted, complex automation

**Strengths:**
- Open-source (Community Edition)
- Job scheduling, SSH execution
- ACL for secure runbook access

**Weaknesses:** Requires maintenance, older UI

#### 2. PagerDuty Runbook Automation
**Best For:** PagerDuty users, simple workflows

**Strengths:**
- Integrated with PagerDuty incidents
- Web-based runbook builder
- Step tracking

**Weaknesses:** Limited to PagerDuty ecosystem

#### 3. Custom Scripts + Git
**Best For:** Small teams, simple runbooks

**Pattern:**
```
/runbooks
  ├── database-failover.sh
  ├── cache-invalidation.sh
  └── README.md (index of runbooks)
```

**Pros:** Version controlled, executable, no vendor
**Cons:** No UI, manual execution tracking

### Recommended Starter Stack (Budget: $500/month)

```
Incident Management: incident.io or Opsgenie ($200-400/month)
Status Page: Instatus ($19-99/month)
Communication: Slack (free or $7/user/month)
Post-Mortems: Google Docs (free)
Runbooks: Git + Markdown (free)
Monitoring Integration: Prometheus + Grafana (free/self-hosted)
```

### Recommended Enterprise Stack (Budget: $2,000+/month)

```
Incident Management: PagerDuty ($1,000-3,000/month)
Status Page: Statuspage.io ($399/month)
Communication: Slack ($7/user/month)
Post-Mortems: Confluence + Jeli ($500+/month)
Runbooks: PagerDuty Runbook Automation (included)
Monitoring Integration: Datadog, New Relic, Splunk
```

---

## Skill Structure Design

### Proposed SKILL.md Structure

```markdown
---
name: incident-management
description: Guide incident response from detection to post-mortem using SRE principles, severity classification, on-call management, blameless culture, and communication protocols. Use when setting up incident processes, designing escalation policies, or conducting post-mortems.
---

## Purpose
Provide end-to-end incident management guidance covering detection, response,
communication, and learning. Emphasizes SRE culture, blameless post-mortems,
and structured processes for high-reliability operations.

## When to Use This Skill
- Setting up incident response processes for a team
- Designing on-call rotations and escalation policies
- Creating runbooks for common failure scenarios
- Conducting blameless post-mortems
- Implementing incident communication protocols
- Choosing incident management tooling
- Improving MTTR and incident frequency metrics

## Core Concepts

### Severity Classification
[Reference: references/severity-levels.md]
- SEV0/P0: Complete outage
- SEV1/P1: Major degradation
- SEV2/P2: Minor issues
- SEV3/P3: Cosmetic/low-impact

### Incident Command Structure
[Reference: references/incident-roles.md]
- Incident Commander (IC)
- Communications Lead
- Subject Matter Experts (SMEs)
- Scribe

### Blameless Post-Mortems
[Reference: references/blameless-postmortems.md]
- Culture principles
- Facilitation guide
- Template and examples

## Decision Frameworks

### 1. Severity Classification
[Script: scripts/classify-severity.py]
Run this script to get recommended severity based on impact/urgency.

### 2. Escalation Matrix
[Reference: references/escalation-matrix.md]

### 3. Tool Selection
[Reference: references/tool-comparison.md]
PagerDuty vs Opsgenie vs incident.io

## Implementation Guide

### Phase 1: Foundation (Week 1)
1. Define severity levels for your organization
2. Set up basic on-call rotation
3. Choose incident management platform
4. Create incident Slack channel template

### Phase 2: Processes (Week 2-3)
1. Document escalation policies
2. Create first 5 runbooks (most common incidents)
3. Set up status page
4. Train team on incident response

### Phase 3: Culture (Week 4+)
1. Conduct first blameless post-mortem
2. Establish post-mortem cadence
3. Track MTTA/MTTR metrics
4. Iterate on runbooks

## Runbook Templates
[Examples: examples/runbooks/]
- database-failover.md
- cache-invalidation.md
- ddos-mitigation.md

## Post-Mortem Template
[Examples: examples/postmortem-template.md]

## Tool Integration Examples
[Examples: examples/integrations/]
- pagerduty-slack-integration.py
- statuspage-auto-update.py
- postmortem-auto-generator.py

## Anti-Patterns to Avoid
- Delayed incident declaration (waiting for certainty)
- Skipping post-mortems for "small" incidents
- Blame culture in post-mortems
- Ignoring action items from post-mortems
- No clear IC assignment
- Alert fatigue from noisy, non-actionable alerts

## Metrics to Track
- MTTA (Mean Time To Acknowledge)
- MTTR (Mean Time To Recovery)
- MTBF (Mean Time Between Failures)
- Incident frequency (SEV0, SEV1, SEV2)
- Action item completion rate

## Further Reading
- Google SRE Book: "Postmortem Culture"
- Atlassian: "How to Run a Blameless Postmortem"
- PagerDuty: "Incident Response Guide"
```

### Proposed Directory Structure

```
skills/incident-management/
├── SKILL.md                          # Main skill file (~400 lines)
├── references/
│   ├── severity-levels.md            # Detailed severity classification
│   ├── incident-roles.md             # IC, Comms Lead, SME responsibilities
│   ├── escalation-matrix.md          # Escalation decision framework
│   ├── blameless-postmortems.md      # Culture, facilitation, examples
│   ├── communication-protocols.md    # Internal/external communication
│   └── tool-comparison.md            # PagerDuty vs Opsgenie vs incident.io
├── examples/
│   ├── runbooks/
│   │   ├── database-failover.md
│   │   ├── cache-invalidation.md
│   │   ├── ddos-mitigation.md
│   │   └── certificate-renewal.md
│   ├── postmortem-template.md        # Full blameless post-mortem template
│   ├── status-update-templates.md    # Slack/email/status page templates
│   └── integrations/
│       ├── pagerduty-slack.py        # Auto-create incident channel
│       ├── statuspage-auto-update.py # Post updates to status page
│       └── postmortem-generator.py   # Auto-generate post-mortem doc
├── scripts/
│   ├── classify-severity.py         # Interactive severity classifier
│   └── validate-runbook.sh          # Check runbook format/links
└── assets/
    ├── incident-response-flowchart.png
    └── escalation-matrix-visual.png
```

### Progressive Disclosure Strategy

**Level 1: SKILL.md (Always Loaded - ~400 lines)**
- Purpose and when to use
- Core concepts (summary)
- Decision framework (high-level)
- Links to references and examples

**Level 2: References (Loaded on Demand)**
- `severity-levels.md`: Detailed classification criteria, examples
- `incident-roles.md`: Full IC/Comms Lead/SME responsibilities
- `blameless-postmortems.md`: Culture guide, facilitation, templates
- `tool-comparison.md`: PagerDuty vs Opsgenie vs incident.io deep-dive

**Level 3: Scripts (Executed, Not Loaded - Token-Free!)**
- `classify-severity.py`: Interactive CLI for severity classification
- `postmortem-generator.py`: Auto-generate post-mortem doc from PagerDuty

**Level 4: Examples (Loaded on Demand)**
- Runbooks: Copy-paste templates for common scenarios
- Post-mortem template: Full example with filled sections
- Integration scripts: Reference implementations

**Total Token Budget:**
- SKILL.md: ~4,000 tokens (always loaded)
- References: ~8,000 tokens total (loaded selectively)
- Examples: ~6,000 tokens total (loaded selectively)
- Scripts: 0 tokens (executed, not loaded)

---

## Integration Points

### Integration with Other Skills

**1. Observability Skills:**
- **Use Together:** Monitoring/alerting setup provides incident detection signals
- **Handoff:** Observability skill sets up alerts → Incident Management defines response
- **Example:** Prometheus alert fires → PagerDuty creates incident → IC follows runbook

**2. Disaster Recovery Skill:**
- **Use Together:** DR focuses on data/infrastructure recovery; Incident Management on operational response
- **Handoff:** Incident Management declares SEV0 → DR runbooks activated for recovery
- **Example:** Database corruption detected → Incident declared → DR playbook restores from backup

**3. Security Incident Response Skill:**
- **Use Together:** Security incidents follow similar process but different protocols
- **Handoff:** Incident Management provides process framework; Security adds compliance/forensics
- **Example:** Data breach detected → Incident declared → Security runbooks + legal notification

**4. Infrastructure-as-Code Skill:**
- **Use Together:** IaC enables fast recovery via automated rebuild
- **Handoff:** Incident Management identifies need to rebuild → IaC scripts execute
- **Example:** Kubernetes cluster compromised → Incident declared → Terraform rebuilds cluster

**5. Performance Engineering Skill:**
- **Use Together:** Performance incidents (slow response times) trigger incident response
- **Handoff:** Incident Management mitigates → Performance Engineering investigates optimization
- **Example:** API latency spike → Incident declared → Performance team profiles code

### External Tool Integrations

**Monitoring → Incident Management:**
- Prometheus Alertmanager → PagerDuty
- Datadog Monitors → Opsgenie
- AWS CloudWatch Alarms → incident.io

**Incident Management → Communication:**
- PagerDuty → Slack (auto-create channels)
- Opsgenie → Microsoft Teams
- incident.io → Statuspage.io

**Incident Management → Runbook Execution:**
- PagerDuty → Rundeck (trigger automated remediation)
- Opsgenie → Ansible (execute playbooks)
- incident.io → GitHub Actions (run workflows)

**Post-Mortem → Knowledge Base:**
- Google Docs → Confluence (archive post-mortems)
- Jeli → Notion (centralized incident learnings)
- Custom → Wiki (searchable runbook library)

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1)

**Objective:** Establish basic incident response capability.

**Tasks:**
1. **Define Severity Levels:**
   - Adapt standard SEV0-SEV3 to your organization
   - Document examples for each severity
   - Share with team for feedback
   - **Deliverable:** `severity-levels.md`

2. **Choose Incident Management Platform:**
   - Evaluate: PagerDuty, Opsgenie, incident.io
   - Consider: Team size, budget, integrations
   - Set up trial account
   - **Deliverable:** Platform selected, trial active

3. **Set Up Basic On-Call Rotation:**
   - Define: Primary + Secondary on-call
   - Schedule: 1-week rotations
   - Configure: Escalation after 5 min no-ack
   - **Deliverable:** On-call schedule published

4. **Create Incident Slack Channel Template:**
   - Format: `#incident-YYYY-MM-DD-topic`
   - Pin: Severity, IC, status update template
   - **Deliverable:** Slack workflow or bot configured

**Success Criteria:**
- [ ] Severity levels documented and approved
- [ ] Incident management platform configured
- [ ] On-call rotation active
- [ ] Team trained on declaring incidents

### Phase 2: Processes (Weeks 2-3)

**Objective:** Document and automate incident response processes.

**Tasks:**
1. **Document Escalation Policies:**
   - Define: When to escalate (time, severity, expertise)
   - Create: Escalation matrix (Primary → Secondary → Lead → Director)
   - Configure: Platform escalation rules
   - **Deliverable:** `escalation-matrix.md`

2. **Create First 5 Runbooks:**
   - Identify: 5 most common incidents from past 6 months
   - Template: Use runbook structure (Trigger, Steps, Rollback, Owner)
   - Test: Run through each runbook in staging
   - **Deliverable:** 5 runbooks in `examples/runbooks/`

3. **Set Up Status Page:**
   - Choose: Statuspage.io, Instatus, or custom
   - Configure: Components (API, Database, Web App)
   - Integrate: Auto-update from incident platform
   - **Deliverable:** Status page live, URL shared

4. **Train Team on Incident Response:**
   - Workshop: 1-hour session covering severity, roles, runbooks
   - Simulation: Tabletop exercise (simulate SEV1 incident)
   - Q&A: Address team concerns
   - **Deliverable:** Team trained, simulation completed

**Success Criteria:**
- [ ] Escalation policies documented and configured
- [ ] 5 runbooks created and tested
- [ ] Status page live and integrated
- [ ] Team comfortable with incident response process

### Phase 3: Culture (Weeks 4-8)

**Objective:** Establish blameless culture and continuous improvement.

**Tasks:**
1. **Conduct First Blameless Post-Mortem:**
   - Schedule: Within 48 hours of next SEV1+ incident
   - Facilitate: Use blameless principles (no blame, focus on systems)
   - Document: Use post-mortem template
   - Share: Distribute to engineering, product, support
   - **Deliverable:** First post-mortem completed

2. **Establish Post-Mortem Cadence:**
   - Policy: All SEV0/SEV1 incidents get post-mortems
   - Schedule: Within 48 hours of resolution
   - Follow-Up: Action items in sprint planning
   - **Deliverable:** Post-mortem policy documented

3. **Track MTTA/MTTR Metrics:**
   - Implement: Dashboards for MTTA, MTTR, MTBF
   - Review: Weekly trend analysis
   - Improvement: Set targets (e.g., MTTR < 1 hour for SEV1)
   - **Deliverable:** Metrics dashboard live

4. **Iterate on Runbooks:**
   - Review: Update runbooks after each use
   - Expand: Add 5 more runbooks based on new incidents
   - Automate: Convert manual steps to scripts
   - **Deliverable:** 10 runbooks, 2 automated

**Success Criteria:**
- [ ] Blameless post-mortem culture established
- [ ] MTTA/MTTR metrics trending downward
- [ ] 10 runbooks created, 2 automated
- [ ] Team confidence in incident response high

### Phase 4: Optimization (Months 3-6)

**Objective:** Advanced automation and optimization.

**Tasks:**
1. **Automate Incident Declaration:**
   - Implement: Slack slash command `/incident-declare`
   - Auto-Create: Incident channel, assign IC, post status
   - Integrate: PagerDuty, status page
   - **Deliverable:** Automated incident declaration

2. **Implement Runbook Automation:**
   - Choose: Rundeck, PagerDuty Runbook Automation, or custom
   - Migrate: 5 runbooks to automated execution
   - Track: Step completion during incidents
   - **Deliverable:** 5 automated runbooks

3. **Advanced Post-Mortem Analysis:**
   - Tool: Evaluate Jeli for pattern detection
   - Review: Quarterly incident trend analysis
   - Share: Executive report on incident learnings
   - **Deliverable:** Quarterly incident review process

4. **Chaos Engineering for Incident Response:**
   - Simulate: Monthly DR drills (database failover, region outage)
   - Test: Verify runbooks work under pressure
   - Improve: Update runbooks based on drill learnings
   - **Deliverable:** Monthly DR drill cadence

**Success Criteria:**
- [ ] Incident declaration fully automated
- [ ] 50%+ of runbooks automated
- [ ] Quarterly incident reviews completed
- [ ] Monthly DR drills running

### Ongoing: Maintenance and Refinement

**Continuous Activities:**
- **Weekly:** On-call handoff ceremony
- **Post-Incident:** Blameless post-mortem within 48 hours
- **Monthly:** Review MTTA/MTTR trends, update runbooks
- **Quarterly:** Incident trend analysis, tooling evaluation
- **Annually:** Incident response training refresh, update severity definitions

**Metrics to Track:**
- Incident frequency (downward trend expected)
- MTTR (< 1 hour for SEV1)
- Action item completion rate (> 90%)
- On-call satisfaction (survey quarterly)
- Customer satisfaction (post-incident surveys)

---

## Conclusion

This skill provides comprehensive guidance for building world-class incident management capabilities. By focusing on **culture (blameless), process (structured response), and tools (automation)**, teams can reduce MTTR, improve reliability, and create a learning-oriented engineering culture.

**Key Takeaways:**

1. **Declare Early, Declare Often:** Incidents are not failures; late detection is.
2. **Mitigation First:** Stop customer impact before diagnosing root cause.
3. **Blameless Culture:** Focus on systems, not people, to enable honest learning.
4. **Runbooks Are Living Documents:** Update after every use, automate over time.
5. **Metrics Drive Improvement:** Track MTTA/MTTR/MTBF to measure progress.
6. **Communication is Critical:** Internal coordination and external transparency build trust.
7. **Action Items Matter:** Post-mortems without follow-through are wasted effort.

**Next Steps:**
1. Review this master plan with your team
2. Begin Phase 1: Foundation (Week 1 tasks)
3. Create first version of SKILL.md based on this structure
4. Test skill with real incident scenarios
5. Iterate based on team feedback

**Remember:** The goal is not zero incidents (impossible in complex systems), but **rapid detection, effective response, transparent communication, and continuous learning** from every incident.

---

**Document Status:** Init.md Complete ✓
**Next Phase:** Create SKILL.md and bundled resources (references/, examples/, scripts/)
**Estimated Total Skill Size:** 500-800 lines (~5,000 tokens for SKILL.md, ~15,000 tokens total with references)
