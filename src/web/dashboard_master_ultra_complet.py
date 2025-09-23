#!/usr/bin/env python3
"""
🚀 DASHBOARD MASTER ULTRA-COMPLET
Exploitation maximale dual-GPU + 16 cores pour monitoring total PaniniFS
"""

import asyncio
import json
import time
import psutil
import subprocess
import os
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import re

# Configuration optimisée pour machine puissante
CONFIG = {
    "update_interval": 1.0,  # Monitoring ultra-rapide
    "port": 8888,
    "gpu_monitoring": True,
    "deep_analysis": True,
    "auto_optimization": True,
    "workspace": "/home/stephane/GitHub/PaniniFS-Research"
}

@dataclass
class SystemMetrics:
    timestamp: float
    cpu_percent: float
    cpu_per_core: List[float]
    memory_percent: float
    memory_available: int
    load_avg: List[float]
    gpu_hd7750_temp: float
    gpu_hd7750_usage: float
    gpu_rx480_temp: float
    gpu_rx480_usage: float
    disk_usage: float
    network_io: Dict[str, int]

@dataclass
class VSCodeMetrics:
    processes: int
    memory_usage: float
    cpu_usage: float
    pylance_instances: int
    extensions_loaded: int
    crashes_today: int
    uptime_current: float

@dataclass
class PaniniMissions:
    corpus_tasks: Dict[str, str]
    dhatu_processing: Dict[str, Any]
    research_active: List[str]
    analysis_running: List[str]
    completed_today: int
    errors_count: int

class DualGPUMonitor:
    """Monitoring spécialisé dual-GPU HD7750 + RX480"""
    
    def __init__(self):
        self.gpu_paths = {
            "hd7750": "/sys/class/drm/card0/device",
            "rx480": "/sys/class/drm/card1/device"
        }
    
    def get_gpu_metrics(self) -> Dict[str, Any]:
        metrics = {}
        
        for gpu_name, base_path in self.gpu_paths.items():
            try:
                # Température
                temp_path = f"{base_path}/hwmon/hwmon*/temp1_input"
                temp_files = subprocess.run(f"ls {temp_path} 2>/dev/null", 
                                          shell=True, capture_output=True, text=True)
                if temp_files.stdout.strip():
                    with open(temp_files.stdout.strip().split()[0], 'r') as f:
                        temp = int(f.read().strip()) / 1000
                else:
                    temp = 0
                
                # Usage GPU
                usage_path = f"{base_path}/gpu_busy_percent"
                try:
                    with open(usage_path, 'r') as f:
                        usage = float(f.read().strip())
                except:
                    usage = 0
                
                # Fréquences
                freq_path = f"{base_path}/pp_dpm_sclk"
                frequencies = []
                try:
                    with open(freq_path, 'r') as f:
                        frequencies = f.read().strip().split('\n')
                except:
                    pass
                
                metrics[gpu_name] = {
                    "temperature": temp,
                    "usage": usage,
                    "frequencies": frequencies,
                    "active": temp > 0
                }
                
            except Exception as e:
                metrics[gpu_name] = {"error": str(e), "active": False}
        
        return metrics

