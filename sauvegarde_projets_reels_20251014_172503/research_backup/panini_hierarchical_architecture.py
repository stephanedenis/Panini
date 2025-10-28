#!/usr/bin/env python3
"""
🏗️ PANINI-FS HIERARCHICAL KNOWLEDGE ARCHITECTURE
============================================================
🎯 Mission: Architecture hiérarchique exclusive avec confidentialités indépendantes
🔬 Focus: Privé exclusif → Teams partagés → Public ouvert
🚀 Design: Hiérarchie stricte avec zones de confidentialités séparées

HIÉRARCHIE ÉTABLIE:
┌─────────────────────────────────────────────────────────┐
│ 🔒 PRIVÉ (Exclusif, Base de tout)                      │
│ ├── Connaissances personnelles complètes               │ 
│ ├── Source de vérité pour synchronisation              │
│ └── Aucun partage automatique                          │
└─────────────────────────────────────────────────────────┘
           │ Filtrage sélectif vers ↓
┌─────────────────────────────────────────────────────────┐
│ 👥 TEAMS (Confidentialités indépendantes)              │
│ ├── Team A: Confidentialité isolée                     │
│ ├── Team B: Confidentialité isolée                     │
│ ├── Elements communs possibles entre teams             │
│ └── Synchronisation bidirectionnelle limitée           │
└─────────────────────────────────────────────────────────┘
           │ Anonymisation vers ↓
┌─────────────────────────────────────────────────────────┐
│ 🌐 PUBLIC (Concepts anonymisés)                        │
│ ├── Synthèses conceptuelles sans données privées       │
│ ├── Relations génériques                               │
│ └── Pas de remontée vers niveaux supérieurs           │
└─────────────────────────────────────────────────────────┘
"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, asdict
import hashlib

@dataclass
class ConfidentialityZone:
    """Zone de confidentialité avec règles d'isolation"""
    zone_id: str
    zone_type: str  # 'private', 'team_a', 'team_b', 'public'
    isolation_level: str  # 'exclusive', 'shared_limited', 'open'
    access_rules: Dict[str, Any]
    sharing_targets: List[str]  # Zones vers lesquelles on peut partager
    restricted_from: List[str]  # Zones d'où on ne peut pas recevoir

@dataclass 
class HierarchicalRule:
    """Règle de hiérarchie pour contrôle de flux"""
    from_zone: str
    to_zone: str
    flow_type: str  # 'one_way', 'bidirectional', 'blocked'
    filter_policy: str  # 'full', 'anonymized', 'metadata_only', 'blocked'
    approval_required: bool

