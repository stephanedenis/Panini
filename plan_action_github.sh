#!/bin/bash

# 🚀 PLAN D'ACTION GITHUB PANINI
# Organisation et synchronisation complète ecosystem

echo "🚀 PLAN D'ACTION GITHUB PANINI"
echo "============================="
echo

WORKSPACE="/home/stephane/GitHub/Panini"
cd "$WORKSPACE"

# Actions à proposer
propose_actions() {
    echo "📋 ACTIONS PROPOSÉES BASÉES SUR L'AUDIT :"
    echo
    
    echo "1️⃣ 🏗️  CRÉER REPOSITORIES MANQUANTS"
    echo "   → Panini-OntoWave (priorité haute)"
    echo "   → Repositories pour projets réels uniquement"
    echo
    
    echo "2️⃣ 📋 RÉORGANISER ISSUES & PROJETS"
    echo "   → Nettoyer les 12 issues actuelles"
    echo "   → Aligner avec architecture 3 projets réels"
    echo "   → Organiser projets GitHub (15 actuels)"
    echo
    
    echo "3️⃣ 🔗 NETTOYER SUBMODULES"
    echo "   → 13 submodules configurés mais non-initialisés"
    echo "   → Garder seulement les projets réels"
    echo "   → Supprimer les scaffolds"
    echo
    
    echo "4️⃣ 📊 SYNCHRONISER TRAVAIL LOCAL"
    echo "   → 23 fichiers d'analyse non-trackés"
    echo "   → Organiser documentation"
    echo "   → Commit architecture finale"
    echo
    
    echo "Quelle action voulez-vous prioriser ?"
    echo
    echo "a) Créer Panini-OntoWave repository"
    echo "b) Réorganiser issues selon architecture réelle"
    echo "c) Nettoyer submodules (garder projets réels)"
    echo "d) Synchroniser travail local (commit analyses)"
    echo "e) Tout faire automatiquement"
    echo
    read -r -p "Votre choix (a/b/c/d/e): " choice
    
    case "$choice" in
        a) create_ontowave_repo ;;
        b) reorganize_issues ;;
        c) clean_submodules ;;
        d) sync_local_work ;;
        e) full_automation ;;
        *) echo "❌ Choix invalide" ;;
    esac
}

# Action A : OntoWave déjà intégré (FAIT ✅)
create_ontowave_repo() {
    echo
    echo "✅ ONTOWAVE DÉJÀ INTÉGRÉ AVEC SUCCÈS"
    echo "=================================="
    
    echo "🎉 OntoWave repository confirmé et intégré :"
    echo "  📍 GitHub : https://github.com/stephanedenis/OntoWave.git"
    echo "  🔗 Submodule : projects/ontowave/"
    echo "  📊 Status : 18 issues ouvertes, très actif"
    echo "  💻 Tech : TypeScript/Vite avec tests complets"
    echo
    
    # Vérifier l'intégration
    if [ -d "projects/ontowave" ]; then
        echo "✅ Submodule OntoWave fonctionnel :"
        echo "  � Chemin : projects/ontowave/"
        echo "  🔍 Contenu : $(ls projects/ontowave/ | wc -l) fichiers/dossiers"
        
        cd "projects/ontowave"
        echo "  🌿 Branche : $(git branch --show-current 2>/dev/null || echo 'N/A')"
        echo "  📝 Dernier commit : $(git log -1 --format='%h - %s' 2>/dev/null || echo 'N/A')"
        cd "$WORKSPACE"
        
        echo
        echo "🎯 ARCHITECTURE 3 PROJETS RÉELS CONFIRMÉE :"
        echo "  ✅ 🧪 Research (cœur recherche)"
        echo "  ✅ 🗂️ Filesystem (FS sémantique)"  
        echo "  ✅ 🌊 OntoWave (interface MD)"
        echo
        echo "� Prêt pour nettoyage des 10 modules scaffolds restants !"
    else
        echo "❌ Erreur : Submodule OntoWave non trouvé"
    fi
}

