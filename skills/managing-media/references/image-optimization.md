# Image Optimization Guide

Reduce file sizes and improve load times with responsive images, modern formats, and lazy loading.


## Table of Contents

- [Modern Image Formats](#modern-image-formats)
- [Responsive Images](#responsive-images)
- [Next.js Image Component](#nextjs-image-component)
- [Lazy Loading](#lazy-loading)
- [Client-Side Compression](#client-side-compression)
- [CDN Integration](#cdn-integration)
- [Best Practices](#best-practices)
- [Tools](#tools)

## Modern Image Formats

| Format | Use Case | Browser Support | Compression |
|--------|----------|-----------------|-------------|
| **WebP** | General purpose | 97%+ | 30% smaller than JPEG |
| **AVIF** | Best compression | 90%+ | 50% smaller than JPEG |
| **JPEG** | Fallback, photos | 100% | Baseline |
| **PNG** | Transparency, lossless | 100% | Large files |

## Responsive Images

```html
<img
  srcset="
    image-320.webp 320w,
    image-640.webp 640w,
    image-1280.webp 1280w
  "
  sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
  src="image-640.jpg"
  alt="Description"
/>
```

## Next.js Image Component

```tsx
import Image from 'next/image';

<Image
  src="/photos/sunset.jpg"
  alt="Sunset"
  width={800}
  height={600}
  quality={85}  // 0-100, default 75
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,..."
  loading="lazy"
/>
```

## Lazy Loading

```tsx
<img
  src="image.jpg"
  loading="lazy"  // Native lazy loading
  alt="Description"
/>
```

## Client-Side Compression

```tsx
async function optimizeImage(file: File): Promise<Blob> {
  const img = await createImageBitmap(file);
  const canvas = document.createElement('canvas');

  // Resize to max 1920px width
  const scale = Math.min(1, 1920 / img.width);
  canvas.width = img.width * scale;
  canvas.height = img.height * scale;

  const ctx = canvas.getContext('2d')!;
  ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

  return new Promise((resolve) => {
    canvas.toBlob((blob) => resolve(blob!), 'image/webp', 0.85);
  });
}
```

## CDN Integration

```tsx
// Cloudflare Images
const cloudflareUrl = (imageId: string, variant: string) =>
  `https://imagedelivery.net/${ACCOUNT_HASH}/${imageId}/${variant}`;

<img src={cloudflareUrl('img-id', 'public')} alt="..." />

// With transformations
<img src={cloudflareUrl('img-id', 'thumbnail')} alt="Thumbnail" />
```

## Best Practices

1. **Use WebP/AVIF** - 30-50% smaller than JPEG
2. **Responsive images** - srcset for different screen sizes
3. **Lazy loading** - Below-the-fold images
4. **Compress before upload** - Client-side optimization
5. **CDN delivery** - Global edge caching
6. **Placeholder** - Blur or solid color while loading
7. **Alt text** - Always include for accessibility
8. **Dimensions** - Prevent layout shift

## Tools

- Sharp (Node.js): https://sharp.pixelplumbing.com/
- ImageMagick: https://imagemagick.org/
- Cloudflare Images: https://developers.cloudflare.com/images/
