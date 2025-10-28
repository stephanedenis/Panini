#!/bin/bash

# 🔍 ANALYSE DU CONTENU RÉEL DES MODULES
# Distinguer les placeholders des vrais résultats de calculs

echo "🔍 ANALYSE CONTENU RÉEL - VISION MÉTIER CLARIFIÉE"
echo "================================================"
echo

WORKSPACE="/home/stephane/GitHub/Panini"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT="analyse_contenu_reel_${TIMESTAMP}.md"

cd "$WORKSPACE"

# Initialiser le rapport
echo "# 🔍 ANALYSE DU CONTENU RÉEL DES MODULES" > "$REPORT"
echo "Date : $(date)" >> "$REPORT"
echo >> "$REPORT"
echo "## 🎯 VISION MÉTIER CLARIFIÉE" >> "$REPORT"
echo >> "$REPORT"
echo "### 🤖 **AGENTS & ORCHESTRATION**" >> "$REPORT"
echo "- **Nouveau nom** : \`agent-orchestrator\` (au lieu d'execution-orchestrator)" >> "$REPORT"
echo "- **Fusion** : colab + cloud + autonomous + reactive → gestion agents" >> "$REPORT"
echo "- **Copilotage** : Onboarding IA, règles, politiques, scripts communs" >> "$REPORT"
echo >> "$REPORT"
echo "### 🗂️ **PANINI-FS = VRAI FILESYSTEM**" >> "$REPORT"
echo "- **Type** : Filesystem virtuel (comme ZFS/BTRFS)" >> "$REPORT"
echo "- **Montage** : FS + WebDAV" >> "$REPORT"
echo "- **Backend** : Git repos (public/groupe/privé)" >> "$REPORT"
echo "- **Focus** : Sémantique + propriété + droits + attributions" >> "$REPORT"
echo >> "$REPORT"
echo "### 🧪 **DISTINCTION PLACEHOLDERS vs RÉSULTATS**" >> "$REPORT"
echo "- **Recherche** : Calculs intensifs éparpillés" >> "$REPORT"
echo "- **Expérimentations** : À regrouper dans research/" >> "$REPORT"
echo >> "$REPORT"

