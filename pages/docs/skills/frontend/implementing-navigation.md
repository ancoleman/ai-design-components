---
sidebar_position: 10
title: Implementing Navigation
description: Navigation patterns and routing for frontend and backend applications
tags: [frontend, backend, navigation, routing, accessibility]
---

# Implementing Navigation Patterns & Routing

Comprehensive guidance for implementing navigation systems across both frontend and backend applications.

## When to Use

Use this skill when:
- Building primary navigation (top, side, mega menus)
- Implementing secondary navigation (breadcrumbs, tabs, pagination)
- Setting up client-side routing (React Router, Next.js)
- Configuring server-side routes (Flask, Django, FastAPI)
- Creating mobile navigation patterns (hamburger, bottom nav)
- Implementing keyboard-accessible navigation
- Building command palettes or search-driven navigation
- Creating multi-step wizards or steppers
- Ensuring WCAG 2.1 AA compliance for navigation

## Navigation Decision Framework

```
Information Architecture → Navigation Pattern

Flat (1-2 levels)      → Top Navigation
Deep (3+ levels)       → Side Navigation
E-commerce/Large       → Mega Menu
Linear Process         → Stepper/Wizard
Long Content          → Table of Contents
Power Users           → Command Palette
Multi-section Page    → Tabs
Large Data Sets       → Pagination
```

## Frontend Navigation Components

### Primary Navigation Patterns

**Top Navigation (Horizontal)**
- Best for shallow hierarchies, marketing sites
- 5-7 primary links maximum for cognitive load

**Side Navigation (Vertical)**
- Best for deep hierarchies, admin panels, dashboards
- Supports multi-level nesting and collapsible sections

**Mega Menu**
- Best for e-commerce, content-heavy sites
- Rich content with images and descriptions

### Secondary Navigation Components

**Breadcrumbs**
- Shows hierarchical path and current location
- Essential for deep sites and e-commerce

**Tabs**
- Content switching without page reload
- URL synchronization for bookmarking

**Pagination**
- For search results, product lists, articles
- Consider virtualization for performance

### Client-Side Routing

**React Router (Industry Standard)**
- Type-safe routing with loader patterns
- Nested routes and lazy loading support

**Next.js App Router**
- File-based routing with RSC support
- Parallel and intercepting routes

## Backend Routing Patterns

### Python Web Frameworks

**Flask**
- Blueprint-based organization
- Route decorators and URL rules

**Django**
- URL configuration with namespaces
- Path converters and regex patterns

**FastAPI**
- Router-based organization
- Path operations and dependencies

## Mobile Navigation

### Patterns for Touch Devices

**Hamburger Menu**
- Slide-out drawer for primary navigation

**Bottom Navigation**
- 3-5 primary actions, thumb-friendly

**Tab Bar**
- Horizontal scrollable tabs with swipe
- Natural for mobile-first applications

## Accessibility Requirements

### Keyboard Navigation

```
Tab       → Move forward through links
Shift+Tab → Move backward through links
Enter     → Activate link/button
Space     → Activate button
Arrow keys → Navigate within menus
Escape    → Close dropdowns/modals
```

### ARIA Patterns

Essential ARIA attributes for accessible navigation:
- Landmark roles (navigation, main, search)
- States (aria-current, aria-expanded)
- Properties (aria-label, aria-describedby)

### Focus Management

- Visible focus indicators (2px minimum, 3:1 contrast)
- Focus trap for modals and dropdowns
- Skip navigation link for keyboard users

## Library Recommendations

### Frontend Routing

**React Router** is the recommended solution for React applications:
- Industry standard with excellent TypeScript support
- Built-in accessibility with NavLink active states

### Component Libraries

For rapid development, consider:
- Headless UI libraries (Radix UI, React Aria)
- Accessible by default
- Work with any styling approach

## Progressive Enhancement

Build navigation that works without JavaScript:
- Server-rendered HTML navigation
- Progressive enhancement with client-side routing
- Fallback for JavaScript failures

## Performance Considerations

- Lazy load route components
- Prefetch navigation targets
- Use route-based code splitting
- Implement loading states for navigation

## Related Skills

- [Theming Components](./theming-components.md) - Navigation styling
- [Designing Layouts](./designing-layouts.md) - Navigation layout patterns
- [Building Forms](./building-forms.md) - Multi-step wizard forms
- [Implementing Search Filter](./implementing-search-filter.md) - Search-driven navigation

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/implementing-navigation)
- Patterns: `references/menu-patterns.md`, `references/navigation-components.md`
- Routing: `references/client-routing.md`, `references/flask-routing.md`, `references/django-urls.md`
- Accessibility: `references/accessibility-navigation.md`
- Examples: `examples/horizontal-menu.tsx`, `examples/tab-navigation.tsx`
