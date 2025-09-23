#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 Intelligent Research Coordinator
Coordination optimisée entre Colab intensif et collecteur intelligent
"""

import json
import time
import subprocess
import requests
from pathlib import Path
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Any, Optional

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IntelligentResearchCoordinator:
    """Coordinateur pour optimiser recherche Colab + collecte locale"""
    
    def __init__(self):
        self.base_dir = Path("/home/stephane/GitHub/PaniniFS-Research")
        self.colab_results_dir = self.base_dir / "colab_integration" / "results"
        self.corpus_dir = self.base_dir / "data" / "incremental_corpus"
        
        # Stats de coordination
        self.stats = {
            'colab_sessions_detected': 0,
            'corpus_batches_processed': 0,
            'quality_improvements': 0,
            'github_syncs': 0,
            'start_time': time.time(),
            'last_colab_result': None,
            'last_corpus_batch': None
        }
        
        logger.info("🔄 Intelligent Research Coordinator initialisé")
        logger.info(f"📊 Monitoring: Colab ({self.colab_results_dir}) + Corpus ({self.corpus_dir})")
    
    def detect_colab_activity(self) -> Optional[Dict[str, Any]]:
        """Détecte nouvelle activité Colab"""
        try:
            # Chercher nouveaux résultats Colab
            if not self.colab_results_dir.exists():
                return None
            
            # Trouver la session la plus récente
            session_dirs = [d for d in self.colab_results_dir.iterdir() if d.is_dir()]
            if not session_dirs:
                return None
            
            latest_session = max(session_dirs, key=lambda x: x.stat().st_mtime)
            
            # Vérifier si nouvelle par rapport à la dernière connue
            if self.stats['last_colab_result'] == str(latest_session):
                return None
            
            # Lire métadonnées de la session
            metadata_file = latest_session / "session_metadata.json"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                
                # Lire analyse dhātu
                analysis_files = list(latest_session.glob("dhatu_analysis_*.json"))
                if analysis_files:
                    with open(analysis_files[0], 'r') as f:
                        analysis = json.load(f)
                    
                    result = {
                        'session_dir': str(latest_session),
                        'session_id': metadata.get('session_id'),
                        'timestamp': metadata.get('imported_at'),
                        'analysis': analysis
                    }
                    
                    self.stats['last_colab_result'] = str(latest_session)
                    self.stats['colab_sessions_detected'] += 1
                    
                    return result
            
            return None
            
        except Exception as e:
            logger.error(f"Erreur détection Colab: {e}")
            return None
    
    def analyze_corpus_quality(self) -> Dict[str, Any]:
        """Analyse la qualité du corpus collecté"""
        try:
            batch_files = list(self.corpus_dir.glob("intelligent_batch_*.json"))
            if not batch_files:
                return {'batch_count': 0, 'total_docs': 0, 'avg_quality': 0.0}
            
            total_docs = 0
            total_quality = 0.0
            domain_distribution = {}
            recent_batches = []
            
            for batch_file in batch_files:
                try:
                    with open(batch_file, 'r') as f:
                        batch_data = json.load(f)
                    
                    metadata = batch_data.get('metadata', {})
                    docs_count = metadata.get('document_count', 0)
                    avg_potential = metadata.get('average_dhatu_potential', 0.0)
                    
                    total_docs += docs_count
                    total_quality += avg_potential * docs_count
                    
                    # Distribution des domaines
                    for domain in metadata.get('domains', []):
                        domain_distribution[domain] = domain_distribution.get(domain, 0) + 1
                    
                    # Batches récents (dernières 24h)
                    batch_time = datetime.fromisoformat(metadata.get('timestamp', '2020-01-01_00:00:00').replace('_', 'T'))
                    if batch_time > datetime.now() - timedelta(hours=24):
                        recent_batches.append({
                            'batch_number': metadata.get('batch_number'),
                            'timestamp': metadata.get('timestamp'),
                            'document_count': docs_count,
                            'quality': avg_potential
                        })
                
                except Exception as e:
                    logger.warning(f"Erreur lecture batch {batch_file}: {e}")
                    continue
            
            avg_quality = total_quality / total_docs if total_docs > 0 else 0.0
            
            return {
                'batch_count': len(batch_files),
                'total_docs': total_docs,
                'avg_quality': avg_quality,
                'domain_distribution': domain_distribution,
                'recent_batches': recent_batches
            }
            
        except Exception as e:
            logger.error(f"Erreur analyse corpus: {e}")
            return {'batch_count': 0, 'total_docs': 0, 'avg_quality': 0.0}
    
    def optimize_collector_based_on_colab(self, colab_result: Dict[str, Any], corpus_analysis: Dict[str, Any]):
        """Optimise le collecteur basé sur les résultats Colab"""
        try:
            analysis = colab_result.get('analysis', {})
            dhatu_analysis = analysis.get('dhatu_analysis', {})
            
            # Extraire insights clés
            dominant_dhatu = dhatu_analysis.get('dominant_dhatu', '√gam')
            confidence_score = dhatu_analysis.get('confidence_score', 0.5)
            patterns_detected = dhatu_analysis.get('patterns_detected', 0)
            
            # Suggestions d'optimisation
            optimizations = []
            
            if confidence_score > 0.8:
                optimizations.append("🎯 Confidence élevée détectée - augmenter rate limit collecteur")
            
            if patterns_detected > 7:
                optimizations.append("🧠 Patterns riches - focus sur domaines linguistiques")
            
            if dominant_dhatu and '√gam' in dominant_dhatu:
                optimizations.append("🚶 Dhātu mouvement dominant - prioriser textes with movement verbs")
            
            corpus_quality = corpus_analysis.get('avg_quality', 0.0)
            if corpus_quality < 0.5:
                optimizations.append("📈 Qualité corpus à améliorer - augmenter seuil qualité")
            
            # Créer fichier de configuration pour le collecteur
            config = {
                'timestamp': datetime.now().isoformat(),
                'colab_insights': {
                    'dominant_dhatu': dominant_dhatu,
                    'confidence_score': confidence_score,
                    'patterns_detected': patterns_detected
                },
                'corpus_analysis': corpus_analysis,
                'optimizations': optimizations,
                'recommended_settings': {
                    'quality_threshold': max(0.4, corpus_quality * 1.2),
                    'rate_limit': 1.0 if confidence_score > 0.8 else 1.5,
                    'focus_domains': ['linguistics', 'sanskrit_studies', 'cognitive_science'] if '√gam' in dominant_dhatu else ['general']
                }
            }
            
            config_file = self.corpus_dir / "collector_optimization.json"
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            logger.info(f"🎯 Configuration collecteur optimisée basée sur Colab")
            for opt in optimizations:
                logger.info(f"   {opt}")
            
            self.stats['quality_improvements'] += 1
            return True
            
        except Exception as e:
            logger.error(f"Erreur optimisation: {e}")
            return False
    
    def sync_with_github(self) -> bool:
        """Synchronisation GitHub"""
        try:
            subprocess.run(['git', 'pull', 'origin', 'main'], 
                         cwd=self.base_dir, check=True, capture_output=True)
            
            # Vérifier s'il y a des nouveaux fichiers à pousser
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  cwd=self.base_dir, capture_output=True, text=True)
            
            if result.stdout.strip():
                subprocess.run(['git', 'add', '.'], 
                             cwd=self.base_dir, check=True, capture_output=True)
                
                commit_msg = f"🔄 Auto-sync coordination - {datetime.now().strftime('%H:%M:%S')}"
                subprocess.run(['git', 'commit', '-m', commit_msg], 
                             cwd=self.base_dir, check=True, capture_output=True)
                
                subprocess.run(['git', 'push', 'origin', 'main'], 
                             cwd=self.base_dir, check=True, capture_output=True)
                
                self.stats['github_syncs'] += 1
                logger.info("🔄 GitHub sync réussi avec nouveaux fichiers")
                return True
            else:
                logger.debug("🔄 GitHub sync - rien à pousser")
                return True
                
        except subprocess.CalledProcessError as e:
            logger.warning(f"Git sync failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Git error: {e}")
            return False
    
    def monitor_collector_health(self) -> Dict[str, Any]:
        """Surveille la santé du collecteur"""
        try:
            # Vérifier si le processus collecteur tourne
            result = subprocess.run(['pgrep', '-f', 'intelligent_corpus_collector'], 
                                  capture_output=True, text=True)
            
            collector_running = bool(result.stdout.strip())
            
            # Analyser logs récents
            log_file = self.base_dir / "logs" / "intelligent_collector.log"
            recent_activity = False
            last_activity = None
            
            if log_file.exists():
                # Lire dernières lignes
                result = subprocess.run(['tail', '-10', str(log_file)], 
                                      capture_output=True, text=True)
                
                if result.stdout:
                    lines = result.stdout.strip().split('\n')
                    for line in reversed(lines):
                        if 'Document' in line and 'Q:' in line:
                            recent_activity = True
                            last_activity = line.strip()
                            break
            
            health = {
                'collector_running': collector_running,
                'recent_activity': recent_activity,
                'last_activity': last_activity,
                'timestamp': datetime.now().isoformat()
            }
            
            return health
            
        except Exception as e:
            logger.error(f"Erreur monitoring collecteur: {e}")
            return {'collector_running': False, 'recent_activity': False}
    
    def run_coordination_cycle(self, max_hours: float = 4.0):
        """Lance cycle de coordination continu"""
        
        logger.info("🔄 DÉMARRAGE COORDINATION INTELLIGENTE")
        logger.info(f"⏰ Durée maximale: {max_hours} heures")
        logger.info("🎯 Optimisation continue Colab ↔ Collecteur")
        logger.info("=" * 60)
        
        start_time = time.time()
        max_duration = max_hours * 3600
        last_optimization = 0
        
        try:
            while (time.time() - start_time) < max_duration:
                
                # Détecter activité Colab
                colab_result = self.detect_colab_activity()
                if colab_result:
                    logger.info(f"🔬 Nouvelle session Colab détectée: {colab_result['session_id']}")
                    
                    # Analyser corpus actuel
                    corpus_analysis = self.analyze_corpus_quality()
                    logger.info(f"📊 Corpus: {corpus_analysis['total_docs']} docs, qualité {corpus_analysis['avg_quality']:.3f}")
                    
                    # Optimiser collecteur
                    self.optimize_collector_based_on_colab(colab_result, corpus_analysis)
                    last_optimization = time.time()
                
                # Monitoring périodique
                collector_health = self.monitor_collector_health()
                
                # Synchronisation GitHub
                if (time.time() - start_time) % 300 < 30:  # Toutes les 5 minutes
                    self.sync_with_github()
                
                # Rapport périodique
                if int(time.time() - start_time) % 600 == 0:  # Toutes les 10 minutes
                    elapsed = time.time() - start_time
                    corpus_analysis = self.analyze_corpus_quality()
                    
                    logger.info(f"📊 Coordination Status ({elapsed/60:.1f}min):")
                    logger.info(f"   🔬 Sessions Colab: {self.stats['colab_sessions_detected']}")
                    logger.info(f"   📄 Corpus docs: {corpus_analysis['total_docs']}")
                    logger.info(f"   🎯 Optimisations: {self.stats['quality_improvements']}")
                    logger.info(f"   🔄 Syncs GitHub: {self.stats['github_syncs']}")
                    logger.info(f"   🤖 Collecteur: {'🟢' if collector_health['collector_running'] else '🔴'}")
                
                time.sleep(30)  # Check toutes les 30 secondes
        
        except KeyboardInterrupt:
            logger.info("⚠️ Coordination interrompue par utilisateur")
        except Exception as e:
            logger.error(f"Erreur coordination: {e}")
        
        # Rapport final
        total_time = time.time() - start_time
        final_corpus = self.analyze_corpus_quality()
        
        logger.info("🎯 COORDINATION TERMINÉE")
        logger.info(f"⏱️ Durée: {total_time/60:.1f} minutes")
        logger.info(f"🔬 Sessions Colab: {self.stats['colab_sessions_detected']}")
        logger.info(f"📄 Corpus final: {final_corpus['total_docs']} docs (Q:{final_corpus['avg_quality']:.3f})")
        logger.info(f"🎯 Optimisations appliquées: {self.stats['quality_improvements']}")

def main():
    """Point d'entrée principal"""
    
    print("🔄 INTELLIGENT RESEARCH COORDINATOR")
    print("🧠 Coordination Colab Pro ↔ Collecteur Intelligent")
    print("=" * 60)
    print("🎯 Optimisation continue basée sur résultats en temps réel")
    print()
    
    coordinator = IntelligentResearchCoordinator()
    
    try:
        coordinator.run_coordination_cycle(max_hours=4.0)
        
    except KeyboardInterrupt:
        print("\n⚠️ Coordination interrompue")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        logger.exception("Erreur détaillée:")

if __name__ == "__main__":
    main()