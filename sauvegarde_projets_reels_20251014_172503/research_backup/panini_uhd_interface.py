#!/usr/bin/env python3
"""
🖥️ PANINI-FS INTERFACE UHD/4K CÔTE À CÔTE
============================================================
🎯 Mission: Interface professionnelle pour écrans UHD/4K
🔬 Focus: Document reconstitué + représentation interne colorée
🌐 Layout: Arbre (gauche) | Document PDF (centre) | Graphe détaillé (droite)

Interface optimisée pour écrans UHD/4K avec:
- Panneau gauche: Arbre de contenu navigable
- Panneau centre: Document reconstitué (PDF, texte, etc.)
- Panneau droite: Graphe détaillé avec couleurs hiérarchiques
- Rouge: Privé | Jaune: Confidentiel | Vert: Public
"""

import json
import base64
import mimetypes
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
import threading
import webbrowser

class PaniniUHDInterfaceHandler(BaseHTTPRequestHandler):
    """Handler pour interface UHD/4K côte à côte"""
    
    def __init__(self, *args, vfs_data=None, **kwargs):
        self.vfs_data = vfs_data or {}
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handler pour interface UHD"""
        parsed = urlparse(self.path)
        path = parsed.path
        
        print(f"🖥️ UHD Request: {path}")
        
        if path == '/' or path == '/uhd':
            self._serve_uhd_interface()
        elif path.startswith('/api/document/'):
            document_id = path.split('/')[-1]
            self._serve_document_content(document_id)
        elif path.startswith('/api/graph/'):
            node_id = path.split('/')[-1]
            self._serve_node_graph(node_id)
        elif path == '/api/tree':
            self._serve_content_tree()
        elif path.startswith('/static/'):
            self._serve_static_file(path)
        else:
            self._serve_404()
    
    def _serve_uhd_interface(self):
        """Interface principale UHD/4K"""
        html = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🖥️ PaniniFS - Interface UHD/4K Côte à Côte</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #ffffff;
            overflow: hidden;
            height: 100vh;
        }
        
        .uhd-container {
            display: grid;
            grid-template-columns: 350px 1fr 500px;
            grid-template-rows: 60px 1fr;
            height: 100vh;
            gap: 2px;
        }
        
        .top-bar {
            grid-column: 1 / -1;
            background: rgba(0,0,0,0.3);
            display: flex;
            align-items: center;
            padding: 0 20px;
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        .top-bar h1 {
            font-size: 1.8em;
            font-weight: 300;
            margin-right: auto;
        }
        
        .status-indicators {
            display: flex;
            gap: 15px;
            align-items: center;
        }
        
        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        .status-dot.private { background: #ff4757; }
        .status-dot.confidential { background: #ffa502; }
        .status-dot.public { background: #2ed573; }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }
        
        .content-tree {
            background: rgba(0,0,0,0.2);
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255,255,255,0.1);
            overflow-y: auto;
            padding: 20px;
        }
        
        .document-viewer {
            background: rgba(255,255,255,0.95);
            color: #333;
            display: flex;
            flex-direction: column;
            position: relative;
        }
        
        .document-header {
            background: rgba(0,0,0,0.1);
            padding: 15px 20px;
            border-bottom: 1px solid rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .document-content {
            flex: 1;
            overflow: auto;
            padding: 20px;
            background: #ffffff;
        }
        
        .graph-panel {
            background: rgba(0,0,0,0.2);
            backdrop-filter: blur(10px);
            border-left: 1px solid rgba(255,255,255,0.1);
            display: flex;
            flex-direction: column;
            padding: 20px;
            overflow: hidden;
        }
        
        .tree-item {
            display: flex;
            align-items: center;
            padding: 8px 12px;
            margin: 2px 0;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            position: relative;
        }
        
        .tree-item:hover {
            background: rgba(255,255,255,0.1);
            transform: translateX(4px);
        }
        
        .tree-item.selected {
            background: rgba(74, 144, 226, 0.3);
            border-left: 4px solid #4a90e2;
        }
        
        .tree-item.private { border-left: 4px solid #ff4757; }
        .tree-item.confidential { border-left: 4px solid #ffa502; }
        .tree-item.public { border-left: 4px solid #2ed573; }
        
        .tree-icon {
            margin-right: 10px;
            font-size: 1.1em;
        }
        
        .tree-label {
            flex: 1;
            font-size: 0.9em;
        }
        
        .tree-meta {
            font-size: 0.75em;
            opacity: 0.7;
        }
        
        .graph-container {
            flex: 1;
            position: relative;
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            margin-top: 10px;
            overflow: hidden;
        }
        
        .graph-svg {
            width: 100%;
            height: 100%;
        }
        
        .node {
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .node:hover {
            filter: brightness(1.2);
            transform: scale(1.1);
        }
        
        .node.private { fill: #ff4757; }
        .node.confidential { fill: #ffa502; }
        .node.public { fill: #2ed573; }
        .node.mixed { fill: url(#gradient-mixed); }
        
        .link {
            stroke: rgba(255,255,255,0.3);
            stroke-width: 2;
        }
        
        .link.private { stroke: #ff4757; }
        .link.confidential { stroke: #ffa502; }
        .link.public { stroke: #2ed573; }
        
        .node-label {
            fill: #ffffff;
            font-size: 11px;
            text-anchor: middle;
            pointer-events: none;
            font-weight: 500;
        }
        
        .pdf-viewer {
            width: 100%;
            height: 100%;
            border: none;
        }
        
        .text-content {
            line-height: 1.6;
            font-size: 14px;
            white-space: pre-wrap;
            font-family: 'Monaco', 'Consolas', monospace;
        }
        
        .loading {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            font-size: 1.2em;
            opacity: 0.7;
        }
        
        .document-meta {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            color: #495057;
        }
        
        .meta-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
        }
        
        .meta-item {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        
        .meta-label {
            font-size: 0.8em;
            font-weight: 600;
            color: #6c757d;
            text-transform: uppercase;
        }
        
        .meta-value {
            font-size: 0.9em;
            color: #495057;
            font-family: 'Monaco', monospace;
        }
        
        .privacy-badge {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.75em;
            font-weight: 600;
            text-transform: uppercase;
            color: white;
        }
        
        .privacy-badge.private { background: #ff4757; }
        .privacy-badge.confidential { background: #ffa502; }
        .privacy-badge.public { background: #2ed573; }
        
        .graph-legend {
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(0,0,0,0.7);
            padding: 10px;
            border-radius: 8px;
            font-size: 0.8em;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 5px;
        }
        
        .legend-color {
            width: 16px;
            height: 16px;
            border-radius: 50%;
        }
        
        .zoom-controls {
            position: absolute;
            bottom: 10px;
            right: 10px;
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
        
        .zoom-btn {
            width: 35px;
            height: 35px;
            background: rgba(0,0,0,0.7);
            border: none;
            border-radius: 50%;
            color: white;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2em;
        }
        
        .zoom-btn:hover {
            background: rgba(0,0,0,0.9);
        }
    </style>
</head>
<body>
    <div class="uhd-container">
        <div class="top-bar">
            <h1>🖥️ PaniniFS - Interface UHD/4K</h1>
            <div class="status-indicators">
                <span style="font-size: 0.9em; margin-right: 15px;">Niveaux hiérarchiques:</span>
                <div class="status-dot private"></div>
                <span style="font-size: 0.8em;">Privé</span>
                <div class="status-dot confidential"></div>
                <span style="font-size: 0.8em;">Confidentiel</span>
                <div class="status-dot public"></div>
                <span style="font-size: 0.8em;">Public</span>
            </div>
        </div>
        
        <div class="content-tree">
            <h3 style="margin-bottom: 15px; font-weight: 300;">📁 Arbre de Contenu</h3>
            <div id="tree-content">
                <div class="loading">Chargement...</div>
            </div>
        </div>
        
        <div class="document-viewer">
            <div class="document-header">
                <div>
                    <span id="doc-title">Sélectionnez un document</span>
                    <span id="doc-privacy-badge" class="privacy-badge" style="margin-left: 10px; display: none;"></span>
                </div>
                <div style="display: flex; gap: 10px;">
                    <button onclick="toggleMetadata()" style="padding: 6px 12px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;">📊 Métadonnées</button>
                    <button onclick="refreshDocument()" style="padding: 6px 12px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer;">🔄 Actualiser</button>
                </div>
            </div>
            <div class="document-content">
                <div id="document-display" class="loading">
                    <div style="text-align: center; padding: 40px;">
                        <h3>🚀 Bienvenue dans l'Interface UHD PaniniFS</h3>
                        <p style="margin: 20px 0; line-height: 1.6;">
                            Cette interface optimisée pour écrans UHD/4K vous permet de visualiser côte à côte :<br>
                            <strong>• Gauche :</strong> Arbre de contenu navigable<br>
                            <strong>• Centre :</strong> Document reconstitué (PDF, texte, images)<br>
                            <strong>• Droite :</strong> Graphe détaillé avec couleurs hiérarchiques
                        </p>
                        <p style="color: #666;">
                            <strong>🎨 Code couleur :</strong><br>
                            🔴 Rouge = Privé exclusif | 🟡 Jaune = Confidentiel teams | 🟢 Vert = Public anonymisé
                        </p>
                        <p style="margin-top: 30px; font-style: italic;">
                            Sélectionnez un fichier dans l'arbre pour commencer l'exploration.
                        </p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="graph-panel">
            <h3 style="margin-bottom: 15px; font-weight: 300;">🕸️ Graphe Détaillé</h3>
            <div class="graph-container">
                <svg class="graph-svg" id="graph-svg">
                    <defs>
                        <radialGradient id="gradient-mixed" cx="50%" cy="50%" r="50%">
                            <stop offset="0%" style="stop-color:#ff4757"/>
                            <stop offset="50%" style="stop-color:#ffa502"/>
                            <stop offset="100%" style="stop-color:#2ed573"/>
                        </radialGradient>
                    </defs>
                </svg>
                
                <div class="graph-legend">
                    <div class="legend-item">
                        <div class="legend-color" style="background: #ff4757;"></div>
                        <span>Nœud Privé</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="background: #ffa502;"></div>
                        <span>Nœud Confidentiel</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="background: #2ed573;"></div>
                        <span>Nœud Public</span>
                    </div>
                </div>
                
                <div class="zoom-controls">
                    <button class="zoom-btn" onclick="zoomGraph(1.2)">+</button>
                    <button class="zoom-btn" onclick="zoomGraph(0.8)">−</button>
                    <button class="zoom-btn" onclick="resetZoom()">⌂</button>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <script>
        let currentDocument = null;
        let currentGraph = null;
        let graphTransform = d3.zoomIdentity;
        let showMetadata = false;
        
        // Charger l'arbre de contenu
        function loadContentTree() {
            fetch('/api/tree')
                .then(r => r.json())
                .then(data => displayContentTree(data))
                .catch(e => {
                    document.getElementById('tree-content').innerHTML = 
                        '<div style="color: #ff4757;">❌ Erreur: ' + e.message + '</div>';
                });
        }
        
        function displayContentTree(data) {
            const container = document.getElementById('tree-content');
            let html = '';
            
            if (data.nodes) {
                data.nodes.forEach(node => {
                    const privacyLevel = determinePrivacyLevel(node);
                    const icon = getFileIcon(node.content_type);
                    const size = node.size_original ? formatFileSize(node.size_original) : '';
                    
                    html += `
                        <div class="tree-item ${privacyLevel}" onclick="selectDocument('${node.node_id}')">
                            <span class="tree-icon">${icon}</span>
                            <div class="tree-label">
                                <div>${node.filename || node.node_id.substring(0, 12)}</div>
                                <div class="tree-meta">${size} • ${node.content_type || 'unknown'}</div>
                            </div>
                        </div>
                    `;
                });
            }
            
            container.innerHTML = html || '<div style="color: #ffa502;">📁 Aucun contenu</div>';
        }
        
        function determinePrivacyLevel(node) {
            const metadata = node.metadata || {};
            const hints = metadata.semantic_hints || [];
            
            // Logique de classification basée sur les indices sémantiques
            if (hints.some(h => h.includes('personal') || h.includes('private'))) {
                return 'private';
            } else if (hints.some(h => h.includes('team') || h.includes('project'))) {
                return 'confidential';
            }
            return 'public';
        }
        
        function getFileIcon(contentType) {
            if (!contentType) return '📄';
            if (contentType.includes('pdf')) return '📕';
            if (contentType.includes('image')) return '🖼️';
            if (contentType.includes('text')) return '📝';
            if (contentType.includes('audio')) return '🎵';
            if (contentType.includes('video')) return '🎬';
            return '📄';
        }
        
        function formatFileSize(bytes) {
            if (bytes < 1024) return bytes + ' B';
            if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
            return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
        }
        
        function selectDocument(nodeId) {
            // Marquer comme sélectionné
            document.querySelectorAll('.tree-item').forEach(item => {
                item.classList.remove('selected');
            });
            event.target.closest('.tree-item').classList.add('selected');
            
            currentDocument = nodeId;
            
            // Charger le document
            fetch(`/api/document/${nodeId}`)
                .then(r => r.json())
                .then(data => displayDocument(data))
                .catch(e => {
                    document.getElementById('document-display').innerHTML = 
                        '<div class="loading">❌ Erreur chargement: ' + e.message + '</div>';
                });
            
            // Charger le graphe
            fetch(`/api/graph/${nodeId}`)
                .then(r => r.json())
                .then(data => displayGraph(data))
                .catch(e => console.log('Graphe non disponible:', e));
        }
        
        function displayDocument(data) {
            const display = document.getElementById('document-display');
            const title = document.getElementById('doc-title');
            const badge = document.getElementById('doc-privacy-badge');
            
            title.textContent = data.filename || data.node_id;
            
            // Badge de confidentialité
            badge.className = `privacy-badge ${data.privacy_level || 'public'}`;
            badge.textContent = data.privacy_level || 'public';
            badge.style.display = 'inline-block';
            
            let content = '';
            
            // Métadonnées (optionnelles)
            if (showMetadata) {
                content += `
                    <div class="document-meta">
                        <h4 style="margin-bottom: 10px;">📊 Métadonnées du Document</h4>
                        <div class="meta-grid">
                            <div class="meta-item">
                                <span class="meta-label">Node ID</span>
                                <span class="meta-value">${data.node_id}</span>
                            </div>
                            <div class="meta-item">
                                <span class="meta-label">Type</span>
                                <span class="meta-value">${data.content_type || 'N/A'}</span>
                            </div>
                            <div class="meta-item">
                                <span class="meta-label">Taille</span>
                                <span class="meta-value">${data.size_original ? formatFileSize(data.size_original) : 'N/A'}</span>
                            </div>
                            <div class="meta-item">
                                <span class="meta-label">Hash</span>
                                <span class="meta-value">${data.content_hash ? data.content_hash.substring(0, 16) + '...' : 'N/A'}</span>
                            </div>
                            <div class="meta-item">
                                <span class="meta-label">Compression</span>
                                <span class="meta-value">${data.compression_ratio || 'N/A'}%</span>
                            </div>
                            <div class="meta-item">
                                <span class="meta-label">Confidentialité</span>
                                <span class="meta-value privacy-badge ${data.privacy_level || 'public'}">${data.privacy_level || 'public'}</span>
                            </div>
                        </div>
                    </div>
                `;
            }
            
            // Contenu du document
            if (data.content_type && data.content_type.includes('pdf') && data.content_url) {
                content += `<iframe class="pdf-viewer" src="${data.content_url}" type="application/pdf"></iframe>`;
            } else if (data.content) {
                content += `<div class="text-content">${data.content}</div>`;
            } else {
                content += `
                    <div class="loading">
                        <div style="text-align: center;">
                            <h4>📄 ${data.filename || 'Document'}</h4>
                            <p style="margin: 15px 0;">Type: ${data.content_type || 'Inconnu'}</p>
                            <p style="color: #666;">Contenu non disponible pour prévisualisation</p>
                            <p style="margin-top: 20px; font-size: 0.9em;">
                                Le document est référencé dans le VFS avec déduplication.<br>
                                Visualisez le graphe à droite pour voir sa structure interne.
                            </p>
                        </div>
                    </div>
                `;
            }
            
            display.innerHTML = content;
        }
        
        function displayGraph(data) {
            const svg = d3.select('#graph-svg');
            svg.selectAll('*').remove();
            
            if (!data.nodes || data.nodes.length === 0) {
                svg.append('text')
                    .attr('x', '50%')
                    .attr('y', '50%')
                    .attr('text-anchor', 'middle')
                    .attr('fill', 'white')
                    .attr('font-size', '14px')
                    .text('Graphe non disponible');
                return;
            }
            
            const width = 480;
            const height = 600;
            
            const simulation = d3.forceSimulation(data.nodes)
                .force('link', d3.forceLink(data.links || []).id(d => d.id).distance(100))
                .force('charge', d3.forceManyBody().strength(-300))
                .force('center', d3.forceCenter(width / 2, height / 2));
            
            // Liens
            const link = svg.append('g')
                .selectAll('line')
                .data(data.links || [])
                .enter().append('line')
                .attr('class', d => `link ${d.privacy_level || 'public'}`);
            
            // Nœuds
            const node = svg.append('g')
                .selectAll('circle')
                .data(data.nodes)
                .enter().append('circle')
                .attr('class', d => `node ${d.privacy_level || 'public'}`)
                .attr('r', d => Math.sqrt(d.size || 1000) / 10 + 5)
                .call(d3.drag()
                    .on('start', dragstarted)
                    .on('drag', dragged)
                    .on('end', dragended));
            
            // Labels
            const label = svg.append('g')
                .selectAll('text')
                .data(data.nodes)
                .enter().append('text')
                .attr('class', 'node-label')
                .text(d => d.name || d.id.substring(0, 8));
            
            simulation.on('tick', () => {
                link
                    .attr('x1', d => d.source.x)
                    .attr('y1', d => d.source.y)
                    .attr('x2', d => d.target.x)
                    .attr('y2', d => d.target.y);
                
                node
                    .attr('cx', d => d.x)
                    .attr('cy', d => d.y);
                
                label
                    .attr('x', d => d.x)
                    .attr('y', d => d.y + 4);
            });
            
            function dragstarted(event, d) {
                if (!event.active) simulation.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
            }
            
            function dragged(event, d) {
                d.fx = event.x;
                d.fy = event.y;
            }
            
            function dragended(event, d) {
                if (!event.active) simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
            }
            
            // Zoom
            const zoom = d3.zoom()
                .scaleExtent([0.1, 4])
                .on('zoom', (event) => {
                    graphTransform = event.transform;
                    svg.selectAll('g').attr('transform', event.transform);
                });
            
            svg.call(zoom);
            currentGraph = { svg, zoom, simulation };
        }
        
        function toggleMetadata() {
            showMetadata = !showMetadata;
            if (currentDocument) {
                selectDocument(currentDocument);
            }
        }
        
        function refreshDocument() {
            if (currentDocument) {
                selectDocument(currentDocument);
            }
        }
        
        function zoomGraph(factor) {
            if (currentGraph) {
                const newTransform = graphTransform.scale(factor);
                currentGraph.svg.transition().duration(300)
                    .call(currentGraph.zoom.transform, newTransform);
            }
        }
        
        function resetZoom() {
            if (currentGraph) {
                currentGraph.svg.transition().duration(500)
                    .call(currentGraph.zoom.transform, d3.zoomIdentity);
            }
        }
        
        // Initialisation
        loadContentTree();
        
        // Actualisation automatique
        setInterval(loadContentTree, 30000);
    </script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def _serve_content_tree(self):
        """API pour arbre de contenu"""
        try:
            if not self.vfs_data:
                vfs_files = list(Path('.').glob('panini_vfs_architecture_*.json'))
                if vfs_files:
                    with open(vfs_files[0], 'r', encoding='utf-8') as f:
                        self.vfs_data = json.load(f)
            
            node_registry = self.vfs_data.get('virtual_filesystem', {}).get('structure', {}).get('node_registry', {})
            
            nodes = []
            for node_id, node_data in node_registry.items():
                # Déterminer le niveau de confidentialité
                metadata = node_data.get('metadata', {})
                hints = metadata.get('semantic_hints', [])
                
                privacy_level = 'public'
                if any('personal' in str(hint).lower() or 'private' in str(hint).lower() for hint in hints):
                    privacy_level = 'private'
                elif any('team' in str(hint).lower() or 'project' in str(hint).lower() for hint in hints):
                    privacy_level = 'confidential'
                
                nodes.append({
                    'node_id': node_id,
                    'filename': f"document_{node_id[:8]}.{node_data.get('content_type', '').lstrip('.')}",
                    'content_type': node_data.get('content_type'),
                    'size_original': node_data.get('size_original'),
                    'privacy_level': privacy_level,
                    'metadata': metadata
                })
            
            response = {'nodes': nodes}
            
        except Exception as e:
            response = {'error': f'Erreur: {e}', 'nodes': []}
        
        self._send_json(response)
    
    def _serve_document_content(self, document_id):
        """API pour contenu de document"""
        try:
            if not self.vfs_data:
                vfs_files = list(Path('.').glob('panini_vfs_architecture_*.json'))
                if vfs_files:
                    with open(vfs_files[0], 'r', encoding='utf-8') as f:
                        self.vfs_data = json.load(f)
            
            node_registry = self.vfs_data.get('virtual_filesystem', {}).get('structure', {}).get('node_registry', {})
            
            if document_id in node_registry:
                node_data = node_registry[document_id]
                metadata = node_data.get('metadata', {})
                hints = metadata.get('semantic_hints', [])
                
                # Déterminer confidentialité
                privacy_level = 'public'
                if any('personal' in str(hint).lower() or 'private' in str(hint).lower() for hint in hints):
                    privacy_level = 'private'
                elif any('team' in str(hint).lower() or 'project' in str(hint).lower() for hint in hints):
                    privacy_level = 'confidential'
                
                # Calculer ratio compression
                compression_ratio = None
                if node_data.get('size_original') and node_data.get('size_compressed'):
                    compression_ratio = round(((node_data['size_original'] - node_data['size_compressed']) / node_data['size_original']) * 100, 1)
                
                response = {
                    'node_id': document_id,
                    'filename': f"document_{document_id[:8]}.{node_data.get('content_type', '').lstrip('.')}",
                    'content_type': node_data.get('content_type'),
                    'size_original': node_data.get('size_original'),
                    'content_hash': node_data.get('content_hash'),
                    'privacy_level': privacy_level,
                    'compression_ratio': compression_ratio,
                    'metadata': metadata,
                    'content': f"Contenu simulé pour {document_id}\\n\\nCe document fait partie du VFS PaniniFS avec déduplication.\\nNiveau de confidentialité: {privacy_level}\\n\\nMétadonnées techniques:\\n- Hash: {node_data.get('content_hash', 'N/A')[:32]}...\\n- Taille: {node_data.get('size_original', 'N/A')} bytes\\n- Type: {node_data.get('content_type', 'N/A')}\\n\\nIndices sémantiques: {', '.join(hints) if hints else 'Aucun'}"
                }
            else:
                response = {'error': 'Document non trouvé'}
                
        except Exception as e:
            response = {'error': f'Erreur: {e}'}
        
        self._send_json(response)
    
    def _serve_node_graph(self, node_id):
        """API pour graphe de nœud"""
        try:
            # Simuler un graphe de décomposition du document
            nodes = [
                {
                    'id': node_id,
                    'name': f'Doc_{node_id[:8]}',
                    'privacy_level': 'private',
                    'size': 2000,
                    'type': 'document'
                },
                {
                    'id': f'{node_id}_header',
                    'name': 'Header',
                    'privacy_level': 'public',
                    'size': 500,
                    'type': 'metadata'
                },
                {
                    'id': f'{node_id}_content',
                    'name': 'Content',
                    'privacy_level': 'private',
                    'size': 1200,
                    'type': 'content'
                },
                {
                    'id': f'{node_id}_refs',
                    'name': 'References',
                    'privacy_level': 'confidential',
                    'size': 300,
                    'type': 'references'
                }
            ]
            
            links = [
                {'source': node_id, 'target': f'{node_id}_header', 'privacy_level': 'public'},
                {'source': node_id, 'target': f'{node_id}_content', 'privacy_level': 'private'},
                {'source': node_id, 'target': f'{node_id}_refs', 'privacy_level': 'confidential'},
                {'source': f'{node_id}_content', 'target': f'{node_id}_refs', 'privacy_level': 'confidential'}
            ]
            
            response = {
                'nodes': nodes,
                'links': links,
                'center_node': node_id
            }
            
        except Exception as e:
            response = {'error': f'Erreur: {e}', 'nodes': [], 'links': []}
        
        self._send_json(response)
    
    def _serve_static_file(self, path):
        """Servir fichiers statiques (si nécessaire)"""
        self.send_response(404)
        self.end_headers()
    
    def _serve_404(self):
        """Page 404"""
        self.send_response(404)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(b"<h1>404 - Page non trouvee</h1>")
    
    def _send_json(self, data):
        """Envoyer réponse JSON"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