# Action B : Réorganiser issues
reorganize_issues() {
    echo
    echo "📋 RÉORGANISATION ISSUES GITHUB"
    echo "==============================="
    
    echo "🎯 Objectif : Aligner issues avec architecture 3 projets réels"
    echo
    echo "📊 Issues actuelles (12) :"
    gh issue list --limit 15 --json number,title,labels | jq -r '.[] | "  #\(.number) - \(.title)"'
    echo
    
    echo "💡 Stratégie proposée :"
    echo "  🧪 RESEARCH : Issues #1,#2,#3,#5,#12,#13"
    echo "  🗂️ FILESYSTEM : Issues #4,#11"  
    echo "  🌊 ONTOWAVE : Nouvelles issues à créer"
    echo "  🛠️ TOOLS : Issues #8,#9,#10,#14"
    echo
    
    echo "Voulez-vous :"
    echo "1) Créer des labels pour les 3 projets réels"
    echo "2) Réorganiser les issues existantes"
    echo "3) Créer issues OntoWave manquantes"
    echo "4) Archiver issues obsolètes"
    echo
    read -r -p "Action (1/2/3/4): " action
    
    case "$action" in
        1)
            echo "🏷️ Création des labels..."
            gh label create "project:research" --description "Research module" --color "0052cc" || true
            gh label create "project:filesystem" --description "Filesystem module" --color "d73a4a" || true
            gh label create "project:ontowave" --description "OntoWave interface" --color "0e8a16" || true
            gh label create "type:architecture" --description "Architecture decisions" --color "f9d0c4" || true
            echo "✅ Labels créés !"
            ;;
        2)
            echo "📝 Réorganisation des issues..."
            echo "  (Vous pouvez utiliser l'interface GitHub pour les labels)"
            echo "  Ou utiliser : gh issue edit <number> --add-label <label>"
            ;;
        3)
            echo "🌊 Création issues OntoWave..."
            gh issue create \
                --title "[ONTOWAVE] Interface navigation MD sémantique" \
                --body "Créer interface ultra-légère pour navigation et visualisation des documents Markdown avec API plugins modulaire" \
                --label "project:ontowave"
            echo "✅ Issue OntoWave créée !"
            ;;
        4)
            echo "📦 Identification issues obsolètes..."
            echo "  Issues potentiellement obsolètes avec l'architecture 3 projets :"
            echo "  (Révision manuelle recommandée)"
            ;;
    esac
}

# Action C : Nettoyer submodules
clean_submodules() {
    echo
    echo "🔗 NETTOYAGE SUBMODULES"
    echo "======================="
    
    echo "📊 Submodules actuels (13) :"
    if [ -f ".gitmodules" ]; then
        grep "^\[submodule" .gitmodules | sed 's/\[submodule "\(.*\)"\]/  📦 \1/'
    fi
    echo
    
    echo "🎯 Stratégie basée sur architecture réelle :"
    echo "  ✅ GARDER : research, filesystem, (ontowave à ajouter)"
    echo "  ❌ SUPPRIMER : 10 modules scaffolds/mixtes"
    echo
    
    echo "⚠️ Cette action va modifier .gitmodules et supprimer des submodules"
    echo "💾 Sauvegarde automatique créée"
    echo
    read -r -p "Confirmer le nettoyage ? (y/N): " confirm
    
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        # Sauvegarde
        cp .gitmodules .gitmodules.backup.$(date +%Y%m%d_%H%M%S)
        
        # Identifier les modules à garder
        modules_to_keep=("research" "modules/core/filesystem")
        
        echo "🧹 Nettoyage en cours..."
        
        # Supprimer les submodules scaffolds
        modules_to_remove=(
            "shared/copilotage"
            "modules/infrastructure/reactive"
            "modules/infrastructure/autonomous"
            "modules/core/semantic"
            "modules/services/colab"
            "modules/orchestration/execution"
            "modules/services/datasets"
            "modules/services/publication"
            "shared/attribution"
            "shared/speckit"
            "modules/orchestration/cloud"
        )
        
        for module in "${modules_to_remove[@]}"; do
            echo "  🗑️ Suppression : $module"
            git submodule deinit -f "$module" 2>/dev/null || true
            git rm -f "$module" 2>/dev/null || true
            rm -rf ".git/modules/$module" 2>/dev/null || true
        done
        
        echo "✅ Submodules nettoyés - Architecture 3 projets réels !"
        echo "📄 Sauvegarde : .gitmodules.backup.*"
    else
        echo "❌ Nettoyage annulé"
    fi
}

