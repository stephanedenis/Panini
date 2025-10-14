#!/bin/bash
# Script de préparation des repositories locaux pour le redressement
# Nettoie, commite et prépare tous les repos PaniniFS-* pour le renommage

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[PREP]${NC} $1"
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

# Liste des repositories à traiter
REPOS=(
    "PaniniFS"
    "PaniniFS-AttributionRegistry"
    "PaniniFS-AutonomousMissions"
    "PaniniFS-CloudOrchestrator"
    "PaniniFS-CoLabController"
    "PaniniFS-CopilotageShared"
    "PaniniFS-DatasetsIngestion"
    "PaniniFS-ExecutionOrchestrator"
    "PaniniFS-PublicationEngine"
    "PaniniFS-SemanticCore"
    "PaniniFS-SpecKit-Shared"
    "PaniniFS-UltraReactive"
)

# Fonction pour préparer un repository
prepare_repository() {
    local repo_name="$1"
    local repo_path="/home/stephane/GitHub/$repo_name"
    
    log "Traitement de $repo_name..."
    
    # Vérifier si le repository existe
    if [ ! -d "$repo_path" ]; then
        warning "Repository $repo_name introuvable: $repo_path"
        return 1
    fi
    
    cd "$repo_path"
    
    # Vérifier si c'est un repository Git
    if [ ! -d ".git" ]; then
        warning "$repo_name n'est pas un repository Git"
        return 1
    fi
    
    # Vérifier l'état Git
    if ! git status --porcelain | grep -q .; then
        success "$repo_name déjà propre"
        return 0
    fi
    
    # Il y a des modifications
    warning "$repo_name a des modifications non commitées"
    echo "Modifications détectées:"
    git status --short | head -10
    
    # Proposer des actions
    echo ""
    echo "Actions possibles pour $repo_name:"
    echo "1. Commiter toutes les modifications"
    echo "2. Stash (sauvegarder temporairement)"
    echo "3. Reset (perdre les modifications) ⚠️"
    echo "4. Ignorer ce repository"
    echo ""
    
    read -p "Choisir action (1-4): " -n 1 -r
    echo
    
    case $REPLY in
        1)
            log "Commit des modifications dans $repo_name..."
            git add -A
            git commit -m "feat: Préparation pour redressement architectural

Modifications automatiquement commitées avant renommage PaniniFS-* → Panini-*
Date: $(date)
Script: preparation_repositories_locaux.sh

Ces modifications étaient en attente et ont été sauvegardées
avant la transformation architecturale."
            
            if [ $? -eq 0 ]; then
                success "✅ Modifications commitées dans $repo_name"
            else
                error "❌ Échec du commit dans $repo_name"
                return 1
            fi
            ;;
        2)
            log "Stash des modifications dans $repo_name..."
            git stash push -m "Sauvegarde avant redressement architectural $(date)"
            
            if [ $? -eq 0 ]; then
                success "✅ Modifications stashées dans $repo_name"
                info "Pour récupérer: cd $repo_path && git stash pop"
            else
                error "❌ Échec du stash dans $repo_name"
                return 1
            fi
            ;;
        3)
            warning "⚠️ Reset des modifications dans $repo_name (PERTE DE DONNÉES)"
            read -p "Confirmer reset ? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                git reset --hard HEAD
                git clean -fd
                success "✅ Repository $repo_name reseté"
            else
                warning "Reset annulé pour $repo_name"
                return 1
            fi
            ;;
        4)
            warning "Repository $repo_name ignoré"
            return 1
            ;;
        *)
            error "Option invalide"
            return 1
            ;;
    esac
    
    return 0
}

