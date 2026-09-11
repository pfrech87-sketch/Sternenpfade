with open('js/chatbot.js', 'r') as f:
    content = f.read()

# Insert the suggestions div in HTML
html_to_find = '<div id="sternenpfade-chatbot-input-area">'
suggestions_html = '''
                <div id="sternenpfade-chatbot-suggestions">
                    <div class="chatbot-suggestion-chip">Wann sind die nächsten Termine?</div>
                    <div class="chatbot-suggestion-chip">Gibt es Gruppentermine?</div>
                    <div class="chatbot-suggestion-chip">Was ist Tierkommunikation?</div>
                </div>
                <div id="sternenpfade-chatbot-input-area">'''
content = content.replace(html_to_find, suggestions_html)

# Insert the event listeners for chips
js_to_find = 'sendBtn.addEventListener(\'click\', sendMessage);'
chips_js = '''sendBtn.addEventListener('click', sendMessage);
    
    // Add event listeners to suggestion chips
    document.querySelectorAll('.chatbot-suggestion-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            inputField.value = chip.textContent;
            sendMessage();
            // Hide suggestions after first use
            document.getElementById('sternenpfade-chatbot-suggestions').style.display = 'none';
        });
    });'''
content = content.replace(js_to_find, chips_js)

with open('js/chatbot.js', 'w') as f:
    f.write(content)
