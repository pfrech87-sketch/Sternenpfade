import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import cm

DATA_DIR = os.environ.get('DATA_DIR', os.path.dirname(os.path.abspath(__file__)))
INVOICE_DIR = os.path.join(DATA_DIR, 'invoices')
if not os.path.exists(INVOICE_DIR):
    os.makedirs(INVOICE_DIR)

def generate_invoice(order):
    """
    Generate a PDF invoice for the given order dictionary.
    Expected order format:
    {
        'id': 1,
        'order_number': '137',
        'customer_name': 'Johann Becker',
        'customer_email': 'patrick.frech@hotmail.com',
        'customer_phone': '+436508038987',
        'billing_address': 'Rechnungsstraße 1\n4493 Wolfern\nÖsterreich',
        'created_at': '20.04.2026',
        'total_amount': 90.00,
        'payment_method': 'Überweisung, Vorkasse',
        'notes': 'Kommentare...',
        'items': [
            {'name': 'Schamanische Tierkommunikation', 'quantity': 1, 'price': 90.00}
        ]
    }
    """
    filename = f"Rechnung_{order['order_number']}.pdf"
    filepath = os.path.join(INVOICE_DIR, filename)
    
    doc = SimpleDocTemplate(filepath, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(name='TitleStyle', parent=styles['Heading1'], fontSize=20, spaceAfter=20)
    bold_style = ParagraphStyle(name='BoldStyle', parent=styles['Normal'], fontName='Helvetica-Bold')
    right_align_style = ParagraphStyle(name='RightAlign', parent=styles['Normal'], alignment=2)
    right_align_bold = ParagraphStyle(name='RightAlignBold', parent=styles['Normal'], alignment=2, fontName='Helvetica-Bold')
    
    # Header Table (Rechnung Title & Logo)
    # Using a placeholder for logo, you can change the path to your actual logo
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'pfad_jenseits_img_1776710470972.png')
    
    header_data = []
    if os.path.exists(logo_path):
        img = Image(logo_path, width=3*cm, height=3*cm)
        header_data.append([Paragraph("<b>Rechnung</b>", title_style), img])
    else:
        header_data.append([Paragraph("<b>Rechnung</b>", title_style), ""])
        
    header_table = Table(header_data, colWidths=[12*cm, 5*cm])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 1*cm))
    
    # Addresses Table
    sender_text = """
    <b>Sternenpfade | Patrick Frech</b><br/>
    Dr. Derflerstraße 3/2<br/>
    4493 Wolfern<br/>
    Österreich<br/>
    info@sternenpfade.at
    """
    
    billing_text = f"<b>{order['customer_name']}</b><br/>{order['billing_address'].replace(chr(10), '<br/>')}<br/><br/>{order['customer_email']}<br/>{order.get('customer_phone', '')}"
    
    addr_data = [
        [Paragraph(billing_text, styles['Normal']), Paragraph(sender_text, right_align_style)]
    ]
    addr_table = Table(addr_data, colWidths=[8.5*cm, 8.5*cm])
    addr_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(addr_table)
    elements.append(Spacer(1, 1*cm))
    
    # Date & Invoice Number
    date_formatted = order['created_at'].split(' ')[0] if ' ' in order['created_at'] else order['created_at']
    meta_data = [
        [Paragraph("<b>Datum</b>", styles['Normal']), Paragraph("<b>Rechnungsnummer</b>", right_align_bold)],
        [Paragraph(date_formatted, styles['Normal']), Paragraph(str(order['order_number']), right_align_style)]
    ]
    meta_table = Table(meta_data, colWidths=[8.5*cm, 8.5*cm])
    meta_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 1*cm))
    
    # Items Table
    item_data = [
        [Paragraph("<b>Artikel</b>", styles['Normal']), Paragraph("<b>Menge</b>", styles['Normal']), Paragraph("<b>Pro Artikel</b>", styles['Normal']), Paragraph("<b>Preis</b>", styles['Normal'])]
    ]
    
    for item in order['items']:
        price_str = f"€ {item['price']:.2f}".replace('.', ',')
        total_price_str = f"€ {(item['price'] * item['quantity']):.2f}".replace('.', ',')
        item_data.append([
            Paragraph(item['name'], styles['Normal']),
            str(item['quantity']),
            price_str,
            total_price_str
        ])
        
    items_table = Table(item_data, colWidths=[8*cm, 3*cm, 3*cm, 3*cm])
    items_table.setStyle(TableStyle([
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(items_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # Total
    total_str = f"€ {order['total_amount']:.2f}".replace('.', ',')
    total_data = [
        ["", Paragraph("<b>Gesamtbetrag</b>", ParagraphStyle('total_label', parent=styles['Normal'], fontSize=12, alignment=2, fontName='Helvetica-Bold')), Paragraph(f"<b>{total_str}</b>", ParagraphStyle('total_val', parent=styles['Normal'], fontSize=12, alignment=2, fontName='Helvetica-Bold'))]
    ]
    total_table = Table(total_data, colWidths=[8*cm, 4*cm, 5*cm])
    total_table.setStyle(TableStyle([
        ('ALIGN', (1, 0), (2, 0), 'RIGHT'),
    ]))
    elements.append(total_table)
    elements.append(Spacer(1, 2*cm))
    
    # Payment Method & Comments
    footer_data = [
        [Paragraph("<b>Zahlungsmethode</b>", styles['Normal']), Paragraph("<b>Kommentare</b>", styles['Normal'])],
        [Paragraph(order.get('payment_method', 'Überweisung, Vorkasse'), styles['Normal']), Paragraph(order.get('notes', ''), styles['Normal'])]
    ]
    footer_table = Table(footer_data, colWidths=[8.5*cm, 8.5*cm])
    footer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(footer_table)
    
    # Build PDF
    doc.build(elements)
    return filepath

if __name__ == '__main__':
    # Test Generation
    test_order = {
        'id': 1,
        'order_number': '137',
        'customer_name': 'Johann Becker',
        'customer_email': 'patrick.frech@hotmail.com',
        'customer_phone': '+436508038987',
        'billing_address': 'Rechnungsstraße 1\n4493 Wolfern\nÖsterreich',
        'created_at': '20.04.2026',
        'total_amount': 90.00,
        'payment_method': 'Überweisung, Vorkasse',
        'notes': 'Gero',
        'items': [
            {'name': 'Schamanische Tierkommunikation', 'quantity': 1, 'price': 90.00}
        ]
    }
    path = generate_invoice(test_order)
    print(f"Generated test invoice at: {path}")
