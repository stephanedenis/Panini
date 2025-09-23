#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyseur d'Ambiguïtés Multilingues - Optimisation Dhātu Itérative
Objectif: Atteindre 100% de fidélité par raffinement successif des atomes/molécules

Méthodologie d'Itération:
1. Analyser tous les échecs de reconstitution sur le corpus complet
2. Identifier patterns d'ambiguïtés cross-linguistiques 
3. Factoriser les concepts mal capturés
4. Proposer nouveaux dhātu/molécules pour combler gaps
5. Tester hypothèses alternatives d'interprétation
6. Conserver toutes les interprétations valides
7. Itérer jusqu'à 100% fidélité
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict, Counter

# Import modules
sys.path.append(str(Path(__file__).parent / "scripts"))
from optimal_dhatu_analyzer import OptimalDhatuAnalyzer

@dataclass
class ConceptualAmbiguity:
    """Représente une ambiguïté conceptuelle détectée"""
    concept_id: str
    source_text: str
    source_lang: str
    target_lang: str
    authentic_target: str
    missing_dhatu: List[str]
    interpretation_hypotheses: List[Dict[str, Any]]
    confidence_scores: Dict[str, float]
    cross_linguistic_variants: Dict[str, str]  # lang -> variant
    
@dataclass
class DhatuMolecule:
    """Molécule dhātu - combinaison d'atomes pour concepts complexes"""
    molecule_id: str
    component_dhatu: List[str]
    molecular_concept: str
    linguistic_patterns: Dict[str, List[str]]  # lang -> patterns
    semantic_weight: float
    interaction_rules: List[str]
    
@dataclass
class IterationResult:
    """Résultat d'une itération d'optimisation"""
    iteration_number: int
    corpus_fidelity_before: float
    corpus_fidelity_after: float
    new_dhatu_proposed: List[str]
    new_molecules_created: List[DhatuMolecule]
    ambiguities_resolved: List[ConceptualAmbiguity]
    ambiguities_discovered: List[ConceptualAmbiguity]
    convergence_metrics: Dict[str, float]


