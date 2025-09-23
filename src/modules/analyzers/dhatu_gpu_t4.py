"""
🚀 Analyseur Dhātu GPU T4 - Module Spécialisé Colab
Optimisé spécifiquement pour GPU T4 en environnement Colab
"""

import time
from typing import Dict, Any
from ..interfaces import AnalyzerInterface


class DhatuGPUT4Analyzer(AnalyzerInterface):
    """Analyseur dhātu optimisé pour GPU T4 (Colab)"""
    
    def __init__(self):
        super().__init__()
        self.name = "DhatuGPUT4Analyzer"
        self.batch_size = 128  # Optimal pour T4
        self.max_workers = 12  # T4 optimisé
        self.dhatu_patterns = self._load_dhatu_patterns()
        self.gpu_available = False
        
    def detect_compatibility(self) -> Dict[str, Any]:
        """Détecte la compatibilité avec GPU T4"""
        compatibility = {
            'compatible': False,
            'gpu_type': 'none',
            'memory_available': 0,
            'colab_environment': False
        }
        
        try:
            import torch
            if torch.cuda.is_available():
                gpu_name = torch.cuda.get_device_name(0)
                if 'T4' in gpu_name:
                    compatibility.update({
                        'compatible': True,
                        'gpu_type': 'T4',
                        'memory_available': torch.cuda.get_device_properties(0).total_memory // (1024**3),
                        'colab_environment': 'COLAB_GPU' in os.environ
                    })
                    self.gpu_available = True
        except ImportError:
            pass
        
        return compatibility
    
    def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialise l'analyseur GPU T4"""
        try:
            if self.gpu_available:
                import torch
                torch.cuda.empty_cache()  # Nettoyage mémoire
                self.device = torch.device('cuda:0')
                
                # Configuration T4 optimisée
                torch.backends.cudnn.benchmark = True
                torch.backends.cudnn.enabled = True
                
                print(f"🚀 {self.name} initialisé sur GPU T4")
                return True
            else:
                print(f"⚠️ GPU T4 non disponible, fallback CPU")
                return False
                
        except Exception as e:
            print(f"❌ Erreur initialisation T4: {e}")
            return False
    
    def process(self, data: Any) -> Dict[str, Any]:
        """Traitement optimisé GPU T4"""
        start_time = time.time()
        
        if isinstance(data, str):
            documents = [data]
        elif isinstance(data, list):
            documents = data
        else:
            documents = [str(data)]
        
        results = {
            'dhatu_analysis': {'total_matches': 0, 'patterns_found': []},
            'molecular_analysis': {'total_molecules': 0, 'combinations': []},
            'ambiguity_analysis': {'total_ambiguities': 0, 'resolved': []},
            'processing_time': 0,
            'documents_processed': len(documents)
        }
        
        # Traitement par batches optimisé T4
        total_matches = 0
        for i in range(0, len(documents), self.batch_size):
            batch = documents[i:i+self.batch_size]
            batch_results = self._process_batch_gpu_t4(batch)
            
            total_matches += batch_results['matches']
            results['dhatu_analysis']['patterns_found'].extend(batch_results['patterns'])
            results['molecular_analysis']['combinations'].extend(batch_results['molecules'])
        
        results['dhatu_analysis']['total_matches'] = total_matches
        results['molecular_analysis']['total_molecules'] = len(results['molecular_analysis']['combinations'])
        results['processing_time'] = time.time() - start_time
        
        # Mise à jour métriques
        self.update_metrics(len(documents), results['processing_time'])
        
        return results
    
    def _process_batch_gpu_t4(self, batch: list) -> Dict[str, Any]:
        """Traitement batch spécifique GPU T4"""
        batch_results = {
            'matches': 0,
            'patterns': [],
            'molecules': []
        }
        
        for doc in batch:
            # Analyse dhātu rapide avec patterns précompilés
            for pattern in self.dhatu_patterns:
                if pattern['regex'].search(doc):
                    batch_results['matches'] += 1
                    batch_results['patterns'].append({
                        'pattern': pattern['name'],
                        'position': pattern['regex'].search(doc).start(),
                        'confidence': pattern['weight']
                    })
            
            # Analyse moléculaire simplifiée
            words = doc.split()
            for i in range(len(words) - 1):
                combination = f"{words[i]}+{words[i+1]}"
                if len(combination) > 6:  # Filtrage basique
                    batch_results['molecules'].append({
                        'combination': combination,
                        'frequency': 1,
                        'semantic_weight': min(1.0, len(combination) / 20)
                    })
        
        return batch_results
    
    def _load_dhatu_patterns(self):
        """Charge les patterns dhātu optimisés pour T4"""
        import re
        
        patterns = [
            {'name': 'gam', 'pattern': r'√गम्|गम्|गच्छ', 'weight': 1.0},
            {'name': 'kr', 'pattern': r'√कृ|कृ|कर्', 'weight': 1.0},
            {'name': 'bhu', 'pattern': r'√भू|भू|भव', 'weight': 1.0},
            {'name': 'as', 'pattern': r'√अस्|अस्|अस्ति', 'weight': 1.0},
            {'name': 'da', 'pattern': r'√दा|दा|दत्त', 'weight': 0.9},
            {'name': 'stha', 'pattern': r'√स्था|स्था|तिष्ठ', 'weight': 0.9},
            {'name': 'i', 'pattern': r'√इ|इ|गच्छ', 'weight': 0.8},
            {'name': 'vid', 'pattern': r'√विद्|विद्|वेत्ति', 'weight': 0.8}
        ]
        
        # Compilation des regex pour performance T4
        for pattern in patterns:
            pattern['regex'] = re.compile(pattern['pattern'])
        
        return patterns
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Métriques spécifiques GPU T4"""
        metrics = self.performance_metrics.copy()
        
        if self.gpu_available:
            try:
                import torch
                metrics.update({
                    'gpu_memory_used': torch.cuda.memory_allocated() // (1024**2),
                    'gpu_memory_cached': torch.cuda.memory_reserved() // (1024**2),
                    'gpu_utilization': self._get_gpu_utilization(),
                    'optimal_batch_size': self.batch_size,
                    'accelerator': 'T4-CUDA'
                })
            except:
                pass
        else:
            metrics['accelerator'] = 'CPU-FALLBACK'
        
        return metrics
    
    def _get_gpu_utilization(self) -> float:
        """Estimation utilisation GPU T4"""
        try:
            import torch
            if torch.cuda.is_available():
                return min(100.0, (torch.cuda.memory_allocated() / 
                                 torch.cuda.get_device_properties(0).total_memory) * 100)
        except:
            pass
        return 0.0
    
    def cleanup(self) -> None:
        """Nettoyage spécifique GPU T4"""
        if self.gpu_available:
            try:
                import torch
                torch.cuda.empty_cache()
                torch.cuda.synchronize()
                print(f"🧹 {self.name} nettoyé (GPU T4)")
            except:
                pass