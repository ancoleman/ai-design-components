---
sidebar_position: 7
title: Implementing Search Filter
description: Search and filter interfaces for frontend and backend with debouncing and optimization
tags: [frontend, backend, search, filtering, performance]
---

# Implementing Search & Filter

Implement search and filter interfaces with comprehensive frontend components and backend query optimization.

## When to Use

Use this skill when:
- Building product search with category and price filters
- Implementing autocomplete/typeahead search
- Creating faceted search interfaces with dynamic counts
- Adding search to data tables or lists
- Building advanced boolean search for power users
- Implementing backend search with SQLAlchemy or Django ORM
- Integrating Elasticsearch for full-text search
- Optimizing search performance with debouncing and caching

## Overview

This skill provides production-ready patterns for implementing search and filtering functionality across the full stack. It covers React/TypeScript components for the frontend and Python patterns for the backend, emphasizing performance optimization, accessibility, and user experience.

## Core Components

### Frontend Search Patterns

**Search Input with Debouncing**
- Implement 300ms debounce for performance
- Show loading states during search
- Clear button (X) for resetting
- Keyboard shortcuts (Cmd/Ctrl+K)

**Autocomplete/Typeahead**
- Suggestion dropdown with keyboard navigation
- Highlight matched text in suggestions
- Recent searches and popular items
- Prevent request flooding with debouncing

**Filter UI Components**
- Checkbox filters for multi-select
- Range sliders for numerical values
- Dropdown filters for single selection
- Filter chips showing active selections

### Backend Query Patterns

**Database Query Building**
- Dynamic query construction with SQLAlchemy
- Django ORM filter chaining
- Index optimization for search columns
- Full-text search in PostgreSQL

**Elasticsearch Integration**
- Document indexing strategies
- Query DSL for complex searches
- Faceted aggregations
- Relevance scoring and boosting

**API Design**
- RESTful search endpoints
- Query parameter validation
- Pagination with cursor/offset
- Response caching strategies

## Implementation Workflows

### Client-Side Search (&lt;1000 items)
1. Load data into memory
2. Implement filter functions in JavaScript
3. Apply debounced search on text input
4. Update results instantly
5. Maintain filter state in React

### Server-Side Search (>1000 items)
1. Design search API endpoint
2. Validate and sanitize query parameters
3. Build database query dynamically
4. Apply pagination
5. Return results with metadata
6. Cache frequent queries

### Hybrid Approach
1. Use client-side filtering for immediate feedback
2. Fetch server results in background
3. Merge and deduplicate results
4. Update UI progressively

## Performance Optimization

### Frontend Optimization

**Debouncing Implementation**
- Use `debounce` from lodash or custom
- Cancel pending requests on new input
- Show skeleton loaders during fetch

**Query Parameter Management**
- Sync filters with URL for shareable searches
- Use React Router or Next.js for URL state

### Backend Optimization

**Query Optimization**
- Create appropriate database indexes
- Use query analyzers to identify bottlenecks
- Implement query result caching

**Validation & Security**
- Sanitize all search inputs
- Prevent SQL injection
- Rate limit search endpoints

## Accessibility Requirements

### ARIA Patterns
- Use `role="search"` for search regions
- Implement `aria-live` for result updates
- Provide clear labels for filters
- Support keyboard-only navigation

### Keyboard Support
- Tab through all interactive elements
- Arrow keys for autocomplete navigation
- Escape to close dropdowns
- Enter to select/submit

## Technology Stack

### Frontend Libraries

**Primary: Downshift (Autocomplete)**
Accessible autocomplete primitives, headless/unstyled:
```bash
npm install downshift
```

**Alternative: React Select**
Full-featured select/filter component with async search

### Backend Technologies

**Python/SQLAlchemy**
- Dynamic query building
- Relationship loading optimization
- Query result pagination

**Python/Django**
- Django Filter backend
- Django REST Framework filters
- Full-text search with PostgreSQL

**Elasticsearch (Python)**
- elasticsearch-py client
- elasticsearch-dsl for query building

## Related Skills

- [Building Tables](./building-tables.md) - Table filtering and search
- [Creating Dashboards](./creating-dashboards.md) - Dashboard filter coordination
- [Building Forms](./building-forms.md) - Filter input components
- [Providing Feedback](./providing-feedback.md) - Search loading states

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/implementing-search-filter)
- Frontend: `references/search-input-patterns.md`, `references/autocomplete-patterns.md`
- Backend: `references/database-querying.md`, `references/elasticsearch-integration.md`
- Performance: `references/performance-optimization.md`
- Examples: `examples/product-search.tsx`, `examples/sqlalchemy_search.py`
