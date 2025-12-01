// Custom Video Player
// Example implementation using video.js

import { useEffect, useRef } from 'react';
import videojs from 'video.js';
import 'video.js/dist/video-js.css';

export function VideoPlayer() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const playerRef = useRef<any>(null);

  useEffect(() => {
    if (!videoRef.current) return;

    // Initialize video.js player
    const player = videojs(videoRef.current, {
      controls: true,
      fluid: true,
      responsive: true,
      playbackRates: [0.5, 1, 1.5, 2],
      controlBar: {
        pictureInPictureToggle: true
      }
    });

    playerRef.current = player;

    // Event listeners
    player.on('play', () => {
      console.log('Video playing');
    });

    player.on('pause', () => {
      console.log('Video paused');
    });

    // Cleanup
    return () => {
      if (playerRef.current) {
        playerRef.current.dispose();
      }
    };
  }, []);

  return (
    <div
      className="video-container"
      style={{
        background: 'var(--video-player-bg)',
        borderRadius: 'var(--video-border-radius)',
        overflow: 'hidden'
      }}
    >
      <video
        ref={videoRef}
        className="video-js vjs-big-play-centered"
        poster="/thumbnails/video-poster.jpg"
      >
        <source src="/videos/sample.mp4" type="video/mp4" />
        <source src="/videos/sample.webm" type="video/webm" />

        {/* Captions */}
        <track
          kind="captions"
          src="/captions/english.vtt"
          srcLang="en"
          label="English"
          default
        />

        <p className="vjs-no-js">
          To view this video please enable JavaScript, and consider upgrading to a
          web browser that supports HTML5 video
        </p>
      </video>
    </div>
  );
}

// Example usage:
// <VideoPlayer />
