#!/usr/bin/env python3
"""
Orchestrateur Pipeline Itératif PaniniFS
Traitement progressif par niveaux de complexité avec optimisation cyclique

Architecture:
1. Corpus préscolaire (2-5 ans) → modèle de base
2. Corpus primaire (6-11 ans) → raffinement
3. Corpus secondaire (12-17 ans) → complexification
4. Corpus universitaire (18-25 ans) → spécialisation
5. Corpus expert (25+ ans) → optimisation finale

Chaque cycle simplifie et optimise le modèle basé sur les patterns découverts
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import subprocess
import os

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('orchestrateur_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class OrchestrateurPipelineIteratif:
    def __init__(self):
        self.niveaux_complexite = [
            {
                'nom': 'prescolaire',
                'description': 'Corpus préscolaire (2-5 ans)',
                'age_min': 2,
                'age_max': 5,
                'priorite': 1,
                'patterns_cibles': ['phonemes_base', 'structures_simples', 'repetitions']
            },
            {
                'nom': 'primaire',
                'description': 'Corpus primaire (6-11 ans)',
                'age_min': 6,
                'age_max': 11,
                'priorite': 2,
                'patterns_cibles': ['grammaire_base', 'vocabulaire_structure', 'regles_simples']
            },
            {
                'nom': 'secondaire',
                'description': 'Corpus secondaire (12-17 ans)',
                'age_min': 12,
                'age_max': 17,
                'priorite': 3,
                'patterns_cibles': ['syntaxe_complexe', 'abstractions', 'nuances_semantiques']
            },
            {
                'nom': 'universitaire',
                'description': 'Corpus universitaire (18-25 ans)',
                'age_min': 18,
                'age_max': 25,
                'priorite': 4,
                'patterns_cibles': ['concepts_avances', 'specialisation_domaines', 'argumentation']
            },
            {
                'nom': 'expert',
                'description': 'Corpus expert (25+ ans)',
                'age_min': 25,
                'age_max': 100,
                'priorite': 5,
                'patterns_cibles': ['innovations_linguistiques', 'creation_concepts', 'meta_analyse']
            }
        ]
        
        self.etat_pipeline = {
            'niveau_actuel': 0,
            'cycles_completes': 0,
            'modele_qualite': 0.0,
            'derniere_optimisation': None,
            'processus_actifs': []
        }
        
        self.chemin_resultats = Path('pipeline_iteratif_resultats')
        self.chemin_resultats.mkdir(exist_ok=True)
        
        self.running = False

    async def demarrer_orchestration(self):
        """Démarre l'orchestration complète en arrière-plan"""
        logger.info("🚀 Démarrage orchestrateur pipeline itératif")
        self.running = True
        
        # Sauvegarder état initial
        await self.sauvegarder_etat()
        
        try:
            # Boucle infinie de traitement cyclique
            while self.running:
                # Traitement séquentiel par niveaux
                for niveau in self.niveaux_complexite:
                    if not self.running:
                        break
                        
                    await self.traiter_niveau_complexite(niveau)
                    await self.optimiser_modele_cyclique()
                    
                    self.etat_pipeline['niveau_actuel'] = (self.etat_pipeline['niveau_actuel'] + 1) % len(self.niveaux_complexite)
                    
                    # Attente entre niveaux
                    await asyncio.sleep(30)
                
                if self.running:
                    self.etat_pipeline['cycles_completes'] += 1
                    await self.sauvegarder_etat()
                    
                    logger.info(f"✅ Cycle {self.etat_pipeline['cycles_completes']} terminé - Attente avant prochain cycle")
                    await self.generer_rapport_final()
                    
                    # Attente entre cycles complets (10 minutes)
                    await asyncio.sleep(600)
            
        except Exception as e:
            logger.error(f"❌ Erreur pipeline: {e}")
            await self.gerer_erreur_pipeline(e)

    async def traiter_niveau_complexite(self, niveau: Dict[str, Any]):
        """Traite un niveau de complexité spécifique"""
        nom_niveau = niveau['nom']
        logger.info(f"📚 Traitement niveau: {niveau['description']}")
        
        # 1. Collecter corpus pour ce niveau
        corpus_niveau = await self.collecter_corpus_niveau(niveau)
        
        # 2. Analyser patterns spécifiques
        patterns = await self.analyser_patterns_niveau(corpus_niveau, niveau)
        
        # 3. Intégrer au modèle existant
        modele_ameliore = await self.integrer_au_modele(patterns, niveau)
        
        # 4. Valider amélioration
        qualite_amelioration = await self.valider_amelioration(modele_ameliore)
        
        # 5. Sauvegarder résultats
        await self.sauvegarder_resultats_niveau(nom_niveau, {
            'corpus': corpus_niveau,
            'patterns': patterns,
            'modele': modele_ameliore,
            'qualite': qualite_amelioration
        })
        
        logger.info(f"✅ Niveau {nom_niveau} terminé (qualité: {qualite_amelioration:.3f})")

    async def collecter_corpus_niveau(self, niveau: Dict[str, Any]) -> Dict[str, Any]:
        """Collecte corpus spécifique à un niveau de complexité"""
        nom_niveau = niveau['nom']
        age_min = niveau['age_min']
        age_max = niveau['age_max']
        
        logger.info(f"📖 Collection corpus {nom_niveau} ({age_min}-{age_max} ans)")
        
        # Chercher dans corpus multilingue existant
        corpus_specifique = {
            'documents': [],
            'metadonnees': {
                'niveau': nom_niveau,
                'age_range': f"{age_min}-{age_max}",
                'patterns_cibles': niveau['patterns_cibles']
            }
        }
        
        # Charger corpus multilingue si disponible
        try:
            if Path('corpus_multilingue_dev.json').exists():
                with open('corpus_multilingue_dev.json', 'r', encoding='utf-8') as f:
                    corpus_complet = json.load(f)
                    
                # Filtrer par niveau de complexité
                for doc in corpus_complet.get('documents', []):
                    if self.document_correspond_niveau(doc, niveau):
                        corpus_specifique['documents'].append(doc)
        except Exception as e:
            logger.warning(f"⚠️ Erreur chargement corpus: {e}")
        
        # Si pas assez de documents, collecter plus
        if len(corpus_specifique['documents']) < 10:
            corpus_additionnel = await self.collecter_corpus_additionnel(niveau)
            corpus_specifique['documents'].extend(corpus_additionnel)
        
        logger.info(f"📊 Corpus {nom_niveau}: {len(corpus_specifique['documents'])} documents")
        return corpus_specifique

    def document_correspond_niveau(self, document: Dict[str, Any], niveau: Dict[str, Any]) -> bool:
        """Vérifie si un document correspond au niveau de complexité"""
        # Logique de filtrage basée sur métadonnées du document
        titre = document.get('title', '').lower()
        resume = document.get('abstract', '').lower()
        
        # Mots-clés par niveau
        mots_cles_niveau = {
            'prescolaire': ['child', 'toddler', 'preschool', 'early', 'infant', 'baby', 'enfant', 'préscolaire'],
            'primaire': ['elementary', 'primary', 'school', 'child', 'primaire', 'école'],
            'secondaire': ['adolescent', 'teenager', 'secondary', 'high school', 'lycée', 'collège'],
            'universitaire': ['university', 'college', 'student', 'undergraduate', 'universitaire'],
            'expert': ['expert', 'professional', 'advanced', 'specialist', 'professionnel']
        }
        
        mots_niveau = mots_cles_niveau.get(niveau['nom'], [])
        
        # Vérifier présence de mots-clés
        for mot in mots_niveau:
            if mot in titre or mot in resume:
                return True
                
        return False

    async def collecter_corpus_additionnel(self, niveau: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Collecte corpus additionnel pour un niveau si nécessaire"""
        logger.info(f"🔍 Collection additionnelle pour niveau {niveau['nom']}")
        
        # Pour le moment, retourner corpus vide
        # À implémenter: collection ciblée selon le niveau
        return []

    async def analyser_patterns_niveau(self, corpus: Dict[str, Any], niveau: Dict[str, Any]) -> Dict[str, Any]:
        """Analyse les patterns spécifiques à un niveau"""
        logger.info(f"🔬 Analyse patterns niveau {niveau['nom']}")
        
        patterns_detectes = {
            'phonemes': [],
            'structures': [],
            'complexite_score': 0.0,
            'niveau': niveau['nom']
        }
        
        documents = corpus.get('documents', [])
        if not documents:
            return patterns_detectes
        
        # Analyse basique de complexité
        total_mots = 0
        total_phrases = 0
        structures_uniques = set()
        
        for doc in documents:
            contenu = doc.get('content', '') or doc.get('abstract', '')
            if contenu:
                mots = contenu.split()
                phrases = contenu.split('.')
                
                total_mots += len(mots)
                total_phrases += len(phrases)
                
                # Détecter structures (patterns simples)
                for mot in mots[:100]:  # Limiter pour performance
                    if len(mot) > 2:
                        structures_uniques.add(mot.lower()[:3])  # Préfixes
        
        # Calculer score de complexité
        if total_phrases > 0:
            mots_par_phrase = total_mots / total_phrases
            complexite = min(1.0, (mots_par_phrase - 5) / 20)  # Normaliser
            patterns_detectes['complexite_score'] = max(0.0, complexite)
        
        patterns_detectes['structures'] = list(structures_uniques)[:100]  # Limiter
        
        logger.info(f"📈 Patterns {niveau['nom']}: {len(structures_uniques)} structures, complexité {patterns_detectes['complexite_score']:.3f}")
        return patterns_detectes

    async def integrer_au_modele(self, patterns: Dict[str, Any], niveau: Dict[str, Any]) -> Dict[str, Any]:
        """Intègre les patterns au modèle existant"""
        logger.info(f"🧠 Intégration modèle niveau {niveau['nom']}")
        
        # Charger modèle existant ou créer nouveau
        modele = await self.charger_modele_existant()
        
        # Intégrer nouveaux patterns
        if 'niveaux' not in modele:
            modele['niveaux'] = {}
        
        modele['niveaux'][niveau['nom']] = {
            'patterns': patterns,
            'metadata': niveau,
            'timestamp': datetime.now().isoformat()
        }
        
        # Recalculer métriques globales
        modele['metriques_globales'] = await self.calculer_metriques_globales(modele)
        
        return modele

    async def charger_modele_existant(self) -> Dict[str, Any]:
        """Charge le modèle existant ou créé un nouveau"""
        chemin_modele = self.chemin_resultats / 'modele_panini_iteratif.json'
        
        if chemin_modele.exists():
            try:
                with open(chemin_modele, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"⚠️ Erreur chargement modèle: {e}")
        
        # Nouveau modèle
        return {
            'version': '1.0',
            'creation': datetime.now().isoformat(),
            'niveaux': {},
            'metriques_globales': {}
        }

    async def calculer_metriques_globales(self, modele: Dict[str, Any]) -> Dict[str, Any]:
        """Calcule métriques globales du modèle"""
        niveaux = modele.get('niveaux', {})
        
        if not niveaux:
            return {'qualite_moyenne': 0.0, 'complexite_moyenne': 0.0}
        
        complexites = []
        for niveau_data in niveaux.values():
            patterns = niveau_data.get('patterns', {})
            complexite = patterns.get('complexite_score', 0.0)
            complexites.append(complexite)
        
        complexite_moyenne = sum(complexites) / len(complexites) if complexites else 0.0
        
        # Qualité basée sur progression cohérente
        qualite = min(1.0, complexite_moyenne * len(niveaux) / 5)  # 5 niveaux max
        
        return {
            'qualite_moyenne': qualite,
            'complexite_moyenne': complexite_moyenne,
            'niveaux_traites': len(niveaux),
            'progression_coherente': self.verifier_progression_coherente(complexites)
        }

    def verifier_progression_coherente(self, complexites: List[float]) -> bool:
        """Vérifie que la complexité progresse de manière cohérente"""
        if len(complexites) < 2:
            return True
        
        # Vérifier tendance croissante
        for i in range(1, len(complexites)):
            if complexites[i] < complexites[i-1] * 0.8:  # Tolérance 20%
                return False
        
        return True

    async def valider_amelioration(self, modele: Dict[str, Any]) -> float:
        """Valide l'amélioration du modèle"""
        metriques = modele.get('metriques_globales', {})
        qualite = metriques.get('qualite_moyenne', 0.0)
        
        # Sauvegarder qualité dans état
        self.etat_pipeline['modele_qualite'] = qualite
        
        logger.info(f"📊 Qualité modèle: {qualite:.3f}")
        return qualite

    async def optimiser_modele_cyclique(self):
        """Optimise le modèle à la fin de chaque cycle"""
        logger.info("⚡ Optimisation cyclique du modèle")
        
        # Charger modèle actuel
        modele = await self.charger_modele_existant()
        
        # Simplification: éliminer redondances
        modele_optimise = await self.simplifier_modele(modele)
        
        # Consolidation: fusionner patterns similaires
        modele_optimise = await self.consolider_patterns(modele_optimise)
        
        # Sauvegarder modèle optimisé
        await self.sauvegarder_modele(modele_optimise)
        
        self.etat_pipeline['derniere_optimisation'] = datetime.now().isoformat()
        logger.info("✅ Optimisation cyclique terminée")

    async def simplifier_modele(self, modele: Dict[str, Any]) -> Dict[str, Any]:
        """Simplifie le modèle en éliminant les redondances"""
        logger.info("🔧 Simplification du modèle")
        
        niveaux = modele.get('niveaux', {})
        
        # Éliminer structures dupliquées entre niveaux
        structures_globales = set()
        for niveau_nom, niveau_data in niveaux.items():
            patterns = niveau_data.get('patterns', {})
            structures = patterns.get('structures', [])
            
            # Garder seulement structures uniques
            structures_uniques = []
            for structure in structures:
                if structure not in structures_globales:
                    structures_uniques.append(structure)
                    structures_globales.add(structure)
            
            patterns['structures'] = structures_uniques
        
        logger.info(f"📉 Structures réduites à {len(structures_globales)} uniques")
        return modele

    async def consolider_patterns(self, modele: Dict[str, Any]) -> Dict[str, Any]:
        """Consolide patterns similaires"""
        logger.info("🔄 Consolidation des patterns")
        
        # Pour simplifier, on garde le modèle tel quel
        # À implémenter: clustering de patterns similaires
        
        return modele

    async def sauvegarder_modele(self, modele: Dict[str, Any]):
        """Sauvegarde le modèle optimisé"""
        chemin_modele = self.chemin_resultats / 'modele_panini_iteratif.json'
        
        with open(chemin_modele, 'w', encoding='utf-8') as f:
            json.dump(modele, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Modèle sauvegardé: {chemin_modele}")

    async def sauvegarder_resultats_niveau(self, nom_niveau: str, resultats: Dict[str, Any]):
        """Sauvegarde les résultats d'un niveau"""
        chemin_niveau = self.chemin_resultats / f'niveau_{nom_niveau}.json'
        
        with open(chemin_niveau, 'w', encoding='utf-8') as f:
            json.dump(resultats, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Résultats niveau {nom_niveau} sauvegardés")

    async def sauvegarder_etat(self):
        """Sauvegarde l'état actuel du pipeline"""
        chemin_etat = self.chemin_resultats / 'etat_pipeline.json'
        
        etat_complet = {
            **self.etat_pipeline,
            'timestamp': datetime.now().isoformat(),
            'niveaux_disponibles': self.niveaux_complexite
        }
        
        with open(chemin_etat, 'w', encoding='utf-8') as f:
            json.dump(etat_complet, f, indent=2, ensure_ascii=False)

    async def generer_rapport_final(self):
        """Génère rapport final du pipeline itératif"""
        logger.info("📋 Génération rapport final")
        
        modele_final = await self.charger_modele_existant()
        
        rapport = {
            'pipeline_complete': True,
            'timestamp': datetime.now().isoformat(),
            'cycles_totaux': self.etat_pipeline['cycles_completes'],
            'qualite_finale': self.etat_pipeline['modele_qualite'],
            'niveaux_traites': list(modele_final.get('niveaux', {}).keys()),
            'metriques_finales': modele_final.get('metriques_globales', {}),
            'optimisations_cycliques': self.etat_pipeline['cycles_completes']
        }
        
        chemin_rapport = self.chemin_resultats / 'rapport_final_pipeline.json'
        with open(chemin_rapport, 'w', encoding='utf-8') as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📊 Rapport final: {chemin_rapport}")

    async def gerer_erreur_pipeline(self, erreur: Exception):
        """Gère les erreurs du pipeline"""
        logger.error(f"🚨 Erreur pipeline: {erreur}")
        
        # Sauvegarder état d'erreur
        self.etat_pipeline['erreur'] = {
            'timestamp': datetime.now().isoformat(),
            'message': str(erreur),
            'niveau_actuel': self.etat_pipeline['niveau_actuel']
        }
        
        await self.sauvegarder_etat()

    def arreter_orchestration(self):
        """Arrête l'orchestration"""
        logger.info("🛑 Arrêt orchestrateur pipeline")
        self.running = False

async def main():
    """Point d'entrée principal"""
    orchestrateur = OrchestrateurPipelineIteratif()
    
    try:
        await orchestrateur.demarrer_orchestration()
    except KeyboardInterrupt:
        logger.info("⏹️ Arrêt demandé par utilisateur")
        orchestrateur.arreter_orchestration()
    except Exception as e:
        logger.error(f"❌ Erreur fatale: {e}")

if __name__ == "__main__":
    asyncio.run(main())