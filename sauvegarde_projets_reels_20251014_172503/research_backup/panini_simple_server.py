#!/usr/bin/env python3
"""
🌐 PANINI-FS SIMPLE HTTP SERVER
============================================================
🎯 Mission: Serveur HTTP simple pour démonstration VFS
🔬 Focus: Navigation contenu, API basique, sans dépendances
🚀 Utilise seulement modules Python standards

Serveur de démonstration pour architecture VFS PaniniFS
sans dépendances externes.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
import webbrowser
import threading
import time

class PaniniSimpleAPIHandler(BaseHTTPRequestHandler):
    """Handler HTTP simple pour API PaniniFS"""
    
    def __init__(self, *args, vfs_data=None, **kwargs):
        self.vfs_data = vfs_data or {}
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handler GET pour API et interface"""
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        
        print(f"📥 GET {path}")
        
        # Routes API
        if path == '/api/health':
            self._send_json({'status': 'healthy', 'vfs_loaded': bool(self.vfs_data)})
        
        elif path == '/api/nodes':
            self._handle_get_nodes()
        
        elif path == '/api/graph':
            self._handle_get_graph()
        
        elif path.startswith('/api/content/'):
            node_id = path.split('/')[-1]
            self._handle_get_content(node_id)
        
        elif path == '/api/semantic/search':
            query_param = query.get('query', [''])[0]
            self._handle_semantic_search(query_param)
        
        # Interface web
        elif path == '/' or path == '/index.html':
            self._serve_web_interface()
        
        # Fichiers statiques
        elif path.endswith('.css'):
            self._serve_css()
        elif path.endswith('.js'):
            self._serve_js()
        
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        """Handler POST pour opérations"""
        parsed = urlparse(self.path)
        path = parsed.path
        
        print(f"📤 POST {path}")
        
        if path.startswith('/api/decompose/'):
            node_id = path.split('/')[-1]
            self._handle_decompose(node_id)
        
        elif path == '/api/generate':
            self._handle_generate()
        
        else:
            self.send_error(404, "Not Found")
    
    def _send_json(self, data):
        """Envoyer réponse JSON"""
        response = json.dumps(data, indent=2, ensure_ascii=False)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(response.encode())))
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))
    
    def _handle_get_nodes(self):
        """Récupérer tous les nœuds"""
        if not self.vfs_data:
            self._send_json({'error': 'VFS not loaded'})
            return
        
        node_registry = self.vfs_data.get('virtual_filesystem', {}).get('structure', {}).get('node_registry', {})
        
        nodes = []
        for node_id, node_data in node_registry.items():
            nodes.append({
                'node_id': node_id,
                'content_type': node_data.get('content_type', 'unknown'),
                'size_original': node_data.get('size_original', 0),
                'generative_potential': node_data.get('generative_potential', 0.0),
                'semantic_tags': node_data.get('semantic_tags', []),
                'decomposition_level': node_data.get('decomposition_level', 0)
            })
        
        self._send_json(nodes)
    
    def _handle_get_graph(self):
        """Récupérer structure graphique"""
        if not self.vfs_data:
            self._send_json({'error': 'VFS not loaded'})
            return
        
        node_registry = self.vfs_data.get('virtual_filesystem', {}).get('structure', {}).get('node_registry', {})
        dedup_map = self.vfs_data.get('virtual_filesystem', {}).get('structure', {}).get('deduplication_map', {})
        
        # Construire nœuds
        nodes = []
        for node_id, node_data in node_registry.items():
            nodes.append({
                'id': node_id,
                'name': node_id[:16] + '...',
                'type': 'content',
                'size': node_data.get('size_original', 1000),
                'generative_potential': node_data.get('generative_potential', 0.0),
                'semantic_tags': node_data.get('semantic_tags', []),
                'content_type': node_data.get('content_type', 'unknown')
            })
        
        # Construire arêtes de déduplication
        edges = []
        content_to_files = {}
        for filename, node_id in dedup_map.items():
            if node_id not in content_to_files:
                content_to_files[node_id] = []
            content_to_files[node_id].append(filename)
        
        for node_id, files in content_to_files.items():
            if len(files) > 1:
                edges.append({
                    'source': node_id,
                    'target': node_id,
                    'type': 'duplicate',
                    'files': files
                })
        
        graph_data = {
            'nodes': nodes,
            'edges': edges,
            'stats': {
                'total_nodes': len(nodes),
                'total_edges': len(edges),
                'duplicate_groups': len([g for g in content_to_files.values() if len(g) > 1])
            }
        }
        
        self._send_json(graph_data)
    
    def _handle_get_content(self, node_id):
        """Récupérer contenu d'un nœud"""
        if not self.vfs_data:
            self._send_json({'error': 'VFS not loaded'})
            return
        
        node_registry = self.vfs_data.get('virtual_filesystem', {}).get('structure', {}).get('node_registry', {})
        
        if node_id not in node_registry:
            self._send_json({'error': 'Node not found'})
            return
        
        node_data = node_registry[node_id]
        
        content_info = {
            'node_id': node_id,
            'metadata': node_data,
            'content_preview': f"Contenu simulé pour nœud {node_id}",
            'analysis': {
                'size_efficiency': node_data.get('size_compressed', 0) / max(node_data.get('size_original', 1), 1),
                'semantic_richness': len(node_data.get('semantic_tags', [])),
                'generative_score': node_data.get('generative_potential', 0.0)
            }
        }
        
        self._send_json(content_info)
    
    def _handle_semantic_search(self, query):
        """Recherche sémantique"""
        if not query:
            self._send_json({'error': 'Query required'})
            return
        
        node_registry = self.vfs_data.get('virtual_filesystem', {}).get('structure', {}).get('node_registry', {})
        
        results = []
        query_lower = query.lower()
        
        for node_id, node_data in node_registry.items():
            score = 0.0
            semantic_tags = node_data.get('semantic_tags', [])
            
            for tag in semantic_tags:
                if query_lower in tag.lower():
                    score += 1.0
            
            if score > 0:
                results.append({
                    'node_id': node_id,
                    'score': score,
                    'matched_tags': [tag for tag in semantic_tags if query_lower in tag.lower()],
                    'generative_potential': node_data.get('generative_potential', 0.0)
                })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        
        self._send_json({
            'query': query,
            'results': results[:10],
            'total_found': len(results)
        })
    
    def _handle_decompose(self, node_id):
        """Décomposer un nœud"""
        # Simulation décomposition
        result = {
            'original_node': node_id,
            'strategy': 'structural',
            'components': [
                {'name': 'header', 'size': 1024, 'type': 'metadata'},
                {'name': 'content', 'size': 50000, 'type': 'data'},
                {'name': 'footer', 'size': 512, 'type': 'metadata'}
            ]
        }
        self._send_json(result)
    
    def _handle_generate(self):
        """Générer nouveau contenu"""
        generated = {
            'node_id': f"generated_{int(time.time())}",
            'operation': 'combine',
            'result': {
                'size_estimated': 45000,
                'content_type': 'synthetic',
                'generative_potential': 0.9
            }
        }
        self._send_json(generated)
    
    def _serve_web_interface(self):
        """Servir interface web intégrée"""
        html = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PaniniFS Explorer</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1400px; margin: 0 auto; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .dashboard { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-bottom: 20px; }
        .panel { background: white; border-radius: 8px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .graph-container { height: 600px; border: 1px solid #ddd; border-radius: 4px; }
        .controls button { margin-right: 10px; padding: 8px 16px; border: none; border-radius: 4px; background: #007bff; color: white; cursor: pointer; }
        .controls button:hover { background: #0056b3; }
        .node { cursor: pointer; stroke: #fff; stroke-width: 2px; }
        .node:hover { stroke: #333; stroke-width: 3px; }
        .link { stroke: #999; stroke-opacity: 0.6; }
        .semantic-tag { background: #e1f5fe; padding: 2px 6px; border-radius: 3px; margin: 0 2px; }
        .loading { text-align: center; padding: 50px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌐 PaniniFS Explorer</h1>
            <p>Interface d'exploration du système de fichiers virtuel PaniniFS</p>
        </div>
        
        <div class="dashboard">
            <div class="panel">
                <h2>📊 Graphe des Nœuds</h2>
                <div class="controls">
                    <button onclick="loadGraph()">Charger Graphe</button>
                    <button onclick="resetView()">Reset</button>
                </div>
                <div id="graph" class="graph-container">
                    <div class="loading">Cliquez sur "Charger Graphe" pour voir la visualisation</div>
                </div>
            </div>
            
            <div class="panel">
                <h2>🔍 Détails</h2>
                <div id="node-details">
                    <p>Cliquez sur un nœud pour voir ses détails</p>
                </div>
                
                <h3>🏷️ Recherche</h3>
                <input type="text" id="search-input" placeholder="Rechercher..." style="width: 100%; padding: 8px;">
                <button onclick="performSearch()" style="margin-top: 10px;">Rechercher</button>
                <div id="search-results"></div>
            </div>
        </div>
        
        <div class="panel">
            <h2>📈 Statistiques</h2>
            <div id="stats"></div>
        </div>
    </div>

    <script>
        let graphData = null;
        let simulation = null;
        
        async function loadGraph() {
            try {
                const response = await fetch('/api/graph');
                graphData = await response.json();
                renderGraph(graphData);
                updateStats(graphData.stats);
            } catch (error) {
                console.error('Erreur chargement graphe:', error);
                document.getElementById('graph').innerHTML = '<div class="loading">Erreur de chargement</div>';
            }
        }
        
        function renderGraph(data) {
            const container = d3.select("#graph");
            container.selectAll("*").remove();
            
            const width = 750;
            const height = 550;
            
            const svg = container.append("svg")
                .attr("width", width)
                .attr("height", height);
            
            simulation = d3.forceSimulation(data.nodes)
                .force("link", d3.forceLink(data.edges).id(d => d.id).distance(100))
                .force("charge", d3.forceManyBody().strength(-300))
                .force("center", d3.forceCenter(width / 2, height / 2));
            
            const link = svg.append("g")
                .selectAll("line")
                .data(data.edges)
                .enter().append("line")
                .attr("class", "link")
                .attr("stroke-width", 2);
            
            const node = svg.append("g")
                .selectAll("circle")
                .data(data.nodes)
                .enter().append("circle")
                .attr("class", "node")
                .attr("r", d => Math.max(5, Math.sqrt(d.size) / 200))
                .attr("fill", d => {
                    switch(d.content_type) {
                        case 'pdf': return '#f44336';
                        case 'jpg': return '#4caf50';
                        case 'txt': return '#2196f3';
                        default: return '#ff9800';
                    }
                })
                .on("click", function(event, d) {
                    showNodeDetails(d);
                    d3.selectAll(".node").style("opacity", 0.3);
                    d3.select(this).style("opacity", 1);
                });
            
            simulation.on("tick", () => {
                link
                    .attr("x1", d => d.source.x)
                    .attr("y1", d => d.source.y)
                    .attr("x2", d => d.target.x)
                    .attr("y2", d => d.target.y);
                
                node
                    .attr("cx", d => d.x)
                    .attr("cy", d => d.y);
            });
        }
        
        async function showNodeDetails(node) {
            try {
                const response = await fetch(`/api/content/${node.id}`);
                const details = await response.json();
                
                const tags = node.semantic_tags.map(tag => 
                    `<span class="semantic-tag">${tag}</span>`
                ).join('');
                
                document.getElementById('node-details').innerHTML = `
                    <h4>${node.name}</h4>
                    <p><strong>Type:</strong> ${node.content_type}</p>
                    <p><strong>Taille:</strong> ${(node.size / 1024).toFixed(1)} KB</p>
                    <p><strong>Potentiel Génératif:</strong> ${(node.generative_potential * 100).toFixed(0)}%</p>
                    <p><strong>Tags:</strong></p>
                    <div>${tags}</div>
                `;
            } catch (error) {
                console.error('Erreur détails nœud:', error);
            }
        }
        
        async function performSearch() {
            const query = document.getElementById('search-input').value;
            if (!query) return;
            
            try {
                const response = await fetch(`/api/semantic/search?query=${encodeURIComponent(query)}`);
                const results = await response.json();
                
                const resultsHtml = results.results.map(result => 
                    `<div style="padding: 8px; border-left: 3px solid #4caf50; margin: 5px 0; background: #f8f9fa;">
                        <strong>Nœud ${result.node_id.substring(0, 16)}...</strong><br>
                        <small>Score: ${result.score}, Tags: ${result.matched_tags.join(', ')}</small>
                    </div>`
                ).join('');
                
                document.getElementById('search-results').innerHTML = resultsHtml || '<p>Aucun résultat</p>';
            } catch (error) {
                console.error('Erreur recherche:', error);
            }
        }
        
        function updateStats(stats) {
            document.getElementById('stats').innerHTML = `
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;">
                    <div style="text-align: center;">
                        <div style="font-size: 24px; font-weight: bold; color: #4CAF50;">${stats.total_nodes}</div>
                        <div>Nœuds Uniques</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 24px; font-weight: bold; color: #f44336;">${stats.duplicate_groups}</div>
                        <div>Groupes Doublons</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 24px; font-weight: bold; color: #2196F3;">${stats.total_edges}</div>
                        <div>Relations</div>
                    </div>
                </div>
            `;
        }
        
        function resetView() {
            if (simulation) {
                d3.selectAll(".node").style("opacity", 1);
                document.getElementById('node-details').innerHTML = '<p>Cliquez sur un nœud pour voir ses détails</p>';
            }
        }
    </script>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(html.encode())))
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Personnaliser logs"""
        pass  # Réduire verbosité

class PaniniSimpleServer:
    """Serveur HTTP simple pour PaniniFS"""
    
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.vfs_data = {}
        self.server = None
        
    def load_vfs_data(self):
        """Charger données VFS"""
        # Charger architecture VFS la plus récente
        arch_files = list(Path(".").glob("panini_vfs_architecture_*.json"))
        if arch_files:
            latest_arch = max(arch_files, key=os.path.getctime)
            with open(latest_arch, 'r', encoding='utf-8') as f:
                self.vfs_data = json.load(f)
            print(f"✅ VFS chargé: {latest_arch}")
        else:
            print("⚠️ Aucune architecture VFS trouvée")
    
    def create_handler_class(self):
        """Créer classe handler avec VFS"""
        vfs_data = self.vfs_data
        
        class BoundHandler(PaniniSimpleAPIHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, vfs_data=vfs_data, **kwargs)
        
        return BoundHandler
    
    def start(self):
        """Démarrer serveur"""
        self.load_vfs_data()
        
        handler_class = self.create_handler_class()
        self.server = HTTPServer((self.host, self.port), handler_class)
        
        print(f"🌐 Serveur PaniniFS démarré")
        print(f"📍 URL: http://{self.host}:{self.port}")
        print(f"📊 Nœuds VFS: {len(self.vfs_data.get('virtual_filesystem', {}).get('structure', {}).get('node_registry', {}))}")
        
        # Ouvrir navigateur automatiquement
        def open_browser():
            time.sleep(1)
            webbrowser.open(f"http://{self.host}:{self.port}")
        
        threading.Thread(target=open_browser, daemon=True).start()
        
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Arrêt serveur")
            self.server.shutdown()

def main():
    """Point d'entrée"""
    print("🌐 PANINI-FS SIMPLE SERVER")
    print("="*40)
    
    server = PaniniSimpleServer(host='localhost', port=8000)
    server.start()

if __name__ == "__main__":
    main()