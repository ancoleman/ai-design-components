# Tool Usage & Function Calling Visualization

## Table of Contents

- [Function Call Display](#function-call-display)
- [Code Execution](#code-execution)
- [Web Search Integration](#web-search-integration)
- [File Operations](#file-operations)
- [API Call Visualization](#api-call-visualization)
- [Database Queries](#database-queries)
- [Multi-Step Tool Chains](#multi-step-tool-chains)
- [Permission Management](#permission-management)

## Function Call Display

### Basic Function Call Indicator

Show when AI is using functions:

```tsx
interface ToolCall {
  id: string;
  name: string;
  arguments: Record<string, any>;
  status: 'pending' | 'running' | 'completed' | 'failed';
  result?: any;
  error?: string;
  startTime: Date;
  endTime?: Date;
}

function ToolCallDisplay({ toolCall }: { toolCall: ToolCall }) {
  const [expanded, setExpanded] = useState(false);

  const getStatusIcon = () => {
    switch (toolCall.status) {
      case 'pending': return <ClockIcon className="pending" />;
      case 'running': return <Spinner size="small" />;
      case 'completed': return <CheckCircleIcon className="success" />;
      case 'failed': return <XCircleIcon className="error" />;
    }
  };

  const getDuration = () => {
    if (!toolCall.endTime) return null;
    const ms = toolCall.endTime.getTime() - toolCall.startTime.getTime();
    return ms < 1000 ? `${ms}ms` : `${(ms / 1000).toFixed(1)}s`;
  };

  return (
    <div className={`tool-call ${toolCall.status}`}>
      <div
        className="tool-call-header"
        onClick={() => setExpanded(!expanded)}
      >
        {getStatusIcon()}
        <span className="tool-name">{toolCall.name}</span>
        {toolCall.status === 'running' && (
          <span className="status-text">Running...</span>
        )}
        {toolCall.status === 'completed' && getDuration() && (
          <span className="duration">{getDuration()}</span>
        )}
        <ChevronIcon className={expanded ? 'expanded' : ''} />
      </div>

      {expanded && (
        <div className="tool-call-details">
          <div className="tool-arguments">
            <h5>Input:</h5>
            <pre>{JSON.stringify(toolCall.arguments, null, 2)}</pre>
          </div>

          {toolCall.status === 'completed' && toolCall.result && (
            <div className="tool-result">
              <h5>Output:</h5>
              <pre>{JSON.stringify(toolCall.result, null, 2)}</pre>
            </div>
          )}

          {toolCall.status === 'failed' && toolCall.error && (
            <div className="tool-error">
              <h5>Error:</h5>
              <pre className="error-message">{toolCall.error}</pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
```

### Tool Chain Visualization

Show multiple tool calls in sequence:

```tsx
function ToolChain({ tools, currentIndex }) {
  return (
    <div className="tool-chain">
      <div className="chain-header">
        <ToolsIcon />
        <h4>Using multiple tools</h4>
      </div>

      <div className="chain-timeline">
        {tools.map((tool, index) => (
          <div
            key={tool.id}
            className={`chain-step ${
              index < currentIndex ? 'completed' :
              index === currentIndex ? 'active' :
              'pending'
            }`}
          >
            <div className="step-connector" />
            <div className="step-node">
              {index < currentIndex ? (
                <CheckIcon />
              ) : index === currentIndex ? (
                <Spinner size="tiny" />
              ) : (
                <span>{index + 1}</span>
              )}
            </div>
            <div className="step-content">
              <div className="step-name">{tool.name}</div>
              {tool.description && (
                <div className="step-description">{tool.description}</div>
              )}
              {tool.status === 'completed' && tool.preview && (
                <div className="step-preview">{tool.preview}</div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
```

## Code Execution

### Code Execution Display

Show code being run by AI:

```tsx
function CodeExecution({ execution }) {
  const [showCode, setShowCode] = useState(true);
  const [showOutput, setShowOutput] = useState(true);

  return (
    <div className="code-execution">
      <div className="execution-header">
        <CodeIcon />
        <span>Running code</span>
        <span className="language-badge">{execution.language}</span>
        {execution.status === 'running' && <Spinner size="small" />}
      </div>

      <div className="execution-content">
        {/* Code Input */}
        <div className="execution-section">
          <button
            onClick={() => setShowCode(!showCode)}
            className="section-toggle"
          >
            {showCode ? <ChevronDownIcon /> : <ChevronRightIcon />}
            Code
          </button>

          {showCode && (
            <div className="code-block">
              <div className="code-actions">
                <button onClick={() => copyToClipboard(execution.code)}>
                  <CopyIcon /> Copy
                </button>
                <button onClick={() => downloadCode(execution)}>
                  <DownloadIcon /> Download
                </button>
              </div>
              <SyntaxHighlighter
                language={execution.language}
                style={dark}
                showLineNumbers
              >
                {execution.code}
              </SyntaxHighlighter>
            </div>
          )}
        </div>

        {/* Output */}
        {execution.status !== 'pending' && (
          <div className="execution-section">
            <button
              onClick={() => setShowOutput(!showOutput)}
              className="section-toggle"
            >
              {showOutput ? <ChevronDownIcon /> : <ChevronRightIcon />}
              Output
            </button>

            {showOutput && (
              <div className="output-block">
                {execution.status === 'running' ? (
                  <div className="running-output">
                    <Spinner />
                    <span>Executing...</span>
                  </div>
                ) : execution.status === 'completed' ? (
                  <>
                    {execution.output && (
                      <pre className="stdout">{execution.output}</pre>
                    )}
                    {execution.error && (
                      <pre className="stderr">{execution.error}</pre>
                    )}
                    {execution.returnValue !== undefined && (
                      <div className="return-value">
                        <span>Return value:</span>
                        <code>{JSON.stringify(execution.returnValue)}</code>
                      </div>
                    )}
                  </>
                ) : (
                  <div className="execution-error">
                    <ErrorIcon />
                    <span>Execution failed</span>
                    <pre>{execution.error}</pre>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Execution Metadata */}
        {execution.status === 'completed' && (
          <div className="execution-metadata">
            <span>Execution time: {execution.duration}ms</span>
            <span>Memory used: {formatBytes(execution.memoryUsed)}</span>
          </div>
        )}
      </div>
    </div>
  );
}
```

### Interactive Code Execution

Allow users to modify and re-run code:

```tsx
function InteractiveCodeExecution({ initialCode, language, onExecute }) {
  const [code, setCode] = useState(initialCode);
  const [isRunning, setIsRunning] = useState(false);
  const [output, setOutput] = useState(null);
  const [history, setHistory] = useState([]);

  const handleExecute = async () => {
    setIsRunning(true);
    try {
      const result = await onExecute(code, language);
      setOutput(result);
      setHistory(prev => [...prev, { code, result, timestamp: new Date() }]);
    } catch (error) {
      setOutput({ error: error.message });
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="interactive-code-execution">
      <div className="code-editor">
        <div className="editor-toolbar">
          <span className="language">{language}</span>
          <button
            onClick={handleExecute}
            disabled={isRunning}
            className="run-button"
          >
            {isRunning ? (
              <>
                <Spinner size="small" />
                Running...
              </>
            ) : (
              <>
                <PlayIcon />
                Run Code
              </>
            )}
          </button>
        </div>

        <CodeMirror
          value={code}
          onChange={setCode}
          language={language}
          theme="dark"
          height="200px"
        />
      </div>

      {output && (
        <div className="execution-output">
          <div className="output-header">
            <TerminalIcon />
            <span>Output</span>
            <button onClick={() => setOutput(null)}>
              <CloseIcon />
            </button>
          </div>

          {output.error ? (
            <pre className="error-output">{output.error}</pre>
          ) : (
            <pre className="success-output">{output.stdout || output.result}</pre>
          )}
        </div>
      )}

      {history.length > 0 && (
        <details className="execution-history">
          <summary>History ({history.length} runs)</summary>
          {history.map((entry, i) => (
            <div key={i} className="history-entry">
              <span className="history-time">
                {formatTime(entry.timestamp)}
              </span>
              <button onClick={() => setCode(entry.code)}>
                Restore
              </button>
            </div>
          ))}
        </details>
      )}
    </div>
  );
}
```

## Web Search Integration

### Search Progress Display

Show web search in progress:

```tsx
function WebSearchDisplay({ search }) {
  const [expandedResults, setExpandedResults] = useState(new Set());

  return (
    <div className="web-search-display">
      <div className="search-header">
        <SearchIcon />
        <span>Searching the web</span>
        {search.status === 'searching' && <Spinner size="small" />}
      </div>

      <div className="search-query">
        <span className="label">Query:</span>
        <code>{search.query}</code>
      </div>

      {search.status === 'searching' && (
        <div className="search-progress">
          <div className="progress-steps">
            <div className={`step ${search.step >= 1 ? 'active' : ''}`}>
              Searching...
            </div>
            <div className={`step ${search.step >= 2 ? 'active' : ''}`}>
              Analyzing results...
            </div>
            <div className={`step ${search.step >= 3 ? 'active' : ''}`}>
              Extracting information...
            </div>
          </div>
        </div>
      )}

      {search.results && search.results.length > 0 && (
        <div className="search-results">
          <h5>Found {search.results.length} results:</h5>
          {search.results.map((result, i) => (
            <div key={i} className="search-result">
              <div
                className="result-header"
                onClick={() => {
                  const next = new Set(expandedResults);
                  if (next.has(i)) {
                    next.delete(i);
                  } else {
                    next.add(i);
                  }
                  setExpandedResults(next);
                }}
              >
                <span className="result-number">{i + 1}</span>
                <a
                  href={result.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  onClick={(e) => e.stopPropagation()}
                  className="result-title"
                >
                  {result.title}
                </a>
                <span className="result-domain">
                  {new URL(result.url).hostname}
                </span>
                <ChevronIcon
                  className={expandedResults.has(i) ? 'expanded' : ''}
                />
              </div>

              {expandedResults.has(i) && (
                <div className="result-content">
                  <p className="result-snippet">{result.snippet}</p>
                  {result.relevantQuote && (
                    <blockquote className="relevant-quote">
                      "{result.relevantQuote}"
                    </blockquote>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

## File Operations

### File Access Visualization

Show which files AI is reading/writing:

```tsx
function FileOperations({ operations }) {
  const groupedOps = operations.reduce((acc, op) => {
    if (!acc[op.file]) acc[op.file] = [];
    acc[op.file].push(op);
    return acc;
  }, {});

  return (
    <div className="file-operations">
      <div className="operations-header">
        <FileIcon />
        <span>File Operations</span>
        <span className="count">{operations.length} operations</span>
      </div>

      <div className="operations-list">
        {Object.entries(groupedOps).map(([filename, ops]) => (
          <div key={filename} className="file-group">
            <div className="file-header">
              <FileTypeIcon type={getFileType(filename)} />
              <span className="filename">{filename}</span>
              <div className="operation-badges">
                {ops.some(op => op.type === 'read') && (
                  <span className="badge read">Read</span>
                )}
                {ops.some(op => op.type === 'write') && (
                  <span className="badge write">Write</span>
                )}
                {ops.some(op => op.type === 'create') && (
                  <span className="badge create">Create</span>
                )}
                {ops.some(op => op.type === 'delete') && (
                  <span className="badge delete">Delete</span>
                )}
              </div>
            </div>

            <div className="operation-details">
              {ops.map((op, i) => (
                <div key={i} className={`operation ${op.type}`}>
                  <span className="op-type">{op.type.toUpperCase()}</span>
                  <span className="op-time">{formatTime(op.timestamp)}</span>
                  {op.preview && (
                    <div className="op-preview">
                      <code>{op.preview}</code>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
```

## API Call Visualization

### API Request Display

Show external API calls:

```tsx
function APICallDisplay({ apiCall }) {
  const [showDetails, setShowDetails] = useState(false);

  return (
    <div className="api-call-display">
      <div className="api-header">
        <APIIcon />
        <span className="method-badge" data-method={apiCall.method}>
          {apiCall.method}
        </span>
        <code className="api-endpoint">{apiCall.endpoint}</code>
        {apiCall.status === 'pending' && <Spinner size="small" />}
        {apiCall.status === 'success' && (
          <CheckIcon className="success" />
        )}
        {apiCall.status === 'error' && (
          <XIcon className="error" />
        )}
      </div>

      <button
        onClick={() => setShowDetails(!showDetails)}
        className="details-toggle"
      >
        {showDetails ? 'Hide' : 'Show'} Details
      </button>

      {showDetails && (
        <div className="api-details">
          {/* Request */}
          <div className="request-section">
            <h5>Request</h5>

            {apiCall.headers && (
              <div className="headers">
                <h6>Headers:</h6>
                <pre>{JSON.stringify(apiCall.headers, null, 2)}</pre>
              </div>
            )}

            {apiCall.params && (
              <div className="params">
                <h6>Parameters:</h6>
                <pre>{JSON.stringify(apiCall.params, null, 2)}</pre>
              </div>
            )}

            {apiCall.body && (
              <div className="body">
                <h6>Body:</h6>
                <pre>{JSON.stringify(apiCall.body, null, 2)}</pre>
              </div>
            )}
          </div>

          {/* Response */}
          {apiCall.response && (
            <div className="response-section">
              <h5>Response</h5>
              <div className="response-status">
                Status: {apiCall.response.status} {apiCall.response.statusText}
              </div>
              <div className="response-time">
                Time: {apiCall.response.duration}ms
              </div>
              <div className="response-body">
                <h6>Data:</h6>
                <pre>{JSON.stringify(apiCall.response.data, null, 2)}</pre>
              </div>
            </div>
          )}

          {/* Error */}
          {apiCall.error && (
            <div className="error-section">
              <h5>Error</h5>
              <pre className="error-message">{apiCall.error.message}</pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
```

## Database Queries

### SQL Query Visualization

Display database queries being executed:

```tsx
function DatabaseQuery({ query }) {
  const [showResults, setShowResults] = useState(true);
  const [showExplain, setShowExplain] = useState(false);

  return (
    <div className="database-query">
      <div className="query-header">
        <DatabaseIcon />
        <span>Database Query</span>
        <span className="db-name">{query.database}</span>
        {query.status === 'executing' && <Spinner size="small" />}
      </div>

      <div className="query-sql">
        <div className="sql-toolbar">
          <button onClick={() => formatSQL(query.sql)}>
            <FormatIcon /> Format
          </button>
          <button onClick={() => setShowExplain(!showExplain)}>
            <InfoIcon /> Explain
          </button>
          <button onClick={() => copyToClipboard(query.sql)}>
            <CopyIcon /> Copy
          </button>
        </div>

        <SyntaxHighlighter language="sql" style={dark}>
          {query.sql}
        </SyntaxHighlighter>
      </div>

      {showExplain && query.explain && (
        <div className="query-explain">
          <h5>Query Plan:</h5>
          <pre>{query.explain}</pre>
        </div>
      )}

      {query.status === 'completed' && (
        <div className="query-results">
          <div className="results-header">
            <h5>Results</h5>
            <span className="row-count">
              {query.results.length} rows
            </span>
            <span className="exec-time">
              {query.executionTime}ms
            </span>
            <button onClick={() => setShowResults(!showResults)}>
              {showResults ? 'Hide' : 'Show'}
            </button>
          </div>

          {showResults && (
            <div className="results-table">
              <table>
                <thead>
                  <tr>
                    {query.columns.map(col => (
                      <th key={col}>{col}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {query.results.slice(0, 100).map((row, i) => (
                    <tr key={i}>
                      {query.columns.map(col => (
                        <td key={col}>{formatValue(row[col])}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
              {query.results.length > 100 && (
                <div className="more-results">
                  Showing first 100 of {query.results.length} rows
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
```

## Multi-Step Tool Chains

### Complex Tool Workflow

Visualize multi-step tool operations:

```tsx
function ToolWorkflow({ workflow }) {
  const [activeStep, setActiveStep] = useState(workflow.currentStep);

  return (
    <div className="tool-workflow">
      <div className="workflow-header">
        <WorkflowIcon />
        <h4>{workflow.name}</h4>
        <div className="workflow-progress">
          {workflow.completedSteps}/{workflow.totalSteps} steps
        </div>
      </div>

      <div className="workflow-diagram">
        <svg width="100%" height={workflow.steps.length * 80}>
          {workflow.steps.map((step, i) => {
            const y = i * 80 + 40;
            const isActive = i === activeStep;
            const isCompleted = i < workflow.currentStep;

            return (
              <g key={step.id}>
                {/* Connection line */}
                {i < workflow.steps.length - 1 && (
                  <line
                    x1="40"
                    y1={y}
                    x2="40"
                    y2={y + 80}
                    stroke={isCompleted ? '#10b981' : '#e5e7eb'}
                    strokeWidth="2"
                  />
                )}

                {/* Step node */}
                <circle
                  cx="40"
                  cy={y}
                  r="20"
                  fill={isCompleted ? '#10b981' : isActive ? '#3b82f6' : '#e5e7eb'}
                />

                {/* Step icon/number */}
                <text
                  x="40"
                  y={y + 5}
                  textAnchor="middle"
                  fill="white"
                  fontSize="14"
                >
                  {isCompleted ? '✓' : i + 1}
                </text>

                {/* Step details */}
                <foreignObject x="80" y={y - 30} width="300" height="60">
                  <div className={`step-info ${isActive ? 'active' : ''}`}>
                    <div className="step-name">{step.name}</div>
                    <div className="step-description">{step.description}</div>
                    {isActive && step.progress && (
                      <div className="step-progress">
                        <div
                          className="progress-bar"
                          style={{ width: `${step.progress}%` }}
                        />
                      </div>
                    )}
                  </div>
                </foreignObject>
              </g>
            );
          })}
        </svg>
      </div>

      {workflow.error && (
        <div className="workflow-error">
          <ErrorIcon />
          <span>Workflow failed at step {workflow.currentStep + 1}</span>
          <pre>{workflow.error}</pre>
        </div>
      )}
    </div>
  );
}
```

## Permission Management

### Tool Permission Requests

Request user permission for sensitive operations:

```tsx
function PermissionRequest({ request, onApprove, onDeny }) {
  const [rememberChoice, setRememberChoice] = useState(false);

  const getSensitivityLevel = () => {
    if (request.type === 'file_write') return 'high';
    if (request.type === 'api_call') return 'medium';
    if (request.type === 'code_execution') return 'high';
    if (request.type === 'database_write') return 'high';
    return 'low';
  };

  const sensitivity = getSensitivityLevel();

  return (
    <div className={`permission-request ${sensitivity}`}>
      <div className="permission-header">
        <ShieldIcon />
        <h4>Permission Required</h4>
      </div>

      <div className="permission-content">
        <p>The AI wants to perform the following action:</p>

        <div className="action-details">
          <div className="action-type">
            <strong>{request.type.replace('_', ' ').toUpperCase()}</strong>
          </div>
          <div className="action-description">
            {request.description}
          </div>

          {request.details && (
            <details className="action-full-details">
              <summary>View details</summary>
              <pre>{JSON.stringify(request.details, null, 2)}</pre>
            </details>
          )}
        </div>

        {sensitivity === 'high' && (
          <div className="sensitivity-warning">
            <WarningIcon />
            <span>This is a sensitive operation. Review carefully.</span>
          </div>
        )}

        <div className="permission-actions">
          <label className="remember-choice">
            <input
              type="checkbox"
              checked={rememberChoice}
              onChange={(e) => setRememberChoice(e.target.checked)}
            />
            Remember for similar actions this session
          </label>

          <div className="action-buttons">
            <button
              onClick={() => onDeny(request.id)}
              className="deny-btn"
            >
              Deny
            </button>
            <button
              onClick={() => onApprove(request.id, rememberChoice)}
              className="approve-btn"
            >
              Allow
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
```

### Permission Settings

Configure tool permissions:

```tsx
function ToolPermissionSettings({ permissions, onChange }) {
  const toolCategories = [
    { id: 'file_system', name: 'File System', icon: <FileIcon /> },
    { id: 'code_execution', name: 'Code Execution', icon: <CodeIcon /> },
    { id: 'web_requests', name: 'Web Requests', icon: <GlobeIcon /> },
    { id: 'database', name: 'Database', icon: <DatabaseIcon /> },
  ];

  const permissionLevels = [
    { value: 'always_ask', label: 'Always Ask', color: 'orange' },
    { value: 'allow', label: 'Allow', color: 'green' },
    { value: 'deny', label: 'Deny', color: 'red' },
  ];

  return (
    <div className="tool-permission-settings">
      <h3>Tool Permissions</h3>
      <p>Control what actions the AI can perform</p>

      <div className="permission-grid">
        {toolCategories.map(category => (
          <div key={category.id} className="permission-category">
            <div className="category-header">
              {category.icon}
              <span>{category.name}</span>
            </div>

            <div className="permission-controls">
              {permissionLevels.map(level => (
                <label key={level.value} className="permission-option">
                  <input
                    type="radio"
                    name={category.id}
                    value={level.value}
                    checked={permissions[category.id] === level.value}
                    onChange={() => onChange(category.id, level.value)}
                  />
                  <span className={`level-label ${level.color}`}>
                    {level.label}
                  </span>
                </label>
              ))}
            </div>

            <div className="permission-details">
              {category.id === 'file_system' && (
                <ul>
                  <li>Read files</li>
                  <li>Write/modify files</li>
                  <li>Create/delete files</li>
                </ul>
              )}
              {category.id === 'code_execution' && (
                <ul>
                  <li>Run Python code</li>
                  <li>Execute JavaScript</li>
                  <li>Run shell commands</li>
                </ul>
              )}
              {/* More details for other categories */}
            </div>
          </div>
        ))}
      </div>

      <div className="permission-presets">
        <h4>Quick Presets:</h4>
        <button onClick={() => applyPreset('restrictive')}>
          Restrictive (Ask Everything)
        </button>
        <button onClick={() => applyPreset('balanced')}>
          Balanced (Common Actions Allowed)
        </button>
        <button onClick={() => applyPreset('permissive')}>
          Permissive (Allow Most)
        </button>
      </div>
    </div>
  );
}
```

## Best Practices Summary

1. **Show progress clearly** - Users need to know what's happening
2. **Make details expandable** - Progressive disclosure for technical info
3. **Color-code status** - Green=success, yellow=warning, red=error
4. **Display duration** - Show how long operations take
5. **Allow inspection** - Let users see inputs and outputs
6. **Request permissions** - For sensitive operations
7. **Group related operations** - Show tool chains logically
8. **Provide previews** - Quick glimpse of results
9. **Enable re-running** - Let users retry failed operations
10. **Maintain audit trail** - Show complete history of actions