#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Validation des Commandes - Spec-Kit PaniniFS
Implémente la directive d'approbation automatique des commandes
"""

import json
import re
import sys
import os
import time
from datetime import datetime
from pathlib import Path

class CommandValidator:
    def __init__(self, config_path=None):
        self.config_path = config_path or os.path.join(
            os.path.dirname(__file__), 
            "../copilot-approved-scripts.json"
        )
        self.config = self._load_config()
        self.log_path = os.path.join(
            os.path.dirname(__file__), 
            "../logs/command_execution.log"
        )
        
    def _load_config(self):
        """Charger la configuration d'approbation"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Erreur chargement config: {e}")
            return None
    
    def validate_command(self, command, args="", workspace_path=""):
        """Validation principale d'une commande"""
        start_time = time.time()
        
        # 1. Vérification config disponible
        if not self.config:
            return self._fail_safe_response("Config non disponible")
        
        # 2. Recherche pattern correspondant
        matching_pattern = self._find_matching_pattern(command, args)
        if not matching_pattern:
            return self._create_response(
                False, "Aucun pattern correspondant trouvé", 
                command, args, time.time() - start_time
            )
        
        # 3. Validation contraintes sécurité
        security_check = self._check_security_constraints(command, args, workspace_path)
        if not security_check['safe']:
            return self._create_response(
                False, f"Contrainte sécurité: {security_check['reason']}", 
                command, args, time.time() - start_time
            )
        
        # 4. Validation contraintes contextuelles
        context_check = self._check_execution_context(command, args, workspace_path)
        if not context_check['valid']:
            return self._create_response(
                False, f"Contrainte contexte: {context_check['reason']}", 
                command, args, time.time() - start_time
            )
        
        return self._create_response(
            True, f"Approuvé via pattern: {matching_pattern['category']}", 
            command, args, time.time() - start_time, matching_pattern
        )
    
    def _find_matching_pattern(self, command, args):
        """Trouver un pattern correspondant"""
        full_command = f"{command} {args}"
        
        # Mode debug
        if os.getenv('DEBUG_VALIDATION'):
            print(f"🔍 Recherche pattern pour: '{full_command}'")
        
        # Vérifier dans chaque catégorie
        for category, commands in self.config.get('approved_commands', {}).items():
            if not isinstance(commands, list):
                continue
                
            if os.getenv('DEBUG_VALIDATION'):
                print(f"  📂 Catégorie: {category} ({len(commands)} patterns)")
                
            for cmd_config in commands:
                pattern = cmd_config.get('pattern', '')
                
                # Conversion pattern vers regex
                regex_pattern = self._pattern_to_regex(pattern)
                
                if os.getenv('DEBUG_VALIDATION'):
                    print(f"    🔎 Pattern: '{pattern}' -> '{regex_pattern}'")
                
                if re.match(regex_pattern, full_command, re.IGNORECASE):
                    if os.getenv('DEBUG_VALIDATION'):
                        print(f"    ✅ Match trouvé!")
                    
                    # Vérifier conditions additionnelles
                    condition = cmd_config.get('condition', 'always')
                    if self._check_condition(condition, command, args):
                        return {
                            'category': category,
                            'pattern': pattern,
                            'config': cmd_config
                        }
                    elif os.getenv('DEBUG_VALIDATION'):
                        print(f"    ❌ Condition échouée: {condition}")
                elif os.getenv('DEBUG_VALIDATION'):
                    print(f"    ❌ Pas de match")
        
        # Vérifier dans approved_patterns pour scripts Python
        if command.startswith('python3') and args.endswith('.py'):
            script_name = args.split()[-1].replace('.py', '')
            for pattern_name, pattern_config in self.config.get('approved_patterns', {}).items():
                pattern = pattern_config.get('pattern', '')
                if self._match_script_pattern(script_name, pattern):
                    return {
                        'category': 'script_patterns',
                        'pattern': pattern,
                        'config': pattern_config
                    }
        
        return None
    
    def _pattern_to_regex(self, pattern):
        """Convertir un pattern en regex"""
        # Échapper les caractères spéciaux regex d'abord
        regex = re.escape(pattern)
        
        # Puis traiter les placeholders
        # Remplacer {variable} par des groupes nommés  
        regex = re.sub(r'\\{(\w+)\\}', r'(?P<\1>[^\\s]+)', regex)
        
        # Remplacer * et ? pour les wildcards
        regex = regex.replace('\\*', '.*')
        regex = regex.replace('\\?', '.')
        
        # Patterns spéciaux plus stricts
        regex = regex.replace('(?P<script_name>[^\\s]+)', r'(?P<script_name>[\w_.-]+)')
        regex = regex.replace('(?P<port>[^\\s]+)', r'(?P<port>\d{4,5})')
        regex = regex.replace('(?P<seconds>[^\\s]+)', r'(?P<seconds>\d{1,4})')
        regex = regex.replace('(?P<path>[^\\s]+)', r'(?P<path>[\w/.,-]+)')
        regex = regex.replace('(?P<filename>[^\\s]+)', r'(?P<filename>[\w/.,-]+)')
        regex = regex.replace('(?P<args>[^\\s]+)', r'(?P<args>.*)')
        
        # Ancrer le pattern complet
        return f'^{regex}$'
    
    def _match_script_pattern(self, script_name, pattern):
        """Vérifier si un script correspond à un pattern"""
        if '**/*' in pattern:
            pattern = pattern.replace('**/*', '')
        
        # Patterns spéciaux
        pattern_checks = {
            '_extractor.py': script_name.endswith('_extractor'),
            '_analyzer.py': script_name.endswith('_analyzer'),
            '_validator.py': script_name.endswith('_validator'),
            'panini_*.py': script_name.startswith('panini_'),
            'demo_*.py': script_name.startswith('demo_'),
            'test_*.py': script_name.startswith('test_'),
            '*_generator.py': script_name.endswith('_generator')
        }
        
        return pattern_checks.get(pattern, False)
    
    def _check_condition(self, condition, command, args):
        """Vérifier les conditions d'approbation"""
        if condition == 'always':
            return True
        
        # Conditions simples
        if 'script_name matches approved_patterns' in condition:
            return True  # Déjà vérifié dans find_matching_pattern
        
        if 'port between' in condition:
            # Extraire port des arguments
            port_match = re.search(r':(\d+)', args)
            if port_match:
                port = int(port_match.group(1))
                if 'port between 3000-9999' in condition:
                    return 3000 <= port <= 9999
        
        if 'seconds <=' in condition:
            # Extraire valeur numérique
            num_match = re.search(r'(\d+)', args)
            if num_match:
                value = int(num_match.group(1))
                if 'seconds <= 10' in condition:
                    return value <= 10
                elif 'seconds <= 300' in condition:
                    return value <= 300
        
        return True  # Par défaut, accepter si condition non comprise
    
    def _check_security_constraints(self, command, args, workspace_path):
        """Vérifier les contraintes de sécurité"""
        full_command = f"{command} {args}".strip()
        
        # Vérifier commandes interdites
        forbidden = self.config.get('safety_constraints', {}).get('forbidden_operations', [])
        for forbidden_op in forbidden:
            if forbidden_op in full_command:
                return {'safe': False, 'reason': f'Opération interdite: {forbidden_op}'}
        
        # Vérifier répertoire autorisé
        allowed_dirs = self.config.get('safety_constraints', {}).get('execution_limits', {}).get('allowed_directories', [])
        if workspace_path and allowed_dirs:
            workspace_allowed = any(workspace_path.startswith(allowed_dir) for allowed_dir in allowed_dirs)
            if not workspace_allowed:
                return {'safe': False, 'reason': f'Répertoire non autorisé: {workspace_path}'}
        
        return {'safe': True, 'reason': 'Sécurité OK'}
    
    def _check_execution_context(self, command, args, workspace_path):
        """Vérifier le contexte d'exécution"""
        # Vérifications basiques
        if command == 'rm' and '-rf' in args:
            return {'valid': False, 'reason': 'rm -rf dangereux'}
        
        # Vérifier ports autorisés pour serveurs
        if 'http.server' in args or any(server_cmd in args for server_cmd in ['panini_', 'demo_', 'serveur_']):
            port_match = re.search(r'(\d{4,5})', args)
            if port_match:
                port = int(port_match.group(1))
                if not (3000 <= port <= 9999):
                    return {'valid': False, 'reason': f'Port {port} non autorisé (3000-9999 requis)'}
        
        return {'valid': True, 'reason': 'Contexte OK'}
    
    def _create_response(self, approved, reason, command, args, duration, pattern=None):
        """Créer la réponse de validation"""
        response = {
            'approved': approved,
            'reason': reason,
            'command': command,
            'args': args,
            'validation_duration_ms': round(duration * 1000, 2),
            'timestamp': datetime.now().isoformat(),
            'pattern_used': pattern.get('pattern') if pattern else None
        }
        
        # Logger la décision
        self._log_decision(response)
        
        return response
    
    def _fail_safe_response(self, reason):
        """Réponse fail-safe en cas de problème"""
        return {
            'approved': False,
            'reason': f'FAIL-SAFE: {reason}',
            'fail_safe_mode': True,
            'timestamp': datetime.now().isoformat()
        }
    
    def _log_decision(self, response):
        """Logger la décision dans le fichier de log"""
        try:
            os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
            
            log_entry = {
                'timestamp': response['timestamp'],
                'status': 'APPROVED' if response['approved'] else 'REJECTED',
                'command': response['command'],
                'args': response['args'],
                'reason': response['reason'],
                'duration_ms': response['validation_duration_ms']
            }
            
            with open(self.log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
                
        except Exception as e:
            print(f"⚠️ Erreur logging: {e}")

def main():
    """Point d'entrée principal"""
    if len(sys.argv) < 2:
        print("Usage: python3 validate_command.py <command> [args] [workspace_path]")
        sys.exit(1)
    
    command = sys.argv[1]
    args = sys.argv[2] if len(sys.argv) > 2 else ""
    workspace_path = sys.argv[3] if len(sys.argv) > 3 else os.getcwd()
    
    validator = CommandValidator()
    result = validator.validate_command(command, args, workspace_path)
    
    # Affichage résultat
    status_icon = "✅" if result['approved'] else "❌"
    print(f"{status_icon} {result['reason']}")
    print(f"⏱️ Validation: {result.get('validation_duration_ms', 0)}ms")
    
    if result.get('pattern_used'):
        print(f"📋 Pattern: {result['pattern_used']}")
    
    # Code de sortie
    sys.exit(0 if result['approved'] else 1)

if __name__ == '__main__':
    main()