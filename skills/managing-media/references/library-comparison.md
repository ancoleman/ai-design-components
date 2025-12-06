# Media Library Comparison


## Table of Contents

- [Image Galleries](#image-galleries)
  - [react-image-gallery](#react-image-gallery)
  - [LightGallery](#lightgallery)
  - [React Image Lightbox](#react-image-lightbox)
- [Video Players](#video-players)
  - [video.js](#videojs)
  - [Plyr](#plyr)
  - [ReactPlayer](#reactplayer)
- [Audio Players](#audio-players)
  - [wavesurfer.js](#wavesurferjs)
  - [Howler.js](#howlerjs)
  - [react-h5-audio-player](#react-h5-audio-player)
- [PDF Viewers](#pdf-viewers)
  - [react-pdf](#react-pdf)
  - [PDF.js (Mozilla)](#pdfjs-mozilla)
  - [Cloud Viewers](#cloud-viewers)
- [File Upload](#file-upload)
  - [react-dropzone](#react-dropzone)
  - [Uppy](#uppy)
  - [Filepond](#filepond)
- [Selection Guide](#selection-guide)
  - [Choose react-image-gallery when:](#choose-react-image-gallery-when)
  - [Choose video.js when:](#choose-videojs-when)
  - [Choose wavesurfer.js when:](#choose-wavesurferjs-when)
  - [Choose react-pdf when:](#choose-react-pdf-when)
  - [Choose react-dropzone when:](#choose-react-dropzone-when)
- [Performance Comparison](#performance-comparison)
- [Accessibility Comparison](#accessibility-comparison)
- [See Also](#see-also)

## Image Galleries

### react-image-gallery
**Trust Score:** 8.6/10
**Code Snippets:** 11+
**Bundle Size:** ~30KB

**Pros:**
- Feature complete out of the box
- Mobile swipe support
- Fullscreen mode
- Good documentation

**Cons:**
- Larger bundle size
- Less customization than headless

**Best For:** Complete gallery solution with minimal setup

---

### LightGallery
**Trust Score:** 9.6/10
**Code Snippets:** 429+

**Pros:**
- Extensive features
- Excellent documentation
- Plugin ecosystem
- Touch gestures

**Cons:**
- Large bundle size (~100KB+)
- Commercial license for some features

**Best For:** Feature-rich galleries, enterprises

---

### React Image Lightbox
**Bundle Size:** ~15KB

**Pros:**
- Lightweight
- Simple API
- Good keyboard support

**Cons:**
- Limited features
- Less active maintenance

**Best For:** Simple lightbox needs, small bundle

---

## Video Players

### video.js
**Trust Score:** 9.0+/10
**Community:** Very active

**Pros:**
- Industry standard
- Plugin ecosystem
- HLS/DASH support
- Excellent accessibility
- Free and open source

**Cons:**
- Larger learning curve
- More setup required

**Best For:** Professional video needs, streaming

---

### Plyr
**Bundle Size:** ~30KB

**Pros:**
- Beautiful default UI
- Simple setup
- Good accessibility
- Multiple providers (YouTube, Vimeo)

**Cons:**
- Less extensible than video.js
- Smaller community

**Best For:** Quick setup, embedded videos

---

### ReactPlayer
**Bundle Size:** ~64KB

**Pros:**
- Supports many sources
- React-first API
- Simple integration

**Cons:**
- Less customization
- Depends on external players

**Best For:** Multi-source video (YouTube, Vimeo, files)

---

## Audio Players

### wavesurfer.js
**Trust Score:** 8.5+/10

**Pros:**
- Beautiful waveforms
- Plugin support
- Responsive
- Good documentation

**Cons:**
- Performance with very long audio
- Setup complexity

**Best For:** Waveform visualization, music apps

---

### Howler.js
**Bundle Size:** ~9KB

**Pros:**
- Lightweight
- Audio sprite support
- Web Audio API
- Cross-browser

**Cons:**
- No built-in UI
- Manual waveform needed

**Best For:** Audio playback without UI, games

---

### react-h5-audio-player
**Bundle Size:** ~20KB

**Pros:**
- Ready-to-use UI
- Responsive
- Accessible
- Playlist support

**Cons:**
- Limited customization
- No waveform

**Best For:** Standard audio player with UI

---

## PDF Viewers

### react-pdf
**Trust Score:** 9.0+/10

**Pros:**
- Renders in browser
- Text selection
- Worker-based
- Customizable

**Cons:**
- Bundle size (~150KB)
- Setup complexity

**Best For:** Full-featured PDF rendering

---

### PDF.js (Mozilla)

**Pros:**
- Industry standard
- Complete feature set
- Free and open source

**Cons:**
- Large bundle
- Complex API

**Best For:** Advanced PDF needs

---

### Cloud Viewers
**Google Docs Viewer, Office Online**

**Pros:**
- No client-side processing
- Supports many formats
- No bundle impact

**Cons:**
- Requires internet
- Privacy concerns
- Less control

**Best For:** Simple preview, public documents

---

## File Upload

### react-dropzone
**Trust Score:** 9.0+/10

**Pros:**
- Headless (full control)
- Small bundle (~10KB)
- Excellent API
- Accessible

**Cons:**
- No UI provided
- Manual styling needed

**Best For:** Custom upload UI

---

### Uppy
**Trust Score:** 8.5+/10

**Pros:**
- Feature complete
- Beautiful UI
- Cloud integrations
- Resumable uploads

**Cons:**
- Large bundle (~100KB+)
- Complex for simple needs

**Best For:** Complex upload workflows

---

### Filepond
**Bundle Size:** ~30KB

**Pros:**
- Beautiful default UI
- Image optimization
- Plugin support
- Good UX

**Cons:**
- Less headless flexibility
- Commercial plugins

**Best For:** Quick beautiful uploads

---

## Selection Guide

### Choose react-image-gallery when:
- Need full-featured gallery quickly
- Mobile support is critical
- Bundle size <50KB acceptable

### Choose video.js when:
- Professional video requirements
- Need streaming (HLS/DASH)
- Accessibility is critical
- Plugin ecosystem valuable

### Choose wavesurfer.js when:
- Audio waveforms needed
- Music or podcast app
- Visual feedback important

### Choose react-pdf when:
- PDF rendering in browser
- Text selection needed
- Full customization required

### Choose react-dropzone when:
- Custom upload UI
- Small bundle critical
- Headless flexibility needed

## Performance Comparison

| Library | Type | Bundle Size | Load Time |
|---------|------|-------------|-----------|
| react-image-gallery | Image | ~30KB | Fast |
| video.js | Video | ~200KB | Medium |
| wavesurfer.js | Audio | ~80KB | Medium |
| react-pdf | PDF | ~150KB | Slow |
| react-dropzone | Upload | ~10KB | Fast |

## Accessibility Comparison

| Library | ARIA | Keyboard | Screen Reader |
|---------|------|----------|---------------|
| react-image-gallery | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| video.js | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| wavesurfer.js | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| react-pdf | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| react-dropzone | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

⭐⭐⭐⭐⭐ Excellent
⭐⭐⭐⭐ Good
⭐⭐⭐ Acceptable

## See Also
- `implementation-guide.md` - Selection framework
- `performance-optimization.md` - Performance strategies
- `accessibility-patterns.md` - Accessibility requirements
