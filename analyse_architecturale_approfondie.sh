#!/bin/bash
# Script d'analyse architecturale approfondie de l'écosystème Panini
# Objectif: Comprendre les duplications et incohérences

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[ANALYSE]${NC} $1"
}

section() {
    echo -e "${PURPLE}[SECTION]${NC} $1"
    echo "========================================"
}

warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

error() {
    echo -e "${RED}[PROBLÈME]${NC} $1"
}

info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

# Analyse 1: Taille et contenu de chaque submodule
analyze_submodule_sizes() {
    section "1. ANALYSE TAILLE ET CONTENU DES SUBMODULES"
    
    echo "Repository | Taille | Fichiers | Type Contenu"
    echo "-----------|--------|----------|-------------"
    
    for submodule in $(git submodule status | awk '{print $2}'); do
        if [ -d "$submodule" ]; then
            local size=$(du -sh "$submodule" 2>/dev/null | cut -f1)
            local file_count=$(find "$submodule" -type f 2>/dev/null | wc -l)
            local main_content=""
            
            # Identifier le type de contenu principal
            if [ -f "$submodule/package.json" ]; then
                main_content="Node.js"
            elif [ -f "$submodule/pyproject.toml" ] || [ -f "$submodule/setup.py" ]; then
                main_content="Python"
            elif [ -f "$submodule/Cargo.toml" ]; then
                main_content="Rust"
            elif [ -d "$submodule/src" ]; then
                main_content="Code Source"
            elif [ -d "$submodule/docs" ]; then
                main_content="Documentation"
            elif find "$submodule" -name "*.py" | head -1 >/dev/null 2>&1; then
                main_content="Scripts Python"
            elif find "$submodule" -name "*.md" | head -5 >/dev/null 2>&1; then
                main_content="Markdown/Docs"
            else
                main_content="Mixte/Autre"
            fi
            
            printf "%-20s | %-6s | %-8s | %s\n" "$(basename $submodule)" "$size" "$file_count" "$main_content"
        fi
    done
    echo ""
}

# Analyse 2: Détection des duplications
analyze_duplications() {
    section "2. DÉTECTION DES DUPLICATIONS"
    
    log "Recherche de modules dupliqués dans Panini-FS..."
    
    if [ -d "modules/core/filesystem/modules" ]; then
        error "🚨 DUPLICATION DÉTECTÉE: Panini-FS contient d'autres modules !"
        echo ""
        info "Modules trouvés dans Panini-FS:"
        ls -la modules/core/filesystem/modules/ | grep "^d" | awk '{print "   - " $9}' | grep -v "^\.$\|^\.\.$"
        echo ""
        
        log "Comparaison avec les submodules externes..."
        for internal_module in $(ls modules/core/filesystem/modules/ 2>/dev/null); do
            # Chercher le submodule correspondant
            local external_found=""
            for submodule in $(git submodule status | awk '{print $2}'); do
                local submodule_name=$(basename "$submodule")
                if [[ "$submodule_name" == *"$(echo $internal_module | sed 's/-/ /g')"* ]] || [[ "$internal_module" == *"$(echo $submodule_name | sed 's/-/ /g')"* ]]; then
                    external_found="$submodule"
                    break
                fi
            done
            
            if [ -n "$external_found" ]; then
                error "   DUPLICATION: $internal_module (interne) ↔ $external_found (submodule)"
            else
                warning "   ORPHELIN: $internal_module (seulement interne)"
            fi
        done
    else
        info "✅ Pas de duplication évidente dans Panini-FS"
    fi
    echo ""
}

# Analyse 3: Responsabilités et cohérence
analyze_responsibilities() {
    section "3. ANALYSE DES RESPONSABILITÉS"
    
    log "Analyse du contenu pour identifier les responsabilités..."
    echo ""
    
    # Analyser chaque submodule
    for submodule in $(git submodule status | awk '{print $2}'); do
        if [ -d "$submodule" ]; then
            echo "📂 $(basename $submodule):"
            
            # Chercher des indices de responsabilité
            local responsibilities=""
            
            # Analyser le README principal
            if [ -f "$submodule/README.md" ]; then
                local readme_content=$(head -10 "$submodule/README.md" | tr '\n' ' ')
                echo "   Description: $(echo "$readme_content" | sed 's/^#* *//' | cut -c1-80)..."
            fi
            
            # Analyser la structure
            if [ -d "$submodule/src" ]; then
                local src_dirs=$(find "$submodule/src" -type d -maxdepth 2 2>/dev/null | head -5 | sed 's|.*/||' | tr '\n' ', ')
                echo "   Structure src: $src_dirs"
            fi
            
            # Détecter les technologies
            local tech_stack=""
            [ -f "$submodule/package.json" ] && tech_stack="${tech_stack}Node.js "
            [ -f "$submodule/pyproject.toml" ] && tech_stack="${tech_stack}Python "
            [ -f "$submodule/Cargo.toml" ] && tech_stack="${tech_stack}Rust "
            [ -f "$submodule/requirements.txt" ] && tech_stack="${tech_stack}Python-deps "
            [ -d "$submodule/.github" ] && tech_stack="${tech_stack}CI/CD "
            
            if [ -n "$tech_stack" ]; then
                echo "   Technologies: $tech_stack"
            fi
            
            # Détecter les problèmes
            local issues=""
            if [ -d "$submodule/modules" ]; then
                issues="${issues}Contient-autres-modules "
            fi
            if find "$submodule" -name "copilotage" -type d | head -1 >/dev/null 2>&1; then
                issues="${issues}Contient-copilotage "
            fi
            if [ $(find "$submodule" -type f 2>/dev/null | wc -l) -gt 1000 ]; then
                issues="${issues}Très-volumineux "
            fi
            
            if [ -n "$issues" ]; then
                warning "   ⚠️ Problèmes: $issues"
            fi
            
            echo ""
        fi
    done
}

