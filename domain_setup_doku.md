# Domain-Umzug: Webador zu Render

Diese Dokumentation beschreibt die finalen Schritte, um deine Domain `sternenpfade.at` von Webador auf deinen neuen Render-Server umzuleiten, **ohne** dass dein E-Mail-Postfach (`info@sternenpfade.at`) beeinträchtigt wird.

Sobald du mit dem Testen fertig bist und live gehen möchtest, folge dieser Anleitung.

## Vorbereitung: Die Daten von Render holen
1. Logge dich in dein [Render Dashboard](https://dashboard.render.com) ein.
2. Klicke auf deinen Web Service (Sternenpfade).
3. Gehe im linken Menü auf **"Settings"** und scrolle runter zu **"Custom Domains"**.
4. Klicke auf **"Add Custom Domain"**, trage `sternenpfade.at` ein und bestätige (am besten auch für `www.sternenpfade.at`).
5. Render zeigt dir nun ein Fenster mit den benötigten Ziel-Werten an. Lass dieses Fenster einfach offen.

## Hauptschritt: DNS-Einträge bei Webador ändern
Jetzt musst du Webador mitteilen, dass die Website ab sofort bei Render läuft.

1. Logge dich in dein **Webador Konto** ein.
2. Gehe in die **Einstellungen** deiner Domain/Website.
3. Suche den Bereich **"DNS-Einstellungen"** (manchmal auch "Erweiterte Domain-Einstellungen" oder "DNS-Verwaltung").
4. Du siehst nun eine Tabelle mit verschiedenen DNS-Records.

**WICHTIG für deine E-Mails:**
Ändere oder lösche **NIEMALS** die Einträge vom Typ `MX` oder `TXT` (SPF). Diese sind dafür verantwortlich, dass du weiterhin E-Mails über `info@sternenpfade.at` empfangen und versenden kannst!

### 1. Den WWW-Eintrag setzen (CNAME)
Suche nach einem bestehenden Eintrag für `www` oder lege einen neuen an:
* **Typ:** `CNAME`
* **Name / Hostname:** `www`
* **Wert / Ziel:** `sternenpfade.onrender.com`

### 2. Den Haupt-Eintrag setzen (A-Record)
Suche nach einem bestehenden A-Record, der als Hostname `@` hat (oder leer ist) und auf die alte Webador-IP (z.B. `35.204.150.5`) zeigt. **Lösche diesen alten A-Record.**
Lege dann den neuen an:
* **Typ:** `A`
* **Name / Hostname:** `@` *(oder leer lassen, falls Webador kein @ akzeptiert)*
* **Wert / Ziel:** `216.24.57.1` *(Das ist die IP-Adresse von Render)*

## Abschluss: Geduld und Verifizierung
1. Speichere die Einstellungen bei Webador.
2. Gehe zurück zum offenen Fenster bei Render und klicke auf **"Verify"**.
3. **Wartezeit einplanen:** DNS-Änderungen greifen selten in der ersten Sekunde. Es kann **15 Minuten bis hin zu 24 Stunden** dauern, bis alle Internet-Server weltweit die neue Adresse gelernt haben.
4. Render wird den Status erst auf "Not verified" oder "Pending" setzen. Das ist normal!
5. Lade die Render-Seite nach einer Weile neu. Sobald dort ein grünes **"Verified"** steht, ist der Umzug erfolgreich abgeschlossen.
6. Render generiert dann automatisch das SSL-Zertifikat (das Schloss-Symbol) für dich.

Deine neue Website ist ab dann sicher unter `https://sternenpfade.at` erreichbar!
