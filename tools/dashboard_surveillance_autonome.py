#!/usr/bin/env python3
"""
🎯 DASHBOARD SURVEILLANCE SYSTÈMES AUTONOMES
=============================================
Monitoring temps réel de l'écosystème de recherche dhātu
"""

import json
import time
import psutil
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import threading
import re
from typing import Dict, List, Any, Optional


class AutonomousSystemsDashboard:
    """Dashboard surveillance systèmes autonomes"""
    
    def __init__(self, workspace: Path, port: int = 8890):
        self.workspace = workspace
        self.port = port
        self.running = False
        
        # Systèmes à surveiller
        self.monitored_systems = {
            'coordinateur_global_autonome.py': {
                'name': 'Coordinateur Global',
                'icon': '🎯',
                'priority': 'critical'
            },
            'systeme_autonome_recherche_dhatu.py': {
                'name': 'Moteur Recherche',
                'icon': '🔬',
                'priority': 'high'
            },
            'collecteur_corpus_autonome.py': {
                'name': 'Collecteur Corpus',
                'icon': '📚',
                'priority': 'medium'
            },
            'optimiseur_ml_autonome.py': {
                'name': 'Optimiseur ML',
                'icon': '🧠',
                'priority': 'medium'
            },
            'systeme_validation_metriques.py': {
                'name': 'Validation Métriques',
                'icon': '📊',
                'priority': 'low'
            }
        }
        
        # Métriques collectées
        self.metrics_history = []
        self.last_update = time.time()
        
    def get_system_processes(self) -> Dict[str, Dict]:
        """Récupération processus systèmes autonomes"""
        processes = {}
        
        for script_name, system_info in self.monitored_systems.items():
            processes[script_name] = {
                'name': system_info['name'],
                'icon': system_info['icon'],
                'priority': system_info['priority'],
                'running': False,
                'pid': None,
                'cpu_percent': 0.0,
                'memory_percent': 0.0,
                'uptime': 0,
                'status': 'stopped'
            }
            
            # Recherche processus
            try:
                result = subprocess.run([
                    'pgrep', '-f', script_name
                ], capture_output=True, text=True, timeout=5)
                
                if result.returncode == 0 and result.stdout.strip():
                    pids = result.stdout.strip().split('\n')
                    if pids and pids[0]:
                        pid = int(pids[0])
                        try:
                            proc = psutil.Process(pid)
                            processes[script_name].update({
                                'running': True,
                                'pid': pid,
                                'cpu_percent': proc.cpu_percent(),
                                'memory_percent': proc.memory_percent(),
                                'uptime': time.time() - proc.create_time(),
                                'status': 'running'
                            })
                        except psutil.NoSuchProcess:
                            processes[script_name]['status'] = 'zombie'
                            
            except Exception as e:
                processes[script_name]['status'] = f'error: {e}'
                
        return processes
    
    def get_autonomous_directories(self) -> Dict[str, Dict]:
        """Scan répertoires autonomes créés"""
        directories = {}
        
        patterns = [
            'autonomous_research_*',
            'coordination_*',
            'corpus_collection_*',
            'optimization_*',
            'validation_metrics_*'
        ]
        
        for pattern in patterns:
            for dir_path in self.workspace.glob(pattern):
                if dir_path.is_dir():
                    # Statistiques répertoire
                    files = list(dir_path.glob('*'))
                    total_size = sum(f.stat().st_size for f in files if f.is_file())
                    
                    # Fichiers récents
                    recent_files = [
                        f for f in files 
                        if f.is_file() and (time.time() - f.stat().st_mtime) < 3600
                    ]
                    
                    directories[dir_path.name] = {
                        'path': str(dir_path),
                        'files_count': len(files),
                        'total_size': total_size,
                        'recent_files': len(recent_files),
                        'last_modified': max(
                            (f.stat().st_mtime for f in files if f.is_file()),
                            default=0
                        )
                    }
        
        return directories
    
    def get_research_metrics(self) -> Dict[str, Any]:
        """Métriques de recherche depuis les logs"""
        metrics = {
            'cycles_completed': 0,
            'hypotheses_generated': 0,
            'hypotheses_tested': 0,
            'discoveries': 0,
            'corpus_size': 0,
            'errors_count': 0,
            'last_activity': None
        }
        
        # Scan logs recherche
        log_files = list(self.workspace.glob('**/*.log'))
        
        for log_file in log_files:
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extraction métriques
                cycles = len(re.findall(r'Début cycle \d+', content))
                hypotheses_gen = len(re.findall(r'Générées \d+ nouvelles hypothèses', content))
                errors = len(re.findall(r'ERROR|Erreur', content, re.IGNORECASE))
                
                metrics['cycles_completed'] += cycles
                metrics['hypotheses_generated'] += hypotheses_gen
                metrics['errors_count'] += errors
                
                # Dernière activité
                if log_file.stat().st_mtime > (metrics['last_activity'] or 0):
                    metrics['last_activity'] = log_file.stat().st_mtime
                    
            except Exception:
                continue
        
        # Scan fichiers JSON pour métriques supplémentaires
        json_files = list(self.workspace.glob('**/*.json'))
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Corpus
                if isinstance(data, list) and any('dhatu' in str(item) for item in data[:5]):
                    metrics['corpus_size'] += len(data)
                
                # Hypothèses
                if isinstance(data, dict):
                    if 'hypotheses' in data:
                        metrics['hypotheses_tested'] += len(data['hypotheses'])
                    
                    if 'discoveries' in data:
                        metrics['discoveries'] += len(data['discoveries'])
                        
            except Exception:
                continue
        
        return metrics
    
    def get_system_health(self) -> Dict[str, Any]:
        """Santé globale du système"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Load average
            load_avg = psutil.getloadavg() if hasattr(psutil, 'getloadavg') else [0, 0, 0]
            
            health = {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available_gb': memory.available / (1024**3),
                'disk_percent': disk.percent,
                'load_average': load_avg,
                'status': 'healthy'
            }
            
            # Évaluation santé
            if cpu_percent > 90 or memory.percent > 95:
                health['status'] = 'critical'
            elif cpu_percent > 75 or memory.percent > 85:
                health['status'] = 'warning'
                
            return health
            
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def collect_metrics(self) -> Dict[str, Any]:
        """Collection complète métriques"""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'uptime': time.time() - self.last_update,
            'processes': self.get_system_processes(),
            'directories': self.get_autonomous_directories(),
            'research_metrics': self.get_research_metrics(),
            'system_health': self.get_system_health()
        }
        
        # Stockage historique (garder 100 derniers)
        self.metrics_history.append(metrics)
        if len(self.metrics_history) > 100:
            self.metrics_history = self.metrics_history[-100:]
        
        return metrics
    
    def generate_dashboard_html(self, metrics: Dict[str, Any]) -> str:
        """Génération HTML dashboard"""
        
        # Calcul statistiques
        running_systems = sum(1 for p in metrics['processes'].values() if p['running'])
        total_systems = len(metrics['processes'])
        
        processes_html = ""
        for script, info in metrics['processes'].items():
            status_class = "running" if info['running'] else "stopped"
            status_icon = "🟢" if info['running'] else "🔴"
            
            processes_html += f"""
            <div class="system-card {status_class}">
                <div class="system-header">
                    <span class="system-icon">{info['icon']}</span>
                    <span class="system-name">{info['name']}</span>
                    <span class="status-icon">{status_icon}</span>
                </div>
                <div class="system-details">
                    <div>Status: {info['status']}</div>
                    {f"<div>PID: {info['pid']}</div>" if info['pid'] else ""}
                    {f"<div>CPU: {info['cpu_percent']:.1f}%</div>" if info['running'] else ""}
                    {f"<div>Memory: {info['memory_percent']:.1f}%</div>" if info['running'] else ""}
                    {f"<div>Uptime: {int(info['uptime'])}s</div>" if info['running'] else ""}
                </div>
            </div>
            """
        
        directories_html = ""
        for dir_name, dir_info in metrics['directories'].items():
            last_mod = datetime.fromtimestamp(dir_info['last_modified']).strftime('%H:%M:%S')
            size_mb = dir_info['total_size'] / (1024*1024)
            
            directories_html += f"""
            <div class="directory-card">
                <div class="dir-name">📁 {dir_name}</div>
                <div class="dir-stats">
                    <span>Files: {dir_info['files_count']}</span>
                    <span>Size: {size_mb:.1f}MB</span>
                    <span>Recent: {dir_info['recent_files']}</span>
                    <span>Last: {last_mod}</span>
                </div>
            </div>
            """
        
        research_metrics = metrics['research_metrics']
        health = metrics['system_health']
        
        return f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 Dashboard Systèmes Autonomes Dhātu</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            min-height: 100vh;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}
        
        .status-overview {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: rgba(255,255,255,0.15);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }}
        
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            margin: 10px 0;
        }}
        
        .main-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .section {{
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }}
        
        .section h2 {{
            margin-bottom: 20px;
            font-size: 1.5em;
            border-bottom: 2px solid rgba(255,255,255,0.3);
            padding-bottom: 10px;
        }}
        
        .system-card {{
            background: rgba(255,255,255,0.1);
            margin: 10px 0;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #ff6b6b;
        }}
        
        .system-card.running {{
            border-left-color: #4ecdc4;
        }}
        
        .system-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        
        .system-icon {{
            font-size: 1.5em;
            margin-right: 10px;
        }}
        
        .system-name {{
            font-weight: bold;
            flex-grow: 1;
        }}
        
        .system-details {{
            font-size: 0.9em;
            opacity: 0.8;
        }}
        
        .system-details div {{
            margin: 2px 0;
        }}
        
        .directory-card {{
            background: rgba(255,255,255,0.08);
            padding: 12px;
            margin: 8px 0;
            border-radius: 8px;
        }}
        
        .dir-name {{
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .dir-stats {{
            font-size: 0.85em;
            display: flex;
            gap: 15px;
            opacity: 0.8;
        }}
        
        .health-indicator {{
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }}
        
        .health-healthy {{ background: #4ecdc4; }}
        .health-warning {{ background: #f9ca24; }}
        .health-critical {{ background: #ff6b6b; }}
        
        .auto-refresh {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(255,255,255,0.2);
            padding: 10px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }}
        
        @media (max-width: 768px) {{
            .main-grid {{
                grid-template-columns: 1fr;
            }}
            .status-overview {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
    </style>
</head>
<body>
    <div class="auto-refresh">🔄 Auto-refresh: 5s</div>
    
    <div class="header">
        <h1>🎯 Dashboard Systèmes Autonomes Dhātu</h1>
        <p>Surveillance temps réel de l'écosystème de recherche sanskritique</p>
        <p><strong>Dernière mise à jour:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="status-overview">
        <div class="stat-card">
            <div>💻 Systèmes Actifs</div>
            <div class="stat-value">{running_systems}/{total_systems}</div>
        </div>
        <div class="stat-card">
            <div>🔄 Cycles Recherche</div>
            <div class="stat-value">{research_metrics['cycles_completed']}</div>
        </div>
        <div class="stat-card">
            <div>🧠 Hypothèses</div>
            <div class="stat-value">{research_metrics['hypotheses_generated']}</div>
        </div>
        <div class="stat-card">
            <div>📚 Corpus</div>
            <div class="stat-value">{research_metrics['corpus_size']}</div>
        </div>
    </div>
    
    <div class="main-grid">
        <div class="section">
            <h2>🚀 Processus Autonomes</h2>
            {processes_html}
        </div>
        
        <div class="section">
            <h2>📊 Santé Système</h2>
            <div class="system-card">
                <div class="system-header">
                    <span class="health-indicator health-{health['status']}"></span>
                    <span>Statut Global: {health['status'].title()}</span>
                </div>
                <div class="system-details">
                    <div>CPU: {health.get('cpu_percent', 0):.1f}%</div>
                    <div>RAM: {health.get('memory_percent', 0):.1f}%</div>
                    <div>Disque: {health.get('disk_percent', 0):.1f}%</div>
                    <div>RAM libre: {health.get('memory_available_gb', 0):.1f}GB</div>
                </div>
            </div>
            
            <h3 style="margin-top: 20px; margin-bottom: 10px;">📈 Métriques Recherche</h3>
            <div class="system-details">
                <div>Hypothèses testées: {research_metrics['hypotheses_tested']}</div>
                <div>Découvertes: {research_metrics['discoveries']}</div>
                <div>Erreurs: {research_metrics['errors_count']}</div>
                <div>Dernière activité: {datetime.fromtimestamp(research_metrics['last_activity']).strftime('%H:%M:%S') if research_metrics['last_activity'] else 'N/A'}</div>
            </div>
        </div>
    </div>
    
    <div class="section">
        <h2>📁 Répertoires Autonomes</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px;">
            {directories_html}
        </div>
    </div>
    
    <script>
        // Auto-refresh toutes les 5 secondes
        setTimeout(function() {{
            window.location.reload();
        }}, 5000);
        
        // Ajout timestamp aux éléments
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('Dashboard chargé:', new Date());
        }});
    </script>
</body>
</html>
        """


