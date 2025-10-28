#!/bin/bash

# 📋 RÉORGANISATION ISSUES SELON ARCHITECTURE 3 PROJETS RÉELS
# Organisation automatique des 12 issues existantes

echo "📋 RÉORGANISATION ISSUES GITHUB PANINI"
echo "====================================="
echo

cd /home/stephane/GitHub/Panini

# Classification des issues selon architecture réelle
classify_issues() {
    echo "🎯 CLASSIFICATION SELON 3 PROJETS RÉELS :"
    echo
    
    # RESEARCH ISSUES (Cœur de recherche)
    echo "🧪 ISSUES PROJECT:RESEARCH :"
    echo "  #13 - Atomes Sémantiques Évolutifs + Multilinguisme"
    echo "  #12 - Séparation Contenant/Contenu - Corpus"  
    echo "  #5  - Foundations mathématiques compression sémantique"
    echo "  #3  - Extraction primitive cross-modal"
    echo "  #2  - Optimisation algorithmes hashing sémantique"
    echo "  #1  - Développement primitives aspectuelles"
    
    # FILESYSTEM ISSUES (FS sémantique)
    echo
    echo "🗂️ ISSUES PROJECT:FILESYSTEM :"
    echo "  #11 - Validateurs PaniniFS - Ingestion/Restitution"
    echo "  #4  - Prototype système fichiers adressage sémantique"
    
    # LEGACY/TOOLS ISSUES (Anciens modules)
    echo
    echo "📦 ISSUES LEGACY/TOOLS :"
    echo "  #14 - Dashboard Métriques (tools)"
    echo "  #10 - Infrastructure autonomie (legacy)"
    echo "  #9  - Copilotage Git workflow (legacy)"
    echo "  #8  - Documentation dhatu (tools)"
    
    # ONTOWAVE ISSUES (À créer)
    echo
    echo "🌊 ISSUES ONTOWAVE (À créer) :"
    echo "  → Interface navigation MD"
    echo "  → API plugins modulaire"
    echo "  → Visualisation sémantique"
}

# Application des labels
apply_labels() {
    echo
    echo "🏷️ APPLICATION DES LABELS :"
    echo "=========================="
    
    # Research issues
    echo "🧪 Labeling RESEARCH issues..."
    gh issue edit 13 --add-label "project:research" 2>/dev/null || echo "  ⚠️ Issue #13 erreur"
    gh issue edit 12 --add-label "project:research" 2>/dev/null || echo "  ⚠️ Issue #12 erreur"
    gh issue edit 5 --add-label "project:research" 2>/dev/null || echo "  ⚠️ Issue #5 erreur"
    gh issue edit 3 --add-label "project:research" 2>/dev/null || echo "  ⚠️ Issue #3 erreur"
    gh issue edit 2 --add-label "project:research" 2>/dev/null || echo "  ⚠️ Issue #2 erreur"
    gh issue edit 1 --add-label "project:research" 2>/dev/null || echo "  ⚠️ Issue #1 erreur"
    
    # Filesystem issues  
    echo "🗂️ Labeling FILESYSTEM issues..."
    gh issue edit 11 --add-label "project:filesystem" 2>/dev/null || echo "  ⚠️ Issue #11 erreur"
    gh issue edit 4 --add-label "project:filesystem" 2>/dev/null || echo "  ⚠️ Issue #4 erreur"
    
    # Legacy issues
    echo "📦 Labeling LEGACY issues..."
    gh issue edit 10 --add-label "legacy:modules" 2>/dev/null || echo "  ⚠️ Issue #10 erreur"
    gh issue edit 9 --add-label "legacy:modules" 2>/dev/null || echo "  ⚠️ Issue #9 erreur"
    
    # Tools issues (garder comme outils)
    echo "🛠️ Labeling TOOLS issues..."
    gh issue edit 14 --add-label "type:architecture" 2>/dev/null || echo "  ⚠️ Issue #14 erreur"
    gh issue edit 8 --add-label "documentation" 2>/dev/null || echo "  ⚠️ Issue #8 déjà labellé"
    
    echo "✅ Labels appliqués !"
}

# Création issues OntoWave
create_ontowave_issues() {
    echo
    echo "🌊 CRÉATION ISSUES ONTOWAVE :"
    echo "============================"
    
    echo "📝 Création issue principale OntoWave..."
    gh issue create \
        --title "[ONTOWAVE] Interface navigation MD sémantique ultra-légère" \
        --body "## 🎯 Objectif
Développer interface OntoWave pour navigation et visualisation des documents Markdown avec API plugins modulaire.

## 📋 Fonctionnalités
- [x] Architecture TypeScript/Vite ✅
- [x] Structure modulaire ✅  
- [x] Tests Playwright ✅
- [ ] Navigation sémantique MD
- [ ] API plugins
- [ ] Visualisation liens
- [ ] Intégration Panini

## 🔗 Liens
- Repository: https://github.com/stephanedenis/OntoWave
- Submodule: projects/ontowave/" \
        --label "project:ontowave" || echo "  ⚠️ Erreur création issue OntoWave"
    
    echo "✅ Issue OntoWave créée !"
}

