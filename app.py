from flask import Flask, request, jsonify, send_file, send_from_directory, redirect
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

# Auto-compile case studies on startup
try:
    print("[SYSTEM-CHECK] Starte Kompilierung der Fallbeispiele...")
    import build_fallbeispiele
    build_fallbeispiele.main()
    print("[SYSTEM-CHECK] Fallbeispiele erfolgreich kompiliert!")
except Exception as e:
    print(f"[SYSTEM-CHECK] Warnung bei der Kompilierung der Fallbeispiele: {e}")

app = Flask(__name__, 
            static_folder=os.path.dirname(os.path.abspath(__file__)), 
            static_url_path='/')
CORS(app)

# --- SYSTEM-CHECK BEIM START ---
email_pw = os.environ.get('EMAIL_PASSWORD', '')
if not email_pw:
    print("[SYSTEM-CHECK] FEHLER: EMAIL_PASSWORD wurde NICHT gefunden!")
else:
    print(f"[SYSTEM-CHECK] OK: EMAIL_PASSWORD gefunden (Länge: {len(email_pw)} Zeichen)")
# ------------------------------

# --- ADMIN BASIC AUTHENTICATION ---
from functools import wraps
from flask import Response

def check_auth(username, password):
    expected_username = os.environ.get('ADMIN_USERNAME', 'info@sternenpfade.at')
    allowed_usernames = [expected_username, 'info@sternenfpade.at', 'info@sternenpfade.at', 'admin']
    expected_password = os.environ.get('ADMIN_PASSWORD', 'patrick')
    return username in allowed_usernames and password == expected_password

