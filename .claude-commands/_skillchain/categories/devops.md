# DevOps Workflow Orchestrator

**Context Received:**
- Goal: {original_goal}
- Skills: {matched_skills}
- Category: devops
- Estimated: {estimated_time}, {estimated_questions} questions

---

## Step 1: Load Shared Resources

Read `{SKILLCHAIN_DIR}/_shared/execution-flow.md`

Store in context for all skills.

**Note:** DevOps workflows do not require theming-rules.md (frontend-only).

---

## Step 2: Confirm Skill Chain with User

Present detected chain:

```
TPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPW
Q  SKILL CHAIN DETECTED FOR: "{original_goal}"             Q
`PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPc
Q  MATCHED DEVOPS SKILLS:                                  Q
{for each matched skill with score > 0:}
Q    {n}. ⚙️ {skill.name} (matched: "{keyword}")            Q
Q          Plugin: {skill.invocation}                      Q
`PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPc
Q  Estimated time: {estimated_time}                        Q
Q  Estimated questions: {estimated_questions}              Q
`PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPc
Q  OPTIONS:                                                Q
Q    " Type "confirm" to proceed                           Q
Q    " Type "skip" to use all defaults (faster)            Q
Q    " Type "customize" to add/remove skills               Q
Q    " Type "help" to see workflow commands                Q
ZPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP]
```

Wait for user response:
- "confirm" → Proceed to Step 3
- "skip" → Set skip_all_questions = true, proceed to Step 3
- "customize" → Allow skill additions/removals, then proceed
- "help" → Show workflow commands from execution-flow.md

---

## Step 3: Skill Invocation Loop

Initialize:
```
skill_configs = {}
current_skill_index = 1
total_skills = len(confirmed_skills)
```

For each skill in confirmed_skills:

### 3.1 Announce Skill

```
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
 STEP {current_skill_index}/{total_skills}: {SKILL.NAME}
 Plugin: {skill.invocation}
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
```

### 3.2 Invoke Skill

```
Skill({ skill: "{skill.invocation}" })
```

**DevOps skill invocation strings:**
- writing-dockerfiles: `devops-skills:writing-dockerfiles`
- testing-strategies: `devops-skills:testing-strategies`
- managing-incidents: `devops-skills:managing-incidents`
- building-ci-pipelines: `devops-skills:building-ci-pipelines`
- implementing-gitops: `devops-skills:implementing-gitops`
- platform-engineering: `devops-skills:platform-engineering`

### 3.3 Load Questions

All DevOps skills use `questions.source: "skill"` format.

The skill's SKILL.md will be loaded when invoked. Extract questions from the section specified in the registry.

### 3.4 Ask User (unless skip_all_questions)

If skip_all_questions:
  Use defaults for all questions
Else:
  For each question in questions:
    Present question with:
      - Context from previous skills
      - Smart defaults based on goal keywords
      - Current answer if revisiting (for "back" command)
      - Dependency information if applicable

    Wait for answer or workflow command:
      - Answer → Store and continue
      - "skip" → Use default for this question
      - "back" → Return to previous skill
      - "status" → Show progress, re-ask question
      - "done" → Break loop, proceed to output generation
      - "restart" → Go back to Step 2

### 3.5 Store Configuration

```
skill_configs[skill.name] = {
  answers: user_answers,
  invocation: skill.invocation,
  priority: skill.priority,
  dependencies: skill.dependencies
}

current_skill_index += 1
```

---

## Step 4: Generate DevOps Output

**IMPORTANT:** DevOps workflows DO NOT use `assembling-components` skill (frontend-only).

Instead, generate DevOps artifacts directly:

### 4.1 Analyze Collected Configurations

Review all `skill_configs` to identify:
- Containerization requirements (Dockerfile patterns)
- Testing frameworks and coverage targets
- CI/CD pipeline structure and tools
- GitOps deployment approach
- Platform engineering components
- Incident management processes

### 4.2 Identify Integration Points

Detect where skills need to interact:
- Docker builds in CI pipelines
- Testing stages in pipeline workflow
- GitOps syncing with CI/CD outputs
- Platform portal integrating all components
- Incident runbooks referencing deployment processes

### 4.3 Generate Production-Ready Artifacts

Create complete DevOps implementation:

```
TPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPW
Q  GENERATING DEVOPS ARTIFACTS FOR: "{original_goal}"      Q
`PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPc
Q  Based on configurations:                                Q
{for each skill in skill_configs:}
Q    ⚙️ {skill.name}: {summary of choices}                  Q
ZPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP]

Generating:
  1. Dockerfiles and container configurations
  2. Test suites and coverage configs
  3. CI pipeline definitions
  4. GitOps manifests and sync configs
  5. Platform engineering templates
  6. Incident response runbooks
```

