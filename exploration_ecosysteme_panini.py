#!/usr/bin/env python3
"""
EXPLORATION ÉCOSYSTÈME PANINI COMPLET
====================================

Analyse complète de tous les modules Panini pour comprendre l'ampleur
et les aspirations du projet global.
"""

import os
import subprocess
from pathlib import Path
import json

def explorer_ecosysteme_panini():
    """Explorer tous les modules de l'écosystème Panini"""
    
    print("🌟 EXPLORATION ÉCOSYSTÈME PANINI COMPLET")
    print("=" * 55)
    
    base_dir = Path.home() / "GitHub"
    
    # Identifier tous les modules Panini
    modules_panini = []
    
    for item in base_dir.iterdir():
        if item.is_dir() and ('panini' in item.name.lower() or item.name == 'OntoWave'):
            modules_panini.append(item)
    
    modules_panini.sort(key=lambda x: x.name)
    
    print(f"📋 MODULES DÉCOUVERTS: {len(modules_panini)}")
    for module in modules_panini:
        print(f"   • {module.name}")
    
    return modules_panini

def analyser_module(module_path):
    """Analyser un module spécifique"""
    
    print(f"\n📁 ANALYSE: {module_path.name}")
    print("=" * (10 + len(module_path.name)))
    
    analyse = {
        'nom': module_path.name,
        'chemin': str(module_path),
        'taille': 0,
        'fichiers_cles': [],
        'technologies': set(),
        'description': 'N/A',
        'statut': 'inconnu'
    }
    
    try:
        # Taille du module
        result = subprocess.run(['du', '-sh', str(module_path)], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            analyse['taille'] = result.stdout.split()[0]
        
        # Fichiers clés
        fichiers_cles = [
            'README.md', 'README.rst', 'ROADMAP.md', 
            'package.json', 'setup.py', 'pyproject.toml',
            'ORGANIZATION.md', 'PRODUCTION-READY-100.md'
        ]
        
        for fichier in fichiers_cles:
            fichier_path = module_path / fichier
            if fichier_path.exists():
                analyse['fichiers_cles'].append(fichier)
        
        # Technologies détectées
        tech_indicators = {
            'package.json': 'Node.js/TypeScript',
            'setup.py': 'Python',
            'pyproject.toml': 'Python Modern',
            'Cargo.toml': 'Rust',
            'go.mod': 'Go',
            'requirements.txt': 'Python',
            'tsconfig.json': 'TypeScript',
            'vite.config.ts': 'Vite/Frontend'
        }
        
        for indicator, tech in tech_indicators.items():
            if (module_path / indicator).exists():
                analyse['technologies'].add(tech)
        
        # Lire description depuis README
        readme_files = ['README.md', 'ORGANIZATION.md', 'ROADMAP.md']
        for readme in readme_files:
            readme_path = module_path / readme
            if readme_path.exists():
                try:
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        content = f.read()[:1000]  # Premier 1000 caractères
                        if content:
                            analyse['description'] = content
                            break
                except:
                    pass
        
        # Statut du projet
        if any(f in analyse['fichiers_cles'] for f in ['PRODUCTION-READY-100.md', 'NPM-PUBLICATION-READY.md']):
            analyse['statut'] = 'PRODUCTION'
        elif 'README.md' in analyse['fichiers_cles']:
            analyse['statut'] = 'DÉVELOPPEMENT'
        else:
            analyse['statut'] = 'ÉBAUCHE'
        
        # Affichage
        print(f"   📊 Taille: {analyse['taille']}")
        print(f"   🔧 Technologies: {', '.join(analyse['technologies'])}")
        print(f"   📋 Statut: {analyse['statut']}")
        print(f"   📄 Fichiers clés: {', '.join(analyse['fichiers_cles'])}")
        
        if analyse['description'] != 'N/A':
            desc_preview = analyse['description'][:200].replace('\n', ' ')
            print(f"   📝 Description: {desc_preview}...")
        
    except Exception as e:
        print(f"   ❌ Erreur analyse: {e}")
    
    return analyse

def detecter_architecture_globale(analyses):
    """Détecter l'architecture globale de l'écosystème"""
    
    print(f"\n🏗️ ARCHITECTURE ÉCOSYSTÈME PANINI")
    print("=" * 35)
    
    # Classification des modules
    categories = {
        'Core/Research': [],
        'Infrastructure': [],
        'Orchestration': [],
        'Applications': [],
        'Outils': []
    }
    
    for analyse in analyses:
        nom = analyse['nom']
        
        if 'research' in nom.lower() or nom == 'PaniniFS':
            categories['Core/Research'].append(analyse)
        elif any(keyword in nom.lower() for keyword in ['orchestrator', 'execution', 'cloud']):
            categories['Orchestration'].append(analyse)
        elif any(keyword in nom.lower() for keyword in ['semantic', 'reactive', 'engine']):
            categories['Infrastructure'].append(analyse)
        elif any(keyword in nom.lower() for keyword in ['gest', 'ontowave']):
            categories['Applications'].append(analyse)
        else:
            categories['Outils'].append(analyse)
    
    for category, modules in categories.items():
        if modules:
            print(f"\n📂 {category} ({len(modules)} modules)")
            for module in modules:
                statut_icon = {'PRODUCTION': '🚀', 'DÉVELOPPEMENT': '🔧', 'ÉBAUCHE': '📝'}.get(module['statut'], '❓')
                print(f"   {statut_icon} {module['nom']} ({module['taille']}) - {', '.join(module['technologies'])}")
    
    return categories

def identifier_dependances(analyses):
    """Identifier les dépendances entre modules"""
    
    print(f"\n🔗 ANALYSE DÉPENDANCES")
    print("=" * 25)
    
    # Patterns de dépendances possibles
    dependances = []
    
    for analyse in analyses:
        module_path = Path(analyse['chemin'])
        
        # Chercher références à autres modules Panini
        for autre in analyses:
            if autre['nom'] != analyse['nom']:
                # Chercher dans package.json, imports, etc.
                try:
                    # Package.json
                    package_json = module_path / 'package.json'
                    if package_json.exists():
                        with open(package_json, 'r') as f:
                            content = f.read()
                            if autre['nom'].lower() in content.lower():
                                dependances.append((analyse['nom'], autre['nom'], 'package.json'))
                    
                    # README/docs
                    for doc_file in ['README.md', 'ORGANIZATION.md']:
                        doc_path = module_path / doc_file
                        if doc_path.exists():
                            with open(doc_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                if autre['nom'] in content:
                                    dependances.append((analyse['nom'], autre['nom'], doc_file))
                                    break
                except:
                    pass
    
    if dependances:
        print("🔗 Dépendances détectées:")
        for source, target, context in dependances:
            print(f"   • {source} → {target} (via {context})")
    else:
        print("ℹ️ Aucune dépendance explicite détectée (modules possiblement autonomes)")
    
    return dependances

def generer_rapport_ecosysteme(analyses, categories, dependances):
    """Générer un rapport complet de l'écosystème"""
    
    print(f"\n📊 RAPPORT ÉCOSYSTÈME PANINI")
    print("=" * 30)
    
    # Statistiques globales
    total_modules = len(analyses)
    modules_production = len([a for a in analyses if a['statut'] == 'PRODUCTION'])
    modules_dev = len([a for a in analyses if a['statut'] == 'DÉVELOPPEMENT'])
    
    technologies = set()
    for analyse in analyses:
        technologies.update(analyse['technologies'])
    
    print(f"📈 STATISTIQUES:")
    print(f"   • Total modules: {total_modules}")
    print(f"   • En production: {modules_production}")
    print(f"   • En développement: {modules_dev}")
    print(f"   • Technologies: {', '.join(technologies)}")
    
    # Modules prioritaires
    print(f"\n🎯 MODULES PRIORITAIRES:")
    prioritaires = [a for a in analyses if a['statut'] == 'PRODUCTION'] + \
                  [a for a in analyses if 'Core' in str(categories)]
    
    for module in prioritaires[:5]:  # Top 5
        print(f"   🌟 {module['nom']} - {module['statut']}")
    
    # Recommandations
    print(f"\n💡 RECOMMANDATIONS:")
    print(f"   1. Prioriser modules PRODUCTION pour comprendre l'état de l'art")
    print(f"   2. Examiner PaniniFS-Research comme base théorique")
    print(f"   3. Étudier OntoWave comme application concrète")
    print(f"   4. Comprendre l'architecture d'orchestration")
    
    return {
        'total_modules': total_modules,
        'analyses': analyses,
        'categories': categories,
        'dependances': dependances,
        'technologies': technologies
    }

def main():
    """Exploration complète de l'écosystème"""
    
    # Phase 1: Découverte
    modules = explorer_ecosysteme_panini()
    
    # Phase 2: Analyse détaillée
    analyses = []
    for module in modules:
        analyse = analyser_module(module)
        analyses.append(analyse)
    
    # Phase 3: Architecture globale
    categories = detecter_architecture_globale(analyses)
    
    # Phase 4: Dépendances
    dependances = identifier_dependances(analyses)
    
    # Phase 5: Rapport final
    rapport = generer_rapport_ecosysteme(analyses, categories, dependances)
    
    print(f"\n✨ EXPLORATION TERMINÉE")
    print(f"Écosystème Panini: {rapport['total_modules']} modules analysés")
    print(f"Prochaine étape: Exploration approfondie des modules clés")

if __name__ == "__main__":
    main()