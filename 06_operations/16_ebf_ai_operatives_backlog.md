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
Titel: Referenz-Stack Open WebUI + MLX + Chroma festziehen

Ergebnis:
- ein eindeutiger Zielpfad fuer UI, Modellanbindung und Vektorstore

Akzeptanzkriterien:
- `mvp/` ist der Referenzpfad
- Startreihenfolge ist dokumentiert
- lokale Ports und Persistenz sind klar benannt

### Task 1.2 `P0`
Titel: Start-, Stop- und Healthcheck-Logik vereinheitlichen

Ergebnis:
- einfacher operativer Einstieg fuer Admins

Akzeptanzkriterien:
- Startskript vorhanden
- Stopskript vorhanden
- Healthchecks fuer Open WebUI, MLX und Chroma sind definiert

### Task 1.3 `P0`
Titel: MLX/OpenAI-kompatiblen Hostserver als Standard festlegen

Ergebnis:
- Open WebUI kann stabil mit dem lokalen Modellserver sprechen

Akzeptanzkriterien:
- `/health` funktioniert
- `/v1/models` funktioniert
- `/v1/chat/completions` funktioniert
- Provider-Setup in Open WebUI ist dokumentiert

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

### Task 2.4 `P0`
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

## Epic 3 - Zugriff schlank beginnen

Ziel: Pilotbetrieb ohne Entra sauber beherrschbar machen.

### Task 3.1 `P0`
Titel: Lokales Open-WebUI-Adminmodell definieren

Ergebnis:
- klare Trennung zwischen wenigen Admins und Pilotnutzern

Akzeptanzkriterien:
- Admin-Verantwortung ist dokumentiert
- lokale Pilotnutzer sind benannt
- Rechte werden minimal vergeben

### Task 3.2 `P1`
Titel: Bereiche und Knowledge Bases lokal trennen

Ergebnis:
- mindestens getrennte Bereiche fuer sensible oder fachlich unterschiedliche Daten

Akzeptanzkriterien:
- Bereichsgrenzen sind definiert
- Collections oder Knowledge Bases sind benannt
- spaetere Entra-Zuordnung ist vorbereitet

### Task 3.3 `P1`
Titel: Rechte- und Zugriffstests fuer den lokalen Pilot dokumentieren

Ergebnis:
- nachvollziehbare Pruefung fuer Pilotnutzer und Admins

Akzeptanzkriterien:
- Positiv- und Negativfaelle sind vorhanden
- Ergebnisse koennen wiederholt geprueft werden
- Abweichungen werden dokumentiert

### Task 3.4 `P2`
Titel: OIDC und Group Sync fuer Open WebUI konfigurieren

Ergebnis:
- Login ueber Entra mit gruppenbasiertem Zugriff

Akzeptanzkriterien:
- Testlogin funktioniert
- Gruppen aus dem Token werden erkannt
- Rechteaenderungen greifen nach erneutem Login

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
- Eskalationsfaelle zur Cloud sind definiert
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
- Umsetzungsoptionen sind benannt
