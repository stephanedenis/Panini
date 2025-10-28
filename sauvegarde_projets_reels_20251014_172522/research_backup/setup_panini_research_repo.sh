#!/bin/bash
# Script de configuration du dépôt Panini-Research
# Ce script :
# 1. Crée le dépôt GitHub Panini-Research
# 2. Configure le remote
# 3. Commit et push le contenu actuel
# 4. Configure comme submodule dans GitHub-Centralized

set -e

REPO_NAME="Panini-Research"
GITHUB_USER="stephanedenis"
PANINI_DIR="/home/stephane/GitHub/Panini-Research"
CENTRALIZED_DIR="/home/stephane/GitHub/GitHub-Centralized"

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  Configuration du dépôt Panini-Research                      ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Étape 1 : Créer le dépôt sur GitHub via gh CLI
echo "📦 Étape 1 : Création du dépôt GitHub ${REPO_NAME}..."
if command -v gh &> /dev/null; then
    cd "$PANINI_DIR"
    gh repo create "$REPO_NAME" \
        --public \
        --description "PaniniFS Research - Architecture de digestion universelle de fichiers avec grammaires formelles" \
        --source=. \
        --remote=origin \
        --push=false
    echo "✅ Dépôt créé sur GitHub"
else
    echo "⚠️  GitHub CLI (gh) non installé."
    echo "   Veuillez créer manuellement le dépôt sur github.com/${GITHUB_USER}/${REPO_NAME}"
    echo "   Puis exécuter la partie 2 de ce script."
    read -p "Appuyez sur Entrée après avoir créé le dépôt..."
fi

# Étape 2 : Configurer le remote (si pas déjà fait par gh)
echo ""
echo "🔗 Étape 2 : Configuration du remote origin..."
cd "$PANINI_DIR"
if ! git remote get-url origin &> /dev/null; then
    git remote add origin "git@github.com:${GITHUB_USER}/${REPO_NAME}.git"
fi
echo "✅ Remote configuré : git@github.com:${GITHUB_USER}/${REPO_NAME}.git"

# Étape 3 : Commit et push
echo ""
echo "💾 Étape 3 : Commit et push du contenu..."
cd "$PANINI_DIR"

# S'assurer qu'on est sur main
git branch -M main

# Ajouter tous les fichiers créés
git add .github/ \
    PANINI_UNIVERSAL_DIGESTION_ARCHITECTURE.md \
    SESSION_SUMMARY_20251003.md \
    audit_server_consolidation.py \
    panini_*.py \
    serveur_*.py \
    *.md \
    *.json \
    *.html \
    *.sh 2>/dev/null || true

# Commit
git commit -m "🎉 Session 2025-10-03: Architecture universelle + infrastructure

- Vision clarifiée: Digestion UNIVERSELLE de fichiers (binaire + texte)
- Architecture grammaires formelles (PDF, PNG, JPEG, ZIP, ELF)
- Infrastructure approbations GitHub Copilot (v2.1)
- Audit serveurs: 6 serveurs → consolidation vers port 5000
- Plan d'exécution 6 semaines
- Scripts validation, optimisation, monitoring
- Documentation complète (5 docs stratégiques, 5 scripts)

Livrables:
- PANINI_UNIVERSAL_DIGESTION_ARCHITECTURE.md (518 lignes)
- .github/DIRECTIVE_CONSOLIDATION_SERVEUR_UNIVERSEL.md (370 lignes)
- .github/DIRECTIVE_APPROBATIONS_COMMANDES.md (280 lignes)
- SESSION_SUMMARY_20251003.md (490 lignes)
- .github/README.md (410 lignes)
- 5 scripts d'infrastructure (~1,900 lignes)
- 2 rapports d'audit

Métriques:
- 33+ patterns configurés
- 79% taux d'approbation
- 3-7ms validation
- 12 auto-optimisations
- 26 endpoints catalogués
- 8 duplications identifiées" || true

# Push
echo "🚀 Push vers GitHub..."
git push -u origin main

echo ""
echo "✅ Dépôt Panini-Research créé et poussé sur GitHub"
echo "   URL: https://github.com/${GITHUB_USER}/${REPO_NAME}"

# Étape 4 : Ajouter comme submodule dans GitHub-Centralized
echo ""
echo "🔗 Étape 4 : Configuration comme submodule dans GitHub-Centralized..."

if [ -d "$CENTRALIZED_DIR" ]; then
    cd "$CENTRALIZED_DIR"
    
    # Créer le répertoire projects/panini s'il n'existe pas
    mkdir -p projects
    
    # Ajouter comme submodule
    if [ ! -d "projects/panini" ]; then
        git submodule add "git@github.com:${GITHUB_USER}/${REPO_NAME}.git" projects/panini
        echo "✅ Submodule ajouté à projects/panini"
    else
        echo "⚠️  Submodule déjà existant à projects/panini"
    fi
    
    # Commit dans GitHub-Centralized
    git add .gitmodules projects/panini 2>/dev/null || true
    git commit -m "➕ Ajout submodule Panini-Research dans projects/panini" || true
    
    echo ""
    echo "✅ Submodule configuré dans GitHub-Centralized"
    echo "   Path: projects/panini"
    echo "   Remote: git@github.com:${GITHUB_USER}/${REPO_NAME}.git"
else
    echo "⚠️  Répertoire GitHub-Centralized non trouvé à ${CENTRALIZED_DIR}"
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  🎉 Configuration terminée avec succès !                     ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Résumé:"
echo "  • Dépôt indépendant : https://github.com/${GITHUB_USER}/${REPO_NAME}"
echo "  • Submodule dans    : GitHub-Centralized/projects/panini"
echo "  • Remote origin     : git@github.com:${GITHUB_USER}/${REPO_NAME}.git"
echo ""
echo "🚀 Prochaines étapes:"
echo "  1. Vérifier sur GitHub: https://github.com/${GITHUB_USER}/${REPO_NAME}"
echo "  2. Cloner ailleurs avec: git clone --recurse-submodules \\
       git@github.com:${GITHUB_USER}/GitHub-Centralized.git"
echo ""
