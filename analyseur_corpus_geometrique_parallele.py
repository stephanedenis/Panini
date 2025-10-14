#!/usr/bin/env python3
"""
ANALYSEUR CORPUS GÉOMÉTRIQUE PARALLÈLE v4.0
==========================================

Système d'analyse concurrent basé sur géométrie dhātu avancée
avec dimensions supérieures (nombres premiers) et reproductibilité complète.

INNOVATIONS:
- Espaces 5D/7D/11D pour dhātu antagonistes  
- Analyse concurrente avec monitoring ressources
- Logging expérimental détaillé pour reproductibilité
- Intégration dictionnaire raffiné contextuel
- Métriques critiques pour amélioration continue
"""

import json
import numpy as np
import multiprocessing as mp
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass, asdict
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import time
import psutil
import os
import logging
from pathlib import Path
import hashlib
import pickle

# Configuration logging expérimental
def setup_experimental_logging(experiment_id: str) -> logging.Logger:
    """Configuration logging détaillé pour reproductibilité"""
    logger = logging.getLogger(f'corpus_geometric_{experiment_id}')
    logger.setLevel(logging.DEBUG)
    
    # Handler fichier avec timestamp
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    log_file = f"corpus_geometric_experiment_{experiment_id}_{timestamp}.log"
    
    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    
    # Format détaillé avec métadonnées système
    formatter = logging.Formatter(
        '%(asctime)s | PID:%(process)d | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s'
    )
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    return logger, log_file

@dataclass 
class ExperimentalConfig:
    """Configuration expérimentale complète pour reproductibilité"""
    experiment_id: str
    prime_dimensions: List[int]  # [5, 7, 11] pour antagonistes
    dhatu_count: int
    corpus_chunk_size: int
    concurrent_workers: int
    geometric_thresholds: Dict[str, float]
    random_seed: int
    system_specs: Dict[str, Any]
    input_files: List[str]
    algorithm_version: str
    
    def save_config(self, path: str):
        """Sauvegarde configuration pour reproductibilité"""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(asdict(self), f, ensure_ascii=False, indent=2)
    
    def hash_config(self) -> str:
        """Hash configuration pour vérification reproductibilité"""
        config_str = json.dumps(asdict(self), sort_keys=True)
        return hashlib.sha256(config_str.encode()).hexdigest()[:16]

@dataclass
class GeometricDhatuVector:
    """Vecteur dhātu multi-dimensionnel avec bases nombres premiers"""
    name: str
    base_2d: np.ndarray    # Représentation binaire simple
    base_5d: np.ndarray    # Dimension quintaire pour antagonistes  
    base_7d: np.ndarray    # Dimension septenary pour nuances
    base_11d: np.ndarray   # Dimension undenary pour hypercomplexité
    activation_strength: float
    context_weights: Dict[str, float]
    
@dataclass
class ParallelAnalysisResult:
    """Résultat analyse parallèle avec métriques critiques"""
    experiment_id: str
    processing_time: float
    memory_usage: Dict[str, float]
    cpu_usage: Dict[str, float] 
    dhatu_activations: Dict[str, GeometricDhatuVector]
    geometric_relations: List[Dict[str, Any]]
    quality_metrics: Dict[str, float]
    critical_insights: List[str]
    improvement_suggestions: List[str]

class ResourceMonitor:
    """Monitoring ressources système pour analyses concurrentes"""
    
    def __init__(self, experiment_id: str):
        self.experiment_id = experiment_id
        self.start_time = time.time()
        self.measurements = []
    
    def measure(self, label: str = "checkpoint"):
        """Mesure instantanée ressources"""
        measurement = {
            'timestamp': time.time() - self.start_time,
            'label': label,
            'memory': {
                'rss': psutil.Process().memory_info().rss / (1024**2),  # MB
                'vms': psutil.Process().memory_info().vms / (1024**2),  # MB
                'available': psutil.virtual_memory().available / (1024**2),  # MB
                'percent': psutil.virtual_memory().percent
            },
            'cpu': {
                'percent': psutil.cpu_percent(interval=0.1),
                'cores_used': psutil.cpu_count(logical=False),
                'load_avg': os.getloadavg() if hasattr(os, 'getloadavg') else [0,0,0]
            }
        }
        self.measurements.append(measurement)
        return measurement

