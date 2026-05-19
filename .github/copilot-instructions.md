# Instructions Copilot — Projet Panini

## Contexte du projet

**Panini** est un système de **décomposition sémantique** basé sur les dhātu sanskrits. Il décompose le contenu en primitives sémantiques et le reconstruit avec une intégrité bit-perfect. Ce n'est PAS un outil de compression générique.

- **Langage principal:** Python 3.10+
- **Environnement:** `.venv/` (virtualenv local)
- **Architecture:** Écosystème de 6 projets (voir `docs/ARCHITECTURE_REAL_6PROJECTS.md`)
- **Source principale:** `src/`

## Les 6 projets de l'écosystème

| Projet | Rôle | Priorité |
|--------|------|----------|
| **Panini-FS** | Moteur de décomposition sémantique + lecteur FUSE3 (Rust/Python) | 🔴 CORE |
| **OntoWave** | Couche de visualisation ontologique (TypeScript/Node) | 🟡 PRODUCTION |
| **Pensine-Web** | Journal de connaissances (remplace Logseq) (JavaScript) | 🔴 URGENT |
| **Panini-Research** | Laboratoire d'exploration et prototypage (Python) | 🟢 RECHERCHE |
| **SemanticAutomation** | Workflows d'analyse sémantique | 🟡 FUTUR |
| **Support** | Utilitaires partagés et infrastructure | 🟢 SUPPORT |

## Structure du projet

```
Panini/
├── copilotage/      # Submodule Panini-Copilotage — directives et protocoles partagés de l'écosystème
├── src/             # Code source principal (package panini_colabmcp)
├── modules/         # Submodules actifs (core, orchestration, reactive, publication, missions, data, ontowave)
├── docs/            # Documentation, rapports et journaux (docs/journal-de-bord/)
├── notebooks/       # Jupyter notebooks (développement et expérimentation)
├── scripts/         # Scripts utilitaires
├── tests/           # Tests unitaires et d'intégration
├── research/        # Submodule Panini-Research (laboratoire d'exploration)
├── tech/            # Prototypes et expérimentations techniques
├── tools/           # Outils de développement
├── data/            # Données (corpus, références, résultats)
└── config/          # Configuration agents et système
```

## Règles de copilotage

### Autonomie
- **AUTO_TOOL_VALIDATION:** Avant tout `run_in_terminal` ou subprocess direct, proposer l'outil copilotage équivalent.
- **MISSION_AUTONOMY_ENFORCER:** Pour toute mission estimée > 2h, éliminer toutes les micro-validations.
- **CONTINUOUS_LEARNING_LOGGER:** Capturer patterns, erreurs et succès dans `docs/journal-de-bord/`.

### Commandes complexes
Si une commande dépasse 3 paramètres, chaîne plusieurs outils, ou contient une logique conditionnelle → créer un fichier Python dédié plutôt qu'une commande inline.

### Gestion des modifications
- Ne jamais modifier `legacy/` sauf demande explicite.
- Les nouvelles fonctionnalités vont dans `src/` ou le module approprié sous `modules/`.
- Toute expérimentation technique va dans `tech/` ou `notebooks/`.

## Conventions de nommage

| Type | Format |
|------|--------|
| Rapports | `RAPPORT_[SUJET]_v[X.Y.Z].md` |
| Analyses | `ANALYSE_[DOMAINE]_[DETAILS].md` |
| Cache/données | `CACHE_[TYPE]_[VERSION].json` |
| Validation | `VALIDATION_[SCOPE]_[VERSION].md` |
| Scripts Python | `snake_case.py` |
| Modules | `snake_case/` avec `__init__.py` |

## Journal de bord

**OBLIGATION — tout commit doit être accompagné d'une entrée de journal.**

Chaque dépôt tient son propre journal dans `docs/journal-de-bord/`. Les règles complètes sont dans `copilotage/regles/REGLES_JOURNAL_v1.md` (submodule Panini-Copilotage).

Résumé des règles :
- **Emplacement :** `docs/journal-de-bord/YYYY-MM-DD.md` (un seul fichier par jour)
- **Avant tout commit :** créer/mettre à jour le fichier du jour puis le stager
- **Vérifier la date :** `date +%Y-%m-%d` — basculer sur le fichier du nouveau jour si la session traverse minuit
- **Contenu minimal :** contexte, décisions (avec raisonnement), problèmes/solutions, état en fin de session

## Workflow standard

1. **Analyser** → Script Python dans `scripts/` ou module dans `src/`
2. **Tester** → Test dans `tests/`
3. **Documenter** → Rapport dans `docs/rapports/` ou `copilotage/journal/`
4. **Valider** → Mise à jour du cache dans `data/references_cache/`
5. **Journaliser** → Entrée dans `docs/journal-de-bord/` avant tout commit

## Références clés à consulter

- `copilotage/regles/REGLES_COPILOTAGE_v0.0.2.md` — règles d'autonomie agent
- `copilotage/directives/architecture_modulaire.md` — conventions architecture
- `docs/ARCHITECTURE_REAL_6PROJECTS.md` — vue d'ensemble de l'architecture (6 projets)
- `pyproject.toml` — dépendances et configuration Python
