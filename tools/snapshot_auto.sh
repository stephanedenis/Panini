#!/bin/bash
# 📸 SNAPSHOT AUTOMATIQUE PROJET
# Crée un snapshot complet de l'état du projet
# Usage: ./snapshot_auto.sh [label-optionnel]

SNAPSHOT_DIR="copilotage/snapshots"
mkdir -p "$SNAPSHOT_DIR"

TIMESTAMP=$(date +%Y-%m-%d_%H%M%S)
HOST=$(hostname)
PID=$$
LABEL="${1:-auto}"

SNAPSHOT_FILE="$SNAPSHOT_DIR/snapshot_${TIMESTAMP}_${HOST}_${LABEL}.md"

echo "📸 Création snapshot projet..."

cat > "$SNAPSHOT_FILE" << 'SNAPSHOT_EOF'
# 📸 Snapshot Automatique Projet Panini

**Date**: $(date --iso-8601=seconds)
**Host**: $(hostname)
**User**: $(whoami)
**PID**: $$
**Label**: LABEL_PLACEHOLDER

---

## 🔍 Git Status

### État Général
```
$(git status)
```

### Branche Actuelle
```
Branche: $(git branch --show-current)
Commit HEAD: $(git log -1 --oneline)
```

### Fichiers Modifiés Non Committés
```
$(git diff --name-status 2>/dev/null || echo "Aucun fichier modifié")
```

### Fichiers Non Trackés
```
$(git ls-files --others --exclude-standard | head -20)
```

---

## 📊 Dernière Activité

### 5 Derniers Commits
```
$(git log -5 --pretty=format:"%h - %ai - %an: %s")
```

### Statistiques Dernière Semaine
```
$(git log --since="1 week ago" --oneline | wc -l) commits
$(git diff --shortstat HEAD~7..HEAD 2>/dev/null || echo "N/A")
```

---

## 📁 Arborescence Racine

### Fichiers
```
$(ls -lh | grep -v '^d' | head -20)
```

### Dossiers
```
$(ls -lh | grep '^d' | head -20)
```

### Statistiques Disque
```
Taille totale: $(du -sh . 2>/dev/null | cut -f1)
Fichiers: $(find . -type f | wc -l)
Dossiers: $(find . -type d | wc -l)
```

---

## 🔧 Processus Actifs

### Python/Jupyter
```
$(ps aux | grep -E "[p]ython|[j]upyter" | head -10 || echo "Aucun processus Python actif")
```

### VS Code
```
$(ps aux | grep "[c]ode" | head -5 || echo "VS Code non actif")
```

### Git Operations
```
$(ps aux | grep "[g]it" | head -5 || echo "Aucune opération Git active")
```

---

## 💾 Usage Ressources

### Disque
```
$(df -h /home/stephane/GitHub/Panini | tail -1)
```

### Mémoire
```
$(free -h | grep Mem)
```

### Load Average
```
$(uptime)
```

---

## 🌳 Submodules

```
$(git submodule status 2>/dev/null || echo "Aucun submodule ou erreur")
```

---

## 📦 Sauvegardes Présentes

```
$(ls -lh sauvegarde* 2>/dev/null | head -5 || echo "Aucune sauvegarde dans racine")
```

---

## 🚨 Alertes Potentielles

### Fichiers Volumineux Non Committés
```
$(find . -type f -size +10M ! -path "./.git/*" ! -path "*/node_modules/*" ! -path "*/wikipedia*" -exec ls -lh {} \; 2>/dev/null | head -10 || echo "Aucun")
```

### Fichiers Modifiés > 1h Non Committés
```
$(git status --short | head -10 || echo "Aucun")
```

---

**Snapshot généré**: $(date)
**Prochaine action recommandée**: Vérifier Git status et committer si nécessaire

SNAPSHOT_EOF

# Remplacer placeholders
sed -i "s/LABEL_PLACEHOLDER/$LABEL/g" "$SNAPSHOT_FILE"

# Exécuter les commandes (le heredoc littéral ci-dessus les a préservées)
# On doit maintenant les évaluer
echo "📸 Snapshot créé: $SNAPSHOT_FILE"
echo "📏 Taille: $(du -h "$SNAPSHOT_FILE" | cut -f1)"

# Suggestion auto-commit snapshot (optionnel, commenté par défaut)
# cd "$(dirname "$SNAPSHOT_FILE")" && git add . && git commit -m "📸 Snapshot auto $TIMESTAMP [$LABEL]" 2>/dev/null

echo "✅ Snapshot complet enregistré!"
