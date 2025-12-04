import React, { useEffect, useRef } from 'react';
import WaveSurfer from 'wavesurfer.js';

/**
 * Audio Waveform Player
 *
 * Visualize audio with interactive waveform
 * Library: wavesurfer.js
 * Install: npm install wavesurfer.js
 */

export function AudioWaveform({ src }: { src: string }) {
  const waveformRef = useRef<HTMLDivElement>(null);
  const wavesurfer = useRef<WaveSurfer | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    if (!waveformRef.current) return;

    wavesurfer.current = WaveSurfer.create({
      container: waveformRef.current,
      waveColor: '#9ca3af',
      progressColor: '#3b82f6',
      cursorColor: '#3b82f6',
      barWidth: 2,
      barGap: 1,
      barRadius: 2,
      height: 100,
      normalize: true,
    });

    wavesurfer.current.load(src);

    wavesurfer.current.on('play', () => setIsPlaying(true));
    wavesurfer.current.on('pause', () => setIsPlaying(false));

    return () => wavesurfer.current?.destroy();
  }, [src]);

  return (
    <div className="p-4">
      <div ref={waveformRef} className="mb-4" />

      <button
        onClick={() => wavesurfer.current?.playPause()}
        className="px-4 py-2 bg-blue-500 text-white rounded"
      >
        {isPlaying ? 'Pause' : 'Play'}
      </button>
    </div>
  );
}

export default AudioWaveform;
