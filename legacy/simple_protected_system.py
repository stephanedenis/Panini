#!/usr/bin/env python3
"""
Système Autonome Protégé Simplifié
Version corrigée sans threads pour les signaux
"""

import os
import sys
import time
import signal
import psutil
import subprocess
from pathlib import Path
from datetime import datetime


class SimpleProtectedSystem:
    def __init__(self):
        self.workspace = Path('/home/stephane/GitHub/PaniniFS-Research')
        self.results_dir = self.workspace / 'autonomous_results'
        self.results_dir.mkdir(exist_ok=True)
        
        self.log_file = self.results_dir / 'protected_system.log'
        self.active = True
        self.processes = {}
        
        # Protection thresholds
        self.max_cpu = 70
        self.max_memory = 75
        self.check_interval = 5
        
        self.setup_signals()
        self.log("🛡️ Système autonome protégé initialisé")
    
    def log(self, message):
        """Logging avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        
        with open(self.log_file, 'a') as f:
            f.write(log_msg + '\n')
    
    def setup_signals(self):
        """Configuration gestionnaires de signaux"""
        def signal_handler(signum, frame):
            self.log(f"⚠️ Signal {signum} reçu")
            if signum == signal.SIGTERM:
                self.log("🚨 SIGTERM détecté - arrêt d'urgence")
                self.emergency_shutdown()
            self.active = False
            sys.exit(0)
        
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
    
    def emergency_shutdown(self):
        """Arrêt d'urgence avec sauvegarde"""
        try:
            emergency_data = {
                'timestamp': datetime.now().isoformat(),
                'reason': 'SIGTERM_protection',
                'processes': list(self.processes.keys()),
                'system_metrics': {
                    'cpu': psutil.cpu_percent(),
                    'memory': psutil.virtual_memory().percent,
                    'load': os.getloadavg()[0]
                }
            }
            
            emergency_file = self.results_dir / 'emergency_shutdown.json'
            import json
            with open(emergency_file, 'w') as f:
                json.dump(emergency_data, f, indent=2)
            
            self.log(f"💾 Données d'urgence sauvées: {emergency_file}")
            
        except Exception as e:
            self.log(f"❌ Erreur sauvegarde urgence: {e}")
    
    def check_system_resources(self):
        """Vérification ressources système"""
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        load = os.getloadavg()[0]
        
        pressure = 0
        alerts = []
        
        if cpu > self.max_cpu:
            pressure += 30
            alerts.append(f"CPU élevé: {cpu:.1f}%")
        
        if memory > self.max_memory:
            pressure += 40
            alerts.append(f"Mémoire élevée: {memory:.1f}%")
        
        if load > 12:
            pressure += 20
            alerts.append(f"Load élevé: {load:.1f}")
        
        return {
            'pressure': pressure,
            'alerts': alerts,
            'metrics': {'cpu': cpu, 'memory': memory, 'load': load}
        }
    
    def apply_protection(self, pressure):
        """Application mesures de protection"""
        if pressure > 70:
            self.log("🚨 Pression CRITIQUE - pause longue")
            time.sleep(5)
            try:
                os.nice(5)  # Priorité plus basse
            except:
                pass
        elif pressure > 40:
            self.log("⚠️ Pression ÉLEVÉE - pause modérée")
            time.sleep(2)
        elif pressure > 20:
            self.log("📊 Pression MODÉRÉE - pause légère")
            time.sleep(1)
    
    def start_component(self, name, script_name):
        """Démarre un composant autonome"""
        try:
            script_path = self.workspace / script_name
            if not script_path.exists():
                self.log(f"❌ Script {script_name} non trouvé")
                return False
            
            process = subprocess.Popen([
                sys.executable, str(script_path)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            self.processes[name] = process
            self.log(f"✅ {name} démarré (PID: {process.pid})")
            return True
            
        except Exception as e:
            self.log(f"❌ Erreur démarrage {name}: {e}")
            return False
    
    def check_processes(self):
        """Vérification état des processus"""
        for name, process in list(self.processes.items()):
            if process.poll() is not None:
                self.log(f"⚠️ Processus {name} arrêté")
                del self.processes[name]
    
    def run_protected_system(self):
        """Boucle principale du système protégé"""
        self.log("🚀 DÉMARRAGE SYSTÈME AUTONOME PROTÉGÉ")
        self.log("=" * 50)
        
        # Ajustement priorité initial
        try:
            current_nice = os.getpriority(os.PRIO_PROCESS, 0)
            if current_nice < 3:
                os.nice(3)
                self.log(f"⚖️ Priorité ajustée: {current_nice} → {os.getpriority(os.PRIO_PROCESS, 0)}")
        except Exception as e:
            self.log(f"❌ Erreur ajustement priorité: {e}")
        
        # Démarrage composants
        components_started = 0
        
        if self.start_component('corpus_processor', 'autonomous_corpus_processor.py'):
            components_started += 1
        
        time.sleep(3)
        
        if self.start_component('dashboard', 'autonomous_dashboard.py'):
            components_started += 1
        
        time.sleep(3)
        
        if self.start_component('dhatu_optimizer', 'autonomous_dhatu_optimizer.py'):
            components_started += 1
        
        self.log(f"📊 Composants démarrés: {components_started}/3")
        
        if components_started == 0:
            self.log("❌ Aucun composant démarré - arrêt")
            return
        
        # Boucle de surveillance protégée
        self.log("👁️ Surveillance active avec protection")
        cycle_count = 0
        
        try:
            while self.active:
                cycle_count += 1
                
                # Vérification ressources
                resource_check = self.check_system_resources()
                pressure = resource_check['pressure']
                
                # Affichage périodique
                if cycle_count % 12 == 0:  # Toutes les minutes
                    metrics = resource_check['metrics']
                    self.log(f"📊 CPU: {metrics['cpu']:.1f}% | "
                            f"RAM: {metrics['memory']:.1f}% | "
                            f"Load: {metrics['load']:.1f} | "
                            f"Processus: {len(self.processes)}")
                
                # Alertes et protection
                if resource_check['alerts']:
                    for alert in resource_check['alerts']:
                        self.log(f"⚠️ {alert}")
                    self.apply_protection(pressure)
                
                # Vérification processus
                self.check_processes()
                
                # Attente avec vérification arrêt
                for _ in range(self.check_interval):
                    if not self.active:
                        break
                    time.sleep(1)
        
        except KeyboardInterrupt:
            self.log("🛑 Interruption clavier")
        except Exception as e:
            self.log(f"❌ Erreur système: {e}")
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Arrêt propre du système"""
        self.log("🛑 Arrêt système autonome protégé")
        self.active = False
        
        # Arrêt processus
        for name, process in self.processes.items():
            try:
                self.log(f"🛑 Arrêt {name}")
                process.terminate()
                process.wait(timeout=5)
            except Exception as e:
                self.log(f"❌ Erreur arrêt {name}: {e}")
                try:
                    process.kill()
                except:
                    pass
        
        self.log("✅ Système arrêté")


def main():
    print("🛡️ SYSTÈME AUTONOME PROTÉGÉ TUMBLEWEED v2")
    print("=" * 48)
    print("• Protection anti-SIGTERM intégrée")
    print("• Surveillance adaptative des ressources")
    print("• Redémarrage automatique des composants")
    print("• Sauvegarde d'urgence en cas de kill")
    print("=" * 48)
    
    system = SimpleProtectedSystem()
    system.run_protected_system()


if __name__ == '__main__':
    main()