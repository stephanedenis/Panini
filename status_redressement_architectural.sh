#!/bin/bash
# Script de statut du redressement architectural Panini
# Affiche l'état actuel et les prochaines étapes

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Fonctions d'affichage
completed() {
    echo -e "${GREEN}[✓ TERMINÉ]${NC} $1"
}

pending() {
    echo -e "${YELLOW}[⏳ EN ATTENTE]${NC} $1"
}

error() {
    echo -e "${RED}[✗ PROBLÈME]${NC} $1"
}

info() {
    echo -e "${CYAN}[ℹ INFO]${NC} $1"
}

progress() {
    echo -e "${PURPLE}[🔄 EN COURS]${NC} $1"
}

unknown() {
    echo -e "${BLUE}[? INDÉTERMINÉ]${NC} $1"
}

# Fonction pour vérifier l'état des phases
check_phase_status() {
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║               📊 STATUT REDRESSEMENT PANINI                   ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    
    # Phase 1: Préparation
    echo "Phase 1️⃣  - Préparation et Planification"
    echo "─────────────────────────────────────────"
    
    # Vérifier les fichiers de plan générés
    local plan_files=$(find . -name "redressement_architectural_plan_*.json" 2>/dev/null | wc -l)
    local md_plan_files=$(find . -name "PLAN_REDRESSEMENT_ARCHITECTURAL_*.md" 2>/dev/null | wc -l)
    
    if [ "$plan_files" -gt 0 ] && [ "$md_plan_files" -gt 0 ]; then
        completed "Plans de redressement générés ($plan_files JSON, $md_plan_files MD)"
        local phase1_status="completed"
    else
        pending "Plans de redressement non générés"
        local phase1_status="pending"
    fi
    
    # Vérifier scripts disponibles
    local scripts=("plan_redressement_architectural.py" "renommage_github_redressement.sh" "restructuration_panini_parent.sh" "validate_redressement_architectural.sh")
    local scripts_ready=0
    for script in "${scripts[@]}"; do
        if [ -f "$script" ] && [ -x "$script" ]; then
            scripts_ready=$((scripts_ready + 1))
        fi
    done
    
    if [ "$scripts_ready" -eq ${#scripts[@]} ]; then
        completed "Scripts d'automatisation prêts ($scripts_ready/${#scripts[@]})"
    else
        error "Scripts manquants ou non exécutables ($scripts_ready/${#scripts[@]})"
    fi
    
    echo ""
    
    # Phase 2: Renommage GitHub
    echo "Phase 2️⃣  - Renommage Repositories GitHub"
    echo "─────────────────────────────────────────"
    
    # Vérifier si GitHub CLI est configuré
    if command -v gh &> /dev/null && gh auth status &> /dev/null 2>&1; then
        completed "GitHub CLI authentifié et prêt"
    else
        error "GitHub CLI non configuré ou non authentifié"
    fi
    
    # Vérifier la présence des repositories à renommer
    info "Vérification des repositories GitHub..."
    
    # Estimation du statut de renommage basée sur les noms actuels
    local repos_to_rename=("PaniniFS" "PaniniFS-Research" "PaniniFS-CopilotageShared" "PaniniFS-CoLabController" "PaniniFS-Tools" "PaniniFS-SecuredPrivate")
    local renamed_detected=0
    
    # Simple heuristique: si plan existe, supposer que la vérification a été faite
    if [ "$phase1_status" = "completed" ]; then
        pending "Renommage GitHub en attente d'exécution"
        info "Repos à traiter: ${#repos_to_rename[@]} repositories PaniniFS*"
    else
        unknown "État du renommage indéterminable (Phase 1 requise)"
    fi
    
    echo ""
    
    # Phase 3: Restructuration
    echo "Phase 3️⃣  - Restructuration Panini Parent"
    echo "─────────────────────────────────────────"
    
    # Vérifier structure actuelle
    if [ -d "modules" ] && [ -d "shared" ] && [ -d "projects" ]; then
        completed "Structure modulaire détectée"
        local structure_status="completed"
    elif [ -d "modules" ] || [ -d "shared" ] || [ -d "projects" ]; then
        progress "Structure modulaire partiellement créée"
        local structure_status="partial"
    else
        pending "Structure modulaire non créée"
        local structure_status="pending"
    fi
    
    # Vérifier submodules actuels
    if [ -f ".gitmodules" ]; then
        local submodule_count=$(grep -c '\[submodule' .gitmodules 2>/dev/null || echo 0)
        info "Submodules configurés: $submodule_count"
        
        if [ "$submodule_count" -gt 0 ]; then
            info "État des submodules:"
            git submodule status 2>/dev/null | head -5 || echo "   Erreur lecture submodules"
        fi
    else
        pending "Aucun fichier .gitmodules trouvé"
    fi
    
    echo ""
    
    # Phase 4: Validation
    echo "Phase 4️⃣  - Validation et Finalisation"
    echo "─────────────────────────────────────────"
    
    # Vérifier si validation script est disponible
    if [ -x "validate_redressement_architectural.sh" ]; then
        info "Script de validation disponible"
        
        # Essayer de détecter si validation a été exécutée
        if [ -f "validation_redressement_*.log" ] || [ -f "VALIDATION_REPORT_*.md" ]; then
            completed "Rapports de validation détectés"
        else
            pending "Validation non exécutée"
        fi
    else
        error "Script de validation manquant"
    fi
    
    echo ""
}

# Fonction pour afficher l'état des repositories
show_repository_status() {
    echo "📁 ÉTAT DES REPOSITORIES"
    echo "========================"
    echo ""
    
    # Repository principal
    info "Repository principal: $(basename $(pwd))"
    
    # État Git local
    if git status --porcelain | grep -q .; then
        error "Modifications non commitées détectées"
        git status --short | head -10
    else
        completed "Working directory propre"
    fi
    
    # Branches
    local current_branch=$(git branch --show-current)
    info "Branche courante: $current_branch"
    
    # Derniers commits
    info "Derniers commits:"
    git log --oneline -3 | sed 's/^/   /'
    
    echo ""
    
    # Submodules si existants
    if [ -f ".gitmodules" ]; then
        info "Submodules configurés:"
        git config --file .gitmodules --get-regexp '^submodule\..*\.path$' | while read key value; do
            echo "   📂 $value"
        done
    fi
    
    echo ""
}

# Fonction pour afficher les recommandations
show_recommendations() {
    echo "💡 RECOMMANDATIONS PROCHAINES ÉTAPES"
    echo "===================================="
    echo ""
    
    # Détecter quelle phase exécuter ensuite
    local plan_files=$(find . -name "redressement_architectural_plan_*.json" 2>/dev/null | wc -l)
    
    if [ "$plan_files" -eq 0 ]; then
        echo "🎯 Action recommandée: Exécuter Phase 1"
        echo "   ./redressement_architectural_panini.sh"
        echo "   ou seulement: python3 plan_redressement_architectural.py"
        echo ""
        echo "   Cette phase analyse la situation actuelle et génère un plan détaillé."
    else
        echo "🎯 Action recommandée: Continuer selon le plan généré"
        echo "   ./redressement_architectural_panini.sh"
        echo ""
        echo "   ou phases individuelles:"
        echo "   Phase 2: ./renommage_github_redressement.sh"
        echo "   Phase 3: ./restructuration_panini_parent.sh"
        echo "   Phase 4: ./validate_redressement_architectural.sh"
    fi
    
    echo ""
    echo "📚 Documentation disponible:"
    echo "   - GUIDE_REDRESSEMENT_ARCHITECTURAL.md (guide complet)"
    if [ "$plan_files" -gt 0 ]; then
        echo "   - PLAN_REDRESSEMENT_ARCHITECTURAL_*.md (plan spécifique)"
    fi
    echo ""
    
    echo "⚠️  Recommandations importantes:"
    echo "   ✅ Sauvegardez vos modifications avant de continuer"
    echo "   ✅ Assurez-vous que GitHub CLI est authentifié"
    echo "   ✅ Vérifiez que tous les repositories sont propres"
    echo "   ✅ Informez les collaborateurs avant le renommage"
    echo ""
}

# Fonction pour l'aide
show_help() {
    echo "📖 AIDE - Statut Redressement Architectural"
    echo "==========================================="
    echo ""
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --quick, -q    Affichage rapide (statut des phases seulement)"
    echo "  --repos, -r    État des repositories seulement"
    echo "  --help, -h     Afficher cette aide"
    echo ""
    echo "Le script affiche par défaut:"
    echo "  📊 Statut de chaque phase du redressement"
    echo "  📁 État des repositories locaux"
    echo "  💡 Recommandations pour les prochaines étapes"
    echo ""
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
            exit 0
            ;;
        --quick|-q)
            check_phase_status
            ;;
        --repos|-r)
            show_repository_status
            ;;
        *)
            check_phase_status
            echo ""
            show_repository_status
            echo ""
            show_recommendations
            ;;
    esac
}

# Point d'entrée
main "$@"