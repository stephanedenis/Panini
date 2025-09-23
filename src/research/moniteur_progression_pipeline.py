#!/usr/bin/env python3
"""
Moniteur Progression Pipeline
Surveille et affiche progression en temps réel
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def monitorer_progression():
    """Monitore la progression du pipeline"""
    logger.info("📊 Démarrage monitoring progression")
    
    while True:
        try:
            # Lire état pipeline
            if Path('pipeline_iteratif_resultats/etat_pipeline.json').exists():
                with open('pipeline_iteratif_resultats/etat_pipeline.json', 'r') as f:
                    etat = json.load(f)
                
                niveau_actuel = etat.get('niveau_actuel', 0)
                qualite = etat.get('modele_qualite', 0.0)
                cycles = etat.get('cycles_completes', 0)
                
                # Afficher progression
                niveaux = ['préscolaire', 'primaire', 'secondaire', 'universitaire', 'expert']
                niveau_nom = niveaux[min(niveau_actuel, len(niveaux)-1)]
                
                logger.info(f"🎯 Niveau: {niveau_nom} | Qualité: {qualite:.3f} | Cycles: {cycles}")
            
            # Vérifier corpus
            corpus_files = ['corpus_prescolaire.json', 'corpus_multilingue_dev.json']
            for corpus_file in corpus_files:
                if Path(corpus_file).exists():
                    with open(corpus_file, 'r') as f:
                        data = json.load(f)
                    docs = len(data.get('documents', []))
                    logger.info(f"📚 {corpus_file}: {docs} documents")
            
        except Exception as e:
            logger.warning(f"⚠️ Erreur monitoring: {e}")
        
        await asyncio.sleep(30)  # Monitoring toutes les 30s

async def main():
    await monitorer_progression()

if __name__ == "__main__":
    asyncio.run(main())
