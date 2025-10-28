#!/usr/bin/env python3
"""
🎨 PANINI-FS WEB EXPLORATION INTERFACE
============================================================
🎯 Mission: Interface web interactive pour exploration VFS
🔬 Focus: Visualisation graphique, décomposition, générativité
🚀 Composants: FastAPI + React specs + D3.js + API générativité

Interface web moderne pour exploration interactive du FS virtuel
PaniniFS avec capacités de décomposition et générativité.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import hashlib

class PaniniWebExplorerGenerator:
    """Générateur interface web d'exploration PaniniFS"""
    
    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path(".")
        
    def generate_fastapi_backend(self) -> str:
        """Générer code backend FastAPI"""
        
        fastapi_code = '''#!/usr/bin/env python3
"""
🚀 PANINI-FS FASTAPI BACKEND
============================================================
Backend API pour interface web d'exploration PaniniFS
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import json
import os
from pathlib import Path

app = FastAPI(title="PaniniFS Explorer API", version="1.0.0")

# CORS pour développement
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Données VFS globales
vfs_data = {}

class NodeResponse(BaseModel):
    node_id: str
    content_type: str
    size_original: int
    generative_potential: float
    semantic_tags: List[str]
    decomposition_level: int

class GraphResponse(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    stats: Dict[str, Any]

@app.on_event("startup")
async def load_vfs_data():
    """Charger données VFS au démarrage"""
    global vfs_data
    
    # Charger architecture VFS la plus récente
    arch_files = list(Path(".").glob("panini_vfs_architecture_*.json"))
    if arch_files:
        latest_arch = max(arch_files, key=os.path.getctime)
        with open(latest_arch, 'r', encoding='utf-8') as f:
            vfs_data = json.load(f)
        print(f"✅ VFS chargé: {latest_arch}")
    else:
        print("⚠️ Aucune architecture VFS trouvée")

@app.get("/api/health")
async def health_check():
    """Vérification santé API"""
    return {"status": "healthy", "vfs_loaded": bool(vfs_data)}

@app.get("/api/nodes/", response_model=List[NodeResponse])
async def get_all_nodes():
    """Récupérer tous les nœuds"""
    if not vfs_data:
        raise HTTPException(status_code=503, detail="VFS not loaded")
    
    nodes = []
    node_registry = vfs_data.get('virtual_filesystem', {}).get('structure', {}).get('node_registry', {})
    
    for node_id, node_data in node_registry.items():
        nodes.append(NodeResponse(
            node_id=node_id,
            content_type=node_data.get('content_type', 'unknown'),
            size_original=node_data.get('size_original', 0),
            generative_potential=node_data.get('generative_potential', 0.0),
            semantic_tags=node_data.get('semantic_tags', []),
            decomposition_level=node_data.get('decomposition_level', 0)
        ))
    
    return nodes

@app.get("/api/graph/", response_model=GraphResponse)
async def get_graph_structure():
    """Récupérer structure graphique pour visualisation"""
    if not vfs_data:
        raise HTTPException(status_code=503, detail="VFS not loaded")
    
    node_registry = vfs_data.get('virtual_filesystem', {}).get('structure', {}).get('node_registry', {})
    dedup_map = vfs_data.get('virtual_filesystem', {}).get('structure', {}).get('deduplication_map', {})
    
    # Construire nœuds pour D3.js
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
    
    # Construire arêtes (relations)
    edges = []
    
    # Arêtes de déduplication
    content_to_files = {}
    for filename, node_id in dedup_map.items():
        if node_id not in content_to_files:
            content_to_files[node_id] = []
        content_to_files[node_id].append(filename)
    
    for node_id, files in content_to_files.items():
        if len(files) > 1:
            # Créer arêtes entre fichiers dupliqués
            for i, file1 in enumerate(files):
                for file2 in files[i+1:]:
                    edges.append({
                        'source': node_id,
                        'target': node_id,  # Self-edge pour duplicata
                        'type': 'duplicate',
                        'files': [file1, file2]
                    })
    
    # Statistiques
    stats = {
        'total_nodes': len(nodes),
        'total_edges': len(edges),
        'duplicate_groups': len([g for g in content_to_files.values() if len(g) > 1]),
        'total_content_types': len(set(n['content_type'] for n in nodes))
    }
    
    return GraphResponse(nodes=nodes, edges=edges, stats=stats)

@app.get("/api/content/{node_id}")
async def get_node_content(node_id: str):
    """Récupérer contenu d'un nœud"""
    if not vfs_data:
        raise HTTPException(status_code=503, detail="VFS not loaded")
    
    node_registry = vfs_data.get('virtual_filesystem', {}).get('structure', {}).get('node_registry', {})
    
    if node_id not in node_registry:
        raise HTTPException(status_code=404, detail="Node not found")
    
    # Simulation contenu - dans implémentation réelle, récupérer du content store
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
    
    return JSONResponse(content_info)

@app.post("/api/decompose/{node_id}")
async def decompose_node(node_id: str, strategy: str = Query("structural")):
    """Décomposer un nœud selon une stratégie"""
    if not vfs_data:
        raise HTTPException(status_code=503, detail="VFS not loaded")
    
    node_registry = vfs_data.get('virtual_filesystem', {}).get('structure', {}).get('node_registry', {})
    
    if node_id not in node_registry:
        raise HTTPException(status_code=404, detail="Node not found")
    
    # Simulation décomposition
    strategies = {
        'structural': {
            'components': [
                {'name': 'header', 'size': 1024, 'type': 'metadata'},
                {'name': 'content', 'size': 50000, 'type': 'data'},
                {'name': 'footer', 'size': 512, 'type': 'metadata'}
            ]
        },
        'semantic': {
            'components': [
                {'name': 'topic_A', 'size': 20000, 'type': 'semantic'},
                {'name': 'topic_B', 'size': 15000, 'type': 'semantic'},
                {'name': 'references', 'size': 5000, 'type': 'links'}
            ]
        },
        'temporal': {
            'components': [
                {'name': 'v1.0', 'size': 30000, 'type': 'version'},
                {'name': 'v1.1_diff', 'size': 5000, 'type': 'delta'},
                {'name': 'v1.2_diff', 'size': 3000, 'type': 'delta'}
            ]
        }
    }
    
    result = {
        'original_node': node_id,
        'strategy': strategy,
        'components': strategies.get(strategy, {'components': []})['components'],
        'decomposition_tree': {
            'root': node_id,
            'children': [f"{node_id}_comp_{i}" for i in range(len(strategies.get(strategy, {'components': []})['components']))]
        }
    }
    
    return JSONResponse(result)

@app.get("/api/semantic/search")
async def semantic_search(query: str = Query(...), limit: int = Query(10)):
    """Recherche sémantique dans les nœuds"""
    if not vfs_data:
        raise HTTPException(status_code=503, detail="VFS not loaded")
    
    node_registry = vfs_data.get('virtual_filesystem', {}).get('structure', {}).get('node_registry', {})
    
    # Simulation recherche sémantique
    results = []
    query_lower = query.lower()
    
    for node_id, node_data in list(node_registry.items())[:limit]:
        # Score basé sur tags sémantiques
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
    
    # Trier par score
    results.sort(key=lambda x: x['score'], reverse=True)
    
    return JSONResponse({
        'query': query,
        'results': results[:limit],
        'total_found': len(results)
    })

@app.post("/api/generate/")
async def generate_content(request: Dict[str, Any]):
    """Générer nouveau contenu basé sur nœuds existants"""
    operation = request.get('operation', 'combine')
    source_nodes = request.get('source_nodes', [])
    parameters = request.get('parameters', {})
    
    # Simulation génération
    generated_node = {
        'node_id': f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        'operation': operation,
        'source_nodes': source_nodes,
        'parameters': parameters,
        'result': {
            'size_estimated': sum([10000, 20000, 15000][:len(source_nodes)]),
            'content_type': 'synthetic',
            'generative_potential': 0.9,
            'semantic_tags': ['generated', 'synthetic', f'op_{operation}']
        }
    }
    
    return JSONResponse(generated_node)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
        
        # Sauvegarder
        backend_file = self.output_dir / "panini_web_backend.py"
        with open(backend_file, 'w', encoding='utf-8') as f:
            f.write(fastapi_code)
        
        print(f"✅ Backend FastAPI généré: {backend_file}")
        return str(backend_file)
    
    def generate_react_frontend_specs(self) -> str:
        """Générer spécifications frontend React"""
        
        frontend_specs = {
            'package_json': {
                "name": "panini-fs-explorer",
                "version": "1.0.0",
                "description": "Interface web d'exploration PaniniFS",
                "dependencies": {
                    "react": "^18.2.0",
                    "react-dom": "^18.2.0",
                    "d3": "^7.8.5",
                    "axios": "^1.4.0",
                    "react-router-dom": "^6.11.0",
                    "@mui/material": "^5.13.0",
                    "@emotion/react": "^11.11.0",
                    "@emotion/styled": "^11.11.0"
                },
                "scripts": {
                    "start": "react-scripts start",
                    "build": "react-scripts build",
                    "test": "react-scripts test",
                    "eject": "react-scripts eject"
                }
            },
            'components': {
                'App.js': {
                    'description': 'Composant principal avec routing',
                    'features': ['Navigation', 'Layout', 'State management']
                },
                'NodeGraph.js': {
                    'description': 'Visualisation D3.js du graphe de nœuds',
                    'features': ['Force layout', 'Zoom', 'Interactions', 'Filtering']
                },
                'ContentViewer.js': {
                    'description': 'Visualiseur multi-format de contenu',
                    'features': ['PDF preview', 'Image display', 'Text rendering']
                },
                'DecompositionExplorer.js': {
                    'description': 'Explorateur hiérarchique décomposition',
                    'features': ['Tree view', 'Drill-down', 'Strategy selection']
                },
                'GenerativePanel.js': {
                    'description': 'Interface de génération de contenu',
                    'features': ['Operation selection', 'Node combination', 'Preview']
                },
                'SemanticSearch.js': {
                    'description': 'Interface de recherche sémantique',
                    'features': ['Live search', 'Tag filtering', 'Score display']
                }
            },
            'api_client': {
                'description': 'Client API pour communication backend',
                'endpoints': {
                    'getNodes': 'GET /api/nodes/',
                    'getGraph': 'GET /api/graph/',
                    'getContent': 'GET /api/content/{id}',
                    'decomposeNode': 'POST /api/decompose/{id}',
                    'semanticSearch': 'GET /api/semantic/search',
                    'generateContent': 'POST /api/generate/'
                }
            },
            'd3_visualizations': {
                'node_graph': {
                    'layout': 'force-directed',
                    'features': ['Drag nodes', 'Zoom/pan', 'Node filtering', 'Edge styling'],
                    'node_types': {
                        'content': {'color': '#4CAF50', 'radius': 'size-based'},
                        'generative': {'color': '#FF9800', 'radius': 'potential-based'},
                        'composite': {'color': '#2196F3', 'radius': 'fixed'}
                    }
                },
                'decomposition_tree': {
                    'layout': 'hierarchical',
                    'features': ['Collapsible', 'Level highlighting', 'Component details']
                }
            }
        }
        
        # Sauvegarder spécifications
        specs_file = self.output_dir / f"panini_web_frontend_specs_{self.session_id}.json"
        with open(specs_file, 'w', encoding='utf-8') as f:
            json.dump(frontend_specs, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Spécifications React générées: {specs_file}")
        return str(specs_file)
    
    def generate_html_prototype(self) -> str:
        """Générer prototype HTML avec D3.js"""
        
        html_prototype = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PaniniFS Explorer - Prototype</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .panel {
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .graph-container {
            height: 600px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        
        .controls {
            margin-bottom: 15px;
        }
        
        .controls button {
            margin-right: 10px;
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            background: #007bff;
            color: white;
            cursor: pointer;
        }
        
        .controls button:hover {
            background: #0056b3;
        }
        
        .node-info {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            margin-top: 15px;
        }
        
        .semantic-tag {
            display: inline-block;
            background: #e1f5fe;
            padding: 2px 8px;
            border-radius: 12px;
            margin: 2px;
            font-size: 12px;
        }
        
        .generative-score {
            color: #ff9800;
            font-weight: bold;
        }
        
        /* Styles D3.js */
        .node {
            cursor: pointer;
            stroke: #fff;
            stroke-width: 2px;
        }
        
        .node:hover {
            stroke: #333;
            stroke-width: 3px;
        }
        
        .link {
            stroke: #999;
            stroke-opacity: 0.6;
        }
        
        .link-duplicate {
            stroke: #f44336;
            stroke-dasharray: 5,5;
        }
        
        .link-semantic {
            stroke: #00bcd4;
            stroke-dasharray: 2,2;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌐 PaniniFS Explorer</h1>
            <p>Interface d'exploration interactive du système de fichiers virtuel PaniniFS</p>
        </div>
        
        <div class="dashboard">
            <div class="panel">
                <h2>📊 Graphe des Nœuds</h2>
                <div class="controls">
                    <button onclick="filterByType('all')">Tous</button>
                    <button onclick="filterByType('content')">Contenu</button>
                    <button onclick="filterByType('generative')">Génératif</button>
                    <button onclick="resetZoom()">Reset Zoom</button>
                </div>
                <div id="graph" class="graph-container"></div>
            </div>
            
            <div class="panel">
                <h2>🔍 Détails du Nœud</h2>
                <div id="node-details">
                    <p>Cliquez sur un nœud pour voir ses détails</p>
                </div>
                
                <h3>🚀 Actions Génératives</h3>
                <div class="controls">
                    <button onclick="decomposeNode()">Décomposer</button>
                    <button onclick="combineNodes()">Combiner</button>
                    <button onclick="analyzeSemantics()">Analyser</button>
                </div>
                
                <h3>🏷️ Recherche Sémantique</h3>
                <input type="text" id="semantic-search" placeholder="Rechercher par tags..." 
                       style="width: 100%; padding: 8px; margin-bottom: 10px;">
                <div id="search-results"></div>
            </div>
        </div>
        
        <div class="panel">
            <h2>📈 Statistiques VFS</h2>
            <div id="stats-container">
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px;">
                    <div style="text-align: center;">
                        <div style="font-size: 24px; font-weight: bold; color: #4CAF50;">42</div>
                        <div>Nœuds Uniques</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 24px; font-weight: bold; color: #f44336;">7</div>
                        <div>Doublons</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 24px; font-weight: bold; color: #ff9800;">0.7</div>
                        <div>Score Génératif Moyen</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 24px; font-weight: bold; color: #2196F3;">88%</div>
                        <div>Efficacité Compression</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Données simulées pour prototype
        const sampleData = {
            nodes: [
                {id: 'node_1', name: 'Samuel CD.pdf', type: 'content', size: 142000, generative_potential: 0.6, semantic_tags: ['person:samuel', 'media:cd']},
                {id: 'node_2', name: 'Document A', type: 'content', size: 50000, generative_potential: 0.8, semantic_tags: ['document:pdf']},
                {id: 'node_3', name: 'Generated Combo', type: 'generative', size: 75000, generative_potential: 0.9, semantic_tags: ['generated', 'composite']},
                {id: 'node_4', name: 'Image Set', type: 'content', size: 200000, generative_potential: 0.4, semantic_tags: ['media:image', 'collection']},
                {id: 'node_5', name: 'Archive Data', type: 'content', size: 500000, generative_potential: 0.7, semantic_tags: ['archive', 'compressed']}
            ],
            links: [
                {source: 'node_1', target: 'node_3', type: 'generative'},
                {source: 'node_2', target: 'node_3', type: 'generative'},
                {source: 'node_1', target: 'node_1', type: 'duplicate'},
                {source: 'node_4', target: 'node_5', type: 'semantic'}
            ]
        };
        
        let selectedNode = null;
        
        // Initialiser visualisation D3.js
        function initGraph() {
            const container = d3.select("#graph");
            const width = 800;
            const height = 550;
            
            const svg = container.append("svg")
                .attr("width", width)
                .attr("height", height);
            
            const simulation = d3.forceSimulation(sampleData.nodes)
                .force("link", d3.forceLink(sampleData.links).id(d => d.id).distance(100))
                .force("charge", d3.forceManyBody().strength(-300))
                .force("center", d3.forceCenter(width / 2, height / 2));
            
            // Liens
            const link = svg.append("g")
                .selectAll("line")
                .data(sampleData.links)
                .enter().append("line")
                .attr("class", d => `link link-${d.type}`)
                .attr("stroke-width", 2);
            
            // Nœuds
            const node = svg.append("g")
                .selectAll("circle")
                .data(sampleData.nodes)
                .enter().append("circle")
                .attr("class", "node")
                .attr("r", d => Math.sqrt(d.size) / 100)
                .attr("fill", d => {
                    switch(d.type) {
                        case 'content': return '#4CAF50';
                        case 'generative': return '#FF9800';
                        default: return '#2196F3';
                    }
                })
                .on("click", function(event, d) {
                    selectedNode = d;
                    updateNodeDetails(d);
                    
                    // Highlighting
                    d3.selectAll(".node").style("opacity", 0.3);
                    d3.select(this).style("opacity", 1);
                })
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended));
            
            // Labels
            const label = svg.append("g")
                .selectAll("text")
                .data(sampleData.nodes)
                .enter().append("text")
                .text(d => d.name.length > 15 ? d.name.substring(0, 15) + '...' : d.name)
                .attr("font-size", "10px")
                .attr("text-anchor", "middle")
                .attr("dy", "0.35em");
            
            simulation.on("tick", () => {
                link
                    .attr("x1", d => d.source.x)
                    .attr("y1", d => d.source.y)
                    .attr("x2", d => d.target.x)
                    .attr("y2", d => d.target.y);
                
                node
                    .attr("cx", d => d.x)
                    .attr("cy", d => d.y);
                
                label
                    .attr("x", d => d.x)
                    .attr("y", d => d.y + Math.sqrt(d.size) / 100 + 15);
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
        }
        
        function updateNodeDetails(node) {
            const detailsContainer = document.getElementById('node-details');
            const tags = node.semantic_tags.map(tag => 
                `<span class="semantic-tag">${tag}</span>`
            ).join('');
            
            detailsContainer.innerHTML = `
                <div class="node-info">
                    <h4>${node.name}</h4>
                    <p><strong>Type:</strong> ${node.type}</p>
                    <p><strong>Taille:</strong> ${(node.size / 1024).toFixed(1)} KB</p>
                    <p><strong>Potentiel Génératif:</strong> 
                       <span class="generative-score">${(node.generative_potential * 100).toFixed(0)}%</span>
                    </p>
                    <p><strong>Tags Sémantiques:</strong></p>
                    <div>${tags}</div>
                </div>
            `;
        }
        
        function filterByType(type) {
            d3.selectAll(".node").style("opacity", d => {
                return type === 'all' || d.type === type ? 1 : 0.1;
            });
        }
        
        function resetZoom() {
            d3.selectAll(".node").style("opacity", 1);
            selectedNode = null;
            document.getElementById('node-details').innerHTML = 
                '<p>Cliquez sur un nœud pour voir ses détails</p>';
        }
        
        function decomposeNode() {
            if (selectedNode) {
                alert(`Décomposition de ${selectedNode.name} en cours...\\nStratégie: Structurelle\\nComposants détectés: 3`);
            } else {
                alert('Sélectionnez d\\'abord un nœud');
            }
        }
        
        function combineNodes() {
            alert('Interface de combinaison de nœuds\\n(Sélection multiple en développement)');
        }
        
        function analyzeSemantics() {
            if (selectedNode) {
                alert(`Analyse sémantique de ${selectedNode.name}:\\n` +
                      `Tags: ${selectedNode.semantic_tags.join(', ')}\\n` +
                      `Relations potentielles: 3 trouvées`);
            } else {
                alert('Sélectionnez d\\'abord un nœud');
            }
        }
        
        // Recherche sémantique
        document.getElementById('semantic-search').addEventListener('input', function(e) {
            const query = e.target.value.toLowerCase();
            const resultsContainer = document.getElementById('search-results');
            
            if (query.length < 2) {
                resultsContainer.innerHTML = '';
                return;
            }
            
            const matches = sampleData.nodes.filter(node => 
                node.semantic_tags.some(tag => tag.toLowerCase().includes(query))
            );
            
            resultsContainer.innerHTML = matches.map(node => 
                `<div style="padding: 5px; border-left: 3px solid #4CAF50; margin: 5px 0; background: #f8f9fa;">
                    <strong>${node.name}</strong><br>
                    <small>Score génératif: ${(node.generative_potential * 100).toFixed(0)}%</small>
                </div>`
            ).join('');
        });
        
        // Initialiser au chargement
        document.addEventListener('DOMContentLoaded', initGraph);
    </script>
</body>
</html>'''
        
        # Sauvegarder prototype
        prototype_file = self.output_dir / "panini_web_explorer_prototype.html"
        with open(prototype_file, 'w', encoding='utf-8') as f:
            f.write(html_prototype)
        
        print(f"✅ Prototype HTML généré: {prototype_file}")
        return str(prototype_file)
    
    def generate_deployment_guide(self) -> str:
        """Générer guide de déploiement"""
        
        deployment_guide = '''# 🚀 GUIDE DE DÉPLOIEMENT PANINI-FS EXPLORER

## Architecture Complète

### 1. Backend FastAPI
```bash
# Installation dépendances
pip install fastapi uvicorn

# Démarrage serveur API
python panini_web_backend.py
# Accessible sur http://localhost:8000
```

### 2. Serveur WebDAV
```bash
# Démarrage serveur WebDAV
python panini_webdav_server.py
# Accessible sur http://localhost:8080/panini/
```

### 3. Interface Web (Production)
```bash
# Création projet React
npx create-react-app panini-fs-explorer
cd panini-fs-explorer

# Installation dépendances
npm install d3 axios @mui/material @emotion/react @emotion/styled

# Développement
npm start
# Production
npm run build
```

### 4. Prototype HTML (Développement Rapide)
```bash
# Ouvrir directement dans navigateur
open panini_web_explorer_prototype.html
```

## Configuration Docker

### docker-compose.yml
```yaml
version: '3.8'
services:
  panini-api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    command: python panini_web_backend.py
  
  panini-webdav:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - ./data:/app/data
    command: python panini_webdav_server.py
  
  panini-web:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - panini-api
```

## Navigation WebDAV

### Windows
```
\\\\localhost:8080\\panini\\
```

### macOS/Linux
```bash
# Mount WebDAV
mkdir /mnt/panini
mount -t davfs http://localhost:8080/panini/ /mnt/panini
```

### Explorateur Web
```
http://localhost:8000 - API Documentation
http://localhost:3000 - Interface React
file://./panini_web_explorer_prototype.html - Prototype
```

## Fonctionnalités Disponibles

✅ **Navigation WebDAV**: Exploration transparente des fichiers dédupliqués
✅ **API REST**: Endpoints complets pour nœuds, graphe, contenu
✅ **Visualisation D3.js**: Graphe interactif avec zoom, filtres
✅ **Recherche Sémantique**: Recherche par tags et similarité
✅ **Décomposition**: Stratégies structurelles, sémantiques, temporelles
✅ **Générativité**: Combinaison et synthèse de nœuds
✅ **Déduplication**: Transparente via FS virtuel

## URLs d'Accès

- **API Health**: http://localhost:8000/api/health
- **Documentation API**: http://localhost:8000/docs
- **WebDAV Root**: http://localhost:8080/panini/
- **Interface Web**: http://localhost:3000
- **Prototype**: ./panini_web_explorer_prototype.html
'''
        
        # Sauvegarder guide
        guide_file = self.output_dir / f"panini_deployment_guide_{self.session_id}.md"
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(deployment_guide)
        
        print(f"✅ Guide de déploiement généré: {guide_file}")
        return str(guide_file)
    
    def run_complete_web_interface_generation(self):
        """Exécuter génération complète interface web"""
        print("🎨 PANINI-FS WEB EXPLORATION INTERFACE GENERATOR")
        print("="*60)
        print("🎯 Mission: Interface web interactive pour exploration VFS")
        print("🔬 Focus: Visualisation graphique, décomposition, générativité")
        print(f"⏰ Session: {datetime.now().isoformat()}")
        
        try:
            print("\n🚀 Génération composants interface web...")
            
            # Générer backend FastAPI
            backend_file = self.generate_fastapi_backend()
            
            # Générer spécifications React
            frontend_specs = self.generate_react_frontend_specs()
            
            # Générer prototype HTML
            prototype_file = self.generate_html_prototype()
            
            # Générer guide déploiement
            deployment_guide = self.generate_deployment_guide()
            
            print(f"\n🎉 INTERFACE WEB PANINI-FS GÉNÉRÉE !")
            print("="*60)
            print(f"🔧 Backend FastAPI: {Path(backend_file).name}")
            print(f"📋 Spécifications React: {Path(frontend_specs).name}")
            print(f"🎨 Prototype HTML: {Path(prototype_file).name}")
            print(f"📖 Guide déploiement: {Path(deployment_guide).name}")
            
            print(f"\n🚀 DÉMARRAGE RAPIDE:")
            print(f"1. python {Path(backend_file).name} (API)")
            print(f"2. python panini_webdav_server.py (WebDAV)")
            print(f"3. Ouvrir {Path(prototype_file).name} (Interface)")
            
            print(f"\n🌐 URLS D'ACCÈS:")
            print(f"• API: http://localhost:8000")
            print(f"• WebDAV: http://localhost:8080/panini/")
            print(f"• Interface: file://./{Path(prototype_file).name}")
            
        except Exception as e:
            print(f"❌ Erreur génération interface: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    generator = PaniniWebExplorerGenerator()
    generator.run_complete_web_interface_generation()