"""
🚀 Setup Standard GitHub-Sync pour Notebooks
Module de configuration uniforme pour Colab et environnement local
"""

import sys
import os
from typing import Dict, Any, Tuple


def setup_github_sync_environment() -> Dict[str, Any]:
    """
    Configuration automatique de l'environnement GitHub-Sync
    Détecte Colab/Local et configure chemins, repo, imports
    """
    
    setup_result = {
        'environment': 'unknown',
        'repo_path': None,
        'src_path': None,
        'success': False,
        'messages': []
    }
    
    # Détection environnement
    if 'google.colab' in sys.modules:
        # === ENVIRONNEMENT COLAB ===
        setup_result['environment'] = 'colab'
        setup_result['messages'].append("🔍 Environnement Colab détecté")
        
        # Configuration chemins Colab
        repo_path = '/content/PaniniFS-Research'
        
        # Clone repo si nécessaire
        if not os.path.exists(repo_path):
            setup_result['messages'].append("📥 Clonage repository...")
            
            # Import IPython pour commandes shell
            try:
                from IPython import get_ipython
                ipython = get_ipython()
                result = ipython.system(f'git clone https://github.com/stephanedenis/PaniniFS-Research.git {repo_path}')
                
                if os.path.exists(repo_path):
                    setup_result['messages'].append("✅ Repository cloné avec succès")
                else:
                    setup_result['messages'].append("❌ Échec clonage repository")
                    return setup_result
                    
            except Exception as e:
                setup_result['messages'].append(f"❌ Erreur clonage: {e}")
                return setup_result
        else:
            setup_result['messages'].append("✅ Repository déjà présent")
        
        # Configuration chemins Colab
        setup_result['repo_path'] = repo_path
        setup_result['src_path'] = os.path.join(repo_path, 'src')
        
        # Changer vers le répertoire repo
        try:
            os.chdir(repo_path)
            setup_result['messages'].append(f"📂 Répertoire changé vers: {repo_path}")
        except Exception as e:
            setup_result['messages'].append(f"⚠️ Erreur changement répertoire: {e}")
    
    else:
        # === ENVIRONNEMENT LOCAL ===
        setup_result['environment'] = 'local'
        setup_result['messages'].append("🔍 Environnement local détecté")
        
        # Configuration chemins local
        current_dir = os.getcwd()
        
        # Recherche répertoire PaniniFS-Research
        if 'PaniniFS-Research' in current_dir:
            # Déjà dans le bon répertoire ou sous-répertoire
            while 'PaniniFS-Research' in os.path.basename(current_dir) or \
                  os.path.exists(os.path.join(current_dir, 'src', 'github_sync')):
                repo_path = current_dir
                break
            else:
                # Remonter jusqu'à trouver PaniniFS-Research
                while current_dir != '/':
                    if os.path.basename(current_dir) == 'PaniniFS-Research' and \
                       os.path.exists(os.path.join(current_dir, 'src')):
                        repo_path = current_dir
                        break
                    current_dir = os.path.dirname(current_dir)
                else:
                    setup_result['messages'].append("❌ Répertoire PaniniFS-Research non trouvé")
                    return setup_result
        else:
            setup_result['messages'].append("❌ Pas dans PaniniFS-Research")
            return setup_result
        
        setup_result['repo_path'] = repo_path
        setup_result['src_path'] = os.path.join(repo_path, 'src')
        setup_result['messages'].append(f"✅ Répertoire projet: {repo_path}")
    
    # Configuration Python path
    if setup_result['src_path'] not in sys.path:
        sys.path.insert(0, setup_result['src_path'])
        setup_result['messages'].append(f"🔧 Ajout Python path: {setup_result['src_path']}")
    else:
        setup_result['messages'].append("✅ Python path déjà configuré")
    
    # Vérification structure
    github_sync_path = os.path.join(setup_result['src_path'], 'github_sync')
    if os.path.exists(github_sync_path):
        setup_result['messages'].append("✅ Modules GitHub-Sync trouvés")
        setup_result['success'] = True
    else:
        setup_result['messages'].append("❌ Modules GitHub-Sync manquants")
        setup_result['success'] = False
    
    return setup_result


def import_github_sync_modules() -> Tuple[bool, Dict[str, Any]]:
    """
    Import standardisé des modules GitHub-Sync
    Retourne (success, modules_dict)
    """
    
    modules = {}
    
    try:
        # Import modules principaux
        from github_sync.config_manager import GitHubSyncConfig
        from github_sync.github_loader import GitHubModuleLoader
        from github_sync.hot_reload import HotReloadManager
        from github_sync.module_updater import ModuleUpdater
        
        modules['GitHubSyncConfig'] = GitHubSyncConfig
        modules['GitHubModuleLoader'] = GitHubModuleLoader
        modules['HotReloadManager'] = HotReloadManager
        modules['ModuleUpdater'] = ModuleUpdater
        
        return True, modules
        
    except ImportError as e:
        return False, {'error': str(e)}


def initialize_github_sync_objects():
    """Initialise les objets GitHub-Sync de manière standardisée"""
    
    try:
        from github_sync.config_manager import GitHubSyncConfig
        from github_sync.github_loader import GitHubModuleLoader
        from github_sync.hot_reload import HotReloadManager
        from github_sync.module_updater import ModuleUpdater
        
        print("🔧 Initialisation objets GitHub-Sync...")
        
        # Créer objets dans le bon ordre
        config = GitHubSyncConfig()
        loader = GitHubModuleLoader(config)
        hot_reload = HotReloadManager(loader)  # HotReloadManager ne prend que le loader
        updater = ModuleUpdater(config)
        
        objects = {
            'config': config,
            'loader': loader, 
            'hot_reload': hot_reload,
            'updater': updater
        }
        
        print("✅ Objets GitHub-Sync initialisés")
        return objects
        
    except Exception as e:
        print(f"❌ Erreur initialisation GitHub-Sync: {e}")
        return None


def initialize_github_sync_system():
    """
    Fonction complète d'initialisation GitHub-Sync
    Combine setup environnement + création objets
    """
    
    # Setup environnement
    setup_result = setup_github_sync_environment()
    
    if not setup_result['success']:
        setup_result['objects_created'] = False
        return setup_result
    
    # Initialiser objets
    objects = initialize_github_sync_objects()
    
    if objects:
        setup_result['objects_created'] = True
        setup_result.update(objects)  # Ajoute config, loader, etc. au result
        setup_result['messages'].append("✅ Système GitHub-Sync complet")
    else:
        setup_result['objects_created'] = False
        setup_result['messages'].append("❌ Échec création objets GitHub-Sync")
    
    return setup_result


def print_setup_summary(result: Dict[str, Any]):
    """Affiche un résumé du setup"""
    
    print("🚀 SETUP GITHUB-SYNC")
    print("=" * 50)
    
    for message in result['messages']:
        print(message)
    
    print()
    
    if result.get('objects_created'):
        print("📊 OBJETS DISPONIBLES:")
        print("├── config     : Configuration GitHub-Sync")
        print("├── loader     : Chargeur modules GitHub")
        print("├── updater    : Gestionnaire mises à jour")
        print("└── hot_reload : Manager hot-reload")
        print()
        print("🎯 Système prêt à utiliser!")
    else:
        print("❌ Initialisation échouée")
        print("🔧 Vérifiez les erreurs ci-dessus")
