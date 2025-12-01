# Product Tours: Step-by-Step Walkthroughs

**Purpose:** This document provides detailed patterns for implementing product tours that guide users through key features with sequential spotlights and modal overlays.

## Overview

Product tours are step-by-step walkthroughs that introduce users to your product's core functionality through a series of focused interactions. Each step highlights a specific UI element and explains its purpose or usage.

## When to Use Product Tours

**Appropriate scenarios:**
- First-time user onboarding
- Major UI/UX redesigns
- Complex interfaces with multiple features
- Feature-rich applications requiring guided introduction
- B2B SaaS products with learning curves

**Not appropriate for:**
- Simple, self-explanatory interfaces
- Every single feature (focus on core value)
- Mobile apps with limited screen space
- Returning users (offer skip/resume options)

## Core Components

### 1. Spotlight/Beacon
- Highlights target UI element
- Uses overlay to dim surrounding content
- Arrow or pointer to specific element
- Adjusts position based on element location

### 2. Modal/Tooltip Content
- Concise title (4-8 words)
- Brief description (1-2 sentences max)
- Screenshot or visual aid (optional)
- Clear call-to-action

### 3. Navigation Controls
- "Next" button (primary action)
- "Back" button (secondary, from step 2+)
- "Skip tour" link (always visible)
- Progress indicator (Step X of Y)

### 4. Progress Tracking
- Visual progress bar or dots
- Step counter (current/total)
- Estimated time remaining (optional)

## Best Practices

### Length and Pacing

**Optimal tour length:**
- 3-5 steps: Ideal for most products
- 5-7 steps: Maximum before fatigue sets in
- 7+ steps: Split into multiple tours or make optional

**Step duration:**
- Each step should take 5-15 seconds to read/understand
- Total tour: 1-3 minutes maximum
- Respect user time and attention

### Content Guidelines

**Title:**
- Action-oriented (e.g., "Create Your First Project")
- Clear and specific
- 4-8 words maximum

**Description:**
- One clear benefit or explanation
- 1-2 sentences (25-40 words)
- Conversational, friendly tone
- Avoid jargon

**Visual hierarchy:**
- Title: Largest, bold
- Description: Medium size, regular weight
- Controls: Clearly visible and clickable

### Positioning

**Spotlight placement:**
- Default: Center or near highlighted element
- Adjust for screen edges and scrolling
- Ensure no overlap with critical UI
- Mobile: Often bottom or top sheet

**Arrow/pointer:**
- Points directly at target element
- Adjusts based on available space
- Clear visual connection

## Implementation Patterns

### Pattern 1: Modal Tour (Traditional)

**Characteristics:**
- Full modal overlay
- Dimmed background
- Cannot interact with app during tour
- Clear, focused experience

**Use when:**
- First-time user experience
- Critical onboarding flow
- Sequential steps must be followed

**Example structure:**
```typescript
const tourSteps = [
  {
    target: '.dashboard',
    title: 'Welcome to Your Dashboard',
    content: 'This is your central hub for all activities.',
    placement: 'center',
    disableBeacon: true,
  },
  {
    target: '.create-button',
    title: 'Create Your First Project',
    content: 'Click here to start a new project.',
    placement: 'bottom',
  },
  // ... more steps
];
```

### Pattern 2: Contextual Beacons

**Characteristics:**
- Pulsing beacon on UI elements
- Click to view tooltip with info
- Non-blocking, user-initiated
- Can interact with app between steps

**Use when:**
- Optional feature discovery
- Non-linear exploration
- Advanced features for power users

### Pattern 3: Hybrid Tour

**Characteristics:**
- Combines modal and beacon patterns
- Blocks critical steps
- Allows exploration for optional steps
- Flexibility with guidance

**Use when:**
- Complex onboarding with branches
- Mix of required and optional steps
- Power user vs. beginner paths

## User Controls

### Skip Functionality

