"""
🎯 Détecteur GPU Intelligent - Sélection Dynamique d'Optimisation
Module de détection et sélection automatique des ressources GPU
"""

import os
import sys
import subprocess
from typing import Dict, Any, Optional, List

# Import avec fallback pour éviter les erreurs relatives
try:
    from ..interfaces import GPUOptimizerInterface
except ImportError:
    try:
        from modules.interfaces import GPUOptimizerInterface
    except ImportError:
        # Fallback minimal si interfaces non disponibles
        class GPUOptimizerInterface:
            pass


class GPUDetector:
    """Détecteur intelligent des capacités GPU disponibles"""
    
    @staticmethod
    def detect_all_gpu_capabilities() -> Dict[str, Any]:
        """Détection complète des GPU disponibles"""
        
        capabilities = {
            'cuda_available': False,
            'opencl_available': False,
            'gpu_count': 0,
            'gpu_names': [],
            'total_memory': 0,
            'recommended_mode': 'cpu',
            'optimal_batch_size': 16,
            'max_workers': 2
        }
        
        # Détection CUDA/PyTorch
        cuda_info = GPUDetector._detect_cuda()
        capabilities.update(cuda_info)
        
        # Détection OpenCL/AMD
        if not capabilities['cuda_available']:
            opencl_info = GPUDetector._detect_opencl()
            capabilities.update(opencl_info)
        
        # Détection GPU intégrés
        if not capabilities['cuda_available'] and not capabilities['opencl_available']:
            integrated_info = GPUDetector._detect_integrated_gpu()
            capabilities.update(integrated_info)
        
        # Recommandations selon les capacités
        capabilities = GPUDetector._generate_recommendations(capabilities)
        
        return capabilities
    
    @staticmethod
    def _detect_cuda() -> Dict[str, Any]:
        """Détection spécifique CUDA/PyTorch"""
        info = {'cuda_available': False, 'pytorch_version': None}
        
        try:
            import torch
            info['pytorch_version'] = torch.__version__
            
            if torch.cuda.is_available():
                info.update({
                    'cuda_available': True,
                    'gpu_count': torch.cuda.device_count(),
                    'gpu_names': [torch.cuda.get_device_name(i) 
                                for i in range(torch.cuda.device_count())],
                    'total_memory': sum([torch.cuda.get_device_properties(i).total_memory 
                                       for i in range(torch.cuda.device_count())]) // (1024**3),
                    'recommended_mode': 'cuda',
                    'optimal_batch_size': 64,
                    'max_workers': 8
                })
                
                # Détection T4 spécifique (Colab)
                gpu_names = info['gpu_names']
                if any('T4' in name for name in gpu_names):
                    info.update({
                        'gpu_type': 'T4',
                        'colab_optimized': True,
                        'optimal_batch_size': 128,
                        'max_workers': 12
                    })
                
        except ImportError:
            pass
        
        return info
    
    @staticmethod
    def _detect_opencl() -> Dict[str, Any]:
        """Détection OpenCL pour GPU AMD/Intel"""
        info = {'opencl_available': False}
        
        # Vérification des fichiers système AMD
        amd_paths = ['/dev/dri', '/sys/class/drm', '/dev/kfd']
        amd_detected = any(os.path.exists(path) for path in amd_paths)
        
        if amd_detected:
            try:
                # Tentative de détection via rocm-smi ou clinfo
                result = subprocess.run(['lspci'], capture_output=True, text=True)
                if 'AMD' in result.stdout or 'Radeon' in result.stdout:
                    info.update({
                        'opencl_available': True,
                        'gpu_vendor': 'AMD',
                        'recommended_mode': 'opencl',
                        'optimal_batch_size': 32,
                        'max_workers': 6
                    })
            except:
                pass
        
        return info
    
    @staticmethod
    def _detect_integrated_gpu() -> Dict[str, Any]:
        """Détection GPU intégrés Intel/AMD"""
        info = {'integrated_gpu': False}
        
        try:
            result = subprocess.run(['lspci'], capture_output=True, text=True)
            if 'Intel' in result.stdout and 'Graphics' in result.stdout:
                info.update({
                    'integrated_gpu': True,
                    'gpu_vendor': 'Intel',
                    'recommended_mode': 'cpu_optimized',
                    'optimal_batch_size': 16,
                    'max_workers': 4
                })
        except:
            pass
        
        return info
    
    @staticmethod
    def _generate_recommendations(capabilities: Dict[str, Any]) -> Dict[str, Any]:
        """Génère les recommandations d'optimisation"""
        
        # Ajustements selon la mémoire disponible
        total_memory = capabilities.get('total_memory', 0)
        if total_memory > 16:  # Plus de 16 GB
            capabilities['optimal_batch_size'] *= 2
            capabilities['max_workers'] += 4
        elif total_memory < 8:  # Moins de 8 GB
            capabilities['optimal_batch_size'] //= 2
            capabilities['max_workers'] = max(2, capabilities['max_workers'] - 2)
        
        return capabilities


class ModuleSelector:
    """Sélecteur intelligent de modules selon le contexte"""
    
    @staticmethod
    def get_best_analyzer(gpu_context: Dict[str, Any]) -> str:
        """Sélectionne le meilleur analyseur selon le contexte GPU"""
        
        if gpu_context.get('cuda_available') and gpu_context.get('colab_optimized'):
            return 'dhatu_gpu_t4'
        elif gpu_context.get('cuda_available'):
            return 'dhatu_gpu_cuda'
        elif gpu_context.get('opencl_available'):
            return 'dhatu_gpu_opencl'
        elif gpu_context.get('integrated_gpu'):
            return 'dhatu_cpu_optimized'
        else:
            return 'dhatu_basic'
    
    @staticmethod
    def get_best_loader(data_volume: str, gpu_context: Dict[str, Any]) -> str:
        """Sélectionne le meilleur chargeur selon le volume et contexte"""
        
        if data_volume == 'turbo' and gpu_context.get('cuda_available'):
            return 'turbo_gpu_loader'
        elif data_volume == 'turbo':
            return 'turbo_standard_loader'
        elif data_volume == 'batch':
            return 'batch_loader'
        else:
            return 'stream_loader'


class DynamicOptimizer:
    """Optimiseur dynamique qui ajuste les paramètres en temps réel"""
    
    def __init__(self, initial_context: Dict[str, Any]):
        self.context = initial_context
        self.performance_history = []
    
    def update_optimization(self, performance_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Met à jour l'optimisation selon les performances mesurées"""
        
        self.performance_history.append(performance_metrics)
        
        # Ajustement dynamique du batch size
        current_speed = performance_metrics.get('processing_speed', 0)
        if len(self.performance_history) > 3:
            avg_speed = sum(p.get('processing_speed', 0) 
                          for p in self.performance_history[-3:]) / 3
            
            if current_speed < avg_speed * 0.8:  # Performance dégradée
                self.context['optimal_batch_size'] = max(8, 
                    self.context['optimal_batch_size'] // 2)
            elif current_speed > avg_speed * 1.2:  # Performance améliorée
                self.context['optimal_batch_size'] = min(256, 
                    self.context['optimal_batch_size'] * 2)
        
        return self.context
    
    def get_current_recommendations(self) -> Dict[str, Any]:
        """Retourne les recommandations actuelles optimisées"""
        return self.context