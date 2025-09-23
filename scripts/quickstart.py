#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Start Guide - PaniniFS Research
Guide de démarrage rapide en Python
"""

import sys
import time
from pathlib import Path


def show_quickstart():
    """Affiche le guide de démarrage rapide"""
    print("🚀 GUIDE DÉMARRAGE RAPIDE - PaniniFS Research")
    print("=" * 50)
    print()
    
    print("📋 COMMANDES DISPONIBLES:")
    print()
    
    print("1️⃣  DÉMARRAGE COMPLET (recommandé):")
    print("    python3 scripts/panini_manager.py all")
    print()
    
    print("2️⃣  DÉMARRAGE API SEULEMENT:")
    print("    python3 scripts/panini_manager.py start")
    print()
    
    print("3️⃣  SYNCHRONISATION COLAB:")
    print("    python3 scripts/panini_manager.py sync")
    print()
    
    print("4️⃣  VOIR STATUT:")
    print("    python3 scripts/panini_manager.py status")
    print()
    
    print("🔗 LIENS DIRECTS:")
    print("   • Dashboard: http://localhost:5000/dashboard")
    print("   • API: http://localhost:5000/health")
    print("   • Notebook Colab: https://colab.research.google.com"
          "/github/stephanedenis/PaniniFS-Research/blob/main"
          "/PaniniFS_Colab_GPU.ipynb")
    print()
    
    print("⚡ WORKFLOW RECOMMANDÉ:")
    print("   1. python3 scripts/panini_manager.py all")
    print("   2. Ouvrir http://localhost:5000/dashboard")
    print("   3. Utiliser le notebook Colab pour GPU")
    print("   4. Synchroniser avec: python3 scripts/panini_manager.py sync")
    print()
    
    print("📁 FICHIERS IMPORTANTS:")
    notebook = Path("PaniniFS_Colab_GPU.ipynb")
    api_script = Path("src/cloud/api_rest.py")
    manager = Path("scripts/panini_manager.py")
    
    print(f"   • Notebook: {'✅' if notebook.exists() else '❌'} "
          f"{notebook}")
    print(f"   • API: {'✅' if api_script.exists() else '❌'} "
          f"{api_script}")
    print(f"   • Manager: {'✅' if manager.exists() else '❌'} "
          f"{manager}")
    print()
    
    print("🛠️  DÉPANNAGE:")
    print("   • Si API ne démarre pas: vérifier les ports")
    print("   • Si erreur modules: pip install -r requirements.txt")
    print("   • Pour aide détaillée: voir README.md")
    print()


def main():
    """Fonction principale"""
    show_quickstart()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        print("🔄 Démarrage automatique...")
        time.sleep(2)
        
        try:
            import subprocess
            subprocess.run([
                sys.executable, "scripts/panini_manager.py", "all"
            ], check=True)
            print("✅ Démarrage réussi !")
        except Exception as e:
            print(f"❌ Erreur: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()