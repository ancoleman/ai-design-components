# Post-Mortem: [Incident Title]

**Incident ID:** INC-YYYY-MM-DD-###
**Severity:** [SEV0 | SEV1 | SEV2]
**Duration:** [X hours/minutes] ([Start Time] - [End Time] [Timezone])
**Date:** [Month Day, Year]
**Author:** [Name]
**Attendees:** [List all post-mortem meeting participants]
**Status:** [Draft | Final | Archived]

---

## Incident Summary

**In 2-3 sentences, describe what happened in plain language accessible to non-technical readers.**

Example:
> On December 3, 2025, our API experienced elevated error rates (15% failure) due to database connection pool exhaustion. Approximately 5,000 customers were unable to complete checkout during the 90-minute incident. The issue was resolved by increasing the connection pool size and implementing circuit breaker logic.

---

## Impact Assessment

### Customer Impact

- **Users Affected:** [Number or percentage] ([X% of active users])
- **Duration:** [Hours/minutes of customer-facing impact]
- **Affected Functionality:** [Specific features unavailable]
- **Data Loss:** [None | Describe scope if any]
- **Geographic Spread:** [Regions affected: US-East, EU, Global, etc.]

### Business Impact

- **Revenue Impact:** [Estimated $ amount or "Negligible"]
- **SLA Breach:** [Yes/No - If yes, describe SLA violation]
- **Support Load:** [Number of tickets filed during incident]
- **Reputation:** [Social media mentions, news coverage if any]
- **Contractual:** [Customer SLA violations, penalties if applicable]

### Technical Impact

- **Services Affected:** [List all affected services/components]
- **Infrastructure:** [Database, API servers, network, etc.]
- **Dependencies:** [Third-party services impacted, upstream/downstream]
- **Data Integrity:** [Data loss, corruption, or inconsistency]

---

## Timeline

**All times in [Timezone]**

Provide a chronological record of events from detection to full recovery.

| Time  | Event | Actor |
|-------|-------|-------|
| HH:MM | First alert: "[Alert Name]" fired in [monitoring system] | [System] |
| HH:MM | @[engineer] acknowledged alert, began investigation | @[engineer] |
| HH:MM | Incident declared [severity], IC @[name] assigned | @[IC] |
| HH:MM | Root cause identified: [Brief description] | @[SME] |
| HH:MM | Mitigation applied: [Action taken] | @[SME] |
| HH:MM | [Metric] improved from [X%] to [Y%] | [System] |
| HH:MM | Secondary issue discovered: [Description] | @[SME] |
| HH:MM | Additional mitigation: [Action taken] | @[SME] |
| HH:MM | All metrics returned to baseline | [System] |
| HH:MM | IC declared incident resolved after [X min] stability | @[IC] |

**Key Milestones:**
- **Detection:** [HH:MM] (Time from incident start to first alert)
- **Acknowledgment:** [HH:MM] (MTTA: [X minutes])
- **Mitigation:** [HH:MM] (Time to stop customer impact)
- **Resolution:** [HH:MM] (MTTR: [X minutes])

---

## Root Cause Analysis

### Primary Root Cause

**What was the direct trigger or failure point that caused the incident?**

Example:
> Database connection pool size (100 connections) was insufficient for peak traffic load (2x normal due to holiday shopping season).

### Contributing Factors

**What conditions worsened the impact or prevented faster resolution?**

1. [Factor 1: e.g., Aggressive retry logic caused "thundering herd" when database slowed]
2. [Factor 2: e.g., No monitoring/alerting on connection pool saturation]
3. [Factor 3: e.g., Recent code deploy increased database query frequency by 20%]
4. [Factor 4: e.g., Runbook for database scaling was outdated]

### 5 Whys Analysis

**Dig deeper to identify systemic root causes:**

1. **Why did [incident occur]?**
   - [Answer]

