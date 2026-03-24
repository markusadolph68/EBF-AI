# EBF Pilot Setup auf Mac mini M4 (64 GB)

## Ziel
Lokaler Pilot mit:
- **MLX** für Inferenz auf Apple Silicon
- **Open WebUI** als Oberfläche
- **Chroma** als lokale Vektor-Datenbank
- optional **RunPod L40S** als Cloud-Backend

---

## 1. Empfohlene Ordnerstruktur

```text
~/ebf-ai-pilot/
├── docker-compose.yml
├── .env
├── app/
│   └── mlx_server.py
├── chroma_data/
├── openwebui_data/
├── documents/
│   ├── faq/
│   ├── prozesse/
│   └── angebote/
└── scripts/
    ├── start.sh
    └── stop.sh
```

---

## 2. Einmalige Installationen auf dem Mac

### Homebrew
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Basis-Tools
```bash
brew install python git docker
```

### Python-Pakete
```bash
python3 -m pip install --upgrade pip
python3 -m pip install mlx mlx-lm fastapi uvicorn chromadb
```

### Docker Desktop
- Docker Desktop für macOS installieren
- danach starten

---

## 3. Projektordner anlegen

```bash
mkdir -p ~/ebf-ai-pilot/app
mkdir -p ~/ebf-ai-pilot/chroma_data
mkdir -p ~/ebf-ai-pilot/openwebui_data
mkdir -p ~/ebf-ai-pilot/documents/faq
mkdir -p ~/ebf-ai-pilot/documents/prozesse
mkdir -p ~/ebf-ai-pilot/documents/angebote
mkdir -p ~/ebf-ai-pilot/scripts
cd ~/ebf-ai-pilot
```

---

## 4. Datei `.env`

Datei `~/ebf-ai-pilot/.env` anlegen:

```env
OPEN_WEBUI_PORT=3000
MLX_PORT=8000
CHROMA_PORT=8001
MODEL_NAME=mlx-community/Llama-3.2-3B-Instruct
RUNPOD_BASE_URL=
RUNPOD_API_KEY=
```

Für den Start kannst du `RUNPOD_BASE_URL` und `RUNPOD_API_KEY` leer lassen.

---

## 5. Datei `app/mlx_server.py`

```python
from fastapi import FastAPI
from pydantic import BaseModel
from mlx_lm import load, generate

app = FastAPI()

MODEL_NAME = "mlx-community/Llama-3.2-3B-Instruct"
model, tokenizer = load(MODEL_NAME)

class CompletionRequest(BaseModel):
    prompt: str
    max_tokens: int = 300

@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL_NAME}

@app.post("/v1/completions")
def completions(req: CompletionRequest):
    text = generate(
        model,
        tokenizer,
        prompt=req.prompt,
        max_tokens=req.max_tokens
    )
    return {
        "id": "mlx-local",
        "object": "text_completion",
        "choices": [
            {
                "index": 0,
                "text": text,
                "finish_reason": "stop"
            }
        ]
    }
```

---

## 6. Datei `docker-compose.yml`

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    restart: unless-stopped
    ports:
      - "${OPEN_WEBUI_PORT}:8080"
    volumes:
      - ./openwebui_data:/app/backend/data
    environment:
      - WEBUI_SECRET_KEY=ebf-local-pilot
    extra_hosts:
      - "host.docker.internal:host-gateway"

  chroma:
    image: chromadb/chroma:latest
    container_name: chroma
    restart: unless-stopped
    ports:
      - "${CHROMA_PORT}:8000"
    volumes:
      - ./chroma_data:/chroma/chroma
```

---

## 7. Start- und Stop-Skripte

### `scripts/start.sh`
```bash
#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."

echo "[1/2] Docker Dienste starten..."
docker compose up -d

