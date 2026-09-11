import os

header = """<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Sternenpfade</title>
    <meta name="description" content="{desc}">
    <link rel="stylesheet" href="/css/styles.css">
    <link rel="icon" type="image/png" href="/assets/favicon.png?v=2">
    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
    new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    })(window,document,'script','dataLayer','GTM-KX6NL5LL');</script>
    <!-- End Google Tag Manager -->
</head>
<body>
    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KX6NL5LL"
    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
    
    <div class="cosmic-bg"></div>
    <div class="cosmic-overlay"></div>

    <header>
        <div class="container nav-container">
            <a href="/" class="logo mobile-logo"><img src="/assets/logo-wei.png" alt="Sternenpfade Logo" style="height: 45px;"></a>
            <nav>
                <ul class="nav-links">
                    <li><a href="/">Start</a></li>
                    <li><a href="/tiere">Für Tiere</a></li>
                    <li><a href="/menschen">Für Menschen</a></li>
                    <li><a href="/jenseits">Jenseits</a></li>
                    <li class="logo-item">
                        <a href="/" class="logo">
                            <img src="/assets/logo-wei.png" alt="Sternenpfade Logo" style="height: 60px;">
                        </a>
                    </li>
                    <li><a href="/kreise-kurse" class="active">Ausbildung</a></li>
                    <li><a href="/about">Über mich</a></li>
                    <li><a href="/kontakt">Kontakt</a></li>
                    <li><a href="/buchung" style="color: var(--c-pink); font-weight: 500;">Buchung</a></li>
                </ul>
            </nav>
            <button class="mobile-menu-btn" aria-label="Mobile Navigation öffnen">&#9776;</button>
        </div>
    </header>

    <main id="main-content">
"""

footer = """
    </main>
    <footer>
        <div class="container">
            <div class="footer-grid">
                <div class="footer-col">
                    <a href="/" class="logo" style="margin-bottom: 1rem;"><img src="/assets/logo-wei.png" alt="Sternenpfade Logo" style="height: 55px;"></a>
                    <p style="font-size: 0.9rem;">Modernes Schamanentum & Bewusstseinsarbeit für eine neue Zeit.</p>
                </div>
                <div class="footer-col">
                    <h4>Pfade</h4>
                    <ul>
                        <li><a href="/tiere">Für Tiere</a></li>
                        <li><a href="/menschen">Für Menschen</a></li>
                        <li><a href="/jenseits">Jenseits</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>Angebote</h4>
                    <ul>
                        <li><a href="/kreise-kurse">Ausbildung</a></li>
                        <li><a href="/fallbeispiele">Fallbeispiele</a></li>
                        <li><a href="/buchung">Direkt buchen</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>Rechtliches</h4>
                    <ul>
                        <li><a href="/kontakt">Kontakt</a></li>
                        <li><a href="/impressum">Impressum</a></li>
                        <li><a href="/datenschutz">Datenschutz</a></li>
                        <li><a href="/agb">AGB</a></li>
                        <li><a href="/ki-transparenz">KI-Transparenz</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                &copy; 2026 Sternenpfade. Alle Rechte vorbehalten.
            </div>
        </div>
    </footer>
    <script src="js/main.js"></script>
</body>
</html>
"""

