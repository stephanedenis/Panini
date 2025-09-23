#!/usr/bin/env python3
"""
Module RESILIENCE_LAYER - Gestion erreurs robuste et fallbacks automatiques

Objectif: Éliminer blocages par erreurs non-gérées via système résilience
adaptatif avec fallbacks intelligents et retry automatiques.

Architecture:
- ErrorClassifier: Classification erreurs par type et sévérité
- FallbackStrategy: Stratégies fallback selon contexte d'erreur
- RetryManager: Retry intelligent avec backoff adaptatif
- RecoveryEngine: Récupération automatique état stable

Priorité: CRITIQUE - Robustesse infrastructure
"""

import asyncio
import json
import logging
import time
import traceback
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, Any, Optional, List, Callable, Union
from dataclasses import dataclass, asdict
import functools


class ErrorSeverity(Enum):
    """Niveaux sévérité erreurs"""
    MINOR = "minor"          # Erreur récupérable automatiquement
    MODERATE = "moderate"    # Erreur nécessitant fallback
    SEVERE = "severe"        # Erreur bloquante nécessitant récupération
    CRITICAL = "critical"    # Erreur système nécessitant arrêt


class ErrorCategory(Enum):
    """Catégories erreurs pour stratégies ciblées"""
    NETWORK = "network"           # Erreurs réseau/API
    FILE_SYSTEM = "filesystem"    # Erreurs fichiers/permissions
    VALIDATION = "validation"     # Erreurs validation données
    TIMEOUT = "timeout"          # Erreurs timeout
    DEPENDENCY = "dependency"     # Erreurs outils/dépendances
    UNKNOWN = "unknown"          # Erreurs non classifiées


class FallbackStrategy(Enum):
    """Stratégies fallback automatiques"""
    RETRY_WITH_BACKOFF = "retry_backoff"
    USE_DEFAULT_VALUE = "default_value" 
    SKIP_OPERATION = "skip_operation"
    ALTERNATIVE_METHOD = "alternative_method"
    GRACEFUL_DEGRADATION = "graceful_degradation"
    SAVE_AND_CONTINUE = "save_continue"


@dataclass
class ErrorContext:
    """Contexte complet erreur pour diagnostic"""
    error_type: str
    error_message: str
    severity: ErrorSeverity
    category: ErrorCategory
    operation_context: Dict[str, Any]
    timestamp: datetime
    stack_trace: str
    retry_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Sérialisation pour logging"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        data['severity'] = self.severity.value
        data['category'] = self.category.value
        return data


@dataclass
class RecoveryResult:
    """Résultat tentative récupération"""
    success: bool
    strategy_used: FallbackStrategy
    result_value: Any
    recovery_time: float
    error_resolved: bool
    fallback_data: Dict[str, Any]


