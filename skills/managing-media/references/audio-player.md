# Audio Player Implementation

Custom audio players with waveform visualization, playlists, and controls.

## Native HTML5 Audio

```tsx
<audio controls>
  <source src="audio.mp3" type="audio/mpeg" />
  <source src="audio.ogg" type="audio/ogg" />
  Your browser does not support audio.
</audio>
```

## Custom Audio Player

```tsx
function AudioPlayer({ src }: { src: string }) {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);

  const togglePlay = () => {
    if (isPlaying) {
      audioRef.current?.pause();
    } else {
      audioRef.current?.play();
    }
    setIsPlaying(!isPlaying);
  };

  return (
    <div className="audio-player">
      <audio
        ref={audioRef}
        src={src}
        onTimeUpdate={(e) => setCurrentTime(e.currentTarget.currentTime)}
        onDurationChange={(e) => setDuration(e.currentTarget.duration)}
        onEnded={() => setIsPlaying(false)}
      />

      <button onClick={togglePlay}>
        {isPlaying ? '⏸' : '▶'}
      </button>

      <input
        type="range"
        min={0}
        max={duration}
        value={currentTime}
        onChange={(e) => {
          const time = parseFloat(e.target.value);
          audioRef.current!.currentTime = time;
          setCurrentTime(time);
        }}
        className="flex-1"
      />

      <span>{formatTime(currentTime)} / {formatTime(duration)}</span>
    </div>
  );
}

function formatTime(seconds: number): string {
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, '0')}`;
}
```

## Waveform Visualization

```tsx
import WaveSurfer from 'wavesurfer.js';

function WaveformPlayer({ src }: { src: string }) {
  const waveformRef = useRef<HTMLDivElement>(null);
  const wavesurfer = useRef<WaveSurfer | null>(null);

  useEffect(() => {
    wavesurfer.current = WaveSurfer.create({
      container: waveformRef.current!,
      waveColor: '#4F4A85',
      progressColor: '#3B82F6',
      cursorColor: '#3B82F6',
      height: 80,
    });

    wavesurfer.current.load(src);

    return () => wavesurfer.current?.destroy();
  }, [src]);

  return (
    <div>
      <div ref={waveformRef} />
      <button onClick={() => wavesurfer.current?.playPause()}>
        Play/Pause
      </button>
    </div>
  );
}
```

## Playlist

```tsx
function Playlist({ tracks }: { tracks: Track[] }) {
  const [currentTrack, setCurrentTrack] = useState(0);

  return (
    <div>
      <AudioPlayer
        src={tracks[currentTrack].url}
        onEnded={() => setCurrentTrack((currentTrack + 1) % tracks.length)}
      />

      <div className="playlist">
        {tracks.map((track, i) => (
          <div
            key={track.id}
            onClick={() => setCurrentTrack(i)}
            className={currentTrack === i ? 'active' : ''}
          >
            {track.title} - {track.artist}
          </div>
        ))}
      </div>
    </div>
  );
}
```

## Resources

- WaveSurfer.js: https://wavesurfer-js.org/
- Howler.js: https://howlerjs.com/
