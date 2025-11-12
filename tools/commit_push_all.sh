#!/bin/bash
# Script pour committer et pusher dans le projet parent et tous les submodules
# Usage: ./commit_push_all.sh "Message de commit"

set -e

PROJECT_ROOT="/home/stephane/GitHub/Panini"
cd "$PROJECT_ROOT"

# Message de commit (argument ou message par défaut)
COMMIT_MSG="${1:-Déploiement système journalisation + réorganisation modules}"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  🚀 COMMIT & PUSH - PROJET PARENT + SUBMODULES              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "📝 Message de commit: $COMMIT_MSG"
echo ""

# Fonction pour commit et push dans un repo
commit_and_push() {
    local REPO_PATH=$1
    local REPO_NAME=$2
    
    cd "$REPO_PATH"
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📦 $REPO_NAME"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Vérifier s'il y a des changements
    if git diff-index --quiet HEAD -- 2>/dev/null; then
        echo "   ℹ️  Aucun changement à committer"
    else
        echo "   📝 Changements détectés:"
        git status --short | head -10
        if [ $(git status --short | wc -l) -gt 10 ]; then
            echo "   ... et $(( $(git status --short | wc -l) - 10 )) autres fichiers"
        fi
        echo ""
        
        # Add all changes
        echo "   ➕ git add -A"
        git add -A
        
        # Commit
        echo "   💾 git commit -m \"$COMMIT_MSG\""
        git commit -m "$COMMIT_MSG" || true
        
        # Push
        echo "   🚀 git push"
        git push || {
            echo "   ⚠️  Push échoué - peut-être besoin de pull d'abord"
            return 1
        }
        
        echo "   ✅ Commit et push réussis"
    fi
    echo ""
}

# Liste des submodules
SUBMODULES=$(git submodule status | awk '{print $2}')

# Compteurs
TOTAL=0
SUCCESS=0
NO_CHANGES=0
FAILED=0

echo "🔍 Traitement des submodules..."
echo ""

# Committer dans chaque submodule
for submodule in $SUBMODULES; do
    TOTAL=$((TOTAL + 1))
    SUBMODULE_PATH="$PROJECT_ROOT/$submodule"
    
    if commit_and_push "$SUBMODULE_PATH" "$submodule"; then
        if git -C "$SUBMODULE_PATH" diff-index --quiet HEAD -- 2>/dev/null; then
            NO_CHANGES=$((NO_CHANGES + 1))
        else
            SUCCESS=$((SUCCESS + 1))
        fi
    else
        FAILED=$((FAILED + 1))
    fi
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🏠 PROJET PARENT (Panini)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Revenir à la racine pour le projet parent
cd "$PROJECT_ROOT"

# Mettre à jour les références des submodules
echo "🔄 Mise à jour des références submodules..."
git add -A

# Vérifier les changements du parent
if git diff-index --quiet HEAD -- 2>/dev/null; then
    echo "   ℹ️  Aucun changement à committer dans le parent"
else
    echo "📝 Changements dans le projet parent:"
    git status --short | head -20
    echo ""
    
    echo "💾 git commit -m \"$COMMIT_MSG\""
    git commit -m "$COMMIT_MSG" || true
    
    echo "🚀 git push"
    git push || {
        echo "⚠️  Push échoué - peut-être besoin de pull d'abord"
    }
    
    echo "✅ Projet parent commité et pushé"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  📊 RÉSUMÉ                                                   ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Submodules traités:   $TOTAL"
echo "✅ Avec changements:   $SUCCESS"
echo "ℹ️  Sans changements:  $NO_CHANGES"
echo "❌ Échecs:             $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "🎉 SUCCÈS! Tous les commits et push sont terminés."
else
    echo "⚠️  Attention: $FAILED échec(s). Vérifier manuellement."
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
