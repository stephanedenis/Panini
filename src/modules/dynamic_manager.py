"""
🔧 Module de Substitution Dynamique - Gestionnaire de Modules
Système de sélection et substitution automatique des modules selon contexte
"""

import importlib
import time
from typing import Dict, Any, Optional, Type
from ..interfaces import AnalyzerInterface, LoaderInterface


class ModuleRegistry:
    """Registre des modules disponibles avec métadonnées"""
    
    ANALYZERS = {
        'dhatu_gpu_t4': {
            'module_path': 'src.modules.analyzers.dhatu_gpu_t4',
            'class_name': 'DhatuGPUT4Analyzer',
            'requirements': ['cuda_available', 'colab_optimized'],
            'performance_rating': 10,
            'memory_requirement': 8  # GB
        },
        'dhatu_gpu_cuda': {
            'module_path': 'src.modules.analyzers.dhatu_gpu_cuda',
            'class_name': 'DhatuGPUCudaAnalyzer',
            'requirements': ['cuda_available'],
            'performance_rating': 8,
            'memory_requirement': 4
        },
        'dhatu_gpu_opencl': {
            'module_path': 'src.modules.analyzers.dhatu_gpu_opencl',
            'class_name': 'DhatuGPUOpenCLAnalyzer',
            'requirements': ['opencl_available'],
            'performance_rating': 6,
            'memory_requirement': 3
        },
        'dhatu_cpu_optimized': {
            'module_path': 'src.modules.analyzers.dhatu_cpu_optimized',
            'class_name': 'DhatuCPUOptimizedAnalyzer',
            'requirements': ['integrated_gpu'],
            'performance_rating': 4,
            'memory_requirement': 2
        },
        'dhatu_basic': {
            'module_path': 'src.modules.analyzers.dhatu_basic',
            'class_name': 'DhatuBasicAnalyzer',
            'requirements': [],
            'performance_rating': 2,
            'memory_requirement': 1
        }
    }
    
    LOADERS = {
        'turbo_gpu_loader': {
            'module_path': 'src.modules.loaders.turbo_gpu_loader',
            'class_name': 'TurboGPULoader',
            'requirements': ['cuda_available'],
            'performance_rating': 10
        },
        'turbo_standard_loader': {
            'module_path': 'src.modules.loaders.turbo_standard_loader',
            'class_name': 'TurboStandardLoader',
            'requirements': [],
            'performance_rating': 6
        },
        'batch_loader': {
            'module_path': 'src.modules.loaders.batch_loader',
            'class_name': 'BatchLoader',
            'requirements': [],
            'performance_rating': 4
        }
    }


