#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyseur d'Écarts de Reconstitution Dhātu
Test empirique de fidélité sémantique par décomposition/reconstitution

Méthodologie:
1. Extraction dhātu depuis texte source 
2. Reconstitution sémantique vers langue cible
3. Mesure écarts avec version authentique
4. Identification patterns d'échec et optimisation modèle
"""

import json
import re
import math
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
import sys

# Import des modules existants
sys.path.append(str(Path(__file__).parent / "scripts"))
from optimal_dhatu_analyzer import OptimalDhatuAnalyzer


@dataclass
class DhatuExtraction:
    """Représente l'extraction dhātu d'un texte"""
    source_text: str
    source_lang: str
    extracted_dhatu: List[Dict[str, Any]]
    coverage_score: float
    semantic_gaps: List[str]
    
@dataclass
class ReconstitutionResult:
    """Résultat d'une reconstitution cross-linguistique"""
    source_extraction: DhatuExtraction
    target_lang: str
    reconstructed_text: str
    authentic_target: str
    fidelity_scores: Dict[str, float]
    semantic_deviations: List[str]
    success_metrics: Dict[str, Any]


class ReconstitutionAnalyzer:
    """Analyseur principal des écarts de reconstitution"""
    
    def __init__(self):
        self.dhatu_analyzer = OptimalDhatuAnalyzer()
        self.corpus_file = Path(__file__).parent / "corpus_children_literature" / "corpus_pilot.json"
        
        # Règles de reconstitution sémantique
        self.reconstitution_rules = {
            'EXIST': {
                'fr': ['il était', 'il y avait', 'vivait', 'se trouvait'],
                'en': ['there was', 'there lived', 'existed', 'was'],
                'de': ['es war', 'es gab', 'lebte', 'existierte']
            },
            'COMM': {
                'fr': ['dit', 'parla', 'demanda', 'répondit', 'déclara'],
                'en': ['said', 'spoke', 'asked', 'replied', 'declared'],
                'de': ['sagte', 'sprach', 'fragte', 'antwortete', 'erklärte']
            },
            'TRANS': {
                'fr': ['alla', 'vint', 'courut', 'marcha', 'se dirigea'],
                'en': ['went', 'came', 'ran', 'walked', 'moved'],
                'de': ['ging', 'kam', 'lief', 'wanderte', 'bewegte sich']
            },
            'DECIDE': {
                'fr': ['décida', 'choisit', 'résolut', 'opta'],
                'en': ['decided', 'chose', 'resolved', 'opted'],
                'de': ['entschied', 'wählte', 'beschloss', 'entschloss sich']
            },
            'EVAL': {
                'fr': ['beau', 'bon', 'mauvais', 'excellent', 'terrible'],
                'en': ['beautiful', 'good', 'bad', 'excellent', 'terrible'],
                'de': ['schön', 'gut', 'schlecht', 'ausgezeichnet', 'schrecklich']
            },
            'GROUP': {
                'fr': ['ensemble', 'groupe', 'famille', 'équipe'],
                'en': ['together', 'group', 'family', 'team'],
                'de': ['zusammen', 'Gruppe', 'Familie', 'Team']
            },
            'ITER': {
                'fr': ['encore', 'de nouveau', 'répéta', 'continua'],
                'en': ['again', 'once more', 'repeated', 'continued'],
                'de': ['wieder', 'nochmals', 'wiederholte', 'fortsetzte']
            },
            'LOCATE': {
                'fr': ['dans', 'sur', 'près de', 'à côté de'],
                'en': ['in', 'on', 'near', 'beside'],
                'de': ['in', 'auf', 'nahe', 'neben']
            },
            'SEQ': {
                'fr': ['puis', 'ensuite', 'après', 'alors'],
                'en': ['then', 'next', 'after', 'so'],
                'de': ['dann', 'danach', 'nach', 'so']
            }
        }
        
        # Métriques de fidélité
        self.fidelity_thresholds = {
            'word_overlap_ratio': 0.40,     # 40% mots communs minimum
            'semantic_preservation': 0.65,   # 65% préservation sémantique
            'narrative_flow': 0.70,         # 70% cohérence narrative
            'cultural_fidelity': 0.60       # 60% fidélité culturelle
        }
    
    def load_corpus(self) -> List[Dict[str, Any]]:
        """Charge le corpus littérature jeunesse"""
        
        if not self.corpus_file.exists():
            raise FileNotFoundError(f"Corpus non trouvé: {self.corpus_file}")
        
        with open(self.corpus_file, 'r', encoding='utf-8') as f:
            corpus_data = json.load(f)
        
        return corpus_data['texts']
    
    def extract_dhatu_from_text(self, text: str, lang: str) -> DhatuExtraction:
        """Extrait les dhātu d'un texte source"""
        
        analysis = self.dhatu_analyzer.analyze_text(text)
        
        # Structurer l'extraction dhātu
        extracted_dhatu = []
        for dhatu_name, count in analysis['dhatu_distribution'].items():
            if count > 0:
                dhatu_info = {
                    'dhatu': dhatu_name,
                    'frequency': count,
                    'semantic_weight': count / len(text.split()),
                    'context_examples': self._find_dhatu_contexts(text, dhatu_name)
                }
                extracted_dhatu.append(dhatu_info)
        
        # Identifier gaps sémantiques
        semantic_gaps = [gap.text for gap in analysis['semantic_gaps'][:5]]
        
        return DhatuExtraction(
            source_text=text,
            source_lang=lang,
            extracted_dhatu=extracted_dhatu,
            coverage_score=analysis['coverage_stats']['semantic_coverage'],
            semantic_gaps=semantic_gaps
        )
    
    def reconstruct_from_dhatu(self, extraction: DhatuExtraction, target_lang: str) -> str:
        """Reconstitue un texte dans la langue cible à partir des dhātu"""
        
        # Stratégie de reconstitution basée sur dhātu
        reconstructed_segments = []
        
        # Analyser la structure narrative du texte original
        source_sentences = extraction.source_text.split('.')
        source_words = extraction.source_text.split()
        
        # Pour chaque dhātu extrait, générer un segment reconstitué
        for dhatu_info in extraction.extracted_dhatu:
            dhatu = dhatu_info['dhatu']
            frequency = dhatu_info['frequency']
            
            # Sélectionner expressions cibles
            if dhatu in self.reconstitution_rules and target_lang in self.reconstitution_rules[dhatu]:
                target_expressions = self.reconstitution_rules[dhatu][target_lang]
                
                # Choisir expression basée sur contexte et fréquence
                selected_expr = self._select_best_expression(
                    target_expressions, dhatu_info['context_examples'], frequency
                )
                
                reconstructed_segments.append(selected_expr)
        
        # Reconstituer structure narrative
        if target_lang == 'en':
            narrative_structure = self._build_english_narrative(reconstructed_segments, extraction)
        elif target_lang == 'de':
            narrative_structure = self._build_german_narrative(reconstructed_segments, extraction)
        elif target_lang == 'fr':
            narrative_structure = self._build_french_narrative(reconstructed_segments, extraction)
        else:
            narrative_structure = " ".join(reconstructed_segments)
        
        return narrative_structure
    
    def measure_fidelity(self, reconstructed: str, authentic: str, target_lang: str) -> Dict[str, float]:
        """Mesure la fidélité entre texte reconstitué et version authentique"""
        
        fidelity_scores = {}
        
        # 1. Word Overlap Ratio (Jaccard similarity)
        recon_words = set(reconstructed.lower().split())
        auth_words = set(authentic.lower().split())
        
        intersection = len(recon_words & auth_words)
        union = len(recon_words | auth_words)
        fidelity_scores['word_overlap_ratio'] = intersection / union if union > 0 else 0
        
        # 2. Semantic Preservation (approximation via mots-clés sémantiques)
        semantic_preservation = self._calculate_semantic_preservation(reconstructed, authentic, target_lang)
        fidelity_scores['semantic_preservation'] = semantic_preservation
        
        # 3. Narrative Flow (séquence d'événements)
        narrative_flow = self._calculate_narrative_flow(reconstructed, authentic)
        fidelity_scores['narrative_flow'] = narrative_flow
        
        # 4. Cultural Fidelity (préservation éléments culturels)
        cultural_fidelity = self._calculate_cultural_fidelity(reconstructed, authentic, target_lang)
        fidelity_scores['cultural_fidelity'] = cultural_fidelity
        
        # Score global pondéré
        weights = {'word_overlap_ratio': 0.25, 'semantic_preservation': 0.35, 
                  'narrative_flow': 0.25, 'cultural_fidelity': 0.15}
        
        fidelity_scores['global_fidelity'] = sum(
            fidelity_scores[metric] * weight for metric, weight in weights.items()
        )
        
        return fidelity_scores
    
    def run_reconstitution_test(self, text_id: str, source_lang: str, target_lang: str) -> ReconstitutionResult:
        """Exécute un test complet de reconstitution pour un texte"""
        
        corpus = self.load_corpus()
        
        # Trouver le texte dans le corpus
        target_text = None
        for text in corpus:
            if text['id'] == text_id:
                target_text = text
                break
        
        if not target_text:
            raise ValueError(f"Texte '{text_id}' non trouvé dans le corpus")
        
        if source_lang not in target_text['versions'] or target_lang not in target_text['versions']:
            raise ValueError(f"Langues {source_lang}/{target_lang} non disponibles pour {text_id}")
        
        # Étape 1: Extraction dhātu depuis source
        source_text = target_text['versions'][source_lang]
        extraction = self.extract_dhatu_from_text(source_text, source_lang)
        
        # Étape 2: Reconstitution vers langue cible
        reconstructed = self.reconstruct_from_dhatu(extraction, target_lang)
        
        # Étape 3: Mesure fidélité avec version authentique
        authentic_target = target_text['versions'][target_lang]
        fidelity_scores = self.measure_fidelity(reconstructed, authentic_target, target_lang)
        
        # Étape 4: Identifier déviations sémantiques
        semantic_deviations = self._identify_semantic_deviations(
            reconstructed, authentic_target, extraction
        )
        
        # Métriques de succès
        success_metrics = {
            'passes_fidelity_threshold': fidelity_scores['global_fidelity'] >= 0.65,
            'preserves_key_concepts': len(semantic_deviations) <= 3,
            'maintains_narrative_structure': fidelity_scores['narrative_flow'] >= 0.70,
            'dhatu_coverage_adequate': extraction.coverage_score >= 0.60
        }
        
        return ReconstitutionResult(
            source_extraction=extraction,
            target_lang=target_lang,
            reconstructed_text=reconstructed,
            authentic_target=authentic_target,
            fidelity_scores=fidelity_scores,
            semantic_deviations=semantic_deviations,
            success_metrics=success_metrics
        )
    
    def run_comprehensive_validation(self) -> Dict[str, Any]:
        """Lance validation complète sur tout le corpus"""
        
        print("🧪 VALIDATION COMPLÈTE RECONSTITUTION DHĀTU")
        print("=" * 50)
        
        corpus = self.load_corpus()
        validation_results = {
            'test_results': [],
            'global_metrics': {},
            'language_pair_performance': {},
            'failure_patterns': [],
            'recommendations': []
        }
        
        # Test toutes les paires de langues pour tous les textes
        language_pairs = [('fr', 'en'), ('en', 'fr'), ('fr', 'de'), ('de', 'fr'), ('en', 'de'), ('de', 'en')]
        
        all_fidelity_scores = []
        pair_scores = {f"{src}-{tgt}": [] for src, tgt in language_pairs}
        
        for text in corpus:
            text_id = text['id']
            print(f"\n📖 Test: {text['title']}")
            
            for source_lang, target_lang in language_pairs:
                if source_lang in text['versions'] and target_lang in text['versions']:
                    try:
                        result = self.run_reconstitution_test(text_id, source_lang, target_lang)
                        validation_results['test_results'].append({
                            'text_id': text_id,
                            'source_lang': source_lang,
                            'target_lang': target_lang,
                            'fidelity_score': result.fidelity_scores['global_fidelity'],
                            'success_metrics': result.success_metrics,
                            'dhatu_count': len(result.source_extraction.extracted_dhatu)
                        })
                        
                        all_fidelity_scores.append(result.fidelity_scores['global_fidelity'])
                        pair_scores[f"{source_lang}-{target_lang}"].append(result.fidelity_scores['global_fidelity'])
                        
                        print(f"   {source_lang}→{target_lang}: {result.fidelity_scores['global_fidelity']:.3f}")
                        
                    except Exception as e:
                        print(f"   ❌ {source_lang}→{target_lang}: Erreur - {e}")
        
        # Calculer métriques globales
        validation_results['global_metrics'] = {
            'mean_fidelity': sum(all_fidelity_scores) / len(all_fidelity_scores) if all_fidelity_scores else 0,
            'total_tests': len(all_fidelity_scores),
            'success_rate': sum(1 for score in all_fidelity_scores if score >= 0.65) / len(all_fidelity_scores) if all_fidelity_scores else 0,
            'min_fidelity': min(all_fidelity_scores) if all_fidelity_scores else 0,
            'max_fidelity': max(all_fidelity_scores) if all_fidelity_scores else 0
        }
        
        # Performance par paire de langues
        for pair, scores in pair_scores.items():
            if scores:
                validation_results['language_pair_performance'][pair] = {
                    'mean_fidelity': sum(scores) / len(scores),
                    'test_count': len(scores),
                    'success_rate': sum(1 for score in scores if score >= 0.65) / len(scores)
                }
        
        return validation_results
    
    # Méthodes utilitaires privées
    
    def _find_dhatu_contexts(self, text: str, dhatu_name: str) -> List[str]:
        """Trouve les contextes où un dhātu apparaît dans le texte"""
        # Implémentation simplifiée
        return [f"contexte_{dhatu_name}"]
    
    def _select_best_expression(self, expressions: List[str], contexts: List[str], frequency: int) -> str:
        """Sélectionne la meilleure expression cible basée sur le contexte"""
        # Stratégie simple: prendre la première expression
        return expressions[0] if expressions else "unknown"
    
    def _build_english_narrative(self, segments: List[str], extraction: DhatuExtraction) -> str:
        """Construit narrative anglaise à partir des segments"""
        if not segments:
            return "A story unfolds..."
        
        # Structure narrative anglaise basique
        narrative = "Once upon a time, " + segments[0]
        for segment in segments[1:]:
            narrative += f". {segment.capitalize()}"
        narrative += "."
        
        return narrative
    
    def _build_german_narrative(self, segments: List[str], extraction: DhatuExtraction) -> str:
        """Construit narrative allemande à partir des segments"""
        if not segments:
            return "Es war einmal..."
        
        narrative = "Es war einmal, " + segments[0]
        for segment in segments[1:]:
            narrative += f". {segment.capitalize()}"
        narrative += "."
        
        return narrative
    
    def _build_french_narrative(self, segments: List[str], extraction: DhatuExtraction) -> str:
        """Construit narrative française à partir des segments"""
        if not segments:
            return "Il était une fois..."
        
        narrative = "Il était une fois, " + segments[0]
        for segment in segments[1:]:
            narrative += f". {segment.capitalize()}"
        narrative += "."
        
        return narrative
    
    def _calculate_semantic_preservation(self, reconstructed: str, authentic: str, lang: str) -> float:
        """Calcule préservation sémantique (approximation via mots-clés)"""
        
        # Mots-clés sémantiques importants par langue
        semantic_keywords = {
            'fr': ['dit', 'alla', 'était', 'fit', 'vit', 'prit'],
            'en': ['said', 'went', 'was', 'did', 'saw', 'took'],
            'de': ['sagte', 'ging', 'war', 'tat', 'sah', 'nahm']
        }
        
        if lang not in semantic_keywords:
            return 0.5  # Score neutre par défaut
        
        keywords = semantic_keywords[lang]
        recon_matches = sum(1 for kw in keywords if kw in reconstructed.lower())
        auth_matches = sum(1 for kw in keywords if kw in authentic.lower())
        
        if auth_matches == 0:
            return 1.0 if recon_matches == 0 else 0.0
        
        return min(recon_matches / auth_matches, 1.0)
    
    def _calculate_narrative_flow(self, reconstructed: str, authentic: str) -> float:
        """Calcule cohérence du flow narratif"""
        
        # Indicateurs de séquence narrative
        sequence_indicators = ['puis', 'ensuite', 'alors', 'then', 'next', 'after', 'dann', 'danach']
        
        recon_sequences = sum(1 for ind in sequence_indicators if ind in reconstructed.lower())
        auth_sequences = sum(1 for ind in sequence_indicators if ind in authentic.lower())
        
        if auth_sequences == 0:
            return 1.0 if recon_sequences == 0 else 0.8
        
        return min(recon_sequences / auth_sequences, 1.0)
    
    def _calculate_cultural_fidelity(self, reconstructed: str, authentic: str, lang: str) -> float:
        """Calcule fidélité culturelle (expressions idiomatiques, etc.)"""
        
        # Expressions culturelles typiques par langue
        cultural_expressions = {
            'fr': ['il était une fois', 'bien sûr', 'tout de suite'],
            'en': ['once upon a time', 'of course', 'right away'],
            'de': ['es war einmal', 'natürlich', 'sofort']
        }
        
        if lang not in cultural_expressions:
            return 0.7  # Score neutre
        
        expressions = cultural_expressions[lang]
        recon_cultural = sum(1 for expr in expressions if expr in reconstructed.lower())
        auth_cultural = sum(1 for expr in expressions if expr in authentic.lower())
        
        if auth_cultural == 0:
            return 0.8  # Score par défaut si pas d'expressions culturelles
        
        return min(recon_cultural / auth_cultural, 1.0)
    
    def _identify_semantic_deviations(self, reconstructed: str, authentic: str, extraction: DhatuExtraction) -> List[str]:
        """Identifie les déviations sémantiques majeures"""
        
        deviations = []
        
        # Vérifier si les dhātu principaux sont représentés
        for dhatu_info in extraction.extracted_dhatu[:3]:  # Top 3 dhātu
            dhatu = dhatu_info['dhatu']
            if dhatu not in str(extraction.source_text).upper():  # Approximation simplifiée
                deviations.append(f"Dhātu {dhatu} perdu dans reconstitution")
        
        # Vérifier longueur relative
        recon_words = len(reconstructed.split())
        auth_words = len(authentic.split())
        
        if abs(recon_words - auth_words) > auth_words * 0.5:
            deviations.append(f"Longueur très différente: {recon_words} vs {auth_words} mots")
        
        return deviations


