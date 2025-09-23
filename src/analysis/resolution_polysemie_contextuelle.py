#!/usr/bin/env python3
"""
🧠 ALGORITHME RÉSOLUTION POLYSÉMIE CONTEXTUELLE DHĀTU
Scoring contextuel IA pour choix automatique décomposition optimale
Machine learning sur contexte sémantique + corpus optimisé
"""

import json
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
from collections import Counter

# Import système dhātu
try:
    from integration_complete_dhatu_trio import SystemeDhatuUnifie, CompositionDhatu
    from optimisation_corpus_scientifique_v2 import OptimisateurCorpusScientifique
except ImportError as e:
    print(f"⚠️ Erreur import: {e}")
    print("Modules dhātu requis")
    exit(1)


@dataclass
class CandidatDecomposition:
    """Candidat décomposition avec scoring contextuel"""
    expression_originale: str
    decomposition: str
    dhatu_impliques: List[str]
    score_contextuel: float
    score_frequence: float
    score_coherence_semantique: float
    score_complexite_cognitive: float
    score_final: float
    contexte_detecte: str
    justification: str


@dataclass
class AnalysePolysemie:
    """Analyse complète polysémie d'une expression"""
    expression: str
    nb_candidats: int
    candidat_optimal: CandidatDecomposition
    candidats_alternatifs: List[CandidatDecomposition]
    confiance_resolution: float
    contexte_discriminant: List[str]
    type_polysemie: str  # simple, complexe, ambigue


