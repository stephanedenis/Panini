#!/usr/bin/env python3
"""
ANALYSEUR ANTAGONISMES ÉMOTIONNELS AVANCÉ
========================================

Détection automatique des antagonismes implicites basée sur la neurobiologie,
la phénoménologie et la logique compositionnelle des émotions Panksepp.
"""

import json
import time
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass

@dataclass
class AntagonismAnalysis:
    """Analyse détaillée d'un antagonisme émotionnel"""
    dhatu_pair: Tuple[str, str]
    antagonism_strength: float
    neurobiological_conflict: str
    phenomenological_evidence: str
    composability_impact: str
    resolution_mechanisms: List[str]
    real_world_examples: List[str]

class AdvancedEmotionalAntagonismAnalyzer:
    """Analyseur avancé des antagonismes émotionnels"""
    
    def __init__(self):
        self.panksepp_systems = ['SEEK', 'RAGE', 'FEAR', 'LUST', 'CARE', 'GRIEF', 'PLAY']
        self.neurobiological_circuits = self._define_neural_circuits()
        self.phenomenological_oppositions = self._define_phenomenological_oppositions()
        
    def _define_neural_circuits(self) -> Dict[str, Dict[str, Any]]:
        """Définit circuits neurobiologiques de chaque système Panksepp"""
        
        return {
            'SEEK': {
                'primary_circuits': ['VTA', 'Nucleus Accumbens', 'Cortex Préfrontal'],
                'neurotransmitters': ['Dopamine'],
                'activation_pattern': 'Approche, exploration, motivation',
                'inhibited_by': ['Stress élevé', 'Peur intense', 'Dépression'],
                'competes_with': ['Systèmes évitement']
            },
            'RAGE': {
                'primary_circuits': ['Amygdale', 'Hypothalamus', 'PAG'],
                'neurotransmitters': ['Noradrénaline', 'Testostérone'],
                'activation_pattern': 'Attack, domination, destruction',
                'inhibited_by': ['Ocytocine élevée', 'Sérotonine'],
                'competes_with': ['Systèmes affiliation']
            },
            'FEAR': {
                'primary_circuits': ['Amygdale', 'Hippocampe', 'Locus Coeruleus'],
                'neurotransmitters': ['Noradrénaline', 'GABA déficit'],
                'activation_pattern': 'Évitement, freeze, fuite',
                'inhibited_by': ['GABA', 'Opioïdes'],
                'competes_with': ['Systèmes approche']
            },
            'LUST': {
                'primary_circuits': ['Hypothalamus', 'Aire préoptique'],
                'neurotransmitters': ['Testostérone', 'Œstrogènes', 'Dopamine'],
                'activation_pattern': 'Recherche sexuelle, copulation',
                'inhibited_by': ['Cortisol', 'Prolactine', 'Stress'],
                'competes_with': ['Systèmes stress']
            },
            'CARE': {
                'primary_circuits': ['Cortex cingulaire', 'Aire préoptique'],
                'neurotransmitters': ['Ocytocine', 'Vasopressine', 'Opioïdes'],
                'activation_pattern': 'Protection, nurturing, empathie',
                'inhibited_by': ['Stress chronique', 'Testostérone élevée'],
                'competes_with': ['Systèmes agression']
            },
            'GRIEF': {
                'primary_circuits': ['Cingulaire antérieur', 'Système opioïde'],
                'neurotransmitters': ['Opioïdes endogènes', 'Cortisol'],
                'activation_pattern': 'Détresse séparation, pleurs',
                'inhibited_by': ['Ocytocine', 'Dopamine'],
                'competes_with': ['Systèmes récompense']
            },
            'PLAY': {
                'primary_circuits': ['Cortex préfrontal', 'Système cannabinoïde'],
                'neurotransmitters': ['Anandamide', 'Dopamine'],
                'activation_pattern': 'Jeu social, exploration joyeuse',
                'inhibited_by': ['Cortisol', 'Stress'],
                'competes_with': ['Systèmes stress/survie']
            }
        }
    
    def _define_phenomenological_oppositions(self) -> List[Dict[str, Any]]:
        """Définit oppositions phénoménologiques documentées"""
        
        return [
            {
                'pair': ('RAGE', 'CARE'),
                'opposition_type': 'Motivational',
                'description': 'Destruction vs construction, agression vs protection',
                'intensity_dependency': True,
                'temporal_resolution': 'Possible alternance rapide',
                'examples': ['Parent protège enfant (CARE) puis attaque agresseur (RAGE)'],
                'phenomenology': 'Tensions entre impulse destructeur et protecteur'
            },
            {
                'pair': ('FEAR', 'SEEK'),
                'opposition_type': 'Behavioral',
                'description': 'Évitement vs approche, retrait vs exploration', 
                'intensity_dependency': True,
                'temporal_resolution': 'Alternance lente nécessaire',
                'examples': ['Phobie bloque curiosité', 'Anxiété paralyse apprentissage'],
                'phenomenology': 'Conflit approche-évitement classique'
            },
            {
                'pair': ('GRIEF', 'PLAY'),
                'opposition_type': 'Affective',
                'description': 'Douleur vs plaisir, fermeture vs ouverture',
                'intensity_dependency': True,
                'temporal_resolution': 'Transition graduelle possible',
                'examples': ['Deuil empêche jeu spontané', 'Dépression = absence PLAY'],
                'phenomenology': 'Incompatibilité tonale émotionnelle'
            },
            {
                'pair': ('GRIEF', 'LUST'),
                'opposition_type': 'Physiological',
                'description': 'Stress vs reproduction, fermeture vs ouverture',
                'intensity_dependency': False,
                'temporal_resolution': 'Récupération lente nécessaire',
                'examples': ['Deuil conjugal', 'Dépression sexuelle'],
                'phenomenology': 'Incompatibilité énergétique fondamentale'
            },
            {
                'pair': ('RAGE', 'GRIEF'),
                'opposition_type': 'Energetic',
                'description': 'Externalisation vs internalisation, action vs passivité',
                'intensity_dependency': True,
                'temporal_resolution': 'Alternance possible',
                'examples': ['Colère masque chagrin', 'Basculement rage→tristesse'],
                'phenomenology': 'Différence direction énergie émotionnelle'
            }
        ]
    
    def analyze_implicit_antagonisms(self) -> Dict[str, Any]:
        """Analyse tous les antagonismes implicites possibles"""
        
        print("🔍 ANALYSE ANTAGONISMES ÉMOTIONNELS AVANCÉE")
        print("=" * 45)
        
        results = {
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'analysis_type': 'Advanced Emotional Antagonism Detection',
            'detected_antagonisms': [],
            'neurobiological_conflicts': [],
            'phenomenological_conflicts': [],
            'composability_warnings': [],
            'resolution_strategies': {}
        }
        
        # Analyse toutes paires possibles
        for i, dhatu1 in enumerate(self.panksepp_systems):
            for dhatu2 in self.panksepp_systems[i+1:]:
                
                antagonism = self._analyze_pair_antagonism(dhatu1, dhatu2)
                
                if antagonism.antagonism_strength > 0.3:  # Seuil significatif
                    results['detected_antagonisms'].append({
                        'pair': antagonism.dhatu_pair,
                        'strength': antagonism.antagonism_strength,
                        'neurobiological_conflict': antagonism.neurobiological_conflict,
                        'phenomenological_evidence': antagonism.phenomenological_evidence,
                        'composability_impact': antagonism.composability_impact,
                        'resolution_mechanisms': antagonism.resolution_mechanisms,
                        'real_world_examples': antagonism.real_world_examples
                    })
                    
                    print(f"⚠️ {dhatu1} ↔ {dhatu2}: {antagonism.antagonism_strength:.3f}")
                    print(f"   💭 {antagonism.phenomenological_evidence}")
                    
        print(f"\n📊 {len(results['detected_antagonisms'])} antagonismes détectés")
        
        # Classification par force
        strong_antagonisms = [a for a in results['detected_antagonisms'] if a['strength'] > 0.7]
        moderate_antagonisms = [a for a in results['detected_antagonisms'] if 0.5 < a['strength'] <= 0.7]
        weak_antagonisms = [a for a in results['detected_antagonisms'] if 0.3 < a['strength'] <= 0.5]
        
        results['classification'] = {
            'strong_antagonisms': len(strong_antagonisms),
            'moderate_antagonisms': len(moderate_antagonisms),
            'weak_antagonisms': len(weak_antagonisms)
        }
        
        # Génération stratégies résolution
        results['resolution_strategies'] = self._generate_resolution_strategies(results['detected_antagonisms'])
        
        return results
    
    def _analyze_pair_antagonism(self, dhatu1: str, dhatu2: str) -> AntagonismAnalysis:
        """Analyse antagonisme pour une paire spécifique"""
        
        circuit1 = self.neurobiological_circuits[dhatu1]
        circuit2 = self.neurobiological_circuits[dhatu2]
        
        # 1. Conflit neurobiologique
        neuro_conflict_score = self._calculate_neurobiological_conflict(circuit1, circuit2)
        neuro_conflict_desc = self._describe_neurobiological_conflict(dhatu1, dhatu2, circuit1, circuit2)
        
        # 2. Opposition phénoménologique
        phenom_conflict_score = self._calculate_phenomenological_conflict(dhatu1, dhatu2)
        phenom_evidence = self._get_phenomenological_evidence(dhatu1, dhatu2)
        
        # 3. Score global antagonisme
        antagonism_strength = (neuro_conflict_score + phenom_conflict_score) / 2
        
        # 4. Impact composabilité
        composability_impact = self._assess_composability_impact(dhatu1, dhatu2, antagonism_strength)
        
        # 5. Mécanismes résolution
        resolution_mechanisms = self._identify_resolution_mechanisms(dhatu1, dhatu2, antagonism_strength)
        
        # 6. Exemples réels
        real_examples = self._generate_real_world_examples(dhatu1, dhatu2)
        
        return AntagonismAnalysis(
            dhatu_pair=(dhatu1, dhatu2),
            antagonism_strength=antagonism_strength,
            neurobiological_conflict=neuro_conflict_desc,
            phenomenological_evidence=phenom_evidence,
            composability_impact=composability_impact,
            resolution_mechanisms=resolution_mechanisms,
            real_world_examples=real_examples
        )
    
    def _calculate_neurobiological_conflict(self, circuit1: Dict, circuit2: Dict) -> float:
        """Calcule conflit neurobiologique entre deux circuits"""
        
        score = 0.0
        
        # Compétition neurotransmetteurs
        nt1 = set(circuit1['neurotransmitters'])
        nt2 = set(circuit2['neurotransmitters'])
        
        # Neurotransmetteurs opposés connus
        opposing_pairs = [
            ('Dopamine', 'Cortisol'),
            ('Ocytocine', 'Testostérone'),
            ('GABA', 'Noradrénaline')
        ]
        
        for nt_a, nt_b in opposing_pairs:
            if (nt_a in nt1 and nt_b in nt2) or (nt_b in nt1 and nt_a in nt2):
                score += 0.3
        
        # Compétition circuits anatomiques
        circuits1 = set(circuit1['primary_circuits'])
        circuits2 = set(circuit2['primary_circuits'])
        
        # Circuits concurrents connus
        competing_regions = [
            ('Amygdale', 'Cortex Préfrontal'),
            ('VTA', 'Locus Coeruleus')
        ]
        
        for region_a, region_b in competing_regions:
            if (region_a in circuits1 and region_b in circuits2) or \
               (region_b in circuits1 and region_a in circuits2):
                score += 0.4
        
        # Inhibition documentée
        if any(circuit2['activation_pattern'] in inhibitor 
               for inhibitor in circuit1.get('competes_with', [])):
            score += 0.5
            
        if any(circuit1['activation_pattern'] in inhibitor 
               for inhibitor in circuit2.get('competes_with', [])):
            score += 0.5
        
        return min(score, 1.0)
    
    def _describe_neurobiological_conflict(self, dhatu1: str, dhatu2: str, 
                                         circuit1: Dict, circuit2: Dict) -> str:
        """Décrit conflit neurobiologique"""
        
        conflicts = []
        
        # Circuits opposés
        if 'Amygdale' in circuit1['primary_circuits'] and \
           'Cortex Préfrontal' in circuit2['primary_circuits']:
            conflicts.append("Amygdale (émotion) vs PFC (régulation)")
            
        # Neurotransmetteurs
        if 'Dopamine' in circuit1['neurotransmitters'] and \
           'Cortisol' in circuit2['neurotransmitters']:
            conflicts.append("Dopamine (récompense) vs Cortisol (stress)")
            
        if not conflicts:
            conflicts.append(f"Activation {circuit1['activation_pattern']} vs {circuit2['activation_pattern']}")
            
        return "; ".join(conflicts)
    
    def _calculate_phenomenological_conflict(self, dhatu1: str, dhatu2: str) -> float:
        """Calcule conflit phénoménologique"""
        
        # Cherche dans oppositions documentées
        for opposition in self.phenomenological_oppositions:
            if set(opposition['pair']) == {dhatu1, dhatu2}:
                base_score = 0.8
                if opposition['intensity_dependency']:
                    return base_score * 0.8  # Réductible avec gestion intensité
                return base_score
        
        # Oppositions logiques implicites
        oppositions_logiques = {
            ('SEEK', 'FEAR'): 0.7,    # Approche vs évitement
            ('RAGE', 'CARE'): 0.8,    # Destruction vs construction  
            ('GRIEF', 'PLAY'): 0.6,   # Fermeture vs ouverture
            ('GRIEF', 'LUST'): 0.7,   # Retrait vs engagement
            ('RAGE', 'GRIEF'): 0.5    # Externalisation vs internalisation
        }
        
        pair_key = tuple(sorted([dhatu1, dhatu2]))
        return oppositions_logiques.get(pair_key, 0.2)  # Conflit faible par défaut
    
    def _get_phenomenological_evidence(self, dhatu1: str, dhatu2: str) -> str:
        """Obtient évidence phénoménologique"""
        
        for opposition in self.phenomenological_oppositions:
            if set(opposition['pair']) == {dhatu1, dhatu2}:
                return opposition['description']
        
        # Descriptions par défaut
        default_descriptions = {
            ('RAGE', 'CARE'): "Impulsion destructrice vs protectrice",
            ('SEEK', 'FEAR'): "Curiosité vs prudence excessive",
            ('GRIEF', 'PLAY'): "Fermeture émotionnelle vs ouverture ludique",
            ('GRIEF', 'LUST'): "Retrait vs engagement sensuel",
            ('RAGE', 'GRIEF'): "Action vs passivité émotionnelle"
        }
        
        pair_key = tuple(sorted([dhatu1, dhatu2]))
        return default_descriptions.get(pair_key, "Opposition motivationnelle")
    
    def _assess_composability_impact(self, dhatu1: str, dhatu2: str, strength: float) -> str:
        """Évalue impact sur composabilité"""
        
        if strength > 0.8:
            return "CRITIQUE - Éviter coactivation simultanée"
        elif strength > 0.6:
            return "MODÉRÉ - Nécessite gestion intensités ou alternance"
        elif strength > 0.4:
            return "LÉGER - Coexistence possible avec précautions"
        else:
            return "MINIMAL - Composition généralement viable"
    
    def _identify_resolution_mechanisms(self, dhatu1: str, dhatu2: str, strength: float) -> List[str]:
        """Identifie mécanismes de résolution"""
        
        mechanisms = []
        
        if strength > 0.7:
            mechanisms.extend([
                "Alternance temporelle stricte",
                "Séparation contextuelle",
                "Gestion intensité différentielle"
            ])
        elif strength > 0.5:
            mechanisms.extend([
                "Modulation intensité",
                "Transition graduelle",
                "Focus attentionnel sélectif"
            ])
        else:
            mechanisms.extend([
                "Coexistence naturelle possible",
                "Équilibre dynamique"
            ])
            
        # Mécanismes spécifiques
        specific_mechanisms = {
            ('RAGE', 'CARE'): ["Protection focalisée différentielle"],
            ('FEAR', 'SEEK'): ["Exploration graduelle sécurisée"],
            ('GRIEF', 'PLAY'): ["Jeu thérapeutique progressif"]
        }
        
        pair_key = tuple(sorted([dhatu1, dhatu2]))
        if pair_key in specific_mechanisms:
            mechanisms.extend(specific_mechanisms[pair_key])
        
        return mechanisms
    
    def _generate_real_world_examples(self, dhatu1: str, dhatu2: str) -> List[str]:
        """Génère exemples concrets"""
        
        examples_map = {
            ('RAGE', 'CARE'): [
                "Parent en colère contre menace externe mais doux avec enfant",
                "Défense agressive du territoire familial",
                "Alternance colère-tendresse parentale"
            ],
            ('FEAR', 'SEEK'): [
                "Phobie sociale empêche exploration relationnelle", 
                "Anxiété performance bloque apprentissage",
                "Prudence excessive limite découvertes"
            ],
            ('GRIEF', 'PLAY'): [
                "Deuil empêche jeu spontané enfant",
                "Dépression = perte capacité ludique",
                "Mélancolie créative vs anhédonie"
            ],
            ('GRIEF', 'LUST'): [
                "Deuil conjugal inhibe désir sexuel",
                "Dépression diminue libido",
                "Récupération lente après perte"
            ]
        }
        
        pair_key = tuple(sorted([dhatu1, dhatu2]))
        return examples_map.get(pair_key, ["Conflit motivationnel général"])
    
    def _generate_resolution_strategies(self, antagonisms: List[Dict]) -> Dict[str, List[str]]:
        """Génère stratégies globales de résolution"""
        
        strategies = {
            'architectural': [
                "Éviter >2 antagonismes forts par composition",
                "Privilégier alternance temporelle pour conflits critiques",
                "Implémenter mécanismes de transition graduée"
            ],
            'implementation': [
                "Système de pondération intensité",
                "Détection automatique conflits",
                "Suggestions compositions alternatives"
            ],
            'therapeutic': [
                "Reconnaissance patterns antagonistes personnels",
                "Techniques gestion émotions conflictuelles",
                "Développement flexibilité émotionnelle"
            ]
        }
        
        return strategies

