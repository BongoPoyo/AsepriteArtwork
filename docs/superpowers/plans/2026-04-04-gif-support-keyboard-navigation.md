# GIF Support and Keyboard Navigation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a third "Gifs" section to the artwork gallery with full keyboard navigation support and section navigation buttons.

**Architecture:** Modify `generate-website.py` to scan three directories (showcase/, png/, gif/) and generate three distinct sections. Add navigation buttons to the top bar. Enhance CSS with focus indicators and skip link. Extend JavaScript with comprehensive keyboard shortcuts and focus management.

**Tech Stack:** Python 3, HTML5, CSS3 (CSS custom properties), vanilla JavaScript

---

## File Structure

**Files to modify:**
- `generate-website.py` - Add GIF directory scanning, three-section generation, navigation buttons
- `website/page.html` - Add skip link and navigation button placeholder
- `website/page.css` - Add focus indicators, skip link styling, smooth scroll, navigation button styling, empty state styling
- `website/page.js` - Add keyboard shortcuts (Home/End), focus trap, focus restoration

**No new files created** - All changes are modifications to existing files.

---

## Task 1: Fix GIF Path Bug in collect_images()

**Files:**
- Modify: `generate-website.py:67-73`

The current code incorrectly assigns `png/` prefix to all non-showcase files. GIFs from the `gif/` directory need their own prefix.

- [ ] **Step 1: Read the current collect_images() function**

Read lines 51-93 of `generate-website.py` to understand the current logic.

- [ ] **Step 2: Identify the bug**

Line 73 assigns `Path('png') / rel_path` for all non-showcase files. This causes GIFs to have incorrect paths like `png/flying-snowball.gif` instead of `gif/flying-snowball.gif`.

- [ ] **Step 3: Fix the path assignment logic**

Replace the path assignment section (lines 67-73) with:

```python
                    if base_dir == SHOWCASE_DIR:
                        rel_path = Path('showcase') / rel_path
                    elif base_dir == PNG_DIR:
                        rel_path = Path('png') / rel_path
                    elif base_dir == GIF_DIR:
                        rel_path = Path('gif') / rel_path
```

- [ ] **Step 4: Test the fix**

Run: `python3 generate-website.py`

Expected: Script completes without errors. Check `index.html` to verify GIF files now have `gif/` prefix in their paths.

- [ ] **Step 5: Commit**

```bash
git add generate-website.py
git commit -m "fix: correct path prefix for GIF files in gif/ directory"
```

---

## Task 2: Split Images into Three Categories

**Files:**
- Modify: `generate-website.py:145-165`

Currently the code splits images into two categories (showcase and other). We need three categories (showcase, other, gifs).

- [ ] **Step 1: Update main() to split images into three lists**

Replace the image splitting section (lines 151-164) with:

```python
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
```

- [ ] **Step 2: Test the split**

Run: `python3 generate-website.py`

Expected: Script completes. Verify the logic correctly categorizes images by checking the count of each type.

- [ ] **Step 3: Commit**

```bash
git add generate-website.py
git commit -m "refactor: split images into three categories (showcase, other, gifs)"
```

---

## Task 3: Update generate_gallery_html() for Three Sections

**Files:**
- Modify: `generate-website.py:95-132`

The function currently generates two sections. Update it to generate three sections with proper IDs and empty state handling.

- [ ] **Step 1: Update function signature**

Change line 95 from:

```python
def generate_gallery_html(showcase_images, other_images):
```

To:

```python
def generate_gallery_html(showcase_images, other_images, gif_images):
```

- [ ] **Step 2: Replace the entire function body**

Replace lines 96-132 with:

