import React, { useEffect, useRef } from 'react';
import videojs from 'video.js';
import 'video.js/dist/video-js.css';

/**
 * Video.js Player
 *
 * Full-featured video player with HLS support, quality switching, and plugins
 * Install: npm install video.js
 */

export function VideoJSPlayer({ src }: { src: string }) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const playerRef = useRef<any>(null);

  useEffect(() => {
    if (!videoRef.current) return;

    playerRef.current = videojs(videoRef.current, {
      controls: true,
      autoplay: false,
      preload: 'metadata',
      fluid: true,  // Responsive
      playbackRates: [0.5, 1, 1.5, 2],
      sources: [{
        src,
        type: 'video/mp4',
      }],
    });

    return () => {
      if (playerRef.current) {
        playerRef.current.dispose();
      }
    };
  }, [src]);

  return (
    <div className="max-w-4xl mx-auto">
      <div data-vjs-player>
        <video
          ref={videoRef}
          className="video-js vjs-big-play-centered"
        />
      </div>
    </div>
  );
}

export default VideoJSPlayer;
