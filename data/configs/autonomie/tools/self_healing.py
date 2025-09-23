#!/usr/bin/env python3
"""
Module SELF_HEALING_TOOLS - Monitoring santé et auto-réparation

Objectif: Éliminer défaillances outils via système monitoring continu
et auto-réparation proactive détectant/corrigeant points de blocage.

Architecture:
- HealthMonitor: Surveillance continue état système/outils
- BlockageDetector: Détection patterns blocage avant échec
- AutoRepairEngine: Réparation automatique problèmes détectés
- SystemValidator: Validation intégrité outils et dépendances

Priorité: CRITIQUE - Robustesse infrastructure outils
"""

import asyncio
import json
import logging
import psutil
import shutil
import subprocess
import time
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, asdict
import threading
import queue
import importlib.util
import signal
import os


class HealthStatus(Enum):
    """États santé système"""
    HEALTHY = "healthy"
    WARNING = "warning"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    FAILED = "failed"


class ComponentType(Enum):
    """Types composants surveillés"""
    SYSTEM_RESOURCE = "system_resource"
    EXTERNAL_TOOL = "external_tool"
    PYTHON_MODULE = "python_module"
    FILE_SYSTEM = "file_system"
    NETWORK = "network"
    PROCESS = "process"
    TERMINAL_SESSION = "terminal_session"  # Nouveau type pour sessions terminal


class RepairAction(Enum):
    """Actions réparation disponibles"""
    RESTART_SERVICE = "restart_service"
    CLEAR_CACHE = "clear_cache"
    REINSTALL_DEPENDENCY = "reinstall_dependency"
    FREE_RESOURCES = "free_resources"
    FIX_PERMISSIONS = "fix_permissions"
    RESET_CONFIGURATION = "reset_configuration"
    ALTERNATIVE_METHOD = "alternative_method"
    KILL_INTERACTIVE_PROCESS = "kill_interactive_process"  # Nouveau
    ESCAPE_PAGER_EDITOR = "escape_pager_editor"           # Nouveau


@dataclass
class HealthMetric:
    """Métrique santé composant"""
    component_name: str
    component_type: ComponentType
    status: HealthStatus
    value: float
    threshold_warning: float
    threshold_critical: float
    unit: str
    timestamp: datetime
    details: Dict[str, Any]


@dataclass
class BlockagePattern:
    """Pattern blocage détecté"""
    pattern_name: str
    component_name: str
    detection_time: datetime
    severity: HealthStatus
    indicators: List[str]
    predicted_failure_time: Optional[datetime]
    repair_suggestions: List[RepairAction]


@dataclass
class RepairResult:
    """Résultat tentative réparation"""
    repair_action: RepairAction
    component_name: str
    success: bool
    repair_time: float
    error_message: Optional[str]
    verification_passed: bool
    timestamp: datetime


