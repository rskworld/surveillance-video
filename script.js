// Project: Surveillance Video Dataset
// Author: Molla Samser
// Website: https://rskworld.in/
// Contact: help@rskworld.in
// Phone: +91 93305 39277
// Address: Nutanhat, Mongolkote, Purba Burdwan, West Bengal, India, 713147

function loadVideo(videoPath) {
    const video = document.getElementById('surveillanceVideo');
    if (video) {
        // Add loading state
        video.style.opacity = '0.5';
        video.style.transition = 'opacity 0.3s ease';
        
        video.src = videoPath;
        video.load();
        
        video.addEventListener('canplay', function() {
            this.style.opacity = '1';
            this.play();
        }, { once: true });
        
        video.addEventListener('error', function() {
            this.style.opacity = '1';
            console.error('Error loading video:', videoPath);
        });
    }
}

function showTab(tabName) {
    // Hide all tab contents
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => {
        content.classList.remove('active');
    });
    
    // Remove active class from all buttons
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab content with fade animation
    const selectedTab = document.getElementById(tabName);
    if (selectedTab) {
        selectedTab.style.opacity = '0';
        selectedTab.classList.add('active');
        setTimeout(() => {
            selectedTab.style.opacity = '1';
            selectedTab.style.transition = 'opacity 0.3s ease';
        }, 10);
    }
    
    // Add active class to clicked button
    if (event && event.target) {
        event.target.classList.add('active');
    }
}

// Smooth scroll to section
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        const offset = 80; // Account for sticky navbar
        const elementPosition = section.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - offset;
        
        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Initialize video player
    const video = document.getElementById('surveillanceVideo');
    if (video) {
        video.addEventListener('error', function(e) {
            console.log('Video load error:', e);
        });
        
        // Add video controls enhancement
        video.addEventListener('play', function() {
            this.style.boxShadow = '0 0 20px rgba(102, 126, 234, 0.5)';
        });
        
        video.addEventListener('pause', function() {
            this.style.boxShadow = '0 5px 20px rgba(0,0,0,0.5)';
        });
    }
    
    // Enhanced navigation link clicks
    document.querySelectorAll('.nav-links a[href^="#"]').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            scrollToSection(targetId);
        });
    });
    
    // Add intersection observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.6s ease-out forwards';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe sections for animation
    document.querySelectorAll('section').forEach(section => {
        section.style.opacity = '0';
        observer.observe(section);
    });
    
    // Add ripple effect to buttons
    document.querySelectorAll('.btn, .btn-download').forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.6);
                transform: scale(0);
                animation: ripple-animation 0.6s ease-out;
                pointer-events: none;
            `;
            
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Back to top button functionality
    const backToTop = document.getElementById('backToTop');
    if (backToTop) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                backToTop.classList.add('show');
            } else {
                backToTop.classList.remove('show');
            }
        });
        
        backToTop.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // Add typing effect to subtitle (optional enhancement)
    const subtitle = document.querySelector('.subtitle');
    if (subtitle) {
        const text = subtitle.textContent;
        subtitle.textContent = '';
        subtitle.style.opacity = '1';
        let i = 0;
        const typeInterval = setInterval(() => {
            if (i < text.length) {
                subtitle.textContent += text.charAt(i);
                i++;
            } else {
                clearInterval(typeInterval);
            }
        }, 50);
    }
    
    // Add parallax effect to header
    window.addEventListener('scroll', function() {
        const header = document.querySelector('header');
        if (header) {
            const scrolled = window.pageYOffset;
            const rate = scrolled * 0.5;
            header.style.transform = `translateY(${rate}px)`;
        }
    });
});

