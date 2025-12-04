---
sidebar_position: 4
---

# Platform Engineering

Master plan for building internal developer platforms (IDPs) that enable self-service infrastructure and improve developer experience. This skill covers platform design principles, golden paths, abstraction layers, and measuring platform adoption and effectiveness.

**Status**: 🟢 Master Plan Available

## Key Topics

- **Platform Vision**: Developer experience goals, golden paths, self-service capabilities, platform as product
- **Platform Architecture**: Control plane, data plane, API design, extensibility patterns
- **Service Catalog**: Service templates, scaffolding, standardization, best practices enforcement
- **Developer Portal**: Unified interface, documentation, service discovery, status dashboards
- **Infrastructure Abstraction**: Hiding complexity, sensible defaults, escape hatches for advanced users
- **Automation**: Self-service provisioning, automated workflows, policy enforcement
- **Observability**: Platform metrics, developer experience metrics, cost visibility
- **Platform Adoption**: Onboarding, training, feedback loops, measuring success

## Primary Tools & Technologies

- **Platform Frameworks**: Backstage, Port, Humanitec, Kratix, Crossplane
- **Service Mesh**: Istio, Linkerd, Consul Connect
- **API Gateway**: Kong, Ambassador, Traefik, Nginx
- **Developer Portals**: Backstage, Cortex, OpsLevel
- **Templating**: Cookiecutter, Yeoman, Copier, custom scaffolding
- **Policy Engines**: OPA, Kyverno, Cloud Custodian
- **Documentation**: Docusaurus, MkDocs, GitBook, Confluence
- **Workflow Automation**: Temporal, Airflow, Argo Workflows

## Integration Points

- **Building CI/CD Pipelines**: Platform-provided pipeline templates
- **GitOps Workflows**: Platform manages GitOps configurations
- **Kubernetes Operations**: Kubernetes as platform substrate
- **Infrastructure as Code**: IaC abstracted through platform
- **Security Operations**: Security policies enforced by platform
- **Observability**: Observability built into platform services
- **Cloud Cost Management**: Cost tracking and optimization in platform
- **Incident Management**: Platform-assisted incident response

## Use Cases

- Building internal developer platform from scratch
- Implementing golden path for microservices
- Creating self-service database provisioning
- Designing developer onboarding experience
- Standardizing CI/CD across teams
- Building service catalog with templates
- Implementing platform observability
- Measuring platform adoption and ROI

## Decision Framework

**Platform scope based on organization:**
- **Small teams (< 50 devs)**: Focus on automation, documentation, simple self-service
- **Medium teams (50-200 devs)**: Developer portal, service catalog, standardized templates
- **Large teams (200+ devs)**: Full IDP, multi-tenancy, advanced abstractions, dedicated platform team

**Build vs buy:**
- **Build**: Unique requirements, existing tools, full control, engineering capacity
- **Buy/Adopt**: Standard needs, faster time-to-value, limited resources, proven solutions

**Abstraction level:**
- **Low abstraction**: Expose Kubernetes directly, Terraform modules, manual configuration
- **Medium abstraction**: Service templates, guided workflows, sensible defaults, escape hatches
- **High abstraction**: Fully managed services, minimal configuration, opinionated workflows

**Golden path design:**
1. Identify most common use cases (80/20 rule)
2. Create opinionated, frictionless path for common cases
3. Provide escape hatches for advanced needs
4. Document both paths clearly
5. Measure adoption and iterate

## Platform Success Metrics

- **Developer satisfaction**: NPS, surveys, feedback
- **Time to first deploy**: Onboarding effectiveness
- **Lead time for changes**: Platform impact on velocity
- **Platform adoption rate**: Services using platform vs total
- **Self-service usage**: Tickets avoided through automation
- **Mean time to recovery**: Platform impact on reliability
- **Cost efficiency**: Resource utilization, waste reduction

## Platform Anti-Patterns to Avoid

- Building without developer input (ivory tower platform)
- Forcing migration without clear value (adoption resistance)
- Over-abstracting and hiding too much (loss of control)
- Under-abstracting and exposing too much complexity (no improvement)
- Lack of documentation and training (poor adoption)
- No feedback loops (platform drift from needs)
- Platform team as gatekeeper (bottleneck)
