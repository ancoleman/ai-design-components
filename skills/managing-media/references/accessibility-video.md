# Video Accessibility

Captions, transcripts, audio descriptions, and keyboard controls for accessible video.

## Captions (Required)

```html
<video controls>
  <source src="video.mp4" type="video/mp4" />
  <track kind="captions" src="captions-en.vtt" srclang="en" label="English" default />
  <track kind="captions" src="captions-es.vtt" srclang="es" label="Spanish" />
</video>
```

## WebVTT Format

```
WEBVTT

00:00:00.000 --> 00:00:03.000
Welcome to our tutorial

00:00:03.500 --> 00:00:06.000
In this video, we'll cover...
```

## Audio Descriptions

```html
<video controls>
  <source src="video.mp4" />
  <track kind="descriptions" src="descriptions.vtt" srclang="en" label="Descriptions" />
</video>
```

## Transcript

```tsx
<div>
  <video controls>
    <source src="video.mp4" />
  </video>

  <details className="mt-4">
    <summary>Transcript</summary>
    <p>Full text transcript of the video...</p>
  </details>
</div>
```

## Keyboard Controls

- Space: Play/Pause
- Arrow Left/Right: Skip 5s
- Arrow Up/Down: Volume
- F: Fullscreen
- M: Mute

## Best Practices

1. **Captions required** - WCAG Level A
2. **Transcript provided** - Full text alternative
3. **Audio descriptions** - For visual-only content
4. **Keyboard controls** - All functions accessible
5. **No autoplay** - Let users control

## Resources

- WCAG Media: https://www.w3.org/WAI/media/av/