class GeometricDhatuAnalyzer:
    """Analyseur géométrique avancé avec dimensions supérieures"""
    
    def __init__(self, config: ExperimentalConfig, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.monitor = ResourceMonitor(config.experiment_id)
        
        # Initialisation espaces géométriques multi-dimensionnels
        self._init_prime_dimensional_spaces()
        
        # Chargement dictionnaire raffiné
        self._load_refined_dictionary()
        
        # Dhātu universels avec représentations multi-dimensionnelles
        self._init_geometric_dhatus()
        
        self.logger.info(f"Analyseur géométrique initialisé - Experiment: {config.experiment_id}")
        self.logger.info(f"Config hash: {config.hash_config()}")
        
    def _init_prime_dimensional_spaces(self):
        """Initialise espaces géométriques basés nombres premiers"""
        self.prime_spaces = {}
        
        # Set random seed pour reproductibilité
        np.random.seed(self.config.random_seed)
        
        for prime in self.config.prime_dimensions:
            # Espaces orthogonaux pour chaque dimension premier
            # Génération matrice orthogonale via QR decomposition
            random_matrix = np.random.randn(prime, prime)
            q, r = np.linalg.qr(random_matrix)
            
            self.prime_spaces[prime] = {
                'dimension': prime,
                'basis_vectors': q,  # Matrice orthogonale
                'antagonist_projections': self._compute_antagonist_projections(prime),
                'discrete_lattice': self._build_discrete_lattice(prime)
            }
            
            self.logger.debug(f"Espace {prime}D initialisé avec base orthonormée")
        
        self.monitor.measure("prime_spaces_init")
    
    def _compute_antagonist_projections(self, dimension: int) -> np.ndarray:
        """Calcule projections pour dhātu antagonistes"""
        # Projections maximisant distance pour concepts opposés
        projections = np.zeros((9, dimension))  # 9 dhātu
        
        # Exemples: AMOUR vs DESTRUCTION, CREATION vs ITERATION
        antagonist_pairs = [
            (0, 4),  # RELATE vs COMM (spatial vs communicatif)
            (1, 7),  # MODAL vs DECIDE (possibilité vs action)  
            (2, 5),  # EXIST vs CAUSE (être vs faire)
        ]
        
        for i, (dhatu_a, dhatu_b) in enumerate(antagonist_pairs):
            if i < dimension // 2:
                projections[dhatu_a, i] = 1.0
                projections[dhatu_b, i] = -1.0  # Opposition géométrique
        
        return projections
    
    def _build_discrete_lattice(self, dimension: int) -> Dict[str, np.ndarray]:
        """Construit lattice discret pour dhātu non-continus"""
        lattice_points = {}
        
        # Points lattice pour concepts discrets (nombres, categories, etc.)
        for i in range(min(dimension, 9)):  # Un point par dhātu 
            point = np.zeros(dimension)
            point[i] = 1.0
            lattice_points[f'dhatu_{i}'] = point
            
        return lattice_points
    
    def _load_refined_dictionary(self):
        """Charge dictionnaire raffiné pour enrichissement contextuel"""
        try:
            refined_files = list(Path('.').glob('dictionnaire_raffine_*.json'))
            if refined_files:
                latest_refined = max(refined_files, key=os.path.getctime)
                
                with open(latest_refined, 'r', encoding='utf-8') as f:
                    self.refined_dict = json.load(f)
                
                self.logger.info(f"Dictionnaire raffiné chargé: {latest_refined}")
                self.logger.info(f"Concepts raffinés: {len(self.refined_dict.get('concepts_raffines', {}))}")
            else:
                self.refined_dict = {}
                self.logger.warning("Aucun dictionnaire raffiné trouvé")
                
        except Exception as e:
            self.logger.error(f"Erreur chargement dictionnaire: {e}")
            self.refined_dict = {}
    
    def _init_geometric_dhatus(self):
        """Initialise dhātu avec représentations géométriques multi-dimensionnelles"""
        dhatu_names = ['RELATE', 'MODAL', 'EXIST', 'EVAL', 'COMM', 'CAUSE', 'ITER', 'DECIDE', 'FEEL']
        
        self.geometric_dhatus = {}
        
        for i, name in enumerate(dhatu_names):
            # Vecteurs base pour chaque dimension
            base_2d = np.random.randn(2)
            base_5d = np.random.randn(5)  
            base_7d = np.random.randn(7)
            base_11d = np.random.randn(11)
            
            # Normalisation sur sphère unitaire
            base_2d = base_2d / np.linalg.norm(base_2d)
            base_5d = base_5d / np.linalg.norm(base_5d)
            base_7d = base_7d / np.linalg.norm(base_7d) 
            base_11d = base_11d / np.linalg.norm(base_11d)
            
            # Enrichissement contextuel depuis dictionnaire raffiné
            context_weights = self._extract_contextual_weights(name)
            
            dhatu = GeometricDhatuVector(
                name=name,
                base_2d=base_2d,
                base_5d=base_5d, 
                base_7d=base_7d,
                base_11d=base_11d,
                activation_strength=0.0,
                context_weights=context_weights
            )
            
            self.geometric_dhatus[name] = dhatu
            
        self.logger.info(f"Dhātu géométriques initialisés: {len(self.geometric_dhatus)}")
        self.monitor.measure("dhatus_init")
    
    def _extract_contextual_weights(self, dhatu_name: str) -> Dict[str, float]:
        """Extrait poids contextuels depuis dictionnaire raffiné"""
        if dhatu_name in self.refined_dict.get('concepts_raffines', {}):
            refined_concept = self.refined_dict['concepts_raffines'][dhatu_name]
            
            # Convertir dimensions contextuelles en poids
            context_dims = refined_concept.get('contextual_dimensions', {})
            weights = {}
            
            for context, data in context_dims.items():
                if isinstance(data, dict) and 'weight' in data:
                    weights[context] = data['weight']
                    
            return weights
        
        # Poids par défaut uniformes
        return {'default': 1.0}
    
    def analyze_corpus_chunk_parallel(self, text_chunk: str, chunk_id: int) -> Dict[str, Any]:
        """Analyse chunk corpus avec géométrie multi-dimensionnelle"""
        self.logger.debug(f"Début analyse chunk {chunk_id} - Taille: {len(text_chunk)} chars")
        
        start_time = time.time()
        chunk_result = {
            'chunk_id': chunk_id,
            'text_size': len(text_chunk),
            'dhatu_activations': {},
            'geometric_features': {},
            'quality_score': 0.0
        }
        
        # Analyse dans chaque espace dimensionnel
        for prime_dim in self.config.prime_dimensions:
            dim_analysis = self._analyze_in_prime_dimension(text_chunk, prime_dim)
            chunk_result['geometric_features'][f'dim_{prime_dim}'] = dim_analysis
        
        # Fusion multi-dimensionnelle
        fused_activations = self._fuse_dimensional_activations(chunk_result['geometric_features'])
        chunk_result['dhatu_activations'] = fused_activations
        
        # Score qualité contextuel
        chunk_result['quality_score'] = self._compute_contextual_quality_score(text_chunk, fused_activations)
        
        processing_time = time.time() - start_time
        chunk_result['processing_time'] = processing_time
        
        self.logger.debug(f"Chunk {chunk_id} terminé en {processing_time:.2f}s - Qualité: {chunk_result['quality_score']:.3f}")
        
        return chunk_result
    
    def _analyze_in_prime_dimension(self, text: str, prime_dim: int) -> Dict[str, Any]:
        """Analyse texte dans espace prime_dim dimensionnel"""
        space = self.prime_spaces[prime_dim]
        
        # Détection activations dhātu dans texte
        activations = {}
        
        for dhatu_name, dhatu in self.geometric_dhatus.items():
            # Projection dans espace prime_dim
            if prime_dim == 5:
                vector = dhatu.base_5d
            elif prime_dim == 7:
                vector = dhatu.base_7d 
            elif prime_dim == 11:
                vector = dhatu.base_11d
            else:
                vector = dhatu.base_2d
                
            # Détection patterns dans texte (simulation)
            pattern_strength = self._detect_dhatu_patterns(text, dhatu_name)
            
            # Projection géométrique
            projected_activation = np.dot(vector, space['basis_vectors'][:len(vector), :])
            
            activations[dhatu_name] = {
                'pattern_strength': pattern_strength,
                'geometric_projection': projected_activation.tolist(),
                'dimension': prime_dim
            }
        
        return {
            'dimension': prime_dim,
            'activations': activations,
            'space_coverage': self._compute_space_coverage(activations, prime_dim)
        }
    
    def _detect_dhatu_patterns(self, text: str, dhatu_name: str) -> float:
        """Détection patterns dhātu dans texte (version simplifiée pour demo)"""
        # Patterns de base par dhātu  
        patterns = {
            'RELATE': ['with', 'between', 'among', 'relationship'],
            'MODAL': ['can', 'could', 'should', 'must', 'may'],
            'EXIST': ['is', 'are', 'be', 'being', 'exist'],
            'EVAL': ['good', 'bad', 'better', 'compare', 'quality'],
            'COMM': ['say', 'tell', 'speak', 'write', 'message'],
            'CAUSE': ['because', 'make', 'cause', 'reason'],
            'ITER': ['again', 'repeat', 'continue', 'keep'],
            'DECIDE': ['choose', 'decide', 'select', 'pick'],
            'FEEL': ['feel', 'emotion', 'mood', 'sense']
        }
        
        dhatu_patterns = patterns.get(dhatu_name, [])
        
        # Comptage occurrences (normalisé)
        text_lower = text.lower()
        total_matches = sum(text_lower.count(pattern) for pattern in dhatu_patterns)
        
        # Normalisation par longueur texte
        strength = min(total_matches / max(len(text_lower.split()), 1), 1.0)
        
        return strength
    
    def _compute_space_coverage(self, activations: Dict[str, Any], dimension: int) -> float:
        """Calcule couverture espace géométrique"""
        active_vectors = []
        
        for dhatu_name, activation in activations.items():
            if activation['pattern_strength'] > 0.1:
                active_vectors.append(np.array(activation['geometric_projection']))
        
        if len(active_vectors) < 2:
            return 0.0
        
        # Volume parallélépipède formé par vecteurs actifs (approximation)
        active_matrix = np.array(active_vectors)
        try:
            coverage = abs(np.linalg.det(active_matrix[:dimension, :dimension]))
            return min(coverage, 1.0)
        except:
            return 0.0
    
    def _fuse_dimensional_activations(self, geometric_features: Dict[str, Any]) -> Dict[str, Any]:
        """Fusionne activations multi-dimensionnelles"""
        fused_activations = {}
        
        for dhatu_name in self.geometric_dhatus.keys():
            activations_by_dim = {}
            total_strength = 0.0
            
            for dim_key, dim_analysis in geometric_features.items():
                dim_num = int(dim_key.split('_')[1])
                dhatu_activation = dim_analysis['activations'].get(dhatu_name, {})
                
                pattern_strength = dhatu_activation.get('pattern_strength', 0.0)
                activations_by_dim[dim_num] = pattern_strength
                total_strength += pattern_strength
            
            # Moyenne pondérée par dimension
            weights = {2: 1.0, 5: 2.0, 7: 1.5, 11: 1.2}  # Poids selon complexité
            weighted_strength = sum(
                activations_by_dim.get(dim, 0.0) * weights.get(dim, 1.0) 
                for dim in self.config.prime_dimensions
            ) / sum(weights.get(dim, 1.0) for dim in self.config.prime_dimensions)
            
            fused_activations[dhatu_name] = {
                'total_strength': total_strength,
                'weighted_strength': weighted_strength,
                'dimensional_breakdown': activations_by_dim
            }
        
        return fused_activations
    
    def _compute_contextual_quality_score(self, text: str, activations: Dict[str, Any]) -> float:
        """Score qualité contextuel utilisant dictionnaire raffiné"""
        quality_factors = []
        
        # Diversité dhātu activés
        active_dhatus = sum(1 for act in activations.values() if act['weighted_strength'] > 0.1)
        diversity_score = min(active_dhatus / len(self.geometric_dhatus), 1.0)
        quality_factors.append(('diversity', diversity_score, 0.3))
        
        # Cohérence contextuelle (basée sur dictionnaire raffiné)
        coherence_score = self._compute_contextual_coherence(activations)
        quality_factors.append(('coherence', coherence_score, 0.4))
        
        # Expressivité géométrique
        expressivity_score = self._compute_geometric_expressivity(activations)
        quality_factors.append(('expressivity', expressivity_score, 0.3))
        
        # Score pondéré
        total_score = sum(score * weight for _, score, weight in quality_factors)
        
        return total_score
    
    def _compute_contextual_coherence(self, activations: Dict[str, Any]) -> float:
        """Cohérence contextuelle basée dictionnaire raffiné"""
        coherence_sum = 0.0
        active_count = 0
        
        for dhatu_name, activation in activations.items():
            if activation['weighted_strength'] > 0.1:
                # Cherche cohérence contextuelle dans dictionnaire raffiné
                if dhatu_name in self.refined_dict.get('concepts_raffines', {}):
                    concept_data = self.refined_dict['concepts_raffines'][dhatu_name]
                    confidence_score = concept_data.get('confidence_score', 0.5)
                    coherence_sum += confidence_score
                else:
                    coherence_sum += 0.5  # Score neutre
                
                active_count += 1
        
        return coherence_sum / max(active_count, 1)
    
    def _compute_geometric_expressivity(self, activations: Dict[str, Any]) -> float:
        """Expressivité géométrique multi-dimensionnelle"""
        expressivity_scores = []
        
        for dhatu_name, activation in activations.items():
            dimensional_variance = np.var(list(activation['dimensional_breakdown'].values()))
            expressivity_scores.append(dimensional_variance)
        
        # Variance moyenne = expressivité
        return np.mean(expressivity_scores) if expressivity_scores else 0.0

    def run_parallel_corpus_analysis(self, corpus_files: List[str]) -> ParallelAnalysisResult:
        """Lance analyse corpus parallèle complète"""
        self.logger.info(f"🚀 DÉBUT ANALYSE PARALLÈLE - Experiment {self.config.experiment_id}")
        self.logger.info(f"📁 Fichiers corpus: {len(corpus_files)}")
        self.logger.info(f"⚙️ Workers concurrents: {self.config.concurrent_workers}")
        
        start_time = time.time()
        
        # Chargement et chunking corpus
        all_chunks = self._load_and_chunk_corpus(corpus_files)
        self.logger.info(f"📊 Chunks créés: {len(all_chunks)}")
        
        # Analyse parallèle
        chunk_results = []
        
        with ProcessPoolExecutor(max_workers=self.config.concurrent_workers) as executor:
            # Soumission tâches
            future_to_chunk = {
                executor.submit(self.analyze_corpus_chunk_parallel, chunk_text, chunk_id): chunk_id
                for chunk_id, chunk_text in enumerate(all_chunks)
            }
            
            # Collecte résultats avec monitoring
            for future in as_completed(future_to_chunk):
                chunk_id = future_to_chunk[future]
                
                try:
                    chunk_result = future.result()
                    chunk_results.append(chunk_result)
                    
                    # Monitoring périodique
                    if len(chunk_results) % 10 == 0:
                        self.monitor.measure(f"chunks_processed_{len(chunk_results)}")
                        self.logger.info(f"✅ Chunks traités: {len(chunk_results)}/{len(all_chunks)}")
                        
                except Exception as e:
                    self.logger.error(f"Erreur chunk {chunk_id}: {e}")
        
        # Fusion résultats et analyse finale
        final_result = self._synthesize_parallel_results(chunk_results)
        final_result.processing_time = time.time() - start_time
        final_result.experiment_id = self.config.experiment_id
        
        # Métriques finales
        final_measurement = self.monitor.measure("analysis_complete")
        final_result.memory_usage = final_measurement['memory']
        final_result.cpu_usage = final_measurement['cpu']
        
        self.logger.info(f"🎯 ANALYSE TERMINÉE en {final_result.processing_time:.1f}s")
        self.logger.info(f"💾 Mémoire max: {max(m['memory']['rss'] for m in self.monitor.measurements):.1f}MB")
        self.logger.info(f"⚡ CPU moyen: {np.mean([m['cpu']['percent'] for m in self.monitor.measurements]):.1f}%")
        
        return final_result
    
    def _load_and_chunk_corpus(self, corpus_files: List[str]) -> List[str]:
        """Charge et découpe corpus en chunks pour parallélisation"""
        all_chunks = []
        
        for file_path in corpus_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Chunking par taille
                    chunk_size = self.config.corpus_chunk_size
                    for i in range(0, len(content), chunk_size):
                        chunk = content[i:i + chunk_size]
                        if len(chunk.strip()) > 50:  # Éviter chunks trop petits
                            all_chunks.append(chunk)
                    
                    self.logger.debug(f"Fichier {file_path} chargé: {len(content)} chars → {len(all_chunks)} chunks")
                    
                except Exception as e:
                    self.logger.error(f"Erreur lecture {file_path}: {e}")
            else:
                self.logger.warning(f"Fichier introuvable: {file_path}")
        
        return all_chunks
    
    def _synthesize_parallel_results(self, chunk_results: List[Dict[str, Any]]) -> ParallelAnalysisResult:
        """Synthèse résultats parallèles avec métriques critiques"""
        
        # Fusion activations dhātu
        global_dhatu_activations = {}
        total_quality_score = 0.0
        
        for chunk_result in chunk_results:
            total_quality_score += chunk_result.get('quality_score', 0.0)
            
            for dhatu_name, activation in chunk_result.get('dhatu_activations', {}).items():
                if dhatu_name not in global_dhatu_activations:
                    global_dhatu_activations[dhatu_name] = {
                        'total_strength': 0.0,
                        'weighted_strength': 0.0,
                        'activation_count': 0
                    }
                
                global_dhatu_activations[dhatu_name]['total_strength'] += activation.get('total_strength', 0.0)
                global_dhatu_activations[dhatu_name]['weighted_strength'] += activation.get('weighted_strength', 0.0)
                global_dhatu_activations[dhatu_name]['activation_count'] += 1
        
        # Moyennes globales
        for dhatu_name in global_dhatu_activations:
            count = global_dhatu_activations[dhatu_name]['activation_count']
            if count > 0:
                global_dhatu_activations[dhatu_name]['avg_strength'] = \
                    global_dhatu_activations[dhatu_name]['weighted_strength'] / count
        
        # Métriques qualité
        avg_quality = total_quality_score / max(len(chunk_results), 1)
        
        quality_metrics = {
            'average_quality': avg_quality,
            'dhatu_coverage': len([d for d in global_dhatu_activations.values() if d.get('avg_strength', 0) > 0.1]),
            'processing_efficiency': len(chunk_results) / self.config.concurrent_workers,
            'geometric_expressivity': self._compute_global_geometric_expressivity(global_dhatu_activations)
        }
        
        # Insights critiques
        critical_insights = self._generate_critical_insights(global_dhatu_activations, quality_metrics)
        improvement_suggestions = self._generate_improvement_suggestions(global_dhatu_activations, quality_metrics)
        
        return ParallelAnalysisResult(
            experiment_id=self.config.experiment_id,
            processing_time=0.0,  # Sera rempli par run_parallel_corpus_analysis
            memory_usage={},      # Sera rempli par run_parallel_corpus_analysis  
            cpu_usage={},         # Sera rempli par run_parallel_corpus_analysis
            dhatu_activations=global_dhatu_activations,
            geometric_relations=[],  # TODO: implémenter si nécessaire
            quality_metrics=quality_metrics,
            critical_insights=critical_insights,
            improvement_suggestions=improvement_suggestions
        )
    
    def _compute_global_geometric_expressivity(self, activations: Dict[str, Any]) -> float:
        """Expressivité géométrique globale"""
        expressivity_values = []
        
        for dhatu_name, activation_data in activations.items():
            avg_strength = activation_data.get('avg_strength', 0.0)
            if avg_strength > 0.1:
                expressivity_values.append(avg_strength)
        
        # Variance des forces d'activation = expressivité
        return np.var(expressivity_values) if len(expressivity_values) > 1 else 0.0
    
    def _generate_critical_insights(self, activations: Dict[str, Any], quality_metrics: Dict[str, float]) -> List[str]:
        """Génère insights critiques pour amélioration"""
        insights = []
        
        # Top dhātu activés
        top_dhatus = sorted(activations.items(), key=lambda x: x[1].get('avg_strength', 0), reverse=True)[:3]
        insights.append(f"🔥 Dhātu dominants: {', '.join([d[0] for d in top_dhatus])}")
        
        # Couverture géométrique  
        coverage = quality_metrics['dhatu_coverage']
        if coverage < 5:
            insights.append(f"⚠️ Couverture dhātu faible: {coverage}/9 - Texte possiblement spécialisé")
        elif coverage >= 7:
            insights.append(f"✅ Excellente couverture dhātu: {coverage}/9 - Texte riche et varié")
        
        # Expressivité géométrique
        expressivity = quality_metrics['geometric_expressivity']
        if expressivity > 0.1:
            insights.append(f"🎯 Haute expressivité géométrique: {expressivity:.3f} - Nuances complexes détectées")
        
        return insights
    
    def _generate_improvement_suggestions(self, activations: Dict[str, Any], quality_metrics: Dict[str, float]) -> List[str]:
        """Suggestions d'amélioration basées sur analyse critique"""
        suggestions = []
        
        # Efficacité traitement
        efficiency = quality_metrics['processing_efficiency']
        if efficiency < 0.8:
            suggestions.append(f"🚀 Augmenter workers concurrents (efficacité actuelle: {efficiency:.2f})")
        
        # Qualité moyenne
        avg_quality = quality_metrics['average_quality']
        if avg_quality < 0.6:
            suggestions.append(f"📊 Améliorer qualité corpus (score actuel: {avg_quality:.2f}) - Filtrer ou enrichir données")
        
        # Dhātu sous-utilisés
        underused_dhatus = [name for name, data in activations.items() if data.get('avg_strength', 0) < 0.05]
        if len(underused_dhatus) > 3:
            suggestions.append(f"🔍 Améliorer détection patterns pour: {', '.join(underused_dhatus[:3])}")
        
        # Dimensions géométriques
        if quality_metrics['geometric_expressivity'] < 0.05:
            suggestions.append("📐 Explorer dimensions supérieures (13D, 17D) pour expressivité accrue")
        
        return suggestions

def create_experimental_config() -> ExperimentalConfig:
    """Crée configuration expérimentale pour reproductibilité"""
    
    # Détection corpus disponibles
    corpus_files = []
    potential_files = [
        'data/corpus_complet_unifie.json',
        'data/corpus_multilingue_dev.json', 
        'data/corpus_prescolaire.json',
        'data/corpus_scientifique.json',
        'corpus_complet_unifie.json',
        'corpus_multilingue_dev.json', 
        'corpus_prescolaire.json',
        'corpus_scientifique.json'
    ]
    
    for file in potential_files:
        if os.path.exists(file):
            corpus_files.append(file)
    
    # Configuration système
    system_specs = {
        'cpu_count': psutil.cpu_count(logical=False),
        'cpu_count_logical': psutil.cpu_count(logical=True),
        'memory_total_gb': psutil.virtual_memory().total / (1024**3),
        'python_version': os.sys.version,
        'platform': os.sys.platform
    }
    
    # Workers optimaux (75% des cœurs logiques)
    optimal_workers = max(1, int(psutil.cpu_count(logical=True) * 0.75))
    
    experiment_id = f"geometric_parallel_{int(time.time())}"
    
    config = ExperimentalConfig(
        experiment_id=experiment_id,
        prime_dimensions=[5, 7, 11],  # Dimensions supérieures
        dhatu_count=9,
        corpus_chunk_size=8192,      # 8KB par chunk
        concurrent_workers=optimal_workers,
        geometric_thresholds={
            'activation_threshold': 0.1,
            'quality_threshold': 0.6,
            'expressivity_threshold': 0.05
        },
        random_seed=42,              # Reproductibilité
        system_specs=system_specs,
        input_files=corpus_files,
        algorithm_version="geometric_parallel_v4.0"
    )
    
    return config

def main():
    """Point d'entrée analyse corpus géométrique parallèle"""
    
    print("🔺 ANALYSEUR CORPUS GÉOMÉTRIQUE PARALLÈLE v4.0")
    print("=" * 60)
    
    # Configuration expérimentale
    config = create_experimental_config()
    print(f"🧪 Experiment ID: {config.experiment_id}")
    print(f"📐 Dimensions: {config.prime_dimensions}")
    print(f"⚙️ Workers: {config.concurrent_workers}")
    print(f"📁 Corpus files: {len(config.input_files)}")
    
    # Logging expérimental
    logger, log_file = setup_experimental_logging(config.experiment_id)
    logger.info("🚀 DÉBUT EXPÉRIENCE GÉOMÉTRIQUE PARALLÈLE")
    
    # Sauvegarde configuration
    config_file = f"config_{config.experiment_id}.json"
    config.save_config(config_file)
    logger.info(f"Configuration sauvegardée: {config_file}")
    print(f"📋 Config hash: {config.hash_config()}")
    
    if not config.input_files:
        print("❌ Aucun fichier corpus trouvé")
        logger.error("Aucun fichier corpus disponible")
        return
    
    try:
        # Initialisation analyseur
        analyzer = GeometricDhatuAnalyzer(config, logger)
        
        # Lancement analyse parallèle
        result = analyzer.run_parallel_corpus_analysis(config.input_files)
        
        # Sauvegarde résultats
        result_file = f"parallel_analysis_result_{config.experiment_id}.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(result), f, ensure_ascii=False, indent=2)
        
        # Rapport final
        print(f"\n🎯 ANALYSE TERMINÉE")
        print(f"⏱️  Durée: {result.processing_time:.1f}s")
        print(f"💾 Mémoire max: {result.memory_usage.get('rss', 0):.1f}MB")
        print(f"📊 Qualité moyenne: {result.quality_metrics.get('average_quality', 0):.3f}")
        print(f"🔥 Dhātu coverage: {result.quality_metrics.get('dhatu_coverage', 0)}/9")
        
        print(f"\n💡 INSIGHTS CRITIQUES:")
        for insight in result.critical_insights:
            print(f"   {insight}")
        
        print(f"\n🚀 SUGGESTIONS D'AMÉLIORATION:")
        for suggestion in result.improvement_suggestions:
            print(f"   {suggestion}")
        
        print(f"\n📄 Résultats: {result_file}")
        print(f"📄 Log détaillé: {log_file}")
        print(f"📄 Configuration: {config_file}")
        
        logger.info("✅ EXPÉRIENCE TERMINÉE AVEC SUCCÈS")
        
    except Exception as e:
        logger.error(f"Erreur critique: {e}")
        print(f"❌ ERREUR: {e}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()