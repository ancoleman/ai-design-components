---
sidebar_position: 14
title: Guiding Users
description: Onboarding and help systems with product tours, tutorials, tooltips, and checklists
tags: [frontend, onboarding, help, tutorials, tooltips]
---

# Guiding Users Through Onboarding and Help Systems

Systematic patterns for onboarding users and delivering contextual help, from first-time product tours to ongoing feature discovery.

## When to Use

Use this skill when:
- Building first-time user experiences or product tours
- Implementing feature discovery and announcements
- Creating interactive tutorials or guided tasks
- Adding tooltips, hints, or contextual help
- Designing setup flows or completion checklists
- Building help panels or documentation systems
- Implementing progressive disclosure patterns
- Measuring onboarding effectiveness and user activation
- Ensuring onboarding accessibility

## Quick Decision Framework

Select the appropriate guidance mechanism based on user state and content type:

```
First-time user          → Product Tour (step-by-step)
New feature launch       → Feature Spotlight (tooltip + animation)
Complex workflow         → Interactive Tutorial (guided tasks)
Account setup            → Checklist (progress tracking)
Contextual help needed   → Tooltip/Hint system
Ongoing support          → Help Panel (sidebar/searchable)
Feature unlock           → Progressive Disclosure
```

## Core Guidance Mechanisms

### Product Tours

Step-by-step walkthroughs that guide users through key features:
- Sequential spotlights with modal overlays
- Progress indicators (Step 2 of 5)
- Skip, Previous, and Next controls
- Dismiss and resume capability
- Context-sensitive activation

**Implementation:**
```bash
npm install react-joyride
```

### Feature Spotlights

Announce new features to existing users:
- Pulsing hotspot animations
- Contextual tooltip with arrow
- "Got it" acknowledgment
- Auto-dismiss after first view
- Non-blocking overlay

### Interactive Tutorials

Guided task completion with validation:
- "Complete these tasks to get started"
- Checkbox completion tracking
- Celebration animations on completion
- Sandbox mode with sample data
- Undo and reset capabilities

### Setup Checklists

Track multi-step onboarding progress:
- Visual progress indicators (3/4 complete)
- Direct links to each task
- Profile completion percentages
- Achievement badges and gamification
- Persistent until completed

### Contextual Tooltips and Hints

Just-in-time help when users need it:
- Hover or click-triggered tooltips
- Progressive hint levels (1, 2, 3)
- "Need help?" assistance triggers
- Context-aware suggestions
- Keyboard-accessible

### Help Panels

Comprehensive help systems:
- Sidebar or drawer interface
- Contextual help based on current page
- Search help articles and docs
- Video tutorials and demos
- Contact support integration
- Collapsible and resizable

## Timing and Triggering Strategies

### When to Show Onboarding

Appropriate triggers:
- First login (always)
- Immediately after signup
- New feature launch (to existing users)
- User appears stuck (smart triggering)
- User explicitly requests help

### When NOT to Show Onboarding

Avoid showing when:
- User is mid-task or focused
- Shown in every session (becomes annoying)
- Before allowing free exploration
- Tour exceeds 7 steps (too long)
- User already dismissed or completed

**Auto-dismiss timing:**
- Simple tooltips: 5-7 seconds
- Feature announcements: 10-15 seconds or manual dismiss
- Tours: User-controlled, no auto-dismiss
- Persistent hints: Until user acknowledges

## Progressive Disclosure Patterns

Show only what's needed, when it's needed:

**Techniques:**
1. **Accordion Help**: Collapsed by default, expand for details
2. **"Learn More" Links**: Deep dive content optional
3. **Advanced Settings**: Hidden behind "Show advanced" toggle
4. **Gradual Feature Introduction**: Unlock features as user progresses
5. **Contextual Hints**: Show based on user actions

## Accessibility Requirements

### Keyboard Navigation

