#!/bin/bash
# 🚀 DÉMARRER SESSION - Initialise journal et monitoring
# Usage: ./start_session.sh "Description mission"

if [ -z "$1" ]; then
    echo "❌ Usage: $0 \"Description de la mission\""
    exit 1
fi

MISSION="$1"
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M:%S)
TIMESTAMP=$(date +%Y-%m-%d_%H%M%S)
HOST=$(hostname)
PID=$$

JOURNAL_DIR="copilotage/journal"
mkdir -p "$JOURNAL_DIR"

SESSION_FILE="$JOURNAL_DIR/JOURNAL_SESSION_${DATE}_${HOST}_${PID}.md"

echo "🚀 Démarrage session..."
echo "📓 Journal: $SESSION_FILE"

cat > "$SESSION_FILE" << EOF
# 📓 JOURNAL SESSION - $MISSION

**Date**: $DATE  
**Heure début**: $TIME  
**Host**: $HOST  
**PID**: $PID  
**Mission**: $MISSION

---

## 🎯 Objectifs Session

<!-- Remplir les objectifs de la session -->

- [ ] Objectif 1
- [ ] Objectif 2
- [ ] Objectif 3

---

## 📊 État Initial

### Git Status
\`\`\`
$(git status)
\`\`\`

### Derniers Commits
\`\`\`
$(git log -3 --oneline)
\`\`\`

### Fichiers Modifiés
\`\`\`
$(git diff --name-status 2>/dev/null || echo "Aucun")
\`\`\`

---

## ⏱️ Timeline

### [$TIME] Démarrage Session

**Action**: Initialisation session "$MISSION"

EOF

echo "✅ Session initialisée!"
echo "📁 Journal: $SESSION_FILE"
echo ""
echo "💡 Commandes utiles:"
echo "   - Snapshot: tools/snapshot_auto.sh"
echo "   - Backup: tools/backup_copilot_discussions.sh"
echo "   - Fin session: tools/end_session.sh"
echo ""
echo "🔔 N'oubliez pas de committer régulièrement (au moins 1x/heure)!"
echo "🔔 Le hook post-commit génère automatiquement le journal!"

# Créer snapshot initial
echo ""
echo "📸 Création snapshot initial..."
tools/snapshot_auto.sh "session_start" 2>/dev/null

# Sauvegarder chemin session pour end_session
echo "$SESSION_FILE" > /tmp/panini_current_session.txt

echo ""
echo "✅ Session prête! Bon travail!"
