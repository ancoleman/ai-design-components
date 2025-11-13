# Complete Guide: Adding AI Design Components Marketplace to Claude Code

## Overview

This guide walks you through adding the **ai-design-components** marketplace to Claude Code, enabling access to comprehensive UI/UX component design skills for AI-assisted development. The marketplace provides 14 specialized skills organized into 6 plugin categories, covering everything from foundational design systems to advanced data visualization and interactive components.

---

## What You're Installing

The **ai-design-components** marketplace contains:

### 🎨 **Foundation Skills** (1/1 complete)
- **design-tokens**: Design system tokens and theming for consistent styling

### 📊 **Data Skills** (2/3 complete)
- **data-viz**: Data visualization methods and components
- **tables**: Table components and data display patterns
- **dashboards**: Dashboard layout and analytics components

### 📝 **Input Skills** (1/2 complete)
- **forms**: Form systems and validation patterns
- **search-filter**: Search and filtering functionality

### ⚡ **Interaction Skills** (0/3 complete - WIP)
- **ai-chat**: AI chat interface patterns
- **drag-drop**: Drag and drop functionality
- **feedback**: User feedback systems

### 🏗️ **Structure Skills** (0/3 complete - WIP)
- **navigation**: Navigation patterns and components
- **layout**: Layout systems and responsive design
- **timeline**: Timeline and chronological displays

### 🎬 **Content Skills** (0/2 complete - WIP)
- **media**: Media management components
- **onboarding**: User onboarding flows

---

## Prerequisites

Before you begin, ensure you have:

1. **Claude Code installed** - Version 2.0.13 or later (includes plugin support)
2. **Git access** - If using a private repository, ensure authentication is set up
3. **Repository location** - Know where your ai-design-components repo is hosted

---

## Installation Methods

### Method 1: GitHub Repository (Recommended)

If your marketplace is hosted on GitHub, this is the simplest method.

#### Step 1: Add the Marketplace

Open Claude Code and run:

```bash
/plugin marketplace add ancoleman/ai-design-components
```

Replace `ancoleman/ai-design-components` with your actual GitHub username and repository name.

#### Step 2: Verify Installation

Check that the marketplace was added successfully:

```bash
/plugin marketplace list
```

You should see `ai-design-components` in the list of available marketplaces.

#### Step 3: Browse Available Skills

Open the plugin menu to see all available skills:

```bash
/plugin
```

This will show you all 6 plugin categories and their 14 individual skills.

---

### Method 2: Direct Git Repository URL

If you're using GitLab, Bitbucket, or another git hosting service:

```bash
/plugin marketplace add https://github.com/ancoleman/ai-design-components.git
```

Replace with your actual git repository URL.

---

### Method 3: Local Development/Testing

For local testing or development of the marketplace:

```bash
/plugin marketplace add ./path/to/ai-design-components
```

Or if you're in a different directory:

```bash
/plugin marketplace add ~/projects/ai-design-components
```

---

### Method 4: Direct marketplace.json URL

If you're hosting the marketplace.json file directly on a web server:

```bash
/plugin marketplace add https://your-domain.com/path/to/marketplace.json
```

---

## Installing Individual Plugins

Once the marketplace is added, you can install specific plugin categories:

### Install Foundation Skills
```bash
/plugin install ui-foundation-skills@ai-design-components
```

### Install Data Visualization Skills
```bash
/plugin install ui-data-skills@ai-design-components
```

### Install Form & Input Skills
```bash
/plugin install ui-input-skills@ai-design-components
```

### Install Interaction Skills
```bash
/plugin install ui-interaction-skills@ai-design-components
```

### Install Structure & Layout Skills
```bash
/plugin install ui-structure-skills@ai-design-components
```

### Install Content & Media Skills
```bash
/plugin install ui-content-skills@ai-design-components
```

---

## Using Individual Skills

After installing a plugin category, you can access specific skills:

### Example: Using Data Visualization Skills

```bash
# If you need help choosing the right chart type
/data-viz help

# Apply data visualization guidance to your project
@data-viz analyze this dataset and suggest visualizations
```

### Example: Using Design Tokens

```bash
# Apply consistent design tokens
/design-tokens setup

# Get color palette recommendations
@design-tokens suggest colors for a healthcare dashboard
```

---

## Automatic Team Installation

