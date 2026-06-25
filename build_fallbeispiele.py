import os
import json
import xml.etree.ElementTree as ET
from datetime import datetime

# Path definitions
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(ROOT_DIR, 'data', 'fallbeispiele.json')
OUTPUT_DIR = os.path.join(ROOT_DIR, 'fallbeispiele')
SITEMAP_FILE = os.path.join(ROOT_DIR, 'sitemap.xml')

# Ensure directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Common HTML Head elements
HTML_HEAD_TEMPLATE = """    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Sternenpfade</title>
    <meta name="description" content="{description}">
    <link rel="stylesheet" href="/css/styles.css">
    <link rel="icon" type="image/png" href="/assets/favicon.png?v=2">
    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
    new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    }})(window,document,'script','dataLayer','GTM-KX6NL5LL');</script>
    <!-- End Google Tag Manager -->

    <!-- Open Graph Tags für Social Media & KI Previews -->
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="{og_image}">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:type" content="website">
    <link rel="canonical" href="{canonical_url}">
"""

# Common Header template (Universal Navigation with Absolute Paths)
HEADER_TEMPLATE = """    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KX6NL5LL"
    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
    <!-- End Google Tag Manager (noscript) -->
    <div class="cosmic-bg"></div>
    <div class="cosmic-overlay"></div>

    <header>
        <div class="container nav-container">
            <!-- Mobile Logo -->
            <a href="/index.html" class="logo mobile-logo"><img src="/assets/logo-wei.png" alt="Sternenpfade Logo" style="height: 45px;"></a>
            
            <nav>
                <ul class="nav-links">
                    <li><a href="/index.html">Start</a></li>
                    <li><a href="/tiere.html">Für Tiere</a></li>
                    <li><a href="/menschen.html">Für Menschen</a></li>
                    <li><a href="/jenseits.html">Jenseits</a></li>
                    
                    <li class="logo-item">
                        <a href="/index.html" class="logo">
                            <img src="/assets/logo-wei.png" alt="Sternenpfade Logo" style="height: 60px;">
                        </a>
                    </li>

                    <li><a href="/kreise-kurse.html">Kreise & Kurse</a></li>
                    <li><a href="/about.html">Über mich</a></li>
                    <li><a href="/kontakt.html">Kontakt</a></li>
                    <li><a href="/buchung" style="color: var(--c-pink); font-weight: 500;">Buchung</a></li>
                </ul>
            </nav>
            <button class="mobile-menu-btn" aria-label="Mobile Navigation öffnen">&#9776;</button>
        </div>
    </header>
"""

# Common Footer template (Universal Footer with Absolute Paths)
FOOTER_TEMPLATE = """    <footer>
        <div class="container">
            <div class="footer-grid">
                <div class="footer-col">
                    <a href="/index.html" class="logo" style="margin-bottom: 1rem;"><img src="/assets/logo-wei.png" alt="Sternenpfade Logo" style="height: 55px;"></a>
                    <p style="font-size: 0.9rem;">Modernes Schamanentum & Bewusstseinsarbeit für eine neue Zeit.</p>
                </div>
                 <div class="footer-col">
                    <h4>Pfade</h4>
                    <ul>
                        <li><a href="/tiere.html">Für Tiere</a></li>
                        <li><a href="/menschen.html">Für Menschen</a></li>
                        <li><a href="/jenseits.html">Jenseits</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>Angebote</h4>
                    <ul>
                        <li><a href="/kreise-kurse.html">Kreise & Kurse</a></li>
                        <li><a href="/fallbeispiele">Fallbeispiele</a></li>
                        <li><a href="/buchung">Direkt buchen</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>Rechtliches</h4>
                    <ul>
                        <li><a href="/kontakt.html">Kontakt</a></li>
                        <li><a href="/impressum.html">Impressum</a></li>
                        <li><a href="#">Datenschutz</a></li>
                        <li><a href="/agb.html">AGB</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>Social Media</h4>
                    <div style="display: flex; gap: 1rem; margin-top: 0.5rem;">
                        <a href="https://www.instagram.com/deinesternenpfade/" target="_blank" title="Instagram" style="color: rgba(255,255,255,0.7); transition: color 0.3s ease;" onmouseover="this.style.color='var(--c-white)'" onmouseout="this.style.color='rgba(255,255,255,0.7)'">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>
                        </a>
                        <a href="https://www.tiktok.com/@sternenpfade" target="_blank" title="TikTok" style="color: rgba(255,255,255,0.7); transition: color 0.3s ease;" onmouseover="this.style.color='var(--c-white)'" onmouseout="this.style.color='rgba(255,255,255,0.7)'">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z" /></svg>
                        </a>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                &copy; 2026 Sternenpfade. Alle Rechte vorbehalten.
            </div>
        </div>
    </footer>
    <script src="/js/main.js"></script>
"""

