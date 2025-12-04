# Skill Orchestration Plan

**Created:** December 3, 2025
**Status:** Active
**Total Skills to Create:** 40 init.md files remaining (47 proposed - 7 already done)

---

## Current State Analysis

### Existing Skills (29 with SKILL.md - Production Ready)
```
UI/UX Skills (15):
- building-forms, building-tables, building-ai-chat, creating-dashboards
- providing-feedback, implementing-navigation, implementing-search-filter
- designing-layouts, displaying-timelines, managing-media, guiding-users
- implementing-drag-drop, theming-components, visualizing-data, assembling-components

Backend Skills (14):
- api-patterns, databases-relational, databases-document, databases-vector
- databases-graph, databases-timeseries, message-queues, realtime-sync
- auth-security, model-serving, deploying-applications, ai-data-engineering
- observability, ingesting-data
```

### Phase 1 Skills (6 with init.md - Ready for SKILL.md)
```
1. testing-strategies       ✅ init.md complete (1790 lines, comprehensive)
2. building-ci-pipelines    ✅ init.md exists (needs review)
3. kubernetes-operations    ✅ init.md exists (needs review)
4. infrastructure-as-code   ✅ init.md complete (770 lines, comprehensive)
5. security-hardening       ✅ init.md exists (needs review)
6. secret-management        ✅ init.md exists (needs review)
```

### Phase 2 Skills (Directories Created, Need init.md)
```
7. gitops-workflows         ❌ Empty directory
8. linux-administration     ❌ Empty directory
9. network-architecture     ❌ Empty directory
10. load-balancing-patterns ❌ Empty directory
11. disaster-recovery       ❌ Empty directory
12. performance-engineering ✅ init.md exists
```

### Phase 3-4 Skills (Not Yet Started - 35 skills)
Detailed in PROPOSED_SKILLS.md

---

## Multi-Language Support Matrix

### MULTI-LANGUAGE Skills (TypeScript/Python/Go/Rust Examples Required)

| Skill | Primary Languages | Rationale |
|-------|-------------------|-----------|
| `testing-strategies` | TS, Python, Go, Rust | Testing frameworks differ by language |
| `building-clis` | Python, Go, Rust | CLI frameworks are language-specific |
| `sdk-design` | TS, Python, Go | SDK patterns vary by language |
| `debugging-techniques` | Python, Go, Rust | Debuggers are language-specific |
| `data-transformation` | Python, SQL, Spark | Data tools vary |
| `streaming-data` | Python, Java/Scala, Go | Stream processing frameworks |
| `performance-engineering` | TS, Python, Go, Rust | Profiling tools differ |
| `shell-scripting` | Bash, Zsh | Shell-focused |
| `sql-optimization` | SQL dialects | PostgreSQL, MySQL, etc. |

### Multi-Tool/Platform Skills (Multiple IaC/Config Tools)

| Skill | Tools Covered |
|-------|---------------|
| `infrastructure-as-code` | Terraform/OpenTofu, Pulumi (TS/Py/Go), CDK, CloudFormation |
| `building-ci-pipelines` | GitHub Actions, GitLab CI, Jenkins, Tekton/Argo |
| `gitops-workflows` | ArgoCD, Flux |
| `configuration-management` | Ansible, Chef, Puppet |
| `kubernetes-operations` | kubectl, Helm, Kustomize, Operators |
| `service-mesh` | Istio, Linkerd, Cilium |
| `container orchestration` | Docker, Podman, containerd |

### Single-Domain/Config Skills (YAML/Config/Design Patterns)

| Category | Skills |
|----------|--------|
| **Networking** | network-architecture, load-balancing-patterns, dns-management, configuring-nginx, configuring-firewalls |
| **Security** | security-architecture, compliance-frameworks, security-hardening, secret-management, vulnerability-management, siem-logging, implementing-tls |
| **DevOps** | platform-engineering, disaster-recovery, incident-management, writing-github-actions |
| **Cloud** | aws-patterns, gcp-patterns, azure-patterns, cost-optimization, resource-tagging |
| **AI/ML** | mlops-patterns, prompt-engineering, llm-evaluation, embedding-optimization |
| **Data** | data-architecture |