# Fonction pour analyser le contenu d'un module
analyze_module_content() {
    local module_path="$1"
    local module_name=$(basename "$module_path")
    
    if [ ! -d "$module_path" ]; then
        return
    fi
    
    echo "🔍 Analyse : $module_name..."
    
    echo "## 📦 MODULE : $module_name" >> "$REPORT"
    echo >> "$REPORT"
    
    # Statistiques de base
    local total_files=$(find "$module_path" -type f 2>/dev/null | wc -l)
    local py_files=$(find "$module_path" -name "*.py" 2>/dev/null | wc -l)
    local rs_files=$(find "$module_path" -name "*.rs" 2>/dev/null | wc -l)
    local json_files=$(find "$module_path" -name "*.json" 2>/dev/null | wc -l)
    local md_files=$(find "$module_path" -name "*.md" 2>/dev/null | wc -l)
    local size=$(du -sh "$module_path" 2>/dev/null | cut -f1)
    
    echo "### 📊 Statistiques" >> "$REPORT"
    echo "- **Taille** : $size" >> "$REPORT"
    echo "- **Fichiers total** : $total_files" >> "$REPORT"
    echo "- **Python** : $py_files fichiers" >> "$REPORT"
    echo "- **Rust** : $rs_files fichiers" >> "$REPORT"
    echo "- **JSON** : $json_files fichiers" >> "$REPORT"
    echo "- **Markdown** : $md_files fichiers" >> "$REPORT"
    echo >> "$REPORT"
    
    # Analyser les types de contenu
    echo "### 🔍 Types de contenu détectés" >> "$REPORT"
    echo >> "$REPORT"
    
    # Chercher des résultats de calculs
    local calc_results=$(find "$module_path" -name "*.json" -o -name "*result*" -o -name "*output*" -o -name "*analysis*" 2>/dev/null | wc -l)
    if [ "$calc_results" -gt 0 ]; then
        echo "#### 🧮 **RÉSULTATS DE CALCULS** ($calc_results fichiers)" >> "$REPORT"
        find "$module_path" -name "*.json" -o -name "*result*" -o -name "*output*" -o -name "*analysis*" 2>/dev/null | head -10 | while read file; do
            file_size=$(du -sh "$file" 2>/dev/null | cut -f1)
            echo "- \`$(basename "$file")\` ($file_size)" >> "$REPORT"
        done
        echo >> "$REPORT"
    fi
    
    # Chercher du code réel
    if [ "$py_files" -gt 0 ] || [ "$rs_files" -gt 0 ]; then
        echo "#### 💻 **CODE RÉEL**" >> "$REPORT"
        if [ "$py_files" -gt 0 ]; then
            # Analyser la complexité du code Python
            local py_lines=$(find "$module_path" -name "*.py" -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print $1}')
            echo "- **Python** : $py_files fichiers, $py_lines lignes" >> "$REPORT"
            
            # Chercher des fonctions/classes importantes
            grep -r "^class\|^def " "$module_path" --include="*.py" 2>/dev/null | head -5 | while read line; do
                echo "  - \`$(echo "$line" | cut -d: -f2 | xargs)\`" >> "$REPORT"
            done
        fi
        
        if [ "$rs_files" -gt 0 ]; then
            local rs_lines=$(find "$module_path" -name "*.rs" -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print $1}')
            echo "- **Rust** : $rs_files fichiers, $rs_lines lignes" >> "$REPORT"
        fi
        echo >> "$REPORT"
    fi
    
    # Chercher des configurations/templates
    local config_files=$(find "$module_path" -name "*.yml" -o -name "*.yaml" -o -name "*.toml" -o -name "*.cfg" 2>/dev/null | wc -l)
    if [ "$config_files" -gt 0 ]; then
        echo "#### ⚙️ **CONFIGURATIONS** ($config_files fichiers)" >> "$REPORT"
        find "$module_path" -name "*.yml" -o -name "*.yaml" -o -name "*.toml" -o -name "*.cfg" 2>/dev/null | head -5 | while read file; do
            echo "- \`$(basename "$file")\`" >> "$REPORT"
        done
        echo >> "$REPORT"
    fi
    
    # Identifier si c'est un placeholder ou du contenu réel
    echo "### 🎯 **STATUT ÉVALUÉ**" >> "$REPORT"
    
    if [ "$total_files" -lt 5 ]; then
        echo "- 🚨 **PLACEHOLDER** : Très peu de fichiers" >> "$REPORT"
    elif [ "$py_files" -eq 0 ] && [ "$rs_files" -eq 0 ] && [ "$json_files" -eq 0 ]; then
        echo "- ⚠️ **SCAFFOLD** : Principalement docs/configs" >> "$REPORT"
    elif [ "$calc_results" -gt 5 ] || [ "$py_files" -gt 10 ]; then
        echo "- ✅ **CONTENU RÉEL** : Code et/ou résultats significatifs" >> "$REPORT"
    else
        echo "- 🔄 **MIXTE** : Contenu partiel, à évaluer" >> "$REPORT"
    fi
    
    echo >> "$REPORT"
    echo "---" >> "$REPORT"
    echo >> "$REPORT"
}

# Analyser chaque module
echo "📊 ANALYSE DU CONTENU PAR MODULE"
echo "================================"

