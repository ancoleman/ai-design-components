# Search Performance Optimization

## Frontend Performance

### Debouncing and Throttling
```typescript
import { useCallback, useRef } from 'react';

/**
 * Custom debounce hook with cancellation
 */
export function useDebounce<T extends (...args: any[]) => any>(
  callback: T,
  delay: number
): [T, () => void] {
  const timeoutRef = useRef<NodeJS.Timeout>();

  const cancel = useCallback(() => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
  }, []);

  const debouncedCallback = useCallback(
    (...args: Parameters<T>) => {
      cancel();
      timeoutRef.current = setTimeout(() => {
        callback(...args);
      }, delay);
    },
    [callback, delay, cancel]
  ) as T;

  return [debouncedCallback, cancel];
}

/**
 * Custom throttle hook
 */
export function useThrottle<T extends (...args: any[]) => any>(
  callback: T,
  limit: number
): T {
  const inThrottle = useRef(false);

  const throttledCallback = useCallback(
    (...args: Parameters<T>) => {
      if (!inThrottle.current) {
        callback(...args);
        inThrottle.current = true;
        setTimeout(() => {
          inThrottle.current = false;
        }, limit);
      }
    },
    [callback, limit]
  ) as T;

  return throttledCallback;
}

// Adaptive debouncing based on input speed
export function useAdaptiveDebounce(
  callback: (value: string) => void,
  minDelay = 200,
  maxDelay = 500
) {
  const lastInputTime = useRef<number>(Date.now());
  const inputSpeed = useRef<number[]>([]);
  const timeoutRef = useRef<NodeJS.Timeout>();

  const calculateDelay = () => {
    if (inputSpeed.current.length < 2) return maxDelay;

    const avgSpeed = inputSpeed.current.reduce((a, b) => a + b, 0) / inputSpeed.current.length;

    // Faster typing = shorter delay
    if (avgSpeed < 100) return minDelay;
    if (avgSpeed < 200) return (minDelay + maxDelay) / 2;
    return maxDelay;
  };

  return useCallback((value: string) => {
    const now = Date.now();
    const timeSinceLastInput = now - lastInputTime.current;
    lastInputTime.current = now;

    // Track input speed
    inputSpeed.current.push(timeSinceLastInput);
    if (inputSpeed.current.length > 5) {
      inputSpeed.current.shift();
    }

    // Clear existing timeout
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    // Set new timeout with adaptive delay
    const delay = calculateDelay();
    timeoutRef.current = setTimeout(() => {
      callback(value);
    }, delay);
  }, [callback, minDelay, maxDelay]);
}
```

### Request Cancellation
```typescript
class SearchRequestManager {
  private abortController: AbortController | null = null;

  /**
   * Execute search with automatic cancellation of previous requests
   */
  async search(query: string, filters: any): Promise<any> {
    // Cancel previous request
    this.cancel();

    // Create new abort controller
    this.abortController = new AbortController();

    try {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, filters }),
        signal: this.abortController.signal
      });

      if (!response.ok) {
        throw new Error(`Search failed: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      if (error.name === 'AbortError') {
        // Request was cancelled, return null
        return null;
      }
      throw error;
    }
  }

  /**
   * Cancel current request
   */
  cancel(): void {
    if (this.abortController) {
      this.abortController.abort();
      this.abortController = null;
    }
  }
}

// React hook for request management
export function useSearchRequest() {
  const requestManager = useRef(new SearchRequestManager());

  useEffect(() => {
    return () => {
      // Cancel any pending request on unmount
      requestManager.current.cancel();
    };
  }, []);

  const search = useCallback(async (query: string, filters: any) => {
    return requestManager.current.search(query, filters);
  }, []);

  const cancel = useCallback(() => {
    requestManager.current.cancel();
  }, []);

  return { search, cancel };
}
```

### Result Caching
```typescript
interface CacheEntry<T> {
  data: T;
  timestamp: number;
  hits: number;
}

class SearchCache<T> {
  private cache = new Map<string, CacheEntry<T>>();
  private maxSize: number;
  private ttl: number; // Time to live in milliseconds

