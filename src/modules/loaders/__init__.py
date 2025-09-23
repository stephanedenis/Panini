"""
📚 Loaders Package - Chargeurs de Données
Collection de chargeurs pour différents types de corpus
"""

try:
    from .corpus_loader import CorpusLoader
    __all__ = ['CorpusLoader']
except ImportError:
    __all__ = []