# Progress Indicator Implementation Patterns

## Overview

Progress indicators communicate the status of operations, helping users understand system activity and manage expectations for completion times.

## When to Show Progress

### Timing Thresholds
```typescript
interface ProgressThresholds {
  immediate: 0;        // < 100ms: No indicator
  quick: 100;         // 100ms-1s: Small spinner
  moderate: 1000;     // 1-5s: Spinner + text
  long: 5000;         // 5-30s: Progress bar
  veryLong: 30000;    // > 30s: Progress + cancel
}

function getProgressIndicator(expectedDuration: number) {
  if (expectedDuration < 100) return null;
  if (expectedDuration < 1000) return 'spinner-small';
  if (expectedDuration < 5000) return 'spinner-with-text';
  if (expectedDuration < 30000) return 'progress-bar';
  return 'progress-bar-with-cancel';
}
```

## Spinner Patterns

### Basic Spinner
```css
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.spinner {
  width: 24px;
  height: 24px;
  border: 3px solid var(--spinner-track);
  border-top-color: var(--spinner-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* Size variants */
.spinner-small {
  width: 16px;
  height: 16px;
  border-width: 2px;
}

.spinner-large {
  width: 32px;
  height: 32px;
  border-width: 4px;
}
```

### Dots Spinner
```css
@keyframes pulse {
  0%, 60%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  30% {
    transform: scale(1);
    opacity: 1;
  }
}

.dots-spinner {
  display: flex;
  gap: 4px;
}

.dots-spinner .dot {
  width: 8px;
  height: 8px;
  background: var(--spinner-color);
  border-radius: 50%;
  animation: pulse 1.4s ease-in-out infinite;
}

.dots-spinner .dot:nth-child(1) {
  animation-delay: 0s;
}

.dots-spinner .dot:nth-child(2) {
  animation-delay: 0.2s;
}

.dots-spinner .dot:nth-child(3) {
  animation-delay: 0.4s;
}
```

### Spinner with Message
```tsx
function SpinnerWithMessage({ message, showElapsed = false }) {
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    if (!showElapsed) return;

    const interval = setInterval(() => {
      setElapsed(prev => prev + 1);
    }, 1000);

    return () => clearInterval(interval);
  }, [showElapsed]);

  return (
    <div className="spinner-container">
      <div className="spinner" />
      <div className="spinner-message">
        <div>{message}</div>
        {showElapsed && elapsed > 10 && (
          <div className="spinner-elapsed">
            ({elapsed} seconds)
          </div>
        )}
      </div>
    </div>
  );
}
```

## Progress Bar Patterns

### Determinate Progress Bar
```tsx
interface DeterminateProgressProps {
  value: number;
  max?: number;
  showLabel?: boolean;
  showPercentage?: boolean;
  size?: 'small' | 'medium' | 'large';
}

function DeterminateProgress({
  value,
  max = 100,
  showLabel = false,
  showPercentage = true,
  size = 'medium'
}) {
  const percentage = Math.round((value / max) * 100);

  return (
    <div className={`progress-container progress-${size}`}>
      {showLabel && (
        <div className="progress-label">
          {showPercentage && <span>{percentage}%</span>}
        </div>
      )}

      <div className="progress-track">
        <div
          className="progress-bar"
          style={{ width: `${percentage}%` }}
          role="progressbar"
          aria-valuenow={value}
          aria-valuemin={0}
          aria-valuemax={max}
        >
          {showPercentage && !showLabel && (
            <span className="progress-text">{percentage}%</span>
          )}
        </div>
      </div>
    </div>
  );
}
```

### Indeterminate Progress Bar
```css
@keyframes indeterminate {
  0% {
    left: -100%;
    width: 100%;
  }
  100% {
    left: 100%;
    width: 100%;
  }
}

.progress-indeterminate .progress-bar {
  width: 100%;
  position: relative;
  overflow: hidden;
}

.progress-indeterminate .progress-bar::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  height: 100%;
  width: 100%;
  background: var(--progress-color);
  animation: indeterminate 2s linear infinite;
}
```