  constructor(maxSize = 50, ttl = 5 * 60 * 1000) {
    this.maxSize = maxSize;
    this.ttl = ttl;
  }

  /**
   * Generate cache key from search parameters
   */
  private getCacheKey(params: any): string {
    return JSON.stringify(params, Object.keys(params).sort());
  }

  /**
   * Get cached result if available and not expired
   */
  get(params: any): T | null {
    const key = this.getCacheKey(params);
    const entry = this.cache.get(key);

    if (!entry) return null;

    // Check if expired
    if (Date.now() - entry.timestamp > this.ttl) {
      this.cache.delete(key);
      return null;
    }

    // Update hit count for LRU
    entry.hits++;
    return entry.data;
  }

  /**
   * Store result in cache
   */
  set(params: any, data: T): void {
    const key = this.getCacheKey(params);

    // Check cache size and evict if needed
    if (this.cache.size >= this.maxSize && !this.cache.has(key)) {
      this.evictLRU();
    }

    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      hits: 0
    });
  }

  /**
   * Evict least recently used entry
   */
  private evictLRU(): void {
    let minHits = Infinity;
    let lruKey = '';

    for (const [key, entry] of this.cache) {
      if (entry.hits < minHits) {
        minHits = entry.hits;
        lruKey = key;
      }
    }

    if (lruKey) {
      this.cache.delete(lruKey);
    }
  }

  /**
   * Clear entire cache
   */
  clear(): void {
    this.cache.clear();
  }

  /**
   * Get cache statistics
   */
  getStats() {
    return {
      size: this.cache.size,
      maxSize: this.maxSize,
      entries: Array.from(this.cache.entries()).map(([key, entry]) => ({
        key,
        age: Date.now() - entry.timestamp,
        hits: entry.hits
      }))
    };
  }
}

// React hook for cached search
export function useCachedSearch<T>() {
  const cache = useRef(new SearchCache<T>());
  const [stats, setStats] = useState(cache.current.getStats());

  const search = useCallback(async (
    params: any,
    fetcher: () => Promise<T>
  ): Promise<T> => {
    // Check cache first
    const cached = cache.current.get(params);
    if (cached !== null) {
      console.log('Cache hit for:', params);
      return cached;
    }

    // Fetch and cache
    console.log('Cache miss, fetching:', params);
    const result = await fetcher();
    cache.current.set(params, result);

    // Update stats
    setStats(cache.current.getStats());

    return result;
  }, []);

  const clearCache = useCallback(() => {
    cache.current.clear();
    setStats(cache.current.getStats());
  }, []);

  return { search, clearCache, stats };
}
```

## Backend Performance

### Database Index Optimization
```sql
-- PostgreSQL indexes for search optimization

-- Single column indexes
CREATE INDEX idx_products_title ON products USING gin(to_tsvector('english', title));
CREATE INDEX idx_products_description ON products USING gin(to_tsvector('english', description));
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_brand ON products(brand);
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_products_created_at ON products(created_at DESC);
CREATE INDEX idx_products_rating ON products(rating DESC);

-- Composite indexes for common filter combinations
CREATE INDEX idx_products_category_price ON products(category, price);
CREATE INDEX idx_products_brand_price ON products(brand, price);
CREATE INDEX idx_products_category_brand ON products(category, brand);

-- Partial indexes for common conditions
CREATE INDEX idx_products_in_stock ON products(id) WHERE in_stock = true;
CREATE INDEX idx_products_featured ON products(id) WHERE featured = true;
CREATE INDEX idx_products_on_sale ON products(id) WHERE sale_price IS NOT NULL;

-- Full-text search index
CREATE INDEX idx_products_search_vector ON products
USING gin((
  setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
  setweight(to_tsvector('english', coalesce(description, '')), 'B') ||
  setweight(to_tsvector('english', coalesce(tags, '')), 'C')
));

-- BRIN index for time-series data
CREATE INDEX idx_products_created_brin ON products USING brin(created_at);
```

### Query Optimization Patterns
```python
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload, joinedload

