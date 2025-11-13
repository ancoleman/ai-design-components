# Anthropic skill-creator Analysis & Key Learnings

**Date:** November 13, 2025
**Source:** https://github.com/anthropics/skills/tree/main/skill-creator
**Files Analyzed:** 5 (SKILL.md, LICENSE.txt, 3 Python scripts)

---

## Files Fetched

1. **SKILL.md** - Complete skill creation guide
2. **LICENSE.txt** - Apache License 2.0
3. **scripts/init_skill.py** - Generates new skill templates
4. **scripts/package_skill.py** - Creates distributable ZIP files
5. **scripts/quick_validate.py** - Validates skill structure

---

## Key Learnings from Anthropic's skill-creator

### 1. Skill Creation Process (6 Steps)

Anthropic recommends a structured workflow:

**Step 1: Understanding with Concrete Examples**
- Ask users for specific examples
- "What would trigger this skill?"
- Avoid overwhelming with questions
- Get clarity before building

**Step 2: Planning Reusable Contents**
- Analyze each example
- Identify: scripts, references, assets needed
- Determine what's repetitive (→ scripts)
- Determine what's reference material (→ references)

**Step 3: Initialize the Skill**
- Run `init_skill.py` to generate template
- Creates proper structure automatically
- Includes example files in each directory

**Step 4: Edit the Skill**
- Write for another Claude instance to use
- Focus on non-obvious information
- Use imperative/infinitive form (not "you should")
- Answer: purpose, when to use, how to use

**Step 5: Package the Skill**
- Run `package_skill.py` to create ZIP
- Automatically validates first
- Checks frontmatter, naming, structure

**Step 6: Iterate**
- Test on real tasks
- Notice struggles
- Update skill
- Test again

**⭐ Key Insight:** Anthropic emphasizes starting with concrete examples, not abstract theory.

---

### 2. Progressive Disclosure (3 Levels)

Anthropic explicitly documents the loading model:

**Level 1: Metadata** (~100 words)
- Always in context
- Name + description from YAML

**Level 2: SKILL.md body** (<5k words)
- Loaded when skill triggers
- Keep lean and focused

**Level 3: Bundled resources** (unlimited)
- Scripts: Executed without loading into context
- References: Loaded only when Claude decides it's needed
- Assets: Never loaded (used in output)

**⭐ Key Insight:** Scripts can be executed WITHOUT loading into context = infinite complexity with zero token cost.

---

### 3. File Organization Best Practices

