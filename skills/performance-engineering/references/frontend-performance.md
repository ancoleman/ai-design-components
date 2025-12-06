# Frontend Performance Optimization

## Table of Contents

1. [Core Web Vitals](#core-web-vitals)
2. [Bundle Optimization](#bundle-optimization)
3. [Image Optimization](#image-optimization)
4. [Resource Loading](#resource-loading)
5. [Rendering Performance](#rendering-performance)
6. [Measurement Tools](#measurement-tools)

---

## Core Web Vitals

### Overview

Core Web Vitals are Google's metrics for user experience, affecting SEO rankings and user retention.

**Three key metrics:**
1. **LCP (Largest Contentful Paint):** Loading performance
2. **INP (Interaction to Next Paint):** Interactivity (replaced FID in 2024)
3. **CLS (Cumulative Layout Shift):** Visual stability

### LCP (Largest Contentful Paint)

**Definition:** Time until largest content element is rendered.

**Targets:**
- **Good:** < 2.5 seconds
- **Needs Improvement:** 2.5s - 4s
- **Poor:** > 4 seconds

**What counts as LCP:**
- `<img>` elements
- `<image>` inside `<svg>`
- `<video>` with poster image
- Element with background image via CSS
- Block-level text elements

**Optimization techniques:**

#### 1. Optimize Server Response Time (TTFB)
```typescript
// Use CDN for static assets
// Enable HTTP/2 or HTTP/3
// Optimize database queries
// Use server-side caching

// Cloudflare, Fastly, or Akamai for CDN
```

#### 2. Preload Critical Resources
```html
<!-- Preload LCP image -->
<link rel="preload" as="image" href="/hero-image.jpg" />

<!-- Preload critical fonts -->
<link rel="preload" as="font" href="/fonts/main.woff2" type="font/woff2" crossorigin />
```

#### 3. Optimize Images
```html
<!-- Use modern formats -->
<picture>
  <source srcset="/image.avif" type="image/avif" />
  <source srcset="/image.webp" type="image/webp" />
  <img src="/image.jpg" alt="Fallback" loading="eager" />
</picture>

<!-- Use responsive images -->
<img
  srcset="/image-320w.jpg 320w, /image-640w.jpg 640w, /image-1280w.jpg 1280w"
  sizes="(max-width: 640px) 100vw, 640px"
  src="/image-640w.jpg"
  alt="Responsive image"
/>
```

#### 4. Eliminate Render-Blocking Resources
```html
<!-- Inline critical CSS -->
<style>
  /* Critical above-the-fold styles */
  body { font-family: sans-serif; }
  .hero { background: blue; }
</style>

<!-- Defer non-critical CSS -->
<link rel="preload" as="style" href="/styles.css" onload="this.rel='stylesheet'" />

<!-- Defer JavaScript -->
<script src="/app.js" defer></script>
```

### INP (Interaction to Next Paint)

**Definition:** Latency of interactions (clicks, taps, key presses) to visual update.

**Targets:**
- **Good:** < 200ms
- **Needs Improvement:** 200ms - 500ms
- **Poor:** > 500ms

**Optimization techniques:**

#### 1. Minimize JavaScript Execution Time
```typescript
// Bad: Heavy computation on main thread
function processData(data: any[]) {
  return data.map(item => expensiveCalculation(item)); // Blocks UI
}

// Good: Use Web Worker
const worker = new Worker('/worker.js');
worker.postMessage(data);
worker.onmessage = (e) => {
  const results = e.data;
};
```

#### 2. Debounce/Throttle Event Handlers
```typescript
// Bad: Handler runs on every keystroke
input.addEventListener('keyup', (e) => {
  search(e.target.value);  // API call on every key
});

// Good: Debounce (wait for pause)
import { debounce } from 'lodash';

input.addEventListener('keyup', debounce((e) => {
  search(e.target.value);
}, 300));
```

#### 3. Optimize React Rendering
```typescript
// Bad: Unnecessary re-renders
function ParentComponent() {
  const [count, setCount] = useState(0);

  return (
    <>
      <button onClick={() => setCount(count + 1)}>Increment</button>
      <ExpensiveChild data={data} />  {/* Re-renders on every count change */}
    </>
  );
}

// Good: Memoization
const ExpensiveChild = React.memo(({ data }) => {
  // Only re-renders when data changes
  return <div>{/* ... */}</div>;
});
```

#### 4. Code Splitting
```typescript
// Bad: Load everything upfront
import { Chart } from './Chart';
import { Dashboard } from './Dashboard';

// Good: Lazy load on interaction
const Chart = lazy(() => import('./Chart'));

function App() {
  const [showChart, setShowChart] = useState(false);

  return (
    <>
      <button onClick={() => setShowChart(true)}>Show Chart</button>
      {showChart && <Suspense fallback={<div>Loading...</div>}><Chart /></Suspense>}
    </>
  );
}
```

### CLS (Cumulative Layout Shift)

**Definition:** Sum of unexpected layout shifts during page lifecycle.

**Targets:**
- **Good:** < 0.1
- **Needs Improvement:** 0.1 - 0.25
- **Poor:** > 0.25

**Optimization techniques:**

#### 1. Reserve Space for Images/Videos
```html
<!-- Bad: No dimensions (causes layout shift) -->
<img src="/image.jpg" alt="Image" />

<!-- Good: Reserve space -->
<img src="/image.jpg" alt="Image" width="640" height="360" />

<!-- Or use aspect-ratio CSS -->
<style>
  img {
    aspect-ratio: 16 / 9;
    width: 100%;
    height: auto;
  }
</style>
```

#### 2. Reserve Space for Ads/Embeds
```html
<!-- Reserve space for ad slot -->
<div style="min-height: 250px;">
  <!-- Ad code here -->
</div>
```

#### 3. Avoid Inserting Content Above Existing Content
```typescript
// Bad: Insert at top (shifts content down)
container.insertBefore(newElement, container.firstChild);

// Good: Append at bottom (no shift)
container.appendChild(newElement);

// Or: Use position: absolute to overlay
```

#### 4. Preload Fonts
```html
<!-- Prevent FOIT (Flash of Invisible Text) -->
<link rel="preload" as="font" href="/fonts/main.woff2" type="font/woff2" crossorigin />

<style>
  @font-face {
    font-family: 'CustomFont';
    src: url('/fonts/main.woff2') format('woff2');
    font-display: swap; /* Show fallback font while loading */
  }
</style>
```

---

## Bundle Optimization

### Code Splitting

**Techniques:**

#### 1. Route-Based Splitting
```typescript
// React Router with lazy loading
import { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

const Home = lazy(() => import('./pages/Home'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<div>Loading...</div>}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
```

#### 2. Vendor Splitting
```javascript
// webpack.config.js
module.exports = {
  optimization: {
    splitChunks: {
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all',
        },
      },
    },
  },
};
```

#### 3. Component-Level Splitting
```typescript
// Load heavy component on interaction
const HeavyChart = lazy(() => import('./HeavyChart'));

function Dashboard() {
  const [showChart, setShowChart] = useState(false);

  return (
    <>
      <button onClick={() => setShowChart(true)}>Show Chart</button>
      {showChart && (
        <Suspense fallback={<Spinner />}>
          <HeavyChart />
        </Suspense>
      )}
    </>
  );
}
```

### Tree Shaking

Remove unused code from bundles.

```typescript
// Bad: Imports entire library
import _ from 'lodash';
const result = _.debounce(fn, 300);

// Good: Import only what's needed
import debounce from 'lodash/debounce';
const result = debounce(fn, 300);

// Best: Use ES modules (automatic tree shaking)
import { debounce } from 'lodash-es';
```

### Minification and Compression

```javascript
// webpack.config.js
const TerserPlugin = require('terser-webpack-plugin');
const CompressionPlugin = require('compression-webpack-plugin');

module.exports = {
  optimization: {
    minimize: true,
    minimizer: [new TerserPlugin()],
  },
  plugins: [
    new CompressionPlugin({
      algorithm: 'brotliCompress',  // Better than gzip
      test: /\.(js|css|html|svg)$/,
    }),
  ],
};
```

---

## Image Optimization

### Modern Formats

**Format comparison:**

| Format | Compression | Browser Support | Use Case |
|--------|-------------|-----------------|----------|
| AVIF | Excellent (50% smaller than JPEG) | Modern browsers | Best quality/size |
| WebP | Very Good (30% smaller than JPEG) | Wide support | Fallback for AVIF |
| JPEG | Good | Universal | Legacy fallback |
| PNG | Lossless | Universal | Transparency, graphics |
| SVG | Text-based | Universal | Icons, logos |

**Progressive enhancement:**
```html
<picture>
  <source srcset="/image.avif" type="image/avif" />
  <source srcset="/image.webp" type="image/webp" />
  <img src="/image.jpg" alt="Image" loading="lazy" />
</picture>
```

### Responsive Images

```html
<!-- Responsive based on viewport width -->
<img
  srcset="
    /image-320w.jpg 320w,
    /image-640w.jpg 640w,
    /image-1280w.jpg 1280w
  "
  sizes="
    (max-width: 640px) 100vw,
    (max-width: 1280px) 50vw,
    640px
  "
  src="/image-640w.jpg"
  alt="Responsive image"
/>

<!-- Art direction (different crops) -->
<picture>
  <source media="(max-width: 640px)" srcset="/image-square.jpg" />
  <source media="(max-width: 1280px)" srcset="/image-landscape.jpg" />
  <img src="/image-wide.jpg" alt="Art direction" />
</picture>
```

### Lazy Loading

```html
<!-- Native lazy loading -->
<img src="/image.jpg" alt="Image" loading="lazy" />

<!-- Intersection Observer (custom)  -->
<script>
const images = document.querySelectorAll('img[data-src]');
const imageObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      imageObserver.unobserve(img);
    }
  });
});

images.forEach(img => imageObserver.observe(img));
</script>
```

### Image CDN

```typescript
// Use image CDN for transformations
// Cloudinary, Imgix, Cloudflare Images

const imageUrl = (src: string, width: number) =>
  `https://cdn.example.com/image/fetch/w_${width},f_auto,q_auto/${src}`;

// Usage
<img src={imageUrl('/original.jpg', 640)} alt="Optimized" />
```

---

## Resource Loading

### Preload Critical Resources

```html
<!-- Preload LCP image (high priority) -->
<link rel="preload" as="image" href="/hero.jpg" />

<!-- Preload critical fonts -->
<link rel="preload" as="font" href="/fonts/main.woff2" type="font/woff2" crossorigin />

<!-- Preload critical JavaScript -->
<link rel="preload" as="script" href="/critical.js" />
```

### Preconnect to External Domains

```html
<!-- Preconnect to external API (DNS + TCP + TLS) -->
<link rel="preconnect" href="https://api.example.com" />

<!-- Prefetch DNS only (lower priority) -->
<link rel="dns-prefetch" href="https://analytics.example.com" />
```

### Prefetch Next Pages

```html
<!-- Prefetch likely next page (on hover) -->
<script>
document.querySelectorAll('a').forEach(link => {
  link.addEventListener('mouseenter', () => {
    const url = link.href;
    const prefetch = document.createElement('link');
    prefetch.rel = 'prefetch';
    prefetch.href = url;
    document.head.appendChild(prefetch);
  });
});
</script>
```

### Resource Hints Summary

| Hint | Purpose | When to Use |
|------|---------|-------------|
| `preload` | High-priority fetch | Critical resources needed immediately |
| `preconnect` | Establish connection | External domains used soon |
| `dns-prefetch` | Resolve DNS | External domains used later |
| `prefetch` | Low-priority fetch | Resources for next navigation |
| `prerender` | Pre-render page | Very likely next page (careful!) |

---

## Rendering Performance

### Avoid Layout Thrashing

**Problem:** Reading layout properties triggers reflow.

```typescript
// Bad: Layout thrashing (forced reflow on every iteration)
for (let i = 0; i < elements.length; i++) {
  const height = elements[i].offsetHeight;  // Read (triggers reflow)
  elements[i].style.height = (height + 10) + 'px';  // Write
}

// Good: Batch reads then writes
const heights = elements.map(el => el.offsetHeight);  // Read all
heights.forEach((height, i) => {
  elements[i].style.height = (height + 10) + 'px';  // Write all
});
```

### Use CSS Transforms

```css
/* Bad: Triggers layout */
.element {
  position: absolute;
  left: 100px;
  top: 100px;
}

/* Good: Compositing only (GPU-accelerated) */
.element {
  transform: translate(100px, 100px);
  will-change: transform;
}
```

### Virtualize Long Lists

```typescript
// React Virtual (for long lists)
import { useVirtual } from 'react-virtual';

function VirtualList({ items }) {
  const parentRef = useRef();

  const rowVirtualizer = useVirtual({
    size: items.length,
    parentRef,
    estimateSize: useCallback(() => 50, []),
  });

  return (
    <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
      <div style={{ height: `${rowVirtualizer.totalSize}px` }}>
        {rowVirtualizer.virtualItems.map(virtualRow => (
          <div
            key={virtualRow.index}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              transform: `translateY(${virtualRow.start}px)`,
            }}
          >
            {items[virtualRow.index]}
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## Measurement Tools

### Lighthouse

**CLI:**
```bash
npm install -g lighthouse

# Run audit
lighthouse https://example.com --view

# With performance budget
lighthouse https://example.com --budget-path=./budget.json
```

**Budget (budget.json):**
```json
[
  {
    "path": "/*",
    "resourceSizes": [
      { "resourceType": "script", "budget": 300 },
      { "resourceType": "image", "budget": 500 },
      { "resourceType": "total", "budget": 1000 }
    ],
    "resourceCounts": [
      { "resourceType": "third-party", "budget": 10 }
    ]
  }
]
```

### WebPageTest

```bash
# CLI
npm install -g webpagetest

# Run test
webpagetest test https://example.com --location Dulles:Chrome --runs 3

# Output: Waterfall, filmstrip, metrics
```

### Chrome User Experience Report (CrUX)

```bash
# Query field data from real users
curl "https://chromeuxreport.googleapis.com/v1/records:queryRecord" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### Performance Observer API

```typescript
// Monitor Core Web Vitals in production
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

getCLS(console.log);
getFID(console.log);
getFCP(console.log);
getLCP(console.log);
getTTFB(console.log);

// Send to analytics
function sendToAnalytics(metric) {
  fetch('/analytics', {
    method: 'POST',
    body: JSON.stringify(metric),
  });
}

getCLS(sendToAnalytics);
getLCP(sendToAnalytics);
```

---

## Frontend Performance Checklist

### Loading Performance
- [ ] LCP < 2.5s
- [ ] TTFB < 600ms
- [ ] Preload critical resources (fonts, LCP image)
- [ ] Use CDN for static assets
- [ ] Enable HTTP/2 or HTTP/3
- [ ] Implement code splitting (route-based, vendor)
- [ ] Optimize images (modern formats, responsive, lazy loading)
- [ ] Minify and compress assets (brotli)

### Interactivity
- [ ] INP < 200ms
- [ ] Debounce/throttle event handlers
- [ ] Use Web Workers for heavy computation
- [ ] Optimize React rendering (memoization, virtualization)
- [ ] Lazy load non-critical components

### Visual Stability
- [ ] CLS < 0.1
- [ ] Reserve space for images/videos (width/height)
- [ ] Reserve space for ads/embeds
- [ ] Preload fonts (prevent FOIT)
- [ ] Avoid inserting content above existing content

### Measurement
- [ ] Set up Lighthouse CI
- [ ] Monitor Core Web Vitals in production (RUM)
- [ ] Define performance budgets
- [ ] Track trends over time
