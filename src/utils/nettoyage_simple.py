#!/usr/bin/env python3

import shutil
import os

print("🧹 NETTOYAGE WORKSPACE")

# Créer les dossiers
folders = ['systeme_evenementiel', 'dashboards', 'archives', 'utilitaires']

for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"📁 Créé: {folder}/")

# Déplacer les fichiers événementiels
event_files = [
    'systeme_evenementiel_cpu.py',
    'dashboard_evenementiel.py',
    'verifier_statut.py', 
    'ouvrir_dashboard.py'
]

moved = 0
for f in event_files:
    if os.path.exists(f):
        dest = f'systeme_evenementiel/{f}'
        if not os.path.exists(dest):
            shutil.move(f, dest)
            print(f"📦 {f} → systeme_evenementiel/")
            moved += 1

# Déplacer les dashboards
dashboard_files = [
    'dashboard_realtime_avance.py',
    'moniteur_systeme_avance.py',
    'resource_allocation_monitor.py'
]

for f in dashboard_files:
    if os.path.exists(f):
        dest = f'dashboards/{f}'
        if not os.path.exists(dest):
            shutil.move(f, dest)
            print(f"📊 {f} → dashboards/")
            moved += 1

# Archiver les obsolètes
obsoletes = [
    'statut.py',
    'test_systeme_evenementiel.py',
    'verif_evenementiel.py',
    'dashboard_simple.py',
    'dashboard_avec_donnees.py'
]

archived = 0
for f in obsoletes:
    if os.path.exists(f):
        dest = f'archives/{f}'
        if not os.path.exists(dest):
            shutil.move(f, dest)
            print(f"🗃️ {f} → archives/")
            archived += 1

print(f"\n✅ Nettoyage terminé: {moved} déplacés, {archived} archivés")