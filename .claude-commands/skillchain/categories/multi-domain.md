# Multi-Domain Workflow Orchestrator

Handles cross-domain goals that span multiple categories (infrastructure + security + devops, frontend + backend + cloud, etc.)

---

## Step 1: Load Shared Resources

Read execution-flow.md for general workflow guidance:

```
Read {SKILLCHAIN_DIR}/_shared/execution-flow.md
```

If any frontend/UI skills are detected in the chain, also load theming rules:

```
Read {SKILLCHAIN_DIR}/_shared/theming-rules.md
```

---

## Step 2: Detect Involved Domains

Analyze the user goal to identify which domains are involved:

### Domain Detection Rules

Parse the goal for keywords matching these domains:

**Infrastructure:**
- Keywords: kubernetes, k8s, terraform, cluster, container orchestration, helm
- Registry: infrastructure.yaml

**Security:**
- Keywords: security, secrets, vault, encryption, compliance, audit, RBAC, IAM
- Registry: security.yaml

**DevOps:**
- Keywords: CI/CD, pipeline, deployment, automation, jenkins, github actions, gitops
- Registry: devops.yaml

**Cloud:**
- Keywords: aws, azure, gcp, cloud, s3, lambda, serverless, cloud functions
- Registry: cloud.yaml

**Data:**
- Keywords: data pipeline, ETL, streaming, kafka, airflow, data processing
- Registry: data.yaml

**Developer:**
- Keywords: IDE, debugging, testing, code review, git workflow
- Registry: developer.yaml

**FinOps:**
- Keywords: cost, budget, tagging, cost optimization
- Registry: finops.yaml

**AI/ML:**
- Keywords: RAG, embeddings, vector, LLM, model serving
- Registry: ai-ml.yaml

**Frontend:**
- Keywords: UI, dashboard, react, component, chart, form
- Registry: frontend.yaml

**Backend:**
- Keywords: API, database, postgres, authentication, REST
- Registry: backend.yaml

### Load Relevant Registries

```python
detected_domains = []
for domain in all_domains:
  if goal_contains_keywords(user_goal, domain.keywords):
    detected_domains.append(domain)
    load_registry(f"{SKILLCHAIN_DIR}/_registries/{domain.name}.yaml")
```

---

## Step 3: Determine Domain Execution Order

Organize detected domains into execution phases:

### Phase 1: Infrastructure Foundation (if present)
Execute these domains FIRST as they provide the foundation:
- infrastructure (k8s cluster setup)
- cloud (cloud resource provisioning)

### Phase 2: Platform Services (if present)
Execute after infrastructure is ready:
- security (secrets management, RBAC)
- data (data pipelines, databases)
- backend (APIs, services)

### Phase 3: Application Layer (if present)
Execute after platform is ready:
- frontend (UI components)
- ai-ml (RAG pipelines, model serving)

### Phase 4: Operations (if present)
Execute LAST to set up operational concerns:
- devops (CI/CD, deployment automation)
- finops (cost optimization, tagging)
- developer (tooling, workflows)

### Execution Order Example

**Goal: "Deploy secure kubernetes cluster with monitoring and cost tracking"**

Detected domains: infrastructure, security, devops, finops

Execution order:
```
Phase 1: infrastructure (kubernetes cluster)
Phase 2: security (RBAC, secrets, network policies)
Phase 4: devops (CI/CD, deployment), finops (cost optimization, tagging)
```

---

## Step 4: Confirm Multi-Domain Chain and Prepare Skill Invocations

**CRITICAL: This step prepares you to INVOKE skills using the Skill tool. You MUST actually call the Skill tool for each skill - this is not documentation, it's a required action.**

Present the detected domains and execution order to the user:

