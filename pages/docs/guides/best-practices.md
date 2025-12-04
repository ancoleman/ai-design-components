---
sidebar_position: 3
title: Skills Best Practices
description: Anthropic's official guidelines for skill development
---

# Skills Best Practices

Comprehensive best practices for developing Claude Skills, based on Anthropic's official guidelines and our experience with AI Design Components.

## Core Principles

### 1. Conciseness is Critical

**Context window is a public good** - minimize token usage

- Only include what Claude doesn't already know
- Remove general knowledge; focus on specialized, domain-specific information
- Keep SKILL.md under 500 lines
- Use progressive disclosure for additional content

**Example:**
- ❌ Bad: "React is a JavaScript library for building user interfaces. It was created by Facebook..."
- ✅ Good: "Use React Hook Form for forms. It reduces re-renders by 30-40% vs Formik."

### 2. Appropriate Degrees of Freedom

Choose the right format based on how deterministic the task is:

**High Freedom (Text Instructions):**
- Multiple valid approaches exist
- Context-dependent decisions
- Creative problem-solving needed
- Example: "Design a dashboard layout considering user's data density preferences"

**Medium Freedom (Templates/Config):**
- Preferred patterns with acceptable variation
- Structured but flexible
- Example: Component templates with configurable props

**Low Freedom (Executable Scripts):**
- Fragile operations requiring consistency
- Deterministic processes
- Example: Token generation, validation scripts

**Key Insight:** Scripts execute WITHOUT being loaded into context = zero token cost!

### 3. Progressive Disclosure Design

Structure information in layers:

**Level 1:** Metadata (name + description) - Always in context (~100 words)
**Level 2:** SKILL.md body - Loaded when triggered (&lt;5k words ideal)
**Level 3:** Bundled resources - Loaded/executed as needed (unlimited)

**Rules:**
- Main SKILL.md references additional files (one level deep only)
- Avoid deeply nested references (SKILL.md → file.md → another.md is BAD)
- All reference files should link directly from SKILL.md
- Use descriptive filenames: `chart-types.md`, not `doc2.md`

### 4. Evaluation-Driven Development

Build skills through iteration:

1. **Identify gaps** - Run tasks without Skill first, document failures
2. **Create evaluations** - Build 3+ test scenarios
3. **Establish baseline** - Measure performance without Skill
4. **Write minimal instructions** - Just enough to pass evaluations
5. **Iterate** - Execute evaluations and refine

**Two-Claude Method:**
- **Claude A** (expert) - Designs and refines the Skill
- **Claude B** (agent) - Uses the Skill for real work
- Test with Claude B on real tasks, return to Claude A with observations

## Skill Development Guidelines

### Naming Convention

Use **gerund form** (verb + -ing):
- ✅ Good: `building-forms`, `visualizing-data`, `processing-pdfs`, `analyzing-spreadsheets`
- ❌ Bad: `form-builder`, `data-viz-helper`, `pdf-processor`, `tools`

**Requirements:**
- Lowercase with hyphens only
- Max 64 characters
- Descriptive and action-oriented
- No starting/ending hyphens or consecutive hyphens

### SKILL.md Structure

**Frontmatter (Required):**
```yaml
---
name: skill-name              # lowercase, hyphens, gerund form
description: What this skill does AND when to use it (max 1024 chars)
---
```

**Description Requirements:**
- Include both WHAT and WHEN
- Use third-person ("This skill helps...")
- Max 1024 characters
- No angle brackets or special characters

**Content Structure:**
1. **Purpose** (2-3 sentences)
   - What the skill does
   - Primary use cases

2. **When to Use** (specific triggers)
   - Concrete scenarios
   - Decision criteria

3. **How to Use** (reference resources)
   - Link to bundled resources
   - Provide decision frameworks
   - Include working examples

4. **Decision Frameworks** (not option lists)
   - Help Claude choose between alternatives
   - Provide clear criteria

5. **Examples** (concrete, not abstract)
   - Working code examples
   - Real-world scenarios

**Writing Style:**
- Use imperative/infinitive form (NOT second person)
- ✅ "To build a form, use React Hook Form..."
- ✅ "Reference validation-patterns.md for details..."
- ❌ "You should use React Hook Form..."
- ❌ "If you want to build a form..."

### File Structure

