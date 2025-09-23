#!/usr/bin/env python3
"""
🎯 OPTIMISEUR SCORING CONTEXTUEL AVANCÉ
Machine learning adaptatif pour améliorer taux réussite polysémie >70%
Optimisation weights dynamique + apprentissage patterns
"""

import json
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from collections import Counter, defaultdict
import random

# Import modules base
try:
    from resolution_polysemie_contextuelle import ResolveurPolysemieContextuelle, CandidatDecomposition, AnalysePolysemie
    from extension_cross_linguistique import ExtensionCrossLinguistique, ResultatCrossLinguistique
    from integration_complete_dhatu_trio import SystemeDhatuUnifie
except ImportError as e:
    print(f"⚠️ Erreur import: {e}")
    print("Modules requis manquants")
    exit(1)


@dataclass
class ConfigurationOptimisation:
    """Configuration optimisation scoring"""
    weights_initiaux: Dict[str, float]
    plage_optimisation: Dict[str, Tuple[float, float]]
    algorithme: str  # "gradient_descent", "genetic", "adaptive"
    iterations_max: int
    convergence_seuil: float
    taille_population: int  # pour algorithmique génétique
    taux_mutation: float
    validation_split: float


@dataclass
class ResultatOptimisation:
    """Résultat optimisation weights scoring"""
    weights_optimaux: Dict[str, float]
    score_performance: float
    iterations_convergence: int
    historique_scores: List[float]
    amelioration_relative: float
    configurations_testees: int
    temps_optimisation: float


@dataclass
class MetriquePerformance:
    """Métriques performance détaillées"""
    taux_reussite: float
    confiance_moyenne: float
    polysemies_resolues: int
    coherence_cross_linguistique: float
    score_composite: float
    distribution_types: Dict[str, int]


