#!/usr/bin/env python3
"""
Système Auto-Recovery Autonome - Reprise automatique après crash
Garantit la continuité de l'autonomie même après redémarrage OS/VS Code
"""

import os
import sys
import json
import time
import signal
import subprocess
from datetime import datetime
from pathlib import Path
import psutil


class AutonomousRecoverySystem:
    def __init__(self):
        self.workspace = Path('/home/stephane/GitHub/PaniniFS-Research')
        self.recovery_dir = self.workspace / 'autonomous_recovery'
        self.recovery_dir.mkdir(exist_ok=True)
        
        # Fichiers de persistance
        self.state_file = self.recovery_dir / 'autonomous_state.json'
        self.process_registry = self.recovery_dir / 'active_processes.json'
        self.recovery_log = self.recovery_dir / 'recovery.log'
        
        # Configuration
        self.check_interval = 30  # Vérification toutes les 30s
        self.max_restarts = 5
        self.processes_to_monitor = [
            'autonomous_corpus_processor.py',
            'autonomous_dashboard.py', 
            'autonomous_dhatu_optimizer.py'
        ]
        
        self.log("🛡️ Système Auto-Recovery initialisé")
    
    def log(self, message):
        """Logging persistant"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        with open(self.recovery_log, 'a') as f:
            f.write(log_message + '\n')
    
    def save_state(self, state_data):
        """Sauvegarde état pour recovery"""
        try:
            state_data['timestamp'] = datetime.now().isoformat()
            state_data['pid'] = os.getpid()
            
            with open(self.state_file, 'w') as f:
                json.dump(state_data, f, indent=2)
                
            self.log(f"💾 État sauvegardé: {len(state_data)} éléments")
            
        except Exception as e:
            self.log(f"❌ Erreur sauvegarde état: {e}")
    
    def load_state(self):
        """Charge état précédent"""
        try:
            if self.state_file.exists():
                with open(self.state_file) as f:
                    state = json.load(f)
                
                self.log(f"📂 État chargé: {state.get('timestamp', 'N/A')}")
                return state
            else:
                self.log("ℹ️ Aucun état précédent trouvé")
                return {}
                
        except Exception as e:
            self.log(f"❌ Erreur chargement état: {e}")
            return {}
    
    def register_process(self, script_name, pid, command):
        """Enregistre processus pour monitoring"""
        try:
            processes = self.get_registered_processes()
            
            processes[script_name] = {
                'pid': pid,
                'command': command,
                'started_at': datetime.now().isoformat(),
                'restart_count': processes.get(script_name, {}).get('restart_count', 0)
            }
            
            with open(self.process_registry, 'w') as f:
                json.dump(processes, f, indent=2)
            
            self.log(f"📋 Processus enregistré: {script_name} (PID: {pid})")
            
        except Exception as e:
            self.log(f"❌ Erreur enregistrement processus: {e}")
    
    def get_registered_processes(self):
        """Récupère processus enregistrés"""
        try:
            if self.process_registry.exists():
                with open(self.process_registry) as f:
                    return json.load(f)
            return {}
        except:
            return {}
    
    def is_process_running(self, pid):
        """Vérifie si processus fonctionne"""
        try:
            return psutil.pid_exists(pid)
        except:
            return False
    
    def restart_process(self, script_name, command):
        """Redémarre processus crashé"""
        try:
            self.log(f"🔄 Redémarrage de {script_name}...")
            
            # Lancement nouveau processus
            full_command = f"cd {self.workspace} && python3 {command}"
            process = subprocess.Popen(
                full_command,
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # Mise à jour registre
            processes = self.get_registered_processes()
            if script_name in processes:
                processes[script_name]['restart_count'] += 1
            else:
                processes[script_name] = {'restart_count': 1}
            
            processes[script_name].update({
                'pid': process.pid,
                'command': command,
                'restarted_at': datetime.now().isoformat()
            })
            
            with open(self.process_registry, 'w') as f:
                json.dump(processes, f, indent=2)
            
            self.log(f"✅ {script_name} redémarré (PID: {process.pid})")
            return True
            
        except Exception as e:
            self.log(f"❌ Échec redémarrage {script_name}: {e}")
            return False
    
    def monitor_processes(self):
        """Surveillance continue des processus"""
        self.log("👁️ Démarrage surveillance processus...")
        
        while True:
            try:
                processes = self.get_registered_processes()
                
                for script_name, process_info in processes.items():
                    pid = process_info.get('pid')
                    command = process_info.get('command', script_name)
                    restart_count = process_info.get('restart_count', 0)
                    
                    if not self.is_process_running(pid):
                        self.log(f"💀 Processus mort détecté: {script_name} (PID: {pid})")
                        
                        if restart_count < self.max_restarts:
                            self.restart_process(script_name, command)
                        else:
                            self.log(f"⚠️ Limite redémarrages atteinte pour {script_name}")
                
                # Vérification processus critiques
                self.ensure_critical_processes()
                
                time.sleep(self.check_interval)
                
            except Exception as e:
                self.log(f"❌ Erreur surveillance: {e}")
                time.sleep(60)
    
    def ensure_critical_processes(self):
        """S'assure que les processus critiques fonctionnent"""
        running_scripts = []
        
        # Vérifie processus Python actifs
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] == 'python3':
                    cmdline = ' '.join(proc.info['cmdline'])
                    for script in self.processes_to_monitor:
                        if script in cmdline:
                            running_scripts.append(script)
            except:
                continue
        
        # Redémarre processus manquants
        for script in self.processes_to_monitor:
            if script not in running_scripts:
                processes = self.get_registered_processes()
                if script not in processes or processes[script].get('restart_count', 0) < self.max_restarts:
                    self.log(f"🚨 Processus critique manquant: {script}")
                    self.restart_process(script, script)
    
    def create_startup_script(self):
        """Crée script de démarrage automatique"""
        startup_script = self.recovery_dir / 'auto_startup.sh'
        
        script_content = f'''#!/bin/bash
# Script de démarrage automatique - Autonomie PaniniFS
cd {self.workspace}

echo "🚀 Démarrage automatique autonomie PaniniFS - $(date)"

# Activation environnement virtuel
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    echo "✅ Environnement virtuel activé"
fi

# Démarrage système recovery
python3 autonomous_recovery_system.py &
echo "🛡️ Système recovery démarré"

# Démarrage processus critiques
python3 autonomous_corpus_processor.py &
echo "📊 Processeur corpus démarré"

python3 autonomous_dashboard.py &
echo "🖥️ Dashboard démarré"

python3 autonomous_dhatu_optimizer.py &
echo "⚡ Optimiseur dhātu démarré"

echo "🎯 Tous les processus autonomes démarrés"
echo "📍 Dashboard: http://localhost:8090"
echo "📋 Logs: {self.recovery_dir}/recovery.log"
'''
        
        startup_script.write_text(script_content)
        startup_script.chmod(0o755)
        
        self.log(f"📜 Script startup créé: {startup_script}")
    
    def setup_auto_recovery(self):
        """Configuration complète auto-recovery"""
        self.log("⚙️ Configuration auto-recovery...")
        
        # État initial
        initial_state = {
            'recovery_system_active': True,
            'monitoring_enabled': True,
            'startup_timestamp': datetime.now().isoformat(),
            'workspace': str(self.workspace),
            'processes_monitored': self.processes_to_monitor
        }
        
        self.save_state(initial_state)
        
        # Script de démarrage
        self.create_startup_script()
        
        # Enregistrement signal handlers
        signal.signal(signal.SIGTERM, self.graceful_shutdown)
        signal.signal(signal.SIGINT, self.graceful_shutdown)
        
        self.log("✅ Auto-recovery configuré")
    
    def graceful_shutdown(self, signum, frame):
        """Arrêt propre avec sauvegarde"""
        self.log(f"🛑 Arrêt gracieux (signal {signum})")
        
        # Sauvegarde état final
        shutdown_state = {
            'shutdown_timestamp': datetime.now().isoformat(),
            'shutdown_reason': f'Signal {signum}',
            'processes_registered': len(self.get_registered_processes())
        }
        
        self.save_state(shutdown_state)
        
        self.log("💾 État final sauvegardé")
        sys.exit(0)
    
    def run_recovery_system(self):
        """Lance système recovery complet"""
        self.log("🚀 DÉMARRAGE SYSTÈME AUTO-RECOVERY")
        
        # Configuration
        self.setup_auto_recovery()
        
        # Chargement état précédent
        previous_state = self.load_state()
        if previous_state:
            self.log(f"🔄 Reprise depuis: {previous_state.get('timestamp', 'N/A')}")
        
        # Surveillance continue
        try:
            self.monitor_processes()
        except KeyboardInterrupt:
            self.graceful_shutdown(signal.SIGINT, None)

def main():
    recovery_system = AutonomousRecoverySystem()
    
    try:
        recovery_system.run_recovery_system()
        return 0
    except Exception as e:
        recovery_system.log(f"💥 ERREUR CRITIQUE RECOVERY: {e}")
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)