# EBF AI Phase 1 Zielarchitektur

## Ziel

Diese Zielarchitektur definiert die verbindliche Referenz fuer Phase 1 des EBF-AI-Piloten.
Phase 1 bedeutet:
- stabiler Betrieb
- sauberer Zugriff
- verlaessliche Wissensantworten

Nicht Teil von Phase 1 sind:
- Tool Layer
- Memory ueber Sessions
- tiefe Systemintegrationen

## Architekturentscheidung fuer Phase 1

Die Referenzarchitektur fuer Phase 1 ist:

1. Open WebUI als Frontend
2. lokaler OpenAI-kompatibler MLX-Server als Standard-LLM-Endpoint
3. Chroma als Vektor-Datenbank
4. Docling-basierte Ingestion-Pipeline fuer Dokumente
5. Entra OIDC mit Gruppen-Sync fuer Zugriffstrennung

## Bevorzugte Komponenten

### Frontend
- Open WebUI

Begruendung:
- schnelle Bereitstellung
- RAG- und Benutzeroberflaeche bereits passend zum Pilot
- gut kombinierbar mit OIDC und lokalen OpenAI-kompatiblen Endpoints

### Lokaler Modellserver
- robuste MLX/OpenAI-Server-Variante aus `02_setup/2_ebf-macmini-pilot-mlx-openai-server.md`

Begruendung:
- Open WebUI erwartet typischerweise `/v1/models` und `/v1/chat/completions`
- die Minimalvariante ist fuer Pilotbetrieb zu knapp

### Standardmodell lokal
- Qwen3.5-9B als Ziel-Standard fuer den Pilot

Begruendung:
- laut bestehender Bewertung besseres Verhaeltnis aus Qualitaet und Laufzeit
- ausreichend fuer Phase-1-Wissensassistent

Hinweis:
- falls Qwen3.5-9B lokal nicht stabil laeuft, ist Llama 3.x 8B der Fallback fuer Vergleich und Betrieb

### Cloud-Modell
- in Phase 1 optional, nicht Standardpfad

Begruendung:
- zuerst muss der lokale Wissensassistent belastbar werden
- Cloud-Routing wird erst in Phase 2 relevant

### Vektor-Datenbank
- Chroma persistent lokal

### Dokumentverarbeitung
- Docling fuer Parsing
- manifestgesteuerte Reindexierung
- Chunking anhand von Struktur statt fixer Zeichenbloecke

### Zugriff
- Entra OIDC
- Group Sync in Open WebUI
- getrennte Knowledge Bases pro Bereich

## Zielbild als Datenfluss

```text
Nutzer
  ↓
Microsoft Entra Login
  ↓
Open WebUI
  ↓
OpenAI-kompatibler MLX-Server
  ↓
RAG-Retrieval gegen Chroma
  ↓
Dokument-Chunks mit Metadaten
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
- getrennte Knowledge Base oder gleichwertige Zugriffstrennung

## Betriebsmodell fuer Phase 1

### Laufende Komponenten
- `open-webui`
- `chroma`
- `mlx_openai_server`

### Persistente Daten
- `openwebui_data/`
- `chroma_data/`
- `processed/manifests/`

### Quellordner
- `documents/hr/`
- `documents/vertrieb/`
- `documents/projekte/`
- optional `documents/policies/`

## Healthchecks

Folgende Pruefungen sind fuer Phase 1 verbindlich:

### Open WebUI
- UI erreichbar
- Login moeglich
- Modellprovider sichtbar

### MLX-Server
- `GET /health`
- `GET /v1/models`
- `POST /v1/chat/completions`

### Chroma
- Heartbeat oder gleichwertige API-Pruefung
- Collection erreichbar

### Zugriff
- Testnutzer mit Gruppe sieht nur erlaubte Knowledge Bases
- Testnutzer ohne Gruppe sieht keinen unberechtigten Bereich

## Konfigurationsentscheidungen

### Open WebUI
- OIDC aktiv
- Group Management aktiv
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

## Was in Phase 1 bewusst noch nicht optimiert wird

- komplexes Modell-Routing
- agentische Workflows
- Tool-Ausfuehrung
- Personalisierung und Memory
- KPI-Dashboard mit Vollmonitoring

## Architektur-Freigabe fuer Phase 1

Phase 1 sollte als technisch freigegeben gelten, wenn:
- die drei Kernkomponenten reproduzierbar starten
- Open WebUI mit dem robusten MLX-Endpoint stabil spricht
- Pilotdokumente strukturiert in Chroma landen
- Zugriffstrennung ueber Entra-Gruppen funktioniert
- Testfragen ueber denselben Prozess wiederholt pruefbar sind
