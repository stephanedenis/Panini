#!/bin/bash
# Script de rollback du redressement architectural Panini
# Restaure l'état précédent en cas de problème

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[ROLLBACK]${NC} $1"
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

# Répertoire de sauvegarde
BACKUP_DIR="/tmp/panini_redressement_backup_$(date +%Y%m%d_%H%M%S)"
RESTORE_LOG="rollback_$(date +%Y%m%d_%H%M%S).log"

# Fonction pour trouver les sauvegardes existantes
find_backups() {
    log "Recherche des sauvegardes disponibles..."
    
    local backup_patterns=(
        "/tmp/panini_backup_*"
        "/tmp/panini_redressement_backup_*"
        "/home/stephane/GitHub/backup_panini_*"
        "./backup_*"
    )
    
    echo "Sauvegardes trouvées:" | tee -a "$RESTORE_LOG"
    echo "=====================" | tee -a "$RESTORE_LOG"
    
    local found_backups=false
    for pattern in "${backup_patterns[@]}"; do
        for backup in $pattern; do
            if [ -d "$backup" ]; then
                local backup_date=$(stat -c %y "$backup" | cut -d' ' -f1-2)
                echo "📁 $backup (créé: $backup_date)" | tee -a "$RESTORE_LOG"
                found_backups=true
            fi
        done
    done
    
    if [ "$found_backups" = false ]; then
        warning "Aucune sauvegarde automatique trouvée"
        echo "Aucune sauvegarde trouvée" | tee -a "$RESTORE_LOG"
        return 1
    fi
    
    return 0
}

# Fonction pour restaurer depuis une sauvegarde
restore_from_backup() {
    local backup_path="$1"
    
    if [ ! -d "$backup_path" ]; then
        error "Sauvegarde introuvable: $backup_path"
        return 1
    fi
    
    log "Restauration depuis: $backup_path"
    echo "Début restauration: $(date)" | tee -a "$RESTORE_LOG"
    
    # Sauvegarder l'état actuel avant rollback
    log "Sauvegarde de l'état actuel avant rollback..."
    local current_backup="$BACKUP_DIR/current_state"
    mkdir -p "$current_backup"
    
    # Copier fichiers principaux
    cp -r .git "$current_backup/" 2>/dev/null || true
    cp -r modules "$current_backup/" 2>/dev/null || true
    cp -r shared "$current_backup/" 2>/dev/null || true
    cp -r projects "$current_backup/" 2>/dev/null || true
    cp .gitmodules "$current_backup/" 2>/dev/null || true
    cp README.md "$current_backup/" 2>/dev/null || true
    
    # Restaurer les fichiers de la sauvegarde
    log "Restauration des fichiers..."
    
    # .gitmodules
    if [ -f "$backup_path/.gitmodules" ]; then
        cp "$backup_path/.gitmodules" ./ || {
            error "Échec restauration .gitmodules"
            return 1
        }
        success "✅ .gitmodules restauré"
    fi
    
    # README.md
    if [ -f "$backup_path/README.md" ]; then
        cp "$backup_path/README.md" ./ || true
        success "✅ README.md restauré"
    fi
    
    # Structure de répertoires
    for dir in modules shared projects; do
        if [ -d "$dir" ]; then
            rm -rf "$dir"
            log "Supprimé répertoire actuel: $dir"
        fi
        
        if [ -d "$backup_path/$dir" ]; then
            cp -r "$backup_path/$dir" ./ || {
                warning "Problème lors de la restauration de $dir"
            }
            success "✅ Répertoire $dir restauré"
        fi
    done
    
    # Restaurer la configuration Git
    log "Restauration configuration Git..."
    
    # Reset des submodules
    if [ -f .gitmodules ]; then
        git submodule deinit --all -f 2>/dev/null || true
        git submodule init 2>/dev/null || true
        git submodule update 2>/dev/null || true
    fi
    
    # Commit de rollback
    log "Commit de rollback..."
    git add -A
    git commit -m "🔄 Rollback architectural - Restauration depuis sauvegarde
    
Sauvegarde source: $backup_path
Date rollback: $(date)
Script: rollback_redressement_architectural.sh
    
Cette restauration annule les modifications du redressement architectural." || {
        warning "Commit de rollback échoué - changements stagés"
    }
    
    success "✅ Restauration terminée"
    echo "Fin restauration: $(date)" | tee -a "$RESTORE_LOG"
    
    return 0
}

