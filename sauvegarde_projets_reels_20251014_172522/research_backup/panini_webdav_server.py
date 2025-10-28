#!/usr/bin/env python3
"""
🌐 PANINI-FS WEBDAV SERVER PROTOTYPE
============================================================
🎯 Mission: Serveur WebDAV pour FS virtuel PaniniFS
🔬 Focus: Navigation transparente, déduplication, vues multiples
🚀 Fonctionnalités: VFS mapping, content-on-demand, semantic views

Prototype serveur WebDAV intégré avec FS virtuel PaniniFS
pour exploration transparente du contenu dédupliqué.
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import hashlib
import gzip
import mimetypes
from urllib.parse import unquote, quote
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import xml.etree.ElementTree as ET

class PaniniVFSHandler:
    """Handler pour FS virtuel PaniniFS"""
    
    def __init__(self, vfs_data: Dict[str, Any]):
        self.vfs = vfs_data
        self.node_registry = vfs_data.get('virtual_filesystem', {}).get('structure', {}).get('node_registry', {})
        self.dedup_map = vfs_data.get('virtual_filesystem', {}).get('structure', {}).get('deduplication_map', {})
        
    def get_virtual_path_info(self, path: str) -> Optional[Dict[str, Any]]:
        """Obtenir infos chemin virtuel"""
        # Nettoyer le chemin
        clean_path = path.strip('/').replace('//', '/')
        
        if not clean_path or clean_path == 'panini':
            # Racine - lister tous les fichiers dédupliqués
            return {
                'type': 'directory',
                'name': 'panini',
                'children': list(self.dedup_map.keys()),
                'size': 0,
                'modified': datetime.now().isoformat()
            }
        
        # Chercher dans mapping déduplication
        if clean_path in self.dedup_map:
            node_id = self.dedup_map[clean_path]
            if node_id in self.node_registry:
                node = self.node_registry[node_id]
                return {
                    'type': 'file',
                    'name': clean_path,
                    'node_id': node_id,
                    'size': node.get('size_original', 0),
                    'content_type': mimetypes.guess_type(clean_path)[0] or 'application/octet-stream',
                    'modified': node.get('creation_timestamp', datetime.now().isoformat()),
                    'generative_potential': node.get('generative_potential', 0.0),
                    'semantic_tags': node.get('semantic_tags', [])
                }
        
        return None
    
    def get_content(self, node_id: str) -> Optional[bytes]:
        """Récupérer contenu d'un nœud"""
        # Ici on simule - dans l'implémentation réelle,
        # on récupèrerait le contenu du content store
        return b"Content simulé pour node " + node_id.encode()

