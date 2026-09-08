# Instructions Copilot — Projet Panini

## Les 4 projets de l'écosystème (architecture réelle, août 2026)

| Projet | Rôle | Repo | Langage | Priorité |
|--------|------|------|---------|----------|
| **NIPADA** | Moteur de sémantique computationnelle NP-complet | `Panini-Research/src/nipada/` | Python 3.13 | 🔴 LE PRODUIT |
| **Panini-FS** | Stockage sémantique + FUSE3 (Rust) | `modules/core/filesystem/` | Rust/Python | 🔴 CORE |
| **OntoWave** | Visualisation ontologique | `modules/ontowave/` | TypeScript/Node | 🟡 PRODUCTION |
| **Pensine-Web** | Journal de connaissances (app finale) | repo séparé | JavaScript | 🔴 URGENT |

### Ce que chaque projet FAIT (et ne fait PAS)

- **NIPADA** = computation du sens (LE produit) : **noyau iso** (14 atomes V14 + 9 dhātus + logique trinaire Ł3 + TrinarySAT + DTP) assisté de sa **couche descriptive** (graphe encyclopédique flou) → décompose le texte et le reconstruit via DTP (0 % WER). Dans le pipeline E2E, la synthèse DTP est un `compile()` déterministe ; TrinarySAT (SAT trinaire) est la voie `compute` pour la reconstruction difficile (action 1.6 — `research/philosophy-theory/VERIFICATION_FONDATIONS_PAR_NIVEAUX_v0.1.md`).
- **Panini-FS** = stockage sémantique. RocksDB + Tantivy + FUSE3 → stocke, versionne, synchronise les données sémantiques. Infrastructure, pas produit.
- **OntoWave** = visualisation. Affiche les graphes ontologiques → consommé par Pensine-Web et l'Explorer. Infrastructure, pas produit.
- **Pensine-Web** = application utilisateur. Journal de connaissances qui utilise l'API Panini-FS + OntoWave.

### Flux de dépendances
```
Panini-FS (fondation) → OntoWave (affichage) → Pensine-Web (app)
NIPADA (recherche) → résultats validés → Panini-FS (stockage)
```

## Ce qui distingue NIPADA (à savoir avant toute intervention)

### NIPADA n'est PAS un LLM
- **Fondation** : algébrique (14 atomes + 9 dhātus) ≠ statistique (100B+ paramètres)
- **Déterminisme** : SAT-solveur déterministe ≠ stochastique
- **Hallucination** : 0% ≠ 3.2% (GPT-4)
- **Vitesse** : 10.9ms ≠ 1200ms GPT-4 (110× plus rapide)
- **Coût** : $0 ≠ $100M+ entraînement
- **Traçabilité** : chaîne de provenance complète ≠ boîte noire
- **Source** : §614, journal 2026-06-30

### NIPADA n'est PAS une grammaire générative chomskyenne
- **Domaine** : sémantique ≠ syntaxe
- **Génère** : texte depuis atomes V14 + Dhātus ≠ phrases depuis règles NP/VP
- **Validation** : WER vs original ≠ jugement de grammaticalité
- **Source** : §674, journal 2026-07-02

### NIPADA n'est PAS un système expert
- **Primitives** : 14 atomes universels ≠ règles métier spécifiques
- **Domaine** : universel (tout texte) ≠ spécifique (MYCIN=médecine)
- **Construction** : automatique (pipeline NLP) ≠ manuelle (experts)
- **Réseau** : diachronique (généalogie) ≠ synchronique (état figé)
- **Source** : §562-§568, journal 2026-06-28

### Ce que NIPADA fait qu'aucun autre système ne fait
1. Décomposition déterministe (texte → atomes de sens) — pas d'approximation
2. Reconstruction par SAT-solver (atomes → DTP → texte identique) — pas de génération
3. Graphe généalogique comme tissu computationnel — pas un dictionnaire
4. NP-complétude comme architecture : décomposition polynomiale, reconstruction NP-difficile
5. Vérifiabilité totale : chaque étape traçable, résultat comparé via WER

## Machine Hauru

