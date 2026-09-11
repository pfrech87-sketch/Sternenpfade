with open('app.py', 'r') as f:
    content = f.read()

# Replace the chat-logs route to be an API route instead of render_template
old_route = """@app.route('/admin/chat-logs')
@requires_auth
def admin_chat_logs():
    from db import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM chat_logs ORDER BY created_at DESC LIMIT 100')
    logs = cursor.fetchall()
    conn.close()
    return render_template('admin/chat-logs.html', logs=logs)"""

new_route = """@app.route('/api/chat-logs')
@requires_auth
def api_chat_logs():
    from db import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM chat_logs ORDER BY created_at DESC LIMIT 100')
    logs = cursor.fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in logs])"""

content = content.replace(old_route, new_route)

with open('app.py', 'w') as f:
    f.write(content)
