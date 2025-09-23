"""
🔄 Hot Reload Manager - Rechargement Modules Sans Interruption
Système de rechargement à chaud intégré aux cycles de traitement
"""

import time
import threading
from typing import Dict, Any, Optional, Callable
from datetime import datetime
from .github_loader import GitHubModuleLoader


class HotReloadManager:
    """Gestionnaire de rechargement à chaud des modules GitHub"""
    
    def __init__(self, github_loader: GitHubModuleLoader):
        self.github_loader = github_loader
        self.reload_thread = None
        self.reload_in_progress = False
        self.reload_queue = []
        self.callbacks = {}
        
        # Configuration
        self.auto_reload_enabled = True
        self.reload_between_cycles = True
        self.safety_checks_enabled = True
        
        # Métriques
        self.reload_stats = {
            'total_reloads': 0,
            'successful_reloads': 0,
            'failed_reloads': 0,
            'rollbacks': 0,
            'last_reload_time': None
        }
    
    def register_cycle_hooks(self, 
                           pre_cycle_hook: Optional[Callable] = None,
                           post_cycle_hook: Optional[Callable] = None,
                           between_cycles_hook: Optional[Callable] = None):
        """Enregistre les hooks pour intégration aux cycles"""
        
        if pre_cycle_hook:
            self.callbacks['pre_cycle'] = pre_cycle_hook
        if post_cycle_hook:
            self.callbacks['post_cycle'] = post_cycle_hook
        if between_cycles_hook:
            self.callbacks['between_cycles'] = between_cycles_hook
        
        print("🔗 Hooks cycle enregistrés pour hot-reload")
    
    def check_and_prepare_updates(self) -> Dict[str, Any]:
        """Phase 1: Vérification et préparation des MAJ (début cycle)"""
        
        print("🔍 Phase 1: Vérification MAJ GitHub...")
        
        # Hook pré-cycle
        if 'pre_cycle' in self.callbacks:
            self.callbacks['pre_cycle']()
        
        # Vérification versions GitHub
        version_check = self.github_loader.check_remote_versions()
        
        preparation_result = {
            'updates_available': version_check.get('updates_available', False),
            'modules_to_update': [],
            'preparation_success': False
        }
        
        if version_check.get('updates_available'):
            print("🔄 Mises à jour détectées - Préparation...")
            
            # Téléchargement en arrière-plan
            download_result = self.github_loader.download_module_updates()
            
            if download_result['downloaded']:
                # Validation des nouveaux modules
                validation_result = self.github_loader.validate_new_modules()
                
                if validation_result['valid']:
                    preparation_result.update({
                        'preparation_success': True,
                        'modules_to_update': validation_result['valid'],
                        'download_stats': download_result,
                        'validation_stats': validation_result
                    })
                    
                    # Ajouter à la queue de reload
                    self.reload_queue.extend(validation_result['valid'])
                    
                    print(f"✅ {len(validation_result['valid'])} modules prêts pour hot-reload")
                else:
                    print("❌ Validation modules échouée")
            else:
                print("❌ Téléchargement modules échoué")
        else:
            print("✅ Modules à jour - Aucune préparation nécessaire")
            preparation_result['preparation_success'] = True
        
        return preparation_result
    
    def process_with_stable_modules(self, process_function: Callable, *args, **kwargs) -> Any:
        """Phase 2: Traitement avec modules stables (pendant cycle)"""
        
        print("⚡ Phase 2: Traitement avec modules stables...")
        
        # S'assurer qu'aucun reload n'est en cours
        while self.reload_in_progress:
            time.sleep(0.1)
        
        # Traitement avec modules actuels (garantie stabilité)
        try:
            result = process_function(*args, **kwargs)
            
            # Hook post-traitement
            if 'post_cycle' in self.callbacks:
                self.callbacks['post_cycle'](result)
            
            return result
            
        except Exception as e:
            print(f"❌ Erreur traitement: {e}")
            # En cas d'erreur, déclencher fallback d'urgence
            self.github_loader.emergency_fallback()
            raise
    
    def hot_reload_between_cycles(self) -> Dict[str, Any]:
        """Phase 3: Hot-reload entre les cycles (moment sûr)"""
        
        if not self.reload_queue or not self.reload_between_cycles:
            return {'status': 'skipped', 'reason': 'no_updates_or_disabled'}
        
        print("🔄 Phase 3: Hot-reload entre cycles...")
        
        # Hook entre-cycles
        if 'between_cycles' in self.callbacks:
            self.callbacks['between_cycles']()
        
        # Marquer reload en cours
        self.reload_in_progress = True
        
        try:
            # Effectuer le hot-reload
            reload_result = self.github_loader.hot_reload_modules()
            
            # Mettre à jour statistiques
            self.reload_stats['total_reloads'] += 1
            
            if reload_result['reloaded']:
                self.reload_stats['successful_reloads'] += len(reload_result['reloaded'])
                print(f"✅ Hot-reload réussi: {len(reload_result['reloaded'])} modules")
            
            if reload_result['failed']:
                self.reload_stats['failed_reloads'] += len(reload_result['failed'])
                print(f"❌ Échecs hot-reload: {len(reload_result['failed'])} modules")
            
            if reload_result['rollbacks']:
                self.reload_stats['rollbacks'] += len(reload_result['rollbacks'])
                print(f"↩️ Rollbacks: {len(reload_result['rollbacks'])} modules")
            
            # Vider la queue après traitement
            self.reload_queue.clear()
            self.reload_stats['last_reload_time'] = datetime.now().isoformat()
            
            return {
                'status': 'completed',
                'reload_result': reload_result,
                'stats_updated': True
            }
            
        except Exception as e:
            print(f"❌ Erreur critique hot-reload: {e}")
            # Fallback d'urgence
            self.github_loader.emergency_fallback()
            return {'status': 'emergency_fallback', 'error': str(e)}
        
        finally:
            self.reload_in_progress = False
    
    def integrated_cycle_workflow(self, 
                                process_function: Callable,
                                cycle_pause_seconds: int = 5,
                                *args, **kwargs) -> Dict[str, Any]:
        """Workflow intégré complet: vérification → traitement → hot-reload"""
        
        workflow_start = time.time()
        workflow_result = {
            'cycle_id': int(workflow_start),
            'phases': {},
            'total_time': 0,
            'success': False
        }
        
        try:
            # Phase 1: Préparation (début cycle)
            phase1_start = time.time()
            prep_result = self.check_and_prepare_updates()
            workflow_result['phases']['preparation'] = {
                'result': prep_result,
                'duration': time.time() - phase1_start
            }
            
            # Phase 2: Traitement stable
            phase2_start = time.time()
            process_result = self.process_with_stable_modules(process_function, *args, **kwargs)
            workflow_result['phases']['processing'] = {
                'result': process_result,
                'duration': time.time() - phase2_start
            }
            
            # Pause entre cycles (moment optimal pour reload)
            if cycle_pause_seconds > 0:
                print(f"⏸️ Pause cycle: {cycle_pause_seconds}s (moment optimal hot-reload)")
                time.sleep(cycle_pause_seconds)
            
            # Phase 3: Hot-reload (entre cycles)
            phase3_start = time.time()
            reload_result = self.hot_reload_between_cycles()
            workflow_result['phases']['hot_reload'] = {
                'result': reload_result,
                'duration': time.time() - phase3_start
            }
            
            workflow_result['success'] = True
            
        except Exception as e:
            workflow_result['error'] = str(e)
            print(f"❌ Erreur workflow intégré: {e}")
        
        workflow_result['total_time'] = time.time() - workflow_start
        
        return workflow_result
    
    def start_background_monitoring(self, check_interval_minutes: int = 10):
        """Démarre la surveillance GitHub en arrière-plan"""
        
        if self.reload_thread and self.reload_thread.is_alive():
            print("⚠️ Surveillance déjà active")
            return
        
        def monitor_loop():
            while self.auto_reload_enabled:
                try:
                    # Vérification périodique GitHub
                    version_check = self.github_loader.check_remote_versions()
                    
                    if version_check.get('updates_available'):
                        print(f"🔔 Nouvelles versions détectées à {datetime.now().strftime('%H:%M:%S')}")
                        
                        # Préparer pour prochain cycle
                        download_result = self.github_loader.download_module_updates()
                        if download_result['downloaded']:
                            validation_result = self.github_loader.validate_new_modules()
                            if validation_result['valid']:
                                self.reload_queue.extend(validation_result['valid'])
                                print(f"📥 {len(validation_result['valid'])} modules prêts pour hot-reload")
                    
                    # Attente avant prochaine vérification
                    time.sleep(check_interval_minutes * 60)
                    
                except Exception as e:
                    print(f"❌ Erreur surveillance GitHub: {e}")
                    time.sleep(60)  # Attente réduite en cas d'erreur
        
        self.reload_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.reload_thread.start()
        
        print(f"🔄 Surveillance GitHub démarrée (vérification toutes les {check_interval_minutes} min)")
    
    def stop_background_monitoring(self):
        """Arrête la surveillance en arrière-plan"""
        self.auto_reload_enabled = False
        if self.reload_thread:
            self.reload_thread.join(timeout=5)
        print("⏹️ Surveillance GitHub arrêtée")
    
    def get_reload_statistics(self) -> Dict[str, Any]:
        """Retourne les statistiques de rechargement"""
        
        success_rate = 0
        if self.reload_stats['total_reloads'] > 0:
            success_rate = (self.reload_stats['successful_reloads'] / 
                          self.reload_stats['total_reloads']) * 100
        
        return {
            **self.reload_stats,
            'success_rate': success_rate,
            'queue_length': len(self.reload_queue),
            'reload_in_progress': self.reload_in_progress,
            'auto_reload_enabled': self.auto_reload_enabled,
            'github_status': self.github_loader.get_module_status()
        }
    
    def manual_reload_trigger(self) -> Dict[str, Any]:
        """Déclenchement manuel d'un hot-reload"""
        print("🔄 Déclenchement manuel hot-reload...")
        
        # Forcer vérification et téléchargement
        prep_result = self.check_and_prepare_updates()
        
        if prep_result['preparation_success']:
            # Effectuer reload immédiatement
            return self.hot_reload_between_cycles()
        else:
            return {'status': 'failed', 'reason': 'preparation_failed'}
    
    def configure_reload_strategy(self, 
                                auto_reload: bool = True,
                                between_cycles: bool = True,
                                safety_checks: bool = True):
        """Configure la stratégie de rechargement"""
        
        self.auto_reload_enabled = auto_reload
        self.reload_between_cycles = between_cycles
        self.safety_checks_enabled = safety_checks
        
        print(f"🔧 Stratégie hot-reload configurée:")
        print(f"├── Auto-reload: {'✅' if auto_reload else '❌'}")
        print(f"├── Entre cycles: {'✅' if between_cycles else '❌'}")
        print(f"└── Vérifications sécurité: {'✅' if safety_checks else '❌'}")
    
    def health_check(self) -> Dict[str, Any]:
        """Vérification santé du système hot-reload"""
        
        health_status = {
            'status': 'healthy',
            'issues': [],
            'recommendations': []
        }
        
        # Vérifications
        if self.reload_stats['failed_reloads'] > self.reload_stats['successful_reloads']:
            health_status['issues'].append("Taux d'échec reload élevé")
            health_status['recommendations'].append("Vérifier connectivité GitHub")
        
        if self.reload_stats['rollbacks'] > 5:
            health_status['issues'].append("Nombreux rollbacks")
            health_status['recommendations'].append("Vérifier qualité modules GitHub")
        
        if len(self.reload_queue) > 10:
            health_status['issues'].append("Queue reload surchargée")
            health_status['recommendations'].append("Réduire fréquence vérifications")
        
        if health_status['issues']:
            health_status['status'] = 'degraded'
        
        return health_status