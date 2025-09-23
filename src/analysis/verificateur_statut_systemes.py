#!/usr/bin/env python3
"""
Vérificateur de statut de tous les systèmes PaniniFS Research
Répond à la question: "C'est fait, c'est à faire, ou ça roule en arrière-plan?"
"""

import os
import subprocess
import json
import sys
from pathlib import Path

def check_process_running(process_name):
    """Vérifie si un processus est en cours d'exécution"""
    try:
        result = subprocess.run(['pgrep', '-f', process_name], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def check_file_exists(filepath):
    """Vérifie si un fichier existe"""
    return Path(filepath).exists()

def get_file_size(filepath):
    """Retourne la taille d'un fichier en Mo"""
    try:
        size_bytes = Path(filepath).stat().st_size
        return round(size_bytes / (1024 * 1024), 1)
    except:
        return 0

def check_corpus_status():
    """Vérifie le statut des corpus"""
    status = {}
    
    # Corpus scientifique
    corpus_sci = "tech/corpus_simple/corpus.json"
    if check_file_exists(corpus_sci):
        try:
            with open(corpus_sci, 'r', encoding='utf-8') as f:
                data = json.load(f)
                status['corpus_scientifique'] = {
                    'état': '✅ FAIT',
                    'documents': len(data.get('documents', [])),
                    'taille': f"{get_file_size(corpus_sci)} Mo"
                }
        except:
            status['corpus_scientifique'] = {'état': '❌ ERREUR', 'documents': 0}
    else:
        status['corpus_scientifique'] = {'état': '❌ MANQUANT', 'documents': 0}
    
    # Corpus multilingue développemental
    corpus_multi = "corpus_multilingue_dev.json"
    if check_file_exists(corpus_multi):
        try:
            with open(corpus_multi, 'r', encoding='utf-8') as f:
                data = json.load(f)
                status['corpus_multilingue'] = {
                    'état': '✅ FAIT',
                    'documents': len(data.get('documents', [])),
                    'taille': f"{get_file_size(corpus_multi)} Mo"
                }
        except:
            status['corpus_multilingue'] = {'état': '❌ ERREUR', 'documents': 0}
    else:
        status['corpus_multilingue'] = {'état': '❌ MANQUANT', 'documents': 0}
    
    # Corpus unifié
    corpus_unifie = "corpus_complet_unifie.json"
    if check_file_exists(corpus_unifie):
        try:
            with open(corpus_unifie, 'r', encoding='utf-8') as f:
                data = json.load(f)
                status['corpus_unifie'] = {
                    'état': '✅ FAIT',
                    'documents': len(data.get('documents', [])),
                    'taille': f"{get_file_size(corpus_unifie)} Mo"
                }
        except:
            status['corpus_unifie'] = {'état': '❌ ERREUR', 'documents': 0}
    else:
        status['corpus_unifie'] = {'état': '❌ MANQUANT', 'documents': 0}
    
    return status

def check_archive_status():
    """Vérifie le statut de l'archive de références"""
    status = {}
    
    # Base de données des références
    ref_db = "panini/references/references_database.json"
    if check_file_exists(ref_db):
        try:
            with open(ref_db, 'r', encoding='utf-8') as f:
                data = json.load(f)
                status['references_database'] = {
                    'état': '✅ FAIT',
                    'références': len(data.get('references', [])),
                    'taille': f"{get_file_size(ref_db)} Mo"
                }
        except:
            status['references_database'] = {'état': '❌ ERREUR', 'références': 0}
    else:
        status['references_database'] = {'état': '❌ MANQUANT', 'références': 0}
    
    # Cache des documents
    cache_dir = Path("panini/references/cache")
    if cache_dir.exists():
        pdf_files = list(cache_dir.glob("*.pdf"))
        html_files = list(cache_dir.glob("*.html"))
        total_size = sum(f.stat().st_size for f in pdf_files + html_files) / (1024 * 1024)
        
        status['cache_documents'] = {
            'état': '✅ FAIT',
            'pdfs': len(pdf_files),
            'htmls': len(html_files),
            'taille_totale': f"{round(total_size, 1)} Mo"
        }
    else:
        status['cache_documents'] = {'état': '❌ MANQUANT', 'pdfs': 0, 'htmls': 0}
    
    return status

def check_background_processes():
    """Vérifie les processus en arrière-plan"""
    processes_to_check = [
        'autonomous_corpus_processor.py',
        'autonomous_dhatu_optimizer.py',
        'grand_corpus_collector.py',
        'panini_pipeline_dashboard.py',
        'pipeline_simulator.py'
    ]
    
    running = []
    for process in processes_to_check:
        if check_process_running(process):
            running.append(process)
    
    return running

def check_dhatu_processing():
    """Vérifie le statut du traitement dhatu"""
    status = {}
    
    # Fichier dhatu processing
    dhatu_output = "dhatu_processing_output"
    if Path(dhatu_output).exists():
        files = list(Path(dhatu_output).glob("*.json"))
        status['dhatu_processing'] = {
            'état': '✅ FAIT' if files else '⚠️ PARTIEL',
            'fichiers': len(files)
        }
    else:
        status['dhatu_processing'] = {'état': '❌ À FAIRE', 'fichiers': 0}
    
    return status

def main():
    print("🔍 VÉRIFICATION STATUT SYSTÈMES PANINIFS RESEARCH")
    print("=" * 60)
    
    # Vérification des corpus
    print("\n📚 CORPUS:")
    corpus_status = check_corpus_status()
    for name, info in corpus_status.items():
        état = info['état']
        docs = info.get('documents', info.get('fichiers', 0))
        taille = info.get('taille', '')
        print(f"  {name}: {état} ({docs} docs, {taille})")
    
    # Vérification de l'archive
    print("\n📦 ARCHIVE RÉFÉRENCES:")
    archive_status = check_archive_status()
    for name, info in archive_status.items():
        état = info['état']
        if 'références' in info:
            count = info['références']
            taille = info.get('taille', '')
            print(f"  {name}: {état} ({count} réfs, {taille})")
        elif 'pdfs' in info:
            pdfs = info['pdfs']
            htmls = info['htmls']
            taille = info.get('taille_totale', '')
            print(f"  {name}: {état} ({pdfs} PDFs + {htmls} HTMLs, {taille})")
    
    # Vérification dhatu
    print("\n🔤 TRAITEMENT DHATU:")
    dhatu_status = check_dhatu_processing()
    for name, info in dhatu_status.items():
        état = info['état']
        fichiers = info['fichiers']
        print(f"  {name}: {état} ({fichiers} fichiers)")
    
    # Vérification processus arrière-plan
    print("\n⚡ PROCESSUS ARRIÈRE-PLAN:")
    running_processes = check_background_processes()
    if running_processes:
        for process in running_processes:
            print(f"  🔄 EN COURS: {process}")
    else:
        print("  ⏹️ Aucun processus en arrière-plan")
    
    # Résumé global
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ GLOBAL:")
    
    # Compter les éléments terminés
    total_done = 0
    total_items = 0
    
    for status_dict in [corpus_status, archive_status, dhatu_status]:
        for info in status_dict.values():
            total_items += 1
            if '✅ FAIT' in info['état']:
                total_done += 1
    
    completion_rate = (total_done / total_items * 100) if total_items > 0 else 0
    
    print(f"  Complétude: {total_done}/{total_items} ({completion_rate:.1f}%)")
    
    if running_processes:
        print(f"  Statut: 🔄 RECHERCHE AUTONOME ACTIVE ({len(running_processes)} processus)")
    elif completion_rate >= 80:
        print("  Statut: ✅ SYSTÈMES OPÉRATIONNELS")
    else:
        print("  Statut: ⚠️ CONFIGURATION INCOMPLÈTE")
    
    print("\n🎯 RÉPONSE À VOTRE QUESTION:")
    if completion_rate >= 80 and running_processes:
        print("  ✅ C'EST FAIT + ÇA ROULE EN ARRIÈRE-PLAN")
    elif completion_rate >= 80:
        print("  ✅ C'EST FAIT (prêt pour recherche autonome)")
    elif running_processes:
        print("  🔄 ÇA ROULE EN ARRIÈRE-PLAN (configuration en cours)")
    else:
        print("  ⚠️ C'EST À FAIRE (certains éléments manquants)")

if __name__ == "__main__":
    main()