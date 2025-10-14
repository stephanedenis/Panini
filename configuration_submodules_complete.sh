#!/bin/bash
# Script pour configurer tous les repositories Panini-* comme submodules
# Organisation modulaire : modules/, shared/, projects/

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[SUBMOD]${NC} $1"
}

success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

error() {
    echo -e "${RED}[✗]${NC} $1"
}

info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

# Configuration des submodules avec organisation logique
declare -A SUBMODULES_CONFIG=(
    # Core modules
    ["Panini-FS"]="modules/core/filesystem"
    ["Panini-SemanticCore"]="modules/core/semantic"
    
    # Orchestration
    ["Panini-CloudOrchestrator"]="modules/orchestration/cloud"
    ["Panini-ExecutionOrchestrator"]="modules/orchestration/execution"
    
    # Services
    ["Panini-CoLabController"]="modules/services/colab"
    ["Panini-PublicationEngine"]="modules/services/publication"
    ["Panini-DatasetsIngestion"]="modules/services/datasets"
    
    # Infrastructure
    ["Panini-UltraReactive"]="modules/infrastructure/reactive"
    ["Panini-AutonomousMissions"]="modules/infrastructure/autonomous"
    
    # Shared components
    ["Panini-CopilotageShared"]="shared/copilotage"
    ["Panini-SpecKit-Shared"]="shared/speckit"
    ["Panini-AttributionRegistry"]="shared/attribution"
    
    # Research (déjà existant mais à déplacer)
    ["Panini-Research"]="research"
)

# Fonction pour créer la structure de répertoires
create_directory_structure() {
    log "Création de la structure modulaire..."
    
    # Créer les répertoires principaux
    mkdir -p modules/{core,orchestration,services,infrastructure}
    mkdir -p shared
    mkdir -p projects
    mkdir -p research
    
    success "✅ Structure modulaire créée"
}

# Fonction pour ajouter un submodule
add_submodule() {
    local repo_name="$1"
    local submodule_path="$2"
    
    log "Ajout submodule: $repo_name → $submodule_path"
    
    # Vérifier si le repository existe sur GitHub
    if ! gh repo view "stephanedenis/$repo_name" &>/dev/null; then
        error "Repository $repo_name introuvable sur GitHub"
        return 1
    fi
    
    # Vérifier si le submodule existe déjà
    if git config --file .gitmodules --get-regexp "submodule\..*\.path" | grep -q "$submodule_path"; then
        warning "Submodule déjà configuré pour $submodule_path"
        return 0
    fi
    
    # Créer le répertoire parent si nécessaire
    local parent_dir=$(dirname "$submodule_path")
    if [ ! -d "$parent_dir" ]; then
        mkdir -p "$parent_dir"
    fi
    
    # Supprimer le répertoire cible s'il existe et n'est pas un submodule
    if [ -d "$submodule_path" ] && [ ! -f "$submodule_path/.git" ]; then
        warning "Suppression répertoire existant: $submodule_path"
        rm -rf "$submodule_path"
    fi
    
    # Ajouter le submodule
    local repo_url="https://github.com/stephanedenis/$repo_name.git"
    if git submodule add "$repo_url" "$submodule_path"; then
        success "✅ Submodule ajouté: $repo_name → $submodule_path"
        return 0
    else
        error "❌ Échec ajout submodule: $repo_name"
        return 1
    fi
}

# Fonction pour déplacer un submodule existant
move_existing_submodule() {
    local repo_name="$1"
    local old_path="$2"
    local new_path="$3"
    
    log "Déplacement submodule: $old_path → $new_path"
    
    # Supprimer l'ancien submodule
    git submodule deinit -f "$old_path"
    git rm -f "$old_path"
    rm -rf ".git/modules/$old_path"
    
    # Ajouter à la nouvelle position
    add_submodule "$repo_name" "$new_path"
}

