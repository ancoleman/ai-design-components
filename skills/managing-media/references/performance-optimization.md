# Media Performance Optimization

## Image Optimization

### File Formats

**Modern Formats:**
- **WebP**: 25-35% smaller than JPEG, excellent browser support
- **AVIF**: 50% smaller than JPEG, growing support
- **JPEG**: Universal fallback

**Strategy:**
```html
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="Description">
</picture>
```

### Responsive Images

**Srcset for Resolution:**
```html
<img
  src="image-800.jpg"
  srcset="image-400.jpg 400w, image-800.jpg 800w, image-1200.jpg 1200w"
  sizes="(max-width: 600px) 100vw, 50vw"
  alt="Description"
>
```

### Compression

**Guidelines:**
- JPEG: 80-85% quality for photos
- PNG: Use tools like pngquant
- WebP: 80% quality for photos, lossless for graphics

**Automated Optimization:**
```bash
python scripts/optimize_images.py --input images/ --quality 80 --formats webp,jpg
```

### Lazy Loading

**Native:**
```html
<img src="image.jpg" loading="lazy" alt="Description">
```

**Intersection Observer (more control):**
```javascript
const imgObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      imgObserver.unobserve(img);
    }
  });
});
```

### Placeholders

**Blur-up Technique:**
1. Show tiny blurred image (< 1KB)
2. Load full image in background
3. Fade in when loaded

**Skeleton Screens:**
```css
.image-skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}
```

## Video Optimization

### Encoding

**Recommended Settings:**
- **Resolution**: 1080p, 720p, 480p, 360p
- **Codec**: H.264 (compatibility), H.265 (efficiency)
- **Bitrate**:
  - 1080p: 8 Mbps
  - 720p: 5 Mbps
  - 480p: 2.5 Mbps

### Adaptive Streaming

**HLS (HTTP Live Streaming):**
- Multiple quality levels
- Automatic quality switching
- Works on all devices

**Implementation:**
```javascript
import videojs from 'video.js';

const player = videojs('video', {
  sources: [{
    src: 'video.m3u8',
    type: 'application/x-mpegURL'
  }]
});
```

### Preload Strategies

**None (recommended):**
```html
<video preload="none" poster="thumbnail.jpg">
```
- Loads nothing until user clicks play
- Best for bandwidth

**Metadata:**
```html
<video preload="metadata">
```
- Loads duration and dimensions
- Good compromise

**Auto:**
```html
<video preload="auto">
```
- Loads entire video
- Use only when autoplay expected

### Poster Images

Always provide:
```html
<video poster="thumbnail.jpg">
```
- Shows before play
- Reduces perceived load time
- Use optimized JPEG (< 100KB)

## Audio Optimization

### Formats

**MP3**: Universal support, good compression
**AAC**: Better quality at same bitrate
**Opus**: Best compression, growing support

**Strategy:**
```html
<audio>
  <source src="audio.opus" type="audio/opus">
  <source src="audio.mp3" type="audio/mpeg">
</audio>
```

### Bitrate

- Podcast/Voice: 64-96 kbps
- Music: 128-192 kbps
- High-quality music: 256-320 kbps

## Document Optimization

### PDF

**Compression:**
- Optimize images in PDF
- Remove unnecessary metadata
- Use PDF/A for archival

**Lazy Loading:**
```javascript
// Load PDF page by page
const loadPage = (pageNum) => {
  return pdf.getPage(pageNum).then(page => {
    // Render only when needed
  });
};
```

## CDN Integration

### Benefits
- Edge caching (lower latency)
- Automatic compression
- Format negotiation
- Resize on demand

### Popular CDNs
- **Cloudinary**: Image/video optimization, transformations
- **Imgix**: Real-time image processing
- **CloudFront**: AWS CDN with S3
- **Fastly**: High-performance edge

### Example (Cloudinary):
```html
<img src="https://res.cloudinary.com/demo/image/upload/w_400,f_auto,q_auto/sample.jpg">
```
- `w_400`: Resize to 400px
- `f_auto`: Auto format (WebP if supported)
- `q_auto`: Auto quality

## Performance Budgets

### Target Metrics

**Images:**
- Total page images: < 1MB
- Hero image: < 200KB
- Thumbnails: < 30KB each
- LCP (Largest Contentful Paint): < 2.5s

**Video:**
- Initial load: < 100KB (poster only)
- First frame: < 3s
- Buffering: < 1s between segments

**Documents:**
- PDF first page: < 2s
- Full document: Progressive loading

## Monitoring

### Core Web Vitals

**LCP (Largest Contentful Paint):**
- Good: < 2.5s
- Needs improvement: 2.5-4s
- Poor: > 4s

**CLS (Cumulative Layout Shift):**
- Specify image dimensions
- Reserve space for lazy-loaded content

**FID (First Input Delay):**
- Minimize main thread blocking
- Use web workers for processing

### Testing Tools

```bash
# Analyze media performance
node scripts/analyze_media_performance.js --files images/*.jpg

# Generate performance report
python scripts/performance_report.py --output report.html
```

## Best Practices Checklist

### Images
- [ ] Use modern formats (WebP, AVIF) with fallbacks
- [ ] Implement responsive images (srcset)
- [ ] Lazy load below-the-fold images
- [ ] Compress images (80-85% quality)
- [ ] Serve via CDN
- [ ] Specify width/height to prevent CLS

### Video
- [ ] Use adaptive streaming (HLS/DASH)
- [ ] Provide multiple quality levels
- [ ] Set preload="none" or "metadata"
- [ ] Include poster image
- [ ] Compress and optimize encoding
- [ ] Serve via CDN with edge caching

### Audio
- [ ] Use appropriate bitrate
- [ ] Provide multiple formats
- [ ] Lazy load if not immediately needed
- [ ] Show loading state

### Documents
- [ ] Compress PDFs
- [ ] Load pages on demand
- [ ] Optimize embedded images
- [ ] Provide download option

## See Also
- `image-optimization.md` - Image-specific optimization
- `video-optimization.md` - Video-specific optimization
- `cloud-storage.md` - CDN and cloud integration
