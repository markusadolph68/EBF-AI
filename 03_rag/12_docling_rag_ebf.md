# 📄 Docling Integration für EBFfy (RAG-Upgrade)

## 🎯 Ziel
Verbesserung der RAG-Qualität durch strukturierte Dokumentverarbeitung mit **Docling**.

---

# 🧠 Warum Docling?

Ohne strukturierte Verarbeitung:
- PDFs verlieren Struktur
- Tabellen werden zerstört
- Kontext geht verloren

👉 Ergebnis:
- schlechter Retrieval
- mehr Halluzinationen

Mit Docling:
- erkennt Layout & Abschnitte
- extrahiert Tabellen korrekt
- erzeugt strukturierte Daten (JSON/Markdown)

👉 Ergebnis:
- deutlich bessere Antworten

---

# 🏗️ Zielarchitektur

```text
Dokumente (PDF, DOCX)
        ↓
Docling (Parsing)
        ↓
Chunking + Metadaten
        ↓
Chroma (Vector DB)
        ↓
Open WebUI
        ↓
LLM
```

---

# ⚙️ Installation

```bash
pip install docling chromadb
```

---

# 🧪 Beispiel-Pipeline

```python
from docling import Document
import chromadb

doc = Document.from_file("angebot.pdf")
structured = doc.to_dict()

client = chromadb.Client()
collection = client.get_or_create_collection("ebf_docs")

chunks = []
for section in structured.get("sections", []):
    text = section.get("text", "")
    if text:
        chunks.append(text)

for i, chunk in enumerate(chunks):
    collection.add(
        documents=[chunk],
        ids=[f"doc_{i}"]
    )
```

---

# 🧠 Best Practices

- Chunking: 200–500 Tokens
- Metadaten nutzen
- saubere Dokumente verwenden

---

# 🚀 Einführungsstrategie

Phase 1: wichtige PDFs  
Phase 2: komplette Pipeline

---

# 🧾 TL;DR

👉 Docling verbessert massiv die RAG-Qualität