```
>═══════════════════════════════════════════════════════════
  MULTI-DOMAIN SKILL CHAIN DETECTED
═══════════════════════════════════════════════════════════

Goal: "{original_goal}"

Detected Domains: [{domain1}, {domain2}, {domain3}, ...]

Execution Plan:
───────────────────────────────────────────────────────────

PHASE 1: Infrastructure Foundation
  □ infrastructure → {matched skills}
  □ cloud → {matched skills}

PHASE 2: Platform Services
  □ security → {matched skills}
  □ backend → {matched skills}

PHASE 3: Application Layer
  □ frontend → {matched skills}
  □ ai-ml → {matched skills}

PHASE 4: Operations
  □ devops → {matched skills}
  □ finops → {matched skills}

───────────────────────────────────────────────────────────
Total Skills: {N}
Estimated Questions: {X}
Estimated Time: {Y} minutes
───────────────────────────────────────────────────────────

⚠️  IMPORTANT: Each skill listed above will be INVOKED using the Skill tool.
You will call Skill({ skill: "plugin-prefix:skill-name" }) for each one.

Options:
  • Type "confirm" to proceed
  • Type "skip" to use all defaults (faster)
  • Type "customize" to add/remove skills
  • Type "help" to see workflow commands

Your choice:
```

Wait for user response:
- "confirm" → Proceed to Step 5
- "skip" → Set skip_all_questions = true, proceed to Step 5
- "customize" → Allow skill additions/removals, then proceed
- "help" → Show workflow commands from execution-flow.md

---

## Step 5: Execute Multi-Domain Workflow

Initialize:
```
domain_configs = {}  # Track configs by domain
skill_configs = {}   # Track configs by skill
current_phase = 1
max_phase = 4
skip_all_questions = false
```

For each phase (1 through 4):

### 5.1 Announce Phase

```
═══════════════════════════════════════════════════════════
 PHASE {current_phase}/{max_phase}: {PHASE_NAME}
═══════════════════════════════════════════════════════════
```

### 5.2 Execute Domains in Phase

For each domain in current phase:

#### 5.2.1 Announce Domain

```
─────────────────────────────────────────────────────────
▸ DOMAIN: {domain.name}
  Skills: [{skill1}, {skill2}, ...]
─────────────────────────────────────────────────────────
```

#### 5.2.2 Invoke Each Skill in Domain

**CRITICAL: You MUST use the Skill tool to invoke each skill. THIS IS A REQUIRED ACTION, NOT DOCUMENTATION.**

**Skill Invocation Protocol (MANDATORY EXECUTION LOOP):**

For each skill in domain, execute this REQUIRED loop:

1. **ANNOUNCE** - Tell user which skill you're about to invoke:
   ```
   ⚙️ Invoking skill: {plugin-prefix:skill-name}
   Purpose: {brief_description}
   ```

2. **INVOKE** - Actually call the Skill tool (THIS IS REQUIRED):
   ```
   Skill({ skill: "{plugin-prefix:skill-name}" })
   ```

   **THIS IS NOT OPTIONAL. You MUST call the Skill tool with the exact format above.**

3. **FOLLOW** - After invoking, the skill's SKILL.md content will load into context:
   - Read the expanded skill instructions carefully
   - Follow ALL instructions in the loaded skill content
   - Execute any scripts or tools the skill directs you to use
   - Ask configuration questions if defined in "## Skillchain Configuration"

4. **TRACK** - Store the configuration and outputs:
   ```
   skill_configs[skill.name] = {
     answers: user_answers,
     invocation: skill.invocation,
     domain: domain.name,
     phase: current_phase,
     outputs_generated: [list of files created]
   }
   ```

5. **PROCEED** - Move to next skill in domain or next domain in phase

**Domain-Specific Skill Prefixes (USE THESE EXACT FORMATS):**

Multi-domain combines skills from 3+ domains. Use the correct plugin prefix for each domain:

**DevOps Domain:**
- `devops-skills:building-ci-pipelines`
- `devops-skills:writing-dockerfiles`
- `infrastructure-skills:writing-infrastructure-code`
- `infrastructure-skills:operating-kubernetes`
- `ui-foundation-skills:theming-components` (if frontend involved)

**Security Domain:**
- `security-skills:architecting-security`
- `data-engineering-skills:secret-management`
- `security-skills:architecting-security`
- `security-skills:implementing-compliance`

**Cloud Domain:**
- `cloud-provider-skills:deploying-on-aws`
- `cloud-provider-skills:deploying-on-azure`
- `cloud-provider-skills:deploying-on-gcp`
- `cloud-provider-skills:deploying-on-aws`

**Data Domain:**
- `data-engineering-skills:streaming-data`
- `data-engineering-skills:transforming-data`
- `data-engineering-skills:transforming-data`
- `backend-data-skills:using-relational-databases`