### Python-Primary Skills (with optional TS)

| Skill | Primary | Secondary |
|-------|---------|-----------|
| `prompt-engineering` | Python | TypeScript |
| `llm-evaluation` | Python | TypeScript |
| `embedding-optimization` | Python | - |
| `mlops-patterns` | Python | YAML configs |

---

## Wave Execution Strategy

### Wave 1: Validate Phase 1 (Already Done - 7 init.md files)
**Status:** Complete - validate quality only

### Wave 2: Phase 2 Remaining (5 skills) - IMMEDIATE
**Agent Count:** 5 parallel agents
```
1. gitops-workflows
2. linux-administration
3. network-architecture
4. load-balancing-patterns
5. disaster-recovery
```

### Wave 3: Security Skills (6 skills)
**Agent Count:** 6 parallel agents
```
1. security-architecture (High Level)
2. compliance-frameworks (High Level)
3. vulnerability-management (Mid Level)
4. siem-logging (Mid Level)
5. implementing-tls (Low Level)
6. configuring-firewalls (Low Level)
```

### Wave 4: Developer Productivity (7 skills)
**Agent Count:** 7 parallel agents
```
1. api-design-principles (High Level)
2. building-clis (Mid Level) - MULTI-LANGUAGE
3. sdk-design (Mid Level) - MULTI-LANGUAGE
4. documentation-generation (Mid Level)
5. debugging-techniques (Low Level) - MULTI-LANGUAGE
6. git-workflows (Low Level)
7. writing-github-actions (Low Level)
```

### Wave 5: Infrastructure & Networking (6 skills)
**Agent Count:** 6 parallel agents
```
1. designing-distributed-systems (High Level)
2. configuration-management (Mid Level)
3. dns-management (Mid Level)
4. service-mesh (Mid Level)
5. configuring-nginx (Low Level)
6. shell-scripting (Low Level)
```

### Wave 6: DevOps & Platform (5 skills)
**Agent Count:** 5 parallel agents
```
1. platform-engineering (High Level)
2. incident-management (Mid Level)
3. cost-optimization (Mid Level)
4. resource-tagging (Low Level)
5. writing-dockerfiles (Low Level)
```

### Wave 7: Data & Analytics (4 skills)
**Agent Count:** 4 parallel agents
```
1. data-architecture (High Level)
2. streaming-data (Mid Level) - MULTI-LANGUAGE
3. data-transformation (Mid Level) - MULTI-LANGUAGE
4. sql-optimization (Low Level)
```

### Wave 8: AI/ML Operations (4 skills)
**Agent Count:** 4 parallel agents
```
1. mlops-patterns (High Level)
2. prompt-engineering (Mid Level)
3. llm-evaluation (Mid Level)
4. embedding-optimization (Low Level)
```

### Wave 9: Cloud-Specific (3 skills)
**Agent Count:** 3 parallel agents
```
1. aws-patterns (Mid Level)
2. gcp-patterns (Mid Level)
3. azure-patterns (Mid Level)
```

---

## Agent Instructions Template

### Standard Agent Prompt for init.md Creation