class OptimiseurScoringContextuel:
    """Optimiseur ML adaptatif pour scoring contextuel dhātu"""
    
    def __init__(self):
        self.resolveur_base = ResolveurPolysemieContextuelle()
        self.extension_cross = ExtensionCrossLinguistique()
        
        # Configuration optimisation par défaut
        self.config_default = ConfigurationOptimisation(
            weights_initiaux={
                "contexte": 0.40,
                "frequence": 0.25,
                "coherence": 0.20,
                "complexite": 0.15
            },
            plage_optimisation={
                "contexte": (0.20, 0.60),
                "frequence": (0.10, 0.40),
                "coherence": (0.10, 0.40),
                "complexite": (0.05, 0.30)
            },
            algorithme="adaptive",
            iterations_max=100,
            convergence_seuil=0.001,
            taille_population=20,
            taux_mutation=0.1,
            validation_split=0.3
        )
        
        # Corpus apprentissage étendu
        self.corpus_apprentissage = self._generer_corpus_apprentissage()
        self.corpus_validation = self._generer_corpus_validation()
        
        # Historique optimisation
        self.historique_optimisation = []
        self.meilleurs_weights = None
        self.meilleur_score = 0.0
        
        # Patterns apprentissage découverts
        self.patterns_decouverts = {
            "contextes_efficaces": defaultdict(float),
            "combinations_gagnantes": [],
            "correlations_dhatu": defaultdict(list)
        }
    
    def _generer_corpus_apprentissage(self) -> List[Tuple[str, str, str, float]]:
        """Générer corpus d'apprentissage avec ground truth"""
        corpus = []
        
        # Expressions polysémiques avec score attendu
        expressions_polysemiques = [
            # Polysémie MODAL/QUANT forte
            ("probablement beaucoup", "recherche scientifique montre", "fr", 0.85),
            ("certainement nombreux", "données indiquent participants", "fr", 0.90),
            ("wahrscheinlich viel", "wissenschaftliche Studie zeigt", "de", 0.85),
            ("大概很多", "科学研究表明", "zh", 0.80),
            ("probably much", "scientific research shows", "en", 0.85),
            
            # Polysémie ASPECT/MODAL
            ("commence peut-être", "processus d'analyse va", "fr", 0.75),
            ("va certainement finir", "projet recherche doit", "fr", 0.80),
            ("fängt vielleicht an", "Analyseprozess wird", "de", 0.75),
            ("可能开始", "分析过程将", "zh", 0.70),
            ("might begin", "analysis process will", "en", 0.75),
            
            # Polysémie ASPECT/QUANT
            ("de plus en plus nombreux", "cas observés deviennent", "fr", 0.80),
            ("plusieurs fois commencer", "expérience doit être", "fr", 0.70),
            ("immer mehr", "Fälle werden beobachtet", "de", 0.80),
            ("越来越多", "观察到的案例", "zh", 0.75),
            ("more and more", "observed cases become", "en", 0.80),
            
            # Polysémie complexe tri-dhātu
            ("va probablement beaucoup augmenter", "nombre de cas va", "fr", 0.85),
            ("devrait certainement énormément diminuer", "fréquence erreur devrait", "fr", 0.85),
            ("wird wahrscheinlich viel steigen", "Anzahl der Fälle wird", "de", 0.80),
            ("可能会大大增加", "案例数量可能", "zh", 0.75),
            ("will probably increase much", "number of cases will", "en", 0.80),
            
            # Expressions simples (contrôle haute performance)
            ("impossible", "il est complètement", "fr", 0.95),
            ("beaucoup", "il y en a", "fr", 0.90),
            ("unmöglich", "es ist völlig", "de", 0.95),
            ("很多", "有", "zh", 0.90),
            ("impossible", "it is completely", "en", 0.95),
            
            # Expressions ambiguës (performance attendue faible)
            ("peut beaucoup", "il faut peut-être", "fr", 0.30),
            ("très finir", "c'est difficile de", "fr", 0.25),
            ("sehr beenden", "es ist schwer zu", "de", 0.25),
            ("很结束", "很难", "zh", 0.20),
            ("very finish", "it's hard to", "en", 0.25),
            
            # Expressions contexte scientifique fort
            ("significativement plus élevé", "résultats montrent niveau", "fr", 0.85),
            ("statistiquement probable", "analyse données suggère", "fr", 0.90),
            ("signifikant höher", "Ergebnisse zeigen Niveau", "de", 0.85),
            ("统计上可能", "数据分析表明", "zh", 0.80),
            ("statistically probable", "data analysis suggests", "en", 0.90)
        ]
        
        # Expressions avec variations contextuelles
        for expr, contexte_base, langue, score_attendu in expressions_polysemiques:
            # Contexte original
            corpus.append((expr, contexte_base, langue, score_attendu))
            
            # Variations contextuelles (± 0.1 score)
            variations_contexte = [
                f"étude {contexte_base}",
                f"{contexte_base} clairement",
                f"recherche approfondie {contexte_base}",
                f"{contexte_base} avec précision"
            ]
            
            for variation in variations_contexte:
                score_varie = max(0.1, min(0.95, score_attendu + random.uniform(-0.1, 0.1)))
                corpus.append((expr, variation, langue, score_varie))
        
        return corpus
    
    def _generer_corpus_validation(self) -> List[Tuple[str, str, str, float]]:
        """Générer corpus validation indépendant"""
        return [
            # Nouvelles expressions non vues pendant apprentissage
            ("très probablement nombreux", "étude récente montre", "fr", 0.85),
            ("könnte sehr viel werden", "neue Forschung zeigt", "de", 0.75),
            ("可能非常多", "最新研究显示", "zh", 0.75),
            ("might be very numerous", "recent study shows", "en", 0.80),
            
            ("commence certainement", "nouveau processus va", "fr", 0.80),
            ("wird sicher anfangen", "neuer Prozess wird", "de", 0.80),
            ("肯定会开始", "新过程将", "zh", 0.75),
            ("will certainly begin", "new process will", "en", 0.80),
            
            # Expressions difficiles
            ("peut-être beaucoup finir", "il faut", "fr", 0.40),
            ("vielleicht viel beenden", "man muss", "de", 0.35),
            ("可能很多结束", "需要", "zh", 0.30),
            ("maybe much finish", "one must", "en", 0.35)
        ]
    
    def evaluer_performance(self, weights: Dict[str, float], 
                          corpus: List[Tuple[str, str, str, float]]) -> MetriquePerformance:
        """Évaluer performance avec weights donnés"""
        
        # Mise à jour weights dans résolveur
        resolveur_test = ResolveurPolysemieContextuelle()
        resolveur_test.weights_scoring = weights.copy()
        
        scores_correlation = []
        reussites = 0
        confiances = []
        types_polysemie = Counter()
        
        for expression, contexte, langue, score_attendu in corpus:
            # Adaptation langue
            if langue != "fr":
                contextes_adaptes = self.extension_cross.adapter_contextes_discriminants(langue)
                resolveur_test.contextes_discriminants = contextes_adaptes
            
            # Analyse
            analyse = resolveur_test.resoudre_polysemie(expression, contexte)
            
            # Métriques
            confiance_obtenue = analyse.confiance_resolution
            confiances.append(confiance_obtenue)
            types_polysemie[analyse.type_polysemie] += 1
            
            # Corrélation avec score attendu
            correlation = 1.0 - abs(confiance_obtenue - score_attendu)
            scores_correlation.append(correlation)
            
            # Seuil réussite adaptatif
            seuil_reussite = max(0.5, score_attendu * 0.7)
            if confiance_obtenue >= seuil_reussite:
                reussites += 1
        
        # Calculs métriques
        taux_reussite = (reussites / len(corpus)) * 100 if corpus else 0
        confiance_moyenne = sum(confiances) / len(confiances) if confiances else 0
        correlation_moyenne = sum(scores_correlation) / len(scores_correlation) if scores_correlation else 0
        
        # Score composite pondéré
        score_composite = (
            taux_reussite * 0.4 +           # 40% taux réussite
            confiance_moyenne * 100 * 0.3 + # 30% confiance moyenne  
            correlation_moyenne * 100 * 0.3  # 30% corrélation ground truth
        )
        
        return MetriquePerformance(
            taux_reussite=taux_reussite,
            confiance_moyenne=confiance_moyenne,
            polysemies_resolues=types_polysemie.get("resolu_confiance", 0) + types_polysemie.get("resolu_incertain", 0),
            coherence_cross_linguistique=correlation_moyenne,
            score_composite=score_composite,
            distribution_types=dict(types_polysemie)
        )
    
    def optimisation_gradient_descent(self, config: ConfigurationOptimisation) -> ResultatOptimisation:
        """Optimisation par descente de gradient"""
        
        weights_actuels = config.weights_initiaux.copy()
        learning_rate = 0.01
        historique_scores = []
        
        meilleur_score = 0.0
        meilleurs_weights = weights_actuels.copy()
        iteration = 0
        
        for iteration in range(config.iterations_max):
            # Évaluation actuelle
            performance = self.evaluer_performance(weights_actuels, self.corpus_apprentissage)
            score_actuel = performance.score_composite
            historique_scores.append(score_actuel)
            
            # Mise à jour meilleur
            if score_actuel > meilleur_score:
                meilleur_score = score_actuel
                meilleurs_weights = weights_actuels.copy()
            
            # Calcul gradients (approximation numérique)
            gradients = {}
            epsilon = 0.001
            
            for weight_name in weights_actuels:
                # Perturbation positive
                weights_plus = weights_actuels.copy()
                weights_plus[weight_name] += epsilon
                weights_plus = self._normaliser_weights(weights_plus)
                
                performance_plus = self.evaluer_performance(weights_plus, self.corpus_apprentissage)
                
                # Gradient approximé
                gradient = (performance_plus.score_composite - score_actuel) / epsilon
                gradients[weight_name] = gradient
            
            # Mise à jour weights
            for weight_name in weights_actuels:
                weights_actuels[weight_name] += learning_rate * gradients[weight_name]
            
            # Normalisation et contraintes
            weights_actuels = self._normaliser_weights(weights_actuels)
            weights_actuels = self._appliquer_contraintes(weights_actuels, config.plage_optimisation)
            
            # Convergence
            if iteration > 10:
                amelioration_recente = abs(historique_scores[-1] - historique_scores[-10])
                if amelioration_recente < config.convergence_seuil:
                    break
        
        # Calcul amélioration
        score_initial = historique_scores[0] if historique_scores else 0
        amelioration = ((meilleur_score - score_initial) / score_initial * 100) if score_initial > 0 else 0
        
        return ResultatOptimisation(
            weights_optimaux=meilleurs_weights,
            score_performance=meilleur_score,
            iterations_convergence=iteration + 1,
            historique_scores=historique_scores,
            amelioration_relative=amelioration,
            configurations_testees=iteration + 1,
            temps_optimisation=0.0  # À implémenter si nécessaire
        )
    
    def optimisation_genetique(self, config: ConfigurationOptimisation) -> ResultatOptimisation:
        """Optimisation par algorithme génétique"""
        
        # Population initiale
        population = []
        for _ in range(config.taille_population):
            individu = {}
            for weight_name, (min_val, max_val) in config.plage_optimisation.items():
                individu[weight_name] = random.uniform(min_val, max_val)
            individu = self._normaliser_weights(individu)
            population.append(individu)
        
        historique_scores = []
        meilleur_score = 0.0
        meilleurs_weights = None
        
        for generation in range(config.iterations_max):
            # Évaluation population
            fitness_scores = []
            for individu in population:
                performance = self.evaluer_performance(individu, self.corpus_apprentissage)
                fitness_scores.append(performance.score_composite)
            
            # Mise à jour meilleur
            score_generation = max(fitness_scores)
            historique_scores.append(score_generation)
            
            if score_generation > meilleur_score:
                meilleur_score = score_generation
                meilleur_idx = fitness_scores.index(score_generation)
                meilleurs_weights = population[meilleur_idx].copy()
            
            # Sélection (tournoi)
            nouvelle_population = []
            for _ in range(config.taille_population):
                parent1 = self._selection_tournoi(population, fitness_scores)
                parent2 = self._selection_tournoi(population, fitness_scores)
                
                # Croisement
                enfant = self._croisement(parent1, parent2)
                
                # Mutation
                if random.random() < config.taux_mutation:
                    enfant = self._mutation(enfant, config.plage_optimisation)
                
                nouvelle_population.append(enfant)
            
            population = nouvelle_population
            
            # Convergence
            if generation > 20:
                stabilite = np.std(historique_scores[-10:])
                if stabilite < config.convergence_seuil:
                    break
        
        score_initial = historique_scores[0] if historique_scores else 0
        amelioration = ((meilleur_score - score_initial) / score_initial * 100) if score_initial > 0 else 0
        
        return ResultatOptimisation(
            weights_optimaux=meilleurs_weights,
            score_performance=meilleur_score,
            iterations_convergence=generation + 1,
            historique_scores=historique_scores,
            amelioration_relative=amelioration,
            configurations_testees=generation * config.taille_population,
            temps_optimisation=0.0
        )
    
    def optimisation_adaptive(self, config: ConfigurationOptimisation) -> ResultatOptimisation:
        """Optimisation adaptative hybride (gradient + génétique)"""
        
        # Phase 1: Exploration génétique (50% iterations)
        config_genetique = config
        config_genetique.iterations_max = config.iterations_max // 2
        
        resultat_genetique = self.optimisation_genetique(config_genetique)
        
        # Phase 2: Raffinement gradient descent
        config_gradient = config
        config_gradient.weights_initiaux = resultat_genetique.weights_optimaux
        config_gradient.iterations_max = config.iterations_max - config_genetique.iterations_max
        
        resultat_gradient = self.optimisation_gradient_descent(config_gradient)
        
        # Combinaison résultats
        historique_combine = resultat_genetique.historique_scores + resultat_gradient.historique_scores
        
        # Sélection meilleur
        if resultat_gradient.score_performance > resultat_genetique.score_performance:
            meilleur_resultat = resultat_gradient
        else:
            meilleur_resultat = resultat_genetique
        
        return ResultatOptimisation(
            weights_optimaux=meilleur_resultat.weights_optimaux,
            score_performance=meilleur_resultat.score_performance,
            iterations_convergence=len(historique_combine),
            historique_scores=historique_combine,
            amelioration_relative=meilleur_resultat.amelioration_relative,
            configurations_testees=resultat_genetique.configurations_testees + resultat_gradient.configurations_testees,
            temps_optimisation=0.0
        )
    
    def _normaliser_weights(self, weights: Dict[str, float]) -> Dict[str, float]:
        """Normaliser weights pour somme = 1.0"""
        total = sum(weights.values())
        if total > 0:
            return {k: v / total for k, v in weights.items()}
        return weights
    
    def _appliquer_contraintes(self, weights: Dict[str, float], 
                             contraintes: Dict[str, Tuple[float, float]]) -> Dict[str, float]:
        """Appliquer contraintes min/max aux weights"""
        weights_contraints = {}
        for weight_name, valeur in weights.items():
            if weight_name in contraintes:
                min_val, max_val = contraintes[weight_name]
                weights_contraints[weight_name] = max(min_val, min(max_val, valeur))
            else:
                weights_contraints[weight_name] = valeur
        
        return self._normaliser_weights(weights_contraints)
    
    def _selection_tournoi(self, population: List[Dict], fitness_scores: List[float], 
                          taille_tournoi: int = 3) -> Dict[str, float]:
        """Sélection par tournoi pour algorithme génétique"""
        indices_tournoi = random.sample(range(len(population)), min(taille_tournoi, len(population)))
        meilleur_idx = max(indices_tournoi, key=lambda i: fitness_scores[i])
        return population[meilleur_idx].copy()
    
    def _croisement(self, parent1: Dict[str, float], parent2: Dict[str, float]) -> Dict[str, float]:
        """Croisement uniforme pour algorithme génétique"""
        enfant = {}
        for weight_name in parent1:
            if random.random() < 0.5:
                enfant[weight_name] = parent1[weight_name]
            else:
                enfant[weight_name] = parent2[weight_name]
        
        return self._normaliser_weights(enfant)
    
    def _mutation(self, individu: Dict[str, float], 
                  contraintes: Dict[str, Tuple[float, float]]) -> Dict[str, float]:
        """Mutation gaussienne pour algorithme génétique"""
        individu_mute = individu.copy()
        
        # Sélection aléatoire d'un weight à muter
        weight_a_muter = random.choice(list(individu.keys()))
        
        # Mutation gaussienne
        if weight_a_muter in contraintes:
            min_val, max_val = contraintes[weight_a_muter]
            ecart_type = (max_val - min_val) * 0.1  # 10% de la plage
            mutation = random.gauss(0, ecart_type)
            
            nouvelle_valeur = individu_mute[weight_a_muter] + mutation
            individu_mute[weight_a_muter] = max(min_val, min(max_val, nouvelle_valeur))
        
        return self._normaliser_weights(individu_mute)
    
    def optimiser_scoring(self, config: Optional[ConfigurationOptimisation] = None) -> ResultatOptimisation:
        """Optimisation principale du scoring contextuel"""
        
        if config is None:
            config = self.config_default
        
        print(f"🎯 OPTIMISATION SCORING CONTEXTUEL - {config.algorithme.upper()}")
        print(f"Corpus apprentissage: {len(self.corpus_apprentissage)} expressions")
        print(f"Corpus validation: {len(self.corpus_validation)} expressions")
        print("="*60)
        
        # Évaluation baseline
        performance_baseline = self.evaluer_performance(config.weights_initiaux, self.corpus_apprentissage)
        print(f"📊 Performance baseline: {performance_baseline.score_composite:.1f}%")
        print(f"   Taux réussite: {performance_baseline.taux_reussite:.1f}%")
        print(f"   Confiance moyenne: {performance_baseline.confiance_moyenne:.3f}")
        
        # Optimisation selon algorithme
        if config.algorithme == "gradient_descent":
            resultat = self.optimisation_gradient_descent(config)
        elif config.algorithme == "genetic":
            resultat = self.optimisation_genetique(config)
        elif config.algorithme == "adaptive":
            resultat = self.optimisation_adaptive(config)
        else:
            raise ValueError(f"Algorithme inconnu: {config.algorithme}")
        
        # Validation sur corpus indépendant
        performance_validation = self.evaluer_performance(resultat.weights_optimaux, self.corpus_validation)
        
        # Sauvegarde historique
        self.historique_optimisation.append({
            "algorithme": config.algorithme,
            "performance_baseline": asdict(performance_baseline),
            "resultat_optimisation": asdict(resultat),
            "performance_validation": asdict(performance_validation)
        })
        
        # Mise à jour meilleurs weights globaux
        if performance_validation.score_composite > self.meilleur_score:
            self.meilleur_score = performance_validation.score_composite
            self.meilleurs_weights = resultat.weights_optimaux.copy()
        
        return resultat
    
    def valider_optimisation(self, weights_optimaux: Dict[str, float]) -> Dict[str, Any]:
        """Validation finale de l'optimisation"""
        
        print(f"\n🎊 VALIDATION OPTIMISATION FINALE")
        print("="*33)
        
        # Test sur corpus validation
        performance_validation = self.evaluer_performance(weights_optimaux, self.corpus_validation)
        
        # Test cross-linguistique étendu
        expressions_cross = [
            ("probablement beaucoup", "recherche scientifique", "fr"),
            ("wahrscheinlich viel", "wissenschaftliche Forschung", "de"),
            ("大概很多", "科学研究", "zh"),
            ("probably much", "scientific research", "en")
        ]
        
        coherences_cross = []
        for expr, contexte, langue in expressions_cross:
            resultat_cross = self.extension_cross.resoudre_polysemie_multilingue(expr, contexte, langue)
            coherences_cross.append(resultat_cross.coherence_cross_linguistique)
        
        coherence_cross_moyenne = sum(coherences_cross) / len(coherences_cross)
        
        # Calcul score final global
        score_global = (
            performance_validation.score_composite * 0.6 +      # 60% performance validation
            coherence_cross_moyenne * 100 * 0.4                # 40% cohérence cross-linguistique
        )
        
        # Validation objectifs
        objectif_taux_reussite = 70.0
        objectif_confiance = 0.6
        objectif_coherence_cross = 0.5
        
        validation_reussie = (
            performance_validation.taux_reussite >= objectif_taux_reussite and
            performance_validation.confiance_moyenne >= objectif_confiance and
            coherence_cross_moyenne >= objectif_coherence_cross
        )
        
        return {
            "weights_optimaux": weights_optimaux,
            "performance_validation": asdict(performance_validation),
            "coherence_cross_linguistique": coherence_cross_moyenne,
            "score_global": score_global,
            "validation_reussie": validation_reussie,
            "objectifs": {
                "taux_reussite": f"{performance_validation.taux_reussite:.1f}% ({'✅' if performance_validation.taux_reussite >= objectif_taux_reussite else '❌'} {objectif_taux_reussite}%)",
                "confiance_moyenne": f"{performance_validation.confiance_moyenne:.3f} ({'✅' if performance_validation.confiance_moyenne >= objectif_confiance else '❌'} {objectif_confiance})",
                "coherence_cross": f"{coherence_cross_moyenne:.3f} ({'✅' if coherence_cross_moyenne >= objectif_coherence_cross else '❌'} {objectif_coherence_cross})"
            }
        }