### Segmented Progress
```tsx
function SegmentedProgress({ currentStep, totalSteps, labels }) {
  return (
    <div className="segmented-progress">
      <div className="segments">
        {Array.from({ length: totalSteps }).map((_, index) => (
          <div
            key={index}
            className={`segment ${index < currentStep ? 'completed' : ''}
                       ${index === currentStep ? 'active' : ''}`}
          >
            <div className="segment-bar" />
            {labels && (
              <div className="segment-label">{labels[index]}</div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
```

### Circular Progress
```tsx
function CircularProgress({ value, size = 120, strokeWidth = 8 }) {
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (value / 100) * circumference;

  return (
    <div className="circular-progress">
      <svg width={size} height={size}>
        <circle
          className="circular-progress-track"
          cx={size / 2}
          cy={size / 2}
          r={radius}
          strokeWidth={strokeWidth}
          fill="none"
        />
        <circle
          className="circular-progress-bar"
          cx={size / 2}
          cy={size / 2}
          r={radius}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          fill="none"
        />
      </svg>
      <div className="circular-progress-text">
        {value}%
      </div>
    </div>
  );
}
```

## Linear Progress (Top Bar)

### Page Load Progress
```tsx
function PageLoadProgress() {
  const [progress, setProgress] = useState(0);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    // Simulate page load
    setVisible(true);

    const intervals = [
      setTimeout(() => setProgress(30), 100),
      setTimeout(() => setProgress(60), 500),
      setTimeout(() => setProgress(90), 800),
      setTimeout(() => setProgress(100), 1000),
      setTimeout(() => setVisible(false), 1200)
    ];

    return () => intervals.forEach(clearTimeout);
  }, []);

  if (!visible) return null;

  return (
    <div className="page-progress">
      <div
        className="page-progress-bar"
        style={{ width: `${progress}%` }}
      />
    </div>
  );
}
```

### NProgress-style Implementation
```css
.nprogress {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  z-index: 10000;
}

.nprogress-bar {
  background: var(--primary-color);
  height: 100%;
  transition: width 200ms ease;
}

.nprogress-peg {
  display: block;
  position: absolute;
  right: 0;
  width: 100px;
  height: 100%;
  box-shadow: 0 0 10px var(--primary-color), 0 0 5px var(--primary-color);
  opacity: 1;
  transform: rotate(3deg) translate(0px, -4px);
}
```

## Skeleton Screens

### Basic Skeleton
```css
@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.skeleton {
  background: linear-gradient(
    90deg,
    var(--skeleton-base) 25%,
    var(--skeleton-highlight) 50%,
    var(--skeleton-base) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--radius-sm);
}

.skeleton-text {
  height: 16px;
  margin-bottom: 8px;
}

.skeleton-title {
  height: 24px;
  width: 50%;
  margin-bottom: 16px;
}

.skeleton-image {
  height: 200px;
  width: 100%;
  margin-bottom: 16px;
}
```

### Card Skeleton
```tsx
function CardSkeleton() {
  return (
    <div className="card">
      <div className="skeleton skeleton-image" />
      <div className="card-body">
        <div className="skeleton skeleton-title" />
        <div className="skeleton skeleton-text" />
        <div className="skeleton skeleton-text" style={{ width: '80%' }} />
        <div className="skeleton skeleton-text" style={{ width: '60%' }} />
      </div>
    </div>
  );
}
```

### Table Skeleton
```tsx
function TableSkeleton({ rows = 5, columns = 4 }) {
  return (
    <table className="table-skeleton">
      <thead>
        <tr>
          {Array.from({ length: columns }).map((_, i) => (
            <th key={i}>
              <div className="skeleton skeleton-text" />
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {Array.from({ length: rows }).map((_, rowIndex) => (
          <tr key={rowIndex}>
            {Array.from({ length: columns }).map((_, colIndex) => (
              <td key={colIndex}>
                <div
                  className="skeleton skeleton-text"
                  style={{ width: `${60 + Math.random() * 40}%` }}
                />
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

## Progress with Time Estimates

### Time Calculation
```typescript
class ProgressTimer {
  private startTime: number;
  private totalItems: number;
  private processedItems: number = 0;

