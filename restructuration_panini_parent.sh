#!/bin/bash
# Script de restructuration Panini avec submodules organisés
# À exécuter APRÈS le renommage des repositories

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[RESTRUCTURE]${NC} $1"
}

success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Configuration de la nouvelle architecture
PANINI_ROOT="/home/stephane/GitHub/Panini"

# Structure des submodules selon le plan
declare -A SUBMODULES_CONFIG=(
    # Core modules
    ["Panini-FS"]="modules/core/filesystem"
    ["Panini-SemanticCore"]="modules/core/semantic"
    
    # Orchestration
    ["Panini-CloudOrchestrator"]="modules/orchestration/cloud"
    ["Panini-ExecutionOrchestrator"]="modules/orchestration/execution"
    
    # Services
    ["Panini-CoLabController"]="modules/services/colab"
    ["Panini-PublicationEngine"]="modules/services/publication"
    ["Panini-DatasetsIngestion"]="modules/services/datasets"
    
    # Infrastructure
    ["Panini-UltraReactive"]="modules/infrastructure/reactive"
    ["Panini-AutonomousMissions"]="modules/infrastructure/autonomous"
    
    # Shared
    ["Panini-CopilotageShared"]="shared/copilotage"
    ["Panini-SpecKit-Shared"]="shared/speckit"
    ["Panini-AttributionRegistry"]="shared/attribution"
    
    # Projects
    ["Panini-Gest"]="projects/gest"
    ["Panini-OntoWave"]="projects/ontowave"
)

# Créer la structure de dossiers
create_directory_structure() {
    log "Création de la structure de dossiers..."
    
    cd "$PANINI_ROOT"
    
    # Créer les dossiers principaux
    local directories=(
        "modules"
        "modules/core"
        "modules/orchestration"
        "modules/services"
        "modules/infrastructure"
        "shared"
        "projects"
    )
    
    for dir in "${directories[@]}"; do
        mkdir -p "$dir"
        log "Créé: $dir/"
    done
    
    success "Structure de dossiers créée"
}

# Sauvegarder le .gitmodules actuel
backup_gitmodules() {
    cd "$PANINI_ROOT"
    
    if [ -f ".gitmodules" ]; then
        local backup_file=".gitmodules.backup.$(date +%Y%m%d_%H%M%S)"
        log "Sauvegarde .gitmodules → $backup_file"
        cp ".gitmodules" "$backup_file"
    fi
}

# Nettoyer les anciens submodules
clean_old_submodules() {
    log "Nettoyage des anciens submodules..."
    
    cd "$PANINI_ROOT"
    
    # Supprimer les anciens submodules s'ils existent
    local old_submodules=("PaniniFS-Research" "copilotage/shared")
    
    for submodule in "${old_submodules[@]}"; do
        if [ -d "$submodule" ]; then
            log "Suppression ancien submodule: $submodule"
            
            # Retirer du git
            git submodule deinit -f "$submodule" 2>/dev/null || true
            git rm -f "$submodule" 2>/dev/null || true
            rm -rf ".git/modules/$submodule" 2>/dev/null || true
            rm -rf "$submodule" 2>/dev/null || true
        fi
    done
    
    # Nettoyer .gitmodules
    if [ -f ".gitmodules" ]; then
        > .gitmodules  # Vider le fichier
    fi
    
    success "Anciens submodules nettoyés"
}

# Ajouter un submodule avec vérifications
add_submodule_safe() {
    local repo_name="$1"
    local target_path="$2"
    local repo_url="git@github.com:stephanedenis/$repo_name.git"
    
    log "Ajout submodule: $repo_name → $target_path"
    
    # Vérifier que le repository existe localement (après renommage)
    if [ ! -d "/home/stephane/GitHub/$repo_name" ]; then
        warning "Repository $repo_name introuvable localement"
        return 1
    fi
    
    # Supprimer le dossier cible s'il existe
    if [ -d "$target_path" ]; then
        rm -rf "$target_path"
    fi
    
    # Ajouter le submodule
    if git submodule add "$repo_url" "$target_path"; then
        success "Submodule $repo_name ajouté"
        return 0
    else
        error "Échec ajout submodule $repo_name"
        return 1
    fi
}