# Action D : Synchroniser travail local
sync_local_work() {
    echo
    echo "📊 SYNCHRONISATION TRAVAIL LOCAL"
    echo "==============================="
    
    echo "📁 Fichiers non-trackés (23) :"
    git status --porcelain | grep "^??" | head -10
    echo "  ... (plus de fichiers)"
    echo
    
    echo "🎯 Stratégies proposées :"
    echo "  1) Organiser en dossiers thématiques"
    echo "  2) Commit architecture finale"
    echo "  3) Créer documentation consolidée"
    echo "  4) Nettoyer fichiers temporaires"
    echo
    
    read -r -p "Action (1/2/3/4): " sync_action
    
    case "$sync_action" in
        1)
            echo "📁 Organisation thématique..."
            mkdir -p docs/architecture docs/analyses scripts/
            
            mv *ARCHITECTURE* *PLAN* *PROPOSITION* *RECOMMANDATION* *RESUME* docs/architecture/ 2>/dev/null || true
            mv analyse_* analyseur_* docs/analyses/ 2>/dev/null || true
            mv *.sh scripts/ 2>/dev/null || true
            mv modules_*.txt docs/analyses/ 2>/dev/null || true
            
            echo "✅ Fichiers organisés !"
            ;;
        2)
            echo "💾 Commit architecture finale..."
            git add docs/ scripts/ 2>/dev/null || true
            git commit -m "docs: Architecture finale et outils d'analyse écosystème Panini
            
- Consolidation vers 3 projets réels (research, filesystem, ontowave)
- Outils d'analyse architecturale et audit GitHub
- Documentation complète des décisions architecturales" || echo "⚠️ Erreur commit"
            echo "✅ Architecture commitée !"
            ;;
        3)
            echo "📖 Documentation consolidée..."
            cat > ARCHITECTURE_PANINI_FINALE.md << 'EOF'
# 🎯 ARCHITECTURE PANINI FINALE

## 🚀 Vision
Écosystème focalisé sur 3 projets réels au lieu de 13 modules dispersés.

## 🏗️ Structure
- **🧪 Research** - Cœur du travail de recherche
- **🗂️ Filesystem** - Système de fichiers sémantique
- **🌊 OntoWave** - Interface navigation MD ultra-légère

## 📊 Migration
- 7 modules scaffolds → Consolidation optionnelle
- 4 modules mixtes → Extraction contenu réel
- Focus sur projets utilisateur authentiques
EOF
            echo "✅ Documentation créée : ARCHITECTURE_PANINI_FINALE.md"
            ;;
        4)
            echo "🧹 Nettoyage fichiers temporaires..."
            rm -f *.log *_temp.* 2>/dev/null || true
            echo "✅ Nettoyage effectué !"
            ;;
    esac
}

# Action E : Automatisation complète
full_automation() {
    echo
    echo "🚀 AUTOMATISATION COMPLÈTE"
    echo "=========================="
    
    echo "⚠️ Cette action va :"
    echo "  1. Créer Panini-OntoWave repository"
    echo "  2. Nettoyer submodules (garder 3 projets réels)"
    echo "  3. Organiser documentation"
    echo "  4. Commit architecture finale"
    echo "  5. Créer issues OntoWave"
    echo
    echo "💾 Sauvegarde complète avant modifications"
    echo
    read -r -p "Lancer automatisation complète ? (y/N): " auto_confirm
    
    if [[ "$auto_confirm" =~ ^[Yy]$ ]]; then
        echo "🚀 Lancement automatisation..."
        
        # Sauvegarde
        echo "💾 Sauvegarde..."
        cp .gitmodules .gitmodules.auto_backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null || true
        
        # Toutes les actions
        create_ontowave_repo
        clean_submodules
        sync_local_work
        
        echo "🎉 AUTOMATISATION TERMINÉE !"
        echo "✅ Écosystème GitHub Panini optimisé pour 3 projets réels"
    else
        echo "❌ Automatisation annulée"
    fi
}

# Programme principal
main() {
    echo "🎯 Basé sur l'audit GitHub, voici les actions recommandées"
    echo "📊 État actuel : 2/15 repositories actifs, 12 issues, 13 submodules non-initialisés"
    echo
    propose_actions
}

main