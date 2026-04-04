// imageData is injected from HTML:
// <script>const imageData = [...];</script>

let currentIndex = 0;

// Determine grid columns (must match CSS breakpoints)
function getGridColumns() {
    const width = window.innerWidth;
    if (width >= 1200) return 5;
    if (width >= 769) return 3;
    return 1;
}

// Lazy loading
document.addEventListener('DOMContentLoaded', () => {
    const images = document.querySelectorAll('.thumbnail[data-src]');

    const observer = new IntersectionObserver((entries, obs) => {
        for (const entry of entries) {
            if (!entry.isIntersecting) continue;

            const img = entry.target;
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
            obs.unobserve(img);
        }
    });

    images.forEach(img => observer.observe(img));
});

// Lightbox open
function openLightbox(index) {
    currentIndex = index;

    const lightbox = document.getElementById('lightbox');
    const img = document.getElementById('lightbox-image');
    const filename = document.getElementById('lightbox-filename');
    const metadata = document.getElementById('lightbox-metadata');

    const data = imageData[index];

    img.src = data.path;
    filename.textContent = data.filename;
    metadata.textContent = `${data.width} × ${data.height} • ${data.size}`;

    lightbox.classList.add('active');
    document.body.style.overflow = 'hidden';
    trapFocus();
}

// Close lightbox
function closeLightbox() {
    const lightbox = document.getElementById('lightbox');
    lightbox.classList.remove('active');
    document.body.style.overflow = '';
}

// Change image
function showImage(index) {
    if (index < 0) index = imageData.length - 1;
    if (index >= imageData.length) index = 0;

    currentIndex = index;

    const img = document.getElementById('lightbox-image');
    const filename = document.getElementById('lightbox-filename');
    const metadata = document.getElementById('lightbox-metadata');

    const data = imageData[index];

    img.src = data.path;
    filename.textContent = data.filename;
    metadata.textContent = `${data.width} × ${data.height} • ${data.size}`;
}

// Navigation
function navigate(direction) {
    showImage(currentIndex + direction);
}

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

// Keyboard controls (vim-style included)
document.addEventListener('keydown', (e) => {
    const lightbox = document.getElementById('lightbox');

    // If lightbox isn't active, open first image on any key press
    if (!lightbox.classList.contains('active')) {
        openLightbox(0);
        return; // stop processing this key
    }

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
});
// Click outside to close
document.addEventListener('DOMContentLoaded', () => {
    const lightbox = document.getElementById('lightbox');

    if (!lightbox) return;

    lightbox.addEventListener('click', (e) => {
        if (e.target.id === 'lightbox') {
            closeLightbox();
        }
    });
});
