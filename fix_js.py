with open('js/chatbot.js', 'r') as f:
    content = f.read()

bad_func = """    function updateMessageHTML(msgDiv, text) {
        if (!text) {
            msgDiv.innerHTML = '';
            return;
        }
        let html = text
            .replace(/\\\\*\\\\*(.*?)\\\\*\\\\*/g, '<strong>$1</strong>')
            .replace(/\\\\*(.*?)\\\\*/g, '<em>$1</em>')
            .replace(/\\\\\\[(.*?)\\\\\\]\\\\((.*?)\\\\)/g, '<a href="$2" target="_blank" class="chat-link">$1</a>')
            .replace(/\\\\n/g, '<br>');
        msgDiv.innerHTML = html;
    }"""

good_func = """    function updateMessageHTML(msgDiv, text) {
        if (!text) {
            msgDiv.innerHTML = '';
            return;
        }
        let html = text
            .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
            .replace(/\\*(.*?)\\*/g, '<em>$1</em>')
            .replace(/\\[(.*?)\\]\\((.*?)\\)/g, '<a href="$2" target="_blank" class="chat-link">$1</a>')
            .replace(/\\n/g, '<br>');
        msgDiv.innerHTML = html;
    }"""

if bad_func in content:
    content = content.replace(bad_func, good_func)
else:
    # Just replace all backslash issues
    import re
    content = re.sub(r'\\\\', r'\\', content)
    
with open('js/chatbot.js', 'w') as f:
    f.write(content)
