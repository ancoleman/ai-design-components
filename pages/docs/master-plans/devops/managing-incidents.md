---
sidebar_position: 5
---

# Incident Management

Master plan for effective incident response, on-call practices, and post-incident learning. This skill covers incident lifecycle management, communication patterns, runbook development, and building resilient on-call culture.

**Status**: 🟢 Master Plan Available

## Key Topics

- **Incident Lifecycle**: Detection, triage, response, resolution, post-mortem, follow-up actions
- **Severity Classification**: Severity levels, escalation criteria, response SLAs, stakeholder communication
- **On-Call Practices**: Rotation schedules, handoffs, alert fatigue prevention, burnout avoidance
- **Incident Communication**: Status updates, stakeholder notifications, internal/external communication
- **Runbook Development**: Standardized procedures, troubleshooting guides, automated remediation
- **Post-Mortem Culture**: Blameless retrospectives, action items, knowledge sharing, learning from failure
- **Incident Tools**: Alert routing, incident tracking, war rooms, communication platforms
- **Chaos Engineering**: Proactive failure injection, resilience testing, game days

## Primary Tools & Technologies

- **Incident Management**: PagerDuty, Opsgenie, VictorOps (Splunk On-Call), Incident.io
- **Communication**: Slack, Microsoft Teams, Zoom, dedicated incident channels
- **War Rooms**: Zoom, Google Meet, dedicated Slack channels with workflows
- **Runbooks**: Confluence, Notion, GitHub Wiki, PagerDuty Runbooks
- **Post-Mortems**: Jira, Linear, GitHub Issues, dedicated post-mortem templates
- **Monitoring**: Datadog, New Relic, Grafana, CloudWatch, Prometheus
- **Log Analysis**: Splunk, ELK Stack, Loki, CloudWatch Logs
- **Chaos Engineering**: Chaos Monkey, Gremlin, Litmus Chaos, ChaosBlade

## Integration Points

- **Observability**: Monitoring and alerting trigger incidents
- **GitOps Workflows**: Automated rollbacks via GitOps
- **Building CI/CD Pipelines**: Pipeline failures trigger incidents
- **Kubernetes Operations**: K8s issues and automated remediation
- **Security Operations**: Security incidents and response
- **Platform Engineering**: Platform-assisted incident response
- **Testing Strategies**: Post-incident test creation
- **Infrastructure as Code**: Infrastructure changes during incidents

## Use Cases

- Setting up on-call rotation and escalation policies
- Creating runbooks for common incidents
- Designing incident communication workflows
- Implementing automated incident detection
- Running blameless post-mortems
- Building incident response playbooks
- Reducing alert fatigue and false positives
- Conducting chaos engineering experiments
- Training new engineers on incident response

## Decision Framework

**Severity classification:**
- **SEV-1 (Critical)**: Total outage, data loss, security breach, immediate response
- **SEV-2 (High)**: Degraded service, some users affected, response within 1 hour
- **SEV-3 (Medium)**: Limited impact, workarounds available, response within 4 hours
- **SEV-4 (Low)**: Minor issues, scheduled fixes, response within 1 business day

**On-call rotation design:**
- **Follow-the-sun**: 24/7 coverage, regional teams, no night shifts
- **Primary/Secondary**: Primary on-call, secondary escalation, shared load
- **Weekend rotation**: Separate weekend rotation, compressed schedules
- **Compensation**: On-call pay, time off, recognition, burnout prevention

**Alert design principles:**
- **Actionable**: Every alert requires human action
- **Contextual**: Include relevant debugging information
- **Prioritized**: Not all alerts are equal, route accordingly
- **Aggregated**: Group related alerts, reduce noise
- **Tested**: Validate alert accuracy, reduce false positives

**Runbook structure:**
- **Symptoms**: What the user/system is experiencing
- **Impact**: Scope and severity of the issue
- **Diagnosis**: How to confirm the issue
- **Resolution**: Step-by-step fix procedures
- **Escalation**: When and who to escalate to
- **Prevention**: Long-term fixes and action items

## Post-Mortem Best Practices

**Blameless culture:**
- Focus on system failures, not individual mistakes
- Assume good intentions and competence
- Identify systemic issues and process gaps
- Create psychological safety for honest discussion

**Post-mortem template:**
1. **Summary**: Brief incident description
2. **Timeline**: Detailed event sequence with timestamps
3. **Root Cause**: Technical and process failures
4. **Impact**: Users affected, revenue impact, SLA breaches
5. **Resolution**: What fixed the issue
6. **Action Items**: Concrete follow-up tasks with owners
7. **Lessons Learned**: What went well, what needs improvement

**Follow-up actions:**
- Track action items to completion
- Share learnings across teams
- Update runbooks and documentation
- Implement preventive measures
- Schedule follow-up review

## On-Call Health Metrics

- **Alert volume**: Alerts per shift, trending over time
- **Alert accuracy**: True positive rate, false alarm percentage
- **Response time**: Time to acknowledge, time to resolve
- **Incident frequency**: Incidents per week/month, by severity
- **Burnout indicators**: Rotation balance, weekend incidents, after-hours load
- **Runbook coverage**: Percentage of incidents with runbooks
- **Post-mortem completion**: Percentage of incidents with post-mortems
