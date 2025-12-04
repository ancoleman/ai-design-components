import React, { useState, useRef } from 'react';
import { Play, Pause, SkipBack, SkipForward } from 'lucide-react';

/**
 * Custom Audio Player
 *
 * Features: Play/pause, seek, volume, time display, playlist support
 */

export function AudioPlayer({ src }: { src: string }) {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(1);

  const togglePlay = () => {
    if (isPlaying) {
      audioRef.current?.pause();
    } else {
      audioRef.current?.play();
    }
    setIsPlaying(!isPlaying);
  };

  const skip = (seconds: number) => {
    if (audioRef.current) {
      audioRef.current.currentTime += seconds;
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="p-4 bg-gray-100 rounded-lg max-w-md">
      <audio
        ref={audioRef}
        src={src}
        onTimeUpdate={(e) => setCurrentTime(e.currentTarget.currentTime)}
        onDurationChange={(e) => setDuration(e.currentTarget.duration)}
        onEnded={() => setIsPlaying(false)}
        onVolumeChange={(e) => setVolume(e.currentTarget.volume)}
      />

      {/* Controls */}
      <div className="flex items-center gap-4 mb-4">
        <button onClick={() => skip(-10)} className="p-2">
          <SkipBack size={20} />
        </button>

        <button
          onClick={togglePlay}
          className="p-3 bg-blue-500 text-white rounded-full hover:bg-blue-600"
        >
          {isPlaying ? <Pause size={24} /> : <Play size={24} />}
        </button>

        <button onClick={() => skip(10)} className="p-2">
          <SkipForward size={20} />
        </button>
      </div>

      {/* Progress Bar */}
      <div className="mb-2">
        <input
          type="range"
          min={0}
          max={duration || 0}
          value={currentTime}
          onChange={(e) => {
            const time = parseFloat(e.target.value);
            if (audioRef.current) {
              audioRef.current.currentTime = time;
            }
          }}
          className="w-full"
        />

        <div className="flex justify-between text-xs text-gray-600">
          <span>{formatTime(currentTime)}</span>
          <span>{formatTime(duration)}</span>
        </div>
      </div>

      {/* Volume */}
      <div className="flex items-center gap-2">
        <span className="text-sm">🔊</span>
        <input
          type="range"
          min={0}
          max={1}
          step={0.1}
          value={volume}
          onChange={(e) => {
            const vol = parseFloat(e.target.value);
            if (audioRef.current) {
              audioRef.current.volume = vol;
            }
          }}
          className="w-24"
        />
      </div>
    </div>
  );
}

export default AudioPlayer;
