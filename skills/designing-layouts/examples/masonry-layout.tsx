import React, { useState, useEffect, useRef } from 'react';

/**
 * Pinterest-style Masonry Layout
 * Features: Variable height items, responsive columns, smooth transitions
 */

interface MasonryItem {
  id: string;
  content: React.ReactNode;
  height?: number; // Optional predefined height
}

interface MasonryLayoutProps {
  items: MasonryItem[];
  columns?: number; // Fixed columns or auto-calculate
  gap?: number;
  minColumnWidth?: number;
}

export function MasonryLayout({
  items,
  columns,
  gap = 16,
  minColumnWidth = 250
}: MasonryLayoutProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [columnCount, setColumnCount] = useState(columns || 3);
  const [columnHeights, setColumnHeights] = useState<number[]>([]);
  const [itemPositions, setItemPositions] = useState<Map<string, { column: number; top: number }>>(new Map());

  // Calculate number of columns based on container width
  useEffect(() => {
    if (columns) {
      setColumnCount(columns);
      return;
    }

    const updateColumns = () => {
      if (containerRef.current) {
        const containerWidth = containerRef.current.offsetWidth;
        const calculatedColumns = Math.max(1, Math.floor(containerWidth / minColumnWidth));
        setColumnCount(calculatedColumns);
      }
    };

    updateColumns();

    const resizeObserver = new ResizeObserver(updateColumns);
    if (containerRef.current) {
      resizeObserver.observe(containerRef.current);
    }

    return () => resizeObserver.disconnect();
  }, [columns, minColumnWidth]);

  // Calculate item positions
  useEffect(() => {
    const heights = new Array(columnCount).fill(0);
    const positions = new Map<string, { column: number; top: number }>();

    items.forEach((item) => {
      // Find the shortest column
      const shortestColumn = heights.indexOf(Math.min(...heights));

      // Position item in shortest column
      positions.set(item.id, {
        column: shortestColumn,
        top: heights[shortestColumn]
      });

      // Update column height (use predefined height or estimate)
      const itemHeight = item.height || 200; // Default estimate
      heights[shortestColumn] += itemHeight + gap;
    });

    setColumnHeights(heights);
    setItemPositions(positions);
  }, [items, columnCount, gap]);

  const getColumnWidth = () => {
    if (!containerRef.current) return '100%';
    const containerWidth = containerRef.current.offsetWidth;
    const totalGaps = (columnCount - 1) * gap;
    const columnWidth = (containerWidth - totalGaps) / columnCount;
    return `${columnWidth}px`;
  };

  return (
    <div
      ref={containerRef}
      className="masonry-container"
      style={{
        position: 'relative',
        height: Math.max(...columnHeights) + 'px'
      }}
    >
      {items.map((item) => {
        const position = itemPositions.get(item.id);
        if (!position) return null;

        const columnWidth = getColumnWidth();
        const left = `calc(${position.column} * (${columnWidth} + ${gap}px))`;

        return (
          <div
            key={item.id}
            className="masonry-item"
            style={{
              position: 'absolute',
              top: `${position.top}px`,
              left: left,
              width: columnWidth,
              transition: 'all 0.3s ease'
            }}
          >
            {item.content}
          </div>
        );
      })}
    </div>
  );
}

/**
 * CSS-Only Masonry Layout (Modern Browsers)
 * Uses CSS Grid with experimental masonry support
 */
