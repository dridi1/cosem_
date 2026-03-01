// Navbar behavior
document.addEventListener('DOMContentLoaded', () => {
    const navbar = document.getElementById('marketing-navbar');
    const navToggle = document.getElementById('marketing-nav-toggle');
    const navMenu = document.getElementById('marketing-nav-menu');

    const updateNavbarScrollState = () => {
        if (!navbar) {
            return;
        }

        if (window.scrollY > 50) {
            navbar.classList.remove('bg-grain-soft/80');
            navbar.classList.add('bg-grain-soft/95', 'shadow-grain');
        } else {
            navbar.classList.add('bg-grain-soft/80');
            navbar.classList.remove('bg-grain-soft/95', 'shadow-grain');
        }
    };

    const closeMobileMenu = () => {
        if (!navMenu || !navToggle) {
            return;
        }

        navMenu.classList.add('hidden');
        navToggle.setAttribute('aria-expanded', 'false');
    };

    updateNavbarScrollState();
    window.addEventListener('scroll', updateNavbarScrollState);

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            const willOpen = navMenu.classList.contains('hidden');
            navMenu.classList.toggle('hidden');
            navToggle.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
        });

        navMenu.querySelectorAll('a').forEach((link) => {
            link.addEventListener('click', () => {
                if (window.innerWidth < 1024) {
                    closeMobileMenu();
                }
            });
        });

        window.addEventListener('resize', () => {
            if (window.innerWidth >= 1024) {
                navMenu.classList.remove('hidden');
                navToggle.setAttribute('aria-expanded', 'false');
            } else {
                closeMobileMenu();
            }
        });

        if (window.innerWidth >= 1024) {
            navMenu.classList.remove('hidden');
        } else {
            closeMobileMenu();
        }
    }
});

// Initialize AOS
document.addEventListener('DOMContentLoaded', function() {
    if (typeof AOS !== 'undefined') {
        AOS.init();
    }
});

// IntersectionObserver for section animations
document.addEventListener('DOMContentLoaded', () => {
    const sections = document.querySelectorAll('.section');
    if (!sections.length) {
        return;
    }

    const options = {
        threshold: 0.5
    };

    let observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('in-view');
            } else {
                entry.target.classList.remove('in-view');
            }
        });
    }, options);

    sections.forEach(section => {
        observer.observe(section);
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const heroSlides = document.querySelectorAll('.hero-slide');
    if (!heroSlides.length) {
        return;
    }

    let currentIndex = 0;

    const setActiveSlide = (nextIndex) => {
        heroSlides.forEach((slide, index) => {
            slide.classList.toggle('is-active', index === nextIndex);
        });
    };

    setActiveSlide(currentIndex);

    setInterval(() => {
        currentIndex = (currentIndex + 1) % heroSlides.length;
        setActiveSlide(currentIndex);
    }, 5000);
});

document.addEventListener('DOMContentLoaded', () => {
    const counters = document.querySelectorAll('[data-counter-value]');
    if (!counters.length) {
        return;
    }

    const formatNumber = (value) => new Intl.NumberFormat('en-US').format(value);

    const animateCounter = (element) => {
        if (element.dataset.counterAnimated === 'true') {
            return;
        }

        const target = Number.parseInt(element.dataset.counterValue || '0', 10);
        if (Number.isNaN(target)) {
            return;
        }

        element.dataset.counterAnimated = 'true';

        const duration = 1400;
        const startTime = performance.now();

        const updateValue = (currentTime) => {
            const progress = Math.min((currentTime - startTime) / duration, 1);
            const easedProgress = 1 - Math.pow(1 - progress, 3);
            const currentValue = Math.round(target * easedProgress);

            element.textContent = formatNumber(currentValue);

            if (progress < 1) {
                window.requestAnimationFrame(updateValue);
            } else {
                element.textContent = formatNumber(target);
            }
        };

        window.requestAnimationFrame(updateValue);
    };

    const observer = new IntersectionObserver((entries, currentObserver) => {
        entries.forEach((entry) => {
            if (!entry.isIntersecting) {
                return;
            }

            animateCounter(entry.target);
            currentObserver.unobserve(entry.target);
        });
    }, {
        threshold: 0.4
    });

    counters.forEach((counter) => {
        observer.observe(counter);
    });
});
