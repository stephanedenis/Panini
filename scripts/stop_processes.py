#!/usr/bin/env python3

import psutil

print("🛑 ARRÊT DES PROCESSUS AUTONOMES")

# Processus à arrêter
targets = [
    'systeme_evenementiel_cpu.py',
    'dashboard_evenementiel.py', 
    'dashboard_realtime_avance.py',
    'moniteur_systeme_avance.py'
]

stopped = 0

for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
        cmdline = ' '.join(proc.info['cmdline'] or [])
        
        for target in targets:
            if target in cmdline:
                print(f"🔴 Arrêt {target} (PID {proc.info['pid']})")
                proc.terminate()
                stopped += 1
                break
                
    except:
        continue

print(f"✅ {stopped} processus arrêtés")
print("💡 Workspace prêt pour réorganisation")