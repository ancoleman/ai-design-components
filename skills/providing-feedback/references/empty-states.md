# Empty State Design Patterns

## Overview

Empty states appear when there's no data to display. They're opportunities to guide users, explain features, and encourage action rather than showing blank screens.

## Types of Empty States

### First Use Empty State
```tsx
interface FirstUseEmptyState {
  type: 'first-use';
  illustration: 'welcome' | 'onboarding';
  headline: string;
  description: string;
  primaryAction: {
    label: string;
    onClick: () => void;
  };
  secondaryAction?: {
    label: string;
    onClick: () => void;
  };
}
```

**Example:**
```tsx
function FirstUseEmpty() {
  return (
    <div className="empty-state empty-first-use">
      <WelcomeIllustration />
      <h2>Welcome to Projects</h2>
      <p>Create your first project to get started with organizing your work</p>
      <button className="btn-primary">Create Project</button>
      <button className="btn-link">Import Existing</button>
    </div>
  );
}
```

### No Results Empty State
```tsx
interface NoResultsEmptyState {
  type: 'no-results';
  searchQuery?: string;
  suggestions?: string[];
  illustration: 'search' | 'filter';
}
```

**Example:**
```tsx
function NoResultsEmpty({ query, suggestions }) {
  return (
    <div className="empty-state empty-no-results">
      <SearchIllustration />
      <h2>No results found</h2>
      <p>We couldn't find anything matching "{query}"</p>

      {suggestions && (
        <div className="suggestions">
          <p>Try:</p>
          <ul>
            {suggestions.map(suggestion => (
              <li key={suggestion}>
                <button className="suggestion-link">
                  {suggestion}
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}

      <button className="btn-secondary">Clear Filters</button>
    </div>
  );
}
```

### Error Empty State
```tsx
interface ErrorEmptyState {
  type: 'error';
  error: Error;
  canRetry: boolean;
  onRetry?: () => void;
}
```

**Example:**
```tsx
function ErrorEmpty({ error, onRetry }) {
  return (
    <div className="empty-state empty-error">
      <ErrorIllustration />
      <h2>Something went wrong</h2>
      <p>{error.message || 'We couldn\'t load the data'}</p>

      <div className="empty-actions">
        <button onClick={onRetry} className="btn-primary">
          Try Again
        </button>
        <button className="btn-link">Contact Support</button>
      </div>
    </div>
  );
}
```

### Permission Denied Empty State
```tsx
function PermissionDeniedEmpty() {
  return (
    <div className="empty-state empty-permission">
      <LockIllustration />
      <h2>Access Restricted</h2>
      <p>You don't have permission to view this content</p>
      <button className="btn-primary">Request Access</button>
    </div>
  );
}
```

### Cleared/Deleted Empty State
```tsx
function ClearedEmpty() {
  return (
    <div className="empty-state empty-cleared">
      <TrashIllustration />
      <h2>All items deleted</h2>
      <p>You've cleared all items from this list</p>
      <button className="btn-primary">Add New Item</button>
      <button className="btn-link">Restore Deleted</button>
    </div>
  );
}
```

## Empty State Anatomy

### Standard Structure
```tsx
function EmptyState({
  illustration,
  headline,
  description,
  primaryAction,
  secondaryAction
}) {
  return (
    <div className="empty-state">
      {/* Illustration */}
      <div className="empty-illustration">
        {illustration}
      </div>

      {/* Content */}
      <div className="empty-content">
        <h2 className="empty-headline">{headline}</h2>
        <p className="empty-description">{description}</p>
      </div>

      {/* Actions */}
      <div className="empty-actions">
        {primaryAction && (
          <button
            className="btn-primary"
            onClick={primaryAction.onClick}
          >
            {primaryAction.label}
          </button>
        )}

        {secondaryAction && (
          <button
            className="btn-secondary"
            onClick={secondaryAction.onClick}
          >
            {secondaryAction.label}
          </button>
        )}
      </div>
    </div>
  );
}
```

