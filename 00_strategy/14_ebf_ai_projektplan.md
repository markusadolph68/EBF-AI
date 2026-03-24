# EBF AI Projektplan

## 1. Projektziel

EBF baut keinen reinen Wissenschatbot, sondern schrittweise eine interne AI-Plattform.

Der aktuelle Stand ist:
- Open WebUI als Frontend
- RAG mit Chroma
- lokale und Cloud-Modelle
- erste Zugriffskontrolle ueber Entra

Das Zielbild ist:
- verlaesslicher Wissensassistent
- produktiver Arbeitsassistent
- spaeter AI-Plattform mit Tools, Governance und Monitoring

## 2. Projektlogik

Das Projekt sollte nicht nach Tools organisiert werden, sondern nach Wertstroemen:

1. Plattform
2. Wissen und RAG
3. Nutzer und Zugriff
4. Arbeitslogik und Use Cases
5. Betrieb und Governance

So bleibt klar, was technisch gebaut wird, warum es gebraucht wird und wie der Pilot produktionsreif wird.

## 3. Empfohlene Projektstruktur

### Stream A - Plattform
Ziel: stabile technische Basis fuer den Pilot.

Inhalte:
- Mac mini / Laufzeitumgebung
- MLX oder alternativer lokaler OpenAI-kompatibler Endpoint
- Open WebUI
- Chroma
- Deployment-, Start- und Backup-Logik

Deliverables:
- dokumentierte Zielarchitektur
- einheitliche Ordnerstruktur
- reproduzierbares Setup
- Healthchecks fuer alle Kernkomponenten

### Stream B - Wissen und RAG
Ziel: verlaessliche Wissensbasis statt "funktioniert manchmal".

Inhalte:
- Dokumentquellen definieren
- Parsing mit Docling
- Chunking-Strategie
- Metadatenmodell
- Reindex- und Update-Logik
- Testfragen und Qualitaetsmessung

Deliverables:
- definierte Quellordner
- Ingestion-Pipeline
- Manifest-Logik
- Referenzsatz mit 10-20 guten Dokumenten
- Testkatalog fuer Retrieval und Antwortqualitaet

### Stream C - Nutzer und Zugriff
Ziel: richtige Inhalte fuer die richtigen Gruppen.

Inhalte:
- Entra App Registration
- Gruppenmodell
- Login und Group Sync in Open WebUI
- Bereichstrennung fuer Knowledge Bases

Deliverables:
- Entra Gruppenmodell
- dokumentierte Berechtigungslogik
- getrennte Knowledge Bases fuer sensible Bereiche
- Testfaelle fuer Zugriffsrechte

### Stream D - Arbeitslogik und Use Cases
Ziel: vom Chatbot zum Arbeitsassistenten.

Inhalte:
- priorisierte Anwendungsfaelle
- Systemprompts
- Antworttemplates
- strukturierte Ausgabeformate
- Modell-Routing lokal vs. Cloud

Deliverables:
- Top-3 Pilot-Use-Cases
- Prompt- und Output-Standards
- definierte Regeln fuer Modellwahl
- messbarer Nutzwert pro Use Case

### Stream E - Betrieb und Governance
Ziel: kontrollierbarer und skalierbarer Betrieb.

Inhalte:
- Logging
- Monitoring
- Rollen und Verantwortungen
- Reviewprozess fuer neue Inhalte
- Datenschutz, Compliance und Freigaben

Deliverables:
- einfaches Betriebsmodell
- Rollenmatrix
- Qualitaets- und Freigabeprozess
- KPI-Set fuer Pilotbewertung

## 4. Phasenmodell

### Phase 1 - Pilot stabilisieren
Ziel: verlaesslicher Wissensassistent.

Prioritaet:
- Setup vereinheitlichen
- RAG-Quellen bereinigen
- Metadaten und Chunking festlegen
- Zugriffskontrolle fuer Bereiche aufsetzen
- Testkatalog anlegen

Ergebnis:
- funktionierender, reproduzierbarer Pilot
- bessere Antwortqualitaet
- geringeres Fehlerrisiko

### Phase 2 - Arbeitsassistent aufbauen
Ziel: messbare Unterstuetzung fuer konkrete Aufgaben.

Prioritaet:
- 2 bis 3 Kern-Use-Cases priorisieren
- Prompt-Orchestrierung einfuehren
- Templates fuer Antworten definieren
- Modell-Routing und Output-Standards einfuehren

