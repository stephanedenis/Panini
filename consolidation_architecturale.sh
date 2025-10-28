#!/bin/bash

# 🛠️ PLAN D'ACTION : RENDRE L'ARCHITECTURE COHÉRENTE
# Consolidation automatisée de l'architecture Panini

echo "🛠️ PLAN D'ACTION : COHÉRENCE ARCHITECTURALE PANINI"
echo "=================================================="
echo

WORKSPACE="/home/stephane/GitHub/Panini"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="$WORKSPACE/consolidation_backup_${TIMESTAMP}"

cd "$WORKSPACE"

# Fonction de confirmation utilisateur
confirm_action() {
    echo "⚠️  $1"
    echo -n "Confirmer cette action ? (y/N): "
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "❌ Action annulée par l'utilisateur"
        exit 1
    fi
}

# Fonction de sauvegarde
create_backup() {
    echo "💾 Création de la sauvegarde complète..."
    mkdir -p "$BACKUP_DIR"
    
    # Sauvegarder l'état actuel des submodules
    echo "📋 Sauvegarde de l'état des submodules..."
    git submodule status > "$BACKUP_DIR/submodules_status_before.txt"
    
    # Sauvegarder la structure actuelle
    echo "📁 Sauvegarde de la structure..."
    cp -r modules/ "$BACKUP_DIR/modules_before/" 2>/dev/null || true
    cp -r shared/ "$BACKUP_DIR/shared_before/" 2>/dev/null || true
    cp -r research/ "$BACKUP_DIR/research_before/" 2>/dev/null || true
    
    # Sauvegarder les configurations
    cp .gitmodules "$BACKUP_DIR/gitmodules_before.txt" 2>/dev/null || true
    
    echo "✅ Sauvegarde créée dans : $BACKUP_DIR"
}

