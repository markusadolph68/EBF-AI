# 🚀 Produktionsreife Ingestion-Pipeline für EBFfy
## Docling + Chroma + Metadaten + Update-Logik

---

## 🎯 Ziel

Eine robuste Pipeline, die Dokumente für RAG verarbeitet und dabei:

- **Docling** für strukturiertes Parsing nutzt
- **Chunking** sauber umsetzt
- **Metadaten** mitführt
- **Chroma** als Vektor-Datenbank befüllt
- **Updates** und Re-Indexierung kontrolliert behandelt

---

# 🧱 Zielarchitektur

```text
Dokumentenquelle
   ├── PDFs
   ├── DOCX
   ├── Markdown
   └── TXT
        ↓
Datei-Scanner
        ↓
Docling Parsing
        ↓
Normalisierung
        ↓
Chunking
        ↓
Metadaten-Anreicherung
        ↓
Embedding
        ↓
Chroma
        ↓
Open WebUI / LLM
```

---

# 🧠 Warum diese Pipeline wichtig ist

Ohne saubere Pipeline:
- schlechte Chunk-Grenzen
- zerstörte Tabellen
- doppelte Dokumente
- veraltete Inhalte im Index
- schwankende Antwortqualität

Mit sauberer Pipeline:
- bessere Retrieval-Treffer
- weniger Halluzinationen
- sauberere Quellenbasis
- reproduzierbare Qualität

---

# 📁 Empfohlene Ordnerstruktur

```text
~/ebf-ai-pilot/
├── documents/
│   ├── hr/
│   ├── vertrieb/
│   ├── projekte/
│   └── policies/
├── processed/
│   ├── parsed/
│   ├── chunks/
│   └── manifests/
├── chroma_data/
├── scripts/
│   ├── ingest.py
│   ├── reindex.py
│   └── utils.py
└── logs/
```

---

# ⚙️ Technische Bausteine

## 1. Parsing
**Docling** für:
- Layout
- Überschriften
- Tabellen
- Abschnitte

## 2. Speicherung
**Chroma** für:
- Embeddings
- Metadaten
- semantische Suche

## 3. Status / Update-Kontrolle
**Manifest-Datei je Dokument** für:
- Hash
- Version
- letzter Import
- Chunk-Anzahl
- Bereich

---

# 🧾 Metadatenmodell

Pro Chunk mindestens:

```json
{
  "source_file": "angebot_2026_01.pdf",
  "document_id": "angebot_2026_01",
  "area": "vertrieb",
  "title": "Angebot Managed AI Services",
  "version": "2026-01",
  "confidentiality": "internal",
  "chunk_index": 4,
  "section": "Leistungsumfang",
  "last_updated": "2026-03-22",
  "checksum": "sha256:..."
}
```

---

# ✂️ Chunking-Strategie

## Empfehlung
- **200–500 Tokens pro Chunk**
- leichter Overlap, z. B. **30–60 Tokens**
- Chunking an:
  - Überschriften
  - Absätzen
  - Tabellenblöcken

## Nicht empfehlenswert
- fixe 2.000-Zeichen-Blöcke ohne Struktur
- Tabellen mit Fließtext vermischen
- ganze Dokumente als ein Chunk

---

# 🔄 Update-Logik

## Ziel
Nur geänderte Dokumente neu indexieren.

## Vorgehen
1. Datei einlesen
2. SHA256-Hash berechnen
3. Manifest prüfen
4. nur bei Änderung:
   - alte Chunks löschen
   - neu parsen
   - neu chunken
   - neu in Chroma schreiben
   - Manifest aktualisieren

## Vorteil
- schnellere Re-Indexierung
- weniger Dubletten
- sauberer Datenbestand

---

# 🧪 Beispiel: Python-Workflow