  constructor(totalItems: number) {
    this.startTime = Date.now();
    this.totalItems = totalItems;
  }

  update(processedItems: number) {
    this.processedItems = processedItems;
  }

  getElapsedTime(): number {
    return Date.now() - this.startTime;
  }

  getEstimatedTimeRemaining(): number {
    if (this.processedItems === 0) return 0;

    const elapsedTime = this.getElapsedTime();
    const timePerItem = elapsedTime / this.processedItems;
    const remainingItems = this.totalItems - this.processedItems;

    return Math.round(timePerItem * remainingItems);
  }

  getFormattedTimeRemaining(): string {
    const ms = this.getEstimatedTimeRemaining();

    if (ms < 1000) return 'Less than a second';
    if (ms < 60000) return `${Math.round(ms / 1000)} seconds`;
    if (ms < 3600000) return `${Math.round(ms / 60000)} minutes`;

    return `${Math.round(ms / 3600000)} hours`;
  }
}
```

### Progress with Time Display
```tsx
function ProgressWithTime({ current, total, startTime }) {
  const [timeRemaining, setTimeRemaining] = useState('Calculating...');

  useEffect(() => {
    const elapsed = Date.now() - startTime;
    const rate = current / elapsed;
    const remaining = (total - current) / rate;

    setTimeRemaining(formatTime(remaining));
  }, [current, total, startTime]);

  const percentage = (current / total) * 100;

  return (
    <div className="progress-with-time">
      <div className="progress-header">
        <span>{Math.round(percentage)}% Complete</span>
        <span>{timeRemaining} remaining</span>
      </div>
      <div className="progress-track">
        <div
          className="progress-bar"
          style={{ width: `${percentage}%` }}
        />
      </div>
      <div className="progress-footer">
        <span>{current} of {total} items</span>
      </div>
    </div>
  );
}
```

## File Upload Progress

### Upload with Progress
```tsx
function FileUploadProgress({ file, onComplete, onError }) {
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState<'uploading' | 'complete' | 'error'>('uploading');

  useEffect(() => {
    const xhr = new XMLHttpRequest();

    xhr.upload.addEventListener('progress', (e) => {
      if (e.lengthComputable) {
        const percentComplete = (e.loaded / e.total) * 100;
        setProgress(percentComplete);
      }
    });

    xhr.addEventListener('load', () => {
      if (xhr.status === 200) {
        setStatus('complete');
        onComplete?.(xhr.response);
      } else {
        setStatus('error');
        onError?.(new Error('Upload failed'));
      }
    });

    xhr.addEventListener('error', () => {
      setStatus('error');
      onError?.(new Error('Network error'));
    });

    const formData = new FormData();
    formData.append('file', file);

    xhr.open('POST', '/api/upload');
    xhr.send(formData);

    return () => xhr.abort();
  }, [file]);

  return (
    <div className="upload-progress">
      <div className="upload-info">
        <FileIcon />
        <div className="upload-details">
          <div className="upload-name">{file.name}</div>
          <div className="upload-size">
            {formatFileSize(file.size)} - {Math.round(progress)}%
          </div>
        </div>
      </div>

      <div className="progress-track">
        <div
          className="progress-bar"
          style={{ width: `${progress}%` }}
        />
      </div>

      {status === 'error' && (
        <div className="upload-error">
          Upload failed. <button>Retry</button>
        </div>
      )}
    </div>
  );
}
```

### Multi-file Upload Queue
```tsx
function MultiFileUpload({ files }) {
  const [uploads, setUploads] = useState(
    files.map(file => ({
      id: file.name,
      file,
      progress: 0,
      status: 'pending'
    }))
  );

  const uploadFile = async (upload) => {
    setUploads(prev =>
      prev.map(u =>
        u.id === upload.id ? { ...u, status: 'uploading' } : u
      )
    );

    // Simulate upload with progress updates
    for (let i = 0; i <= 100; i += 10) {
      await new Promise(resolve => setTimeout(resolve, 200));

      setUploads(prev =>
        prev.map(u =>
          u.id === upload.id ? { ...u, progress: i } : u
        )
      );
    }

    setUploads(prev =>
      prev.map(u =>
        u.id === upload.id ? { ...u, status: 'complete' } : u
      )
    );
  };

  const totalProgress = uploads.reduce((sum, u) => sum + u.progress, 0) / uploads.length;

  return (
    <div className="multi-upload">
      <div className="upload-summary">
        <h3>Uploading {uploads.length} files</h3>
        <div className="total-progress">
          <div
            className="progress-bar"
            style={{ width: `${totalProgress}%` }}
          />
        </div>
      </div>

      <div className="upload-list">
        {uploads.map(upload => (
          <FileUploadItem
            key={upload.id}
            upload={upload}
            onRetry={() => uploadFile(upload)}
          />
        ))}
      </div>
    </div>
  );
}
```

## Loading States for Different Components

### Button Loading State
```tsx
function LoadingButton({ loading, children, ...props }) {
  return (
    <button disabled={loading} {...props}>
      {loading && <Spinner className="button-spinner" />}
      <span className={loading ? 'button-text-loading' : ''}>
        {children}
      </span>
    </button>
  );
}
```

### Card Loading State
```tsx
function LoadingCard({ loading, children }) {
  if (loading) {
    return <CardSkeleton />;
  }

  return <div className="card">{children}</div>;
}
```

### Table Loading Overlay
```tsx
function TableWithLoading({ loading, data, columns }) {
  return (
    <div className="table-container">
      {loading && (
        <div className="table-loading-overlay">
          <Spinner size="large" />
          <div>Loading data...</div>
        </div>
      )}

      <table className={loading ? 'table-loading' : ''}>
        {/* Table content */}
      </table>
    </div>
  );
}
```

## Accessibility

### ARIA Attributes
```html
<!-- Determinate progress -->
<div
  role="progressbar"
  aria-valuenow="45"
  aria-valuemin="0"
  aria-valuemax="100"
  aria-label="Upload progress"
