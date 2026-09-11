with open('app.py', 'r') as f:
    content = f.read()

import re

# We want to replace the part in /api/chat that says:
#         chat_session = model.start_chat(history=formatted_history)
#         response = chat_session.send_message(user_message)
#         
# 
#         response_text = response.text
#         ...
#         return jsonify({'response': response_text})

old_code_pattern = r"        chat_session = model\.start_chat\(history=formatted_history\)\s*response = chat_session\.send_message\(user_message\)\s*response_text = response\.text.*?return jsonify\(\{'response': response_text\}\)"

new_code = """        chat_session = model.start_chat(history=formatted_history)
        response = chat_session.send_message(user_message, stream=True)
        
        def generate():
            full_response = ""
            try:
                for chunk in response:
                    text = chunk.text
                    if text:
                        full_response += text
                        import json
                        yield f"data: {json.dumps({'text': text})}\\n\\n"
                
                # Log to database
                try:
                    from db import get_db_connection
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO chat_logs (user_message, bot_response) VALUES (?, ?)', (user_message, full_response))
                    conn.commit()
                    conn.close()
                except Exception as db_e:
                    print(f"Error saving chat log: {db_e}")
                    
            except Exception as e:
                import traceback
                traceback.print_exc()
                import json
                yield f"data: {json.dumps({'error': 'Fehler bei der Generierung'})}\\n\\n"
            
            yield "data: [DONE]\\n\\n"

        from flask import Response
        return Response(generate(), mimetype='text/event-stream')"""

content = re.sub(old_code_pattern, new_code, content, flags=re.DOTALL)

with open('app.py', 'w') as f:
    f.write(content)
