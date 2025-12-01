# Media Accessibility Patterns

## WCAG 2.1 Requirements for Media

### Level A (Minimum)
- Audio-only and video-only alternatives
- Captions for prerecorded video
- Audio descriptions or alternative
- Keyboard accessible controls

### Level AA (Recommended)
- Captions for live video
- Audio descriptions for prerecorded video
- Contrast ratios for overlays

### Level AAA (Enhanced)
- Sign language interpretation
- Extended audio descriptions
- Media alternative for text

## Images

### Alt Text Guidelines

**Informative Images:**
```html
<img src="chart.png" alt="Bar chart showing 40% increase in sales in Q4 2024">
```

**Decorative Images:**
```html
<img src="divider.png" alt="">
```

**Functional Images:**
```html
<img src="search-icon.png" alt="Search">
```

**Complex Images:**
```html
<figure>
  <img src="complex-chart.png" alt="Sales trends by region">
  <figcaption>
    Detailed description: The chart shows sales increasing in the North region...
  </figcaption>
</figure>
```

### Color Contrast

Overlays and text on images:
- Normal text: 4.5:1 minimum
- Large text (18pt+): 3:1 minimum
- Use semi-transparent backgrounds for text overlays

## Video

### Captions

**Requirements:**
- Synchronized with audio
- Identify speakers
- Include sound effects
- Readable font size
- High contrast

**VTT Format:**
```
WEBVTT

00:00:01.000 --> 00:00:04.000
[Music playing]

00:00:04.000 --> 00:00:08.000
<v John>Hello everyone, welcome to the tutorial.</v>
```

### Audio Descriptions

Describe visual content during natural pauses:
```
WEBVTT

00:00:10.000 --> 00:00:14.000
[Audio description: John points to the chart on screen]
```

### Transcripts

Provide full text alternative:
- All dialogue
- Sound effects
- Visual information
- Speaker identification

Example structure:
```
Video Transcript

[0:00] Background music plays
[0:04] John (on camera): "Hello everyone..."
[0:15] [Screen shows code editor]
```

### Keyboard Controls

Essential shortcuts:
- **Space** - Play/pause
- **←/→** - Rewind/forward
- **↑/↓** - Volume
- **M** - Mute
- **F** - Fullscreen
- **C** - Captions

### ARIA Attributes

```html
<div role="region" aria-label="Video player">
  <video id="main-video">...</video>
  <div role="group" aria-label="Playback controls">
    <button aria-label="Play">▶</button>
    <button aria-label="Pause">⏸</button>
    <button aria-label="Mute">🔇</button>
  </div>
</div>
```

## Audio

### Transcripts Required

Provide text alternative for all audio:
```html
<audio controls>
  <source src="podcast.mp3" type="audio/mpeg">
</audio>
<a href="podcast-transcript.html">View transcript</a>
```

### Visual Indicators

For deaf/hard of hearing:
- Visual play/pause state
- Waveform visualization
- Progress indicator
- Volume level display

### ARIA Labels

```html
<button
  aria-label="Play episode"
  aria-pressed="false"
>
  ▶
</button>
```

### Controls

- Large hit areas (44x44px minimum)
- Keyboard accessible
- Clear focus indicators
- Screen reader announcements

## File Upload

### Accessibility Requirements

**File Input:**
```html
<label for="file-upload">
  Choose files to upload
  <input
    type="file"
    id="file-upload"
    multiple
    aria-describedby="file-requirements"
  >
</label>
<div id="file-requirements">
  Maximum 10MB per file. Accepts JPG, PNG, WebP.
</div>
```

**Drag-and-Drop:**
```html
<div
  role="button"
  tabindex="0"
  aria-label="Drag and drop files or click to browse"
  class="upload-zone"
>
  <p>Drop files here or click to browse</p>
</div>
```

**Progress Announcements:**
```html
<div role="status" aria-live="polite">
  Uploading: 45% complete
</div>
```

**Error Messages:**
```html
<div role="alert" aria-live="assertive">
  Upload failed: File too large. Maximum size is 10MB.
</div>
```

## Image Galleries

### Keyboard Navigation

- **Arrow keys** - Navigate between images
- **Enter** - Open lightbox
- **ESC** - Close lightbox
- **Tab** - Navigate controls

### Focus Management

Lightbox pattern:
1. Save focus before opening
2. Move focus to first control
3. Trap focus within lightbox
4. Restore focus on close

### Screen Reader Support

```html
<figure>
  <img src="photo1.jpg" alt="Description">
  <figcaption>
    Image 1 of 24
  </figcaption>
</figure>
```

### ARIA Carousel

```html
<div
  role="region"
  aria-roledescription="carousel"
  aria-label="Image gallery"
>
  <div role="group" aria-roledescription="slide" aria-label="1 of 10">
    <img src="..." alt="...">
  </div>
</div>
```

## PDF Viewers

### Accessible PDFs

Ensure source PDFs are accessible:
- Tagged PDF structure
- Reading order defined
- Alt text for images
- Form labels
- Table headers

### Viewer Controls

- Keyboard navigation between pages
- Search function keyboard accessible
- Zoom controls accessible
- Download button labeled

### Screen Reader Announcements

```html
<div role="status" aria-live="polite">
  Page 5 of 42
</div>
```

## Testing Checklist

### Images
- [ ] Alt text provided for all meaningful images
- [ ] Empty alt for decorative images
- [ ] Complex images have long descriptions
- [ ] Text on images has sufficient contrast

### Video
- [ ] Captions available
- [ ] Audio descriptions provided (if needed)
- [ ] Transcript available
- [ ] Keyboard controls work
- [ ] No auto-play or can be paused

### Audio
- [ ] Transcript provided
- [ ] Visual playback indicators
- [ ] Keyboard controls
- [ ] ARIA labels on controls

### Upload
- [ ] File input labeled
- [ ] Drag-drop keyboard accessible
- [ ] Progress announced
- [ ] Errors announced
- [ ] Success confirmed

### Galleries
- [ ] Keyboard navigation works
- [ ] Focus managed in lightbox
- [ ] Current position announced
- [ ] Controls labeled

## Validation Tools

### Automated Testing
```bash
# Run accessibility validation
node scripts/validate_media_accessibility.js
```

### Manual Testing
- Keyboard-only navigation
- Screen reader testing (NVDA, JAWS, VoiceOver)
- High contrast mode
- Zoom to 200%

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM: Alternative Text](https://webaim.org/techniques/alttext/)
- [WebAIM: Captions](https://webaim.org/techniques/captions/)
- [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)

## See Also
- `accessibility-images.md` - Image-specific patterns
- `accessibility-video.md` - Video-specific patterns
- `accessibility-audio.md` - Audio-specific patterns