# Fonction pour traiter tous les repositories
prepare_all_repositories() {
    log "🧹 PRÉPARATION DE TOUS LES REPOSITORIES LOCAUX"
    echo "=============================================="
    
    local total=${#REPOS[@]}
    local success_count=0
    local failed_repos=()
    
    for repo in "${REPOS[@]}"; do
        echo ""
        if prepare_repository "$repo"; then
            success_count=$((success_count + 1))
        else
            failed_repos+=("$repo")
        fi
    done
    
    echo ""
    echo "📊 RÉSUMÉ DE LA PRÉPARATION"
    echo "==========================="
    success "✅ Repositories préparés: $success_count/$total"
    
    if [ ${#failed_repos[@]} -gt 0 ]; then
        warning "❌ Repositories avec problèmes:"
        for repo in "${failed_repos[@]}"; do
            echo "   - $repo"
        done
    fi
    
    if [ ${#failed_repos[@]} -eq 0 ]; then
        success "🎉 Tous les repositories sont prêts pour le renommage !"
        return 0
    else
        warning "⚠️ Certains repositories nécessitent attention manuelle"
        return 1
    fi
}

# Fonction pour vérifier l'état global
check_repositories_status() {
    log "🔍 VÉRIFICATION DE L'ÉTAT GLOBAL"
    echo "================================"
    
    for repo in "${REPOS[@]}"; do
        local repo_path="/home/stephane/GitHub/$repo"
        
        if [ ! -d "$repo_path" ]; then
            error "$repo: Introuvable"
            continue
        fi
        
        cd "$repo_path"
        
        if git status --porcelain | grep -q .; then
            warning "$repo: Modifications non commitées"
        else
            success "$repo: Propre"
        fi
    done
}

# Fonction pour mise à jour des URLs distantes après renommage
update_remote_urls() {
    log "🔗 MISE À JOUR DES URLs DISTANTES POST-RENOMMAGE"
    echo "================================================"
    
    # Mappages de renommage
    declare -A url_mappings=(
        ["PaniniFS"]="Panini-FS"
        ["PaniniFS-AttributionRegistry"]="Panini-AttributionRegistry"
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
    
    for old_name in "${!url_mappings[@]}"; do
        local new_name="${url_mappings[$old_name]}"
        local repo_path="/home/stephane/GitHub/$old_name"
        
        if [ ! -d "$repo_path" ]; then
            warning "$old_name: Repository local introuvable"
            continue
        fi
        
        cd "$repo_path"
        
        # Obtenir l'URL actuelle
        local current_url=$(git remote get-url origin 2>/dev/null || echo "")
        
        if [ -z "$current_url" ]; then
            warning "$old_name: Pas d'URL remote origin"
            continue
        fi
        
        # Construire la nouvelle URL
        local new_url
        if [[ $current_url == *"ssh://git@github.com"* ]]; then
            new_url="ssh://git@github.com/stephanedenis/$new_name.git"
        elif [[ $current_url == *"git@github.com:"* ]]; then
            new_url="git@github.com:stephanedenis/$new_name.git"
        elif [[ $current_url == *"https://github.com"* ]]; then
            new_url="https://github.com/stephanedenis/$new_name.git"
        else
            warning "$old_name: Format URL remote non reconnu: $current_url"
            continue
        fi
        
        # Mettre à jour l'URL
        log "Mise à jour URL remote pour $old_name..."
        info "  Ancienne: $current_url"
        info "  Nouvelle: $new_url"
        
        git remote set-url origin "$new_url"
        
        if [ $? -eq 0 ]; then
            success "✅ URL mise à jour pour $old_name"
        else
            error "❌ Échec mise à jour URL pour $old_name"
        fi
    done
}

# Menu principal
show_menu() {
    echo "🧹 PRÉPARATION REPOSITORIES LOCAUX - REDRESSEMENT PANINI"
    echo "========================================================="
    echo ""
    echo "1. 🔍 Vérifier l'état de tous les repositories"
    echo "2. 🧹 Préparer tous les repositories (commit/stash/clean)"
    echo "3. 🔗 Mettre à jour les URLs distantes (après renommage GitHub)"
    echo "4. ❌ Quitter"
    echo ""
    read -p "Choisir une option (1-4): " choice
    
    case $choice in
        1)
            check_repositories_status
            ;;
        2)
            prepare_all_repositories
            ;;
        3)
            update_remote_urls
            ;;
        4)
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
    cd /home/stephane/GitHub 2>/dev/null || {
        error "Impossible d'accéder au répertoire GitHub"
        exit 1
    }
    
    if [ "$1" = "--status" ]; then
        check_repositories_status
    elif [ "$1" = "--prepare" ]; then
        prepare_all_repositories
    elif [ "$1" = "--update-urls" ]; then
        update_remote_urls
    else
        show_menu
    fi
}

# Point d'entrée
main "$@"