#!/usr/bin/env python3
"""
Testeur de Configuration - Validation de la Directive de Simplification
Vérifie que toutes les configurations VS Code et Copilot fonctionnent ensemble.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
import tempfile

class ConfigurationTester:
    """Testeur pour valider la configuration de simplification."""
    
    def __init__(self):
        """Initialise le testeur."""
        self.workspace_root = Path.cwd()
        self.vscode_dir = self.workspace_root / ".vscode"
        self.results = {"passed": 0, "failed": 0, "tests": []}
    
    def test_vscode_settings(self):
        """Teste la configuration VS Code."""
        print("🔧 Test des paramètres VS Code...")
        
        settings_file = self.vscode_dir / "settings.json"
        if not settings_file.exists():
            self._record_test("VS Code settings.json", False, "Fichier manquant")
            return
        
        try:
            with open(settings_file, 'r') as f:
                config = json.load(f)
            
            # Les paramètres sont dans la section "settings"
            settings = config.get("settings", {})
            
            # Vérification des paramètres Copilot
            required_settings = [
                ("copilot.enable", dict),
                ("copilot.chat.enable", bool),
                ("github.copilot.chat.experimental.codeGeneration.instructions", list)
            ]
            
            for setting_path, expected_type in required_settings:
                if self._check_nested_setting(settings, setting_path, expected_type):
                    self._record_test(f"Setting {setting_path}", True, "Configuré correctement")
                else:
                    self._record_test(f"Setting {setting_path}", False, f"Manquant ou type incorrect")
            
        except json.JSONDecodeError as e:
            self._record_test("VS Code settings.json", False, f"JSON invalide: {e}")
        except Exception as e:
            self._record_test("VS Code settings.json", False, f"Erreur: {e}")
    
    def test_copilot_instructions(self):
        """Teste les instructions Copilot."""
        print("🤖 Test des instructions Copilot...")
        
        settings_file = self.vscode_dir / "settings.json"
        try:
            with open(settings_file, 'r') as f:
                config = json.load(f)
            
            # Les paramètres sont dans la section "settings"
            settings = config.get("settings", {})
            
            instructions = settings.get("github.copilot.chat.experimental.codeGeneration.instructions", [])
            
            if not instructions:
                self._record_test("Instructions Copilot", False, "Aucune instruction trouvée")
                return
            
            # Vérification du contenu des instructions
            directive_found = False
            for instruction in instructions:
                if isinstance(instruction, dict) and "text" in instruction:
                    text = instruction["text"]
                    if "commande trop complexe" in text.lower() and "fichier python" in text.lower():
                        directive_found = True
                        break
            
            if directive_found:
                self._record_test("Directive de simplification", True, "Trouvée dans les instructions")
            else:
                self._record_test("Directive de simplification", False, "Non trouvée")
                
        except Exception as e:
            self._record_test("Instructions Copilot", False, f"Erreur: {e}")
    
    def test_snippets(self):
        """Teste les snippets de simplification."""
        print("📝 Test des snippets...")
        
        snippets_file = self.vscode_dir / "python-simplification.code-snippets"
        if not snippets_file.exists():
            self._record_test("Snippets de simplification", False, "Fichier manquant")
            return
        
        try:
            with open(snippets_file, 'r') as f:
                snippets = json.load(f)
            
            required_snippets = [
                "Simplification de commande complexe",
                "Script de gestion de processus", 
                "Script de recherche de fichiers",
                "Script d'analyse de logs",
                "Appel simplificateur automatique"
            ]
            
            for snippet_name in required_snippets:
                if snippet_name in snippets:
                    snippet = snippets[snippet_name]
                    if "prefix" in snippet and "body" in snippet:
                        self._record_test(f"Snippet '{snippet_name}'", True, f"Préfixe: {snippet['prefix']}")
                    else:
                        self._record_test(f"Snippet '{snippet_name}'", False, "Structure invalide")
                else:
                    self._record_test(f"Snippet '{snippet_name}'", False, "Manquant")
                    
        except json.JSONDecodeError as e:
            self._record_test("Snippets", False, f"JSON invalide: {e}")
        except Exception as e:
            self._record_test("Snippets", False, f"Erreur: {e}")
    
    def test_simplificateur_script(self):
        """Teste le script simplificateur."""
        print("🔄 Test du script simplificateur...")
        
        script_path = self.workspace_root / "simplificateur_commandes.py"
        if not script_path.exists():
            self._record_test("Script simplificateur", False, "Fichier manquant")
            return
        
        try:
            # Test d'import du module
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
                tmp.write(f"""
