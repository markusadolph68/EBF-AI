# EBF Pilot Setup – Vollständigere MLX/OpenAI-Server-Variante

## Ziel
Diese Variante ist robuster als der Minimalserver und besser geeignet, wenn **Open WebUI** sauber mit einem **OpenAI-kompatiblen lokalen Endpoint** sprechen soll.

Sie ergänzt den bestehenden Pilot-Guide um:
- eine etwas vollständigere API-Struktur
- Chat-Completions statt nur einfache Completions
- ein klareres Request/Response-Schema
- eine bessere Basis für Open WebUI

---

## 1. Voraussetzungen

Zusätzlich zu deinem bestehenden Setup:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install mlx mlx-lm fastapi uvicorn pydantic
```

Optional sinnvoll:
```bash
python3 -m pip install python-dotenv
```

---

## 2. Empfohlene Datei `app/mlx_openai_server.py`

```python
import os
from typing import List, Optional, Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mlx_lm import load, generate


MODEL_NAME = os.getenv("MODEL_NAME", "mlx-community/Llama-3.2-3B-Instruct")

app = FastAPI(title="MLX OpenAI-Compatible Server")

model, tokenizer = load(MODEL_NAME)


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatCompletionRequest(BaseModel):
    model: Optional[str] = None
    messages: List[Message]
    max_tokens: int = 300
    temperature: float = 0.2


class CompletionRequest(BaseModel):
    model: Optional[str] = None
    prompt: str
    max_tokens: int = 300
    temperature: float = 0.2


def build_prompt(messages: List[Message]) -> str:
    system_parts = []
    conversation_parts = []

    for msg in messages:
        if msg.role == "system":
            system_parts.append(msg.content.strip())
        elif msg.role == "user":
            conversation_parts.append(f"User: {msg.content.strip()}")
        elif msg.role == "assistant":
            conversation_parts.append(f"Assistant: {msg.content.strip()}")

    system_text = "\n".join(system_parts).strip()
    convo_text = "\n".join(conversation_parts).strip()

    if system_text:
        return f"{system_text}\n\n{convo_text}\nAssistant:"
    return f"{convo_text}\nAssistant:"


@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL_NAME}


@app.get("/v1/models")
def list_models():
    return {
        "object": "list",
        "data": [
            {
                "id": MODEL_NAME,
                "object": "model",
                "owned_by": "local-mlx"
            }
        ]
    }


@app.post("/v1/completions")
def completions(req: CompletionRequest):
    try:
        text = generate(
            model,
            tokenizer,
            prompt=req.prompt,
            max_tokens=req.max_tokens,
        )
        return {
            "id": "cmpl-local-mlx",
            "object": "text_completion",
            "model": MODEL_NAME,
            "choices": [
                {
                    "index": 0,
                    "text": text,
                    "finish_reason": "stop"
                }
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/chat/completions")
def chat_completions(req: ChatCompletionRequest):
    try:
        prompt = build_prompt(req.messages)
        text = generate(
            model,
            tokenizer,
            prompt=prompt,
            max_tokens=req.max_tokens,
        )
        return {
            "id": "chatcmpl-local-mlx",
            "object": "chat.completion",
            "model": MODEL_NAME,
            "choices": [
                {
                    "index": 0,
                    "finish_reason": "stop",
                    "message": {
                        "role": "assistant",
                        "content": text
                    }
                }
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 3. `.env` anpassen

Wenn du diese Server-Variante nutzen willst, sollte in deiner `.env` mindestens stehen:

```env
MODEL_NAME=mlx-community/Llama-3.2-3B-Instruct
MLX_PORT=8000
```

Später kannst du hier auch ein anderes MLX-Modell setzen.

---

## 4. Startbefehl

Im Projektordner:

```bash
cd ~/ebf-ai-pilot/app
MODEL_NAME=mlx-community/Llama-3.2-3B-Instruct \
python3 -m uvicorn mlx_openai_server:app --host 0.0.0.0 --port 8000
```

Oder dauerhaft über dein Startskript.

---

## 5. `scripts/start.sh` anpassen

Wenn du von `mlx_server.py` auf die robustere Variante wechselst, nutze stattdessen:

```bash
#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."

echo "[1/2] Docker Dienste starten..."
docker compose up -d

echo "[2/2] MLX OpenAI Server starten..."
cd app
python3 -m uvicorn mlx_openai_server:app --host 0.0.0.0 --port 8000
```

---

## 6. Open WebUI-Einstellungen

In **Open WebUI**:

### Provider anlegen
- **Type:** OpenAI-compatible
- **Base URL:** `http://host.docker.internal:8000/v1`
- **API Key:** `mlx`

### Warum diese Variante besser ist
Open WebUI erwartet typischerweise eher:
- `/v1/models`
- `/v1/chat/completions`

Genau diese Endpunkte stellt die robustere Variante bereit.

---

## 7. Schnelltests mit curl

### Health
```bash
curl http://localhost:8000/health
```

### Models
```bash
curl http://localhost:8000/v1/models
```

### Completions
```bash
curl http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Erkläre RAG in drei Sätzen auf Deutsch.",
    "max_tokens": 200
  }'
```

### Chat Completions
```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mlx-community/Llama-3.2-3B-Instruct",
    "messages": [
      {"role": "system", "content": "Antworte auf Deutsch, kurz und präzise."},
      {"role": "user", "content": "Was ist RAG?"}
    ],
    "max_tokens": 200
  }'
```

---

## 8. Sinnvolle Modellwahl für deinen Mac mini M4 mit 64 GB

Für den Anfang würde ich lokal testen mit:

### Sehr stabil
- `mlx-community/Llama-3.2-3B-Instruct`

### Danach als sinnvoller nächster Schritt
- ein 7B- oder 8B-Instruct-Modell in MLX-Form

Wichtig:
- lieber zuerst stabil und reproduzierbar
- dann größer werden

---

## 9. Bekannte Grenzen dieser Variante

Auch diese robustere Variante ist noch **kein vollständiger OpenAI-Ersatz**.

Das heißt:
- Streaming fehlt
- Embeddings fehlen
- Tool Calling fehlt
- Auth ist minimal
- Token-Usage wird nicht sauber berechnet
- einige Open-WebUI-Funktionen könnten je nach Version mehr erwarten

Für einen kleinen Pilot ist das trotzdem oft ausreichend.

---

## 10. Wann du später upgraden solltest

Du solltest auf eine noch vollständigere Lösung wechseln, wenn du:
- mehrere Nutzer gleichzeitig hast
- Streaming brauchst
- Embeddings über denselben Endpoint willst
- Open WebUI vollständig stabilisieren willst
- lokal und RunPod konsistent betreiben willst

Dann ist ein dedizierter MLX/OpenAI-Wrapper oder ein anderer standardnäherer lokaler Server sinnvoll.

---

## 11. Empfohlene Reihenfolge

### Jetzt
- mit dieser Datei lokal starten
- Open WebUI anbinden
- 10–20 Dokumente testen

### Danach
- Chroma-Pipeline ergänzen
- größeres Modell testen
- optional RunPod L40S als zweites Backend anbinden

---

## 12. Kurzfazit

Für deinen Pilot ist diese Variante der bessere lokale Standard, weil sie:
- näher an der OpenAI-API ist
- besser zu Open WebUI passt
- später leichter durch RunPod ergänzt werden kann
