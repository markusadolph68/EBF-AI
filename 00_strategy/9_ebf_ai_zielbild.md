# EBF AI-Zielbild
## Vom Wissenschatbot zur AI-Plattform

## Ausgangssituation

EBF baut aktuell einen internen AI-Assistenten mit:

- Open WebUI
- RAG (Chroma)
- lokalen Modellen (MLX)
- optional spaeter Cloud-Erweiterungen

Ergebnis heute:
**Funktionierender Wissenschatbot**

## Zentrale Erkenntnis

Der Unterschied zu ChatGPT liegt nicht im Modell,
sondern in der Systemarchitektur drumherum.

## Reifegradmodell

### Stufe 1 - Wissenschatbot
- beantwortet Fragen
- nutzt interne Dokumente
- liefert erste Produktivitaet

### Stufe 2 - Arbeitsassistent
- strukturierte Antworten
- Templates fuer Angebote und Analysen
- Kontext pro Aufgabe
- Modell-Routing lokal plus optional Cloud

### Stufe 3 - AI-Plattform
- fuehrt Aktionen aus
- integriert Systeme
- merkt sich Kontext und Nutzerverhalten
- ist messbar und steuerbar

## Was konkret noch fehlt

### 1. Tool Layer
- APIs anbinden
- Aktionen ausfuehren statt nur antworten

### 2. Orchestrierung
- strukturierte Prompts
- Rollenlogik
- Antwortstandards

### 3. Memory
- Nutzerkontext
- Verlauf ueber Sessions

### 4. Retrieval-Qualitaet
- bessere Dokumentstruktur
- Metadaten
- praezisere Treffer

### 5. Monitoring & Governance
- Qualitaet messen
- Nutzung verstehen
- Kontrolle und Compliance

## Zielarchitektur (vereinfacht)

```text
Open WebUI (Frontend)
        ↓
Orchestrierung / Prompt Layer
        ↓
RAG (Chroma, strukturierte Daten)
        ↓
LLM (MLX lokal, spaeter optional Cloud)
        ↓
Tools / APIs (zukuenftig)
```

## Empfohlene Roadmap

### Phase 1 (jetzt)
- Open WebUI + MLX + Chroma stabilisieren
- RAG stabilisieren
- Datenqualitaet erhoehen
- Testkatalog aufbauen

### Phase 2
- Templates und Arbeitslogik
- Modell-Routing
- bessere Outputs

### Phase 3
- Entra und Unternehmenszugriff anschliessen
- Tool Layer
- Integration in Systeme
- Monitoring und Governance

## Strategischer Vorteil fuer EBF

- Wissen wird strukturiert nutzbar
- Prozesse werden teilautomatisiert
- Mitarbeiter werden produktiver
- AI wird integrierter Bestandteil der Arbeit

## TL;DR

Heute:
**Guter Wissenschatbot**

Ziel:
**AI-gestuetzte Arbeitsplattform**

Schluessel:
- nicht das Modell
- sondern die Architektur
