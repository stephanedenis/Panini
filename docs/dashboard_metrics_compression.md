# Dashboard Métriques Compression Temps Réel

Dashboard de monitoring en temps réel pour PaniniFS, atomes sémantiques et traducteurs.

## 🎯 Objectif

Fournir une interface web moderne pour monitorer les métriques de validation PaniniFS et découverte d'atomes sémantiques.

## ✨ Fonctionnalités

### Métriques PaniniFS
- **Taux compression par format** : Ratios de compression pour text, json, markdown, etc.
- **Temps ingestion/restitution** : Performance du pipeline en millisecondes
- **Intégrité (% succès)** : Pourcentage de validation réussie
- **Scalabilité (nb fichiers)** : Nombre de fichiers traités

### Atomes Sémantiques
- **Nb atomes découverts** : Total d'atomes identifiés par type (phonetic, morpheme, syntactic, semantic)
- **Validation multilangue (nb langues)** : Nombre de langues validées
- **Taux compression par atome** : Ratio de compression par type d'atome
- **Évolution dhātu → nouveaux** : Dhātu existants vs nouveaux découverts

### Traducteurs
- **Nb traducteurs identifiés** : Sources de patterns identifiées
- **Biais détectés** : Asymétries et biais structurels
- **Patterns récurrents** : Top patterns avec fréquences

## 🚀 Lancement

### Méthode 1 : Script de lancement
```bash
./scripts/run_metrics_dashboard.sh
```

### Méthode 2 : Lancement direct
```bash
# Installation des dépendances (première fois uniquement)
pip3 install flask flask-socketio

# Lancement du dashboard
python3 src/web/dashboard_metrics_compression.py
```

## 📡 Accès

Une fois lancé, le dashboard est accessible sur :
- **URL** : http://localhost:8889
- **API REST** : http://localhost:8889/api/metrics

## 🔄 Mise à jour automatique

Le dashboard se met à jour automatiquement toutes les 5 secondes pour afficher les dernières métriques disponibles.

## 📊 Sources de données

Le dashboard collecte les métriques depuis :
- `synthesis_validation_results/` : Métriques PaniniFS (compression, intégrité, performance)
- `universal_atoms_results/` : Métriques atomes sémantiques (découverte, multilangue)
- `molecular_patterns_results/` : Métriques traducteurs (patterns, biais)

## 🧪 Génération de données de test

Pour tester le dashboard avec des données simulées :
```bash
python3 tools/generate_mock_metrics.py
```

## ✅ Métriques de succès

- [x] Dashboard opérationnel port 8889
- [x] Métriques temps réel (mise à jour toutes les 5s)
- [x] PaniniFS : Compression par format
- [x] PaniniFS : Temps ingestion/restitution
- [x] PaniniFS : Intégrité et scalabilité
- [x] Atomes : Découverte par type
- [x] Atomes : Validation multilangue
- [x] Atomes : Compression par atome
- [x] Dhātu : Évolution existants/nouveaux
- [x] Traducteurs : Identifiés avec qualité
- [x] Traducteurs : Biais détectés
- [x] Traducteurs : Patterns récurrents

## 🎨 Interface

Le dashboard propose une interface moderne avec :
- Design responsive (adapté aux écrans desktop, tablette, mobile)
- Thème sombre pour confort visuel prolongé
- Mise à jour en temps réel via polling HTTP
- Indicateurs visuels colorés (badges, progression)
- Animations fluides

## 🔧 Architecture technique

- **Backend** : Flask + Flask-SocketIO
- **Frontend** : HTML5 + CSS3 + JavaScript vanilla
- **Mise à jour** : HTTP polling (toutes les 5 secondes)
- **Port** : 8889
- **Format données** : JSON

## 📝 Notes

- Le dashboard utilise Flask en mode développement. Pour production, utiliser un serveur WSGI (gunicorn, uwsgi)
- Les données de métriques sont lues depuis des fichiers JSON générés par les composants PaniniFS
- Le dashboard ne modifie jamais les données sources, lecture seule uniquement