```
You are creating an init.md master plan for the `{skill-name}` skill.

## Your Task
Create a comprehensive init.md file following the established pattern from existing skills.

## Required Sections

1. **Header Block**
   - Skill Name, Level (High/Mid/Low), Status, Last Updated

2. **Table of Contents**
   - All major sections linked

3. **Strategic Positioning**
   - Why this skill matters (2025 context)
   - Market drivers
   - How it differs from existing solutions
   - Target audience

4. **Skill Purpose and Scope**
   - What this skill teaches (core competencies)
   - What it does NOT cover
   - Success criteria

5. **Research Findings**
   - Use Google Search Grounding for 2025 trends
   - Use Context7 for library documentation
   - Document research date and tools used
   - Key trends identified

6. **Component Taxonomy**
   - Tiered organization (patterns, tools, approaches)
   - Clear categorization

7. **Decision Frameworks**
   - When to use which approach
   - Decision trees or matrices
   - Trade-off analysis

8. **{Multi-Language OR Tool-Specific} Implementations**
   - Code examples for each language/tool
   - Practical, copy-paste ready

9. **Library Recommendations**
   - Primary and alternative libraries
   - Trust scores from Context7
   - Code snippet counts
   - Installation commands
   - Working examples

10. **Skill Structure Design**
    - Proposed file organization
    - SKILL.md structure
    - Progressive disclosure strategy

11. **Integration Points**
    - How this skill connects to others
    - Skill chaining patterns

12. **Implementation Roadmap**
    - Phased delivery plan

## Research Requirements

1. **Google Search Grounding** (use mcp__litellm__gs-google_search_grounding)
   - Query: "{skill-name} best practices 2025"
   - Query: "{skill-name} tools comparison 2025"
   - Query: "{skill-name} {primary-tool} vs {alternative-tool}"

2. **Context7 Library Research** (use mcp__litellm__context7-resolve-library-id, mcp__litellm__context7-get-library-docs)
   - Resolve library IDs for primary tools
   - Get documentation with relevant topics
   - Extract trust scores and snippet counts

## Quality Standards

- Target 500-1500 lines (varies by skill level)
- High Level skills: 800-1200 lines
- Mid Level skills: 500-800 lines
- Low Level skills: 300-500 lines

- Include working code examples
- All library recommendations must have research backing
- Decision frameworks must be actionable
- Follow SKILLS_BEST_PRACTICE.md guidelines

## Output

Write the complete init.md file to:
/Users/antoncoleman/Documents/repos/ai-design-components/skills/{skill-name}/init.md

Create the directory if it doesn't exist.
```

---

## Skill Level Definitions (from PROPOSED_SKILLS.md)

### High Level Skills (Strategic/Architectural)
- **Scope:** Cross-cutting concerns, architectural patterns, decision frameworks
- **Token Budget:** 8,000-12,000 tokens
- **init.md Target:** 800-1200 lines

### Mid Level Skills (Implementation Patterns)
- **Scope:** Specific technology implementations, integration patterns
- **Token Budget:** 5,000-8,000 tokens
- **init.md Target:** 500-800 lines

### Low Level Skills (Tactical/Quick Reference)
- **Scope:** Single-purpose utilities, quick patterns, specific tools
- **Token Budget:** 2,000-5,000 tokens
- **init.md Target:** 300-500 lines

---

## Success Metrics

### Per-Agent Deliverable
- [ ] init.md file created in correct location
- [ ] Research conducted (Google Search + Context7)
- [ ] All required sections present
- [ ] Working code examples included
- [ ] Library recommendations with trust scores
- [ ] Decision frameworks are actionable
- [ ] Appropriate length for skill level

### Overall Project Success
- [ ] All 47 proposed skills have init.md files
- [ ] Multi-language skills have TS/Python/Go/Rust examples
- [ ] Integration points mapped between skills
- [ ] Consistent quality across all init.md files

---

## Execution Commands

### Wave 2 Launch (5 Agents)
```
Launch agents in parallel for:
1. gitops-workflows
2. linux-administration
3. network-architecture
4. load-balancing-patterns
5. disaster-recovery
```

Each agent receives:
- The standard agent prompt template
- Skill-specific parameters (name, level, multi-language flag)
- Access to SKILLS_BEST_PRACTICE.md
- Access to RESEARCH_GUIDE.md
- Research tool access (Google Search, Context7)

---

## Notes

- Agents should run in parallel within each wave
- Each agent is stateless - provide complete instructions
- Monitor for research tool failures (retry up to 4 times)
- Validate output quality before proceeding to next wave