echo "[2/2] MLX Server starten..."
cd app
python3 -m uvicorn mlx_server:app --host 0.0.0.0 --port 8000
```

### `scripts/stop.sh`
```bash
#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."
docker compose down
pkill -f "uvicorn mlx_server:app" || true
```

### Ausführbar machen
```bash
chmod +x ~/ebf-ai-pilot/scripts/start.sh
chmod +x ~/ebf-ai-pilot/scripts/stop.sh
```

---

## 8. Starten

### Terminal 1
```bash
cd ~/ebf-ai-pilot
./scripts/start.sh
```

### Prüfung MLX
Im Browser oder Terminal:
```bash
curl http://localhost:8000/health
```

### Prüfung Open WebUI
Im Browser:
```text
http://localhost:3000
```

### Prüfung Chroma
Im Browser oder Terminal:
```bash
curl http://localhost:8001/api/v1/heartbeat
```

---

## 9. Open WebUI konfigurieren

Nach dem ersten Aufruf:

1. Admin-Account anlegen
2. **Settings**
3. **Connections**
4. neuen Provider anlegen

### Lokaler MLX-Provider
- **Type:** OpenAI-compatible
- **Base URL:** `http://host.docker.internal:8000/v1`
- **API Key:** `mlx`

Hinweis: Der kleine Beispielserver ist minimal. Manche Funktionen von Open WebUI können je nach Version mehr OpenAI-Endpunkte erwarten. Für den Pilot reicht das oft zum Start, für stabileren Betrieb ist später ein vollständigerer OpenAI-kompatibler MLX-Server sinnvoll.

---

## 10. Chroma nutzen

Für den Start reicht es, Chroma als laufenden Dienst bereitzuhalten. Wenn du später eine eigene Ingestion-Pipeline baust, ist die URL:

```text
http://localhost:8001
```

---

## 11. Dokumente vorbereiten

Lege deine Pilot-Dokumente hier ab:

```text
~/ebf-ai-pilot/documents/
```

Empfohlene Unterordner:
- `faq/`
- `prozesse/`
- `angebote/`

Empfohlen:
- zuerst nur **10–20 saubere Dokumente**
- lieber Markdown, TXT, DOCX oder gut strukturierte PDFs
- pro Dokument klarer Titel und Datum

---

## 12. Optional: RunPod L40S einbinden

Wenn du später RunPod ergänzen willst:

1. RunPod-Endpoint anlegen
2. OpenAI-kompatible URL notieren
3. API-Key erzeugen
4. Werte in `.env` ergänzen:

```env
RUNPOD_BASE_URL=https://api.runpod.ai/v2/DEIN-ENDPOINT/openai/v1
RUNPOD_API_KEY=DEIN_KEY
```

Dann in Open WebUI einen zweiten Provider anlegen:

### RunPod-Provider
- **Type:** OpenAI-compatible
- **Base URL:** `https://api.runpod.ai/v2/DEIN-ENDPOINT/openai/v1`
- **API Key:** dein RunPod-Key

So kannst du lokal zwischen:
- **MLX lokal**
- **RunPod L40S**
wechseln.

---

## 13. Sinnvolle erste Tests

### Modelltest
- „Antworte auf Deutsch in 5 Stichpunkten: Was ist RAG?“

### Wissensfragen
- „Wie läuft Prozess X ab?“
- „Fasse Dokument Y zusammen.“
- „Welche Schritte muss ich beachten?“

### Qualitätsprüfung
- korrekt: ja/nein
- Quelle brauchbar: ja/nein
- Halluzination: ja/nein
- Antwortzeit ok: ja/nein

---

## 14. Empfohlener Systemprompt

```text
Antworte auf Deutsch, klar und knapp.
Nutze bevorzugt bereitgestellte Inhalte und Quellen.
Erfinde keine internen Informationen.
Wenn etwas unklar oder nicht belegt ist, sage das offen.
```

---

## 15. Typische Fehler vermeiden

- nicht mit 200 Dokumenten starten
- keine PDF-Sammlung ohne Struktur
- nicht gleich zu große Modelle wählen
- erst einen Use Case sauber testen
- RunPod erst ergänzen, wenn lokal alles läuft

---

## 16. Empfohlene Reihenfolge

### Phase 1
- alles lokal zum Laufen bringen
- Open WebUI + MLX testen

### Phase 2
- 10–20 Dokumente kuratieren
- erste RAG-Tests

### Phase 3
- optional RunPod L40S zuschalten
- lokales und Cloud-Modell vergleichen

---

## 17. Nächster sinnvoller Schritt

Wenn der Stack läuft, brauchst du als Nächstes:
- eine kleine **Ingestion-Pipeline**
- sinnvolles **Chunking**
- saubere **Metadaten**
- reproduzierbare **Testfragen**
