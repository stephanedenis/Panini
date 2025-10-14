# 🧠 PANINI AUTONOME - GUIDE DASHBOARD LIVE

## 📊 Dashboard Live Disponibles

### 🐍 Dashboard Python Interactif
```bash
python3 dashboard_live_panini.py
```
**Fonctionnalités:**
- Interface colorée et interactive
- Mise à jour temps réel (1-2s)
- Tracking 7 workers parallèles
- Métriques live (cycles, découvertes, fidélité)
- Barres de progression animées
- Contrôles clavier (q pour quitter)

### 🔧 Dashboard Bash Natif
```bash
./dashboard_live_bash.sh
```
**Fonctionnalités:**
- Dashboard pur Bash (sans dépendances)
- Interface ASCII art
- 3 modes: Live continu, Snapshot, Rapide (1s)
- Compatible tous environnements Linux
- Affichage structuré avec bordures

### ⚡ Monitoring Rapide
```bash
bash monitoring_panini_rapide.sh
```
**Fonctionnalités:**
- Status instantané
- Métriques essentielles
- Affichage compact
- Idéal pour checks rapides

## 🚀 Lancement Recommandé

### Pour Interface Riche (Python)
```bash
cd /home/stephane/GitHub/Panini
python3 dashboard_live_panini.py
```

### Pour Environnement Simple (Bash)
```bash
cd /home/stephane/GitHub/Panini
./dashboard_live_bash.sh
# Choix 1: Dashboard Live continu
# Choix 2: Snapshot unique
# Choix 3: Rafraîchissement rapide (1s)
```

## 📈 Métriques Surveillées

### 🔄 Métriques Système
- **Cycles**: Nombre de cycles d'apprentissage
- **Découvertes**: Nouvelles entités identifiées
- **Fidélité**: Pourcentage d'alignement Panini
- **Uptime**: Temps de fonctionnement continu

### 👥 Workers Actifs (7 parallèles)
1. **Analyse Corpus**: Traitement multilingue
2. **Mining Discussions**: Extraction patterns
3. **Découverte Émergente**: Patterns nouveaux  
4. **Recherche Universaux**: Entités fondamentales
5. **Test Domaines**: Validation sémantique
6. **Traitement Archives**: Documentation
7. **Recherche Sémantique**: Emergence conceptuelle

### 🎯 Objectifs Progression
- **Restitution 100%**: Fidélité Panini parfaite
- **Universaux (25)**: Collection universaux complets
- **Domaines (25)**: Couverture sémantique totale

## 🛠️ Contrôles Interface

### Dashboard Python
- **q**: Quitter proprement
- **r**: Refresh manuel
- **p**: Pause/Resume
- **h**: Aide

### Dashboard Bash
- **Ctrl+C**: Arrêt propre
- **Menu**: Choix mode affichage
- **Refresh**: Automatique selon mode

## 🔧 Résolution Problèmes

### Python Dashboard Ne Lance Pas
```bash
# Vérifier Python
python3 --version

# Installer si nécessaire
sudo apt install python3

# Lancer avec debug
python3 -v dashboard_live_panini.py
```

### Bash Dashboard Problème
```bash
# Vérifier permissions
ls -la dashboard_live_bash.sh

# Corriger si nécessaire  
chmod +x dashboard_live_bash.sh

# Test bc (calculateur)
echo "2.5 + 1.2" | bc -l
```

## 📊 Données Live Simulées

Le dashboard affiche des **données simulées réalistes** montrant:
- Progression continue des cycles
- Découvertes émergentes
- Évolution fidélité Panini
- Activité des 7 workers
- Métriques système temps réel

**Note**: Les données sont générées pour visualiser le comportement du système autonome Panini en fonctionnement continu.

## 🎯 Usage Optimal

1. **Lancement**: Choisir dashboard selon environnement
2. **Monitoring**: Observer progression découvertes
3. **Validation**: Vérifier fidélité Panini
4. **Analysis**: Suivre workers parallèles
5. **Arrêt**: Utiliser contrôles appropriés

---
🧠 **Panini Autonome Parfait** - Recherche fondamentale continue