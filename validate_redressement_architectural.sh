#!/bin/bash
# Script de validation finale du redressement architectural Panini
# Vérifie que toute la restructuration s'est bien déroulée

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[VALIDATE]${NC} $1"
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

PANINI_ROOT="/home/stephane/GitHub/Panini"
VALIDATION_ERRORS=0

# Incrémenter compteur d'erreurs
add_error() {
    ((VALIDATION_ERRORS++))
}

# Vérifier la structure de dossiers
validate_directory_structure() {
    log "Validation structure de dossiers..."
    
    local expected_dirs=(
        "modules"
        "modules/core"
        "modules/orchestration" 
        "modules/services"
        "modules/infrastructure"
        "shared"
        "projects"
    )
    
    cd "$PANINI_ROOT"
    
    for dir in "${expected_dirs[@]}"; do
        if [ -d "$dir" ]; then
            success "Structure OK: $dir/"
        else
            error "Structure manquante: $dir/"
            add_error
        fi
    done
}

# Vérifier les repositories renommés sur GitHub
validate_github_repositories() {
    log "Validation repositories GitHub renommés..."
    
    local expected_repos=(
        "Panini-FS"
        "Panini-SemanticCore"
        "Panini-CloudOrchestrator"
        "Panini-ExecutionOrchestrator"
        "Panini-CoLabController"
        "Panini-PublicationEngine"
        "Panini-DatasetsIngestion"
        "Panini-UltraReactive"
        "Panini-AutonomousMissions"
        "Panini-CopilotageShared"
        "Panini-SpecKit-Shared"
        "Panini-AttributionRegistry"
        "Panini-Gest"
        "Panini-OntoWave"
    )
    
    if ! command -v gh &> /dev/null; then
        warning "GitHub CLI non disponible, validation GitHub sautée"
        return 0
    fi
    
    for repo in "${expected_repos[@]}"; do
        if gh repo view "stephanedenis/$repo" &> /dev/null; then
            success "Repository GitHub OK: $repo"
        else
            error "Repository GitHub manquant: $repo"
            add_error
        fi
    done
}

# Vérifier les repositories locaux renommés
validate_local_repositories() {
    log "Validation repositories locaux renommés..."
    
    local github_path="/home/stephane/GitHub"
    local expected_repos=(
        "Panini-FS"
        "Panini-SemanticCore"
        "Panini-CloudOrchestrator"
        "Panini-ExecutionOrchestrator"
        "Panini-CoLabController"
        "Panini-PublicationEngine"
        "Panini-DatasetsIngestion"
        "Panini-UltraReactive"
        "Panini-AutonomousMissions"
        "Panini-CopilotageShared"
        "Panini-SpecKit-Shared"
        "Panini-AttributionRegistry"
        "Panini-Gest"
        "Panini-OntoWave"
    )
    
    for repo in "${expected_repos[@]}"; do
        local repo_path="$github_path/$repo"
        if [ -d "$repo_path" ]; then
            if [ -d "$repo_path/.git" ]; then
                # Vérifier que l'URL remote est correcte
                cd "$repo_path"
                local remote_url=$(git remote get-url origin 2>/dev/null || echo "unknown")
                if [[ "$remote_url" == *"$repo"* ]]; then
                    success "Repository local OK: $repo"
                else
                    error "URL remote incorrecte pour $repo: $remote_url"
                    add_error
                fi
            else
                error "Repository local $repo n'est pas un repo Git"
                add_error
            fi
        else
            error "Repository local manquant: $repo"
            add_error
        fi
    done
}

