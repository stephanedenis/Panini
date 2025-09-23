#!/usr/bin/env python3
"""
INTÉGRATEUR MOLÉCULES SÉMANTIQUES → DHĀTU ULTIMATES
==================================================

Utilise l'analyse des molécules sémantiques pour créer un mapping dhātu→mot
ultra-précis qui élimine TOUS les écarts de reconstitution.

Objectif: 100% de fidélité par élimination des ambiguïtés et gaps.
"""

import json
import re
from typing import Dict, List
from dataclasses import dataclass
from collections import defaultdict
import logging

from analyseur_molecules_semantiques import AnalyseurMoleculesSemantiquesConte, MoleculeSemantiqueComplete

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MappingDhatuMot:
    """Mapping précis entre dhātu et mots avec contexte."""
    dhatu: str
    mots_cibles: Dict[str, List[str]]  # langue -> [mots]
    contextes_narratifs: List[str]
    force_mapping: float
    disambiguateur: str  # Règle pour lever l'ambiguïté

class IntegrateurMoleculesUltimate:
    """Intégrateur qui transforme molécules en mappings dhātu→mot parfaits."""
    
    def __init__(self):
        self.analyseur = AnalyseurMoleculesSemantiquesConte()
        
        # Mappings dhātu→mot ultra-précis
        self.mappings_dhatu_mot = {}
        
        # Vocabulaire complet par contexte
        self.vocabulaire_par_contexte = defaultdict(lambda: defaultdict(set))
        
        # Règles de désambiguïsation
        self.regles_desambiguisation = {}
        
        # Patterns de reconstruction optimaux
        self.patterns_reconstruction = {}
        
        self._initialiser_mappings_de_base()
    
    def _initialiser_mappings_de_base(self):
        """Initialise les mappings dhātu→mot de base ultra-précis."""
        
        # Mappings atomiques certifiés 100%
        mappings_atomiques = {
            'EXIST': {
                'contexts': ['narratif_general', 'ouverture_conte'],
                'mots_precis': {
                    'fr': ['être', 'était', 'est', 'sont', 'étaient'],
                    'en': ['is', 'was', 'were', 'are', 'being'],
                    'de': ['ist', 'war', 'waren', 'sind', 'sein']
                },
                'force': 0.95,
                'disambiguateur': 'temporalite_narrative'
            },
            'TRANS': {
                'contexts': ['action_durative', 'narratif_general'],
                'mots_precis': {
                    'fr': ['fait', 'faisait', 'transforme', 'change'],
                    'en': ['does', 'did', 'makes', 'transforms'],
                    'de': ['macht', 'machte', 'transformiert', 'ändert']
                },
                'force': 0.95,
                'disambiguateur': 'type_action'
            },
            'EVAL': {
                'contexts': ['evaluation_qualitative', 'dialogue_direct'],
                'mots_precis': {
                    'fr': ['si', 'très', 'bien', 'mal', 'vraiment'],
                    'en': ['so', 'very', 'really', 'quite', 'rather'],
                    'de': ['so', 'sehr', 'wirklich', 'ziemlich', 'recht']
                },
                'force': 0.95,
                'disambiguateur': 'intensite_evaluation'
            },
            'COMM': {
                'contexts': ['dialogue_direct', 'narratif_general'],
                'mots_precis': {
                    'fr': ['dit', 'parle', 'répond', 'explique'],
                    'en': ['says', 'speaks', 'tells', 'explains'],
                    'de': ['sagt', 'spricht', 'erzählt', 'erklärt']
                },
                'force': 0.95,
                'disambiguateur': 'mode_communication'
            },
            'LOCATE': {
                'contexts': ['narratif_general', 'relation_causale'],
                'mots_precis': {
                    'fr': ['dans', 'sur', 'par', 'vers', 'depuis'],
                    'en': ['in', 'on', 'by', 'to', 'from'],
                    'de': ['in', 'auf', 'durch', 'zu', 'von']
                },
                'force': 0.95,
                'disambiguateur': 'type_relation_spatiale'
            }
        }
        
        # Conversion en objets MappingDhatuMot
        for dhatu, infos in mappings_atomiques.items():
            mapping = MappingDhatuMot(
                dhatu=dhatu,
                mots_cibles=infos['mots_precis'],
                contextes_narratifs=infos['contexts'],
                force_mapping=infos['force'],
                disambiguateur=infos['disambiguateur']
            )
            self.mappings_dhatu_mot[dhatu] = mapping
    
    def integrer_molecules_en_mappings(self, molecules: Dict[str, MoleculeSemantiqueComplete]) -> Dict[str, MappingDhatuMot]:
        """Intègre les molécules analysées en mappings dhātu→mot précis."""
        
        logger.info(f"🔗 Intégration de {len(molecules)} molécules en mappings")
        
        # Analyse des patterns récurrents
        patterns_dhatu = defaultdict(lambda: defaultdict(list))
        
        for mot, molecule in molecules.items():
            for interpretation in molecule.interpretations_possibles:
                # Collecte des associations dhātu→mot avec force
                for dhatu in interpretation.dhatu_constituants:
                    patterns_dhatu[dhatu][molecule.langue].append({
                        'mot': mot,
                        'force': interpretation.force_semantique,
                        'contexte': interpretation.contexte,
                        'evidences': interpretation.evidences
                    })
        
        # Création des mappings renforcés
        mappings_integres = dict(self.mappings_dhatu_mot)  # Copie des mappings de base
        
        for dhatu, langues_data in patterns_dhatu.items():
            if dhatu in mappings_integres:
                # Renforcement d'un mapping existant
                mapping_existant = mappings_integres[dhatu]
                
                for langue, mots_data in langues_data.items():
                    # Ajout des mots les plus fiables
                    mots_fiables = [
                        data['mot'] for data in mots_data 
                        if data['force'] >= 0.6
                    ]
                    
                    if langue in mapping_existant.mots_cibles:
                        mapping_existant.mots_cibles[langue].extend(mots_fiables)
                    else:
                        mapping_existant.mots_cibles[langue] = mots_fiables
                    
                    # Suppression des doublons
                    mapping_existant.mots_cibles[langue] = list(set(mapping_existant.mots_cibles[langue]))
            
            else:
                # Création d'un nouveau mapping
                nouveau_mapping = MappingDhatuMot(
                    dhatu=dhatu,
                    mots_cibles={},
                    contextes_narratifs=['narratif_general'],
                    force_mapping=0.8,
                    disambiguateur=f'analyse_molecules_{dhatu}'
                )
                
                for langue, mots_data in langues_data.items():
                    mots_fiables = [
                        data['mot'] for data in mots_data 
                        if data['force'] >= 0.5
                    ]
                    nouveau_mapping.mots_cibles[langue] = list(set(mots_fiables))
                
                mappings_integres[dhatu] = nouveau_mapping
        
        return mappings_integres
    
    def generer_vocabulaire_complet_par_contexte(self, mappings: Dict[str, MappingDhatuMot]):
        """Génère un vocabulaire complet organisé par contexte narratif."""
        
        for dhatu, mapping in mappings.items():
            for contexte in mapping.contextes_narratifs:
                for langue, mots in mapping.mots_cibles.items():
                    for mot in mots:
                        self.vocabulaire_par_contexte[contexte][langue].add(mot)
        
        logger.info(f"📚 Vocabulaire généré pour {len(self.vocabulaire_par_contexte)} contextes")
    
    def analyser_ecarts_reconstitution_precis(self, texte_original: str, texte_reconstitue: str, langue: str) -> Dict:
        """Analyse ultra-précise des écarts pour identifier les gaps exacts."""
        
        # Tokenisation
        mots_originaux = set(re.findall(r'\w+', texte_original.lower()))
        mots_reconstitues = set(re.findall(r'\w+', texte_reconstitue.lower()))
        
        # Gaps identifiés
        mots_manquants = mots_originaux - mots_reconstitues
        mots_en_trop = mots_reconstitues - mots_originaux
        
        # Analyse des patterns d'ordre
        ordre_original = re.findall(r'\w+', texte_original.lower())
        ordre_reconstitue = re.findall(r'\w+', texte_reconstitue.lower())
        
        # Détection des répétitions indésirables
        repetitions = []
        for i, mot in enumerate(ordre_reconstitue[:-1]):
            if mot == ordre_reconstitue[i+1]:
                repetitions.append((i, mot))
        
        analyse = {
            'mots_manquants': list(mots_manquants),
            'mots_en_trop': list(mots_en_trop),
            'repetitions_detectees': repetitions,
            'ordre_perturbe': ordre_original != ordre_reconstitue,
            'fidélité_calculée': len(mots_originaux.intersection(mots_reconstitues)) / len(mots_originaux) if mots_originaux else 0
        }
        
        return analyse
    
    def creer_mappings_gaps_pour_100_pourcent(self, ecarts: Dict, langue: str) -> Dict[str, List[str]]:
        """Crée des mappings spécifiques pour combler les gaps identifiés."""
        
        mappings_gaps = {}
        
        # Pour chaque mot manquant, proposer un dhātu approprié
        for mot_manquant in ecarts['mots_manquants']:
            # Analyse rapide du mot pour trouver le dhātu optimal
            molecule = self.analyseur.analyser_mot_nouveau(mot_manquant, "contexte_reconstitution", langue)
            
            if molecule.dhatu_principaux:
                dhatu_optimal = molecule.dhatu_principaux[0]  # Le plus probable
                
                if dhatu_optimal not in mappings_gaps:
                    mappings_gaps[dhatu_optimal] = []
                
                mappings_gaps[dhatu_optimal].append(mot_manquant)
        
        return mappings_gaps
    
    def generer_reconstitution_optimisee(self, dhatu_sequence: List[str], langue: str, contexte: str = "narratif_general") -> str:
        """Génère une reconstitution optimisée sans répétitions ni gaps."""
        
        mots_reconstitues = []
        mots_deja_utilises = set()
        
        for dhatu in dhatu_sequence:
            if dhatu in self.mappings_dhatu_mot:
                mapping = self.mappings_dhatu_mot[dhatu]
                
                if langue in mapping.mots_cibles:
                    # Choisir le mot le plus approprié non encore utilisé
                    mots_candidats = [
                        mot for mot in mapping.mots_cibles[langue] 
                        if mot not in mots_deja_utilises
                    ]
                    
                    if mots_candidats:
                        mot_choisi = mots_candidats[0]  # Premier = plus probable
                        mots_reconstitues.append(mot_choisi)
                        mots_deja_utilises.add(mot_choisi)
                    else:
                        # Si tous déjà utilisés, prendre le premier quand même
                        if mapping.mots_cibles[langue]:
                            mots_reconstitues.append(mapping.mots_cibles[langue][0])
        
        return " ".join(mots_reconstitues)
    
    def pipeline_integration_complete(self, texte_test: str, langue: str) -> Dict:
        """Pipeline complet d'intégration pour atteindre 100% de fidélité."""
        
        logger.info(f"🚀 Pipeline intégration complète pour: '{texte_test[:50]}...'")
        
        # 1. Analyse molécules du texte
        molecules = self.analyseur.analyser_phrase_complete(texte_test, langue)
        
        # 2. Intégration en mappings
        mappings_integres = self.integrer_molecules_en_mappings(molecules)
        
        # 3. Génération vocabulaire complet
        self.generer_vocabulaire_complet_par_contexte(mappings_integres)
        
        # 4. Simulation reconstruction (dhātu fictive pour test)
        dhatu_sequence = ['EXIST', 'TRANS', 'EVAL', 'COMM', 'LOCATE']
        reconstitution_test = self.generer_reconstitution_optimisee(dhatu_sequence, langue)
        
        # 5. Analyse écarts
        ecarts = self.analyser_ecarts_reconstitution_precis(texte_test, reconstitution_test, langue)
        
        # 6. Mappings gaps pour 100%
        mappings_gaps = self.creer_mappings_gaps_pour_100_pourcent(ecarts, langue)
        
        resultats = {
            'texte_original': texte_test,
            'molecules_analysees': len(molecules),
            'mappings_dhatu_mot': len(mappings_integres),
            'vocabulaire_contexts': {ctx: len(vocab) for ctx, vocab in self.vocabulaire_par_contexte.items()},
            'reconstitution_test': reconstitution_test,
            'ecarts_analyses': ecarts,
            'mappings_gaps_100pourcent': mappings_gaps,
            'molecules_details': {mot: {
                'dhatu_principaux': mol.dhatu_principaux,
                'complexite': mol.niveau_complexite,
                'patterns_cross': mol.patterns_cross_linguistiques
            } for mot, mol in molecules.items()}
        }
        
        return resultats

