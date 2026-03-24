# EBF AI MVP

Docker-basierter MVP fuer:
- lokale Anmeldung ohne Entra
- Spaces
- Dokument-Upload pro Space
- Docling-basierte Ingestion
- Chroma als RAG-Speicher
- Chat mit hostseitigem MLX/OpenAI-kompatiblem LLM

## Architektur

- `app`: FastAPI mit Server-Side-HTML
- `chroma`: Vektor-Datenbank
- `mlx_host`: MLX/OpenAI-kompatibler Server auf dem Mac-Host

## Wichtiger Mac-Hinweis

Der MVP nutzt Docker fuer App und Chroma.
Das Chat-LLM laeuft bewusst hostseitig mit MLX auf dem Mac Mini, weil MLX/Metal in Linux-Containern auf macOS nicht sauber nutzbar ist.

Deshalb ist die Chat-Anbindung bewusst OpenAI-kompatibel und auf MLX am Host ausgelegt:
- hostseitiger MLX/OpenAI-Server
- kleines Qwen-3.5-Modell fuer Apple Silicon
- spaeter austauschbar gegen anderen OpenAI-kompatiblen Provider

## Schnellstart

1. Konfiguration anlegen:

```bash
cd mvp
cp .env.example .env
mkdir -p data
```

2. Stack starten:

```bash
docker compose up --build
```

3. MLX-Server auf dem Host starten:

```bash
cd mvp
python3 -m venv .venv-mlx
source .venv-mlx/bin/activate
pip install -r mlx_host/requirements.txt
python mlx_host/mlx_openai_server.py
```

4. UI oeffnen:

```text
http://localhost:8080
```

5. Ersten Benutzer registrieren, Space anlegen und Dokumente hochladen.

## Empfohlene MVP-Defaults

- Chunk Size: `350`
- Chunk Overlap: `50`
- Retrieval K: `4`
- Embedding Model: `intfloat/multilingual-e5-small`
- Chat-LLM: `NexVeridian/Qwen3.5-4B-5bit`

## Persistente Daten

Alle Daten liegen unter:

```text
mvp/data/
```

Darin liegen:
- SQLite-Datenbank
- Uploads
- verarbeitete Dokumente
- Chroma-Daten

## MLX-Konfiguration

Die Standardwerte in [.env](/Users/markusadolph/Library/CloudStorage/OneDrive-EBF-EDVBeratungFöllmerGmbH/EBF RAG/mvp/.env) zeigen auf:

- `LLM_BASE_URL=http://host.docker.internal:8000/v1`
- `LLM_MODEL=NexVeridian/Qwen3.5-4B-5bit`

Wenn du spaeter ein anderes MLX-Modell testen willst, reicht es meist, nur `LLM_MODEL` anzupassen und den Host-Server neu zu starten.

## Nächste sinnvolle Ausbaustufen

- Entra SSO statt lokaler Anmeldung
- Hintergrundjobs fuer Ingestion
- Versions- und Reindex-Management
- Rollen und Space-Sharing
- besseres Prompting und Modell-Routing
