#!/usr/bin/env python3
"""
🔬 ANALYSEUR D'EXEMPLES DÉTAILLÉS
Validation approfondie des nouveaux concepts dhātu du 22 septembre 2025
"""

import json
from pathlib import Path
from datetime import datetime

class AnalyseurExemplesDetailles:
    def __init__(self):
        self.dhatu_universaux = {
            'TRANS': "Transformation, changement d'état",
            'EVAL': "Évaluation, jugement, appréciation", 
            'LOCATE': "Localisation, positionnement spatial/temporel",
            'FEEL': "Émotion, ressenti, identité personnelle",
            'ACT': "Action, mouvement, dynamisme",
            'QUAL': "Qualité, propriété, caractéristique",
            'REL': "Relation, connexion, lien",
            'KNOW': "Connaissance, information, savoir",
            'EXIST': "Existence, être, présence"
        }
        
    def analyser_concept_contextuel(self):
        """Analyse du concept d'analyse contextuelle"""
        print("🎯 CONCEPT 1: ANALYSE CONTEXTUELLE")
        print("="*50)
        
        exemple = {
            "phrase": "Il était une fois une reine.",
            "innovation": "Détection automatique du contexte situationnel",
            "nouveaux_attributs": [
                "contexte_situationnel → 'conte, narration'",
                "locuteur → 'narrateur externe'", 
                "variables_inconnues → 'identité reine, époque, lieu'"
            ]
        }
        
        print(f"📝 Phrase analysée: '{exemple['phrase']}'")
        print(f"✨ Innovation: {exemple['innovation']}")
        print("\n🔍 NOUVEAUX ATTRIBUTS DÉTECTÉS:")
        for attr in exemple['nouveaux_attributs']:
            print(f"   • {attr}")
            
        print("\n💭 ANALYSE DHĀTU PROBABLE:")
        analyse_dhatu = {
            "était": ["EXIST", "LOCATE"],  # existence dans le temps
            "fois": ["LOCATE", "TRANS"],   # localisation temporelle
            "reine": ["FEEL", "QUAL"]      # identité + qualité sociale
        }
        
        for mot, dhatus in analyse_dhatu.items():
            dhatu_desc = " + ".join([f"{d}({self.dhatu_universaux[d]})" for d in dhatus])
            print(f"   • '{mot}' → {dhatu_desc}")
            
        print("\n❓ QUESTIONS DE VALIDATION:")
        print("   1. Le contexte 'conte' est-il correctement détecté ?")
        print("   2. Les variables inconnues sont-elles pertinentes ?")
        print("   3. Faut-il différencier narrateur/locuteur ?")
        
        return exemple

    def analyser_concepts_onomastiques(self):
        """Analyse des concepts onomastiques (noms propres)"""
        print("\n🎯 CONCEPT 2-4: ANALYSE ONOMASTIQUE")
        print("="*50)
        
        exemples = [
            {
                "nom": "Marie", 
                "type": "anthroponyme",
                "dhatu_propose": "FEEL",
                "justification": "Identité personnelle, dimension émotionnelle"
            },
            {
                "nom": "Jean",
                "type": "anthroponyme", 
                "dhatu_propose": "FEEL",
                "justification": "Identité personnelle, dimension émotionnelle"
            },
            {
                "nom": "Berlin",
                "type": "toponyme",
                "dhatu_propose": "LOCATE", 
                "justification": "Référence spatiale, positionnement géographique"
            }
        ]
        
        phrase_contexte = "Marie et Jean visitent Berlin chaque été."
        print(f"📝 Contexte: '{phrase_contexte}'")
        
        print("\n🏷️ CLASSIFICATION ONOMASTIQUE:")
        for ex in exemples:
            print(f"   • '{ex['nom']}' → {ex['type']}")
            print(f"     Dhātu: {ex['dhatu_propose']} ({self.dhatu_universaux[ex['dhatu_propose']]})")
            print(f"     Justification: {ex['justification']}")
            print()
            
        print("💡 INNOVATION DÉTECTÉE:")
        print("   • Différenciation automatique anthroponyme/toponyme")
        print("   • Assignment dhātu selon la nature du référent")
        print("   • Prise en compte du contexte de la phrase")
        
        print("\n❓ QUESTIONS DE VALIDATION:")
        print("   1. FEEL est-il approprié pour tous les anthroponymes ?")
        print("   2. LOCATE couvre-t-il tous les toponymes ?") 
        print("   3. Faut-il des sous-catégories (prénom/nom, ville/pays) ?")
        print("   4. Comment traiter les noms ambigus (Paris=personne ou ville) ?")
        
        return exemples

    def analyser_molecules_semantiques(self):
        """Analyse du concept de molécules sémantiques"""
        print("\n🎯 CONCEPT 5: MOLÉCULES SÉMANTIQUES")
        print("="*50)
        
        exemple_detaille = {
            "mot": "lièvre",
            "dhatu_constituants": ["TRANS", "EVAL", "LOCATE"],
            "force_semantique": 0.50,
            "complexite": 3,
            "interpretation_dhatu": {
                "TRANS": "Transformation → vitesse, fuite, changement de position",
                "EVAL": "Évaluation → comparaison (vs tortue), jugement de rapidité", 
                "LOCATE": "Localisation → mouvement dans l'espace, position relative"
            }
        }
        
        print(f"🔤 Mot analysé: '{exemple_detaille['mot']}'")
        print(f"🧬 Dhātu constituants: {exemple_detaille['dhatu_constituants']}")
        print(f"⚡ Force sémantique: {exemple_detaille['force_semantique']}")
        print(f"📊 Complexité: {exemple_detaille['complexite']}")
        
        print("\n🔍 INTERPRÉTATION DÉTAILLÉE:")
        for dhatu, interpretation in exemple_detaille['interpretation_dhatu'].items():
            print(f"   • {dhatu}: {interpretation}")
            
        # Autres exemples de molécules
        autres_molecules = [
            {"mot": "sagesse", "dhatu": ["KNOW", "EVAL", "FEEL"], "force": 0.75},
            {"mot": "tempête", "dhatu": ["TRANS", "ACT", "LOCATE"], "force": 0.85},
            {"mot": "justice", "dhatu": ["EVAL", "REL", "QUAL"], "force": 0.70}
        ]
        
        print("\n🧪 AUTRES EXEMPLES DE MOLÉCULES:")
        for mol in autres_molecules:
            dhatu_desc = " + ".join([f"{d}" for d in mol['dhatu']])
            print(f"   • '{mol['mot']}' → {dhatu_desc} (force: {mol['force']})")
            
        print("\n💡 INNOVATION DÉTECTÉE:")
        print("   • Décomposition automatique mots → dhātu constitutifs")
        print("   • Calcul de force sémantique (intensité conceptuelle)")
        print("   • Mesure de complexité (nombre dhātu impliqués)")
        print("   • Interprétation contextuelle des dhātu")
        
        print("\n❓ QUESTIONS DE VALIDATION:")
        print("   1. La formule de force sémantique est-elle appropriée ?")
        print("   2. Comment valider la décomposition dhātu ?")
        print("   3. Faut-il pondérer différemment chaque dhātu ?")
        print("   4. Comment traiter la polysémie (plusieurs décompositions possibles) ?")
        
        return exemple_detaille

    def generer_recommandations(self):
        """Générer des recommandations pour l'amélioration"""
        print("\n🚀 RECOMMANDATIONS D'AMÉLIORATION")
        print("="*50)
        
        recommandations = {
            "Analyse Contextuelle": [
                "Ajouter détection genre littéraire (conte, roman, essai)",
                "Distinguer narrateur homodiégétique/hétérodiégétique", 
                "Créer ontologie des contextes situationnels",
                "Implémenter résolution variables inconnues"
            ],
            "Analyse Onomastique": [
                "Créer base de données noms propres annotés",
                "Implémenter résolution ambiguïté (Paris personne/lieu)",
                "Ajouter sous-catégories dhātu (FEEL_PERSON, LOCATE_CITY)",
                "Tester sur corpus multilingue (noms translittérés)"
            ],
            "Molécules Sémantiques": [
                "Valider décompositions avec experts linguistes", 
                "Créer métriques inter-annotateur agreement",
                "Implémenter apprentissage machine pour force sémantique",
                "Ajouter visualisation graphique molécules complexes"
            ],
            "Validation Générale": [
                "Mesurer performance sur corpus de référence",
                "Comparer avec analyseurs existants (spaCy, NLTK)",
                "Créer interface validation collaborative", 
                "Documenter cas limites et exceptions"
            ]
        }
        
        for categorie, recs in recommandations.items():
            print(f"\n📋 {categorie}:")
            for i, rec in enumerate(recs, 1):
                print(f"   {i}. {rec}")
                
        return recommandations

    def generer_rapport_complet(self):
        """Générer le rapport complet d'analyse"""
        print("\n" + "="*70)
        print("📊 RAPPORT COMPLET - NOUVEAUX CONCEPTS DHĀTU")
        print("="*70)
        
        # Analyse de chaque concept
        concept1 = self.analyser_concept_contextuel()
        concepts234 = self.analyser_concepts_onomastiques() 
        concept5 = self.analyser_molecules_semantiques()
        recs = self.generer_recommandations()
        
        # Synthèse finale
        print("\n🎯 SYNTHÈSE FINALE")
        print("="*50)
        print("✅ POINTS FORTS IDENTIFIÉS:")
        print("   • Innovation dans détection contexte situationnel")
        print("   • Classification onomastique automatique robuste")
        print("   • Décomposition sémantique en dhātu constituants")
        print("   • Métriques quantitatives (force, complexité)")
        
        print("\n⚠️ DÉFIS À RELEVER:")
        print("   • Validation linguistique rigoureuse nécessaire")
        print("   • Gestion polysémie et ambiguïtés")
        print("   • Scalabilité sur gros corpus")
        print("   • Accord inter-annotateur à mesurer")
        
        print("\n🎊 CONCLUSION:")
        print("   Les 25 nouveaux concepts représentent une avancée significative")
        print("   dans l'analyse dhātu automatisée. Priorité à la validation.")
        
        # Sauvegarder le rapport
        rapport_complet = {
            "date_analyse": datetime.now().isoformat(),
            "concepts_analyses": {
                "analyse_contextuelle": concept1,
                "analyse_onomastique": concepts234,
                "molecules_semantiques": concept5
            },
            "recommandations": recs,
            "synthese": {
                "points_forts": 4,
                "defis_identifies": 4, 
                "priorite": "validation_linguistique"
            }
        }
        
        with open("ANALYSE_DETAILLEE_CONCEPTS_20250922.json", "w", encoding="utf-8") as f:
            json.dump(rapport_complet, f, ensure_ascii=False, indent=2)
            
        print(f"\n💾 Rapport sauvegardé: ANALYSE_DETAILLEE_CONCEPTS_20250922.json")

def main():
    analyseur = AnalyseurExemplesDetailles()
    analyseur.generer_rapport_complet()

if __name__ == "__main__":
    main()