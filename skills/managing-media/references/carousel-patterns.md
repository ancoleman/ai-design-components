# Carousel and Slider Patterns

Image carousels, sliders, and slideshow implementations with accessibility.

## Basic Carousel

```tsx
function Carousel({ images }: { images: string[] }) {
  const [currentIndex, setCurrentIndex] = useState(0);

  const next = () => setCurrentIndex((currentIndex + 1) % images.length);
  const prev = () => setCurrentIndex((currentIndex - 1 + images.length) % images.length);

  return (
    <div className="relative">
      <img src={images[currentIndex]} alt={`Slide ${currentIndex + 1}`} />

      <button onClick={prev} className="absolute left-4 top-1/2 -translate-y-1/2">
        ←
      </button>
      <button onClick={next} className="absolute right-4 top-1/2 -translate-y-1/2">
        →
      </button>

      <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2">
        {images.map((_, i) => (
          <button
            key={i}
            onClick={() => setCurrentIndex(i)}
            className={`w-2 h-2 rounded-full ${i === currentIndex ? 'bg-white' : 'bg-white/50'}`}
          />
        ))}
      </div>
    </div>
  );
}
```

## Swiper.js Integration

```tsx
import { Swiper, SwiperSlide } from 'swiper/react';
import { Navigation, Pagination, Autoplay } from 'swiper/modules';
import 'swiper/css';

<Swiper
  modules={[Navigation, Pagination, Autoplay]}
  navigation
  pagination={{ clickable: true }}
  autoplay={{ delay: 3000 }}
  loop
>
  {images.map((img, i) => (
    <SwiperSlide key={i}>
      <img src={img} alt={`Slide ${i + 1}`} />
    </SwiperSlide>
  ))}
</Swiper>
```

## Keyboard Navigation

```tsx
useEffect(() => {
  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'ArrowLeft') prev();
    if (e.key === 'ArrowRight') next();
  };

  window.addEventListener('keydown', handleKeyDown);
  return () => window.removeEventListener('keydown', handleKeyDown);
}, []);
```

## Best Practices

1. **Keyboard navigation** - Arrow keys, Home, End
2. **Touch gestures** - Swipe on mobile
3. **Pagination dots** - Show current slide
4. **Lazy load** - Load adjacent slides only
5. **Pause on hover** - Stop autoplay
6. **ARIA labels** - For screen readers
7. **Performance** - Limit simultaneous slides in DOM

## Resources

- Swiper: https://swiperjs.com/
- Embla Carousel: https://www.embla-carousel.com/
