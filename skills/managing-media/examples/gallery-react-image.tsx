import React, { useState } from 'react';
import Image from 'next/image';

/**
 * Next.js Image Gallery
 *
 * Optimized gallery using Next.js Image component
 * Features: Automatic optimization, lazy loading, blur placeholder
 */

const images = [
  { id: 1, src: '/photos/1.jpg', width: 800, height: 600, alt: 'Photo 1' },
  { id: 2, src: '/photos/2.jpg', width: 800, height: 600, alt: 'Photo 2' },
  { id: 3, src: '/photos/3.jpg', width: 800, height: 600, alt: 'Photo 3' },
  { id: 4, src: '/photos/4.jpg', width: 800, height: 600, alt: 'Photo 4' },
  { id: 5, src: '/photos/5.jpg', width: 800, height: 600, alt: 'Photo 5' },
  { id: 6, src: '/photos/6.jpg', width: 800, height: 600, alt: 'Photo 6' },
];

export function NextImageGallery() {
  const [selectedImage, setSelectedImage] = useState<number | null>(null);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-6">Photo Gallery</h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {images.map((img, index) => (
          <div
            key={img.id}
            onClick={() => setSelectedImage(index)}
            className="relative aspect-square overflow-hidden rounded-lg cursor-pointer hover:opacity-90 transition"
          >
            <Image
              src={img.src}
              alt={img.alt}
              fill
              sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
              className="object-cover"
              placeholder="blur"
              blurDataURL="data:image/jpeg;base64,/9j/4AAQSkZJRg..."
            />
          </div>
        ))}
      </div>

      {/* Lightbox */}
      {selectedImage !== null && (
        <div
          className="fixed inset-0 bg-black/90 z-50 flex items-center justify-center p-4"
          onClick={() => setSelectedImage(null)}
        >
          <div className="relative max-w-7xl max-h-[90vh]">
            <Image
              src={images[selectedImage].src}
              width={images[selectedImage].width}
              height={images[selectedImage].height}
              alt={images[selectedImage].alt}
              className="max-h-[90vh] object-contain"
            />
          </div>

          <button
            onClick={(e) => {
              e.stopPropagation();
              setSelectedImage((selectedImage - 1 + images.length) % images.length);
            }}
            className="absolute left-4 top-1/2 -translate-y-1/2 text-white text-4xl"
          >
            ←
          </button>

          <button
            onClick={(e) => {
              e.stopPropagation();
              setSelectedImage((selectedImage + 1) % images.length);
            }}
            className="absolute right-4 top-1/2 -translate-y-1/2 text-white text-4xl"
          >
            →
          </button>

          <button
            onClick={() => setSelectedImage(null)}
            className="absolute top-4 right-4 text-white text-2xl"
          >
            ✕
          </button>
        </div>
      )}
    </div>
  );
}

export default NextImageGallery;
