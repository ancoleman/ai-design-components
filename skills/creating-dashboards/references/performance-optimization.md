# Dashboard Performance Optimization

## Table of Contents
- [Loading Strategies](#loading-strategies)
- [Rendering Optimization](#rendering-optimization)
- [Data Management](#data-management)
- [Memory Management](#memory-management)
- [Network Optimization](#network-optimization)
- [Monitoring & Profiling](#monitoring--profiling)

## Loading Strategies

### Progressive Widget Loading
```tsx
function ProgressiveDashboard({ widgets }) {
  const [loadPhase, setLoadPhase] = useState(0);
  const [loadedWidgets, setLoadedWidgets] = useState<Set<string>>(new Set());

  useEffect(() => {
    const loadingStrategy = [
      // Phase 1: Critical above-the-fold widgets
      widgets.filter(w => w.priority === 'critical'),
      // Phase 2: Visible widgets
      widgets.filter(w => w.priority === 'high'),
      // Phase 3: Below-the-fold widgets
      widgets.filter(w => w.priority === 'normal'),
      // Phase 4: Optional widgets
      widgets.filter(w => w.priority === 'low')
    ];

    loadingStrategy.forEach((phase, index) => {
      setTimeout(() => {
        setLoadPhase(index + 1);
        phase.forEach(widget => {
          setLoadedWidgets(prev => new Set(prev).add(widget.id));
        });
      }, index * 200); // Stagger loading
    });
  }, [widgets]);

  return (
    <div className="dashboard">
      {widgets.map(widget => (
        <div key={widget.id} className="widget-container">
          {loadedWidgets.has(widget.id) ? (
            <Widget {...widget} />
          ) : (
            <WidgetPlaceholder />
          )}
        </div>
      ))}
    </div>
  );
}
```

### Intersection Observer Loading
```tsx
function LazyWidget({ widget }) {
  const ref = useRef<HTMLDivElement>(null);
  const [isVisible, setIsVisible] = useState(false);
  const [hasLoaded, setHasLoaded] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          if (!hasLoaded) {
            setHasLoaded(true);
          }
        } else {
          setIsVisible(false);
        }
      },
      {
        threshold: 0.1,
        rootMargin: '50px' // Start loading 50px before visible
      }
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => {
      if (ref.current) {
        observer.unobserve(ref.current);
      }
    };
  }, [hasLoaded]);

  return (
    <div ref={ref} className="widget-wrapper">
      {hasLoaded ? (
        <Widget {...widget} isVisible={isVisible} />
      ) : (
        <WidgetSkeleton height={widget.height} />
      )}
    </div>
  );
}
```

### Priority-Based Loading Queue
```tsx
class WidgetLoader {
  private queue: PriorityQueue<Widget>;
  private loading = new Map<string, Promise<any>>();
  private maxConcurrent = 4;
  private currentLoading = 0;

  constructor() {
    this.queue = new PriorityQueue((a, b) => b.priority - a.priority);
  }

  async loadWidget(widget: Widget): Promise<any> {
    // Check if already loading
    if (this.loading.has(widget.id)) {
      return this.loading.get(widget.id);
    }

    // Add to queue
    this.queue.enqueue(widget);
    return this.processQueue();
  }

  private async processQueue() {
    while (this.currentLoading < this.maxConcurrent && !this.queue.isEmpty()) {
      const widget = this.queue.dequeue();
      if (!widget) break;

      this.currentLoading++;
      const loadPromise = this.fetchWidgetData(widget)
        .finally(() => {
          this.currentLoading--;
          this.loading.delete(widget.id);
          this.processQueue(); // Process next in queue
        });

      this.loading.set(widget.id, loadPromise);
    }
  }

  private async fetchWidgetData(widget: Widget) {
    const response = await fetch(`/api/widget/${widget.id}/data`);
    return response.json();
  }
}

// Usage
const widgetLoader = new WidgetLoader();

function PriorityLoadedWidget({ widget }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    widgetLoader.loadWidget(widget).then(setData);
  }, [widget]);

  return data ? <Widget data={data} /> : <Loading />;
}
```

## Rendering Optimization

### React.memo for Widget Optimization
```tsx
const OptimizedWidget = React.memo(
  ({ id, data, filters }) => {
    console.log(`Rendering widget ${id}`);

    return (
      <div className="widget">
        <WidgetHeader id={id} />
        <WidgetContent data={data} />
        <WidgetFooter filters={filters} />
      </div>
    );
  },
  (prevProps, nextProps) => {
    // Custom comparison function
    // Only re-render if data actually changed
    return (
      prevProps.id === nextProps.id &&
      JSON.stringify(prevProps.data) === JSON.stringify(nextProps.data) &&
      JSON.stringify(prevProps.filters) === JSON.stringify(nextProps.filters)
    );
  }
);
```

### Virtualization for Large Widget Lists
```tsx
import { VariableSizeGrid } from 'react-window';

function VirtualizedDashboard({ widgets, columns = 4 }) {
  const getItemSize = (index: number) => {
    const widget = widgets[index];
    return widget.height || 300; // Default height
  };

  const Cell = ({ columnIndex, rowIndex, style }) => {
    const index = rowIndex * columns + columnIndex;
    if (index >= widgets.length) return null;

    return (
      <div style={style}>
        <OptimizedWidget {...widgets[index]} />
      </div>
    );
  };

  return (
    <VariableSizeGrid
      columnCount={columns}
      columnWidth={index => 300} // Fixed column width
      height={window.innerHeight}
      rowCount={Math.ceil(widgets.length / columns)}
      rowHeight={getItemSize}
      width={window.innerWidth}
      overscanRowCount={2} // Render 2 extra rows for smooth scrolling
    >
      {Cell}
    </VariableSizeGrid>
  );
}
```

### Batched State Updates
```tsx
function useBatchedUpdates() {
  const [updates, setUpdates] = useState<Update[]>([]);
  const pendingUpdates = useRef<Update[]>([]);
  const rafId = useRef<number>();

  const scheduleUpdate = useCallback((update: Update) => {
    pendingUpdates.current.push(update);

    // Cancel previous frame
    if (rafId.current) {
      cancelAnimationFrame(rafId.current);
    }

    // Schedule batch update
    rafId.current = requestAnimationFrame(() => {
      setUpdates(current => [...current, ...pendingUpdates.current]);
      pendingUpdates.current = [];
    });
  }, []);

  useEffect(() => {
    return () => {
      if (rafId.current) {
        cancelAnimationFrame(rafId.current);
      }
    };
  }, []);

  return { updates, scheduleUpdate };
}
```

## Data Management

### Efficient Data Structures
```tsx
class DashboardDataStore {
  private widgetData = new Map<string, any>();
  private subscriptions = new Map<string, Set<Function>>();
  private cache = new LRUCache<string, any>(100); // Max 100 entries

  setWidgetData(widgetId: string, data: any) {
    // Store in map
    this.widgetData.set(widgetId, data);

    // Update cache
    this.cache.set(widgetId, {
      data,
      timestamp: Date.now()
    });

    // Notify subscribers
    this.notifySubscribers(widgetId, data);
  }

  getWidgetData(widgetId: string): any {
    // Try cache first
    const cached = this.cache.get(widgetId);
    if (cached && Date.now() - cached.timestamp < 60000) {
      return cached.data;
    }

    // Return from store
    return this.widgetData.get(widgetId);
  }

  subscribe(widgetId: string, callback: Function) {
    if (!this.subscriptions.has(widgetId)) {
      this.subscriptions.set(widgetId, new Set());
    }
    this.subscriptions.get(widgetId)!.add(callback);

    // Return unsubscribe function
    return () => {
      const subs = this.subscriptions.get(widgetId);
      if (subs) {
        subs.delete(callback);
      }
    };
  }

  private notifySubscribers(widgetId: string, data: any) {
    const subs = this.subscriptions.get(widgetId);
    if (subs) {
      subs.forEach(callback => callback(data));
    }
  }

  clearCache() {
    this.cache.clear();
  }

  clearWidget(widgetId: string) {
    this.widgetData.delete(widgetId);
    this.cache.delete(widgetId);
    this.subscriptions.delete(widgetId);
  }
}
```

### Data Aggregation and Transformation
```tsx
function useAggregatedData(widgets: Widget[]) {
  const [aggregated, setAggregated] = useState({});

  useEffect(() => {
    const worker = new Worker('/workers/data-aggregator.js');

    worker.postMessage({
      type: 'AGGREGATE',
      widgets: widgets.map(w => ({ id: w.id, type: w.type }))
    });

    worker.onmessage = (event) => {
      if (event.data.type === 'AGGREGATED') {
        setAggregated(event.data.result);
      }
    };

    return () => worker.terminate();
  }, [widgets]);

  return aggregated;
}

// Web Worker: data-aggregator.js
self.onmessage = function(event) {
  if (event.data.type === 'AGGREGATE') {
    const result = {};

    event.data.widgets.forEach(widget => {
      // Perform heavy computations
      result[widget.id] = performAggregation(widget);
    });

    self.postMessage({
      type: 'AGGREGATED',
      result
    });
  }
};
```

## Memory Management

### Widget Cleanup
```tsx
function Widget({ id, data }) {
  useEffect(() => {
    // Setup
    const charts = initializeCharts(data);
    const subscriptions = setupSubscriptions(id);

    // Cleanup
    return () => {
      // Dispose of chart instances
      charts.forEach(chart => chart.destroy());

      // Cancel subscriptions
      subscriptions.forEach(sub => sub.unsubscribe());

      // Clear timers
      clearInterval(refreshTimer);

      // Clear cached data
      widgetCache.delete(id);
    };
  }, [id]);

  return <div id={`widget-${id}`}>...</div>;
}
```

### Memory Leak Prevention
```tsx
function useSafeAsync() {
  const mounted = useRef(true);
  const abortControllers = useRef<Set<AbortController>>(new Set());

  useEffect(() => {
    return () => {
      mounted.current = false;
      // Abort all pending requests
      abortControllers.current.forEach(controller => controller.abort());
    };
  }, []);

  const safeAsync = useCallback(async (asyncFunc: () => Promise<any>) => {
    const controller = new AbortController();
    abortControllers.current.add(controller);

    try {
      const result = await asyncFunc();

      if (mounted.current) {
        return result;
      }
    } catch (error) {
      if (error.name !== 'AbortError') {
        throw error;
      }
    } finally {
      abortControllers.current.delete(controller);
    }
  }, []);

  return safeAsync;
}
```

### Resource Pooling
```tsx
class ChartPool {
  private available: Chart[] = [];
  private inUse = new Map<string, Chart>();
  private maxSize = 20;

  acquire(widgetId: string, config: ChartConfig): Chart {
    let chart = this.available.pop();

    if (!chart) {
      chart = new Chart(config);
    } else {
      chart.update(config);
    }

    this.inUse.set(widgetId, chart);
    return chart;
  }

  release(widgetId: string) {
    const chart = this.inUse.get(widgetId);

    if (chart) {
      this.inUse.delete(widgetId);

      if (this.available.length < this.maxSize) {
        chart.clear();
        this.available.push(chart);
      } else {
        chart.destroy();
      }
    }
  }

  clear() {
    this.inUse.forEach(chart => chart.destroy());
    this.available.forEach(chart => chart.destroy());
    this.inUse.clear();
    this.available = [];
  }
}

const chartPool = new ChartPool();

function PooledChartWidget({ id, config }) {
  useEffect(() => {
    const chart = chartPool.acquire(id, config);

    return () => {
      chartPool.release(id);
    };
  }, [id, config]);

  return <div id={`chart-${id}`} />;
}
```

## Network Optimization

### Request Batching
```tsx
class RequestBatcher {
  private batch: Map<string, Promise<any>> = new Map();
  private timer: NodeJS.Timeout | null = null;
  private delay = 50; // Batch window in ms

  async fetch(endpoint: string, params: any): Promise<any> {
    const key = `${endpoint}:${JSON.stringify(params)}`;

    // Check if request already in batch
    if (this.batch.has(key)) {
      return this.batch.get(key);
    }

    // Create promise for this request
    const promise = new Promise((resolve, reject) => {
      // Add to batch
      this.addToBatch(key, { endpoint, params, resolve, reject });
    });

    this.batch.set(key, promise);
    return promise;
  }

  private addToBatch(key: string, request: BatchRequest) {
    if (!this.timer) {
      this.timer = setTimeout(() => this.executeBatch(), this.delay);
    }
  }

  private async executeBatch() {
    const requests = Array.from(this.batch.entries());
    this.batch.clear();
    this.timer = null;

    try {
      // Send all requests in single call
      const response = await fetch('/api/batch', {
        method: 'POST',
        body: JSON.stringify(requests.map(([key, _]) => key))
      });

      const results = await response.json();

      // Resolve individual promises
      requests.forEach(([key, promise], index) => {
        promise.resolve(results[index]);
      });
    } catch (error) {
      requests.forEach(([key, promise]) => {
        promise.reject(error);
      });
    }
  }
}
```

### Response Compression
```tsx
function useCompressedData(endpoint: string) {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch(endpoint, {
      headers: {
        'Accept-Encoding': 'gzip, deflate, br'
      }
    })
    .then(response => {
      // Check if response is compressed
      const encoding = response.headers.get('content-encoding');
      console.log(`Response compressed with: ${encoding}`);

      return response.json();
    })
    .then(setData);
  }, [endpoint]);

  return data;
}
```

### Prefetching Strategies
```tsx
function usePrefetch() {
  const prefetchCache = useRef(new Map());

  const prefetch = useCallback(async (widgets: Widget[]) => {
    // Identify widgets likely to be needed
    const toPrefetch = widgets.filter(w =>
      w.priority === 'high' && !prefetchCache.current.has(w.id)
    );

    // Prefetch in background
    toPrefetch.forEach(async widget => {
      const data = await fetch(`/api/widget/${widget.id}/data`, {
        priority: 'low' // Low priority fetch
      });

      prefetchCache.current.set(widget.id, await data.json());
    });
  }, []);

  const getPrefetched = useCallback((widgetId: string) => {
    const data = prefetchCache.current.get(widgetId);
    if (data) {
      prefetchCache.current.delete(widgetId); // Use once
    }
    return data;
  }, []);

  return { prefetch, getPrefetched };
}
```

## Monitoring & Profiling

### Performance Metrics Collection
```tsx
class DashboardMetrics {
  private metrics = {
    widgetLoadTimes: new Map<string, number>(),
    renderTimes: new Map<string, number>(),
    dataFetchTimes: new Map<string, number>(),
    errors: []
  };

  startTimer(category: string, id: string) {
    const key = `${category}:${id}`;
    performance.mark(`${key}:start`);
  }

  endTimer(category: string, id: string) {
    const key = `${category}:${id}`;
    performance.mark(`${key}:end`);

    performance.measure(
      key,
      `${key}:start`,
      `${key}:end`
    );

    const measure = performance.getEntriesByName(key)[0];
    this.metrics[category].set(id, measure.duration);
  }

  getReport() {
    const avgLoadTime = this.calculateAverage(this.metrics.widgetLoadTimes);
    const avgRenderTime = this.calculateAverage(this.metrics.renderTimes);
    const avgFetchTime = this.calculateAverage(this.metrics.dataFetchTimes);

    return {
      averageLoadTime: avgLoadTime,
      averageRenderTime: avgRenderTime,
      averageFetchTime: avgFetchTime,
      totalErrors: this.metrics.errors.length,
      slowestWidget: this.findSlowest(this.metrics.widgetLoadTimes),
      performance: this.calculatePerformanceScore()
    };
  }

  private calculateAverage(map: Map<string, number>): number {
    const values = Array.from(map.values());
    return values.reduce((a, b) => a + b, 0) / values.length;
  }

  private findSlowest(map: Map<string, number>): string {
    let slowest = '';
    let maxTime = 0;

    map.forEach((time, id) => {
      if (time > maxTime) {
        maxTime = time;
        slowest = id;
      }
    });

    return slowest;
  }

  private calculatePerformanceScore(): number {
    const avgLoad = this.calculateAverage(this.metrics.widgetLoadTimes);

    if (avgLoad < 100) return 100;
    if (avgLoad < 300) return 90;
    if (avgLoad < 500) return 70;
    if (avgLoad < 1000) return 50;
    return 30;
  }
}

// Usage
const metrics = new DashboardMetrics();

function MonitoredWidget({ id, ...props }) {
  useEffect(() => {
    metrics.startTimer('widgetLoadTimes', id);

    return () => {
      metrics.endTimer('widgetLoadTimes', id);
    };
  }, [id]);

  return <Widget id={id} {...props} />;
}
```

### Real User Monitoring (RUM)
```tsx
function useRUM() {
  useEffect(() => {
    // Core Web Vitals
    if ('PerformanceObserver' in window) {
      // Largest Contentful Paint
      const lcpObserver = new PerformanceObserver((entries) => {
        const lastEntry = entries.getEntries().pop();
        console.log('LCP:', lastEntry?.startTime);

        // Send to analytics
        analytics.track('dashboard_lcp', {
          value: lastEntry?.startTime,
          url: window.location.href
        });
      });
      lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });

      // First Input Delay
      const fidObserver = new PerformanceObserver((entries) => {
        entries.getEntries().forEach(entry => {
          console.log('FID:', entry.processingStart - entry.startTime);
        });
      });
      fidObserver.observe({ entryTypes: ['first-input'] });

      // Cumulative Layout Shift
      let clsValue = 0;
      const clsObserver = new PerformanceObserver((entries) => {
        entries.getEntries().forEach(entry => {
          if (!entry.hadRecentInput) {
            clsValue += entry.value;
            console.log('CLS:', clsValue);
          }
        });
      });
      clsObserver.observe({ entryTypes: ['layout-shift'] });

      return () => {
        lcpObserver.disconnect();
        fidObserver.disconnect();
        clsObserver.disconnect();
      };
    }
  }, []);
}
```