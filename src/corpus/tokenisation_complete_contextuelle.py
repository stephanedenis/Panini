#!/usr/bin/env python3
"""
TOKENISATION COMPLÈTE CONTEXTUELLE - Pipeline v7.1 Enhanced

Amélioration critique de l'Étape 2 : Conservation intégrale de tous les éléments
linguistiques avec étiquetage contextuel précis.

Principe fondamental : RIEN ne doit être perdu, même ce qu'on ne comprend pas encore.
Chaque élément porte potentiellement du sens sémantique crucial.
"""

import re
import time
import json
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import uuid

@dataclass
class ElementLinguistique:
    """Représente un élément linguistique complet avec son contexte"""
    id: str  # UUID unique
    contenu: str  # Le texte exact
    type_element: str  # mot, ponctuation, espace, majuscule, etc.
    position_absolue: int  # Position dans le texte original
    position_relative: int  # Position dans la phrase
    contexte_gauche: str  # 3 éléments précédents
    contexte_droit: str  # 3 éléments suivants
    
    # Métadonnées linguistiques
    langue_detectee: str
    probable_fonction_grammaticale: str
    niveau_certitude: float  # 0.0 à 1.0
    
    # Étiquetage contextuel temporaire
    etiquettes_temporaires: List[str]
    variables_inconnues: Dict[str, Any]
    
    # Contexte de traitement
    locuteur: str
    contexte_situationnel: str
    moment_traitement: str
    version_pipeline: str
    etat_modele: str
    
    # Pour textes traduits
    traducteur_original: str = None
    contexte_traduction: str = None
    moment_traduction: str = None

@dataclass
class ContextePhrase:
    """Contexte complet d'une phrase"""
    phrase_originale: str
    langue: str
    elements: List[ElementLinguistique]
    structure_syntaxique: Dict[str, Any]
    elements_non_compris: List[str]
    hypotheses_semantiques: List[Dict[str, Any]]
    timestamp_analyse: str
    version_analyseur: str

