# Incident Roles and Responsibilities


## Table of Contents

- [Overview](#overview)
- [Core Principle](#core-principle)
- [Incident Commander (IC)](#incident-commander-ic)
  - [Primary Responsibilities](#primary-responsibilities)
  - [What IC Does NOT Do](#what-ic-does-not-do)
  - [Required Skills](#required-skills)
  - [Selection Criteria](#selection-criteria)
  - [IC Rotation](#ic-rotation)
  - [IC Decision Authority](#ic-decision-authority)
- [Communications Lead](#communications-lead)
  - [Primary Responsibilities](#primary-responsibilities)
  - [When to Assign Communications Lead](#when-to-assign-communications-lead)
  - [Required Skills](#required-skills)
  - [Communication Cadence](#communication-cadence)
- [Subject Matter Experts (SMEs)](#subject-matter-experts-smes)
  - [Primary Responsibilities](#primary-responsibilities)
  - [Role Assignment](#role-assignment)
  - [SME Coordination with IC](#sme-coordination-with-ic)
  - [Required Skills](#required-skills)
- [Scribe](#scribe)
  - [Primary Responsibilities](#primary-responsibilities)
  - [When to Assign Scribe](#when-to-assign-scribe)
  - [Documentation Format](#documentation-format)
  - [Required Skills](#required-skills)
- [Supporting Roles (As Needed)](#supporting-roles-as-needed)
  - [Executive Liaison](#executive-liaison)
  - [Legal/Compliance Liaison](#legalcompliance-liaison)
  - [Vendor Coordinator](#vendor-coordinator)
- [Role Handoff Procedures](#role-handoff-procedures)
  - [IC Handoff (Long Incidents > 4 Hours)](#ic-handoff-long-incidents-4-hours)
  - [SME Handoff](#sme-handoff)
- [Role Training and Drills](#role-training-and-drills)
  - [IC Training Program](#ic-training-program)
  - [Communication Lead Training](#communication-lead-training)
  - [SME Readiness](#sme-readiness)
- [Role Assignment Matrix](#role-assignment-matrix)
- [Anti-Patterns](#anti-patterns)
  - [IC Doing Hands-On Debugging](#ic-doing-hands-on-debugging)
  - [No Clear IC Assignment](#no-clear-ic-assignment)
  - [Communications Lead Speculating on Root Cause](#communications-lead-speculating-on-root-cause)
  - [SME Withholding Context from IC](#sme-withholding-context-from-ic)
  - [Scribe Editorializing](#scribe-editorializing)
- [Role Evolution](#role-evolution)
  - [Small Teams (5-10 Engineers)](#small-teams-5-10-engineers)
  - [Medium Teams (10-50 Engineers)](#medium-teams-10-50-engineers)
  - [Large Teams (50+ Engineers)](#large-teams-50-engineers)
- [Post-Incident Role Evaluation](#post-incident-role-evaluation)
- [Further Reading](#further-reading)

## Overview

Clear role definition during incidents prevents confusion, ensures coordination, and accelerates resolution. Roles are adapted from the Incident Command System (ICS), proven in emergency response and adapted for technology incidents.

## Core Principle

**Separation of Concerns:** Strategic coordination (IC) is distinct from tactical execution (SMEs). No single person should both command and execute.

---

## Incident Commander (IC)

### Primary Responsibilities

**Strategic Coordination:**
- Own overall incident response from declaration to closure
- Make high-level decisions (rollback vs. debug, escalate vs. continue)
- Delegate tasks to Subject Matter Experts (SMEs)
- Coordinate between teams if multi-team incident
- Declare incident resolved when stability confirmed

**Communication Management:**
- Ensure regular status updates posted (delegate to Communications Lead for SEV0)
- Brief stakeholders on incident progress
- Coordinate with executive leadership if needed
- Call post-mortem meeting within 48 hours

**Resource Allocation:**
- Request additional responders if needed
- Manage on-call escalations
- Coordinate with external vendors if third-party involved

### What IC Does NOT Do

**No Hands-On Debugging:** IC delegates technical work to SMEs. IC stays "above the water" to maintain strategic view.

**No Communication Execution:** For SEV0, delegate status updates to Communications Lead. IC focuses on coordination.

**No Firefighting:** IC is not "the hero." IC enables the team to be effective.

### Required Skills

- **Leadership:** Ability to coordinate under pressure
- **Decision-Making:** Make strategic calls with incomplete information
- **Communication:** Clear, concise updates to technical and non-technical audiences
- **Technical Context:** Understand systems enough to ask right questions (but not necessarily hands-on expert)

### Selection Criteria

**SEV0/SEV1:**
- Senior engineer or team lead
- On-call rotation or designated IC pool
- Training: IC training workshop, simulation exercises

**SEV2:**
- Primary on-call engineer can self-assign IC role
- Optional: Escalate to senior IC if incident complexity increases

### IC Rotation

**Dedicated IC Pool (Large Organizations):**
- 5-10 senior engineers trained as ICs
- 1-week IC rotation separate from on-call
- IC does NOT debug, only coordinates

**Combined On-Call + IC (Small Teams):**
- Senior on-call acts as IC
- May do both coordination and hands-on work for SEV2
- Escalate to separate IC for SEV0/SEV1

### IC Decision Authority

**IC Has Authority To:**
- Declare incident and assign severity
- Escalate or de-escalate severity
- Request resources (additional engineers, vendor support)
- Make rollback/rollforward decisions
- Declare incident resolved
- Schedule post-mortem

**IC Should Consult For:**
- Major architectural changes during incident (discuss with team lead)
- Customer communication language (consult Communications Lead)
- Legal/compliance implications (involve legal team)
- Significant cost decisions (e.g., scaling infrastructure 10x)

---

## Communications Lead

### Primary Responsibilities

**Internal Communication:**
- Post status updates to incident Slack channel every 15-30 minutes (SEV0/SEV1)
- Update stakeholders: executives, product, support, sales
- Coordinate with on-call managers for escalations
- Maintain real-time incident timeline

**External Communication:**
- Post updates to public status page (Statuspage.io, Instatus, etc.)
- Draft customer-facing incident emails
- Coordinate social media updates (if applicable)
- Handle regulatory notifications (GDPR, HIPAA, etc.)

**Stakeholder Management:**
- Brief executives on customer impact and ETA
- Update support team for customer ticket handling
- Coordinate with sales for enterprise customer outreach
- Provide product team with feature impact assessment

### When to Assign Communications Lead

**SEV0:** Always assign dedicated Communications Lead (frees IC to focus on coordination)

**SEV1:** Optional, depends on incident complexity and duration
- Assign if incident > 1 hour duration
- Assign if high stakeholder interest (executive visibility, major customer impact)

**SEV2/SEV3:** Not needed (IC or single responder handles communication)

### Required Skills

- **Clear Writing:** Ability to explain technical issues in simple language
- **Empathy:** Understanding of customer frustration and anxiety
- **Stakeholder Management:** Balance transparency with avoiding over-promising
- **Timeliness:** Post updates on schedule, even if "no new information"

### Communication Cadence

**SEV0:**
- Internal updates: Every 15 minutes
- External status page: Every 15-30 minutes
- Executive brief: Every 30 minutes or at major milestones

**SEV1:**
- Internal updates: Every 30 minutes
- External status page: Every 30-60 minutes
- Executive brief: At incident start and resolution

**Templates:**
See `examples/communication-templates.md` for status update and email templates.

---

## Subject Matter Experts (SMEs)

### Primary Responsibilities

**Hands-On Technical Work:**
- Debug issues, review logs, analyze metrics
- Execute runbooks and remediation steps
- Implement mitigation (rollback, traffic shift, failover)
- Test fixes and verify resolution
- Provide technical context to IC

**Knowledge Sharing:**
- Explain technical findings to IC in plain language
- Document actions taken in incident timeline
- Recommend next steps based on expertise
- Identify when escalation to other specialists needed

### Role Assignment

**Primary SME:**
- On-call engineer, first responder
- Deep knowledge of affected system

**Secondary SME:**
- Backup on-call or specialist
- Called in if primary SME stuck or needs specific expertise

**Specialist SME:**
- Database expert, network engineer, security specialist
- Escalated to when specialized knowledge required

### SME Coordination with IC

**Report to IC:**
- "We've identified the issue: database connection pool exhausted"
- "Implementing mitigation: increasing pool size from 100 to 200"
- "Mitigation complete, monitoring for 10 minutes to confirm stability"

**Request from IC:**
- "Do we need to page the database team, or can you handle this?"
- "What's your confidence level in this fix?"
- "If this doesn't work, what's Plan B?"

### Required Skills

- **Deep Technical Expertise:** Expert in specific system or domain
- **Troubleshooting:** Systematic debugging approach
- **Communication:** Explain complex technical issues clearly
- **Runbook Execution:** Follow documented procedures accurately

---

## Scribe

### Primary Responsibilities

**Real-Time Documentation:**
- Record timeline of events (detection, actions, decisions)
- Capture key decisions made by IC
- Document changes deployed during incident
- Note external dependencies or blockers
- Track responders involved and their contributions

**Post-Incident Support:**
- Provide incident notes for post-mortem
- Share timeline with post-mortem facilitator
- Help reconstruct sequence of events

### When to Assign Scribe

**SEV0:** Always assign dedicated Scribe (critical for post-mortem accuracy)

**SEV1:** Optional
- Assign if incident > 2 hours
- Assign if complex multi-team coordination

**SEV2/SEV3:** Not needed (incident platform logs sufficient)

### Documentation Format

**Incident Timeline (Example):**

```
14:15 - Alert: "API Error Rate High" detected
14:17 - @alice (on-call) acknowledged alert, investigating
14:20 - @alice: Identified database connection pool saturation
14:20 - Incident declared SEV1, @bob assigned as IC
14:25 - IC decision: Increase connection pool from 100 → 200
14:27 - @alice deployed connection pool increase
14:30 - Error rate dropped from 15% → 5%
14:35 - @alice: Found secondary issue - retry logic causing thundering herd
14:40 - IC decision: Disable aggressive retry, enable circuit breaker
14:45 - @alice deployed circuit breaker config
14:50 - Error rate returned to baseline (<0.1%)
15:00 - IC: Monitoring for stability (30 min observation)
15:30 - IC: Incident resolved, service stable
```

**Tools:**
- Shared Google Doc (real-time collaboration)
- Incident management platform notes (PagerDuty, incident.io)
- Slack channel pins (pinned timeline post)

### Required Skills

- **Fast Typing:** Keep up with real-time incident updates
- **Active Listening:** Capture important details from war room discussions
- **Attention to Detail:** Accurate timestamps and action recording
- **Neutrality:** Document facts, not opinions or blame

---

## Supporting Roles (As Needed)

### Executive Liaison

**When:** SEV0 with major business impact (CEO/board visibility)

**Responsibilities:**
- Brief C-level on incident status
- Translate technical details to business impact
- Manage investor/media inquiries
- Coordinate customer VIP outreach

**Assigned By:** IC escalates to VP Engineering or CTO

---

### Legal/Compliance Liaison

**When:** Security incidents, data breaches, regulatory violations

**Responsibilities:**
- Advise on legal obligations (notification timelines)
- Coordinate with external legal counsel
- Manage regulatory notifications (GDPR, HIPAA, PCI)
- Preserve forensic evidence

**Assigned By:** IC notifies legal team immediately

---

### Vendor Coordinator

**When:** Third-party service degradation (AWS, Stripe, Twilio)

**Responsibilities:**
- Open support tickets with vendor
- Escalate through vendor TAM (Technical Account Manager)
- Relay vendor updates to IC
- Coordinate vendor-provided fixes

**Assigned By:** IC or SME identifies vendor dependency

---

## Role Handoff Procedures

### IC Handoff (Long Incidents > 4 Hours)

**Outgoing IC:**
- Brief incoming IC on current status
- Share incident channel, timeline, key decisions
- Introduce to SMEs and Communications Lead
- Announce handoff in incident channel

**Incoming IC:**
- Review timeline and current actions
- Confirm understanding with outgoing IC
- Announce taking over IC role in channel
- Continue response with fresh perspective

**When to Handoff:**
- Incident duration > 4 hours (fatigue risk)
- Shift change (follow-the-sun)
- Incoming IC has greater expertise for incident type

### SME Handoff

**Outgoing SME:**
- Summarize actions taken and current hypothesis
- Share relevant logs, metrics, runbooks
- Highlight blockers or pending decisions
- Announce handoff to IC

**Incoming SME:**
- Pair with outgoing SME for 5-10 minutes
- Review current system state
- Continue debugging from handoff point

---

## Role Training and Drills

### IC Training Program

**Components:**
1. **ICS Overview:** Incident Command System principles (2-hour workshop)
2. **Decision-Making Under Pressure:** Simulated incident exercises
3. **Communication Skills:** Stakeholder updates, executive briefings
4. **Tooling:** Hands-on with PagerDuty, Slack, status pages
5. **Shadowing:** Observe experienced IC during real incident

**Frequency:** Annual refresher training, quarterly simulation drills

### Communication Lead Training

**Components:**
1. **Writing for Clarity:** Technical to non-technical translation
2. **Stakeholder Management:** Balancing transparency and reassurance
3. **Template Usage:** Practice with status update and email templates
4. **Regulatory Requirements:** GDPR, HIPAA notification rules (if applicable)

**Frequency:** Semi-annual training

### SME Readiness

**Prerequisites:**
- Deep system knowledge through daily work
- Runbook familiarity (review monthly)
- Access verification (VPN, dashboards, deployment tools)
- On-call training (alerting, escalation)

**Ongoing:** Runbook review every sprint, DR drills monthly

---

## Role Assignment Matrix

| Severity | IC | Communications Lead | SME | Scribe |
|----------|-----|---------------------|-----|--------|
| SEV0 | Senior Engineer/Lead | Required | Multiple SMEs | Required |
| SEV1 | Senior On-Call | Optional (if > 1hr) | 1-2 SMEs | Optional (if > 2hr) |
| SEV2 | Primary On-Call (self-assigned) | Not needed | Primary On-Call | Not needed |
| SEV3 | Not assigned | Not needed | Assignee | Not needed |

---

## Anti-Patterns

### IC Doing Hands-On Debugging

**Problem:** IC loses strategic view while deep in logs, coordination suffers.

**Solution:** IC delegates all debugging to SMEs, stays focused on coordination.

---

### No Clear IC Assignment

**Problem:** Multiple people leading, confusion about decisions, slower resolution.

**Solution:** Explicitly assign IC at incident declaration, announce in channel.

---

### Communications Lead Speculating on Root Cause

**Problem:** External communication promises fix ETA, root cause later found to be different.

**Solution:** Stick to facts, avoid speculation. "Investigating" vs. "Identified" distinction.

---

### SME Withholding Context from IC

**Problem:** SME knows issue severity increased but doesn't inform IC, delayed escalation.

**Solution:** SMEs continuously update IC on findings, confidence level, blockers.

---

### Scribe Editorializing

**Problem:** Scribe adds opinions ("@alice made a bad decision") instead of facts.

**Solution:** Document actions and outcomes, not judgments. Save analysis for post-mortem.

---

## Role Evolution

### Small Teams (5-10 Engineers)

- **IC:** Senior on-call also acts as IC (combined role)
- **SME:** Primary on-call does hands-on work
- **Communications Lead:** IC handles communication
- **Scribe:** Not assigned (incident platform logs sufficient)

### Medium Teams (10-50 Engineers)

- **IC:** Dedicated IC pool (5-7 trained engineers)
- **SME:** Primary + secondary on-call
- **Communications Lead:** Assigned for SEV1+
- **Scribe:** Assigned for SEV0

### Large Teams (50+ Engineers)

- **IC:** Full-time IC rotation (not on on-call)
- **SME:** Multiple SMEs per incident (database, network, app)
- **Communications Lead:** Dedicated role for all SEV1+
- **Scribe:** Assigned for all SEV1+
- **Support Roles:** Legal liaison, executive liaison, vendor coordinator

---

## Post-Incident Role Evaluation

After each SEV0/SEV1, review role effectiveness:

**Questions:**
- Was IC able to focus on coordination, or pulled into debugging?
- Did Communications Lead post updates on schedule?
- Were SMEs able to troubleshoot effectively?
- Was Scribe timeline accurate and complete?
- Were handoffs smooth (if applicable)?

**Improvements:**
- Update role descriptions based on learnings
- Provide additional training if gaps identified
- Adjust role assignment criteria
- Document role-specific best practices

---

## Further Reading

- FEMA: "Incident Command System (ICS) Overview"
- Google SRE Book: "Managing Incidents" (Chapter 14)
- PagerDuty: "Incident Response Roles and Responsibilities"
- FireHydrant: "Incident Command Structure for Tech"
