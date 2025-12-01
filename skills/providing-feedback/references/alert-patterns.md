# Alert Banner Implementation Patterns

## Overview

Alert banners are persistent notifications that appear at the top of a page or section to communicate important information that requires user awareness but not immediate action.

## Alert Types & Severity

### Information Alert
```tsx
interface InfoAlert {
  type: 'info';
  icon: InfoIcon;
  title?: string;
  message: string;
  dismissible: true;
  actions?: Action[];
  style: {
    background: 'var(--alert-info-bg)',
    borderColor: 'var(--alert-info-border)',
    iconColor: 'var(--alert-info-icon)'
  };
}
```

**Use cases:**
- System announcements
- Feature updates
- Helpful tips
- Non-critical information

### Success Alert
```tsx
interface SuccessAlert {
  type: 'success';
  icon: CheckCircleIcon;
  title?: string;
  message: string;
  dismissible: true;
  autoDissmiss?: number; // Optional auto-dismiss after X seconds
  style: {
    background: 'var(--alert-success-bg)',
    borderColor: 'var(--alert-success-border)',
    iconColor: 'var(--alert-success-icon)'
  };
}
```

**Use cases:**
- Operation completed successfully
- Form submitted
- Settings saved
- Process completed

### Warning Alert
```tsx
interface WarningAlert {
  type: 'warning';
  icon: ExclamationTriangleIcon;
  title?: string;
  message: string;
  dismissible: true;
  actions?: Action[];
  style: {
    background: 'var(--alert-warning-bg)',
    borderColor: 'var(--alert-warning-border)',
    iconColor: 'var(--alert-warning-icon)'
  };
}
```

**Use cases:**
- Approaching limits (storage, usage)
- Deprecation notices
- Potential issues
- Required actions soon

### Error Alert
```tsx
interface ErrorAlert {
  type: 'error';
  icon: XCircleIcon;
  title?: string;
  message: string;
  dismissible: false; // Often not dismissible until resolved
  actions?: Action[];
  retry?: () => void;
  style: {
    background: 'var(--alert-error-bg)',
    borderColor: 'var(--alert-error-border)',
    iconColor: 'var(--alert-error-icon)'
  };
}
```

**Use cases:**
- System errors
- Connection issues
- Critical failures
- Required immediate attention

## Positioning Strategies

### Page-Level Alert (Top)
```css
.alert-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: var(--z-index-alert, 1000);
}

.alert {
  width: 100%;
  padding: 12px 24px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Push down page content */
body.has-alert {
  padding-top: 60px; /* Alert height */
}
```

### Section-Level Alert
```css
.section-alert {
  margin-bottom: 16px;
  border-radius: var(--radius-md);
  border: 1px solid;
}

.card .section-alert {
  margin: -16px -16px 16px -16px; /* Negative margin to align with card edges */
  border-radius: var(--radius-md) var(--radius-md) 0 0;
}
```

### Inline Alert (Within Content)
```css
.inline-alert {
  margin: 16px 0;
  padding: 12px 16px;
  border-left: 4px solid;
  background: var(--alert-bg);
}
```

## Alert Anatomy

### Standard Alert Structure
```tsx
function Alert({ type, title, message, dismissible, actions }) {
  return (
    <div className={`alert alert-${type}`} role="alert">
      {/* Icon */}
      <div className="alert-icon">
        {getIcon(type)}
      </div>

      {/* Content */}
      <div className="alert-content">
        {title && <div className="alert-title">{title}</div>}
        <div className="alert-message">{message}</div>

        {/* Actions */}
        {actions && (
          <div className="alert-actions">
            {actions.map(action => (
              <button
                key={action.id}
                onClick={action.onClick}
                className={`alert-action ${action.primary ? 'primary' : ''}`}
              >
                {action.label}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Dismiss button */}
      {dismissible && (
        <button className="alert-dismiss" aria-label="Dismiss">
          <XIcon />
        </button>
      )}
    </div>
  );
}
```