class DashboardRequestHandler(BaseHTTPRequestHandler):
    """Handler HTTP pour le dashboard"""
    
    def __init__(self, dashboard, *args, **kwargs):
        self.dashboard = dashboard
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Gestion requêtes GET"""
        if self.path == '/':
            # Page principale dashboard
            metrics = self.dashboard.collect_metrics()
            html = self.dashboard.generate_dashboard_html(metrics)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
            
        elif self.path == '/api/metrics':
            # API JSON métriques
            metrics = self.dashboard.collect_metrics()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(json.dumps(metrics, indent=2).encode('utf-8'))
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppression logs HTTP"""
        pass


def create_handler(dashboard):
    """Factory pour handler avec dashboard"""
    def handler(*args, **kwargs):
        DashboardRequestHandler(dashboard, *args, **kwargs)
    return handler


def main():
    """Point d'entrée principal"""
    workspace = Path('/home/stephane/GitHub/PaniniFS-Research')
    dashboard = AutonomousSystemsDashboard(workspace, port=8890)
    
    print(f"🎯 Lancement Dashboard Systèmes Autonomes")
    print(f"📊 Surveillance: {len(dashboard.monitored_systems)} systèmes")
    print(f"🌐 URL: http://localhost:8890")
    print(f"📁 Workspace: {workspace}")
    print(f"🔄 Actualisation: 5 secondes")
    
    # Création serveur HTTP
    handler = lambda *args, **kwargs: DashboardRequestHandler(dashboard, *args, **kwargs)
    httpd = HTTPServer(('localhost', dashboard.port), handler)
    
    try:
        dashboard.running = True
        print(f"✅ Dashboard actif sur http://localhost:{dashboard.port}")
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        print(f"\n🛑 Arrêt dashboard")
        dashboard.running = False
        httpd.shutdown()


if __name__ == "__main__":
    main()