# Fonction pour traiter tous les submodules
configure_all_submodules() {
    log "🏗️ CONFIGURATION COMPLÈTE DES SUBMODULES PANINI"
    echo "================================================="
    
    # Créer la structure
    create_directory_structure
    
    # Traiter le submodule Research existant
    if [ -d "PaniniFS-Research" ]; then
        move_existing_submodule "Panini-Research" "PaniniFS-Research" "research"
    fi
    
    # Traiter le submodule CopilotageShared existant  
    if [ -d "copilotage/shared" ]; then
        move_existing_submodule "Panini-CopilotageShared" "copilotage/shared" "shared/copilotage"
    fi
    
    # Ajouter tous les nouveaux submodules
    local total=0
    local success_count=0
    local failed_repos=()
    
    for repo_name in "${!SUBMODULES_CONFIG[@]}"; do
        local submodule_path="${SUBMODULES_CONFIG[$repo_name]}"
        total=$((total + 1))
        
        # Ignorer ceux déjà traités
        if [ "$repo_name" = "Panini-Research" ] || [ "$repo_name" = "Panini-CopilotageShared" ]; then
            success_count=$((success_count + 1))
            continue
        fi
        
        echo ""
        if add_submodule "$repo_name" "$submodule_path"; then
            success_count=$((success_count + 1))
        else
            failed_repos+=("$repo_name")
        fi
        
        # Pause courte entre ajouts
        sleep 1
    done
    
    echo ""
    echo "📊 RÉSUMÉ CONFIGURATION SUBMODULES"
    echo "=================================="
    success "✅ Submodules configurés: $success_count/$total"
    
    if [ ${#failed_repos[@]} -gt 0 ]; then
        warning "❌ Repositories avec problèmes:"
        for repo in "${failed_repos[@]}"; do
            echo "   - $repo"
        done
        return 1
    else
        success "🎉 Tous les submodules configurés avec succès !"
        return 0
    fi
}

# Fonction pour initialiser tous les submodules
initialize_submodules() {
    log "🔄 INITIALISATION DES SUBMODULES"
    echo "================================"
    
    git submodule update --init --recursive
    
    if [ $? -eq 0 ]; then
        success "✅ Tous les submodules initialisés"
    else
        error "❌ Problème lors de l'initialisation"
        return 1
    fi
}

# Fonction pour afficher l'état final
show_final_status() {
    log "📊 ÉTAT FINAL DES SUBMODULES"
    echo "============================="
    
    echo ""
    info "Structure créée:"
    tree -d -L 3 . 2>/dev/null || find . -type d -name ".git" -prune -o -type d -print | head -20
    
    echo ""
    info "Submodules configurés:"
    git submodule status
    
    echo ""
    info "Configuration .gitmodules:"
    cat .gitmodules
}

# Fonction pour créer la documentation
create_documentation() {
    log "📝 CRÉATION DOCUMENTATION ARCHITECTURE"
    
    cat > ARCHITECTURE_MODULAIRE.md << 'EOF'
# 🏗️ Architecture Modulaire Panini

## Structure Organisée

```
Panini/ (Repository Parent Principal)
├── modules/                     # Modules fonctionnels
│   ├── core/                   # Composants centraux
│   │   ├── filesystem/         # Panini-FS
│   │   └── semantic/           # Panini-SemanticCore
│   ├── orchestration/          # Orchestrateurs
│   │   ├── cloud/              # Panini-CloudOrchestrator
│   │   └── execution/          # Panini-ExecutionOrchestrator
│   ├── services/               # Services applicatifs
│   │   ├── colab/              # Panini-CoLabController
│   │   ├── publication/        # Panini-PublicationEngine
│   │   └── datasets/           # Panini-DatasetsIngestion
│   └── infrastructure/         # Infrastructure
│       ├── reactive/           # Panini-UltraReactive
│       └── autonomous/         # Panini-AutonomousMissions
├── shared/                     # Composants partagés
│   ├── copilotage/             # Panini-CopilotageShared
│   ├── speckit/                # Panini-SpecKit-Shared
│   └── attribution/            # Panini-AttributionRegistry
├── projects/                   # Projets applicatifs
│   └── (à venir)
└── research/                   # Recherche et développement
    └── (Panini-Research)
```

## Navigation

### Accès aux modules
```bash
# Module filesystem core
cd modules/core/filesystem

# Service de collaboration
cd modules/services/colab

# Composant partagé
cd shared/copilotage

# Recherche
cd research
```

### Gestion des submodules

```bash
# Initialiser tous les submodules
git submodule update --init --recursive

# Mettre à jour tous les submodules
git submodule update --remote

# Mettre à jour un submodule spécifique
git submodule update --remote modules/core/filesystem
```

## Avantages

- ✅ **Structure claire** : Organisation logique par fonctionnalité
- ✅ **Navigation intuitive** : Chemins descriptifs
- ✅ **Développement modulaire** : Indépendance des composants
- ✅ **Maintenance facilitée** : Séparation des responsabilités
- ✅ **Collaboration optimisée** : Accès centralisé depuis Panini
EOF

    success "✅ Documentation créée: ARCHITECTURE_MODULAIRE.md"
}

# Menu principal
show_menu() {
    echo "🏗️ CONFIGURATION SUBMODULES PANINI - ARCHITECTURE MODULAIRE"
    echo "============================================================="
    echo ""
    echo "1. 🔍 Voir l'état actuel des submodules"
    echo "2. 🏗️ Configurer tous les submodules (COMPLET)"
    echo "3. 🔄 Initialiser les submodules existants"
    echo "4. 📝 Créer documentation architecture"
    echo "5. 📊 Afficher statut final"
    echo "6. ❌ Quitter"
    echo ""
    read -p "Choisir une option (1-6): " choice
    
    case $choice in
        1)
            git submodule status
            ;;
        2)
            configure_all_submodules
            initialize_submodules
            create_documentation
            show_final_status
            ;;
        3)
            initialize_submodules
            ;;
        4)
            create_documentation
            ;;
        5)
            show_final_status
            ;;
        6)
            log "Au revoir !"
            exit 0
            ;;
        *)
            error "Option invalide"
            ;;
    esac
}

# Fonction principale
main() {
    cd /home/stephane/GitHub/Panini 2>/dev/null || {
        error "Impossible d'accéder au repository Panini"
        exit 1
    }
    
    if [ "$1" = "--configure" ]; then
        configure_all_submodules
        initialize_submodules
        create_documentation
    elif [ "$1" = "--status" ]; then
        show_final_status
    else
        show_menu
    fi
}

# Point d'entrée
main "$@"