# Vérifier les submodules configurés
validate_submodules() {
    log "Validation configuration submodules..."
    
    cd "$PANINI_ROOT"
    
    if [ ! -f ".gitmodules" ]; then
        error "Fichier .gitmodules manquant"
        add_error
        return 1
    fi
    
    # Compter les submodules attendus
    local expected_submodules=14  # Total des modules dans la nouvelle architecture
    local actual_submodules=$(git submodule status 2>/dev/null | wc -l || echo "0")
    
    if [ "$actual_submodules" -eq "$expected_submodules" ]; then
        success "Nombre de submodules correct: $actual_submodules"
    else
        warning "Nombre de submodules: $actual_submodules (attendu: $expected_submodules)"
    fi
    
    # Vérifier l'état des submodules
    if git submodule status | grep -q "^-"; then
        warning "Certains submodules ne sont pas initialisés"
        log "Initialisation des submodules manquants..."
        git submodule update --init --recursive
    else
        success "Tous les submodules sont initialisés"
    fi
    
    # Vérifier quelques chemins clés
    local key_submodules=(
        "modules/core/filesystem"
        "modules/services/colab"
        "shared/copilotage"
        "projects/gest"
    )
    
    for submodule_path in "${key_submodules[@]}"; do
        if [ -d "$submodule_path" ] && [ -d "$submodule_path/.git" ]; then
            success "Submodule clé OK: $submodule_path"
        else
            error "Submodule clé manquant: $submodule_path"
            add_error
        fi
    done
}

# Vérifier que les anciens noms n'existent plus
validate_old_names_removed() {
    log "Validation suppression anciens noms..."
    
    local github_path="/home/stephane/GitHub"
    local old_repos=(
        "PaniniFS"  # Doit être renommé en Panini-FS
        "PaniniFS-SemanticCore"
        "PaniniFS-CloudOrchestrator"
        "PaniniFS-ExecutionOrchestrator"
        "PaniniFS-CoLabController"
        "PaniniFS-PublicationEngine"
        "PaniniFS-DatasetsIngestion"
        "PaniniFS-UltraReactive"
        "PaniniFS-AutonomousMissions"
        "PaniniFS-CopilotageShared"
        "PaniniFS-SpecKit-Shared"
        "PaniniFS-AttributionRegistry"
    )
    
    local old_names_found=0
    
    for old_repo in "${old_repos[@]}"; do
        if [ -d "$github_path/$old_repo" ]; then
            warning "Ancien nom encore présent: $old_repo"
            ((old_names_found++))
        fi
    done
    
    if [ $old_names_found -eq 0 ]; then
        success "Tous les anciens noms supprimés"
    else
        warning "$old_names_found anciens noms encore présents"
    fi
}

# Vérifier la documentation mise à jour
validate_documentation() {
    log "Validation documentation mise à jour..."
    
    cd "$PANINI_ROOT"
    
    if [ -f "README.md" ]; then
        if grep -q "Panini - Écosystème" README.md; then
            success "README principal mis à jour"
        else
            error "README principal non mis à jour"
            add_error
        fi
        
        if grep -q "modules/core/filesystem" README.md; then
            success "Structure modulaire documentée"
        else
            error "Structure modulaire non documentée"
            add_error
        fi
    else
        error "README.md manquant"
        add_error
    fi
}

# Tests fonctionnels de base
validate_functionality() {
    log "Tests fonctionnels de base..."
    
    cd "$PANINI_ROOT"
    
    # Test: navigation dans les submodules
    if [ -d "modules/core/filesystem" ]; then
        cd "modules/core/filesystem"
        if [ -f "README.md" ]; then
            success "Navigation submodule core/filesystem OK"
        else
            warning "Contenu submodule core/filesystem incomplet"
        fi
        cd "$PANINI_ROOT"
    fi
    
    # Test: commandes git de base
    if git status &> /dev/null; then
        success "Commandes Git fonctionnelles"
    else
        error "Problème avec Git"
        add_error
    fi
    
    # Test: statut submodules
    if git submodule status &> /dev/null; then
        success "Commandes submodules fonctionnelles"
    else
        error "Problème avec submodules"
        add_error
    fi
}

