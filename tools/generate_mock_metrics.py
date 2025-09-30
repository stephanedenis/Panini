#!/usr/bin/env python3
"""
Générateur de données de métriques pour test du dashboard
Crée des fichiers JSON avec des données simulées réalistes
"""

import json
from pathlib import Path
from datetime import datetime
import random

def generate_synthesis_validation_data(output_dir):
    """Génère données de validation PaniniFS"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    data = {
        "timestamp": datetime.now().isoformat(),
        "test_results": [
            {
                "format": "text",
                "compression_ratio": 3.45,
                "fidelity": 0.98
            },
            {
                "format": "json",
                "compression_ratio": 4.12,
                "fidelity": 0.99
            },
            {
                "format": "markdown",
                "compression_ratio": 2.87,
                "fidelity": 0.97
            }
        ],
        "overall_fidelity": 0.98,
        "processing_times": {
            "decomposition_ms": 125,
            "recomposition_ms": 89
        },
        "total_texts_processed": 47
    }
    
    output_file = output_dir / f"synthesis_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Créé: {output_file}")
    return output_file


def generate_atoms_analysis_data(output_dir):
    """Génère données d'analyse d'atomes"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    data = {
        "timestamp": datetime.now().isoformat(),
        "atom_counts": {
            "phonetic": 1247,
            "morpheme": 856,
            "syntactic": 423,
            "semantic": 612
        },
        "cross_linguistic_patterns": {
            "languages_detected": ["français", "anglais", "sanskrit", "espagnol", "mandarin"]
        },
        "compression_efficiency": {
            "phonetic": 2.34,
            "morpheme": 3.56,
            "syntactic": 2.89,
            "semantic": 4.21
        },
        "dhatu_statistics": {
            "established_count": 187,
            "newly_discovered": 23
        },
        "universality_scores": {
            "cross_linguistic_stability": 0.87,
            "semantic_preservation": 0.92
        }
    }
    
    output_file = output_dir / f"universal_atoms_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Créé: {output_file}")
    return output_file


def generate_molecular_patterns_data(output_dir):
    """Génère données de patterns moléculaires (traducteurs)"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    data = {
        "timestamp": datetime.now().isoformat(),
        "top_patterns": [
            {"pattern": "SVO_structure", "count": 342},
            {"pattern": "noun_adjective_agreement", "count": 278},
            {"pattern": "verb_tense_marking", "count": 256},
            {"pattern": "determiner_noun", "count": 201},
            {"pattern": "preposition_noun", "count": 187}
        ],
        "asymmetry_score": 0.35,
        "pattern_sources": ["corpus_fr", "corpus_en", "corpus_es"],
        "pattern_fidelity": 0.91
    }
    
    output_file = output_dir / f"molecular_patterns_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Créé: {output_file}")
    return output_file


def main():
    workspace = Path('/home/runner/work/Panini/Panini')
    
    print("🎯 Génération de données de métriques pour le dashboard...")
    print("=" * 60)
    
    # Générer données de synthèse/validation
    synthesis_dir = workspace / 'synthesis_validation_results'
    generate_synthesis_validation_data(synthesis_dir)
    
    # Générer données d'atomes
    atoms_dir = workspace / 'universal_atoms_results'
    generate_atoms_analysis_data(atoms_dir)
    
    # Générer données de patterns moléculaires
    molecules_dir = workspace / 'molecular_patterns_results'
    generate_molecular_patterns_data(molecules_dir)
    
    print("=" * 60)
    print("✅ Toutes les données de métriques ont été générées")
    print("📊 Le dashboard peut maintenant afficher des métriques réalistes")


if __name__ == '__main__':
    main()
