#!/bin/bash
# Script pour vérifier les hooks de journalisation dans tous les submodules
# Usage: ./check_hooks_submodules.sh

echo "🔍 VÉRIFICATION HOOKS JOURNALISATION - SUBMODULES"
echo "=================================================="
echo ""

PROJECT_ROOT="/home/stephane/GitHub/Panini"
cd "$PROJECT_ROOT"

# Liste des submodules
SUBMODULES=$(git submodule status | awk '{print $2}')

echo "📦 Submodules détectés:"
echo "$SUBMODULES" | nl
echo ""

echo "🔍 Vérification hooks post-commit:"
echo "-----------------------------------"
echo ""

TOTAL=0
WITH_HOOK=0
WITHOUT_HOOK=0

for submodule in $SUBMODULES; do
    TOTAL=$((TOTAL + 1))
    
    # Pour les submodules, .git est un fichier qui pointe vers .git/modules/...
    if [ -f "$PROJECT_ROOT/$submodule/.git" ]; then
        GIT_DIR=$(grep "gitdir:" "$PROJECT_ROOT/$submodule/.git" | cut -d' ' -f2)
        HOOK_PATH="$PROJECT_ROOT/$submodule/$GIT_DIR/hooks/post-commit"
    else
        HOOK_PATH="$PROJECT_ROOT/$submodule/.git/hooks/post-commit"
    fi
    
    if [ -f "$HOOK_PATH" ]; then
        WITH_HOOK=$((WITH_HOOK + 1))
        echo "✅ $submodule"
        echo "   Hook: $(ls -lh "$HOOK_PATH" 2>/dev/null | awk '{print $5" "}')"
    else
        WITHOUT_HOOK=$((WITHOUT_HOOK + 1))
        echo "❌ $submodule"
        echo "   Hook manquant: $HOOK_PATH"
    fi
    echo ""
done

# Projet parent
echo "🏠 Projet Parent (Panini):"
PARENT_HOOK="$PROJECT_ROOT/.git/hooks/post-commit"
if [ -f "$PARENT_HOOK" ]; then
    echo "   ✅ Hook présent"
    echo "   $(ls -lh "$PARENT_HOOK" | awk '{print $5" "$9}')"
else
    echo "   ❌ Hook manquant"
fi
echo ""

echo "=================================================="
echo "📊 RÉSUMÉ"
echo "=================================================="
echo ""
echo "Total submodules: $TOTAL"
echo "✅ Avec hook:     $WITH_HOOK"
echo "❌ Sans hook:     $WITHOUT_HOOK"
echo ""

if [ $WITHOUT_HOOK -gt 0 ]; then
    echo "⚠️  ACTION REQUISE: $WITHOUT_HOOK submodule(s) sans hook de journalisation"
    echo ""
    echo "💡 Pour installer les hooks manquants, utilisez:"
    echo "   bash tools/install_hooks_all_submodules.sh"
else
    echo "✅ Tous les submodules ont leurs hooks de journalisation!"
fi
echo ""
echo "=================================================="
