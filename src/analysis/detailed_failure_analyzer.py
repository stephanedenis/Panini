#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyseur Détaillé des Patterns d'Échec - Diagnostic Dhātu
Objectif: Identifier précisément pourquoi la reconstitution échoue
         et quelles ambiguïtés conceptuelles bloquent la progression vers 100%

Focus: Analyse fine des décalages sémantiques entre langues
       pour découvrir la structure intentionnelle cachée
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from collections import defaultdict, Counter
import sys

# Import modules
sys.path.append(str(Path(__file__).parent / "scripts"))


@dataclass
class SemanticMismatch:
    """Décalage sémantique spécifique entre source et cible"""
    mismatch_id: str
    source_segment: str
    source_lang: str
    target_segment: str
    target_lang: str
    reconstructed_segment: str
    mismatch_type: str  # lexical, structural, aspectual, modal, etc.
    semantic_distance: float
    missing_concepts: List[str]
    interpretation_variants: List[Dict[str, Any]]
    confidence_level: float


@dataclass
class ConceptualGap:
    """Gap conceptuel non résolu par les dhātu actuels"""
    gap_id: str
    concept_name: str
    frequency_across_corpus: int
    cross_linguistic_manifestations: Dict[str, List[str]]  # lang -> expressions
    required_dhatu_properties: List[str]
    semantic_features: Dict[str, Any]
    blocking_ambiguities: List[str]


