"""
🔧 Configuration Manager - Gestionnaire Configuration GitHub-Sync
Gestionnaire centralisé des configurations pour système GitHub-Sync
"""

import json
import os
from typing import Dict, Any
from datetime import datetime


class GitHubSyncConfig:
    """Gestionnaire configuration GitHub-Sync"""
    
    DEFAULT_CONFIG = {
        'repository': {
            'owner': 'stephanedenis',
            'name': 'PaniniFS-Research',
            'branch': 'main'
        },
        'sync_strategy': {
            'mode': 'conservative',  # conservative, aggressive, manual
            'check_interval': 600,  # secondes
            'auto_rollback': True,
            'max_retries': 3
        },
        'hot_reload': {
            'enabled': True,
            'between_cycles': True,
            'safety_checks': True,
            'validation_required': True
        },
        'modules': {
            'cache_dir': 'src/modules/_cache',
            'fallback_dir': 'src/modules/_fallback',
            'versions_dir': 'src/modules/_versions',
            'target_modules': [
                'src/modules/interfaces/base_analyzer.py',
                'src/modules/analyzers/dhatu_analyzer.py',
                'src/modules/loaders/corpus_loader.py',
                'src/modules/gpu/gpu_detector.py'
            ]
        },
        'safety': {
            'max_rollback_points': 5,
            'update_history_limit': 20,
            'emergency_fallback_enabled': True,
            'validation_timeout': 30
        },
        'notifications': {
            'success_notifications': True,
            'error_notifications': True,
            'verbose_logging': False
        }
    }
    
    def __init__(self, config_file: str = "src/github_sync/config.json"):
        self.config_file = config_file
        self.config = self.DEFAULT_CONFIG.copy()
        self._ensure_config_dir()
        self.load_config()
    
    def _ensure_config_dir(self):
        """Assure que le répertoire de config existe"""
        config_dir = os.path.dirname(self.config_file)
        if config_dir and not os.path.exists(config_dir):
            os.makedirs(config_dir, exist_ok=True)
    
    def load_config(self) -> bool:
        """Charge la configuration depuis le fichier"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                
                # Merge avec configuration par défaut
                self._deep_merge(self.config, user_config)
                return True
            else:
                # Créer fichier config avec valeurs par défaut
                self.save_config()
                return False
                
        except Exception as e:
            print(f"⚠️ Erreur chargement config: {e}")
            print("🔄 Utilisation configuration par défaut")
            return False
    
    def save_config(self) -> bool:
        """Sauvegarde la configuration actuelle"""
        try:
            # Ajouter métadonnées
            config_with_meta = self.config.copy()
            config_with_meta['_metadata'] = {
                'last_updated': datetime.now().isoformat(),
                'version': '1.0.0',
                'auto_generated': True
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_with_meta, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Configuration sauvegardée: {self.config_file}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur sauvegarde config: {e}")
            return False
    
    def _deep_merge(self, base_dict: dict, update_dict: dict):
        """Merge profond de dictionnaires"""
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict):
                if isinstance(value, dict):
                    self._deep_merge(base_dict[key], value)
                else:
                    base_dict[key] = value
            else:
                base_dict[key] = value
    
    def get(self, path: str, default=None):
        """Récupère une valeur par chemin pointé (ex: 'sync_strategy.mode')"""
        keys = path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except KeyError:
            return default
    
    def set(self, path: str, value: Any) -> bool:
        """Définit une valeur par chemin pointé"""
        keys = path.split('.')
        config_dict = self.config
        
        try:
            # Naviguer jusqu'à l'avant-dernier niveau
            for key in keys[:-1]:
                if key not in config_dict:
                    config_dict[key] = {}
                config_dict = config_dict[key]
            
            # Définir la valeur finale
            config_dict[keys[-1]] = value
            return True
            
        except Exception as e:
            print(f"❌ Erreur définition config {path}: {e}")
            return False
    
    def configure_strategy(self, strategy: str, **options) -> bool:
        """Configure la stratégie de synchronisation"""
        
        valid_strategies = ['conservative', 'aggressive', 'manual']
        if strategy not in valid_strategies:
            print(f"❌ Stratégie invalide: {strategy}")
            print(f"Options valides: {', '.join(valid_strategies)}")
            return False
        
        # Configuration par stratégie
        strategy_configs = {
            'conservative': {
                'sync_strategy.mode': 'conservative',
                'sync_strategy.check_interval': 600,
                'sync_strategy.auto_rollback': True,
                'hot_reload.between_cycles': True,
                'hot_reload.safety_checks': True,
                'safety.validation_timeout': 30
            },
            'aggressive': {
                'sync_strategy.mode': 'aggressive',
                'sync_strategy.check_interval': 180,
                'sync_strategy.auto_rollback': False,
                'hot_reload.between_cycles': False,
                'hot_reload.safety_checks': False,
                'safety.validation_timeout': 10
            },
            'manual': {
                'sync_strategy.mode': 'manual',
                'sync_strategy.check_interval': 0,  # Pas de vérification auto
                'sync_strategy.auto_rollback': True,
                'hot_reload.between_cycles': True,
                'hot_reload.safety_checks': True,
                'safety.validation_timeout': 60
            }
        }
        
        # Appliquer configuration
        config = strategy_configs[strategy]
        for path, value in config.items():
            self.set(path, value)
        
        # Appliquer options personnalisées
        for option_key, option_value in options.items():
            if '.' in option_key:
                self.set(option_key, option_value)
            else:
                self.set(f'sync_strategy.{option_key}', option_value)
        
        print(f"🔧 Stratégie configurée: {strategy.upper()}")
        self.display_current_strategy()
        
        return True
    
    def display_current_strategy(self):
        """Affiche la stratégie actuelle"""
        mode = self.get('sync_strategy.mode')
        interval = self.get('sync_strategy.check_interval')
        auto_rollback = self.get('sync_strategy.auto_rollback')
        between_cycles = self.get('hot_reload.between_cycles')
        
        print(f"├── Mode: {mode}")
        print(f"├── Intervalle vérification: {interval//60 if interval > 0 else 'Manuel'} min")
        print(f"├── Auto-rollback: {'✅' if auto_rollback else '❌'}")
        print(f"└── Reload entre cycles: {'✅' if between_cycles else '❌'}")
    
    def get_repository_config(self) -> Dict[str, str]:
        """Retourne la configuration repository"""
        return self.get('repository', {})
    
    def get_module_paths(self) -> list:
        """Retourne les chemins des modules cibles"""
        return self.get('modules.target_modules', [])
    
    def get_cache_directories(self) -> Dict[str, str]:
        """Retourne les répertoires de cache"""
        return {
            'cache': self.get('modules.cache_dir'),
            'fallback': self.get('modules.fallback_dir'),
            'versions': self.get('modules.versions_dir')
        }
    
    def add_target_module(self, module_path: str) -> bool:
        """Ajoute un module aux cibles de synchronisation"""
        target_modules = self.get('modules.target_modules', [])
        
        if module_path not in target_modules:
            target_modules.append(module_path)
            self.set('modules.target_modules', target_modules)
            print(f"➕ Module ajouté: {module_path}")
            return True
        else:
            print(f"⚠️ Module déjà présent: {module_path}")
            return False
    
    def remove_target_module(self, module_path: str) -> bool:
        """Retire un module des cibles de synchronisation"""
        target_modules = self.get('modules.target_modules', [])
        
        if module_path in target_modules:
            target_modules.remove(module_path)
            self.set('modules.target_modules', target_modules)
            print(f"➖ Module retiré: {module_path}")
            return True
        else:
            print(f"⚠️ Module non trouvé: {module_path}")
            return False
    
    def validate_config(self) -> Dict[str, Any]:
        """Valide la configuration actuelle"""
        validation_result = {
            'valid': True,
            'warnings': [],
            'errors': []
        }
        
        # Vérifier repository
        repo_config = self.get_repository_config()
        if not repo_config.get('owner') or not repo_config.get('name'):
            validation_result['errors'].append("Configuration repository incomplète")
            validation_result['valid'] = False
        
        # Vérifier stratégie
        strategy = self.get('sync_strategy.mode')
        if strategy not in ['conservative', 'aggressive', 'manual']:
            validation_result['errors'].append(f"Stratégie invalide: {strategy}")
            validation_result['valid'] = False
        
        # Vérifier modules cibles
        target_modules = self.get('modules.target_modules', [])
        if not target_modules:
            validation_result['warnings'].append("Aucun module cible défini")
        
        # Vérifier répertoires
        cache_dirs = self.get_cache_directories()
        for dir_type, dir_path in cache_dirs.items():
            if not dir_path:
                validation_result['warnings'].append(f"Répertoire {dir_type} non défini")
        
        return validation_result
    
    def export_config(self, export_path: str) -> bool:
        """Exporte la configuration vers un fichier"""
        try:
            export_config = {
                'exported_at': datetime.now().isoformat(),
                'source_file': self.config_file,
                'config': self.config
            }
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_config, f, indent=2, ensure_ascii=False)
            
            print(f"📤 Configuration exportée: {export_path}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur export config: {e}")
            return False
    
    def import_config(self, import_path: str) -> bool:
        """Importe une configuration depuis un fichier"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                imported_data = json.load(f)
            
            if 'config' in imported_data:
                self.config = imported_data['config']
            else:
                self.config = imported_data
            
            # Valider et sauvegarder
            validation = self.validate_config()
            if validation['valid']:
                self.save_config()
                print(f"📥 Configuration importée: {import_path}")
                return True
            else:
                print("❌ Configuration importée invalide:")
                for error in validation['errors']:
                    print(f"  • {error}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur import config: {e}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """Remet la configuration aux valeurs par défaut"""
        self.config = self.DEFAULT_CONFIG.copy()
        success = self.save_config()
        if success:
            print("🔄 Configuration remise aux valeurs par défaut")
        return success
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Retourne un résumé de la configuration"""
        return {
            'strategy': self.get('sync_strategy.mode'),
            'auto_rollback': self.get('sync_strategy.auto_rollback'),
            'check_interval_min': self.get('sync_strategy.check_interval', 0) // 60,
            'target_modules_count': len(self.get('modules.target_modules', [])),
            'hot_reload_enabled': self.get('hot_reload.enabled'),
            'safety_checks': self.get('hot_reload.safety_checks'),
            'config_file': self.config_file
        }