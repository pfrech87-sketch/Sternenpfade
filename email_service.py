import os
import smtplib
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# SMTP Konfiguration für Webador
SMTP_SERVER = "smtp.webador.com"
SMTP_USER = "info@sternenpfade.at"
SMTP_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')

SENDER_NAME = "Sternenpfade"

# Mapping der digitalen Produkte
DIGITAL_PRODUCTS = {
    "Gratis Download: Herzens-Verständnis": "https://www.sternenpfade.at/downloads/herzens-verstaendnis.pdf",
    "Gratis Download Herzens-Verstaendnis": "https://www.sternenpfade.at/downloads/herzens-verstaendnis.pdf",
    "Heilreise mit Anubis": "https://www.sternenpfade.at/downloads/anubis-meditation.mp3",
    "Zurueck in deine Mitte": "https://www.sternenpfade.at/downloads/zurueck-in-deine-mitte.mp3"
}

def _create_message(to_email, subject, body_parts):
    """Hilfsfunktion zum Erstellen einer Multipart-E-Mail (HTML & Text)"""
    text_content = "\n".join(body_parts)
    html_content = "<html><body style='font-family: sans-serif; line-height: 1.6; color: #333; max-width: 600px;'>" + \
                   "<br/>".join(body_parts).replace("\n", "<br/>") + \
                   "</body></html>"

    msg = MIMEMultipart('alternative')
    msg['From'] = f"{SENDER_NAME} <{SMTP_USER}>"
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(text_content, 'plain'))
    msg.attach(MIMEText(html_content, 'html'))
    return msg

def _send_via_smtp(msg):
    """Hilfsfunktion zum Versenden über verschiedene Ports"""
    if not SMTP_PASSWORD:
        print("Fehler: EMAIL_PASSWORD nicht gesetzt.")
        return False

    # Wir probieren Port 465 (SSL) und 587 (STARTTLS)
    for port in [465, 587]:
        try:
            if port == 465:
                with smtplib.SMTP_SSL(SMTP_SERVER, port, timeout=15) as server:
                    server.login(SMTP_USER, SMTP_PASSWORD)
                    server.send_message(msg)
                    return True
            else:
                with smtplib.SMTP(SMTP_SERVER, port, timeout=15) as server:
                    server.starttls()
                    server.login(SMTP_USER, SMTP_PASSWORD)
                    server.send_message(msg)
                    return True
        except Exception as e:
            print(f"Versand über Port {port} fehlgeschlagen: {e}")
            continue
    return False

def send_order_confirmation(order_dict, pdf_path):
    customer_email = str(order_dict.get('customer_email', '')).strip()
    customer_name = str(order_dict.get('customer_name', '')).strip()
    
    if not customer_email: return False

    items = order_dict.get('items', [])
    download_links = []
    is_free_order = order_dict.get('total_amount', 0) == 0
    
    for item in items:
        name = item.get('name', item.get('item_name', ''))
        if name in DIGITAL_PRODUCTS and is_free_order:
            download_links.append((name, DIGITAL_PRODUCTS[name]))

    subject = f"Bestellbestätigung - Sternenpfade (Nr. {order_dict.get('order_number')})"

    body_parts = [
        f"Hallo {customer_name},", "",
        "vielen lieben Dank für deine Bestellung bei Sternenpfade 🤍💙✨",
        "dein Download ist nun bereit." if is_free_order else f"deine Bestellung Nr. {order_dict.get('order_number')} ist eingegangen.",
        ""
    ]

    if download_links:
        body_parts.append("✨ DEINE DOWNLOADS:")
        for name, link in download_links:
            body_parts.append(f"- {name}: {link}")
        body_parts.append("")

    if not is_free_order:
        body_parts.extend([
            "Im Anhang findest du deine Rechnung als PDF-Datei.",
            "Bitte überweise den Betrag vorab auf das auf der Rechnung angegebene Konto.",
            "Sobald die Zahlung eingelangt ist, beginne ich mit der Bearbeitung.",
            ""
        ])
    
    body_parts.extend([
        "Wenn es sich um eine Tierkommunikation oder einen Jenseitskontakt handelt, nehme ich mir dafür bewusst Zeit.",
        "Falls noch Informationen fehlen, melde ich mich persönlich bei dir.",
        "",
        "Von Herzen danke für dein Vertrauen.",
        "",
        "Herzensgruß",
        "Patrick",
        "✨ www.sternenpfade.at"
    ])

    msg = _create_message(customer_email, subject, body_parts)

    # Rechnung anhängen
    if pdf_path and os.path.exists(pdf_path):
        try:
            with open(pdf_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(pdf_path)}")
                msg.attach(part)
        except Exception as e:
            print(f"Anhang-Fehler: {e}")

    # Senden
    success = _send_via_smtp(msg)
    
    # Kopie an dich selbst senden
    if success:
        try:
            admin_msg = _create_message(SMTP_USER, f"[KOPIE] {subject}", body_parts)
            _send_via_smtp(admin_msg)
        except: pass
        
    return success

def send_digital_delivery(order_dict):
    customer_email = str(order_dict.get('customer_email', '')).strip()
    customer_name = str(order_dict.get('customer_name', '')).strip()
    
    items = order_dict.get('items', [])
    download_links = []
    for item in items:
        name = item.get('name', item.get('item_name', ''))
        if name in DIGITAL_PRODUCTS:
            download_links.append((name, DIGITAL_PRODUCTS[name]))

    if not download_links: return False 

    body_parts = [
        f"Hallo {customer_name},", "",
        "vielen Dank für deine Zahlung! Deine Downloads sind nun für dich bereit:",
        ""
    ]
    for name, link in download_links:
        body_parts.append(f"✨ {name}: {link}")
    
    body_parts.extend([
        "",
        "Ich wünsche dir viel Freude und tiefe Erkenntnisse damit.",
        "",
        "Herzensgruß",
        "Patrick",
        "✨ www.sternenpfade.at"
    ])

    msg = _create_message(customer_email, f"Deine Downloads - Sternenpfade (Bestellung {order_dict.get('order_number')})", body_parts)
    return _send_via_smtp(msg)
