# Dashboard Métriques Compression Temps Réel

Dashboard de monitoring en temps réel pour l'ensemble des recherches Panini : PaniniFS, atomes sémantiques, traducteurs, corpus multilingues, et métriques de symétries composition/décomposition.

## 🎯 Objectif

Fournir une interface web moderne et modulaire pour monitorer l'ensemble des recherches Panini, incluant la validation PaniniFS, découverte d'atomes sémantiques, analyse des traducteurs et leurs biais culturels, et identification des universaux à travers les symétries parfaites de composition/décomposition.

## ✨ Fonctionnalités

### Métriques PaniniFS
- **Taux compression par format** : Ratios de compression pour text, json, markdown, etc.
- **Temps ingestion/restitution** : Performance du pipeline en millisecondes
- **Intégrité** : Statut binaire (succès total ou échec) - la reconstitution doit être absolue, sans perte
- **Scalabilité (nb fichiers)** : Nombre de fichiers traités

### Atomes Sémantiques & Représentation Pure
- **Nb atomes découverts** : Total d'atomes identifiés par type (phonetic, morpheme, syntactic, semantic)
- **Validation multilangue (nb langues)** : Nombre de langues validées
- **Taux compression par atome** : Ratio de compression par type d'atome
- **Évolution dhātu → nouveaux** : Dhātu existants vs nouveaux découverts
- **Symétries composition/décomposition** : Patterns candidats comme universaux, théorie de l'information au-delà du langage et du binaire

### Traducteurs - Métadonnées & Biais Culturels
- **Identité traducteurs** : Qui a traduit (nom, époque, contexte)
- **Quand traduit** : Timestamps et périodes historiques des traductions
- **Style propre** : Chaque traducteur est auteur de sa traduction avec sa propre interprétation
- **Biais culturels** : Asymétries et biais propres au milieu, vécu et époque du traducteur
- **Patterns récurrents** : Signatures stylistiques identifiables par traducteur

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

Le dashboard collecte les métriques depuis plusieurs sources configurables :
- `synthesis_validation_results/` : Métriques PaniniFS (compression, intégrité, performance)
- `universal_atoms_results/` : Métriques atomes sémantiques (découverte, multilangue)
- `molecular_patterns_results/` : Métriques traducteurs (patterns, biais)
- **Architecture modulaire** : Ajout de nouvelles sources sans refonte du système
- **Panels croisés** : Corrélation de données entre différentes sources pour analyses approfondies

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
- **Design responsive** : Adapté aux écrans desktop, tablette, mobile
- **Optimisation UHD/4K** : Layout multi-colonnes (3-4 colonnes) pour résolutions 3840×2160, grille fluide pour 1440p et 1080p
- **Thème sombre** : Confort visuel prolongé avec contraste optimisé
- **Mise à jour temps réel** : Polling HTTP pour actualisation continue des données
- **Indicateurs visuels** : Badges colorés, barres de progression, graphiques informatifs
- **Animations utilitaires uniquement** : Animations pour améliorer perspectives sur données complexes ou attirer attention sur nouvelles informations (pas d'animations décoratives)

## 🔧 Architecture technique

- **Backend** : Flask + Flask-SocketIO
- **Frontend** : HTML5 + CSS3 + JavaScript vanilla
- **Mise à jour** : HTTP polling (toutes les 5 secondes)
- **Port** : 8889 (standardisé dans l'écosystème Panini - réutilisé pour nouvelles versions)
- **Format données** : JSON
- **Dates techniques** : Format ISO 8601 obligatoire (ex: 2025-09-30T14:23:45Z)
- **Déploiement** : Configuration pour GitHub Pages avec lecture JSON depuis branche main

### Ports standardisés écosystème Panini
- `8889` : Dashboard principal (ce dashboard)
- `8890` : API données temps réel
- `8891` : WebSocket live updates
- `8892` : PaniniFS monitoring
- `8893` : Atomes sémantiques API
- `8894` : Traducteurs DB

## 📝 Notes

- Le dashboard utilise Flask en mode développement. Pour production, utiliser un serveur WSGI (gunicorn, uwsgi)
- Les données de métriques sont lues depuis des fichiers JSON générés par les composants PaniniFS
- Le dashboard ne modifie jamais les données sources, lecture seule uniquement
