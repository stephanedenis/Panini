#!/bin/bash

# 🎯 CONSOLIDATION FOCALISÉE : PROJETS RÉELS PANINI
# Script basé sur l'analyse des vrais projets utilisateur

echo "🎯 CONSOLIDATION FOCALISÉE PANINI - PROJETS RÉELS"
echo "================================================"
echo

WORKSPACE="/home/stephane/GitHub/Panini"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="$WORKSPACE/sauvegarde_projets_reels_${TIMESTAMP}"

cd "$WORKSPACE"

# Fonction de confirmation
confirm_action() {
    echo "⚠️  $1"
    echo -n "Confirmer cette action ? (y/N): "
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "❌ Action annulée"
        exit 1
    fi
}

# Sauvegarde sécurisée
create_backup() {
    echo "💾 SAUVEGARDE SÉCURISÉE DES PROJETS RÉELS"
    echo "========================================"
    
    mkdir -p "$BACKUP_DIR"
    
    echo "🧪 Sauvegarde RESEARCH (cœur du travail)..."
    if [ -d "research" ]; then
        cp -r research/ "$BACKUP_DIR/research_backup/" 2>/dev/null || true
    fi
    
    echo "🗂️ Sauvegarde FILESYSTEM (projet réel)..."
    if [ -d "modules/core/filesystem" ]; then
        cp -r modules/core/filesystem/ "$BACKUP_DIR/filesystem_backup/" 2>/dev/null || true
    fi
    
    echo "📁 Sauvegarde structure complète..."
    cp -r modules/ "$BACKUP_DIR/modules_avant/" 2>/dev/null || true
    cp -r shared/ "$BACKUP_DIR/shared_avant/" 2>/dev/null || true
    cp .gitmodules "$BACKUP_DIR/gitmodules_avant.txt" 2>/dev/null || true
    
    echo "✅ Sauvegarde créée : $BACKUP_DIR"
}

# Phase 1 : Nettoyer filesystem (extraire expérimentations)
clean_filesystem_project() {
    echo
    echo "🗂️ PHASE 1 : NETTOYAGE FILESYSTEM (PROJET RÉEL)"
    echo "=============================================="
    
    confirm_action "Nettoyer le projet filesystem en préservant le code FS pur ?"
    
    local fs_path="modules/core/filesystem"
    
    if [ -d "$fs_path" ]; then
        echo "📊 État avant nettoyage :"
        echo "  - Taille totale : $(du -sh "$fs_path" | cut -f1)"
        
        # Préparer research pour recevoir les expérimentations
        echo "🧪 Préparation de research/ pour les expérimentations..."
        mkdir -p research/filesystem_experiments/
        mkdir -p research/filesystem_archive/
        
        # Extraire les expérimentations volumineuses vers research
        echo "📦 Extraction des expérimentations vers research/..."
        
        if [ -d "$fs_path/cleanup" ]; then
            echo "  → cleanup/ (48M) → research/filesystem_archive/"
            mv "$fs_path/cleanup" research/filesystem_archive/ 2>/dev/null || true
        fi
        
        if [ -d "$fs_path/experiments" ]; then
            echo "  → experiments/ → research/filesystem_experiments/"
            mv "$fs_path/experiments" research/filesystem_experiments/ 2>/dev/null || true
        fi
        
        if [ -d "$fs_path/RESEARCH" ]; then
            echo "  → RESEARCH/ → research/filesystem_experiments/"
            mv "$fs_path/RESEARCH" research/filesystem_experiments/RESEARCH_from_fs/ 2>/dev/null || true
        fi
        
        # Supprimer les duplications détectées
        echo "🗑️ Suppression des modules dupliqués..."
        if [ -d "$fs_path/modules" ]; then
            rm -rf "$fs_path/modules"
            echo "  → modules/ (duplications) supprimés"
        fi
        
        echo "📊 État après nettoyage :"
        echo "  - Taille filesystem : $(du -sh "$fs_path" | cut -f1)"
        echo "  - Expérimentations dans research/ : ✅"
        echo "✅ Filesystem nettoyé - Focus sur le FS sémantique pur !"
    fi
}