class OptimizedSearchQueries:
    """Optimized database query patterns."""

    @staticmethod
    def search_with_pagination(session, query, filters, page=1, per_page=20):
        """Optimized search with count query separation."""

        # Build base query
        base_query = session.query(Product)

        # Apply filters
        if query:
            base_query = base_query.filter(
                or_(
                    Product.title.ilike(f'%{query}%'),
                    Product.description.ilike(f'%{query}%')
                )
            )

        if filters.get('category'):
            base_query = base_query.filter(Product.category.in_(filters['category']))

        if filters.get('min_price'):
            base_query = base_query.filter(Product.price >= filters['min_price'])

        # Separate count query (without joins/eager loading)
        count_query = base_query.with_entities(func.count(Product.id))
        total = count_query.scalar()

        # Main query with eager loading
        results_query = base_query.options(
            selectinload(Product.images),
            selectinload(Product.reviews)
        )

        # Apply pagination
        offset = (page - 1) * per_page
        results = results_query.offset(offset).limit(per_page).all()

        return {
            'results': results,
            'total': total,
            'page': page,
            'per_page': per_page
        }

    @staticmethod
    def get_facet_counts(session, base_filters=None):
        """Get facet counts with single query using window functions."""

        # Use CTE for base filtered results
        base_query = session.query(Product.id)

        if base_filters:
            # Apply base filters
            pass

        base_cte = base_query.cte('base_products')

        # Get all facets in single query using UNION ALL
        facets_query = session.query(
            literal('category').label('facet_type'),
            Product.category.label('facet_value'),
            func.count(Product.id).label('count')
        ).join(
            base_cte, Product.id == base_cte.c.id
        ).group_by(Product.category)

        # Add more facets
        facets_query = facets_query.union_all(
            session.query(
                literal('brand'),
                Product.brand,
                func.count(Product.id)
            ).join(
                base_cte, Product.id == base_cte.c.id
            ).group_by(Product.brand)
        )

        results = facets_query.all()

        # Group by facet type
        facets = {}
        for facet_type, facet_value, count in results:
            if facet_type not in facets:
                facets[facet_type] = []
            facets[facet_type].append({
                'value': facet_value,
                'count': count
            })

        return facets
```

### Elasticsearch Performance Tuning
```python
class ElasticsearchOptimization:
    """Elasticsearch performance optimization strategies."""

    @staticmethod
    def create_optimized_mapping():
        """Create mapping optimized for search performance."""
        return {
            'settings': {
                'number_of_shards': 2,
                'number_of_replicas': 1,
                'index': {
                    'refresh_interval': '5s',  # Reduce refresh frequency
                    'max_result_window': 10000,  # Limit deep pagination
                    'max_inner_result_window': 100,
                    'search': {
                        'slowlog': {
                            'threshold': {
                                'query': {
                                    'warn': '10s',
                                    'info': '5s'
                                }
                            }
                        }
                    }
                },
                'analysis': {
                    'analyzer': {
                        'search_analyzer': {
                            'type': 'custom',
                            'tokenizer': 'standard',
                            'filter': [
                                'lowercase',
                                'stop',
                                'snowball',
                                'synonym_filter'
                            ]
                        }
                    },
                    'filter': {
                        'synonym_filter': {
                            'type': 'synonym',
                            'synonyms': [
                                'laptop,notebook',
                                'phone,mobile,cell',
                                'tv,television'
                            ]
                        }
                    }
                }
            },
            'mappings': {
                'properties': {
                    'title': {
                        'type': 'text',
                        'analyzer': 'search_analyzer',
                        'search_analyzer': 'search_analyzer',
                        'fields': {
                            'keyword': {
                                'type': 'keyword',
                                'ignore_above': 256
                            },
                            'ngram': {
                                'type': 'text',
                                'analyzer': 'ngram_analyzer'
                            }
                        }
                    },
                    'description': {
                        'type': 'text',
                        'analyzer': 'search_analyzer',
                        'index_options': 'offsets'  # For highlighting
                    },
                    'category': {
                        'type': 'keyword',
                        'eager_global_ordinals': True  # For aggregations
                    },
                    'price': {
                        'type': 'scaled_float',
                        'scaling_factor': 100  # Store as cents
                    },
                    'suggest': {
                        'type': 'completion',  # For autocomplete
                        'analyzer': 'simple'
                    }
                }
            }
        }

    @staticmethod
    def search_with_request_cache(es, query, use_cache=True):
        """Use request cache for aggregations."""
        body = {
            'query': query,
            'aggs': {
                'categories': {
                    'terms': {
                        'field': 'category',
                        'size': 20
                    }
                }
            },
            'request_cache': use_cache  # Enable request cache
        }

        return es.search(index='products', body=body)

    @staticmethod
    def bulk_index_optimized(es, documents, batch_size=500):
        """Optimized bulk indexing."""
        from elasticsearch.helpers import bulk, parallel_bulk

        def generate_actions():
            for doc in documents:
                yield {
                    '_index': 'products',
                    '_id': doc['id'],
                    '_source': doc,
                    '_op_type': 'index'  # Use 'create' to avoid updates
                }

        # Use parallel bulk for large datasets
        if len(documents) > 10000:
            for success, info in parallel_bulk(
                es,
                generate_actions(),
                chunk_size=batch_size,
                thread_count=4,
                raise_on_error=False
            ):
                if not success:
                    print(f"Failed to index: {info}")
        else:
            bulk(es, generate_actions(), chunk_size=batch_size)