For teams working on shared projects, configure automatic marketplace installation in your repository's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "ai-design-components": {
      "source": {
        "source": "github",
        "repo": "ancoleman/ai-design-components"
      }
    }
  },
  "enabledPlugins": [
    "ui-foundation-skills@ai-design-components",
    "ui-data-skills@ai-design-components",
    "ui-input-skills@ai-design-components"
  ]
}
```

When team members open the project and trust the repository, Claude Code will:
1. Automatically add the ai-design-components marketplace
2. Install the specified plugins
3. Make all skills immediately available

---

## Marketplace Structure Explained

Your `marketplace.json` defines the plugin organization:

```json
{
  "name": "ai-design-components",
  "owner": "Anton Coleman <acoleman@paloaltonetworks.com>",
  "version": "0.1.0",
  "description": "Comprehensive UI/UX component design skills for AI-assisted development",
  "plugins": [...]
}
```

Each plugin entry contains:
- **name**: Plugin identifier (e.g., `ui-foundation-skills`)
- **description**: What the plugin provides
- **source**: Where the skill files are located (e.g., `./`)
- **skills**: Array of individual skill names
- **strict**: Whether plugin.json is required (false means marketplace.json serves as manifest)

---

## Skill Activation & Usage

### How Skills Work

Skills are specialized knowledge sets that Claude can use when working on design tasks. When you install a plugin category, all its skills become available to Claude.

### Triggering Skills

Skills activate based on:
1. **Direct invocation**: Using `/skill-name` or `@skill-name` syntax
2. **Context detection**: Claude recognizes when a skill is relevant to your query
3. **Explicit requests**: Asking Claude to "use the data-viz skill" or "apply design tokens"

### Best Practices

**For Data Visualization:**
```
"I need to display monthly revenue trends for the past year - 
what visualization method should I use?"
```

**For Design Tokens:**
```
"Set up a design system with consistent colors, typography, 
and spacing for a SaaS dashboard"
```

**For Forms:**
```
"Create a multi-step user registration form with validation"
```

---

## Advanced Configuration

### Custom Skill Locations

If your skills are in non-standard locations, you can specify paths in the marketplace.json:

```json
{
  "name": "ui-foundation-skills",
  "source": "./skills/foundation",
  "skills": ["design-tokens"],
  "commands": ["./commands/"],
  "agents": ["./agents/design-reviewer.md"]
}
```

### Version Pinning

Specify exact versions for production stability:

```json
{
  "name": "ui-data-skills",
  "version": "1.0.0",
  "source": "./",
  "skills": ["data-viz", "tables", "dashboards"]
}
```

---

## Managing Your Marketplace

### Update Marketplace Data
```bash
/plugin marketplace update ai-design-components
```
Refreshes plugin listings and metadata from the source.

### List All Marketplaces
```bash
/plugin marketplace list
```
Shows all configured marketplaces and their status.

### Remove Marketplace
```bash
/plugin marketplace remove ai-design-components
```
⚠️ This will uninstall all plugins from this marketplace.

---

## Managing Installed Plugins

### List Installed Plugins
```bash
/plugin list
```

### Enable/Disable Plugins
```bash
/plugin disable ui-interaction-skills
/plugin enable ui-interaction-skills
```

### Uninstall a Plugin
```bash
/plugin uninstall ui-foundation-skills
```

### Update All Plugins
```bash
/plugin update
```

---

## Troubleshooting

### Issue: Marketplace Not Loading

**Symptoms:** Can't add marketplace or see plugins

**Solutions:**
1. Verify the repository URL is correct and accessible
2. Ensure `.claude-plugin/marketplace.json` exists in the repo root
3. Validate JSON syntax: `claude plugin validate`
4. For private repos, check GitHub authentication:
   ```bash
   gh auth status
   ```

### Issue: Skills Not Activating

**Symptoms:** Skills installed but Claude doesn't use them

**Solutions:**
1. Verify plugin is enabled: `/plugin list`
2. Re-enable the plugin: `/plugin disable ui-data-skills` then `/plugin enable ui-data-skills`
3. Explicitly mention the skill in your request: "Use the data-viz skill to..."
4. Check skill files exist in the expected location

### Issue: Plugin Installation Fails

**Symptoms:** Marketplace loads but plugin won't install

**Solutions:**
1. Check that skill directories exist at the paths specified in `marketplace.json`
2. Verify each skill has a `SKILL.md` file (if strict mode is enabled)
3. For GitHub sources, ensure the repository is public or you have access
4. Test by cloning the repo manually to verify file structure

### Issue: Permission Denied

**Symptoms:** Cannot access private repository

**Solutions:**
1. Set up SSH keys for the git hosting service
2. Use HTTPS with personal access tokens
3. For GitHub: Generate a token at https://github.com/settings/tokens
4. Authenticate: `gh auth login`

---

## Validation & Testing

### Before Sharing Your Marketplace

1. **Validate JSON Syntax:**
   ```bash
   claude plugin validate ./marketplace.json
   ```

2. **Test Local Installation:**
   ```bash
   /plugin marketplace add ./ai-design-components
   /plugin install ui-foundation-skills@ai-design-components
   ```

3. **Verify Skill Loading:**
   Create a test query that should trigger each skill and confirm it works.

4. **Check Documentation:**
   Ensure each SKILL.md file is comprehensive and has clear usage examples.

---

## Repository Structure Requirements

For your marketplace to work correctly, ensure this structure:

```
ai-design-components/
├── .claude-plugin/
│   └── marketplace.json          # Required: Marketplace definition
├── design-tokens/
│   └── SKILL.md                  # Your design tokens skill
├── data-viz/
│   └── SKILL.md                  # Your data visualization skill
├── tables/
│   └── SKILL.md                  # Your tables skill
├── dashboards/
│   └── SKILL.md                  # Your dashboards skill
├── forms/
│   └── SKILL.md                  # Your forms skill
├── search-filter/
│   └── SKILL.md                  # Your search/filter skill
├── ai-chat/
│   └── SKILL.md                  # Your AI chat skill (WIP)
├── drag-drop/
│   └── SKILL.md                  # Your drag-drop skill (WIP)
├── feedback/
│   └── SKILL.md                  # Your feedback skill (WIP)
├── navigation/
│   └── SKILL.md                  # Your navigation skill (WIP)
├── layout/
│   └── SKILL.md                  # Your layout skill (WIP)
├── timeline/
│   └── SKILL.md                  # Your timeline skill (WIP)
├── media/
│   └── SKILL.md                  # Your media skill (WIP)
├── onboarding/
│   └── SKILL.md                  # Your onboarding skill (WIP)
└── README.md                     # Documentation
```

Since your `marketplace.json` uses `"source": "./"`, Claude Code will look for skill directories in the repository root.

---

## Example Workflow: Complete Setup

Here's a complete example from start to finish:

```bash
# 1. Add the marketplace
/plugin marketplace add ancoleman/ai-design-components

