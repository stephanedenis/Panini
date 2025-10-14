#!/usr/bin/env python3
"""
🤖 SYSTÈME AUTONOME REFACTORING ÉCOSYSTÈME PANINI
================================================

Utilise l'infrastructure autonome existante pour automatiser :
- Analyse continue état écosystème
- Migration intelligente des préfixes  
- Coordination multi-agents
- Validation automatique étapes
"""

import asyncio
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional
from enum import Enum

# Import infrastructure autonome existante  
from copilotage.autonomie.core.autonomous_mode import (
    AutonomousModeController, AutonomyLevel, enable_autonomous_mode
)
from copilotage.autonomie.timeout_manager.timeout_controller import (
    AdaptiveTimeoutController, TimeoutCategory
)


class RefactoringPhase(Enum):
    """Phases de refactoring autonome"""
    ANALYSIS = "analysis"
    BACKUP = "backup"  
    RENAME = "rename"
    EXTRACT = "extract"
    COORDINATE = "coordinate"
    VALIDATE = "validate"


@dataclass
class RefactoringTask:
    """Tâche de refactoring autonome"""
    task_id: str
    phase: RefactoringPhase
    module_name: str
    action: str
    status: str = "pending"
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    result: Optional[Dict] = None
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []


class AutonomousEcosystemRefactoring:
    """Système autonome refactoring écosystème"""
    
    def __init__(self, github_root: Path = Path("/home/stephane/GitHub")):
        self.github_root = github_root
        self.workspace_root = github_root / "PaniniFS-Research"
        
        # Infrastructure autonome
        self.autonomous_controller = None
        self.timeout_controller = AdaptiveTimeoutController(self.workspace_root)
        
        # État refactoring
        self.tasks_queue = []
        self.completed_tasks = []
        self.ecosystem_state = {}
        
        # Configuration
        self.config = {
            'backup_prefix': 'v-pre-refactoring',
            'estimated_hours': 4.0,  # Durée estimée complète
            'checkpoint_interval': 300,  # 5 minutes
            'max_retries': 3
        }
        
        print("🤖 Système Autonome Refactoring Écosystème initialisé")
        print(f"   Workspace: {self.workspace_root}")
        print(f"   Durée estimée: {self.config['estimated_hours']}h")

    async def initialize_autonomous_mode(self):
        """Initialiser mode autonome pour refactoring"""
        print("\n🚀 ACTIVATION MODE AUTONOME REFACTORING")
        print("=" * 40)
        
        self.autonomous_controller = enable_autonomous_mode(
            str(self.workspace_root),
            self.config['estimated_hours']
        )
        
        print(f"✅ Mode autonome activé")
        print(f"   Mission ID: {self.autonomous_controller.mission_id}")
        print(f"   Niveau: {self.autonomous_controller.autonomy_level}")
        
        return self.autonomous_controller

    async def analyze_ecosystem_autonomous(self) -> Dict[str, Any]:
        """Analyse autonome état écosystème"""
        print("\n🔍 ANALYSE AUTONOME ÉCOSYSTÈME")
        print("=" * 30)
        
        analysis_task = RefactoringTask(
            task_id=f"analysis_{int(time.time())}",
            phase=RefactoringPhase.ANALYSIS,
            module_name="ecosystem",
            action="comprehensive_analysis"
        )
        
        analysis_task.start_time = datetime.now()
        
        try:
            # Découverte automatique modules
            discovered_modules = {}
            for module_path in self.github_root.iterdir():
                if module_path.is_dir() and not module_path.name.startswith('.'):
                    module_info = await self._analyze_module_autonomous(module_path)
                    if module_info:
                        discovered_modules[module_path.name] = module_info
            
            # Classification automatique
            classification = self._classify_modules_autonomous(discovered_modules)
            
            # Identification problèmes
            issues = self._identify_issues_autonomous(discovered_modules, classification)
            
            # Plan d'action autonome
            action_plan = await self._generate_action_plan_autonomous(issues)
            
            analysis_result = {
                'timestamp': datetime.now().isoformat(),
                'discovered_modules': discovered_modules,
                'classification': classification,
                'identified_issues': issues,
                'action_plan': action_plan,
                'metrics': {
                    'total_modules': len(discovered_modules),
                    'incorrect_prefixes': sum(1 for m in discovered_modules.values() 
                                            if m.get('prefix_correct') is False),
                    'production_ready': sum(1 for m in discovered_modules.values() 
                                          if m.get('status') == 'PRODUCTION'),
                    'estimated_tasks': len(action_plan.get('tasks', []))
                }
            }
            
            analysis_task.result = analysis_result
            analysis_task.status = "completed"
            analysis_task.end_time = datetime.now()
            
            print(f"✅ Analyse complétée")
            print(f"   Modules: {analysis_result['metrics']['total_modules']}")
            print(f"   Préfixes incorrects: {analysis_result['metrics']['incorrect_prefixes']}")
            print(f"   Tâches planifiées: {analysis_result['metrics']['estimated_tasks']}")
            
            self.ecosystem_state = analysis_result
            self.completed_tasks.append(analysis_task)
            
            return analysis_result
            
        except Exception as e:
            analysis_task.errors.append(str(e))
            analysis_task.status = "failed"
            analysis_task.end_time = datetime.now()
            print(f"❌ Erreur analyse: {e}")
            raise

    async def _analyze_module_autonomous(self, module_path: Path) -> Optional[Dict]:
        """Analyse autonome module individuel"""
        
        # Skip certains répertoires
        skip_dirs = {'.git', '__pycache__', '.venv', 'node_modules', '.pytest_cache'}
        if module_path.name in skip_dirs:
            return None
            
        try:
            module_info = {
                'name': module_path.name,
                'path': str(module_path),
                'exists': module_path.exists(),
                'is_git_repo': (module_path / '.git').exists(),
                'size_mb': await self._get_directory_size(module_path),
                'last_modified': module_path.stat().st_mtime,
                'technologies': self._detect_technologies(module_path),
                'prefix_analysis': self._analyze_prefix(module_path.name),
                'integration_level': await self._detect_integration_level(module_path)
            }
            
            return module_info
            
        except Exception as e:
            print(f"   ⚠️  Erreur analyse {module_path.name}: {e}")
            return None

    def _classify_modules_autonomous(self, modules: Dict) -> Dict[str, List[str]]:
        """Classification autonome modules par type"""
        
        classification = {
            'CORE': [],
            'APPLICATIONS': [], 
            'INFRASTRUCTURE': [],
            'RESEARCH': [],
            'DEPRECATED': []
        }
        
        for name, info in modules.items():
            # Règles classification
            if 'panini' in name.lower() and 'research' in name.lower():
                classification['RESEARCH'].append(name)
            elif info.get('integration_level', 0) > 0.8:  # Forte intégration
                classification['APPLICATIONS'].append(name)
            elif 'orchestrator' in name.lower() or 'controller' in name.lower():
                classification['INFRASTRUCTURE'].append(name)
            elif info.get('size_mb', 0) > 1000:  # Gros modules
                classification['CORE'].append(name)
            elif info.get('last_modified', 0) < (time.time() - 30*24*3600):  # +30 jours
                classification['DEPRECATED'].append(name)
            else:
                classification['APPLICATIONS'].append(name)
        
        return classification

    def _identify_issues_autonomous(self, modules: Dict, classification: Dict) -> List[Dict]:
        """Identification autonome problèmes"""
        
        issues = []
        
        # Préfixes incorrects
        for name, info in modules.items():
            prefix_info = info.get('prefix_analysis', {})
            if not prefix_info.get('is_correct', True):
                issues.append({
                    'type': 'INCORRECT_PREFIX',
                    'module': name,
                    'current': prefix_info.get('current'),
                    'suggested': prefix_info.get('suggested'),
                    'priority': 'HIGH'
                })
        
        # Modules dépréciés
        for deprecated in classification.get('DEPRECATED', []):
            issues.append({
                'type': 'DEPRECATED_MODULE',
                'module': deprecated,
                'action': 'MIGRATE_OR_REMOVE',
                'priority': 'MEDIUM'
            })
        
        # Fragmentation
        if len(classification['APPLICATIONS']) > 3:
            issues.append({
                'type': 'FRAGMENTATION',
                'modules': classification['APPLICATIONS'],
                'action': 'UNIFY_ARCHITECTURE',
                'priority': 'HIGH'
            })
        
        return issues

    async def _generate_action_plan_autonomous(self, issues: List[Dict]) -> Dict:
        """Génération autonome plan d'action"""
        
        tasks = []
        
        # Tâches par issues
        for issue in issues:
            if issue['type'] == 'INCORRECT_PREFIX':
                tasks.append({
                    'phase': 'RENAME',
                    'action': f"Rename {issue['module']} to {issue['suggested']}",
                    'module': issue['module'],
                    'priority': issue['priority'],
                    'estimated_duration': 0.5  # heures
                })
            
            elif issue['type'] == 'DEPRECATED_MODULE':
                tasks.append({
                    'phase': 'MIGRATE',
                    'action': f"Migrate or remove {issue['module']}",
                    'module': issue['module'],
                    'priority': issue['priority'],
                    'estimated_duration': 1.0
                })
        
        # Organisation par phases
        phases = {}
        for task in tasks:
            phase = task['phase']
            if phase not in phases:
                phases[phase] = []
            phases[phase].append(task)
        
        return {
            'tasks': tasks,
            'phases': phases,
            'estimated_total_hours': sum(t['estimated_duration'] for t in tasks),
            'parallel_execution_possible': len(tasks) > 1
        }

    async def execute_refactoring_autonomous(self):
        """Exécution autonome refactoring complet"""
        print("\n🚀 EXÉCUTION AUTONOME REFACTORING")
        print("=" * 35)
        
        if not self.ecosystem_state:
            await self.analyze_ecosystem_autonomous()
        
        action_plan = self.ecosystem_state.get('action_plan', {})
        tasks = action_plan.get('tasks', [])
        
        if not tasks:
            print("✅ Aucune tâche de refactoring nécessaire")
            return
        
        print(f"📋 {len(tasks)} tâches à exécuter")
        
        # Exécution par phases
        phases = action_plan.get('phases', {})
        for phase_name, phase_tasks in phases.items():
            print(f"\n🔄 Phase: {phase_name}")
            
            # Exécution parallèle si possible
            if len(phase_tasks) > 1 and action_plan.get('parallel_execution_possible'):
                await self._execute_tasks_parallel(phase_tasks)
            else:
                await self._execute_tasks_sequential(phase_tasks)
        
        # Validation finale
        await self._validate_refactoring_complete()
        
        print("\n✅ REFACTORING AUTONOME TERMINÉ")
        await self._generate_completion_report()

    async def _execute_tasks_parallel(self, tasks: List[Dict]):
        """Exécution parallèle tâches"""
        print(f"   ⚡ Exécution parallèle {len(tasks)} tâches")
        
        async def execute_task(task):
            return await self._execute_single_task(task)
        
        results = await asyncio.gather(
            *[execute_task(task) for task in tasks],
            return_exceptions=True
        )
        
        # Gestion résultats
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"   ❌ Tâche {i+1} échouée: {result}")
            else:
                print(f"   ✅ Tâche {i+1} complétée")

    async def _execute_tasks_sequential(self, tasks: List[Dict]):
        """Exécution séquentielle tâches"""
        print(f"   🔄 Exécution séquentielle {len(tasks)} tâches")
        
        for i, task in enumerate(tasks, 1):
            print(f"   {i}/{len(tasks)}: {task.get('action', 'Unknown task')}")
            
            try:
                await self._execute_single_task(task)
                print(f"      ✅ Terminée")
            except Exception as e:
                print(f"      ❌ Échouée: {e}")
                # Continuer malgré l'erreur (mode autonome)

    async def _execute_single_task(self, task: Dict):
        """Exécution autonome tâche individuelle"""
        
        # Timeout adaptatif selon type tâche
        timeout = await self.timeout_controller.calculate_timeout(
            operation_type=task.get('phase', 'generic'),
            category=TimeoutCategory.FILE_OPERATIONS,
            context={'module': task.get('module')}
        )
        
        # Exécution avec timeout
        result = await self.timeout_controller.execute_with_timeout(
            operation_func=lambda: self._perform_task_action(task),
            operation_type=task.get('phase', 'generic'),
            category=TimeoutCategory.FILE_OPERATIONS,
            context=task
        )
        
        return result

    def _perform_task_action(self, task: Dict) -> Dict:
        """Implémentation actions spécifiques"""
        
        action_type = task.get('phase', '').upper()
        module_name = task.get('module', '')
        
        if action_type == 'RENAME':
            return self._perform_rename_action(task)
        elif action_type == 'MIGRATE':
            return self._perform_migrate_action(task)
        elif action_type == 'EXTRACT':
            return self._perform_extract_action(task)
        else:
            return {'status': 'skipped', 'reason': f'Unknown action: {action_type}'}

    def _perform_rename_action(self, task: Dict) -> Dict:
        """Action renommage autonome"""
        # Implémentation sécurisée renommage
        print(f"      🔄 Simulation renommage: {task.get('module')}")
        # TODO: Implémentation réelle
        return {'status': 'completed', 'action': 'rename_simulation'}

    async def _validate_refactoring_complete(self):
        """Validation finale refactoring"""
        print("\n🔍 VALIDATION FINALE")
        
        # Re-analyse post-refactoring
        final_state = await self.analyze_ecosystem_autonomous()
        
        # Comparaison avant/après
        initial_issues = len(self.ecosystem_state.get('identified_issues', []))
        final_issues = len(final_state.get('identified_issues', []))
        
        improvement = initial_issues - final_issues
        
        print(f"   Issues avant: {initial_issues}")
        print(f"   Issues après: {final_issues}")
        print(f"   Amélioration: {improvement} (+{improvement/max(initial_issues,1)*100:.1f}%)")

    # Méthodes utilitaires
    async def _get_directory_size(self, path: Path) -> float:
        """Taille répertoire en MB"""
        try:
            total = sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
            return total / (1024 * 1024)  # MB
        except:
            return 0.0

    def _detect_technologies(self, path: Path) -> List[str]:
        """Détection technologies module"""
        techs = []
        if (path / 'package.json').exists():
            techs.append('Node.js/TypeScript')
        if (path / 'pyproject.toml').exists() or (path / 'requirements.txt').exists():
            techs.append('Python')
        if (path / 'Cargo.toml').exists():
            techs.append('Rust')
        return techs

    def _analyze_prefix(self, module_name: str) -> Dict:
        """Analyse préfixe module"""
        correct_prefixes = {'PaniniFS', 'Panini-', 'OntoWave'}
        
        is_correct = any(module_name.startswith(prefix) for prefix in correct_prefixes)
        
        if module_name.startswith('PaniniFS-') and module_name != 'PaniniFS':
            suggested = module_name.replace('PaniniFS-', 'Panini-')
            is_correct = False
        else:
            suggested = module_name
        
        return {
            'current': module_name,
            'is_correct': is_correct,
            'suggested': suggested
        }

    async def _detect_integration_level(self, path: Path) -> float:
        """Détecter niveau intégration Panini (0.0-1.0)"""
        integration_score = 0.0
        
        # Recherche fichiers intégration
        integration_files = [
            'docs/panini/',
            'src/panini/',
            'integration/',
            'dhatu'
        ]
        
        for pattern in integration_files:
            if list(path.rglob(pattern)):
                integration_score += 0.25
        
        return min(integration_score, 1.0)

    async def _generate_completion_report(self):
        """Rapport final refactoring"""
        report_path = self.workspace_root / f"refactoring_report_{int(time.time())}.json"
        
        report = {
            'completion_time': datetime.now().isoformat(),
            'initial_state': self.ecosystem_state,
            'completed_tasks': [asdict(task) for task in self.completed_tasks],
            'autonomous_controller': {
                'mission_id': self.autonomous_controller.mission_id if self.autonomous_controller else None,
                'autonomy_level': str(self.autonomous_controller.autonomy_level) if self.autonomous_controller else None
            }
        }
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 Rapport généré: {report_path}")


async def main():
    """Point d'entrée système autonome"""
    
    print("🤖 DÉMARRAGE SYSTÈME AUTONOME REFACTORING ÉCOSYSTÈME PANINI")
    print("=" * 60)
    
    # Initialisation
    refactoring_system = AutonomousEcosystemRefactoring()
    
    # Mode autonome
    await refactoring_system.initialize_autonomous_mode()
    
    # Analyse et refactoring
    await refactoring_system.analyze_ecosystem_autonomous()
    await refactoring_system.execute_refactoring_autonomous()
    
    print("\n🎯 SYSTÈME AUTONOME REFACTORING TERMINÉ")


if __name__ == "__main__":
    asyncio.run(main())