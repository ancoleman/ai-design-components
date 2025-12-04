---
sidebar_position: 1
title: Creating Skills
description: Guide to contributing new skills
---

# Creating Skills

Learn how to create effective Claude Skills following Anthropic's best practices.

## Overview

This guide covers the complete process of creating Claude Skills from initial concept to implementation. Whether you're contributing to AI Design Components or building your own skills, following these guidelines will help you create high-quality, maintainable skills.

## Getting Started

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/ai-design-components.git
   cd ai-design-components
   ```
3. **Set up the upstream remote**:
   ```bash
   git remote add upstream https://github.com/ancoleman/ai-design-components.git
   ```
4. **Install the skillchain** to test your changes:
   ```bash
   ./commands/install-skillchain.sh
   ```

## Key Principles

When creating skills, follow these core principles:

### 1. Conciseness is Critical
- **Context window is a public good** - minimize token usage
- **Only include what Claude doesn't already know**
- Remove general knowledge; focus on specialized, domain-specific information
- Keep SKILL.md under 500 lines; use progressive disclosure for additional content

### 2. Appropriate Degrees of Freedom
- **High freedom (text instructions)**: Multiple valid approaches, context-dependent
- **Medium freedom (templates/config)**: Preferred patterns with acceptable variation
- **Low freedom (executable scripts)**: Fragile operations requiring consistency

### 3. Progressive Disclosure Design
- Main SKILL.md references additional files (one level deep only)
- Avoid deeply nested references (SKILL.md → file.md → another.md is BAD)
- All reference files should link directly from SKILL.md
- Use descriptive filenames: `chart-types.md`, not `doc2.md`

### 4. Evaluation-Driven Development
1. **Identify gaps** - Run tasks without Skill first, document failures
2. **Create evaluations** - Build 3+ test scenarios
3. **Establish baseline** - Measure performance without Skill
4. **Write minimal instructions** - Just enough to pass evaluations
5. **Iterate** - Execute evaluations and refine

## Naming Convention

Use **gerund form** (verb + -ing):
- ✅ Good: `building-forms`, `visualizing-data`, `processing-pdfs`
- ❌ Bad: `form-builder`, `data-viz-helper`, `tools`

**Requirements:**
- Lowercase with hyphens only
- Max 64 characters
- Descriptive and action-oriented

## File Structure

### Standard Skill Layout

```
skills/[skill-name]/
├── SKILL.md              # Main skill file (&lt;500 lines)
├── references/           # Detailed documentation
│   ├── guide-name.md
│   └── patterns.md
├── examples/             # Code examples by language/framework
│   ├── react/
│   ├── vue/
│   └── python/
├── scripts/              # Utility scripts (executed without loading)
│   └── helper.py
└── assets/               # Templates, schemas, etc.
    └── template.json
```

### SKILL.md Requirements

**Frontmatter:**
```yaml
---
name: skill-name              # lowercase, hyphens, gerund form
description: What this skill does AND when to use it (max 1024 chars)
---
```

**Content Structure:**
1. **Purpose** - 2-3 sentences about what the skill does
2. **When to Use** - Specific triggers and use cases
3. **How to Use** - Reference bundled resources, provide guidance
4. **Decision Frameworks** - Help Claude choose between options
5. **Examples** - Concrete, working examples

**Writing Style:**
- Use imperative/infinitive form (NOT second person)
- ✅ "To build a form, use React Hook Form..."
- ✅ "Reference validation-patterns.md for details..."
- ❌ "You should use React Hook Form..."
- ❌ "If you want to build a form..."

## Development Workflow

### Branch Naming

Use descriptive branch names:
- `feature/skill-name` - New skills
- `feature/description` - New features
- `fix/issue-description` - Bug fixes
- `docs/what-changed` - Documentation updates
- `refactor/what-changed` - Code refactoring

### Implementation Steps

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-skill-name
   ```

2. **Start with concrete examples**:
   - "Build a login form with validation"
   - "Create a bar chart showing sales trends"
   - What would trigger this skill?

