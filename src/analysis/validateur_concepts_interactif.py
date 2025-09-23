#!/usr/bin/env python3
"""
🧪 VALIDATEUR INTERACTIF CONCEPTS DHĀTU
Session du 22 septembre 2025 - Validation nouveaux développements
"""

import json
from pathlib import Path
from datetime import datetime

class ValidateurConceptsDhatu:
    def __init__(self):
        self.session_date = "2025-09-22"
        self.concepts_a_valider = []
        self.feedbacks = []
        
        # Charger les analyses de ce matin
        self.charger_analyses_session()
    
    def charger_analyses_session(self):
        """Charge les analyses générées ce matin"""
        fichiers_session = [
            "analyse_20250922_085336_fr.json",
            "analyse_onomastique_20250922_090407_fr.json", 
            "analyse_molecules_semantiques_conte.json"
        ]
        
        for fichier in fichiers_session:
            if Path(fichier).exists():
                with open(fichier) as f:
                    data = json.load(f)
                    self.analyser_nouveaux_concepts(fichier, data)
    
    def analyser_nouveaux_concepts(self, fichier, data):
        """Identifie les nouveaux concepts dans les analyses"""
        concepts = []
        
        if "molecules_analysees" in data:
            # Système de molécules sémantiques
            for mot, analyse in data["molecules_analysees"].items():
                concept = {
                    "type": "molecule_semantique",
                    "source": fichier,
                    "exemple": {
                        "mot": mot,
                        "dhatu_constituants": analyse.get("dhatu_principaux", []),
                        "force_semantique": self.extraire_force_moyenne(analyse),
                        "complexite": analyse.get("niveau_complexite", 0)
                    }
                }
                concepts.append(concept)
        
        elif "noms_detectes" in data:
            # Système onomastique
            for nom in data["noms_detectes"]:
                concept = {
                    "type": "analyse_onomastique", 
                    "source": fichier,
                    "exemple": {
                        "nom": nom,
                        "phrase": data.get("phrase_originale", ""),
                        "types_detectes": self.extraire_types_onomastiques(data, nom)
                    }
                }
                concepts.append(concept)
        
        elif "elements" in data:
            # Analyse contextuelle fine
            concept = {
                "type": "analyse_contextuelle",
                "source": fichier,
                "exemple": {
                    "phrase": data.get("phrase_originale", ""),
                    "elements_analyses": len(data["elements"]),
                    "nouveaux_attributs": self.extraire_nouveaux_attributs(data)
                }
            }
            concepts.append(concept)
        
        self.concepts_a_valider.extend(concepts)
    
    def extraire_force_moyenne(self, analyse):
        """Calcule la force sémantique moyenne"""
        forces = []
        for interp in analyse.get("interpretations_possibles", []):
            forces.append(interp.get("force_semantique", 0))
        return sum(forces) / len(forces) if forces else 0
    
    def extraire_types_onomastiques(self, data, nom):
        """Extrait les types onomastiques détectés"""
        for analyse in data.get("analyses_individuelles", []):
            if analyse.get("nom_original") == nom:
                return analyse.get("type_onomastique", "inconnu")
        return "non_analyse"
    
    def extraire_nouveaux_attributs(self, data):
        """Identifie les nouveaux attributs dans l'analyse"""
        nouveaux = []
        for element in data.get("elements", [])[:3]:  # Sample 3 premiers
            for attr in element.keys():
                if attr in ["locuteur", "contexte_situationnel", "variables_inconnues"]:
                    nouveaux.append(attr)
        return list(set(nouveaux))
    
    def presenter_exemples_validation(self):
        """Présente les exemples pour validation"""
        print("🧪 VALIDATION NOUVEAUX CONCEPTS DHĀTU")
        print("=" * 50)
        print(f"📅 Session: {self.session_date}")
        print(f"🔬 Concepts détectés: {len(self.concepts_a_valider)}")
        
        for i, concept in enumerate(self.concepts_a_valider[:5], 1):  # Top 5
            print(f"\n📋 EXEMPLE {i}: {concept['type'].upper()}")
            print("-" * 30)
            
            if concept["type"] == "molecule_semantique":
                self.presenter_molecule(concept["exemple"])
            elif concept["type"] == "analyse_onomastique":
                self.presenter_onomastique(concept["exemple"])
            elif concept["type"] == "analyse_contextuelle":
                self.presenter_contextuel(concept["exemple"])
            
            # Question de validation
            print(f"\n❓ VALIDATION REQUISE:")
            print(f"   • Ce concept vous semble-t-il pertinent ?")
            print(f"   • Les dhātu assignés sont-ils appropriés ?")
            print(f"   • Suggestions d'amélioration ?")
    
    def presenter_molecule(self, exemple):
        """Présente un exemple de molécule sémantique"""
        print(f"   🔤 Mot analysé: '{exemple['mot']}'")
        print(f"   🧬 Dhātu constituants: {exemple['dhatu_constituants']}")
        print(f"   ⚡ Force sémantique: {exemple['force_semantique']:.2f}")
        print(f"   📊 Complexité: {exemple['complexite']}")
        
        print(f"\n   💭 Interprétation:")
        for dhatu in exemple['dhatu_constituants']:
            print(f"      • {dhatu}: {self.expliquer_dhatu(dhatu)}")
    
    def presenter_onomastique(self, exemple):
        """Présente un exemple d'analyse onomastique"""
        print(f"   👤 Nom: '{exemple['nom']}'")
        print(f"   📝 Contexte: \"{exemple['phrase']}\"")
        print(f"   🏷️  Type: {exemple['types_detectes']}")
        
        print(f"\n   💭 Analyse dhātu:")
        if exemple['types_detectes'] == "anthroponyme":
            print(f"      • Probable dhātu: FEEL (identité émotionnelle)")
        elif exemple['types_detectes'] == "toponyme":
            print(f"      • Probable dhātu: LOCATE (référence spatiale)")
        else:
            print(f"      • Dhātu à déterminer pour type: {exemple['types_detectes']}")
    
    def presenter_contextuel(self, exemple):
        """Présente un exemple d'analyse contextuelle"""
        print(f"   📝 Phrase: \"{exemple['phrase']}\"")
        print(f"   🔢 Éléments analysés: {exemple['elements_analyses']}")
        print(f"   ✨ Nouveaux attributs: {exemple['nouveaux_attributs']}")
        
        print(f"\n   💭 Innovations détectées:")
        for attr in exemple['nouveaux_attributs']:
            if attr == "locuteur":
                print(f"      • Identification automatique du locuteur")
            elif attr == "contexte_situationnel":  
                print(f"      • Détection du contexte situationnel")
            elif attr == "variables_inconnues":
                print(f"      • Marquage explicite des incertitudes")
    
    def expliquer_dhatu(self, dhatu):
        """Explique un dhātu"""
        explications = {
            "EXIST": "existence, être, présence",
            "TRANS": "transformation, changement",
            "EVAL": "évaluation, jugement",
            "COMM": "communication, expression",
            "LOCATE": "localisation, positionnement",
            "FEEL": "sentiment, perception",
            "ITER": "répétition, itération",
            "DECIDE": "décision, choix",
            "RELATE": "relation, connexion"
        }
        return explications.get(dhatu, "dhātu à définir")
    
    def generer_rapport_validation(self):
        """Génère un rapport pour validation"""
        rapport = {
            "session_date": self.session_date,
            "concepts_analyses": len(self.concepts_a_valider),
            "types_concepts": {},
            "exemples_detailles": self.concepts_a_valider[:10],
            "recommendations": [
                "Valider la granularité des dhātu (9 universaux vs sous-dhātu)",
                "Tester la robustesse cross-linguistique",
                "Mesurer l'accord inter-annotateur humain",
                "Optimiser les métriques de force sémantique"
            ]
        }
        
        # Compter les types
        for concept in self.concepts_a_valider:
            type_concept = concept["type"]
            rapport["types_concepts"][type_concept] = rapport["types_concepts"].get(type_concept, 0) + 1
        
        with open(f"RAPPORT_VALIDATION_CONCEPTS_{self.session_date.replace('-', '')}.json", "w") as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False)
        
        return rapport

def main():
    """Fonction principale de validation"""
    validateur = ValidateurConceptsDhatu()
    
    # Présenter les exemples
    validateur.presenter_exemples_validation()
    
    # Générer rapport
    rapport = validateur.generer_rapport_validation()
    
    print(f"\n✅ RAPPORT DE VALIDATION GÉNÉRÉ")
    print(f"📊 Types de concepts: {rapport['types_concepts']}")
    print(f"💾 Fichier: RAPPORT_VALIDATION_CONCEPTS_{validateur.session_date.replace('-', '')}.json")
    
    print(f"\n🎯 PROCHAINES ÉTAPES RECOMMANDÉES:")
    for i, rec in enumerate(rapport["recommendations"], 1):
        print(f"   {i}. {rec}")

if __name__ == "__main__":
    main()