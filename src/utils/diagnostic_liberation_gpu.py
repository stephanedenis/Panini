#!/usr/bin/env python3
"""
Diagnostic et Libération GPU AMD
Analyse exhaustive de l'utilisation GPU et libération des ressources
"""

import subprocess
import time
import json
from datetime import datetime

class GPUDiagnosticTool:
    def __init__(self):
        self.log("🔍 Outil de Diagnostic GPU AMD initialisé")
    
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def get_gpu_processes(self):
        """Identifier tous les processus utilisant la GPU"""
        try:
            # Méthode 1: Via rocm-smi (si disponible)
            result = subprocess.run(['rocm-smi', '--showpids'], 
                                  capture_output=True, text=True, 
                                  timeout=10)
            if result.returncode == 0:
                return result.stdout
        except:
            pass
        
        # Méthode 2: Via lsof sur les devices DRM
        try:
            result = subprocess.run(['lsof', '/dev/dri/card*'], 
                                  capture_output=True, text=True,
                                  timeout=10)
            if result.returncode == 0:
                return result.stdout
        except:
            pass
        
        return "Aucun processus GPU détecté avec les méthodes standard"
    
    def kill_gpu_heavy_processes(self):
        """Arrêter les processus gourmands en GPU"""
        targets = [
            'firefox', 'chrome', 'chromium', 'electron',
            'steam', 'lutris', 'wine', 'blender',
            'davinci-resolve', 'kdenlive', 'obs',
            'xorg', 'wayland', 'kwin', 'mutter',
            'dashboard', 'panini', 'gpu'
        ]
        
        killed = []
        for target in targets:
            try:
                result = subprocess.run(['pkill', '-f', target], 
                                      capture_output=True, timeout=5)
                if result.returncode == 0:
                    killed.append(target)
                    self.log(f"🔪 Processus {target} terminé")
            except:
                pass
        
        return killed
    
    def force_gpu_reset(self):
        """Reset forcé de la GPU"""
        try:
            # Forcer le mode low power
            subprocess.run(['sudo', 'tee', '/sys/class/drm/card*/device/power_dpm_force_performance_level'], 
                          input='low', text=True, timeout=5)
            time.sleep(2)
            
            # Revenir en auto
            subprocess.run(['sudo', 'tee', '/sys/class/drm/card*/device/power_dpm_force_performance_level'], 
                          input='auto', text=True, timeout=5)
            
            self.log("🔄 Reset GPU forcé (low -> auto)")
            return True
        except Exception as e:
            self.log(f"❌ Erreur reset GPU: {e}")
            return False
    
    def check_gpu_usage(self):
        """Vérifier l'usage GPU actuel"""
        try:
            result = subprocess.run(['radeontop', '-d', '-', '-l', '1'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if lines:
                    last_line = lines[-1]
                    # Parser la ligne pour extraire l'usage GPU
                    if 'gpu' in last_line:
                        parts = last_line.split(',')
                        for part in parts:
                            if 'gpu' in part and '%' in part:
                                usage = part.split('gpu')[1].strip().replace('%', '').replace(' ', '')
                                try:
                                    return float(usage)
                                except:
                                    pass
        except Exception as e:
            self.log(f"❌ Erreur mesure GPU: {e}")
        
        return None
    
    def comprehensive_cleanup(self):
        """Nettoyage complet GPU"""
        self.log("🧹 Début du nettoyage complet GPU")
        
        # 1. Mesure initiale
        initial_usage = self.check_gpu_usage()
        if initial_usage:
            self.log(f"📊 Usage GPU initial: {initial_usage}%")
        
        # 2. Identifier processus
        self.log("🔍 Identification des processus GPU...")
        processes = self.get_gpu_processes()
        self.log(f"📋 Processus détectés:\n{processes}")
        
        # 3. Tuer processus gourmands
        self.log("🔪 Arrêt des processus gourmands...")
        killed = self.kill_gpu_heavy_processes()
        if killed:
            self.log(f"✅ Processus arrêtés: {', '.join(killed)}")
        
        # 4. Reset GPU
        self.log("🔄 Reset forcé GPU...")
        self.force_gpu_reset()
        
        # 5. Attendre stabilisation
        self.log("⏳ Attente stabilisation (5s)...")
        time.sleep(5)
        
        # 6. Mesure finale
        final_usage = self.check_gpu_usage()
        if final_usage:
            self.log(f"📊 Usage GPU final: {final_usage}%")
            if initial_usage and final_usage < initial_usage:
                improvement = initial_usage - final_usage
                self.log(f"✅ Amélioration: -{improvement:.1f}%")
            else:
                self.log("⚠️ Aucune amélioration détectée")
        
        return final_usage
    
    def emergency_gpu_suspend(self):
        """Suspension d'urgence GPU (dernière option)"""
        self.log("🚨 SUSPENSION D'URGENCE GPU")
        self.log("⚠️ Ceci peut rendre l'affichage instable!")
        
        try:
            # Suspendre tous les processus DRM
            subprocess.run(['sudo', 'pkill', '-STOP', '-f', 'drm'], timeout=5)
            time.sleep(2)
            
            # Les redémarrer
            subprocess.run(['sudo', 'pkill', '-CONT', '-f', 'drm'], timeout=5)
            
            self.log("🔄 Processus DRM redémarrés")
            return True
        except Exception as e:
            self.log(f"❌ Erreur suspension urgence: {e}")
            return False

def main():
    diagnostic = GPUDiagnosticTool()
    
    print("=" * 60)
    print("🔧 DIAGNOSTIC ET LIBÉRATION GPU AMD")
    print("=" * 60)
    
    # Nettoyage standard
    final_usage = diagnostic.comprehensive_cleanup()
    
    # Si toujours problématique, proposer suspension d'urgence
    if final_usage and final_usage > 80:
        print("\n" + "⚠️" * 20)
        print("GPU toujours très utilisée!")
        response = input("Voulez-vous tenter la suspension d'urgence? (y/N): ")
        if response.lower() == 'y':
            diagnostic.emergency_gpu_suspend()
    
    print("\n✅ Diagnostic terminé")

if __name__ == "__main__":
    main()