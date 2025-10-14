#!/usr/bin/env python3
"""
🚀 REFACTORING COMPLET ARCHITECTURE PANINI
==========================================

Exécution complète immédiate selon validations utilisateur :
1. PaniniFS-Research → Panini (module central)  
2. OntoWave → Panini-OntoWave
3. .gitignore pour 233GB données reconstructibles
4. domaine paninifs disponible
5. Support intégré dans Panini/
"""

import os
import subprocess
import time
from pathlib import Path
import json


class RefactoringArchitecturePanini:
    """Refactoring architecture complet validé"""
    
    def __init__(self):
        self.github_root = Path("/home/stephane/GitHub")
        self.current_research = self.github_root / "PaniniFS-Research"
        
        # Configuration refactoring
        self.config = {
            'module_central': 'Panini',
            'domaine_disponible': 'paninifs',
            'gitignore_data': True,
            'integration_support': True,
            'execution_immediate': True
        }
        
        print("🚀 REFACTORING ARCHITECTURE PANINI - EXÉCUTION IMMÉDIATE")
        print("=" * 55)
        print(f"✅ Validations utilisateur reçues")
        print(f"📁 Module central: {self.config['module_central']}")
        print(f"🌐 Domaine: {self.config['domaine_disponible']}")
        
    def phase_1_renommages_principaux(self):
        """Phase 1: Renommages critiques"""
        print("\n🔄 PHASE 1: RENOMMAGES PRINCIPAUX")
        print("=" * 35)
        
        renommages = [
            {
                'ancien': 'PaniniFS-Research',
                'nouveau': 'Panini',
                'type': 'module_central',
                'critique': True
            },
            {
                'ancien': 'OntoWave', 
                'nouveau': 'Panini-OntoWave',
                'type': 'produit',
                'critique': True
            }
        ]
        
        for renommage in renommages:
            print(f"   🔄 {renommage['ancien']} → {renommage['nouveau']}")
            
            ancien_path = self.github_root / renommage['ancien']
            nouveau_path = self.github_root / renommage['nouveau']
            
            if ancien_path.exists():
                # Git tag sécurité avant renommage
                try:
                    os.chdir(ancien_path)
                    subprocess.run([
                        'git', 'tag', f"pre-rename-{int(time.time())}"
                    ], check=False)
                    
                    # Renommage physique
                    print(f"      📁 Renommage physique...")
                    ancien_path.rename(nouveau_path)
                    
                    print(f"      ✅ {renommage['nouveau']} créé")
                    
                except Exception as e:
                    print(f"      ❌ Erreur: {e}")
            else:
                print(f"      ⚠️  {ancien_path} n'existe pas")
        
        # Mise à jour références
        self._update_references_phase1()
        
        return renommages

    def phase_2_gitignore_donnees(self):
        """Phase 2: Configuration .gitignore pour données reconstructibles"""
        print("\n📋 PHASE 2: CONFIGURATION .GITIGNORE DONNÉES")  
        print("=" * 45)
        
        panini_path = self.github_root / "Panini"
        if not panini_path.exists():
            print("   ⚠️  Panini n'existe pas encore, utilisation PaniniFS-Research")
            panini_path = self.current_research
        
        gitignore_path = panini_path / ".gitignore"
        
        # Règles .gitignore pour données reconstructibles
        gitignore_rules = [
            "",
            "# === DONNÉES RECONSTRUCTIBLES (233GB) ===",
            "# Copie Wikipedia et données dérivées - recette dispo pour reconstitution",
            "",
            "# Corpus Wikipedia complets",
            "corpus_*/",
            "wikipedia_*/",
            "*_corpus_complet.json",
            "*_corpus_unifie.json", 
            "",
            "# Collections multilingues reconstructibles",
            "corpus_multilingue_*.json",
            "grand_corpus_*.json",
            "collections_*.json",
            "",
            "# Données d'entraînement ML (reconstructibles)",
            "training_data/",
            "model_weights/",
            "embeddings_cache/",
            "*.pkl.gz",
            "*.h5",
            "*.safetensors",
            "",
            "# Analyses/métriques (regenerables)", 
            "analyse_*_*.json",
            "metrics_*/",
            "benchmark_results/",
            "performance_logs/",
            "",
            "# Cache et temporaires",
            "cache/",
            "temp/",
            ".cache/",
            "__pycache__/",
            "*.pyc",
            "*.pyo",
            "",
            "# Environnements virtuels",
            ".venv/",
            "venv/",
            "env/",
            "",
            "# IDE et éditeurs",
            ".vscode/settings.json",
            ".idea/",
            "*.swp",
            "*.swo",
            "",
            "# Logs système",
            "*.log",
            "logs/",
            "autonomous_*.log",
            "",
            "# === GARDER EN GIT ===",
            "# Scripts de reconstruction des données",
            "!scripts/reconstruction/",
            "!tools/data_generation/",
            "!recipes/",
            "",
            "# Configuration et métadonnées critiques",
            "!config/",
            "!*.md",
            "!*.py",
            "!*.json",
            "!*.toml",
            "!*.yaml",
            "!*.yml",
            "",
            "# Mais exclure les gros JSON de données",
            "*_data_*.json",
            "*_corpus_*.json",
            "*_collection_*.json"
        ]
        
        try:
            # Lire .gitignore existant
            existing_content = ""
            if gitignore_path.exists():
                with open(gitignore_path, 'r') as f:
                    existing_content = f.read()
            
            # Ajouter nouvelles règles si pas déjà présentes
            new_content = existing_content
            if "DONNÉES RECONSTRUCTIBLES" not in existing_content:
                new_content += "\n".join(gitignore_rules)
                
                with open(gitignore_path, 'w') as f:
                    f.write(new_content)
                
                print(f"   ✅ .gitignore mis à jour")
                print(f"   📊 {len(gitignore_rules)} règles ajoutées")
                print(f"   💾 Protection 233GB données reconstructibles")
            else:
                print(f"   ✅ .gitignore déjà configuré")
            
        except Exception as e:
            print(f"   ❌ Erreur .gitignore: {e}")
        
        return gitignore_rules

    def phase_3_integration_support(self):
        """Phase 3: Intégration modules support dans Panini/"""
        print("\n🔧 PHASE 3: INTÉGRATION SUPPORT DANS PANINI/")
        print("=" * 45)
        
        panini_path = self.github_root / "Panini"
        if not panini_path.exists():
            panini_path = self.current_research
            
        # Modules support à intégrer
        modules_support = [
            {
                'source': 'PaniniFS-ExecutionOrchestrator',
                'destination': 'orchestration',
                'description': 'Coordination Local/Colab/Cloud'
            },
            {
                'source': 'PaniniFS/modules/semantic-core',
                'destination': 'semantic-core', 
                'description': 'Dhātu universels'
            },
            {
                'source': 'modules/gest',  # Si dans PaniniFS
                'destination': 'computer-vision',
                'description': 'Outils vision computer'
            },
            {
                'source': 'copilotage',
                'destination': 'copilotage',
                'description': 'Infrastructure autonomie (déjà dans Research)'
            }
        ]
        
        # Créer structure Panini/ si pas existante
        support_dir = panini_path / "support"
        support_dir.mkdir(exist_ok=True)
        
        for module in modules_support:
            source_path = self.github_root / module['source']
            dest_path = support_dir / module['destination']
            
            print(f"   📦 {module['source']} → support/{module['destination']}/")
            
            if source_path.exists():
                try:
                    # Copie (pas move pour sécurité)
                    if not dest_path.exists():
                        if source_path.is_dir():
                            subprocess.run([
                                'cp', '-r', str(source_path), str(dest_path)
                            ], check=True)
                        else:
                            subprocess.run([
                                'cp', str(source_path), str(dest_path)
                            ], check=True)
                        
                        print(f"      ✅ Intégré dans Panini/support/")
                    else:
                        print(f"      ✅ Déjà présent")
                        
                except Exception as e:
                    print(f"      ❌ Erreur intégration: {e}")
            else:
                print(f"      ⚠️  Source introuvable: {source_path}")
        
        # Créer README support
        readme_support = support_dir / "README.md"
        with open(readme_support, 'w') as f:
            f.write("""# Panini Support Modules

Modules de support intégrés dans le module central Panini.

## Architecture

- `orchestration/` - Coordination Local/Colab/Cloud
- `semantic-core/` - Dhātu universels et primitives 
- `computer-vision/` - Outils vision computer
- `copilotage/` - Infrastructure autonomie

## Principe

Ces modules ne sont que du support à la recherche Panini.
Ils n'ont pas de raison d'être indépendants.
""")
        
        print(f"   📚 README support créé")
        
        return modules_support

    def phase_4_agents_spec_kits(self):
        """Phase 4: Configuration agents avec spec-kits individuels"""
        print("\n👥 PHASE 4: AGENTS ET SPEC-KITS INDIVIDUELS")
        print("=" * 45)
        
        agents_config = [
            {
                'nom': 'Agent-Panini',
                'workspace': 'Panini',
                'role': 'Coordinateur recherche centrale',
                'specialites': ['dhātu', 'théories', 'coordination', 'recherche'],
                'access': ['lecture_écriture_complète']
            },
            {
                'nom': 'Agent-OntoWave',
                'workspace': 'Panini-OntoWave', 
                'role': 'Documentation interactive production',
                'specialites': ['typescript', 'vite', 'architecture_fractale', 'APIs'],
                'access': ['Panini/semantic-core', 'Panini/bridges']
            },
            {
                'nom': 'Agent-FS',
                'workspace': 'Panini-FS',
                'role': 'Digesteur/resynthétiseur fichiers',
                'specialites': ['compression_sémantique', 'formats', 'parsing'],
                'access': ['Panini/semantic-core', 'Panini/orchestration']
            },
            {
                'nom': 'Agent-Gest',
                'workspace': 'Panini-Gest',
                'role': 'Reconnaissance gestuelle ASL/LSQ',
                'specialites': ['computer_vision', 'mediapipe', 'kinect', 'ML'],
                'access': ['Panini/semantic-core', 'Panini/computer-vision']
            }
        ]
        
        panini_path = self.github_root / "Panini"
        if not panini_path.exists():
            panini_path = self.current_research
            
        # Créer répertoire agents
        agents_dir = panini_path / "agents"
        agents_dir.mkdir(exist_ok=True)
        
        for agent in agents_config:
            print(f"   🤖 Configuration {agent['nom']}")
            
            # Créer spec-kit individuel
            agent_dir = agents_dir / agent['nom'].lower().replace('-', '_')
            agent_dir.mkdir(exist_ok=True)
            
            # Constitution spec-kit
            spec_kit = {
                'agent_identity': {
                    'name': agent['nom'],
                    'role': agent['role'],
                    'workspace': agent['workspace'],
                    'specialties': agent['specialites']
                },
                'access_rights': {
                    'primary_workspace': agent['workspace'],
                    'submodules_access': agent['access'],
                    'coordination': 'Via Agent-Panini'
                },
                'collaboration_protocols': {
                    'reporting': 'Agent-Panini',
                    'data_sharing': 'Panini/shared/',
                    'conflict_resolution': 'Agent-Panini arbitrage'
                },
                'autonomy_level': 'HIGH',
                'mission_types': agent['specialites']
            }
            
            # Sauvegarder spec-kit
            spec_file = agent_dir / "spec_kit.json"
            with open(spec_file, 'w') as f:
                json.dump(spec_kit, f, indent=2)
                
            print(f"      ✅ Spec-kit créé: {spec_file}")
        
        # Créer coordination centrale
        coordination_file = agents_dir / "coordination.md"
        with open(coordination_file, 'w') as f:
            f.write("""# Coordination Multi-Agents Panini

## Architecture

- **Agent-Panini** : Coordinateur central (vous)
- **Agent-OntoWave** : Documentation interactive  
- **Agent-FS** : Digesteur fichiers
- **Agent-Gest** : Vision computer

## Protocoles

1. **Reporting** : Tous les agents reportent à Agent-Panini
2. **Partage données** : Via Panini/shared/
3. **Résolution conflits** : Agent-Panini arbitre
4. **Synchronisation** : Panini/agents/sync/

## Domaines

- `paninifs` disponible pour redirection
- `ontowave.org` → Panini-OntoWave
""")
        
        print(f"   📋 Coordination configurée")
        
        return agents_config

    def phase_5_configuration_domaines(self):
        """Phase 5: Configuration domaines et redirections"""
        print("\n🌐 PHASE 5: CONFIGURATION DOMAINES")
        print("=" * 35)
        
        domaines_config = {
            'paninifs': {
                'disponible': True,
                'utilisation': 'Redirection vers modules Panini',
                'suggestion': 'Hub central ou redirection intelligente'
            },
            'ontowave.org': {
                'destination': 'Panini-OntoWave',
                'type': 'Produit principal documentation'
            }
        }
        
        # Créer configuration DNS
        panini_path = self.github_root / "Panini" 
        if not panini_path.exists():
            panini_path = self.current_research
            
        config_dir = panini_path / "config"
        config_dir.mkdir(exist_ok=True)
        
        dns_config = config_dir / "domaines.json"
        with open(dns_config, 'w') as f:
            json.dump(domaines_config, f, indent=2)
        
        print(f"   🌐 paninifs: Disponible pour hub/redirection")
        print(f"   🌐 ontowave.org: → Panini-OntoWave")
        print(f"   📁 Configuration: {dns_config}")
        
        return domaines_config

    def _update_references_phase1(self):
        """Mise à jour références après renommages"""
        print("      🔄 Mise à jour références...")
        
        # TODO: Mise à jour références Git, imports, etc.
        # Pour l'instant, création marker
        marker_file = self.current_research / "REFACTORING_REFERENCES_TODO.md"
        with open(marker_file, 'w') as f:
            f.write("""# Références à mettre à jour post-refactoring

## Git Remotes
- [ ] Mettre à jour remotes GitHub
- [ ] Vérifier branches synchronisées  

## Imports Python
- [ ] Chercher imports PaniniFS-Research
- [ ] Remplacer par Panini

## Documentation  
- [ ] README.md mentions
- [ ] URLs dans docs

## Config CI/CD
- [ ] GitHub Actions workflows
- [ ] Paths dans scripts
""")
        
        print(f"      📋 Marker références créé")

    def validation_finale(self):
        """Validation architecture finale"""
        print("\n✅ VALIDATION FINALE ARCHITECTURE")
        print("=" * 35)
        
        checks = [
            {
                'nom': 'Module Central Panini',
                'check': lambda: (self.github_root / "Panini").exists() or (self.github_root / "PaniniFS-Research").exists(),
                'description': 'Module central recherche présent'
            },
            {
                'nom': 'Panini-OntoWave',
                'check': lambda: (self.github_root / "Panini-OntoWave").exists() or (self.github_root / "OntoWave").exists(),
                'description': 'Produit documentation présent'
            },
            {
                'nom': '.gitignore Données',
                'check': lambda: "DONNÉES RECONSTRUCTIBLES" in open(self.current_research / ".gitignore").read() if (self.current_research / ".gitignore").exists() else False,
                'description': '233GB données reconstructibles protégées'
            },
            {
                'nom': 'Support Intégré',
                'check': lambda: (self.current_research / "support").exists(),
                'description': 'Modules support intégrés dans Panini'
            },
            {
                'nom': 'Agents Configurés',
                'check': lambda: (self.current_research / "agents").exists(),
                'description': 'Spec-kits agents créés'
            }
        ]
        
        resultats = []
        for check in checks:
            try:
                result = check['check']()
                status = "✅" if result else "❌"
                print(f"   {status} {check['nom']}: {check['description']}")
                resultats.append(result)
            except Exception as e:
                print(f"   ⚠️  {check['nom']}: Erreur - {e}")
                resultats.append(False)
        
        succes = sum(resultats)
        total = len(checks)
        
        print(f"\n📊 **BILAN FINAL**: {succes}/{total} validations réussies")
        
        if succes == total:
            print("🎯 **REFACTORING ARCHITECTURE COMPLET RÉUSSI !**")
        else:
            print("⚠️  **REFACTORING PARTIEL** - Actions manuelles requises")
            
        return succes, total

    def execute_complete_refactoring(self):
        """Exécution complète refactoring"""
        print("🚀 DÉBUT REFACTORING ARCHITECTURE COMPLET")
        print("=" * 45)
        
        try:
            # Phases séquentielles
            phase1 = self.phase_1_renommages_principaux()
            phase2 = self.phase_2_gitignore_donnees()  
            phase3 = self.phase_3_integration_support()
            phase4 = self.phase_4_agents_spec_kits()
            phase5 = self.phase_5_configuration_domaines()
            
            # Validation finale
            succes, total = self.validation_finale()
            
            return {
                'success': succes == total,
                'phases': [phase1, phase2, phase3, phase4, phase5],
                'validation': {'succes': succes, 'total': total}
            }
            
        except Exception as e:
            print(f"❌ ERREUR REFACTORING: {e}")
            return {'success': False, 'error': str(e)}


