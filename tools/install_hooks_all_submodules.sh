#!/bin/bash
# Script pour installer les hooks de journalisation dans tous les submodules
# Usage: ./install_hooks_all_submodules.sh

echo "🔧 INSTALLATION HOOKS JOURNALISATION - TOUS LES SUBMODULES"
echo "==========================================================="
echo ""

PROJECT_ROOT="/home/stephane/GitHub/Panini"
cd "$PROJECT_ROOT"

# Template du hook post-commit
create_hook() {
    local SUBMODULE_PATH=$1
    local HOOK_FILE="$SUBMODULE_PATH/.git/hooks/post-commit"
    
    cat > "$HOOK_FILE" << 'EOF'
#!/bin/bash
# 📓 HOOK GIT POST-COMMIT - JOURNALISATION AUTOMATIQUE
# Crée/met à jour automatiquement le journal à chaque commit

JOURNAL_DIR="copilotage/journal"
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M:%S)
HOST=$(hostname)
PID=$$
COMMIT_MSG=$(git log -1 --pretty=%B)
COMMIT_HASH=$(git log -1 --pretty=%H)
COMMIT_SHORT=$(git log -1 --pretty=%h)

# Créer dossier journal si nécessaire
mkdir -p "$JOURNAL_DIR"

# Fichier journal du jour
JOURNAL_FILE="$JOURNAL_DIR/JOURNAL_AUTO_${DATE}_${HOST}.md"

# Si nouveau journal, créer header
if [ ! -f "$JOURNAL_FILE" ]; then
    cat > "$JOURNAL_FILE" << EOFHEADER
# 📓 Journal Automatique - $DATE

**Host**: $HOST  
**Début session**: $(date --iso-8601=seconds)  
**Système**: Journalisation automatique via Git hooks

---

EOFHEADER
fi

# Ajouter entrée commit
cat >> "$JOURNAL_FILE" << EOFENTRY

## [$TIME] Commit \`$COMMIT_SHORT\`

**Message**: $COMMIT_MSG

**Hash complet**: \`$COMMIT_HASH\`

### Fichiers modifiés

\`\`\`
$(git diff-tree --no-commit-id --name-status -r HEAD)
\`\`\`

### Statistiques

\`\`\`
$(git log -1 --stat)
\`\`\`

---

EOFENTRY

echo "📓 Journal automatique mis à jour: $JOURNAL_FILE"

# Compter commits du jour
COMMITS_TODAY=$(grep -c "## \[" "$JOURNAL_FILE" 2>/dev/null || echo 0)
echo "✅ Commits aujourd'hui: $COMMITS_TODAY"
EOF

    chmod +x "$HOOK_FILE"
}

# Liste des submodules
SUBMODULES=$(git submodule status | awk '{print $2}')

echo "📦 Installation dans les submodules:"
echo ""

TOTAL=0
SUCCESS=0
FAILED=0

for submodule in $SUBMODULES; do
    TOTAL=$((TOTAL + 1))
    SUBMODULE_FULL_PATH="$PROJECT_ROOT/$submodule"
    
    echo "[$TOTAL] $submodule"
    
    # Pour les submodules, .git est un fichier qui pointe vers .git/modules/...
    if [ -f "$SUBMODULE_FULL_PATH/.git" ]; then
        # Lire le gitdir depuis le fichier .git
        GIT_DIR=$(grep "gitdir:" "$SUBMODULE_FULL_PATH/.git" | cut -d' ' -f2)
        GIT_DIR_FULL="$SUBMODULE_FULL_PATH/$GIT_DIR"
        
        # Créer le dossier hooks si nécessaire
        mkdir -p "$GIT_DIR_FULL/hooks"
        
        # Créer le dossier copilotage/journal dans le submodule
        mkdir -p "$SUBMODULE_FULL_PATH/copilotage/journal"
        
        # Créer le hook dans le bon emplacement
        HOOK_FILE="$GIT_DIR_FULL/hooks/post-commit"
        
        cat > "$HOOK_FILE" << 'EOFHOOK'
#!/bin/bash
# 📓 HOOK GIT POST-COMMIT - JOURNALISATION AUTOMATIQUE
# Crée/met à jour automatiquement le journal à chaque commit

JOURNAL_DIR="copilotage/journal"
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M:%S)
HOST=$(hostname)
PID=$$
COMMIT_MSG=$(git log -1 --pretty=%B)
COMMIT_HASH=$(git log -1 --pretty=%H)
COMMIT_SHORT=$(git log -1 --pretty=%h)

# Créer dossier journal si nécessaire
mkdir -p "$JOURNAL_DIR"

# Fichier journal du jour
JOURNAL_FILE="$JOURNAL_DIR/JOURNAL_AUTO_${DATE}_${HOST}.md"

# Si nouveau journal, créer header
if [ ! -f "$JOURNAL_FILE" ]; then
    cat > "$JOURNAL_FILE" << EOFHEADER
# 📓 Journal Automatique - $DATE

**Host**: $HOST  
**Début session**: $(date --iso-8601=seconds)  
**Système**: Journalisation automatique via Git hooks

---

EOFHEADER
fi

# Ajouter entrée commit
cat >> "$JOURNAL_FILE" << EOFENTRY

## [$TIME] Commit \`$COMMIT_SHORT\`

**Message**: $COMMIT_MSG

**Hash complet**: \`$COMMIT_HASH\`

### Fichiers modifiés

\`\`\`
$(git diff-tree --no-commit-id --name-status -r HEAD)
\`\`\`

### Statistiques

\`\`\`
$(git log -1 --stat)
\`\`\`

---

EOFENTRY

echo "📓 Journal automatique mis à jour: $JOURNAL_FILE"

# Compter commits du jour
COMMITS_TODAY=$(grep -c "## \[" "$JOURNAL_FILE" 2>/dev/null || echo 0)
echo "✅ Commits aujourd'hui: $COMMITS_TODAY"
EOFHOOK
        
        chmod +x "$HOOK_FILE"
        
        if [ -f "$HOOK_FILE" ]; then
            SUCCESS=$((SUCCESS + 1))
            echo "    ✅ Hook installé: $GIT_DIR/hooks/post-commit"
        else
            FAILED=$((FAILED + 1))
            echo "    ❌ Échec installation"
        fi
    else
        FAILED=$((FAILED + 1))
        echo "    ❌ Pas un submodule Git valide"
    fi
    echo ""
done

echo "==========================================================="
echo "📊 RÉSUMÉ INSTALLATION"
echo "==========================================================="
echo ""
echo "Total submodules: $TOTAL"
echo "✅ Installés:     $SUCCESS"
echo "❌ Échecs:        $FAILED"
echo ""

if [ $SUCCESS -eq $TOTAL ]; then
    echo "🎉 SUCCÈS! Tous les hooks sont installés."
    echo ""
    echo "📝 Test recommandé:"
    echo "   1. Entrer dans un submodule: cd modules/core/filesystem"
    echo "   2. Faire un commit test: git commit --allow-empty -m 'Test hook journalisation'"
    echo "   3. Vérifier: cat copilotage/journal/JOURNAL_AUTO_*.md"
else
    echo "⚠️  Attention: $FAILED échec(s) d'installation"
    echo "   Vérifier manuellement les submodules concernés"
fi

echo ""
echo "💡 Pour vérifier l'installation:"
echo "   bash tools/check_hooks_submodules.sh"
echo ""
echo "==========================================================="
