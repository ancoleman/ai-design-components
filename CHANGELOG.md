# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-12-01

### Added
- Complete SKILL.md implementations for all 14 component skills
- New skills completed:
  - `managing-media` - Media & file management components
  - `guiding-users` - Onboarding & help systems
  - `displaying-timelines` - Timeline & activity components
  - `building-ai-chat` - AI chat interfaces (strategic priority)
  - `creating-dashboards` - Dashboard & analytics components
  - `building-tables` - Tables & data grids
  - `implementing-search-filter` - Search & filter interfaces
  - `implementing-drag-drop` - Drag-and-drop functionality
  - `providing-feedback` - Feedback & notification systems
  - `implementing-navigation` - Navigation patterns
  - `designing-layouts` - Layout systems & responsive design
- Reference files for theming-components:
  - `color-system.md` - Complete color token reference
  - `typography-system.md` - Typography token reference
  - `spacing-system.md` - Spacing token reference
- Comprehensive chart catalog for visualizing-data (24+ chart types)

### Changed
- Renamed all skill directories to use gerund naming convention (Anthropic best practice):
  - `data-viz` → `visualizing-data`
  - `forms` → `building-forms`
  - `design-tokens` → `theming-components`
  - `ai-chat` → `building-ai-chat`
  - `dashboards` → `creating-dashboards`
  - `tables` → `building-tables`
  - `search-filter` → `implementing-search-filter`
  - `drag-drop` → `implementing-drag-drop`
  - `feedback` → `providing-feedback`
  - `navigation` → `implementing-navigation`
  - `layout` → `designing-layouts`
  - `timeline` → `displaying-timelines`
  - `media` → `managing-media`
  - `onboarding` → `guiding-users`
- Reduced `theming-components/SKILL.md` from 878 to 384 lines (progressive disclosure)
- Reduced `visualizing-data/SKILL.md` from 639 to 329 lines (progressive disclosure)
- Updated marketplace.json with all 14 correct skill paths
- Moved all init.md files to `docs/init_files/` for reference

### Fixed
- Skill naming convention violations (now all use gerund form)
- SKILL.md line count violations (all now under 500 lines)
- Directory names now match SKILL.md frontmatter names

## [0.1.0] - 2025-01-13

### Added
- Initial project structure with 14 component skill categories
- Completed `data-viz` skill with 24+ visualization types and decision frameworks
- Completed `forms` skill with 50+ input types and validation patterns
- Comprehensive master plans (init.md) for all 14 skill categories
- Research methodology guide for library recommendations
- Skills organized into 6 plugin groups in marketplace.json:
  - ui-foundation-skills (design-tokens)
  - ui-data-skills (data-viz, tables, dashboards)
  - ui-input-skills (forms, search-filter)
  - ui-interaction-skills (ai-chat, drag-drop, feedback)
  - ui-structure-skills (navigation, layout, timeline)
  - ui-content-skills (media, onboarding)
- Project documentation (README.md, CLAUDE.md, skill_best_practice.md)
- MIT License
- Comprehensive .gitignore for development

### In Progress
- 12 additional component skills awaiting SKILL.md implementation
- Design tokens foundational system
- AI chat interfaces (strategic priority)

[0.2.0]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.2.0
[0.1.0]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.1.0
