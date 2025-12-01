# AI-Assisted Component Library: Media & File Management
## Master Plan for Media Component Skill

**Document Version:** 1.0
**Date:** November 13, 2025

---

## Executive Summary

Media components handle images, videos, audio, documents, and file management. This skill covers upload patterns, galleries, players, viewers, and optimization strategies.

---

## Component Taxonomy

### File Upload

**Drag & Drop Uploader**
- Drag zone with visual feedback
- Click to browse fallback
- Multiple file support
- Progress bars per file
- Preview thumbnails
- Cancel uploads

**Image Uploader**
- Image preview
- Crop/rotate tools
- Size/format validation
- Client-side resize (optimization)
- Alt text input (accessibility)

**Advanced Features**
- Paste from clipboard
- Camera capture (mobile)
- Resumable uploads (large files)
- Chunked uploads
- Cloud storage integration

---

### Image Display

**Image Gallery**
- Grid or masonry layout
- Lazy loading
- Lightbox on click
- Zoom and pan
- Captions
- Keyboard navigation (←→ arrows)

**Carousel/Slider**
- Auto-play (optional, pausable)
- Dots or thumbnails navigation
- Swipe on touch devices
- Accessible (ARIA roles)

**Image Optimization**
- Responsive images (`srcset`)
- WebP with fallback
- Progressive JPEGs
- Blur-up placeholders
- CDN integration

---

### Video Components

**Video Player**
- Custom controls or native
- Play/pause, volume, fullscreen
- Captions/subtitles (VTT)
- Playback speed
- Picture-in-picture
- Keyboard shortcuts

**Video Optimization**
- Adaptive streaming (HLS, DASH)
- Thumbnail preview on hover
- Lazy loading
- Preload strategies

---

### Audio Components

**Audio Player**
- Play/pause, seek, volume
- Waveform visualization
- Playlist support
- Download option
- Speed control

---

### Document Viewers

**PDF Viewer**
- Page navigation
- Zoom in/out
- Search text
- Download/print
- Thumbnail sidebar

**Office Document Preview**
- DOCX, XLSX, PPTX preview
- Read-only or editable
- Collaboration features
- Version history

---

## Performance & Optimization

**Image Optimization:**
- Compress before upload
- Generate thumbnails
- Responsive srcset
- WebP conversion
- CDN delivery

**Video Optimization:**
- Transcode to multiple qualities
- Adaptive bitrate streaming
- CDN with edge caching
- Lazy load off-screen videos

**File Size Limits:**
- Validate client-side first
- Clear error messages
- Suggest compression tools
- Progressive upload for large files

---

## Accessibility

**Images:**
- Alt text required
- Empty alt for decorative
- Figure/figcaption for context

**Videos:**
- Captions/subtitles
- Transcript link
- Keyboard controls
- Pause auto-play

**Audio:**
- Transcripts available
- Visual indicators (playing, paused)
- Keyboard controls

---

## Skill Structure

```yaml
---
name: media-file-management
description: Component library for media and file management. Covers file upload (drag-drop, multi-file, resumable), image galleries (lightbox, carousel, masonry), video players (custom controls, captions, adaptive streaming), audio players (waveform, playlists), document viewers (PDF, Office), and optimization strategies (compression, responsive images, lazy loading, CDN).
---
```

---

## Styling & Theming

### Design Token Integration

All media and file management components use the **design-tokens** skill for visual styling, enabling consistent design, theme switching, and brand customization.

**See:** `skills/design-tokens/` for complete theming documentation.

### Token Categories Used

**Color Tokens:**
- `--upload-zone-border` - Upload area border
- `--upload-zone-bg` - Upload area background
- `--upload-zone-border-active` - Border when dragging files
- `--upload-zone-bg-active` - Background when dragging
- `--image-overlay-bg` - Image gallery overlay
- `--video-player-bg` - Video player background
- `--video-controls-bg` - Video control bar background
- `--progress-bar-bg` - Upload progress background
- `--progress-bar-fill` - Upload progress fill

**Spacing Tokens:**
- `--upload-zone-padding` - Upload area padding
- `--gallery-gap` - Space between gallery images
- `--thumbnail-size` - Thumbnail dimensions
- `--player-padding` - Video/audio player padding

**Border & Radius:**
- `--image-border-radius` - Image corner radius
- `--upload-zone-border-radius` - Upload area corners
- `--video-border-radius` - Video player corners

**Shadow Tokens:**
- `--image-shadow` - Image elevation
- `--upload-zone-shadow` - Upload area shadow
- `--lightbox-shadow` - Lightbox modal shadow

### Component-Specific Tokens

```css
/* File Upload */
--upload-zone-border: 2px dashed var(--color-border);
--upload-zone-bg: var(--color-bg-secondary);
--upload-zone-border-active: 2px solid var(--color-primary);
--upload-zone-bg-active: var(--color-primary-50);
--upload-zone-padding: var(--spacing-xl);
--upload-zone-border-radius: var(--radius-lg);

/* Image Gallery */
--gallery-gap: var(--spacing-md);
--image-border-radius: var(--radius-md);
--image-shadow: var(--shadow-md);
--thumbnail-size: 120px;
--image-overlay-bg: rgba(0, 0, 0, 0.7);

/* Video Player */
--video-player-bg: var(--color-black);
--video-controls-bg: rgba(0, 0, 0, 0.7);
--video-border-radius: var(--radius-md);
--player-padding: 0;

/* Progress Indicators */
--progress-bar-bg: var(--color-gray-200);
--progress-bar-fill: var(--color-primary);
--progress-bar-height: 4px;
```

### Theme Support

- ✅ **Light Mode** - Clean image/video presentation
- ✅ **Dark Mode** - Reduced glare for media viewing
- ✅ **High Contrast** - Clear upload zone boundaries
- ✅ **Custom Brand Themes** - Brand-colored progress bars and controls

### Accessibility via Tokens

- **High Contrast Mode**: Strong upload zone borders
- **Focus Indicators**: Visible focus on media controls
- **Keyboard Navigation**: Token-styled interactive elements
- **Reduced Motion**: Disable carousel auto-play animations

---

## Before Implementation: Library Validation

**Optional but Recommended:** Before implementing, see `../RESEARCH_GUIDE.md` for methodology to validate library recommendations.

---

## Recommended Libraries & Tools

### **Image Gallery: react-image-gallery** (Full-Featured)

**Library:** `/xiaolin/react-image-gallery`
**Trust Score:** 8.6/10
**Code Snippets:** 11+

**Features:** Mobile swipe, fullscreen, thumbnails, lazy loading, responsive

**Alternative: LightGallery** (Trust: 9.6/10, Snippets: 429+) - More features, larger bundle

**Installation:**
```bash
npm install react-image-gallery
```

**Lazy Loading:** Use native `loading="lazy"` attribute or react-lazyload

---

**END OF MASTER PLAN**
