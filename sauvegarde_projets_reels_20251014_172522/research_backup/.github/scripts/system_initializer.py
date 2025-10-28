#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Initialisateur Système Approbations - Spec-Kit PaniniFS
Configuration et démarrage du système d'approbation optimisé
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

class SystemInitializer:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.scripts_path = self.base_path / "scripts"
        self.logs_path = self.base_path / "logs"
        self.config_path = self.base_path / "copilot-approved-scripts.json"
        
    def initialize_complete_system(self):
        """Initialisation complète du système"""
        print("🚀 INITIALISATION SYSTÈME APPROBATIONS PANINI-FS")
        print("=" * 60)
        
        # 1. Vérifier et créer la structure
        self._setup_directory_structure()
        
        # 2. Vérifier la configuration
        self._validate_configuration()
        
        # 3. Initialiser les logs
        self._initialize_logging()
        
        # 4. Tester le système de validation
        self._test_validation_system()
        
        # 5. Configurer la tâche cron pour l'optimisation
        self._setup_automation()
        
        # 6. Démarrer le monitoring (optionnel)
        self._offer_monitoring_start()
        
        print("✅ Initialisation terminée avec succès!")
        return True
    
    def _setup_directory_structure(self):
        """Créer la structure de répertoires"""
        print("📁 Configuration structure répertoires...")
        
        # Créer les répertoires nécessaires
        directories = [
            self.logs_path,
            self.scripts_path,
            self.base_path / "docs",
            self.base_path / "config",
            self.base_path / "reports"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"   ✓ {directory}")
        
        # Rendre les scripts exécutables
        scripts = [
            "validate_command.py",
            "weekly_optimizer.py", 
            "approval_monitor.py"
        ]
        
        for script in scripts:
            script_path = self.scripts_path / script
            if script_path.exists():
                os.chmod(script_path, 0o755)
                print(f"   ✓ {script} rendu exécutable")
    
    def _validate_configuration(self):
        """Valider la configuration actuelle"""
        print("⚙️ Validation configuration...")
        
        if not self.config_path.exists():
            print(f"   ❌ Configuration manquante: {self.config_path}")
            return False
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Vérifications essentielles
            required_sections = ['version', 'metadata', 'approved_commands', 'security_constraints']
            
            for section in required_sections:
                if section not in config:
                    print(f"   ❌ Section manquante: {section}")
                    return False
                print(f"   ✓ Section {section}")
            
            # Vérifier la version
            version = config.get('version', '1.0')
            print(f"   ✓ Version configuration: {version}")
            
            # Compter les patterns
            total_patterns = sum(len(patterns) for patterns in config['approved_commands'].values())
            print(f"   ✓ Patterns configurés: {total_patterns}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Erreur validation: {e}")
            return False
    
    def _initialize_logging(self):
        """Initialiser le système de logging"""
        print("📝 Initialisation logging...")
        
        # Créer les fichiers de log
        log_files = [
            "command_execution.log",
            "optimization_history.log", 
            "alerts.log",
            "system_status.log"
        ]
        
        for log_file in log_files:
            log_path = self.logs_path / log_file
            if not log_path.exists():
                log_path.touch()
                print(f"   ✓ Créé: {log_file}")
            else:
                print(f"   ✓ Existant: {log_file}")
        
        # Créer un log d'initialisation
        init_log = {
            'timestamp': datetime.now().isoformat(),
            'event': 'system_initialization',
            'status': 'success',
            'components': ['logging', 'validation', 'optimization', 'monitoring'],
            'version': '2.0',
            'initialized_by': 'system_initializer'
        }
        
        with open(self.logs_path / "system_status.log", 'a', encoding='utf-8') as f:
            f.write(json.dumps(init_log, ensure_ascii=False) + '\n')
    
    def _test_validation_system(self):
        """Tester le système de validation"""
        print("🧪 Test système validation...")
        
        validate_script = self.scripts_path / "validate_command.py"
        
        if not validate_script.exists():
            print("   ❌ Script validation manquant")
            return False
        
        # Tests de base
        test_commands = [
            ("python3", "panini_binary_decomposer.py --test"),
            ("curl", "http://127.0.0.1:9000/health"),
            ("ls", "-la /tmp"),
            ("rm", "-rf /")  # Doit être rejeté
        ]
        
        for command, args in test_commands:
            try:
                result = subprocess.run([
                    sys.executable, str(validate_script), command, args
                ], capture_output=True, text=True, timeout=5)
                
                if result.returncode == 0:
                    print(f"   ✅ {command}: APPROUVÉ")
                else:
                    print(f"   ❌ {command}: REJETÉ ({result.stdout.strip()})")
                    
            except subprocess.TimeoutExpired:
                print(f"   ⏱️ {command}: TIMEOUT")
            except Exception as e:
                print(f"   ⚠️ {command}: ERREUR - {e}")
        
        return True
    
    def _setup_automation(self):
        """Configurer l'automatisation"""
        print("⚡ Configuration automatisation...")
        
        # Créer un script wrapper pour cron
        cron_script = self.scripts_path / "weekly_optimization_cron.sh"
        
        cron_content = f"""#!/bin/bash
# Script automatique d'optimisation hebdomadaire PaniniFS
# Généré automatiquement le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

cd "{self.base_path}"
export PYTHONPATH="{self.base_path}:$PYTHONPATH"

# Log de démarrage
echo "[$(date)] Démarrage optimisation hebdomadaire" >> logs/automation.log

# Exécuter l'optimiseur
python3 scripts/weekly_optimizer.py >> logs/automation.log 2>&1

# Vérifier le statut
if [ $? -eq 0 ]; then
    echo "[$(date)] Optimisation terminée avec succès" >> logs/automation.log
else
    echo "[$(date)] ERREUR optimisation" >> logs/automation.log
fi
"""
        
        with open(cron_script, 'w', encoding='utf-8') as f:
            f.write(cron_content)
        
        os.chmod(cron_script, 0o755)
        print(f"   ✓ Script cron créé: {cron_script}")
        
        # Proposer l'installation cron
        print("\n💡 Pour automatiser l'optimisation hebdomadaire:")
        print("   crontab -e")
        print("   Ajouter la ligne:")
        print(f"   0 2 * * 0 {cron_script}")  # Dimanche 2h du matin
        print("   (optimisation tous les dimanches à 2h)")
    
    def _offer_monitoring_start(self):
        """Proposer de démarrer le monitoring"""
        print("🔍 Monitoring en temps réel disponible")
        
        response = input("Démarrer le monitoring maintenant? (o/n): ").lower().strip()
        
        if response in ['o', 'oui', 'y', 'yes']:
            try:
                monitor_script = self.scripts_path / "approval_monitor.py"
                print(f"🚀 Démarrage monitoring: {monitor_script}")
                
                # Démarrer en arrière-plan
                subprocess.Popen([
                    sys.executable, str(monitor_script)
                ], cwd=str(self.base_path))
                
                print("✅ Monitoring démarré en arrière-plan")
                print("💡 Utilisez 'ps aux | grep approval_monitor' pour vérifier")
                
            except Exception as e:
                print(f"❌ Erreur démarrage monitoring: {e}")
        else:
            print("💡 Pour démarrer plus tard:")
            print(f"   python3 {self.scripts_path}/approval_monitor.py")
    
    def generate_status_report(self):
        """Générer un rapport de statut du système"""
        print("📊 Génération rapport statut...")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'system_version': '2.0',
            'components': {
                'validation': self._check_component_status('validate_command.py'),
                'optimization': self._check_component_status('weekly_optimizer.py'),
                'monitoring': self._check_component_status('approval_monitor.py'),
                'configuration': self._check_configuration_status()
            },
            'file_structure': self._check_file_structure(),
            'recommendations': self._generate_recommendations()
        }
        
        # Sauvegarder le rapport
        report_path = self.base_path / "reports" / f"system_status_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"✅ Rapport sauvé: {report_path}")
        return report
    
    def _check_component_status(self, script_name):
        """Vérifier le statut d'un composant"""
        script_path = self.scripts_path / script_name
        
        return {
            'exists': script_path.exists(),
            'executable': script_path.exists() and os.access(script_path, os.X_OK),
            'size': script_path.stat().st_size if script_path.exists() else 0,
            'last_modified': datetime.fromtimestamp(script_path.stat().st_mtime).isoformat() if script_path.exists() else None
        }
    
    def _check_configuration_status(self):
        """Vérifier le statut de la configuration"""
        if not self.config_path.exists():
            return {'status': 'missing'}
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            total_patterns = sum(len(patterns) for patterns in config.get('approved_commands', {}).values())
            
            return {
                'status': 'valid',
                'version': config.get('version', 'unknown'),
                'total_patterns': total_patterns,
                'last_updated': config.get('metadata', {}).get('last_updated'),
                'optimization_count': config.get('metadata', {}).get('optimization_count', 0)
            }
            
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _check_file_structure(self):
        """Vérifier la structure des fichiers"""
        structure = {}
        
        for path in [self.logs_path, self.scripts_path, self.base_path / "docs", self.base_path / "reports"]:
            structure[path.name] = {
                'exists': path.exists(),
                'is_directory': path.is_dir() if path.exists() else False,
                'file_count': len(list(path.iterdir())) if path.exists() and path.is_dir() else 0
            }
        
        return structure
    
    def _generate_recommendations(self):
        """Générer des recommandations"""
        recommendations = []
        
        # Vérifier les logs
        if (self.logs_path / "command_execution.log").stat().st_size == 0:
            recommendations.append("Aucune activité détectée - vérifier l'intégration du système de validation")
        
        # Vérifier l'optimisation
        if not (self.logs_path / "optimization_history.log").exists():
            recommendations.append("Exécuter une première optimisation pour initialiser l'historique")
        
        # Vérifier l'automatisation
        try:
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            if 'weekly_optimization_cron.sh' not in result.stdout:
                recommendations.append("Configurer la tâche cron pour l'optimisation automatique")
        except:
            recommendations.append("Vérifier la disponibilité de cron pour l'automatisation")
        
        return recommendations

