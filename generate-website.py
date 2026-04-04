#!/usr/bin/env python3
"""
Generate static HTML gallery for Aseprite artwork.
Scans showcase/ and png/ directory and creates index.html with all images.
"""

import os
import json
from pathlib import Path

PNG_DIR = Path("png")
GIF_DIR = Path("gif")
SHOWCASE_DIR = Path("showcase")


TEMPLATE_FILE = Path("website/page.html")
OUTPUT_FILE = Path("index.html")

GITHUB_REPO = "https://github.com/BongoPoyo/Artwork"
MAIN_SITE = "https://bongopoyo.github.io/"

SUPPORTED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.webp', '.gif')

# def get_images(directory: Path):
#     """Return sorted list of PNG files in a directory."""
#     if not directory.exists():
#         return []

#     return sorted([
#         f for f in directory.iterdir()
#         if f.suffix.lower() == ".png"
#     ])


def render_images(images, base_path):
    """Convert image list to HTML <img> tags."""
    html = ""
    for img in images:
        html += f'<img src="{base_path}/{img.name}" loading="lazy">\n'
    return html

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

    for base_dir in [SHOWCASE_DIR, PNG_DIR, GIF_DIR]:
        if not base_dir.exists():
            continue
        
        for root, dirs, files in os.walk(base_dir):
            for filename in sorted(files):
                if filename.lower().endswith(SUPPORTED_EXTENSIONS):
                    filepath = Path(root) / filename
                    # Get path relative to png/ directory
                    rel_path = filepath.relative_to(base_dir)

                    if base_dir == SHOWCASE_DIR:
                        rel_path = Path('showcase') / rel_path
                    elif base_dir == PNG_DIR:
                        rel_path = Path('png') / rel_path
                    elif base_dir == GIF_DIR:
                        rel_path = Path('gif') / rel_path

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

def generate_gallery_html(showcase_images, other_images, gif_images):
    """Generate HTML for three-section gallery."""

    html = ""

    # Artwork section
    if showcase_images:
        html += '<h1 id="showcase" class="section-title">Artwork</h1>\n'
        html += '<div class="gallery">\n'

        for i, img in enumerate(showcase_images):
            html += f'''        <div class="image-card" tabindex="0" role="button" aria-label="View {img['filename']}" onclick="openLightbox({i})">
            <img class="thumbnail" data-src="{img['path']}" alt="{img['filename']}">
            <div class="image-info">
                <div class="filename" title="{img['filename']}">{img['filename']}</div>
                <div class="metadata">{img['width']} × {img['height']} • {img['size']}</div>
            </div>
        </div>\n'''

        html += '    </div>\n\n'
    else:
        html += '<h1 id="showcase" class="section-title">Artwork</h1>\n'
        html += '<p class="empty-state">No artwork yet.</p>\n\n'

    # Other Artwork section
    if other_images:
        offset = len(showcase_images)

        html += '<h1 id="other" class="section-title">Other Artwork</h1>\n'
        html += '<div class="gallery">\n'

        for i, img in enumerate(other_images):
            html += f'''        <div class="image-card" tabindex="0" role="button" aria-label="View {img['filename']}" onclick="openLightbox({i + offset})">
            <img class="thumbnail" data-src="{img['path']}" alt="{img['filename']}">
            <div class="image-info">
                <div class="filename" title="{img['filename']}">{img['filename']}</div>
                <div class="metadata">{img['width']} × {img['height']} • {img['size']}</div>
            </div>
        </div>\n'''

        html += '    </div>\n\n'
    else:
        html += '<h1 id="other" class="section-title">Other Artwork</h1>\n'
        html += '<p class="empty-state">No other artwork yet.</p>\n\n'

    # GIFs section
    if gif_images:
        offset = len(showcase_images) + len(other_images)

        html += '<h1 id="gifs" class="section-title">Gifs</h1>\n'
        html += '<div class="gallery">\n'

        for i, img in enumerate(gif_images):
            html += f'''        <div class="image-card" tabindex="0" role="button" aria-label="View {img['filename']}" onclick="openLightbox({i + offset})">
            <img class="thumbnail" data-src="{img['path']}" alt="{img['filename']}">
            <div class="image-info">
                <div class="filename" title="{img['filename']}">{img['filename']}</div>
                <div class="metadata">{img['width']} × {img['height']} • {img['size']}</div>
            </div>
        </div>\n'''

        html += '    </div>\n'
    else:
        html += '<h1 id="gifs" class="section-title">Gifs</h1>\n'
        html += '<p class="empty-state">No gifs yet.</p>\n'

    return html

def load_template():
    if not TEMPLATE_FILE.exists():
        raise FileNotFoundError(f"{TEMPLATE_FILE} not found")
    return TEMPLATE_FILE.read_text()


def render_template(template: str, context: dict):
    for key, value in context.items():
        template = template.replace(f"{{{{{key}}}}}", value)
    return template

def main():
    print("🎨 Generating Artwork Gallery...")

    all_images = collect_images()
    print(f"📸 Found {len(all_images)} images")

    showcase_images = []
    other_images = []
    gif_images = []

    # Split by directory
    for img in all_images:
        if img['path'].startswith('showcase/'):
            showcase_images.append(img)
        elif img['path'].startswith('gif/'):
            gif_images.append(img)
        elif img['path'].startswith('png/'):
            other_images.append(img)

    # Maintain ordering consistency
    image_data = showcase_images + other_images + gif_images

    # Generate gallery HTML
    gallery_html = generate_gallery_html(showcase_images, other_images, gif_images)

    # Proper JSON (IMPORTANT FIX)
    js_data = json.dumps(image_data)

    # Load template
    template = load_template()

    # Inject values
    html_content = render_template(template, {
        "gallery": gallery_html,
        "image_data": js_data,
        "main_site": MAIN_SITE,
        "github_repo": GITHUB_REPO
    })

    # Write output
    OUTPUT_FILE.write_text(html_content)

    print(f"✅ Generated {OUTPUT_FILE}")


if __name__ == '__main__':
    main()