```python
def generate_gallery_html(showcase_images, other_images, gif_images):
    """Generate HTML for three-section gallery."""

    html = ""

    # Showcase section
    if showcase_images:
        html += '<h1 class="section-title" id="showcase">Artwork</h1>\n'
        html += '<div class="gallery">\n'

        for i, img in enumerate(showcase_images):
            html += f'''        <div class="image-card" tabindex="0" role="button" aria-label="View full-size: {img['filename']}" onclick="openLightbox({i})" onkeydown="if(event.key==='Enter') openLightbox({i})">
            <img class="thumbnail" data-src="{img['path']}" alt="{img['filename']}">
            <div class="image-info">
                <div class="filename" title="{img['filename']}">{img['filename']}</div>
                <div class="metadata">{img['width']} × {img['height']} • {img['size']}</div>
            </div>
        </div>\n'''

        html += '    </div>\n\n'
    else:
        html += '<h1 class="section-title" id="showcase">Artwork</h1>\n'
        html += '<p class="empty-state">No artwork yet</p>\n\n'

    # Other Artwork section
    offset = len(showcase_images)

    if other_images:
        html += '<h1 class="section-title" id="other">Other Artwork</h1>\n'
        html += '<div class="gallery">\n'

        for i, img in enumerate(other_images):
            html += f'''        <div class="image-card" tabindex="0" role="button" aria-label="View full-size: {img['filename']}" onclick="openLightbox({i + offset})" onkeydown="if(event.key==='Enter') openLightbox({i + offset})">
            <img class="thumbnail" data-src="{img['path']}" alt="{img['filename']}">
            <div class="image-info">
                <div class="filename" title="{img['filename']}">{img['filename']}</div>
                <div class="metadata">{img['width']} × {img['height']} • {img['size']}</div>
            </div>
        </div>\n'''

        html += '    </div>\n\n'
    else:
        html += '<h1 class="section-title" id="other">Other Artwork</h1>\n'
        html += '<p class="empty-state">No artwork yet</p>\n\n'

    # Gifs section
    offset = len(showcase_images) + len(other_images)

    if gif_images:
        html += '<h1 class="section-title" id="gifs">Gifs</h1>\n'
        html += '<div class="gallery">\n'

        for i, img in enumerate(gif_images):
            html += f'''        <div class="image-card" tabindex="0" role="button" aria-label="View full-size: {img['filename']}" onclick="openLightbox({i + offset})" onkeydown="if(event.key==='Enter') openLightbox({i + offset})">
            <img class="thumbnail" data-src="{img['path']}" alt="{img['filename']}">
            <div class="image-info">
                <div class="filename" title="{img['filename']}">{img['filename']}</div>
                <div class="metadata">{img['width']} × {img['height']} • {img['size']}</div>
            </div>
        </div>\n'''

        html += '    </div>\n'
    else:
        html += '<h1 class="section-title" id="gifs">Gifs</h1>\n'
        html += '<p class="empty-state">No artwork yet</p>\n'

    return html
```

- [ ] **Step 3: Update the function call in main()**

Change line 170 from:

```python
    gallery_html = generate_gallery_html(showcase_images, other_images)
```

To:

```python
    gallery_html = generate_gallery_html(showcase_images, other_images, gif_images)
```

- [ ] **Step 4: Test the generation**

Run: `python3 generate-website.py`

Expected: Script completes. Open `index.html` and verify:
- Three section titles exist: "Artwork", "Other Artwork", "Gifs"
- Each section has `id="showcase"`, `id="other"`, `id="gifs"`
- Image cards have `tabindex="0"`, `role="button"`, and `aria-label` attributes

- [ ] **Step 5: Commit**

```bash
git add generate-website.py
git commit -m "feat: add three-section gallery with GIF support and ARIA attributes"
```

---

## Task 4: Generate Navigation Buttons

**Files:**
- Modify: `generate-website.py:134-144` (add new function after `render_template()`)

Create a function to generate the navigation buttons HTML.

- [ ] **Step 1: Add generate_navigation_buttons() function**

Add this function after `render_template()` (after line 143):

```python
def generate_navigation_buttons():
    """Generate HTML for section navigation buttons."""
    return '''        <a href="#showcase" class="nav-button">Artwork</a>
        <a href="#other" class="nav-button">Other Artwork</a>
        <a href="#gifs" class="nav-button">Gifs</a>'''
```

- [ ] **Step 2: Update template rendering in main()**

Change line 179 from:

```python
    html_content = render_template(template, {
        "gallery": gallery_html,
        "image_data": js_data,
        "main_site": MAIN_SITE,
        "github_repo": GITHUB_REPO
    })
```