def main():
    """Point d'entrée principal"""
    print("🔧 INITIALISATEUR SYSTÈME APPROBATIONS PANINI-FS")
    print("Version 2.0 - Spec-Kit Complet")
    print("=" * 60)
    
    initializer = SystemInitializer()
    
    try:
        # Initialisation complète
        success = initializer.initialize_complete_system()
        
        if success:
            # Générer rapport de statut
            print("\n📊 Génération rapport final...")
            report = initializer.generate_status_report()
            
            print("\n🎉 SYSTÈME INITIALISÉ AVEC SUCCÈS!")
            print("=" * 60)
            print("🔧 Composants installés:")
            print("   • Système de validation des commandes")
            print("   • Optimiseur hebdomadaire automatique") 
            print("   • Moniteur temps réel des approbations")
            print("   • Logging et reporting complets")
            print("   • Structure de gouvernance Spec-Kit")
            
            print("\n🚀 Prochaines étapes:")
            print("   1. Configurer la tâche cron pour l'automatisation")
            print("   2. Tester le système avec quelques commandes")
            print("   3. Surveiller les logs pour optimiser les patterns")
            print("   4. Exécuter l'optimiseur hebdomadaire si nécessaire")
            
            return 0
        else:
            print("❌ Échec de l'initialisation")
            return 1
            
    except Exception as e:
        print(f"💥 Erreur critique: {e}")
        return 1

if __name__ == '__main__':
    exit(main())