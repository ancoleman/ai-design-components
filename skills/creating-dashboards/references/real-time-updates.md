# Real-Time Dashboard Updates

## Table of Contents
- [Update Strategy Comparison](#update-strategy-comparison)
- [Server-Sent Events (SSE)](#server-sent-events-sse)
- [WebSocket Implementation](#websocket-implementation)
- [Polling Patterns](#polling-patterns)
- [Update Coordination](#update-coordination)
- [Error Handling & Reconnection](#error-handling--reconnection)
- [Performance Optimization](#performance-optimization)

## Update Strategy Comparison

### Decision Matrix
| Method | Use Case | Pros | Cons | Best For |
|--------|----------|------|------|----------|
| **SSE** | Server → Client updates | Simple, auto-reconnect, HTTP-based | Unidirectional only | Dashboard metrics, notifications |
| **WebSocket** | Bidirectional communication | Real-time, low latency, bidirectional | Complex setup, stateful | Collaborative editing, chat |
| **Long Polling** | Fallback for older browsers | Works everywhere, simple | Higher latency, resource intensive | Legacy support |
| **Smart Polling** | Periodic updates | Simple, predictable, cacheable | Not real-time, bandwidth usage | Non-critical updates |

### Choosing the Right Method
```typescript
function selectUpdateStrategy(requirements: Requirements): UpdateStrategy {
  // Need bidirectional communication?
  if (requirements.bidirectional) {
    return 'websocket';
  }

  // Need guaranteed real-time updates?
  if (requirements.realTime && requirements.lowLatency) {
    return requirements.serverPush ? 'sse' : 'websocket';
  }

  // Browser compatibility concerns?
  if (requirements.legacySupport) {
    return 'polling';
  }

  // Default recommendation for dashboards
  return 'sse';
}
```

## Server-Sent Events (SSE)

### Basic SSE Implementation
```tsx
function useSSE(endpoint: string) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [status, setStatus] = useState<'connecting' | 'open' | 'closed'>('connecting');

  useEffect(() => {
    const eventSource = new EventSource(endpoint);

    eventSource.onopen = () => {
      setStatus('open');
      setError(null);
    };

    eventSource.onmessage = (event) => {
      try {
        const parsedData = JSON.parse(event.data);
        setData(parsedData);
      } catch (err) {
        console.error('Failed to parse SSE data:', err);
      }
    };

    eventSource.onerror = (err) => {
      setError(err);
      setStatus('closed');

      // EventSource will auto-reconnect
      // But we can handle the error state
      console.error('SSE connection error:', err);
    };

    return () => {
      eventSource.close();
      setStatus('closed');
    };
  }, [endpoint]);

  return { data, error, status };
}
```

### SSE with Multiple Event Types
```tsx
function useMultiEventSSE(endpoint: string) {
  const [metrics, setMetrics] = useState({});
  const [alerts, setAlerts] = useState([]);
  const [status, setStatus] = useState({});

  useEffect(() => {
    const eventSource = new EventSource(endpoint);

    // Different event types
    eventSource.addEventListener('metrics', (event) => {
      const data = JSON.parse(event.data);
      setMetrics(prev => ({ ...prev, ...data }));
    });

    eventSource.addEventListener('alert', (event) => {
      const alert = JSON.parse(event.data);
      setAlerts(prev => [...prev, alert]);
    });

    eventSource.addEventListener('status', (event) => {
      const statusUpdate = JSON.parse(event.data);
      setStatus(statusUpdate);
    });

    // Heartbeat to detect connection issues
    eventSource.addEventListener('heartbeat', () => {
      console.log('Heartbeat received');
    });

    return () => eventSource.close();
  }, [endpoint]);

  return { metrics, alerts, status };
}
```

### SSE Server Implementation (Node.js)
```javascript
// Server-side SSE endpoint
app.get('/api/dashboard/stream', (req, res) => {
  // Set SSE headers
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Access-Control-Allow-Origin': '*'
  });

  // Send initial data
  res.write(`data: ${JSON.stringify({ type: 'init', timestamp: Date.now() })}\n\n`);

  // Send updates every 5 seconds
  const interval = setInterval(() => {
    const metrics = generateMetrics();
    res.write(`event: metrics\ndata: ${JSON.stringify(metrics)}\n\n`);
  }, 5000);

  // Send heartbeat every 30 seconds
  const heartbeat = setInterval(() => {
    res.write(':heartbeat\n\n');
  }, 30000);

  // Clean up on client disconnect
  req.on('close', () => {
    clearInterval(interval);
    clearInterval(heartbeat);
  });
});
```

## WebSocket Implementation

### WebSocket Hook with Reconnection
```tsx
function useWebSocket(url: string, options = {}) {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [lastMessage, setLastMessage] = useState(null);
  const [readyState, setReadyState] = useState(WebSocket.CONNECTING);
  const reconnectAttempts = useRef(0);
  const maxReconnectAttempts = options.maxReconnectAttempts || 5;
  const reconnectInterval = options.reconnectInterval || 3000;

  const connect = useCallback(() => {
    try {
      const ws = new WebSocket(url);

      ws.onopen = () => {
        console.log('WebSocket connected');
        setReadyState(WebSocket.OPEN);
        reconnectAttempts.current = 0;
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        setLastMessage(data);

        // Handle different message types
        switch (data.type) {
          case 'metrics':
            handleMetricsUpdate(data.payload);
            break;
          case 'alert':
            handleAlert(data.payload);
            break;
          default:
            console.log('Unknown message type:', data.type);
        }
      };

      ws.onclose = () => {
        setReadyState(WebSocket.CLOSED);

        // Attempt reconnection
        if (reconnectAttempts.current < maxReconnectAttempts) {
          reconnectAttempts.current++;
          setTimeout(connect, reconnectInterval);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setReadyState(WebSocket.CLOSED);
      };

      setSocket(ws);
    } catch (error) {
      console.error('Failed to create WebSocket:', error);
    }
  }, [url]);

  useEffect(() => {
    connect();

    return () => {
      if (socket) {
        socket.close();
      }
    };
  }, []);

  const sendMessage = useCallback((message: any) => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify(message));
    } else {
      console.warn('WebSocket is not connected');
    }
  }, [socket]);

  return {
    lastMessage,
    sendMessage,
    readyState,
    reconnect: connect
  };
}
```

### Bidirectional Dashboard Communication
```tsx
function InteractiveDashboard() {
  const { lastMessage, sendMessage, readyState } = useWebSocket(
    'ws://localhost:3000/dashboard'
  );

  // Send filter changes to server
  const handleFilterChange = (filters) => {
    sendMessage({
      type: 'UPDATE_FILTERS',
      payload: filters
    });
  };

  // Request specific data
  const requestWidgetData = (widgetId) => {
    sendMessage({
      type: 'REQUEST_WIDGET_DATA',
      payload: { widgetId }
    });
  };

  // Subscribe to specific metrics
  const subscribeToMetric = (metricName) => {
    sendMessage({
      type: 'SUBSCRIBE',
      payload: { metric: metricName }
    });
  };

  return (
    <div>
      {readyState === WebSocket.OPEN ? (
        <span className="status-indicator online">Connected</span>
      ) : (
        <span className="status-indicator offline">Disconnected</span>
      )}

      <FilterPanel onChange={handleFilterChange} />

      {/* Dashboard widgets */}
    </div>
  );
}
```

## Polling Patterns

### Smart Polling with Exponential Backoff
```tsx
function useSmartPolling(
  fetchFunction: () => Promise<any>,
  initialInterval = 5000
) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [isPolling, setIsPolling] = useState(true);
  const intervalRef = useRef(initialInterval);
  const errorCount = useRef(0);

  useEffect(() => {
    if (!isPolling) return;

    const poll = async () => {
      try {
        const result = await fetchFunction();
        setData(result);
        setError(null);

        // Reset interval on success
        intervalRef.current = initialInterval;
        errorCount.current = 0;
      } catch (err) {
        setError(err);
        errorCount.current++;

        // Exponential backoff on errors
        intervalRef.current = Math.min(
          initialInterval * Math.pow(2, errorCount.current),
          60000 // Max 1 minute
        );
      }
    };

    // Initial fetch
    poll();

    // Set up polling interval
    const timer = setInterval(poll, intervalRef.current);

    return () => clearInterval(timer);
  }, [fetchFunction, initialInterval, isPolling]);

  return {
    data,
    error,
    isPolling,
    startPolling: () => setIsPolling(true),
    stopPolling: () => setIsPolling(false)
  };
}
```

### Adaptive Polling Based on Activity
```tsx
function useAdaptivePolling(endpoint: string) {
  const [data, setData] = useState(null);
  const [pollingRate, setPollingRate] = useState(30000); // Start at 30s
  const lastActivityRef = useRef(Date.now());

  useEffect(() => {
    // Track user activity
    const handleActivity = () => {
      lastActivityRef.current = Date.now();
      // Increase polling rate when user is active
      setPollingRate(5000);
    };

    window.addEventListener('mousemove', handleActivity);
    window.addEventListener('keypress', handleActivity);

    // Check for inactivity and slow down polling
    const inactivityTimer = setInterval(() => {
      const timeSinceActivity = Date.now() - lastActivityRef.current;

      if (timeSinceActivity > 60000) {
        // No activity for 1 minute, slow polling
        setPollingRate(60000);
      } else if (timeSinceActivity > 30000) {
        // No activity for 30 seconds, medium polling
        setPollingRate(30000);
      }
    }, 10000);

    return () => {
      window.removeEventListener('mousemove', handleActivity);
      window.removeEventListener('keypress', handleActivity);
      clearInterval(inactivityTimer);
    };
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(endpoint);
        const result = await response.json();
        setData(result);
      } catch (error) {
        console.error('Polling error:', error);
      }
    };

    fetchData();
    const timer = setInterval(fetchData, pollingRate);

    return () => clearInterval(timer);
  }, [endpoint, pollingRate]);

  return { data, pollingRate };
}
```

### Long Polling Implementation
```tsx
function useLongPolling(endpoint: string) {
  const [data, setData] = useState(null);
  const [isPolling, setIsPolling] = useState(true);
  const abortControllerRef = useRef<AbortController>();

  useEffect(() => {
    if (!isPolling) return;

    const poll = async () => {
      abortControllerRef.current = new AbortController();

      try {
        const response = await fetch(endpoint, {
          signal: abortControllerRef.current.signal,
          headers: {
            'X-Long-Poll-Timeout': '30000' // 30 second timeout
          }
        });

        if (response.ok) {
          const result = await response.json();
          setData(result);
        }

        // Immediately poll again
        if (isPolling) {
          poll();
        }
      } catch (error) {
        if (error.name !== 'AbortError') {
          console.error('Long polling error:', error);
          // Retry after delay
          setTimeout(() => {
            if (isPolling) poll();
          }, 5000);
        }
      }
    };

    poll();

    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, [endpoint, isPolling]);

  return {
    data,
    stop: () => setIsPolling(false),
    start: () => setIsPolling(true)
  };
}
```

## Update Coordination

### Centralized Update Manager
```tsx
class DashboardUpdateManager {
  private widgets = new Map<string, WidgetSubscriber>();
  private updateSource: EventSource | WebSocket | null = null;

  initialize(strategy: 'sse' | 'websocket', endpoint: string) {
    if (strategy === 'sse') {
      this.initializeSSE(endpoint);
    } else {
      this.initializeWebSocket(endpoint);
    }
  }

  private initializeSSE(endpoint: string) {
    this.updateSource = new EventSource(endpoint);

    this.updateSource.onmessage = (event) => {
      this.handleUpdate(JSON.parse(event.data));
    };
  }

  private initializeWebSocket(endpoint: string) {
    this.updateSource = new WebSocket(endpoint);

    this.updateSource.onmessage = (event) => {
      this.handleUpdate(JSON.parse(event.data));
    };
  }

  private handleUpdate(update: DashboardUpdate) {
    // Route updates to appropriate widgets
    if (update.widgetId) {
      // Update specific widget
      const subscriber = this.widgets.get(update.widgetId);
      if (subscriber) {
        subscriber.onUpdate(update.data);
      }
    } else if (update.type === 'broadcast') {
      // Update all widgets
      this.widgets.forEach(subscriber => {
        subscriber.onUpdate(update.data);
      });
    }
  }

  subscribeWidget(widgetId: string, subscriber: WidgetSubscriber) {
    this.widgets.set(widgetId, subscriber);
  }

  unsubscribeWidget(widgetId: string) {
    this.widgets.delete(widgetId);
  }

  cleanup() {
    if (this.updateSource) {
      if (this.updateSource instanceof EventSource) {
        this.updateSource.close();
      } else {
        this.updateSource.close();
      }
    }
  }
}

// Usage in component
function Widget({ id, type }) {
  const updateManager = useContext(UpdateManagerContext);

  useEffect(() => {
    const subscriber = {
      onUpdate: (data) => {
        // Handle widget update
        console.log(`Widget ${id} received update:`, data);
      }
    };

    updateManager.subscribeWidget(id, subscriber);

    return () => {
      updateManager.unsubscribeWidget(id);
    };
  }, [id, updateManager]);

  return <div>Widget content</div>;
}
```

### Differential Updates
```tsx
function useDifferentialUpdates(initialData) {
  const [data, setData] = useState(initialData);
  const [updateQueue, setUpdateQueue] = useState([]);

  const applyDiff = useCallback((diff) => {
    setData(prevData => {
      // Apply JSON Patch or custom diff format
      if (diff.op === 'replace') {
        return {
          ...prevData,
          [diff.path]: diff.value
        };
      } else if (diff.op === 'add') {
        return {
          ...prevData,
          [diff.path]: [...(prevData[diff.path] || []), diff.value]
        };
      } else if (diff.op === 'remove') {
        const newData = { ...prevData };
        delete newData[diff.path];
        return newData;
      }
      return prevData;
    });
  }, []);

  // Process update queue
  useEffect(() => {
    if (updateQueue.length > 0) {
      const diff = updateQueue[0];
      applyDiff(diff);
      setUpdateQueue(prev => prev.slice(1));
    }
  }, [updateQueue, applyDiff]);

  return {
    data,
    queueUpdate: (diff) => setUpdateQueue(prev => [...prev, diff])
  };
}
```

## Error Handling & Reconnection

### Robust Connection Management
```tsx
function useRobustConnection(endpoint: string, options = {}) {
  const [status, setStatus] = useState<ConnectionStatus>('disconnected');
  const [error, setError] = useState<Error | null>(null);
  const [retryCount, setRetryCount] = useState(0);

  const maxRetries = options.maxRetries || 5;
  const retryDelay = options.retryDelay || 3000;

  const connect = useCallback(() => {
    setStatus('connecting');
    setError(null);

    const source = new EventSource(endpoint);

    source.onopen = () => {
      setStatus('connected');
      setRetryCount(0);
      console.log('Connection established');
    };

    source.onerror = (event) => {
      setStatus('error');
      setError(new Error('Connection failed'));

      if (retryCount < maxRetries) {
        setStatus('reconnecting');
        setTimeout(() => {
          setRetryCount(prev => prev + 1);
          source.close();
          connect();
        }, retryDelay * Math.pow(2, retryCount)); // Exponential backoff
      } else {
        setStatus('failed');
        console.error('Max reconnection attempts reached');
      }
    };

    return source;
  }, [endpoint, retryCount, maxRetries, retryDelay]);

  useEffect(() => {
    const source = connect();
    return () => source.close();
  }, []);

  return { status, error, retryCount };
}
```

### Circuit Breaker Pattern
```tsx
class CircuitBreaker {
  private failureCount = 0;
  private lastFailureTime: number | null = null;
  private state: 'closed' | 'open' | 'half-open' = 'closed';

  constructor(
    private threshold = 5,
    private timeout = 60000 // 1 minute
  ) {}

  async execute<T>(operation: () => Promise<T>): Promise<T> {
    if (this.state === 'open') {
      const now = Date.now();
      if (now - this.lastFailureTime! > this.timeout) {
        this.state = 'half-open';
      } else {
        throw new Error('Circuit breaker is OPEN');
      }
    }

    try {
      const result = await operation();

      if (this.state === 'half-open') {
        this.state = 'closed';
        this.failureCount = 0;
      }

      return result;
    } catch (error) {
      this.failureCount++;
      this.lastFailureTime = Date.now();

      if (this.failureCount >= this.threshold) {
        this.state = 'open';
        console.error('Circuit breaker opened due to failures');
      }

      throw error;
    }
  }

  reset() {
    this.failureCount = 0;
    this.state = 'closed';
    this.lastFailureTime = null;
  }
}

// Usage
const circuitBreaker = new CircuitBreaker();

function useFetchWithCircuitBreaker(endpoint: string) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      const result = await circuitBreaker.execute(async () => {
        const response = await fetch(endpoint);
        if (!response.ok) throw new Error('Fetch failed');
        return response.json();
      });

      setData(result);
      setError(null);
    } catch (err) {
      setError(err);
      console.error('Fetch with circuit breaker failed:', err);
    }
  };

  return { data, error, retry: fetchData };
}
```

## Performance Optimization

### Update Batching
```tsx
function useBatchedUpdates(flushInterval = 100) {
  const [updates, setUpdates] = useState([]);
  const batchRef = useRef([]);
  const timerRef = useRef<NodeJS.Timeout>();

  const addUpdate = useCallback((update) => {
    batchRef.current.push(update);

    // Clear existing timer
    if (timerRef.current) {
      clearTimeout(timerRef.current);
    }

    // Set new timer to flush batch
    timerRef.current = setTimeout(() => {
      if (batchRef.current.length > 0) {
        setUpdates(batchRef.current);
        batchRef.current = [];
      }
    }, flushInterval);
  }, [flushInterval]);

  // Process batched updates
  useEffect(() => {
    if (updates.length > 0) {
      console.log(`Processing ${updates.length} batched updates`);
      // Apply all updates at once
      applyBatchedUpdates(updates);
      setUpdates([]);
    }
  }, [updates]);

  return { addUpdate };
}
```

### Selective Widget Updates
```tsx
function OptimizedDashboard() {
  const [widgetData, setWidgetData] = useState({});
  const [updateMetadata, setUpdateMetadata] = useState({});

  const handleUpdate = useCallback((update) => {
    const { widgetId, data, timestamp } = update;

    // Check if update is newer than current data
    if (updateMetadata[widgetId]?.timestamp >= timestamp) {
      console.log(`Skipping stale update for widget ${widgetId}`);
      return;
    }

    // Only update the specific widget
    setWidgetData(prev => ({
      ...prev,
      [widgetId]: data
    }));

    setUpdateMetadata(prev => ({
      ...prev,
      [widgetId]: { timestamp, updateCount: (prev[widgetId]?.updateCount || 0) + 1 }
    }));
  }, [updateMetadata]);

  return (
    <div>
      {Object.entries(widgetData).map(([id, data]) => (
        <MemoizedWidget
          key={id}
          id={id}
          data={data}
          metadata={updateMetadata[id]}
        />
      ))}
    </div>
  );
}

const MemoizedWidget = React.memo(({ id, data, metadata }) => {
  return (
    <div className="widget">
      <h3>Widget {id}</h3>
      <pre>{JSON.stringify(data, null, 2)}</pre>
      {metadata && (
        <div className="metadata">
          Updates: {metadata.updateCount}
        </div>
      )}
    </div>
  );
}, (prevProps, nextProps) => {
  // Only re-render if data actually changed
  return JSON.stringify(prevProps.data) === JSON.stringify(nextProps.data);
});
```