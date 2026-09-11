// js/chatbot.js

(function initChatbotUI() {
    // Inject the Chatbot HTML
    const chatbotHTML = `
        <div id="sternenpfade-chatbot-container">
            <div id="sternenpfade-chatbot-window">
                <div id="sternenpfade-chatbot-header">
                    <h3>Sternenpfade Assistent</h3>
                    <button id="sternenpfade-chatbot-close">&times;</button>
                </div>
                <div id="sternenpfade-chatbot-messages">
                    <div class="chatbot-message bot">Hallo! Ich bin der kleine Sternenfuchs. Wie kann ich dir heute auf deinem Weg weiterhelfen?</div>
                </div>
                
                <div id="sternenpfade-chatbot-suggestions">
                    <div class="chatbot-suggestion-chip">Wann sind die nächsten Termine?</div>
                    <div class="chatbot-suggestion-chip">Gibt es Gruppentermine?</div>
                    <div class="chatbot-suggestion-chip">Was ist Tierkommunikation?</div>
                </div>
                <div id="sternenpfade-chatbot-input-area">
                    <input type="text" id="sternenpfade-chatbot-input" placeholder="Schreibe eine Nachricht..." autocomplete="off" />
                    <button id="sternenpfade-chatbot-send">
                        <svg viewBox="0 0 24 24">
                            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"></path>
                        </svg>
                    </button>
                </div>
            </div>
            <div id="sternenpfade-chatbot-prompt">Brauchst du Hilfe?</div>
            <div id="sternenpfade-chatbot-avatar"></div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', chatbotHTML);

    const avatar = document.getElementById('sternenpfade-chatbot-avatar');
    const chatWindow = document.getElementById('sternenpfade-chatbot-window');
    const closeBtn = document.getElementById('sternenpfade-chatbot-close');
    const messagesContainer = document.getElementById('sternenpfade-chatbot-messages');
    const inputField = document.getElementById('sternenpfade-chatbot-input');
    const sendBtn = document.getElementById('sternenpfade-chatbot-send');

    let chatHistory = [];

    // Toggle Chat Window
    avatar.addEventListener('click', () => {
        chatWindow.classList.toggle('active');
        const container = document.getElementById('sternenpfade-chatbot-container');
        container.classList.toggle('chat-active');
        
        if (chatWindow.classList.contains('active')) {
            inputField.focus();
            // GTM Tracking: Chatbot Opened
            window.dataLayer = window.dataLayer || [];
            window.dataLayer.push({
                'event': 'chatbot_open'
            });
        }
    });

    closeBtn.addEventListener('click', () => {
        chatWindow.classList.remove('active');
        const container = document.getElementById('sternenpfade-chatbot-container');
        container.classList.remove('chat-active');
    });

    // Send Message
    const sendMessage = async () => {
        const text = inputField.value.trim();
        if (!text) return;

        // Add user message to UI
        addMessage(text, 'user');
        inputField.value = '';

        // GTM Tracking: Chatbot Message Sent
        window.dataLayer = window.dataLayer || [];
        window.dataLayer.push({
            'event': 'chatbot_message_sent'
        });

        // Add typing indicator
        const typingId = showTypingIndicator();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: text, history: chatHistory })
            });

            removeTypingIndicator(typingId);

            if (response.ok) {
                const msgDiv = addMessage('', 'bot');
                let fullResponse = "";
                
                const reader = response.body.getReader();
                const decoder = new TextDecoder("utf-8");
                let buffer = "";

                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;
                    
                    buffer += decoder.decode(value, { stream: true });
                    const lines = buffer.split('\n');
                    buffer = lines.pop(); // keep incomplete line
                    
                    for (const line of lines) {
                        if (line.startsWith('data: ') && line !== 'data: [DONE]') {
                            const dataStr = line.substring(6);
                            try {
                                const dataObj = JSON.parse(dataStr);
                                if (dataObj.text) {
                                    fullResponse += dataObj.text;
                                    updateMessageHTML(msgDiv, fullResponse);
                                    scrollToBottom();
                                } else if (dataObj.error) {
                                    updateMessageHTML(msgDiv, "Es gab einen Fehler während der Generierung.");
                                    scrollToBottom();
                                }
                            } catch (e) {
                                console.error("Error parsing SSE:", e);
                            }
                        }
                    }
                }
                
                // Update history
                chatHistory.push({ role: 'user', content: text });
                chatHistory.push({ role: 'model', content: fullResponse });
            } else {
                addMessage('Verzeihung, es gab einen Fehler bei der Verbindung. Bitte versuche es später noch einmal.', 'bot');
            }
        } catch (error) {
            removeTypingIndicator(typingId);
            addMessage('Verzeihung, es gab einen Fehler bei der Verbindung. Bitte versuche es später noch einmal.', 'bot');
            console.error('Chat API Error:', error);
        }
    };

    sendBtn.addEventListener('click', sendMessage);
    
    // Add event listeners to suggestion chips
    document.querySelectorAll('.chatbot-suggestion-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            inputField.value = chip.textContent;
            sendMessage();
            // Hide suggestions after first use
            document.getElementById('sternenpfade-chatbot-suggestions').style.display = 'none';
        });
    });
    inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    function addMessage(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `chatbot-message ${sender}`;
        if (sender === 'bot') {
            updateMessageHTML(msgDiv, text);
        } else {
            msgDiv.textContent = text;
        }
        messagesContainer.appendChild(msgDiv);
        scrollToBottom();
        return msgDiv;
    }

    function updateMessageHTML(msgDiv, text) {
        if (!text) {
            msgDiv.innerHTML = '';
            return;
        }
        let html = text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" class="chat-link">$1</a>')
            .replace(/\n/g, '<br>');
        msgDiv.innerHTML = html;
    }

    function showTypingIndicator() {
        const id = 'typing-' + Date.now();
        const indicator = document.createElement('div');
        indicator.id = id;
        indicator.className = 'chatbot-typing-indicator';
        indicator.innerHTML = `
            <div class="chatbot-typing-dot"></div>
            <div class="chatbot-typing-dot"></div>
            <div class="chatbot-typing-dot"></div>
        `;
        messagesContainer.appendChild(indicator);
        scrollToBottom();
        return id;
    }

    function removeTypingIndicator(id) {
        const indicator = document.getElementById(id);
        if (indicator) {
            indicator.remove();
        }
    }

    function scrollToBottom() {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
})();
