#!/bin/bash
# 🏁 TERMINER SESSION - Finalise journal et backups
# Usage: ./end_session.sh

DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M:%S)
HOST=$(hostname)

# Récupérer session active
if [ -f /tmp/panini_current_session.txt ]; then
    SESSION_FILE=$(cat /tmp/panini_current_session.txt)
else
    # Trouver dernier journal du jour
    SESSION_FILE=$(ls -t copilotage/journal/JOURNAL_SESSION_${DATE}_*.md 2>/dev/null | head -1)
fi

if [ -z "$SESSION_FILE" ] || [ ! -f "$SESSION_FILE" ]; then
    echo "⚠️  Aucune session active trouvée"
    echo "Tentative de création journal de clôture..."
    SESSION_FILE="copilotage/journal/JOURNAL_SESSION_${DATE}_${HOST}_end.md"
fi

echo "🏁 Finalisation session..."
echo "📓 Journal: $SESSION_FILE"

# Ajouter section fin de session
cat >> "$SESSION_FILE" << EOF

---

## 🏁 Fin de Session

### [$TIME] Clôture Session

**Heure fin**: $TIME

### Git Status Final
\`\`\`
$(git status)
\`\`\`

### Commits de la Session
\`\`\`
$(git log --since="today" --oneline)
\`\`\`

### Fichiers Modifiés Non Committés
\`\`\`
$(git diff --name-status 2>/dev/null || echo "Aucun - Tout est committé! ✅")
\`\`\`

---

## 📊 Statistiques Session

- **Durée**: $(echo "Session en cours - calculer manuellement")
- **Commits**: $(git log --since="today" --oneline | wc -l)
- **Fichiers modifiés**: $(git diff --stat HEAD@{1day}..HEAD 2>/dev/null | tail -1 || echo "N/A")

---

## ✅ Checklist Fin Session

- [ ] Tous les fichiers importants committés
- [ ] Push vers GitHub effectué
- [ ] Documentation/journal mis à jour
- [ ] Backups réalisés
- [ ] Aucun fichier temporaire important non sauvegardé

---

## 💡 Notes Finales / Prochaines Étapes

<!-- Ajouter notes pour la prochaine session -->

---

**Session terminée**: $(date --iso-8601=seconds)  
**Prochaine session**: À planifier

EOF

echo "✅ Journal finalisé!"

# Créer snapshot final
echo ""
echo "📸 Création snapshot final..."
tools/snapshot_auto.sh "session_end" 2>/dev/null

# Backup discussions
echo ""
echo "💾 Backup discussions Copilot..."
tools/backup_copilot_discussions.sh 2>/dev/null

# Vérifier si tout est committé
echo ""
if [ -n "$(git status --short)" ]; then
    echo "⚠️  ATTENTION: Fichiers non committés détectés!"
    echo ""
    git status --short
    echo ""
    echo "💡 Recommandation: Committer avant de terminer"
    echo "   git add ."
    echo "   git commit -m \"Fin session: $(date +%Y-%m-%d)\""
    echo "   git push"
else
    echo "✅ Tous les fichiers sont committés!"
fi

# Nettoyer fichier session temporaire
rm -f /tmp/panini_current_session.txt

echo ""
echo "🎉 Session terminée avec succès!"
echo "📁 Journal: $SESSION_FILE"
echo ""
echo "💾 N'oubliez pas de push vers GitHub:"
echo "   git push origin $(git branch --show-current)"