class PaniniMissionTracker:
    """Tracker intelligent de toutes les missions PaniniFS"""
    
    def __init__(self, workspace: str):
        self.workspace = Path(workspace)
        self.db_path = self.workspace / "dashboard_data.db"
        self.init_database()
    
    def init_database(self):
        """Initialise la base de données de tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS mission_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            mission_type TEXT,
            mission_name TEXT,
            status TEXT,
            progress REAL,
            details TEXT
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            metrics TEXT
        )
        """)
        
        conn.commit()
        conn.close()
    
    def scan_active_missions(self) -> PaniniMissions:
        """Scan intelligent de toutes les missions actives"""
        corpus_tasks = self._scan_corpus_tasks()
        dhatu_processing = self._scan_dhatu_processing()
        research_active = self._scan_research_activities()
        analysis_running = self._scan_analysis_tasks()
        
        # Compter les succès du jour
        completed_today = self._count_completed_today()
        errors_count = self._count_errors_today()
        
        return PaniniMissions(
            corpus_tasks=corpus_tasks,
            dhatu_processing=dhatu_processing,
            research_active=research_active,
            analysis_running=analysis_running,
            completed_today=completed_today,
            errors_count=errors_count
        )
    
    def _scan_corpus_tasks(self) -> Dict[str, str]:
        """Scan des tâches corpus en cours"""
        tasks = {}
        
        # Rechercher les fichiers corpus récents
        corpus_files = list(self.workspace.glob("corpus_*.json"))
        for file in corpus_files[-5:]:  # 5 plus récents
            mtime = file.stat().st_mtime
            age = time.time() - mtime
            if age < 3600:  # Modifié dans la dernière heure
                tasks[file.name] = "active"
            elif age < 86400:  # Modifié aujourd'hui
                tasks[file.name] = "recent"
        
        # Vérifier les processus corpus actifs
        try:
            result = subprocess.run(["pgrep", "-f", "corpus"], 
                                  capture_output=True, text=True)
            if result.stdout.strip():
                tasks["corpus_processes"] = f"{len(result.stdout.strip().split())} running"
        except:
            pass
        
        return tasks
    
    def _scan_dhatu_processing(self) -> Dict[str, Any]:
        """Scan du processing dhatu"""
        processing = {}
        
        # Fichiers dhatu récents
        dhatu_files = list(self.workspace.glob("*dhatu*.json"))
        processing["dhatu_files"] = len(dhatu_files)
        
        # Processus dhatu actifs
        try:
            result = subprocess.run(["pgrep", "-f", "dhatu"], 
                                  capture_output=True, text=True)
            processing["active_processes"] = len(result.stdout.strip().split()) if result.stdout.strip() else 0
        except:
            processing["active_processes"] = 0
        
        # Analyse des logs dhatu
        log_files = list(self.workspace.glob("*dhatu*.log"))
        processing["log_files"] = len(log_files)
        
        return processing
    
    def _scan_research_activities(self) -> List[str]:
        """Scan des activités de recherche"""
        activities = []
        
        # Scripts Python en cours d'exécution
        try:
            result = subprocess.run(["pgrep", "-f", "python.*panini"], 
                                  capture_output=True, text=True)
            if result.stdout.strip():
                activities.append(f"Python Panini: {len(result.stdout.strip().split())} processes")
        except:
            pass
        
        # Fichiers markdown récents (recherche/docs)
        md_files = list(self.workspace.glob("*.md"))
        recent_md = [f for f in md_files if time.time() - f.stat().st_mtime < 3600]
        if recent_md:
            activities.append(f"Documentation: {len(recent_md)} files updated")
        
        return activities
    
    def _scan_analysis_tasks(self) -> List[str]:
        """Scan des tâches d'analyse"""
        tasks = []
        
        # Fichiers d'analyse récents
        analysis_files = list(self.workspace.glob("analyse_*.json"))
        recent_analysis = [f for f in analysis_files if time.time() - f.stat().st_mtime < 3600]
        
        for file in recent_analysis:
            tasks.append(f"Analysis: {file.name}")
        
        return tasks
    
    def _count_completed_today(self) -> int:
        """Compte les missions complétées aujourd'hui"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today_start = datetime.now().replace(hour=0, minute=0, second=0).timestamp()
        
        cursor.execute("""
        SELECT COUNT(*) FROM mission_logs 
        WHERE timestamp > ? AND status = 'completed'
        """, (today_start,))
        
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def _count_errors_today(self) -> int:
        """Compte les erreurs aujourd'hui"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today_start = datetime.now().replace(hour=0, minute=0, second=0).timestamp()
        
        cursor.execute("""
        SELECT COUNT(*) FROM mission_logs 
        WHERE timestamp > ? AND status = 'error'
        """, (today_start,))
        
        count = cursor.fetchone()[0]
        conn.close()
        return count

