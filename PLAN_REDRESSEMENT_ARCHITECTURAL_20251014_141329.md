# 🏗️ PLAN DE REDRESSEMENT ARCHITECTURAL PANINI

**Créé le :** 2025-10-14 14:13:29

## 📊 État Actuel

- **Total repositories :** 16
- **Repository parent :** Panini

### Repositories à renommer :
- `PaniniFS` → `Panini-FS`
- `PaniniFS-CopilotageShared` → `Panini-CopilotageShared`
- `PaniniFS-AttributionRegistry` → `Panini-AttributionRegistry`
- `PaniniFS-DatasetsIngestion` → `Panini-DatasetsIngestion`
- `PaniniFS-ExecutionOrchestrator` → `Panini-ExecutionOrchestrator`
- `PaniniFS-UltraReactive` → `Panini-UltraReactive`
- `PaniniFS-PublicationEngine` → `Panini-PublicationEngine`
- `PaniniFS-SemanticCore` → `Panini-SemanticCore`
- `PaniniFS-AutonomousMissions` → `Panini-AutonomousMissions`
- `PaniniFS-CoLabController` → `Panini-CoLabController`
- `PaniniFS-CloudOrchestrator` → `Panini-CloudOrchestrator`
- `PaniniFS-SpecKit-Shared` → `Panini-SpecKit-Shared`

## 🎯 Architecture Cible

```
Panini (Parent principal)
├── core/
│   ├── Panini-FS → modules/core/filesystem
│   ├── Panini-SemanticCore → modules/core/semantic
├── orchestration/
│   ├── Panini-CloudOrchestrator → modules/orchestration/cloud
│   ├── Panini-ExecutionOrchestrator → modules/orchestration/execution
├── services/
│   ├── Panini-CoLabController → modules/services/colab
│   ├── Panini-PublicationEngine → modules/services/publication
│   ├── Panini-DatasetsIngestion → modules/services/datasets
├── infrastructure/
│   ├── Panini-UltraReactive → modules/infrastructure/reactive
│   ├── Panini-AutonomousMissions → modules/infrastructure/autonomous
├── shared/
│   ├── Panini-CopilotageShared → shared/copilotage
│   ├── Panini-SpecKit-Shared → shared/speckit
│   ├── Panini-AttributionRegistry → shared/attribution
├── projects/
│   ├── Panini-Gest → projects/gest
│   ├── Panini-OntoWave → projects/ontowave
```

## 📋 Phases de Migration

### Phase 1: Préparation et sauvegarde
**Durée estimée :** 1-2 heures
**Risque :** Faible

**Actions :**
- Sauvegarde complète de tous les repositories
- Création des scripts de renommage GitHub
- Validation de l'état Git de tous les repos
- Export des GitHub Projects/Issues

### Phase 2: Renommage des repositories GitHub
**Durée estimée :** 2-3 heures
**Risque :** Moyen

**Actions :**
- Renommage PaniniFS → Panini-FS
- Renommage tous PaniniFS-* → Panini-*
- Mise à jour des URLs remotes locales
- Vérification accessibilité repositories

### Phase 3: Restructuration Panini parent
**Durée estimée :** 3-4 heures
**Risque :** Moyen

**Actions :**
- Consolidation Panini-Research dans Panini
- Création structure modules/ avec catégories
- Configuration .gitmodules pour tous les submodules
- Mise à jour documentation principale

### Phase 4: Configuration submodules
**Durée estimée :** 2-3 heures
**Risque :** Élevé

**Actions :**
- Ajout de tous les modules comme submodules
- Configuration des chemins selon nouvelle architecture
- Synchronisation et tests
- Mise à jour des références croisées

### Phase 5: Finalisation et documentation
**Durée estimée :** 1-2 heures
**Risque :** Faible

**Actions :**
- Mise à jour de toute la documentation
- Création guides migration pour utilisateurs
- Tests complets de l'écosystème
- Communication changements

