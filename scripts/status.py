#!/usr/bin/env python3
"""
Script de statut - Vérifie l'état du système
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire src au PYTHONPATH pour les imports
project_root = os.path.dirname(os.path.dirname(__file__))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from utils.system_utils import SystemController


def main():
    """Affiche le statut du système"""
    
    print("🔍 STATUT SYSTÈME PANINI")
    print("=" * 30)
    
    controller = SystemController()
    status = controller.get_system_status()
    
    # Statut général
    status_icon = {
        'ACTIF': '✅',
        'IDLE': '⚠️',
        'INACTIF': '❌'
    }.get(status['status'], '❓')
    
    print(f"{status_icon} Système: {status['status']}")
    print(f"📊 Processus autonomes: {status['processes']['count']}")
    print(f"⚡ CPU total: {status['processes']['total_cpu']:.1f}%")
    
    # Détails des processus
    if status['processes']['details']:
        print("\n📋 PROCESSUS ACTIFS:")
        for proc in status['processes']['details']:
            affinity_str = f"cores {proc['affinity']}" if proc['affinity'] else "aucune"
            print(f"   🔸 {proc['name']} (PID {proc['pid']})")
            print(f"      CPU: {proc['cpu_percent']:.1f}%, RAM: {proc['memory_mb']:.1f}MB")
            print(f"      Affinité: {affinity_str}")
    
    # Métriques système
    cpu = status['system']['cpu']
    memory = status['system']['memory']
    
    print(f"\n🖥️ SYSTÈME:")
    print(f"   CPU: {cpu['total_cores']} cores, {cpu['average_usage']:.1f}% moyen")
    print(f"   Mémoire: {memory['used_percent']:.1f}% utilisée {memory['status']}")
    
    # Cores actifs
    active_cores = sum(1 for core in cpu['per_core_usage'] if core['usage'] > 10)
    print(f"   Cores actifs: {active_cores}/{cpu['total_cores']}")
    
    # Ports réseau
    ports = status['system']['ports']
    if ports:
        print(f"\n🌐 PORTS:")
        for port, info in ports.items():
            print(f"   Port {port}: {info['status']} (PID {info.get('pid', 'N/A')})")
    
    # Recommandations
    print(f"\n💡 RECOMMANDATIONS:")
    
    if status['status'] == 'INACTIF':
        print("   🚀 Lancer: python3 scripts/main.py")
    elif status['status'] == 'IDLE':
        print("   ⚡ Système actif mais peu chargé")
        print("   📊 Dashboard: http://localhost:8892")
    else:
        print("   ✅ Système optimal")
        print("   📊 Dashboard: http://localhost:8892")
        print("   🔧 Monitoring: Cores dédiés visibles dans htop")


if __name__ == "__main__":
    main()