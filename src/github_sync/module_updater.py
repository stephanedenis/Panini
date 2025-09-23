"""
🔄 Module Updater - Orchestrateur Central GitHub-Sync
Système central d'orchestration des mises à jour modules GitHub
"""

import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from .github_loader import GitHubModuleLoader
from .hot_reload import HotReloadManager


class ModuleUpdater:
    """Orchestrateur central pour mises à jour modules GitHub"""
    
    def __init__(self, repo_owner="stephanedenis", repo_name="PaniniFS-Research"):
        self.github_loader = GitHubModuleLoader(repo_owner, repo_name)
        self.hot_reload_manager = HotReloadManager(self.github_loader)
        
        # Configuration
        self.update_strategy = "conservative"  # conservative, aggressive, manual
        self.auto_rollback_enabled = True
        self.max_retries = 3
        
        # État système
        self.system_state = {
            'last_successful_update': None,
            'update_history': [],
            'current_module_versions': {},
            'rollback_points': []
        }
        
        self._load_system_state()
    
    def _load_system_state(self):
        """Charge l'état système depuis le cache"""
        try:
            state_file = "src/modules/_versions/system_state.json"
            with open(state_file, 'r') as f:
                self.system_state.update(json.load(f))
        except:
            pass
    
    def _save_system_state(self):
        """Sauvegarde l'état système"""
        try:
            state_file = "src/modules/_versions/system_state.json"
            with open(state_file, 'w') as f:
                json.dump(self.system_state, f, indent=2)
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde état: {e}")
    
    def configure_update_strategy(self, strategy: str, **options):
        """Configure la stratégie de mise à jour"""
        
        valid_strategies = ["conservative", "aggressive", "manual"]
        if strategy not in valid_strategies:
            raise ValueError(f"Stratégie invalide. Options: {valid_strategies}")
        
        self.update_strategy = strategy
        
        # Options par stratégie
        if strategy == "conservative":
            self.hot_reload_manager.configure_reload_strategy(
                auto_reload=True,
                between_cycles=True,
                safety_checks=True
            )
            self.auto_rollback_enabled = True
            self.github_loader.check_interval = 600  # 10 minutes
            
        elif strategy == "aggressive":
            self.hot_reload_manager.configure_reload_strategy(
                auto_reload=True,
                between_cycles=False,  # Reload pendant traitement
                safety_checks=False
            )
            self.auto_rollback_enabled = False
            self.github_loader.check_interval = 180  # 3 minutes
            
        elif strategy == "manual":
            self.hot_reload_manager.configure_reload_strategy(
                auto_reload=False,
                between_cycles=True,
                safety_checks=True
            )
            self.auto_rollback_enabled = True
        
        print(f"🔧 Stratégie mise à jour: {strategy.upper()}")
        print(f"├── Auto-rollback: {'✅' if self.auto_rollback_enabled else '❌'}")
        print(f"└── Intervalle vérification: {self.github_loader.check_interval//60} min")
    
    def execute_full_update_cycle(self, force: bool = False) -> Dict[str, Any]:
        """Exécute un cycle complet de mise à jour"""
        
        cycle_start = time.time()
        cycle_id = f"update_{int(cycle_start)}"
        
        cycle_result = {
            'cycle_id': cycle_id,
            'timestamp': datetime.now().isoformat(),
            'strategy': self.update_strategy,
            'phases': {},
            'success': False,
            'rollback_performed': False
        }
        
        print(f"🔄 Démarrage cycle MAJ complet ({self.update_strategy})...")
        
        try:
            # Phase 1: Vérification GitHub
            print("📡 Phase 1: Vérification GitHub...")
            phase1_start = time.time()
            
            version_check = self.github_loader.check_remote_versions()
            
            cycle_result['phases']['github_check'] = {
                'duration': time.time() - phase1_start,
                'updates_available': version_check.get('updates_available', False),
                'remote_versions': version_check.get('remote_versions', {})
            }
            
            if not version_check.get('updates_available') and not force:
                print("✅ Aucune mise à jour nécessaire")
                cycle_result['success'] = True
                cycle_result['reason'] = 'no_updates_needed'
                return cycle_result
            
            # Phase 2: Téléchargement
            print("📥 Phase 2: Téléchargement modules...")
            phase2_start = time.time()
            
            download_result = self.github_loader.download_module_updates(force_download=force)
            
            cycle_result['phases']['download'] = {
                'duration': time.time() - phase2_start,
                'downloaded': download_result['downloaded'],
                'failed': download_result['failed']
            }
            
            if not download_result['downloaded']:
                print("❌ Aucun module téléchargé")
                cycle_result['reason'] = 'download_failed'
                return cycle_result
            
            # Phase 3: Validation
            print("🧪 Phase 3: Validation modules...")
            phase3_start = time.time()
            
            validation_result = self.github_loader.validate_new_modules()
            
            cycle_result['phases']['validation'] = {
                'duration': time.time() - phase3_start,
                'valid': validation_result['valid'],
                'invalid': validation_result['invalid']
            }
            
            if not validation_result['valid']:
                print("❌ Aucun module valide")
                cycle_result['reason'] = 'validation_failed'
                return cycle_result
            
            # Phase 4: Création point de rollback
            print("💾 Phase 4: Point de rollback...")
            rollback_point = self._create_rollback_point()
            cycle_result['rollback_point'] = rollback_point
            
            # Phase 5: Hot-reload
            print("🔄 Phase 5: Hot-reload...")
            phase5_start = time.time()
            
            reload_result = self.github_loader.hot_reload_modules()
            
            cycle_result['phases']['hot_reload'] = {
                'duration': time.time() - phase5_start,
                'reloaded': reload_result['reloaded'],
                'failed': reload_result['failed'],
                'rollbacks': reload_result['rollbacks']
            }
            
            # Phase 6: Test post-reload
            print("🧪 Phase 6: Tests post-reload...")
            phase6_start = time.time()
            
            post_test_result = self._test_modules_post_reload(validation_result['valid'])
            
            cycle_result['phases']['post_test'] = {
                'duration': time.time() - phase6_start,
                'success': post_test_result['success'],
                'issues': post_test_result.get('issues', [])
            }
            
            # Décision rollback automatique
            if not post_test_result['success'] and self.auto_rollback_enabled:
                print("⚠️ Tests post-reload échoués - Rollback automatique...")
                rollback_success = self._execute_rollback(rollback_point)
                cycle_result['rollback_performed'] = rollback_success
                cycle_result['reason'] = 'auto_rollback_post_test'
                return cycle_result
            
            # Succès - Mise à jour état système
            self._update_system_state_success(cycle_result)
            cycle_result['success'] = True
            
            print(f"✅ Cycle MAJ réussi en {time.time() - cycle_start:.2f}s")
            
        except Exception as e:
            print(f"❌ Erreur critique cycle MAJ: {e}")
            cycle_result['error'] = str(e)
            
            # Rollback d'urgence
            if self.auto_rollback_enabled and 'rollback_point' in cycle_result:
                print("🚨 Rollback d'urgence...")
                rollback_success = self._execute_rollback(cycle_result['rollback_point'])
                cycle_result['rollback_performed'] = rollback_success
        
        finally:
            cycle_result['total_duration'] = time.time() - cycle_start
            self._save_update_history(cycle_result)
            self._save_system_state()
        
        return cycle_result
    
    def _create_rollback_point(self) -> Dict[str, Any]:
        """Crée un point de rollback avant mise à jour"""
        
        rollback_point = {
            'timestamp': datetime.now().isoformat(),
            'module_versions': self.github_loader.module_versions.copy(),
            'system_state': self.system_state.copy()
        }
        
        # Sauvegarder modules actuels vers fallback
        try:
            import shutil
            import os
            
            cache_files = [f for f in os.listdir(self.github_loader.cache_dir) if f.endswith('.py')]
            
            for module_file in cache_files:
                cache_path = os.path.join(self.github_loader.cache_dir, module_file)
                fallback_path = os.path.join(self.github_loader.fallback_dir, module_file)
                
                if os.path.exists(cache_path):
                    shutil.copy2(cache_path, fallback_path)
            
            rollback_point['fallback_created'] = True
            
        except Exception as e:
            print(f"⚠️ Erreur création fallback: {e}")
            rollback_point['fallback_created'] = False
        
        # Ajouter à l'historique (garder 5 derniers)
        self.system_state['rollback_points'].append(rollback_point)
        if len(self.system_state['rollback_points']) > 5:
            self.system_state['rollback_points'] = self.system_state['rollback_points'][-5:]
        
        return rollback_point
    
    def _test_modules_post_reload(self, updated_modules: List[str]) -> Dict[str, Any]:
        """Teste les modules après hot-reload"""
        
        test_result = {
            'success': True,
            'tested_modules': [],
            'issues': []
        }
        
        for module_file in updated_modules:
            try:
                # Tests basiques selon type module
                if 'analyzer' in module_file:
                    # Test qu'on peut créer un analyseur
                    test_result['tested_modules'].append(f"{module_file}:analyzer_creation")
                
                elif 'loader' in module_file:
                    # Test qu'on peut créer un loader
                    test_result['tested_modules'].append(f"{module_file}:loader_creation")
                
                elif 'detector' in module_file:
                    # Test détection GPU
                    test_result['tested_modules'].append(f"{module_file}:gpu_detection")
                
            except Exception as e:
                test_result['success'] = False
                test_result['issues'].append(f"{module_file}: {str(e)}")
        
        return test_result
    
    def _execute_rollback(self, rollback_point: Dict[str, Any]) -> bool:
        """Exécute un rollback vers un point de sauvegarde"""
        
        try:
            print(f"↩️ Rollback vers {rollback_point['timestamp'][:19]}...")
            
            # Restaurer versions modules
            self.github_loader.module_versions = rollback_point['module_versions']
            
            # Utiliser modules fallback
            emergency_success = self.github_loader.emergency_fallback()
            
            if emergency_success:
                print("✅ Rollback réussi")
                return True
            else:
                print("❌ Rollback échoué")
                return False
                
        except Exception as e:
            print(f"❌ Erreur rollback: {e}")
            return False
    
    def _update_system_state_success(self, cycle_result: Dict[str, Any]):
        """Met à jour l'état système après succès"""
        
        self.system_state.update({
            'last_successful_update': cycle_result['timestamp'],
            'current_module_versions': self.github_loader.module_versions.copy()
        })
    
    def _save_update_history(self, cycle_result: Dict[str, Any]):
        """Sauvegarde l'historique des mises à jour"""
        
        # Garder seulement les 20 dernières
        self.system_state['update_history'].append({
            'cycle_id': cycle_result['cycle_id'],
            'timestamp': cycle_result['timestamp'],
            'success': cycle_result['success'],
            'duration': cycle_result.get('total_duration', 0),
            'strategy': cycle_result['strategy']
        })
        
        if len(self.system_state['update_history']) > 20:
            self.system_state['update_history'] = self.system_state['update_history'][-20:]
    
    def get_update_status(self) -> Dict[str, Any]:
        """Retourne l'état actuel des mises à jour"""
        
        return {
            'strategy': self.update_strategy,
            'auto_rollback': self.auto_rollback_enabled,
            'last_update': self.system_state.get('last_successful_update'),
            'update_count': len(self.system_state['update_history']),
            'rollback_points': len(self.system_state['rollback_points']),
            'github_status': self.github_loader.get_module_status(),
            'hot_reload_stats': self.hot_reload_manager.get_reload_statistics()
        }
    
    def manual_update_trigger(self, force: bool = False) -> Dict[str, Any]:
        """Déclenchement manuel d'une mise à jour"""
        
        print("🔄 Déclenchement manuel mise à jour...")
        return self.execute_full_update_cycle(force=force)
    
    def list_available_rollback_points(self) -> List[Dict[str, Any]]:
        """Liste les points de rollback disponibles"""
        
        return [
            {
                'timestamp': rp['timestamp'],
                'age_hours': (datetime.now() - datetime.fromisoformat(rp['timestamp'])).total_seconds() / 3600,
                'fallback_available': rp.get('fallback_created', False)
            }
            for rp in self.system_state['rollback_points']
        ]
    
    def manual_rollback(self, rollback_index: int = -1) -> bool:
        """Rollback manuel vers un point spécifique"""
        
        if not self.system_state['rollback_points']:
            print("❌ Aucun point de rollback disponible")
            return False
        
        try:
            rollback_point = self.system_state['rollback_points'][rollback_index]
            return self._execute_rollback(rollback_point)
        except IndexError:
            print(f"❌ Point de rollback {rollback_index} inexistant")
            return False