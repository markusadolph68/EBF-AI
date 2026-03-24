# EBF Pilot Setup auf Mac mini M4 (64 GB)

## Ziel
Lokaler Pilot mit:
- **MLX** für Inferenz auf Apple Silicon
- **Open WebUI** als Oberfläche
- **Chroma** als lokale Vektor-Datenbank
- optional **RunPod L40S** als Cloud-Backend

## Schnellstart
1. Homebrew, Python und Docker installieren
2. `cp .env.example .env`
3. Python-Pakete installieren:
   ```bash
   python3 -m pip install --upgrade pip
   python3 -m pip install mlx mlx-lm fastapi uvicorn chromadb pydantic
   ```
4. Docker Desktop starten
5. Dienste starten:
   ```bash
   ./scripts/start.sh
   ```
6. Open WebUI öffnen:
   `http://localhost:3000`

## Provider in Open WebUI
- Type: `OpenAI-compatible`
- Base URL: `http://host.docker.internal:8000/v1`
- API Key: `mlx`

## Projektstruktur
```text
ebf-ai-pilot/
├── README.md
├── .env.example
├── docker-compose.yml
├── app/
│   ├── mlx_server.py
│   └── mlx_openai_server.py
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
