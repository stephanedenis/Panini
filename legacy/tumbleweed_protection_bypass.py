#!/usr/bin/env python3
"""
Script de contournement protections Tumbleweed
Ajuste automatiquement les paramètres pour éviter les kills OS
"""

import os
import sys
import time
import psutil
import signal


class TumbleweedBypass:
    def __init__(self):
        self.max_cpu_percent = 75  # Limite CPU à 75%
        self.max_memory_percent = 80  # Limite RAM à 80%
        self.check_interval = 5  # Vérification toutes les 5s
        
        # Ajustement priorité processus
        try:
            os.nice(5)  # Priorité plus basse
            print("✅ Priorité processus ajustée")
        except:
            print("⚠️ Impossible ajuster priorité")
    
    def monitor_and_throttle(self):
        """Surveillance et limitation automatique"""
        while True:
            try:
                # Métriques système
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                
                # Limitation CPU
                if cpu_percent > self.max_cpu_percent:
                    print(f"🛑 CPU élevé ({cpu_percent:.1f}%) - throttling")
                    time.sleep(2)  # Pause forcée
                
                # Limitation mémoire
                if memory.percent > self.max_memory_percent:
                    print(f"🛑 RAM élevée ({memory.percent:.1f}%) - limitation")
                    # Forcer garbage collection
                    import gc
                    gc.collect()
                
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                print("🛑 Arrêt surveillance")
                break
            except Exception as e:
                print(f"❌ Erreur surveillance: {e}")
                time.sleep(10)


if __name__ == '__main__':
    bypass = TumbleweedBypass()
    bypass.monitor_and_throttle()
