"""
Module web pour dashboards et API
"""

from flask import Flask, render_template_string, jsonify
import json
from typing import Dict, Any
import os

from ..core.system_base import ProcessManager, SystemMonitor


class DashboardBase:
    """Classe de base pour les dashboards"""
    
    def __init__(self, name: str, port: int):
        self.name = name
        self.port = port
        self.app = Flask(name)
        self.process_manager = ProcessManager()
        self.system_monitor = SystemMonitor()
        self._setup_routes()
    
    def _setup_routes(self):
        """Configure les routes de base"""
        
        @self.app.route('/api/health')
        def health():
            return jsonify({'status': 'ok', 'service': self.name})
        
        @self.app.route('/api/system')
        def system_info():
            return jsonify({
                'cpu': self.system_monitor.get_cpu_metrics(),
                'memory': self.system_monitor.get_memory_metrics()
            })
    
    def add_route(self, rule: str, endpoint: str, handler):
        """Ajoute une route personnalisée"""
        self.app.add_url_rule(rule, endpoint, handler)
    
    def run(self, debug: bool = False):
        """Lance le dashboard"""
        print(f"🌐 {self.name} démarré sur http://localhost:{self.port}")
        self.app.run(host='0.0.0.0', port=self.port, debug=debug)


class EventSystemDashboard(DashboardBase):
    """Dashboard spécialisé pour le système événementiel"""
    
    def __init__(self, port: int = 8892):
        super().__init__("EventSystemDashboard", port)
        self._setup_event_routes()
    
    def _setup_event_routes(self):
        """Configure les routes spécifiques au système événementiel"""
        
        @self.app.route('/')
        def dashboard():
            return self._render_dashboard()
        
        @self.app.route('/api/metrics')
        def api_metrics():
            return jsonify(self._get_event_metrics())
        
        @self.app.route('/api/processes')
        def api_processes():
            keywords = ['systeme_evenementiel_cpu.py']
            processes = self.process_manager.find_processes_by_keywords(keywords)
            return jsonify([{
                'pid': p['pid'],
                'cpu_percent': p['cpu_percent'],
                'memory_mb': p['memory_mb'],
                'affinity': p['affinity']
            } for p in processes])
    
    def _get_event_metrics(self) -> Dict[str, Any]:
        """Collecte les métriques du système événementiel"""
        
        # Cherche les processus événementiels
        keywords = ['systeme_evenementiel_cpu.py']
        event_processes = self.process_manager.find_processes_by_keywords(keywords)
        
        # Métriques CPU
        cpu_metrics = self.system_monitor.get_cpu_metrics()
        
        # Allocation dédiée
        dedicated_cores = {
            'corpus_processor': [1, 2],
            'research_processor': [3, 4],
            'optimization_processor': [5, 6, 7],
            'validation_processor': [8]
        }
        
        # Métriques des processus événementiels
        total_event_cpu = sum(p['cpu_percent'] for p in event_processes)
        
        # Statut système
        if len(event_processes) > 0:
            if total_event_cpu > 5:
                system_status = 'ACTIF'
            else:
                system_status = 'IDLE'
        else:
            system_status = 'INACTIF'
        
        return {
            'timestamp': self.system_monitor.get_cpu_metrics(),
            'system_status': system_status,
            'event_processes': event_processes,
            'cpu_metrics': cpu_metrics,
            'dedicated_cores': dedicated_cores,
            'total_event_cpu': total_event_cpu
        }
    
    def _render_dashboard(self) -> str:
        """Génère le HTML du dashboard"""
        
        metrics = self._get_event_metrics()
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>🎯 Dashboard Système Événementiel</title>
            <meta charset="utf-8">
            <meta http-equiv="refresh" content="3">
            <style>
                body { 
                    font-family: 'Courier New', monospace; 
                    background: #1a1a1a; 
                    color: #00ff00; 
                    margin: 20px;
                    font-size: 14px;
                }
                .header { 
                    border: 2px solid #00ff00; 
                    padding: 15px; 
                    margin-bottom: 20px;
                    text-align: center;
                }
                .metrics-grid {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 20px;
                    margin-bottom: 20px;
                }
                .metric-box {
                    border: 1px solid #00ff00;
                    padding: 15px;
                    background: #0d1f0d;
                }
                .cpu-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                    gap: 10px;
                    margin-top: 10px;
                }
                .cpu-core {
                    border: 1px solid #666;
                    padding: 8px;
                    text-align: center;
                    background: #111;
                }
                .cpu-active { border-color: #ff6600; }
                .cpu-busy { border-color: #ff0000; }
                .status-actif { color: #00ff00; }
                .status-idle { color: #ffff00; }
                .status-inactif { color: #ff6666; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎯 DASHBOARD SYSTÈME ÉVÉNEMENTIEL</h1>
                <h2>Architecture: Événements + Affinité CPU</h2>
            </div>
            
            <div class="metrics-grid">
                <div class="metric-box">
                    <h3>📊 STATUT SYSTÈME</h3>
                    <p>Statut: <span class="status-{{ metrics.system_status.lower() }}">{{ metrics.system_status }}</span></p>
                    <p>Processus événementiels: {{ metrics.event_processes|length }}</p>
                    <p>CPU événementiel total: {{ "%.1f"|format(metrics.total_event_cpu) }}%</p>
                </div>
                
                <div class="metric-box">
                    <h3>🖥️ ALLOCATION CPU</h3>
                    <p>Cores totaux: {{ metrics.cpu_metrics.total_cores }}</p>
                    <p>CPU moyen: {{ "%.1f"|format(metrics.cpu_metrics.average_usage) }}%</p>
                    <p>Architecture: Événementielle</p>
                </div>
            </div>
            
            <div class="metric-box">
                <h3>🖥️ UTILISATION CPU PAR CORE</h3>
                <div class="cpu-grid">
                    {% for core in metrics.cpu_metrics.per_core_usage %}
                    <div class="cpu-core 
                        {% if core.usage > 30 %}cpu-busy
                        {% elif core.usage > 10 %}cpu-active
                        {% endif %}">
                        <strong>Core {{ core.core }}</strong><br>
                        {{ "%.1f"|format(core.usage) }}% {{ core.status }}
                    </div>
                    {% endfor %}
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 20px; color: #666;">
                <p>🔄 Auto-refresh: 3 secondes | API: /api/metrics</p>
            </div>
        </body>
        </html>
        """
        
        return render_template_string(html_template, metrics=metrics)


def create_dashboard(dashboard_type: str = "event", port: int = 8892):
    """Factory pour créer des dashboards"""
    
    if dashboard_type == "event":
        return EventSystemDashboard(port)
    else:
        raise ValueError(f"Type de dashboard inconnu: {dashboard_type}")