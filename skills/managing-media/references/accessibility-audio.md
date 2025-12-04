# Audio Accessibility

Transcripts, visual indicators, and keyboard controls for accessible audio content.

## Transcript (Required)

```tsx
<div>
  <audio controls>
    <source src="podcast.mp3" />
  </audio>

  <details className="mt-4">
    <summary>Transcript</summary>
    <div className="prose">
      <p><strong>Host:</strong> Welcome to our podcast...</p>
      <p><strong>Guest:</strong> Thank you for having me...</p>
    </div>
  </details>
</div>
```

## Visual Play Indicator

```tsx
function AudioWithVisual({ src }: { src: string }) {
  const [isPlaying, setIsPlaying] = useState(false);

  return (
    <div className="flex items-center gap-4">
      <audio
        src={src}
        onPlay={() => setIsPlaying(true)}
        onPause={() => setIsPlaying(false)}
      />

      {isPlaying && (
        <div className="flex gap-1">
          <div className="w-1 h-4 bg-blue-500 animate-pulse" />
          <div className="w-1 h-6 bg-blue-500 animate-pulse animation-delay-75" />
          <div className="w-1 h-4 bg-blue-500 animate-pulse animation-delay-150" />
        </div>
      )}
    </div>
  );
}
```

## Keyboard Controls

```tsx
useEffect(() => {
  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === ' ') {
      e.preventDefault();
      audioRef.current?.paused ? audioRef.current?.play() : audioRef.current?.pause();
    }
    if (e.key === 'ArrowLeft') {
      audioRef.current!.currentTime -= 5;  // Skip back 5s
    }
    if (e.key === 'ArrowRight') {
      audioRef.current!.currentTime += 5;  // Skip forward 5s
    }
  };

  window.addEventListener('keydown', handleKeyDown);
  return () => window.removeEventListener('keydown', handleKeyDown);
}, []);
```

## Best Practices

1. **Transcript required** - Text alternative (WCAG Level A)
2. **Visual feedback** - For deaf/hard-of-hearing users
3. **Keyboard controls** - Space, arrows
4. **No autoplay** - User-initiated only
5. **Volume control** - Accessible to keyboard

## Resources

- WCAG Audio: https://www.w3.org/WAI/media/av/
