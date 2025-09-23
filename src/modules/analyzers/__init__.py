"""
🧠 Analyzers Package - Analyseurs Dhātu
Collection d'analyseurs spécialisés pour traitement dhātu
"""

# Import des analyseurs disponibles
try:
    from .dhatu_analyzer import DhatuAnalyzer
    __all__ = ['DhatuAnalyzer']
except ImportError:
    __all__ = []

# Import conditionnel des analyseurs GPU
try:
    from .dhatu_gpu_t4 import DhatuGPUT4Analyzer
    __all__.append('DhatuGPUT4Analyzer')
except ImportError:
    pass