"""
🔄 GitHub Module Loader - Chargement Dynamique depuis Repository
Système de chargement et mise à jour des modules depuis GitHub en temps réel
"""

import os
import json
import hashlib
import importlib
import sys
import time
import tempfile
import shutil
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import subprocess
import urllib.request
import urllib.parse


class GitHubModuleLoader:
    """Chargeur de modules depuis GitHub avec mise à jour automatique"""
    
    def __init__(self, repo_owner="stephanedenis", repo_name="PaniniFS-Research", branch="main"):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.branch = branch
        self.base_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}"
        
        # Dossiers locaux
        self.cache_dir = "src/modules/_remote"
        self.versions_dir = "src/modules/_versions"
        self.fallback_dir = "src/modules/_fallback"
        
        # État des modules
        self.loaded_modules = {}
        self.module_versions = {}
        self.last_check_time = 0
        self.check_interval = 300  # 5 minutes
        
        self._ensure_directories()
        self._load_version_cache()
    
    def _ensure_directories(self):
        """Assure l'existence des dossiers nécessaires"""
        for directory in [self.cache_dir, self.versions_dir, self.fallback_dir]:
            os.makedirs(directory, exist_ok=True)
    
    def _load_version_cache(self):
        """Charge le cache des versions des modules"""
        version_file = os.path.join(self.versions_dir, "module_versions.json")
        if os.path.exists(version_file):
            try:
                with open(version_file, 'r') as f:
                    self.module_versions = json.load(f)
            except:
                self.module_versions = {}
    
    def _save_version_cache(self):
        """Sauvegarde le cache des versions"""
        version_file = os.path.join(self.versions_dir, "module_versions.json")
        with open(version_file, 'w') as f:
            json.dump(self.module_versions, f, indent=2)
    
    def check_remote_versions(self) -> Dict[str, Any]:
        """Vérifie les versions des modules sur GitHub"""
        
        # Limitation fréquence vérification
        current_time = time.time()
        if current_time - self.last_check_time < self.check_interval:
            return {'status': 'cached', 'updates_available': False}
        
        self.last_check_time = current_time
        
        print("🔍 Vérification versions modules GitHub...")
        
        remote_versions = {}
        updates_available = False
        
        # Modules à vérifier
        module_paths = [
            "src/modules/analyzers/dhatu_gpu_t4.py",
            "src/modules/gpu/detector.py", 
            "src/modules/loaders/turbo_gpu_loader.py",
            "src/modules/interfaces.py",
            "src/modules/dynamic_manager.py"
        ]
        
        for module_path in module_paths:
            try:
                # Obtenir hash du fichier distant
                remote_hash = self._get_remote_file_hash(module_path)
                if remote_hash:
                    remote_versions[module_path] = remote_hash
                    
                    # Comparer avec version locale
                    local_hash = self.module_versions.get(module_path, "")
                    if remote_hash != local_hash:
                        updates_available = True
                        print(f"🔄 MAJ disponible: {os.path.basename(module_path)}")
                    else:
                        print(f"✅ À jour: {os.path.basename(module_path)}")
                        
            except Exception as e:
                print(f"⚠️ Erreur vérification {module_path}: {e}")
        
        return {
            'status': 'checked',
            'remote_versions': remote_versions,
            'updates_available': updates_available,
            'check_time': datetime.now().isoformat()
        }
    
    def _get_remote_file_hash(self, file_path: str) -> Optional[str]:
        """Obtient le hash d'un fichier distant sur GitHub"""
        try:
            url = f"{self.base_url}/{file_path}"
            with urllib.request.urlopen(url, timeout=10) as response:
                content = response.read()
                return hashlib.sha256(content).hexdigest()[:16]  # Hash court
        except:
            return None
    
    def download_module_updates(self, force_download: bool = False) -> Dict[str, Any]:
        """Télécharge les mises à jour des modules depuis GitHub"""
        
        print("📥 Téléchargement mises à jour modules...")
        
        download_results = {
            'downloaded': [],
            'failed': [],
            'skipped': [],
            'total_size': 0
        }
        
        # Vérifier d'abord les versions
        version_check = self.check_remote_versions()
        if not version_check.get('updates_available') and not force_download:
            print("✅ Tous les modules sont à jour")
            return download_results
        
        remote_versions = version_check.get('remote_versions', {})
        
        for module_path, remote_hash in remote_versions.items():
            local_hash = self.module_versions.get(module_path, "")
            
            if remote_hash != local_hash or force_download:
                success = self._download_single_module(module_path, remote_hash)
                if success:
                    download_results['downloaded'].append(module_path)
                    self.module_versions[module_path] = remote_hash
                else:
                    download_results['failed'].append(module_path)
            else:
                download_results['skipped'].append(module_path)
        
        # Sauvegarder cache versions
        self._save_version_cache()
        
        print(f"📊 Téléchargement terminé:")
        print(f"├── Téléchargés: {len(download_results['downloaded'])}")
        print(f"├── Échecs: {len(download_results['failed'])}")
        print(f"└── Ignorés: {len(download_results['skipped'])}")
        
        return download_results
    
    def _download_single_module(self, module_path: str, expected_hash: str) -> bool:
        """Télécharge un module unique depuis GitHub"""
        try:
            url = f"{self.base_url}/{module_path}"
            
            # Télécharger dans un fichier temporaire
            with urllib.request.urlopen(url, timeout=30) as response:
                content = response.read()
            
            # Vérifier intégrité
            actual_hash = hashlib.sha256(content).hexdigest()[:16]
            if actual_hash != expected_hash:
                print(f"❌ Hash mismatch pour {module_path}")
                return False
            
            # Sauvegarder dans cache
            cache_path = os.path.join(self.cache_dir, os.path.basename(module_path))
            
            # Backup ancienne version
            if os.path.exists(cache_path):
                backup_path = f"{cache_path}.backup"
                shutil.copy2(cache_path, backup_path)
            
            # Écrire nouvelle version
            with open(cache_path, 'wb') as f:
                f.write(content)
            
            print(f"✅ Module téléchargé: {os.path.basename(module_path)}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur téléchargement {module_path}: {e}")
            return False
    
    def validate_new_modules(self) -> Dict[str, Any]:
        """Valide les nouveaux modules téléchargés"""
        
        print("🧪 Validation nouveaux modules...")
        
        validation_results = {
            'valid': [],
            'invalid': [],
            'syntax_errors': [],
            'import_errors': []
        }
        
        # Modules à valider
        cached_modules = [f for f in os.listdir(self.cache_dir) if f.endswith('.py')]
        
        for module_file in cached_modules:
            module_path = os.path.join(self.cache_dir, module_file)
            
            # Test syntaxe
            if not self._validate_syntax(module_path):
                validation_results['syntax_errors'].append(module_file)
                continue
            
            # Test import (en sandbox)
            if not self._validate_import(module_path):
                validation_results['import_errors'].append(module_file)
                continue
            
            validation_results['valid'].append(module_file)
            print(f"✅ Module validé: {module_file}")
        
        success_rate = len(validation_results['valid']) / len(cached_modules) if cached_modules else 0
        
        print(f"📊 Validation terminée:")
        print(f"├── Valides: {len(validation_results['valid'])}")
        print(f"├── Erreurs syntaxe: {len(validation_results['syntax_errors'])}")
        print(f"├── Erreurs import: {len(validation_results['import_errors'])}")
        print(f"└── Taux succès: {success_rate:.1%}")
        
        return validation_results
    
    def _validate_syntax(self, module_path: str) -> bool:
        """Valide la syntaxe d'un module"""
        try:
            with open(module_path, 'r', encoding='utf-8') as f:
                source = f.read()
            compile(source, module_path, 'exec')
            return True
        except SyntaxError:
            return False
    
    def _validate_import(self, module_path: str) -> bool:
        """Valide qu'un module peut être importé"""
        try:
            # Sandbox import test
            spec = importlib.util.spec_from_file_location("test_module", module_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                return True
        except:
            pass
        return False
    
    def hot_reload_modules(self) -> Dict[str, Any]:
        """Recharge les modules à chaud sans interruption"""
        
        print("🔄 Hot-reload des modules...")
        
        reload_results = {
            'reloaded': [],
            'failed': [],
            'rollbacks': []
        }
        
        # Modules en cache à recharger
        cached_modules = [f for f in os.listdir(self.cache_dir) if f.endswith('.py')]
        
        for module_file in cached_modules:
            cache_path = os.path.join(self.cache_dir, module_file)
            
            try:
                # Identifier le module dans sys.modules
                module_name = self._find_loaded_module_name(module_file)
                
                if module_name:
                    # Sauvegarder état actuel
                    old_module = sys.modules.get(module_name)
                    
                    # Recharger depuis cache
                    self._reload_module_from_cache(module_name, cache_path)
                    
                    # Tester rapidement la nouvelle version
                    if self._quick_module_test(module_name):
                        reload_results['reloaded'].append(module_file)
                        print(f"🔄 Module rechargé: {module_file}")
                    else:
                        # Rollback en cas de problème
                        if old_module:
                            sys.modules[module_name] = old_module
                        reload_results['rollbacks'].append(module_file)
                        print(f"↩️ Rollback: {module_file}")
                else:
                    print(f"⚠️ Module non chargé: {module_file}")
                    
            except Exception as e:
                reload_results['failed'].append(module_file)
                print(f"❌ Échec reload {module_file}: {e}")
        
        print(f"📊 Hot-reload terminé:")
        print(f"├── Rechargés: {len(reload_results['reloaded'])}")
        print(f"├── Rollbacks: {len(reload_results['rollbacks'])}")
        print(f"└── Échecs: {len(reload_results['failed'])}")
        
        return reload_results
    
    def _find_loaded_module_name(self, module_file: str) -> Optional[str]:
        """Trouve le nom du module chargé correspondant au fichier"""
        base_name = module_file.replace('.py', '')
        
        # Recherche dans sys.modules
        for module_name, module in sys.modules.items():
            if hasattr(module, '__file__') and module.__file__:
                if base_name in module.__file__:
                    return module_name
        return None
    
    def _reload_module_from_cache(self, module_name: str, cache_path: str):
        """Recharge un module depuis le cache"""
        spec = importlib.util.spec_from_file_location(module_name, cache_path)
        if spec and spec.loader:
            new_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(new_module)
            sys.modules[module_name] = new_module
    
    def _quick_module_test(self, module_name: str) -> bool:
        """Test rapide d'un module rechargé"""
        try:
            module = sys.modules.get(module_name)
            if not module:
                return False
            
            # Tests basiques selon le type de module
            if 'analyzer' in module_name.lower():
                # Test qu'une classe analyseur existe
                return any(hasattr(getattr(module, attr), 'process') 
                          for attr in dir(module) 
                          if not attr.startswith('_'))
            elif 'loader' in module_name.lower():
                # Test qu'une classe loader existe
                return any(hasattr(getattr(module, attr), 'load_data')
                          for attr in dir(module) 
                          if not attr.startswith('_'))
            else:
                # Test import basique
                return True
                
        except:
            return False
    
    def get_module_status(self) -> Dict[str, Any]:
        """Retourne l'état actuel des modules GitHub"""
        
        return {
            'repo': f"{self.repo_owner}/{self.repo_name}",
            'branch': self.branch,
            'cached_modules': len([f for f in os.listdir(self.cache_dir) if f.endswith('.py')]),
            'loaded_modules': len(self.loaded_modules),
            'last_check': datetime.fromtimestamp(self.last_check_time).isoformat(),
            'versions_tracked': len(self.module_versions),
            'cache_dir': self.cache_dir
        }
    
    def emergency_fallback(self):
        """Bascule vers les modules de secours en cas de problème critique"""
        print("🚨 EMERGENCY FALLBACK - Basculement modules de secours")
        
        # Copier modules actuels vers fallback si pas déjà fait
        fallback_modules = [f for f in os.listdir(self.fallback_dir) if f.endswith('.py')]
        
        if not fallback_modules:
            print("⚠️ Aucun module de secours disponible")
            return False
        
        try:
            # Recharger modules de secours
            for module_file in fallback_modules:
                fallback_path = os.path.join(self.fallback_dir, module_file)
                module_name = self._find_loaded_module_name(module_file)
                if module_name:
                    self._reload_module_from_cache(module_name, fallback_path)
            
            print("✅ Basculement modules de secours réussi")
            return True
            
        except Exception as e:
            print(f"❌ Échec basculement: {e}")
            return False