```
skills/[skill-name]/
├── SKILL.md              # Main skill file (&lt;500 lines)
├── references/           # Detailed documentation (loaded on-demand)
│   ├── guide-name.md
│   └── patterns.md
├── examples/             # Code examples by language/framework
│   ├── react/
│   ├── vue/
│   └── python/
├── scripts/              # Utility scripts (executed without loading!)
│   └── helper.py
└── assets/               # Templates, schemas, etc.
    └── template.json
```

**File Path Convention:**
- Always use forward slashes: `references/guide.md`
- Never use backslashes: `references\guide.md` (Windows-style)

## Quality Checklist

Before finalizing a skill, verify:

### Core Quality
- [ ] Description includes both WHAT and WHEN
- [ ] SKILL.md body under 500 lines
- [ ] No time-sensitive information
- [ ] Consistent terminology throughout
- [ ] Examples are concrete, not abstract
- [ ] File references are one level deep from SKILL.md

### Naming and Structure
- [ ] Name uses gerund form (verb + -ing)
- [ ] Name: lowercase, hyphens only, max 64 chars
- [ ] Description: max 1024 chars, non-empty
- [ ] File paths use forward slashes (not backslashes)
- [ ] Frontmatter format correct (starts and ends with `---`)

### Code and Scripts
- [ ] Scripts solve problems rather than punt to Claude
- [ ] Error handling is explicit and helpful
- [ ] No "voodoo constants" - all values justified
- [ ] Required packages listed and verified

### Testing
- [ ] At least 3 evaluations created
- [ ] Tested with relevant models (Haiku, Sonnet, Opus)
- [ ] Tested with real usage scenarios
- [ ] Performance and token usage acceptable

## Anti-Patterns to Avoid

### 1. Windows-Style Paths
❌ Bad: `references\guide.md`, `scripts\helper.py`
✅ Good: `references/guide.md`, `scripts/helper.py`

### 2. Deeply Nested References
❌ Bad: SKILL.md → intermediate.md → actual-content.md
✅ Good: SKILL.md → actual-content.md (one level only)

### 3. Offering Too Many Options
❌ Bad: "You could use library A, B, C, D, E, or F..."
✅ Good: "Use library A for most cases. Use B if you need feature X."

### 4. Assuming Package Availability
❌ Bad: "Run the script" (script fails due to missing packages)
✅ Good: "Install: pip install pandas numpy. Then run the script."

### 5. Including Unnecessary Context
❌ Bad: "React is a JavaScript library created by Facebook in 2013..."
✅ Good: "Use React Hook Form for performant form handling."

### 6. Time-Sensitive Information
❌ Bad: "The latest version is 2.5.1 (as of March 2024)"
✅ Good: "Check npm for the latest version"

### 7. Inconsistent Terminology
❌ Bad: Using "form", "input form", "data entry form" interchangeably
✅ Good: Choose "form" and use it consistently

## Testing Across Models

Different Claude models require different levels of guidance:

**Haiku:**
- Needs more detailed guidance
- More explicit examples
- Step-by-step instructions

**Sonnet:**
- Balanced approach
- Moderate detail
- Decision frameworks sufficient

**Opus:**
- Can handle less guidance
- More inference capability
- Higher-level patterns work

**Best Practice:** Test with all three models and adjust detail level accordingly.

## Token Efficiency Patterns

### Scripts are Token-Free

**Most important pattern:**
```
Scripts in scripts/ can be EXECUTED without being LOADED into context.
= Infinite code complexity with ZERO token cost.
```

**Applications:**
- Token generation scripts (free)
- Validation scripts (free)
- Theme building (free)
- Complex algorithms (free)

### Progressive Disclosure

**3-Level Loading:**
```
Level 1: Metadata (name + description) - Always in context (~100 words)
Level 2: SKILL.md body - Loaded when triggered (&lt;5k words ideal)
Level 3: Bundled resources - Loaded/executed as needed (unlimited)
```

**Our structure:**
- init.md = master plan (planning phase)
- SKILL.md = actual skill (implementation phase)
- references/, scripts/, examples/, assets/ = bundled resources

## Component Design Best Practices

### Decision Frameworks Over Lists

❌ **Bad: Option List**
```markdown
For forms, you can use:
- React Hook Form
- Formik
- React Final Form
- Unform
- Final Form
```