def slugify(text):
    return text.lower().replace(" ", "-").replace("&", "und").replace("ö", "oe").replace("ä", "ae").replace("ü", "ue").replace("ß", "ss")

def build_overview_page(cases):
    """Builds the main /fallbeispiele overview HTML page."""
    
    # Render case cards
    cards_html = ""
    for case in cases:
        # Create categories for filtering
        animal_cat = case['animalType'].lower().replace(" ", "-")
        topic_cats = ",".join([slugify(t) for t in case['topics']])
        status_cat = case['status'].lower().replace(" ", "-")
        
        tags_html = "".join([f'<span class="tag-badge">{topic}</span>' for topic in case['topics'][:3]])
        
        cards_html += f"""
                <div class="glass-card case-card" data-animal="{animal_cat}" data-topics="{topic_cats}" data-status="{status_cat}">
                    <div class="case-card-img-container">
                        <img src="{case['heroImage']['src']}" alt="{case['heroImage']['alt']}">
                    </div>
                    <div class="case-card-content">
                        <span class="case-card-meta">{case['animalType']} &bull; {case['country']}</span>
                        <h3 class="case-card-title">{case['title']}</h3>
                        <p class="case-card-essence">»{case['essence']}«</p>
                        <p class="case-card-summary">{case['shortSummary']}</p>
                        <div class="case-card-tags">
                            {tags_html}
                        </div>
                        <a href="/fallbeispiele/{case['slug']}" class="btn btn-secondary card-cta" style="margin-top: 1.5rem; display: block; font-size: 0.8rem; padding: 0.6rem 1.5rem;">Fallbeispiel lesen ➔</a>
                    </div>
                </div>
        """

    # Combine layout
    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
{HTML_HEAD_TEMPLATE.format(
    title="Fallbeispiele aus der Tierkommunikation & Jenseitskontakte",
    description="Entdecke echte Fallbeispiele über schamanische Tierkommunikation, energetische Tierbegleitung und Jenseitskontakte aus Österreich und der Schweiz.",
    og_image="https://www.sternenpfade.at/assets/social-share.png",
    canonical_url="https://www.sternenpfade.at/fallbeispiele"
)}
    <style>
        .filter-section {{
            margin-bottom: 3rem;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
            background: rgba(255, 255, 255, 0.02);
            padding: 2rem;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
        }}
        .filter-group {{
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 0.8rem;
        }}
        .filter-label {{
            font-size: 0.95rem;
            font-weight: 500;
            color: var(--c-gold);
            min-width: 100px;
        }}
        .filter-chips {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }}
        .filter-chip {{
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--c-white);
            padding: 0.4rem 1rem;
            border-radius: 50px;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        .filter-chip:hover {{
            background: rgba(255, 255, 255, 0.1);
            border-color: var(--c-gold);
        }}
        .filter-chip.active {{
            background: var(--c-teal);
            border-color: var(--c-teal);
            box-shadow: 0 0 10px rgba(1, 99, 149, 0.5);
            font-weight: 500;
        }}
        .case-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 2rem;
        }}
        .case-card {{
            padding: 0 !important;
            overflow: hidden;
            border-color: rgba(255, 255, 255, 0.05);
            transition: all 0.3s ease;
        }}
        .case-card-img-container {{
            width: 100%;
            height: 220px;
            overflow: hidden;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }}
        .case-card-img-container img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.5s ease;
        }}
        .case-card:hover .case-card-img-container img {{
            transform: scale(1.05);
        }}
        .case-card-content {{
            padding: 2rem;
        }}
        .case-card-meta {{
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--c-teal);
            margin-bottom: 0.5rem;
            display: block;
        }}
        .case-card-title {{
            font-size: 1.4rem;
            color: var(--c-white);
            margin-bottom: 1rem;
            line-height: 1.3;
        }}
        .case-card-essence {{
            font-style: italic;
            color: var(--c-gold);
            font-size: 0.95rem;
            margin-bottom: 1rem;
        }}
        .case-card-summary {{
            font-size: 0.95rem;
            color: rgba(255, 255, 255, 0.7);
            margin-bottom: 1.5rem;
        }}
        .case-card-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }}
        .tag-badge {{
            font-size: 0.75rem;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            color: rgba(255, 255, 255, 0.6);
        }}
        .card-cta:hover {{
            background: var(--c-teal) !important;
            border-color: var(--c-teal) !important;
            color: var(--c-white) !important;
            box-shadow: 0 0 15px rgba(1, 99, 149, 0.4);
        }}
    </style>