class VSCodeHealthMonitor:
    """Monitoring santé VS Code post dual-GPU"""
    
    def get_vscode_metrics(self) -> VSCodeMetrics:
        processes = 0
        memory_usage = 0.0
        cpu_usage = 0.0
        pylance_instances = 0
        
        # Compter les processus VS Code
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent', 'cmdline']):
            try:
                if 'code' in proc.info['name'].lower():
                    processes += 1
                    memory_usage += proc.info['memory_percent']
                    cpu_usage += proc.info['cpu_percent']
                    
                    if proc.info['cmdline'] and 'pylance' in ' '.join(proc.info['cmdline']):
                        pylance_instances += 1
            except:
                continue
        
        # Compter les crashes aujourd'hui
        crashes_today = self._count_crashes_today()
        
        # Extensions chargées (approximation via processus)
        extensions_loaded = max(0, processes - 3)  # Processus de base VS Code
        
        # Uptime actuel du processus principal
        uptime_current = self._get_main_vscode_uptime()
        
        return VSCodeMetrics(
            processes=processes,
            memory_usage=memory_usage,
            cpu_usage=cpu_usage,
            pylance_instances=pylance_instances,
            extensions_loaded=extensions_loaded,
            crashes_today=crashes_today,
            uptime_current=uptime_current
        )
    
    def _count_crashes_today(self) -> int:
        """Compte les crashes VS Code aujourd'hui"""
        try:
            result = subprocess.run([
                "journalctl", "--since", "today", "--grep", "code.*dumped core"
            ], capture_output=True, text=True)
            return len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        except:
            return 0
    
    def _get_main_vscode_uptime(self) -> float:
        """Uptime du processus VS Code principal"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'create_time', 'cmdline']):
                if ('code' in proc.info['name'].lower() and 
                    proc.info['cmdline'] and 
                    '--type' not in ' '.join(proc.info['cmdline'])):
                    return time.time() - proc.info['create_time']
        except:
            pass
        return 0.0

class DashboardWebServer:
    """Serveur web pour l'interface dashboard"""
    
    def __init__(self, port: int):
        self.port = port
        self.latest_data = {}
        
    def update_data(self, data: Dict[str, Any]):
        """Met à jour les données du dashboard"""
        self.latest_data = data
        self.latest_data['last_update'] = time.time()
    
    def start_server(self):
        """Démarre le serveur web"""
        
        class DashboardHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.server_instance = self.server.dashboard_instance
                
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(self.get_dashboard_html().encode())
                
                elif self.path == '/api/data':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(self.server_instance.latest_data, default=str).encode())
                
                elif self.path.startswith('/static/'):
                    # Servir les fichiers statiques si nécessaire
                    self.send_error(404)
                
                else:
                    self.send_error(404)
            
            def get_dashboard_html(self) -> str:
                """Génère le HTML du dashboard ultra-complet"""
                return '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 PaniniFS Dashboard Master</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1800px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .card h2 {
            margin-bottom: 15px;
            color: #4fc3f7;
            border-bottom: 2px solid #4fc3f7;
            padding-bottom: 10px;
        }
        
        .metric {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 10px 0;
            padding: 8px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
        }
        
        .metric-value {
            font-weight: bold;
            color: #81c784;
        }
        
        .metric-value.warning { color: #ffb74d; }
        .metric-value.danger { color: #e57373; }
        
        .progress-bar {
            width: 100%;
            height: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            overflow: hidden;
            margin: 5px 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4fc3f7, #81c784);
            border-radius: 10px;
            transition: width 0.3s ease;
        }
        
        .gpu-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        
        .gpu-card {
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 10px;
            border: 2px solid;
        }
        
        .gpu-hd7750 { border-color: #4fc3f7; }
        .gpu-rx480 { border-color: #e57373; }
        
        .mission-list {
            max-height: 300px;
            overflow-y: auto;
        }
        
        .mission-item {
            background: rgba(255, 255, 255, 0.05);
            margin: 5px 0;
            padding: 10px;
            border-radius: 8px;
            border-left: 4px solid #4fc3f7;
        }
        
        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
        }
        
        .status-active { background: #4caf50; }
        .status-warning { background: #ff9800; }
        .status-error { background: #f44336; }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            grid-column: 1 / -1;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #4fc3f7, #81c784);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .last-update {
            opacity: 0.7;
            font-size: 0.9em;
        }
        
        @media (max-width: 768px) {
            .container {
                grid-template-columns: 1fr;
            }
            .gpu-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 PaniniFS Dashboard Master</h1>
            <p>Configuration Dual-GPU Optimisée • 16 Cores • 62GB RAM</p>
            <p class="last-update" id="lastUpdate">Dernière mise à jour: --</p>
        </div>
        
        <!-- GPU Monitoring -->
        <div class="card">
            <h2>🎮 Dual GPU Status</h2>
            <div class="gpu-grid">
                <div class="gpu-card gpu-hd7750">
                    <h3>HD 7750 (Affichage)</h3>
                    <div class="metric">
                        <span>Température:</span>
                        <span class="metric-value" id="gpu-hd7750-temp">--°C</span>
                    </div>
                    <div class="metric">
                        <span>Usage:</span>
                        <span class="metric-value" id="gpu-hd7750-usage">--%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" id="gpu-hd7750-progress"></div>
                    </div>
                </div>
                
                <div class="gpu-card gpu-rx480">
                    <h3>RX 480 (Calcul)</h3>
                    <div class="metric">
                        <span>Température:</span>
                        <span class="metric-value" id="gpu-rx480-temp">--°C</span>
                    </div>
                    <div class="metric">
                        <span>Usage:</span>
                        <span class="metric-value" id="gpu-rx480-usage">--%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" id="gpu-rx480-progress"></div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- System Performance -->
        <div class="card">
            <h2>⚡ Performance Système</h2>
            <div class="metric">
                <span>CPU Global:</span>
                <span class="metric-value" id="cpu-usage">--%</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" id="cpu-progress"></div>
            </div>
            
            <div class="metric">
                <span>Mémoire:</span>
                <span class="metric-value" id="memory-usage">-- GB</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" id="memory-progress"></div>
            </div>
            
            <div class="metric">
                <span>Load Average:</span>
                <span class="metric-value" id="load-avg">--</span>
            </div>
            
            <div class="metric">
                <span>Disque:</span>
                <span class="metric-value" id="disk-usage">--%</span>
            </div>
        </div>
        
        <!-- VS Code Health -->
        <div class="card">
            <h2>💻 VS Code Santé</h2>
            <div class="metric">
                <span><span class="status-indicator" id="vscode-status"></span>Processus:</span>
                <span class="metric-value" id="vscode-processes">--</span>
            </div>
            
            <div class="metric">
                <span>Mémoire:</span>
                <span class="metric-value" id="vscode-memory">--%</span>
            </div>
            
            <div class="metric">
                <span>CPU:</span>
                <span class="metric-value" id="vscode-cpu">--%</span>
            </div>
            
            <div class="metric">
                <span>Pylance:</span>
                <span class="metric-value" id="vscode-pylance">-- instances</span>
            </div>
            
            <div class="metric">
                <span>Uptime:</span>
                <span class="metric-value" id="vscode-uptime">--</span>
            </div>
            
            <div class="metric">
                <span>Crashes aujourd'hui:</span>
                <span class="metric-value" id="vscode-crashes">--</span>
            </div>
        </div>
        
        <!-- Missions PaniniFS -->
        <div class="card">
            <h2>🎯 Missions Actives</h2>
            <div class="metric">
                <span>Complétées aujourd'hui:</span>
                <span class="metric-value" id="missions-completed">--</span>
            </div>
            
            <div class="metric">
                <span>Erreurs:</span>
                <span class="metric-value" id="missions-errors">--</span>
            </div>
            
            <div class="mission-list" id="missions-list">
                <!-- Missions dynamiques -->
            </div>
        </div>
        
        <!-- Corpus Processing -->
        <div class="card">
            <h2>📚 Corpus Processing</h2>
            <div id="corpus-status">
                <!-- Status corpus dynamique -->
            </div>
        </div>
        
        <!-- Dhatu Analysis -->
        <div class="card">
            <h2>🔬 Dhatu Analysis</h2>
            <div id="dhatu-status">
                <!-- Status dhatu dynamique -->
            </div>
        </div>
    </div>
    
    <script>
        let isConnected = true;
        
        function updateDashboard() {
            fetch('/api/data')
                .then(response => response.json())
                .then(data => {
                    isConnected = true;
                    updateSystemMetrics(data.system || {});
                    updateGPUMetrics(data.gpu || {});
                    updateVSCodeMetrics(data.vscode || {});
                    updateMissions(data.missions || {});
                    
                    document.getElementById('lastUpdate').textContent = 
                        'Dernière mise à jour: ' + new Date().toLocaleTimeString();
                })
                .catch(error => {
                    console.error('Erreur:', error);
                    isConnected = false;
                    document.getElementById('lastUpdate').textContent = 
                        'Connexion perdue: ' + new Date().toLocaleTimeString();
                });
        }
        
        function updateSystemMetrics(system) {
            document.getElementById('cpu-usage').textContent = 
                (system.cpu_percent || 0).toFixed(1) + '%';
            document.getElementById('cpu-progress').style.width = 
                (system.cpu_percent || 0) + '%';
            
            const memoryGB = ((system.memory_available || 0) / (1024**3)).toFixed(1);
            document.getElementById('memory-usage').textContent = memoryGB + ' GB';
            document.getElementById('memory-progress').style.width = 
                (system.memory_percent || 0) + '%';
            
            document.getElementById('load-avg').textContent = 
                system.load_avg ? system.load_avg.slice(0, 2).join(', ') : '--';
            
            document.getElementById('disk-usage').textContent = 
                (system.disk_usage || 0).toFixed(1) + '%';
        }
        
        function updateGPUMetrics(gpu) {
            // HD 7750
            const hd7750 = gpu.hd7750 || {};
            document.getElementById('gpu-hd7750-temp').textContent = 
                (hd7750.temperature || 0).toFixed(1) + '°C';
            document.getElementById('gpu-hd7750-usage').textContent = 
                (hd7750.usage || 0).toFixed(1) + '%';
            document.getElementById('gpu-hd7750-progress').style.width = 
                (hd7750.usage || 0) + '%';
            
            // RX 480
            const rx480 = gpu.rx480 || {};
            document.getElementById('gpu-rx480-temp').textContent = 
                (rx480.temperature || 0).toFixed(1) + '°C';
            document.getElementById('gpu-rx480-usage').textContent = 
                (rx480.usage || 0).toFixed(1) + '%';
            document.getElementById('gpu-rx480-progress').style.width = 
                (rx480.usage || 0) + '%';
        }
        
        function updateVSCodeMetrics(vscode) {
            document.getElementById('vscode-processes').textContent = 
                vscode.processes || '--';
            document.getElementById('vscode-memory').textContent = 
                (vscode.memory_usage || 0).toFixed(1) + '%';
            document.getElementById('vscode-cpu').textContent = 
                (vscode.cpu_usage || 0).toFixed(1) + '%';
            document.getElementById('vscode-pylance').textContent = 
                vscode.pylance_instances || '--';
            
            const uptime = vscode.uptime_current || 0;
            const hours = Math.floor(uptime / 3600);
            const minutes = Math.floor((uptime % 3600) / 60);
            document.getElementById('vscode-uptime').textContent = 
                hours + 'h ' + minutes + 'm';
            
            document.getElementById('vscode-crashes').textContent = 
                vscode.crashes_today || '0';
            
            // Status indicator
            const statusEl = document.getElementById('vscode-status');
            if (vscode.crashes_today > 0) {
                statusEl.className = 'status-indicator status-error';
            } else if (vscode.processes > 10) {
                statusEl.className = 'status-indicator status-warning';
            } else {
                statusEl.className = 'status-indicator status-active';
            }
        }
        
        function updateMissions(missions) {
            document.getElementById('missions-completed').textContent = 
                missions.completed_today || '0';
            document.getElementById('missions-errors').textContent = 
                missions.errors_count || '0';
            
            // Missions list
            const missionsList = document.getElementById('missions-list');
            missionsList.innerHTML = '';
            
            if (missions.corpus_tasks) {
                Object.entries(missions.corpus_tasks).forEach(([name, status]) => {
                    const item = document.createElement('div');
                    item.className = 'mission-item';
                    item.innerHTML = `
                        <span class="status-indicator status-${status === 'active' ? 'active' : 'warning'}"></span>
                        Corpus: ${name} (${status})
                    `;
                    missionsList.appendChild(item);
                });
            }
            
            if (missions.research_active) {
                missions.research_active.forEach(activity => {
                    const item = document.createElement('div');
                    item.className = 'mission-item';
                    item.innerHTML = `
                        <span class="status-indicator status-active"></span>
                        ${activity}
                    `;
                    missionsList.appendChild(item);
                });
            }
        }
        
        // Mise à jour automatique
        setInterval(updateDashboard, 1000);
        updateDashboard();
    </script>
</body>
</html>
                '''
            
            def log_message(self, format, *args):
                # Supprime les logs HTTP pour éviter le spam
                pass
        
        server = HTTPServer(('localhost', self.port), DashboardHandler)
        server.dashboard_instance = self
        print(f"🌐 Dashboard démarré sur http://localhost:{self.port}")
        server.serve_forever()

class MasterDashboard:
    """Dashboard Master Ultra-Complet"""
    
    def __init__(self):
        self.config = CONFIG
        self.gpu_monitor = DualGPUMonitor()
        self.mission_tracker = PaniniMissionTracker(self.config["workspace"])
        self.vscode_monitor = VSCodeHealthMonitor()
        self.web_server = DashboardWebServer(self.config["port"])
        
        self.running = False
        
    async def collect_all_metrics(self) -> Dict[str, Any]:
        """Collecte toutes les métriques en parallèle"""
        
        # Métriques système
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_per_core = psutil.cpu_percent(interval=0.1, percpu=True)
        memory = psutil.virtual_memory()
        load_avg = os.getloadavg()
        disk = psutil.disk_usage('/')
        
        # Network I/O
        network = psutil.net_io_counters()
        network_io = {
            "bytes_sent": network.bytes_sent,
            "bytes_recv": network.bytes_recv
        }
        
        # GPU metrics
        gpu_metrics = self.gpu_monitor.get_gpu_metrics()
        
        system_metrics = SystemMetrics(
            timestamp=time.time(),
            cpu_percent=cpu_percent,
            cpu_per_core=cpu_per_core,
            memory_percent=memory.percent,
            memory_available=memory.available,
            load_avg=list(load_avg),
            gpu_hd7750_temp=gpu_metrics.get('hd7750', {}).get('temperature', 0),
            gpu_hd7750_usage=gpu_metrics.get('hd7750', {}).get('usage', 0),
            gpu_rx480_temp=gpu_metrics.get('rx480', {}).get('temperature', 0),
            gpu_rx480_usage=gpu_metrics.get('rx480', {}).get('usage', 0),
            disk_usage=disk.percent,
            network_io=network_io
        )
        
        # VS Code metrics
        vscode_metrics = self.vscode_monitor.get_vscode_metrics()
        
        # Mission tracking
        mission_metrics = self.mission_tracker.scan_active_missions()
        
        return {
            "system": asdict(system_metrics),
            "vscode": asdict(vscode_metrics),
            "missions": asdict(mission_metrics),
            "gpu": gpu_metrics,
            "timestamp": time.time()
        }
    
    async def monitoring_loop(self):
        """Boucle principale de monitoring"""
        print("🚀 Démarrage monitoring ultra-complet...")
        
        while self.running:
            try:
                # Collecte des métriques
                metrics = await self.collect_all_metrics()
                
                # Mise à jour du serveur web
                self.web_server.update_data(metrics)
                
                # Sauvegarde périodique
                if int(time.time()) % 60 == 0:  # Chaque minute
                    self.save_metrics(metrics)
                
                # Auto-optimisations
                if self.config["auto_optimization"]:
                    await self.auto_optimize(metrics)
                
                await asyncio.sleep(self.config["update_interval"])
                
            except Exception as e:
                print(f"Erreur monitoring: {e}")
                await asyncio.sleep(5)
    
    def save_metrics(self, metrics: Dict[str, Any]):
        """Sauvegarde les métriques"""
        conn = sqlite3.connect(self.mission_tracker.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO performance_logs (timestamp, metrics)
        VALUES (?, ?)
        """, (time.time(), json.dumps(metrics)))
        
        conn.commit()
        conn.close()
    
    async def auto_optimize(self, metrics: Dict[str, Any]):
        """Optimisations automatiques basées sur les métriques"""
        
        # Si CPU élevé mais VS Code stable, répartir la charge
        if (metrics["system"]["cpu_percent"] > 80 and 
            metrics["vscode"]["crashes_today"] == 0):
            
            # Réduire la priorité des processus non-critiques
            try:
                subprocess.run(["renice", "+5", "-p"] + 
                             [str(p.pid) for p in psutil.process_iter() 
                              if "chrome" in p.name().lower() or "firefox" in p.name().lower()],
                             check=False)
            except:
                pass
        
        # Si GPU RX480 inactif, proposer des tâches
        if metrics["gpu"].get("rx480", {}).get("usage", 0) < 10:
            # Log suggestion d'utilisation GPU
            print("💡 RX 480 disponible pour calculs intensifs")
    
    def start(self):
        """Démarre le dashboard complet"""
        self.running = True
        
        # Démarrage du serveur web en thread séparé
        web_thread = threading.Thread(target=self.web_server.start_server, daemon=True)
        web_thread.start()
        
        # Boucle principale de monitoring
        asyncio.run(self.monitoring_loop())
    
    def stop(self):
        """Arrête le dashboard"""
        self.running = False

def main():
    """Point d'entrée principal"""
    print("🚀 DASHBOARD MASTER ULTRA-COMPLET")
    print("=" * 50)
    print("Configuration Dual-GPU Détectée:")
    print("  • HD 7750 (Affichage)")
    print("  • RX 480 (Calcul)")  
    print("  • 16 Cores + 62GB RAM")
    print("=" * 50)
    
    dashboard = MasterDashboard()
    
    try:
        dashboard.start()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du dashboard...")
        dashboard.stop()

if __name__ == "__main__":
    main()