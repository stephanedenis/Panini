#!/usr/bin/env python3
"""
ANALYSEUR COMPOSABILITÉ ÉMOTIONNELLE PANKSEPP
=============================================

Analyse approfondie de la composabilité réelle des primitives émotionnelles Panksepp.
Au-delà de la validation neurobiologique, examine les antagonismes, synergies,
contraintes compositionnelles et cohérence sémantique des combinaisons.
"""

import json
import time
import itertools
from typing import Dict, List, Any, Tuple, Set
from dataclasses import dataclass
from enum import Enum

class InteractionType(Enum):
    """Types d'interaction entre dhātu émotionnels"""
    SYNERGISTIC = "synergistic"      # Renforcent mutuellement
    NEUTRAL = "neutral"              # Coexistent sans interaction
    COMPETITIVE = "competitive"       # Se concurrencent
    ANTAGONISTIC = "antagonistic"     # S'opposent mutuellement
    INHIBITORY = "inhibitory"        # L'un inhibe l'autre

class CompositionValidity(Enum):
    """Validité d'une composition émotionnelle"""
    VALID = "valid"                  # Composition cohérente
    QUESTIONABLE = "questionable"    # Composition douteuse
    INVALID = "invalid"              # Composition incohérente

@dataclass
class EmotionalInteraction:
    """Structure d'interaction entre deux dhātu émotionnels"""
    dhatu1: str
    dhatu2: str
    interaction_type: InteractionType
    neurobiological_basis: str
    phenomenological_evidence: str
    strength: float  # 0.0 à 1.0
    examples: List[str]
    constraints: List[str]

@dataclass
class CompositionAnalysis:
    """Analyse d'une composition émotionnelle"""
    composition: List[str]
    validity: CompositionValidity
    coherence_score: float
    conflicts: List[Tuple[str, str]]
    synergies: List[Tuple[str, str]]
    phenomenological_examples: List[str]
    constraints_violated: List[str]
    alternative_compositions: List[List[str]]

