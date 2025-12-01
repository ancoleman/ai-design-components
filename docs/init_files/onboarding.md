# AI-Assisted Component Library: Onboarding & Help Systems
## Master Plan for Onboarding Component Skill

**Document Version:** 1.0
**Date:** November 13, 2025

---

## Executive Summary

Onboarding components guide users through product adoption and feature discovery. This skill covers product tours, tooltips, help panels, checklists, walkthroughs, and progressive disclosure patterns.

---

## Component Taxonomy

### Product Tours

**Step-by-Step Walkthrough**
- Sequential spotlights on features
- Modal overlays with arrows
- Progress indicator (Step 2 of 5)
- Skip tour option
- Previous/Next navigation
- **Use:** First-time user experience

**Features:**
- Dismiss and resume later
- Context-sensitive (show relevant features)
- Track completion per user
- A/B test different tours

---

### Interactive Tutorials

**Guided Tasks**
- "Complete these 3 tasks to get started"
- Check off as completed
- Celebratory animation on completion
- Unlock next level
- **Example:** Duolingo, Codecademy

**Sandbox Mode**
- Safe environment to explore
- Sample data (not real)
- Undo/reset easily
- "You're in practice mode" indicator

---

### Tooltips & Hints

**Contextual Tooltips**
- Persistent until dismissed
- Arrow pointing to element
- "Got it" button
- **Use:** New feature announcements

**Pulsing Hotspots**
- Animated indicator on new features
- Click to reveal tooltip
- Auto-dismiss after first view
- **Use:** Feature discovery

**Hint System**
- Progressive hints (level 1, 2, 3)
- "Need help?" trigger
- Context-aware suggestions
- **Use:** Complex workflows

---

### Checklists

**Setup Checklist**
- "Get started in 4 steps"
- Visual progress (3/4 complete)
- Links to each task
- Celebrate completion
- **Use:** Onboarding, account setup

**Progress Tracking**
- Profile completion (60%)
- Achievement badges
- Gamification elements
- **Use:** User engagement

---

### Help Systems

**Help Panel (Sidebar)**
- Contextual help based on page
- Search help articles
- Contact support
- Collapsible
- **Use:** Complex applications

**Inline Documentation**
- Code examples
- API references
- Embedded in interface
- **Use:** Developer tools

**Video Tutorials**
- Short (1-3 min) explainer videos
- Embedded or modal
- Closed captions
- Skip/replay controls
- **Use:** Visual learners

---

## Progressive Disclosure

**Principle:** Show only what's needed, when it's needed

**Techniques:**
1. **Accordion Help**: Collapsed by default, expand for details
2. **"Learn more" Links**: Deep dive optional
3. **Advanced Settings**: Hidden behind "Show advanced"
4. **Gradual Feature Introduction**: Unlock features as user progresses

---

## Timing & Triggers

**When to Show Onboarding:**
- First login (always)
- After signup (immediate)
- New feature launch (to existing users)
- User seems stuck (smart triggering)
- User requests help

**When NOT to Show:**
- Every single session (annoying)
- When user is mid-task
- Before user can explore freely
- Too many steps (>7 steps is too long)

---

## Accessibility

**Keyboard Navigation:**
- Tab through tour steps
- ESC to dismiss
- Arrow keys for next/prev

**Screen Readers:**
- Announce step number
- Read tooltip content
- Describe highlighted element

**Reduced Motion:**
- Respect `prefers-reduced-motion`
- Disable animations
- Instant transitions

---

## Measuring Success

**Metrics:**
- Tour completion rate
- Time to first value
- Feature adoption rate
- Support ticket reduction
- User activation rate

**Optimization:**
- A/B test tour length
- Test different messaging
- Measure drop-off points
- Iterate based on data

---

## Anti-Patterns to Avoid

❌ **Forced Tours**: Must complete before using product
❌ **Too Long**: >7 steps loses attention
❌ **Every Session**: Showing same tour repeatedly
❌ **No Skip Option**: Let users explore on their own
❌ **Wall of Text**: Use visuals, keep copy concise
❌ **Blocking Everything**: Allow exploration during tour

---

## Implementation Libraries

**React:**
- **react-joyride**: Feature-rich product tours
- **intro.js**: Classic step-by-step tours
- **shepherd.js**: Flexible tour framework
- **driver.js**: Lightweight, modern

**Features to Look For:**
- Customizable styling
- Keyboard support
- Mobile responsive
- Progress tracking
- Analytics integration

---

## Skill Structure

```yaml
---
name: onboarding-help-systems
description: Component library for onboarding and help systems. Covers product tours (step-by-step walkthroughs, spotlights), interactive tutorials (guided tasks, sandbox mode), tooltips and hints (contextual, pulsing hotspots, progressive hints), checklists (setup progress, gamification), help panels (sidebar, inline docs, videos), progressive disclosure patterns, timing strategies, accessibility (keyboard, screen readers, reduced motion), and metrics for measuring success.
---
```

```
onboarding/
├── SKILL.md
├── references/
│   ├── product-tours.md
│   ├── interactive-tutorials.md
│   ├── tooltips-hints.md
│   ├── checklists.md
│   ├── help-systems.md
│   ├── progressive-disclosure.md
│   └── measuring-success.md
├── examples/
│   ├── first-time-tour.tsx
│   ├── feature-spotlight.tsx
│   ├── setup-checklist.tsx
│   └── help-panel.tsx
└── assets/
    └── celebration-animations/
```

