# DNS-Umzug: Webador zu Render (Backup & Übersicht)

Diese Datei dient als **Sicherheits-Backup** deiner DNS-Einstellungen bei Webador für den Go-Live auf Render. Falls etwas schiefgeht, kannst du anhand der "ALT"-Werte den ursprünglichen Zustand jederzeit wiederherstellen.

---

## ❌ Diese Einträge werden GELÖSCHT (Papierkorb)
Diese beiden Einträge verweisen auf den alten Webador-Baukasten und müssen gelöscht werden, damit Render übernehmen kann.

**1. Die alte Haupt-IP (A-Record)**
* **Typ:** `A`
* **Name:** *(leer)*
* **Wert:** `35.204.150.5`

**2. Der alte Sternchen-Eintrag (Subdomains)**
* **Typ:** `CNAME`
* **Name:** `*`
* **Wert:** `website-rendering.webador.com`

---

## ✅ Diese Einträge kommen NEU hinzu (+ Datensatz hinzufügen)
Diese beiden Einträge leiten den Website-Verkehr (ohne www und mit www) auf deinen neuen Render-Server um.

**1. Die neue Haupt-IP (A-Record für sternenpfade.at)**
* **Typ:** `A`
* **Name:** *(leer)*
* **Wert:** `216.24.57.1` *(Die Render-IP)*

**2. Die Weiterleitung für www (CNAME für www.sternenpfade.at)**
* **Typ:** `CNAME`
* **Name:** `www`
* **Wert:** `sternenpfade.onrender.com` *(Ersetze dies durch deinen exakten Render-Link, falls er anders lautet)*

---

## 🛡️ Diese Einträge bleiben UNBERÜHRT (Nicht anfassen!)
Alle folgenden Einträge sind zwingend für den E-Mail-Verkehr (`info@sternenpfade.at`) erforderlich. Wenn diese geändert werden, kommen keine Rechnungen oder Buchungsbestätigungen mehr an!

* `MX` | *(leer)* | `mail.webador.com`
* `TXT` | *(leer)* | `v=spf1 include:_spf.webador.com ~all`
* `TXT` | `_dmarc` | `v=DMARC1; p=none`
* `TXT` | `mandrill._domainkey` | `v=DKIM1; k=rsa; p=...`
* `CNAME` | `mail` | `mail.webador.com`
* `CNAME` | `autodiscover` | `block.mail.webador.com`
* `CNAME` | `autoconfig` | `autoconfig.mail.webador.com`
* `CNAME` | `sparkpost._domainkey` | `sparkpost._domainkey.webador.com`
* `CNAME` | `jouwweb._domainkey` | `website-rendering._domainkey.jouwweb.nl`
* `SRV` | `_autodiscover._tcp` | `0 443 autoconfig.mail.webador.com`

---

## Nächste Schritte nach der Änderung
1. Webador-Einstellungen speichern.
2. In Render einloggen -> Web Service anklicken -> Settings -> Custom Domains.
3. `sternenpfade.at` und `www.sternenpfade.at` hinzufügen und auf **Verify** klicken.
4. Geduld haben (es kann ein paar Stunden dauern, bis Render das grüne "Verified" anzeigt).
