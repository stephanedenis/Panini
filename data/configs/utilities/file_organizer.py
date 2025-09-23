#!/usr/bin/env python3
"""
📁 FILE ORGANIZER - Organisateur de Fichiers
Utilitaire pour maintenir l'organisation et la conformité du workspace
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

def analyze_workspace_structure():
    """Analyser structure actuelle du workspace"""
    
    print("📁 FILE ORGANIZER")
    print("🎯 Analyse et organisation du workspace")
    print("=" * 50)
    
    # Structure attendue
    expected_structure = {
        "copilotage": "🤖 Coordination agents",
        "production": "📦 Documents finaux",
        "research": "📚 Recherche active",
        "data": "📊 Données et références",
        "publications": "📖 Articles et livres",
        "tools": "🔧 Scripts utilitaires",
        "archives": "🗄️ Historique et backups"
    }
    
    print("📊 ANALYSE STRUCTURE :")
    
    current_dirs = [d.name for d in Path(".").iterdir() if d.is_dir() and not d.name.startswith('.')]
    current_files = [f.name for f in Path(".").iterdir() if f.is_file()]
    
    # Vérifier dossiers attendus
    for expected_dir, description in expected_structure.items():
        if expected_dir in current_dirs:
            print(f"   ✅ {expected_dir}/ - {description}")
        else:
            print(f"   ❌ {expected_dir}/ - MANQUANT - {description}")
    
    # Identifier dossiers inattendus
    unexpected_dirs = [d for d in current_dirs if d not in expected_structure.keys()]
    if unexpected_dirs:
        print(f"\n⚠️  DOSSIERS INATTENDUS :")
        for unexpected in unexpected_dirs:
            print(f"   📁 {unexpected}/ - À analyser")
    
    # Analyser fichiers racine
    print(f"\n📄 FICHIERS RACINE ({len(current_files)}) :")
    for file in current_files:
        print(f"   📄 {file}")
    
    return current_dirs, current_files, unexpected_dirs

def organize_misplaced_files():
    """Organiser fichiers mal placés"""
    
    print(f"\n🔄 ORGANISATION FICHIERS :")
    
    # Règles d'organisation
    organization_rules = {
        # Scripts et utilitaires
        "*.py": ("tools/scripts", "🐍 Scripts Python"),
        "*.sh": ("tools/scripts", "🔧 Scripts bash"),
        "*.js": ("tools/scripts", "📜 Scripts JavaScript"),
        
        # Documents et rapports
        "*.md": ("", "📄 Documentation - Analyser manuellement"),
        "*.pdf": ("production/documents", "📑 Documents PDF"),
        "*.html": ("production/documents", "🌐 Documents HTML"),
        
        # Données et configuration
        "*.json": ("data/reference", "📊 Données JSON"),
        "*.csv": ("data/reference", "📈 Données CSV"),
        "*.txt": ("data/reference", "📝 Fichiers texte"),
        
        # Archives et logs
        "*.log": ("archives/logs", "📋 Fichiers de log"),
        "*.bak": ("archives/backups", "💾 Fichiers backup"),
        "*.tmp": ("DELETE", "🗑️ Fichiers temporaires")
    }
    
    organized_count = 0
    root_files = [f for f in Path(".").iterdir() if f.is_file()]
    
    for file_path in root_files:
        file_name = file_path.name
        file_ext = "*" + file_path.suffix if file_path.suffix else file_name
        
        # Chercher règle applicable
        destination = None
        description = None
        
        for pattern, (dest, desc) in organization_rules.items():
            if pattern.startswith("*") and file_name.endswith(pattern[1:]):
                destination = dest
                description = desc
                break
            elif pattern == file_name:
                destination = dest
                description = desc
                break
        
        if destination:
            if destination == "DELETE":
                try:
                    file_path.unlink()
                    organized_count += 1
                    print(f"   🗑️  {file_name} - Supprimé (temporaire)")
                except Exception as e:
                    print(f"   ❌ {file_name} - Erreur suppression : {e}")
            elif destination == "":
                print(f"   📄 {file_name} - {description}")
            else:
                try:
                    dest_path = Path(destination)
                    dest_path.mkdir(parents=True, exist_ok=True)
                    shutil.move(file_path, dest_path / file_name)
                    organized_count += 1
                    print(f"   ✅ {file_name} → {destination}/ - {description}")
                except Exception as e:
                    print(f"   ❌ {file_name} - Erreur déplacement : {e}")
        else:
            print(f"   ❓ {file_name} - Aucune règle définie")
    
    print(f"\n📊 {organized_count} fichiers organisés")
    return organized_count

def validate_naming_conventions():
    """Valider conventions de nommage"""
    
    print(f"\n📝 VALIDATION CONVENTIONS NOMMAGE :")
    
    # Conventions attendues
    naming_patterns = {
        "research/discoveries": {
            "pattern": r"[A-Z_]+\.md$",
            "example": "DECOUVERTE_DHATU_CORE_SET.md",
            "description": "MAJUSCULES avec underscores"
        },
        "data/references_cache": {
            "pattern": r"[A-Z_]+_v\d+\.\d+\.\d+\.md$|[A-Z_]+\.md$",
            "example": "REGLES_COPILOTAGE_v0.0.1.md",
            "description": "MAJUSCULES avec versioning"
        },
        "production/documents": {
            "pattern": r"[a-z_]+\.(pdf|html)$",
            "example": "dhatu_complete_final.pdf",
            "description": "minuscules avec underscores"
        }
    }
    
    violations = 0
    
    for directory, rules in naming_patterns.items():
        dir_path = Path(directory)
        if dir_path.exists():
            print(f"   📁 {directory}/ - {rules['description']}")
            files = [f for f in dir_path.rglob("*") if f.is_file()]
            
            import re
            pattern = re.compile(rules["pattern"])
            
            for file in files:
                if not pattern.match(file.name):
                    violations += 1
                    print(f"      ⚠️  {file.name} - Non conforme (ex: {rules['example']})")
        else:
            print(f"   ⏭️  {directory}/ - N'existe pas")
    
    if violations == 0:
        print("   ✅ Toutes les conventions respectées")
    else:
        print(f"   ⚠️  {violations} violations trouvées")
    
    return violations

def create_organization_report():
    """Créer rapport d'organisation"""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Analyser état actuel
    current_dirs, current_files, unexpected_dirs = analyze_workspace_structure()
    organized_count = organize_misplaced_files()
    violations = validate_naming_conventions()
    
    # Calculer score organisation
    structure_score = len([d for d in ["copilotage", "production", "research", "data"] if d in current_dirs]) / 4 * 100
    cleanliness_score = max(0, (10 - len(current_files)) / 10 * 100) if len(current_files) > 0 else 100
    naming_score = max(0, (20 - violations) / 20 * 100) if violations > 0 else 100
    
    overall_score = (structure_score + cleanliness_score + naming_score) / 3
    
    # Rapport détaillé
    report = f"""# 📁 RAPPORT ORGANISATION - {timestamp}

## 📊 SCORE GLOBAL : {overall_score:.1f}%

### 🎯 MÉTRIQUES
- 📁 Structure : {structure_score:.1f}% ({len(current_dirs)} dossiers)
- 🧹 Propreté : {cleanliness_score:.1f}% ({len(current_files)} fichiers racine)
- 📝 Conventions : {naming_score:.1f}% ({violations} violations)

### ✅ ACTIONS RÉALISÉES
- 📦 Fichiers organisés : {organized_count}
- 📁 Dossiers analysés : {len(current_dirs)}
- ⚠️  Violations nommage : {violations}

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

### 🎯 RECOMMANDATIONS
{f"✅ Organisation excellente - Maintenance continue" if overall_score >= 90 else ""}
{f"🔧 Améliorations mineures possibles" if 75 <= overall_score < 90 else ""}
{f"⚠️ Réorganisation recommandée" if 50 <= overall_score < 75 else ""}
{f"🚨 Réorganisation urgente nécessaire" if overall_score < 50 else ""}

---
*Rapport automatique - File Organizer*
"""
    
    # Sauvegarder rapport
    report_path = Path("copilotage/maintenance/last_organization_report.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\n📄 Rapport sauvé : {report_path}")
    print(f"📊 Score organisation : {overall_score:.1f}%")
    
    return overall_score

def main():
    """Organisateur principal de fichiers"""
    
    os.chdir(Path(__file__).parent.parent.parent)  # Retour racine
    
    print("📁 FILE ORGANIZER PANINI-FS")
    print("🎯 Organisation intelligente du workspace")
    print()
    
    # Générer rapport complet
    score = create_organization_report()
    
    print(f"\n🎉 ORGANISATION TERMINÉE")
    print(f"   📊 Score : {score:.1f}%")
    print(f"   📄 Rapport : copilotage/maintenance/last_organization_report.md")
    
    # Code retour
    if score >= 80:
        return 0  # Excellent
    elif score >= 60:
        return 1  # Bon
    else:
        return 2  # À améliorer

if __name__ == "__main__":
    exit(main())
