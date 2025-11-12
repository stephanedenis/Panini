#!/usr/bin/env python3
"""
Script de validation de la cohérence inter-modules - Projet Panini

Vérifie que chaque module suit la structure standard définie dans ARCHITECTURE_STANDARD.md

Date: 2025-11-12
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Set
import json

class ModuleValidator:
    """Validateur de structure des modules"""
    
    def __init__(self, root_path: Path):
        self.root = root_path
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.successes: List[str] = []
        
    def validate_module_structure(self, module_path: Path, module_name: str) -> Dict:
        """Valide la structure d'un module"""
        results = {
            'name': module_name,
            'path': str(module_path),
            'has_readme': False,
            'has_docs': False,
            'has_src': False,
            'has_tests': False,
            'issues': []
        }
        
        # Vérifier README.md
        readme = module_path / 'README.md'
        if readme.exists():
            results['has_readme'] = True
            self.successes.append(f"✅ {module_name}: README.md présent")
        else:
            results['issues'].append('Manque README.md')
            self.warnings.append(f"⚠️  {module_name}: Manque README.md")
        
        # Vérifier docs/
        docs_dir = module_path / 'docs'
        if docs_dir.exists() and docs_dir.is_dir():
            results['has_docs'] = True
            self.successes.append(f"✅ {module_name}: docs/ présent")
        else:
            results['issues'].append('Manque docs/')
            self.warnings.append(f"⚠️  {module_name}: Manque docs/")
        
        # Vérifier src/
        src_dir = module_path / 'src'
        if src_dir.exists() and src_dir.is_dir():
            results['has_src'] = True
            self.successes.append(f"✅ {module_name}: src/ présent")
        
        # Vérifier tests/
        tests_dir = module_path / 'tests'
        if tests_dir.exists() and tests_dir.is_dir():
            results['has_tests'] = True
            self.successes.append(f"✅ {module_name}: tests/ présent")
        
        return results
    
    def find_duplicate_files(self, pattern: str) -> Dict[str, List[Path]]:
        """Trouve les fichiers dupliqués par nom"""
        files_by_name: Dict[str, List[Path]] = {}
        
        for file_path in self.root.rglob(pattern):
            # Ignorer les archives
            if 'archive' in str(file_path).lower() or 'backup' in str(file_path).lower():
                continue
            
            name = file_path.name
            if name not in files_by_name:
                files_by_name[name] = []
            files_by_name[name].append(file_path)
        
        # Filtrer pour garder seulement les doublons
        duplicates = {name: paths for name, paths in files_by_name.items() if len(paths) > 1}
        return duplicates
    
    def validate_notebooks_location(self) -> Dict[str, List[Path]]:
        """Vérifie que les notebooks sont aux bons endroits"""
        issues = {
            'misplaced_notebooks': [],
            'colab_notebooks': [],
            'research_notebooks': []
        }
        
        # Notebooks Colab (doivent être dans /notebooks)
        notebooks_dir = self.root / 'notebooks'
        if notebooks_dir.exists():
            for nb in notebooks_dir.glob('*.ipynb'):
                issues['colab_notebooks'].append(nb)
        
        # Notebooks recherche (doivent être dans /research)
        research_dir = self.root / 'research' / 'notebooks'
        if research_dir.exists():
            for nb in research_dir.glob('*.ipynb'):
                issues['research_notebooks'].append(nb)
        
        # Notebooks mal placés (dans modules/ par exemple)
        for nb in self.root.rglob('*.ipynb'):
            if 'archive' in str(nb) or 'backup' in str(nb):
                continue
            if notebooks_dir not in nb.parents and research_dir not in nb.parents:
                issues['misplaced_notebooks'].append(nb)
                self.errors.append(f"❌ Notebook mal placé: {nb.relative_to(self.root)}")
        
        return issues
    
    def validate_copilotage(self) -> Dict:
        """Valide que copilotage/ contient uniquement du contexte agents"""
        results = {
            'is_valid': True,
            'documentation_files': [],
            'corpus_files': []
        }
        
        copilotage_dir = self.root / 'copilotage'
        if not copilotage_dir.exists():
            self.errors.append("❌ Dossier copilotage/ manquant!")
            results['is_valid'] = False
            return results
        
        # Vérifier qu'il n'y a pas de docs/ ou documentation/
        if (copilotage_dir / 'docs').exists():
            self.errors.append("❌ copilotage/docs/ ne devrait pas exister!")
            results['is_valid'] = False
        
        if (copilotage_dir / 'documentation').exists():
            self.errors.append("❌ copilotage/documentation/ ne devrait pas exister!")
            results['is_valid'] = False
        
        # Chercher des fichiers de documentation projet
        for md_file in copilotage_dir.rglob('*.md'):
            if 'journal' not in str(md_file):  # Les journaux sont OK
                relative_path = md_file.relative_to(copilotage_dir)
                # Vérifier si c'est un fichier de contexte agent ou documentation projet
                content_preview = md_file.read_text(encoding='utf-8')[:500].lower()
                if any(kw in content_preview for kw in ['projet', 'guide', 'manuel', 'documentation']):
                    results['documentation_files'].append(md_file)
                    self.warnings.append(f"⚠️  Possible doc projet dans copilotage/: {relative_path}")
        
        return results
    
    def generate_report(self) -> str:
        """Génère un rapport de validation"""
        report = []
        report.append("=" * 80)
        report.append("📋 RAPPORT DE VALIDATION - COHÉRENCE INTER-MODULES")
        report.append("=" * 80)
        report.append("")
        
        # Succès
        if self.successes:
            report.append(f"✅ SUCCÈS ({len(self.successes)}):")
            for success in self.successes[:10]:  # Limiter à 10
                report.append(f"   {success}")
            if len(self.successes) > 10:
                report.append(f"   ... et {len(self.successes) - 10} autres")
            report.append("")
        
        # Avertissements
        if self.warnings:
            report.append(f"⚠️  AVERTISSEMENTS ({len(self.warnings)}):")
            for warning in self.warnings:
                report.append(f"   {warning}")
            report.append("")
        
        # Erreurs
        if self.errors:
            report.append(f"❌ ERREURS ({len(self.errors)}):")
            for error in self.errors:
                report.append(f"   {error}")
            report.append("")
        
        # Score global
        total_checks = len(self.successes) + len(self.warnings) + len(self.errors)
        score = len(self.successes) / total_checks * 100 if total_checks > 0 else 0
        report.append("=" * 80)
        report.append(f"📊 SCORE DE COHÉRENCE: {score:.1f}%")
        report.append("=" * 80)
        
        return "\n".join(report)


