"""
🐍 Modules System - Architecture Modulaire

Système de modules interchangeables pour PaniniFS Research.

Structure:
- analyzers/: Analyseurs spécialisés (dhatu, GPU, etc.)
- loaders/: Chargeurs de corpus et données
- gpu/: Détection et gestion GPU
- interfaces.py: Interfaces communes
- dynamic_manager.py: Gestionnaire dynamique modules
"""

__version__ = "1.0.0"

# Import des interfaces principales
from .interfaces import AnalyzerInterface, LoaderInterface, GPUOptimizerInterface
from .dynamic_manager import DynamicModuleManager

# Aliases pour compatibilité
BaseAnalyzer = AnalyzerInterface
BaseLoader = LoaderInterface

__all__ = [
    'AnalyzerInterface',
    'LoaderInterface',
    'GPUOptimizerInterface',
    'BaseAnalyzer',  # Alias pour compatibilité
    'BaseLoader',    # Alias pour compatibilité
    'DynamicModuleManager'
]