### Expandable Alert
```tsx
function ExpandableAlert({ title, summary, details }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="alert expandable-alert">
      <div className="alert-header">
        <div className="alert-icon">
          <InfoIcon />
        </div>
        <div className="alert-content">
          <div className="alert-title">{title}</div>
          <div className="alert-summary">{summary}</div>
        </div>
        <button
          className="alert-expand"
          onClick={() => setExpanded(!expanded)}
          aria-expanded={expanded}
        >
          {expanded ? <ChevronUpIcon /> : <ChevronDownIcon />}
        </button>
      </div>

      {expanded && (
        <div className="alert-details">
          {details}
        </div>
      )}
    </div>
  );
}
```

## Animation Patterns

### Slide Down Entry
```css
@keyframes alert-slide-down {
  from {
    transform: translateY(-100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.alert-enter {
  animation: alert-slide-down 300ms ease-out;
}
```

### Fade Out Dismissal
```css
@keyframes alert-fade-out {
  from {
    opacity: 1;
    height: auto;
  }
  to {
    opacity: 0;
    height: 0;
    margin: 0;
    padding: 0;
  }
}

.alert-exit {
  animation: alert-fade-out 200ms ease-in;
  overflow: hidden;
}
```

## Multi-Alert Management

### Alert Stack
```tsx
interface AlertStackState {
  alerts: Alert[];
  maxVisible: number;
}

function AlertStack() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const MAX_VISIBLE = 3;

  const addAlert = (alert: Alert) => {
    setAlerts(prev => {
      const newAlerts = [...prev, alert];
      // Keep only the most recent MAX_VISIBLE alerts
      return newAlerts.slice(-MAX_VISIBLE);
    });
  };

  const dismissAlert = (id: string) => {
    setAlerts(prev => prev.filter(a => a.id !== id));
  };

  return (
    <div className="alert-stack">
      {alerts.map((alert, index) => (
        <div
          key={alert.id}
          className="alert-wrapper"
          style={{
            transform: `translateY(${index * 4}px)`,
            zIndex: alerts.length - index
          }}
        >
          <Alert
            {...alert}
            onDismiss={() => dismissAlert(alert.id)}
          />
        </div>
      ))}
    </div>
  );
}
```

### Priority Queue
```typescript
class AlertQueue {
  private queue: Alert[] = [];

  add(alert: Alert) {
    // Insert based on priority
    const insertIndex = this.queue.findIndex(
      a => this.getPriority(a.type) < this.getPriority(alert.type)
    );

    if (insertIndex === -1) {
      this.queue.push(alert);
    } else {
      this.queue.splice(insertIndex, 0, alert);
    }

    this.render();
  }

  private getPriority(type: string): number {
    const priorities = {
      error: 4,
      warning: 3,
      success: 2,
      info: 1
    };
    return priorities[type] || 0;
  }
}
```

## Responsive Design

### Mobile Adaptation
```css
/* Mobile: Full width, smaller padding */
@media (max-width: 768px) {
  .alert {
    border-radius: 0;
    padding: 8px 12px;
    font-size: 14px;
  }

  .alert-actions {
    margin-top: 8px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .alert-action {
    width: 100%;
    padding: 8px;
  }
}

/* Desktop: Contained width, more padding */
@media (min-width: 769px) {
  .page-alert {
    max-width: 1200px;
    margin: 0 auto;
    border-radius: 0 0 var(--radius-md) var(--radius-md);
  }
}
```

### Compact Mode
```tsx
function CompactAlert({ message, type }) {
  return (
    <div className={`alert alert-compact alert-${type}`}>
      <span className="alert-icon-compact">
        {getCompactIcon(type)}
      </span>
      <span className="alert-message-compact">{message}</span>
    </div>
  );
}
```

## Accessibility

### ARIA Attributes
```html
<!-- Standard alert -->
<div role="alert" aria-live="polite">
  <h3 id="alert-title">System Maintenance</h3>
  <p aria-describedby="alert-title">
    The system will be down for maintenance at 2 AM.
  </p>
</div>

<!-- Critical alert -->
<div role="alert" aria-live="assertive" aria-atomic="true">
  <span class="sr-only">Error:</span>
  Connection lost. Please check your internet connection.
</div>
```