>
  45%
</div>

<!-- Indeterminate progress -->
<div
  role="progressbar"
  aria-label="Loading"
  aria-busy="true"
>
  Loading...
</div>

<!-- Live region for updates -->
<div aria-live="polite" aria-atomic="true">
  75% complete
</div>
```

### Screen Reader Support
```tsx
function AccessibleProgress({ value, max, label }) {
  const percentage = Math.round((value / max) * 100);

  return (
    <>
      <div
        role="progressbar"
        aria-valuenow={value}
        aria-valuemin={0}
        aria-valuemax={max}
        aria-label={label}
      >
        <div className="progress-visual">
          {/* Visual progress bar */}
        </div>
      </div>

      {/* Screen reader announcements */}
      <div className="sr-only" aria-live="polite" aria-atomic="true">
        {percentage}% complete
      </div>
    </>
  );
}
```

## Best Practices

1. **Show immediately**: Display within 100ms for perceived performance
2. **Use appropriate type**: Spinner for unknown, bar for known duration
3. **Provide context**: Always include descriptive text
4. **Show time estimates**: For operations > 5 seconds
5. **Allow cancellation**: For operations > 30 seconds
6. **Smooth animations**: Use CSS transitions for progress updates
7. **Avoid layout shift**: Reserve space for progress indicators
8. **Mobile optimization**: Ensure touch-friendly cancel buttons
9. **Error recovery**: Provide retry options on failure
10. **Accessibility**: Include proper ARIA attributes and announcements