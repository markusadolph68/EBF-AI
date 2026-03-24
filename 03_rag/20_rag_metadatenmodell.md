# EBF RAG Metadatenmodell

## Ziel

Dieses Metadatenmodell definiert die Pflicht- und Sollfelder fuer Dokumente und Chunks im Phase-1-Pilot.
Es dient drei Zielen:
- bessere Retrieval-Qualitaet
- saubere Update-Logik
- spaetere Zugriffstrennung

## Grundsatz

Metadaten werden auf zwei Ebenen betrachtet:
- Dokumentebene
- Chunk-Ebene

Dokumentebene beschreibt die Quelle als Ganzes.
Chunk-Ebene beschreibt den konkreten Abschnitt, der in Chroma gespeichert wird.

## Pflichtfelder auf Dokumentebene

| Feld | Typ | Beispiel | Zweck |
|------|-----|----------|-------|
| `document_id` | string | `angebot_managed_ai_2026_01` | stabile Dokument-ID |
| `source_file` | string | `angebot_managed_ai_2026_01.pdf` | Ursprungsdatei |
| `source_path` | string | `documents/vertrieb/angebot_managed_ai_2026_01.pdf` | fachliche Herkunft |
| `area` | string | `vertrieb` | Bereichstrennung |
| `title` | string | `Angebot Managed AI Services` | fachlicher Titel |
| `version` | string | `2026-01` | Versionsbezug |
| `confidentiality` | string | `internal` | Schutzklasse |
| `checksum` | string | `sha256:...` | Aenderungserkennung |
| `last_updated` | string | `2026-03-22` | fachlicher Aktualitaetsstand |
| `ingested_at` | string | `2026-03-24T11:30:00Z` | technischer Importzeitpunkt |

## Pflichtfelder auf Chunk-Ebene

| Feld | Typ | Beispiel | Zweck |
|------|-----|----------|-------|
| `chunk_id` | string | `angebot_managed_ai_2026_01_004` | eindeutige Chunk-ID |
| `document_id` | string | `angebot_managed_ai_2026_01` | Bezug zum Dokument |
| `source_file` | string | `angebot_managed_ai_2026_01.pdf` | Rueckverfolgbarkeit |
| `area` | string | `vertrieb` | Filterung im Retrieval |
| `confidentiality` | string | `internal` | Zugriff und Governance |
| `chunk_index` | integer | `4` | Reihenfolge im Dokument |
| `section` | string | `Leistungsumfang` | fachlicher Kontext |
| `checksum` | string | `sha256:...` | Konsistenz zum Dokument |

## Sollfelder

| Feld | Typ | Beispiel | Zweck |
|------|-----|----------|-------|
| `document_type` | string | `angebot` | spaetere Filter |
| `owner` | string | `vertrieb` | inhaltliche Verantwortung |
| `language` | string | `de` | Mehrsprachigkeit |
| `kb_name` | string | `kb-vertrieb` | Zuordnung zur Knowledge Base |
| `tags` | string[] | `["managed-services","ai"]` | fachliche Suche |
| `page_from` | integer | `7` | Quellenbezug bei PDF |
| `page_to` | integer | `8` | Quellenbezug bei PDF |

## Feldregeln

### `document_id`
- stabil und ohne Leerzeichen
- bevorzugt aus Dateiname plus Version ableiten
- darf sich nicht pro Importlauf aendern

### `area`
Nur definierte Werte verwenden:
- `hr`
- `vertrieb`
- `projekte`
- `policies`

### `confidentiality`
Fuer Phase 1 genuegen diese Werte:
- `public-internal`
- `internal`
- `restricted`

Empfehlung:
- Standard ist `internal`
- sensible HR- oder Projektinhalte als `restricted`

### `version`
- kein Freitext
- bevorzugt `YYYY-MM` oder fachliche Dokumentversion

### `section`
- wenn moeglich aus Docling-Ueberschrift ableiten
- bei fehlender Struktur technisch sinnvoll benennen, zum Beispiel `section_04`

## Beispiel Dokument-Metadaten

```json
{
  "document_id": "angebot_managed_ai_2026_01",
  "source_file": "angebot_managed_ai_2026_01.pdf",
  "source_path": "documents/vertrieb/angebot_managed_ai_2026_01.pdf",
  "area": "vertrieb",
  "title": "Angebot Managed AI Services",
  "version": "2026-01",
  "confidentiality": "internal",
  "checksum": "sha256:8f7c...",
  "last_updated": "2026-03-22",
  "ingested_at": "2026-03-24T11:30:00Z",
  "document_type": "angebot",
  "owner": "vertrieb",
  "language": "de",
  "kb_name": "kb-vertrieb",
  "tags": ["managed-services", "ai"]
}
```

## Beispiel Chunk-Metadaten

```json
{
  "chunk_id": "angebot_managed_ai_2026_01_004",
  "document_id": "angebot_managed_ai_2026_01",
  "source_file": "angebot_managed_ai_2026_01.pdf",
  "area": "vertrieb",
  "confidentiality": "internal",
  "chunk_index": 4,
  "section": "Leistungsumfang",
  "checksum": "sha256:8f7c...",
  "page_from": 7,
  "page_to": 8
}
```

## Mindestanforderung fuer Chroma

Jeder in Chroma gespeicherte Chunk muss mindestens haben:
- `document_id`
- `source_file`
- `area`
- `confidentiality`
- `section`
- `chunk_index`
- `checksum`

Ohne diese Felder soll ein Chunk im Pilot nicht geschrieben werden.

## Nutzung im Retrieval

Die Metadaten muessen spaeter mindestens fuer diese Zwecke nutzbar sein:
- Filter nach `area`
- Filter nach `confidentiality`
- Quellenanzeige ueber `source_file` und `section`
- Reindexierung ueber `document_id` und `checksum`

## Nutzung im Betrieb

Das Manifest pro Dokument sollte mindestens spiegeln:
- `document_id`
- `source_file`
- `area`
- `checksum`
- `version`
- `chunk_count`
- `ingested_at`

## Freigaberegel fuer Phase 1

Das Metadatenmodell ist fuer Phase 1 einsatzbereit, wenn:
- alle Pilotdokumente die Pflichtfelder erhalten
- Chroma-Chunks die Mindestfelder mitfuehren
- das Feld `area` konsistent zur Zugriffstrennung passt
- Aenderungen ueber `checksum` eindeutig erkannt werden