</head>
<body>
{HEADER_TEMPLATE}

    <main id="main-content" class="theme-tiere">
        <!-- Hero Section -->
        <section class="hero" style="min-height: 45vh; padding-top: 130px; align-items: flex-start;">
            <div class="container hero-content">
                <span class="hero-subtitle">Erfahrungen aus der Praxis</span>
                <h1>Fallbeispiele &amp; Tiergespräche</h1>
                <p style="max-width: 800px;">
                    Jedes Tier hat seine eigene Geschichte und Seelenschwingung. In diesen anonymisierten Fallbeispielen gebe ich dir einen Einblick in meine Arbeit als Tierkommunikator und zeige dir, was sich auf emotionaler und schamanisch-energetischer Ebene bewegen darf.
                </p>
            </div>
        </section>

        <!-- Filters & Cases Section -->
        <section class="section" style="padding-top: 1rem;">
            <div class="container">
                
                <!-- Filter Chips -->
                <div class="filter-section">
                    <!-- Tierart -->
                    <div class="filter-group">
                        <span class="filter-label">Tierart:</span>
                        <div class="filter-chips" id="filter-animal">
                            <button class="filter-chip active" data-filter="all">Alle</button>
                            <button class="filter-chip" data-filter="hund">Hund</button>
                            <button class="filter-chip" data-filter="katze">Katze</button>
                            <button class="filter-chip" data-filter="pferd">Pferd</button>
                        </div>
                    </div>
                    <!-- Thema -->
                    <div class="filter-group">
                        <span class="filter-label">Thema:</span>
                        <div class="filter-chips" id="filter-topic">
                            <button class="filter-chip active" data-filter="all">Alle</button>
                            <button class="filter-chip" data-filter="tierkommunikation">Tierkommunikation</button>
                            <button class="filter-chip" data-filter="jenseitskontakt">Jenseitskontakt</button>
                            <button class="filter-chip" data-filter="verhaltensauffaelligkeiten">Verhaltensauffälligkeiten</button>
                            <button class="filter-chip" data-filter="energetische-begleitung">Energetische Begleitung</button>
                            <button class="filter-chip" data-filter="tierschutzhund">Tierschutz</button>
                        </div>
                    </div>
                    <!-- Status -->
                    <div class="filter-group">
                        <span class="filter-label">Status:</span>
                        <div class="filter-chips" id="filter-status">
                            <button class="filter-chip active" data-filter="all">Alle</button>
                            <button class="filter-chip" data-filter="lebendes-tier">Lebendes Tier</button>
                            <button class="filter-chip" data-filter="verstorbene-tierseele">Verstorbene Tierseele</button>
                        </div>
                    </div>
                </div>

                <!-- Case Studies Cards Grid -->
                <div class="case-grid" id="cases-container">
                    {cards_html}
                </div>

                <!-- Explanatory Block (Kunden Orientierung) -->
                <div class="glass-card" style="margin-top: 5rem; border-color: rgba(1,99,149,0.2); max-width: 900px; margin-left: auto; margin-right: auto;">
                    <h2 style="color: var(--c-teal); text-align: center; margin-bottom: 2rem;">Warum teile ich diese Fallbeispiele?</h2>
                    <p style="margin-bottom: 1.5rem;">
                        Viele Tierhalter kommen mit konkreten Sorgen zu mir: Der Hund büxt aus, die Katze zieht sich zurück oder das Pferd zeigt Blockaden. Oftmals stehen dahinter jedoch seelische Themen oder energetische Spannungen, die sich über die rein körperliche Ebene hinaus erstrecken.
                    </p>
                    <p style="margin-bottom: 1.5rem;">
                        Diese Fallstudien sollen dir helfen zu verstehen, dass Tierkommunikation weitaus mehr ist als das Stellen einfacher Fragen und Empfangen von Antworten. Sie ermöglicht es, das energetische Feld zwischen Tier und Mensch zu beleuchten, die Verbindung zu vertiefen und das Tier auf seelischer Ebene energetisch zu begleiten.
                    </p>
                    <p style="margin-bottom: 0; font-style: italic; color: var(--c-hint); font-size: 0.95rem; text-align: center;">
                        Hinweis: Zum Schutz der Privatsphäre sind alle Fallbeispiele anonymisiert. Tiernamen wurden teilweise geändert und personenbezogene Daten verfremdet.
                    </p>
                </div>

            </div>
        </section>

        <!-- CTA Section -->
        <section class="section" style="background: rgba(18, 11, 30, 0.4);">
            <div class="container" style="text-align: center; max-width: 800px;">
                <h2 style="color: var(--c-white); margin-bottom: 1.5rem;">Möchtest du wissen, was dein Tier dir zeigen möchte?</h2>
                <p style="margin-bottom: 2.5rem; font-size: 1.15rem; color: rgba(255, 255, 255, 0.8);">
                    Jedes Tier trägt eine eigene, tiefe Botschaft für seinen Menschen. Gerne begleite ich auch dich und deinen tierischen Wegbegleiter schamanisch und helfe dir, eure Seelenverbindung deutlicher wahrzunehmen.
                </p>
                <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
                    <a href="/buchung" class="btn btn-primary" style="background: var(--c-teal); border: none;">Tierkommunikation buchen</a>
                    <a href="/dienstleistungen/tierkommunikation" class="btn btn-secondary">Mehr über Tierkommunikation erfahren</a>
                </div>
            </div>
        </section>
    </main>