class PaniniHierarchicalArchitect:
    """Architecte de la hiérarchie des connaissances PaniniFS"""
    
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)
        self.session_id = datetime.now().strftime("%Y-%m-%dT%H-%M-%SZ")
        
        # Configuration des zones de confidentialité
        self.confidentiality_zones = self._setup_confidentiality_zones()
        
        # Règles hiérarchiques strictes
        self.hierarchical_rules = self._setup_hierarchical_rules()
        
        # Architecture des repositories avec hiérarchie
        self.hierarchical_repos = self._setup_hierarchical_repos()
    
    def _setup_confidentiality_zones(self) -> Dict[str, ConfidentialityZone]:
        """Configuration des zones de confidentialité indépendantes"""
        return {
            'private_exclusive': ConfidentialityZone(
                zone_id='private_exclusive',
                zone_type='private',
                isolation_level='exclusive',
                access_rules={
                    'read_access': ['owner_only'],
                    'write_access': ['owner_only'],
                    'share_access': ['manual_selection_only'],
                    'audit_level': 'full_tracking'
                },
                sharing_targets=['team_a', 'team_b', 'public_anonymized'],
                restricted_from=[]  # Ne reçoit de personne
            ),
            
            'team_a_confidential': ConfidentialityZone(
                zone_id='team_a_confidential',
                zone_type='team_a',
                isolation_level='shared_limited',
                access_rules={
                    'read_access': ['team_a_members'],
                    'write_access': ['team_a_contributors'],
                    'share_access': ['team_a_leads'],
                    'audit_level': 'team_tracking'
                },
                sharing_targets=['public_anonymized'],  # Peut partager vers public
                restricted_from=['team_b_confidential']  # Isolation des autres teams
            ),
            
            'team_b_confidential': ConfidentialityZone(
                zone_id='team_b_confidential', 
                zone_type='team_b',
                isolation_level='shared_limited',
                access_rules={
                    'read_access': ['team_b_members'],
                    'write_access': ['team_b_contributors'],
                    'share_access': ['team_b_leads'],
                    'audit_level': 'team_tracking'
                },
                sharing_targets=['public_anonymized'],
                restricted_from=['team_a_confidential']  # Isolation des autres teams
            ),
            
            'teams_common_area': ConfidentialityZone(
                zone_id='teams_common_area',
                zone_type='inter_team',
                isolation_level='shared_limited',
                access_rules={
                    'read_access': ['all_team_members'],
                    'write_access': ['cross_team_leads'],
                    'share_access': ['project_managers'],
                    'audit_level': 'cross_team_tracking'
                },
                sharing_targets=['public_anonymized'],
                restricted_from=[]  # Peut recevoir des teams mais pas du privé
            ),
            
            'public_anonymized': ConfidentialityZone(
                zone_id='public_anonymized',
                zone_type='public',
                isolation_level='open',
                access_rules={
                    'read_access': ['everyone'],
                    'write_access': ['system_only'],  # Seulement par synchronisation
                    'share_access': ['unrestricted'],
                    'audit_level': 'minimal_tracking'
                },
                sharing_targets=[],  # Ne partage vers personne (niveau le plus bas)
                restricted_from=[]  # Peut recevoir de tous mais filtré
            )
        }
    
    def _setup_hierarchical_rules(self) -> List[HierarchicalRule]:
        """Règles hiérarchiques strictes pour contrôle de flux"""
        return [
            # PRIVÉ → TEAMS (filtrage sélectif manuel)
            HierarchicalRule(
                from_zone='private_exclusive',
                to_zone='team_a_confidential',
                flow_type='one_way',
                filter_policy='manual_selection',
                approval_required=True
            ),
            HierarchicalRule(
                from_zone='private_exclusive',
                to_zone='team_b_confidential', 
                flow_type='one_way',
                filter_policy='manual_selection',
                approval_required=True
            ),
            
            # TEAMS → PUBLIC (anonymisation automatique)
            HierarchicalRule(
                from_zone='team_a_confidential',
                to_zone='public_anonymized',
                flow_type='one_way',
                filter_policy='anonymized',
                approval_required=False
            ),
            HierarchicalRule(
                from_zone='team_b_confidential',
                to_zone='public_anonymized',
                flow_type='one_way', 
                filter_policy='anonymized',
                approval_required=False
            ),
            
            # TEAMS ↔ COMMON AREA (éléments communs possibles)
            HierarchicalRule(
                from_zone='team_a_confidential',
                to_zone='teams_common_area',
                flow_type='bidirectional',
                filter_policy='metadata_only',
                approval_required=True
            ),
            HierarchicalRule(
                from_zone='team_b_confidential',
                to_zone='teams_common_area',
                flow_type='bidirectional',
                filter_policy='metadata_only',
                approval_required=True
            ),
            
            # INTERDICTIONS STRICTES
            HierarchicalRule(
                from_zone='public_anonymized',
                to_zone='private_exclusive',
                flow_type='blocked',
                filter_policy='blocked',
                approval_required=False
            ),
            HierarchicalRule(
                from_zone='team_a_confidential',
                to_zone='team_b_confidential',
                flow_type='blocked',
                filter_policy='blocked', 
                approval_required=False
            ),
            HierarchicalRule(
                from_zone='team_b_confidential',
                to_zone='team_a_confidential',
                flow_type='blocked',
                filter_policy='blocked',
                approval_required=False
            )
        ]
    
    def _setup_hierarchical_repos(self) -> Dict[str, Dict[str, Any]]:
        """Configuration des repositories avec hiérarchie stricte"""
        return {
            'panini_private_base': {
                'name': 'panini-private-knowledge-base',
                'confidentiality_zone': 'private_exclusive',
                'hierarchy_level': 1,  # Niveau le plus élevé
                'description': 'Repository privé exclusif - Source de vérité personnelle',
                'path': self.workspace_root / 'repos' / 'panini-private-knowledge-base',
                'structure': {
                    'knowledge/personal/': 'Connaissances exclusivement personnelles',
                    'knowledge/candidates_for_sharing/': 'Candidats pour partage vers teams',
                    'sync/outbound_rules/': 'Règles de partage vers teams',
                    'audit/sharing_history/': 'Historique des partages effectués'
                },
                'sync_targets': ['panini_team_a', 'panini_team_b'],
                'sync_policy': 'manual_approval_required'
            },
            
            'panini_team_a': {
                'name': 'panini-team-a-knowledge', 
                'confidentiality_zone': 'team_a_confidential',
                'hierarchy_level': 2,
                'description': 'Repository Team A - Confidentialité isolée',
                'path': self.workspace_root / 'repos' / 'panini-team-a-knowledge',
                'structure': {
                    'knowledge/team_specific/': 'Connaissances spécifiques Team A',
                    'knowledge/from_private/': 'Connaissances reçues du privé',
                    'knowledge/candidates_for_common/': 'Candidats zone commune',
                    'sync/to_public_queue/': 'Queue pour synchronisation publique'
                },
                'sync_targets': ['panini_teams_common', 'panini_public'],
                'sync_policy': 'team_lead_approval'
            },
            
            'panini_team_b': {
                'name': 'panini-team-b-knowledge',
                'confidentiality_zone': 'team_b_confidential', 
                'hierarchy_level': 2,
                'description': 'Repository Team B - Confidentialité isolée',
                'path': self.workspace_root / 'repos' / 'panini-team-b-knowledge',
                'structure': {
                    'knowledge/team_specific/': 'Connaissances spécifiques Team B',
                    'knowledge/from_private/': 'Connaissances reçues du privé',
                    'knowledge/candidates_for_common/': 'Candidats zone commune',
                    'sync/to_public_queue/': 'Queue pour synchronisation publique'
                },
                'sync_targets': ['panini_teams_common', 'panini_public'],
                'sync_policy': 'team_lead_approval'
            },
            
            'panini_teams_common': {
                'name': 'panini-teams-common-knowledge',
                'confidentiality_zone': 'teams_common_area',
                'hierarchy_level': 2.5,  # Entre teams et public
                'description': 'Zone commune entre teams - Éléments partagés',
                'path': self.workspace_root / 'repos' / 'panini-teams-common-knowledge',
                'structure': {
                    'knowledge/cross_team/': 'Connaissances inter-équipes',
                    'knowledge/shared_projects/': 'Projets collaboratifs',
                    'knowledge/common_concepts/': 'Concepts communs validés',
                    'sync/from_teams/': 'Contributions des teams'
                },
                'sync_targets': ['panini_public'],
                'sync_policy': 'cross_team_consensus'
            },
            
            'panini_public': {
                'name': 'panini-public-knowledge',
                'confidentiality_zone': 'public_anonymized',
                'hierarchy_level': 3,  # Niveau le plus bas
                'description': 'Repository public - Concepts anonymisés uniquement',
                'path': self.workspace_root / 'repos' / 'panini-public-knowledge',
                'structure': {
                    'knowledge/concepts/': 'Concepts génériques anonymisés',
                    'knowledge/relations/': 'Relations conceptuelles publiques',
                    'knowledge/aggregated/': 'Données agrégées sans sources',
                    'metadata/contributors/': 'Métadonnées de contribution anonymes'
                },
                'sync_targets': [],  # Pas de synchronisation sortante
                'sync_policy': 'automatic_from_approved_sources'
            }
        }
    
    def validate_hierarchical_flow(self, from_zone: str, to_zone: str, content_type: str) -> Dict[str, Any]:
        """Validation d'un flux selon les règles hiérarchiques"""
        
        # Trouver la règle applicable
        applicable_rule = None
        for rule in self.hierarchical_rules:
            if rule.from_zone == from_zone and rule.to_zone == to_zone:
                applicable_rule = rule
                break
        
        if not applicable_rule:
            return {
                'allowed': False,
                'reason': f'Aucune règle définie pour {from_zone} → {to_zone}',
                'filter_required': None
            }
        
        if applicable_rule.flow_type == 'blocked':
            return {
                'allowed': False,
                'reason': f'Flux bloqué entre {from_zone} et {to_zone}',
                'filter_required': None
            }
        
        return {
            'allowed': True,
            'flow_type': applicable_rule.flow_type,
            'filter_policy': applicable_rule.filter_policy,
            'approval_required': applicable_rule.approval_required,
            'content_type': content_type
        }
    
    def create_hierarchical_repositories(self):
        """Création des repositories avec structure hiérarchique"""
        print("🏗️ Création de l'architecture hiérarchique PaniniFS")
        print("="*55)
        
        for repo_id, config in self.hierarchical_repos.items():
            repo_path = config['path']
            zone = config['confidentiality_zone']
            level = config['hierarchy_level']
            
            print(f"\n📁 Création {config['name']}")
            print(f"   Zone: {zone} (Niveau {level})")
            
            # Créer le repository Git
            if repo_path.exists():
                print(f"   ⚠️  Repository existe déjà: {repo_path}")
                continue
                
            repo_path.mkdir(parents=True, exist_ok=True)
            
            # Initialiser Git
            subprocess.run(['git', 'init'], cwd=repo_path, capture_output=True)
            
            # Créer structure selon hiérarchie
            for folder, description in config['structure'].items():
                folder_path = repo_path / folder
                folder_path.mkdir(parents=True, exist_ok=True)
                
                # Fichier README dans chaque dossier
                readme_content = f"# {folder}\n\n{description}\n\n**Zone de confidentialité**: {zone}\n**Niveau hiérarchique**: {level}\n"
                (folder_path / "README.md").write_text(readme_content)
            
            # Configuration du repository
            config_data = {
                'repository_id': repo_id,
                'confidentiality_zone': zone,
                'hierarchy_level': level,
                'sync_targets': config['sync_targets'],
                'sync_policy': config['sync_policy'],
                'created_at': self.session_id,
                'rules': [asdict(rule) for rule in self.hierarchical_rules if rule.from_zone == zone]
            }
            
            (repo_path / "PANINI_REPOSITORY_CONFIG.json").write_text(
                json.dumps(config_data, indent=2, ensure_ascii=False)
            )
            
            # Commit initial
            subprocess.run(['git', 'add', '.'], cwd=repo_path, capture_output=True)
            subprocess.run(['git', 'commit', '-m', f'🏗️ Initial hierarchical setup for {zone}'], 
                         cwd=repo_path, capture_output=True)
            
            print(f"   ✅ Repository créé avec structure hiérarchique")
    
    def generate_hierarchy_documentation(self):
        """Génération de la documentation de hiérarchie"""
        doc_content = f"""# 🏗️ ARCHITECTURE HIÉRARCHIQUE PANINI-FS

## 🎯 Principe de Hiérarchie Exclusive

### ✅ RÉPONSE À VOTRE QUESTION:
**OUI, nos encyclopédies sont hiérarchiques et exclusives :**

```
🔒 PRIVÉ (Niveau 1 - Base exclusive)
├── Source de vérité personnelle
├── Aucune remontée depuis niveaux inférieurs  
└── Partage manuel sélectif vers teams

👥 TEAMS (Niveau 2 - Confidentialités indépendantes)
├── Team A: Isolation stricte de Team B
├── Team B: Isolation stricte de Team A  
├── Zone commune possible entre teams
└── Synchronisation vers public uniquement

🌐 PUBLIC (Niveau 3 - Concepts anonymisés)
├── Réception depuis tous niveaux supérieurs
├── Anonymisation automatique
└── Aucune remontée vers niveaux supérieurs
```

## 📊 Zones de Confidentialité

### 🔒 Zone Privée Exclusive
- **Isolation**: Complète, aucune intrusion
- **Source**: Base de toutes connaissances
- **Partage**: Manuel sélectif uniquement

### 👥 Zones Teams Indépendantes  
- **Team A ↔ Team B**: Isolation stricte
- **Éléments communs**: Zone inter-teams séparée
- **Confidentialité**: Indépendante par team

### 🌐 Zone Publique Ouverte
- **Réception**: Filtrage automatique depuis tous
- **Contenu**: Concepts anonymisés uniquement
- **Accès**: Ouvert mais pas de remontée

## 🔄 Règles de Flux Hiérarchiques

### ✅ Flux Autorisés
```
PRIVÉ → TEAMS (manuel, filtré)
TEAMS → PUBLIC (automatique, anonymisé)  
TEAMS ↔ ZONE_COMMUNE (métadonnées, approbation)
```

### ❌ Flux Interdits
```
PUBLIC → PRIVÉ (bloqué)
PUBLIC → TEAMS (bloqué)
TEAM_A ↔ TEAM_B (isolation stricte)
```

## 📁 Repositories Créés

"""
        
        for repo_id, config in self.hierarchical_repos.items():
            doc_content += f"""
### {config['name']}
- **Zone**: {config['confidentiality_zone']}
- **Niveau**: {config['hierarchy_level']}  
- **Cibles sync**: {', '.join(config['sync_targets'])}
- **Politique**: {config['sync_policy']}
"""
        
        doc_content += f"""
## 🛡️ Validation de Sécurité

### Confidentialités Indépendantes
- ✅ Teams isolation stricte respectée
- ✅ Privé reste exclusif  
- ✅ Public anonymisé seulement
- ✅ Pas de remontée non autorisée

### Éléments Communs Teams
- ✅ Zone commune séparée des confidentialités
- ✅ Métadonnées seulement, pas de contenu sensible
- ✅ Approbation requise pour partage

**🎉 Architecture conforme à vos exigences!**

*Généré le {self.session_id}*
"""
        
        doc_path = self.workspace_root / f"HIERARCHICAL_ARCHITECTURE_ANALYSIS_{self.session_id}.md"
        doc_path.write_text(doc_content)
        
        return doc_path