# Modules core
for module in modules/core/*; do
    [ -d "$module" ] && analyze_module_content "$module"
done

# Modules services
for module in modules/services/*; do
    [ -d "$module" ] && analyze_module_content "$module"
done

# Modules infrastructure
for module in modules/infrastructure/*; do
    [ -d "$module" ] && analyze_module_content "$module"
done

# Modules orchestration
for module in modules/orchestration/*; do
    [ -d "$module" ] && analyze_module_content "$module"
done

# Shared
for module in shared/*; do
    [ -d "$module" ] && analyze_module_content "$module"
done

# Research
if [ -d "research" ]; then
    analyze_module_content "research"
fi

# Analyse spéciale de Panini-FS (recherche de contenu éparpillé)
analyze_filesystem_content() {
    echo "## 🗂️ ANALYSE SPÉCIALE : PANINI-FS" >> "$REPORT"
    echo >> "$REPORT"
    
    if [ -d "modules/core/filesystem" ]; then
        echo "### 🔍 Recherche de calculs éparpillés dans Panini-FS" >> "$REPORT"
        echo >> "$REPORT"
        
        # Chercher des fichiers de résultats volumineux
        echo "#### 📈 **GROS FICHIERS** (possibles résultats de calculs)" >> "$REPORT"
        find modules/core/filesystem -type f -size +1M 2>/dev/null | head -10 | while read file; do
            size=$(du -sh "$file" | cut -f1)
            echo "- \`$file\` ($size)" >> "$REPORT"
        done
        echo >> "$REPORT"
        
        # Chercher des répertoires suspects
        echo "#### 📂 **RÉPERTOIRES VOLUMINEUX**" >> "$REPORT"
        du -sh modules/core/filesystem/* 2>/dev/null | sort -hr | head -10 | while read size path; do
            echo "- \`$path\` ($size)" >> "$REPORT"
        done
        echo >> "$REPORT"
        
        # Chercher des patterns de recherche
        echo "#### 🧪 **TRACES D'EXPÉRIMENTATIONS**" >> "$REPORT"
        find modules/core/filesystem -name "*experiment*" -o -name "*test*" -o -name "*analysis*" -o -name "*research*" 2>/dev/null | head -10 | while read file; do
            echo "- \`$file\`" >> "$REPORT"
        done
        echo >> "$REPORT"
    fi
}

echo "🗂️ Analyse spéciale Panini-FS..."
analyze_filesystem_content

# Synthèse et recommandations
echo "## 🎯 SYNTHÈSE ET RECOMMANDATIONS" >> "$REPORT"
echo >> "$REPORT"

echo "### 📋 **MODULES PAR CATÉGORIE**" >> "$REPORT"
echo >> "$REPORT"

echo "#### 🤖 **ORCHESTRATION AGENTS** (à fusionner)" >> "$REPORT"
echo "- \`colab\` → driver local CoLab" >> "$REPORT"
echo "- \`cloud\` → driver cloud" >> "$REPORT"
echo "- \`autonomous\` → missions autonomes" >> "$REPORT"
echo "- \`reactive\` → monitoring/réactivité" >> "$REPORT"
echo "- **→ Nouveau nom** : \`agent-orchestrator\`" >> "$REPORT"
echo >> "$REPORT"

echo "#### 🗂️ **FILESYSTEM SÉMANTIQUE** (à nettoyer)" >> "$REPORT"
echo "- \`filesystem\` → vrai FS virtuel + WebDAV" >> "$REPORT"
echo "- **À faire** : Extraire expérimentations → research/" >> "$REPORT"
echo "- **Focus** : FS + sémantique + droits/attributions" >> "$REPORT"
echo >> "$REPORT"

echo "#### 🧠 **SÉMANTIQUE CORE**" >> "$REPORT"
echo "- \`semantic\` → extraction dhātu, hypergraphes" >> "$REPORT"
echo "- **Status** : À évaluer selon contenu" >> "$REPORT"
echo >> "$REPORT"

echo "#### 🛠️ **OUTILLAGE IA** (à regrouper)" >> "$REPORT"
echo "- \`copilotage\` → onboarding IA, règles, scripts" >> "$REPORT"
echo "- \`attribution\` → propriété/citations" >> "$REPORT"
echo "- \`speckit\` → templates/spécifications" >> "$REPORT"
echo "- **→ Nouveau nom** : \`ai-tooling\`" >> "$REPORT"
echo >> "$REPORT"

echo "#### 📚 **SERVICES APPLICATIFS**" >> "$REPORT"
echo "- \`datasets\` → ingestion données" >> "$REPORT"
echo "- \`publication\` → exports Medium/Leanpub" >> "$REPORT"
echo "- **Status** : À évaluer selon contenu" >> "$REPORT"
echo >> "$REPORT"

echo "#### 🧪 **RECHERCHE**" >> "$REPORT"
echo "- \`research\` → expérimentations pures" >> "$REPORT"
echo "- **À faire** : Centraliser les expérimentations éparpillées" >> "$REPORT"
echo >> "$REPORT"

echo "### 🎯 **ARCHITECTURE CIBLE PROPOSÉE**" >> "$REPORT"
echo >> "$REPORT"
echo "1. **\`panini-filesystem\`** : FS virtuel + WebDAV + sémantique" >> "$REPORT"
echo "2. **\`agent-orchestrator\`** : Gestion agents (colab+cloud+autonomous+reactive)" >> "$REPORT"
echo "3. **\`semantic-core\`** : Extraction dhātu + hypergraphes" >> "$REPORT"
echo "4. **\`ai-tooling\`** : Copilotage + attribution + speckit" >> "$REPORT"
echo "5. **\`application-services\`** : Datasets + publication" >> "$REPORT"
echo "6. **\`research\`** : Expérimentations centralisées" >> "$REPORT"
echo >> "$REPORT"

echo "✅ Analyse terminée ! Rapport : $REPORT"
echo
echo "📋 PROCHAINES ÉTAPES :"
echo "1. Consulter le rapport détaillé"
echo "2. Valider l'architecture cible"
echo "3. Créer le plan de migration"
echo
echo "🚀 Rapport disponible : $REPORT"