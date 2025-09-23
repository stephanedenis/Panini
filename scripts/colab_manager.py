#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire Communication Bidirectionnelle Colab
Gère les cycles Local ↔ Colab de façon transparente
"""

import sys
import subprocess
from pathlib import Path


class ColabCommunicationManager:
    """Gestionnaire communication bidirectionnelle avec Colab"""
    
    def __init__(self):
        self.repo_owner = "stephanedenis"
        self.repo_name = "PaniniFS-Research"
        
    def log(self, message: str, level: str = "INFO"):
        """Log avec timestamp"""
        import time
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def create_and_deploy_notebook(self, name: str, template: str = "dhatu_analysis", 
                                 auto_open: bool = False):
        """Créer et déployer notebook vers Colab"""
        self.log(f"🚀 Déploiement notebook: {name}")
        
        try:
            cmd = [
                sys.executable, "scripts/notebook_deployer.py",
                "--name", name,
                "--template", template
            ]
            
            if auto_open:
                cmd.append("--open")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                self.log("✅ Notebook déployé avec succès")
                
                # Extraire lien Colab du résultat
                lines = result.stdout.split('\n')
                colab_url = None
                for line in lines:
                    if "🔗 Colab:" in line:
                        colab_url = line.split("🔗 Colab: ")[1].strip()
                        break
                
                return True, colab_url
            else:
                self.log(f"❌ Erreur déploiement: {result.stderr}", "ERROR")
                return False, None
                
        except Exception as e:
            self.log(f"❌ Exception déploiement: {e}", "ERROR")
            return False, None
    
    def start_result_monitoring(self):
        """Démarre surveillance résultats Colab"""
        self.log("👀 Démarrage surveillance résultats")
        
        try:
            subprocess.Popen([
                sys.executable, "scripts/total_automation.py", "--start"
            ])
            self.log("✅ Surveillance active")
            return True
        except Exception as e:
            self.log(f"❌ Erreur surveillance: {e}", "ERROR")
            return False
    
    def check_communication_status(self):
        """Vérifie statut communication bidirectionnelle"""
        self.log("📊 Vérification statut communication")
        
        status = {
            "api_active": False,
            "notebooks_count": 0,
            "colab_results": 0,
            "automation_active": False
        }
        
        # API Status
        try:
            result = subprocess.run([
                sys.executable, "scripts/panini_manager.py", "status"
            ], capture_output=True, text=True, timeout=10)
            
            if "API: ✅ Active" in result.stdout:
                status["api_active"] = True
        except:
            pass
        
        # Notebooks count
        notebooks_dir = Path("colab_integration/notebooks")
        if notebooks_dir.exists():
            status["notebooks_count"] = len(list(notebooks_dir.glob("*.ipynb")))
        
        # Colab results
        results_dir = Path("colab_integration/results")
        if results_dir.exists():
            status["colab_results"] = len([d for d in results_dir.iterdir() if d.is_dir()])
        
        # Automation status
        try:
            result = subprocess.run([
                sys.executable, "scripts/total_automation.py", "--status"
            ], capture_output=True, text=True, timeout=10)
            
            if "Automatisation: ✅ Active" in result.stdout:
                status["automation_active"] = True
        except:
            pass
        
        return status
    
    def show_communication_dashboard(self):
        """Affiche dashboard communication"""
        status = self.check_communication_status()
        
        print("🔄 DASHBOARD COMMUNICATION COLAB")
        print("=" * 35)
        print()
        
        # Status général
        api_icon = "✅" if status["api_active"] else "❌"
        auto_icon = "✅" if status["automation_active"] else "❌"
        
        print(f"🔗 API Locale: {api_icon} {'Active' if status['api_active'] else 'Inactive'}")
        print(f"🤖 Automatisation: {auto_icon} {'Active' if status['automation_active'] else 'Arrêtée'}")
        print(f"📓 Notebooks Colab: {status['notebooks_count']}")
        print(f"📊 Sessions Résultats: {status['colab_results']}")
        print()
        
        # Liens directs
        print("🔗 LIENS RAPIDES:")
        print("   • Dashboard Local: http://localhost:5000/dashboard")
        print("   • Notebook Principal: https://colab.research.google.com/"
              f"github/{self.repo_owner}/{self.repo_name}/blob/main/"
              "PaniniFS_Colab_GPU.ipynb")
        print()
        
        # Actions disponibles
        print("🎯 ACTIONS RAPIDES:")
        print("   • Nouveau notebook: python3 scripts/colab_manager.py --create")
        print("   • Démarrer surveillance: python3 scripts/colab_manager.py --monitor")
        print("   • Sync résultats: python3 scripts/panini_manager.py sync")
        print()
        
        # Recommandations
        if not status["api_active"]:
            print("💡 RECOMMANDATION: Démarrer API locale")
            print("   python3 scripts/panini_manager.py start")
            print()
        
        if not status["automation_active"]:
            print("💡 RECOMMANDATION: Activer automatisation")
            print("   python3 scripts/total_automation.py --start")
            print()
    
    def setup_full_workflow(self):
        """Configuration workflow complet"""
        self.log("🚀 CONFIGURATION WORKFLOW COMPLET")
        print("=" * 40)
        
        # 1. Vérifier API
        self.log("1️⃣ Vérification API...")
        result = subprocess.run([
            sys.executable, "scripts/panini_manager.py", "all"
        ], timeout=30)
        
        if result.returncode == 0:
            self.log("✅ API configurée")
        else:
            self.log("❌ Erreur configuration API", "ERROR")
            return False
        
        # 2. Démarrer automatisation
        self.log("2️⃣ Configuration automatisation...")
        if self.start_result_monitoring():
            self.log("✅ Automatisation configurée")
        else:
            self.log("⚠️ Automatisation manuelle requise", "WARN")
        
        # 3. Vérifier notebooks existants
        self.log("3️⃣ Vérification notebooks...")
        notebooks_dir = Path("colab_integration/notebooks")
        if notebooks_dir.exists():
            notebooks = list(notebooks_dir.glob("*.ipynb"))
            self.log(f"📓 {len(notebooks)} notebooks disponibles")
        
        # 4. Configuration terminée
        self.log("✅ WORKFLOW CONFIGURÉ")
        print("\n🎯 SYSTÈME PRÊT POUR:")
        print("   • Création notebooks Local → Colab")
        print("   • Exécution GPU dans Colab")
        print("   • Synchronisation automatique Colab → Local")
        print("   • Monitoring continu bidirectionnel")
        
        return True


def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Gestionnaire Communication Colab")
    parser.add_argument("--create", metavar="NAME", help="Créer nouveau notebook")
    parser.add_argument("--template", default="dhatu_analysis", help="Template notebook")
    parser.add_argument("--open", action="store_true", help="Ouvrir dans Colab")
    parser.add_argument("--monitor", action="store_true", help="Démarrer surveillance")
    parser.add_argument("--status", action="store_true", help="Afficher dashboard")
    parser.add_argument("--setup", action="store_true", help="Configuration complète")
    
    args = parser.parse_args()
    
    manager = ColabCommunicationManager()
    
    if args.create:
        success, colab_url = manager.create_and_deploy_notebook(
            args.create, args.template, args.open
        )
        if success and colab_url:
            print(f"\n✅ Notebook créé: {args.create}")
            print(f"🔗 Colab: {colab_url}")
    
    elif args.monitor:
        manager.start_result_monitoring()
        print("👀 Surveillance démarrée")
    
    elif args.status:
        manager.show_communication_dashboard()
    
    elif args.setup:
        manager.setup_full_workflow()
    
    else:
        print("🔄 GESTIONNAIRE COMMUNICATION COLAB")
        print("=" * 35)
        print()
        print("Usage:")
        print("  python3 scripts/colab_manager.py --create NOM    # Nouveau notebook")
        print("  python3 scripts/colab_manager.py --monitor       # Surveillance")
        print("  python3 scripts/colab_manager.py --status        # Dashboard")
        print("  python3 scripts/colab_manager.py --setup         # Config complète")
        print()
        print("Exemples:")
        print("  python3 scripts/colab_manager.py --create \"analyse_syntaxique\" --open")
        print("  python3 scripts/colab_manager.py --create \"benchmark\" --template gpu_benchmark")
        print()
        print("🎯 Communication bidirectionnelle Local ↔ Colab")


if __name__ == "__main__":
    main()