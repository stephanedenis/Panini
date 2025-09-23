#!/usr/bin/env python3
"""
Script d'arrêt - Arrête tous les processus
"""

import sys
from pathlib import Path

# Ajoute le dossier src au path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from utils.system_utils import SystemController


def main():
    """Arrête tous les processus autonomes"""
    
    print("🛑 ARRÊT SYSTÈME PANINI")
    print("=" * 25)
    
    controller = SystemController()
    
    # Vérifie l'état actuel
    status = controller.get_system_status()
    
    if status['status'] == 'INACTIF':
        print("✅ Aucun processus à arrêter")
        return
    
    print(f"📊 {status['processes']['count']} processus trouvés")
    for proc in status['processes']['details']:
        print(f"   🔸 {proc['name']} (PID {proc['pid']})")
    
    # Arrêt des processus
    print("\n🔄 Arrêt en cours...")
    result = controller.stop_all_autonomous_processes()
    
    print(f"✅ {result['message']}")
    
    # Vérification finale
    final_status = controller.get_system_status()
    if final_status['status'] == 'INACTIF':
        print("🎯 Tous les processus arrêtés")
        print("💡 Pour relancer: python3 scripts/main.py")
    else:
        print(f"⚠️ Statut final: {final_status['status']}")
        print("💡 Vérifiez avec: python3 scripts/status.py")


if __name__ == "__main__":
    main()