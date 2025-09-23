#!/usr/bin/env python3
"""
ANALYSEUR DE MOLÉCULES SÉMANTIQUES CONTEXTUELLES
===============================================

Décompose tout mot non-atomique en molécules dhātu et capture
toutes les interprétations possibles selon le contexte.

Approche : Analyse compositionnelle + contexte + ambiguïtés préservées
"""

import json
import re
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class InterpretationContextuelle:
    """Une interprétation possible d'un mot selon le contexte."""
    interpretation_id: str
    contexte: str
    dhatu_constituants: List[str]
    force_semantique: float
    evidences: List[str]  # Preuves contextuelles
    ambiguites: List[str]  # Ambiguïtés détectées

@dataclass
class MoleculeSemantiqueComplete:
    """Molécule sémantique complète avec toutes ses interprétations."""
    mot_source: str
    langue: str
    interpretations_possibles: List[InterpretationContextuelle]
    dhatu_principaux: List[str]
    niveau_complexite: int  # 1=quasi-atomique, 5=très complexe
    patterns_cross_linguistiques: Dict[str, str]

class AnalyseurMoleculesSemantiquesConte:
    """Analyseur spécialisé pour les molécules sémantiques des contes."""
    
    def __init__(self):
        self.dhatu_atomiques = {
            'EXIST': 'existence, être, présence ontologique',
            'COMM': 'communication, expression, transmission',
            'TRANS': 'transformation, changement d\'état',
            'DECIDE': 'décision, choix, volition',
            'EVAL': 'évaluation, jugement, appréciation',
            'GROUP': 'relation, association, groupement',
            'ITER': 'répétition, itération, cyclicité',
            'LOCATE': 'localisation, position, direction',
            'SEQ': 'séquence, ordre, progression'
        }
        
        self.molecules_analysees = {}
        self.patterns_compositionnels = {}
        self.contextes_narratifs = {}
        
        self._initialiser_patterns_compositionnels()
        self._initialiser_contextes_narratifs()
    
    def _initialiser_patterns_compositionnels(self):
        """Initialise les patterns de composition sémantique."""
        
        # Patterns verbo-nominaux
        self.patterns_compositionnels['verbo_nominal'] = {
            'fr': {
                'se_moquait': ['EVAL', 'COMM', 'TRANS'],  # évaluation + communication + action
                'travaillait': ['TRANS', 'ITER', 'EXIST'],  # transformation + répétition + être
                'collectait': ['TRANS', 'GROUP', 'ITER'],  # transformation + groupement + répétition
                'cousait': ['TRANS', 'ITER', 'LOCATE'],  # transformation + répétition + localisation
                'verspottete': ['EVAL', 'COMM', 'TRANS'],  # (même pattern cross-linguistique)
                'arbeitete': ['TRANS', 'ITER', 'EXIST'],
                'sammelte': ['TRANS', 'GROUP', 'ITER']
            },
            'en': {
                'mocked': ['EVAL', 'COMM', 'TRANS'],
                'worked': ['TRANS', 'ITER', 'EXIST'],
                'collected': ['TRANS', 'GROUP', 'ITER'],
                'sewing': ['TRANS', 'ITER', 'LOCATE']
            },
            'de': {
                'verspottete': ['EVAL', 'COMM', 'TRANS'],
                'arbeitete': ['TRANS', 'ITER', 'EXIST'],
                'sammelte': ['TRANS', 'GROUP', 'ITER'],
                'nähte': ['TRANS', 'ITER', 'LOCATE']
            }
        }
        
        # Patterns adverbiaux complexes
        self.patterns_compositionnels['adverbial_complexe'] = {
            'fr': {
                'lentement_mais_sûrement': ['EVAL', 'SEQ', 'DECIDE'],  # manière + progression + certitude
                'très_vite': ['EVAL', 'TRANS'],  # intensité + rapidité
                'calmement': ['EVAL', 'EXIST'],  # manière + état
                'dur_pour': ['EVAL', 'TRANS']  # difficulté + finalité
            },
            'en': {
                'slowly_but_surely': ['EVAL', 'SEQ', 'DECIDE'],
                'very_fast': ['EVAL', 'TRANS'],
                'calmly': ['EVAL', 'EXIST'],
                'hard_to': ['EVAL', 'TRANS']
            },
            'de': {
                'langsam_aber_sicher': ['EVAL', 'SEQ', 'DECIDE'],
                'sehr_schnell': ['EVAL', 'TRANS'],
                'ruhig': ['EVAL', 'EXIST'],
                'hart_um': ['EVAL', 'TRANS']
            }
        }
        
        # Patterns causaux
        self.patterns_compositionnels['causal'] = {
            'fr': {
                'à_cause_de_sa_lenteur': ['EVAL', 'TRANS', 'LOCATE'],  # jugement + causation + attribution
                'pour_l\'hiver': ['TRANS', 'LOCATE', 'SEQ'],  # finalité + temps + séquence
                'contre_toi': ['EVAL', 'LOCATE', 'GROUP']  # opposition + direction + relation
            },
            'en': {
                'because_of_its_slowness': ['EVAL', 'TRANS', 'LOCATE'],
                'for_winter': ['TRANS', 'LOCATE', 'SEQ'],
                'against_you': ['EVAL', 'LOCATE', 'GROUP']
            },
            'de': {
                'wegen_ihrer_langsamkeit': ['EVAL', 'TRANS', 'LOCATE'],
                'für_den_winter': ['TRANS', 'LOCATE', 'SEQ'],
                'gegen_dich': ['EVAL', 'LOCATE', 'GROUP']
            }
        }
    
    def _initialiser_contextes_narratifs(self):
        """Initialise les contextes narratifs spécialisés."""
        
        self.contextes_narratifs = {
            'ouverture_conte': {
                'marqueurs': ['il était une fois', 'once upon a time', 'es war einmal'],
                'dhatu_dominants': ['EVID_NARR', 'SEQ', 'LOCATE'],
                'interpretations_privilegiees': ['narratif_traditionnel', 'temporalite_mythique']
            },
            'dialogue_direct': {
                'marqueurs': ['"', '«', '»', 'dit', 'said', 'sagte'],
                'dhatu_dominants': ['COMM', 'EXIST', 'EVAL'],
                'interpretations_privilegiees': ['parole_directe', 'subjectivite']
            },
            'action_durative': {
                'marqueurs': ['était en train', 'was', 'war dabei'],
                'dhatu_dominants': ['TRANS', 'ITER', 'EXIST'],
                'interpretations_privilegiees': ['processus_en_cours', 'durativite']
            },
            'evaluation_qualitative': {
                'marqueurs': ['si', 'so', 'très', 'very', 'sehr'],
                'dhatu_dominants': ['EVAL', 'TRANS'],
                'interpretations_privilegiees': ['intensite', 'qualification']
            },
            'relation_causale': {
                'marqueurs': ['à cause de', 'because of', 'wegen'],
                'dhatu_dominants': ['EVAL', 'TRANS', 'LOCATE'],
                'interpretations_privilegiees': ['causalite', 'attribution']
            }
        }
    
    def analyser_mot_nouveau(self, mot: str, contexte_phrase: str, langue: str) -> MoleculeSemantiqueComplete:
        """Analyse un mot nouveau pour créer sa molécule sémantique."""
        
        logger.info(f"🔬 Analyse molécule: '{mot}' (contexte: '{contexte_phrase[:50]}...')")
        
        # 1. Détection du contexte narratif
        contexte_detecte = self._detecter_contexte_narratif(contexte_phrase)
        
        # 2. Analyse compositionnelle du mot
        interpretations = self._generer_interpretations_compositionnelles(mot, contexte_detecte, langue)
        
        # 3. Analyse cross-linguistique
        patterns_cross = self._analyser_patterns_cross_linguistiques(mot, langue)
        
        # 4. Évaluation de la complexité
        niveau_complexite = self._evaluer_complexite_semantique(mot, interpretations)
        
        # 5. Extraction dhātu principaux
        dhatu_principaux = self._extraire_dhatu_principaux(interpretations)
        
        molecule = MoleculeSemantiqueComplete(
            mot_source=mot,
            langue=langue,
            interpretations_possibles=interpretations,
            dhatu_principaux=dhatu_principaux,
            niveau_complexite=niveau_complexite,
            patterns_cross_linguistiques=patterns_cross
        )
        
        # Cache pour réutilisation
        self.molecules_analysees[f"{mot}_{langue}"] = molecule
        
        return molecule
    
    def _detecter_contexte_narratif(self, phrase: str) -> str:
        """Détecte le contexte narratif principal de la phrase."""
        
        phrase_lower = phrase.lower()
        
        # Recherche par priorité
        for contexte, details in self.contextes_narratifs.items():
            for marqueur in details['marqueurs']:
                if marqueur in phrase_lower:
                    return contexte
        
        # Contexte par défaut
        return 'narratif_general'
    
    def _generer_interpretations_compositionnelles(self, mot: str, contexte: str, langue: str) -> List[InterpretationContextuelle]:
        """Génère toutes les interprétations compositionnelles possibles."""
        
        interpretations = []
        
        # 1. Recherche dans patterns compositionnels
        for categorie, patterns_langue in self.patterns_compositionnels.items():
            if langue in patterns_langue and mot in patterns_langue[langue]:
                dhatu_constituants = patterns_langue[langue][mot]
                
                interpretation = InterpretationContextuelle(
                    interpretation_id=f"{categorie}_{mot}",
                    contexte=contexte,
                    dhatu_constituants=dhatu_constituants,
                    force_semantique=0.9,  # Forte pour patterns connus
                    evidences=[f"pattern_{categorie}", f"contexte_{contexte}"],
                    ambiguites=[]
                )
                interpretations.append(interpretation)
        
        # 2. Analyse morphologique pour mots inconnus
        if not interpretations:
            interpretations.extend(self._analyser_morphologiquement(mot, contexte, langue))
        
        # 3. Interprétations contextuelles spécialisées
        if contexte in self.contextes_narratifs:
            contexte_info = self.contextes_narratifs[contexte]
            
            # Interprétation biaisée par le contexte
            interpretation_contextuelle = InterpretationContextuelle(
                interpretation_id=f"contextuel_{contexte}_{mot}",
                contexte=contexte,
                dhatu_constituants=contexte_info['dhatu_dominants'],
                force_semantique=0.7,
                evidences=[f"contexte_narratif_{contexte}"],
                ambiguites=[f"interpretation_biaisee_par_{contexte}"]
            )
            interpretations.append(interpretation_contextuelle)
        
        return interpretations
    
    def _analyser_morphologiquement(self, mot: str, contexte: str, langue: str) -> List[InterpretationContextuelle]:
        """Analyse morphologique pour décomposer un mot inconnu."""
        
        interpretations = []
        
        # Patterns morphologiques par langue
        patterns_morpho = {
            'fr': {
                # Suffixes verbaux
                r'.*ait$': ['TRANS', 'ITER', 'EXIST'],  # imparfait
                r'.*ent$': ['TRANS', 'EXIST'],  # présent 3e pluriel
                r'.*er$': ['TRANS'],  # infinitif
                # Suffixes nominaux
                r'.*eur$': ['EVAL', 'EXIST'],  # agent/qualité
                r'.*ment$': ['EVAL', 'TRANS'],  # adverbe de manière
                r'.*tion$': ['TRANS', 'GROUP']  # action/résultat
            },
            'en': {
                r'.*ing$': ['TRANS', 'ITER'],  # progressive
                r'.*ed$': ['TRANS', 'EXIST'],  # passé
                r'.*ly$': ['EVAL', 'TRANS'],  # adverbe
                r'.*ness$': ['EVAL', 'EXIST'],  # qualité
                r'.*tion$': ['TRANS', 'GROUP']
            },
            'de': {
                r'.*te$': ['TRANS', 'ITER', 'EXIST'],  # prétérit
                r'.*en$': ['TRANS', 'EXIST'],  # infinitif/pluriel
                r'.*heit$': ['EVAL', 'EXIST'],  # qualité abstraite
                r'.*keit$': ['EVAL', 'EXIST'],  # possibilité/qualité
                r'.*ung$': ['TRANS', 'GROUP']  # action/résultat
            }
        }
        
        if langue in patterns_morpho:
            for pattern, dhatu_probable in patterns_morpho[langue].items():
                if re.match(pattern, mot):
                    interpretation = InterpretationContextuelle(
                        interpretation_id=f"morpho_{pattern}_{mot}",
                        contexte=contexte,
                        dhatu_constituants=dhatu_probable,
                        force_semantique=0.6,  # Moyenne pour analyse morpho
                        evidences=[f"pattern_morphologique_{pattern}"],
                        ambiguites=[f"analyse_morpho_ambigue_{pattern}"]
                    )
                    interpretations.append(interpretation)
        
        # Si aucun pattern trouvé, interprétation générique
        if not interpretations:
            interpretation_generique = InterpretationContextuelle(
                interpretation_id=f"generique_{mot}",
                contexte=contexte,
                dhatu_constituants=['EXIST', 'TRANS'],  # Dhātu les plus probables
                force_semantique=0.3,  # Faible pour générique
                evidences=['analyse_generique'],
                ambiguites=['interpretation_incertaine', 'dhatu_non_confirmes']
            )
            interpretations.append(interpretation_generique)
        
        return interpretations
    
    def _analyser_patterns_cross_linguistiques(self, mot: str, langue_source: str) -> Dict[str, str]:
        """Analyse les patterns cross-linguistiques pour trouver équivalents."""
        
        patterns_cross = {}
        
        # Recherche dans tous les patterns compositionnels
        for categorie, patterns_par_langue in self.patterns_compositionnels.items():
            if langue_source in patterns_par_langue:
                if mot in patterns_par_langue[langue_source]:
                    # Chercher équivalents dans autres langues
                    dhatu_mot = patterns_par_langue[langue_source][mot]
                    
                    for autre_langue, patterns_langue in patterns_par_langue.items():
                        if autre_langue != langue_source:
                            for autre_mot, dhatu_autre in patterns_langue.items():
                                if dhatu_autre == dhatu_mot:  # Même composition dhātu
                                    patterns_cross[autre_langue] = autre_mot
        
        return patterns_cross
    
    def _evaluer_complexite_semantique(self, mot: str, interpretations: List[InterpretationContextuelle]) -> int:
        """Évalue le niveau de complexité sémantique (1-5)."""
        
        # Facteurs de complexité
        nb_interpretations = len(interpretations)
        nb_ambiguites = sum(len(interp.ambiguites) for interp in interpretations)
        nb_dhatu_moyen = sum(len(interp.dhatu_constituants) for interp in interpretations) / max(1, nb_interpretations)
        
        # Calcul score complexité
        score_complexite = 1
        
        if nb_interpretations > 3:
            score_complexite += 1
        if nb_ambiguites > 2:
            score_complexite += 1
        if nb_dhatu_moyen > 2:
            score_complexite += 1
        if len(mot) > 10:  # Mots longs souvent plus complexes
            score_complexite += 1
        
        return min(5, score_complexite)
    
    def _extraire_dhatu_principaux(self, interpretations: List[InterpretationContextuelle]) -> List[str]:
        """Extrait les dhātu principaux par fréquence pondérée."""
        
        dhatu_scores = defaultdict(float)
        
        for interpretation in interpretations:
            poids = interpretation.force_semantique
            for dhatu in interpretation.dhatu_constituants:
                dhatu_scores[dhatu] += poids
        
        # Tri par score décroissant
        dhatu_tries = sorted(dhatu_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Retour des dhātu principaux (score > moyenne)
        if dhatu_tries:
            score_moyen = sum(score for _, score in dhatu_tries) / len(dhatu_tries)
            dhatu_principaux = [dhatu for dhatu, score in dhatu_tries if score >= score_moyen]
            return dhatu_principaux[:5]  # Maximum 5 dhātu principaux
        
        return []
    
    def analyser_phrase_complete(self, phrase: str, langue: str) -> Dict[str, MoleculeSemantiqueComplete]:
        """Analyse tous les mots d'une phrase pour créer les molécules."""
        
        logger.info(f"🧪 Analyse phrase complète: '{phrase}'")
        
        molecules_phrase = {}
        
        # Nettoyage et tokenisation
        mots = re.findall(r'\w+', phrase.lower())
        
        for mot in mots:
            if len(mot) > 2:  # Ignorer mots très courts
                molecule = self.analyser_mot_nouveau(mot, phrase, langue)
                molecules_phrase[mot] = molecule
        
        return molecules_phrase
    
    def generer_rapport_molecules(self, molecules: Dict[str, MoleculeSemantiqueComplete]) -> str:
        """Génère un rapport détaillé des molécules analysées."""
        
        rapport = f"""
🧬 RAPPORT D'ANALYSE MOLÉCULES SÉMANTIQUES
=========================================

📊 STATISTIQUES:
   • Molécules analysées: {len(molecules)}
   • Complexité moyenne: {sum(m.niveau_complexite for m in molecules.values()) / len(molecules):.1f}
   • Dhātu uniques utilisés: {len(set().union(*[m.dhatu_principaux for m in molecules.values()]))}

🔬 ANALYSE DÉTAILLÉE:
"""
        
        for mot, molecule in molecules.items():
            rapport += f"\n📝 MOT: '{mot}' (Complexité: {molecule.niveau_complexite}/5)"
            rapport += f"\n   Dhātu principaux: {', '.join(molecule.dhatu_principaux)}"
            rapport += f"\n   Patterns cross-linguistiques: {molecule.patterns_cross_linguistiques}"
            
            for i, interp in enumerate(molecule.interpretations_possibles, 1):
                rapport += f"\n   🎯 Interprétation {i}: {interp.interpretation_id}"
                rapport += f"\n      Contexte: {interp.contexte}"
                rapport += f"\n      Dhātu: {interp.dhatu_constituants}"
                rapport += f"\n      Force: {interp.force_semantique:.2f}"
                if interp.ambiguites:
                    rapport += f"\n      ⚠️ Ambiguïtés: {', '.join(interp.ambiguites)}"
        
        return rapport

def tester_analyseur_conte():
    """Test de l'analyseur sur des extraits de contes."""
    
    print("🧬 TEST ANALYSEUR MOLÉCULES SÉMANTIQUES")
    print("=" * 50)
    
    analyseur = AnalyseurMoleculesSemantiquesConte()
    
    # Phrases test avec mots complexes
    phrases_test = [
        ("Un lièvre se moquait d'une tortue à cause de sa lenteur.", "fr"),
        ("The hare worked hard to collect food for winter.", "en"),
        ("Die Königin nähte am Fenster während des Winters.", "de")
    ]
    
    toutes_molecules = {}
    
    for phrase, langue in phrases_test:
        print(f"\n🔍 Analyse: {phrase}")
        molecules = analyseur.analyser_phrase_complete(phrase, langue)
        toutes_molecules.update(molecules)
    
    # Rapport complet
    rapport = analyseur.generer_rapport_molecules(toutes_molecules)
    print(rapport)
    
    # Sauvegarde
    resultats = {
        'molecules_analysees': {mot: asdict(mol) for mot, mol in toutes_molecules.items()},
        'statistiques': {
            'total_molecules': len(toutes_molecules),
            'complexite_moyenne': sum(m.niveau_complexite for m in toutes_molecules.values()) / len(toutes_molecules),
            'dhatu_utilises': list(set().union(*[m.dhatu_principaux for m in toutes_molecules.values()]))
        }
    }
    
    with open('analyse_molecules_semantiques_conte.json', 'w', encoding='utf-8') as f:
        json.dump(resultats, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Résultats sauvegardés: analyse_molecules_semantiques_conte.json")

if __name__ == "__main__":
    tester_analyseur_conte()