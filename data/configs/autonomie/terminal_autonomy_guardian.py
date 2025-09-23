#!/usr/bin/env python3
"""
Module TERMINAL_AUTONOMY_GUARDIAN - Gardien autonomie terminaux

Objectif: Prévention proactive et résolution automatique de tous les blocages
terminal qui peuvent compromettre l'autonomie des agents (pagers, éditeurs).

Architecture intégrée:
- InteractiveCommandBlocklist: Liste noire commandes interactives
- CommandSanitizer: Transformation automatique commandes dangereuses
- TerminalGuardian: Surveillance continue et intervention automatique
- AutonomyValidator: Validation mode autonomie avant exécution

Priorité: CRITIQUE - Élimination définitive bris autonomie terminal
"""

import asyncio
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass
import subprocess
import psutil


@dataclass
class CommandTransformation:
    """Transformation commande pour autonomie"""
    original_command: str
    safe_command: str
    transformation_type: str
    reason: str
    timestamp: datetime


class InteractiveCommandBlocklist:
    """Liste noire complète commandes interactives"""
    
    def __init__(self):
        # Commandes absolument interdites en mode autonomie
        self.forbidden_commands = {
            'vi', 'vim', 'nvim', 'nano', 'emacs', 'ed', 'joe', 'micro',
            'less', 'more', 'most', 'pg',
            'top', 'htop', 'iotop', 'watch',
            'tail -f',  # Version interactive
        }
        
        # Patterns commandes à risque
        self.risky_patterns = [
            r'git\s+(log|show|diff|blame)(?!\s+--no-pager)',
            r'gh\s+api.*--method\s+POST(?!.*\|\s*cat)',
            r'man\s+\w+(?!\s+--help)',
            r'python.*input\(',
            r'read\s+-p'  # Bash read avec prompt
        ]
        
        # Commandes avec flags sécurisants
        self.safe_flags = {
            'git': ['--no-pager', '--porcelain'],
            'gh': ['--json', '| cat', '| head'],
            'ls': ['-1'],  # Pas d'interaction
            'find': ['-print'],
            'grep': ['-l', '-c']  # Output limité
        }
    
    def is_command_forbidden(self, command: str) -> bool:
        """Vérifie si commande est interdite"""
        cmd_parts = command.strip().lower().split()
        if not cmd_parts:
            return False
        
        base_command = cmd_parts[0]
        
        # Check liste noire directe
        if base_command in self.forbidden_commands:
            return True
        
        # Check patterns risqués avec regex
        import re
        for pattern in self.risky_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return True
        
        return False
    
    def get_safe_alternative(self, command: str) -> Optional[str]:
        """Retourne alternative sécurisée pour commande"""
        cmd_lower = command.strip().lower()
        
        # Transformations spécifiques
        if cmd_lower.startswith('vi ') or cmd_lower.startswith('vim '):
            filename = command.split()[-1]
            return f"echo 'Édition de {filename} interdite en mode autonomie'"
        
        if cmd_lower.startswith('less ') or cmd_lower.startswith('more '):
            filename = command.split()[-1]
            return f"cat {filename} | head -50"
        
        if 'git log' in cmd_lower and '--no-pager' not in cmd_lower:
            return command.replace('git log', 'git --no-pager log') + ' --oneline -10'
        
        if 'git show' in cmd_lower and '--no-pager' not in cmd_lower:
            return command.replace('git show', 'git --no-pager show')
        
        if 'git diff' in cmd_lower and '--no-pager' not in cmd_lower:
            return command.replace('git diff', 'git --no-pager diff')
        
        if 'gh api' in cmd_lower and '--method POST' in cmd_lower and '| cat' not in cmd_lower:
            return f"{command} | cat"
        
        if cmd_lower.startswith('man '):
            topic = command.split()[-1]
            return f"{topic} --help 2>/dev/null || echo 'Aide non disponible pour {topic}'"
        
        return None


