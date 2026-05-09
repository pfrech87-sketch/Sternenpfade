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

DIGITAL_PRODUCTS = {
    "Gratis Download: Herzens-Verständnis": "https://www.sternenpfade.at/downloads/herzens-verstaendnis.pdf",
    "Gratis Download Herzens-Verstaendnis": "https://www.sternenpfade.at/downloads/herzens-verstaendnis.pdf",
    "Heilreise mit Anubis": "https://www.sternenpfade.at/downloads/anubis-meditation.mp3",
    "Zurueck in deine Mitte": "https://www.sternenpfade.at/downloads/zurueck-in-deine-mitte.mp3"
}

def send_order_confirmation(order_dict, pdf_path):
    customer_email = str(order_dict.get('customer_email', '')).strip()
    customer_name = str(order_dict.get('customer_name', '')).strip()
    
    if not customer_email:
        print("Fehler: Keine Kunden-E-Mail.")
        return False

    if not SMTP_PASSWORD:
        print("Fehler: EMAIL_PASSWORD Umgebungsvariable fehlt.")
        return False

    items = order_dict.get('items', [])
    download_links = []
    is_free_order = order_dict.get('total_amount', 0) == 0
    
    for item in items:
        name = item.get('name', item.get('item_name', ''))
        if name in DIGITAL_PRODUCTS and is_free_order:
            download_links.append((name, DIGITAL_PRODUCTS[name]))

    subject = f"Bestellbestätigung - Sternenpfade (Bestellnummer: {order_dict.get('order_number')})"

    greeting = f"Hallo {customer_name},"
    thanks = "vielen lieben Dank für deine Bestellung bei Sternenpfade 🤍💙✨"
    main_text = "dein gewünschter Download ist nun für dich bereit." if is_free_order else f"deine Bestellung Nr. {order_dict.get('order_number')} ist bei mir eingegangen."

    body_parts = [greeting, "", thanks, main_text, ""]
    if download_links:
        body_parts.append("✨ DEINE DOWNLOADS:")
        for name, link in download_links:
            body_parts.append(f"- {name}: {link}")
        body_parts.append("")

    if not is_free_order:
        body_parts.append("Im Anhang findest du deine Rechnung zur Bestellung als PDF-Datei.")
        body_parts.append("")
        body_parts.append("Bitte überweise den Rechnungsbetrag vorab auf das auf der Rechnung angegebene Konto.")
        body_parts.append("Sobald die Zahlung eingelangt ist, beginne ich mit der Bearbeitung deiner Bestellung.")
        body_parts.append("")
    
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

    text_content = "\n".join(body_parts)
    html_content = "<html><body style='font-family: sans-serif; line-height: 1.5; color: #333;'>" + \
                   "<br/>".join(body_parts).replace("\n", "<br/>") + \
                   "</body></html>"

    msg = MIMEMultipart('alternative')
    msg['From'] = f"{SENDER_NAME} <{SMTP_USER}>"
    msg['To'] = customer_email
    msg['Subject'] = subject

    msg.attach(MIMEText(text_content, 'plain'))
    msg.attach(MIMEText(html_content, 'html'))

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

    # Wir versuchen es nacheinander mit verschiedenen Ports
    ports_to_try = [465, 587]
    
    for port in ports_to_try:
        try:
            print(f"Versuche E-Mail via Webador (Port {port}) an {customer_email} zu senden...")
            if port == 465:
                server = smtplib.SMTP_SSL(SMTP_SERVER, port, timeout=10)
            else:
                server = smtplib.SMTP(SMTP_SERVER, port, timeout=10)
                server.starttls()
            
            # Debug-Level auf 1 setzen, um den kompletten Dialog im Log zu sehen
            server.set_debuglevel(1)
            
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            
            # Admin-Kopie
            admin_msg = MIMEMultipart('alternative')
            admin_msg['From'] = f"{SENDER_NAME} <{SMTP_USER}>"
            admin_msg['To'] = SMTP_USER
            admin_msg['Subject'] = f"[ADMIN-KOPIE] {subject}"
            admin_msg.attach(MIMEText(text_content, 'plain'))
            server.send_message(admin_msg)
            
            server.quit()
            print(f"Versand über SMTP (Port {port}) erfolgreich.")
            return True
        except Exception as e:
            print(f"Fehler auf Port {port}: {e}")
            continue # Nächsten Port probieren
            
    print("Alle SMTP-Versuche sind fehlgeschlagen.")
    return False

def send_digital_delivery(order_dict):
    # Ähnliche Logik wie oben für die spätere digitale Auslieferung
    pass
