#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire simplifié PaniniFS Research
Script Python unique pour toutes les opérations
"""

import sys
import time
import subprocess
from pathlib import Path


def log(message: str, level: str = "INFO"):
    """Log avec timestamp"""
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")


def check_api():
    """Vérifie si l'API est active"""
    try:
        import requests
        response = requests.get("http://localhost:5000/health", timeout=3)
        return response.status_code == 200
    except Exception:
        return False


def start_api():
    """Démarre l'API"""
    if check_api():
        log("✅ API déjà active")
        return True
    
    api_script = Path("src/cloud/api_rest.py")
    if not api_script.exists():
        log("❌ Script API non trouvé", "ERROR")
        return False
    
    log("🚀 Démarrage API...")
    try:
        subprocess.Popen([sys.executable, str(api_script)])
        
        # Attendre démarrage
        for i in range(10):
            time.sleep(1)
            if check_api():
                log("✅ API prête sur http://localhost:5000")
                return True
            log(f"   Attente... ({i+1}/10)")
        
        log("❌ Timeout API", "ERROR")
        return False
    except Exception as e:
        log(f"❌ Erreur: {e}", "ERROR")
        return False


def sync_colab():
    """Synchronise résultats Colab"""
    log("🔄 Vérification résultats Colab...")
    
    results_dir = Path("colab_integration/results")
    if not results_dir.exists():
        log("ℹ️  Aucun résultat Colab trouvé")
        return True
    
    sessions = [d for d in results_dir.iterdir() if d.is_dir()]
    log(f"📊 {len(sessions)} sessions Colab trouvées")
    
    if sessions:
        log("✅ Résultats Colab disponibles")
        for session in sessions[-3:]:  # 3 plus récentes
            log(f"   📁 {session.name}")
    
    return True


def show_status():
    """Affiche le statut"""
    log("📊 STATUT PANINIFS RESEARCH")
    log("=" * 30)
    
    # API
    api_active = check_api()
    log(f"🔗 API: {'✅ Active' if api_active else '❌ Inactive'}")
    
    if api_active:
        try:
            import requests
            health = requests.get("http://localhost:5000/health").json()
            log(f"   Jobs: {health.get('active_jobs', 0)}")
            log(f"   Status: {health.get('status', 'unknown')}")
        except Exception:
            pass
    
    # Notebooks
    notebook = Path("PaniniFS_Colab_GPU.ipynb")
    log(f"📓 Notebook: {'✅ Prêt' if notebook.exists() else '❌ Manquant'}")
    
    # Résultats
    results_dir = Path("colab_integration/results")
    if results_dir.exists():
        count = len([d for d in results_dir.iterdir() if d.is_dir()])
        log(f"📊 Sessions Colab: {count}")
    else:
        log("📊 Sessions Colab: 0")
    
    # Liens
    log("\n🔗 LIENS:")
    log("   Dashboard: http://localhost:5000/dashboard")
    log("   Notebook: https://colab.research.google.com"
        "/github/stephanedenis/PaniniFS-Research/blob/main"
        "/PaniniFS_Colab_GPU.ipynb")


def main():
    """Fonction principale"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 scripts/panini_manager.py start    # Démarrer API")
        print("  python3 scripts/panini_manager.py sync     # Sync Colab")
        print("  python3 scripts/panini_manager.py status   # Voir statut")
        print("  python3 scripts/panini_manager.py all      # Tout démarrer")
        return
    
    command = sys.argv[1]
    
    if command == "start":
        success = start_api()
        sys.exit(0 if success else 1)
    
    elif command == "sync":
        success = sync_colab()
        sys.exit(0 if success else 1)
    
    elif command == "status":
        show_status()
    
    elif command == "all":
        log("🚀 DÉMARRAGE COMPLET")
        log("=" * 20)
        
        if start_api():
            sync_colab()
            log("\n✅ SYSTÈME PRÊT !")
            show_status()
        else:
            log("❌ Échec démarrage", "ERROR")
            sys.exit(1)
    
    else:
        print(f"Commande inconnue: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()