**Always provide:**
- "Skip tour" link in every step
- Confirm skip if tour >3 steps
- Remember skip preference
- Offer tour restart from help menu

**Skip confirmation (for longer tours):**
```
Are you sure you want to skip the tour?
You can restart it anytime from the Help menu.
[Skip Tour] [Continue Tour]
```

### Pause and Resume

**For tours >5 steps:**
- Save progress automatically
- Allow resume on next login
- Offer "Continue where you left off" option
- Expire after X days or completion

### Tour Completion

**On final step:**
- Congratulatory message
- Clear indication of completion
- Next steps or call-to-action
- Optional: Achievement badge or gamification

**Example completion:**
```
🎉 You're All Set!
You've completed the tour. Ready to [Primary Action]?
[Get Started]
```

## Accessibility

### Keyboard Navigation

**Required keyboard support:**
- Tab: Move between controls (Next, Back, Skip)
- Enter/Space: Activate buttons
- Escape: Close/skip tour (with confirmation)
- Arrow keys: Previous/Next step (optional)

### Screen Reader Support

**ARIA attributes:**
```html
<div role="dialog" aria-labelledby="tour-title" aria-describedby="tour-content">
  <h2 id="tour-title">Step 2 of 5: Create Your First Project</h2>
  <p id="tour-content">Click the Create button to start...</p>
  <div role="group" aria-label="Tour navigation">
    <button aria-label="Previous step">Back</button>
    <button aria-label="Next step">Next</button>
    <button aria-label="Skip tour">Skip</button>
  </div>
</div>
```

**Announcements:**
- Announce step number and total
- Read title and content automatically
- Alert on tour completion

### Focus Management

**Focus order:**
1. Tour modal gains focus when opened
2. Focus moves to first interactive element (usually "Next")
3. Focus trapped within modal during tour
4. Focus restored to trigger element on close

### Reduced Motion

**Respect `prefers-reduced-motion`:**
- Disable spotlight animations
- Use instant transitions instead of slides
- Remove pulsing beacon effects
- Maintain functionality without motion

## Timing and Triggering

### When to Show

**First-time users:**
- Immediately after signup/login
- After account setup completion
- When dashboard/main view loads

**Returning users:**
- Never auto-show again (unless requested)
- Offer restart option in help menu
- Show for major UI changes (with announcement)

### Smart Triggering

**Context-aware tours:**
- Show relevant tours based on user actions
- Delay tours if user actively engaging
- Pause tours if user navigates away
- Resume or restart based on context

**User signals for tour:**
- Inactivity for X seconds (hesitation)
- Multiple page views without action
- Clicking on help or "?" icons
- Explicit "Show me how" requests

## Analytics and Optimization

### Key Metrics

**Track these events:**
- Tour started (% of eligible users)
- Step completion rate (per step)
- Tour completion rate (end-to-end)
- Skip rate (overall and per step)
- Time spent per step
- Drop-off points

### Optimization Strategies

**Iterative improvements:**
1. **High skip rate (>50%)**: Tour too long or irrelevant
   - Shorten tour to core features
   - Make tour optional
   - Improve targeting

2. **Drop-off at specific step**: Step confusing or overwhelming
   - Simplify content
   - Add visual aid
   - Split into two steps

3. **Low completion rate (<40%)**: Tour not engaging
   - Make more interactive
   - Add progress incentives
   - Improve copy and visuals

4. **Fast progression**: Users skipping content
   - Content too basic
   - Users already familiar
   - Offer advanced skip option

### A/B Testing

**Test variations:**
- Tour length (3 steps vs. 5 steps)
- Content style (formal vs. conversational)
- Visual style (modal vs. tooltip)
- Timing (immediate vs. delayed)
- Progress indicators (bar vs. dots vs. numbers)

## react-joyride Implementation

### Basic Setup

