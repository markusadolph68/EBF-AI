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

### `P2` OIDC und Group Sync fuer Open WebUI konfigurieren
Ziel:
- Entra erst nach stabilem lokalem Pilot anschliessen

Definition of Done:
- Testlogin funktioniert
- Gruppen aus dem Token werden erkannt
- Rechteaenderungen greifen nach erneutem Login

### `P2` Modell-Routing lokal vs. Cloud definieren
Ziel:
- Regeln fuer Speed, Kosten und Qualitaet festlegen

Definition of Done:
- Standardmodell ist festgelegt
- Eskalationsfaelle zur Cloud sind beschrieben
- Vergleichsergebnisse liegen vor

### `P2` Logging- und Monitoring-Konzept vorbereiten
Ziel:
- spaetere Produktionsreife vorbereiten

Definition of Done:
- relevante Signale und Kennzahlen sind beschrieben
- Umsetzungsoptionen sind benannt

## Diese Woche

### `P0` Referenz-Stack Open WebUI + MLX + Chroma festziehen
Ziel:
- eindeutiger Zielpfad fuer den Pilot

Naechster Schritt:
- `mvp/` als Referenzstack finalisieren und pruefen

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

### `P0` Ingestion-Pipeline mit Manifest-Logik aufsetzen
Ziel:
- wiederholbare Verarbeitung geaenderter Dokumente

Naechster Schritt:
- Dokumentordner und erste Imports gegen Chroma fahren

### `P0` Testkatalog fuer Retrieval und Antwortqualitaet anlegen
Ziel:
- wiederholbare Qualitaetspruefung

Naechster Schritt:
- erste Testfragen je Bereich sammeln

## In Arbeit

### `P0` Start-, Stop- und Healthcheck-Logik vereinheitlichen
Status:
- Skripte und Checks werden im Referenzpfad gebuendelt

Restarbeiten:
- einmal lokal gegen den Stack pruefen

Definition of Done:
- Start, Stop und Healthcheck sind ohne Spezialwissen nutzbar

## Review

### `P1` Lokales Open-WebUI-Adminmodell definieren
Prueffragen:
- sind Adminrechte minimal vergeben
- ist klar, wer den Pilot operativ betreut
- braucht der Pilot schon weitere Nutzerrollen

### `P1` Bereiche und Knowledge Bases lokal trennen
Prueffragen:
- sind Bereichsgrenzen fachlich korrekt
- passt die technische Trennung zu den Pilotdokumenten
- bleibt die spaetere Entra-Zuordnung moeglich

### `P0` MLX/OpenAI-kompatiblen Hostserver als Standard festlegen
Prueffragen:
- funktionieren `/health`, `/v1/models` und Chat sauber
- ist das Provider-Setup in Open WebUI klar dokumentiert

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
