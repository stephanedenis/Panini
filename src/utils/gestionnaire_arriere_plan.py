#!/usr/bin/env python3
"""
Gestionnaire Arrière-Plan PaniniFS
Lance et gère tous les processus de recherche en arrière-plan
avec monitoring automatique et redémarrage si nécessaire
"""

import asyncio
import subprocess
import signal
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import psutil
import os

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gestionnaire_arriere_plan.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class GestionnaireArriereplan:
    def __init__(self):
        self.processus_actifs = {}
        self.processus_config = [
            {
                'nom': 'orchestrateur_pipeline',
                'script': 'orchestrateur_pipeline_iteratif.py',
                'description': 'Pipeline itératif par niveaux de complexité',
                'priorite': 1,
                'auto_restart': True,
                'intervalle_check': 300,  # 5 minutes au lieu de 30s
                'max_restarts_per_hour': 6  # Maximum 6 redémarrages par heure
            },
            {
                'nom': 'collecteur_corpus',
                'script': 'collecteur_corpus_prescolaire.py',
                'description': 'Collection corpus préscolaire',
                'priorite': 2,
                'auto_restart': True,
                'intervalle_check': 300,  # 5 minutes
                'max_restarts_per_hour': 12
            },
            {
                'nom': 'optimiseur_dhatu',
                'script': 'autonomous_dhatu_optimizer.py',
                'description': 'Optimisation dhatu en continu',
                'priorite': 3,
                'auto_restart': False,  # Désactiver auto-restart pour éviter surcharge
                'intervalle_check': 300,
                'max_restarts_per_hour': 3
            },
            {
                'nom': 'moniteur_pipeline',
                'script': 'moniteur_progression_pipeline.py',
                'description': 'Monitoring progression temps réel',
                'priorite': 4,
                'auto_restart': True,
                'intervalle_check': 120,  # 2 minutes
                'max_restarts_per_hour': 30
            }
        ]
        
        self.etat_systeme = {
            'demarrage': datetime.now().isoformat(),
            'processus_actifs': 0,
            'derniere_verification': None,
            'erreurs_totales': 0,
            'redemarrages_totaux': 0
        }
        
        # Historique redémarrages pour limitation
        self.restart_history = {}
        
        self.running = False
        self.chemin_logs = Path('logs_arriere_plan')
        self.chemin_logs.mkdir(exist_ok=True)

    async def demarrer_tous_processus(self):
        """Démarre tous les processus en arrière-plan"""
        logger.info("🚀 Démarrage gestionnaire arrière-plan PaniniFS")
        self.running = True
        
        # Créer scripts manquants si nécessaire
        await self.creer_scripts_manquants()
        
        # Démarrer processus par ordre de priorité
        processus_tries = sorted(self.processus_config, key=lambda x: x['priorite'])
        
        for config in processus_tries:
            await self.demarrer_processus(config)
            await asyncio.sleep(2)  # Délai entre démarrages
        
        # Boucle de monitoring
        await self.boucle_monitoring()

    async def creer_scripts_manquants(self):
        """Crée les scripts manquants pour le pipeline complet"""
        scripts_a_creer = {
            'collecteur_corpus_prescolaire.py': await self.generer_collecteur_prescolaire(),
            'moniteur_progression_pipeline.py': await self.generer_moniteur_progression()
        }
        
        for nom_script, contenu in scripts_a_creer.items():
            if not Path(nom_script).exists():
                logger.info(f"📝 Création script manquant: {nom_script}")
                with open(nom_script, 'w', encoding='utf-8') as f:
                    f.write(contenu)
                os.chmod(nom_script, 0o755)  # Rendre exécutable

    async def generer_collecteur_prescolaire(self) -> str:
        """Génère le script de collection corpus préscolaire"""
        return '''#!/usr/bin/env python3
"""
Collecteur Corpus Préscolaire
Collection spécialisée pour enfants 2-5 ans
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def collecter_corpus_prescolaire():
    """Collecte corpus préscolaire en continu"""
    logger.info("🍼 Démarrage collection corpus préscolaire")
    
    corpus_prescolaire = {
        'metadata': {
            'type': 'prescolaire',
            'age_range': '2-5',
            'creation': datetime.now().isoformat()
        },
        'documents': []
    }
    
    # Chercher dans corpus existant
    try:
        if Path('corpus_multilingue_dev.json').exists():
            with open('corpus_multilingue_dev.json', 'r', encoding='utf-8') as f:
                corpus_complet = json.load(f)
            
            # Filtrer documents préscolaires
            mots_cles = ['child', 'toddler', 'preschool', 'infant', 'enfant', 'préscolaire']
            
            for doc in corpus_complet.get('documents', []):
                titre = doc.get('title', '').lower()
                resume = doc.get('abstract', '').lower()
                
                if any(mot in titre or mot in resume for mot in mots_cles):
                    corpus_prescolaire['documents'].append(doc)
        
        # Sauvegarder corpus préscolaire
        with open('corpus_prescolaire.json', 'w', encoding='utf-8') as f:
            json.dump(corpus_prescolaire, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📚 Corpus préscolaire: {len(corpus_prescolaire['documents'])} documents")
        
    except Exception as e:
        logger.error(f"❌ Erreur collection: {e}")
    
    # Attendre avant prochaine collection
    await asyncio.sleep(300)  # 5 minutes

async def main():
    while True:
        await collecter_corpus_prescolaire()

if __name__ == "__main__":
    asyncio.run(main())
'''

    async def generer_moniteur_progression(self) -> str:
        """Génère le script de monitoring progression"""
        return '''#!/usr/bin/env python3
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
'''

    async def demarrer_processus(self, config: Dict) -> bool:
        """Démarre un processus spécifique"""
        nom = config['nom']
        script = config['script']
        
        # Vérifier si script existe
        if not Path(script).exists():
            logger.warning(f"⚠️ Script manquant: {script}")
            return False
        
        try:
            # Démarrer processus
            cmd = ['python3', script]
            
            # Rediriger logs vers fichier
            log_file = self.chemin_logs / f'{nom}.log'
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                cwd=Path.cwd()
            )
            
            # Enregistrer processus
            self.processus_actifs[nom] = {
                'process': process,
                'config': config,
                'demarrage': datetime.now(),
                'redemarrages': 0,
                'derniere_verification': None
            }
            
            logger.info(f"✅ Processus démarré: {nom} (PID: {process.pid})")
            self.etat_systeme['processus_actifs'] += 1
            
            # Capturer logs en arrière-plan
            asyncio.create_task(self.capturer_logs_processus(nom, process))
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur démarrage {nom}: {e}")
            self.etat_systeme['erreurs_totales'] += 1
            return False

    async def capturer_logs_processus(self, nom: str, process):
        """Capture les logs d'un processus"""
        log_file = self.chemin_logs / f'{nom}.log'
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"\\n=== Démarrage {datetime.now()} ===\\n")
                
                async for line in process.stdout:
                    line_str = line.decode('utf-8', errors='ignore')
                    f.write(line_str)
                    f.flush()
                    
        except Exception as e:
            logger.warning(f"⚠️ Erreur capture logs {nom}: {e}")

    async def boucle_monitoring(self):
        """Boucle principale de monitoring"""
        logger.info("🔍 Démarrage boucle monitoring")
        
        while self.running:
            try:
                await self.verifier_processus()
                await self.sauvegarder_etat()
                await asyncio.sleep(10)  # Vérification toutes les 10s
                
            except Exception as e:
                logger.error(f"❌ Erreur monitoring: {e}")
                await asyncio.sleep(30)

    async def verifier_processus(self):
        """Vérifie l'état de tous les processus"""
        self.etat_systeme['derniere_verification'] = datetime.now().isoformat()
        
        processus_a_redemarrer = []
        
        for nom, info in list(self.processus_actifs.items()):
            process = info['process']
            config = info['config']
            
            # Vérifier si processus est encore actif
            if process.returncode is not None:
                logger.warning(f"⚠️ Processus {nom} terminé (code: {process.returncode})")
                
                if config.get('auto_restart', False):
                    # Vérifier limitations de redémarrage
                    if self.peut_redemarrer(nom, config):
                        processus_a_redemarrer.append((nom, config))
                    else:
                        logger.warning(f"⏸️ Redémarrage {nom} limité - trop de tentatives récentes")
                
                # Retirer de la liste des actifs
                del self.processus_actifs[nom]
                self.etat_systeme['processus_actifs'] -= 1
        
        # Redémarrer processus si nécessaire
        for nom, config in processus_a_redemarrer:
            logger.info(f"🔄 Redémarrage processus: {nom}")
            await self.demarrer_processus(config)
            self.etat_systeme['redemarrages_totaux'] += 1
            
            # Enregistrer redémarrage
            self.enregistrer_redemarrage(nom)

    def peut_redemarrer(self, nom: str, config: Dict) -> bool:
        """Vérifie si un processus peut être redémarré selon les limites"""
        max_restarts = config.get('max_restarts_per_hour', 60)
        now = time.time()
        
        # Nettoyer historique > 1 heure
        if nom in self.restart_history:
            self.restart_history[nom] = [
                timestamp for timestamp in self.restart_history[nom] 
                if now - timestamp < 3600  # 1 heure
            ]
        
        # Vérifier limite
        restarts_last_hour = len(self.restart_history.get(nom, []))
        return restarts_last_hour < max_restarts
    
    def enregistrer_redemarrage(self, nom: str):
        """Enregistre un redémarrage dans l'historique"""
        if nom not in self.restart_history:
            self.restart_history[nom] = []
        self.restart_history[nom].append(time.time())

    async def sauvegarder_etat(self):
        """Sauvegarde l'état du gestionnaire"""
        etat_complet = {
            **self.etat_systeme,
            'timestamp': datetime.now().isoformat(),
            'processus_details': {
                nom: {
                    'demarrage': info['demarrage'].isoformat(),
                    'redemarrages': info['redemarrages'],
                    'pid': info['process'].pid,
                    'actif': info['process'].returncode is None
                }
                for nom, info in self.processus_actifs.items()
            }
        }
        
        with open('etat_gestionnaire_arriere_plan.json', 'w', encoding='utf-8') as f:
            json.dump(etat_complet, f, indent=2, ensure_ascii=False)

    async def arreter_tous_processus(self):
        """Arrête tous les processus"""
        logger.info("🛑 Arrêt de tous les processus")
        self.running = False
        
        for nom, info in self.processus_actifs.items():
            process = info['process']
            
            try:
                # Tentative d'arrêt propre
                process.terminate()
                await asyncio.wait_for(process.wait(), timeout=5)
                logger.info(f"✅ Processus {nom} arrêté proprement")
                
            except asyncio.TimeoutError:
                # Forcer l'arrêt
                process.kill()
                logger.warning(f"⚠️ Processus {nom} forcé à s'arrêter")
            
            except Exception as e:
                logger.error(f"❌ Erreur arrêt {nom}: {e}")

    def signal_handler(self, signum, frame):
        """Gestionnaire de signaux pour arrêt propre"""
        logger.info(f"📡 Signal reçu: {signum}")
        asyncio.create_task(self.arreter_tous_processus())


async def main():
    """Point d'entrée principal"""
    gestionnaire = GestionnaireArriereplan()
    
    # Gérer signaux d'arrêt
    signal.signal(signal.SIGINT, gestionnaire.signal_handler)
    signal.signal(signal.SIGTERM, gestionnaire.signal_handler)
    
    try:
        await gestionnaire.demarrer_tous_processus()
    except KeyboardInterrupt:
        logger.info("⏹️ Arrêt demandé par utilisateur")
    finally:
        await gestionnaire.arreter_tous_processus()


if __name__ == "__main__":
    asyncio.run(main())