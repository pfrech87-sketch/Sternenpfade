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
            
            fetch('https://api.web3forms.com/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: json
            })
            .then(async (response) => {
                let json = await response.json();
                if (response.status == 200) {
                    formResult.innerHTML = "Vielen Dank! Deine Nachricht wurde erfolgreich gesendet.";
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
                    formResult.innerHTML = json.message || "Etwas ist schief gelaufen.";
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
});
