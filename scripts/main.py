#!/usr/bin/env python3
"""
Script principal de contrôle du système PaniniFS Research
Point d'entrée unifié pour tous les composants
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire src au PYTHONPATH pour les imports
project_root = os.path.dirname(os.path.dirname(__file__))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from utils.system_utils import SystemController, SystemLauncher


def main():
    """Point d'entrée principal du système"""
    print("🚀 SYSTÈME PANINI-FS RESEARCH")
    print("=" * 40)
    
    controller = SystemController()
    launcher = SystemLauncher()
    
    # Vérifier l'état actuel
    status = controller.get_system_status()
    
    if status['processes']['count'] > 0:
        print("⚠️  Système déjà en cours d'exécution")
        print(f"Processus actifs: {status['processes']['count']}")
        
        response = input("\nRedémarrer le système? (o/n): ")
        if response.lower() in ['o', 'oui', 'y', 'yes']:
            print("🛑 Arrêt des processus existants...")
            controller.stop_all_autonomous_processes()
        else:
            print("✅ Système maintenu en l'état")
            return
    
    # Lancer le système
    print("\n🔧 Lancement du système modulaire...")
    success = launcher.launch_event_system()
    
    if success:
        print("✅ Système lancé avec succès!")
        print("\n📊 Accès:")
        print("- Dashboard: http://localhost:8890")
        print("- Status: python3 scripts/status.py")
        print("- Arrêt: python3 scripts/stop.py")
    else:
        print("❌ Échec du lancement")


if __name__ == "__main__":
    main()