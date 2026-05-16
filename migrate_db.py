import sqlite3
import os

def migrate_db():
    data_dir = os.environ.get('DATA_DIR', os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(data_dir, 'sternenpfade.db')
    
    print(f"Versuche Datenbank zu migrieren: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Füge neue Spalte 'payment_status' hinzu
        cursor.execute("ALTER TABLE orders ADD COLUMN payment_status TEXT DEFAULT 'Ausstehend'")
        
        # 2. Bestehenden 'status' in 'payment_status' kopieren
        cursor.execute("UPDATE orders SET payment_status = status")
        
        # 3. Alte Statuswerte an das neue 'Offen' und 'Erledigt' anpassen
        cursor.execute("UPDATE orders SET status = 'Offen' WHERE status = 'Ausstehend'")
        cursor.execute("UPDATE orders SET status = 'Erledigt' WHERE status = 'Abgeschlossen'")
        
        conn.commit()
        conn.close()
        print("Erfolgreich! Datenbank ist bereit für die neuen Statusfelder.")
        
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Spalte existiert bereits! Migration wurde schon durchgeführt.")
        else:
            print(f"SQL Fehler: {e}")
    except Exception as e:
        print(f"Fehler: {e}")

if __name__ == '__main__':
    migrate_db()
