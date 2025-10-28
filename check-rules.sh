#!/bin/bash

# 🌿 Script d'aide pour respecter les règles de développement Panini
# Usage: ./check-rules.sh [command]

set -e

# Couleurs pour output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🌿 Vérification des Règles de Développement Panini${NC}"
echo "=================================================="

# Fonction pour vérifier la branche actuelle
check_branch() {
    current_branch=$(git branch --show-current)
    
    if [ "$current_branch" = "main" ]; then
        echo -e "${RED}❌ ERREUR: Vous êtes sur la branche main${NC}"
        echo -e "${YELLOW}⚠️  Règle: Chaque issue doit être traitée dans une branche dédiée${NC}"
        echo ""
        echo "Solutions :"
        echo "1. Créer une nouvelle branche :"
        echo "   git checkout -b fix/description-du-probleme"
        echo "   git checkout -b feature/nom-de-la-fonctionnalite"
        echo ""
        return 1
    else
        echo -e "${GREEN}✅ Branche dédiée: $current_branch${NC}"
        
        # Vérifier la convention de nommage
        if [[ $current_branch =~ ^(feature|fix|refactor|docs)/.+ ]]; then
            echo -e "${GREEN}✅ Convention de nommage respectée${NC}"
        else
            echo -e "${YELLOW}⚠️  Convention de nommage recommandée:${NC}"
            echo "   feature/nom-fonctionnalite"
            echo "   fix/nom-du-bug"
            echo "   refactor/nom-refactoring"
            echo "   docs/nom-documentation"
        fi
    fi
    echo ""
}

# Fonction pour vérifier les tests Playwright
check_playwright() {
    echo -e "${BLUE}🧪 Vérification des Tests Playwright${NC}"
    
    if [ -d "tests/e2e" ]; then
        test_count=$(find tests/e2e -name "*.spec.js" | wc -l)
        echo -e "${GREEN}✅ Dossier tests/e2e trouvé ($test_count tests)${NC}"
        
        # Lister les tests
        if [ $test_count -gt 0 ]; then
            echo "Tests disponibles :"
            find tests/e2e -name "*.spec.js" | sed 's|tests/e2e/||' | sed 's/^/  - /'
        fi
    else
        echo -e "${YELLOW}⚠️  Dossier tests/e2e non trouvé${NC}"
        echo "Créer avec: mkdir -p tests/e2e"
    fi
    echo ""
}

# Fonction pour vérifier les captures d'écran
check_screenshots() {
    echo -e "${BLUE}📸 Vérification des Captures d'Écran${NC}"
    
    # Rechercher des captures récentes
    screenshots=$(find . -name "*.png" -mtime -1 2>/dev/null | grep -v node_modules | head -5)
    
    if [ -n "$screenshots" ]; then
        echo -e "${GREEN}✅ Captures d'écran récentes trouvées:${NC}"
        echo "$screenshots" | sed 's/^/  - /'
    else
        echo -e "${YELLOW}⚠️  Aucune capture récente trouvée${NC}"
        echo "Pour features avec impact visuel, générer avec :"
        echo "  npx playwright test tests/e2e/capture-feature.spec.js"
    fi
    echo ""
}

# Fonction pour vérifier les modifications avec impact visuel
check_visual_impact() {
    echo -e "${BLUE}🎨 Vérification Impact Visuel${NC}"
    
    # Vérifier les fichiers modifiés
    if git rev-parse --verify HEAD >/dev/null 2>&1; then
        visual_files=$(git diff --name-only HEAD~1..HEAD 2>/dev/null | grep -E '\.(css|scss|vue|html|jsx?|tsx?|md)$' || true)
        
        if [ -n "$visual_files" ]; then
            echo -e "${YELLOW}⚠️  Fichiers avec potentiel impact visuel modifiés:${NC}"
            echo "$visual_files" | sed 's/^/  - /'
            echo ""
            echo -e "${RED}📸 OBLIGATOIRE: Joindre capture d'écran au PR${NC}"
        else
            echo -e "${GREEN}✅ Aucun impact visuel détecté${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  Impossible de vérifier l'impact visuel (nouveau repo)${NC}"
    fi
    echo ""
}

