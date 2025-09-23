"""
🔧 Interface Standard pour Modules Analyseurs
Architecture modulaire avec substitution dynamique
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import time

class AnalyzerInterface(ABC):
    """Interface standard pour tous les modules d'analyse"""
    
    def __init__(self):
        self.name = self.__class__.__name__
        self.performance_metrics = {
            'documents_processed': 0,
            'processing_speed': 0.0,
            'gpu_utilization': 0.0,
            'memory_usage': 0.0,
            'last_update': time.time()
        }
    
    @abstractmethod
    def detect_compatibility(self) -> Dict[str, Any]:
        """Détecte la compatibilité avec l'environnement actuel"""
        pass
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialise le module avec la configuration donnée"""
        pass
    
    @abstractmethod
    def process(self, data: Any) -> Dict[str, Any]:
        """Traite les données et retourne les résultats"""
        pass
    
    @abstractmethod
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Retourne les métriques de performance du module"""
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Nettoie les ressources utilisées par le module"""
        pass
    
    def update_metrics(self, processed_count: int, processing_time: float):
        """Mise à jour automatique des métriques"""
        self.performance_metrics['documents_processed'] += processed_count
        if processing_time > 0:
            self.performance_metrics['processing_speed'] = processed_count / processing_time
        self.performance_metrics['last_update'] = time.time()

class GPUOptimizerInterface(ABC):
    """Interface pour les optimiseurs GPU"""
    
    @abstractmethod
    def detect_gpu_capabilities(self) -> Dict[str, Any]:
        """Détecte les capacités GPU disponibles"""
        pass
    
    @abstractmethod
    def optimize_for_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Optimise selon le contexte donné"""
        pass
    
    @abstractmethod
    def get_recommended_batch_size(self) -> int:
        """Recommande une taille de batch optimale"""
        pass

class LoaderInterface(ABC):
    """Interface pour les chargeurs de données"""
    
    @abstractmethod
    def load_data(self, source_config: Dict[str, Any]) -> Any:
        """Charge les données selon la configuration"""
        pass
    
    @abstractmethod
    def validate_data(self, data: Any) -> bool:
        """Valide la qualité des données chargées"""
        pass