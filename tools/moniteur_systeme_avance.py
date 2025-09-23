#!/usr/bin/env python3
"""
🔍 MONITEUR SYSTÈME AVANCÉ - CPU/GPU/Pipeline
============================================
Monitoring détaillé en temps réel de tous les systèmes autonomes
"""

import psutil
import json
import time
import subprocess
import threading
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import os
import logging

class AdvancedSystemMonitor:
    """Moniteur système avancé avec détails CPU/GPU/Pipeline"""
    
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.monitoring_data = {}
        self.gpu_info = {}
        self.processes_info = {}
        self.pipeline_status = {}
        
        # Configuration
        self.update_interval = 2  # secondes
        self.data_retention = 300  # 5 minutes d'historique
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Fichier de données partagées
        self.data_file = workspace / 'monitoring_data_realtime.json'
        
        # Initialisation
        self._detect_gpu_capabilities()
        self._identify_autonomous_processes()
        
    def _detect_gpu_capabilities(self):
        """Détection des capacités GPU"""
        try:
            # AMD GPU via rocm-smi
            result = subprocess.run(['rocm-smi', '--showid', '--showtemp', '--showuse'], 
                                   capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.gpu_info['type'] = 'AMD'
                self.gpu_info['rocm_available'] = True
                self._parse_rocm_output(result.stdout)
            else:
                raise Exception("rocm-smi non disponible")
                
        except Exception:
            try:
                # Fallback avec radeontop
                result = subprocess.run(['radeontop', '-d', '-', '-l', '1'], 
                                       capture_output=True, text=True, timeout=3)
                if result.returncode == 0:
                    self.gpu_info['type'] = 'AMD'
                    self.gpu_info['radeontop_available'] = True
                else:
                    raise Exception("radeontop non disponible")
            except Exception:
                # Pas de GPU détecté ou outils non disponibles
                self.gpu_info = {'type': 'none', 'available': False}
                
        self.logger.info(f"GPU détecté: {self.gpu_info}")
    
    def _parse_rocm_output(self, output: str):
        """Parse la sortie de rocm-smi"""
        lines = output.strip().split('\n')
        for line in lines:
            if 'GPU' in line and '%' in line:
                # Parse GPU utilization
                match = re.search(r'(\d+)%', line)
                if match:
                    self.gpu_info['utilization'] = int(match.group(1))
    
    def _identify_autonomous_processes(self):
        """Identification des processus autonomes"""
        autonomous_keywords = [
            'coordinateur_global_autonome',
            'systeme_autonome_recherche_dhatu',
            'collecteur_corpus_autonome', 
            'optimiseur_ml_autonome',
            'systeme_validation_metriques',
            'dashboard_surveillance_autonome',
            'dashboard_master_ultra_complet',
            'systeme_autonome_recherche_dhatu_fixed'
        ]
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_info']):
            try:
                cmdline = ' '.join(proc.info['cmdline'] or [])
                for keyword in autonomous_keywords:
                    if keyword in cmdline:
                        self.processes_info[proc.info['pid']] = {
                            'name': keyword,
                            'cmdline': cmdline,
                            'process': proc
                        }
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        self.logger.info(f"Processus autonomes identifiés: {len(self.processes_info)}")
    
    def get_process_detailed_metrics(self, pid: int, proc_info: Dict) -> Dict:
        """Métriques détaillées pour un processus"""
        try:
            process = proc_info['process']
            
            # Métriques de base
            cpu_percent = process.cpu_percent()
            memory_info = process.memory_info()
            
            # Affinité CPU
            try:
                cpu_affinity = process.cpu_affinity()
            except (AttributeError, psutil.AccessDenied):
                cpu_affinity = []
            
            # Nombre de threads
            try:
                num_threads = process.num_threads()
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                num_threads = 0
            
            # Status du processus
            try:
                status = process.status()
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                status = 'unknown'
            
            # Temps CPU
            try:
                cpu_times = process.cpu_times()
                cpu_total = cpu_times.user + cpu_times.system
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                cpu_total = 0
            
            # Activité sur les fichiers récents
            recent_activity = self._get_process_file_activity(proc_info['name'])
            
            # Détection utilisation GPU (basé sur les process OpenCL/CUDA)
            gpu_usage = self._estimate_gpu_usage_for_process(pid)
            
            return {
                'name': proc_info['name'],
                'pid': pid,
                'cpu_percent': cpu_percent,
                'memory_mb': memory_info.rss / 1024 / 1024,
                'memory_vms_mb': memory_info.vms / 1024 / 1024,
                'cpu_affinity': cpu_affinity,
                'num_threads': num_threads,
                'status': status,
                'cpu_total_time': cpu_total,
                'recent_file_activity': recent_activity,
                'estimated_gpu_usage': gpu_usage,
                'timestamp': datetime.now().isoformat()
            }
            
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            return {
                'name': proc_info['name'],
                'pid': pid,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _get_process_file_activity(self, process_name: str) -> Dict:
        """Analyse l'activité récente des fichiers du processus"""
        activity = {
            'files_created_last_minute': 0,
            'files_modified_last_minute': 0,
            'latest_files': [],
            'working_directories': []
        }
        
        # Recherche des fichiers récents liés au processus
        now = time.time()
        one_minute_ago = now - 60
        
        # Patterns de recherche basés sur le nom du processus
        search_patterns = {
            'coordinateur_global_autonome': ['coordination_*', 'global_*'],
            'systeme_autonome_recherche_dhatu': ['autonomous_research_*', 'cycle_*'],
            'collecteur_corpus_autonome': ['corpus_*', 'collection_*'],
            'optimiseur_ml_autonome': ['optimization_*', 'ml_*'],
            'systeme_validation_metriques': ['validation_*', 'metrics_*'],
            'dashboard_surveillance_autonome': ['dashboard_*', 'surveillance_*'],
            'systeme_autonome_recherche_dhatu_fixed': ['auto_fixed_*', 'cycle_*']
        }
        
        patterns = search_patterns.get(process_name, [process_name + '*'])
        
        for pattern in patterns:
            try:
                for file_path in self.workspace.rglob(pattern):
                    if file_path.is_file():
                        stat = file_path.stat()
                        
                        if stat.st_mtime > one_minute_ago:
                            activity['files_modified_last_minute'] += 1
                            
                        if stat.st_ctime > one_minute_ago:
                            activity['files_created_last_minute'] += 1
                            
                        # Garder les 3 fichiers les plus récents
                        if len(activity['latest_files']) < 3:
                            activity['latest_files'].append({
                                'path': str(file_path.relative_to(self.workspace)),
                                'size_kb': stat.st_size / 1024,
                                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                            })
                            
                        # Répertoires de travail
                        parent_dir = str(file_path.parent.relative_to(self.workspace))
                        if parent_dir not in activity['working_directories']:
                            activity['working_directories'].append(parent_dir)
                            
            except Exception as e:
                self.logger.debug(f"Erreur analyse activité {pattern}: {e}")
                
        return activity
    
    def _estimate_gpu_usage_for_process(self, pid: int) -> Dict:
        """Estimation de l'utilisation GPU par processus"""
        gpu_usage = {
            'using_gpu': False,
            'gpu_memory_mb': 0,
            'gpu_utilization_percent': 0,
            'opencl_contexts': 0,
            'compute_shaders_active': False
        }
        
        try:
            # Vérification des descripteurs de fichiers GPU
            proc_fd_path = Path(f'/proc/{pid}/fd')
            if proc_fd_path.exists():
                for fd_link in proc_fd_path.iterdir():
                    try:
                        target = fd_link.readlink()
                        if 'dri' in str(target) or 'gpu' in str(target):
                            gpu_usage['using_gpu'] = True
                            break
                    except (OSError, PermissionError):
                        continue
            
            # Estimation simple basée sur les patterns d'utilisation
            if gpu_usage['using_gpu']:
                gpu_usage['gpu_utilization_percent'] = min(50, max(5, 
                    self.gpu_info.get('utilization', 0)))
                gpu_usage['gpu_memory_mb'] = 256  # Estimation
                gpu_usage['opencl_contexts'] = 1
                gpu_usage['compute_shaders_active'] = True
                
        except Exception as e:
            self.logger.debug(f"Erreur estimation GPU pour PID {pid}: {e}")
            
        return gpu_usage
    
    def get_system_pipeline_status(self) -> Dict:
        """Status du pipeline système global"""
        pipeline_status = {
            'corpus_collection_active': False,
            'research_cycles_running': False,
            'optimization_active': False,
            'validation_running': False,
            'dashboard_serving': False,
            'gpu_pipeline_active': False,
            'overall_health': 'unknown'
        }
        
        # Analyse des processus actifs
        active_processes = list(self.processes_info.keys())
        
        pipeline_status['corpus_collection_active'] = any(
            'collecteur_corpus' in info['name'] 
            for info in self.processes_info.values()
        )
        
        pipeline_status['research_cycles_running'] = any(
            'systeme_autonome_recherche' in info['name'] 
            for info in self.processes_info.values()
        )
        
        pipeline_status['optimization_active'] = any(
            'optimiseur_ml' in info['name'] 
            for info in self.processes_info.values()
        )
        
        pipeline_status['validation_running'] = any(
            'validation_metriques' in info['name'] 
            for info in self.processes_info.values()
        )
        
        pipeline_status['dashboard_serving'] = any(
            'dashboard' in info['name'] 
            for info in self.processes_info.values()
        )
        
        # GPU pipeline
        pipeline_status['gpu_pipeline_active'] = any(
            self._estimate_gpu_usage_for_process(pid)['using_gpu']
            for pid in active_processes
        )
        
        # Santé globale
        active_count = sum([
            pipeline_status['corpus_collection_active'],
            pipeline_status['research_cycles_running'],
            pipeline_status['optimization_active'],
            pipeline_status['validation_running'],
            pipeline_status['dashboard_serving']
        ])
        
        if active_count >= 4:
            pipeline_status['overall_health'] = 'excellent'
        elif active_count >= 3:
            pipeline_status['overall_health'] = 'good'
        elif active_count >= 2:
            pipeline_status['overall_health'] = 'partial'
        else:
            pipeline_status['overall_health'] = 'limited'
            
        return pipeline_status
    
    def collect_all_metrics(self) -> Dict:
        """Collection de toutes les métriques"""
        timestamp = datetime.now().isoformat()
        
        # Refresh process list
        self._identify_autonomous_processes()
        
        # Métriques système globales
        system_metrics = {
            'cpu_percent_global': psutil.cpu_percent(interval=1),
            'cpu_count': psutil.cpu_count(),
            'memory_total_mb': psutil.virtual_memory().total / 1024 / 1024,
            'memory_used_mb': psutil.virtual_memory().used / 1024 / 1024,
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage_percent': psutil.disk_usage('/').percent,
            'timestamp': timestamp
        }
        
        # Métriques GPU globales
        if self.gpu_info.get('type') != 'none':
            try:
                # Mise à jour info GPU
                self._detect_gpu_capabilities()
                gpu_metrics = {
                    'gpu_type': self.gpu_info.get('type', 'unknown'),
                    'gpu_utilization': self.gpu_info.get('utilization', 0),
                    'gpu_available': self.gpu_info.get('available', False),
                    'timestamp': timestamp
                }
            except Exception as e:
                gpu_metrics = {'error': str(e), 'timestamp': timestamp}
        else:
            gpu_metrics = {'type': 'none', 'timestamp': timestamp}
        
        # Métriques par processus
        process_metrics = {}
        for pid, proc_info in self.processes_info.items():
            process_metrics[pid] = self.get_process_detailed_metrics(pid, proc_info)
        
        # Status pipeline
        pipeline_status = self.get_system_pipeline_status()
        
        # Assemblage final
        all_metrics = {
            'timestamp': timestamp,
            'system': system_metrics,
            'gpu': gpu_metrics,
            'processes': process_metrics,
            'pipeline': pipeline_status,
            'summary': {
                'total_processes': len(process_metrics),
                'total_cpu_usage': sum(
                    p.get('cpu_percent', 0) for p in process_metrics.values()
                    if isinstance(p.get('cpu_percent'), (int, float))
                ),
                'total_memory_mb': sum(
                    p.get('memory_mb', 0) for p in process_metrics.values()
                    if isinstance(p.get('memory_mb'), (int, float))
                ),
                'gpu_processes': sum(
                    1 for p in process_metrics.values()
                    if p.get('estimated_gpu_usage', {}).get('using_gpu', False)
                )
            }
        }
        
        return all_metrics
    
    def save_metrics(self, metrics: Dict):
        """Sauvegarde des métriques"""
        try:
            # Lecture des données existantes
            if self.data_file.exists():
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    historical_data = json.load(f)
            else:
                historical_data = {'metrics_history': []}
            
            # Ajout nouvelles métriques
            historical_data['metrics_history'].append(metrics)
            historical_data['latest'] = metrics
            
            # Limite l'historique
            max_history = self.data_retention // self.update_interval
            if len(historical_data['metrics_history']) > max_history:
                historical_data['metrics_history'] = historical_data['metrics_history'][-max_history:]
            
            # Sauvegarde
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(historical_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde métriques: {e}")
    
    def run_monitoring_loop(self):
        """Boucle principale de monitoring"""
        self.logger.info("🔍 Démarrage monitoring système avancé")
        
        try:
            while True:
                start_time = time.time()
                
                # Collection métriques
                metrics = self.collect_all_metrics()
                
                # Sauvegarde
                self.save_metrics(metrics)
                
                # Log résumé
                summary = metrics['summary']
                self.logger.info(
                    f"📊 {summary['total_processes']} processus, "
                    f"CPU: {summary['total_cpu_usage']:.1f}%, "
                    f"MEM: {summary['total_memory_mb']:.0f}MB, "
                    f"GPU: {summary['gpu_processes']} processus"
                )
                
                # Attente prochaine itération
                elapsed = time.time() - start_time
                sleep_time = max(0, self.update_interval - elapsed)
                time.sleep(sleep_time)
                
        except KeyboardInterrupt:
            self.logger.info("🛑 Arrêt monitoring demandé")
        except Exception as e:
            self.logger.error(f"❌ Erreur monitoring: {e}")


def main():
    """Point d'entrée principal"""
    workspace = Path('/home/stephane/GitHub/PaniniFS-Research')
    monitor = AdvancedSystemMonitor(workspace)
    monitor.run_monitoring_loop()


if __name__ == "__main__":
    main()