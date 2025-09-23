#!/usr/bin/env python3
"""
Protection Avancée Tumbleweed - Système anti-kill OS
Prévient les SIGTERM en surveillant et limitant les ressources
"""

import os
import sys
import time
import signal
import psutil
import threading
import json
from pathlib import Path
from datetime import datetime


class TumbleweedProcessProtector:
    def __init__(self):
        self.workspace = Path('/home/stephane/GitHub/PaniniFS-Research')
        self.log_file = self.workspace / 'autonomous_results' / 'protection.log'
        
        # Seuils de protection (basés sur l'analyse système)
        self.thresholds = {
            'cpu_max': 70,      # Max 70% CPU pour éviter thermal throttling
            'memory_max': 75,   # Max 75% RAM pour éviter OOM killer
            'load_max': 12,     # Max 12 sur 16 cores
            'processes_max': 50000,  # Bien en dessous de ulimit 256426
            'check_interval': 3      # Vérification toutes les 3s
        }
        
        # État de protection
        self.protection_active = True
        self.throttle_mode = False
        self.warning_count = 0
        self.last_throttle = 0
        
        # Processus surveillés
        self.monitored_pids = set()
        
        self.log("🛡️ Protection Tumbleweed initialisée")
        self.setup_signal_handlers()
    
    def log(self, message):
        """Logging avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        with open(self.log_file, 'a') as f:
            f.write(log_message + '\n')
    
    def setup_signal_handlers(self):
        """Configure gestionnaires de signaux"""
        def signal_handler(signum, frame):
            self.log(f"⚠️ Signal {signum} reçu - protection activée")
            if signum == signal.SIGTERM:
                self.log("🛑 SIGTERM détecté - sauvegarde d'urgence")
                self.emergency_save()
            sys.exit(0)
        
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGUSR1, signal_handler)
    
    def emergency_save(self):
        """Sauvegarde d'urgence avant kill"""
        try:
            emergency_data = {
                'timestamp': datetime.now().isoformat(),
                'reason': 'SIGTERM_received',
                'system_state': {
                    'cpu_percent': psutil.cpu_percent(),
                    'memory_percent': psutil.virtual_memory().percent,
                    'load_avg': os.getloadavg(),
                    'process_count': len(psutil.pids())
                },
                'monitored_processes': list(self.monitored_pids)
            }
            
            emergency_file = self.workspace / 'autonomous_results' / 'emergency_save.json'
            with open(emergency_file, 'w') as f:
                json.dump(emergency_data, f, indent=2)
            
            self.log(f"💾 Sauvegarde d'urgence: {emergency_file}")
            
        except Exception as e:
            self.log(f"❌ Erreur sauvegarde urgence: {e}")
    
    def adjust_process_priority(self):
        """Ajuste la priorité du processus"""
        try:
            current_nice = os.getpriority(os.PRIO_PROCESS, 0)
            if current_nice < 5:
                os.nice(5)  # Priorité plus basse
                self.log(f"⚖️ Priorité ajustée: {current_nice} → {os.getpriority(os.PRIO_PROCESS, 0)}")
        except Exception as e:
            self.log(f"❌ Erreur ajustement priorité: {e}")
    
    def check_system_pressure(self):
        """Vérifie la pression système"""
        try:
            # Métriques système
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            load_avg = os.getloadavg()[0]  # Load 1 minute
            process_count = len(psutil.pids())
            
            pressure_score = 0
            warnings = []
            
            # Évaluation CPU
            if cpu_percent > self.thresholds['cpu_max']:
                pressure_score += 30
                warnings.append(f"CPU élevé: {cpu_percent:.1f}%")
            
            # Évaluation mémoire
            if memory.percent > self.thresholds['memory_max']:
                pressure_score += 40
                warnings.append(f"RAM élevée: {memory.percent:.1f}%")
            
            # Évaluation load average
            if load_avg > self.thresholds['load_max']:
                pressure_score += 20
                warnings.append(f"Load élevé: {load_avg:.1f}")
            
            # Évaluation nombre processus
            if process_count > self.thresholds['processes_max']:
                pressure_score += 10
                warnings.append(f"Trop de processus: {process_count}")
            
            return {
                'score': pressure_score,
                'warnings': warnings,
                'metrics': {
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory.percent,
                    'load_avg': load_avg,
                    'process_count': process_count
                }
            }
            
        except Exception as e:
            self.log(f"❌ Erreur check pressure: {e}")
            return {'score': 0, 'warnings': [], 'metrics': {}}
    
    def apply_throttling(self, pressure_level):
        """Applique limitation selon niveau de pression"""
        current_time = time.time()
        
        if pressure_level > 70:  # Pression critique
            if current_time - self.last_throttle > 5:  # Éviter spam
                self.log("🚨 Pression CRITIQUE - throttling agressif")
                time.sleep(3)  # Pause longue
                
                # Forcer garbage collection
                import gc
                gc.collect()
                
                # Réduire priorité si possible
                try:
                    os.nice(2)
                except:
                    pass
                
                self.last_throttle = current_time
                
        elif pressure_level > 50:  # Pression élevée
            if current_time - self.last_throttle > 10:
                self.log("⚠️ Pression ÉLEVÉE - throttling modéré")
                time.sleep(1.5)
                self.last_throttle = current_time
                
        elif pressure_level > 30:  # Pression modérée
            if current_time - self.last_throttle > 15:
                self.log("📊 Pression MODÉRÉE - throttling léger")
                time.sleep(0.5)
                self.last_throttle = current_time
    
    def monitor_child_processes(self):
        """Surveille les processus enfants"""
        try:
            current_process = psutil.Process()
            children = current_process.children(recursive=True)
            
            for child in children:
                try:
                    if child.pid not in self.monitored_pids:
                        self.monitored_pids.add(child.pid)
                        self.log(f"👶 Nouveau processus enfant: PID {child.pid}")
                    
                    # Vérifier si processus consomme trop
                    child_cpu = child.cpu_percent()
                    child_memory = child.memory_percent()
                    
                    if child_cpu > 50 or child_memory > 20:
                        self.log(f"⚠️ Processus gourmand PID {child.pid}: CPU {child_cpu:.1f}% RAM {child_memory:.1f}%")
                        
                        # Ajuster priorité du processus enfant
                        try:
                            child.nice(10)
                        except:
                            pass
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    if child.pid in self.monitored_pids:
                        self.monitored_pids.remove(child.pid)
                        
        except Exception as e:
            self.log(f"❌ Erreur monitoring enfants: {e}")
    
    def adaptive_protection_loop(self):
        """Boucle de protection adaptative"""
        self.log("🔄 Démarrage protection adaptative")
        
        while self.protection_active:
            try:
                # Vérification pression système
                pressure_data = self.check_system_pressure()
                pressure_score = pressure_data['score']
                
                # Affichage périodique des métriques
                if int(time.time()) % 30 == 0:  # Toutes les 30s
                    metrics = pressure_data['metrics']
                    self.log(f"📊 CPU: {metrics.get('cpu_percent', 0):.1f}% | "
                            f"RAM: {metrics.get('memory_percent', 0):.1f}% | "
                            f"Load: {metrics.get('load_avg', 0):.1f} | "
                            f"Pression: {pressure_score}")
                
                # Application throttling si nécessaire
                if pressure_score > 0:
                    self.warning_count += 1
                    for warning in pressure_data['warnings']:
                        self.log(f"⚠️ {warning}")
                    
                    self.apply_throttling(pressure_score)
                else:
                    self.warning_count = 0
                
                # Surveillance processus enfants
                self.monitor_child_processes()
                
                # Ajustement automatique seuils
                if self.warning_count > 10:
                    self.log("🔧 Ajustement seuils - système sous pression")
                    self.thresholds['cpu_max'] = max(60, self.thresholds['cpu_max'] - 5)
                    self.thresholds['memory_max'] = max(65, self.thresholds['memory_max'] - 5)
                    self.warning_count = 0
                
                time.sleep(self.thresholds['check_interval'])
                
            except KeyboardInterrupt:
                self.log("🛑 Interruption protection")
                break
            except Exception as e:
                self.log(f"❌ Erreur boucle protection: {e}")
                time.sleep(10)
    
    def start_protection(self, target_function=None, *args, **kwargs):
        """Démarre protection en arrière-plan"""
        # Ajustement initial
        self.adjust_process_priority()
        
        # Thread de protection
        protection_thread = threading.Thread(
            target=self.adaptive_protection_loop, 
            daemon=True
        )
        protection_thread.start()
        
        self.log("✅ Protection système activée")
        
        # Exécution fonction cible si fournie
        if target_function:
            try:
                self.log(f"🎯 Exécution fonction protégée: {target_function.__name__}")
                return target_function(*args, **kwargs)
            except Exception as e:
                self.log(f"❌ Erreur fonction protégée: {e}")
                raise
        else:
            # Mode surveillance uniquement
            try:
                while self.protection_active:
                    time.sleep(60)
            except KeyboardInterrupt:
                self.log("🛑 Arrêt protection")
    
    def stop_protection(self):
        """Arrête la protection"""
        self.protection_active = False
        self.log("🛑 Protection arrêtée")


def protect_function(func):
    """Décorateur pour protéger une fonction"""
    def wrapper(*args, **kwargs):
        protector = TumbleweedProcessProtector()
        return protector.start_protection(func, *args, **kwargs)
    return wrapper


# Exemple d'utilisation
@protect_function
def intensive_computation():
    """Exemple de calcul intensif protégé"""
    print("🚀 Début calcul intensif protégé")
    
    for i in range(1000000):
        # Simulation calcul intensif
        result = sum(range(100))
        
        if i % 100000 == 0:
            print(f"📊 Progression: {i/10000:.1f}%")
    
    print("✅ Calcul terminé")


def main():
    print("🛡️ SYSTÈME PROTECTION TUMBLEWEED")
    print("=" * 40)
    
    # Test du système de protection
    protector = TumbleweedProcessProtector()
    
    try:
        # Démonstration protection
        protector.start_protection()
    except KeyboardInterrupt:
        protector.stop_protection()


if __name__ == '__main__':
    main()