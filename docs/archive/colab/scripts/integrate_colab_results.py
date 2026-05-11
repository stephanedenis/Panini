#!/usr/bin/env python3
"""
Intégrateur résultats Colab dans système local
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import requests

sys.path.append(str(Path(__file__).parent.parent))
from src.cloud.integration_manager import IntegrationManager, JobStatus

class ColabResultsIntegrator:
    def __init__(self):
        self.manager = IntegrationManager()
        self.results_dir = Path("colab_integration/results")
        
    def scan_colab_results(self):
        """Scan résultats Colab récents"""
        sessions = []
        
        if not self.results_dir.exists():
            print("❌ Dossier résultats Colab non trouvé")
            return sessions
        
        for session_dir in self.results_dir.iterdir():
            if session_dir.is_dir():
                metadata_file = session_dir / "session_metadata.json"
                if metadata_file.exists():
                    try:
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                        sessions.append({
                            'session_id': metadata['session_id'],
                            'path': session_dir,
                            'metadata': metadata
                        })
                    except Exception as e:
                        print(f"❌ Erreur lecture {session_dir}: {e}")
        
        return sorted(sessions, key=lambda x: x['metadata']['timestamp'], reverse=True)
    
    def integrate_session(self, session):
        """Intègre une session Colab dans le système local"""
        session_id = session['session_id']
        metadata = session['metadata']
        
        print(f"🔗 Intégration session {session_id}...")
        
        # Créer job dans système local pour traçabilité
        job_id = self.manager.create_job(
            job_type="dhatu_analysis",
            notebook_path="colab_integration/notebooks/panini_github_colab_integration.ipynb",
            input_data={
                "corpus_size": metadata['corpus_stats']['total_documents'],
                "colab_session": session_id
            },
            config={
                "gpu": metadata['gpu_info']['device_name'],
                "source": "colab_gpu"
            }
        )
        
        # Marquer comme terminé avec résultats Colab
        self.manager.update_job_status(
            job_id,
            JobStatus.COMPLETED,
            output_data={
                "dhatu_statistics": metadata['dhatu_statistics'],
                "execution_time": metadata['corpus_stats']['analysis_time'],
                "throughput": metadata['corpus_stats']['throughput'],
                "colab_session_id": session_id,
                "results_path": str(session['path'])
            }
        )
        
        # Ajouter métriques
        self.manager.add_metrics(job_id, "colab_gpu_performance", {
            "execution_time": metadata['corpus_stats']['analysis_time'],
            "throughput": metadata['corpus_stats']['throughput'],
            "gpu_memory": metadata['gpu_info']['memory_total'],
            "documents_processed": metadata['corpus_stats']['total_documents']
        })
        
        print(f"✅ Session {session_id} intégrée (Job ID: {job_id})")
        return job_id
    
    def sync_all(self):
        """Synchronise tous les résultats Colab récents"""
        sessions = self.scan_colab_results()
        
        print(f"📊 {len(sessions)} sessions Colab trouvées")
        
        integrated = 0
        for session in sessions[:5]:  # Limiter aux 5 plus récentes
            try:
                self.integrate_session(session)
                integrated += 1
            except Exception as e:
                print(f"❌ Erreur intégration {session['session_id']}: {e}")
        
        print(f"✅ {integrated} sessions intégrées")
        return integrated

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--sync", action="store_true", help="Synchroniser tous les résultats")
    args = parser.parse_args()
    
    integrator = ColabResultsIntegrator()
    
    if args.sync:
        integrator.sync_all()
    else:
        sessions = integrator.scan_colab_results()
        print(f"📊 {len(sessions)} sessions disponibles")
        for session in sessions[:3]:
            print(f"  🧬 {session['session_id']}: {session['metadata']['corpus_stats']['total_documents']} docs")
