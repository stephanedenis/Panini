#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example Integration - Semantic Atoms Research Pipeline
========================================================

Demonstrates integrated usage of the four core research modules:
1. SemanticAtomsDiscovery
2. MultilingualValidator  
3. TranslatorMetadataDB
4. DhatuEvolutionTracker

This example shows a complete research workflow from atom discovery
to validation and tracking.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.research.semantic_atoms_discovery import SemanticAtomsDiscovery
from src.research.multilingual_validator import MultilingualValidator
from src.research.translator_metadata_db import TranslatorMetadataDB
from src.research.dhatu_evolution_tracker import DhatuEvolutionTracker


def run_complete_research_pipeline():
    """
    Complete research pipeline example
    """
    print("=" * 70)
    print("🧬 SEMANTIC ATOMS RESEARCH PIPELINE - INTEGRATED EXAMPLE")
    print("=" * 70)
    
    # ========================================================================
    # PHASE 1: SEMANTIC ATOMS DISCOVERY
    # ========================================================================
    print("\n" + "=" * 70)
    print("PHASE 1: Semantic Atoms Discovery")
    print("=" * 70)
    
    discovery = SemanticAtomsDiscovery()
    
    # Sample multilingual corpus
    sample_corpus = [
        {
            'text': "L'enfant joue dans le jardin avec ses amis. Il aime courir et sauter.",
            'language': 'fr',
            'source': 'children_stories',
            'translator': 'translator_001'
        },
        {
            'text': "The child plays in the garden with his friends. He loves to run and jump.",
            'language': 'en',
            'source': 'children_stories',
            'translator': 'translator_002'
        },
        {
            'text': "El niño juega en el jardín con sus amigos. Le encanta correr y saltar.",
            'language': 'es',
            'source': 'children_stories',
            'translator': 'translator_003'
        },
        {
            'text': "Das Kind spielt im Garten mit seinen Freunden. Es liebt zu laufen und zu springen.",
            'language': 'de',
            'source': 'children_stories',
            'translator': 'translator_004'
        },
        {
            'text': "Il bambino gioca nel giardino con i suoi amici. Ama correre e saltare.",
            'language': 'it',
            'source': 'children_stories',
            'translator': 'translator_005'
        }
    ]
    
    # Analyze texts for atoms
    print("\n📊 Analyzing multilingual corpus...")
    for text_info in sample_corpus:
        atoms = discovery.analyze_text_for_atoms(
            text_info['text'],
            text_info['language'],
            text_info['source']
        )
        print(f"  {text_info['language'].upper()}: {sum(atoms.values())} atom occurrences")
    
    # Discover new atoms
    print("\n🔬 Discovering new semantic atoms...")
    new_atoms = discovery.discover_new_atoms(sample_corpus, min_frequency=3, min_languages=3)
    print(f"  Discovered {len(new_atoms)} new atoms")
    for atom in new_atoms[:5]:  # Show first 5
        print(f"    - {atom.atom_id}: {atom.concept} ({len(atom.languages)} languages)")
    
    # Validate by compression
    print("\n📦 Validating atoms through compression...")
    validation_results = {}
    for atom_id in ['EXIST', 'RELATE', 'ACT', 'EMOT']:
        metrics = discovery.validate_atom_by_compression(atom_id, sample_corpus)
        validation_results[atom_id] = metrics
        print(f"  {atom_id}: ratio={metrics.ratio:.2%}, fidelity={metrics.fidelity_score:.2%}")
    
    discovery_stats = discovery.get_statistics()
    print(f"\n✅ Discovery complete:")
    print(f"  - Dhātu tested: {discovery_stats['dhatu_tested']}")
    print(f"  - New atoms: {discovery_stats['new_atoms_discovered']}")
    print(f"  - Languages: {discovery_stats['languages_analyzed']}")
    
    # ========================================================================
    # PHASE 2: MULTILINGUAL VALIDATION
    # ========================================================================
    print("\n" + "=" * 70)
    print("PHASE 2: Multilingual Validation")
    print("=" * 70)
    
    validator = MultilingualValidator()
    
    # Add parallel corpus
    print("\n📚 Adding parallel corpus...")
    validator.add_parallel_corpus(
        corpus_id='children_story_001',
        title='Child Playing in Garden',
        language_texts={
            info['language']: info['text'] 
            for info in sample_corpus
        },
        source='children_stories'
    )
    
    # Validate atoms with multilingual patterns
    print("\n✅ Validating atom convergence...")
    
    # Example patterns for EXIST atom
    exist_patterns = {
        'fr': ['être', 'est', 'sont'],
        'en': ['be', 'is', 'are'],
        'es': ['ser', 'estar', 'es', 'son'],
        'de': ['sein', 'ist', 'sind'],
        'it': ['essere', 'è', 'sono']
    }
    
    exist_metrics = validator.validate_atom_convergence('EXIST', exist_patterns)
    print(f"  EXIST: {len(exist_metrics.languages_present)} languages, score={exist_metrics.convergence_score:.2%}")
    
    # Detect divergences
    print("\n🔍 Detecting linguistic divergences...")
    divergences = validator.detect_divergences('EXIST', exist_patterns)
    print(f"  Found {len(divergences)} divergence indicators")
    
    validation_report = validator.generate_validation_report()
    print(f"\n✅ Validation complete:")
    print(f"  - Corpora: {validation_report['statistics']['total_corpora']}")
    print(f"  - Languages: {validation_report['statistics']['total_languages']}")
    print(f"  - Validated atoms: {validation_report['statistics']['atoms_validated']}")
    
    # ========================================================================
    # PHASE 3: TRANSLATOR METADATA DATABASE
    # ========================================================================
    print("\n" + "=" * 70)
    print("PHASE 3: Translator Metadata Database")
    print("=" * 70)
    
    translator_db = TranslatorMetadataDB()
    
    # Add translators
    print("\n👥 Adding translators to database...")
    translators = [
        {
            'id': 'translator_001',
            'name': 'Marie Dupont',
            'languages': ['fr', 'en'],
            'specializations': ['children_literature', 'education']
        },
        {
            'id': 'translator_002',
            'name': 'John Smith',
            'languages': ['en', 'fr'],
            'specializations': ['children_literature']
        },
        {
            'id': 'translator_003',
            'name': 'Carlos García',
            'languages': ['es', 'en'],
            'specializations': ['children_literature', 'poetry']
        },
        {
            'id': 'translator_004',
            'name': 'Hans Müller',
            'languages': ['de', 'en'],
            'specializations': ['children_literature']
        },
        {
            'id': 'translator_005',
            'name': 'Giovanni Rossi',
            'languages': ['it', 'en'],
            'specializations': ['children_literature']
        }
    ]
    
    for t in translators:
        translator_db.add_translator(
            translator_id=t['id'],
            name=t['name'],
            languages=t['languages'],
            specializations=t['specializations']
        )
    
    # Add translation works
    print("\n📖 Adding translation works...")
    for i, text_info in enumerate(sample_corpus):
        translator_db.add_translation_work(
            work_id=f"work_{i+1:03d}",
            title=f"Children Story - {text_info['language'].upper()}",
            translator_id=text_info['translator'],
            source_language='original',
            target_language=text_info['language'],
            domain='children_literature',
            quality_score=0.90
        )
    
    # Analyze translator bias
    print("\n📊 Analyzing translator bias...")
    bias_report = translator_db.analyze_translator_bias('translator_001')
    print(f"  Translator: translator_001")
    print(f"  Works: {bias_report['total_works']}")
    print(f"  Bias indicators: {len(bias_report['bias_indicators'])}")
    
    db_stats = translator_db.get_statistics()
    print(f"\n✅ Database complete:")
    print(f"  - Translators: {db_stats['total_translators']}")
    print(f"  - Works: {db_stats['total_works']}")
    print(f"  - Languages: {db_stats['languages_covered']}")
    
    # ========================================================================
    # PHASE 4: DHĀTU EVOLUTION TRACKING
    # ========================================================================
    print("\n" + "=" * 70)
    print("PHASE 4: Dhātu Evolution Tracking")
    print("=" * 70)
    
    tracker = DhatuEvolutionTracker()
    
    # Create initial dhātus
    print("\n✨ Creating initial dhātu set...")
    base_dhatus = [
        ('EXIST', 'être/existence'),
        ('RELATE', 'relations/spatial'),
        ('ACT', 'action/mouvement'),
        ('EMOT', 'émotions/affect'),
        ('COMM', 'communication')
    ]
    
    for dhatu_id, concept in base_dhatus:
        tracker.create_dhatu(dhatu_id, concept, source='dhatu')
    
    # Update with discovery results
    print("\n📝 Updating dhātus with discovery data...")
    for atom_id, atom in discovery.dhatu_atoms.items():
        if atom.frequency > 0:
            tracker.update_dhatu(
                atom_id,
                frequency=atom.frequency,
                languages=atom.languages,
                compression_ratio=atom.compression_ratio,
                validation_score=atom.validation_score
            )
    
    # Validate dhātus
    print("\n✅ Validating dhātus...")
    for atom_id in ['EXIST', 'RELATE', 'ACT']:
        tracker.validate_dhatu(
            atom_id,
            tested_languages=['fr', 'en', 'es', 'de', 'it'],
            compression_tests=5,
            avg_compression_ratio=validation_results.get(atom_id, None).ratio if atom_id in validation_results else 0.2,
            avg_fidelity_score=validation_results.get(atom_id, None).fidelity_score if atom_id in validation_results else 0.85,
            convergence_score=0.88
        )
    
    # Add discovered atoms
    print("\n🔬 Adding discovered atoms...")
    for atom in new_atoms[:3]:  # Add first 3 new atoms
        tracker.create_dhatu(atom.atom_id, atom.concept, source='discovered')
        tracker.update_dhatu(
            atom.atom_id,
            frequency=atom.frequency,
            languages=atom.languages
        )
    
    tracker_stats = tracker.get_statistics()
    print(f"\n✅ Evolution tracking complete:")
    print(f"  - Total created: {tracker_stats['total_dhatus_created']}")
    print(f"  - Active: {tracker_stats['total_dhatus_active']}")
    print(f"  - Validated: {tracker_stats['total_dhatus_validated']}")
    print(f"  - Validation rate: {tracker_stats['validation_rate']:.2%}")
    
    # ========================================================================
    # FINAL REPORT
    # ========================================================================
    print("\n" + "=" * 70)
    print("FINAL INTEGRATED REPORT")
    print("=" * 70)
    
    print("\n📊 SUCCESS METRICS PROGRESS:")
    print(f"  ✓ Dhātu tested: {discovery_stats['dhatu_tested']} / 50+ target")
    print(f"  ✓ New atoms discovered: {discovery_stats['new_atoms_discovered']} / 20+ target")
    print(f"  ✓ Languages analyzed: {discovery_stats['languages_analyzed']} / 10+ target")
    print(f"  ✓ Translators in database: {db_stats['total_translators']} / 100+ target")
    print(f"  ✓ Compression validated: {len(validation_results)} atoms tested")
    
    print("\n💾 Saving all results...")
    discovery_file = discovery.save_results('integrated_discovery.json')
    validation_file = validator.save_results('integrated_validation.json')
    translator_file = translator_db.export_to_json()
    tracker_file = tracker.save_results('integrated_evolution.json')
    
    print(f"\n✅ All results saved:")
    print(f"  - Discovery: {discovery_file}")
    print(f"  - Validation: {validation_file}")
    print(f"  - Translators: {translator_file}")
    print(f"  - Evolution: {tracker_file}")
    
    print("\n" + "=" * 70)
    print("✨ INTEGRATED RESEARCH PIPELINE COMPLETE!")
    print("=" * 70)
    
    return {
        'discovery': discovery_stats,
        'validation': validation_report['statistics'],
        'translators': db_stats,
        'evolution': tracker_stats
    }


if __name__ == "__main__":
    results = run_complete_research_pipeline()
    print("\n🎉 Pipeline execution successful!")
    print(f"\nKey Results:")
    print(f"  - Languages analyzed: {results['discovery']['languages_analyzed']}")
    print(f"  - Atoms validated: {results['validation']['atoms_validated']}")
    print(f"  - Active dhātus: {results['evolution']['total_dhatus_active']}")
