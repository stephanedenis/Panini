#!/usr/bin/env python3
"""
Validation Complète Système Autonome - Rapport Final
Tests de fiabilité et performance de tous les composants
"""

import sys
import json
import time
import requests
from datetime import datetime
from pathlib import Path
import psutil


class AutonomousSystemValidator:
    def __init__(self):
        self.workspace = Path('/home/stephane/GitHub/PaniniFS-Research')
        self.results_dir = self.workspace / 'autonomous_results'
        self.validation_results = {}
        
        self.log("🔍 Démarrage validation système autonome")
    
    def log(self, message):
        """Logging validation"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        return log_message
    
    def validate_corpus_processor(self):
        """Valide processeur de corpus"""
        self.log("📊 Validation processeur corpus...")
        
        results = {
            'component': 'corpus_processor',
            'status': 'unknown',
            'metrics': {}
        }
        
        try:
            # Vérification fichier stats
            stats_file = self.results_dir / 'autonomous_processing_stats.json'
            if stats_file.exists():
                with open(stats_file) as f:
                    stats = json.load(f)
                
                results['metrics'] = {
                    'corpus_processed': stats.get('successful', 0),
                    'total_atoms': stats.get('total_atoms', 0),
                    'processing_rate': stats.get('atoms_per_minute', 0),
                    'success_rate': stats.get('successful', 0) / max(stats.get('total_files', 1), 1) * 100
                }
                
                if results['metrics']['corpus_processed'] > 0:
                    results['status'] = 'operational'
                    self.log(f"✅ Corpus processor: {results['metrics']['corpus_processed']} corpus traités")
                else:
                    results['status'] = 'inactive'
                    self.log("⚠️ Corpus processor: aucun corpus traité")
            else:
                results['status'] = 'not_found'
                self.log("❌ Corpus processor: fichier stats manquant")
                
        except Exception as e:
            results['status'] = 'error'
            results['error'] = str(e)
            self.log(f"❌ Erreur validation corpus: {e}")
        
        return results
    
    def validate_dashboard(self):
        """Valide dashboard autonome"""
        self.log("🖥️ Validation dashboard...")
        
        results = {
            'component': 'dashboard',
            'status': 'unknown',
            'metrics': {}
        }
        
        try:
            # Test connexion dashboard
            response = requests.get('http://localhost:8090/api/status', timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                results['status'] = 'operational'
                results['metrics'] = {
                    'response_time_ms': response.elapsed.total_seconds() * 1000,
                    'cpu_monitoring': data.get('cpu_percent', 0),
                    'memory_monitoring': data.get('memory_percent', 0),
                    'uptime': data.get('uptime', '0h')
                }
                self.log(f"✅ Dashboard opérationnel: {results['metrics']['response_time_ms']:.0f}ms")
            else:
                results['status'] = 'error'
                results['error'] = f"HTTP {response.status_code}"
                self.log(f"❌ Dashboard erreur: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            results['status'] = 'offline'
            self.log("❌ Dashboard: connexion impossible")
        except Exception as e:
            results['status'] = 'error'
            results['error'] = str(e)
            self.log(f"❌ Erreur validation dashboard: {e}")
        
        return results
    
    def validate_dhatu_optimizer(self):
        """Valide optimiseur dhātu"""
        self.log("⚡ Validation optimiseur dhātu...")
        
        results = {
            'component': 'dhatu_optimizer',
            'status': 'unknown',
            'metrics': {}
        }
        
        try:
            # Vérification résultats optimisation
            optimization_file = self.results_dir / 'dhatu_optimization_results.json'
            if optimization_file.exists():
                with open(optimization_file) as f:
                    stats = json.load(f)
                
                results['metrics'] = {
                    'atoms_processed': stats.get('total_atoms_processed', 0),
                    'throughput_atoms_per_minute': stats.get('throughput_atoms_per_minute', 0),
                    'peak_throughput': stats.get('peak_throughput', 0),
                    'target_400k_achieved': stats.get('target_achieved', False),
                    'optimization_factor': stats.get('optimization_factor', 1.0)
                }
                
                if results['metrics']['throughput_atoms_per_minute'] > 100000:
                    results['status'] = 'high_performance'
                    self.log(f"🚀 Optimiseur haute performance: {results['metrics']['throughput_atoms_per_minute']:.0f} atomes/min")
                elif results['metrics']['throughput_atoms_per_minute'] > 50000:
                    results['status'] = 'operational'
                    self.log(f"✅ Optimiseur opérationnel: {results['metrics']['throughput_atoms_per_minute']:.0f} atomes/min")
                else:
                    results['status'] = 'low_performance'
                    self.log(f"⚠️ Optimiseur performance faible: {results['metrics']['throughput_atoms_per_minute']:.0f} atomes/min")
            else:
                results['status'] = 'not_found'
                self.log("❌ Optimiseur: fichier résultats manquant")
                
        except Exception as e:
            results['status'] = 'error'
            results['error'] = str(e)
            self.log(f"❌ Erreur validation optimiseur: {e}")
        
        return results
    
    def validate_recovery_system(self):
        """Valide système auto-recovery"""
        self.log("🛡️ Validation auto-recovery...")
        
        results = {
            'component': 'recovery_system',
            'status': 'unknown',
            'metrics': {}
        }
        
        try:
            # Vérification fichiers recovery
            recovery_dir = self.workspace / 'autonomous_recovery'
            state_file = recovery_dir / 'autonomous_state.json'
            process_registry = recovery_dir / 'active_processes.json'
            
            if recovery_dir.exists() and state_file.exists():
                with open(state_file) as f:
                    state = json.load(f)
                
                # Vérification processus enregistrés
                registered_processes = 0
                if process_registry.exists():
                    with open(process_registry) as f:
                        processes = json.load(f)
                        registered_processes = len(processes)
                
                results['metrics'] = {
                    'recovery_active': state.get('recovery_system_active', False),
                    'monitoring_enabled': state.get('monitoring_enabled', False),
                    'registered_processes': registered_processes,
                    'last_update': state.get('timestamp', 'N/A')
                }
                
                if results['metrics']['recovery_active'] and registered_processes > 0:
                    results['status'] = 'operational'
                    self.log(f"✅ Auto-recovery actif: {registered_processes} processus surveillés")
                else:
                    results['status'] = 'partial'
                    self.log("⚠️ Auto-recovery: configuration partielle")
            else:
                results['status'] = 'not_configured'
                self.log("❌ Auto-recovery: non configuré")
                
        except Exception as e:
            results['status'] = 'error'
            results['error'] = str(e)
            self.log(f"❌ Erreur validation recovery: {e}")
        
        return results
    
    def validate_system_resources(self):
        """Valide utilisation ressources système"""
        self.log("🖥️ Validation ressources système...")
        
        try:
            cpu_percent = psutil.cpu_percent(interval=2)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            results = {
                'component': 'system_resources',
                'status': 'operational',
                'metrics': {
                    'cpu_usage_percent': cpu_percent,
                    'memory_usage_percent': memory.percent,
                    'disk_usage_percent': disk.percent,
                    'cpu_cores': psutil.cpu_count(),
                    'memory_total_gb': round(memory.total / (1024**3), 1)
                }
            }
            
            # Évaluation performance
            if cpu_percent > 80 or memory.percent > 80:
                results['status'] = 'high_load'
                self.log(f"⚠️ Charge système élevée: CPU {cpu_percent:.1f}% | RAM {memory.percent:.1f}%")
            else:
                self.log(f"✅ Ressources normales: CPU {cpu_percent:.1f}% | RAM {memory.percent:.1f}%")
            
            return results
            
        except Exception as e:
            return {
                'component': 'system_resources',
                'status': 'error',
                'error': str(e)
            }
    
    def generate_final_report(self):
        """Génère rapport final complet"""
        self.log("📋 Génération rapport final...")
        
        # Validation de tous les composants
        validations = {
            'corpus_processor': self.validate_corpus_processor(),
            'dashboard': self.validate_dashboard(),
            'dhatu_optimizer': self.validate_dhatu_optimizer(),
            'recovery_system': self.validate_recovery_system(),
            'system_resources': self.validate_system_resources()
        }
        
        # Calcul score global
        operational_count = sum(1 for v in validations.values() if v['status'] in ['operational', 'high_performance'])
        total_components = len(validations)
        system_health_score = (operational_count / total_components) * 100
        
        # Rapport final
        final_report = {
            'validation_timestamp': datetime.now().isoformat(),
            'system_health_score': system_health_score,
            'total_components': total_components,
            'operational_components': operational_count,
            'component_validations': validations,
            'overall_status': 'fully_autonomous' if system_health_score >= 80 else 'partial_autonomy' if system_health_score >= 60 else 'requires_attention',
            'autonomy_capabilities': {
                'corpus_processing': validations['corpus_processor']['status'] == 'operational',
                'real_time_monitoring': validations['dashboard']['status'] == 'operational',
                'performance_optimization': validations['dhatu_optimizer']['status'] in ['operational', 'high_performance'],
                'crash_recovery': validations['recovery_system']['status'] == 'operational',
                'resource_management': validations['system_resources']['status'] in ['operational', 'high_load']
            }
        }
        
        # Sauvegarde rapport
        report_file = self.results_dir / 'autonomous_system_validation_final.json'
        with open(report_file, 'w') as f:
            json.dump(final_report, f, indent=2)
        
        # Affichage rapport
        self.log("=" * 70)
        self.log("🎯 RAPPORT FINAL - VALIDATION SYSTÈME AUTONOME")
        self.log("=" * 70)
        self.log(f"📊 Score santé système: {system_health_score:.1f}%")
        self.log(f"✅ Composants opérationnels: {operational_count}/{total_components}")
        self.log(f"🚀 Statut global: {final_report['overall_status'].upper()}")
        self.log("")
        
        self.log("🔍 DÉTAIL COMPOSANTS:")
        for name, validation in validations.items():
            status_icon = "✅" if validation['status'] in ['operational', 'high_performance'] else "⚠️" if validation['status'] in ['partial', 'low_performance'] else "❌"
            self.log(f"  {status_icon} {name}: {validation['status']}")
        self.log("")
        
        self.log("🎯 CAPACITÉS AUTONOMIE:")
        for capability, enabled in final_report['autonomy_capabilities'].items():
            icon = "✅" if enabled else "❌"
            self.log(f"  {icon} {capability}: {'ACTIVÉE' if enabled else 'INACTIVE'}")
        self.log("")
        
        if system_health_score >= 80:
            self.log("🏆 SUCCÈS: Système complètement autonome opérationnel!")
            self.log("🚀 Capable de fonctionner en autonomie totale")
            self.log("🛡️ Protection automatique contre les crashes")
            self.log("📊 Monitoring temps réel actif")
            self.log("⚡ Optimisation performance continue")
        else:
            self.log("⚠️ Système partiellement autonome - optimisations requises")
        
        self.log("=" * 70)
        self.log(f"💾 Rapport sauvegardé: {report_file}")
        
        return final_report

def main():
    validator = AutonomousSystemValidator()
    
    try:
        report = validator.generate_final_report()
        
        if report['overall_status'] == 'fully_autonomous':
            return 0
        else:
            return 1
            
    except Exception as e:
        validator.log(f"💥 ERREUR CRITIQUE VALIDATION: {e}")
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)