# 2. Verify it was added
/plugin marketplace list

# 3. Browse available plugins
/plugin

# 4. Install the data visualization plugin
/plugin install ui-data-skills@ai-design-components

# 5. Install the foundation plugin for design tokens
/plugin install ui-foundation-skills@ai-design-components

# 6. Verify installation
/plugin list

# 7. Start using skills in your work
# Just ask Claude naturally:
```

Then in your conversation with Claude:

```
"I'm building a financial dashboard and need to display:
1. Monthly revenue trends over 2 years
2. Regional sales breakdown
3. Top 10 products by revenue
4. Customer acquisition funnel

Can you help me choose the right visualization methods for each?"
```

Claude will automatically use the `data-viz` skill to provide expert guidance.

---

## Next Steps After Installation

### 1. **Explore Each Skill**

Try out different skills to understand what they provide:
- Ask for design token recommendations
- Request data visualization suggestions  
- Get form validation patterns

### 2. **Customize for Your Workflow**

- Add your team's specific design patterns to the skills
- Create custom commands that combine multiple skills
- Build agents that specialize in your design system

### 3. **Share with Your Team**

- Add the `.claude/settings.json` configuration to your repository
- Document team-specific conventions for using the skills
- Create example projects that showcase the skills in action

### 4. **Contribute Back**

- Complete the WIP skills (interaction, structure, content categories)
- Add more visualization methods to data-viz
- Share improvements via pull requests

---

## Ultrathink Mode Usage

For complex design decisions, you can invoke ultrathink mode with your design components:

```bash
/ultrathink "Design a complete data analytics dashboard for healthcare 
that displays patient outcomes, resource utilization, and operational 
metrics. Use the data-viz and dashboard skills to ensure best practices."
```

This activates a multi-agent system that will:
1. **Architect**: Plan the dashboard structure using layout and navigation skills
2. **Researcher**: Analyze healthcare dashboard patterns using data-viz skill
3. **Coder**: Implement components using design-tokens for consistency
4. **Tester**: Validate accessibility and usability

---

## Support & Resources

### Getting Help

- **Marketplace Issues**: Check the troubleshooting section above
- **Skill Documentation**: Each SKILL.md file contains detailed usage information
- **Claude Code Docs**: https://docs.claude.com/en/docs/claude-code/plugin-marketplaces
- **Community**: Join Claude Code Discord (#claude-code channel)

### Useful Commands Reference

```bash
# Marketplace Management
/plugin marketplace add <source>
/plugin marketplace list
/plugin marketplace update <name>
/plugin marketplace remove <name>

