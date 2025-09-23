#!/usr/bin/env python3
"""
Diagnostic Simple de l'État du Système PaniniFS
Vérifie ce qui fonctionne vraiment et ce qui ne fonctionne pas
"""

import psutil
import os
import json
from pathlib import Path
from datetime import datetime

def verifier_processus_panini():
    """Vérifie quels processus PaniniFS sont actifs"""
    print("🔍 PROCESSUS PANINI ACTIFS:")
    print("=" * 50)
    
    processus_trouve = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'status', 'cpu_percent']):
        try:
            cmdline = ' '.join(proc.info['cmdline'] or [])
            if any(term in cmdline.lower() for term in ['orchestrateur', 'gestionnaire', 'collecteur', 'panini', 'dashboard']):
                processus_trouve.append({
                    'pid': proc.info['pid'],
                    'nom': proc.info['name'],
                    'commande': cmdline[:80] + '...' if len(cmdline) > 80 else cmdline,
                    'statut': proc.info['status'],
                    'cpu': proc.info['cpu_percent']
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    if processus_trouve:
        for p in processus_trouve:
            print(f"✅ PID {p['pid']:>6} | {p['statut']:>10} | CPU {p['cpu']:>5.1f}% | {p['commande']}")
    else:
        print("❌ AUCUN processus PaniniFS actif")
    
    return len(processus_trouve)

def verifier_fichiers_importants():
    """Vérifie l'existence des fichiers clés"""
    print("\n📁 FICHIERS IMPORTANTS:")
    print("=" * 50)
    
    fichiers_cles = [
        ('orchestrateur_pipeline_iteratif.py', 'Orchestrateur principal'),
        ('gestionnaire_arriere_plan.py', 'Gestionnaire de processus'),
        ('collecteur_corpus_scientifique.py', 'Collecteur de corpus'),
        ('corpus_scientifique.json', 'Corpus principal'),
        ('corpus_multilingue_dev.json', 'Corpus développement'),
        ('pipeline_iteratif_resultats/etat_pipeline.json', 'État pipeline'),
        ('gestionnaire_arriere_plan.log', 'Logs gestionnaire')
    ]
    
    fichiers_existants = 0
    for fichier, description in fichiers_cles:
        if Path(fichier).exists():
            taille = Path(fichier).stat().st_size
            print(f"✅ {fichier:<40} | {description} ({taille:,} bytes)")
            fichiers_existants += 1
        else:
            print(f"❌ {fichier:<40} | {description} (MANQUANT)")
    
    return fichiers_existants

def verifier_corpus():
    """Vérifie le contenu des corpus"""
    print("\n📚 ÉTAT DES CORPUS:")
    print("=" * 50)
    
    corpus_files = [
        'corpus_scientifique.json',
        'corpus_multilingue_dev.json',
        'corpus_prescolaire.json'
    ]
    
    total_documents = 0
    for corpus_file in corpus_files:
        if Path(corpus_file).exists():
            try:
                with open(corpus_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if isinstance(data, list):
                    docs = len(data)
                elif isinstance(data, dict):
                    docs = len(data.get('documents', []))
                else:
                    docs = 0
                
                print(f"✅ {corpus_file:<30} | {docs:>6} documents")
                total_documents += docs
            except Exception as e:
                print(f"❌ {corpus_file:<30} | Erreur: {e}")
        else:
            print(f"❌ {corpus_file:<30} | MANQUANT")
    
    print(f"\n📊 TOTAL: {total_documents} documents disponibles")
    return total_documents

def verifier_etat_pipeline():
    """Vérifie l'état du pipeline"""
    print("\n⚙️ ÉTAT DU PIPELINE:")
    print("=" * 50)
    
    etat_file = 'pipeline_iteratif_resultats/etat_pipeline.json'
    if Path(etat_file).exists():
        try:
            with open(etat_file, 'r') as f:
                etat = json.load(f)
            
            print(f"✅ Niveau actuel: {etat.get('niveau_actuel', 0)}")
            print(f"✅ Cycles complétés: {etat.get('cycles_completes', 0)}")
            print(f"✅ Documents traités: {etat.get('documents_traites', 0)}")
            print(f"✅ Qualité modèle: {etat.get('modele_qualite', 0):.2%}")
            
            # Vérifier dernière modification
            mod_time = Path(etat_file).stat().st_mtime
            derniere_modif = datetime.fromtimestamp(mod_time)
            print(f"📅 Dernière mise à jour: {derniere_modif.strftime('%Y-%m-%d %H:%M:%S')}")
            
            return True
        except Exception as e:
            print(f"❌ Erreur lecture état: {e}")
            return False
    else:
        print("❌ Fichier d'état du pipeline MANQUANT")
        return False

def verifier_logs_recents():
    """Vérifie les logs récents"""
    print("\n📋 LOGS RÉCENTS:")
    print("=" * 50)
    
    log_file = 'gestionnaire_arriere_plan.log'
    if Path(log_file).exists():
        try:
            with open(log_file, 'r') as f:
                lines = f.readlines()
            
            print("📄 5 dernières entrées de log:")
            for line in lines[-5:]:
                print(f"   {line.strip()}")
            
            # Compter redémarrages
            redemarrages = sum(1 for line in lines if 'Redémarrage' in line)
            print(f"\n🔄 Total redémarrages détectés: {redemarrages}")
            
            return True
        except Exception as e:
            print(f"❌ Erreur lecture logs: {e}")
            return False
    else:
        print("❌ Fichier de logs MANQUANT")
        return False

def verifier_ressources_systeme():
    """Vérifie l'utilisation des ressources"""
    print("\n💻 RESSOURCES SYSTÈME:")
    print("=" * 50)
    
    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    print(f"🔥 CPU: {cpu_percent:>6.1f}%")
    
    # Mémoire
    memory = psutil.virtual_memory()
    print(f"🧠 RAM: {memory.percent:>6.1f}% ({memory.used//1024//1024//1024}GB / {memory.total//1024//1024//1024}GB)")
    
    # Processus gourmands
    print("\n🔍 Top 3 processus CPU:")
    processus = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            processus.append((proc.info['pid'], proc.info['name'], proc.info['cpu_percent']))
        except:
            continue
    
    processus.sort(key=lambda x: x[2], reverse=True)
    for pid, nom, cpu in processus[:3]:
        if cpu > 0:
            print(f"   PID {pid:>6} | {nom:<20} | {cpu:>5.1f}%")

def diagnostic_complet():
    """Effectue un diagnostic complet"""
    print("🔬 DIAGNOSTIC SYSTÈME PANINI-FS")
    print("=" * 70)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Vérifications
    nb_processus = verifier_processus_panini()
    nb_fichiers = verifier_fichiers_importants()
    nb_documents = verifier_corpus()
    pipeline_ok = verifier_etat_pipeline()
    logs_ok = verifier_logs_recents()
    
    verifier_ressources_systeme()
    
    # Résumé
    print("\n🎯 RÉSUMÉ DIAGNOSTIC:")
    print("=" * 50)
    
    if nb_processus == 0:
        print("🚨 PROBLÈME MAJEUR: Aucun processus PaniniFS actif")
        print("💡 ACTION: Démarrer le gestionnaire arrière-plan")
    elif nb_processus < 3:
        print("⚠️  ATTENTION: Peu de processus actifs")
        print("💡 ACTION: Vérifier configuration gestionnaire")
    else:
        print("✅ Processus: Niveau normal")
    
    if nb_documents == 0:
        print("🚨 PROBLÈME: Aucun corpus disponible")
        print("💡 ACTION: Lancer collecteur de corpus")
    else:
        print(f"✅ Corpus: {nb_documents} documents disponibles")
    
    if not pipeline_ok:
        print("🚨 PROBLÈME: Pipeline non initialisé")
        print("💡 ACTION: Lancer orchestrateur pipeline")
    else:
        print("✅ Pipeline: État disponible")
    
    # Score global
    score = 0
    if nb_processus > 0: score += 30
    if nb_documents > 0: score += 25
    if pipeline_ok: score += 25
    if logs_ok: score += 10
    if nb_fichiers >= 5: score += 10
    
    print(f"\n📊 SCORE SANTÉ SYSTÈME: {score}/100")
    
    if score < 30:
        print("🚨 SYSTÈME EN PANNE - Redémarrage nécessaire")
    elif score < 60:
        print("⚠️  SYSTÈME DÉGRADÉ - Actions correctives requises")
    elif score < 80:
        print("🔶 SYSTÈME FONCTIONNEL - Optimisations possibles")
    else:
        print("✅ SYSTÈME OPTIMAL - Tout fonctionne bien")

if __name__ == "__main__":
    diagnostic_complet()