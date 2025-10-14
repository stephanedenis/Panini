#!/usr/bin/env python3
"""
Nettoyeur de processus stagnants PaniniFS
Arrête proprement les analyses en cours et nettoie le système
"""

import subprocess
import json
import os
import time
from pathlib import Path

class ProcessCleaner:
    """Nettoyeur de processus stagnants"""
    
    def __init__(self):
        self.stopped_processes = []
        self.preserved_processes = []
        self.cleaned_files = []
        
    def identify_stagnant_processes(self):
        """Identifie les processus à arrêter"""
        stagnant_patterns = [
            'analyseur_ambiguites_semantiques',
            'systeme_detection_automatique',
            'processus_raffinement_definitions',
            'coordinateur_analyses_concurrentes',
            'analyseur_corpus_geometrique'
        ]
        
        preserve_patterns = [
            'dashboard_simplifie_panlang'
        ]
        
        print("🔍 IDENTIFICATION PROCESSUS STAGNANTS")
        print("=" * 45)
        
        for pattern in stagnant_patterns:
            try:
                result = subprocess.run(['pgrep', '-f', pattern], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    pids = [pid.strip() for pid in result.stdout.split('\n') if pid.strip()]
                    print(f"⚠️ Trouvé {pattern}: {len(pids)} processus")
                    for pid in pids:
                        self.stopped_processes.append((pattern, pid))
            except Exception as e:
                print(f"Erreur vérification {pattern}: {e}")
        
        # Vérifier processus à préserver
        for pattern in preserve_patterns:
            try:
                result = subprocess.run(['pgrep', '-f', pattern], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    pids = [pid.strip() for pid in result.stdout.split('\n') if pid.strip()]
                    print(f"✅ Préservé {pattern}: {len(pids)} processus")
                    for pid in pids:
                        self.preserved_processes.append((pattern, pid))
            except Exception as e:
                print(f"Erreur vérification {pattern}: {e}")
    
    def stop_stagnant_processes(self):
        """Arrête les processus stagnants"""
        if not self.stopped_processes:
            print("✅ Aucun processus stagnant trouvé")
            return
        
        print(f"\n🛑 ARRÊT PROCESSUS STAGNANTS")
        print("=" * 35)
        
        for pattern, pid in self.stopped_processes:
            try:
                subprocess.run(['kill', pid], check=True)
                print(f"✅ Arrêté {pattern} (PID: {pid})")
                time.sleep(0.5)  # Pause entre arrêts
            except subprocess.CalledProcessError:
                print(f"⚠️ Processus {pattern} (PID: {pid}) déjà arrêté")
            except Exception as e:
                print(f"❌ Erreur arrêt {pattern} (PID: {pid}): {e}")
    
    def cleanup_temporary_files(self):
        """Nettoie les fichiers temporaires d'analyse"""
        temp_patterns = [
            '*_log.txt',
            'config_geometric_parallel_*.json',
            'evaluation_strategique_*.json'
        ]
        
        preserve_patterns = [
            'analyse_ambiguites_dictionnaire_*.json',
            'dictionnaire_raffine_*.json', 
            'parallel_analysis_result_*.json',
            'rapport_*.md',
            'RAPPORT_*.md'
        ]
        
        print(f"\n🧹 NETTOYAGE FICHIERS TEMPORAIRES")
        print("=" * 40)
        
        all_files = list(Path('.').glob('*'))
        
        # Nettoyer fichiers temporaires
        for pattern in temp_patterns:
            matching_files = list(Path('.').glob(pattern))
            for file_path in matching_files:
                # Vérifier si pas dans les fichiers à préserver
                should_preserve = any(
                    file_path.match(preserve_pattern) 
                    for preserve_pattern in preserve_patterns
                )
                
                if not should_preserve:
                    try:
                        file_path.unlink()
                        print(f"🗑️ Supprimé: {file_path.name}")
                        self.cleaned_files.append(str(file_path))
                    except Exception as e:
                        print(f"⚠️ Erreur suppression {file_path}: {e}")
                else:
                    print(f"✅ Préservé: {file_path.name}")
    
    def update_process_registry(self):
        """Met à jour le registre des processus"""
        registry_file = 'registre_processus_actifs.json'
        
        if not os.path.exists(registry_file):
            return
        
        print(f"\n📋 MISE À JOUR REGISTRE PROCESSUS")
        print("=" * 35)
        
        try:
            with open(registry_file, 'r', encoding='utf-8') as f:
                registry = json.load(f)
            
            # Marquer processus stagnants comme arrêtés
            if 'processus_locaux' in registry:
                for process_name, process_info in registry['processus_locaux'].items():
                    if any(pattern in process_name for pattern, _ in self.stopped_processes):
                        if process_info.get('statut') != 'terminé_succès':
                            process_info['statut'] = 'arrêté_nettoyage'
                            process_info['fin'] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
                            process_info['notes'] = f"🛑 Arrêté lors nettoyage système - {time.strftime('%Y-%m-%d %H:%M')}"
            
            # Ajouter info nettoyage
            registry['derniere_maintenance'] = {
                'timestamp': time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                'processus_arretes': len(self.stopped_processes),
                'processus_preserves': len(self.preserved_processes),
                'fichiers_nettoyes': len(self.cleaned_files),
                'type': 'nettoyage_stagnants'
            }
            
            with open(registry_file, 'w', encoding='utf-8') as f:
                json.dump(registry, f, ensure_ascii=False, indent=2)
            
            print("✅ Registre mis à jour")
            
        except Exception as e:
            print(f"❌ Erreur mise à jour registre: {e}")
    
    def generate_cleanup_summary(self):
        """Génère résumé du nettoyage"""
        print(f"\n📊 RÉSUMÉ NETTOYAGE")
        print("=" * 25)
        print(f"🛑 Processus arrêtés: {len(self.stopped_processes)}")
        print(f"✅ Processus préservés: {len(self.preserved_processes)}")
        print(f"🗑️ Fichiers nettoyés: {len(self.cleaned_files)}")
        
        if self.preserved_processes:
            print(f"\n✅ PROCESSUS ACTIFS:")
            for pattern, pid in self.preserved_processes:
                print(f"   - {pattern} (PID: {pid})")
        
        print(f"\n🎯 SYSTÈME NETTOYÉ - Prêt pour prochaine session")
        
        return {
            'stopped_processes': len(self.stopped_processes),
            'preserved_processes': len(self.preserved_processes),
            'cleaned_files': len(self.cleaned_files),
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def run_complete_cleanup(self):
        """Lance nettoyage complet"""
        print("🧹 NETTOYEUR PROCESSUS STAGNANTS")
        print("=" * 50)
        
        self.identify_stagnant_processes()
        self.stop_stagnant_processes()
        self.cleanup_temporary_files()
        self.update_process_registry()
        
        summary = self.generate_cleanup_summary()
        
        # Sauvegarder rapport nettoyage
        cleanup_report = f"nettoyage_rapport_{int(time.time())}.json"
        with open(cleanup_report, 'w', encoding='utf-8') as f:
            json.dump({
                'summary': summary,
                'stopped_processes': [
                    {'pattern': pattern, 'pid': pid} 
                    for pattern, pid in self.stopped_processes
                ],
                'preserved_processes': [
                    {'pattern': pattern, 'pid': pid} 
                    for pattern, pid in self.preserved_processes
                ],
                'cleaned_files': self.cleaned_files
            }, f, ensure_ascii=False, indent=2)
        
        print(f"📄 Rapport nettoyage: {cleanup_report}")
        
        return summary

def main():
    """Point d'entrée nettoyeur"""
    cleaner = ProcessCleaner()
    cleaner.run_complete_cleanup()

if __name__ == "__main__":
    main()