```

## Monitoring and Metrics

### Performance Tracking
```typescript
class PerformanceMonitor {
  private metrics: Map<string, number[]> = new Map();

  /**
   * Measure operation performance
   */
  async measure<T>(
    operation: string,
    fn: () => Promise<T>
  ): Promise<T> {
    const start = performance.now();

    try {
      const result = await fn();
      const duration = performance.now() - start;

      this.recordMetric(operation, duration);

      // Log slow operations
      if (duration > 1000) {
        console.warn(`Slow operation: ${operation} took ${duration.toFixed(2)}ms`);
      }

      return result;
    } catch (error) {
      const duration = performance.now() - start;
      this.recordMetric(`${operation}_error`, duration);
      throw error;
    }
  }

  /**
   * Record metric
   */
  private recordMetric(operation: string, duration: number): void {
    if (!this.metrics.has(operation)) {
      this.metrics.set(operation, []);
    }

    const values = this.metrics.get(operation)!;
    values.push(duration);

    // Keep only last 100 measurements
    if (values.length > 100) {
      values.shift();
    }
  }

  /**
   * Get performance statistics
   */
  getStats(operation?: string): any {
    if (operation) {
      const values = this.metrics.get(operation);
      if (!values || values.length === 0) {
        return null;
      }

      return this.calculateStats(values);
    }

    // Get stats for all operations
    const allStats: any = {};
    for (const [op, values] of this.metrics) {
      allStats[op] = this.calculateStats(values);
    }

    return allStats;
  }

  /**
   * Calculate statistics from values
   */
  private calculateStats(values: number[]) {
    const sorted = [...values].sort((a, b) => a - b);
    const sum = values.reduce((a, b) => a + b, 0);

    return {
      count: values.length,
      mean: sum / values.length,
      median: sorted[Math.floor(sorted.length / 2)],
      min: sorted[0],
      max: sorted[sorted.length - 1],
      p95: sorted[Math.floor(sorted.length * 0.95)],
      p99: sorted[Math.floor(sorted.length * 0.99)]
    };
  }

  /**
   * Send metrics to analytics service
   */
  report(): void {
    const stats = this.getStats();

    // Send to analytics service
    if (typeof window !== 'undefined' && window.gtag) {
      Object.entries(stats).forEach(([operation, metrics]: [string, any]) => {
        window.gtag('event', 'performance', {
          event_category: 'search',
          event_label: operation,
          value: Math.round(metrics.mean)
        });
      });
    }
  }
}

// Usage
const monitor = new PerformanceMonitor();

export async function searchWithMonitoring(query: string, filters: any) {
  return monitor.measure('search_request', async () => {
    const response = await fetch('/api/search', {
      method: 'POST',
      body: JSON.stringify({ query, filters })
    });

    return monitor.measure('search_parse', async () => {
      return response.json();
    });
  });
}
```