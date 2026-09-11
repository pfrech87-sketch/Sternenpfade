import re

files = [
    {
        "name": "ahnenkreis.html",
        "date": "09. Oktober 2026",
        "time": "17:00 Uhr",
        "price": "90 €",
        "intro": "Tauche ein in die tiefe Verbindung zu deinen Wurzeln. Dieser Ahnenkreis bietet dir einen geschützten Raum für Friedensarbeit mit dem Familienfeld und zur Heilung alter, vererbter Muster."
    },
    {
        "name": "meditationsabend.html",
        "date": "30. Oktober 2026",
        "time": "17:00 Uhr",
        "price": "90 €",
        "intro": "Ein geführter Abend, um in Stille und Achtsamkeit die mediale Verbindung zur geistigen Welt zu spüren und zu üben. Komm zur Ruhe und öffne dich für die Botschaften aus dem Jenseits."
    },
    {
        "name": "krafttier-wochenende.html",
        "date": "17. Oktober 2026",
        "time": "Ganzes Wochenende",
        "price": "190 €",
        "intro": "Ein intensives Wochenende in der Natur, an dem du auf schamanischen Reisen deinem Krafttier begegnest. Lerne, wie du mit deinem geistigen Verbündeten kommunizierst und seine Stärke in den Alltag holst."
    }
]

for f_info in files:
    with open(f_info['name'], 'r') as file:
        content = file.read()
    
    # Update Hero subtitle to include time if applicable
    time_str = f" | {f_info['time']}" if f_info['time'] else ""
    # Simple regex to replace the subtitle content in the hero section
    content = re.sub(r'(<span class="hero-subtitle"[^>]*>)[^<]+(</span>)', r'\g<1>' + f"{f_info['date']}{time_str} | Praxis in Wolfern (Steyr-Land)" + r'\g<2>', content)
    
    # Create the new engaging section
    new_section = f"""<section class="section">
        <div class="container">
            <div class="glass-card" style="max-width: 850px; margin: -80px auto 0 auto; padding: 4rem 3rem; position: relative; z-index: 2; border-top: 2px solid var(--c-gold); box-shadow: 0 20px 40px rgba(0,0,0,0.4);">
                
                <div style="text-align: center; margin-bottom: 2.5rem;">
                    <span style="color: var(--c-teal); font-weight: 600; text-transform: uppercase; letter-spacing: 2px; font-size: 0.85rem;">Event Details</span>
                    <h2 style="margin-top: 0.5rem; color: var(--c-white); font-size: 2.2rem;">Über die Veranstaltung</h2>
                </div>
                
                <p style="font-size: 1.15rem; line-height: 1.8; color: rgba(255,255,255,0.9); margin-bottom: 3rem; text-align: center; max-width: 700px; margin-left: auto; margin-right: auto;">
                    {f_info['intro']}
                </p>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 3.5rem;">
                    <div style="background: rgba(255,255,255,0.03); padding: 1.8rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.08); text-align: center; transition: transform 0.3s ease;">
                        <div style="font-size: 2rem; margin-bottom: 0.8rem; color: var(--c-gold);">📅</div>
                        <strong style="color: var(--c-gold); display: block; margin-bottom: 0.3rem; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">Datum & Zeit</strong>
                        <span style="color: var(--c-white); font-weight: 500;">{f_info['date']}<br>{f_info['time']}</span>
                    </div>
                    <div style="background: rgba(255,255,255,0.03); padding: 1.8rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.08); text-align: center; transition: transform 0.3s ease;">
                        <div style="font-size: 2rem; margin-bottom: 0.8rem; color: var(--c-teal);">📍</div>
                        <strong style="color: var(--c-teal); display: block; margin-bottom: 0.3rem; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">Ort</strong>
                        <span style="color: var(--c-white); font-weight: 500;">Praxis in Wolfern<br>(Steyr-Land)</span>
                    </div>
                    <div style="background: rgba(255,255,255,0.03); padding: 1.8rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.08); text-align: center; transition: transform 0.3s ease;">
                        <div style="font-size: 2rem; margin-bottom: 0.8rem; color: var(--c-pink);">💎</div>
                        <strong style="color: var(--c-pink); display: block; margin-bottom: 0.3rem; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">Preis</strong>
                        <span style="font-size: 1.4rem; font-weight: 700; color: var(--c-white);">{f_info['price']}</span>
                    </div>
                </div>

                <div style="text-align: center;">
                    <p style="color: var(--c-hint); margin-bottom: 1.5rem; font-size: 0.95rem;">Die Plätze sind limitiert. Sichere dir jetzt deinen Platz.</p>
                    <a href="/kreise-kurse#voranmeldung" class="btn btn-primary" style="padding: 1.2rem 3rem; font-size: 1.1rem; box-shadow: 0 10px 25px rgba(250, 180, 53, 0.3);">Zur Voranmeldung</a>
                </div>
            </div>
        </div>
    </section>"""
    
    # Replace the old section entirely
    # The old section started with <section class="section"> and ended right before </main>
    # We will use regex to find <section class="section"> and replace everything up to </main>
    
    content = re.sub(r'<section class="section">.*?</section>', new_section, content, flags=re.DOTALL)
    
    with open(f_info['name'], 'w') as file:
        file.write(content)

