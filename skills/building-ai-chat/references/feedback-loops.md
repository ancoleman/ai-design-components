# Feedback & Improvement Loop Patterns

## Table of Contents

- [Simple Feedback Mechanisms](#simple-feedback-mechanisms)
- [Regeneration Patterns](#regeneration-patterns)
- [Message Editing](#message-editing)
- [Detailed Feedback Collection](#detailed-feedback-collection)
- [RLHF Integration](#rlhf-integration)
- [Quality Metrics](#quality-metrics)
- [A/B Testing Responses](#ab-testing-responses)

## Simple Feedback Mechanisms

### Thumbs Up/Down Implementation

Quick, frictionless feedback collection:

```tsx
interface FeedbackData {
  messageId: string;
  conversationId: string;
  feedback: 'positive' | 'negative' | null;
  timestamp: Date;
  metadata?: {
    responseTime?: number;
    tokenCount?: number;
    model?: string;
  };
}

function SimpleFeedback({ message, onFeedback }) {
  const [feedback, setFeedback] = useState<'positive' | 'negative' | null>(null);
  const [showThankYou, setShowThankYou] = useState(false);

  const handleFeedback = async (type: 'positive' | 'negative') => {
    // Toggle if clicking same button
    const newFeedback = feedback === type ? null : type;
    setFeedback(newFeedback);

    // Send feedback to backend
    const feedbackData: FeedbackData = {
      messageId: message.id,
      conversationId: message.conversationId,
      feedback: newFeedback,
      timestamp: new Date(),
      metadata: {
        responseTime: message.responseTime,
        tokenCount: message.tokenCount,
        model: message.model
      }
    };

    await onFeedback(feedbackData);

    // Show thank you message
    if (newFeedback) {
      setShowThankYou(true);
      setTimeout(() => setShowThankYou(false), 2000);
    }
  };

  return (
    <div className="simple-feedback">
      <button
        className={`feedback-btn ${feedback === 'positive' ? 'selected' : ''}`}
        onClick={() => handleFeedback('positive')}
        aria-label="Good response"
        title="This was helpful"
      >
        <ThumbsUpIcon />
        {feedback === 'positive' && <span className="count">Thanks!</span>}
      </button>

      <button
        className={`feedback-btn ${feedback === 'negative' ? 'selected' : ''}`}
        onClick={() => handleFeedback('negative')}
        aria-label="Bad response"
        title="This wasn't helpful"
      >
        <ThumbsDownIcon />
      </button>

      {showThankYou && (
        <div className="thank-you-toast">
          Thank you for your feedback!
        </div>
      )}
    </div>
  );
}
```

### Copy and Share Actions

Enable users to save and share useful responses:

```tsx
function ResponseActions({ message }) {
  const [copied, setCopied] = useState(false);
  const [shareUrl, setShareUrl] = useState<string | null>(null);

  const copyToClipboard = async () => {
    try {
      // Copy as markdown
      await navigator.clipboard.writeText(message.content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      // Fallback for older browsers
      const textarea = document.createElement('textarea');
      textarea.value = message.content;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const copyAsJSON = async () => {
    const jsonData = {
      role: message.role,
      content: message.content,
      timestamp: message.timestamp,
      model: message.model
    };

    await navigator.clipboard.writeText(JSON.stringify(jsonData, null, 2));
  };

  const shareMessage = async () => {
    // Create shareable link
    const shareData = {
      messageId: message.id,
      conversationId: message.conversationId
    };

    try {
      const response = await createShareableLink(shareData);
      setShareUrl(response.url);

      // Use Web Share API if available
      if (navigator.share) {
        await navigator.share({
          title: 'AI Response',
          text: message.content.substring(0, 100) + '...',
          url: response.url
        });
      }
    } catch (error) {
      console.error('Share failed:', error);
    }
  };

  return (
    <div className="response-actions">
      <div className="action-group">
        <button onClick={copyToClipboard} className="copy-btn">
          {copied ? <CheckIcon /> : <CopyIcon />}
          {copied ? 'Copied!' : 'Copy'}
        </button>

        <Menu>
          <MenuButton>
            <ChevronDownIcon />
          </MenuButton>
          <MenuItems>
            <MenuItem onClick={copyAsJSON}>Copy as JSON</MenuItem>
            <MenuItem onClick={() => copyCode(message.content)}>
              Copy code blocks only
            </MenuItem>
            <MenuItem onClick={() => copyAsPlainText(message.content)}>
              Copy as plain text
            </MenuItem>
          </MenuItems>
        </Menu>
      </div>

      <button onClick={shareMessage} className="share-btn">
        <ShareIcon /> Share
      </button>

      {shareUrl && (
        <div className="share-dialog">
          <input
            type="text"
            value={shareUrl}
            readOnly
            onClick={(e) => e.currentTarget.select()}
          />
          <button onClick={() => navigator.clipboard.writeText(shareUrl)}>
            Copy Link
          </button>
        </div>
      )}
    </div>
  );
}
```

## Regeneration Patterns

### Basic Regeneration

Simple retry with same prompt:

```tsx
function RegenerationControl({ message, onRegenerate }) {
  const [isRegenerating, setIsRegenerating] = useState(false);
  const [regenerationCount, setRegenerationCount] = useState(0);

  const handleRegenerate = async () => {
    setIsRegenerating(true);
    setRegenerationCount(prev => prev + 1);

    try {
      await onRegenerate(message.id);
    } finally {
      setIsRegenerating(false);
    }
  };

  return (
    <div className="regeneration-control">
      <button
        onClick={handleRegenerate}
        disabled={isRegenerating}
        className="regenerate-btn"
      >
        {isRegenerating ? (
          <>
            <Spinner size="small" />
            Regenerating...
          </>
        ) : (
          <>
            <RefreshIcon />
            Regenerate
            {regenerationCount > 0 && (
              <span className="count">({regenerationCount})</span>
            )}
          </>
        )}
      </button>

      {regenerationCount > 2 && (
        <div className="regeneration-hint">
          <InfoIcon />
          <span>
            Try editing your prompt for better results
          </span>
        </div>
      )}
    </div>
  );
}
```

### Advanced Regeneration with Options

Regenerate with modified parameters:

```tsx
function AdvancedRegeneration({ message, onRegenerate }) {
  const [showOptions, setShowOptions] = useState(false);
  const [options, setOptions] = useState({
    temperature: 0.7,
    model: message.model || 'default',
    style: 'balanced',
    length: 'auto'
  });

  const regenerateWithOptions = async () => {
    await onRegenerate(message.id, {
      ...options,
      originalPrompt: message.prompt,
      feedback: 'User requested regeneration with modified parameters'
    });

    setShowOptions(false);
  };

  return (
    <div className="advanced-regeneration">
      <button
        onClick={() => setShowOptions(!showOptions)}
        className="regenerate-advanced-btn"
      >
        <SettingsIcon />
        Regenerate with options
      </button>

      {showOptions && (
        <div className="regeneration-options">
          <div className="option-group">
            <label>Creativity:</label>
            <input
              type="range"
              min="0"
              max="1"
              step="0.1"
              value={options.temperature}
              onChange={(e) => setOptions({
                ...options,
                temperature: parseFloat(e.target.value)
              })}
            />
            <span>{options.temperature}</span>
          </div>

          <div className="option-group">
            <label>Style:</label>
            <select
              value={options.style}
              onChange={(e) => setOptions({ ...options, style: e.target.value })}
            >
              <option value="concise">Concise</option>
              <option value="balanced">Balanced</option>
              <option value="detailed">Detailed</option>
              <option value="creative">Creative</option>
              <option value="formal">Formal</option>
              <option value="casual">Casual</option>
            </select>
          </div>

          <div className="option-group">
            <label>Length:</label>
            <select
              value={options.length}
              onChange={(e) => setOptions({ ...options, length: e.target.value })}
            >
              <option value="auto">Auto</option>
              <option value="short">Short</option>
              <option value="medium">Medium</option>
              <option value="long">Long</option>
            </select>
          </div>

          <div className="option-group">
            <label>Model:</label>
            <select
              value={options.model}
              onChange={(e) => setOptions({ ...options, model: e.target.value })}
            >
              <option value="gpt-4">GPT-4</option>
              <option value="gpt-3.5">GPT-3.5</option>
              <option value="claude-3">Claude 3</option>
            </select>
          </div>

          <div className="option-actions">
            <button onClick={regenerateWithOptions} className="primary">
              Regenerate with these settings
            </button>
            <button onClick={() => setShowOptions(false)}>
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
```

### Version Comparison

Compare multiple regenerations:

```tsx
function ResponseVersions({ versions, currentVersion, onSelectVersion }) {
  const [comparisonMode, setComparisonMode] = useState<'single' | 'side-by-side'>('single');
  const [selectedVersions, setSelectedVersions] = useState<[number, number]>([0, 1]);

  return (
    <div className="response-versions">
      <div className="version-header">
        <h4>Response Versions ({versions.length})</h4>
        <div className="view-toggle">
          <button
            className={comparisonMode === 'single' ? 'active' : ''}
            onClick={() => setComparisonMode('single')}
          >
            Single
          </button>
          <button
            className={comparisonMode === 'side-by-side' ? 'active' : ''}
            onClick={() => setComparisonMode('side-by-side')}
          >
            Compare
          </button>
        </div>
      </div>

      {comparisonMode === 'single' ? (
        <div className="single-version">
          <div className="version-selector">
            {versions.map((version, index) => (
              <button
                key={version.id}
                className={`version-btn ${currentVersion === index ? 'active' : ''}`}
                onClick={() => onSelectVersion(index)}
              >
                v{index + 1}
                {version.feedback && (
                  <span className={`feedback-indicator ${version.feedback}`}>
                    {version.feedback === 'positive' ? '👍' : '👎'}
                  </span>
                )}
              </button>
            ))}
          </div>

          <div className="version-content">
            <Streamdown>{versions[currentVersion].content}</Streamdown>
            <div className="version-metadata">
              <span>Generated: {formatTime(versions[currentVersion].timestamp)}</span>
              {versions[currentVersion].model && (
                <span>Model: {versions[currentVersion].model}</span>
              )}
            </div>
          </div>
        </div>
      ) : (
        <div className="side-by-side-comparison">
          <div className="comparison-column">
            <select
              value={selectedVersions[0]}
              onChange={(e) => setSelectedVersions([
                parseInt(e.target.value),
                selectedVersions[1]
              ])}
            >
              {versions.map((v, i) => (
                <option key={i} value={i}>Version {i + 1}</option>
              ))}
            </select>
            <div className="version-content">
              <Streamdown>{versions[selectedVersions[0]].content}</Streamdown>
            </div>
          </div>

          <div className="comparison-column">
            <select
              value={selectedVersions[1]}
              onChange={(e) => setSelectedVersions([
                selectedVersions[0],
                parseInt(e.target.value)
              ])}
            >
              {versions.map((v, i) => (
                <option key={i} value={i}>Version {i + 1}</option>
              ))}
            </select>
            <div className="version-content">
              <Streamdown>{versions[selectedVersions[1]].content}</Streamdown>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
```

## Message Editing

### Edit and Resubmit

Allow users to modify their prompts:

```tsx
function EditableMessage({ message, onEdit, onResubmit }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedContent, setEditedContent] = useState(message.content);
  const [showDiff, setShowDiff] = useState(false);

  const handleSave = async () => {
    if (editedContent !== message.content) {
      await onEdit(message.id, editedContent);

      // Optionally resubmit for new response
      if (message.role === 'user') {
        const shouldResubmit = window.confirm(
          'Do you want to get a new response for the edited message?'
        );
        if (shouldResubmit) {
          await onResubmit(message.id, editedContent);
        }
      }
    }

    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditedContent(message.content);
    setIsEditing(false);
    setShowDiff(false);
  };

  return (
    <div className="editable-message">
      {!isEditing ? (
        <>
          <div className="message-content">
            <Streamdown>{message.content}</Streamdown>
          </div>
          <button
            onClick={() => setIsEditing(true)}
            className="edit-trigger"
            aria-label="Edit message"
          >
            <EditIcon />
          </button>
        </>
      ) : (
        <div className="edit-mode">
          <textarea
            value={editedContent}
            onChange={(e) => setEditedContent(e.target.value)}
            className="edit-textarea"
            rows={Math.max(5, editedContent.split('\n').length)}
          />

          {showDiff && (
            <div className="diff-preview">
              <DiffViewer
                oldValue={message.content}
                newValue={editedContent}
              />
            </div>
          )}

          <div className="edit-actions">
            <button onClick={handleSave} className="save-btn">
              <CheckIcon /> Save {message.role === 'user' && '& Resubmit'}
            </button>
            <button onClick={() => setShowDiff(!showDiff)}>
              <DiffIcon /> {showDiff ? 'Hide' : 'Show'} Changes
            </button>
            <button onClick={handleCancel} className="cancel-btn">
              Cancel
            </button>
          </div>
        </div>
      )}

      {message.edited && (
        <div className="edited-indicator">
          <EditIcon size="small" />
          Edited {formatRelativeTime(message.editedAt)}
        </div>
      )}
    </div>
  );
}
```

## Detailed Feedback Collection

### Structured Feedback Form

Collect specific improvement information:

```tsx
interface DetailedFeedback {
  messageId: string;
  overallRating: 'positive' | 'negative';
  issues: string[];
  customIssue?: string;
  suggestion?: string;
  wouldRecommend: boolean;
}

function DetailedFeedbackForm({ message, onSubmit, onClose }) {
  const [feedback, setFeedback] = useState<DetailedFeedback>({
    messageId: message.id,
    overallRating: 'negative',
    issues: [],
    wouldRecommend: false
  });

  const commonIssues = [
    { id: 'incorrect', label: 'Incorrect information' },
    { id: 'incomplete', label: 'Incomplete response' },
    { id: 'irrelevant', label: 'Not relevant to my question' },
    { id: 'confusing', label: 'Confusing or unclear' },
    { id: 'too-long', label: 'Too verbose' },
    { id: 'too-short', label: 'Too brief' },
    { id: 'tone', label: 'Inappropriate tone' },
    { id: 'refused', label: 'Refused when it shouldn\'t' },
    { id: 'hallucination', label: 'Made up information' }
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await onSubmit(feedback);
    onClose();
  };

  return (
    <form className="detailed-feedback-form" onSubmit={handleSubmit}>
      <h3>Help us improve</h3>
      <p>What went wrong with this response?</p>

      <div className="issue-checkboxes">
        {commonIssues.map(issue => (
          <label key={issue.id} className="issue-option">
            <input
              type="checkbox"
              checked={feedback.issues.includes(issue.id)}
              onChange={(e) => {
                if (e.target.checked) {
                  setFeedback({
                    ...feedback,
                    issues: [...feedback.issues, issue.id]
                  });
                } else {
                  setFeedback({
                    ...feedback,
                    issues: feedback.issues.filter(i => i !== issue.id)
                  });
                }
              }}
            />
            <span>{issue.label}</span>
          </label>
        ))}
      </div>

      <div className="custom-issue">
        <label>
          Other issue (optional):
          <input
            type="text"
            value={feedback.customIssue || ''}
            onChange={(e) => setFeedback({
              ...feedback,
              customIssue: e.target.value
            })}
            placeholder="Describe the issue..."
          />
        </label>
      </div>

      <div className="suggestion">
        <label>
          How could this response be better? (optional):
          <textarea
            value={feedback.suggestion || ''}
            onChange={(e) => setFeedback({
              ...feedback,
              suggestion: e.target.value
            })}
            placeholder="Your suggestion..."
            rows={3}
          />
        </label>
      </div>

      <div className="recommend">
        <label className="checkbox-label">
          <input
            type="checkbox"
            checked={feedback.wouldRecommend}
            onChange={(e) => setFeedback({
              ...feedback,
              wouldRecommend: e.target.checked
            })}
          />
          I would recommend this AI to others
        </label>
      </div>

      <div className="form-actions">
        <button type="submit" className="submit-btn">
          Submit Feedback
        </button>
        <button type="button" onClick={onClose} className="cancel-btn">
          Cancel
        </button>
      </div>
    </form>
  );
}
```

## RLHF Integration

### Preference Collection

Collect preferences for reinforcement learning:

```tsx
function PreferenceComparison({ optionA, optionB, onPreference }) {
  const [selected, setSelected] = useState<'A' | 'B' | null>(null);
  const [reason, setReason] = useState('');

  const submitPreference = async () => {
    if (!selected) return;

    const preference = {
      chosen: selected === 'A' ? optionA : optionB,
      rejected: selected === 'A' ? optionB : optionA,
      reason,
      timestamp: new Date(),
      metadata: {
        prompt: optionA.prompt, // Same prompt for both
        models: {
          A: optionA.model,
          B: optionB.model
        }
      }
    };

    await onPreference(preference);
  };

  return (
    <div className="preference-comparison">
      <h3>Which response is better?</h3>
      <p>Help train the AI by selecting the better response</p>

      <div className="comparison-options">
        <div
          className={`option option-a ${selected === 'A' ? 'selected' : ''}`}
          onClick={() => setSelected('A')}
        >
          <div className="option-header">
            <input
              type="radio"
              name="preference"
              checked={selected === 'A'}
              onChange={() => setSelected('A')}
            />
            <label>Response A</label>
          </div>
          <div className="option-content">
            <Streamdown>{optionA.content}</Streamdown>
          </div>
        </div>

        <div
          className={`option option-b ${selected === 'B' ? 'selected' : ''}`}
          onClick={() => setSelected('B')}
        >
          <div className="option-header">
            <input
              type="radio"
              name="preference"
              checked={selected === 'B'}
              onChange={() => setSelected('B')}
            />
            <label>Response B</label>
          </div>
          <div className="option-content">
            <Streamdown>{optionB.content}</Streamdown>
          </div>
        </div>
      </div>

      {selected && (
        <div className="reason-input">
          <label>
            Why is this response better? (optional)
            <select
              value={reason}
              onChange={(e) => setReason(e.target.value)}
            >
              <option value="">Select a reason...</option>
              <option value="more-accurate">More accurate</option>
              <option value="clearer">Clearer explanation</option>
              <option value="more-complete">More complete</option>
              <option value="better-format">Better formatting</option>
              <option value="more-relevant">More relevant</option>
              <option value="better-tone">Better tone</option>
              <option value="other">Other</option>
            </select>
          </label>
        </div>
      )}

      <div className="comparison-actions">
        <button
          onClick={submitPreference}
          disabled={!selected}
          className="submit-preference"
        >
          Submit Preference
        </button>
        <button className="skip-btn">
          Skip
        </button>
      </div>
    </div>
  );
}
```

## Quality Metrics

### Response Quality Dashboard

Track and display quality metrics:

```tsx
function QualityMetrics({ conversationId }) {
  const [metrics, setMetrics] = useState<any>(null);
  const [timeRange, setTimeRange] = useState<'day' | 'week' | 'month'>('week');

  useEffect(() => {
    loadMetrics(conversationId, timeRange).then(setMetrics);
  }, [conversationId, timeRange]);

  if (!metrics) return <Spinner />;

  return (
    <div className="quality-metrics">
      <div className="metrics-header">
        <h3>Response Quality</h3>
        <select
          value={timeRange}
          onChange={(e) => setTimeRange(e.target.value as any)}
        >
          <option value="day">Last 24 hours</option>
          <option value="week">Last 7 days</option>
          <option value="month">Last 30 days</option>
        </select>
      </div>

      <div className="metrics-grid">
        <MetricCard
          title="Satisfaction Rate"
          value={`${metrics.satisfactionRate}%`}
          change={metrics.satisfactionChange}
          icon={<ThumbsUpIcon />}
          color="green"
        />

        <MetricCard
          title="Regeneration Rate"
          value={`${metrics.regenerationRate}%`}
          change={metrics.regenerationChange}
          icon={<RefreshIcon />}
          color="orange"
          inverse // Lower is better
        />

        <MetricCard
          title="Edit Rate"
          value={`${metrics.editRate}%`}
          change={metrics.editChange}
          icon={<EditIcon />}
          color="blue"
          inverse
        />

        <MetricCard
          title="Avg Response Time"
          value={`${metrics.avgResponseTime}s`}
          change={metrics.responseTimeChange}
          icon={<ClockIcon />}
          color="purple"
          inverse
        />
      </div>

      <div className="quality-chart">
        <h4>Quality Trend</h4>
        <LineChart
          data={metrics.trend}
          lines={[
            { key: 'satisfaction', color: '#10b981', label: 'Satisfaction' },
            { key: 'accuracy', color: '#3b82f6', label: 'Accuracy' }
          ]}
        />
      </div>

      <div className="top-issues">
        <h4>Top Issues Reported</h4>
        <ul>
          {metrics.topIssues.map((issue, i) => (
            <li key={i}>
              <span className="issue-name">{issue.name}</span>
              <span className="issue-count">{issue.count} reports</span>
              <div className="issue-bar">
                <div
                  className="issue-fill"
                  style={{ width: `${issue.percentage}%` }}
                />
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

function MetricCard({ title, value, change, icon, color, inverse = false }) {
  const isPositive = inverse ? change < 0 : change > 0;

  return (
    <div className={`metric-card ${color}`}>
      <div className="metric-icon">{icon}</div>
      <div className="metric-content">
        <h4>{title}</h4>
        <div className="metric-value">{value}</div>
        {change !== undefined && (
          <div className={`metric-change ${isPositive ? 'positive' : 'negative'}`}>
            {isPositive ? <TrendUpIcon /> : <TrendDownIcon />}
            {Math.abs(change)}%
          </div>
        )}
      </div>
    </div>
  );
}
```

## A/B Testing Responses

### Experiment Framework

Test different response strategies:

```tsx
interface Experiment {
  id: string;
  name: string;
  variants: Array<{
    id: string;
    name: string;
    config: any;
    allocation: number; // Percentage
  }>;
  metrics: string[];
  status: 'active' | 'completed' | 'paused';
}

function ABTestingDashboard({ experiments, onCreateExperiment }) {
  const [selectedExperiment, setSelectedExperiment] = useState<Experiment | null>(null);

  return (
    <div className="ab-testing-dashboard">
      <div className="experiments-list">
        <h3>Active Experiments</h3>
        {experiments.map(exp => (
          <div
            key={exp.id}
            className={`experiment-card ${exp.status}`}
            onClick={() => setSelectedExperiment(exp)}
          >
            <h4>{exp.name}</h4>
            <div className="experiment-status">
              <StatusBadge status={exp.status} />
              <span>{exp.variants.length} variants</span>
            </div>
            <div className="experiment-metrics">
              {exp.metrics.map(metric => (
                <span key={metric} className="metric-tag">
                  {metric}
                </span>
              ))}
            </div>
          </div>
        ))}

        <button onClick={onCreateExperiment} className="create-experiment">
          <PlusIcon /> New Experiment
        </button>
      </div>

      {selectedExperiment && (
        <ExperimentResults experiment={selectedExperiment} />
      )}
    </div>
  );
}

function ExperimentResults({ experiment }) {
  const [results, setResults] = useState<any>(null);

  useEffect(() => {
    loadExperimentResults(experiment.id).then(setResults);
  }, [experiment.id]);

  if (!results) return <Spinner />;

  return (
    <div className="experiment-results">
      <h3>{experiment.name} Results</h3>

      <div className="variants-performance">
        {experiment.variants.map(variant => {
          const variantResults = results.variants[variant.id];
          return (
            <div key={variant.id} className="variant-card">
              <h4>{variant.name}</h4>
              <div className="variant-allocation">
                {variant.allocation}% of traffic
              </div>

              <div className="variant-metrics">
                {experiment.metrics.map(metric => (
                  <div key={metric} className="metric">
                    <span className="metric-name">{metric}:</span>
                    <span className="metric-value">
                      {variantResults[metric]}
                    </span>
                    {variantResults[`${metric}_significance`] && (
                      <span className="significance">
                        {variantResults[`${metric}_significance`] > 0.95 ? '✓' : ''}
                      </span>
                    )}
                  </div>
                ))}
              </div>

              {variantResults.winner && (
                <div className="winner-badge">
                  <TrophyIcon /> Winner
                </div>
              )}
            </div>
          );
        })}
      </div>

      <div className="experiment-chart">
        <h4>Performance Over Time</h4>
        <LineChart
          data={results.timeline}
          lines={experiment.variants.map(v => ({
            key: v.id,
            label: v.name,
            color: getVariantColor(v.id)
          }))}
        />
      </div>

      <div className="experiment-actions">
        <button className="declare-winner">
          Declare Winner
        </button>
        <button className="pause-experiment">
          Pause Experiment
        </button>
        <button className="export-results">
          Export Results
        </button>
      </div>
    </div>
  );
}
```

## Best Practices Summary

1. **Make feedback frictionless** - One-click thumbs up/down
2. **Thank users** - Acknowledge feedback immediately
3. **Allow regeneration** - Multiple attempts are normal
4. **Support editing** - Users refine prompts iteratively
5. **Collect detailed feedback optionally** - Don't force it
6. **Track quality metrics** - Monitor satisfaction trends
7. **Enable version comparison** - A/B testing for users
8. **Implement RLHF** - Continuous improvement from preferences
9. **Show impact** - Tell users how feedback helps
10. **Test systematically** - A/B test response strategies