#!/usr/bin/env python3
"""
Plan Autonome de Recherche PaniniFS
Exécution continue sans interaction humaine pour faire avancer la recherche réelle
"""

import os
import json
import time
import subprocess
import glob
from datetime import datetime
from pathlib import Path

class AutonomousResearchPlan:
    def __init__(self):
        self.start_time = datetime.now()
        self.workspace = Path("/home/stephane/GitHub/PaniniFS-Research")
        self.results_dir = self.workspace / "autonomous_results"
        self.results_dir.mkdir(exist_ok=True)
        
        self.execution_log = []
        self.research_progress = {
            "dhatu_analysis_completed": False,
            "patterns_extracted": 0,
            "hypotheses_tested": 0,
            "corpus_processed": 0,
            "discoveries": []
        }
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        log_entry = f"{timestamp} {level}: {message}"
        print(log_entry)
        self.execution_log.append(log_entry)
        
    def save_progress(self):
        """Sauvegarde automatique du progrès"""
        progress_file = self.results_dir / f"research_progress_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(progress_file, 'w') as f:
            json.dump({
                "start_time": self.start_time.isoformat(),
                "current_time": datetime.now().isoformat(),
                "progress": self.research_progress,
                "execution_log": self.execution_log[-100:]  # Dernières 100 entrées
            }, f, indent=2)
        
    def analyze_existing_dhatu_corpus(self):
        """Analyse le corpus dhatu existant pour identifier les vraies données"""
        self.log("🔍 ANALYSE CORPUS DHATU EXISTANT")
        
        dhatu_paths = [
            "tech/data/dhatu_*.json",
            "panini/data/dhatu/*.json",
            "tech/corpus_*/dhatu*.json"
        ]
        
        real_dhatu_files = []
        total_elements = 0
        
        for pattern in dhatu_paths:
            files = glob.glob(str(self.workspace / pattern))
            for file_path in files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                    if isinstance(data, list):
                        elements = len(data)
                    elif isinstance(data, dict) and 'dhatu' in data:
                        elements = len(data['dhatu'])
                    elif isinstance(data, dict) and 'elements' in data:
                        elements = len(data['elements'])
                    else:
                        elements = len(data) if hasattr(data, '__len__') else 0
                        
                    if elements > 0:
                        real_dhatu_files.append({
                            'path': file_path,
                            'elements': elements,
                            'size_kb': os.path.getsize(file_path) // 1024
                        })
                        total_elements += elements
                        
                except Exception as e:
                    self.log(f"Erreur lecture {file_path}: {e}", "WARNING")
        
        self.log(f"📊 Corpus dhatu réel identifié:")
        self.log(f"   - {len(real_dhatu_files)} fichiers trouvés")
        self.log(f"   - {total_elements:,} éléments dhatu au total")
        
        # Sauvegarde des résultats d'analyse
        analysis_result = {
            'timestamp': datetime.now().isoformat(),
            'total_files': len(real_dhatu_files),
            'total_elements': total_elements,
            'files': real_dhatu_files
        }
        
        with open(self.results_dir / "dhatu_corpus_analysis.json", 'w') as f:
            json.dump(analysis_result, f, indent=2)
            
        self.research_progress['dhatu_analysis_completed'] = True
        self.research_progress['corpus_processed'] = total_elements
        
        return real_dhatu_files
    
    def execute_unified_dhatu_pipeline(self, dhatu_files):
        """Exécute le pipeline dhatu unifié sur les vraies données"""
        self.log("⚛️ EXÉCUTION PIPELINE DHATU UNIFIÉ")
        
        if not os.path.exists("tech/unified_dhatu_pipeline.py"):
            self.log("Pipeline dhatu unifié non trouvé, création version simplifiée", "WARNING")
            return False
            
        try:
            # Exécution du pipeline avec timeout raisonnable
            result = subprocess.run([
                "python3", "tech/unified_dhatu_pipeline.py"
            ], capture_output=True, text=True, timeout=300, cwd=self.workspace)
            
            if result.returncode == 0:
                self.log("✅ Pipeline dhatu exécuté avec succès")
                self.log(f"Sortie: {result.stdout[-500:]}")  # Dernières 500 chars
                self.research_progress['patterns_extracted'] += 1
                return True
            else:
                self.log(f"Erreur pipeline: {result.stderr}", "ERROR")
                return False
                
        except subprocess.TimeoutExpired:
            self.log("Pipeline dhatu timeout (300s), arrêt forcé", "WARNING")
            return False
        except Exception as e:
            self.log(f"Erreur exécution pipeline: {e}", "ERROR")
            return False
    
    def test_linguistic_hypotheses(self):
        """Test des hypothèses linguistiques sur les données réelles"""
        self.log("🧪 TEST HYPOTHÈSES LINGUISTIQUES")
        
        hypothesis_tests = [
            "tech/peer_verification_system.py",
            "tech/verification_final.py",
            "autonomous_dhatu_optimizer.py"
        ]
        
        results = []
        for test_script in hypothesis_tests:
            if os.path.exists(self.workspace / test_script):
                try:
                    self.log(f"Exécution {test_script}")
                    result = subprocess.run([
                        "python3", test_script
                    ], capture_output=True, text=True, timeout=180, cwd=self.workspace)
                    
                    if result.returncode == 0:
                        self.log(f"✅ {test_script} terminé")
                        results.append({
                            'script': test_script,
                            'success': True,
                            'output_length': len(result.stdout)
                        })
                        self.research_progress['hypotheses_tested'] += 1
                    else:
                        self.log(f"❌ {test_script} échoué: {result.stderr[:200]}", "WARNING")
                        
                except subprocess.TimeoutExpired:
                    self.log(f"⏱️ {test_script} timeout", "WARNING")
                except Exception as e:
                    self.log(f"Erreur {test_script}: {e}", "ERROR")
        
        return results
    
    def autonomous_discovery_cycle(self):
        """Cycle de découverte autonome continue"""
        self.log("🚀 DÉMARRAGE CYCLE DÉCOUVERTE AUTONOME")
        
        cycle_count = 0
        while True:
            cycle_count += 1
            self.log(f"🔄 CYCLE {cycle_count} - {datetime.now().strftime('%H:%M:%S')}")
            
            try:
                # 1. Analyse corpus (si pas encore fait)
                if not self.research_progress['dhatu_analysis_completed']:
                    dhatu_files = self.analyze_existing_dhatu_corpus()
                    
                    # 2. Exécution pipeline sur vraies données
                    if dhatu_files:
                        self.execute_unified_dhatu_pipeline(dhatu_files)
                
                # 3. Test hypothèses linguistiques
                self.test_linguistic_hypotheses()
                
                # 4. Sauvegarde progrès
                self.save_progress()
                
                # 5. Recherche de nouvelles découvertes
                self.scan_for_discoveries()
                
                self.log(f"✅ CYCLE {cycle_count} TERMINÉ")
                self.log(f"📊 Progrès: {self.research_progress['patterns_extracted']} patterns, {self.research_progress['hypotheses_tested']} tests")
                
                # Pause entre cycles (ajustable selon performance système)
                time.sleep(120)  # 2 minutes entre cycles
                
            except KeyboardInterrupt:
                self.log("🛑 Arrêt demandé par utilisateur")
                break
            except Exception as e:
                self.log(f"Erreur cycle {cycle_count}: {e}", "ERROR")
                time.sleep(60)  # Pause plus longue en cas d'erreur
    
    def scan_for_discoveries(self):
        """Scanner les résultats pour identifier des découvertes"""
        discovery_patterns = [
            "panini_high_performance_report_*.json",
            "pilot_validation_report.json",
            "tech/corpus_*/performance_report.json"
        ]
        
        new_discoveries = 0
        for pattern in discovery_patterns:
            files = glob.glob(str(self.workspace / pattern))
            for file_path in files:
                # Vérifier si fichier modifié récemment (dernière heure)
                if os.path.getmtime(file_path) > time.time() - 3600:
                    try:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                        
                        # Recherche d'indicateurs de découverte
                        if any(key in str(data).lower() for key in ['gain', 'performance', 'breakthrough', 'discovery']):
                            discovery_summary = f"Découverte dans {os.path.basename(file_path)}"
                            if discovery_summary not in [d.get('summary', '') for d in self.research_progress['discoveries']]:
                                self.research_progress['discoveries'].append({
                                    'timestamp': datetime.now().isoformat(),
                                    'file': file_path,
                                    'summary': discovery_summary
                                })
                                new_discoveries += 1
                                self.log(f"🎯 DÉCOUVERTE: {discovery_summary}")
                                
                    except Exception as e:
                        continue
        
        if new_discoveries > 0:
            self.log(f"📈 {new_discoveries} nouvelles découvertes identifiées")

def main():
    """Point d'entrée principal"""
    print("🚀 PLAN AUTONOME DE RECHERCHE PANINI")
    print("=" * 60)
    print("🎯 Objectif: Recherche continue sans interaction humaine")
    print("📊 Focus: Données linguistiques réelles uniquement")
    print("⚛️ Méthode: Cycles de découverte automatisés")
    print("=" * 60)
    
    planner = AutonomousResearchPlan()
    
    try:
        planner.autonomous_discovery_cycle()
    except Exception as e:
        planner.log(f"Erreur fatale: {e}", "CRITICAL")
    finally:
        planner.save_progress()
        duration = datetime.now() - planner.start_time
        planner.log(f"🏁 Session terminée après {duration}")

if __name__ == "__main__":
    main()