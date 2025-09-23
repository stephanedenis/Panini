# 🧬 PaniniFS Research

**Recherche linguistique computationnelle avec accélération GPU**

[![Open Main Notebook](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/stephanedenis/PaniniFS-Research/blob/main/PaniniFS_Colab_GPU.ipynb)

## 🚀 Démarrage Rapide

### 📓 Analyse Dhātu GPU (TESTÉ ✅)
Cliquez sur le badge ci-dessus pour lancer l'analyse dhātu avec accélération GPU dans Colab Pro.

**Performance** : 15x plus rapide que CPU local
- 500 documents en 3-5 secondes
- 2000 documents en 12-15 secondes  
- 10000 documents en 60 secondes

### 🔧 API Locale + Dashboard
```bash
# Lancer le système intégré
python3 scripts/start_colab_integration.py

# Dashboard: http://localhost:5000
```

## 📁 Structure du Projet

### 🧬 Analyse Linguistique
- **`PaniniFS_Colab_GPU.ipynb`** - Notebook principal GPU-optimisé
- **`colab_integration/`** - Workflow GitHub ↔ Colab complet
- **`src/`** - Modules d'analyse dhātu et traitement corpus

### ⚡ Infrastructure Cloud
- **`src/cloud/`** - API REST + intégration Colab
- **`scripts/`** - Automation et synchronisation
- **`src/web/`** - Dashboard monitoring temps réel

### 📊 Données et Résultats
- **`corpus_*.json`** - Corpus multilingues 
- **`analyse_*.json`** - Résultats d'analyses
- **`tech/`** - Outils techniques et validation

## 🎯 Fonctionnalités

### 🧬 Analyse Dhātu Avancée
- **9 patterns universels** : ACTION, COGNITION, EMOTION, etc.
- **Vectorisation sémantique** par document
- **Analyse multilingue** (français, anglais, extensible)
- **Visualisations interactives** des résultats

### 🚀 Accélération GPU
- **Colab Pro integration** testée et validée ✅
- **Synchronisation automatique** GitHub ↔ Colab
- **Export résultats** JSON + Markdown
- **Performance monitoring** en temps réel

### 🔄 Workflow Intégré
```
Local Development → GitHub → Colab GPU → Results → Local Dashboard
```

## 📚 Documentation

- **[COLAB_NOTEBOOKS.md](COLAB_NOTEBOOKS.md)** - Guide notebooks Colab
- **[GUIDE_GITHUB_COLAB_INTEGRATION.md](GUIDE_GITHUB_COLAB_INTEGRATION.md)** - Workflow complet
- **[README_STATUS.md](README_STATUS.md)** - État du projet

## 🏆 Accomplissements Récents

✅ **Notebook Colab fonctionnel** - Testé et validé  
✅ **API REST + WebSockets** - Système hybride opérationnel  
✅ **Dashboard monitoring** - Métriques temps réel  
✅ **Synchronisation GitHub-Colab** - Workflow automatisé  
✅ **Performance GPU** - 15x accélération confirmée  

## 🔗 Liens Utiles

- **Notebook Principal** : [PaniniFS_Colab_GPU.ipynb](https://colab.research.google.com/github/stephanedenis/PaniniFS-Research/blob/main/PaniniFS_Colab_GPU.ipynb)
- **Dashboard Local** : http://localhost:5000 (après démarrage API)
- **Repository Principal** : PaniniFS (intégration submodule)

---

**🧬 PaniniFS Research - Linguistique Computationnelle GPU-Accélérée**
