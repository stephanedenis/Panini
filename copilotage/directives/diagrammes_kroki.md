# 📊 Diagrammes - Règle de Standardisation Panini

**STATUS**: ✅ RÈGLE OBLIGATOIRE pour tous les projets  
**Date**: 2025-12-24  
**Auteur**: Copilotage Panini

---

## 🎯 Règle Fondamentale

**Tous les diagrammes doivent utiliser Kroki (via Mermaid, PlantUML, etc.)**

✅ **AUTORISÉ**: Mermaid flowchart, sequenceDiagram, stateDiagram, timeline  
❌ **INTERDIT**: Diagrammes ASCII art (┌─┼┬─┐, │, └─┴┘, ├, ▼, etc.)  
❌ **INTERDIT**: Images PNG/JPG statiques  
❌ **INTERDIT**: Diagrammes en texte brut  

---

## 📝 Syntaxe Markdown (Kroki Support)

### Flowchart (graphiques de flux)
```markdown
```mermaid
flowchart TD
    A["🔄 GitHub Event"]
    B["⚙️ Workflow"]
    C["🚀 Cloud Run"]
    
    A --> B
    B --> C
```
```

### Sequence Diagram (interaction temporelle)
```markdown
```mermaid
sequenceDiagram
    participant Client
    participant Server
    participant API
    
    Client->>Server: POST /api/analyze
    Server-->>Client: HTTP 202
    Server->>API: GET /resource
    API-->>Server: 200 OK
```
```

### State Diagram (machine à états)
```markdown
```mermaid
stateDiagram-v2
    [*] --> State1
    State1 --> State2
    State2 --> [*]
```
```

### Timeline (chronologie)
```markdown
```mermaid
timeline
    title Kernel Keep-Alive
    t=0s     : Assigned
    t=60s    : Refresh
    t=120s   : Refresh
    t=1800s  : 30 minutes
```
```

### Graph (diagrammes généralistes)
```markdown
```mermaid
graph TB
    A[Start] -->|condition| B[Process]
    B -->|success| C[End]
    B -->|error| D[Retry]
```
```

---

## ✅ Cas d'Usage

| Diagramme | Format | Exemple |
|-----------|--------|---------|
| **Architecture système** | Mermaid graph | Composants + flux données |
| **Pipeline étapes** | Mermaid flowchart | 5 étapes orchestration |
| **Interactions API** | Mermaid sequenceDiagram | HTTP calls temporalité |
| **Timing de events** | Mermaid timeline | Keep-alive refresh intervals |
| **Transitions états** | Mermaid stateDiagram | OAuth2 token lifecycle |

---

## 🔄 Exemple de Conversion

### ❌ Avant (ASCII - INTERDIT)
```
┌────────────────┐
│   GitHub       │
│   Event        │
└────────┬───────┘
         │
         ▼
┌────────────────┐
│  Workflow      │
└────────┬───────┘
         │
         ▼
┌────────────────┐
│  Cloud Run     │
└────────────────┘
```

### ✅ Après (Mermaid - AUTORISÉ)
```mermaid
flowchart TD
    A["🔔 GitHub Event"]
    B["⚙️ Workflow"]
    C["☁️ Cloud Run"]
    
    A --> B
    B --> C
```

---

## 💡 Avantages de Kroki

| Aspect | ASCII | Kroki |
|--------|-------|-------|
| **Versionnable** | ❌ Difficile à merger | ✅ Texte pur, git diff facile |
| **Maintenable** | ❌ Format fragile | ✅ Syntaxe robuste |
| **Modifiable** | ❌ Refaire entièrement | ✅ Édition progressive |
| **Rendu** | ❌ Manual | ✅ Auto sur GitHub/docs |
| **Cohérence** | ❌ Style aléatoire | ✅ Style unifié |
| **Accessibilité** | ❌ Pas de sémantique | ✅ Structure sémantique |

---

## 📋 Checklist de Validation

Avant de valider un PR avec diagrammes:

- [ ] Aucun diagramme ASCII (┌─┬─┐ interdit)
- [ ] Tout utilise Mermaid/PlantUML
- [ ] Diagrammes rendu correctement sur GitHub
- [ ] Syntaxe Markdown respectée (```mermaid)
- [ ] Commentaires explicatifs présents
- [ ] Pas d'images statiques (PNG/JPG)
- [ ] Légende ou annotations présentes

---

## 🔧 Outils Recommandés

| Outil | Usage |
|-------|-------|
| **Mermaid Live** | https://mermaid.live - Éditeur visuel en ligne |
| **VSCode Extension** | "Markdown Preview Mermaid Support" |
| **GitHub** | Rendu natif des diagrammes Mermaid |
| **Kroki Server** | https://kroki.io - Conversion formats multiples |

---

## 📚 Références

- **Mermaid Docs**: https://mermaid.js.org/
- **Kroki Documentation**: https://docs.kroki.io/
- **GitHub Native Support**: Rendu direct .md files

---

## 🚨 Violations Connues

Fichiers à rectifier si conversion effectuée:

- [x] PHASE2_ARCHITECTURE.md (8 diagrammes ASCII → Kroki)
- [x] PHASE2_INTEGRATION_GUIDE.md (2 diagrammes ASCII → Kroki)
- [x] PHASE2_COMPLETION_REPORT.md (1 diagramme ASCII → Kroki)
- [x] PHASE2_FINAL_MANIFEST.md (1 diagramme ASCII → Kroki)

---

**Dernière mise à jour**: 2025-12-24  
**Maintenu par**: Copilotage Panini  
**Appliqué à**: Tous les projets Panini