class EmotionalComposabilityAnalyzer:
    """Analyseur de composabilité des primitives émotionnelles Panksepp"""
    
    def __init__(self):
        self.panksepp_systems = ['SEEK', 'RAGE', 'FEAR', 'LUST', 'CARE', 'GRIEF', 'PLAY']
        self.interaction_matrix = self._build_interaction_matrix()
        self.composition_constraints = self._define_composition_constraints()
        self.phenomenological_data = self._load_phenomenological_evidence()
        
    def _build_interaction_matrix(self) -> Dict[Tuple[str, str], EmotionalInteraction]:
        """Construit matrice d'interactions entre dhātu émotionnels"""
        
        interactions = {}
        
        # ANTAGONISMES NEUROLOGIQUES DOCUMENTÉS
        interactions[('RAGE', 'CARE')] = EmotionalInteraction(
            dhatu1='RAGE', dhatu2='CARE',
            interaction_type=InteractionType.ANTAGONISTIC,
            neurobiological_basis="Circuits amygdale (RAGE) vs PFC/ocytocine (CARE) - inhibition réciproque",
            phenomenological_evidence="Colère intense bloque empathie temporairement",
            strength=0.8,
            examples=["Violence domestique", "Rage parentale", "Conflit empathique"],
            constraints=["Coexistence difficile à haute intensité", "Alternance temporelle possible"]
        )
        
        interactions[('FEAR', 'SEEK')] = EmotionalInteraction(
            dhatu1='FEAR', dhatu2='SEEK',
            interaction_type=InteractionType.INHIBITORY,
            neurobiological_basis="Amygdale (FEAR) inhibe VTA/dopamine (SEEK) - mécanisme survie",
            phenomenological_evidence="Peur paralyse curiosité et exploration",
            strength=0.9,
            examples=["Phobie sociale", "Anxiété performance", "Évitement apprentissage"],
            constraints=["FEAR dominant = SEEK inhibé", "Seuil critique d'activation"]
        )
        
        interactions[('GRIEF', 'PLAY')] = EmotionalInteraction(
            dhatu1='GRIEF', dhatu2='PLAY',
            interaction_type=InteractionType.COMPETITIVE,
            neurobiological_basis="Système opioïde (GRIEF) vs cannabinoïde (PLAY) - ressources partagées",
            phenomenological_evidence="Chagrin profond incompatible avec jeu spontané",
            strength=0.7,
            examples=["Deuil pathologique", "Dépression majeure", "Anhédonie"],
            constraints=["Intensité inversement corrélée", "Transition lente possible"]
        )
        
        # SYNERGIES NEUROLOGIQUES DOCUMENTÉES
        interactions[('SEEK', 'PLAY')] = EmotionalInteraction(
            dhatu1='SEEK', dhatu2='PLAY',
            interaction_type=InteractionType.SYNERGISTIC,
            neurobiological_basis="Dopamine (SEEK) + cannabinoïdes (PLAY) = circuit récompense amplifié",
            phenomenological_evidence="Curiosité ludique maximise apprentissage",
            strength=0.9,
            examples=["Jeu exploratoire enfant", "Créativité artistique", "Innovation scientifique"],
            constraints=["Renforcement mutuel", "Optimum vers 3-4 ans développement"]
        )
        
        interactions[('CARE', 'GRIEF')] = EmotionalInteraction(
            dhatu1='CARE', dhatu2='GRIEF',
            interaction_type=InteractionType.SYNERGISTIC,
            neurobiological_basis="Ocytocine (CARE) + opioïdes (GRIEF) = attachement profond",
            phenomenological_evidence="Amour rend vulnérable à la perte",
            strength=0.8,
            examples=["Deuil amoureux", "Compassion", "Empathie pour souffrance"],
            constraints=["CARE amplifie GRIEF potentiel", "Coactivation fréquente"]
        )
        
        interactions[('LUST', 'CARE')] = EmotionalInteraction(
            dhatu1='LUST', dhatu2='CARE',
            interaction_type=InteractionType.SYNERGISTIC,
            neurobiological_basis="Hormones sexuelles + ocytocine = attachement romantique",
            phenomenological_evidence="Désir évolue vers amour attachement",
            strength=0.7,
            examples=["Amour romantique", "Formation couple", "Transition hormonale"],
            constraints=["Séquence développementale", "Intensité LUST décline avec CARE"]
        )
        
        # COMPÉTITIONS SUBTILES
        interactions[('RAGE', 'FEAR')] = EmotionalInteraction(
            dhatu1='RAGE', dhatu2='FEAR',
            interaction_type=InteractionType.COMPETITIVE,
            neurobiological_basis="Amygdale - circuits attack vs escape partagent ressources",
            phenomenological_evidence="Fight-or-flight : exclusion mutuelle à haute intensité",
            strength=0.6,
            examples=["Rage masque peur", "Peur inhibe agression", "Basculement rapide"],
            constraints=["Alternance dominance", "Seuils activation différents"]
        )
        
        interactions[('SEEK', 'CARE')] = EmotionalInteraction(
            dhatu1='SEEK', dhatu2='CARE',
            interaction_type=InteractionType.SYNERGISTIC,
            neurobiological_basis="Dopamine exploration + ocytocine = soin curieux",
            phenomenological_evidence="Curiosité pour l'autre renforce liens",
            strength=0.8,
            examples=["Curiosité parentale", "Exploration empathique", "Découverte autre"],
            constraints=["Équilibre attention self/other", "Développement progressif"]
        )
        
        # INHIBITIONS COMPLEXES
        interactions[('GRIEF', 'LUST')] = EmotionalInteraction(
            dhatu1='GRIEF', dhatu2='LUST',
            interaction_type=InteractionType.INHIBITORY,
            neurobiological_basis="Stress cortisol (GRIEF) inhibe hormones sexuelles",
            phenomenological_evidence="Chagrin diminue désir sexuel",
            strength=0.8,
            examples=["Deuil conjugal", "Dépression sexuelle", "Récupération graduelle"],
            constraints=["GRIEF inhibe LUST unilatéralement", "Récupération lente"]
        )
        
        return interactions
    
    def _define_composition_constraints(self) -> Dict[str, List[str]]:
        """Définit contraintes compositionnelles générales"""
        
        return {
            'max_antagonistic_pairs': [
                "Maximum 1 paire antagoniste par composition",
                "Éviter RAGE+CARE à haute intensité simultanée"
            ],
            'cognitive_load_limits': [
                "Maximum 4 dhātu émotionnels simultanés (Miller 7±2)",
                "Préférer 2-3 dhātu pour cohérence phénoménologique"
            ],
            'temporal_constraints': [
                "Certaines transitions nécessitent temps (LUST→CARE)",
                "Basculements rapides possibles (FEAR↔RAGE)"
            ],
            'intensity_dependencies': [
                "Antagonismes plus forts à haute intensité",
                "Synergies optimales à intensité modérée"
            ],
            'developmental_constraints': [
                "LUST émerge tardivement (puberté)",
                "SEEK+PLAY optimaux enfance",
                "CARE mature avec expérience"
            ]
        }
    
    def _load_phenomenological_evidence(self) -> Dict[str, Any]:
        """Charge évidence phénoménologique des émotions complexes"""
        
        return {
            'documented_complex_emotions': {
                'JALOUSIE': {
                    'composition_proposed': ['RAGE', 'FEAR', 'CARE'],
                    'phenomenological_validity': 0.9,
                    'clinical_evidence': "Forte documentation psychiatrique",
                    'cross_cultural': True,
                    'developmental_emergence': "18-24 mois (théorie esprit)",
                    'antagonisms_present': [('RAGE', 'CARE')],
                    'resolution_mechanism': "Alternance temporelle dominance"
                },
                'NOSTALGIE': {
                    'composition_proposed': ['GRIEF', 'SEEK', 'EXIST'],
                    'phenomenological_validity': 0.8,
                    'clinical_evidence': "Documentation psychologie positive",
                    'cross_cultural': True,
                    'developmental_emergence': "Adolescence tardive",
                    'antagonisms_present': [],
                    'resolution_mechanism': "Synergie GRIEF+SEEK possible"
                },
                'SCHADENFREUDE': {
                    'composition_proposed': ['PLAY', 'RAGE'],
                    'phenomenological_validity': 0.7,
                    'clinical_evidence': "Études neurosciences sociales",
                    'cross_cultural': False,  # Concept germanique
                    'developmental_emergence': "Enfance tardive",
                    'antagonisms_present': [],
                    'resolution_mechanism': "PLAY transforme RAGE en plaisir"
                },
                'MELANCHOLIA': {
                    'composition_proposed': ['GRIEF', 'SEEK', 'PLAY'],
                    'phenomenological_validity': 0.6,
                    'clinical_evidence': "Littérature romantique, psychanalyse",
                    'cross_cultural': False,
                    'developmental_emergence': "Adulte",
                    'antagonisms_present': [('GRIEF', 'PLAY')],
                    'resolution_mechanism': "Contradiction créative résolution artistique"
                }
            },
            'impossible_combinations': {
                'PURE_RAGE_CARE': {
                    'reason': "Antagonisme neurobiologique direct",
                    'evidence': "Études IRM : activation réciproque exclusive"
                },
                'HIGH_FEAR_HIGH_SEEK': {
                    'reason': "Inhibition adaptative survie",
                    'evidence': "Circuits amygdale bloquent VTA"
                },
                'INTENSE_GRIEF_INTENSE_PLAY': {
                    'reason': "Compétition ressources neurochimiques",
                    'evidence': "Système opioïde vs cannabinoïde"
                }
            }
        }
    
    def analyze_composition_validity(self, composition: List[str]) -> CompositionAnalysis:
        """Analyse validité d'une composition émotionnelle"""
        
        analysis = CompositionAnalysis(
            composition=composition,
            validity=CompositionValidity.VALID,
            coherence_score=1.0,
            conflicts=[],
            synergies=[],
            phenomenological_examples=[],
            constraints_violated=[],
            alternative_compositions=[]
        )
        
        # 1. Détection des conflits
        emotional_dhatus = [d for d in composition if d in self.panksepp_systems]
        
        for i, dhatu1 in enumerate(emotional_dhatus):
            for dhatu2 in emotional_dhatus[i+1:]:
                pair_key = tuple(sorted([dhatu1, dhatu2]))
                reverse_key = (dhatu2, dhatu1) if (dhatu2, dhatu1) in self.interaction_matrix else pair_key
                
                if pair_key in self.interaction_matrix or reverse_key in self.interaction_matrix:
                    interaction = self.interaction_matrix.get(pair_key, self.interaction_matrix.get(reverse_key))
                    
                    if interaction.interaction_type in [InteractionType.ANTAGONISTIC, InteractionType.INHIBITORY]:
                        analysis.conflicts.append((dhatu1, dhatu2))
                        analysis.coherence_score *= (1.0 - interaction.strength * 0.5)
                    elif interaction.interaction_type == InteractionType.SYNERGISTIC:
                        analysis.synergies.append((dhatu1, dhatu2))
                        analysis.coherence_score *= (1.0 + interaction.strength * 0.2)
        
        # 2. Évaluation contraintes
        if len(emotional_dhatus) > 4:
            analysis.constraints_violated.append("Limite cognitive dépassée (>4 dhātu émotionnels)")
            analysis.coherence_score *= 0.7
        
        if len(analysis.conflicts) > 1:
            analysis.constraints_violated.append("Trop de conflits simultanés")
            analysis.coherence_score *= 0.5
        
        # 3. Détermination validité
        if analysis.coherence_score < 0.3:
            analysis.validity = CompositionValidity.INVALID
        elif analysis.coherence_score < 0.6:
            analysis.validity = CompositionValidity.QUESTIONABLE
        
        # 4. Exemples phénoménologiques
        analysis.phenomenological_examples = self._find_phenomenological_examples(composition)
        
        # 5. Compositions alternatives
        if analysis.validity != CompositionValidity.VALID:
            analysis.alternative_compositions = self._suggest_alternative_compositions(composition)
        
        return analysis
    
    def _find_phenomenological_examples(self, composition: List[str]) -> List[str]:
        """Trouve exemples phénoménologiques pour une composition"""
        
        examples = []
        
        # Recherche dans les émotions documentées
        for emotion_name, data in self.phenomenological_data['documented_complex_emotions'].items():
            proposed_comp = data['composition_proposed']
            emotional_overlap = set(composition) & set(proposed_comp)
            if len(emotional_overlap) >= 2:
                examples.append(f"{emotion_name.lower()} (similarité: {len(emotional_overlap)}/{len(proposed_comp)})")
        
        # Exemples génériques basés sur patterns
        emotional_dhatus = [d for d in composition if d in self.panksepp_systems]
        if 'RAGE' in emotional_dhatus and 'FEAR' in emotional_dhatus:
            examples.append("Agitation anxieuse, colère défensive")
        if 'CARE' in emotional_dhatus and 'GRIEF' in emotional_dhatus:
            examples.append("Compassion, empathie pour souffrance")
        if 'SEEK' in emotional_dhatus and 'PLAY' in emotional_dhatus:
            examples.append("Curiosité ludique, exploration joyeuse")
        
        return examples
    
    def _suggest_alternative_compositions(self, problematic_composition: List[str]) -> List[List[str]]:
        """Suggère compositions alternatives moins problématiques"""
        
        alternatives = []
        emotional_dhatus = [d for d in problematic_composition if d in self.panksepp_systems]
        non_emotional = [d for d in problematic_composition if d not in self.panksepp_systems]
        
        # Stratégie 1: Remplacer dhātu antagonistes
        conflicts = self._detect_conflicts_in_composition(emotional_dhatus)
        for conflict_pair in conflicts:
            for dhatu_to_remove in conflict_pair:
                alternative = [d for d in emotional_dhatus if d != dhatu_to_remove] + non_emotional
                if len(alternative) >= 2:
                    alternatives.append(alternative)
        
        # Stratégie 2: Simplification (garder synergies)
        synergies = self._detect_synergies_in_composition(emotional_dhatus)
        if synergies:
            for synergy_pair in synergies:
                simplified = list(synergy_pair) + non_emotional
                alternatives.append(simplified)
        
        return alternatives[:3]  # Maximum 3 alternatives
    
    def _detect_conflicts_in_composition(self, emotional_dhatus: List[str]) -> List[Tuple[str, str]]:
        """Détecte conflits dans composition"""
        conflicts = []
        for i, dhatu1 in enumerate(emotional_dhatus):
            for dhatu2 in emotional_dhatus[i+1:]:
                pair_key = tuple(sorted([dhatu1, dhatu2]))
                if pair_key in self.interaction_matrix:
                    interaction = self.interaction_matrix[pair_key]
                    if interaction.interaction_type in [InteractionType.ANTAGONISTIC, InteractionType.INHIBITORY]:
                        conflicts.append((dhatu1, dhatu2))
        return conflicts
    
    def _detect_synergies_in_composition(self, emotional_dhatus: List[str]) -> List[Tuple[str, str]]:
        """Détecte synergies dans composition"""
        synergies = []
        for i, dhatu1 in enumerate(emotional_dhatus):
            for dhatu2 in emotional_dhatus[i+1:]:
                pair_key = tuple(sorted([dhatu1, dhatu2]))
                if pair_key in self.interaction_matrix:
                    interaction = self.interaction_matrix[pair_key]
                    if interaction.interaction_type == InteractionType.SYNERGISTIC:
                        synergies.append((dhatu1, dhatu2))
        return synergies
    
    def systematic_composability_analysis(self) -> Dict[str, Any]:
        """Analyse systématique de toutes les combinaisons possibles"""
        
        print("🔬 ANALYSE SYSTÉMATIQUE COMPOSABILITÉ PANKSEPP")
        print("=" * 50)
        
        results = {
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'analysis_type': 'Systematic Emotional Composability Analysis',
            'total_combinations_analyzed': 0,
            'valid_combinations': [],
            'questionable_combinations': [],
            'invalid_combinations': [],
            'antagonism_patterns': [],
            'synergy_patterns': [],
            'composability_matrix': {},
            'recommendations': []
        }
        
        # Test toutes combinaisons 2-4 dhātu émotionnels
        for size in range(2, 5):  # 2, 3, 4 dhātu
            print(f"\n🧪 Test combinaisons {size} dhātu émotionnels...")
            
            for combination in itertools.combinations(self.panksepp_systems, size):
                combination_list = list(combination)
                analysis = self.analyze_composition_validity(combination_list)
                results['total_combinations_analyzed'] += 1
                
                if analysis.validity == CompositionValidity.VALID:
                    results['valid_combinations'].append({
                        'composition': combination_list,
                        'coherence_score': analysis.coherence_score,
                        'synergies': analysis.synergies,
                        'examples': analysis.phenomenological_examples
                    })
                elif analysis.validity == CompositionValidity.QUESTIONABLE:
                    results['questionable_combinations'].append({
                        'composition': combination_list,
                        'coherence_score': analysis.coherence_score,
                        'conflicts': analysis.conflicts,
                        'alternatives': analysis.alternative_compositions
                    })
                else:
                    results['invalid_combinations'].append({
                        'composition': combination_list,
                        'coherence_score': analysis.coherence_score,
                        'conflicts': analysis.conflicts,
                        'constraints_violated': analysis.constraints_violated
                    })
        
        print(f"✅ Analysées: {results['total_combinations_analyzed']} combinaisons")
        print(f"✅ Valides: {len(results['valid_combinations'])}")
        print(f"⚠️ Douteuses: {len(results['questionable_combinations'])}")
        print(f"❌ Invalides: {len(results['invalid_combinations'])}")
        
        # Analyse patterns
        results['antagonism_patterns'] = self._analyze_antagonism_patterns(results)
        results['synergy_patterns'] = self._analyze_synergy_patterns(results)
        results['composability_matrix'] = self._build_composability_matrix()
        results['recommendations'] = self._generate_composability_recommendations(results)
        
        return results
    
    def _analyze_antagonism_patterns(self, results: Dict) -> List[Dict[str, Any]]:
        """Analyse patterns d'antagonismes"""
        
        antagonism_counts = {}
        
        # Compter antagonismes
        for combo_data in results['invalid_combinations'] + results['questionable_combinations']:
            for conflict in combo_data.get('conflicts', []):
                pair_key = tuple(sorted(conflict))
                antagonism_counts[pair_key] = antagonism_counts.get(pair_key, 0) + 1
        
        # Trier par fréquence
        patterns = []
        for pair, count in sorted(antagonism_counts.items(), key=lambda x: x[1], reverse=True):
            if pair in self.interaction_matrix:
                interaction = self.interaction_matrix[pair]
                patterns.append({
                    'pair': pair,
                    'frequency': count,
                    'interaction_type': interaction.interaction_type.value,
                    'strength': interaction.strength,
                    'neurobiological_basis': interaction.neurobiological_basis
                })
        
        return patterns
    
    def _analyze_synergy_patterns(self, results: Dict) -> List[Dict[str, Any]]:
        """Analyse patterns de synergies"""
        
        synergy_counts = {}
        
        for combo_data in results['valid_combinations']:
            for synergy in combo_data.get('synergies', []):
                pair_key = tuple(sorted(synergy))
                synergy_counts[pair_key] = synergy_counts.get(pair_key, 0) + 1
        
        patterns = []
        for pair, count in sorted(synergy_counts.items(), key=lambda x: x[1], reverse=True):
            if pair in self.interaction_matrix:
                interaction = self.interaction_matrix[pair]
                patterns.append({
                    'pair': pair,
                    'frequency': count,
                    'interaction_type': interaction.interaction_type.value,
                    'strength': interaction.strength,
                    'benefits': interaction.examples
                })
        
        return patterns
    
    def _build_composability_matrix(self) -> Dict[str, Dict[str, float]]:
        """Construit matrice de composabilité entre tous dhātu"""
        
        matrix = {}
        
        for dhatu1 in self.panksepp_systems:
            matrix[dhatu1] = {}
            for dhatu2 in self.panksepp_systems:
                if dhatu1 == dhatu2:
                    matrix[dhatu1][dhatu2] = 1.0
                else:
                    pair_key = tuple(sorted([dhatu1, dhatu2]))
                    if pair_key in self.interaction_matrix:
                        interaction = self.interaction_matrix[pair_key]
                        if interaction.interaction_type == InteractionType.SYNERGISTIC:
                            score = 0.7 + interaction.strength * 0.3
                        elif interaction.interaction_type == InteractionType.NEUTRAL:
                            score = 0.5
                        elif interaction.interaction_type == InteractionType.COMPETITIVE:
                            score = 0.4 - interaction.strength * 0.2
                        else:  # ANTAGONISTIC, INHIBITORY
                            score = 0.2 - interaction.strength * 0.2
                        matrix[dhatu1][dhatu2] = score
                    else:
                        matrix[dhatu1][dhatu2] = 0.5  # Neutre par défaut
        
        return matrix
    
    def _generate_composability_recommendations(self, results: Dict) -> List[str]:
        """Génère recommandations pour composabilité"""
        
        recommendations = []
        
        valid_ratio = len(results['valid_combinations']) / results['total_combinations_analyzed']
        
        if valid_ratio > 0.7:
            recommendations.append("✅ Excellente composabilité générale (>70% combinaisons valides)")
        elif valid_ratio > 0.5:
            recommendations.append("⚠️ Composabilité modérée - attention aux antagonismes")
        else:
            recommendations.append("❌ Composabilité limitée - revoir architecture émotionnelle")
        
        # Recommandations spécifiques antagonismes
        top_antagonisms = results['antagonism_patterns'][:3]
        for pattern in top_antagonisms:
            dhatu1, dhatu2 = pattern['pair']
            recommendations.append(f"🚫 Éviter {dhatu1}+{dhatu2} (antagonisme fort)")
        
        # Recommandations synergies
        top_synergies = results['synergy_patterns'][:3]
        for pattern in top_synergies:
            dhatu1, dhatu2 = pattern['pair']
            recommendations.append(f"✨ Favoriser {dhatu1}+{dhatu2} (synergie documentée)")
        
        return recommendations

