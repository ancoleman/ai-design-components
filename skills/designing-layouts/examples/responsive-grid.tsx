import React, { useState, useEffect } from 'react';

/**
 * Auto-Responsive Grid System
 * Features: Auto-fit/fill, container queries, customizable gaps and columns
 */

interface GridItem {
  id: string;
  content: React.ReactNode;
  span?: number; // How many columns this item should span
  aspectRatio?: string; // Aspect ratio for the item
}

interface ResponsiveGridProps {
  items: GridItem[];
  minItemWidth?: number;
  maxColumns?: number;
  gap?: string;
  variant?: 'auto-fit' | 'auto-fill' | 'fixed';
  useContainerQueries?: boolean;
}

export function ResponsiveGrid({
  items,
  minItemWidth = 250,
  maxColumns = 12,
  gap = 'var(--spacing-md)',
  variant = 'auto-fit',
  useContainerQueries = true
}: ResponsiveGridProps) {
  const [containerWidth, setContainerWidth] = useState<number>(0);
  const [columns, setColumns] = useState<number>(1);

  // Calculate optimal columns based on container width
  useEffect(() => {
    if (variant === 'fixed') return;

    const updateColumns = () => {
      const container = document.querySelector('.grid-container');
      if (container) {
        const width = container.clientWidth;
        setContainerWidth(width);

        const gapSize = parseInt(gap) || 16;
        const availableWidth = width - gapSize;
        const possibleColumns = Math.floor(availableWidth / (minItemWidth + gapSize));
        setColumns(Math.min(possibleColumns, maxColumns));
      }
    };

    updateColumns();

    const observer = new ResizeObserver(updateColumns);
    const container = document.querySelector('.grid-container');
    if (container) {
      observer.observe(container);
    }

    return () => observer.disconnect();
  }, [minItemWidth, maxColumns, gap, variant]);

  const getGridStyles = () => {
    const baseStyles = {
      display: 'grid',
      gap: gap,
      width: '100%'
    };

    switch (variant) {
      case 'auto-fit':
        return {
          ...baseStyles,
          gridTemplateColumns: `repeat(auto-fit, minmax(min(${minItemWidth}px, 100%), 1fr))`
        };
      case 'auto-fill':
        return {
          ...baseStyles,
          gridTemplateColumns: `repeat(auto-fill, minmax(${minItemWidth}px, 1fr))`
        };
      case 'fixed':
        return {
          ...baseStyles,
          gridTemplateColumns: `repeat(${maxColumns}, 1fr)`
        };
      default:
        return baseStyles;
    }
  };

  return (
    <div
      className={`grid-container ${useContainerQueries ? 'grid-container--cq' : ''}`}
      style={useContainerQueries ? { containerType: 'inline-size' } : {}}
    >
      <div className="grid" style={getGridStyles()}>
        {items.map(item => (
          <div
            key={item.id}
            className="grid-item"
            style={{
              gridColumn: item.span ? `span ${item.span}` : undefined,
              aspectRatio: item.aspectRatio || undefined
            }}
          >
            {item.content}
          </div>
        ))}
      </div>

      {/* Grid info for debugging/demo */}
      {process.env.NODE_ENV === 'development' && (
        <div className="grid-info">
          <span>Container: {containerWidth}px</span>
          <span>Columns: {columns}</span>
          <span>Min width: {minItemWidth}px</span>
        </div>
      )}
    </div>
  );
}

/**
 * Card Grid Example
 * Common use case for product cards, blog posts, etc.
 */
interface CardGridProps {
  cards: Array<{
    id: string;
    title: string;
    description: string;
    image?: string;
    tags?: string[];
  }>;
}

export function CardGrid({ cards }: CardGridProps) {
  const gridItems: GridItem[] = cards.map(card => ({
    id: card.id,
    content: (
      <article className="card">
        {card.image && (
          <div className="card__image">
            <img src={card.image} alt="" loading="lazy" />
          </div>
        )}
        <div className="card__content">
          <h3 className="card__title">{card.title}</h3>
          <p className="card__description">{card.description}</p>
          {card.tags && (
            <div className="card__tags">
              {card.tags.map(tag => (
                <span key={tag} className="tag">{tag}</span>
              ))}
            </div>
          )}
        </div>
      </article>
    )
  }));

  return (
    <ResponsiveGrid
      items={gridItems}
      minItemWidth={300}
      gap="var(--spacing-lg)"
      variant="auto-fit"
      useContainerQueries={true}
    />
  );
}

