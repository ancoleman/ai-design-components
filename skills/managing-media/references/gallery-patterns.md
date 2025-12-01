# Image Gallery Patterns

## Grid Gallery

### CSS Grid Layout
```css
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--gallery-gap);
}
```

### Features
- Responsive columns
- Lazy loading
- Click to lightbox
- Keyboard navigation

## Masonry Layout

### Pinterest-Style
- Variable height items
- Optimal packing
- Libraries: Masonry.js, react-masonry-css

### Implementation Considerations
- More complex than grid
- Better for varied aspect ratios
- Performance impact with many images

## Lightbox

### Core Features
- Overlay background
- Full-size image display
- Previous/next navigation
- Zoom and pan
- Close on ESC or click outside

### Accessibility
- Focus trap within lightbox
- Arrow key navigation
- ESC to close
- Keyboard accessible controls

## Lazy Loading

### Native Lazy Loading
```html
<img src="image.jpg" loading="lazy" alt="Description" />
```

### Intersection Observer
For more control:
```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      observer.unobserve(img);
    }
  });
});
```

## Responsive Images

### Srcset and Sizes
```html
<img
  src="image-800.jpg"
  srcset="
    image-400.jpg 400w,
    image-800.jpg 800w,
    image-1200.jpg 1200w
  "
  sizes="(max-width: 600px) 100vw, (max-width: 1200px) 50vw, 33vw"
  alt="Description"
/>
```

## Performance Optimization

- Load thumbnails first
- Lazy load off-screen images
- Use WebP with JPG fallback
- Preload next/previous in lightbox
- Limit initial gallery size

## See Also
- `carousel-patterns.md` - Carousel implementations
- `image-optimization.md` - Image optimization strategies
- `accessibility-images.md` - Image accessibility
