#!/usr/bin/env python3
"""
Generate static HTML gallery for Aseprite artwork.
Scans png/ directory and creates docs/index.html with all images.
"""

import os
from pathlib import Path

PNG_DIR = Path("png")
OUTPUT_FILE = Path("docs/index.html")
GITHUB_REPO = "https://github.com/BongoPoyo/AsepriteArtwork"
MAIN_SITE = "https://bongopoyo.github.io/"

# Catppuccin theme colors from user's site
CSS = f"""
:root {{
    --background: #1e1e2e;
    --surface: #313244;
    --text: #cdd6f4;
    --accent: #f5c2e7;
    --accent-hover: #f8a1f1;
    --shadow: rgba(0, 0, 0, 0.5);
    --darker-bg: #181825;
    --muted: #7f849c;
    --card-hover: #3b3b5a;
    --bottom-bg: #11111b;
}}

*, *::before, *::after {{
    box-sizing: border-box;
    color: var(--text);
}}

* {{
    margin: 0;
    padding: 0;
}}

html {{
    scrollbar-gutter: stable both-edges;
}}

body {{
    font-family: "Segoe UI", "Fira Code", monospace;
    background-color: var(--background);
    color: var(--text);
    min-height: 100vh;
    padding: 80px 20px 100px 20px;
}}

/* Top Bar */
.top-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: var(--darker-bg);
    color: var(--text);
    padding: 12px 24px;
    position: fixed;
    top: 0;
    width: 100%;
    box-shadow: 0 2px 4px #7f849c;
    z-index: 1000;
    transition: background 0.3s;
}}

.logo {{
    font-size: 24px;
    font-weight: bold;
    color: var(--accent);
    transition: ease-in 0.2s;
    text-decoration: none;
}}

.logo:hover {{
    transform: scale(1.05);
}}

.menu-btn {{
    background: transparent;
    color: var(--text);
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
}}

/* Sidebar */
.side-bar {{
    position: fixed;
    top: 0;
    right: 0;
    width: 250px;
    height: 100%;
    background-color: var(--surface);
    color: var(--text);
    box-shadow: -3px 0 15px rgba(0,0,0,0.5);
    display: flex;
    flex-direction: column;
    padding: 60px 20px;
    gap: 20px;
    transform: translateX(250px);
    transition: transform 0.3s ease;
    z-index: 500;
}}

.side-bar.active {{
    transform: translateX(0);
}}

.side-bar p {{
    text-align: left;
    font-size: 0.9rem;
}}

/* Main Content */
.main-content {{
    transition: transform 0.3s ease;
}}

body.side-bar-open .main-content {{
    margin-right: 250px;
    transition: margin-right 0.3s ease;
}}

/* Header */
.header-content {{
    text-align: center;
    margin-bottom: 40px;
    padding: 20px;
}}

h1 {{
    color: var(--accent);
    font-size: 2.5rem;
    margin-bottom: 10px;
    margin-top: 0;
}}

.description {{
    color: var(--muted);
    font-size: 1.1rem;
    margin-bottom: 20px;
}}

.links {{
    display: flex;
    justify-content: center;
    gap: 20px;
    flex-wrap: wrap;
}}

.links a {{
    color: var(--text);
    text-decoration: none;
    padding: 8px 16px;
    border-radius: 8px;
    background-color: var(--surface);
    transition: background-color 0.2s, color 0.2s;
}}

.links a:hover {{
    background-color: var(--card-hover);
    color: var(--accent);
}}

/* Gallery */
.gallery {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 24px;
    max-width: 1600px;
    margin: 0 auto;
    padding: 20px;
}}

.image-card {{
    background-color: var(--surface);
    border-radius: 12px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}}

.image-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 10px 30px var(--shadow);
}}

.image-card:hover .thumbnail {{
    transform: scale(1.05);
    box-shadow: 0 0 20px var(--accent);
}}

.thumbnail {{
    width: 250px;
    height: 250px;
    object-fit: contain;
    border-radius: 8px;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    background-color: var(--darker-bg);
}}

.image-info {{
    margin-top: 12px;
    text-align: center;
    width: 100%;
}}

.filename {{
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 4px;
    word-break: break-word;
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}}

.filename:hover {{
    overflow: visible;
    white-space: normal;
}}

.metadata {{
    font-size: 0.8rem;
    color: var(--muted);
    font-family: "Fira Code", monospace;
}}

/* Lightbox */
.lightbox {{
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.9);
    z-index: 9999;
    justify-content: center;
    align-items: center;
    opacity: 0;
    transition: opacity 0.2s ease;
}}

.lightbox.active {{
    display: flex;
    opacity: 1;
}}

.lightbox-content {{
    position: relative;
    max-width: 90%;
    max-height: 90%;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

.lightbox-image {{
    max-width: 100%;
    max-height: 85vh;
    object-fit: contain;
    border-radius: 8px;
}}

.lightbox-info {{
    margin-top: 16px;
    text-align: center;
    color: var(--text);
}}

.lightbox-filename {{
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 8px;
}}

.lightbox-metadata {{
    font-size: 0.9rem;
    color: var(--muted);
    font-family: "Fira Code", monospace;
}}

.close-btn {{
    position: absolute;
    top: -40px;
    right: 0;
    background: none;
    border: none;
    color: var(--text);
    font-size: 2rem;
    cursor: pointer;
    padding: 8px;
    line-height: 1;
    transition: color 0.2s;
}}

.close-btn:hover {{
    color: var(--accent);
}}

.no-images {{
    text-align: center;
    color: var(--muted);
    font-size: 1.5rem;
    padding: 60px 20px;
}}

/* Bottom Bar */
.bottom-bar {{
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: var(--bottom-bg);
    color: var(--text);
    padding: 12px 12px;
    position: fixed;
    bottom: 0;
    width: 100%;
    left: 0;
    right: 0;
    box-shadow: none;
    flex-wrap: wrap;
    gap: 8px 16px;
    z-index: 1000;
    transition: background 0.3s;
    text-align: center;
}}

.socials {{
    display: flex;
    margin: 0 auto;
    flex-wrap: wrap;
    gap: 8px 16px;
    justify-content: center;
    align-items: center;
    text-align: center;
}}

.socials a {{
    color: var(--muted);
    font-size: 20px;
    text-decoration: none;
    transition: color 0.2s ease, transform 0.15s ease;
}}

.socials a[href*="youtube"]:hover   {{ color: #f38ba8; }}
.socials a[href*="github"]:hover    {{ color: #cdd6f4; }}
.socials a[href*="itch"]:hover      {{ color: #fab387; }}
.socials a[href*="mastodon"]:hover  {{ color: #89b4fa; }}
.socials a[href*="bsky"]:hover      {{ color: #89dceb; }}
.socials a[href*="matrix"]:hover    {{ color: #a6e3a1; }}
.socials a[href*="mailto"]:hover    {{ color: #eba0ac; }}
.socials a[href*="discord"]:hover   {{ color: #74c7ec; }}

.socials a:hover {{
    color: var(--text);
    transform: translateY(-2px);
    text-decoration-line: underline;
}}

/* Mobile responsive */
@media (max-width: 768px) {{
    body {{
        padding: 80px 10px 120px 10px;
    }}

    .gallery {{
        grid-template-columns: 1fr;
        padding: 10px;
    }}

    h1 {{
        font-size: 2rem;
    }}

    .description {{
        font-size: 1rem;
    }}

    .links {{
        flex-direction: column;
        align-items: center;
    }}

    .thumbnail {{
        width: 100%;
        max-width: 350px;
        height: auto;
        aspect-ratio: 1;
    }}

    .bottom-bar {{
        padding: 16px 8px;
    }}

    .socials {{
        gap: 6px 12px;
    }}

    .socials a {{
        font-size: 16px;
    }}
}}

@media (min-width: 769px) and (max-width: 1199px) {{
    .gallery {{
        grid-template-columns: repeat(3, 1fr);
    }}
}}

@media (min-width: 1200px) {{
    .gallery {{
        grid-template-columns: repeat(5, 1fr);
    }}
}}
"""

