# EBFfy Setup - Branding + Deployment Guide
## Open WebUI -> EBF AI Plattform

## Ziel

Open WebUI wird in der Baseline zuerst zu:

`EBFfy` - interner AI-Assistent der EBF Gruppe

Mit:
- eigenem Branding
- hostseitigem MLX-Modellserver
- Chroma als RAG-Basis
- lokalem Pilotbetrieb ohne Entra

Entra ist bewusst nicht Teil dieses Baselineschritts und folgt spaeter als letzter Integrationsschritt.

## Zielarchitektur

```text
Pilotnutzer
        ↓
Open WebUI (EBFfy)
        ↓
LLM Backend (MLX lokal)
        ↓
RAG (Chroma)
```

## 1. `.env` Branding

```env
WEBUI_NAME=EBFfy
WEBUI_SECRET_KEY=ebf-local-pilot
DEFAULT_LOCALE=de-DE
OPEN_WEBUI_PORT=3000
CHROMA_PORT=8001
MLX_PORT=8000
MLX_MODEL_NAME=NexVeridian/Qwen3.5-4B-5bit
```

## 2. Branding

Farben:
- Primary: `#0066CC`
- Secondary: `#0F172A`
- Accent: `#22C55E`
- Background: `#F8FAFC`

## 3. Baseline-Setup

1. `mvp/.env` anlegen
2. `./mvp/scripts/start_stack.sh` ausfuehren
3. `./mvp/scripts/start_mlx_host.sh` ausfuehren
4. `./mvp/scripts/healthcheck.sh` ausfuehren
5. Open WebUI unter `http://localhost:3000` oeffnen

## 4. Provider in Open WebUI

- Typ: `OpenAI-compatible`
- Base URL: `http://host.docker.internal:8000/v1`
- API Key: `mlx`
- Modell: Wert aus `MLX_MODEL_NAME`

## 5. Systemprompt

```text
Du bist EBFfy, der interne AI-Assistent der EBF Gruppe.

Deine Aufgaben:
- beantworte Fragen zu internen Prozessen
- unterstuetze bei Angeboten, Projekten und Analysen

Regeln:
- nutze nur verfuegbare Quellen
- erfinde keine Informationen
- antworte auf Deutsch
```

## 6. Spaeterer Ausbau

Nach stabiler Baseline folgen:
- Domain und Reverse Proxy
- erweitertes Branding
- Entra SSO
- gruppenbasierte Zugriffstrennung

## TL;DR

Erst Open WebUI + MLX + Chroma stabilisieren.
Dann Branding und Pilotbetrieb saubermachen.
Entra kommt zuletzt.
