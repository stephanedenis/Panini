#!/bin/bash

# 🎯 Script de validation pour badge de conformité
# Génère un badge indiquant si le projet respecte les règles

set -e

# Vérifier la branche actuelle
current_branch=$(git branch --show-current 2>/dev/null || echo "unknown")

# Vérifier les tests Playwright
playwright_tests=0
if [ -d "tests/e2e" ]; then
    playwright_tests=$(find tests/e2e -name "*.spec.js" | wc -l)
fi

# Vérifier les captures récentes  
screenshots=0
if find . -name "*.png" -mtime -1 2>/dev/null | grep -v node_modules | head -1 >/dev/null; then
    screenshots=1
fi

# Vérifier les templates GitHub
github_templates=0
if [ -f ".github/pull_request_template.md" ] && [ -d ".github/ISSUE_TEMPLATE" ]; then
    github_templates=1
fi

# Calculer le score de conformité
score=0
total=4

if [ "$current_branch" != "main" ] && [[ $current_branch =~ ^(feature|fix|refactor|docs)/.+ ]]; then
    score=$((score + 1))
fi

if [ $playwright_tests -gt 0 ]; then
    score=$((score + 1))
fi

if [ $screenshots -eq 1 ]; then
    score=$((score + 1))  
fi

if [ $github_templates -eq 1 ]; then
    score=$((score + 1))
fi

# Générer le badge
percentage=$((score * 100 / total))

if [ $percentage -eq 100 ]; then
    color="brightgreen"
    status="100%"
elif [ $percentage -ge 75 ]; then
    color="green"  
    status="${percentage}%"
elif [ $percentage -ge 50 ]; then
    color="yellow"
    status="${percentage}%"
else
    color="red"
    status="${percentage}%"
fi

echo "![Conformité Règles](https://img.shields.io/badge/Conformité%20Règles-${status}-${color})"
echo ""
echo "Détails de conformité :"
echo "- Branche dédiée : $([ "$current_branch" != "main" ] && echo "✅" || echo "❌") ($current_branch)"
echo "- Tests Playwright : $([ $playwright_tests -gt 0 ] && echo "✅ ($playwright_tests)" || echo "❌ (0)")"
echo "- Captures récentes : $([ $screenshots -eq 1 ] && echo "✅" || echo "❌")"
echo "- Templates GitHub : $([ $github_templates -eq 1 ] && echo "✅" || echo "❌")"
echo ""
echo "Score : $score/$total ($percentage%)"