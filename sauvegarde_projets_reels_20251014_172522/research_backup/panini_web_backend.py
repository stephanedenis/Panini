#!/usr/bin/env python3
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
