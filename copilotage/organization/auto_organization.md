# 📁 Directives d'Organisation Automatique

## 🎯 Principe d'Organisation

Tous les fichiers créés dans ce projet doivent automatiquement être placés dans la structure organisée appropriée :

### 📂 Structure Cible

```
PaniniFS-Research/
├── src/                    # Code source principal
│   ├── modules/           # Modules modulaires
│   ├── github_sync/       # Système GitHub-Sync
│   └── interfaces/        # Interfaces communes
├── notebooks/             # Notebooks Jupyter (GitHub-Sync uniquement)
├── docs/                  # Documentation organisée
│   ├── guides/           # Guides d'utilisation
│   ├── rapports/         # Rapports techniques
│   ├── journaux/         # Journaux de session
│   └── architecture/     # Documentation architecture
├── config/               # Fichiers de configuration
├── temp/                 # Fichiers temporaires
│   └── logs/            # Logs système
├── copilotage/          # Directives et contrôle
│   ├── directives/      # Directives stratégiques
│   ├── vscode/          # Configuration VS Code
│   └── organization/    # Règles d'organisation
└── tools/               # Outils et scripts
```

## 🤖 Règles pour GitHub Copilot

### 📝 Création de Documentation
- **Guides** → `docs/guides/`
- **Rapports** → `docs/rapports/`
- **Journaux** → `docs/journaux/`
- **Architecture** → `docs/architecture/`

### 🐍 Création de Code
- **Modules Python** → `src/modules/`
- **Scripts** → `tools/`
- **Tests** → `tests/`

### 📓 Création de Notebooks
- **Notebooks Jupyter** → `notebooks/` (GitHub-Sync uniquement)
- **Archive anciens** → SUPPRIMER (ne pas créer)

### ⚙️ Fichiers Configuration
- **JSON/YAML** → `config/`
- **Logs** → `temp/logs/`
- **Cache** → `temp/cache/`

### 📋 Directives Copilotage
- **Stratégies** → `copilotage/directives/`
- **Config VS Code** → `copilotage/vscode/`
- **Organisation** → `copilotage/organization/`

## 🔧 Instructions Automatisation

### Pour GitHub Copilot :
1. **TOUJOURS** vérifier la structure cible avant création
2. **JAMAIS** créer à la racine si un dossier approprié existe
3. **UTILISER** les chemins complets avec structure organisée
4. **PRÉFÉRER** organisation thématique

### Exemples de Chemins :
```bash
# ✅ CORRECT
src/modules/analyzer/new_analyzer.py
docs/guides/usage_guide.md
config/app_settings.json
temp/logs/session.log

# ❌ INCORRECT  
new_analyzer.py
usage_guide.md
app_settings.json
session.log
```

## 🎯 Cas Spéciaux

### Notebooks Jupyter
- **Autorisés** : Seulement GitHub-Sync dans `notebooks/`
- **Interdits** : Tous autres notebooks
- **Action** : Supprimer anciens, créer nouveaux dans structure

### Fichiers Temporaires
- **Logs** → `temp/logs/`
- **Cache** → `temp/cache/`
- **Build** → `temp/build/`

### Configuration
- **VS Code** → `.vscode/` ET `copilotage/vscode/`
- **Git** → `.gitignore` (mise à jour pour structure)
- **Python** → `config/python.json`

## 🚀 Automatisation VS Code

Utiliser les paramètres VS Code pour :
1. **Auto-placement** des nouveaux fichiers
2. **Templates** avec chemins corrects
3. **Tasks** respectant l'organisation
4. **Extensions** configurées pour structure

## ⚠️ Règles Strictes

1. **RACINE PROPRE** : Maximum 5 fichiers à la racine
2. **PAS DE NOTEBOOKS** sauf GitHub-Sync
3. **PAS DE LOGS** à la racine
4. **PAS DE CONFIGS** temporaires à la racine
5. **ORGANISATION** systématique obligatoire

## 🔄 Maintenance Continue

- Vérification structure chaque session
- Nettoyage automatique fichiers mal placés
- Mise à jour directives selon évolution
- Formation continue Copilot sur organisation