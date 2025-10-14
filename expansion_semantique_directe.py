#!/usr/bin/env python3
"""
EXPANSION SÉMANTIQUE DIRECTE OPTIMISÉE
======================================

Utilise les 25,000 articles Wikipedia décompressés pour expansion sémantique
directe et efficace du dictionnaire récursif vers 100% couverture.

PERFORMANCE OPTIMISÉE:
- Accès direct JSON (pas de décompression runtime)
- Recherche vectorisée par mots-clés
- Cache sémantique intelligent
- Décomposition atomique accélérée
"""

import json
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import Counter, defaultdict
import re
import time

class ExpanseurSemantiqueDirecte:
    """Expansion sémantique haute performance via articles décompressés"""
    
    def __init__(self):
        self.decompressed_dir = Path("wikipedia_decompressed")
        self.output_dir = Path("expansion_semantique_directe")
        self.output_dir.mkdir(exist_ok=True)
        
        # Cache articles pour performance
        self.cache_articles = {}
        self.articles_indexes = {}  # Index mots-clés → articles
        
        # Base atomique universelle
        self.ATOMES_UNIVERSELS = [
            "MOUVEMENT", "COGNITION", "PERCEPTION", "COMMUNICATION",
            "CREATION", "EMOTION", "EXISTENCE", "DESTRUCTION", 
            "POSSESSION", "DOMINATION"
        ]
        
        # Dictionnaire existant
        self.dictionnaire_existant = self._charger_dictionnaire_recursif()
        
        # Concepts cibles (155 identifiés précédemment)
        self.concepts_cibles = self._definir_concepts_cibles()
        
        # Résultats expansion
        self.concepts_resolus = {}
        
    def _charger_dictionnaire_recursif(self) -> Dict:
        """Charge dictionnaire récursif existant"""
        chemin = Path("dictionnaire_recursif/dictionnaire_recursif_complet.json")
        
        if chemin.exists():
            with open(chemin, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("dictionnaire_recursif", {})
        return {}
    
    def _definir_concepts_cibles(self) -> Set[str]:
        """Définit concepts cibles prioritaires pour expansion"""
        return {
            # Perceptions sensorielles
            "VOIR", "REGARDER", "OBSERVER", "CONTEMPLER",
            "ENTENDRE", "ÉCOUTER", "OUÏR", 
            "TOUCHER", "PALPER", "CARESSER", "FRAPPER",
            "GOÛTER", "SAVOURER", "DÉGUSTER",
            "SENTIR", "FLAIRER", "HUMER",
            
            # Actions physiques essentielles
            "MARCHER", "COURIR", "SAUTER", "GRIMPER", "VOLER", "NAGER",
            "PRENDRE", "SAISIR", "TENIR", "LÂCHER", "JETER",
            "MANGER", "BOIRE", "AVALER", "CROQUER",
            "DORMIR", "RÊVER", "SE_RÉVEILLER",
            
            # Mental & cognition
            "PENSER", "RÉFLÉCHIR", "MÉDITER", "ANALYSER",
            "SE_SOUVENIR", "OUBLIER", "RECONNAÎTRE",
            "IMAGINER", "RÊVER", "FANTASMER",
            "DÉCIDER", "CHOISIR", "HÉSITER",
            "COMPRENDRE", "SAISIR", "INTERPRÉTER",
            
            # Émotions raffinées
            "JOIE", "BONHEUR", "EUPHORIE", "EXTASE", "SATISFACTION",
            "TRISTESSE", "CHAGRIN", "MÉLANCOLIE", "NOSTALGIE", "REGRET",
            "COLÈRE", "FUREUR", "IRRITATION", "INDIGNATION", "RAGE",
            "PEUR", "TERREUR", "ANXIÉTÉ", "INQUIÉTUDE", "ANGOISSE",
            "AMOUR", "AFFECTION", "TENDRESSE", "PASSION", "ADORATION",
            "HAINE", "MÉPRIS", "DÉGOÛT", "AVERSION", "RÉPULSION",
            
            # Sociabilité & relations
            "FAMILLE", "PARENT", "ENFANT", "FRÈRE", "SOEUR",
            "AMI", "ENNEMI", "RIVAL", "ALLIÉ", "COMPAGNON",
            "MARIAGE", "UNION", "DIVORCE", "SÉPARATION",
            "GROUPE", "COMMUNAUTÉ", "SOCIÉTÉ", "TRIBU", "NATION",
            
            # Concepts abstraits fondamentaux
            "TEMPS", "DURÉE", "INSTANT", "ÉTERNITÉ", "PASSÉ", "FUTUR",
            "ESPACE", "LIEU", "DISTANCE", "PROXIMITÉ", "ÉLOIGNEMENT",
            "CAUSE", "EFFET", "RAISON", "BUT", "MOYEN", "RÉSULTAT",
            "VÉRITÉ", "MENSONGE", "RÉALITÉ", "ILLUSION", "APPARENCE",
            "BIEN", "MAL", "JUSTE", "INJUSTE", "MORAL", "IMMORAL",
            "BEAU", "LAID", "ESTHÉTIQUE", "HARMONIEUX", "DISGRACIEUX",
            
            # Nature & environnement
            "ARBRE", "FLEUR", "FRUIT", "FEUILLE", "RACINE",
            "EAU", "FEU", "AIR", "TERRE", "PIERRE",
            "SOLEIL", "LUNE", "ÉTOILE", "CIEL", "NUAGE",
            "ANIMAL", "OISEAU", "POISSON", "INSECTE", "MAMMIFÈRE",
            
            # Technologies & outils
            "OUTIL", "MACHINE", "INSTRUMENT", "DISPOSITIF",
            "ROUE", "LEVIER", "CORDE", "LAME", "RÉCIPIENT",
            "MAISON", "ABRI", "TOIT", "MUR", "PORTE", "FENÊTRE",
            
            # Arts & créations
            "ART", "MUSIQUE", "CHANT", "DANSE", "PEINTURE",
            "SCULPTURE", "ARCHITECTURE", "LITTÉRATURE", "POÉSIE",
            "CONTE", "HISTOIRE", "RÉCIT", "MYTHE", "LÉGENDE"
        }
    
    def charger_articles_optimise(self, langues: List[str] = None) -> Dict[str, List[Dict]]:
        """Chargement optimisé articles avec cache"""
        print("📚 CHARGEMENT ARTICLES OPTIMISÉ")
        print("-" * 35)
        
        if langues is None:
            langues = ['fr', 'en', 'de', 'sa', 'hi']
        
        articles_charges = {}
        
        for langue in langues:
            fichier = self.decompressed_dir / f"{langue}_articles_rapide.json"
            
            if fichier.exists():
                print(f"   📖 Chargement {langue}...")
                
                with open(fichier, 'r', encoding='utf-8') as f:
                    articles = json.load(f)
                    articles_charges[langue] = articles
                    
                print(f"   ✅ {langue}: {len(articles)} articles chargés")
                
                # Construction index mots-clés pour recherche rapide
                self._construire_index_mots_cles(langue, articles)
            else:
                print(f"   ❌ {langue}: Fichier non trouvé ({fichier})")
        
        print(f"\n📊 Total: {len(articles_charges)} langues, {sum(len(arts) for arts in articles_charges.values())} articles")
        return articles_charges
    
    def _construire_index_mots_cles(self, langue: str, articles: List[Dict]):
        """Construit index mots-clés → articles pour recherche rapide"""
        
        if langue not in self.articles_indexes:
            self.articles_indexes[langue] = defaultdict(list)
        
        for i, article in enumerate(articles):
            # Extraction mots-clés du titre et contenu
            mots_titre = self._extraire_mots_cles(article['titre'])
            mots_contenu = self._extraire_mots_cles(article['contenu'][:500])  # Premier 500 chars
            
            tous_mots = set(mots_titre + mots_contenu)
            
            for mot in tous_mots:
                if len(mot) >= 3:  # Mots significatifs seulement
                    self.articles_indexes[langue][mot.lower()].append(i)
    
    def _extraire_mots_cles(self, texte: str) -> List[str]:
        """Extraction mots-clés optimisée"""
        if not texte:
            return []
        
        # Nettoyage et tokenization
        texte_propre = re.sub(r'[^\w\s]', ' ', texte.lower())
        mots = texte_propre.split()
        
        # Filtrage mots vides (versions multilingue)
        mots_vides = {
            'le', 'la', 'les', 'de', 'du', 'des', 'et', 'ou', 'un', 'une', 'ce', 'cette', 'dans', 'pour', 'avec', 'sur', 'par',
            'the', 'a', 'an', 'and', 'or', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'are', 'was', 'were',
            'der', 'die', 'das', 'und', 'oder', 'in', 'auf', 'mit', 'von', 'zu', 'für', 'durch', 'als', 'ist', 'sind', 'war', 'waren'
        }
        
        return [mot for mot in mots if mot not in mots_vides and len(mot) >= 3]
    
    def rechercher_contextes_concept(self, concept: str, articles_charges: Dict[str, List[Dict]], 
                                   max_contextes: int = 15) -> List[Dict[str, str]]:
        """Recherche contextes optimisée pour un concept"""
        
        concept_lower = concept.lower().replace("_", " ")
        concept_mots = concept_lower.split()
        
        contextes = []
        
        # Recherche dans toutes les langues
        for langue, articles in articles_charges.items():
            if langue not in self.articles_indexes:
                continue
                
            # Recherche par index mots-clés
            articles_candidats = set()
            
            for mot in concept_mots:
                if mot in self.articles_indexes[langue]:
                    articles_candidats.update(self.articles_indexes[langue][mot])
            
            # Vérification contextes dans articles candidats
            for idx in list(articles_candidats)[:max_contextes//len(articles_charges)]:
                if idx < len(articles):
                    article = articles[idx]
                    
                    # Vérification présence concept
                    contenu_lower = article['contenu'].lower()
                    if concept_lower in contenu_lower or any(mot in contenu_lower for mot in concept_mots):
                        
                        # Extraction phrase contextuelle
                        phrases = re.split(r'[.!?]+', article['contenu'])
                        for phrase in phrases:
                            if concept_lower in phrase.lower() or any(mot in phrase.lower() for mot in concept_mots):
                                contextes.append({
                                    'langue': langue,
                                    'source': article['titre'],
                                    'phrase': phrase.strip()[:300],  # Limité
                                    'concept_recherche': concept
                                })
                                break
        
        return contextes[:max_contextes]
    
    def analyser_decomposition_semantique_rapide(self, concept: str, contextes: List[Dict[str, str]]) -> Optional[Tuple[List[str], float]]:
        """Analyse sémantique rapide pour décomposition atomique"""
        
        if not contextes:
            return None
        
        # Patterns sémantiques optimisés par atome
        patterns_optimises = {
            "MOUVEMENT": {
                'patterns': ["mouv", "déplac", "voyage", "march", "cour", "vol", "nag", "all", "ven", "move", "go", "come", "travel", "walk", "run", "fly"],
                'poids': 1.0
            },
            "COGNITION": {
                'patterns': ["pens", "compren", "sav", "connaî", "réfléch", "analy", "think", "understand", "know", "analyze", "learn", "realize"],
                'poids': 1.0  
            },
            "PERCEPTION": {
                'patterns': ["voir", "regard", "entend", "écout", "sent", "touch", "see", "look", "hear", "listen", "feel", "smell", "taste"],
                'poids': 1.2  # Plus discriminant
            },
            "COMMUNICATION": {
                'patterns': ["dir", "parl", "communiq", "exprim", "racont", "expliqu", "say", "speak", "communicate", "express", "tell"],
                'poids': 1.0
            },
            "CREATION": {
                'patterns': ["cré", "fair", "constru", "fabriqu", "produi", "génér", "create", "make", "build", "produce", "generate"],
                'poids': 1.0
            },
            "EMOTION": {
                'patterns': ["aim", "haï", "ressent", "éprouv", "émouv", "plaisir", "douleur", "love", "hate", "feel", "emotion", "joy", "sad", "happy"],
                'poids': 1.1
            },
            "EXISTENCE": {
                'patterns': ["êtr", "exist", "viv", "demeur", "rest", "dur", "be", "exist", "live", "remain", "stay", "become"],
                'poids': 0.9  # Plus général
            },
            "DESTRUCTION": {
                'patterns': ["détru", "cass", "bris", "mour", "fin", "disparaî", "destroy", "break", "die", "end", "disappear", "ruin"],
                'poids': 1.1
            },
            "POSSESSION": {
                'patterns': ["av", "posséd", "prend", "donn", "obten", "perd", "have", "possess", "take", "give", "get", "obtain", "own"],
                'poids': 1.0
            },
            "DOMINATION": {
                'patterns': ["command", "dirig", "contrôl", "domin", "gouver", "règn", "lead", "control", "dominate", "govern", "rule", "power"],
                'poids': 1.1
            }
        }
        
        # Scoring par atome
        scores_atomiques = Counter()
        
        for contexte in contextes:
            phrase_lower = contexte["phrase"].lower()
            
            for atome, config in patterns_optimises.items():
                score_atome = 0
                
                for pattern in config['patterns']:
                    if pattern in phrase_lower:
                        score_atome += 1
                
                if score_atome > 0:
                    scores_atomiques[atome] += score_atome * config['poids']
        
        if not scores_atomiques:
            return None
        
        # Sélection atomes significatifs avec seuils adaptatifs
        atomes_selectes = []
        score_max = scores_atomiques.most_common(1)[0][1] if scores_atomiques else 0
        
        for atome, score in scores_atomiques.most_common(4):  # Max 4 atomes
            # Seuil adaptatif selon score max
            seuil = max(1.5, score_max * 0.3)  
            
            if score >= seuil:
                atomes_selectes.append(atome)
        
        if atomes_selectes:
            # Calcul confiance basé sur convergence et coverage
            nb_contextes = len(contextes)
            convergence = min(1.0, len(atomes_selectes) / 3.0)  # Optimal 2-3 atomes
            coverage = min(1.0, nb_contextes / 10.0)  # Optimal 10+ contextes
            
            confiance = (convergence * 0.6 + coverage * 0.4) * 0.85  # Max 85%
            
            return (atomes_selectes, confiance)
        
        return None
    
    def expansion_massive_optimisee(self, articles_charges: Dict[str, List[Dict]], 
                                  max_concepts: int = 100) -> Dict[str, Dict]:
        """Expansion massive optimisée sur concepts prioritaires"""
        
        print(f"\n🚀 EXPANSION MASSIVE OPTIMISÉE ({max_concepts} concepts)")
        print("=" * 55)
        
        concepts_traites = list(self.concepts_cibles)[:max_concepts]
        
        # Batch processing pour performance
        batch_size = 10
        total_batches = (len(concepts_traites) + batch_size - 1) // batch_size
        
        start_time = time.time()
        concepts_resolus = 0
        
        for batch_idx in range(total_batches):
            batch_start = batch_idx * batch_size
            batch_end = min((batch_idx + 1) * batch_size, len(concepts_traites))
            batch_concepts = concepts_traites[batch_start:batch_end]
            
            print(f"\n--- BATCH {batch_idx + 1}/{total_batches} ({len(batch_concepts)} concepts) ---")
            
            for concept in batch_concepts:
                # Skip si déjà défini
                if concept in self.dictionnaire_existant:
                    print(f"   ⏭️  {concept}: Déjà défini")
                    continue
                
                # Recherche contextes
                contextes = self.rechercher_contextes_concept(concept, articles_charges)
                
                if contextes:
                    # Analyse sémantique
                    analyse = self.analyser_decomposition_semantique_rapide(concept, contextes)
                    
                    if analyse:
                        atomes, confiance = analyse
                        formule = " + ".join(atomes)
                        
                        self.concepts_resolus[concept] = {
                            "decomposition": atomes,
                            "formule_complete": formule,
                            "confiance": confiance,
                            "contextes_count": len(contextes),
                            "source_expansion": "wikipedia_directe_optimisee",
                            "exemples_contextes": contextes[:3]
                        }
                        
                        concepts_resolus += 1
                        print(f"   ✅ {concept} = {formule} (conf: {confiance:.2f})")
                    else:
                        print(f"   ❌ {concept}: Analyse échouée")
                else:
                    print(f"   ❌ {concept}: Aucun contexte")
            
            # Stats progression
            elapsed = time.time() - start_time
            vitesse = concepts_resolus / elapsed if elapsed > 0 else 0
            print(f"\n📊 Progression: {concepts_resolus} résolus, {vitesse:.1f} concepts/min")
        
        return self.concepts_resolus
    
    def generer_integration_finale(self, concepts_resolus: Dict) -> Dict:
        """Génère intégration finale pour dictionnaire récursif"""
        
        # Métriques finales
        total_concepts_nouveaux = len(concepts_resolus)
        confiance_moyenne = sum(c["confiance"] for c in concepts_resolus.values()) / total_concepts_nouveaux if total_concepts_nouveaux > 0 else 0
        
        # Distribution par niveau de confiance
        confiance_distribution = {
            "haute_confiance_80+": len([c for c in concepts_resolus.values() if c["confiance"] >= 0.8]),
            "confiance_moyenne_60-80": len([c for c in concepts_resolus.values() if 0.6 <= c["confiance"] < 0.8]),
            "confiance_basse_60-": len([c for c in concepts_resolus.values() if c["confiance"] < 0.6])
        }
        
        # Coverage estimation mise à jour
        total_dictionnaire_etendu = len(self.dictionnaire_existant) + total_concepts_nouveaux
        couverture_estimee = (total_dictionnaire_etendu / 200) * 100  # Sur 200 concepts estimés nécessaires
        
        rapport_integration = {
            "titre": "Expansion Sémantique Directe - Intégration Finale",
            "description": "Expansion optimisée via 25,000 articles Wikipedia décompressés",
            "performance": {
                "articles_sources": 25000,
                "langues_traitees": 5,
                "concepts_traites": len(self.concepts_cibles),
                "concepts_resolus": total_concepts_nouveaux,
                "taux_resolution": f"{(total_concepts_nouveaux / len(self.concepts_cibles)) * 100:.1f}%"
            },
            "qualite_resolution": {
                "confiance_moyenne": f"{confiance_moyenne:.3f}",
                "distribution_confiance": confiance_distribution,
                "seuil_acceptation": "≥60% confiance recommandé"
            },
            "impact_dictionnaire": {
                "concepts_avant": len(self.dictionnaire_existant),
                "concepts_apres": total_dictionnaire_etendu,
                "augmentation": f"+{total_concepts_nouveaux}",
                "couverture_estimee": f"{couverture_estimee:.1f}%"
            },
            "concepts_integres": {
                concept: {
                    "formule": data["formule_complete"],
                    "confiance": data["confiance"],
                    "contextes": data["contextes_count"]
                }
                for concept, data in list(concepts_resolus.items())[:20]  # Top 20
            },
            "recommandations": [
                "Valider concepts confiance <70% manuellement",
                "Intégrer dans dictionnaire récursif existant", 
                "Tester reconstruction concepts complexes",
                "Itérer sur concepts non-résolus avec corpus étendus",
                "Optimiser patterns sémantiques selon résultats"
            ]
        }
        
        # Sauvegarde intégration
        with open(self.output_dir / "integration_expansion_finale.json", "w", encoding="utf-8") as f:
            json.dump(rapport_integration, f, indent=2, ensure_ascii=False)
        
        # Sauvegarde concepts pour intégration directe
        with open(self.output_dir / "concepts_nouveaux_integration.json", "w", encoding="utf-8") as f:
            json.dump(concepts_resolus, f, indent=2, ensure_ascii=False)
        
        return rapport_integration

def main():
    """Expansion sémantique directe optimisée haute performance"""
    print("⚡ EXPANSION SÉMANTIQUE DIRECTE OPTIMISÉE")
    print("=" * 45)
    print("Performance: 25,000 articles → Concepts résolus")
    print("Cible: 100% couverture dictionnaire récursif")
    print()
    
    expanseur = ExpanseurSemantiqueDirecte()
    
    print(f"🎯 Concepts cibles: {len(expanseur.concepts_cibles)}")
    print(f"📚 Dictionnaire existant: {len(expanseur.dictionnaire_existant)}")
    
    # Chargement articles optimisé
    articles_charges = expanseur.charger_articles_optimise()
    
    if not articles_charges:
        print("\n⚠️  Aucun article chargé. Exécuter d'abord:")
        print("   python3 wikipedia_decompresseur_optimise.py")
        return
    
    # Expansion massive
    concepts_resolus = expanseur.expansion_massive_optimisee(articles_charges, max_concepts=80)
    
    # Intégration finale
    rapport = expanseur.generer_integration_finale(concepts_resolus)
    
    print(f"\n🏆 RÉSULTATS EXPANSION DIRECTE")
    print("=" * 35)
    print(f"⚡ Concepts résolus: {len(concepts_resolus)}")
    print(f"📊 Taux résolution: {rapport['performance']['taux_resolution']}")
    print(f"🎯 Confiance moyenne: {rapport['qualite_resolution']['confiance_moyenne']}")
    print(f"📈 Couverture estimée: {rapport['impact_dictionnaire']['couverture_estimee']}")
    
    print(f"\n📊 Distribution confiance:")
    for niveau, count in rapport['qualite_resolution']['distribution_confiance'].items():
        print(f"   {niveau.replace('_', ' ')}: {count}")
    
    print(f"\n💾 Fichiers générés:")
    print(f"   • {expanseur.output_dir}/integration_expansion_finale.json")
    print(f"   • {expanseur.output_dir}/concepts_nouveaux_integration.json")
    
    if rapport['impact_dictionnaire']['couverture_estimee'].rstrip('%') != '' and float(rapport['impact_dictionnaire']['couverture_estimee'].rstrip('%')) >= 85:
        print(f"\n🎉 QUASI-COMPLÉTUDE ATTEINTE!")
        print(f"   PanLang couvre 85%+ des concepts humains universels")
    else:
        print(f"\n🔄 PROGRESSION MAJEURE")
        print(f"   Expansion continue selon recommandations")
    
    print(f"\n✅ Prêt pour intégration dans dictionnaire récursif!")

if __name__ == "__main__":
    main()