// Custom JavaScript for Sphinx Material theme to match MkDocs Material functionality

// Smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling to all anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                e.preventDefault();
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // Add active state to navigation links
    const currentPath = window.location.pathname;
    document.querySelectorAll('.md-nav__link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('md-nav__link--active');
        }
    });

    // Mobile menu toggle functionality
    const menuToggle = document.querySelector('[data-md-toggle="drawer"]');
    if (menuToggle) {
        menuToggle.addEventListener('change', function() {
            document.body.classList.toggle('md-drawer--active', this.checked);
        });
    }

    // Search functionality enhancement
    const searchInput = document.querySelector('.md-search__input');
    if (searchInput) {
        searchInput.addEventListener('focus', function() {
            this.parentElement.classList.add('md-search--active');
        });
        
        searchInput.addEventListener('blur', function() {
            this.parentElement.classList.remove('md-search--active');
        });
    }

    // Table of contents highlighting
    const tocLinks = document.querySelectorAll('.md-nav__link');
    const sections = document.querySelectorAll('section[id], h1[id], h2[id], h3[id], h4[id], h5[id], h6[id]');
    
    function highlightToc() {
        const scrollPosition = window.scrollY + 100;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                tocLinks.forEach(link => {
                    link.classList.remove('md-nav__link--active');
                    if (link.getAttribute('href') === '#' + sectionId) {
                        link.classList.add('md-nav__link--active');
                    }
                });
            }
        });
    }
    
    window.addEventListener('scroll', highlightToc);
    highlightToc(); // Initial call

    // Back to top button functionality
    const backToTopButton = document.querySelector('[data-md-component="top"]');
    if (backToTopButton) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                backToTopButton.hidden = false;
            } else {
                backToTopButton.hidden = true;
            }
        });
        
        backToTopButton.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // External link handling
    document.querySelectorAll('a[href^="http"]').forEach(link => {
        if (!link.getAttribute('href').includes(window.location.hostname)) {
            link.setAttribute('target', '_blank');
            link.setAttribute('rel', 'noopener noreferrer');
            link.setAttribute('aria-label', 'Open in new tab');
        }
    });

    // Code block copy button enhancement
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach(block => {
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button';
        copyButton.textContent = 'Copy';
        copyButton.style.cssText = `
            position: absolute;
            top: 0.5rem;
            right: 0.5rem;
            background: #007db8;
            color: white;
            border: none;
            padding: 0.25rem 0.5rem;
            border-radius: 0.25rem;
            cursor: pointer;
            font-size: 0.75rem;
            z-index: 10;
        `;
        
        copyButton.addEventListener('click', function() {
            navigator.clipboard.writeText(block.textContent).then(() => {
                copyButton.textContent = 'Copied!';
                setTimeout(() => {
                    copyButton.textContent = 'Copy';
                }, 2000);
            });
        });
        
        block.parentElement.style.position = 'relative';
        block.parentElement.appendChild(copyButton);
    });

    // Grid card hover effects
    const gridCards = document.querySelectorAll('.grid-card');
    gridCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Loading state for images
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('load', function() {
            this.classList.add('loaded');
        });
        
        if (img.complete) {
            img.classList.add('loaded');
        }
    });
});