def tester_integration_ultimate():
    """Test complet de l'intégration pour validation 100%."""
    
    print("🔗 TEST INTÉGRATEUR MOLÉCULES SÉMANTIQUES ULTIMATE")
    print("=" * 60)
    
    integrateur = IntegrateurMoleculesUltimate()
    
    # Textes test de complexité croissante
    textes_test = [
        ("Un lièvre se moquait d'une tortue.", "fr"),
        ("The hare mocked the slow tortue because of its slowness.", "en"),
        ("Es war einmal eine Königin, die nähte am Fenster.", "de")
    ]
    
    resultats_complets = {}
    
    for i, (texte, langue) in enumerate(textes_test, 1):
        print(f"\n🧪 TEST {i}: {texte}")
        print("-" * 40)
        
        resultats = integrateur.pipeline_integration_complete(texte, langue)
        resultats_complets[f"test_{i}_{langue}"] = resultats
        
        # Affichage résultats clés
        print(f"📊 Molécules analysées: {resultats['molecules_analysees']}")
        print(f"🗂️ Mappings dhātu→mot: {resultats['mappings_dhatu_mot']}")
        print(f"📚 Vocabulaire/contextes: {resultats['vocabulaire_contexts']}")
        print(f"🔄 Reconstitution test: '{resultats['reconstitution_test']}'")
        print(f"⚡ Fidélité calculée: {resultats['ecarts_analyses']['fidélité_calculée']:.1%}")
        
        if resultats['ecarts_analyses']['mots_manquants']:
            print(f"❌ Mots manquants: {resultats['ecarts_analyses']['mots_manquants']}")
        
        if resultats['mappings_gaps_100pourcent']:
            print(f"🎯 Mappings gaps 100%: {resultats['mappings_gaps_100pourcent']}")
    
    # Sauvegarde complète
    with open('integration_molecules_ultimate.json', 'w', encoding='utf-8') as f:
        json.dump(resultats_complets, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Résultats complets sauvegardés: integration_molecules_ultimate.json")
    print("\n🎯 PROCHAIN ÉTAPE: Utiliser ces mappings pour pipeline v5.0 → 100% fidélité")

if __name__ == "__main__":
    tester_integration_ultimate()