def start_uhd_server():
    """Démarrer serveur UHD/4K"""
    
    # Charger données VFS
    vfs_data = {}
    try:
        vfs_files = list(Path('.').glob('panini_vfs_architecture_*.json'))
        if vfs_files:
            with open(vfs_files[0], 'r', encoding='utf-8') as f:
                vfs_data = json.load(f)
    except Exception as e:
        print(f"⚠️ VFS non chargé: {e}")
    
    # Créer handler
    def handler(*args, **kwargs):
        return PaniniUHDInterfaceHandler(*args, vfs_data=vfs_data, **kwargs)
    
    # Démarrer serveur
    server = HTTPServer(('localhost', 7000), handler)
    
    print("🖥️ INTERFACE UHD/4K PANINI-FS")
    print("="*50)
    print("🎯 Interface côte à côte optimisée UHD/4K")
    print("🌐 URL: http://localhost:7000/uhd")
    print("📐 Layout: Arbre | Document | Graphe")
    print("🎨 Couleurs: Rouge (Privé) | Jaune (Confidentiel) | Vert (Public)")
    print("="*50)
    print("📝 Appuyez sur Ctrl+C pour arrêter")
    
    try:
        threading.Timer(1.0, lambda: webbrowser.open('http://localhost:7000/uhd')).start()
        server.serve_forever()
    except KeyboardInterrupt:
        print("\\n👋 Serveur UHD arrêté")
        server.shutdown()

if __name__ == "__main__":
    start_uhd_server()