# Fonction pour rollback GitHub (renommage inverse)
rollback_github_renaming() {
    log "Rollback des renommages GitHub..."
    
    warning "⚠️  Cette opération va tenter de restaurer les noms originaux sur GitHub"
    warning "    Elle nécessite GitHub CLI authentifié"
    
    read -p "Continuer avec le rollback GitHub ? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log "Rollback GitHub annulé par l'utilisateur"
        return 0
    fi
    
    # Vérifier GitHub CLI
    if ! command -v gh &> /dev/null || ! gh auth status &> /dev/null; then
        error "GitHub CLI non disponible ou non authentifié"
        return 1
    fi
    
    log "Tentative de rollback des renommages..."
    echo "Début rollback GitHub: $(date)" | tee -a "$RESTORE_LOG"
    
    # Mappages de rollback (inverse du renommage)
    declare -A rollback_mappings=(
        ["Panini-FS"]="PaniniFS"
        ["Panini-Research"]="PaniniFS-Research"
        ["Panini-CopilotageShared"]="PaniniFS-CopilotageShared"
        ["Panini-CoLabController"]="PaniniFS-CoLabController"
        ["Panini-Tools"]="PaniniFS-Tools"
        ["Panini-SecuredPrivate"]="PaniniFS-SecuredPrivate"
        ["Panini-ScienceLab"]="PaniniFS-ScienceLab"
        ["Panini-VisualsLab"]="PaniniFS-VisualsLab"
        ["Panini-WebManager"]="PaniniFS-WebManager"
        ["Panini-SyncManager"]="PaniniFS-SyncManager"
        ["Panini-Gest"]="PaniniFS-Gest"
        ["Panini-LocalOffice"]="PaniniFS-LocalOffice"
    )
    
    local rollback_success=0
    local rollback_total=0
    
    for new_name in "${!rollback_mappings[@]}"; do
        local original_name="${rollback_mappings[$new_name]}"
        rollback_total=$((rollback_total + 1))
        
        log "Tentative: $new_name → $original_name"
        
        # Vérifier si le repo renommé existe
        if gh repo view "stephane-caro/$new_name" &>/dev/null; then
            # Tenter le renommage inverse
            if gh api -X PATCH "/repos/stephane-caro/$new_name" -f "name=$original_name" &>/dev/null; then
                success "✅ $new_name → $original_name"
                rollback_success=$((rollback_success + 1))
            else
                error "❌ Échec rollback: $new_name → $original_name"
            fi
        else
            info "Repository $new_name non trouvé (peut-être déjà rollback)"
        fi
        
        echo "$new_name → $original_name: $(date)" >> "$RESTORE_LOG"
    done
    
    echo "Fin rollback GitHub: $(date)" | tee -a "$RESTORE_LOG"
    echo "Succès: $rollback_success/$rollback_total" | tee -a "$RESTORE_LOG"
    
    if [ "$rollback_success" -gt 0 ]; then
        success "✅ Rollback GitHub partiel ou complet ($rollback_success/$rollback_total)"
    else
        warning "⚠️ Aucun rollback GitHub réussi"
    fi
    
    return 0
}

