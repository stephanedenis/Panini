#!/usr/bin/env python3
"""
Script de génération des notebooks Google Colab Pro
pour recherches linguistiques PaniniFS accélérées
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire src au PYTHONPATH
project_root = os.path.dirname(os.path.dirname(__file__))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from cloud.colab_integrator import ColabIntegrator


def main():
    """Lance la génération des notebooks Colab"""
    
    print("🚀 GÉNÉRATION NOTEBOOKS GOOGLE COLAB PRO")
    print("=" * 50)
    print("Intégration pour recherches linguistiques accélérées")
    print()
    
    try:
        integrator = ColabIntegrator()
        
        # Génération des notebooks
        print("📓 Création des notebooks...")
        
        dhatu_nb = integrator.create_dhatu_analysis_notebook()
        print(f"✅ Analyse Dhātu: {os.path.basename(dhatu_nb)}")
        
        corpus_nb = integrator.create_corpus_processing_notebook()
        print(f"✅ Corpus Multilingue: {os.path.basename(corpus_nb)}")
        
        perf_nb = integrator.create_performance_benchmark_notebook()
        print(f"✅ Benchmark Performance: {os.path.basename(perf_nb)}")
        
        # Guide d'utilisation
        guide = integrator.generate_colab_integration_guide()
        print(f"📚 Guide d'intégration: {os.path.basename(guide)}")
        
        print(f"\n🎯 NOTEBOOKS GÉNÉRÉS AVEC SUCCÈS!")
        print(f"📁 Emplacement: {integrator.colab_notebooks_dir}")
        print()
        print("🔗 ÉTAPES SUIVANTES:")
        print("1. Uploader les fichiers .ipynb vers Google Colab")
        print("2. Configurer Runtime → GPU/TPU")
        print("3. Exécuter pour analyses accélérées")
        print()
        print("💡 AVANTAGES COLAB PRO:")
        print("- GPU Tesla T4/P4 gratuit")
        print("- RAM 25GB (vs 8GB gratuit)")
        print("- Sessions 24h persistantes")
        print("- Accélération 10-100x vs CPU")
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)