#!/usr/bin/env python3
"""
COORDINATEUR ANALYSES CONCURRENTES v2.0
======================================

Orchestrateur pour analyses parallèles reproductibles avec monitoring système.
Lance analyseur géométrique en concurrence avec processus existants.
"""

import json
import subprocess
import psutil
import time
import os
import threading
from pathlib import Path
from typing import Dict, List, Any

class ConcurrentAnalysisCoordinator:
    """Coordinateur analyses concurrentes avec monitoring ressources"""
    
    def __init__(self):
        self.running_processes = {}
        self.resource_history = []
        self.analysis_results = {}
        
        # Monitoring thread
        self.monitoring_active = False
        self.monitor_thread = None
    
    def check_system_resources(self) -> Dict[str, Any]:
        """Vérification ressources système disponibles"""
        memory = psutil.virtual_memory()
        cpu_count = psutil.cpu_count(logical=True)
        load_avg = os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0]
        
        return {
            'memory': {
                'total_gb': memory.total / (1024**3),
                'available_gb': memory.available / (1024**3),
                'used_percent': memory.percent
            },
            'cpu': {
                'logical_cores': cpu_count,
                'load_1m': load_avg[0],
                'load_5m': load_avg[1],
                'load_15m': load_avg[2]
            },
            'timestamp': time.time()
        }
    
    def detect_running_analyses(self) -> Dict[str, Any]:
        """Détecte analyses déjà en cours"""
        running = {}
        
        # Processus Python avec analyse dans le nom
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                
                if ('python' in proc.info['name'] and 
                    any(keyword in cmdline for keyword in [
                        'dashboard', 'analyseur', 'raffinement', 'detection'
                    ])):
                    
                    running[proc.info['pid']] = {
                        'name': proc.info['name'],
                        'cmdline': cmdline,
                        'memory_mb': proc.memory_info().rss / (1024**2),
                        'cpu_percent': proc.cpu_percent()
                    }
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return running
    
    def estimate_concurrent_capacity(self) -> Dict[str, Any]:
        """Estime capacité pour analyses concurrentes"""
        resources = self.check_system_resources()
        running = self.detect_running_analyses()
        
        # Calculs capacité
        memory_used_by_analyses = sum(p['memory_mb'] for p in running.values())
        memory_available_gb = resources['memory']['available_gb']
        
        # Estimation workers optimaux
        current_load = resources['cpu']['load_1m']
        cpu_cores = resources['cpu']['logical_cores']
        
        # Stratégie conservative : utiliser 60% ressources restantes
        recommended_workers = max(1, int((cpu_cores - current_load) * 0.6))
        memory_per_worker_mb = 512  # Estimation conservative
        max_workers_by_memory = int((memory_available_gb * 1024 - memory_used_by_analyses) / memory_per_worker_mb)
        
        optimal_workers = min(recommended_workers, max_workers_by_memory, cpu_cores - 1)
        
        return {
            'recommended_workers': optimal_workers,
            'memory_available_gb': memory_available_gb,
            'memory_used_analyses_mb': memory_used_by_analyses,
            'cpu_load_current': current_load,
            'cpu_cores_available': cpu_cores - int(current_load),
            'running_analyses': len(running),
            'capacity_assessment': 'high' if optimal_workers >= 4 else 'medium' if optimal_workers >= 2 else 'low'
        }
    
    def start_resource_monitoring(self):
        """Démarre monitoring ressources en arrière-plan"""
        self.monitoring_active = True
        
        def monitor_loop():
            while self.monitoring_active:
                measurement = self.check_system_resources()
                measurement['running_processes'] = len(self.detect_running_analyses())
                self.resource_history.append(measurement)
                
                # Garder seulement 100 dernières mesures
                if len(self.resource_history) > 100:
                    self.resource_history.pop(0)
                
                time.sleep(30)  # Mesure toutes les 30s
        
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_resource_monitoring(self):
        """Arrête monitoring ressources"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
    
    def launch_geometric_analysis(self, force_workers: int = None) -> Dict[str, Any]:
        """Lance analyse géométrique parallèle"""
        
        print("🚀 LANCEMENT ANALYSE GÉOMÉTRIQUE CONCURRENTE")
        print("=" * 55)
        
        # Vérification capacités
        capacity = self.estimate_concurrent_capacity()
        
        print(f"📊 ÉTAT SYSTÈME:")
        print(f"   Mémoire disponible: {capacity['memory_available_gb']:.1f} GB")
        print(f"   CPU load: {capacity['cpu_load_current']:.1f}")
        print(f"   Analyses actives: {capacity['running_analyses']}")
        print(f"   Workers recommandés: {capacity['recommended_workers']}")
        print(f"   Capacité: {capacity['capacity_assessment'].upper()}")
        
        if capacity['capacity_assessment'] == 'low':
            print("⚠️ AVERTISSEMENT: Capacité système faible - analyse pourrait être lente")
        
        workers = force_workers if force_workers else capacity['recommended_workers']
        
        # Commande analyse géométrique
        cmd = [
            'python3', 
            'analyseur_corpus_geometrique_parallele.py'
        ]
        
        # Variables d'environnement pour configuration
        env = os.environ.copy()
        env['GEOMETRIC_WORKERS'] = str(workers)
        env['EXPERIMENT_MODE'] = 'concurrent'
        
        print(f"\n🔺 LANCEMENT avec {workers} workers...")
        
        try:
            # Lancement processus en arrière-plan
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env=env,
                cwd=os.getcwd(),
                text=True
            )
            
            self.running_processes['geometric_analysis'] = {
                'process': process,
                'start_time': time.time(),
                'workers': workers,
                'command': ' '.join(cmd)
            }
            
            print(f"✅ Processus lancé - PID: {process.pid}")
            print(f"📄 Logs en temps réel disponibles via PID {process.pid}")
            
            return {
                'status': 'launched',
                'pid': process.pid,
                'workers': workers,
                'capacity_used': capacity
            }
            
        except Exception as e:
            print(f"❌ ERREUR lancement: {e}")
            return {
                'status': 'failed',
                'error': str(e),
                'capacity_used': capacity
            }
    
    def check_analysis_status(self) -> Dict[str, Any]:
        """Vérifie statut analyses en cours"""
        status_report = {
            'timestamp': time.time(),
            'concurrent_analyses': {},
            'system_load': self.check_system_resources(),
            'performance_trend': self._compute_performance_trend()
        }
        
        # Vérification processus géométrique
        if 'geometric_analysis' in self.running_processes:
            proc_info = self.running_processes['geometric_analysis']
            process = proc_info['process']
            
            if process.poll() is None:  # Processus actif
                # Lecture logs récents (non-bloquante)
                try:
                    # Dernières lignes stdout
                    recent_output = "En cours..."  # Simplification pour démo
                    
                    status_report['concurrent_analyses']['geometric'] = {
                        'status': 'running',
                        'duration': time.time() - proc_info['start_time'],
                        'pid': process.pid,
                        'workers': proc_info['workers'],
                        'recent_output': recent_output
                    }
                except:
                    status_report['concurrent_analyses']['geometric'] = {
                        'status': 'running_no_output',
                        'duration': time.time() - proc_info['start_time'],
                        'pid': process.pid
                    }
            else:  # Processus terminé
                return_code = process.returncode
                status_report['concurrent_analyses']['geometric'] = {
                    'status': 'completed' if return_code == 0 else 'failed',
                    'return_code': return_code,
                    'duration': time.time() - proc_info['start_time']
                }
        
        # Analyses système existantes
        running_analyses = self.detect_running_analyses()
        status_report['concurrent_analyses']['system'] = {
            'count': len(running_analyses),
            'total_memory_mb': sum(p['memory_mb'] for p in running_analyses.values()),
            'processes': list(running_analyses.keys())
        }
        
        return status_report
    
    def _compute_performance_trend(self) -> Dict[str, Any]:
        """Calcule tendance performance système"""
        if len(self.resource_history) < 3:
            return {'trend': 'insufficient_data'}
        
        # Moyennes récentes vs anciennes
        recent = self.resource_history[-5:]
        older = self.resource_history[-15:-10] if len(self.resource_history) >= 15 else self.resource_history[:5]
        
        recent_memory = sum(h['memory']['used_percent'] for h in recent) / len(recent)
        older_memory = sum(h['memory']['used_percent'] for h in older) / len(older)
        
        recent_processes = sum(h.get('running_processes', 0) for h in recent) / len(recent)
        older_processes = sum(h.get('running_processes', 0) for h in older) / len(older)
        
        memory_trend = 'increasing' if recent_memory > older_memory + 5 else 'stable'
        process_trend = 'increasing' if recent_processes > older_processes else 'stable'
        
        return {
            'memory_trend': memory_trend,
            'process_trend': process_trend,
            'memory_recent': recent_memory,
            'memory_older': older_memory,
            'processes_recent': recent_processes,
            'processes_older': older_processes
        }
    
    def wait_for_completion(self, timeout_minutes: int = 30) -> Dict[str, Any]:
        """Attend fin analyses avec timeout"""
        print(f"\n⏳ ATTENTE COMPLETION - Timeout: {timeout_minutes} minutes")
        
        start_wait = time.time()
        timeout_seconds = timeout_minutes * 60
        
        while time.time() - start_wait < timeout_seconds:
            status = self.check_analysis_status()
            
            # Vérification si analyse géométrique terminée
            geometric_status = status['concurrent_analyses'].get('geometric', {})
            if geometric_status.get('status') in ['completed', 'failed']:
                print(f"✅ Analyse géométrique terminée: {geometric_status['status']}")
                return status
            
            # Affichage périodique
            elapsed = time.time() - start_wait
            if int(elapsed) % 60 == 0:  # Chaque minute
                print(f"🔄 {elapsed/60:.0f}min - Système: {status['system_load']['memory']['used_percent']:.1f}% RAM")
            
            time.sleep(10)  # Vérification toutes les 10s
        
        print(f"⏱️ TIMEOUT atteint ({timeout_minutes} minutes)")
        return self.check_analysis_status()
    
    def generate_concurrent_report(self) -> str:
        """Génère rapport analyses concurrentes"""
        
        final_status = self.check_analysis_status()
        
        # Recherche fichiers de résultats
        result_files = list(Path('.').glob('parallel_analysis_result_*.json'))
        config_files = list(Path('.').glob('config_geometric_parallel_*.json'))
        log_files = list(Path('.').glob('corpus_geometric_experiment_*.log'))
        
        report_lines = [
            "# 🔺 RAPPORT ANALYSES CONCURRENTES",
            f"**Timestamp**: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 📊 STATUT FINAL",
        ]
        
        # Statut analyses
        for analysis_name, analysis_info in final_status['concurrent_analyses'].items():
            if analysis_name == 'geometric':
                report_lines.extend([
                    f"### Analyse Géométrique Parallèle",
                    f"- **Statut**: {analysis_info.get('status', 'unknown')}",
                    f"- **Durée**: {analysis_info.get('duration', 0):.1f}s",
                    f"- **Workers**: {analysis_info.get('workers', 'N/A')}",
                    f"- **PID**: {analysis_info.get('pid', 'N/A')}",
                    ""
                ])
        
        # Fichiers générés
        report_lines.extend([
            "## 📄 FICHIERS GÉNÉRÉS",
            f"- **Résultats**: {len(result_files)} fichiers",
            f"- **Configurations**: {len(config_files)} fichiers", 
            f"- **Logs**: {len(log_files)} fichiers",
            ""
        ])
        
        # Derniers fichiers
        if result_files:
            latest_result = max(result_files, key=os.path.getctime)
            report_lines.append(f"- **Dernier résultat**: `{latest_result.name}`")
        
        if log_files:
            latest_log = max(log_files, key=os.path.getctime)
            report_lines.append(f"- **Log principal**: `{latest_log.name}`")
        
        # Performance système
        trend = final_status.get('performance_trend', {})
        system_load = final_status.get('system_load', {})
        
        report_lines.extend([
            "",
            "## ⚡ PERFORMANCE SYSTÈME",
            f"- **Mémoire**: {system_load.get('memory', {}).get('used_percent', 0):.1f}% utilisée",
            f"- **CPU Load**: {system_load.get('cpu', {}).get('load_1m', 0):.1f}",
            f"- **Tendance mémoire**: {trend.get('memory_trend', 'unknown')}",
            f"- **Analyses simultanées**: {final_status['concurrent_analyses'].get('system', {}).get('count', 0)}",
            ""
        ])
        
        # Instructions reproductibilité
        report_lines.extend([
            "## 🔬 REPRODUCTIBILITÉ",
            "Pour reproduire ces analyses:",
            "```bash",
            "python3 coordinateur_analyses_concurrentes.py",
            "```",
            "",
            "Configuration expérimentale sauvegardée dans fichiers `config_*.json`",
            ""
        ])
        
        report_content = "\n".join(report_lines)
        
        # Sauvegarde rapport
        report_file = f"rapport_analyses_concurrentes_{int(time.time())}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return report_file

def main():
    """Point d'entrée coordinateur analyses concurrentes"""
    
    print("🎭 COORDINATEUR ANALYSES CONCURRENTES v2.0")
    print("=" * 60)
    
    coordinator = ConcurrentAnalysisCoordinator()
    
    try:
        # Démarrage monitoring
        coordinator.start_resource_monitoring()
        
        # État initial système
        initial_capacity = coordinator.estimate_concurrent_capacity()
        print(f"💻 SYSTÈME: {initial_capacity['capacity_assessment'].upper()} capacity")
        print(f"📊 {initial_capacity['cpu_cores_available']} cores disponibles")
        print(f"💾 {initial_capacity['memory_available_gb']:.1f}GB mémoire libre")
        
        if initial_capacity['running_analyses'] > 0:
            print(f"🔄 {initial_capacity['running_analyses']} analyses déjà actives")
        
        # Lancement analyse géométrique
        launch_result = coordinator.launch_geometric_analysis()
        
        if launch_result['status'] == 'launched':
            print(f"\n✅ ANALYSE GÉOMÉTRIQUE LANCÉE")
            print(f"🎯 PID: {launch_result['pid']}")
            print(f"⚙️ Workers: {launch_result['workers']}")
            
            # Attente avec monitoring
            final_status = coordinator.wait_for_completion(timeout_minutes=15)
            
            # Génération rapport final
            report_file = coordinator.generate_concurrent_report()
            
            print(f"\n📋 RAPPORT FINAL: {report_file}")
            
            # Résumé final
            geometric_final = final_status['concurrent_analyses'].get('geometric', {})
            if geometric_final.get('status') == 'completed':
                print("🎉 SUCCÈS - Analyse géométrique terminée")
            elif geometric_final.get('status') == 'failed':
                print("❌ ÉCHEC - Analyse géométrique échouée")
            else:
                print("⏱️ TIMEOUT - Analyse encore en cours")
            
        else:
            print("❌ ÉCHEC LANCEMENT")
            print(f"Erreur: {launch_result.get('error', 'Unknown')}")
    
    finally:
        # Nettoyage
        coordinator.stop_resource_monitoring()
        
        print("\n🏁 COORDINATEUR TERMINÉ")

if __name__ == "__main__":
    main()