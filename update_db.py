import sqlite3
import os

def update_sequence():
    data_dir = os.environ.get('DATA_DIR', os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(data_dir, 'sternenpfade.db')
    
    print(f"Versuche Datenbank zu aktualisieren: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Setze den Zähler für 'orders' auf 139 (nächste ID wird 140)
        cursor.execute("UPDATE sqlite_sequence SET seq = 139 WHERE name='orders'")
        
        # Überprüfe ob der Eintrag existiert hat, wenn nicht, füge ihn hinzu
        if cursor.rowcount == 0:
            cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('orders', 139)")
            
        conn.commit()
        conn.close()
        print("Erfolgreich! Die nächste Bestellung erhält die Nummer 140.")
        
    except Exception as e:
        print(f"Fehler: {e}")

if __name__ == '__main__':
    update_sequence()
