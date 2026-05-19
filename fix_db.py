import sqlite3
import os
from import_historical_orders import HISTORICAL_ORDERS

def fix_database():
    data_dir = os.environ.get('DATA_DIR', os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(data_dir, 'sternenpfade.db')
    
    print(f"Connecting to database: {db_path}")
    if not os.path.exists(db_path):
        print("ERROR: Database file 'sternenpfade.db' not found!")
        return False, "Database file not found."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    logs = []
    
    try:
        # 1. Delete Evelyn Winkler's order (#194) and its items if it exists
        cursor.execute("SELECT id, customer_name FROM orders WHERE order_number = '194'")
        row = cursor.fetchone()
        if row:
            evelyn_id, name = row
            cursor.execute("DELETE FROM order_items WHERE order_id = ?", (evelyn_id,))
            cursor.execute("DELETE FROM orders WHERE id = ?", (evelyn_id,))
            msg = f"Deleted order #194 (Customer: {name}, ID: {evelyn_id}) and its items."
            print(msg)
            logs.append(msg)
        else:
            msg = "Order #194 not found or already deleted."
            print(msg)
            logs.append(msg)

        # 2. Get and delete all current imported orders and their items
        cursor.execute("SELECT id, order_number FROM orders WHERE status = 'Importiert'")
        imported_orders = cursor.fetchall()
        imported_ids = [row[0] for row in imported_orders]
        
        if imported_ids:
            placeholders = ','.join('?' for _ in imported_ids)
            # Delete order items
            cursor.execute(f"DELETE FROM order_items WHERE order_id IN ({placeholders})", imported_ids)
            # Delete orders
            cursor.execute(f"DELETE FROM orders WHERE id IN ({placeholders})", imported_ids)
            msg = f"Deleted {len(imported_ids)} existing imported orders (IDs: {min(imported_ids)} to {max(imported_ids)}) and their items."
            print(msg)
            logs.append(msg)
        else:
            msg = "No existing imported orders found to delete."
            print(msg)
            logs.append(msg)

        # 3. Re-insert the historical orders with explicit IDs
        imported_count = 0
        for order in HISTORICAL_ORDERS:
            order_id = int(order['order_number'])
            cursor.execute('''
                INSERT INTO orders (
                    id, order_number, customer_name, customer_email, customer_phone,
                    billing_address, shipping_address, status, payment_status,
                    payment_method, notes, total_amount, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                order_id,
                order['order_number'],
                order['customer_name'],
                order['customer_email'],
                '',  # Phone empty
                'Altes System Import',  # Billing Address
                '',  # Shipping Address empty
                'Importiert',  # Status
                order['payment_status'],
                'Altes System',
                'Import altes System',  # Notes
                order['total_amount'],
                order['created_at']
            ))
            
            # Insert standard item
            cursor.execute('''
                INSERT INTO order_items (order_id, item_name, quantity, price)
                VALUES (?, ?, ?, ?)
            ''', (order_id, 'Historischer Import', 1, order['total_amount']))
            imported_count += 1
            
        msg = f"Re-imported {imported_count} historical orders with correct database IDs (90 to 138)."
        print(msg)
        logs.append(msg)

        # 4. Find the maximum ID of non-imported (real) orders
        cursor.execute("SELECT MAX(id) FROM orders WHERE status != 'Importiert'")
        max_real_id = cursor.fetchone()[0]
        if max_real_id is None:
            max_real_id = 0
            
        # 5. Set sqlite_sequence to max_real_id
        cursor.execute("UPDATE sqlite_sequence SET seq = ? WHERE name = 'orders'", (max_real_id,))
        if cursor.rowcount == 0:
            cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('orders', ?)", (max_real_id,))
            
        msg = f"Set sequence counter for 'orders' to {max_real_id}. The next new order will start with ID/number {max_real_id + 1}."
        print(msg)
        logs.append(msg)
        
        conn.commit()
        return True, logs
        
    except Exception as e:
        conn.rollback()
        error_msg = f"Error fixing database: {str(e)}"
        print(error_msg)
        return False, [error_msg]
    finally:
        conn.close()

if __name__ == '__main__':
    success, logs = fix_database()
    if success:
        print("\nDatabase fix completed successfully!")
    else:
        print("\nDatabase fix failed.")