To:

```python
    html_content = render_template(template, {
        "gallery": gallery_html,
        "navigation_buttons": generate_navigation_buttons(),
        "image_data": js_data,
        "main_site": MAIN_SITE,
        "github_repo": GITHUB_REPO
    })
```

- [ ] **Step 3: Test navigation generation**

Run: `python3 generate-website.py`

Expected: Script completes. Check that navigation buttons HTML is generated (view source of `index.html`).

- [ ] **Step 4: Commit**

```bash
git add generate-website.py
git commit -m "feat: add navigation button generation"
```

---

## Task 5: Update HTML Template

**Files:**
- Modify: `website/page.html`

Add skip link and navigation buttons to the template.

- [ ] **Step 1: Add skip link after <body> tag**

Add this line immediately after `<body>` (after line 11):

```html
    <a href="#main-content" class="skip-link">Skip to content</a>
```

- [ ] **Step 2: Add id to main-content div**

Change line 17 from:

```html
<div class="main-content">
```

To:

```html
<div class="main-content" id="main-content">
```

- [ ] **Step 3: Update top bar with navigation**

Replace lines 13-15:

```html
<div class="top-bar">
    <a href="{{main_site}}" class="logo">[Back]</a>
</div>
```

With:

```html
<div class="top-bar">
    <a href="{{main_site}}" class="logo logo-large">[Back]</a>
    <nav class="section-nav">
        {{navigation_buttons}}
    </nav>
</div>
```

- [ ] **Step 4: Add ARIA attributes to lightbox**

Change line 39 from:

```html
<div id="lightbox" class="lightbox">
```

To:

```html
<div id="lightbox" class="lightbox" role="dialog" aria-modal="true" aria-label="Image viewer">
```

- [ ] **Step 5: Add aria-label to close button**

Change line 41 from:

```html
        <button class="close-btn" onclick="closeLightbox()">&times;</button>
```

To:

```html
        <button class="close-btn" onclick="closeLightbox()" aria-label="Close lightbox">&times;</button>
```

- [ ] **Step 6: Test template changes**

Run: `python3 generate-website.py`

Expected: Script completes. Open `index.html` and verify:
- Skip link present at top of body
- Main content div has `id="main-content"`
- Top bar contains both logo and navigation
- Lightbox has ARIA attributes

- [ ] **Step 7: Commit**

```bash
git add website/page.html
git commit -m "feat: add skip link, navigation buttons, and ARIA attributes to template"
```

---

## Task 6: Add CSS for Focus Indicators

**Files:**
- Modify: `website/page.css`

Add visible focus indicators for all interactive elements.

- [ ] **Step 1: Add focus-visible styles**

Add these rules after the `*` selector block (after line 22):

```css

/* Focus indicators */
*:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
}

/* Remove default outline for mouse users */
*:focus:not(:focus-visible) {
    outline: none;
}
```

- [ ] **Step 2: Test focus indicators**

Run: `python3 generate-website.py && python3 -m http.server 8000`
Visit `http://localhost:8000` and press Tab multiple times.

Expected: Each interactive element (logo, nav buttons, thumbnails) shows a visible pink outline when focused.

- [ ] **Step 3: Commit**

```bash
git add website/page.css
git commit -m "a11y: add visible focus indicators for keyboard navigation"
```

---

## Task 7: Add CSS for Skip Link

**Files:**
- Modify: `website/page.css`

Add styling for the skip link that hides it until focused.

- [ ] **Step 1: Add skip link styles**

Add these rules after the focus indicators (after the focus styles you just added):

```css

/* Skip link */
.skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    background: var(--darker-bg);
    color: var(--accent);
    padding: 8px 16px;
    text-decoration: none;
    z-index: 3000;
    transition: top 0.3s;
    font-weight: 600;
}

.skip-link:focus {
    top: 0;
}
```

- [ ] **Step 2: Test skip link**

Run: `python3 generate-website.py && python3 -m http.server 8000`
Visit `http://localhost:8000` and press Tab once.

Expected: Skip link appears at the top of the page. Pressing Enter jumps to main content.

