#!/usr/bin/env python3
"""
RÉORGANISATION WORKSPACE - Structure claire et logique
"""

import os
import shutil
from pathlib import Path

def create_clean_structure():
    """Créer structure de dossiers claire et logique"""
    
    print("📁 RÉORGANISATION WORKSPACE PANINI-FS")
    print("🎯 Objectif : Structure claire et navigable")
    print("="*60)
    
    # NOUVELLE STRUCTURE LOGIQUE
    new_structure = {
        # === PRODUCTION (Fichiers finaux) ===
        "production": {
            "description": "Documents finaux prêts à utiliser",
            "subdirs": ["documents", "generators"]
        },
        
        # === ARCHIVES (Backups et historique) ===  
        "archives": {
            "description": "Backups et historique expérimentations",
            "subdirs": ["experiments", "backups", "reports"]
        },
        
        # === RESEARCH (Recherche active) ===
        "research": {
            "description": "Recherche et développement en cours", 
            "subdirs": ["discoveries", "methodology", "analysis"]
        },
        
        # === PUBLICATIONS (Articles et livres) ===
        "publications": {
            "description": "Articles, livres et documentation",
            "subdirs": ["articles", "books", "docs"]
        },
        
        # === TOOLS (Outils et scripts) ===
        "tools": {
            "description": "Scripts utiles et outils de développement",
            "subdirs": ["scripts", "utilities"]
        },
        
        # === DATA (Données et références) ===
        "data": {
            "description": "Données de référence et corpus",
            "subdirs": ["reference", "corpus", "models"]
        }
    }
    
    # Créer la nouvelle structure
    print("🏗️  CRÉATION NOUVELLE STRUCTURE :")
    for main_dir, info in new_structure.items():
        main_path = Path(main_dir)
        main_path.mkdir(exist_ok=True)
        print(f"   📁 {main_dir}/ - {info['description']}")
        
        for subdir in info['subdirs']:
            sub_path = main_path / subdir
            sub_path.mkdir(exist_ok=True)
            print(f"      📂 {subdir}/")
    
    return new_structure

def move_existing_content():
    """Déplacer le contenu existant vers la nouvelle structure"""
    
    print(f"\n📦 MIGRATION CONTENU EXISTANT :")
    
    migrations = [
        # === PRODUCTION ===
        ("dhatu_complete_final.pdf", "production/documents/"),
        ("dhatu_complete_final.html", "production/documents/"),
        ("generate_dhatu_unicode_final.py", "production/generators/"),
        
        # === ARCHIVES ===
        ("archive_experimentations", "archives/experiments/"),
        ("backup_before_radical_cleanup", "archives/backups/"),
        ("backup_scripts_experimentaux", "archives/backups/"),
        ("FINAL_CLEANUP_REPORT.md", "archives/reports/"),
        ("WORKSPACE_CLEANED.md", "archives/reports/"),
        
        # === RESEARCH ===
        ("discoveries", "research/discoveries/"),
        ("methodology", "research/methodology/"), 
        ("analysis", "research/analysis/"),
        ("experiments", "research/"),
        
        # === PUBLICATIONS ===
        ("publications", "publications/"),
        ("docs", "publications/docs/"),
        
        # === TOOLS ===
        ("scripts", "tools/scripts/"),
        
        # === DATA ===
        ("data", "data/corpus/"),
        ("reference", "data/reference/"),
        ("models", "data/models/"),
        
        # === NETTOYAGE (dossiers temporaires) ===
        ("node_modules", "_temp_to_delete/"),
        ("playwright-report", "_temp_to_delete/"),
        ("test-results", "_temp_to_delete/"),
        ("tests", "_temp_to_delete/"),
        ("validation", "_temp_to_delete/"),
        ("copilotage", "_temp_to_delete/"),
        ("language", "_temp_to_delete/"),
        ("cloud-processing", "_temp_to_delete/")
    ]
    
    moved_count = 0
    temp_dir = Path("_temp_to_delete")
    temp_dir.mkdir(exist_ok=True)
    
    for source, destination in migrations:
        source_path = Path(source)
        dest_path = Path(destination)
        
        if source_path.exists():
            try:
                # Créer le répertoire de destination si nécessaire
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                if source_path.is_dir():
                    if dest_path.exists():
                        shutil.rmtree(dest_path)
                    shutil.move(str(source_path), str(dest_path))
                else:
                    shutil.move(str(source_path), str(dest_path))
                
                moved_count += 1
                print(f"   ✅ {source} → {destination}")
                
            except Exception as e:
                print(f"   ❌ Erreur {source} : {e}")
        # else:
        #     print(f"   ⏭️  {source} (n'existe pas)")
    
    print(f"\n📊 {moved_count} éléments déplacés")
    return moved_count

