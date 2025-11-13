#!/bin/bash
# Désactive les workflows GitHub en les renommant avec .disabled

set -e

REPO_ROOT="/home/stephane/GitHub/Panini"
cd "$REPO_ROOT"

echo "🔧 Désactivation des workflows GitHub problématiques"
echo "=================================================="
echo ""

# Liste des workflows à désactiver (chemins relatifs)
WORKFLOWS_TO_DISABLE=(
    "modules/core/filesystem/.github/workflows/copilotage-ci.yml"
    "modules/core/filesystem/.github/workflows/copilotage-journal-check.yml"
    "modules/core/filesystem/.github/workflows/copilotage-journal-index.yml"
    "modules/core/filesystem/.github/workflows/dhatu-validation.yml"
    "modules/core/filesystem/.github/workflows/e2e-playwright.yml"
    "modules/core/filesystem/.github/workflows/paniniFS-ci.yml"
    "modules/core/filesystem/.github/workflows/pages-diagnostics.yml"
    "modules/core/filesystem/.github/workflows/deploy-pages-mkdocs.yml"
    "modules/core/filesystem/.github/workflows/docs-pages.yml"
    "modules/data/attribution/.github/workflows/ci.yml"
    "modules/ontowave/.github/workflows/ci.yml"
    "modules/ontowave/.github/workflows/npm-publish.yml"
    "modules/ontowave/.github/workflows/roadmap.yml"
    "modules/ontowave/.github/workflows/pr-preview.yml"
    "modules/ontowave/.github/workflows/pages.yml"
    "modules/ontowave/.github/workflows/e2e.yml"
    "modules/orchestration/colab/.github/workflows/ci.yml"
    "modules/publication/engine/.github/workflows/ci.yml"
    "modules/missions/autonomous/.github/workflows/ci.yml"
)

count=0
for workflow in "${WORKFLOWS_TO_DISABLE[@]}"; do
    if [ -f "$workflow" ]; then
        # Vérifier si déjà désactivé
        if [ -f "$workflow.disabled" ]; then
            echo "  ⏭️  Déjà désactivé: $workflow"
        else
            mv "$workflow" "$workflow.disabled"
            echo "  ✅ Désactivé: $workflow → $workflow.disabled"
            ((count++))
        fi
    else
        echo "  ⚠️  Non trouvé: $workflow"
    fi
done

echo ""
echo "=================================================="
echo "✅ Désactivé $count workflows"
echo ""
echo "Les workflows sont renommés .yml.disabled"
echo "GitHub ne les exécutera plus automatiquement"
echo ""
echo "Pour réactiver un workflow:"
echo "  mv <fichier>.yml.disabled <fichier>.yml"
echo ""
