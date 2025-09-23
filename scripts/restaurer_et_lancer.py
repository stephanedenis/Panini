#!/usr/bin/env python3
"""
Restaurateur et Lanceur Système PaniniFS
Restaure les corpus manquants et lance le système complet
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def restaurer_corpus():
    """Restaure les corpus manquants"""
    logger.info("🔧 Restauration des corpus...")
    
    # 1. Corpus multilingue développemental
    source_multilingue = "corpus_multilingue_dev/corpus_multilingue_developpemental.json"
    target_multilingue = "corpus_multilingue_dev.json"
    
    if Path(source_multilingue).exists():
        logger.info(f"📋 Copie {source_multilingue} → {target_multilingue}")
        shutil.copy2(source_multilingue, target_multilingue)
        logger.info("✅ Corpus multilingue restauré")
    else:
        logger.warning(f"⚠️ Source manquante: {source_multilingue}")
    
    # 2. Corpus scientifique
    source_scientifique = "tech/corpus_simple/corpus.json"
    target_scientifique = "corpus_scientifique.json"
    
    if Path(source_scientifique).exists():
        logger.info(f"📋 Copie {source_scientifique} → {target_scientifique}")
        shutil.copy2(source_scientifique, target_scientifique)
        logger.info("✅ Corpus scientifique restauré")
    else:
        logger.warning(f"⚠️ Source manquante: {source_scientifique}")
    
    # 3. Créer corpus unifié s'il n'existe pas
    corpus_unifie = "corpus_complet_unifie.json"
    if not Path(corpus_unifie).exists():
        logger.info("🔄 Création corpus unifié...")
        
        corpus_complet = {
            "metadata": {
                "creation": "2025-09-21",
                "description": "Corpus unifié pour recherche PaniniFS",
                "sources": ["scientifique", "multilingue", "dhatu"]
            },
            "documents": []
        }
        
        # Charger corpus multilingue
        if Path(target_multilingue).exists():
            try:
                with open(target_multilingue, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    docs = data.get('documents', [])
                    corpus_complet['documents'].extend(docs)
                    logger.info(f"📚 Ajouté {len(docs)} docs multilingues")
            except Exception as e:
                logger.warning(f"⚠️ Erreur lecture multilingue: {e}")
        
        # Charger corpus scientifique
        if Path(target_scientifique).exists():
            try:
                with open(target_scientifique, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    docs = data.get('documents', [])
                    corpus_complet['documents'].extend(docs)
                    logger.info(f"📚 Ajouté {len(docs)} docs scientifiques")
            except Exception as e:
                logger.warning(f"⚠️ Erreur lecture scientifique: {e}")
        
        # Sauvegarder corpus unifié
        with open(corpus_unifie, 'w', encoding='utf-8') as f:
            json.dump(corpus_complet, f, indent=2, ensure_ascii=False)
        
        total_docs = len(corpus_complet['documents'])
        logger.info(f"✅ Corpus unifié créé: {total_docs} documents")

def verifier_corpus():
    """Vérifie l'état des corpus"""
    logger.info("🔍 Vérification corpus...")
    
    corpus_files = [
        "corpus_multilingue_dev.json",
        "corpus_scientifique.json", 
        "corpus_complet_unifie.json",
        "panini/references/references_database.json"
    ]
    
    for corpus_file in corpus_files:
        if Path(corpus_file).exists():
            try:
                with open(corpus_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if 'documents' in data:
                    count = len(data['documents'])
                elif 'references' in data:
                    count = len(data['references'])
                else:
                    count = len(data)
                
                size_mb = Path(corpus_file).stat().st_size / (1024 * 1024)
                logger.info(f"✅ {corpus_file}: {count} éléments ({size_mb:.1f} Mo)")
                
            except Exception as e:
                logger.warning(f"⚠️ Erreur lecture {corpus_file}: {e}")
        else:
            logger.warning(f"❌ Manquant: {corpus_file}")

def lancer_systeme():
    """Lance le système complet"""
    logger.info("🚀 Lancement système PaniniFS...")
    
    # Utiliser environnement virtuel si disponible
    venv_python = Path('.venv/bin/python')
    if venv_python.exists():
        python_cmd = str(venv_python)
        logger.info("✅ Utilisation environnement virtuel")
    else:
        python_cmd = 'python3'
        logger.info("⚠️ Utilisation Python système")
    
    try:
        # Lancer gestionnaire arrière-plan
        cmd = [python_cmd, 'gestionnaire_arriere_plan.py']
        
        logger.info(f"📡 Commande: {' '.join(cmd)}")
        
        # Démarrer en arrière-plan
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Sauvegarder PID
        with open('systeme_panini_pid.txt', 'w') as f:
            f.write(str(process.pid))
        
        logger.info(f"✅ Système démarré (PID: {process.pid})")
        logger.info("💡 Utilisez 'python3 verificateur_statut_systemes.py' pour voir la progression")
        
        return process
        
    except Exception as e:
        logger.error(f"❌ Erreur lancement: {e}")
        return None

def afficher_instructions():
    """Affiche les instructions post-lancement"""
    print("\n" + "="*60)
    print("🎯 SYSTÈME PANINIFS RESEARCH LANCÉ")
    print("="*60)
    print("📊 Pour voir le statut: python3 verificateur_statut_systemes.py")
    print("📋 Pour voir les logs: cat gestionnaire_arriere_plan.log")
    print("🛑 Pour arrêter: kill $(cat systeme_panini_pid.txt)")
    print("📁 Résultats dans: pipeline_iteratif_resultats/")
    print("\n🔄 PROGRESSION AUTOMATIQUE:")
    print("  1. Corpus préscolaire (2-5 ans) → modèle de base")
    print("  2. Corpus primaire (6-11 ans) → raffinement")
    print("  3. Corpus secondaire (12-17 ans) → complexification")
    print("  4. Corpus universitaire (18-25 ans) → spécialisation")
    print("  5. Corpus expert (25+ ans) → optimisation finale")
    print("="*60)

def main():
    """Point d'entrée principal"""
    print("🔧 RESTAURATEUR ET LANCEUR PANINIFS")
    print("=" * 40)
    
    try:
        # 1. Restaurer corpus
        restaurer_corpus()
        
        # 2. Vérifier corpus
        verifier_corpus()
        
        # 3. Lancer système
        process = lancer_systeme()
        
        if process:
            # 4. Afficher instructions
            afficher_instructions()
            
            # Vérifier que le système démarre bien
            import time
            time.sleep(3)
            
            if process.poll() is None:
                logger.info("✅ Système en cours d'exécution")
            else:
                logger.warning("⚠️ Système s'est arrêté rapidement")
                # Afficher erreurs
                try:
                    output, _ = process.communicate(timeout=1)
                    logger.error(f"Sortie: {output}")
                except:
                    pass
        
    except KeyboardInterrupt:
        logger.info("⏹️ Arrêt demandé par utilisateur")
    except Exception as e:
        logger.error(f"❌ Erreur fatale: {e}")

if __name__ == "__main__":
    main()