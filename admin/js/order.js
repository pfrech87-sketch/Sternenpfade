document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const orderId = urlParams.get('id');

    if (!orderId) {
        alert('Keine Bestell-ID angegeben');
        window.location.href = 'index.html';
        return;
    }

    fetchOrderDetails(orderId);

    document.getElementById('saveStatusBtn').addEventListener('click', () => saveOrderStatus(orderId));
    document.getElementById('printInvoiceBtn').addEventListener('click', () => printInvoice(orderId));
});

async function fetchOrderDetails(orderId) {
    try {
        const response = await fetch(`/api/admin/orders/${orderId}`);
        if (!response.ok) throw new Error('Failed to fetch order details');
        const order = await response.json();
        renderOrderDetails(order);
    } catch (error) {
        console.error('Error fetching order:', error);
        alert('Fehler beim Laden der Bestelldetails.');
    }
}

function renderOrderDetails(order) {
    document.getElementById('orderNumberDisplay').textContent = order.order_number;
    document.getElementById('customerEmail').textContent = order.customer_email;
    document.getElementById('billingAddress').innerHTML = `${order.customer_name}<br>${order.billing_address.replace(/\n/g, '<br>')}<br>${order.customer_phone || ''}`;
    
    document.getElementById('orderStatusSelect').value = order.status || 'Offen';
    document.getElementById('paymentStatusSelect').value = order.payment_status || 'Ausstehend';
    document.getElementById('orderNotes').value = order.notes || '';
    
    // Items
    const itemsContainer = document.getElementById('orderItemsList');
    itemsContainer.innerHTML = '';
    order.items.forEach(item => {
        const itemRow = document.createElement('div');
        itemRow.className = 'item-row';
        
        const price = `€ ${(item.price * item.quantity).toFixed(2).replace('.', ',')}`;
        
        itemRow.innerHTML = `
            <div>
                ${item.quantity} x <span class="text-blue" style="cursor:pointer; text-decoration:underline;">${item.item_name}</span>
            </div>
            <div class="bold">${price}</div>
        `;
        itemsContainer.appendChild(itemRow);
        
        // Add a line separator
        const hr = document.createElement('hr');
        hr.style.margin = "10px 0";
        hr.style.borderTop = "1px solid #eee";
        itemsContainer.appendChild(hr);
    });

    // Total
    document.getElementById('totalAmount').textContent = `€ ${order.total_amount.toFixed(2).replace('.', ',')}`;
    

}

async function saveOrderStatus(orderId) {
    const newStatus = document.getElementById('orderStatusSelect').value;
    const newPaymentStatus = document.getElementById('paymentStatusSelect').value;
    
    try {
        const response = await fetch(`/api/admin/orders/${orderId}/status`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                status: newStatus,
                payment_status: newPaymentStatus
            })
        });
        
        if (!response.ok) throw new Error('Failed to update status');
        
        alert('Status erfolgreich gespeichert.');
    } catch (error) {
        console.error('Error updating status:', error);
        alert('Fehler beim Speichern des Status.');
    }
}

function printInvoice(orderId) {
    window.open(`/api/admin/orders/${orderId}/invoice`, '_blank');
}
