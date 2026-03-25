# EBF AI MVP

OpenWebUI-basierter MVP fuer den lokalen Pilot auf dem Mac Mini M4.

Standardpfad:
- Open WebUI als Benutzeroberflaeche
- hostseitiger MLX/OpenAI-kompatibler Modellserver
- Chroma als separater HTTP-Vektorstore
- Dokument-Upload und Knowledge-Bases primaer ueber Open WebUI

Nicht Teil dieses Schritts:
- Entra / OIDC
- Mehrbenutzer-Governance
- produktive Automatisierung

## Architektur

- `docker-compose.yml`: Open WebUI plus Chroma
- `mlx_host/`: hostseitiger MLX/OpenAI-kompatibler Server fuer Apple Silicon
- `scripts/start_stack.sh`: startet Open WebUI und Chroma
- `scripts/start_mlx_host.sh`: startet den MLX-Server auf dem Host
- `scripts/healthcheck.sh`: prueft Open WebUI, Chroma und MLX

Optional:
- `ingest/`: experimentelle headless Ingestion direkt nach Chroma
- `app/`: alter FastAPI-Prototyp, nicht mehr der Default-Pfad

## Warum dieser Aufbau

Open WebUI wird laut offizieller Doku mit Chroma als separatem HTTP-Service betrieben, wenn mehrere Worker oder saubere Container-Trennung gewuenscht sind. Dafuer werden `VECTOR_DB=chroma` sowie `CHROMA_HTTP_HOST` und `CHROMA_HTTP_PORT` gesetzt. Fuer OpenAI-kompatible Backends werden `OPENAI_API_BASE_URL(S)` und `OPENAI_API_KEY` verwendet.

Verwendete Open-WebUI-Doku:
- [Quick Start](https://docs.openwebui.com/getting-started/quick-start/)
- [Environment Configuration](https://docs.openwebui.com/reference/env-configuration/)
- [OpenAI-Compatible Provider Setup](https://docs.openwebui.com/getting-started/quick-start/connect-a-provider/starting-with-openai-compatible/)

## Wichtiger Mac-Hinweis

Open WebUI und Chroma laufen in Docker.
Das Chat-Modell laeuft absichtlich auf dem Host, weil MLX/Metal unter macOS nicht sinnvoll als Linux-Container betrieben wird.

## Schnellstart

1. Konfiguration vorbereiten:

```bash
cd mvp
cp .env.example .env
```

2. Open WebUI und Chroma starten:

```bash
./scripts/start_stack.sh
```

3. MLX-Server auf dem Host starten:

```bash
./scripts/start_mlx_host.sh
```

4. Healthchecks laufen lassen:

```bash
./scripts/healthcheck.sh
```

5. Open WebUI oeffnen:

```text
http://localhost:3000
```

## Open WebUI im Pilot benutzen

Nach dem Start:

1. ersten lokalen Benutzer in Open WebUI anlegen
2. unter `Admin > Settings > Connections` pruefen, ob der OpenAI-kompatible Endpoint vorhanden ist
3. Modell `NexVeridian/Qwen3.5-4B-5bit` auswaehlen
4. fuer RAG in Open WebUI eigene Knowledge Bases / Workspaces anlegen
5. Dokumente ueber die Open-WebUI-Oberflaeche hochladen

Wichtig:
- Der MVP-Standardpfad fuer Wissen ist jetzt der Upload ueber Open WebUI.
- Die headless Ingestion unter `scripts/ingest_documents.sh` bleibt optional und schreibt nur direkt nach Chroma. Sie erzeugt keine Open-WebUI-Knowledge-Base-Eintraege.

## Persistenz

Persistente Daten liegen unter:

```text
mvp/data/
├── open-webui/
└── chromadb/
```

Das bedeutet:
- `docker compose down` behaelt Daten
- das Loeschen von `mvp/data/` loescht Open-WebUI- und Chroma-Zustand

## Dokumentordner

Fuer den Pilot bleiben diese Ordner als Ablage und Ingestion-Quelle vorhanden:

```text
mvp/documents/hr/
mvp/documents/vertrieb/
mvp/documents/projekte/
```

Sie sind fuer:
- kuratierte Pilotdokumente
- spaetere Reindex-/Importpfade
- optionale headless Ingestion

## Healthchecks

Die Skripte pruefen:
- Open WebUI unter `http://localhost:3000/`
- Chroma Heartbeat ueber Port `8001`
- MLX unter `http://localhost:8000/health`
- Modellliste unter `http://localhost:8000/v1/models`

## Projektstruktur

```text
mvp/
├── .env.example
├── docker-compose.yml
├── documents/
├── ingest/
├── mlx_host/
├── processed/
├── scripts/
├── data/
└── app/   # alter FastAPI-Prototyp, nicht Standard
```

## Nächste sinnvolle Ausbaustufen

- Open-WebUI-Knowledge-Bases fachlich strukturieren
- kuratierte Pilotdokumente je Bereich festziehen
- Reindex-/Recovery-Pfad fuer Chroma absichern
- Antwortqualitaet mit Testkatalog gegen echte Pilotdaten messen
- Entra erst nach stabilem lokalen Pilot anschliessen