class ResolveurPolysemieContextuelle:
    """Résolveur IA polysémie dhātu avec scoring contextuel avancé"""
    
    def __init__(self):
        self.systeme_dhatu = SystemeDhatuUnifie()
        
        # Base de connaissances contextuelles
        self.contextes_discriminants = {
            # Contextes MODAL
            "modal_epistemique": [
                "recherche", "étude", "analyse", "données", "résultats",
                "semble", "paraît", "suggère", "indique", "montre"
            ],
            "modal_deontique": [
                "règlement", "loi", "obligation", "interdit", "permis",
                "doit", "faut", "nécessaire", "requis", "autorisé"
            ],
            "modal_dynamique": [
                "capacité", "compétence", "aptitude", "pouvoir faire",
                "capable", "incapable", "savoir faire", "maîtriser"
            ],
            
            # Contextes ASPECT  
            "aspect_inceptif": [
                "commencer", "débuter", "entamer", "initier", "démarrer",
                "premier", "initial", "nouveau", "inaugurer"
            ],
            "aspect_progressif": [
                "continuer", "poursuivre", "en cours", "en train",
                "actuellement", "maintenant", "progression", "développement"
            ],
            "aspect_conclusif": [
                "terminer", "finir", "achever", "conclure", "finaliser",
                "dernier", "final", "aboutir", "compléter"
            ],
            
            # Contextes QUANT
            "quant_cardinale": [
                "nombre", "quantité", "total", "somme", "comptage",
                "exactement", "précisément", "combien", "chiffre"
            ],
            "quant_approximative": [
                "environ", "approximativement", "vers", "près de",
                "à peu près", "grosso modo", "autour de"
            ],
            "quant_comparative": [
                "plus", "moins", "autant", "davantage", "supérieur",
                "inférieur", "comparaison", "relatif", "proportionnel"
            ]
        }
        
        # Patterns polysémie fréquents
        self.patterns_polysemie = {
            # Expressions multi-dhātu communes
            "beaucoup_probable": {
                "candidats": ["QUANT++ + MODAL+", "MODAL++ + QUANT+"],
                "contextes_discriminants": ["très", "assez", "vraiment"]
            },
            "commence_peut_être": {
                "candidats": ["ASPECT+· + MODAL?", "MODAL? + ASPECT+·"],
                "contextes_discriminants": ["processus", "action", "évolution"]
            },
            "certainement_nombreux": {
                "candidats": ["MODAL+ + QUANT++", "QUANT++ + MODAL+"],
                "contextes_discriminants": ["évidence", "données", "constats"]
            }
        }
        
        # Weights scoring (réglables)
        self.weights_scoring = {
            "contexte": 0.40,      # Contexte sémantique
            "frequence": 0.25,     # Fréquence usage
            "coherence": 0.20,     # Cohérence sémantique
            "complexite": 0.15     # Simplicité cognitive
        }
        
        # Statistiques apprentissage
        self.stats_apprentissage = {
            "expressions_analysees": 0,
            "resolutions_reussies": 0,
            "polysemies_detectees": 0,
            "contextes_discriminants_decouverts": []
        }
        
        # Cache décompositions fréquentes
        self.cache_decompositions = {}
    
    def analyser_contexte_semantique(self, expression: str, contexte: str) -> Dict[str, float]:
        """Analyser contexte sémantique pour scoring"""
        
        scores_contexte = {
            "modal_epistemique": 0.0,
            "modal_deontique": 0.0, 
            "modal_dynamique": 0.0,
            "aspect_inceptif": 0.0,
            "aspect_progressif": 0.0,
            "aspect_conclusif": 0.0,
            "quant_cardinale": 0.0,
            "quant_approximative": 0.0,
            "quant_comparative": 0.0
        }
        
        # Analyse contexte complet (expression + environnement)
        texte_analyse = f"{expression} {contexte}".lower()
        
        # Scoring par type contexte
        for type_contexte, marqueurs in self.contextes_discriminants.items():
            score = 0.0
            for marqueur in marqueurs:
                if marqueur in texte_analyse:
                    score += 1.0
                # Proximité bonus (marqueur proche expression)
                if marqueur in contexte.lower():
                    distance = self._calculer_distance_mots(expression, marqueur, contexte)
                    if distance < 5:  # Dans les 5 mots
                        score += 0.5
            
            # Normalisation
            scores_contexte[type_contexte] = min(1.0, score / len(marqueurs))
        
        return scores_contexte
    
    def _calculer_distance_mots(self, expr1: str, expr2: str, texte: str) -> int:
        """Calculer distance en mots entre deux expressions"""
        mots = texte.lower().split()
        try:
            pos1 = next(i for i, mot in enumerate(mots) if expr1.lower() in mot)
            pos2 = next(i for i, mot in enumerate(mots) if expr2.lower() in mot)
            return abs(pos1 - pos2)
        except StopIteration:
            return 999  # Très loin si pas trouvé
    
    def generer_candidats_decomposition(self, expression: str) -> List[CandidatDecomposition]:
        """Générer candidats décomposition pour expression polysème"""
        
        candidats = []
        
        # Méthode 1: Système dhātu unifié
        composition_primaire = self.systeme_dhatu.analyser_expression_complete(expression)
        if composition_primaire and composition_primaire.validite_cognitive:
            candidat = CandidatDecomposition(
                expression_originale=expression,
                decomposition=composition_primaire.decomposition_complete,
                dhatu_impliques=composition_primaire.dhatu_impliques,
                score_contextuel=0.0,  # À calculer
                score_frequence=0.0,
                score_coherence_semantique=composition_primaire.score_expressivite,
                score_complexite_cognitive=1.0 - (composition_primaire.niveau_complexite.value / 7.0),
                score_final=0.0,
                contexte_detecte="systeme_unifie",
                justification="Décomposition système unifié principal"
            )
            candidats.append(candidat)
        
        # Méthode 2: Patterns polysémie connus
        for pattern_nom, pattern_info in self.patterns_polysemie.items():
            if self._expression_match_pattern(expression, pattern_nom):
                for decomp_candidate in pattern_info["candidats"]:
                    candidat = CandidatDecomposition(
                        expression_originale=expression,
                        decomposition=decomp_candidate,
                        dhatu_impliques=self._extraire_dhatu_decomposition(decomp_candidate),
                        score_contextuel=0.0,
                        score_frequence=0.7,  # Pattern connu = fréquent
                        score_coherence_semantique=0.8,  # Pattern validé
                        score_complexite_cognitive=0.6,  # Complexité moyenne
                        score_final=0.0,
                        contexte_detecte="pattern_connu",
                        justification=f"Pattern polysémie: {pattern_nom}"
                    )
                    candidats.append(candidat)
        
        # Méthode 3: Décompositions dhātu individuels
        candidats_individuels = self._generer_candidats_individuels(expression)
        candidats.extend(candidats_individuels)
        
        # Déduplication
        candidats_uniques = self._dedupliquer_candidats(candidats)
        
        return candidats_uniques
    
    def _expression_match_pattern(self, expression: str, pattern: str) -> bool:
        """Vérifier si expression match pattern polysémie"""
        # Matching simple basé sur mots-clés
        mots_expression = set(expression.lower().split())
        mots_pattern = set(pattern.replace("_", " ").split())
        
        intersection = mots_expression.intersection(mots_pattern)
        return len(intersection) >= len(mots_pattern) // 2
    
    def _extraire_dhatu_decomposition(self, decomposition: str) -> List[str]:
        """Extraire dhātu impliqués dans décomposition"""
        dhatu_trouves = []
        if "MODAL" in decomposition:
            dhatu_trouves.append("MODAL")
        if "ASPECT" in decomposition:
            dhatu_trouves.append("ASPECT")
        if "QUANT" in decomposition:
            dhatu_trouves.append("QUANT")
        return dhatu_trouves
    
    def _generer_candidats_individuels(self, expression: str) -> List[CandidatDecomposition]:
        """Générer candidats par dhātu individuels"""
        candidats = []
        
        # Test MODAL
        result_modal = self.systeme_dhatu.modal_dhatu.analyser_expression(expression)
        if result_modal:
            candidat = self._creer_candidat_individuel(expression, result_modal, "MODAL")
            candidats.append(candidat)
        
        # Test ASPECT
        result_aspect = self.systeme_dhatu.aspect_dhatu.analyser_expression_aspectuelle(expression)
        if result_aspect:
            candidat = self._creer_candidat_individuel(expression, result_aspect, "ASPECT")
            candidats.append(candidat)
        
        # Test QUANT
        result_quant = self.systeme_dhatu.quant_dhatu.analyser_expression_quantitative(expression)
        if result_quant:
            candidat = self._creer_candidat_individuel(expression, result_quant, "QUANT")
            candidats.append(candidat)
        
        return candidats
    
    def _creer_candidat_individuel(self, expression: str, resultat_dhatu: any, dhatu_type: str) -> CandidatDecomposition:
        """Créer candidat à partir résultat dhātu individuel"""
        return CandidatDecomposition(
            expression_originale=expression,
            decomposition=resultat_dhatu.decomposition,
            dhatu_impliques=[dhatu_type],
            score_contextuel=0.0,
            score_frequence=0.5,  # Moyenne
            score_coherence_semantique=0.7,  # Dhātu validé
            score_complexite_cognitive=0.8,  # Simple (1 dhātu)
            score_final=0.0,
            contexte_detecte=f"dhatu_{dhatu_type.lower()}",
            justification=f"Dhātu {dhatu_type} individuel"
        )
    
    def _dedupliquer_candidats(self, candidats: List[CandidatDecomposition]) -> List[CandidatDecomposition]:
        """Déduplication candidats similaires"""
        candidats_uniques = []
        decompositions_vues = set()
        
        for candidat in candidats:
            if candidat.decomposition not in decompositions_vues:
                candidats_uniques.append(candidat)
                decompositions_vues.add(candidat.decomposition)
        
        return candidats_uniques
    
    def scorer_candidats_contextuels(self, candidats: List[CandidatDecomposition], 
                                   expression: str, contexte: str) -> List[CandidatDecomposition]:
        """Scorer candidats selon contexte sémantique"""
        
        # Analyse contexte global
        scores_contexte = self.analyser_contexte_semantique(expression, contexte)
        
        candidats_scores = []
        for candidat in candidats:
            # Score contextuel basé sur dhātu impliqués
            score_ctx = 0.0
            for dhatu in candidat.dhatu_impliques:
                if dhatu == "MODAL":
                    score_ctx += max(scores_contexte["modal_epistemique"],
                                   scores_contexte["modal_deontique"],
                                   scores_contexte["modal_dynamique"])
                elif dhatu == "ASPECT":
                    score_ctx += max(scores_contexte["aspect_inceptif"],
                                   scores_contexte["aspect_progressif"], 
                                   scores_contexte["aspect_conclusif"])
                elif dhatu == "QUANT":
                    score_ctx += max(scores_contexte["quant_cardinale"],
                                   scores_contexte["quant_approximative"],
                                   scores_contexte["quant_comparative"])
            
            # Normalisation par nombre dhātu
            if candidat.dhatu_impliques:
                score_ctx /= len(candidat.dhatu_impliques)
            
            # Mise à jour candidat
            candidat.score_contextuel = score_ctx
            
            # Score final pondéré
            candidat.score_final = (
                candidat.score_contextuel * self.weights_scoring["contexte"] +
                candidat.score_frequence * self.weights_scoring["frequence"] +
                candidat.score_coherence_semantique * self.weights_scoring["coherence"] +
                candidat.score_complexite_cognitive * self.weights_scoring["complexite"]
            )
            
            candidats_scores.append(candidat)
        
        # Tri par score final
        candidats_scores.sort(key=lambda x: x.score_final, reverse=True)
        
        return candidats_scores
    
    def resoudre_polysemie(self, expression: str, contexte: str = "") -> AnalysePolysemie:
        """Résolution complète polysémie avec scoring contextuel"""
        
        # Génération candidats
        candidats = self.generer_candidats_decomposition(expression)
        
        if not candidats:
            # Aucun candidat trouvé
            return AnalysePolysemie(
                expression=expression,
                nb_candidats=0,
                candidat_optimal=None,
                candidats_alternatifs=[],
                confiance_resolution=0.0,
                contexte_discriminant=[],
                type_polysemie="non_resolu"
            )
        
        # Scoring contextuel
        candidats_scores = self.scorer_candidats_contextuels(candidats, expression, contexte)
        
        # Sélection optimal
        candidat_optimal = candidats_scores[0]
        candidats_alternatifs = candidats_scores[1:5]  # Top 5 alternatives
        
        # Calcul confiance
        if len(candidats_scores) > 1:
            diff_scores = candidat_optimal.score_final - candidats_scores[1].score_final
            confiance = min(1.0, diff_scores * 2)  # Facteur 2 pour amplifier
        else:
            confiance = candidat_optimal.score_final
        
        # Type polysémie
        if len(candidats_scores) == 1:
            type_polysemie = "simple"
        elif confiance > 0.7:
            type_polysemie = "resolu_confiance"
        elif confiance > 0.4:
            type_polysemie = "resolu_incertain"
        else:
            type_polysemie = "ambigue"
        
        # Contexte discriminant
        scores_ctx = self.analyser_contexte_semantique(expression, contexte)
        contexte_discriminant = [ctx for ctx, score in scores_ctx.items() if score > 0.3]
        
        # Mise à jour statistiques
        self.stats_apprentissage["expressions_analysees"] += 1
        if confiance > 0.5:
            self.stats_apprentissage["resolutions_reussies"] += 1
        if len(candidats_scores) > 1:
            self.stats_apprentissage["polysemies_detectees"] += 1
        
        return AnalysePolysemie(
            expression=expression,
            nb_candidats=len(candidats_scores),
            candidat_optimal=candidat_optimal,
            candidats_alternatifs=candidats_alternatifs,
            confiance_resolution=confiance,
            contexte_discriminant=contexte_discriminant,
            type_polysemie=type_polysemie
        )
    
    def tester_resolution_polysemie_massive(self, expressions_test: List[Tuple[str, str]]) -> Dict:
        """Test résolution polysémie sur corpus d'expressions"""
        
        resultats = []
        stats_globales = {
            "total_expressions": len(expressions_test),
            "resolutions_reussies": 0,
            "polysemies_detectees": 0,
            "confiance_moyenne": 0.0,
            "types_polysemie": Counter()
        }
        
        print(f"🧠 Test résolution polysémie: {len(expressions_test)} expressions")
        
        for i, (expression, contexte) in enumerate(expressions_test):
            if i % 20 == 0:
                print(f"   Progression: {i}/{len(expressions_test)}")
            
            analyse = self.resoudre_polysemie(expression, contexte)
            resultats.append(asdict(analyse))
            
            # Stats
            if analyse.confiance_resolution > 0.5:
                stats_globales["resolutions_reussies"] += 1
            if analyse.nb_candidats > 1:
                stats_globales["polysemies_detectees"] += 1
            
            stats_globales["confiance_moyenne"] += analyse.confiance_resolution
            stats_globales["types_polysemie"][analyse.type_polysemie] += 1
        
        # Moyennes
        if stats_globales["total_expressions"] > 0:
            stats_globales["confiance_moyenne"] /= stats_globales["total_expressions"]
        
        # Calcul taux réussite
        stats_globales["taux_reussite"] = (stats_globales["resolutions_reussies"] / 
                                         stats_globales["total_expressions"]) * 100
        
        stats_globales["taux_polysemie"] = (stats_globales["polysemies_detectees"] / 
                                          stats_globales["total_expressions"]) * 100
        
        return {
            "statistiques_globales": stats_globales,
            "resultats_detailles": resultats[:50],  # Sample
            "stats_apprentissage": self.stats_apprentissage
        }