def main():
    """Analyse avancée antagonismes émotionnels"""
    
    analyzer = AdvancedEmotionalAntagonismAnalyzer()
    results = analyzer.analyze_implicit_antagonisms()
    
    print(f"\n🎊 SYNTHÈSE ANTAGONISMES AVANCÉE")
    print("=" * 35)
    
    classification = results['classification']
    print(f"🔴 Antagonismes forts (>0.7): {classification['strong_antagonisms']}")
    print(f"🟡 Antagonismes modérés (0.5-0.7): {classification['moderate_antagonisms']}")
    print(f"🟢 Antagonismes faibles (0.3-0.5): {classification['weak_antagonisms']}")
    
    print(f"\n🔧 STRATÉGIES RÉSOLUTION:")
    for category, strategies in results['resolution_strategies'].items():
        print(f"   {category.upper()}:")
        for strategy in strategies[:2]:
            print(f"     • {strategy}")
    
    # Sauvegarde
    timestamp = int(time.time())
    
    with open(f'analyse_antagonismes_avancee_{timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 ANALYSE COMPLÈTE: analyse_antagonismes_avancee_{timestamp}.json")
    
    # Recommandation finale
    strong_count = classification['strong_antagonisms']
    if strong_count <= 2:
        print(f"\n✅ CONCLUSION: Antagonismes gérables - Architecture Panksepp viable")
    elif strong_count <= 4:
        print(f"\n⚠️ CONCLUSION: Antagonismes modérés - Précautions nécessaires")
    else:
        print(f"\n❌ CONCLUSION: Trop d'antagonismes - Révision architecture recommandée")

if __name__ == "__main__":
    main()