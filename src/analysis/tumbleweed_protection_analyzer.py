#!/usr/bin/env python3
"""
Analyseur des mécanismes de protection OpenSUSE Tumbleweed
Détecte les limites système et les contournements pour autonomie
"""

import os
import sys
import subprocess
import psutil
import time
from pathlib import Path


class TumbleweedProtectionAnalyzer:
    def __init__(self):
        self.workspace = Path('/home/stephane/GitHub/PaniniFS-Research')
        self.results_dir = self.workspace / 'autonomous_results'
        self.results_dir.mkdir(exist_ok=True)
        
        self.protection_mechanisms = {}
        self.current_limits = {}
        self.recommendations = []
        
        print("🔍 ANALYSE PROTECTIONS OPENSUSE TUMBLEWEED")
        print("=" * 50)
    
    def check_systemd_limits(self):
        """Vérifie les limites systemd"""
        print("📊 Analyse limites systemd...")
        
        try:
            # Limites utilisateur courantes
            result = subprocess.run(['systemctl', 'show-environment'], 
                                  capture_output=True, text=True)
            
            # Limites de session
            session_result = subprocess.run(['loginctl', 'show-session', 'self'], 
                                          capture_output=True, text=True)
            
            # Limites cgroup
            cgroup_result = subprocess.run(['systemd-cgtop', '-b', '-n', '1'], 
                                         capture_output=True, text=True)
            
            self.protection_mechanisms['systemd'] = {
                'environment': result.stdout if result.returncode == 0 else "N/A",
                'session_limits': session_result.stdout if session_result.returncode == 0 else "N/A",
                'cgroup_status': cgroup_result.stdout if cgroup_result.returncode == 0 else "N/A"
            }
            
            print("✅ Limites systemd analysées")
            
        except Exception as e:
            print(f"❌ Erreur analyse systemd: {e}")
            self.protection_mechanisms['systemd'] = {'error': str(e)}
    
    def check_oom_killer(self):
        """Vérifie le tueur OOM"""
        print("💀 Analyse OOM Killer...")
        
        try:
            # Configuration OOM
            oom_paths = [
                '/proc/sys/vm/oom_kill_allocating_task',
                '/proc/sys/vm/oom_dump_tasks', 
                '/proc/sys/vm/overcommit_memory',
                '/proc/sys/vm/overcommit_ratio'
            ]
            
            oom_config = {}
            for path in oom_paths:
                try:
                    with open(path) as f:
                        oom_config[os.path.basename(path)] = f.read().strip()
                except:
                    oom_config[os.path.basename(path)] = "N/A"
            
            # Vérification logs OOM récents
            try:
                oom_logs = subprocess.run(['journalctl', '-k', '--since=today', 
                                         '--grep=killed process'], 
                                        capture_output=True, text=True)
                oom_config['recent_kills'] = oom_logs.stdout
            except:
                oom_config['recent_kills'] = "N/A"
            
            self.protection_mechanisms['oom_killer'] = oom_config
            print("✅ OOM Killer analysé")
            
        except Exception as e:
            print(f"❌ Erreur analyse OOM: {e}")
            self.protection_mechanisms['oom_killer'] = {'error': str(e)}
    
    def check_ulimits(self):
        """Vérifie les ulimits système"""
        print("📋 Analyse ulimits...")
        
        try:
            # Ulimits actuelles
            ulimit_result = subprocess.run(['bash', '-c', 'ulimit -a'], 
                                         capture_output=True, text=True)
            
            # Limites spécifiques importantes
            important_limits = {}
            limit_checks = {
                'max_processes': 'ulimit -u',
                'max_files': 'ulimit -n', 
                'max_memory': 'ulimit -m',
                'max_cpu_time': 'ulimit -t',
                'max_virtual_memory': 'ulimit -v'
            }
            
            for name, cmd in limit_checks.items():
                try:
                    result = subprocess.run(['bash', '-c', cmd], 
                                          capture_output=True, text=True)
                    important_limits[name] = result.stdout.strip()
                except:
                    important_limits[name] = "N/A"
            
            self.protection_mechanisms['ulimits'] = {
                'all_limits': ulimit_result.stdout,
                'important_limits': important_limits
            }
            
            print("✅ Ulimits analysées")
            
        except Exception as e:
            print(f"❌ Erreur analyse ulimits: {e}")
            self.protection_mechanisms['ulimits'] = {'error': str(e)}
    
    def check_cpu_frequency_scaling(self):
        """Vérifie la gestion CPU"""
        print("⚡ Analyse gestion CPU...")
        
        try:
            cpu_info = {}
            
            # Gouverneur CPU
            cpu_count = psutil.cpu_count()
            cpu_info['cpu_count'] = cpu_count
            
            # Fréquences CPU
            try:
                cpu_freq = psutil.cpu_freq()
                cpu_info['cpu_freq'] = {
                    'current': cpu_freq.current,
                    'min': cpu_freq.min,
                    'max': cpu_freq.max
                }
            except:
                cpu_info['cpu_freq'] = "N/A"
            
            # Gouverneur actuel
            try:
                with open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor') as f:
                    cpu_info['governor'] = f.read().strip()
            except:
                cpu_info['governor'] = "N/A"
            
            # Gouverneurs disponibles
            try:
                with open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors') as f:
                    cpu_info['available_governors'] = f.read().strip().split()
            except:
                cpu_info['available_governors'] = "N/A"
            
            self.protection_mechanisms['cpu_management'] = cpu_info
            print("✅ Gestion CPU analysée")
            
        except Exception as e:
            print(f"❌ Erreur analyse CPU: {e}")
            self.protection_mechanisms['cpu_management'] = {'error': str(e)}
    
    def check_cgroup_limits(self):
        """Vérifie les limites cgroup v2"""
        print("🏗️ Analyse cgroups...")
        
        try:
            cgroup_info = {}
            
            # Détection cgroup v1 vs v2
            cgroup_version = "unknown"
            if os.path.exists('/sys/fs/cgroup/cgroup.controllers'):
                cgroup_version = "v2"
            elif os.path.exists('/sys/fs/cgroup/cpu'):
                cgroup_version = "v1"
            
            cgroup_info['version'] = cgroup_version
            
            # Limites mémoire
            memory_paths = [
                '/sys/fs/cgroup/memory.max',
                '/sys/fs/cgroup/memory.current', 
                '/sys/fs/cgroup/memory.high'
            ]
            
            memory_limits = {}
            for path in memory_paths:
                try:
                    with open(path) as f:
                        memory_limits[os.path.basename(path)] = f.read().strip()
                except:
                    memory_limits[os.path.basename(path)] = "N/A"
            
            cgroup_info['memory_limits'] = memory_limits
            
            # Limites CPU
            cpu_paths = [
                '/sys/fs/cgroup/cpu.max',
                '/sys/fs/cgroup/cpu.weight'
            ]
            
            cpu_limits = {}
            for path in cpu_paths:
                try:
                    with open(path) as f:
                        cpu_limits[os.path.basename(path)] = f.read().strip()
                except:
                    cpu_limits[os.path.basename(path)] = "N/A"
            
            cgroup_info['cpu_limits'] = cpu_limits
            
            self.protection_mechanisms['cgroups'] = cgroup_info
            print("✅ Cgroups analysés")
            
        except Exception as e:
            print(f"❌ Erreur analyse cgroups: {e}")
            self.protection_mechanisms['cgroups'] = {'error': str(e)}
    
    def analyze_current_process_limits(self):
        """Analyse les limites du processus actuel"""
        print("🔍 Analyse processus actuel...")
        
        try:
            current_process = psutil.Process()
            
            process_info = {
                'pid': current_process.pid,
                'cpu_percent': current_process.cpu_percent(),
                'memory_info': current_process.memory_info()._asdict(),
                'num_threads': current_process.num_threads(),
                'nice': current_process.nice()
            }
            
            # Limites de ressources
            try:
                import resource
                limits = {}
                resource_types = [
                    ('RLIMIT_CPU', resource.RLIMIT_CPU),
                    ('RLIMIT_FSIZE', resource.RLIMIT_FSIZE),
                    ('RLIMIT_DATA', resource.RLIMIT_DATA),
                    ('RLIMIT_STACK', resource.RLIMIT_STACK),
                    ('RLIMIT_CORE', resource.RLIMIT_CORE),
                    ('RLIMIT_RSS', resource.RLIMIT_RSS),
                    ('RLIMIT_NPROC', resource.RLIMIT_NPROC),
                    ('RLIMIT_NOFILE', resource.RLIMIT_NOFILE),
                    ('RLIMIT_MEMLOCK', resource.RLIMIT_MEMLOCK),
                    ('RLIMIT_AS', resource.RLIMIT_AS)
                ]
                
                for name, res_type in resource_types:
                    try:
                        soft, hard = resource.getrlimit(res_type)
                        limits[name] = {'soft': soft, 'hard': hard}
                    except:
                        limits[name] = {'soft': 'N/A', 'hard': 'N/A'}
                
                process_info['resource_limits'] = limits
                
            except ImportError:
                process_info['resource_limits'] = "Module resource non disponible"
            
            self.current_limits = process_info
            print("✅ Processus actuel analysé")
            
        except Exception as e:
            print(f"❌ Erreur analyse processus: {e}")
            self.current_limits = {'error': str(e)}
    
    def generate_protection_strategies(self):
        """Génère stratégies de contournement"""
        print("🛡️ Génération stratégies protection...")
        
        strategies = []
        
        # Stratégie 1: Nice values
        strategies.append({
            'name': 'CPU Nice Management',
            'description': 'Ajuster priorité processus pour éviter kills',
            'implementation': 'os.nice(10)  # Priorité plus basse',
            'risk': 'low'
        })
        
        # Stratégie 2: Memory chunking
        strategies.append({
            'name': 'Memory Chunking',
            'description': 'Traitement par petits chunks pour éviter OOM',
            'implementation': 'batch_size = min(1000, available_memory // chunk_size)',
            'risk': 'low'
        })
        
        # Stratégie 3: Process throttling
        strategies.append({
            'name': 'Process Throttling',
            'description': 'Limitation automatique charge CPU',
            'implementation': 'time.sleep(0.1) si cpu_percent > 80%',
            'risk': 'low'
        })
        
        # Stratégie 4: Resource monitoring
        strategies.append({
            'name': 'Resource Monitoring',
            'description': 'Surveillance continue avec auto-limitation',
            'implementation': 'Monitoring psutil avec seuils dynamiques',
            'risk': 'low'
        })
        
        # Stratégie 5: Cgroup exemption
        strategies.append({
            'name': 'Cgroup Exemption',
            'description': 'Demander exemption limites cgroup',
            'implementation': 'sudo systemctl set-property --runtime user.slice MemoryMax=infinity',
            'risk': 'high'
        })
        
        self.recommendations = strategies
        print("✅ Stratégies générées")
    
    def create_protection_bypass_script(self):
        """Crée script de contournement des protections"""
        bypass_script = self.workspace / 'tumbleweed_protection_bypass.py'
        
        script_content = '''#!/usr/bin/env python3
"""
Script de contournement protections Tumbleweed
Ajuste automatiquement les paramètres pour éviter les kills OS
"""

import os
import sys
import time
import psutil
import signal


class TumbleweedBypass:
    def __init__(self):
        self.max_cpu_percent = 75  # Limite CPU à 75%
        self.max_memory_percent = 80  # Limite RAM à 80%
        self.check_interval = 5  # Vérification toutes les 5s
        
        # Ajustement priorité processus
        try:
            os.nice(5)  # Priorité plus basse
            print("✅ Priorité processus ajustée")
        except:
            print("⚠️ Impossible ajuster priorité")
    
    def monitor_and_throttle(self):
        """Surveillance et limitation automatique"""
        while True:
            try:
                # Métriques système
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                
                # Limitation CPU
                if cpu_percent > self.max_cpu_percent:
                    print(f"🛑 CPU élevé ({cpu_percent:.1f}%) - throttling")
                    time.sleep(2)  # Pause forcée
                
                # Limitation mémoire
                if memory.percent > self.max_memory_percent:
                    print(f"🛑 RAM élevée ({memory.percent:.1f}%) - limitation")
                    # Forcer garbage collection
                    import gc
                    gc.collect()
                
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                print("🛑 Arrêt surveillance")
                break
            except Exception as e:
                print(f"❌ Erreur surveillance: {e}")
                time.sleep(10)


if __name__ == '__main__':
    bypass = TumbleweedBypass()
    bypass.monitor_and_throttle()
'''
        
        bypass_script.write_text(script_content)
        bypass_script.chmod(0o755)
        
        print(f"📜 Script protection créé: {bypass_script}")
        return bypass_script
    
    def save_analysis_report(self):
        """Sauvegarde rapport d'analyse"""
        report = {
            'analysis_timestamp': time.time(),
            'protection_mechanisms': self.protection_mechanisms,
            'current_limits': self.current_limits,
            'recommendations': self.recommendations,
            'os_info': {
                'platform': sys.platform,
                'python_version': sys.version,
                'cpu_count': psutil.cpu_count(),
                'memory_total': psutil.virtual_memory().total
            }
        }
        
        report_file = self.results_dir / 'tumbleweed_protection_analysis.json'
        import json
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"💾 Rapport sauvegardé: {report_file}")
        return report
    
    def print_summary(self):
        """Affiche résumé de l'analyse"""
        print("\n" + "=" * 60)
        print("📋 RÉSUMÉ ANALYSE PROTECTIONS TUMBLEWEED")
        print("=" * 60)
        
        print(f"🖥️ Système: openSUSE Tumbleweed")
        print(f"🔍 Mécanismes détectés: {len(self.protection_mechanisms)}")
        print(f"🛡️ Stratégies recommandées: {len(self.recommendations)}")
        
        print("\n🔍 MÉCANISMES ACTIFS:")
        for mechanism, data in self.protection_mechanisms.items():
            status = "✅" if 'error' not in data else "❌"
            print(f"  {status} {mechanism}")
        
        print("\n🛡️ RECOMMANDATIONS CLÉS:")
        for i, rec in enumerate(self.recommendations[:3], 1):
            print(f"  {i}. {rec['name']} (risque: {rec['risk']})")
        
        print(f"\n🎯 CONCLUSION:")
        print("Pour éviter les kills OS, implémenter surveillance")
        print("ressources avec auto-limitation proactive.")


def main():
    analyzer = TumbleweedProtectionAnalyzer()
    
    # Analyses principales
    analyzer.check_systemd_limits()
    analyzer.check_oom_killer()
    analyzer.check_ulimits()
    analyzer.check_cpu_frequency_scaling()
    analyzer.check_cgroup_limits()
    analyzer.analyze_current_process_limits()
    
    # Stratégies et solutions
    analyzer.generate_protection_strategies()
    analyzer.create_protection_bypass_script()
    
    # Rapport final
    analyzer.save_analysis_report()
    analyzer.print_summary()


if __name__ == '__main__':
    main()