class WebDAVRequestHandler(BaseHTTPRequestHandler):
    """Handler HTTP pour requêtes WebDAV"""
    
    def __init__(self, *args, vfs_handler=None, **kwargs):
        self.vfs_handler = vfs_handler
        super().__init__(*args, **kwargs)
    
    def do_PROPFIND(self):
        """Handler PROPFIND WebDAV"""
        path = unquote(self.path)
        
        # Obtenir infos du chemin virtuel
        path_info = self.vfs_handler.get_virtual_path_info(path)
        
        if not path_info:
            self.send_error(404, "Not Found")
            return
        
        # Générer réponse XML WebDAV
        response_xml = self._generate_propfind_response(path, path_info)
        
        self.send_response(207, "Multi-Status")
        self.send_header('Content-Type', 'application/xml; charset=utf-8')
        self.send_header('Content-Length', str(len(response_xml)))
        self.end_headers()
        self.wfile.write(response_xml.encode('utf-8'))
    
    def do_GET(self):
        """Handler GET pour récupérer contenu"""
        path = unquote(self.path)
        
        path_info = self.vfs_handler.get_virtual_path_info(path)
        
        if not path_info:
            self.send_error(404, "Not Found")
            return
        
        if path_info['type'] == 'directory':
            # Retourner listing HTML simple
            html = self._generate_directory_listing(path, path_info)
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(html)))
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        
        elif path_info['type'] == 'file':
            # Récupérer et retourner contenu fichier
            content = self.vfs_handler.get_content(path_info['node_id'])
            if content:
                self.send_response(200)
                self.send_header('Content-Type', path_info['content_type'])
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(404, "Content Not Found")
    
    def do_OPTIONS(self):
        """Handler OPTIONS pour capacités WebDAV"""
        self.send_response(200)
        self.send_header('Allow', 'OPTIONS, PROPFIND, GET, HEAD')
        self.send_header('DAV', '1, 2')
        self.send_header('Content-Length', '0')
        self.end_headers()
    
    def _generate_propfind_response(self, path: str, path_info: Dict[str, Any]) -> str:
        """Générer réponse XML PROPFIND"""
        root = ET.Element('D:multistatus', {'xmlns:D': 'DAV:'})
        
        if path_info['type'] == 'directory':
            # Réponse pour répertoire
            response = ET.SubElement(root, 'D:response')
            ET.SubElement(response, 'D:href').text = quote(path, safe='/')
            
            propstat = ET.SubElement(response, 'D:propstat')
            prop = ET.SubElement(propstat, 'D:prop')
            
            ET.SubElement(prop, 'D:resourcetype').append(ET.Element('D:collection'))
            ET.SubElement(prop, 'D:getlastmodified').text = path_info['modified']
            
            ET.SubElement(propstat, 'D:status').text = 'HTTP/1.1 200 OK'
            
            # Ajouter entrées pour enfants
            for child in path_info.get('children', []):
                child_response = ET.SubElement(root, 'D:response')
                child_path = f"{path.rstrip('/')}/{child}"
                ET.SubElement(child_response, 'D:href').text = quote(child_path, safe='/')
                
                child_propstat = ET.SubElement(child_response, 'D:propstat')
                child_prop = ET.SubElement(child_propstat, 'D:prop')
                
                ET.SubElement(child_prop, 'D:resourcetype')  # Fichier = vide
                ET.SubElement(child_prop, 'D:getcontentlength').text = '0'  # Placeholder
                
                ET.SubElement(child_propstat, 'D:status').text = 'HTTP/1.1 200 OK'
        
        else:
            # Réponse pour fichier
            response = ET.SubElement(root, 'D:response')
            ET.SubElement(response, 'D:href').text = quote(path, safe='/')
            
            propstat = ET.SubElement(response, 'D:propstat')
            prop = ET.SubElement(propstat, 'D:prop')
            
            ET.SubElement(prop, 'D:resourcetype')  # Vide pour fichier
            ET.SubElement(prop, 'D:getcontentlength').text = str(path_info['size'])
            ET.SubElement(prop, 'D:getcontenttype').text = path_info['content_type']
            ET.SubElement(prop, 'D:getlastmodified').text = path_info['modified']
            
            ET.SubElement(propstat, 'D:status').text = 'HTTP/1.1 200 OK'
        
        return ET.tostring(root, encoding='unicode')
    
    def _generate_directory_listing(self, path: str, path_info: Dict[str, Any]) -> str:
        """Générer listing HTML de répertoire"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>PaniniFS Virtual Directory: {path}</title>
    <style>
        body {{ font-family: monospace; margin: 20px; }}
        .file {{ margin: 5px 0; }}
        .semantic-tag {{ background: #e1f5fe; padding: 2px 6px; border-radius: 3px; margin: 0 2px; }}
        .generative-potential {{ color: #ff9800; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>📁 PaniniFS Virtual Directory</h1>
    <p><strong>Path:</strong> {path}</p>
    <hr>
"""
        
        for child in path_info.get('children', []):
            # Obtenir infos détaillées de l'enfant
            child_info = self.vfs_handler.get_virtual_path_info(child)
            if child_info:
                semantic_tags = ' '.join([f'<span class="semantic-tag">{tag}</span>' 
                                        for tag in child_info.get('semantic_tags', [])])
                generative = child_info.get('generative_potential', 0.0)
                
                html += f"""
    <div class="file">
        📄 <a href="{quote(child, safe='')}">{child}</a>
        <span style="color: #666;">({child_info['size']} bytes)</span>
        {semantic_tags}
        <span class="generative-potential">⚡ {generative:.1f}</span>
    </div>"""
        
        html += """
    <hr>
    <p><em>PaniniFS Virtual Filesystem - Déduplication transparente active</em></p>
</body>
</html>"""
        
        return html

class PaniniWebDAVServer:
    """Serveur WebDAV pour PaniniFS"""
    
    def __init__(self, vfs_data: Dict[str, Any], host='localhost', port=8080):
        self.vfs_data = vfs_data
        self.host = host
        self.port = port
        self.vfs_handler = PaniniVFSHandler(vfs_data)
        self.server = None
        
    def create_handler_class(self):
        """Créer classe handler avec VFS intégré"""
        vfs_handler = self.vfs_handler
        
        class BoundHandler(WebDAVRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, vfs_handler=vfs_handler, **kwargs)
        
        return BoundHandler
    
    def start(self):
        """Démarrer serveur WebDAV"""
        handler_class = self.create_handler_class()
        self.server = HTTPServer((self.host, self.port), handler_class)
        
        print(f"🌐 Serveur WebDAV PaniniFS démarré")
        print(f"📍 URL: http://{self.host}:{self.port}/")
        print(f"📁 Point de montage: /panini/")
        print("🔍 Navigation: Compatible avec explorateurs WebDAV")
        
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Arrêt serveur WebDAV")
            self.server.shutdown()

def load_vfs_architecture() -> Optional[Dict[str, Any]]:
    """Charger architecture VFS la plus récente"""
    arch_files = list(Path(".").glob("panini_vfs_architecture_*.json"))
    if not arch_files:
        return None
    
    latest_arch = max(arch_files, key=os.path.getctime)
    print(f"📁 Chargement architecture: {latest_arch}")
    
    with open(latest_arch, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    """Point d'entrée principal"""
    print("🌐 PANINI-FS WEBDAV SERVER")
    print("="*50)
    
    # Charger architecture VFS
    vfs_data = load_vfs_architecture()
    if not vfs_data:
        print("❌ Aucune architecture VFS trouvée")
        print("💡 Exécutez d'abord panini_virtual_fs_architecture.py")
        return
    
    # Créer et démarrer serveur
    server = PaniniWebDAVServer(vfs_data, host='0.0.0.0', port=8080)
    
    print(f"🚀 Démarrage serveur avec {len(vfs_data.get('virtual_filesystem', {}).get('structure', {}).get('node_registry', {}))} nœuds")
    
    server.start()

if __name__ == "__main__":
    main()