def main():
    """Test optimisation scoring contextuel avancé"""
    print("🎯 OPTIMISEUR SCORING CONTEXTUEL AVANCÉ")
    print("Machine learning adaptatif pour >70% réussite polysémie")
    print("="*65)
    
    # Initialisation optimiseur
    optimiseur = OptimiseurScoringContextuel()
    
    # Configuration optimisation
    config = ConfigurationOptimisation(
        weights_initiaux={
            "contexte": 0.40,
            "frequence": 0.25,
            "coherence": 0.20,
            "complexite": 0.15
        },
        plage_optimisation={
            "contexte": (0.25, 0.65),
            "frequence": (0.10, 0.35),
            "coherence": (0.10, 0.35),
            "complexite": (0.05, 0.25)
        },
        algorithme="adaptive",  # Hybride pour meilleurs résultats
        iterations_max=50,
        convergence_seuil=0.005,
        taille_population=15,
        taux_mutation=0.15,
        validation_split=0.3
    )
    
    print(f"📊 Configuration optimisation:")
    print(f"   Algorithme: {config.algorithme}")
    print(f"   Iterations max: {config.iterations_max}")
    print(f"   Population: {config.taille_population}")
    print(f"   Corpus apprentissage: {len(optimiseur.corpus_apprentissage)}")
    print(f"   Corpus validation: {len(optimiseur.corpus_validation)}")
    
    # Optimisation
    resultat = optimiseur.optimiser_scoring(config)
    
    print(f"\n📈 RÉSULTATS OPTIMISATION:")
    print("="*26)
    print(f"✅ Score performance: {resultat.score_performance:.1f}%")
    print(f"✅ Iterations convergence: {resultat.iterations_convergence}")
    print(f"✅ Amélioration: +{resultat.amelioration_relative:.1f}%")
    print(f"✅ Configurations testées: {resultat.configurations_testees}")
    
    print(f"\n🎯 WEIGHTS OPTIMAUX:")
    print("="*18)
    for weight_name, valeur in resultat.weights_optimaux.items():
        print(f"   {weight_name}: {valeur:.3f}")
    
    # Validation finale
    validation = optimiseur.valider_optimisation(resultat.weights_optimaux)
    
    print(f"\n🎊 VALIDATION FINALE:")
    print("="*19)
    print(f"✅ Score global: {validation['score_global']:.1f}%")
    print(f"✅ Validation réussie: {'✅ OUI' if validation['validation_reussie'] else '❌ NON'}")
    
    print(f"\n🎯 OBJECTIFS:")
    print("="*10)
    for objectif, status in validation["objectifs"].items():
        print(f"   {objectif}: {status}")
    
    # Sauvegarde résultats
    fichier_resultats = "optimisation_scoring_contextuel_resultats.json"
    resultats_complets = {
        "configuration": asdict(config),
        "resultat_optimisation": asdict(resultat),
        "validation_finale": validation,
        "historique": optimiseur.historique_optimisation
    }
    
    with open(fichier_resultats, "w", encoding="utf-8") as f:
        json.dump(resultats_complets, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Résultats sauvegardés: {fichier_resultats}")
    
    if validation['validation_reussie']:
        print(f"\n🚀 OPTIMISATION SCORING RÉUSSIE!")
        print("✅ Système dhātu prêt pour production")
        print("✅ Polysémie contextuelle optimisée")
        print("✅ Support cross-linguistique validé")
    else:
        print(f"\n⚠️ Optimisation à poursuivre:")
        print("- Ajuster paramètres optimisation")
        print("- Enrichir corpus apprentissage")
        print("- Tester autres algorithmes ML")
    
    return optimiseur, resultat, validation

if __name__ == "__main__":
    optimiseur, resultat, validation = main()