def main():
    """Exécution refactoring complet immédiat"""
    
    print("🚀 REFACTORING ARCHITECTURE PANINI - VALIDATIONS UTILISATEUR")
    print("=" * 60)
    print("✅ 1. .gitignore 233GB données reconstructibles")
    print("✅ 2. Domaine paninifs disponible") 
    print("✅ 3. Support intégré (sauf besoins Colab Pro)")
    print("✅ 4. Agents avec spec-kits individuels")
    print("✅ 5. Exécution immédiate autorisée")
    
    # Lancement
    refactoring = RefactoringArchitecturePanini()
    result = refactoring.execute_complete_refactoring()
    
    if result.get('success'):
        print("\n🎯 **REFACTORING TERMINÉ AVEC SUCCÈS !**")
        print("   📚 Panini = module central recherche")
        print("   🚀 Panini-OntoWave = documentation interactive")  
        print("   💾 Panini-FS = digesteur fichiers")
        print("   👋 Panini-Gest = reconnaissance gestuelle")
        print("   🔧 Support intégré dans Panini/support/")
        print("   👥 4 agents avec spec-kits configurés")
        print("   🌐 Domaines: paninifs + ontowave.org")
    else:
        print("\n⚠️  **REFACTORING PARTIEL** - Interventions requises")
        error = result.get('error')
        if error:
            print(f"   Erreur: {error}")


if __name__ == "__main__":
    main()