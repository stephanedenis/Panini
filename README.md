# 🧬 Panini — Moteur de Décomposition et Recomposition Sémantique

[![Architecture](https://img.shields.io/badge/Architecture-6_Projets-blue)](docs/ARCHITECTURE_REAL_6PROJECTS.md)
[![Documentation](https://img.shields.io/badge/Docs-Complète-orange)](docs/)
[![Python](https://img.shields.io/badge/Python-3.10+-green)](pyproject.toml)
[![Licence](https://img.shields.io/badge/Licence-Voir_LICENSE-lightgrey)](LICENSE)

## 📋 Vue d'Ensemble

**Panini** est un système d'analyse sémantique basé sur les **dhātu sanskrits** — 9 patrons universels qui permettent de décomposer n'importe quel contenu en primitives atomiques et de le reconstruire avec **100% d'intégrité bit-perfect**.

L'approche : décomposer → représenter sémantiquement → recomposer sans perte. Panini-FS exploite cette capacité pour la compression de données ; Pensine-Web l'exploite pour la gestion des connaissances.

### ✨ Caractéristiques Principales

- 🧬 **Décomposition atomique** — 9 dhātu universels couvrent tous les patrons sémantiques
- 🔒 **Intégrité bit-perfect** — Reconstruction 100% garantie
- 📦 **Content-Addressed Storage (CAS)** — Déduplication sémantique avancée
- 🔍 **Primitives universelles** — Indépendant de la langue source
- 🌐 **Visualisation ontologique** — Interface OntoWave (TypeScript/Node)

## 🏗️ Écosystème (6 Projets)

| Projet | Rôle | Tech | Priorité |
|--------|------|------|----------|
| **Panini-FS** | Moteur de décomposition sémantique + lecteur FUSE3 | Rust/Python | 🔴 CORE |
| **OntoWave** | Couche de visualisation ontologique | TypeScript/Node | 🟡 PRODUCTION |
| **Pensine-Web** | Journal de connaissances (remplace Logseq) | JavaScript | 🔴 URGENT |
| **Panini-Research** | Laboratoire d'exploration et prototypage | Python | 🟢 RECHERCHE |
| **SemanticAutomation** | Workflows d'analyse sémantique | TBD | 🟡 FUTUR |
| **Support** | Utilitaires partagés et infrastructure | Divers | 🟢 SUPPORT |

→ Architecture complète : [docs/ARCHITECTURE_REAL_6PROJECTS.md](docs/ARCHITECTURE_REAL_6PROJECTS.md)

## 📁 Structure du Dépôt

```
Panini/
├── copilotage/         # Règles, directives et journaux d'agent
├── src/                # Code source principal (package panini_colabmcp)
├── modules/            # Submodules Git actifs (9 composants)
├── docs/               # Documentation, rapports et journaux
├── notebooks/          # Jupyter notebooks (développement)
├── research/           # Submodule Panini-Research (laboratoire)
├── scripts/            # Scripts utilitaires
├── tests/              # Tests unitaires et d'intégration
├── tech/               # Prototypes et expérimentations techniques
├── tools/              # Outils de développement
├── data/               # Données (corpus, références, résultats)
└── config/             # Configuration agents et système
```

## 🚀 Démarrage Rapide

```bash
# Cloner avec les submodules
git clone --recursive https://github.com/stephanedenis/Panini.git
cd Panini

# Installer l'environnement Python
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Pour le laboratoire de recherche :

```bash
cd research
# Voir research/README.md
```

## 📚 Documentation

- [**Index de la documentation**](docs/index.md) — Point d'entrée unique
- [**Architecture (6 projets)**](docs/ARCHITECTURE_REAL_6PROJECTS.md) — Référence canonique
- [**Journal de bord**](docs/journal-de-bord/) — Historique des décisions
- [**Rapports**](docs/rapports/) — Rapports de session archivés

## 🛠️ Développement

### Contribuer

1. **Fork** le repository principal ou le submodule concerné
2. **Créer** une branche feature (`git checkout -b feature/ma-feature`)
3. **Commit** (`git commit -m 'feat: description'`)
4. **Push** et ouvrir une Pull Request

### Submodules actifs

```bash
# Mettre à jour tous les submodules
git submodule update --remote

# Initialiser le submodule research
git submodule update --init research
```

## 🎯 État Actuel & Roadmap

- ✅ Architecture 6-projets définie et documentée
- ✅ Submodule Panini-Research initialisé
- ✅ Package Python `panini-colabmcp` v0.1.0 structuré
- 🔜 Panini-FS : moteur de décomposition sémantique (MVP)
- 🔜 Pensine-Web : interface de journalisation (lancement urgent)
- 🔜 Tests d'intégration cross-module

Roadmap détaillée : [docs/ROADMAP_PHASED_4PHASES.md](docs/ROADMAP_PHASED_4PHASES.md)

## 📞 Contact & Support

- **Issues** : [GitHub Issues](https://github.com/stephanedenis/Panini/issues)
- **Discussions** : [GitHub Discussions](https://github.com/stephanedenis/Panini/discussions)

## 📄 Licence

Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

**Projet Panini** - *From chaos to clarity* 🚀  
Architecture v2.0 - Novembre 2025
