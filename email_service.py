import os
import smtplib
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# SMTP Konfiguration für Webador
SMTP_SERVER = "mail.webador.com"
SMTP_USER = "info@sternenpfade.at"
SMTP_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')

SENDER_NAME = "Sternenpfade"

# Mapping der digitalen Produkte
DIGITAL_PRODUCTS = {
    "Gratis Download: Herzens-Verständnis": "https://www.sternenpfade.at/downloads/herzens-verstaendnis.pdf",
    "Gratis Download Herzens-Verstaendnis": "https://www.sternenpfade.at/downloads/herzens-verstaendnis.pdf",
    "Heilreise mit Anubis": "https://www.sternenpfade.at/downloads/anubis-meditation.mp3",
    "Friedensreise mit Anubis": "https://www.sternenpfade.at/downloads/anubis-meditation.mp3",
    "Friedensreise mit Anubis (Meditation)": "https://www.sternenpfade.at/downloads/anubis-meditation.mp3",
    "Zurueck in deine Mitte": "https://www.sternenpfade.at/downloads/zurueck-in-deine-mitte.mp3",
    "Zurueck in deine Kraft": "https://www.sternenpfade.at/downloads/zurueck-in-deine-mitte.mp3",
    "Zurück in deine Kraft": "https://www.sternenpfade.at/downloads/zurueck-in-deine-mitte.mp3",
    "Zurueck in deine Kraft (Meditation)": "https://www.sternenpfade.at/downloads/zurueck-in-deine-mitte.mp3",
    "Zurück in deine Kraft (Meditation)": "https://www.sternenpfade.at/downloads/zurueck-in-deine-mitte.mp3"
}

DIGITAL_PRODUCT_FILES = {
    "Gratis Download: Herzens-Verständnis": "Impulse zur Tierkommunikation.pdf",
    "Gratis Download Herzens-Verstaendnis": "Impulse zur Tierkommunikation.pdf",
    "Friedensreise mit Anubis": "anubis-meditation.mp3",
    "Friedensreise mit Anubis (Meditation)": "anubis-meditation.mp3",
    "Heilreise mit Anubis": "anubis-meditation.mp3",
    "Zurueck in deine Mitte": "zurueck-in-deine-mitte.mp3",
    "Zurueck in deine Kraft": "zurueck-in-deine-mitte.mp3",
    "Zurück in deine Kraft": "zurueck-in-deine-mitte.mp3",
    "Zurueck in deine Kraft (Meditation)": "zurueck-in-deine-mitte.mp3",
    "Zurück in deine Kraft (Meditation)": "zurueck-in-deine-mitte.mp3"
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
    """Hilfsfunktion zum Versenden über STARTTLS (Port 587)"""
    if not SMTP_PASSWORD:
        print("Fehler: EMAIL_PASSWORD nicht gesetzt.")
        return False

    try:
        with smtplib.SMTP(SMTP_SERVER, 587, timeout=15) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            return True
    except Exception as e:
        print(f"Versand über Port 587 fehlgeschlagen: {e}")
        return False

def send_order_confirmation(order_dict, pdf_path):
    customer_email = str(order_dict.get('customer_email', '')).strip()
    customer_name = str(order_dict.get('customer_name', '')).strip()
    
    if not customer_email: return False

    items = order_dict.get('items', [])
    total_amount = order_dict.get('total_amount', 0)
    is_free_order = total_amount == 0
    is_refund = total_amount < 0

    if is_refund:
        subject = f"Gutschrift / Stornorechnung - Sternenpfade (Nr. {order_dict.get('order_number')})"
        body_parts = [
            f"Hallo {customer_name},", "",
            f"anbei findest du deine Gutschrift / Stornorechnung Nr. {order_dict.get('order_number')} als PDF-Datei.",
            "Der Betrag wurde entsprechend erstattet bzw. gutgeschrieben.",
            "",
            "Bei Fragen stehen wir dir jederzeit gerne zur Verfügung.",
            "",
            "Von Herzen danke für dein Vertrauen.",
            "",
            "Herzensgruß",
            "Patrick",
            "✨ www.sternenpfade.at"
        ]
    else:
        subject = f"Bestellbestätigung - Sternenpfade (Nr. {order_dict.get('order_number')})"
        body_parts = [
            f"Hallo {customer_name},", "",
            "vielen lieben Dank für deine Bestellung bei Sternenpfade 🤍💙✨",
            "dein Download ist nun bereit (als Anhang an dieser E-Mail)." if is_free_order else f"deine Bestellung Nr. {order_dict.get('order_number')} ist eingegangen.",
            ""
        ]

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

    # Anhänge definieren
    attachments = []
    if is_free_order:
        downloads_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
        for item in items:
            name = item.get('name', item.get('item_name', ''))
            if name in DIGITAL_PRODUCT_FILES:
                file_path = os.path.join(downloads_dir, DIGITAL_PRODUCT_FILES[name])
                if os.path.exists(file_path):
                    attachments.append(file_path)
    else:
        if pdf_path and os.path.exists(pdf_path):
            attachments.append(pdf_path)

    # Anhänge an die E-Mail anfügen
    for path in attachments:
        try:
            with open(path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(path)}")
                msg.attach(part)
        except Exception as e:
            print(f"Anhang-Fehler für {path}: {e}")

    # Senden
    success = _send_via_smtp(msg)
    
    # Kopie an dich selbst senden
    if success:
        try:
            admin_msg = _create_message(SMTP_USER, f"[KOPIE] {subject}", body_parts)
            # Attach same files to admin copy
            for path in attachments:
                with open(path, "rb") as f:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(path)}")
                    admin_msg.attach(part)
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