# Phase 2 : Ajouter OntoWave comme submodule
add_ontowave_submodule() {
    echo
    echo "🌊 PHASE 2 : AJOUT ONTOWAVE (INTERFACE ULTRA-LÉGÈRE)"
    echo "=================================================="
    
    confirm_action "Ajouter OntoWave comme submodule indépendant ?"
    
    # Vérifier que OntoWave existe
    if [ ! -d "/home/stephane/GitHub/Panini-OntoWave" ]; then
        echo "❌ OntoWave non trouvé : /home/stephane/GitHub/Panini-OntoWave"
        echo "   Veuillez vérifier le chemin ou cloner le repository"
        return 1
    fi
    
    # Créer la structure projects/
    echo "📁 Création de la structure projects/..."
    mkdir -p projects/
    
    # Ajouter comme submodule
    echo "🔗 Ajout d'OntoWave comme submodule..."
    
    # Vérifier si déjà configuré
    if grep -q "ontowave" .gitmodules 2>/dev/null; then
        echo "  ⚠️ OntoWave déjà configuré dans .gitmodules"
    else
        git submodule add https://github.com/stephanedenis/Panini-OntoWave.git projects/ontowave
        echo "  ✅ Submodule ajouté : projects/ontowave"
    fi
    
    # Vérifier l'ajout
    if [ -d "projects/ontowave" ]; then
        echo "📊 OntoWave configuré :"
        echo "  - Localisation : projects/ontowave/"
        echo "  - Type : Submodule indépendant"
        echo "  - Vocation : Interface MD navigation ultra-légère"
        echo "✅ OntoWave intégré à l'écosystème !"
    else
        echo "❌ Erreur lors de l'ajout d'OntoWave"
        return 1
    fi
}

# Phase 3 : Créer outils de soutien (optionnel)
create_support_tools() {
    echo
    echo "🛠️ PHASE 3 : OUTILS DE SOUTIEN (OPTIONNEL)"
    echo "========================================"
    
    echo "💡 Cette phase crée les outils de soutien pour le développement/recherche."
    echo "   Ces outils fusionnent les modules scaffolds/mixtes détectés."
    echo
    echo "🤔 Voulez-vous créer les outils de soutien maintenant ?"
    echo "   (Vous pouvez le faire plus tard selon vos besoins)"
    echo
    echo "   y = Créer maintenant"
    echo "   n = Seulement les 3 projets principaux pour l'instant"
    echo
    read -r -p "Votre choix (y/N): " choice
    
    if [[ ! "$choice" =~ ^[Yy]$ ]]; then
        echo "⏭️ Outils de soutien reportés - Focus sur les projets principaux"
        return 0
    fi
    
    echo "🔧 Création des outils de soutien..."
    
    # AI-Tooling (modules mixtes)
    echo "🛠️ Création ai-tooling/ (soutien développement)..."
    mkdir -p consolidated/ai-tooling/
    
    for module in shared/copilotage shared/attribution shared/speckit; do
        if [ -d "$module" ]; then
            module_name=$(basename "$module")
            echo "  → $module_name"
            cp -r "$module" "consolidated/ai-tooling/" 2>/dev/null || true
        fi
    done
    
    if [ -d "modules/orchestration/execution" ]; then
        echo "  → execution (mixte)"
        cp -r modules/orchestration/execution consolidated/ai-tooling/execution 2>/dev/null || true
    fi
    
    # Agent-Orchestrator (modules scaffolds)
    echo "🤖 Création agent-orchestrator/ (soutien recherche)..."
    mkdir -p consolidated/agent-orchestrator/
    
    # Base structure
    mkdir -p consolidated/agent-orchestrator/drivers/
    mkdir -p consolidated/agent-orchestrator/missions/
    mkdir -p consolidated/agent-orchestrator/monitoring/
    
    # Fusionner les scaffolds
    for module in modules/services/colab modules/orchestration/cloud; do
        if [ -d "$module" ]; then
            module_name=$(basename "$module")
            echo "  → driver: $module_name"
            cp -r "$module" "consolidated/agent-orchestrator/drivers/" 2>/dev/null || true
        fi
    done
    
    for module in modules/infrastructure/autonomous; do
        if [ -d "$module" ]; then
            echo "  → missions: autonomous"
            cp -r "$module" "consolidated/agent-orchestrator/missions/" 2>/dev/null || true
        fi
    done
    
    for module in modules/infrastructure/reactive; do
        if [ -d "$module" ]; then
            echo "  → monitoring: reactive"
            cp -r "$module" "consolidated/agent-orchestrator/monitoring/" 2>/dev/null || true
        fi
    done
    
    echo "✅ Outils de soutien créés dans consolidated/"
}

