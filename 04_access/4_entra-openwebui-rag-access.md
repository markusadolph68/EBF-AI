# 🔐 EBF Setup – Entra ID + Open WebUI + RAG Zugriffskontrolle

## 🎯 Ziel
Zugriff auf RAG-Daten (Knowledge Bases) in Open WebUI so steuern, dass **nur bestimmte Benutzergruppen** Zugriff haben.

---

# 🧠 Zielarchitektur

```text
Microsoft Entra (Gruppen)
        ↓
OIDC / OAuth2 Login
        ↓
Open WebUI (Group Sync)
        ↓
Knowledge Bases (RAG) mit Zugriff pro Gruppe
```

---

# 🧱 1. Gruppenmodell in Entra

## 🔹 Sharing-Gruppen (für Datenzugriff)

- OWUI-RAG-HR
- OWUI-RAG-Vertrieb
- OWUI-RAG-Projekte

👉 Diese Gruppen steuern **Zugriff auf Knowledge Bases**

---

## 🔹 Optional: Berechtigungsgruppen

- OWUI-Admins
- OWUI-Knowledge-Editors
- OWUI-Tools-Advanced

👉 Diese steuern **Funktionen**, nicht Inhalte

---

# ⚙️ 2. Entra App Registration

## Einstellungen:

- **Redirect URI**
```text
https://chat.ebf-intern.de/oauth/oidc/callback
```

- Notiere:
  - Client ID
  - Tenant ID
  - Client Secret

---

# 🧾 3. Gruppen-Claim aktivieren (wichtig!)

In Entra:

- Token Configuration → Add Groups Claim

👉 Empfehlung:
- „Groups assigned to the application“

⚠️ Wichtig:
- zu viele Gruppen → Token wird zu groß
- dann fehlen Gruppen im Login

---

# 🔧 4. Open WebUI .env Konfiguration

```env
WEBUI_URL=https://chat.ebf-intern.de

ENABLE_OAUTH_SIGNUP=true
OAUTH_MERGE_ACCOUNTS_BY_EMAIL=true

OAUTH_PROVIDER_NAME=Microsoft Entra

OPENID_PROVIDER_URL=https://login.microsoftonline.com/DEIN_TENANT_ID/v2.0/.well-known/openid-configuration
OPENID_REDIRECT_URI=https://chat.ebf-intern.de/oauth/oidc/callback

OAUTH_CLIENT_ID=DEINE_CLIENT_ID
OAUTH_CLIENT_SECRET=DEIN_CLIENT_SECRET

OAUTH_SCOPES=openid profile email

ENABLE_OAUTH_GROUP_MANAGEMENT=true
ENABLE_OAUTH_GROUP_CREATION=true
OAUTH_GROUP_CLAIM=groups
OAUTH_GROUP_DEFAULT_SHARE=members
```

---

# 🔐 5. Verhalten (wichtig zu verstehen)

👉 Gruppen werden bei jedem Login synchronisiert

- Gruppe im Token → Zugriff vorhanden
- Gruppe fehlt → Zugriff wird entfernt

👉 Änderungen greifen erst nach:
- Logout / Login

---

# 📚 6. RAG Zugriff steuern (Open WebUI)

## Vorgehen:

1. Login über Entra
2. Prüfen, ob Gruppen sichtbar sind
3. Knowledge Bases erstellen
4. Zugriff pro Gruppe setzen

---

## Beispiel

### HR Knowledge Base
- Zugriff: OWUI-RAG-HR

### Vertrieb Knowledge Base
- Zugriff: OWUI-RAG-Vertrieb

### Projekte Knowledge Base
- Zugriff: OWUI-RAG-Projekte

---

# 🏢 7. Konkretes Zielmodell für EBF

## HR
Gruppe: OWUI-RAG-HR

Zugriff auf:
- HR Policies
- Onboarding
- Verträge / Prozesse

---

## Vertrieb
Gruppe: OWUI-RAG-Vertrieb

Zugriff auf:
- Angebotsbausteine
- Leistungen
- Referenzen

---

## Projekte
Gruppe: OWUI-RAG-Projekte

Zugriff auf:
- Projektmethodik
- Checklisten
- Delivery Playbooks

---

## Admin
Gruppe: OWUI-Admins

Zugriff auf:
- komplette Plattform
- Modelle
- Konfiguration

---

# ⚠️ 8. Wichtige Stolperfallen

## ❗ Gruppen-Token Limit
- zu viele Gruppen → fehlen im Token

👉 Lösung:
- nur relevante Gruppen verwenden

---

## ❗ Sync Verhalten
- Open WebUI überschreibt Gruppen bei Login

👉 bedeutet:
- Entra = einzige Wahrheit

---

## ❗ Default-Rechte
- Open WebUI ist **additiv**

👉 daher:
- Default minimal halten
- Zugriff nur über Gruppen vergeben

---

# 🚀 9. Best Practice für deinen Pilot

## Schrittfolge:

1. Entra Gruppen anlegen
2. App registrieren
3. Gruppenclaim aktivieren
4. Open WebUI konfigurieren
5. Login testen
6. Knowledge Bases trennen
7. Zugriff per Gruppe vergeben

---

# 🔒 10. Erweiterung (optional)

## SCIM (für später)
- automatische Benutzer- & Gruppen-Synchronisation
- besser für Produktion

---

# 🧾 TL;DR

👉 Zugriff auf RAG steuerst du über:

- Entra Gruppen
- OIDC Login
- Open WebUI Group Sync
- Private Knowledge Bases

👉 Wichtig:
- Gruppen sauber definieren
- Default-Rechte minimal halten
- pro Bereich eigene Knowledge Base

---

# 💡 Empfehlung

Für deinen Pilot:

👉 halte es einfach:

- 3 Gruppen (HR / Vertrieb / Projekte)
- 3 Knowledge Bases
- Entra als einzige Quelle

→ funktioniert sofort und ist sauber skalierbar