### Layout Styles
```css
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 48px 24px;
  min-height: 400px;
}

.empty-illustration {
  margin-bottom: 32px;
  opacity: 0.8;
}

.empty-illustration svg {
  width: 200px;
  height: 200px;
}

.empty-content {
  max-width: 480px;
  margin-bottom: 32px;
}

.empty-headline {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.empty-description {
  font-size: 16px;
  color: var(--text-secondary);
  line-height: 1.5;
}

.empty-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: center;
}

/* Responsive */
@media (max-width: 768px) {
  .empty-state {
    padding: 32px 16px;
  }

  .empty-illustration svg {
    width: 160px;
    height: 160px;
  }

  .empty-headline {
    font-size: 20px;
  }

  .empty-actions {
    flex-direction: column;
    width: 100%;
    max-width: 280px;
  }

  .empty-actions button {
    width: 100%;
  }
}
```

## Illustration Patterns

### Simple SVG Illustrations
```tsx
function FolderIllustration() {
  return (
    <svg viewBox="0 0 200 200" fill="none">
      <rect
        x="40"
        y="60"
        width="120"
        height="100"
        rx="4"
        fill="var(--illustration-primary)"
        opacity="0.2"
      />
      <path
        d="M40 80 L40 60 Q40 56 44 56 L76 56 L84 64 L156 64 Q160 64 160 68 L160 80"
        fill="var(--illustration-primary)"
        opacity="0.3"
      />
      <circle
        cx="100"
        cy="110"
        r="20"
        fill="var(--illustration-accent)"
        opacity="0.4"
      />
      <text
        x="100"
        y="115"
        textAnchor="middle"
        fill="var(--illustration-text)"
        fontSize="24"
        fontWeight="bold"
      >
        ?
      </text>
    </svg>
  );
}
```

### Animated Illustrations
```css
@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.empty-illustration.animated svg {
  animation: float 3s ease-in-out infinite;
}

/* Subtle motion for elements */
.empty-illustration svg .floating-element {
  animation: float 4s ease-in-out infinite;
  animation-delay: 0.5s;
}
```

### Icon-Based Illustrations
```tsx
function IconIllustration({ icon: Icon, badge }) {
  return (
    <div className="icon-illustration">
      <div className="icon-background">
        <Icon size={64} />
        {badge && (
          <div className="icon-badge">{badge}</div>
        )}
      </div>
    </div>
  );
}
```

## Context-Specific Empty States

### Table Empty State
```tsx
function TableEmptyState({ columns }) {
  return (
    <tr className="table-empty-row">
      <td colSpan={columns} className="table-empty-cell">
        <div className="empty-state empty-state-inline">
          <TableIllustration />
          <h3>No data available</h3>
          <p>Start by adding your first record</p>
          <button className="btn-primary btn-small">Add Record</button>
        </div>
      </td>
    </tr>
  );
}
```

### List Empty State
```tsx
function ListEmptyState() {
  return (
    <li className="list-empty-item">
      <div className="empty-state empty-state-compact">
        <p className="empty-message">No items in this list</p>
        <button className="btn-link">Add item</button>
      </div>
    </li>
  );
}
```

### Grid Empty State
```tsx
function GridEmptyState() {
  return (
    <div className="grid-empty-container">
      <div className="empty-state">
        <GridIllustration />
        <h2>No items to display</h2>
        <p>Upload files or create new items to see them here</p>
        <div className="empty-actions">
          <button className="btn-primary">
            <UploadIcon /> Upload Files
          </button>
          <button className="btn-secondary">
            <PlusIcon /> Create New
          </button>
        </div>
      </div>
    </div>
  );
}
```

## Progressive Enhancement

### Loading to Empty Transition
```tsx
function ProgressiveEmptyState() {
  const [state, setState] = useState<'loading' | 'empty' | 'error'>('loading');

  useEffect(() => {
    // Simulate data fetch
    setTimeout(() => {
      setState('empty'); // or 'error'
    }, 2000);
  }, []);

  if (state === 'loading') {
    return <LoadingSkeleton />;
  }

  if (state === 'error') {
    return <ErrorEmpty />;
  }

  return <FirstUseEmpty />;
}
```

### Animated Entry
```css
@keyframes empty-state-enter {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.empty-state {
  animation: empty-state-enter 400ms ease-out;
}

.empty-state > * {
  animation: empty-state-enter 400ms ease-out backwards;
}

.empty-illustration {
  animation-delay: 0ms;
}

.empty-content {
  animation-delay: 100ms;
}

.empty-actions {
  animation-delay: 200ms;
}
```

## Educational Empty States