Essential keyboard support:
- Tab through tour steps and controls
- ESC to dismiss tours and tooltips
- Arrow keys for Previous/Next navigation
- Enter/Space to activate buttons
- Focus visible indicators

### Screen Reader Support

ARIA patterns for announcements:
- Announce step number and total (Step 2 of 5)
- Read tooltip and help content
- Describe highlighted UI elements
- Announce progress completion
- Alert on errors or blockers

### Reduced Motion

Respect `prefers-reduced-motion`:
- Disable pulsing animations
- Use instant transitions instead of animations
- Remove parallax and complex effects
- Maintain functionality without motion

## Library Recommendations

### Primary: react-joyride (Feature-Rich, Accessible)

**Trust Score:** 9.6/10

Best for comprehensive product tours:
- WAI-ARIA compliant out of the box
- Full keyboard navigation support
- Highly customizable styling
- Programmatic control
- Localization support

```bash
npm install react-joyride
```

### Alternative: driver.js (Lightweight, Modern)

Best for minimal bundle size:
- Vanilla JavaScript (framework agnostic)
- ~5KB gzipped
- Modern API design
- No dependencies

```bash
npm install driver.js
```

## Measuring Success

### Key Metrics

Track these indicators:
- Tour completion rate (target: >60%)
- Time to first value (faster = better)
- Feature adoption rate post-tour
- Support ticket reduction
- User activation rate (completed key actions)
- Drop-off points in tours

### Optimization Strategies

Iterate based on data:
- A/B test tour length (shorter often better)
- Test different messaging and copy
- Measure drop-off at each step
- Simplify steps with high abandonment
- Add skip options for returning users
- Personalize based on user type

## Anti-Patterns to Avoid

Common mistakes that harm user experience:

❌ **Forced Tours**: Requiring tour completion before product use
❌ **Too Long**: Tours exceeding 7 steps lose user attention
❌ **Every Session**: Showing same tour repeatedly
❌ **No Skip Option**: Preventing users from exploring independently
❌ **Wall of Text**: Using lengthy explanations instead of visuals
❌ **Poor Timing**: Interrupting focused work

## Design Token Integration

All onboarding components use the design-tokens skill for consistent theming:

**Token categories used:**
- **Colors**: Tour spotlight, overlay, tooltip backgrounds
- **Spacing**: Tour padding, tooltip spacing
- **Typography**: Title sizes, body text, help content
- **Borders**: Border radius for modals and tooltips
- **Shadows**: Elevation for tour spotlights
- **Motion**: Transition durations, pulse animations

Supports light, dark, high-contrast, and custom brand themes.

## Key Principles

1. **Respect User Time**: Keep tours under 7 steps, make skippable
2. **Show, Don't Tell**: Use visuals and interactions over text
3. **Progressive Enhancement**: Start simple, add guidance as needed
4. **Context is King**: Show help when and where it's relevant
5. **Measure Everything**: Track completion, iterate based on data
6. **Accessibility First**: Keyboard, screen reader, reduced motion support
7. **Celebrate Progress**: Acknowledge completion and achievements
8. **Allow Exploration**: Don't force tours, enable discovery

## Related Skills

- [Theming Components](./theming-components.md) - Onboarding styling
- [Providing Feedback](./providing-feedback.md) - Celebration animations
- [Implementing Navigation](./implementing-navigation.md) - Wizard navigation
- [Building Forms](./building-forms.md) - Setup form guidance

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/guiding-users)
- Patterns: `references/product-tours.md`, `references/interactive-tutorials.md`, `references/tooltips-hints.md`
- Implementation: `references/checklists.md`, `references/help-systems.md`, `references/progressive-disclosure.md`
- Strategy: `references/timing-strategies.md`, `references/measuring-success.md`
- Accessibility: `references/accessibility-patterns.md`
- Examples: `examples/first-time-tour.tsx`, `examples/feature-spotlight.tsx`, `examples/guided-tutorial.tsx`