**AI/ML Domain:**
- `backend-ai-skills:ai-data-engineering`
- `backend-ai-skills:ai-data-engineering`
- `backend-ai-skills:model-serving`
- `ai-ml-skills:implementing-mlops`

**Developer Domain:**
- `developer-productivity-skills:debugging-techniques`
- `devops-skills:testing-strategies`
- `developer-productivity-skills:debugging-techniques`

**FinOps Domain:**
- `finops-skills:optimizing-costs`
- `finops-skills:optimizing-costs`
- `finops-skills:resource-tagging`

**Example of Complete Invocation Sequence:**

```
Phase 1: Infrastructure Foundation
─────────────────────────────────────────────────────────
▸ DOMAIN: devops

⚙️ Invoking skill: infrastructure-skills:operating-kubernetes
Purpose: Configure Kubernetes cluster orchestration

[ACTUAL SKILL TOOL CALL HAPPENS HERE - REQUIRED]
Skill({ skill: "infrastructure-skills:operating-kubernetes" })

[Skill loads, you follow its instructions, ask questions, generate configs]

✓ Skill complete. Generated:
  - k8s/cluster-config.yaml
  - k8s/namespaces.yaml

[Move to next skill]

▸ DOMAIN: cloud

⚙️ Invoking skill: cloud-provider-skills:deploying-on-aws
Purpose: Provision AWS infrastructure

[ACTUAL SKILL TOOL CALL HAPPENS HERE - REQUIRED]
Skill({ skill: "cloud-provider-skills:deploying-on-aws" })

[Skill loads, you follow its instructions...]
```

**REMEMBER: The Skill tool call is MANDATORY. You are not documenting skills, you are EXECUTING them.**

#### 5.2.3 Load Questions

All skills use `questions.source: "skill"` format.

Extract questions from SKILL.md `## Skillchain Configuration` section.

#### 5.2.4 Ask User (unless skip_all_questions)

Present questions with:
- Context from previous domains/phases
- Cross-domain awareness (e.g., "You're deploying to Kubernetes, so...")
- Smart defaults based on earlier choices
- Dependencies on skills from earlier phases

Handle workflow commands:
- "skip" → Use default for this question
- "back" → Return to previous skill (may cross domain boundaries)
- "status" → Show progress across all phases
- "done" → Skip remaining phases, proceed to generation
- "restart" → Go back to Step 4

#### 5.2.5 Store Configuration

```
skill_configs[skill.name] = {
  answers: user_answers,
  invocation: skill.invocation,
  domain: domain.name,
  phase: current_phase
}

domain_configs[domain.name][skill.name] = skill_configs[skill.name]
```

### 5.3 Phase Completion

After all domains in phase complete:

```
═══════════════════════════════════════════════════════════
✓ PHASE {current_phase} COMPLETE
  Configured: {list of domains}
═══════════════════════════════════════════════════════════
```

Increment current_phase and continue to next phase.

---

## Step 5.5: Validate Chain Outputs

After all phases and domains have executed, validate the combined output:

### Load Validation Logic

```
Read {SKILLCHAIN_DATA}/shared/validation.md
```

### Per-Skill Output Validation

For each skill that was invoked:
```
skill_outputs = Read {SKILLS_DIR}/{skill_name}/outputs.yaml
For each output in skill_outputs.base_outputs:
  If NOT exists {project_path}/{output.path}:
    Mark as missing, log for user
  Else if output.must_contain exists:
    Check file contains expected patterns
```

### Run Chain Validation

```
If chain_context.blueprint exists:
  # Option 1: Use completeness checker script
  Run: python scripts/runtime/completeness_checker.py {project_path} --blueprint {blueprint} --maturity {maturity}

  # Option 2: Manual validation (if script not available)
  # Load blueprint deliverables
  Read {SKILLCHAIN_CMD}/blueprints/{chain_context.blueprint}.md
  Parse "## Deliverables Specification" section

  # Apply maturity adjustments
  For each deliverable in deliverables:
    If deliverable.maturity_required exists:
      If chain_context.maturity NOT in deliverable.maturity_required:
        Mark deliverable as "skipped"

  # Validate each required deliverable
  For each deliverable NOT skipped:
    result = validate_deliverable(deliverable, chain_context.project_path)
    chain_context.deliverables_status[deliverable.name] = result

  # Calculate completeness
  required_count = count(deliverables where status != "skipped")
  fulfilled_count = count(deliverables where status == "fulfilled")
  completeness = fulfilled_count / required_count

Else:
  # No blueprint - run basic completeness check
  Run run_basic_completeness_check(chain_context.project_path)
```

