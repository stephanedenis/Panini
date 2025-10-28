#!/bin/bash

# 🔍 ANALYSE DES MODULES : CRÉÉS PAR UTILISATEUR vs GÉNÉRÉS
# Distinguer les vrais projets des modules de dépendance

echo "🔍 ANALYSE MODULES : UTILISATEUR vs GÉNÉRÉS"
echo "=========================================="
echo

WORKSPACE="/home/stephane/GitHub/Panini"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT="analyse_modules_utilisateur_${TIMESTAMP}.md"

cd "$WORKSPACE"

# Initialiser le rapport
echo "# 🔍 ANALYSE MODULES : UTILISATEUR vs GÉNÉRÉS" > "$REPORT"
echo "Date : $(date)" >> "$REPORT"
echo >> "$REPORT"

echo "## 🎯 OBJECTIF" >> "$REPORT"
echo "Distinguer les modules créés par l'utilisateur des modules générés automatiquement ou par dépendance." >> "$REPORT"
echo >> "$REPORT"

# Fonction pour analyser l'origine d'un module
analyze_module_origin() {
    local module_path="$1"
    local module_name=$(basename "$module_path")
    
    if [ ! -d "$module_path" ]; then
        return
    fi
    
    echo "🔍 Analyse origine : $module_name..."
    
    local indicators_user=""
    local indicators_generated=""
    local total_files=$(find "$module_path" -type f 2>/dev/null | wc -l)
    local py_files=$(find "$module_path" -name "*.py" 2>/dev/null | wc -l)
    local rs_files=$(find "$module_path" -name "*.rs" 2>/dev/null | wc -l)
    local md_files=$(find "$module_path" -name "*.md" 2>/dev/null | wc -l)
    local config_files=$(find "$module_path" -name "*.yml" -o -name "*.yaml" -o -name "*.json" 2>/dev/null | wc -l)
    local size=$(du -sh "$module_path" 2>/dev/null | cut -f1)
    
    echo "### 📦 MODULE : $module_name" >> "$REPORT"
    echo "**Taille** : $size | **Fichiers** : $total_files | **Python** : $py_files | **Rust** : $rs_files" >> "$REPORT"
    echo >> "$REPORT"
    
    # Indicateurs de création utilisateur
    if [ "$py_files" -gt 10 ] || [ "$rs_files" -gt 5 ]; then
        indicators_user="$indicators_user ✅ Code substantiel ($py_files Python, $rs_files Rust)"
    fi
    
    if find "$module_path" -name "*.py" -exec grep -l "def\|class" {} \; 2>/dev/null | head -1 | grep -q .; then
        indicators_user="$indicators_user ✅ Code fonctionnel (fonctions/classes)"
    fi
    
    if [ "$size" != "0" ] && [[ "$size" =~ M$ ]] && [[ ! "$size" =~ ^[0-9]K$ ]]; then
        indicators_user="$indicators_user ✅ Taille significative ($size)"
    fi
    
    # Chercher des imports spécifiques ou du code unique
    if find "$module_path" -name "*.py" -exec grep -l "import.*panini\|from.*panini\|dhatu\|semantic" {} \; 2>/dev/null | head -1 | grep -q .; then
        indicators_user="$indicators_user ✅ Imports spécifiques Panini"
    fi
    
    # Chercher des commits/historique
    if [ -d "$module_path/.git" ]; then
        indicators_user="$indicators_user ✅ Repository Git propre"
    fi
    
    # Indicateurs de génération automatique
    if [ "$total_files" -lt 10 ] && [ "$py_files" -eq 0 ] && [ "$rs_files" -eq 0 ]; then
        indicators_generated="$indicators_generated ⚠️ Très peu de contenu ($total_files fichiers)"
    fi
    
    if [ "$config_files" -gt 5 ] && [ "$py_files" -eq 0 ]; then
        indicators_generated="$indicators_generated ⚠️ Principalement configs GitHub"
    fi
    
    # Chercher des templates ou scaffolds
    if find "$module_path" -name "*template*" -o -name "*scaffold*" -o -name "*generated*" 2>/dev/null | head -1 | grep -q .; then
        indicators_generated="$indicators_generated ⚠️ Contient templates/scaffolds"
    fi
    
    # Chercher des README génériques
    if [ -f "$module_path/README.md" ]; then
        readme_lines=$(wc -l < "$module_path/README.md" 2>/dev/null || echo "0")
        if [ "$readme_lines" -lt 10 ]; then
            indicators_generated="$indicators_generated ⚠️ README très court ($readme_lines lignes)"
        fi
        
        if grep -q "module PaniniFS" "$module_path/README.md" 2>/dev/null; then
            indicators_generated="$indicators_generated ⚠️ README générique"
        fi
    fi
    
    # Évaluation finale
    echo "#### 🔍 Indicateurs d'origine" >> "$REPORT"
    echo >> "$REPORT"
    
    if [ -n "$indicators_user" ]; then
        echo "**CRÉÉ PAR UTILISATEUR** :" >> "$REPORT"
        echo "$indicators_user" | sed 's/✅/- ✅/g' >> "$REPORT"
        echo >> "$REPORT"
    fi
    
    if [ -n "$indicators_generated" ]; then
        echo "**POSSIBLEMENT GÉNÉRÉ** :" >> "$REPORT"
        echo "$indicators_generated" | sed 's/⚠️/- ⚠️/g' >> "$REPORT"
        echo >> "$REPORT"
    fi
    
    # Conclusion
    echo "#### 🎯 **ÉVALUATION** :" >> "$REPORT"
    if [[ -n "$indicators_user" && "$indicators_user" =~ ✅.*✅ ]]; then
        echo "**🟢 PROJET UTILISATEUR** - Contenu substantiel créé manuellement" >> "$REPORT"
        echo "  📦 $module_name" >> " modules_utilisateur.txt"
    elif [[ -n "$indicators_generated" && "$indicators_generated" =~ ⚠️.*⚠️ ]]; then
        echo "**🔴 MODULE GÉNÉRÉ** - Principalement scaffold/template" >> "$REPORT"
        echo "  📦 $module_name" >> "modules_generes.txt"
    else
        echo "**🟡 MIXTE** - À examiner manuellement" >> "$REPORT"
        echo "  📦 $module_name" >> "modules_mixtes.txt"
    fi
    
    echo >> "$REPORT"
    echo "---" >> "$REPORT"
    echo >> "$REPORT"
}