**scripts/**
- Executable code for deterministic tasks
- Token-efficient (execution without context loading)
- For repeatedly rewritten code

**references/**
- Documentation Claude should reference
- Loaded as needed
- Keep SKILL.md lean, move details here
- Avoid duplication with SKILL.md

**assets/**
- Files used in OUTPUT
- Templates, images, boilerplate
- NEVER loaded into context
- Copied or modified for final product

**⭐ Key Insight:** Clear separation between scripts (execute), references (read), and assets (use).

---

### 4. YAML Frontmatter Requirements

**Required Fields:**
- `name:` - hyphen-case (lowercase, digits, hyphens only)
  - Cannot start/end with hyphen
  - No consecutive hyphens
  - No spaces, underscores, camelCase

- `description:` - What and when to use
  - Cannot contain angle brackets (< or >)
  - Should be specific about triggers

**Optional Fields:**
- `license:` - Reference to license file

**Validation:**
- Enforced by `quick_validate.py`
- Checks frontmatter format
- Validates naming convention
- Ensures description quality

---

### 5. Writing Style Guidelines

**From SKILL.md:**

**✅ Use Imperative/Infinitive Form:**
- "To accomplish X, do Y"
- "Create a file..."
- "Execute the script..."

**❌ Avoid Second Person:**
- NOT "You should do X"
- NOT "If you need to do X"

**Why:** Maintains consistency and clarity for AI consumption

**⭐ Key Insight:** Write objectively, as instructions, not conversation.

---

### 6. Tool Scripts (Anthropic Provides)

**init_skill.py:**
- Generates skill template automatically
- Creates SKILL.md with TODOs
- Creates example scripts/, references/, assets/
- Usage: `scripts/init_skill.py <skill-name> --path <output-dir>`

**package_skill.py:**
- Creates distributable ZIP
- Validates BEFORE packaging
- Preserves directory structure
- Usage: `scripts/package_skill.py <skill-folder> [output-dir]`

**quick_validate.py:**
- Validates skill structure
- Checks frontmatter format
- Enforces naming conventions
- Usage: `python quick_validate.py <skill_directory>`

**⭐ Key Insight:** Anthropic provides tooling to enforce best practices.

---

### 7. Skill Structure Approaches (4 Patterns)

From the SKILL.md template, Anthropic identifies 4 structural patterns:

**1. Workflow-Based**
- Sequential multi-step processes
- Example: "To build a frontend app, follow these steps..."
- When: Clear procedural workflows

**2. Task-Based**
- Collection of related tools/capabilities
- Example: "This skill provides tools for PDF manipulation..."
- When: Multiple related but independent tasks

**3. Reference/Guidelines**
- Standards, policies, best practices
- Example: "Follow these brand guidelines..."
- When: Ensuring compliance or consistency

**4. Capabilities-Based**
- Integrated system combining workflows + tools + references
- Example: "This skill helps analyze BigQuery data using schemas and scripts..."
- When: Complex domains needing multiple resources

**⭐ Key Insight:** Our component skills are mostly "Capabilities-Based" (workflows + references + examples + tokens).

---

## How This Applies to Our Component Library

### What We're Doing Right ✅

1. **✅ init.md files as master plans**
   - Aligns with Step 1-2 (understanding + planning)
   - We have comprehensive planning docs

2. **✅ Progressive disclosure design**
   - Our structure: init.md → SKILL.md → references/ → examples/
   - Matches Anthropic's 3-level model

3. **✅ References to RESEARCH_GUIDE.md**
   - Follows Anthropic pattern (reference files)
   - Loaded only when needed

4. **✅ Design tokens as bundled resource**
   - tokens/ directory = assets or references
   - Can be used without loading into context

5. **✅ Styling sections reference design-tokens skill**
   - Cross-skill references (good pattern)

---

### What We Should Adjust 🔧

#### 1. Naming Convention

**Current:** Some files might not follow hyphen-case
**Should be:** All lowercase, hyphens only (no underscores, camelCase)

**Examples:**
- ✅ design-tokens
- ✅ ai-chat
- ✅ data-viz
- ✅ search-filter
- ✅ drag-drop

**Check:** All our skill names already follow this! ✅

---

#### 2. Description Format (Third Person)

**Current:** Some descriptions might use second person
**Should use:** Third person, objective

**Example:**
```yaml
# ❌ Avoid
description: Use this skill when you want to create forms...

# ✅ Correct
description: This skill should be used when creating forms, validation patterns, or input components...
```

**Action:** Review all frontmatter descriptions

---

#### 3. SKILL.md Writing Style

**When we create SKILL.md files:**

**✅ Use:**
- "To create a bar chart, use Recharts..."
- "Execute the validation script..."
- "Reference the color-system.md file..."

**❌ Avoid:**
- "You should use Recharts..."
- "If you want to create a chart..."
- "You can reference..."

---

#### 4. Create Utility Scripts

**Anthropic provides 3 utility scripts. We should create equivalents:**

**Our needed scripts:**
```
scripts/
├── init_component_skill.py    # Like init_skill.py
├── validate_skill.py           # Like quick_validate.py
└── package_skill.py            # Like package_skill.py
```

**Why:** Automate skill creation, enforce standards, package for distribution

---

#### 5. Example Files in Each Skill

**Anthropic's init_skill.py creates:**
- scripts/example_script.py (with TODO comments)
- references/api_reference.md (with TODO sections)
- assets/ directory (for templates)

**We should:**
- Create example files when building SKILL.md
- Or reference to create them during implementation

---

### 6. Validation Checks

**From quick_validate.py, check:**
- ✅ YAML frontmatter exists and is valid
- ✅ name field present and hyphen-case
- ✅ description field present and no angle brackets
- ✅ SKILL.md file exists
- ✅ No consecutive hyphens in name
- ✅ Name doesn't start/end with hyphen

**We should add:** Validation script for our skills

---

## Recommended Actions for Our Component Library

### Immediate Actions:

**1. Create Utility Scripts** (High Priority)
```bash
# Create in project root
scripts/
├── init_component_skill.py    # Generate new component skill
├── validate_skill.py           # Validate structure
└── package_skill.py            # Create distributable ZIP
```

**Benefits:**
- Enforce naming conventions
- Validate frontmatter
- Automate skill creation
- Package for distribution

---

**2. Validate Existing Skills** (Medium Priority)
```bash
# Run validation on all 14 skills
for skill in skills/*/; do
  python scripts/validate_skill.py "$skill"
