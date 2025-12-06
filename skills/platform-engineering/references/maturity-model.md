# Platform Maturity Model

## Table of Contents

1. [Overview](#overview)
2. [Maturity Levels](#maturity-levels)
3. [Assessment Framework](#assessment-framework)
4. [Adoption Metrics](#adoption-metrics)
5. [Improvement Roadmap](#improvement-roadmap)

## Overview

The Platform Maturity Model provides a structured framework to assess current platform capabilities and chart a path toward higher maturity. Organizations progress through five levels, from ad-hoc manual processes to AI-augmented platforms.

**Purpose of the Model:**
- Assess current state across multiple dimensions
- Identify capability gaps and priorities
- Create data-driven improvement roadmap
- Benchmark against industry standards
- Communicate platform value to leadership

## Maturity Levels

### Level 0: Ad-Hoc (Pre-Platform)

**Characteristics:**
- Each team manages own infrastructure independently
- No standardization across teams or projects
- Manual provisioning and deployments
- Tribal knowledge, scattered documentation in wikis/Confluence
- Duplicate tooling and inconsistent practices
- Engineers manually configure every resource

**Challenges:**
- High cognitive load on engineers (need to know 15+ tools)
- Security and compliance gaps (no systematic enforcement)
- Slow onboarding (weeks to months for new developers)
- Difficult to scale teams or infrastructure
- Configuration drift and "snowflake" environments
- No visibility into resource costs or utilization

**Typical Timeline:**
- Startups in early stages
- Organizations that have grown rapidly without platform investment
- Companies transitioning from monolith to microservices

**Next Steps to Level 1:**
- Document common infrastructure patterns
- Introduce basic IaC for critical resources
- Set up shared monitoring and logging
- Create runbooks for common operations

### Level 1: Basic Automation

**Characteristics:**
- Some infrastructure as code (Terraform, CloudFormation)
- CI/CD pipelines for some applications
- Shared tooling (centralized logging, monitoring)
- Basic documentation (wikis, README files in repositories)
- Common patterns emerging but not enforced

**Capabilities:**
- Faster provisioning than manual (hours vs. days)
- Some consistency through shared tools
- Basic observability (logs, metrics accessible)
- Repeatable deployments for some services

**Gaps:**
- No self-service (still requires platform team tickets)
- Limited standardization (many ways to accomplish same task)
- Point solutions, not integrated platform
- Documentation scattered and often outdated
- No systematic onboarding process

**Typical Timeline:**
- Organizations 1-2 years into DevOps transformation
- Teams with 2-5 infrastructure engineers

**Next Steps to Level 2:**
- Create first golden path template for most common use case
- Set up basic developer portal (documentation hub)
- Establish service catalog (manual but centralized)
- Define platform vision and charter

### Level 2: Paved Paths (Early Platform)

**Characteristics:**
- Golden path templates for common use cases (3-5 templates)
- Service catalog with approved patterns
- Self-service for standard scenarios (via scripts or basic portal)
- Integrated developer portal (early stage, may be Backstage v1)
- Documented best practices and architecture decision records

**Capabilities:**
- Fast onboarding for standard use cases (minutes to hours)
- Consistent patterns across teams
- Self-service reduces platform team toil
- Security and compliance baked into templates
- Reduced time to first deployment

**Gaps:**
- Limited coverage (golden paths handle only 40-60% of cases)
- Escape hatches unclear or absent
- Metrics on platform usage/satisfaction informal
- Portal may be basic (primarily documentation-focused)
- Limited integration between tools

**Typical Timeline:**
- Organizations 6-12 months into platform initiative
- Platform team of 3-5 engineers

**Adoption Metrics:**
- 20-40% of teams using golden paths
- Onboarding time reduced by 50%
- 2-3 templates covering common use cases

**Next Steps to Level 3:**
- Expand template coverage to 80% of use cases
- Integrate CI/CD, monitoring, security into portal
- Implement self-service environment provisioning
- Establish platform SLOs and monitoring

### Level 3: Self-Service Platform

**Characteristics:**
- Comprehensive service catalog (100+ services documented)
- Full-featured developer portal (Backstage, Port, or commercial IDP)
- Self-service for 80%+ of use cases
- Clear escape hatches for advanced scenarios
- Automated environment provisioning (dev, staging, production)
- Integrated CI/CD, monitoring, security tools

**Capabilities:**
- Onboarding in minutes for standard cases
- Developers can provision, deploy, monitor without platform team intervention
- Consistent practices enforced through golden paths
- Platform team focuses on capabilities, not tickets
- Environment parity (dev matches prod configuration)
- Fast feedback loops (CI/CD visibility in portal)

**Monitoring:**
- Basic platform metrics (usage, adoption rate)
- Developer satisfaction surveys (quarterly)
- DORA metrics baseline established
- Template usage analytics

**Typical Timeline:**
- Organizations 12-18 months into platform maturity journey
- Platform team of 5-10 engineers

**Adoption Metrics:**
- 60-80% of teams using platform
- Self-service rate: 70-80% (actions without tickets)
- Deployment frequency: 5-10x increase
- Onboarding time: <1 day for standard services

**Next Steps to Level 4:**
- Add product manager to platform team
- Implement comprehensive DevEx metrics
- Integrate FinOps (cost visibility and optimization)
- Add advanced workflows (canary deployments, ephemeral environments)

### Level 4: Product-Driven Platform

**Characteristics:**
- Platform treated as product (product manager, roadmap, OKRs)
- Data-driven decision making (DORA, SPACE metrics)
- Platform engineering team structured as product team
- Continuous feedback loops with developer "customers"
- Advanced self-service (ephemeral environments, preview deployments)
- FinOps integration (cost visibility, budgets, optimization recommendations)
- Platform SLOs and SLIs rigorously tracked

**Capabilities:**
- Full self-service across development lifecycle
- Proactive optimization recommendations (cost, performance, security)
- Cost attribution per service/team/environment
- Advanced workflows (canary deployments, automated rollbacks)
- Policy-as-code enforcement (security, compliance)
- Platform evangelization program (internal champions)

**Measurement:**
- Comprehensive DevEx metrics (DORA + SPACE frameworks)
- Platform SLOs (uptime, latency, error rate)
- Developer NPS (Net Promoter Score) tracked quarterly
- ROI metrics (developer time saved, deployment velocity)
- Cost optimization impact ($X saved via right-sizing)

**Typical Timeline:**
- Organizations 18-36 months into platform maturity
- Platform team of 10-20 engineers (including product manager, UX designer)

**Adoption Metrics:**
- 80-95% of teams using platform
- Self-service rate: 90%+
- Developer NPS: +50 or higher
- Deployment frequency: 20x baseline
- Lead time to production: <1 hour

**Next Steps to Level 5:**
- Integrate AI-assisted capabilities
- Implement predictive analytics
- Add natural language interfaces
- Build intelligent recommendation engines

### Level 5: AI-Augmented Platform (2025+)

**Characteristics:**
- AI-assisted troubleshooting and optimization
- Predictive resource management (auto-scaling before demand)
- Automated security vulnerability remediation
- Natural language interfaces for infrastructure ("ChatOps on steroids")
- Proactive cost optimization recommendations
- Intelligent golden path suggestions based on use case analysis
- Generative templates based on requirements

**Capabilities:**
- "ChatOps" for infrastructure operations ("Deploy feature X to staging")
- Automated incident response (detection, diagnosis, remediation)
- Predictive scaling and cost forecasting
- Generative templates based on natural language requirements
- Anomaly detection (security, cost, performance)
- Self-healing infrastructure

**Advanced Measurement:**
- Real-time DevEx analytics dashboards
- Predictive platform capacity planning
- Business impact correlation (platform improvements → feature velocity → revenue)
- Automated metric collection and analysis
- Continuous optimization recommendations

**Typical Timeline:**
- Leading organizations in 2025-2026
- Platform team of 15-30 engineers (including ML/AI specialists)

**Adoption Metrics:**
- Near 100% platform adoption
- Developer NPS: +70 or higher
- AI handles 50%+ of common platform tasks
- Proactive issue resolution (before user impact)

**Emerging Capabilities:**
- Natural language infrastructure provisioning
- Automated compliance remediation
- Intelligent cost optimization (beyond simple right-sizing)
- Predictive incident prevention

## Assessment Framework

Use this framework to assess current platform maturity across multiple dimensions:

### Assessment Dimensions

**1. Self-Service Capabilities**
- Level 0: No self-service (everything manual)
- Level 1: Scripts for basic operations
- Level 2: Templates for common use cases
- Level 3: Portal-based self-service for 80% of cases
- Level 4: Advanced self-service (ephemeral envs, canary deployments)
- Level 5: AI-assisted self-service (natural language)

**2. Developer Portal**
- Level 0: No portal (scattered documentation)
- Level 1: Wiki or Confluence
- Level 2: Basic portal (documentation hub)
- Level 3: Full-featured portal (Backstage, Port)
- Level 4: Product-grade portal with analytics
- Level 5: AI-augmented portal with intelligent recommendations

**3. Golden Paths**
- Level 0: No templates
- Level 1: 1-2 informal templates
- Level 2: 3-5 documented templates
- Level 3: 10+ templates covering 80% of use cases
- Level 4: Comprehensive templates with versioning, migration support
- Level 5: Generative templates based on requirements

**4. Automation**
- Level 0: Manual provisioning and deployment
- Level 1: Some IaC and CI/CD
- Level 2: Automated standard workflows
- Level 3: Comprehensive automation
- Level 4: Proactive automation (policy-as-code, auto-remediation)
- Level 5: AI-driven automation

**5. Observability**
- Level 0: Ad-hoc logging
- Level 1: Centralized logging and basic metrics
- Level 2: Metrics, logs, traces for most services
- Level 3: Integrated observability in portal
- Level 4: Advanced analytics, cost visibility
- Level 5: Predictive analytics, anomaly detection

**6. Platform Team Structure**
- Level 0: No dedicated platform team
- Level 1: 1-2 infrastructure engineers
- Level 2: 3-5 platform engineers
- Level 3: 5-10 platform engineers
- Level 4: Product team structure (PM, engineers, UX)
- Level 5: Large team (15-30+) with specialists

### Assessment Worksheet

For each dimension, rate current state (0-5) and identify gaps:

```
Dimension: Self-Service Capabilities
Current Level: 2 (Templates for common use cases)
Target Level: 3 (Portal-based self-service)
Gap: Need to build developer portal and expand template coverage
Priority: High
Estimated Effort: 3-6 months
```

Repeat for all dimensions, then prioritize gaps based on:
- Business impact (developer productivity, time-to-market)
- Effort required (team capacity, dependencies)
- Risk mitigation (security, compliance)

## Adoption Metrics

Track these metrics to measure platform maturity and adoption:

### Primary Metrics

**1. Platform Adoption Rate**
- Definition: Percentage of engineering teams using platform
- Calculation: (Teams using platform / Total teams) × 100
- Targets:
  - Level 2: 20-40%
  - Level 3: 60-80%
  - Level 4: 80-95%
  - Level 5: 95-100%

**2. Self-Service Rate**
- Definition: Percentage of platform actions completed without platform team tickets
- Calculation: (Self-service actions / Total actions) × 100
- Targets:
  - Level 2: 40-60%
  - Level 3: 70-80%
  - Level 4: 90%+
  - Level 5: 95%+

**3. Onboarding Time**
- Definition: Time from new developer account to first production deployment
- Measurement: Track via surveys or automated telemetry
- Targets:
  - Level 0: Weeks to months
  - Level 1: Days to weeks
  - Level 2: Hours to days
  - Level 3: <1 day
  - Level 4: <4 hours
  - Level 5: <1 hour

**4. Template Usage Rate**
- Definition: Percentage of new services created via golden paths
- Calculation: (Services from templates / Total new services) × 100
- Targets:
  - Level 2: 40-60%
  - Level 3: 70-80%
  - Level 4: 85%+

### DORA Metrics

**1. Deployment Frequency**
- How often code reaches production
- Targets:
  - Level 0-1: Weekly to monthly
  - Level 2: Daily
  - Level 3: Multiple times per day
  - Level 4: On-demand (10+ per day)
  - Level 5: Continuous (50+ per day)

**2. Lead Time for Changes**
- Commit to production duration
- Targets:
  - Level 0-1: Weeks to months
  - Level 2: Days to weeks
  - Level 3: Hours to days
  - Level 4: <1 day
  - Level 5: <1 hour

**3. Mean Time to Recovery (MTTR)**
- Time to restore service after incident
- Targets:
  - Level 0-1: Hours to days
  - Level 2: Hours
  - Level 3: <1 hour
  - Level 4: <30 minutes
  - Level 5: <15 minutes (automated recovery)

**4. Change Failure Rate**
- Percentage of deployments causing incidents
- Targets:
  - Level 0-1: 20-40%
  - Level 2: 10-20%
  - Level 3: 5-10%
  - Level 4: <5%
  - Level 5: <2%

### Developer Satisfaction Metrics

**1. Developer NPS (Net Promoter Score)**
- Survey question: "How likely are you to recommend this platform to colleagues?"
- Scale: 0-10 (Detractors: 0-6, Passives: 7-8, Promoters: 9-10)
- Calculation: % Promoters - % Detractors
- Targets:
  - Level 2: +10 to +20
  - Level 3: +30 to +40
  - Level 4: +50 to +60
  - Level 5: +70+

**2. Platform Support Ticket Volume**
- Track tickets to platform team
- Trend should decrease as self-service improves
- Targets:
  - Level 3: 50% reduction from baseline
  - Level 4: 75% reduction
  - Level 5: 90% reduction

### Cost Metrics

**1. Cost per Deploy**
- Infrastructure cost divided by deployment count
- Should decrease as automation improves

**2. Cost Visibility**
- Percentage of resources with cost attribution
- Targets:
  - Level 3: 50%
  - Level 4: 90%+
  - Level 5: 100%

**3. Cost Optimization Realized**
- Dollars saved via right-sizing, resource cleanup
- Track quarterly

## Improvement Roadmap

### Creating a Maturity Roadmap

**Step 1: Assess Current State**
1. Complete assessment worksheet for all dimensions
2. Identify current maturity level per dimension
3. Calculate overall platform maturity (average or weighted)
4. Gather baseline metrics (DORA, adoption, NPS)

**Step 2: Define Target State**
1. Set target maturity level (typically current + 1 or 2 levels)
2. Define success criteria for each dimension
3. Set target metrics (DORA, adoption, NPS)
4. Establish timeline (6-12 months for one level, 12-24 for two)

**Step 3: Identify Gaps and Priorities**
1. List capability gaps between current and target
2. Prioritize by: Business impact, effort, risk
3. Group into themes (portal, automation, templates, metrics)
4. Sequence based on dependencies

**Step 4: Build Roadmap**
1. Divide into phases (Foundation, Pilot, Expansion, Maturity)
2. Assign initiatives to phases
3. Estimate effort and assign ownership
4. Define success metrics for each phase

**Step 5: Execute and Iterate**
1. Start with Foundation phase (vision, team, quick wins)
2. Pilot with 2-3 teams, gather feedback
3. Expand based on learnings
4. Measure continuously, adjust roadmap quarterly

### Sample Roadmap: Level 1 → Level 3 (12-18 months)

**Phase 1: Foundation (Months 1-3)**
- Form platform team (3-5 engineers)
- Define platform vision and charter
- Set up basic developer portal (Backstage)
- Create first golden path template (most common use case)
- Establish baseline metrics (DORA, onboarding time)

**Phase 2: Pilot (Months 4-6)**
- Onboard 2-3 pilot teams
- Create 3-5 golden path templates
- Integrate CI/CD into portal
- Add service catalog (100 services documented)
- Weekly feedback sessions, rapid iteration

**Phase 3: Expansion (Months 7-12)**
- Scale to 20-50% of teams
- Expand to 10+ golden path templates
- Integrate observability, security, secrets management
- Establish platform SLOs
- Self-service documentation and training
- Internal evangelization (demos, champions)

**Phase 4: Optimization (Months 13-18)**
- 60-80% adoption across organization
- Advanced features (ephemeral environments)
- Policy-as-code enforcement (OPA, Kyverno)
- Platform analytics and dashboards
- Continuous improvement based on metrics

**Target Metrics (18 months):**
- Platform adoption: 70%
- Self-service rate: 75%
- Onboarding time: <1 day
- Deployment frequency: 5-10x baseline
- Developer NPS: +30

### Common Roadblocks and Mitigations

**Roadblock 1: Lack of Executive Buy-In**
- Mitigation: Build business case with ROI projections
- Show competitor benchmarks (platform maturity correlation with business outcomes)
- Start small with pilot team, demonstrate quick wins

**Roadblock 2: Platform Team Resource Constraints**
- Mitigation: Start with 2-3 engineers, scale gradually
- Use commercial IDP for faster time-to-value
- Community contributions (hub-and-spoke model)

**Roadblock 3: Low Developer Adoption**
- Mitigation: Make platform easier than alternatives
- White-glove onboarding for pilot teams
- Internal evangelization and champions program
- Rapid response to feedback

**Roadblock 4: Over-Engineering**
- Mitigation: Start with 1 golden path, iterate
- Avoid "boil the ocean" syndrome
- Measure usage, expand based on demand

**Roadblock 5: Resistance to Standardization**
- Mitigation: Provide clear escape hatches
- Balance flexibility and standardization
- Engage senior engineers in platform design