class TokenisateurCompletContextuel:
    """Tokenisateur qui conserve ABSOLUMENT TOUT avec contexte précis"""
    
    def __init__(self):
        self.version = "v7.1-Enhanced"
        self.timestamp_init = datetime.now().isoformat()
        print(f"🔬 Tokenisateur Complet Contextuel {self.version} initialisé")
        print(f"📅 Timestamp: {self.timestamp_init}")
        
        # Patterns pour identifier les types d'éléments
        self.patterns = {
            'ponctuation': r'[.!?;:,()[\]{}"\'`]',
            'espaces': r'\s+',
            'majuscules': r'[A-ZÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞ]',
            'accents': r'[àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ]',
            'apostrophe': r"[''']",
            'tirets': r'[-–—]',
            'guillemets': r'[«»""„]',
            'chiffres': r'\d+',
            'mots': r'\b\w+\b'
        }
    
    def tokeniser_phrase_complete(self, phrase: str, langue: str, 
                                contexte_locuteur: str = "inconnu",
                                contexte_situationnel: str = "analyse_generale",
                                traducteur: str = None) -> ContextePhrase:
        """Tokenisation complète avec conservation intégrale"""
        
        print(f"\n🔍 TOKENISATION COMPLÈTE : '{phrase}'")
        print(f"🌍 Langue: {langue} | 👤 Locuteur: {contexte_locuteur}")
        print("-" * 60)
        
        debut = time.time()
        timestamp_analyse = datetime.now().isoformat()
        
        # Décomposition caractère par caractère d'abord
        elements_bruts = self._decomposer_completement(phrase)
        
        # Reconstruction intelligente avec contexte
        elements_linguistiques = self._analyser_elements_contextuels(
            elements_bruts, phrase, langue, contexte_locuteur, 
            contexte_situationnel, timestamp_analyse, traducteur
        )
        
        # Analyse de structure syntaxique
        structure = self._analyser_structure_syntaxique(elements_linguistiques, langue)
        
        # Identification des éléments non compris
        elements_non_compris = self._identifier_elements_non_compris(elements_linguistiques)
        
        # Génération d'hypothèses sémantiques
        hypotheses = self._generer_hypotheses_semantiques(elements_linguistiques, langue)
        
        contexte_phrase = ContextePhrase(
            phrase_originale=phrase,
            langue=langue,
            elements=elements_linguistiques,
            structure_syntaxique=structure,
            elements_non_compris=elements_non_compris,
            hypotheses_semantiques=hypotheses,
            timestamp_analyse=timestamp_analyse,
            version_analyseur=self.version
        )
        
        temps_total = (time.time() - debut) * 1000
        
        self._afficher_analyse_complete(contexte_phrase, temps_total)
        
        return contexte_phrase
    
    def _decomposer_completement(self, phrase: str) -> List[Tuple[str, int]]:
        """Décompose la phrase en conservant TOUT"""
        elements = []
        position = 0
        
        # Utilisation de regex pour capturer tous les éléments
        pattern_global = r'(\w+|[^\w\s]|\s+)'
        matches = re.finditer(pattern_global, phrase)
        
        for match in matches:
            contenu = match.group()
            pos_debut = match.start()
            elements.append((contenu, pos_debut))
        
        return elements
    
    def _analyser_elements_contextuels(self, elements_bruts: List[Tuple[str, int]], 
                                     phrase: str, langue: str, locuteur: str,
                                     contexte_sit: str, timestamp: str, 
                                     traducteur: str) -> List[ElementLinguistique]:
        """Analyse contextuelle complète de chaque élément"""
        
        elements_linguistiques = []
        
        for i, (contenu, pos_abs) in enumerate(elements_bruts):
            # Génération d'un ID unique
            element_id = str(uuid.uuid4())[:8]
            
            # Détermination du type d'élément
            type_element = self._determiner_type_element(contenu)
            
            # Contexte gauche et droit
            contexte_gauche = self._extraire_contexte_gauche(elements_bruts, i)
            contexte_droit = self._extraire_contexte_droit(elements_bruts, i)
            
            # Analyse de la fonction grammaticale probable
            fonction_gram, certitude = self._analyser_fonction_grammaticale(
                contenu, contexte_gauche, contexte_droit, langue
            )
            
            # Étiquetage temporaire pour éléments non compris
            etiquettes_temp = self._generer_etiquettes_temporaires(
                contenu, type_element, fonction_gram, certitude
            )
            
            # Variables inconnues identifiées
            variables_inconnues = self._identifier_variables_inconnues(
                contenu, contexte_gauche, contexte_droit, langue
            )
            
            # État du modèle au moment du traitement
            etat_modele = self._capturer_etat_modele()
            
            element = ElementLinguistique(
                id=element_id,
                contenu=contenu,
                type_element=type_element,
                position_absolue=pos_abs,
                position_relative=i,
                contexte_gauche=contexte_gauche,
                contexte_droit=contexte_droit,
                langue_detectee=langue,
                probable_fonction_grammaticale=fonction_gram,
                niveau_certitude=certitude,
                etiquettes_temporaires=etiquettes_temp,
                variables_inconnues=variables_inconnues,
                locuteur=locuteur,
                contexte_situationnel=contexte_sit,
                moment_traitement=timestamp,
                version_pipeline=self.version,
                etat_modele=etat_modele,
                traducteur_original=traducteur,
                contexte_traduction=f"analyse_{langue}" if traducteur else None,
                moment_traduction=timestamp if traducteur else None
            )
            
            elements_linguistiques.append(element)
        
        return elements_linguistiques
    
    def _determiner_type_element(self, contenu: str) -> str:
        """Détermine le type précis de l'élément"""
        if re.match(self.patterns['espaces'], contenu):
            return "espace"
        elif re.match(self.patterns['ponctuation'], contenu):
            return "ponctuation"
        elif re.match(self.patterns['chiffres'], contenu):
            return "chiffre"
        elif re.match(self.patterns['mots'], contenu):
            if contenu[0].isupper():
                return "mot_majuscule"
            else:
                return "mot_minuscule"
        elif contenu in ['\'', ''', ''']:
            return "apostrophe"
        else:
            return "element_special"
    
    def _extraire_contexte_gauche(self, elements: List[Tuple[str, int]], position: int) -> str:
        """Extrait le contexte des 3 éléments précédents"""
        debut = max(0, position - 3)
        contexte = [elem[0] for elem in elements[debut:position]]
        return ''.join(contexte)
    
    def _extraire_contexte_droit(self, elements: List[Tuple[str, int]], position: int) -> str:
        """Extrait le contexte des 3 éléments suivants"""
        fin = min(len(elements), position + 4)
        contexte = [elem[0] for elem in elements[position + 1:fin]]
        return ''.join(contexte)
    
    def _analyser_fonction_grammaticale(self, contenu: str, ctx_gauche: str, 
                                      ctx_droit: str, langue: str) -> Tuple[str, float]:
        """Analyse la fonction grammaticale probable"""
        
        # Articles définis/indéfinis
        articles = {
            'fr': ['le', 'la', 'les', 'un', 'une', 'des', 'du', 'de'],
            'en': ['the', 'a', 'an'],
            'de': ['der', 'die', 'das', 'ein', 'eine', 'einen']
        }
        
        # Prépositions communes
        prepositions = {
            'fr': ['de', 'à', 'dans', 'sur', 'avec', 'pour', 'par', 'en'],
            'en': ['of', 'to', 'in', 'on', 'with', 'for', 'by', 'at'],
            'de': ['von', 'zu', 'in', 'auf', 'mit', 'für', 'durch', 'an']
        }
        
        contenu_lower = contenu.lower()
        
        if contenu_lower in articles.get(langue, []):
            return "article", 0.9
        elif contenu_lower in prepositions.get(langue, []):
            return "preposition", 0.9
        elif contenu in ['.', '!', '?']:
            return "ponctuation_finale", 1.0
        elif contenu in [',', ';', ':']:
            return "ponctuation_separation", 1.0
        elif contenu.isupper() and len(contenu) > 1:
            return "nom_propre_probable", 0.7
        elif contenu[0].isupper():
            return "debut_phrase_ou_nom_propre", 0.6
        else:
            return "element_lexical", 0.5
    
    def _generer_etiquettes_temporaires(self, contenu: str, type_elem: str, 
                                      fonction: str, certitude: float) -> List[str]:
        """Génère des étiquettes temporaires pour éléments non compris"""
        etiquettes = []
        
        if certitude < 0.7:
            etiquettes.append("INCERTAIN")
        
        if type_elem == "element_special":
            etiquettes.append("ELEMENT_SPECIAL_NON_CATEGORISE")
        
        if fonction == "element_lexical" and certitude < 0.6:
            etiquettes.append("SEMANTIQUE_A_DETERMINER")
        
        if len(contenu) == 1 and contenu not in ['.', ',', '!', '?', ';', ':']:
            etiquettes.append("CARACTERE_ISOLE_SIGNIFICATION_INCONNUE")
        
        return etiquettes
    
    def _identifier_variables_inconnues(self, contenu: str, ctx_gauche: str, 
                                      ctx_droit: str, langue: str) -> Dict[str, Any]:
        """Identifie les variables inconnues à étudier plus tard"""
        variables = {}
        
        # Choix de casse (majuscule/minuscule)
        if contenu.isalpha():
            variables["choix_casse"] = {
                "casse_originale": contenu,
                "position_phrase": "debut" if not ctx_gauche.strip() else "milieu",
                "justification_inconnue": True
            }
        
        # Choix de ponctuation
        if contenu in ['.', '!', '?']:
            variables["choix_ponctuation_finale"] = {
                "type_choisi": contenu,
                "alternatives_possibles": ['.', '!', '?'],
                "intention_locuteur_inconnue": True
            }
        
        # Mots composés ou apostrophes
        if '\'' in contenu or "'" in contenu:
            variables["contraction_apostrophe"] = {
                "forme_contractee": contenu,
                "forme_complete_possible": "à_determiner",
                "registre_langue": "à_analyser"
            }
        
        return variables
    
    def _capturer_etat_modele(self) -> str:
        """Capture l'état du modèle au moment du traitement"""
        return f"TokenisateurComplet_{self.version}_{self.timestamp_init}"
    
    def _analyser_structure_syntaxique(self, elements: List[ElementLinguistique], 
                                     langue: str) -> Dict[str, Any]:
        """Analyse la structure syntaxique de la phrase"""
        structure = {
            "nombre_elements_total": len(elements),
            "nombre_mots": len([e for e in elements if "mot" in e.type_element]),
            "nombre_ponctuation": len([e for e in elements if e.type_element == "ponctuation"]),
            "nombre_espaces": len([e for e in elements if e.type_element == "espace"]),
            "elements_majuscules": [e.contenu for e in elements if e.type_element == "mot_majuscule"],
            "structure_ponctuation": [e.contenu for e in elements if e.type_element == "ponctuation"],
            "pattern_syntaxique": self._extraire_pattern_syntaxique(elements)
        }
        return structure
    
    def _extraire_pattern_syntaxique(self, elements: List[ElementLinguistique]) -> str:
        """Extrait le pattern syntaxique de la phrase"""
        pattern = []
        for elem in elements:
            if "mot" in elem.type_element:
                pattern.append("M")
            elif elem.type_element == "ponctuation":
                pattern.append("P")
            elif elem.type_element == "espace":
                pattern.append("_")
        return "".join(pattern)
    
    def _identifier_elements_non_compris(self, elements: List[ElementLinguistique]) -> List[str]:
        """Identifie les éléments dont le sens n'est pas encore compris"""
        non_compris = []
        for elem in elements:
            if elem.niveau_certitude < 0.7:
                non_compris.append(f"{elem.contenu} (certitude: {elem.niveau_certitude:.1f})")
        return non_compris
    
    def _generer_hypotheses_semantiques(self, elements: List[ElementLinguistique], 
                                      langue: str) -> List[Dict[str, Any]]:
        """Génère des hypothèses sémantiques pour investigation future"""
        hypotheses = []
        
        # Hypothèse sur l'intention communicative
        ponctuation_finale = [e for e in elements if e.contenu in ['.', '!', '?']]
        if ponctuation_finale:
            type_ponct = ponctuation_finale[-1].contenu
            hypotheses.append({
                "type": "intention_communicative",
                "hypothese": f"Intention {self._interpreter_ponctuation(type_ponct)}",
                "niveau_confiance": 0.8,
                "elements_support": [type_ponct]
            })
        
        # Hypothèse sur le registre de langue
        majuscules = [e for e in elements if e.type_element == "mot_majuscule"]
        if len(majuscules) > 1:
            hypotheses.append({
                "type": "registre_langue",
                "hypothese": "Registre formel possible (plusieurs majuscules)",
                "niveau_confiance": 0.6,
                "elements_support": [e.contenu for e in majuscules]
            })
        
        return hypotheses
    
    def _interpreter_ponctuation(self, ponctuation: str) -> str:
        """Interprète l'intention derrière la ponctuation"""
        interpretations = {
            '.': "déclarative/neutre",
            '!': "exclamative/emphase",
            '?': "interrogative/questionnement"
        }
        return interpretations.get(ponctuation, "inconnue")
    
    def _afficher_analyse_complete(self, contexte: ContextePhrase, temps_ms: float):
        """Affiche l'analyse complète"""
        print(f"\n📊 ANALYSE COMPLÈTE TERMINÉE")
        print(f"⏱️ Temps: {temps_ms:.2f}ms")
        print(f"🔢 Éléments analysés: {len(contexte.elements)}")
        print(f"📈 Structure: {contexte.structure_syntaxique['pattern_syntaxique']}")
        
        print(f"\n🔍 ÉLÉMENTS DÉTAILLÉS:")
        for i, elem in enumerate(contexte.elements):
            print(f"  {i+1:2d}. '{elem.contenu}' [{elem.type_element}] "
                  f"({elem.probable_fonction_grammaticale}, {elem.niveau_certitude:.1f})")
            if elem.etiquettes_temporaires:
                print(f"      🏷️ Étiquettes: {', '.join(elem.etiquettes_temporaires)}")
            if elem.variables_inconnues:
                print(f"      ❓ Variables: {len(elem.variables_inconnues)} inconnues")
        
        if contexte.elements_non_compris:
            print(f"\n⚠️ ÉLÉMENTS NON COMPRIS:")
            for elem in contexte.elements_non_compris:
                print(f"   • {elem}")
        
        if contexte.hypotheses_semantiques:
            print(f"\n💡 HYPOTHÈSES SÉMANTIQUES:")
            for hyp in contexte.hypotheses_semantiques:
                print(f"   • {hyp['type']}: {hyp['hypothese']} (confiance: {hyp['niveau_confiance']:.1f})")


