#!/bin/bash
# Script automatique de renommage repositories GitHub - REDRESSEMENT PANINI
# ATTENTION : Vérifiez les permissions GitHub avant exécution
# Utilise GitHub CLI (gh) pour les renommages

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[RENAME]${NC} $1"
}

success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifications préliminaires
check_prerequisites() {
    log "Vérification des prérequis..."
    
    # Vérifier GitHub CLI
    if ! command -v gh &> /dev/null; then
        error "GitHub CLI (gh) non installé. Installez-le avec: sudo apt install gh"
        exit 1
    fi
    
    # Vérifier authentification GitHub
    if ! gh auth status &> /dev/null; then
        error "GitHub CLI non authentifié. Exécutez: gh auth login"
        exit 1
    fi
    
    success "Prérequis OK"
}

# Fonction de renommage sécurisée
rename_repository() {
    local current_name="$1"
    local target_name="$2"
    local local_path="/home/stephane/GitHub/$current_name"
    
    log "🔄 Renommage $current_name → $target_name"
    
    # Vérifier que le repository local existe
    if [ ! -d "$local_path" ]; then
        warning "Repository local $current_name introuvable, passage au suivant"
        return 0
    fi
    
    # Vérifier que c'est un repository git
    if [ ! -d "$local_path/.git" ]; then
        warning "$current_name n'est pas un repository git, passage au suivant"
        return 0
    fi
    
    cd "$local_path"
    
    # Vérifier l'état git propre
    if ! git diff --quiet || ! git diff --cached --quiet; then
        warning "Repository $current_name a des modifications non commitées"
        read -p "Continuer quand même ? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log "Passage au repository suivant"
            return 0
        fi
    fi
    
    # Renommage GitHub via CLI
    log "Renommage GitHub: $current_name → $target_name"
    if gh repo rename "$target_name" --repo "stephanedenis/$current_name"; then
        success "Repository GitHub renommé avec succès"
    else
        error "Échec du renommage GitHub pour $current_name"
        return 1
    fi
    
    # Mise à jour URL remote locale
    log "Mise à jour URL remote locale"
    local new_url="git@github.com:stephanedenis/$target_name.git"
    git remote set-url origin "$new_url"
    
    # Vérifier la nouvelle URL
    if git remote -v | grep -q "$target_name"; then
        success "URL remote mise à jour"
    else
        error "Échec mise à jour URL remote"
        return 1
    fi
    
    # Renommage du dossier local
    cd ..
    log "Renommage dossier local: $current_name → $target_name"
    if mv "$current_name" "$target_name"; then
        success "Dossier local renommé"
    else
        error "Échec renommage dossier local"
        return 1
    fi
    
    success "✅ $current_name → $target_name : TERMINÉ"
    return 0
}

# Sauvegarde préventive
create_backup() {
    local backup_dir="/home/stephane/GitHub/BACKUP_REDRESSEMENT_$(date +%Y%m%d_%H%M%S)"
    log "Création sauvegarde préventive: $backup_dir"
    
    mkdir -p "$backup_dir"
    
    # Lister tous les repos Panini pour sauvegarde
    local repos_to_backup=(
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
    
    for repo in "${repos_to_backup[@]}"; do
        if [ -d "/home/stephane/GitHub/$repo" ]; then
            log "Sauvegarde $repo..."
            cp -r "/home/stephane/GitHub/$repo" "$backup_dir/"
        fi
    done
    
    success "Sauvegarde créée: $backup_dir"
    echo "$backup_dir" > "/tmp/panini_backup_location.txt"
}

# Fonction principale
main() {
    echo "🔄 DÉBUT RENOMMAGE REPOSITORIES GITHUB - REDRESSEMENT PANINI"
    echo "=============================================================="
    echo "Objectif: PaniniFS-* → Panini-* pour cohérence architecturale"
    echo ""
    
    check_prerequisites
    
    # Demander confirmation
    warning "ATTENTION: Cette opération va renommer tous les repositories PaniniFS-*"
    warning "Assurez-vous d'avoir des sauvegardes et que personne d'autre ne travaille dessus"
    read -p "Continuer avec le renommage ? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log "Opération annulée par l'utilisateur"
        exit 0
    fi
    
    # Créer sauvegarde
    create_backup
    
    # Renommages selon le plan
    declare -A RENAME_MAP=(
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
    
    local success_count=0
    local total_count=${#RENAME_MAP[@]}
    
    for current_name in "${!RENAME_MAP[@]}"; do
        target_name="${RENAME_MAP[$current_name]}"
        
        if rename_repository "$current_name" "$target_name"; then
            ((success_count++))
        else
            error "Échec pour $current_name"
        fi
        
        echo ""
    done
    
    echo "📊 RÉSULTATS FINAUX"
    echo "==================="
    echo "✅ Succès: $success_count/$total_count repositories"
    
    if [ $success_count -eq $total_count ]; then
        success "🎉 TOUS LES RENOMMAGES RÉUSSIS !"
        echo ""
        echo "📋 ÉTAPES SUIVANTES:"
        echo "1. Vérifier que tous les repositories sont accessibles sur GitHub"
        echo "2. Mettre à jour les liens dans la documentation"
        echo "3. Configurer les submodules dans le repository Panini parent"
        echo "4. Informer les collaborateurs des changements"
    else
        warning "⚠️  Certains renommages ont échoué"
        echo "📋 Actions requises:"
        echo "1. Vérifier les logs d'erreur ci-dessus"
        echo "2. Renommer manuellement les repositories échoués"
        echo "3. Vérifier les permissions GitHub"
    fi
    
    if [ -f "/tmp/panini_backup_location.txt" ]; then
        local backup_location=$(cat "/tmp/panini_backup_location.txt")
        echo ""
        echo "💾 Sauvegarde disponible: $backup_location"
        echo "   (Supprimez après validation complète)"
    fi
}

# Point d'entrée
main "$@"