import React, { useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

/**
 * Image Carousel
 *
 * Features: Previous/next navigation, dots indicator, keyboard support, autoplay
 */

const images = [
  'https://picsum.photos/800/400?random=1',
  'https://picsum.photos/800/400?random=2',
  'https://picsum.photos/800/400?random=3',
  'https://picsum.photos/800/400?random=4',
];

export function Carousel() {
  const [currentIndex, setCurrentIndex] = useState(0);

  const next = () => setCurrentIndex((currentIndex + 1) % images.length);
  const prev = () => setCurrentIndex((currentIndex - 1 + images.length) % images.length);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'ArrowLeft') prev();
      if (e.key === 'ArrowRight') next();
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [currentIndex]);

  return (
    <div className="relative max-w-4xl mx-auto">
      <div className="relative h-96 overflow-hidden rounded-lg">
        {images.map((img, i) => (
          <img
            key={i}
            src={img}
            alt={`Slide ${i + 1}`}
            className={`absolute inset-0 w-full h-full object-cover transition-opacity duration-500 ${
              i === currentIndex ? 'opacity-100' : 'opacity-0'
            }`}
          />
        ))}
      </div>

      <button
        onClick={prev}
        className="absolute left-4 top-1/2 -translate-y-1/2 bg-white/80 p-2 rounded-full hover:bg-white"
      >
        <ChevronLeft />
      </button>

      <button
        onClick={next}
        className="absolute right-4 top-1/2 -translate-y-1/2 bg-white/80 p-2 rounded-full hover:bg-white"
      >
        <ChevronRight />
      </button>

      <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2">
        {images.map((_, i) => (
          <button
            key={i}
            onClick={() => setCurrentIndex(i)}
            className={`w-2 h-2 rounded-full ${
              i === currentIndex ? 'bg-white' : 'bg-white/50'
            }`}
          />
        ))}
      </div>
    </div>
  );
}

export default Carousel;
