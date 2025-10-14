#!/bin/bash
# Script de renommage GitHub un par un avec gestion des repositories déjà renommés

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[RENAME]${NC} $1"
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

# Mappages de renommage
declare -A RENAME_MAP=(
    ["PaniniFS"]="Panini-FS"
    ["PaniniFS-AutonomousMissions"]="Panini-AutonomousMissions"
    ["PaniniFS-CloudOrchestrator"]="Panini-CloudOrchestrator"
    ["PaniniFS-CoLabController"]="Panini-CoLabController"
    ["PaniniFS-CopilotageShared"]="Panini-CopilotageShared"
    ["PaniniFS-DatasetsIngestion"]="Panini-DatasetsIngestion"
    ["PaniniFS-ExecutionOrchestrator"]="Panini-ExecutionOrchestrator"
    ["PaniniFS-PublicationEngine"]="Panini-PublicationEngine"
    ["PaniniFS-SemanticCore"]="Panini-SemanticCore"
    ["PaniniFS-SpecKit-Shared"]="Panini-SpecKit-Shared"
    ["PaniniFS-UltraReactive"]="Panini-UltraReactive"
)

# Fonction pour renommer un repository
rename_single_repo() {
    local old_name="$1"
    local new_name="$2"
    
    log "🔄 Traitement: $old_name → $new_name"
    
    # Vérifier si le repository local existe (ancien nom)
    local old_path="/home/stephane/GitHub/$old_name"
    local new_path="/home/stephane/GitHub/$new_name"
    
    if [ ! -d "$old_path" ]; then
        if [ -d "$new_path" ]; then
            success "✅ $old_name déjà renommé vers $new_name (local)"
        else
            warning "Repository local $old_name introuvable"
        fi
        return 0
    fi
    
    # Vérifier si le nouveau nom existe déjà sur GitHub
    if gh repo view "stephanedenis/$new_name" &>/dev/null; then
        success "✅ Repository GitHub $new_name existe déjà"
    else
        # Renommer sur GitHub
        log "Renommage GitHub: $old_name → $new_name"
        if gh api -X PATCH "/repos/stephanedenis/$old_name" -f "name=$new_name" &>/dev/null; then
            success "✅ Repository GitHub renommé: $old_name → $new_name"
        else
            error "❌ Échec renommage GitHub: $old_name → $new_name"
            return 1
        fi
    fi
    
    # Renommer le dossier local si nécessaire
    if [ -d "$old_path" ] && [ ! -d "$new_path" ]; then
        log "Renommage dossier local: $old_name → $new_name"
        mv "$old_path" "$new_path"
        success "✅ Dossier local renommé: $old_name → $new_name"
    fi
    
    # Mettre à jour l'URL remote
    if [ -d "$new_path" ]; then
        cd "$new_path"
        local new_url="git@github.com:stephanedenis/$new_name.git"
        git remote set-url origin "$new_url"
        success "✅ URL remote mise à jour: $new_name"
    fi
    
    return 0
}

# Fonction pour traiter tous les renommages
process_all_renames() {
    log "🚀 RENOMMAGE SYSTEMATIQUE - REPOSITORIES PANINI"
    echo "==============================================="
    
    local total=0
    local success_count=0
    local failed_repos=()
    
    for old_name in "${!RENAME_MAP[@]}"; do
        local new_name="${RENAME_MAP[$old_name]}"
        total=$((total + 1))
        
        echo ""
        if rename_single_repo "$old_name" "$new_name"; then
            success_count=$((success_count + 1))
        else
            failed_repos+=("$old_name")
        fi
        
        # Pause courte entre renommages
        sleep 1
    done
    
    echo ""
    echo "📊 RÉSUMÉ DES RENOMMAGES"
    echo "======================="
    success "✅ Repositories traités: $success_count/$total"
    
    if [ ${#failed_repos[@]} -gt 0 ]; then
        warning "❌ Repositories avec problèmes:"
        for repo in "${failed_repos[@]}"; do
            echo "   - $repo"
        done
        return 1
    else
        success "🎉 Tous les renommages terminés avec succès !"
        return 0
    fi
}

# Fonction pour vérifier l'état après renommage
check_rename_status() {
    log "🔍 VÉRIFICATION ÉTAT POST-RENOMMAGE"
    echo "==================================="
    
    echo "Repositories locaux:"
    ls /home/stephane/GitHub/ | grep -E "(Panini|PaniniFS)" | sort
    
    echo ""
    echo "Repositories GitHub:"
    gh repo list stephanedenis | grep -E "(Panini|PaniniFS)" | sort
}

# Menu principal
main() {
    case "${1:-}" in
        --status)
            check_rename_status
            ;;
        *)
            process_all_renames
            echo ""
            check_rename_status
            ;;
    esac
}

# Point d'entrée
main "$@"