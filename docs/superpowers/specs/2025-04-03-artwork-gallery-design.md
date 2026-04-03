# Aseprite Artwork Gallery - Design Document

**Date:** 2025-04-03
**Status:** ✅ Implemented

## Overview

A static HTML gallery for displaying Aseprite artwork, automatically generated from PNG files in the `png/` directory. The gallery matches the design and Catppuccin theme of the main website (bongopoyo.github.io).

## Architecture

### Components

1. **Python Generator Script** (`generate_gallery.py`)
   - Recursively scans `png/` directory for PNG files
   - Extracts image metadata (dimensions, file size) using Pillow
   - Generates complete `docs/index.html` with embedded CSS and JavaScript
   - No runtime dependencies - fully static output

2. **Static HTML Page** (`docs/index.html`)
   - Single-file solution (CSS and JS embedded)
   - Responsive grid: 5 columns (desktop) / 3 columns (tablet) / 1 column (mobile)
   - Lazy loading with IntersectionObserver
   - Lightbox modal with keyboard navigation

3. **GitHub Actions Workflow** (`.github/workflows/update-gallery.yml`)
   - Triggers on push to `main` when `png/**` changes
   - Runs Python script to regenerate gallery
   - Auto-commits updated HTML

## Features

### Layout
- **Top Bar:** Logo "[Aseprite Artwork]" + menu button
- **Sidebar:** Slides in from right with info
- **Main Content:** Title, description, links, gallery grid
- **Bottom Bar:** Social links (Itch, YouTube, GitHub, BlueSky, Mastodon, Email, Matrix, Discord)

### Gallery Grid
- Responsive columns: 5 / 3 / 1
- Fixed 250x250px thumbnails (maintain aspect ratio)
- Image metadata display:
  - Filename (truncated with tooltip)
  - Dimensions (e.g., "1024 × 768")
  - File size (e.g., "1.2 MB")

### Interactions
- **Hover Effects:**
  - Card lifts slightly (translateY -5px)
  - Image scales to 1.05
  - Pink glow (#f5c2e7) around image

- **Lightbox:**
  - Click any image to open full-size view
  - Shows filename, dimensions, file size
  - Close via click outside, × button, or q/Escape

- **Keyboard Navigation:**
  - `h`/`l` or ←/→: previous/next image
  - `j`/`k` or ↓/↑: navigate between rows
  - `q` or `Escape`: close lightbox

### Performance
- Lazy loading images as they enter viewport
- Pre-generated static HTML (no runtime file system access)
- No external dependencies

## Styling

### Catppuccin Theme
```css
--background: #1e1e2e
--surface: #313244
--text: #cdd6f4
--accent: #f5c2e7
--accent-hover: #f8a1f1
--shadow: rgba(0, 0, 0, 0.5)
--darker-bg: #181825
--muted: #7f849c
--card-hover: #3b3b5a
--bottom-bg: #11111b
```

### Typography
- Font stack: "Segoe UI", "Fira Code", monospace
- Matches main website style

### Social Link Hover Colors
- YouTube: #f38ba8
- GitHub: #cdd6f4
- Itch: #fab387
- Mastodon: #89b4fa
- BlueSky: #89dceb
- Matrix: #a6e3a1
- Email: #eba0ac
- Discord: #74c7ec

## File Structure

```
AsepriteArtwork/
├── png/
│   ├── image1.png
│   └── ...
├── docs/
│   ├── index.html          (generated)
│   └── superpowers/
│       └── specs/
│           └── 2025-04-03-artwork-gallery-design.md
├── .github/
│   └── workflows/
│       └── update-gallery.yml
├── generate_gallery.py     (new)
├── add_pngs_to_readme.py   (existing)
└── README.md               (existing)
```

## GitHub Pages Setup

1. Go to repo Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main` / `docs` folder
4. URL: `https://bongopoyo.github.io/AsepriteArtwork/`

## Workflow

### Adding New Artwork
1. Add PNG files to `png/` directory
2. Commit and push to GitHub
3. GitHub Actions automatically regenerates `docs/index.html`
4. Gallery updates within ~30 seconds

### Local Development
```bash
# Generate gallery locally
python3 generate_gallery.py

# Preview with live server
python3 -m http.server 8000
# Visit http://localhost:8000/docs/
```

## Dependencies

### Python
- Pillow (PIL) for image metadata extraction

### Browser
- Modern browser with IntersectionObserver support
- No external JavaScript libraries

## Future Improvements

Potential enhancements for later:
- Search/filter by filename
- Sort by date/size/name
- Tagging system
- Dark/light mode toggle
- Image download button
- Gallery statistics (total images, total size, etc.)

## Notes

- Paths use `../png/file.png` relative to `docs/` folder
- Works offline once loaded (no CDN dependencies)
- Vim-key navigation honors muscle memory
- Sidebar currently minimal - could be expanded with filters/stats
