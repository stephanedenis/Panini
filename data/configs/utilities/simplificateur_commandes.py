#!/usr/bin/env python3
"""
Détecteur et Simplificateur Automatique de Commandes Complexes
Analyse les commandes et génère automatiquement des scripts Python simplifiés.
"""

import re
import os
import sys
import textwrap
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import subprocess
import shlex

@dataclass
class CommandAnalysis:
    """Analyse d'une commande pour déterminer sa complexité."""
    command: str
    complexity_score: int
    reasons: List[str]
    is_complex: bool
    suggested_filename: str
    generated_script: str

class CommandSimplifier:
    """Analyseur et simplificateur de commandes complexes."""
    
    COMPLEXITY_PATTERNS = {
        'pipes': (r'\|(?!\|)', 'Utilisation de pipes'),
        'redirections': (r'[>&]\d*', 'Redirections de flux'),
        'logical_operators': (r'&&|\|\|', 'Opérateurs logiques'),
        'background_jobs': (r'&\s*$', 'Processus en arrière-plan'),
        'command_substitution': (r'\$\(.*?\)|`.*?`', 'Substitution de commandes'),
        'wildcards': (r'\*|\?|\[.*?\]', 'Caractères génériques complexes'),
        'regex': (r'-E\s+["\'].*?["\']|grep\s+["\'].*?["\']', 'Expressions régulières'),
        'loops': (r'\bfor\b|\bwhile\b|\bdo\b', 'Boucles'),
        'many_options': (r'-\w{3,}|--\w+.*?--\w+', 'Nombreuses options'),
        'file_operations': (r'\bfind\b.*?-exec|\bxargs\b', 'Opérations sur fichiers multiples'),
    }
    
    COMMAND_TEMPLATES = {
        'process_management': {
            'pattern': r'ps\s+.*?\|\s*grep.*?\|\s*(?:awk|cut).*?\|\s*xargs.*?kill',
            'template': '''#!/usr/bin/env python3
"""Script pour gérer les processus {process_name}."""

import subprocess
import signal
import psutil
import sys

def find_processes(pattern):
    """Trouve les processus correspondant au pattern."""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = ' '.join(proc.info['cmdline'] or [])
            if pattern.lower() in cmdline.lower() or pattern.lower() in proc.info['name'].lower():
                processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return processes

def terminate_processes(pattern, force=False):
    """Termine les processus correspondant au pattern."""
    processes = find_processes(pattern)
    if not processes:
        print(f"Aucun processus trouvé pour: {{pattern}}")
        return 0
    
    print(f"Processus trouvés: {{len(processes)}}")
    for proc in processes:
        try:
            print(f"  PID {{proc.pid}}: {{proc.name()}} - {{' '.join(proc.cmdline() or [])}}")
            if force:
                proc.kill()
            else:
                proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print(f"  Erreur pour PID {{proc.pid}}: {{e}}")
    
    return len(processes)

def main():
    """Fonction principale."""
    pattern = "{process_pattern}"
    try:
        count = terminate_processes(pattern)
        print(f"✅ {{count}} processus traités")
        return 0
    except Exception as e:
        print(f"❌ Erreur: {{e}}")
        return 1

if __name__ == "__main__":
    exit(main())'''
        },
        
        'file_search': {
            'pattern': r'find\s+.*?-name.*?-exec.*?grep.*?\\;',
            'template': '''#!/usr/bin/env python3
"""Script pour rechercher dans les fichiers."""

import os
import re
import sys
from pathlib import Path

def search_in_files(directory, file_pattern, search_pattern, case_sensitive=True):
    """Recherche un pattern dans les fichiers correspondants."""
    results = []
    flags = 0 if case_sensitive else re.IGNORECASE
    
    try:
        search_regex = re.compile(search_pattern, flags)
        file_regex = re.compile(file_pattern.replace('*', '.*').replace('?', '.'))
    except re.error as e:
        print(f"❌ Erreur dans les expressions régulières: {{e}}")
        return []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file_regex.match(file):
                file_path = Path(root) / file
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line_num, line in enumerate(f, 1):
                            if search_regex.search(line):
                                results.append({{
                                    'file': str(file_path),
                                    'line': line_num,
                                    'content': line.strip()
                                }})
                except (UnicodeDecodeError, PermissionError):
                    continue
    
    return results

def main():
    """Fonction principale."""
    directory = "{search_directory}"
    file_pattern = "{file_pattern}"
    search_pattern = "{search_pattern}"
    
    try:
        results = search_in_files(directory, file_pattern, search_pattern)
        
        if not results:
            print("Aucun résultat trouvé")
            return 0
        
        print(f"{{len(results)}} résultats trouvés:")
        for result in results:
            print(f"  {{result['file']}}:{{result['line']}}: {{result['content']}}")
        
        return 0
    except Exception as e:
        print(f"❌ Erreur: {{e}}")
        return 1

if __name__ == "__main__":
    exit(main())'''
        },
        
        'log_analysis': {
            'pattern': r'tail.*?\|\s*grep.*?\|\s*(?:awk|cut|sort)',
            'template': '''#!/usr/bin/env python3
"""Script pour analyser les logs."""

import re
import sys
from pathlib import Path
from collections import defaultdict, Counter
import datetime

def analyze_log_file(file_path, pattern=None, lines_count=100):
    """Analyse un fichier de log."""
    results = {{
        'total_lines': 0,
        'matches': [],
        'patterns': Counter(),
        'timestamps': []
    }}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            results['total_lines'] = len(lines)
            
            # Prendre les dernières lignes
            recent_lines = lines[-lines_count:] if len(lines) > lines_count else lines
            
            for line_num, line in enumerate(recent_lines, 1):
                line = line.strip()
                if not line:
                    continue
                
                # Recherche de pattern
                if pattern and re.search(pattern, line, re.IGNORECASE):
                    results['matches'].append({{
                        'line_num': len(lines) - len(recent_lines) + line_num,
                        'content': line
                    }})
                
                # Extraction des timestamps
                timestamp_match = re.search(r'\\d{{4}}-\\d{{2}}-\\d{{2}}\\s+\\d{{2}}:\\d{{2}}:\\d{{2}}', line)
                if timestamp_match:
                    results['timestamps'].append(timestamp_match.group())
        
    except (FileNotFoundError, PermissionError) as e:
        print(f"❌ Erreur lecture fichier: {{e}}")
        return None
    
    return results

def main():
    """Fonction principale."""
    log_file = "{log_file}"
    search_pattern = "{search_pattern}"
    
    try:
        results = analyze_log_file(log_file, search_pattern)
        
        if not results:
            return 1
        
        print(f"📊 Analyse de {{log_file}}")
        print(f"  Total lignes: {{results['total_lines']}}")
        
        if results['matches']:
            print(f"  Correspondances trouvées: {{len(results['matches'])}}")
            for match in results['matches'][-10:]:  # Dernières 10
                print(f"    L{{match['line_num']}}: {{match['content']}}")
        else:
            print("  Aucune correspondance trouvée")
        
        return 0
    except Exception as e:
        print(f"❌ Erreur: {{e}}")
        return 1

if __name__ == "__main__":
    exit(main())'''
        }
    }
    
    def __init__(self):
        """Initialise le simplificateur."""
        self.scripts_dir = Path("scripts_generes")
        self.scripts_dir.mkdir(exist_ok=True)
    
    def analyze_command(self, command: str) -> CommandAnalysis:
        """Analyse la complexité d'une commande."""
        complexity_score = 0
        reasons = []
        
        # Analyse des patterns de complexité
        for pattern_name, (pattern, description) in self.COMPLEXITY_PATTERNS.items():
            matches = re.findall(pattern, command)
            if matches:
                complexity_score += len(matches)
                reasons.append(f"{description} ({len(matches)} occurrences)")
        
        # Critères supplémentaires
        command_parts = shlex.split(command) if command else []
        if len(command_parts) > 5:
            complexity_score += 2
            reasons.append(f"Nombreux arguments ({len(command_parts)} parties)")
        
        is_complex = complexity_score >= 3
        
        # Génération du nom de fichier suggéré
        suggested_filename = self._generate_filename(command)
        
        # Génération du script si complexe
        generated_script = ""
        if is_complex:
            generated_script = self._generate_script(command, suggested_filename)
        
        return CommandAnalysis(
            command=command,
            complexity_score=complexity_score,
            reasons=reasons,
            is_complex=is_complex,
            suggested_filename=suggested_filename,
            generated_script=generated_script
        )
    
    def _generate_filename(self, command: str) -> str:
        """Génère un nom de fichier basé sur la commande."""
        # Extraction du verbe principal
        main_verbs = {
            'find': 'rechercher',
            'grep': 'filtrer',
            'ps': 'lister_processus',
            'kill': 'arreter_processus',
            'tail': 'analyser_logs',
            'sort': 'trier',
            'awk': 'extraire_donnees',
            'sed': 'modifier_texte',
            'rsync': 'synchroniser',
            'tar': 'archiver',
            'chmod': 'modifier_permissions'
        }
        
        words = command.split()
        if not words:
            return "script_genere.py"
        
        main_command = words[0]
        verb = main_verbs.get(main_command, main_command)
        
        # Détection de l'objet
        if 'process' in command or 'ps' in command:
            return f"{verb}_processus.py"
        elif '.log' in command or 'tail' in command:
            return f"{verb}_logs.py"
        elif 'file' in command or 'find' in command:
            return f"{verb}_fichiers.py"
        else:
            return f"{verb}_donnees.py"
    
    def _generate_script(self, command: str, filename: str) -> str:
        """Génère le script Python correspondant."""
        # Détection du type de commande et utilisation du template approprié
        for template_name, template_info in self.COMMAND_TEMPLATES.items():
            if re.search(template_info['pattern'], command):
                return self._fill_template(template_info['template'], command)
        
        # Template générique
        return self._generate_generic_script(command, filename)
    
    def _fill_template(self, template: str, command: str) -> str:
        """Remplit un template avec les informations de la commande."""
        # Extraction des informations spécifiques
        placeholders = {
            'process_name': 'processus',
            'process_pattern': 'pattern',
            'search_directory': '.',
            'file_pattern': '*',
            'search_pattern': 'pattern',
            'log_file': '/var/log/syslog',
        }
        
        # Analyse spécifique selon le type de commande
        if 'grep' in command:
            grep_match = re.search(r'grep\s+["\']([^"\']+)["\']', command)
            if grep_match:
                placeholders['search_pattern'] = grep_match.group(1)
                placeholders['process_pattern'] = grep_match.group(1)
        
        if 'find' in command:
            find_match = re.search(r'find\s+(\S+)', command)
            if find_match:
                placeholders['search_directory'] = find_match.group(1)
        
        # Remplacement des placeholders
        filled_template = template
        for key, value in placeholders.items():
            filled_template = filled_template.replace(f'{{{key}}}', value)
        
        return filled_template
    
    def _generate_generic_script(self, command: str, filename: str) -> str:
        """Génère un script générique."""
        return f'''#!/usr/bin/env python3
"""
Script généré automatiquement pour simplifier une commande complexe.
Remplace: {command}
"""

import subprocess
import sys
import os
from pathlib import Path

def execute_command_safely():
    """Exécute la commande originale de manière sécurisée."""
    original_command = {repr(command)}
    
    try:
        # Décomposition et validation de la commande
        print(f"🔄 Exécution: {{original_command}}")
        
        # Exécution avec capture de sortie
        result = subprocess.run(
            original_command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300  # Timeout de 5 minutes
        )
        
        if result.returncode == 0:
            print("✅ Commande exécutée avec succès")
            if result.stdout:
                print("📤 Sortie:")
                print(result.stdout)
        else:
            print(f"⚠️ Commande terminée avec code {{result.returncode}}")
            if result.stderr:
                print("📤 Erreurs:")
                print(result.stderr)
        
        return result.returncode
        
    except subprocess.TimeoutExpired:
        print("❌ Timeout: Commande trop longue à exécuter")
        return 1
    except Exception as e:
        print(f"❌ Erreur d'exécution: {{e}}")
        return 1

def main():
    """Fonction principale."""
    try:
        return execute_command_safely()
    except KeyboardInterrupt:
        print("\\n⏹️ Interruption utilisateur")
        return 130
    except Exception as e:
        print(f"❌ Erreur inattendue: {{e}}")
        return 1

if __name__ == "__main__":
    exit(main())'''
    
    def create_script_file(self, analysis: CommandAnalysis) -> Path:
        """Crée le fichier script et retourne son chemin."""
        script_path = self.scripts_dir / analysis.suggested_filename
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(analysis.generated_script)
        
        # Rendre le script exécutable
        script_path.chmod(0o755)
        
        return script_path
    
    def simplify_command_interactive(self, command: str) -> Optional[Path]:
        """Interface interactive pour simplifier une commande."""
        analysis = self.analyze_command(command)
        
        print(f"🔍 Analyse de la commande: {command}")
        print(f"📊 Score de complexité: {analysis.complexity_score}")
        
        if not analysis.is_complex:
            print("✅ Commande suffisamment simple, aucune action nécessaire")
            return None
        
        print("⚠️ Commande complexe détectée!")
        print("📋 Raisons:")
        for reason in analysis.reasons:
            print(f"  • {reason}")
        
        print(f"💡 Fichier suggéré: {analysis.suggested_filename}")
        
        response = input("\\n🤔 Créer le script simplificateur? (o/N): ").strip().lower()
        if response in ['o', 'oui', 'y', 'yes']:
            script_path = self.create_script_file(analysis)
            print(f"✅ Script créé: {script_path}")
            print(f"🚀 Utilisation: python3 {script_path}")
            return script_path
        else:
            print("❌ Simplification annulée")
            return None

def main():
    """Interface en ligne de commande."""
    if len(sys.argv) < 2:
        print("Usage: python3 simplificateur_commandes.py 'commande à analyser'")
        print("Exemple: python3 simplificateur_commandes.py 'ps aux | grep python | awk \"{print $2}\" | xargs kill'")
        return 1
    
    command = ' '.join(sys.argv[1:])
    simplifier = CommandSimplifier()
    
    try:
        script_path = simplifier.simplify_command_interactive(command)
        return 0 if script_path else 1
    except KeyboardInterrupt:
        print("\\n⏹️ Interruption utilisateur")
        return 130
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return 1

if __name__ == "__main__":
    exit(main())