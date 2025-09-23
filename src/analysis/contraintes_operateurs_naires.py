#!/usr/bin/env python3
"""
⚖️ CONTRAINTES ET LIMITATIONS : USAGE RAISONNÉ DES OPÉRATEURS N-AIRES
Principe de parcimonie cognitive et validation empirique des applications
"""

import json
from dataclasses import dataclass
from typing import List, Dict, Set
from enum import Enum

class NiveauComplexite(Enum):
    """Niveaux de complexité cognitive tolérables"""
    BASIQUE = 1      # Binaire simple (∅, +)
    MODERE = 2       # Trinaire justifié (!, ?, +)
    AVANCE = 3       # Quaternaire spécialisé
    EXPERT = 4       # Quinaire/hexaire domaines pointus
    EXPERIMENTAL = 5 # Au-delà - recherche uniquement

class DomaineApplication(Enum):
    """Domaines d'application avec contraintes spécifiques"""
    LEXIQUE_COURANT = "lexique_courant"
    MODALITE_EPISTÉMIQUE = "modalite_epistemique"  
    ASPECT_TEMPOREL = "aspect_temporel"
    INTENSITE_GRADUELLE = "intensite_graduelle"
    DISTRIBUTION_SPATIALE = "distribution_spatiale"
    METAPHORE_FIGUREE = "metaphore_figuree"

@dataclass
class ContrainteUsage:
    """Contrainte d'usage pour opérateurs n-aires"""
    domaine: DomaineApplication
    niveau_max: NiveauComplexite
    justification_cognitive: str
    validation_empirique: bool
    exemples_valides: List[str]
    contre_exemples: List[str]

