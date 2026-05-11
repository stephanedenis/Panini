#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test complet de l'architecture d'intégration Colab Pro
Validation end-to-end : soumission, suivi, résultats
"""

import asyncio
import requests
import json
import time
import sys
from pathlib import Path
from typing import Dict, Any, List

# Configuration du test
API_BASE_URL = "http://localhost:5000"
TEST_CORPUS_PATH = "data/corpus/test_dhatu.json"


class IntegrationTester:
    """Testeur complet de l'intégration Colab"""
    
    def __init__(self, api_url: str = API_BASE_URL):
        self.api_url = api_url
        self.test_results = []
        self.jobs_created = []
        
    def log(self, message: str, status: str = "INFO"):
        """Log avec timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {status}: {message}")
        
    def test_api_health(self) -> bool:
        """Test santé de l'API"""
        self.log("Test de santé API...")
        
        try:
            response = requests.get(f"{self.api_url}/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.log(f"API opérationnelle: {data}")
                return True
            else:
                self.log(f"API erreur: {response.status_code}", "ERROR")
                return False
                
        except requests.exceptions.ConnectionError:
            self.log("API non accessible - démarrer avec: python3 src/cloud/api_rest.py", "ERROR")
            return False
        except Exception as e:
            self.log(f"Erreur santé API: {e}", "ERROR")
            return False
    
    def create_test_corpus(self):
        """Crée un corpus de test"""
        self.log("Création corpus de test...")
        
        corpus_path = Path(TEST_CORPUS_PATH)
        corpus_path.parent.mkdir(parents=True, exist_ok=True)
        
        test_corpus = {
            "metadata": {
                "name": "corpus_test_integration",
                "version": "1.0",
                "created_at": time.time(),
                "description": "Corpus test pour validation intégration Colab"
            },
            "documents": [
                {
                    "id": "test_001",
                    "language": "fr",
                    "source": "test",
                    "content": "L'analyse dhātu révèle des patterns universels dans les langues humaines.",
                    "metadata": {"type": "research"}
                },
                {
                    "id": "test_002", 
                    "language": "en",
                    "source": "test",
                    "content": "Machine learning algorithms can extract semantic primitives from natural language.",
                    "metadata": {"type": "technical"}
                },
                {
                    "id": "test_003",
                    "language": "fr",
                    "source": "test", 
                    "content": "Les transformations sémantiques préservent l'essence conceptuelle du message.",
                    "metadata": {"type": "theory"}
                }
            ]
        }
        
        with open(corpus_path, 'w', encoding='utf-8') as f:
            json.dump(test_corpus, f, indent=2, ensure_ascii=False)
            
        self.log(f"Corpus créé: {corpus_path} ({len(test_corpus['documents'])} documents)")
        return str(corpus_path)
    
    def test_job_submission(self) -> List[str]:
        """Test soumission de différents types de jobs"""
        self.log("Test soumission jobs...")
        
        corpus_path = self.create_test_corpus()
        job_ids = []
        
        # Test 1: Analyse dhātu
        dhatu_job = {
            "job_type": "dhatu_analysis",
            "corpus_path": corpus_path,
            "config": {
                "gpu": "T4",
                "max_analysis_time": 300,
                "output_format": "json"
            }
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/api/jobs",
                json=dhatu_job,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                job_id = data.get('job_id')
                job_ids.append(job_id)
                self.jobs_created.append(job_id)
                self.log(f"Job dhātu soumis: {job_id}")
            else:
                self.log(f"Erreur soumission dhātu: {response.status_code} - {response.text}", "ERROR")
                
        except Exception as e:
            self.log(f"Exception soumission dhātu: {e}", "ERROR")
        
        # Test 2: Collecte corpus
        corpus_job = {
            "job_type": "corpus_collection",
            "sources": ["wikipedia", "test"],
            "languages": ["fr", "en"],
            "target_count": 10,
            "config": {
                "max_collection_time": 600,
                "quality_filter": "medium"
            }
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/api/jobs",
                json=corpus_job,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                job_id = data.get('job_id')
                job_ids.append(job_id)
                self.jobs_created.append(job_id)
                self.log(f"Job corpus soumis: {job_id}")
            else:
                self.log(f"Erreur soumission corpus: {response.status_code} - {response.text}", "ERROR")
                
        except Exception as e:
            self.log(f"Exception soumission corpus: {e}", "ERROR")
        
        # Test 3: Benchmark performance
        benchmark_job = {
            "job_type": "performance_benchmark",
            "test_config": {
                "benchmark_type": "dhatu_analysis",
                "iterations": 5,
                "corpus_sizes": [10, 50, 100],
                "gpu_types": ["T4"]
            }
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/api/jobs",
                json=benchmark_job,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                job_id = data.get('job_id')
                job_ids.append(job_id)
                self.jobs_created.append(job_id)
                self.log(f"Job benchmark soumis: {job_id}")
            else:
                self.log(f"Erreur soumission benchmark: {response.status_code} - {response.text}", "ERROR")
                
        except Exception as e:
            self.log(f"Exception soumission benchmark: {e}", "ERROR")
        
        self.log(f"Jobs soumis: {len(job_ids)}/3")
        return job_ids
    
    def test_job_monitoring(self, job_ids: List[str], max_wait: int = 60):
        """Test monitoring des jobs"""
        self.log(f"Test monitoring {len(job_ids)} jobs (max {max_wait}s)...")
        
        start_time = time.time()
        job_statuses = {}
        
        while (time.time() - start_time) < max_wait:
            all_completed = True
            
            for job_id in job_ids:
                try:
                    response = requests.get(
                        f"{self.api_url}/api/jobs/{job_id}",
                        timeout=5
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        status = data.get('status', 'unknown')
                        progress = data.get('progress', 0.0)
                        
                        if job_id not in job_statuses or job_statuses[job_id] != status:
                            self.log(f"Job {job_id[:8]}... : {status} ({progress*100:.1f}%)")
                            job_statuses[job_id] = status
                        
                        if status not in ['completed', 'failed', 'cancelled']:
                            all_completed = False
                    else:
                        self.log(f"Erreur statut job {job_id}: {response.status_code}", "ERROR")
                        
                except Exception as e:
                    self.log(f"Exception monitoring {job_id}: {e}", "ERROR")
            
            if all_completed:
                self.log("Tous les jobs terminés!")
                break
                
            time.sleep(5)  # Attendre 5 secondes avant prochain check
        
        return job_statuses
    
    def test_dashboard_data(self):
        """Test récupération données dashboard"""
        self.log("Test données dashboard...")
        
        try:
            response = requests.get(f"{self.api_url}/api/dashboard", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                self.log(f"Stats globales: {data.get('stats', [])}")
                self.log(f"Jobs actifs: {data.get('active_jobs', 0)}")
                self.log(f"Queue size: {data.get('queue_size', 0)}")
                
                recent_jobs = data.get('recent_jobs', [])
                self.log(f"Jobs récents: {len(recent_jobs)}")
                
                return True
            else:
                self.log(f"Erreur dashboard: {response.status_code}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"Exception dashboard: {e}", "ERROR")
            return False
    
    def test_job_results(self, job_ids: List[str]):
        """Test récupération résultats"""
        self.log("Test récupération résultats...")
        
        for job_id in job_ids:
            try:
                response = requests.get(
                    f"{self.api_url}/api/jobs/{job_id}/results",
                    timeout=10
                )
                
                if response.status_code == 200:
                    if response.headers.get('content-type') == 'application/json':
                        data = response.json()
                        self.log(f"Résultats job {job_id[:8]}... : {len(str(data))} bytes")
                    else:
                        self.log(f"Fichier résultat job {job_id[:8]}... : {len(response.content)} bytes")
                elif response.status_code == 400:
                    data = response.json()
                    self.log(f"Job {job_id[:8]}... non terminé: {data.get('status', 'unknown')}")
                else:
                    self.log(f"Erreur résultats job {job_id}: {response.status_code}", "ERROR")
                    
            except Exception as e:
                self.log(f"Exception résultats {job_id}: {e}", "ERROR")
    
    def test_job_listing(self):
        """Test listage des jobs"""
        self.log("Test listage jobs...")
        
        try:
            # Test sans filtre
            response = requests.get(f"{self.api_url}/api/jobs", timeout=10)
            if response.status_code == 200:
                data = response.json()
                jobs = data.get('jobs', [])
                self.log(f"Jobs listés: {len(jobs)}")
            
            # Test avec filtre status
            response = requests.get(f"{self.api_url}/api/jobs?status=pending", timeout=10)
            if response.status_code == 200:
                data = response.json()
                pending_jobs = data.get('jobs', [])
                self.log(f"Jobs pending: {len(pending_jobs)}")
            
            # Test avec limite
            response = requests.get(f"{self.api_url}/api/jobs?limit=5", timeout=10)
            if response.status_code == 200:
                data = response.json()
                limited_jobs = data.get('jobs', [])
                self.log(f"Jobs limités: {len(limited_jobs)}")
                
            return True
            
        except Exception as e:
            self.log(f"Exception listage: {e}", "ERROR")
            return False
    
    def test_error_handling(self):
        """Test gestion d'erreurs"""
        self.log("Test gestion erreurs...")
        
        # Test job invalide
        try:
            invalid_job = {"job_type": "invalid_type"}
            response = requests.post(
                f"{self.api_url}/api/jobs",
                json=invalid_job,
                timeout=10
            )
            
            if response.status_code == 400:
                self.log("✓ Erreur job invalide correctement gérée")
            else:
                self.log(f"✗ Erreur job invalide mal gérée: {response.status_code}", "ERROR")
                
        except Exception as e:
            self.log(f"Exception test erreur: {e}", "ERROR")
        
        # Test job inexistant
        try:
            response = requests.get(
                f"{self.api_url}/api/jobs/inexistant-job-id",
                timeout=10
            )
            
            if response.status_code == 404:
                self.log("✓ Job inexistant correctement géré")
            else:
                self.log(f"✗ Job inexistant mal géré: {response.status_code}", "ERROR")
                
        except Exception as e:
            self.log(f"Exception test job inexistant: {e}", "ERROR")
    
    def cleanup_test_jobs(self):
        """Nettoie les jobs de test"""
        self.log("Nettoyage jobs de test...")
        
        for job_id in self.jobs_created:
            try:
                response = requests.post(
                    f"{self.api_url}/api/jobs/{job_id}/cancel",
                    timeout=5
                )
                
                if response.status_code == 200:
                    self.log(f"Job {job_id[:8]}... annulé")
                    
            except Exception as e:
                self.log(f"Erreur annulation {job_id}: {e}", "ERROR")
    
    def run_complete_test(self):
        """Lance tous les tests"""
        self.log("🚀 DÉBUT DES TESTS D'INTÉGRATION COLAB PRO")
        self.log("=" * 50)
        
        # 1. Test santé API
        if not self.test_api_health():
            self.log("ARRÊT: API non disponible", "ERROR")
            return False
        
        # 2. Test soumission jobs
        job_ids = self.test_job_submission()
        if not job_ids:
            self.log("ARRÊT: Aucun job soumis", "ERROR")
            return False
        
        # 3. Test monitoring
        job_statuses = self.test_job_monitoring(job_ids, max_wait=30)
        
        # 4. Test dashboard
        self.test_dashboard_data()
        
        # 5. Test listage
        self.test_job_listing()
        
        # 6. Test résultats
        self.test_job_results(job_ids)
        
        # 7. Test gestion erreurs
        self.test_error_handling()
        
        # 8. Nettoyage
        self.cleanup_test_jobs()
        
        self.log("=" * 50)
        self.log("✅ TESTS D'INTÉGRATION TERMINÉS")
        
        # Résumé
        self.log(f"Jobs créés: {len(self.jobs_created)}")
        self.log(f"Statuts finaux: {job_statuses}")
        
        return True


class QuickTest:
    """Tests rapides pour validation fonctionnelle"""
    
    @staticmethod
    def test_imports():
        """Test imports modules"""
        print("Test imports...")
        
        try:
            from src.cloud.integration_manager import IntegrationManager, ColabIntegrationAPI
            print("✓ Modules intégration importés")
            
            # Test instanciation
            manager = IntegrationManager(db_path=":memory:")
            api = ColabIntegrationAPI(manager)
            print("✓ Classes instanciées")
            
            return True
            
        except Exception as e:
            print(f"✗ Erreur import: {e}")
            return False
    
    @staticmethod
    def test_database():
        """Test base de données"""
        print("Test base de données...")
        
        try:
            from src.cloud.integration_manager import IntegrationManager, JobType
            
            manager = IntegrationManager(db_path=":memory:")
            
            # Test création job
            job_id = manager.create_job(
                JobType.DHATU_ANALYSIS,
                "test.ipynb",
                {"test": "data"}
            )
            
            # Test récupération
            job = manager.get_job(job_id)
            if job and job.id == job_id:
                print("✓ Base de données fonctionnelle")
                return True
            else:
                print("✗ Erreur récupération job")
                return False
                
        except Exception as e:
            print(f"✗ Erreur BDD: {e}")
            return False
    
    @staticmethod
    def run_quick_tests():
        """Lance tests rapides"""
        print("🔥 TESTS RAPIDES INTÉGRATION")
        print("-" * 30)
        
        tests = [
            QuickTest.test_imports,
            QuickTest.test_database
        ]
        
        results = []
        for test in tests:
            try:
                result = test()
                results.append(result)
            except Exception as e:
                print(f"✗ Exception: {e}")
                results.append(False)
        
        success_rate = sum(results) / len(results) * 100
        print(f"\nRésultat: {success_rate:.1f}% réussi")
        
        return all(results)


def main():
    """Fonction principale"""
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        return QuickTest.run_quick_tests()
    
    # Tests complets
    tester = IntegrationTester()
    return tester.run_complete_test()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)