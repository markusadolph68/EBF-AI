# EBF AI Phase 1 Zielarchitektur

## Ziel

Diese Zielarchitektur definiert die verbindliche Referenz fuer Phase 1 des EBF-AI-Piloten.
Phase 1 bedeutet:
- stabiler Betrieb
- schlanke lokale Pilotnutzung ohne SSO-Abhaengigkeit
- verlaessliche Wissensantworten

Nicht Teil von Phase 1 sind:
- Entra OIDC und Group Sync
- Tool Layer
- Memory ueber Sessions
- tiefe Systemintegrationen

## Architekturentscheidung fuer Phase 1

Die Referenzarchitektur fuer Phase 1 ist:

1. Open WebUI als Frontend
2. lokaler OpenAI-kompatibler MLX-Server als Standard-LLM-Endpoint
3. Chroma als Vektor-Datenbank
4. Docling-basierte Ingestion-Pipeline fuer Dokumente
5. lokale Open-WebUI-Accounts und manueller Admin-Betrieb als Pilot-Baseline

## Bevorzugte Komponenten

### Frontend
- Open WebUI

Begruendung:
- schnelle Bereitstellung
- passende UI fuer Chat, Provider und spaetere Knowledge-Base-Verwaltung
- gut kombinierbar mit lokalen OpenAI-kompatiblen Endpoints

### Lokaler Modellserver
- robuste MLX/OpenAI-Server-Variante aus `02_setup/2_ebf-macmini-pilot-mlx-openai-server.md`

Begruendung:
- Open WebUI erwartet typischerweise `/v1/models` und `/v1/chat/completions`
- die Minimalvariante ist fuer Pilotbetrieb zu knapp

### Standardmodell lokal
- Qwen3.5-4B-5bit als sichere Startkonfiguration fuer den Pilot

Begruendung:
- niedrigeres Betriebsrisiko auf Apple Silicon
- ausreichend fuer den ersten stabilen Wissensassistenten

Hinweis:
- nach erfolgreicher Stabilisierung kann auf ein staerkeres lokales Modell hochgeruestet werden

### Cloud-Modell
- in Phase 1 optional, nicht Standardpfad

Begruendung:
- zuerst muss der lokale Wissensassistent belastbar werden
- Cloud-Routing wird erst spaeter relevant

### Vektor-Datenbank
- Chroma persistent lokal

### Dokumentverarbeitung
- Docling fuer Parsing
- manifestgesteuerte Reindexierung
- Chunking anhand von Struktur statt fixer Zeichenbloecke

### Zugriff
- lokale Open-WebUI-Accounts
- manuell freigegebene Bereiche oder Knowledge Bases
- Entra bewusst erst nach stabilem Pilotbetrieb

## Zielbild als Datenfluss

```text
Nutzer
  ↓
Lokaler Open WebUI Login
  ↓
Open WebUI
  ↓
OpenAI-kompatibler MLX-Server
  ↓
Antwort an den Nutzer
```

## Ingestion-Datenfluss

```text
Dokumentenquellen
  ↓
Datei-Scanner
  ↓
Docling Parsing
  ↓
Normalisierung
  ↓
Chunking
  ↓
Metadaten
  ↓
Embeddings
  ↓
Chroma
```

## Verbindliche Bereiche fuer Phase 1

Mindestens diese Trennung ist vorgesehen:
- `hr`
- `vertrieb`
- `projekte`

Optional zusaetzlich:
- `policies`

Jeder Bereich bekommt:
- definierte Quelldokumente
- eigene Metadatenkennzeichnung
- getrennte Collection oder gleichwertige technische Trennung
- spaetere Zuordnung zu Open-WebUI-Knowledge-Bases

## Betriebsmodell fuer Phase 1

### Laufende Komponenten
- `open-webui`
- `chroma`
- `mlx_openai_server`
- `ingest_documents.py` als kontrollierter Batch-Prozess

### Persistente Daten
- `mvp/data/openwebui/`
- `mvp/data/chroma/`
- `mvp/processed/manifests/`

### Quellordner
- `mvp/documents/hr/`
- `mvp/documents/vertrieb/`
- `mvp/documents/projekte/`
- optional `mvp/documents/policies/`

## Healthchecks

Folgende Pruefungen sind fuer Phase 1 verbindlich:

### Open WebUI
- UI erreichbar
- lokaler Admin-Login moeglich
- Modellprovider konfigurierbar

### MLX-Server
- `GET /health`
- `GET /v1/models`
- `POST /v1/chat/completions`
- optional `POST /v1/completions`

### Chroma
- Heartbeat oder gleichwertige API-Pruefung
- Collections erreichbar

### Zugriff
- lokaler Standardnutzer kann den Pilot nutzen
- Adminrechte sind bewusst knapp vergeben
- Entra ist noch kein Abnahmekriterium

## Konfigurationsentscheidungen

### Open WebUI
- lokale Authentifizierung aktiv
- zunaechst nur wenige Pilotnutzer
- minimale Default-Rechte

### Modellanbindung
- OpenAI-kompatibler lokaler Endpoint
- ein Standardmodell fuer Phase 1
- kein produktiver Mischbetrieb ohne definierte Routing-Regeln

### RAG
- nur kuratierte Pilotdokumente
- Chunking nach Struktur
- Metadaten je Chunk verpflichtend
- Reindexierung nur kontrolliert

### Zugriff
- keine Abhaengigkeit von Entra fuer Phase 1
- lokale Pilotnutzung zuerst
- Entra als letzter Integrationsschritt nach erfolgreicher Stabilisierung

## Was in Phase 1 bewusst noch nicht optimiert wird

- Entra OIDC und Gruppen-Sync
- komplexes Modell-Routing
- agentische Workflows
- Tool-Ausfuehrung
- Personalisierung und Memory
- KPI-Dashboard mit Vollmonitoring

## Architektur-Freigabe fuer Phase 1

Phase 1 sollte als technisch freigegeben gelten, wenn:
- die drei Kernkomponenten reproduzierbar starten
- Open WebUI mit dem MLX-Endpoint stabil spricht
- Pilotdokumente strukturiert in Chroma landen
- die lokale Pilotnutzung ohne Spezialwissen bedienbar ist
- Testfragen ueber denselben Prozess wiederholt pruefbar sind
