#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧗 OPTIMISEUR HILL-CLIMBING PANLANG
===================================
Stratégie d'amélioration continue avec hill-climbing et backtracking

ÉTAT INITIAL:
- Score actuel: 0.614 (ULTIME v1.0)
- Concepts: 155
- Statut: QUALITÉ CORRECTE

STRATÉGIE:
1. Itération continue d'amélioration
2. Hill-climbing avec sauvegarde du meilleur
3. Intégration nouveaux corpus si stagnation
4. Backtracking possible au sommet précédent
5. Rapport activité toutes les 10 minutes

Auteur: Système PanLang - Optimisation Continue
Date: 2025-09-27
"""

import json
import logging
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import random
import hashlib
from dataclasses import dataclass
from enum import Enum

class StatutOptimisation(Enum):
    EXPLORATION = "exploration"
    AMELIORATION = "amelioration"  
    STAGNATION = "stagnation"
    INTEGRATION_CORPUS = "integration_corpus"
    BACKTRACK = "backtrack"

@dataclass
class EtatModele:
    """État d'un modèle PanLang à un moment donné"""
    version: str
    score: float
    concepts: int
    timestamp: str
    chemin_dictionnaire: str
    hash_modele: str
    metadata: Dict

class OptimiseurHillClimbingPanLang:
    """Optimiseur hill-climbing continu pour PanLang"""
    
    def __init__(self):
        self.setup_logging()
        self.meilleur_modele = None
        self.modele_actuel = None
        self.historique_modeles = []
        self.iteration_courante = 0
        self.derniere_amelioration = None
        self.statut_actuel = StatutOptimisation.EXPLORATION
        self.corpus_integres = set()
        self.arret_demande = False
        
        # Configuration hill-climbing
        self.seuil_amelioration_min = 0.001  # 0.1% minimum
        self.max_iterations_stagnation = 3
        self.iterations_depuis_amelioration = 0
        
        # Thread rapport périodique
        self.thread_rapport = None
        self.demarrage = datetime.now()
        
    def setup_logging(self):
        """Configuration des logs"""
        log_dir = Path("optimisation_hillclimbing")
        log_dir.mkdir(exist_ok=True)
        
        # Log principal avec rotation
        log_file = log_dir / f"hillclimbing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Log d'activité séparé pour rapports
        self.log_activite = logging.getLogger('activite')
        handler_activite = logging.FileHandler(log_dir / "activite_continue.log")
        handler_activite.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        self.log_activite.addHandler(handler_activite)
    
    def charger_etat_initial(self) -> EtatModele:
        """Charge l'état initial depuis le meilleur modèle actuel"""
        
        try:
            chemin_ultime = "dictionnaire_panlang_ULTIME/dictionnaire_panlang_ULTIME_complet.json"
            with open(chemin_ultime, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Calcul hash pour identification unique
            hash_modele = hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()[:12]
            
            etat_initial = EtatModele(
                version="ULTIME-1.0",
                score=0.614,  # Score connu depuis validation
                concepts=data["metadata"]["concepts_totaux"],
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                chemin_dictionnaire=chemin_ultime,
                hash_modele=hash_modele,
                metadata=data["metadata"]
            )
            
            self.logger.info(f"🎯 État initial chargé: {etat_initial.concepts} concepts, score {etat_initial.score:.3f}")
            return etat_initial
            
        except Exception as e:
            self.logger.error(f"❌ Erreur chargement état initial: {e}")
            raise
    
    def sauvegarder_etat_modele(self, etat: EtatModele, raison: str = "sauvegarde"):
        """Sauvegarde un état de modèle avec métadonnées complètes"""
        
        save_dir = Path("optimisation_hillclimbing/etats_modeles")
        save_dir.mkdir(exist_ok=True)
        
        # Nom de fichier avec timestamp et hash
        nom_fichier = f"etat_{etat.version}_{etat.hash_modele}_{datetime.now().strftime('%H%M%S')}.json"
        chemin_sauvegarde = save_dir / nom_fichier
        
        donnees_sauvegarde = {
            "etat_modele": {
                "version": etat.version,
                "score": etat.score,
                "concepts": etat.concepts,
                "timestamp": etat.timestamp,
                "hash_modele": etat.hash_modele
            },
            "contexte_sauvegarde": {
                "raison": raison,
                "iteration": self.iteration_courante,
                "statut_optimisation": self.statut_actuel.value,
                "date_sauvegarde": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "metadata_originale": etat.metadata
        }
        
        with open(chemin_sauvegarde, 'w', encoding='utf-8') as f:
            json.dump(donnees_sauvegarde, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"💾 État sauvegardé: {nom_fichier} ({raison})")
        return chemin_sauvegarde
    
    def detecter_nouveaux_corpus(self) -> List[str]:
        """Détecte de nouveaux corpus disponibles - VERSION CORRIGÉE avec Wikipedia local"""
        
        # 🚀 PATTERNS EXHAUSTIFS - Accès Wikipedia local + Gutenberg + corpus workspace
        patterns_exhaustifs = [
            # Corpus workspace classiques
            "**/*corpus*.json",           # Récursif tous corpus
            "**/corpus.json",             # Fichiers corpus simples  
            "data/**/*.json",             # Tous JSON dans data/
            "**/*multilingue*.json",      # Corpus multilingues
            "**/*scientifique*.json",     # Corpus scientifiques
            "**/*prescolaire*.json",      # Corpus préscolaires
            "**/*unifie*.json",           # Corpus unifiés
            "tech/**/*.json",             # Corpus techniques
            "expansion_*/**/*.json",      # Corpus d'expansion
            
            # 📚 WIKIPEDIA LOCAL (dumps et extractions)
            "**/*wiki*.json",             # Extractions Wikipedia JSON
            "**/*wikipedia*.json",        # Données Wikipedia
            "**/*dump*.json",             # Dumps Wikipedia
            "**/*wiki*.txt",              # Textes Wikipedia
            "**/*wikipedia*.txt",         # Articles Wikipedia texte
            "dumps/**/*.json",            # Répertoire dumps
            "wikipedia/**/*.json",        # Répertoire wikipedia
            "**/lang_*/**/*.json",        # Langues spécifiques
            "**/*_fr.json", "**/*_en.json", "**/*_es.json", "**/*_de.json",  # Langues
            
            # 📖 GUTENBERG ET TEXTES CLASSIQUES
            "**/*gutenberg*.json",        # Données Gutenberg
            "**/*gutenberg*.txt",         # Textes Gutenberg
            "**/*livre*.json",            # Livres numérisés
            "**/*book*.json",             # Books anglais
            "**/*text*.json",             # Collections de textes
            
            # 🎯 FORMATS ALTERNATIFS
            "*.txt", "data/*.txt",        # Fichiers texte racine/data
            "**/*.md",                    # Markdown avec contenu
            "**/*analyse*.json",          # Fichiers d'analyse
            "**/*collection*.json"        # Collections diverses
        ]
        
        nouveaux_corpus = []
        workspace_root = Path.cwd()
        
        for pattern in patterns_exhaustifs:
            try:
                for chemin in workspace_root.glob(pattern):
                    if chemin.is_file() and str(chemin) not in self.corpus_integres:
                        if self._valider_corpus_ameliore(chemin):
                            nouveaux_corpus.append(str(chemin))
            except Exception as e:
                self.logger.debug(f"⚠️ Erreur pattern {pattern}: {e}")
        
        # Priorité aux corpus les plus volumineux/riches
        nouveaux_corpus_tries = sorted(
            nouveaux_corpus, 
            key=lambda x: Path(x).stat().st_size, 
            reverse=True
        )
        
        self.logger.info(f"🔍 {len(nouveaux_corpus_tries)} nouveaux corpus détectés (Wikipedia + Gutenberg + workspace)")
        return nouveaux_corpus_tries[:15]  # Limite raisonnable mais généreuse
    
    def generer_variation_modele(self) -> Optional[EtatModele]:
        """Génère une variation du modèle actuel pour test d'amélioration"""
        
        self.statut_actuel = StatutOptimisation.EXPLORATION
        
        # Stratégies de variation
        strategies = [
            "expansion_semantique_aleatoire",
            "optimisation_formules_existantes", 
            "generation_concepts_emergents_avances",
            "raffinement_atomique",
            "fusion_concepts_similaires"
        ]
        
        strategie = random.choice(strategies)
        self.logger.info(f"🧪 Test variation: {strategie}")
        
        try:
            if strategie == "expansion_semantique_aleatoire":
                return self._variation_expansion_aleatoire()
            elif strategie == "optimisation_formules_existantes":
                return self._variation_optimisation_formules()
            elif strategie == "generation_concepts_emergents_avances":
                return self._variation_concepts_emergents()
            else:
                return self._variation_generique()
                
        except Exception as e:
            self.logger.error(f"❌ Erreur génération variation {strategie}: {e}")
            return None
    
    def _variation_expansion_aleatoire(self) -> EtatModele:
        """Variation par expansion sémantique aléatoire"""
        
        # Génération de 5-15 nouveaux concepts par combinaisons aléatoires
        atomes_universels = [
            'MOUVEMENT', 'COGNITION', 'PERCEPTION', 'COMMUNICATION',
            'CREATION', 'EMOTION', 'EXISTENCE', 'DESTRUCTION', 
            'POSSESSION', 'DOMINATION'
        ]
        
        nouveaux_concepts = {}
        nb_concepts = random.randint(5, 15)
        
        for i in range(nb_concepts):
            # Combinaison aléatoire de 2-4 atomes
            nb_atomes = random.randint(2, 4)
            atomes_choisis = random.sample(atomes_universels, nb_atomes)
            
            nom_concept = f"CONCEPT_GENERE_{i+1:03d}"
            formule = " + ".join(atomes_choisis)
            
            nouveaux_concepts[nom_concept] = {
                "formule": formule,
                "complexite": len(atomes_choisis),
                "validite": random.uniform(0.4, 0.8),
                "source": "expansion_aleatoire",
                "iteration": self.iteration_courante
            }
        
        return self._creer_nouveau_modele(nouveaux_concepts, "expansion_aleatoire")
    
    def _variation_optimisation_formules(self) -> EtatModele:
        """Variation par optimisation des formules existantes"""
        
        # Chargement du modèle actuel pour optimisation
        try:
            with open(self.modele_actuel.chemin_dictionnaire, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            concepts_optimises = {}
            concepts_existants = data.get("concepts", {})
            
            # Optimisation de concepts sélectionnés aléatoirement
            concepts_a_optimiser = random.sample(
                list(concepts_existants.keys()), 
                min(10, len(concepts_existants))
            )
            
            for concept_nom in concepts_a_optimiser:
                concept_data = concepts_existants[concept_nom]
                
                # Tentative d'optimisation de la formule
                if isinstance(concept_data, dict) and "formule" in concept_data:
                    formule_actuelle = concept_data["formule"]
                    
                    # Simplification ou complexification légère
                    if "+" in formule_actuelle:
                        atomes = [a.strip() for a in formule_actuelle.split("+")]
                        
                        if len(atomes) > 2 and random.random() < 0.5:
                            # Simplification: retirer un atome
                            atomes_optimises = random.sample(atomes, len(atomes) - 1)
                        else:
                            # Complexification: ajouter un atome complémentaire
                            atomes_universels = ['MOUVEMENT', 'COGNITION', 'PERCEPTION', 'COMMUNICATION', 'CREATION', 'EMOTION', 'EXISTENCE', 'DESTRUCTION', 'POSSESSION', 'DOMINATION']
                            atomes_possibles = [a for a in atomes_universels if a not in atomes]
                            if atomes_possibles:
                                nouvel_atome = random.choice(atomes_possibles)
                                atomes_optimises = atomes + [nouvel_atome]
                            else:
                                atomes_optimises = atomes
                        
                        nouvelle_formule = " + ".join(atomes_optimises)
                        
                        concepts_optimises[f"{concept_nom}_OPT"] = {
                            "formule": nouvelle_formule,
                            "complexite": len(atomes_optimises),
                            "validite": concept_data.get("validite", 0.5) + random.uniform(-0.1, 0.2),
                            "source": "optimisation_formule",
                            "concept_origine": concept_nom
                        }
            
            return self._creer_nouveau_modele(concepts_optimises, "optimisation_formules")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur optimisation formules: {e}")
            raise
    
    def _variation_concepts_emergents(self) -> EtatModele:
        """Variation par génération de concepts émergents avancés"""
        
        patterns_sophistiques = [
            ("CONSCIENCE_COLLECTIVE", ["COGNITION", "COMMUNICATION", "EXISTENCE", "EMOTION"]),
            ("RESILIENCE_ADAPTIVE", ["DESTRUCTION", "CREATION", "MOUVEMENT", "EXISTENCE"]),
            ("INTELLIGENCE_INTUITIVE", ["PERCEPTION", "COGNITION", "EMOTION"]),
            ("CREATIVITE_SYSTEMIQUE", ["CREATION", "COMMUNICATION", "DOMINATION", "PERCEPTION"]),
            ("SAGESSE_EXPERIMENTALE", ["COGNITION", "EXISTENCE", "EMOTION", "PERCEPTION"]),
            ("LEADERSHIP_TRANSFORMATIONNEL", ["COMMUNICATION", "CREATION", "DOMINATION", "MOUVEMENT"]),
            ("EMPATHIE_STRATEGIQUE", ["EMOTION", "COGNITION", "COMMUNICATION", "PERCEPTION"]),
            ("INNOVATION_COLLABORATIVE", ["CREATION", "COMMUNICATION", "POSSESSION"])
        ]
        
        concepts_emergents = {}
        nb_concepts = random.randint(3, len(patterns_sophistiques))
        patterns_choisis = random.sample(patterns_sophistiques, nb_concepts)
        
        for nom_concept, atomes in patterns_choisis:
            concepts_emergents[nom_concept] = {
                "formule": " + ".join(atomes),
                "complexite": len(atomes),
                "validite": random.uniform(0.6, 0.9),  # Concepts sophistiqués = validité élevée
                "source": "emergence_avancee",
                "sophistication": "haute",
                "domaine": self._identifier_domaine_concept(atomes)
            }
        
        return self._creer_nouveau_modele(concepts_emergents, "concepts_emergents_avances")
    
    def _variation_generique(self) -> EtatModele:
        """Variation générique par ajout de concepts mixtes"""
        
        concepts_mixtes = {}
        
        # Mix de concepts ciblés selon domaines sous-représentés
        domaines_cibles = {
            "SCIENCE": ["OBSERVER", "EXPERIMENTER", "ANALYSER", "DEDUIRE"],
            "TECHNOLOGIE": ["INNOVER", "CONCEVOIR", "PROGRAMMER", "OPTIMISER"], 
            "SOCIAL": ["COLLABORER", "NEGOCIER", "INFLUENCER", "FEDERER"],
            "SPIRITUEL": ["MEDITER", "TRANSCENDER", "CONTEMPLER", "UNIFIER"]
        }
        
        for domaine, concepts_domaine in domaines_cibles.items():
            concept_choisi = random.choice(concepts_domaine)
            
            # Attribution d'atomes cohérents avec le domaine
            if domaine == "SCIENCE":
                atomes = ["COGNITION", "PERCEPTION", "COMMUNICATION"]
            elif domaine == "TECHNOLOGIE":
                atomes = ["CREATION", "COGNITION", "DOMINATION"]
            elif domaine == "SOCIAL":
                atomes = ["COMMUNICATION", "EMOTION", "POSSESSION"]
            else:  # SPIRITUEL
                atomes = ["EXISTENCE", "COGNITION", "EMOTION"]
            
            concepts_mixtes[concept_choisi] = {
                "formule": " + ".join(atomes),
                "complexite": len(atomes),
                "validite": random.uniform(0.5, 0.8),
                "source": "variation_generique",
                "domaine": domaine.lower()
            }
        
        return self._creer_nouveau_modele(concepts_mixtes, "variation_generique")
    
    def _identifier_domaine_concept(self, atomes: List[str]) -> str:
        """Identifie le domaine probable d'un concept selon ses atomes"""
        
        if "COGNITION" in atomes and "PERCEPTION" in atomes:
            return "epistemologique"
        elif "EMOTION" in atomes and "COMMUNICATION" in atomes:
            return "social"
        elif "CREATION" in atomes and "DESTRUCTION" in atomes:
            return "transformationnel"
        elif "DOMINATION" in atomes:
            return "politique"
        else:
            return "general"
    
    def _creer_nouveau_modele(self, nouveaux_concepts: Dict, source: str) -> EtatModele:
        """Crée un nouveau modèle en fusionnant avec l'existant"""
        
        try:
            # Chargement du modèle de base
            with open(self.modele_actuel.chemin_dictionnaire, 'r', encoding='utf-8') as f:
                data_base = json.load(f)
            
            # Fusion des concepts
            concepts_fusionnes = data_base.get("concepts", {}).copy()
            concepts_fusionnes.update(nouveaux_concepts)
            
            # Création nouveau modèle
            nouvelle_version = f"{self.modele_actuel.version}-iter{self.iteration_courante:03d}"
            
            nouveau_modele_data = {
                "metadata": {
                    "version": nouvelle_version,
                    "date_creation": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "concepts_totaux": len(concepts_fusionnes),
                    "source_variation": source,
                    "concepts_ajoutes": len(nouveaux_concepts),
                    "iteration_hill_climbing": self.iteration_courante,
                    "modele_parent": self.modele_actuel.version
                },
                "concepts": concepts_fusionnes
            }
            
            # Sauvegarde du nouveau modèle
            nouveau_chemin = f"optimisation_hillclimbing/modeles_test/modele_{nouvelle_version}.json"
            Path(nouveau_chemin).parent.mkdir(parents=True, exist_ok=True)
            
            with open(nouveau_chemin, 'w', encoding='utf-8') as f:
                json.dump(nouveau_modele_data, f, ensure_ascii=False, indent=2)
            
            # Création de l'état
            hash_modele = hashlib.md5(json.dumps(nouveau_modele_data, sort_keys=True).encode()).hexdigest()[:12]
            
            nouvel_etat = EtatModele(
                version=nouvelle_version,
                score=0.0,  # À évaluer
                concepts=len(concepts_fusionnes),
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                chemin_dictionnaire=nouveau_chemin,
                hash_modele=hash_modele,
                metadata=nouveau_modele_data["metadata"]
            )
            
            self.logger.info(f"✨ Nouveau modèle créé: {nouvelle_version} ({len(nouveaux_concepts)} concepts ajoutés)")
            return nouvel_etat
            
        except Exception as e:
            self.logger.error(f"❌ Erreur création nouveau modèle: {e}")
            raise
    
    def evaluer_modele(self, etat: EtatModele) -> float:
        """Évalue la performance d'un modèle de manière rapide"""
        
        try:
            # Validation rapide simplifiée
            score_base = 0.0
            
            # Score basé sur le nombre de concepts (facteur quantitatif)
            score_concepts = min(1.0, etat.concepts / 300)  # 300 concepts = score parfait
            score_base += score_concepts * 0.3
            
            # Évaluation qualitative rapide
            with open(etat.chemin_dictionnaire, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            concepts = data.get("concepts", {})
            
            # Score basé sur la validité moyenne
            validites = []
            for concept_data in concepts.values():
                if isinstance(concept_data, dict):
                    validite = concept_data.get("validite", 0.5)
                    validites.append(validite)
            
            if validites:
                score_qualite = sum(validites) / len(validites)
                score_base += score_qualite * 0.4
            
            # Score basé sur la diversité des sources
            sources = set()
            for concept_data in concepts.values():
                if isinstance(concept_data, dict):
                    source = concept_data.get("source", "unknown")
                    sources.add(source)
            
            score_diversite = min(1.0, len(sources) / 10)  # 10 sources différentes = parfait
            score_base += score_diversite * 0.2
            
            # Score bonus pour innovation
            concepts_emergents = sum(1 for c in concepts.values() 
                                   if isinstance(c, dict) and 
                                   c.get("source", "").startswith("emerge"))
            
            score_innovation = min(1.0, concepts_emergents / 20)
            score_base += score_innovation * 0.1
            
            score_final = min(1.0, score_base)
            
            self.logger.info(f"📊 Évaluation {etat.version}: {score_final:.3f} ({etat.concepts} concepts)")
            return score_final
            
        except Exception as e:
            self.logger.error(f"❌ Erreur évaluation modèle {etat.version}: {e}")
            return 0.0
    
    def integrer_nouveau_corpus(self) -> Optional[EtatModele]:
        """Intègre un nouveau corpus pour sortir de la stagnation"""
        
        self.statut_actuel = StatutOptimisation.INTEGRATION_CORPUS
        self.logger.info("📚 Recherche de nouveaux corpus...")
        
        nouveaux_corpus = self.detecter_nouveaux_corpus()
        
        if not nouveaux_corpus:
            self.logger.warning("⚠️ Aucun nouveau corpus disponible")
            return None
        
        corpus_choisi = random.choice(nouveaux_corpus)
        self.logger.info(f"📖 Intégration corpus: {Path(corpus_choisi).name}")
        
        try:
            concepts_corpus = self._extraire_concepts_corpus(corpus_choisi)
            if concepts_corpus:
                self.corpus_integres.add(corpus_choisi)
                return self._creer_nouveau_modele(concepts_corpus, f"corpus_{Path(corpus_choisi).stem}")
            else:
                self.logger.warning(f"⚠️ Aucun concept extrait de {corpus_choisi}")
                return None
                
        except Exception as e:
            self.logger.error(f"❌ Erreur intégration corpus {corpus_choisi}: {e}")
            return None
    
    def _extraire_concepts_corpus(self, chemin_corpus: str) -> Dict:
        """Extrait des concepts d'un corpus"""
        
        concepts_extraits = {}
        
        try:
            if Path(chemin_corpus).suffix == '.json':
                with open(chemin_corpus, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Extraction selon structure du corpus
                if isinstance(data, dict):
                    for key, value in data.items():
                        if isinstance(value, str) and len(value) > 10:
                            # Génération concept basique depuis texte
                            concepts_extraits[key.upper()] = {
                                "formule": self._generer_formule_depuis_texte(value),
                                "complexite": 2,
                                "validite": 0.6,
                                "source": f"corpus_{Path(chemin_corpus).stem}",
                                "texte_origine": value[:100] + "..."
                            }
                        elif isinstance(value, dict) and "formule" in value:
                            concepts_extraits[key.upper()] = value
                
            elif Path(chemin_corpus).suffix == '.txt':
                # Extraction depuis fichier texte
                with open(chemin_corpus, 'r', encoding='utf-8') as f:
                    lignes = f.readlines()[:50]  # Limite pour éviter surcharge
                
                for i, ligne in enumerate(lignes):
                    if len(ligne.strip()) > 20:
                        concept_nom = f"CONCEPT_TEXTE_{i+1:03d}"
                        concepts_extraits[concept_nom] = {
                            "formule": self._generer_formule_depuis_texte(ligne),
                            "complexite": 3,
                            "validite": 0.5,
                            "source": f"texte_{Path(chemin_corpus).stem}",
                            "ligne_origine": i + 1
                        }
            
            self.logger.info(f"📚 {len(concepts_extraits)} concepts extraits de {Path(chemin_corpus).name}")
            return concepts_extraits
            
        except Exception as e:
            self.logger.error(f"❌ Erreur extraction corpus {chemin_corpus}: {e}")
            return {}
    
    def _valider_corpus_ameliore(self, chemin: Path) -> bool:
        """Validation améliorée d'un corpus - seuils abaissés pour Wikipedia/Gutenberg"""
        
        try:
            if not chemin.is_file():
                return False
            
            # Exclusions système mais permissive pour Wikipedia/Gutenberg
            chemin_str = str(chemin).lower()
            if any(excl in chemin_str for excl in ['node_modules', '.git', '__pycache__', '.pytest_cache', 'package-lock']):
                return False
                
            # Priorité HAUTE pour Wikipedia et Gutenberg
            est_wikipedia = any(wiki in chemin_str for wiki in ['wiki', 'wikipedia', 'dump'])
            est_gutenberg = any(gut in chemin_str for gut in ['gutenberg', 'livre', 'book'])
            
            if chemin.suffix == '.json':
                with open(chemin, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if isinstance(data, dict):
                    # Seuils spéciaux pour sources prioritaires
                    if est_wikipedia or est_gutenberg:
                        return len(data) >= 1  # Très permissif pour Wikipedia/Gutenberg
                    else:
                        return len(data) >= 3  # Seuil abaissé vs 5 original
                        
            elif chemin.suffix in ['.txt', '.md']:
                taille = chemin.stat().st_size
                
                # Seuils adaptés selon la source
                if est_wikipedia or est_gutenberg:
                    return 100 <= taille <= 50_000_000  # Très large pour Wikipedia/Gutenberg
                else:
                    return 500 <= taille <= 10_000_000   # Seuil abaissé vs 1000 original
            
            return False
            
        except Exception as e:
            self.logger.debug(f"⚠️ Erreur validation {chemin}: {e}")
            return False
    
    def _generer_formule_depuis_texte(self, texte: str) -> str:
        """Génère une formule atomique basique depuis un texte"""
        
        # Analyse basique du contenu pour choisir des atomes pertinents
        mots_cles = {
            "COGNITION": ["penser", "réfléchir", "comprendre", "analyser", "raisonner"],
            "EMOTION": ["sentir", "ressentir", "émouvoir", "aimer", "craindre"],
            "COMMUNICATION": ["dire", "parler", "exprimer", "communiquer", "transmettre"],
            "CREATION": ["créer", "faire", "construire", "produire", "inventer"],
            "PERCEPTION": ["voir", "observer", "percevoir", "remarquer", "sentir"],
            "MOUVEMENT": ["aller", "bouger", "déplacer", "avancer", "mouvoir"],
            "EXISTENCE": ["être", "exister", "vivre", "subsister", "demeurer"],
            "DESTRUCTION": ["détruire", "casser", "éliminer", "supprimer", "ruiner"],
            "POSSESSION": ["avoir", "posséder", "détenir", "garder", "conserver"],
            "DOMINATION": ["contrôler", "dominer", "diriger", "commander", "gouverner"]
        }
        
        texte_lower = texte.lower()
        atomes_detectes = []
        
        for atome, mots in mots_cles.items():
            if any(mot in texte_lower for mot in mots):
                atomes_detectes.append(atome)
        
        # Si pas d'atomes détectés, combinaison aléatoire
        if not atomes_detectes:
            atomes_universels = list(mots_cles.keys())
            atomes_detectes = random.sample(atomes_universels, random.randint(2, 3))
        
        # Limite à 4 atomes maximum
        if len(atomes_detectes) > 4:
            atomes_detectes = random.sample(atomes_detectes, 4)
        
        return " + ".join(atomes_detectes)
    
    def effectuer_backtrack(self) -> bool:
        """Effectue un backtrack vers le meilleur modèle précédent"""
        
        self.statut_actuel = StatutOptimisation.BACKTRACK
        
        if self.meilleur_modele is None:
            self.logger.warning("⚠️ Aucun modèle pour backtrack")
            return False
        
        self.logger.info(f"🔙 Backtrack vers {self.meilleur_modele.version} (score: {self.meilleur_modele.score:.3f})")
        
        # Restauration du meilleur modèle
        self.modele_actuel = self.meilleur_modele
        self.iterations_depuis_amelioration = 0
        
        # Sauvegarde de l'action de backtrack
        self.sauvegarder_etat_modele(self.meilleur_modele, "backtrack")
        
        return True
    
    def rapport_activite_periodique(self):
        """Rapport d'activité toutes les 10 minutes"""
        
        while not self.arret_demande:
            time.sleep(600)  # 10 minutes
            
            if self.arret_demande:
                break
            
            duree = datetime.now() - self.demarrage
            
            rapport = f"""
🕰️ RAPPORT ACTIVITÉ - {datetime.now().strftime('%H:%M:%S')}
========================================
⏱️ Durée session: {duree}
🔄 Itération courante: {self.iteration_courante}
📊 Statut: {self.statut_actuel.value.upper()}

📈 MODÈLE ACTUEL:
   Version: {self.modele_actuel.version if self.modele_actuel else 'None'}
   Score: {self.modele_actuel.score:.3f if self.modele_actuel else 'N/A'}
   Concepts: {self.modele_actuel.concepts if self.modele_actuel else 'N/A'}

🏆 MEILLEUR MODÈLE:
   Version: {self.meilleur_modele.version if self.meilleur_modele else 'None'}
   Score: {self.meilleur_modele.score:.3f if self.meilleur_modele else 'N/A'}
   Concepts: {self.meilleur_modele.concepts if self.meilleur_modele else 'N/A'}

🔧 ÉTAT OPTIMISATION:
   Modèles testés: {len(self.historique_modeles)}
   Dernière amélioration: {self.derniere_amelioration or 'Jamais'}
   Stagnation: {self.iterations_depuis_amelioration}/{self.max_iterations_stagnation}
   Corpus intégrés: {len(self.corpus_integres)}

🎯 PROCHAINES ACTIONS: {self._predire_prochaines_actions()}
"""
            
            print(rapport)
            self.log_activite.info(rapport.replace('\n', ' | '))
    
    def _predire_prochaines_actions(self) -> str:
        """Prédit les prochaines actions selon l'état actuel"""
        
        if self.iterations_depuis_amelioration >= self.max_iterations_stagnation:
            return "Intégration nouveau corpus ou backtrack"
        elif self.statut_actuel == StatutOptimisation.INTEGRATION_CORPUS:
            return "Test nouveau modèle avec corpus intégré"
        elif self.statut_actuel == StatutOptimisation.BACKTRACK:
            return "Reprise exploration depuis meilleur modèle"
        else:
            return "Génération et test variations modèle"
    
    def iteration_hill_climbing(self) -> bool:
        """Une itération complète de hill-climbing"""
        
        self.iteration_courante += 1
        self.logger.info(f"🔄 ITÉRATION {self.iteration_courante}")
        
        try:
            # Génération d'une variation ou intégration corpus si stagnation
            if self.iterations_depuis_amelioration >= self.max_iterations_stagnation:
                # Tentative intégration nouveau corpus
                nouveau_modele = self.integrer_nouveau_corpus()
                
                if nouveau_modele is None:
                    # Aucun corpus disponible -> backtrack
                    if self.effectuer_backtrack():
                        return True
                    else:
                        self.logger.warning("⚠️ Impossible de continuer - arrêt recommandé")
                        return False
            else:
                # Génération variation normale
                nouveau_modele = self.generer_variation_modele()
                
                if nouveau_modele is None:
                    self.logger.error("❌ Impossible de générer variation")
                    return False
            
            # Évaluation du nouveau modèle
            score_nouveau = self.evaluer_modele(nouveau_modele)
            nouveau_modele.score = score_nouveau
            
            # Décision hill-climbing
            amelioration = False
            
            if self.modele_actuel is None or score_nouveau > self.modele_actuel.score + self.seuil_amelioration_min:
                # Amélioration trouvée
                self.statut_actuel = StatutOptimisation.AMELIORATION
                
                # Sauvegarde ancien modèle dans historique
                if self.modele_actuel:
                    self.historique_modeles.append(self.modele_actuel)
                
                # Adoption du nouveau modèle
                self.modele_actuel = nouveau_modele
                
                # Mise à jour du meilleur si nécessaire
                if self.meilleur_modele is None or score_nouveau > self.meilleur_modele.score:
                    self.meilleur_modele = nouveau_modele
                    self.sauvegarder_etat_modele(self.meilleur_modele, "nouveau_meilleur")
                    self.logger.info(f"🏆 NOUVEAU MEILLEUR: {score_nouveau:.3f} (+{score_nouveau - (self.meilleur_modele.score if self.meilleur_modele else 0):.3f})")
                
                self.derniere_amelioration = datetime.now().strftime("%H:%M:%S")
                self.iterations_depuis_amelioration = 0
                amelioration = True
                
                self.logger.info(f"✅ Amélioration acceptée: {self.modele_actuel.score:.3f}")
                
            else:
                # Pas d'amélioration
                self.statut_actuel = StatutOptimisation.STAGNATION
                self.iterations_depuis_amelioration += 1
                
                self.logger.info(f"❌ Variation rejetée: {score_nouveau:.3f} vs {self.modele_actuel.score:.3f}")
            
            # Sauvegarde de l'état testé
            self.sauvegarder_etat_modele(nouveau_modele, "variation_testee" if not amelioration else "amelioration")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erreur itération {self.iteration_courante}: {e}")
            return False
    
    def optimisation_continue(self):
        """Boucle principale d'optimisation continue"""
        
        print("🧗 DÉMARRAGE OPTIMISATION HILL-CLIMBING CONTINUE")
        print("================================================")
        
        # Initialisation
        self.modele_actuel = self.charger_etat_initial()
        self.meilleur_modele = self.modele_actuel
        self.sauvegarder_etat_modele(self.modele_actuel, "etat_initial")
        
        # Démarrage thread rapport périodique
        self.thread_rapport = threading.Thread(target=self.rapport_activite_periodique, daemon=True)
        self.thread_rapport.start()
        
        print(f"🎯 État initial: {self.modele_actuel.concepts} concepts, score {self.modele_actuel.score:.3f}")
        print("⏱️ Rapports d'activité toutes les 10 minutes")
        print("🛑 Interrompez manuellement quand souhaité")
        print()
        
        # Boucle principale
        while not self.arret_demande:
            try:
                success = self.iteration_hill_climbing()
                
                if not success:
                    self.logger.error("❌ Échec itération - arrêt recommandé")
                    break
                
                # Pause courte entre itérations
                time.sleep(2)
                
            except KeyboardInterrupt:
                print("\n🛑 Interruption demandée par l'utilisateur")
                break
            except Exception as e:
                self.logger.error(f"❌ Erreur critique: {e}")
                break
        
        # Arrêt propre
        self.arret_demande = True
        
        print(f"\n🏁 OPTIMISATION TERMINÉE")
        print(f"   🔄 Itérations effectuées: {self.iteration_courante}")
        print(f"   🏆 Meilleur score atteint: {self.meilleur_modele.score:.3f}")
        print(f"   📚 Concepts final: {self.meilleur_modele.concepts}")
        print(f"   ⏱️ Durée totale: {datetime.now() - self.demarrage}")

def main():
    """Point d'entrée principal"""
    
    try:
        optimiseur = OptimiseurHillClimbingPanLang()
        optimiseur.optimisation_continue()
        
    except KeyboardInterrupt:
        print("\n🛑 Arrêt demandé par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        logging.error(f"❌ Erreur fatale: {e}")

if __name__ == "__main__":
    main()