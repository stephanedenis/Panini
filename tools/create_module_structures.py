#!/usr/bin/env python3
"""
Script pour créer les structures manquantes dans les modules

Crée automatiquement README.md et docs/ pour les modules qui en manquent.

Date: 2025-11-12
"""

from pathlib import Path
from datetime import datetime

# Template README.md pour un module
README_TEMPLATE = """# {module_name}

**Date de création**: {date}  
**Statut**: 🚧 En développement

## 🎯 Objectif

{description}

## 📁 Structure

```
{module_name}/
├── README.md          # Ce fichier
├── docs/             # Documentation du module
├── src/              # Code source
└── tests/            # Tests unitaires
```

## 🔧 Utilisation

```python
# À compléter
```

## 📚 Documentation

Voir `/docs` pour la documentation complète.

## 🧪 Tests

```bash
pytest tests/
```

## 🔗 Dépendances

- À documenter

## 📝 Historique

| Date       | Action                    | Auteur  |
|------------|---------------------------|---------|
| {date}     | Création module           | Système |

---

**Maintenu par**: Équipe Panini  
**Dernière mise à jour**: {date}
"""

DOCS_README_TEMPLATE = """# Documentation - {module_name}

**Date de création**: {date}

## 📚 Contenu

Cette documentation couvre :

- Architecture du module
- Guides d'utilisation
- Références API
- Exemples de code

## 📁 Structure

```
docs/
├── README.md         # Ce fichier
├── architecture/    # Diagrammes et conception
├── guides/          # Guides utilisateur
└── api/             # Documentation API
```

## 🚀 Commencer

1. Consulter les guides d'utilisation
2. Voir les exemples de code
3. Explorer la documentation API

## 🔗 Liens Utiles

- Documentation projet parent: `/docs`
- Code source: `../src`
- Tests: `../tests`

---

**Dernière mise à jour**: {date}
"""

# Descriptions par défaut des modules
MODULE_DESCRIPTIONS = {
    'core': 'Fonctionnalités et composants de base du système Panini.',
    'data': 'Gestion, transformation et persistence des données.',
    'infrastructure': 'Infrastructure technique, déploiement et configuration.',
    'missions': 'Orchestration et gestion des missions autonomes.',
    'orchestration': 'Coordination des composants et workflows du système.',
    'publication': 'Gestion de la publication et distribution du contenu.',
    'reactive': 'Programmation réactive et gestion des événements.',
    'services': 'Services applicatifs et APIs externes.',
}


def create_module_structure(module_path: Path, module_name: str):
    """Crée les structures manquantes pour un module"""
    date = datetime.now().strftime('%Y-%m-%d')
    description = MODULE_DESCRIPTIONS.get(module_name, 'Module du projet Panini.')
    
    changes = []
    
    # Créer README.md si manquant
    readme_path = module_path / 'README.md'
    if not readme_path.exists():
        content = README_TEMPLATE.format(
            module_name=module_name,
            date=date,
            description=description
        )
        readme_path.write_text(content, encoding='utf-8')
        changes.append(f"✅ Créé: {readme_path.relative_to(module_path.parent.parent)}")
    
    # Créer docs/ si manquant
    docs_dir = module_path / 'docs'
    if not docs_dir.exists():
        docs_dir.mkdir(parents=True)
        changes.append(f"✅ Créé: {docs_dir.relative_to(module_path.parent.parent)}/")
        
        # Créer README dans docs/
        docs_readme = docs_dir / 'README.md'
        content = DOCS_README_TEMPLATE.format(
            module_name=module_name,
            date=date
        )
        docs_readme.write_text(content, encoding='utf-8')
        changes.append(f"✅ Créé: {docs_readme.relative_to(module_path.parent.parent)}")
        
        # Créer sous-dossiers de base
        for subdir in ['architecture', 'guides', 'api']:
            (docs_dir / subdir).mkdir(exist_ok=True)
            changes.append(f"✅ Créé: {(docs_dir / subdir).relative_to(module_path.parent.parent)}/")
    
    return changes


def main():
    """Point d'entrée principal"""
    root = Path(__file__).parent.parent
    modules_dir = root / 'modules'
    
    print("🔨 Création des structures manquantes pour les modules...")
    print()
    
    all_changes = []
    
    if modules_dir.exists():
        for module_path in sorted(modules_dir.iterdir()):
            if module_path.is_dir() and not module_path.name.startswith('.'):
                module_name = module_path.name
                print(f"📦 Module: {module_name}")
                
                changes = create_module_structure(module_path, module_name)
                if changes:
                    for change in changes:
                        print(f"   {change}")
                    all_changes.extend(changes)
                else:
                    print(f"   ✅ Structure déjà complète")
                print()
    
    # Résumé
    print("=" * 80)
    if all_changes:
        print(f"✅ {len(all_changes)} modifications effectuées")
        print()
        print("🔄 Prochaines étapes:")
        print("   1. Personnaliser les README.md créés")
        print("   2. Ajouter la documentation dans docs/")
        print("   3. Relancer la validation: python3 tools/validate_module_coherence.py")
    else:
        print("✅ Toutes les structures sont déjà en place")
    print("=" * 80)


if __name__ == '__main__':
    main()
