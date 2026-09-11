import os
import glob

for filepath in glob.glob('admin/*.html'):
    if 'chat-logs.html' in filepath:
        continue
    with open(filepath, 'r') as f:
        content = f.read()
    
    if 'Chat-Logs' not in content and 'class="nav-links"' in content:
        # Find where to insert it, maybe after "Kunden"
        content = content.replace('<li><a href="customers.html">Kunden</a></li>', '<li><a href="customers.html">Kunden</a></li>\n                <li><a href="chat-logs.html">Chat-Logs</a></li>')
        content = content.replace('<li><a href="/admin/customers.html">Kunden</a></li>', '<li><a href="/admin/customers.html">Kunden</a></li>\n                <li><a href="/admin/chat-logs.html">Chat-Logs</a></li>')
        
        with open(filepath, 'w') as f:
            f.write(content)
