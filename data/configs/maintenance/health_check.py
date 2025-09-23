#!/usr/bin/env python3
"""
🏥 HEALTH CHECK - Vérification Santé Projet
Utilitaire de diagnostic complet du workspace PaniniFS-Research
"""

import os
import json
from pathlib import Path
from datetime import datetime

def check_critical_structure():
    """Vérifier structure critique du projet"""
    
    print("🏥 DIAGNOSTIC SANTÉ PROJET")
    print("=" * 50)
    
    # Dossiers critiques requis
    critical_dirs = [
        ("copilotage", "🤖 Coordination agents - CRITIQUE"),
        ("production", "📦 Documents finaux"),
        ("research", "📚 Recherche active"),
        ("data", "📊 Données et références"),
        ("publications", "📖 Articles et livres"),
        ("tools", "🔧 Scripts utilitaires"),
        ("archives", "🗄️ Historique et backups")
    ]
    
    print("📁 VÉRIFICATION STRUCTURE :")
    structure_ok = True
    
    for dir_name, description in critical_dirs:
        if Path(dir_name).exists():
            print(f"   ✅ {dir_name}/ - {description}")
        else:
            print(f"   ❌ {dir_name}/ - MANQUANT - {description}")
            structure_ok = False
    
    return structure_ok

def check_copilotage_integrity():
    """Vérifier intégrité du dossier copilotage"""
    
    print(f"\n🤖 VÉRIFICATION COPILOTAGE :")
    
    copilotage_files = [
        ("regles/REGLES_COPILOTAGE_v0.0.1.md", "📋 Règles principales"),
        ("protocols/workflow_standard.md", "🔄 Workflow standard"),
        ("protocols/handoff_procedures.md", "🤝 Procédures transfert"),
        ("documentation/project_overview.md", "📖 Vue d'ensemble"),
        ("shared/status_tracking.md", "📊 Suivi d'état"),
        ("README.md", "📄 Documentation principale")
    ]
    
    copilotage_ok = True
    copilotage_path = Path("copilotage")
    
    if not copilotage_path.exists():
        print("   ❌ CRITIQUE : Dossier /copilotage/ MANQUANT")
        return False
    
    for file_path, description in copilotage_files:
        full_path = copilotage_path / file_path
        if full_path.exists():
            print(f"   ✅ {file_path} - {description}")
        else:
            print(f"   ⚠️ {file_path} - MANQUANT - {description}")
            copilotage_ok = False
    
    return copilotage_ok

def check_production_files():
    """Vérifier fichiers de production essentiels"""
    
    print(f"\n📦 VÉRIFICATION PRODUCTION :")
    
    production_files = [
        ("documents/dhatu_complete_final.pdf", "📄 Document reMarkable"),
        ("documents/dhatu_complete_final.html", "🌐 Source HTML"),
        ("generators/generate_dhatu_unicode_final.py", "🐍 Générateur Unicode")
    ]
    
    production_ok = True
    production_path = Path("production")
    
    if not production_path.exists():
        print("   ❌ Dossier /production/ manquant")
        return False
    
    for file_path, description in production_files:
        full_path = production_path / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"   ✅ {file_path} - {description} ({size} bytes)")
        else:
            print(f"   ❌ {file_path} - MANQUANT - {description}")
            production_ok = False
    
    return production_ok

def check_workspace_cleanliness():
    """Vérifier propreté du workspace"""
    
    print(f"\n🧹 VÉRIFICATION PROPRETÉ :")
    
    # Fichiers temporaires à éviter
    temp_patterns = [
        "*.tmp", "*.temp", "*~", ".DS_Store",
        "*.pyc", "__pycache__", "node_modules",
        "*.log", "test-results", "playwright-report"
    ]
    
    # Compter fichiers racine
    root_files = [f for f in Path(".").iterdir() if f.is_file()]
    root_dirs = [d for d in Path(".").iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    print(f"   📄 Fichiers racine : {len(root_files)}")
    print(f"   📁 Dossiers racine : {len(root_dirs)}")
    
    if len(root_files) <= 5:
        print("   ✅ Racine propre (≤5 fichiers)")
    else:
        print("   ⚠️ Racine encombrée (>5 fichiers)")
        for f in root_files:
            print(f"      📄 {f.name}")
    
    return len(root_files) <= 5

def generate_health_report():
    """Générer rapport de santé complet"""
    
    print(f"\n📊 GÉNÉRATION RAPPORT :")
    
    # Collecter métriques
    structure_ok = check_critical_structure()
    copilotage_ok = check_copilotage_integrity()
    production_ok = check_production_files()
    workspace_clean = check_workspace_cleanliness()
    
    # Score global
    checks = [structure_ok, copilotage_ok, production_ok, workspace_clean]
    score = sum(checks) / len(checks) * 100
    
    # Statut global
    if score >= 90:
        status = "🟢 EXCELLENT"
    elif score >= 75:
        status = "🟡 BON"
    elif score >= 50:
        status = "🟠 MOYEN"
    else:
        status = "🔴 CRITIQUE"
    
    # Rapport détaillé
    report = f"""# 🏥 RAPPORT SANTÉ PROJET - {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 📊 SCORE GLOBAL : {score:.1f}% - {status}

### ✅ VÉRIFICATIONS
- 📁 Structure critique : {'✅' if structure_ok else '❌'}
- 🤖 Copilotage intégrité : {'✅' if copilotage_ok else '❌'}
- 📦 Fichiers production : {'✅' if production_ok else '❌'}
- 🧹 Workspace propre : {'✅' if workspace_clean else '❌'}

### 🎯 RECOMMANDATIONS
{'✅ Projet en excellente santé - Aucune action requise' if score >= 90 else ''}
{'⚠️ Quelques améliorations possibles - Vérifier détails ci-dessus' if 75 <= score < 90 else ''}
{'🔧 Maintenance nécessaire - Corriger problèmes identifiés' if 50 <= score < 75 else ''}
{'🚨 Intervention urgente - Structure compromise' if score < 50 else ''}

### 📁 STRUCTURE ATTENDUE
```
PaniniFS-Research/
├── copilotage/          # 🤖 Coordination agents
├── production/          # 📦 Documents finaux  
├── research/           # 📚 Recherche active
├── data/               # 📊 Données références
├── publications/       # 📖 Articles et livres
├── tools/              # 🔧 Scripts utilitaires
└── archives/           # 🗄️ Historique backups
```

---
*Diagnostic automatique - Copilotage Health Check*
"""
    
    # Sauvegarder rapport
    report_path = Path("copilotage/maintenance/last_health_report.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"   ✅ Rapport sauvé : {report_path}")
    print(f"   📊 Score global : {score:.1f}% - {status}")
    
    return score, status

def main():
    """Diagnostic complet du projet"""
    
    os.chdir(Path(__file__).parent.parent.parent)  # Retour racine
    
    print("🏥 HEALTH CHECK PANINI-FS RESEARCH")
    print("🎯 Diagnostic complet du workspace")
    print()
    
    # Exécuter diagnostic
    score, status = generate_health_report()
    
    print(f"\n🎉 DIAGNOSTIC TERMINÉ")
    print(f"   📊 Score : {score:.1f}%")
    print(f"   🎯 Statut : {status}")
    print(f"   📄 Rapport : copilotage/maintenance/last_health_report.md")
    
    # Code retour pour scripts
    if score >= 75:
        return 0  # Succès
    elif score >= 50:
        return 1  # Avertissement
    else:
        return 2  # Erreur critique

if __name__ == "__main__":
    exit(main())
