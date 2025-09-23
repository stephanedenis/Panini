# Organisation du Workspace PaniniFS-Research

## Structure

### 🎯 systeme_evenementiel/
Système événementiel avec affinité CPU exclusive
- Architecture événementielle (plus de cycles fixes)
- Allocation CPU dédiée par processeur
- Dashboard spécialisé sur port 8892

### 📊 dashboards/
Interfaces web et monitoring temps réel
- Dashboards avec auto-refresh
- Monitoring système avancé
- Métriques CPU/GPU/processus

### 🤖 systemes_autonomes/
Systèmes autonomes et coordinateurs
- Coordinateur global
- Processeurs spécialisés autonomes
- Validation et métriques

### 🔧 pipelines_dhatu/
Pipelines de traitement dhatu
- Évolution aspectuelle
- Reconstruction intelligente
- Dictionnaires exhaustifs

### 📚 corpus_collection/
Collection et analyse de corpus
- Collection multilingue
- Corpus préscolaires
- Analyseurs corpus

### 🛠️ utilitaires/
Scripts utilitaires et diagnostic
- Vérification statut
- Diagnostic performance
- Analyse goulots d'étranglement

### 🗃️ archives/
Fichiers obsolètes conservés pour référence

## État Actuel du Système

✅ **Système Événementiel Actif**
- 3 processus événementiels en cours
- Affinité CPU configurée (cores 1-8)
- Dashboard accessible: http://localhost:8892

✅ **Architecture Optimisée**
- Traitement par événements (pas de cycles fixes)
- Cores dédiés par processeur
- Monitoring temps réel fonctionnel

## Scripts Principaux

```bash
# Système événementiel
python3 systeme_evenementiel/systeme_evenementiel_cpu.py &
python3 systeme_evenementiel/ouvrir_dashboard.py

# Vérification
python3 systeme_evenementiel/verifier_statut.py

# Monitoring
python3 dashboards/dashboard_evenementiel.py &
```