---

## Styling & Theming

### Design Token Integration

All onboarding and help components use the **design-tokens** skill for visual styling, enabling consistent design, theme switching, and brand customization.

**See:** `skills/design-tokens/` for complete theming documentation.

### Token Categories Used

**Color Tokens:**
- `--tour-spotlight-bg` - Tour spotlight/modal background
- `--tour-spotlight-text` - Tour text color
- `--tour-overlay-bg` - Dark overlay background
- `--tour-progress-color` - Progress indicator color
- `--tour-progress-bg` - Progress track background
- `--tooltip-bg` - Contextual tooltip background
- `--tooltip-text` - Tooltip text color
- `--hotspot-color` - Pulsing hotspot color
- `--checklist-checked-color` - Completed item color
- `--checklist-unchecked-color` - Incomplete item color

**Spacing Tokens:**
- `--tour-spotlight-padding` - Tour modal padding
- `--tooltip-padding` - Tooltip padding
- `--checklist-gap` - Space between checklist items
- `--tour-arrow-size` - Arrow pointer size

**Typography Tokens:**
- `--tour-title-font-size` - Tour step title size
- `--tour-title-font-weight` - Tour title weight
- `--tour-body-font-size` - Tour body text size
- `--tooltip-font-size` - Tooltip text size

**Border & Radius:**
- `--tour-spotlight-border-radius` - Tour modal corners
- `--tooltip-border-radius` - Tooltip corners
- `--hotspot-size` - Hotspot indicator size

**Shadow Tokens:**
- `--tour-spotlight-shadow` - Tour modal elevation
- `--tooltip-shadow` - Tooltip shadow

**Motion Tokens:**
- `--tour-transition-duration` - Tour step transitions
- `--hotspot-pulse-duration` - Hotspot animation speed

### Component-Specific Tokens

```css
/* Product Tour */
--tour-spotlight-bg: var(--color-white);
--tour-spotlight-text: var(--color-text-primary);
--tour-spotlight-padding: var(--spacing-xl);
--tour-spotlight-border-radius: var(--radius-lg);
--tour-spotlight-shadow: var(--shadow-2xl);
--tour-overlay-bg: rgba(0, 0, 0, 0.7);

/* Progress Indicator */
--tour-progress-color: var(--color-primary);
--tour-progress-bg: var(--color-gray-200);

/* Tooltips */
--tooltip-bg: var(--color-gray-900);
--tooltip-text: var(--color-white);
--tooltip-padding: var(--spacing-sm);
--tooltip-border-radius: var(--radius-sm);
--tooltip-shadow: var(--shadow-md);
--tour-arrow-size: 8px;

/* Pulsing Hotspots */
--hotspot-color: var(--color-primary);
--hotspot-size: 16px;
--hotspot-pulse-duration: 2s;

/* Checklists */
--checklist-checked-color: var(--color-success);
--checklist-unchecked-color: var(--color-border);
--checklist-gap: var(--spacing-sm);

/* Animations */
--tour-transition-duration: var(--duration-normal);
```

### Theme Support

- ✅ **Light Mode** - Clear, inviting onboarding
- ✅ **Dark Mode** - Adjusted overlay and spotlight
- ✅ **High Contrast** - Strong visual guidance
- ✅ **Custom Brand Themes** - Brand-colored progress and highlights

### Example: Custom Onboarding Theming

```css
/* Friendly, welcoming onboarding theme */
:root[data-theme="friendly-onboarding"] {
  /* Softer overlay */
  --tour-overlay-bg: rgba(0, 0, 0, 0.5);

  /* Rounded, approachable */
  --tour-spotlight-border-radius: var(--radius-xl);

  /* Brand-colored progress */
  --tour-progress-color: #FF6B35;

  /* Animated hotspots */
  --hotspot-pulse-duration: 1.5s;
}
```

### Accessibility via Tokens

- **High Contrast Mode**: Strong tour spotlight visibility
- **Focus Indicators**: Clear focus management in tour steps
- **Reduced Motion**: Disable pulse animations and transitions
- **Screen Readers**: ARIA announcements with token-styled visuals
- **Keyboard Navigation**: Token-styled navigation buttons

---

## Before Implementation: Library Validation

**Optional but Recommended:** Before implementing, see `../RESEARCH_GUIDE.md` for methodology to validate library recommendations.

---

## Recommended Libraries & Tools

### **Primary: react-joyride** (Feature-Rich, Accessible)

**Library:** `/gilbarbara/react-joyride`
**Trust Score:** 9.6/10
**Code Snippets:** 29+

**Why react-joyride?**
- WAI-ARIA compliant
- Keyboard navigation
- Highly customizable
- Programmatic control
- Localization support

**Installation:**
```bash
npm install react-joyride
```

**Alternatives:** driver.js (vanilla JS), intro.js, react-shepherd

---

**END OF MASTER PLAN**

*Effective onboarding is critical for user activation and retention. These patterns help users discover value quickly while respecting their time and intelligence.*