# Mise à jour descriptions issues
update_issue_descriptions() {
    echo
    echo "📝 MISE À JOUR DESCRIPTIONS :"
    echo "============================"
    
    echo "🧪 Mise à jour issues Research..."
    # Exemple pour issue #13
    gh issue edit 13 --body "## 🧪 PROJECT: RESEARCH

Cette issue fait partie du **cœur de recherche Panini** (94M).

### 🎯 Contexte Architecture
- Module: \`research/\` (enrichi avec expérimentations)
- Focus: Atomes sémantiques évolutifs
- Priorité: HAUTE (cœur de travail)

### 📋 Tâches
- [ ] Multilinguisme avancé
- [ ] Base traducteurs
- [ ] Évolution sémantique

Voir: \`research/\` pour implémentation." 2>/dev/null || echo "  ⚠️ Issue #13 mise à jour échouée"
    
    echo "🗂️ Mise à jour issues Filesystem..."
    gh issue edit 11 --body "## 🗂️ PROJECT: FILESYSTEM

Cette issue fait partie du **système de fichiers sémantique** (3M épuré).

### 🎯 Contexte Architecture  
- Module: \`modules/core/filesystem/\` (nettoyé)
- Focus: FS sémantique pur
- Priorité: HAUTE (projet réel)

### 📋 Tâches
- [ ] Validateurs ingestion
- [ ] Restitution multi-format
- [ ] Interface FS sémantique

Voir: \`modules/core/filesystem/\` pour implémentation." 2>/dev/null || echo "  ⚠️ Issue #11 mise à jour échouée"
    
    echo "✅ Descriptions mises à jour !"
}

# Archivage issues legacy
archive_legacy_issues() {
    echo
    echo "📦 ARCHIVAGE ISSUES LEGACY :"
    echo "==========================="
    
    echo "📝 Mise à jour issues legacy (modules supprimés)..."
    
    # Issue #10 - Infrastructure autonomie (module supprimé)
    gh issue edit 10 --body "## 📦 LEGACY: MODULE SUPPRIMÉ

⚠️ **Ce module a été supprimé** lors de la refactorisation architecture 3 projets réels.

### 🎯 Statut
- Module \`modules/infrastructure/autonomous\` → **SUPPRIMÉ**
- Fonctionnalité → Peut être recréée si nécessaire dans \`research/\`
- Priorité → **BASSE** (scaffold éliminé)

### 🔄 Migration
Si cette fonctionnalité est encore nécessaire :
1. Analyser besoins réels
2. Intégrer dans \`research/\` ou créer outil dédié
3. Éviter dispersion architecturale" 2>/dev/null || echo "  ⚠️ Issue #10 archivage échoué"
    
    echo "✅ Issues legacy archivées !"
}

# Rapport final
generate_report() {
    echo
    echo "📊 RAPPORT ORGANISATION ISSUES :"
    echo "==============================="
    
    echo "✅ ORGANISATION ACCOMPLIE :"
    echo
    echo "🧪 RESEARCH (6 issues) :"
    echo "  #13, #12, #5, #3, #2, #1"
    echo
    echo "🗂️ FILESYSTEM (2 issues) :"
    echo "  #11, #4"
    echo
    echo "🌊 ONTOWAVE (1+ issues) :"
    echo "  Nouvelles issues créées"
    echo
    echo "📦 LEGACY/TOOLS (4 issues) :"
    echo "  #14, #10, #9, #8"
    echo
    echo "🎯 RÉSULTAT : Issues alignées avec architecture 3 projets réels !"
}

# Programme principal
main() {
    classify_issues
    
    echo
    echo "🤔 Voulez-vous appliquer cette organisation ?"
    echo "  1) Appliquer labels automatiquement"
    echo "  2) Créer issues OntoWave"  
    echo "  3) Mettre à jour descriptions"
    echo "  4) Archiver issues legacy"
    echo "  5) Tout faire automatiquement"
    echo "  6) Juste voir la classification"
    echo
    read -r -p "Votre choix (1-6): " choice
    
    case "$choice" in
        1) apply_labels ;;
        2) create_ontowave_issues ;;
        3) update_issue_descriptions ;;
        4) archive_legacy_issues ;;
        5) 
            apply_labels
            create_ontowave_issues
            update_issue_descriptions
            archive_legacy_issues
            generate_report
            ;;
        6) echo "✅ Classification affichée seulement" ;;
        *) echo "❌ Choix invalide" ;;
    esac
}

main