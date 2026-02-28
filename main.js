// STERNENPFADE - PREMIUM BOOKING & ORDER MANAGEMENT SYSTEM

document.addEventListener('DOMContentLoaded', () => {
    console.log('Sternenpfade Relaunch Initialized');

    // --- Mobile Navigation ---
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('nav-links');
    const navOverlay = document.getElementById('nav-overlay');

    const openNav = () => {
        hamburger?.classList.add('active');
        navLinks?.classList.add('mobile-open');
        navOverlay?.classList.add('active');
        document.body.style.overflow = 'hidden';
    };

    const closeNav = () => {
        hamburger?.classList.remove('active');
        navLinks?.classList.remove('mobile-open');
        navOverlay?.classList.remove('active');
        document.body.style.overflow = '';
    };

    hamburger?.addEventListener('click', () => {
        navLinks?.classList.contains('mobile-open') ? closeNav() : openNav();
    });

    navOverlay?.addEventListener('click', closeNav);

    // Close menu when a link is clicked
    navLinks?.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', closeNav);
    });

    // --- Order Logic ---
    const bookingForm = document.getElementById('premium-booking-form');
    const formContent = document.getElementById('form-content');
    const successMessage = document.getElementById('success-message');
    const ordersList = document.getElementById('orders-list');
    const adminDashboard = document.getElementById('admin-dashboard');

    // 1. CTA Connectivity: Scroll to Form and Auto-Select Service
    document.querySelectorAll('.booking-cta').forEach(button => {
        button.addEventListener('click', () => {
            const service = button.getAttribute('data-service');
            const serviceSelect = document.getElementById('service');
            const formSection = document.querySelector('.booking-form-section');

            if (serviceSelect) serviceSelect.value = service;
            formSection.scrollIntoView({ behavior: 'smooth' });
        });
    });

    // 2. Order Submission & Storage
    if (bookingForm) {
        bookingForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const photoFile = document.getElementById('pet-photo').files[0];
            const reader = new FileReader();

            const submitOrder = (photoData = null) => {
                const orderData = {
                    id: 'SP-' + Date.now(),
                    date: new Date().toLocaleString('de-DE'),
                    name: document.getElementById('name').value,
                    email: document.getElementById('email').value,
                    phone: document.getElementById('phone').value,
                    service: document.getElementById('service').options[document.getElementById('service').selectedIndex].text,
                    animal: document.getElementById('animal').value || 'Unbekannt',
                    message: document.getElementById('message').value,
                    photo: photoData,
                    status: 'Neu'
                };

                const orders = JSON.parse(localStorage.getItem('sternenpfade_orders') || '[]');
                orders.unshift(orderData);
                localStorage.setItem('sternenpfade_orders', JSON.stringify(orders));

                formContent.classList.add('hidden');
                successMessage.classList.remove('hidden');
                renderOrders();
            };

            if (photoFile) {
                reader.onloadend = () => submitOrder(reader.result);
                reader.readAsDataURL(photoFile);
            } else {
                submitOrder();
            }
        });
    }

    // 3. Admin Dashboard Logic
    const renderOrders = () => {
        if (!ordersList) return;
        const orders = JSON.parse(localStorage.getItem('sternenpfade_orders') || '[]');

        if (orders.length === 0) {
            ordersList.innerHTML = '<p style="color: var(--text-muted); text-align: center;">Bisher keine Anfragen erhalten.</p>';
            return;
        }

        ordersList.innerHTML = orders.map(order => `
            <div class="card" style="padding: 2rem; border-left: 4px solid var(--accent-gold); margin-bottom: 2rem; display: grid; grid-template-columns: 150px 1fr; gap: 2rem; align-items: start;">
                <div style="text-align: center;">
                    ${order.photo ? `<img src="${order.photo}" style="width: 150px; height: 150px; object-fit: cover; border-radius: 15px; border: 1px solid var(--glass-border);">` : `<div style="width: 150px; height: 150px; background: rgba(255,255,255,0.05); border-radius: 15px; display: flex; align-items: center; justify-content: center; color: var(--text-muted); font-size: 0.7rem;">Kein Bild</div>`}
                    <p style="font-size: 0.7rem; color: var(--accent-gold); margin-top: 1rem; font-weight: bold;">${order.status}</p>
                </div>
                <div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                        <span style="font-size: 0.8rem; color: var(--accent-gold); font-weight: bold;">ID: ${order.id}</span>
                        <span style="font-size: 0.8rem; color: var(--text-muted);">${order.date}</span>
                    </div>
                    <h4 style="margin-bottom: 0.5rem;">${order.service} für <strong>${order.animal}</strong></h4>
                    <p style="font-size: 0.9rem; margin-bottom: 0.2rem;">Absender: <strong>${order.name}</strong></p>
                    <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 1rem;">
                        Email: ${order.email} | Tel: ${order.phone}
                    </p>
                    <div style="background: rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 15px; font-size: 0.85rem; font-style: italic; color: var(--text-muted); line-height: 1.5;">
                        "${order.message}"
                    </div>
                    <div style="margin-top: 1.5rem; display: flex; gap: 1rem;">
                        <button class="btn btn-secondary" style="padding: 0.5rem 1rem; font-size: 0.7rem;" onclick="deleteOrder('${order.id}')">Löschen</button>
                        <button class="btn btn-primary" style="padding: 0.5rem 1rem; font-size: 0.7rem;" onclick="window.location.href='mailto:${order.email}?subject=Ihre Buchung bei Sternenpfade'">Email senden</button>
                        <button class="btn btn-secondary" style="padding: 0.5rem 1rem; font-size: 0.7rem; background: #25d366; color: white; border: none;" onclick="window.location.href='https://wa.me/${order.phone.replace(/[^0-9]/g, '')}'">WhatsApp öffnen</button>
                    </div>
                </div>
            </div>
        `).join('');
    };

    // Global toggle for Admin Dashboard
    window.toggleAdmin = () => {
        adminDashboard.classList.toggle('hidden');
        if (!adminDashboard.classList.contains('hidden')) {
            adminDashboard.scrollIntoView({ behavior: 'smooth' });
            renderOrders();
        }
    };

    // Global delete function
    window.deleteOrder = (id) => {
        if (confirm('Bestellung wirklich löschen?')) {
            let orders = JSON.parse(localStorage.getItem('sternenpfade_orders') || '[]');
            orders = orders.filter(o => o.id !== id);
            localStorage.setItem('sternenpfade_orders', JSON.stringify(orders));
            renderOrders();
        }
    };

    // Global export function
    window.exportOrders = () => {
        const orders = localStorage.getItem('sternenpfade_orders') || '[]';
        const blob = new Blob([orders], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `sternenpfade_bestellungen_${new Date().toISOString().split('T')[0]}.json`;
        a.click();
    };

    // --- SCROLL EFFECTS ---
    const observerOptions = { threshold: 0.1 };
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    document.querySelectorAll('.card, section h2, .section-title').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 1s cubic-bezier(0.165, 0.84, 0.44, 1)';
        observer.observe(el);
    });

    // Initial render for Admin if it was left open
    renderOrders();
});

