#!/usr/bin/env python3
"""
📊 PANINI-FS REPOSITORY STATUS VIEWER
============================================================
🎯 Mission: Visualiser état des repositories Git PaniniFS
🔬 Focus: Status, contenus, synchronisation, statistiques
🚀 Usage: Monitoring et audit de l'architecture multi-repos

Visualiseur d'état pour l'architecture Git distribuée PaniniFS.
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import os

class PaniniReposStatusViewer:
    """Visualiseur d'état repositories PaniniFS"""
    
    def __init__(self, repos_root: str = "repos"):
        self.repos_root = Path(repos_root)
        
    def analyze_all_repositories(self) -> Dict[str, Any]:
        """Analyser tous les repositories"""
        print("📊 PANINI-FS REPOSITORY STATUS VIEWER")
        print("="*50)
        print(f"🔍 Analyse repositories dans: {self.repos_root.absolute()}")
        
        if not self.repos_root.exists():
            print("❌ Dossier repos non trouvé")
            return {}
        
        repos = list(self.repos_root.glob("panini-*"))
        if not repos:
            print("❌ Aucun repository PaniniFS trouvé")
            return {}
        
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'repos_root': str(self.repos_root.absolute()),
            'repositories': {},
            'summary': {}
        }
        
        print(f"📁 Repositories trouvés: {len(repos)}")
        
        for repo_path in repos:
            repo_name = repo_path.name
            print(f"\n🔍 Analyse {repo_name}...")
            
            repo_analysis = self.analyze_single_repository(repo_path)
            analysis['repositories'][repo_name] = repo_analysis
        
        # Générer résumé
        analysis['summary'] = self.generate_summary(analysis['repositories'])
        
        self.display_analysis(analysis)
        return analysis
    
    def analyze_single_repository(self, repo_path: Path) -> Dict[str, Any]:
        """Analyser un repository individuel"""
        analysis = {
            'name': repo_path.name,
            'path': str(repo_path),
            'is_git_repo': False,
            'git_status': {},
            'content_analysis': {},
            'files_count': 0,
            'directories': [],
            'knowledge_content': {},
            'errors': []
        }
        
        try:
            # Vérifier si c'est un repo Git
            git_dir = repo_path / '.git'
            if git_dir.exists():
                analysis['is_git_repo'] = True
                analysis['git_status'] = self.get_git_status(repo_path)
            
            # Analyser contenu
            analysis['content_analysis'] = self.analyze_repository_content(repo_path)
            
            # Compter fichiers
            files = list(repo_path.rglob('*'))
            analysis['files_count'] = len([f for f in files if f.is_file()])
            
            # Lister dossiers principaux
            analysis['directories'] = [d.name for d in repo_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
            
            # Analyser contenu spécialisé
            if 'knowledge' in repo_path.name:
                analysis['knowledge_content'] = self.analyze_knowledge_content(repo_path)
            elif 'data-models' in repo_path.name:
                analysis['knowledge_content'] = self.analyze_data_models_content(repo_path)
            
        except Exception as e:
            analysis['errors'].append(str(e))
        
        return analysis
    
    def get_git_status(self, repo_path: Path) -> Dict[str, Any]:
        """Obtenir status Git du repository"""
        git_status = {
            'has_commits': False,
            'last_commit': None,
            'branch': None,
            'uncommitted_changes': False,
            'commit_count': 0
        }
        
        original_cwd = os.getcwd()
        
        try:
            os.chdir(repo_path)
            
            # Vérifier commits
            try:
                result = subprocess.run(['git', 'rev-list', '--count', 'HEAD'], 
                                      capture_output=True, text=True, check=True)
                git_status['commit_count'] = int(result.stdout.strip())
                git_status['has_commits'] = git_status['commit_count'] > 0
            except:
                pass
            
            # Dernier commit
            if git_status['has_commits']:
                try:
                    result = subprocess.run(['git', 'log', '-1', '--format=%h %s (%ci)'], 
                                          capture_output=True, text=True, check=True)
                    git_status['last_commit'] = result.stdout.strip()
                except:
                    pass
            
            # Branche actuelle
            try:
                result = subprocess.run(['git', 'branch', '--show-current'], 
                                      capture_output=True, text=True, check=True)
                git_status['branch'] = result.stdout.strip()
            except:
                pass
            
            # Changements non commités
            try:
                result = subprocess.run(['git', 'status', '--porcelain'], 
                                      capture_output=True, text=True, check=True)
                git_status['uncommitted_changes'] = bool(result.stdout.strip())
            except:
                pass
                
        except Exception as e:
            git_status['error'] = str(e)
        finally:
            os.chdir(original_cwd)
        
        return git_status
    
    def analyze_repository_content(self, repo_path: Path) -> Dict[str, Any]:
        """Analyser contenu du repository"""
        content = {
            'has_readme': False,
            'config_files': [],
            'json_files': [],
            'data_files': [],
            'structure_complete': False
        }
        
        # README
        readme_files = list(repo_path.glob('README*'))
        content['has_readme'] = len(readme_files) > 0
        
        # Fichiers JSON
        json_files = list(repo_path.rglob('*.json'))
        content['json_files'] = [str(f.relative_to(repo_path)) for f in json_files]
        
        # Fichiers de config
        config_patterns = ['*config*', '*.toml', '*.yaml', '*.yml']
        for pattern in config_patterns:
            config_files = list(repo_path.rglob(pattern))
            content['config_files'].extend([str(f.relative_to(repo_path)) for f in config_files])
        
        # Structure attendue selon type de repo
        if 'data-models' in repo_path.name:
            expected_dirs = ['models', 'metadata', 'hashes', 'indexes']
        else:  # knowledge repos
            expected_dirs = ['encyclopedia', 'graphs', 'knowledge', 'exports']
        
        existing_dirs = [d.name for d in repo_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
        content['structure_complete'] = all(dir_name in existing_dirs for dir_name in expected_dirs)
        content['missing_dirs'] = [d for d in expected_dirs if d not in existing_dirs]
        
        return content
    
    def analyze_knowledge_content(self, repo_path: Path) -> Dict[str, Any]:
        """Analyser contenu encyclopédie"""
        knowledge = {
            'concepts_files': 0,
            'relations_files': 0,
            'insights_files': 0,
            'latest_content': None,
            'access_level': 'unknown'
        }
        
        # Compter fichiers par type
        concepts_dir = repo_path / 'encyclopedia' / 'concepts'
        if concepts_dir.exists():
            knowledge['concepts_files'] = len(list(concepts_dir.glob('*.json')))
        
        relations_dir = repo_path / 'encyclopedia' / 'relations'
        if relations_dir.exists():
            knowledge['relations_files'] = len(list(relations_dir.glob('*.json')))
        
        # Déterminer niveau d'accès
        if 'public' in repo_path.name:
            knowledge['access_level'] = 'public'
        elif 'private' in repo_path.name:
            knowledge['access_level'] = 'private'
        elif 'team' in repo_path.name:
            knowledge['access_level'] = 'team'
        
        # Dernier contenu ajouté
        all_json = list(repo_path.rglob('*.json'))
        if all_json:
            latest_file = max(all_json, key=lambda f: f.stat().st_mtime)
            knowledge['latest_content'] = str(latest_file.relative_to(repo_path))
        
        return knowledge
    
    def analyze_data_models_content(self, repo_path: Path) -> Dict[str, Any]:
        """Analyser contenu data models"""
        data_models = {
            'digested_models': 0,
            'semantic_models': 0,
            'metadata_files': 0,
            'hash_files': 0,
            'latest_model': None
        }
        
        # Compter modèles
        digested_dir = repo_path / 'models' / 'digested'
        if digested_dir.exists():
            data_models['digested_models'] = len(list(digested_dir.glob('*.json')))
        
        semantic_dir = repo_path / 'models' / 'semantic'
        if semantic_dir.exists():
            data_models['semantic_models'] = len(list(semantic_dir.glob('*.json')))
        
        metadata_dir = repo_path / 'metadata'
        if metadata_dir.exists():
            data_models['metadata_files'] = len(list(metadata_dir.glob('*')))
        
        # Dernier modèle
        models_files = list((repo_path / 'models').rglob('*.json')) if (repo_path / 'models').exists() else []
        if models_files:
            latest_model = max(models_files, key=lambda f: f.stat().st_mtime)
            data_models['latest_model'] = str(latest_model.relative_to(repo_path))
        
        return data_models
    
    def generate_summary(self, repositories: Dict[str, Any]) -> Dict[str, Any]:
        """Générer résumé de l'analyse"""
        summary = {
            'total_repositories': len(repositories),
            'git_repositories': 0,
            'repositories_with_content': 0,
            'total_commits': 0,
            'total_files': 0,
            'knowledge_repositories': 0,
            'data_repositories': 0,
            'sync_status': 'unknown'
        }
        
        for repo_name, repo_data in repositories.items():
            if repo_data.get('is_git_repo'):
                summary['git_repositories'] += 1
            
            if repo_data.get('files_count', 0) > 1:  # Plus que juste README
                summary['repositories_with_content'] += 1
            
            summary['total_commits'] += repo_data.get('git_status', {}).get('commit_count', 0)
            summary['total_files'] += repo_data.get('files_count', 0)
            
            if 'knowledge' in repo_name:
                summary['knowledge_repositories'] += 1
            elif 'data' in repo_name:
                summary['data_repositories'] += 1
        
        # Status de sync basé sur présence de contenu
        has_data_content = any('data' in name and repo.get('files_count', 0) > 1 
                              for name, repo in repositories.items())
        has_knowledge_content = any('knowledge' in name and repo.get('files_count', 0) > 1 
                                   for name, repo in repositories.items())
        
        if has_data_content and has_knowledge_content:
            summary['sync_status'] = 'synchronized'
        elif has_data_content:
            summary['sync_status'] = 'data_only'
        else:
            summary['sync_status'] = 'empty'
        
        return summary
    
    def display_analysis(self, analysis: Dict[str, Any]):
        """Afficher analyse complète"""
        print(f"\n📊 RÉSUMÉ GLOBAL")
        print("="*30)
        
        summary = analysis['summary']
        print(f"📁 Repositories totaux: {summary['total_repositories']}")
        print(f"🔧 Repositories Git: {summary['git_repositories']}")
        print(f"📄 Fichiers totaux: {summary['total_files']}")
        print(f"💾 Commits totaux: {summary['total_commits']}")
        print(f"📚 Encyclopédies: {summary['knowledge_repositories']}")
        print(f"🔍 Data models: {summary['data_repositories']}")
        print(f"🔄 Status sync: {summary['sync_status']}")
        
        print(f"\n📂 DÉTAILS PAR REPOSITORY")
        print("="*30)
        
        for repo_name, repo_data in analysis['repositories'].items():
            self.display_repository_details(repo_data)
    
    def display_repository_details(self, repo_data: Dict[str, Any]):
        """Afficher détails d'un repository"""
        name = repo_data['name']
        
        # Emoji selon type
        if 'public' in name:
            emoji = '🌐'
        elif 'private' in name:
            emoji = '🔒'
        elif 'team' in name:
            emoji = '👥'
        elif 'data' in name:
            emoji = '📊'
        else:
            emoji = '📁'
        
        print(f"\n{emoji} {name}")
        print(f"   📍 {repo_data['path']}")
        
        # Status Git
        if repo_data['is_git_repo']:
            git_status = repo_data['git_status']
            print(f"   🔧 Git: ✅ ({git_status.get('commit_count', 0)} commits)")
            if git_status.get('last_commit'):
                print(f"   💾 Dernier commit: {git_status['last_commit']}")
        else:
            print(f"   🔧 Git: ❌")
        
        # Contenu
        print(f"   📄 Fichiers: {repo_data['files_count']}")
        print(f"   📂 Dossiers: {', '.join(repo_data['directories'])}")
        
        # Contenu spécialisé
        knowledge = repo_data.get('knowledge_content', {})
        if 'knowledge' in name:
            concepts = knowledge.get('concepts_files', 0)
            access = knowledge.get('access_level', 'unknown')
            print(f"   📚 Concepts: {concepts} fichiers")
            print(f"   🔐 Accès: {access}")
            if knowledge.get('latest_content'):
                print(f"   ⏰ Dernier: {knowledge['latest_content']}")
        elif 'data' in name:
            models = knowledge.get('digested_models', 0)
            print(f"   🔍 Modèles digérés: {models}")
            if knowledge.get('latest_model'):
                print(f"   ⏰ Dernier: {knowledge['latest_model']}")
        
        # Erreurs
        if repo_data.get('errors'):
            print(f"   ⚠️  Erreurs: {', '.join(repo_data['errors'])}")

def main():
    """Point d'entrée principal"""
    viewer = PaniniReposStatusViewer()
    analysis = viewer.analyze_all_repositories()
    
    # Sauvegarder analyse
    if analysis:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        analysis_file = Path(f"panini_repos_analysis_{timestamp}.json")
        
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Analyse sauvegardée: {analysis_file}")
        
        print(f"\n🚀 COMMANDES UTILES:")
        print(f"cd repos/panini-data-models && git log --oneline")
        print(f"find repos -name '*.json' | wc -l")
        print(f"python3 demo_repo_sync.py  # Re-tester sync")

if __name__ == "__main__":
    main()