# Fonction pour rollback complet
full_rollback() {
    log "🔄 ROLLBACK COMPLET DU REDRESSEMENT ARCHITECTURAL"
    echo "=================================================="
    
    warning "⚠️  ATTENTION: Cette opération va:"
    echo "   🔄 Restaurer l'état local depuis une sauvegarde"
    echo "   🔄 Tenter de restaurer les noms GitHub originaux"
    echo "   🔄 Créer un commit de rollback"
    echo "   💾 Sauvegarder l'état actuel avant rollback"
    echo ""
    
    read -p "Confirmer le rollback complet ? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log "Rollback annulé par l'utilisateur"
        exit 0
    fi
    
    # Trouver et choisir une sauvegarde
    if ! find_backups; then
        error "Impossible de procéder sans sauvegarde"
        exit 1
    fi
    
    echo ""
    read -p "Entrez le chemin de la sauvegarde à restaurer: " backup_choice
    
    if [ ! -d "$backup_choice" ]; then
        error "Sauvegarde invalide: $backup_choice"
        exit 1
    fi
    
    # Exécuter le rollback
    echo ""
    log "Début du rollback complet..."
    
    # 1. Rollback local
    if restore_from_backup "$backup_choice"; then
        success "✅ Rollback local réussi"
    else
        error "❌ Rollback local échoué"
        exit 1
    fi
    
    # 2. Rollback GitHub (optionnel)
    echo ""
    rollback_github_renaming
    
    # 3. Résumé final
    echo ""
    success "🎉 Rollback terminé !"
    echo ""
    info "📝 Log de rollback: $RESTORE_LOG"
    info "💾 Sauvegarde pré-rollback: $current_backup"
    echo ""
    info "🔍 Vérifiez l'état avec: ./status_redressement_architectural.sh"
    
    return 0
}

# Fonction pour rollback partiel (seulement local)
local_rollback() {
    log "🔄 ROLLBACK LOCAL SEULEMENT"
    echo "============================"
    
    if ! find_backups; then
        error "Aucune sauvegarde disponible pour rollback local"
        exit 1
    fi
    
    echo ""
    read -p "Entrez le chemin de la sauvegarde à restaurer: " backup_choice
    
    if restore_from_backup "$backup_choice"; then
        success "✅ Rollback local terminé"
        info "📝 Log: $RESTORE_LOG"
    else
        error "❌ Rollback local échoué"
        exit 1
    fi
}

# Fonction pour rollback GitHub seulement
github_rollback() {
    log "🔄 ROLLBACK GITHUB SEULEMENT"
    echo "============================="
    
    rollback_github_renaming
    
    info "📝 Log: $RESTORE_LOG"
}

# Afficher l'aide
show_help() {
    echo "🔄 Rollback Redressement Architectural Panini"
    echo "=============================================="
    echo ""
    echo "Usage: $0 [option]"
    echo ""
    echo "Options:"
    echo "  --full, -f       Rollback complet (local + GitHub)"
    echo "  --local, -l      Rollback local seulement"
    echo "  --github, -g     Rollback GitHub seulement"
    echo "  --list, -ls      Lister les sauvegardes disponibles"
    echo "  --help, -h       Afficher cette aide"
    echo ""
    echo "Sans option: Mode interactif"
    echo ""
    echo "⚠️  Important:"
    echo "   - Le rollback GitHub nécessite GitHub CLI authentifié"
    echo "   - Une sauvegarde de l'état actuel est créée avant rollback"
    echo "   - Les logs de rollback sont conservés"
    echo ""
}

# Menu interactif
interactive_menu() {
    echo "🔄 MENU ROLLBACK INTERACTIF"
    echo "============================"
    echo ""
    echo "1. 🔍 Lister les sauvegardes disponibles"
    echo "2. 🔄 Rollback complet (local + GitHub)"
    echo "3. 💾 Rollback local seulement"
    echo "4. 🌐 Rollback GitHub seulement"
    echo "5. ❌ Annuler"
    echo ""
    
    read -p "Choisissez une option (1-5): " choice
    
    case $choice in
        1)
            find_backups
            ;;
        2)
            full_rollback
            ;;
        3)
            local_rollback
            ;;
        4)
            github_rollback
            ;;
        5)
            log "Rollback annulé"
            exit 0
            ;;
        *)
            error "Option invalide"
            exit 1
            ;;
    esac
}

# Fonction principale
main() {
    cd /home/stephane/GitHub/Panini 2>/dev/null || {
        error "Impossible d'accéder au directory Panini"
        exit 1
    }
    
    case "${1:-}" in
        --help|-h)
            show_help
            ;;
        --full|-f)
            full_rollback
            ;;
        --local|-l)
            local_rollback
            ;;
        --github|-g)
            github_rollback
            ;;
        --list|-ls)
            find_backups
            ;;
        *)
            interactive_menu
            ;;
    esac
}

# Point d'entrée
main "$@"