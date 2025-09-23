#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lanceur simplifié PaniniFS Research
Remplace les scripts .sh par version Python intégrée
"""

import sys
import time
import json
import subprocess
from pathlib import Path
from datetime import datetime


class PaniniFSLauncher:
    """Lanceur simplifié pour PaniniFS Research"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.api_script = self.repo_path / "src" / "cloud" / "api_rest.py"
        self.sync_script = self.repo_path / "scripts" / "sync_colab_results.py"
        
    def log(self, message: str, level: str = "INFO"):
        """Log avec timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def check_api_status(self) -> bool:
        """Vérifie si l'API est déjà active"""
        try:
            import requests
            response = requests.get("http://localhost:5000/health", timeout=3)
            return response.status_code == 200
        except:
            return False
    
    def start_api(self) -> bool:
        """Démarre l'API REST en arrière-plan"""
        if self.check_api_status():
            self.log("✅ API déjà active sur http://localhost:5000")
            return True
        
        if not self.api_script.exists():
            self.log(f"❌ Script API non trouvé: {self.api_script}", "ERROR")
            return False
        
        self.log("🚀 Démarrage API REST...")
        
        try:
            # Démarrer en arrière-plan
            subprocess.Popen([
                sys.executable, str(self.api_script)
            ], cwd=self.repo_path)
            
            # Attendre que l'API soit prête
            for i in range(10):
                time.sleep(1)
                if self.check_api_status():
                    self.log("✅ API active sur http://localhost:5000")
                    return True
                self.log(f"   Attente API... ({i+1}/10)")
            
            self.log("❌ Timeout démarrage API", "ERROR")
            return False
            
        except Exception as e:
            self.log(f"❌ Erreur démarrage API: {e}", "ERROR")
            return False
    
    def sync_colab_results(self) -> bool:
        """Synchronise les résultats Colab"""
        if not self.sync_script.exists():
            self.log(f"❌ Script sync non trouvé: {self.sync_script}", "ERROR")
            return False
        
        self.log("🔄 Synchronisation résultats Colab...")
        
        try:
            result = subprocess.run([
                sys.executable, str(self.sync_script)
            ], cwd=self.repo_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log("✅ Synchronisation terminée")
                # Afficher output du sync
                if result.stdout.strip():
                    for line in result.stdout.strip().split('\n'):
                        print(f"   {line}")
                return True
            else:
                self.log(f"❌ Erreur sync: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Erreur sync: {e}", "ERROR")
            return False
    
    def show_status(self):
        """Affiche le statut du système"""
        self.log("📊 STATUT SYSTÈME PANINIFS")
        self.log("=" * 30)
        
        # API Status
        api_active = self.check_api_status()
        self.log(f"🔗 API REST: {'✅ Active' if api_active else '❌ Inactive'}")
        
        if api_active:
            try:
                import requests
                response = requests.get("http://localhost:5000/health")
                health = response.json()
                self.log(f"   Jobs actifs: {health.get('active_jobs', 0)}")
                self.log(f"   Queue size: {health.get('queue_size', 0)}")
                self.log(f"   Manager: {health.get('integration_manager', 'unknown')}")
            except:
                pass
        
        # Notebooks Colab
        notebook_main = self.repo_path / "PaniniFS_Colab_GPU.ipynb"
        notebook_advanced = self.repo_path / "colab_integration" / "notebooks" / "panini_github_colab_integration.ipynb"
        
        self.log(f"📓 Notebook principal: {'✅' if notebook_main.exists() else '❌'}")
        self.log(f"📓 Notebook avancé: {'✅' if notebook_advanced.exists() else '❌'}")
        
        # Résultats Colab
        results_dir = self.repo_path / "colab_integration" / "results"
        if results_dir.exists():
            session_count = len([d for d in results_dir.iterdir() if d.is_dir()])
            self.log(f"📊 Sessions Colab: {session_count}")
        else:
            self.log("📊 Sessions Colab: 0")
        
        # Liens utiles
        self.log("\n🔗 LIENS UTILES:")
        self.log("   Dashboard: http://localhost:5000/dashboard")
        self.log("   API Health: http://localhost:5000/health")
        self.log("   Colab Notebook: https://colab.research.google.com/github/stephanedenis/PaniniFS-Research/blob/main/PaniniFS_Colab_GPU.ipynb")
    
    def run_full_workflow(self):
        """Workflow complet de démarrage"""
        self.log("🚀 DÉMARRAGE WORKFLOW PANINIFS")
        self.log("=" * 35)
        
        # 1. Démarrer API
        if not self.start_api():
            self.log("❌ Impossible de démarrer l'API", "ERROR")
            return False
        
        # 2. Synchroniser résultats Colab
        if not self.sync_colab_results():
            self.log("⚠️  Synchronisation échouée, mais API active", "WARNING")
        
        # 3. Afficher statut final
        self.log("\n" + "="*35)
        self.show_status()
        
        self.log("\n🎯 WORKFLOW PRÊT !")
        self.log("Utilisez 'python3 scripts/launcher.py --status' pour vérifier l'état")
        
        return True


def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Lanceur PaniniFS Research")
    parser.add_argument("--status", action="store_true", help="Afficher statut système")
    parser.add_argument("--start-api", action="store_true", help="Démarrer API seulement")
    parser.add_argument("--sync", action="store_true", help="Sync Colab seulement")
    parser.add_argument("--repo", default=".", help="Chemin repository")
    
    args = parser.parse_args()
    
    launcher = PaniniFSLauncher(args.repo)
    
    if args.status:
        launcher.show_status()
    elif args.start_api:
        success = launcher.start_api()
        sys.exit(0 if success else 1)
    elif args.sync:
        success = launcher.sync_colab_results()
        sys.exit(0 if success else 1)
    else:
        # Workflow complet par défaut
        success = launcher.run_full_workflow()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()