done
```

**Check:**
- Frontmatter format
- Naming conventions
- Description quality
- File structure

---

**3. Review Descriptions** (Low Priority - Probably Fine)

Ensure all YAML descriptions use third person:
- "This skill should be used when..."
- NOT "Use this skill when..."
- NOT "You can use this when..."

---

**4. Document Writing Style** (For Implementation Phase)

When creating SKILL.md files:
- Use imperative/infinitive form
- Be objective (not conversational)
- Write instructions, not guidance
- Example: "To build a dashboard, combine..."

---

## Key Takeaways

### 1. **Scripts are Token-Free**

Most important insight:
```
Scripts can be EXECUTED without being LOADED into context.
= Infinite code complexity with ZERO token cost.
```

**Application:**
- Token generation scripts (free)
- Validation scripts (free)
- Data processing (free)
- Complex algorithms (free)

**This changes everything.** We can have sophisticated scripts with no context penalty.

---

### 2. **Progressive Disclosure is Critical**

Anthropic explicitly models 3 levels:
```
Metadata (always) → SKILL.md (when triggered) → Resources (as needed)
```

**Our structure matches:**
```
Frontmatter (always) → SKILL.md (when triggered) → references/ (as needed)
                                                  → examples/ (as needed)
                                                  → scripts/ (executed)
