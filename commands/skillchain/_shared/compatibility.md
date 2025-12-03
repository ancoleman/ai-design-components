# Skill Compatibility Matrix

## Version Compatibility Rules

### Semantic Versioning
- MAJOR: Breaking changes (incompatible with previous)
- MINOR: New features (backwards compatible)
- PATCH: Bug fixes (backwards compatible)

### Skill Dependencies

| Skill | Depends On | Min Version |
|-------|------------|-------------|
| visualizing-data | theming-components | 1.0.0 |
| building-tables | theming-components | 1.0.0 |
| creating-dashboards | theming-components, designing-layouts | 1.0.0 |
| building-forms | theming-components | 1.0.0 |
| building-ai-chat | theming-components, building-forms | 1.0.0 |
| implementing-search-filter | theming-components | 1.0.0 |
| implementing-drag-drop | theming-components | 1.0.0 |
| providing-feedback | theming-components | 1.0.0 |
| implementing-navigation | theming-components | 1.0.0 |
| designing-layouts | theming-components | 1.0.0 |
| displaying-timelines | theming-components | 1.0.0 |
| managing-media | theming-components | 1.0.0 |
| guiding-users | theming-components | 1.0.0 |
| assembling-components | * (all previous) | 1.0.0 |
| databases-vector | ingesting-data | 1.0.0 |
| ai-data-engineering | databases-vector | 1.0.0 |
| model-serving | ai-data-engineering | 1.0.0 |
| message-queues | api-patterns | 1.0.0 |
| realtime-sync | api-patterns | 1.0.0 |
| auth-security | api-patterns | 1.0.0 |

### Blueprint Compatibility

| Blueprint | Min Registry Version | Required Skills |
|-----------|---------------------|-----------------|
| dashboard | 2.0.0 | theming-components@1.0.0, visualizing-data@1.0.0 |
| crud-api | 2.0.0 | api-patterns@1.0.0, databases-relational@1.0.0 |
| rag-pipeline | 2.0.0 | databases-vector@1.0.0, ai-data-engineering@1.0.0 |

## Upgrade Path

When upgrading skills:
1. Check compatibility matrix
2. Upgrade dependencies first
3. Test with existing configurations
4. Update user preferences if schema changed
