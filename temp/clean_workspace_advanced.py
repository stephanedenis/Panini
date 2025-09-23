#!/usr/bin/env python3
"""
Nettoyage avancé de l'espace de travail
Organise tous les dossiers et fichiers restants
"""

import os
import shutil
import glob
from pathlib import Path

def clean_workspace():
    """Nettoyage complet de l'espace de travail"""
    
    base_path = '/home/stephane/GitHub/PaniniFS-Research'
    os.chdir(base_path)
    
    print("🧹 NETTOYAGE AVANCÉ DE L'ESPACE DE TRAVAIL")
    print("=" * 50)
    
    # Créer les dossiers de destination
    destinations = {
        'results': 'data/results',
        'archives': 'data/archives', 
        'logs': 'data/logs',
        'configs': 'data/configs',
        'temp': 'temp',
        'tools': 'tools'
    }
    
    for dest in destinations.values():
        os.makedirs(dest, exist_ok=True)
    
    # Règles de déplacement par catégories
    move_rules = {
        # Résultats et données générées
        'data/results/': [
            '*_results/', '*results*/', 'autonomous_results/',
            'gpu_*_results/', 'synthesis_*_results/', 'universal_*_results/',
            'molecular_*_results/', 'pipeline_*_resultats/',
            'accelerated_research_*/', 'autonomous_research_*/',
            'coordination_global_*/', 'corpus_collection_corpus_*/',
            'ml_optimization_*/', 'turbo_*/', 'validation_metrics_*/'
        ],
        
        # Archives et corpus
        'data/archives/': [
            'archives/', 'corpus/', 'corpus_*/', 'grand_corpus_reel/',
            'dhatu_processing_output/'
        ],
        
        # Logs et monitoring
        'data/logs/': [
            'logs_*/', '*.log', 'autonomous_recovery/'
        ],
        
        # Configurations
        'data/configs/': [
            'config/', 'systemd/', '.vscode/', 'copilotage/'
        ],
        
        # Outils et utilitaires
        'tools/': [
            'panini/', 'projects/', 'tech/', 'web/', 'utilitaires/',
            'templates/', 'scripts_generes/', 'verification_system/',
            'systemes_autonomes/', 'systeme_evenementiel/', 'pipelines_dhatu/',
            'dashboards/'
        ],
        
        # Fichiers temporaires/tests
        'temp/': [
            'test_*.py', 'test_*.html', '__pycache__/', '*.pyc',
            'dashboard_data.db', 'event_system_metrics.json',
            '*_pid.txt', 'dashboard_resource_integration.js'
        ]
    }
    
    moved_count = 0
    
    # Appliquer les règles de déplacement
    for destination, patterns in move_rules.items():
        print(f"\n📁 Déplacement vers {destination}")
        dest_path = os.path.join(base_path, destination)
        os.makedirs(dest_path, exist_ok=True)
        
        for pattern in patterns:
            items = glob.glob(pattern)
            for item in items:
                if os.path.exists(item):
                    item_name = os.path.basename(item)
                    target = os.path.join(dest_path, item_name)
                    
                    try:
                        if os.path.isdir(item):
                            if os.path.exists(target):
                                shutil.rmtree(target)
                            shutil.move(item, target)
                            print(f"   📂 {item_name} → {destination}")
                        else:
                            if os.path.exists(target):
                                os.remove(target)
                            shutil.move(item, target)
                            print(f"   📄 {item_name} → {destination}")
                        moved_count += 1
                    except Exception as e:
                        print(f"   ❌ Erreur avec {item}: {e}")
    
    # Déplacer les scripts shell restants
    shell_scripts = glob.glob('*.sh')
    if shell_scripts:
        print(f"\n🔧 Scripts shell vers tools/")
        tools_scripts = os.path.join(base_path, 'tools/scripts')
        os.makedirs(tools_scripts, exist_ok=True)
        
        for script in shell_scripts:
            target = os.path.join(tools_scripts, script)
            try:
                if os.path.exists(target):
                    os.remove(target)
                shutil.move(script, target)
                print(f"   🔧 {script} → tools/scripts/")
                moved_count += 1
            except Exception as e:
                print(f"   ❌ Erreur avec {script}: {e}")
    
    # Déplacer les binaires/rpm
    binaries = glob.glob('amdgpu_top*')
    if binaries:
        print(f"\n💿 Binaires vers tools/")
        tools_bin = os.path.join(base_path, 'tools/bin')
        os.makedirs(tools_bin, exist_ok=True)
        
        for binary in binaries:
            target = os.path.join(tools_bin, binary)
            try:
                if os.path.exists(target):
                    os.remove(target)
                shutil.move(binary, target)
                print(f"   💿 {binary} → tools/bin/")
                moved_count += 1
            except Exception as e:
                print(f"   ❌ Erreur avec {binary}: {e}")
    
    print(f"\n✅ NETTOYAGE TERMINÉ")
    print(f"📊 {moved_count} éléments déplacés")
    
    # Vérifier ce qui reste
    remaining = []
    for item in os.listdir('.'):
        if item not in ['.git', '.gitmodules', '.venv', 'README.md', 
                       'src', 'scripts', 'data', 'legacy', 'docs', 
                       'tools', 'temp']:
            remaining.append(item)
    
    if remaining:
        print(f"\n⚠️  Éléments restants: {len(remaining)}")
        for item in remaining[:10]:  # Montrer les 10 premiers
            print(f"   - {item}")
        if len(remaining) > 10:
            print(f"   ... et {len(remaining) - 10} autres")
    else:
        print(f"\n🎉 RACINE PARFAITEMENT PROPRE !")
        print("Structure finale:")
        print("├── src/        # Code source")
        print("├── scripts/    # Scripts de contrôle") 
        print("├── data/       # Données et résultats")
        print("├── tools/      # Outils et utilitaires")
        print("├── docs/       # Documentation")
        print("├── legacy/     # Code historique")
        print("├── temp/       # Fichiers temporaires")
        print("└── README.md   # Guide utilisateur")

if __name__ == "__main__":
    clean_workspace()