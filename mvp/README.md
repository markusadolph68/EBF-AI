# EBF AI MVP

Referenz-MVP auf Basis von:
- Open WebUI als Benutzeroberflaeche
- hostseitigem MLX/OpenAI-kompatiblem Modellserver
- Chroma als Vektor-Datenbank
- Docling-basierter, headless Ingestion nach Chroma

Wichtig:
- Entra ist bewusst **nicht** Teil dieses Baselineschritts.
- Zuerst wird ein lokal reproduzierbarer Pilot mit Open WebUI + MLX + Chroma stabilisiert.
- Entra folgt spaeter als letzter Integrationsschritt.

## Architektur

- `docker-compose.yml`: Open WebUI und Chroma
- `mlx_host/`: hostseitiger MLX/OpenAI-kompatibler Server fuer Apple Silicon
- `ingest/`: headless Ingestion von `documents/` nach Chroma
- `scripts/`: Start-, Stop-, Healthcheck- und Ingestion-Skripte

## Wichtiger Mac-Hinweis

Open WebUI und Chroma laufen in Docker.
Der Modellserver laeuft absichtlich auf dem Host, weil MLX/Metal unter macOS nicht sinnvoll im Linux-Container laeuft.

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

6. In Open WebUI den Provider anlegen:
- Typ: `OpenAI-compatible`
- Base URL: `http://host.docker.internal:8000/v1`
- API Key: `mlx`
- Modell: Wert aus `MLX_MODEL_NAME`

## Dokumente und Ingestion

Pilotdokumente liegen unter:

```text
mvp/documents/hr/
mvp/documents/vertrieb/
mvp/documents/projekte/
```

Optional kann pro Dokument eine Sidecar-Datei `<datei>.metadata.json` abgelegt werden, um Felder wie `title`, `version`, `confidentiality`, `document_type`, `owner`, `kb_name` oder `tags` zu setzen.

Die headless Ingestion nach Chroma startest du so:

```bash
./scripts/ingest_documents.sh
```

Dabei werden:
- Texte mit Docling extrahiert
- Chunks erzeugt
- Pflichtmetadaten gesetzt
- Manifeste unter `mvp/processed/manifests/` geschrieben

## Healthchecks

Folgende Checks sind vorgesehen:
- Open WebUI ueber `http://localhost:3000/`
- Chroma Heartbeat ueber Port `8001`
- MLX-Server ueber `http://localhost:8000/health`
- Modellliste ueber `http://localhost:8000/v1/models`

## Projektstruktur

```text
mvp/
├── .env.example
├── docker-compose.yml
├── documents/
│   ├── hr/
│   ├── vertrieb/
│   └── projekte/
├── ingest/
│   ├── ingest_documents.py
│   └── requirements.txt
├── mlx_host/
│   ├── mlx_openai_server.py
│   └── requirements.txt
├── processed/
│   └── manifests/
└── scripts/
    ├── healthcheck.sh
    ├── ingest_documents.sh
    ├── start_mlx_host.sh
    ├── start_stack.sh
    └── stop_stack.sh
```

## Status

Der alte FastAPI-Prototyp unter `mvp/app/` bleibt vorerst als Referenz erhalten, ist aber **nicht mehr** der Default-Pfad fuer den Pilot.

## Naechste sinnvolle Ausbaustufen

- kuratierte Pilotdokumente je Bereich festziehen
- Open-WebUI-Knowledge-Base-Setup und RAG-Prozess operationalisieren
- Testkatalog gegen echte Pilotdaten fahren
- Prompt-Standards und Antwortformate schrittweise vereinheitlichen
- Entra erst nach stabilem lokalen Pilot anschliessen
