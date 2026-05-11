# Scripts Python PaniniFS Research

## Scripts Disponibles

### 1. `panini_manager.py` - Gestionnaire Principal
Script unique pour gérer toutes les opérations PaniniFS Research.

**Commandes disponibles :**
```bash
# Démarrage complet (recommandé)
python3 scripts/panini_manager.py all

# Démarrer seulement l'API
python3 scripts/panini_manager.py start

# Synchroniser résultats Colab
python3 scripts/panini_manager.py sync

# Voir le statut système
python3 scripts/panini_manager.py status
```

**Fonctionnalités :**
- ✅ Démarrage automatique API
- ✅ Vérification état système
- ✅ Synchronisation Colab
- ✅ Monitoring en temps réel
- ✅ Gestion des erreurs

### 2. `quickstart.py` - Guide de Démarrage
Affiche le guide complet de démarrage rapide.

```bash
# Voir le guide
python3 scripts/quickstart.py

# Démarrage automatique
python3 scripts/quickstart.py --auto
```

### 3. `sync_colab_results.py` - Synchronisation Avancée
Synchronisation détaillée des résultats Colab avec Git.

```bash
python3 scripts/sync_colab_results.py
```

### 4. `launcher.py` - Lanceur Complet
Lanceur avancé avec toutes les fonctionnalités.

```bash
python3 scripts/launcher.py --start-api
python3 scripts/launcher.py --sync-colab
python3 scripts/launcher.py --status
```

## Workflow Recommandé

### Démarrage Rapide
1. **Premier démarrage :**
   ```bash
   python3 scripts/panini_manager.py all
   ```

2. **Ouvrir le dashboard :**
   - http://localhost:5000/dashboard

3. **Utiliser Colab pour GPU :**
   - https://colab.research.google.com/github/stephanedenis/PaniniFS-Research/blob/main/PaniniFS_Colab_GPU.ipynb

4. **Synchroniser les résultats :**
   ```bash
   python3 scripts/panini_manager.py sync
   ```

### Utilisation Quotidienne
```bash
# Voir l'état
python3 scripts/panini_manager.py status

# Redémarrer si nécessaire
python3 scripts/panini_manager.py start

# Sync après travail Colab
python3 scripts/panini_manager.py sync
```

## Avantages des Scripts Python

### ✅ Plus de dépendances shell
- Scripts 100% Python
- Compatible multiplateforme
- Pas d'intervention manuelle

### ✅ Interface unifiée
- Une seule commande pour tout
- Messages clairs et colorés
- Gestion d'erreur robuste

### ✅ Automation complète
- Démarrage automatique API
- Vérification santé système
- Synchronisation intelligente

### ✅ Monitoring intégré
- État en temps réel
- Logs détaillés
- Liens directs

## Liens Importants

- **Dashboard Local :** http://localhost:5000/dashboard
- **API Health :** http://localhost:5000/health
- **Notebook Colab :** [PaniniFS_Colab_GPU.ipynb](https://colab.research.google.com/github/stephanedenis/PaniniFS-Research/blob/main/PaniniFS_Colab_GPU.ipynb)
- **Documentation :** README.md

## Support

Pour toute question ou problème :
1. Vérifier `python3 scripts/panini_manager.py status`
2. Consulter les logs dans `gestionnaire_arriere_plan.log`
3. Voir la documentation complète dans README.md

---
*Scripts créés pour remplacer complètement les dépendances shell et simplifier l'utilisation.*