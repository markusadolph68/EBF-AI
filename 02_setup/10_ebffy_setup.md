# 🚀 EBFfy Setup – Branding + Deployment Guide  
## Open WebUI → EBF AI Plattform

---

## 🎯 Ziel

Open WebUI wird zu:

👉 **EBFfy – interner AI Assistent der EBF Gruppe**

Mit:
- eigenem Branding  
- eigener Domain  
- Entra SSO  
- professionellem Look & Feel  

---

# 🧱 Zielarchitektur

```text
Internet / Mitarbeiter
        ↓
https://ai.ebf.de
        ↓
Reverse Proxy (Nginx / Traefik)
        ↓
Open WebUI (EBFfy)
        ↓
LLM Backend (MLX / RunPod)
        ↓
RAG (Chroma)
```

---

# ⚙️ 1. `.env` Branding (Copy & Paste)

```env
WEBUI_NAME=EBFfy
WEBUI_URL=https://ai.ebf.de
WEBUI_DESCRIPTION=Interner AI Assistent der EBF Gruppe

DEFAULT_LOCALE=de-DE
ENABLE_SIGNUP=false

ENABLE_OAUTH_SIGNUP=true
OAUTH_PROVIDER_NAME=Microsoft Entra

OPENID_PROVIDER_URL=https://login.microsoftonline.com/DEIN_TENANT_ID/v2.0/.well-known/openid-configuration
OPENID_REDIRECT_URI=https://ai.ebf.de/oauth/oidc/callback

OAUTH_CLIENT_ID=DEINE_CLIENT_ID
OAUTH_CLIENT_SECRET=DEIN_CLIENT_SECRET
OAUTH_SCOPES=openid profile email

ENABLE_OAUTH_GROUP_MANAGEMENT=true
OAUTH_GROUP_CLAIM=groups
OAUTH_GROUP_DEFAULT_SHARE=members
```

---

# 🌐 2. Domain Setup

```text
ai.ebf.de → Server-IP
```

---

# 🔐 3. Reverse Proxy (Nginx Beispiel)

```nginx
server {
    listen 80;
    server_name ai.ebf.de;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

# 🎨 4. Branding

## Farben
- Primary: #0066CC
- Secondary: #0F172A
- Accent: #22C55E
- Background: #F8FAFC

---

# 🧠 5. Systemprompt

```text
Du bist EBFfy, der interne AI-Assistent der EBF Gruppe.

Deine Aufgaben:
- beantworte Fragen zu internen Prozessen
- unterstütze bei Angeboten, Projekten und Analysen

Regeln:
- nutze nur verfügbare Quellen
- erfinde keine Informationen
- antworte auf Deutsch
```

---

# 🔐 6. Entra Login

- App Name: EBFfy
- Redirect URI: https://ai.ebf.de/oauth/oidc/callback

---

# 🔥 7. Quick Wins

- Domain
- Name
- SSO
- Systemprompt

---

# 🧾 TL;DR

👉 Open WebUI wird zu EBFfy  
👉 Branding + SSO + Domain = Produktgefühl
