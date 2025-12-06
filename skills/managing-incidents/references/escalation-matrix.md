# Escalation Matrix


## Table of Contents

- [Overview](#overview)
- [Escalation Decision Matrix](#escalation-decision-matrix)
- [Escalation Triggers](#escalation-triggers)
  - [Time-Based Escalation](#time-based-escalation)
  - [Severity-Based Escalation](#severity-based-escalation)
  - [Expertise-Based Escalation](#expertise-based-escalation)
- [Escalation Contacts](#escalation-contacts)
  - [On-Call Hierarchy](#on-call-hierarchy)
  - [Specialized Escalation Paths](#specialized-escalation-paths)
- [Escalation Communication](#escalation-communication)
  - [Internal Notification](#internal-notification)
  - [Executive Notification](#executive-notification)
- [Avoiding Over-Escalation](#avoiding-over-escalation)
- [Further Reading](#further-reading)

## Overview

Escalation ensures incidents get appropriate resources and attention based on duration, complexity, and impact. This matrix defines when and how to escalate incidents.

## Escalation Decision Matrix

| Time Since Start | No Progress | Severity Increase | Expertise Needed | Action |
|------------------|-------------|-------------------|------------------|---------|
| < 15 minutes | Primary on-call | - | - | Continue investigation |
| 15-30 minutes | Secondary on-call | SEV2 → SEV1 | Specialist (DB, Network) | Escalate to secondary |
| 30-60 minutes | Team Lead | SEV1 → SEV0 | Architect | Escalate to team lead |
| 60+ minutes | Director/VP Eng | - | Senior leadership | Escalate to director |

## Escalation Triggers

### Time-Based Escalation

**15 Minutes - No Acknowledgment:**
- Primary on-call hasn't acknowledged alert
- Auto-escalate to secondary on-call via PagerDuty/Opsgenie

**30 Minutes - No Progress:**
- Investigation ongoing but no mitigation path identified
- Escalate to team lead or senior engineer for guidance

**60 Minutes - Extended Duration:**
- Incident unresolved after 1 hour
- Escalate to engineering manager or director
- Consider declaring SEV0 if customer impact severe

### Severity-Based Escalation

**SEV2 → SEV1:**
- Impact expands (5% → 25% of customers)
- Escalate to team lead, assign IC

**SEV1 → SEV0:**
- Complete outage or critical functionality lost
- Escalate to VP Engineering, notify executives

### Expertise-Based Escalation

**Database Issues:**
- Escalate to @db-team within 15 minutes if database-related

**Network/Infrastructure:**
- Escalate to @infra-team if network or infrastructure issue

**Security Incident:**
- Escalate to @security-team immediately for security issues

**Third-Party Vendor:**
- Open vendor support ticket within 15 minutes
- Escalate through TAM (Technical Account Manager) if available

## Escalation Contacts

### On-Call Hierarchy

```
Primary On-Call
    ↓ (5 min no ack)
Secondary On-Call
    ↓ (15 min no resolution)
Team Lead / Senior Engineer
    ↓ (30 min no resolution OR SEV0)
Engineering Manager
    ↓ (60 min OR high business impact)
Director / VP Engineering
```

### Specialized Escalation Paths

**Database:**
- Primary: @db-oncall
- Secondary: @senior-dba
- Escalation: @db-team-lead

**Security:**
- Primary: @security-oncall
- Immediate: @security-team-lead (for all security incidents)
- Legal: @legal-team (for data breaches)

**Infrastructure:**
- Primary: @infra-oncall
- Secondary: @sre-team
- Escalation: @infra-lead

## Escalation Communication

### Internal Notification

When escalating, post in incident channel:
```
@team-lead Escalating to you - no progress after 30 minutes.
Current status: [Brief summary]
Need: [Specific help needed]
```

### Executive Notification

For SEV0 incidents, notify executives within 15 minutes:
- **Who to notify:** CTO, VP Engineering, CEO (for major outages)
- **How:** Slack DM + brief email
- **What to include:** Business impact, ETA, current actions

**Executive Brief Template:**
```
SEV0 Incident: [Title]
Duration: [X minutes]
Impact: [Y% of customers unable to [action]]
Current Status: [Investigating/Mitigating]
ETA: [Best estimate or "Unknown"]
IC: @[name]
```

## Avoiding Over-Escalation

**Do NOT escalate if:**
- Issue being actively mitigated
- Clear path to resolution identified
- Escalation would distract without adding value

**Example:** Database slow, root cause identified, mitigation in progress → Do NOT escalate unless mitigation fails.

## Further Reading

- PagerDuty: "Escalation Policies Best Practices"
- Google SRE: "Incident Management"
