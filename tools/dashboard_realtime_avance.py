#!/usr/bin/env python3
"""
🚀 DASHBOARD SYSTÈME TEMPS RÉEL - CPU/GPU/Pipeline
=================================================
Interface web avancée pour monitoring en temps réel
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import json
import threading
import time
from datetime import datetime
from pathlib import Path
import logging
import sys
import signal


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dhatu_monitoring_2025'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

class RealTimeDashboard:
    """Dashboard temps réel avec monitoring avancé"""
    
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.data_file = workspace / 'monitoring_data_realtime.json'
        self.running = False
        self.latest_data = {}
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def load_latest_data(self):
        """Charge les dernières données du moniteur"""
        try:
            if self.data_file.exists():
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.latest_data = data.get('latest', {})
                    return True
        except Exception as e:
            self.logger.error(f"Erreur lecture données: {e}")
            self.latest_data = {}
        return False
    
    def get_dashboard_data(self):
        """Prépare les données pour le dashboard"""
        if not self.load_latest_data():
            return self._get_empty_dashboard()
            
        try:
            data = self.latest_data
            
            # Transformation pour l'affichage
            dashboard_data = {
                'timestamp': data.get('timestamp', ''),
                'system_overview': {
                    'cpu_global': data.get('system', {}).get('cpu_percent_global', 0),
                    'memory_percent': data.get('system', {}).get('memory_percent', 0),
                    'disk_percent': data.get('system', {}).get('disk_usage_percent', 0),
                    'total_processes': data.get('summary', {}).get('total_processes', 0),
                    'gpu_type': data.get('gpu', {}).get('gpu_type', 'none'),
                    'gpu_utilization': data.get('gpu', {}).get('gpu_utilization', 0),
                },
                'pipeline_status': data.get('pipeline', {}),
                'processes_detail': self._format_processes_data(data.get('processes', {})),
                'performance_summary': data.get('summary', {}),
                'gpu_detail': data.get('gpu', {}),
                'health_status': self._calculate_health_status(data)
            }
            
            return dashboard_data
            
        except Exception as e:
            self.logger.error(f"Erreur formatage données: {e}")
            return self._get_empty_dashboard()
    
    def _format_processes_data(self, processes_raw):
        """Formate les données des processus pour l'affichage"""
        processes = []
        
        for pid, proc_data in processes_raw.items():
            if isinstance(proc_data, dict) and 'error' not in proc_data:
                
                # Calcul du status d'activité
                activity_level = 'low'
                cpu_percent = proc_data.get('cpu_percent', 0)
                file_activity = proc_data.get('recent_file_activity', {})
                
                if cpu_percent > 10 or file_activity.get('files_modified_last_minute', 0) > 0:
                    activity_level = 'high'
                elif cpu_percent > 2 or file_activity.get('files_created_last_minute', 0) > 0:
                    activity_level = 'medium'
                
                # GPU info
                gpu_info = proc_data.get('estimated_gpu_usage', {})
                
                process_formatted = {
                    'pid': pid,
                    'name': proc_data.get('name', '').replace('_', ' ').title(),
                    'short_name': proc_data.get('name', '').split('_')[-1].title(),
                    'cpu_percent': round(cpu_percent, 1),
                    'memory_mb': round(proc_data.get('memory_mb', 0), 1),
                    'memory_vms_mb': round(proc_data.get('memory_vms_mb', 0), 1),
                    'num_threads': proc_data.get('num_threads', 0),
                    'status': proc_data.get('status', 'unknown'),
                    'activity_level': activity_level,
                    'cpu_affinity': proc_data.get('cpu_affinity', []),
                    'cpu_affinity_str': ','.join(map(str, proc_data.get('cpu_affinity', []))),
                    'recent_files': file_activity.get('latest_files', [])[:2],  # 2 premiers
                    'files_activity': {
                        'created': file_activity.get('files_created_last_minute', 0),
                        'modified': file_activity.get('files_modified_last_minute', 0)
                    },
                    'working_dirs': file_activity.get('working_directories', [])[:3],  # 3 premiers
                    'gpu_usage': {
                        'using_gpu': gpu_info.get('using_gpu', False),
                        'gpu_memory_mb': gpu_info.get('gpu_memory_mb', 0),
                        'gpu_utilization': gpu_info.get('gpu_utilization_percent', 0),
                        'opencl_contexts': gpu_info.get('opencl_contexts', 0),
                        'compute_shaders': gpu_info.get('compute_shaders_active', False)
                    },
                    'uptime_indicator': self._calculate_uptime_indicator(proc_data),
                    'performance_score': self._calculate_performance_score(proc_data)
                }
                
                processes.append(process_formatted)
        
        # Tri par activité puis par CPU
        processes.sort(key=lambda x: (x['activity_level'] != 'high', -x['cpu_percent']))
        
        return processes
    
    def _calculate_uptime_indicator(self, proc_data):
        """Calcule un indicateur de temps de fonctionnement"""
        cpu_total = proc_data.get('cpu_total_time', 0)
        if cpu_total > 100:
            return 'long'
        elif cpu_total > 10:
            return 'medium'
        else:
            return 'short'
    
    def _calculate_performance_score(self, proc_data):
        """Calcule un score de performance (0-100)"""
        score = 50  # Base
        
        # Bonus CPU utilization modérée
        cpu = proc_data.get('cpu_percent', 0)
        if 5 <= cpu <= 25:
            score += 20
        elif cpu > 25:
            score += 10
        
        # Bonus activité fichiers
        activity = proc_data.get('recent_file_activity', {})
        if activity.get('files_modified_last_minute', 0) > 0:
            score += 15
        if activity.get('files_created_last_minute', 0) > 0:
            score += 10
        
        # Bonus GPU utilization
        gpu = proc_data.get('estimated_gpu_usage', {})
        if gpu.get('using_gpu', False):
            score += 20
        
        # Malus erreurs
        if proc_data.get('status') == 'zombie':
            score -= 30
        elif proc_data.get('status') == 'stopped':
            score -= 20
        
        return min(100, max(0, score))
    
    def _calculate_health_status(self, data):
        """Calcule le status de santé global"""
        pipeline = data.get('pipeline', {})
        system = data.get('system', {})
        
        health_score = 100
        
        # Pénalités système
        if system.get('memory_percent', 0) > 80:
            health_score -= 20
        if system.get('cpu_percent_global', 0) > 90:
            health_score -= 15
        if system.get('disk_usage_percent', 0) > 90:
            health_score -= 10
        
        # Bonus pipeline actif
        pipeline_components = [
            pipeline.get('corpus_collection_active', False),
            pipeline.get('research_cycles_running', False),
            pipeline.get('optimization_active', False),
            pipeline.get('validation_running', False),
            pipeline.get('dashboard_serving', False)
        ]
        
        active_components = sum(pipeline_components)
        if active_components >= 4:
            health_score += 10
        elif active_components <= 2:
            health_score -= 20
        
        # Status final
        if health_score >= 85:
            status = 'excellent'
        elif health_score >= 70:
            status = 'good'
        elif health_score >= 50:
            status = 'fair'
        else:
            status = 'poor'
        
        return {
            'score': health_score,
            'status': status,
            'active_components': active_components,
            'total_components': len(pipeline_components)
        }
    
    def _get_empty_dashboard(self):
        """Données vides par défaut"""
        return {
            'timestamp': datetime.now().isoformat(),
            'system_overview': {
                'cpu_global': 0,
                'memory_percent': 0,
                'disk_percent': 0,
                'total_processes': 0,
                'gpu_type': 'none',
                'gpu_utilization': 0,
            },
            'pipeline_status': {
                'overall_health': 'unknown'
            },
            'processes_detail': [],
            'performance_summary': {},
            'gpu_detail': {},
            'health_status': {
                'score': 0,
                'status': 'unknown',
                'active_components': 0,
                'total_components': 0
            }
        }
    
    def start_background_updates(self):
        """Démarre les mises à jour en arrière-plan"""
        def update_loop():
            while self.running:
                try:
                    # Charge nouvelles données
                    dashboard_data = self.get_dashboard_data()
                    
                    # Émission WebSocket
                    socketio.emit('dashboard_update', dashboard_data)
                    
                    # Attente
                    time.sleep(3)  # Mise à jour toutes les 3 secondes
                    
                except Exception as e:
                    self.logger.error(f"Erreur mise à jour: {e}")
                    time.sleep(5)
        
        self.running = True
        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()
        self.logger.info("🔄 Mises à jour en arrière-plan démarrées")