- **OS** : openSUSE, kernel 7.1.4
- **CPU** : 2× Intel Xeon E5-2687W v3 (40 cœurs)
- **RAM** : 125 Go
- **GPU** : 2× NVIDIA Quadro RTX 5000 (16 Go, CUDA 13.0)
- **Python** : 3.13.14 → `.venv/` (virtualenv local)
- **Rust** : 1.97.1 (rustup)
- **FPGA** : Stratix V (Storey Peak) — IP PCIe pas programmée, via USB/JTAG

## Structure du projet

```
Panini/
├── copilotage/      # Submodule Panini-Copilotage — directives partagées
├── src/             # Code source Panini Hub (panini_colabmcp)
├── modules/         # Submodules: core/filesystem, ontowave, orchestration...
├── research/        # Submodule → Panini-Research = NIPADA (LE LABO PRINCIPAL)
├── docs/            # Documentation, rapports, journaux (docs/journal-de-bord/)
├── notebooks/       # Jupyter notebooks
├── scripts/         # Scripts utilitaires
├── tests/           # Tests unitaires et d'intégration
├── tech/            # Prototypes et expérimentations
├── tools/           # Outils de développement
├── data/            # Données (corpus, références, résultats)
└── config/          # Configuration agents et système
```

## Où est le code NIPADA ?

⚠️ Le code principal NIPADA n'est PAS dans `src/` — il est dans le repo **Panini-Research** :
- Chemin local : `~/Data13TB/stephane/GitHub/Panini-Research/src/nipada/`
- Submodule : `Panini/research/` pointe vers ce repo
- Le Hub (`src/`) contient le code d'orchestration (GitHub sync, Colab, cloud)

## Référence rapide anti-hallucination

La mémoire persistante `/memories/repo/nipada-cheat-sheet.md` contient :
- Toutes les métriques exactes (R², WER, tailles de graphe)
- Les 10 pièges critiques
- Les chemins de fichiers exacts
- La chronologie des percées

**À consulter en début de chaque session.**

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

### Anti-ASCII
- **INTERDIT** : ASCII art ou diagrammes en caractères dans le code, les documents, ou les réponses.
- **OBLIGATOIRE** : utiliser diagram-as-code (Mermaid, Kroki) ou SVG externalisé (fichier `.svg` séparé, référencé via `![description](path.svg)` dans le markdown).
- **Pas de SVG inline/embeddé** dans les fichiers `.md`.

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



---

## 🧭 Architecture sémantique Panini — deux niveaux, jamais confondus

- **Noyau (iso)** = moteur rigide / mathématique : 14 atomes V14 (encodage leibnizien), 9 dhātus, logique trinaire Ł3 (exacte — pas du flou), TrinarySAT, DTP, graphe = tissu computationnel. Il **infère** (directement ou par réalités émergentes), il est déterministe ; il **ne décrit jamais** aucun corpus.
- **NIPADA — couche descriptive** = encyclopédie en logique floue (Zadeh, poids [0,1]) : graphe encyclopédique de métadonnées, graphe de transmission généalogico-culturel, corpus. Elle **décrit la réalité observable** et fournit les paramètres que le noyau n'infère pas (régime descriptif R4 : fiction, oral, presse…).
- **NIPADA — produit** = instanciation complète du noyau dans le langage naturel : **noyau + couche descriptive** (le produit contient les deux niveaux).
- **Principe de séparation** : *le noyau ne décrit jamais — il infère ; NIPADA décrit ce que le noyau ne peut inférer.* Mêmes atomes et opérateurs aux deux niveaux ; seule la **source des paramètres** diffère (inférence vs description).
- **Versionnement couplé** : un noyau n'est testable qu'à travers sa NIPADA — on teste le couple **Kᵢ + NIPADAᵢ**, jamais un noyau seul (les corpus signés v271, v272… sont des versions de la couche descriptive).
- Vocabulaire figé : « NIPADA en logique floue » désigne **uniquement la couche descriptive** (niveau 2) ; Ł3 ≠ flou ; trois usages du flou (Zadeh pragmatique / Ł3 moteur / poids du graphe) = **un seul système** à décrire comme tel.
- Référence canonique : `PaniniResearch/Panini-Research` → `docs/ARCHITECTURE_NOYAU_NIPADA_v1.0.md` (dérivée de `philosophy-theory/DOCUMENT_DE_CONTEXTE_v2.0.md` §2.1).
