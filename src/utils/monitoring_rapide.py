#!/usr/bin/env python3
"""
📊 MONITORING RAPIDE SYSTÈME AUTONOME
====================================
Surveillance en une commande de l'écosystème
"""

import requests
import json
import time
from datetime import datetime


def quick_status():
    """Status rapide du système autonome"""
    print(f"🎯 MONITORING SYSTÈME AUTONOME - {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    try:
        # API dashboard autonome
        response = requests.get('http://localhost:8890/api/metrics', timeout=5)
        if response.status_code == 200:
            data = response.json()
            
            # Processus
            processes = data.get('processes', {})
            running = sum(1 for p in processes.values() if p.get('running', False))
            total = len(processes)
            
            print(f"🚀 SYSTÈMES AUTONOMES: {running}/{total} actifs")
            
            for script, info in processes.items():
                name = info.get('name', script)
                icon = info.get('icon', '📄')
                status = "🟢" if info.get('running') else "🔴"
                
                if info.get('running'):
                    cpu = info.get('cpu_percent', 0)
                    mem = info.get('memory_percent', 0)
                    uptime = int(info.get('uptime', 0))
                    print(f"   {icon} {name}: {status} CPU:{cpu:.1f}% RAM:{mem:.1f}% Up:{uptime}s")
                else:
                    print(f"   {icon} {name}: {status} ARRÊTÉ")
            
            # Métriques recherche
            research = data.get('research_metrics', {})
            print(f"\n📈 MÉTRIQUES RECHERCHE:")
            print(f"   🔄 Cycles: {research.get('cycles_completed', 0)}")
            print(f"   🧠 Hypothèses: {research.get('hypotheses_generated', 0)}")
            print(f"   📚 Corpus: {research.get('corpus_size', 0)} éléments")
            print(f"   ❌ Erreurs: {research.get('errors_count', 0)}")
            
            # Santé système
            health = data.get('system_health', {})
            status_emoji = {
                'healthy': '🟢',
                'warning': '🟡', 
                'critical': '🔴'
            }.get(health.get('status'), '❓')
            
            print(f"\n🏥 SANTÉ SYSTÈME: {status_emoji} {health.get('status', 'Unknown').upper()}")
            print(f"   💻 CPU: {health.get('cpu_percent', 0):.1f}%")
            print(f"   🧠 RAM: {health.get('memory_percent', 0):.1f}%")
            print(f"   💾 Disque: {health.get('disk_percent', 0):.1f}%")
            
            # Répertoires
            dirs = data.get('directories', {})
            if dirs:
                print(f"\n📁 RÉPERTOIRES AUTONOMES: {len(dirs)}")
                for name, info in list(dirs.items())[:3]:
                    files = info.get('files_count', 0)
                    size = info.get('total_size', 0) / (1024*1024)
                    print(f"   📂 {name}: {files} fichiers, {size:.1f}MB")
            
        else:
            print(f"❌ Dashboard autonome inaccessible (port 8890)")
            
    except Exception as e:
        print(f"❌ Erreur monitoring: {e}")
    
    print("\n🌐 DASHBOARDS DISPONIBLES:")
    print("   🎯 Autonome: http://localhost:8890")
    print("   📊 Master:   http://localhost:8888")
    print("\n💡 Commandes utiles:")
    print("   watch -n 5 python3 monitoring_rapide.py")
    print("   tail -f coordinateur.log")
    print("   python3 test_surveillance_autonome.py")


if __name__ == "__main__":
    quick_status()