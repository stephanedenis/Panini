#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launcher Intégration Colab Pro - PaniniFS Research
Script unique pour démarrer le système complet d'intégration
"""

import os
import sys
import time
import signal
import subprocess
import threading
import webbrowser
from pathlib import Path
import argparse
import psutil


class ColabIntegrationLauncher:
    """Launcher principal pour l'intégration Colab Pro"""
    
    def __init__(self):
        self.workspace_root = Path(__file__).parent.parent
        self.processes = []
        self.running = False
        
    def log(self, message: str, level: str = "INFO"):
        """Log avec timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def check_dependencies(self) -> bool:
        """Vérifie les dépendances requises"""
        self.log("Vérification des dépendances...")
        
        # Vérifier Python
        python_version = sys.version_info
        if python_version < (3, 8):
            self.log(f"Python 3.8+ requis, trouvé: {python_version}", "ERROR")
            return False
        
        # Vérifier modules Python
        required_modules = [
            'flask', 'flask_socketio', 'requests', 'sqlite3', 
            'asyncio', 'json', 'pathlib'
        ]
        
        missing_modules = []
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing_modules.append(module)
        
        if missing_modules:
            self.log(f"Modules manquants: {missing_modules}", "ERROR")
            self.log("Installer avec: pip install flask flask-socketio requests", "INFO")
            return False
        
        # Vérifier structure de fichiers
        required_files = [
            'src/cloud/integration_manager.py',
            'src/cloud/api_rest.py',
            'src/web/dashboard_colab_integration.html',
            'colab_notebooks/panini_dhatu_analysis.ipynb'
        ]
        
        missing_files = []
        for file_path in required_files:
            if not (self.workspace_root / file_path).exists():
                missing_files.append(file_path)
        
        if missing_files:
            self.log(f"Fichiers manquants: {missing_files}", "ERROR")
            return False
        
        self.log("✓ Toutes les dépendances sont satisfaites")
        return True
    
    def check_ports(self, ports: list) -> bool:
        """Vérifie disponibilité des ports"""
        for port in ports:
            for conn in psutil.net_connections():
                if conn.laddr.port == port and conn.status == 'LISTEN':
                    self.log(f"Port {port} déjà utilisé par PID {conn.pid}", "WARNING")
                    return False
        return True
    
    def start_integration_api(self):
        """Démarre l'API d'intégration"""
        self.log("Démarrage API d'intégration...")
        
        api_script = self.workspace_root / "src/cloud/api_rest.py"
        
        # Démarrer processus API
        proc = subprocess.Popen(
            [sys.executable, str(api_script)],
            cwd=self.workspace_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        self.processes.append(proc)
        self.log(f"API démarrée (PID: {proc.pid})")
        
        # Attendre que l'API soit prête
        max_wait = 30
        for i in range(max_wait):
            try:
                import requests
                response = requests.get("http://localhost:5000/health", timeout=2)
                if response.status_code == 200:
                    self.log("✓ API opérationnelle sur http://localhost:5000")
                    return True
            except:
                pass
            
            if i < max_wait - 1:
                time.sleep(1)
        
        self.log("API ne répond pas dans les temps", "ERROR")
        return False
    
    def open_dashboard(self):
        """Ouvre le dashboard web"""
        dashboard_path = self.workspace_root / "src/web/dashboard_colab_integration.html"
        dashboard_url = f"file://{dashboard_path.absolute()}"
        
        self.log(f"Ouverture dashboard: {dashboard_url}")
        
        try:
            webbrowser.open(dashboard_url)
            self.log("✓ Dashboard ouvert dans le navigateur")
        except Exception as e:
            self.log(f"Erreur ouverture dashboard: {e}", "ERROR")
            self.log(f"Ouvrir manuellement: {dashboard_url}", "INFO")
    
    def run_quick_test(self):
        """Lance un test rapide du système"""
        self.log("Lancement test rapide...")
        
        test_script = self.workspace_root / "scripts/test_integration_colab.py"
        
        proc = subprocess.run(
            [sys.executable, str(test_script), "--quick"],
            cwd=self.workspace_root,
            capture_output=True,
            text=True
        )
        
        if proc.returncode == 0:
            self.log("✓ Tests rapides réussis")
            return True
        else:
            self.log(f"Tests échoués: {proc.stderr}", "ERROR")
            return False
    
    def show_usage_info(self):
        """Affiche informations d'utilisation"""
        print("\n" + "="*60)
        print("🚀 SYSTÈME D'INTÉGRATION COLAB PRO DÉMARRÉ")
        print("="*60)
        print()
        print("📍 URLs importantes:")
        print("   • API REST: http://localhost:5000")
        print("   • Health check: http://localhost:5000/health")
        print("   • Dashboard: Ouvert dans navigateur")
        print()
        print("📋 Prochaines étapes:")
        print("   1. Vérifier dashboard web (ouvert automatiquement)")
        print("   2. Uploader notebooks vers Google Colab Pro:")
        print("      - colab_notebooks/panini_test_colab.ipynb")
        print("      - colab_notebooks/panini_dhatu_analysis.ipynb")
        print("   3. Soumettre premier job via dashboard ou API")
        print()
        print("🔧 Commandes utiles:")
        print("   • Test système: python3 scripts/test_integration_colab.py")
        print("   • API santé: curl http://localhost:5000/health")
        print("   • Arrêt système: Ctrl+C")
        print()
        print("📖 Documentation complète:")
        print("   docs/GUIDE_COLAB_PRO_INTEGRATION.md")
        print()
        print("="*60)
    
    def setup_signal_handlers(self):
        """Configure gestionnaires de signaux"""
        def signal_handler(signum, frame):
            self.log("Signal reçu, arrêt en cours...")
            self.shutdown()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def monitor_processes(self):
        """Surveille les processus en arrière-plan"""
        while self.running:
            for proc in self.processes[:]:  # Copie pour éviter modification pendant itération
                if proc.poll() is not None:  # Processus terminé
                    self.log(f"Processus {proc.pid} terminé avec code {proc.returncode}", "WARNING")
                    self.processes.remove(proc)
            
            time.sleep(5)
    
    def shutdown(self):
        """Arrêt propre du système"""
        self.log("Arrêt du système d'intégration...")
        self.running = False
        
        for proc in self.processes:
            try:
                self.log(f"Arrêt processus {proc.pid}...")
                proc.terminate()
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.log(f"Force kill processus {proc.pid}")
                proc.kill()
            except Exception as e:
                self.log(f"Erreur arrêt processus {proc.pid}: {e}", "ERROR")
        
        self.log("✓ Système arrêté proprement")
    
    def start_full_system(self, open_browser: bool = True, run_tests: bool = True):
        """Démarre le système complet"""
        self.log("🚀 DÉMARRAGE SYSTÈME INTÉGRATION COLAB PRO")
        self.log("="*50)
        
        # 1. Vérifications préalables
        if not self.check_dependencies():
            return False
        
        if not self.check_ports([5000]):
            self.log("Port 5000 occupé - arrêter processus existant ou changer port", "ERROR")
            return False
        
        # 2. Tests rapides (optionnel)
        if run_tests:
            if not self.run_quick_test():
                self.log("Tests échoués - continuer quand même? (y/N)", "WARNING")
                if input().lower() != 'y':
                    return False
        
        # 3. Démarrage API
        if not self.start_integration_api():
            return False
        
        # 4. Ouverture dashboard
        if open_browser:
            time.sleep(2)  # Attendre que l'API soit stable
            self.open_dashboard()
        
        # 5. Configuration monitoring
        self.running = True
        self.setup_signal_handlers()
        
        # 6. Affichage informations
        self.show_usage_info()
        
        # 7. Démarrage monitoring
        monitor_thread = threading.Thread(target=self.monitor_processes, daemon=True)
        monitor_thread.start()
        
        # 8. Boucle principale
        try:
            self.log("Système prêt - Appuyer Ctrl+C pour arrêter")
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            self.shutdown()
        
        return True


def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description="Launcher système d'intégration Colab Pro"
    )
    parser.add_argument(
        '--no-browser', 
        action='store_true',
        help="Ne pas ouvrir le dashboard automatiquement"
    )
    parser.add_argument(
        '--no-tests',
        action='store_true',
        help="Ignorer les tests rapides au démarrage"
    )
    parser.add_argument(
        '--check-only',
        action='store_true',
        help="Vérifier dépendances seulement"
    )
    
    args = parser.parse_args()
    
    launcher = ColabIntegrationLauncher()
    
    if args.check_only:
        success = launcher.check_dependencies()
        return 0 if success else 1
    
    success = launcher.start_full_system(
        open_browser=not args.no_browser,
        run_tests=not args.no_tests
    )
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())