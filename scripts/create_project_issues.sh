#!/bin/bash
# Script pour créer les issues initiales des projets dhātu

echo "📝 Création issues initiales projets dhātu"
echo "=========================================="

# Function pour créer une issue et l'ajouter à un projet
create_project_issue() {
    local project_number="$1"
    local title="$2"
    local body="$3"
    local label="$4"
    
    echo "📝 Création issue: $title"
    
    # Créer l'issue dans le repository
    local issue_url=$(gh issue create \
        --repo stephanedenis/PaniniFS-Research \
        --title "$title" \
        --body "$body" \
        --label "$label")
    
    if [ $? -eq 0 ]; then
        echo "   ✅ Issue créée: $issue_url"
        
        # Extraire le numéro de l'issue de l'URL
        local issue_number=$(echo "$issue_url" | grep -o '[0-9]*$')
        
        # Ajouter l'issue au projet
        if [ -n "$issue_number" ]; then
            gh project item-add $project_number --owner stephanedenis --url "$issue_url" 2>/dev/null || \
                echo "   ⚠️  Issue créée mais non ajoutée au projet (nécessite configuration manuelle)"
        fi
    else
        echo "   ❌ Erreur création issue"
    fi
    
    sleep 2  # Éviter rate limiting
}

# Issues pour chaque catégorie de projet
create_core_issues() {
    local project_number="$1"
    local project_name="$2"
    
    create_project_issue "$project_number" \
        "📚 Setup documentation $project_name" \
        "Configurer la documentation de base du projet $project_name:
- README.md avec description
- Architecture technique
- Guide installation
- Exemples d'usage
- Liens vers /projects/ documentation" \
        "documentation"
    
    create_project_issue "$project_number" \
        "🏗️ Project architecture $project_name" \
        "Définir l'architecture technique du projet $project_name:
- Structure modules/packages
- Interfaces API
- Dépendances externes
- Patterns de design
- Tests framework" \
        "architecture"
        
    create_project_issue "$project_number" \
        "🧪 Initial testing framework $project_name" \
        "Mettre en place le framework de tests pour $project_name:
- Tests unitaires
- Tests intégration
- CI/CD pipeline
- Coverage reporting
- Performance benchmarks" \
        "testing"
        
    create_project_issue "$project_number" \
        "🚀 MVP implementation $project_name" \
        "Implémenter le MVP (Minimum Viable Product) de $project_name:
- Fonctionnalités core
- Interface basique
- Validation proof-of-concept
- Documentation utilisateur
- Déploiement initial" \
        "enhancement"
}

echo ""
echo "🎯 Création issues pour projets CORE..."

# Projets CORE
create_core_issues 1 "dhatu-universal-compressor"
create_core_issues 2 "dhatu-corpus-manager" 
create_core_issues 3 "dhatu-web-framework"
create_core_issues 4 "dhatu-gpu-accelerator"

echo ""
echo "🎯 Création issues pour projets TOOLS..."

# Projets TOOLS (même structure d'issues)
create_core_issues 5 "dhatu-pattern-analyzer"
create_core_issues 6 "dhatu-creative-generator"
create_core_issues 7 "dhatu-space-visualizer"
create_core_issues 8 "dhatu-evolution-simulator"

echo ""
echo "🎯 Création issues pour projets INTERFACES..."

# Projets INTERFACES
create_core_issues 9 "dhatu-dashboard"
create_core_issues 10 "dhatu-api-gateway"

echo ""
echo "🎯 Création issues pour projets RESEARCH..."

# Projets RESEARCH
create_core_issues 11 "dhatu-linguistics-engine"
create_core_issues 12 "dhatu-multimodal-learning"

echo ""
echo "🎉 Création des issues initiales terminée!"
echo ""
echo "📋 Issues créées pour tous les 12 projets dhātu"
echo "🔗 Voir les issues: https://github.com/stephanedenis/PaniniFS-Research/issues"
echo "🔗 Voir les projets: https://github.com/stephanedenis/PaniniFS-Research/projects"
echo ""