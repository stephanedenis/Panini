# 🚀 Guide d'Utilisation Rapide - Colab + Collecteur

## 🎯 Démarrage en 1 commande

```bash
python3 scripts/quick_launch.py
```

Cette commande :
- ✅ Synchronise Git automatiquement
- 🤖 Lance le collecteur en continu
- 🌐 Ouvre Colab dans votre navigateur
- 📊 Configure toute l'interaction

## 📓 Utilisation du Notebook Colab

### 1. Ouvrir le carnet
Le carnet `colab_dhatu_simple.ipynb` s'ouvre automatiquement dans votre navigateur.

**Lien direct:** https://colab.research.google.com/github/stephanedenis/PaniniFS-Research/blob/main/notebooks/colab_dhatu_simple.ipynb

### 2. Exécuter les cellules

**Dans l'ordre:**
1. 📦 **Setup rapide** - Clone/synchronise le repository
2. 🔍 **Analyseur Dhātu** - Initialise l'analyseur simple
3. 📁 **Charger données** - Analyse les documents collectés
4. 📊 **Stats rapides** - Visualise les résultats
5. 🤖 **Interaction collecteur** - Envoie feedback au collecteur
6. 🔄 **Mode continu** (optionnel) - Surveillance continue

### 3. Interaction en temps réel

Le notebook :
- 📥 Lit automatiquement les données du collecteur
- 📊 Analyse les dhātus détectés
- 📤 Envoie des recommandations au collecteur
- 🔄 Synchronise via GitHub en continu

## 🤖 Collecteur Intelligent

### Configuration optimisée
- **Vitesse:** 5 documents par cycle
- **Fréquence:** 1 cycle par minute
- **Sources:** Wikipedia + contenu académique
- **Qualité:** Scoring automatique

### Données collectées
```
data/incremental_corpus/
├── fast_batch_YYYYMMDD_HHMMSS.json
├── fast_batch_YYYYMMDD_HHMMSS.json
└── ...
```

### Feedback automatique
```
colab_results/
├── colab_feedback.json      # Recommandations de Colab
├── fast_collector_stats.json # Stats du collecteur
└── launch_info.json         # Info de lancement
```

## 📊 Monitoring

### Vérifier le statut
```bash
# Processus actifs
ps aux | grep collector

# Logs en temps réel
tail -f fast_collector.log

# Stats récentes
cat colab_results/fast_collector_stats.json
```

### Données récentes
```bash
# Derniers fichiers collectés
ls -la data/incremental_corpus/ | tail -5

# Dernier feedback Colab
cat colab_results/colab_feedback.json
```

## ⏹️ Arrêt propre

```bash
python3 scripts/stop_collection.py
```

## 🔄 Workflow optimisé

### 1. Recherche intensive
```
Colab (GPU) ← → GitHub ← → Collecteur local (CPU)
    ↓                         ↓
 Analyse dhātus         Collecte corpus
 Feedback qualité       Push incrémental
```

### 2. Synchronisation continue
- **Collecteur:** Push toutes les minutes
- **Colab:** Pull à la demande
- **Feedback:** Instant via GitHub

### 3. Optimisation automatique
- Colab analyse la qualité des documents
- Recommande des sources au collecteur
- Collecteur adapte sa stratégie
- Boucle d'amélioration continue

## 🎯 Avantages de cette approche

✅ **Simplicité:** 1 commande pour tout démarrer
✅ **Rapidité:** Collecteur optimisé, cycles courts
✅ **Interaction:** Feedback temps réel Colab ↔ Collecteur
✅ **Robustesse:** Arrêt/redémarrage propre
✅ **Visibilité:** Logs et stats en continu
✅ **GitHub-only:** Pas de dépendances externes

## 📝 Exemple de session

```bash
# 1. Démarrage
python3 scripts/quick_launch.py
# → Colab s'ouvre, collecteur démarre

# 2. Dans Colab
# → Exécuter les cellules une par une
# → Voir les analyses en temps réel

# 3. Monitoring local
tail -f fast_collector.log
# → Voir la collecte en cours

# 4. Arrêt
python3 scripts/stop_collection.py
# → Tout s'arrête proprement
```

🚀 **C'est parti pour la recherche dhātu optimisée !**