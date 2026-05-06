document.addEventListener('DOMContentLoaded', () => {
    fetchOrders();

    document.getElementById('statusFilter').addEventListener('change', fetchOrders);
    document.getElementById('searchInput').addEventListener('input', fetchOrders);
});

async function fetchOrders() {
    const status = document.getElementById('statusFilter').value;
    const search = document.getElementById('searchInput').value;
    
    let url = '/api/admin/orders';
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    if (search) params.append('search', search);
    
    if (params.toString()) {
        url += '?' + params.toString();
    }

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Failed to fetch orders');
        const orders = await response.json();
        renderOrders(orders);
    } catch (error) {
        console.error('Error fetching orders:', error);
        document.getElementById('ordersBody').innerHTML = '<tr><td colspan="7" style="text-align:center; color:red;">Fehler beim Laden der Bestellungen. Server läuft?</td></tr>';
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

        tr.innerHTML = `
            <td><span class="status-badge status-${order.status}">${order.status}</span></td>
            <td>${order.customer_name}</td>
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
