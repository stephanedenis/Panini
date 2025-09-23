#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire d'intégration Colab Pro - Système bidirectionnel
Architecture hybride : SQLite (persistance) + Queue en mémoire (performance)
"""

import json
import sqlite3
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import uuid


class JobStatus(Enum):
    PENDING = "pending"
    QUEUED = "queued"
    UPLOADING = "uploading"
    PROCESSING = "processing"
    DOWNLOADING = "downloading"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class JobType(Enum):
    DHATU_ANALYSIS = "dhatu_analysis"
    CORPUS_COLLECTION = "corpus_collection"
    PERFORMANCE_BENCHMARK = "performance_benchmark"
    CUSTOM_NOTEBOOK = "custom_notebook"


@dataclass
class ColabJob:
    """Modèle de job Colab avec tracking complet"""
    id: str
    job_type: JobType
    status: JobStatus
    created_at: datetime
    updated_at: datetime
    
    # Configuration job
    notebook_path: str
    input_data: Dict[str, Any]
    config: Dict[str, Any]
    
    # Résultats
    output_data: Optional[Dict[str, Any]] = None
    results_path: Optional[str] = None
    error_message: Optional[str] = None
    
    # Métriques
    execution_time: Optional[float] = None
    gpu_usage: Optional[Dict[str, Any]] = None
    memory_usage: Optional[Dict[str, Any]] = None
    cost_estimate: Optional[float] = None
    
    # URLs et références
    colab_url: Optional[str] = None
    notebook_id: Optional[str] = None
    drive_folder: Optional[str] = None


class IntegrationManager:
    """Gestionnaire principal d'intégration Colab Pro"""
    
    def __init__(self, db_path: str = "data/integration.db", 
                 workspace_path: str = "."):
        self.db_path = Path(db_path)
        self.workspace_path = Path(workspace_path)
        self.job_queue = asyncio.Queue()
        self.active_jobs = {}
        self.results_cache = {}
        
        # Configuration logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Initialiser base de données
        self._init_database()
        
    def _init_database(self):
        """Initialise la base de données SQLite"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    id TEXT PRIMARY KEY,
                    job_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL,
                    notebook_path TEXT NOT NULL,
                    input_data TEXT,
                    config TEXT,
                    output_data TEXT,
                    results_path TEXT,
                    error_message TEXT,
                    execution_time REAL,
                    gpu_usage TEXT,
                    memory_usage TEXT,
                    cost_estimate REAL,
                    colab_url TEXT,
                    notebook_id TEXT,
                    drive_folder TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id TEXT NOT NULL,
                    timestamp TIMESTAMP NOT NULL,
                    metric_type TEXT NOT NULL,
                    metric_data TEXT NOT NULL,
                    FOREIGN KEY (job_id) REFERENCES jobs (id)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS corpus_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id TEXT NOT NULL,
                    source_url TEXT,
                    content_type TEXT,
                    language TEXT,
                    dhatu_signature TEXT,
                    processed_at TIMESTAMP NOT NULL,
                    file_path TEXT,
                    metadata TEXT,
                    FOREIGN KEY (job_id) REFERENCES jobs (id)
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_jobs_type ON jobs(job_type)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_metrics_job_id ON metrics(job_id)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_corpus_job_id ON corpus_entries(job_id)
            """)
            
    def create_job(self, job_type: JobType, notebook_path: str, 
                   input_data: Dict[str, Any], config: Dict[str, Any] = None) -> str:
        """Crée un nouveau job Colab"""
        
        job_id = str(uuid.uuid4())
        now = datetime.now()
        
        job = ColabJob(
            id=job_id,
            job_type=job_type,
            status=JobStatus.PENDING,
            created_at=now,
            updated_at=now,
            notebook_path=notebook_path,
            input_data=input_data,
            config=config or {}
        )
        
        # Sauvegarder en BDD
        self._save_job(job)
        
        # Ajouter à la queue
        asyncio.create_task(self.job_queue.put(job))
        
        self.logger.info(f"Job créé : {job_id} ({job_type.value})")
        return job_id
    
    def _save_job(self, job: ColabJob):
        """Sauvegarde un job en base de données"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO jobs VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            """, (
                job.id, job.job_type.value, job.status.value,
                job.created_at, job.updated_at, job.notebook_path,
                json.dumps(job.input_data), json.dumps(job.config),
                json.dumps(job.output_data) if job.output_data else None,
                job.results_path, job.error_message, job.execution_time,
                json.dumps(job.gpu_usage) if job.gpu_usage else None,
                json.dumps(job.memory_usage) if job.memory_usage else None,
                job.cost_estimate, job.colab_url, job.notebook_id, job.drive_folder
            ))
    
    def get_job(self, job_id: str) -> Optional[ColabJob]:
        """Récupère un job par ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
            
            if not row:
                return None
                
            return ColabJob(
                id=row['id'],
                job_type=JobType(row['job_type']),
                status=JobStatus(row['status']),
                created_at=datetime.fromisoformat(row['created_at']),
                updated_at=datetime.fromisoformat(row['updated_at']),
                notebook_path=row['notebook_path'],
                input_data=json.loads(row['input_data']) if row['input_data'] else {},
                config=json.loads(row['config']) if row['config'] else {},
                output_data=json.loads(row['output_data']) if row['output_data'] else None,
                results_path=row['results_path'],
                error_message=row['error_message'],
                execution_time=row['execution_time'],
                gpu_usage=json.loads(row['gpu_usage']) if row['gpu_usage'] else None,
                memory_usage=json.loads(row['memory_usage']) if row['memory_usage'] else None,
                cost_estimate=row['cost_estimate'],
                colab_url=row['colab_url'],
                notebook_id=row['notebook_id'],
                drive_folder=row['drive_folder']
            )
    
    def update_job_status(self, job_id: str, status: JobStatus, 
                         output_data: Dict[str, Any] = None, error_message: str = None):
        """Met à jour le statut d'un job"""
        job = self.get_job(job_id)
        if not job:
            self.logger.error(f"Job non trouvé : {job_id}")
            return
            
        job.status = status
        job.updated_at = datetime.now()
        
        if output_data:
            job.output_data = output_data
            
        if error_message:
            job.error_message = error_message
            
        self._save_job(job)
        self.logger.info(f"Job {job_id} : {status.value}")
    
    def get_jobs_by_status(self, status: JobStatus) -> List[ColabJob]:
        """Récupère tous les jobs d'un statut donné"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("SELECT * FROM jobs WHERE status = ? ORDER BY created_at DESC", 
                              (status.value,)).fetchall()
            
            jobs = []
            for row in rows:
                job = self.get_job(row['id'])
                if job:
                    jobs.append(job)
                    
            return jobs
    
    def add_metrics(self, job_id: str, metric_type: str, metric_data: Dict[str, Any]):
        """Ajoute des métriques pour un job"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO metrics (job_id, timestamp, metric_type, metric_data)
                VALUES (?, ?, ?, ?)
            """, (job_id, datetime.now(), metric_type, json.dumps(metric_data)))
    
    def get_metrics(self, job_id: str, metric_type: str = None) -> List[Dict[str, Any]]:
        """Récupère les métriques d'un job"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            query = "SELECT * FROM metrics WHERE job_id = ?"
            params = [job_id]
            
            if metric_type:
                query += " AND metric_type = ?"
                params.append(metric_type)
                
            query += " ORDER BY timestamp DESC"
            
            rows = conn.execute(query, params).fetchall()
            
            return [{
                'timestamp': row['timestamp'],
                'metric_type': row['metric_type'],
                'metric_data': json.loads(row['metric_data'])
            } for row in rows]
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Données pour dashboard temps réel"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            # Statistiques globales
            stats = conn.execute("""
                SELECT 
                    status,
                    COUNT(*) as count,
                    AVG(execution_time) as avg_execution_time,
                    SUM(cost_estimate) as total_cost
                FROM jobs 
                GROUP BY status
            """).fetchall()
            
            # Jobs récents
            recent_jobs = conn.execute("""
                SELECT * FROM jobs 
                ORDER BY updated_at DESC 
                LIMIT 10
            """).fetchall()
            
            # Métriques GPU récentes
            gpu_metrics = conn.execute("""
                SELECT m.* FROM metrics m
                JOIN jobs j ON m.job_id = j.id
                WHERE m.metric_type = 'gpu_usage'
                ORDER BY m.timestamp DESC
                LIMIT 20
            """).fetchall()
            
            return {
                'stats': [dict(row) for row in stats],
                'recent_jobs': [dict(row) for row in recent_jobs],
                'gpu_metrics': [dict(row) for row in gpu_metrics],
                'queue_size': self.job_queue.qsize(),
                'active_jobs': len(self.active_jobs)
            }
    
    async def job_processor(self):
        """Processeur principal de la queue de jobs"""
        while True:
            try:
                job = await self.job_queue.get()
                self.logger.info(f"Traitement job : {job.id}")
                
                # Ajouter aux jobs actifs
                self.active_jobs[job.id] = job
                
                # Mettre à jour statut
                self.update_job_status(job.id, JobStatus.QUEUED)
                
                # Traiter selon le type
                if job.job_type == JobType.DHATU_ANALYSIS:
                    await self._process_dhatu_analysis(job)
                elif job.job_type == JobType.CORPUS_COLLECTION:
                    await self._process_corpus_collection(job)
                elif job.job_type == JobType.PERFORMANCE_BENCHMARK:
                    await self._process_performance_benchmark(job)
                else:
                    await self._process_custom_notebook(job)
                
                # Retirer des jobs actifs
                if job.id in self.active_jobs:
                    del self.active_jobs[job.id]
                    
                self.job_queue.task_done()
                
            except Exception as e:
                self.logger.error(f"Erreur traitement job : {e}")
                if job.id in self.active_jobs:
                    self.update_job_status(job.id, JobStatus.FAILED, 
                                         error_message=str(e))
                    del self.active_jobs[job.id]
    
    async def _process_dhatu_analysis(self, job: ColabJob):
        """Traite un job d'analyse dhātu"""
        try:
            # TODO: Implémentation upload vers Colab
            self.update_job_status(job.id, JobStatus.UPLOADING)
            await asyncio.sleep(2)  # Simulation upload
            
            # TODO: Déclencher exécution notebook
            self.update_job_status(job.id, JobStatus.PROCESSING)
            await asyncio.sleep(10)  # Simulation traitement
            
            # TODO: Télécharger résultats
            self.update_job_status(job.id, JobStatus.DOWNLOADING)
            await asyncio.sleep(3)  # Simulation download
            
            # Simuler résultats
            results = {
                "dhatu_signatures": ["abc123", "def456"],
                "coverage_score": 0.85,
                "processing_time": 120.5,
                "corpus_size": 1000
            }
            
            self.update_job_status(job.id, JobStatus.COMPLETED, output_data=results)
            
        except Exception as e:
            self.update_job_status(job.id, JobStatus.FAILED, error_message=str(e))
    
    async def _process_corpus_collection(self, job: ColabJob):
        """Traite un job de collecte de corpus"""
        # TODO: Implémentation similaire
        pass
    
    async def _process_performance_benchmark(self, job: ColabJob):
        """Traite un job de benchmark performance"""
        # TODO: Implémentation similaire
        pass
        
    async def _process_custom_notebook(self, job: ColabJob):
        """Traite un notebook personnalisé"""
        # TODO: Implémentation similaire
        pass