{FOOTER_TEMPLATE}

    <script>
        // Client-Side Filter Script
        document.addEventListener('DOMContentLoaded', () => {{
            const filterChips = document.querySelectorAll('.filter-chip');
            const cards = document.querySelectorAll('.case-card');
            
            // Filters state
            const activeFilters = {{
                animal: 'all',
                topic: 'all',
                status: 'all'
            }};

            filterChips.forEach(chip => {{
                chip.addEventListener('click', () => {{
                    const group = chip.parentElement.id.replace('filter-', '');
                    const filterValue = chip.getAttribute('data-filter');
                    
                    // Toggle active class in the current group
                    chip.parentElement.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
                    chip.classList.add('active');
                    
                    // Update active filters
                    activeFilters[group] = filterValue;
                    
                    // Apply filtering
                    applyFilters();
                }});
            }});

            function applyFilters() {{
                cards.forEach(card => {{
                    const animal = card.getAttribute('data-animal');
                    const topics = card.getAttribute('data-topics').split(',');
                    const status = card.getAttribute('data-status');
                    
                    const matchAnimal = activeFilters.animal === 'all' || animal === activeFilters.animal;
                    const matchTopic = activeFilters.topic === 'all' || topics.includes(activeFilters.topic);
                    const matchStatus = activeFilters.status === 'all' || status === activeFilters.status;
                    
                    if (matchAnimal && matchTopic && matchStatus) {{
                        card.style.display = 'flex';
                        // Trigger fade in animation
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0)';
                    }} else {{
                        card.style.opacity = '0';
                        card.style.transform = 'translateY(15px)';
                        setTimeout(() => {{
                            if (card.style.opacity === '0') {{
                                card.style.display = 'none';
                            }}
                        }}, 200);
                    }}
                }});
            }}
        }});
    </script>
