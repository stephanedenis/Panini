#!/bin/bash
# Script principal de redressement architectural Panini
# Guide interactif pour l'exécution complète du redressement

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[REDRESS]${NC} $1"
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

# Fonction pour afficher l'en-tête
show_header() {
    clear
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║           🏗️  REDRESSEMENT ARCHITECTURAL PANINI  🏗️           ║"
    echo "╠════════════════════════════════════════════════════════════════╣"
    echo "║  Objectif: Panini parent principal + modules Panini-*         ║"
    echo "║  Durée totale estimée: 6-10 heures                            ║"
    echo "║  Niveau: MAJEUR - Restructuration complète                    ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
}

# Vérification des prérequis
check_prerequisites() {
    log "Vérification des prérequis..."
    local all_ok=true
    
    # GitHub CLI
    if command -v gh &> /dev/null; then
        if gh auth status &> /dev/null; then
            success "GitHub CLI authentifié"
        else
            error "GitHub CLI non authentifié - Exécutez: gh auth login"
            all_ok=false
        fi
    else
        error "GitHub CLI non installé - Installez avec: sudo apt install gh"
        all_ok=false
    fi
    
    # Git
    if command -v git &> /dev/null; then
        success "Git disponible"
    else
        error "Git non installé"
        all_ok=false
    fi
    
    # Python
    if command -v python3 &> /dev/null; then
        success "Python 3 disponible"
    else
        error "Python 3 non installé"
        all_ok=false
    fi
    
    # Repository Panini
    if [ -d "/home/stephane/GitHub/Panini" ]; then
        success "Repository Panini trouvé"
    else
        error "Repository Panini introuvable"
        all_ok=false
    fi
    
    if [ "$all_ok" = false ]; then
        echo ""
        error "Prérequis manquants - Corrigez les problèmes ci-dessus avant de continuer"
        exit 1
    fi
    
    success "Tous les prérequis sont satisfaits"
}

# Affichage du plan d'action
show_action_plan() {
    echo ""
    info "📋 PLAN D'ACTION COMPLET"
    echo "========================"
    echo ""
    echo "Phase 1️⃣  Préparation et planification      (30 min, Risque: Faible)"
    echo "Phase 2️⃣  Renommage repositories GitHub     (2-3h, Risque: Moyen)"
    echo "Phase 3️⃣  Restructuration Panini parent     (3-4h, Risque: Moyen-Élevé)"
    echo "Phase 4️⃣  Validation et finalisation        (1-2h, Risque: Faible)"
    echo ""
    echo "🎯 Résultat attendu:"
    echo "   ✅ Panini = Parent principal unique"
    echo "   ✅ Tous PaniniFS-* → Panini-* (nomenclature cohérente)"
    echo "   ✅ Structure modulaire organisée"
    echo "   ✅ Submodules fonctionnels"
    echo ""
}

# Phase 1: Préparation
execute_phase1() {
    echo ""
    log "🚀 PHASE 1: PRÉPARATION ET PLANIFICATION"
    echo "========================================="
    
    cd /home/stephane/GitHub/Panini
    
    warning "Cette phase génère le plan détaillé de redressement"
    read -p "Continuer avec la Phase 1 ? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log "Phase 1 sautée par l'utilisateur"
        return 1
    fi
    
    log "Génération du plan de redressement..."
    python3 plan_redressement_architectural.py
    
    if [ $? -eq 0 ]; then
        success "✅ Phase 1 terminée avec succès"
        echo ""
        info "📄 Fichiers générés:"
        echo "   - redressement_architectural_plan_*.json"
        echo "   - PLAN_REDRESSEMENT_ARCHITECTURAL_*.md"
        echo ""
        info "👀 Consultez ces fichiers pour valider le plan avant de continuer"
        return 0
    else
        error "❌ Phase 1 échouée"
        return 1
    fi
}

# Phase 2: Renommage
execute_phase2() {
    echo ""
    log "🔄 PHASE 2: RENOMMAGE REPOSITORIES GITHUB"
    echo "=========================================="
    
    warning "⚠️  PHASE CRITIQUE - Cette phase renomme tous les repositories GitHub"
    warning "    Tous les repositories PaniniFS-* seront renommés en Panini-*"
    warning "    PaniniFS sera renommé en Panini-FS"
    echo ""
    warning "🛡️  Sécurités activées:"
    echo "   ✅ Sauvegarde automatique avant modifications"
    echo "   ✅ Vérification état Git avant chaque renommage"
    echo "   ✅ Confirmation utilisateur pour chaque étape"
    echo ""
    
    read -p "Continuer avec la Phase 2 ? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log "Phase 2 sautée par l'utilisateur"
        return 1
    fi
    
    log "Exécution du renommage GitHub..."
    ./renommage_github_redressement.sh
    
    if [ $? -eq 0 ]; then
        success "✅ Phase 2 terminée avec succès"
        return 0
    else
        error "❌ Phase 2 échouée"
        return 1
    fi
}

