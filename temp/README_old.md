# PaniniFS Research# PaniniFS-Research



Système de recherche linguistique avancé avec architecture modulaire événementielle.Research repository for Panini-inspired linguistic analysis and computational framework development.



## 🏗️ Architecture## 🎯 **ANALYSE DHĀTU SUR CORPUS RÉEL - REPRODUCTION VALIDÉE**



```Cette recherche démontre l'extraction et l'analyse d'**atomes dhātu** depuis un corpus de **478 documents authentiques** collectés depuis des sources externes réelles (Wikipedia, arXiv, Project Gutenberg, RSS News, Academic papers, Forums).

PaniniFS-Research/

├── src/                    # Code source principal### 📊 **Résultats Reproductibles**

│   ├── core/              # Système de base et événements- ✅ **478 documents authentiques** depuis 9 sources externes

│   ├── web/               # Interfaces web et dashboards- ✅ **2,654 atomes dhātu** extraits par algorithmes linguistiques

│   ├── utils/             # Utilitaires système- ✅ **108 patterns dhātu** identifiés cross-linguistiquement

│   ├── analysis/          # Analyseurs linguistiques- ✅ **10 langues naturelles** avec 52.2% ratio cross-linguistique  

│   ├── corpus/            # Collecteurs et processeurs de corpus- ✅ **Validation automatique** de tous les critères

│   ├── research/          # Systèmes autonomes et pipelines

│   └── dhatu/             # Analyse aspectuelle et morphologique### 🚀 **Reproduction en Une Commande**

├── scripts/               # Scripts de contrôle et lancement```bash

├── data/                  # Données, logs et configurationscd web && ./demo_reproduction.sh

├── legacy/                # Code historique et tests```

└── docs/                  # Documentation**Durée** : 8-16 minutes | **Prérequis** : Python 3.8+, internet



```### 📚 **Documentation Complète**

- 📋 [Guide de reproduction détaillé](REPRODUCTION_GUIDE.md)

## 🚀 Démarrage Rapide- 🔬 [README reproduction](web/README_REPRODUCTION.md)

- 🔍 [Script de validation](web/validate_reproduction.py)

### Lancement du système principal- 📊 [Checksums de vérification](web/checksums.sha256)

```bash

python3 scripts/main.py## Structure

```

- `seed/` - Contenu migré depuis `.seed_research/` du repository principal

### Contrôle du système- `experiments/` - Expériences en cours

```bash- `discoveries/` - Découvertes documentées

python3 scripts/status.py        # Statut- `protocols/` - Méthodologies et protocoles de recherche

python3 scripts/stop.py          # Arrêt complet- `scripts/` - Scripts utilitaires pour la recherche

```

## Migration

### Lancement des composants individuels

```bashCe repository a été créé pour centraliser tout le contenu de recherche précédemment dispersé dans le repository principal PaniniFS.

python3 scripts/run_event_system.py    # Système événementiel

python3 scripts/run_dashboard.py       # Dashboard web### Contenu migré

```

- `.seed_research/` → `seed/`

## 📊 Surveillance- Scripts de recherche → `scripts/`

- Documentation de recherche → documentation appropriée

- **Dashboard Web**: `http://localhost:8890`

- **Métriques système**: Temps réel via API REST## Usage

- **Logs**: Centralisés dans `data/`

Ce submodule est intégré au repository principal PaniniFS dans le dossier `RESEARCH/`.

## 🎯 Fonctionnalités

- **Système événementiel** avec affinité CPU
- **Architecture modulaire** avec réutilisation maximale
- **Dashboards web** temps réel
- **Processeurs de corpus** multilingues
- **Analyseurs linguistiques** avancés
- **Pipelines de recherche** autonomes

## 🛠️ Développement

Le code est organisé en modules Python réutilisables avec une séparation claire des responsabilités.

### Structure des modules

- `src.core`: Classes de base pour gestion système et événements
- `src.web`: Composants web et dashboards
- `src.utils`: Utilitaires de haut niveau
- `src.analysis`: Analyseurs et validateurs
- `src.corpus`: Collecte et traitement de corpus
- `src.research`: Recherche autonome et pipelines

## 📝 Configuration

Les configurations sont centralisées dans `data/` et peuvent être modifiées via les utilitaires système.

---

*Architecture modulaire avec maximum de réutilisation de code*