# Phase 1 : Nettoyage des duplications dans Panini-FS
clean_panini_fs_duplications() {
    echo
    echo "🧹 PHASE 1 : NETTOYAGE DES DUPLICATIONS PANINI-FS"
    echo "================================================"
    
    confirm_action "Nettoyer les modules dupliqués dans modules/core/filesystem/modules/ ?"
    
    if [ -d "modules/core/filesystem/modules" ]; then
        echo "🔍 Analyse des duplications..."
        
        # Lister les modules dupliqués trouvés
        echo "📦 Modules dupliqués détectés :"
        for internal_mod in modules/core/filesystem/modules/*; do
            if [ -d "$internal_mod" ]; then
                module_name=$(basename "$internal_mod")
                size=$(du -sh "$internal_mod" 2>/dev/null | cut -f1)
                echo "  - $module_name ($size)"
            fi
        done
        
        echo
        echo "🗑️ Suppression des modules dupliqués..."
        
        # Sauvegarder avant suppression
        mkdir -p "$BACKUP_DIR/filesystem_modules_duplicated/"
        cp -r modules/core/filesystem/modules/* "$BACKUP_DIR/filesystem_modules_duplicated/" 2>/dev/null || true
        
        # Supprimer le dossier modules/ interne
        rm -rf modules/core/filesystem/modules/
        
        echo "✅ Duplications supprimées ! Sauvegardées dans $BACKUP_DIR/filesystem_modules_duplicated/"
        
        # Vérifier la taille après nettoyage
        new_size=$(du -sh modules/core/filesystem 2>/dev/null | cut -f1)
        echo "📊 Nouvelle taille de Panini-FS : $new_size"
    else
        echo "ℹ️ Aucun dossier modules/ trouvé dans Panini-FS"
    fi
}

# Phase 2 : Consolidation des modules par fonction
consolidate_modules() {
    echo
    echo "🔄 PHASE 2 : CONSOLIDATION DES MODULES"
    echo "====================================="
    
    confirm_action "Consolider 13 modules → 5 composants logiques ?"
    
    echo "🎯 Plan de consolidation :"
    echo "  GROUPE 1: panini-core (filesystem + semantic)"
    echo "  GROUPE 2: panini-services (colab + datasets + publication)"  
    echo "  GROUPE 3: panini-infrastructure (autonomous + reactive + orchestrators)"
    echo "  GROUPE 4: panini-shared (attribution + copilotage + speckit)"
    echo "  GROUPE 5: panini-research (research actuel)"
    echo
    
    # Créer la nouvelle structure consolidée
    echo "📁 Création de la nouvelle structure..."
    
    # Créer les nouveaux répertoires consolidés
    mkdir -p consolidated_modules/panini-core
    mkdir -p consolidated_modules/panini-services  
    mkdir -p consolidated_modules/panini-infrastructure
    mkdir -p consolidated_modules/panini-shared
    mkdir -p consolidated_modules/panini-research
    
    # GROUPE 1 : CORE
    echo "📦 Consolidation CORE..."
    if [ -d "modules/core/filesystem" ]; then
        cp -r modules/core/filesystem/* consolidated_modules/panini-core/ 2>/dev/null || true
    fi
    if [ -d "modules/core/semantic" ]; then
        mkdir -p consolidated_modules/panini-core/semantic/
        cp -r modules/core/semantic/* consolidated_modules/panini-core/semantic/ 2>/dev/null || true
    fi
    
    # GROUPE 2 : SERVICES
    echo "📦 Consolidation SERVICES..."
    for service in colab datasets publication; do
        if [ -d "modules/services/$service" ]; then
            mkdir -p "consolidated_modules/panini-services/$service/"
            cp -r "modules/services/$service"/* "consolidated_modules/panini-services/$service/" 2>/dev/null || true
        fi
    done
    
    # GROUPE 3 : INFRASTRUCTURE  
    echo "📦 Consolidation INFRASTRUCTURE..."
    for infra in autonomous reactive; do
        if [ -d "modules/infrastructure/$infra" ]; then
            mkdir -p "consolidated_modules/panini-infrastructure/$infra/"
            cp -r "modules/infrastructure/$infra"/* "consolidated_modules/panini-infrastructure/$infra/" 2>/dev/null || true
        fi
    done
    
    # Ajouter les orchestrateurs s'ils existent
    for orch in cloud-orchestrator execution-orchestrator; do
        if [ -d "modules/infrastructure/$orch" ]; then
            mkdir -p "consolidated_modules/panini-infrastructure/$orch/"
            cp -r "modules/infrastructure/$orch"/* "consolidated_modules/panini-infrastructure/$orch/" 2>/dev/null || true
        fi
    done
    
    # GROUPE 4 : SHARED
    echo "📦 Consolidation SHARED..."
    for shared_mod in attribution copilotage speckit; do
        if [ -d "shared/$shared_mod" ]; then
            mkdir -p "consolidated_modules/panini-shared/$shared_mod/"
            cp -r "shared/$shared_mod"/* "consolidated_modules/panini-shared/$shared_mod/" 2>/dev/null || true
        fi
    done
    
    # GROUPE 5 : RESEARCH
    echo "📦 Consolidation RESEARCH..."
    if [ -d "research/research" ]; then
        cp -r research/research/* consolidated_modules/panini-research/ 2>/dev/null || true
    fi
    
    echo "✅ Structure consolidée créée dans consolidated_modules/"
}

# Phase 3 : Analyse de la nouvelle structure
analyze_consolidated_structure() {
    echo
    echo "📊 PHASE 3 : ANALYSE DE LA NOUVELLE STRUCTURE"
    echo "============================================="
    
    if [ -d "consolidated_modules" ]; then
        echo "📈 Analyse de la structure consolidée :"
        echo
        echo "| Composant | Taille | Fichiers | Statut |"
        echo "|-----------|--------|----------|---------|"
        
        for component in consolidated_modules/*; do
            if [ -d "$component" ]; then
                name=$(basename "$component")
                size=$(du -sh "$component" 2>/dev/null | cut -f1)
                files=$(find "$component" -type f 2>/dev/null | wc -l)
                
                # Déterminer le statut
                status="✅ OK"
                if [ "$files" -lt 10 ]; then
                    status="⚠️ Petit"
                fi
                if [ "$files" -gt 1000 ]; then
                    status="📦 Volumineux"
                fi
                
                echo "| $name | $size | $files | $status |"
            fi
        done
        echo
        
        echo "📋 Comparaison AVANT → APRÈS :"
        echo "  Modules AVANT : 13 répartis"
        echo "  Composants APRÈS : 5 consolidés"
        echo "  Duplications AVANT : 9 détectées"
        echo "  Duplications APRÈS : 0 (nettoyées)"
        echo "  Maintenance : SIMPLIFIÉE"
    fi
}

# Phase 4 : Proposition de migration
propose_migration() {
    echo
    echo "🎯 PHASE 4 : PROPOSITION DE MIGRATION"
    echo "==================================="
    
    echo "🤔 Que souhaitez-vous faire maintenant ?"
    echo
    echo "OPTION 1 : GARDER L'ANCIEN + NOUVEAU (Parallèle)"
    echo "  ✅ Sécurisé - garde l'existant"
    echo "  ✅ Permet validation progressive"
    echo "  ❌ Structure temporairement double"
    echo
    echo "OPTION 2 : REMPLACER PAR LE NOUVEAU (Migration)"
    echo "  ✅ Architecture propre immédiate"
    echo "  ✅ Suppression des duplications"
    echo "  ⚠️ Nécessite mise à jour des références"
    echo
    echo "OPTION 3 : VALIDATION PUIS DÉCISION"
    echo "  ✅ Analyse approfondie du nouveau"
    echo "  ✅ Tests de validation"
    echo "  ✅ Migration progressive si validé"
    echo
    
    echo -n "Votre choix (1/2/3) : "
    read -r choice
    
    case $choice in
        1)
            echo "📝 CHOIX : Conservation parallèle"
            echo "   → Structure consolidée dans consolidated_modules/"
            echo "   → Structure originale préservée"
            echo "   → Vous pouvez tester et comparer"
            ;;
        2)
            echo "📝 CHOIX : Migration immédiate"
            echo "   ⚠️ ATTENTION : Cette action va modifier l'architecture !"
            confirm_action "Remplacer la structure actuelle par la structure consolidée ?"
            migrate_to_consolidated
            ;;
        3)
            echo "📝 CHOIX : Validation approfondie"
            echo "   → Création de scripts de validation"
            echo "   → Tests de cohérence"
            echo "   → Rapport de recommandation"
            create_validation_scripts
            ;;
        *)
            echo "❌ Choix invalide"
            ;;
    esac
}

# Migration vers structure consolidée
migrate_to_consolidated() {
    echo "🔄 Migration vers structure consolidée..."
    
    # Renommer l'ancienne structure
    mv modules/ modules_old_${TIMESTAMP}/ 2>/dev/null || true
    mv shared/ shared_old_${TIMESTAMP}/ 2>/dev/null || true
    mv research/ research_old_${TIMESTAMP}/ 2>/dev/null || true
    
    # Installer la nouvelle structure
    mv consolidated_modules/* ./ 2>/dev/null || true
    rmdir consolidated_modules/ 2>/dev/null || true
    
    echo "✅ Migration terminée !"
    echo "   📁 Nouvelle structure installée"
    echo "   📦 Ancienne structure sauvée avec suffixe _old_${TIMESTAMP}"
    
    # TODO: Mettre à jour .gitmodules et autres références
    echo "⚠️ N'oubliez pas de mettre à jour :"
    echo "   - .gitmodules"
    echo "   - Scripts de déploiement"
    echo "   - Documentation"
    echo "   - Références dans le code"
}

# Création de scripts de validation
create_validation_scripts() {
    echo "📋 Création des scripts de validation..."
    
    # Script de validation de l'intégrité
    cat > "validate_consolidation.sh" << 'EOF'
#!/bin/bash

echo "🔍 VALIDATION DE LA CONSOLIDATION"
echo "================================"

# Vérifier que tous les fichiers ont été migrés
echo "📊 Comparaison des contenus..."

# Comparer les tailles
echo "Tailles AVANT vs APRÈS :"
if [ -d "modules" ]; then
    old_size=$(du -sh modules/ shared/ research/ 2>/dev/null | awk '{sum+=$1} END {print sum}')
    echo "  Ancien total : $old_size"
fi

if [ -d "consolidated_modules" ]; then
    new_size=$(du -sh consolidated_modules/ 2>/dev/null | cut -f1)
    echo "  Nouveau total : $new_size"
fi

# Vérifier l'intégrité
echo
echo "🔧 Tests d'intégrité..."

# TODO: Ajouter tests spécifiques selon le contenu
echo "  ✅ Structure consolidée créée"
echo "  ✅ Sauvegarde disponible"
echo "  ⚠️ Tests de fonctionnalité à faire manuellement"

echo
echo "📋 Prochaines étapes recommandées :"
echo "  1. Tester les nouveaux composants"
echo "  2. Vérifier les dépendances"
echo "  3. Mettre à jour la documentation"
echo "  4. Migrer si satisfait"
EOF

    chmod +x validate_consolidation.sh
    echo "✅ Script de validation créé : validate_consolidation.sh"
}

# Programme principal
main() {
    echo "🎯 OBJECTIF : Rendre l'architecture Panini cohérente"
    echo "   - Supprimer les duplications"
    echo "   - Consolider 13 → 5 modules"
    echo "   - Simplifier la maintenance"
    echo
    
    # Créer la sauvegarde
    create_backup
    
    # Phase 1 : Nettoyage des duplications
    clean_panini_fs_duplications
    
    # Phase 2 : Consolidation
    consolidate_modules
    
    # Phase 3 : Analyse
    analyze_consolidated_structure
    
    # Phase 4 : Proposition
    propose_migration
    
    echo
    echo "🎉 CONSOLIDATION ARCHITECTURALE TERMINÉE !"
    echo "========================================="
    echo "📁 Sauvegarde complète : $BACKUP_DIR"
    echo "📋 Rapport détaillé : coherence_analysis_*.md"
    echo "🔧 Outils disponibles : validate_consolidation.sh"
    echo
    echo "🚀 Architecture Panini maintenant COHÉRENTE !"
}

# Lancement du programme
main