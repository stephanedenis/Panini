#!/bin/bash

# 🔍 AUDIT COMPLET ÉCOSYSTÈME GITHUB PANINI
# Analyse des repositories, issues, projets, branches, etc.

echo "🔍 AUDIT COMPLET ÉCOSYSTÈME GITHUB PANINI"
echo "========================================"
echo

WORKSPACE="/home/stephane/GitHub/Panini"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
AUDIT_FILE="$WORKSPACE/audit_github_ecosystem_${TIMESTAMP}.md"

cd "$WORKSPACE"

# Initialiser le rapport
init_report() {
    cat > "$AUDIT_FILE" << 'EOF'
# 🔍 AUDIT ÉCOSYSTÈME GITHUB PANINI

**Date :** $(date)
**Objectif :** État complet des repositories, issues, projets GitHub

## 📊 RÉSUMÉ EXÉCUTIF

### 🎯 Repositories Actifs
### 📋 Issues & Tâches  
### 🚀 Projets GitHub
### 🌿 État Branches
### 🔗 Submodules

---

EOF
}

# Analyser les repositories locaux
analyze_local_repos() {
    echo "📁 ANALYSE REPOSITORIES LOCAUX"
    echo "=============================="
    
    cat >> "$AUDIT_FILE" << 'EOF'
## 📁 REPOSITORIES LOCAUX

EOF
    
    # Panini principal
    echo "🎯 Repository principal : Panini"
    echo "  📍 Chemin : $(pwd)"
    echo "  🌿 Branche : $(git branch --show-current 2>/dev/null || echo 'N/A')"
    echo "  📊 Commits : $(git rev-list --count HEAD 2>/dev/null || echo 'N/A')"
    echo "  📝 Dernier commit : $(git log -1 --format='%h - %s (%cr)' 2>/dev/null || echo 'N/A')"
    
    cat >> "$AUDIT_FILE" << EOF
### 🎯 Panini (Principal)
- **Chemin :** $(pwd)
- **Branche :** $(git branch --show-current 2>/dev/null || echo 'N/A')
- **Commits :** $(git rev-list --count HEAD 2>/dev/null || echo 'N/A')
- **Dernier commit :** $(git log -1 --format='%h - %s (%cr)' 2>/dev/null || echo 'N/A')
- **Status :** $(git status --porcelain | wc -l) fichiers modifiés

EOF
    
    # Submodules configurés
    echo
    echo "🔗 Submodules configurés :"
    if [ -f ".gitmodules" ]; then
        while IFS= read -r line; do
            if [[ $line =~ ^\[submodule ]]; then
                submodule_name=$(echo "$line" | sed 's/\[submodule "\(.*\)"\]/\1/')
                echo "  📦 $submodule_name"
            elif [[ $line =~ ^[[:space:]]*path ]]; then
                submodule_path=$(echo "$line" | sed 's/.*= *//')
                echo "    📍 Chemin : $submodule_path"
                
                if [ -d "$submodule_path" ]; then
                    cd "$submodule_path"
                    local_branch=$(git branch --show-current 2>/dev/null || echo 'N/A')
                    local_commits=$(git rev-list --count HEAD 2>/dev/null || echo 'N/A')
                    echo "    🌿 Branche : $local_branch"
                    echo "    📊 Commits : $local_commits"
                    
                    cat >> "$AUDIT_FILE" << EOF
### 📦 $submodule_name
- **Chemin :** $submodule_path
- **Branche :** $local_branch
- **Commits :** $local_commits
- **État :** $([ -d .git ] && echo "Initialisé" || echo "Non initialisé")

EOF
                    cd "$WORKSPACE"
                else
                    echo "    ❌ Pas initialisé"
                    cat >> "$AUDIT_FILE" << EOF
### 📦 $submodule_name
- **Chemin :** $submodule_path
- **État :** ❌ Non initialisé

EOF
                fi
            fi
        done < .gitmodules
    else
        echo "  ⚠️ Aucun .gitmodules trouvé"
    fi
}

# Vérifier les repositories distants
check_remote_repos() {
    echo
    echo "🌐 REPOSITORIES DISTANTS GITHUB"
    echo "==============================="
    
    cat >> "$AUDIT_FILE" << 'EOF'
## 🌐 REPOSITORIES DISTANTS

EOF
    
    # Liste des repos Panini connus
    local repos=(
        "Panini"
        "Panini-OntoWave"
        "Panini-research"
        "Panini-filesystem"
        "Panini-semantic"
        "Panini-colab"
        "Panini-publication"
        "Panini-autonomous"
        "Panini-reactive"
        "Panini-cloud"
        "Panini-copilotage"
        "Panini-datasets"
        "Panini-execution"
        "Panini-attribution"
        "Panini-speckit"
    )
    
    echo "🔍 Vérification des repositories GitHub..."
    
    for repo in "${repos[@]}"; do
        echo "  🔍 Vérification : $repo"
        
        # Utiliser gh CLI si disponible, sinon curl
        if command -v gh &> /dev/null; then
            repo_info=$(gh repo view "stephanedenis/$repo" --json name,description,isPrivate,pushedAt,issues,pullRequests 2>/dev/null)
            if [ $? -eq 0 ]; then
                echo "    ✅ Trouvé sur GitHub"
                
                # Extraire les informations
                is_private=$(echo "$repo_info" | jq -r '.isPrivate // "N/A"')
                last_push=$(echo "$repo_info" | jq -r '.pushedAt // "N/A"')
                open_issues=$(echo "$repo_info" | jq -r '.issues.totalCount // "N/A"')
                open_prs=$(echo "$repo_info" | jq -r '.pullRequests.totalCount // "N/A"')
                description=$(echo "$repo_info" | jq -r '.description // "Pas de description"')
                
                echo "    📝 Description : $description"
                echo "    🔒 Privé : $is_private"
                echo "    📅 Dernier push : $last_push"
                echo "    📋 Issues ouvertes : $open_issues"
                echo "    🔄 PR ouvertes : $open_prs"
                
                cat >> "$AUDIT_FILE" << EOF
### ✅ $repo
- **Status :** Actif sur GitHub
- **Description :** $description
- **Privé :** $is_private
- **Dernier push :** $last_push
- **Issues ouvertes :** $open_issues
- **PR ouvertes :** $open_prs

EOF
            else
                echo "    ❌ Non trouvé ou inaccessible"
                cat >> "$AUDIT_FILE" << EOF
### ❌ $repo
- **Status :** Non trouvé ou inaccessible

EOF
            fi
        else
            echo "    ⚠️ GitHub CLI non disponible - vérification limitée"
            cat >> "$AUDIT_FILE" << EOF
### ⚠️ $repo
- **Status :** Vérification limitée (GitHub CLI non disponible)

EOF
        fi
    done
}

# Analyser les issues et projets
analyze_github_management() {
    echo
    echo "📋 GESTION GITHUB (Issues/Projets)"
    echo "================================="
    
    cat >> "$AUDIT_FILE" << 'EOF'
## 📋 GESTION GITHUB

EOF
    
    if command -v gh &> /dev/null; then
        echo "🔍 Analyse des issues GitHub..."
        
        # Issues du repository principal
        echo "📋 Issues Panini principal :"
        gh issue list --repo stephanedenis/Panini --limit 20 --json number,title,state,labels,assignees,createdAt 2>/dev/null | jq -r '.[] | "  #\(.number) - \(.title) [\(.state)]"' || echo "  ⚠️ Aucune issue ou erreur d'accès"
        
        cat >> "$AUDIT_FILE" << 'EOF'
### 📋 Issues Panini Principal

EOF
        gh issue list --repo stephanedenis/Panini --limit 20 --json number,title,state,labels,assignees,createdAt 2>/dev/null | jq -r '.[] | "- **#\(.number)** - \(.title) `[\(.state)]`"' >> "$AUDIT_FILE" || echo "- ⚠️ Aucune issue accessible" >> "$AUDIT_FILE"
        
        # Vérifier les projets GitHub
        echo
        echo "🚀 Projets GitHub :"
        gh project list --owner stephanedenis 2>/dev/null | head -10 || echo "  ⚠️ Aucun projet ou erreur d'accès"
        
        cat >> "$AUDIT_FILE" << 'EOF'

### 🚀 Projets GitHub

EOF
        gh project list --owner stephanedenis --format json 2>/dev/null | jq -r '.projects[]? | "- **\(.title)** - \(.description // "Pas de description")"' >> "$AUDIT_FILE" || echo "- ⚠️ Aucun projet accessible" >> "$AUDIT_FILE"
        
    else
        echo "⚠️ GitHub CLI non disponible"
        echo "   Pour une analyse complète, installez : apt install gh"
        
        cat >> "$AUDIT_FILE" << 'EOF'
### ⚠️ GitHub CLI Non Disponible
Pour une analyse complète des issues et projets, installez GitHub CLI :
```bash
sudo apt install gh
gh auth login
```
EOF
    fi
}

# Analyser l'état des branches
analyze_branches() {
    echo
    echo "🌿 ÉTAT DES BRANCHES"
    echo "==================="
    
    cat >> "$AUDIT_FILE" << 'EOF'
## 🌿 ÉTAT DES BRANCHES

EOF
    
    echo "🌿 Branches locales Panini principal :"
    git branch -v
    
    cat >> "$AUDIT_FILE" << 'EOF'
### 🌿 Panini Principal
```
EOF
    git branch -v >> "$AUDIT_FILE"
    echo '```' >> "$AUDIT_FILE"
    
    echo
    echo "🔄 État synchronisation avec remote :"
    git remote -v
    git status
    
    cat >> "$AUDIT_FILE" << 'EOF'

### 🔄 Synchronisation Remote
```
EOF
    git remote -v >> "$AUDIT_FILE"
    echo "" >> "$AUDIT_FILE"
    git status >> "$AUDIT_FILE"
    echo '```' >> "$AUDIT_FILE"
}

# Recommandations
generate_recommendations() {
    echo
    echo "💡 GÉNÉRATION RECOMMANDATIONS"
    echo "============================="
    
    cat >> "$AUDIT_FILE" << 'EOF'

## 💡 RECOMMANDATIONS

### 🎯 Actions Prioritaires

#### 📋 Gestion Issues
- [ ] Créer/réviser les issues principales pour les 3 projets réels
- [ ] Organiser les issues par labels (research, filesystem, ontowave)
- [ ] Définir les milestones pour les prochaines versions

#### 🚀 Projets GitHub
- [ ] Créer un projet GitHub "Écosystème Panini" 
- [ ] Organiser les tâches par colonnes (À faire, En cours, Terminé)
- [ ] Lier les issues aux cartes du projet

#### 🔗 Submodules
- [ ] Initialiser les submodules non-initialisés
- [ ] Vérifier la synchronisation avec les remotes
- [ ] Nettoyer les submodules obsolètes

#### 📊 Monitoring
- [ ] Configurer des webhooks pour le suivi automatique
- [ ] Mettre en place des actions GitHub pour CI/CD
- [ ] Organiser les releases et tags

### 🛠️ Outils Recommandés

#### GitHub CLI
```bash
# Installation
sudo apt install gh
gh auth login

# Utilisation
gh issue create --title "Titre" --body "Description"
gh project create --title "Nom du projet"
```

#### Scripts d'automatisation
- Créer des scripts pour synchroniser les submodules
- Automatiser la création d'issues récurrentes
- Mettre en place des rapports de progression automatiques

EOF
}

# Fonction principale
main() {
    echo "🎯 OBJECTIF : Audit complet de l'écosystème GitHub Panini"
    echo "📋 ANALYSE : Repositories, Issues, Projets, Branches"
    echo
    
    # Initialiser le rapport
    init_report
    
    # Analyses
    analyze_local_repos
    check_remote_repos
    analyze_github_management
    analyze_branches
    generate_recommendations
    
    # Finaliser le rapport
    echo
    echo "📊 AUDIT TERMINÉ !"
    echo "=================="
    echo "📄 Rapport complet : $AUDIT_FILE"
    echo
    echo "📋 RÉSUMÉ RAPIDE :"
    
    # Compter les éléments
    local total_repos=$(grep -c "^###" "$AUDIT_FILE" 2>/dev/null || echo "0")
    local active_repos=$(grep -c "✅" "$AUDIT_FILE" 2>/dev/null || echo "0")
    local issues_count=$(grep -c "^- \*\*#" "$AUDIT_FILE" 2>/dev/null || echo "0")
    
    echo "  🎯 Repositories analysés : $total_repos"
    echo "  ✅ Repositories actifs : $active_repos"
    echo "  📋 Issues détectées : $issues_count"
    
    if [ -f ".gitmodules" ]; then
        local submodules_count=$(grep -c "^\[submodule" .gitmodules)
        echo "  🔗 Submodules configurés : $submodules_count"
    fi
    
    echo
    echo "🔍 Consultez le rapport détaillé pour les recommandations !"
    echo "📖 Fichier : $AUDIT_FILE"
}

# Installation GitHub CLI si nécessaire
check_github_cli() {
    echo "🔧 VÉRIFICATION OUTILS"
    echo "======================"
    
    if ! command -v gh &> /dev/null; then
        echo "⚠️ GitHub CLI non installé"
        echo "💡 Pour une analyse complète, voulez-vous l'installer ?"
        echo "   (Recommandé pour accéder aux issues et projets GitHub)"
        echo
        read -r -p "Installer GitHub CLI ? (y/N): " install_gh
        
        if [[ "$install_gh" =~ ^[Yy]$ ]]; then
            echo "📦 Installation GitHub CLI..."
            if command -v apt &> /dev/null; then
                sudo apt update && sudo apt install -y gh
            elif command -v brew &> /dev/null; then
                brew install gh
            else
                echo "❌ Gestionnaire de paquets non supporté"
                echo "   Installez manuellement : https://cli.github.com/"
            fi
            
            if command -v gh &> /dev/null; then
                echo "✅ GitHub CLI installé !"
                echo "🔐 Authentification requise..."
                gh auth login
            fi
        else
            echo "⏭️ Installation reportée - analyse limitée"
        fi
    else
        echo "✅ GitHub CLI disponible"
        
        # Vérifier l'authentification
        if ! gh auth status &> /dev/null; then
            echo "🔐 Authentification GitHub requise..."
            gh auth login
        else
            echo "✅ Authentifié sur GitHub"
        fi
    fi
    
    echo
}

# Lancement avec vérification des outils
check_github_cli
main