#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Optimiseur Hebdomadaire - Spec-Kit PaniniFS
Analyse les logs et optimise automatiquement les patterns d'approbation
"""

import json
import os
import re
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from pathlib import Path

class WeeklyOptimizer:
    def __init__(self, config_path=None, log_path=None):
        self.config_path = config_path or os.path.join(
            os.path.dirname(__file__), 
            "../copilot-approved-scripts.json"
        )
        self.log_path = log_path or os.path.join(
            os.path.dirname(__file__), 
            "../logs/command_execution.log"
        )
        self.optimization_log = os.path.join(
            os.path.dirname(__file__), 
            "../logs/optimization_history.log"
        )
        
    def analyze_and_optimize(self, days=7):
        """Analyse complète et optimisation"""
        print(f"🔄 Démarrage analyse hebdomadaire ({days} jours)")
        
        # 1. Charger et analyser les logs
        logs = self._load_logs(days)
        analysis = self._analyze_logs(logs)
        
        # 2. Identifier les optimisations nécessaires
        optimizations = self._identify_optimizations(analysis)
        
        # 3. Appliquer les optimisations sûres
        applied = self._apply_safe_optimizations(optimizations)
        
        # 4. Générer rapport
        report = self._generate_report(analysis, optimizations, applied)
        
        # 5. Logger l'optimisation
        self._log_optimization(report)
        
        print(f"✅ Optimisation terminée: {len(applied)} changements appliqués")
        return report
    
    def _load_logs(self, days):
        """Charger les logs des derniers jours"""
        logs = []
        cutoff_date = datetime.now() - timedelta(days=days)
        
        try:
            if not os.path.exists(self.log_path):
                print(f"⚠️ Fichier log non trouvé: {self.log_path}")
                return logs
                
            with open(self.log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        log_entry = json.loads(line.strip())
                        log_date = datetime.fromisoformat(log_entry['timestamp'].replace('Z', '+00:00'))
                        
                        if log_date >= cutoff_date:
                            logs.append(log_entry)
                    except Exception as e:
                        print(f"⚠️ Erreur parsing log: {e}")
                        continue
        except Exception as e:
            print(f"❌ Erreur lecture logs: {e}")
        
        return logs
    
    def _analyze_logs(self, logs):
        """Analyser les patterns dans les logs"""
        analysis = {
            'total_commands': len(logs),
            'approved': sum(1 for log in logs if log['status'] == 'APPROVED'),
            'rejected': sum(1 for log in logs if log['status'] == 'REJECTED'),
            'avg_duration': 0,
            'rejected_commands': [],
            'frequent_commands': Counter(),
            'slow_validations': [],
            'error_patterns': defaultdict(int)
        }
        
        # Statistiques de base
        if logs:
            durations = [log.get('duration_ms', 0) for log in logs]
            analysis['avg_duration'] = sum(durations) / len(durations)
        
        # Analyse détaillée
        for log in logs:
            command_signature = f"{log['command']} {log['args'][:50]}"
            analysis['frequent_commands'][command_signature] += 1
            
            if log['status'] == 'REJECTED':
                analysis['rejected_commands'].append({
                    'command': log['command'],
                    'args': log['args'],
                    'reason': log['reason'],
                    'timestamp': log['timestamp']
                })
                
                # Catégoriser les erreurs
                if 'pattern' in log['reason'].lower():
                    analysis['error_patterns']['missing_pattern'] += 1
                elif 'sécurité' in log['reason'].lower():
                    analysis['error_patterns']['security_constraint'] += 1
                elif 'contexte' in log['reason'].lower():
                    analysis['error_patterns']['context_validation'] += 1
                else:
                    analysis['error_patterns']['other'] += 1
            
            if log.get('duration_ms', 0) > 1000:  # > 1 seconde
                analysis['slow_validations'].append(log)
        
        return analysis
    
    def _identify_optimizations(self, analysis):
        """Identifier les optimisations nécessaires"""
        optimizations = {
            'new_patterns': [],
            'extended_patterns': [],
            'performance_improvements': [],
            'security_adjustments': []
        }
        
        # 1. Patterns manquants (commandes légitimes rejetées)
        legitimate_rejected = self._identify_legitimate_rejections(analysis['rejected_commands'])
        for cmd in legitimate_rejected:
            new_pattern = self._generate_safe_pattern(cmd)
            if new_pattern:
                optimizations['new_patterns'].append(new_pattern)
        
        # 2. Extensions de patterns existants
        frequent_rejections = [cmd for cmd, count in analysis['frequent_commands'].most_common(10) 
                             if any(rej['command'] in cmd for rej in analysis['rejected_commands'])]
        
        for cmd_pattern in frequent_rejections:
            extension = self._suggest_pattern_extension(cmd_pattern)
            if extension:
                optimizations['extended_patterns'].append(extension)
        
        # 3. Améliorations performance
        if analysis['avg_duration'] > 500:  # > 500ms
            optimizations['performance_improvements'].append({
                'type': 'regex_optimization',
                'reason': f'Temps moyen: {analysis["avg_duration"]:.1f}ms',
                'action': 'Compiler les regex fréquemment utilisées'
            })
        
        # 4. Ajustements sécurité
        security_ratio = analysis['error_patterns']['security_constraint'] / max(analysis['total_commands'], 1)
        if security_ratio > 0.1:  # > 10% d'erreurs de sécurité
            optimizations['security_adjustments'].append({
                'type': 'security_hardening',
                'reason': f'Taux erreurs sécurité: {security_ratio:.1%}',
                'action': 'Durcir les contraintes de sécurité'
            })
        
        return optimizations
    
    def _identify_legitimate_rejections(self, rejected_commands):
        """Identifier les rejets de commandes légitimes"""
        legitimate = []
        
        for cmd in rejected_commands:
            # Heuristiques pour identifier les commandes légitimes
            if self._is_development_command(cmd):
                legitimate.append(cmd)
            elif self._is_safe_operation(cmd):
                legitimate.append(cmd)
        
        return legitimate
    
    def _is_development_command(self, cmd):
        """Vérifier si c'est une commande de développement"""
        dev_indicators = [
            'panini', 'demo', 'test', 'localhost', '127.0.0.1',
            'python3', 'git', 'curl', 'wget', 'jq'
        ]
        
        command_text = f"{cmd['command']} {cmd['args']}".lower()
        return any(indicator in command_text for indicator in dev_indicators)
    
    def _is_safe_operation(self, cmd):
        """Vérifier si c'est une opération sûre"""
        safe_patterns = [
            r'ls -la?',
            r'cat .*\.json',
            r'head -\d+ ',
            r'tail -\d+ ',
            r'grep -r',
            r'find .* -name',
            r'wc -l'
        ]
        
        command_text = f"{cmd['command']} {cmd['args']}"
        return any(re.match(pattern, command_text) for pattern in safe_patterns)
    
    def _generate_safe_pattern(self, cmd):
        """Générer un pattern sûr pour une commande"""
        command = cmd['command']
        args = cmd['args']
        
        # Patterns spécifiques par type de commande
        if command == 'python3' and 'panini' in args:
            return {
                'pattern': 'python3 panini_*.py {args}',
                'category': 'python_execution',
                'condition': 'args safe for panini scripts',
                'auto_approve': True,
                'reason': f'Fréquemment utilisé: {command} {args[:30]}...'
            }
        
        elif command == 'curl' and '127.0.0.1' in args:
            return {
                'pattern': 'curl {options} "http://127.0.0.1:{port}/{path}"',
                'category': 'network_testing',
                'condition': 'port between 3000-9999',
                'auto_approve': True,
                'reason': f'Test API local: {args[:50]}...'
            }
        
        elif command in ['ls', 'cat', 'head', 'tail']:
            return {
                'pattern': f'{command} {{args}}',
                'category': 'file_operations',
                'condition': 'safe file operations only',
                'auto_approve': True,
                'reason': f'Opération lecture sûre: {command}'
            }
        
        return None
    
    def _suggest_pattern_extension(self, cmd_pattern):
        """Suggérer une extension de pattern existant"""
        # Pour l'instant, retourner None - à implémenter selon les besoins
        return None
    
    def _apply_safe_optimizations(self, optimizations):
        """Appliquer les optimisations sûres"""
        applied = []
        
        try:
            # Charger config actuelle
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Appliquer nouveaux patterns
            for pattern in optimizations['new_patterns']:
                if self._is_safe_to_add(pattern):
                    category = pattern['category']
                    if category not in config['approved_commands']:
                        config['approved_commands'][category] = []
                    
                    config['approved_commands'][category].append({
                        'pattern': pattern['pattern'],
                        'condition': pattern['condition'],
                        'auto_approve': pattern['auto_approve'],
                        'notes': f"Auto-ajouté: {pattern['reason']}"
                    })
                    
                    applied.append({
                        'type': 'new_pattern',
                        'pattern': pattern['pattern'],
                        'category': category
                    })
            
            # Mettre à jour métadonnées
            config['metadata']['last_updated'] = datetime.now().isoformat()
            if 'optimization_count' not in config['metadata']:
                config['metadata']['optimization_count'] = 0
            config['metadata']['optimization_count'] += len(applied)
            
            # Sauvegarder si des changements ont été appliqués
            if applied:
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                    
        except Exception as e:
            print(f"❌ Erreur application optimisations: {e}")
        
        return applied
    
    def _is_safe_to_add(self, pattern):
        """Vérifier qu'un pattern est sûr à ajouter"""
        dangerous_keywords = [
            'rm -rf', 'sudo', 'chmod 777', 'eval', 'exec',
            '| bash', '| sh', '/etc/', '/var/', '/usr/'
        ]
        
        pattern_text = pattern['pattern'].lower()
        return not any(keyword in pattern_text for keyword in dangerous_keywords)
    
    def _generate_report(self, analysis, optimizations, applied):
        """Générer le rapport d'optimisation"""
        return {
            'timestamp': datetime.now().isoformat(),
            'analysis_period_days': 7,
            'statistics': {
                'total_commands': analysis['total_commands'],
                'approval_rate': f"{(analysis['approved'] / max(analysis['total_commands'], 1) * 100):.1f}%",
                'avg_validation_time': f"{analysis['avg_duration']:.1f}ms",
                'rejected_commands': len(analysis['rejected_commands'])
            },
            'optimizations_identified': {
                'new_patterns': len(optimizations['new_patterns']),
                'pattern_extensions': len(optimizations['extended_patterns']),
                'performance_improvements': len(optimizations['performance_improvements']),
                'security_adjustments': len(optimizations['security_adjustments'])
            },
            'applied_changes': len(applied),
            'applied_details': applied,
            'recommendations': self._generate_recommendations(analysis, optimizations)
        }
    
    def _generate_recommendations(self, analysis, optimizations):
        """Générer des recommandations"""
        recommendations = []
        
        if analysis['avg_duration'] > 1000:
            recommendations.append("Optimiser les regex pour réduire le temps de validation")
        
        rejection_rate = len(analysis['rejected_commands']) / max(analysis['total_commands'], 1)
        if rejection_rate > 0.1:
            recommendations.append("Réviser les patterns pour réduire les faux rejets")
        
        if analysis['error_patterns']['security_constraint'] > 5:
            recommendations.append("Examiner les contraintes de sécurité trop restrictives")
        
        return recommendations
    
    def _log_optimization(self, report):
        """Logger le résultat de l'optimisation"""
        try:
            os.makedirs(os.path.dirname(self.optimization_log), exist_ok=True)
            
            with open(self.optimization_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(report, ensure_ascii=False) + '\n')
                
        except Exception as e:
            print(f"⚠️ Erreur logging optimisation: {e}")

def main():
    """Point d'entrée principal"""
    print("🔄 Optimiseur Hebdomadaire PaniniFS")
    
    optimizer = WeeklyOptimizer()
    report = optimizer.analyze_and_optimize()
    
    print("\n📊 RAPPORT D'OPTIMISATION")
    print(f"📈 Commandes analysées: {report['statistics']['total_commands']}")
    print(f"✅ Taux d'approbation: {report['statistics']['approval_rate']}")
    print(f"⏱️ Temps validation moyen: {report['statistics']['avg_validation_time']}")
    print(f"🔧 Changements appliqués: {report['applied_changes']}")
    
    if report['recommendations']:
        print("\n💡 RECOMMANDATIONS:")
        for rec in report['recommendations']:
            print(f"   • {rec}")
    
    return 0

if __name__ == '__main__':
    exit(main())