```

---

### 3. **Start with Concrete Examples**

Anthropic emphasizes:
- Don't start with abstract theory
- Get real examples from users
- Analyze what's repetitive
- Build skill around actual needs

**Application:**
- When implementing skills, start with real use cases
- Test with actual component building
- Iterate based on usage

---

### 4. **Validation Matters**

Anthropic provides validation scripts because:
- Naming conventions matter (hyphen-case)
- Frontmatter format matters
- Description quality matters

**Application:**
- We should validate our skills before "implementation complete"
- Create automated validation
- Enforce standards

---

### 5. **Packaging for Distribution**

Anthropic packages skills as ZIP files:
- Makes sharing easy
- Preserves structure
- Validates before packaging

**Application:**
- When skills are complete, package them
- Share with community
- Distribute to teams

---

## Comparison: Our Approach vs. Anthropic's

| Aspect | Anthropic skill-creator | Our Component Library | Status |
|--------|------------------------|---------------------|--------|
| **init.md** | Not mentioned | Master plan docs | ✅ Our enhancement |
| **SKILL.md** | Required, lean | To be created | ⏸️ Implementation phase |
| **Progressive disclosure** | 3 levels explicit | Matches pattern | ✅ Aligned |
| **scripts/** | Executable, token-free | Planned | ⏸️ To implement |
| **references/** | Loaded as needed | Planned | ⏸️ To implement |
| **assets/** | For output | Planned | ⏸️ To implement |
| **Naming** | hyphen-case enforced | Already correct | ✅ Aligned |
| **Frontmatter** | name + description | Documented | ✅ Aligned |
| **Writing style** | Imperative form | To apply | ⏸️ Implementation |
| **Validation** | Python scripts | Should create | 📝 TODO |
| **Packaging** | ZIP distribution | Should create | 📝 TODO |
| **Research methodology** | Not mentioned | RESEARCH_GUIDE.md | ✅ Our innovation |

---

## Recommendations for Next Steps

### Before Implementation:

**1. Create Utility Scripts** (30 mins)
```python
scripts/init_component_skill.py   # Based on Anthropic's init_skill.py
scripts/validate_skill.py          # Based on quick_validate.py
scripts/package_skill.py           # Based on package_skill.py
```

**2. Validate All Existing Skills** (15 mins)
```bash
python scripts/validate_skill.py skills/design-tokens/
# ... for all 14 skills
```

**3. Review Frontmatter Descriptions** (15 mins)
- Ensure third-person ("This skill should be used...")
- Check for angle brackets
- Verify specificity

---

### During Implementation:

**1. Follow 6-Step Process**
- Start with concrete examples (Step 1)
- Plan resources (Step 2)
- Use init script (Step 3) [or create manually]
- Edit SKILL.md (Step 4)
- Package when complete (Step 5)
- Iterate based on usage (Step 6)

**2. Use Imperative Writing Style**
- "To build a form, use React Hook Form..."
- "Reference the validation-patterns.md file..."
- NOT "You should use..." or "You can..."

**3. Leverage Scripts Heavily**
- Token generation: FREE (scripts/ executed)
- Theme building: FREE
- Validation: FREE
- Color palette generation: FREE
- Schema generation: FREE

---

## Differences: Our Innovations

### 1. **init.md Master Plans** (Our Innovation)

Anthropic doesn't have "master plan" documents.

**Our init.md provides:**
- Strategic positioning
- Complete component taxonomy
- Decision frameworks
- Library research
- Implementation roadmap

**Benefit:** Clear planning before building SKILL.md

---

### 2. **RESEARCH_GUIDE.md** (Our Innovation)

Anthropic doesn't teach library research methodology.

**Our RESEARCH_GUIDE.md provides:**
- How to validate libraries
- How to use available tools
- Query formulation patterns
- Evaluation criteria

**Benefit:** Evergreen, adaptable, teachable

---

### 3. **Design Tokens as Cross-Skill Resource** (Our Innovation)

Anthropic examples show self-contained skills.

**Our approach:**
- design-tokens skill = foundation
- All component skills reference it
- Shared theming system

**Benefit:** Consistency across all components

---

## What to Keep from Anthropic

### ✅ Keep These Patterns:

1. **Progressive disclosure** (3 levels)
2. **Naming conventions** (hyphen-case)
3. **Frontmatter requirements** (name, description)
4. **Directory structure** (scripts, references, assets)
5. **Validation before packaging**
6. **Concrete examples first**
7. **Imperative writing style**
8. **Token-free script execution**

---

## What to Add from Anthropic

### 📝 Add These Tools:

**1. Validation Script**
```python
# scripts/validate_skill.py
# Check frontmatter, naming, structure
```

**2. Packaging Script**
```python
# scripts/package_skill.py
# Create distributable ZIP files
```

**3. Init Script** (Optional - we already have init.md)
```python
# scripts/init_component_skill.py
# Generate skill template from init.md
```

---

## Application to Implementation Phase

### When Building Our First SKILL.md:

**Follow Anthropic's Pattern:**

1. **Concrete Examples First**
   - What are real use cases?
   - "Build a login form with email/password"
   - "Create a bar chart showing monthly sales"
   - "Display KPI cards with trend indicators"

2. **Identify Resources**
   - Scripts: Token generation, validation
   - References: Detailed component docs
   - Assets: Code templates, example data

3. **Write Lean SKILL.md**
   - Purpose: 2-3 sentences
   - When to use: Specific triggers
   - How to use: Reference bundled resources

4. **Use Imperative Style**
   - "Reference color-system.md for palettes"
   - "Execute validate_tokens.py to check"
   - NOT "You can reference..." or "You should..."

---

## Structure Validation Checklist

Based on Anthropic's quick_validate.py:

**For Each Skill:**
- [ ] SKILL.md exists
- [ ] Frontmatter starts with `---`
- [ ] Frontmatter ends with `---`
- [ ] `name:` field present
- [ ] Name is hyphen-case (lowercase, hyphens only)
- [ ] Name doesn't start/end with hyphen
- [ ] No consecutive hyphens (`--`)
- [ ] `description:` field present
- [ ] Description has no angle brackets
- [ ] Description is third-person ("This skill...")

---

## Immediate Next Steps

**Before implementing any skill:**

1. **Create validation script** (high value, 30 mins)
2. **Validate all 14 existing init.md frontmatter** (15 mins)
3. **Fix any validation errors** (varies)
4. **Then proceed with implementation** (pick a skill)

**Benefits:**
- Ensures compliance with Anthropic standards
- Catches issues early
- Automated quality assurance

---

## Summary

**What Anthropic teaches us:**
1. Start with concrete examples (not theory)
2. Progressive disclosure is explicit (3 levels)
3. Scripts are token-free (execute without context)
4. Naming conventions matter (hyphen-case enforced)
5. Validation before packaging (automated)
6. Imperative writing style (objective instructions)

**What we innovate:**
1. Master plans (init.md) - strategic planning
2. Research methodology (RESEARCH_GUIDE.md) - evergreen
3. Design tokens cross-skill - consistency
4. Library recommendations - validated choices

**Combined:** We have Anthropic's best practices + our innovations = superior foundation

---

**Ready to create utility scripts and validate our skills before implementation?**