# Nettoyer les fichiers de sortie
rm -f modules_utilisateur.txt modules_generes.txt modules_mixtes.txt

echo "📊 ANALYSE PAR MODULE"
echo "===================="

# Analyser tous les modules
for module in modules/core/* modules/services/* modules/infrastructure/* modules/orchestration/* shared/*; do
    [ -d "$module" ] && analyze_module_origin "$module"
done

# Analyser research et ontowave si présents
[ -d "research" ] && analyze_module_origin "research"

# Vérifier si OntoWave peut être ajouté comme submodule
if [ -d "/home/stephane/GitHub/Panini-OntoWave" ]; then
    echo "📦 OntoWave détecté en dehors : /home/stephane/GitHub/Panini-OntoWave"
    echo "### 🌊 ONTOWAVE (Externe)" >> "$REPORT"
    echo "**Localisation** : /home/stephane/GitHub/Panini-OntoWave" >> "$REPORT"
    echo "**Status** : Projet utilisateur indépendant" >> "$REPORT"
    echo "**Action** : À ajouter comme submodule" >> "$REPORT"
    echo >> "$REPORT"
fi

# Résumé
echo >> "$REPORT"
echo "## 📊 RÉSUMÉ FINAL" >> "$REPORT"
echo >> "$REPORT"

echo "### 🟢 **PROJETS UTILISATEUR** (à conserver/développer)" >> "$REPORT"
if [ -f "modules_utilisateur.txt" ]; then
    cat modules_utilisateur.txt >> "$REPORT"
else
    echo "*(Aucun détecté automatiquement)*" >> "$REPORT"
fi
echo >> "$REPORT"

echo "### 🔴 **MODULES GÉNÉRÉS** (à fusionner/nettoyer)" >> "$REPORT"
if [ -f "modules_generes.txt" ]; then
    cat modules_generes.txt >> "$REPORT"
else
    echo "*(Aucun détecté automatiquement)*" >> "$REPORT"
fi
echo >> "$REPORT"

echo "### 🟡 **MODULES MIXTES** (à examiner)" >> "$REPORT"
if [ -f "modules_mixtes.txt" ]; then
    cat modules_mixtes.txt >> "$REPORT"
else
    echo "*(Aucun détecté automatiquement)*" >> "$REPORT"
fi
echo >> "$REPORT"

echo "### 🎯 **RECOMMANDATIONS ARCHITECTURALES**" >> "$REPORT"
echo >> "$REPORT"
echo "1. **CONSERVER** : Projets utilisateur comme modules principaux" >> "$REPORT"
echo "2. **FUSIONNER** : Modules générés en outils de soutien" >> "$REPORT"
echo "3. **EXAMINER** : Modules mixtes pour validation manuelle" >> "$REPORT"
echo "4. **AJOUTER** : OntoWave comme submodule indépendant" >> "$REPORT"
echo >> "$REPORT"

echo "✅ Analyse terminée ! Rapport : $REPORT"
echo
echo "📋 RÉSULTATS RAPIDES :"
echo "====================="

echo "🟢 PROJETS UTILISATEUR :"
[ -f "modules_utilisateur.txt" ] && cat modules_utilisateur.txt || echo "  (À déterminer manuellement)"

echo
echo "🔴 MODULES GÉNÉRÉS :"
[ -f "modules_generes.txt" ] && cat modules_generes.txt || echo "  (À déterminer manuellement)"

echo
echo "🌊 ONTOWAVE :"
if [ -d "/home/stephane/GitHub/Panini-OntoWave" ]; then
    echo "  ✅ Détecté - Prêt pour submodule"
else
    echo "  ❌ Non trouvé"
fi

echo
echo "📄 Rapport détaillé : $REPORT"