### Keyboard Navigation
```javascript
class AccessibleAlert {
  constructor(element) {
    const dismissButton = element.querySelector('.alert-dismiss');
    const actionButtons = element.querySelectorAll('.alert-action');

    // Focus management
    if (element.dataset.autoFocus === 'true') {
      (actionButtons[0] || dismissButton)?.focus();
    }

    // Keyboard shortcuts
    element.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && dismissButton) {
        dismissButton.click();
      }
    });
  }
}
```

### Screen Reader Announcements
```tsx
function ScreenReaderAlert({ message, priority = 'polite' }) {
  return (
    <div
      role="status"
      aria-live={priority}
      aria-atomic="true"
      className="sr-only"
    >
      {message}
    </div>
  );
}
```

## Implementation Examples

### With Radix UI Alert Dialog
```tsx
import * as AlertDialog from '@radix-ui/react-alert-dialog';

function CriticalAlert({ title, description, onConfirm }) {
  return (
    <AlertDialog.Root>
      <AlertDialog.Trigger asChild>
        <button className="alert-trigger">Show Alert</button>
      </AlertDialog.Trigger>

      <AlertDialog.Portal>
        <AlertDialog.Overlay className="alert-overlay" />
        <AlertDialog.Content className="alert-content">
          <AlertDialog.Title className="alert-title">
            {title}
          </AlertDialog.Title>
          <AlertDialog.Description className="alert-description">
            {description}
          </AlertDialog.Description>

          <div className="alert-buttons">
            <AlertDialog.Cancel asChild>
              <button className="alert-cancel">Cancel</button>
            </AlertDialog.Cancel>
            <AlertDialog.Action asChild>
              <button className="alert-confirm" onClick={onConfirm}>
                Confirm
              </button>
            </AlertDialog.Action>
          </div>
        </AlertDialog.Content>
      </AlertDialog.Portal>
    </AlertDialog.Root>
  );
}
```

### Custom Alert System
```tsx
const AlertContext = createContext();

export function AlertProvider({ children }) {
  const [alerts, setAlerts] = useState([]);

  const showAlert = useCallback((alert) => {
    const id = Date.now().toString();
    const newAlert = { ...alert, id };

    setAlerts(prev => [...prev, newAlert]);

    // Auto-dismiss if specified
    if (alert.autoDissmiss) {
      setTimeout(() => {
        dismissAlert(id);
      }, alert.autoDissmiss);
    }

    return id;
  }, []);

  const dismissAlert = useCallback((id) => {
    setAlerts(prev => prev.filter(a => a.id !== id));
  }, []);

  return (
    <AlertContext.Provider value={{ showAlert, dismissAlert }}>
      {children}
      <div className="alert-container">
        {alerts.map(alert => (
          <Alert
            key={alert.id}
            {...alert}
            onDismiss={() => dismissAlert(alert.id)}
          />
        ))}
      </div>
    </AlertContext.Provider>
  );
}

// Usage
function MyComponent() {
  const { showAlert } = useContext(AlertContext);

  const handleSave = async () => {
    try {
      await saveData();
      showAlert({
        type: 'success',
        message: 'Data saved successfully',
        autoDissmiss: 5000
      });
    } catch (error) {
      showAlert({
        type: 'error',
        title: 'Save Failed',
        message: error.message,
        actions: [{
          label: 'Retry',
          onClick: handleSave
        }]
      });
    }
  };
}
```

## Best Practices

1. **Clear hierarchy**: Use consistent colors and icons for each type
2. **Contextual placement**: Page-level for global, inline for specific
3. **Action clarity**: Make primary actions obvious
4. **Dismissal logic**: Allow dismissal for non-critical alerts
5. **Persistence**: Keep errors visible until resolved
6. **Mobile-first**: Design for small screens first
7. **Loading states**: Show loading in alerts for async actions
8. **Error details**: Provide actionable error messages
9. **Batch similar**: Group related alerts when possible
10. **Test accessibility**: Verify with screen readers and keyboard