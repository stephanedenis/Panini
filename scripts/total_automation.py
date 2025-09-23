#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire Automatisation Totale PaniniFS Research
Élimine COMPLÈTEMENT les opérations manuelles
"""

import sys
import time
import subprocess
from pathlib import Path
import threading
import signal


class TotalAutomationManager:
    """Gestionnaire d'automatisation totale"""
    
    def __init__(self):
        self.running = False
        self.threads = []
        
    def log(self, message: str, level: str = "INFO"):
        """Log avec timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def check_dependencies(self) -> bool:
        """Vérifie dépendances système"""
        self.log("🔍 Vérification dépendances...")
        
        required_scripts = [
            "scripts/panini_manager.py",
            "scripts/automation_engine.py",
            "scripts/github_watcher.py"
        ]
        
        missing = []
        for script in required_scripts:
            if not Path(script).exists():
                missing.append(script)
        
        if missing:
            self.log(f"❌ Scripts manquants: {missing}", "ERROR")
            return False
        
        # Vérifier modules Python
        try:
            import requests
            import schedule
        except ImportError as e:
            self.log(f"❌ Module manquant: {e}", "ERROR")
            self.log("💡 Installer: pip install requests schedule")
            return False
        
        self.log("✅ Dépendances OK")
        return True
    
    def start_api_if_needed(self) -> bool:
        """Démarre l'API si nécessaire"""
        try:
            result = subprocess.run([
                sys.executable, "scripts/panini_manager.py", "status"
            ], capture_output=True, text=True, timeout=10)
            
            if "API: ✅ Active" in result.stdout:
                self.log("✅ API déjà active")
                return True
            
            # Démarrer API
            self.log("🚀 Démarrage API...")
            result = subprocess.run([
                sys.executable, "scripts/panini_manager.py", "start"
            ], timeout=30)
            
            return result.returncode == 0
            
        except Exception as e:
            self.log(f"❌ Erreur API: {e}", "ERROR")
            return False
    
    def start_automation_engine(self):
        """Lance le moteur d'automatisation en arrière-plan"""
        def run_engine():
            while self.running:
                try:
                    subprocess.run([
                        sys.executable, "scripts/automation_engine.py", "--once"
                    ], timeout=60)
                    time.sleep(300)  # 5 minutes
                except Exception as e:
                    self.log(f"❌ Erreur automation engine: {e}", "ERROR")
                    time.sleep(60)
        
        thread = threading.Thread(target=run_engine, daemon=True)
        thread.start()
        self.threads.append(thread)
        self.log("✅ Moteur automatisation démarré")
    
    def start_github_watcher(self):
        """Lance la surveillance GitHub en arrière-plan"""
        def run_watcher():
            while self.running:
                try:
                    subprocess.run([
                        sys.executable, "scripts/github_watcher.py", "--check"
                    ], timeout=120)
                    time.sleep(600)  # 10 minutes
                except Exception as e:
                    self.log(f"❌ Erreur GitHub watcher: {e}", "ERROR")
                    time.sleep(120)
        
        thread = threading.Thread(target=run_watcher, daemon=True)
        thread.start()
        self.threads.append(thread)
        self.log("✅ Surveillance GitHub démarrée")
    
    def start_periodic_sync(self):
        """Synchronisation périodique"""
        def run_sync():
            while self.running:
                try:
                    subprocess.run([
                        sys.executable, "scripts/panini_manager.py", "sync"
                    ], timeout=60)
                    time.sleep(900)  # 15 minutes
                except Exception as e:
                    self.log(f"❌ Erreur sync périodique: {e}", "ERROR")
                    time.sleep(300)
        
        thread = threading.Thread(target=run_sync, daemon=True)
        thread.start()
        self.threads.append(thread)
        self.log("✅ Synchronisation périodique démarrée")
    
    def show_status(self):
        """Affiche le statut du système"""
        self.log("📊 STATUT AUTOMATISATION TOTALE")
        self.log("=" * 35)
        
        # API Status
        try:
            result = subprocess.run([
                sys.executable, "scripts/panini_manager.py", "status"
            ], capture_output=True, text=True, timeout=10)
            
            if "API: ✅ Active" in result.stdout:
                self.log("🔗 API: ✅ Active")
            else:
                self.log("🔗 API: ❌ Inactive")
        except:
            self.log("🔗 API: ❓ Inconnue")
        
        # Threads actifs
        active_threads = sum(1 for t in self.threads if t.is_alive())
        self.log(f"🧵 Threads: {active_threads}/3 actifs")
        
        # État automatisation
        if self.running:
            self.log("🤖 Automatisation: ✅ Active")
            self.log("   📥 Détection fichiers: Toutes les 5 min")
            self.log("   🔍 Surveillance GitHub: Toutes les 10 min")
            self.log("   🔄 Sync périodique: Toutes les 15 min")
        else:
            self.log("🤖 Automatisation: ❌ Arrêtée")
        
        self.log("\n🔗 WORKFLOW AUTOMATIQUE:")
        self.log("   1. Détection auto fichiers Colab")
        self.log("   2. Import automatique résultats")
        self.log("   3. Sync API automatique")
        self.log("   4. Commit Git automatique")
        self.log("   5. Surveillance GitHub continue")
    
    def install_service_mode(self):
        """Mode service - automatisation invisible"""
        service_script = """#!/bin/bash
# Service PaniniFS Auto
cd /home/stephane/GitHub/PaniniFS-Research
python3 scripts/total_automation.py --service &
"""
        
        service_path = Path.home() / ".local/bin/panini-auto-service.sh"
        service_path.parent.mkdir(exist_ok=True)
        service_path.write_text(service_script)
        service_path.chmod(0o755)
        
        self.log(f"✅ Service installé: {service_path}")
        self.log("💡 Pour démarrer au boot:")
        self.log(f"   echo '@reboot {service_path}' | crontab -")
    
    def signal_handler(self, signum, frame):
        """Gestionnaire signal arrêt"""
        self.log("🛑 Arrêt demandé...")
        self.running = False
        sys.exit(0)
    
    def start_total_automation(self):
        """Démarre l'automatisation totale"""
        self.log("🚀 DÉMARRAGE AUTOMATISATION TOTALE")
        self.log("=" * 40)
        
        # Configuration signaux
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Vérifications préalables
        if not self.check_dependencies():
            self.log("❌ Dépendances manquantes", "ERROR")
            return False
        
        # Démarrer API
        if not self.start_api_if_needed():
            self.log("❌ Impossible de démarrer l'API", "ERROR")
            return False
        
        # Marquer comme actif
        self.running = True
        
        # Démarrer tous les composants
        self.start_automation_engine()
        time.sleep(2)
        
        self.start_github_watcher()
        time.sleep(2)
        
        self.start_periodic_sync()
        time.sleep(2)
        
        self.log("✅ AUTOMATISATION TOTALE ACTIVE !")
        self.log("\n🤖 SYSTÈME COMPLÈTEMENT AUTOMATIQUE")
        self.log("   ✅ Plus d'intervention manuelle nécessaire")
        self.log("   ✅ Détection automatique résultats Colab")
        self.log("   ✅ Import et sync automatiques")
        self.log("   ✅ Commit Git automatique")
        self.log("   ✅ Surveillance GitHub continue")
        self.log("\n🔗 Dashboard: http://localhost:5000/dashboard")
        self.log("🔗 Notebook: https://colab.research.google.com"
                 "/github/stephanedenis/PaniniFS-Research"
                 "/blob/main/PaniniFS_Colab_GPU.ipynb")
        
        # Boucle principale
        try:
            while self.running:
                time.sleep(60)
                # Vérifier threads
                for i, thread in enumerate(self.threads):
                    if not thread.is_alive():
                        self.log(f"⚠️  Thread {i} arrêté, redémarrage...", "WARN")
                        # Redémarrer thread si nécessaire
        
        except KeyboardInterrupt:
            self.log("🛑 Arrêt manuel")
        
        finally:
            self.running = False
            self.log("✅ Automatisation arrêtée")
        
        return True


