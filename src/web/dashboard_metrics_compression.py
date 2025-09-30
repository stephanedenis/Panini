#!/usr/bin/env python3
"""
Dashboard Métriques Compression Temps Réel - Port 8889
Monitoring PaniniFS, Atomes Sémantiques et Traducteurs
"""

from flask import Flask, render_template_string, jsonify
from flask_socketio import SocketIO, emit
import json
import threading
import time
from datetime import datetime
from pathlib import Path
import logging
import sys
import signal
import os
from collections import defaultdict

app = Flask(__name__)
app.config['SECRET_KEY'] = 'panini_metrics_2025'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')


class MetricsCollector:
    """Collecteur de métriques PaniniFS et atomes sémantiques"""
    
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.running = False
        
        # Chemins des données
        self.monitoring_file = workspace / 'data' / 'monitoring_data_realtime.json'
        self.atoms_dir = workspace / 'universal_atoms_results'
        self.synthesis_dir = workspace / 'synthesis_validation_results'
        self.molecules_dir = workspace / 'molecular_patterns_results'
        
        # Métriques en cache
        self.cache = {
            'panini_fs': {},
            'semantic_atoms': {},
            'translators': {},
            'timestamp': datetime.now().isoformat()
        }
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def collect_panini_fs_metrics(self):
        """Collecte métriques PaniniFS (compression, intégrité, scalabilité)"""
        metrics = {
            'compression_by_format': {},
            'ingestion_time_ms': 0,
            'retrieval_time_ms': 0,
            'integrity_success_rate': 0.0,
            'files_count': 0,
            'total_processed': 0
        }
        
        try:
            # Chercher résultats de synthèse/validation
            if self.synthesis_dir.exists():
                synthesis_files = list(self.synthesis_dir.glob("synthesis_validation_*.json"))
                if synthesis_files:
                    latest = max(synthesis_files, key=lambda f: f.stat().st_mtime)
                    with open(latest, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                        # Extraire métriques de compression
                        if 'test_results' in data:
                            for test in data['test_results']:
                                if 'compression_ratio' in test:
                                    format_name = test.get('format', 'unknown')
                                    metrics['compression_by_format'][format_name] = round(test['compression_ratio'], 3)
                        
                        # Métriques d'intégrité
                        if 'overall_fidelity' in data:
                            metrics['integrity_success_rate'] = round(data['overall_fidelity'] * 100, 1)
                        
                        # Temps de traitement
                        if 'processing_times' in data:
                            metrics['ingestion_time_ms'] = int(data['processing_times'].get('decomposition_ms', 0))
                            metrics['retrieval_time_ms'] = int(data['processing_times'].get('recomposition_ms', 0))
                        
                        # Nombre de fichiers
                        metrics['files_count'] = len(data.get('test_results', []))
                        metrics['total_processed'] = data.get('total_texts_processed', 0)
            
            # Si pas de données de synthèse, utiliser données de monitoring
            if metrics['files_count'] == 0 and self.monitoring_file.exists():
                with open(self.monitoring_file, 'r', encoding='utf-8') as f:
                    mon_data = json.load(f)
                    latest = mon_data.get('latest', {})
                    processes = latest.get('processes', {})
                    metrics['files_count'] = len(processes)
            
        except Exception as e:
            self.logger.error(f"Erreur collecte métriques PaniniFS: {e}")
        
        return metrics
    
    def collect_semantic_atoms_metrics(self):
        """Collecte métriques atomes sémantiques (découverte, multilangue, compression)"""
        metrics = {
            'atoms_discovered': 0,
            'multilingual_languages': 0,
            'compression_per_atom': {},
            'dhatu_evolution': {
                'existing_dhatu': 0,
                'new_dhatu': 0
            },
            'atom_types': {
                'phonetic': 0,
                'morpheme': 0,
                'syntactic': 0,
                'semantic': 0
            }
        }
        
        try:
            # Charger résultats d'extraction d'atomes
            if self.atoms_dir.exists():
                atom_files = list(self.atoms_dir.glob("universal_atoms_analysis_*.json"))
                if atom_files:
                    latest = max(atom_files, key=lambda f: f.stat().st_mtime)
                    with open(latest, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                        # Nombre total d'atomes découverts
                        atom_counts = data.get('atom_counts', {})
                        metrics['atom_types']['phonetic'] = atom_counts.get('phonetic', 0)
                        metrics['atom_types']['morpheme'] = atom_counts.get('morpheme', 0)
                        metrics['atom_types']['syntactic'] = atom_counts.get('syntactic', 0)
                        metrics['atom_types']['semantic'] = atom_counts.get('semantic', 0)
                        metrics['atoms_discovered'] = sum(metrics['atom_types'].values())
                        
                        # Langues détectées
                        if 'cross_linguistic_patterns' in data:
                            languages = data['cross_linguistic_patterns'].get('languages_detected', [])
                            metrics['multilingual_languages'] = len(languages)
                        
                        # Compression par atome
                        if 'compression_efficiency' in data:
                            for atom_type, ratio in data['compression_efficiency'].items():
                                metrics['compression_per_atom'][atom_type] = round(ratio, 3)
                        
                        # Évolution dhātu
                        if 'dhatu_statistics' in data:
                            stats = data['dhatu_statistics']
                            metrics['dhatu_evolution']['existing_dhatu'] = stats.get('established_count', 0)
                            metrics['dhatu_evolution']['new_dhatu'] = stats.get('newly_discovered', 0)
            
        except Exception as e:
            self.logger.error(f"Erreur collecte métriques atomes: {e}")
        
        return metrics
    
    def collect_translator_metrics(self):
        """Collecte métriques traducteurs (identifiés, biais, patterns)"""
        metrics = {
            'translators_identified': 0,
            'biases_detected': [],
            'recurring_patterns': [],
            'translation_quality': 0.0
        }
        
        try:
            # Chercher patterns moléculaires (peuvent indiquer traductions)
            if self.molecules_dir.exists():
                molecule_files = list(self.molecules_dir.glob("molecular_patterns_report_*.json"))
                if molecule_files:
                    latest = max(molecule_files, key=lambda f: f.stat().st_mtime)
                    with open(latest, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                        # Patterns récurrents
                        if 'top_patterns' in data:
                            patterns = data['top_patterns'][:5]  # Top 5
                            for pattern in patterns:
                                if isinstance(pattern, dict):
                                    metrics['recurring_patterns'].append({
                                        'pattern': pattern.get('pattern', 'unknown'),
                                        'frequency': pattern.get('count', 0)
                                    })
                        
                        # Détection de biais (patterns asymétriques)
                        if 'asymmetry_score' in data and data['asymmetry_score'] > 0.3:
                            metrics['biases_detected'].append({
                                'type': 'structural_asymmetry',
                                'score': round(data['asymmetry_score'], 3)
                            })
                        
                        # Nombre de "traducteurs" (sources de patterns)
                        if 'pattern_sources' in data:
                            metrics['translators_identified'] = len(data['pattern_sources'])
                        
                        # Qualité de traduction (basée sur fidélité)
                        if 'pattern_fidelity' in data:
                            metrics['translation_quality'] = round(data['pattern_fidelity'] * 100, 1)
            
        except Exception as e:
            self.logger.error(f"Erreur collecte métriques traducteurs: {e}")
        
        return metrics
    
    def collect_all_metrics(self):
        """Collecte toutes les métriques"""
        self.cache['panini_fs'] = self.collect_panini_fs_metrics()
        self.cache['semantic_atoms'] = self.collect_semantic_atoms_metrics()
        self.cache['translators'] = self.collect_translator_metrics()
        self.cache['timestamp'] = datetime.now().isoformat()
        return self.cache
    
    def start_background_updates(self):
        """Démarre les mises à jour en arrière-plan"""
        def update_loop():
            while self.running:
                try:
                    # Collecte métriques
                    metrics = self.collect_all_metrics()
                    
                    # Émission WebSocket
                    socketio.emit('metrics_update', metrics)
                    
                    # Attente
                    time.sleep(5)  # Mise à jour toutes les 5 secondes
                    
                except Exception as e:
                    self.logger.error(f"Erreur mise à jour: {e}")
                    time.sleep(10)
        
        self.running = True
        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()
        self.logger.info("🔄 Mises à jour métriques démarrées")


# Instance globale
workspace_path = Path(os.environ.get('PANINI_WORKSPACE', '/home/runner/work/Panini/Panini'))
collector = MetricsCollector(workspace_path)


# Template HTML du dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🎯 Dashboard Métriques Compression Temps Réel</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #e0e0e0;
            padding: 20px;
            min-height: 100vh;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        .header h1 {
            color: #4CAF50;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .header p { color: #81C784; font-size: 1.1em; }
        .status-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 20px;
            background: rgba(76, 175, 80, 0.1);
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #4CAF50;
        }
        .status-indicator {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #4CAF50;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .card {
            background: rgba(45, 45, 45, 0.8);
            border-radius: 12px;
            padding: 25px;
            border-left: 4px solid #4CAF50;
            backdrop-filter: blur(10px);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(76, 175, 80, 0.3);
        }
        .card h3 {
            color: #4CAF50;
            margin-bottom: 20px;
            font-size: 1.4em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .metric {
            margin: 12px 0;
            padding: 12px;
            background: rgba(61, 61, 61, 0.6);
            border-radius: 6px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .metric strong { color: #81C784; }
        .metric-value {
            font-size: 1.2em;
            font-weight: bold;
            color: #FFF;
        }
        .metric-label { color: #aaa; }
        .atom-types {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-top: 10px;
        }
        .atom-type {
            padding: 10px;
            background: rgba(33, 150, 243, 0.2);
            border-radius: 6px;
            text-align: center;
        }
        .compression-format {
            padding: 8px;
            margin: 5px 0;
            background: rgba(255, 152, 0, 0.2);
            border-radius: 4px;
            border-left: 3px solid #FF9800;
        }
        .pattern-item {
            padding: 10px;
            margin: 8px 0;
            background: rgba(156, 39, 176, 0.2);
            border-radius: 6px;
            border-left: 3px solid #9C27B0;
        }
        .evolution-box {
            display: flex;
            gap: 15px;
            margin-top: 10px;
        }
        .evolution-item {
            flex: 1;
            padding: 15px;
            background: rgba(33, 150, 243, 0.2);
            border-radius: 8px;
            text-align: center;
        }
        .evolution-count {
            font-size: 2em;
            color: #2196F3;
            font-weight: bold;
        }
        .timestamp {
            text-align: center;
            color: #888;
            margin-top: 20px;
            font-size: 0.9em;
        }
        .badge {
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: bold;
        }
        .badge-success { background: #4CAF50; color: #000; }
        .badge-warning { background: #FF9800; color: #000; }
        .badge-info { background: #2196F3; color: #fff; }
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #666;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Dashboard Métriques Compression Temps Réel</h1>
            <p>Monitoring PaniniFS, Atomes Sémantiques et Traducteurs</p>
        </div>
        
        <div class="status-bar">
            <div class="status-indicator">
                <div class="status-dot"></div>
                <span><strong>Statut:</strong> Opérationnel</span>
            </div>
            <div id="last-update">Dernière mise à jour: --:--:--</div>
        </div>
        
        <!-- PaniniFS Metrics -->
        <div class="grid">
            <div class="card">
                <h3>📦 PaniniFS - Compression</h3>
                <div id="panini-compression">
                    <div class="empty-state">Chargement des données...</div>
                </div>
            </div>
            
            <div class="card">
                <h3>⚡ PaniniFS - Performance</h3>
                <div id="panini-performance">
                    <div class="empty-state">Chargement des données...</div>
                </div>
            </div>
        </div>
        
        <!-- Semantic Atoms Metrics -->
        <div class="grid">
            <div class="card">
                <h3>⚛️ Atomes Sémantiques</h3>
                <div id="atoms-stats">
                    <div class="empty-state">Chargement des données...</div>
                </div>
            </div>
            
            <div class="card">
                <h3>🌍 Validation Multilangue</h3>
                <div id="atoms-multilang">
                    <div class="empty-state">Chargement des données...</div>
                </div>
            </div>
        </div>
        
        <!-- Dhatu Evolution & Translators -->
        <div class="grid">
            <div class="card">
                <h3>🔄 Évolution Dhātu</h3>
                <div id="dhatu-evolution">
                    <div class="empty-state">Chargement des données...</div>
                </div>
            </div>
            
            <div class="card">
                <h3>🌐 Traducteurs & Patterns</h3>
                <div id="translators">
                    <div class="empty-state">Chargement des données...</div>
                </div>
            </div>
        </div>
        
        <div class="timestamp" id="timestamp">
            📡 Mise à jour automatique toutes les 5 secondes
        </div>
    </div>

    <script>
        // Utiliser polling HTTP simple au lieu de WebSocket
        let updateInterval;
        
        function fetchMetrics() {
            fetch('/api/metrics')
                .then(response => response.json())
                .then(data => updateDashboard(data))
                .catch(error => console.error('Erreur fetch métriques:', error));
        }
        
        function updateDashboard(data) {
            // Mise à jour timestamp
            const timestamp = new Date(data.timestamp).toLocaleString('fr-FR');
            document.getElementById('last-update').innerHTML = 
                `<strong>Dernière mise à jour:</strong> ${timestamp}`;
            
            // PaniniFS - Compression
            updatePaniniCompression(data.panini_fs);
            
            // PaniniFS - Performance
            updatePaniniPerformance(data.panini_fs);
            
            // Atomes sémantiques
            updateAtomsStats(data.semantic_atoms);
            updateAtomsMultilang(data.semantic_atoms);
            
            // Dhātu Evolution
            updateDhatuEvolution(data.semantic_atoms);
            
            // Traducteurs
            updateTranslators(data.translators);
        }
        
        function updatePaniniCompression(panini) {
            const formats = panini.compression_by_format || {};
            let html = '';
            
            if (Object.keys(formats).length === 0) {
                html = '<div class="empty-state">Aucune donnée de compression disponible</div>';
            } else {
                html += '<div class="metric"><span class="metric-label">Taux de compression par format:</span></div>';
                for (const [format, ratio] of Object.entries(formats)) {
                    const percentage = ((1 - 1/ratio) * 100).toFixed(1);
                    html += `
                        <div class="compression-format">
                            <strong>${format}:</strong> ${ratio}× 
                            <span class="badge badge-success">${percentage}% réduction</span>
                        </div>
                    `;
                }
            }
            
            document.getElementById('panini-compression').innerHTML = html;
        }
        
        function updatePaniniPerformance(panini) {
            const html = `
                <div class="metric">
                    <span class="metric-label">Temps ingestion:</span>
                    <span class="metric-value">${panini.ingestion_time_ms || 0} ms</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Temps restitution:</span>
                    <span class="metric-value">${panini.retrieval_time_ms || 0} ms</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Intégrité (% succès):</span>
                    <span class="metric-value">${panini.integrity_success_rate || 0}%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Scalabilité (nb fichiers):</span>
                    <span class="metric-value">${panini.files_count || 0}</span>
                </div>
            `;
            document.getElementById('panini-performance').innerHTML = html;
        }
        
        function updateAtomsStats(atoms) {
            const types = atoms.atom_types || {};
            const total = atoms.atoms_discovered || 0;
            
            let html = `
                <div class="metric">
                    <span class="metric-label">Total atomes découverts:</span>
                    <span class="metric-value">${total}</span>
                </div>
                <div class="atom-types">
            `;
            
            for (const [type, count] of Object.entries(types)) {
                html += `
                    <div class="atom-type">
                        <div style="color: #2196F3; font-weight: bold;">${count}</div>
                        <div style="font-size: 0.85em; color: #aaa;">${type}</div>
                    </div>
                `;
            }
            
            html += '</div>';
            
            // Compression per atom
            const compression = atoms.compression_per_atom || {};
            if (Object.keys(compression).length > 0) {
                html += '<div class="metric" style="margin-top: 15px;"><span class="metric-label">Compression par type:</span></div>';
                for (const [type, ratio] of Object.entries(compression)) {
                    html += `
                        <div class="compression-format">
                            <strong>${type}:</strong> ${ratio}× 
                        </div>
                    `;
                }
            }
            
            document.getElementById('atoms-stats').innerHTML = html;
        }
        
        function updateAtomsMultilang(atoms) {
            const languages = atoms.multilingual_languages || 0;
            
            const html = `
                <div class="metric">
                    <span class="metric-label">Nombre de langues validées:</span>
                    <span class="metric-value">${languages}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Statut validation:</span>
                    <span class="badge ${languages > 0 ? 'badge-success' : 'badge-warning'}">
                        ${languages > 0 ? 'Multilangue actif' : 'En attente'}
                    </span>
                </div>
            `;
            
            document.getElementById('atoms-multilang').innerHTML = html;
        }
        
        function updateDhatuEvolution(atoms) {
            const evolution = atoms.dhatu_evolution || {};
            const existing = evolution.existing_dhatu || 0;
            const newDhatu = evolution.new_dhatu || 0;
            
            const html = `
                <div class="evolution-box">
                    <div class="evolution-item">
                        <div class="evolution-count">${existing}</div>
                        <div style="color: #aaa; margin-top: 5px;">Dhātu existants</div>
                    </div>
                    <div class="evolution-item">
                        <div class="evolution-count" style="color: #4CAF50;">${newDhatu}</div>
                        <div style="color: #aaa; margin-top: 5px;">Nouveaux dhātu</div>
                    </div>
                </div>
                <div class="metric" style="margin-top: 15px;">
                    <span class="metric-label">Taux de découverte:</span>
                    <span class="badge badge-info">
                        ${existing + newDhatu > 0 ? ((newDhatu / (existing + newDhatu)) * 100).toFixed(1) + '%' : '0%'}
                    </span>
                </div>
            `;
            
            document.getElementById('dhatu-evolution').innerHTML = html;
        }
        
        function updateTranslators(translators) {
            const count = translators.translators_identified || 0;
            const biases = translators.biases_detected || [];
            const patterns = translators.recurring_patterns || [];
            const quality = translators.translation_quality || 0;
            
            let html = `
                <div class="metric">
                    <span class="metric-label">Traducteurs identifiés:</span>
                    <span class="metric-value">${count}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Qualité traduction:</span>
                    <span class="metric-value">${quality}%</span>
                </div>
            `;
            
            // Biais détectés
            if (biases.length > 0) {
                html += '<div class="metric"><span class="metric-label">Biais détectés:</span></div>';
                biases.forEach(bias => {
                    html += `
                        <div class="pattern-item">
                            <strong>${bias.type}:</strong> ${bias.score}
                            <span class="badge badge-warning">Attention</span>
                        </div>
                    `;
                });
            }
            
            // Patterns récurrents
            if (patterns.length > 0) {
                html += '<div class="metric" style="margin-top: 10px;"><span class="metric-label">Patterns récurrents (Top 5):</span></div>';
                patterns.forEach(pattern => {
                    html += `
                        <div class="pattern-item">
                            <strong>${pattern.pattern}:</strong> ${pattern.frequency} occurrences
                        </div>
                    `;
                });
            }
            
            if (biases.length === 0 && patterns.length === 0 && count === 0) {
                html = '<div class="empty-state">Aucune donnée de traduction disponible</div>';
            }
            
            document.getElementById('translators').innerHTML = html;
        }
        
        // Démarrer polling
        fetchMetrics(); // Première mise à jour immédiate
        updateInterval = setInterval(fetchMetrics, 5000); // Mise à jour toutes les 5 secondes
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """Page principale du dashboard"""
    return render_template_string(DASHBOARD_HTML)


@app.route('/api/metrics')
def api_metrics():
    """API REST pour les métriques"""
    return jsonify(collector.cache)


@socketio.on('connect')
def handle_connect():
    """Connexion WebSocket"""
    print(f'Client connecté')
    emit('metrics_update', collector.collect_all_metrics())


@socketio.on('disconnect')
def handle_disconnect():
    """Déconnexion WebSocket"""
    print(f'Client déconnecté')


@socketio.on('request_update')
def handle_request_update():
    """Demande de mise à jour manuelle"""
    emit('metrics_update', collector.collect_all_metrics())


def signal_handler(sig, frame):
    """Gestionnaire d'arrêt propre"""
    print('\n🛑 Arrêt dashboard demandé')
    collector.running = False
    sys.exit(0)


if __name__ == '__main__':
    # Configuration signaux
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Démarrage mises à jour
    collector.start_background_updates()
    
    print("=" * 60)
    print("🚀 Dashboard Métriques Compression Temps Réel")
    print("=" * 60)
    print("📡 Interface disponible sur: http://localhost:8889")
    print("🔄 WebSocket actif pour mises à jour temps réel")
    print("📊 Métriques:")
    print("   - PaniniFS: Compression, Intégrité, Performance")
    print("   - Atomes: Découverte, Multilangue, Compression")
    print("   - Traducteurs: Identifiés, Biais, Patterns")
    print("=" * 60)
    print("Ctrl+C pour arrêter")
    print()
    
    # Démarrage serveur
    socketio.run(app, host='0.0.0.0', port=8889, debug=False)
