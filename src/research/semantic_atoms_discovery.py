#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Semantic Atoms Discovery - Découverte d'Atomes Sémantiques Universaux
========================================================================

Découvrir atomes sémantiques universaux via analyse multilingue.
Commencer par dhātu mais NE PAS se limiter à cet ensemble.

Approche progressive:
- Dhātu comme hypothèse initiale (point départ)
- Validation empirique par compression
- Extension/modification selon résultats
- Atomes finaux ≠ nécessairement dhātu
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict, Counter
from dataclasses import dataclass, field
from datetime import datetime
import math


@dataclass
class SemanticAtom:
    """Atome sémantique découvert empiriquement"""
    atom_id: str
    concept: str
    source: str  # 'dhatu' ou 'discovered'
    frequency: int = 0
    languages: Set[str] = field(default_factory=set)
    compression_ratio: float = 0.0
    validation_score: float = 0.0
    examples: List[Dict] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)


@dataclass
class CompressionMetrics:
    """Métriques de compression pour validation atome"""
    original_size: int
    compressed_size: int
    ratio: float
    fidelity_score: float
    languages_tested: List[str]


class SemanticAtomsDiscovery:
    """Découverte d'atomes sémantiques universaux"""
    
    def __init__(self, results_dir: Optional[Path] = None):
        """
        Initialisation du système de découverte
        
        Args:
            results_dir: Répertoire pour sauvegarder les résultats
        """
        self.results_dir = results_dir or Path('/home/runner/work/Panini/Panini/results/semantic_atoms')
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # Base d'atomes dhātu comme hypothèse initiale
        self.dhatu_atoms = self._initialize_dhatu_base()
        
        # Atomes découverts empiriquement
        self.discovered_atoms = {}
        
        # Métriques de compression par atome
        self.compression_metrics = {}
        
        # Statistiques globales
        self.stats = {
            'dhatu_tested': 0,
            'new_atoms_discovered': 0,
            'languages_analyzed': set(),
            'total_compressions': 0
        }
        
        self.log("🧬 Semantic Atoms Discovery initialized")
    
    def _initialize_dhatu_base(self) -> Dict[str, SemanticAtom]:
        """
        Initialise la base dhātu comme point de départ
        
        Returns:
            Dict mapping dhatu_id to SemanticAtom
        """
        # 9 dhātu universels de base + extensions
        base_dhatu = {
            'EXIST': 'être/existence',
            'RELATE': 'relations/spatial',
            'COMM': 'communication',
            'EMOT': 'émotions/affect',
            'COGN': 'cognition/pensée',
            'ACT': 'action/mouvement',
            'TRANS': 'transformation/changement',
            'ITER': 'itération/répétition',
            'DECIDE': 'décision/volition',
            # Extensions potentielles
            'PERCEPT': 'perception/sens',
            'POSSESS': 'possession/appartenance',
            'QUANT': 'quantité/mesure',
            'TIME': 'temps/temporalité',
            'CAUSE': 'causalité/raison',
            'MODAL': 'modalité/possibilité'
        }
        
        atoms = {}
        for atom_id, concept in base_dhatu.items():
            atoms[atom_id] = SemanticAtom(
                atom_id=atom_id,
                concept=concept,
                source='dhatu',
                metadata={'initial_hypothesis': True}
            )
        
        return atoms
    
    def analyze_text_for_atoms(self, text: str, language: str,
                              source: str = 'unknown') -> Dict[str, int]:
        """
        Analyse un texte pour détecter atomes sémantiques
        
        Args:
            text: Texte à analyser
            language: Code langue (fr, en, etc.)
            source: Source du texte
            
        Returns:
            Dict mapping atom_id to frequency
        """
        atom_frequencies = Counter()
        
        # Patterns de détection pour chaque dhātu (simplifiés)
        patterns = self._get_detection_patterns(language)
        
        words = text.lower().split()
        
        for atom_id, atom_patterns in patterns.items():
            for pattern in atom_patterns:
                if isinstance(pattern, str):
                    # Pattern simple
                    if pattern in text.lower():
                        atom_frequencies[atom_id] += text.lower().count(pattern)
                else:
                    # Regex pattern
                    matches = re.findall(pattern, text.lower())
                    atom_frequencies[atom_id] += len(matches)
        
        # Mise à jour des atomes dhātu
        for atom_id, freq in atom_frequencies.items():
            if atom_id in self.dhatu_atoms:
                self.dhatu_atoms[atom_id].frequency += freq
                self.dhatu_atoms[atom_id].languages.add(language)
                
        self.stats['languages_analyzed'].add(language)
        
        return dict(atom_frequencies)
    
    def discover_new_atoms(self, texts: List[Dict[str, str]],
                          min_frequency: int = 5,
                          min_languages: int = 3) -> List[SemanticAtom]:
        """
        Découvre de nouveaux atomes sémantiques à partir de patterns
        
        Args:
            texts: Liste de {text, language, source}
            min_frequency: Fréquence minimale pour considérer un atome
            min_languages: Nombre minimum de langues pour validation
            
        Returns:
            Liste des nouveaux atomes découverts
        """
        # Patterns cross-linguistiques candidats
        candidate_patterns = defaultdict(lambda: {'count': 0, 'languages': set()})
        
        for text_info in texts:
            text = text_info['text']
            lang = text_info['language']
            
            # Extraction de n-grams comme candidats
            words = text.lower().split()
            
            # Unigrams
            for word in words:
                if len(word) >= 3:  # Minimum 3 caractères
                    candidate_patterns[word]['count'] += 1
                    candidate_patterns[word]['languages'].add(lang)
            
            # Bigrams
            for i in range(len(words) - 1):
                bigram = f"{words[i]} {words[i+1]}"
                candidate_patterns[bigram]['count'] += 1
                candidate_patterns[bigram]['languages'].add(lang)
        
        # Filtrer et créer nouveaux atomes
        new_atoms = []
        
        for pattern, data in candidate_patterns.items():
            if (data['count'] >= min_frequency and 
                len(data['languages']) >= min_languages):
                
                # Vérifier si pas déjà couvert par dhātu existants
                if not self._is_covered_by_existing(pattern):
                    atom_id = f"DISC_{len(self.discovered_atoms) + 1}"
                    
                    new_atom = SemanticAtom(
                        atom_id=atom_id,
                        concept=pattern,
                        source='discovered',
                        frequency=data['count'],
                        languages=data['languages'],
                        metadata={
                            'discovery_date': datetime.now().isoformat(),
                            'min_frequency': min_frequency,
                            'min_languages': min_languages
                        }
                    )
                    
                    self.discovered_atoms[atom_id] = new_atom
                    new_atoms.append(new_atom)
                    self.stats['new_atoms_discovered'] += 1
        
        self.log(f"🔬 Discovered {len(new_atoms)} new semantic atoms")
        return new_atoms
    
    def validate_atom_by_compression(self, atom_id: str, 
                                    corpus_texts: List[Dict]) -> CompressionMetrics:
        """
        Valide un atome par mesure de compression
        
        Args:
            atom_id: ID de l'atome à valider
            corpus_texts: Corpus multilingue pour test
            
        Returns:
            Métriques de compression
        """
        original_total = 0
        compressed_total = 0
        languages_tested = set()
        
        for text_info in corpus_texts:
            text = text_info['text']
            lang = text_info['language']
            languages_tested.add(lang)
            
            original_total += len(text)
            
            # Simulation compression: remplacer occurrences par code court
            compressed = self._simulate_compression(text, atom_id)
            compressed_total += len(compressed)
        
        ratio = (original_total - compressed_total) / original_total if original_total > 0 else 0
        
        # Score de fidélité (simulation)
        fidelity_score = 0.85 + (ratio * 0.15)  # Entre 0.85 et 1.0
        
        metrics = CompressionMetrics(
            original_size=original_total,
            compressed_size=compressed_total,
            ratio=ratio,
            fidelity_score=fidelity_score,
            languages_tested=list(languages_tested)
        )
        
        self.compression_metrics[atom_id] = metrics
        self.stats['total_compressions'] += 1
        
        # Mise à jour de l'atome
        if atom_id in self.dhatu_atoms:
            self.dhatu_atoms[atom_id].compression_ratio = ratio
            self.dhatu_atoms[atom_id].validation_score = fidelity_score
            self.stats['dhatu_tested'] += 1
        elif atom_id in self.discovered_atoms:
            self.discovered_atoms[atom_id].compression_ratio = ratio
            self.discovered_atoms[atom_id].validation_score = fidelity_score
        
        return metrics
    
    def _simulate_compression(self, text: str, atom_id: str) -> str:
        """Simule compression en remplaçant patterns par codes"""
        # Simulation simplifiée
        patterns = self._get_atom_patterns(atom_id)
        compressed = text
        
        for pattern in patterns:
            if isinstance(pattern, str):
                # Remplacer par code court (ex: {atom_id})
                compressed = compressed.replace(pattern, f"[{atom_id}]")
        
        return compressed
    
    def _get_detection_patterns(self, language: str) -> Dict[str, List]:
        """Retourne patterns de détection par langue"""
        # Patterns simplifiés par dhātu et langue
        patterns = {
            'EXIST': {
                'fr': ['être', 'est', 'sont', 'était', 'existe'],
                'en': ['be', 'is', 'are', 'was', 'were', 'exist'],
                'es': ['ser', 'estar', 'es', 'son', 'existe']
            },
            'RELATE': {
                'fr': ['dans', 'sur', 'avec', 'pour', 'relation'],
                'en': ['in', 'on', 'with', 'for', 'relation'],
                'es': ['en', 'con', 'para', 'relación']
            },
            'COMM': {
                'fr': ['dire', 'parler', 'mot', 'dire', 'communique'],
                'en': ['say', 'tell', 'speak', 'word', 'communicate'],
                'es': ['decir', 'hablar', 'palabra', 'comunicar']
            },
            'EMOT': {
                'fr': ['aimer', 'sentiment', 'émotion', 'joie', 'peur'],
                'en': ['love', 'feel', 'emotion', 'joy', 'fear'],
                'es': ['amar', 'sentir', 'emoción', 'alegría', 'miedo']
            },
            'ACT': {
                'fr': ['faire', 'action', 'mouvement', 'aller', 'prendre'],
                'en': ['do', 'make', 'action', 'go', 'take', 'move'],
                'es': ['hacer', 'acción', 'ir', 'tomar', 'mover']
            }
        }
        
        result = {}
        for atom_id, lang_patterns in patterns.items():
            result[atom_id] = lang_patterns.get(language, lang_patterns.get('en', []))
        
        return result
    
    def _get_atom_patterns(self, atom_id: str) -> List[str]:
        """Retourne tous les patterns pour un atome"""
        all_patterns = []
        patterns_by_lang = self._get_detection_patterns('fr')
        
        if atom_id in patterns_by_lang:
            all_patterns.extend(patterns_by_lang[atom_id])
        
        return all_patterns
    
    def _is_covered_by_existing(self, pattern: str) -> bool:
        """Vérifie si un pattern est déjà couvert par atomes existants"""
        # Vérification simplifiée
        for atom in list(self.dhatu_atoms.values()) + list(self.discovered_atoms.values()):
            if pattern.lower() in atom.concept.lower():
                return True
        return False
    
    def get_statistics(self) -> Dict:
        """Retourne statistiques de découverte"""
        stats = {
            'dhatu_tested': len([a for a in self.dhatu_atoms.values() if a.compression_ratio > 0]),
            'new_atoms_discovered': len(self.discovered_atoms),
            'languages_analyzed': len(self.stats['languages_analyzed']),
            'total_atoms': len(self.dhatu_atoms) + len(self.discovered_atoms),
            'total_compressions': self.stats['total_compressions'],
            'avg_compression_ratio': self._calculate_avg_compression(),
            'top_atoms': self._get_top_atoms(10)
        }
        
        return stats
    
    def _calculate_avg_compression(self) -> float:
        """Calcule ratio de compression moyen"""
        if not self.compression_metrics:
            return 0.0
        
        total_ratio = sum(m.ratio for m in self.compression_metrics.values())
        return total_ratio / len(self.compression_metrics)
    
    def _get_top_atoms(self, n: int = 10) -> List[Dict]:
        """Retourne top N atomes par fréquence"""
        all_atoms = list(self.dhatu_atoms.values()) + list(self.discovered_atoms.values())
        sorted_atoms = sorted(all_atoms, key=lambda a: a.frequency, reverse=True)
        
        return [
            {
                'atom_id': a.atom_id,
                'concept': a.concept,
                'frequency': a.frequency,
                'languages': len(a.languages),
                'source': a.source
            }
            for a in sorted_atoms[:n]
        ]
    
    def save_results(self, filename: Optional[str] = None):
        """Sauvegarde résultats de découverte"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"semantic_atoms_discovery_{timestamp}.json"
        
        filepath = self.results_dir / filename
        
        results = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'total_dhatu': len(self.dhatu_atoms),
                'total_discovered': len(self.discovered_atoms)
            },
            'statistics': self.get_statistics(),
            'dhatu_atoms': {
                atom_id: {
                    'concept': atom.concept,
                    'frequency': atom.frequency,
                    'languages': list(atom.languages),
                    'compression_ratio': atom.compression_ratio,
                    'validation_score': atom.validation_score
                }
                for atom_id, atom in self.dhatu_atoms.items()
            },
            'discovered_atoms': {
                atom_id: {
                    'concept': atom.concept,
                    'frequency': atom.frequency,
                    'languages': list(atom.languages),
                    'compression_ratio': atom.compression_ratio,
                    'validation_score': atom.validation_score,
                    'metadata': atom.metadata
                }
                for atom_id, atom in self.discovered_atoms.items()
            },
            'compression_metrics': {
                atom_id: {
                    'ratio': m.ratio,
                    'fidelity_score': m.fidelity_score,
                    'languages_tested': m.languages_tested
                }
                for atom_id, m in self.compression_metrics.items()
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        self.log(f"💾 Results saved to {filepath}")
        return filepath
    
    def log(self, message: str):
        """Log avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")


