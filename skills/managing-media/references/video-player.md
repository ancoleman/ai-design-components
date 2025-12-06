# Video Player Implementation


## Table of Contents

- [Native HTML5 Video](#native-html5-video)
  - [Basic Implementation](#basic-implementation)
  - [Attributes](#attributes)
- [Custom Controls](#custom-controls)
  - [Why Custom Controls?](#why-custom-controls)
  - [Implementation with video.js](#implementation-with-videojs)
- [Captions and Subtitles](#captions-and-subtitles)
  - [VTT Format](#vtt-format)
  - [Implementation](#implementation)
- [Adaptive Streaming](#adaptive-streaming)
  - [HLS (HTTP Live Streaming)](#hls-http-live-streaming)
  - [DASH (Dynamic Adaptive Streaming)](#dash-dynamic-adaptive-streaming)
  - [Implementation](#implementation)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Picture-in-Picture](#picture-in-picture)
  - [API](#api)
- [Accessibility](#accessibility)
  - [Requirements](#requirements)
  - [ARIA](#aria)
- [Performance Optimization](#performance-optimization)
- [See Also](#see-also)

## Native HTML5 Video

### Basic Implementation
```html
<video controls poster="thumbnail.jpg">
  <source src="video.mp4" type="video/mp4">
  <source src="video.webm" type="video/webm">
  <track kind="captions" src="captions-en.vtt" srclang="en" label="English">
</video>
```

### Attributes
- `controls` - Show native controls
- `poster` - Thumbnail before play
- `preload` - `none`, `metadata`, `auto`
- `autoplay` - Auto-play (avoid for accessibility)
- `loop` - Loop playback
- `muted` - Start muted (required for autoplay)

## Custom Controls

### Why Custom Controls?
- Consistent UI across browsers
- Brand styling
- Advanced features
- Better accessibility

### Implementation with video.js
```javascript
import videojs from 'video.js';

const player = videojs('my-video', {
  controls: true,
  fluid: true,
  playbackRates: [0.5, 1, 1.5, 2],
  plugins: {
    // Add plugins here
  }
});
```

## Captions and Subtitles

### VTT Format
```
WEBVTT

00:00:00.000 --> 00:00:02.000
Hello, welcome to the video.

00:00:02.000 --> 00:00:05.000
This is a subtitle example.
```

### Implementation
```html
<track
  kind="captions"
  src="captions-en.vtt"
  srclang="en"
  label="English"
  default
>
```

## Adaptive Streaming

### HLS (HTTP Live Streaming)
- Apple standard
- Widely supported
- Multiple quality levels

### DASH (Dynamic Adaptive Streaming)
- Industry standard
- Better compression
- DRM support

### Implementation
Both supported by video.js with plugins.

## Keyboard Shortcuts

Essential shortcuts:
- **Space/K** - Play/pause
- **←/→** - Seek backward/forward
- **↑/↓** - Volume up/down
- **M** - Mute/unmute
- **F** - Fullscreen
- **C** - Toggle captions

## Picture-in-Picture

### API
```javascript
if (document.pictureInPictureEnabled) {
  video.requestPictureInPicture();
}
```

## Accessibility

### Requirements
- Captions for all speech
- Transcript available
- Keyboard controls
- Pause auto-play
- Audio description track

### ARIA
```html
<div role="region" aria-label="Video player">
  <video>...</video>
</div>
```

## Performance Optimization

- Use `preload="metadata"` by default
- Lazy load off-screen videos
- Provide poster image
- Compress and transcode
- Use CDN for delivery

## See Also
- `video-optimization.md` - Performance strategies
- `accessibility-video.md` - Video accessibility
- `cloud-storage.md` - Video hosting
