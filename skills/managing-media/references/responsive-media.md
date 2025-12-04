# Responsive Media Patterns

Adaptive images and videos for different screen sizes and device capabilities.

## Responsive Images

### srcset and sizes

```html
<img
  src="fallback.jpg"
  srcset="small.jpg 480w, medium.jpg 800w, large.jpg 1200w"
  sizes="(max-width: 600px) 480px, (max-width: 1000px) 800px, 1200px"
  alt="Description"
/>
```

### Picture Element (Art Direction)

```html
<picture>
  <source media="(max-width: 600px)" srcset="mobile.jpg" />
  <source media="(max-width: 1200px)" srcset="tablet.jpg" />
  <img src="desktop.jpg" alt="Description" />
</picture>
```

## Responsive Video

```html
<video
  controls
  poster="thumbnail.jpg"
  preload="metadata"
>
  <source src="video-1080p.mp4" media="(min-width: 1200px)" />
  <source src="video-720p.mp4" media="(min-width: 800px)" />
  <source src="video-480p.mp4" />
</video>
```

## Aspect Ratio Container

```tsx
function AspectRatioBox({ ratio = 16/9, children }: Props) {
  return (
    <div style={{ position: 'relative', paddingBottom: `${(1 / ratio) * 100}%` }}>
      <div style={{ position: 'absolute', inset: 0 }}>
        {children}
      </div>
    </div>
  );
}

<AspectRatioBox ratio={16/9}>
  <img src="image.jpg" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
</AspectRatioBox>
```

## Best Practices

1. **srcset for resolution** - Serve appropriate size
2. **Picture for art direction** - Different crops per breakpoint
3. **Aspect ratio containers** - Prevent layout shift
4. **Object-fit** - cover, contain, fill
5. **Lazy loading** - Below-the-fold media

## Resources

- Responsive Images: https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images
