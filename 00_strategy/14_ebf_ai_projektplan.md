# EBF AI Projektplan

## 1. Projektziel

EBF baut keinen reinen Wissenschatbot, sondern schrittweise eine interne AI-Plattform.

Der aktuelle Stand ist:
- Open WebUI als Frontend
- RAG mit Chroma
- lokaler MLX-Modellserver
- erste Pilotdokumente und Setup-Bausteine

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
- lokaler MLX/OpenAI-kompatibler Endpoint
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
Ziel: Pilot zunaechst einfach, spaeter sauber abgesichert betreiben.

Inhalte:
- lokale Pilotnutzer in Open WebUI
- schlankes Admin-Modell
- manuelle Bereichstrennung fuer Knowledge Bases
- Entra als letzter Integrationsschritt

Deliverables:
- lokaler Pilotzugriff ohne SSO-Abhaengigkeit
- dokumentierte Minimalrechte
- getrennte Bereiche fuer sensible Inhalte
- spaeteres Entra-Zielbild beschrieben

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
- Open WebUI + MLX + Chroma als Referenzstack festziehen
- RAG-Quellen bereinigen
- Metadaten und Chunking festlegen
- lokale Pilotnutzung sauber aufsetzen
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

### Phase 3 - Plattform haerten und erweitern
Ziel: vom stabilen Pilot zur unternehmensfaehigen Plattform.

Prioritaet:
- Entra SSO und Zugriffstrennung anschliessen
- Tool Layer vorbereiten
- API-Integrationen bewerten
- Memory-Konzept definieren
- Monitoring und Governance ausbauen

Ergebnis:
- Pilot wird unternehmensfaehig im Zugriff
- Assistent kann nicht nur antworten, sondern spaeter handeln
- Basis fuer Produktivbetrieb

## 5. Priorisierte Arbeitspakete

### Sofort sinnvoll
1. Open WebUI + MLX + Chroma als Referenz-MVP festziehen
2. Start-, Stop- und Healthcheck-Logik vereinheitlichen
3. Dokumentquellen fuer den Pilot auswaehlen
4. Metadatenmodell und Chunking-Regeln festlegen
5. Ingestion-Pfad mit Manifest-Logik aufsetzen
6. Testfragen je Bereich erstellen

### Danach
1. Testkatalog gegen echte Pilotdaten fahren
2. Rollen und Betriebsmodell festlegen
3. Top-Use-Cases mit Fachbereich abstimmen
4. Prompt-Standards und Templates bauen

### Spaeter
1. Entra und gruppenbasierten Zugriff anschliessen
2. APIs und Tool Layer priorisieren
3. Monitoring, KPI-Dashboard und Memory-Ansatz aufbauen

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
- der lokale Pilotbetrieb stabil funktioniert
- Testfragen ueberwiegend korrekt beantwortet werden
- mindestens 2 Use Cases echten Zeitgewinn liefern

## 8. Offene Risiken

Die wichtigsten Risiken sind:
- zu frueher Fokus auf Modelle statt Datenqualitaet
- zu frueher Fokus auf Entra statt stabilem Kernstack
- unklare Verantwortlichkeit fuer Inhalte
- fehlende Testfaelle fuer Retrieval und Zugriff
- zu breite Pilotabdeckung ohne priorisierte Use Cases
- fehlendes Betriebsmodell nach dem ersten Erfolg

## 9. Konkrete naechste 14 Tage

### Woche 1
- Zielarchitektur finalisieren
- Open WebUI + MLX + Chroma als Referenzstack festziehen
- Pilotdokumente auswaehlen
- Ordner- und Datenmodell beschliessen
- erste Testfragen sammeln

### Woche 2
- Ingestion-Pipeline fuer Pilotdaten aufsetzen
- Testlauf mit Pilotfragen fahren
- Knowledge-Base- und Bereichstrennung lokal vorbereiten
