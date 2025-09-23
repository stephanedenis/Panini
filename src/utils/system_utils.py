"""
Utilitaires système de haut niveau pour contrôle et lancement
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

# Import absolu depuis le même package
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from core.system_base import ProcessManager, SystemMonitor, setup_logging


class SystemController:
    """Contrôleur principal du système"""
    
    def __init__(self):
        self.logger = setup_logging()
        self.process_manager = ProcessManager()
        self.system_monitor = SystemMonitor()
        self.autonomous_keywords = [
            'systeme_evenementiel_cpu.py',
            'dashboard_evenementiel.py',
            'coordinateur_global_autonome.py',
            'systeme_autonome_recherche_dhatu.py'
        ]
    
    def stop_all_autonomous_processes(self) -> Dict:
        """Arrête tous les processus autonomes"""
        self.logger.info("🛑 Arrêt de tous les processus autonomes")
        
        processes = self.process_manager.find_processes_by_keywords(
            self.autonomous_keywords
        )
        
        if not processes:
            return {'stopped': 0, 'forced': 0, 'message': 'Aucun processus trouvé'}
        
        stopped, forced = self.process_manager.stop_processes(processes)
        
        return {
            'stopped': stopped,
            'forced': forced,
            'message': f'{stopped} arrêtés, {forced} forcés'
        }
    
    def get_system_status(self) -> Dict:
        """Retourne le statut complet du système"""
        
        # Processus autonomes
        processes = self.process_manager.find_processes_by_keywords(
            self.autonomous_keywords
        )
        
        # Métriques système
        cpu_metrics = self.system_monitor.get_cpu_metrics()
        memory_metrics = self.system_monitor.get_memory_metrics()
        ports_status = self.system_monitor.get_network_ports([8890, 8891, 8892])
        
        # Calcul du statut
        total_cpu = sum(p['cpu_percent'] for p in processes)
        
        if len(processes) > 0 and total_cpu > 1:
            system_status = 'ACTIF'
        elif len(processes) > 0:
            system_status = 'IDLE'
        else:
            system_status = 'INACTIF'
        
        return {
            'timestamp': time.time(),
            'status': system_status,
            'processes': {
                'count': len(processes),
                'total_cpu': total_cpu,
                'details': [
                    {
                        'name': p['name'],
                        'pid': p['pid'],
                        'cpu_percent': p['cpu_percent'],
                        'memory_mb': p['memory_mb'],
                        'affinity': p['affinity']
                    }
                    for p in processes
                ]
            },
            'system': {
                'cpu': cpu_metrics,
                'memory': memory_metrics,
                'ports': ports_status
            }
        }
    
    def save_status_report(self, filepath: str = None) -> str:
        """Sauvegarde un rapport de statut"""
        
        if filepath is None:
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            filepath = f'system_status_{timestamp}.json'
        
        status = self.get_system_status()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(status, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Rapport sauvegardé: {filepath}")
        return filepath


class SystemLauncher:
    """Lanceur de systèmes"""
    
    def __init__(self):
        self.logger = setup_logging()
    
    def launch_event_system(self) -> bool:
        """Lance le système événementiel"""
        import subprocess
        
        script_path = Path('scripts/run_event_system.py')
        if not script_path.exists():
            self.logger.error(f"Script non trouvé: {script_path}")
            return False
        
        try:
            process = subprocess.Popen(['python3', str(script_path)])
            self.logger.info(f"Système événementiel lancé (PID {process.pid})")
            return True
        except Exception as e:
            self.logger.error(f"Erreur lancement: {e}")
            return False
    
    def launch_dashboard(self, port: int = 8892) -> bool:
        """Lance le dashboard"""
        import subprocess
        
        script_path = Path('src/scripts/run_dashboard.py')
        if not script_path.exists():
            self.logger.error(f"Script non trouvé: {script_path}")
            return False
        
        try:
            process = subprocess.Popen(['python3', str(script_path), str(port)])
            self.logger.info(f"Dashboard lancé (PID {process.pid}) sur port {port}")
            return True
        except Exception as e:
            self.logger.error(f"Erreur lancement dashboard: {e}")
            return False


class WorkspaceOrganizer:
    """Organisateur du workspace"""
    
    def __init__(self):
        self.logger = setup_logging()
        self.root = Path('.')
    
    def clean_root(self) -> Dict:
        """Nettoie la racine du projet"""
        
        moved_files = []
        kept_files = []
        
        # Fichiers à garder à la racine
        keep_in_root = {
            'README.md',
            '.gitignore',
            'requirements.txt',
            'setup.py',
            'pyproject.toml'
        }
        
        for item in self.root.iterdir():
            if item.is_file() and item.name not in keep_in_root:
                if item.suffix in ['.py', '.md', '.sh', '.log', '.json']:
                    # Détermine la destination
                    if item.suffix == '.py':
                        dest_dir = self.root / 'legacy'
                    elif item.suffix == '.md':
                        dest_dir = self.root / 'docs'
                    else:
                        dest_dir = self.root / 'legacy'
                    
                    dest_dir.mkdir(exist_ok=True)
                    dest_path = dest_dir / item.name
                    
                    if not dest_path.exists():
                        item.rename(dest_path)
                        moved_files.append(str(dest_path))
                        self.logger.info(f"Déplacé: {item.name} → {dest_dir.name}/")
                else:
                    kept_files.append(item.name)
        
        return {
            'moved': len(moved_files),
            'kept': len(kept_files),
            'moved_files': moved_files,
            'kept_files': kept_files
        }
    
    def create_main_readme(self) -> str:
        """Crée le README principal"""
        
        content = """# PaniniFS-Research

## 🎯 Système Événementiel avec Affinité CPU

Architecture événementielle remplaçant les cycles temporels fixes par un traitement réactif avec allocation CPU dédiée.

## 🚀 Démarrage Rapide

```bash
# Lancer le système complet
python3 scripts/main.py

# Vérifier le statut
python3 scripts/status.py

# Ouvrir l'interface web
python3 scripts/dashboard.py
```

## 📁 Structure

- `src/` - Code source organisé en modules
  - `core/` - Modules de base (système, événements)
  - `web/` - Interfaces web et API
  - `utils/` - Utilitaires et outils
- `scripts/` - Scripts d'exécution principaux
- `docs/` - Documentation
- `legacy/` - Anciens fichiers conservés

## ⚡ Caractéristiques

- **Architecture événementielle** : Traitement immédiat
- **Affinité CPU** : Cores dédiés par processeur
- **Monitoring temps réel** : Dashboard web auto-refresh
- **Code modulaire** : Réutilisable et maintenable

## 🌐 Interfaces

- Dashboard principal: http://localhost:8892
- API métriques: /api/metrics
- Statut système: /api/system

---
*Architecture optimisée pour la recherche autonome sur les systèmes Dhatu*
"""
        
        readme_path = self.root / 'README.md'
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.logger.info("README.md principal créé")
        return str(readme_path)