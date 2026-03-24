# EBF AI Operatives Backlog

## Ziel

Dieses Backlog uebersetzt den Projektplan in umsetzbare Epics und Tasks fuer den Pilot.

## Priorisierung

- `P0`: blockierend fuer einen belastbaren Pilot
- `P1`: hoher Nutzen direkt nach Stabilisierung
- `P2`: sinnvoll fuer Ausbau nach Phase 1

## Epic 1 - Plattform stabilisieren

Ziel: reproduzierbare technische Basis fuer den Pilotbetrieb.

### Task 1.1 `P0`
Titel: Zielarchitektur final dokumentieren

Ergebnis:
- eine abgestimmte Architekturuebersicht fuer Frontend, Modelle, RAG und Zugriff

Akzeptanzkriterien:
- Komponenten und Datenfluss sind beschrieben
- lokale und Cloud-Anteile sind klar getrennt
- Betriebsverantwortung ist benannt

### Task 1.2 `P0`
Titel: Zielordner und Artefakte vereinheitlichen

Ergebnis:
- konsistente Projektstruktur fuer Strategie, Setup, RAG, Zugriff und Betrieb

Akzeptanzkriterien:
- bestehende Dokumente sind einsortiert
- neue Inhalte folgen derselben Struktur
- Such- und Uebergabeaufwand sinkt

### Task 1.3 `P0`
Titel: Standard-Setup fuer Open WebUI, Chroma und Modellserver festlegen

Ergebnis:
- eine bevorzugte Referenzvariante fuer den Pilot

Akzeptanzkriterien:
- Startreihenfolge ist dokumentiert
- benoetigte Konfigurationen sind benannt
- Gesundheitspruefungen sind definiert

### Task 1.4 `P1`
Titel: Betriebscheckliste fuer Start, Stop und Fehlerbilder erstellen

Ergebnis:
- einfaches Runbook fuer den Alltag

Akzeptanzkriterien:
- Start- und Stop-Prozess ist beschrieben
- Kernfehler sind mit Erstmassnahmen dokumentiert
- Verantwortliche wissen, wie sie den Status pruefen

## Epic 2 - RAG und Wissensqualitaet absichern

Ziel: verlaessliche Antworten auf Basis hochwertiger Dokumente.

### Task 2.1 `P0`
Titel: Pilotdokumente je Bereich auswaehlen

Ergebnis:
- kuratierter Startbestand mit 10 bis 20 hochwertigen Dokumenten

Akzeptanzkriterien:
- Dokumente sind fachlich freigegeben
- Bereiche wie HR, Vertrieb, Projekte sind markiert
- Dubletten und veraltete Inhalte sind ausgeschlossen

### Task 2.2 `P0`
Titel: Metadatenmodell festlegen

Ergebnis:
- Standardfelder fuer Quelle, Bereich, Version und Vertraulichkeit

Akzeptanzkriterien:
- Pflichtfelder sind definiert
- das Modell unterstuetzt spaetere Zugriffstrennung
- es ist fuer Chunks und Dokumente anwendbar

### Task 2.3 `P0`
Titel: Chunking-Regeln definieren

Ergebnis:
- verbindliche Regeln fuer Abschnittsgrenzen, Token-Groesse und Overlap

Akzeptanzkriterien:
- Regeln sind dokumentiert
- Tabellen und Ueberschriften werden sinnvoll behandelt
- die Regeln sind an Pilotdokumenten testbar

### Task 2.4 `P1`
Titel: Ingestion-Pipeline mit Manifest-Logik aufsetzen

Ergebnis:
- wiederholbare Verarbeitung geaenderter Dokumente

Akzeptanzkriterien:
- unveraenderte Dokumente werden uebersprungen
- geaenderte Dokumente werden neu indexiert
- Metadaten werden in Chroma mitgeschrieben

### Task 2.5 `P0`
Titel: Testkatalog fuer Retrieval und Antwortqualitaet anlegen

Ergebnis:
- standardisierte Testfragen pro Bereich

Akzeptanzkriterien:
- jede Frage hat erwartete Quelle oder Zielantwort
- Trefferqualitaet und Antwortqualitaet koennen bewertet werden
- derselbe Katalog ist wiederverwendbar

## Epic 3 - Zugriff und Sicherheit sauber aufsetzen

Ziel: richtige Inhalte fuer die richtigen Nutzergruppen.

### Task 3.1 `P0`
Titel: Entra-Gruppenmodell definieren

Ergebnis:
- klare Trennung zwischen Inhaltsgruppen und Adminrechten

Akzeptanzkriterien:
- Gruppen sind benannt
- ihre Funktion ist dokumentiert
- Gruppen sind auf Knowledge Bases abbildbar

### Task 3.2 `P0`
Titel: OIDC und Group Sync fuer Open WebUI konfigurieren

Ergebnis:
- Login ueber Entra mit gruppenbasiertem Zugriff

