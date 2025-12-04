# Image Accessibility

WCAG 2.1 compliance for images including alt text, captions, and decorative images.

## Alt Text

```tsx
// Informative images
<img src="chart.png" alt="Bar chart showing 30% revenue increase in Q4 2025" />

// Functional images (buttons, links)
<a href="/search">
  <img src="search-icon.svg" alt="Search" />
</a>

// Decorative images (no information)
<img src="border.png" alt="" role="presentation" />
```

## Complex Images

```tsx
<figure>
  <img
    src="data-visualization.png"
    alt="Sales data visualization"
    aria-describedby="chart-description"
  />
  <figcaption id="chart-description">
    Sales increased 30% from Q3 to Q4 2025. Electronics: $120K, Clothing: $85K, Home: $62K.
  </figcaption>
</figure>
```

## SVG Accessibility

```tsx
<svg role="img" aria-labelledby="chart-title chart-desc">
  <title id="chart-title">Revenue Chart</title>
  <desc id="chart-desc">Revenue grew from $50K to $80K over 6 months</desc>
  {/* SVG content */}
</svg>
```

## Best Practices

1. **Descriptive alt text** - Convey information, not "image of..."
2. **Empty alt for decorative** - `alt=""` to hide from screen readers
3. **Long descriptions** - Use aria-describedby for complex images
4. **Avoid text in images** - Use real text with CSS
5. **Color contrast** - Text overlays must have 4.5:1 contrast

## Resources

- WCAG Images: https://www.w3.org/WAI/tutorials/images/
