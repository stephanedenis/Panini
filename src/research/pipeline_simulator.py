#!/usr/bin/env python3
"""
Simulateur Pipeline PaniniFS - Pour démonstration du dashboard
Simule un traitement de corpus avec progression réaliste
"""

import time
import json
import random
import threading
from datetime import datetime

class PipelineSimulator:
    def __init__(self):
        self.phases = [
            {"name": "Initialisation environnement", "duration": 10, "progress": 0},
            {"name": "Génération corpus synthétique", "duration": 30, "progress": 0},
            {"name": "Traitement atomique massif", "duration": 60, "progress": 0},
            {"name": "Synthèse moléculaire", "duration": 45, "progress": 0},
            {"name": "Validation finale", "duration": 20, "progress": 0}
        ]
        self.current_phase = 0
        self.total_elements = 1000000
        self.processed_elements = 0
        self.start_time = datetime.now()
        self.running = True
        
    def log_progress(self, message):
        timestamp = datetime.now().strftime('[%H:%M:%S]')
        print(f"{timestamp} {message}")
        
    def simulate_processing(self):
        """Simule le traitement avec progression réaliste"""
        self.log_progress("🚀 SIMULATEUR PIPELINE PANINI DÉMARRÉ")
        self.log_progress("=" * 50)
        self.log_progress(f"📊 Corpus cible: {self.total_elements:,} éléments")
        self.log_progress(f"🎮 GPU: RX 480 (2304 shaders)")
        self.log_progress(f"🖥️ CPU: 16 cores, 64GB RAM")
        self.log_progress("=" * 50)
        
        for phase_idx, phase in enumerate(self.phases):
            if not self.running:
                break
                
            self.current_phase = phase_idx
            self.log_progress(f"📋 Phase {phase_idx + 1}: {phase['name']}")
            
            # Simulation de progression par étapes
            steps = 20  # 20 étapes par phase
            step_duration = phase["duration"] / steps
            elements_per_step = self.total_elements // (len(self.phases) * steps)
            
            for step in range(steps):
                if not self.running:
                    break
                    
                # Simulation de travail avec variations réalistes
                time.sleep(step_duration * random.uniform(0.8, 1.2))
                
                # Mise à jour de la progression
                phase["progress"] = (step + 1) / steps * 100
                self.processed_elements += elements_per_step
                
                # Log périodique de progression
                if step % 5 == 0 or step == steps - 1:
                    rate = random.randint(50000, 95000)  # Taux de traitement simulé
                    self.log_progress(
                        f"📊 {phase['name']}: {phase['progress']:.1f}% | "
                        f"{self.processed_elements:,}/{self.total_elements:,} | "
                        f"{rate:,} éléments/sec"
                    )
                
                # Simulation d'activité CPU/mémoire variable
                if random.random() < 0.3:  # 30% de chance d'activity burst
                    self.log_progress(f"⚡ Burst performance: CPU {random.randint(85, 98)}%, RAM {random.randint(12, 28)}GB")
            
            self.log_progress(f"✅ Phase {phase_idx + 1} terminée: {phase['name']}")
            
        # Rapport final
        if self.running:
            duration = (datetime.now() - self.start_time).total_seconds()
            self.log_progress("=" * 50)
            self.log_progress("🏆 PIPELINE TERMINÉ AVEC SUCCÈS")
            self.log_progress(f"⏱️ Durée totale: {duration:.1f}s")
            self.log_progress(f"📊 Éléments traités: {self.processed_elements:,}")
            self.log_progress(f"🚀 Débit moyen: {self.processed_elements/duration:.0f} éléments/sec")
            self.log_progress("=" * 50)

    def get_current_status(self):
        """Retourne le statut actuel pour le dashboard"""
        if self.current_phase < len(self.phases):
            current_phase_info = self.phases[self.current_phase]
            overall_progress = ((self.current_phase + current_phase_info["progress"]/100) / len(self.phases)) * 100
        else:
            overall_progress = 100.0
            current_phase_info = {"name": "Terminé", "progress": 100}
            
        return {
            "phase": current_phase_info["name"],
            "phase_progress": current_phase_info["progress"],
            "overall_progress": overall_progress,
            "elements_processed": self.processed_elements,
            "total_elements": self.total_elements,
            "phase_number": self.current_phase + 1,
            "total_phases": len(self.phases)
        }

    def stop(self):
        """Arrête la simulation"""
        self.running = False
        self.log_progress("🛑 Simulation arrêtée")

def main():
    """Fonction principale"""
    simulator = PipelineSimulator()
    
    try:
        # Démarrage de la simulation dans un thread séparé
        sim_thread = threading.Thread(target=simulator.simulate_processing)
        sim_thread.daemon = True
        sim_thread.start()
        
        # Boucle principale pour maintenir le processus actif
        while sim_thread.is_alive():
            time.sleep(1)
            
    except KeyboardInterrupt:
        simulator.stop()
        print("\n🛑 Simulation interrompue par l'utilisateur")

if __name__ == "__main__":
    main()