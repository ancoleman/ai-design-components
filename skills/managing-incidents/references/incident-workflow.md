# Incident Response Workflow


## Table of Contents

- [Overview](#overview)
- [Incident Lifecycle Stages](#incident-lifecycle-stages)
- [Stage Details](#stage-details)
  - [1. Detection](#1-detection)
  - [2. Triage & Severity Assignment](#2-triage-severity-assignment)
  - [3. Incident Declaration](#3-incident-declaration)
  - [4. Investigation & Diagnosis](#4-investigation-diagnosis)
  - [5. Mitigation](#5-mitigation)
  - [6. Resolution](#6-resolution)
  - [7. Monitoring](#7-monitoring)
  - [8. Closure](#8-closure)
  - [9. Post-Mortem](#9-post-mortem)
- [Decision Points](#decision-points)
  - [When to Declare Incident](#when-to-declare-incident)
  - [When to Escalate](#when-to-escalate)
  - [When to Close](#when-to-close)
- [Workflow Variations](#workflow-variations)
  - [SEV0 Workflow (All Hands)](#sev0-workflow-all-hands)
  - [SEV2 Workflow (Single Responder)](#sev2-workflow-single-responder)
  - [SEV3 Workflow (Ticket)](#sev3-workflow-ticket)
- [Communication During Workflow](#communication-during-workflow)
  - [Status Update Frequency](#status-update-frequency)
  - [Update Template](#update-template)
  - [External Communication](#external-communication)
- [Workflow Anti-Patterns](#workflow-anti-patterns)
- [Further Reading](#further-reading)

## Overview

Standard incident lifecycle from detection through post-mortem. Follow this workflow to ensure consistent, effective incident response.

## Incident Lifecycle Stages

```
1. Detection
   ↓
2. Triage & Severity Assignment
   ↓
3. Incident Declaration
   ↓
4. Investigation & Diagnosis
   ↓
5. Mitigation
   ↓
6. Resolution
   ↓
7. Monitoring
   ↓
8. Closure
   ↓
9. Post-Mortem
```

## Stage Details

### 1. Detection

**Sources:**
- Automated alerts (Prometheus, Datadog, CloudWatch)
- Customer reports (support tickets, social media)
- Synthetic monitoring (uptime checks)
- Internal discovery (engineer notices issue)

**Actions:**
- Alert fires to on-call via PagerDuty/Opsgenie
- On-call acknowledges within 5 minutes (MTTA target)

### 2. Triage & Severity Assignment

**On-Call Assesses:**
- What is broken?
- How many customers affected?
- Is core functionality impacted?
- Is there a workaround?

**Assign Severity:** SEV0, SEV1, SEV2, or SEV3 (use `python scripts/classify-severity.py`)

### 3. Incident Declaration

**For SEV1/SEV0:**
- Create incident Slack channel: `#incident-YYYY-MM-DD-topic`
- Assign Incident Commander (IC)
- Post initial status: Severity, IC, brief description
- Update status page: "Investigating"

**Slack Command:**
```
/incident-declare SEV1 API experiencing elevated error rates
```

### 4. Investigation & Diagnosis

**IC Coordinates:**
- SMEs investigate logs, metrics, recent changes
- Runbooks consulted if known failure scenario
- Hypothesis formed about root cause

**Key Questions:**
- When did this start?
- What changed recently (deploys, config, traffic)?
- Which systems are affected?

**IC Decision:** Enough info to mitigate? If yes → Mitigation. If no → Continue investigation.

### 5. Mitigation

**Goal:** Stop customer impact ASAP (not fix root cause).

**Common Mitigations:**
- Rollback recent deploy
- Disable feature flag
- Failover to secondary database
- Scale up infrastructure
- Rate limit traffic
- Enable maintenance mode

**IC Announces:** "Mitigation deployed: [action]. Monitoring for impact reduction."

### 6. Resolution

**Goal:** Fix root cause permanently.

**Actions:**
- Deploy permanent fix (if mitigation was temporary)
- Verify fix resolves issue
- Test affected functionality

**Example:** Mitigation was rollback → Resolution is fixing bug and deploying fixed version.

### 7. Monitoring

**Duration:** 30+ minutes of stability before closure.

**Monitor:**
- Error rates returned to baseline
- Latency normal
- No new customer reports
- All metrics green

**IC Decision:** If stable → Proceed to Closure. If unstable → Return to Investigation.

### 8. Closure

**IC Declares Resolved:**
- Post in incident channel: "Incident resolved at [timestamp]"
- Update status page: "Resolved"
- Thank responders
- Schedule post-mortem (within 48 hours)

**Closure Criteria:**
- Issue resolved and stable for 30+ minutes
- Monitoring confirms normal metrics
- No customer-reported issues
- IC confident in stability

### 9. Post-Mortem

**Timeline:** Within 48 hours of resolution.

**Process:**
- IC schedules post-mortem meeting
- Scribe creates post-mortem document (use `examples/postmortem-template.md`)
- Team conducts blameless review
- Action items defined with owners and due dates

For detailed post-mortem facilitation process, consult the blameless post-mortems guide.

## Decision Points

### When to Declare Incident

**Declare if:**
- Customer-facing impact occurring
- Production issue requiring multiple people
- Severity SEV1 or higher
- Uncertain about impact (declare, can always downgrade)

**Do NOT wait for certainty.** Declaring enables coordination.

### When to Escalate

**Escalate if:**
- No progress after 30 minutes
- Severity increases (SEV2 → SEV1)
- Specialized expertise needed (database, security)
- Incident extends beyond expected timeframe

Consult the escalation matrix for detailed escalation paths and contacts.

### When to Close

**Close when:**
- Issue resolved and stable for 30+ minutes
- Monitoring shows baseline metrics
- No customer-reported issues
- IC confirms no further action needed

**Do NOT close prematurely.** Closing too early risks recurrence.

## Workflow Variations

### SEV0 Workflow (All Hands)

1. Detection → Immediate page to all hands
2. Declare SEV0 → Assign IC, Communications Lead, Scribe
3. War room → Video call for real-time coordination
4. Executive notification → Within 15 minutes
5. Status updates → Every 15 minutes
6. Post-mortem → Within 24 hours (faster than normal)

### SEV2 Workflow (Single Responder)

1. Detection → Alert to on-call
2. Single responder investigates → No IC needed
3. Fix applied → Standard response
4. Update status page if customer-visible
5. Post-mortem optional (recommended if novel issue)

### SEV3 Workflow (Ticket)

1. Detection → Create ticket, no alert
2. Triage → Assign to backlog
3. Plan fix → Next sprint
4. No post-mortem → Track in regular sprint retrospective

## Communication During Workflow

### Status Update Frequency

- **SEV0:** Every 15 minutes
- **SEV1:** Every 30 minutes
- **SEV2:** At major milestones

### Update Template

```
[TIMESTAMP] Update #[N] - [Status]

Current Status: [Investigating | Identified | Implementing Fix | Monitoring]
Issue: [One-sentence description]
Impact: [Who/what affected]
Progress: [What we've learned/done]
Next Steps: [What we're doing next]
ETA: [Expected resolution or "Unknown"]
Next Update: [TIMESTAMP]
```

### External Communication

- Status page updated: Investigating → Identified → Monitoring → Resolved
- Customer email: Post-resolution (within 24 hours for SEV0/SEV1)

## Workflow Anti-Patterns

**Delayed Declaration:**
- Waiting for certainty before declaring
- Fix: Declare early, can always downgrade

**IC Doing Hands-On Debugging:**
- IC loses strategic view
- Fix: IC delegates all debugging to SMEs

**No Status Updates:**
- Stakeholders uninformed, anxiety increases
- Fix: Set timer for regular updates

**Premature Closure:**
- Closing before confirming stability
- Fix: Monitor for 30+ minutes before closure

## Further Reading

- Google SRE Book: "Managing Incidents" (Chapter 14)
- PagerDuty: "Incident Response Process"
- Atlassian: "Incident Management Best Practices"
