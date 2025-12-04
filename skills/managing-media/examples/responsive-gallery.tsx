import React from 'react';

/**
 * Responsive Image Gallery
 *
 * Grid layout that adapts to screen size with lightbox on click
 */

const images = Array.from({ length: 12 }, (_, i) => ({
  id: i + 1,
  src: `https://picsum.photos/400/300?random=${i}`,
  alt: `Image ${i + 1}`,
}));

export function ResponsiveGallery() {
  const [lightbox, setLightbox] = useState<number | null>(null);

  return (
    <div className="p-4">
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {images.map((img, i) => (
          <div
            key={img.id}
            onClick={() => setLightbox(i)}
            className="aspect-square overflow-hidden rounded-lg cursor-pointer hover:opacity-90 transition"
          >
            <img
              src={img.src}
              alt={img.alt}
              loading="lazy"
              className="w-full h-full object-cover"
            />
          </div>
        ))}
      </div>

      {/* Lightbox */}
      {lightbox !== null && (
        <div
          className="fixed inset-0 bg-black/90 z-50 flex items-center justify-center"
          onClick={() => setLightbox(null)}
        >
          <img
            src={images[lightbox].src}
            alt={images[lightbox].alt}
            className="max-w-[90vw] max-h-[90vh] object-contain"
            onClick={(e) => e.stopPropagation()}
          />

          <button
            onClick={(e) => {
              e.stopPropagation();
              setLightbox((lightbox - 1 + images.length) % images.length);
            }}
            className="absolute left-4 top-1/2 -translate-y-1/2 text-white text-4xl"
          >
            ←
          </button>

          <button
            onClick={(e) => {
              e.stopPropagation();
              setLightbox((lightbox + 1) % images.length);
            }}
            className="absolute right-4 top-1/2 -translate-y-1/2 text-white text-4xl"
          >
            →
          </button>
        </div>
      )}
    </div>
  );
}

export default ResponsiveGallery;
