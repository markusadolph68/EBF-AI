# EBF AI Testkatalog Pilotfragen

## Ziel

Dieser Testkatalog dient dazu, den Phase-1-Pilot wiederholt gegen dieselben Fragen zu pruefen.
Er testet:
- Retrieval-Treffer
- Antwortqualitaet
- Quellenbezug
- Zugriffstrennung

## Bewertungslogik

Jede Frage sollte mindestens entlang dieser Kriterien bewertet werden:
- Richtige Quelle gefunden: `ja/nein`
- Richtiger Abschnitt gefunden: `ja/nein/teilweise`
- Antwort fachlich korrekt: `ja/nein/teilweise`
- Quelle nachvollziehbar genannt: `ja/nein`
- Halluzination erkennbar: `ja/nein`

## Testgruppen

- HR
- Vertrieb
- Projekte
- Bereichsuebergreifend
- Zugriff

## HR

### HR-01
Frage:
- Welche Schritte umfasst das interne Onboarding neuer Mitarbeitender?

Erwartung:
- Antwort basiert auf Onboarding- oder HR-Prozessdokumenten
- Schritte werden strukturiert zusammengefasst

### HR-02
Frage:
- Wo sind Regelungen zu Urlaub, Krankmeldung oder Abwesenheiten dokumentiert?

Erwartung:
- Verweis auf passende HR-Policies
- keine erfundenen Detailregeln

### HR-03
Frage:
- Welche Unterlagen muessen fuer einen neuen Mitarbeitenden vorliegen?

Erwartung:
- Quellen aus HR oder Recruiting-Prozessen
- nachvollziehbare Auflistung

### HR-04
Frage:
- Welche internen Ansprechpartner sind fuer HR-Prozesse relevant?

Erwartung:
- nur beantworten, wenn Quellen es hergeben
- sonst transparent auf fehlende Information hinweisen

## Vertrieb

### Vertrieb-01
Frage:
- Welche Leistungen sind im Angebot fuer Managed AI Services enthalten?

Erwartung:
- korrekter Bezug auf Angebotsunterlagen
- klare Struktur nach Leistungsbausteinen

### Vertrieb-02
Frage:
- Welche Argumente oder Referenzen eignen sich fuer einen AI-Pilot im Mittelstand?

Erwartung:
- Nutzung von Angebots- oder Referenzunterlagen
- keine frei erfundenen Kundenbeispiele

### Vertrieb-03
Frage:
- Welche Unterschiede gibt es zwischen Pilot, Produktivbetrieb und Plattformausbau?

Erwartung:
- Zusammenfuehrung aus Strategie- und Roadmap-Dokumenten
- saubere Trennung der Stufen

### Vertrieb-04
Frage:
- Welche Punkte gehoeren typischerweise in ein Angebot fuer einen internen AI-Assistenten?

Erwartung:
- strukturierte Antwort aus Vertriebs- und Angebotswissen
- keine juristisch verbindlichen Aussagen ohne Quelle

## Projekte

### Projekte-01
Frage:
- Welche Projektartefakte oder Checklisten sind fuer den Delivery-Start vorgesehen?

Erwartung:
- Antwort basiert auf Projektmethodik oder Delivery-Unterlagen
- klare Nennung der gefundenen Quelle

### Projekte-02
Frage:
- Wie sollte ein AI-Pilot aus Projektsicht in Phasen strukturiert werden?

Erwartung:
- sinnvolle Ableitung aus Roadmap- oder Projektunterlagen
- keine Vermischung mit allgemeinen Internetstandards

### Projekte-03
Frage:
- Welche Risiken werden fuer den Pilotbetrieb gesehen?

Erwartung:
- Rueckgriff auf Projektplan, Roadmap oder Betriebsdokumente
- Risiken werden konkret benannt

### Projekte-04
Frage:
- Welche Rollen braucht der Pilot fuer Betrieb, Inhalte und Tests?

Erwartung:
- Antwort aus Projekt- und Betriebsunterlagen
- klare Rollentrennung

## Bereichsuebergreifend

### Cross-01
Frage:
- Was ist das Zielbild von EBF AI ueber den heutigen Wissenschatbot hinaus?

Erwartung:
- Antwort aus Zielbild- und Strategieunterlagen
- Stufenmodell wird korrekt wiedergegeben

### Cross-02
Frage:
- Was fehlt aktuell noch zum ChatGPT-Ersatz?

Erwartung:
- Tooling, Orchestrierung, Memory, Retrieval-Qualitaet, Monitoring/Governance
- keine Verwechslung mit reinem Modellvergleich

### Cross-03
Frage:
- Warum ist die Ingestion-Pipeline so wichtig fuer die Qualitaet des Systems?

Erwartung:
- Zusammenhang zwischen Parsing, Chunking, Metadaten und Antwortqualitaet

### Cross-04
Frage:
- Welche Reihenfolge ist fuer die Umsetzung des Projekts sinnvoll?

Erwartung:
- Plattform, Wissensqualitaet, Zugriff, Use Cases, danach Ausbau

## Zugriff

### Zugriff-01
Frage:
- Ein Nutzer aus der Gruppe Vertrieb fragt nach HR-Richtlinien. Was darf er sehen?

Erwartung:
- nur vertriebsberechtigte Inhalte
- kein Zugriff auf HR-spezifische Knowledge Base

### Zugriff-02
Frage:
- Ein Nutzer ohne Projektgruppe fragt nach internen Delivery-Playbooks. Was passiert?

Erwartung:
- Zugriff wird verweigert oder es werden keine unberechtigten Inhalte geliefert

### Zugriff-03
Frage:
- Ein Admin prueft, ob die Knowledge Bases korrekt nach Gruppen getrennt sind. Welche Faelle muessen getestet werden?

Erwartung:
- Positiv- und Negativfaelle fuer jede Gruppe
- Login-/Logout-Effekt bei Gruppenwechsel beachten

### Zugriff-04
Frage:
- Was passiert, wenn eine Gruppe im Entra-Token fehlt?

Erwartung:
- Zugriff ist nach erneutem Login nicht mehr vorhanden
- Entra bleibt die fuehrende Wahrheit

## Testdurchfuehrung

Empfehlung pro Testlauf:
- 5 Fragen aus HR
- 5 Fragen aus Vertrieb
- 5 Fragen aus Projekte oder Cross
- 3 Zugriffstests

## Ampellogik

- `Gruen`: richtige Quelle, richtige Antwort, keine Halluzination
- `Gelb`: teilweise korrekt oder unklare Quellenlage
- `Rot`: falsche Antwort, falscher Zugriff oder Halluzination

## Mindestziel fuer Phase 1

Phase 1 sollte erst als belastbar gelten, wenn:
- die meisten Kernfragen `Gruen` sind
- keine kritischen Zugriffstests `Rot` sind
- die Fehlerbilder dokumentiert und wiederholbar sind