class CommandSanitizer:
    """Sanitiseur automatique commandes"""
    
    def __init__(self):
        self.blocklist = InteractiveCommandBlocklist()
        self.transformation_log: List[CommandTransformation] = []
    
    def sanitize_command(self, command: str, 
                        context: Dict[str, Any] = None) -> CommandTransformation:
        """Sanitise commande pour autonomie"""
        
        original = command.strip()
        
        # Vérifier si commande interdite
        if self.blocklist.is_command_forbidden(original):
            
            # Chercher alternative sécurisée
            safe_alternative = self.blocklist.get_safe_alternative(original)
            
            if safe_alternative:
                transformation = CommandTransformation(
                    original_command=original,
                    safe_command=safe_alternative,
                    transformation_type="auto_safe_alternative",
                    reason="Commande interactive transformée pour autonomie",
                    timestamp=datetime.now()
                )
            else:
                # Fallback: bloquer complètement
                transformation = CommandTransformation(
                    original_command=original,
                    safe_command=f"echo 'Commande bloquée pour autonomie: {original}'",
                    transformation_type="blocked",
                    reason="Commande interactive sans alternative sécurisée",
                    timestamp=datetime.now()
                )
        else:
            # Commande OK
            transformation = CommandTransformation(
                original_command=original,
                safe_command=original,
                transformation_type="pass_through",
                reason="Commande sécurisée pour autonomie",
                timestamp=datetime.now()
            )
        
        # Logging transformation
        self.transformation_log.append(transformation)
        
        # Garde seulement les 1000 dernières transformations
        if len(self.transformation_log) > 1000:
            self.transformation_log = self.transformation_log[-1000:]
        
        return transformation
    
    def get_transformation_stats(self) -> Dict[str, Any]:
        """Statistiques transformations"""
        if not self.transformation_log:
            return {"total": 0}
        
        total = len(self.transformation_log)
        by_type = {}
        recent_blocked = 0
        
        # Analyse par type
        for t in self.transformation_log:
            t_type = t.transformation_type
            by_type[t_type] = by_type.get(t_type, 0) + 1
        
        # Blocages récents (dernière heure)
        cutoff = datetime.now().timestamp() - 3600
        recent_blocked = sum(1 for t in self.transformation_log 
                           if t.timestamp.timestamp() > cutoff 
                           and t.transformation_type != "pass_through")
        
        return {
            "total": total,
            "by_type": by_type,
            "recent_blocked_last_hour": recent_blocked,
            "blocking_rate": (by_type.get("blocked", 0) + 
                            by_type.get("auto_safe_alternative", 0)) / total,
            "last_transformation": self.transformation_log[-1].timestamp.isoformat()
        }