class ValidateurOperateursNaires:
    """Validateur rigoureux des opérateurs n-aires"""
    
    def __init__(self):
        self.contraintes = self._definir_contraintes_rigoureuses()
        self.limites_cognitives = self._etablir_limites_cognitives()
        
    def _definir_contraintes_rigoureuses(self):
        """Définir contraintes d'usage rigoureuses par domaine"""
        return {
            DomaineApplication.LEXIQUE_COURANT: ContrainteUsage(
                domaine=DomaineApplication.LEXIQUE_COURANT,
                niveau_max=NiveauComplexite.MODERE,  # MAX trinaire !
                justification_cognitive="Charge cognitive limitée pour usage quotidien",
                validation_empirique=True,
                exemples_valides=[
                    "intensifier → INTENSE+ (basique)",
                    "atténuer → INTENSE! (négation justifiée)",
                    "peut-être_intensifier → INTENSE? (modalité courante)"
                ],
                contre_exemples=[
                    "INTENSE++++ (trop granulaire pour usage courant)",
                    "INTENSE[2.847] (précision excessive)",
                    "INTENSE@duratif<possible>#futur (surcharge cognitive)"
                ]
            ),
            
            DomaineApplication.MODALITE_EPISTÉMIQUE: ContrainteUsage(
                domaine=DomaineApplication.MODALITE_EPISTÉMIQUE,
                niveau_max=NiveauComplexite.AVANCE,  # Quinaire justifié
                justification_cognitive="Modalité épistémique naturellement graduée (impossible→certain)",
                validation_empirique=True,
                exemples_valides=[
                    "impossible → MODAL!! (négation forte)",
                    "improbable → MODAL!· (négation faible)",
                    "possible → MODAL? (neutre)",
                    "probable → MODAL?+ (affirmation faible)", 
                    "certain → MODAL++ (affirmation forte)"
                ],
                contre_exemples=[
                    "MODAL+++++ (trop de gradations)",
                    "MODAL[π] (quantification non-cognitive)"
                ]
            ),
            
            DomaineApplication.ASPECT_TEMPOREL: ContrainteUsage(
                domaine=DomaineApplication.ASPECT_TEMPOREL,
                niveau_max=NiveauComplexite.EXPERT,  # Hexaire spécialisé
                justification_cognitive="Aspects temporels bien établis linguistiquement",
                validation_empirique=True,
                exemples_valides=[
                    "commencer → TRANS→+ (inceptif)",
                    "continuer → TRANS→ (progressif)",
                    "durer → TRANS═ (duratif)",
                    "aboutir → TRANS→· (résultatif)",
                    "finir → TRANS→∅ (terminatif)",
                    "répéter → TRANS↻ (itératif)"
                ],
                contre_exemples=[
                    "TRANS→→→+ (complexification inutile)",
                    "TRANS∿∿∿ (symboles non-cognitifs)"
                ]
            ),
            
            DomaineApplication.INTENSITE_GRADUELLE: ContrainteUsage(
                domaine=DomaineApplication.INTENSITE_GRADUELLE,
                niveau_max=NiveauComplexite.AVANCE,  # Quaternaire max
                justification_cognitive="Limitation cognitive ~7±2 distinctions",
                validation_empirique=True,
                exemples_valides=[
                    "légèrement → INTENSE+· (faible)",
                    "modérément → INTENSE+ (moyen)",
                    "fortement → INTENSE++ (fort)",
                    "extrêmement → INTENSE+++ (extrême)"
                ],
                contre_exemples=[
                    "INTENSE+++++++ (dépassement cognitif)",
                    "INTENSE[2.718281828] (fausse précision)"
                ]
            ),
            
            DomaineApplication.DISTRIBUTION_SPATIALE: ContrainteUsage(
                domaine=DomaineApplication.DISTRIBUTION_SPATIALE,
                niveau_max=NiveauComplexite.MODERE,  # Trinaire suffit
                justification_cognitive="Distinction spatial simple : local/distribué/universel",
                validation_empirique=False,  # À valider
                exemples_valides=[
                    "ici → LOCATE+ (local)",
                    "partout → LOCATE++ (distribué)", 
                    "universellement → LOCATE+++ (universel)"
                ],
                contre_exemples=[
                    "LOCATE++++++++ (granularité excessive)"
                ]
            )
        }
    
    def _etablir_limites_cognitives(self):
        """Établir limites cognitives basées sur littérature"""
        return {
            "memoire_travail": {
                "limite": "7±2 éléments (Miller 1956)",
                "application": "Max 7 niveaux d'opérateurs",
                "consequence": "Hexaire = limite absolue"
            },
            "charge_cognitive": {
                "limite": "Complexité perçue vs utilité",
                "application": "Trinaire pour usage courant",
                "consequence": "N-aires > 3 pour spécialistes uniquement"
            },
            "realite_linguistique": {
                "limite": "Distinctions attestées dans langues naturelles",
                "application": "Validation cross-linguistique obligatoire",
                "consequence": "Innovations doivent être motivées empiriquement"
            },
            "principle_parcimonie": {
                "limite": "Rasoir d'Ockham cognitif",
                "application": "Minimum de complexité pour maximum d'expressivité",
                "consequence": "Justification systématique de chaque niveau"
            }
        }
    
    def valider_usage(self, expression: str, dhatu_representation: str, domaine: DomaineApplication):
        """Valider l'usage d'une représentation dhātu n-aire"""
        print(f"🔍 VALIDATION : '{expression}' → {dhatu_representation}")
        
        if domaine not in self.contraintes:
            return self._refuser("Domaine non reconnu")
        
        contrainte = self.contraintes[domaine]
        
        # Analyse de complexité
        complexite = self._analyser_complexite(dhatu_representation)
        print(f"   📊 Complexité détectée : {complexite.name}")
        
        # Vérification niveau maximum
        if complexite.value > contrainte.niveau_max.value:
            return self._refuser(f"Dépasse niveau max {contrainte.niveau_max.name} pour domaine {domaine.value}")
        
        # Vérification validation empirique
        if not contrainte.validation_empirique and complexite.value > NiveauComplexite.MODERE.value:
            return self._refuser("Domaine non validé empiriquement pour niveau avancé")
        
        # Vérification contre-exemples
        for contre_exemple in contrainte.contre_exemples:
            if self._similarite_representation(dhatu_representation, contre_exemple) > 0.7:
                return self._refuser(f"Similaire à contre-exemple : {contre_exemple}")
        
        return self._approuver(contrainte.justification_cognitive)
    
    def _analyser_complexite(self, representation: str) -> NiveauComplexite:
        """Analyser la complexité d'une représentation dhātu"""
        
        # Compter opérateurs spéciaux
        operateurs_complexes = ["+++++", "++++", "+++", "!!", "→", "═", "↻", "?+", "!·"]
        operateurs_detectes = sum(1 for op in operateurs_complexes if op in representation)
        
        # Compter paramètres additionnels  
        parametres = representation.count("[") + representation.count("<") + representation.count("@")
        
        # Évaluer complexité totale
        score_complexite = operateurs_detectes + parametres * 2
        
        if score_complexite == 0:
            return NiveauComplexite.BASIQUE
        elif score_complexite <= 2:
            return NiveauComplexite.MODERE  
        elif score_complexite <= 4:
            return NiveauComplexite.AVANCE
        elif score_complexite <= 6:
            return NiveauComplexite.EXPERT
        else:
            return NiveauComplexite.EXPERIMENTAL
    
    def _similarite_representation(self, repr1: str, repr2: str) -> float:
        """Calculer similarité entre représentations"""
        # Similarité simple basée sur caractères communs
        chars1 = set(repr1.replace(" ", ""))
        chars2 = set(repr2.replace(" ", ""))
        if not chars1 and not chars2:
            return 1.0
        intersection = len(chars1.intersection(chars2))
        union = len(chars1.union(chars2))
        return intersection / union if union > 0 else 0.0
    
    def _refuser(self, raison: str):
        """Refuser usage avec raison"""
        return {
            "statut": "REFUSÉ",
            "raison": raison,
            "recommendation": "Simplifier ou changer de domaine"
        }
    
    def _approuver(self, justification: str):
        """Approuver usage avec justification"""
        return {
            "statut": "APPROUVÉ",
            "justification": justification,
            "recommendation": "Usage valide"
        }
    
    def generer_guide_bonnes_pratiques(self):
        """Générer guide des bonnes pratiques"""
        print("📋 GUIDE DES BONNES PRATIQUES - OPÉRATEURS N-AIRES")
        print("="*65)
        
        print("\n🎯 PRINCIPE DIRECTEUR : PARCIMONIE COGNITIVE")
        print("   'La complexité minimale pour l'expressivité maximale'")
        
        print("\n📊 NIVEAUX D'USAGE RECOMMANDÉS")
        print("-"*40)
        
        recommandations = {
            "Usage quotidien (TAL grand public)": {
                "niveau": "BASIQUE → MODÉRÉ (binaire/trinaire)",
                "exemples": ["présent (+)", "absent (∅)", "négatif (!)"],
                "justification": "Charge cognitive minimale"
            },
            "Applications spécialisées (linguistique)": {
                "niveau": "MODÉRÉ → AVANCÉ (trinaire/quaternaire)",
                "exemples": ["modalité épistémique", "intensité graduée"],
                "justification": "Expertise justifie complexité"
            },
            "Recherche expérimentale": {
                "niveau": "AVANCÉ → EXPERT (quaternaire/hexaire)",
                "exemples": ["aspects temporels fins", "distributions complexes"],
                "justification": "Innovation contrôlée"
            },
            "Développement algorithmique": {
                "niveau": "EXPERT uniquement (hexaire+)",
                "exemples": ["optimisation interne", "représentations transitoires"],
                "justification": "Usage non-humain"
            }
        }
        
        for contexte, info in recommandations.items():
            print(f"\n🔍 {contexte}")
            print(f"   Niveau: {info['niveau']}")
            print(f"   Exemples: {', '.join(info['exemples'])}")
            print(f"   Justification: {info['justification']}")
        
        print(f"\n⚠️ SIGNAUX D'ALARME (usage abusif)")
        print("-"*45)
        
        signaux_alarme = [
            "Plus de 7 distinctions pour un seul dhātu",
            "Quantification numérique excessive (ex: [2.71828])",
            "Symboles non-cognitifs (ex: ∿∿∿, ◊◊◊)",
            "Combinaisons sans justification linguistique",
            "Usage quaternaire+ pour lexique courant",
            "Notation incompréhensible par expert humain"
        ]
        
        for signal in signaux_alarme:
            print(f"   🚨 {signal}")
        
        print(f"\n✅ CRITÈRES DE VALIDATION OBLIGATOIRES")
        print("-"*45)
        
        criteres = [
            "Justification cognitive (littérature psycholinguistique)",
            "Validation empirique (corpus, expériences)",
            "Attestation cross-linguistique (au moins 3 langues)",
            "Utilité vs complexité (analyse coût/bénéfice)",
            "Compréhensibilité expert (test utilisateur)",
            "Robustesse computationnelle (implémentation stable)"
        ]
        
        for critere in criteres:
            print(f"   ✓ {critere}")
        
        return {
            "recommandations": recommandations,
            "signaux_alarme": signaux_alarme,
            "criteres_validation": criteres
        }
    
    def tester_cas_limites(self):
        """Tester des cas limites d'usage"""
        print("\n🧪 TESTS DE CAS LIMITES")
        print("="*30)
        
        cas_tests = [
            # Cas valides
            ("intensifier", "INTENSE+", DomaineApplication.LEXIQUE_COURANT),
            ("atténuer", "INTENSE!", DomaineApplication.LEXIQUE_COURANT), 
            ("probablement", "MODAL?+", DomaineApplication.MODALITE_EPISTÉMIQUE),
            ("commencer", "TRANS→+", DomaineApplication.ASPECT_TEMPOREL),
            
            # Cas invalides
            ("super-mega-intensifier", "INTENSE+++++++", DomaineApplication.LEXIQUE_COURANT),
            ("précisément_π_fois", "QUANT[3.14159]", DomaineApplication.INTENSITE_GRADUELLE),
            ("bizarrement", "EVAL∿∿∿<alien>@impossible", DomaineApplication.LEXIQUE_COURANT),
        ]
        
        resultats = []
        for expression, representation, domaine in cas_tests:
            resultat = self.valider_usage(expression, representation, domaine)
            resultats.append((expression, representation, resultat))
            print(f"   {resultat['statut']}: {resultat.get('raison', resultat.get('justification', ''))}")
        
        return resultats

