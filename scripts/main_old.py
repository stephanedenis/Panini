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
    
    if status['running_processes']:
        print("⚠️  Système déjà en cours d'exécution")
        print(f"Processus actifs: {len(status['running_processes'])}")
        
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

import os
import sys
import time
import json
from pathlib import Path

# Ajouter le répertoire src au PYTHONPATH pour les imports
project_root = os.path.dirname(os.path.dirname(__file__))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from core.system_base import ProcessManager, SystemMonitor, setup_logging
from utils.system_utils import SystemController, SystemLauncher

import sys
import os
from pathlib import Path

# Ajoute le dossier src au path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from utils.system_utils import SystemController, SystemLauncher


def main():
    """Lance le système complet"""
    
    print("🚀 LANCEMENT SYSTÈME PANINI ÉVÉNEMENTIEL")
    print("=" * 50)
    
    controller = SystemController()
    launcher = SystemLauncher()
    
    # Vérifie l'état actuel
    print("🔍 Vérification état actuel...")
    status = controller.get_system_status()
    
    if status['status'] != 'INACTIF':
        print(f"⚠️ Système déjà actif: {status['status']}")
        print(f"📊 {status['processes']['count']} processus en cours")
        
        response = input("Voulez-vous redémarrer ? (o/N): ")
        if response.lower() == 'o':
            print("🛑 Arrêt des processus existants...")
            result = controller.stop_all_autonomous_processes()
            print(f"✅ {result['message']}")
        else:
            print("👋 Utilisation du système existant")
            print("📡 Dashboard: http://localhost:8892")
            return
    
    # Lance le système événementiel
    print("\n🎯 Lancement système événementiel...")
    if launcher.launch_event_system():
        print("✅ Système événementiel démarré")
    else:
        print("❌ Échec lancement système")
        return
    
    # Lance le dashboard
    print("📊 Lancement dashboard...")
    if launcher.launch_dashboard():
        print("✅ Dashboard démarré")
    else:
        print("❌ Échec lancement dashboard")
    
    print(f"\n🎯 SYSTÈME COMPLET DÉMARRÉ")
    print("📡 Interface web: http://localhost:8892")
    print("🔧 Architecture: Événementielle avec affinité CPU")
    print("⚡ Traitement: Immédiat sur événements")
    
    print(f"\n💡 Commandes utiles:")
    print("   python3 scripts/status.py    # Vérifier statut")
    print("   python3 scripts/stop.py      # Arrêter système")
    print("   python3 scripts/dashboard.py # Ouvrir dashboard")


if __name__ == "__main__":
    main()