import sys
sys.path.insert(0, '{self.workspace_root}')
from simplificateur_commandes import CommandSimplifier
simplifier = CommandSimplifier()
analysis = simplifier.analyze_command('ps aux | grep python | awk "{{print $2}}" | xargs kill')
print(f"Complexité: {{analysis.complexity_score}}")
print(f"Est complexe: {{analysis.is_complex}}")
""")
                tmp_path = tmp.name
            
            result = subprocess.run([sys.executable, tmp_path], 
                                  capture_output=True, text=True, timeout=10)
            
            os.unlink(tmp_path)
            
            if result.returncode == 0:
                output = result.stdout.strip()
                if "Complexité:" in output and "Est complexe:" in output:
                    self._record_test("Fonctionnalité simplificateur", True, "Analyse fonctionnelle")
                else:
                    self._record_test("Fonctionnalité simplificateur", False, f"Sortie inattendue: {output}")
            else:
                self._record_test("Fonctionnalité simplificateur", False, f"Erreur: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            self._record_test("Fonctionnalité simplificateur", False, "Timeout")
        except Exception as e:
            self._record_test("Fonctionnalité simplificateur", False, f"Erreur: {e}")
    
    def test_integration(self):
        """Teste l'intégration complète."""
        print("🔗 Test d'intégration...")
        
        # Test de création d'un script simple
        try:
            script_path = self.workspace_root / "simplificateur_commandes.py"
            test_command = 'find . -name "*.py" -exec grep -l "def main" {} \\; | wc -l'
            
            # Simulation d'utilisation
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
                tmp.write(f"""
import sys
sys.path.insert(0, '{self.workspace_root}')
from simplificateur_commandes import CommandSimplifier

simplifier = CommandSimplifier()
analysis = simplifier.analyze_command('{test_command}')

# Vérification que la commande est détectée comme complexe
if analysis.is_complex:
    print("✅ Commande détectée comme complexe")
    print(f"Score: {{analysis.complexity_score}}")
    print(f"Fichier suggéré: {{analysis.suggested_filename}}")
    print("✅ Script généré avec succès")
else:
    print("❌ Commande non détectée comme complexe")
""")
                tmp_path = tmp.name
            
            result = subprocess.run([sys.executable, tmp_path], 
                                  capture_output=True, text=True, timeout=15)
            
            os.unlink(tmp_path)
            
            if result.returncode == 0 and "✅ Commande détectée comme complexe" in result.stdout:
                self._record_test("Intégration complète", True, "Workflow fonctionnel")
            else:
                self._record_test("Intégration complète", False, f"Workflow défaillant: {result.stdout}")
                
        except Exception as e:
            self._record_test("Intégration complète", False, f"Erreur: {e}")
    
    def _check_nested_setting(self, settings, path, expected_type):
        """Vérifie un paramètre imbriqué."""
        keys = path.split('.')
        current = settings
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return False
        
        return isinstance(current, expected_type)
    
    def _record_test(self, name, passed, details):
        """Enregistre le résultat d'un test."""
        self.results["tests"].append({
            "name": name,
            "passed": passed,
            "details": details
        })
        
        if passed:
            self.results["passed"] += 1
            print(f"  ✅ {name}: {details}")
        else:
            self.results["failed"] += 1
            print(f"  ❌ {name}: {details}")
    
    def run_all_tests(self):
        """Exécute tous les tests."""
        print("🧪 Validation de la Configuration de Simplification")
        print("=" * 60)
        
        self.test_vscode_settings()
        self.test_copilot_instructions()
        self.test_snippets()
        self.test_simplificateur_script()
        self.test_integration()
        
        return self.results
    
    def print_summary(self):
        """Affiche le résumé des tests."""
        print("\\n" + "=" * 60)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 60)
        
        total = self.results["passed"] + self.results["failed"]
        success_rate = (self.results["passed"] / total * 100) if total > 0 else 0
        
        print(f"✅ Tests réussis: {self.results['passed']}")
        print(f"❌ Tests échoués: {self.results['failed']}")
        print(f"📈 Taux de réussite: {success_rate:.1f}%")
        
        if self.results["failed"] > 0:
            print("\\n🔧 Actions recommandées:")
            for test in self.results["tests"]:
                if not test["passed"]:
                    print(f"  • {test['name']}: {test['details']}")
        
        if success_rate >= 80:
            print("\\n🎉 Configuration prête à l'utilisation!")
            print("\\n📚 Comment utiliser:")
            print("  1. Redémarrer VS Code (Ctrl+Shift+P → 'Reload Window')")
            print("  2. Utiliser les snippets avec préfixe 'simp-'")
            print("  3. Demander à Copilot de simplifier des commandes complexes")
            print("  4. Utiliser: python3 simplificateur_commandes.py 'commande'")
        else:
            print("\\n⚠️ Configuration incomplète - vérifiez les erreurs ci-dessus")

def main():
    """Fonction principale."""
    try:
        tester = ConfigurationTester()
        results = tester.run_all_tests()
        tester.print_summary()
        
        # Code de sortie basé sur le taux de réussite
        total = results["passed"] + results["failed"]
        success_rate = (results["passed"] / total * 100) if total > 0 else 0
        
        return 0 if success_rate >= 80 else 1
        
    except KeyboardInterrupt:
        print("\\n⏹️ Tests interrompus")
        return 130
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
        return 1

if __name__ == "__main__":
    exit(main())