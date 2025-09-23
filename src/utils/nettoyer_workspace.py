#!/usr/bin/env python3

import os
import shutil
from pathlib import Path

def nettoyer_workspace():
    """Organise et nettoie le workspace"""
    
    print("🧹 GRAND NETTOYAGE DU WORKSPACE")
    print("=" * 40)
    
    workspace = Path('.')
    
    # Créer les dossiers d'organisation
    folders = {
        'systeme_evenementiel': 'Système événementiel avec affinité CPU',
        'dashboards': 'Interfaces web et monitoring',
        'systemes_autonomes': 'Systèmes autonomes et coordinateurs', 
        'pipelines_dhatu': 'Pipelines de traitement dhatu',
        'corpus_collection': 'Collection et analyse de corpus',
        'utilitaires': 'Scripts utilitaires et diagnostic',
        'archives': 'Fichiers obsolètes et anciens'
    }
    
    for folder in folders:
        folder_path = workspace / folder
        if not folder_path.exists():
            folder_path.mkdir()
            print(f"📁 Créé: {folder}/")
    
    # Classification des fichiers
    classifications = {
        'systeme_evenementiel': [
            'systeme_evenementiel_cpu.py',
            'dashboard_evenementiel.py', 
            'verifier_statut.py',
            'ouvrir_dashboard.py',
            'statut_evenementiel.py',
            'migration_evenementiel.py',
            'lancer_evenementiel.py'
        ],
        
        'dashboards': [
            'dashboard_realtime_avance.py',
            'moniteur_systeme_avance.py',
            'resource_allocation_monitor.py',
            'resource_dashboard_web.py',
            'dashboard_surveillance_autonome.py'
        ],
        
        'systemes_autonomes': [
            'coordinateur_global_autonome.py',
            'systeme_autonome_recherche_dhatu.py',
            'collecteur_corpus_autonome.py',
            'optimiseur_ml_autonome.py',
            'systeme_validation_metriques.py'
        ],
        
        'pipelines_dhatu': [
            'dhatu_aspectual_evolution.py',
            'pipeline_aspectuel_optimise_v2.py',
            'pipeline_reconstitution_aspectuelle.py',
            'algorithme_reconstruction_intelligente.py',
            'dictionnaire_dhatu_mot_exhaustif.py'
        ],
        
        'corpus_collection': [
            'corpus_collector_children.py',
            'collecteur_corpus_prescolaire.py',
            'analyseur_corpus_multilingue.py',
            'collecteur_multilingue_dev.py',
            'grand_corpus_collector.py'
        ],
        
        'utilitaires': [
            'verifier_statut.py',
            'diagnostic_complet.py',
            'check_performance.py',
            'analyseur_goulots_etranglement.py',
            'diagnostic_rapide.py'
        ]
    }
    
    # Fichiers obsolètes à archiver
    obsoletes = [
        'test_systeme_evenementiel.py',
        'verif_evenementiel.py', 
        'statut.py',
        'rapport_transition.py',
        'dashboard_simple.py',
        'dashboard_avec_donnees.py',
        'dashboard_maitre.py',
        'afficher_dashboard.py',
        'demarrer_dashboard.py',
        'installer_et_lancer_dashboard.py',
        'lancer_dashboard.py',
        'nettoyer_dashboards.py'
    ]
    
    # Déplacer les fichiers
    moved_count = 0
    
    for category, files in classifications.items():
        for filename in files:
            source = workspace / filename
            if source.exists():
                dest = workspace / category / filename
                if not dest.exists():
                    shutil.move(str(source), str(dest))
                    print(f"📦 {filename} → {category}/")
                    moved_count += 1
    
    # Archiver les obsolètes
    archived_count = 0
    for filename in obsoletes:
        source = workspace / filename
        if source.exists():
            dest = workspace / 'archives' / filename
            if not dest.exists():
                shutil.move(str(source), str(dest))
                print(f"🗃️ {filename} → archives/")
                archived_count += 1
    
    # Créer un README pour chaque dossier
    readme_content = {
        'systeme_evenementiel': """# Système Événementiel avec Affinité CPU

## Fichiers principaux
- `systeme_evenementiel_cpu.py` : Système principal événementiel
- `dashboard_evenementiel.py` : Dashboard web spécialisé
- `verifier_statut.py` : Vérification statut sans paramètres

## Utilisation
```bash
python3 systeme_evenementiel_cpu.py &  # Lance le système
python3 ouvrir_dashboard.py           # Ouvre l'interface web
```
""",
        
        'dashboards': """# Dashboards et Monitoring

## Interfaces web
- `dashboard_evenementiel.py` : Dashboard système événementiel
- `dashboard_realtime_avance.py` : Dashboard temps réel avancé
- `moniteur_systeme_avance.py` : Monitoring système avancé

## Utilisation
- Port 8892 : Dashboard événementiel
- Auto-refresh : 3 secondes
""",
        
        'systemes_autonomes': """# Systèmes Autonomes

## Coordinateurs
- `coordinateur_global_autonome.py` : Coordinateur principal
- `systeme_autonome_recherche_dhatu.py` : Recherche autonome

## Processeurs spécialisés
- `collecteur_corpus_autonome.py` : Collection autonome
- `optimiseur_ml_autonome.py` : Optimisation ML
""",
        
        'archives': """# Archives

Fichiers obsolètes conservés pour référence historique.
Ces fichiers ont été remplacés par des versions plus récentes.
"""
    }
    
    for folder, content in readme_content.items():
        readme_path = workspace / folder / 'README.md'
        if not readme_path.exists():
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"📝 README créé: {folder}/README.md")
    
    print(f"\n✅ NETTOYAGE TERMINÉ")
    print(f"📦 {moved_count} fichiers organisés")
    print(f"🗃️ {archived_count} fichiers archivés") 
    print(f"📁 {len(folders)} dossiers structurés")
    
    # Créer un fichier de résumé de l'organisation
    summary_path = workspace / 'ORGANISATION_WORKSPACE.md'
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("""# Organisation du Workspace PaniniFS-Research

## Structure

### 🎯 systeme_evenementiel/
Système événementiel avec affinité CPU exclusive
- Architecture événementielle (plus de cycles fixes)
- Allocation CPU dédiée par processeur
- Dashboard spécialisé sur port 8892

### 📊 dashboards/
Interfaces web et monitoring temps réel
- Dashboards avec auto-refresh
- Monitoring système avancé
- Métriques CPU/GPU/processus

### 🤖 systemes_autonomes/
Systèmes autonomes et coordinateurs
- Coordinateur global
- Processeurs spécialisés autonomes
- Validation et métriques

### 🔧 pipelines_dhatu/
Pipelines de traitement dhatu
- Évolution aspectuelle
- Reconstruction intelligente
- Dictionnaires exhaustifs

### 📚 corpus_collection/
Collection et analyse de corpus
- Collection multilingue
- Corpus préscolaires
- Analyseurs corpus

### 🛠️ utilitaires/
Scripts utilitaires et diagnostic
- Vérification statut
- Diagnostic performance
- Analyse goulots d'étranglement

### 🗃️ archives/
Fichiers obsolètes conservés pour référence

## État Actuel du Système

✅ **Système Événementiel Actif**
- 3 processus événementiels en cours
- Affinité CPU configurée (cores 1-8)
- Dashboard accessible: http://localhost:8892

✅ **Architecture Optimisée**
- Traitement par événements (pas de cycles fixes)
- Cores dédiés par processeur
- Monitoring temps réel fonctionnel

## Scripts Principaux

```bash
# Système événementiel
python3 systeme_evenementiel/systeme_evenementiel_cpu.py &
python3 systeme_evenementiel/ouvrir_dashboard.py

# Vérification
python3 systeme_evenementiel/verifier_statut.py

# Monitoring
python3 dashboards/dashboard_evenementiel.py &
```
""")
    
    print(f"📄 ORGANISATION_WORKSPACE.md créé")
    
    return moved_count, archived_count

if __name__ == "__main__":
    nettoyer_workspace()