def main():
    """Point d'entrée principal"""
    root = Path(__file__).parent.parent
    validator = ModuleValidator(root)
    
    print("🔍 Validation de la structure du projet Panini...")
    print()
    
    # 1. Valider les modules principaux
    print("📦 Validation des modules...")
    modules_dir = root / 'modules'
    if modules_dir.exists():
        for module_path in modules_dir.iterdir():
            if module_path.is_dir() and not module_path.name.startswith('.'):
                validator.validate_module_structure(module_path, f"modules/{module_path.name}")
    
    # 2. Valider le projet parent
    print("📦 Validation du projet parent...")
    validator.validate_module_structure(root, "Panini (parent)")
    
    # 3. Vérifier les doublons
    print("\n🔍 Recherche de fichiers dupliqués...")
    duplicates = validator.find_duplicate_files("*.md")
    if duplicates:
        print(f"⚠️  {len(duplicates)} fichiers dupliqués trouvés:")
        for name, paths in list(duplicates.items())[:5]:  # Limiter à 5
            print(f"   - {name}: {len(paths)} copies")
            validator.warnings.append(f"Fichier dupliqué: {name} ({len(paths)} copies)")
    
    # 4. Valider emplacement notebooks
    print("\n📓 Validation emplacement notebooks...")
    nb_issues = validator.validate_notebooks_location()
    if nb_issues['misplaced_notebooks']:
        print(f"❌ {len(nb_issues['misplaced_notebooks'])} notebooks mal placés")
    else:
        print("✅ Tous les notebooks sont aux bons emplacements")
        validator.successes.append("Notebooks bien organisés")
    
    # 5. Valider copilotage
    print("\n🤖 Validation copilotage/...")
    copilotage_results = validator.validate_copilotage()
    if copilotage_results['is_valid']:
        print("✅ copilotage/ est correctement structuré")
        validator.successes.append("copilotage/ correctement structuré")
    
    # Générer le rapport
    print("\n")
    report = validator.generate_report()
    print(report)
    
    # Sauvegarder le rapport
    report_file = root / 'data' / f'validation_coherence_{Path(__file__).stem}.txt'
    report_file.parent.mkdir(exist_ok=True)
    report_file.write_text(report, encoding='utf-8')
    print(f"\n📄 Rapport sauvegardé: {report_file.relative_to(root)}")
    
    # Code de sortie
    if validator.errors:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