### Feature Discovery
```tsx
function FeatureDiscoveryEmpty() {
  const [currentTip, setCurrentTip] = useState(0);
  const tips = [
    'Use keyboard shortcuts for faster navigation',
    'Drag and drop files to upload',
    'Star important items for quick access'
  ];

  return (
    <div className="empty-state empty-educational">
      <LightbulbIllustration />
      <h2>Did you know?</h2>
      <p className="tip-content">{tips[currentTip]}</p>

      <div className="tip-navigation">
        <button
          onClick={() => setCurrentTip((currentTip - 1 + tips.length) % tips.length)}
          aria-label="Previous tip"
        >
          ←
        </button>
        <span>{currentTip + 1} / {tips.length}</span>
        <button
          onClick={() => setCurrentTip((currentTip + 1) % tips.length)}
          aria-label="Next tip"
        >
          →
        </button>
      </div>

      <button className="btn-primary">Get Started</button>
    </div>
  );
}
```

### Onboarding Empty State
```tsx
function OnboardingEmpty() {
  const steps = [
    { icon: '📁', label: 'Create a project' },
    { icon: '👥', label: 'Invite team members' },
    { icon: '🚀', label: 'Start collaborating' }
  ];

  return (
    <div className="empty-state empty-onboarding">
      <h2>Get started in 3 easy steps</h2>

      <ol className="onboarding-steps">
        {steps.map((step, index) => (
          <li key={index} className="onboarding-step">
            <span className="step-icon">{step.icon}</span>
            <span className="step-label">{step.label}</span>
          </li>
        ))}
      </ol>

      <button className="btn-primary">Start Setup</button>
    </div>
  );
}
```

## Gamification Elements

### Achievement Empty State
```tsx
function AchievementEmpty() {
  return (
    <div className="empty-state empty-achievement">
      <TrophyIllustration />
      <h2>Complete your first task!</h2>
      <p>You're 0/5 tasks away from your first achievement</p>

      <div className="progress-bar">
        <div className="progress-fill" style={{ width: '0%' }} />
      </div>

      <button className="btn-primary">Create Task</button>
    </div>
  );
}
```

### Motivational Empty State
```tsx
function MotivationalEmpty() {
  const quotes = [
    'Every expert was once a beginner',
    'The journey of a thousand miles begins with a single step',
    'Start where you are, use what you have, do what you can'
  ];

  const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];

  return (
    <div className="empty-state empty-motivational">
      <RocketIllustration />
      <h2>Ready to begin?</h2>
      <blockquote className="motivational-quote">
        "{randomQuote}"
      </blockquote>
      <button className="btn-primary">Take the First Step</button>
    </div>
  );
}
```

## Accessibility Considerations

### Screen Reader Support
```tsx
function AccessibleEmptyState({ type, message }) {
  return (
    <div
      className="empty-state"
      role="status"
      aria-label={`Empty state: ${type}`}
    >
      <div aria-hidden="true" className="empty-illustration">
        {/* Visual illustration not announced */}
      </div>

      <div className="empty-content">
        <h2>{message}</h2>
        <p>No items to display</p>
      </div>

      <div className="empty-actions">
        <button
          className="btn-primary"
          aria-describedby="empty-description"
        >
          Add Item
        </button>
      </div>
    </div>
  );
}
```

### Keyboard Navigation
```tsx
function KeyboardFriendlyEmpty() {
  useEffect(() => {
    // Auto-focus primary action for keyboard users
    const primaryButton = document.querySelector('.empty-state .btn-primary');
    if (primaryButton && document.activeElement === document.body) {
      (primaryButton as HTMLElement).focus();
    }
  }, []);

  return (
    <div className="empty-state">
      {/* Empty state content */}
    </div>
  );
}
```

## Best Practices

1. **Be helpful**: Explain why it's empty and how to fix it
2. **Stay positive**: Use friendly, encouraging language
3. **Provide actions**: Always include at least one clear action
4. **Keep it simple**: Don't overwhelm with too many options
5. **Use illustrations**: Visual elements make empty states less stark
6. **Consider context**: Tailor message to specific situation
7. **Progressive disclosure**: Start simple, reveal complexity as needed
8. **Mobile-friendly**: Ensure responsive design and touch targets
9. **Educate users**: Use empty states to teach features
10. **Test variations**: A/B test different messages and designs