# Analyse finale
analyze_final_structure() {
    echo
    echo "📊 ANALYSE DE LA STRUCTURE FINALE"
    echo "================================="
    
    echo "🎯 PROJETS PRINCIPAUX (développement actif) :"
    echo
    
    if [ -d "research" ]; then
        research_size=$(du -sh research 2>/dev/null | cut -f1)
        research_files=$(find research -type f 2>/dev/null | wc -l)
        echo "  🧪 research/ - $research_size ($research_files fichiers) - CŒUR TRAVAIL"
    fi
    
    if [ -d "modules/core/filesystem" ]; then
        fs_size=$(du -sh modules/core/filesystem 2>/dev/null | cut -f1)
        fs_files=$(find modules/core/filesystem -type f 2>/dev/null | wc -l)
        echo "  🗂️ filesystem/ - $fs_size ($fs_files fichiers) - FS SÉMANTIQUE"
    fi
    
    if [ -d "projects/ontowave" ]; then
        echo "  🌊 ontowave/ - Submodule - INTERFACE MD NAVIGATION"
    fi
    
    echo
    echo "🛠️ OUTILS DE SOUTIEN (optionnels) :"
    
    if [ -d "consolidated/ai-tooling" ]; then
        tooling_size=$(du -sh consolidated/ai-tooling 2>/dev/null | cut -f1)
        echo "  🛠️ ai-tooling/ - $tooling_size - SOUTIEN DÉVELOPPEMENT"
    else
        echo "  🛠️ ai-tooling/ - À créer si besoin"
    fi
    
    if [ -d "consolidated/agent-orchestrator" ]; then
        orchestrator_size=$(du -sh consolidated/agent-orchestrator 2>/dev/null | cut -f1)
        echo "  🤖 agent-orchestrator/ - $orchestrator_size - SOUTIEN RECHERCHE"
    else
        echo "  🤖 agent-orchestrator/ - À créer si besoin"
    fi
    
    echo
    echo "📊 COMPARAISON :"
    echo "  AVANT : 13 modules dispersés + duplications"
    echo "  APRÈS : 3 projets principaux + outils optionnels"
    echo "  FOCUS : Projets réels préservés et clarifiés"
}

# Programme principal
main() {
    echo "🎯 OBJECTIF : Consolidation focalisée sur vos projets réels"
    echo
    echo "📋 PLAN D'ACTION :"
    echo "  1. 🧪 PRÉSERVER research/ (cœur de votre travail)"
    echo "  2. 🗂️ NETTOYER filesystem/ (projet FS sémantique)"
    echo "  3. 🌊 AJOUTER OntoWave (interface ultra-légère)"
    echo "  4. 🛠️ OUTILS soutien (optionnel)"
    echo
    echo "✅ Approche : Focus sur vos 3 projets réels"
    echo "⚠️ 7 modules scaffolds + 4 mixtes → outils optionnels"
    echo
    
    # Sauvegarde
    create_backup
    
    # Phase 1 : Nettoyer filesystem
    clean_filesystem_project
    
    # Phase 2 : Ajouter OntoWave
    add_ontowave_submodule
    
    # Phase 3 : Outils optionnels
    create_support_tools
    
    # Analyse finale
    analyze_final_structure
    
    echo
    echo "🎉 CONSOLIDATION FOCALISÉE TERMINÉE !"
    echo "===================================="
    echo "📁 Sauvegarde : $BACKUP_DIR"
    echo
    echo "🎯 RÉSULTAT : Architecture focalisée sur vos projets réels :"
    echo "  🧪 Research (préservé et enrichi)"
    echo "  🗂️ Filesystem (nettoyé, focus FS sémantique)"
    echo "  🌊 OntoWave (interface MD navigation)"
    echo "  🛠️ Outils soutien (selon besoins)"
    echo
    echo "🚀 Panini maintenant ALIGNÉ avec vos priorités de développement !"
}

# Lancement
main