class DetailedFailurePatternAnalyzer:
    """Analyseur détaillé des patterns d'échec de reconstitution"""
    
    def __init__(self):
        self.corpus_file = Path(__file__).parent / "corpus_children_literature" / "corpus_pilot.json"
        self.semantic_mismatches = []
        self.conceptual_gaps = []
        
        # Patterns linguistiques détaillés pour analyse fine
        self.linguistic_patterns = {
            'aspectual_markers': {
                'fr': {
                    'perfectif': ['passa', 'courut', 'dit', 'fit', 'alla'],
                    'imperfectif': ['passait', 'courait', 'disait', 'faisait', 'allait'],
                    'progressif': ['était en train de', 'était en cours de']
                },
                'en': {
                    'simple_past': ['ran', 'said', 'went', 'did', 'was'],
                    'progressive': ['was running', 'was saying', 'was going'],
                    'perfect': ['has run', 'had said', 'had gone']
                },
                'de': {
                    'perfekt': ['ist gelaufen', 'hat gesagt', 'ist gegangen'],
                    'präteritum': ['lief', 'sagte', 'ging'],
                    'progressiv': ['war dabei zu', 'war gerade dabei']
                }
            },
            
            'modal_expressions': {
                'fr': {
                    'possibilité': ['peut', 'pourrait', 'il se peut que'],
                    'obligation': ['doit', 'il faut que', 'est obligé de'],
                    'volition': ['veut', 'désire', 'souhaite'],
                    'capacité': ['sait', 'peut', 'est capable de']
                },
                'en': {
                    'possibility': ['may', 'might', 'could', 'perhaps'],
                    'obligation': ['must', 'have to', 'need to'],
                    'volition': ['wants', 'wishes', 'desires'],
                    'ability': ['can', 'is able to', 'knows how to']
                },
                'de': {
                    'möglichkeit': ['kann', 'könnte', 'vielleicht'],
                    'verpflichtung': ['muss', 'soll', 'hat zu'],
                    'wille': ['will', 'möchte', 'wünscht'],
                    'fähigkeit': ['kann', 'vermag', 'ist imstande']
                }
            },
            
            'evidential_markers': {
                'fr': {
                    'direct': ['voit', 'entend', 'constate'],
                    'reporté': ['dit-on', 'parait-il', 'selon'],
                    'inféré': ['semble', 'apparemment', 'probablement']
                },
                'en': {
                    'direct': ['sees', 'hears', 'observes'],
                    'reported': ['allegedly', 'reportedly', 'according to'],
                    'inferred': ['seems', 'apparently', 'probably']
                },
                'de': {
                    'direkt': ['sieht', 'hört', 'beobachtet'],
                    'berichtet': ['angeblich', 'berichten zufolge'],
                    'gefolgert': ['scheint', 'anscheinend', 'wahrscheinlich']
                }
            }
        }
    
    def analyze_text_pair_detailed(self, text_id: str, source_lang: str, target_lang: str) -> List[SemanticMismatch]:
        """Analyse détaillée d'une paire de textes pour identifier décalages précis"""
        
        # Charger corpus
        with open(self.corpus_file, 'r', encoding='utf-8') as f:
            corpus_data = json.load(f)
        
        # Trouver le texte
        target_text = None
        for text in corpus_data['texts']:
            if text['id'] == text_id:
                target_text = text
                break
        
        if not target_text:
            return []
        
        source_text = target_text['versions'][source_lang]
        authentic_target = target_text['versions'][target_lang]
        
        # Segmenter textes en unités sémantiques
        source_segments = self._segment_text_semantically(source_text, source_lang)
        target_segments = self._segment_text_semantically(authentic_target, target_lang)
        
        # Analyser chaque segment pour décalages
        mismatches = []
        
        for i, (source_seg, target_seg) in enumerate(zip(source_segments, target_segments)):
            
            # Simuler reconstitution pour ce segment
            reconstructed_seg = self._reconstruct_segment(source_seg, source_lang, target_lang)
            
            # Analyser type de décalage
            mismatch_type = self._classify_mismatch_type(source_seg, target_seg, reconstructed_seg, source_lang, target_lang)
            
            # Calculer distance sémantique
            semantic_distance = self._calculate_semantic_distance(target_seg, reconstructed_seg, target_lang)
            
            # Identifier concepts manquants
            missing_concepts = self._identify_missing_concepts_in_segment(source_seg, target_seg, source_lang, target_lang)
            
            # Générer variants d'interprétation
            interpretation_variants = self._generate_interpretation_variants(source_seg, source_lang, target_lang)
            
            if semantic_distance > 0.3:  # Seuil de décalage significatif
                mismatch = SemanticMismatch(
                    mismatch_id=f"{text_id}_{source_lang}_{target_lang}_seg_{i}",
                    source_segment=source_seg,
                    source_lang=source_lang,
                    target_segment=target_seg,
                    target_lang=target_lang,
                    reconstructed_segment=reconstructed_seg,
                    mismatch_type=mismatch_type,
                    semantic_distance=semantic_distance,
                    missing_concepts=missing_concepts,
                    interpretation_variants=interpretation_variants,
                    confidence_level=1.0 - semantic_distance
                )
                mismatches.append(mismatch)
        
        return mismatches
    
    def discover_conceptual_gaps(self, all_mismatches: List[SemanticMismatch]) -> List[ConceptualGap]:
        """Découvre gaps conceptuels systémiques à partir des décalages"""
        
        # Grouper décalages par concept manquant
        concept_frequency = Counter()
        concept_manifestations = defaultdict(lambda: defaultdict(list))
        
        for mismatch in all_mismatches:
            for concept in mismatch.missing_concepts:
                concept_frequency[concept] += 1
                concept_manifestations[concept][mismatch.source_lang].append(mismatch.source_segment)
                concept_manifestations[concept][mismatch.target_lang].append(mismatch.target_segment)
        
        # Créer gaps conceptuels pour concepts fréquents
        conceptual_gaps = []
        
        for concept, frequency in concept_frequency.most_common():
            if frequency >= 2:  # Seuil minimum de récurrence
                
                # Analyser propriétés dhātu requises
                required_properties = self._analyze_required_dhatu_properties(concept, all_mismatches)
                
                # Analyser features sémantiques
                semantic_features = self._extract_semantic_features(concept, concept_manifestations[concept])
                
                # Identifier ambiguïtés bloquantes
                blocking_ambiguities = self._identify_blocking_ambiguities(concept, all_mismatches)
                
                gap = ConceptualGap(
                    gap_id=f"gap_{concept}_{frequency}",
                    concept_name=concept,
                    frequency_across_corpus=frequency,
                    cross_linguistic_manifestations=dict(concept_manifestations[concept]),
                    required_dhatu_properties=required_properties,
                    semantic_features=semantic_features,
                    blocking_ambiguities=blocking_ambiguities
                )
                conceptual_gaps.append(gap)
        
        return conceptual_gaps
    
    def run_comprehensive_failure_analysis(self) -> Dict[str, Any]:
        """Lance analyse complète des patterns d'échec sur corpus entier"""
        
        print("🔬 ANALYSE DÉTAILLÉE PATTERNS D'ÉCHEC")
        print("=" * 50)
        
        # Charger corpus
        with open(self.corpus_file, 'r', encoding='utf-8') as f:
            corpus_data = json.load(f)
        
        all_mismatches = []
        language_pairs = [('fr', 'en'), ('en', 'fr'), ('fr', 'de'), ('de', 'fr'), ('en', 'de'), ('de', 'en')]
        
        # Analyser chaque texte et paire de langues
        for text in corpus_data['texts']:
            text_id = text['id']
            print(f"\n📖 Analyse: {text['title']}")
            
            for source_lang, target_lang in language_pairs:
                if source_lang in text['versions'] and target_lang in text['versions']:
                    print(f"   🔍 {source_lang} → {target_lang}")
                    
                    mismatches = self.analyze_text_pair_detailed(text_id, source_lang, target_lang)
                    all_mismatches.extend(mismatches)
                    
                    print(f"      📊 Décalages détectés: {len(mismatches)}")
                    
                    # Afficher décalages majeurs
                    major_mismatches = [m for m in mismatches if m.semantic_distance > 0.7]
                    for mismatch in major_mismatches[:2]:  # Top 2 par paire
                        print(f"      ⚠️ {mismatch.mismatch_type}: {mismatch.semantic_distance:.3f}")
                        print(f"         Source: {mismatch.source_segment[:50]}...")
                        print(f"         Cible: {mismatch.target_segment[:50]}...")
                        print(f"         Reconstitué: {mismatch.reconstructed_segment[:50]}...")
        
        # Découvrir gaps conceptuels
        print(f"\n🔍 Découverte gaps conceptuels...")
        conceptual_gaps = self.discover_conceptual_gaps(all_mismatches)
        
        # Analyser patterns globaux
        analysis_results = {
            'total_mismatches': len(all_mismatches),
            'conceptual_gaps': len(conceptual_gaps),
            'mismatch_types_distribution': self._analyze_mismatch_types(all_mismatches),
            'semantic_distance_distribution': self._analyze_semantic_distances(all_mismatches),
            'most_problematic_concepts': [gap.concept_name for gap in conceptual_gaps[:5]],
            'language_pair_difficulty': self._analyze_language_pair_difficulty(all_mismatches),
            'blocking_factors': self._identify_major_blocking_factors(conceptual_gaps),
            'improvement_recommendations': self._generate_improvement_recommendations(conceptual_gaps)
        }
        
        # Afficher résultats
        print(f"\n📊 RÉSULTATS ANALYSE:")
        print(f"   • Décalages totaux: {analysis_results['total_mismatches']}")
        print(f"   • Gaps conceptuels: {analysis_results['conceptual_gaps']}")
        print(f"   • Concepts problématiques: {analysis_results['most_problematic_concepts']}")
        
        print(f"\n🎯 FACTEURS BLOQUANTS MAJEURS:")
        for factor in analysis_results['blocking_factors']:
            print(f"   • {factor}")
        
        print(f"\n💡 RECOMMANDATIONS AMÉLIORATION:")
        for rec in analysis_results['improvement_recommendations']:
            print(f"   • {rec}")
        
        return analysis_results
    
    # Méthodes utilitaires détaillées
    
    def _segment_text_semantically(self, text: str, lang: str) -> List[str]:
        """Segmente texte en unités sémantiques cohérentes"""
        
        # Segmentation simple par phrases et groupes sémantiques
        sentences = re.split(r'[.!?]+', text)
        semantic_segments = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:  # Ignorer segments trop courts
                # Diviser en groupes sémantiques (sujet-verbe-objet, etc.)
                if lang == 'fr':
                    # Patterns français
                    groups = re.split(r'[,;]', sentence)
                elif lang == 'en':
                    # Patterns anglais
                    groups = re.split(r'[,;]', sentence)
                elif lang == 'de':
                    # Patterns allemands
                    groups = re.split(r'[,;]', sentence)
                else:
                    groups = [sentence]
                
                for group in groups:
                    group = group.strip()
                    if len(group) > 5:
                        semantic_segments.append(group)
        
        return semantic_segments
    
    def _reconstruct_segment(self, source_segment: str, source_lang: str, target_lang: str) -> str:
        """Reconstitue un segment via dhātu (simulation simplifiée)"""
        
        # Simulation basique de reconstitution
        # Dans l'implémentation réelle, utiliserait l'analyseur dhātu complet
        
        words = source_segment.split()
        reconstructed_words = []
        
        for word in words:
            # Simulation de mapping cross-linguistique basique
            if target_lang == 'en':
                if word.lower() in ['lièvre', 'lapin']:
                    reconstructed_words.append('hare')
                elif word.lower() in ['tortue']:
                    reconstructed_words.append('tortoise')
                elif word.lower() in ['dit', 'parla']:
                    reconstructed_words.append('said')
                elif word.lower() in ['courut', 'courir']:
                    reconstructed_words.append('ran')
                else:
                    reconstructed_words.append(f'[{word}]')  # Mot non traduit
            
            elif target_lang == 'de':
                if word.lower() in ['lièvre', 'lapin']:
                    reconstructed_words.append('Hase')
                elif word.lower() in ['tortue']:
                    reconstructed_words.append('Schildkröte')
                elif word.lower() in ['dit', 'parla']:
                    reconstructed_words.append('sagte')
                elif word.lower() in ['courut', 'courir']:
                    reconstructed_words.append('lief')
                else:
                    reconstructed_words.append(f'[{word}]')
        
        return ' '.join(reconstructed_words)
    
    def _classify_mismatch_type(self, source_seg: str, target_seg: str, reconstructed_seg: str, source_lang: str, target_lang: str) -> str:
        """Classifie le type de décalage sémantique"""
        
        # Analyser patterns linguistiques pour classifier
        source_lower = source_seg.lower()
        target_lower = target_seg.lower()
        
        # Décalage aspectuel ?
        aspectual_markers_source = self.linguistic_patterns['aspectual_markers'].get(source_lang, {})
        aspectual_markers_target = self.linguistic_patterns['aspectual_markers'].get(target_lang, {})
        
        source_aspects = []
        target_aspects = []
        
        for aspect, markers in aspectual_markers_source.items():
            if any(marker in source_lower for marker in markers):
                source_aspects.append(aspect)
        
        for aspect, markers in aspectual_markers_target.items():
            if any(marker in target_lower for marker in markers):
                target_aspects.append(aspect)
        
        if source_aspects != target_aspects:
            return 'aspectual_mismatch'
        
        # Décalage modal ?
        modal_markers_source = self.linguistic_patterns['modal_expressions'].get(source_lang, {})
        modal_markers_target = self.linguistic_patterns['modal_expressions'].get(target_lang, {})
        
        source_modals = []
        target_modals = []
        
        for modal, markers in modal_markers_source.items():
            if any(marker in source_lower for marker in markers):
                source_modals.append(modal)
        
        for modal, markers in modal_markers_target.items():
            if any(marker in target_lower for marker in markers):
                target_modals.append(modal)
        
        if source_modals != target_modals:
            return 'modal_mismatch'
        
        # Décalage lexical ?
        if '[' in reconstructed_seg:  # Mots non traduits
            return 'lexical_gap'
        
        # Décalage structurel ?
        if len(source_seg.split()) != len(target_seg.split()):
            return 'structural_mismatch'
        
        return 'semantic_drift'
    
    def _calculate_semantic_distance(self, target_seg: str, reconstructed_seg: str, lang: str) -> float:
        """Calcule distance sémantique entre segment cible et reconstitué"""
        
        # Méthode simplifiée : ratio de mots différents
        target_words = set(target_seg.lower().split())
        reconstructed_words = set(reconstructed_seg.lower().split())
        
        # Enlever mots de fonction communs
        function_words = {
            'fr': {'le', 'la', 'les', 'de', 'du', 'des', 'un', 'une', 'et', 'à'},
            'en': {'the', 'a', 'an', 'of', 'to', 'and', 'in', 'on', 'at'},
            'de': {'der', 'die', 'das', 'ein', 'eine', 'und', 'zu', 'in', 'auf'}
        }
        
        if lang in function_words:
            target_words -= function_words[lang]
            reconstructed_words -= function_words[lang]
        
        if not target_words and not reconstructed_words:
            return 0.0
        
        intersection = len(target_words & reconstructed_words)
        union = len(target_words | reconstructed_words)
        
        return 1.0 - (intersection / union if union > 0 else 0)
    
    def _identify_missing_concepts_in_segment(self, source_seg: str, target_seg: str, source_lang: str, target_lang: str) -> List[str]:
        """Identifie concepts manquants dans un segment"""
        
        missing = []
        
        # Analyser aspects manquants
        if 'était' in source_seg.lower() and 'was' not in target_seg.lower():
            missing.append('past_continuous_aspect')
        
        # Analyser modalités manquantes
        if any(modal in source_seg.lower() for modal in ['peut', 'doit', 'veut']) and \
           not any(modal in target_seg.lower() for modal in ['can', 'must', 'want']):
            missing.append('modal_information')
        
        # Analyser évidence manquante
        if any(ev in source_seg.lower() for ev in ['dit-on', 'semble', 'parait']) and \
           not any(ev in target_seg.lower() for ev in ['apparently', 'seems', 'reportedly']):
            missing.append('evidential_information')
        
        return missing
    
    def _generate_interpretation_variants(self, source_seg: str, source_lang: str, target_lang: str) -> List[Dict[str, Any]]:
        """Génère variants d'interprétation possibles"""
        
        variants = []
        
        # Variant aspectuel
        if source_lang == 'fr' and target_lang == 'en':
            if 'était' in source_seg.lower():
                variants.append({
                    'type': 'aspectual',
                    'interpretation': 'past_continuous',
                    'reconstruction': source_seg.replace('était', 'was being'),
                    'confidence': 0.8
                })
        
        # Variant modal
        if 'peut' in source_seg.lower():
            variants.append({
                'type': 'modal',
                'interpretation': 'possibility',
                'reconstruction': source_seg.replace('peut', 'may/can'),
                'confidence': 0.7
            })
        
        return variants
    
    def _analyze_required_dhatu_properties(self, concept: str, mismatches: List[SemanticMismatch]) -> List[str]:
        """Analyse propriétés dhātu requises pour un concept"""
        
        properties = []
        
        if 'aspect' in concept:
            properties.extend(['temporal_anchoring', 'completion_status', 'duration_encoding'])
        
        if 'modal' in concept:
            properties.extend(['probability_encoding', 'obligation_level', 'volition_marker'])
        
        if 'evidential' in concept:
            properties.extend(['information_source', 'certainty_level', 'directness_marker'])
        
        return properties
    
    def _extract_semantic_features(self, concept: str, manifestations: Dict[str, List[str]]) -> Dict[str, Any]:
        """Extrait features sémantiques d'un concept"""
        
        features = {
            'cross_linguistic_frequency': len(manifestations),
            'linguistic_complexity': 'high' if len(manifestations) > 2 else 'medium',
            'ambiguity_level': 'high',  # Par défaut pour concepts problématiques
        }
        
        return features
    
    def _identify_blocking_ambiguities(self, concept: str, mismatches: List[SemanticMismatch]) -> List[str]:
        """Identifie ambiguïtés qui bloquent résolution du concept"""
        
        blocking = []
        
        concept_mismatches = [m for m in mismatches if concept in m.missing_concepts]
        
        for mismatch in concept_mismatches:
            if mismatch.semantic_distance > 0.8:
                blocking.append(f"High_semantic_distance_in_{mismatch.mismatch_type}")
        
        return list(set(blocking))
    
    def _analyze_mismatch_types(self, mismatches: List[SemanticMismatch]) -> Dict[str, int]:
        """Analyse distribution des types de décalages"""
        
        type_counts = Counter(m.mismatch_type for m in mismatches)
        return dict(type_counts)
    
    def _analyze_semantic_distances(self, mismatches: List[SemanticMismatch]) -> Dict[str, float]:
        """Analyse distribution des distances sémantiques"""
        
        distances = [m.semantic_distance for m in mismatches]
        
        return {
            'mean_distance': sum(distances) / len(distances) if distances else 0,
            'max_distance': max(distances) if distances else 0,
            'min_distance': min(distances) if distances else 0
        }
    
    def _analyze_language_pair_difficulty(self, mismatches: List[SemanticMismatch]) -> Dict[str, float]:
        """Analyse difficulté par paire de langues"""
        
        pair_distances = defaultdict(list)
        
        for mismatch in mismatches:
            pair_key = f"{mismatch.source_lang}-{mismatch.target_lang}"
            pair_distances[pair_key].append(mismatch.semantic_distance)
        
        pair_difficulty = {}
        for pair, distances in pair_distances.items():
            pair_difficulty[pair] = sum(distances) / len(distances) if distances else 0
        
        return pair_difficulty
    
    def _identify_major_blocking_factors(self, gaps: List[ConceptualGap]) -> List[str]:
        """Identifie facteurs bloquants majeurs"""
        
        factors = []
        
        # Analyser fréquence des gaps
        high_freq_gaps = [gap for gap in gaps if gap.frequency_across_corpus >= 3]
        if high_freq_gaps:
            factors.append(f"Gaps conceptuels haute fréquence: {[g.concept_name for g in high_freq_gaps]}")
        
        # Analyser complexité cross-linguistique
        complex_gaps = [gap for gap in gaps if len(gap.cross_linguistic_manifestations) >= 3]
        if complex_gaps:
            factors.append(f"Concepts cross-linguistiquement complexes: {[g.concept_name for g in complex_gaps]}")
        
        return factors
    
    def _generate_improvement_recommendations(self, gaps: List[ConceptualGap]) -> List[str]:
        """Génère recommandations d'amélioration"""
        
        recommendations = []
        
        # Recommandations basées sur gaps
        aspect_gaps = [gap for gap in gaps if 'aspect' in gap.concept_name]
        if aspect_gaps:
            recommendations.append("Ajouter dhātu aspectuels: PERF, PROG, ITER_PERF")
        
        modal_gaps = [gap for gap in gaps if 'modal' in gap.concept_name]
        if modal_gaps:
            recommendations.append("Ajouter dhātu modaux: POSS, OBLIG, VOLI")
        
        evidential_gaps = [gap for gap in gaps if 'evidential' in gap.concept_name]
        if evidential_gaps:
            recommendations.append("Ajouter dhātu évidentiels: DIRECT, REPORT, INFER")
        
        return recommendations


def main():
    """Point d'entrée principal"""
    
    analyzer = DetailedFailurePatternAnalyzer()
    
    try:
        # Lancer analyse complète
        results = analyzer.run_comprehensive_failure_analysis()
        
        # Sauvegarder résultats détaillés
        results_file = Path(__file__).parent / "detailed_failure_analysis.json"
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Analyse sauvegardée: {results_file}")
        
    except Exception as e:
        print(f"❌ Erreur analyse: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()