JAVASCRIPT = """
// Image data for navigation
const imageData = __IMAGE_DATA__;

let currentIndex = 0;

// Get current grid column count based on window width
function getGridColumns() {
    const width = window.innerWidth;
    if (width >= 1200) return 5;
    if (width >= 769) return 3;
    return 1;
}

// Menu functionality
const menuBtn = document.querySelector('.menu-btn');
const sidebar = document.querySelector('.side-bar');
const body = document.body;

menuBtn.addEventListener('click', () => {
    sidebar.classList.toggle('active');
    body.classList.toggle('side-bar-open');
});

// Close sidebar if clicking outside
body.addEventListener('click', (e) => {
    if (!sidebar.contains(e.target) && !menuBtn.contains(e.target)) {
        sidebar.classList.remove('active');
        body.classList.remove('side-bar-open');
    }
});

// Lazy load images
document.addEventListener('DOMContentLoaded', () => {
    const images = document.querySelectorAll('.thumbnail[data-src]');

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
});

// Lightbox functions
function openLightbox(index) {
    currentIndex = index;
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-image');
    const filename = document.getElementById('lightbox-filename');
    const metadata = document.getElementById('lightbox-metadata');

    const data = imageData[index];
    lightboxImg.src = data.path;
    filename.textContent = data.filename;
    metadata.textContent = `${data.width} × ${data.height} • ${data.size}`;

    lightbox.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    const lightbox = document.getElementById('lightbox');
    lightbox.classList.remove('active');
    document.body.style.overflow = '';
}

function showImage(index) {
    if (index < 0) index = imageData.length - 1;
    if (index >= imageData.length) index = 0;

    currentIndex = index;
    const lightboxImg = document.getElementById('lightbox-image');
    const filename = document.getElementById('lightbox-filename');
    const metadata = document.getElementById('lightbox-metadata');

    const data = imageData[index];
    lightboxImg.src = data.path;
    filename.textContent = data.filename;
    metadata.textContent = `${data.width} × ${data.height} • ${data.size}`;
}

function navigate(direction) {
    showImage(currentIndex + direction);
}

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    const lightbox = document.getElementById('lightbox');
    if (!lightbox.classList.contains('active')) return;

    switch(e.key) {
        case 'ArrowLeft':
        case 'h':
            navigate(-1);
            break;
        case 'ArrowRight':
        case 'l':
            navigate(1);
            break;
        case 'ArrowUp':
        case 'k':
            // Navigate up by row (adapts to current grid size)
            navigate(-getGridColumns());
            break;
        case 'ArrowDown':
        case 'j':
            // Navigate down by row (adapts to current grid size)
            navigate(getGridColumns());
            break;
        case 'q':
        case 'Escape':
            closeLightbox();
            break;
    }
});

// Close lightbox on click outside
document.getElementById('lightbox').addEventListener('click', (e) => {
    if (e.target.id === 'lightbox') {
        closeLightbox();
    }
});
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aseprite Artwork</title>
    <style>
{css}
    </style>
</head>
<body>
    <div class="top-bar">
        <a href="/" class="logo">[Aseprite Artwork]</a>
        <button class="menu-btn">☰</button>
    </div>

    <div class="side-bar">
        <p>My Aseprite artwork collection 🎨</p>
        <p>Generated automatically from the png/ folder</p>
    </div>

    <div class="main-content">
        <div class="header-content">
            <h1>Aseprite Artwork</h1>
            <p class="description">Consists of .png and .ase of my aseprite artwork</p>
            <div class="links">
                <a href="{main_site}" target="_blank">Main Website</a>
                <a href="{github_repo}" target="_blank">GitHub Repo</a>
            </div>
        </div>

        <main>
{gallery}
        </main>
    </div>

    <div class="bottom-bar">
        <div class="socials">
            <a href="https://bongopoyo.itch.io/" aria-label="itch.io">Itch</a>
            <a href="https://www.youtube.com/@bongopoyo" aria-label="YouTube">YouTube</a>
            <a href="https://github.com/bongopoyo" aria-label="GitHub">GitHub</a>
            <a href="https://bsky.app/profile/bongopoyo.bsky.social" aria-label="Bluesky">BlueSky</a>
            <a href="https://mastodon.social/@bongopoyo" aria-label="Mastodon">Mastodon</a>
            <a href="mailto:bongopoyo@proton.me" aria-label="Email">Email</a>
            <a href="https://matrix.to/#/@bongopoyo:matrix.org" aria-label="Matrix">Matrix</a>
            <a href="https://discord.gg/cDxfzC28EZ" aria-label="Discord">Discord</a>
        </div>
    </div>

    <div id="lightbox" class="lightbox">
        <div class="lightbox-content">
            <button class="close-btn" onclick="closeLightbox()">&times;</button>
            <img id="lightbox-image" class="lightbox-image" src="" alt="">
            <div class="lightbox-info">
                <div id="lightbox-filename" class="lightbox-filename"></div>
                <div id="lightbox-metadata" class="lightbox-metadata"></div>
            </div>
        </div>
    </div>

    <script>
{javascript}
    </script>
</body>
</html>
"""