/**
 * Feature Grid Example
 * For feature sections with icons and descriptions
 */
interface FeatureGridProps {
  features: Array<{
    id: string;
    icon: React.ReactNode;
    title: string;
    description: string;
  }>;
  columns?: number;
}

export function FeatureGrid({ features, columns = 3 }: FeatureGridProps) {
  const gridItems: GridItem[] = features.map(feature => ({
    id: feature.id,
    content: (
      <div className="feature">
        <div className="feature__icon">{feature.icon}</div>
        <h3 className="feature__title">{feature.title}</h3>
        <p className="feature__description">{feature.description}</p>
      </div>
    )
  }));

  return (
    <ResponsiveGrid
      items={gridItems}
      minItemWidth={280}
      maxColumns={columns}
      gap="var(--spacing-xl)"
      variant="auto-fit"
    />
  );
}

/**
 * Image Gallery Grid
 * Responsive image gallery with different aspect ratios
 */
interface GalleryImage {
  id: string;
  src: string;
  alt: string;
  span?: number;
  aspectRatio?: string;
}

export function ImageGallery({ images }: { images: GalleryImage[] }) {
  const gridItems: GridItem[] = images.map(img => ({
    id: img.id,
    span: img.span,
    aspectRatio: img.aspectRatio || '1',
    content: (
      <figure className="gallery-item">
        <img
          src={img.src}
          alt={img.alt}
          loading="lazy"
          decoding="async"
        />
      </figure>
    )
  }));

  return (
    <ResponsiveGrid
      items={gridItems}
      minItemWidth={200}
      gap="var(--spacing-sm)"
      variant="auto-fit"
    />
  );
}

// CSS Styles
const styles = `
/* Grid Container */
.grid-container {
  width: 100%;
  position: relative;
}

.grid-container--cq {
  container-type: inline-size;
  container-name: grid;
}

/* Grid */
.grid {
  display: grid;
  width: 100%;
}

.grid-item {
  min-width: 0; /* Prevent overflow */
  position: relative;
}

/* Container Queries for Grid Items */
@container grid (min-width: 600px) {
  .card {
    display: grid;
    grid-template-columns: 200px 1fr;
    gap: var(--spacing-md);
  }

  .card__image {
    aspect-ratio: 1;
  }
}

@container grid (min-width: 900px) {
  .feature {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: var(--spacing-md);
    align-items: start;
  }
}

/* Card Styles */
.card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s, box-shadow 0.2s;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.card__image {
  aspect-ratio: 16/9;
  overflow: hidden;
  background: var(--color-background);
}

.card__image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card__content {
  padding: var(--spacing-md);
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.card__title {
  font-size: var(--text-lg);
  font-weight: 600;
  margin: 0;
  line-height: 1.3;
}

.card__description {
  color: var(--color-text-secondary);
  margin: 0;
  flex: 1;
}

.card__tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-xs);
  margin-top: auto;
}

.tag {
  padding: 2px 8px;
  background: var(--color-primary-light);
  color: var(--color-primary);
  border-radius: var(--radius-sm);
  font-size: var(--text-sm);
}

/* Feature Styles */
.feature {
  text-align: center;
  padding: var(--spacing-lg);
}

.feature__icon {
  font-size: 48px;
  margin-bottom: var(--spacing-md);
  color: var(--color-primary);
}

.feature__title {
  font-size: var(--text-xl);
  font-weight: 600;
  margin: 0 0 var(--spacing-sm) 0;
}

.feature__description {
  color: var(--color-text-secondary);
  margin: 0;
}

/* Gallery Styles */
.gallery-item {
  margin: 0;
  overflow: hidden;
  border-radius: var(--radius-md);
  background: var(--color-background);
}

.gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.3s;
}

.gallery-item:hover img {
  transform: scale(1.05);
}

/* Grid Info (Development) */
.grid-info {
  position: fixed;
  bottom: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 12px;
  display: flex;
  gap: 16px;
  z-index: 9999;
  font-family: monospace;
}

/* Responsive Breakpoints */
@media (max-width: 640px) {
  .card__content {
    padding: var(--spacing-sm);
  }

  .feature {
    padding: var(--spacing-md);
  }

  .feature__icon {
    font-size: 36px;
  }
}

@media (min-width: 1280px) {
  .card__content {
    padding: var(--spacing-lg);
  }
}

/* Print Styles */
@media print {
  .grid {
    display: block;
  }

  .grid-item {
    page-break-inside: avoid;
    margin-bottom: var(--spacing-md);
  }
}
`;