import sqlite3
import os

# --- DIE ECHTEN HISTORISCHEN BESTELLUNGEN AUS WEBADOR (2026) ---
HISTORICAL_ORDERS = [
    {'order_number': '138', 'customer_name': 'Janine Mayer', 'customer_email': 'info@sternenpfade.at', 'total_amount': 40.0, 'created_at': '2026-04-30 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '137', 'customer_name': 'Johann Becker', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-04-20 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '136', 'customer_name': 'Elisabeth Rieder', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-04-20 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '135', 'customer_name': 'Heidelinde G.', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-04-16 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '134', 'customer_name': 'Brenda Knapp', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-04-12 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '133', 'customer_name': 'Michaela K.', 'customer_email': 'info@sternenpfade.at', 'total_amount': 120.0, 'created_at': '2026-04-12 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '132', 'customer_name': 'Nathalie Hirr', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-04-12 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '131', 'customer_name': 'Elisabeth Rieder', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-04-02 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '130', 'customer_name': 'Evelyn Steink.', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-03-31 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '129', 'customer_name': 'Amina Godus', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-03-30 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '128', 'customer_name': 'Aaron Alfred C.', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-03-28 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '127', 'customer_name': 'Nathalie Hirr', 'customer_email': 'info@sternenpfade.at', 'total_amount': 180.0, 'created_at': '2026-03-28 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '126', 'customer_name': 'Mirjam Baum', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-03-28 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '125', 'customer_name': 'Julia Breyer', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-03-24 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '124', 'customer_name': 'Aaron Coen', 'customer_email': 'info@sternenpfade.at', 'total_amount': 0.0, 'created_at': '2026-03-21 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '123', 'customer_name': 'Janine Mayer', 'customer_email': 'info@sternenpfade.at', 'total_amount': 40.0, 'created_at': '2026-03-19 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '122', 'customer_name': 'Renate Wers.', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-03-16 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '121', 'customer_name': 'Elisabeth Rieder', 'customer_email': 'info@sternenpfade.at', 'total_amount': 50.0, 'created_at': '2026-03-16 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '120', 'customer_name': 'Barbara Mar', 'customer_email': 'info@sternenpfade.at', 'total_amount': 120.0, 'created_at': '2026-03-16 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '119', 'customer_name': 'Johann Becker', 'customer_email': 'info@sternenpfade.at', 'total_amount': 120.0, 'created_at': '2026-03-16 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '118', 'customer_name': 'Janine Mayer', 'customer_email': 'info@sternenpfade.at', 'total_amount': 40.0, 'created_at': '2026-03-06 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '117', 'customer_name': 'Anita Walchho', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-03-02 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '116', 'customer_name': 'Elisabeth Rieder', 'customer_email': 'info@sternenpfade.at', 'total_amount': 40.0, 'created_at': '2026-02-28 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '115', 'customer_name': 'Barbara Wur', 'customer_email': 'info@sternenpfade.at', 'total_amount': 0.0, 'created_at': '2026-02-28 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '114', 'customer_name': 'Judith Nagy', 'customer_email': 'info@sternenpfade.at', 'total_amount': 40.0, 'created_at': '2026-02-28 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '113', 'customer_name': 'Judith Nagy', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-02-15 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '112', 'customer_name': 'Barbara Hufe', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-02-15 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '111', 'customer_name': 'Nathalie Hub', 'customer_email': 'info@sternenpfade.at', 'total_amount': 40.0, 'created_at': '2026-02-15 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '110', 'customer_name': 'Janine Mayer', 'customer_email': 'info@sternenpfade.at', 'total_amount': 30.0, 'created_at': '2026-02-10 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '109', 'customer_name': 'Elisabeth Rieder', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-02-10 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '108', 'customer_name': 'Alexandra Ob', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-02-10 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '107', 'customer_name': 'Sandra Prukl', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-02-10 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '106', 'customer_name': 'Christine Fre', 'customer_email': 'info@sternenpfade.at', 'total_amount': 40.0, 'created_at': '2026-02-09 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '105', 'customer_name': 'Milena Bokle', 'customer_email': 'info@sternenpfade.at', 'total_amount': 30.0, 'created_at': '2026-02-09 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '104', 'customer_name': 'Andrea Weiss', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-02-09 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '103', 'customer_name': 'Carla Tecime', 'customer_email': 'info@sternenpfade.at', 'total_amount': 180.0, 'created_at': '2026-02-03 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '102', 'customer_name': 'Doris Stöckl', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-02-03 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '101', 'customer_name': 'Katrin Hager', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-02-03 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '100', 'customer_name': 'Kevin Wörger', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-02-03 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '99', 'customer_name': 'Hans Becker', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-02-03 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '98', 'customer_name': 'Regina Tierhi', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-02-03 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '97', 'customer_name': 'Ursula Lackn', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-02-03 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '96', 'customer_name': 'Susanne Sch', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-01-31 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '95', 'customer_name': 'Andrea Saute', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-01-26 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '94', 'customer_name': 'Caroline Koe', 'customer_email': 'info@sternenpfade.at', 'total_amount': 0.0, 'created_at': '2026-01-21 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '93', 'customer_name': 'Sonja Wagne', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-01-15 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '92', 'customer_name': 'Doris Stöckl', 'customer_email': 'info@sternenpfade.at', 'total_amount': 0.0, 'created_at': '2026-01-11 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '91', 'customer_name': 'Conny Hötsch', 'customer_email': 'info@sternenpfade.at', 'total_amount': 90.0, 'created_at': '2026-01-06 12:00:00', 'payment_status': 'Bezahlt'},
    {'order_number': '90', 'customer_name': 'Romana Wagn', 'customer_email': 'info@sternenpfade.at', 'total_amount': 40.0, 'created_at': '2026-01-06 12:00:00', 'payment_status': 'Bezahlt'}
]

def import_orders():
    data_dir = os.environ.get('DATA_DIR', os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(data_dir, 'sternenpfade.db')
    
    print(f"Verbinde mit der Datenbank: {db_path}")
    
    if not os.path.exists(db_path):
        print("FEHLER: Datenbankdatei 'sternenpfade.db' nicht gefunden!")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    imported_count = 0
    skipped_count = 0
    
    for order in HISTORICAL_ORDERS:
        # Prüfen, ob die Bestellnummer bereits existiert
        cursor.execute("SELECT id FROM orders WHERE order_number = ?", (order['order_number'],))
        exists = cursor.fetchone()
        
        if exists:
            print(f"Übersprungen: Bestellnummer {order['order_number']} existiert bereits in der Datenbank.")
            skipped_count += 1
            continue
            
        try:
            cursor.execute('''
                INSERT INTO orders (
                    order_number, customer_name, customer_email, customer_phone,
                    billing_address, shipping_address, status, payment_status,
                    payment_method, notes, total_amount, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                order['order_number'],
                order['customer_name'],
                order['customer_email'],
                '',  # Telefonnummer leer
                'Altes System Import',  # Rechnungsadresse
                '',  # Lieferadresse leer
                'Importiert',  # Bearbeitungsstatus auf 'Importiert' gesetzt
                order['payment_status'],
                'Altes System',
                'Import altes System',  # Hinweis im Notizenfeld
                order['total_amount'],
                order['created_at']
            ))
            
            # Leeres Item in order_items anlegen, damit es keine Verknüpfungsfehler gibt
            order_id = cursor.lastrowid
            cursor.execute('''
                INSERT INTO order_items (order_id, item_name, quantity, price)
                VALUES (?, ?, ?, ?)
            ''', (order_id, 'Historischer Import', 1, order['total_amount']))
            
            imported_count += 1
            print(f"Erfolgreich importiert: {order['order_number']} - {order['customer_name']} ({order['total_amount']} EUR)")
            
        except Exception as e:
            print(f"Fehler beim Importieren von {order['order_number']}: {e}")
            
    conn.commit()
    conn.close()
    
    print("\n--- IMPORT ABGESCHLOSSEN ---")
    print(f"Erfolgreich importiert: {imported_count}")
    print(f"Bereits vorhanden (übersprungen): {skipped_count}")

if __name__ == '__main__':
    import_orders()
