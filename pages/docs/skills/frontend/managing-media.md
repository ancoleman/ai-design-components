---
sidebar_position: 13
title: Managing Media
description: Media and file management with upload, galleries, video/audio players, and optimization
tags: [frontend, media, upload, gallery, video, audio]
---

# Managing Media & Files

Systematic patterns for implementing media and file management components across all formats (images, videos, audio, documents).

## When to Use

Use this skill when:
- Implementing file upload (single, multiple, drag-and-drop)
- Building image galleries, carousels, or lightboxes
- Creating video or audio players
- Displaying PDF or document viewers
- Optimizing media for performance (responsive images, lazy loading)
- Handling large file uploads (chunked, resumable)
- Integrating cloud storage (S3, Cloudinary)
- Implementing media accessibility (alt text, captions, transcripts)
- Designing empty states for missing media

## Quick Decision Framework

Select implementation based on media type and requirements:

```text
Images                  → Gallery pattern + lazy loading + responsive srcset
Videos                  → Player with controls + captions + adaptive streaming
Audio                   → Player with waveform + playlist support
Documents (PDF)         → Viewer with navigation + search + download
File Upload (small)     → Basic drag-drop with preview
File Upload (large)     → Chunked upload with progress + resume
Multiple Files          → Queue management + parallel uploads
```

## File Upload Patterns

### Basic Upload (Under 10MB)

For small files with simple requirements:
- Drag-and-drop zone with visual feedback
- Click to browse fallback
- File type and size validation
- Preview thumbnails for images
- Progress indicator

### Advanced Upload (Over 10MB)

For large files requiring reliability:
- Chunked uploads (resume on failure)
- Parallel uploads for multiple files
- Upload queue management
- Cancel and retry controls
- Client-side compression

### Image-Specific Upload

For image files with editing requirements:
- Crop and rotate tools
- Client-side resize before upload
- Format conversion (PNG → WebP)
- Alt text input field (accessibility)

## Image Display Components

### Image Gallery

For collections of images:
- Grid or masonry layout
- Lazy loading (native or custom)
- Lightbox on click
- Zoom and pan controls
- Keyboard navigation (arrow keys)
- Responsive design

### Carousel/Slider

For sequential image display:
- Auto-play (optional, pausable for accessibility)
- Dot or thumbnail navigation
- Touch/swipe support
- ARIA roles for accessibility
- Infinite loop option

### Image Optimization

Essential optimization strategies:
- Responsive images using `srcset` and `sizes`
- Modern formats (WebP with JPG fallback)
- Progressive JPEGs
- Blur-up placeholders
- CDN integration

## Video Components

### Video Player

For custom video playback:
- Custom controls or native
- Play/pause, volume, fullscreen
- Captions/subtitles (VTT format)
- Playback speed control
- Picture-in-picture support
- Keyboard shortcuts

### Video Optimization

Performance strategies:
- Adaptive streaming (HLS, DASH)
- Thumbnail preview on hover
- Lazy loading off-screen videos
- Preload strategies (`metadata`, `auto`, `none`)
- Multiple quality levels

## Audio Components

### Audio Player

For audio playback:
- Play/pause, seek, volume controls
- Waveform visualization (optional)
- Playlist support
- Download option
- Playback speed control
- Visual indicators for accessibility

## Document Viewers

### PDF Viewer

For PDF document display:
- Page navigation (prev/next, jump to page)
- Zoom in/out controls
- Text search within document
- Download and print options
- Thumbnail sidebar

## Performance Optimization

### File Size Guidelines

Validate client-side before upload:
- Images: 5MB max recommended
- Videos: 100MB max for web
- Audio: 10MB max
- Documents: 25MB max

### Image Optimization Checklist

Strategies:
- Compress before upload (client or server)
- Generate multiple sizes (thumbnails, medium, large)
- Use responsive `srcset` for device targeting
- Convert to modern formats (WebP, AVIF)
- Serve via CDN with edge caching

## Accessibility Requirements

### Images

Essential patterns:
- Alt text required for meaningful images
- Empty alt (`alt=""`) for decorative images
- Use `<figure>` and `<figcaption>` for context
- Sufficient color contrast for overlays

### Videos

Essential patterns:
- Captions/subtitles for all speech
- Transcript link provided
- Keyboard controls (space, arrows, M for mute)
- Pause auto-play (WCAG requirement)
- Audio description track (if applicable)

### Audio

Essential patterns:
- Transcripts available
- Visual indicators (playing, paused, volume)
- Keyboard controls
- ARIA labels for controls

## Library Recommendations

### Image Gallery: react-image-gallery

Best for feature-complete galleries:
- Mobile swipe support
- Fullscreen mode
- Thumbnail navigation
- Lazy loading built-in

```bash
npm install react-image-gallery
```

### Video: video.js

Best for custom video players:
- Plugin ecosystem
- HLS and DASH support
- Accessible controls
- Theming support

```bash
npm install video.js
```

### Audio: wavesurfer.js

Best for waveform visualization:
- Beautiful waveform display
- Timeline interactions
- Plugin support
- Responsive

```bash
npm install wavesurfer.js
```

### PDF: react-pdf

Best for PDF rendering in React:
- Page-by-page rendering
- Text selection support
- Worker-based for performance

```bash
npm install react-pdf
```

## Cloud Storage Integration

### Client-Side Direct Upload

For AWS S3, Cloudinary, etc.:
1. Request signed URL from backend
2. Upload directly to cloud storage
3. Notify backend of completion
4. Display uploaded media

Benefits:
- Reduces server load
- Faster uploads (direct to CDN)
- No file size limits on your server

## Design Token Integration

All media components use the design-tokens skill for theming:
- Color tokens for backgrounds, overlays, controls
- Spacing tokens for padding and gaps
- Border tokens for thumbnails and containers
- Shadow tokens for elevation
- Motion tokens for animations

## Related Skills

- [Theming Components](./theming-components.md) - Media component styling
- [Building Forms](./building-forms.md) - File input fields and validation
- [Providing Feedback](./providing-feedback.md) - Upload progress indicators
- [Building AI Chat](./building-ai-chat.md) - Media attachments in chat

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/managing-media)
- Upload: `references/upload-patterns.md`, `references/advanced-upload.md`
- Display: `references/gallery-patterns.md`, `references/video-player.md`, `references/audio-player.md`
- Optimization: `references/image-optimization.md`, `references/performance-optimization.md`
- Cloud: `references/cloud-storage.md`
- Examples: `examples/basic-upload.tsx`, `examples/image-gallery.tsx`, `examples/video-player.tsx`