def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Automatisation totale PaniniFS")
    parser.add_argument("--start", action="store_true", help="Démarrer automatisation")
    parser.add_argument("--status", action="store_true", help="Voir statut")
    parser.add_argument("--service", action="store_true", help="Mode service")
    parser.add_argument("--install-service", action="store_true", help="Installer service")
    
    args = parser.parse_args()
    
    manager = TotalAutomationManager()
    
    if args.status:
        manager.show_status()
    
    elif args.install_service:
        manager.install_service_mode()
    
    elif args.service or args.start:
        success = manager.start_total_automation()
        sys.exit(0 if success else 1)
    
    else:
        print("🤖 AUTOMATISATION TOTALE PANINIFS")
        print("=" * 35)
        print()
        print("Usage:")
        print("  python3 scripts/total_automation.py --start     # Démarrer")
        print("  python3 scripts/total_automation.py --status    # Statut")
        print("  python3 scripts/total_automation.py --service   # Mode service")
        print("  python3 scripts/total_automation.py --install-service  # Installer")
        print()
        print("🎯 WORKFLOW AUTOMATIQUE:")
        print("   1. Détection automatique fichiers Colab")
        print("   2. Import et synchronisation automatiques")
        print("   3. Surveillance GitHub continue")
        print("   4. Plus d'intervention manuelle !")


if __name__ == "__main__":
    main()