### Generate Validation Report

```
┌────────────────────────────────────────┐
│ MULTI-DOMAIN SKILLCHAIN VALIDATION     │
├────────────────────────────────────────┤
│ Blueprint: {chain_context.blueprint}   │
│ Maturity: {chain_context.maturity}     │
│ Domains: {detected_domains}            │
├────────────────────────────────────────┤
For each deliverable in chain_context.deliverables_status:
  If status == "fulfilled": │ ✓ {name}
  If status == "missing":   │ ✗ {name} - MISSING
  If status == "skipped":   │ ○ {name} (skipped - {maturity})
├────────────────────────────────────────┤
│ Required: {required_count}             │
│ Fulfilled: {fulfilled_count}           │
│ Completeness: {completeness}%          │
└────────────────────────────────────────┘
```

### Handle Missing Deliverables

```
If completeness < 80%:
  "⚠️ Some cross-domain components weren't fully generated:

   Missing:
   [list deliverables where status == "missing"]

   Would you like me to:
   A) Generate the missing components
   B) Continue without them
   C) See detailed validation report

   Note: Missing components may affect domain integration points."

  If user chooses A:
    For each missing deliverable:
      Identify which domain/skill owns that deliverable
      Invoke appropriate skill from that domain
    Re-run validation (go back to "Run Chain Validation")
    Re-validate cross-domain integration points
```

---

## Step 6: Generate Multi-Domain Output

After all phases complete, generate integrated deliverables:

### 6.1 Analyze Cross-Domain Integration Points

Identify where domains need to interact:

**Infrastructure → Security:**
- Kubernetes RBAC policies
- Network policies
- Pod security standards

**Infrastructure → DevOps:**
- Kubernetes deployment manifests
- CI/CD pipeline configs for k8s
- Helm charts

**Backend → Security:**
- API authentication middleware
- Secrets injection into services
- Database encryption

**Cloud → FinOps:**
- Resource tagging policies
- Cost allocation by cloud service
- Budget alerts

**Frontend → Backend:**
- API client generation
- Authentication token handling
- Type-safe API contracts

**AI/ML → Backend:**
- Vector database integration
- LLM inference API endpoints
- Streaming response handling

### 6.2 Generate Integrated Output

Create complete multi-domain implementation:

```
═══════════════════════════════════════════════════════════
  MULTI-DOMAIN IMPLEMENTATION COMPLETE
═══════════════════════════════════════════════════════════

Configured Domains: [{domain1}, {domain2}, ...]
Total Skills: {N}

Generated Structure:
═► multi-domain-project/
     infrastructure/
        kubernetes/
           cluster-config.yaml       # K8s cluster setup
           namespaces.yaml           # Namespace definitions
        terraform/
           main.tf                   # Infrastructure as code
           variables.tf
     security/
        rbac/
           roles.yaml                # Kubernetes RBAC
           bindings.yaml
        secrets/
           vault-config.hcl          # HashiCorp Vault
           secret-injection.yaml     # K8s secrets
        network/
           network-policies.yaml     # K8s network policies
     backend/
        src/
           api/                      # API services
           db/                       # Database models
        k8s/
           deployments.yaml          # K8s deployments
           services.yaml             # K8s services
     frontend/
        src/
           tokens.css                # Design tokens
           components/               # UI components
        k8s/
           deployment.yaml           # Frontend deployment
     devops/
        ci-cd/
           .github/workflows/        # GitHub Actions
           jenkins/                  # Jenkins pipelines
        deployment/
           deploy.sh                 # Deployment automation
           rollback.sh
     finops/
        cost-optimization/
           recommendations.csv       # Cost savings
        tagging/
           tag-policies/             # Cloud tag enforcement
     monitoring/
        prometheus/
           config.yaml               # Metrics collection
        grafana/
           dashboards/               # Observability dashboards

Integration Points:
═► Infrastructure + Security
   • Kubernetes RBAC configured
   • Network policies enforced
   • Pod security standards: {level}

═► Backend + Security
   • API authentication: {method}
   • Secrets managed by: {vault/k8s-secrets}
   • Database encryption: enabled

═► DevOps + Infrastructure
   • CI/CD deploys to: {k8s-cluster}
   • Deployment strategy: {rolling/blue-green/canary}
   • GitOps enabled: {yes/no}

═► FinOps + Cloud
   • Tagging enforced at: {deployment/account}
   • Cost allocation by: {namespace/service/team}
   • Budget alerts configured

[If frontend included:]
═► Frontend + Backend
   • API client: type-safe, generated
   • Authentication: JWT tokens
   • Theming: tokens.css (light/dark)

Deployment Order:
1. Provision infrastructure (Terraform/K8s cluster)
2. Configure security (RBAC, secrets, network policies)
3. Deploy backend services (K8s deployments)
4. [If frontend:] Deploy frontend (K8s/static hosting)
5. Configure CI/CD pipelines
6. Apply FinOps policies and monitoring

Next Steps:
1. Review generated configurations
2. Update environment variables and secrets
3. Run infrastructure provisioning: {command}
4. Deploy security policies: {command}
5. Deploy applications: {command}
6. Verify deployment: {command}

Would you like me to:
A) Generate the full implementation code
B) Explain any integration point in detail
C) Modify configurations for a specific domain
D) Add additional domains (data/ai-ml/developer)
```