# Fonction pour créer une branche selon les règles
create_branch() {
    echo -e "${BLUE}🌿 Création de Branche selon les Règles${NC}"
    echo ""
    echo "Types de branches disponibles :"
    echo "1. fix/nom-du-bug - Pour corriger un problème"
    echo "2. feature/nom-fonctionnalite - Pour une nouvelle fonctionnalité"  
    echo "3. refactor/nom-refactoring - Pour du refactoring"
    echo "4. docs/nom-documentation - Pour la documentation"
    echo ""
    read -p "Choisissez le type (1-4): " choice
    read -p "Nom de la branche (sans préfixe): " branch_name
    
    case $choice in
        1) prefix="fix" ;;
        2) prefix="feature" ;;
        3) prefix="refactor" ;;
        4) prefix="docs" ;;
        *) echo "Choix invalide"; exit 1 ;;
    esac
    
    full_branch="$prefix/$branch_name"
    
    echo ""
    echo -e "${BLUE}Création de la branche: $full_branch${NC}"
    git checkout main
    git pull origin main
    git checkout -b "$full_branch"
    
    echo -e "${GREEN}✅ Branche créée avec succès!${NC}"
    echo ""
    echo "Prochaines étapes :"
    echo "1. Développer votre fonctionnalité"
    echo "2. Écrire des tests Playwright si nécessaire"
    echo "3. Générer des captures si impact visuel"
    echo "4. Commiter et pusher"
    echo "5. Créer un PR avec template"
}

# Fonction pour exécuter tous les tests
run_tests() {
    echo -e "${BLUE}🧪 Exécution des Tests Playwright${NC}"
    
    if [ -d "tests/e2e" ]; then
        if command -v npx >/dev/null 2>&1; then
            echo "Exécution des tests..."
            npx playwright test tests/e2e/
        else
            echo -e "${RED}❌ npx non trouvé. Installer Node.js/npm${NC}"
            exit 1
        fi
    else
        echo -e "${YELLOW}⚠️  Aucun test trouvé dans tests/e2e/${NC}"
    fi
}

# Fonction pour générer template PR
generate_pr_template() {
    echo -e "${BLUE}📋 Génération Template PR${NC}"
    
    current_branch=$(git branch --show-current)
    
    cat > PR_DRAFT.md << EOF
## 📋 Description

<!-- Décrivez brièvement les changements apportés -->

## 🏷️ Type de changement

- [ ] 🐛 Bug fix
- [ ] ✨ Nouvelle fonctionnalité  
- [ ] 💥 Breaking change
- [ ] 📚 Documentation uniquement
- [ ] 🎨 **Impact visuel**

## 📸 Preuves Visuelles

<!-- ⚠️ OBLIGATOIRE si "Impact visuel" est coché -->

### 🖼️ Capture d'écran - Résultat Final

![Validation](VALIDATION-$(echo $current_branch | tr '/' '-' | tr '[:lower:]' '[:upper:]').png)

## ✅ Checklist

- [ ] 🌿 Branche créée depuis main ($current_branch)
- [ ] 🧪 Tests Playwright passent
- [ ] 📸 Capture d'écran jointe (si impact visuel)
- [ ] 📝 Description complète

Closes #[numéro_issue]
EOF

    echo -e "${GREEN}✅ Template PR généré: PR_DRAFT.md${NC}"
}

# Menu principal
case "$1" in
    "branch")
        create_branch
        ;;
    "test")
        run_tests
        ;;
    "template")
        generate_pr_template
        ;;
    "")
        check_branch
        check_playwright
        check_screenshots
        check_visual_impact
        
        echo -e "${BLUE}📋 Commandes Disponibles:${NC}"
        echo "  ./check-rules.sh branch     - Créer une branche selon les règles"
        echo "  ./check-rules.sh test       - Exécuter les tests Playwright"
        echo "  ./check-rules.sh template   - Générer template PR"
        echo ""
        ;;
    *)
        echo "Usage: $0 [branch|test|template]"
        exit 1
        ;;
esac