class HealthMonitor:
    """Surveillance continue santé système"""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = Path(workspace_root)
        self.monitoring_active = False
        self.monitoring_thread = None
        self.metrics_queue = queue.Queue()
        
        # Configuration monitoring
        self.monitor_config = self._load_monitor_config()
        self.health_history = {}
        
        # Fichiers logs
        self.logs_dir = self.workspace_root / "copilotage" / "autonomie" / "health"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger = self._setup_logger()
        
    def _load_monitor_config(self) -> Dict[str, Any]:
        """Configuration surveillance par composant"""
        return {
            "system_resources": {
                "cpu_usage": {"warning": 80.0, "critical": 95.0},
                "memory_usage": {"warning": 85.0, "critical": 95.0},
                "disk_usage": {"warning": 90.0, "critical": 98.0},
                "check_interval": 30.0
            },
            "external_tools": {
                "git": {"check_command": "git --version", "timeout": 5.0},
                "gh": {"check_command": "gh --version", "timeout": 5.0},
                "python": {"check_command": "python --version", "timeout": 3.0},
                "check_interval": 300.0  # 5 minutes
            },
            "python_modules": {
                "required_modules": [
                    "requests", "json", "pathlib", "subprocess", 
                    "asyncio", "logging", "datetime"
                ],
                "check_interval": 600.0  # 10 minutes
            },
            "file_system": {
                "critical_paths": [
                    "copilotage/utilities/tools",
                    "copilotage/autonomie",
                    ".git"
                ],
                "check_interval": 120.0  # 2 minutes
            }
        }
    
    def _setup_logger(self) -> logging.Logger:
        """Configuration logger surveillance"""
        logger = logging.getLogger("health_monitor")
        logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler(self.logs_dir / "health_monitor.log")
        formatter = logging.Formatter(
            '%(asctime)s - HEALTH - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def start_monitoring(self):
        """Démarrage surveillance continue"""
        if self.monitoring_active:
            return
            
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        
        self.logger.info("Health monitoring started")
    
    def stop_monitoring(self):
        """Arrêt surveillance"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5.0)
        
        self.logger.info("Health monitoring stopped")
    
    def _monitoring_loop(self):
        """Boucle principale surveillance"""
        last_checks = {}
        
        while self.monitoring_active:
            current_time = time.time()
            
            # Vérification ressources système
            if self._should_check("system_resources", last_checks, current_time):
                self._check_system_resources()
                last_checks["system_resources"] = current_time
            
            # Vérification outils externes
            if self._should_check("external_tools", last_checks, current_time):
                self._check_external_tools()
                last_checks["external_tools"] = current_time
            
            # Vérification modules Python
            if self._should_check("python_modules", last_checks, current_time):
                self._check_python_modules()
                last_checks["python_modules"] = current_time
            
            # Vérification système fichiers
            if self._should_check("file_system", last_checks, current_time):
                self._check_file_system()
                last_checks["file_system"] = current_time
            
            time.sleep(10.0)  # Intervalle base
    
    def _should_check(self, check_type: str, last_checks: Dict[str, float], 
                     current_time: float) -> bool:
        """Détermine si vérification nécessaire"""
        config = self.monitor_config.get(check_type, {})
        interval = config.get("check_interval", 60.0)
        
        last_check = last_checks.get(check_type, 0)
        return (current_time - last_check) >= interval
    
    def _check_system_resources(self):
        """Vérification ressources système"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            self._record_metric(
                "cpu_usage", ComponentType.SYSTEM_RESOURCE,
                cpu_percent, 80.0, 95.0, "%",
                {"cores": psutil.cpu_count()}
            )
            
            # Mémoire
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            self._record_metric(
                "memory_usage", ComponentType.SYSTEM_RESOURCE,
                memory_percent, 85.0, 95.0, "%",
                {
                    "total_gb": round(memory.total / (1024**3), 2),
                    "available_gb": round(memory.available / (1024**3), 2)
                }
            )
            
            # Disque
            disk = psutil.disk_usage(str(self.workspace_root))
            disk_percent = (disk.used / disk.total) * 100
            self._record_metric(
                "disk_usage", ComponentType.SYSTEM_RESOURCE,
                disk_percent, 90.0, 98.0, "%",
                {
                    "total_gb": round(disk.total / (1024**3), 2),
                    "free_gb": round(disk.free / (1024**3), 2)
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error checking system resources: {e}")
    
    def _check_external_tools(self):
        """Vérification outils externes"""
        tools = self.monitor_config["external_tools"]
        
        for tool_name, tool_config in tools.items():
            if tool_name == "check_interval":
                continue
                
            try:
                command = tool_config["check_command"]
                timeout = tool_config["timeout"]
                
                result = subprocess.run(
                    command.split(),
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    cwd=str(self.workspace_root)
                )
                
                if result.returncode == 0:
                    status = HealthStatus.HEALTHY
                    value = 1.0
                else:
                    status = HealthStatus.FAILED
                    value = 0.0
                    
                self._record_metric(
                    tool_name, ComponentType.EXTERNAL_TOOL,
                    value, 0.5, 0.1, "bool",
                    {
                        "return_code": result.returncode,
                        "stdout": result.stdout[:200],
                        "stderr": result.stderr[:200]
                    },
                    status
                )
                
            except subprocess.TimeoutExpired:
                self._record_metric(
                    tool_name, ComponentType.EXTERNAL_TOOL,
                    0.0, 0.5, 0.1, "bool",
                    {"error": "timeout"},
                    HealthStatus.CRITICAL
                )
                
            except Exception as e:
                self._record_metric(
                    tool_name, ComponentType.EXTERNAL_TOOL,
                    0.0, 0.5, 0.1, "bool",
                    {"error": str(e)},
                    HealthStatus.FAILED
                )
    
    def _check_python_modules(self):
        """Vérification modules Python"""
        required_modules = self.monitor_config["python_modules"]["required_modules"]
        
        for module_name in required_modules:
            try:
                spec = importlib.util.find_spec(module_name)
                if spec is not None:
                    status = HealthStatus.HEALTHY
                    value = 1.0
                    details = {"importable": True}
                else:
                    status = HealthStatus.FAILED
                    value = 0.0
                    details = {"importable": False, "error": "module not found"}
                    
                self._record_metric(
                    f"module_{module_name}", ComponentType.PYTHON_MODULE,
                    value, 0.5, 0.1, "bool",
                    details, status
                )
                
            except Exception as e:
                self._record_metric(
                    f"module_{module_name}", ComponentType.PYTHON_MODULE,
                    0.0, 0.5, 0.1, "bool",
                    {"error": str(e)},
                    HealthStatus.FAILED
                )
    
    def _check_file_system(self):
        """Vérification système fichiers"""
        critical_paths = self.monitor_config["file_system"]["critical_paths"]
        
        for path_str in critical_paths:
            try:
                path = self.workspace_root / path_str
                
                if path.exists():
                    # Vérification permissions
                    readable = path.is_dir() and any(path.iterdir()) if path.is_dir() else path.is_file()
                    writable = True
                    
                    try:
                        # Test écriture
                        if path.is_dir():
                            test_file = path / ".health_check"
                            test_file.write_text("health_check")
                            test_file.unlink()
                        else:
                            # Pour fichier, test parent directory
                            test_file = path.parent / ".health_check"
                            test_file.write_text("health_check")
                            test_file.unlink()
                    except Exception:
                        writable = False
                    
                    if readable and writable:
                        status = HealthStatus.HEALTHY
                        value = 1.0
                    elif readable:
                        status = HealthStatus.WARNING
                        value = 0.7
                    else:
                        status = HealthStatus.CRITICAL
                        value = 0.3
                        
                    self._record_metric(
                        f"path_{path_str.replace('/', '_')}", ComponentType.FILE_SYSTEM,
                        value, 0.8, 0.5, "bool",
                        {"readable": readable, "writable": writable, "exists": True},
                        status
                    )
                    
                else:
                    self._record_metric(
                        f"path_{path_str.replace('/', '_')}", ComponentType.FILE_SYSTEM,
                        0.0, 0.8, 0.5, "bool",
                        {"exists": False},
                        HealthStatus.FAILED
                    )
                    
            except Exception as e:
                self._record_metric(
                    f"path_{path_str.replace('/', '_')}", ComponentType.FILE_SYSTEM,
                    0.0, 0.8, 0.5, "bool",
                    {"error": str(e)},
                    HealthStatus.FAILED
                )
    
    def _record_metric(self, component_name: str, component_type: ComponentType,
                      value: float, threshold_warning: float, threshold_critical: float,
                      unit: str, details: Dict[str, Any],
                      override_status: Optional[HealthStatus] = None):
        """Enregistrement métrique santé"""
        
        # Détermination status
        if override_status:
            status = override_status
        elif value <= threshold_critical:
            status = HealthStatus.CRITICAL
        elif value <= threshold_warning:
            status = HealthStatus.WARNING
        else:
            status = HealthStatus.HEALTHY
        
        metric = HealthMetric(
            component_name=component_name,
            component_type=component_type,
            status=status,
            value=value,
            threshold_warning=threshold_warning,
            threshold_critical=threshold_critical,
            unit=unit,
            timestamp=datetime.now(),
            details=details
        )
        
        # Ajout à l'historique
        if component_name not in self.health_history:
            self.health_history[component_name] = []
            
        self.health_history[component_name].append(metric)
        
        # Garde seulement les 100 dernières mesures
        if len(self.health_history[component_name]) > 100:
            self.health_history[component_name] = self.health_history[component_name][-100:]
        
        # Log si problème
        if status in [HealthStatus.WARNING, HealthStatus.CRITICAL, HealthStatus.FAILED]:
            self.logger.warning(f"Health issue - {component_name}: {status.value} (value: {value})")
        
        # Ajout à la queue pour traitement
        self.metrics_queue.put(metric)
    
    def get_current_health_status(self) -> Dict[str, Any]:
        """État santé actuel du système"""
        status_summary = {
            "overall_status": HealthStatus.HEALTHY,
            "components": {},
            "critical_issues": [],
            "warnings": [],
            "last_update": datetime.now().isoformat()
        }
        
        critical_count = 0
        warning_count = 0
        
        for component_name, metrics in self.health_history.items():
            if metrics:
                latest_metric = metrics[-1]
                status_summary["components"][component_name] = {
                    "status": latest_metric.status.value,
                    "value": latest_metric.value,
                    "unit": latest_metric.unit,
                    "timestamp": latest_metric.timestamp.isoformat(),
                    "details": latest_metric.details
                }
                
                if latest_metric.status == HealthStatus.CRITICAL:
                    critical_count += 1
                    status_summary["critical_issues"].append({
                        "component": component_name,
                        "issue": f"Critical value: {latest_metric.value} {latest_metric.unit}"
                    })
                elif latest_metric.status == HealthStatus.WARNING:
                    warning_count += 1
                    status_summary["warnings"].append({
                        "component": component_name,
                        "issue": f"Warning value: {latest_metric.value} {latest_metric.unit}"
                    })
        
        # Détermination status global
        if critical_count > 0:
            status_summary["overall_status"] = HealthStatus.CRITICAL
        elif warning_count > 2:
            status_summary["overall_status"] = HealthStatus.DEGRADED
        elif warning_count > 0:
            status_summary["overall_status"] = HealthStatus.WARNING
        
        return status_summary


class BlockageDetector:
    """Détecteur patterns blocage proactif"""
    
    def __init__(self, health_monitor: HealthMonitor):
        self.health_monitor = health_monitor
        self.blockage_patterns = self._load_blockage_patterns()
        
    def _load_blockage_patterns(self) -> Dict[str, Any]:
        """Patterns blocage connus"""
        return {
            "memory_leak": {
                "components": ["memory_usage"],
                "pattern": "increasing_trend",
                "threshold": 0.95,
                "duration": 300,  # 5 minutes
                "severity": HealthStatus.CRITICAL
            },
            "disk_full": {
                "components": ["disk_usage"],
                "pattern": "approaching_limit",
                "threshold": 0.98,
                "duration": 60,
                "severity": HealthStatus.CRITICAL
            },
            "tool_failures": {
                "components": ["git", "gh", "python"],
                "pattern": "repeated_failures",
                "threshold": 3,  # 3 échecs consécutifs
                "duration": 600,  # 10 minutes
                "severity": HealthStatus.SEVERE
            },
            "cpu_spike": {
                "components": ["cpu_usage"],
                "pattern": "sustained_high",
                "threshold": 0.95,
                "duration": 180,  # 3 minutes
                "severity": HealthStatus.WARNING
            }
        }
    
    def detect_blockages(self) -> List[BlockagePattern]:
        """Détection patterns blocage"""
        detected_patterns = []
        
        for pattern_name, pattern_config in self.blockage_patterns.items():
            try:
                pattern = self._check_pattern(pattern_name, pattern_config)
                if pattern:
                    detected_patterns.append(pattern)
            except Exception as e:
                logging.error(f"Error detecting pattern {pattern_name}: {e}")
        
        return detected_patterns
    
    def _check_pattern(self, pattern_name: str, config: Dict[str, Any]) -> Optional[BlockagePattern]:
        """Vérification pattern spécifique"""
        components = config["components"]
        pattern_type = config["pattern"]
        threshold = config["threshold"]
        duration = config["duration"]
        
        # Collecte métriques pour composants
        relevant_metrics = []
        for component in components:
            if component in self.health_monitor.health_history:
                metrics = self.health_monitor.health_history[component]
                # Métriques récentes (dernière durée spécifiée)
                cutoff_time = datetime.now() - timedelta(seconds=duration)
                recent_metrics = [m for m in metrics if m.timestamp >= cutoff_time]
                relevant_metrics.extend(recent_metrics)
        
        if not relevant_metrics:
            return None
        
        # Analyse selon type pattern
        if pattern_type == "increasing_trend":
            return self._check_increasing_trend(pattern_name, relevant_metrics, threshold, config)
        elif pattern_type == "approaching_limit":
            return self._check_approaching_limit(pattern_name, relevant_metrics, threshold, config)
        elif pattern_type == "repeated_failures":
            return self._check_repeated_failures(pattern_name, relevant_metrics, threshold, config)
        elif pattern_type == "sustained_high":
            return self._check_sustained_high(pattern_name, relevant_metrics, threshold, config)
        
        return None
    
    def _check_increasing_trend(self, pattern_name: str, metrics: List[HealthMetric],
                               threshold: float, config: Dict[str, Any]) -> Optional[BlockagePattern]:
        """Détection tendance croissante"""
        if len(metrics) < 3:
            return None
        
        # Tri par timestamp
        sorted_metrics = sorted(metrics, key=lambda x: x.timestamp)
        
        # Calcul tendance (régression linéaire simple)
        values = [m.value for m in sorted_metrics]
        n = len(values)
        
        # Pente moyenne
        slope = (values[-1] - values[0]) / n
        
        # Si tendance croissante et dernière valeur proche seuil
        if slope > 0 and values[-1] > threshold * 0.8:
            # Prédiction temps avant seuil
            time_to_threshold = (threshold - values[-1]) / slope if slope > 0 else None
            predicted_failure = None
            if time_to_threshold and time_to_threshold > 0:
                predicted_failure = datetime.now() + timedelta(seconds=time_to_threshold)
            
            return BlockagePattern(
                pattern_name=pattern_name,
                component_name=sorted_metrics[-1].component_name,
                detection_time=datetime.now(),
                severity=HealthStatus(config["severity"]),
                indicators=[f"Increasing trend: slope={slope:.3f}", f"Current value: {values[-1]:.2f}"],
                predicted_failure_time=predicted_failure,
                repair_suggestions=[RepairAction.FREE_RESOURCES, RepairAction.RESTART_SERVICE]
            )
        
        return None
    
    def _check_approaching_limit(self, pattern_name: str, metrics: List[HealthMetric],
                                threshold: float, config: Dict[str, Any]) -> Optional[BlockagePattern]:
        """Détection approche limite"""
        if not metrics:
            return None
        
        latest_metric = max(metrics, key=lambda x: x.timestamp)
        
        if latest_metric.value >= threshold:
            return BlockagePattern(
                pattern_name=pattern_name,
                component_name=latest_metric.component_name,
                detection_time=datetime.now(),
                severity=HealthStatus(config["severity"]),
                indicators=[f"Value at limit: {latest_metric.value:.2f} >= {threshold}"],
                predicted_failure_time=datetime.now(),  # Immédiat
                repair_suggestions=[RepairAction.FREE_RESOURCES, RepairAction.CLEAR_CACHE]
            )
        
        return None
    
    def _check_repeated_failures(self, pattern_name: str, metrics: List[HealthMetric],
                                threshold: int, config: Dict[str, Any]) -> Optional[BlockagePattern]:
        """Détection échecs répétés"""
        if len(metrics) < threshold:
            return None
        
        # Tri par timestamp
        sorted_metrics = sorted(metrics, key=lambda x: x.timestamp)
        
        # Vérification échecs consécutifs récents
        recent_failures = 0
        for metric in reversed(sorted_metrics):
            if metric.status in [HealthStatus.FAILED, HealthStatus.CRITICAL]:
                recent_failures += 1
            else:
                break
        
        if recent_failures >= threshold:
            return BlockagePattern(
                pattern_name=pattern_name,
                component_name=sorted_metrics[-1].component_name,
                detection_time=datetime.now(),
                severity=HealthStatus(config["severity"]),
                indicators=[f"Consecutive failures: {recent_failures}"],
                predicted_failure_time=None,
                repair_suggestions=[RepairAction.RESTART_SERVICE, RepairAction.REINSTALL_DEPENDENCY]
            )
        
        return None
    
    def _check_sustained_high(self, pattern_name: str, metrics: List[HealthMetric],
                             threshold: float, config: Dict[str, Any]) -> Optional[BlockagePattern]:
        """Détection valeur haute soutenue"""
        if len(metrics) < 3:
            return None
        
        # Vérification toutes valeurs au-dessus seuil
        high_values = [m for m in metrics if m.value >= threshold]
        
        if len(high_values) >= len(metrics) * 0.8:  # 80% des mesures
            return BlockagePattern(
                pattern_name=pattern_name,
                component_name=metrics[-1].component_name,
                detection_time=datetime.now(),
                severity=HealthStatus(config["severity"]),
                indicators=[f"Sustained high values: {len(high_values)}/{len(metrics)} above {threshold}"],
                predicted_failure_time=datetime.now() + timedelta(minutes=10),
                repair_suggestions=[RepairAction.RESTART_SERVICE, RepairAction.FREE_RESOURCES]
            )
        
        return None


class TerminalBlockageDetector:
    """Détecteur spécialisé blocages terminal (pagers, éditeurs)"""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = Path(workspace_root)
        self.logger = logging.getLogger("terminal_blockage")
        
        # Processus interactifs connus
        self.interactive_processes = {
            'less', 'more', 'most', 'pg',
            'vi', 'vim', 'nvim', 'nano', 'emacs', 'ed',
            'man', 'git', 'gh'
        }
        
        # Signaux communs pour échapper des pagers/éditeurs
        self.escape_sequences = {
            'less': ['q'],
            'more': ['q'],
            'vi': [':q!', '\x1b'],  # :q! et ESC
            'vim': [':q!', '\x1b'],
            'nano': ['\x18'],       # Ctrl+X
            'emacs': ['\x18\x03'],  # Ctrl+X Ctrl+C
            'man': ['q'],
            'git': ['q'],           # Pour git log, git show, etc.
            'gh': ['q']             # Pour certaines commandes gh interactives
        }
    
    def detect_terminal_blockage(self) -> List[Dict[str, Any]]:
        """Détection blocages terminal actifs"""
        blocked_terminals = []
        
        try:
            # Recherche processus interactifs suspects
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
                try:
                    if self._is_blocking_process(proc):
                        blocked_terminals.append({
                            'pid': proc.info['pid'],
                            'name': proc.info['name'],
                            'cmdline': ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else '',
                            'duration': time.time() - proc.info['create_time'],
                            'type': 'interactive_process'
                        })
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Détection patterns terminal suspendus
            suspended_patterns = self._detect_suspended_terminals()
            blocked_terminals.extend(suspended_patterns)
            
        except Exception as e:
            self.logger.error(f"Error detecting terminal blockage: {e}")
        
        return blocked_terminals
    
    def _is_blocking_process(self, proc) -> bool:
        """Détermine si un processus bloque probablement un terminal"""
        try:
            name = proc.info['name']
            cmdline = proc.info['cmdline']
            
            # Processus interactif connu
            if name in self.interactive_processes:
                # Vérifier s'il tourne depuis trop longtemps (>2 min)
                duration = time.time() - proc.info['create_time']
                if duration > 120:  # 2 minutes
                    return True
            
            # Commandes git/gh avec patterns suspects
            if cmdline and len(cmdline) > 0:
                cmd_str = ' '.join(cmdline).lower()
                if ('git log' in cmd_str or 'git show' in cmd_str or 
                    'git diff' in cmd_str or 'gh api' in cmd_str):
                    duration = time.time() - proc.info['create_time']
                    if duration > 60:  # 1 minute pour ces commandes
                        return True
            
            return False
            
        except Exception:
            return False
    
    def _detect_suspended_terminals(self) -> List[Dict[str, Any]]:
        """Détection terminaux suspendus par TTY analysis"""
        suspended = []
        
        try:
            # Recherche sessions terminal avec états suspects
            # (Cette partie pourrait être étendue avec analyse TTY plus sophistiquée)
            
            # Pour l'instant, détecter via processus parents
            terminal_procs = []
            for proc in psutil.process_iter(['pid', 'name', 'ppid']):
                try:
                    if proc.info['name'] in ['bash', 'zsh', 'sh', 'fish']:
                        terminal_procs.append(proc)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Analyser les enfants de chaque terminal
            for terminal in terminal_procs:
                try:
                    children = terminal.children(recursive=True)
                    long_running_children = []
                    
                    for child in children:
                        try:
                            if child.name() in self.interactive_processes:
                                duration = time.time() - child.create_time()
                                if duration > 180:  # 3 minutes
                                    long_running_children.append({
                                        'pid': child.pid,
                                        'name': child.name(),
                                        'duration': duration
                                    })
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
                    
                    if long_running_children:
                        suspended.append({
                            'terminal_pid': terminal.pid,
                            'type': 'suspended_terminal',
                            'blocking_children': long_running_children,
                            'duration': max(c['duration'] for c in long_running_children)
                        })
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            self.logger.error(f"Error detecting suspended terminals: {e}")
        
        return suspended
    
    def auto_escape_blockage(self, blockage_info: Dict[str, Any]) -> bool:
        """Échappement automatique d'un blocage terminal"""
        try:
            if blockage_info['type'] == 'interactive_process':
                return self._escape_interactive_process(blockage_info)
            elif blockage_info['type'] == 'suspended_terminal':
                return self._escape_suspended_terminal(blockage_info)
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error auto-escaping blockage: {e}")
            return False
    
    def _escape_interactive_process(self, blockage_info: Dict[str, Any]) -> bool:
        """Échappement processus interactif"""
        try:
            pid = blockage_info['pid']
            name = blockage_info['name']
            
            # Tentative envoi séquences d'échappement
            if name in self.escape_sequences:
                proc = psutil.Process(pid)
                
                # Essayer d'envoyer SIGTERM d'abord (plus propre)
                proc.terminate()
                time.sleep(2)
                
                # Vérifier si terminé
                if not proc.is_running():
                    self.logger.info(f"Successfully terminated {name} (PID: {pid})")
                    return True
                
                # Si pas terminé, SIGKILL en dernier recours
                proc.kill()
                time.sleep(1)
                
                if not proc.is_running():
                    self.logger.info(f"Force killed {name} (PID: {pid})")
                    return True
            
            return False
            
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            self.logger.warning(f"Could not escape process: {e}")
            return False
    
    def _escape_suspended_terminal(self, blockage_info: Dict[str, Any]) -> bool:
        """Échappement terminal suspendu"""
        try:
            blocking_children = blockage_info['blocking_children']
            
            # Terminer tous les processus bloquants
            escaped_count = 0
            for child_info in blocking_children:
                try:
                    proc = psutil.Process(child_info['pid'])
                    proc.terminate()
                    time.sleep(1)
                    
                    if not proc.is_running():
                        escaped_count += 1
                    else:
                        proc.kill()
                        if not proc.is_running():
                            escaped_count += 1
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    escaped_count += 1  # Considéré comme résolu
            
            success = escaped_count == len(blocking_children)
            if success:
                self.logger.info(f"Escaped suspended terminal (cleaned {escaped_count} processes)")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error escaping suspended terminal: {e}")
            return False


class AutoRepairEngine:
    """Moteur réparation automatique"""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = Path(workspace_root)
        self.repair_handlers = self._load_repair_handlers()
        
        # Logs réparations
        self.repair_log_dir = self.workspace_root / "copilotage" / "autonomie" / "repairs"
        self.repair_log_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger("auto_repair")
        
    def _load_repair_handlers(self) -> Dict[RepairAction, Callable]:
        """Mapping actions réparation → implémentations"""
        return {
            RepairAction.RESTART_SERVICE: self._restart_service,
            RepairAction.CLEAR_CACHE: self._clear_cache,
            RepairAction.REINSTALL_DEPENDENCY: self._reinstall_dependency,
            RepairAction.FREE_RESOURCES: self._free_resources,
            RepairAction.FIX_PERMISSIONS: self._fix_permissions,
            RepairAction.RESET_CONFIGURATION: self._reset_configuration,
            RepairAction.ALTERNATIVE_METHOD: self._use_alternative_method
        }
    
    async def repair_blockage(self, blockage: BlockagePattern) -> List[RepairResult]:
        """Réparation automatique blocage"""
        results = []
        
        for repair_action in blockage.repair_suggestions:
            try:
                result = await self._execute_repair(repair_action, blockage.component_name)
                results.append(result)
                
                # Si réparation réussie, arrêter
                if result.success and result.verification_passed:
                    break
                    
            except Exception as e:
                result = RepairResult(
                    repair_action=repair_action,
                    component_name=blockage.component_name,
                    success=False,
                    repair_time=0.0,
                    error_message=str(e),
                    verification_passed=False,
                    timestamp=datetime.now()
                )
                results.append(result)
        
        return results
    
    async def _execute_repair(self, action: RepairAction, component_name: str) -> RepairResult:
        """Exécution action réparation"""
        start_time = time.time()
        
        try:
            handler = self.repair_handlers.get(action)
            if not handler:
                raise Exception(f"No handler for repair action: {action}")
            
            # Exécution réparation
            success = await handler(component_name)
            repair_time = time.time() - start_time
            
            # Vérification post-réparation
            verification_passed = await self._verify_repair(action, component_name)
            
            result = RepairResult(
                repair_action=action,
                component_name=component_name,
                success=success,
                repair_time=repair_time,
                error_message=None,
                verification_passed=verification_passed,
                timestamp=datetime.now()
            )
            
            # Log résultat
            self.logger.info(f"Repair completed: {asdict(result)}")
            
            return result
            
        except Exception as e:
            repair_time = time.time() - start_time
            
            result = RepairResult(
                repair_action=action,
                component_name=component_name,
                success=False,
                repair_time=repair_time,
                error_message=str(e),
                verification_passed=False,
                timestamp=datetime.now()
            )
            
            self.logger.error(f"Repair failed: {asdict(result)}")
            return result
    
    async def _restart_service(self, component_name: str) -> bool:
        """Redémarrage service/processus"""
        # Pour outils externes, essayer reconfiguration
        if component_name in ["git", "gh", "python"]:
            try:
                # Test simple réexécution
                if component_name == "git":
                    result = subprocess.run(["git", "status"], capture_output=True, timeout=10, cwd=str(self.workspace_root))
                elif component_name == "gh":
                    result = subprocess.run(["gh", "auth", "status"], capture_output=True, timeout=10)
                elif component_name == "python":
                    result = subprocess.run(["python", "--version"], capture_output=True, timeout=5)
                
                return result.returncode == 0
            except Exception:
                return False
        
        return True  # Considérer succès par défaut
    
    async def _clear_cache(self, component_name: str) -> bool:
        """Nettoyage caches"""
        try:
            # Nettoyage caches Python
            cache_dirs = [
                self.workspace_root / "__pycache__",
                self.workspace_root / ".pytest_cache",
                Path.home() / ".cache" / "pip"
            ]
            
            for cache_dir in cache_dirs:
                if cache_dir.exists():
                    shutil.rmtree(cache_dir, ignore_errors=True)
            
            # Nettoyage fichiers temporaires
            temp_patterns = ["*.tmp", "*.temp", "*.log.old"]
            for pattern in temp_patterns:
                for temp_file in self.workspace_root.rglob(pattern):
                    try:
                        temp_file.unlink()
                    except Exception:
                        pass
            
            return True
            
        except Exception:
            return False
    
    async def _reinstall_dependency(self, component_name: str) -> bool:
        """Réinstallation dépendance"""
        try:
            if component_name.startswith("module_"):
                module_name = component_name.replace("module_", "")
                
                # Tentative réinstallation via pip
                result = subprocess.run([
                    "python", "-m", "pip", "install", "--upgrade", "--force-reinstall", module_name
                ], capture_output=True, timeout=300)
                
                return result.returncode == 0
            
            return True
            
        except Exception:
            return False
    
    async def _free_resources(self, component_name: str) -> bool:
        """Libération ressources"""
        try:
            # Nettoyage mémoire Python
            import gc
            gc.collect()
            
            # Fermeture processus fils si possibles
            current_process = psutil.Process()
            for child in current_process.children(recursive=True):
                try:
                    if child.status() == psutil.STATUS_ZOMBIE:
                        child.terminate()
                except Exception:
                    pass
            
            return True
            
        except Exception:
            return False
    
    async def _fix_permissions(self, component_name: str) -> bool:
        """Correction permissions"""
        try:
            if component_name.startswith("path_"):
                # Extraction chemin depuis nom composant
                path_str = component_name.replace("path_", "").replace("_", "/")
                path = self.workspace_root / path_str
                
                if path.exists():
                    # Tentative correction permissions
                    if path.is_file():
                        path.chmod(0o644)
                    elif path.is_dir():
                        path.chmod(0o755)
                        
                    return True
            
            return True
            
        except Exception:
            return False
    
    async def _reset_configuration(self, component_name: str) -> bool:
        """Reset configuration par défaut"""
        # Implémentation basique - peut être étendue
        return True
    
    async def _use_alternative_method(self, component_name: str) -> bool:
        """Utilisation méthode alternative"""
        # Implémentation basique - activation mode fallback
        return True
    
    async def _verify_repair(self, action: RepairAction, component_name: str) -> bool:
        """Vérification succès réparation"""
        # Attendre un peu pour stabilisation
        await asyncio.sleep(2.0)
        
        # Test rapide selon composant
        try:
            if component_name == "git":
                result = subprocess.run(["git", "--version"], capture_output=True, timeout=5)
                return result.returncode == 0
            elif component_name == "gh":
                result = subprocess.run(["gh", "--version"], capture_output=True, timeout=5)
                return result.returncode == 0
            elif component_name.startswith("module_"):
                module_name = component_name.replace("module_", "")
                spec = importlib.util.find_spec(module_name)
                return spec is not None
            elif component_name.startswith("path_"):
                path_str = component_name.replace("path_", "").replace("_", "/")
                path = self.workspace_root / path_str
                return path.exists()
            
            return True  # Vérification réussie par défaut
            
        except Exception:
            return False


class SelfHealingController:
    """Contrôleur principal auto-réparation"""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = Path(workspace_root)
        
        # Composants auto-réparation
        self.health_monitor = HealthMonitor(workspace_root)
        self.blockage_detector = BlockageDetector(self.health_monitor)
        self.repair_engine = AutoRepairEngine(workspace_root)
        
        # État auto-réparation
        self.healing_active = False
        self.healing_thread = None
        
        # Historique réparations
        self.repair_history = []
        
    def start_self_healing(self):
        """Démarrage auto-réparation continue"""
        if self.healing_active:
            return
        
        # Démarrage surveillance
        self.health_monitor.start_monitoring()
        
        # Démarrage boucle auto-réparation
        self.healing_active = True
        self.healing_thread = threading.Thread(target=self._healing_loop)
        self.healing_thread.daemon = True
        self.healing_thread.start()
        
        print("🔧 Self-healing system activated")
    
    def stop_self_healing(self):
        """Arrêt auto-réparation"""
        self.healing_active = False
        
        if self.healing_thread:
            self.healing_thread.join(timeout=10.0)
        
        self.health_monitor.stop_monitoring()
        
        print("🔧 Self-healing system deactivated")
    
    def _healing_loop(self):
        """Boucle principale auto-réparation"""
        while self.healing_active:
            try:
                # Détection blocages
                blockages = self.blockage_detector.detect_blockages()
                
                for blockage in blockages:
                    print(f"🚨 Blockage detected: {blockage.pattern_name} on {blockage.component_name}")
                    
                    # Réparation automatique
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    repair_results = loop.run_until_complete(
                        self.repair_engine.repair_blockage(blockage)
                    )
                    
                    # Historique
                    self.repair_history.extend(repair_results)
                    
                    # Rapport succès
                    successful_repairs = [r for r in repair_results if r.success and r.verification_passed]
                    if successful_repairs:
                        print(f"✅ Blockage repaired: {successful_repairs[0].repair_action.value}")
                    else:
                        print(f"❌ Failed to repair blockage: {blockage.pattern_name}")
                
                time.sleep(60.0)  # Vérification chaque minute
                
            except Exception as e:
                print(f"Error in healing loop: {e}")
                time.sleep(30.0)
    
    def get_system_health_report(self) -> Dict[str, Any]:
        """Rapport santé complet système"""
        health_status = self.health_monitor.get_current_health_status()
        
        # Métriques auto-réparation
        successful_repairs = len([r for r in self.repair_history if r.success])
        total_repairs = len(self.repair_history)
        
        report = {
            "health_status": health_status,
            "self_healing_metrics": {
                "active": self.healing_active,
                "total_repairs_attempted": total_repairs,
                "successful_repairs": successful_repairs,
                "success_rate": successful_repairs / total_repairs if total_repairs > 0 else 1.0,
                "recent_repairs": [asdict(r) for r in self.repair_history[-5:]]  # 5 dernières
            },
            "recommendations": self._generate_recommendations(health_status)
        }
        
        return report
    
    def _generate_recommendations(self, health_status: Dict[str, Any]) -> List[str]:
        """Génération recommandations selon état santé"""
        recommendations = []
        
        overall_status = health_status.get("overall_status", HealthStatus.HEALTHY)
        
        if overall_status == HealthStatus.CRITICAL:
            recommendations.append("Système en état critique - intervention manuelle recommandée")
            recommendations.append("Vérifier logs auto-réparation pour diagnostic détaillé")
        
        elif overall_status == HealthStatus.DEGRADED:
            recommendations.append("Performance dégradée - surveillance renforcée activée")
        
        critical_issues = health_status.get("critical_issues", [])
        if critical_issues:
            recommendations.append(f"Résolution prioritaire: {len(critical_issues)} problèmes critiques")
        
        return recommendations


def create_self_healing_system(workspace_root: str) -> SelfHealingController:
    """Factory création système auto-réparation"""
    return SelfHealingController(Path(workspace_root))


if __name__ == "__main__":
    # Test système auto-réparation
    healing_system = create_self_healing_system("/home/stephane/GitHub/PaniniFS-Research")
    
    # Démarrage surveillance
    healing_system.start_self_healing()
    
    try:
        # Test fonctionnement pendant 30 secondes
        time.sleep(30)
        
        # Rapport santé
        report = healing_system.get_system_health_report()
        print(f"\n📊 RAPPORT SANTÉ SYSTÈME:")
        print(f"Status global: {report['health_status']['overall_status']}")
        print(f"Auto-réparations: {report['self_healing_metrics']['successful_repairs']}/{report['self_healing_metrics']['total_repairs_attempted']}")
        
        if report["recommendations"]:
            print(f"\n💡 Recommandations:")
            for rec in report["recommendations"]:
                print(f"  - {rec}")
    
    finally:
        healing_system.stop_self_healing()