# Video Optimization Guide

Compress, transcode, and deliver video efficiently with adaptive streaming and CDN integration.

## Video Formats

| Format | Use Case | Browser Support | Compression |
|--------|----------|-----------------|-------------|
| **MP4 (H.264)** | Universal | 100% | Baseline |
| **WebM (VP9)** | Better compression | 95%+ | 20% smaller |
| **MP4 (H.265/HEVC)** | Best quality | Safari only | 40% smaller |

## Adaptive Streaming (HLS/DASH)

```html
<!-- HLS (Apple) -->
<video controls>
  <source src="video.m3u8" type="application/x-mpegURL" />
</video>

<!-- Use Video.js or HLS.js for broader support -->
```

## Transcoding with FFmpeg

```bash
# Convert to H.264 MP4
ffmpeg -i input.mov -c:v libx264 -crf 23 -c:a aac -b:a 128k output.mp4

# Create multiple quality levels
ffmpeg -i input.mov -c:v libx264 -b:v 5000k -s 1920x1080 1080p.mp4
ffmpeg -i input.mov -c:v libx264 -b:v 2500k -s 1280x720 720p.mp4
ffmpeg -i input.mov -c:v libx264 -b:v 1000k -s 854x480 480p.mp4
```

## Cloudflare Stream

```tsx
<iframe
  src={`https://iframe.cloudflare.com/${VIDEO_ID}`}
  allow="accelerometer; gyroscope; autoplay; encrypted-media; picture-in-picture"
  allowFullScreen
/>
```

## Mux Video

```tsx
import MuxPlayer from '@mux/mux-player-react';

<MuxPlayer
  playbackId="PLAYBACK_ID"
  metadata={{
    video_title: "My Video",
    viewer_user_id: "user-123"
  }}
  streamType="on-demand"
  autoPlay={false}
/>
```

## Best Practices

1. **Multiple resolutions** - 1080p, 720p, 480p
2. **Adaptive streaming** - HLS/DASH for quality switching
3. **CDN delivery** - Reduce origin load
4. **Lazy loading** - Below-the-fold videos
5. **Poster image** - Thumbnail while loading
6. **Preload metadata** - Not full video
7. **Compression** - CRF 23 for H.264

## Resources

- FFmpeg: https://ffmpeg.org/
- Video.js: https://videojs.com/
- Mux: https://www.mux.com/