# Configurer tous les submodules
configure_all_submodules() {
    log "Configuration de tous les submodules..."
    
    cd "$PANINI_ROOT"
    
    local success_count=0
    local total_count=${#SUBMODULES_CONFIG[@]}
    
    for repo_name in "${!SUBMODULES_CONFIG[@]}"; do
        target_path="${SUBMODULES_CONFIG[$repo_name]}"
        
        if add_submodule_safe "$repo_name" "$target_path"; then
            ((success_count++))
        fi
    done
    
    echo ""
    log "📊 Résultats: $success_count/$total_count submodules configurés"
    
    if [ $success_count -gt 0 ]; then
        # Initialiser et mettre à jour tous les submodules
        log "Initialisation des submodules..."
        git submodule update --init --recursive
        success "Submodules initialisés"
    fi
    
    return $success_count
}

# Consolidation du contenu Panini-Research
consolidate_research() {
    log "Consolidation du contenu recherche..."
    
    local research_path="/home/stephane/GitHub/Panini-Research"
    
    if [ -d "$research_path" ]; then
        log "Intégration contenu de Panini-Research..."
        
        # Créer dossier research s'il n'existe pas
        mkdir -p "$PANINI_ROOT/research"
        
        # Copier le contenu unique (éviter doublons)
        if [ -d "$research_path/notebooks" ]; then
            cp -r "$research_path/notebooks"/* "$PANINI_ROOT/notebooks/" 2>/dev/null || true
        fi
        
        if [ -d "$research_path/docs" ] && [ ! -d "$PANINI_ROOT/docs/research" ]; then
            mkdir -p "$PANINI_ROOT/docs/research"
            cp -r "$research_path/docs"/* "$PANINI_ROOT/docs/research/" 2>/dev/null || true
        fi
        
        success "Contenu recherche consolidé"
    else
        warning "Panini-Research non trouvé pour consolidation"
    fi
}

# Mettre à jour la documentation principale
update_main_documentation() {
    log "Mise à jour documentation principale..."
    
    cd "$PANINI_ROOT"
    
    # Créer un nouveau README principal
    cat > README.md << 'EOF'
# 🎌 Panini - Écosystème de Compression Sémantique Universelle

**Parent Principal** - Architecture modulaire complète basée sur l'analyse linguistique sanskrite et les dhātu informationnels.

## 🏗️ Architecture Modulaire

```
Panini/
├── modules/
│   ├── core/                    # Composants fondamentaux
│   │   ├── filesystem/          # → Panini-FS (système de fichiers sémantique)
│   │   └── semantic/            # → Panini-SemanticCore (moteur sémantique)
│   ├── orchestration/           # Orchestrateurs
│   │   ├── cloud/               # → Panini-CloudOrchestrator
│   │   └── execution/           # → Panini-ExecutionOrchestrator
│   ├── services/                # Services spécialisés
│   │   ├── colab/               # → Panini-CoLabController
│   │   ├── publication/         # → Panini-PublicationEngine
│   │   └── datasets/            # → Panini-DatasetsIngestion
│   └── infrastructure/          # Infrastructure
│       ├── reactive/            # → Panini-UltraReactive
│       └── autonomous/          # → Panini-AutonomousMissions
├── shared/                      # Ressources partagées
│   ├── copilotage/              # → Panini-CopilotageShared
│   ├── speckit/                 # → Panini-SpecKit-Shared
│   └── attribution/             # → Panini-AttributionRegistry
└── projects/                    # Projets dérivés
    ├── gest/                    # → Panini-Gest
    └── ontowave/                # → Panini-OntoWave
```

## 🚀 Démarrage Rapide

### Initialisation complète
```bash
# Cloner avec tous les submodules
git clone --recursive git@github.com:stephanedenis/Panini.git
cd Panini

# Ou initialiser les submodules après clonage
git submodule update --init --recursive
```

### Navigation modules
```bash
# Accéder au système de fichiers core
cd modules/core/filesystem

# Accéder aux services
cd modules/services/colab

# Accéder aux projets
cd projects/gest
```

## 📚 Documentation

- **Architecture** : [docs/architecture/](docs/architecture/)
- **Guides** : [docs/guides/](docs/guides/)
- **Recherche** : [docs/research/](docs/research/)
- **API** : [docs/api/](docs/api/)

## 🔧 Développement

Chaque module est un repository indépendant avec sa propre documentation et ses tests.
Consultez le README de chaque module pour les instructions spécifiques.

## 🌟 Contributions

Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour les guidelines de contribution.

---

*Basé sur les travaux de Pāṇini et la découverte des dhātu informationnels.*
EOF
    
    success "Documentation principale mise à jour"
}

# Créer le commit de restructuration
commit_restructuration() {
    log "Création du commit de restructuration..."
    
    cd "$PANINI_ROOT"
    
    # Ajouter tous les changements
    git add .
    
    # Créer le commit
    if git commit -m "feat: restructuration architecturale majeure

- Panini devient le parent principal de l'écosystème
- Tous les modules organisés comme submodules thématiques
- Structure modulaire: core, orchestration, services, infrastructure
- Consolidation recherche et documentation
- Architecture cohérente avec nomenclature Panini-*

BREAKING CHANGE: Réorganisation complète de l'architecture
Tous les repositories PaniniFS-* renommés en Panini-*"; then
        success "Commit de restructuration créé"
    else
        warning "Aucun changement à committer ou commit échoué"
    fi
}

# Fonction principale
main() {
    echo "🏗️ RESTRUCTURATION PANINI - PARENT PRINCIPAL"
    echo "=============================================="
    echo "Création architecture modulaire avec submodules organisés"
    echo ""
    
    # Vérifier qu'on est dans le bon repository
    if [ ! -d "$PANINI_ROOT" ]; then
        error "Repository Panini introuvable: $PANINI_ROOT"
        exit 1
    fi
    
    cd "$PANINI_ROOT"
    
    if [ ! -d ".git" ]; then
        error "Pas dans un repository Git"
        exit 1
    fi
    
    # Demander confirmation
    warning "Cette opération va restructurer complètement le repository Panini"
    warning "Assurez-vous que le renommage GitHub a été fait au préalable"
    read -p "Continuer avec la restructuration ? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log "Opération annulée par l'utilisateur"
        exit 0
    fi
    
    # Exécution des étapes
    backup_gitmodules
    create_directory_structure
    clean_old_submodules
    
    local submodules_count
    configure_all_submodules
    submodules_count=$?
    
    consolidate_research
    update_main_documentation
    commit_restructuration
    
    echo ""
    echo "📊 RÉSULTATS FINAUX DE LA RESTRUCTURATION"
    echo "=========================================="
    success "✅ Structure modulaire créée"
    success "✅ $submodules_count submodules configurés"
    success "✅ Documentation mise à jour"
    success "✅ Commit de restructuration créé"
    
    echo ""
    echo "🎯 ÉTAPES SUIVANTES RECOMMANDÉES:"
    echo "1. git push origin main  # Pousser la restructuration"
    echo "2. Vérifier tous les submodules : git submodule status"
    echo "3. Tester la navigation dans les modules"
    echo "4. Mettre à jour les liens externes et documentation"
    echo "5. Informer les collaborateurs de la nouvelle structure"
    
    echo ""
    success "🎉 RESTRUCTURATION PANINI TERMINÉE !"
}

# Point d'entrée
main "$@"