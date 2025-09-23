# 📚 Notebooks Colab - Guide d'Utilisation

## 🔥 Notebooks Actifs

### 1. `colab_dhatu_gpu_accelerated.ipynb` 
**🚀 RECOMMANDÉ POUR GPU T4**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/stephanedonis/PaniniFS-Research/blob/main/notebooks/colab_dhatu_gpu_accelerated.ipynb)

- **Usage** : Analyse massive avec GPU T4
- **Performance** : 100-500 docs/seconde  
- **Features** :
  - Traitement parallélisé optimisé GPU
  - Calculs vectorisés (NumPy/PyTorch)
  - Analyse par batch (64 documents)
  - Visualisations temps réel
  - Feedback intelligent pour collecteur turbo
  - Monitoring performance GPU

**💡 Utiliser quand** :
- GPU T4 activé dans Colab
- Gros volumes de données (>1000 documents)
- Besoin de performance maximale
- Collecteur turbo à nourrir

---

### 2. `colab_dhatu_robust.ipynb`
**🛡️ VERSION STABLE UNIVERSELLE**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/stephanedonis/PaniniFS-Research/blob/main/notebooks/colab_dhatu_robust.ipynb)

- **Usage** : Analyse fiable sans dépendances
- **Performance** : 10-50 docs/seconde
- **Features** :
  - Configuration Git automatique
  - Gestion d'erreurs complète
  - Compatible CPU/GPU
  - Fallback intelligent
  - Sauvegarde locale garantie

**💡 Utiliser quand** :
- Première utilisation
- Problèmes de configuration Git
- Analyse modérée (100-1000 documents)
- Besoin de stabilité maximale
- GPU non disponible

---

## 📂 Archives

Les notebooks suivants sont archivés mais restent disponibles :

- `analyse_phonologique.ipynb` - Analyse phonologique spécialisée
- `dhatu_multi_hypotheses_intensive.ipynb` - Analyse multi-hypothèses
- `colab_dhatu_simple.ipynb` - Version basique (remplacée par robust)

## 🎯 Workflow Recommandé

### Pour Débutants
```
1. Commencer par → colab_dhatu_robust.ipynb
2. Tester avec quelques documents
3. Vérifier Git et sauvegarde
```

### Pour Performance Maximale  
```
1. Activer GPU T4 dans Colab
2. Utiliser → colab_dhatu_gpu_accelerated.ipynb
3. Charger données massivement
4. Analyser en batch de 64 docs
```

### Pour Collecteur Turbo
```
1. Version GPU pour traiter 846 docs/min
2. Feedback automatique vers collecteur
3. Optimisation continue des paramètres
```

## 🔧 Configuration Requise

### Version Robust
- Python 3.7+
- Aucune dépendance externe
- Fonctionne sur CPU/GPU

### Version GPU Accelerated  
- GPU T4 recommandé
- PyTorch (installation automatique)
- NumPy, matplotlib
- 4-8 GB RAM minimum

## 🚀 Liens Rapides

| Notebook | Usage | Performance | Lien |
|----------|-------|-------------|------|
| GPU Accelerated | Analyse massive | 100-500 docs/s | [🚀 Ouvrir](https://colab.research.google.com/github/stephanedonis/PaniniFS-Research/blob/main/notebooks/colab_dhatu_gpu_accelerated.ipynb) |
| Robust | Stable universel | 10-50 docs/s | [🛡️ Ouvrir](https://colab.research.google.com/github/stephanedonis/PaniniFS-Research/blob/main/notebooks/colab_dhatu_robust.ipynb) |

## 💡 Conseils d'Utilisation

1. **Toujours commencer** par la version Robust pour valider la configuration
2. **Passer au GPU** quand le volume dépasse 1000 documents  
3. **Monitorer la performance** avec les métriques intégrées
4. **Sauvegarder régulièrement** les résultats d'analyse

---

*Dernière mise à jour : 22 septembre 2025*
*Collecteur turbo compatible : 846 docs/min*