---

## Error Handling

### No Common Domains

If goal is too vague to detect any domains:

```
⚠ Unable to Detect Domains

Your goal: "{user_goal}"

This seems like a multi-domain request, but I couldn't identify specific domains.

Could you clarify which areas you need?
□ Infrastructure (Kubernetes, Terraform)
□ Security (Secrets, RBAC, compliance)
□ DevOps (CI/CD, deployment automation)
□ Cloud (AWS, Azure, GCP)
□ Backend (APIs, databases)
□ Frontend (UI components)
□ FinOps (Cost optimization, tagging)
□ AI/ML (RAG, embeddings, model serving)

Select all that apply (comma-separated):
```

### Domain Conflicts

If domains have conflicting requirements:

```
⚠ DOMAIN CONFLICT DETECTED

security: Requires private network (no internet access)
devops: Requires GitHub Actions (public internet)

Recommendation:
- Use self-hosted GitHub Actions runners in private network
- OR use private GitLab CI/CD

Which approach?
A) Self-hosted runners (more secure, more complex)
B) Public CI/CD with network exceptions
C) Explain trade-offs in detail
```

### Skill Load Failures Across Domains

If skill from one domain fails:

```
⚠ ERROR: Skill '{skill.name}' from domain '{domain}' failed

Reason: {error_message}

This skill is in Phase {phase}. Other domains depend on it:
- {dependent_domain1}
- {dependent_domain2}

Options:
1. Retry this skill
2. Continue without (may affect dependent domains)
3. Stop and investigate

Your choice (1/2/3):
```

---

## Multi-Domain Guidelines

### 1. Respect Phase Dependencies
Never execute a skill from Phase 3 before Phase 1 completes.

### 2. Cross-Domain Context Sharing
Skills in later phases can reference configurations from earlier phases.

### 3. Integration Validation
After all phases, validate integration points between domains.

### 4. Avoid Redundancy
If multiple domains configure the same resource (e.g., Kubernetes), consolidate.

### 5. Domain Boundaries
Keep domain-specific code separate; use well-defined interfaces for integration.

---

## Summary

**Multi-domain orchestrator responsibilities:**
1. Detect all involved domains from user goal
2. Load appropriate registries for each domain
3. Organize domains into 4 execution phases
4. Execute skills in dependency order across phases
5. Track configurations per domain and per skill
6. Generate integrated multi-domain deliverables
7. Validate cross-domain integration points
8. Provide deployment guidance across all domains

**Key differences from single-domain orchestrators:**
- Manages MULTIPLE domains instead of one category
- Phases ensure proper dependency ordering
- Cross-domain context sharing for smart defaults
- Integration point validation is critical
- Generates unified project structure spanning all domains