```typescript
import Joyride, { Step, CallBackProps } from 'react-joyride';

const steps: Step[] = [
  {
    target: '.dashboard',
    content: 'Welcome to your dashboard!',
    placement: 'center',
    disableBeacon: true,
  },
  {
    target: '.create-button',
    content: 'Create your first project here.',
    placement: 'bottom',
  },
];

function ProductTour() {
  const [run, setRun] = useState(true);

  const handleJoyrideCallback = (data: CallBackProps) => {
    const { status, action } = data;

    if (status === 'finished' || status === 'skipped') {
      setRun(false);
      // Save completion state
      localStorage.setItem('tourCompleted', 'true');
    }
  };

  return (
    <Joyride
      steps={steps}
      run={run}
      continuous
      showProgress
      showSkipButton
      callback={handleJoyrideCallback}
      styles={{
        options: {
          primaryColor: 'var(--color-primary)',
          zIndex: 10000,
        },
      }}
    />
  );
}
```

### Custom Styling with Design Tokens

```typescript
const joyrideStyles = {
  options: {
    backgroundColor: 'var(--tour-spotlight-bg)',
    textColor: 'var(--tour-spotlight-text)',
    primaryColor: 'var(--color-primary)',
    overlayColor: 'var(--tour-overlay-bg)',
    arrowColor: 'var(--tour-spotlight-bg)',
    borderRadius: 'var(--tour-spotlight-border-radius)',
    zIndex: 10000,
  },
  tooltip: {
    padding: 'var(--tour-spotlight-padding)',
    boxShadow: 'var(--tour-spotlight-shadow)',
  },
  tooltipContent: {
    fontSize: 'var(--tour-body-font-size)',
  },
  tooltipTitle: {
    fontSize: 'var(--tour-title-font-size)',
    fontWeight: 'var(--tour-title-font-weight)',
  },
};
```

### Advanced Features

**Conditional steps:**
```typescript
const steps = useMemo(() => {
  const baseSteps = [...];

  if (userHasProjects) {
    // Skip project creation step
    return baseSteps.filter(step => step.target !== '.create-button');
  }

  return baseSteps;
}, [userHasProjects]);
```

**Programmatic control:**
```typescript
const [stepIndex, setStepIndex] = useState(0);

// Jump to specific step
function goToStep(index: number) {
  setStepIndex(index);
}

// Restart tour
function restartTour() {
  setStepIndex(0);
  setRun(true);
}

<Joyride
  stepIndex={stepIndex}
  steps={steps}
  run={run}
  // ...
/>
```

## Common Pitfalls

### Mistakes to Avoid

❌ **Too many steps**: >7 steps overwhelms users
❌ **Too much text**: Long paragraphs lose attention
❌ **No skip option**: Forces users through tour
❌ **Repeating every session**: Annoys returning users
❌ **Blocking all interaction**: Prevents exploration
❌ **Generic content**: Not specific to user context
❌ **Poor mobile experience**: Desktop-only tours
❌ **Missing accessibility**: Keyboard/screen reader gaps

### Solutions

✅ **Limit to 3-5 key steps**: Focus on core value
✅ **Use concise copy**: 1-2 sentences per step
✅ **Always allow skip**: Respect user agency
✅ **Remember completion**: localStorage or backend
✅ **Allow interaction**: Use beacons, not just modals
✅ **Personalize**: Conditional steps based on user
✅ **Mobile-responsive**: Test on all screen sizes
✅ **Full keyboard support**: Tab, Enter, Escape

## Related Patterns

- **Feature Spotlights**: Single-feature announcements
- **Interactive Tutorials**: Task-based guided learning
- **Contextual Tooltips**: Just-in-time help
- **Checklists**: Track multi-step completion
- **Help Panels**: Comprehensive documentation

## References

- WAI-ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/
- react-joyride Documentation: https://docs.react-joyride.com/
- User Onboarding Best Practices: Industry standards and research

---

*Keep tours short, skippable, and focused on delivering core value quickly.*
