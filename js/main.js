// js/main.js

document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Navigation Toggle
    const mobileBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if(mobileBtn && navLinks) {
        mobileBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            // Toggle icon between hamburger and close
            if(navLinks.classList.contains('active')){
                mobileBtn.innerHTML = '&#10005;'; // X mark
            } else {
                mobileBtn.innerHTML = '&#9776;'; // Hamburger
            }
        });
    }

    // 2. Sticky Header on Scroll
    const header = document.querySelector('header');
    
    window.addEventListener('scroll', () => {
        if(window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // 3. Highlight current page in navigation
    const currentPath = window.location.pathname.split('/').pop();
    const navItems = document.querySelectorAll('.nav-links a');
    
    navItems.forEach(item => {
        const itemPath = item.getAttribute('href');
        if (itemPath === currentPath || (currentPath === '' && itemPath === 'index.html')) {
            item.classList.add('active');
        }
    });
    // 4. Web3Forms AJAX Form Submission
    const contactForm = document.getElementById('contactForm');
    const formResult = document.getElementById('formResult');
    
    if(contactForm && formResult) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(contactForm);
            const object = Object.fromEntries(formData);
            const json = JSON.stringify(object);
            
            formResult.style.display = 'block';
            formResult.innerHTML = "Nachricht wird gesendet...";
            formResult.style.color = "var(--c-white)";
            
            fetch('/api/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: json
            })
            .then(async (response) => {
                let json = await response.json();
                if (response.status == 200 || response.status == 201) {
                    formResult.innerHTML = json.message || "Vielen Dank! Deine Nachricht wurde erfolgreich gesendet.";
                    formResult.style.background = "linear-gradient(135deg, var(--c-teal), var(--c-violet))";
                    formResult.style.color = "var(--c-white)";
                    formResult.style.padding = "12px 20px";
                    formResult.style.borderRadius = "8px";
                    formResult.style.boxShadow = "0 0 15px rgba(255, 255, 255, 0.4)";
                    formResult.style.border = "1px solid rgba(255, 255, 255, 0.2)";
                    formResult.style.textAlign = "center";
                    formResult.style.display = "block";
                } else {
                    console.log(response);
                    formResult.innerHTML = json.error || json.message || "Etwas ist schief gelaufen.";
                    formResult.style.color = "var(--c-pink)";
                }
            })
            .catch(error => {
                console.log(error);
                formResult.innerHTML = "Fehler beim Senden der Nachricht. Bitte versuche es später noch einmal.";
                formResult.style.color = "var(--c-pink)";
            })
            .then(function() {
                contactForm.reset();
                setTimeout(() => {
                    formResult.style.display = 'none';
                    formResult.style.background = '';
                    formResult.style.color = '';
                    formResult.style.padding = '';
                    formResult.style.borderRadius = '';
                    formResult.style.boxShadow = '';
                    formResult.style.border = '';
                    formResult.style.textAlign = '';
                }, 8000);
            });
        });
    }

    // 5. FAQ Accordion Logic
    document.querySelectorAll('.faq-question').forEach(button => {
        button.addEventListener('click', () => {
            const item = button.closest('.faq-item');
            
            // Optional: Close all others
            document.querySelectorAll('.faq-item').forEach(other => {
                if (other !== item) other.classList.remove('active');
            });
            
            item.classList.toggle('active');
        });
    });

    // 6. Testimonial Slider
    const slidesContainer = document.querySelector('.testimonial-slides');
    if (slidesContainer) {
        const slidesArray = Array.from(slidesContainer.querySelectorAll('.testimonial-slide'));
        // Shuffle the array (Fisher-Yates)
        for (let i = slidesArray.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [slidesArray[i], slidesArray[j]] = [slidesArray[j], slidesArray[i]];
        }
        // Re-append in randomized order
        slidesArray.forEach(slide => {
            slide.classList.remove('active');
            slide.style.display = 'none';
            slide.style.opacity = '0';
            slide.style.transform = 'translateY(20px)';
            slidesContainer.appendChild(slide);
        });
        // Make the first shuffled slide active initially
        if (slidesArray.length > 0) {
            slidesArray[0].classList.add('active');
            slidesArray[0].style.display = 'block';
            slidesArray[0].style.opacity = '1';
            slidesArray[0].style.transform = 'translateY(0)';
        }
    }

    const slides = document.querySelectorAll('.testimonial-slide');
    const dots = document.querySelectorAll('.slider-dot');
    const prevArrow = document.querySelector('.prev-arrow');
    const nextArrow = document.querySelector('.next-arrow');
    let currentSlide = 0;
    let slideInterval;

    if (slides.length > 0) {
        function showSlide(index) {
            slides.forEach((slide, i) => {
                if (i === index) {
                    slide.style.display = 'block';
                    // Force a reflow for transition
                    slide.offsetHeight; 
                    slide.style.opacity = '1';
                    slide.style.transform = 'translateY(0)';
                } else {
                    slide.style.opacity = '0';
                    slide.style.transform = 'translateY(20px)';
                    // Match the CSS transition duration before hiding
                    setTimeout(() => {
                        if (currentSlide !== i) {
                            slide.style.display = 'none';
                        }
                    }, 600);
                }
            });

            dots.forEach((dot, i) => {
                if (i === index) {
                    dot.classList.add('active');
                    dot.style.background = 'var(--c-gold)';
                } else {
                    dot.classList.remove('active');
                    dot.style.background = 'rgba(255, 255, 255, 0.3)';
                }
            });
            currentSlide = index;
        }

        function nextSlide() {
            let next = (currentSlide + 1) % slides.length;
            showSlide(next);
        }

        function prevSlide() {
            let prev = (currentSlide - 1 + slides.length) % slides.length;
            showSlide(prev);
        }

        function startAutoPlay() {
            stopAutoPlay();
            slideInterval = setInterval(nextSlide, 7000); // Rotate every 7 seconds
        }

        function stopAutoPlay() {
            if (slideInterval) {
                clearInterval(slideInterval);
            }
        }

        if (prevArrow && nextArrow) {
            prevArrow.addEventListener('click', () => {
                prevSlide();
                startAutoPlay(); // Reset timer
            });
            nextArrow.addEventListener('click', () => {
                nextSlide();
                startAutoPlay(); // Reset timer
            });
        }

        dots.forEach((dot, i) => {
            dot.addEventListener('click', () => {
                showSlide(i);
                startAutoPlay(); // Reset timer
            });
        });

        // Pause on Hover
        const container = document.querySelector('.testimonial-slider-container');
        if (container) {
            container.addEventListener('mouseenter', stopAutoPlay);
            container.addEventListener('mouseleave', startAutoPlay);
        }

        // Initialize
        showSlide(0);
        startAutoPlay();
    }
});
