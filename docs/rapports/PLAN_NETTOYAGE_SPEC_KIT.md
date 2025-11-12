# 🎯 Plan de Nettoyage Repo Principal Panini + Spec Kit Integration

**Date**: 28 Octobre 2025  
**Objectifs**: 
1. Nettoyer le repo principal Panini (253 fichiers à la racine!)
2. Déplacer recherches vers `research/`
3. Préparer Spec Kit pour génération Panini-FS

---

## 📊 État Actuel

### Repo Principal (/home/stephane/GitHub/Panini)
- **253 fichiers** à la racine (chaos)
- Mélange de:
  - Recherches dhātu/sémantique
  - Scripts d'analyse
  - Rapports et documentation
  - Code de recherche PanLang
  - Tests et validations
  
### Repo Research (/home/stephane/GitHub/Panini/research)
- ✅ **Déjà nettoyé** (réorganisation complète aujourd'hui)
- Structure claire avec 12 initiatives

---

## 🎯 Objectif 1: Spec Kit pour Panini-FS

### Qu'est-ce que Spec Kit ?

**Spec Kit** (https://speckit.org/) est l'outil officiel de GitHub pour le **Spec-Driven Development**.

**Philosophie**:
- ✅ Les spécifications deviennent **exécutables**
- ✅ L'IA génère le code automatiquement
- ✅ Focus sur le **quoi** et le **pourquoi**, pas le **comment**
- ✅ Intégration native avec GitHub Copilot

**Workflow Spec Kit**:
```
/constitution → /specify → /clarify → /plan → /tasks → /analyze → /implement
```

### Installation Spec Kit

```bash
# Installation globale (recommandée)
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# Vérifier installation
specify --version

# Vérifier requirements
specify check
```

### Initialisation Projet Panini-FS

```bash
# Créer nouveau repo produit Panini-FS
cd /home/stephane/GitHub
mkdir Panini-FS-Product
cd Panini-FS-Product

# Initialiser avec GitHub Copilot
specify init . --ai copilot

# OU avec Claude (si préféré)
specify init . --ai claude
```

### Phase 1: Constitution & Specification

```bash
# 1. Établir principes du projet
/constitution
Focus on:
- High performance (>100 MB/s ingestion)
- Type safety (Rust + TypeScript)
- Content-addressed storage integrity
- Universal Engine integration
- 100% lossless reconstruction
- Production-ready quality

# 2. Spécifier ce qu'on veut construire
/specify
Build Panini-FS, a universal format digester that decomposes any file format 
into content-addressed primitives and reconstructs them losslessly.

Core features:
- Format detection for 69+ formats (PNG, JPEG, PDF, MP3, etc.)
- Grammar-based decomposition
- Content-addressed storage with SHA-256
- Lossless reconstruction with validation
- IP metadata integration via Universal Engine
- High-performance async processing

Technical requirements:
- Rust backend for core engine
- TypeScript client library
- Support for streaming large files
- Automatic deduplication
- Comprehensive test coverage

See complete specifications in:
- /home/stephane/GitHub/Panini/research/panini-fs/specs/ARCHITECTURE_SPEC.md
- /home/stephane/GitHub/Panini/research/panini-fs/specs/RUST_IMPLEMENTATION_SPEC.md

# 3. Clarifier ambiguïtés
/clarify
(Spec Kit posera des questions ciblées)

# 4. Créer plan technique
/plan
Use Rust for backend with:
- tokio for async runtime
- serde for serialization
- sha2 for content addressing
- pest for grammar parsing
- flate2 for compression

Use TypeScript for client with:
- Zod for validation
- Type-safe API client

Architecture: See ARCHITECTURE_SPEC.md for complete design

# 5. Générer tâches
/tasks

# 6. Analyser cohérence
/analyze

# 7. Implémenter
/implement
```

### Avantages Spec Kit pour Panini-FS

✅ **Spécifications déjà prêtes** dans `research/panini-fs/specs/`
✅ **GitHub Copilot génère le code** automatiquement
✅ **Focus sur architecture** pas sur plumbing
✅ **Qualité production** par défaut
✅ **Tests intégrés** dans le workflow
✅ **Documentation automatique**

---

## 🎯 Objectif 2: Nettoyer Repo Principal

### Analyse des Fichiers à Déplacer

#### Catégorie 1: Recherche Dhātu/Sémantique
**Destination**: `research/semantic-primitives/`

Fichiers à déplacer:
- `ACCOMPLISSEMENTS_FINAUX_CYCLE_DHATU.md`
- `GUIDE_COMPLET_TRIPARTITE_DHATU.md`
- `ANALYSE_COMPARATIVE_DIAGRAMMES_DHATU.md`
- `VALIDATION_VISUELLE_CYCLES_DHATU.md`
- `CORRECTIONS_RENDU_DIAGRAMMES.md`
- `TEST_RENDU_DIAGRAMMES.md`
- `CONFIGURATION_EXTENSIONS_DIAGRAMMES.md`
- `DOCUMENTATION_DIAGRAMMES_CYCLES_DHATU.md`
- `DIAGRAMMES_*`
- `dhatu_*.py`
- `analyseur_semantique_dhatu.py`

#### Catégorie 2: Recherche PanLang
**Destination**: `research/semantic-primitives/panlang/` (nouveau)

Fichiers à déplacer:
- `panlang_*.py`
- `integrateur_panlang.py`
- `rapport_panlang_rapide.py`
- `dictionnaire_recursif_semantique.py`

#### Catégorie 3: Encyclopédies & Analyseurs
**Destination**: `research/ecosystem-analysis/tools/`

Fichiers à déplacer:
- `encyclopedie_compositionnelle_universelle.py`
- `wikipedia_*.py`
- `analyseur_*.py`
- `expansion_*.py`

#### Catégorie 4: Scripts & Outils
**Destination**: `research/shared/scripts/`

Fichiers à déplacer:
- `generate_*.py`
- Autres scripts utilitaires

#### Catégorie 5: Rapports & Documentation
**Destination**: `research/sessions/` ou `research/semantic-primitives/docs/`

Fichiers à déplacer:
- `RAPPORT_*.md`
- `RESUME_*.md`
- Autres rapports de session

### Script de Migration Automatique

```bash
#!/bin/bash
# migrate_to_research.sh

PANINI_ROOT="/home/stephane/GitHub/Panini"
RESEARCH_ROOT="$PANINI_ROOT/research"

cd "$PANINI_ROOT"

# Créer structures manquantes
mkdir -p "$RESEARCH_ROOT/semantic-primitives/panlang"
mkdir -p "$RESEARCH_ROOT/ecosystem-analysis/tools"

# 1. Dhātu Research
echo "📦 Migration recherche dhātu..."
find . -maxdepth 1 -name "*DHATU*" -exec mv {} "$RESEARCH_ROOT/semantic-primitives/docs/" \;
find . -maxdepth 1 -name "*dhatu*.py" -exec mv {} "$RESEARCH_ROOT/semantic-primitives/analysis-scripts/" \;
find . -maxdepth 1 -name "*DIAGRAMMES*" -exec mv {} "$RESEARCH_ROOT/semantic-primitives/docs/" \;

# 2. PanLang Research
echo "📦 Migration PanLang..."
find . -maxdepth 1 -name "panlang*.py" -exec mv {} "$RESEARCH_ROOT/semantic-primitives/panlang/" \;
mv integrateur_panlang.py "$RESEARCH_ROOT/semantic-primitives/panlang/" 2>/dev/null
mv dictionnaire_recursif_semantique.py "$RESEARCH_ROOT/semantic-primitives/panlang/" 2>/dev/null

# 3. Encyclopédies & Analyseurs
echo "📦 Migration analyseurs..."
mv encyclopedie_compositionnelle_universelle.py "$RESEARCH_ROOT/ecosystem-analysis/tools/" 2>/dev/null
find . -maxdepth 1 -name "wikipedia*.py" -exec mv {} "$RESEARCH_ROOT/ecosystem-analysis/tools/" \;
find . -maxdepth 1 -name "analyseur*.py" -exec mv {} "$RESEARCH_ROOT/ecosystem-analysis/tools/" \;
find . -maxdepth 1 -name "expansion*.py" -exec mv {} "$RESEARCH_ROOT/ecosystem-analysis/tools/" \;

# 4. Scripts génériques
echo "📦 Migration scripts..."
find . -maxdepth 1 -name "generate*.py" -exec mv {} "$RESEARCH_ROOT/shared/scripts/" \;

# 5. Rapports
echo "📦 Migration rapports..."
find . -maxdepth 1 -name "RAPPORT*.md" -exec mv {} "$RESEARCH_ROOT/sessions/" \;
find . -maxdepth 1 -name "RESUME*.md" -exec mv {} "$RESEARCH_ROOT/sessions/" \;
find . -maxdepth 1 -name "GUIDE*.md" -exec mv {} "$RESEARCH_ROOT/semantic-primitives/docs/" \;

# 6. Fichiers JSON de données
echo "📦 Migration données..."
find . -maxdepth 1 -name "*.json" -exec mv {} "$RESEARCH_ROOT/misc/data/" \;

echo "✅ Migration terminée!"
```

### Structure Finale Souhaitée

**Repo Principal (Panini)** - Production seulement:
```
Panini/
├── README.md                    # Vue d'ensemble écosystème
├── LICENSE
├── .gitignore
├── .github/                     # CI/CD workflows
├── docs/                        # Documentation utilisateur
├── panini/                      # Package Python principal
│   ├── __init__.py
│   ├── core/
│   ├── formats/
│   └── utils/
├── tests/                       # Tests du package
├── examples/                    # Exemples d'utilisation
├── pyproject.toml              # Config Python package
└── research/                    # Submodule → Panini-Research repo
```

**Repo Research** - Recherche seulement:
```
Panini-Research/
├── README.md
├── panini-fs/                   # Specs digesteur formats
├── universal-engine/            # IP System complet
├── semantic-primitives/         # Dhātu + PanLang
│   ├── analysis-scripts/
│   ├── panlang/                 # ← Nouveau
│   ├── docs/
│   └── results/
├── ecosystem-analysis/
│   └── tools/                   # ← Analyseurs déplacés
├── ...
```

---

## 📋 Plan d'Exécution

### Étape 1: Installer Spec Kit ⏱️ 5 min

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
specify --version
specify check
```

### Étape 2: Créer Repo Produit Panini-FS ⏱️ 10 min

```bash
cd /home/stephane/GitHub
mkdir Panini-FS-Product
cd Panini-FS-Product
git init
specify init . --ai copilot
```

### Étape 3: Exécuter Workflow Spec Kit ⏱️ 1-2 heures

```bash
# Dans VS Code avec GitHub Copilot
/constitution     # Établir principes
/specify          # Référencer specs de research/
/clarify          # Répondre aux questions
/plan             # Plan technique Rust + TypeScript
/tasks            # Décomposer en tâches
/analyze          # Vérifier cohérence
/implement        # Générer le code!
```

### Étape 4: Backup Repo Principal ⏱️ 2 min

```bash
cd /home/stephane/GitHub/Panini
git add -A
git commit -m "📸 Snapshot avant nettoyage repo principal"
git push origin main
tar -czf ../panini_backup_$(date +%Y%m%d_%H%M%S).tar.gz .
```

### Étape 5: Migrer vers Research ⏱️ 30 min

```bash
cd /home/stephane/GitHub/Panini
bash migrate_to_research.sh
```

### Étape 6: Vérifier & Commit ⏱️ 15 min

```bash
# Vérifier structure
find . -maxdepth 1 -type f | wc -l  # Devrait être ~10-20

# Commit
cd /home/stephane/GitHub/Panini
git add -A
git commit -m "🗂️ Nettoyage repo principal: migration recherches vers research/"
git push origin main

cd research
git add -A
git commit -m "📦 Ajout recherches dhātu/PanLang depuis repo principal"
git push origin main
```

---

## 🎯 Résultat Final

### Séparation Claire

**Panini (Repo Principal)**:
- ✅ Package Python production
- ✅ Documentation utilisateur
- ✅ Exemples
- ✅ CI/CD
- ✅ 10-20 fichiers racine max

**Panini-Research**:
- ✅ Toutes les recherches
- ✅ Prototypes
- ✅ Analyses
- ✅ Specs pour produits

**Panini-FS-Product**:
- ✅ Généré par Spec Kit
- ✅ Code Rust + TypeScript
- ✅ Qualité production
- ✅ Tests automatiques

### Workflow Futur

```
Recherche → Specs → Spec Kit → Produit
   ↓          ↓         ↓          ↓
Research  panini-fs/ GitHub   Panini-FS
  repo     /specs/   Copilot   Product
```

---

## 🚀 Commencer Maintenant ?

1. **Priorité 1**: Installer Spec Kit et initialiser Panini-FS-Product
2. **Priorité 2**: Migrer recherches du repo principal vers research/
3. **Priorité 3**: Exécuter workflow Spec Kit pour générer Panini-FS

**Prêt à commencer ?** 🎯
