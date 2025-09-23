#!/usr/bin/env python3
"""
Lance le système événementiel uniquement
"""

import sys
from pathlib import Path
import time

# Ajoute le dossier src au path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from core.event_system import EventCoordinator, EventProcessor, EventType, SystemEvent
from core.system_base import setup_logging


def create_corpus_processor():
    """Crée le processeur de corpus"""
    processor = EventProcessor("corpus_processor", [1, 2])
    
    def handle_corpus_event(event):
        # Simulation de traitement corpus
        print(f"🧠 10 hypothèses générées depuis corpus")
        if event.data.get('total_files', 0) > 10:
            print(f"📊 Seuil atteint: {event.data}")
    
    processor.register_handler(EventType.CORPUS_DATA_READY, handle_corpus_event)
    return processor


def create_research_processor():
    """Crée le processeur de recherche"""
    processor = EventProcessor("research_processor", [3, 4])
    
    def handle_research_event(event):
        print(f"🔬 Recherche hypothèse: {event.data.get('hypothesis', 'inconnue')}")
    
    processor.register_handler(EventType.RESEARCH_HYPOTHESIS_GENERATED, handle_research_event)
    return processor


def create_optimization_processor():
    """Crée le processeur d'optimisation"""
    processor = EventProcessor("optimization_processor", [5, 6, 7])
    
    def handle_optimization_event(event):
        print(f"⚡ Optimisation: {event.data.get('target', 'générale')}")
    
    processor.register_handler(EventType.OPTIMIZATION_REQUEST, handle_optimization_event)
    return processor


def create_validation_processor():
    """Crée le processeur de validation"""
    processor = EventProcessor("validation_processor", [8])
    
    def handle_validation_event(event):
        print(f"✅ Validation: {event.data.get('result', 'en cours')}")
    
    processor.register_handler(EventType.VALIDATION_REQUIRED, handle_validation_event)
    return processor


def main():
    """Lance le système événementiel"""
    
    print("🚀 SYSTÈME ÉVÉNEMENTIEL AVEC AFFINITÉ CPU DÉMARRÉ")
    print("=" * 60)
    print("🔧 Architecture: Événements + Affinité CPU exclusive")
    print("⚡ Processeurs: corpus(2), research(2), optimization(3), validation(1)")
    print("📊 Métriques temps réel disponibles")
    print("🛑 Ctrl+C pour arrêter")
    
    # Configuration du logging
    logger = setup_logging()
    
    # Création du coordinateur
    coordinator = EventCoordinator()
    
    # Ajout des processeurs
    coordinator.add_processor(create_corpus_processor())
    coordinator.add_processor(create_research_processor())
    coordinator.add_processor(create_optimization_processor())
    coordinator.add_processor(create_validation_processor())
    
    # Démarrage du système
    coordinator.start()
    
    try:
        # Génération d'événements de test
        event_count = 0
        while True:
            # Événement corpus périodique
            corpus_event = SystemEvent(
                EventType.CORPUS_DATA_READY,
                {'total_files': 12, 'threshold': 10}
            )
            coordinator.send_event("corpus_processor", corpus_event)
            event_count += 1
            
            # Événement recherche occasionnel
            if event_count % 5 == 0:
                research_event = SystemEvent(
                    EventType.RESEARCH_HYPOTHESIS_GENERATED,
                    {'hypothesis': f'H{event_count}', 'confidence': 0.85}
                )
                coordinator.send_event("research_processor", research_event)
            
            time.sleep(2)  # Génère des événements toutes les 2 secondes
            
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du système événementiel...")
        coordinator.stop()
        print("✅ Système arrêté proprement")


if __name__ == "__main__":
    main()