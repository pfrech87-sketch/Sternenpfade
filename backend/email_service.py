import os
import smtplib
from email.message import EmailMessage
from email.utils import formatdate

SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USERNAME = os.environ.get('SMTP_USERNAME', '')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'info@sternenpfade.at')

# Mapping of product names to their download links
DIGITAL_PRODUCTS = {
    "Gratis Download: Herzens-Verständnis": "https://www.sternenpfade.at/downloads/herzens-verstaendnis.pdf",
    "Gratis Download Herzens-Verstaendnis": "https://www.sternenpfade.at/downloads/herzens-verstaendnis.pdf",
    "Heilreise mit Anubis": "https://www.sternenpfade.at/downloads/anubis-meditation.mp3",
    "Zurueck in deine Mitte": "https://www.sternenpfade.at/downloads/zurueck-in-deine-mitte.mp3"
}

def send_order_confirmation(order_dict, pdf_path):
    customer_email = order_dict.get('customer_email')
    if not customer_email:
        print("No customer email provided. Skipping email sending.")
        return False

    items = order_dict.get('items', [])
    download_links = []
    is_free_order = order_dict.get('total_amount', 0) == 0
    
    for item in items:
        name = item.get('name', item.get('item_name', ''))
        # Only include link in initial confirmation if it's a free order
        if name in DIGITAL_PRODUCTS and is_free_order:
            download_links.append((name, DIGITAL_PRODUCTS[name]))

    if not SMTP_USERNAME or not SMTP_PASSWORD:
        print("SMTP credentials not configured in environment variables. Skipping real email sending.")
        print(f"Simulated sending email to {customer_email}")
        print(f"Subject: Bestellbestätigung - Sternenpfade (Bestellnummer: {order_dict.get('order_number')})")
        if download_links:
            print(f"Contains downloads: {download_links}")
        return False

    msg = EmailMessage()
    msg['Subject'] = f"Bestellbestätigung - Sternenpfade (Bestellnummer: {order_dict.get('order_number')})"
    msg['From'] = SENDER_EMAIL
    msg['To'] = customer_email
    msg['Cc'] = 'info@sternenpfade.at'
    msg['Date'] = formatdate(localtime=True)

    # Build the body
    greeting = f"Hallo {order_dict.get('customer_name', '')},"
    thanks = "vielen lieben Dank für deine Bestellung bei Sternenpfade 🤍💙✨"
    
    if is_free_order:
        main_text = "dein gewünschter Download ist nun für dich bereit."
    else:
        main_text = f"deine Bestellung Nr. {order_dict.get('order_number')} ist bei mir eingegangen."

    body_parts = [greeting, "", thanks, main_text, ""]

    if download_links:
        body_parts.append("✨ DEINE DOWNLOADS:")
        for name, link in download_links:
            body_parts.append(f"- {name}: {link}")
        body_parts.append("")

    if not is_free_order:
        body_parts.append(f"Im Anhang findest du deine Rechnung zur Bestellung als PDF-Datei.")
        body_parts.append("")
        body_parts.append("Bitte überweise den Rechnungsbetrag vorab auf das auf der Rechnung angegebene Konto.")
        body_parts.append("Sobald die Zahlung eingelangt ist, beginne ich mit der Bearbeitung deiner Bestellung.")
        body_parts.append("")
    
    body_parts.append("Wenn es sich um eine Tierkommunikation oder einen Jenseitskontakt handelt, nehme ich mir dafür bewusst Zeit und verbinde mich in einem geschützten spirituellen Raum mit deinem Tier.")
    body_parts.append("Falls noch Informationen, Fragen oder ein Foto fehlen, melde ich mich persönlich bei dir.")
    body_parts.append("")
    body_parts.append("Bei Fragen kannst du dich jederzeit gerne bei mir melden.")
    body_parts.append("Von Herzen danke für dein Vertrauen.")
    body_parts.append("")
    body_parts.append("Herzensgruß")
    body_parts.append("Patrick")
    body_parts.append("Schamane, Tierkommunikator & Gründer von Sternenpfade")
    body_parts.append("✨ www.sternenpfade.at")

    body = "\n".join(body_parts)
    msg.set_content(body)

def send_digital_delivery(order_dict):
    customer_email = order_dict.get('customer_email')
    if not customer_email:
        return False

    items = order_dict.get('items', [])
    download_links = []
    
    for item in items:
        name = item.get('name', item.get('item_name', ''))
        if name in DIGITAL_PRODUCTS:
            download_links.append((name, DIGITAL_PRODUCTS[name]))

    if not download_links:
        return False # Nothing to deliver

    if not SMTP_USERNAME or not SMTP_PASSWORD:
        print(f"Simulated digital delivery email to {customer_email}")
        print(f"Downloads: {download_links}")
        return False

    msg = EmailMessage()
    msg['Subject'] = f"Deine Downloads von Sternenpfade - Bestellung {order_dict.get('order_number')}"
    msg['From'] = SENDER_EMAIL
    msg['To'] = customer_email
    msg['Date'] = formatdate(localtime=True)

    greeting = f"Hallo {order_dict.get('customer_name', '')},"
    body_parts = [
        greeting,
        "",
        "vielen Dank für deine Zahlung! Dein Download ist nun für dich bereit.",
        "",
        "✨ DEINE DOWNLOADS:",
    ]
    
    for name, link in download_links:
        body_parts.append(f"- {name}: {link}")
    
    body_parts.extend([
        "",
        "Ich wünsche dir viel Freude und tiefe Erkenntnisse damit.",
        "",
        "Bei Fragen kannst du dich jederzeit gerne bei mir melden.",
        "",
        "Herzensgruß",
        "Patrick",
        "✨ www.sternenpfade.at"
    ])

    msg.set_content("\n".join(body_parts))

    try:
        if SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        else:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send delivery email: {e}")
        return False

    # Attach PDF
    if pdf_path and os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as f:
            pdf_data = f.read()
            pdf_name = os.path.basename(pdf_path)
        
        msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename=pdf_name)

    try:
        if SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        else:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Successfully sent confirmation email to {customer_email}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
