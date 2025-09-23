#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API REST Flask pour intégration Colab Pro
Endpoints pour communication bidirectionnelle local ↔ Colab
"""

from flask import Flask, request, jsonify, send_file
from flask_socketio import SocketIO, emit
import logging
import sys
from pathlib import Path
from typing import Dict, Any

# Ajout du path pour imports locaux
sys.path.append(str(Path(__file__).parent.parent.parent))

# Import des modules d'intégration
from src.cloud.integration_manager import (
    IntegrationManager, ColabIntegrationAPI, JobStatus
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'colab-integration-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Configuration globale
integration_manager = IntegrationManager()
colab_api = ColabIntegrationAPI(integration_manager)

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/health', methods=['GET'])
def health_check():
    """Vérification santé API"""
    return jsonify({
        'status': 'healthy',
        'integration_manager': 'ready',
        'queue_size': integration_manager.job_queue.qsize(),
        'active_jobs': len(integration_manager.active_jobs)
    })


@app.route('/api/jobs', methods=['POST'])
def submit_job():
    """Soumet un nouveau job Colab"""
    try:
        data = request.get_json()
        
        # Validation données
        if not data or 'job_type' not in data:
            return jsonify({'error': 'job_type requis'}), 400
            
        job_type = data['job_type']
        
        # Router selon le type de job
        if job_type == 'dhatu_analysis':
            if 'corpus_path' not in data:
                return jsonify({'error': 'corpus_path requis'}), 400
                
            job_id = colab_api.submit_dhatu_analysis(
                data['corpus_path'],
                data.get('config', {})
            )
            
        elif job_type == 'corpus_collection':
            if not all(k in data for k in ['sources', 'languages']):
                return jsonify({
                    'error': 'sources et languages requis'
                }), 400
                
            job_id = colab_api.submit_corpus_collection(
                data['sources'],
                data['languages'],
                data.get('target_count', 1000)
            )
            
        elif job_type == 'performance_benchmark':
            if 'test_config' not in data:
                return jsonify({'error': 'test_config requis'}), 400
                
            job_id = colab_api.submit_performance_benchmark(
                data['test_config']
            )
            
        else:
            return jsonify({'error': 'Type de job non supporté'}), 400
        
        # Notifier via WebSocket
        socketio.emit('job_submitted', {
            'job_id': job_id,
            'job_type': job_type
        })
        
        return jsonify({
            'job_id': job_id,
            'status': 'submitted',
            'message': f'Job {job_type} soumis avec succès'
        })
        
    except Exception as e:
        logger.error(f"Erreur soumission job : {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/jobs/<job_id>', methods=['GET'])
def get_job_status(job_id):
    """Récupère le statut d'un job"""
    try:
        status = colab_api.get_job_status(job_id)
        
        if 'error' in status:
            return jsonify(status), 404
            
        return jsonify(status)
        
    except Exception as e:
        logger.error(f"Erreur récupération statut {job_id} : {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/jobs', methods=['GET'])
def list_jobs():
    """Liste tous les jobs avec filtres"""
    try:
        status_filter = request.args.get('status')
        limit = int(request.args.get('limit', 20))
        
        # Récupérer jobs depuis la BDD
        if status_filter:
            try:
                status_enum = JobStatus(status_filter)
                jobs = integration_manager.get_jobs_by_status(status_enum)
            except ValueError:
                return jsonify({'error': 'Statut invalide'}), 400
        else:
            # Récupérer tous les jobs récents
            jobs = []
            for status in JobStatus:
                jobs.extend(integration_manager.get_jobs_by_status(status))
        
        # Limiter et formater
        jobs = sorted(jobs, key=lambda x: x.updated_at, reverse=True)[:limit]
        
        formatted_jobs = []
        for job in jobs:
            formatted_jobs.append({
                'id': job.id,
                'job_type': job.job_type.value,
                'status': job.status.value,
                'created_at': job.created_at.isoformat(),
                'updated_at': job.updated_at.isoformat(),
                'execution_time': job.execution_time,
                'error_message': job.error_message
            })
        
        return jsonify({
            'jobs': formatted_jobs,
            'total': len(formatted_jobs)
        })
        
    except Exception as e:
        logger.error(f"Erreur liste jobs : {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/jobs/<job_id>/results', methods=['GET'])
def download_results(job_id):
    """Télécharge les résultats d'un job"""
    try:
        job = integration_manager.get_job(job_id)
        
        if not job:
            return jsonify({'error': 'Job non trouvé'}), 404
            
        if job.status != JobStatus.COMPLETED:
            return jsonify({
                'error': 'Job non terminé',
                'status': job.status.value
            }), 400
        
        if job.results_path and Path(job.results_path).exists():
            return send_file(job.results_path, as_attachment=True)
        else:
            # Retourner données JSON si pas de fichier
            return jsonify({
                'job_id': job_id,
                'results': job.output_data,
                'download_time': job.updated_at.isoformat()
            })
        
    except Exception as e:
        logger.error(f"Erreur téléchargement résultats {job_id} : {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/jobs/<job_id>/cancel', methods=['POST'])
def cancel_job(job_id):
    """Annule un job"""
    try:
        integration_manager.update_job_status(
            job_id, 
            JobStatus.CANCELLED,
            error_message="Job annulé par l'utilisateur"
        )
        
        # Notifier via WebSocket
        socketio.emit('job_cancelled', {'job_id': job_id})
        
        return jsonify({
            'job_id': job_id,
            'status': 'cancelled',
            'message': 'Job annulé avec succès'
        })
        
    except Exception as e:
        logger.error(f"Erreur annulation job {job_id} : {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/dashboard', methods=['GET'])
def dashboard_data():
    """Données pour dashboard temps réel"""
    try:
        data = colab_api.get_dashboard_data()
        
        # Ajouter métriques système
        data['system_info'] = {
            'api_version': '1.0.0',
            'uptime': 'TODO',  # À implémenter
            'memory_usage': 'TODO'  # À implémenter
        }
        
        return jsonify(data)
        
    except Exception as e:
        logger.error(f"Erreur données dashboard : {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/metrics/<job_id>', methods=['GET'])
def get_job_metrics(job_id):
    """Récupère les métriques d'un job"""
    try:
        metric_type = request.args.get('type')
        metrics = integration_manager.get_metrics(job_id, metric_type)
        
        return jsonify({
            'job_id': job_id,
            'metrics': metrics,
            'count': len(metrics)
        })
        
    except Exception as e:
        logger.error(f"Erreur métriques job {job_id} : {e}")
        return jsonify({'error': str(e)}), 500


# WebSocket Events pour temps réel
@socketio.on('connect')
def handle_connect():
    """Client connecté"""
    logger.info('Client connecté au WebSocket')
    emit('connected', {'message': 'Connexion WebSocket établie'})


@socketio.on('subscribe_job')
def handle_job_subscription(data):
    """S'abonner aux mises à jour d'un job"""
    job_id = data.get('job_id')
    if job_id:
        logger.info(f'Client abonné au job : {job_id}')
        emit('subscribed', {'job_id': job_id})


@socketio.on('subscribe_dashboard')
def handle_dashboard_subscription():
    """S'abonner aux mises à jour du dashboard"""
    logger.info('Client abonné au dashboard')
    emit('dashboard_subscribed', {'message': 'Abonné aux mises à jour'})


def notify_job_update(job_id: str, status: str, data: Dict[str, Any] = None):
    """Notifier mise à jour job via WebSocket"""
    socketio.emit('job_update', {
        'job_id': job_id,
        'status': status,
        'data': data or {},
        'timestamp': str(datetime.now())
    })


def notify_dashboard_update():
    """Notifier mise à jour dashboard"""
    try:
        data = colab_api.get_dashboard_data()
        socketio.emit('dashboard_update', data)
    except Exception as e:
        logger.error(f"Erreur notification dashboard : {e}")


# Tâche périodique pour notifications temps réel
import threading
import time
from datetime import datetime


def periodic_notifications():
    """Tâche périodique pour notifications dashboard"""
    while True:
        try:
            time.sleep(10)  # Toutes les 10 secondes
            notify_dashboard_update()
        except Exception as e:
            logger.error(f"Erreur notifications périodiques : {e}")


# Démarrer tâche en arrière-plan
notification_thread = threading.Thread(
    target=periodic_notifications, 
    daemon=True
)


if __name__ == '__main__':
    # Démarrer processeur de jobs
    import asyncio
    
    def start_job_processor():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(integration_manager.job_processor())
    
    job_processor_thread = threading.Thread(
        target=start_job_processor,
        daemon=True
    )
    job_processor_thread.start()
    
    # Démarrer notifications
    notification_thread.start()
    
    # Démarrer serveur Flask
    logger.info("Démarrage API d'intégration Colab Pro...")
    logger.info("API disponible sur http://localhost:5000")
    logger.info("Documentation endpoints : /health, /api/jobs, /api/dashboard")
    
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=False,
        allow_unsafe_werkzeug=True
    )