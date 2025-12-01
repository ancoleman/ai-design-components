// Image Gallery with Lightbox
// Example implementation using react-image-gallery

import ImageGallery from 'react-image-gallery';
import 'react-image-gallery/styles/css/image-gallery.css';

interface Image {
  original: string;
  thumbnail: string;
  description?: string;
}

export function ImageGalleryExample() {
  const images: Image[] = [
    {
      original: '/images/photo1.jpg',
      thumbnail: '/images/photo1-thumb.jpg',
      description: 'Photo 1 description'
    },
    {
      original: '/images/photo2.jpg',
      thumbnail: '/images/photo2-thumb.jpg',
      description: 'Photo 2 description'
    },
    // Add more images...
  ];

  return (
    <div className="gallery-container">
      <ImageGallery
        items={images}
        showPlayButton={false}
        showFullscreenButton={true}
        showThumbnails={true}
        lazyLoad={true}
        slideDuration={300}
        slideInterval={3000}
        onImageLoad={() => {
          console.log('Image loaded');
        }}
      />
    </div>
  );
}

// Custom styling with design tokens:
// .image-gallery {
//   --image-gallery-gap: var(--gallery-gap);
//   --image-gallery-border-radius: var(--image-border-radius);
// }
