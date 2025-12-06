# Performance Optimization for Data Visualization

Strategies for handling datasets from 100 to 100,000+ points.


## Table of Contents

- [Performance Tiers by Data Volume](#performance-tiers-by-data-volume)
- [Strategy 1: Downsampling (<10K points)](#strategy-1-downsampling-10k-points)
- [Strategy 2: Canvas Rendering (10K-100K points)](#strategy-2-canvas-rendering-10k-100k-points)
- [Strategy 3: Virtualization (Chart Viewport)](#strategy-3-virtualization-chart-viewport)
- [Strategy 4: Server-Side Aggregation (>100K points)](#strategy-4-server-side-aggregation-100k-points)
- [Strategy 5: Progressive Loading](#strategy-5-progressive-loading)
- [Strategy 6: Web Workers (Heavy Computation)](#strategy-6-web-workers-heavy-computation)
- [Performance Benchmarks](#performance-benchmarks)
- [Optimization Checklist](#optimization-checklist)

## Performance Tiers by Data Volume

| Data Points | Rendering | Library | FPS Target | Notes |
|-------------|-----------|---------|------------|-------|
| <1,000 | SVG | Recharts, Plotly | 60fps | Direct rendering, no optimization needed |
| 1K-10K | SVG (optimized) or Canvas | D3.js | 30-60fps | Consider sampling or Canvas |
| 10K-100K | Canvas | D3 Canvas, Plotly WebGL | 30fps+ | Canvas required for smooth interaction |
| >100K | Server aggregation | Backend + simple viz | N/A | Aggregate before sending to client |

---

## Strategy 1: Downsampling (<10K points)

**Reduce data points while preserving visual appearance:**

```javascript
// Largest Triangle Three Buckets (LTTB) algorithm
function downsampleLTTB(data, threshold) {
  if (data.length <= threshold) return data;

  const sampled = [data[0]]; // Always include first point
  const bucketSize = (data.length - 2) / (threshold - 2);

  for (let i = 0; i < threshold - 2; i++) {
    const avgRangeStart = Math.floor((i + 0) * bucketSize) + 1;
    const avgRangeEnd = Math.floor((i + 1) * bucketSize) + 1;
    const avgRangeLength = avgRangeEnd - avgRangeStart;

    // Calculate average point in next bucket
    let avgX = 0, avgY = 0;
    for (let j = avgRangeStart; j < avgRangeEnd; j++) {
      avgX += data[j].x;
      avgY += data[j].y;
    }
    avgX /= avgRangeLength;
    avgY /= avgRangeLength;

    // Find point in current bucket with largest triangle area
    const rangeStart = Math.floor((i - 1) * bucketSize) + 1;
    const rangeEnd = Math.floor((i + 0) * bucketSize) + 1;

    let maxArea = -1, maxAreaPoint;
    const prevPoint = sampled[sampled.length - 1];

    for (let j = rangeStart; j < rangeEnd; j++) {
      const area = Math.abs(
        (prevPoint.x - avgX) * (data[j].y - prevPoint.y) -
        (prevPoint.x - data[j].x) * (avgY - prevPoint.y)
      ) * 0.5;

      if (area > maxArea) {
        maxArea = area;
        maxAreaPoint = data[j];
      }
    }

    sampled.push(maxAreaPoint);
  }

  sampled.push(data[data.length - 1]); // Always include last point
  return sampled;
}

// Simple uniform downsampling (faster but less accurate)
function downsampleUniform(data, targetPoints) {
  const step = Math.ceil(data.length / targetPoints);
  return data.filter((_, i) => i % step === 0);
}

// Usage
const largeDataset = fetch('/api/data').then(r => r.json());  // 5000 points
const downsampled = downsampleLTTB(largeDataset, 500);        // Reduce to 500
```

---

## Strategy 2: Canvas Rendering (10K-100K points)

**Switch from SVG to Canvas for better performance:**

**SVG (DOM-based):**
- Each element is a DOM node
- Slow with >1000 elements
- Accessible, crisp, scalable
- Good for <1000 points

**Canvas (Pixel-based):**
- Single bitmap
- Fast with 10K+ elements
- Not accessible (rasterized)
- Excellent for large datasets

**D3 with Canvas Example:**
```javascript
import * as d3 from 'd3';

function renderCanvasScatter(data, canvas) {
  const width = canvas.width;
  const height = canvas.height;
  const context = canvas.getContext('2d');

  // Scales
  const xScale = d3.scaleLinear()
    .domain(d3.extent(data, d => d.x))
    .range([40, width - 20]);

  const yScale = d3.scaleLinear()
    .domain(d3.extent(data, d => d.y))
    .range([height - 40, 20]);

  // Clear canvas
  context.clearRect(0, 0, width, height);

  // Draw points (can handle 10K+ at 60fps)
  context.fillStyle = '#3B82F6';
  context.globalAlpha = 0.6;

  data.forEach(d => {
    context.beginPath();
    context.arc(xScale(d.x), yScale(d.y), 3, 0, 2 * Math.PI);
    context.fill();
  });

  // Draw axes (using SVG overlay or Canvas)
  drawAxes(context, xScale, yScale, width, height);
}

// Usage with 10,000 points
const canvas = document.getElementById('chart-canvas');
renderCanvasScatter(largeData, canvas);
```

---

## Strategy 3: Virtualization (Chart Viewport)

**Render only visible data (zoom/pan):**

```javascript
function renderVisibleRange(data, viewport) {
  const { xMin, xMax, yMin, yMax } = viewport;

  // Filter to visible data only
  const visibleData = data.filter(d =>
    d.x >= xMin && d.x <= xMax &&
    d.y >= yMin && d.y <= yMax
  );

  // Render only visible points
  return visibleData;
}

// On zoom/pan, update viewport and re-render
function handleZoom(transform) {
  const newViewport = {
    xMin: transform.invertX(0),
    xMax: transform.invertX(width),
    yMin: transform.invertY(height),
    yMax: transform.invertY(0),
  };

  const visibleData = renderVisibleRange(fullDataset, newViewport);
  render(visibleData);
}
```

---

## Strategy 4: Server-Side Aggregation (>100K points)

**Aggregate on backend before sending to client:**

```python
# Backend (Python/FastAPI example)
from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get("/api/chart-data")
def get_aggregated_data(
    granularity: str = "day",  # hour, day, week, month
    metric: str = "sum"         # sum, avg, count
):
    # Load full dataset (millions of rows)
    df = pd.read_csv('large_dataset.csv')

    # Aggregate based on granularity
    if granularity == "day":
        df = df.groupby(pd.Grouper(key='timestamp', freq='D')).agg({
            'value': metric
        }).reset_index()

    # Return manageable dataset (~500 points)
    return df.to_dict('records')
```

```javascript
// Frontend
const data = await fetch('/api/chart-data?granularity=day&metric=sum')
  .then(r => r.json());

// Render ~500 points (fast)
<LineChart data={data}>...</LineChart>
```

---

## Strategy 5: Progressive Loading

**Load data incrementally:**

```javascript
function useLazyChartData(endpoint, chunkSize = 1000) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let offset = 0;
    const chunks = [];

    async function loadChunk() {
      const response = await fetch(`${endpoint}?offset=${offset}&limit=${chunkSize}`);
      const chunk = await response.json();

      if (chunk.length > 0) {
        chunks.push(...chunk);
        setData([...chunks]);
        offset += chunkSize;

        // Load next chunk
        setTimeout(loadChunk, 100);
      } else {
        setLoading(false);
      }
    }

    loadChunk();
  }, [endpoint]);

  return { data, loading };
}

// Usage
const { data, loading } = useLazyChartData('/api/large-dataset');
```

---

## Strategy 6: Web Workers (Heavy Computation)

**Offload data processing to background thread:**

```javascript
// worker.js
self.onmessage = function(e) {
  const { data, operation } = e.data;

  let result;
  switch (operation) {
    case 'downsample':
      result = downsampleLTTB(data, 500);
      break;
    case 'aggregate':
      result = aggregateData(data);
      break;
    default:
      result = data;
  }

  self.postMessage(result);
};

// main.js
const worker = new Worker('worker.js');

worker.postMessage({ data: largeDataset, operation: 'downsample' });

worker.onmessage = function(e) {
  const processedData = e.data;
  renderChart(processedData);
};
```

---

## Performance Benchmarks

**Target Frame Rates:**
- **Static charts:** N/A (render once)
- **Interactive (zoom/pan):** 30fps minimum, 60fps ideal
- **Animated transitions:** 60fps for smooth

**Memory Usage:**
- **SVG:** ~1KB per element (1000 points = 1MB)
- **Canvas:** Fixed (regardless of points)
- **Target:** <100MB for chart rendering

**Load Time:**
- **Initial render:** <1 second
- **Interaction response:** <100ms
- **Data fetch:** <2 seconds

---

## Optimization Checklist

**Before optimizing:**
- [ ] Measure current performance (FPS, memory, load time)
- [ ] Identify bottleneck (rendering, data processing, network)
- [ ] Set performance target

**Optimization techniques (in order):**
1. [ ] Downsample data (if >1000 points)
2. [ ] Switch to Canvas (if >5000 points)
3. [ ] Use Web Workers (if heavy computation)
4. [ ] Server-side aggregation (if >100K points)
5. [ ] Progressive loading (if network-bound)
6. [ ] Virtualization (if scrollable chart area)

**After optimizing:**
- [ ] Verify FPS ≥30fps
- [ ] Check memory usage <100MB
- [ ] Test on low-end devices
- [ ] Ensure accessibility maintained

---

*Performance optimization is about choosing the right strategy for your data volume. Don't optimize prematurely, but plan for scale.*