def format_size(bytes_size):
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"


def collect_images():
    """Scan png directory and collect image metadata."""
    images = []

    if not PNG_DIR.exists():
        print(f"⚠️  Warning: {PNG_DIR} directory not found")
        return images

    for root, dirs, files in os.walk(PNG_DIR):
        for filename in sorted(files):
            if filename.lower().endswith('.png'):
                filepath = Path(root) / filename
                rel_path = filepath.relative_to(PNG_DIR.parent)
                # Prepend ../ since HTML is in docs/ folder
                rel_path = Path('..') / rel_path

                try:
                    from PIL import Image
                    with Image.open(filepath) as img:
                        width, height = img.size
                except Exception as e:
                    print(f"⚠️  Warning: Could not read {filepath}: {e}")
                    continue

                file_size = filepath.stat().st_size

                images.append({
                    'filename': filename,
                    'path': str(rel_path),
                    'width': width,
                    'height': height,
                    'size': format_size(file_size)
                })

    return images


def generate_gallery_html(images):
    """Generate HTML for image gallery."""
    if not images:
        return '<div class="no-images">No images found in png/ directory</div>'

    gallery_items = []
    for i, img in enumerate(images):
        gallery_items.append(f'''        <div class="image-card" onclick="openLightbox({i})">
            <img class="thumbnail" data-src="{img['path']}" alt="{img['filename']}" loading="lazy">
            <div class="image-info">
                <div class="filename" title="{img['filename']}">{img['filename']}</div>
                <div class="metadata">{img['width']} × {img['height']} • {img['size']}</div>
            </div>
        </div>''')

    return '<div class="gallery">\n' + '\n'.join(gallery_items) + '\n    </div>'


def main():
    """Generate the gallery HTML."""
    print("🎨 Generating Aseprite Artwork Gallery...")

    # Create docs directory if it doesn't exist
    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    # Collect images
    images = collect_images()
    print(f"📸 Found {len(images)} images")

    # Generate gallery HTML
    gallery_html = generate_gallery_html(images)

    # Prepare JavaScript with image data
    js_data = str(images).replace("'", '"')
    javascript = JAVASCRIPT.replace('__IMAGE_DATA__', js_data)

    # Generate full HTML
    html_content = HTML_TEMPLATE.format(
        css=CSS,
        gallery=gallery_html,
        javascript=javascript,
        main_site=MAIN_SITE,
        github_repo=GITHUB_REPO
    )

    # Write to file
    OUTPUT_FILE.write_text(html_content)
    print(f"✅ Generated {OUTPUT_FILE} with {len(images)} images")


if __name__ == '__main__':
    main()
