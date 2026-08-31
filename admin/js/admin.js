document.addEventListener('DOMContentLoaded', () => {
    fetchOrders();
    
    if (document.getElementById('dashboardMonths')) {
        loadDashboard();
    }

    if (document.getElementById('statusFilter')) {
        document.getElementById('statusFilter').addEventListener('change', fetchOrders);
    }
    if (document.getElementById('paymentFilter')) {
        document.getElementById('paymentFilter').addEventListener('change', fetchOrders);
    }
    if (document.getElementById('searchInput')) {
        document.getElementById('searchInput').addEventListener('input', fetchOrders);
    }
});

async function fetchOrders() {
    const statusEl = document.getElementById('statusFilter');
    const paymentEl = document.getElementById('paymentFilter');
    const searchEl = document.getElementById('searchInput');

    const status = statusEl ? statusEl.value : '';
    const payment = paymentEl ? paymentEl.value : '';
    const search = searchEl ? searchEl.value : '';
    
    let url = '/api/admin/orders';
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    if (payment) params.append('payment_status', payment);
    if (search) params.append('search', search);
    
    if (params.toString()) {
        url += '?' + params.toString();
    }

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Failed to fetch orders');
        let orders = await response.json();
        
        if (window.location.pathname.includes('offene-posten.html')) {
            orders = orders.filter(o => o.status === 'Offen' || o.payment_status === 'Ausstehend' || !o.payment_status);
        }
        
        renderOrders(orders);
    } catch (error) {
        console.error('Error fetching orders:', error);
        const tbody = document.getElementById('ordersBody');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; color:red;">Fehler beim Laden der Bestellungen. Server läuft?</td></tr>';
        }
    }
}

function renderOrders(orders) {
    const tbody = document.getElementById('ordersBody');
    tbody.innerHTML = '';

    if (orders.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;">Keine Bestellungen gefunden.</td></tr>';
        return;
    }

    orders.forEach(order => {
        const tr = document.createElement('tr');
        
        // Format Date
        const date = new Date(order.created_at).toLocaleDateString('de-AT', {
            day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit'
        });

        // Format Currency
        const total = `€ ${order.total_amount.toFixed(2).replace('.', ',')}`;

        const importBadge = (order.notes && order.notes.includes('Import altes System')) 
            ? '<span class="import-badge">Import</span>' 
            : '';

        tr.innerHTML = `
            <td><span class="status-badge status-${order.status}">${order.status}</span></td>
            <td><span class="status-badge status-${order.payment_status || 'Ausstehend'}">${order.payment_status || 'Ausstehend'}</span></td>
            <td>${order.customer_name} ${importBadge}</td>
            <td>${date}</td>
            <td>${order.payment_method}</td>
            <td>${total}</td>
            <td>${order.order_number}</td>
            <td>
                <a href="order.html?id=${order.id}" class="btn btn-sm btn-default">Bearbeiten</a>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function loadDashboard() {
    try {
        const response = await fetch('/api/admin/orders');
        if (!response.ok) throw new Error('Failed to fetch dashboard data');
        const allOrders = await response.json();
        renderDashboard(allOrders);
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        document.getElementById('dashboardMonths').innerHTML = '<div style="color: red; padding: 20px;">Fehler beim Laden der Umsatzstatistik.</div>';
    }
}

function renderDashboard(orders) {
    let totalRevenue = 0;
    let paidRevenue = 0;
    let pendingRevenue = 0;
    let orderCount = orders.length;

    const monthlyData = {};

    orders.forEach(order => {
        if (order.status === 'Storniert') return;

        const amount = order.total_amount || 0;
        totalRevenue += amount;

        if (order.payment_status === 'Bezahlt') {
            paidRevenue += amount;
        } else {
            pendingRevenue += amount;
        }

        const date = new Date(order.created_at);
        if (!isNaN(date.getTime())) {
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const key = `${year}-${month}`;

            if (!monthlyData[key]) {
                monthlyData[key] = {
                    total: 0,
                    paid: 0,
                    count: 0,
                    name: date.toLocaleString('de-AT', { month: 'long', year: 'numeric' })
                };
            }
            monthlyData[key].total += amount;
            if (order.payment_status === 'Bezahlt') {
                monthlyData[key].paid += amount;
            }
            monthlyData[key].count += 1;
        }
    });

    document.getElementById('statTotalRevenue').innerText = `€ ${totalRevenue.toFixed(2).replace('.', ',')}`;
    document.getElementById('statPaidRevenue').innerText = `€ ${paidRevenue.toFixed(2).replace('.', ',')}`;
    document.getElementById('statPendingRevenue').innerText = `€ ${pendingRevenue.toFixed(2).replace('.', ',')}`;
    document.getElementById('statOrderCount').innerText = orderCount;

    const monthsContainer = document.getElementById('dashboardMonths');
    monthsContainer.innerHTML = '';

    const sortedKeys = Object.keys(monthlyData).sort((a, b) => b.localeCompare(a));

    if (sortedKeys.length === 0) {
        monthsContainer.innerHTML = '<div style="text-align: center; color: #777; width: 100%; padding: 20px;">Keine Umsatzdaten vorhanden.</div>';
        return;
    }

    const maxMonthlyRevenue = Math.max(...Object.values(monthlyData).map(m => m.total)) || 1;

    sortedKeys.forEach(key => {
        const data = monthlyData[key];
        const percent = Math.min(100, Math.round((data.total / maxMonthlyRevenue) * 100));

        const monthCard = document.createElement('div');
        monthCard.className = 'month-card';
        monthCard.innerHTML = `
            <div class="month-header">
                <span class="month-name">${data.name}</span>
                <span class="month-orders-badge">${data.count} ${data.count === 1 ? 'Bestellung' : 'Bestellungen'}</span>
            </div>
            <div class="month-totals">
                <div class="month-total-row">
                    <span class="month-total-label">Gesamtumsatz:</span>
                    <span class="month-total-value">€ ${data.total.toFixed(2).replace('.', ',')}</span>
                </div>
                <div class="month-total-row">
                    <span class="month-total-label">Davon bezahlt:</span>
                    <span class="month-total-value paid-value">€ ${data.paid.toFixed(2).replace('.', ',')}</span>
                </div>
            </div>
            <div class="progress-bar-container">
                <div class="progress-bar-fill" style="width: ${percent}%;"></div>
            </div>
        `;
        monthsContainer.appendChild(monthCard);
    });
}