def main():
    """Point d'entrée principal"""
    
    analyzer = ReconstitutionAnalyzer()
    
    try:
        # Test simple d'abord
        print("🧪 TEST PILOTE - Tortoise and Hare")
        print("-" * 40)
        
        result = analyzer.run_reconstitution_test('tortoise_hare', 'fr', 'en')
        
        print(f"📝 Texte source (FR): {result.source_extraction.source_text[:100]}...")
        print(f"🔄 Reconstitué (EN): {result.reconstructed_text}")
        print(f"✅ Authentique (EN): {result.authentic_target[:100]}...")
        print(f"\n📊 Scores de fidélité:")
        for metric, score in result.fidelity_scores.items():
            print(f"   • {metric}: {score:.3f}")
        
        print(f"\n🎯 Métriques de succès:")
        for metric, success in result.success_metrics.items():
            status = "✅" if success else "❌"
            print(f"   {status} {metric}: {success}")
        
        if result.semantic_deviations:
            print(f"\n⚠️ Déviations sémantiques:")
            for deviation in result.semantic_deviations:
                print(f"   • {deviation}")
        
        # Validation complète si test pilote réussi
        if result.fidelity_scores['global_fidelity'] >= 0.50:
            print(f"\n🚀 LANCEMENT VALIDATION COMPLÈTE...")
            validation = analyzer.run_comprehensive_validation()
            
            print(f"\n📈 RÉSULTATS GLOBAUX:")
            print(f"   • Tests effectués: {validation['global_metrics']['total_tests']}")
            print(f"   • Fidélité moyenne: {validation['global_metrics']['mean_fidelity']:.3f}")
            print(f"   • Taux de succès: {validation['global_metrics']['success_rate']:.1%}")
            print(f"   • Fidélité min/max: {validation['global_metrics']['min_fidelity']:.3f} / {validation['global_metrics']['max_fidelity']:.3f}")
            
            print(f"\n🌍 PERFORMANCE PAR PAIRE DE LANGUES:")
            for pair, metrics in validation['language_pair_performance'].items():
                print(f"   • {pair}: {metrics['mean_fidelity']:.3f} (succès: {metrics['success_rate']:.1%})")
        
        else:
            print(f"\n⚠️ Test pilote en dessous du seuil - optimisation nécessaire")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()