class ErrorClassifier:
    """Classification intelligente erreurs par type et sévérité"""
    
    def __init__(self):
        self.classification_rules = self._load_classification_rules()
        
    def _load_classification_rules(self) -> Dict[str, Any]:
        """Règles classification erreurs"""
        return {
            # Erreurs réseau
            "network_errors": {
                "patterns": [
                    "ConnectionError", "TimeoutError", "RequestException",
                    "HTTPError", "URLError", "socket.error"
                ],
                "category": ErrorCategory.NETWORK,
                "default_severity": ErrorSeverity.MODERATE
            },
            
            # Erreurs système fichiers
            "filesystem_errors": {
                "patterns": [
                    "FileNotFoundError", "PermissionError", "OSError",
                    "IOError", "IsADirectoryError", "NotADirectoryError"
                ],
                "category": ErrorCategory.FILE_SYSTEM,
                "default_severity": ErrorSeverity.MODERATE
            },
            
            # Erreurs validation
            "validation_errors": {
                "patterns": [
                    "ValueError", "TypeError", "KeyError", "IndexError",
                    "AttributeError", "ValidationError"
                ],
                "category": ErrorCategory.VALIDATION,
                "default_severity": ErrorSeverity.MINOR
            },
            
            # Erreurs timeout
            "timeout_errors": {
                "patterns": [
                    "TimeoutError", "asyncio.TimeoutError", "socket.timeout",
                    "requests.exceptions.Timeout"
                ],
                "category": ErrorCategory.TIMEOUT,
                "default_severity": ErrorSeverity.MODERATE
            },
            
            # Erreurs dépendances
            "dependency_errors": {
                "patterns": [
                    "ImportError", "ModuleNotFoundError", "CalledProcessError",
                    "SubprocessError", "CommandNotFound"
                ],
                "category": ErrorCategory.DEPENDENCY,
                "default_severity": ErrorSeverity.SEVERE
            }
        }
    
    def classify_error(self, error: Exception, context: Dict[str, Any] = None) -> ErrorContext:
        """Classification erreur avec contexte"""
        error_type = type(error).__name__
        error_message = str(error)
        stack_trace = traceback.format_exc()
        
        # Classification par patterns
        category = ErrorCategory.UNKNOWN
        severity = ErrorSeverity.MODERATE
        
        for rule_name, rule_data in self.classification_rules.items():
            if any(pattern in error_type for pattern in rule_data["patterns"]) or \
               any(pattern in error_message for pattern in rule_data["patterns"]):
                category = rule_data["category"]
                severity = rule_data["default_severity"]
                break
        
        # Ajustement sévérité selon contexte
        if context:
            operation_criticality = context.get('criticality', 'normal')
            if operation_criticality == 'critical' and severity == ErrorSeverity.MINOR:
                severity = ErrorSeverity.MODERATE
            elif operation_criticality == 'low' and severity == ErrorSeverity.MODERATE:
                severity = ErrorSeverity.MINOR
        
        return ErrorContext(
            error_type=error_type,
            error_message=error_message,
            severity=severity,
            category=category,
            operation_context=context or {},
            timestamp=datetime.now(),
            stack_trace=stack_trace
        )


class RetryManager:
    """Gestionnaire retry intelligent avec backoff adaptatif"""
    
    def __init__(self):
        self.retry_strategies = self._load_retry_strategies()
        
    def _load_retry_strategies(self) -> Dict[ErrorCategory, Dict[str, Any]]:
        """Stratégies retry par catégorie erreur"""
        return {
            ErrorCategory.NETWORK: {
                "max_retries": 5,
                "base_delay": 1.0,
                "max_delay": 60.0,
                "backoff_factor": 2.0,
                "jitter": True
            },
            ErrorCategory.TIMEOUT: {
                "max_retries": 3,
                "base_delay": 2.0,
                "max_delay": 30.0,
                "backoff_factor": 1.5,
                "jitter": False
            },
            ErrorCategory.FILE_SYSTEM: {
                "max_retries": 3,
                "base_delay": 0.5,
                "max_delay": 10.0,
                "backoff_factor": 2.0,
                "jitter": True
            },
            ErrorCategory.VALIDATION: {
                "max_retries": 1,
                "base_delay": 0.1,
                "max_delay": 1.0,
                "backoff_factor": 1.0,
                "jitter": False
            },
            ErrorCategory.DEPENDENCY: {
                "max_retries": 2,
                "base_delay": 5.0,
                "max_delay": 120.0,
                "backoff_factor": 3.0,
                "jitter": True
            },
            ErrorCategory.UNKNOWN: {
                "max_retries": 2,
                "base_delay": 1.0,
                "max_delay": 10.0,
                "backoff_factor": 2.0,
                "jitter": True
            }
        }
    
    def should_retry(self, error_context: ErrorContext) -> bool:
        """Détermine si retry approprié"""
        strategy = self.retry_strategies.get(error_context.category)
        if not strategy:
            return False
            
        return error_context.retry_count < strategy["max_retries"]
    
    def calculate_delay(self, error_context: ErrorContext) -> float:
        """Calcul délai retry avec backoff"""
        strategy = self.retry_strategies.get(error_context.category)
        if not strategy:
            return 1.0
            
        base_delay = strategy["base_delay"]
        backoff_factor = strategy["backoff_factor"]
        max_delay = strategy["max_delay"]
        jitter = strategy["jitter"]
        
        # Calcul backoff exponentiel
        delay = base_delay * (backoff_factor ** error_context.retry_count)
        delay = min(delay, max_delay)
        
        # Ajout jitter pour éviter thundering herd
        if jitter:
            import random
            delay *= (0.5 + random.random() * 0.5)
            
        return delay