export function CSSMasonryLayout({ items, columns = 4, gap = '1rem' }: {
  items: React.ReactNode[];
  columns?: number;
  gap?: string;
}) {
  return (
    <>
      <div className="css-masonry-modern">
        {items.map((item, index) => (
          <div key={index} className="css-masonry-item">
            {item}
          </div>
        ))}
      </div>

      <style>{`
        /* Modern CSS Grid Masonry (Experimental - Check browser support) */
        @supports (grid-template-rows: masonry) {
          .css-masonry-modern {
            display: grid;
            grid-template-columns: repeat(${columns}, 1fr);
            grid-template-rows: masonry;
            gap: ${gap};
          }
        }

        /* Fallback to columns */
        @supports not (grid-template-rows: masonry) {
          .css-masonry-modern {
            column-count: ${columns};
            column-gap: ${gap};
          }

          .css-masonry-item {
            break-inside: avoid;
            margin-bottom: ${gap};
          }
        }

        /* Responsive columns */
        @media (max-width: 1200px) {
          .css-masonry-modern {
            column-count: 3;
            grid-template-columns: repeat(3, 1fr);
          }
        }

        @media (max-width: 900px) {
          .css-masonry-modern {
            column-count: 2;
            grid-template-columns: repeat(2, 1fr);
          }
        }

        @media (max-width: 600px) {
          .css-masonry-modern {
            column-count: 1;
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </>
  );
}

/**
 * Pinterest-Style Cards Example
 */
interface PinterestCard {
  id: string;
  image: string;
  title: string;
  description?: string;
  author?: {
    name: string;
    avatar?: string;
  };
  stats?: {
    likes: number;
    comments: number;
  };
}

export function PinterestGrid({ cards }: { cards: PinterestCard[] }) {
  const masonryItems: MasonryItem[] = cards.map(card => ({
    id: card.id,
    content: (
      <article className="pinterest-card">
        <div className="pinterest-card__image">
          <img src={card.image} alt={card.title} loading="lazy" />
          <button className="pinterest-card__save" aria-label="Save">
            📌 Save
          </button>
        </div>

        <div className="pinterest-card__content">
          <h3 className="pinterest-card__title">{card.title}</h3>

          {card.description && (
            <p className="pinterest-card__description">{card.description}</p>
          )}

          {card.author && (
            <div className="pinterest-card__author">
              {card.author.avatar && (
                <img src={card.author.avatar} alt="" className="author-avatar" />
              )}
              <span className="author-name">{card.author.name}</span>
            </div>
          )}

          {card.stats && (
            <div className="pinterest-card__stats">
              <span>❤️ {card.stats.likes}</span>
              <span>💬 {card.stats.comments}</span>
            </div>
          )}
        </div>
      </article>
    ),
    // Estimate height based on content
    height: card.description ? 350 : 280
  }));

  return <MasonryLayout items={masonryItems} minColumnWidth={236} gap={20} />;
}

/**
 * Photo Gallery Example
 */
export function PhotoGallery({ photos }: {
  photos: Array<{
    id: string;
    src: string;
    alt: string;
    width: number;
    height: number;
    caption?: string;
  }>
}) {
  const masonryItems: MasonryItem[] = photos.map(photo => ({
    id: photo.id,
    content: (
      <figure className="photo-gallery-item">
        <img
          src={photo.src}
          alt={photo.alt}
          loading="lazy"
          style={{ aspectRatio: `${photo.width}/${photo.height}` }}
        />
        {photo.caption && (
          <figcaption className="photo-caption">{photo.caption}</figcaption>
        )}
      </figure>
    ),
    // Calculate height based on aspect ratio
    height: (250 * photo.height) / photo.width
  }));

  return <MasonryLayout items={masonryItems} minColumnWidth={250} gap={16} />;
}

// CSS Styles
const styles = `
/* Masonry Container */
.masonry-container {
  width: 100%;
  position: relative;
  transition: height 0.3s ease;
}

.masonry-item {
  position: absolute;
  transition: all 0.3s ease;
}

/* Pinterest Card Styles */
.pinterest-card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
}

.pinterest-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.pinterest-card__image {
  position: relative;
  overflow: hidden;
  background: var(--color-background);
}

.pinterest-card__image img {
  width: 100%;
  height: auto;
  display: block;
}

.pinterest-card__save {
  position: absolute;
  top: 8px;
  right: 8px;
  background: var(--color-error);
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: var(--radius-full);
  font-weight: 600;
  opacity: 0;
  transform: translateY(-4px);
  transition: opacity 0.2s, transform 0.2s;
  cursor: pointer;
}

.pinterest-card:hover .pinterest-card__save {
  opacity: 1;
  transform: translateY(0);
}

.pinterest-card__content {
  padding: var(--spacing-md);
}

.pinterest-card__title {
  font-size: var(--text-base);
  font-weight: 600;
  margin: 0 0 var(--spacing-xs) 0;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.pinterest-card__description {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin: 0 0 var(--spacing-sm) 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.pinterest-card__author {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  margin-bottom: var(--spacing-sm);
}

.author-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  object-fit: cover;
}

.author-name {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.pinterest-card__stats {
  display: flex;
  gap: var(--spacing-md);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

/* Photo Gallery Styles */
.photo-gallery-item {
  margin: 0;
  border-radius: var(--radius-md);
  overflow: hidden;
  background: var(--color-surface);
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s, box-shadow 0.2s;
}

.photo-gallery-item:hover {
  transform: scale(1.02);
  box-shadow: var(--shadow-md);
}

.photo-gallery-item img {
  width: 100%;
  height: auto;
  display: block;
}

.photo-caption {
  padding: var(--spacing-sm);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  background: var(--color-surface);
}

/* Loading State */
.masonry-loading {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.skeleton-card {
  background: linear-gradient(90deg, var(--color-background) 25%, var(--color-surface) 50%, var(--color-background) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--radius-lg);
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Responsive */
@media (max-width: 640px) {
  .pinterest-card__content {
    padding: var(--spacing-sm);
  }

  .pinterest-card__title {
    font-size: var(--text-sm);
  }
}

/* Dark Mode Support */
@media (prefers-color-scheme: dark) {
  .pinterest-card {
    background: var(--color-surface-dark);
  }

  .photo-gallery-item {
    background: var(--color-surface-dark);
  }
}
`;