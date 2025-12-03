# Contributing to AI Design Components

Thank you for your interest in contributing to AI Design Components! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Ways to Contribute](#ways-to-contribute)
- [Development Workflow](#development-workflow)
- [Skill Development Guidelines](#skill-development-guidelines)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [acoleman@paloaltonetworks.com](mailto:acoleman@paloaltonetworks.com).

## Getting Started

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

## Ways to Contribute

### 🐛 Report Bugs

Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.yml) to report issues. Include:
- Clear steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Claude Code version, etc.)

### 💡 Suggest Features

Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.yml) to propose new features or enhancements.

### 🎨 Contribute Skills

Use the [Skill Contribution template](.github/ISSUE_TEMPLATE/skill_contribution.yml) to propose a new skill or major enhancement. See [Skill Development Guidelines](#skill-development-guidelines) below.

### 📚 Improve Documentation

Use the [Documentation template](.github/ISSUE_TEMPLATE/documentation.yml) to suggest documentation improvements. Good documentation is critical!

### ❓ Ask Questions

Use the [Question template](.github/ISSUE_TEMPLATE/question.yml) for general questions and discussions.

## Development Workflow

### Branch Naming

Use descriptive branch names:
- `feature/skill-name` - New skills
- `feature/description` - New features
- `fix/issue-description` - Bug fixes
- `docs/what-changed` - Documentation updates
- `refactor/what-changed` - Code refactoring

### Commit Messages

Follow conventional commits format:

```
type(scope): brief description

Detailed explanation if needed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
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

## Skill Development Guidelines

When contributing a new skill or enhancing an existing one, follow these guidelines from [skill_best_practice.md](skill_best_practice.md):

### 1. Naming Convention

- Use **gerund form** (verb + -ing): `building-forms`, `visualizing-data`
- Lowercase with hyphens only
- Max 64 characters
- ❌ Bad: `form-builder`, `data-viz-helper`, `tools`
- ✅ Good: `building-forms`, `visualizing-data`, `managing-state`

### 2. File Structure

```
skills/[skill-name]/
├── SKILL.md              # Main skill file (<500 lines)
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

### 3. SKILL.md Requirements

**Frontmatter:**
```yaml
---
name: skill-name              # lowercase, hyphens, gerund form
description: What this skill does AND when to use it (max 1024 chars)
---
```

**Content:**
- Under 500 lines (use progressive disclosure)
- Include WHAT and WHEN in description
- Provide decision frameworks (not just option lists)
- Include concrete examples
- Only specialized knowledge (assume Claude knows basics)
- Use imperative/infinitive form (not second person)
  - ✅ "To build a form, use React Hook Form..."
  - ❌ "You should use React Hook Form..."

### 4. Progressive Disclosure

- Main SKILL.md references additional files
- Keep references **one level deep** (SKILL.md → file.md, not → another.md)
- Use descriptive filenames: `chart-types.md` not `doc2.md`
- Scripts execute **without loading** (zero token cost!)

### 5. Research Requirements

Before submitting a skill:
- Research library recommendations (use Context7 if available)
- Document trust scores and weekly downloads
- Provide working code examples
- Include library comparison matrix

### 6. Quality Checklist

Before submitting:
- [ ] Name uses gerund form
- [ ] Description includes WHAT and WHEN (max 1024 chars)
- [ ] SKILL.md under 500 lines
- [ ] File references one level deep
- [ ] Use forward slashes (not backslashes)
- [ ] Concrete examples (not abstract)
- [ ] Decision frameworks included
- [ ] No time-sensitive information
- [ ] Tested with real usage scenarios

### 7. Skillchain Integration

If your skill should be accessible via `/skillchain`:

1. Add to `commands/skillchain/_registry.yaml`:
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

2. Update the appropriate category orchestrator in `commands/skillchain/categories/`

## Pull Request Process

1. **Update your fork** with latest upstream changes:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes** following the guidelines above

4. **Test your changes**:
   ```bash
   # Install locally and test
   ./commands/install-skillchain.sh

   # Test the skill with Claude Code
   claude
   /skillchain [test your skill]
   ```

5. **Commit with descriptive messages**:
   ```bash
   git add .
   git commit -m "feat(skill): Add your-skill-name"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request** on GitHub:
   - Fill out the PR template completely
   - Reference any related issues
   - Explain what changed and why
   - Include before/after examples if applicable

8. **Address review feedback** promptly

9. **Ensure CI passes** (if applicable)

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

## Questions?

- Use the [Question template](.github/ISSUE_TEMPLATE/question.yml)
- Join [GitHub Discussions](https://github.com/ancoleman/ai-design-components/discussions)
- Review [CLAUDE.md](CLAUDE.md) for project structure
- Read [skill_best_practice.md](skill_best_practice.md) for detailed skill guidelines

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).

---

Thank you for contributing to AI Design Components! 🎉