# Phase 3: Restructuration
execute_phase3() {
    echo ""
    log "🏗️ PHASE 3: RESTRUCTURATION PANINI PARENT"
    echo "=========================================="
    
    warning "Cette phase restructure complètement le repository Panini"
    echo ""
    info "Actions qui seront effectuées:"
    echo "   🔧 Création structure modulaire (modules/, shared/, projects/)"
    echo "   🧹 Nettoyage anciens submodules"
    echo "   🔗 Configuration nouveaux submodules organisés"
    echo "   📚 Consolidation contenu recherche"
    echo "   📝 Mise à jour documentation"
    echo "   💾 Commit de restructuration"
    echo ""
    
    read -p "Continuer avec la Phase 3 ? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log "Phase 3 sautée par l'utilisateur"
        return 1
    fi
    
    log "Exécution de la restructuration..."
    ./restructuration_panini_parent.sh
    
    if [ $? -eq 0 ]; then
        success "✅ Phase 3 terminée avec succès"
        return 0
    else
        error "❌ Phase 3 échouée"
        return 1
    fi
}

# Phase 4: Validation
execute_phase4() {
    echo ""
    log "✅ PHASE 4: VALIDATION ET FINALISATION"
    echo "======================================"
    
    info "Cette phase valide que tout fonctionne correctement"
    echo ""
    
    read -p "Continuer avec la Phase 4 ? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log "Phase 4 sautée par l'utilisateur"
        return 1
    fi
    
    log "Validation complète..."
    ./validate_redressement_architectural.sh
    
    local validation_result=$?
    
    if [ $validation_result -eq 0 ]; then
        success "✅ Phase 4 terminée avec succès"
        
        # Push automatique si validation OK
        log "Push de la restructuration vers GitHub..."
        cd /home/stephane/GitHub/Panini
        git push origin main
        
        if [ $? -eq 0 ]; then
            success "✅ Restructuration poussée vers GitHub"
        else
            warning "⚠️ Échec du push - Vérifiez manuellement"
        fi
        
        return 0
    else
        warning "⚠️ Phase 4 avec erreurs ($validation_result problèmes détectés)"
        return $validation_result
    fi
}

# Résumé final
show_final_summary() {
    echo ""
    echo "🎉 REDRESSEMENT ARCHITECTURAL PANINI TERMINÉ !"
    echo "=============================================="
    echo ""
    success "✅ Architecture cohérente avec Panini comme parent principal"
    success "✅ Nomenclature uniforme Panini-* adoptée"
    success "✅ Structure modulaire organisée et fonctionnelle"
    success "✅ Documentation mise à jour"
    echo ""
    info "🎯 PROCHAINES ÉTAPES RECOMMANDÉES:"
    echo "   1. Tester la navigation dans les modules"
    echo "   2. Informer les collaborateurs des changements"
    echo "   3. Mettre à jour les liens externes"
    echo "   4. Valider le fonctionnement complet"
    echo ""
    info "📚 Navigation exemple:"
    echo "   cd modules/core/filesystem    # → Panini-FS"
    echo "   cd modules/services/colab     # → Panini-CoLabController"
    echo "   cd projects/gest              # → Panini-Gest"
    echo ""
    success "🌟 L'écosystème Panini est maintenant cohérent et prêt !"
}

# Menu interactif
show_interactive_menu() {
    while true; do
        echo ""
        echo "🎛️  MENU INTERACTIF"
        echo "=================="
        echo "1. 📋 Afficher le guide complet"
        echo "2. 🔍 Vérifier les prérequis"
        echo "3. 🚀 Exécuter toutes les phases automatiquement"
        echo "4. 1️⃣  Exécuter Phase 1 (Préparation)"
        echo "5. 2️⃣  Exécuter Phase 2 (Renommage GitHub)"
        echo "6. 3️⃣  Exécuter Phase 3 (Restructuration)"
        echo "7. 4️⃣  Exécuter Phase 4 (Validation)"
        echo "8. 🆘 Aide et documentation"
        echo "9. 🚪 Quitter"
        echo ""
        read -p "Choisissez une option (1-9): " choice
        
        case $choice in
            1)
                less GUIDE_REDRESSEMENT_ARCHITECTURAL.md
                ;;
            2)
                check_prerequisites
                ;;
            3)
                log "Exécution complète automatique..."
                execute_phase1 && execute_phase2 && execute_phase3 && execute_phase4
                if [ $? -eq 0 ]; then
                    show_final_summary
                    break
                fi
                ;;
            4)
                execute_phase1
                ;;
            5)
                execute_phase2
                ;;
            6)
                execute_phase3
                ;;
            7)
                execute_phase4
                ;;
            8)
                echo ""
                info "📚 Documentation disponible:"
                echo "   - GUIDE_REDRESSEMENT_ARCHITECTURAL.md (guide complet)"
                echo "   - PLAN_REDRESSEMENT_ARCHITECTURAL_*.md (plan détaillé)"
                echo "   - Scripts individuels avec option --help"
                echo ""
                info "🆘 En cas de problème:"
                echo "   - Consultez les logs d'erreur détaillés"
                echo "   - Utilisez les sauvegardes automatiques créées"
                echo "   - Exécutez les phases individuellement"
                ;;
            9)
                log "Au revoir !"
                exit 0
                ;;
            *)
                warning "Option invalide. Choisissez entre 1 et 9."
                ;;
        esac
    done
}

# Fonction principale
main() {
    show_header
    
    # Mode automatique si argument fourni
    if [ "$1" = "--auto" ]; then
        log "Mode automatique activé"
        check_prerequisites
        show_action_plan
        
        warning "Mode automatique - Toutes les phases seront exécutées"
        read -p "Continuer ? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            execute_phase1 && execute_phase2 && execute_phase3 && execute_phase4
            if [ $? -eq 0 ]; then
                show_final_summary
            fi
        fi
    else
        # Mode interactif
        check_prerequisites
        show_action_plan
        show_interactive_menu
    fi
}

# Point d'entrée
main "$@"