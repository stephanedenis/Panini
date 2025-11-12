#!/bin/bash
# 💾 BACKUP AUTOMATIQUE DISCUSSIONS COPILOT
# Sauvegarde l'état VS Code Copilot et contexte session

BACKUP_DIR="copilotage/journal/discussions_backups"
mkdir -p "$BACKUP_DIR"

TIMESTAMP=$(date +%Y-%m-%d_%H%M%S)
HOST=$(hostname)

echo "💾 Backup discussions Copilot..."

# 1. Copier état VS Code Copilot
VSCODE_COPILOT="$HOME/.config/Code/User/globalStorage/github.copilot"
if [ -d "$VSCODE_COPILOT" ]; then
    COPILOT_BACKUP="$BACKUP_DIR/copilot_state_${TIMESTAMP}_${HOST}"
    cp -r "$VSCODE_COPILOT" "$COPILOT_BACKUP"
    echo "✅ État Copilot sauvegardé: $COPILOT_BACKUP"
    echo "   Taille: $(du -sh "$COPILOT_BACKUP" | cut -f1)"
else
    echo "⚠️  Dossier VS Code Copilot non trouvé: $VSCODE_COPILOT"
fi

# 2. Sauvegarder historique chat Copilot (si accessible)
VSCODE_CHAT="$HOME/.config/Code/User/globalStorage/github.copilot-chat"
if [ -d "$VSCODE_CHAT" ]; then
    CHAT_BACKUP="$BACKUP_DIR/copilot_chat_${TIMESTAMP}_${HOST}"
    cp -r "$VSCODE_CHAT" "$CHAT_BACKUP"
    echo "✅ Historique chat sauvegardé: $CHAT_BACKUP"
fi

# 3. Créer métadonnées backup
META_FILE="$BACKUP_DIR/backup_${TIMESTAMP}_${HOST}_metadata.json"
cat > "$META_FILE" << EOF
{
  "timestamp": "$(date --iso-8601=seconds)",
  "host": "$HOST",
  "user": "$(whoami)",
  "backup_type": "copilot_discussions",
  "git_branch": "$(git branch --show-current 2>/dev/null || echo 'N/A')",
  "git_commit": "$(git log -1 --pretty=%H 2>/dev/null || echo 'N/A')",
  "git_status": "$(git status --short | wc -l) fichiers modifiés",
  "disk_usage": "$(du -sh . | cut -f1)",
  "backups_created": [
    "$(ls -1 "$BACKUP_DIR"/copilot_state_${TIMESTAMP}_* 2>/dev/null || echo 'none')",
    "$(ls -1 "$BACKUP_DIR"/copilot_chat_${TIMESTAMP}_* 2>/dev/null || echo 'none')"
  ]
}
EOF

echo "📋 Métadonnées créées: $META_FILE"

# 4. Compter backups existants
BACKUP_COUNT=$(ls -1d "$BACKUP_DIR"/copilot_state_* 2>/dev/null | wc -l)
echo "📊 Total backups discussions: $BACKUP_COUNT"

# 5. Nettoyer vieux backups (garder 30 derniers jours)
find "$BACKUP_DIR" -type d -name "copilot_*" -mtime +30 -exec rm -rf {} \; 2>/dev/null
find "$BACKUP_DIR" -type f -name "backup_*_metadata.json" -mtime +30 -delete 2>/dev/null

echo "✅ Backup discussions complet!"
echo "📁 Dossier: $BACKUP_DIR"
echo "💾 Espace utilisé: $(du -sh "$BACKUP_DIR" | cut -f1)"
