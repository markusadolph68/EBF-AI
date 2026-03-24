# EBF AI Management Onepager

## Ausgangslage

EBF hat bereits die Bausteine fuer einen internen AI-Assistenten aufgebaut:
- Open WebUI
- RAG mit Chroma
- lokale und Cloud-Modelle
- Entra fuer SSO und Zugriff

Der aktuelle Reifegrad ist ein funktionierender Wissenschatbot.

## Zielbild

EBF entwickelt den Pilot in drei Stufen weiter:

1. Wissensassistent
2. Arbeitsassistent
3. AI-Plattform

Der Engpass ist nicht primaer das Modell, sondern die Systemarchitektur drumherum:
- Datenqualitaet
- Zugriffstrennung
- Orchestrierung
- Betrieb und Governance

## Strategische Prioritaet

Fuer den Pilot ist die richtige Reihenfolge:

1. Plattform stabilisieren
2. RAG-Qualitaet absichern
3. Zugriffe sauber trennen
4. konkrete Use Cases priorisieren
5. erst danach Tools, Memory und tiefere Automatisierung ausbauen

## Ziel fuer Phase 1

In Phase 1 soll ein verlaesslicher interner Wissensassistent entstehen, der:
- reproduzierbar betrieben werden kann
- korrekte Antworten aus definierten Dokumenten liefert
- sensible Inhalte nach Gruppen trennt
- mit Testfragen messbar bewertet wird

## Nutzen fuer EBF

Kurzfristiger Nutzen:
- schnellere Informationssuche
- weniger Rueckfragen zu Prozessen und Dokumenten
- professioneller interner AI-Zugang

Mittelfristiger Nutzen:
- strukturierte Unterstuetzung bei Angeboten, Projekten und Analysen
- Wiederverwendung internen Wissens
- Grundlage fuer spaetere AI-gestuetzte Arbeitsablaeufe

## Entscheidende Arbeitspakete

### 1. Technische Basis
- einheitliches Setup fuer Open WebUI, Chroma und Modellanbindung
- dokumentierte Zielarchitektur
- reproduzierbarer Start und Betrieb

### 2. Wissensbasis
- Auswahl hochwertiger Pilotdokumente
- Parsing, Chunking und Metadatenstandard
- kontrollierte Reindexierung
- Testkatalog fuer Qualitaet

### 3. Zugriff
- Entra-Gruppenmodell
- getrennte Knowledge Bases
- sauberer Group Sync und Rechte-Test

### 4. Fachlicher Mehrwert
- 2 bis 3 priorisierte Use Cases
- standardisierte Prompts und Antwortformate
- messbarer Zeitgewinn im Alltag

## Erfolgskriterien des Piloten

Der Pilot ist erfolgreich, wenn:
- die Plattform stabil laeuft
- die wichtigsten Dokumente sauber indexiert sind
- Zugriffe nach Bereichen korrekt greifen
- Testfragen ueberwiegend korrekt beantwortet werden
- mindestens zwei Use Cases echten Produktivitaetsnutzen liefern

## Hauptrisiken

- Fokus auf Modellwahl statt Datenqualitaet
- zu viele Themen gleichzeitig
- fehlende Inhaltsverantwortung in den Fachbereichen
- unzureichende Tests fuer Retrieval und Berechtigungen

## Empfehlung

Der Pilot sollte in den naechsten zwei Wochen auf eine belastbare Phase-1-Basis gebracht werden.
Danach sollte die Entscheidung ueber Phase 2 an messbaren Ergebnissen aus Qualitaet, Nutzung und Fachnutzen ausgerichtet werden.
