# 📐 Architecture Standard - Projet Panini

**Date**: 2025-11-12  
**Version**: 1.0

## 🎯 Principes d'Organisation

### Structure Standard par Module

Chaque module (parent ou sous-module) suit cette structure :

```
module/
├── docs/                    # Documentation propre au module
│   ├── README.md           # Vue d'ensemble du module
│   ├── architecture/       # Diagrammes et conception
│   ├── guides/            # Guides d'utilisation
│   └── api/               # Documentation API
├── src/                    # Code source du module
│   ├── __init__.py
│   └── ...
├── tests/                  # Tests unitaires et d'intégration
├── corpus/                 # Corpus de textes (si applicable)
│   └── README.md          # Description du corpus
├── references/            # Documents de référence externe
│   └── README.md          # Index des références
├── notebooks/             # Notebooks Colab (jobs système uniquement)
│   └── *.ipynb           # Format: {module}_{job}.ipynb
├── research/              # Notebooks de recherche locale
│   └── *.ipynb           # Expérimentation et prototypage
└── README.md              # Point d'entrée du module
```

## 📦 Modules Identifiés

### Projet Parent: `/` (Panini)
```
/
├── docs/                  # Documentation projet principal
├── src/                   # Code source principal
├── modules/               # Sous-modules indépendants
├── notebooks/             # Notebooks Colab (jobs système)
├── research/              # Recherche et expérimentation
├── corpus/                # Corpus textuels du projet
├── references/            # Références scientifiques
├── copilotage/            # Submodule commun agents (contexte partagé)
├── tools/                 # Outils et scripts utilitaires
├── tests/                 # Tests du projet principal
└── README.md
```

### Sous-modules dans `/modules`
- `core/` - Fonctionnalités cœur
- `data/` - Gestion des données
- `infrastructure/` - Infrastructure technique
- `missions/` - Orchestration des missions
- `ontowave/` - Module OntoWave
- `orchestration/` - Orchestration système
- `publication/` - Gestion des publications
- `reactive/` - Programmation réactive
- `services/` - Services applicatifs

### Code Source Principal `/src`
Structure actuelle à valider et organiser selon besoins.

## 🔧 Copilotage - Submodule Commun

Le dossier `copilotage/` est un **submodule partagé** pour les agents :

```
copilotage/
├── autonomie/             # Modes autonomes
├── directives/            # Directives des agents
├── protocols/             # Protocoles de communication
├── regles/               # Règles et contraintes
├── journal/              # Journalisation des agents
├── utilities/            # Utilitaires communs
└── config.yml            # Configuration agents
```

⚠️ **Attention**: `copilotage/` ne doit PAS contenir :
- Documentation projet spécifique → va dans `/docs`
- Documentation des sous-modules → va dans `modules/{module}/docs`
- Corpus ou références → vont dans `corpus/` ou `references/`

## 📊 Séparation Stricte

### Documentation (`docs/`)
- Guides utilisateur
- Architecture technique
- Rapports de développement
- API et références code

### Corpus (`corpus/`)
- Textes d'entraînement
- Données linguistiques
- Exemples et échantillons
- Datasets structurés

### Références (`references/`)
- Articles scientifiques
- Documentation externe
- Standards et spécifications
- Bibliographie

### Research (`research/`)
- Notebooks expérimentaux
- Prototypes
- Analyses exploratoires
- Études de faisabilité

### Notebooks (`notebooks/`)
- **Uniquement** notebooks Colab
- Jobs système automatisés
- Synchronisation GitHub
- Dashboards temps réel

## 🚀 Actions de Migration

### Phase 1: Consolidation Documentation
1. Fusionner `copilotage/docs/` → `/docs/copilotage/`
2. Fusionner `copilotage/documentation/` → `/docs/copilotage/`
3. Garder structure cohérente

### Phase 2: Séparation Corpus/Références
1. Identifier fichiers textes dans `data/`
2. Créer `/corpus` et `/references`
3. Migrer selon nature du contenu

### Phase 3: Notebooks
1. Valider notebooks dans `/notebooks` (tous Colab?)
2. Si notebooks de recherche → déplacer vers `/research`
3. Créer `research/notebooks/` si nécessaire

### Phase 4: Modules Standards
1. Pour chaque module dans `/modules`:
   - Créer structure standard
   - Migrer documentation existante
   - Séparer corpus/références si applicable

### Phase 5: Élimination Doublons
1. Supprimer `ESSENCE_PANINIFS.md` dupliqué
2. Consolider fichiers versionnés (v7.x)
3. Nettoyer structures redondantes

## ✅ Validation Finale

Chaque module doit avoir :
- [ ] Un `README.md` clair
- [ ] `docs/` avec documentation propre
- [ ] `src/` organisé et cohérent
- [ ] Séparation corpus/références respectée
- [ ] Pas de doublons inter-modules
- [ ] Usage correct de `copilotage/` (si applicable)

---

**Maintenu par**: Équipe Panini  
**Dernière révision**: 2025-11-12
