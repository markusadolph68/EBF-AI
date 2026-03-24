# EBF AI Kanban Board

## Nutzung

Dieses Board ist als einfache Arbeitssteuerung fuer den Pilot gedacht.
Empfohlene Spalten:
- Backlog
- Diese Woche
- In Arbeit
- Review
- Erledigt

## Backlog

### `P2` Modell-Routing lokal vs. Cloud definieren
Ziel:
- Regeln fuer Speed, Kosten und Qualitaet festlegen

Definition of Done:
- Standardmodell ist festgelegt
- Eskalationsfaelle zur Cloud sind beschrieben
- Vergleichsergebnisse liegen vor

### `P2` Reviewprozess fuer neue Dokumente definieren
Ziel:
- geregelter Weg fuer neue Wissensinhalte

Definition of Done:
- Einreichung, Freigabe und Reindexierung sind dokumentiert
- Verantwortlichkeiten sind benannt

### `P2` Logging- und Monitoring-Konzept vorbereiten
Ziel:
- spaetere Produktionsreife vorbereiten

Definition of Done:
- relevante Signale und Kennzahlen sind beschrieben
- Umsetzungsoptionen sind benannt

## Diese Woche

### `P0` Zielarchitektur final dokumentieren
Ziel:
- abgestimmtes Gesamtbild fuer Plattform, RAG, Modelle und Zugriff

Naechster Schritt:
- finale Architekturuebersicht auf einer Seite festziehen

### `P0` Pilotdokumente je Bereich auswaehlen
Ziel:
- sauberer Startbestand fuer den Pilot

Naechster Schritt:
- 10 bis 20 hochwertige Dokumente benennen und freigeben

### `P0` Metadatenmodell festlegen
Ziel:
- Standard fuer Quelle, Bereich, Version und Vertraulichkeit

Naechster Schritt:
- Pflichtfelder final beschliessen

### `P0` Entra-Gruppenmodell definieren
Ziel:
- Trennung von Inhaltsgruppen und Adminrechten

Naechster Schritt:
- konkrete Gruppennamen und Berechtigungslogik festlegen

### `P0` Testkatalog fuer Retrieval und Antwortqualitaet anlegen
Ziel:
- wiederholbare Qualitaetspruefung

Naechster Schritt:
- erste Testfragen je Bereich sammeln

## In Arbeit

### `P0` Zielordner und Artefakte vereinheitlichen
Status:
- Grundstruktur ist umgesetzt

Restarbeiten:
- neue Dokumente konsequent in der Zielstruktur pflegen

Definition of Done:
- keine ungeordneten Kerndokumente mehr im Wurzelverzeichnis

## Review

### `P0` Standard-Setup fuer Open WebUI, Chroma und Modellserver festlegen
Prueffragen:
- welche Servervariante ist Referenz fuer den Pilot
- welche Healthchecks sind Pflicht
- welche Konfiguration ist verbindlich

### `P0` Chunking-Regeln definieren
Prueffragen:
- funktionieren die Regeln auf echten Pilotdokumenten
- sind Tabellen und Ueberschriften sauber behandelt

### `P0` Knowledge Bases nach Bereichen trennen
Prueffragen:
- sind Bereichsgrenzen fachlich korrekt
- sind Standardrechte minimal gesetzt

## Erledigt

### Projektstruktur im Repo aufgebaut
Ergebnis:
- Strategie, Architektur, Setup, RAG, Zugriff, Betrieb und Assets sind getrennt abgelegt

### Projektplan erstellt
Referenz:
- `00_strategy/14_ebf_ai_projektplan.md`

### Management-Onepager erstellt
Referenz:
- `01_architecture/15_ebf_ai_management_onepager.md`

### Operatives Backlog erstellt
Referenz:
- `06_operations/16_ebf_ai_operatives_backlog.md`

## Empfohlene Board-Regeln

- maximal 3 Themen gleichzeitig in `In Arbeit`
- `P0` vor `P1` und `P2`
- jedes Ticket braucht Owner und naechsten Schritt
- nichts geht nach `Erledigt`, bevor die Definition of Done erfuellt ist