Akzeptanzkriterien:
- Testlogin funktioniert
- Gruppen aus dem Token werden erkannt
- Rechteaenderungen greifen nach erneutem Login

### Task 3.3 `P0`
Titel: Knowledge Bases nach Bereichen trennen

Ergebnis:
- mindestens getrennte Bereiche fuer sensible oder fachlich unterschiedliche Daten

Akzeptanzkriterien:
- Bereichsgrenzen sind definiert
- Knowledge Bases sind den Gruppen zugeordnet
- Standardrechte sind minimal gehalten

### Task 3.4 `P1`
Titel: Rechte-Testfaelle dokumentieren

Ergebnis:
- nachvollziehbare Pruefung fuer erlaubte und unerlaubte Zugriffe

Akzeptanzkriterien:
- Positiv- und Negativfaelle sind vorhanden
- Ergebnisse koennen wiederholt geprueft werden
- Abweichungen werden dokumentiert

## Epic 4 - Fachliche Use Cases priorisieren

Ziel: vom Wissenschatbot zum Arbeitsassistenten.

### Task 4.1 `P1`
Titel: Top-3 Use Cases mit Fachbereichen festlegen

Ergebnis:
- priorisierte Aufgaben mit klarem Nutzenversprechen

Akzeptanzkriterien:
- jeder Use Case hat Zielgruppe, Input und erwarteten Output
- Nutzen und Aufwand sind einschaetzbar
- Priorisierung ist abgestimmt

### Task 4.2 `P1`
Titel: Prompt-Standards definieren

Ergebnis:
- gemeinsame Grundlogik fuer Sprache, Quellenverhalten und Antwortstruktur

Akzeptanzkriterien:
- Basisregeln sind dokumentiert
- Halluzinationsvermeidung ist explizit beschrieben
- Fachbereiche koennen die Regeln nachvollziehen

### Task 4.3 `P1`
Titel: Antworttemplates fuer Pilot-Use-Cases entwerfen

Ergebnis:
- wiederverwendbare Formate fuer Angebote, Zusammenfassungen oder Analysen

Akzeptanzkriterien:
- Templates sind pro Use Case beschrieben
- Ausgabeformate sind konsistent
- Nutzer koennen den Mehrwert gegenueber freiem Chat erkennen

### Task 4.4 `P2`
Titel: Modell-Routing lokal vs. Cloud definieren

Ergebnis:
- klare Regeln fuer Geschwindigkeit, Kosten und Qualitaet

Akzeptanzkriterien:
- Standardmodell ist festgelegt
- Eskalationsfaelle fuer komplexe Aufgaben sind definiert
- Vergleichstests liegen vor

## Epic 5 - Betrieb und Governance verankern

Ziel: steuerbarer Betrieb statt Einzelwissen.

### Task 5.1 `P1`
Titel: Rollenmatrix fuer Betrieb und Inhalte erstellen

Ergebnis:
- klare Verantwortlichkeiten fuer Plattform, Inhalte und Freigaben

Akzeptanzkriterien:
- Sponsor, AI Admin, Content Owner und Tester sind beschrieben
- Entscheidungen haben benannte Owner
- Freigaben sind nachvollziehbar

### Task 5.2 `P1`
Titel: Pilot-KPIs festlegen

Ergebnis:
- kleiner Satz messbarer Steuerungskennzahlen

Akzeptanzkriterien:
- Qualitaet, Nutzung und Nutzen sind abgedeckt
- KPIs sind ohne grossen Zusatzaufwand erfassbar
- sie sind fuer Phase-2-Entscheidungen geeignet

### Task 5.3 `P2`
Titel: Reviewprozess fuer neue Dokumente definieren

Ergebnis:
- geregelter Weg fuer neue oder geaenderte Wissensinhalte

Akzeptanzkriterien:
- Einreichung, Freigabe und Reindexierung sind beschrieben
- Verantwortliche sind benannt
- veraltete Inhalte koennen entfernt oder ersetzt werden

### Task 5.4 `P2`
Titel: Logging- und Monitoring-Konzept vorbereiten

Ergebnis:
- Grundlage fuer spaetere Produktionsreife

Akzeptanzkriterien:
- relevante Signale sind definiert
- Fehler, Nutzung und Antwortqualitaet sind beruecksichtigt
- Umsetzungsoptionen sind benannt

## Empfohlene Reihenfolge fuer die naechsten zwei Wochen

### Woche 1
- Task 1.1
- Task 1.2
- Task 2.1
- Task 2.2
- Task 3.1
- Task 2.5

### Woche 2
- Task 1.3
- Task 2.3
- Task 2.4
- Task 3.2
- Task 3.3
- Task 4.1

## Definition of Done fuer Phase 1

Phase 1 ist abgeschlossen, wenn:
- die Plattform reproduzierbar startet
- Pilotdokumente mit Metadaten indexiert sind
- Bereichszugriffe funktionieren
- Testfragen ueberwiegend korrekt beantwortet werden
- die naechsten Use Cases fuer Phase 2 priorisiert sind
