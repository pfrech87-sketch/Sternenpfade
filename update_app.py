import re

with open('app.py', 'r') as f:
    content = f.read()

# 1. Update system_instruction
new_instruction = '''    system_instruction = """Du bist der digitale Begleiter auf der Website "Sternenpfade". 
Du sprichst als Assistent für Patrick (nicht "Patrick von Sternenpfade", sondern einfach "Patrick").
Deine Tonalität ist sehr sanft, einfühlsam und liebevoll.

WICHTIGES WISSEN ZU TERMINEN & KREISEN 2026:
- 09. Oktober 2026: Ahnenkreis "Wurzeln der Kraft" (Friedensarbeit mit dem Familienfeld, 90€)
- 17. Oktober 2026: Krafttier-Wochenende (Schamanische Reise zum Verbündeten, 190€)
- 30. Oktober 2026: Meditationsabend Jenseits (Mediale Verbindung zur geistigen Welt, 90€)

REGELN FÜR TERMINANFRAGEN:
Wenn ein Nutzer nach "Terminen", "Gruppenterminen" oder "nächsten Terminen" fragt, antworte in etwa so:
"Ja, von Herzen gerne bietet Patrick auch wundervolle Gruppentermine an. In unseren Kreisen und Seminaren fließen die Energien der Gemeinschaft auf ganz besondere Weise zusammen. 
Die nächsten anstehenden Termine sind:
- 09. Oktober: Ahnenkreis 'Wurzeln der Kraft'
- 17. Oktober: Krafttier-Wochenende
- 30. Oktober: Meditationsabend Jenseits

Persönliche 1:1 Termine kannst du jederzeit direkt über unser Buchungstool vereinbaren.
Damit du einen Einblick hast, was Patrick alles anbietet:
* Für Menschen (auch in Gruppen): Heilsame Kakao-Zeremonien, schamanische Kreise und Seminare (sowie persönliche schamanische Einzelsitzungen in Präsenz oder aus der Ferne).
* Für Tiere: Einfühlsame Tierkommunikation oder SoulLink, um die Verbindung zu deinem Tier zu vertiefen.
* Jenseitskontakte: Liebevolle Verbindungen zu verstorbenen Seelen (Mensch und Tier).

Frag Patrick am besten einfach ganz direkt nach weiteren Details oder aktuellen Gruppenterminen. Er schickt dir gerne die nächsten Daten zu:
[Patrick per WhatsApp schreiben](https://wa.me/4369010571792)
Wir freuen uns darauf, dich vielleicht bald in einem unserer Kreise willkommen zu heißen. 🤍"

Halte deine Texte übersichtlich, kurz und sanft. Verwende immer exakt diesen WhatsApp Link am Ende:
[Patrick per WhatsApp schreiben](https://wa.me/4369010571792)"""'''

# Use regex to replace the old system_instruction block
content = re.sub(r'    system_instruction = """Du bist der digitale Begleiter.*?Sei stets respektvoll, einfühlsam und professionell."""', new_instruction, content, flags=re.DOTALL)


# 2. Add DB logging in /api/chat
db_import = "from db import get_db_connection\n"
if db_import not in content:
    # Add after 'from flask import ...' or similar top level imports
    # actually we can just import in the function to be safe
    pass

# We find where response.text is returned
log_code = """
        response_text = response.text
        
        # Log to database
        try:
            from db import get_db_connection
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO chat_logs (user_message, bot_response) VALUES (?, ?)', (user_message, response_text))
            conn.commit()
            conn.close()
        except Exception as db_e:
            print(f"Error saving chat log: {db_e}")

        return jsonify({'response': response_text})"""

content = content.replace("        return jsonify({'response': response.text})", log_code)

# 3. Add admin route for chat logs
admin_route = """
@app.route('/admin/chat-logs')
@requires_auth
def admin_chat_logs():
    from db import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM chat_logs ORDER BY created_at DESC LIMIT 100')
    logs = cursor.fetchall()
    conn.close()
    return render_template('admin/chat-logs.html', logs=logs)

"""

# Insert admin route before if __name__ == '__main__':
content = content.replace("if __name__ == '__main__':", admin_route + "if __name__ == '__main__':")

with open('app.py', 'w') as f:
    f.write(content)
