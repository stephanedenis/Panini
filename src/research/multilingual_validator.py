#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multilingual Validator - Validation Multilingue des Atomes Sémantiques
========================================================================

Validation des atomes sémantiques par convergence multilingue.
Divergences = indices de structure fine à explorer.

Concepts clés:
- Corpus parallèles (même contenu, langues multiples)
- Convergence multilangue = validation atome
- Divergences = indices structure fine
"""

import json
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict, Counter
from dataclasses import dataclass, field
from datetime import datetime
import math


@dataclass
class ParallelCorpus:
    """Corpus parallèle - même contenu en plusieurs langues"""
    corpus_id: str
    title: str
    languages: Dict[str, str]  # lang_code -> text
    source: str
    metadata: Dict = field(default_factory=dict)


@dataclass
class ConvergenceMetrics:
    """Métriques de convergence multilingue pour un atome"""
    atom_id: str
    languages_present: Set[str]
    convergence_score: float  # 0-1, 1 = présent dans toutes langues
    frequency_variance: float  # Variance de fréquence entre langues
    is_universal: bool
    divergences: List[str] = field(default_factory=list)


@dataclass
class DivergenceIndicator:
    """Indicateur de divergence linguistique"""
    corpus_id: str
    atom_id: str
    languages_with: Set[str]
    languages_without: Set[str]
    potential_fine_structure: str
    confidence: float


class MultilingualValidator:
    """Validateur multilingue pour atomes sémantiques"""
    
    def __init__(self, results_dir: Optional[Path] = None):
        """
        Initialisation du validateur multilingue
        
        Args:
            results_dir: Répertoire pour sauvegarder les résultats
        """
        self.results_dir = results_dir or Path('/home/runner/work/Panini/Panini/results/multilingual_validation')
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # Corpus parallèles chargés
        self.parallel_corpora = {}
        
        # Résultats de convergence par atome
        self.convergence_results = {}
        
        # Divergences détectées
        self.divergences = []
        
        # Langues supportées
        self.supported_languages = {
            'fr': 'Français',
            'en': 'English',
            'es': 'Español',
            'de': 'Deutsch',
            'it': 'Italiano',
            'pt': 'Português',
            'ar': 'العربية',
            'zh': '中文',
            'ja': '日本語',
            'ru': 'Русский',
            'hi': 'हिन्दी',
            'sa': 'संस्कृत'
        }
        
        # Statistiques
        self.stats = {
            'corpora_analyzed': 0,
            'languages_tested': set(),
            'atoms_validated': set(),
            'divergences_found': 0
        }
        
        self.log("🌍 Multilingual Validator initialized")
    
    def add_parallel_corpus(self, corpus_id: str, title: str, 
                           language_texts: Dict[str, str],
                           source: str = 'unknown',
                           metadata: Optional[Dict] = None) -> ParallelCorpus:
        """
        Ajoute un corpus parallèle
        
        Args:
            corpus_id: Identifiant unique du corpus
            title: Titre du corpus
            language_texts: Dict {lang_code: text}
            source: Source du corpus
            metadata: Métadonnées additionnelles
            
        Returns:
            ParallelCorpus créé
        """
        corpus = ParallelCorpus(
            corpus_id=corpus_id,
            title=title,
            languages=language_texts,
            source=source,
            metadata=metadata or {}
        )
        
        self.parallel_corpora[corpus_id] = corpus
        self.stats['corpora_analyzed'] += 1
        self.stats['languages_tested'].update(language_texts.keys())
        
        self.log(f"📚 Added parallel corpus '{title}' ({len(language_texts)} languages)")
        
        return corpus
    
    def validate_atom_convergence(self, atom_id: str, 
                                  atom_patterns: Dict[str, List[str]],
                                  min_convergence: float = 0.7) -> ConvergenceMetrics:
        """
        Valide la convergence multilingue d'un atome
        
        Args:
            atom_id: ID de l'atome à valider
            atom_patterns: Dict {lang_code: [patterns]}
            min_convergence: Score minimum pour considérer universel (0-1)
            
        Returns:
            Métriques de convergence
        """
        languages_present = set()
        frequencies_by_lang = {}
        total_languages = len(self.stats['languages_tested'])
        
        # Analyser chaque corpus parallèle
        for corpus in self.parallel_corpora.values():
            for lang, text in corpus.languages.items():
                if lang in atom_patterns:
                    # Chercher patterns de l'atome dans le texte
                    count = 0
                    for pattern in atom_patterns[lang]:
                        count += text.lower().count(pattern.lower())
                    
                    if count > 0:
                        languages_present.add(lang)
                        if lang not in frequencies_by_lang:
                            frequencies_by_lang[lang] = []
                        frequencies_by_lang[lang].append(count)
        
        # Calculer score de convergence
        if total_languages > 0:
            convergence_score = len(languages_present) / total_languages
        else:
            convergence_score = 0.0
        
        # Calculer variance de fréquence
        all_freqs = [sum(freqs) for freqs in frequencies_by_lang.values()]
        if all_freqs:
            mean_freq = sum(all_freqs) / len(all_freqs)
            variance = sum((f - mean_freq) ** 2 for f in all_freqs) / len(all_freqs)
            frequency_variance = math.sqrt(variance) / mean_freq if mean_freq > 0 else 0
        else:
            frequency_variance = 0.0
        
        # Déterminer si universel
        is_universal = convergence_score >= min_convergence
        
        # Identifier divergences
        divergences = []
        if convergence_score < 1.0 and convergence_score > 0:
            missing_langs = self.stats['languages_tested'] - languages_present
            if missing_langs:
                divergences.append(
                    f"Missing in: {', '.join(sorted(missing_langs))}"
                )
        
        metrics = ConvergenceMetrics(
            atom_id=atom_id,
            languages_present=languages_present,
            convergence_score=convergence_score,
            frequency_variance=frequency_variance,
            is_universal=is_universal,
            divergences=divergences
        )
        
        self.convergence_results[atom_id] = metrics
        if is_universal:
            self.stats['atoms_validated'].add(atom_id)
        
        return metrics
    
    def detect_divergences(self, atom_id: str, 
                          atom_patterns: Dict[str, List[str]],
                          min_confidence: float = 0.6) -> List[DivergenceIndicator]:
        """
        Détecte les divergences linguistiques pour identifier structure fine
        
        Args:
            atom_id: ID de l'atome
            atom_patterns: Patterns par langue
            min_confidence: Confiance minimum pour divergence
            
        Returns:
            Liste des divergences détectées
        """
        divergences = []
        
        for corpus in self.parallel_corpora.values():
            languages_with = set()
            languages_without = set()
            
            for lang, text in corpus.languages.items():
                if lang not in atom_patterns:
                    continue
                    
                has_atom = False
                for pattern in atom_patterns[lang]:
                    if pattern.lower() in text.lower():
                        has_atom = True
                        break
                
                if has_atom:
                    languages_with.add(lang)
                else:
                    languages_without.add(lang)
            
            # Si divergence significative
            if languages_with and languages_without:
                total = len(languages_with) + len(languages_without)
                confidence = abs(len(languages_with) - len(languages_without)) / total
                
                if confidence >= min_confidence:
                    # Hypothèse de structure fine
                    if len(languages_with) < len(languages_without):
                        potential_structure = f"Culture-specific concept (present in {', '.join(languages_with)})"
                    else:
                        potential_structure = f"Universal with exceptions (absent in {', '.join(languages_without)})"
                    
                    divergence = DivergenceIndicator(
                        corpus_id=corpus.corpus_id,
                        atom_id=atom_id,
                        languages_with=languages_with,
                        languages_without=languages_without,
                        potential_fine_structure=potential_structure,
                        confidence=confidence
                    )
                    
                    divergences.append(divergence)
                    self.stats['divergences_found'] += 1
        
        self.divergences.extend(divergences)
        return divergences
    
    def validate_corpus_consistency(self, corpus_id: str,
                                   atom_patterns_dict: Dict[str, Dict[str, List[str]]]) -> Dict:
        """
        Valide la cohérence d'un corpus parallèle pour plusieurs atomes
        
        Args:
            corpus_id: ID du corpus
            atom_patterns_dict: Dict {atom_id: {lang: [patterns]}}
            
        Returns:
            Rapport de cohérence
        """
        if corpus_id not in self.parallel_corpora:
            self.log(f"⚠️  Corpus {corpus_id} not found")
            return {}
        
        corpus = self.parallel_corpora[corpus_id]
        consistency_report = {
            'corpus_id': corpus_id,
            'title': corpus.title,
            'languages': list(corpus.languages.keys()),
            'atoms_analyzed': len(atom_patterns_dict),
            'atom_results': {}
        }
        
        for atom_id, patterns in atom_patterns_dict.items():
            atom_consistency = {
                'present_in': [],
                'absent_in': [],
                'consistency_score': 0.0
            }
            
            for lang in corpus.languages.keys():
                if lang not in patterns:
                    continue
                
                text = corpus.languages[lang]
                is_present = any(
                    pattern.lower() in text.lower() 
                    for pattern in patterns[lang]
                )
                
                if is_present:
                    atom_consistency['present_in'].append(lang)
                else:
                    atom_consistency['absent_in'].append(lang)
            
            total_langs = len(atom_consistency['present_in']) + len(atom_consistency['absent_in'])
            if total_langs > 0:
                atom_consistency['consistency_score'] = len(atom_consistency['present_in']) / total_langs
            
            consistency_report['atom_results'][atom_id] = atom_consistency
        
        return consistency_report
    
    def generate_validation_report(self, min_languages: int = 3) -> Dict:
        """
        Génère rapport de validation multilingue
        
        Args:
            min_languages: Nombre minimum de langues pour validation
            
        Returns:
            Rapport complet
        """
        report = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'corpora_count': len(self.parallel_corpora),
                'languages_tested': list(self.stats['languages_tested']),
                'min_languages': min_languages
            },
            'statistics': {
                'total_corpora': self.stats['corpora_analyzed'],
                'total_languages': len(self.stats['languages_tested']),
                'atoms_validated': len(self.stats['atoms_validated']),
                'divergences_found': self.stats['divergences_found']
            },
            'convergence_results': {},
            'universal_atoms': [],
            'divergent_atoms': [],
            'divergences': []
        }
        
        # Résultats de convergence
        for atom_id, metrics in self.convergence_results.items():
            report['convergence_results'][atom_id] = {
                'languages_present': list(metrics.languages_present),
                'convergence_score': metrics.convergence_score,
                'frequency_variance': metrics.frequency_variance,
                'is_universal': metrics.is_universal,
                'divergences': metrics.divergences
            }
            
            if metrics.is_universal and len(metrics.languages_present) >= min_languages:
                report['universal_atoms'].append({
                    'atom_id': atom_id,
                    'languages': list(metrics.languages_present),
                    'score': metrics.convergence_score
                })
            elif metrics.divergences:
                report['divergent_atoms'].append({
                    'atom_id': atom_id,
                    'languages': list(metrics.languages_present),
                    'score': metrics.convergence_score,
                    'divergences': metrics.divergences
                })
        
        # Divergences détaillées
        for div in self.divergences:
            report['divergences'].append({
                'corpus_id': div.corpus_id,
                'atom_id': div.atom_id,
                'languages_with': list(div.languages_with),
                'languages_without': list(div.languages_without),
                'structure_hypothesis': div.potential_fine_structure,
                'confidence': div.confidence
            })
        
        return report
    
    def save_results(self, filename: Optional[str] = None):
        """Sauvegarde résultats de validation"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"multilingual_validation_{timestamp}.json"
        
        filepath = self.results_dir / filename
        
        report = self.generate_validation_report()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.log(f"💾 Results saved to {filepath}")
        return filepath
    
    def log(self, message: str):
        """Log avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")


def main():
    """Example usage and testing"""
    print("🌍 MULTILINGUAL VALIDATOR")
    print("=" * 60)
    
    validator = MultilingualValidator()
    
    # Example: Add parallel corpus
    corpus1 = validator.add_parallel_corpus(
        corpus_id='little_prince_ch1',
        title='Le Petit Prince - Chapitre 1',
        language_texts={
            'fr': "Lorsque j'avais six ans j'ai vu, une fois, une magnifique image.",
            'en': "Once when I was six years old I saw a magnificent picture.",
            'es': "Una vez, cuando tenía seis años, vi una magnífica imagen."
        },
        source='Antoine de Saint-Exupéry'
    )
    
    corpus2 = validator.add_parallel_corpus(
        corpus_id='declaration_droits',
        title='Déclaration Universelle des Droits de l\'Homme - Article 1',
        language_texts={
            'fr': "Tous les êtres humains naissent libres et égaux en dignité et en droits.",
            'en': "All human beings are born free and equal in dignity and rights.",
            'es': "Todos los seres humanos nacen libres e iguales en dignidad y derechos.",
            'de': "Alle Menschen sind frei und gleich an Würde und Rechten geboren."
        },
        source='ONU 1948'
    )
    
    # Example: Validate atom convergence
    atom_patterns = {
        'fr': ['être', 'naissent', 'sont'],
        'en': ['be', 'are', 'born'],
        'es': ['ser', 'son', 'nacen'],
        'de': ['sind', 'geboren']
    }
    
    metrics = validator.validate_atom_convergence('EXIST', atom_patterns)
    print(f"\n✅ EXIST atom validation:")
    print(f"  Languages present: {', '.join(metrics.languages_present)}")
    print(f"  Convergence score: {metrics.convergence_score:.2%}")
    print(f"  Is universal: {metrics.is_universal}")
    
    # Detect divergences
    divergences = validator.detect_divergences('EXIST', atom_patterns)
    print(f"\n🔍 Divergences detected: {len(divergences)}")
    
    # Generate report
    report = validator.generate_validation_report()
    print(f"\n📊 VALIDATION REPORT")
    print(f"  Total corpora: {report['statistics']['total_corpora']}")
    print(f"  Languages tested: {report['statistics']['total_languages']}")
    print(f"  Atoms validated: {report['statistics']['atoms_validated']}")
    print(f"  Universal atoms: {len(report['universal_atoms'])}")
    
    # Save results
    filepath = validator.save_results()
    print(f"\n✅ Results saved to: {filepath}")
    
    return 0


if __name__ == "__main__":
    main()