class FallbackEngine:
    """Moteur fallbacks automatiques selon contexte"""
    
    def __init__(self):
        self.fallback_registry = self._load_fallback_registry()
        
    def _load_fallback_registry(self) -> Dict[str, Any]:
        """Registre stratégies fallback"""
        return {
            ErrorCategory.NETWORK: [
                FallbackStrategy.RETRY_WITH_BACKOFF,
                FallbackStrategy.USE_DEFAULT_VALUE,
                FallbackStrategy.GRACEFUL_DEGRADATION
            ],
            ErrorCategory.FILE_SYSTEM: [
                FallbackStrategy.ALTERNATIVE_METHOD,
                FallbackStrategy.USE_DEFAULT_VALUE,
                FallbackStrategy.SKIP_OPERATION
            ],
            ErrorCategory.VALIDATION: [
                FallbackStrategy.USE_DEFAULT_VALUE,
                FallbackStrategy.SKIP_OPERATION,
                FallbackStrategy.GRACEFUL_DEGRADATION
            ],
            ErrorCategory.TIMEOUT: [
                FallbackStrategy.SAVE_AND_CONTINUE,
                FallbackStrategy.RETRY_WITH_BACKOFF,
                FallbackStrategy.SKIP_OPERATION
            ],
            ErrorCategory.DEPENDENCY: [
                FallbackStrategy.ALTERNATIVE_METHOD,
                FallbackStrategy.GRACEFUL_DEGRADATION,
                FallbackStrategy.SKIP_OPERATION
            ]
        }
    
    def get_fallback_strategy(self, error_context: ErrorContext, 
                             operation_context: Dict[str, Any]) -> FallbackStrategy:
        """Sélection stratégie fallback optimale"""
        available_strategies = self.fallback_registry.get(
            error_context.category, 
            [FallbackStrategy.SKIP_OPERATION]
        )
        
        # Sélection selon criticité opération
        criticality = operation_context.get('criticality', 'normal')
        has_alternatives = operation_context.get('has_alternatives', False)
        can_use_defaults = operation_context.get('can_use_defaults', True)
        
        if criticality == 'critical':
            # Opération critique - essayer alternatives d'abord
            if has_alternatives and FallbackStrategy.ALTERNATIVE_METHOD in available_strategies:
                return FallbackStrategy.ALTERNATIVE_METHOD
            elif FallbackStrategy.RETRY_WITH_BACKOFF in available_strategies:
                return FallbackStrategy.RETRY_WITH_BACKOFF
                
        elif criticality == 'low':
            # Opération peu critique - skip plus facilement
            if FallbackStrategy.SKIP_OPERATION in available_strategies:
                return FallbackStrategy.SKIP_OPERATION
                
        # Sélection par défaut selon disponibilité
        if can_use_defaults and FallbackStrategy.USE_DEFAULT_VALUE in available_strategies:
            return FallbackStrategy.USE_DEFAULT_VALUE
        elif has_alternatives and FallbackStrategy.ALTERNATIVE_METHOD in available_strategies:
            return FallbackStrategy.ALTERNATIVE_METHOD
        else:
            return available_strategies[0] if available_strategies else FallbackStrategy.SKIP_OPERATION


