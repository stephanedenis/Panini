#!/usr/bin/env python3
"""
Intégrateur Protection Autonome
Combine le système autonome avec la protection Tumbleweed
"""

import os
import sys
import time
import threading
import subprocess
from pathlib import Path
from datetime import datetime

# Import protection Tumbleweed
from tumbleweed_process_protector import TumbleweedProcessProtector, protect_function


class AutonomousProtectedSystem:
    def __init__(self):
        self.workspace = Path('/home/stephane/GitHub/PaniniFS-Research')
        self.protection = TumbleweedProcessProtector()
        self.autonomous_processes = {}
        self.system_active = True
        
        print("🚀 Système Autonome Protégé - Initialisation")
    
    def log(self, message):
        """Logging unifié"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    @protect_function
    def run_corpus_processor(self):
        """Lance processeur corpus avec protection"""
        try:
            self.log("📊 Démarrage processeur corpus protégé")
            
            script_path = self.workspace / 'autonomous_corpus_processor.py'
            if not script_path.exists():
                self.log(f"❌ Script non trouvé: {script_path}")
                return False
            
            # Lancement avec protection
            process = subprocess.Popen([
                sys.executable, str(script_path)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            self.autonomous_processes['corpus_processor'] = process
            self.log(f"✅ Processeur corpus lancé (PID: {process.pid})")
            
            return True
            
        except Exception as e:
            self.log(f"❌ Erreur lancement corpus processor: {e}")
            return False
    
    @protect_function
    def run_dashboard(self):
        """Lance dashboard avec protection"""
        try:
            self.log("🌐 Démarrage dashboard protégé")
            
            script_path = self.workspace / 'autonomous_dashboard.py'
            if not script_path.exists():
                self.log(f"❌ Script non trouvé: {script_path}")
                return False
            
            process = subprocess.Popen([
                sys.executable, str(script_path)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            self.autonomous_processes['dashboard'] = process
            self.log(f"✅ Dashboard lancé (PID: {process.pid})")
            
            return True
            
        except Exception as e:
            self.log(f"❌ Erreur lancement dashboard: {e}")
            return False
    
    @protect_function
    def run_dhatu_optimizer(self):
        """Lance optimiseur dhātu avec protection"""
        try:
            self.log("🔍 Démarrage optimiseur dhātu protégé")
            
            script_path = self.workspace / 'autonomous_dhatu_optimizer.py'
            if not script_path.exists():
                self.log(f"❌ Script non trouvé: {script_path}")
                return False
            
            process = subprocess.Popen([
                sys.executable, str(script_path)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            self.autonomous_processes['dhatu_optimizer'] = process
            self.log(f"✅ Optimiseur dhātu lancé (PID: {process.pid})")
            
            return True
            
        except Exception as e:
            self.log(f"❌ Erreur lancement dhātu optimizer: {e}")
            return False
    
    def monitor_processes(self):
        """Surveille les processus autonomes"""
        while self.system_active:
            try:
                for name, process in list(self.autonomous_processes.items()):
                    if process.poll() is not None:
                        self.log(f"⚠️ Processus {name} terminé - redémarrage")
                        
                        # Relancement automatique
                        if name == 'corpus_processor':
                            self.run_corpus_processor()
                        elif name == 'dashboard':
                            self.run_dashboard()
                        elif name == 'dhatu_optimizer':
                            self.run_dhatu_optimizer()
                
                time.sleep(30)  # Vérification toutes les 30s
                
            except Exception as e:
                self.log(f"❌ Erreur monitoring: {e}")
                time.sleep(60)
    
    def start_full_system(self):
        """Démarre le système complet protégé"""
        self.log("🚀 DÉMARRAGE SYSTÈME AUTONOME PROTÉGÉ")
        self.log("=" * 50)
        
        try:
            # Démarrage protection globale
            protection_thread = threading.Thread(
                target=self.protection.adaptive_protection_loop,
                daemon=True
            )
            protection_thread.start()
            self.log("🛡️ Protection système activée")
            
            # Démarrage composants autonomes
            success_count = 0
            
            if self.run_corpus_processor():
                success_count += 1
            
            time.sleep(2)  # Délai entre démarrages
            
            if self.run_dashboard():
                success_count += 1
            
            time.sleep(2)
            
            if self.run_dhatu_optimizer():
                success_count += 1
            
            self.log(f"📊 Composants démarrés: {success_count}/3")
            
            if success_count > 0:
                # Monitoring continu
                monitor_thread = threading.Thread(
                    target=self.monitor_processes,
                    daemon=True
                )
                monitor_thread.start()
                self.log("👁️ Monitoring activé")
                
                # Boucle principale
                self.log("✅ Système autonome protégé opérationnel")
                self.log("Press Ctrl+C pour arrêter")
                
                try:
                    while self.system_active:
                        time.sleep(60)
                        self.log("💓 Système actif - "
                               f"{len(self.autonomous_processes)} processus")
                        
                except KeyboardInterrupt:
                    self.shutdown_system()
            else:
                self.log("❌ Échec démarrage - aucun composant lancé")
        
        except Exception as e:
            self.log(f"❌ Erreur système: {e}")
            self.shutdown_system()
    
    def shutdown_system(self):
        """Arrêt propre du système"""
        self.log("🛑 Arrêt système autonome protégé")
        
        self.system_active = False
        
        # Arrêt processus
        for name, process in self.autonomous_processes.items():
            try:
                self.log(f"🛑 Arrêt {name} (PID: {process.pid})")
                process.terminate()
                process.wait(timeout=10)
            except Exception as e:
                self.log(f"❌ Erreur arrêt {name}: {e}")
                try:
                    process.kill()
                except:
                    pass
        
        # Arrêt protection
        self.protection.stop_protection()
        
        self.log("✅ Système arrêté proprement")


def main():
    """Point d'entrée principal"""
    print("🛡️ SYSTÈME AUTONOME PROTÉGÉ TUMBLEWEED")
    print("=" * 45)
    print("Protection automatique contre SIGTERM")
    print("Monitoring adaptatif des ressources")
    print("Redémarrage automatique des composants")
    print("=" * 45)
    
    system = AutonomousProtectedSystem()
    
    try:
        system.start_full_system()
    except KeyboardInterrupt:
        system.shutdown_system()
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        system.shutdown_system()


if __name__ == '__main__':
    main()