# Instance globale
dashboard = RealTimeDashboard(Path('/home/stephane/GitHub/PaniniFS-Research'))


@app.route('/')
def index():
    """Page principale du dashboard"""
    return render_template('dashboard_realtime.html')


@app.route('/api/data')
def api_data():
    """API REST pour les données"""
    return jsonify(dashboard.get_dashboard_data())


@app.route('/api/processes')
def api_processes():
    """API pour les processus uniquement"""
    data = dashboard.get_dashboard_data()
    return jsonify(data.get('processes_detail', []))


@socketio.on('connect')
def handle_connect():
    """Connexion WebSocket"""
    print(f'Client connecté: {request.sid}')
    emit('dashboard_update', dashboard.get_dashboard_data())


@socketio.on('disconnect')
def handle_disconnect():
    """Déconnexion WebSocket"""
    print(f'Client déconnecté: {request.sid}')


@socketio.on('request_update')
def handle_request_update():
    """Demande de mise à jour manuelle"""
    emit('dashboard_update', dashboard.get_dashboard_data())


def signal_handler(sig, frame):
    """Gestionnaire d'arrêt propre"""
    print('\\n🛑 Arrêt dashboard demandé')
    dashboard.running = False
    sys.exit(0)


if __name__ == '__main__':
    # Configuration signaux
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Démarrage mises à jour
    dashboard.start_background_updates()
    
    print("🚀 Démarrage Dashboard Système Temps Réel")
    print("📡 Interface disponible sur: http://localhost:8891")
    print("🔄 WebSocket actif pour mises à jour temps réel")
    
    # Démarrage serveur
    socketio.run(app, host='0.0.0.0', port=8891, debug=False)