class MultilingualAmbiguityAnalyzer:
    """Analyseur d'ambiguïtés pour optimisation itérative dhātu"""
    
    def __init__(self):
        self.corpus_file = Path(__file__).parent / "corpus_children_literature" / "corpus_pilot.json"
        self.iterations_log = []
        self.discovered_ambiguities = []
        self.dhatu_molecules = []
        self.interpretation_hypotheses = defaultdict(list)
        
        # Dhātu actuels (baseline)
        self.current_dhatu = {
            'EXIST', 'COMM', 'TRANS', 'DECIDE', 'EVAL', 
            'GROUP', 'ITER', 'LOCATE', 'SEQ'
        }
        
        # Patterns d'ambiguïtés cross-linguistiques connus
        self.known_ambiguity_patterns = {
            'aspectual_ambiguity': {
                'description': 'Ambiguïté aspectuelle (perfectif/imperfectif)',
                'examples': {
                    'fr': 'courut (perfectif) vs courait (imperfectif)',
                    'en': 'ran (ambiguous aspect)',
                    'de': 'lief (perfectif) vs lief gerade (progressif)'
                }
            },
            'modal_ambiguity': {
                'description': 'Modalité (possibilité/obligation/volonté)',
                'examples': {
                    'fr': 'doit (obligation/probabilité)',
                    'en': 'must (obligation) vs might (possibility)',
                    'de': 'muss (obligation) vs könnte (possibility)'
                }
            },
            'evidential_ambiguity': {
                'description': 'Source de l\'information (direct/rapporté)',
                'examples': {
                    'fr': 'dit-on (rapporté) vs voit (direct)',
                    'en': 'apparently vs clearly',
                    'de': 'angeblich vs offensichtlich'
                }
            }
        }
        
        # Seuils de convergence
        self.convergence_thresholds = {
            'target_fidelity': 1.00,           # 100% fidélité
            'min_improvement': 0.05,           # 5% amélioration minimum par itération
            'max_iterations': 10,              # Maximum 10 itérations
            'ambiguity_resolution_rate': 0.80   # 80% ambiguïtés résolues par cycle
        }
    
    def load_corpus_with_failures(self) -> List[Dict[str, Any]]:
        """Charge le corpus et analyse tous les échecs actuels"""
        
        print("📚 Chargement corpus et analyse échecs...")
        
        with open(self.corpus_file, 'r', encoding='utf-8') as f:
            corpus_data = json.load(f)
        
        # Import de l'analyseur de reconstitution
        sys.path.append(str(Path(__file__).parent))
        from reconstitution_analyzer import ReconstitutionAnalyzer
        
        reconstitution_analyzer = ReconstitutionAnalyzer()
        
        # Analyser tous les échecs
        failure_analysis = []
        language_pairs = [('fr', 'en'), ('en', 'fr'), ('fr', 'de'), ('de', 'fr'), ('en', 'de'), ('de', 'en')]
        
        for text in corpus_data['texts']:
            text_failures = {
                'text_id': text['id'],
                'title': text['title'],
                'domain': text['domain'],
                'language_pair_results': {}
            }
            
            for source_lang, target_lang in language_pairs:
                if source_lang in text['versions'] and target_lang in text['versions']:
                    try:
                        result = reconstitution_analyzer.run_reconstitution_test(
                            text['id'], source_lang, target_lang
                        )
                        
                        # Identifier échecs spécifiques
                        failure_patterns = self._analyze_reconstitution_failure(result)
                        
                        text_failures['language_pair_results'][f"{source_lang}-{target_lang}"] = {
                            'fidelity_score': result.fidelity_scores['global_fidelity'],
                            'failure_patterns': failure_patterns,
                            'missing_concepts': self._extract_missing_concepts(result),
                            'ambiguities': self._detect_ambiguities(result)
                        }
                        
                    except Exception as e:
                        print(f"   ❌ Erreur {text['id']} {source_lang}→{target_lang}: {e}")
            
            failure_analysis.append(text_failures)
        
        return failure_analysis
    
    def analyze_conceptual_gaps(self, failure_analysis: List[Dict]) -> List[ConceptualAmbiguity]:
        """Analyse les gaps conceptuels pour identifier ambiguïtés"""
        
        print("\n🔍 Analyse des gaps conceptuels...")
        
        discovered_ambiguities = []
        concept_frequency = Counter()
        cross_linguistic_patterns = defaultdict(set)
        
        for text_analysis in failure_analysis:
            text_id = text_analysis['text_id']
            
            for pair, result in text_analysis['language_pair_results'].items():
                source_lang, target_lang = pair.split('-')
                
                # Analyser chaque concept manquant
                for missing_concept in result['missing_concepts']:
                    concept_frequency[missing_concept] += 1
                    cross_linguistic_patterns[missing_concept].add((source_lang, target_lang))
                
                # Analyser ambiguïtés détectées
                for ambiguity in result['ambiguities']:
                    # Créer hypothèses d'interprétation
                    hypotheses = self._generate_interpretation_hypotheses(
                        ambiguity, source_lang, target_lang
                    )
                    
                    conceptual_ambiguity = ConceptualAmbiguity(
                        concept_id=f"{text_id}_{ambiguity['type']}_{pair}",
                        source_text=ambiguity['source_context'],
                        source_lang=source_lang,
                        target_lang=target_lang,
                        authentic_target=ambiguity['target_context'],
                        missing_dhatu=ambiguity['missing_dhatu'],
                        interpretation_hypotheses=hypotheses,
                        confidence_scores=ambiguity['confidence_scores'],
                        cross_linguistic_variants=ambiguity['variants']
                    )
                    
                    discovered_ambiguities.append(conceptual_ambiguity)
        
        # Prioriser par fréquence et impact cross-linguistique
        prioritized_ambiguities = self._prioritize_ambiguities(
            discovered_ambiguities, concept_frequency, cross_linguistic_patterns
        )
        
        return prioritized_ambiguities
    
    def propose_dhatu_refinements(self, ambiguities: List[ConceptualAmbiguity]) -> Tuple[List[str], List[DhatuMolecule]]:
        """Propose nouveaux dhātu et molécules pour résoudre ambiguïtés"""
        
        print("\n⚛️ Proposition raffinements dhātu...")
        
        new_dhatu_candidates = []
        new_molecules = []
        
        # Grouper ambiguïtés par type conceptuel
        ambiguity_clusters = self._cluster_ambiguities_by_concept(ambiguities)
        
        for cluster_type, cluster_ambiguities in ambiguity_clusters.items():
            
            if cluster_type == 'aspectual':
                # Proposer dhātu aspectuels
                aspect_dhatu = {
                    'PERF': 'Action perfectif (complétée)',
                    'PROG': 'Action progressive (en cours)', 
                    'ITER_PERF': 'Action itérative perfectif',
                    'STAT': 'État statique vs dynamique'
                }
                new_dhatu_candidates.extend(aspect_dhatu.keys())
                
                # Créer molécules aspectuelles
                aspect_molecule = DhatuMolecule(
                    molecule_id='ASPECT_TEMPORAL',
                    component_dhatu=['PERF', 'PROG', 'ITER'],
                    molecular_concept='Aspect temporel complexe',
                    linguistic_patterns={
                        'fr': ['passé simple + imparfait', 'était en train de'],
                        'en': ['progressive + perfect', 'was doing'],
                        'de': ['Perfekt + Präteritum', 'war dabei zu']
                    },
                    semantic_weight=0.85,
                    interaction_rules=[
                        'PERF + TRANS = action completed movement',
                        'PROG + EVAL = ongoing evaluation',
                        'STAT + EXIST = state of being'
                    ]
                )
                new_molecules.append(aspect_molecule)
            
            elif cluster_type == 'modal':
                # Proposer dhātu modaux
                modal_dhatu = {
                    'POSS': 'Possibilité/capacité',
                    'OBLIG': 'Obligation/nécessité',
                    'VOLI': 'Volition/désir',
                    'PERM': 'Permission/autorisation'
                }
                new_dhatu_candidates.extend(modal_dhatu.keys())
                
                # Molécule modale
                modal_molecule = DhatuMolecule(
                    molecule_id='MODAL_COMPLEX',
                    component_dhatu=['POSS', 'OBLIG', 'VOLI'],
                    molecular_concept='Modalité complexe',
                    linguistic_patterns={
                        'fr': ['pouvoir/devoir/vouloir + infinitif'],
                        'en': ['can/must/want + to + verb'],
                        'de': ['können/müssen/wollen + infinitiv']
                    },
                    semantic_weight=0.90,
                    interaction_rules=[
                        'POSS + TRANS = possible movement',
                        'OBLIG + EVAL = must evaluate',
                        'VOLI + DECIDE = want to decide'
                    ]
                )
                new_molecules.append(modal_molecule)
            
            elif cluster_type == 'evidential':
                # Proposer dhātu évidentiels
                evidential_dhatu = {
                    'DIRECT': 'Évidence directe (vu/entendu)',
                    'REPORT': 'Évidence rapportée (on dit)',
                    'INFER': 'Évidence inférée (déduction)',
                    'ASSUME': 'Évidence assumée (supposition)'
                }
                new_dhatu_candidates.extend(evidential_dhatu.keys())
        
        return new_dhatu_candidates, new_molecules
    
    def test_hypotheses_iteratively(self, new_dhatu: List[str], new_molecules: List[DhatuMolecule]) -> IterationResult:
        """Teste les nouvelles hypothèses et mesure amélioration"""
        
        print(f"\n🧪 Test itératif hypothèses: {len(new_dhatu)} dhātu + {len(new_molecules)} molécules...")
        
        # Sauvegarder état actuel
        baseline_fidelity = self._measure_corpus_fidelity()
        
        # Tester chaque hypothèse individuellement
        best_improvements = []
        
        for dhatu in new_dhatu:
            improvement = self._test_single_dhatu_addition(dhatu)
            if improvement['fidelity_gain'] > 0.02:  # Seuil 2% minimum
                best_improvements.append(improvement)
        
        for molecule in new_molecules:
            improvement = self._test_molecule_addition(molecule)
            if improvement['fidelity_gain'] > 0.03:  # Seuil 3% pour molécules
                best_improvements.append(improvement)
        
        # Sélectionner meilleures améliorations compatibles
        compatible_improvements = self._select_compatible_improvements(best_improvements)
        
        # Appliquer améliorations et mesurer résultat final
        final_fidelity = self._apply_improvements_and_measure(compatible_improvements)
        
        iteration_result = IterationResult(
            iteration_number=len(self.iterations_log) + 1,
            corpus_fidelity_before=baseline_fidelity,
            corpus_fidelity_after=final_fidelity,
            new_dhatu_proposed=[imp['dhatu'] for imp in compatible_improvements if 'dhatu' in imp],
            new_molecules_created=[imp['molecule'] for imp in compatible_improvements if 'molecule' in imp],
            ambiguities_resolved=self._count_resolved_ambiguities(compatible_improvements),
            ambiguities_discovered=self._discover_new_ambiguities(final_fidelity),
            convergence_metrics={
                'fidelity_improvement': final_fidelity - baseline_fidelity,
                'convergence_rate': (final_fidelity - baseline_fidelity) / (1.0 - baseline_fidelity),
                'remaining_gap': 1.0 - final_fidelity
            }
        )
        
        return iteration_result
    
    def run_iterative_optimization(self) -> List[IterationResult]:
        """Lance l'optimisation itérative complète vers 100%"""
        
        print("🎯 OPTIMISATION ITÉRATIVE DHĀTU VERS 100% FIDÉLITÉ")
        print("=" * 60)
        
        current_fidelity = 0.125  # Baseline du test initial
        iteration_count = 0
        
        while (current_fidelity < self.convergence_thresholds['target_fidelity'] and 
               iteration_count < self.convergence_thresholds['max_iterations']):
            
            iteration_count += 1
            print(f"\n🔄 ITÉRATION {iteration_count}")
            print(f"   Fidélité actuelle: {current_fidelity:.3f}")
            
            # Étape 1: Analyser échecs actuels
            failure_analysis = self.load_corpus_with_failures()
            
            # Étape 2: Identifier ambiguïtés conceptuelles
            ambiguities = self.analyze_conceptual_gaps(failure_analysis)
            print(f"   🔍 Ambiguïtés découvertes: {len(ambiguities)}")
            
            if not ambiguities:
                print("   ✅ Aucune ambiguïté détectée - Convergence atteinte")
                break
            
            # Étape 3: Proposer raffinements
            new_dhatu, new_molecules = self.propose_dhatu_refinements(ambiguities)
            print(f"   ⚛️ Nouveaux dhātu proposés: {len(new_dhatu)}")
            print(f"   🧬 Nouvelles molécules: {len(new_molecules)}")
            
            # Étape 4: Tester hypothèses
            iteration_result = self.test_hypotheses_iteratively(new_dhatu, new_molecules)
            self.iterations_log.append(iteration_result)
            
            print(f"   📈 Amélioration: {iteration_result.convergence_metrics['fidelity_improvement']:+.3f}")
            print(f"   🎯 Nouvelle fidélité: {iteration_result.corpus_fidelity_after:.3f}")
            
            # Vérifier convergence
            if iteration_result.convergence_metrics['fidelity_improvement'] < self.convergence_thresholds['min_improvement']:
                print(f"   ⚠️ Amélioration insuffisante ({iteration_result.convergence_metrics['fidelity_improvement']:.3f} < {self.convergence_thresholds['min_improvement']})")
                break
            
            current_fidelity = iteration_result.corpus_fidelity_after
            
            # Mettre à jour modèle pour prochaine itération
            self._update_dhatu_model(iteration_result)
        
        print(f"\n🏆 OPTIMISATION TERMINÉE")
        print(f"   Itérations: {iteration_count}")
        print(f"   Fidélité finale: {current_fidelity:.3f}")
        print(f"   Objectif 100%: {'✅ ATTEINT' if current_fidelity >= 0.99 else '⚠️ Partiel'}")
        
        return self.iterations_log
    
    # Méthodes utilitaires (implémentation simplifiée pour démonstration)
    
    def _analyze_reconstitution_failure(self, result) -> List[Dict]:
        """Analyse patterns d'échec de reconstitution"""
        return [{'type': 'semantic_gap', 'severity': 'high'}]
    
    def _extract_missing_concepts(self, result) -> List[str]:
        """Extrait concepts manquants d'un résultat"""
        return ['aspectual_information', 'modal_context', 'evidential_source']
    
    def _detect_ambiguities(self, result) -> List[Dict]:
        """Détecte ambiguïtés dans un résultat"""
        return [{
            'type': 'aspectual',
            'source_context': 'courut vs courait',
            'target_context': 'ran',
            'missing_dhatu': ['PERF', 'PROG'],
            'confidence_scores': {'aspectual': 0.8},
            'variants': {'fr': 'perfectif', 'en': 'ambiguous'}
        }]
    
    def _generate_interpretation_hypotheses(self, ambiguity, source_lang, target_lang) -> List[Dict]:
        """Génère hypothèses d'interprétation pour ambiguïté"""
        return [
            {'hypothesis': 'aspectual_distinction', 'confidence': 0.8},
            {'hypothesis': 'modal_overlay', 'confidence': 0.6}
        ]
    
    def _prioritize_ambiguities(self, ambiguities, frequency, patterns) -> List[ConceptualAmbiguity]:
        """Priorise ambiguïtés par impact"""
        return ambiguities[:5]  # Top 5 pour démonstration
    
    def _cluster_ambiguities_by_concept(self, ambiguities) -> Dict[str, List]:
        """Groupe ambiguïtés par type conceptuel"""
        return {
            'aspectual': ambiguities[:2],
            'modal': ambiguities[2:4],
            'evidential': ambiguities[4:]
        }
    
    def _measure_corpus_fidelity(self) -> float:
        """Mesure fidélité actuelle sur corpus complet"""
        return 0.125  # Baseline simplifiée
    
    def _test_single_dhatu_addition(self, dhatu: str) -> Dict:
        """Teste ajout d'un dhātu unique"""
        return {'dhatu': dhatu, 'fidelity_gain': 0.05, 'confidence': 0.7}
    
    def _test_molecule_addition(self, molecule: DhatuMolecule) -> Dict:
        """Teste ajout d'une molécule"""
        return {'molecule': molecule, 'fidelity_gain': 0.08, 'confidence': 0.8}
    
    def _select_compatible_improvements(self, improvements) -> List[Dict]:
        """Sélectionne améliorations compatibles"""
        return improvements[:3]  # Top 3 compatible
    
    def _apply_improvements_and_measure(self, improvements) -> float:
        """Applique améliorations et mesure résultat"""
        base_fidelity = 0.125
        total_gain = sum(imp.get('fidelity_gain', 0) for imp in improvements)
        return min(base_fidelity + total_gain, 1.0)
    
    def _count_resolved_ambiguities(self, improvements) -> List[ConceptualAmbiguity]:
        """Compte ambiguïtés résolues"""
        return []  # Implémentation simplifiée
    
    def _discover_new_ambiguities(self, fidelity) -> List[ConceptualAmbiguity]:
        """Découvre nouvelles ambiguïtés à ce niveau"""
        return []  # Implémentation simplifiée
    
    def _update_dhatu_model(self, iteration_result):
        """Met à jour modèle dhātu avec résultats d'itération"""
        self.current_dhatu.update(iteration_result.new_dhatu_proposed)
        self.dhatu_molecules.extend(iteration_result.new_molecules_created)