✅ **Good: Decision Framework**
```markdown
For forms:
- **Primary: React Hook Form** - Best performance, smallest bundle (8KB)
  - Use for: 95% of projects
  - Pros: Minimal re-renders, excellent TypeScript, great DX

- **Alternative: Formik** - More opinionated, larger ecosystem
  - Use when: Need extensive Yup integration, team familiar with it
  - Pros: Large community, many examples
  - Cons: 3x larger bundle, more re-renders
```

### Accessibility First

Always include accessibility considerations:

**For UI Components:**
- ARIA patterns
- Keyboard navigation
- Screen reader support
- Color contrast
- Focus management

**Example:**
```markdown
## Accessibility Requirements

- ✅ ARIA labels for all interactive elements
- ✅ Keyboard navigation (Tab, Enter, Escape)
- ✅ Screen reader tested with NVDA/JAWS
- ✅ WCAG 2.1 AA color contrast
- ✅ Focus visible on all interactive elements
```

### Performance Considerations

Include performance guidance:

**For Data-Heavy Components:**
- Bundle size benchmarks
- Virtualization thresholds
- Lazy loading strategies
- Memoization patterns

**Example:**
```markdown
## Performance Guidelines

- **Bundle Size:** &lt;10KB gzipped (check with bundlephobia.com)
- **Virtualization:** Enable for >100 items
- **Lazy Loading:** Use React.lazy() for modal content
- **Memoization:** Wrap expensive calculations with useMemo
```

## Documentation Style Guide

### Write in Active Voice

❌ Bad: "The form can be validated using Zod"
✅ Good: "Validate forms using Zod"

### Use Imperative Form

❌ Bad: "You should create a validation schema"
✅ Good: "Create a validation schema"

### Be Specific, Not General

❌ Bad: "Use a form library"
✅ Good: "Use React Hook Form for form management"

### Include Working Examples

❌ Bad: "Configure the library with appropriate options"
✅ Good:
```typescript
import { useForm } from 'react-hook-form'

const { register, handleSubmit } = useForm({
  mode: 'onBlur',  // Validate on blur
  reValidateMode: 'onChange'  // Re-validate on change
})
```

## Validation Requirements

### Frontmatter Validation

Check before submitting:
- [ ] Starts with `---`
- [ ] Ends with `---`
- [ ] `name:` is hyphen-case (lowercase, hyphens only)
- [ ] `description:` is third-person
- [ ] No angle brackets in description
- [ ] Name doesn't start/end with hyphen
- [ ] No consecutive hyphens in name

### Content Validation

- [ ] Under 500 lines (excluding frontmatter)
- [ ] All links work (internal and external)
- [ ] Code blocks have language tags
- [ ] File paths use forward slashes
- [ ] No TODO or FIXME comments
- [ ] All examples are complete and runnable

## Multi-Language Support

When creating backend skills, provide patterns for multiple languages:

**Structure:**
```
examples/
├── typescript/
│   ├── fastify/
│   └── hono/
├── python/
│   ├── fastapi/
│   └── django/
├── rust/
│   └── axum/
└── go/
    └── chi/
```

**Language Coverage:**
- TypeScript (primary for frontend, backend)
- Python (data, ML, backend)
- Rust (performance-critical, systems)
- Go (infrastructure, services)

## Summary

**Key Takeaways:**
1. **Conciseness is critical** - Only specialized knowledge
2. **Progressive disclosure** - 3-level information architecture
3. **Scripts are token-free** - Execute without loading
4. **Evaluation-driven** - Build through testing
5. **Decision frameworks** - Not just option lists
6. **Accessibility first** - Always include WCAG guidance
7. **Multi-language** - Backend skills support 4 languages

**Remember:**
- Keep SKILL.md under 500 lines
- Use gerund form for naming
- Test across Haiku, Sonnet, Opus
- Validate with checklist before submitting

## Next Steps

- [Creating Skills](./creating-skills.md) - Complete implementation guide
- [Research Methodology](./research-methodology.md) - Library validation process
- [Skills Overview](../skills/overview.md) - Explore existing skills

## Resources

- [Anthropic Skills Documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Skills Cookbook](https://github.com/anthropics/claude-cookbooks/tree/main/skills)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)

---

**Following these best practices ensures high-quality, maintainable skills that maximize Claude's effectiveness while minimizing token usage.**