def test_tokenisation_complete():
    """Test de la tokenisation complète"""
    print("🧪 TEST DE TOKENISATION COMPLÈTE CONTEXTUELLE")
    print("=" * 80)
    
    tokenisateur = TokenisateurCompletContextuel()
    
    # Test avec les exemples précédents
    phrases_test = [
        ("Un lièvre se moquait d'une tortue.", "fr", "Ésope", "fable_classique", None),
        ("The hare mocked the tortoise.", "en", "Aesop", "classic_fable", "traducteur_anonyme"),
        ("Il était une fois une reine.", "fr", "conteur_traditionnel", "conte_oral", None),
        ("Dr. Smith's cat—what a story!", "en", "narrateur_moderne", "anecdote_informelle", None)
    ]
    
    for phrase, langue, locuteur, contexte, traducteur in phrases_test:
        print(f"\n" + "="*60)
        contexte_analyse = tokenisateur.tokeniser_phrase_complete(
            phrase, langue, locuteur, contexte, traducteur
        )
        
        # Sauvegarde de l'analyse pour traçabilité future
        nom_fichier = f"analyse_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{langue}.json"
        with open(nom_fichier, 'w', encoding='utf-8') as f:
            # Conversion en dictionnaire pour sérialisation
            contexte_dict = asdict(contexte_analyse)
            json.dump(contexte_dict, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Analyse sauvegardée: {nom_fichier}")


if __name__ == "__main__":
    test_tokenisation_complete()