- [ ] **Step 3: Commit**

```bash
git add website/page.css
git commit -m "a11y: add skip link for keyboard users"
```

---

## Task 8: Add CSS for Smooth Scrolling

**Files:**
- Modify: `website/page.css`

Add smooth scrolling for anchor navigation and scroll padding for the fixed header.

- [ ] **Step 1: Update html selector**

Replace the `html` block (lines 24-26) with:

```css
html {
    scrollbar-gutter: stable both-edges;
    scroll-behavior: smooth;
    scroll-padding-top: 80px;
}
```

- [ ] **Step 2: Test smooth scrolling**

Run: `python3 generate-website.py && python3 -m http.server 8000`
Visit `http://localhost:8000` and click on navigation buttons.

Expected: Page smoothly scrolls to each section, accounting for the fixed header height.

- [ ] **Step 3: Commit**

```bash
git add website/page.css
git commit -m "ux: add smooth scrolling for anchor navigation"
```

---

## Task 9: Add CSS for Navigation Buttons

**Files:**
- Modify: `website/page.css`

Style the navigation buttons to match the current logo design.

- [ ] **Step 1: Add navigation button styles**

Add these rules after the `.logo` selector (after line 66):

```css

.section-nav {
    display: flex;
    gap: 15px;
}

.nav-button {
    font-size: 24px;
    font-weight: bold;
    color: var(--text);
    text-decoration: none;
    transition: color 0.2s, transform 0.2s;
}

.nav-button:hover {
    color: var(--accent);
    transform: scale(1.05);
}
```

- [ ] **Step 2: Update logo-large size**

Add a new rule after the `.logo` block:

```css

.logo-large {
    font-size: 32px;
}
```

- [ ] **Step 3: Test navigation button styling**

Run: `python3 generate-website.py && python3 -m http.server 8000`
Visit `http://localhost:8000`.

Expected:
- [Back] button is larger (32px)
- Navigation buttons are same size as original logo (24px)
- All buttons show hover effects with color change and scale

- [ ] **Step 4: Commit**

```bash
git add website/page.css
git commit -m "style: add navigation button styling with hover effects"
```

---

## Task 10: Add CSS for Empty State

**Files:**
- Modify: `website/page.css`

Add styling for empty section messages.

- [ ] **Step 1: Add empty state styles**

Add these rules after the `.section-title` block (after line 193):

```css

.empty-state {
    text-align: center;
    color: var(--muted);
    padding: 40px 20px;
    font-style: italic;
    font-size: 1.1rem;
}
```

- [ ] **Step 2: Test empty state (temporarily)**

To test, temporarily rename the `gif/` directory:
```bash
mv gif gif.bak
python3 generate-website.py
mv gif.bak gif
```

Visit `http://localhost:8000` and scroll to Gifs section.

Expected: "No artwork yet" message displayed in muted color, centered, italic.

- [ ] **Step 3: Commit**

```bash
git add website/page.css
git commit -m "style: add empty state message styling"
```

---

## Task 11: Add Keyboard Shortcuts (Home/End) to JavaScript

**Files:**
- Modify: `website/page.js:82-118`

Add Home and End key support for jumping to first/last image in lightbox.

- [ ] **Step 1: Update keyboard event handler**

Replace the entire switch statement in the keydown handler (lines 92-117) with:

```javascript
    // Lightbox is active → handle navigation
    switch (e.key) {
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
            navigate(-getGridColumns());
            break;

        case 'ArrowDown':
        case 'j':
            navigate(getGridColumns());
            break;

        case 'Home':
            showImage(0);
            e.preventDefault();
            break;

        case 'End':
            showImage(imageData.length - 1);
            e.preventDefault();
            break;

        case 'Escape':
        case 'q':
            closeLightbox();
            break;
    }
```

- [ ] **Step 2: Test Home/End keys**

Run: `python3 generate-website.py && python3 -m http.server 8000`
Visit `http://localhost:8000`, open any image, and press:
- `Home` - should go to first image
- `End` - should go to last image

Expected: Lightbox jumps to first/last image respectively.

- [ ] **Step 3: Commit**

