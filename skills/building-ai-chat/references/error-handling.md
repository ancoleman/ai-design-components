# AI-Specific Error Handling Patterns

## Table of Contents

- [Refusal Handling](#refusal-handling)
- [Hallucination Mitigation](#hallucination-mitigation)
- [Rate Limiting](#rate-limiting)
- [Context Limit Errors](#context-limit-errors)
- [Network & Connection Issues](#network--connection-issues)
- [Model Availability](#model-availability)
- [Timeout Handling](#timeout-handling)
- [Graceful Degradation](#graceful-degradation)

## Refusal Handling

### Clear Refusal Communication

Explain why AI cannot help with specific requests:

```tsx
interface RefusalResponse {
  type: 'refusal';
  reason: 'safety' | 'capability' | 'policy' | 'unclear' | 'out-of-scope';
  message: string;
  suggestion?: string;
  alternatives?: string[];
  learnMoreUrl?: string;
}

function RefusalMessage({ refusal }: { refusal: RefusalResponse }) {
  const getRefusalIcon = () => {
    switch (refusal.reason) {
      case 'safety': return <ShieldIcon />;
      case 'capability': return <InfoIcon />;
      case 'policy': return <PolicyIcon />;
      case 'unclear': return <QuestionIcon />;
      case 'out-of-scope': return <BoundaryIcon />;
      default: return <InfoIcon />;
    }
  };

  const getRefusalExplanation = () => {
    switch (refusal.reason) {
      case 'safety':
        return "This request could lead to harmful outcomes.";
      case 'capability':
        return "I don't have the ability to complete this task.";
      case 'policy':
        return "This violates usage policies.";
      case 'unclear':
        return "I need more information to help with this.";
      case 'out-of-scope':
        return "This is outside my area of expertise.";
      default:
        return "I cannot help with this request.";
    }
  };

  return (
    <div className={`refusal-message ${refusal.reason}`}>
      <div className="refusal-header">
        {getRefusalIcon()}
        <h4>Unable to Complete Request</h4>
      </div>

      <div className="refusal-content">
        <p className="refusal-main">
          {refusal.message || getRefusalExplanation()}
        </p>

        {refusal.suggestion && (
          <div className="refusal-suggestion">
            <h5>Try this instead:</h5>
            <p>{refusal.suggestion}</p>
          </div>
        )}

        {refusal.alternatives && refusal.alternatives.length > 0 && (
          <div className="refusal-alternatives">
            <h5>Alternative approaches:</h5>
            <ul>
              {refusal.alternatives.map((alt, i) => (
                <li key={i}>{alt}</li>
              ))}
            </ul>
          </div>
        )}

        {refusal.learnMoreUrl && (
          <a
            href={refusal.learnMoreUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="learn-more-link"
          >
            Learn more about our usage policies →
          </a>
        )}
      </div>

      <details className="refusal-details">
        <summary>Why do refusals happen?</summary>
        <p>
          AI assistants have safety guidelines to ensure helpful, harmless, and honest interactions.
          Refusals protect both users and the AI from potential misuse or errors.
        </p>
      </details>
    </div>
  );
}
```

### Soft Refusals with Guidance

Help users rephrase problematic requests:

```tsx
function SoftRefusal({ originalRequest, issue }) {
  const [showRephraseHelper, setShowRephraseHelper] = useState(false);
  const [rephrasedRequest, setRephrasedRequest] = useState('');

  const rephraseExamples = {
    'too-broad': {
      original: "Tell me everything about programming",
      better: "What are the key concepts I should learn as a beginner programmer?"
    },
    'inappropriate': {
      original: "Help me hack into a system",
      better: "How can I learn about cybersecurity ethically?"
    },
    'unclear': {
      original: "Fix it",
      better: "Can you help me debug this JavaScript function that's returning undefined?"
    }
  };

  return (
    <div className="soft-refusal">
      <div className="refusal-message">
        <WarningIcon />
        <p>
          I notice your request might be {issue}.
          Let me help you rephrase it in a way I can assist with.
        </p>
      </div>

      <button
        onClick={() => setShowRephraseHelper(!showRephraseHelper)}
        className="rephrase-btn"
      >
        Help me rephrase
      </button>

      {showRephraseHelper && (
        <div className="rephrase-helper">
          <h4>Rephrase Your Request</h4>

          {rephraseExamples[issue] && (
            <div className="rephrase-example">
              <div className="example-bad">
                <span className="label">Instead of:</span>
                <p>{rephraseExamples[issue].original}</p>
              </div>
              <div className="example-good">
                <span className="label">Try:</span>
                <p>{rephraseExamples[issue].better}</p>
              </div>
            </div>
          )}

          <textarea
            value={rephrasedRequest}
            onChange={(e) => setRephrasedRequest(e.target.value)}
            placeholder="Type your rephrased request here..."
            rows={3}
          />

          <button
            onClick={() => submitRephrased(rephrasedRequest)}
            disabled={!rephrasedRequest.trim()}
          >
            Submit Rephrased Request
          </button>
        </div>
      )}
    </div>
  );
}
```

## Hallucination Mitigation

### Uncertainty Indicators

Show when AI might be less confident:

```tsx
function UncertaintyIndicator({ confidence, message }) {
  if (confidence > 0.8) return null;

  const getUncertaintyLevel = () => {
    if (confidence < 0.3) return 'high';
    if (confidence < 0.6) return 'medium';
    return 'low';
  };

  const level = getUncertaintyLevel();

  return (
    <div className={`uncertainty-indicator ${level}`}>
      <div className="uncertainty-header">
        <WarningIcon />
        <span>
          {level === 'high' && 'Low confidence response'}
          {level === 'medium' && 'Moderate confidence'}
          {level === 'low' && 'Some uncertainty'}
        </span>
      </div>

      <div className="uncertainty-actions">
        <button className="verify-btn">
          <SearchIcon /> Verify with search
        </button>
        <button className="sources-btn">
          <BookIcon /> Request sources
        </button>
      </div>

      {level === 'high' && (
        <div className="uncertainty-warning">
          <p>
            This response may contain inaccuracies. Please verify important information
            from authoritative sources before using it.
          </p>
        </div>
      )}
    </div>
  );
}
```

### Citation Requests

Enable users to request sources:

```tsx
function CitationSupport({ message, onRequestCitations }) {
  const [citations, setCitations] = useState([]);
  const [loading, setLoading] = useState(false);

  const requestCitations = async () => {
    setLoading(true);
    try {
      const sources = await onRequestCitations(message.id);
      setCitations(sources);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="citation-support">
      {citations.length === 0 && (
        <button
          onClick={requestCitations}
          disabled={loading}
          className="request-citations-btn"
        >
          {loading ? (
            <>
              <Spinner size="small" />
              Finding sources...
            </>
          ) : (
            <>
              <CitationIcon />
              Add citations
            </>
          )}
        </button>
      )}

      {citations.length > 0 && (
        <div className="citations-list">
          <h5>Sources:</h5>
          {citations.map((citation, i) => (
            <div key={i} className="citation">
              <span className="citation-number">[{i + 1}]</span>
              <a
                href={citation.url}
                target="_blank"
                rel="noopener noreferrer"
                className="citation-link"
              >
                {citation.title}
              </a>
              <span className="citation-domain">
                ({new URL(citation.url).hostname})
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

## Rate Limiting

### Clear Rate Limit Communication

Show remaining capacity and wait times:

```tsx
function RateLimitHandler({ error, limits }) {
  const [timeRemaining, setTimeRemaining] = useState(error.retryAfter);
  const [queued, setQueued] = useState(false);

  useEffect(() => {
    if (timeRemaining <= 0) return;

    const timer = setInterval(() => {
      setTimeRemaining(prev => {
        if (prev <= 1) {
          clearInterval(timer);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [timeRemaining]);

  const queueMessage = () => {
    setQueued(true);
    // Message will be sent automatically when rate limit resets
  };

  return (
    <div className="rate-limit-handler">
      <div className="rate-limit-header">
        <ClockIcon />
        <h4>Rate Limit Reached</h4>
      </div>

      <div className="rate-limit-content">
        <p>You've reached the maximum number of requests.</p>

        <div className="limit-details">
          <div className="limit-item">
            <span className="label">Limit:</span>
            <span className="value">{limits.max} messages per {limits.window}</span>
          </div>
          <div className="limit-item">
            <span className="label">Used:</span>
            <span className="value">{limits.used} / {limits.max}</span>
          </div>
          <div className="limit-item">
            <span className="label">Resets in:</span>
            <span className="value countdown">
              {formatDuration(timeRemaining)}
            </span>
          </div>
        </div>

        <div className="rate-limit-progress">
          <div
            className="progress-fill"
            style={{ width: `${(limits.used / limits.max) * 100}%` }}
          />
        </div>

        {!queued ? (
          <div className="rate-limit-actions">
            <button onClick={queueMessage} className="queue-btn">
              Queue message for later
            </button>
            <button className="upgrade-btn">
              Upgrade for higher limits
            </button>
          </div>
        ) : (
          <div className="queue-status">
            <CheckIcon />
            <span>Message queued - will send in {formatDuration(timeRemaining)}</span>
          </div>
        )}
      </div>

      <details className="rate-limit-faq">
        <summary>Why do rate limits exist?</summary>
        <ul>
          <li>Ensure fair access for all users</li>
          <li>Prevent abuse and maintain service quality</li>
          <li>Manage computational resources efficiently</li>
        </ul>
      </details>
    </div>
  );
}
```

## Context Limit Errors

### Context Overflow Handling

When conversation exceeds token limits:

```tsx
function ContextLimitError({ currentTokens, maxTokens, onResolve }) {
  const [resolution, setResolution] = useState<'summarize' | 'new' | 'export'>('summarize');
  const [isResolving, setIsResolving] = useState(false);

  const handleResolve = async () => {
    setIsResolving(true);
    try {
      await onResolve(resolution);
    } finally {
      setIsResolving(false);
    }
  };

  const overflow = currentTokens - maxTokens;
  const percentageOver = ((overflow / maxTokens) * 100).toFixed(1);

  return (
    <div className="context-limit-error">
      <div className="error-header critical">
        <AlertIcon />
        <h3>Conversation Too Long</h3>
      </div>

      <div className="error-content">
        <p>
          This conversation has exceeded the maximum context length by {percentageOver}%.
        </p>

        <div className="context-visualization">
          <div className="context-bar overflow">
            <div
              className="context-used"
              style={{ width: '100%' }}
            />
            <div
              className="context-overflow"
              style={{ width: `${percentageOver}%` }}
            />
          </div>
          <div className="context-labels">
            <span>0</span>
            <span className="max">Max: {maxTokens.toLocaleString()}</span>
            <span className="current">
              Current: {currentTokens.toLocaleString()}
            </span>
          </div>
        </div>

        <div className="resolution-options">
          <h4>How would you like to proceed?</h4>

          <label className="resolution-option">
            <input
              type="radio"
              value="summarize"
              checked={resolution === 'summarize'}
              onChange={(e) => setResolution(e.target.value as any)}
            />
            <div className="option-content">
              <h5>Summarize & Continue</h5>
              <p>Compress earlier messages while keeping recent context</p>
            </div>
          </label>

          <label className="resolution-option">
            <input
              type="radio"
              value="new"
              checked={resolution === 'new'}
              onChange={(e) => setResolution(e.target.value as any)}
            />
            <div className="option-content">
              <h5>Start Fresh</h5>
              <p>Begin a new conversation with clean context</p>
            </div>
          </label>

          <label className="resolution-option">
            <input
              type="radio"
              value="export"
              checked={resolution === 'export'}
              onChange={(e) => setResolution(e.target.value as any)}
            />
            <div className="option-content">
              <h5>Export & Continue</h5>
              <p>Save this conversation and start a continuation</p>
            </div>
          </label>
        </div>

        <button
          onClick={handleResolve}
          disabled={isResolving}
          className="resolve-btn primary"
        >
          {isResolving ? (
            <>
              <Spinner size="small" />
              Processing...
            </>
          ) : (
            <>Continue with {resolution}</>
          )}
        </button>
      </div>
    </div>
  );
}
```

## Network & Connection Issues

### Connection Error Handling

Handle various network failures:

```tsx
function NetworkErrorHandler({ error, onRetry }) {
  const [retryCount, setRetryCount] = useState(0);
  const [isRetrying, setIsRetrying] = useState(false);
  const maxRetries = 3;

  const getErrorMessage = () => {
    if (error.code === 'NETWORK_ERROR') {
      return "Unable to connect to the AI service. Please check your internet connection.";
    }
    if (error.code === 'TIMEOUT') {
      return "The request took too long. The AI service might be experiencing high load.";
    }
    if (error.code === 'SERVER_ERROR') {
      return "The AI service encountered an error. This is usually temporary.";
    }
    return "An unexpected error occurred while connecting to the AI service.";
  };

  const retry = async () => {
    setIsRetrying(true);
    setRetryCount(prev => prev + 1);

    try {
      await onRetry();
    } catch (err) {
      if (retryCount < maxRetries - 1) {
        // Exponential backoff
        const delay = Math.pow(2, retryCount) * 1000;
        setTimeout(retry, delay);
      }
    } finally {
      setIsRetrying(false);
    }
  };

  return (
    <div className="network-error">
      <div className="error-icon">
        <WifiOffIcon />
      </div>

      <h3>Connection Problem</h3>
      <p>{getErrorMessage()}</p>

      {error.details && (
        <details className="error-details">
          <summary>Technical details</summary>
          <pre>{JSON.stringify(error.details, null, 2)}</pre>
        </details>
      )}

      <div className="error-actions">
        {retryCount < maxRetries ? (
          <button
            onClick={retry}
            disabled={isRetrying}
            className="retry-btn"
          >
            {isRetrying ? (
              <>
                <Spinner size="small" />
                Retrying... ({retryCount + 1}/{maxRetries})
              </>
            ) : (
              <>
                <RefreshIcon />
                Try Again
              </>
            )}
          </button>
        ) : (
          <div className="max-retries-reached">
            <p>Maximum retry attempts reached.</p>
            <button onClick={() => window.location.reload()}>
              Reload Page
            </button>
          </div>
        )}

        <button className="status-btn">
          Check Service Status
        </button>
      </div>

      <div className="connection-tips">
        <h4>Troubleshooting tips:</h4>
        <ul>
          <li>Check your internet connection</li>
          <li>Try refreshing the page</li>
          <li>Disable VPN or proxy if using one</li>
          <li>Clear browser cache and cookies</li>
        </ul>
      </div>
    </div>
  );
}
```

### Offline Mode

Handle offline scenarios gracefully:

```tsx
function OfflineMode({ isOnline, pendingMessages, onReconnect }) {
  const [showQueue, setShowQueue] = useState(false);

  return (
    <div className={`offline-mode ${!isOnline ? 'active' : ''}`}>
      {!isOnline && (
        <div className="offline-banner">
          <OfflineIcon />
          <span>You're offline</span>
          {pendingMessages.length > 0 && (
            <button onClick={() => setShowQueue(!showQueue)}>
              {pendingMessages.length} queued messages
            </button>
          )}
        </div>
      )}

      {showQueue && (
        <div className="message-queue">
          <h4>Queued Messages</h4>
          <p>These messages will be sent when you're back online</p>

          {pendingMessages.map((msg, i) => (
            <div key={i} className="queued-message">
              <span className="queue-number">{i + 1}</span>
              <div className="message-preview">
                {msg.content.substring(0, 100)}...
              </div>
              <button onClick={() => removeFromQueue(msg.id)}>
                <CloseIcon />
              </button>
            </div>
          ))}
        </div>
      )}

      <div className="offline-capabilities">
        <h4>Available Offline:</h4>
        <ul>
          <li>✓ View conversation history</li>
          <li>✓ Search past messages</li>
          <li>✓ Export conversations</li>
          <li>✓ Queue messages for later</li>
          <li>✗ Get AI responses</li>
          <li>✗ Real-time features</li>
        </ul>
      </div>
    </div>
  );
}
```

## Model Availability

### Model Selection with Fallback

Handle model unavailability:

```tsx
function ModelSelector({ preferredModel, availableModels, onModelChange }) {
  const [selectedModel, setSelectedModel] = useState(preferredModel);
  const [showUnavailable, setShowUnavailable] = useState(false);

  const allModels = [
    { id: 'gpt-4', name: 'GPT-4', status: 'available', speed: 'slow', quality: 'best' },
    { id: 'gpt-3.5', name: 'GPT-3.5', status: 'available', speed: 'fast', quality: 'good' },
    { id: 'claude-3', name: 'Claude 3', status: 'unavailable', speed: 'medium', quality: 'best' },
  ];

  const handleModelSelect = (modelId: string) => {
    const model = allModels.find(m => m.id === modelId);

    if (model?.status === 'unavailable') {
      showModelUnavailableError(model);
      return;
    }

    setSelectedModel(modelId);
    onModelChange(modelId);
  };

  return (
    <div className="model-selector">
      <div className="model-header">
        <h4>AI Model</h4>
        <button onClick={() => setShowUnavailable(!showUnavailable)}>
          {showUnavailable ? 'Hide' : 'Show'} unavailable
        </button>
      </div>

      <div className="model-grid">
        {allModels
          .filter(m => showUnavailable || m.status === 'available')
          .map(model => (
            <button
              key={model.id}
              className={`model-option ${selectedModel === model.id ? 'selected' : ''} ${model.status}`}
              onClick={() => handleModelSelect(model.id)}
              disabled={model.status === 'unavailable'}
            >
              <div className="model-name">{model.name}</div>
              <div className="model-badges">
                <span className={`speed-badge ${model.speed}`}>
                  {model.speed}
                </span>
                <span className={`quality-badge ${model.quality}`}>
                  {model.quality}
                </span>
              </div>
              {model.status === 'unavailable' && (
                <div className="unavailable-overlay">
                  <LockIcon />
                  <span>Unavailable</span>
                </div>
              )}
            </button>
          ))}
      </div>

      {selectedModel !== preferredModel && (
        <div className="fallback-notice">
          <InfoIcon />
          <span>
            Using {selectedModel} because {preferredModel} is unavailable
          </span>
        </div>
      )}
    </div>
  );
}
```

## Timeout Handling

### Request Timeout Management

Handle long-running requests:

```tsx
function TimeoutHandler({ request, timeout = 30000, onCancel, onExtend }) {
  const [timeElapsed, setTimeElapsed] = useState(0);
  const [status, setStatus] = useState<'running' | 'warning' | 'timeout'>('running');

  useEffect(() => {
    const interval = setInterval(() => {
      setTimeElapsed(prev => {
        const next = prev + 100;

        if (next >= timeout * 2) {
          setStatus('timeout');
        } else if (next >= timeout) {
          setStatus('warning');
        }

        return next;
      });
    }, 100);

    return () => clearInterval(interval);
  }, [timeout]);

  const percentage = Math.min((timeElapsed / timeout) * 100, 100);

  if (status === 'timeout') {
    return (
      <div className="timeout-error">
        <div className="timeout-header">
          <TimeoutIcon />
          <h3>Request Timed Out</h3>
        </div>

        <p>This request is taking much longer than expected.</p>

        <div className="timeout-actions">
          <button onClick={() => onExtend(30000)} className="extend-btn">
            Wait 30 more seconds
          </button>
          <button onClick={onCancel} className="cancel-btn">
            Cancel request
          </button>
        </div>

        <details className="timeout-reasons">
          <summary>Why did this happen?</summary>
          <ul>
            <li>Complex request requiring more processing</li>
            <li>High server load</li>
            <li>Network congestion</li>
            <li>Large context to process</li>
          </ul>
        </details>
      </div>
    );
  }

  return (
    <div className={`timeout-handler ${status}`}>
      {status === 'warning' && (
        <div className="timeout-warning">
          <WarningIcon />
          <span>This is taking longer than usual...</span>
          <button onClick={() => onExtend(30000)}>
            Keep waiting
          </button>
          <button onClick={onCancel}>
            Cancel
          </button>
        </div>
      )}

      <div className="timeout-progress">
        <div
          className="progress-bar"
          style={{ width: `${percentage}%` }}
        />
      </div>

      <div className="timeout-info">
        <span>Processing for {(timeElapsed / 1000).toFixed(1)}s</span>
      </div>
    </div>
  );
}
```

## Graceful Degradation

### Feature Degradation Strategy

Maintain functionality during partial failures:

```tsx
function DegradedModeHandler({ degradedFeatures, onDismiss }) {
  const getDegradationMessage = (feature: string) => {
    const messages = {
      'streaming': 'Live streaming is unavailable. Responses will appear all at once.',
      'attachments': 'File attachments are temporarily disabled.',
      'voice': 'Voice input/output is currently unavailable.',
      'history': 'Conversation history sync is paused.',
      'search': 'Message search is temporarily unavailable.',
      'export': 'Export functionality is limited.'
    };
    return messages[feature] || `${feature} is temporarily unavailable.`;
  };

  if (degradedFeatures.length === 0) return null;

  return (
    <div className="degraded-mode-banner">
      <div className="degraded-header">
        <WarningIcon />
        <span>Limited Functionality</span>
        <button onClick={onDismiss} aria-label="Dismiss">×</button>
      </div>

      <div className="degraded-features">
        {degradedFeatures.map(feature => (
          <div key={feature} className="degraded-feature">
            <span className="feature-status">⚠️</span>
            <span className="feature-message">
              {getDegradationMessage(feature)}
            </span>
          </div>
        ))}
      </div>

      <details className="degraded-details">
        <summary>What can I still do?</summary>
        <ul>
          <li>✓ Send and receive messages</li>
          <li>✓ View current conversation</li>
          <li>✓ Copy responses</li>
          <li>✓ Basic chat functionality</li>
        </ul>
      </details>
    </div>
  );
}
```

### Error Recovery Suggestions

Provide actionable recovery steps:

```tsx
function ErrorRecovery({ error, onAction }) {
  const getRecoverySuggestions = () => {
    const suggestions = [];

    if (error.type === 'context_limit') {
      suggestions.push({
        action: 'summarize',
        label: 'Summarize conversation',
        description: 'Compress earlier messages to free up space'
      });
    }

    if (error.type === 'rate_limit') {
      suggestions.push({
        action: 'wait',
        label: 'Wait and retry',
        description: `Try again in ${error.retryAfter} seconds`
      });
    }

    if (error.type === 'network') {
      suggestions.push({
        action: 'retry',
        label: 'Retry request',
        description: 'Try sending the request again'
      });
    }

    suggestions.push({
      action: 'new_conversation',
      label: 'Start fresh',
      description: 'Begin a new conversation'
    });

    return suggestions;
  };

  return (
    <div className="error-recovery">
      <h4>Suggested Actions</h4>

      <div className="recovery-options">
        {getRecoverySuggestions().map((suggestion, i) => (
          <button
            key={i}
            onClick={() => onAction(suggestion.action)}
            className="recovery-option"
          >
            <div className="option-label">{suggestion.label}</div>
            <div className="option-description">{suggestion.description}</div>
          </button>
        ))}
      </div>

      <div className="recovery-help">
        <button className="help-link">
          <HelpIcon /> Get help with this error
        </button>
        <button className="report-link">
          <FlagIcon /> Report this issue
        </button>
      </div>
    </div>
  );
}
```

## Best Practices Summary

1. **Clear communication** - Explain errors in user-friendly terms
2. **Actionable solutions** - Always provide next steps
3. **Graceful degradation** - Maintain core functionality
4. **Automatic retry** - With exponential backoff
5. **Offline support** - Queue messages when disconnected
6. **Uncertainty signals** - Show when AI might be wrong
7. **Educate users** - Explain why errors occur
8. **Progressive disclosure** - Technical details in expandable sections
9. **Recovery paths** - Multiple ways to resolve issues
10. **Maintain trust** - Acknowledge limitations honestly