class RecoveryEngine:
    """Moteur récupération automatique état stable"""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = Path(workspace_root)
        self.recovery_log_dir = self.workspace_root / "copilotage" / "autonomie" / "recovery"
        self.recovery_log_dir.mkdir(parents=True, exist_ok=True)
        
        self.recovery_strategies = self._load_recovery_strategies()
        
    def _load_recovery_strategies(self) -> Dict[FallbackStrategy, Callable]:
        """Mapping stratégies → implémentations"""
        return {
            FallbackStrategy.RETRY_WITH_BACKOFF: self._retry_with_backoff,
            FallbackStrategy.USE_DEFAULT_VALUE: self._use_default_value,
            FallbackStrategy.SKIP_OPERATION: self._skip_operation,
            FallbackStrategy.ALTERNATIVE_METHOD: self._try_alternative_method,
            FallbackStrategy.GRACEFUL_DEGRADATION: self._graceful_degradation,
            FallbackStrategy.SAVE_AND_CONTINUE: self._save_and_continue
        }
    
    async def recover_from_error(self, error_context: ErrorContext, 
                               operation_func: Callable,
                               fallback_strategy: FallbackStrategy,
                               operation_context: Dict[str, Any]) -> RecoveryResult:
        """Récupération erreur avec stratégie spécifiée"""
        start_time = time.time()
        
        recovery_func = self.recovery_strategies.get(fallback_strategy)
        if not recovery_func:
            return RecoveryResult(
                success=False,
                strategy_used=fallback_strategy,
                result_value=None,
                recovery_time=0.0,
                error_resolved=False,
                fallback_data={"error": "Unknown fallback strategy"}
            )
        
        try:
            result = await recovery_func(
                error_context, operation_func, operation_context
            )
            
            recovery_time = time.time() - start_time
            
            return RecoveryResult(
                success=True,
                strategy_used=fallback_strategy,
                result_value=result,
                recovery_time=recovery_time,
                error_resolved=True,
                fallback_data={"strategy": fallback_strategy.value}
            )
            
        except Exception as recovery_error:
            recovery_time = time.time() - start_time
            
            return RecoveryResult(
                success=False,
                strategy_used=fallback_strategy,
                result_value=None,
                recovery_time=recovery_time,
                error_resolved=False,
                fallback_data={
                    "recovery_error": str(recovery_error),
                    "original_error": error_context.error_message
                }
            )
    
    async def _retry_with_backoff(self, error_context: ErrorContext,
                                operation_func: Callable,
                                operation_context: Dict[str, Any]) -> Any:
        """Retry avec backoff adaptatif"""
        retry_manager = RetryManager()
        
        for attempt in range(error_context.retry_count, 
                           retry_manager.retry_strategies[error_context.category]["max_retries"]):
            
            if attempt > 0:
                delay = retry_manager.calculate_delay(error_context)
                await asyncio.sleep(delay)
            
            try:
                return await self._call_async_if_needed(operation_func)
            except Exception as e:
                error_context.retry_count = attempt + 1
                if attempt == retry_manager.retry_strategies[error_context.category]["max_retries"] - 1:
                    raise e
                    
        raise Exception("Max retries exceeded")
    
    async def _use_default_value(self, error_context: ErrorContext,
                               operation_func: Callable,
                               operation_context: Dict[str, Any]) -> Any:
        """Utilisation valeur par défaut"""
        default_value = operation_context.get('default_value')
        if default_value is not None:
            return default_value
            
        # Valeurs par défaut selon type opération
        operation_type = operation_context.get('operation_type', 'unknown')
        defaults = {
            'file_read': '',
            'api_call': {},
            'computation': 0,
            'list_operation': [],
            'boolean_check': False
        }
        
        return defaults.get(operation_type, None)
    
    async def _skip_operation(self, error_context: ErrorContext,
                            operation_func: Callable,
                            operation_context: Dict[str, Any]) -> Any:
        """Skip opération avec logging"""
        skip_reason = f"Skipped due to {error_context.category.value} error: {error_context.error_message}"
        
        # Log skip pour traçabilité
        skip_log = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation_context.get('operation_type', 'unknown'),
            "reason": skip_reason,
            "error_context": error_context.to_dict()
        }
        
        skip_log_file = self.recovery_log_dir / "skipped_operations.json"
        with open(skip_log_file, 'a') as f:
            f.write(json.dumps(skip_log) + '\n')
            
        return None
    
    async def _try_alternative_method(self, error_context: ErrorContext,
                                    operation_func: Callable,
                                    operation_context: Dict[str, Any]) -> Any:
        """Tentative méthode alternative"""
        alternative_func = operation_context.get('alternative_function')
        if alternative_func:
            return await self._call_async_if_needed(alternative_func)
            
        # Méthodes alternatives par défaut selon catégorie
        if error_context.category == ErrorCategory.FILE_SYSTEM:
            # Alternative: créer répertoire parent si nécessaire
            file_path = operation_context.get('file_path')
            if file_path:
                Path(file_path).parent.mkdir(parents=True, exist_ok=True)
                return await self._call_async_if_needed(operation_func)
                
        elif error_context.category == ErrorCategory.NETWORK:
            # Alternative: mode offline si disponible
            offline_func = operation_context.get('offline_function')
            if offline_func:
                return await self._call_async_if_needed(offline_func)
                
        raise Exception("No alternative method available")
    
    async def _graceful_degradation(self, error_context: ErrorContext,
                                  operation_func: Callable,
                                  operation_context: Dict[str, Any]) -> Any:
        """Dégradation gracieuse avec fonctionnalité réduite"""
        # Implémentation mode dégradé selon contexte
        degraded_func = operation_context.get('degraded_function')
        if degraded_func:
            return await self._call_async_if_needed(degraded_func)
            
        # Mode dégradé par défaut - version simplifiée
        simplified_result = operation_context.get('simplified_result', {})
        return simplified_result
    
    async def _save_and_continue(self, error_context: ErrorContext,
                               operation_func: Callable,
                               operation_context: Dict[str, Any]) -> Any:
        """Sauvegarde état et continuation"""
        # Sauvegarde état actuel pour reprise ultérieure
        save_data = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation_context.get('operation_type'),
            "state": operation_context.get('current_state', {}),
            "error": error_context.to_dict()
        }
        
        save_file = self.recovery_log_dir / f"saved_state_{int(time.time())}.json"
        with open(save_file, 'w') as f:
            json.dump(save_data, f, indent=2)
            
        # Continue avec valeur par défaut ou None
        return operation_context.get('continue_value')
    
    async def _call_async_if_needed(self, func: Callable) -> Any:
        """Appel fonction async ou sync selon type"""
        if asyncio.iscoroutinefunction(func):
            return await func()
        else:
            return func()


