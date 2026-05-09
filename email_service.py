import os
import smtplib
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# SMTP Konfiguration für Webador
SMTP_SERVER = "smtp.webador.com"
SMTP_PORT = 465 # SSL Port
SMTP_USER = "info@sternenpfade.at"
# Das Passwort wird sicher aus den Umgebungsvariablen geladen
SMTP_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')

SENDER_NAME = "Sternenpfade"

# Mapping der digitalen Produkte zu ihren Download-Links
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
        print("Fehler: Keine Kunden-E-Mail-Adresse vorhanden.")
        return False

    if not SMTP_PASSWORD:
        print("Fehler: EMAIL_PASSWORD ist nicht konfiguriert (Umgebungsvariable fehlt).")
        return False

    items = order_dict.get('items', [])
    download_links = []
    is_free_order = order_dict.get('total_amount', 0) == 0
    
    for item in items:
        name = item.get('name', item.get('item_name', ''))
        if name in DIGITAL_PRODUCTS and is_free_order:
            download_links.append((name, DIGITAL_PRODUCTS[name]))

    # Betreff erstellen
    subject = f"Bestellbestätigung - Sternenpfade (Bestellnummer: {order_dict.get('order_number')})"

    # Nachrichtenteile bauen
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

    # E-Mail Objekt erstellen
    msg = MIMEMultipart('alternative')
    msg['From'] = f"{SENDER_NAME} <{SMTP_USER}>"
    msg['To'] = customer_email
    msg['Subject'] = subject

    # Text und HTML hinzufügen
    msg.attach(MIMEText(text_content, 'plain'))
    msg.attach(MIMEText(html_content, 'html'))

    # PDF Anhang hinzufügen
    if pdf_path and os.path.exists(pdf_path):
        try:
            with open(pdf_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={os.path.basename(pdf_path)}",
                )
                msg.attach(part)
        except Exception as e:
            print(f"Fehler beim Anhängen der PDF: {e}")

    # E-Mail über SMTP senden
    try:
        print(f"Versuche E-Mail via Webador-SMTP an {customer_email} zu senden...")
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            
            # Kopie an den Admin senden (einfach noch einmal senden oder BCC nutzen)
            # Hier senden wir eine Kopie an info@sternenpfade.at
            msg['To'] = SMTP_USER
            msg['Subject'] = f"[KOPIE] {subject}"
            server.send_message(msg)
            
        print(f"E-Mail erfolgreich gesendet an {customer_email} und Kopie an Admin.")
        return True
    except Exception as e:
        print(f"SMTP Fehler: {e}")
        return False

def send_digital_delivery(order_dict):
    customer_email = str(order_dict.get('customer_email', '')).strip()
    customer_name = str(order_dict.get('customer_name', '')).strip()
    
    if not customer_email or not SMTP_PASSWORD:
        return False

    items = order_dict.get('items', [])
    download_links = []
    
    for item in items:
        name = item.get('name', item.get('item_name', ''))
        if name in DIGITAL_PRODUCTS:
            download_links.append((name, DIGITAL_PRODUCTS[name]))

    if not download_links:
        return False 

    greeting = f"Hallo {customer_name},"
    body_parts = [
        greeting, "",
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

    text_content = "\n".join(body_parts)
    html_content = "<html><body style='font-family: sans-serif; line-height: 1.5; color: #333;'>" + \
                   "<br/>".join(body_parts).replace("\n", "<br/>") + \
                   "</body></html>"

    msg = MIMEMultipart('alternative')
    msg['From'] = f"{SENDER_NAME} <{SMTP_USER}>"
    msg['To'] = customer_email
    msg['Subject'] = f"Deine Downloads von Sternenpfade - Bestellung {order_dict.get('order_number')}"

    msg.attach(MIMEText(text_content, 'plain'))
    msg.attach(MIMEText(html_content, 'html'))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Fehler bei digitaler Auslieferung: {e}")
        return False
