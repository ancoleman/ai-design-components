# Styling & Theming Section Template

## Purpose

This template provides the standard "Styling & Theming" section to be added to each component skill's `init.md` file. This section documents how the component uses design tokens for visual styling.

## Where to Insert

Add this section **before** the "## Skill Structure" section in each `init.md` file.

## Status

**✅ Completed:**
- `design-tokens/init.md` - Foundational theming skill created
- `forms/init.md` - Styling section added
- `ai-chat/init.md` - Styling section added
- `tables/init.md` - Styling section added

**📝 Remaining (use template below):**
- `data-viz/init.md`
- `dashboards/init.md`
- `feedback/init.md`
- `navigation/init.md`
- `search-filter/init.md`
- `layout/init.md`
- `media/init.md`
- `timeline/init.md`
- `drag-drop/init.md`
- `onboarding/init.md`

---

## Template

```markdown
---

## Styling & Theming

### Design Token Integration

All [COMPONENT TYPE] components use the **design-tokens** skill for visual styling, enabling consistent design, theme switching, and brand customization.

**See:** `skills/design-tokens/` for complete theming documentation.

### Token Categories Used

**Color Tokens:**
- `--[component]-bg` - [Description]
- `--[component]-text-color` - [Description]
- `--[component]-border-color` - [Description]
[Add relevant color tokens for this component type]

**Spacing Tokens:**
- `--[component]-padding` - [Description]
- `--[component]-gap` - [Description]
[Add relevant spacing tokens]

**Typography Tokens:**
- `--[component]-font-size` - [Description]
- `--[component]-font-weight` - [Description]
[Add relevant typography tokens]

**Border & Radius:**
- `--[component]-border-width` - [Description]
- `--[component]-border-radius` - [Description]

**Shadow Tokens:**
- `--[component]-shadow` - [Description]

[**Motion Tokens:** (if applicable)]
[- `--[component]-transition` - [Description]]

### Component-Specific Tokens

\```css
/* [Component Name] */
--[component]-primary-token: var(--semantic-token);
--[component]-secondary-token: value;

/* Example values showing token hierarchy */
--button-bg-primary: var(--color-primary);
--button-text-primary: var(--color-white);
--button-padding: var(--spacing-md);
\```

### Theme Support

- ✅ **Light Mode** - [Description of light theme]
- ✅ **Dark Mode** - [Description of dark theme]
- ✅ **High Contrast** - [Description of accessibility theme]
- ✅ **Custom Brand Themes** - [Description of customization]

### Example: Custom Theming

\```css
/* Example custom theme for [component] */
:root[data-theme="custom-[component]"] {
  /* Override specific tokens */
  --[component]-primary-token: #CustomValue;

  /* Adjust spacing/sizing */
  --[component]-spacing: var(--spacing-lg);

  /* Customize appearance */
  --[component]-border-radius: var(--radius-xl);
}
\```

[**Dark Mode Considerations:** (optional, if component has significant dark mode differences)]
[\```css
:root[data-theme="dark"] {
  --[component]-bg: var(--color-gray-900);
  --[component]-text: var(--color-gray-100);
  /* ... other dark mode overrides */
}
\```]

### Accessibility via Tokens

- **High Contrast Mode**: [Describe how tokens ensure accessibility]
- **Reduced Motion**: [Describe motion preference handling]
- **Color Contrast**: [Describe WCAG compliance]
- **Focus Indicators**: [Describe focus state tokens]

---
```

## Component-Specific Token Examples

### Data Visualization
```css
--chart-primary-color: var(--color-primary);
--chart-secondary-color: var(--color-secondary);
--chart-axis-color: var(--color-text-secondary);
--chart-grid-color: var(--color-border);
--chart-tooltip-bg: var(--color-gray-900);
--chart-tooltip-text: var(--color-white);
```

### Dashboards
```css
--dashboard-bg: var(--color-bg-secondary);
--widget-bg: var(--color-white);
--widget-shadow: var(--shadow-md);
--widget-border-radius: var(--radius-lg);
--kpi-value-color: var(--color-text-primary);
--kpi-trend-positive: var(--color-success);
--kpi-trend-negative: var(--color-error);
```

### Feedback/Notifications
```css
--toast-bg: var(--color-gray-900);
--toast-text: var(--color-white);
--toast-shadow: var(--shadow-xl);
--alert-success-bg: var(--color-success-bg);
--alert-error-bg: var(--color-error-bg);
--modal-backdrop-bg: rgba(0, 0, 0, 0.5);
```

### Navigation
```css
--nav-bg: var(--color-white);
--nav-border-color: var(--color-border);
--nav-item-color: var(--color-text-primary);
--nav-item-hover-bg: var(--color-gray-100);
--nav-item-active-bg: var(--color-primary-50);
--nav-item-active-color: var(--color-primary);
```

### Layout
```css
--layout-max-width: 1280px;
--layout-gutter: var(--spacing-md);
--container-padding: var(--spacing-lg);
--grid-gap: var(--spacing-md);
```

### Media
```css
--image-border-radius: var(--radius-md);
--image-shadow: var(--shadow-md);
--video-player-bg: var(--color-black);
--video-controls-bg: rgba(0, 0, 0, 0.7);
--upload-zone-border-color: var(--color-border);
--upload-zone-border-color-active: var(--color-primary);
```

### Timeline
```css
--timeline-line-color: var(--color-border);
--timeline-dot-color: var(--color-primary);
--timeline-item-bg: var(--color-white);
--timeline-item-shadow: var(--shadow-sm);
--timestamp-color: var(--color-text-secondary);
```

### Drag-Drop
```css
--draggable-cursor: grab;
--dragging-cursor: grabbing;
--drop-zone-border-color: var(--color-border);
--drop-zone-border-color-active: var(--color-primary);
--drop-zone-bg-active: var(--color-primary-50);
--dragged-item-opacity: 0.5;
```

### Onboarding
```css
--tour-spotlight-bg: var(--color-white);
--tour-spotlight-shadow: var(--shadow-2xl);
--tour-overlay-bg: rgba(0, 0, 0, 0.7);
--tour-progress-color: var(--color-primary);
--tooltip-bg: var(--color-gray-900);
--tooltip-text: var(--color-white);
```

---

## Integration Benefits

By adding this section to each component init.md, we achieve:

1. **Separation of Concerns**: Component behavior separate from visual styling
2. **Consistency**: All components reference the same token system
3. **Theme Support**: Built-in light/dark/high-contrast/custom themes
4. **Brand Flexibility**: Easy to apply brand identity via token overrides
5. **Accessibility**: WCAG compliance handled at token level
6. **Documentation**: Clear reference for which tokens each component uses
7. **Progressive Disclosure**: Detailed token docs in design-tokens skill

---

## Quick Integration Steps

For each remaining component init.md:

1. **Identify location**: Find "## Skill Structure" section
2. **Add section**: Insert "## Styling & Theming" before it
3. **Customize tokens**: List relevant tokens for that component type
4. **Provide examples**: Show how to override tokens for custom theming
5. **Document accessibility**: Describe how tokens ensure WCAG compliance

---

*This template ensures consistent styling documentation across all component skills while maintaining the flexibility for component-specific token definitions.*
