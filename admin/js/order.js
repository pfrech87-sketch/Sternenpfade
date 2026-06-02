let currentOrder = null;

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

    // Refund Modal Event Listeners
    document.getElementById('refundBtn').addEventListener('click', () => openRefundModal());
    document.getElementById('closeRefundModalBtn').addEventListener('click', closeRefundModal);
    document.getElementById('cancelRefundBtn').addEventListener('click', closeRefundModal);

    const radioButtons = document.querySelectorAll('input[name="refundType"]');
    radioButtons.forEach(radio => {
        radio.addEventListener('change', handleRefundTypeChange);
    });

    document.getElementById('customRefundAmount').addEventListener('input', updateRefundTotal);
    document.getElementById('customRefundName').addEventListener('input', updateRefundTotal);
    document.getElementById('submitRefundBtn').addEventListener('click', () => submitRefund(orderId));
});

async function fetchOrderDetails(orderId) {
    try {
        const response = await fetch(`/api/admin/orders/${orderId}`);
        if (!response.ok) throw new Error('Failed to fetch order details');
        const order = await response.json();
        currentOrder = order;
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

    // Check if imported from old system
    const printBtn = document.getElementById('printInvoiceBtn');
    if (printBtn) {
        if (order.notes && order.notes.includes('Import altes System')) {
            printBtn.disabled = true;
            printBtn.style.opacity = '0.5';
            printBtn.style.cursor = 'not-allowed';
            printBtn.textContent = '📄 Keine Rechnung (Altes System)';
        } else {
            printBtn.disabled = false;
            printBtn.style.opacity = '1';
            printBtn.style.cursor = 'pointer';
            printBtn.textContent = '📄 Rechnung downloaden ↓';
        }
    }
    

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

/* --- Refund Modal Control Logic --- */

function openRefundModal() {
    if (!currentOrder) return;
    
    // Reset modal fields
    document.getElementById('refundOrderNumberDisplay').textContent = currentOrder.order_number;
    document.querySelector('input[name="refundType"][value="full"]').checked = true;
    document.getElementById('sendRefundEmail').checked = true;
    document.getElementById('customRefundName').value = '';
    document.getElementById('customRefundAmount').value = '0.00';
    
    // Show full refund section, hide others
    document.getElementById('refundItemsSection').style.display = 'none';
    document.getElementById('refundCustomSection').style.display = 'none';
    
    // Populate items list for itemized refund
    const tbody = document.getElementById('refundItemsBody');
    tbody.innerHTML = '';
    
    currentOrder.items.forEach((item, index) => {
        const tr = document.createElement('tr');
        const itemTotal = item.price * item.quantity;
        
        tr.innerHTML = `
            <td style="padding: 8px; text-align: center; border-bottom: 1px solid #eee;">
                <input type="checkbox" class="refund-item-checkbox" data-index="${index}" style="width: 16px; height: 16px; cursor: pointer;">
            </td>
            <td style="padding: 8px; border-bottom: 1px solid #eee;">${item.item_name}</td>
            <td style="padding: 8px; text-align: right; border-bottom: 1px solid #eee;">€ ${item.price.toFixed(2).replace('.', ',')}</td>
            <td style="padding: 8px; text-align: center; border-bottom: 1px solid #eee;">
                <input type="number" class="refund-item-qty" data-index="${index}" min="1" max="${item.quantity}" value="${item.quantity}" style="width: 60px; padding: 4px; border: 1px solid #ccc; border-radius: 4px; text-align: center;" disabled>
            </td>
            <td style="padding: 8px; text-align: right; font-weight: 600; border-bottom: 1px solid #eee;" class="refund-item-row-total">€ ${itemTotal.toFixed(2).replace('.', ',')}</td>
        `;
        tbody.appendChild(tr);
        
        const checkbox = tr.querySelector('.refund-item-checkbox');
        const qtyInput = tr.querySelector('.refund-item-qty');
        
        checkbox.addEventListener('change', () => {
            qtyInput.disabled = !checkbox.checked;
            updateRefundTotal();
        });
        
        qtyInput.addEventListener('input', () => {
            let val = parseInt(qtyInput.value);
            if (isNaN(val) || val < 1) val = 1;
            if (val > item.quantity) val = item.quantity;
            qtyInput.value = val;
            
            const rowTotal = item.price * val;
            tr.querySelector('.refund-item-row-total').textContent = `€ ${rowTotal.toFixed(2).replace('.', ',')}`;
            updateRefundTotal();
        });
    });

    document.getElementById('refundModal').style.display = 'flex';
    updateRefundTotal();
}

function closeRefundModal() {
    document.getElementById('refundModal').style.display = 'none';
}

function handleRefundTypeChange() {
    const refundType = document.querySelector('input[name="refundType"]:checked').value;
    
    if (refundType === 'full') {
        document.getElementById('refundItemsSection').style.display = 'none';
        document.getElementById('refundCustomSection').style.display = 'none';
    } else if (refundType === 'items') {
        document.getElementById('refundItemsSection').style.display = 'block';
        document.getElementById('refundCustomSection').style.display = 'none';
    } else if (refundType === 'custom') {
        document.getElementById('refundItemsSection').style.display = 'none';
        document.getElementById('refundCustomSection').style.display = 'block';
    }
    updateRefundTotal();
}

function updateRefundTotal() {
    if (!currentOrder) return;
    
    const refundType = document.querySelector('input[name="refundType"]:checked').value;
    let total = 0;
    
    if (refundType === 'full') {
        total = currentOrder.total_amount;
    } else if (refundType === 'items') {
        const checkboxes = document.querySelectorAll('.refund-item-checkbox');
        checkboxes.forEach(checkbox => {
            if (checkbox.checked) {
                const index = checkbox.getAttribute('data-index');
                const item = currentOrder.items[index];
                const qtyInput = document.querySelector(`.refund-item-qty[data-index="${index}"]`);
                const qty = parseInt(qtyInput.value) || 0;
                total += item.price * qty;
            }
        });
    } else if (refundType === 'custom') {
        const amountInput = document.getElementById('customRefundAmount');
        total = parseFloat(amountInput.value) || 0;
    }
    
    document.getElementById('refundTotalDisplay').textContent = `€ -${total.toFixed(2).replace('.', ',')}`;
}

async function submitRefund(orderId) {
    if (!currentOrder) return;
    
    const refundType = document.querySelector('input[name="refundType"]:checked').value;
    const sendEmail = document.getElementById('sendRefundEmail').checked;
    
    const payload = {
        refund_type: refundType,
        send_email: sendEmail
    };
    
    if (refundType === 'items') {
        const items = [];
        const checkboxes = document.querySelectorAll('.refund-item-checkbox');
        let selectedCount = 0;
        
        checkboxes.forEach(checkbox => {
            if (checkbox.checked) {
                selectedCount++;
                const index = checkbox.getAttribute('data-index');
                const item = currentOrder.items[index];
                const qtyInput = document.querySelector(`.refund-item-qty[data-index="${index}"]`);
                const qty = parseInt(qtyInput.value) || 0;
                items.push({
                    name: item.item_name,
                    quantity: qty
                });
            }
        });
        
        if (selectedCount === 0) {
            alert('Bitte wähle mindestens ein Produkt aus, das storniert werden soll.');
            return;
        }
        payload.items = items;
    } else if (refundType === 'custom') {
        const customName = document.getElementById('customRefundName').value.trim();
        const customAmount = parseFloat(document.getElementById('customRefundAmount').value) || 0;
        
        if (customAmount <= 0) {
            alert('Bitte gib einen gültigen Erstattungsbetrag größer als 0 € ein.');
            return;
        }
        
        payload.custom_name = customName;
        payload.custom_price = customAmount;
    }
    
    const submitBtn = document.getElementById('submitRefundBtn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Buchen...';
    
    try {
        const response = await fetch(`/api/admin/orders/${orderId}/refund`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            let msg = `Gutschrift Nr. ${result.order_number} wurde erfolgreich gebucht!`;
            if (sendEmail) {
                msg += result.email_sent ? '\nE-Mail wurde erfolgreich versendet.' : '\nHinweis: E-Mail konnte nicht gesendet werden (SMTP-Fehler).';
            }
            alert(msg);
            closeRefundModal();
            window.location.href = 'index.html';
        } else {
            throw new Error(result.error || 'Fehler beim Buchen der Gutschrift.');
        }
    } catch (error) {
        alert('Fehler: ' + error.message);
        submitBtn.disabled = false;
        submitBtn.textContent = 'Gutschrift buchen';
    }
}