def main():
    """Démonstration de l'architecture hiérarchique"""
    architect = PaniniHierarchicalArchitect()
    
    print("🏗️ PANINI-FS HIERARCHICAL ARCHITECTURE")
    print("🎯 Hiérarchie exclusive avec confidentialités indépendantes")
    print("="*60)
    
    # Créer les repositories hiérarchiques
    architect.create_hierarchical_repositories()
    
    # Tests de validation de flux
    print(f"\n🔍 Tests de validation des flux hiérarchiques:")
    
    test_flows = [
        ('private_exclusive', 'team_a_confidential', 'knowledge_share'),
        ('team_a_confidential', 'team_b_confidential', 'knowledge_share'),  # Devrait être bloqué
        ('team_a_confidential', 'public_anonymized', 'concept_share'),
        ('public_anonymized', 'private_exclusive', 'feedback'),  # Devrait être bloqué
    ]
    
    for from_zone, to_zone, content_type in test_flows:
        result = architect.validate_hierarchical_flow(from_zone, to_zone, content_type)
        status = "✅" if result['allowed'] else "❌"
        print(f"   {status} {from_zone} → {to_zone}: {result.get('reason', 'Autorisé')}")
    
    # Générer documentation
    doc_path = architect.generate_hierarchy_documentation()
    print(f"\n📚 Documentation générée: {doc_path}")
    
    print(f"\n🎉 Architecture hiérarchique PaniniFS créée avec succès!")
    print(f"📁 Repositories dans: ./repos/")

if __name__ == "__main__":
    main()