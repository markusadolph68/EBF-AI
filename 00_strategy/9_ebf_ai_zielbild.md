# 🚀 EBF AI-Zielbild  
## Vom Wissenschatbot zur AI-Plattform

---

## 🎯 Ausgangssituation

EBF baut aktuell einen internen AI-Assistenten mit:

- Open WebUI  
- RAG (Chroma)  
- lokalen & Cloud-Modellen (MLX / RunPod)  
- Entra (SSO & Zugriff)

👉 Ergebnis heute:  
**Funktionierender Wissenschatbot**

---

## ❗ Zentrale Erkenntnis

> Der Unterschied zu ChatGPT liegt **nicht im Modell**,  
> sondern in der **Systemarchitektur drumherum**

---

## 🧠 Reifegradmodell

### 🟢 Stufe 1 – Wissenschatbot (heute)
- beantwortet Fragen  
- nutzt interne Dokumente  
- erste Produktivität  

👉 Nutzen: schnell, aber begrenzt  

---

### 🟡 Stufe 2 – Arbeitsassistent
- strukturierte Antworten  
- Templates (z. B. Angebote, Analysen)  
- Kontext pro Aufgabe  
- Modell-Routing (lokal + Cloud)  

👉 Nutzen: **echte Arbeitserleichterung**

---

### 🔵 Stufe 3 – AI-Plattform (Zielbild)
- führt Aktionen aus (APIs / Tools)  
- integriert Systeme (CRM, Projekte, M365)  
- merkt sich Kontext & Nutzerverhalten  
- ist messbar & steuerbar  

👉 Nutzen: **digitale Assistenz auf Unternehmensniveau**

---

## 🔧 Was konkret noch fehlt

### 1. Tool Layer (Gamechanger)
- APIs anbinden  
- Aktionen ausführen statt nur antworten  

---

### 2. Orchestrierung
- strukturierte Prompts  
- Rollenlogik  
- Antwortstandards  

---

### 3. Memory
- Nutzerkontext  
- Verlauf über Sessions  

---

### 4. Retrieval-Qualität
- bessere Dokumentstruktur  
- Metadaten  
- präzisere Treffer  

---

### 5. Monitoring & Governance
- Qualität messen  
- Nutzung verstehen  
- Kontrolle & Compliance  

---

## 🏗️ Zielarchitektur (vereinfacht)

```text
Entra (SSO + Gruppen)
        ↓
Open WebUI (Frontend)
        ↓
Orchestrierung / Prompt Layer
        ↓
RAG (Chroma, strukturierte Daten)
        ↓
LLM (MLX lokal + RunPod L40S)
        ↓
Tools / APIs (zukünftig)
```

---

## 📈 Empfohlene Roadmap

### Phase 1 (jetzt)
- RAG stabilisieren  
- Datenqualität erhöhen  
- Testkatalog aufbauen  

---

### Phase 2
- Templates & Arbeitslogik  
- Modell-Routing  
- bessere Outputs  

---

### Phase 3
- Tool Layer (APIs)  
- Integration in Systeme  
- Monitoring & Governance  

---

## 💡 Strategischer Vorteil für EBF

- Wissen wird **strukturiert nutzbar**  
- Prozesse werden **teilautomatisiert**  
- Mitarbeiter werden **produktiver**  
- AI wird **integrierter Bestandteil der Arbeit**

---

## 🧾 TL;DR

👉 Heute:  
**Guter Wissenschatbot**

👉 Ziel:  
**AI-gestützte Arbeitsplattform**

👉 Schlüssel:  
- nicht das Modell  
- sondern die Architektur
