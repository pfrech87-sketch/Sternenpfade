import sqlite3
import os

DATA_DIR = os.environ.get('DATA_DIR', os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(DATA_DIR, 'sternenpfade.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Orders Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            customer_phone TEXT,
            billing_address TEXT NOT NULL,
            shipping_address TEXT,
            status TEXT DEFAULT 'Offen',
            payment_status TEXT DEFAULT 'Ausstehend',
            payment_method TEXT DEFAULT 'Überweisung, Vorkasse',
            notes TEXT,
            total_amount REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create Order Items Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id)
        )
    ''')

    # Create Admin Users Table (optional for now, can hardcode login or use basic auth, but good to have)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')

    # Create Customers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            billing_address TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Populate customers from existing orders if customers table is empty
    cursor.execute('SELECT COUNT(*) as count FROM customers')
    if cursor.fetchone()[0] == 0:
        cursor.execute('SELECT DISTINCT customer_name, customer_email, customer_phone, billing_address FROM orders')
        existing_orders = cursor.fetchall()
        for row in existing_orders:
            name = row['customer_name'].strip() if row['customer_name'] else ''
            email = row['customer_email'].strip() if row['customer_email'] else ''
            phone = row['customer_phone'].strip() if row['customer_phone'] else ''
            address = row['billing_address'].strip() if row['billing_address'] else ''
            if name and email:
                cursor.execute('''
                    INSERT OR IGNORE INTO customers (name, email, phone, billing_address)
                    VALUES (?, ?, ?, ?)
                ''', (name, email, phone, address))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