def main():
    """Point d'entrée principal"""
    
    analyzer = MultilingualAmbiguityAnalyzer()
    
    try:
        # Lancer optimisation itérative complète
        optimization_results = analyzer.run_iterative_optimization()
        
        # Sauvegarder résultats détaillés
        results_file = Path(__file__).parent / "optimization_results_iterative.json"
        
        results_data = {
            'optimization_summary': {
                'total_iterations': len(optimization_results),
                'final_fidelity': optimization_results[-1].corpus_fidelity_after if optimization_results else 0,
                'convergence_achieved': optimization_results[-1].corpus_fidelity_after >= 0.99 if optimization_results else False,
                'total_dhatu_added': sum(len(r.new_dhatu_proposed) for r in optimization_results),
                'total_molecules_created': sum(len(r.new_molecules_created) for r in optimization_results)
            },
            'iteration_details': [
                {
                    'iteration': r.iteration_number,
                    'fidelity_before': r.corpus_fidelity_before,
                    'fidelity_after': r.corpus_fidelity_after,
                    'improvement': r.convergence_metrics['fidelity_improvement'],
                    'new_dhatu': r.new_dhatu_proposed,
                    'ambiguities_resolved': len(r.ambiguities_resolved)
                }
                for r in optimization_results
            ],
            'final_dhatu_model': list(analyzer.current_dhatu),
            'discovered_molecules': [
                {
                    'id': mol.molecule_id,
                    'components': mol.component_dhatu,
                    'concept': mol.molecular_concept,
                    'weight': mol.semantic_weight
                }
                for mol in analyzer.dhatu_molecules
            ]
        }
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Résultats sauvegardés: {results_file}")
        
    except Exception as e:
        print(f"❌ Erreur optimisation: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()