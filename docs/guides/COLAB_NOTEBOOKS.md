# 🧬 PaniniFS Research - Notebooks GPU

## 🚀 Accès Direct Colab Pro

### 📓 Notebook Principal
**PaniniFS_Colab_GPU.ipynb** - Analyse dhātu avec accélération GPU

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/stephanedenis/PaniniFS-Research/blob/main/PaniniFS_Colab_GPU.ipynb)

**Lien direct** : https://colab.research.google.com/github/stephanedenis/PaniniFS-Research/blob/main/PaniniFS_Colab_GPU.ipynb

### 📚 Notebooks Avancés

#### Workflow Complet GitHub-Colab
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/stephanedenis/PaniniFS-Research/blob/main/colab_integration/notebooks/panini_github_colab_integration.ipynb)

**Lien** : https://colab.research.google.com/github/stephanedenis/PaniniFS-Research/blob/main/colab_integration/notebooks/panini_github_colab_integration.ipynb

---

## 🔥 Configuration GPU Requise

⚠️ **IMPORTANT** : Configurer Runtime → Change runtime type → **GPU** avant exécution

### 🎯 GPU Recommandés
- **T4** : 16 GB VRAM (optimal pour corpus moyens)
- **P4** : 8 GB VRAM (suffisant pour tests)
- **V100** : 32 GB VRAM (performance maximale si disponible)

---

## ⚡ Performance Attendue

| Corpus Size | CPU Local | GPU Colab | Accélération |
|-------------|-----------|-----------|--------------|
| 500 docs    | 45s       | 3-5s      | **15x**      |
| 2000 docs   | 3min      | 12-15s    | **12x**      |
| 10000 docs  | 15min     | 60s       | **15x**      |

---

## 🧬 Fonctionnalités

### 📊 Analyse Dhātu
- **9 patterns dhātu** universels
- **Analyse vectorielle** par document
- **Statistiques globales** multi-corpus
- **Visualisations** interactives

### 💾 Export Automatique
- **JSON** complet des résultats
- **Markdown** résumé exécutif
- **Téléchargement** automatique
- **Integration** API locale (optionnelle)

### 🌍 Support Multilingue
- **Français & Anglais** natifs
- **Patterns adaptatifs** par langue
- **Corpus mélangés** supportés

---

## 🚀 Démarrage Rapide

1. **Cliquer** le badge "Open in Colab" ci-dessus
2. **Configurer** GPU dans Runtime
3. **Exécuter** toutes les cellules séquentiellement
4. **Télécharger** les résultats automatiquement

---

## 🔗 Intégration Locale

Après exécution Colab, synchroniser avec l'API locale :

```bash
# Dans votre environnement local
bash scripts/sync_colab_results.sh
python3 scripts/integrate_colab_results.py --sync
```

Dashboard local : http://localhost:5000/dashboard

---

**🧬 PaniniFS Research - Powered by Colab Pro GPU Acceleration**