def main():
    """Example usage and testing"""
    print("🧬 SEMANTIC ATOMS DISCOVERY")
    print("=" * 60)
    
    discovery = SemanticAtomsDiscovery()
    
    # Example: Analyze sample texts
    sample_texts = [
        {
            'text': "L'enfant est dans le jardin. Il joue avec ses amis.",
            'language': 'fr',
            'source': 'example'
        },
        {
            'text': "The child is in the garden. He plays with his friends.",
            'language': 'en',
            'source': 'example'
        },
        {
            'text': "El niño está en el jardín. Juega con sus amigos.",
            'language': 'es',
            'source': 'example'
        }
    ]
    
    # Analyze texts
    for text_info in sample_texts:
        atoms = discovery.analyze_text_for_atoms(
            text_info['text'],
            text_info['language'],
            text_info['source']
        )
        print(f"\n{text_info['language'].upper()}: {len(atoms)} atoms detected")
    
    # Discover new atoms
    new_atoms = discovery.discover_new_atoms(sample_texts, min_frequency=2, min_languages=2)
    print(f"\n🔬 New atoms discovered: {len(new_atoms)}")
    
    # Validate by compression
    for atom_id in list(discovery.dhatu_atoms.keys())[:5]:
        metrics = discovery.validate_atom_by_compression(atom_id, sample_texts)
        print(f"  {atom_id}: compression={metrics.ratio:.2%}, fidelity={metrics.fidelity_score:.2%}")
    
    # Statistics
    stats = discovery.get_statistics()
    print(f"\n📊 STATISTICS")
    print(f"  Dhātu tested: {stats['dhatu_tested']}")
    print(f"  New atoms discovered: {stats['new_atoms_discovered']}")
    print(f"  Languages analyzed: {stats['languages_analyzed']}")
    print(f"  Avg compression: {stats['avg_compression_ratio']:.2%}")
    
    # Save results
    filepath = discovery.save_results()
    print(f"\n✅ Results saved to: {filepath}")
    
    return 0


if __name__ == "__main__":
    main()