Ergebnis:
- konsistentere Antworten
- direkte Arbeitserleichterung
- klarer Fachnutzen

### Phase 3 - Plattform erweitern
Ziel: Richtung AI-Plattform gehen.

Prioritaet:
- Tool Layer vorbereiten
- API-Integrationen bewerten
- Memory-Konzept definieren
- Monitoring und Governance ausbauen

Ergebnis:
- Assistent kann nicht nur antworten, sondern spaeter handeln
- Basis fuer Produktivbetrieb

## 5. Priorisierte Arbeitspakete

### Sofort sinnvoll
1. Zielordner und Artefakte konsolidieren
2. Zielarchitektur auf einer Seite festziehen
3. Dokumentquellen fuer den Pilot auswaehlen
4. Metadatenmodell und Chunking-Regeln festlegen
5. Entra-Gruppen und Knowledge-Base-Schnitt definieren
6. Testfragen je Bereich erstellen

### Danach
1. Ingestion-Pipeline produktionsnah aufsetzen
2. Rollen und Betriebsmodell festlegen
3. Top-Use-Cases mit Fachbereich abstimmen
4. Prompt-Standards und Templates bauen

### Spaeter
1. APIs und Tool Layer priorisieren
2. Monitoring und KPI-Dashboard aufbauen
3. Memory-Ansatz und Personalisierung pruefen

## 6. Minimale Projektorganisation

Empfohlene Rollen:
- Sponsor: priorisiert Nutzen und Budget
- AI Admin: Plattform, Setup, Betrieb
- Content Owner je Bereich: Inhalte und Freigabe
- Fachtester: bewertet Antworten und Use Cases

Empfohlener Rhythmus:
- 1x pro Woche Technik-Review
- 1x pro Woche Fachreview mit Testfragen
- 1 gemeinsames Pilotboard mit offenen Punkten, Risiken und Entscheidungen

## 7. Erfolgskriterien fuer den Pilot

Der Pilot ist erfolgreich, wenn:
- das Setup reproduzierbar startet
- die wichtigsten Dokumente sauber indexiert sind
- Zugriffe pro Bereich korrekt funktionieren
- Testfragen ueberwiegend korrekt beantwortet werden
- mindestens 2 Use Cases echten Zeitgewinn liefern

## 8. Offene Risiken

Die wichtigsten Risiken sind:
- zu frueher Fokus auf Modelle statt Datenqualitaet
- unklare Verantwortlichkeit fuer Inhalte
- fehlende Testfaelle fuer Retrieval und Zugriff
- zu breite Pilotabdeckung ohne priorisierte Use Cases
- fehlendes Betriebsmodell nach dem ersten Erfolg

## 9. Konkrete naechste 14 Tage

### Woche 1
- Zielarchitektur finalisieren
- Ordner- und Datenmodell beschliessen
- Pilotdokumente auswaehlen
- Entra-Gruppenmodell definieren
- erste Testfragen sammeln

### Woche 2
- Ingestion-Pipeline fuer Pilotdaten aufsetzen
- Knowledge Bases trennen
- Zugriffsrechte testen
- Qualitaet gegen Testfragen pruefen
- Top-Use-Cases fuer Phase 2 priorisieren

## 10. Empfehlung zur Repo-Struktur

Wenn dieses Verzeichnis weiter als Arbeitsbasis genutzt wird, sollte es in klare Bereiche getrennt werden:

```text
EBF RAG/
├── 00_strategy/
├── 01_architecture/
├── 02_setup/
├── 03_rag/
├── 04_access/
├── 05_use_cases/
├── 06_operations/
└── 99_assets/
```

Zuordnung der bestehenden Dateien:
- Zielbild und Roadmap nach `00_strategy/`
- Setup-Dokumente nach `02_setup/`
- RAG- und Ingestion-Dokumente nach `03_rag/`
- Entra/Open WebUI Zugriff nach `04_access/`
- PPTX und Bilder nach `99_assets/`

## 11. Kurzfazit

Die richtige Reihenfolge fuer EBF ist:

1. Plattform stabilisieren
2. Wissensqualitaet absichern
3. Zugriff sauber trennen
4. fachliche Use Cases priorisieren
5. erst danach Tooling, Memory und erweiterte Plattformfunktionen

Damit wird aus mehreren guten Einzelideen ein steuerbares Projekt mit klarer Reihenfolge.