class DynamicModuleManager:
    """Gestionnaire dynamique de modules avec substitution temps réel"""
    
    def __init__(self):
        self.loaded_modules = {}
        self.active_analyzer = None
        self.active_loader = None
        self.context_history = []
        
    def select_optimal_analyzer(self, gpu_context: Dict[str, Any]) -> str:
        """Sélectionne l'analyseur optimal selon le contexte"""
        
        available_memory = gpu_context.get('total_memory', 0)
        candidates = []
        
        for analyzer_id, spec in ModuleRegistry.ANALYZERS.items():
            # Vérification des exigences
            requirements_met = True
            for req in spec['requirements']:
                if not gpu_context.get(req, False):
                    requirements_met = False
                    break
            
            # Vérification mémoire
            memory_ok = available_memory >= spec['memory_requirement']
            
            if requirements_met and memory_ok:
                candidates.append({
                    'id': analyzer_id,
                    'performance': spec['performance_rating'],
                    'memory': spec['memory_requirement']
                })
        
        # Tri par performance décroissante
        candidates.sort(key=lambda x: x['performance'], reverse=True)
        
        return candidates[0]['id'] if candidates else 'dhatu_basic'
    
    def select_optimal_loader(self, data_type: str, gpu_context: Dict[str, Any]) -> str:
        """Sélectionne le chargeur optimal"""
        
        if data_type == 'turbo':
            if gpu_context.get('cuda_available'):
                return 'turbo_gpu_loader'
            else:
                return 'turbo_standard_loader'
        else:
            return 'batch_loader'
    
    def load_module_dynamically(self, module_id: str, module_type: str) -> Optional[Any]:
        """Charge un module dynamiquement"""
        
        # Vérification cache
        if module_id in self.loaded_modules:
            return self.loaded_modules[module_id]
        
        try:
            # Sélection du registre
            registry = (ModuleRegistry.ANALYZERS if module_type == 'analyzer' 
                       else ModuleRegistry.LOADERS)
            
            if module_id not in registry:
                print(f"❌ Module {module_id} non trouvé dans le registre")
                return None
            
            spec = registry[module_id]
            
            # Import dynamique
            module = importlib.import_module(spec['module_path'])
            module_class = getattr(module, spec['class_name'])
            
            # Instanciation
            instance = module_class()
            
            # Mise en cache
            self.loaded_modules[module_id] = instance
            
            print(f"✅ Module {module_id} chargé dynamiquement")
            return instance
            
        except Exception as e:
            print(f"❌ Erreur chargement module {module_id}: {e}")
            return None
    
    def substitute_analyzer(self, new_analyzer_id: str, gpu_context: Dict[str, Any]) -> bool:
        """Substitue l'analyseur actuel par un nouveau"""
        
        # Nettoyage de l'ancien analyseur
        if self.active_analyzer:
            try:
                self.active_analyzer.cleanup()
                print(f"🧹 Ancien analyseur nettoyé")
            except:
                pass
        
        # Chargement du nouveau
        new_analyzer = self.load_module_dynamically(new_analyzer_id, 'analyzer')
        if not new_analyzer:
            return False
        
        # Test de compatibilité
        compatibility = new_analyzer.detect_compatibility()
        if not compatibility.get('compatible', False):
            print(f"⚠️ Analyseur {new_analyzer_id} non compatible")
            return False
        
        # Initialisation
        if new_analyzer.initialize(gpu_context):
            self.active_analyzer = new_analyzer
            print(f"🔄 Analyseur substitué: {new_analyzer_id}")
            return True
        else:
            print(f"❌ Échec initialisation {new_analyzer_id}")
            return False
    
    def monitor_and_adapt(self, performance_metrics: Dict[str, Any], 
                         gpu_context: Dict[str, Any]) -> bool:
        """Surveille les performances et adapte les modules si nécessaire"""
        
        current_speed = performance_metrics.get('processing_speed', 0)
        gpu_utilization = performance_metrics.get('gpu_utilization', 0)
        
        # Historique des performances
        self.context_history.append({
            'timestamp': time.time(),
            'speed': current_speed,
            'gpu_util': gpu_utilization
        })
        
        # Conserver seulement les 10 dernières mesures
        if len(self.context_history) > 10:
            self.context_history = self.context_history[-10:]
        
        # Analyse de tendance
        if len(self.context_history) >= 5:
            recent_speeds = [h['speed'] for h in self.context_history[-5:]]
            avg_recent_speed = sum(recent_speeds) / len(recent_speeds)
            
            # Dégradation détectée
            if current_speed < avg_recent_speed * 0.7:
                print("📉 Dégradation de performance détectée")
                return self._attempt_module_upgrade(gpu_context)
            
            # Sous-utilisation GPU détectée
            if gpu_utilization < 30 and gpu_context.get('cuda_available'):
                print("🔧 Sous-utilisation GPU détectée")
                return self._attempt_optimization(gpu_context)
        
        return False
    
    def _attempt_module_upgrade(self, gpu_context: Dict[str, Any]) -> bool:
        """Tente une mise à niveau de module"""
        
        current_analyzer_id = getattr(self.active_analyzer, 'name', 'unknown')
        optimal_analyzer_id = self.select_optimal_analyzer(gpu_context)
        
        if optimal_analyzer_id != current_analyzer_id:
            print(f"🔄 Tentative upgrade: {current_analyzer_id} → {optimal_analyzer_id}")
            return self.substitute_analyzer(optimal_analyzer_id, gpu_context)
        
        return False
    
    def _attempt_optimization(self, gpu_context: Dict[str, Any]) -> bool:
        """Tente d'optimiser la configuration actuelle"""
        
        if self.active_analyzer and hasattr(self.active_analyzer, 'optimize_parameters'):
            try:
                self.active_analyzer.optimize_parameters(gpu_context)
                print("🔧 Paramètres analyseur optimisés")
                return True
            except:
                pass
        
        return False
    
    def get_module_status(self) -> Dict[str, Any]:
        """Retourne l'état actuel des modules"""
        
        return {
            'loaded_modules': list(self.loaded_modules.keys()),
            'active_analyzer': getattr(self.active_analyzer, 'name', None),
            'active_loader': getattr(self.active_loader, 'name', None),
            'performance_history_length': len(self.context_history),
            'substitutions_available': True
        }
    
    def cleanup_all_modules(self):
        """Nettoie tous les modules chargés"""
        
        for module_id, module_instance in self.loaded_modules.items():
            try:
                if hasattr(module_instance, 'cleanup'):
                    module_instance.cleanup()
                print(f"🧹 Module {module_id} nettoyé")
            except:
                pass
        
        self.loaded_modules.clear()
        self.active_analyzer = None
        self.active_loader = None
        print("🧹 Tous les modules nettoyés")