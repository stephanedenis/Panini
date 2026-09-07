"""
Module d'initialisation pour l'intégration cloud
"""

try:
    from .colab_integrator import ColabIntegrator
    __all__ = ['ColabIntegrator']
except ImportError:
    # colab_integrator est en cours de migration depuis research/
    __all__ = []