### 4.4 Output Organization

Organize artifacts by DevOps domain:

```
devops/
├── docker/
│   ├── Dockerfile
│   ├── .dockerignore
│   └── docker-compose.yml
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── coverage.config.js
├── .github/workflows/          # or .gitlab-ci.yml, Jenkinsfile, etc.
│   ├── ci.yml
│   ├── deploy.yml
│   └── release.yml
├── gitops/
│   ├── argocd/                # or flux/
│   ├── base/
│   ├── overlays/
│   └── sync-policy.yaml
├── platform/
│   ├── backstage/             # or other IDP
│   ├── templates/
│   └── catalog-info.yaml
├── runbooks/
│   ├── incident-response.md
│   ├── on-call-guide.md
│   └── rollback-procedure.md
└── README.md
```

### 4.5 Validation Checklist

Verify generated artifacts include:
- [ ] Dockerfiles optimized (multi-stage, layer caching)
- [ ] Test coverage configured per user preferences
- [ ] CI pipeline stages properly ordered
- [ ] GitOps sync policies defined
- [ ] Platform catalog entries created
- [ ] Incident runbooks actionable and clear
- [ ] All secrets handled via environment variables
- [ ] README with setup and usage instructions
- [ ] Version control ignores (.gitignore, .dockerignore)

### 4.6 Present Output

Display generated files with explanations:

```
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
 🚀 DEVOPS IMPLEMENTATION COMPLETE
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP

Generated {file_count} files across {skill_count} DevOps skills:

KEY FILES:
  📦 {dockerfile_path}           - Container configuration
  🧪 {test_config_path}          - Testing framework setup
  ⚙️ {ci_pipeline_path}          - CI/CD pipeline definition
  🔄 {gitops_manifest_path}      - GitOps deployment config
  🏗️ {platform_catalog_path}     - Platform catalog entry
  📖 {runbook_path}              - Incident response guide

NEXT STEPS:
  1. Review Dockerfile and build locally: {docker_build_cmd}
  2. Run tests: {test_command}
  3. Push code to trigger CI pipeline
  4. Monitor GitOps sync: {gitops_monitor_cmd}
  5. Register with platform: {platform_register_cmd}

PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
```

---

## Error Handling

### Skill Invocation Failure

If skill invocation fails:

```
❌ ERROR: Skill '{skill.name}' failed to load

Plugin: {skill.invocation}
Reason: {error_message}

Options:
1. Continue with remaining skills (skip this one)
2. Retry this skill
3. Stop workflow and show partial progress

Your choice (1/2/3):
```

Handle user choice:
- 1 → Mark skill as skipped, continue to next skill
- 2 → Re-invoke skill, reset current_skill_index
- 3 → Stop loop, proceed to Step 4 with partial configs

### Dependency Failures

When a dependent skill was skipped/failed:

```
⚠️ WARNING: '{skill.name}' depends on '{dependency}' which was skipped.

Example: building-ci-pipelines depends on testing-strategies.
Without test configuration, CI pipeline will use default test commands.

Continue? (yes/no)
```

If "no" → Allow user to go back and configure dependency

### Invalid Configuration Combinations

Detect incompatible choices:

```
⚠️ CONFIGURATION CONFLICT DETECTED

building-ci-pipelines specified: GitHub Actions
platform-engineering specified: GitLab (includes built-in CI)

Options:
1. Use GitHub Actions (more flexible, external platform)
2. Use GitLab CI (integrated, simpler setup)
3. Go back and reconfigure

Your choice (1/2/3):
```

---

## DevOps Skill Ordering

Follow these ordering principles when invoking DevOps skills:

1. **Foundation** (priority 3-5):
   - writing-dockerfiles (priority 3)
   - testing-strategies (priority 5)

2. **Incident Management** (priority 8):
   - managing-incidents (priority 8)

3. **Automation** (priority 10-15):
   - building-ci-pipelines (priority 10, depends on testing-strategies)
   - implementing-gitops (priority 15)

4. **Platform** (priority 20):
   - platform-engineering (priority 20, highest level abstraction)

**Recommended sequences:**

**Full DevOps Pipeline:**
```
1. writing-dockerfiles
2. testing-strategies
3. building-ci-pipelines (uses Docker + tests)
4. implementing-gitops
5. platform-engineering (integrates all)
6. managing-incidents
```

**Quick Docker + CI:**
```
1. writing-dockerfiles
2. testing-strategies
3. building-ci-pipelines
```

**GitOps Focus:**
```
1. implementing-gitops
2. managing-incidents
```

---

**Orchestrator Complete - Lines: 195**
