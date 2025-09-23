"""
🚀 GitHub-Sync System - Module Principal

Système révolutionnaire de synchronisation GitHub pour Colab
avec hot-reload sans interruption des sessions.

Modules disponibles:
- config_manager: Gestionnaire configuration
- github_loader: Chargeur modules GitHub  
- hot_reload: Gestionnaire hot-reload
- module_updater: Orchestrateur mises à jour
"""

__version__ = "1.0.0"
__author__ = "PaniniFS Research Team"

# Import des classes principales pour faciliter l'utilisation
from .config_manager import GitHubSyncConfig
from .github_loader import GitHubModuleLoader
from .hot_reload import HotReloadManager
from .module_updater import ModuleUpdater

__all__ = [
    'GitHubSyncConfig',
    'GitHubModuleLoader', 
    'HotReloadManager',
    'ModuleUpdater'
]