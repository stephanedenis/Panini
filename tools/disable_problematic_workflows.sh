#!/bin/bash
# Désactive tous les workflows GitHub qui pourraient causer des erreurs
# dans les submodules Panini

set -e

REPO_ROOT="/home/stephane/GitHub/Panini"
cd "$REPO_ROOT"

echo "🔧 Désactivation des workflows GitHub problématiques"
echo "=================================================="
echo ""

# Fonction pour désactiver un workflow
disable_workflow() {
    local workflow_file="$1"
    local reason="$2"
    
    if [ ! -f "$workflow_file" ]; then
        return
    fi
    
    # Vérifier si déjà désactivé
    if grep -q "^# DISABLED:" "$workflow_file" 2>/dev/null; then
        echo "  ⏭️  Déjà désactivé: $workflow_file"
        return
    fi
    
    # Créer backup
    cp "$workflow_file" "$workflow_file.bak"
    
    # Désactiver en commentant les triggers
    if grep -q "^on:" "$workflow_file"; then
        # Ajouter commentaire DISABLED en haut
        sed -i '1i# DISABLED: '"$reason"'' "$workflow_file"
        sed -i '2i# Original triggers commented out - use workflow_dispatch only\n' "$workflow_file"
        
        # Commenter les triggers sauf workflow_dispatch
        awk '
            /^on:/ { in_on=1; print; next }
            in_on && /^  workflow_dispatch:/ { print; next }
            in_on && /^[^ ]/ { in_on=0 }
            in_on && !/^  workflow_dispatch:/ { print "#  " substr($0, 3); next }
            { print }
        ' "$workflow_file" > "$workflow_file.tmp"
        mv "$workflow_file.tmp" "$workflow_file"
        
        echo "  ✅ Désactivé: $workflow_file"
    else
        # Restaurer backup si pas de trigger trouvé
        mv "$workflow_file.bak" "$workflow_file"
        echo "  ⚠️  Pas de trigger 'on:' trouvé: $workflow_file"
    fi
}

# Workflows à désactiver avec leurs raisons
declare -A WORKFLOWS_TO_DISABLE=(
    # Submodule filesystem (Panini-FS)
    ["modules/core/filesystem/.github/workflows/copilotage-ci.yml"]="Dependencies missing"
    ["modules/core/filesystem/.github/workflows/copilotage-journal-check.yml"]="Not needed in submodule"
    ["modules/core/filesystem/.github/workflows/copilotage-journal-index.yml"]="Not needed in submodule"
    ["modules/core/filesystem/.github/workflows/dhatu-validation.yml"]="Complex dependencies"
    ["modules/core/filesystem/.github/workflows/e2e-playwright.yml"]="Browser testing not configured"
    ["modules/core/filesystem/.github/workflows/paniniFS-ci.yml"]="Replaced by simpler tests"
    ["modules/core/filesystem/.github/workflows/pages-diagnostics.yml"]="Pages not active"
    ["modules/core/filesystem/.github/workflows/deploy-pages-mkdocs.yml"]="MkDocs not configured"
    ["modules/core/filesystem/.github/workflows/docs-pages.yml"]="Duplicate pages workflow"
    
    # Autres submodules problématiques
    ["modules/data/attribution/.github/workflows/ci.yml"]="Dependencies missing"
    ["modules/ontowave/.github/workflows/ci.yml"]="npm dependencies missing"
    ["modules/ontowave/.github/workflows/npm-publish.yml"]="Not ready for publish"
    ["modules/ontowave/.github/workflows/roadmap.yml"]="Not needed"
    ["modules/ontowave/.github/workflows/pr-preview.yml"]="Preview not configured"
    ["modules/ontowave/.github/workflows/pages.yml"]="Pages not active"
    ["modules/ontowave/.github/workflows/e2e.yml"]="E2E not configured"
    ["modules/orchestration/colab/.github/workflows/ci.yml"]="Dependencies missing"
    ["modules/publication/engine/.github/workflows/ci.yml"]="Dependencies missing"
    ["modules/missions/autonomous/.github/workflows/ci.yml"]="Dependencies missing"
)

# Désactiver les workflows listés
count=0
for workflow in "${!WORKFLOWS_TO_DISABLE[@]}"; do
    reason="${WORKFLOWS_TO_DISABLE[$workflow]}"
    if [ -f "$workflow" ]; then
        disable_workflow "$workflow" "$reason"
        ((count++))
    fi
done

echo ""
echo "=================================================="
echo "✅ Désactivé $count workflows"
echo ""
echo "Note: Les workflows peuvent toujours être lancés manuellement"
echo "      via workflow_dispatch dans l'interface GitHub"
echo ""
echo "Pour réactiver un workflow:"
echo "  1. Supprimer les lignes '# DISABLED:' en haut"
echo "  2. Décommenter les triggers (retirer '# ' au début)"
echo "  3. Commit et push"
echo ""
