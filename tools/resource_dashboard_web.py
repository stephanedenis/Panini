#!/usr/bin/env python3
"""
🎛️ EXTENSION DASHBOARD WEB: AFFECTATION RESSOURCES
Interface web pour visualiser l'affectation des ressources en temps réel
"""

import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
from resource_allocation_monitor import ResourceAllocationMonitor

class ResourceDashboardHandler(BaseHTTPRequestHandler):
    """Handler pour le dashboard d'affectation ressources"""
    
    def do_GET(self):
        """Handle GET requests"""
        path = urlparse(self.path).path
        
        if path == "/":
            self.serve_dashboard()
        elif path == "/api/resources":
            self.serve_resource_data()
        elif path == "/api/refresh":
            self.serve_refresh_data()
        else:
            self.send_error(404)
    
    def serve_dashboard(self):
        """Sert le dashboard HTML"""
        html = self.generate_dashboard_html()
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_resource_data(self):
        """Sert les données de ressources en JSON"""
        monitor = ResourceAllocationMonitor()
        data = monitor.generate_allocation_report()
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def serve_refresh_data(self):
        """Sert des données rafraîchies"""
        monitor = ResourceAllocationMonitor()
        report = monitor.generate_allocation_report()
        
        # Format simplifié pour rafraîchissement rapide
        refresh_data = {
            "timestamp": report["timestamp_human"],
            "gpu_summary": {
                "hd7750": {
                    "temp": report["gpu_allocations"]["hd7750"]["temperature"],
                    "usage": report["gpu_allocations"]["hd7750"]["utilization"],
                    "processes": len(report["gpu_allocations"]["hd7750"]["current_processes"])
                },
                "rx480": {
                    "temp": report["gpu_allocations"]["rx480"]["temperature"], 
                    "usage": report["gpu_allocations"]["rx480"]["utilization"],
                    "processes": len(report["gpu_allocations"]["rx480"]["current_processes"])
                }
            },
            "system_summary": {
                "cpu_usage": max(report["cpu_allocations"]["per_core_usage"]),
                "memory_percent": report["memory_allocations"]["percent_used"],
                "panini_processes": len(report["cpu_allocations"]["panini_processes"]),
                "panini_memory": report["memory_allocations"]["panini_memory_usage"]
            }
        }
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(refresh_data).encode())
    
    def generate_dashboard_html(self):
        """Génère le HTML du dashboard"""
        return """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 PaniniFS - Affectation Ressources</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        .card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .card h3 {
            margin-top: 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .gpu-status {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 10px 0;
            padding: 10px;
            background: rgba(0,0,0,0.2);
            border-radius: 8px;
        }
        .metric-value {
            font-size: 1.2em;
            font-weight: bold;
            color: #4ade80;
        }
        .high-usage {
            color: #f87171;
        }
        .process-list {
            max-height: 200px;
            overflow-y: auto;
            margin-top: 10px;
        }
        .process-item {
            display: flex;
            justify-content: space-between;
            padding: 5px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .refresh-btn {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #10b981;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
        }
        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
        }
        .status-active { background: #10b981; }
        .status-idle { background: #fbbf24; }
        .status-offline { background: #ef4444; }
        .auto-refresh {
            position: fixed;
            top: 70px;
            right: 20px;
            font-size: 0.9em;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 PaniniFS Research - Affectation Ressources</h1>
            <p id="timestamp">Chargement...</p>
        </div>
        
        <button class="refresh-btn" onclick="refreshData()">🔄 Actualiser</button>
        <div class="auto-refresh">Auto-refresh: <span id="countdown">30</span>s</div>
        
        <div class="grid">
            <!-- GPU Status -->
            <div class="card">
                <h3>🖥️ Status GPU Dual</h3>
                <div class="gpu-status">
                    <div>
                        <strong>HD 7750 (Display)</strong><br>
                        <span class="status-indicator status-active"></span>
                        <span id="hd7750-temp">--</span>°C | 
                        <span id="hd7750-usage">--</span>% | 
                        <span id="hd7750-processes">--</span> processus
                    </div>
                </div>
                <div class="gpu-status">
                    <div>
                        <strong>RX 480 (Compute)</strong><br>
                        <span class="status-indicator status-active"></span>
                        <span id="rx480-temp">--</span>°C | 
                        <span id="rx480-usage">--</span>% | 
                        <span id="rx480-processes">--</span> processus
                    </div>
                </div>
            </div>
            
            <!-- CPU Allocation -->
            <div class="card">
                <h3>🧠 Affectation CPU</h3>
                <div id="cpu-summary">Chargement...</div>
                <div class="process-list" id="panini-processes">
                </div>
            </div>
            
            <!-- Memory Usage -->
            <div class="card">
                <h3>💾 Utilisation Mémoire</h3>
                <div id="memory-summary">Chargement...</div>
                <div class="process-list" id="memory-processes">
                </div>
            </div>
            
            <!-- Research Activities -->
            <div class="card">
                <h3>🔬 Activités Recherche</h3>
                <div id="research-summary">Chargement...</div>
            </div>
        </div>
    </div>

    <script>
        let refreshInterval;
        let countdown = 30;
        
        function refreshData() {
            console.log('Refreshing data...');
            
            fetch('/api/refresh')
                .then(response => response.json())
                .then(data => {
                    updateDashboard(data);
                    resetCountdown();
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                });
        }
        
        function updateDashboard(data) {
            // Update timestamp
            document.getElementById('timestamp').textContent = 
                `Dernière mise à jour: ${data.timestamp}`;
            
            // Update GPU status
            const hd7750 = data.gpu_summary.hd7750;
            document.getElementById('hd7750-temp').textContent = hd7750.temp;
            document.getElementById('hd7750-usage').textContent = hd7750.usage;
            document.getElementById('hd7750-processes').textContent = hd7750.processes;
            
            const rx480 = data.gpu_summary.rx480;
            document.getElementById('rx480-temp').textContent = rx480.temp;
            document.getElementById('rx480-usage').textContent = rx480.usage;
            document.getElementById('rx480-processes').textContent = rx480.processes;
            
            // Update CPU summary
            const system = data.system_summary;
            document.getElementById('cpu-summary').innerHTML = `
                <div class="gpu-status">
                    <span>CPU Max: <span class="metric-value ${system.cpu_usage > 80 ? 'high-usage' : ''}">${system.cpu_usage.toFixed(1)}%</span></span>
                    <span>Processus PaniniFS: <span class="metric-value">${system.panini_processes}</span></span>
                </div>
            `;
            
            // Update Memory summary
            document.getElementById('memory-summary').innerHTML = `
                <div class="gpu-status">
                    <span>RAM: <span class="metric-value ${system.memory_percent > 80 ? 'high-usage' : ''}">${system.memory_percent.toFixed(1)}%</span></span>
                    <span>PaniniFS: <span class="metric-value">${system.panini_memory}MB</span></span>
                </div>
            `;
        }
        
        function resetCountdown() {
            countdown = 30;
            document.getElementById('countdown').textContent = countdown;
        }
        
        function startAutoRefresh() {
            refreshInterval = setInterval(() => {
                countdown--;
                document.getElementById('countdown').textContent = countdown;
                
                if (countdown <= 0) {
                    refreshData();
                }
            }, 1000);
        }
        
        // Initial load
        refreshData();
        startAutoRefresh();
        
        // Load full data on page load
        fetch('/api/resources')
            .then(response => response.json())
            .then(data => {
                console.log('Full resource data loaded:', data);
                
                // Update research summary
                const summary = data.executive_summary;
                document.getElementById('research-summary').innerHTML = `
                    <div class="gpu-status">
                        <span>RX480 Actif: <span class="metric-value">${summary.rx480_active ? '✅' : '❌'}</span></span>
                        <span>Charge CPU: <span class="metric-value ${summary.cpu_load_high ? 'high-usage' : ''}">${summary.cpu_load_high ? 'Élevée' : 'Normale'}</span></span>
                    </div>
                    <div class="gpu-status">
                        <span>Pression Mémoire: <span class="metric-value ${summary.memory_pressure ? 'high-usage' : ''}">${summary.memory_pressure ? 'Élevée' : 'Normale'}</span></span>
                        <span>Processus Total: <span class="metric-value">${summary.total_panini_processes}</span></span>
                    </div>
                `;
            });
    </script>
</body>
</html>
        """

def start_resource_dashboard(port=8889):
    """Démarre le dashboard d'affectation ressources"""
    
    class ThreadedHTTPServer(HTTPServer):
        def __init__(self, server_address, RequestHandlerClass):
            super().__init__(server_address, RequestHandlerClass)
            self.daemon_threads = True
    
    server = ThreadedHTTPServer(("localhost", port), ResourceDashboardHandler)
    
    print(f"🎯 Dashboard Ressources démarré sur http://localhost:{port}")
    print(f"📊 Affichage: Affectation GPU dual + CPU + Mémoire")
    print(f"🔄 Auto-refresh: 30 secondes")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Dashboard arrêté")
        server.shutdown()

if __name__ == "__main__":
    start_resource_dashboard()