class ResilienceLayer:
    """Couche résilience principale intégrant tous composants"""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = Path(workspace_root)
        
        # Composants résilience
        self.error_classifier = ErrorClassifier()
        self.retry_manager = RetryManager()
        self.fallback_engine = FallbackEngine()
        self.recovery_engine = RecoveryEngine(workspace_root)
        
        # Configuration logging
        self.logger = self._setup_logger()
        
        # Métriques résilience
        self.metrics = {
            "total_errors": 0,
            "recovered_errors": 0,
            "failed_recoveries": 0,
            "recovery_times": []
        }
    
    def _setup_logger(self) -> logging.Logger:
        """Configuration logger résilience"""
        logger = logging.getLogger("resilience_layer")
        logger.setLevel(logging.INFO)
        
        log_dir = self.workspace_root / "copilotage" / "autonomie" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        handler = logging.FileHandler(log_dir / "resilience.log")
        formatter = logging.Formatter(
            '%(asctime)s - RESILIENCE - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def resilient_execute(self, operation_func: Callable, 
                         operation_context: Dict[str, Any] = None) -> Any:
        """Exécution résiliente avec gestion erreurs complète"""
        if operation_context is None:
            operation_context = {}
            
        async def _execute():
            try:
                # Tentative exécution normale
                return await self.recovery_engine._call_async_if_needed(operation_func)
                
            except Exception as e:
                self.metrics["total_errors"] += 1
                
                # Classification erreur
                error_context = self.error_classifier.classify_error(e, operation_context)
                
                self.logger.error(f"Error classified: {json.dumps(error_context.to_dict())}")
                
                # Vérification possibilité retry
                if self.retry_manager.should_retry(error_context):
                    error_context.retry_count += 1
                    
                    try:
                        delay = self.retry_manager.calculate_delay(error_context)
                        await asyncio.sleep(delay)
                        
                        # Retry récursif
                        return await _execute()
                        
                    except Exception as retry_error:
                        # Échec retry - passage aux fallbacks
                        error_context = self.error_classifier.classify_error(
                            retry_error, operation_context
                        )
                
                # Sélection stratégie fallback
                fallback_strategy = self.fallback_engine.get_fallback_strategy(
                    error_context, operation_context
                )
                
                self.logger.info(f"Using fallback strategy: {fallback_strategy.value}")
                
                # Récupération avec fallback
                recovery_result = await self.recovery_engine.recover_from_error(
                    error_context, operation_func, fallback_strategy, operation_context
                )
                
                # Mise à jour métriques
                if recovery_result.success:
                    self.metrics["recovered_errors"] += 1
                else:
                    self.metrics["failed_recoveries"] += 1
                    
                self.metrics["recovery_times"].append(recovery_result.recovery_time)
                
                self.logger.info(f"Recovery result: {json.dumps(asdict(recovery_result))}")
                
                if recovery_result.success:
                    return recovery_result.result_value
                else:
                    # Échec récupération - erreur finale
                    final_error = Exception(
                        f"Resilience layer failed to recover from error: {error_context.error_message}"
                    )
                    self.logger.error(f"Final error: {final_error}")
                    raise final_error
        
        # Exécution asyncio même pour fonctions sync
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        return loop.run_until_complete(_execute())
    
    def get_resilience_metrics(self) -> Dict[str, Any]:
        """Métriques performance résilience"""
        total_operations = self.metrics["total_errors"] + self.metrics["recovered_errors"]
        
        if total_operations > 0:
            success_rate = self.metrics["recovered_errors"] / total_operations
        else:
            success_rate = 1.0
            
        avg_recovery_time = (
            sum(self.metrics["recovery_times"]) / len(self.metrics["recovery_times"])
            if self.metrics["recovery_times"] else 0.0
        )
        
        return {
            "total_errors": self.metrics["total_errors"],
            "recovered_errors": self.metrics["recovered_errors"],
            "failed_recoveries": self.metrics["failed_recoveries"],
            "success_rate": success_rate,
            "average_recovery_time": avg_recovery_time,
            "total_operations": total_operations
        }