```bash
git add website/page.js
git commit -m "a11y: add Home/End keyboard shortcuts for lightbox navigation"
```

---

## Task 12: Add Focus Trap to Lightbox

**Files:**
- Modify: `website/page.js`

Prevent keyboard users from tabbing outside the lightbox when it's open.

- [ ] **Step 1: Add trapFocus() function**

Add this function after the `navigate()` function (after line 79):

```javascript
// Trap focus within lightbox
function trapFocus() {
    const lightbox = document.getElementById('lightbox');
    if (!lightbox) return;

    const focusableElements = lightbox.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];

    const handleTabKey = (e) => {
        if (e.key !== 'Tab') return;

        if (e.shiftKey) {
            if (document.activeElement === firstElement) {
                e.preventDefault();
                lastElement.focus();
            }
        } else {
            if (document.activeElement === lastElement) {
                e.preventDefault();
                firstElement.focus();
            }
        }
    };

    lightbox.addEventListener('keydown', handleTabKey);
}
```

- [ ] **Step 2: Call trapFocus() when lightbox opens**

Add `trapFocus()` call at the end of `openLightbox()` function (after line 48):

```javascript
    lightbox.classList.add('active');
    document.body.style.overflow = 'hidden';
    trapFocus();
```

- [ ] **Step 3: Test focus trap**

Run: `python3 generate-website.py && python3 -m http.server 8000`
Visit `http://localhost:8000`, open lightbox, press Tab repeatedly.

Expected: Focus cycles within the lightbox (close button, image, etc.) and doesn't escape to the background page.

- [ ] **Step 4: Commit**

```bash
git add website/page.js
git commit -m "a11y: add focus trap to lightbox for keyboard navigation"
```

---

## Task 13: Add Focus Restoration on Lightbox Close

**Files:**
- Modify: `website/page.js`

Remember which element had focus before opening lightbox and restore focus when closing.

- [ ] **Step 1: Add focus tracking variable**

Add at the top of the file after `let currentIndex = 0;` (after line 4):

```javascript
let lastFocusedElement = null;
```

- [ ] **Step 2: Save focus when opening lightbox**

Add this line at the start of `openLightbox()` function (after line 34):

```javascript
    lastFocusedElement = document.activeElement;
```

- [ ] **Step 3: Restore focus when closing lightbox**

Add this line at the end of `closeLightbox()` function (after line 55):

```javascript
    if (lastFocusedElement) {
        lastFocusedElement.focus();
    }
```

- [ ] **Step 4: Test focus restoration**

Run: `python3 generate-website.py && python3 -m http.server 8000`
Visit `http://localhost:8000`, Tab to a specific thumbnail, press Enter to open lightbox, press Escape to close.

Expected: Focus returns to the same thumbnail that was clicked.

- [ ] **Step 5: Commit**

```bash
git add website/page.js
git commit -m "a11y: restore focus to thumbnail after closing lightbox"
```

---

## Task 14: Remove Auto-Open on Keypress

**Files:**
- Modify: `website/page.js:82-89`

The current code auto-opens the lightbox on any keypress when it's closed. This interferes with keyboard navigation.

- [ ] **Step 1: Remove auto-open behavior**

Replace lines 85-89:

```javascript
    // If lightbox isn't active, open first image on any key press
    if (!lightbox.classList.contains('active')) {
        openLightbox(0);
        return; // stop processing this key
    }
```

With:

```javascript
    // Only handle keys when lightbox is active
    if (!lightbox.classList.contains('active')) {
        return;
    }
```

- [ ] **Step 2: Test keyboard navigation without auto-open**

Run: `python3 generate-website.py && python3 -m http.server 8000`
Visit `http://localhost:8000`, don't open lightbox, press random keys.

Expected: Nothing happens. Lightbox only opens when clicking/activating an image.

- [ ] **Step 3: Commit**

```bash
git add website/page.js
git commit -m "fix: remove auto-open lightbox on keypress"
```

---

## Task 15: Final Integration Testing

**Files:**
- Test all components together

- [ ] **Step 1: Generate final site**

Run: `python3 generate-website.py`

