# 🌐 OPTIONS D'APPLICATION DES OPTIMISATIONS

## 📋 Portée Actuelle

### ✅ Appliqué SEULEMENT à PaniniFS-Research
- Configuration Pylance haute performance
- Extensions affinity optimisée  
- Associations fichiers .dhatu/.panini
- Monitoring intelligent du workspace

### 🎯 Options d'Extension

#### Option 1: Configuration Globale (Recommandée)
```bash
# Appliquer les optimisations à TOUS vos projets VS Code
cp .vscode/settings.json ~/.config/Code/User/settings.json.backup
# Puis fusionner les optimisations génériques
```

**Bénéfices:**
- ✅ Tous projets Python optimisés
- ✅ Pylance haute performance partout
- ✅ Extensions intelligemment réparties
- ✅ GPU acceleration globale

**Risques:**
- ⚠️ Peut conflictuer avec configs spécifiques
- ⚠️ Consommation mémoire accrue sur petits projets

#### Option 2: Template Réutilisable
```bash
# Créer un template pour nouveaux projets
mkdir ~/.config/Code/templates/
cp .vscode/settings.json ~/.config/Code/templates/high-performance.json
```

**Bénéfices:**
- ✅ Choix manuel par projet
- ✅ Configs spécialisées possibles
- ✅ Pas de conflit

#### Option 3: Hybride Intelligent
```json
// Settings globaux: optimisations génériques
{
  "terminal.integrated.gpuAcceleration": "on",
  "python.analysis.autoImportCompletions": true,
  "extensions.experimental.affinity": {...}
}

// Settings workspace: spécifiques PaniniFS
{
  "files.associations": {"*.dhatu": "python"},
  "python.analysis.extraPaths": ["./panini", "./dhatu"]
}
```

## 🚀 Recommandation

### Pour Machine Puissante (16 cores, 62GB)
**Appliquer globalement** les optimisations génériques:
- Extensions affinity
- GPU acceleration  
- Pylance haute performance
- Indexation complète

### Garder Spécifique au Workspace
- Associations fichiers custom (.dhatu, .panini)
- Chemins Python spécifiques
- Configurations projet-specific

## 🎛️ Configuration Hybride Optimale

### Global (~/.config/Code/User/settings.json)
```json
{
  "python.analysis.autoImportCompletions": true,
  "python.analysis.indexing": true,
  "python.analysis.memory.keepLibraryAst": true,
  "extensions.experimental.affinity": {
    "ms-python.vscode-pylance": 1,
    "ms-python.python": 1
  },
  "terminal.integrated.gpuAcceleration": "on",
  "workbench.experimental.enableNewProfilesUI": true,
  "editor.semanticHighlighting.enabled": true,
  "editor.bracketPairColorization.enabled": true
}
```

### Workspace (projet-specific)
```json
{
  "python.defaultInterpreterPath": "./.venv/bin/python",
  "files.associations": {
    "*.dhatu": "python",
    "*.panini": "python"  
  },
  "python.analysis.extraPaths": ["./panini", "./dhatu"]
}
```

---
**Question**: Souhaitez-vous que j'applique la **configuration hybride** ?