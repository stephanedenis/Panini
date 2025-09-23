#!/usr/bin/env python3
"""
Test de Stress Protégé - Vérifie le système de protection
"""

import time
import multiprocessing
import numpy as np
from tumbleweed_process_protector import protect_function


@protect_function
def stress_cpu_memory():
    """Test de stress CPU + mémoire avec protection"""
    print("🔥 DÉBUT TEST STRESS PROTÉGÉ")
    print("=" * 40)
    
    # Test progressif
    for phase in range(1, 6):
        print(f"\n📈 Phase {phase}/5 - Intensité croissante")
        
        # Charge CPU progressive
        cpu_load = phase * 2
        print(f"🔄 Lancement {cpu_load} processus CPU")
        
        processes = []
        for i in range(cpu_load):
            p = multiprocessing.Process(target=cpu_intensive_task, args=(5,))
            p.start()
            processes.append(p)
        
        # Charge mémoire progressive
        memory_size = phase * 50  # MB
        print(f"💾 Allocation {memory_size}MB de mémoire")
        
        try:
            # Allocation mémoire
            big_array = np.random.random((memory_size * 1024 * 256,))  # 1MB per 1024*256 floats
            
            # Calculs sur l'array
            for i in range(10):
                result = np.mean(big_array) * np.std(big_array)
                print(f"  📊 Calcul {i+1}/10: {result:.2e}")
                time.sleep(1)
            
            del big_array  # Libération mémoire
            
        except MemoryError:
            print("❌ Limite mémoire atteinte")
        
        # Attendre fin processus CPU
        for p in processes:
            p.join(timeout=2)
            if p.is_alive():
                p.terminate()
        
        print(f"✅ Phase {phase} terminée")
        time.sleep(3)  # Pause entre phases
    
    print("\n🏁 TEST STRESS TERMINÉ")


def cpu_intensive_task(duration):
    """Tâche intensive CPU"""
    start_time = time.time()
    counter = 0
    
    while time.time() - start_time < duration:
        # Calculs inutiles pour charger CPU
        counter += sum(range(1000))
        
        # Vérification périodique
        if counter % 10000 == 0:
            elapsed = time.time() - start_time
            if elapsed > duration:
                break


def main():
    print("🧪 TEST SYSTÈME PROTECTION TUMBLEWEED")
    print("=" * 45)
    print("Ce test va progressivement augmenter la charge")
    print("pour vérifier que la protection fonctionne.")
    print("Surveiller les messages de throttling.")
    print("=" * 45)
    
    try:
        stress_cpu_memory()
    except KeyboardInterrupt:
        print("\n🛑 Test interrompu")
    except Exception as e:
        print(f"\n❌ Erreur test: {e}")


if __name__ == '__main__':
    main()