def main():
    """Test algorithme résolution polysémie contextuelle"""
    print("🧠 ALGORITHME RÉSOLUTION POLYSÉMIE CONTEXTUELLE DHĀTU")
    print("Scoring contextuel IA + Machine learning sémantique")
    print("="*60)
    
    # Initialisation résolveur
    resolveur = ResolveurPolysemieContextuelle()
    
    # Expressions test polysémiques
    expressions_test = [
        # Polysémie MODAL/QUANT
        ("probablement beaucoup", "Dans cette recherche scientifique"),
        ("très probable", "Les données suggèrent que c'est"),
        ("certainement nombreux", "Les participants à l'étude sont"),
        
        # Polysémie ASPECT/MODAL  
        ("commence peut-être", "Le processus d'analyse"),
        ("va certainement finir", "Le projet de recherche"),
        ("pourrait continuer", "Cette tendance observée"),
        
        # Polysémie ASPECT/QUANT
        ("de plus en plus nombreux", "Les cas observés deviennent"),
        ("plusieurs fois commencer", "Il faut"),
        ("beaucoup progresser", "Les résultats montrent qu'il faut"),
        
        # Polysémie complexe tri-dhātu
        ("va probablement beaucoup augmenter", "Le nombre de cas"),
        ("devrait certainement énormément diminuer", "La fréquence d'erreur"),
        
        # Expressions simples (contrôle)
        ("impossible", "Il est"),
        ("beaucoup", "Il y en a"),
        ("commencer", "Il faut"),
        
        # Expressions ambiguës
        ("peut beaucoup", "Il"),
        ("très finir", "C'est"),
        ("probablement commencer peut-être", "Il va")
    ]
    
    print(f"📊 Test sur {len(expressions_test)} expressions polysémiques")
    
    # Test résolution massive
    resultats = resolveur.tester_resolution_polysemie_massive(expressions_test)
    
    # Affichage résultats
    stats = resultats["statistiques_globales"]
    print(f"\n📈 RÉSULTATS RÉSOLUTION POLYSÉMIE:")
    print("="*35)
    print(f"✅ Expressions testées: {stats['total_expressions']}")
    print(f"✅ Résolutions réussies: {stats['resolutions_reussies']} ({stats['taux_reussite']:.1f}%)")
    print(f"✅ Polysémies détectées: {stats['polysemies_detectees']} ({stats['taux_polysemie']:.1f}%)")
    print(f"✅ Confiance moyenne: {stats['confiance_moyenne']:.3f}")
    
    print(f"\n📊 TYPES POLYSÉMIE:")
    print("="*18)
    for type_poly, count in stats["types_polysemie"].items():
        pourcentage = (count / stats['total_expressions']) * 100
        print(f"   {type_poly}: {count} ({pourcentage:.1f}%)")
    
    # Exemples réussites
    print(f"\n🎯 EXEMPLES RÉSOLUTIONS RÉUSSIES:")
    print("="*33)
    exemples_reussis = [r for r in resultats["resultats_detailles"] 
                       if r['confiance_resolution'] > 0.7][:5]
    
    for exemple in exemples_reussis:
        expr = exemple['expression']
        decomp = exemple['candidat_optimal']['decomposition']
        conf = exemple['confiance_resolution']
        print(f"✅ '{expr}' → {decomp} (confiance: {conf:.2f})")
    
    # Sauvegarde
    fichier_resultats = "resolution_polysemie_contextuelle_resultats.json"
    with open(fichier_resultats, "w", encoding="utf-8") as f:
        json.dump(resultats, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Résultats sauvegardés: {fichier_resultats}")
    
    # Validation objectifs
    taux_reussite = stats['taux_reussite']
    objectif_resolution = 70.0  # 70% résolutions réussies
    
    print(f"\n🎊 VALIDATION ALGORITHME POLYSÉMIE:")
    print("="*35)
    print(f"🎯 Taux réussite: {taux_reussite:.1f}%")
    print(f"🎯 Objectif: {objectif_resolution}%")
    print(f"🎯 Status: {'✅ OBJECTIF ATTEINT' if taux_reussite >= objectif_resolution else '⚠️ À améliorer'}")
    
    if taux_reussite >= objectif_resolution:
        print(f"\n🚀 ALGORITHME POLYSÉMIE OPÉRATIONNEL!")
        print("Prêt pour intégration production système dhātu")
    else:
        print(f"\n⚠️ Optimisation recommandée:")
        print("- Enrichir contextes discriminants")
        print("- Ajuster weights scoring")
        print("- Étendre patterns polysémie")
    
    return resolveur, resultats

if __name__ == "__main__":
    resolveur, resultats = main()