2. **Why [answer to #1]?**
   - [Answer]

3. **Why [answer to #2]?**
   - [Answer]

4. **Why [answer to #3]?**
   - [Answer]

5. **Why [answer to #4]?**
   - [Answer]

**Systemic Root Cause:** [The process, tool, or cultural issue revealed by 5 Whys]

Example:
> Release process lacks load testing requirement for traffic spike scenarios, allowing performance-impacting changes to reach production without validation.

---

## What Went Well

**Celebrate effective incident response behaviors to reinforce positive actions.**

1. **[Positive aspect]:** [Description]
   - Example: "Fast detection: Alert fired within 2 minutes of error rate increase"

2. **[Positive aspect]:** [Description]
   - Example: "Clear IC leadership: @bob immediately took IC role and delegated tasks"

3. **[Positive aspect]:** [Description]
   - Example: "Effective communication: Status updates posted every 15 minutes"

4. **[Positive aspect]:** [Description]
   - Example: "Quick mitigation: Connection pool increase deployed within 10 minutes"

5. **[Positive aspect]:** [Description]
   - Example: "No data loss: All customer data remained intact"

---

## What Went Wrong

**Identify improvement areas, focusing on process, tools, or training gaps (NOT individuals).**

**Important:** Frame as learning opportunities, not blame. Use "How did the system fail?" not "Who failed?"

1. **[Improvement area]:** [Description]
   - Example: "No proactive monitoring: Connection pool saturation not monitored, only reactive error alerts"

2. **[Improvement area]:** [Description]
   - Example: "Untested retry logic: Circuit breaker not tested under database degradation scenarios"

3. **[Improvement area]:** [Description]
   - Example: "Missing load testing: Recent deploy not load tested for 2x traffic spike"

4. **[Improvement area]:** [Description]
   - Example: "Communication delay: First status page update 30 minutes into incident"

5. **[Improvement area]:** [Description]
   - Example: "Outdated runbook: Database scaling runbook referenced deprecated configuration"

---

## Action Items

**Define specific, actionable improvements with clear owners and due dates.**

**Requirements for each action item:**
- **Specific:** Clear task description, not vague ("Improve monitoring" ❌ | "Add connection pool saturation alert" ✅)
- **Owned:** Single person responsible (not "team")
- **Dated:** Realistic due date
- **Prioritized:** High/Medium/Low based on impact

| Action | Owner | Due Date | Priority | Status | Notes |
|--------|-------|----------|----------|--------|-------|
| [Action item 1] | @[name] | YYYY-MM-DD | High | Not Started | [Optional context] |
| [Action item 2] | @[name] | YYYY-MM-DD | High | In Progress | [Optional context] |
| [Action item 3] | @[name] | YYYY-MM-DD | Medium | Complete | [Optional context] |
| [Action item 4] | @[name] | YYYY-MM-DD | Medium | Not Started | [Optional context] |
| [Action item 5] | @[name] | YYYY-MM-DD | Low | Not Started | [Optional context] |

**Example Action Items:**

| Action | Owner | Due Date | Priority | Status |
|--------|-------|----------|----------|--------|
| Add connection pool saturation alert (threshold: 80%, Slack notification) | @alice | 2025-12-10 | High | In Progress |
| Implement circuit breaker library for database queries | @bob | 2025-12-15 | High | Not Started |
| Add "load test for 2x traffic" step to release checklist | @charlie | 2025-12-05 | Medium | Complete |
| Create runbook for database connection pool scaling | @alice | 2025-12-12 | Medium | Not Started |
| Send post-incident email to affected customers (draft in examples/communication-templates.md) | @comms | 2025-12-04 | High | Complete |
| Review and update all database runbooks for accuracy | @db-team | 2025-12-20 | Low | Not Started |

---

## Lessons Learned

**Key takeaways for organizational knowledge and future prevention.**

1. **[Lesson]:** [Description of insight gained]
   - Example: "Connection pool metrics are critical leading indicators: Monitor saturation before errors occur"

2. **[Lesson]:** [Description of insight gained]
   - Example: "Retry logic needs circuit breakers: Prevent thundering herd in database degradation scenarios"

3. **[Lesson]:** [Description of insight gained]
   - Example: "Load testing must include traffic spike scenarios: 2x traffic should be standard test case"

4. **[Lesson]:** [Description of insight gained]
   - Example: "Proactive monitoring > Reactive alerting: Leading indicators (saturation) better than lagging (errors)"

5. **[Lesson]:** [Description of insight gained]
   - Example: "Runbooks are living documents: Quarterly review and update cycle needed"

---

## Supporting Data

**Attach relevant logs, metrics, screenshots for reference.**

### Graphs and Metrics

- **API Error Rate:** [Link to Grafana dashboard or screenshot]
- **Database Connection Pool:** [Link to metrics]
- **Traffic Patterns:** [Link to traffic graphs]
- **CPU/Memory/Disk:** [Link to infrastructure metrics]

### Log Excerpts

```
[Paste relevant log entries showing error states, warnings, or key events]

Example:
2025-12-03 14:15:32 ERROR: Database connection pool exhausted (max: 100, active: 100)
2025-12-03 14:15:33 ERROR: Checkout API failed: connection timeout
```

### Configuration Changes

```
[Show before/after configuration if relevant]

Example:
Before: connection_pool_size = 100
After:  connection_pool_size = 200
```

### Alerts Fired

- **14:15:32 PST:** `API-Error-Rate-High` (Datadog)
- **14:17:45 PST:** `Database-Connection-Pool-Low` (manual check, not automated)
- **14:30:15 PST:** `API-Error-Rate-Normal` (recovery)

---

## Prevention Measures

**Summarize how action items will prevent recurrence.**

**Short-Term (Completed within 2 weeks):**
1. [Immediate fix applied, e.g., "Connection pool size increased to 200"]
2. [Monitoring added, e.g., "Alert added for 80% pool saturation"]

**Medium-Term (Completed within 1-2 months):**
1. [Process improvement, e.g., "Load testing requirement added to release checklist"]
2. [Tool improvement, e.g., "Circuit breaker library implemented"]

**Long-Term (Completed within 3-6 months):**
1. [Architectural change, e.g., "Auto-scaling connection pool implementation"]
2. [Training, e.g., "Team training on database performance tuning"]

---

## Communication

### Internal Communication

**Incident Channel:** [#incident-YYYY-MM-DD-topic]
**Status Updates:** [Number of updates posted, cadence]
**Stakeholders Notified:** [Engineering, product, support, leadership]

### External Communication

**Status Page:** [Link to public status page updates]
**Customer Email:** [Sent? Yes/No - If yes, link to email draft]
**Social Media:** [Twitter, LinkedIn updates if applicable]
**Press/Media:** [Any media coverage or press releases]

### Regulatory Notifications

**Required:** [Yes/No - GDPR, HIPAA, PCI, etc.]
**Notification Sent:** [Yes/No - If yes, date and recipient]
**Documentation:** [Link to regulatory notification records]

---

## Follow-Up Actions

### Action Item Tracking

- **Review Cadence:** [Weekly in sprint planning]
- **Tracking Tool:** [Jira, GitHub Issues, Linear, etc.]
- **Completion Target:** [Date by which all high-priority items should be complete]

### Post-Mortem Distribution

- [X] Engineering team (via Slack #engineering)
- [X] Product team (via email)
- [X] Support team (via Slack #support)
- [X] Leadership (via email)
- [X] Knowledge base (archived in Confluence/Wiki)

### Post-Mortem Review

**Next Post-Mortem Review:** [Quarterly incident review meeting]
**Discussion:** [Will this post-mortem be discussed in team meeting? When?]

---

## Related Incidents

**Previous Similar Incidents:**
- [INC-YYYY-MM-DD-###: Brief description, link]
- [INC-YYYY-MM-DD-###: Brief description, link]

**Pattern Detection:**
[If this is a recurring issue, note the pattern and systemic cause]

Example:
> This is the third database connection pool exhaustion incident in 6 months. Indicates need for auto-scaling connection pool implementation (action item added).

---

## Appendix

### Glossary

**[Term 1]:** [Definition for non-technical readers]
**[Term 2]:** [Definition for non-technical readers]

Example:
- **Connection Pool:** A cache of database connections maintained by the application to avoid creating a new connection for each query
- **Circuit Breaker:** A design pattern that prevents cascading failures by stopping requests to a failing service

### References

- **Runbook:** [Link to relevant runbook, e.g., RB-DB-001 Database Failover]
- **Monitoring Dashboard:** [Link to Grafana/Datadog dashboard]
- **Incident Channel:** [Link to Slack incident channel archive]
- **Related Documentation:** [Links to architecture docs, configuration guides, etc.]

---

## Sign-Off

**Approved By:**
- **Incident Commander:** @[IC name] - [Date]
- **Engineering Manager:** @[Manager name] - [Date]
- **VP Engineering:** @[VP name] - [Date] (for SEV0 only)

**Post-Mortem Meeting Held:** [Yes/No - Date and attendees]
**Document Status:** [Draft → Final → Archived]
**Archive Location:** [Link to knowledge base location]

---

## Document Changelog

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| YYYY-MM-DD | 1.0 | Initial draft | @[name] |
| YYYY-MM-DD | 1.1 | Added [section] after review | @[name] |
| YYYY-MM-DD | 2.0 | Final version approved | @[IC] |

---

**Remember:**
- **Blameless:** Focus on systems, not people
- **Specific:** Action items must be clear and actionable
- **Honest:** Psychological safety requires honesty
- **Timely:** Complete within 48 hours while memory fresh
- **Follow-Through:** Track action items to completion

**Questions?** Contact @[IC or post-mortem facilitator]