# Analyse 4: Dépendances croisées
analyze_dependencies() {
    section "4. ANALYSE DES DÉPENDANCES CROISÉES"
    
    log "Recherche de références entre modules..."
    echo ""
    
    for submodule in $(git submodule status | awk '{print $2}'); do
        if [ -d "$submodule" ]; then
            local module_name=$(basename "$submodule")
            echo "🔗 Dépendances de $module_name:"
            
            # Chercher des imports/références vers d'autres modules Panini
            local refs_found=false
            for other_submodule in $(git submodule status | awk '{print $2}'); do
                if [ "$submodule" != "$other_submodule" ]; then
                    local other_name=$(basename "$other_submodule")
                    local search_terms=("$other_name" "$(echo $other_name | sed 's/Panini-//')" "$(echo $other_name | tr '[:upper:]' '[:lower:]')")
                    
                    for term in "${search_terms[@]}"; do
                        if grep -r "$term" "$submodule" --include="*.py" --include="*.js" --include="*.md" --include="*.json" >/dev/null 2>&1; then
                            echo "   → Référence vers $other_name"
                            refs_found=true
                            break
                        fi
                    done
                fi
            done
            
            if [ "$refs_found" = false ]; then
                info "   Aucune dépendance détectée"
            fi
            echo ""
        fi
    done
}

# Analyse 5: Suggestions d'architecture
suggest_architecture() {
    section "5. SUGGESTIONS D'ARCHITECTURE SIMPLIFIÉE"
    
    log "Basé sur l'analyse, voici mes suggestions..."
    echo ""
    
    info "ARCHITECTURE ACTUELLE (PROBLÉMATIQUE):"
    echo "   - Trop de modules (13 submodules)"
    echo "   - Panini-FS contient d'autres modules (duplication)"
    echo "   - Responsabilités floues"
    echo "   - Hiérarchie confuse"
    echo ""
    
    info "ARCHITECTURE SUGGÉRÉE SIMPLIFIÉE:"
    echo "   1. 🧠 Panini-Core        (semantic + filesystem unifié)"
    echo "   2. 🔧 Panini-Services    (colab + publication + datasets)"
    echo "   3. ⚡ Panini-Infrastructure (reactive + autonomous + cloud + execution)"
    echo "   4. 🤝 Panini-Shared      (copilotage + speckit + attribution)"
    echo "   5. 🔬 Panini-Research    (recherche et expérimentation)"
    echo ""
    
    warning "QUESTIONS À CLARIFIER:"
    echo "   Q1: Faut-il fusionner filesystem et semantic en un seul 'Core' ?"
    echo "   Q2: Les services peuvent-ils être regroupés en un seul module ?"
    echo "   Q3: Panini-FS doit-il être nettoyé de ses sous-modules internes ?"
    echo "   Q4: Quels modules sont vraiment essentiels vs expérimentaux ?"
    echo "   Q5: Y a-t-il du contenu à migrer avant suppression ?"
    echo ""
}

# Fonction principale d'analyse
main() {
    log "🔍 ANALYSE ARCHITECTURALE APPROFONDIE - ÉCOSYSTÈME PANINI"
    echo "=========================================================="
    echo ""
    
    analyze_submodule_sizes
    analyze_duplications  
    analyze_responsibilities
    analyze_dependencies
    suggest_architecture
    
    echo ""
    log "📋 PROCHAINES ÉTAPES RECOMMANDÉES:"
    echo "   1. Répondre aux questions de clarification"
    echo "   2. Décider de l'architecture cible simplifiée"
    echo "   3. Planifier la migration/fusion des modules"
    echo "   4. Nettoyer les duplications"
    echo "   5. Valider la cohérence finale"
    echo ""
}

# Point d'entrée
main "$@"