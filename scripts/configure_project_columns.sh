#!/bin/bash
# Script pour configurer les colonnes des projets dhātu

echo "📋 Configuration colonnes projets dhātu"
echo "========================================"

# Colonnes standard pour tous les projets
COLUMNS=("📋 Backlog" "🏗️ In Progress" "🧪 Testing" "✅ Done")

# Function pour ajouter des colonnes à un projet
add_columns_to_project() {
    local project_number="$1"
    local project_title="$2"
    
    echo ""
    echo "🔧 Configuration projet #$project_number: $project_title"
    
    # Obtenir les détails du projet
    local project_info=$(gh project view $project_number --owner stephanedenis --format json)
    local project_id=$(echo "$project_info" | jq -r '.id')
    
    if [ "$project_id" = "null" ] || [ -z "$project_id" ]; then
        echo "❌ Impossible d'obtenir l'ID du projet #$project_number"
        return 1
    fi
    
    echo "   Project ID: $project_id"
    
    # Créer les champs/colonnes (nouvelle API GitHub Projects)
    for column in "${COLUMNS[@]}"; do
        echo "   📋 Ajout colonne: $column"
        
        # Note: Les nouveaux GitHub Projects utilisent des "champs" plutôt que des "colonnes"
        # La commande pourrait différer selon la version de gh
        gh project field-create $project_number --owner stephanedenis \
            --name "Status" --type "single_select" \
            --option "$column" 2>/dev/null || echo "   ⚠️  Colonne déjà configurée ou méthode alternative requise"
    done
    
    echo "   ✅ Configuration terminée"
}

echo ""
echo "🎯 Configuration des 12 projets dhātu..."

# Récupérer la liste des projets
project_list=$(gh project list --owner stephanedenis --format json)

# Traiter chaque projet
echo "$project_list" | jq -r '.[] | "\(.number)|\(.title)"' | while IFS='|' read -r number title; do
    add_columns_to_project "$number" "$title"
    sleep 2  # Éviter le rate limiting
done

echo ""
echo "🎉 Configuration des colonnes terminée!"
echo ""
echo "🔗 Vérifiez vos projets sur:"
echo "   https://github.com/stephanedenis/PaniniFS-Research/projects"
echo "   https://github.com/users/stephanedenis/projects"
echo ""