# API de convenance
class ColabIntegrationAPI:
    """API simplifiée pour intégration Colab"""
    
    def __init__(self, manager: IntegrationManager):
        self.manager = manager
    
    def submit_dhatu_analysis(self, corpus_path: str, config: Dict[str, Any] = None) -> str:
        """Soumet une analyse dhātu"""
        return self.manager.create_job(
            JobType.DHATU_ANALYSIS,
            "colab_notebooks/panini_dhatu_analysis.ipynb",
            {"corpus_path": corpus_path},
            config or {}
        )
    
    def submit_corpus_collection(self, sources: List[str], languages: List[str], 
                                target_count: int = 1000) -> str:
        """Soumet une collecte de corpus"""
        return self.manager.create_job(
            JobType.CORPUS_COLLECTION,
            "colab_notebooks/panini_corpus_collection.ipynb",
            {
                "sources": sources,
                "languages": languages,
                "target_count": target_count
            }
        )
    
    def submit_performance_benchmark(self, test_config: Dict[str, Any]) -> str:
        """Soumet un benchmark performance"""
        return self.manager.create_job(
            JobType.PERFORMANCE_BENCHMARK,
            "colab_notebooks/panini_performance_benchmark.ipynb",
            test_config
        )
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Récupère le statut d'un job"""
        job = self.manager.get_job(job_id)
        if not job:
            return {"error": "Job non trouvé"}
            
        return {
            "id": job.id,
            "status": job.status.value,
            "progress": self._calculate_progress(job),
            "results": job.output_data,
            "error": job.error_message,
            "created_at": job.created_at.isoformat(),
            "updated_at": job.updated_at.isoformat()
        }
    
    def _calculate_progress(self, job: ColabJob) -> float:
        """Calcule le pourcentage de progression"""
        status_progress = {
            JobStatus.PENDING: 0.0,
            JobStatus.QUEUED: 0.1,
            JobStatus.UPLOADING: 0.2,
            JobStatus.PROCESSING: 0.6,
            JobStatus.DOWNLOADING: 0.9,
            JobStatus.COMPLETED: 1.0,
            JobStatus.FAILED: 0.0,
            JobStatus.CANCELLED: 0.0
        }
        return status_progress.get(job.status, 0.0)
    
    def download_results(self, job_id: str, output_path: str) -> bool:
        """Télécharge les résultats d'un job"""
        job = self.manager.get_job(job_id)
        if not job or job.status != JobStatus.COMPLETED:
            return False
            
        # TODO: Implémentation téléchargement
        return True
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Données pour dashboard"""
        return self.manager.get_dashboard_data()

if __name__ == "__main__":
    # Test rapide
    async def test_integration():
        manager = IntegrationManager()
        api = ColabIntegrationAPI(manager)
        
        # Démarrer processeur
        processor_task = asyncio.create_task(manager.job_processor())
        
        # Soumettre job test
        job_id = api.submit_dhatu_analysis("data/corpus/test.json")
        print(f"Job soumis : {job_id}")
        
        # Attendre quelques secondes
        await asyncio.sleep(20)
        
        # Vérifier statut
        status = api.get_job_status(job_id)
        print(f"Statut : {status}")
        
        processor_task.cancel()
    
    asyncio.run(test_integration())