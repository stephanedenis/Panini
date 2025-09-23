#!/usr/bin/env python3
"""
Simplificateur Global pour tous les modules Panini
Interface unifiée pour appliquer la directive de simplification dans tout l'écosystème.
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire copilotage au path Python
copilotage_dir = Path(__file__).parent.parent
sys.path.insert(0, str(copilotage_dir))

try:
    from utilities.simplificateur_commandes import CommandSimplifier
except ImportError:
    # Fallback si l'import ne fonctionne pas
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from simplificateur_commandes import CommandSimplifier

class PaniniGlobalSimplifier:
    """Simplificateur global pour tous les modules Panini."""
    
    def __init__(self):
        """Initialise le simplificateur global."""
        self.base_simplifier = CommandSimplifier()
        self.workspace_root = self._find_workspace_root()
        self.module_paths = self._discover_panini_modules()
    
    def _find_workspace_root(self):
        """Trouve la racine du workspace PaniniFS-Research."""
        current = Path(__file__).parent
        while current.parent != current:
            if (current / "copilotage").exists() and (current / "panini").exists():
                return current
            current = current.parent
        return Path.cwd()
    
    def _discover_panini_modules(self):
        """Découvre tous les modules Panini dans le workspace."""
        modules = {
            'tech': self.workspace_root / 'tech',
            'panini': self.workspace_root / 'panini',
            'docs': self.workspace_root / 'docs',
            'copilotage': self.workspace_root / 'copilotage',
        }
        
        # Ajouter les sous-modules découverts dynamiquement
        for module_dir in ['tech', 'panini']:
            base_path = self.workspace_root / module_dir
            if base_path.exists():
                for subdir in base_path.iterdir():
                    if subdir.is_dir() and not subdir.name.startswith('.'):
                        modules[f"{module_dir}/{subdir.name}"] = subdir
        
        return {k: v for k, v in modules.items() if v.exists()}
    
    def simplify_for_module(self, command: str, target_module: str = None):
        """Simplifie une commande pour un module spécifique."""
        analysis = self.base_simplifier.analyze_command(command)
        
        if not analysis.is_complex:
            print(f"✅ Commande suffisamment simple: {command}")
            return None
        
        # Adapter le nom de fichier selon le module
        if target_module:
            module_prefix = target_module.replace('/', '_')
            filename_parts = analysis.suggested_filename.split('.')
            analysis.suggested_filename = f"{module_prefix}_{filename_parts[0]}.{filename_parts[1]}"
        
        # Déterminer le répertoire de destination
        if target_module and target_module in self.module_paths:
            scripts_dir = self.module_paths[target_module] / "scripts_generes"
        else:
            scripts_dir = self.workspace_root / "scripts_generes"
        
        scripts_dir.mkdir(exist_ok=True)
        
        # Créer le script dans le bon répertoire
        script_path = scripts_dir / analysis.suggested_filename
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(self._enhance_script_for_panini(analysis.generated_script, target_module))
        
        script_path.chmod(0o755)
        
        return script_path
    
    def _enhance_script_for_panini(self, base_script: str, module: str = None):
        """Améliore le script généré avec les spécificités Panini."""
        header = f'''#!/usr/bin/env python3
"""
Script généré par PaniniFS Global Simplifier
Module: {module or 'global'}
Suit la directive de simplification des règles de copilotage v0.0.2
"""

import sys
from pathlib import Path

# Configuration Panini
WORKSPACE_ROOT = Path(__file__).parent.parent
if "{module or 'global'}" != "global":
    MODULE_ROOT = WORKSPACE_ROOT / "{module or 'global'}"
else:
    MODULE_ROOT = WORKSPACE_ROOT

# Ajouter les paths Panini
sys.path.insert(0, str(WORKSPACE_ROOT))
sys.path.insert(0, str(WORKSPACE_ROOT / "copilotage"))

'''
        
        # Remplacer le header existant
        lines = base_script.split('\n')
        start_main = -1
        for i, line in enumerate(lines):
            if 'def main():' in line or 'def execute_command_safely():' in line:
                start_main = i
                break
        
        if start_main > 0:
            enhanced_script = header + '\n'.join(lines[start_main:])
        else:
            enhanced_script = header + base_script
        
        return enhanced_script
    
    def apply_to_all_modules(self, command: str):
        """Applique la simplification à tous les modules découverts."""
        print(f"🔄 Application de la simplification à tous les modules Panini")
        print(f"📋 Commande à simplifier: {command}")
        
        results = {}
        
        for module_name, module_path in self.module_paths.items():
            print(f"\\n📁 Module: {module_name}")
            script_path = self.simplify_for_module(command, module_name)
            
            if script_path:
                print(f"  ✅ Script créé: {script_path}")
                results[module_name] = script_path
            else:
                print(f"  ℹ️ Simplification non nécessaire")
                results[module_name] = None
        
        return results
    
    def validate_installation(self):
        """Valide que la simplification est bien installée partout."""
        print("🔍 Validation de l'installation de la directive de simplification")
        
        # Vérifier les règles de copilotage
        regles_file = self.workspace_root / "copilotage/regles/REGLES_COPILOTAGE_v0.0.1.md"
        if regles_file.exists():
            content = regles_file.read_text()
            if "DIRECTIVE SIMPLIFICATION OBLIGATOIRE" in content:
                print("  ✅ Règles de copilotage mises à jour")
            else:
                print("  ❌ Directive manquante dans les règles")
        
        # Vérifier VS Code settings
        vscode_settings = self.workspace_root / ".vscode/settings.json"
        if vscode_settings.exists():
            print("  ✅ Configuration VS Code présente")
        else:
            print("  ⚠️ Configuration VS Code manquante")
        
        # Vérifier les utilities
        simplificateur = self.workspace_root / "copilotage/utilities/simplificateur_commandes.py"
        if simplificateur.exists():
            print("  ✅ Simplificateur global installé")
        else:
            print("  ❌ Simplificateur global manquant")
        
        # Compter les modules découverts
        print(f"  📊 Modules Panini découverts: {len(self.module_paths)}")
        for module in self.module_paths:
            print(f"    - {module}")

def main():
    """Interface en ligne de commande du simplificateur global."""
    if len(sys.argv) < 2:
        print("🎯 PaniniFS Global Simplifier")
        print("Usage:")
        print("  python3 panini_global_simplifier.py 'commande à simplifier'")
        print("  python3 panini_global_simplifier.py --validate")
        print("  python3 panini_global_simplifier.py --apply-all 'commande'")
        print()
        print("Exemples:")
        print("  python3 panini_global_simplifier.py 'ps aux | grep python | awk \"{print $2}\" | xargs kill'")
        print("  python3 panini_global_simplifier.py --validate")
        return 1
    
    simplifier = PaniniGlobalSimplifier()
    
    if sys.argv[1] == "--validate":
        simplifier.validate_installation()
        return 0
    elif sys.argv[1] == "--apply-all" and len(sys.argv) > 2:
        command = ' '.join(sys.argv[2:])
        results = simplifier.apply_to_all_modules(command)
        
        print(f"\\n📊 Résumé:")
        created_count = sum(1 for r in results.values() if r is not None)
        print(f"  ✅ Scripts créés: {created_count}")
        print(f"  📁 Modules traités: {len(results)}")
        
        return 0
    else:
        command = ' '.join(sys.argv[1:])
        script_path = simplifier.simplify_for_module(command)
        
        if script_path:
            print(f"✅ Script créé: {script_path}")
            print(f"🚀 Utilisation: python3 {script_path}")
            return 0
        else:
            return 1

if __name__ == "__main__":
    exit(main())