3. **Plan reusable resources**:
   - **scripts/**: Repeatedly rewritten code
   - **references/**: Documentation to reference
   - **assets/**: Templates and files used in output

4. **Create SKILL.md**:
   - Write frontmatter with name and description
   - Document purpose and when to use
   - Reference bundled resources
   - Include decision frameworks

5. **Add bundled resources**:
   - scripts/ - Execute without loading (token-free!)
   - references/ - Load only when needed
   - examples/ - Code examples (can be references/ or assets/)

6. **Test your changes**:
   ```bash
   # Install locally and test
   ./commands/install-skillchain.sh

   # Test the skill with Claude Code
   claude
   /skillchain [test your skill]
   ```

7. **Commit with descriptive messages**:
   ```bash
   git add .
   git commit -m "feat(skill): Add your-skill-name"
   ```

## Quality Checklist

Before submitting, ensure:

**Core Quality:**
- [ ] Description includes both WHAT and WHEN
- [ ] SKILL.md body under 500 lines
- [ ] No time-sensitive information
- [ ] Consistent terminology throughout
- [ ] Examples are concrete, not abstract
- [ ] File references are one level deep from SKILL.md

**Naming and Structure:**
- [ ] Name uses gerund form (verb + -ing)
- [ ] Name: lowercase, hyphens only, max 64 chars
- [ ] Description: max 1024 chars, non-empty
- [ ] File paths use forward slashes (not backslashes)

**Code and Scripts (if applicable):**
- [ ] Scripts solve problems rather than punt to Claude
- [ ] Error handling is explicit and helpful
- [ ] No "voodoo constants" - all values justified
- [ ] Required packages listed and verified

**Testing:**
- [ ] At least 3 evaluations created
- [ ] Tested with relevant models
- [ ] Tested with real usage scenarios
- [ ] Performance and token usage acceptable

## Skillchain Integration

If your skill should be accessible via `/skillchain`:

1. **Add to registry** (`commands/skillchain/_registry.yaml`):
   ```yaml
   skill-name:
     category: frontend  # or backend
     group: interaction  # group name
     priority: 3         # execution order
     parallel_group: interaction  # for parallel loading
     keywords:
       - keyword1
       - keyword2
     invocation: "Skill(skill-name)"
     dependencies:
       - theming-components
     questions:
       - What framework are you using?
       - Do you need dark mode support?
     estimate_tokens: 450
     version: "1.0.0"
   ```

2. **Update category orchestrator** in `commands/skillchain/categories/`

## Research Requirements

Before submitting a skill:
- Research library recommendations (use Context7 if available)
- Document trust scores and weekly downloads
- Provide working code examples
- Include library comparison matrix

See [Research Methodology](./research-methodology.md) for details.

## Commit Messages

Follow conventional commits format:

```
type(scope): brief description

Detailed explanation if needed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com>
```

**Types:**
- `feat`: New feature or skill
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(skill): Add animating-components skill

docs(readme): Update installation instructions for v0.3.3

fix(skillchain): Correct path discovery for global installation
```

## Pull Request Process

1. **Update your fork** with latest upstream changes:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Open a Pull Request** on GitHub:
   - Fill out the PR template completely
   - Reference any related issues
   - Explain what changed and why
   - Include before/after examples if applicable

4. **Address review feedback** promptly

5. **Ensure CI passes** (if applicable)

## Anti-Patterns to Avoid

1. **Windows-style paths** - Always use forward slashes: `scripts/helper.py`
2. **Deeply nested references** - Keep one level: SKILL.md → reference.md (not → another.md)
3. **Offering too many options** - Provide clear primary approach
4. **Assuming package availability** - Always list dependencies
5. **Including unnecessary context** - If Claude knows it, omit it
6. **Time-sensitive information** - Avoid content that becomes outdated
7. **Inconsistent terminology** - Choose one term and stick with it

## Testing Across Models

Test your skill with different Claude models:
- **Haiku** - Needs more guidance
- **Sonnet** - Balanced
- **Opus** - Can handle less guidance

Adjust the level of detail based on performance across models.

## Style Guidelines

### Markdown

- Use ATX-style headers (`#` not underlines)
- Add blank lines around headers
- Use fenced code blocks with language tags
- Keep lines under 100 characters when possible

### Code Examples

- Include working, tested examples
- Show both input and output
- Add comments explaining non-obvious parts
- Support multiple languages/frameworks when relevant

### Documentation

- Write in clear, concise language
- Use active voice
- Include examples for abstract concepts
- Link to related documentation
- Keep a beginner-friendly tone

## Two-Claude Method

Use this approach for iterative development:

- **Claude A** (expert) - Designs and refines the Skill
- **Claude B** (agent) - Uses the Skill for real work
- Test with Claude B on real tasks, return to Claude A with observations

## Questions?

- Use the [Question template](https://github.com/ancoleman/ai-design-components/issues/new/choose)
- Join [GitHub Discussions](https://github.com/ancoleman/ai-design-components/discussions)
- Review [Best Practices](./best-practices.md) for detailed guidance
- Read [Research Methodology](./research-methodology.md) for library validation

## Next Steps

- [Best Practices](./best-practices.md) - Anthropic's official guidelines
- [Research Methodology](./research-methodology.md) - How to validate library recommendations
- [Skills Overview](../skills/overview.md) - Explore existing skills
- [Skillchain Documentation](../skillchain/overview.md) - Learn about skillchain integration

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to AI Design Components!
