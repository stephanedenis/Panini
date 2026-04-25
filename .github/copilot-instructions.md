# Instructions Copilot — Projet Panini

## Contexte du projet

**Panini** est un système de compression sémantique basé sur les dhātu sanskrits. Il décompose tout format de fichier en primitives atomiques et le reconstruit avec une intégrité bit-perfect.

- **Langage principal:** Python 3.10+
- **Environnement:** `.venv/` (virtualenv local)
- **Architecture:** Modulaire — 12 submodules indépendants sous `modules/`
- **Source principale:** `src/`

## Structure du projet

```
Panini/
├── copilotage/      # Règles, directives et journaux d'agent — lire en priorité
├── src/             # Code source principal
├── modules/         # 12 submodules (compression, corpus, dhatu, web, etc.)
├── docs/            # Documentation et rapports
├── notebooks/       # Jupyter notebooks (développement et expérimentation)
├── scripts/         # Scripts utilitaires
├── tests/           # Tests unitaires et d'intégration
├── research/        # Submodule Panini-Research
├── tech/            # Prototypes et expérimentations techniques
├── tools/           # Outils de développement
├── data/            # Données (corpus, références, résultats)
└── config/          # Configuration agents et système
```

## Règles de copilotage

### Autonomie
- **AUTO_TOOL_VALIDATION:** Avant tout `run_in_terminal` ou subprocess direct, proposer l'outil copilotage équivalent.
- **MISSION_AUTONOMY_ENFORCER:** Pour toute mission estimée > 2h, éliminer toutes les micro-validations.
- **CONTINUOUS_LEARNING_LOGGER:** Capturer patterns, erreurs et succès dans `copilotage/journal/`.

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

- **Emplacement :** `docs/journal-de-bord/YYYY-MM-DD.md`
- **Format du nom :** date locale du jour, **un seul fichier par jour** (ex: `2026-04-25.md`). Pas de suffixe d'heure.
- **Contenu minimal :**
  - Résumé des décisions prises durant la session
  - Raisonnements importants (pourquoi ce choix et pas un autre)
  - Problèmes rencontrés et solutions retenues
  - État des travaux en cours (ce qui reste à faire)
- L'agent doit créer ou mettre à jour l'entrée de journal **avant** d'exécuter le commit.
- **Avant tout commit, vérifier la date courante** (`date +%Y-%m-%d`) et basculer sur le fichier du jour si la session traverse minuit.
- Toute nouvelle section dans la même journée s'ajoute au fichier existant — ne jamais créer un second fichier pour la même date.

## Workflow standard

1. **Analyser** → Script Python dans `scripts/` ou module dans `src/`
2. **Tester** → Test dans `tests/`
3. **Documenter** → Rapport dans `docs/rapports/` ou `copilotage/journal/`
4. **Valider** → Mise à jour du cache dans `data/references_cache/`
5. **Journaliser** → Entrée dans `docs/journal-de-bord/` avant tout commit

## Références clés à consulter

- `copilotage/regles/REGLES_COPILOTAGE_v0.0.2.md` — règles d'autonomie agent
- `copilotage/directives/architecture_modulaire.md` — conventions architecture
- `ARCHITECTURE_STANDARD.md` — vue d'ensemble de l'architecture
- `pyproject.toml` — dépendances et configuration Python
