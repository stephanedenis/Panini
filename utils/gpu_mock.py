"""
Mock GPU pour développement local (Solution 3)

Permet de développer et tester du code GPU sur CPU.
Le même code s'exécute ensuite sur Colab avec un vrai GPU.

Usage:
    # En début de script
    from utils.gpu_mock import setup_device
    
    device = setup_device()  # GPU si dispo, sinon CPU avec mock
    
    # Utiliser normalement
    model = model.to(device)
    data = data.to(device)

Features:
    - Détection automatique GPU/CPU
    - Mock transparent de torch.cuda
    - Messages informatifs
    - Compatible avec tout code PyTorch
"""

import sys
from typing import Optional

def setup_device(force_cpu: bool = False, verbose: bool = True):
    """
    Setup device approprié (GPU ou CPU avec mock)
    
    Args:
        force_cpu: Forcer CPU même si GPU disponible (pour tests)
        verbose: Afficher messages informatifs
    
    Returns:
        torch.device: Device à utiliser (cuda ou cpu)
    """
    try:
        import torch
    except ImportError:
        if verbose:
            print("⚠️  PyTorch non installé, impossible d'utiliser GPU")
        return None
    
    # Check GPU disponible
    if not force_cpu and torch.cuda.is_available():
        device = torch.device("cuda")
        if verbose:
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
            print(f"✅ GPU détecté: {gpu_name}")
            print(f"   Mémoire: {gpu_memory:.1f} GB")
            print(f"   Device: {device}")
    else:
        device = torch.device("cpu")
        if verbose:
            if force_cpu:
                print("🔧 CPU forcé pour tests (GPU disponible mais désactivé)")
            else:
                print("⚠️  Aucun GPU détecté, utilisation du CPU")
                print("   Le code fonctionnera mais sera plus lent")
            print(f"   Device: {device}")
    
    return device


class MockGPU:
    """
    Mock de torch.cuda pour développement sans GPU
    
    Simule l'API CUDA avec des opérations CPU.
    Transparent pour le code utilisateur.
    """
    
    @staticmethod
    def is_available() -> bool:
        """GPU non disponible (mock)"""
        return False
    
    @staticmethod
    def device_count() -> int:
        """0 GPU disponibles"""
        return 0
    
    @staticmethod
    def get_device_name(device: int = 0) -> str:
        """Nom du device mocké"""
        return "CPU (Mocked GPU)"
    
    @staticmethod
    def get_device_properties(device: int = 0):
        """Propriétés mockées"""
        class MockProperties:
            name = "CPU (Mocked)"
            total_memory = 0
            major = 0
            minor = 0
        return MockProperties()
    
    @staticmethod
    def current_device() -> int:
        """Device actuel (toujours 0 en mock)"""
        return 0
    
    @staticmethod
    def synchronize():
        """Sync (no-op en CPU)"""
        pass
    
    @staticmethod
    def empty_cache():
        """Clear cache (no-op en CPU)"""
        pass


def apply_gpu_mock(verbose: bool = True):
    """
    Applique le mock GPU sur torch.cuda
    
    Permet d'exécuter du code GPU sur CPU en remplaçant
    torch.cuda par notre mock.
    
    Args:
        verbose: Afficher message d'activation
    
    Returns:
        bool: True si mock appliqué, False si GPU déjà disponible
    """
    try:
        import torch
    except ImportError:
        if verbose:
            print("⚠️  PyTorch non installé, mock GPU impossible")
        return False
    
    if torch.cuda.is_available():
        if verbose:
            print("ℹ️  GPU disponible, mock non nécessaire")
        return False
    
    # Remplacer torch.cuda par notre mock
    torch.cuda = MockGPU
    
    if verbose:
        print("🔧 GPU Mock activé")
        print("   Code GPU s'exécutera sur CPU")
        print("   Performance réduite mais logique identique")
    
    return True


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_device_info() -> dict:
    """
    Récupère infos sur le device actuel
    
    Returns:
        dict: {
            'has_gpu': bool,
            'device_type': str,
            'device_name': str,
            'device_count': int,
            'memory_gb': float or None
        }
    """
    try:
        import torch
        
        has_gpu = torch.cuda.is_available()
        
        if has_gpu:
            device_name = torch.cuda.get_device_name(0)
            device_count = torch.cuda.device_count()
            memory = torch.cuda.get_device_properties(0).total_memory / 1e9
        else:
            device_name = "CPU"
            device_count = 0
            memory = None
        
        return {
            'has_gpu': has_gpu,
            'device_type': 'cuda' if has_gpu else 'cpu',
            'device_name': device_name,
            'device_count': device_count,
            'memory_gb': memory
        }
    
    except ImportError:
        return {
            'has_gpu': False,
            'device_type': 'none',
            'device_name': 'PyTorch not installed',
            'device_count': 0,
            'memory_gb': None
        }


def print_device_info():
    """Affiche les infos device de façon lisible"""
    info = get_device_info()
    
    print("=" * 60)
    print("DEVICE INFORMATION")
    print("=" * 60)
    print(f"GPU Available: {'✅ Yes' if info['has_gpu'] else '❌ No'}")
    print(f"Device Type: {info['device_type']}")
    print(f"Device Name: {info['device_name']}")
    print(f"Device Count: {info['device_count']}")
    
    if info['memory_gb']:
        print(f"Memory: {info['memory_gb']:.1f} GB")
    
    print("=" * 60)


# ============================================================================
# AUTO-SETUP (optionnel)
# ============================================================================

def auto_setup(force_cpu: bool = False, verbose: bool = True):
    """
    Setup automatique au import
    
    Usage:
        from utils.gpu_mock import auto_setup
        device = auto_setup()  # Configure tout automatiquement
    
    Args:
        force_cpu: Forcer CPU
        verbose: Messages informatifs
    
    Returns:
        torch.device or None
    """
    device = setup_device(force_cpu=force_cpu, verbose=verbose)
    
    if device is not None and device.type == 'cpu':
        # Appliquer mock si CPU
        try:
            import torch
            if not torch.cuda.is_available():
                apply_gpu_mock(verbose=verbose)
        except ImportError:
            pass
    
    return device


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("GPU MOCK - DEMONSTRATION")
    print("=" * 60 + "\n")
    
    # Afficher infos device
    print_device_info()
    
    print("\n--- Test Setup Device ---\n")
    device = setup_device()
    
    if device:
        print(f"\n✅ Device configuré: {device}")
        
        try:
            import torch
            
            # Test basique
            print("\n--- Test PyTorch Operations ---\n")
            x = torch.randn(3, 3).to(device)
            y = torch.randn(3, 3).to(device)
            z = x @ y
            
            print(f"Matrix multiplication OK")
            print(f"Result shape: {z.shape}")
            print(f"Result device: {z.device}")
            
        except ImportError:
            print("\n⚠️  PyTorch non installé, impossible de tester")
    
    else:
        print("\n❌ Impossible de configurer device")
    
    print("\n" + "=" * 60)
