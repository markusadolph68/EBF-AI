# EBF Setup - Entra ID + Open WebUI + RAG Zugriffskontrolle

## Status

Diese Doku ist bewusst **nicht** der aktuelle Baselineschritt.
Sie gilt erst dann, wenn der lokale Pilot mit Open WebUI + MLX + Chroma stabil laeuft.

Reihenfolge:
1. lokalen Pilot stabilisieren
2. Dokumente, Metadaten und Tests absichern
3. Zugriff lokal und operativ im Kleinen pruefen
4. erst danach Entra anschliessen

## Ziel

Zugriff auf RAG-Daten in Open WebUI so steuern, dass spaeter nur bestimmte Benutzergruppen Zugriff haben.

## Voraussetzungen

Vor Entra muessen mindestens diese Punkte stehen:
- Open WebUI laeuft stabil
- MLX-Endpoint ist angebunden
- Chroma und Ingestion funktionieren reproduzierbar
- Pilotdokumente sind je Bereich getrennt
- lokaler Pilotbetrieb ist ohne Entra verprobt

## Zielarchitektur

```text
Microsoft Entra (Gruppen)
        ↓
OIDC / OAuth2 Login
        ↓
Open WebUI (Group Sync)
        ↓
Knowledge Bases mit Zugriff pro Gruppe
```

## 1. Gruppenmodell in Entra

Sharing-Gruppen fuer Datenzugriff:
- `OWUI-RAG-HR`
- `OWUI-RAG-Vertrieb`
- `OWUI-RAG-Projekte`

Optionale Berechtigungsgruppen:
- `OWUI-Admins`
- `OWUI-Knowledge-Editors`
- `OWUI-Tools-Advanced`

## 2. Entra App Registration

Wichtige Einstellungen:
- Redirect URI: `https://chat.ebf-intern.de/oauth/oidc/callback`
- Client ID notieren
- Tenant ID notieren
- Client Secret notieren

## 3. Gruppen-Claim aktivieren

In Entra:
- Token Configuration -> Add Groups Claim
- Empfehlung: nur "Groups assigned to the application"

## 4. Open WebUI `.env` Konfiguration

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

## 5. Verhalten

Gruppen werden bei jedem Login synchronisiert:
- Gruppe im Token -> Zugriff vorhanden
- Gruppe fehlt -> Zugriff wird entfernt
- Aenderungen greifen nach Logout und erneutem Login

## 6. RAG Zugriff steuern

Vorgehen:
1. Login ueber Entra
2. Gruppen in Open WebUI pruefen
3. Knowledge Bases erstellen
4. Zugriff pro Gruppe setzen

Beispiel:
- HR Knowledge Base -> `OWUI-RAG-HR`
- Vertrieb Knowledge Base -> `OWUI-RAG-Vertrieb`
- Projekte Knowledge Base -> `OWUI-RAG-Projekte`

## 7. Wichtige Stolperfallen

- zu viele Gruppen -> Token wird zu gross
- Open WebUI synchronisiert Gruppen nur beim Login
- Default-Rechte muessen minimal bleiben

## 8. Rollout-Empfehlung

Entra erst aktivieren, wenn:
- der lokale Pilot inhaltlich belastbar ist
- der Testkatalog gruene Ergebnisse liefert
- die Bereichstrennung fachlich akzeptiert ist
- Admins den Betrieb ohne Debugging beherrschen
