from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import sqlite3
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from db import get_db_connection, init_db
from invoice_service import generate_invoice
from email_service import send_order_confirmation, send_digital_delivery

# Initialize database
init_db()

app = Flask(__name__, static_folder=os.path.dirname(os.path.abspath(__file__)), static_url_path='/')
CORS(app)  # Enable CORS for all routes (since frontend is on same origin or different port in dev)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/downloads/<path:filename>')
def download_file(filename):
    # In a real app, you might want to check if the user has a valid order
    # For now, we serve from the downloads folder
    downloads_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'downloads')
    return send_from_directory(downloads_dir, filename)

@app.route('/api/checkout', methods=['POST'])
def checkout():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Basic Validation
    required_fields = ['customer_name', 'customer_email', 'billing_address', 'items']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    items = data.get('items', [])
    if not items:
        return jsonify({'error': 'Order must contain at least one item'}), 400

    total_amount = sum(item.get('price', 0) * item.get('quantity', 1) for item in items)
    
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Generate an order number (e.g., ORD-YYYYMMDD-ID)
        # First, insert the order to get the ID
        cursor.execute('''
            INSERT INTO orders (
                order_number, customer_name, customer_email, customer_phone,
                billing_address, shipping_address, notes, total_amount, payment_method, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            'TEMP', # Placeholder
            data['customer_name'],
            data['customer_email'],
            data.get('customer_phone', ''),
            data['billing_address'],
            data.get('shipping_address', ''),
            data.get('notes', ''),
            total_amount,
            'Kostenlos' if total_amount == 0 else data.get('payment_method', 'Überweisung, Vorkasse'),
            'Abgeschlossen' if total_amount == 0 else 'Ausstehend'
        ))
        
        order_id = cursor.lastrowid
        
        # Update order number to a proper format
        order_number = f"100{order_id}" # Starting at 1001
        cursor.execute('UPDATE orders SET order_number = ? WHERE id = ?', (order_number, order_id))
        
        # Insert items
        for item in items:
            cursor.execute('''
                INSERT INTO order_items (order_id, item_name, quantity, price)
                VALUES (?, ?, ?, ?)
            ''', (order_id, item['name'], item.get('quantity', 1), item['price']))
            
        conn.commit()
        
        # Fetch the newly created order to generate PDF
        cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
        order_row = cursor.fetchone()
        
        order_dict = dict(order_row)
        order_dict['items'] = items
        
        # Format date for PDF
        order_dict['created_at'] = order_dict['created_at'] # Already set by SQLite default
        
        # Generate Invoice
        pdf_path = generate_invoice(order_dict)
        
        # Send Order Confirmation Email
        send_order_confirmation(order_dict, pdf_path)
        
        return jsonify({
            'success': True,
            'message': 'Order created successfully',
            'order_id': order_id,
            'order_number': order_number
        }), 201
        
    except Exception as e:
        conn.rollback()
        print(f"Error in checkout: {e}")
        return jsonify({'error': 'Failed to process order'}), 500
    finally:
        conn.close()

# --- ADMIN ROUTES ---

@app.route('/api/admin/orders', methods=['GET'])
def get_orders():
    # In a real app, verify admin authentication here
    conn = get_db_connection()
    try:
        # Get query parameters for filtering
        status_filter = request.args.get('status')
        search_query = request.args.get('search')
        
        query = 'SELECT * FROM orders'
        params = []
        conditions = []
        
        if status_filter:
            conditions.append('status = ?')
            params.append(status_filter)
            
        if search_query:
            conditions.append('(customer_name LIKE ? OR order_number LIKE ?)')
            params.append(f'%{search_query}%')
            params.append(f'%{search_query}%')
            
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
            
        query += ' ORDER BY created_at DESC'
        
        orders = conn.execute(query, params).fetchall()
        return jsonify([dict(row) for row in orders])
    finally:
        conn.close()

@app.route('/api/admin/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    conn = get_db_connection()
    try:
        order = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
        if not order:
            return jsonify({'error': 'Order not found'}), 404
            
        items = conn.execute('SELECT * FROM order_items WHERE order_id = ?', (order_id,)).fetchall()
        
        order_dict = dict(order)
        order_dict['items'] = [dict(row) for row in items]
        
        return jsonify(order_dict)
    finally:
        conn.close()

@app.route('/api/admin/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    data = request.json
    new_status = data.get('status')
    
    if not new_status:
        return jsonify({'error': 'Status is required'}), 400
        
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE orders SET status = ? WHERE id = ?', (new_status, order_id))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Order not found'}), 404
            
        conn.commit()
        
        # If status is set to 'Abgeschlossen', check if we need to send digital downloads
        if new_status == 'Abgeschlossen':
            cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
            order_row = cursor.fetchone()
            if order_row:
                order_dict = dict(order_row)
                cursor.execute('SELECT * FROM order_items WHERE order_id = ?', (order_id,))
                items = cursor.fetchall()
                order_dict['items'] = [dict(item) for item in items]
                
                # This only sends if digital items are in the order
                send_digital_delivery(order_dict)
                
        return jsonify({'success': True, 'message': 'Status updated'})
    finally:
        conn.close()

@app.route('/api/admin/orders/<int:order_id>/invoice', methods=['GET'])
def get_order_invoice(order_id):
    conn = get_db_connection()
    try:
        order = conn.execute('SELECT order_number FROM orders WHERE id = ?', (order_id,)).fetchone()
        if not order:
            return jsonify({'error': 'Order not found'}), 404
            
        filename = f"Rechnung_{order['order_number']}.pdf"
        data_dir = os.environ.get('DATA_DIR', os.path.dirname(os.path.abspath(__file__)))
        filepath = os.path.join(data_dir, 'invoices', filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'Invoice PDF not found'}), 404
            
        return send_file(filepath, as_attachment=True)
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