# Plugin Management
/plugin install <name>@<marketplace>
/plugin list
/plugin enable <name>
/plugin disable <name>
/plugin uninstall <name>
/plugin update

# Interactive Browsing
/plugin                           # Browse all available plugins
```

---

## Technical Notes

### Token Efficiency

Skills are designed for token efficiency:
- Core concepts are front-loaded
- Progressive disclosure for complex topics
- Reference patterns rather than full examples
- Cross-references between related skills

### Skill Interaction

Skills can work together:
- `design-tokens` provides values for all other component skills
- `data-viz` guides chart selection for `dashboards`
- `forms` and `search-filter` share validation patterns
- `navigation` and `layout` coordinate page structure

### Version Strategy

The marketplace follows semantic versioning:
- **0.1.0**: Initial beta with foundation and data skills
- **0.2.0**: Complete input and interaction skills (planned)
- **0.3.0**: Complete structure and content skills (planned)
- **1.0.0**: Full production release with all 14 skills

---

## Frequently Asked Questions

**Q: Can I use some skills without installing all plugins?**  
A: Yes! Install only the plugin categories you need. Each plugin is independent.

**Q: How do I update skills when you release new versions?**  
A: Run `/plugin marketplace update ai-design-components` then `/plugin update`

**Q: Can I modify the skills for my team's needs?**  
A: Yes! Fork the repository, customize the skills, and host your own marketplace.

**Q: Do skills work offline?**  
A: Once installed, skills are available offline. Only marketplace updates require internet.

**Q: Can I create my own skills in this marketplace?**  
A: Yes! Add new skill directories and update marketplace.json to include them.

**Q: How do I know which skill to use?**  
A: Just describe your task naturally - Claude will activate relevant skills automatically.

---

## Conclusion

The ai-design-components marketplace provides a comprehensive foundation for AI-assisted UI/UX development. By organizing design knowledge into focused, reusable skills, it enables Claude to provide expert guidance across the entire component design process - from foundational tokens to advanced data visualizations.

Start with the foundation and data skills (the most complete), then gradually adopt other categories as your needs grow and the WIP skills are completed.

**Ready to get started?** Run:

```bash
/plugin marketplace add ancoleman/ai-design-components
/plugin install ui-foundation-skills@ai-design-components
/plugin install ui-data-skills@ai-design-components
```

Then ask Claude: *"Help me design a dashboard component - what should I consider?"*

---

## Appendix: Complete marketplace.json Reference

Your current marketplace.json configuration:

```json
{
  "name": "ai-design-components",
  "owner": "Anton Coleman <acoleman@paloaltonetworks.com>",
  "version": "0.1.0",
  "description": "Comprehensive UI/UX component design skills for AI-assisted development",
  "plugins": [
    {
      "name": "ui-foundation-skills",
      "description": "Foundational design system including tokens and theming for consistent styling across all components",
      "source": "./",
      "skills": ["design-tokens"],
      "strict": false
    },
    {
      "name": "ui-data-skills",
      "description": "Data visualization, tables, and dashboard components for displaying and analyzing data (2/3 complete)",
      "source": "./",
      "skills": ["data-viz", "tables", "dashboards"],
      "strict": false
    },
    {
      "name": "ui-input-skills",
      "description": "Data visualization, tables, and dashboard components for displaying and analyzing data (2/3 complete)",
      "source": "./",
      "skills": ["forms", "search-filter"],
      "strict": false
    },
    {
      "name": "ui-interaction-skills",
      "description": "Interactive components including AI chat interfaces, drag-drop functionality, and feedback systems (0/3 complete - WIP)",
      "source": "./",
      "skills": ["ai-chat", "drag-drop", "feedback"],
      "strict": false
    },
    {
      "name": "ui-structure-skills",
      "description": "Navigation, layout, and timeline components for app structure and organization (0/3 complete - WIP)",
      "source": "./",
      "skills": ["navigation", "layout", "timeline"],
      "strict": false
    },
    {
      "name": "ui-content-skills",
      "description": "Media management and user onboarding components for content-rich experiences (0/2 complete - WIP)",
      "source": "./",
      "skills": ["media", "onboarding"],
      "strict": false
    }
  ]
}
```

---

**Document Version**: 1.0  
**Last Updated**: November 2025  
**Maintained By**: Anton Coleman  
**License**: Same as ai-design-components repository