def main():
    """Analyse complète composabilité émotionnelle"""
    
    print("🔬 ANALYSEUR COMPOSABILITÉ ÉMOTIONNELLE PANKSEPP")
    print("=" * 50)
    print("🎯 Objectif: Analyser composabilité réelle au-delà de la validation biologique")
    
    analyzer = EmotionalComposabilityAnalyzer()
    
    # Test compositions spécifiques
    print(f"\n🧪 TEST COMPOSITIONS SPÉCIFIQUES")
    print("=" * 35)
    
    test_compositions = [
        ['RAGE', 'CARE'],           # Antagonisme fort
        ['SEEK', 'PLAY'],          # Synergie documentée  
        ['GRIEF', 'PLAY'],         # Compétition
        ['RAGE', 'FEAR', 'CARE'],  # Jalousie (antagonisme + synergie)
        ['GRIEF', 'SEEK', 'EXIST'], # Nostalgie
        ['LUST', 'CARE', 'CREAT']   # Passion créative
    ]
    
    for composition in test_compositions:
        analysis = analyzer.analyze_composition_validity(composition)
        status_emoji = {"valid": "✅", "questionable": "⚠️", "invalid": "❌"}
        
        print(f"{status_emoji[analysis.validity.value]} {' + '.join(composition)}: "
              f"{analysis.coherence_score:.3f} ({analysis.validity.value})")
        
        if analysis.conflicts:
            print(f"   🚫 Conflits: {', '.join([f'{c[0]}↔{c[1]}' for c in analysis.conflicts])}")
        if analysis.synergies:
            print(f"   ✨ Synergies: {', '.join([f'{s[0]}+{s[1]}' for s in analysis.synergies])}")
    
    # Analyse systématique
    print(f"\n⚡ ANALYSE SYSTÉMATIQUE TOUTES COMBINAISONS")
    results = analyzer.systematic_composability_analysis()
    
    print(f"\n🎊 RÉSULTATS COMPOSABILITÉ")
    print("=" * 30)
    print(f"📊 Total analysé: {results['total_combinations_analyzed']} combinaisons")
    print(f"✅ Valides: {len(results['valid_combinations'])} ({len(results['valid_combinations'])/results['total_combinations_analyzed']*100:.1f}%)")
    print(f"⚠️ Douteuses: {len(results['questionable_combinations'])}")  
    print(f"❌ Invalides: {len(results['invalid_combinations'])}")
    
    print(f"\n🔍 TOP ANTAGONISMES:")
    for pattern in results['antagonism_patterns'][:5]:
        dhatu1, dhatu2 = pattern['pair']
        print(f"   🚫 {dhatu1} ↔ {dhatu2}: {pattern['interaction_type']} (force: {pattern['strength']:.2f})")
    
    print(f"\n✨ TOP SYNERGIES:")
    for pattern in results['synergy_patterns'][:5]:
        dhatu1, dhatu2 = pattern['pair']
        print(f"   ✨ {dhatu1} + {dhatu2}: renforcement mutuel (force: {pattern['strength']:.2f})")
    
    print(f"\n💡 RECOMMANDATIONS:")
    for rec in results['recommendations']:
        print(f"   {rec}")
    
    # Sauvegarde
    timestamp = int(time.time())
    
    with open(f'analyse_composabilite_emotionnelle_{timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 RAPPORT DÉTAILLÉ: analyse_composabilite_emotionnelle_{timestamp}.json")
    
    # Évaluation finale
    valid_ratio = len(results['valid_combinations']) / results['total_combinations_analyzed']
    if valid_ratio > 0.7:
        print(f"\n🎯 CONCLUSION: Architecture Panksepp excellente composabilité!")
    elif valid_ratio > 0.5:
        print(f"\n⚠️ CONCLUSION: Composabilité modérée - attention aux antagonismes")
    else:
        print(f"\n❌ CONCLUSION: Problèmes composabilité majeurs - révision nécessaire")

if __name__ == "__main__":
    main()