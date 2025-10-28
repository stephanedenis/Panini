#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audit de Consolidation - PaniniFS
Analyse tous les serveurs existants et leurs endpoints
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class ServerAudit:
    def __init__(self):
        self.workspace = Path('/home/stephane/GitHub/PaniniFS-Research')
        self.servers = []
        self.endpoints = defaultdict(list)
        self.ports = {}
        self.duplications = defaultdict(list)
        
    def audit_all_servers(self):
        """Scanner tous les serveurs PaniniFS"""
        print("🔍 AUDIT DES SERVEURS PANINI-FS")
        print("=" * 60)
        
        # Trouver tous les fichiers serveur
        server_patterns = [
            '**/panini_*server*.py',
            '**/panini_*backend*.py',
            '**/panini_*interface*.py',
            '**/serveur_*.py'
        ]
        
        for pattern in server_patterns:
            for file_path in self.workspace.glob(pattern):
                if file_path.is_file():
                    self._analyze_server(file_path)
        
        # Analyser les résultats
        self._detect_duplications()
        self._generate_report()
        
    def _analyze_server(self, file_path):
        """Analyser un fichier serveur"""
        print(f"\n📄 Analyse: {file_path.name}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            server_info = {
                'name': file_path.name,
                'path': str(file_path),
                'size': file_path.stat().st_size,
                'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                'endpoints': [],
                'port': None,
                'server_type': None,
                'classes': [],
                'functions': []
            }
            
            # Détecter le port
            port_match = re.search(r'[:\(](\d{4,5})[,\)]', content)
            if port_match:
                server_info['port'] = int(port_match.group(1))
                self.ports[server_info['port']] = file_path.name
                print(f"   🔌 Port: {server_info['port']}")
            
            # Détecter le type de serveur
            if 'FastAPI' in content:
                server_info['server_type'] = 'FastAPI'
            elif 'HTTPServer' in content:
                server_info['server_type'] = 'HTTPServer'
            elif 'BaseHTTPRequestHandler' in content:
                server_info['server_type'] = 'BaseHTTPRequestHandler'
            
            if server_info['server_type']:
                print(f"   🛠️ Type: {server_info['server_type']}")
            
            # Extraire les endpoints
            # Pour FastAPI
            fastapi_routes = re.findall(r'@app\.(get|post|put|delete|patch)\(["\']([^"\']+)', content)
            for method, route in fastapi_routes:
                endpoint = {
                    'method': method.upper(),
                    'path': route,
                    'type': 'FastAPI'
                }
                server_info['endpoints'].append(endpoint)
                self.endpoints[route].append(file_path.name)
                print(f"   📍 {method.upper()} {route}")
            
            # Pour HTTP handlers
            http_paths = re.findall(r'if\s+path\s*==\s*["\']([^"\']+)', content)
            for path in set(http_paths):
                endpoint = {
                    'method': 'GET',
                    'path': path,
                    'type': 'HTTPServer'
                }
                server_info['endpoints'].append(endpoint)
                self.endpoints[path].append(file_path.name)
                print(f"   📍 GET {path}")
            
            # Extraire les classes
            classes = re.findall(r'class\s+(\w+)', content)
            server_info['classes'] = list(set(classes))
            if classes:
                print(f"   🏗️ Classes: {', '.join(set(classes[:5]))}")
            
            # Extraire les fonctions principales
            functions = re.findall(r'def\s+(\w+)\(', content)
            server_info['functions'] = list(set(functions))
            
            self.servers.append(server_info)
            
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
    
    def _detect_duplications(self):
        """Détecter les endpoints dupliqués"""
        print("\n\n🔍 DÉTECTION DES DUPLICATIONS")
        print("=" * 60)
        
        for endpoint, servers in self.endpoints.items():
            if len(servers) > 1:
                self.duplications[endpoint] = servers
                print(f"\n⚠️ Endpoint dupliqué: {endpoint}")
                print(f"   Présent dans: {', '.join(servers)}")
    
    def _generate_report(self):
        """Générer le rapport de consolidation"""
        print("\n\n📊 RAPPORT DE CONSOLIDATION")
        print("=" * 60)
        
        # Statistiques globales
        total_servers = len(self.servers)
        total_endpoints = sum(len(s['endpoints']) for s in self.servers)
        unique_endpoints = len(self.endpoints)
        duplicated_endpoints = len(self.duplications)
        
        print(f"\n📈 Statistiques:")
        print(f"   • Serveurs trouvés: {total_servers}")
        print(f"   • Endpoints totaux: {total_endpoints}")
        print(f"   • Endpoints uniques: {unique_endpoints}")
        print(f"   • Endpoints dupliqués: {duplicated_endpoints}")
        print(f"   • Ports utilisés: {len(self.ports)}")
        
        # Détail des ports
        print(f"\n🔌 Ports utilisés:")
        for port, server in sorted(self.ports.items()):
            print(f"   • Port {port}: {server}")
        
        # Matrice de consolidation
        print(f"\n📋 MATRICE DE CONSOLIDATION")
        print("=" * 60)
        
        consolidation_matrix = []
        
        for server in self.servers:
            entry = {
                'server': server['name'],
                'port': server['port'],
                'type': server['server_type'],
                'endpoints_count': len(server['endpoints']),
                'unique_endpoints': [
                    e['path'] for e in server['endpoints']
                    if len(self.endpoints[e['path']]) == 1
                ],
                'shared_endpoints': [
                    e['path'] for e in server['endpoints']
                    if len(self.endpoints[e['path']]) > 1
                ],
                'priority': self._calculate_priority(server)
            }
            consolidation_matrix.append(entry)
        
        # Trier par priorité
        consolidation_matrix.sort(key=lambda x: x['priority'], reverse=True)
        
        print("\n🎯 Priorités de migration:")
        for i, entry in enumerate(consolidation_matrix, 1):
            priority_label = ['🔴 CRITIQUE', '🟠 HAUTE', '🟡 MOYENNE', '🟢 BASSE'][min(entry['priority'] - 1, 3)]
            print(f"\n{i}. {entry['server']} - {priority_label}")
            print(f"   Port: {entry['port']}")
            print(f"   Type: {entry['type']}")
            print(f"   Endpoints: {entry['endpoints_count']}")
            if entry['unique_endpoints']:
                print(f"   Uniques: {len(entry['unique_endpoints'])}")
            if entry['shared_endpoints']:
                print(f"   Partagés: {len(entry['shared_endpoints'])}")
        
        # Recommandations
        print(f"\n\n💡 RECOMMANDATIONS")
        print("=" * 60)
        
        recommendations = []
        
        # Serveur cible
        target_server = max(consolidation_matrix, key=lambda x: x['endpoints_count'])
        recommendations.append(
            f"1. Utiliser '{target_server['server']}' comme base (le plus complet)"
        )
        
        # Consolidation des ports
        if len(self.ports) > 1:
            recommendations.append(
                f"2. Consolider tous les serveurs sur port 5000 unique"
            )
        
        # Endpoints à migrer
        recommendations.append(
            f"3. Migrer {duplicated_endpoints} endpoints dupliqués"
        )
        
        # Serveurs à archiver
        obsolete_servers = [s for s in consolidation_matrix if s['priority'] == 1]
        if obsolete_servers:
            recommendations.append(
                f"4. Archiver {len(obsolete_servers)} serveurs obsolètes"
            )
        
        for rec in recommendations:
            print(f"   {rec}")
        
        # Sauvegarder le rapport
        self._save_report({
            'timestamp': datetime.now().isoformat(),
            'statistics': {
                'total_servers': total_servers,
                'total_endpoints': total_endpoints,
                'unique_endpoints': unique_endpoints,
                'duplicated_endpoints': duplicated_endpoints,
                'ports_used': len(self.ports)
            },
            'servers': self.servers,
            'duplications': dict(self.duplications),
            'consolidation_matrix': consolidation_matrix,
            'recommendations': recommendations
        })
    
    def _calculate_priority(self, server):
        """Calculer la priorité d'un serveur (4=critique, 1=basse)"""
        score = 0
        
        # Plus d'endpoints = plus important
        score += min(len(server['endpoints']), 10)
        
        # Serveur récent = plus important
        if 'advanced' in server['name'].lower() or 'universal' in server['name'].lower():
            score += 5
        
        # Type moderne = plus important
        if server['server_type'] == 'FastAPI':
            score += 3
        
        # Port standard = plus important
        if server['port'] == 5000:
            score += 5
        
        # Convertir en priorité 1-4
        if score >= 15:
            return 4  # Critique
        elif score >= 10:
            return 3  # Haute
        elif score >= 5:
            return 2  # Moyenne
        else:
            return 1  # Basse
    
    def _save_report(self, report):
        """Sauvegarder le rapport JSON"""
        report_file = self.workspace / '.github' / 'reports' / f'server_audit_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"\n✅ Rapport sauvegardé: {report_file}")

def main():
    auditor = ServerAudit()
    auditor.audit_all_servers()
    
    print("\n\n🎯 PROCHAINES ÉTAPES")
    print("=" * 60)
    print("1. Créer panini_universal_server.py basé sur cette analyse")
    print("2. Migrer les endpoints uniques vers le serveur universel")
    print("3. Tester la compatibilité des endpoints")
    print("4. Déprécier les anciens serveurs")
    print("5. Archiver le code obsolète")
    
    return 0

if __name__ == '__main__':
    exit(main())
