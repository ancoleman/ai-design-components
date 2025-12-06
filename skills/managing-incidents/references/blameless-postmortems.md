# Blameless Post-Mortems Guide


## Table of Contents

- [Overview](#overview)
- [Core Philosophy](#core-philosophy)
  - [Blameless Culture Tenets](#blameless-culture-tenets)
- [Post-Mortem Process](#post-mortem-process)
  - [Timeline](#timeline)
- [Post-Mortem Meeting Facilitation](#post-mortem-meeting-facilitation)
  - [Facilitator Role](#facilitator-role)
  - [Meeting Structure](#meeting-structure)
- [Root Cause Analysis Techniques](#root-cause-analysis-techniques)
  - [5 Whys Method](#5-whys-method)
  - [Fishbone Diagram (Ishikawa)](#fishbone-diagram-ishikawa)
- [Post-Mortem Document Template](#post-mortem-document-template)
  - [Section 1: Incident Summary](#section-1-incident-summary)
  - [Section 2: Timeline](#section-2-timeline)
  - [Section 3: Root Cause Analysis](#section-3-root-cause-analysis)
  - [Section 4: Impact Assessment](#section-4-impact-assessment)
  - [Section 5: What Went Well](#section-5-what-went-well)
  - [Section 6: What Went Wrong](#section-6-what-went-wrong)
  - [Section 7: Action Items](#section-7-action-items)
  - [Section 8: Lessons Learned](#section-8-lessons-learned)
- [Facilitation Techniques](#facilitation-techniques)
  - [Keeping Discussion Blameless](#keeping-discussion-blameless)
  - [Encouraging Honest Participation](#encouraging-honest-participation)
- [Common Post-Mortem Mistakes](#common-post-mortem-mistakes)
  - [Mistake 1: Stopping at Human Error](#mistake-1-stopping-at-human-error)
  - [Mistake 2: Vague Action Items](#mistake-2-vague-action-items)
  - [Mistake 3: Too Many Action Items](#mistake-3-too-many-action-items)
  - [Mistake 4: No Follow-Up](#mistake-4-no-follow-up)
  - [Mistake 5: Punishing Honesty](#mistake-5-punishing-honesty)
- [Post-Mortem Distribution](#post-mortem-distribution)
  - [Internal Audiences](#internal-audiences)
  - [External Communication](#external-communication)
- [Knowledge Base Integration](#knowledge-base-integration)
  - [Post-Mortem Archive](#post-mortem-archive)
  - [Runbook Updates](#runbook-updates)
- [Post-Mortem Metrics](#post-mortem-metrics)
  - [Track Effectiveness](#track-effectiveness)
- [Blameless Culture Maintenance](#blameless-culture-maintenance)
  - [Leadership Behaviors](#leadership-behaviors)
  - [Team Norms](#team-norms)
- [Further Reading](#further-reading)

## Overview

Blameless post-mortems transform incidents from failures into learning opportunities. Focus on systemic improvements rather than individual blame to build psychological safety and organizational resilience.

## Core Philosophy

### Blameless Culture Tenets

**1. Assume Good Intentions**

Everyone made the best decision with the information available at the time. No one comes to work intending to break things.

**2. Focus on Systems, Not People**

Humans are not root causes. Systems that allow human error are root causes. Ask "How did the system fail?" not "Who failed?"

**3. Psychological Safety**

Create an environment where honesty is rewarded. Engineers must feel safe admitting mistakes without fear of punishment.

**4. Learning Opportunity**

Incidents are gifts of organizational knowledge. Each incident reveals gaps in processes, tools, or training.

**5. No Punishment for Mistakes**

Punishment discourages honesty and prevents learning. Exception: Willful negligence or malicious behavior (extremely rare).

---

## Post-Mortem Process

### Timeline

**Within 2 Hours of Resolution:**
- IC schedules post-mortem meeting (24-48 hours out)
- Assign post-mortem facilitator (NOT the IC)
- Create post-mortem document from template

**Pre-Meeting (Before Post-Mortem Meeting):**
- Scribe shares incident timeline
- IC drafts initial post-mortem document
- SMEs gather supporting data (logs, metrics, screenshots)
- Distribute draft to attendees 24 hours before meeting

**Post-Mortem Meeting (60-90 minutes):**
- Facilitator walks through timeline
- Team discusses root causes (5 Whys, Fishbone)
- Identify what went well and what went wrong
- Define action items with owners and due dates

**Post-Meeting:**
- Finalize post-mortem document
- Distribute to engineering, product, support, leadership
- Add to knowledge base for searchability
- Track action items in sprint planning

---

## Post-Mortem Meeting Facilitation

### Facilitator Role

**Why Not IC:** IC may be defensive about decisions made. Neutral facilitator keeps discussion blameless and productive.

**Facilitator Selection:** Senior engineer, SRE, engineering manager (someone trusted by team, skilled in group facilitation).

### Meeting Structure

**1. Introduction (5 minutes)**

Facilitator sets tone:
> "This is a blameless post-mortem. We're here to learn, not to assign blame. Everyone did their best with the information they had. Our goal is to understand how the system failed and how we can improve it."

**2. Timeline Review (15 minutes)**

Scribe or IC walks through timeline chronologically:
- What happened and when
- Who was involved
- What decisions were made
- What actions were taken

No judgment, just facts. Team asks clarifying questions.

**3. Root Cause Analysis (20 minutes)**

Facilitator leads 5 Whys or Fishbone diagram exercise to identify root causes.

**Important:** Stop at process or system failures, not at individuals.

Bad example:
> "Root cause: Alice deployed without testing."

Good example:
> "Root cause: Deployment process allows production deploys without staging validation."

**4. What Went Well (10 minutes)**

Celebrate effective responses:
- Fast detection (monitoring alert fired within 2 minutes)
- Clear IC leadership and delegation
- Effective communication (status updates every 15 minutes)
- Quick mitigation (rollback completed in 5 minutes)

Reinforces positive behaviors to repeat.

**5. What Went Wrong (15 minutes)**

Identify improvement areas (focus on process, tools, training):
- No pre-deploy validation step
- Missing monitoring for connection pool saturation
- Runbook outdated (referenced old database hostname)
- Communication delay (first status page update 30 minutes in)

Frame as learning opportunities, not mistakes.

**6. Action Items (15 minutes)**

Define specific, actionable improvements:
- ✅ Good: "Add connection pool saturation alert (threshold: 80%), owner: @alice, due: Dec 10"
- ❌ Bad: "Improve monitoring" (too vague)

Each action item must have:
- Specific task description
- Owner (single person)
- Due date
- Success criteria (how to verify completion)

**7. Closing (5 minutes)**

Facilitator summarizes:
- Key learnings
- Action item count and owners
- Next steps (document distribution, follow-up tracking)

Thank team for honest participation.

---

## Root Cause Analysis Techniques

### 5 Whys Method

Ask "Why?" five times to dig from symptom to root cause.

**Example:**

1. **Why did the API fail?**
   - Because the database connection pool was exhausted.

2. **Why was the connection pool exhausted?**
   - Because traffic doubled during holiday shopping.

3. **Why didn't the pool scale with traffic?**
   - Because pool size was hardcoded to 100 connections.

4. **Why was it hardcoded instead of auto-scaling?**
   - Because the configuration management system doesn't support dynamic scaling.

5. **Why doesn't the config system support dynamic scaling?**
   - Because it was designed before auto-scaling requirements emerged.

**Root Cause:** Configuration management system lacks dynamic scaling capabilities.

**Action Items:**
- Migrate to configuration system with dynamic scaling support
- Add auto-scaling rules for connection pool
- Document dynamic configuration best practices

---

### Fishbone Diagram (Ishikawa)

Categorize contributing factors into:
- **People:** Training gaps, expertise missing
- **Process:** Deployment procedure, communication protocol
- **Technology:** Tool limitations, infrastructure constraints
- **Environment:** Time pressure, external dependencies

**Example:**

```
                         API Outage
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
    PEOPLE                PROCESS             TECHNOLOGY
    - No DB expert    - No load testing    - Hardcoded pool size
    on-call           - Missing runbook    - No auto-scaling
                      - No staging check  - Monitoring gap
                                                │
                                          ENVIRONMENT
                                          - Holiday traffic spike
                                          - Vendor maintenance window
```

All branches contribute to incident. Focus on systemic factors, not individuals.

---

## Post-Mortem Document Template

### Section 1: Incident Summary

**Format:**
```markdown
## Incident Summary

**Incident ID:** INC-2025-12-03-001
**Severity:** SEV1
**Duration:** 90 minutes (14:15 - 15:45 PST)
**Date:** December 3, 2025
**Author:** [Name]
**Attendees:** [IC, SMEs, stakeholders]

### Summary
In 2-3 sentences, describe what happened in plain language.

Example: "On December 3, 2025, our API experienced elevated error rates (15% failure) due to database connection pool exhaustion. Approximately 5,000 customers were unable to complete checkout during the incident."
```

---

### Section 2: Timeline

**Format:**
```markdown
## Timeline (All times PST)

| Time  | Event |
|-------|-------|
| 14:15 | Alert: "API Error Rate High" fired |
| 14:17 | On-call engineer @alice acknowledged, began investigation |
| 14:20 | Incident declared SEV1, IC @bob assigned |
| 14:25 | Root cause identified: DB connection pool saturated |
| 14:30 | Mitigation: Increased connection pool size 100 → 200 |
| 14:35 | Error rate dropped to 5% |
| 14:45 | Secondary issue found: retry logic causing thundering herd |
| 14:50 | Disabled aggressive retry, enabled circuit breaker |
| 15:00 | Error rate returned to baseline (<0.1%) |
| 15:00-15:45 | Monitoring for stability |
| 15:45 | IC declared incident resolved |
```

**Include:**
- Detection time (first alert or customer report)
- Key investigation milestones
- Decisions made by IC
- Mitigation actions
- Resolution confirmation

---

### Section 3: Root Cause Analysis

**Format:**
```markdown
## Root Cause Analysis

### Primary Root Cause
The direct trigger or failure point.

Example: "Database connection pool size (100 connections) was insufficient for peak traffic load (doubled due to holiday shopping)."

### Contributing Factors
Conditions that worsened impact or prevented faster resolution.

1. Aggressive retry logic caused "thundering herd" when DB slowed
2. No alerting on connection pool saturation (only on API errors)
3. Recent code deploy increased DB query frequency by 20%
4. No load testing for 2x traffic scenarios

### 5 Whys Analysis
1. Why did API fail? → DB connection pool exhausted
2. Why was pool exhausted? → Traffic doubled, pool size unchanged
3. Why didn't we anticipate? → No load testing for 2x traffic
4. Why no load testing? → Not in release checklist
5. Why not in checklist? → Process gap

**Root Cause:** Release process lacks traffic spike load testing requirement.
```

---

### Section 4: Impact Assessment

**Format:**
```markdown
## Impact Assessment

### Customer Impact
- **Users Affected:** ~5,000 (15% of active users during incident)
- **Duration:** 90 minutes
- **Functionality:** Unable to complete checkout
- **Data Loss:** None
- **Geographic Spread:** Global (all regions)

### Business Impact
- **Revenue:** Estimated $12,000 in lost transactions
- **SLA Breach:** 99.9% monthly SLA violated (now at 99.85%)
- **Support Load:** 47 tickets filed during incident
- **Reputation:** 12 negative social media posts

### Technical Impact
- **Services Affected:** API, checkout service, payment processing
- **Infrastructure:** Database connection pool, application servers
- **Dependencies:** None (isolated to our infrastructure)
```

---

### Section 5: What Went Well

**Format:**
```markdown
## What Went Well

Celebrate effective responses:

1. **Fast Detection:** Alert fired within 2 minutes of error rate increase
2. **Clear IC Assignment:** @bob took IC role immediately, delegated effectively
3. **Communication:** Status updates posted every 15 minutes to #incident channel
4. **Quick Mitigation:** Connection pool increase deployed within 15 minutes
5. **No Data Loss:** No customer data lost or corrupted
6. **Documentation:** Real-time timeline maintained by scribe
```

Reinforces behaviors to repeat in future incidents.

---

### Section 6: What Went Wrong

**Format:**
```markdown
## What Went Wrong

Focus on process, tools, or training gaps (not people):

1. **No Proactive Monitoring:** Connection pool metrics not monitored, only reactive error alerts
2. **Retry Logic Untested:** Circuit breaker not tested under DB degradation scenarios
3. **Missing Load Testing:** Recent deploy not load tested for 2x traffic spike
4. **Delayed External Communication:** First status page update 30 minutes into incident
5. **Outdated Runbook:** Database failover runbook referenced old hostname
```

Frame as improvement opportunities, not mistakes.

---

### Section 7: Action Items

**Format:**
```markdown
## Action Items

| Action | Owner | Due Date | Priority | Status |
|--------|-------|----------|----------|--------|
| Add connection pool saturation alert (threshold: 80%) | @alice | 2025-12-10 | High | In Progress |
| Implement circuit breaker library for DB queries | @bob | 2025-12-15 | High | Not Started |
| Add "load test for 2x traffic" to release checklist | @charlie | 2025-12-05 | Medium | Complete |
| Update database failover runbook with new hostnames | @alice | 2025-12-08 | Medium | Not Started |
| Send post-incident email to affected customers | @comms | 2025-12-04 | High | Complete |
| Review and update all runbooks for accuracy | @team | 2025-12-20 | Low | Not Started |
```

**Action Item Requirements:**
- **Specific:** Clear task description
- **Owned:** Single owner (not "team")
- **Dated:** Realistic due date
- **Prioritized:** High/Medium/Low
- **Tracked:** Status updated weekly in sprint planning

**Follow-Up:**
- Review action items in sprint planning
- Track completion rate (target: >90%)
- Celebrate completions in team meetings
- Escalate blocked items to leadership

---

### Section 8: Lessons Learned

**Format:**
```markdown
## Lessons Learned

Key takeaways for organizational knowledge:

1. **Connection pool metrics are leading indicators:** Monitor saturation before errors occur.
2. **Retry logic needs circuit breakers:** Prevent thundering herd in degradation scenarios.
3. **Load testing must include traffic spikes:** 2x traffic scenarios should be standard.
4. **Proactive > Reactive:** Leading indicator alerts (pool saturation) better than lagging indicators (errors).
5. **Runbooks are living documents:** Quarterly review and update cycle needed.
```

---

## Facilitation Techniques

### Keeping Discussion Blameless

**If Blame Language Appears:**

❌ "Alice shouldn't have deployed without testing."

Facilitator redirects:
✅ "Let's focus on the process. What would have prevented this deploy? Should we add a staging validation step to our deployment checklist?"

---

**If Defensiveness Arises:**

Engineer: "I followed the runbook exactly!"

Facilitator validates:
✅ "You absolutely did the right thing following the runbook. Let's discuss: Was the runbook accurate? Did it cover this scenario? How can we improve it?"

---

**If Discussion Stalls:**

Facilitator uses prompts:
- "What surprised us about this incident?"
- "If we could go back in time, what would we change?"
- "What monitoring or tooling would have helped?"

---

### Encouraging Honest Participation

**Create Psychological Safety:**

Facilitator starts meeting:
> "I want to emphasize: Mistakes are learning opportunities. No one will be punished for speaking honestly here. In fact, the more honest we are, the more we learn."

**Acknowledge Difficulty:**

Facilitator validates emotions:
> "I know this was a stressful incident. It's hard to revisit tough moments. But your insights will help prevent this from happening again."

**Celebrate Honesty:**

When engineer admits gap:
> "Thank you for that honest assessment. That's exactly the kind of insight we need to improve."

---

## Common Post-Mortem Mistakes

### Mistake 1: Stopping at Human Error

❌ "Root cause: Engineer deployed without testing."

✅ "Root cause: Deployment process allows untested code to reach production. Recommend: Add mandatory staging validation step."

**Principle:** Humans will make mistakes. Systems should prevent mistakes from causing incidents.

---

### Mistake 2: Vague Action Items

❌ "Improve monitoring."

✅ "Add connection pool saturation alert with 80% threshold, Slack notification, owner: @alice, due: Dec 10."

**Principle:** Specific, actionable, owned, dated.

---

### Mistake 3: Too Many Action Items

❌ 25 action items defined (only 3 completed).

✅ 5 high-priority action items (4 completed on time).

**Principle:** Focus on high-impact improvements, not exhaustive lists.

---

### Mistake 4: No Follow-Up

❌ Post-mortem written, filed, never reviewed again.

✅ Action items tracked in sprint planning, completion celebrated, learnings shared in onboarding.

**Principle:** Post-mortems only valuable if action items completed.

---

### Mistake 5: Punishing Honesty

❌ Engineer admits mistake in post-mortem, receives performance warning.

✅ Engineer admits gap, team fixes process, engineer thanked for honesty.

**Principle:** Punishment destroys blameless culture. Next incident, no one will be honest.

---

## Post-Mortem Distribution

### Internal Audiences

**Engineering Team:**
- Full post-mortem document
- Discussion in team meeting
- Action items in sprint backlog

**Product Team:**
- Executive summary (impact, resolution, prevention)
- Customer-facing features affected

**Support Team:**
- Customer impact details
- Expected follow-up questions
- How to respond to inquiries

**Leadership:**
- Executive summary
- Business impact (revenue, SLA, reputation)
- High-level action items and timeline

### External Communication

**Customer Email (Post-Incident):**
- Plain-language summary of what happened
- Impact scope and duration
- What was done to fix
- What will be done to prevent recurrence
- Apology and support contact

See `examples/communication-templates.md` for customer email template.

**Public Post-Mortem (Optional):**
- Some companies publish redacted post-mortems publicly
- Builds trust through transparency
- Examples: Cloudflare, GitHub, GitLab
- Redact: Customer names, internal system details, security-sensitive information

---

## Knowledge Base Integration

### Post-Mortem Archive

Store all post-mortems in searchable knowledge base:
- **Wiki:** Confluence, Notion, GitHub Wiki
- **Folder Structure:** By date, severity, or affected service
- **Tagging:** Service tags (API, database, network), incident type (outage, degradation)

**Search Use Cases:**
- "Has this happened before?" (search by error message, affected service)
- "What did we learn about database failovers?" (search by tag)
- Onboarding: New engineers read past post-mortems to learn systems

---

### Runbook Updates

After each post-mortem:
- Update relevant runbooks with new learnings
- Add new runbooks for novel incident types
- Archive outdated runbooks

**Example:**
Post-mortem reveals database failover runbook referenced old hostname.
Action item: Update runbook with current hostnames, add validation step to verify DNS before promoting replica.

---

## Post-Mortem Metrics

### Track Effectiveness

**Action Item Completion Rate:**
- Formula: (Completed Items / Total Items) × 100
- Target: > 90%
- Review: Monthly in engineering leadership meeting

**Incident Recurrence Rate:**
- Formula: Same root cause incidents / Total incidents
- Target: < 5%
- Indicates: Effectiveness of preventive action items

**Time to Post-Mortem:**
- Formula: Hours from incident resolution to post-mortem meeting
- Target: < 48 hours
- Ensures: Fresh memory, timely learning

**Post-Mortem Quality:**
- Criteria: Blameless tone, specific action items, root cause identified
- Review: Sample post-mortems quarterly for quality

---

## Blameless Culture Maintenance

### Leadership Behaviors

**Leaders Must Model Blameless Behavior:**

❌ "Who broke production?"
✅ "What process allowed this to reach production?"

❌ "This was a stupid mistake."
✅ "This reveals a gap in our testing process."

**Leaders Must Celebrate Learning:**

After action items completed:
> "Great work on implementing the circuit breaker. This will prevent similar incidents. Thank you for turning this incident into a learning opportunity."

---

### Team Norms

**Incident Retro (Quarterly):**
- Review post-mortems from past quarter
- Identify trends (common root causes)
- Celebrate: Most improved metric (MTTR reduction, action item completion)
- Discuss: Is our post-mortem process working?

**Blameless Language:**
- Team commits to blameless language in Slack, meetings, code reviews
- Correct each other gently when blame language appears
- Reinforce: "We focus on systems, not people."

---

## Further Reading

**Books:**
- "The Field Guide to Understanding Human Error" by Sidney Dekker
- "The Checklist Manifesto" by Atul Gawande
- "Site Reliability Engineering" (Google) - Chapter 15: "Postmortem Culture"

**Articles:**
- Etsy: "Blameless PostMortems and a Just Culture"
- John Allspaw: "Blameless Post-Mortems and a Just Culture"
- Google SRE: "Postmortem Culture: Learning from Failure"

**Templates:**
- Atlassian: "Incident Postmortem Template"
- PagerDuty: "Post-Mortem Template"
- GitHub: dastergon/postmortem-templates (collection)

**Training:**
- "Human Factors in Incident Analysis" workshops
- "Blameless Culture" training (internal or external)
- "Facilitation Skills for Post-Mortems" courses
