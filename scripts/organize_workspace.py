#!/usr/bin/env python3
"""
Utilitaire pour organiser automatiquement l'espace de travail
selon des règles catégorielles intelligentes
"""

import os
import shutil
import glob
from pathlib import Path

def organize_workspace():
    """Organise l'espace de travail selon des catégories logiques"""
    
    # Définition des règles de catégorisation
    categories = {
        'src/analysis': [
            '*analyzer*.py', '*analyse*.py', '*reconstitution*.py',
            '*validation*.py', '*validator*.py', '*verificateur*.py',
            'detailed_failure_analyzer.py', 'synthesis_validator.py',
            'contraintes_operateurs_naires.py', 'recherche_sens_optimaux_naires.py',
            'resolution_polysemie_contextuelle.py', 'validateur_concepts_interactif.py',
            'validation_finale_autonomie.py', 'protocole_validation_reconstitution.py'
        ],
        
        'src/corpus': [
            '*corpus*.py', '*collection*.py', '*integrateur*.py',
            'integrateur_corpus_complet.py', 'integrateur_molecules_ultimate.py',
            'lance_collection_multilingue.py', 'launch_corpus_collection.py',
            'extension_cross_linguistique.py', 'tokenisation_complete_contextuelle.py',
            'universal_atoms_extractor.py', 'molecular_pattern_builder.py'
        ],
        
        'src/research': [
            '*autonome*.py', '*pipeline*.py', '*orchestrateur*.py',
            'pipeline_hybride_v3_final.py', 'pipeline_v5_ultimate_100_pourcent.py',
            'pipeline_simulator.py', 'orchestrateur_pipeline_iteratif.py',
            'analyse_autonome_projet.py', 'MISSION_FINALE_v4_ultimate.py',
            'demarche_complete_detaillee.py', 'implementation_extensions_prioritaires.py'
        ],
        
        'src/utils': [
            '*optimiseur*.py', '*monitoring*.py', '*diagnostic*.py',
            '*gestionnaire*.py', '*moniteur*.py', '*moteur*.py',
            'generateur_optimiseur_performance.py', 'gestionnaire_arriere_plan.py',
            'diagnostic_etat_systeme.py', 'monitoring_rapide.py',
            'moniteur_progression_pipeline.py', 'moteur_recherche_accelere.py',
            'moteur_turbo_recherche.py', 'nettoyage_simple.py', 'nettoyer_workspace.py',
            'simplificateur_commandes.py', 'tester_configuration_simplification.py'
        ],
        
        'src/core': [
            '*systeme*.py', '*lanceur*.py', '*gpu*.py', '*accelerateur*.py',
            'accelerateur_systeme.py', 'lanceur_systeme_panini.py',
            'gpu_accelerated_panini.py', 'gpu_infrastructure_summary.py',
            'panini_gpu_integrator.py', 'panini_gpu_optimizer.py',
            'panini_high_performance_optimizer.py', 'systeme_marqueurs_onomastiques.py',
            'rx480_auto_session.py', 'rx480_integrated_launcher.py', 'rx480_system_monitor.py',
            'diagnostic_liberation_gpu.py'
        ],
        
        'scripts': [
            '*lancer*.py', '*redemarrer*.py', '*arreter*.py', '*stop*.py',
            'arreter_tout.py', 'redemarrer_systeme.py', 'restaurer_et_lancer.py',
            'lancer_traitement_reel.py', 'lance_roquette_turbo.py',
            'stop_processes.py', 'verificateur_statut_systemes.py',
            'verifier_config_vscode.py', 'verifier_performance.py'
        ],
        
        'legacy': [
            '*protection*.py', '*tumbleweed*.py', '*test*.py',
            'simple_protected_system.py', 'tumbleweed_process_protector.py',
            'tumbleweed_protection_analyzer.py', 'tumbleweed_protection_bypass.py',
            'test_protection_stress.py', 'test_surveillance_autonome.py',
            'testeur_fonctions_lexicales_etendu.py'
        ]
    }
    
    base_path = '/home/stephane/GitHub/PaniniFS-Research'
    moved_files = {}
    
    print("🗂️  ORGANISATION AUTOMATIQUE DE L'ESPACE DE TRAVAIL")
    print("=" * 55)
    
    for category, patterns in categories.items():
        category_path = os.path.join(base_path, category)
        os.makedirs(category_path, exist_ok=True)
        moved_files[category] = []
        
        for pattern in patterns:
            files = glob.glob(os.path.join(base_path, pattern))
            for file_path in files:
                if os.path.isfile(file_path):
                    filename = os.path.basename(file_path)
                    destination = os.path.join(category_path, filename)
                    
                    try:
                        shutil.move(file_path, destination)
                        moved_files[category].append(filename)
                        print(f"📁 {filename} → {category}")
                    except Exception as e:
                        print(f"❌ Erreur avec {filename}: {e}")
    
    # Déplacer les fichiers data
    print("\n📊 DÉPLACEMENT DES FICHIERS DE DONNÉES")
    print("=" * 40)
    
    data_patterns = ['*.json', '*.log', '*.md']
    data_path = os.path.join(base_path, 'data')
    os.makedirs(data_path, exist_ok=True)
    
    for pattern in data_patterns:
        files = glob.glob(os.path.join(base_path, pattern))
        for file_path in files:
            if os.path.isfile(file_path):
                filename = os.path.basename(file_path)
                # Garder README.md dans la racine
                if filename.upper() == 'README.MD':
                    continue
                    
                destination = os.path.join(data_path, filename)
                try:
                    shutil.move(file_path, destination)
                    print(f"📊 {filename} → data/")
                except Exception as e:
                    print(f"❌ Erreur avec {filename}: {e}")
    
    # Résumé
    print("\n📋 RÉSUMÉ DE L'ORGANISATION")
    print("=" * 30)
    
    total_moved = 0
    for category, files in moved_files.items():
        count = len(files)
        total_moved += count
        if count > 0:
            print(f"{category}: {count} fichiers")
    
    print(f"\n✅ Total: {total_moved} fichiers déplacés")
    
    # Vérifier ce qui reste
    remaining_py = glob.glob(os.path.join(base_path, '*.py'))
    if remaining_py:
        print(f"\n⚠️  Fichiers Python restants dans la racine: {len(remaining_py)}")
        for file_path in remaining_py[:5]:  # Montrer les 5 premiers
            print(f"   - {os.path.basename(file_path)}")
        if len(remaining_py) > 5:
            print(f"   ... et {len(remaining_py) - 5} autres")

if __name__ == "__main__":
    organize_workspace()