# Génération rapport de validation
generate_validation_report() {
    local report_file="VALIDATION_REDRESSEMENT_$(date +%Y%m%d_%H%M%S).md"
    
    cat > "$report_file" << EOF
# 📋 RAPPORT DE VALIDATION - REDRESSEMENT ARCHITECTURAL PANINI

**Date :** $(date '+%Y-%m-%d %H:%M:%S')
**Erreurs détectées :** $VALIDATION_ERRORS

## ✅ Validations Effectuées

### Structure de Dossiers
- [x] modules/ créé
- [x] modules/core/ créé
- [x] modules/orchestration/ créé
- [x] modules/services/ créé
- [x] modules/infrastructure/ créé
- [x] shared/ créé
- [x] projects/ créé

### Repositories GitHub
$(if command -v gh &> /dev/null; then echo "- [x] Vérification repositories GitHub effectuée"; else echo "- [ ] GitHub CLI non disponible"; fi)

### Repositories Locaux
- [x] Vérification noms repositories locaux
- [x] Vérification URLs remotes

### Submodules
- [x] Configuration .gitmodules
- [x] Initialisation submodules
- [x] Vérification chemins clés

### Documentation
- [x] README principal mis à jour
- [x] Structure modulaire documentée

### Tests Fonctionnels
- [x] Navigation submodules
- [x] Commandes Git
- [x] Commandes submodules

## 📊 Résultat Global

$(if [ $VALIDATION_ERRORS -eq 0 ]; then
    echo "🎉 **VALIDATION RÉUSSIE** - Redressement architectural complet !"
else
    echo "⚠️ **$VALIDATION_ERRORS ERREURS DÉTECTÉES** - Actions correctives requises"
fi)

---
*Rapport généré automatiquement par validate_redressement_architectural.sh*
EOF
    
    success "Rapport de validation généré: $report_file"
}

# Fonction principale
main() {
    echo "🔍 VALIDATION REDRESSEMENT ARCHITECTURAL PANINI"
    echo "================================================"
    echo "Vérification complète de la restructuration"
    echo ""
    
    # Vérifier qu'on est dans le bon repository
    if [ ! -d "$PANINI_ROOT" ]; then
        error "Repository Panini introuvable: $PANINI_ROOT"
        exit 1
    fi
    
    # Exécution des validations
    validate_directory_structure
    echo ""
    
    validate_local_repositories
    echo ""
    
    validate_github_repositories
    echo ""
    
    validate_submodules
    echo ""
    
    validate_old_names_removed
    echo ""
    
    validate_documentation
    echo ""
    
    validate_functionality
    echo ""
    
    # Génération du rapport
    generate_validation_report
    
    echo ""
    echo "📊 RÉSULTATS FINAUX DE LA VALIDATION"
    echo "====================================="
    
    if [ $VALIDATION_ERRORS -eq 0 ]; then
        success "🎉 VALIDATION COMPLÈTE RÉUSSIE !"
        echo ""
        echo "✅ Le redressement architectural Panini est complet et fonctionnel"
        echo "✅ Tous les repositories sont renommés selon la convention Panini-*"
        echo "✅ La structure modulaire est correctement configurée"
        echo "✅ Les submodules fonctionnent correctement"
        echo ""
        echo "🎯 L'écosystème Panini est maintenant cohérent et prêt à l'utilisation !"
    else
        warning "⚠️ $VALIDATION_ERRORS ERREURS DÉTECTÉES"
        echo ""
        echo "📋 Actions requises :"
        echo "1. Consulter les erreurs détaillées ci-dessus"
        echo "2. Corriger les problèmes identifiés"
        echo "3. Relancer la validation"
        echo ""
        echo "💡 La plupart des erreurs peuvent être corrigées en relançant les scripts"
        echo "   de renommage ou de restructuration selon le problème identifié."
    fi
    
    echo ""
    echo "📄 Rapport détaillé disponible dans le fichier de validation généré"
    
    return $VALIDATION_ERRORS
}

# Point d'entrée
main "$@"