def create_resilience_layer(workspace_root: str) -> ResilienceLayer:
    """Factory création couche résilience"""
    return ResilienceLayer(Path(workspace_root))


# Décorateur pour exécution résiliente
def resilient(operation_context: Dict[str, Any] = None):
    """Décorateur pour rendre fonction résiliente"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Récupération couche résilience depuis contexte global ou création
            resilience = getattr(wrapper, '_resilience_layer', None)
            if not resilience:
                # Création instance par défaut
                resilience = create_resilience_layer("/home/stephane/GitHub/PaniniFS-Research")
                wrapper._resilience_layer = resilience
            
            # Exécution résiliente
            return resilience.resilient_execute(
                lambda: func(*args, **kwargs),
                operation_context or {}
            )
        return wrapper
    return decorator


if __name__ == "__main__":
    # Test couche résilience
    resilience = create_resilience_layer("/home/stephane/GitHub/PaniniFS-Research")
    
    # Test fonction avec erreur réseau
    def simulate_network_error():
        import random
        if random.random() < 0.7:  # 70% chance d'erreur
            raise ConnectionError("Network unreachable")
        return "Success!"
    
    # Test résilience
    try:
        result = resilience.resilient_execute(
            simulate_network_error,
            {
                "operation_type": "api_call",
                "criticality": "normal",
                "default_value": "Offline mode",
                "can_use_defaults": True
            }
        )
        print(f"Résultat résilient: {result}")
        
        # Affichage métriques
        metrics = resilience.get_resilience_metrics()
        print(f"Métriques résilience: {json.dumps(metrics, indent=2)}")
        
    except Exception as e:
        print(f"Erreur non récupérable: {e}")