</body>
</html>
"""
    return html

def build_detail_page(case, all_cases):
    """Builds an individual case study detail HTML page."""
    
    # 1. Breadcrumbs
    breadcrumbs = f"""
            <nav class="breadcrumbs" style="margin-bottom: 2rem; font-size: 0.9rem; color: var(--c-hint);">
                <a href="/index.html" style="color: var(--c-hint);">Start</a> / 
                <a href="/fallbeispiele" style="color: var(--c-hint);">Fallbeispiele</a> / 
                <span style="color: var(--c-white); font-weight: 500;">{case['animalName']}</span>
            </nav>
    """

    # 2. Table of Contents
    toc_items = ""
    for idx, sec in enumerate(case['sections'], 1):
        toc_items += f'<li><a href="#section-{idx}">{sec["headline"]}</a></li>'
    
    toc_html = f"""
                    <div class="glass-card toc-card" style="margin-bottom: 2rem; border-color: rgba(1,99,149,0.15);">
                        <h4 style="color: var(--c-teal); margin-bottom: 1rem; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 1px;">Inhaltsverzeichnis</h4>
                        <ol style="padding-left: 1.2rem; display: flex; flex-direction: column; gap: 0.6rem; font-size: 0.95rem;">
                            {toc_items}
                        </ol>
                    </div>
    """

    # 3. Facts Box
    facts_rows = ""
    for label, val in case['facts'].items():
        facts_rows += f"""
                            <div class="fact-row">
                                <span class="fact-label">{label}:</span>
                                <span class="fact-value">{val}</span>
                            </div>
        """
        
    facts_box_html = f"""
                    <div class="glass-card facts-card" style="border-color: rgba(1,99,149,0.3); background: rgba(1,99,149,0.05); margin-bottom: 2rem;">
                        <h3 style="color: var(--c-teal); margin-bottom: 1.5rem; font-size: 1.4rem;">Fakten zum Fall</h3>
                        <div class="facts-list">
                            {facts_rows}
                        </div>
                    </div>
    """

    # 4. Content Sections
    sections_html = ""
    for idx, sec in enumerate(case['sections'], 1):
        sections_html += f"""
                <section id="section-{idx}" class="story-section" style="margin-bottom: 3.5rem;">
                    <h2 class="story-headline" style="color: var(--c-teal); font-size: 1.8rem; margin-bottom: 1.2rem; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 0.5rem;">{idx}. {sec['headline']}</h2>
                    <div class="story-body" style="font-size: 1.05rem; font-weight: 300; line-height: 1.7; color: rgba(255,255,255,0.85);">
                        {sec['body']}
                    </div>
                </section>
        """

    # 5. FAQ Accordion
    faq_items = ""
    for item in case['faqs']:
        faq_items += f"""
                    <div class="faq-item">
                        <button class="faq-question">{item['question']} <span class="icon">+</span></button>
                        <div class="faq-answer"><p>{item['answer']}</p></div>
                    </div>
        """

    faq_section_html = f"""
        <section class="section" style="padding-top: 2rem; background: rgba(18, 11, 30, 0.3); border-radius: 24px; margin-top: 4rem;">
            <div class="container" style="max-width: 800px;">
                <h2 style="text-align: center; color: var(--c-white); margin-bottom: 2.5rem;">Häufige Fragen zu diesem Fall</h2>
                <div class="faq-container">
                    {faq_items}
                </div>
            </div>
        </section>
    """

    # 6. JSON-LD Schemas (FAQ & Article combined)
    faq_schema_items = []
    for item in case['faqs']:
        faq_schema_items.append({
            "@type": "Question",
            "name": item['question'],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": item['answer']
            }
        })
        
    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "@id": f"https://www.sternenpfade.at/fallbeispiele/{case['slug']}#article",
                "headline": case['title'],
                "description": case['metaDescription'],
                "image": f"https://www.sternenpfade.at{case['heroImage']['src']}",
                "datePublished": datetime.now().strftime("%Y-%m-%d"),
                "author": {
                    "@type": "Person",
                    "name": "Patrick Frech, MA",
                    "jobTitle": "Schamane & Tierkommunikator",
                    "url": "https://www.sternenpfade.at"
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "Sternenpfade",
                    "logo": {
                        "@type": "ImageObject",
                        "url": "https://www.sternenpfade.at/assets/logo-wei.png"
                    }
                },
                "about": case['topics'],
                "mainEntityOfPage": {
                    "@type": "WebPage",
                    "@id": f"https://www.sternenpfade.at/fallbeispiele/{case['slug']}"
                }
            },
            {
                "@type": "FAQPage",
                "@id": f"https://www.sternenpfade.at/fallbeispiele/{case['slug']}#faq",
                "mainEntity": faq_schema_items
            }
        ]
    }
    json_ld_string = json.dumps(json_ld, ensure_ascii=False, indent=2)

    # 7. Related cases (link other case studies dynamically)
    related = [c for c in all_cases if c['slug'] != case['slug']][:2]
    
    related_cards_html = ""
    for r in related:
        related_cards_html += f"""
                    <div class="glass-card" style="border-color: rgba(1,99,149,0.2); display: flex; flex-direction: column;">
                        <span style="font-size: 2.5rem; margin-bottom: 1rem; display: block;">🐾</span>
                        <h3 style="color: var(--c-teal); font-size: 1.4rem; margin-bottom: 0.5rem;">{r['title']}</h3>
                        <p style="font-size: 0.95rem; margin-bottom: 1.5rem; font-style: italic; color: var(--c-gold);">»{r['essence']}«</p>
                        <p style="font-size: 0.95rem; margin-bottom: 1.5rem; color: rgba(255,255,255,0.7);">{r['shortSummary']}</p>
                        <a href="/fallbeispiele/{r['slug']}" class="btn btn-secondary" style="font-size: 0.8rem; padding: 0.6rem 1.5rem; margin-top: auto; display: inline-block; width: fit-content;">Fallbeispiel lesen ➔</a>
                    </div>
        """
        
    # If fewer than 2 related cases, pad with core services
    if len(related) < 2:
        if len(related) == 0:
            related_cards_html += """
                    <div class="glass-card" style="border-color: rgba(1,99,149,0.2); display: flex; flex-direction: column;">
                        <span style="font-size: 2.5rem; margin-bottom: 1rem; display: block;">💬</span>
                        <h3 style="color: var(--c-teal); font-size: 1.4rem; margin-bottom: 0.5rem;">Schamanische Tierkommunikation</h3>
                        <p style="font-size: 0.95rem; margin-bottom: 1.5rem; color: rgba(255,255,255,0.7);">Erfahre, was dein Tier fühlt, spürt und welche Botschaften es für dich bereit hält. Patrick verbindet sich energetisch und liefert dir eine detaillierte Auswertung.</p>
                        <a href="/dienstleistungen/tierkommunikation" class="btn btn-secondary" style="font-size: 0.8rem; padding: 0.6rem 1.5rem; margin-top: auto; display: inline-block; width: fit-content;">Details ansehen</a>
                    </div>
                    <div class="glass-card" style="border-color: rgba(250,180,53,0.2); display: flex; flex-direction: column;">
                        <span style="font-size: 2.5rem; margin-bottom: 1rem; display: block;">🌈</span>
                        <h3 style="color: var(--c-gold); font-size: 1.4rem;">Jenseitskontakt für Tiere</h3>
                        <p style="font-size: 0.95rem; margin-bottom: 1.5rem; color: rgba(255,255,255,0.7);">Begleitung über die Regenbogenbrücke hinaus. Ein liebevolles und klärendes Gespräch mit der vorausgegangenen Seele deines treuen Begleiters.</p>
                        <a href="/dienstleistungen/jenseits-der-regenbogenbruecke" class="btn btn-secondary" style="font-size: 0.8rem; padding: 0.6rem 1.5rem; margin-top: auto; display: inline-block; width: fit-content;">Details ansehen</a>
                    </div>
            """
        elif len(related) == 1:
            related_cards_html += """
                    <div class="glass-card" style="border-color: rgba(1,99,149,0.2); display: flex; flex-direction: column;">
                        <span style="font-size: 2.5rem; margin-bottom: 1rem; display: block;">💬</span>
                        <h3 style="color: var(--c-teal); font-size: 1.4rem; margin-bottom: 0.5rem;">Schamanische Tierkommunikation</h3>
                        <p style="font-size: 0.95rem; margin-bottom: 1.5rem; color: rgba(255,255,255,0.7);">Erfahre, was dein Tier fühlt, spürt und welche Botschaften es für dich bereit hält. Patrick verbindet sich energetisch und liefert dir eine detaillierte Auswertung.</p>
                        <a href="/dienstleistungen/tierkommunikation" class="btn btn-secondary" style="font-size: 0.8rem; padding: 0.6rem 1.5rem; margin-top: auto; display: inline-block; width: fit-content;">Details ansehen</a>
                    </div>
            """
            
    related_cases_html = f"""
        <section class="section">
            <div class="container">
                <h2 style="text-align: center; margin-bottom: 3rem; color: var(--c-white);">Passende Fallbeispiele & Angebote</h2>
                <div class="grid-2">
                    {related_cards_html}
                </div>
            </div>
        </section>
    """

    # Assemble HTML
    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
{HTML_HEAD_TEMPLATE.format(
    title=case['metaTitle'],
    description=case['metaDescription'],
    og_image=f"https://www.sternenpfade.at{case['heroImage']['src']}",
    canonical_url=f"https://www.sternenpfade.at/fallbeispiele/{case['slug']}"
)}
    <style>
        .detail-layout {{
            display: grid;
            grid-template-columns: 1.8fr 1fr;
            gap: 3rem;
            align-items: start;
        }}
        .fact-row {{
            display: flex;
            justify-content: space-between;
            padding: 0.8rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            font-size: 0.95rem;
        }}
        .fact-row:last-child {{
            border-bottom: none;
        }}
        .fact-label {{
            font-weight: 500;
            color: var(--c-teal);
            max-width: 130px;
        }}
        .fact-value {{
            color: var(--c-white);
            text-align: right;
            font-weight: 300;
        }}
        .story-body p {{
            margin-bottom: 1.2rem;
        }}
        .story-body ul {{
            margin-bottom: 1.5rem;
            padding-left: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}
        .story-body ul li {{
            font-weight: 300;
        }}
        .disclaimer-card {{
            border-left: 4px solid var(--c-gold) !important;
            border-color: rgba(250, 180, 53, 0.15);
            background: rgba(250, 180, 53, 0.02) !important;
            padding: 1.5rem 2rem !important;
            margin-bottom: 3rem;
        }}
        .toc-card ol li a {{
            color: rgba(255, 255, 255, 0.8);
            transition: color 0.3s ease;
        }}
        .toc-card ol li a:hover {{
            color: var(--c-teal);
            text-decoration: underline;
        }}
        @media (max-width: 968px) {{
            .detail-layout {{
                grid-template-columns: 1fr;
            }}
            .facts-card {{
                order: -1;
            }}
        }}
    </style>
    <script type="application/ld+json">
{json_ld_string}
    </script>
</head>
<body>
{HEADER_TEMPLATE}

    <main id="main-content" class="theme-tiere">
        
        <!-- Hero Section -->
        <section class="hero" style="min-height: 50vh; padding-top: 130px; align-items: center; text-align: center;">
            <div class="container hero-content">
                {breadcrumbs}
                <span class="hero-subtitle" style="text-transform: uppercase; letter-spacing: 2px; color: var(--c-teal); font-weight: 500;">Fallstudie &bull; {case['animalType']}</span>
                <h1 style="font-size: 3rem; margin-top: 1rem; line-height: 1.2;">{case['title']}</h1>
                <p style="max-width: 800px; margin: 1.5rem auto 2.5rem auto; font-size: 1.2rem;">
                    Ein berührendes Fallbeispiel aus der Tierkommunikation über Vertrauen, innere Sicherheit, Herzensenergie und die tiefe Verbindung zwischen Mensch und Hund.
                </p>
                <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
                    <a href="/buchung" class="btn btn-primary" style="background: var(--c-teal); border: none;">Tierkommunikation buchen</a>
                    <a href="/dienstleistungen/tierkommunikation" class="btn btn-secondary">Mehr über Tierkommunikation erfahren</a>
                </div>
            </div>
        </section>

        <!-- Main Content Area -->
        <section class="section" style="padding-top: 0;">
            <div class="container">
                <div class="detail-layout">
                    
                    <!-- Left: Story Details -->
                    <div class="story-content">
                        
                        <!-- Disclaimer Card -->
                        <div class="glass-card disclaimer-card">
                            <p style="font-size: 0.95rem; line-height: 1.5; color: rgba(255,255,255,0.7); margin-bottom: 0;">
                                <strong>Anonymisierter Erfahrungsbericht:</strong> Dieses Fallbeispiel stammt aus der echten Praxis von Sternenpfade. Zur Wahrung der Anonymität wurden persönliche Details der Halterin verfremdet. Jedes Tier ist ein Individuum – dementsprechend verläuft jeder Prozess und jede Kommunikation einzigartig.
                            </p>
                        </div>

                        <!-- Story Sections -->
                        {sections_html}

                    </div>

                    <!-- Right: Sticky Factbox & TOC -->
                    <div class="sidebar-content" style="position: sticky; top: 100px;">
                        {facts_box_html}
                        {toc_html}
                        
                        <div style="border-radius: 24px; overflow: hidden; box-shadow: var(--shadow-glow); height: 260px;">
                            <img src="{case['heroImage']['src']}" alt="{case['heroImage']['alt']}" style="width: 100%; height: 100%; object-fit: cover;">
                        </div>
                    </div>

                </div>
            </div>
        </section>

        <!-- FAQ Section -->
        {faq_section_html}

        <!-- CTA Action Cards -->
        {related_cases_html}

    </main>

{FOOTER_TEMPLATE}
</body>
</html>
"""
    return html

