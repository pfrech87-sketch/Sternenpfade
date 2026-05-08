import os
import requests
import base64

BREVO_API_KEY = os.environ.get('BREVO_API_KEY', '')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'info@sternenpfade.at')
SENDER_NAME = "Sternenpfade"

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
        return False

    if not BREVO_API_KEY:
        print("BREVO_API_KEY not configured. Skipping email sending.")
        return False

    items = order_dict.get('items', [])
    download_links = []
    is_free_order = order_dict.get('total_amount', 0) == 0
    
    for item in items:
        name = item.get('name', item.get('item_name', ''))
        if name in DIGITAL_PRODUCTS and is_free_order:
            download_links.append((name, DIGITAL_PRODUCTS[name]))

    # Build the body
    greeting = f"Hallo {order_dict.get('customer_name', '')},"
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

    content = "<br/>".join(body_parts).replace("\n", "<br/>")

    # Prepare Attachment
    attachments = []
    if pdf_path and os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            b64_content = base64.b64encode(f.read()).decode()
            attachments.append({
                "content": b64_content,
                "name": os.path.basename(pdf_path)
            })

    # Brevo API Payload
    payload = {
        "sender": {"name": SENDER_NAME, "email": SENDER_EMAIL},
        "to": [{"email": customer_email, "name": order_dict.get('customer_name')}],
        "cc": [{"email": "info@sternenpfade.at", "name": "Sternenpfade Admin"}],
        "subject": f"Bestellbestätigung - Sternenpfade (Bestellnummer: {order_dict.get('order_number')})",
        "htmlContent": f"<html><body>{content}</body></html>",
        "attachment": attachments
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": BREVO_API_KEY,
        "x-sib-api-key": BREVO_API_KEY
    }

    try:
        response = requests.post("https://api.brevo.com/v3/smtp/email", json=payload, headers=headers)
        if response.status_code in [201, 200, 202]:
            print(f"Successfully sent confirmation email via API to {customer_email}")
            return True
        else:
            print(f"Failed to send email via API: {response.text}")
            return False
    except Exception as e:
        print(f"Error sending email via API: {e}")
        return False

def send_digital_delivery(order_dict):
    # Similar implementation for digital delivery via API if needed
    pass
