# Platform Engineering Decision Frameworks

## Table of Contents

1. [Build vs. Buy IDP Decision Matrix](#build-vs-buy-idp-decision-matrix)
2. [Golden Path Design: Flexibility vs. Standardization](#golden-path-design-flexibility-vs-standardization)
3. [Platform Adoption Strategy](#platform-adoption-strategy)
4. [Platform Team Structure](#platform-team-structure)

## Build vs. Buy IDP Decision Matrix

### When to Build Custom Platform

**Indicators:**
- ✅ Unique requirements not met by commercial/open-source solutions
- ✅ Large engineering organization (1000+ engineers) with dedicated platform team (10+ engineers)
- ✅ Strong internal expertise in platform technologies (Kubernetes, IaC, CI/CD)
- ✅ Need for deep customization and control
- ✅ Open-source ecosystem preference (avoid vendor lock-in)
- ✅ Long-term investment (3+ year horizon)
- ✅ Existing infrastructure complex (multi-cloud, hybrid, legacy systems)

**Risks:**
- ⚠️ High upfront development cost (6-12 months to MVP)
- ⚠️ Ongoing maintenance burden (dedicated team required)
- ⚠️ Risk of building features that already exist in commercial products
- ⚠️ Slower time-to-value compared to buying

**Recommended Approach:**
- Start with Backstage (open source) as foundation
- Build custom plugins for unique integrations
- Contribute plugins back to community
- Examples: Spotify, American Airlines, Netflix

**ROI Calculation:**
- Platform team cost: 10 engineers × $200K = $2M/year
- Upfront development: 6-12 months to MVP
- Ongoing: Platform features, bug fixes, upgrades
- Break-even: When (developer productivity gains × engineer count) > platform team cost
- Typical: Organizations with 500+ engineers see positive ROI in 12-18 months

### When to Buy Commercial IDP

**Indicators:**
- ✅ Mid-size organization (100-1000 engineers) with limited platform resources (<5 platform engineers)
- ✅ Need fast time-to-value (3-6 months to production)
- ✅ Prefer managed infrastructure and support
- ✅ Standard use cases (web apps, microservices, CI/CD)
- ✅ Budget available for tooling (vs. headcount)
- ✅ Want to focus engineering on business value, not platform

**Risks:**
- ⚠️ Licensing costs (can be significant at scale)
- ⚠️ Potential vendor lock-in (migration difficult)
- ⚠️ Limited customization compared to open source
- ⚠️ Reliance on vendor roadmap for new features

**Recommended Approach:**
- Evaluate Port, Humanitec, Cortex, or Harness
- Start with pilot team (20-50 developers)
- Measure ROI (developer time saved, deployment frequency increase)
- Scale if metrics show clear value

**ROI Calculation:**
- Commercial IDP cost: $50-200 per developer/month
- For 500 engineers: $30K-120K/month = $360K-1.44M/year
- Small platform team: 2-3 engineers × $200K = $400K-600K/year
- Total cost: $760K-2M/year (vs. $2M+ for build)
- Faster time-to-value: 3-6 months vs. 6-12 months
- Lower risk: Proven product, vendor support

### When to Adopt Hybrid Approach

**Indicators:**
- ✅ Large organization needing both flexibility and speed
- ✅ Complex infrastructure requiring orchestration backend
- ✅ Want open-source portal with commercial orchestration (or vice versa)
- ✅ Willing to integrate multiple systems

**Recommended Approach:**
- **Portal:** Backstage (open source, customizable)
- **Orchestration:** Humanitec or Crossplane (infrastructure abstraction)
- **GitOps:** Argo CD (open source, proven)
- **Observability:** Commercial (Datadog, New Relic) or open source (Prometheus + Grafana)
- Example: Many enterprises in 2025 using Backstage + Humanitec combination

**Integration Considerations:**
- Ensure portals can integrate with orchestration backends (APIs, webhooks)
- Backstage + Humanitec: Humanitec plugin for Backstage available
- Backstage + Crossplane: Kubernetes plugin shows Crossplane resources
- Unified authentication (SSO across all platform components)

### Decision Tree

```
Start: Need Internal Developer Platform?
│
├─ Organization Size?
│  ├─ <100 engineers → Use cloud provider tools (AWS Proton, GCP, Azure) or simple CI/CD (GitHub Actions + documentation)
│  ├─ 100-500 engineers → Buy commercial IDP (Port, Humanitec) OR adopt Backstage with minimal customization
│  ├─ 500-1000 engineers → Buy commercial IDP OR invest in Backstage with dedicated team (2-3 engineers)
│  └─ 1000+ engineers → Build on Backstage with large platform team (5-10 engineers) OR hybrid (Backstage + commercial orchestration)
│
├─ Platform Engineering Expertise?
│  ├─ Limited (<2 experienced engineers) → Buy commercial IDP
│  ├─ Moderate (2-5 engineers) → Backstage with community plugins
│  └─ Strong (5+ engineers) → Custom Backstage build
│
├─ Time to Value?
│  ├─ Urgent (<3 months) → Buy commercial IDP
│  ├─ Moderate (3-6 months) → Backstage with minimal customization
│  └─ Long-term (6-12 months) → Custom platform build
│
├─ Customization Needs?
│  ├─ Standard use cases → Commercial IDP
│  ├─ Some unique requirements → Backstage with custom plugins
│  └─ Highly unique → Full custom build on Backstage
│
└─ Budget?
   ├─ Limited tooling budget → Backstage (open source)
   ├─ Moderate budget → Commercial IDP or hybrid
   └─ Flexible budget → Best-in-class tools across stack (hybrid)
```

### Selection Criteria Comparison

| Criteria | Build (Backstage) | Buy (Commercial) | Hybrid |
|----------|-------------------|------------------|--------|
| **Time to MVP** | 6-12 months | 3-6 months | 4-8 months |
| **Upfront Cost** | High (team setup) | Low (subscription) | Medium |
| **Ongoing Cost** | High (10+ engineers) | Medium (licensing) | Medium-High |
| **Customization** | Maximum | Limited | High |
| **Vendor Lock-In** | None | High | Medium |
| **Maintenance** | Self (team required) | Vendor | Mixed |
| **Support** | Community | Vendor | Mixed |
| **Best For** | Large orgs, unique needs | Mid-size, standard needs | Complex, large orgs |

## Golden Path Design: Flexibility vs. Standardization

### Principle: The 80/20 Rule

Golden paths should handle 80% of use cases; remaining 20% get escape hatches.

**Why This Matters:**
- Too rigid: Developers route around platform, create shadow IT
- Too flexible: No productivity gains, duplicate effort across teams
- Balanced: High adoption (easy path), innovation enabled (escape hatches)

### Spectrum of Control

#### High Standardization (Low Flexibility)

**When to Use:**
- Regulated industries (finance, healthcare, government)
- Security/compliance critical (SOC2, HIPAA, PCI-DSS)
- High risk of misconfigurations leading to outages or vulnerabilities
- Junior engineering teams needing guardrails

**Characteristics:**
- Limited technology choices (approved list only)
- Mandatory templates (cannot opt-out)
- Policy enforcement via admission controllers (OPA, Kyverno)
- Escape hatches require approval process (platform team review, architecture board)

**Examples:**
- Must use approved base images (security scanning passed)
- Cannot disable network policies (micro-segmentation enforced)
- Required resource limits enforced (prevent noisy neighbor)
- Mandatory observability instrumentation (metrics, logs, traces)

**Implementation:**
- OPA Gatekeeper policies: Reject deployments without required labels
- Kyverno policies: Mutate deployments to add security context
- Approval workflows: Production access requires manager + platform team approval
- Template versioning: All services must use template v2.x or higher

**Risks:**
- Stifles innovation (cannot experiment with new technologies)
- Frustration from advanced engineers ("getting in the way")
- Slower adoption of new best practices (approval process bottleneck)
- Can drive engineers to workarounds or shadow IT

**Mitigation:**
- Clear documentation on why constraints exist
- Fast-track approval process for trusted teams
- Regular review of constraints (remove outdated ones)
- Exemption process for justified cases

#### Balanced Approach (Recommended for Most)

**When to Use:**
- Most organizations (standard risk tolerance)
- Mix of junior and senior engineers
- Want to encourage best practices without blocking innovation

**Characteristics:**
- Recommended golden paths (easy, well-documented, supported)
- Alternatives allowed with documentation (justify deviations)
- Soft enforcement (defaults + education, not hard blocks)
- Easy escalation for exceptions (self-service + platform team review if needed)

**Examples:**
- Recommended: Use approved frameworks (Node.js, Python, Go), but custom frameworks allowed with runbook
- Default: Standard observability (Prometheus + Grafana), but custom metrics/logging allowed
- Encouraged: Use templates for new projects, but manual setup possible
- Documented: "If you deviate, you own support for that component"

**Implementation:**
- Templates are default in portal, but "advanced setup" option available
- Policy engines in audit mode (warn, not block)
- Documentation clearly marks "recommended" vs. "experimental"
- Platform team office hours for discussing deviations

**Benefits:**
- High adoption (golden paths are easiest option)
- Innovation enabled (advanced users can experiment)
- Clear expectations (deviations documented and owned)
- Balanced autonomy and standardization

**Success Metrics:**
- 80%+ of services use golden paths
- Advanced users happy (can deviate when needed)
- Platform team not overwhelmed with support for custom setups

#### High Flexibility (Low Standardization)

**When to Use:**
- Highly innovative organizations (startups, research labs)
- Senior engineering teams (know best practices)
- Experimentation culture (fail fast, learn quickly)

**Characteristics:**
- Golden paths as suggestions (not requirements)
- Minimal policy enforcement (only critical security/compliance)
- "You build it, you run it" ownership model
- Platform provides tools, not mandates

**Examples:**
- Choose any language, framework, database (platform-agnostic)
- Custom infrastructure configurations allowed
- Observability and security guidance provided, not enforced
- Engineers own full stack for their services

**Implementation:**
- Portal provides templates as starting points
- No policy engines (except security minimums)
- Documentation is guidance, not rules
- Platform team available for consultation, not enforcement

**Risks:**
- Inconsistency across teams (harder to support)
- Security/compliance gaps (if not careful)
- Duplicate effort (teams solving same problems differently)
- High cognitive load (engineers must know everything)

**Mitigation:**
- Regular architecture reviews (share patterns)
- Security scanning enforced (even for custom setups)
- Platform team publishes "patterns we've seen work"
- Shared libraries for common functions

### Decision Matrix

| Dimension | High Standardization | Balanced | High Flexibility |
|-----------|---------------------|----------|------------------|
| **Industry** | Finance, Healthcare, Gov | Tech, Retail, SaaS | Startups, Research |
| **Risk Tolerance** | Low | Moderate | High |
| **Team Maturity** | Junior to Mid | Mixed | Senior |
| **Innovation Priority** | Low (stability focus) | Moderate | High |
| **Support Model** | Centralized | Hybrid | Decentralized |
| **Approval Process** | Required for deviations | Optional for major changes | Self-service |
| **Enforcement** | Hard (policy engines) | Soft (defaults + education) | Minimal (guidance only) |

### Recommendations by Use Case

**1. Financial Services Platform:**
- **Approach:** High Standardization
- **Rationale:** Regulatory compliance (SOC2, PCI-DSS), audit requirements
- **Implementation:**
  - Mandatory templates with strict policies
  - Escape hatches require architecture review board approval
  - Policy-as-code enforced (OPA Gatekeeper)
  - All deployments logged and auditable
- **Example Policy:** "All services must use approved base images from internal registry, pass security scanning, and enforce encryption at rest and in transit"

**2. E-Commerce Platform:**
- **Approach:** Balanced
- **Rationale:** Mix of standard web apps and innovative features, junior to senior engineers
- **Implementation:**
  - Golden paths for web apps, APIs, data pipelines
  - Custom solutions allowed with documentation and ownership
  - Platform team provides guidance, not blockers
  - Soft enforcement (warnings, not blocks)
- **Example Policy:** "Recommended to use Node.js microservice template, but custom setups allowed if team documents architecture and owns support"

**3. Early-Stage Startup:**
- **Approach:** High Flexibility
- **Rationale:** Speed and innovation critical, senior engineers, limited platform resources
- **Implementation:**
  - Minimal platform (CI/CD + monitoring basics)
  - Engineers own full stack
  - Golden paths emerge over time from repeated patterns
  - Platform team publishes guidance, not rules
- **Example Policy:** "No required templates. Platform team provides example repos and is available for consultation."

## Platform Adoption Strategy

### Phase 1: Foundation (Months 1-3)

**Goals:**
- Establish platform vision and charter
- Form platform team and assign roles
- Build executive sponsorship
- Choose IDP technology stack

**Activities:**

**Discovery:**
- Interview developers (15-20 individual interviews)
  - Pain points: What slows you down?
  - Workflows: How do you currently deploy?
  - Tool preferences: What tools do you wish you had?
- Audit existing infrastructure and tooling
  - Inventory: Cloud resources, CI/CD pipelines, monitoring tools
  - Gaps: What's missing? What's duplicated?
- Identify quick wins (high-impact, low-effort improvements)
  - Example: Centralized logging if currently scattered

**Strategy:**
- Define platform vision and principles
  - Vision: "Enable developers to focus on business logic, not infrastructure"
  - Principles: Self-service, secure by default, gradual adoption
- Establish success metrics
  - Baseline DORA metrics (current deployment frequency, lead time)
  - Developer satisfaction (baseline survey)
  - Platform KPIs (adoption rate, self-service rate)
- Secure budget and headcount for platform team
  - Business case: ROI from developer productivity gains
  - Headcount: 3-5 initial platform engineers

**Foundation:**
- Set up developer portal (Backstage, Port, or commercial)
  - Deploy to cloud infrastructure
  - Configure authentication (SSO)
  - Basic homepage and documentation
- Create initial service catalog
  - Manually document top 20 services
  - Ownership, repository links, runbook links
- Build first golden path template
  - Identify most common use case (e.g., Node.js API)
  - Scaffold: Repository structure, CI/CD, deployment config
  - Test with pilot service

**Success Criteria:**
- Platform vision documented and communicated to engineering org
- Platform team formed (3-5 initial members with clear roles)
- Developer portal accessible to all engineers
- 1 golden path template available and tested

**Timeline:** 3 months (Month 1: Discovery, Month 2: Strategy + Team, Month 3: Foundation build)

### Phase 2: Pilot (Months 4-6)

**Goals:**
- Validate platform with pilot teams
- Prove ROI (faster onboarding, reduced incidents, higher satisfaction)
- Iterate based on feedback

**Activities:**

**Pilot Selection:**
- Choose 2-3 teams (15-30 total developers)
  - Criteria: Friendly (willing to give feedback), representative of broader org, mix of greenfield and brownfield
- Greenfield: New projects (test full workflow from scratch)
- Brownfield: Existing services (test migration path)
- Committed to giving feedback and iterating

**Enablement:**
- White-glove onboarding for pilot teams
  - Kickoff meeting: Platform overview, goals, feedback process
  - Dedicated Slack channel for pilot teams
  - Platform engineer embedded with each pilot team (first 2 weeks)
- Weekly office hours (platform team available for questions)
- Document feedback and pain points
  - Feedback log: Issues, feature requests, confusion points
  - Prioritize by impact and frequency

**Iteration:**
- Rapid fixes for blockers (prioritize pilot team needs)
  - Goal: Fix critical issues within 1-2 days
  - Example: If CI/CD integration broken, fix immediately
- Expand golden paths (2-3 additional templates)
  - Based on pilot team needs (e.g., Python service, React frontend)
- Integrate key tools (CI/CD, monitoring, secrets)
  - Backstage plugins: GitHub Actions, Prometheus, Vault
  - Single pane of glass for developers

**Success Criteria:**
- 3 pilot teams using platform successfully
- 50% reduction in onboarding time for new services (pilot teams)
  - Measure: Time from code scaffold to production deployment
- Positive feedback from pilot teams (satisfaction survey: >7/10)
- 3-5 golden path templates available

**Timeline:** 3 months (Month 4: Pilot selection + onboarding, Months 5-6: Iteration + expansion)

### Phase 3: Expansion (Months 7-12)

**Goals:**
- Scale platform to broader organization (20-50% of teams)
- Build internal champions and evangelists
- Establish platform operations and support model

**Activities:**

**Evangelization:**
- Internal blog posts and demos (showcase pilot team successes)
  - Case studies: "Team X reduced deployment time from 2 hours to 10 minutes"
  - Metrics: DORA improvements, developer satisfaction
- Lunch-and-learns (platform capabilities, new features)
  - Monthly sessions, different topics (golden paths, self-service, troubleshooting)
- Internal champions program (power users who help others)
  - Recruit 1-2 champions per team
  - Champions get early access to features, direct line to platform team
  - Recognize champions (internal awards, blog posts)

**Self-Service:**
- Comprehensive documentation (getting started, recipes, troubleshooting)
  - Getting started: 15-minute quick start guide
  - Recipes: Common tasks (deploy service, add database, configure monitoring)
  - Troubleshooting: FAQ, common errors
- Video tutorials and walkthroughs
  - Screen recordings: Creating service from template, deploying to production
- Slack/Teams channel for community support
  - Platform team monitors, but community can answer questions
  - Knowledge base built from Q&A

**Operations:**
- Platform SLOs and monitoring (uptime, latency, error rate)
  - SLO: 99.5% uptime for developer portal
  - SLO: <5s latency for API calls
  - SLO: <1% error rate for deployments
- On-call rotation for platform team
  - 24/7 coverage for production incidents
  - Escalation path: On-call → platform lead → director
- Incident response playbooks
  - Portal down: Steps to diagnose and recover
  - Deployment failures: Troubleshooting guide

**Expansion:**
- Onboard 10-20 additional teams
  - Self-service onboarding (documentation + videos)
  - Platform team office hours for questions
- Expand service catalog (100+ services documented)
  - Automated discovery where possible (scan repositories)
- Add advanced features (ephemeral environments, FinOps integration)
  - Ephemeral environments: Per-PR preview deployments
  - FinOps: Cost visibility per service/team

**Success Criteria:**
- 20-50% of engineering teams using platform
- Self-service adoption (80% of onboarding without platform team involvement)
- Platform SLOs met (99.5% uptime)
- Measurable DORA metric improvements (5x deployment frequency, 50% reduction in lead time)

**Timeline:** 6 months (Months 7-9: Evangelization + self-service, Months 10-12: Expansion + operations)

### Phase 4: Maturity (Year 2+)

**Goals:**
- Platform as standard way of working (80%+ adoption)
- Continuous improvement based on metrics and feedback
- Platform team as product team (roadmap, OKRs, customer focus)

**Activities:**

**Product Management:**
- Hire product manager for platform team
- Quarterly roadmap planning (prioritized by impact)
  - Feature requests from teams
  - Platform team initiatives
  - Prioritization: Impact × Effort matrix
- Developer NPS surveys (measure satisfaction quarterly)
  - Track trends, identify problem areas
- Usage analytics (which features used, which neglected)
  - Instrument portal with analytics (page views, feature usage)
  - Identify underutilized features (consider deprecation or improvement)

**Advanced Capabilities:**
- AI-assisted features (chatbots for common questions, recommendation engines)
- FinOps optimization (automated right-sizing, cost anomaly detection)
- Policy-as-code expansion (comprehensive guardrails for security, compliance)

**Ecosystem:**
- Contribute back to open-source community (Backstage plugins)
- Partner integrations (third-party tools)
- Internal marketplace (teams can publish reusable components)

**Success Criteria:**
- 80%+ of engineering teams using platform
- Top-quartile DORA metrics (compared to industry benchmarks)
- High developer NPS (>50)
- Platform team operates as product team (clear roadmap, customer focus)

**Timeline:** Ongoing (Year 2+)

### Adoption Metrics to Track

| Metric | Phase 1 (Foundation) | Phase 2 (Pilot) | Phase 3 (Expansion) | Phase 4 (Maturity) |
|--------|---------------------|----------------|---------------------|-------------------|
| **Teams Using Platform** | 0 | 2-3 (pilot) | 10-20 (20-50%) | 40+ (80%+) |
| **Services in Catalog** | 20 (manual) | 50-100 | 100-500 | 500+ |
| **Golden Path Templates** | 1 | 3-5 | 10+ | 20+ |
| **Self-Service Rate** | N/A | 50% | 80% | 95% |
| **Deployment Frequency** | Baseline | 2x baseline | 5x baseline | 10x baseline |
| **Onboarding Time** | Baseline (days) | 50% reduction | 75% reduction | 90% reduction (hours) |
| **Developer NPS** | Baseline | +10 | +30 | +50 |

## Platform Team Structure

### Model 1: Centralized Platform Team

**Structure:**
- Single platform team (5-20 engineers) serving entire organization
- Team owns: Developer portal, infrastructure orchestration, CI/CD, observability integration
- Team provides: Golden paths, support, strategic roadmap

**When to Use:**
- Small to mid-size organizations (100-500 engineers)
- Consistent technology stack across organization
- Limited platform engineering expertise (need to concentrate talent)

**Roles and Responsibilities:**

**Platform Lead (1):**
- Overall platform strategy and vision
- Roadmap prioritization
- Stakeholder management (engineering leadership, security, finance)

**Platform Product Manager (0-1):**
- Developer customer research
- Feature prioritization based on impact
- Success metrics and analytics

**Platform Engineers (3-10):**
- Build and maintain developer portal (Backstage plugins, integrations)
- Create and update golden path templates
- Integrate infrastructure orchestration (Crossplane, Terraform)
- Developer support (office hours, troubleshooting)

**SRE / On-Call (1-2):**
- Platform operations and monitoring
- Incident response
- SLO tracking and performance optimization

**DevEx Specialist (0-1):**
- Developer experience research
- Documentation and training
- Usability testing of platform features

**Pros:**
- ✅ Concentrated expertise (deep specialization)
- ✅ Consistent platform experience across organization
- ✅ Efficient resource utilization (no duplication)
- ✅ Clear ownership and accountability

**Cons:**
- ❌ Risk of bottleneck (all requests go through one team)
- ❌ May not understand all domain-specific needs
- ❌ Can become ivory tower (disconnected from app teams)
- ❌ Limited scalability (one team supporting 100s of developers)

**Best Practices:**
- Embed platform engineers with app teams temporarily (3-6 months rotations)
  - Learn domain-specific needs
  - Build relationships, trust
- Self-service focus (minimize ticket-based work)
  - Goal: 90%+ of actions self-service
- Regular office hours and demos (stay connected to developers)
  - Weekly office hours (drop-in for questions)
  - Monthly demos (new features, best practices)

**Scaling Limits:**
- Works well up to 500 engineers
- Beyond 500, consider federated or hub-and-spoke model

### Model 2: Federated Platform Model

**Structure:**
- Central platform team (5-10 engineers) sets standards and provides core capabilities
- Embedded platform engineers (1-2 per business unit/product area) customize for domains
- Shared responsibility: Central team (core platform), embedded engineers (domain-specific integrations)

**When to Use:**
- Large organizations (500-2000+ engineers)
- Multiple business units or product lines with different needs
- Some platform expertise distributed across organization

**Roles and Responsibilities:**

**Central Platform Team (5-10 engineers):**
- Platform strategy and vision
- Core developer portal (Backstage core, authentication, service catalog)
- Shared golden path templates (common use cases)
- Platform standards and governance
- Tool evaluations and vendor management

**Embedded Platform Engineers (1-2 per business unit):**
- Domain-specific golden paths (e.g., ML platform templates)
- Custom integrations (business unit-specific tools)
- Local developer support and evangelization
- Feedback conduit to central team

**Reporting Structure:**
- Embedded engineers report to: Business unit lead (dotted line to central platform lead)
- Or: Central platform lead (dotted line to business unit lead)
- Key: Clear alignment on priorities and responsibilities

**Pros:**
- ✅ Scales well (distributed support across domains)
- ✅ Domain expertise (embedded engineers understand specific needs)
- ✅ Balance of consistency (central standards) and flexibility (domain customization)
- ✅ Reduces bottlenecks (embedded engineers handle domain-specific work)

**Cons:**
- ❌ Coordination overhead (central + embedded teams must align)
- ❌ Risk of fragmentation (domains diverge if not careful)
- ❌ Requires more total headcount (embedded engineers across domains)

**Best Practices:**
- Clear charter: Central team owns platform core, embedded teams own integrations
  - Written charter: What's centralized vs. domain-specific
  - Decision log: When decisions made, rationale
- Regular sync meetings (central + all embedded engineers)
  - Bi-weekly: Share progress, discuss challenges
  - Quarterly: Strategic planning, roadmap alignment
- Shared knowledge base (central team documents patterns, embedded teams contribute)
  - Confluence/Notion: Platform architecture, best practices, recipes
- Rotation program (embedded engineers rotate through central team 3-6 months)
  - Cross-pollination of ideas
  - Career development

**Scaling Limits:**
- Works well from 500 to 5000+ engineers
- Number of embedded engineers scales with business units (not total headcount)

### Model 3: Hub-and-Spoke Model

**Structure:**
- Central "hub" team (3-5 platform engineers) provides foundational platform
- "Spoke" teams (app/product teams) contribute plugins, templates, integrations
- Community-driven: Platform team curates, app teams contribute

**When to Use:**
- Organizations with strong open-source culture
- High engineering maturity (senior engineers across teams)
- Want to distribute platform ownership (avoid bottleneck)

**Roles and Responsibilities:**

**Hub Team (3-5 engineers):**
- Core developer portal infrastructure
- Platform governance (quality standards for contributions)
- Curate community contributions (review, merge, deprecate)
- Strategic roadmap (platform direction)
- Tooling and infrastructure for contribution (e.g., plugin development kit)

**Spoke Teams (distributed):**
- Contribute plugins for tools they use (e.g., Datadog plugin)
- Build domain-specific templates (e.g., ML service template)
- Share reusable components (libraries, scripts)
- Dog-food platform, provide feedback

**Contribution Process:**
- RFC (Request for Comments) for major features
- Pull requests to platform repository
- Code review by hub team
- Documentation required for all contributions
- Maintenance responsibility: Contributors own their plugins

**Pros:**
- ✅ Distributes ownership (not reliant on one team)
- ✅ Scales without headcount (community contributions)
- ✅ Innovation from diverse perspectives
- ✅ High engagement (teams invested in platform success)

**Cons:**
- ❌ Quality control challenges (varied contribution quality)
- ❌ Maintenance burden (who maintains old plugins?)
- ❌ Requires strong governance (avoid chaos)
- ❌ Not suitable for low-maturity orgs (needs senior engineers)

**Best Practices:**
- Clear contribution guidelines
  - Code quality standards
  - Documentation requirements
  - Testing requirements
- Deprecation policy (sunset unused/unmaintained plugins)
- Recognition for contributors (internal awards, blog posts, conference talks)
- Hub team capacity reserved for governance (not building all features)

**Scaling Limits:**
- Works well for mature organizations (500+ engineers, strong open-source culture)
- Requires active community management

### Team Sizing Guidelines

| Organization Size | Recommended Model | Central Team Size | Embedded Engineers |
|------------------|-------------------|-------------------|--------------------|
| <100 engineers | Centralized | 2-3 | 0 |
| 100-500 engineers | Centralized | 5-10 | 0 |
| 500-1000 engineers | Centralized or Federated | 5-10 | 2-4 (if federated) |
| 1000-2000 engineers | Federated | 8-12 | 5-10 |
| 2000-5000 engineers | Federated or Hub-and-Spoke | 10-15 | 10-20 (if federated) |
| 5000+ engineers | Federated or Hub-and-Spoke | 15-30 | 20+ (if federated) |

### Choosing the Right Model

**Decision Factors:**

1. **Organization Size:**
   - <500 engineers → Centralized
   - 500-2000 → Federated
   - 2000+ → Federated or Hub-and-Spoke

2. **Engineering Culture:**
   - Traditional (centralized IT) → Centralized
   - Matrixed (business units) → Federated
   - Open-source culture → Hub-and-Spoke

3. **Platform Engineering Expertise:**
   - Concentrated (few experts) → Centralized
   - Distributed (expertise in business units) → Federated
   - High maturity (senior engineers across org) → Hub-and-Spoke

4. **Customization Needs:**
   - Standardized (one tech stack) → Centralized
   - Varied (different needs per business unit) → Federated
   - Experimental (lots of innovation) → Hub-and-Spoke

5. **Budget:**
   - Limited headcount → Centralized or Hub-and-Spoke
   - Can support embedded engineers → Federated
