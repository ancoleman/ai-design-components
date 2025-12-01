# Media & File Management Skill

This skill implements comprehensive media and file management components following Anthropic's Skills best practices.

## Skill Overview

**Name:** `managing-media`

**Purpose:** Provides systematic patterns for implementing media and file management components across all formats (images, videos, audio, documents).

**Coverage:**
- File upload (drag-drop, multi-file, resumable)
- Image galleries (lightbox, carousel, masonry)
- Video players (custom controls, captions, streaming)
- Audio players (waveform, playlists)
- Document viewers (PDF, Office)
- Optimization strategies (compression, responsive images, CDN)

## Structure

```
media/
├── SKILL.md                    # Main skill file (474 lines)
├── README.md                   # This file
├── init.md                     # Master plan (preserved from planning phase)
├── references/                 # Detailed documentation
│   ├── implementation-guide.md
│   ├── upload-patterns.md
│   ├── gallery-patterns.md
│   ├── video-player.md
│   ├── library-comparison.md
│   ├── accessibility-patterns.md
│   └── performance-optimization.md
├── examples/                   # Working code examples
│   ├── basic-upload.tsx
│   ├── image-gallery.tsx
│   └── video-player.tsx
├── scripts/                    # Utility scripts (token-free execution)
│   ├── optimize_images.py
│   └── validate_media_accessibility.js
└── assets/                     # Configuration and templates
    ├── upload-config.json
    └── media-templates/
```

## Usage

This skill activates when:
- Implementing file upload features
- Building image galleries or carousels
- Creating video or audio players
- Displaying PDF or document viewers
- Optimizing media for performance
- Handling large file uploads
- Implementing media accessibility

## Progressive Disclosure

The skill follows Anthropic's progressive disclosure pattern:
1. **SKILL.md** - Core guidance and quick decision frameworks (474 lines)
2. **references/** - Detailed documentation loaded as needed
3. **scripts/** - Executable utilities (no context cost)
4. **examples/** - Working implementations

## Key Features

### Decision Frameworks
- Media type selection guide
- Upload strategy by file size
- Performance optimization thresholds
- Accessibility requirements

### Library Recommendations
- **Images:** react-image-gallery, LightGallery
- **Video:** video.js, Plyr
- **Audio:** wavesurfer.js, Howler.js
- **PDF:** react-pdf
- **Upload:** react-dropzone, Uppy

### Optimization Strategies
- Responsive images (srcset, sizes)
- Modern formats (WebP, AVIF)
- Lazy loading
- Adaptive streaming
- CDN integration

### Accessibility Patterns
- WCAG 2.1 compliance
- Alt text guidelines
- Caption/subtitle requirements
- Keyboard navigation
- ARIA patterns

## Integration

This skill integrates with:
- **design-tokens** - Visual styling via token system
- **forms** - File input fields and validation
- **feedback** - Upload progress and error messages
- **ai-chat** - Image attachments and file sharing
- **dashboards** - Media widgets and thumbnails

## Line Count

SKILL.md: **474 lines** (under 500-line requirement ✓)

## Validation

The skill has been validated against Anthropic's best practices checklist:

### Core Quality ✓
- Description includes WHAT and WHEN
- SKILL.md under 500 lines
- No time-sensitive information
- Consistent terminology
- Concrete examples
- One-level deep references

### Naming and Structure ✓
- Gerund form name: `managing-media`
- Lowercase, hyphens only
- Description under 1024 chars
- Forward slashes in paths
- Descriptive file names

### Progressive Disclosure ✓
- Main file concise
- References for details
- Scripts for deterministic operations
- Clear execution intent

## Development Status

- [x] SKILL.md created (474 lines)
- [x] Directory structure created
- [x] Core reference files created
- [x] Example implementations created
- [x] Utility scripts created
- [x] Configuration assets created
- [ ] Full example implementations (to be expanded)
- [ ] Additional reference documentation (to be expanded)

## Next Steps

To expand this skill:
1. Add more working examples (chunked upload, carousel, etc.)
2. Expand reference documentation
3. Add more utility scripts
4. Create evaluation scenarios
5. Test across models (Haiku, Sonnet, Opus)

## License

Part of the ai-design-components project. See root LICENSE file.