class TerminalGuardian:
    """Gardien surveillance terminaux"""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = Path(workspace_root)
        self.logger = logging.getLogger("terminal_guardian")
        self.sanitizer = CommandSanitizer()
        
        # Surveillance active
        self.monitoring_active = False
        self.intervention_count = 0
    
    def start_monitoring(self):
        """Démarre surveillance continue"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.logger.info("🛡️  Terminal Guardian activé - surveillance autonomie")
        
        # Lancement monitoring en arrière-plan
        import threading
        threading.Thread(target=self._monitor_loop, daemon=True).start()
    
    def stop_monitoring(self):
        """Arrête surveillance"""
        self.monitoring_active = False
        self.logger.info("Terminal Guardian désactivé")
    
    def _monitor_loop(self):
        """Boucle surveillance principale"""
        while self.monitoring_active:
            try:
                # Vérifier processus suspects
                suspects = self._detect_blocking_processes()
                
                # Intervention si nécessaire
                if suspects:
                    self._auto_intervene(suspects)
                
                time.sleep(5)  # Check toutes les 5 secondes
                
            except Exception as e:
                self.logger.error(f"Erreur surveillance: {e}")
                time.sleep(10)
    
    def _detect_blocking_processes(self) -> List[Dict[str, Any]]:
        """Détection processus bloquants"""
        suspects = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
                try:
                    name = proc.info['name']
                    cmdline = proc.info['cmdline']
                    duration = time.time() - proc.info['create_time']
                    
                    # Processus interactifs suspects
                    if name in ['less', 'more', 'vi', 'vim', 'nano'] and duration > 30:
                        suspects.append({
                            'pid': proc.info['pid'],
                            'name': name,
                            'cmdline': ' '.join(cmdline) if cmdline else '',
                            'duration': duration,
                            'threat_level': 'high'
                        })
                    
                    # Git/GitHub avec durée suspecte
                    if cmdline and duration > 60:
                        cmd_str = ' '.join(cmdline).lower()
                        if any(pattern in cmd_str for pattern in ['git log', 'git show', 'gh api']):
                            suspects.append({
                                'pid': proc.info['pid'],
                                'name': name,
                                'cmdline': cmd_str,
                                'duration': duration,
                                'threat_level': 'medium'
                            })
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            self.logger.error(f"Erreur détection: {e}")
        
        return suspects
    
    def _auto_intervene(self, suspects: List[Dict[str, Any]]):
        """Intervention automatique"""
        for suspect in suspects:
            try:
                pid = suspect['pid']
                threat_level = suspect['threat_level']
                
                if threat_level == 'high':
                    # Intervention immédiate
                    proc = psutil.Process(pid)
                    proc.terminate()
                    
                    self.intervention_count += 1
                    self.logger.warning(f"🚨 Intervention: terminé processus {suspect['name']} (PID: {pid})")
                
                elif threat_level == 'medium':
                    # Attendre un peu plus avant intervention
                    if suspect['duration'] > 120:  # 2 minutes
                        proc = psutil.Process(pid)
                        proc.terminate()
                        
                        self.intervention_count += 1
                        self.logger.warning(f"⚠️  Intervention: terminé processus suspect {suspect['name']} (PID: {pid})")
                
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                self.logger.info(f"Processus {pid} déjà terminé: {e}")
    
    def process_command_safely(self, command: str, 
                              context: Dict[str, Any] = None) -> str:
        """Traitement sécurisé commande"""
        
        # Sanitisation
        transformation = self.sanitizer.sanitize_command(command, context)
        
        # Logging si transformation
        if transformation.transformation_type != "pass_through":
            self.logger.info(f"🔧 Commande transformée: {transformation.original_command} → {transformation.safe_command}")
        
        return transformation.safe_command
    
    def get_guardian_status(self) -> Dict[str, Any]:
        """État du gardien"""
        return {
            "monitoring_active": self.monitoring_active,
            "intervention_count": self.intervention_count,
            "sanitizer_stats": self.sanitizer.get_transformation_stats(),
            "uptime": "active" if self.monitoring_active else "inactive"
        }


class AutonomyValidator:
    """Validateur mode autonomie"""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = Path(workspace_root)
        self.guardian = TerminalGuardian(workspace_root)
    
    def ensure_full_autonomy(self, command: str, 
                           context: Dict[str, Any] = None) -> str:
        """Assure autonomie complète pour commande"""
        
        # Démarrer surveillance si pas active
        if not self.guardian.monitoring_active:
            self.guardian.start_monitoring()
        
        # Traitement sécurisé
        safe_command = self.guardian.process_command_safely(command, context)
        
        return safe_command
    
    def validate_autonomy_mode(self) -> Dict[str, Any]:
        """Validation mode autonomie"""
        
        # Vérifier pas de processus bloquants actifs
        blocking_procs = self.guardian._detect_blocking_processes()
        
        # État Guardian
        guardian_status = self.guardian.get_guardian_status()
        
        # Déterminer status global
        if blocking_procs:
            autonomy_status = "compromised"
            issues = [f"Processus bloquant détecté: {p['name']}" for p in blocking_procs]
        elif not guardian_status["monitoring_active"]:
            autonomy_status = "unprotected"
            issues = ["Surveillance Guardian inactive"]
        else:
            autonomy_status = "protected"
            issues = []
        
        return {
            "autonomy_status": autonomy_status,
            "blocking_processes": len(blocking_procs),
            "guardian_active": guardian_status["monitoring_active"],
            "total_interventions": guardian_status["intervention_count"],
            "issues": issues,
            "timestamp": datetime.now().isoformat()
        }


# Interface principale pour l'autonomie
def protect_terminal_autonomy(workspace_root: Path) -> AutonomyValidator:
    """Interface principale protection autonomie terminal"""
    
    validator = AutonomyValidator(workspace_root)
    
    # Auto-activation surveillance
    validator.guardian.start_monitoring()
    
    print("🛡️  Protection autonomie terminal activée")
    print(f"📊 Status: {validator.validate_autonomy_mode()}")
    
    return validator


# Test si exécuté directement
if __name__ == "__main__":
    
    def test_terminal_autonomy():
        print("🧪 TEST PROTECTION AUTONOMIE TERMINAL")
        print("=" * 60)
        
        # Initialisation
        validator = protect_terminal_autonomy(Path.cwd())
        
        # Test commandes problématiques
        test_commands = [
            "gh api repos/:owner/:repo/milestones --method POST --field title='Test'",
            "git log --oneline",
            "vi config.txt",
            "less README.md",
            "python normal_script.py",  # OK
            "man python"
        ]
        
        print("\n🔍 TEST COMMANDES:")
        for cmd in test_commands:
            safe_cmd = validator.ensure_full_autonomy(cmd)
            status = "🔧 TRANSFORMÉE" if cmd != safe_cmd else "✅ OK"
            print(f"{status} {cmd}")
            if cmd != safe_cmd:
                print(f"      → {safe_cmd}")
        
        # Status final
        print(f"\n📊 STATUS AUTONOMIE FINALE:")
        final_status = validator.validate_autonomy_mode()
        for key, value in final_status.items():
            print(f"   {key}: {value}")
        
        # Stats Guardian
        print(f"\n🛡️  STATS GUARDIAN:")
        guardian_stats = validator.guardian.get_guardian_status()
        for key, value in guardian_stats.items():
            print(f"   {key}: {value}")
    
    test_terminal_autonomy()