def authenticate():
    return Response(
        'Zugriff verweigert. Bitte gib den korrekten Benutzernamen und das Passwort ein.', 401,
        {'WWW-Authenticate': 'Basic realm="Sternenpfade Admin Login"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory(os.path.join(app.static_folder, 'assets'), filename)

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(app.static_folder, 'css'), filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(os.path.join(app.static_folder, 'js'), filename)

@app.route('/admin')
@app.route('/admin/')
@requires_auth
def serve_admin_index():
    admin_dir = os.path.join(app.static_folder, 'admin')
    return send_from_directory(admin_dir, 'index.html')

@app.route('/admin/<path:filename>')
@requires_auth
def serve_admin_pages(filename):
    admin_dir = os.path.join(app.static_folder, 'admin')
    return send_from_directory(admin_dir, filename)

# Disable caching for development
@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response

# --- CLEAN SEO-URL ROUTING ---

@app.route('/dienstleistungen/tierkommunikation')
def tierkommunikation_page():
    return app.send_static_file('tierkommunikation-detail.html')

@app.route('/dienstleistungen/jenseits-der-regenbogenbruecke')
def jenseits_regenbogenbruecke_page():
    return app.send_static_file('jenseitskontakt-tiere-detail.html')

@app.route('/dienstleistungen/schamanische-begleitung-firmen-raeume-gruppen')
def schamanische_begleitung_firmen_page():
    return app.send_static_file('schamanische-begleitung-firmen.html')

@app.route('/schamanische-begleitung-firmen')
def redirect_schamanische_begleitung_firmen():
    return redirect('/dienstleistungen/schamanische-begleitung-firmen-raeume-gruppen', code=301)

@app.route('/buchung')
def buchung_page():
    return app.send_static_file('booking.html')

@app.route('/tierkommunikation-hund')
def tierkommunikation_hund_page():
    return app.send_static_file('tierkommunikation-hund.html')

@app.route('/tierkommunikation-katze')
def tierkommunikation_katze_page():
    return app.send_static_file('tierkommunikation-katze.html')

@app.route('/tierkommunikation-pferd')
def tierkommunikation_pferd_page():
    return app.send_static_file('tierkommunikation-pferd.html')

@app.route('/kontakt-mit-verstorbenem-tier')
def kontakt_verstorbenes_tier_page():
    return app.send_static_file('kontakt-mit-verstorbenem-tier.html')

@app.route('/jenseitskontakt-hund')
def jenseitskontakt_hund_page():
    return app.send_static_file('jenseitskontakt-hund.html')

@app.route('/jenseitskontakt-katze')
def jenseitskontakt_katze_page():
    return app.send_static_file('jenseitskontakt-katze.html')

@app.route('/fallbeispiele')
def fallbeispiele_page():
    return app.send_static_file('fallbeispiele.html')

@app.route('/tiere')
def tiere_page():
    return app.send_static_file('tiere.html')

@app.route('/menschen')
def menschen_page():
    return app.send_static_file('menschen.html')

@app.route('/jenseits')
def jenseits_page():
    return app.send_static_file('jenseits.html')

@app.route('/about')
def about_page():
    return app.send_static_file('about.html')

@app.route('/kontakt')
def kontakt_page():
    return app.send_static_file('kontakt.html')

@app.route('/impressum')
def impressum_page():
    return app.send_static_file('impressum.html')

@app.route('/agb')
def agb_page():
    return app.send_static_file('agb.html')

@app.route('/kreise-kurse')
def kreise_kurse_page():
    return app.send_static_file('kreise-kurse.html')

@app.route('/datenschutz')
def datenschutz_page():
    return app.send_static_file('datenschutz.html')

@app.route('/lp/termin')
def lp_termin_page():
    return app.send_static_file('lp-termin.html')

@app.route('/fallbeispiele/<slug>')
def fallbeispiele_detail_page(slug):
    # Sanitize the slug to prevent directory traversal
    safe_slug = "".join([c for c in slug if c.isalnum() or c in '-_'])
    filename = f"{safe_slug}.html"
    filepath = os.path.join(app.static_folder, 'fallbeispiele', filename)
    if os.path.exists(filepath):
        return send_from_directory(os.path.join(app.static_folder, 'fallbeispiele'), filename)
    return "Seite nicht gefunden", 404

@app.route('/sitemap.xml')
def sitemap_xml():
    return app.send_static_file('sitemap.xml')

@app.route('/robots.txt')
def robots_txt():
    return app.send_static_file('robots.txt')

# --- 301 Permanent Redirects for Legacy URLs ---

@app.route('/index.html')
def redirect_index():
    return redirect('/', code=301)

@app.route('/tiere.html')
def redirect_tiere():
    return redirect('/tiere', code=301)

@app.route('/menschen.html')
def redirect_menschen():
    return redirect('/menschen', code=301)

@app.route('/jenseits.html')
def redirect_jenseits():
    return redirect('/jenseits', code=301)

@app.route('/about.html')
def redirect_about():
    return redirect('/about', code=301)

@app.route('/kontakt.html')
def redirect_kontakt():
    return redirect('/kontakt', code=301)

@app.route('/impressum.html')
def redirect_impressum():
    return redirect('/impressum', code=301)

@app.route('/agb.html')
def redirect_agb():
    return redirect('/agb', code=301)

@app.route('/kreise-kurse.html')
def redirect_kreise_kurse():
    return redirect('/kreise-kurse', code=301)

@app.route('/datenschutz.html')
def redirect_datenschutz_html():
    return redirect('/datenschutz', code=301)

@app.route('/lp-termin.html')
def redirect_lp_termin_html():
    return redirect('/lp/termin', code=301)

@app.route('/tierkommunikation-detail.html')
def redirect_tierkommunikation():
    return redirect('/dienstleistungen/tierkommunikation', code=301)

@app.route('/jenseitskontakt-tiere-detail.html')
def redirect_jenseitskontakt_tiere():
    return redirect('/dienstleistungen/jenseits-der-regenbogenbruecke', code=301)

@app.route('/booking.html')
def redirect_booking():
    return redirect('/buchung', code=301)

@app.route('/buchung-anmeldung')
def redirect_buchung_anmeldung():
    return redirect('/buchung', code=301)

@app.route('/seminar-backup')
def redirect_seminar_backup():
    return redirect('/', code=301)

@app.route('/<path:filename>')
def serve_pages(filename):
    if filename.endswith('.html'):
        return app.send_static_file(filename)
    return send_from_directory(app.static_folder, filename)


@app.route('/downloads/<path:filename>')
def download_file(filename):
    # In a real app, you might want to check if the user has a valid order
    # For now, we serve from the downloads folder
    downloads_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
    return send_from_directory(downloads_dir, filename)

@app.route('/api/test-email')
def test_email():
    test_order = {
        'order_number': 'TEST-123',
        'customer_name': 'Test User',
        'customer_email': 'info@sternenpfade.at',
        'customer_phone': '+43 123 456789',
        'billing_address': 'Teststraße 1, 1234 Testort',
        'total_amount': 10.0,
        'created_at': '2026-05-08',
        'items': [{'name': 'Test Artikel', 'price': 10.0, 'quantity': 1}]
    }
    from invoice_service import generate_invoice
    try:
        pdf_path = generate_invoice(test_order)
        success = send_order_confirmation(test_order, pdf_path)
        if success:
            return jsonify({'success': True, 'message': 'Test email sent successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to send email. Check logs.'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

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
                billing_address, shipping_address, notes, total_amount, payment_method, status, payment_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            'Erledigt' if total_amount == 0 else 'Offen',
            'Bezahlt' if total_amount == 0 else 'Ausstehend'
        ))
        
        order_id = cursor.lastrowid
        
        # Upsert customer details
        cust_name = data['customer_name'].strip()
        cust_email = data['customer_email'].strip()
        cust_phone = data.get('customer_phone', '').strip()
        cust_address = data['billing_address'].strip()
        if cust_name and cust_email:
            cursor.execute('SELECT id FROM customers WHERE name = ?', (cust_name,))
            cust_row = cursor.fetchone()
            if cust_row:
                cursor.execute('''
                    UPDATE customers SET email = ?, phone = ?, billing_address = ?
                    WHERE id = ?
                ''', (cust_email, cust_phone, cust_address, cust_row['id']))
            else:
                cursor.execute('''
                    INSERT INTO customers (name, email, phone, billing_address)
                    VALUES (?, ?, ?, ?)
                ''', (cust_name, cust_email, cust_phone, cust_address))
        
        # Update order number to a proper format
        order_number = str(order_id) # Set to exact ID (e.g., 140)
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
        print(f"Attempting to send confirmation email for order {order_number} to {order_dict.get('customer_email')}...")
        email_success = send_order_confirmation(order_dict, pdf_path)
        print(f"Email sending result: {email_success}")
        
        if email_success:
            return jsonify({
                'success': True,
                'message': 'Order created successfully',
                'order_id': order_id,
                'order_number': order_number
            }), 201
        else:
            return jsonify({
                'error': 'E-Mail Versand fehlgeschlagen. Bitte prüfe deine E-Mail Adresse oder kontaktiere uns direkt.',
                'order_number': order_number
            }), 500
            
    except Exception as e:
        conn.rollback()
        error_msg = str(e)
        print(f"Error in checkout: {error_msg}")
        return jsonify({'error': f'Fehler bei der Bestellung: {error_msg}'}), 500
    finally:
        conn.close()

@app.route('/api/admin/orders', methods=['POST'])
@requires_auth
def admin_create_order():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    required_fields = ['items']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    items = data.get('items', [])
    if not items:
        return jsonify({'error': 'Order must contain at least one item'}), 400

    # Extract and apply fallback default values if empty
    customer_name = data.get('customer_name', '').strip()
    if not customer_name:
        customer_name = 'Patrick Frech'

    customer_email = data.get('customer_email', '').strip()
    if not customer_email:
        customer_email = 'patrick.frech@hotmail.com'

    customer_phone = data.get('customer_phone', '').strip()
    if not customer_phone:
        customer_phone = '0650 803 8987'

    billing_address = data.get('billing_address', '').strip()
    if not billing_address:
        billing_address = 'Rechnungsstraße 1, 4493 Wolfern'

    total_amount = sum(item.get('price', 0) * item.get('quantity', 1) for item in items)
    
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO orders (
                order_number, customer_name, customer_email, customer_phone,
                billing_address, shipping_address, notes, total_amount, payment_method, status, payment_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            'TEMP', # Placeholder
            customer_name,
            customer_email,
            customer_phone,
            billing_address,
            data.get('shipping_address', ''),
            data.get('notes', ''),
            total_amount,
            data.get('payment_method', 'Überweisung, Vorkasse'),
            data.get('status', 'Offen'),
            data.get('payment_status', 'Ausstehend')
        ))
        
        order_id = cursor.lastrowid
        
        # Upsert customer details
        cust_name = customer_name.strip()
        cust_email = customer_email.strip()
        cust_phone = customer_phone.strip()
        cust_address = billing_address.strip()
        if cust_name and cust_email:
            cursor.execute('SELECT id FROM customers WHERE name = ?', (cust_name,))
            cust_row = cursor.fetchone()
            if cust_row:
                cursor.execute('''
                    UPDATE customers SET email = ?, phone = ?, billing_address = ?
                    WHERE id = ?
                ''', (cust_email, cust_phone, cust_address, cust_row['id']))
            else:
                cursor.execute('''
                    INSERT INTO customers (name, email, phone, billing_address)
                    VALUES (?, ?, ?, ?)
                ''', (cust_name, cust_email, cust_phone, cust_address))

        order_number = str(order_id)
        cursor.execute('UPDATE orders SET order_number = ? WHERE id = ?', (order_number, order_id))
        
        for item in items:
            cursor.execute('''
                INSERT INTO order_items (order_id, item_name, quantity, price)
                VALUES (?, ?, ?, ?)
            ''', (order_id, item['name'], item.get('quantity', 1), item['price']))
            
        conn.commit()
        
        # Fetch newly created order
        cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
        order_row = cursor.fetchone()
        
        order_dict = dict(order_row)
        order_dict['items'] = items
        order_dict['created_at'] = order_dict['created_at']
        
        # Generate Invoice
        pdf_path = generate_invoice(order_dict)
        
        # Send Email if requested
        email_sent = False
        if data.get('send_email', True):
            print(f"[Admin] Attempting to send confirmation email for manual order {order_number} to {order_dict.get('customer_email')}...")
            email_sent = send_order_confirmation(order_dict, pdf_path)
            print(f"[Admin] Email sending result: {email_sent}")
        else:
            print(f"[Admin] Skipping email confirmation for manual order {order_number} (requested by admin).")
            
        return jsonify({
            'success': True,
            'message': 'Bestellung erfolgreich manuell angelegt!',
            'order_id': order_id,
            'order_number': order_number,
            'email_sent': email_sent
        }), 201
        
    except Exception as e:
        conn.rollback()
        error_msg = str(e)
        print(f"Error in admin_create_order: {error_msg}")
        return jsonify({'error': f'Fehler bei der manuellen Bestellung: {error_msg}'}), 500
    finally:
        conn.close()

@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.json
    if not data:
        return jsonify({'error': 'Keine Daten übermittelt.'}), 400

    # Basic Validation
    required_fields = ['name', 'email', 'message']
    for field in required_fields:
        if field not in data or not str(data[field]).strip():
            return jsonify({'error': f'Bitte fülle das Feld "{field}" aus.'}), 400

    from email_service import send_contact_form
    try:
        success = send_contact_form(data)
        if success:
            return jsonify({'success': True, 'message': 'Vielen Dank! Deine Nachricht wurde erfolgreich gesendet.'}), 200
        else:
            return jsonify({'error': 'Fehler beim Senden der E-Mail. Bitte kontaktiere uns direkt via info@sternenpfade.at.'}), 500
    except Exception as e:
        print(f"Error in contact API: {e}")
        return jsonify({'error': f'Serverfehler beim Verarbeiten der Anfrage: {str(e)}'}), 500

# --- ADMIN ROUTES ---


@app.route('/api/admin/orders', methods=['GET'])
@requires_auth
def get_orders():
    # In a real app, verify admin authentication here
    conn = get_db_connection()
    try:
        # Get query parameters for filtering
        status_filter = request.args.get('status')
        payment_filter = request.args.get('payment_status')
        search_query = request.args.get('search')
        
        query = 'SELECT * FROM orders'
        params = []
        conditions = []
        
        if status_filter:
            conditions.append('status = ?')
            params.append(status_filter)
            
        if payment_filter:
            conditions.append('payment_status = ?')
            params.append(payment_filter)
            
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
@requires_auth
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
@requires_auth
def update_order_status(order_id):
    data = request.json
    new_status = data.get('status')
    new_payment_status = data.get('payment_status')
    
    if not new_status:
        return jsonify({'error': 'Status is required'}), 400
        
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        if new_payment_status:
            cursor.execute('UPDATE orders SET status = ?, payment_status = ? WHERE id = ?', (new_status, new_payment_status, order_id))
        else:
            cursor.execute('UPDATE orders SET status = ? WHERE id = ?', (new_status, order_id))
            
        if cursor.rowcount == 0:
            return jsonify({'error': 'Order not found'}), 404
            
        conn.commit()
        
        # If status is set to 'Erledigt', check if we need to send digital downloads
        if new_status == 'Erledigt':
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
@requires_auth
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

@app.route('/api/admin/orders/<int:order_id>/resend', methods=['POST'])
@requires_auth
def admin_resend_invoice(order_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
        order_row = cursor.fetchone()
        if not order_row:
            return jsonify({'error': 'Order not found'}), 404
            
        cursor.execute('SELECT * FROM order_items WHERE order_id = ?', (order_id,))
        items_rows = cursor.fetchall()
        
        order_dict = dict(order_row)
        order_dict['items'] = [dict(row) for row in items_rows]
        
        # Determine PDF invoice path
        filename = f"Rechnung_{order_dict['order_number']}.pdf"
        data_dir = os.environ.get('DATA_DIR', os.path.dirname(os.path.abspath(__file__)))
        pdf_path = os.path.join(data_dir, 'invoices', filename)
        
        # If invoice PDF doesn't exist, generate it
        if not os.path.exists(pdf_path):
            from invoice_service import generate_invoice
            pdf_path = generate_invoice(order_dict)
            
        # Send Email
        success = send_order_confirmation(order_dict, pdf_path)
        if success:
            return jsonify({'success': True, 'message': 'Rechnung erfolgreich erneut gesendet!'})
        else:
            return jsonify({'error': 'E-Mail Versand fehlgeschlagen. Bitte SMTP-Einstellungen prüfen.'}), 500
    except Exception as e:
        print(f"Error in resend: {e}")
        return jsonify({'error': f'Fehler beim Senden: {str(e)}'}), 500
    finally:
        conn.close()

@app.route('/api/admin/orders/<int:order_id>/refund', methods=['POST'])
@requires_auth
def admin_refund_order(order_id):
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    refund_type = data.get('refund_type')
    if refund_type not in ['full', 'items', 'custom']:
        return jsonify({'error': 'Invalid refund type'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1. Fetch original order
        cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
        original_order = cursor.fetchone()
        if not original_order:
            return jsonify({'error': 'Original order not found'}), 404

        original_order_dict = dict(original_order)

        # 2. Fetch original order items
        cursor.execute('SELECT * FROM order_items WHERE order_id = ?', (order_id,))
        original_items = cursor.fetchall()
        original_items_dict = [dict(item) for item in original_items]

        # 3. Determine refund items and total amount
        refund_items = []
        refund_total = 0.0

        if refund_type == 'full':
            for item in original_items_dict:
                item_qty = item['quantity']
                item_price = item['price']
                refund_items.append({
                    'name': f"Storno: {item['item_name']}",
                    'quantity': item_qty,
                    'price': -item_price
                })
                refund_total += (-item_price) * item_qty

        elif refund_type == 'items':
            selected_items = data.get('items', [])
            if not selected_items:
                return jsonify({'error': 'No items selected for refund'}), 400

            for sel_item in selected_items:
                # Find matching original item by name or id
                orig_item = next((item for item in original_items_dict if item['item_name'] == sel_item['name']), None)
                if not orig_item:
                    return jsonify({'error': f"Item '{sel_item['name']}' not found in original order"}), 400

                qty = int(sel_item.get('quantity', 0))
                if qty <= 0 or qty > orig_item['quantity']:
                    return jsonify({'error': f"Invalid quantity for item '{sel_item['name']}'"}), 400

                refund_items.append({
                    'name': f"Storno: {orig_item['item_name']}",
                    'quantity': qty,
                    'price': -orig_item['price']
                })
                refund_total += (-orig_item['price']) * qty

        elif refund_type == 'custom':
            custom_name = data.get('custom_name', '').strip()
            custom_price = data.get('custom_price', 0)
            try:
                custom_price = float(custom_price)
            except ValueError:
                return jsonify({'error': 'Invalid custom price'}), 400

            if not custom_name:
                custom_name = "Gutschrift / Freibetrag"
            else:
                custom_name = f"Gutschrift: {custom_name}"

            if custom_price <= 0:
                return jsonify({'error': 'Refund amount must be positive'}), 400

            refund_items.append({
                'name': custom_name,
                'quantity': 1,
                'price': -custom_price
            })
            refund_total = -custom_price

        # 4. Insert refund order
        cursor.execute('''
            INSERT INTO orders (
                order_number, customer_name, customer_email, customer_phone,
                billing_address, shipping_address, notes, total_amount, payment_method, status, payment_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            'TEMP', # Placeholder
            original_order_dict['customer_name'],
            original_order_dict['customer_email'],
            original_order_dict.get('customer_phone', ''),
            original_order_dict['billing_address'],
            original_order_dict.get('shipping_address', ''),
            f"Gutschrift / Storno zu Rechnung #{original_order_dict['order_number']}",
            refund_total,
            'Gutschrift',
            'Erledigt',
            'Bezahlt'
        ))

        new_order_id = cursor.lastrowid
        new_order_number = str(new_order_id)
        cursor.execute('UPDATE orders SET order_number = ? WHERE id = ?', (new_order_number, new_order_id))

        # 5. Insert refund items
        for r_item in refund_items:
            cursor.execute('''
                INSERT INTO order_items (order_id, item_name, quantity, price)
                VALUES (?, ?, ?, ?)
            ''', (new_order_id, r_item['name'], r_item['quantity'], r_item['price']))

        conn.commit()

        # 6. Fetch the newly created refund order dict
        cursor.execute('SELECT * FROM orders WHERE id = ?', (new_order_id,))
        refund_order_row = cursor.fetchone()
        refund_order_dict = dict(refund_order_row)
        refund_order_dict['items'] = refund_items

        # 7. Generate PDF Invoice for refund
        pdf_path = generate_invoice(refund_order_dict)

        # 8. Send Email if requested
        email_sent = False
        if data.get('send_email', True):
            print(f"[Refund] Sending refund PDF email for order {new_order_number} to {refund_order_dict.get('customer_email')}...")
            email_sent = send_order_confirmation(refund_order_dict, pdf_path)
            print(f"[Refund] Email sending result: {email_sent}")

        return jsonify({
            'success': True,
            'message': 'Gutschrift/Storno erfolgreich gebucht!',
            'order_id': new_order_id,
            'order_number': new_order_number,
            'email_sent': email_sent
        }), 201

    except Exception as e:
        conn.rollback()
        error_msg = str(e)
        print(f"Error in refund creation: {error_msg}")
        return jsonify({'error': f'Fehler beim Erstellen der Gutschrift: {error_msg}'}), 500
    finally:
        conn.close()

@app.route('/api/admin/customers', methods=['GET'])
@requires_auth
def get_admin_customers():
    search_query = request.args.get('search')
    conn = get_db_connection()
    try:
        if search_query:
            customers = conn.execute(
                'SELECT * FROM customers WHERE name LIKE ? OR email LIKE ? ORDER BY name',
                (f'%{search_query}%', f'%{search_query}%')
            ).fetchall()
        else:
            customers = conn.execute('SELECT * FROM customers ORDER BY name').fetchall()
        return jsonify([dict(row) for row in customers])
    finally:
        conn.close()

@app.route('/api/admin/customers/<int:customer_id>', methods=['DELETE'])
@requires_auth
def delete_admin_customer(customer_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Customer not found'}), 404
        conn.commit()
        return jsonify({'success': True, 'message': 'Customer deleted'})
    finally:
        conn.close()

@app.route('/api/admin/customers/<int:customer_id>', methods=['PUT'])
@requires_auth
def update_admin_customer(customer_id):
    data = request.json
    if not data or not data.get('name') or not data.get('email') or not data.get('billing_address'):
        return jsonify({'error': 'Missing required customer fields'}), 400
        
    name = data['name'].strip()
    email = data['email'].strip()
    phone = data.get('phone', '').strip()
    address = data['billing_address'].strip()
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Check if another customer with same name already exists
        cursor.execute('SELECT id FROM customers WHERE name = ? AND id != ?', (name, customer_id))
        if cursor.fetchone():
            return jsonify({'error': 'A customer with this name already exists'}), 400
            
        cursor.execute('''
            UPDATE customers SET name = ?, email = ?, phone = ?, billing_address = ?
            WHERE id = ?
        ''', (name, email, phone, address, customer_id))
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'Customer not found'}), 404
            
        conn.commit()
        return jsonify({'success': True, 'message': 'Customer updated'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/admin/customers', methods=['POST'])
@requires_auth
def create_admin_customer():
    data = request.json
    if not data or not data.get('name') or not data.get('email') or not data.get('billing_address'):
        return jsonify({'error': 'Missing required customer fields'}), 400
        
    name = data['name'].strip()
    email = data['email'].strip()
    phone = data.get('phone', '').strip()
    address = data['billing_address'].strip()
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # Check if exists
        cursor.execute('SELECT id FROM customers WHERE name = ?', (name,))
        if cursor.fetchone():
            return jsonify({'error': 'A customer with this name already exists'}), 400
            
        cursor.execute('''
            INSERT INTO customers (name, email, phone, billing_address)
            VALUES (?, ?, ?, ?)
        ''', (name, email, phone, address))
        conn.commit()
        return jsonify({'success': True, 'message': 'Customer created', 'id': cursor.lastrowid}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/admin/fix-db', methods=['POST'])
@requires_auth
def run_fix_database():
    from fix_db import fix_database
    success, logs = fix_database()
    if success:
        return jsonify({'success': True, 'message': 'Datenbank erfolgreich repariert!', 'logs': logs})
    else:
        return jsonify({'success': False, 'error': 'Fehler bei der Datenbankreparatur.', 'logs': logs}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