```python
from pathlib import Path
import hashlib
import json
import chromadb
from docling import Document

BASE = Path("./documents")
MANIFEST_DIR = Path("./processed/manifests")
MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

client = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_or_create_collection("ebf_docs")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifest(doc_id: str):
    manifest_path = MANIFEST_DIR / f"{doc_id}.json"
    if manifest_path.exists():
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    return None


def save_manifest(doc_id: str, data: dict):
    manifest_path = MANIFEST_DIR / f"{doc_id}.json"
    manifest_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_with_docling(path: Path):
    doc = Document.from_file(str(path))
    structured = doc.to_dict()
    chunks = []

    for i, section in enumerate(structured.get("sections", [])):
        text = section.get("text", "").strip()
        if not text:
            continue
        chunks.append({
            "text": text,
            "section": section.get("title", f"section_{i}"),
            "chunk_index": i
        })

    return chunks


def upsert_document(path: Path, area: str):
    doc_id = path.stem
    checksum = sha256_file(path)
    manifest = load_manifest(doc_id)

    if manifest and manifest.get("checksum") == checksum:
        print(f"Skip unchanged: {path.name}")
        return

    # Alte Einträge löschen
    try:
        existing = collection.get(where={"document_id": doc_id})
        ids = existing.get("ids", [])
        if ids:
            collection.delete(ids=ids)
    except Exception:
        pass

    chunks = parse_with_docling(path)

    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:
        chunk_id = f"{doc_id}_{chunk['chunk_index']}"
        ids.append(chunk_id)
        documents.append(chunk["text"])
        metadatas.append({
            "document_id": doc_id,
            "source_file": path.name,
            "area": area,
            "section": chunk["section"],
            "chunk_index": chunk["chunk_index"],
            "checksum": checksum
        })

    if ids:
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

    save_manifest(doc_id, {
        "document_id": doc_id,
        "source_file": path.name,
        "area": area,
        "checksum": checksum,
        "chunk_count": len(ids)
    })

    print(f"Indexed: {path.name} ({len(ids)} chunks)")


for area_dir in BASE.iterdir():
    if not area_dir.is_dir():
        continue
    area = area_dir.name
    for file_path in area_dir.iterdir():
        if file_path.suffix.lower() in {".pdf", ".docx", ".md", ".txt"}:
            upsert_document(file_path, area)
```

---

# 🧰 Empfohlene Erweiterungen

## 1. Embeddings explizit steuern
Statt Defaults:
- einheitliches Embedding-Modell festlegen
- lokal oder API-basiert
- gleiche Strategie für alle Dokumente

## 2. Logging
Pro Lauf loggen:
- Anzahl Dokumente
- neu / übersprungen / Fehler
- Dauer
- Chunk-Anzahl

## 3. Fehlerordner
Fehlerhafte Dateien nach:
```text
processed/errors/
```
verschieben oder markieren

## 4. Soft Delete
Statt sofort zu löschen:
- Dokument als inaktiv markieren
- später bereinigen

---

# 🔐 Zugriff & Governance

Die Ingestion-Pipeline sollte die spätere Zugriffstrennung unterstützen.

## Empfehlung
Schon bei der Ingestion `area` und `confidentiality` sauber setzen:
- `hr`
- `vertrieb`
- `projekte`

Damit kannst du:
- Filter im Retrieval nutzen
- Knowledge Bases sauber trennen
- Entra-Gruppen später konsistent zuordnen

---

# 📊 Betriebsmodell

## Täglich oder manuell?
Für den Pilot:
- manuell oder 1x täglich

Für später:
- geplanter Lauf
- Delta-Import
- Review-Prozess für neue Dokumente

## Rollen
- **Content Owner**: fachlich verantwortlich
- **AI Admin**: Pipeline, Chroma, Open WebUI
- **Tester**: Qualitätsfeedback

---

# 🧪 Testkriterien

Bewerte regelmäßig:

- Wurde das richtige Dokument gefunden?
- Wurde der richtige Abschnitt gefunden?
- Ist die Antwort korrekt?
- Ist die Quelle nachvollziehbar?
- Gibt es Halluzinationen?
- Ist die Version aktuell?

---

# 🚀 Einführungsplan für EBF

## Phase 1
- 10–20 hochwertige Dokumente
- Docling nur für PDFs / DOCX
- manuelle Re-Indexierung

## Phase 2
- Manifest-Logik
- saubere Metadaten
- Logging
- Bereichstrennung

## Phase 3
- Delta-Imports
- Qualitätsmetriken
- Embedding-Standardisierung
- produktiver Betrieb

---

# 🧾 TL;DR

Für EBFfy sollte die produktionsreife RAG-Pipeline so aussehen:

- **Docling** für Parsing
- **strukturiertes Chunking**
- **saubere Metadaten**
- **Chroma** als Speicher
- **Manifest + Hashing** für Updates
- **Bereichstrennung** für Zugriffskontrolle

👉 Das ist einer der größten Qualitätshebel für dein gesamtes System.