def create_navigation_readme():
    """Créer README de navigation dans la nouvelle structure"""
    
    readme_content = """# 📁 Structure Workspace PaniniFS-Research

## 🎯 Organisation Logique

### 📦 PRODUCTION (Prêt à utiliser)
```
production/
├── documents/          # Documents finaux (PDF, HTML)
│   ├── dhatu_complete_final.pdf    # Document Unicode reMarkable
│   └── dhatu_complete_final.html   # Source HTML
└── generators/         # Générateurs fonctionnels
    └── generate_dhatu_unicode_final.py  # Générateur LibreOffice
```

### 📚 RESEARCH (Recherche active)
```
research/
├── discoveries/        # Découvertes linguistiques
├── methodology/        # Méthodologies de recherche
├── analysis/          # Analyses en cours
└── experiments/       # Expérimentations diverses
```

### 📖 PUBLICATIONS (Articles et livres)
```
publications/
├── articles/          # Articles Medium, académiques
├── books/            # Livres LeanPub
└── docs/             # Documentation générale
```

### 🔧 TOOLS (Outils de développement)
```
tools/
├── scripts/          # Scripts utiles
│   └── generate_research_rss.py  # Générateur RSS
└── utilities/        # Utilitaires divers
```

### 📊 DATA (Données et références)
```
data/
├── reference/        # Données de référence
├── corpus/          # Corpus linguistiques
└── models/          # Modèles et structures
```

### 🗄️ ARCHIVES (Historique et backups)
```
archives/
├── experiments/      # PDF d'expérimentations
├── backups/         # Sauvegardes de sécurité
└── reports/         # Rapports de nettoyage
```

## 🚀 Usage

### Documents Finaux
- **reMarkable** : `production/documents/dhatu_complete_final.pdf`
- **Régénération** : `python3 production/generators/generate_dhatu_unicode_final.py`

### Recherche
- **Nouvelles découvertes** : `research/discoveries/`
- **Méthodologies** : `research/methodology/`

### Publications
- **Articles** : `publications/articles/`
- **Livres** : `publications/books/`

## ✅ Avantages Structure

- 📂 **Navigation intuitive** par fonction
- 🎯 **Séparation claire** production/recherche/archives
- 🔍 **Recherche rapide** par domaine
- 🚀 **Prêt production** dans `production/`
- 💾 **Sécurité** avec `archives/`

*Structure optimisée - 9 septembre 2025*
"""

    with open("README_NAVIGATION.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"✅ Guide de navigation créé : README_NAVIGATION.md")

def cleanup_temp():
    """Nettoyer les dossiers temporaires"""
    
    print(f"\n🧹 NETTOYAGE DOSSIERS TEMPORAIRES :")
    
    temp_dir = Path("_temp_to_delete")
    if temp_dir.exists():
        try:
            shutil.rmtree(temp_dir)
            print(f"✅ Dossiers temporaires supprimés")
        except Exception as e:
            print(f"❌ Erreur nettoyage : {e}")

def show_new_structure():
    """Afficher la nouvelle structure"""
    
    print(f"\n📁 NOUVELLE STRUCTURE FINALE :")
    
    for root, dirs, files in os.walk('.'):
        # Ignorer .git
        if '.git' in root:
            continue
            
        level = root.replace('.', '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}📁 {os.path.basename(root)}/")
        
        subindent = ' ' * 2 * (level + 1)
        for file in files[:3]:  # Premiers 3 fichiers
            if not file.startswith('.'):
                print(f"{subindent}📄 {file}")
        if len(files) > 3:
            print(f"{subindent}... et {len(files)-3} autres fichiers")

def main():
    print("🏗️  RÉORGANISATION COMPLÈTE WORKSPACE")
    print("🎯 Objectif : Structure claire par fonction")
    print()
    
    # 1. Créer nouvelle structure
    new_structure = create_clean_structure()
    
    # 2. Migrer contenu existant
    moved = move_existing_content()
    
    # 3. Créer guide navigation
    create_navigation_readme()
    
    # 4. Nettoyer temporaires
    cleanup_temp()
    
    # 5. Afficher résultat
    show_new_structure()
    
    print(f"\n🎉 RÉORGANISATION TERMINÉE")
    print(f"   📦 {moved} éléments déplacés")
    print(f"   📁 6 sections principales créées")
    print(f"   📋 Guide navigation : README_NAVIGATION.md")
    print(f"   ✨ Structure claire et navigable")
    
    print(f"\n🚀 ACCÈS RAPIDE :")
    print(f"   📄 Document final : production/documents/dhatu_complete_final.pdf")
    print(f"   🐍 Générateur : production/generators/generate_dhatu_unicode_final.py")
    print(f"   📚 Recherche : research/")
    print(f"   📖 Publications : publications/")
    print(f"   🗄️ Archives : archives/")

if __name__ == "__main__":
    main()
