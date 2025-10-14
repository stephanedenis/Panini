# 🏗️ Architecture Modulaire Panini

## Structure Organisée

```
Panini/ (Repository Parent Principal)
├── modules/                     # Modules fonctionnels
│   ├── core/                   # Composants centraux
│   │   ├── filesystem/         # Panini-FS
│   │   └── semantic/           # Panini-SemanticCore
│   ├── orchestration/          # Orchestrateurs
│   │   ├── cloud/              # Panini-CloudOrchestrator
│   │   └── execution/          # Panini-ExecutionOrchestrator
│   ├── services/               # Services applicatifs
│   │   ├── colab/              # Panini-CoLabController
│   │   ├── publication/        # Panini-PublicationEngine
│   │   └── datasets/           # Panini-DatasetsIngestion
│   └── infrastructure/         # Infrastructure
│       ├── reactive/           # Panini-UltraReactive
│       └── autonomous/         # Panini-AutonomousMissions
├── shared/                     # Composants partagés
│   ├── copilotage/             # Panini-CopilotageShared
│   ├── speckit/                # Panini-SpecKit-Shared
│   └── attribution/            # Panini-AttributionRegistry
├── projects/                   # Projets applicatifs
│   └── (à venir)
└── research/                   # Recherche et développement
    └── (Panini-Research)
```

## Navigation

### Accès aux modules
```bash
# Module filesystem core
cd modules/core/filesystem

# Service de collaboration
cd modules/services/colab

# Composant partagé
cd shared/copilotage

# Recherche
cd research
```

### Gestion des submodules

```bash
# Initialiser tous les submodules
git submodule update --init --recursive

# Mettre à jour tous les submodules
git submodule update --remote

# Mettre à jour un submodule spécifique
git submodule update --remote modules/core/filesystem
```

## Avantages

- ✅ **Structure claire** : Organisation logique par fonctionnalité
- ✅ **Navigation intuitive** : Chemins descriptifs
- ✅ **Développement modulaire** : Indépendance des composants
- ✅ **Maintenance facilitée** : Séparation des responsabilités
- ✅ **Collaboration optimisée** : Accès centralisé depuis Panini