Expected: No errors or warnings.

- [ ] **Step 2: Test all sections**

Visit `http://localhost:8000` and verify:
- Three sections exist: "Artwork", "Other Artwork", "Gifs"
- GIFs animate in thumbnails and lightbox
- Empty sections show "No artwork yet" (if any)

- [ ] **Step 3: Test navigation buttons**

Click each navigation button:
- [Artwork] jumps to Artwork section
- [Other Artwork] jumps to Other Artwork section
- [Gifs] jumps to Gifs section

Expected: Smooth scroll to each section, header doesn't overlap content.

- [ ] **Step 4: Test keyboard navigation (Tab)**

Press Tab repeatedly through the entire page:
1. Skip link appears
2. [Back] button focuses
3. [Artwork] button focuses
4. [Other Artwork] button focuses
5. [Gifs] button focuses
6. Each thumbnail focuses in order

Expected: Visible focus indicator on each element, logical tab order.

- [ ] **Step 5: Test keyboard navigation (Enter/Space)**

Tab to a thumbnail, press Enter.

Expected: Lightbox opens showing that image.

- [ ] **Step 6: Test lightbox keyboard shortcuts**

Open lightbox, test each key:
- `Escape` - closes lightbox
- `Left Arrow` or `h` - previous image
- `Right Arrow` or `l` - next image
- `Home` - first image
- `End` - last image

Expected: All shortcuts work correctly.

- [ ] **Step 7: Test focus trap**

With lightbox open, press Tab repeatedly.

Expected: Focus cycles within lightbox, doesn't escape to background.

- [ ] **Step 8: Test focus restoration**

1. Tab to a specific thumbnail (remember which one)
2. Press Enter to open lightbox
3. Press Escape to close lightbox
4. Verify focus is back on the same thumbnail

Expected: Focus returns to the thumbnail that was clicked.

- [ ] **Step 9: Test skip link**

1. Refresh page
2. Press Tab once
3. Press Enter

Expected: Page jumps to main content area.

- [ ] **Step 10: Test with actual GIFs**

Verify the three GIF files in `gif/` directory:
- flying-snowball.gif
- orange-run.gif
- suicidal-boy.gif

Expected: All GIFs appear in Gifs section, animate in thumbnails and lightbox.

- [ ] **Step 11: Check for console errors**

Open browser DevTools Console, reload page, interact with everything.

Expected: No console errors or warnings.

- [ ] **Step 12: Final commit**

```bash
git add index.html
git commit -m "chore: update generated index.html with GIF support and keyboard navigation"
```

---

## Task 16: Cleanup Documentation

**Files:**
- Remove: `docs/` directory

- [ ] **Step 1: Remove docs directory**

Run: `rm -rf docs/`

- [ ] **Step 2: Verify removal**

Run: `ls -la`

Expected: No `docs/` directory exists.

- [ ] **Step 3: Commit cleanup**

```bash
git add -A
git commit -m "chore: remove temporary documentation files"
```

---

## Testing Checklist

After completing all tasks, verify:

- [ ] All three sections display correctly with proper IDs
- [ ] GIFs animate in thumbnails and lightbox
- [ ] Empty sections show "No artwork yet" message
- [ ] Navigation buttons jump to correct sections with smooth scroll
- [ ] Tab key navigates through all interactive elements in logical order
- [ ] Focus indicators (pink outline) visible on all focused elements
- [ ] Skip link appears on first Tab press
- [ ] Lightbox keyboard shortcuts work (Escape, arrows, h/j/k/l, Home/End)
- [ ] Focus trap keeps Tab within lightbox when open
- [ ] Focus returns to thumbnail after closing lightbox
- [ ] All images display with correct metadata (dimensions × file size)
- [ ] No console errors
- [ ] Works with mouse-only navigation
- [ ] Works with keyboard-only navigation

---

## Completion

All tasks completed. The gallery now supports:
- Three distinct sections (Artwork, Other Artwork, Gifs)
- Animated GIF thumbnails and lightbox viewing
- Navigation buttons for quick section access
- Full keyboard navigation and accessibility
- Focus management and ARIA attributes
- Empty state handling