pages = [
    {
        "filename": "ahnenkreis.html",
        "title": "Ahnenkreis 'Wurzeln der Kraft'",
        "desc": "Ahnenkreis und Friedensarbeit mit dem Familienfeld.",
        "img": "/assets/ahnenkreis.jpg",
        "date": "09. Oktober 2026",
        "location": "Praxis in Wolfern (Steyr-Land)",
        "price": "45 €",
        "intro": "Tauche ein in die tiefe Verbindung zu deinen Wurzeln. Dieser Ahnenkreis bietet dir einen geschützten Raum für Friedensarbeit mit dem Familienfeld und zur Heilung alter, vererbter Muster.",
        "pre_reg_link": "/kreise-kurse#voranmeldung"
    },
    {
        "filename": "meditationsabend.html",
        "title": "Meditationsabend Jenseits",
        "desc": "Mediale Verbindung zur geistigen Welt.",
        "img": "/assets/jenseits_meditation.jpg",
        "date": "30. Oktober 2026",
        "location": "Praxis in Wolfern (Steyr-Land)",
        "price": "45 €",
        "intro": "Ein geführter Abend, um in Stille und Achtsamkeit die mediale Verbindung zur geistigen Welt zu spüren und zu üben. Komm zur Ruhe und öffne dich für die Botschaften aus dem Jenseits.",
        "pre_reg_link": "/kreise-kurse#voranmeldung"
    },
    {
        "filename": "krafttier-wochenende.html",
        "title": "Krafttier-Wochenende",
        "desc": "Deine schamanische Reise zum Verbündeten.",
        "img": "/assets/krafttier_wochenende.jpg",
        "date": "17. Oktober 2026",
        "location": "Praxis in Wolfern (Steyr-Land)",
        "price": "120 €",
        "intro": "Ein intensives Wochenende in der Natur, an dem du auf schamanischen Reisen deinem Krafttier begegnest. Lerne, wie du mit deinem geistigen Verbündeten kommunizierst und seine Stärke in den Alltag holst.",
        "pre_reg_link": "/kreise-kurse#voranmeldung"
    }
]

for p in pages:
    content = f"""
    <section class="hero" style="min-height: 40vh; padding-top: 120px; align-items: flex-start; background: url('{p['img']}') center/cover no-repeat; position: relative;">
        <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(18, 11, 30, 0.75);"></div>
        <div class="container hero-content" style="position: relative; z-index: 1;">
            <a href="/kreise-kurse" style="color: var(--c-teal); text-decoration: none; margin-bottom: 1rem; display: inline-block;">&larr; Zurück zur Übersicht</a>
            <h1 style="margin-bottom: 0.5rem;">{p['title']}</h1>
            <span class="hero-subtitle" style="color: var(--c-gold); font-size: 1.1rem;">{p['date']} | {p['location']}</span>
        </div>
    </section>

    <section class="section">
        <div class="container">
            <div class="glass-card" style="max-width: 800px; margin: 0 auto; padding: 3rem;">
                <h2 style="margin-bottom: 1.5rem; color: var(--c-gold);">Über die Veranstaltung</h2>
                <p style="font-size: 1.1rem; line-height: 1.8; color: rgba(255,255,255,0.85); margin-bottom: 2.5rem;">
                    {p['intro']}
                </p>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 3rem; background: rgba(255,255,255,0.03); padding: 1.5rem; border-radius: 12px; border: 1px solid var(--glass-border);">
                    <div>
                        <strong style="color: var(--c-teal); display: block; margin-bottom: 0.3rem;">Datum:</strong>
                        <span>{p['date']}</span>
                    </div>
                    <div>
                        <strong style="color: var(--c-teal); display: block; margin-bottom: 0.3rem;">Ort:</strong>
                        <span>{p['location']}</span>
                    </div>
                    <div>
                        <strong style="color: var(--c-teal); display: block; margin-bottom: 0.3rem;">Energieausgleich:</strong>
                        <span style="font-size: 1.2rem; font-weight: 600; color: var(--c-white);">{p['price']}</span>
                    </div>
                </div>

                <div style="text-align: center;">
                    <a href="{p['pre_reg_link']}" class="btn btn-primary" style="padding: 1rem 2.5rem; font-size: 1.1rem;">Zur Voranmeldung</a>
                </div>
            </div>
        </div>
    </section>
    """
    header_parsed = header.replace("{title}", p['title']).replace("{desc}", p['desc'])
    with open(p['filename'], 'w') as f:
        f.write(header_parsed + content + footer)

print("Pages generated successfully.")