def update_sitemap(cases):
    """Automatically adds the new clean URLs to sitemap.xml."""
    print("Updating sitemap.xml...")
    if not os.path.exists(SITEMAP_FILE):
        print("Sitemap file not found, skipping sitemap integration.")
        return

    # Parse sitemap.xml
    ET.register_namespace('', "http://www.sitemaps.org/schemas/sitemap/0.9")
    tree = ET.parse(SITEMAP_FILE)
    root = tree.getroot()

    # Find existing URLs in sitemap
    existing_urls = []
    for url_node in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
        loc_node = url_node.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
        if loc_node is not None:
            existing_urls.append(loc_node.text)

    # Check and add new URLs
    sitemap_changed = False
    new_urls = ['https://www.sternenpfade.at/fallbeispiele']
    for case in cases:
        new_urls.append(f"https://www.sternenpfade.at/fallbeispiele/{case['slug']}")

    for url in new_urls:
        if url not in existing_urls:
            print(f"Adding new URL to sitemap: {url}")
            url_node = ET.Element('{http://www.sitemaps.org/schemas/sitemap/0.9}url')
            
            loc_node = ET.Element('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
            loc_node.text = url
            url_node.append(loc_node)
            
            lastmod_node = ET.Element('{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod')
            lastmod_node.text = datetime.now().strftime("%Y-%m-%d")
            url_node.append(lastmod_node)
            
            changefreq_node = ET.Element('{http://www.sitemaps.org/schemas/sitemap/0.9}changefreq')
            changefreq_node.text = 'weekly'
            url_node.append(changefreq_node)
            
            priority_node = ET.Element('{http://www.sitemaps.org/schemas/sitemap/0.9}priority')
            priority_node.text = '0.8'
            url_node.append(priority_node)
            
            root.append(url_node)
            sitemap_changed = True

    if sitemap_changed:
        # Standard formatting (pretty-print helper to output clean indentations)
        def indent(elem, level=0):
            i = "\n" + level * "  "
            if len(elem):
                if not elem.text or not elem.text.strip():
                    elem.text = i + "  "
                if not elem.tail or not elem.tail.strip():
                    elem.tail = i
                for elem in elem:
                    indent(elem, level + 1)
                if not elem.tail or not elem.tail.strip():
                    elem.tail = i
            else:
                if level and (not elem.tail or not elem.tail.strip()):
                    elem.tail = i
        
        indent(root)
        tree.write(SITEMAP_FILE, encoding='utf-8', xml_declaration=True)
        print("sitemap.xml successfully updated.")
    else:
        print("Sitemap up to date. No additions needed.")

def main():
    """Reads case studies database and builds all HTML files."""
    if not os.path.exists(DATA_FILE):
        print(f"Error: JSON data file not found at {DATA_FILE}")
        return
        
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        cases = json.load(f)
        
    print(f"Loaded {len(cases)} case studies.")
    
    # 1. Compile Overview Page
    overview_html = build_overview_page(cases)
    overview_output_path = os.path.join(ROOT_DIR, 'fallbeispiele.html')
    with open(overview_output_path, 'w', encoding='utf-8') as f:
        f.write(overview_html)
    print(f"Generated overview page at: {overview_output_path}")

    # 2. Compile Detail Pages
    for case in cases:
        detail_html = build_detail_page(case, cases)
        detail_output_path = os.path.join(OUTPUT_DIR, f"{case['slug']}.html")
        with open(detail_output_path, 'w', encoding='utf-8') as f:
            f.write(detail_html)
        print(f"Generated detail page for '{case['animalName']}' at: {detail_output_path}")

    # 3. Update Sitemap
    update_sitemap(cases)

    print("Compilation completed successfully!")

if __name__ == '__main__':
    main()