def main():
    """Démonstration complète des contraintes d'usage"""
    validateur = ValidateurOperateursNaires()
    
    print("⚖️ CONTRAINTES ET LIMITATIONS : USAGE RAISONNÉ DES OPÉRATEURS N-AIRES")
    print("="*75)
    
    # Guide des bonnes pratiques
    guide = validateur.generer_guide_bonnes_pratiques()
    
    # Tests de validation
    resultats = validateur.tester_cas_limites()
    
    print(f"\n🎯 CONCLUSION : INNOVATION CONTRÔLÉE")
    print("="*40)
    print("Les opérateurs n-aires sont révolutionnaires MAIS :")
    print("   ✅ Doivent respecter contraintes cognitives")
    print("   ✅ Nécessitent validation empirique")  
    print("   ✅ Usage gradué selon expertise")
    print("   ✅ Principe parcimonie > complexification")
    print("   → INNOVATION RESPONSABLE ET SCIENTIFIQUE")
    
    # Sauvegarde résultats
    synthese = {
        "principe": "Parcimonie cognitive",
        "contraintes_par_domaine": {d.value: {
            "niveau_max": c.niveau_max.name,
            "justification": c.justification_cognitive,
            "validation": c.validation_empirique
        } for d, c in validateur.contraintes.items()},
        "limites_cognitives": validateur.limites_cognitives,
        "guide_bonnes_pratiques": guide,
        "tests_validation": [(expr, repr, res['statut']) for expr, repr, res in resultats],
        "conclusion": "Innovation contrôlée et responsable"
    }
    
    with open("contraintes_operateurs_naires.json", "w", encoding="utf-8") as f:
        json.dump(synthese, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Contraintes documentées: contraintes_operateurs_naires.json")

if __name__ == "__main__":
    main()