def send_contact_form(contact_dict):
    """Versendet eine E-Mail für das Kontaktformular an info@sternenpfade.at und eine Bestätigung an den Absender."""
    name = str(contact_dict.get('name', '')).strip()
    email = str(contact_dict.get('email', '')).strip()
    phone = str(contact_dict.get('phone', '')).strip()
    message = str(contact_dict.get('message', '')).strip()
    
    # 1. E-Mail an dich selbst (Patrick)
    admin_subject = f"Neue Kontaktanfrage über Sternenpfade Website von {name}"
    admin_body = [
        "Hallo Patrick,", "",
        "eine neue Kontaktanfrage wurde über deine Website eingereicht.", "",
        "✨ DETAILS:",
        f"- Name: {name}",
        f"- E-Mail: {email}",
        f"- Telefonnummer: {phone if phone else 'Nicht angegeben'}",
        "",
        "💬 NACHRICHT:",
        message,
        "",
        "---",
        "Diese E-Mail wurde automatisch von deinem Sternenpfade-Backend generiert."
    ]
    
    admin_msg = _create_message(SMTP_USER, admin_subject, admin_body)
    admin_msg['Reply-To'] = email
    
    success = _send_via_smtp(admin_msg)
    
    # 2. Bestätigung an den Absender (Customer)
    if success and email:
        try:
            customer_subject = "Deine Kontaktanfrage bei Sternenpfade"
            customer_body = [
                f"Hallo {name},", "",
                "vielen lieben Dank für deine Nachricht und deine Anfrage bei Sternenpfade! 🤍💙✨", "",
                "Ich habe deine Nachricht erhalten und werde mich in Kürze bei dir melden.", "",
                "💬 DEINE NACHRICHT:",
                message,
                "",
                "Von Herzen danke für dein Vertrauen.",
                "",
                "Herzensgruß",
                "Patrick",
                "✨ www.sternenpfade.at"
            ]
            customer_msg = _create_message(email, customer_subject, customer_body)
            _send_via_smtp(customer_msg)
        except Exception as e:
            print(f"Fehler beim Senden der Bestätigung an den Kunden: {e}")
            
    return success

